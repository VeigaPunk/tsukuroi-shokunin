#!/usr/bin/env python3
"""G-3 receipt: four-way predicate identity for round-42 C1 and C2.

Sources compared, character for character:
  1. SCORECARD.md "Round 42 - declaration" bold sentence, at commit a84fc9d (read with git show)
  2. the counter docstring sentence
  3. the `predicate` string the counter prints
  4. the `predicate` field of before/c<n>-before.jsonl line 2

Also normalises the two expression-level aliases in the `verdict = ...` condition
(`len(CASES)` -> `cases`, `base_hits` -> `novelty_base_hits`) and checks the code
condition equals the sentence. Read-only: no lane writes.
"""
import json
import re
import subprocess

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
FREEZE = 'a84fc9dec860f8bea516dff7ddfdc98223cdae52'
BEFORE = LANE + '/.ufo/waves/round-42/before'
COUNTER = {'C1': 'tools/score-size-invariance-r42.py', 'C2': 'tools/check-scrub-record-r42.py'}
ALIAS = {'C1': {'len(CASES)': 'cases'}, 'C2': {'base_hits': 'novelty_base_hits'}}


def git_show(rev, path):
    p = subprocess.run(['git', '-C', LANE, 'show', f'{rev}:{path}'], capture_output=True, check=True)
    return p.stdout.decode()


def norm_body(s):
    return s.strip().rstrip('.')


card = git_show(FREEZE, 'SCORECARD.md')
rows = {}
for ln in card.splitlines():
    if ln.startswith('| C1 |') or ln.startswith('| C2 |'):
        rows[ln[2:4]] = ln
decl = {k: re.search(r'\*\*(PASS iff .*?)\*\*', v).group(1) for k, v in rows.items()}

ok = True
for name, path in COUNTER.items():
    src = git_show(FREEZE, path)
    doc = ' '.join(l.strip() for l in re.search(r'Predicate \([^)]*\):\n(.*?)\n\n', src, re.S)
                   .group(1).strip().splitlines())
    lit = ''.join(re.findall(r"'([^']*)'", re.search(r"'predicate': \((.*?)\),\n", src, re.S).group(1)))
    before = json.loads(open(f'{BEFORE}/{name.lower()}-before.jsonl').read().splitlines()[1])['predicate']
    expr = ' '.join(re.search(r'verdict = \((.*?)\)\n', src, re.S).group(1).split())
    for k, v in ALIAS[name].items():
        expr = re.sub(r'(?<![A-Za-z_])' + re.escape(k) + r'(?![A-Za-z_])', v, expr)

    body = norm_body(decl[name][len('PASS iff '):])
    checks = {
        'decl_body == docstring_body': body == norm_body(doc[len('PASS iff '):]),
        'decl_body == printed_literal': body == norm_body(lit),
        'decl_body == before_receipt': body == norm_body(before),
        'verdict_expr(aliased) == sentence': expr == body,
        'conjunct_count_match': len(re.split(r'\s+and\s+', expr)) == len(re.split(r'\s+and\s+', body)),
    }
    ok &= all(checks.values())
    print(f'== {name} ({path})')
    print('  declaration :', repr(decl[name]))
    print('  docstring   :', repr(doc))
    print('  literal     :', repr(lit))
    print('  before      :', repr(before))
    print('  verdict expr:', repr(expr))
    for k, v in checks.items():
        print(f'  {k}: {v}')
print('RESULT:', 'IDENTICAL' if ok else 'DIVERGENCE')
