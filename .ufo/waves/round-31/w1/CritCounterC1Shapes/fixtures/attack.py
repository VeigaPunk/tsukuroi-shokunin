#!/usr/bin/env python3
"""Attack harness for the round-31 C1 frozen counter.

Builds one fixture commit per shape in the sandbox clone (base 8cff9e7c), runs
tools/check-btrfs-repair-r31.py --revision <commit> --lane <clone>, and prints the
Q01 per-row line plus the summary. We only need the Q01 row's `fail` list to tell
whether a given gate accepted or refused the shape; R7 answer-key groups are expected
to fail (we never recover the sealed keys), so a shape "passes a gate" when the gate's
own fail string is ABSENT from the list.
"""
import json
import os
import subprocess
import hashlib

REPO = '/fast/scratch/hyaku/tsukuroi-r31/CritCounterC1Shapes/repo'
SNAPS = '/fast/scratch/hyaku/tsukuroi-r31/CritCounterC1Shapes/snaps'
BASE = '8cff9e7cfb034b49c645d548801ac3185a827cb4'
URL = 'https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/'
PIN = '71ad07a3f200284b01d6ee18fc4cc8732fe0542b80556e2cc798247505daa60b'
SNAPREL = '.ufo/waves/round-31/fixture/Defragmentation.rst'


def env():
    e = {k: v for k, v in os.environ.items()
         if not (k.startswith('GIT_') or k.startswith('LD_') or k.startswith('PYTHON'))}
    e.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
              'GIT_CONFIG_SYSTEM': os.devnull, 'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'})
    return e


def git(*args, check=True):
    p = subprocess.run(['/usr/bin/git', '-C', REPO, *args], capture_output=True, env=env())
    if check and p.returncode:
        raise SystemExit('git %s: %s' % (args, p.stderr.decode()))
    return p


DATA = open(os.path.join(SNAPS, 'Defragmentation.rst'), 'rb').read()
LINE25 = DATA.decode().splitlines()[24]
QUOTE = ' '.join(LINE25.split()[:25])        # 6..25 words, substring of line 25, carries 'defragment'
assert QUOTE in LINE25 and hashlib.sha256(DATA).hexdigest() == PIN

REGROW = (f'| S164 | btrfs-progs v7.1 Documentation/Defragmentation.rst — {URL}Defragmentation.rst '
          f'| docs | A | fixture | sha256 {PIN} | fixture row | mined | 2026-10-22 | on-release | fixture |')
SKILLLINE = '| [R31-Q01] | defragment fixture skill line | fixture | S164 line 25 |'
GOODSTMT = ('The defragment behaviour is recorded in this row of the lane for the record only and nothing at all.')
# ^ >=12 words, carries token 'defragment', shares no 6-word run with the quote.


def base_files(statement=GOODSTMT, snapshot=SNAPREL, regrow=REGROW, skill_extra=SKILLLINE,
               row_extra='', quote=QUOTE, line=25):
    row = ('{"id":"Q01","question":"Q01","statement":%s,"source":"S164",'
           '"snapshot":%s,"line":%d,"quote":%s%s}' % (
               json.dumps(statement), json.dumps(snapshot), line, json.dumps(quote), row_extra))
    entry = '{"rows":[' + row + ']}\n'
    sources = git('show', f'{BASE}:corpus/SOURCES.md').stdout.decode().rstrip('\n') + '\n' + regrow + '\n'
    skill = git('show', f'{BASE}:SKILL.md').stdout.decode().rstrip('\n') + '\n\n' + skill_extra + '\n'
    return {
        'corpus/knowledge/btrfs-repair-r31.json': entry.encode(),
        'corpus/SOURCES.md': sources.encode(),
        'SKILL.md': skill.encode(),
        snapshot: DATA,
    }


