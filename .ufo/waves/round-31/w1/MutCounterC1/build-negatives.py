#!/usr/bin/env python3
"""Build one-rule-violating negative fixtures from the positive fixture, as commits on top of it.

Each fixture is derived from the pristine positive commit via `git show` (never from the
working tree, so no fixture can leak into the next). Each violates exactly one counter rule.
"""
import hashlib
import json
import os
import subprocess
import sys

REPO = '/fast/scratch/hyaku/tsukuroi-r31/MutCounterC1/work/c1-fixture'
ENTRY = 'corpus/knowledge/btrfs-repair-r31.json'
SNAPDIR = '.ufo/waves/round-31/mutc1'


def env():
    e = {k: v for k, v in os.environ.items()
         if not (k.startswith('GIT_') or k.startswith('LD_') or k.startswith('PYTHON'))}
    e.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
              'GIT_CONFIG_SYSTEM': os.devnull, 'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'})
    return e


def git(*args):
    p = subprocess.run(['/usr/bin/git', '-C', REPO, *args], capture_output=True, env=env())
    if p.returncode:
        raise SystemExit('git %s failed: %s' % (args, p.stderr.decode()))
    return p.stdout


def show(rev, path):
    return git('show', f'{rev}:{path}').decode()


def write_commit(base, files, label):
    git('checkout', '-q', '--detach', base)
    for path, data in files.items():
        full = os.path.join(REPO, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, 'wb').write(data if isinstance(data, bytes) else data.encode())
        git('add', path)
    git('-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid', '-c',
        'commit.gpgsign=false', 'commit', '-qm', label)
    return git('rev-parse', 'HEAD').decode().strip()


def main():
    base = sys.argv[1]
    out = {}
    trim = show(base, f'{SNAPDIR}/Trim.rst')
    reg = show(base, 'corpus/SOURCES.md')
    skill = show(base, 'SKILL.md')
    entry = json.loads(show(base, ENTRY))

    def edited(fn):
        import copy
        d = copy.deepcopy(entry)
        fn(d)
        return json.dumps(d, indent=1) + '\n'

    def doc(q, **kw):
        def f(d):
            for r in d['rows']:
                if r['id'] == q:
                    r.update(kw)
        return edited(f)

    # R1: two rows for Q03 / an extra id Q09.
    def dup(d):
        d['rows'].append(dict([x for x in d['rows'] if x['id'] == 'Q03'][0]))
    out['N-R1dup'] = write_commit(base, {ENTRY: edited(dup)}, 'N-R1dup')

    def extra(d):
        r = dict([x for x in d['rows'] if x['id'] == 'Q03'][0])
        r['id'] = 'Q09'
        d['rows'].append(r)
    out['N-R1extra'] = write_commit(base, {ENTRY: edited(extra)}, 'N-R1extra')

    # R2: an extra key in the Q03 row.
    def addkey(d):
        for x in d['rows']:
            if x['id'] == 'Q03':
                x['note'] = 'extra'
    out['N-R2'] = write_commit(base, {ENTRY: edited(addkey)}, 'N-R2')

    # R3 sha: bytes differ from the pin, cited lines untouched.
    out['N-R3sha'] = write_commit(base, {f'{SNAPDIR}/Trim.rst': trim + '<!-- pad -->\n'}, 'N-R3sha')
    # R3 path: same bytes, path outside .ufo/waves/round-31/.
    out['N-R3path'] = write_commit(base, {
        '.ufo/waves/round-31-other/Trim.rst': trim,
        ENTRY: doc('Q08', snapshot='.ufo/waves/round-31-other/Trim.rst')}, 'N-R3path')

    # R4 line: cite a line that does not hold the quote. R4 words: a 4-word quote.
    out['N-R4line'] = write_commit(base, {ENTRY: doc('Q08', line=30)}, 'N-R4line')
    out['N-R4words'] = write_commit(base, {
        ENTRY: doc('Q08', quote=' '.join(trim.splitlines()[28].split()[:4]))}, 'N-R4words')

    # R5 status / count / base-registry.
    out['N-R5status'] = write_commit(base, {'corpus/SOURCES.md': reg.replace(
        '| mined | 2026-10-22 | on-release | fixture |',
        '| draft | 2026-10-22 | on-release | fixture |', 1)}, 'N-R5status')
    s166 = [ln for ln in reg.splitlines() if ln.startswith('| S166 |')][0]
    out['N-R5count'] = write_commit(base, {'corpus/SOURCES.md': reg.rstrip('\n') + '\n' + s166 + '\n'},
                                    'N-R5count')
    pin = '927b67b4ab13f681866e699fcd6ea4917a42ef08e4db1731b0adf065022d955c'
    lines = []
    for ln in reg.splitlines():
        if ln.startswith('| S001 |'):
            ln = ('| S001 | btrfs-progs v7.1 Documentation/btrfs-check.rst — '
                  'https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/'
                  f'btrfs-check.rst | docs | A | fixture | sha256 {pin} | fixture row | mined | '
                  '2026-10-22 | on-release | fixture |')
        lines.append(ln)
    out['N-R5base'] = write_commit(base, {'corpus/SOURCES.md': '\n'.join(lines) + '\n',
                                          ENTRY: doc('Q03', source='S001')}, 'N-R5base')

    # R6: drop the Q03 SKILL.md line / fence it / comment it.
    line3 = [ln for ln in skill.splitlines() if ln.startswith('| [R31-Q03] ')][0]
    out['N-R6skill'] = write_commit(base, {'SKILL.md': skill.replace(line3 + '\n', '')}, 'N-R6skill')
    out['N-R6fence'] = write_commit(base, {'SKILL.md': skill.replace(
        line3, '```\n' + line3 + '\n```')}, 'N-R6fence')
    out['N-R6comment'] = write_commit(base, {'SKILL.md': skill.replace(
        line3, '<!--\n' + line3 + '\n-->')}, 'N-R6comment')

    # R7: missing sealed key group / a 6-word run / a 5-word run with the quote.
    q01 = [x for x in entry['rows'] if x['id'] == 'Q01'][0]
    out['N-R7key'] = write_commit(base, {ENTRY: doc(
        'Q01', statement=q01['statement'].replace('data space', 'data room'))}, 'N-R7key')
    q1 = q01['quote']
    out['N-R7run6'] = write_commit(base, {ENTRY: doc(
        'Q01', statement=q01['statement'] + ' ' + ' '.join(q1.split()[:6]))}, 'N-R7run6')
    out['N-R7run5'] = write_commit(base, {ENTRY: doc(
        'Q01', statement=q01['statement'] + ' ' + ' '.join(q1.split()[:5]))}, 'N-R7run5')

    # pin prefix: grind bytes whose sha256 shares the pin's first 4 hex, cited lines untouched.
    raw = trim.encode()
    i = 0
    while True:
        cand = raw + ('<!-- pad %d -->\n' % i).encode()
        if hashlib.sha256(cand).hexdigest().startswith('2a11'):
            break
        i += 1
    out['N-pinprefix'] = write_commit(base, {f'{SNAPDIR}/Trim.rst': cand}, 'N-pinprefix')
    print(json.dumps({'pin_grind': i, 'sha256': hashlib.sha256(cand).hexdigest()}))
    for k, v in out.items():
        print(json.dumps({'fixture': k, 'commit': v}))


if __name__ == '__main__':
    main()
