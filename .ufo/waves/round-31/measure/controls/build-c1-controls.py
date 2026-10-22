#!/usr/bin/env python3
"""Build the round-31 C1 do-nothing controls as commits in a sandbox clone (never in the lane).

Each control is one commit on top of TOOLREV (the declaration commit that carries the frozen
counter `tools/check-btrfs-repair-r31.py`) in a `git clone --no-local` of the lane under
/fast/scratch/hyaku. The counter is then run on each control commit through
`tools/run-receipt.py --lane <clone>`; the receipts are committed under
`.ufo/waves/round-31/measure/controls/`.

Open controls (this file):
  K2 restate-r30   the lane's own round-30 btrfs rows D01-D08 relabelled Q01-Q08: same
                   statements, sources, snapshots, lines and quotes; SKILL.md lines are the
                   round-30 `| [R30-Dnn] ` lines relabelled `| [R31-Qnn] `. Re-scoring knowledge
                   the lane already holds.
  K3 junk-real     the real pinned btrfs-progs v7.1 snapshots, quotes verbatim at real lines that
                   carry the novelty token, well-formed `mined` registry rows S164-S169 with the
                   frozen URL and sha256, SKILL.md lines with the token, statements of filler words
                   that name the token and nothing the source teaches.
  K4 quote-copy    K3 with each statement replaced by its quote plus six filler words.
Sealed controls (`build-c1-sealed.py`, kept out of the lane until after data; its sha256 is
committed with the receipts): K1 sourceless-forged (the counter's own bytes as the snapshot, a
made-up S900 row, statements that carry every answer key) and K5 reader-ceiling (the same as
K3 but with statements written by the L1 after reading the sources: the positive control).
The base K0 is the claim base itself (`2077e2fa`), run without a fixture.

Usage: python3 build-c1-controls.py --lane <lane> --toolrev <REV> --snapdir <dir with the six
       v7.1 .rst files> --work <scratch dir>
Prints one JSON line per control: {"control", "commit"}.
"""
import argparse
import json
import os
import re
import subprocess

FILES = {  # question -> (snapshot file, quote line)
    'Q01': ('Defragmentation.rst', 25), 'Q02': ('btrfs-rescue.rst', 126),
    'Q03': ('btrfs-check.rst', 30), 'Q04': ('ch-mount-options.rst', 38),
    'Q05': ('ch-mount-options.rst', 92), 'Q06': ('ch-mount-options.rst', 135),
    'Q07': ('btrfs-replace.rst', 12), 'Q08': ('Trim.rst', 29),
}
SIDS = {'Defragmentation.rst': 'S164', 'btrfs-rescue.rst': 'S165', 'btrfs-check.rst': 'S166',
        'ch-mount-options.rst': 'S167', 'btrfs-replace.rst': 'S168', 'Trim.rst': 'S169'}
TOKEN = {'Q01': 'defragment', 'Q02': 'zero-log', 'Q03': '--repair', 'Q04': 'autodefrag',
         'Q05': 'commit=', 'Q06': 'nodatacow', 'Q07': 'btrfs replace', 'Q08': 'fstrim'}
URL = 'https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/'
SNAPDIR = '.ufo/waves/round-31/fixture'


def env():
    e = {k: v for k, v in os.environ.items()
         if not (k.startswith('GIT_') or k.startswith('LD_') or k.startswith('PYTHON'))}
    e.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
              'GIT_CONFIG_SYSTEM': os.devnull, 'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'})
    return e


def git(repo, *args):
    p = subprocess.run(['/usr/bin/git', '-C', repo, *args], capture_output=True, env=env())
    if p.returncode:
        raise SystemExit('git %s failed: %s' % (args, p.stderr.decode()))
    return p.stdout.decode().strip()


def commit(repo, base, files, msg):
    git(repo, 'checkout', '-q', '--detach', base)
    for path, data in files.items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(data if isinstance(data, bytes) else data.encode())
        git(repo, 'add', path)
    git(repo, '-c', 'user.name=control', '-c', 'user.email=control@invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-qm', msg)
    return git(repo, 'rev-parse', 'HEAD')


def sha256(b):
    import hashlib
    return hashlib.sha256(b).hexdigest()


