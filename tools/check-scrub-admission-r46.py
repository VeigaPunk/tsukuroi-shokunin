#!/usr/bin/env python3
"""Round-46 C2 counter (frozen before data): admission of the pending btrfs scrub grounding rows GR1, GR2, GR3.

Entry: corpus/knowledge/btrfs-scrub-grounding-r45.md (round 45; its depth gate FAILED on binding, rows pending —
SCORECARD "Round 45 — measured outcome", R45-C2-BINDING-CHANNEL). This counter re-binds counted verdicts through
a channel the seat writes itself — its own report file — and binds each verdict to the exact bytes it read.

Legs:
  r45_legs_ok  the frozen round-45 counter, read from REV (`tools/check-scrub-grounding-r45.py`, sha256 must equal
               R45_SHA), run over REV, reports rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1,
               novelty_base_hits 0 and pointer_ok 1 (its verdicts_ok leg, bound to round-45 waves, is ignored).
  section hash for row GR<n> at REV: the entry's lines from the line `## GR<n>` up to, not including, the next line
               that starts with `## `; sha256 of those lines joined with "\\n", UTF-8. `--section-hash` prints them.
  verdicts     counted seat universe (frozen names and roles), per row n in 1..3:
                 V46RevGR<n>a, V46RevGR<n>b   (agent reviewer)    V46CritGR<n>a, V46CritGR<n>b (agent critic)
                 V46ResRevGR<n>               (agent reviewer)    V46ResCritGR<n>              (agent critic)
               A seat BINDS iff, at REV:
                 (1) across every `.ufo/waves/round-46/<wave>-dispatch.json` (any wave name — the binding never
                     names a wave, so a retired or renamed wave cannot strand it), the seat name occurs exactly once
                     in `taskCall.tasks[].name`, with `agent` equal to its role; both JSON files parse as objects
                     with no duplicate key anywhere;
                 (2) that wave's `<wave>-results.json` lists exactly one `results[]` entry with the same name and
                     agent (the orchestrator spawned it; status and output are not read);
                 (3) the seat's report `.ufo/waves/round-46/<wave>/<seat>.md` exists; its FIRST line is exactly
                     `ROW GR<n> VERDICT: <holds|partly|fails>` (n = the seat's row; no leading blank, padding, CR or
                     BOM) and its SECOND line is exactly `SECTION SHA256: <64 lowercase hex>`;
                 (4) no other line of the report matches `ROW GR<d> VERDICT: <word>` with a different row or word;
                 (5) the rest of the report is at least 300 bytes and cites at least one `<file>:<line>` of a file
                     the row quotes (GR1 cmdline.c|vsprintf.c|kstrtox.c|sysfs.c; GR2 dev-replace.c|scrub.c|sysfs.c;
                     GR3 systemd.kill.xml|btrfs-scrub@.service|scrub.c|capture.txt).
               Row ok iff no bound seat of the row reads `fails` (on any hash), and the bound seats whose SECTION
               SHA256 equals the row's section hash at REV number at least 2 and all read `holds`.
  marks_ok     admission marks at REV, one point each: the entry has a line exactly
               `## Gate status — round 46 (GR1-GR3 admitted)`; SKILL.md has a line starting
               `## Scrub grounding — round 46 admission`; corpus/README.md has a line containing both
               `btrfs-scrub-grounding-r45.md` and `admitted round 46`.
  base_ok      BASE resolves and is an ancestor of REV, else exit 2.

Predicate (same sentence in the declaration and the receipt label):
  PASS iff r45_legs_ok == 1 and verdicts_ok == 3 and marks_ok == 3.

Standing limit (not claimed away): committed bytes cannot tell forged orchestrator records and seat reports from
real ones (round-45 control K3); the binding proves shape, spawn record and byte-binding, not authorship.

Usage: python3 tools/check-scrub-admission-r46.py --revision <REV> [--lane <repo>] [--section-hash]
Writes nothing. Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = '2042117cfb724170772f4c128cc2ddba0b61d817'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
R45 = 'tools/check-scrub-grounding-r45.py'
R45_SHA = 'a1eb402dffae97fcefd9bd539529f1cacc5034419b6de06e1f8ac1c08d011331'
WAVES = '.ufo/waves/round-46'
ROWS = ('GR1', 'GR2', 'GR3')
CITE = {'GR1': ('cmdline.c', 'vsprintf.c', 'kstrtox.c', 'sysfs.c'),
        'GR2': ('dev-replace.c', 'scrub.c', 'sysfs.c'),
        'GR3': ('systemd.kill.xml', 'btrfs-scrub@.service', 'scrub.c', 'capture.txt')}
MARK_ENTRY = '## Gate status — round 46 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 46 admission'
MARK_README = ('btrfs-scrub-grounding-r45.md', 'admitted round 46')
VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (holds|partly|fails)')
ANY_VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (\w+)')
HASH_RE = re.compile(r'SECTION SHA256: ([0-9a-f]{64})')
PREDICATE = 'r45_legs_ok == 1 and verdicts_ok == 3 and marks_ok == 3'
R45_LEGS = {'rows': 3, 'quotes_ok': 3, 'props_ok': 3, 'host_ok': 3, 'sources_ok': 1, 'novelty_base_hits': 0,
            'pointer_ok': 1}


def universe(row):
    n = row[2:]
    return [(f'V46RevGR{n}a', 'reviewer'), (f'V46RevGR{n}b', 'reviewer'), (f'V46CritGR{n}a', 'critic'),
            (f'V46CritGR{n}b', 'critic'), (f'V46ResRevGR{n}', 'reviewer'), (f'V46ResCritGR{n}', 'critic')]


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
    except (ValueError, UnicodeDecodeError):
        return None
    return v if isinstance(v, dict) else None


def section_hashes(entry):
    lines = entry.split('\n')
    out = {}
    for row in ROWS:
        try:
            i = lines.index(f'## {row}')
        except ValueError:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].startswith('## '):
            j += 1
        out[row] = hashlib.sha256('\n'.join(lines[i:j]).encode('utf-8')).hexdigest()
    return out


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
    """-> (verdict, hash, detail) or (None, None, reason)."""
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
        return None, None, f'dispatched {len(hits)} times'
    wave, agent = hits[0]
    if agent != role:
        return None, None, f'agent {agent} != {role}'
    res = load_obj(lane, rev, f'{WAVES}/{wave}-results.json')
    results = res.get('results') if isinstance(res, dict) else None
    if not isinstance(results, list):
        return None, None, f'{wave}-results.json unreadable'
    if sum(1 for r in results if isinstance(r, dict) and r.get('name') == seat and r.get('agent') == role) != 1:
        return None, None, 'not exactly one results entry'
    rb = show(lane, rev, f'{WAVES}/{wave}/{seat}.md')
    if rb is None:
        return None, None, f'no report {wave}/{seat}.md'
    try:
        text = rb.decode('utf-8')
    except UnicodeDecodeError:
        return None, None, 'report not UTF-8'
    lines = text.split('\n')
    if len(lines) < 3:
        return None, None, 'report too short'
    m = VERDICT_RE.fullmatch(lines[0])
    h = HASH_RE.fullmatch(lines[1])
    if not m or m.group(1) != row:
        return None, None, f'first line {lines[0][:80]!r}'
    if not h:
        return None, None, f'second line {lines[1][:80]!r}'
    for r, w in ANY_VERDICT_RE.findall('\n'.join(lines[1:])):
        if r != row or w != m.group(2):
            return None, None, f'contradicting line ROW {r} VERDICT: {w}'
    rest = '\n'.join(lines[2:])
    if len(rest.encode('utf-8')) < 300:
        return None, None, 'report body under 300 bytes'
    if not any(re.search(re.escape(f) + r':\d+', rest) for f in CITE[row]):
        return None, None, 'no file:line citation of the row sources'
    return m.group(2), h.group(1), f'{wave}/{seat}.md'


def r45_legs(lane, rev):
    b = show(lane, rev, R45)
    if b is None or hashlib.sha256(b).hexdigest() != R45_SHA:
        return 0, {'error': 'round-45 counter missing or changed'}
    p = subprocess.run([sys.executable, '-', '--revision', rev, '--lane', lane, '--sessions', os.devnull],
                       input=b, capture_output=True)
    try:
        out = json.loads(p.stdout.decode(errors='replace').strip().splitlines()[-1])
    except (ValueError, IndexError):
        return 0, {'error': 'round-45 counter output unreadable', 'rc': p.returncode}
    legs = {k: out.get(k) for k in R45_LEGS}
    return int(all(out.get(k) == v for k, v in R45_LEGS.items())), legs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--section-hash', action='store_true')
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    p = git(lane, 'rev-parse', '--verify', a.revision + '^{commit}')
    if p.returncode != 0:
        print(json.dumps({'error': f'cannot resolve {a.revision}'}))
        return 2
    rev = p.stdout.decode().strip()
    eb = show(lane, rev, ENTRY)
    entry = eb.decode('utf-8', errors='replace') if eb else ''
    hashes = section_hashes(entry)
    if a.section_hash:
        print(json.dumps({'revision': rev, 'entry': ENTRY, 'section_sha256': hashes}, sort_keys=True))
        return 0 if len(hashes) == 3 else 2
    if git(lane, 'merge-base', '--is-ancestor', BASE, rev).returncode != 0:
        print(json.dumps({'error': f'base {BASE} is not an ancestor of {rev}', 'base_ok': 0, 'verdict': 'FAIL'}))
        return 2

    legs_ok, legs = r45_legs(lane, rev)
    disp = dispatches(lane, rev)
    per = {}
    verdicts_ok = 0
    for row in ROWS:
        seats = {}
        for seat, role in universe(row):
            v, h, why = bind(lane, rev, disp, seat, role, row)
            seats[seat] = {'verdict': v, 'hash': h, 'detail': why}
        cur = hashes.get(row)
        on_cur = [s for s in seats.values() if s['verdict'] and s['hash'] == cur]
        any_fails = any(s['verdict'] == 'fails' for s in seats.values())
        ok = (cur is not None and not any_fails and len(on_cur) >= 2
              and all(s['verdict'] == 'holds' for s in on_cur))
        per[row] = {'section_sha256': cur, 'bound_on_current': len(on_cur), 'any_fails': any_fails,
                    'row_ok': ok, 'seats': seats}
        verdicts_ok += ok

    sb = show(lane, rev, 'SKILL.md')
    rb = show(lane, rev, 'corpus/README.md')
    marks = {'entry': MARK_ENTRY in entry.split('\n'),
             'skill': any(ln.startswith(MARK_SKILL) for ln in (sb or b'').decode(errors='replace').split('\n')),
             'readme': any(all(x in ln for x in MARK_README)
                           for ln in (rb or b'').decode(errors='replace').split('\n'))}
    marks_ok = sum(marks.values())
    ok = legs_ok == 1 and verdicts_ok == 3 and marks_ok == 3
    print(json.dumps({
        'counter': 'check-scrub-admission-r46', 'revision': rev, 'base': BASE, 'base_ok': 1, 'predicate': PREDICATE,
        'r45_legs_ok': legs_ok, 'r45_legs': legs, 'verdicts_ok': verdicts_ok, 'marks_ok': marks_ok, 'marks': marks,
        'waves_seen': sorted(disp), 'per_row': per, 'verdict': 'PASS' if ok else 'FAIL'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
