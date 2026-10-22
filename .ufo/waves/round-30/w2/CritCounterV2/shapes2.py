#!/usr/bin/env python3
"""CritCounterV2 harness: new should-fail / should-pass shapes for check-btrfs-space-r30.py version 2.

Reuses the wave-1 CritCounterShapes helpers (w1rerun/shapes.py, which loads base_fixture() from the
clone's battery v2), runs the counter in --tree mode, renders SKILL.md with GitHub's cmark-gfm
(cmarkgfm, unsafe, GFM extensions) as an oracle for marker shapes, checks the lane's verbatim
quote contract (`sed -n '<line>p' | grep -cF '<quote>'` == 1) for quote shapes, and mutates the
real lane tree at the tip for the R8 real-data shapes.
Usage: <gfm-venv-python> shapes2.py <clone> <outdir>
"""
import copy
import html
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLONE, OUT = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], CLONE, OUT]
sys.path.insert(0, os.path.join(HERE, 'w1rerun'))
os.makedirs(OUT, exist_ok=True)
import shapes as S  # noqa: E402
import cmarkgfm  # noqa: E402
from cmarkgfm.cmark import Options  # noqa: E402

bat, row, EV = S.bat, S.row, S.EV
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
TIP = '29bf87fa3971df04cb96e4ad9a28805d8154ed2f'
BASE = 'fbfec6bdf8833e7513732a06000801a8ee9b690b'
TABLE = ['| id | statement | source |', '|---|---|---|']
SH = []


def shape(name, expected, catch, targets):
    def deco(fn):
        SH.append((name, expected, catch, targets, fn))
        return fn
    return deco


def gfm(md, rid='D01'):
    """Rendered facts for marker rid: is it the first cell of a visible table row, the row's visible text, mentions."""
    out = cmarkgfm.github_flavored_markdown_to_html(md, options=Options.CMARK_OPT_UNSAFE)
    vis = re.sub(r'<!--.*?-->|<\?.*?\?>|<!\[CDATA\[.*?\]\]>|<![A-Za-z][^>]*>', ' ', out, flags=re.S)
    vis = re.sub(r'<pre.*?</pre>|<code.*?</code>|<script.*?</script>|&lt;script.*?&lt;/script&gt;', ' ', vis, flags=re.S)
    m = re.search(r'<tr>\s*<td[^>]*>\[R30-%s\]</td>(.*?)</tr>' % rid, vis, re.S)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', vis))
    return {'gfm_marker_in_table_row': bool(m),
            'gfm_row_text': ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', m.group(1))).split()) if m else None,
            'gfm_mentions': len(re.findall(r'R30-%s' % rid, text))}


def verbatim(files, r):
    lines = S.b(files[r['snapshot']]).split(b'\n')
    ln = r['line']
    one = lines[ln - 1] if 1 <= ln <= len(lines) else b''
    return one.count(r['quote'].encode()) >= 1 and r['quote'].encode() in one


def at_end(f, rid, wrap):
    S.move_marker_to_end(f, rid, wrap)


# ------------------------------------------------ wave-1 host shapes re-keyed for the v2 capture key
@shape('H01k-value-is-date-component-on-keyed-line', 'refuse', 'mechanical', ['D08'])
def _(f, rw):
    r = row(rw, 'D08')
    f[r['capture']] = '# capture\nallocation/metadata/bytes_used sampled 2026-10-22: 1007\n'
    r.update(value='2026', statement=r['statement'].replace('1007', '2026'))
    S.skill_line(f, 'D08', lambda l: [l.replace('1007', '2026')])


@shape('H02k-value-is-grep-n-line-number-on-keyed-line', 'refuse', 'mechanical', ['D08'])
def _(f, rw):
    r = row(rw, 'D08')
    f[r['capture']] = '# capture\n7:/sys/fs/btrfs/u/allocation/metadata/bytes_used:1007\n'
    r.update(value='7', statement=r['statement'].replace('1007', '7'))
    S.skill_line(f, 'D08', lambda l: [l.replace('1007', '7')])


@shape('H04k-value-from-other-key-on-keyed-line', 'refuse', 'mechanical', ['D08'])
def _(f, rw):
    r = row(rw, 'D08')
    f[r['capture']] = '# capture\nallocation/metadata/bytes_used: 1007 allocation/metadata/total_bytes: 5000\n'
    r.update(value='5000', statement=r['statement'].replace('1007', '5000'))
    S.skill_line(f, 'D08', lambda l: [l.replace('1007', '5000')])


