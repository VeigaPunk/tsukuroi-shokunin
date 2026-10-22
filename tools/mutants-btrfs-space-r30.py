#!/usr/bin/env python3
"""Should-fail battery for tools/check-btrfs-space-r30.py (round 30, claim C1; QUALITY 73).

Builds, in a private temporary directory, a synthetic fixture tree in which all ten rows
D01-D10 verify (the CONTROL must read 10), then applies one mutation per shape and runs the
counter in fixture mode (`--tree`, `--base-sources`). A SHOULD-FAIL shape is ACCEPTED when its
targeted row still verifies; a SHOULD-PASS shape is REFUSED when any row stops verifying.
No git is run, so no inherited git environment can reach the counter.

The shapes come from the round-27 to round-29 counter attacks (CritOwedCounterShapes,
CritOwedV2Shapes, ResRevV3Counter, the round-29 spot-check routed defect 2): extra JSON keys
such as `"status": "withdrawn"`, duplicate keys and ids, markers in fences, comments, indented
or list-prefixed code, italic, bold or look-alike ids, quotes off the cited line, sources
that are not new, not mined or not opened this round, snapshots outside the evidence tree, and
host values missing from the capture.

Usage: python3 tools/mutants-btrfs-space-r30.py [--counter <path>] [--keep]
Output: one JSON line per shape, then a summary JSON line with `control`,
`should_fail_accepted`, `should_fail_total`, `should_pass_refused`, `should_pass_total`,
`counter_sha256`.  Exit 0 when the control reads 10 and no shape is misjudged, 1 otherwise.
"""
import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EV = '.ufo/waves/round-30/fixture'
TOKENS = {'D01': 'unallocated', 'D02': 'global reserve', 'D03': 'usage', 'D04': 'DUP',
          'D05': 'reclaim', 'D06': 'allocation', 'D07': 'snapshot', 'D08': 'metadata',
          'D09': 'data', 'D10': 'global_rsv'}
HOST = ('D08', 'D09', 'D10')
HEADER = ('| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
          '|---|---|---|---|---|---|---|---|---|---|---|\n')


def base_fixture():
    files, rows, reg = {}, [], []
    for i, (rid, tok) in enumerate(sorted(TOKENS.items())):
        sid = 'S9%02d' % i
        snap = '%s/%s.txt' % (EV, sid)
        text = ('header line for %s\n' % sid +
                'This fixture sentence explains the %s behaviour of the filesystem in detail.\n' % tok +
                'trailer line\n')
        files[snap] = text
        sha = hashlib.sha256(text.encode()).hexdigest()
        reg.append('| %s | Fixture source %s | docs | A | scope | sha256 %s | teaches | mined | 2026-10-22 | on-release | SKILL.md |'
                   % (sid, sid, sha))
        row = {'id': rid, 'statement': 'The fixture statement for row %s says one concrete thing about btrfs space use here.' % rid,
               'source': sid, 'snapshot': snap, 'line': 2,
               'quote': 'explains the %s behaviour of the filesystem' % tok}
        if rid in HOST:
            cap = '%s/capture-%s.txt' % (EV, rid)
            files[cap] = '# capture for %s\nvalue %d bytes\n' % (rid, 1000 + i)
            row.update({'capture': cap, 'capture_line': 2, 'value': str(1000 + i)})
            row['statement'] += ' The host value was %s bytes at capture time.' % row['value']
        rows.append(row)
    files['corpus/SOURCES.md'] = '# SOURCES\n\n' + HEADER + '\n'.join(reg) + '\n'
    skill = ['# SKILL', '', '| id | statement | source |', '|---|---|---|']
    for r in rows:
        extra = (' value ' + r['value']) if 'value' in r else ''
        skill.append('| [R30-%s] | statement%s | %s |' % (r['id'], extra, r['source']))
    files['SKILL.md'] = '\n'.join(skill) + '\n'
    return files, rows


def dump(rows):
    return json.dumps({'rows': rows}, indent=1)


def row(rows, rid):
    return next(r for r in rows if r['id'] == rid)


def sub_skill(files, old, new):
    assert old in files['SKILL.md'], old
    files['SKILL.md'] = files['SKILL.md'].replace(old, new)


def m_skill_line(rid, fn):
    def f(files, rows):
        lines = files['SKILL.md'].split('\n')
        i = next(k for k, l in enumerate(lines) if l.startswith('| [R30-%s] ' % rid))
        lines[i:i + 1] = fn(lines[i])
        files['SKILL.md'] = '\n'.join(lines)
    return f


def m_row(rid, fn):
    def f(files, rows):
        fn(row(rows, rid), files)
    return f


