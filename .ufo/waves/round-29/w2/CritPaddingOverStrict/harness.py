#!/usr/bin/env python3
"""CritPaddingOverStrict: commit register/PROVINCE variants in the sandbox clone and run the tip counter."""
import copy
import json
import os
import subprocess
import sys

CLONE = '/fast/scratch/hyaku/tsukuroi-r29/CritPaddingOverStrict/repo'
BASE = '10d5288fc1051364e711203855e7c53710dfcc21'
REG = 'corpus/knowledge/adjacency-mori-oom-r27.json'
ENV = dict({k: v for k, v in os.environ.items() if not k.startswith('GIT_')},
           GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)


def git(*a, inp=None):
    r = subprocess.run(['git', '-C', CLONE] + list(a), capture_output=True, env=ENV, input=inp)
    if r.returncode:
        raise SystemExit('git %s: %s' % (a, r.stderr.decode()))
    return r.stdout.decode()


def base_text(path):
    return git('show', '%s:%s' % (BASE, path))


BASE_REG = json.loads(base_text(REG))
BASE_PROV = base_text('PROVINCE.md')
R = {r['id']: i for i, r in enumerate(BASE_REG['rows'])}


def commit(name, reg=None, prov=None, extra=None):
    git('checkout', '-q', '-f', '--detach', BASE)
    files = dict(extra or {})
    if reg is not None:
        files[REG] = json.dumps(reg, indent=1, ensure_ascii=False) + '\n'
    if prov is not None:
        files['PROVINCE.md'] = prov
    for p, t in files.items():
        with open(os.path.join(CLONE, p), 'w', encoding='utf-8') as fh:
            fh.write(t)
    git('add', '-A')
    git('-c', 'user.name=crit', '-c', 'user.email=crit@sandbox', 'commit', '-q', '--allow-empty', '-m', name)
    sha = git('rev-parse', 'HEAD').strip()
    git('checkout', '-q', '-f', '--detach', BASE)
    return sha


def run(sha):
    r = subprocess.run([sys.executable, os.path.join(CLONE, 'tools/check-adjacency-overlap.py'),
                        '--revision', sha, '--repo', CLONE], capture_output=True, env=ENV)
    out = json.loads(r.stdout.decode())
    return r.returncode, out['anchored_rows'], {k: v for k, v in out['rows'].items() if v}, out['shape_errors'], out['sibling_check']


def reg_with(fn):
    reg = copy.deepcopy(BASE_REG)
    fn(reg, lambda rid: reg['rows'][R[rid]])
    return reg


def prov_sub(old, new, text=None):
    text = BASE_PROV if text is None else text
    assert text.count(old) == 1, old
    return text.replace(old, new)


ROW = {rid: next(l for l in BASE_PROV.splitlines() if l.startswith('| %s |' % rid)) for rid in R}
TABLE_HDR = '| id | owner | class | pointer |\n|---|---|---|---|\n'

V = []  # (kind, name, note, reg, prov)


def sp(name, note, reg=None, prov=None):
    V.append(('should-pass', name, note, reg, prov))


def sf(name, note, reg=None, prov=None):
    V.append(('should-fail', name, note, reg, prov))


# ---------------------------------------------------------------- should-pass
sp('control', 'tip bytes unchanged (fresh commit)', reg_with(lambda g, r: None))
sp('p-b13-h3-notes-after-table',
   'a ### subsection after the table, as PROVINCE.md:54 does under its other Adjacent section',
   prov=BASE_PROV.rstrip('\n') + '\n\n### Round 29 follow-up\n\nOV4 was reported to mori on 2026-10-22; no reply yet.\n')
sp('p-b13-h4-under-section',
   'a #### note heading after the table',
   prov=BASE_PROV.rstrip('\n') + '\n\n#### Note\n\nRows are reported, never absorbed.\n')
sp('p-b13-indented-heading-quote-elsewhere',
   'the section heading quoted in an indented code block in the Frontier section (CommonMark: code, not a heading)',
   prov=prov_sub('## Frontier\n', '## Frontier\n\n    ## Adjacent — mori userspace OOM killers (round 27)\n\n'))