def make_commit(files, msg, symlinks=None):
    git('checkout', '-q', '--detach', BASE)
    git('rm', '-rq', '--cached', '--ignore-unmatch', '.', check=False)
    git('checkout', '-q', BASE, '--', '.')
    for path, data in files.items():
        full = os.path.join(REPO, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(data)
        git('add', '-f', path)
    for path, target in (symlinks or {}).items():
        full = os.path.join(REPO, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        if os.path.lexists(full):
            os.remove(full)
        os.symlink(target, full)
        git('add', '-f', path)
    git('-c', 'user.name=atk', '-c', 'user.email=atk@invalid', '-c', 'commit.gpgsign=false',
        'commit', '-qm', msg)
    return git('rev-parse', 'HEAD').stdout.decode().strip()


def run(rev):
    p = subprocess.run(['/usr/bin/python3', os.path.join(REPO, 'tools/check-btrfs-repair-r31.py'),
                        '--revision', rev, '--lane', REPO], capture_output=True, env=env())
    q01 = summ = None
    for ln in p.stdout.decode().splitlines():
        try:
            o = json.loads(ln)
        except ValueError:
            continue
        if o.get('id') == 'Q01':
            q01 = o
        if o.get('predicate'):
            summ = o
    return q01, summ, p.stderr.decode()


def show(name, q01):
    if q01 is None:
        print(f'[{name}] NO Q01 LINE (file-level reject)')
    else:
        print(f'[{name}] new_sourced={q01["new_sourced"]} fail={q01["fail"]}')


SHAPES = {}


def shape(fn):
    SHAPES[fn.__name__] = fn
    return fn


@shape
def s00_baseline():
    return base_files(), {}


@shape
def s01_dupkey_nested():
    # duplicate "id" key inside the row object (nested level).
    return base_files(row_extra=',"id":"Q01"'), {}


@shape
def s02_mined_wrong_cell():
    # status cell = draft, but the TIER cell is exactly "mined".
    reg = (f'| S164 | btrfs-progs v7.1 Documentation/Defragmentation.rst — {URL}Defragmentation.rst '
           f'| docs | mined | fixture | sha256 {PIN} | fixture row | draft | 2026-10-22 | on-release | fixture |')
    return base_files(regrow=reg), {}


@shape
def s03_mined_absent():
    # control: no cell equals "mined" at all.
    reg = (f'| S164 | btrfs-progs v7.1 Documentation/Defragmentation.rst — {URL}Defragmentation.rst '
           f'| docs | A | fixture | sha256 {PIN} | fixture row | draft | 2026-10-22 | on-release | fixture |')
    return base_files(regrow=reg), {}


@shape
def s04_quote_as_statement():
    # control: statement = quote verbatim (13 words) -> must trip the 6-word-run guard.
    return base_files(statement=QUOTE), {}


@shape
def s05_punct_merge():
    # the quote copied verbatim, but a single interior word pair joined by '.' so every
    # 6-word window of the quote is broken, while split() still counts >=12 words.
    # Merge the pivot word pair with '.' (a word char under words()) so that every 6-word
    # window of the quote now contains the merged token and none can match. All words stay
    # readable; split() still counts >=12.
    stmt = QUOTE.replace('extent sharing', 'extent.sharing') + ' recorded for the lane defragment note here now'
    return base_files(statement=stmt), {}


@shape
def s06_unicode_lookalike():
    # the quote copied, but ASCII 'e'->Cyrillic 'e', 'o'->Cyrillic 'o', 'a'->Cyrillic 'a'
    # on every word EXCEPT the token-bearing 'Defragmentation', shifting tokenisation.
    sub = {'e': '\u0435', 'o': '\u043e', 'a': '\u0430'}
    out = []
    for w in QUOTE.split():
        if 'efragment' in w.lower():
            out.append(w)
        else:
            out.append(''.join(sub.get(c, sub.get(c.lower(), c)) if c.lower() in sub else c for c in w))
    stmt = ' '.join(out) + ' and defragment stays here now'
    return base_files(statement=stmt), {}


@shape
def s07_snap_dotslash():
    snap = '.ufo/waves/round-31/./Defragmentation.rst'
    f = base_files(snapshot=SNAPREL)
    # cite the ./-containing path in the row but commit bytes at the real path.
    row_snap = snap
    files = base_files(snapshot=SNAPREL)
    entry = ('{"rows":[{"id":"Q01","question":"Q01","statement":%s,"source":"S164",'
             '"snapshot":%s,"line":25,"quote":%s}]}\n' % (
                 json.dumps(GOODSTMT), json.dumps(row_snap), json.dumps(QUOTE)))
    files['corpus/knowledge/btrfs-repair-r31.json'] = entry.encode()
    return files, {}


@shape
def s08_snap_symlink():
    # commit a symlink at a second path that points at the real snapshot; cite the symlink.
    link = '.ufo/waves/round-31/fixture/link.rst'
    files = base_files(snapshot=SNAPREL)
    entry = ('{"rows":[{"id":"Q01","question":"Q01","statement":%s,"source":"S164",'
             '"snapshot":%s,"line":25,"quote":%s}]}\n' % (
                 json.dumps(GOODSTMT), json.dumps(link), json.dumps(QUOTE)))
    files['corpus/knowledge/btrfs-repair-r31.json'] = entry.encode()
    return files, {link: 'Defragmentation.rst'}


@shape
def s09_skill_in_details():
    extra = '<details>\n<summary>more</summary>\n\n' + SKILLLINE + '\n\n</details>'
    return base_files(skill_extra=extra), {}


@shape
def s10_skill_in_fence():
    extra = '```\n' + SKILLLINE + '\n```'
    return base_files(skill_extra=extra), {}


@shape
def s11_skill_indented():
    extra = '    ' + SKILLLINE  # 4-space indent
    return base_files(skill_extra=extra), {}


@shape
def s12_skill_double_details():
    extra = SKILLLINE + '\n\n<details>\n\n' + SKILLLINE + '\n\n</details>'
    return base_files(skill_extra=extra), {}


def main():
    results = {}
    for name in sorted(SHAPES):
        files, links = SHAPES[name]()
        rev = make_commit(files, name, links)
        q01, summ, err = run(rev)
        show(name, q01)
        if err.strip():
            print('   stderr:', err.strip()[:200])
        results[name] = {'commit': rev, 'q01': q01, 'summary': summ}
    out = os.path.join(os.path.dirname(__file__), 'results.json')
    with open(out, 'w') as fh:
        json.dump(results, fh, indent=1)
    print('wrote', out)


if __name__ == '__main__':
    main()
