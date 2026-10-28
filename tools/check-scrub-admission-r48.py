#!/usr/bin/env python3
"""Round-48 C2 counter (frozen before data): admission of the btrfs scrub grounding rows GR1, GR2, GR3.

Successor of tools/check-scrub-admission-r48.py (round 47 closed `rejected-honest-stop`: the counted
GR2 critic read the unmount-suspend wording as false, the K22 map omitted S240 ioctl.c, the wave cohort
was unsettled at measurement). Round 48 re-reads all three rows with counted seats of ONE wave (w2)
against the corrected bytes (GR2 attributes btrfs_scrub_cancel to btrfs_dev_replace_cancel,
dev-replace.c:1126-1144; the unmount suspend path only sets SUSPENDED).

Amendments over r47, applied before any seat (frozen with the counter):
  A1  K22 map gains S240 ioctl.c (round-43 snapshot, sha256 digest-pinned) and CITE GR2 gains ioctl.c.
  A2  A seat whose report carries an unresolvable file:line citation is UNBOUND for credit (its `holds`
      earns nothing) but a bound-format seat whose verdict on the CURRENT row hash is `partly` or
      `fails` blocks the row whatever its citations: a citation slip never launders a negative.
  A3  Universe per row: three reviewers + three critics in the single wave (R48RevGR<n>{a,b,c},
      R48CritGR<n>{a,b,c}); a row needs >=3 credited seats, >=1 reviewer and >=1 critic among them,
      pairwise distinct bodies (K23), all `holds`, no blocking negative.
  F1/F2/F3/K22/K23 of round 47 carry over unchanged (structural row extent, exact-line SKILL mark,
  negation-proof README mark, in-band parse failures, quote and citation resolution, distinct bodies).

Seat reports bind on files: line 1 `ROW GR<n> VERDICT: holds|partly|fails`, line 2
`SECTION SHA256: <hex>`, then the body (>=300 bytes, with file:line citations of pinned sources).
The counter parses files the seats write (never a wrapped final text).

Usage: python3 tools/check-scrub-admission-r48.py --revision <REV> [--lane <repo>] [--section-hash]
Writes nothing. Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
Round-47 carry-overs (unchanged): the F1 structural row extent, the F2 exact-line SKILL mark and
negation-proof README mark, the F3 in-band parse failures, the K22 quote/citation resolution and
the K23 distinct-bodies rule — see tools/check-scrub-admission-r47.py for their origin findings.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = '5fdf062f969292736e36513e39f98b1b8de43635'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
WAVES = '.ufo/waves/round-48'
WAVE = 'w2'
ROWS = ('GR1', 'GR2', 'GR3')
# pinned digest-checked snapshots the rows cite: S-id -> {file -> (path, sha256)}
SNAPSHOTS = {
    'S237': {'scrub.c': ('.ufo/waves/round-42/frozen/src/scrub.c',
                         '48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801')},
    'S242': {'scrub.c': ('.ufo/waves/round-44/frozen/src/scrub.c',
                         'f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8')},
    'S240': {'ioctl.c': ('.ufo/waves/round-43/frozen/src/ioctl.c',
                         '7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01')},
    'S243': {'sysfs.c': ('.ufo/waves/round-44/frozen/src/sysfs.c',
                         'ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43')},
    'S244': {'btrfs-scrub@.service': ('.ufo/waves/round-44/frozen/src/btrfs-scrub@.service',
                                      'eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252')},
    'S246': {'cmdline.c': ('.ufo/waves/round-45/frozen/src/cmdline.c',
                           '1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d'),
             'vsprintf.c': ('.ufo/waves/round-45/frozen/src/vsprintf.c',
                            'cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca'),
             'kstrtox.c': ('.ufo/waves/round-45/frozen/src/kstrtox.c',
                           '0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4')},
    'S247': {'dev-replace.c': ('.ufo/waves/round-45/frozen/src/dev-replace.c',
                               'f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a')},
    'S248': {'systemd.kill.xml': ('.ufo/waves/round-45/frozen/src/systemd.kill.xml',
                                  '448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72')},
    'S249': {'capture.txt': ('.ufo/waves/round-45/frozen/hostcap/capture.txt',
                             'f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70')},
}
CITE = {'GR1': ('cmdline.c', 'vsprintf.c', 'kstrtox.c', 'sysfs.c'),
        'GR2': ('dev-replace.c', 'scrub.c', 'sysfs.c', 'ioctl.c'),
        'GR3': ('systemd.kill.xml', 'btrfs-scrub@.service', 'scrub.c', 'capture.txt')}
MARK_ENTRY = '## Gate status — round 48 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 48 admission'
MARK_README = ('btrfs-scrub-grounding-r45.md', 'admitted round 48')
NEGATE_RE = re.compile(r'unadmitted|not admitted|never admitted|stay pending|stays pending')
VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (holds|partly|fails)')
ANY_VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (\w+)')
HASH_RE = re.compile(r'SECTION SHA256: ([0-9a-f]{64})')
QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` ([^:]+):(\d+): "(.*)"\s*$')
CITE_RE = re.compile(r'\b([A-Za-z0-9_.@+-]+\.[a-z0-9]+):(\d+)\b')
PREDICATE = 'structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3'


def universe(row):
    n = row[2:]
    return ([(f'R48RevGR{n}{x}', 'reviewer') for x in 'abc']
            + [(f'R48CritGR{n}{x}', 'critic') for x in 'abc'])


class DupKey(ValueError):
    pass


def no_dups(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise DupKey(k)
        out[k] = v
    return out


def git(lane, *args):
    return subprocess.run(['git', '-C', lane, *args], capture_output=True, stdin=subprocess.DEVNULL)


def show(lane, rev, path):
    p = git(lane, 'show', f'{rev}:{path}')
    return p.stdout if p.returncode == 0 else None


def load_obj(lane, rev, path):
    b = show(lane, rev, path)
    if b is None:
        return None
    try:
        v = json.loads(b.decode('utf-8'), object_pairs_hook=no_dups)
    except Exception:
        return None
    return v if isinstance(v, dict) else None


NEXT = {'GR1': '## GR2', 'GR2': '## GR3', 'GR3': '## How this changes OS triage'}


def row_extent(lines, row):
    """-> ((i, j) of the F1-bound extent, None) or (None, problem)."""
    idxs = [i for i, ln in enumerate(lines) if ln == f'## {row}']
    if not idxs:
        return None, f'{row}: header absent'
    if len(idxs) > 1:
        return None, f'{row}: header occurs {len(idxs)} times'
    i = idxs[0]
    want = NEXT[row]
    js = [j for j, ln in enumerate(lines[i + 1:], start=i + 1) if ln == want]
    if len(js) != 1:
        return None, f'{row}: expected next header {want!r} occurs {len(js)} times'
    j = js[0]
    inner = [ln for ln in lines[i + 1:j] if ln.startswith('## ')]
    if inner:
        return None, f'{row}: unexpected "## " line inside the row: {inner[0][:60]!r}'
    return (i, j), None


def section_hashes(entry):
    """F1: the bound extent is the whole row, from `## GR<n>` up to (exclusive) the
    expected next header; any other `## ` line inside the extent or a missing /
    duplicated expected header fails closed. -> (hashes, structural_ok, problems)."""
    lines = entry.split('\n')
    out = {}
    problems = []
    for row in ROWS:
        ext, prob = row_extent(lines, row)
        if prob:
            problems.append(prob)
            continue
        i, j = ext
        out[row] = hashlib.sha256('\n'.join(lines[i:j]).encode('utf-8')).hexdigest()
    return out, int(not problems), problems


def dispatches(lane, rev):
    """Only the round's one counted wave (WAVE) is read: attempt-1's void w1 never counts."""
    return {WAVE: load_obj(lane, rev, f'{WAVES}/{WAVE}-dispatch.json')}


def bind(lane, rev, disp, seat, role, row):
    """-> (verdict, hash, body, detail) or (None, None, None, reason)."""
    hits = []
    for wave, obj in disp.items():
        if obj is None:
            continue
        tc = obj.get('taskCall')
        tasks = tc.get('tasks') if isinstance(tc, dict) else None
        if not isinstance(tasks, list):
            continue
        for t in tasks:
            if isinstance(t, dict) and t.get('name') == seat:
                hits.append((wave, t.get('agent')))
    if len(hits) != 1:
        return None, None, None, f'dispatched {len(hits)} times'
    wave, agent = hits[0]
    if agent != role:
        return None, None, None, f'agent {agent} != {role}'
    res = load_obj(lane, rev, f'{WAVES}/{wave}-results.json')
    results = res.get('results') if isinstance(res, dict) else None
    if not isinstance(results, list):
        return None, None, None, f'{wave}-results.json unreadable'
    if sum(1 for r in results if isinstance(r, dict) and r.get('name') == seat and r.get('agent') == role) != 1:
        return None, None, None, 'not exactly one results entry'
    rb = show(lane, rev, f'{WAVES}/{wave}/{seat}.md')
    if rb is None:
        return None, None, None, f'no report {wave}/{seat}.md'
    try:
        text = rb.decode('utf-8')
    except UnicodeDecodeError:
        return None, None, None, 'report not UTF-8'
    lines = text.split('\n')
    if len(lines) < 3:
        return None, None, None, 'report too short'
    m = VERDICT_RE.fullmatch(lines[0])
    h = HASH_RE.fullmatch(lines[1])
    if not m or m.group(1) != row:
        return None, None, None, f'first line {lines[0][:80]!r}'
    if not h:
        return None, None, None, f'second line {lines[1][:80]!r}'
    for r, w in ANY_VERDICT_RE.findall('\n'.join(lines[1:])):
        if r != row or w != m.group(2):
            # A2: a self-contradicting report is a negative on its own hash, never a vanished seat
            return 'partly', h.group(1), '\n'.join(lines[2:]), f'contradicting line ROW {r} VERDICT: {w}'
    rest = '\n'.join(lines[2:])
    return m.group(2), h.group(1), rest, f'{wave}/{seat}.md'


def snapshots(lane, rev):
    """-> {(sid, file): lines} for digest-pinned snapshots present at REV."""
    cache = {}
    for sid, files in SNAPSHOTS.items():
        for fname, (path, want_sha) in files.items():
            b = show(lane, rev, path)
            if b is None or hashlib.sha256(b).hexdigest() != want_sha:
                continue
            cache[(sid, fname)] = b.decode('utf-8', errors='replace').split('\n')
    return cache


def verify_citation(cache, fname, lineno):
    """K22 (seat side): cited file:line must resolve in a pinned digest-checked snapshot."""
    cands = [lines for (sid, sf), lines in cache.items() if sf == fname]
    if not cands:
        return False, f'{fname} not a pinned snapshot file'
    if any(1 <= lineno <= len(lines) for lines in cands):
        return True, 'resolves'
    return False, f'{fname}:{lineno} outside all pinned snapshots'


def quote_legs(lane, rev, entry, hashes):
    """K22 (entry side): every Quote line of each row verifies on its pinned snapshot."""
    lines = entry.split('\n')
    cache = snapshots(lane, rev)
    per = {}
    for row in ROWS:
        ext, prob = row_extent(lines, row)
        if hashes.get(row) is None or prob:
            per[row] = {'quotes': 0, 'ok': 0, 'bad': [prob or 'no section hash']}
            continue
        i, j = ext
        n_ok = n_q = 0
        bad = []
        norm = lambda s: ' '.join(s.split())
        for ln in lines[i:j]:
            m = QUOTE_RE.match(ln)
            if not m:
                continue
            n_q += 1
            sid, fname, line_no, want = m.group(1), m.group(2).strip(), int(m.group(3)), m.group(4)
            got = cache.get((sid, fname))
            if got is None:
                bad.append(f'{sid} {fname}: snapshot absent or digest moved')
                continue
            if not (1 <= line_no <= len(got)):
                bad.append(f'{sid} {fname}:{line_no}: outside snapshot ({len(got)} lines)')
                continue
            if norm(want) not in norm(got[line_no - 1]):
                bad.append(f'{sid} {fname}:{line_no}: quote mismatch')
                continue
            n_ok += 1
        per[row] = {'quotes': n_q, 'ok': n_ok, 'bad': bad}
    return per


def report_citations_ok(cache, body, row):
    if len(body.encode('utf-8')) < 300:
        return False, 'report body under 300 bytes'
    if not any(re.search(re.escape(f) + r':\d+', body) for f in CITE[row]):
        return False, 'no file:line citation of the row sources'
    hits = CITE_RE.findall(body)
    if not hits:
        return False, 'no file:line citations'
    for fname, lineno in hits:
        ok, why = verify_citation(cache, fname, int(lineno))
        if not ok:
            return False, why
    return True, f'{len(hits)} citations resolve'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--section-hash', action='store_true')
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    try:
        return run(a, lane)
    except Exception as e:
        print(json.dumps({'counter': 'check-scrub-admission-r48', 'error': f'{type(e).__name__}: {e}',
                          'verdict': 'FAIL'}))
        return 2


def run(a, lane):
    p = git(lane, 'rev-parse', '--verify', a.revision + '^{commit}')
    if p.returncode != 0:
        print(json.dumps({'error': f'cannot resolve {a.revision}'}))
        return 2
    rev = p.stdout.decode().strip()
    eb = show(lane, rev, ENTRY)
    entry = eb.decode('utf-8', errors='replace') if eb else ''
    hashes, structural_ok, problems = section_hashes(entry)
    if a.section_hash:
        print(json.dumps({'revision': rev, 'entry': ENTRY, 'structural_ok': structural_ok,
                          'problems': problems, 'section_sha256': hashes}, sort_keys=True))
        return 0 if len(hashes) == 3 and structural_ok else 2
    if git(lane, 'merge-base', '--is-ancestor', BASE, rev).returncode != 0:
        print(json.dumps({'error': f'base {BASE} is not an ancestor of {rev}', 'base_ok': 0, 'verdict': 'FAIL'}))
        return 2

    quotes = quote_legs(lane, rev, entry, hashes)
    quotes_ok = sum(1 for row in ROWS
                    if quotes[row]['quotes'] > 0 and quotes[row]['ok'] == quotes[row]['quotes'])
    disp = dispatches(lane, rev)
    cache = snapshots(lane, rev)
    per = {}
    verdicts_ok = 0
    for row in ROWS:
        seats = {}
        credited = []   # (seat, role, body-hash) of seats on the current row hash with clean citations
        cite_problems = []
        cur = hashes.get(row)
        for seat, role in universe(row):
            v, h, body, why = bind(lane, rev, disp, seat, role, row)
            seats[seat] = {'verdict': v, 'hash': h, 'detail': why}
            if v and h == cur:
                ok, msg = report_citations_ok(cache, body, row)
                if not ok:
                    cite_problems.append(f'{seat}: {msg}')  # A2: unbound for credit only
                elif v == 'holds':
                    credited.append((seat, role, hashlib.sha256(body.encode()).hexdigest()))
        # A2: a bound-format seat on the current hash that is not `holds` blocks the row
        blocking = [n for n, s in seats.items() if s['verdict'] in ('partly', 'fails') and s['hash'] == cur]
        any_fails = any(s['verdict'] == 'fails' for s in seats.values())
        distinct = len({b for _, _, b in credited}) == len(credited)  # K23
        roles = {r for _, r, _ in credited}
        row_quotes_ok = quotes[row]['quotes'] > 0 and quotes[row]['ok'] == quotes[row]['quotes']
        ok = (cur is not None and not blocking and not any_fails and len(credited) >= 3
              and roles == {'reviewer', 'critic'} and distinct
              and structural_ok == 1 and row_quotes_ok)
        per[row] = {'section_sha256': cur, 'credited': [n for n, _, _ in credited], 'blocking': blocking,
                    'any_fails': any_fails, 'distinct_bodies': distinct,
                    'unbound_for_citation': cite_problems, 'quotes': quotes[row], 'row_ok': ok,
                    'seats': seats}
        verdicts_ok += ok

    sb = show(lane, rev, 'SKILL.md')
    rb = show(lane, rev, 'corpus/README.md')
    entry_lines = entry.split('\n')
    skill_lines = (sb or b'').decode(errors='replace').split('\n')
    readme_lines = (rb or b'').decode(errors='replace').split('\n')
    marks = {'entry': MARK_ENTRY in entry_lines,
             'skill': MARK_SKILL in skill_lines,  # F2: exact line, not a prefix
             'readme': any(all(x in ln for x in MARK_README) and not NEGATE_RE.search(ln)
                           for ln in readme_lines)}  # F2: negation earns nothing
    marks_ok = sum(marks.values())
    ok = structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3
    print(json.dumps({
        'counter': 'check-scrub-admission-r48', 'revision': rev, 'base': BASE, 'base_ok': 1,
        'predicate': PREDICATE, 'structural_ok': structural_ok, 'structural_problems': problems,
        'quotes_ok': quotes_ok, 'verdicts_ok': verdicts_ok, 'marks_ok': marks_ok, 'marks': marks,
        'waves_seen': sorted(disp), 'per_row': per, 'verdict': 'PASS' if ok else 'FAIL'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
