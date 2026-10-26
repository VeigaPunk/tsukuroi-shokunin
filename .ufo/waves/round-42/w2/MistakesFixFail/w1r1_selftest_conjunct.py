#!/usr/bin/env python3
"""W1 row R42-C1-SELFTEST-UNMEASURED — the proposed selftest-content conjunct, run as a check.

Fix under test (w1/MistakesSweep.md row 1): the C1 predicate gains a selftest-CONTENT conjunct
`selftest_cases >= 130` and `census.count('(R42-C1)') == 2`, so a census that is byte-identical to
the implementation minus both R42-C1 cases cannot be accepted.

This script is that conjunct, not a re-implementation of the counter: the case count is parsed from
the census's own selftest badge, the label count from the census bytes.

Usage: w1r1_selftest_conjunct.py <census.sh> <selftest-badge>
  exit 0 = conjunct holds (green), 1 = conjunct fails (red)
"""
import re
import sys

MIN_CASES = 130
PROPOSED_LABELS = 2      # the row's literal
RECOMMENDED = 2          # `>= 2` — see output: the tip carries 4


def conjunct(src, badge):
    m = re.search(r'\((\d+) cases, (\d+) passed, (\d+) failed\)', badge or '')
    cases = int(m.group(1)) if m else 0
    labels = src.count('(R42-C1)')
    cases_ok = cases >= MIN_CASES
    literal_ok = labels == PROPOSED_LABELS
    ge_ok = labels >= RECOMMENDED
    return cases, labels, cases_ok, literal_ok, ge_ok


def main():
    src = open(sys.argv[1], errors='replace').read()
    badge = sys.argv[2]
    cases, labels, cases_ok, literal_ok, ge_ok = conjunct(src, badge)
    ok = cases_ok and literal_ok
    print(f'badge          : {badge}')
    print(f'cases parsed   : {cases}  (>= {MIN_CASES}: {cases_ok})')
    print(f'R42-C1 labels  : {labels}  (== {PROPOSED_LABELS} as proposed: {literal_ok}; >= {RECOMMENDED}: {ge_ok})')
    print(f'CONJUNCT       : {"PASS (green)" if ok else "FAIL (red)"}'
          f'{"  [literal == 2 rejects the tip: use >= 2]" if cases_ok and not literal_ok and ge_ok else ""}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