sp('p-b13-indented-h3-in-section',
   'an indented code line "    ### example" inside the section (code, not a heading)',
   prov=prov_sub(ROW['OV6'] + '\n', ROW['OV6'] + '\n\nExample of a nested heading the counter refuses:\n\n    ### example\n'))
sp('p-b13-inline-code-comment-opener',
   'OV3 pointer cell mentions `<!--` in inline code (renders as text)',
   prov=prov_sub(ROW['OV3'], ROW['OV3'][:-2] + '; `<!--` blocks are not rows |'))
sp('p-b13-single-dash-delimiter',
   'GFM delimiter row |-|-|-|-| (one hyphen per cell)',
   prov=prov_sub(TABLE_HDR, TABLE_HDR.replace('|---|---|---|---|', '|-|-|-|-|')))
sp('p-b13-two-dash-aligned-delimiter',
   'GFM delimiter row | :-- | :-: | --: | -- |',
   prov=prov_sub(TABLE_HDR, TABLE_HDR.replace('|---|---|---|---|', '| :-- | :-: | --: | -- |')))
sp('p-b13-pipeless-rows',
   'GFM table rows without leading/trailing pipes',
   prov=prov_sub(ROW['OV3'], ROW['OV3'].strip('| ').strip()))
sp('p-b7-bold-id',
   'OV1 id cell bold (**OV1**); owner/class bold is already accepted',
   prov=prov_sub('| OV1 |', '| **OV1** |'))
sp('p-b15-conflicts-does-not-agree',
   'OV4 CONFLICTS pointer: "mori F8 does not agree with the lane\'s OOMRules= qualifier ..."',
   prov=prov_sub(ROW['OV4'], "| OV4 | tsukuroi | CONFLICTS | mori F8 does not agree with the lane's OOMRules= qualifier (lane lines 387-390); reported to mori |"))
sp('p-b15-conflicts-mori-agreed-to-fix',
   'OV5 CONFLICTS pointer: "... lane notice points at mori; mori agreed to correct its r12 entry"',
   prov=prov_sub(ROW['OV5'], ROW['OV5'][:-2] + '; mori agreed to correct its r12 entry |'))
sp('p-b15-agrees-does-not-contradict',
   'OV3 AGREES pointer: "meaning of `auto` (lane lines 201-202); mori does not contradict the lane"',
   prov=prov_sub(ROW['OV3'], '| OV3 | tsukuroi | AGREES | meaning of `auto` (lane lines 201-202); mori does not contradict the lane |'))
sp('p-b15-agrees-no-longer-conflicts-with',
   'OV3 AGREES pointer: "... mori HEAD no longer conflicts with the ancestor clause"',
   prov=prov_sub(ROW['OV3'], '| OV3 | tsukuroi | AGREES | meaning of `auto` (lane lines 201-202); mori HEAD no longer conflicts with the ancestor clause |'))
sp('p-b4-four-token-unit-list-lane',
   'OV1 lane_quote = the four unit names (4 whitespace tokens, the distinctive anchor)',
   reg_with(lambda g, r: r('OV1').update(lane_quote='`user@1000.service`, `user-1000.slice`, `user.slice` and `-.slice`')))
sp('p-b4-three-token-attribute-names',
   'OV6 quote = "the `user.oomd_ooms` / `user.oomd_kill`" (4 tokens) at its corrected line 198',
   reg_with(lambda g, r: r('OV6').update(quote='the `user.oomd_ooms` / `user.oomd_kill`', quote_line=198)))
sp('p-ov6-quote-line-corrected',
   'OV6 quote_line 196 -> 198 (the correction corrections_r27_a2 records)',
   reg_with(lambda g, r: r('OV6').update(quote_line=198)))
sp('p-b9-ov4-lane-other-sentence',
   'OV4 lane_quote from the allowed file, the OOMRules= sentence at memory-pressure-r25.md:387',
   reg_with(lambda g, r: r('OV4').update(lane_quote='Units with `OOMRules=` are also monitored')))
sp('p-b9-ov2-lane-drifted-target',
   'OV2 lane_quote from PROVINCE.md lines 30-31 (the drifted target the action names)',
   reg_with(lambda g, r: r('OV2').update(lane_quote='Host memory and kill-event measurements support OS triage;')))
