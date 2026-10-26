#!/usr/bin/env python3
"""C2CritAxis round-39 control: rewrite ONLY the TO rule cells (cells[1] -> index 2
when split on '|'); keep id, source cell and host cell byte-identical."""
import re
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
ENTRY = 'corpus/knowledge/pacman-transaction-order-r39.md'
R38 = 'corpus/knowledge/pacman-hook-order-r38.md'

FALSE = {
    'TO1': 'PostTransaction hooks run **before** `transaction started` is logged; the PreTransaction phase runs **after** `transaction completed`',
    'TO2': 'A sync commit adds or upgrades the targets first and only then removes the conflicting and to-be-replaced packages',
    'TO3': 'The `post_install`/`post_upgrade` scriptlet runs before the `installed`/`upgraded` line is logged, and the files are extracted after that line',
    'TO4': 'Install scriptlets receive the **old** version first and the new version second',
    'TO5': 'The hook directories are read once at handle initialisation: the Pre and Post phases see the same directory listing',
    'TO6': '`ldconfig` runs after every single package add, and it still runs when a package failed to commit',
    'TO7': 'The old version of an upgraded package logs `removed` and runs its `pre_remove` and `post_remove` scriptlets',
    'TO8': 'Only install-scriptlet output is tagged `ALPM-SCRIPTLET`; hook output carries a different tag',
}


def show(rev, path):
    p = subprocess.run(['git', '-C', LANE, 'show', f'{rev}:{path}'],
                       capture_output=True, check=True)
    return p.stdout.decode()


def r38_rules():
    rules = {}
    for line in show('2e1c2a4', R38).splitlines():
        m = re.match(r'^\| (HO\d) \|', line)
        if m:
            parts = line.rstrip('\n').split('|')
            rules[m.group(1)] = parts[2].strip()
    return rules


def rewrite(entry, rules):
    out = []
    hit = 0
    for line in entry.splitlines(keepends=True):
        m = re.match(r'^\| (TO\d+) \|', line)
        if not m:
            out.append(line)
            continue
        parts = line.rstrip('\n').split('|')
        assert len(parts) == 6, (m.group(1), len(parts))
        parts[2] = ' ' + rules[m.group(1)] + ' '
        out.append('|'.join(parts) + '\n')
        hit += 1
    assert hit == 8, hit
    return ''.join(out)


def main():
    kind, dest = sys.argv[1], sys.argv[2]
    entry = show('2e1c2a4', ENTRY)
    if kind == 'false':
        rules = FALSE
    elif kind == 'ho':
        ho = r38_rules()
        assert len(ho) == 7, sorted(ho)
        rules = {f'TO{i}': ho[f'HO{i}'] for i in range(1, 8)}
        rules['TO8'] = ho['HO7']
    else:
        raise SystemExit('kind must be false|ho')
    open(dest, 'w').write(rewrite(entry, rules))


if __name__ == '__main__':
    main()
