#!/usr/bin/env python3
"""C2MutCounter-3 (round-40 w1 item C2-12): counter mutants vs pre-data C2 controls.

Re-implements ONLY the C2 half of .ufo/waves/round-40/controls/run_controls.py
(controls C2-K0..C2-K7; variant builders copied verbatim), then re-runs the same
control set with mutated counters. Three supplementary controls (C2X-*) are added
as liveness proofs for conjuncts the frozen set does not guard:
  C2X-K1b-tokens-only-rule   rule = the row's frozen tokens only (<12 words)
  C2X-K2c-value-only         only the value cell tampered ('unknown')
  C2X-K4b-held-rows-usedby   K4 held rows PLUS the entry appended to their used_by
All clones/commits live under the seat scratch dir; the lane is never touched.
Output: <scratch>/runs.jsonl + stdout summary.
"""
import difflib
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
FREEZE = 'a447b67b2502bae1e96fda341ae5ad32243ae524'
BASE = '53b294a274656be6479aadf2ec2fee890ded77ce'
C2 = 'tools/check-exec-environment-r40.py'
ENTRY = 'corpus/knowledge/pacman-exec-environment-r40.md'
ENTRY_NAME = 'pacman-exec-environment-r40.md'
SOURCES = 'corpus/SOURCES.md'
PRISTINE_SHA = 'd4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d'
CAND = {
    SOURCES: ('bf2380503b8e4a5d33162026854b0b7b66d18b86',
              '1676992a3d2013e2c9e4a9d6715f704bb287e37cc6942bd0f05c5c1a2c2c42a1'),
    ENTRY: ('bf2380503b8e4a5d33162026854b0b7b66d18b86',
            '2230ccaf4037ccfcb8628b97f15fcff9eca86f9e5e37bee1c5392712ce21c9ef'),
}
GENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'GIT_CONFIG_NOSYSTEM': '1',
        'GIT_CONFIG_GLOBAL': os.devnull, 'HOME': '/nonexistent'}
SCRATCH = '/fast/scratch/hyaku/tsukuroi-r40/C2MutCounter'

_spec = importlib.util.spec_from_file_location('c2counter', os.path.join(LANE, C2))
_c2mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_c2mod)
TOKENS = _c2mod.TOKENS

# --- exact mutation targets (each verified to occur exactly once in the frozen bytes) ---
M1_OLD = ("            neg = NEG.search(rule.replace('`', ''))\n"
          "            if neg:\n"
          "                r['reasons'].append(f'rule carries negation word {neg.group(0)!r}')\n")
P1_OLD = ("            rc = collapse(rule)\n"
          "            if len(rc.split()) < 12:\n"
          "                r['reasons'].append('rule shorter than 12 words')\n")
MW_OLD = ("            if len(rc.split()) < 12:\n"
          "                r['reasons'].append('rule shorter than 12 words')\n")
P2_OLD = "                        copied = copied or qc in rc\n"
P3_OLD = ("            if copied:\n"
          "                r['reasons'].append('rule cell contains its own quote')\n")
M3_OLD = ("            upstream = [i for i in ids if i in srows and i not in base_ids and "
          "srows[i]['status'] == 'mined'\n")
M3_NEW = ("            upstream = [i for i in ids if i in srows and srows[i]['status'] == 'mined'\n")
M4_OLD = ("            if value.replace('`', '').strip() != vals[ex]:\n"
          "                r['reasons'].append(f'value {value!r} != derived {vals[ex]!r}')\n")
M5_OLD = ("    ok = (verified == 8 and dup_rows == 0 and dup_heads == 0 and source_ok == 1 "
          "and counts_ok == 2\n"
          "          and nov_total == 0)\n")
M5_NEW = ("    ok = (verified == 8 and dup_rows == 0 and dup_heads == 0 and source_ok == 1 "
          "and counts_ok == 2)\n")