@shape('H05k-host-rows-share-one-measurement-via-capture-copy', 'refuse', 'mechanical', ['D08', 'D09'])
def _(f, rw):
    d8, d9 = row(rw, 'D08'), row(rw, 'D09')
    line = '# c\nallocation/metadata/bytes_used: 1007 (unallocated not read)\n'
    f[d8['capture']] = line
    f[EV + '/capture-copy.txt'] = line
    d9.update(capture=EV + '/capture-copy.txt', capture_line=2, value='1007',
              statement=d9['statement'].replace('1008', '1007'))
    S.skill_line(f, 'D09', lambda l: [l.replace('1008', '1007')])


@shape('H06k-capture-is-doc-example-not-host', 'refuse', 'semantic', ['D10'])
def _(f, rw):
    r = row(rw, 'D10')
    f.pop(r['capture'])
    doc = row(rw, 'D01')['snapshot']
    f[doc] = f[doc].replace('trailer line', 'Example: /sys/fs/btrfs/<uuid>/allocation/global_rsv_size: 1009')
    r.update(capture=doc, capture_line=3)


@shape('H07-capture-key-negated-on-line', 'refuse', 'mechanical', ['D09'])
def _(f, rw):
    r = row(rw, 'D09')
    f[r['capture']] = '# capture\nunallocated: not read; allocation/data/total_bytes: 1008\n'


@shape('H08-value-is-digit-run-inside-hex-uuid', 'refuse', 'mechanical', ['D10'])
def _(f, rw):
    r = row(rw, 'D10')
    f[r['capture']] = '# c\n/sys/fs/btrfs/1d02a454-c549-4a35/allocation/global_rsv_size: 536870912\n'
    r.update(value='454', statement=r['statement'].replace('1009', '454'))
    S.skill_line(f, 'D10', lambda l: [l.replace('1009', '454')])


# ------------------------------------------------ R6 / R7
@shape('N40-token-only-on-already-cited-line-window-start-above', 'refuse', 'mechanical', ['D02'])
def _(f, rw):
    d1, d2 = row(rw, 'D01'), row(rw, 'D02')
    text = 'On ENOSPC the kernel consults two pools\nthe unallocated space and the global reserve are both consulted first.\nt\n'
    S.set_snap(f, d1, text, 2, 'the unallocated space and the global reserve are both consulted')
    f.pop(d2['snapshot'])
    d2.update(source=d1['source'], snapshot=d1['snapshot'], line=1,
              quote='On ENOSPC the kernel consults two pools the unallocated space and the global reserve')
    S.skill_line(f, 'D02', lambda l: [l.replace('S901', 'S900')])


@shape('N41-hyphen-meta-data-satisfies-data-token', 'refuse', 'mechanical', ['D09'])
def _(f, rw):
    r = row(rw, 'D09')
    S.set_snap(f, r, 'h\nThe meta-data block groups hold the extent tree and checksums.\nt\n', 2,
               'The meta-data block groups hold the extent tree')


@shape('N42-hyphen-de-dup-satisfies-dup-token', 'refuse', 'mechanical', ['D04'])
def _(f, rw):
    r = row(rw, 'D04')
    S.set_snap(f, r, 'h\nOut-of-band de-dup tools share identical extents between files.\nt\n', 2,
               'Out-of-band de-dup tools share identical extents')


@shape('N43-near-identical-snapshot-copy-reused', 'refuse', 'mechanical', ['D02'])
def _(f, rw):
    d1, d2 = row(rw, 'D01'), row(rw, 'D02')
    text = 'h\nOn ENOSPC the unallocated space and the global reserve are both consulted first.\nt\n'
    S.set_snap(f, d1, text, 2, 'On ENOSPC the unallocated space and the global reserve are both consulted')
    S.set_snap(f, d2, text + '\n', 2, d1['quote'])


@shape('N44-html-snapshot-quote-not-verbatim-entity', 'refuse', 'mechanical', ['D05'])
def _(f, rw):
    r = row(rw, 'D05')
    f.pop(r['snapshot'])
    r['snapshot'] = r['snapshot'][:-4] + '.html'
    S.set_snap(f, r, 'h\n<p>Block groups below the threshold are reclaim candidates &amp; get relocated.</p>\nt\n', 2,
               'Block groups below the threshold are reclaim candidates & get relocated.')


