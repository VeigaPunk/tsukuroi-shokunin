#!/usr/bin/env python3
"""R49MutAdj: mutation probes for tools/check-adjacency-table-r49.py (frozen bytes)."""
import hashlib
import json
import os
import re
import subprocess
import sys

S = '/fast/scratch/hyaku/tsukuroi-r49/R49MutAdj'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '32a855608aa3ebb19b0602a94cc33bcfda564a61'
FREEZE = '55c07cd3f8bff2e12117c34d57b4c618de74d85c'
PRISTINE = os.path.join(S, 'counter-frozen.py')
PROV = open(os.path.join(S, 'PROVINCE.frozen.md'), encoding='utf-8').read()
BASE_PROV_PATH = os.path.join(S, 'prov-base.md')


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def fixture(name, text):
    p = os.path.join(S, f'{name}.md')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(text)
    return p


def run(script, provfile, rev=REV):
    p = subprocess.run([sys.executable, script, '--lane', LANE, '--revision', rev,
                        '--province-file', provfile],
                       capture_output=True, text=True, cwd=S, stdin=subprocess.DEVNULL,
                       env={**os.environ, 'TMPDIR': S})
    try:
        d = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:
        d = {'unparsable': p.stdout, 'stderr': p.stderr}
    d['_rc'] = p.returncode
    return d


KEYS = ('verdict', 'adj_rows', 'linked_rows', 'bare_ranges', 'anchors_ok', 'registry_ok',
        'anchors_checker_rc')


def brief(d):
    return {k: d.get(k) for k in KEYS}


# ---------------------------------------------------------------- fixtures
prov = PROV
# F1: one bare sibling range added to ADJ-01's ownership cell
f1 = prov.replace('| `OUT-002` |', '| `OUT-002`, `../mori-shokunin/PROVINCE.md:10-20` |', 1)
assert f1 != prov and 'PROVINCE.md:10-20' in f1
# F2: ADJ-01 and ADJ-02 point at each other's anchor (wrong ADJ class)
f2 = prov.replace('| `OUT-002` |', '| `@@A@@` |', 1).replace('| `OUT-003` |', '| `@@B@@` |', 1)
f2 = f2.replace('| `@@A@@` |', '| `OUT-003` |', 1).replace('| `@@B@@` |', '| `OUT-002` |', 1)
assert f2.count('`OUT-003`') == 1 and '| `OUT-003` |' in f2
# F3: OUT-002 anchor quote grown to 26 words (still one cell, no pipe)
long_quote = ('GET /v1/models versus the alias flag versus the configured model id and its '
              'served identity resolution order in the running endpoint today under the '
              'current serving configuration')
assert len(long_quote.split()) > 25, len(long_quote.split())
f3 = prov.replace('`GET /v1/models` vs `--alias` vs the configured model id', long_quote, 1)
assert f3 != prov
# F4: a valid OUT-011 anchor row that the registry does not carry, named by ADJ-01
out002_row = next(ln for ln in prov.split('\n') if ln.startswith('| OUT-002 |'))
out011_row = out002_row.replace('| OUT-002 |', '| OUT-011 |', 1)
assert out011_row != out002_row
f4 = prov.replace(out002_row, out002_row + '\n' + out011_row, 1)
f4 = f4.replace('| `OUT-002` |', '| `OUT-002`, `OUT-011` |', 1)
assert '`OUT-011` |' in f4

FIX = {
    'F1-bare-range': fixture('F1-bare-range', f1),
    'F2-wrong-class': fixture('F2-wrong-class', f2),
    'F3-long-quote': fixture('F3-long-quote', f3),
    'F4-registry-missing': fixture('F4-registry-missing', f4),
}

# ---------------------------------------------------------------- controls K0..K3 (battery c2 construction)
base_prov = subprocess.run(['git', '-C', LANE, 'show', '6256760d1382ce4ce20fcba830d4b2912cfbf12b:PROVINCE.md'],
                           capture_output=True, text=True).stdout
open(BASE_PROV_PATH, 'w', encoding='utf-8').write(base_prov)
k1 = base_prov
for rid, outs in (('ADJ-01', 'OUT-002'), ('ADJ-02', 'OUT-003'), ('ADJ-03', 'OUT-004'),
                  ('ADJ-04', 'OUT-005'), ('ADJ-05', 'OUT-006, OUT-007'),
                  ('ADJ-06', 'OUT-008, OUT-009'), ('ADJ-07', 'OUT-010')):
    k1 = re.sub(r'(\| ' + rid + r' \|.*?)\| (`\.\./[^|]+?`) \|', r'\1| \2, `' + outs + r'` |', k1)
