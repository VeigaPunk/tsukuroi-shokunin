#!/usr/bin/env python3
"""Mutate the C1 counter one rule at a time and score every fixture under baseline and mutant.

A mutant that leaves every fixture's new_sourced count unchanged is a survivor.
"""
import hashlib
import json
import os
import re
import subprocess

LANE = '/fast/scratch/hyaku/tsukuroi-r31/MutCounterC1'
CTL = '/fast/scratch/hyaku/tsukuroi-r31/ctl/c1-controls'
REPO = f'{LANE}/repo'
CONTR = f'{LANE}/work/c1-controls'
FIXT = f'{LANE}/work/c1-fixture'
OUT = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/MutCounterC1'

FIXTURES = [
    ('K0-base', '2077e2fa4fa70ea79aa77b6d91f4acd35bc54897', REPO),
    ('K1-sealed-forged', 'bf2c014aff4dad845e66c3f322dfd4617ee2d896', CTL),
    ('K2-restate-r30', '1558cedc14349b2bd196cf37706f552a9644e25a', CONTR),
    ('K3-junk-real', '9f4a219ac313c17ff5c5f077398c77acf84d9857', CONTR),
    ('K4-quote-copy', '9d17d2c2d152b2b590d1dab9003f24f7c2bb8a64', CONTR),
    ('K5-sealed-positive', '92cdff13496762c89e1baa2681b8baccb1cf8ed3', CTL),
    ('P1-my-positive', '5175b34c16452cba25f99840f92268d5bff9b5b2', FIXT),
    ('N-R1dup', '2f6267898118366c1276a956f3213bd7e1025f96', FIXT),
    ('N-R1extra', '9da5b96582b4f2e256a6eb3e104c49354a6edd3e', FIXT),
    ('N-R2', '613fb42ac8ad392a4b92c0d6b19a65cb6b8e4e02', FIXT),
    ('N-R3sha', '0d5e86a321baacbc5dcfde5585a2e8dd79527ffd', FIXT),
    ('N-R3path', '9e0904dd5678bf86821b92d0ce1370838b5458a7', FIXT),
    ('N-R4line', 'ff0c3a525209dfc47c9aec1d03ffeb14663d2560', FIXT),
    ('N-R4words', '618dfda5b472c07b44fe93be2c7ab75f14d1c112', FIXT),
    ('N-R5status', '6c14033fc15a4c0ed8b8bff70be3b0e7858ab114', FIXT),
    ('N-R5count', 'e92c1eac684d0ca18538c5925fb50af12979dbf0', FIXT),
    ('N-R5base', '45f2425acfc34b430fafda42a0245c601e21127c', FIXT),
    ('N-R6skill', 'cc1963003e32f9d10b2d8a480388c514202f971c', FIXT),
    ('N-R6fence', 'a5f0307ce20ddea6770cb02d433da9db3bc99c5b', FIXT),
    ('N-R6comment', 'fc57db2f4aca9d94fb9dcf9a569c744d06152037', FIXT),
    ('N-R7key', '0c054acce6f35d4f16b43fdbaeb7d10d2a4f3f34', FIXT),
    ('N-R7run6', 'c70b7c5da868865f1397a78812af44beb1304618', FIXT),
    ('N-R7run5', '838d7d72df9bacc3b06d32ceead865097bc423c2', FIXT),
    ('N-pinprefix', '486cba9741f18a036f038d4315880957b8969f46', FIXT),
]

R1_ROWS = """        rs = rows.get(qid, [])
        if len(rs) != 1:
            fail.append(f'R1 {len(rs)} rows for {qid}')
        else:"""
R1_ROWS_NEW = """        rs = rows.get(qid, [])
        if not rs:
            fail.append('R1 entry absent')
        else:"""

