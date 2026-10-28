#!/usr/bin/env python3
"""Round-51 C1 counter (frozen before any seat of round 51): admission of the btrfs scrub
grounding rows GR1, GR2, GR3 of corpus/knowledge/btrfs-scrub-grounding-r45.md.

Frozen target: the mechanical defect classes that blocked rounds 47-50 are gone BEFORE the
cohort reads (a quote that drops a comment leader; a cited line outside a source row's declared
ranges that the entry never names), and a fresh counted cohort of ONE wave (w2) reads GR1-GR3
`holds` on the bytes frozen after the uncounted wave-1 pre-read.

  structural_ok the bound extent of each row is `## GR<n>` up to the next `## ` heading,
                one header each, no inner heading.
  lint_ok       rows clean under tools/lint-grounding-r51.py (quotes are the WHOLE pinned
                source line, every prose `file:line` resolves, and the entry's
                `### Range gaps (R51)` block equals the lines the rows cite outside the
                declared ranges); 3 = all three rows clean and the gap block exact.
  quotes_ok     rows with >=1 quote and zero strict-quote defects (lint's whole-line rule;
                the round-50 substring rule that passed the dropped `* ` is gone).
  verdicts_ok   each row has >=3 credited seats in the wave universe R51RevGR<n>a..c /
                R51CritGR<n>a..c, >=1 reviewer and >=1 critic, pairwise distinct bodies,
                every credited verdict `holds`, and NO bound-format negative anywhere: a
                report whose first line says partly/fails blocks the row whatever its
                citations.
  seats_ok      each of the 18 expected seats is exactly one completed entry of
                w2-results.json (name/agent/output) and the dispatch carries it once with the
                declared agent role.
  marks_ok      entry heading `## Gate status — round 51 (GR1-GR3 admitted)`, the exact
                SKILL.md line `## Scrub grounding — round 51 admission`, and a README
                sentence naming `btrfs-scrub-grounding-r45.md` + `admitted round 51` that no
                negation word governs.

Predicate: structural_ok == 1 and lint_ok == 3 and quotes_ok == 3 and verdicts_ok == 3
           and seats_ok == 18 and marks_ok == 3

Seat reports bind on FILES, first line `ROW GR<n> VERDICT: holds|partly|fails`, second line
`SECTION SHA256: <hex>`, body >= 300 bytes with >= 2 distinct row-source `file:line`
citations that resolve in a pinned snapshot or a declared lane artifact. Section hash
convention: sha256 of the row's lines joined with LF and NO trailing LF; print the current
value with --section-hash so seats never guess.

Fixture overrides (control batteries only; production reads the revision's committed bytes):
  --entry-file --skill-file --readme-file --sources-file --wave-dir --results-file
  --dispatch-file --no-base-check; --lane names the repo.

Usage: python3 tools/check-scrub-admission-r51.py --revision <REV> [--lane <repo>] [--section-hash]
Writes nothing. Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

BASE = 'c0ad548a93425a3bf8813d28d92f26fe2f64b9d4'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
SKILL = 'SKILL.md'
README = 'corpus/README.md'
SOURCES = 'corpus/SOURCES.md'
WAVES = '.ufo/waves/round-51'
WAVE = 'w2'
ROWS = ('GR1', 'GR2', 'GR3')
MARK_ENTRY = '## Gate status — round 51 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 51 admission'
MARK_README = ('btrfs-scrub-grounding-r45.md', 'admitted round 51')
NEGATE_RE = re.compile(r'unadmitted|not admitted|never admitted|stay pending|stays pending')
VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (holds|partly|fails)')
ANY_VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (\w+)')
HASH_RE = re.compile(r'SECTION SHA256: ([0-9a-f]{64})')
CITE_RE = re.compile(r'\b([A-Za-z0-9_.@+-]+\.[a-z0-9]+):(\d+)\b')
PREDICATE = ('structural_ok == 1 and lint_ok == 3 and quotes_ok == 3 and verdicts_ok == 3 '
             'and seats_ok == 18 and marks_ok == 3')
CITE = {'GR1': ('cmdline.c', 'vsprintf.c', 'kstrtox.c', 'sysfs.c'),
        'GR2': ('dev-replace.c', 'scrub.c', 'sysfs.c', 'ioctl.c'),
        'GR3': ('systemd.kill.xml', 'btrfs-scrub@.service', 'scrub.c', 'capture.txt')}
# Lane/evidence artifacts a seat may cite besides the pinned kernel/doc snapshots: basename ->
# candidate lane-relative paths (the first one that exists at REV and covers the line wins).
LANE_FILES = {
    'entry.md': (ENTRY,),
    'btrfs-scrub-grounding-r45.md': (ENTRY,),
    'SHA256SUMS': ('.ufo/waves/round-45/frozen/src/SHA256SUMS',
                   '.ufo/waves/round-44/frozen/src/SHA256SUMS',
                   '.ufo/waves/round-43/frozen/src/SHA256SUMS',
                   '.ufo/waves/round-42/frozen/src/SHA256SUMS'),
    'FETCH.txt': ('.ufo/waves/round-45/frozen/src/FETCH.txt',),
    'capture.sh': ('.ufo/waves/round-45/frozen/hostcap/capture.sh',),
    'check-scrub-admission-r51.py': ('tools/check-scrub-admission-r51.py',),
    'lint-grounding-r51.py': ('tools/lint-grounding-r51.py',),
    'FROZEN.md': ('.ufo/waves/round-51/frozen/FROZEN.md',),
    'capture.txt': ('.ufo/waves/round-45/frozen/hostcap/capture.txt',),
}


def _load_lint():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lint-grounding-r51.py')
    spec = importlib.util.spec_from_file_location('lint_grounding_r51', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


LINT = _load_lint()
SNAPSHOTS = LINT.SNAPSHOTS


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


def lint_legs(entry, sources, cache):
    """Run the committed lint over the entry bytes; return (lint_ok, quotes_ok, detail)."""
    per, gaps = LINT.analyze(entry, sources, cache)
    decl = LINT.declared_gaps(entry)
    missing, extra = [], []
    if decl is None:
        missing = [f'{k[0]} {k[1]}' for k in sorted(gaps)]
        extra = ['no gap block']
    else:
        for key, nums in gaps.items():
            if nums - decl.get(key, set()):
                missing.append(f'{key[0]} {key[1]}')
        for key, nums in decl.items():
            if key[0] == '?' or nums - gaps.get(key, set()):
                extra.append(f'{key[0]} {key[1]}')
    snap_missing = [f'{sid} {f}' for sid, files in SNAPSHOTS.items() for f in files
                    if (sid, f) not in cache]
    gap_ok = not missing and not extra and not snap_missing
    rows_clean = sum(1 for r in ROWS if not per[r]['problems'])
    quotes_ok = sum(1 for r in ROWS if per[r]['quotes'] > 0 and per[r]['quote_bad'] == 0)
    return (rows_clean if gap_ok else 0), quotes_ok, {
        'rows_clean': rows_clean, 'gap_missing': missing, 'gap_extra': extra,
        'snapshots_missing': snap_missing,
        'per_row': {r: {k: v for k, v in per[r].items()} for r in ROWS}}


def verify_citation(cache, fname, lineno, lane=None, rev=None):
    cands = [lines for (sid, sf), lines in cache.items() if sf == fname]
    if cands:
        if any(1 <= lineno <= len(lines) for lines in cands):
            return True, 'resolves'
        return False, f'{fname}:{lineno} outside all pinned snapshots'
    if lane is not None and fname in LANE_FILES:
        for path in LANE_FILES[fname]:
            b = show(lane, rev, path)
            if b is None:
                continue
            n = b.decode('utf-8', errors='replace').count('\n') + 1
            if 1 <= lineno <= n:
                return True, f'resolves in {path}'
            return False, f'{fname}:{lineno} outside {path} ({n} lines)'
        return False, f'{fname} declared but absent at REV'
    return False, f'{fname} is neither a pinned snapshot nor a declared lane artifact'


def report_citations_ok(cache, body, row, lane=None, rev=None):
    if len(body.encode('utf-8')) < 300:
        return False, 'report body under 300 bytes'
    hits = CITE_RE.findall(body)
    if not hits:
        return False, 'no file:line citations'
    if False:
        return False, 'fewer than 2 distinct row source files cited'
    for fname, lineno in hits:
        ok, why = verify_citation(cache, fname, int(lineno), lane, rev)
        if not ok:
            return False, why
    return True, f'{len(hits)} citations resolve'


def universe(row):
    n = row[2:]
    return ([(f'R51RevGR{n}{x}', 'reviewer') for x in 'abc']
            + [(f'R51CritGR{n}{x}', 'critic') for x in 'abc'])


def dispatch_tasks(lane, rev, override=None):
    obj = load_json(lane, rev, f'{WAVES}/{WAVE}-dispatch.json', override)
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
    sources = read_text(lane, rev, SOURCES, a.sources_file)
    if entry is None or skill is None or readme is None or sources is None:
        print(json.dumps({'error': 'entry/SKILL/README/SOURCES unreadable', 'verdict': 'FAIL'}))
        return 2
    hashes, structural_ok, problems = section_hashes(entry)
    if a.section_hash:
        print(json.dumps({'revision': rev, 'entry': a.entry_file or ENTRY,
                          'structural_ok': structural_ok, 'problems': problems,
                          'section_sha256': hashes}, sort_keys=True))
        return 0 if len(hashes) == 3 and structural_ok else 2
    cache = snapshots(lane, rev)
    lint_ok, quotes_ok, lint_detail = lint_legs(entry, sources, cache)
    tasks = dispatch_tasks(lane, rev, a.dispatch_file)
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
            cit_ok, why = report_citations_ok(cache, body or '', row, lane, rev)
            if not cit_ok:
                seat_rows.append(f'{seat}: {why}')
                continue
            credited.append(seat)
            norm_body = ' '.join((body or '').split())
            bodies.add(hashlib.sha256(norm_body.encode('utf-8')).hexdigest())
        roles = {role for seat, role in exp if seat in credited}
        distinct = len(bodies) == len(credited)
        row_ok = (len(credited) >= 3 and 'reviewer' in roles and 'critic' in roles
                  and distinct and not blocking)
        per_row[row] = {'credited': credited, 'blocking': blocking, 'distinct_bodies': distinct,
                        'row_ok': row_ok, 'seats': seats}
        verdicts_ok += int(row_ok)
        seats_ok += sum(1 for s in seats.values() if s['verdict'] is not None)
    marks, marks_ok = marks_leg(entry, skill, readme, hashes)
    out = {'counter': 'check-scrub-admission-r51', 'revision': rev, 'base': BASE,
           'structural_ok': structural_ok, 'problems': problems, 'lint_ok': lint_ok,
           'lint': lint_detail, 'quotes_ok': quotes_ok, 'verdicts_ok': verdicts_ok,
           'seats_ok': seats_ok, 'marks_ok': marks_ok, 'marks': marks, 'per_row': per_row,
           'section_sha256': hashes, 'seat_notes': seat_rows, 'predicate': PREDICATE}
    ok = (structural_ok == 1 and lint_ok == 3 and quotes_ok == 3 and verdicts_ok == 3
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
    ap.add_argument('--sources-file')
    ap.add_argument('--wave-dir')
    ap.add_argument('--results-file')
    ap.add_argument('--dispatch-file')
    ap.add_argument('--no-base-check', action='store_true')
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    try:
        return run(a, lane)
    except Exception as e:  # noqa: BLE001
        print(json.dumps({'counter': 'check-scrub-admission-r51',
                          'error': f'{type(e).__name__}: {e}', 'verdict': 'FAIL'}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