def set_reg(sid, old, new):
    def f(files, rows):
        lines = files['corpus/SOURCES.md'].split('\n')
        i = next(k for k, l in enumerate(lines) if l.startswith('| %s |' % sid))
        assert old in lines[i]
        lines[i] = lines[i].replace(old, new)
        files['corpus/SOURCES.md'] = '\n'.join(lines)
    return f


def snap_edit(rid, fn):
    def f(files, rows):
        r = row(rows, rid)
        files[r['snapshot']] = fn(files[r['snapshot']])
    return f


def reuse_line(files, rows):
    """D02 cites the same snapshot line as D01; every other rule for D02 still holds."""
    d1, d2 = row(rows, 'D01'), row(rows, 'D02')
    files[d1['snapshot']] = files[d1['snapshot']].replace(
        'of the filesystem in detail.', 'of the filesystem and the global reserve behaviour in detail.')
    d2.update({'source': d1['source'], 'snapshot': d1['snapshot'], 'line': 2,
               'quote': 'and the global reserve behaviour in detail'})
    sub_skill(files, '| [R30-D02] | statement | S901 |', '| [R30-D02] | statement | S900 |')


SHOULD_FAIL = [
    ('F01-json-missing', 'D01', lambda fl, rw: fl.__setitem__('__nojson__', True)),
    ('F02-duplicate-json-key', 'D01', lambda fl, rw: fl.__setitem__('__dupkey__', True)),
    ('F03-extra-key-status-withdrawn', 'D01', m_row('D01', lambda r, fl: r.__setitem__('status', 'withdrawn'))),
    ('F04-extra-key-null', 'D02', m_row('D02', lambda r, fl: r.__setitem__('note', None))),
    ('F05-duplicate-id-row', 'D01', lambda fl, rw: rw.append(copy.deepcopy(row(rw, 'D01')))),
    ('F06-statement-11-words', 'D01', m_row('D01', lambda r, fl: r.__setitem__('statement', 'one two three four five six seven eight nine ten eleven'))),
    ('F07-source-rejected', 'D01', set_reg('S900', '| mined |', '| rejected |')),
    ('F08-source-opened-other-day', 'D01', set_reg('S900', '| 2026-10-22 |', '| 2026-10-21 |')),
    ('F09-source-at-base', 'D01', lambda fl, rw: fl.__setitem__('__base__', '| S900 | old |')),
    ('F10-snapshot-sha-absent', 'D01', lambda fl, rw: fl.__setitem__('corpus/SOURCES.md', __import__('re').sub(
        r'(\| S900 \|.*?)sha256 [0-9a-f]{64}', r'\1sha256 not-recorded', fl['corpus/SOURCES.md']))),
    ('F11-snapshot-outside-evidence', 'D01', m_row('D01', lambda r, fl: (fl.__setitem__('corpus/x.txt', fl[r['snapshot']]), r.__setitem__('snapshot', 'corpus/x.txt')))),
    ('F12-snapshot-path-traversal', 'D01', m_row('D01', lambda r, fl: r.__setitem__('snapshot', '.ufo/waves/round-30/../../SKILL.md'))),
    ('F13-quote-fabricated', 'D01', m_row('D01', lambda r, fl: r.__setitem__('quote', 'unallocated space is always reclaimed by the kernel'))),
    ('F14-quote-wrong-line', 'D01', m_row('D01', lambda r, fl: r.__setitem__('line', 3))),
    ('F15-quote-too-short', 'D01', m_row('D01', lambda r, fl: r.__setitem__('quote', 'the unallocated'))),
    ('F16-quote-lacks-token', 'D01', m_row('D01', lambda r, fl: r.__setitem__('quote', 'This fixture sentence explains the'))),
    ('F17-quote-starts-next-line', 'D01', m_row('D01', lambda r, fl: (r.__setitem__('line', 1)))),
    ('F18-cited-line-reused', 'D02', lambda fl, rw: reuse_line(fl, rw)),
    ('F19-line-as-string', 'D01', m_row('D01', lambda r, fl: r.__setitem__('line', '2'))),
    ('F20-source-id-malformed', 'D01', m_row('D01', lambda r, fl: r.__setitem__('source', 'S90'))),
    ('F21-host-value-not-on-capture', 'D08', m_row('D08', lambda r, fl: r.__setitem__('value', '999999'))),
    ('F22-host-statement-lacks-value', 'D08', m_row('D08', lambda r, fl: r.__setitem__('statement', 'The fixture statement for row D08 says one concrete thing about btrfs space use here.'))),
    ('F23-host-value-not-integer', 'D08', m_row('D08', lambda r, fl: r.__setitem__('value', 'about 1007'))),
    ('F24-host-capture-missing', 'D09', m_row('D09', lambda r, fl: r.__setitem__('capture', EV + '/nope.txt'))),
    ('F25-host-value-digit-prefix', 'D10', m_row('D10', lambda r, fl: fl.__setitem__(r['capture'], '# c\nvalue 21009 bytes\n'))),
    ('F26-marker-missing', 'D01', m_skill_line('D01', lambda l: [])),
    ('F27-marker-in-fence', 'D01', m_skill_line('D01', lambda l: ['```', l, '```'])),
    ('F28-marker-in-tilde-fence', 'D01', m_skill_line('D01', lambda l: ['~~~~', l, '~~~~'])),
    ('F29-marker-in-comment', 'D01', m_skill_line('D01', lambda l: ['<!--', l, '-->'])),
    ('F30-marker-in-comment-after-empty-comment', 'D01', m_skill_line('D01', lambda l: ['<!--> visible <!-- open', l, 'close -->'])),
    ('F31-marker-indented-code', 'D01', m_skill_line('D01', lambda l: ['    ' + l])),
    ('F32-marker-list-prefixed', 'D01', m_skill_line('D01', lambda l: ['-     ' + l])),
    ('F33-marker-blockquote', 'D01', m_skill_line('D01', lambda l: ['> ' + l])),
    ('F34-marker-italic-id', 'D01', m_skill_line('D01', lambda l: [l.replace('[R30-D01]', '*[R30-D01]*')])),
    ('F35-marker-bold-id', 'D01', m_skill_line('D01', lambda l: [l.replace('[R30-D01]', '**[R30-D01]**')])),
    ('F36-marker-unbalanced-asterisk', 'D01', m_skill_line('D01', lambda l: [l.replace('[R30-D01]', '*[R30-D01]')])),
    ('F37-marker-cyrillic-d', 'D01', m_skill_line('D01', lambda l: [l.replace('R30-D01', 'R30-\u0414' + '01')])),
    ('F38-marker-zero-width', 'D01', m_skill_line('D01', lambda l: [l.replace('R30-D01', 'R30-\u200bD01')])),
    ('F39-marker-twice', 'D01', m_skill_line('D01', lambda l: [l, l])),
    ('F40-second-mention-in-prose', 'D01', m_skill_line('D01', lambda l: [l, 'see R30-D01 above'])),
    ('F41-marker-lacks-source', 'D01', m_skill_line('D01', lambda l: [l.replace('S900', 'S-none')])),
    ('F42-marker-source-prefix-only', 'D01', m_skill_line('D01', lambda l: [l.replace('S900', 'S9001')])),
    ('F43-host-marker-lacks-value', 'D08', m_skill_line('D08', lambda l: [l.replace(' value 1007', '')])),
    ('F44-snapshot-edited-after-registry', 'D01', snap_edit('D01', lambda t: t + 'appended\n')),
    ('F45-source-row-duplicated', 'D01', lambda fl, rw: fl.__setitem__('corpus/SOURCES.md', fl['corpus/SOURCES.md'] + next(l for l in fl['corpus/SOURCES.md'].split('\n') if l.startswith('| S900 |')) + '\n')),
    ('F46-rows-not-list', 'D01', lambda fl, rw: fl.__setitem__('__rowsdict__', True)),
]

