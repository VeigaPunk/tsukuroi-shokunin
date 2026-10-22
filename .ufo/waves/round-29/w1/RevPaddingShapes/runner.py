#!/usr/bin/env python3
"""Re-run the round-28 wave-1 CritC1NewShapes padding mutants plus round-29
additions against any revision's adjacency counter.

Usage (wave 2): export the revision under test to a tree, then

  python3 runner.py --tree <export> --counter <tree>/tools/check-adjacency-overlap.py \
      --work <empty sandbox dir> --siblings-root /home/vgpnk/Projects/shokunin \
      --out results.jsonl

Each mutant is committed in a private sandbox repo (never the lane repo) and
scored twice: once with the real siblings root (sibling-verified) and once with
an empty root (sibling-unavailable). "accepted" = exit 0 and anchored_rows 6 in
either mode, matching the wave-1 and residual-report definition. GIT_* vars are
stripped from every subprocess environment (seat containment).
"""
import argparse, copy, hashlib, json, os, re, shutil, subprocess, sys

REG = 'corpus/knowledge/adjacency-mori-oom-r27.json'
SNAP = '.ufo/waves/round-27/siblings/mori/corpus/knowledge/userspace-oom-killers-r26.md'
SECTION = '## Adjacent — mori userspace OOM killers (round 27)'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}

ARGS = None  # filled in main()


def g(*a):
    return subprocess.run(['git', '-C', ARGS.work] + list(a), capture_output=True, text=True, env=ENV)


def rd(p):
    with open(os.path.join(ARGS.work, p), encoding='utf-8') as fh:
        return fh.read()


def wr(p, s):
    full = os.path.join(ARGS.work, p)
    os.makedirs(os.path.dirname(full) or '.', exist_ok=True)
    with open(full, 'w', encoding='utf-8') as fh:
        fh.write(s)


def setup():
    shutil.rmtree(ARGS.work, ignore_errors=True)
    shutil.copytree(ARGS.tree, ARGS.work, symlinks=True)
    os.makedirs(ARGS.nosib_root, exist_ok=True)
    g('init', '-q')
    g('add', '-A')
    g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'base export')
    return g('rev-parse', 'HEAD').stdout.strip()


def by_id(reg):
    return {r['id']: r for r in reg['rows']}


def province_section_bounds(text):
    i = text.index(SECTION)
    j = text.find('\n## ', i + 1)
    return i, (len(text) if j < 0 else j)


def _province_rows_block(p):
    i, j = province_section_bounds(p)
    sec = p[i:j]
    tbl = [l for l in sec.split('\n') if l.startswith('|')]
    return i, j, sec, tbl


# ------------------------------------------------------- wave-1 mutants (22)
def n_same_anchor_six_times(reg, f):
    r = by_id(reg)
    src = r['OV3']
    for rid in ('OV1', 'OV2', 'OV4', 'OV5'):
        for k in ('heading', 'quote', 'quote_line', 'lane_path', 'lane_quote'):
            r[rid][k] = src[k]
    return 'OV1, OV2, OV4, OV5 copy OV3 heading, quote, quote_line, lane_path, lane_quote (one anchor, five pads)'


def n_dot_slash_lane_snapshot(reg, f):
    r = by_id(reg)['OV3']
    r['lane_path'] = './' + SNAP
    r['lane_quote'] = r['quote']
    return 'OV3 lane_path "./" + mori snapshot path, lane_quote = the mori quote'


def n_dot_slash_lane_register(reg, f):
    r = by_id(reg)['OV4']
    r['lane_path'] = './' + REG
    r['lane_quote'] = 'Report to mori: its F8 sentence drops the qualifier'
    return 'OV4 lane_path "./corpus/knowledge/adjacency-mori-oom-r27.json", lane_quote = its own action text'


def n_dot_segment_lane_register(reg, f):
    r = by_id(reg)['OV4']
    r['lane_path'] = 'corpus/./knowledge/adjacency-mori-oom-r27.json'
    r['lane_quote'] = 'Report to mori: its F8 sentence drops the qualifier'
    return 'OV4 lane_path "corpus/./knowledge/adjacency-mori-oom-r27.json", lane_quote = its own action text'


def n_lane_from_counter_source(reg, f):
    r = by_id(reg)['OV3']
    r['lane_path'] = 'tools/check-adjacency-overlap.py'
    r['lane_quote'] = 'Count anchored rows of the round-27 mori overlap register'
    return 'OV3 lane_path tools/check-adjacency-overlap.py (the counter), lane_quote its docstring line'


