#!/usr/bin/env python3
"""Outside oracle for the derived hook order: /var/log/pacman.log.

Independent of both the entry table and the census arm. libalpm logs
"running '<name>'..." once per executed hook (hook.c:659), so every transaction
leaves a run sequence in the log. Checks against the derived order:

  * within one phase, positions must increase (HO1/HO7: the run sequence is a
    subsequence of the candidate table order);
  * no hook runs inside the committing window, i.e. between
    "transaction started" and "transaction completed"/"failed"/"interrupted"
    (trans.c:201-204 runs Pre hooks before that log line, :237-240 Post after);
  * in the inter-transaction window the PostTransaction runs of the previous
    transaction must all precede the PreTransaction runs of the next one;
  * after "transaction failed"/"interrupted" no PostTransaction hook may run
    until the next "transaction completed" (HO6, alpm-hooks.5.asciidoc CAVEATS).

The log spans host history, so hook names of older host states appear; they are
counted and skipped, and ordering is still tested across the in-table names of
each window.

Usage: check-log-order.py <derived-rows.txt> [/var/log/pacman.log]
"""

import re
import sys

RUN = re.compile(r"running '([^']+)'\.\.\.")
START = re.compile(r"\[ALPM\] transaction started")
DONE = re.compile(r"\[ALPM\] transaction completed")
FAIL = re.compile(r"\[ALPM\] transaction (failed|interrupted)")
HEADER = re.compile(r"^\[(\d{4}-\d{2}-\d{2})T")


def load_order(path):
    """name -> (when, pos) for the two phases."""
    order = {}
    for line in open(path, encoding="utf-8"):
        parts = line.split()
        if len(parts) != 7:
            continue
        order[parts[2]] = (parts[0], int(parts[1]))
    return order


def main():
    order_path = sys.argv[1]
    log_path = sys.argv[2] if len(sys.argv) > 2 else "/var/log/pacman.log"
    order = load_order(order_path)

    problems = []
    unknown = {}
    totals = {"windows": 0, "runs": 0, "in_table": 0, "transactions": 0,
              "failed": 0, "windows_with_post": 0, "windows_with_pre": 0}
    windows = []         # finished windows, each a list of (date, name, when, pos)

    window = []          # (date, name, when, pos) in the current idle window
    dead = False         # a failed/interrupted transaction is pending in this window
    date = "?"
    in_mid = False

    def flush(why):
        nonlocal window, dead
        if window:
            totals["windows"] += 1
            seen_pre = False
            last = {"PreTransaction": 0, "PostTransaction": 0}
            has_post = any(w == "PostTransaction" for _, _, w, _ in window)
            has_pre = any(w == "PreTransaction" for _, _, w, _ in window)
            totals["windows_with_post"] += 1 if has_post else 0
            totals["windows_with_pre"] += 1 if has_pre else 0
            for d, name, when, pos in window:
                if dead and when == "PostTransaction":
                    problems.append("%s: %s ran after a failed/interrupted "
                                    "transaction before the next completed one"
                                    % (d, name))
                if when == "PreTransaction":
                    seen_pre = True
                elif seen_pre:
                    problems.append("%s: %s (Post) ran after a Pre hook in the "
                                    "same window" % (d, name))
                if pos <= last[when]:
                    problems.append("%s: %s out of order (%s pos %d after %d)"
                                    % (d, name, when, pos, last[when]))
                last[when] = max(last[when], pos)
            windows.append(list(window))
        window = []
        dead = False

    for lineno, line in enumerate(open(log_path, encoding="utf-8", errors="replace"), 1):
        m = HEADER.match(line)
        if m:
            date = m.group(1)
        if START.search(line):
            flush("started")
            totals["transactions"] += 1
            in_mid = True
            continue
        if DONE.search(line):
            flush("completed")
            in_mid = False
            continue
        if FAIL.search(line):
            flush("failed")
            totals["failed"] += 1
            in_mid = False
            dead = True
            continue
        m = RUN.search(line)
        if not m:
            continue
        totals["runs"] += 1
        name = m.group(1)
        if in_mid:
            problems.append("%s line %d: %s ran between transaction started "
                            "and completed" % (date, lineno, name))
            continue
        if name not in order:
            unknown[name] = unknown.get(name, 0) + 1
            continue
        totals["in_table"] += 1
        when, pos = order[name]
        window.append((date, name, when, pos))

    flush("eof")

    print("ordering table: %s (%d names)" % (order_path, len(order)))
    print("log: %s" % log_path)
    print("transactions started: %d, failed/interrupted: %d"
          % (totals["transactions"], totals["failed"]))
    print("hook run lines: %d, attributable to the current table: %d"
          % (totals["runs"], totals["in_table"]))
    print("idle windows with runs: %d (with Post: %d, with Pre: %d)"
          % (totals["windows"], totals["windows_with_post"],
             totals["windows_with_pre"]))
    print("names absent from the current table (older host state): %d distinct, "
          "%d occurrences" % (len(unknown), sum(unknown.values())))
    for name, n in sorted(unknown.items(), key=lambda kv: (-kv[1], kv[0]))[:12]:
        print("  not-in-table: %-52s %d" % (name, n))
    print("violations: %d" % len(problems))
    for p in problems[:40]:
        print("  %s" % p)

    if "--dump" in sys.argv:
        n = 2
        for i, arg in enumerate(sys.argv):
            if arg == "--dump" and i + 1 < len(sys.argv):
                n = int(sys.argv[i + 1])
        print("")
        print("longest %d run windows (position from the derived table):" % n)
        for w in sorted(windows, key=lambda w: -len(w))[:n]:
            print("  window %s, %d runs:" % (w[0][0], len(w)))
            for d, name, when, pos in w:
                print("    %-16s %3d  %s" % (when, pos, name))

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
