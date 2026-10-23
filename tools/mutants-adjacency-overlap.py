#!/usr/bin/env python3
"""Should-fail register battery for tools/check-adjacency-overlap.py (round 28, claim C1). Every subprocess follows the round-32 child-environment allow-list: no ambient name is copied into a child, user configuration is isolated, HOME is private, PATH is fixed, and repository discovery is sandbox-ceilinged.

Origin: round-27 wave-2 seat CritC2Tool's driver (`.ufo/waves/round-27/w2a2/CritC2Tool.md`),
made reproducible from committed bytes: the lane data is `git archive <--base>` into a private
temporary sandbox repo (never the lane), and the counter is the blob
`<--counter-rev>:tools/check-adjacency-overlap.py`. Each mutant is committed in the sandbox and
counted twice: with the live sibling root and with an empty sibling root.

A should-fail mutant is ACCEPTED when either run exits 0 with anchored_rows 6. The summary line
(last line of stdout, JSON) carries `should_fail_total` and `should_fail_accepted`.

Usage: python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> | --counter-file <path>) [--lane <repo>]
Read-only on the lane; writes only under a fresh tempfile.mkdtemp() directory, removed at exit.
"""
import argparse, atexit, copy, hashlib, io, json, os, shutil, subprocess, sys, tarfile, tempfile

# round-32 child-environment allow-list: a child environment is built from this base plus the
# names this builder sets on purpose; no ambient name is copied.
CHILD_ENV_BASE = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}


def clean_env():
    env = dict(CHILD_ENV_BASE)
    env.update({
        'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_SYSTEM': os.devnull,
        'HOME': HOME, 'XDG_CONFIG_HOME': os.path.join(HOME, '.config'),
        'PATH': '/usr/bin:/bin', 'GIT_CEILING_DIRECTORIES': os.path.dirname(ROOT),
    })
    return env

_ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
_ap.add_argument('--base', required=True)
_g = _ap.add_mutually_exclusive_group(required=True)
_g.add_argument('--counter-rev', help='lane revision whose tools/check-adjacency-overlap.py is counted')
_g.add_argument('--counter-file', help='a counter file on disk (mutation testing only)')
_ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ap.add_argument('--siblings-root', default='/home/vgpnk/Projects/shokunin')
_ap.add_argument('--keep', action='store_true', help='keep the temporary sandbox')
ARGS = _ap.parse_args()

ROOT = tempfile.mkdtemp(prefix='mut-adj-')
HOME = os.path.join(ROOT, 'home')
os.mkdir(HOME)
if not ARGS.keep:
    atexit.register(shutil.rmtree, ROOT, True)
TREE = ROOT + '/tree'
SBX = ROOT + '/sbx'
NOSIB = ROOT + '/nosib'
REALSIB = ARGS.siblings_root
TOOL = ROOT + '/counter/check-adjacency-overlap.py'
REG = 'corpus/knowledge/adjacency-mori-oom-r27.json'
SNAP = '.ufo/waves/round-27/siblings/mori/corpus/knowledge/userspace-oom-killers-r26.md'
SNAPDIR = '.ufo/waves/round-27/siblings/mori/'
MORI = os.path.join(REALSIB, 'mori-shokunin')
PIN = 'ef9dbee136d6ed2ef98687f5cb0c0a16506a5155'


def _export():
    lane = ARGS.lane
    rev = subprocess.run(['git', '-C', lane, 'rev-parse', '--verify', ARGS.base + '^{commit}'],
                         capture_output=True, text=True, check=True, env=clean_env()).stdout.strip()
    tar = subprocess.run(['git', '-C', lane, 'archive', rev],
                         capture_output=True, check=True, env=clean_env()).stdout
    os.makedirs(TREE)
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        t.extractall(TREE, filter='data')
    if ARGS.counter_file:
        with open(ARGS.counter_file, 'rb') as fh:
            blob = fh.read()
    else:
        blob = subprocess.run(['git', '-C', lane, 'show', ARGS.counter_rev + ':tools/check-adjacency-overlap.py'],
                              capture_output=True, check=True, env=clean_env()).stdout
    os.makedirs(os.path.dirname(TOOL))
    with open(TOOL, 'wb') as fh:
        fh.write(blob)
    return rev, hashlib.sha256(blob).hexdigest()


