#!/usr/bin/env python3
"""Round-43 C2 counter (frozen before data): btrfs scrub record rows SR1, SR3, SR6.

Entry: corpus/knowledge/btrfs-scrub-record-r43.md. It re-grounds the two rows round 42 withdrew (SC1 and SC3 of
corpus/knowledge/btrfs-scrub-record-r42.md; routed defect R42-C2-REGROUND) and grounds at the kernel source the
running-state limit round 42 stated only from a host errno (its SC4 narrowing). Each row is a `## SR<n>` section:
  **Statement.** <lane text>
  **Quote.** `S237` scrub.c:<line>: "<text>"     or     **Quote.** `S240` ioctl.c:<line>: "<text>"
  **Host reading.** <text naming capture.txt:<line>>
Snapshots: scrub.c is the round-42 frozen btrfs-progs v7.1 file (S237), ioctl.c the round-43 frozen Linux
v7.2.11 fs/btrfs/ioctl.c (S240); capture.txt the round-43 own-work host capture (S241). sha256 pinned below.

Per row the counter checks:
  quote_ok   - at least one quote, every quote's text occurs on its named line of a digest-checked snapshot, the
               id matches the file (scrub.c <-> S237, ioctl.c <-> S240), at least one quote lies in the row's
               frozen window, and SR6 quotes both files (QUALITY 79, 86).
  prop_ok    - the statement text carries every frozen proposition token of the row (QUALITY 87: the rule cell
               is read, not only the quote cells).
  host_ok    - SR6 carries a host line naming an existing capture line; SR1/SR3 host lines, when present, too.
  verdict_ok - verdict binding (QUALITY 89/90, routed R42-VERDICT-FORM): the seat is a task of
               `.ufo/waves/round-43/w2-dispatch.json` (taskCall.tasks, same name and agent role) with exactly one
               entry of the same name and role in `w2-results.json`; the declared verdict line is the JSON
               field `verdict_line` when the recorded output parses as a JSON object, otherwise the output's
               first non-empty line, and it must be exactly `ROW SR<n> VERDICT: <holds|partly|fails>` for that
               row (anchored, a line of its own); the committed report `.ufo/waves/round-43/w2/<name>.md` must
               open with that identical line. A mention elsewhere counts for nothing. Seats per row:
               `C2RevSR<n>` (reviewer) and `C2CritSR<n>` (critic). Row ok iff both bound and both `holds`, or
               no bound `fails` and every `partly` is followed by a bound residual reviewer `C2ResSR<n>`
               (`residual-dispatch.json`, `residual-results.json`, `.ufo/waves/round-43/residual/<name>.md`,
               same binding) reading `holds`. An unbound counted seat makes its row not ok.
Global conjuncts:
  sources_ok - S240 and S241 are rows at the revision absent at the base, status `mined`, opened 2026-10-26,
               used-by naming the entry; S240 kind `code`, its anchor names v7.2.11; S241 kind `own-work`;
               S237 is a row whose used-by names the entry; the entry's `source:` line names S237, S240, S241.
  novelty    - each row's novelty token has 0 hits at the base in corpus/knowledge and SKILL.md outside the
               round-42 entry's appended "## Corrections — round-42 wave 2" section (the uncounted text these
               rows re-ground).
  pointer_ok - the first 20 lines of corpus/knowledge/btrfs-scrub-record-r42.md name
               `btrfs-scrub-record-r43.md` (a header-reading sweep sees the supersession).

Reported outside the predicate: transcripts_bound (bound verdict lines also found in a seat transcript under
~/.omp/agent/sessions; host-local, uncommitted, cannot tell forged committed records from real ones).

Predicate (same sentence in the declaration and the receipt label):
  PASS iff rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1
  and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1.

Usage: python3 tools/check-scrub-record-r43.py --revision <REV> [--lane <repo>] [--sessions <dir>]
Writes nothing. Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = '6951ead90566b2d74f7c45b4efca29246badad64'
ENTRY = 'corpus/knowledge/btrfs-scrub-record-r43.md'
OLD = 'corpus/knowledge/btrfs-scrub-record-r42.md'
OLD_CORR = '## Corrections — round-42 wave 2'
WAVE = '.ufo/waves/round-43'
SNAP = {
    'scrub.c': ('.ufo/waves/round-42/frozen/src/scrub.c', 'S237',
                '48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801'),
    'ioctl.c': (f'{WAVE}/frozen/src/ioctl.c', 'S240',
                '7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01'),
}
CAPTURE = (f'{WAVE}/frozen/hostcap/capture.txt',
           'f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556')
ROWS = {
    'SR1': {'novelty': 'O_TRUNC', 'props': ['O_TRUNC', '_tmp', 'rename', 'unlink'], 'host_required': False,
            'windows': [('scrub.c', 476, 540), ('scrub.c', 897, 935), ('scrub.c', 1480, 1500),
                        ('scrub.c', 1715, 1725)]},
    'SR3': {'novelty': 'scrub_resumed_stats', 'props': ['scrub_resumed_stats', 't_start', 'do_print', '-B', 'err'],
            'host_required': False,
            'windows': [('scrub.c', 795, 830), ('scrub.c', 860, 870), ('scrub.c', 1245, 1300),
                        ('scrub.c', 1328, 1336), ('scrub.c', 1425, 1445), ('scrub.c', 1498, 1510),
                        ('scrub.c', 1686, 1710), ('scrub.c', 1828, 1836)]},
    'SR6': {'novelty': 'is_scrub_running_in_kernel',
            'props': ['is_scrub_running_in_kernel', 'CAP_SYS_ADMIN', 'EPERM', 'running'], 'host_required': True,
            'windows': [('scrub.c', 1189, 1206), ('scrub.c', 1940, 1950), ('scrub.c', 336, 344),
                        ('ioctl.c', 3066, 3075), ('ioctl.c', 3118, 3140), ('ioctl.c', 5578, 5584)]},
}
OPENED = '2026-10-26'
QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d{3,})` (scrub\.c|ioctl\.c):(\d+): "(.+)"\s*$')
HOST_RE = re.compile(r'capture\.txt:(\d+)')
PREDICATE = ('rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 '
             'and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1')


def show(lane, rev, path):
    p = subprocess.run(['git', '-C', lane, 'show', f'{rev}:{path}'], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def resolve(lane, rev):
    p = subprocess.run(['git', '-C', lane, 'rev-parse', '--verify', rev + '^{commit}'],
                       capture_output=True, text=True)
    if p.returncode != 0:
        print(json.dumps({'error': f'cannot resolve {rev}'}))
        sys.exit(2)
    return p.stdout.strip()


def sections(text):
    out, cur = {}, None
    for ln in text.splitlines():
        m = re.match(r'^## (SR\d)\s*$', ln)
        if m:
            cur = m.group(1)
            out.setdefault(cur, [])
            continue
        if re.match(r'^## ', ln):
            cur = None
            continue
        if cur:
            out[cur].append(ln)
    return out


def statement(lines):
    """The statement cell: from the **Statement.** line up to the first Quote/Host line."""
    out, on = [], False
    for ln in lines:
        if ln.startswith('**Statement.**'):
            on = True
        elif ln.startswith('**Quote.**') or ln.startswith('**Host reading.**'):
            on = False
        if on:
            out.append(ln)
    return '\n'.join(out)


def registry(text):
    rows = {}
    for ln in (text or '').splitlines():
        if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', ln):
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if len(cells) == 11:
                rows[cells[0]] = cells
    return rows


def load_json(lane, rev, path):
    b = show(lane, rev, path)
    if b is None:
        return None
    try:
        return json.loads(b)
    except ValueError:
        return None


def declared_line(output):
    try:
        obj = json.loads(output)
    except (ValueError, TypeError):
        obj = None
    if isinstance(obj, dict):
        v = obj.get('verdict_line')
        return v if isinstance(v, str) else None
    for ln in output.splitlines():
        if ln.strip():
            return ln.strip()
    return None


def first_line(text):
    for ln in text.splitlines():
        if ln.strip():
            return ln.rstrip('\r')
    return None


def bound(lane, rev, wave, name, role, row):
    """(verdict or None, line) for one seat bound through dispatch + results + report first line."""
    disp = load_json(lane, rev, f'{WAVE}/{wave}-dispatch.json') or {}
    res = load_json(lane, rev, f'{WAVE}/{wave}-results.json') or {}
    tasks = ((disp.get('taskCall') or {}).get('tasks')) or []
    if sum(1 for t in tasks if t.get('name') == name and t.get('agent') == role) != 1:
        return None, None
    ent = [r for r in (res.get('results') or []) if r.get('name') == name and r.get('agent') == role]
    if len(ent) != 1 or not isinstance(ent[0].get('output'), str):
        return None, None
    line = declared_line(ent[0]['output'])
    m = re.fullmatch(r'ROW (SR\d) VERDICT: (holds|partly|fails)', line or '')
    if not m or m.group(1) != row:
        return None, None
    rep = show(lane, rev, f'{WAVE}/{wave}/{name}.md')
    if rep is None or first_line(rep.decode(errors='replace')) != line:
        return None, None
    return m.group(2), line


def transcript_has(sessions, name, line):
    for pat in (os.path.join(sessions, '*', f'{name}.jsonl'), os.path.join(sessions, '*', f'{name}-*.jsonl')):
        for f in glob.glob(pat):
            try:
                with open(f, errors='replace') as fh:
                    if line in fh.read():
                        return True
            except OSError:
                pass
    return False


def novelty_hits(lane, token):
    p = subprocess.run(['git', '-C', lane, 'grep', '-n', '-F', '--', token, BASE, '--', 'corpus/knowledge',
                        'SKILL.md'], capture_output=True, text=True)
    old = (show(lane, BASE, OLD) or b'').decode(errors='replace').split('\n')
    corr_from = next((i + 1 for i, ln in enumerate(old) if ln.startswith(OLD_CORR)), None)
    hits = 0
    for ln in p.stdout.splitlines():
        parts = ln.split(':', 3)
        if len(parts) < 4:
            continue
        path, num = parts[1], int(parts[2]) if parts[2].isdigit() else 0
        if path == OLD and corr_from is not None and num >= corr_from:
            continue
        hits += 1
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--sessions', default=os.path.expanduser('~/.omp/agent/sessions/-Projects-shokunin'))
    a = ap.parse_args()
    rev = resolve(a.lane, a.revision)

    snaps = {}
    for f, (path, _sid, digest) in SNAP.items():
        b = show(a.lane, rev, path)
        snaps[f] = b.decode(errors='replace').split('\n') if b and hashlib.sha256(b).hexdigest() == digest else None
    cb = show(a.lane, rev, CAPTURE[0])
    cap = cb.decode(errors='replace').split('\n') if cb and hashlib.sha256(cb).hexdigest() == CAPTURE[1] else None

    base_hits = {row: novelty_hits(a.lane, spec['novelty']) for row, spec in ROWS.items()}

    eb = show(a.lane, rev, ENTRY)
    entry = eb.decode(errors='replace') if eb else ''
    secs = sections(entry)
    reg = registry((show(a.lane, rev, 'corpus/SOURCES.md') or b'').decode(errors='replace'))
    reg_base = registry((show(a.lane, BASE, 'corpus/SOURCES.md') or b'').decode(errors='replace'))

    per = {}
    quotes_ok = props_ok = host_ok = verdicts_ok = 0
    tbound = tcount = 0
    for row, spec in ROWS.items():
        lines = secs.get(row)
        r = {'present': lines is not None}
        if lines is None:
            per[row] = r
            continue
        qs = [QUOTE_RE.match(ln) for ln in lines if ln.startswith('**Quote.**')]
        good = in_window = bad = 0
        files = set()
        for m in qs:
            if not m:
                bad += 1
                continue
            sid, f, n, q = m.group(1), m.group(2), int(m.group(3)), m.group(4)
            src = snaps.get(f)
            if sid == SNAP[f][1] and src and 1 <= n <= len(src) and q in src[n - 1]:
                good += 1
                files.add(f)
                if any(wf == f and lo <= n <= hi for wf, lo, hi in spec['windows']):
                    in_window += 1
            else:
                bad += 1
        q_ok = good >= 1 and in_window >= 1 and bad == 0 and (row != 'SR6' or files == {'scrub.c', 'ioctl.c'})
        st = statement(lines)
        p_ok = bool(st) and all(t in st for t in spec['props'])
        hl = [ln for ln in lines if ln.startswith('**Host reading.**')]
        hrefs = [int(x) for ln in hl for x in HOST_RE.findall(ln)]
        h_ok = all(cap and 1 <= k <= len(cap) and cap[k - 1].strip() for k in hrefs) and \
            (bool(hrefs) or not spec['host_required']) and (not hl or bool(hrefs))
        n = row[2:]
        v1, l1 = bound(a.lane, rev, 'w2', f'C2RevSR{n}', 'reviewer', row)
        v2, l2 = bound(a.lane, rev, 'w2', f'C2CritSR{n}', 'critic', row)
        vs = [v1, v2]
        resid, lr = None, None
        if 'partly' in vs:
            resid, lr = bound(a.lane, rev, 'residual', f'C2ResSR{n}', 'reviewer', row)
        v_ok = (None not in vs and 'fails' not in vs and resid != 'fails'
                and (all(v == 'holds' for v in vs) or resid == 'holds'))
        for nm, ln in ((f'C2RevSR{n}', l1), (f'C2CritSR{n}', l2), (f'C2ResSR{n}', lr)):
            if ln:
                tcount += 1
                tbound += transcript_has(a.sessions, nm, ln)
        r.update({'quotes': {'good': good, 'in_window': in_window, 'bad': bad, 'files': sorted(files)},
                  'quote_ok': q_ok, 'prop_ok': p_ok, 'host_ok': bool(h_ok),
                  'verdicts': {'rev': v1, 'crit': v2, 'residual': resid}, 'verdict_ok': v_ok})
        quotes_ok += q_ok
        props_ok += p_ok
        host_ok += bool(h_ok)
        verdicts_ok += v_ok
        per[row] = r

    def used_by(c):
        return [p.strip() for p in re.split(r'[,;]', c[10])]

    src = {}
    for sid, kind in (('S240', 'code'), ('S241', 'own-work')):
        c = reg.get(sid)
        src[sid] = bool(c is not None and sid not in reg_base and c[2] == kind and c[7] == 'mined'
                        and c[8] == OPENED and ENTRY in used_by(c)
                        and (sid != 'S240' or 'v7.2.11' in c[5]))
    c = reg.get('S237')
    src['S237'] = bool(c is not None and ENTRY in used_by(c))
    srcline = next((ln for ln in entry.splitlines() if ln.startswith('source:')), '')
    src['source_line'] = all(re.search(rf'\b{s}\b', srcline) for s in ('S237', 'S240', 'S241'))
    sources_ok = int(all(src.values()))

    ob = show(a.lane, rev, OLD)
    head = '\n'.join((ob or b'').decode(errors='replace').split('\n')[:20])
    pointer_ok = int('btrfs-scrub-record-r43.md' in head)

    rows = sum(1 for r in per.values() if r.get('present'))
    nb = sum(base_hits.values())
    ok = (rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1
          and verdicts_ok == 3 and nb == 0 and pointer_ok == 1)
    print(json.dumps({
        'counter': 'check-scrub-record-r43', 'revision': rev, 'base': BASE, 'predicate': PREDICATE,
        'snapshots_ok': all(v is not None for v in snaps.values()), 'capture_ok': cap is not None,
        'rows': rows, 'quotes_ok': quotes_ok, 'props_ok': props_ok, 'host_ok': host_ok,
        'sources_ok': sources_ok, 'sources': src, 'verdicts_ok': verdicts_ok,
        'novelty_base_hits': nb, 'novelty_detail': base_hits, 'pointer_ok': pointer_ok,
        'transcripts_bound': tbound, 'transcripts_checked': tcount,
        'per_row': per, 'verdict': 'PASS' if ok else 'FAIL'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
