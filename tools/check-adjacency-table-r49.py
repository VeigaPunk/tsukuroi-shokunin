#!/usr/bin/env python3
"""Round-49 C2 counter (frozen before any seat of round 49): the ADJ-01..07 ownership table
rows cite PORTABLE anchors, not sibling line ranges.

Surface moved: `PROVINCE.md` `## Adjacent — finding-to-owner handoffs`. That table's
"Ownership source" column still carried bare `../<sibling>/PROVINCE.md:N-M` ranges — the
exact locator class QUALITY 32 / R19-ADJ-POINTERS rules out ("a bare path:N-M is not a
locator"). Each row must now name the OUT-0NN anchor of the `## Adjacent — portable ownership
anchors (round 19)` table whose own `province_pointer` names that ADJ row; the anchor row
must in turn carry its pinned sibling commit, heading and a <=25-word quote, and the
round-19 JSON registry must carry the anchor's blob sha256. The existing read-only checker
`tools/check-adjacency-anchors.py` must still PASS at the measured revision (it re-checks the
anchors against the live sibling bytes) — that leg is a cross-check, never the only leg.

Legs (counted):
  adj_rows        rows found in the ADJ table (7 expected)
  linked_rows     rows whose ownership cell names >=1 OUT id
  bare_ranges     total `*.md:N[-M]` occurrences in the ownership cells (target 0)
  anchors_ok      rows whose every referenced OUT id exists in the anchor table, names this
                  ADJ row, pins a sibling PROVINCE.md at a 12-40 hex commit, has an `# ...`
                  heading cell and a non-empty quote cell of <=25 words
  registry_ok     rows whose every referenced OUT id has a registry row with a 64-hex
                  sibling_blob_sha256 and a 12-40 hex sibling_commit
  anchors_checker_rc  exit status of tools/check-adjacency-anchors.py at REV

Predicate: adj_rows == 7 and linked_rows == 7 and bare_ranges == 0 and anchors_ok == 7
           and registry_ok == 7 and anchors_checker_rc == 0

Fixture overrides (controls only): --province-file, --registry-file, --skip-anchors-check.
Usage: python3 tools/check-adjacency-table-r49.py --revision <REV> [--lane <repo>]
Writes nothing. Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import json
import os
import re
import subprocess
import sys

BASE = '6256760d1382ce4ce20fcba830d4b2912cfbf12b'
PROVINCE = 'PROVINCE.md'
REGISTRY = 'corpus/knowledge/adjacency-anchors-r19.json'
CHECKER = 'tools/check-adjacency-anchors.py'
ADJ_HEAD = '## Adjacent — finding-to-owner handoffs'
ANCHOR_HEAD = '## Adjacent — portable ownership anchors (round 19)'
ADJ_ROW = re.compile(r'^\|\s*(ADJ-0\d)\s*\|')
OUT_ROW = re.compile(r'^\|\s*(OUT-\d{3})\s*\|')
OUT_ID = re.compile(r'OUT-\d{3}')
BARE = re.compile(r'[A-Za-z0-9_.-]+\.md:\d+(?:-\d+)?')
SIB = re.compile(r'^`([A-Za-z0-9_.-]+/PROVINCE\.md)`\s*@\s*`([0-9a-f]{12,40})`$')
HEAD = re.compile(r'^`#[^`]+`$')
HEX64 = re.compile(r'^[0-9a-f]{64}$')
HEX12 = re.compile(r'^[0-9a-f]{12,40}$')
PREDICATE = ('adj_rows == 7 and linked_rows == 7 and bare_ranges == 0 and anchors_ok == 7 '
             'and registry_ok == 7 and anchors_checker_rc == 0')


def git(lane, *args):
    return subprocess.run(['git', '-C', lane, *args], capture_output=True, stdin=subprocess.DEVNULL)


def show_text(lane, rev, path, override):
    if override:
        try:
            with open(override, 'rb') as fh:
                return fh.read().decode('utf-8', errors='replace')
        except OSError:
            return None
    p = git(lane, 'show', f'{rev}:{path}')
    return None if p.returncode else p.stdout.decode('utf-8', errors='replace')


def section(lines, head):
    start = next((i for i, ln in enumerate(lines) if ln.strip() == head), None)
    if start is None:
        return None
    end = next((k for k in range(start + 1, len(lines)) if lines[k].startswith('## ')), len(lines))
    return lines[start:end]


def cells(line):
    parts = line.split('|')
    return [p.strip() for p in parts[1:-1]]


def run(a, lane):
    rev = a.revision
    if not a.no_base_check and git(lane, 'cat-file', '-e', f'{BASE}^{{commit}}').returncode:
        print(json.dumps({'error': f'base {BASE} unreadable', 'verdict': 'FAIL'}))
        return 2
    prov = show_text(lane, rev, PROVINCE, a.province_file)
    if prov is None:
        print(json.dumps({'error': f'{PROVINCE} unreadable', 'verdict': 'FAIL'}))
        return 2
    lines = prov.split('\n')
    adj_sec = section(lines, ADJ_HEAD)
    anc_sec = section(lines, ANCHOR_HEAD)
    problems = []
    if adj_sec is None:
        problems.append(f'missing heading {ADJ_HEAD!r}')
    if anc_sec is None:
        problems.append(f'missing heading {ANCHOR_HEAD!r}')
    adj = {}
    for ln in adj_sec or []:
        m = ADJ_ROW.match(ln)
        if m:
            adj[m.group(1)] = cells(ln)
    anchors = {}
    for ln in anc_sec or []:
        m = OUT_ROW.match(ln)
        if m:
            anchors[m.group(1)] = cells(ln)
    registry = {}
    reg_text = show_text(lane, rev, REGISTRY, a.registry_file)
    if reg_text:
        try:
            reg = json.loads(reg_text)
            rows = reg.get('outbound') if isinstance(reg, dict) else None
            if isinstance(rows, list):
                for r in rows:
                    if isinstance(r, dict) and isinstance(r.get('id'), str):
                        registry[r['id']] = r
        except Exception as e:
            problems.append(f'registry unparsable: {type(e).__name__}')
    elif not a.registry_file:
        problems.append('registry absent')
    bare = 0
    linked = 0
    anchors_ok = 0
    registry_ok = 0
    per_row = {}
    for row_id in sorted(adj):
        cs = adj[row_id]
        own = cs[-1] if cs else ''
        row_bare = BARE.findall(own)
        outs = OUT_ID.findall(own)
        bare += len(row_bare)
        row_problems = []
        if row_bare:
            row_problems.append(f'bare locator(s): {row_bare}')
        if not outs:
            row_problems.append('no OUT anchor named')
        else:
            linked += 1
        a_ok = bool(outs)
        r_ok = bool(outs)
        for out in outs:
            anc = anchors.get(out)
            if anc is None:
                row_problems.append(f'{out} absent from anchor table')
                a_ok = r_ok = False
                continue
            if len(anc) < 5:
                row_problems.append(f'{out} anchor row has {len(anc)} cells')
                a_ok = r_ok = False
                continue
            if anc[1] != row_id:
                row_problems.append(f'{out} points at {anc[1]!r}, not {row_id}')
                a_ok = False
            sm = SIB.fullmatch(anc[2])
            if not sm:
                row_problems.append(f'{out} sibling cell {anc[2]!r} not `<path>/PROVINCE.md` @ `<12-40 hex>`')
                a_ok = False
            if not HEAD.fullmatch(anc[3]):
                row_problems.append(f'{out} heading cell {anc[3]!r} not `# ...`')
                a_ok = False
            quote = anc[4].strip('`').strip()
            if not quote or len(quote.split()) > 25:
                row_problems.append(f'{out} quote cell empty or over 25 words ({len(quote.split())})')
                a_ok = False
            rr = registry.get(out)
            if rr is None:
                row_problems.append(f'{out} absent from {REGISTRY}')
                r_ok = False
                continue
            if not HEX64.fullmatch(str(rr.get('sibling_blob_sha256', ''))):
                row_problems.append(f'{out} registry blob sha256 invalid')
                r_ok = False
            if not HEX12.fullmatch(str(rr.get('sibling_commit', ''))):
                row_problems.append(f'{out} registry commit invalid')
                r_ok = False
        anchors_ok += int(a_ok)
        registry_ok += int(r_ok)
        per_row[row_id] = {'outs': outs, 'bare': row_bare, 'problems': row_problems}
    checker_rc = -1
    if not a.skip_anchors_check:
        checker = os.path.join(lane, CHECKER)
        p = subprocess.run([sys.executable, checker, '--revision', rev],
                           capture_output=True, stdin=subprocess.DEVNULL, text=True)
        checker_rc = p.returncode
        if checker_rc != 0:
            problems.append(f'{CHECKER} rc={checker_rc}: {p.stdout.strip()[:200]}')
    out = {'counter': 'check-adjacency-table-r49', 'revision': rev, 'base': BASE,
           'adj_rows': len(adj), 'linked_rows': linked, 'bare_ranges': bare,
           'anchors_ok': anchors_ok, 'registry_ok': registry_ok,
           'anchors_checker_rc': checker_rc, 'per_row': per_row, 'problems': problems,
           'predicate': PREDICATE}
    ok = (len(adj) == 7 and linked == 7 and bare == 0 and anchors_ok == 7
          and registry_ok == 7 and checker_rc == 0)
    out['verdict'] = 'PASS' if ok else 'FAIL'
    print(json.dumps(out, sort_keys=True))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--province-file')
    ap.add_argument('--registry-file')
    ap.add_argument('--skip-anchors-check', action='store_true')
    ap.add_argument('--no-base-check', action='store_true')
    a = ap.parse_args()
    try:
        return run(a, os.path.abspath(a.lane))
    except Exception as e:
        print(json.dumps({'counter': 'check-adjacency-table-r49',
                          'error': f'{type(e).__name__}: {e}', 'verdict': 'FAIL'}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