MUTANTS = [
    ('M1-drop-neg', [('neg-check', M1_OLD, '')]),
    ('M2-drop-paraphrase', [('rc+minwords', P1_OLD, ''), ('copied-acc', P2_OLD, ''),
                            ('copied-reason', P3_OLD, '')]),
    ('M2a-drop-minwords', [('minwords', MW_OLD, '')]),
    ('M2b-drop-copied-quote', [('copied-reason', P3_OLD, '')]),
    ('M3-accept-base-rows', [('base-ids-exclusion', M3_OLD, M3_NEW)]),
    ('M4-skip-value-compare', [('value-compare', M4_OLD, '')]),
    ('M5-skip-novelty', [('novelty-predicate-term', M5_OLD, M5_NEW)]),
]


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
    git(d, '-c', 'user.name=fixture', '-c', 'user.email=fixture@shokunin.local', 'commit', '-q',
        '--allow-empty', '-m', msg)
    return git(d, 'rev-parse', 'HEAD')


def run_counter(d, rev):
    p = subprocess.run([sys.executable, os.path.join(d, C2), '--repo', d, '--revision', rev],
                       env={**GENV, 'TMPDIR': SCRATCH}, capture_output=True, text=True, timeout=3600)
    try:
        return p.returncode, json.loads(p.stdout)
    except ValueError:
        return p.returncode, {'raw': p.stdout[-500:], 'stderr': p.stderr[-500:]}


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
HELD = {'util.c': 'S216', 'trans.c': 'S217', 'hook.c': 'S208', 'PKGBUILD': 'S216'}


def to_held(c, skip=()):
    s = c[3]
    for k, sid in HELD.items():
        if c[0] not in skip and re.search(r'\b' + re.escape(k) + r':', s):
            s = re.sub(r'\bS2(19|2[0-5])\b', sid, s, count=1)
            break
    return [*c[:3], s, c[4]]


def held_source_line(held_text):
    return re.sub(r'^source: S219, S220, S221, S222, S223, S224, S225',
                  'source: S208, S216, S217, S219, S220, S221, S222, S223, S224, S225',
                  held_text, flags=re.M)


def used_by_edit(sources_text):
    out, n = [], 0
    for l in sources_text.splitlines():
        if re.match(r'^\| *S(208|216|217) *\|', l):
            cells = [c.strip() for c in l.strip().strip('|').split('|')]
            assert len(cells) >= 11 and ENTRY_NAME not in cells[10], l[:120]
            cells[10] = cells[10] + ', ' + ENTRY_NAME
            l = '| ' + ' | '.join(cells) + ' |'
            n += 1
        out.append(l)
    assert n == 3, f'used_by edit touched {n} rows, expected 3'
    return '\n'.join(out) + '\n'


def all_variants(cand_entry, cand_sources):
    """Frozen C2 controls (verbatim builders) + supplementary C2X controls.

    Returns {name: (entry_text, sources_text_or_None)}."""
    v = {}
    v['C2-K1-x-empty'] = (map_rows(cand_entry, lambda c: [c[0], 'RULE NOT SUPPLIED', *c[2:]]), None)
    v['C2-K2a-x-false-negated'] = (map_rows(cand_entry, lambda c: [c[0], c[1] + ' — none of this holds on Arch, it is not the behaviour', *c[2:]]), None)
    v['C2-K2b-x-false-values'] = (map_rows(cand_entry, lambda c: [c[0], c[1].replace('0022', '0077').replace('/usr/bin/bash', '/usr/bin/zsh'), 'unknown', *c[3:]]), None)
    v['C2-K3-own-work-only'] = (map_rows(cand_entry, lambda c: [*c[:3], re.sub(r'\bS2(19|2[0-4])\b', 'S225', c[3]), c[4]]), None)
    held_text = map_rows(cand_entry, to_held)
    held_text = held_source_line(held_text)
    assert held_text != map_rows(cand_entry, to_held), 'K4 source: rewrite did not apply'
    v['C2-K4-held-rows'] = (held_text, None)

    def quote_rule(c):
        q = QUOTE_RE.findall(c[3])
        return [c[0], (q[0] if q else '') + ' ' + ' '.join(TOKENS_ALL), *c[2:]]
    v['C2-K5-scripted-quote-rule'] = (map_rows(cand_entry, quote_rule), None)
    lines = cand_entry.splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith('## Rules'))
    j = next(k for k, l in enumerate(lines) if k > i and l.startswith('## '))
    v['C2-K6-duplicated-block'] = ('\n'.join(lines[:j] + lines[i:j] + lines[j:]) + '\n', None)
    # supplementary liveness-proof controls
    v['C2X-K1b-tokens-only-rule'] = (map_rows(cand_entry, lambda c: [c[0], ' '.join(TOKENS[c[0]]), *c[2:]]), None)
    v['C2X-K2c-value-only'] = (map_rows(cand_entry, lambda c: [c[0], c[1], 'unknown', *c[3:]]), None)
    held_keep_ex4 = map_rows(cand_entry, lambda c: to_held(c, skip=('EX4',)))
    held_keep_ex4 = held_source_line(held_keep_ex4)
    v['C2X-K4b-held-rows-usedby'] = (held_keep_ex4, used_by_edit(cand_sources))
    dup_quote = '/* hooks with multiple triggers could have duplicate matches */'

    def quote_rule_clean(c):
        q = QUOTE_RE.findall(c[3])
        if c[0] == 'EX7':
            return [c[0], dup_quote + ' ' + ' '.join(TOKENS_ALL), c[2],
                    c[3] + ' ; also hook.c:519-526 “' + dup_quote + '”', c[4]]
        return [c[0], (q[0] if q else '') + ' ' + ' '.join(TOKENS_ALL), *c[2:]]
    v['C2X-K5c-quote-rule-clean'] = (map_rows(cand_entry, quote_rule_clean), None)
    return v


