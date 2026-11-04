#!/usr/bin/env python3
"""Tsukuroi R78 seat ExecHost — read-only journald storage accounting.

Metadata only: never reads journal file contents, raw config output, or env.
Machine-id dir names and file basenames are kept in memory only and are never
written to receipts, stdout, or any file.
"""
import datetime
import json
import os
import re
import stat as st_m
import subprocess

SEAT = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-78/w1/ExecHost"
RECEIPTS = os.path.join(SEAT, "receipts")
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
JROOT = "/var/log/journal"
CLAIM = "07a607df1a5157daafc91bb5c26858af14415f43"
BASE = "b9019a1d0558241bf67cf31ff90256284d8657af"
DIRECTIVE_RE = re.compile(r"^\s*#?\s*(Storage|SystemMaxUse|RuntimeMaxUse|SystemKeepFree|RuntimeKeepFree)\s*=")


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def receipt(pid, cmd, rc, out, note=None):
    body = "utc=%s\nrc=%s\ncmd=%s\n" % (utc(), rc, cmd)
    if note:
        body += "note=%s\n" % note
    body += "---\n" + out
    if not body.endswith("\n"):
        body += "\n"
    with open(os.path.join(RECEIPTS, pid + ".txt"), "w") as f:
        f.write(body)
    print("[receipt] %s rc=%s cmd=%s" % (pid, rc, cmd))


def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True)
    out = p.stdout
    if p.stderr.strip():
        out += ("" if not out or out.endswith("\n") else "\n") + "[stderr] " + p.stderr.strip()
    return p.returncode, out


