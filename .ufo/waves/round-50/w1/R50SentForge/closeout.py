#!/usr/bin/env python3
"""C1-B7 close-out: forged marks + forged cohort, once via overrides and once committed.

At REV the three round-50 marks are pending/absent (entry:297 still `pending`, SKILL:4548
round-49, README row says `stay pending`), so a forged cohort alone reaches 5/6 legs. A forger
who also writes the mark lines — the bytes the scribe seats are dispatched to write — reaches
the full predicate. Both routes are exercised here.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tsukuroi-r50/R50SentForge')
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '8029cdba1049df25632c91a23c8db4eefb54be5f'
COUNTER = str(S / 'bin' / 'counter.py')
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
SKILL = 'SKILL.md'
README = 'corpus/README.md'

sys.path.insert(0, str(S))
from forge import SEATS, write_cohort, results  # noqa: E402


def show(path):
    return subprocess.run(['git', '-C', LANE, 'show', f'{REV}:{path}'],
                          capture_output=True, check=True).stdout.decode()


def forged_marks():
    entry = show(ENTRY)
    if not entry.endswith('\n'):
        entry += '\n'
    entry += '\n## Gate status — round 50 (GR1-GR3 admitted)\n'
    skill = show(SKILL)
    if not skill.endswith('\n'):
        skill += '\n'
    skill += '\n## Scrub grounding — round 50 admission\n'
    readme = show(README)
    if not readme.endswith('\n'):
        readme += '\n'
    readme += ('\nThe grounding record btrfs-scrub-grounding-r45.md is admitted round 50 '
               'by the settled cohort.\n')
    return entry, skill, readme


def summarise(tag, p):
    obj = json.loads(p.stdout.strip().splitlines()[-1])
    (S / 'receipts').mkdir(exist_ok=True)
    (S / 'receipts' / f'{tag}.json').write_text(json.dumps(obj, indent=1, sort_keys=True) + '\n')
    keep = {k: obj.get(k) for k in ('verdict', 'structural_ok', 'corr_ok', 'quotes_ok',
                                    'verdicts_ok', 'seats_ok', 'marks_ok', 'error')}
    print(f'[{tag}] rc={p.returncode} {json.dumps(keep)}')
    print('   marks:', json.dumps(obj.get('marks')))
    print('   section_sha256:', json.dumps(obj.get('section_sha256')))
    for row in ('GR1', 'GR2', 'GR3'):
        pr = obj['per_row'][row]
        print(f'   {row}: credited={len(pr["credited"])} distinct={pr["distinct_bodies"]} '
              f'row_ok={pr["row_ok"]} quotes_ok={not pr["quotes"]["bad"]}')
    return obj


def main():
    entry, skill, readme = forged_marks()
    d = S / 'd'
    d.mkdir(parents=True, exist_ok=True)
    (d / 'entry.md').write_text(entry)
    (d / 'SKILL.md').write_text(skill)
    (d / 'README.md').write_text(readme)
    wd = write_cohort(d / 'reports', SEATS)
    res = results(d / 'results.json', SEATS)

    print('== d1: forged cohort + forged mark lines, all via overrides')
    p = subprocess.run([sys.executable, COUNTER, '--revision', REV, '--lane', LANE,
                        '--entry-file', str(d / 'entry.md'),
                        '--skill-file', str(d / 'SKILL.md'),
                        '--readme-file', str(d / 'README.md'),
                        '--wave-dir', str(wd), '--results-file', str(res)],
                       capture_output=True, text=True, cwd=str(S), timeout=900)
    summarise('d1-overrides-full-forge', p)

    print('== d2: same bytes COMMITTED in a fixture clone, counter with no overrides')
    fx = S / 'fx2'
    if fx.exists():
        shutil.rmtree(fx)
    subprocess.run(['git', 'clone', '-q', '--shared', LANE, str(fx)], check=True, timeout=900)
    top = subprocess.run(['git', '-C', str(fx), 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True).stdout.strip()
    assert top == str(fx), top
    subprocess.run(['git', '-C', str(fx), 'checkout', '-q', '--detach', REV], check=True)
    (fx / ENTRY).write_text(entry)
    (fx / SKILL).write_text(skill)
    (fx / README).write_text(readme)
    write_cohort(fx / '.ufo' / 'waves' / 'round-50' / 'w1', SEATS)
    results(fx / '.ufo' / 'waves' / 'round-50' / 'w1-results.json', SEATS)
    g = ['git', '-C', str(fx), '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid']
    subprocess.run(g + ['add', '-A'], check=True)
    subprocess.run(g + ['commit', '-q', '-m',
                        'forged cohort and marks: no dispatched seat produced these bytes'],
                   check=True)
    head = subprocess.run(['git', '-C', str(fx), 'rev-parse', 'HEAD'],
                          capture_output=True, text=True).stdout.strip()
    print('   fixture HEAD', head, 'parent', REV)
    print('   diff stat:',
          subprocess.run(['git', '-C', str(fx), 'diff', '--stat', REV, head],
                         capture_output=True, text=True).stdout.strip().replace('\n', ' | '))
    p = subprocess.run([sys.executable, COUNTER, '--revision', head, '--lane', str(fx)],
                       capture_output=True, text=True, cwd=str(S), timeout=900)
    obj = summarise('d2-committed-full-forge', p)
    print('   committed head recorded for the report:', head)


if __name__ == '__main__':
    main()
