#!/usr/bin/env python3
"""C2-7: mechanical quote/claim checker for corpus/knowledge/btrfs-scrub-grounding-r45.md.

Own script (not tools/check-scrub-grounding-r45.py).  Reads the entry at a pinned
revision, verifies the snapshot digests it relies on, then for every
'**Quote.** `Snnn` file:LINE: "text"' line checks that the named snapshot file
holds 'text' on line LINE.  Then re-checks the line-number / function-name /
value claims made inside the three Statement cells against the same snapshots.

Usage: quotecheck.py --lane DIR --revision SHA
"""
import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

W = "corpus/knowledge/btrfs-scrub-grounding-r45.md"

# source token -> (snapshot dir relative to lane, files it covers)
SRC = {
    "S246": (".ufo/waves/round-45/frozen/src", {"cmdline.c", "vsprintf.c", "kstrtox.c"}),
    "S247": (".ufo/waves/round-45/frozen/src", {"dev-replace.c"}),
    "S248": (".ufo/waves/round-45/frozen/src", {"systemd.kill.xml"}),
    "S242": (".ufo/waves/round-44/frozen/src", {"scrub.c"}),
    "S243": (".ufo/waves/round-44/frozen/src", {"sysfs.c"}),
    "S244": (".ufo/waves/round-44/frozen/src", {"btrfs-scrub@.service"}),
    "S237": (".ufo/waves/round-42/frozen/src", {"scrub.c"}),
}
CAPTURE = ".ufo/waves/round-45/frozen/hostcap/capture.txt"
CAPTURE_SHA = "f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70"

QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` (\S+):(\d+): "(.*)"$')
fails = []


def ok(cond, tag, msg):
    print(("  PASS " if cond else "  FAIL ") + tag + ": " + msg)
    if not cond:
        fails.append(tag + ": " + msg)
    return cond


def sha256(p):
    h = hashlib.sha256()
    h.update(Path(p).read_bytes())
    return h.hexdigest()


def verify_digests(lane):
    print("== digest verification (SHA256SUMS, every snapshot the entry cites) ==")
    dirs = sorted({d for d, _ in SRC.values()})
    sums = {}
    for d in dirs:
        dp = Path(lane) / d / "SHA256SUMS"
        entries = {}
        for ln in dp.read_text().splitlines():
            h, name = ln.split()
            entries[name] = h
        for name, h in sorted(entries.items()):
            got = sha256(Path(lane) / d / name)
            ok(got == h, "DIGEST", f"{d}/{name} {got[:16]}… {'==' if got == h else '!='} {h[:16]}…")
        sums[d] = entries
    # every file a quote names must be covered by its dir's SHA256SUMS
    for tok, (d, files) in SRC.items():
        for f in files:
            ok(f in sums[d], "INDEXED", f"{tok} {f} listed in {d}/SHA256SUMS")
    ok(sha256(Path(lane) / CAPTURE) == CAPTURE_SHA, "DIGEST", f"capture.txt == {CAPTURE_SHA[:16]}…")
    return sums


RANGE_RE = re.compile(r"([\w./@-]+\.[A-Za-z0-9]+|PKGBUILD) lines ((?:\d+-\d+)(?:, \d+-\d+)*)")


def sources_ranges(lane, rev):
    """token -> {basename: [(lo, hi), ...]} from corpus/SOURCES.md at the revision."""
    out = subprocess.run(["git", "-C", lane, "show", f"{rev}:corpus/SOURCES.md"],
                         capture_output=True, text=True, check=True).stdout
    ranges = {}
    for row in out.splitlines():
        cells = row.split("|")
        if len(cells) < 3:
            continue
        tok = cells[1].strip()
        if tok not in SRC:
            continue
        for m in RANGE_RE.finditer(row):
            f = m.group(1).split("/")[-1]
            spans = [tuple(int(x) for x in r.split("-")) for r in m.group(2).split(", ")]
            ranges.setdefault(tok, {}).setdefault(f, []).extend(spans)
    return ranges


def range_check(lane, rev, quotes):
    print("\n== quoted lines vs the line ranges corpus/SOURCES.md declares for that source ==")
    ranges = sources_ranges(lane, rev)
    for tok, fname, num in quotes:
        spans = ranges.get(tok, {}).get(fname, [])
        if not spans:
            ok(False, "SOURCES", f"{tok} {fname} has no declared range list")
            continue
        inside = any(lo <= num <= hi for lo, hi in spans)
        ok(inside, "SOURCES-RANGE",
           f"{tok} {fname}:{num} within declared {[f'{a}-{b}' for a, b in spans]}")
    # decisive lines the Statements rely on (not quoted): informative
    extra = [("S242", "scrub.c", 3147, "dev->scrub_ctx || (the 'any call' half of GR2)"),
             ("S237", "scrub.c", 439, "handler assignment fd == -1 ? SIG_DFL : ..."),
             ("S237", "scrub.c", 1546, "foreground install of the SIGINT handler"),
             ("S246", "cmdline.c", 183, "shl += 10 (K step of the 1024 cascade)")]
    for tok, fname, num, why in extra:
        spans = ranges.get(tok, {}).get(fname, [])
        inside = any(lo <= num <= hi for lo, hi in spans)
        print(f"  INFO  {'in' if inside else 'OUTSIDE'} declared ranges: {tok} {fname}:{num} — {why}")


def check_quotes(lane, text):
    print("\n== quote lines (31 expected) ==")
    n = 0
    quotes = []
    for ln, line in enumerate(text.splitlines(), 1):
        m = QUOTE_RE.match(line)
        if not m:
            if "**Quote.**" in line:
                ok(False, "PARSE", f"md:{ln} unparsed quote line: {line!r}")
            continue
        n += 1
        tok, fname, num, quoted = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        d, allowed = SRC.get(tok, (None, set()))
        if d is None or fname not in allowed:
            ok(False, "POINTER", f"md:{ln} {tok} {fname} not a file of that source")
            continue
        p = Path(lane) / d / fname
        lines = p.read_text().splitlines()
        if num < 1 or num > len(lines):
            ok(False, "POINTER", f"md:{ln} {tok} {fname}:{num} out of range (1..{len(lines)})")
            continue
        quotes.append((tok, fname, num))
        named = lines[num - 1].strip()
        exact = named == quoted.strip()
        # fuzzy: the quote must be a contiguous slice of the named line
        contains = quoted.strip() in named
        state = "exact" if exact else ("slice" if contains else "MISMATCH")
        ok(contains, "QUOTE", f"md:{ln} {tok} {fname}:{num} [{state}] {quoted[:64]!r}")
        # fragment test: does the named line continue past the quoted text, or does
        # the next line carry the sentence on / the decisive token?
        rest = named[named.index(quoted.strip()) + len(quoted.strip()):] if contains else ""
        nxt = lines[num].strip() if num < len(lines) else ""
        cont = bool(re.match(r"^[a-z(<]", nxt)) or bool(re.match(r"^[a-z(<]", (lines[num].strip() if num < len(lines) else "")))
        kind = "CUT" if (rest or cont) else "whole-line"
        print(f"       {kind}: tail={rest[:60]!r} next {fname}:{num + 1}: {nxt[:96]!r}")
    ok(n == 31, "COUNT", f"{n} quote lines parsed")
    return quotes


def sim_memparse(s):
    """Transcription of memparse() + simple_strntoull() + _parse_integer_fixup_radix()
    from the S246/S243 snapshots (cmdline.c:153-200, vsprintf.c:79-116, kstrtox.c:26-95).
    Returns (value, end_index) and then the sysfs store's accept/reject."""
    i = 0
    base = 0
    # _parse_integer_fixup_radix
    if base == 0:
        if s[0:1] == "0":
            if len(s) > 2 and s[1].lower() == "x" and s[2] in "0123456789abcdefABCDEF":
                base = 16
            else:
                base = 8
        else:
            base = 10
    if base == 16 and s[0:2].lower() == "0x":
        i += 2
    start = i
    res = 0
    # _parse_integer_limit
    while i < len(s):
        c = s[i]
        lc = c.lower()
        if "0" <= c <= "9":
            val = ord(c) - 48
        elif "a" <= lc <= "f":
            val = ord(lc) - 87
        else:
            break
        if val >= base:
            break
        res = res * base + val
        i += 1
    ret, endptr = res, i
    # memparse suffix switch, E P T G M K cascade, shl += 10 each
    shl = 0
    ch = s[endptr:endptr + 1]
    order = "EPTGMK"
    if ch and ch.upper() in order:
        shl = (len(order) - order.index(ch.upper())) * 10
    if shl and endptr != 0:
        if ret > (2**64 - 1) >> shl:
            ret = 2**64 - 1          # check_shl_overflow -> ULLONG_MAX
        else:
            ret <<= shl              # the 10-bit shift per cascade step
        endptr += 1
    # store: skip_spaces then *endptr != 0 -> -EINVAL
    while endptr < len(s) and s[endptr] in " \t\n\r\f\v":
        endptr += 1
    if endptr != len(s):
        return None  # -EINVAL
    return ret


def claim_checks(lane):
    print("\n== Statement-cell claims ==")
    r45 = Path(lane) / SRC["S246"][0]
    r44 = Path(lane) / SRC["S242"][0]
    r42 = Path(lane) / SRC["S237"][0]
    cmdline = (r45 / "cmdline.c").read_text().splitlines()
    vsprintf = (r45 / "vsprintf.c").read_text().splitlines()
    kstrtox = (r45 / "kstrtox.c").read_text().splitlines()
    sysfs = (r44 / "sysfs.c").read_text().splitlines()
    scrub44 = (r44 / "scrub.c").read_text().splitlines()
    devrep = (r45 / "dev-replace.c").read_text().splitlines()
    xml = (r45 / "systemd.kill.xml").read_text().splitlines()
    unit = (r44 / "btrfs-scrub@.service").read_text().splitlines()
    scrub42 = (r42 / "scrub.c").read_text().splitlines()
    cap = [l for l in (Path(lane) / CAPTURE).read_text().splitlines() if l]

    print("-- GR1: memparse / simple_strtoull / radix / store")
    ok(cmdline[152].startswith("unsigned long long memparse("), "GR1-fn", "memparse defined at cmdline.c:153")
    ok("memparse(buf, &endptr)" in sysfs[2039], "GR1-line", "sysfs.c:2040 is memparse(buf,&endptr)")
    ok("skip_spaces(endptr)" in sysfs[2041] and "*endptr != 0" in sysfs[2042]
       and "-EINVAL" in sysfs[2043], "GR1-line", "sysfs.c:2042 skip_spaces, :2043 test, :2044 -EINVAL")
    ok("scrub_speed_max" in sysfs[2047], "GR1-fn", "attr wired as devid/scrub_speed_max (sysfs.c:2048)")
    ok("simple_strtoull(ptr, &endptr, 0)" in cmdline[155], "GR1-line", "memparse base 0 at cmdline.c:156")
    ok("return simple_strntoull(cp, endp, base, INT_MAX)" in vsprintf[113], "GR1-hop",
       "simple_strtoull -> simple_strntoull (vsprintf.c:114); quote points at :86, two hops in")
    ok("_parse_integer_fixup_radix(startp, &base)" in vsprintf[85], "GR1-line", "fixup at vsprintf.c:86")
    ok("_parse_integer_fixup_radix(const char *s" in kstrtox[25], "GR1-fn", "fixup defined kstrtox.c:26")
    ok("*base = 16" in kstrtox[30], "GR1-value", "0x+hexdigit -> base 16 (kstrtox.c:31)")
    ok("*base = 8" in kstrtox[32], "GR1-value", "other leading 0 -> base 8 (kstrtox.c:33)")
    ok("*base = 10" in kstrtox[34], "GR1-value", "else -> base 10 (kstrtox.c:35)")
    ok("s += 2" in kstrtox[37], "GR1-value", "0x prefix consumed (kstrtox.c:38)")
    shl_adds = [i + 1 for i, l in enumerate(cmdline) if "shl += 10" in l]
    ok(len(shl_adds) == 6, "GR1-value", f"six 'shl += 10' steps at cmdline.c:{shl_adds}")
    cases = [l.strip() for l in cmdline[159:187]]
    letters = [re.match(r"case '([A-Za-z])':", c).group(1) for c in cases
               if re.match(r"case '([A-Za-z])':", c)]
    ok(letters == ["E", "e", "P", "p", "T", "t", "G", "g", "M", "m", "K", "k"],
       "GR1-value", "switch cascades E->P->T->G->M->K, both cases each")
    casc = [(n, cmdline[n].strip()) for n in shl_adds]
    ok(all(nxt == "fallthrough;" for _, nxt in casc), "GR1-value",
       "each 'shl += 10' is followed by fallthrough (cascade, no break): " + str(casc))
    shifts = {ch: (len(letters) // 2 - letters.index(ch) // 2) * 10 for ch in "KMGTPE"}
    ok(shifts == {"K": 10, "M": 20, "G": 30, "T": 40, "P": 50, "E": 60}, "GR1-value",
       f"10-bit shift per step: {shifts} -> K=1024, M=1024**2 (not 1000-based)")
    ok("shl && likely(ptr != endptr)" in cmdline[188], "GR1-line", "suffix needs consumed chars (cmdline.c:189)")
    ok("check_shl_overflow(ret, shl, &ret)" in cmdline[190] and "ULLONG_MAX" in cmdline[191],
       "GR1-line", "overflow -> ULLONG_MAX (cmdline.c:191-192)")
    ok("endptr++" in cmdline[192], "GR1-value", "exactly one suffix char consumed (cmdline.c:193)")
    table = {"100M": 104857600, "100m": 104857600, "010": 8, "0x10": 16,
             "10MB": None, "10 M": None, "-1": None, "\n": 0, "5K": 5120,
             "0x1F": 31, "1G": 1073741824, "K": None, "": 0}
    bad = {k: (sim_memparse(k), v) for k, v in table.items() if sim_memparse(k) != v}
    ok(not bad, "GR1-sim", f"example table reproduced from the snapshot code: {table}" if not bad else f"{bad}")
    ok("bwlimit = READ_ONCE(device->scrub_speed_max)" in scrub44[1379]
       and "if (bwlimit == 0)" in scrub44[1380] and "return;" in scrub44[1381],
       "GR1-value", "0 means no limit: scrub.c:1380-1382 returns before throttling (S242; not quoted in GR1)")

    print("-- GR2: btrfs_scrub_dev signature, call sites, EINPROGRESS condition")
    sig = " ".join(l.strip() for l in scrub44[3078:3081])
    params = [p.strip().split()[-1].lstrip("*") for p in
              " ".join(l.strip() for l in scrub44[3078:3081]).split("(", 1)[1].rsplit(")", 1)[0].split(",")]
    ok(params == ["fs_info", "devid", "start", "end", "progress", "readonly", "is_dev_replace"],
       "GR2-value", f"btrfs_scrub_dev params at scrub.c:3079-3081 = {params}; last two = readonly, is_dev_replace")
    i701, i703 = devrep[700], devrep[702]
    ok("src_device->devid" in i701 and i703.strip().endswith("false, true);"), "GR2-value",
       "replace-start call dev-replace.c:701-703: src_device->devid, ..., false, true")
    ok("dev_replace->srcdev->devid" in devrep[1264] and devrep[1267].strip().endswith("false, true);"),
       "GR2-value", "replace-continue call dev-replace.c:1265-1268: srcdev->devid, ..., false, true")
    encl = lambda ln: max(i for i, l in enumerate(devrep[:ln]) if re.match(r"^(static )?\w[\w \*]*\(", l)) + 1
    ok("btrfs_dev_replace_start" in devrep[encl(701) - 1], "GR2-fn",
       f"dev-replace.c:701 sits in btrfs_dev_replace_start (decl {encl(701)})")
    ok("btrfs_dev_replace_kthread" in devrep[encl(1265) - 1], "GR2-fn",
       f"dev-replace.c:1265 sits in btrfs_dev_replace_kthread (decl {encl(1265)})")
    cond = " ".join(l.strip() for l in scrub44[3146:3149])
    ok("dev->scrub_ctx || (!is_dev_replace &&" in cond.replace("  ", " ") or
       ("dev->scrub_ctx ||" in scrub44[3146] and "(!is_dev_replace &&" in scrub44[3147]),
       "GR2-value", "condition scrub.c:3147 dev->scrub_ctx || 3148 (!is_dev_replace && ...: "
                    "'any call' is the first disjunct, unguarded by is_dev_replace")
    ok("!is_dev_replace && btrfs_dev_replace_is_ongoing" not in "".join(
        l.replace("||", "") for l in scrub44[3146:3149]).split("dev->scrub_ctx")[0],
       "GR2-value", "the is_dev_replace guard applies only to the replace-ongoing disjunct")
    ok("-EINPROGRESS" in scrub44[3152] and "down_read(&fs_info->dev_replace.rwsem)" in scrub44[3145],
       "GR2-value", "refusal under dev_replace.rwsem read-lock, ret -EINPROGRESS at scrub.c:3153")
    ioctl_hops = [i + 1 for i, l in enumerate(scrub44)
                  if "BTRFS_IOC_SCRUB" in l or "scrub_ioctl" in l]
    ok(not ioctl_hops, "GR2-hop",
       f"no scrub ioctl handler / BTRFS_IOC_SCRUB in S242 scrub.c (hits={ioctl_hops}); the ioctl->btrfs_scrub_dev "
       "hop lives in fs/btrfs/ioctl.c, which no cited snapshot holds")

    print("-- GR3: unit file, systemd.kill.xml, SIGINT handler")
    ok(unit[8].strip() == "KillSignal=SIGINT", "GR3-line", "unit:9 KillSignal=SIGINT")
    ok(unit[9].strip() == "ExecStart=/usr/bin/btrfs scrub start -B %f", "GR3-line",
       "unit:10 ExecStart=btrfs scrub start -B")
    ok(not any("KillMode" in l for l in unit), "GR3-value", f"unit sets no KillMode (10 lines total: {len(unit)})")
    ok("Defaults to <option>control-group</option>" in xml[100], "GR3-value",
       "xml:101 KillMode defaults to control-group")
    ok("Defaults to <constant>SIGTERM</constant>" in xml[111], "GR3-value", "xml:112 KillSignal defaults to SIGTERM")
    ok("SIGCONT" in xml[114], "GR3-value",
       "the SIGCONT token sits on xml:115, one line past the quoted xml:114 which stops at 'always send'")
    ok("FinalKillSignal=" in xml[96] and "SendSIGKILL=" in xml[96], "GR3-value",
       "xml:97 carries FinalKillSignal=/SendSIGKILL=, one line past the quoted xml:96")
    ok("SIGKILL" in xml[95], "GR3-value", "xml:96 names SIGKILL (quoted line, complete clause start)")
    fore = [i + 1 for i, l in enumerate(scrub42) if "do_background = false" in l]
    ok(1292 <= fore[0] <= 1295, "GR3-line", f"-B sets do_background=false at scrub.c:{fore[0]}")
    ok("scrub_handle_sigint_child(fdmnt)" in scrub42[1545], "GR3-line",
       "foreground path installs the child handler at scrub.c:1546 (fork path is inside if(do_background))")
    ok("fd == -1 ? SIG_DFL : scrub_sigint_record_progress" in scrub42[438], "GR3-value",
       "handler = scrub_sigint_record_progress when fd != -1 (scrub.c:439)")
    ok("BTRFS_IOC_SCRUB_CANCEL" in scrub42[420], "GR3-line",
       "handler issues BTRFS_IOC_SCRUB_CANCEL at scrub.c:421 inside scrub_sigint_record_progress")
    ok("scan" not in scrub42[416] and scrub42[416].strip().startswith("static void scrub_sigint_record_progress"),
       "GR3-fn", "scrub.c:417 is a signal handler (int signal) — SIGINT reaches an async handler, not the main loop")
    ok("scrub_handle_sigint_parent()" in scrub42[1521], "GR3-value",
       "parent ignores SIGINT only on the forked background path (scrub.c:1522)")

    print("-- host values (Statement 'Host reading' cells vs S249 capture)")
    ok("KillMode=control-group" in cap[2] and "KillSignal=2" in cap[2] and "SendSIGKILL=yes" in cap[2]
       and "TimeoutStopUSec=5s" in cap[2] and "FinalKillSignal=9" in cap[2], "HOST",
       "capture.txt:3 matches GR3's systemctl show list exactly")
    ok("DefaultTimeoutStopSec=5s" in cap[3] and cap[3].startswith("stop_default") and ":2:" in cap[3],
       "HOST", "capture.txt:4 drop-in line 2 DefaultTimeoutStopSec=5s")
    ok(cap[4] == "dropin_owner /etc/systemd/system.conf.d/10-faster-shutdown.conf none", "HOST",
       "capture.txt:5 no package owns the drop-in")
    ok("uid=1000" in cap[0] and "CapEff=0000000000000000" in cap[0], "HOST",
       "capture.txt:1 uid 1000, empty effective capability set")
    ok("mode=644 owner=root value=0" in cap[7], "HOST", "capture.txt:8 scrub_speed_max 0/644/root on devid 1")
    ok("devids=1" in cap[8], "HOST", "capture.txt:9 single devid")
    ok("systemd 262 (262-1-arch)" in cap[1] and "7.2.11-arch1-1" in cap[1], "HOST",
       "capture.txt:2 kernel 7.2.11-arch1-1, systemd 262-1-arch")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--revision", required=True)
    a = ap.parse_args()
    text = subprocess.run(["git", "-C", a.lane, "show", f"{a.revision}:{W}"],
                          capture_output=True, text=True, check=True).stdout
    print(f"doc {W} at {a.revision}: {len(text.encode())} bytes")
    verify_digests(a.lane)
    quotes = check_quotes(a.lane, text)
    range_check(a.lane, a.revision, quotes)
    claim_checks(a.lane)
    print(f"\n== {len(fails)} FAIL ==")
    for f in fails:
        print("  " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