def n_lane_from_province_own_summary(reg, f):
    r = by_id(reg)['OV3']
    r['lane_path'] = 'PROVINCE.md'
    r['lane_quote'] = 'Rows are reported, never absorbed: earlyoom behaviour and killer accounting are mori\'s;'
    return 'OV3 lane_path PROVINCE.md, lane_quote = the register\'s own summary paragraph in the Adjacent section'


def n_lane_from_lessons(reg, f):
    body = rd('corpus/lessons/round-27.md')
    m = re.search(r'OV\d[^\n]{40,}', body)
    words = m.group(0).split()[:8] if m else None
    r = by_id(reg)['OV4']
    r['lane_path'] = 'corpus/lessons/round-27.md'
    r['lane_quote'] = ' '.join(words)
    return 'OV4 lane_path corpus/lessons/round-27.md (a round lesson describing the register), lane_quote "%s"' % r['lane_quote']


def n_lane_from_scorecard(reg, f):
    r = by_id(reg)['OV1']
    r['lane_path'] = 'SCORECARD.md'
    body = rd('SCORECARD.md')
    m = re.search(r'[^\n]*adjacency-mori-oom-r27[^\n]*', body)
    words = m.group(0).split()
    i = next(k for k, w in enumerate(words) if 'adjacency-mori-oom-r27' in w)
    r['lane_quote'] = ' '.join(words[max(0, i - 3):i + 3])
    return 'OV1 lane_path SCORECARD.md, lane_quote "%s" (the scorecard naming the register)' % r['lane_quote']


def n_unrelated_lane_quote_agrees(reg, f):
    body = rd('corpus/knowledge/boot-plane.md')
    line = next(l for l in body.splitlines()
                if l and l[0].isalpha() and len(l.split()) >= 10 and '`' not in l)
    q = ' '.join(line.split()[:8])
    r = by_id(reg)['OV3']
    r['lane_path'] = 'corpus/knowledge/boot-plane.md'
    r['lane_quote'] = q
    return 'OV3 (class AGREES, meaning of `auto`) lane side = unrelated boot-plane.md sentence "%s"' % q


def n_mid_word_fragments(reg, f):
    r = by_id(reg)
    r['OV1']['quote'] = 'nit the sibling lane'
    r['OV1']['lane_quote'] = 'ery one of the four'
    r['OV3']['quote'] = 'he upstream default and'
    r['OV3']['lane_quote'] = 'he default and means'
    return 'OV1 quote "nit the sibling lane", lane_quote "ery one of the four"; OV3 quote "he upstream default and", lane_quote "he default and means"'


def n_generic_four_word_quotes(reg, f):
    r = by_id(reg)
    r['OV4']['quote'] = 'if the service were'
    r['OV5']['quote'] = 'that the previous entry'
    r['OV1']['lane_quote'] = 'one of the four'
    return 'OV4 quote "if the service were", OV5 quote "that the previous entry", OV1 lane_quote "one of the four"'


def n_placeholder_actions(reg, f):
    for row in reg['rows']:
        row['action'] = '-'
    return 'every action "-"'


def n_rows_marked_withdrawn(reg, f):
    for row in reg['rows']:
        row['status'] = 'withdrawn'
        row['withdrawn_reason'] = 'not an anchor; kept for history only'
    reg['withdrawn_rows'] = ['OV1', 'OV2', 'OV3', 'OV4', 'OV5', 'OV6']
    reg['corrections_r27_a2'].append({'row': 'all', 'status': 'withdrawn',
                                      'note': 'every row is withdrawn; the register anchors nothing'})
    return 'every row status "withdrawn" + top-level withdrawn_rows OV1..OV6 + a corrections entry withdrawing all'


def n_consistent_false_class(reg, f):
    r = by_id(reg)
    r['OV4']['class'] = 'AGREES'
    r['OV5']['owner'] = 'tsukuroi'
    r['OV5']['class'] = 'AGREES'
    p = f['PROVINCE.md']
    p = p.replace('| OV4 | tsukuroi | CONFLICTS |', '| OV4 | tsukuroi | AGREES |')
    p = p.replace('| OV5 | mori | CONFLICTS |', '| OV5 | tsukuroi | AGREES |')
    f['PROVINCE.md'] = p
    return 'OV4 CONFLICTS->AGREES and OV5 mori/CONFLICTS->tsukuroi/AGREES in BOTH register and PROVINCE'


