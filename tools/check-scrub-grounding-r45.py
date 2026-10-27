#!/usr/bin/env python3
"""Round-45 C2 counter (frozen before data): btrfs scrub grounding rows GR1, GR2, GR3.

Entry: corpus/knowledge/btrfs-scrub-grounding-r45.md. Each row grounds one round-44 `[inference]` on pinned source:
GR1 how `memparse` parses a `scrub_speed_max` write (base 0 radix, one K..E suffix in either case, factor 1024,
overflow to ULLONG_MAX, sysfs EINVAL on trailing text); GR2 a device replace runs `btrfs_scrub_dev` with
is_dev_replace true on the source devid and any non-replace scrub is refused with EINPROGRESS while a replace is
ongoing; GR3 what systemd v262 sends on `systemctl stop` of the packaged scrub service (KillSignal SIGINT to the
control group, SIGCONT, SIGKILL after TimeoutStopSec) and this host's 5 s DefaultTimeoutStopSec drop-in.
Row shape (`## GR<n>` sections):
  **Statement.** <lane text>
  **Quote.** `S<id>` <file>:<line>: "<text>"
  **Host reading.** <text naming capture.txt:<line>>
Snapshot keys (source id, file name) with pinned sha256: (S246, cmdline.c | vsprintf.c | kstrtox.c) and (S247,
dev-replace.c) and (S248, systemd.kill.xml) in .ufo/waves/round-45/frozen/src; (S242, scrub.c), (S243, sysfs.c),
(S244, btrfs-scrub@.service) in .ufo/waves/round-44/frozen/src; (S237, scrub.c) the round-42 btrfs-progs v7.1
snapshot; capture.txt the round-45 own-work host capture (S249).

Per row:
  quote_ok   - at least one quote; every quote's (id, file) is a known snapshot and its text occurs on the named
               line of the digest-checked snapshot AND is substantial: at least 10 characters or the whole stripped
               line, and at least half of the stripped line's length (closes the round-44 gutted-quote gap,
               w1/C2RevCounter F1); at least one quote lies in a frozen window of the row; the row quotes every file
               it requires (GR1: cmdline.c, kstrtox.c, sysfs.c; GR2: dev-replace.c, kernel scrub.c; GR3:
               systemd.kill.xml, btrfs-scrub@.service, progs scrub.c).
  prop_ok    - the statement carries every frozen proposition token of the row (QUALITY 87).
  host_ok    - the row's host block names existing, non-empty capture.txt lines (QUALITY 86).
  verdict_ok - binding (QUALITY 81/89/90). Seats per row: `C2RevGR<n>` (reviewer) and `C2CritGR<n>` (critic) of
               wave `w1`: a task of `.ufo/waves/round-45/w1-dispatch.json` (taskCall.tasks, same name and agent,
               exactly once) with exactly one result of the same name and agent in `w1-results.json`. Both JSON
               files must be objects that parse with no duplicate key anywhere (else nothing binds; closes
               C2MutBinding F1/F4). The result `output` must be a string. Its declared text: if the string parses as
               JSON (no duplicate keys) and the value is an object, it must hold a string `verdict_line`, and a
               `verdict` key, when present, must equal that line's verdict word; if the value is a JSON string, that
               string is the text; any other JSON value binds nothing; otherwise the raw string is the text. The
               declared line is the text's FIRST line exactly (no leading blank, no padding, no CR), and must
               fullmatch `ROW GR<n> VERDICT: <holds|partly|fails>`; the text must hold no other `ROW GR<n> VERDICT:`
               line with a different verdict word. The committed report `.ufo/waves/round-45/w1/<name>.md` must have
               the identical first line and no contradicting `ROW GR<n> VERDICT:` line. Row ok iff both bound and
               both `holds`, or no bound `fails` and every `partly` is answered by a bound residual reviewer
               `C2ResGR<n>` of wave `r1` (`r1-dispatch.json`, `r1-results.json`, `.ufo/waves/round-45/r1/<name>.md`,
               same binding) reading `holds`. An unbound counted seat makes its row not ok.
Global:
  base_ok    - BASE resolves and is an ancestor of REV (closes the round-44 orphan-repo vacuity, F3); otherwise the
               counter exits 2.
  sources_ok - registry rows are read only inside `## Registry` and outside fenced blocks, and an S-id appearing on
               more than one row-shaped line anywhere in the file makes sources_ok 0 (closes the round-44
               last-duplicate-wins gap, F2). S246, S247 (kind code, anchors naming v7.2.11), S248 (kind docs, anchor
               naming v262) and S249 (kind own-work) are rows absent at the base, status `mined`, opened 2026-10-27,
               used-by naming the entry; S237, S242, S243 and S244 have used-by naming the entry; the entry's
               `source:` line opens with an id list holding S246, S247, S248, S249, S242, S243, S244 and S237.
  novelty    - each row's novelty token has 0 hits at the base in corpus/knowledge and SKILL.md.
  pointer_ok - corpus/knowledge/btrfs-scrub-record-r44.md has a `## Round-45` heading whose section names
               `btrfs-scrub-grounding-r45.md`.

Reported outside the predicate: transcripts_bound (bound verdict lines also found in a seat transcript under
~/.omp/agent/sessions; host-local, cannot tell forged committed records from real ones).

Predicate (same sentence in the declaration and the receipt label):
  PASS iff rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1
  and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1.

Usage: python3 tools/check-scrub-grounding-r45.py --revision <REV> [--lane <repo>] [--sessions <dir>]
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

BASE = '5bbd5ff588120fd8e7c744695351a6978b4241c1'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
OLD = 'corpus/knowledge/btrfs-scrub-record-r44.md'
WAVE = '.ufo/waves/round-45'
F45 = f'{WAVE}/frozen/src'
F44 = '.ufo/waves/round-44/frozen/src'
SNAP = {
    ('S246', 'cmdline.c'): (f'{F45}/cmdline.c', '1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d'),
    ('S246', 'vsprintf.c'): (f'{F45}/vsprintf.c', 'cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca'),
    ('S246', 'kstrtox.c'): (f'{F45}/kstrtox.c', '0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4'),
    ('S247', 'dev-replace.c'): (f'{F45}/dev-replace.c',
                                'f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a'),
    ('S248', 'systemd.kill.xml'): (f'{F45}/systemd.kill.xml',
                                   '448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72'),
    ('S242', 'scrub.c'): (f'{F44}/scrub.c', 'f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8'),
    ('S243', 'sysfs.c'): (f'{F44}/sysfs.c', 'ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43'),
    ('S244', 'btrfs-scrub@.service'): (f'{F44}/btrfs-scrub@.service',
                                       'eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252'),
    ('S237', 'scrub.c'): ('.ufo/waves/round-42/frozen/src/scrub.c',
                          '48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801'),
}
CAPTURE = (f'{WAVE}/frozen/hostcap/capture.txt',
           'f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70')
ROWS = {
    'GR1': {'novelty': 'simple_strtoull',
            'props': ['memparse', 'simple_strtoull', 'octal', '1024', 'ULLONG_MAX', 'EINVAL'],
            'requires': {('S246', 'cmdline.c'), ('S246', 'kstrtox.c'), ('S243', 'sysfs.c')},
            'windows': [(('S246', 'cmdline.c'), 142, 200), (('S246', 'vsprintf.c'), 79, 115),
                        (('S246', 'kstrtox.c'), 26, 40), (('S243', 'sysfs.c'), 2030, 2046)]},
    'GR2': {'novelty': 'btrfs_dev_replace_is_ongoing',
            'props': ['btrfs_scrub_dev', 'is_dev_replace', 'btrfs_dev_replace_is_ongoing', 'EINPROGRESS',
                      'scrub context'],
            'requires': {('S247', 'dev-replace.c'), ('S242', 'scrub.c')},
            'windows': [(('S247', 'dev-replace.c'), 698, 704), (('S247', 'dev-replace.c'), 1255, 1269),
                        (('S242', 'scrub.c'), 3079, 3081), (('S242', 'scrub.c'), 3146, 3153)]},
    'GR3': {'novelty': 'DefaultTimeoutStopSec',
            'props': ['KillSignal', 'SIGINT', 'control-group', 'SIGCONT', 'SIGKILL', 'DefaultTimeoutStopSec',
                      '5 s'],
            'requires': {('S248', 'systemd.kill.xml'), ('S244', 'btrfs-scrub@.service'), ('S237', 'scrub.c')},
            'windows': [(('S248', 'systemd.kill.xml'), 62, 116), (('S244', 'btrfs-scrub@.service'), 1, 10),
                        (('S237', 'scrub.c'), 412, 424)]},
}
OPENED = '2026-10-27'
QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d{3,})` ([A-Za-z0-9@._-]+):(\d+): "(.+)"\s*$')
HOST_RE = re.compile(r'capture\.txt:(\d+)')
VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (holds|partly|fails)')
ANY_VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (\w+)')
ROWLINE_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
PREDICATE = ('rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 '
             'and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1')


class DupKey(ValueError):
    pass


def no_dups(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise DupKey(k)
        out[k] = v
    return out


def strict_json(text):
    return json.loads(text, object_pairs_hook=no_dups)


def git(lane, *args):
    return subprocess.run(['git', '-C', lane, *args], capture_output=True, stdin=subprocess.DEVNULL)


def show(lane, rev, path):
    p = git(lane, 'show', f'{rev}:{path}')
    return p.stdout if p.returncode == 0 else None


def sections(text, pat=r'^## (GR\d)\s*$'):
    out, cur = {}, None
    for ln in text.splitlines():
        m = re.match(pat, ln)
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


def block(lines, start):
    out, on = [], False
    for ln in lines:
        if ln.startswith('**'):
            on = ln.startswith(start)
        if on:
            out.append(ln)
    return '\n'.join(out)


def registry(text):
    """(rows inside ## Registry outside fences, ids seen on more than one row-shaped line anywhere)."""
    rows, seen, dups = {}, {}, set()
    in_reg = fence = False
    for ln in (text or '').splitlines():
        m = ROWLINE_RE.match(ln)
        if m:
            seen[m.group(1)] = seen.get(m.group(1), 0) + 1
            if seen[m.group(1)] > 1:
                dups.add(m.group(1))
        if re.match(r'^ {0,3}(```|~~~)', ln):
            fence = not fence
            continue
        if re.match(r'^## ', ln):
            in_reg = ln.strip() == '## Registry'
            continue
        if in_reg and not fence and m:
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if len(cells) == 11:
                rows[cells[0]] = cells
    return rows, dups


def load_obj(lane, rev, path):
    b = show(lane, rev, path)
    if b is None:
        return {}
    try:
        v = strict_json(b.decode(errors='replace'))
    except ValueError:
        return {}
    return v if isinstance(v, dict) else {}


def declared_text(output):
    try:
        obj = strict_json(output)
    except DupKey:
        return None
    except (ValueError, TypeError):
        return output
    if isinstance(obj, dict):
        v = obj.get('verdict_line')
        if not isinstance(v, str):
            return None
        m = VERDICT_RE.fullmatch(v)
        if 'verdict' in obj and (not m or obj.get('verdict') != m.group(2)):
            return None
        return v
    if isinstance(obj, str):
        return obj
    return None


def contradicts(text, row, word):
    return any(r == row and w != word for r, w in ANY_VERDICT_RE.findall(text))


def bound(lane, rev, wave, name, role, row):
    disp = load_obj(lane, rev, f'{WAVE}/{wave}-dispatch.json')
    res = load_obj(lane, rev, f'{WAVE}/{wave}-results.json')
    tasks = (disp.get('taskCall') or {}).get('tasks') if isinstance(disp.get('taskCall'), dict) else None
    if not isinstance(tasks, list):
        return None, None
    if sum(1 for t in tasks if isinstance(t, dict) and t.get('name') == name and t.get('agent') == role) != 1:
        return None, None
    results = res.get('results')
    if not isinstance(results, list):
        return None, None
    ent = [r for r in results if isinstance(r, dict) and r.get('name') == name and r.get('agent') == role]
    if len(ent) != 1 or not isinstance(ent[0].get('output'), str) or not ent[0]['output']:
        return None, None
    text = declared_text(ent[0]['output'])
    if not isinstance(text, str) or not text:
        return None, None
    line = text.split('\n', 1)[0]
    m = VERDICT_RE.fullmatch(line)
    if not m or m.group(1) != row or contradicts(text, row, m.group(2)):
        return None, None
    rep = show(lane, rev, f'{WAVE}/{wave}/{name}.md')
    if rep is None:
        return None, None
    rtext = rep.decode(errors='replace')
    if rtext.split('\n', 1)[0] != line or contradicts(rtext, row, m.group(2)):
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
                        'SKILL.md'], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if p.returncode not in (0, 1):
        return -1
    return len([ln for ln in p.stdout.splitlines() if ln.strip()])


