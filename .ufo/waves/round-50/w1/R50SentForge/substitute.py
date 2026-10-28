#!/usr/bin/env python3
"""C1-B7 substitution probe: committed reports say `fails`, --wave-dir supplies `holds`.

Run 1 (no overrides) must FAIL with every row blocked by the committed bytes.
Run 2 (same revision, same results file, --wave-dir pointing at the forged `holds` set) must
PASS — the counter prints `"revision": <REV>` while none of the judged report bytes live in it.
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
HASHES = {'GR1': '3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1',
          'GR2': 'a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f',
          'GR3': '43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c'}
sys.path.insert(0, str(S))
from forge import SEATS, results  # noqa: E402
from closeout import forged_marks  # noqa: E402


def show(path):
    return subprocess.run(['git', '-C', LANE, 'show', f'{REV}:{path}'],
                          capture_output=True, check=True).stdout.decode()


def summarise(tag, p):
    obj = json.loads(p.stdout.strip().splitlines()[-1])
    (S / 'receipts').mkdir(exist_ok=True)
    (S / 'receipts' / f'{tag}.json').write_text(json.dumps(obj, indent=1, sort_keys=True) + '\n')
    print(f'[{tag}] rc={p.returncode} ' + json.dumps(
        {k: obj.get(k) for k in ('verdict', 'revision', 'verdicts_ok', 'seats_ok', 'marks_ok')}))
    for row in ('GR1', 'GR2', 'GR3'):
        pr = obj['per_row'][row]
        print(f'   {row}: credited={len(pr["credited"])} blocking={pr["blocking"]} '
              f'row_ok={pr["row_ok"]}')
    return obj


def main():
    entry, skill, readme = forged_marks()
    fx = S / 'fx3'
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
    wdir = fx / '.ufo' / 'waves' / 'round-50' / 'w1'
    wdir.mkdir(parents=True)
    for seat, role, row in SEATS:
        (wdir / f'{seat}.md').write_text(
            f'ROW {row} VERDICT: fails\nSECTION SHA256: {HASHES[row]}\n'
            f'The seat read the row and refuses it: the committed bytes say the row does not '
            f'hold on these bytes, citing cmdline.c:1 and vsprintf.c:1 as it read them. '
            f'This body exists so the file is well formed; it is a committed negative verdict.\n')
    results(fx / '.ufo' / 'waves' / 'round-50' / 'w1-results.json', SEATS)
    g = ['git', '-C', str(fx), '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid']
    subprocess.run(g + ['add', '-A'], check=True)
    subprocess.run(g + ['commit', '-q', '-m', 'committed cohort: every row fails'], check=True)
    head = subprocess.run(['git', '-C', str(fx), 'rev-parse', 'HEAD'],
                          capture_output=True, text=True).stdout.strip()
    print('   fixture HEAD', head)
    print('   committed blob of R50RevGR1a:',
          subprocess.run(['git', '-C', str(fx), 'rev-parse', f'{head}:'
                          '.ufo/waves/round-50/w1/R50RevGR1a.md'],
                         capture_output=True, text=True).stdout.strip())

    p = subprocess.run([sys.executable, COUNTER, '--revision', head, '--lane', str(fx)],
                       capture_output=True, text=True, cwd=str(S), timeout=900)
    summarise('e1-committed-fails', p)

    p = subprocess.run([sys.executable, COUNTER, '--revision', head, '--lane', str(fx),
                        '--wave-dir', str(S / 'd' / 'reports'),
                        '--results-file', str(fx / '.ufo' / 'waves' / 'round-50'
                                              / 'w1-results.json')],
                       capture_output=True, text=True, cwd=str(S), timeout=900)
    obj = summarise('e2-substituted-holds', p)
    print('   reported revision:', obj.get('revision'), '| fixture HEAD:', head)


if __name__ == '__main__':
    main()