def n_province_html_comment(reg, f):
    p = f['PROVINCE.md']
    i, j, sec, tbl = _province_rows_block(p)
    block = '\n'.join(tbl)
    sec2 = sec.replace(block, '<!--\n' + block + '\n-->')
    f['PROVINCE.md'] = p[:i] + sec2 + p[j:]
    return 'PROVINCE table wrapped in <!-- ... --> (not rendered)'


def n_province_mixed_fence(reg, f):
    p = f['PROVINCE.md']
    i, j, sec, tbl = _province_rows_block(p)
    block = '\n'.join(tbl)
    sec2 = sec.replace(block, '~~~text\n```\n' + block + '\n~~~')
    f['PROVINCE.md'] = p[:i] + sec2 + p[j:]
    return 'PROVINCE table inside a ~~~ fence whose first content line is ``` (CommonMark: one code block)'


def n_province_indented_code(reg, f):
    p = f['PROVINCE.md']
    i, j, sec, tbl = _province_rows_block(p)
    block = '\n'.join(tbl)
    sec2 = sec.replace(block, '\n'.join('    ' + l for l in tbl))
    f['PROVINCE.md'] = p[:i] + sec2 + p[j:]
    return 'PROVINCE table indented four spaces after a blank line (CommonMark indented code block)'


def n_province_withdrawn_subsection(reg, f):
    p = f['PROVINCE.md']
    i, j, sec, tbl = _province_rows_block(p)
    block = '\n'.join(tbl)
    sec2 = sec.replace(block, 'No row of this register is an anchor any more.\n\n'
                       '### Withdrawn rows (not anchors, history only)\n\n' + block)
    f['PROVINCE.md'] = p[:i] + sec2 + p[j:]
    return 'PROVINCE table moved under "### Withdrawn rows (not anchors, history only)" with prose withdrawing every row'


def n_province_no_delimiter_prose(reg, f):
    p = f['PROVINCE.md']
    i, j, sec, tbl = _province_rows_block(p)
    block = '\n'.join(tbl)
    body = [l for l in tbl if l.startswith('| OV')]
    sec2 = sec.replace(block, 'Rejected candidate rows, quoted verbatim:\n' + '\n'.join(body))
    f['PROVINCE.md'] = p[:i] + sec2 + p[j:]
    return 'PROVINCE header and |---| delimiter removed; OV lines follow a prose line "Rejected candidate rows, quoted verbatim:" (GFM: paragraph, not a table)'


def n_province_pointer_contradicts(reg, f):
    p = f['PROVINCE.md']
    p = re.sub(r'(\| OV5 \| mori \| CONFLICTS \|)[^\n]*', r'\1 no conflict: lane and mori agree on earlyoom; nothing reported |', p)
    f['PROVINCE.md'] = p
    return 'PROVINCE OV5 pointer cell says "no conflict: lane and mori agree"'


# ------------------------------------------------- round-29 added fixtures
def n_dup_anchor_all_six(reg, f):
    r = by_id(reg)
    src = r['OV3']
    for rid in ('OV1', 'OV2', 'OV4', 'OV5'):
        for k in ('heading', 'quote', 'quote_line', 'lane_path', 'lane_quote'):
            r[rid][k] = src[k]
    for k in ('heading', 'quote', 'quote_line'):
        r['OV6'][k] = src[k]
    return 'all six rows share OV3 sibling anchor; OV1-OV5 also share its lane side (OV6 keeps a null lane side, class LANE-GAP)'


def n_dup_anchor_lane_side_only(reg, f):
    r = by_id(reg)
    for rid in ('OV2', 'OV5'):
        r[rid]['lane_path'] = r['OV1']['lane_path']
        r[rid]['lane_quote'] = r['OV1']['lane_quote']
    return 'OV2 and OV5 copy OV1 lane_path and lane_quote only (distinct sibling anchors, duplicated lane side)'


def _province_row_line(p, rid):
    return next(l.strip() for l in p.splitlines()
                if l.strip().startswith('| %s |' % rid))


def n_mirror_pointer_cell(reg, f):
    r = by_id(reg)['OV3']
    cells = [c.strip() for c in _province_row_line(f['PROVINCE.md'], 'OV3').strip('|').split('|')]
    r['lane_path'] = 'PROVINCE.md'
    r['lane_quote'] = cells[3]
    return 'OV3 lane side = PROVINCE.md, lane_quote = its own PROVINCE row pointer cell "%s"' % cells[3]