def apply_patches(pristine, patches, name):
    b = pristine
    for label, old, new in patches:
        assert b.count(old) == 1, f'{name}: {label} old-string count {b.count(old)} != 1'
        b = b.replace(old, new)
    if not patches:
        return b
    assert b != pristine, f'{name}: mutant bytes identical to pristine'
    compile(b, f'{name}.py', 'exec')
    return b


def run_control_set(d, counter_bytes, tag, cand_rev, variants):
    git(d, 'checkout', '-q', '-B', 'master', cand_rev)
    if open(os.path.join(d, C2), 'rb').read() != counter_bytes:
        open(os.path.join(d, C2), 'wb').write(counter_bytes)
        mrev = commit(d, f'counter {tag}')
    else:
        mrev = cand_rev
    rows = []
    rc, rec = run_counter(d, BASE)
    rows.append(('C2-K0-do-nothing-base', rc, rec, BASE))
    for name, (text, src_text) in variants.items():
        git(d, 'checkout', '-q', mrev)
        git(d, 'checkout', '-q', '-B', 'master')
        open(os.path.join(d, ENTRY), 'w').write(text)
        if src_text is not None:
            open(os.path.join(d, SOURCES), 'w').write(src_text)
        r = commit(d, name)
        rc, rec = run_counter(d, r)
        rows.append((name, rc, rec, r))
    git(d, 'checkout', '-q', '-B', 'master', mrev)
    rc, rec = run_counter(d, cand_rev)
    rows.append(('C2-K7-candidate', rc, rec, cand_rev))
    return rows


