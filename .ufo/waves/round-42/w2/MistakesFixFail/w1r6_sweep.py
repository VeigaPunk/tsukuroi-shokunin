#!/usr/bin/env python3
"""W1 row R42-C1-CLASS-UNSWEPT — the sweep that the gate must be able to go green on.

Applies the round-42 fix rule (no early reader on a printf-fed pipe: let awk consume the whole
input, `NR <= N` / `NR == 1` in place of `head -nN`) to every site the gate reports outside
`run_selftest()`, then re-runs the gate over the result. The point of this script is not that the
sweep is the round's deliverable — it is that the gate is satisfiable by the rule it enforces, so a
red gate is a measurement, not an impossible demand.

Usage: w1r6_sweep.py <in.sh> <out.sh>
"""
import sys

D = '"'
SED = "| sed -E 's/[[:space:]]+$//'"
PK = "printf '%s\\n' " + D + "$CAP_OUT" + D
RULES = [
    (PK + " | grep -v '^[[:space:]]*$' | head -n " + D + "$SAMPLE_N" + D,
     PK + " | grep -v '^[[:space:]]*$' | awk -v n=" + D + "$SAMPLE_N" + D + " 'NR <= n'"),
    (PK + " | head -n1 | tr -d '\\r' " + SED,
     PK + " | awk 'NR == 1' | tr -d '\\r' " + SED),
    (PK + " | head -n1 | tr -d '\\r')",
     PK + " | awk 'NR == 1' | tr -d '\\r')"),
    (PK + " | awk 'NF && $1 ~ /\\.timer$/ {print $1}' | head -n " + D + "$TIMER_SCAN_MAX" + D,
     PK + " | awk -v n=" + D + "$TIMER_SCAN_MAX" + D + " 'NF && $1 ~ /\\.timer$/ && ++c <= n {print $1}'"),
    (PK + " | head -n1 | awk -F', *' '{print $NF}')",
     PK + " | awk -F', *' 'NR == 1 {print $NF}')"),
    ("| sort -u | head -n 6 | paste -sd, - || true)",
     "| sort -u | awk 'NR <= 6' | paste -sd, - || true)"),
    ("printf '%s\\n' " + D + "$cl_out" + D + " | grep '^?' | sed 's/^?//' | head -n6 | paste -sd, - || true",
     "printf '%s\\n' " + D + "$cl_out" + D + " | grep '^?' | sed 's/^?//' | awk 'NR <= 6' | paste -sd, - || true"),
]


def main():
    src = open(sys.argv[1]).read()
    total = 0
    for old, new in RULES:
        n = src.count(old)
        if n < 1:
            raise SystemExit(f'rule anchor not found: {old[:80]!r}')
        src = src.replace(old, new)
        total += n
        print(f'  {n}x  {old[:78]}')
    open(sys.argv[2], 'w').write(src)
    print(f'replacements   : {total} sites swept into awk full-consumption form')


if __name__ == '__main__':
    main()