def n_mirror_full_row(reg, f):
    r = by_id(reg)['OV4']
    line = _province_row_line(f['PROVINCE.md'], 'OV4')
    r['lane_path'] = 'PROVINCE.md'
    r['lane_quote'] = line
    return 'OV4 lane side = PROVINCE.md, lane_quote = its own full PROVINCE table row verbatim'


def n_province_later_row_contradicts(reg, f):
    p = f['PROVINCE.md'].rstrip('\n') + '\n| OV4 | mori | AGREES | correction: OV4 is mori\'s and agrees; the row above is superseded |\n'
    f['PROVINCE.md'] = p
    return 'PROVINCE table gains a later row "| OV4 | mori | AGREES | correction: ... the row above is superseded |" (first row wins)'


def n_province_shadow_section(reg, f):
    p = f['PROVINCE.md']
    i, j, sec, tbl = _province_rows_block(p)
    shadow = SECTION + '\n\n' + '\n'.join(tbl) + '\n\n'
    contra = sec
    for rid, own, cls in (('OV1', 'tsukuroi', 'INBOUND-RESOLVES'), ('OV3', 'tsukuroi', 'AGREES'),
                          ('OV4', 'tsukuroi', 'CONFLICTS')):
        contra = contra.replace('| %s | %s | %s |' % (rid, own, cls), '| %s | mori | CONFLICTS |' % rid)
    k = p.index('\n## ') + 1
    f['PROVINCE.md'] = p[:k] + shadow + p[k:i] + contra + p[j:]
    return 'an early duplicate "## Adjacent — mori ... (round 27)" section carries the matching table; the real section later says OV1, OV3, OV4 are mori CONFLICTS (first section wins)'



def n_withdrawn_top_level_and_prose(reg, f):
    reg['status'] = 'withdrawn'
    reg['superseded_by'] = 'corpus/knowledge/adjacency-mori-oom-r28.json'
    reg['withdrawn_note'] = 'register superseded; rows retained for history only'
    for row in reg['rows']:
        row['deprecated'] = True
    p = f['PROVINCE.md']
    i, j = province_section_bounds(p)
    sec = p[i:j]
    sec2 = sec.replace('| id | owner | class | pointer |',
                       '**Withdrawn 2026-10-21 — every row superseded, kept for history only.**\n\n'
                       '| id | owner | class | pointer |', 1)
    f['PROVINCE.md'] = p[:i] + sec2 + p[j:]
    return 'register top-level status "withdrawn" + superseded_by + per-row deprecated:true; PROVINCE section gains a bold withdrawn line above the table'


def n_clipped_words_two_rows(reg, f):
    r = by_id(reg)
    for rid, key in (('OV5', 'quote'), ('OV1', 'lane_quote')):
        words = r[rid][key].split()
        words[0] = words[0][1:]
        words[-1] = words[-1][:-1]
        r[rid][key] = ' '.join(words)
    return 'OV5 quote and OV1 lane_quote lose the first char of the first word and last char of the last word (mid-word-clip variant)'


def n_clipped_words_min_four(reg, f):
    r = by_id(reg)
    words = r['OV3']['quote'].split()[:4]
    words[-1] = words[-1][:-1]
    r['OV3']['quote'] = ' '.join(words)
    words = r['OV3']['lane_quote'].split()[:4]
    words[-1] = words[-1][:-1]
    r['OV3']['lane_quote'] = ' '.join(words)
    return 'OV3 quote and lane_quote cut to the 4-word floor with the last word clipped mid-token'


