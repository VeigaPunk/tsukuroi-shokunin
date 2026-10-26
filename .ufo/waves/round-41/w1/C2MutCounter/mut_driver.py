#!/usr/bin/env python3
"""C2-19 mutation tester for tools/check-package-anatomy-r41.py (seat C2MutCounter).

For each mutant: build the SAME fixture clones run_controls.py builds (shared clone of the lane at the
freeze revision, origin removed, toplevel checked, variant files + the MUTATED counter committed on
master with the fixture identity), then run the mutated counter copy with --repo <clone> --revision <sha>.
Receipts: one JSON per run in the seat receipt dir, carrying the frozen before-record from
controls-c2.jsonl next to the after-record. Scratch under --scratch, removed by the caller.
"""
import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
# Freeze revision for fixture clones: e479fdc5 = "freeze C1/C2 counters, pinned sources, host capture,
# registry rows" — the entry does not exist there (matches the frozen K0 do-nothing receipt); frozen
# snapshots are tracked. The lane tip 71851d63 is kept as a cross-check freeze via --freeze.
FREEZE = 'e479fdc54d0977ccd8112a42d8d139baaebcb02e'
COUNTER = 'tools/check-package-anatomy-r41.py'
SEAT_RECEIPTS = LANE / '.ufo/waves/round-41/w1/C2MutCounter'

_spec = importlib.util.spec_from_file_location('rc', LANE / '.ufo/waves/round-41/controls/run_controls.py')
rc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rc)
_spec2 = importlib.util.spec_from_file_location('c2mod', LANE / 'tools/check-package-anatomy-r41.py')
c2 = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(c2)

PRISTINE = (LANE / COUNTER).read_text()
ENTRY = rc.ENTRY

BEFORE = {}
for line in (LANE / '.ufo/waves/round-41/controls/controls-c2.jsonl').read_text().splitlines():
    if line.strip():
        rec = json.loads(line)
        BEFORE[rec['control']] = rec


def patch(old, new):
    def apply(t):
        assert t.count(old) == 1, f'patch site not unique: {old[:60]!r} count={t.count(old)}'
        return t.replace(old, new)
    return apply


VOK = "    verdicts_ok = sum(1 for k in REQUIRED if vd[k]['holds'] and not vd[k]['fails'])\n"

MUTANTS = {
    # M1a: drop the window check (cited range must lie inside the frozen window); quote-at-cited-lines kept
    'M1a-window-containment': patch(
        "            for fname, lo, hi in refs:\n"
        "                if not (wlo <= lo <= hi <= whi):\n"
        "                    r['reasons'].append(f'cited range {fname}:{lo}-{hi} outside window {wlo}-{whi}')\n"
        "                    continue\n"
        "                body = collapse(' '.join(srcl[want][lo - 1:hi]))\n",
        "            for fname, lo, hi in refs:\n"
        "                body = collapse(' '.join(srcl[want][lo - 1:hi]))\n"),
    # M1b: drop the whole window block (containment AND quote-at-cited-lines lookup)
    'M1b-window-block': patch(
        "            for fname, lo, hi in refs:\n"
        "                if not (wlo <= lo <= hi <= whi):\n"
        "                    r['reasons'].append(f'cited range {fname}:{lo}-{hi} outside window {wlo}-{whi}')\n"
        "                    continue\n"
        "                body = collapse(' '.join(srcl[want][lo - 1:hi]))\n"
        "                for qt in QUOTE_RE.findall(src_cell):\n"
        "                    qc = collapse(qt)\n"
        "                    if 4 <= len(qc.split()) <= 25 and qc in body:\n"
        "                        quote_ok = True\n"
        "                        copied = copied or qc in rc\n",
        ""),
    # M2: drop RELATIONS (the per-row relation loop)
    'M2-relations': patch(
        "            for rel in RELATIONS[pa]:\n"
        "                if not re.search(rel, rc):\n"
        "                    r['reasons'].append(f'relation unmet: {rel}')\n"
        "            neg = NEG.search(rc)\n",
        "            neg = NEG.search(rc)\n"),
    # M3: accept `partly` as holds
    'M3-partly-as-holds': patch(
        VOK,
        "    verdicts_ok = sum(1 for k in REQUIRED if (vd[k]['holds'] or vd[k]['partly']) and not vd[k]['fails'])\n"),
    # M4: ignore `fails`
    'M4-ignore-fails': patch(
        VOK,
        "    verdicts_ok = sum(1 for k in REQUIRED if vd[k]['holds'])\n"),
    # M5a: drop the host_ok check for PA4 (predicate still demands 6)
    'M5a-host-pa4-dropped': patch(
        "            if pa in hexp:\n",
        "            if pa in hexp and pa != 'PA4':\n"),
    # M5b: the weakening a rational cheater writes: PA4 unchecked AND predicate relaxed to 5
    'M5b-host-pa4-dropped-pred5': lambda t: patch(
        "    ok = (verified == 8 and verdicts_ok == 8 and host_ok == 6 and source_ok == 1 and dup_rows == 0\n"
        "          and dup_heads == 0 and nov_total == 0)\n",
        "    ok = (verified == 8 and verdicts_ok == 8 and host_ok == 5 and source_ok == 1 and dup_rows == 0\n"
        "          and dup_heads == 0 and nov_total == 0)\n")(patch(
        "            if pa in hexp:\n",
        "            if pa in hexp and pa != 'PA4':\n")(t)),
    # M6: a verdict file counts for any row (row attribution dropped)
    'M6-verdict-any-row': patch(
        "            out[m.group(1)][vm.group(1)].append(f'{d}/{name}')\n",
        "            for row in out:\n"
        "                out[row][vm.group(1)].append(f'{d}/{name}')\n"),
}

