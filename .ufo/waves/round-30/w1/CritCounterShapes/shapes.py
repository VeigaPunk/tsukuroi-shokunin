#!/usr/bin/env python3
"""CritCounterShapes harness: extra should-fail / should-pass shapes for check-btrfs-space-r30.py.

Reuses base_fixture() of tools/mutants-btrfs-space-r30.py, writes each mutated fixture (bytes,
symlinks allowed), runs the counter in --tree mode, and renders SKILL.md with cmark --unsafe for
the marker shapes. Usage: shapes.py <clone> <outdir>
"""
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

CLONE, OUT = sys.argv[1], sys.argv[2]
COUNTER = os.path.join(CLONE, 'tools/check-btrfs-space-r30.py')
spec = importlib.util.spec_from_file_location('bat', os.path.join(CLONE, 'tools/mutants-btrfs-space-r30.py'))
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)
EV = bat.EV
JSON = 'corpus/knowledge/btrfs-space-r30.json'
OUTSIDE = os.path.join(OUT, 'outside-snapshot.txt')


def row(rows, rid):
    return next(r for r in rows if r['id'] == rid)


def b(x):
    return x.encode('utf-8') if isinstance(x, str) else x


def set_snap(files, r, text, line, quote):
    files[r['snapshot']] = text
    r['line'], r['quote'] = line, quote


def skill_line(files, rid, fn):
    lines = files['SKILL.md'].split('\n')
    i = next(k for k, l in enumerate(lines) if l.startswith('| [R30-%s] ' % rid))
    lines[i:i + 1] = fn(lines[i])
    files['SKILL.md'] = '\n'.join(lines)


def move_marker_to_end(files, rid, wrap):
    """Remove the marker line from the table and append it at EOF wrapped by wrap(line)."""
    lines = files['SKILL.md'].rstrip('\n').split('\n')
    i = next(k for k, l in enumerate(lines) if l.startswith('| [R30-%s] ' % rid))
    m = lines.pop(i)
    files['SKILL.md'] = '\n'.join(lines + [''] + wrap(m)) + '\n'


def reg_line(files, sid):
    lines = files['corpus/SOURCES.md'].split('\n')
    i = next(k for k, l in enumerate(lines) if l.startswith('| %s |' % sid))
    return lines, i


def move_reg_to_end(files, sid, wrap):
    lines, i = reg_line(files, sid)
    m = lines.pop(i)
    files['corpus/SOURCES.md'] = '\n'.join(lines).rstrip('\n') + '\n\n' + '\n'.join(wrap(m)) + '\n'


def resync(files, rows):
    regl = files['corpus/SOURCES.md'].split('\n')
    for r in rows:
        snap = r.get('snapshot') if isinstance(r, dict) else None
        if not isinstance(snap, str):
            continue
        p = os.path.normpath(snap)
        c = files.get(snap, files.get(p))
        if isinstance(c, tuple):            # symlink
            tgt = c[1]
            c = open(tgt, 'rb').read() if os.path.isabs(tgt) and os.path.exists(tgt) else None
        if c is None:
            continue
        sha = hashlib.sha256(b(c)).hexdigest()
        for k, l in enumerate(regl):
            if l.startswith('| %s |' % r['source']):
                regl[k] = re.sub(r'sha256 [0-9a-f]{64}', 'sha256 ' + sha, l)
    files['corpus/SOURCES.md'] = '\n'.join(regl)


# ---------------------------------------------------------------- shapes
# each: (name, expected, catchable, targets, mutate) ; expected 'refuse' (should-fail) or 'accept' (should-pass)
SH = []


def shape(name, expected, catch, targets):
    def deco(fn):
        SH.append((name, expected, catch, targets, fn))
        return fn
    return deco