assert k1 != base_prov
k3 = prov
for rid in ('ADJ-02', 'ADJ-03', 'ADJ-04', 'ADJ-05', 'ADJ-06', 'ADJ-07'):
    k3 = re.sub(r'(\| ' + rid + r' \|.*)\| `OUT-0\d\d`(, `OUT-0\d\d`)? \|', r'\1| `OUT-001` |', k3)
assert k3 != prov
CTRL = {
    'K0-base': BASE_PROV_PATH,
    'K1-ranges-kept': fixture('K1-ranges-kept', k1),
    'K2-OUT-099': fixture('K2-OUT-099', prov.replace('`OUT-003`', '`OUT-099`', 1)),
    'K3-all-OUT-001': fixture('K3-all-OUT-001', k3),
    'Kpass-freeze': fixture('Kpass-freeze', prov),
}

# ---------------------------------------------------------------- mutants
SRC = open(PRISTINE, encoding='utf-8').read()
MUTS = {}

m1_old = "        bare += len(row_bare)\n"
assert SRC.count(m1_old) == 1
MUTS['M1-bare-leg-removed'] = SRC.replace(m1_old, '')

m2_old = ("            if anc[1] != row_id:\n"
          "                row_problems.append(f'{out} points at {anc[1]!r}, not {row_id}')\n"
          "                a_ok = False\n")
assert SRC.count(m2_old) == 1
MUTS['M2-class-equality-removed'] = SRC.replace(m2_old, '')

m3_old = "            if not quote or len(quote.split()) > 25:\n"
m3_new = "            if not quote:\n"
assert SRC.count(m3_old) == 1
MUTS['M3-quote-wordcount-removed'] = SRC.replace(m3_old, m3_new)

m4_old = ("            rr = registry.get(out)\n"
          "            if rr is None:\n"
          "                row_problems.append(f'{out} absent from {REGISTRY}')\n"
          "                r_ok = False\n"
          "                continue\n"
          "            if not HEX64.fullmatch(str(rr.get('sibling_blob_sha256', ''))):\n"
          "                row_problems.append(f'{out} registry blob sha256 invalid')\n"
          "                r_ok = False\n"
          "            if not HEX12.fullmatch(str(rr.get('sibling_commit', ''))):\n"
          "                row_problems.append(f'{out} registry commit invalid')\n"
          "                r_ok = False\n")
assert SRC.count(m4_old) == 1
MUTS['M4-registry-leg-removed'] = SRC.replace(m4_old, '')

paths = {}
for name, text in MUTS.items():
    p = os.path.join(S, name + '.py')
    open(p, 'w', encoding='utf-8').write(text)
    subprocess.run(['python3', '-c', 'import py_compile,sys;py_compile.compile(sys.argv[1],doraise=True)', p],
                   check=True)
    paths[name] = p

out = {'revision': REV, 'freeze': FREEZE,
       'pristine_sha256': sha(PRISTINE),
       'mutant_sha256': {k: sha(v) for k, v in paths.items()},
       'fixture_sha256': {k: sha(v) for k, v in FIX.items()},
       'probes': [], 'controls': []}

ORDER = [('F1-bare-range', 'M1-bare-leg-removed'), ('F2-wrong-class', 'M2-class-equality-removed'),
         ('F3-long-quote', 'M3-quote-wordcount-removed'),
         ('F4-registry-missing', 'M4-registry-leg-removed')]
for fx, mut in ORDER:
    pr = run(PRISTINE, FIX[fx])
    mu = run(paths[mut], FIX[fx])
    out['probes'].append({'fixture': fx, 'mutant': mut,
                          'pristine': brief(pr), 'pristine_rc': pr['_rc'],
                          'mutant': brief(mu), 'mutant_rc': mu['_rc'],
                          'verdict': ('killed' if pr['_rc'] == 1 and mu['_rc'] == 0 else
                                      'survived' if pr['_rc'] == 1 else 'inconclusive')})

for name, p in CTRL.items():
    r = run(PRISTINE, p)                        # no --skip-anchors-check
    out['controls'].append({'control': name, 'with_checker': brief(r), 'rc_with_checker': r['_rc']})

# pristine baseline and the live freeze-revision measurement
out['baseline'] = brief(run(PRISTINE, CTRL['Kpass-freeze']))
freeze_run = run(PRISTINE, CTRL['Kpass-freeze'], rev=FREEZE)
out['freeze_revision_run'] = {'brief': brief(freeze_run), 'rc': freeze_run['_rc'],
                              'problems': freeze_run.get('problems')}
print(json.dumps(out, indent=1, sort_keys=True))
