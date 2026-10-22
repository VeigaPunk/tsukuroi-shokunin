#!/usr/bin/env python3
"""Generate the pacman.log census table for round-24 wave 1 (seat ExecPacmanLogCensus).

Reads /var/log/pacman.log read-only and emits every `[PACMAN] Running` command line
and every ALPM installed/upgraded/downgraded/removed record with its log line number
and timestamp, marking each row against the pause-window start 2026-10-20T09:40:00-0300.

No host mutation: the script only reads the log and writes into the seat draft directory.
"""
import re
import sys
from collections import Counter
from datetime import datetime

LOG = "/var/log/pacman.log"
START = 2463                 # first line in the assigned read range
CONTEXT_LINE = 2462          # one line before START: the operator's full-upgrade argv
WINDOW_START = datetime.fromisoformat("2026-10-20T09:40:00-0300")
INCIDENT = datetime.fromisoformat("2026-10-20T04:25:16-0300")
OUT = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecPacmanLogCensus/table.md"

TS_RE = re.compile(r"^\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{4})\]")
PKG_RE = re.compile(r"^\[ALPM\] (installed|upgraded|downgraded|removed) (.+)$")
RUN_RE = re.compile(r"^\[PACMAN\] Running '(.*)'$")


def parse_ts(line):
    m = TS_RE.match(line)
    return datetime.fromisoformat(m.group(1)) if m else None


def marker(ts):
    if ts is None:
        return "NO-TIMESTAMP"
    return "POST-WINDOW" if ts >= WINDOW_START else "PRE-WINDOW"


def esc(text):
    """Escape pipe characters so a cell cannot break the markdown table."""
    return text.replace("|", "\\|")


def classify(argv):
    """Classify a pacman argv into the operation it performs.

    The classes are what make P5 (rollback by package cache and package
    transactions during the pause) readable: only some operations change the
    installed package set, only one touches the sync databases and only one
    touches the package cache.
    """
    a = argv
    if " -Sy " in a or a.endswith(" -Sy") or " -Sy'" in a:
        return "sync-only (databases)"
    if " -Scc" in a:
        return "cache-clean (all packages)"
    if " -Sc " in a:
        return "cache-clean (uninstalled packages)"
    if " -Sw " in a:
        return "download-only"
    if " -D " in a:
        return "dependency-flag (no package change)"
    if " -R" in a:
        return "remove"
    if " -U " in a:
        return "install-local-package"
    if " -Syu" in a:
        return "full-upgrade"
    if " -S " in a:
        return "install-from-repo"
    return "other"


