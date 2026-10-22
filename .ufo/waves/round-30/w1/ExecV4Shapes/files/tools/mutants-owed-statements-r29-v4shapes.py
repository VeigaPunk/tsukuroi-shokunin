#!/usr/bin/env python3
"""Independent v4-shape battery for the round-29 owed-statement counter.

Builds each fixture from the landed markers at --base in a private clone, then
reports whether the selected marker is counted. Controls cover every should-pass
variant listed in the round-29 v4 measurement. Every Git child obeys the round-30
GIT CHILD ENV CONTRACT; the lane is read-only.
"""
import argparse
import atexit
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
ap.add_argument('--base', required=True)
group = ap.add_mutually_exclusive_group(required=True)
group.add_argument('--counter-rev')
group.add_argument('--counter-file')
ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap.add_argument('--keep', action='store_true')
ARGS = ap.parse_args()

SEAT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SEAT = tempfile.mkdtemp(prefix='owed-r29-v4shapes-', dir=SEAT_ROOT)
if not ARGS.keep:
    atexit.register(shutil.rmtree, SEAT, True)
HOME = os.path.join(SEAT, 'home')
os.makedirs(os.path.join(HOME, '.config'))
ENV = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
ENV.update({
    'GIT_CONFIG_NOSYSTEM': '1',
    'GIT_CONFIG_GLOBAL': os.devnull,
    'GIT_CONFIG_SYSTEM': os.devnull,
    'HOME': HOME,
    'XDG_CONFIG_HOME': os.path.join(HOME, '.config'),
    'PATH': '/usr/bin:/bin',
    'GIT_CEILING_DIRECTORIES': os.path.dirname(SEAT),
})
REPO = os.path.join(SEAT, 'repo')
subprocess.run(['git', 'clone', '-q', '--no-local', ARGS.lane, REPO],
               check=True, capture_output=True, env=ENV)


def lane_git(*args):
    return subprocess.run(['git', '-C', ARGS.lane, *args], check=True,
                          capture_output=True, env=ENV)


def git(*args):
    p = subprocess.run(['git', '-C', REPO, '-c', 'user.name=owed-v4-shapes',
                        '-c', 'user.email=owed-v4-shapes@localhost', *args],
                       capture_output=True, text=True, env=ENV)
    if p.returncode:
        raise SystemExit(f'git {args!r} failed: {p.stderr}')
    return p.stdout.strip()

BASE = lane_git('rev-parse', '--verify', ARGS.base + '^{commit}').stdout.decode().strip()
if ARGS.counter_file:
    with open(ARGS.counter_file, 'rb') as f:
        COUNTER = f.read()
else:
    COUNTER = lane_git('show', ARGS.counter_rev + ':tools/check-owed-statements-r29.py').stdout
COUNTER_SHA = hashlib.sha256(COUNTER).hexdigest()
COUNTER_PATH = os.path.join(SEAT, 'counter', 'check-owed-statements-r29.py')
os.makedirs(os.path.dirname(COUNTER_PATH))
with open(COUNTER_PATH, 'wb') as f:
    f.write(COUNTER)

OOM = 'corpus/knowledge/oom-event-plane.md'
KILL = 'corpus/knowledge/kill-event-deep-r8.md'
SKILL = 'SKILL.md'
DRV = 'corpus/knowledge/driver-firmware-plane.md'
MP = 'corpus/knowledge/memory-pressure-r25.json'
SH = 'corpus/knowledge/storage-health-r26.json'
JSON_FILE = {'O06': MP, 'O07': MP, 'O09': SH, 'O10': SH, 'O11': SH, 'O12': SH}
MD_FILE = {'O01': OOM, 'O02': OOM, 'O03': KILL, 'O04': KILL,
           'O05': SKILL, 'O08': DRV}
ANCHOR_O01 = 'exactly the band the kernel scans first'


def rd(path):
    with open(os.path.join(REPO, path), encoding='utf-8') as f:
        return f.read()