EXTRA_IDS = """            extra = sorted(set(rows) - set(QUESTIONS))
            if extra:
                file_fail.append('R1 extra ids ' + ','.join(extra))
"""
R2 = """            if set(r) != ROW_KEYS:
                fail.append('R2 keys ' + ','.join(sorted(set(r) ^ ROW_KEYS)))
"""
R3 = """            if not snap.startswith('.ufo/waves/round-31/') or '..' in snap.split('/'):
                fail.append('R3 snapshot outside .ufo/waves/round-31/')
            else:
                data = show(lane, rev, snap)
                if data is None:
                    fail.append('R3 snapshot absent at revision')
                elif hashlib.sha256(data).hexdigest() != q['pin']:
                    fail.append('R3 snapshot sha256 differs from pin')
                    data = None
"""
R3_NEW = """            data = show(lane, rev, snap)
            if data is None:
                fail.append('R3 snapshot absent at revision')
"""
PIN = """                elif hashlib.sha256(data).hexdigest() != q['pin']:
                    fail.append('R3 snapshot sha256 differs from pin')
                    data = None
"""
PIN_NEW = """                elif hashlib.sha256(data).hexdigest()[:4] != q['pin'][:4]:
                    fail.append('R3 snapshot sha256 differs from pin')
                    data = None
"""
R4 = """            nq = len(quote.split())
            if not (6 <= nq <= 25):
                fail.append(f'R4 quote has {nq} words')
            if not isinstance(line, int) or isinstance(line, bool) or line < 1:
                fail.append('R4 line is not a positive int')
            elif data is not None:
                lines = data.decode('utf-8', 'replace').splitlines()
                if line > len(lines) or not quote.strip() or quote.strip() not in lines[line - 1]:
                    fail.append('R4 quote not at cited line')
"""
R5 = """            if not re.fullmatch(r'S\\d{3}', src):
                fail.append('R5 source id malformed')
            else:
                if registry_rows(reg_base, src):
                    fail.append('R5 source row exists at base')
                rr = registry_rows(reg_rev, src)
                if len(rr) != 1:
                    fail.append(f'R5 {len(rr)} registry rows for {src}')
                else:
                    cells = status_cell(rr[0])
                    if 'mined' not in cells:
                        fail.append('R5 status cell is not mined')
                    if (URL + q['file']) not in rr[0] or q['pin'] not in rr[0]:
                        fail.append('R5 registry row lacks frozen URL or sha256')
"""
BASEREG = """                if registry_rows(reg_base, src):
                    fail.append('R5 source row exists at base')
"""
R6 = """            sl = skill_lines(skill, qid)
            if len(sl) != 1:
                fail.append(f'R6 {len(sl)} SKILL.md lines for {qid}')
            elif not has_token(sl[0], q['tokens']):
                fail.append('R6 SKILL.md line lacks a novelty token')
            if not has_token(quote, q['tokens']):
                fail.append('R6 quote lacks a novelty token')
            if not has_token(st, q['tokens']):
                fail.append('R6 statement lacks a novelty token')
"""
R7 = """            if len(st.split()) < 12:
                fail.append('R7 statement under 12 words')
            cands = set(words(st))
            cands |= {p for w in list(cands) for p in re.split(r'[-/.]', w) if p}
            digests = {hashlib.sha256((SALT + ' ' + w).encode()).hexdigest()[:16] for w in cands}
            for n, group in enumerate(KEYHASH[qid], 1):
                if not digests.intersection(group):
                    fail.append(f'R7 sealed answer-key group {n} missing')
            if shares_run(st, quote):
                fail.append('R7 statement shares a 6-word run with the quote')
"""
R8 = """        for tok in q['tokens']:
            if hits[tok]:
                fail.append(f'R8 token {tok!r} has {hits[tok]} hits at base')
"""
SKILL_FN = """def skill_lines(text, rid):
    out, fence, comment = [], False, False
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith('```') or s.startswith('~~~'):
            fence = not fence
            continue
        if comment:
            if '-->' in ln:
                comment = False
            continue
        if '<!--' in ln and '-->' not in ln.split('<!--', 1)[1]:
            comment = True
            continue
        if not fence and ln.startswith(f'| [R31-{rid}] '):
            out.append(ln)
    return out
"""
SKILL_FN_NEW = """def skill_lines(text, rid):
    out = []
    for ln in text.splitlines():
        if ln.startswith(f'| [R31-{rid}] '):
            out.append(ln)
    return out
"""

