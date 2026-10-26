#!/usr/bin/env python3
"""Round-42 C2 counter (frozen before data): the btrfs scrub status record, rows SC1-SC5.

Entry: corpus/knowledge/btrfs-scrub-record-r42.md. Each row is a `## SC<n>` section carrying
  **Statement.** <lane text>
  **Quote.** `S<id>` <scrub.c|CHANGES>:<line>: "<text>"          (one or more)
  **Host reading.** <text naming capture.txt:<line>>
The counter checks, per row: (quote) at least one quote whose text occurs on the named line of the frozen
snapshot (`.ufo/waves/round-42/frozen/src/`, sha256 pinned below) and whose line lies inside the row's frozen
source window, and every quote on the row resolves the same way; (novelty) the row text carries its frozen
token, and the token has no hit at the base in corpus/knowledge or SKILL.md; (host) the host line names a
line that exists in the frozen capture (sha256 pinned). Registry (sources_ok): every cited id is a row at the
revision that is absent at the base, opened 2026-10-26, status `mined`, used-by naming the entry.

Verdict binding (round-41 routed defect R41-GUARD-BYPASS, QUALITY 89). A row verdict counts only through the
orchestrator's records committed at the revision: the seat must be a task of `w2-dispatch.json`
(`taskCall.tasks`, name and agent role), have a `w2-results.json` entry with the same name and role, whose
final output carries exactly one `ROW SC<n> VERDICT: <holds|partly|fails>` line, and the committed report
`.ufo/waves/round-42/w2/<name>.md` must carry that identical line. Seats per row: `C2RevSC<n>` (reviewer) and
`C2CritSC<n>` (critic). A row's verdict is ok iff both bound verdicts are `holds`, or each `partly` is followed
by a bound residual reviewer `C2RevSC<n>c` (`residual-dispatch.json`, `residual-results.json`,
`.ufo/waves/round-42/residual/C2RevSC<n>c.md`) reading `holds`; any bound `fails` makes the row not ok.
A verdict file without its dispatch and results records counts for nothing (planted verdicts).

Reported outside the predicate: `transcripts_bound` — how many bound verdict lines also occur in a seat
transcript `<name>.jsonl` / `<name>-<k>.jsonl` under ~/.omp/agent/sessions (host-local, uncommitted; a
cross-check against forged orchestrator files, which the committed-bytes predicate cannot tell apart).

Predicate (same sentence in the declaration and the receipt label):
  PASS iff rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and sources_ok == 1
  and verdicts_ok == 5 and novelty_base_hits == 0.

Usage: python3 tools/check-scrub-record-r42.py --revision <REV> [--lane <repo>] [--sessions <dir>]
Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = 'c8efaa3f120834541f8de1e5e0367e8d1593bae6'
ENTRY = 'corpus/knowledge/btrfs-scrub-record-r42.md'
WAVE = '.ufo/waves/round-42'
SNAP = {
    'scrub.c': '48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801',
    'CHANGES': 'bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22',
}
CAPTURE = (f'{WAVE}/frozen/hostcap/capture.txt',
           '942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c')
ROWS = {
    'SC1': {'token': 'LOCK_EX', 'windows': [('scrub.c', 446, 535)]},
    'SC2': {'token': 'scrub status:1', 'windows': [('scrub.c', 826, 895)]},
    'SC3': {'token': 'status recording disabled',
            'windows': [('scrub.c', 1110, 1125), ('scrub.c', 1186, 1206), ('scrub.c', 1330, 1340),
                        ('scrub.c', 1498, 1512)]},
    'SC4': {'token': '_SCRUB_FS_STAT_MIN', 'windows': [('scrub.c', 280, 330), ('scrub.c', 1925, 1945)]},
    'SC5': {'token': 'scrub_speed_max', 'windows': [('scrub.c', 1208, 1220), ('CHANGES', 460, 470)]},
}
OPENED = '2026-10-26'
QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d{3,})` (scrub\.c|CHANGES):(\d+): "(.+)"\s*$')
HOST_RE = re.compile(r'^\*\*Host reading\.\*\*.*?capture\.txt:(\d+)')
VERDICT_RE = re.compile(r'(?m)^ROW (SC\d) VERDICT: (holds|partly|fails)[ \t]*$')
ANYV_RE = re.compile(r'(?m)^ROW (SC\d) VERDICT: (holds|partly|fails)\b')


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
        m = re.match(r'^## (SC\d)\s*$', ln)
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


def bound(lane, rev, wave, name, role, row):
    """Return (verdict or None, verdict line) for one seat bound through dispatch + results + report."""
    disp = load_json(lane, rev, f'{WAVE}/{wave}-dispatch.json') or {}
    res = load_json(lane, rev, f'{WAVE}/{wave}-results.json') or {}
    tasks = ((disp.get('taskCall') or {}).get('tasks')) or []
    if not any(t.get('name') == name and t.get('agent') == role for t in tasks):
        return None, None
    ent = [r for r in (res.get('results') or []) if r.get('name') == name and r.get('agent') == role]
    if len(ent) != 1 or not isinstance(ent[0].get('output'), str):
        return None, None
    hits = [m for m in VERDICT_RE.finditer(ent[0]['output']) if m.group(1) == row]
    if len(hits) != 1:
        return None, None
    line = hits[0].group(0).strip()
    rep = show(lane, rev, f'{WAVE}/{wave}/{name}.md')
    if rep is None:
        return None, None
    rl = [x.strip() for x in rep.decode(errors='replace').splitlines()]
    if line not in rl:
        return None, None
    words = {m.group(2) for m in ANYV_RE.finditer('\n'.join(rl)) if m.group(1) == row}
    if len(words) != 1:
        return None, None
    return hits[0].group(2), line


def transcript_has(sessions, name, line):
    pats = [os.path.join(sessions, '*', f'{name}.jsonl'), os.path.join(sessions, '*', f'{name}-*.jsonl')]
    for pat in pats:
        for f in glob.glob(pat):
            try:
                with open(f, errors='replace') as fh:
                    if line in fh.read():
                        return True
            except OSError:
                pass
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--sessions', default=os.path.expanduser('~/.omp/agent/sessions/-Projects-shokunin'))
    a = ap.parse_args()
    rev = resolve(a.lane, a.revision)

    snaps = {}
    for f, digest in SNAP.items():
        b = show(a.lane, rev, f'{WAVE}/frozen/src/{f}')
        snaps[f] = b.decode(errors='replace').split('\n') if b and hashlib.sha256(b).hexdigest() == digest else None
    cb = show(a.lane, rev, CAPTURE[0])
    cap = cb.decode(errors='replace').split('\n') if cb and hashlib.sha256(cb).hexdigest() == CAPTURE[1] else None

    base_hits = 0
    for spec in ROWS.values():
        p = subprocess.run(['git', '-C', a.lane, 'grep', '-c', '-F', '--', spec['token'], BASE, '--',
                            'corpus/knowledge', 'SKILL.md'], capture_output=True, text=True)
        base_hits += sum(int(ln.rsplit(':', 1)[1]) for ln in p.stdout.splitlines() if ln.rsplit(':', 1)[-1].isdigit())

    eb = show(a.lane, rev, ENTRY)
    entry = eb.decode(errors='replace') if eb else ''
    secs = sections(entry)
    reg = registry((show(a.lane, rev, 'corpus/SOURCES.md') or b'').decode(errors='replace'))
    reg_base = registry((show(a.lane, BASE, 'corpus/SOURCES.md') or b'').decode(errors='replace'))

    per, cited = {}, set()
    quotes_ok = novelty_ok = host_ok = verdicts_ok = 0
    tbound = tcount = 0
    for row, spec in ROWS.items():
        lines = secs.get(row)
        r = {'present': lines is not None}
        if lines is None:
            per[row] = r
            continue
        text = '\n'.join(lines)
        qs = [QUOTE_RE.match(ln) for ln in lines if ln.startswith('**Quote.**')]
        good, in_window, bad = 0, 0, 0
        for m in qs:
            if not m:
                bad += 1
                continue
            sid, f, n, q = m.group(1), m.group(2), int(m.group(3)), m.group(4)
            cited.add(sid)
            src = snaps.get(f)
            if src and 1 <= n <= len(src) and q in src[n - 1]:
                good += 1
                if any(wf == f and lo <= n <= hi for wf, lo, hi in spec['windows']):
                    in_window += 1
            else:
                bad += 1
        r['quotes'] = {'good': good, 'in_window': in_window, 'bad': bad}
        q_ok = good >= 1 and in_window >= 1 and bad == 0
        n_ok = spec['token'] in text
        hm = [HOST_RE.match(ln) for ln in lines if ln.startswith('**Host reading.**')]
        h_ok = bool(hm) and all(m and cap and 1 <= int(m.group(1)) <= len(cap) and cap[int(m.group(1)) - 1].strip()
                                for m in hm)
        n = row[2:]
        v1, l1 = bound(a.lane, rev, 'w2', f'C2RevSC{n}', 'reviewer', row)
        v2, l2 = bound(a.lane, rev, 'w2', f'C2CritSC{n}', 'critic', row)
        vs = [v1, v2]
        resid, lr = None, None
        if 'partly' in vs:
            resid, lr = bound(a.lane, rev, 'residual', f'C2RevSC{n}c', 'reviewer', row)
        v_ok = (None not in vs and 'fails' not in vs and resid != 'fails'
                and (all(v == 'holds' for v in vs) or resid == 'holds'))
        for nm, ln in ((f'C2RevSC{n}', l1), (f'C2CritSC{n}', l2), (f'C2RevSC{n}c', lr)):
            if ln:
                tcount += 1
                tbound += transcript_has(a.sessions, nm, ln)
        r.update({'quote_ok': q_ok, 'novelty_ok': n_ok, 'host_ok': h_ok,
                  'verdicts': {'rev': v1, 'crit': v2, 'residual': resid}, 'verdict_ok': v_ok})
        quotes_ok += q_ok
        novelty_ok += n_ok
        host_ok += h_ok
        verdicts_ok += v_ok
        per[row] = r

    src_detail = {}
    for sid in sorted(cited):
        c = reg.get(sid)
        ok = (c is not None and sid not in reg_base and c[7] == 'mined' and c[8] == OPENED
              and ENTRY in [p.strip() for p in re.split(r'[,;]', c[10])])
        src_detail[sid] = ok
    sources_ok = int(bool(cited) and all(src_detail.values()))
    rows = sum(1 for r in per.values() if r.get('present'))

    verdict = (rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and sources_ok == 1
               and verdicts_ok == 5 and base_hits == 0)
    print(json.dumps({
        'counter': 'check-scrub-record-r42', 'revision': rev, 'base': BASE,
        'predicate': ('rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and sources_ok == 1 '
                      'and verdicts_ok == 5 and novelty_base_hits == 0'),
        'snapshots_ok': all(v is not None for v in snaps.values()), 'capture_ok': cap is not None,
        'rows': rows, 'quotes_ok': quotes_ok, 'novelty_ok': novelty_ok, 'host_ok': host_ok,
        'sources_ok': sources_ok, 'sources': src_detail, 'verdicts_ok': verdicts_ok,
        'novelty_base_hits': base_hits, 'transcripts_bound': tbound, 'transcripts_checked': tcount,
        'per_row': per, 'verdict': 'PASS' if verdict else 'FAIL'}, sort_keys=True))
    return 0 if verdict else 1


if __name__ == '__main__':
    sys.exit(main())