def registry_rows(snapdir):
    rows = []
    for f, sid in SIDS.items():
        with open(os.path.join(snapdir, f), 'rb') as fh:
            digest = sha256(fh.read())
        rows.append(f'| {sid} | btrfs-progs v7.1 Documentation/{f} — {URL}{f} | docs | A | fixture '
                    f'| sha256 {digest} | fixture row | mined | 2026-10-22 | on-release | fixture |')
    return rows


def real_layout(repo, base, snapdir, statements, label):
    git(repo, 'checkout', '-q', '--detach', base)
    files, rows, skill_add = {}, [], []
    for q, (f, ln) in FILES.items():
        with open(os.path.join(snapdir, f), 'rb') as fh:
            data = fh.read()
        files[f'{SNAPDIR}/{f}'] = data
        line = data.decode().splitlines()[ln - 1]
        words = line.split()
        quote = ' '.join(words[:25])
        rows.append({'id': q, 'question': q, 'statement': statements[q](quote), 'source': SIDS[f],
                     'snapshot': f'{SNAPDIR}/{f}', 'line': ln, 'quote': quote})
        skill_add.append(f'| [R31-{q}] | {TOKEN[q]} fixture line | fixture | {SIDS[f]} line {ln} |')
    files['corpus/knowledge/btrfs-repair-r31.json'] = json.dumps({'rows': rows}, indent=1) + '\n'
    reg = open(os.path.join(repo, 'corpus/SOURCES.md')).read().rstrip('\n') + '\n' + '\n'.join(registry_rows(snapdir)) + '\n'
    files['corpus/SOURCES.md'] = reg
    skill = open(os.path.join(repo, 'SKILL.md')).read().rstrip('\n') + '\n\n' + '\n'.join(skill_add) + '\n'
    files['SKILL.md'] = skill
    return commit(repo, base, files, label)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--toolrev', required=True)
    ap.add_argument('--snapdir', required=True)
    ap.add_argument('--work', required=True)
    a = ap.parse_args()
    repo = os.path.join(a.work, 'c1-controls')
    subprocess.run(['/usr/bin/git', 'clone', '-q', '--no-local', a.lane, repo], env=env(), check=True)
    git(repo, 'remote', 'set-url', '--push', 'origin', 'DISABLED')
    base = git(repo, 'rev-parse', a.toolrev)
    out = {}
    # K2: the lane's own round-30 rows relabelled.
    git(repo, 'checkout', '-q', '--detach', base)
    r30 = json.load(open(os.path.join(repo, 'corpus/knowledge/btrfs-space-r30.json')))['rows']
    rows = []
    for i, q in enumerate(sorted(FILES)):
        r = dict(r30[i])
        rows.append({'id': q, 'question': q, 'statement': r['statement'], 'source': r['source'],
                     'snapshot': r['snapshot'], 'line': r['line'], 'quote': r['quote']})
    skill = open(os.path.join(repo, 'SKILL.md')).read()
    add = []
    for i, q in enumerate(sorted(FILES)):
        m = re.search(r'^\| \[R30-D%02d\] (.*)$' % (i + 1), skill, re.M)
        add.append(f'| [R31-{q}] ' + (m.group(1) if m else 'missing'))
    out['K2-restate-r30'] = commit(repo, base, {
        'corpus/knowledge/btrfs-repair-r31.json': json.dumps({'rows': rows}, indent=1) + '\n',
        'SKILL.md': skill.rstrip('\n') + '\n\n' + '\n'.join(add) + '\n'}, 'K2 restate-r30')
    # K3: junk statements over real snapshots.
    junk = {q: (lambda quote, q=q: f'The {TOKEN[q]} topic is recorded in this row of the lane for the record only and nothing more.')
            for q in FILES}
    out['K3-junk-real'] = real_layout(repo, base, a.snapdir, junk, 'K3 junk-real')
    # K4: quote copied as the statement.
    copy = {q: (lambda quote: quote + ' as the lane records it here') for q in FILES}
    out['K4-quote-copy'] = real_layout(repo, base, a.snapdir, copy, 'K4 quote-copy')
    for k, v in out.items():
        print(json.dumps({'control': k, 'commit': v, 'clone': repo}))


if __name__ == '__main__':
    main()