MUTANTS = {
    'M01-drop-R1': [(R1_ROWS, R1_ROWS_NEW), (EXTRA_IDS, '')],
    'M02-drop-R2': [(R2, '')],
    'M03-drop-R3': [(R3, R3_NEW)],
    'M03b-weaken-pin': [(PIN, PIN_NEW)],
    'M04-drop-R4': [(R4, '')],
    'M05-drop-R5': [(R5, '')],
    'M05b-weaken-base-registry': [(BASEREG, '')],
    'M06-drop-R6': [(R6, '')],
    'M07-drop-R7': [(R7, '')],
    'M08-drop-R8': [(R8, '')],
    'M09-window-7': [('if shares_run(st, quote):', 'if shares_run(st, quote, 7):')],
    'M10-window-5': [('if shares_run(st, quote):', 'if shares_run(st, quote, 5):')],
    'M11-drop-fence-comment-skip': [(SKILL_FN, SKILL_FN_NEW)],
}


def clean_env():
    e = {k: v for k, v in os.environ.items()
         if not (k.startswith('GIT_') or k.startswith('LD_') or k.startswith('PYTHON'))}
    e.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
              'GIT_CONFIG_SYSTEM': os.devnull, 'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'})
    return e


def run(counter, rev, lane):
    p = subprocess.run(['python3', counter, '--revision', rev, '--lane', lane],
                       capture_output=True, env=clean_env())
    out, score, fails = p.stdout.decode(), None, {}
    for ln in out.splitlines():
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        if 'predicate' in d:
            score = d['new_sourced']
        elif 'id' in d:
            fails[d['id']] = d['fail']
    return p.returncode, score, fails


def main():
    src = open(f'{REPO}/tools/check-btrfs-repair-r31.py', encoding='utf-8').read()
    base_sha = hashlib.sha256(src.encode()).hexdigest()
    results = {'baseline_sha256': base_sha, 'mutants': {}, 'fixtures': [f[0] for f in FIXTURES]}
    rc, score, fails = run(f'{REPO}/tools/check-btrfs-repair-r31.py', FIXTURES[0][1], FIXTURES[0][2])
    base = {}
    for name, rev, lane in FIXTURES:
        rc, sc, fl = run(f'{REPO}/tools/check-btrfs-repair-r31.py', rev, lane)
        base[name] = {'score': sc, 'exit': rc, 'fails': fl}
    results['baseline'] = base
    os.makedirs(f'{OUT}/mutants', exist_ok=True)
    for mname, edits in MUTANTS.items():
        text = src
        for old, new in edits:
            if old not in text:
                raise SystemExit(f'{mname}: pattern absent: {old[:60]!r}')
            text = text.replace(old, new, 1)
        d = f'{OUT}/mutants/{mname}'
        os.makedirs(d, exist_ok=True)
        path = f'{d}/check-btrfs-repair-r31.py'
        open(path, 'w', encoding='utf-8').write(text)
        with open(f'{d}/mutant.diff', 'w') as fh:
            subprocess.run(['diff', '-u',
                            '--label', 'a/tools/check-btrfs-repair-r31.py',
                            '--label', 'b/tools/check-btrfs-repair-r31.py',
                            f'{REPO}/tools/check-btrfs-repair-r31.py', path],
                           stdout=fh)
        changed = {}
        for name, rev, lane in FIXTURES:
            rc, sc, fl = run(path, rev, lane)
            delta = sc - base[name]['score']
            if delta:
                changed[name] = {'baseline': base[name]['score'], 'mutant': sc, 'delta': delta,
                                 'mutant_fails': fl}
        results['mutants'][mname] = {'sha256': hashlib.sha256(text.encode()).hexdigest(),
                                     'changed': changed, 'killed': bool(changed)}
    json.dump(results, open(f'{OUT}/mutant-results.json', 'w'), indent=1)

    lines = ['| mutant | killed | fixture (baseline -> mutant) |', '|---|---|---|']
    for mname, r in results['mutants'].items():
        if r['killed']:
            det = ', '.join(f"{k} ({v['baseline']}->{v['mutant']})" for k, v in r['changed'].items())
            lines.append(f'| {mname} | yes | {det} |')
        else:
            lines.append(f'| {mname} | **SURVIVOR** | none |')
    open(f'{OUT}/mutant-table.md', 'w').write('\n'.join(lines) + '\n')

    bl = ['| fixture | baseline score |', '|---|---|']
    for name in results['fixtures']:
        bl.append(f'| {name} | {base[name]["score"]} |')
    open(f'{OUT}/baseline-table.md', 'w').write('\n'.join(bl) + '\n')
    print('\n'.join(lines))
    print('\n'.join(bl))


if __name__ == '__main__':
    main()
