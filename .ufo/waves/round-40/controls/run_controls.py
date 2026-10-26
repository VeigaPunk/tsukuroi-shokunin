#!/usr/bin/env python3
"""Round-40 pre-data controls (L1 TsukuroiR40). Scores each control variant with the FROZEN counters
(tool bytes taken from the freeze commit) in scratch clones of the lane; writes controls.jsonl.

Usage: run_controls.py --lane <lane> --freeze <rev> --base <rev> --cand-dir <dir with candidate files>
       --scratch <dir> --out <controls.jsonl>
The candidate dir holds tools/tsukuroi-census.sh, corpus/SOURCES.md and
corpus/knowledge/pacman-exec-environment-r40.md (the round's claimed after-state, not yet landed).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

ENTRY = 'corpus/knowledge/pacman-exec-environment-r40.md'
C1 = 'tools/score-selftest-literals-r40.py'
C2 = 'tools/check-exec-environment-r40.py'
GENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
        'HOME': '/nonexistent'}


def git(d, *a, check=True):
    p = subprocess.run(['git', '-C', d, *a], env=GENV, capture_output=True, text=True)
    if check and p.returncode:
        raise SystemExit(f'git {a}: {p.stderr}')
    return p.stdout.strip()


def clone(lane, root, name, rev):
    d = os.path.join(root, name)
    shutil.rmtree(d, ignore_errors=True)
    subprocess.run(['git', 'clone', '-q', '--shared', lane, d], env=GENV, check=True)
    git(d, 'remote', 'remove', 'origin')
    assert git(d, 'rev-parse', '--show-toplevel') == d
    git(d, 'checkout', '-q', '-B', 'master', rev)
    return d


def commit(d, msg):
    assert git(d, 'rev-parse', '--show-toplevel') == d
    git(d, 'add', '-A')
    git(d, '-c', 'user.name=fixture', '-c', 'user.email=fixture@shokunin.local', 'commit', '-q', '--allow-empty',
        '-m', msg)
    return git(d, 'rev-parse', 'HEAD')


def tool_bytes(lane, freeze, path):
    return subprocess.run(['git', '-C', lane, 'show', f'{freeze}:{path}'], env=GENV, capture_output=True,
                          check=True).stdout


def run_counter(d, tool, rev, extra):
    p = subprocess.run([sys.executable, os.path.join(d, tool), '--repo', d, '--revision', rev, *extra],
                       env={**GENV, 'TMPDIR': extra[1] if extra else '/tmp'}, capture_output=True, text=True,
                       timeout=3600)
    try:
        return p.returncode, json.loads(p.stdout)
    except ValueError:
        return p.returncode, {'raw': p.stdout[-500:], 'stderr': p.stderr[-500:]}


def rows(text):
    return [l for l in text.splitlines() if re.match(r'^\|\s*EX\d+\s*\|', l)]


def map_rows(text, fn):
    out = []
    for l in text.splitlines():
        if re.match(r'^\|\s*EX\d+\s*\|', l):
            cells = l.strip().strip('|').split('|')
            cells = [c.strip() for c in cells]
            cells = fn(cells)
            l = '| ' + ' | '.join(cells) + ' |'
        out.append(l)
    return '\n'.join(out) + '\n'


QUOTE_RE = re.compile(r'“([^”]+)”')
TOKENS_ALL = ['working directory', 'chroot', '`/`', 'stdout', 'stderr', 'stdin', 'end-of-file', 'SHLVL',
              'BASH_ENV', 'umask', '0022', '/usr/bin/bash', '/bin/sh', '-c', 'tmp/alpm_XXXXXX', '.INSTALL', '01777',
              'NeedsTargets', 'sorted', 'duplicate', 'Depends', 'running', 'AbortOnFail', 'satisfy dependencies',
              'file list', 'NoExtract', 'NoUpgrade', '.pacnew']


def c2_variants(cand_entry):
    v = {}
    v['C2-K1-x-empty'] = map_rows(cand_entry, lambda c: [c[0], 'RULE NOT SUPPLIED', *c[2:]])
    v['C2-K2a-x-false-negated'] = map_rows(cand_entry, lambda c: [c[0], c[1] + ' — none of this holds on Arch, it is not the behaviour', *c[2:]])
    v['C2-K2b-x-false-values'] = map_rows(cand_entry, lambda c: [c[0], c[1].replace('0022', '0077').replace('/usr/bin/bash', '/usr/bin/zsh'), 'unknown', *c[3:]])
    v['C2-K3-own-work-only'] = map_rows(cand_entry, lambda c: [*c[:3], re.sub(r'\bS2(19|2[0-4])\b', 'S225', c[3]), c[4]])
    held = {'util.c': 'S216', 'trans.c': 'S217', 'hook.c': 'S208', 'PKGBUILD': 'S216'}

    def to_held(c):
        s = c[3]
        for k, sid in held.items():
            if re.search(r'\b' + re.escape(k) + r':', s):
                s = re.sub(r'\bS2(19|2[0-5])\b', sid, s, count=1)
                break
        return [*c[:3], s, c[4]]
    held_text = map_rows(cand_entry, to_held)
    held_text = re.sub(r'^source: S219, S220, S221, S222, S223, S224, S225', 'source: S208, S216, S217, S219, S220, S221, S222, S223, S224, S225', held_text, flags=re.M)
    v['C2-K4-held-rows'] = held_text

    def quote_rule(c):
        q = QUOTE_RE.findall(c[3])
        return [c[0], (q[0] if q else '') + ' ' + ' '.join(TOKENS_ALL), *c[2:]]
    v['C2-K5-scripted-quote-rule'] = map_rows(cand_entry, quote_rule)
    lines = cand_entry.splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith('## Rules'))
    j = next(k for k, l in enumerate(lines) if k > i and l.startswith('## ') )
    v['C2-K6-duplicated-block'] = '\n'.join(lines[:j] + lines[i:j] + lines[j:]) + '\n'
    return v


def c1_variants(base_census, cand_census):
    v = {}
    mono = ''.join(
        f"  case_home='storage-mono-{n}'; FX=\"$work/fx/$case_home\"; mkdir -p \"$FX\"; fx_default \"$FX\"\n"
        f"  printf 'proc /proc proc rw 0 0\\n%s\\n' \"$fxmt\" > \"$FX/mounts\"\n"
        f"  check 'mono {n}: btrfs mounted with no sysfs root is BLOCKED' 0 HEALTHY \\\n"
        f"    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'\n"
        for n in range(1, 6))
    anchor = "  check_cli 'cli: unknown argument exits 2 with usage (S10-2)' 2 \\\n"
    assert base_census.count(anchor) == 1
    v['C1-K1-one-literal-fixtures'] = base_census.replace(anchor, mono + '\n' + anchor)
    selfchk = ('  grep -qF \'if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi\' "$SELF" '
               '&& grep -qF \'if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]; then\' "$SELF" '
               '&& grep -qF \'mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null)\' "$SELF" '
               '&& ! grep -q \'case $mtab in\' "$SELF" '
               '|| { echo "TSUKUROI_CENSUS_SELFTEST: FAIL (self-read)"; return 1; }\n')
    a2 = '  local bin fx\n'
    assert base_census.count(a2) == 1
    v['C1-K2-self-reading-selftest'] = base_census.replace(a2, a2 + selfchk)
    v['C1-K3-arm-rewritten'] = cand_census.replace('while read -r _src _mp fst _rest; do', 'while read -r _src _mp fstype _rest; do').replace('if [ "${fst:-}" = btrfs ]; then', 'if [ "${fstype:-}" = btrfs ]; then')
    v['C1-K4-candidate'] = cand_census
    return v


def main():
    ap = argparse.ArgumentParser()
    for k in ('lane', 'freeze', 'base', 'cand-dir', 'scratch', 'out'):
        ap.add_argument('--' + k, required=True)
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    sha = {t: hashlib.sha256(tool_bytes(a.lane, a.freeze, t)).hexdigest() for t in (C1, C2)}
    cand = {p: open(os.path.join(a.cand_dir, p)).read() for p in
            ('tools/tsukuroi-census.sh', 'corpus/SOURCES.md', ENTRY)}
    base_census = tool_bytes(a.lane, a.base, 'tools/tsukuroi-census.sh').decode()
    out = open(a.out, 'w')

    def emit(name, claim, rc, rec, rev):
        keep = {k: rec.get(k) for k in ('rules_verified', 'source_ok', 'counts_ok', 'novelty_base_hits',
                                         'duplicate_rows', 'duplicate_headings', 'baseline_pass', 'neutral_pass',
                                         'mutants_applied', 'survivors', 'survivor_names', 'selfref', 'result',
                                         'error', 'raw')}
        if claim == 'C2':
            keep['row_reasons'] = {k: v['reasons'] for k, v in rec.get('rules', {}).items() if v.get('reasons')}
        row = {'control': name, 'claim': claim, 'counter': C1 if claim == 'C1' else C2,
               'counter_sha256': sha[C1 if claim == 'C1' else C2], 'revision': rev, 'exit': rc, **keep}
        out.write(json.dumps(row) + '\n')
        out.flush()
        print(name, rc, keep.get('result'), file=sys.stderr)

    sc = os.path.join(a.scratch, 'c1s')
    # C2 controls
    d = clone(a.lane, a.scratch, 'c2', a.freeze)
    rc, rec = run_counter(d, C2, a.base, [])
    emit('C2-K0-do-nothing-base', 'C2', rc, rec, git(d, 'rev-parse', a.base))
    for p, t in cand.items():
        if p != 'tools/tsukuroi-census.sh':
            open(os.path.join(d, p), 'w').write(t)
    cand_rev = commit(d, 'C2 candidate')
    for name, text in c2_variants(cand[ENTRY]).items():
        git(d, 'checkout', '-q', cand_rev)
        git(d, 'checkout', '-q', '-B', 'master')
        open(os.path.join(d, ENTRY), 'w').write(text)
        r = commit(d, name)
        rc, rec = run_counter(d, C2, r, [])
        emit(name, 'C2', rc, rec, r)
    git(d, 'checkout', '-q', '-B', 'master', cand_rev)
    rc, rec = run_counter(d, C2, cand_rev, [])
    emit('C2-K7-candidate', 'C2', rc, rec, cand_rev)
    # C1 controls
    d1 = clone(a.lane, a.scratch, 'c1', a.freeze)
    rc, rec = run_counter(d1, C1, a.base, ['--scratch', sc])
    emit('C1-K0-do-nothing-base', 'C1', rc, rec, git(d1, 'rev-parse', a.base))
    start = git(d1, 'rev-parse', 'HEAD')
    for name, text in c1_variants(base_census, cand['tools/tsukuroi-census.sh']).items():
        git(d1, 'checkout', '-q', '-B', 'master', start)
        open(os.path.join(d1, 'tools/tsukuroi-census.sh'), 'w').write(text)
        r = commit(d1, name)
        rc, rec = run_counter(d1, C1, r, ['--scratch', sc])
        emit(name, 'C1', rc, rec, r)
    out.close()
    shutil.rmtree(a.scratch, ignore_errors=True)


if __name__ == '__main__':
    main()
