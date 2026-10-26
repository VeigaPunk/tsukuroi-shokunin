#!/usr/bin/env python3
"""Round-44 C2 counter (frozen before data): btrfs scrub record rows SR7, SR8, SR9.

Entry: corpus/knowledge/btrfs-scrub-record-r44.md. SR7 is the success direction of the scrub-progress ioctl the
round-43 SR6 cites (when the kernel answers 0, ENOTCONN, ENODEV); SR8 the per-device `scrub_speed_max` sysfs
attribute (mode, read format, write parsing, 0 = no limit); SR9 the scrub timer and service Arch packages and what
`-B` and `KillSignal=SIGINT` do to a running scrub. Each row is a `## SR<n>` section:
  **Statement.** <lane text>
  **Quote.** `S<id>` <file>:<line>: "<text>"
  **Host reading.** <text naming capture.txt:<line>>
Snapshot keys are (source id, file name): (S237, scrub.c) the round-42 btrfs-progs v7.1 cmds/scrub.c; (S240,
ioctl.c) the round-43 Linux v7.2.11 fs/btrfs/ioctl.c; (S242, scrub.c) and (S243, sysfs.c) the round-44 Linux v7.2.11
fs/btrfs/scrub.c and sysfs.c; (S244, btrfs-scrub@.timer | btrfs-scrub@.service | PKGBUILD) the Arch btrfs-progs
packaging tag 7.1-1; capture.txt the round-44 own-work host capture (S245). sha256 pinned below.

Per row:
  quote_ok   - at least one quote, every quote's text occurs on its named line of a digest-checked snapshot, the
               (id, file) pair is a known snapshot, at least one quote lies in the row's frozen window, and the row
               quotes every file its spec requires (SR7: kernel scrub.c and ioctl.c; SR8: sysfs.c and kernel
               scrub.c; SR9: the timer, the service, PKGBUILD and progs scrub.c) (QUALITY 79, 86).
  prop_ok    - the statement cell carries every frozen proposition token of the row (QUALITY 87).
  host_ok    - every row carries a host line naming existing capture lines (QUALITY 86: a host value beside the
               upstream rule, never instead of it).
  verdict_ok - binding (QUALITY 89/90; closes the two round-43 binding gaps, `SKILL.md` "Scrub record re-grounded —
               round 43"): the seat is a task of `.ufo/waves/round-44/w2-dispatch.json` (taskCall.tasks, same name and
               agent role, exactly once) with exactly one result of the same name and role in `w2-results.json`. The
               declared line: if the recorded output parses as a JSON object it must hold a string `verdict_line`, and a
               `verdict` key, when present, must equal that line's verdict word (a contradiction binds nothing);
               otherwise the output's FIRST line exactly — no leading blank line, no leading or trailing whitespace.
               It must fullmatch `ROW SR<n> VERDICT: <holds|partly|fails>` for that row, and the committed report
               `.ufo/waves/round-44/w2/<name>.md` must have that identical text as its first line (raw, no blank
               line before it, no padding). Seats per row: `C2RevSR<n>` (reviewer) and `C2CritSR<n>` (critic). Row ok
               iff both bound and both `holds`, or no bound `fails` and every `partly` is followed by a bound residual
               reviewer `C2ResSR<n>` (`residual-dispatch.json`, `residual-results.json`,
               `.ufo/waves/round-44/residual/<name>.md`, same binding) reading `holds`. An unbound counted seat makes
               its row not ok.
Global:
  sources_ok - S242, S243, S244 (kind `code`) and S245 (kind `own-work`) are rows absent at the base, status `mined`,
               opened 2026-10-26, used-by naming the entry; S242/S243 anchors name v7.2.11, S244's names 7.1-1; S237
               and S240 are rows whose used-by names the entry; the entry's `source:` line opens with an id list
               (the S-ids before any other text) that holds S237, S240, S242, S243, S244 and S245 (an id named
               only later in the line's prose does not count; pre-data control K17).
  novelty    - each row's novelty token has 0 hits at the base in corpus/knowledge and SKILL.md.
  pointer_ok - the first 20 lines of corpus/knowledge/btrfs-scrub-record-r43.md name `btrfs-scrub-record-r44.md`.

Reported outside the predicate: transcripts_bound (bound verdict lines also found in a seat transcript under
~/.omp/agent/sessions; host-local, uncommitted, cannot tell forged committed records from real ones).

Predicate (same sentence in the declaration and the receipt label):
  PASS iff rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1
  and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1.

Usage: python3 tools/check-scrub-record-r44.py --revision <REV> [--lane <repo>] [--sessions <dir>]
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

BASE = '98020ece0674e0b569ee23aed10ffbee355b248e'
ENTRY = 'corpus/knowledge/btrfs-scrub-record-r44.md'
OLD = 'corpus/knowledge/btrfs-scrub-record-r43.md'
WAVE = '.ufo/waves/round-44'
F44 = f'{WAVE}/frozen/src'
SNAP = {
    ('S237', 'scrub.c'): ('.ufo/waves/round-42/frozen/src/scrub.c',
                          '48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801'),
    ('S240', 'ioctl.c'): ('.ufo/waves/round-43/frozen/src/ioctl.c',
                          '7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01'),
    ('S242', 'scrub.c'): (f'{F44}/scrub.c', 'f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8'),
    ('S243', 'sysfs.c'): (f'{F44}/sysfs.c', 'ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43'),
    ('S244', 'btrfs-scrub@.timer'): (f'{F44}/btrfs-scrub@.timer',
                                     '9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad'),
    ('S244', 'btrfs-scrub@.service'): (f'{F44}/btrfs-scrub@.service',
                                       'eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252'),
    ('S244', 'PKGBUILD'): (f'{F44}/PKGBUILD', '3b803e8b05d84900fcdab3513720c8005345acd1fe34ded6eaa3b7596c10ce98'),
}
CAPTURE = (f'{WAVE}/frozen/hostcap/capture.txt',
           'efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900')
ROWS = {
    'SR7': {'novelty': 'ENOTCONN', 'props': ['btrfs_scrub_progress', 'scrub_ctx', 'ENOTCONN', 'ENODEV', 'EINPROGRESS'],
            'requires': {('S242', 'scrub.c'), ('S240', 'ioctl.c')},
            'windows': [(('S242', 'scrub.c'), 3140, 3165), (('S242', 'scrub.c'), 3215, 3226),
                        (('S242', 'scrub.c'), 3321, 3337), (('S240', 'ioctl.c'), 3126, 3145)]},
    'SR8': {'novelty': 'memparse', 'props': ['scrub_speed_max', '0644', 'memparse', 'EINVAL', 'no limit'],
            'requires': {('S243', 'sysfs.c'), ('S242', 'scrub.c')},
            'windows': [(('S243', 'sysfs.c'), 70, 76), (('S243', 'sysfs.c'), 2019, 2050),
                        (('S243', 'sysfs.c'), 2108, 2116), (('S242', 'scrub.c'), 1365, 1385)]},
    'SR9': {'novelty': 'KillSignal',
            'props': ['btrfs-scrub@', 'OnCalendar=monthly', 'Persistent=true', 'KillSignal=SIGINT', '-B',
                      'BTRFS_IOC_SCRUB_CANCEL'],
            'requires': {('S244', 'btrfs-scrub@.timer'), ('S244', 'btrfs-scrub@.service'), ('S244', 'PKGBUILD'),
                         ('S237', 'scrub.c')},
            'windows': [(('S244', 'btrfs-scrub@.timer'), 1, 11), (('S244', 'btrfs-scrub@.service'), 1, 10),
                        (('S244', 'PKGBUILD'), 99, 101), (('S237', 'scrub.c'), 412, 444),
                        (('S237', 'scrub.c'), 1286, 1296), (('S237', 'scrub.c'), 1510, 1548),
                        (('S237', 'scrub.c'), 960, 972)]},
}
OPENED = '2026-10-26'
QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d{3,})` (scrub\.c|ioctl\.c|sysfs\.c|btrfs-scrub@\.timer|'
                      r'btrfs-scrub@\.service|PKGBUILD):(\d+): "(.+)"\s*$')
HOST_RE = re.compile(r'capture\.txt:(\d+)')
VERDICT_RE = re.compile(r'ROW (SR\d) VERDICT: (holds|partly|fails)')
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
    out, on = [], False
    for ln in lines:
        if ln.startswith('**Statement.**'):
            on = True
        elif ln.startswith('**Quote.**') or ln.startswith('**Host reading.**'):
            on = False
        if on:
            out.append(ln)
    return '\n'.join(out)


def host_block(lines):
    out, on = [], False
    for ln in lines:
        if ln.startswith('**Host reading.**'):
            on = True
        elif ln.startswith('**Quote.**') or ln.startswith('**Statement.**'):
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
    """The one declared verdict line, or None (unbound)."""
    try:
        obj = json.loads(output)
    except (ValueError, TypeError):
        obj = None
    if isinstance(obj, dict):
        v = obj.get('verdict_line')
        if not isinstance(v, str):
            return None
        m = VERDICT_RE.fullmatch(v)
        if 'verdict' in obj and (not m or obj.get('verdict') != m.group(2)):
            return None
        return v
    if not isinstance(output, str) or not output:
        return None
    return output.split('\n', 1)[0].rstrip('\r')


def bound(lane, rev, wave, name, role, row):
    disp = load_json(lane, rev, f'{WAVE}/{wave}-dispatch.json') or {}
    res = load_json(lane, rev, f'{WAVE}/{wave}-results.json') or {}
    tasks = ((disp.get('taskCall') or {}).get('tasks')) or []
    if sum(1 for t in tasks if t.get('name') == name and t.get('agent') == role) != 1:
        return None, None
    ent = [r for r in (res.get('results') or []) if r.get('name') == name and r.get('agent') == role]
    if len(ent) != 1 or not isinstance(ent[0].get('output'), str):
        return None, None
    line = declared_line(ent[0]['output'])
    m = VERDICT_RE.fullmatch(line or '')
    if not m or m.group(1) != row:
        return None, None
    rep = show(lane, rev, f'{WAVE}/{wave}/{name}.md')
    if rep is None:
        return None, None
    first = rep.decode(errors='replace').split('\n', 1)[0].rstrip('\r')
    if first != line:
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
    return len([ln for ln in p.stdout.splitlines() if ln.strip()])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--sessions', default=os.path.expanduser('~/.omp/agent/sessions/-Projects-shokunin'))
    a = ap.parse_args()
    rev = resolve(a.lane, a.revision)

    snaps = {}
    for key, (path, digest) in SNAP.items():
        b = show(a.lane, rev, path)
        snaps[key] = b.decode(errors='replace').split('\n') if b and hashlib.sha256(b).hexdigest() == digest else None
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
        keys = set()
        for m in qs:
            if not m:
                bad += 1
                continue
            key, n, q = (m.group(1), m.group(2)), int(m.group(3)), m.group(4)
            src = snaps.get(key)
            if src and 1 <= n <= len(src) and q in src[n - 1]:
                good += 1
                keys.add(key)
                if any(wk == key and lo <= n <= hi for wk, lo, hi in spec['windows']):
                    in_window += 1
            else:
                bad += 1
        q_ok = good >= 1 and in_window >= 1 and bad == 0 and spec['requires'] <= keys
        st = statement(lines)
        p_ok = bool(st) and all(t in st for t in spec['props'])
        hb = host_block(lines)
        hrefs = [int(x) for x in HOST_RE.findall(hb)]
        h_ok = bool(cap) and bool(hrefs) and all(1 <= k <= len(cap) and cap[k - 1].strip() for k in hrefs)
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
        r.update({'quotes': {'good': good, 'in_window': in_window, 'bad': bad,
                             'files': sorted('%s:%s' % k for k in keys)},
                  'quote_ok': q_ok, 'prop_ok': p_ok, 'host_ok': h_ok,
                  'verdicts': {'rev': v1, 'crit': v2, 'residual': resid}, 'verdict_ok': v_ok})
        quotes_ok += q_ok
        props_ok += p_ok
        host_ok += h_ok
        verdicts_ok += v_ok
        per[row] = r

    def used_by(c):
        return [p.strip() for p in re.split(r'[,;]', c[10])]

    src = {}
    for sid, kind, tag in (('S242', 'code', 'v7.2.11'), ('S243', 'code', 'v7.2.11'), ('S244', 'code', '7.1-1'),
                           ('S245', 'own-work', None)):
        c = reg.get(sid)
        src[sid] = bool(c is not None and sid not in reg_base and c[2] == kind and c[7] == 'mined'
                        and c[8] == OPENED and ENTRY in used_by(c) and (tag is None or tag in c[5]))
    for sid in ('S237', 'S240'):
        c = reg.get(sid)
        src[sid] = bool(c is not None and ENTRY in used_by(c))
    srcline = next((ln for ln in entry.splitlines() if ln.startswith('source:')), '')
    lead = re.match(r'source:\s*((?:S\d{3,}[\s,]*)+)', srcline)
    ids = set(re.findall(r'S\d{3,}', lead.group(1))) if lead else set()
    src['source_line'] = {'S237', 'S240', 'S242', 'S243', 'S244', 'S245'} <= ids
    sources_ok = int(all(src.values()))

    ob = show(a.lane, rev, OLD)
    head = '\n'.join((ob or b'').decode(errors='replace').split('\n')[:20])
    pointer_ok = int('btrfs-scrub-record-r44.md' in head)

    rows = sum(1 for r in per.values() if r.get('present'))
    nb = sum(base_hits.values())
    ok = (rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1
          and verdicts_ok == 3 and nb == 0 and pointer_ok == 1)
    print(json.dumps({
        'counter': 'check-scrub-record-r44', 'revision': rev, 'base': BASE, 'predicate': PREDICATE,
        'snapshots_ok': all(v is not None for v in snaps.values()), 'capture_ok': cap is not None,
        'rows': rows, 'quotes_ok': quotes_ok, 'props_ok': props_ok, 'host_ok': host_ok,
        'sources_ok': sources_ok, 'sources': src, 'verdicts_ok': verdicts_ok,
        'novelty_base_hits': nb, 'novelty_detail': base_hits, 'pointer_ok': pointer_ok,
        'transcripts_bound': tbound, 'transcripts_checked': tcount,
        'per_row': per, 'verdict': 'PASS' if ok else 'FAIL'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