MUTANTS = [
    ('control', lambda reg, f: 'unchanged'),
    # wave-1 order (driver.out line order preserved)
    ('same-anchor-six-times', n_same_anchor_six_times),
    ('dot-slash-lane-path-snapshot', n_dot_slash_lane_snapshot),
    ('dot-slash-lane-path-register', n_dot_slash_lane_register),
    ('dot-segment-lane-path-register', n_dot_segment_lane_register),
    ('lane-from-counter-source', n_lane_from_counter_source),
    ('lane-from-province-own-summary', n_lane_from_province_own_summary),
    ('lane-from-lessons', n_lane_from_lessons),
    ('lane-from-scorecard', n_lane_from_scorecard),
    ('unrelated-lane-quote-agrees', n_unrelated_lane_quote_agrees),
    ('mid-word-fragments', n_mid_word_fragments),
    ('generic-four-word-quotes', n_generic_four_word_quotes),
    ('placeholder-actions', n_placeholder_actions),
    ('rows-marked-withdrawn', n_rows_marked_withdrawn),
    ('consistent-false-class', n_consistent_false_class),
    ('province-html-comment', n_province_html_comment),
    ('province-mixed-fence', n_province_mixed_fence),
    ('province-indented-code', n_province_indented_code),
    ('province-withdrawn-subsection', n_province_withdrawn_subsection),
    ('province-no-delimiter-prose', n_province_no_delimiter_prose),
    ('province-pointer-contradicts', n_province_pointer_contradicts),
    ('province-later-row-contradicts', n_province_later_row_contradicts),
    ('province-shadow-section', n_province_shadow_section),
    # round-29 additions
    ('r29-dup-anchor-all-six', n_dup_anchor_all_six),
    ('r29-dup-anchor-lane-side-only', n_dup_anchor_lane_side_only),
    ('r29-mirror-pointer-cell', n_mirror_pointer_cell),
    ('r29-mirror-full-row', n_mirror_full_row),
    ('r29-withdrawn-top-level-and-prose', n_withdrawn_top_level_and_prose),
    ('r29-clipped-words-two-rows', n_clipped_words_two_rows),
    ('r29-clipped-words-min-four', n_clipped_words_min_four),
]


def main():
    global ARGS
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--tree', required=True, help='export of the revision under test')
    ap.add_argument('--counter', required=True, help='path to check-adjacency-overlap.py to run')
    ap.add_argument('--work', required=True, help='private sandbox repo dir (wiped)')
    ap.add_argument('--siblings-root', default='/home/vgpnk/Projects/shokunin')
    ap.add_argument('--nosib-root', default='/fast/scratch/hyaku/tsukuroi-r29/RevPaddingShapes/nosib')
    ap.add_argument('--out', default=None, help='JSONL output path (default: stdout only)')
    ARGS = ap.parse_args()

    with open(ARGS.counter, 'rb') as fh:
        csha = hashlib.sha256(fh.read()).hexdigest()

    base = setup()
    reg0 = rd(REG)
    prov0 = rd('PROVINCE.md')
    lines, acc = [], []
    for name, fn in MUTANTS:
        g('checkout', '-q', '-f', base)
        reg = json.loads(reg0)
        files = {'PROVINCE.md': prov0}
        note = fn(reg, files)
        wr(REG, json.dumps(reg, indent=1, ensure_ascii=False) + '\n')
        for p, s in files.items():
            wr(p, s)
        g('add', '-A')
        g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', name, '--allow-empty')
        sha = g('rev-parse', 'HEAD').stdout.strip()
        rec = {'mutant': name, 'sha': sha, 'note': note}
        for label, root in (('live', ARGS.siblings_root), ('nosib', ARGS.nosib_root)):
            p = subprocess.run([sys.executable, ARGS.counter, '--repo', ARGS.work,
                                '--revision', sha, '--siblings-root', root],
                               capture_output=True, text=True, env=ENV)
            try:
                j = json.loads(p.stdout.strip().splitlines()[-1])
            except Exception:
                j = {'raw': p.stdout[-300:], 'err': p.stderr[-300:]}
            rec[label] = {'exit': p.returncode, 'anchored_rows': j.get('anchored_rows'),
                          'reasons': {k: v for k, v in (j.get('rows') or {}).items() if v},
                          'shape_errors': j.get('shape_errors'), 'sibling_check': j.get('sibling_check')}
        rec['accepted'] = any(rec[l]['exit'] == 0 and rec[l]['anchored_rows'] == 6 for l in ('live', 'nosib'))
        lines.append(json.dumps(rec, ensure_ascii=False))
        if rec['accepted'] and name != 'control':
            acc.append(name)
    w1 = [m for m, _ in MUTANTS[1:23]]
    w1_acc = [m for m in acc if m in w1]
    new_acc = [m for m in acc if m not in w1]
    summary = {'counter_sha256': csha, 'wave1_total': 22, 'wave1_accepted': len(w1_acc),
               'wave1_accepted_mutants': w1_acc, 'r29_added_total': len(MUTANTS) - 23,
               'r29_added_accepted': len(new_acc), 'r29_added_accepted_mutants': new_acc}
    lines.append(json.dumps(summary))
    text = '\n'.join(lines) + '\n'
    sys.stdout.write(text)
    if ARGS.out:
        with open(ARGS.out, 'w', encoding='utf-8') as fh:
            fh.write(text)


if __name__ == '__main__':
    main()