# --- quote / snapshot (R6, R7)
@shape('A01-strip-creates-adjacency-plain-text', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    set_snap(f, r, 'notes\nMetadata writes <- do not -> succeed when unallocated space is exhausted.\nend\n', 2,
             'Metadata writes succeed when unallocated space is exhausted')


@shape('A02-quote-from-comment-saying-opposite', 'refuse', 'semantic', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    set_snap(f, r, 'int x;\n/* WRONG, removed in v6.1: unallocated space is never used for metadata chunks */\nint y;\n', 2,
             'unallocated space is never used for metadata chunks')


@shape('A03-quote-from-html-comment-body', 'refuse', 'semantic', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    set_snap(f, r, '<p>visible</p>\n<!--\nhidden draft: unallocated space is only ever used for data chunks\n-->\n', 3,
             'unallocated space is only ever used for data chunks')


@shape('A04-statement-contradicts-quote', 'refuse', 'semantic', ['D01'])
def _(f, rw):
    row(rw, 'D01')['statement'] = ('Btrfs never needs unallocated space for anything, so ENOSPC with free data space '
                                   'cannot happen on any filesystem at all.')


@shape('A05-one-source-for-unrelated-rows', 'accept', 'semantic', ['D01', 'D02', 'D03'])
def _(f, rw):
    d1 = row(rw, 'D01')
    text = ('h\nThis fixture sentence explains the unallocated behaviour of the filesystem in detail.\n'
            'This line explains the global reserve behaviour of the filesystem in detail.\n'
            'This line explains the balance usage filter behaviour of the filesystem.\n')
    f[d1['snapshot']] = text
    for rid, ln, q in (('D02', 3, 'explains the global reserve behaviour of the filesystem'),
                       ('D03', 4, 'explains the balance usage filter behaviour')):
        r = row(rw, rid)
        f.pop(r['snapshot'])
        r.update(source=d1['source'], snapshot=d1['snapshot'], line=ln, quote=q)
        skill_line(f, rid, lambda l, s=d1['source'], o=r: [re.sub(r'S9\d\d', s, l)])


def _two_token_snap(f, rw):
    d1, d2 = row(rw, 'D01'), row(rw, 'D02')
    return d1, d2


@shape('A06-reuse-bypass-blank-cited-line', 'refuse', 'mechanical', ['D01', 'D02'])
def _(f, rw):
    d1, d2 = row(rw, 'D01'), row(rw, 'D02')
    text = '\nOn ENOSPC the unallocated space and the global reserve are both consulted first.\ntrailer\n'
    set_snap(f, d1, text, 1, 'On ENOSPC the unallocated space and the global reserve are both consulted')
    f.pop(d2['snapshot'])
    d2.update(source=d1['source'], snapshot=d1['snapshot'], line=2,
              quote='On ENOSPC the unallocated space and the global reserve are both consulted')
    skill_line(f, 'D02', lambda l: [l.replace('S901', 'S900')])


@shape('A07-reuse-bypass-start-at-last-char-of-previous-line', 'refuse', 'mechanical', ['D01', 'D02'])
def _(f, rw):
    d1, d2 = row(rw, 'D01'), row(rw, 'D02')
    text = 'header X\nOn ENOSPC the unallocated space and the global reserve are both consulted first.\ntrailer\n'
    set_snap(f, d1, text, 2, 'On ENOSPC the unallocated space and the global reserve are both consulted')
    f.pop(d2['snapshot'])
    d2.update(source=d1['source'], snapshot=d1['snapshot'], line=1,
              quote='X On ENOSPC the unallocated space and the global reserve are both consulted')
    skill_line(f, 'D02', lambda l: [l.replace('S901', 'S900')])


@shape('A08-reuse-bypass-path-alias-dot', 'refuse', 'mechanical', ['D01', 'D02'])
def _(f, rw):
    d1, d2 = row(rw, 'D01'), row(rw, 'D02')
    text = 'h\nOn ENOSPC the unallocated space and the global reserve are both consulted first.\nt\n'
    set_snap(f, d1, text, 2, 'On ENOSPC the unallocated space and the global reserve are both consulted')
    f.pop(d2['snapshot'])
    d2.update(source=d1['source'], snapshot=d1['snapshot'].replace('/S900', '/./S900'), line=2, quote=d1['quote'])
    skill_line(f, 'D02', lambda l: [l.replace('S901', 'S900')])


@shape('A09-reuse-bypass-byte-identical-copy', 'refuse', 'mechanical', ['D01', 'D02'])
def _(f, rw):
    d1, d2 = row(rw, 'D01'), row(rw, 'D02')
    text = 'h\nOn ENOSPC the unallocated space and the global reserve are both consulted first.\nt\n'
    set_snap(f, d1, text, 2, 'On ENOSPC the unallocated space and the global reserve are both consulted')
    set_snap(f, d2, text, 2, d1['quote'])


@shape('A10a-token-substring-data-in-metadata', 'refuse', 'mechanical', ['D09'])
def _(f, rw):
    r = row(rw, 'D09')
    set_snap(f, r, 'h\nThe metadata block groups hold the extent tree and checksums.\nt\n', 2,
             'The metadata block groups hold the extent tree')


@shape('A10b-token-substring-dup-in-duplicate', 'refuse', 'mechanical', ['D04'])
def _(f, rw):
    r = row(rw, 'D04')
    set_snap(f, r, 'h\nA duplicate device id is rejected at mount time by the kernel.\nt\n', 2,
             'A duplicate device id is rejected at mount time')


@shape('A11-off-topic-quote-with-token', 'refuse', 'semantic', ['D03'])
def _(f, rw):
    r = row(rw, 'D03')
    set_snap(f, r, 'h\nFor usage of the device scan command see the manual page.\nt\n', 2,
             'For usage of the device scan command see the manual page')


@shape('A12-hollow-12-word-statement', 'refuse', 'semantic', ['D01'])
def _(f, rw):
    row(rw, 'D01')['statement'] = 'a a a a a a a a a a a a'


@shape('A13-crlf-snapshot', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    f[r['snapshot']] = f[r['snapshot']].replace('\n', '\r\n')


@shape('A14a-bom-snapshot-quote-on-line-1', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    set_snap(f, r, '\ufeffThis fixture sentence explains the unallocated behaviour of the filesystem.\nt\n', 1,
             'This fixture sentence explains the unallocated behaviour')


@shape('A14b-bom-json', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    f['__json_prefix__'] = '\ufeff'


@shape('A15a-formfeed-cite-sed-line', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')   # sed -n 3p prints the token line; counter sees it as line 4
    set_snap(f, r, 'h\nint a;\x0cint b;\nThis fixture sentence explains the unallocated behaviour.\nt\n', 3,
             'This fixture sentence explains the unallocated behaviour')


@shape('A15b-formfeed-cite-counter-line', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')   # counter accepts line 4, but sed -n 4p is 't' (verbatim-line contract fails)
    set_snap(f, r, 'h\nint a;\x0cint b;\nThis fixture sentence explains the unallocated behaviour.\nt\n', 4,
             'This fixture sentence explains the unallocated behaviour')


@shape('A16-lone-cr-cite-sed-line', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    set_snap(f, r, 'h\nold\rmac\nThis fixture sentence explains the unallocated behaviour.\nt\n', 3,
             'This fixture sentence explains the unallocated behaviour')


@shape('A17-u2028-cite-sed-line', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    set_snap(f, r, 'h\n<script>var s="a\u2028b";</script>\nThis fixture sentence explains the unallocated behaviour.\nt\n', 3,
             'This fixture sentence explains the unallocated behaviour')


@shape('A18-verbatim-kernel-c-line-global_rsv', 'accept', 'mechanical', ['D02'])
def _(f, rw):
    r = row(rw, 'D02')   # S159-space-info.c:1118 shape
    set_snap(f, r, 'h\n\tif (global_rsv->reserved < global_rsv->size)\n\t\treturn;\n', 2,
             'if (global_rsv->reserved < global_rsv->size)')


@shape('A19a-verbatim-html-entity-quote', 'accept', 'mechanical', ['D05'])
def _(f, rw):
    r = row(rw, 'D05')
    set_snap(f, r, 'h\n<p>Block groups below the threshold are reclaim candidates &amp; get relocated.</p>\nt\n', 2,
             'Block groups below the threshold are reclaim candidates &amp; get relocated.')


@shape('A19b-unescaped-quote-not-verbatim', 'refuse', 'mechanical', ['D05'])
def _(f, rw):
    r = row(rw, 'D05')   # counter-accepted, but `sed -n 2p | grep -cF` gives 0
    set_snap(f, r, 'h\n<p>Block groups below the threshold are reclaim candidates &amp; get relocated.</p>\nt\n', 2,
             'Block groups below the threshold are reclaim candidates & get relocated.')


@shape('A20-verbatim-sysfs-path-angle-placeholder', 'accept', 'mechanical', ['D06'])
def _(f, rw):
    r = row(rw, 'D06')   # S158-sysfs.c:1064 shape
    set_snap(f, r, '/*\n * Path: /sys/fs/btrfs/<uuid>/allocation/\n */\n', 2, '* Path: /sys/fs/btrfs/<uuid>/allocation/')


@shape('A21-snapshot-symlink-outside-tree', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    with open(OUTSIDE, 'w') as fh:
        fh.write(f[r['snapshot']])
    f[r['snapshot']] = ('symlink', OUTSIDE)


@shape('A22-snapshot-symlink-to-sibling-in-evidence', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    f[EV + '/real.txt'] = f[r['snapshot']]
    f[r['snapshot']] = ('symlink', 'real.txt')
    f['__symlink_sha_of__'] = (r['source'], EV + '/real.txt')


@shape('A23-fabricated-snapshot-self-consistent', 'refuse', 'semantic', ['D01'])
def _(f, rw):
    r = row(rw, 'D01')
    set_snap(f, r, 'Fetched from https://btrfs.readthedocs.io/ (claimed)\nBtrfs keeps all unallocated space reserved for the global reserve forever.\n', 2,
             'Btrfs keeps all unallocated space reserved for the global reserve forever')


# --- host (R8)
@shape('H01-value-is-date-component', 'refuse', 'mechanical', ['D08'])
def _(f, rw):
    r = row(rw, 'D08')
    f[r['capture']] = '# captured 2026-10-22T21:13Z from /sys/fs/btrfs/<uuid>/allocation\nvalue 1007 bytes\n'
    r.update(capture_line=1, value='2026')
    r['statement'] = 'The host metadata block groups were sampled read-only from sysfs and held 2026 units at capture time.'
    skill_line(f, 'D08', lambda l: [l.replace('1007', '2026')])


@shape('H02-value-is-grep-n-line-number', 'refuse', 'mechanical', ['D09'])
def _(f, rw):
    r = row(rw, 'D09')
    f[r['capture']] = '# capture\n7:/sys/fs/btrfs/x/allocation/data/total_bytes:1008\n'
    r.update(capture_line=2, value='7')
    r['statement'] = 'The host data block groups were sampled read-only from sysfs and totalled 7 units at capture time.'
    skill_line(f, 'D09', lambda l: [l.replace('1008', '7')])


@shape('H03-statement-has-value-only-inside-other-number', 'refuse', 'mechanical', ['D08'])
def _(f, rw):
    r = row(rw, 'D08')
    f[r['capture']] = '# capture\nvalue 100 bytes\n'
    r['value'] = '100'
    r['statement'] = 'The host metadata block groups were sampled read-only from sysfs and held 1000000 bytes at capture time.'
    skill_line(f, 'D08', lambda l: [l.replace('1007', '100')])


@shape('H04-global_rsv-value-from-data-line', 'refuse', 'mechanical', ['D10'])
def _(f, rw):
    r = row(rw, 'D10')
    f[r['capture']] = ('/sys/fs/btrfs/u/allocation/global_rsv_size:536870912\n'
                       '/sys/fs/btrfs/u/allocation/data/total_bytes:1009\n')
    r['capture_line'] = 2


@shape('H05-three-host-rows-share-one-capture-line', 'refuse', 'mechanical', ['D08', 'D09', 'D10'])
def _(f, rw):
    cap = row(rw, 'D08')['capture']
    f[cap] = '# shared\nvalue 1007 bytes\n'
    for rid in ('D09', 'D10'):
        r = row(rw, rid)
        old = r['value']
        f.pop(r['capture'])
        r.update(capture=cap, capture_line=2, value='1007', statement=r['statement'].replace(old, '1007'))
        skill_line(f, rid, lambda l, o=old: [l.replace(o, '1007')])


@shape('H06-capture-is-a-doc-snapshot-not-host', 'refuse', 'semantic', ['D10'])
def _(f, rw):
    r = row(rw, 'D10')
    f.pop(r['capture'])
    doc = row(rw, 'D01')['snapshot']
    f[doc] = f[doc].replace('trailer line', 'Example output: Global reserve: 1009 MiB')
    r.update(capture=doc, capture_line=3)


# --- SKILL.md (R9)
@shape('K01a-trailing-comment-on-marker-line', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    skill_line(f, 'D01', lambda l: [l + ' <!-- reviewed r30 -->'])


@shape('K01b-trailing-empty-comment-on-marker-line', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    skill_line(f, 'D01', lambda l: [l + ' <!-->'])


@shape('K02-code-span-comment-opener-in-prose-before-table', 'accept', 'mechanical', ['D01', 'D05', 'D10'])
def _(f, rw):
    f['SKILL.md'] = f['SKILL.md'].replace('# SKILL\n', '# SKILL\n\nNever write `<!--` inside a table cell.\n', 1)


@shape('K03a-details-block-blank-line-table', 'accept', 'semantic', ['D01'])
def _(f, rw):
    move_marker_to_end(f, 'D01', lambda m: ['<details><summary>more</summary>', '', '| id | statement | source |',
                                            '|---|---|---|', m, '', '</details>'])


@shape('K03b-details-block-no-blank-line-raw-html', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    move_marker_to_end(f, 'D01', lambda m: ['<details>', '| id | statement | source |', '|---|---|---|', m, '</details>'])


@shape('K04-setext-heading-marker', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    move_marker_to_end(f, 'D01', lambda m: [m, '==='])


@shape('K05-lone-marker-paragraph-no-table', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    move_marker_to_end(f, 'D01', lambda m: ['Some prose.', m, 'More prose.'])


@shape('K06-marker-in-second-table-withdrawn-section', 'refuse', 'semantic', ['D01'])
def _(f, rw):
    move_marker_to_end(f, 'D01', lambda m: ['## Withdrawn rows (do not use)', '', '| id | statement | source |',
                                            '|---|---|---|', m])


@shape('K07-fence-closer-indented-4-hidden-in-code', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    move_marker_to_end(f, 'D01', lambda m: ['```', '    ```', m, '```'])


@shape('K08-fence-closer-with-formfeed-hidden-in-code', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    move_marker_to_end(f, 'D01', lambda m: ['```', '```\x0c', m, '```'])


@shape('K09-script-block-hidden', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    move_marker_to_end(f, 'D01', lambda m: ['<script type="text/plain">', m, '</script>'])


@shape('K10-processing-instruction-hidden', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    move_marker_to_end(f, 'D01', lambda m: ['<?hidden', m, '?>'])


@shape('K11-cdata-hidden', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    move_marker_to_end(f, 'D01', lambda m: ['<![CDATA[', m, ']]>'])


@shape('K12-backtick-info-string-not-a-fence', 'accept', 'mechanical', ['D01', 'D05', 'D10'])
def _(f, rw):
    f['SKILL.md'] = f['SKILL.md'].replace('# SKILL\n', '# SKILL\n\n```a`b is inline, not a fence\n', 1)


@shape('K13-indented-code-containing-fence-text', 'accept', 'mechanical', ['D01', 'D05', 'D10'])
def _(f, rw):
    f['SKILL.md'] = f['SKILL.md'].replace('# SKILL\n', '# SKILL\n\nExample source:\n\n    ```bash\n    echo hi\n\n', 1)


@shape('K14-marker-nbsp-after-id', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    skill_line(f, 'D01', lambda l: [l.replace('[R30-D01] ', '[R30-D01]\u00a0')])


# --- JSON (R1/R2)
@shape('J01-hidden-zero-width-id-row-withdrawal', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    x = copy.deepcopy(row(rw, 'D01'))
    x['id'] = 'D01\u200b'
    x['statement'] = 'WITHDRAWN: this row supersedes D01; the D01 claim is wrong and must not be used by agents.'
    rw.append(x)


@shape('J02-top-level-withdrawn-key', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    f['__json_extra__'] = {'withdrawn': ['D01'], 'status': 'superseded'}


@shape('J03-non-dict-row-note', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    rw.append('D01 is withdrawn; see errata')


@shape('J04-id-escaped-unicode-same-id', 'accept', 'mechanical', ['D01'])
def _(f, rw):
    f['__json_escape_id__'] = True


# --- registry (R4)
@shape('R01-registry-row-inside-fenced-code', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    move_reg_to_end(f, 'S900', lambda m: ['Example of the format:', '', '```', m, '```'])


@shape('R02-registry-row-inside-html-comment', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    move_reg_to_end(f, 'S900', lambda m: ['<!--', m, '-->'])


@shape('R03-registry-row-in-second-table-rejected-section', 'refuse', 'semantic', ['D01'])
def _(f, rw):
    move_reg_to_end(f, 'S900', lambda m: ['## Rejected candidates (round 30)', '', bat.HEADER.rstrip('\n'), m])


@shape('R04-registry-row-second-table-different-columns', 'refuse', 'mechanical', ['D01'])
def _(f, rw):
    # header says column 8 is "reviewer verdict", not status; counter reads positions only
    move_reg_to_end(f, 'S900', lambda m: ['## Reviewer verdicts', '',
                                          '| id | source | kind | tier | scope | anchor | teaches | verdict-word | date | recheck | used-by |',
                                          '|---|---|---|---|---|---|---|---|---|---|---|', m])


def materialize(d, files, rows):
    jp = files.pop('__json_prefix__', '')
    extra = files.pop('__json_extra__', None)
    esc = files.pop('__json_escape_id__', None)
    symsha = files.pop('__symlink_sha_of__', None)
    resync(files, rows)
    if symsha:
        sid, real = symsha
        lines, i = reg_line(files, sid)
        lines[i] = re.sub(r'sha256 [0-9a-f]{64}', 'sha256 ' + hashlib.sha256(b(files[real])).hexdigest(), lines[i])
        files['corpus/SOURCES.md'] = '\n'.join(lines)
    doc = {'rows': rows}
    if extra:
        doc.update(extra)
    text = json.dumps(doc, indent=1)
    if esc:
        text = text.replace('"id": "D01"', '"id": "\\u0044\\u0030\\u0031"', 1)
    files[JSON] = jp + text
    for path, c in files.items():
        full = os.path.join(d, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        if isinstance(c, tuple):
            os.symlink(c[1], full)
        else:
            with open(full, 'wb') as fh:
                fh.write(b(c))


def run(d, bs):
    p = subprocess.run([sys.executable, COUNTER, '--tree', d, '--base-sources', bs], capture_output=True, text=True,
                       env={k: v for k, v in os.environ.items() if not k.startswith('GIT_')}, timeout=60)
    out = [json.loads(l) for l in p.stdout.splitlines() if l.startswith('{')]
    return {o['id']: o for o in out if 'id' in o}, out[-1] if out else {}, p.returncode


def render(d):
    p = subprocess.run(['cmark', '--unsafe', os.path.join(d, 'SKILL.md')], capture_output=True, text=True)
    html = p.stdout
    i = html.find('R30-D01')
    ctx = html[max(0, i - 160):i + 80] if i >= 0 else '(R30-D01 not in output)'
    return ctx


def main():
    work = os.path.join(OUT, 'work')
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    bs = os.path.join(work, 'base-sources.md')
    with open(bs, 'w') as fh:
        fh.write('# base\n\n' + bat.HEADER)
    results = []
    f0, r0 = bat.base_fixture()
    d = os.path.join(work, 'CONTROL')
    materialize(d, f0, r0)
    per, summ, rc = run(d, bs)
    results.append({'shape': 'CONTROL', 'verified': summ.get('verified'), 'rc': rc})
    print(json.dumps(results[-1]))
    for name, expected, catch, targets, fn in SH:
        files, rows = bat.base_fixture()
        fn(files, rows)
        d = os.path.join(work, name)
        materialize(d, files, rows)
        per, summ, rc = run(d, bs)
        tv = {t: per.get(t, {}).get('verified') for t in targets}
        accepted = all(tv.values())
        others_ok = summ.get('verified') == 10 if expected == 'accept' else None
        verdict_ok = (accepted and summ.get('verified') == 10) if expected == 'accept' else (not accepted)
        res = {'shape': name, 'expected': expected, 'catch': catch, 'targets': tv,
               'counter': 'ACCEPTED' if accepted else 'REFUSED', 'total_verified': summ.get('verified'),
               'counter_correct': verdict_ok,
               'failures': {t: per.get(t, {}).get('failures') for t in targets if per.get(t, {}).get('failures')}}
        if name.startswith('K'):
            res['cmark_context'] = render(d)
        results.append(res)
        print(json.dumps(res, ensure_ascii=True))
    bad = [r['shape'] for r in results[1:] if not r['counter_correct']]
    print(json.dumps({'control': results[0]['verified'], 'shapes': len(SH),
                      'misjudged': len(bad), 'misjudged_shapes': bad,
                      'should_fail_accepted': [r['shape'] for r in results[1:] if r['expected'] == 'refuse' and r['counter'] == 'ACCEPTED'],
                      'should_pass_refused': [r['shape'] for r in results[1:] if r['expected'] == 'accept' and not r['counter_correct']],
                      'counter_sha256': hashlib.sha256(open(COUNTER, 'rb').read()).hexdigest()}))


if __name__ == '__main__':
    main()