def main():
    out = open(os.path.join(SCRATCH, 'runs.jsonl'), 'w')
    lane_counter = open(os.path.join(LANE, C2), 'rb').read()
    assert hashlib.sha256(lane_counter).hexdigest() == PRISTINE_SHA, 'lane counter hash'
    frozen_counter = subprocess.run(['git', '-C', LANE, 'show', f'{FREEZE}:{C2}'], env=GENV,
                                    capture_output=True, check=True).stdout
    assert hashlib.sha256(frozen_counter).hexdigest() == PRISTINE_SHA, 'freeze counter hash'
    assert frozen_counter == lane_counter, 'lane tree counter != freeze commit counter'
    cand = {}
    for p, (rev, want) in CAND.items():
        b = subprocess.run(['git', '-C', LANE, 'show', f'{rev}:{p}'], env=GENV,
                           capture_output=True, check=True).stdout
        assert hashlib.sha256(b).hexdigest() == want, f'candidate hash {p}'
        cand[p] = b.decode()

    d = clone(LANE, SCRATCH, 'c2', FREEZE)
    git(d, 'checkout', '-q', '-B', 'master', FREEZE)
    for p, t in cand.items():
        open(os.path.join(d, p), 'w').write(t)
    cand_rev = commit(d, 'C2 candidate')
    print('cand_rev', cand_rev, file=sys.stderr)
    variants = all_variants(cand[ENTRY], cand[SOURCES])
    print('controls:', ', '.join(variants), file=sys.stderr)

    results, shas = {}, {}
    for tag, patches in [('pristine', [])] + MUTANTS:
        counter_bytes = apply_patches(frozen_counter.decode(), patches, tag).encode()
        sha = hashlib.sha256(counter_bytes).hexdigest()
        shas[tag] = sha
        if patches:
            diff = ''.join(difflib.unified_diff(frozen_counter.decode().splitlines(True),
                                                counter_bytes.decode().splitlines(True),
                                                fromfile='check-exec-environment-r40.py', tofile=tag))
            open(os.path.join(SCRATCH, f'{tag}.diff'), 'w').write(diff)
        rows = run_control_set(d, counter_bytes, tag, cand_rev, variants)
        results[tag] = rows
        for control, rc, rec, rev in rows:
            keep = {k: rec.get(k) for k in ('rules_verified', 'source_ok', 'counts_ok',
                                            'novelty_base_hits', 'duplicate_rows', 'duplicate_headings',
                                            'result', 'error', 'raw')}
            reasons = {k: v['reasons'] for k, v in (rec.get('rules') or {}).items() if v.get('reasons')}
            out.write(json.dumps({'counter_tag': tag, 'counter_sha256': sha, 'control': control,
                                  'revision': rev, 'exit': rc, 'row_reasons': reasons, **keep}) + '\n')
        out.flush()
        print(tag, sha, 'done', file=sys.stderr)
    out.close()

    # validation: pristine must reproduce the recorded pre-data controls (frozen nine)
    ctl_path = os.path.join(LANE, '.ufo/waves/round-40/controls/controls.jsonl')
    c2ctl = {r['control']: r for r in map(json.loads, open(ctl_path)) if r['claim'] == 'C2'}
    mismatches = 0
    for control, rc, rec, rev in results['pristine']:
        if control not in c2ctl:
            continue
        ref = c2ctl[control]
        for k in ('exit', 'result', 'rules_verified', 'source_ok', 'counts_ok', 'novelty_base_hits',
                  'duplicate_rows', 'duplicate_headings'):
            if rec.get(k) != ref.get(k):
                print(f'MISMATCH {control} {k}: mine={rec.get(k)!r} recorded={ref.get(k)!r}')
                mismatches += 1
        reasons = {k: v['reasons'] for k, v in (rec.get('rules') or {}).items() if v.get('reasons')}
        if reasons != (ref.get('row_reasons') or {}):
            print(f'MISMATCH {control} row_reasons')
            mismatches += 1
    print(f'validation vs controls.jsonl: {"OK" if mismatches == 0 else f"{mismatches} MISMATCHES"}',
          file=sys.stderr)

    pristine = {c: (rc, rec) for c, rc, rec, _ in results['pristine']}
    fields = ('exit', 'result', 'rules_verified', 'source_ok', 'counts_ok', 'novelty_base_hits',
              'duplicate_rows', 'duplicate_headings')
    print('\n=== flip matrix (pristine -> mutant); F = frozen control, X = supplementary ===')
    for tag, _ in MUTANTS:
        flips, other = [], []
        for control, rc, rec, rev in results[tag]:
            prc, prec = pristine[control]
            grp = 'F' if control in c2ctl else 'X'
            if prc == 1 and prec.get('result') == 'FAIL' and rc == 0 and rec.get('result') == 'PASS':
                flips.append(f'{grp}:{control}')
            elif (prc, prec.get('result')) != (rc, rec.get('result')):
                other.append(f'{grp}:{control}: {prc}/{prec.get("result")} -> {rc}/{rec.get("result")}')
        print(f'{tag}: flips={flips or "NONE"} other_verdict_changes={other or "none"}')
    # lane untouched check (restoration evidence)
    assert hashlib.sha256(open(os.path.join(LANE, C2), 'rb').read()).hexdigest() == PRISTINE_SHA
    print('lane counter unchanged:', PRISTINE_SHA, file=sys.stderr)


if __name__ == '__main__':
    main()