@shape('N45-html-snapshot-multiline-comment-body', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    f.pop(r['snapshot'])
    r['snapshot'] = r['snapshot'][:-4] + '.html'
    S.set_snap(f, r, '<p>visible</p>\n<!--\nhidden draft: unallocated space is only ever used for data chunks\n-->\n', 3,
               'unallocated space is only ever used for data chunks')


@shape('N46-html-snapshot-script-body', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    f.pop(r['snapshot'])
    r['snapshot'] = r['snapshot'][:-4] + '.html'
    S.set_snap(f, r, '<script>\nvar tip = "unallocated space is never needed for metadata";\n</script>\n', 2,
               'unallocated space is never needed for metadata')


@shape('N47-html-snapshot-tag-strip-joins-cells', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    f.pop(r['snapshot'])
    r['snapshot'] = r['snapshot'][:-4] + '.html'
    S.set_snap(f, r, 'h\n<tr><td>unallocated space</td><td>is exhausted</td><td>never</td></tr>\nt\n', 2,
               'unallocated space is exhausted never')


# ------------------------------------------------ R4
@shape('N50-decoy-registry-header-in-comment-before-real-table', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    lines, i = S.reg_line(f, 'S900')
    m = lines.pop(i)
    head = '\n'.join(lines)
    other = [l for l in lines if l.startswith('| S9')]
    decoy = '<!--\n' + bat.HEADER + m + '\n' + '\n'.join(other) + '\n-->\n\n'
    f['corpus/SOURCES.md'] = head.replace('# SOURCES\n\n', '# SOURCES\n\n' + decoy, 1)


@shape('N51-registry-header-without-delimiter-not-a-table', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    t = f['corpus/SOURCES.md']
    f['corpus/SOURCES.md'] = t.replace('|---|---|---|---|---|---|---|---|---|---|---|\n',
                                       '| S899 | placeholder |\n', 1)


# ------------------------------------------------ R9 should-fail (v2 counts the marker; GFM hides or breaks it)
def tbl(m):
    return [''] + TABLE + [m]


@shape('N01-delimiter-column-count-mismatch-not-a-table', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    at_end(f, 'D01', lambda m: ['', '| id | statement | source |', '|---|---|', m])


@shape('N02-source-only-in-cell-beyond-header-width', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    at_end(f, 'D01', lambda m: ['', '| id | statement |', '|---|---|', m.replace('| S900 |', '| none | S900 |')])


@shape('N03-source-only-inside-inline-comment', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    S.skill_line(f, 'D01', lambda l: [l.replace('| S900 |', '| none <!-- S900 --> |')])


@shape('N04-host-value-only-inside-inline-comment', 'refuse', 'mechanical', ['D08'])
def _(f, rw):
    S.skill_line(f, 'D08', lambda l: [l.replace(' value 1007', ' <!-- 1007 -->')])


@shape('N05-second-mention-backslash-escaped-hyphen', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    f['SKILL.md'] += '\nR30\\-D01 is withdrawn; do not use it.\n'


@shape('N06-second-mention-html-entity', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    f['SKILL.md'] += '\nR30&#45;D01 is withdrawn; do not use it.\n'


@shape('N07-table-inside-processing-instruction-block', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    at_end(f, 'D01', lambda m: ['<?hidden'] + tbl(m) + ['?>'])


@shape('N08-table-inside-cdata-block', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    at_end(f, 'D01', lambda m: ['<![CDATA['] + tbl(m) + [']]>'])


@shape('N09-table-inside-declaration-block', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    at_end(f, 'D01', lambda m: ['<!HIDDEN'] + tbl(m) + ['>'])


@shape('N10-fence-closer-formfeed-then-table', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    at_end(f, 'D01', lambda m: ['```', '```\x0c'] + tbl(m) + ['```'])


@shape('N11-fence-closer-tab-indented-then-table', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    at_end(f, 'D01', lambda m: ['```', '\t```'] + tbl(m) + ['```'])


@shape('N12-fence-closer-nbsp-then-table', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    at_end(f, 'D01', lambda m: ['```', '```\u00a0'] + tbl(m) + ['```'])


@shape('N13-pre-closer-with-space-then-table', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    at_end(f, 'D01', lambda m: ['<pre>', '</pre >'] + tbl(m) + ['</pre>'])


@shape('N14-fence-opener-info-string-opens-comment', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    at_end(f, 'D01', lambda m: ['``` <!--', '-->'] + tbl(m) + ['```'])


@shape('N15-table-in-div-hidden', 'refuse', 'semantic', ['D01'])
def _(f, rw):
    at_end(f, 'D01', lambda m: ['<div hidden>'] + tbl(m) + ['', '</div>'])


@shape('N16-withdrawal-in-allowed-top-level-key', 'refuse', 'semantic', ['D01'])
def _(f, rw):
    f['__json_extra__'] = {'supporting_citations': {'D01': 'WITHDRAWN: wrong, do not use'}}


# ------------------------------------------------ R9 should-pass (GFM renders a visible table row; v2 refuses?)
@shape('P20-table-right-after-closed-comment-line', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    f['SKILL.md'] = f['SKILL.md'].replace('# SKILL\n\n', '# SKILL\n\n<!-- table follows -->\n', 1)


@shape('P21-table-right-after-fence-closer', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    f['SKILL.md'] = f['SKILL.md'].replace('# SKILL\n\n', '# SKILL\n\n```\ncode\n```\n', 1)


@shape('P22-table-interrupts-paragraph', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    f['SKILL.md'] = f['SKILL.md'].replace('# SKILL\n\n', '# SKILL\n\nRows:\n', 1)


@shape('P23-bare-comment-opener-mid-prose', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    f['SKILL.md'] = f['SKILL.md'].replace('# SKILL\n', '# SKILL\n\nNever type <!-- inside a cell.\n', 1)


@shape('P24-unclosed-comment-opener-inside-earlier-row', 'accept', 'mechanical', ['D02'])
def _(f, rw):
    S.skill_line(f, 'D01', lambda l: [l.replace('| statement |', '| statement; never type <!-- in a cell |')])


@shape('P25-delimiter-row-without-trailing-pipe', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    f['SKILL.md'] = f['SKILL.md'].replace('|---|---|---|\n', '|---|---|---\n', 1)


@shape('P26-header-row-without-leading-pipe', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    f['SKILL.md'] = f['SKILL.md'].replace('| id | statement | source |\n', 'id | statement | source |\n', 1)


@shape('P27-crlf-skill-and-sources', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    f['__crlf__'] = True


@shape('P28-table-after-hash-tag-line-not-heading', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    f['SKILL.md'] = f['SKILL.md'].replace('# SKILL\n\n', '# SKILL\n\n#tag\n', 1)


@shape('P29-fence-opener-info-string-with-closed-comment', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    f['SKILL.md'] = f['SKILL.md'].replace('# SKILL\n', '# SKILL\n\n```html <!-- x -->\n<p>example</p>\n```\n', 1)


@shape('P30-pre-block-closed-by-other-raw-end-tag', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    f['SKILL.md'] = f['SKILL.md'].replace('# SKILL\n', '# SKILL\n\n<pre>\nexample\n</textarea>\n', 1)


def run_fixture():
    work = os.path.join(OUT, 'work')
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    bs = os.path.join(work, 'base-sources.md')
    with open(bs, 'w') as fh:
        fh.write('# base\n\n' + bat.HEADER)
    res = []
    f0, r0 = bat.base_fixture()
    d = os.path.join(work, 'CONTROL')
    S.materialize(d, f0, r0)
    per, summ, rc = S.run(d, bs)
    res.append({'shape': 'CONTROL', 'verified': summ.get('verified'), 'rc': rc,
                'counter_sha256': summ.get('counter_sha256'), 'gfm_control': gfm(f0['SKILL.md'])})
    print(json.dumps(res[-1]), flush=True)
    for name, expected, catch, targets, fn in SH:
        files, rows = bat.base_fixture()
        fn(files, rows)
        crlf = files.pop('__crlf__', None)
        skill_md = files['SKILL.md']
        snap_view = {r['id']: (copy.deepcopy(r), files.get(r['snapshot'])) for r in rows if r['id'] in targets}
        d = os.path.join(work, name)
        S.materialize(d, files, rows)
        if crlf:
            for p in ('SKILL.md', 'corpus/SOURCES.md'):
                full = os.path.join(d, p)
                t = open(full, 'rb').read().replace(b'\n', b'\r\n')
                open(full, 'wb').write(t)
        per, summ, rc = S.run(d, bs)
        tv = {t: per.get(t, {}).get('verified') for t in targets}
        accepted = all(tv.values())
        ok = (accepted and summ.get('verified') == 10) if expected == 'accept' else not accepted
        o = {'shape': name, 'expected': expected, 'catch': catch, 'targets': tv,
             'counter': 'ACCEPTED' if accepted else 'REFUSED', 'total_verified': summ.get('verified'),
             'counter_correct': ok,
             'failures': {k: v.get('failures') for k, v in per.items() if v.get('failures')}}
        if name[0] in 'NP' and name[:3] not in ('N40', 'N41', 'N42', 'N43', 'N44', 'N45', 'N46', 'N47', 'N50', 'N51') \
                and name[:3] != 'N16':
            o['gfm'] = gfm(skill_md, targets[0] if name[:3] != 'P24' else 'D02')
        for t, (r, c) in snap_view.items():
            if c is not None and isinstance(c, (str, bytes)) and name[:3] in ('N40', 'N41', 'N42', 'N43', 'N44', 'N45', 'N46', 'N47'):
                o.setdefault('verbatim_one_line', {})[t] = verbatim({r['snapshot']: c}, r)
        res.append(o)
        print(json.dumps(o, ensure_ascii=True), flush=True)
    return res


# ------------------------------------------------ real lane tree at the tip, R8 real-data shapes
def real_tree(name, mutate):
    d = os.path.join(OUT, 'real', name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    a = subprocess.run(['git', '-C', CLONE, 'archive', TIP], capture_output=True, env=ENV, check=True).stdout
    subprocess.run(['tar', '-x', '-C', d], input=a, check=True)
    bs = os.path.join(OUT, 'real', 'base-sources.md')
    with open(bs, 'wb') as fh:
        fh.write(subprocess.run(['git', '-C', CLONE, 'show', BASE + ':corpus/SOURCES.md'], capture_output=True,
                                env=ENV, check=True).stdout)
    if mutate:
        mutate(d)
    per, summ, rc = S.run(d, bs)
    return per, summ, rc


def real_value(rid, old, new):
    def m(d):
        jp = os.path.join(d, S.JSON)
        doc = json.load(open(jp))
        r = next(x for x in doc['rows'] if x['id'] == rid)
        r['value'] = new
        r['statement'] = r['statement'].replace(old, new)
        assert new in r['statement']
        json.dump(doc, open(jp, 'w'), indent=1)
        sp = os.path.join(d, 'SKILL.md')
        t = open(sp).read().split('\n')
        i = next(k for k, l in enumerate(t) if l.startswith('| [R30-%s] ' % rid))
        assert old in t[i]
        t[i] = t[i].replace(old, new)
        open(sp, 'w').write('\n'.join(t))
    return m


REAL = [('REAL-CONTROL', 'D09', None),
        ('REAL-D09-value-95-a-line-number-operand-on-line-98', 'D09', real_value('D09', '690922455040', '95')),
        ('REAL-D09-value-998037782528-device-size-operand', 'D09', real_value('D09', '690922455040', '998037782528')),
        ('REAL-D08-value-454-digit-run-in-fsid', 'D08', real_value('D08', '35372056576', '454')),
        ('REAL-D10-value-60902-digit-run-in-fsid', 'D10', real_value('D10', '536870912', '60902'))]


def main():
    res = run_fixture()
    for name, rid, fn in REAL:
        per, summ, rc = real_tree(name, fn)
        o = {'shape': name, 'expected': 'accept' if fn is None else 'refuse', 'catch': 'mechanical',
             'target': rid, 'target_verified': per.get(rid, {}).get('verified'),
             'total_verified': summ.get('verified'), 'failures': per.get(rid, {}).get('failures')}
        o['counter'] = 'ACCEPTED' if o['target_verified'] else 'REFUSED'
        o['counter_correct'] = (o['counter'] == 'ACCEPTED') == (o['expected'] == 'accept')
        res.append(o)
        print(json.dumps(o), flush=True)
    sh = res[1:]
    print(json.dumps({'control': res[0]['verified'], 'shapes': len(sh),
                      'should_fail_accepted': [r['shape'] for r in sh if r['expected'] == 'refuse' and r['counter'] == 'ACCEPTED'],
                      'should_pass_refused': [r['shape'] for r in sh if r['expected'] == 'accept' and not r['counter_correct']],
                      'counter_sha256': res[0].get('counter_sha256')}))


if __name__ == '__main__':
    main()