SHOULD_PASS = [
    ('P01-quote-wraps-two-lines', snap_edit('D01', lambda t: t.replace('the unallocated behaviour of the filesystem', 'the unallocated\nbehaviour of the filesystem'))),
    ('P02-html-snapshot-tags-entities', None),
    ('P03-quote-extra-whitespace', m_row('D02', lambda r, fl: r.__setitem__('quote', '  explains  the global reserve\tbehaviour of the filesystem '))),
    ('P04-closed-fence-and-comment-before', m_skill_line('D03', lambda l: ['```', 'code', '```', '<!-- c -->', l])),
    ('P05-empty-comment-line-before', m_skill_line('D04', lambda l: ['<!-->', l])),
    ('P06-escaped-pipe-in-source-row', set_reg('S905', 'Fixture source S905', 'Fixture \\| source S905')),
]

row_ref = {}


def p02(files, rows):
    r = row(rows, 'D05')
    text = files[r['snapshot']].replace('the reclaim behaviour', 'the <code>reclaim</code> behaviour &amp;')
    files[r['snapshot']] = text
    sha = hashlib.sha256(text.encode()).hexdigest()
    lines = files['corpus/SOURCES.md'].split('\n')
    i = next(k for k, l in enumerate(lines) if l.startswith('| S904 |'))
    import re
    lines[i] = re.sub(r'sha256 [0-9a-f]{64}', 'sha256 ' + sha, lines[i])
    files['corpus/SOURCES.md'] = '\n'.join(lines)
    r['quote'] = 'explains the reclaim behaviour &'


