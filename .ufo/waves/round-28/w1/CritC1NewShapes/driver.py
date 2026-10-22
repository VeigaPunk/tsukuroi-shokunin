#!/usr/bin/env python3
"""New should-fail register shapes for the round-28 adjacency counter (CritC1NewShapes)."""
import copy, json, os, re, shutil, subprocess, sys

EXPORT = '/fast/scratch/hyaku/tsuku28/CritC1NewShapes/tree'
WORK = '/fast/scratch/hyaku/tsuku28/CritC1NewShapes/sbx'
NOSIB = '/fast/scratch/hyaku/tsuku28/CritC1NewShapes/nosib'
REALSIB = '/home/vgpnk/Projects/shokunin'
TOOL = EXPORT + '/tools/check-adjacency-overlap.py'
REG = 'corpus/knowledge/adjacency-mori-oom-r27.json'
SNAP = '.ufo/waves/round-27/siblings/mori/corpus/knowledge/userspace-oom-killers-r26.md'
SECTION = '## Adjacent — mori userspace OOM killers (round 27)'


def g(*a):
    return subprocess.run(['git', '-C', WORK] + list(a), capture_output=True, text=True)


def rd(p):
    with open(os.path.join(WORK, p), encoding='utf-8') as fh:
        return fh.read()


def wr(p, s):
    full = os.path.join(WORK, p)
    os.makedirs(os.path.dirname(full) or '.', exist_ok=True)
    with open(full, 'w', encoding='utf-8') as fh:
        fh.write(s)


def setup():
    shutil.rmtree(WORK, ignore_errors=True)
    shutil.copytree(EXPORT, WORK, symlinks=True)
    os.makedirs(NOSIB, exist_ok=True)
    g('init', '-q')
    g('add', '-A')
    g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'base export f8e3a8f2')
    return g('rev-parse', 'HEAD').stdout.strip()


def rows_of(text):
    return json.loads(text)['rows']


def by_id(reg):
    return {r['id']: r for r in reg['rows']}


def province_section_bounds(text):
    i = text.index(SECTION)
    j = text.find('\n## ', i + 1)
    return i, (len(text) if j < 0 else j)


# ------------------------------------------------------------ mutants
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


def _province_rows_block(p):
    i, j = province_section_bounds(p)
    sec = p[i:j]
    lines = sec.split('\n')
    tbl = [l for l in lines if l.startswith('|')]
    return i, j, sec, tbl


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


MUTANTS = [
    ('control', lambda reg, f: 'unchanged'),
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
]


def main():
    base = setup()
    reg0 = rd(REG)
    prov0 = rd('PROVINCE.md')
    out = []
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
        g('branch', '-f', 'm-' + name, sha)
        rec = {'mutant': name, 'sha': sha, 'note': note}
        for label, root in (('live', REALSIB), ('nosib', NOSIB)):
            p = subprocess.run([sys.executable, TOOL, '--repo', WORK, '--revision', sha,
                                '--siblings-root', root], capture_output=True, text=True)
            try:
                j = json.loads(p.stdout.strip().splitlines()[-1])
            except Exception:
                j = {'raw': p.stdout[-300:], 'err': p.stderr[-300:]}
            rec[label] = {'exit': p.returncode, 'anchored_rows': j.get('anchored_rows'),
                          'reasons': {k: v for k, v in (j.get('rows') or {}).items() if v},
                          'shape_errors': j.get('shape_errors'), 'sibling_check': j.get('sibling_check')}
        rec['accepted'] = any(rec[l]['exit'] == 0 and rec[l]['anchored_rows'] == 6 for l in ('live', 'nosib'))
        out.append(rec)
        print(json.dumps(rec, ensure_ascii=False))
    acc = [r['mutant'] for r in out if r['accepted'] and r['mutant'] != 'control']
    print(json.dumps({'total_new': len(out) - 1, 'accepted': len(acc), 'accepted_mutants': acc}))


if __name__ == '__main__':
    main()
