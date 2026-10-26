#!/usr/bin/env python3
"""Round-41 pre-data controls: score cheap variants that skip the claimed work with the FROZEN counters.

Each control is a fixture clone of the lane at the freeze revision (git clone --shared, origin removed,
fixture identity, toplevel checked), one commit carrying the variant files, then the frozen counter run
with --repo <clone>. Output: one JSON line per control on stdout. Scratch under --scratch, removed at exit.
Usage: run_controls.py --lane <lane> --freeze <REV> --scratch <DIR> [--only c1|c2] [--jobs N]
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ENTRY = 'corpus/knowledge/alpm-package-anatomy-r41.md'
CENSUS = 'tools/tsukuroi-census.sh'
ENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': '/nonexistent', 'GIT_CONFIG_NOSYSTEM': '1',
       'GIT_CONFIG_GLOBAL': '/dev/null'}


def git(d, *a, check=True):
    return subprocess.run(['git', '-C', str(d), *a], env=ENV, capture_output=True, text=True, check=check)


def fixture(lane, rev, scratch, name, files):
    d = Path(tempfile.mkdtemp(prefix=name + '.', dir=scratch))
    subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', str(lane), str(d)], env=ENV, check=True)
    git(d, 'remote', 'remove', 'origin')
    assert git(d, 'rev-parse', '--show-toplevel').stdout.strip() == str(d)
    git(d, 'checkout', '-q', '-B', 'master', rev)
    for path, content in files.items():
        p = d / path
        if content is None:
            if p.exists():
                git(d, 'rm', '-q', path)
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        git(d, 'add', path)
    git(d, '-c', 'user.name=fixture', '-c', 'user.email=fixture@shokunin.local', 'commit', '-q',
        '--allow-empty', '-m', 'control ' + name)
    return d, git(d, 'rev-parse', 'HEAD').stdout.strip()


def score(lane, tool, d, rev, extra, scratch):
    cmd = ['python3', str(Path(lane) / 'tools' / tool), '--repo', str(d), '--revision', rev] + extra
    p = subprocess.run(cmd, env=ENV, capture_output=True, text=True, timeout=7200)
    try:
        r = json.loads(p.stdout)
    except ValueError:
        r = {'parse_error': p.stdout[-400:], 'stderr': p.stderr[-400:]}
    r['exit'] = p.returncode
    return r


# ---------------- C1 variants ----------------
MARKERS = ["case $mtab in", 'fst,,', 'grep -c btrfs', 'tail -n 1 -- "$PROC_MOUNTS"', 'if [ "$fsn" -eq 0 ]; then',
           '${_mp:-} == /*', '${_src:-} == /dev/*', '"$mt" -eq 1']


def prologue(text):
    g = ' '.join("-e '" + m.replace("'", "'\\''") + "'" for m in MARKERS)
    line = (f'  if declare -f probe_storage_arm | grep -qF {g}; then printf '
            "'TSUKUROI_CENSUS_SELFTEST: FAIL (1 cases, 0 passed, 1 failed)\\n'; return 1; fi\n")
    anchor = 'run_selftest() {\n'
    assert text.count(anchor) == 1
    return text.replace(anchor, anchor + line)


def drop_case(text, case):
    lines = text.split('\n')
    i = next(k for k, l in enumerate(lines) if f"case_home='{case}'" in l)
    j = i
    while lines[j].strip():
        j += 1
    return '\n'.join(lines[:i] + lines[j + 1:])


# ---------------- C2 variants ----------------
NATO = 'alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima mike'


def rows(entry):
    return [l for l in entry.splitlines() if re.match(r'^\|\s*PA\d+\s*\|', l)]


def set_rows(entry, new):
    old = rows(entry)
    for o, n in zip(old, new):
        entry = entry.replace(o, n)
    return entry


def cells(l):
    return [c.strip() for c in l.strip().strip('|').split('|')]


def mk(c):
    return '| ' + ' | '.join(c) + ' |'


def first_line_quote(src_text):
    for k, l in enumerate(src_text.splitlines(), 1):
        w = [x for x in l.replace('|', ' ').replace('“', ' ').replace('”', ' ').split() if not re.match(r'S\d{3,}', x)]
        if 4 <= len(w) <= 25:
            return k, ' '.join(w)
    return 1, 'x'


def writer_r40(entry, mod):
    """round-40 C2CritControl writer adapted: value derived, rule = value tokens + NATO filler, quote =
    first 4-25 word line of the required file."""
    out = []
    for l in rows(entry):
        c = cells(l)
        pa = c[0]
        f = mod.REQUIRED[pa][0]
        k, q = first_line_quote((mod.SRC_DIR / f).read_text(errors='replace'))
        sid = re.search(r'S\d{3,}', c[3]).group(0)
        c[1] = c[2].replace('`', '') + ' ' + NATO
        c[3] = f'{sid} {f}:{k}-{k} “{q}”'
        out.append(mk(c))
    return set_rows(entry, out)


def literal_of(rx):
    s = re.sub(r'\\b', '', rx)
    s = re.sub(r'\.\{0,\d+\}|\.\*', ' ', s)
    s = s.replace('\\(', '(').replace('\\)', ')').replace('\\.', '.').replace('\\$', '$')
    return ' '.join(s.split())


def writer_relations(entry, mod):
    """relation-literal writer: rule = the frozen RELATIONS read back as literals + filler; quote and
    value kept from the candidate (inside the window). The recorded lexical bypass."""
    out = []
    for l in rows(entry):
        c = cells(l)
        c[1] = ' ; '.join(literal_of(r) for r in mod.RELATIONS[c[0]]) + ' ' + NATO
        out.append(mk(c))
    return set_rows(entry, out)


def swap(entry):
    e = entry.replace('`.INSTALL` becomes `install`', '`.INSTALL` becomes `mtree`') \
             .replace('`.MTREE` becomes `mtree`', '`.MTREE` becomes `install`')
    e = e.replace('`check()` each run inside `$srcdir` and `verify()` runs inside `$startdir`',
                  '`check()` each run inside `$startdir` and `verify()` runs inside `$srcdir`')
    return e


def negate(entry):
    return entry.replace('only `.PKGINFO` sets the metadata flag', 'only `.PKGINFO` does not set the metadata flag') \
                .replace('`package()` also runs under fakeroot', '`package()` never runs under fakeroot')


def verdict_files(kind_by_row):
    out = {}
    for n in range(1, 9):
        k = kind_by_row.get(n, 'holds')
        if k is None:
            continue
        out[f'.ufo/waves/round-41/w1/C2RevPA{n}.md'] = f'VERDICT: {k}\nrow PA{n}; control fixture verdict\n'
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--freeze', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--only', choices=['c1', 'c2'])
    ap.add_argument('--jobs', default='8')
    ap.add_argument('--names', nargs='*', help='run only these control names (added after the first C1 launch: K0 and '
                    'K4 duplicate the before and after receipts, so C1 runs K1-K3 as parallel processes)')
    a = ap.parse_args()
    lane = Path(a.lane)
    Path(a.scratch).mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix='r41ctl.', dir=a.scratch))
    sys.path.insert(0, str(lane / 'tools'))
    import importlib.util
    spec = importlib.util.spec_from_file_location('c2', lane / 'tools/check-package-anatomy-r41.py')
    c2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c2)
    try:
        base_census = git(lane, 'show', f'{a.freeze}:{CENSUS}').stdout
        cand_census = (lane / CENSUS).read_text()
        cand_entry = (lane / ENTRY).read_text()
        cand_sources = (lane / 'corpus/SOURCES.md').read_text()
        if a.only in (None, 'c1'):
            c1 = {
                'C1-K0-do-nothing': {},
                'C1-K1-declare-f-prologue-on-base': {CENSUS: prologue(base_census)},
                'C1-K2-candidate-without-H9-case': {CENSUS: drop_case(cand_census, 'storage-mounts-no-subvol-opt')},
                'C1-K3-declare-f-prologue-on-candidate': {CENSUS: prologue(cand_census)},
                'C1-K4-candidate': {CENSUS: cand_census},
            }
            for name, files in c1.items():
                if a.names and name not in a.names:
                    continue
                d, rev = fixture(lane, a.freeze, scratch, name, files)
                r = score(lane, 'score-selftest-mounts-r41.py', d, rev,
                          ['--scratch', str(scratch / (name + '.work')), '--jobs', a.jobs], scratch)
                keep = {k: r.get(k) for k in ('baseline_pass', 'capture_pass', 'neutral_pass', 'decoy_pass',
                                              'mutants_applied', 'survivors', 'survivor_names', 'params',
                                              'result', 'exit', 'error')}
                keep['decoys_failed'] = sorted(k for k, v in (r.get('decoys') or {}).items() if not v.get('pass'))
                print(json.dumps({'control': name, 'revision': rev, **keep}), flush=True)
                shutil.rmtree(d, ignore_errors=True)
        if a.only in (None, 'c2'):
            base_files = {ENTRY: cand_entry, 'corpus/SOURCES.md': cand_sources}
            c2v = {
                'C2-K0-do-nothing': {},
                'C2-K1-r40-token-writer': {**base_files, ENTRY: writer_r40(cand_entry, c2), **verdict_files({})},
                'C2-K2-relation-literal-writer-no-verdicts': {**base_files, ENTRY: writer_relations(cand_entry, c2)},
                'C2-K3-x-false-swap': {**base_files, ENTRY: swap(cand_entry), **verdict_files({})},
                'C2-K4-x-false-negation': {**base_files, ENTRY: negate(cand_entry), **verdict_files({})},
                'C2-K5-candidate-one-fails-verdict': {**base_files, **verdict_files({4: 'fails'})},
                'C2-K6-candidate-no-verdicts': dict(base_files),
                'C2-K7-candidate-one-partly-only': {**base_files, **verdict_files({7: 'partly'})},
                'C2-K8-candidate': {**base_files, **verdict_files({})},
            }
            for name, files in c2v.items():
                d, rev = fixture(lane, a.freeze, scratch, name, files)
                r = score(lane, 'check-package-anatomy-r41.py', d, rev, [], scratch)
                keep = {k: r.get(k) for k in ('rules_verified', 'verdicts_ok', 'host_ok', 'source_ok',
                                              'duplicate_rows', 'duplicate_headings', 'novelty_base_hits',
                                              'result', 'exit', 'error')}
                keep['row_reasons'] = {k: v['reasons'][:3] for k, v in (r.get('rules') or {}).items() if v['reasons']}
                print(json.dumps({'control': name, 'revision': rev, **keep}), flush=True)
                shutil.rmtree(d, ignore_errors=True)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    main()