def resync_sha(files, rows, mutated):
    """Keep registry digests equal to snapshot bytes unless the shape targets the digest."""
    import re
    if mutated in ('F44-snapshot-edited-after-registry', 'F10-snapshot-sha-absent', 'P02-html-snapshot-tags-entities'):
        return
    lines = files['corpus/SOURCES.md'].split('\n')
    for r in rows:
        snap = r.get('snapshot')
        if not isinstance(snap, str) or snap not in files:
            continue
        sha = hashlib.sha256(files[snap].encode()).hexdigest()
        for k, l in enumerate(lines):
            if l.startswith('| %s |' % r['source']):
                lines[k] = re.sub(r'sha256 [0-9a-f]{64}', 'sha256 ' + sha, l)
    files['corpus/SOURCES.md'] = '\n'.join(lines)


def run_case(counter, work, name, mutate):
    files, rows = base_fixture()
    row_ref.clear()
    row_ref.update({r['id']: r for r in copy.deepcopy(rows)})
    base_sources = '# base\n\n' + HEADER
    if name == 'P02-html-snapshot-tags-entities':
        p02(files, rows)
    elif mutate:
        mutate(files, rows)
    resync_sha(files, rows, name)
    d = os.path.join(work, name)
    os.makedirs(d)
    if files.pop('__base__', None):
        base_sources += '| S900 | old | docs | A | s | a | t | mined | 2026-10-19 | r | u |\n'
    nojson = files.pop('__nojson__', None)
    dupkey = files.pop('__dupkey__', None)
    rowsdict = files.pop('__rowsdict__', None)
    if not nojson:
        text = dump(rows)
        if dupkey:
            text = text.replace('"id": "D01"', '"id": "D01", "id": "D01"', 1)
        if rowsdict:
            text = json.dumps({'rows': {r['id']: r for r in rows}})
        files['corpus/knowledge/btrfs-space-r30.json'] = text
    for path, content in files.items():
        full = os.path.join(d, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as fh:
            fh.write(content)
    bs = os.path.join(work, name + '.base-sources.md')
    with open(bs, 'w', encoding='utf-8') as fh:
        fh.write(base_sources)
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    p = subprocess.run([sys.executable, counter, '--tree', d, '--base-sources', bs],
                       capture_output=True, text=True, env=env, timeout=60)
    out = [json.loads(l) for l in p.stdout.splitlines() if l.startswith('{')]
    per = {o['id']: o for o in out if 'id' in o}
    summary = out[-1] if out else {}
    return per, summary, p.returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--counter', default=os.path.join(HERE, 'check-btrfs-space-r30.py'))
    ap.add_argument('--keep', action='store_true')
    a = ap.parse_args()
    work = tempfile.mkdtemp(prefix='btrfs-space-battery-')
    per, summary, _rc = run_case(a.counter, work, 'CONTROL', None)
    control = summary.get('verified')
    print(json.dumps({'shape': 'CONTROL', 'verified': control, 'unverified': summary.get('unverified')}))
    accepted, refused = [], []
    for name, target, mutate in SHOULD_FAIL:
        per, summary, _rc = run_case(a.counter, work, name, mutate)
        ok = bool(per.get(target, {}).get('verified'))
        if ok:
            accepted.append(name)
        print(json.dumps({'shape': name, 'kind': 'should-fail', 'target': target, 'accepted': ok,
                          'verified': summary.get('verified'), 'failures': per.get(target, {}).get('failures')}))
    for name, mutate in SHOULD_PASS:
        per, summary, _rc = run_case(a.counter, work, name, mutate)
        bad = summary.get('verified') != 10
        if bad:
            refused.append(name)
        print(json.dumps({'shape': name, 'kind': 'should-pass', 'refused': bad,
                          'verified': summary.get('verified'), 'unverified': summary.get('unverified')}))
    with open(a.counter, 'rb') as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    print(json.dumps({'control': control, 'should_fail_accepted': len(accepted), 'accepted_shapes': accepted,
                      'should_fail_total': len(SHOULD_FAIL), 'should_pass_refused': len(refused),
                      'refused_shapes': refused, 'should_pass_total': len(SHOULD_PASS),
                      'counter_sha256': sha, 'work': work if a.keep else None}))
    if not a.keep:
        shutil.rmtree(work, ignore_errors=True)
    return 0 if control == 10 and not accepted and not refused else 1


if __name__ == '__main__':
    sys.exit(main())