ALL = ['C2-K0-do-nothing', 'C2-K1-r40-token-writer', 'C2-K2-relation-literal-writer-no-verdicts',
       'C2-K3-x-false-swap', 'C2-K4-x-false-negation', 'C2-K5-candidate-one-fails-verdict',
       'C2-K6-candidate-no-verdicts', 'C2-K7-candidate-one-partly-only', 'C2-K8-candidate']


def variant_files(control):
    cand_entry = (LANE / ENTRY).read_text()
    cand_sources = (LANE / 'corpus/SOURCES.md').read_text()
    base_files = {ENTRY: cand_entry, 'corpus/SOURCES.md': cand_sources}
    c2v = {
        'C2-K0-do-nothing': {},
        'C2-K1-r40-token-writer': {**base_files, ENTRY: rc.writer_r40(cand_entry, c2), **rc.verdict_files({})},
        'C2-K2-relation-literal-writer-no-verdicts': {**base_files, ENTRY: rc.writer_relations(cand_entry, c2)},
        'C2-K3-x-false-swap': {**base_files, ENTRY: rc.swap(cand_entry), **rc.verdict_files({})},
        'C2-K4-x-false-negation': {**base_files, ENTRY: rc.negate(cand_entry), **rc.verdict_files({})},
        'C2-K5-candidate-one-fails-verdict': {**base_files, **rc.verdict_files({4: 'fails'})},
        'C2-K6-candidate-no-verdicts': dict(base_files),
        'C2-K7-candidate-one-partly-only': {**base_files, **rc.verdict_files({7: 'partly'})},
        'C2-K8-candidate': {**base_files, **rc.verdict_files({})},
        # seat probes (not L1 controls): demonstrate a mutant is behavior-bearing outside the suite
        'PROBE-holds-and-fails-PA4': {**base_files, **rc.verdict_files({}),
                                      '.ufo/waves/round-41/w1/C2RevPA4b.md':
                                          'VERDICT: fails\nrow PA4; probe second reviewer verdict\n'},
        'PROBE-out-of-window-cite': {**base_files,
                                     ENTRY: probe_out_of_window(cand_entry),
                                     **rc.verdict_files({})},
    }
    return c2v[control]


def probe_out_of_window(cand_entry):
    """Candidate entry with ONLY PA1's citation swapped to the r40 trick (line 1, outside window 95-124);
    rule cell and every other row untouched, so all RELATIONS still hold."""
    out = []
    for l in rc.rows(cand_entry):
        c = rc.cells(l)
        if c[0] == 'PA1':
            f = c2.REQUIRED['PA1'][0]
            k, q = rc.first_line_quote((c2.SRC_DIR / f).read_text(errors='replace'))
            sid = re.search(r'S\d{3,}', c[3]).group(0)
            c[3] = f'{sid} {f}:{k}-{k} “{q}”'
        out.append(rc.mk(c))
    return rc.set_rows(cand_entry, out)


def run_one(mutant, control, scratch_work):
    counter_text = PRISTINE if mutant == 'pristine' else MUTANTS[mutant](PRISTINE)
    files = {**variant_files(control), COUNTER: counter_text}
    d, rev = rc.fixture(LANE, FREEZE, scratch_work, f'{mutant}.{control}', files)
    try:
        cmd = ['python3', str(d / COUNTER), '--repo', str(d), '--revision', rev]
        p = subprocess.run(cmd, env=rc.ENV, capture_output=True, text=True, timeout=7200)
        try:
            after = json.loads(p.stdout)
        except ValueError:
            after = {'parse_error': p.stdout[-400:], 'stderr': p.stderr[-400:]}
        after['exit'] = p.returncode
    finally:
        shutil.rmtree(d, ignore_errors=True)
    before = BEFORE.get(control)
    has_before = before is not None
    keep = ('rules_verified', 'verdicts_ok', 'host_ok', 'source_ok', 'duplicate_rows',
            'duplicate_headings', 'novelty_base_hits', 'result', 'exit', 'error')
    receipt = {'mutant': mutant, 'control': control, 'fixture_revision': rev,
               'before': ({k: before[k] for k in keep} if has_before else None),
               'after': {k: after.get(k) for k in keep},
               'after_row_reasons': {k: v['reasons'][:4] for k, v in (after.get('rules') or {}).items() if v.get('reasons')},
               'flip': (has_before and ((before.get('result') != after.get('result'))
                                        or (before.get('exit') != after.get('exit'))))}
    out = SEAT_RECEIPTS / f'{mutant}__{control}__{FREEZE[:7]}.json'
    out.write_text(json.dumps(receipt, indent=1) + '\n')
    print(json.dumps({'mutant': mutant, 'control': control,
                      'before_result': before.get('result') if has_before else None,
                      'after_result': after.get('result'), 'after_exit': after.get('exit'),
                      'rules_verified': after.get('rules_verified'), 'verdicts_ok': after.get('verdicts_ok'),
                      'host_ok': after.get('host_ok'), 'error': after.get('error'),
                      'flip': receipt['flip']}), flush=True)
    return receipt


def main():
    global FREEZE
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', required=True)
    ap.add_argument('--controls', nargs='+', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--freeze', default=FREEZE)
    a = ap.parse_args()
    FREEZE = a.freeze
    Path(a.scratch).mkdir(parents=True, exist_ok=True)
    for control in a.controls:
        run_one(a.mutant, control, Path(a.scratch))


if __name__ == '__main__':
    main()
