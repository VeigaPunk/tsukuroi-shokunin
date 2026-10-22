#!/usr/bin/env python3
"""Build my own C1 positive fixture (mutant-test canary) over the real v7.1 snapshots.

Statements are written by me from the fetched source bytes (not copied from the quote, not
the sealed K5 text). Layout follows the committed builder: one commit on top of TOOLREV in a
clone, snapshot bytes under .ufo/waves/round-31/mutc1/, S164-S169 registry rows, one
`| [R31-Qnn] ` SKILL.md line each.
"""
import argparse
import hashlib
import json
import os
import subprocess

FILES = {'Q01': ('Defragmentation.rst', 25), 'Q02': ('btrfs-rescue.rst', 126),
         'Q03': ('btrfs-check.rst', 30), 'Q04': ('ch-mount-options.rst', 38),
         'Q05': ('ch-mount-options.rst', 92), 'Q06': ('ch-mount-options.rst', 135),
         'Q07': ('btrfs-replace.rst', 12), 'Q08': ('Trim.rst', 29)}
SIDS = {'Defragmentation.rst': 'S164', 'btrfs-rescue.rst': 'S165', 'btrfs-check.rst': 'S166',
        'ch-mount-options.rst': 'S167', 'btrfs-replace.rst': 'S168', 'Trim.rst': 'S169'}
URL = 'https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/'
SNAPDIR = '.ufo/waves/round-31/mutc1'
# Written by me from the fetched bytes; each answers its frozen question.
STMT = {
    'Q01': ('Defragmentation rewrites the layout of a file\'s extents and breaks the sharing of '
            'those blocks, so a file copied with reflink or held in several snapshots will '
            'afterwards consume more data space than before.'),
    'Q02': ('Run zero-log only when a mount fails during log replay; it clears the log tree and '
            'may discard changes made since the last commit, that is up to 30 seconds worth of '
            'them.'),
    'Q03': ('Run check with --repair only when a developer or an experienced user advises it, and '
            'only after accepting that no fsck can repair every kind of corruption on a volume.'),
    'Q04': ('The autodefrag mount option queues small random writes, currently 64KiB in size, for '
            'background defragmentation, but it is not well suited to large database workloads.'),
    'Q05': ('The commit= mount option sets the interval of the periodic transaction commit, '
            'default 30 seconds; above 300 seconds a warning is printed because a crash then '
            'loses more unwritten data.'),
    'Q06': ('Enabling nodatacow implies nodatasum and switches compression off; files created '
            'under it get the NOCOW attribute, so data checksums are no longer maintained by the '
            'filesystem.'),
    'Q07': ('With btrfs replace start you point at the source as srcdev or devid and a targetdev, '
            'and the target must be the same size or larger than the source device.'),
    'Q08': ('For a btrfs SSD prefer discard=async over discard=sync, or run fstrim periodically '
            'as a service, because the device may ignore the trim hint and relocate data '
            'internally.'),
}
SKILL = {
    'Q01': '| [R31-Q01] | defragment breaks extent sharing | Defragmentation.rst line 25 |',
    'Q02': '| [R31-Q02] | zero-log clears the log tree after a failed mount | btrfs-rescue.rst line 126 |',
    'Q03': '| [R31-Q03] | btrfs check --repair is a last resort | btrfs-check.rst line 30 |',
    'Q04': '| [R31-Q04] | autodefrag suits small random writes, not databases | ch-mount-options.rst line 38 |',
    'Q05': '| [R31-Q05] | commit= bounds the periodic transaction commit | ch-mount-options.rst line 92 |',
    'Q06': '| [R31-Q06] | nodatacow gives up checksums and compression | ch-mount-options.rst line 135 |',
    'Q07': '| [R31-Q07] | replace start takes srcdev or devid and a targetdev | btrfs-replace.rst line 12 |',
    'Q08': '| [R31-Q08] | fstrim periodically beats discard=sync | Trim.rst line 29 |',
}


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--toolrev', required=True)
    ap.add_argument('--snapdir', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--label', default='P1 my positive')
    a = ap.parse_args()
    repo = os.path.join(a.work, 'c1-fixture')
    subprocess.run(['/usr/bin/git', 'clone', '-q', '--no-local', a.lane, repo], env=env(), check=True)
    base = git(repo, 'rev-parse', a.toolrev)
    git(repo, 'checkout', '-q', '--detach', base)
    files, rows, skill_add, reg_rows = {}, [], [], []
    seen_sids = set()
    for q in sorted(FILES):
        fname, ln = FILES[q]
        data = open(os.path.join(a.snapdir, fname), 'rb').read()
        digest = hashlib.sha256(data).hexdigest()
        files[f'{SNAPDIR}/{fname}'] = data
        line = data.decode().splitlines()[ln - 1]
        quote = ' '.join(line.split()[:25])
        rows.append({'id': q, 'question': q, 'statement': STMT[q], 'source': SIDS[fname],
                     'snapshot': f'{SNAPDIR}/{fname}', 'line': ln, 'quote': quote})
        skill_add.append(SKILL[q])
        if SIDS[fname] not in seen_sids:
            seen_sids.add(SIDS[fname])
            reg_rows.append(f'| {SIDS[fname]} | btrfs-progs v7.1 Documentation/{fname} — '
                            f'{URL}{fname} | docs | A | fixture | sha256 {digest} | fixture row | '
                            f'mined | 2026-10-22 | on-release | fixture |')
    files['corpus/knowledge/btrfs-repair-r31.json'] = json.dumps({'rows': rows}, indent=1) + '\n'
    files['corpus/SOURCES.md'] = (open(os.path.join(repo, 'corpus/SOURCES.md')).read().rstrip('\n')
                                  + '\n' + '\n'.join(reg_rows) + '\n')
    files['SKILL.md'] = (open(os.path.join(repo, 'SKILL.md')).read().rstrip('\n') + '\n\n'
                         + '\n'.join(skill_add) + '\n')
    for path, data in files.items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, 'wb').write(data if isinstance(data, bytes) else data.encode())
        git(repo, 'add', path)
    git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid', '-c',
        'commit.gpgsign=false', 'commit', '-qm', a.label)
    print(json.dumps({'fixture': a.label, 'commit': git(repo, 'rev-parse', 'HEAD'),
                      'clone': repo}))


if __name__ == '__main__':
    main()
