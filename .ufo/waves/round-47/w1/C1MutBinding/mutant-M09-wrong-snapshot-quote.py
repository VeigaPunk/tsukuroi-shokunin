#!/usr/bin/env python3
"""Round-47 C1 counter (frozen before data): admission of the btrfs scrub grounding rows GR1, GR2, GR3.

Round 46 left all three rows pending: GR2 read `partly` on its narrowed bytes by the counted
residual critic (`.ufo/waves/round-46/r1/V46ResCritGR2.md`) — the setup ordering omitted the
filesystem-closing `-EAGAIN` return (scrub.c:3094-3095) and the suspend sentence implied every
suspension path cancels the scrub, where only the unmount suspend path is pinned
(dev-replace.c:1143-1144). Round 47 amends GR2 accordingly (pre-wave, by the L1) and re-reads
all three rows with counted seats.

Closures carried from the round-46 wave findings (frozen-rule amendments, applied before any seat):
  F1 (w1/C2RevCounter.md)   a GR row's bound bytes must be exactly its row: fail closed when any
                            line strictly inside the row starts with `## ` (an unbound tail) or
                            when the row header occurs more than once (structural_ok leg).
  F2 (w1/C2RevCounter.md)   admission marks must not be grantable to negating text: the SKILL mark
                            is an exact line, the README mark rejects lines carrying an explicit
                            negation of admission.
  F3 (w1/C2RevCounter.md)   a deeply nested dispatch JSON must degrade to a leg result, never an
                            empty stdout: every parse failure is caught and reported in-band.
  K22 (w1/C2CritControls.md) cited file:line locations must resolve: every `**Quote.**` line in a
                            row is verified against the pinned digest-checked snapshot (normalized
                            containment), and every file:line citation in a counted seat report must
                            name a pinned snapshot file and an existing line.
  K23 (w1/C2CritControls.md) the counted seats bound for a row must not be byte-identical: the
                            bound report bodies (beyond their two binding lines) must be pairwise
                            distinct.

Sizing for two amendment rounds (round-46 lesson R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT): admission is
per-row and every committed round-47 wave's seats count; the universe per row is two reviewers and
two critics plus two residual generations (`R47ResRevGR<n>`/`R47ResCritGR<n>`,
`R47Res2RevGR<n>`/`R47Res2CritGR<n>`), so a row read `partly` may be amended and re-read, and
amended once more and re-read again, without exhausting the counted universe.

Usage: python3 tools/check-scrub-admission-r47.py --revision <REV> [--lane <repo>] [--section-hash]
Writes nothing. Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = '916019057147d7e9ba6b137647b2cee26decf4b8'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
WAVES = '.ufo/waves/round-47'
ROWS = ('GR1', 'GR2', 'GR3')
# pinned digest-checked snapshots the rows cite: S-id -> {file -> (path, sha256)}
SNAPSHOTS = {
    'S237': {'scrub.c': ('.ufo/waves/round-42/frozen/src/scrub.c',
                         '48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801')},
    'S242': {'scrub.c': ('.ufo/waves/round-44/frozen/src/scrub.c',
                         'f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8')},
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
        'GR2': ('dev-replace.c', 'scrub.c', 'sysfs.c'),
        'GR3': ('systemd.kill.xml', 'btrfs-scrub@.service', 'scrub.c', 'capture.txt')}
MARK_ENTRY = '## Gate status — round 47 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 47 admission'
MARK_README = ('btrfs-scrub-grounding-r45.md', 'admitted round 47')
NEGATE_RE = re.compile(r'unadmitted|not admitted|never admitted|stay pending|stays pending')
VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (holds|partly|fails)')
ANY_VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (\w+)')
HASH_RE = re.compile(r'SECTION SHA256: ([0-9a-f]{64})')
QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` ([^:]+):(\d+): "(.*)"\s*$')
CITE_RE = re.compile(r'\b([A-Za-z0-9_.@+-]+\.[a-z0-9]+):(\d+)\b')
PREDICATE = 'structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3'


def universe(row):
    n = row[2:]
    return [(f'R47RevGR{n}a', 'reviewer'), (f'R47RevGR{n}b', 'reviewer'),
            (f'R47CritGR{n}a', 'critic'), (f'R47CritGR{n}b', 'critic'),
            (f'R47ResRevGR{n}', 'reviewer'), (f'R47ResCritGR{n}', 'critic'),
            (f'R47Res2RevGR{n}', 'reviewer'), (f'R47Res2CritGR{n}', 'critic')]


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
    p = git(lane, 'ls-tree', '--name-only', f'{rev}:{WAVES}')
    if p.returncode != 0:
        return {}
    out = {}
    for name in p.stdout.decode(errors='replace').splitlines():
        if name.endswith('-dispatch.json'):
            out[name[:-len('-dispatch.json')]] = load_obj(lane, rev, f'{WAVES}/{name}')
    return out


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
            return None, None, None, f'contradicting line ROW {r} VERDICT: {w}'
    rest = '\n'.join(lines[2:])
    if len(rest.encode('utf-8')) < 300:
        return None, None, None, 'report body under 300 bytes'
    if not any(re.search(re.escape(f) + r':\d+', rest) for f in CITE[row]):
        return None, None, None, 'no file:line citation of the row sources'
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
            cands = [v for (s2, f2), v in cache.items() if f2 == fname]
            got = next((c for c in cands if 1 <= line_no <= len(c) and norm(want) in norm(c[line_no - 1])), None)
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


def report_citations_ok(cache, body):
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
        print(json.dumps({'counter': 'check-scrub-admission-r47', 'error': f'{type(e).__name__}: {e}',
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
        bodies = []
        cite_problems = []
        for seat, role in universe(row):
            v, h, body, why = bind(lane, rev, disp, seat, role, row)
            seats[seat] = {'verdict': v, 'hash': h, 'detail': why}
            if v and h == hashes.get(row):
                ok, msg = report_citations_ok(cache, body)
                if not ok:
                    cite_problems.append(f'{seat}: {msg}')
                else:
                    bodies.append(hashlib.sha256(body.encode()).hexdigest())
        cur = hashes.get(row)
        on_cur = [s for s in seats.values() if s['verdict'] and s['hash'] == cur]
        any_fails = any(s['verdict'] == 'fails' for s in seats.values())
        distinct = len(set(bodies)) == len(bodies) == len(on_cur)  # K23
        row_quotes_ok = quotes[row]['quotes'] > 0 and quotes[row]['ok'] == quotes[row]['quotes']
        ok = (cur is not None and not any_fails and len(on_cur) >= 2 and distinct
              and all(s['verdict'] == 'holds' for s in on_cur)
              and structural_ok == 1 and row_quotes_ok and not cite_problems)
        per[row] = {'section_sha256': cur, 'bound_on_current': len(on_cur), 'any_fails': any_fails,
                    'distinct_bodies': distinct, 'citations_ok': not cite_problems,
                    'citation_problems': cite_problems, 'quotes': quotes[row], 'row_ok': ok,
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
        'counter': 'check-scrub-admission-r47', 'revision': rev, 'base': BASE, 'base_ok': 1,
        'predicate': PREDICATE, 'structural_ok': structural_ok, 'structural_problems': problems,
        'quotes_ok': quotes_ok, 'verdicts_ok': verdicts_ok, 'marks_ok': marks_ok, 'marks': marks,
        'waves_seen': sorted(disp), 'per_row': per, 'verdict': 'PASS' if ok else 'FAIL'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