def wr(path, text):
    full = os.path.join(REPO, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(text)


def md_edit(iid, edit):
    path = MD_FILE[iid]
    text = rd(path)
    lines = text.splitlines()
    matches = [n for n, line in enumerate(lines) if f'[R29-OWED-{iid}]' in line]
    if len(matches) != 1:
        raise RuntimeError(f'expected one markdown marker for {iid}, found {len(matches)}')
    lines[matches[0]] = edit(lines[matches[0]])
    wr(path, '\n'.join(lines) + ('\n' if text.endswith('\n') else ''))


def json_edit(iid, edit):
    path = JSON_FILE[iid]
    doc = json.loads(rd(path))
    matches = [obj for obj in doc['corrections_r29'] if obj.get('id') == f'R29-OWED-{iid}']
    if len(matches) != 1:
        raise RuntimeError(f'expected one JSON marker for {iid}, found {len(matches)}')
    edit(matches[0], doc)
    wr(path, json.dumps(doc, indent=1, ensure_ascii=False) + '\n')


def marked_line(iid, transform):
    md_edit(iid, transform)


def inject_empty_comment_after_id(iid):
    md_edit(iid, lambda line: line.replace(
        '] verdict:', '] <!--> hidden-looking text --> verdict:', 1))


def inject_empty_comment_before_original(iid):
    md_edit(iid, lambda line: line.replace(
        ' | original:', ' <!--> hidden-looking text --> | original:', 1))


def list_five_spaces(iid, prefix):
    md_edit(iid, lambda line: prefix + line)


def bare_italic(iid):
    md_edit(iid, lambda line: line.replace(
        f'[R29-OWED-{iid}]', f'*[R29-OWED-{iid}]*', 1))


def unbalanced_open(iid):
    md_edit(iid, lambda line: line.replace(
        f'[R29-OWED-{iid}]', f'**[R29-OWED-{iid}]', 1))


def unbalanced_close(iid):
    md_edit(iid, lambda line: line.replace(
        f'[R29-OWED-{iid}]', f'[R29-OWED-{iid}]**', 1))


def append_anchor_comment():
    text = rd(OOM)
    lines = text.splitlines()
    matches = [n for n, line in enumerate(lines)
               if ANCHOR_O01 in line and 'R29-OWED-' not in line]
    if len(matches) != 1:
        raise RuntimeError(f'expected one O01 anchor line, found {len(matches)}')
    lines[matches[0]] += f'<!-- {ANCHOR_O01} -->'
    wr(OOM, '\n'.join(lines) + ('\n' if text.endswith('\n') else ''))


def append_cited_file_line():
    wr('corpus/knowledge/storage-health-r26.md',
       rd('corpus/knowledge/storage-health-r26.md') + '\nRound-29 v4 shape control appendix.\n')


def shift_storage_citations():
    path = 'corpus/knowledge/storage-health-r26.md'
    text = rd(path)
    lines = text.splitlines()
    lines.insert(127, '<!-- v4 unique-citation movement control -->')
    wr(path, '\n'.join(lines) + ('\n' if text.endswith('\n') else ''))
    doc = json.loads(rd(SH))
    for obj in doc['corrections_r29']:
        if isinstance(obj.get('basis'), list):
            obj['basis'] = [re.sub(
                r'(corpus/knowledge/storage-health-r26\.md:)([0-9]+)',
                lambda m: m.group(1) + str(int(m.group(2)) + 1), ref)
                for ref in obj['basis']]
    wr(SH, json.dumps(doc, indent=1, ensure_ascii=False) + '\n')


def json_round_key():
    json_edit('O09', lambda obj, _doc: obj.update(round=29))


def json_date_key():
    json_edit('O09', lambda obj, _doc: obj.update(marked_at='2026-10-22'))


def json_r27_metadata():
    def edit(obj, doc):
        previous = doc['corrections_r27'][0]
        for key in ('status', 'corrected_by', 'marked_by'):
            obj[key] = previous[key]
    json_edit('O09', edit)


def json_cross_reference():
    json_edit('O07', lambda obj, _doc: obj.update(
        now=obj['now'] + ' R29-OWED-O06 cross-reference'))


def json_invalid_status():
    json_edit('O11', lambda obj, _doc: obj.update(status='withdrawn'))


def json_invalid_status_future():
    json_edit('O11', lambda obj, _doc: obj.update(status='withdrawn in round 29'))


def json_invalid_status_type():
    json_edit('O11', lambda obj, _doc: obj.update(status=False))


def json_invalid_round():
    json_edit('O11', lambda obj, _doc: obj.update(round='withdrawn'))


def markdown_cross_reference():
    md_edit('O01', lambda line: re.sub(
        r'( \| now: .*?)( \| basis:)',
        lambda m: m.group(1) + ' R29-OWED-O02' + m.group(2), line, count=1))


def markdown_basis_change(fn):
    def edit(line):
        return re.sub(r'corpus/knowledge/memory-pressure-r25\.md:387', fn, line, count=1)
    md_edit('O05', edit)


def cited_path_range():
    markdown_basis_change(lambda _m: 'corpus/knowledge/memory-pressure-r25.md:387-390')


def cited_path_dot_slash():
    markdown_basis_change(lambda _m: './corpus/knowledge/memory-pressure-r25.md:387')


def append_now_suffix(suffix):
    md_edit('O01', lambda line: re.sub(
        r'( \| now: .*?)( \| basis:)',
        lambda m: m.group(1) + suffix + m.group(2), line, count=1))


def cited_file_insert_above():
    shift_storage_citations()


SHOULD_FAIL = [
    ('N8 empty comment after id hides invalid intervening text', 'O05', lambda: inject_empty_comment_after_id('O05')),
    ('N8 empty comment before original hides invalid intervening text', 'O05', lambda: inject_empty_comment_before_original('O05')),
    ('N9 dash list prefix plus five spaces (indented code)', 'O05',
     lambda: list_five_spaces('O05', '-     ')),
    ('N9 ordered-list prefix plus five spaces (indented code)', 'O05',
     lambda: list_five_spaces('O05', '1.     ')),
    ('N20 allowed status metadata set to withdrawn', 'O11', json_invalid_status),
    ('N20 status metadata falsely withdraws the round-29 marker', 'O11', json_invalid_status_future),
    ('N20 allowed status metadata has a boolean value', 'O11', json_invalid_status_type),
    ('N20 round metadata has an unchecked value', 'O11', json_invalid_round),
    ('italic marker id', 'O05', lambda: bare_italic('O05')),
    ('unbalanced opening asterisks around marker id', 'O05', lambda: unbalanced_open('O05')),
    ('unbalanced closing asterisks around marker id', 'O05', lambda: unbalanced_close('O05')),
]

SHOULD_PASS = [
    ('v4 list-dash', 'O01', lambda: marked_line('O01', lambda line: '- ' + line)),
    ('v4 list-dash-bold', 'O01', lambda: marked_line(
        'O01', lambda line: '- ' + line.replace('[R29-OWED-O01]', '**[R29-OWED-O01]**', 1))),
    ('v4 list-star', 'O01', lambda: marked_line('O01', lambda line: '* ' + line)),
    ('v4 list-plus', 'O01', lambda: marked_line('O01', lambda line: '+ ' + line)),
    ('v4 list-ordered', 'O01', lambda: marked_line('O01', lambda line: '1. ' + line)),
    ('v4 list-nested', 'O01', lambda: marked_line('O01', lambda line: '  - ' + line)),
    ('v4 list-dash-two-spaces', 'O01', lambda: marked_line('O01', lambda line: '-  ' + line)),
    ('v4 trailing inline anchor comment', 'O01', append_anchor_comment),
    ('v4 path line-range reference', 'O05', cited_path_range),
    ('v4 ./ path reference', 'O05', cited_path_dot_slash),
    ('v4 cited file appended after its evidence', 'O09', append_cited_file_line),
    ('v4 unique cited line shifted with insertion', 'O09', cited_file_insert_above),
    ('v4 JSON round metadata', 'O09', json_round_key),
    ('v4 JSON marked_at metadata', 'O09', json_date_key),
    ('v4 JSON corrections_r27 metadata keys and values', 'O09', json_r27_metadata),
    ('v4 JSON marker-id cross-reference in now', 'O07', json_cross_reference),
    ('v4 Markdown marker-id cross-reference in now', 'O01', markdown_cross_reference),
    ('v4 now containing separated number and unit', 'O01', lambda: append_now_suffix(' 12 GiB')),
    ('v4 now containing glued number and unit', 'O01', lambda: append_now_suffix(' 12GiB')),
]


def counter(revision):
    p = subprocess.run([sys.executable, COUNTER_PATH, '--revision', revision, '--lane', REPO],
                       capture_output=True, text=True, env=ENV)
    rows, summary = {}, None
    for line in p.stdout.splitlines():
        try:
            value = json.loads(line)
        except ValueError:
            continue
        if 'id' in value:
            rows[value['id']] = value
        else:
            summary = value
    return p.returncode, rows, summary, p.stderr.strip().splitlines()[-1:] if p.stderr.strip() else []


def begin_case():
    git('checkout', '-q', '--detach', BASE)
    git('clean', '-qfd')


def run_case(name, iid, expected, mutate, revision='HEAD'):
    begin_case()
    mutate()
    git('add', '-A')
    git('commit', '--quiet', '-m', name)
    commit = git('rev-parse', 'HEAD')
    rc, rows, summary, errors = counter(revision if revision != 'HEAD' else commit)
    row = rows.get(iid, {})
    return {
        'shape': name,
        'item': iid,
        'expected': expected,
        'commit': commit,
        'exit': rc,
        'marked': summary.get('marked') if summary else None,
        'counts': row.get('ok') is True,
        'why': row.get('why'),
        'counter_sha256': summary.get('counter_sha256') if summary else None,
        'stderr_tail': errors,
    }


def main():
    rc, rows, summary, errors = counter(BASE)
    landed = {
        'shape': 'landed markers at base',
        'revision': BASE,
        'exit': rc,
        'marked': summary.get('marked') if summary else None,
        'counter_sha256': summary.get('counter_sha256') if summary else None,
        'stderr_tail': errors,
    }
    results = []
    for name, iid, mutate in SHOULD_FAIL:
        results.append(run_case(name, iid, 'refuse', mutate))
    for name, iid, mutate in SHOULD_PASS:
        results.append(run_case(name, iid, 'count', mutate))
    git('checkout', '-q', '--detach', BASE)
    print(json.dumps(landed, ensure_ascii=False, sort_keys=True))
    for result in results:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    rejected_accepted = [r['shape'] for r in results if r['expected'] == 'refuse' and r['counts']]
    controls_refused = [r['shape'] for r in results if r['expected'] == 'count' and not r['counts']]
    crashes = [r['shape'] for r in results if r['marked'] is None]
    summary_line = {
        'base': BASE,
        'counter_sha256': COUNTER_SHA,
        'landed_marked': landed['marked'],
        'should_refuse_total': len(SHOULD_FAIL),
        'should_refuse_counted': len(rejected_accepted),
        'counted_shapes': rejected_accepted,
        'should_pass_total': len(SHOULD_PASS),
        'should_pass_refused': len(controls_refused),
        'refused_controls': controls_refused,
        'crashes': crashes,
    }
    print(json.dumps(summary_line, ensure_ascii=False, sort_keys=True))
    return 0 if landed['marked'] == 12 and not rejected_accepted and not controls_refused and not crashes else 1


if __name__ == '__main__':
    sys.exit(main())