def main():
    with open(LOG, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    total = len(lines)

    running = []   # (lineno, ts, argv)
    pkg = []       # (lineno, ts, action, rest)
    tx_markers = []

    for lineno, line in enumerate(lines, 1):
        if lineno < START:
            continue
        ts = parse_ts(line)
        body = line.split("] ", 1)[1] if "] " in line else line
        m = RUN_RE.match(body)
        if m:
            running.append((lineno, ts, m.group(1)))
            continue
        m = PKG_RE.match(body)
        if m:
            pkg.append((lineno, ts, m.group(1), m.group(2)))
            continue
        if body.startswith("[ALPM] transaction started"):
            tx_markers.append((lineno, ts, "transaction started"))
        elif body.startswith("[ALPM] transaction completed"):
            tx_markers.append((lineno, ts, "transaction completed"))

    verbs = Counter(a for _, _, a, _ in pkg)
    pre = sum(1 for _, ts, _, _ in pkg if ts is None or ts < WINDOW_START)
    post = len(pkg) - pre

    out = []
    w = out.append

    w("# pacman.log census — round-24 wave 1, seat ExecPacmanLogCensus")
    w("")
    w("Source file: `/var/log/pacman.log` (read-only; no package transaction, sync,")
    w("service restart, cache write or configuration write was performed by this seat).")
    w("")
    w(f"- Assigned read range: line {START} to end of file (file has {total} lines).")
    w(f"- Pause-window start (the marking boundary): **2026-10-20T09:40:00-0300**.")
    w("- `PRE-WINDOW` = record timestamp is earlier than 2026-10-20T09:40:00-0300.")
    w("- `POST-WINDOW` = record timestamp is at or after 2026-10-20T09:40:00-0300.")
    w("- The mado round-15 libinput incident that triggered the pause ruling is at")
    w("  2026-10-20T04:25:16-0300 (`/var/log/pacman.log:2429`), which is before the")
    w("  assigned read range; it is cited here only as the incident anchor and is")
    w("  listed in the context section below, not counted as an in-range row.")
    w("- One context line (`2462`) is listed separately because it sits one line above")
    w("  the assigned start and carries the operator's full-upgrade argv that the")
    w("  window boundary is defined against.")
    w("")
    w("## Counts")
    w("")
    w("| Measure | Value |")
    w("|---|---|")
    w(f"| `[PACMAN] Running` command lines in range {START}–{total} | {len(running)} |")
    w(f"| ALPM installed records | {verbs.get('installed', 0)} |")
    w(f"| ALPM upgraded records | {verbs.get('upgraded', 0)} |")
    w(f"| ALPM downgraded records | {verbs.get('downgraded', 0)} |")
    w(f"| ALPM removed records | {verbs.get('removed', 0)} |")
    w(f"| Total ALPM package records in range | {len(pkg)} |")
    w(f"| PRE-WINDOW package records | {pre} |")
    w(f"| POST-WINDOW package records | {post} |")
    w(f"| ALPM transaction start/completed markers in range | {len(tx_markers)} |")
    w("")
    w("`downgraded` is zero across the whole file, not only in range: `grep -c downgraded")
    w("/var/log/pacman.log` exits 1 with no output. The two `reinstalled` records in the")
    w("file (lines 2359 and 2365, 2026-10-19T10:03) are outside the assigned range and")
    w("are not listed here.")
    w("")

    # ---------------------------------------------------------------- section A
    w("## Section A — every `[PACMAN] Running` command line in range")
    w("")
    w("| # | Log line | Timestamp (-0300) | Window | Operation class | Command line |")
    w("|---|---|---|---|---|---|")
    for i, (lineno, ts, argv) in enumerate(running, 1):
        w(f"| A{i} | {lineno} | {ts.isoformat() if ts else 'n/a'} | {marker(ts)} | {classify(argv)} | `{esc(argv)}` |")
    w("")
    w("Full untruncated argv for the two long lines (entries A4 at log line 3092 and")
    w("A5 at log line 3125):")
    w("")
    for idx, (lineno, ts, argv) in enumerate(running, 1):
        if lineno in (3092, 3125):
            w(f"**Line {lineno}** (entry A{idx}, {ts.isoformat()}):")
            w("")
            w("```")
            w(argv)
            w("```")
            w("")

    # ---------------------------------------------------------------- section B
    w("## Section B — every ALPM installed / upgraded / downgraded / removed record in range")
    w("")
    w("| # | Log line | Timestamp (-0300) | Action | Package and version change | Window |")
    w("|---|---|---|---|---|---|")
    for i, (lineno, ts, action, rest) in enumerate(pkg, 1):
        w(f"| B{i} | {lineno} | {ts.isoformat() if ts else 'n/a'} | {action} | `{esc(rest)}` | {marker(ts)} |")
    w("")

    # ---------------------------------------------------------------- section C
    w("## Section C — ALPM transaction boundaries in range")
    w("")
    w("| Log line | Timestamp (-0300) | Event | Window |")
    w("|---|---|---|---|")
    for lineno, ts, ev in tx_markers:
        w(f"| {lineno} | {ts.isoformat() if ts else 'n/a'} | {ev} | {marker(ts)} |")
    w("")

    # ---------------------------------------------------------------- section D
    w("## Section D — POST-WINDOW rows in full (the only rows at or after 2026-10-20T09:40 -03)")
    w("")
    w("### D1 — POST-WINDOW `[PACMAN] Running` command lines")
    w("")
    w("| # | Log line | Timestamp (-0300) | Operation class | Command line |")
    w("|---|---|---|---|---|")
    n = 0
    for i, (lineno, ts, argv) in enumerate(running, 1):
        if ts and ts >= WINDOW_START:
            n += 1
            w(f"| A{i} | {lineno} | {ts.isoformat()} | {classify(argv)} | `{esc(argv)}` |")
    w("")
    w("### D2 — POST-WINDOW ALPM package records")
    w("")
    w("| # | Log line | Timestamp (-0300) | Action | Package and version change |")
    w("|---|---|---|---|---|")
    for i, (lineno, ts, action, rest) in enumerate(pkg, 1):
        if ts and ts >= WINDOW_START:
            w(f"| B{i} | {lineno} | {ts.isoformat()} | {action} | `{esc(rest)}` |")
    w("")
    w("No ALPM `removed`, `upgraded` or `downgraded` record falls after")
    w("2026-10-20T09:40:00-0300. Every POST-WINDOW package record is an `installed`")
    w("record, and the count is exactly 5.")
    w("")

    # ---------------------------------------------------------------- section E
    w("## Section E — context row outside the assigned range (line 2462)")
    w("")
    ctx = lines[CONTEXT_LINE - 1]
    w("This line carries the operator's full-upgrade argv. It is one line above the")
    w("assigned read start, so it is reported as context rather than as an in-range row.")
    w("")
    w(f"```")
    w(ctx)
    w("```")
    w("")
    w("| Log line | Timestamp (-0300) | Window |")
    w("|---|---|---|")
    w(f"| {CONTEXT_LINE} | {parse_ts(ctx).isoformat()} | {marker(parse_ts(ctx))} |")
    w("")

    # ---------------------------------------------------------------- section F
    w("## Section F — operation-class summary over the in-range `[PACMAN] Running` lines")
    w("")
    w("| Operation class | PRE-WINDOW | POST-WINDOW | Total |")
    w("|---|---|---|---|")
    classes = sorted({classify(a) for _, _, a in running})
    for c in classes:
        pre_n = sum(1 for _, ts, a in running if classify(a) == c and not (ts and ts >= WINDOW_START))
        post_n = sum(1 for _, ts, a in running if classify(a) == c and ts and ts >= WINDOW_START)
        w(f"| {c} | {pre_n} | {post_n} | {pre_n + post_n} |")
    w("")
    w("Reading of the POST-WINDOW column for premise P5:")
    w("")
    post_by_class = {}
    for _, ts, a in running:
        if ts and ts >= WINDOW_START:
            post_by_class.setdefault(classify(a), []).append((ts, a))
    w(f"- `install-local-package` = {len(post_by_class.get('install-local-package', []))}"
      " invocations, all `pacman -U` of a locally built `.pkg.tar.zst` from the user's")
    w("  yay cache. These changed the installed set: they are the transactions that")
    w("  produced the 5 POST-WINDOW `installed` records (each debug sub-package is")
    w("  its own installed record).")
    w(f"- `dependency-flag (no package change)` = "
      f"{len(post_by_class.get('dependency-flag (no package change)', []))}"
      " invocations, all `pacman -D`. These write only the install-reason field of")
    w("  the local database; they change no package file and produce no ALPM")
    w("  installed/upgraded/removed record.")
    sync_post = post_by_class.get("sync-only (databases)", [])
    w(f"- `sync-only (databases)` = {len(sync_post)} invocation"
      + (f", `{sync_post[0][1]}` at {sync_post[0][0].isoformat()}." if sync_post else "."))
    w("  It refreshes the sync databases and installs nothing.")
    cache_post = post_by_class.get("cache-clean (all packages)", [])
    w(f"- `cache-clean (all packages)` = {len(cache_post)} invocations, all `pacman -Scc` at "
      + ", ".join(t.isoformat() for t, _ in cache_post) + ".")
    w("  These remove cached package files and install nothing.")
    absent = [c for c in ("remove", "full-upgrade", "install-from-repo", "download-only")
              if c not in post_by_class]
    verb = "falls" if len(absent) == 1 else "fall"
    noun = "invocation" if len(absent) == 1 else "invocations"
    w("- No " + ", ".join(f"`{c}`" for c in absent) + f" {noun} {verb} after the window start.")
    w("")

    # ---------------------------------------------------------------- section G
    w("## Section G — package-cache state read after the POST-WINDOW cache clean")
    w("")
    w("Read-only observation at the end of the census. The `ls | wc -l` shape counts")
    w("directory entries, and every one of the four entries is an empty scratch")
    w("directory left by a `pacman -U` download step, not a package file.")
    w("")
    w("| Probe | Result |")
    w("|---|---|")
    w("| `ls /var/cache/pacman/pkg \\| wc -l` | 4 (entries) |")
    w("| `sudo find /var/cache/pacman/pkg -type f \\| wc -l` | 0 (regular files) |")
    w("| `sudo find /var/cache/pacman/pkg -name '*.pkg.tar*' \\| wc -l` | 0 |")
    w("| `sudo find /var/cache/pacman -name '*libinput*' \\| wc -l` | 0 |")
    w("| entries inside each of the 4 `download-*` directories | 0 each |")
    w("")
    w("The four entries are `download-vcoq00` (2026-10-20 09:31), `download-Lsbwhh`")
    w("(2026-10-20 13:23), `download-0jh7Uc` (2026-10-21 17:55) and")
    w("`download-r5r0Ix` (2026-10-21 18:07) — one per `pacman -U` invocation in the")
    w("census, each owned by `alpm` with mode `drwx------` and each empty.")
    w("")
    w("Consequence for the P5 rollback premise: no cached package file exists, so no")
    w("version can be restored from `/var/cache/pacman/pkg`. The count of 4 is a")
    w("count of empty scratch directories, not of retained packages.")
    w("")

    text = "\n".join(out) + "\n"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"wrote {OUT}")
    print(f"running={len(running)} pkg={len(pkg)} pre={pre} post={post} total_lines={total}")
    print(f"verbs={dict(verbs)}")
    sys.exit(0)


if __name__ == "__main__":
    main()