sp('p-b8-shared-sentence-two-overlaps',
   'OV4 anchors the same mori sentence as OV3 (same line, same quote): tradeoff probe',
   reg_with(lambda g, r: r('OV4').update(quote=r('OV3')['quote'], quote_line=r('OV3')['quote_line'])))

# ---------------------------------------------------------------- should-fail
ov3q = BASE_REG['rows'][R['OV3']]['quote']
sf('f-b8-quote-line-shift',
   'OV4 copies OV3 quote, quote_line 145 instead of 146 (window still holds it): one anchor, two rows',
   reg_with(lambda g, r: r('OV4').update(quote=ov3q, quote_line=145)))


def five_on_one(g, r):
    frags = {'OV1': ('`auto` is the upstream default and means the', 144),
             'OV3': (ov3q, 146),
             'OV4': (ov3q, 145),
             'OV5': ('is the upstream default and means the cgroup\'s data', 146),
             'OV2': ('the upstream default and means the cgroup\'s data is', 145)}
    lane3 = r('OV3')['lane_quote']
    for rid, (q, ql) in frags.items():
        r(rid).update(quote=q, quote_line=ql)
        if rid != 'OV2':
            r(rid)['lane_quote'] = lane3


sf('f-b8-five-rows-one-sentence',
   'OV1-OV5 all anchor fragments of the one OV3 mori sentence via quote_line shifts and sub-quotes; OV1/3/4/5 share one lane quote',
   reg_with(five_on_one))
sf('f-lane-anchor-reused',
   'OV1, OV4, OV5 copy OV3 lane_quote (allowed file; no lane-side uniqueness)',
   reg_with(lambda g, r: [r(x).__setitem__('lane_quote', r('OV3')['lane_quote']) for x in ('OV1', 'OV4', 'OV5')]))
sf('f-b9-ov2-self-mirror',
   'OV2 lane_quote = its own PROVINCE pointer cell (register mirror quoting itself)',
   reg_with(lambda g, r: r('OV2').update(lane_quote='mori `PROVINCE.md:66` → lane PROVINCE lines now 30-33 and 44-53; mori re-pins')))
sf('f-b9-ov2-section-heading',
   'OV2 lane_quote = the round-27 section heading text itself',
   reg_with(lambda g, r: r('OV2').update(lane_quote='Adjacent — mori userspace OOM killers (round 27)')))
sf('f-b10-version-cut',
   'OV5 quote cut mid-token at a dot: "... does not exist in earlyoom 1.9" (source 1.9.0)',
   reg_with(lambda g, r: r('OV5').update(quote='The delegation exception that the previous entry named does not exist in earlyoom 1.9')))
sf('f-b10-unit-name-cut',
   'OV1 lane_quote cut inside a unit name: "... `user@1000.service`, `user-1000"',
   reg_with(lambda g, r: r('OV1').update(lane_quote='every one of the four captured units — `user@1000.service`, `user-1000')))
sf('f-b10-hyphen-cut',
   'OV3 quote starts mid-token after a hyphen: "oomd is inactive and disabled here" (source systemd-oomd)',
   reg_with(lambda g, r: r('OV3').update(quote='oomd is inactive and disabled here, and every unit the', quote_line=143)))
sf('f-b4-five-function-words',
   'OV5 quote = five function words "is a statement about a" (line 140)',
   reg_with(lambda g, r: r('OV5').update(quote='is a statement about a', quote_line=140, heading='## Facts')))
sf('f-b11-filler-actions',
   'every action = "see the register row"',
   reg_with(lambda g, r: [x.__setitem__('action', 'see the register row') for x in g['rows']]))
sf('f-b11-repeated-token-action',
   'every action = "x x x x"',
   reg_with(lambda g, r: [x.__setitem__('action', 'x x x x') for x in g['rows']]))
sf('f-b12-withdrawn-in-action',
   'every action rewritten "WITHDRAWN: not an anchor any more, history only"',
   reg_with(lambda g, r: [x.__setitem__('action', 'WITHDRAWN: not an anchor any more, history only') for x in g['rows']]))


def withdraw_top(g, r):
    g['status'] = 'withdrawn'
    g['corrections_r27_a2'].append({'row': 'all', 'field': 'rows', 'status': 'withdrawn',
                                    'note': 'no row of this register is an anchor any more'})


