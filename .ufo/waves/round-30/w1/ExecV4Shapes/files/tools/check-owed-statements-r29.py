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

Marker rules (an item counts only when every rule holds; the first failure is reported).
Version 2 (round-29 wave-1 repair after seat CritOwedCounterShapes counted 18 of 20 should-fail
shapes at the declaration commit `81a061a6`).  Version 2 refuses hollow shapes the declared counter
accepted, and it also accepts six format variants the declared counter refused (bold id, a `now`
quoting the anchor, a string basis, an extension-less path, an S### row with escaped pipes).
Version 3 (round-29 wave-2 repair after seat CritOwedCounterShapes' successor CritOwedV2Shapes
counted 25 of 26 new shapes): a marker must start its line (optionally after `- `), fences follow
CommonMark (an inline ```x``` line is not a fence) and indented code is skipped, look-alike ids are
folded (NFKC, Cyrillic/Greek O) before the uniqueness census, M1 is checked over rendered lines
only, `now` words must contain a letter after format characters are removed, a duplicated S### row
is unusable, `S###` is ASCII-only, path references are normalised (no `tools/`, no `..`) and the
cited line must be byte-identical at the claim base, and a JSON marker has exactly the seven keys
with no repeated key.  Version 4 (round-29 residual ResCritV3OverStrict, over-strictness only):
any CommonMark list or ordered-list prefix may precede a marker; a closed `<!-- ... -->` on a
marker line is stripped instead of hiding the line; JSON identity is counted only from an exact
`"id"` property (mentions inside another marker's text are not markers); a JSON marker may also
carry the metadata keys `round`, `marked_by`, `marked_at`, `status`, `corrected_by`; a cited
line may have moved if its text occurs exactly once at the claim base and once at the revision;
a capitalised verdict is reported as M4.  Version 5 (round-30 independent attack): exact
`<!-->` is treated as an empty comment without stripping following text; list-prefix spacing is
limited to one through four spaces; marker emphasis is either plain or balanced bold; and
allowed JSON metadata values are type/shape checked and status is limited to current or observed
round-27 labels.
Batteries: `tools/mutants-owed-statements-r29.py` (marker-free control),
`tools/mutants-owed-statements-r29-landed.py` (landed markers), and
`tools/mutants-owed-statements-r29-v4shapes.py` (routed shape attack and v4 acceptance controls).
Rules:
 M1  append-only: the base statement is unchanged at the revision.  Markdown: the full base
     line holding the anchor (sha256 in BASE_DIGEST) is still a line of the file, outside any
     marker line.  JSON: the named row field's value hashes to its BASE_DIGEST;
 M2  exactly one marker carries the item id across all six target files, ignoring markers inside
     fenced code blocks and HTML comments, and it sits in the item's own file;
       Markdown target: one line shaped (the id bracket may be bold, `**[R29-OWED-<id>]**`)
       `[R29-OWED-<id>] verdict: <v> | original: "<anchor>" | now: <text> | basis: <refs>`;
       JSON target: one object with `"id": "R29-OWED-<id>"` in the top-level
       `corrections_r29` array, keys `row`, `field`, `withdrawn_text`, `verdict`, `now`, `basis`
       (the round-27 `corrections_r27` pattern plus `id`, `verdict`, `now`, `basis`);
 M3  the marker quotes the anchor exactly (`original` / `withdrawn_text` == the anchor), and
     for JSON names the item's row and field;
 M4  verdict is a string, one of `corrected`, `rebutted`, `qualified`;
 M5  `now` is a string; with every copy of the anchor removed (compared case- and
     space-insensitively; a `now` may quote the anchor, as a literal tool output or a dated
     qualifier, but the anchor never counts toward the floor) it has at least 12 words and at
     least 10 distinct words, and its word set overlaps no other item's `now` word set by more
     than 60 percent (Jaccard);
 M6  basis (a list of strings, or one string) cites at least one resolvable reference: a source
     id `S###` whose `corpus/SOURCES.md` registry row (cells split on unescaped pipes) has status
     `mined` and whose used-by cell lists the target file's full repository path as one
     comma-separated entry; or a repository path `path:LINE` outside `tools/` whose line LINE
     exists, is not blank and is not itself a marker line;
 M7  items O01-O04 (kernel victim selection) need at least one `S###` reference that passes M6,
     was absent from `corpus/SOURCES.md` at the claim base `16e9ab2a` and was opened 2026-10-22
     (a source opened this round; a capture alone cannot establish a kernel mechanism).
Whether a cited source or path is relevant, and whether `now` means anything, is not mechanically
checkable (the landed battery reports such shapes as `semantic`); the round's reviewers judge it.  A malformed marker is a refusal, never a crash: the summary line
is always printed.

Usage: python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]
Output: one JSON line per item, then a summary JSON line with `items`, `marked`, `unmarked`.
Exit 0 when marked == items, 1 otherwise, 2 when the revision cannot be read.
Reads Git objects only (`git show`, `git cat-file`) with inherited GIT_* removed and the
round-30 Git child environment set to isolate system/global config and repository discovery.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata

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
CLAIM_BASE = '16e9ab2abfac430b4e960e8ce64b90420f602342'
OPENED = '2026-10-22'
BASE_DIGEST = {
    'O01': 'b7cbcffa8b3239a6d4310ed931bedbae1e8869e9fa18f062c5352363ee1fb8f4',
    'O02': '34c5baaf20a2cda95e39ad956c5f045f27b9fb012f83211daf2e661766363fe7',
    'O03': '1b1563e3c28865a691ef58705b59e516d3d2574024538bca052bdd8b872e9b88',
    'O04': 'd1a13e5d835e98b9be17e8ff2aabf4ff6e351ba9cb105f2c7e7d35c34e186cfc',
    'O05': 'afd272877b3af52d245defc77e8ebed62e0a4ff04d09f9af294114a9e1a6370f',
    'O06': '425c979cd7f0d41a2efa8bd393fcd9d84ce764b031027f2921ecd6be6f7fc40d',
    'O07': 'dff0f63c2ac82b652ad046bc46f4f9f923d77282a0019919f0dd2f4ea73b9578',
    'O08': '4703768aa5b2ff4bf421fa5de3ada08eef35dad07b55f566fc911b3f37ebde4c',
    'O09': '474c57533c4baac9aa20a667a8624c70f247bdc54cc743eb45498eecfca1d7e0',
    'O10': 'de10215a6992a2e8422b554b1c7af5ebad6e1d9f91d54290fef5653a1c7c0da0',
    'O11': '5ffd3f7d4a6bea776471be8e0513d9642aa4a60f3843591abb0fa8482d8265ef',
    'O12': '33c4b6d0327dba973ecb0041794bd6d8181c3176ab60fad75cdf8f42401a7664',
}
VERDICTS = {'corrected', 'rebutted', 'qualified'}
MD_MARKER = re.compile(
    r'^ {0,3}(?:[-*+][ ]{1,4}|\d{1,9}[.)][ ]{1,4})?'
    r'(?:\*\*\[R29-OWED-(?P<bold_id>O\d\d)\]\*\*|\[R29-OWED-(?P<plain_id>O\d\d)\])'
    r'\s*verdict:\s*(?P<verdict>[A-Za-z]+)\s*\|\s*original:\s*"(?P<original>.*?)"'
    r'\s*\|\s*now:\s*(?P<now>.*?)\s*\|\s*basis:\s*(?P<basis>.+?)\s*$')
SID = re.compile(r'\bS\d{3}\b', re.ASCII)
MARKER_START = re.compile(
    r'^ {0,3}(?:[-*+][ ]{1,4}|\d{1,9}[.)][ ]{1,4})?'
    r'(?:\*\*\[R29-OWED-([^\]\s]{1,8})\]\*\*|\[R29-OWED-([^\]\s]{1,8})\])')
FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})([^`]*)$')
JSON_KEYS = {'id', 'row', 'field', 'withdrawn_text', 'verdict', 'now', 'basis'}
JSON_META = {'round', 'marked_by', 'marked_at', 'status', 'corrected_by'}
JSON_STATUS_VALUES = {
    'active', 'applied', 'corrected', 'rebutted', 'qualified',
    'withdrawn as a universal in round 26', 'withdrawn as stated in round 26',
    'trigger omitted a second branch (round 26)', 'split in round 26', 'wrong location',
    'withdrawn in round 26 (SH6 trigger correction)',
}
CLOSED_COMMENT = re.compile(r'<!--.*?-->')
EMPTY_COMMENT = re.compile(r'<!-->')
PATHREF = re.compile(r'`?((?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+):(\d+)`?')


def clean_env(lane):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    home = os.environ.get('HOME')
    env.update({
        'GIT_OPTIONAL_LOCKS': '0',
        'GIT_CONFIG_NOSYSTEM': '1',
        'GIT_CONFIG_GLOBAL': os.devnull,
        'GIT_CONFIG_SYSTEM': os.devnull,
        'GIT_CEILING_DIRECTORIES': os.path.dirname(
            os.path.dirname(os.path.abspath(lane))),
        'PATH': '/usr/bin:/bin',
        'LC_ALL': 'C',
    })
    if home:
        env['HOME'] = home
        env['XDG_CONFIG_HOME'] = os.environ.get('XDG_CONFIG_HOME', os.path.join(home, '.config'))
    return env


def git(lane, *args):
    return subprocess.run(['git', '-C', lane, *args], capture_output=True,
                          env=clean_env(lane), timeout=60)


def show(lane, rev, path):
    p = git(lane, 'show', f'{rev}:{path}')
    return p.stdout.decode('utf-8', 'replace') if p.returncode == 0 else None


def split_cells(line):
    return [c.strip() for c in re.split(r'(?<!\\)\|', line.strip().strip('|'))]


def sources_rows(text):
    rows = {}
    for line in (text or '').splitlines():
        if not re.match(r'^\| S\d{3} \|', line):
            continue
        cells = split_cells(line)
        if len(cells) >= 11:
            used = {u.strip().strip('`').strip() for u in cells[10].split(',')}
            if cells[0] in rows:
                rows[cells[0]] = {'status': 'duplicate-id', 'opened': '', 'used_by': set()}
                continue
            rows[cells[0]] = {'status': cells[7], 'opened': cells[8], 'used_by': used}
    return rows


def live_lines(text):
    """Lines outside fenced or indented code blocks and HTML comments, with their 1-based numbers."""
    out, fence, comment = [], '', False
    for n, ln in enumerate(text.splitlines(), 1):
        s = ln.strip()
        if comment:
            if '-->' in ln:
                comment = False
            continue
        fm = FENCE.match(ln)
        if fence:
            if fm and fm.group(1)[0] == fence[0] and len(fm.group(1)) >= len(fence) and not fm.group(2).strip():
                fence = ''
            continue
        if fm:
            fence = fm.group(1)
            continue
        if ln.startswith('    ') or ln.startswith('\t'):
            continue
        ln = EMPTY_COMMENT.sub('', ln)
        ln = CLOSED_COMMENT.sub('', ln)
        if '<!--' in ln:
            comment = True
            continue
        out.append((n, ln))
    return out


def marker_id(line):
    """The item id of a marker-shaped line (look-alike characters folded), else None."""
    m = MARKER_START.match(line)
    if not m:
        return None
    raw = unicodedata.normalize('NFKC', m.group(1) or m.group(2))
    folded = raw.translate(str.maketrans({'\u041e': 'O', '\u039f': 'O', '\u043e': 'o', '\u03bf': 'o'}))
    return folded if re.fullmatch(r'O\d\d', folded, re.ASCII) else None


def json_metadata_error(marker):
    """Reject malformed metadata and status values outside known current/history states."""
    for key in JSON_META.intersection(marker):
        value = marker[key]
        if key == 'round':
            if not ((type(value) is int and value == 29) or value == '29'):
                return 'round must identify round 29'
        elif key == 'marked_at':
            if not isinstance(value, str):
                return 'marked_at must be an ISO date or datetime string'
            try:
                if 'T' in value:
                    datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
                else:
                    datetime.date.fromisoformat(value)
            except ValueError:
                return 'marked_at must be an ISO date or datetime string'
        elif key in {'marked_by', 'corrected_by'}:
            if not isinstance(value, str) or not value.strip():
                return f'{key} must be a non-empty string'
        elif key == 'status':
            if not isinstance(value, str) or not value.strip():
                return 'status must be a non-empty string'
            status = ' '.join(value.casefold().split())
            if status not in JSON_STATUS_VALUES:
                return 'status is not an allowed metadata state'
    return None


def words_of(text):
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Cf')
    return [w for w in re.findall(r"[^\s]+", text) if any(ch.isalpha() for ch in w)]


def norm(s):
    return ' '.join(s.lower().split())


def basis_ok(lane, rev, item_file, refs, srcrows, base_sids, need_sid):
    good_sid, good_new_sid, good_path, bad = [], [], [], []
    text = ' '.join(refs)
    for sid in sorted(set(SID.findall(text))):
        r = srcrows.get(sid)
        if r and r['status'] == 'mined' and item_file in r['used_by']:
            good_sid.append(sid)
            if sid not in base_sids and r['opened'] == OPENED:
                good_new_sid.append(sid)
        else:
            bad.append(sid)
    for raw_path, line in PATHREF.findall(text):
        n = int(line)
        path = os.path.normpath(raw_path)
        blocked = path.startswith('tools/') or path.startswith('..') or path.startswith('/')
        body = None if blocked else show(lane, rev, path)
        base_body = None if blocked else show(lane, CLAIM_BASE, path)
        lines = body.splitlines() if body is not None else []
        base_lines = base_body.splitlines() if base_body is not None else []
        cited = lines[n - 1] if body is not None and 1 <= n <= len(lines) else None
        same_place = cited is not None and n <= len(base_lines) and base_lines[n - 1] == cited
        moved_unique = cited is not None and base_lines.count(cited) == 1 and lines.count(cited) == 1
        if cited is not None and cited.strip() and 'R29-OWED-' not in cited and (same_place or moved_unique):
            good_path.append(f'{raw_path}:{line}')
        else:
            bad.append(f'{raw_path}:{line}')
    if need_sid and not good_new_sid:
        return False, f'M7 no S### opened this round that passes M6 (sources={good_sid}, bad={bad})'
    if not good_sid and not good_path:
        return False, f'M6 no resolvable basis reference (bad={bad})'
    return True, {'sources': good_sid, 'paths': good_path, 'unresolved': bad}


class _Obj(dict):
    duplicate_keys = False


def _pairs(pairs):
    d = _Obj(pairs)
    d.duplicate_keys = len(d) != len(pairs)
    return d


def check(lane, rev):
    srcrows = sources_rows(show(lane, rev, 'corpus/SOURCES.md'))
    base_sids = set(sources_rows(show(lane, CLAIM_BASE, 'corpus/SOURCES.md')))
    files = sorted({it[1] for it in ITEMS})
    cache = {f: show(lane, rev, f) for f in files}
    docs = {}
    for f in files:
        if f.endswith('.json') and cache[f] is not None:
            try:
                docs[f] = json.loads(cache[f], object_pairs_hook=_pairs)
            except ValueError:
                docs[f] = None
    # M2 census: where does each id appear, across every target file
    where = {it[0]: [] for it in ITEMS}
    for f in files:
        text = cache[f]
        if text is None:
            continue
        if f.endswith('.json'):
            corr = (docs.get(f) or {}).get('corrections_r29') if isinstance(docs.get(f), dict) else None
            for c in corr if isinstance(corr, list) else []:
                cid = c.get('id') if isinstance(c, dict) else None
                if isinstance(cid, str) and cid.startswith('R29-OWED-') and cid[9:] in where:
                    where[cid[9:]].append((f, c))
            for iid in where:
                hits = len(re.findall(r'"id"\s*:\s*"R29-OWED-' + iid + '"', text))
                listed = sum(1 for wf, _ in where[iid] if wf == f)
                for _ in range(hits - listed):
                    where[iid].append((f, None))
        else:
            for n, ln in live_lines(text):
                iid = marker_id(ln)
                if iid in where:
                    where[iid].append((f, ln))
    out, nows = [], {}
    for iid, path, row, field, anchor in ITEMS:
        res = {'id': iid, 'file': path, 'ok': False}
        out.append(res)
        text = cache[path]
        if text is None:
            res['why'] = 'M1 file missing at revision'
            continue
        if path.endswith('.json'):
            doc = docs.get(path)
            target = next((r for r in doc.get('rows', []) if isinstance(r, dict) and r.get('id') == row), None) \
                if isinstance(doc, dict) else None
            value = target.get(field) if isinstance(target, dict) else None
            if not isinstance(value, str) or hashlib.sha256(value.encode()).hexdigest() != BASE_DIGEST[iid]:
                res['why'] = 'M1 the named row field changed since the claim base (or is missing)'
                continue
        else:
            plain = [ln for _n, ln in live_lines(text) if marker_id(ln) is None]
            if not any(hashlib.sha256(ln.encode()).hexdigest() == BASE_DIGEST[iid] for ln in plain):
                res['why'] = 'M1 the base line holding the anchor changed or was removed'
                continue
        hits = where[iid]
        if len(hits) != 1 or hits[0][0] != path:
            res['why'] = f'M2 {len(hits)} markers ({sorted({h[0] for h in hits})}), need exactly one in {path}'
            continue
        m = hits[0][1]
        if path.endswith('.json'):
            if not isinstance(m, dict):
                res['why'] = 'M2 marker id appears outside corrections_r29'
                continue
            if not JSON_KEYS <= set(m) or set(m) - JSON_KEYS - JSON_META or getattr(m, 'duplicate_keys', False):
                res['why'] = ('M2 JSON marker keys must be ' + ','.join(sorted(JSON_KEYS)) + ' plus optional '
                              + ','.join(sorted(JSON_META)) + ' (no key repeated)')
                continue
            metadata_error = json_metadata_error(m)
            if metadata_error:
                res['why'] = 'M2 JSON metadata ' + metadata_error
                continue
            if m.get('row') != row or m.get('field') != field or m.get('withdrawn_text') != anchor:
                res['why'] = 'M3 row, field or withdrawn_text does not name the anchor exactly'
                continue
            verdict, now, basis = m.get('verdict'), m.get('now'), m.get('basis')
        else:
            mm = MD_MARKER.search(m)
            if not mm or (mm.group('bold_id') or mm.group('plain_id')) != iid:
                res['why'] = 'M2 marker line is not in the required shape'
                continue
            if mm.group('original') != anchor:
                res['why'] = 'M3 original does not equal the anchor'
                continue
            verdict, now, basis = mm.group('verdict'), mm.group('now'), mm.group('basis')
        if not isinstance(verdict, str) or verdict not in VERDICTS:
            res['why'] = f'M4 verdict {verdict!r}'
            continue
        if not isinstance(now, str):
            res['why'] = 'M5 now is not a string'
            continue
        n_now, n_anchor = norm(now), norm(anchor)
        words = [w.lower() for w in words_of(n_now.replace(n_anchor, ' '))]
        if len(words) < 12 or len(set(words)) < 10:
            res['why'] = f'M5 now has {len(words)} words, {len(set(words))} distinct (need 12 and 10)'
            continue
        wset = set(words)
        clash = next((o for o, s in nows.items() if len(wset & s) / len(wset | s) > 0.6), None)
        if clash:
            res['why'] = f'M5 now overlaps item {clash} by more than 60 percent'
            continue
        nows[iid] = wset
        if isinstance(basis, str):
            refs = [basis]
        elif isinstance(basis, list) and basis and all(isinstance(b, str) for b in basis):
            refs = basis
        else:
            res['why'] = 'M6 basis is not a string or a list of strings'
            continue
        ok, detail = basis_ok(lane, rev, path, refs, srcrows, base_sids, iid in KERNEL_MECHANISM)
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
