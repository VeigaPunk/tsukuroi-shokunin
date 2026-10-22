#!/usr/bin/env python3
"""Owed-statement correction counter (round 29, claim C1, axis depth).

Counts how many of the twelve FROZEN owed statements carry one valid, source-backed
correction marker at a landed revision.  The set is the round-27 spot-check routed defects 4
and 5 (`corpus/lessons/round-27-verifier-spotcheck.md:102-103`; enumeration in
`corpus/lessons/round-27.md:80-83` and `.ufo/waves/round-27/w1/RevRoutedDefects.md:20`):
the "+200 band scanned first" OOM-selection reading (O01-O04), the MP4 "nothing monitored"
qualifier debt (O05-O07), the `driver-firmware-plane.md` `[unk]` (O08) and four unmarked
statements of `storage-health-r26.json` (O09-O12).  Every anchor is a verbatim substring of
its file at the round-29 base `16e9ab2a`.

Marker rules (an item counts only when every rule holds; the first failure is reported):
 M1  the anchor text is still present verbatim in its file at the revision (append-only:
     the original statement is kept, never rewritten);
 M2  exactly one marker carries the item id;
       Markdown target: one line containing `[R29-OWED-<id>]`, shaped
       `[R29-OWED-<id>] verdict: <v> | original: "<anchor>" | now: <text> | basis: <refs>`;
       JSON target: one object with `"id": "R29-OWED-<id>"` in the top-level
       `corrections_r29` array, keys `row`, `field`, `withdrawn_text`, `verdict`, `now`, `basis`
       (the round-27 `corrections_r27` pattern plus `id`, `verdict`, `now`, `basis`);
 M3  the marker quotes the anchor exactly (`original` / `withdrawn_text` == the anchor), and
     for JSON the named row and field hold that text;
 M4  verdict is one of `corrected`, `rebutted`, `qualified`;
 M5  `now` has at least 12 words, does not contain the anchor, and is not a word-for-word
     repeat of another item's `now`;
 M6  basis cites at least one resolvable reference: a source id `S###` whose
     `corpus/SOURCES.md` registry row has status `mined` and whose used-by cell names the
     target file's basename, or a repository path `path:LINE` that exists at the revision
     with at least LINE lines;
 M7  items O01-O04 (kernel victim selection) need at least one `S###` reference that passes M6
     (a capture alone cannot establish a kernel mechanism).

Usage: python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]
Output: one JSON line per item, then a summary JSON line with `items`, `marked`, `unmarked`.
Exit 0 when marked == items, 1 otherwise, 2 when the revision cannot be read.
Reads git objects only (`git show`, `git cat-file`) with every inherited GIT_* variable removed.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

ITEMS = (
    ('O01', 'corpus/knowledge/oom-event-plane.md', None, None,
     'exactly the band the kernel scans first'),
    ('O02', 'corpus/knowledge/oom-event-plane.md', None, None,
     'the +200 band is chosen first'),
    ('O03', 'corpus/knowledge/kill-event-deep-r8.md', None, None,
     'under a kernel OOM the scan prefers the higher-scored, larger-RSS tasks first'),
    ('O04', 'corpus/knowledge/kill-event-deep-r8.md', None, None,
     'the +200 band is scanned first'),
    ('O05', 'SKILL.md', None, None,
     'so nothing in that chain is monitored'),
    ('O06', 'corpus/knowledge/memory-pressure-r25.json', 'MP4', 'action',
     "Enabling the unit would still monitor nothing while every unit stays 'auto'"),
    ('O07', 'corpus/knowledge/memory-pressure-r25.json', 'MP4', 'statement',
     "systemd-oomd monitors only cgroups whose units carry 'kill'."),
    ('O08', 'corpus/knowledge/driver-firmware-plane.md', None, None,
     'the loaded module is not re-identified by modinfo [unk]'),
    ('O09', 'corpus/knowledge/storage-health-r26.json', 'SH1', 'statement',
     'under shorter names (write_errs, read_errs, flush_errs, corruption_errs, generation_errs)'),
    ('O10', 'corpus/knowledge/storage-health-r26.json', 'SH3', 'statement',
     'systemd sets that attribute on journal files by default'),
    ('O11', 'corpus/knowledge/storage-health-r26.json', 'SH4', 'statement',
     'No scrub record exists on this host'),
    ('O12', 'corpus/knowledge/storage-health-r26.json', 'SH5', 'statement',
     'FAILED! otherwise'),
)
KERNEL_MECHANISM = {'O01', 'O02', 'O03', 'O04'}
VERDICTS = {'corrected', 'rebutted', 'qualified'}
MD_MARKER = re.compile(
    r'\[R29-OWED-(?P<id>O\d\d)\]\s*verdict:\s*(?P<verdict>[a-z]+)\s*\|\s*original:\s*"(?P<original>.*?)"'
    r'\s*\|\s*now:\s*(?P<now>.*?)\s*\|\s*basis:\s*(?P<basis>.+?)\s*$')
SID = re.compile(r'\bS\d{3}\b')
PATHREF = re.compile(r'`?([A-Za-z0-9_./-]+\.[A-Za-z0-9]+):(\d+)`?')


def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update({'GIT_OPTIONAL_LOCKS': '0', 'LC_ALL': 'C'})
    return env


def git(lane, *args):
    return subprocess.run(['git', '-C', lane, *args], capture_output=True, env=clean_env(), timeout=60)


def show(lane, rev, path):
    p = git(lane, 'show', f'{rev}:{path}')
    return p.stdout.decode('utf-8', 'replace') if p.returncode == 0 else None


def sources_rows(text):
    rows = {}
    for line in (text or '').splitlines():
        if not re.match(r'^\| S\d{3} \|', line):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 11:
            rows[cells[0]] = {'status': cells[7], 'used_by': cells[10]}
    return rows


def basis_ok(lane, rev, item_file, basis_text, srcrows, need_sid):
    base = os.path.basename(item_file)
    good_sid, good_path, bad = [], [], []
    for sid in SID.findall(basis_text):
        r = srcrows.get(sid)
        if r and r['status'] == 'mined' and base in r['used_by']:
            good_sid.append(sid)
        else:
            bad.append(sid)
    for path, line in PATHREF.findall(basis_text):
        body = show(lane, rev, path)
        if body is not None and int(line) >= 1 and len(body.splitlines()) >= int(line):
            good_path.append(f'{path}:{line}')
        else:
            bad.append(f'{path}:{line}')
    if need_sid and not good_sid:
        return False, f'M7 no S### reference that passes M6 (bad={bad})'
    if not good_sid and not good_path:
        return False, f'M6 no resolvable basis reference (bad={bad})'
    return True, {'sources': good_sid, 'paths': good_path, 'unresolved': bad}


def check(lane, rev):
    srcrows = sources_rows(show(lane, rev, 'corpus/SOURCES.md'))
    out, nows = [], {}
    cache = {}
    for iid, path, row, field, anchor in ITEMS:
        if path not in cache:
            cache[path] = show(lane, rev, path)
        text = cache[path]
        res = {'id': iid, 'file': path, 'ok': False}
        out.append(res)
        if text is None:
            res['why'] = 'M1 file missing at revision'
            continue
        if path.endswith('.json'):
            try:
                doc = json.loads(text)
            except ValueError as e:
                res['why'] = f'M1 json unreadable: {e}'
                continue
            target = next((r for r in doc.get('rows', []) if isinstance(r, dict) and r.get('id') == row), None)
            if target is None or not isinstance(target.get(field), str) or anchor not in target[field]:
                res['why'] = 'M1 anchor not present in the named row field'
                continue
            corr = doc.get('corrections_r29')
            ms = [c for c in corr if isinstance(c, dict) and c.get('id') == 'R29-OWED-' + iid] \
                if isinstance(corr, list) else []
            if len(ms) != 1:
                res['why'] = f'M2 {len(ms)} markers'
                continue
            m = ms[0]
            if m.get('row') != row or m.get('field') != field or m.get('withdrawn_text') != anchor:
                res['why'] = 'M3 row, field or withdrawn_text does not name the anchor exactly'
                continue
            verdict, now = m.get('verdict'), m.get('now')
            basis = m.get('basis')
            basis_text = ' '.join(basis) if isinstance(basis, list) and all(isinstance(b, str) for b in basis) else None
            if basis_text is None:
                res['why'] = 'M6 basis is not a list of strings'
                continue
        else:
            if text.count(anchor) < 1:
                res['why'] = 'M1 anchor not present'
                continue
            lines = [ln for ln in text.splitlines() if f'[R29-OWED-{iid}]' in ln]
            if len(lines) != 1:
                res['why'] = f'M2 {len(lines)} markers'
                continue
            mm = MD_MARKER.search(lines[0])
            if not mm or mm.group('id') != iid:
                res['why'] = 'M2 marker line is not in the required shape'
                continue
            if mm.group('original') != anchor:
                res['why'] = 'M3 original does not equal the anchor'
                continue
            verdict, now, basis_text = mm.group('verdict'), mm.group('now'), mm.group('basis')
        if verdict not in VERDICTS:
            res['why'] = f'M4 verdict {verdict!r}'
            continue
        if not isinstance(now, str) or len(now.split()) < 12 or anchor in now:
            res['why'] = 'M5 now is shorter than 12 words or repeats the anchor'
            continue
        key = ' '.join(now.lower().split())
        if key in nows:
            res['why'] = f'M5 now repeats item {nows[key]}'
            continue
        nows[key] = iid
        ok, detail = basis_ok(lane, rev, path, basis_text, srcrows, iid in KERNEL_MECHANISM)
        if not ok:
            res['why'] = detail
            continue
        res.update(ok=True, verdict=verdict, basis=detail)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    p = git(a.lane, 'rev-parse', '--verify', a.revision + '^{commit}')
    if p.returncode != 0:
        print(json.dumps({'error': 'revision unreadable', 'revision': a.revision}))
        return 2
    rev = p.stdout.decode().strip()
    rows = check(a.lane, rev)
    for r in rows:
        print(json.dumps(r, sort_keys=True))
    marked = sum(r['ok'] for r in rows)
    with open(os.path.abspath(__file__), 'rb') as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    print(json.dumps({'revision': rev, 'items': len(rows), 'marked': marked,
                      'unmarked': [r['id'] for r in rows if not r['ok']], 'counter_sha256': sha}))
    return 0 if marked == len(rows) else 1


if __name__ == '__main__':
    sys.exit(main())