BASE_REV, COUNTER_SHA = _export()
RESULTS = []


def sh(*a, cwd=None):
    return subprocess.run(list(a), cwd=cwd, capture_output=True, env=clean_env())


def g(*a):
    r = sh('git', '-C', SBX, *a)
    if r.returncode:
        raise SystemExit(r.stderr.decode())
    return r.stdout.decode().strip()


def setup():
    if not os.path.isdir(SBX + '/.git'):
        shutil.copytree(TREE, SBX, symlinks=True)
        g('init', '-q')
        g('add', '-A', '-f')
        g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'base export ' + BASE_REV)
    os.makedirs(NOSIB, exist_ok=True)
    return g('rev-parse', 'HEAD')


def read(path):
    with open(os.path.join(TREE, path), 'rb') as fh:
        return fh.read()


def run(base, name, mutate, kind, note):
    g('checkout', '-q', '-f', '--detach', base)
    g('clean', '-fdqx')
    reg = json.loads(read(REG))
    files = {}
    mutate(reg, files)
    files.setdefault(REG, (json.dumps(reg, ensure_ascii=False, indent=1) + '\n').encode())
    for p, b in files.items():
        full = os.path.join(SBX, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(b if isinstance(b, bytes) else b.encode())
    g('add', '-A', '-f')
    g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', name, '--allow-empty')
    rev = g('rev-parse', 'HEAD')
    out = {}
    for label, sib in (('live-mori', REALSIB), ('no-sibling', NOSIB)):
        r = sh('python3', TOOL, '--repo', SBX, '--revision', rev, '--siblings-root', sib)
        try:
            j = json.loads(r.stdout.decode())
            rows = j.get('rows', {})
            bad = {k: v for k, v in rows.items() if v} if isinstance(rows, dict) else rows
            out[label] = {'exit': r.returncode, 'anchored_rows': j.get('anchored_rows'),
                          'sibling_check': j.get('sibling_check'), 'failing': bad,
                          'finding': j.get('finding')}
        except Exception:
            out[label] = {'exit': r.returncode, 'anchored_rows': None,
                          'stderr_tail': r.stderr.decode().strip().splitlines()[-1:]}
    accepted = any(o.get('exit') == 0 and o.get('anchored_rows') == 6 for o in out.values())
    rec = {'mutant': name, 'kind': kind, 'accepted': accepted, 'note': note, **out}
    RESULTS.append(rec)
    print(json.dumps(rec, ensure_ascii=False))


def row(reg, rid):
    return next(r for r in reg['rows'] if r['id'] == rid)


snap_bytes = read(SNAP)
snap_lines = snap_bytes.decode().split('\n')
FACTS_LINE = snap_lines.index('## Facts') + 1


def m_wrong_class(reg, f):
    row(reg, 'OV1')['class'] = 'CONFLICTS'
    row(reg, 'OV3')['class'] = 'INBOUND-DRIFTED'
    row(reg, 'OV5')['owner'] = 'contested'


def m_lane_from_register(reg, f):
    r = row(reg, 'OV3')
    r['lane_path'] = REG
    r['lane_quote'] = 'Record agreement.'


def m_lane_from_ufo(reg, f):
    r = row(reg, 'OV4')
    r['lane_path'] = '.ufo/waves/round-27/w1/CritAdjacencyMove.md'
    text = read(r['lane_path']).decode()
    words = ' '.join(text.split()).split(' ')
    r['lane_quote'] = ' '.join(words[20:30])


def m_lane_from_mori_snapshot(reg, f):
    r = row(reg, 'OV3')
    r['lane_path'] = SNAP
    r['lane_quote'] = r['quote']


def m_quote_is_heading(reg, f):
    r = row(reg, 'OV2')
    r['quote_line'] = FACTS_LINE
    r['quote'] = '## Facts'


def m_six_lane_gap(reg, f):
    for r in reg['rows']:
        r['lane_path'] = r['lane_quote'] = None
        r['class'] = 'LANE-GAP'


def m_dotdot(reg, f):
    row(reg, 'OV1')['sibling_path'] = 'corpus/knowledge/../knowledge/userspace-oom-killers-r26.md'


def m_double_slash(reg, f):
    row(reg, 'OV1')['sibling_path'] = 'corpus//knowledge/userspace-oom-killers-r26.md'


def m_dot_segment(reg, f):
    row(reg, 'OV1')['sibling_path'] = 'corpus/./knowledge/userspace-oom-killers-r26.md'


FAKE = ('# Invented mori entry\n\n## Facts\nmori says the lane is wrong about everything here\n'
        'and nobody can check this sentence\n').encode()


def m_fabricated_snapshot(reg, f):
    p = 'corpus/knowledge/invented-r26.md'
    f[SNAPDIR + p] = FAKE
    r = row(reg, 'OV6')
    r.update(sibling_path=p, sibling_blob_sha256=hashlib.sha256(FAKE).hexdigest(), heading='## Facts',
             quote='mori says the lane is wrong about everything', quote_line=4)


def m_fabricated_at_pin_path_name_variant(reg, f):
    p = 'corpus/knowledge/userspace-oom-killers-r26.md.orig'
    f[SNAPDIR + p] = FAKE
    r = row(reg, 'OV6')
    r.update(sibling_path=p, sibling_blob_sha256=hashlib.sha256(FAKE).hexdigest(), heading='## Facts',
             quote='mori says the lane is wrong about everything', quote_line=4)


def m_other_real_mori_file(reg, f):
    p = 'corpus/knowledge/audit-r11.md'
    b = sh('git', '-C', MORI, 'cat-file', '-p', '%s:%s' % (PIN, p)).stdout
    f[SNAPDIR + p] = b
    lines = b.decode().split('\n')
    hi = next(i for i, l in enumerate(lines) if l.startswith('#'))
    qi = next(i for i in range(hi + 1, len(lines)) if len(lines[i].split()) >= 4 and not lines[i].startswith('#'))
    head = next(lines[i] for i in range(qi, -1, -1) if lines[i].startswith('#'))
    r = row(reg, 'OV6')
    r.update(sibling_path=p, sibling_blob_sha256=hashlib.sha256(b).hexdigest(), heading=head,
             quote=' '.join(lines[qi].split()[:4]), quote_line=qi + 1)


def m_extra_row_ov7(reg, f):
    x = copy.deepcopy(row(reg, 'OV1'))
    x.update(id='OV7', **{'class': 'MAYBE'}, owner='nobody', action='')
    reg['rows'].append(x)


def m_extra_row_trailing_space_id(reg, f):
    x = copy.deepcopy(row(reg, 'OV4'))
    x.update(id='OV4 ', **{'class': 'AGREES'}, action='contradicts OV4')
    reg['rows'].append(x)


def m_extra_nondict(reg, f):
    reg['rows'].append('junk row')
    reg['rows'].append(None)


def m_unhashable_id(reg, f):
    x = copy.deepcopy(row(reg, 'OV1'))
    x['id'] = ['OV1']
    reg['rows'].append(x)


def m_one_char_lane_quote(reg, f):
    row(reg, 'OV1')['lane_quote'] = '.'
    row(reg, 'OV2')['lane_quote'] = 'a'


def m_one_word_quote(reg, f):
    row(reg, 'OV1')['quote'] = 'the'


def m_lanegap_with_lane(reg, f):
    row(reg, 'OV3')['class'] = 'LANE-GAP'


def m_snapshot_field_bogus(reg, f):
    for r in reg['rows']:
        r['snapshot'] = '/etc/passwd'


def province_with(fn):
    p = read('PROVINCE.md').decode()
    return fn(p).encode()


def m_province_fenced(reg, f):
    def fn(p):
        out = []
        for l in p.split('\n'):
            if l.startswith('| OV'):
                continue
            out.append(l)
            if l.startswith('| id | owner | class'):
                pass
        p = '\n'.join(out)
        sec = '## Adjacent — mori userspace OOM killers (round 27)'
        block = '\n```text\n' + ''.join('| OV%d | not a table row\n' % i for i in range(1, 7)) + '```\n'
        return p.replace(sec + '\n', sec + '\n' + block, 1)
    f['PROVINCE.md'] = province_with(fn)


def m_province_contradicts(reg, f):
    def fn(p):
        return p.replace('| OV3 | tsukuroi | AGREES |', '| OV3 | mori | CONFLICTS |').replace(
            '| OV6 | mori | LANE-GAP |', '| OV6 | tsukuroi | AGREES |')
    f['PROVINCE.md'] = province_with(fn)


def m_row_missing(reg, f):
    reg['rows'] = [r for r in reg['rows'] if r['id'] != 'OV6']


def m_quote_crosses_section(reg, f):
    # quote_line = last Facts line; window runs into the Decision table heading
    i = FACTS_LINE
    dt = snap_lines.index('## Decision table') + 1
    r = row(reg, 'OV2')
    r['quote_line'] = dt - 1
    r['heading'] = '## Facts'
    r['quote'] = ' '.join((' '.join(snap_lines[dt - 2:dt + 1])).split()[-6:])


def p_upper_sha(reg, f):
    r = row(reg, 'OV1')
    r['sibling_blob_sha256'] = r['sibling_blob_sha256'].upper()


def p_province_backtick(reg, f):
    f['PROVINCE.md'] = province_with(lambda p: p.replace('| OV1 |', '| `OV1` |'))


def p_province_indent(reg, f):
    f['PROVINCE.md'] = province_with(lambda p: p.replace('\n| OV1 |', '\n  | OV1 |'))


def p_province_no_leading_pipe(reg, f):
    f['PROVINCE.md'] = province_with(lambda p: p.replace('\n| OV1 |', '\nOV1 |'))


def p_crlf_snapshot(reg, f):
    p = 'corpus/knowledge/crlf-r26.md'
    b = FAKE.replace(b'\n', b'\r\n')
    f[SNAPDIR + p] = b
    r = row(reg, 'OV6')
    r.update(sibling_path=p, sibling_blob_sha256=hashlib.sha256(b).hexdigest(), heading='## Facts',
             quote='mori says the lane is wrong about everything', quote_line=4)


def p_bom(reg, f):
    f[REG] = b'\xef\xbb\xbf' + (json.dumps(reg, ensure_ascii=False, indent=1) + '\n').encode()


def p_heading_trailing_space_in_row(reg, f):
    row(reg, 'OV1')['heading'] = '## Facts '


def control(reg, f):
    pass


def m_altered_pin(reg, f):
    b = snap_bytes.replace(b'## Limits', b'## Limits (edited)')
    f[SNAP] = b
    for r in reg['rows']:
        r['sibling_blob_sha256'] = hashlib.sha256(b).hexdigest()


MUTANTS = [
    ('control-unchanged', control, 'control', 'unchanged export'),
    ('wrong-class-and-owner', m_wrong_class, 'should-fail', 'OV1 CONFLICTS, OV3 INBOUND-DRIFTED, OV5 owner contested'),
    ('lane-quote-from-register', m_lane_from_register, 'should-fail', 'OV3 lane_path = the register itself, lane_quote = its own action text'),
    ('lane-quote-from-ufo-report', m_lane_from_ufo, 'should-fail', 'OV4 lane_path = .ufo/waves/round-27/w1/CritAdjacencyMove.md'),
    ('lane-quote-from-mori-snapshot', m_lane_from_mori_snapshot, 'should-fail', 'OV3 lane_path = the committed mori snapshot, lane_quote = the mori quote'),
    ('quote-line-at-heading', m_quote_is_heading, 'should-fail', 'OV2 quote_line = the ## Facts line, quote = "## Facts"'),
    ('quote-window-crosses-section', m_quote_crosses_section, 'should-fail', 'OV2 quote_line = line above ## Decision table, quote includes that heading, heading field ## Facts'),
    ('six-lane-gap', m_six_lane_gap, 'should-fail', 'all six rows lane null, class LANE-GAP'),
    ('lanegap-class-with-lane-side', m_lanegap_with_lane, 'should-fail', 'OV3 class LANE-GAP while its lane quote is found'),
    ('one-char-lane-quote', m_one_char_lane_quote, 'should-fail', 'OV1 lane_quote ".", OV2 lane_quote "a"'),
    ('one-word-sibling-quote', m_one_word_quote, 'should-fail', 'OV1 quote "the"'),
    ('sibling-path-dotdot', m_dotdot, 'should-fail', 'OV1 sibling_path corpus/knowledge/../knowledge/...'),
    ('sibling-path-double-slash', m_double_slash, 'should-fail', 'OV1 sibling_path corpus//knowledge/...'),
    ('sibling-path-dot-segment', m_dot_segment, 'should-fail', 'OV1 sibling_path corpus/./knowledge/...'),
    ('fabricated-snapshot-other-path', m_fabricated_snapshot, 'should-fail', 'OV6 points at an invented committed snapshot invented-r26.md'),
    ('fabricated-snapshot-pin-name-variant', m_fabricated_at_pin_path_name_variant, 'should-fail', 'OV6 points at invented bytes at userspace-oom-killers-r26.md.orig'),
    ('other-real-mori-file', m_other_real_mori_file, 'should-fail', 'OV6 anchored in mori audit-r11.md at the pin, not the declared entry'),
    ('extra-row-ov7', m_extra_row_ov7, 'should-fail', '7th row id OV7 with invalid class, owner, empty action'),
    ('extra-row-id-trailing-space', m_extra_row_trailing_space_id, 'should-fail', '7th row id "OV4 " contradicting OV4'),
    ('extra-non-dict-rows', m_extra_nondict, 'should-fail', 'rows gain "junk row" and null'),
    ('unhashable-id-row', m_unhashable_id, 'should-fail', '7th row with id ["OV1"]'),
    ('snapshot-field-bogus', m_snapshot_field_bogus, 'should-fail', 'every row snapshot field = /etc/passwd'),
    ('province-ids-in-code-fence', m_province_fenced, 'should-fail', 'PROVINCE OV rows moved into a fenced text block'),
    ('province-contradicts-register', m_province_contradicts, 'should-fail', 'PROVINCE OV3 mori CONFLICTS and OV6 tsukuroi AGREES'),
    ('row-missing-ov6', m_row_missing, 'divergence', 'register lacks OV6 (rule: holds exactly OV1-OV6)'),
    ('upper-case-sha256', p_upper_sha, 'should-pass', 'OV1 sibling_blob_sha256 upper-case hex of the same digest'),
    ('province-backticked-id', p_province_backtick, 'should-pass', 'PROVINCE cell `OV1`'),
    ('province-indented-row', p_province_indent, 'should-pass', 'PROVINCE OV1 row indented two spaces'),
    ('province-no-leading-pipe', p_province_no_leading_pipe, 'should-pass', 'PROVINCE OV1 row without leading pipe'),
    ('crlf-snapshot', p_crlf_snapshot, 'should-pass', 'OV6 snapshot with CRLF line ends, heading "## Facts"'),
    ('register-utf8-bom', p_bom, 'should-pass', 'register bytes start with a UTF-8 BOM'),
    ('heading-trailing-space-in-row', p_heading_trailing_space_in_row, 'should-pass?', 'OV1 heading "## Facts " (trailing space)'),
    ('altered-pinned-snapshot', m_altered_pin, 'should-fail', 'pinned-path snapshot edited outside quote windows, row digests updated (r27 driver2)'),
]

if __name__ == '__main__':
    base = setup()
    for name, fn, kind, note in MUTANTS:
        run(base, name, fn, kind, note)
    g('checkout', '-q', '-f', '--detach', base)
    sf = [r for r in RESULTS if r['kind'] == 'should-fail']
    ctl = next(r for r in RESULTS if r['kind'] == 'control')
    print(json.dumps({
        'summary': 'mutants-adjacency-overlap', 'base': BASE_REV, 'counter_rev': ARGS.counter_rev,
        'counter_sha256': COUNTER_SHA, 'control_live_anchored_rows': ctl['live-mori'].get('anchored_rows'),
        'control_live_exit': ctl['live-mori'].get('exit'),
        'should_fail_total': len(sf), 'should_fail_accepted': sum(r['accepted'] for r in sf),
        'accepted_mutants': [r['mutant'] for r in sf if r['accepted']],
        'should_pass_accepted': sum(r['accepted'] for r in RESULTS if r['kind'] == 'should-pass'),
    }, ensure_ascii=False))