def quote_good(src, n, q):
    if not src or not (1 <= n <= len(src)):
        return False
    whole = src[n - 1].strip()
    qs = q.strip()
    if not qs or qs not in src[n - 1]:
        return False
    return (len(qs) >= 10 or qs == whole) and 2 * len(qs) >= len(whole)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--sessions', default=os.path.expanduser('~/.omp/agent/sessions/-Projects-shokunin'))
    a = ap.parse_args()
    p = git(a.lane, 'rev-parse', '--verify', a.revision + '^{commit}')
    if p.returncode != 0:
        print(json.dumps({'error': f'cannot resolve {a.revision}'}))
        return 2
    rev = p.stdout.decode().strip()
    if git(a.lane, 'merge-base', '--is-ancestor', BASE, rev).returncode != 0:
        print(json.dumps({'error': f'base {BASE} is not an ancestor of {rev}', 'base_ok': 0, 'verdict': 'FAIL'}))
        return 2

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
    reg, dups = registry((show(a.lane, rev, 'corpus/SOURCES.md') or b'').decode(errors='replace'))
    reg_base, _ = registry((show(a.lane, BASE, 'corpus/SOURCES.md') or b'').decode(errors='replace'))

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
            if quote_good(snaps.get(key), n, q):
                good += 1
                keys.add(key)
                if any(wk == key and lo <= n <= hi for wk, lo, hi in spec['windows']):
                    in_window += 1
            else:
                bad += 1
        q_ok = good >= 1 and in_window >= 1 and bad == 0 and spec['requires'] <= keys
        st = block(lines, '**Statement.**')
        p_ok = bool(st) and all(t in st for t in spec['props'])
        hb = block(lines, '**Host reading.**')
        hrefs = [int(x) for x in HOST_RE.findall(hb)]
        h_ok = bool(cap) and bool(hrefs) and all(1 <= k <= len(cap) and cap[k - 1].strip() for k in hrefs)
        n = row[2:]
        v1, l1 = bound(a.lane, rev, 'w1', f'C2RevGR{n}', 'reviewer', row)
        v2, l2 = bound(a.lane, rev, 'w1', f'C2CritGR{n}', 'critic', row)
        vs = [v1, v2]
        resid, lr = None, None
        if 'partly' in vs:
            resid, lr = bound(a.lane, rev, 'r1', f'C2ResGR{n}', 'reviewer', row)
        v_ok = (None not in vs and 'fails' not in vs and resid != 'fails'
                and (all(v == 'holds' for v in vs) or resid == 'holds'))
        for nm, ln in ((f'C2RevGR{n}', l1), (f'C2CritGR{n}', l2), (f'C2ResGR{n}', lr)):
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
        return [x.strip() for x in re.split(r'[,;]', c[10])]

    src = {'no_duplicate_ids': not dups}
    for sid, kind, tag in (('S246', 'code', 'v7.2.11'), ('S247', 'code', 'v7.2.11'), ('S248', 'docs', 'v262'),
                           ('S249', 'own-work', None)):
        c = reg.get(sid)
        src[sid] = bool(c is not None and sid not in reg_base and c[2] == kind and c[7] == 'mined'
                        and c[8] == OPENED and ENTRY in used_by(c) and (tag is None or tag in c[5]))
    for sid in ('S237', 'S242', 'S243', 'S244'):
        c = reg.get(sid)
        src[sid] = bool(c is not None and ENTRY in used_by(c))
    srcline = next((ln for ln in entry.splitlines() if ln.startswith('source:')), '')
    lead = re.match(r'source:\s*((?:S\d{3,}[\s,]*)+)', srcline)
    ids = set(re.findall(r'S\d{3,}', lead.group(1))) if lead else set()
    src['source_line'] = {'S246', 'S247', 'S248', 'S249', 'S242', 'S243', 'S244', 'S237'} <= ids
    sources_ok = int(all(src.values()))

    ob = show(a.lane, rev, OLD)
    osecs = sections((ob or b'').decode(errors='replace'), pat=r'^## (Round-45)\b.*$')
    pointer_ok = int('btrfs-scrub-grounding-r45.md' in '\n'.join(osecs.get('Round-45', [])))

    rows = sum(1 for r in per.values() if r.get('present'))
    nb = sum(base_hits.values()) if all(v >= 0 for v in base_hits.values()) else 99
    ok = (rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1
          and verdicts_ok == 3 and nb == 0 and pointer_ok == 1)
    print(json.dumps({
        'counter': 'check-scrub-grounding-r45', 'revision': rev, 'base': BASE, 'base_ok': 1, 'predicate': PREDICATE,
        'snapshots_ok': all(v is not None for v in snaps.values()), 'capture_ok': cap is not None,
        'rows': rows, 'quotes_ok': quotes_ok, 'props_ok': props_ok, 'host_ok': host_ok,
        'sources_ok': sources_ok, 'sources': src, 'verdicts_ok': verdicts_ok,
        'novelty_base_hits': nb, 'novelty_detail': base_hits, 'pointer_ok': pointer_ok,
        'transcripts_bound': tbound, 'transcripts_checked': tcount,
        'per_row': per, 'verdict': 'PASS' if ok else 'FAIL'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
