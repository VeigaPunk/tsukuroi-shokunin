#!/usr/bin/env python3
"""Round-49 C1 counter (frozen before any seat of round 49): admission of the btrfs scrub
grounding rows GR1, GR2, GR3 of corpus/knowledge/btrfs-scrub-grounding-r45.md.

Frozen target: the three rows are admitted by a fresh counted cohort of ONE wave (w1) that
reads the CORRECTED bytes, and the counter itself proves the correction landed.

  corr_ok       the seven corrections the round-48 counted cohort named are in the bytes
                (C7) and the five defect strings it named are gone (C8). A clean cohort on
                defective bytes fails; corrected bytes with no cohort fail.
  structural_ok the bound extent of each row is `## GR<n>` up to the next `## ` heading,
                one header each, no inner heading (F1 carry-over).
  quotes_ok     every `**Quote.**` line of each row resolves on its digest-pinned snapshot
                at the cited line with the quoted text (K22 carry-over).
  verdicts_ok   each row has >=3 credited seats in the wave universe R49RevGR<n>a..c /
                R49CritGR<n>a..c, >=1 reviewer and >=1 critic, pairwise distinct bodies,
                every credited verdict `holds`, and NO bound-format negative anywhere: a
                report whose first line says partly/fails blocks the row whatever its
                citations (A2 carry-over).
  seats_ok      each of the 18 expected seats is exactly one completed entry of
                w1-results.json (the orchestrator's real schema: name/agent/output) and the
                dispatch carries it once with the declared agent role.
  marks_ok      entry heading `## Gate status — round 49 (GR1-GR3 admitted)`, the exact
                SKILL.md line `## Scrub grounding — round 49 admission`, and a README
                sentence naming `btrfs-scrub-grounding-r45.md` + `admitted round 49` that no
                negation word governs (F2 carry-over).

Predicate: structural_ok == 1 and corr_ok == 1 and quotes_ok == 3 and verdicts_ok == 3
           and seats_ok == 18 and marks_ok == 3

Seat reports bind on FILES, first line `ROW GR<n> VERDICT: holds|partly|fails`, second line
`SECTION SHA256: <hex>`, body >= 300 bytes with file:line citations of the row's sources.
Section hash convention: sha256 of the row's lines joined with LF and NO trailing LF; print
the current value with --section-hash so seats never guess.

Fixture overrides (control batteries only; production reads the revision's committed bytes):
  --entry-file --skill-file --readme-file --wave-dir --results-file --no-base-check
  --skip-anchors-check is not used here; --lane names the repo.

Usage: python3 tools/check-scrub-admission-r49.py --revision <REV> [--lane <repo>] [--section-hash]
Writes nothing. Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = '6256760d1382ce4ce20fcba830d4b2912cfbf12b'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
SKILL = 'SKILL.md'
README = 'corpus/README.md'
WAVES = '.ufo/waves/round-49'
WAVE = 'w1'
ROWS = ('GR1', 'GR2', 'GR3')
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
MARK_ENTRY = '## Gate status — round 49 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 49 admission'
MARK_README = ('btrfs-scrub-grounding-r45.md', 'admitted round 49')
NEGATE_RE = re.compile(r'unadmitted|not admitted|never admitted|stay pending|stays pending')
VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (holds|partly|fails)')
ANY_VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (\w+)')
HASH_RE = re.compile(r'SECTION SHA256: ([0-9a-f]{64})')
QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` ([^:]+):(\d+): "(.*)"\s*$')
CITE_RE = re.compile(r'\b([A-Za-z0-9_.@+-]+\.[a-z0-9]+):(\d+)\b')
PREDICATE = ('structural_ok == 1 and corr_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 '
             'and seats_ok == 18 and marks_ok == 3')
# C7: the corrections the round-48 counted cohort named (CritGR1a clause; CritGR1a host-reading
# mark; CritGR2a item 1, item 2, item 3, item 4; RevGR2a items 1-2).
CORR_REQ = (
    r'leading `0x` or `0X` followed by a hex digit',
    r'\[inference: by ordinary file-mode checks',
    r'is_valid`, dev-replace\.c:1278-1279',
    r'the copy attached\s*\n?\(scrub\.c:3159\)',
    r'an unknown devid gives `-ENODEV`',
    r'dev-replace\.c:1171-1195',
    r'ioctl\.c:3132',
)
# C8: the defect strings those seats named, which must be gone.
CORR_FORBID = (
    r'leading `0x` followed by a hex digit',
    r'which by SR7',
    r'dev-replace\.c:1171-1199',
    r'only sets the state to SUSPENDED',
    r'which it is for a replace in state',
)


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


def read_text(lane, rev, path, override):
    if override:
        try:
            with open(override, 'rb') as fh:
                return fh.read().decode('utf-8')
        except OSError:
            return None
    b = show(lane, rev, path)
    return None if b is None else b.decode('utf-8', errors='replace')


def load_json(lane, rev, path, override):
    if override:
        try:
            with open(override, 'rb') as fh:
                return json.loads(fh.read().decode('utf-8'), object_pairs_hook=no_dups)
        except Exception:
            return None
    b = show(lane, rev, path)
    if b is None:
        return None
    try:
        return json.loads(b.decode('utf-8'), object_pairs_hook=no_dups)
    except Exception:
        return None


def row_extent(lines, row):
    heads = [i for i, ln in enumerate(lines) if ln.strip() == f'## {row}']
    if len(heads) != 1:
        return None, f'{row}: header appears {len(heads)} times'
    i = heads[0]
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith('## ')), len(lines))
    inner = [ln for ln in lines[i + 1:j] if ln.startswith('## ')]
    if inner:
        return None, f'{row}: unexpected "## " line inside the row: {inner[0][:60]!r}'
    return (i, j), None


def section_hashes(entry):
    lines = entry.split('\n')
    out, problems = {}, []
    for row in ROWS:
        ext, prob = row_extent(lines, row)
        if prob:
            problems.append(prob)
            continue
        i, j = ext
        out[row] = hashlib.sha256('\n'.join(lines[i:j]).encode('utf-8')).hexdigest()
    return out, int(not problems), problems


def snapshots(lane, rev):
    cache = {}
    for sid, files in SNAPSHOTS.items():
        for fname, (path, want_sha) in files.items():
            b = show(lane, rev, path)
            if b is None or hashlib.sha256(b).hexdigest() != want_sha:
                continue
            cache[(sid, fname)] = b.decode('utf-8', errors='replace').split('\n')
    return cache


def quote_legs(entry, hashes, cache):
    lines = entry.split('\n')
    per = {}
    norm = lambda s: ' '.join(s.split())
    for row in ROWS:
        ext, prob = row_extent(lines, row)
        if hashes.get(row) is None or prob:
            per[row] = {'quotes': 0, 'ok': 0, 'bad': [prob or 'no section hash']}
            continue
        i, j = ext
        n_ok = n_q = 0
        bad = []
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


def verify_citation(cache, fname, lineno):
    cands = [lines for (sid, sf), lines in cache.items() if sf == fname]
    if not cands:
        return False, f'{fname} not a pinned snapshot file'
    if any(1 <= lineno <= len(lines) for lines in cands):
        return True, 'resolves'
    return False, f'{fname}:{lineno} outside all pinned snapshots'


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


def universe(row):
    n = row[2:]
    return ([(f'R49RevGR{n}{x}', 'reviewer') for x in 'abc']
            + [(f'R49CritGR{n}{x}', 'critic') for x in 'abc'])


def dispatch_tasks(lane, rev):
    obj = load_json(lane, rev, f'{WAVES}/{WAVE}-dispatch.json', None)
    tc = obj.get('taskCall') if isinstance(obj, dict) else None
    tasks = tc.get('tasks') if isinstance(tc, dict) else None
    return {t.get('name'): t.get('agent') for t in tasks if isinstance(t, dict)} if isinstance(tasks, list) else {}


def bind_seat(lane, rev, tasks, results, seat, role, wave_dir, row, hashes, cache):
    if tasks.get(seat) != role:
        return None, None, None, f'dispatch agent {tasks.get(seat)!r} != {role}'
    hits = [r for r in results if isinstance(r, dict) and r.get('name') == seat]
    if len(hits) != 1:
        return None, None, None, 'not exactly one results entry'
    if hits[0].get('agent') != role:
        return None, None, None, f'results agent {hits[0].get("agent")!r} != {role}'
    if not hits[0].get('output'):
        return None, None, None, 'no completed output'
    if wave_dir:
        path = os.path.join(wave_dir, f'{seat}.md')
        try:
            with open(path, 'rb') as fh:
                raw = fh.read()
        except OSError:
            return None, None, None, f'no report {seat}.md'
    else:
        raw = show(lane, rev, f'{WAVES}/{WAVE}/{seat}.md')
        if raw is None:
            return None, None, None, f'no report {seat}.md'
    try:
        text = raw.decode('utf-8')
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
            return 'partly', h.group(1), '\n'.join(lines[2:]), f'contradicting line ROW {r} VERDICT: {w}'
    return m.group(2), h.group(1), '\n'.join(lines[2:]), f'{seat}.md'


def marks_leg(entry, skill, readme, hashes):
    marks = {'entry': MARK_ENTRY in entry.split('\n'),
             'skill': any(ln.strip() == MARK_SKILL for ln in skill.split('\n')),
             'readme': False}
    norm = ' '.join(readme.split())
    name, phrase = MARK_README
    for sentence in re.split(r'(?<=[.!?])\s+', norm):
        if name in sentence and phrase in sentence and not NEGATE_RE.search(sentence):
            marks['readme'] = True
            break
    return marks, sum(1 for v in marks.values() if v)


def run(a, lane):
    rev = a.revision
    if not a.no_base_check:
        if git(lane, 'cat-file', '-e', f'{BASE}^{{commit}}').returncode != 0:
            print(json.dumps({'error': f'base {BASE} unreadable', 'verdict': 'FAIL'}))
            return 2
    entry = read_text(lane, rev, ENTRY, a.entry_file)
    skill = read_text(lane, rev, SKILL, a.skill_file)
    readme = read_text(lane, rev, README, a.readme_file)
    if entry is None or skill is None or readme is None:
        print(json.dumps({'error': 'entry/SKILL/README unreadable', 'verdict': 'FAIL'}))
        return 2
    hashes, structural_ok, problems = section_hashes(entry)
    if a.section_hash:
        print(json.dumps({'revision': rev, 'entry': a.entry_file or ENTRY,
                          'structural_ok': structural_ok, 'problems': problems,
                          'section_sha256': hashes}, sort_keys=True))
        return 0 if len(hashes) == 3 and structural_ok else 2
    cache = snapshots(lane, rev)
    quotes = quote_legs(entry, hashes, cache)
    quotes_ok = sum(1 for r in ROWS if quotes[r]['quotes'] > 0 and not quotes[r]['bad'])
    corr_missing = [p for p in CORR_REQ if not re.search(p, entry)]
    corr_present = [p for p in CORR_FORBID if re.search(p, entry)]
    corr_ok = int(not corr_missing and not corr_present)
    tasks = dispatch_tasks(lane, rev)
    res = load_json(lane, rev, f'{WAVES}/{WAVE}-results.json', a.results_file)
    results = res.get('results') if isinstance(res, dict) else None
    results = results if isinstance(results, list) else []
    seats_ok, verdicts_ok, per_row, seat_rows = 0, 0, {}, []
    for row in ROWS:
        exp = universe(row)
        credited, blocking, seats, bodies = [], [], {}, set()
        for seat, role in exp:
            v, h, body, detail = bind_seat(lane, rev, tasks, results, seat, role,
                                           a.wave_dir, row, hashes, cache)
            seats[seat] = {'verdict': v, 'hash': h, 'detail': detail}
            if v is None:
                seat_rows.append(f'{seat}: unbound ({detail})')
                continue
            if v in ('partly', 'fails'):
                blocking.append(seat)
                continue
            if h != hashes.get(row):
                seat_rows.append(f'{seat}: hash {h} != {hashes.get(row)}')
                continue
            cit_ok, why = report_citations_ok(cache, body or '', row)
            if not cit_ok:
                seat_rows.append(f'{seat}: {why}')
                continue
            credited.append(seat)
            bodies.add(hashlib.sha256((body or '').encode('utf-8')).hexdigest())
        roles = {role for seat, role in exp if seat in credited}
        distinct = len(bodies) == len(credited)
        row_ok = (len(credited) >= 3 and 'reviewer' in roles and 'critic' in roles
                  and not blocking)
        per_row[row] = {'credited': credited, 'blocking': blocking, 'distinct_bodies': distinct,
                        'row_ok': row_ok, 'quotes': quotes[row], 'seats': seats}
        verdicts_ok += int(row_ok)
        seats_ok += sum(1 for s in seats.values() if s['verdict'] is not None)
    marks, marks_ok = marks_leg(entry, skill, readme, hashes)
    out = {'counter': 'check-scrub-admission-r49', 'revision': rev, 'base': BASE,
           'structural_ok': structural_ok, 'problems': problems, 'corr_ok': corr_ok,
           'corr_missing': corr_missing, 'corr_forbidden_present': corr_present,
           'quotes_ok': quotes_ok, 'verdicts_ok': verdicts_ok, 'seats_ok': seats_ok,
           'marks_ok': marks_ok, 'marks': marks, 'per_row': per_row,
           'section_sha256': hashes, 'seat_notes': seat_rows,
           'predicate': PREDICATE}
    ok = (structural_ok == 1 and corr_ok == 1 and quotes_ok == 3 and verdicts_ok == 3
          and seats_ok == 18 and marks_ok == 3)
    out['verdict'] = 'PASS' if ok else 'FAIL'
    print(json.dumps(out, sort_keys=True))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--section-hash', action='store_true')
    ap.add_argument('--entry-file')
    ap.add_argument('--skill-file')
    ap.add_argument('--readme-file')
    ap.add_argument('--wave-dir')
    ap.add_argument('--results-file')
    ap.add_argument('--no-base-check', action='store_true')
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    try:
        return run(a, lane)
    except Exception as e:
        print(json.dumps({'counter': 'check-scrub-admission-r49',
                          'error': f'{type(e).__name__}: {e}', 'verdict': 'FAIL'}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