def main():
    print("start_utc=%s" % utc())

    # P1: systemd package version
    rc, out = run(["pacman", "-Q", "systemd"])
    receipt("P1-pacman-Q-systemd", "pacman -Q systemd", rc, out)

    # P2: filesystem stats backing /var/log/journal
    rc, out = run(["stat", "-f", JROOT])
    receipt("P2-stat-f-var-log-journal", "stat -f /var/log/journal", rc, out)

    # P3: disk usage as unprivileged user (scope: what this user can see)
    rc, out = run(["journalctl", "--disk-usage"])
    receipt("P3-journalctl-disk-usage-user", "journalctl --disk-usage", rc, out)

    # P4: disk usage with read access to system journal (metadata only)
    rc, out = run(["sudo", "-n", "journalctl", "--disk-usage"])
    receipt("P4-journalctl-disk-usage-sudo", "sudo -n journalctl --disk-usage", rc, out)

    # P5: journald.conf effective config, filtered to the five safe directives
    rc, out = run(["systemd-analyze", "cat-config", "systemd/journald.conf"])
    if rc == 0:
        lines = []
        for ln in out.splitlines():
            m = DIRECTIVE_RE.match(ln)
            if m:
                tag = "commented" if ln.lstrip().startswith("#") else "active"
                lines.append("[%s] %s" % (tag, ln.strip()))
        filtered = "\n".join(lines) if lines else "(no matching directive lines)"
        receipt("P5-journald-conf-directives",
                "systemd-analyze cat-config systemd/journald.conf | filter: ^#?(Storage|SystemMaxUse|RuntimeMaxUse|SystemKeepFree|RuntimeKeepFree)=",
                rc, filtered, note="only the five declared-safe directive lines retained; raw output discarded")
    else:
        receipt("P5-journald-conf-directives",
                "systemd-analyze cat-config systemd/journald.conf", rc, out)

    # P6: metadata-only aggregation, unprivileged scandir/lstat
    agg = {
        "method": "python os.scandir + DirEntry.stat(follow_symlinks=False), depth=immediate machine-id dirs",
        "root_scandir_error": None,
        "machine_id_dirs": 0,
        "dir_list_errors": 0,
        "suffix_matched": {},
        "regular_nonmatching_suffix": 0,
        "nonregular_ignored": 0,
        "stat_errors": 0,
        "total_files_matched": 0,
        "total_allocated_bytes": 0,
        "total_apparent_bytes": 0,
    }
    names = []  # in-memory only
    try:
        top = list(os.scandir(JROOT))
    except OSError as e:
        agg["root_scandir_error"] = "%s errno=%s" % (type(e).__name__, e.errno)
        top = []
    for dent in top:
        try:
            stt = dent.stat(follow_symlinks=False)
        except OSError:
            agg["stat_errors"] += 1
            continue
        if not st_m.S_ISDIR(stt.st_mode):
            agg["nonregular_ignored"] += 1
            continue
        names.append(dent.path)
    for dpath in names:
        try:
            inner = list(os.scandir(dpath))
        except OSError:
            agg["dir_list_errors"] += 1
            continue
        agg["machine_id_dirs"] += 1
        for f in inner:
            try:
                fs = f.stat(follow_symlinks=False)
            except OSError:
                agg["stat_errors"] += 1
                continue
            if not st_m.S_ISREG(fs.st_mode):
                agg["nonregular_ignored"] += 1
                continue
            sfx = None
            if f.name.endswith(".journal~"):
                sfx = ".journal~"
            elif f.name.endswith(".journal"):
                sfx = ".journal"
            if sfx is None:
                agg["regular_nonmatching_suffix"] += 1
                continue
            rec = agg["suffix_matched"].setdefault(sfx, {"count": 0, "allocated_bytes": 0, "apparent_bytes": 0})
            rec["count"] += 1
            rec["allocated_bytes"] += fs.st_blocks * 512
            rec["apparent_bytes"] += fs.st_size
            agg["total_files_matched"] += 1
            agg["total_allocated_bytes"] += fs.st_blocks * 512
            agg["total_apparent_bytes"] += fs.st_size
    names = None
    receipt("P6-scandir-lstat-aggregation-user",
            "python3: os.scandir/lstat metadata aggregation over /var/log/journal (immediate machine-id dirs)",
            0, json.dumps(agg, indent=2, sort_keys=True),
            note="names never recorded; allocated=st_blocks*512; apparent=st_size")

    # P7: privileged-metadata fallback via allow-listed sudo -n ls/stat only (no interpreter, no cat)
    fb = {
        "method": "sudo -n ls -1 (names in memory) + sudo -n stat -c '%F %s %b'; no names recorded",
        "ran": False,
        "top_entries": 0, "top_nonregular": 0, "top_stat_errors": 0,
        "machine_id_dirs": 0, "dir_list_errors": 0,
        "suffix_matched": {}, "regular_nonmatching_suffix": 0,
        "nonregular_ignored": 0, "stat_errors": 0,
        "total_files_matched": 0, "total_allocated_bytes": 0, "total_apparent_bytes": 0,
    }
    if agg["root_scandir_error"]:
        rc, out = run(["sudo", "-n", "ls", "-1", JROOT])
        receipt("P7a-sudo-ls-journal-root", "sudo -n ls -1 /var/log/journal | count only", rc,
                "entry_count=%d" % len(out.splitlines()) if rc == 0 else out,
                note="names held in memory only")
        if rc == 0:
            fb["ran"] = True
            fb["top_entries"] = len(out.splitlines())
            for n in out.splitlines():
                p = JROOT + "/" + n
                rc2, t = run(["sudo", "-n", "stat", "-c", "%F", p])
                if rc2 != 0:
                    fb["top_stat_errors"] += 1
                    continue
                if t.strip() != "directory":
                    fb["top_nonregular"] += 1
                    continue
                rc3, listing = run(["sudo", "-n", "ls", "-1", p])
                if rc3 != 0:
                    fb["dir_list_errors"] += 1
                    continue
                fb["machine_id_dirs"] += 1
                for fn in listing.splitlines():
                    fp = p + "/" + fn
                    sfx = ".journal~" if fn.endswith(".journal~") else (".journal" if fn.endswith(".journal") else None)
                    rc4, ts = run(["sudo", "-n", "stat", "-c", "%F %s %b", fp])
                    if rc4 != 0:
                        fb["stat_errors"] += 1
                        continue
                    parts = ts.split()
                    kind = parts[0] + (" " + parts[1] if parts[0] == "regular" else "")
                    size = int(parts[-2]); blocks = int(parts[-1])
                    if kind != "regular file":
                        fb["nonregular_ignored"] += 1
                    elif sfx is None:
                        fb["regular_nonmatching_suffix"] += 1
                    else:
                        rec = fb["suffix_matched"].setdefault(sfx, {"count": 0, "allocated_bytes": 0, "apparent_bytes": 0})
                        rec["count"] += 1
                        rec["allocated_bytes"] += blocks * 512
                        rec["apparent_bytes"] += size
                        fb["total_files_matched"] += 1
                        fb["total_allocated_bytes"] += blocks * 512
                        fb["total_apparent_bytes"] += size
            names = None
            receipt("P7-sudo-ls-stat-aggregation",
                    "sudo -n ls -1 + sudo -n stat -c '%F %s %b' aggregation over /var/log/journal",
                    0, json.dumps(fb, indent=2, sort_keys=True),
                    note="allow-listed binaries only; names in memory only; no privileged interpreter")

    # P8: lane state (read-only git)
    rc, out = run(["git", "-C", LANE, "rev-parse", "HEAD"])
    receipt("P8a-lane-head", "git -C <lane> rev-parse HEAD", rc, out)
    rc, out = run(["git", "-C", LANE, "cat-file", "-t", CLAIM])
    receipt("P8b-lane-claim-commit-type", "git -C <lane> cat-file -t <claim-commit>", rc, out)
    rc, out = run(["git", "-C", LANE, "cat-file", "-t", BASE])
    receipt("P8c-lane-base-commit-type", "git -C <lane> cat-file -t <base-commit>", rc, out)

    summary = {"start_utc_utc_now": utc(), "user_aggregation": agg, "sudo_aggregation": fb}
    with open(os.path.join(RECEIPTS, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
    print("done_utc=%s" % utc())


if __name__ == "__main__":
    main()