sf('f-b12-withdrawn-top-level-only',
   'top-level status "withdrawn" plus a corrections entry withdrawing all rows; rows untouched',
   reg_with(withdraw_top))
sf('f-b13-prose-withdrawal',
   'PROVINCE section gains a bold prose line "**Withdrawn:** no row below is an anchor any more" before the table',
   prov=prov_sub(TABLE_HDR, '**Withdrawn:** no row below is an anchor any more; history only.\n\n' + TABLE_HDR))
sf('f-b13-setext-heading',
   'a setext h2 "Withdrawn rows (history only)\\n---" before the table: renders as a new h2 section that holds the table',
   prov=prov_sub(TABLE_HDR, 'Withdrawn rows (history only)\n------------------------------\n\n' + TABLE_HDR))
sf('f-b13-setext-h1',
   'a setext h1 "Withdrawn\\n===" before the table',
   prov=prov_sub(TABLE_HDR, 'Withdrawn\n=========\n\n' + TABLE_HDR))
sf('f-b13-html-heading',
   'an HTML <h3>Withdrawn rows</h3> line before the table',
   prov=prov_sub(TABLE_HDR, '<h3>Withdrawn rows (history only)</h3>\n\n' + TABLE_HDR))
sf('f-b13-pre-block',
   'table wrapped in an HTML <pre> block (raw text, not a table)',
   prov=prov_sub(TABLE_HDR, '<pre>\n' + TABLE_HDR).rstrip('\n') + '\n</pre>\n')
sf('f-b13-details-collapsed',
   'table inside a collapsed <details> labelled withdrawn',
   prov=prov_sub(TABLE_HDR, '<details><summary>Withdrawn rows (history only)</summary>\n\n' + TABLE_HDR).rstrip('\n') + '\n\n</details>\n')
sf('f-b15-agreement-noun',
   'OV4 CONFLICTS pointer "in full agreement with the lane; nothing to report"',
   prov=prov_sub(ROW['OV4'], '| OV4 | tsukuroi | CONFLICTS | in full agreement with the lane; nothing to report |'))
sf('f-b15-no-conflicts-plural',
   'OV5 CONFLICTS pointer "no conflicts: lane and mori say the same"',
   prov=prov_sub(ROW['OV5'], '| OV5 | mori | CONFLICTS | no conflicts: lane and mori say the same |'))
sf('f-b15-consistent',
   'OV4 CONFLICTS pointer "mori F8 is consistent with lane lines 387-390"',
   prov=prov_sub(ROW['OV4'], '| OV4 | tsukuroi | CONFLICTS | mori F8 is consistent with lane lines 387-390 |'))
sf('f-b15-agrees-disagrees',
   'OV3 AGREES pointer "mori disagrees: conflicting meaning of `auto`"',
   prov=prov_sub(ROW['OV3'], '| OV3 | tsukuroi | AGREES | mori disagrees: conflicting meaning of `auto` |'))
sf('f-b15-fifth-column',
   'a fifth "note" column; OV5 note "no conflict: lane and mori agree" (B15 reads column 4 only)',
   prov=prov_sub(TABLE_HDR + ''.join(ROW[x] + '\n' for x in sorted(ROW)),
                 '| id | owner | class | pointer | note |\n|---|---|---|---|---|\n' +
                 ''.join(ROW[x] + (' no conflict: lane and mori agree |' if x == 'OV5' else ' |') + '\n'
                         for x in sorted(ROW))))


def main():
    rows = []
    for kind, name, note, reg, prov in V:
        sha = commit(name, reg, prov)
        code, anchored, reasons, shape, sib = run(sha)
        if kind == 'should-pass':
            verdict = 'OK' if anchored == 6 else 'OVER-STRICT'
        else:
            verdict = 'REFUSED' if anchored < 6 else 'ACCEPTED'
        rows.append({'kind': kind, 'variant': name, 'sha': sha, 'exit': code, 'anchored_rows': anchored,
                     'reasons': reasons, 'shape_errors': shape, 'sibling_check': sib,
                     'verdict': verdict, 'note': note})
        print('%-12s %-42s exit=%d anchored=%d %-11s %s' % (kind, name, code, anchored, verdict,
                                                             json.dumps(reasons, ensure_ascii=False)[:160]))
    with open(sys.argv[1], 'w', encoding='utf-8') as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
