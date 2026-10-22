#!/usr/bin/env python3
"""Depth counter for round 31 claim C1 (axis depth): btrfs repair and maintenance decisions
new to the lane, each grounded in btrfs-progs v7.1 documentation bytes opened this round.

FROZEN PREDICATE (label `new_sourced`; the same sentence is in SCORECARD.md "Round 31 —
declaration" and in every receipt this counter prints):
  a frozen question counts as `new_sourced` when its single row in
  corpus/knowledge/btrfs-repair-r31.json quotes, verbatim at the cited line, a committed
  snapshot whose sha256 equals the question's frozen pin, cites an S### row that is absent
  from the base registry and is `mined` at REV with that pin and URL, states a word of every
  sealed answer-key group in a statement of at least 12 words that shares no 6-word run with the quote,
  carries a frozen novelty token in quote, statement and its one `| [R31-Qnn] ` SKILL.md
  line, and every frozen novelty token of the question has 0 hits in the base corpus.

Rules (each failure is named in the row's `fail` list):
  R1 the JSON parses with no duplicate key, is {"rows": [...]}, and holds exactly one row per
     frozen id Q01..Q08 and no other id (ids are strings);
  R2 row keys are exactly id, question, statement, source, snapshot, line, quote;
  R3 snapshot is a path under `.ufo/waves/round-31/` that exists at REV and whose bytes have
     the frozen sha256 PIN of the question (bytes of btrfs-progs tag v7.1);
  R4 line is a positive int, the quote has 6..25 words and is a substring of that line;
  R5 source matches S\\d{3}; corpus/SOURCES.md at BASE has no row with that id; at REV it has
     exactly one row with that id whose status cell is `mined` and whose text contains the
     frozen URL and the frozen sha256;
  R6 quote, statement and the SKILL.md line each contain at least one frozen novelty token
     (case-insensitive); SKILL.md at REV has exactly one line starting `| [R31-Qnn] ` outside
     fenced code blocks and HTML comments;
  R7 the statement has at least 12 words, contains for every sealed answer-key group of the
     question at least one word whose salted digest is in the group (KEYHASH: sha256 of
     'tsukuroi-r31 ' + the lower-cased word or a piece of it split at '-', '/' or '.', first 16 hex; the plaintext keys are revealed in
     the round-31 lesson after data and must hash to these values), and shares no run of 6
     consecutive words with the quote (lower-cased word tokens);
  R8 novelty: every frozen novelty token of the question has 0 case-insensitive hits in
     SKILL.md, PROVINCE.md and corpus/ at BASE (`git grep -i -F`).

BASE is frozen to 2077e2fa4fa70ea79aa77b6d91f4acd35bc54897 (the round-31 claim base).
Known ceiling (declared): the keys are single words, so a writer who has read the source can
string them together with filler and pass R7, and a dictionary attack on the 16-hex digests is
possible; whether a row is true to its source and useful is judged by wave-2 row reviewers,
never by this counter. The keys are sealed so that a writer who skips the source cannot copy
them from this file.

Usage: python3 tools/check-btrfs-repair-r31.py --revision <REV> [--lane <repo>]
Output: one JSON line per frozen id, then a summary line
  {"predicate": "new_sourced", "new_sourced": N, "of": 8, "revision": ..., "counter_sha256": ...}
Exit 0 when new_sourced == 8, 1 otherwise, 2 on a harness error.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = '2077e2fa4fa70ea79aa77b6d91f4acd35bc54897'
ENTRY = 'corpus/knowledge/btrfs-repair-r31.json'
URL = 'https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/'
QUESTIONS = {
    'Q01': dict(q='Does defragmenting a file on btrfs change space use when snapshots or reflinks share its extents?',
                file='Defragmentation.rst',
                pin='71ad07a3f200284b01d6ee18fc4cc8732fe0542b80556e2cc798247505daa60b',
                tokens=['defragment', 'reflink']),
    'Q02': dict(q='When does btrfs rescue zero-log apply after a failed mount, and what does it lose?',
                file='btrfs-rescue.rst',
                pin='838504fe8b00d221e017457e7953717f3ca2a0e886a48a4c457367b8c4063a1d',
                tokens=['zero-log', 'log tree']),
    'Q03': dict(q='When may btrfs check --repair be run on a damaged filesystem?',
                file='btrfs-check.rst',
                pin='927b67b4ab13f681866e699fcd6ea4917a42ef08e4db1731b0adf065022d955c',
                tokens=['--repair']),
    'Q04': dict(q='What does the autodefrag mount option do and for which workload is it unsuitable?',
                file='ch-mount-options.rst',
                pin='aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f',
                tokens=['autodefrag', 'defragmentation']),
    'Q05': dict(q='What does the btrfs commit= mount option bound, and what is its default and warning limit?',
                file='ch-mount-options.rst',
                pin='aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f',
                tokens=['commit=', 'periodic transaction commit']),
    'Q06': dict(q='What does the nodatacow mount option give up on btrfs?',
                file='ch-mount-options.rst',
                pin='aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f',
                tokens=['nodatacow', 'nodatasum']),
    'Q07': dict(q='How is a failing or missing btrfs device replaced, and what size must the target be?',
                file='btrfs-replace.rst',
                pin='da4bf595f072a96a309535c1022b0171a8657a4f207a3d3da73250886fd8bc9e',
                tokens=['btrfs replace', 'replace start']),
    'Q08': dict(q='Which trim mode should a btrfs SSD use: discard=sync, discard=async or periodic fstrim?',
                file='Trim.rst',
                pin='2a114d56f29d727002a981e868cc97e89d7dd77a5e1cf42ad5a9ff05bfcf0ffc',
                tokens=['fstrim']),
}
SALT = 'tsukuroi-r31'
KEYHASH = {
    'Q01': [['e9f83bb8c4fb0c83', 'e042504e4f57919e', '8df0eb4a526f579d', '996b00bd8f1b370d'], ['1e66576b2db2c6d8', '14f7a27a9c172703', '0a272dcbfb26dfc1', '68ddfdcb4477a00b', 'da1d499cd919a133'], ['2bbfee52fcdcb998']],
    'Q02': [['3a4813eea4487192'], ['61e28ad79423b1c7'], ['0b1ca4a2eb109fd8']],
    'Q03': [['c9750f12e3d1243f', '911cf51c6bcc67a5'], ['8c3fc6432ae36fb8']],
    'Q04': [['3d96f80cb16d26f7'], ['799a3d51ae7e194e'], ['5bd906efc6b93c51', 'f1bd9034c4680457']],
    'Q05': [['97a2c6bc7c5443e1', 'fd91650e3a3b2942'], ['0b1ca4a2eb109fd8'], ['74cf638237a546c3'], ['113742ff0d19e837', 'cd033c7f3fc9a42c']],
    'Q06': [['812c2b78f3ecf74e'], ['cad259cab1cc5604', 'c90ae5532c805905', '310b77b4f9eceb8a', '7a3a87e0891cf387'], ['c40ee4515577800c']],
    'Q07': [['0d7c981d8b9cf553'], ['97da85b585bb19c3', '8ea70292222061c3'], ['f7168bd13229f123']],
    'Q08': [['86d37128605fd526'], ['666af48e08924b62'], ['6ca322cbae2da243', 'c77f5f3f237f5170']],
}
ROW_KEYS = {'id', 'question', 'statement', 'source', 'snapshot', 'line', 'quote'}


def clean_env():
    env = {k: v for k, v in os.environ.items()
           if not k.startswith('GIT_') and not k.startswith('LD_') and not k.startswith('PYTHON')}
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                'GIT_CONFIG_SYSTEM': os.devnull, 'GIT_OPTIONAL_LOCKS': '0', 'LC_ALL': 'C',
                'PATH': '/usr/bin:/bin'})
    return env


def git(lane, *args):
    return subprocess.run(['/usr/bin/git', '-C', lane, *args], capture_output=True, env=clean_env())


def show(lane, rev, path):
    p = git(lane, 'show', f'{rev}:{path}')
    return p.stdout if p.returncode == 0 else None


def no_dup(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise ValueError('duplicate key %r' % k)
        seen[k] = v
    return seen


def words(text):
    return re.findall(r"[a-z0-9][a-z0-9=_.+/-]*", text.lower())


def shares_run(a, b, n=6):
    wa, wb = words(a), words(b)
    runs = {tuple(wb[i:i + n]) for i in range(len(wb) - n + 1)}
    return any(tuple(wa[i:i + n]) in runs for i in range(len(wa) - n + 1))


def has_token(text, tokens):
    t = text.lower()
    return any(tok.lower() in t for tok in tokens)


def skill_lines(text, rid):
    out, fence, comment = [], False, False
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith('```') or s.startswith('~~~'):
            fence = not fence
            continue
        if comment:
            if '-->' in ln:
                comment = False
            continue
        if '<!--' in ln and '-->' not in ln.split('<!--', 1)[1]:
            comment = True
            continue
        if not fence and ln.startswith(f'| [R31-{rid}] '):
            out.append(ln)
    return out


def registry_rows(text, sid):
    return [ln for ln in text.splitlines() if re.match(r'^\|\s*' + sid + r'\s*\|', ln)]


def status_cell(row):
    cells = [c.strip() for c in row.strip().strip('|').split('|')]
    return cells


def base_hits(lane, token):
    p = git(lane, 'grep', '-i', '-F', '-c', '-e', token, BASE, '--', 'SKILL.md', 'PROVINCE.md', 'corpus')
    if p.returncode not in (0, 1):
        raise RuntimeError('git grep failed: ' + p.stderr.decode('utf-8', 'replace'))
    return sum(int(x.rsplit(':', 1)[1]) for x in p.stdout.decode().splitlines() if x)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    with open(os.path.abspath(__file__), 'rb') as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    p = git(lane, 'rev-parse', '--verify', a.revision + '^{commit}')
    b = git(lane, 'rev-parse', '--verify', BASE + '^{commit}')
    if p.returncode or b.returncode:
        print(json.dumps({'error': 'revision or base unreadable', 'revision': a.revision}))
        return 2
    rev = p.stdout.decode().strip()
    hits = {}
    try:
        for qid, q in QUESTIONS.items():
            for tok in q['tokens']:
                hits[tok] = base_hits(lane, tok)
    except RuntimeError as e:
        print(json.dumps({'error': str(e)}))
        return 2
    raw = show(lane, rev, ENTRY)
    rows, file_fail = {}, []
    if raw is None:
        file_fail.append('R1 entry absent at revision')
    else:
        try:
            doc = json.loads(raw.decode('utf-8'), object_pairs_hook=no_dup)
            if not isinstance(doc, dict) or set(doc) != {'rows'} or not isinstance(doc['rows'], list):
                raise ValueError('top level is not {"rows": [...]}')
            for r in doc['rows']:
                if not isinstance(r, dict) or not isinstance(r.get('id'), str):
                    raise ValueError('row without a string id')
                rows.setdefault(r['id'], []).append(r)
            extra = sorted(set(rows) - set(QUESTIONS))
            if extra:
                file_fail.append('R1 extra ids ' + ','.join(extra))
        except (ValueError, UnicodeDecodeError) as e:
            file_fail.append('R1 ' + str(e))
            rows = {}
    skill = (show(lane, rev, 'SKILL.md') or b'').decode('utf-8', 'replace')
    reg_rev = (show(lane, rev, 'corpus/SOURCES.md') or b'').decode('utf-8', 'replace')
    reg_base = (show(lane, BASE, 'corpus/SOURCES.md') or b'').decode('utf-8', 'replace')
    count = 0
    for qid, q in QUESTIONS.items():
        fail = list(file_fail)
        for tok in q['tokens']:
            if hits[tok]:
                fail.append(f'R8 token {tok!r} has {hits[tok]} hits at base')
        rs = rows.get(qid, [])
        if len(rs) != 1:
            fail.append(f'R1 {len(rs)} rows for {qid}')
        else:
            r = rs[0]
            if set(r) != ROW_KEYS:
                fail.append('R2 keys ' + ','.join(sorted(set(r) ^ ROW_KEYS)))
            st, quote, snap, line, src = (r.get('statement'), r.get('quote'), r.get('snapshot'),
                                          r.get('line'), r.get('source'))
            if not all(isinstance(x, str) for x in (st, quote, snap, src)):
                fail.append('R2 non-string field')
                st, quote, snap, src = (x if isinstance(x, str) else '' for x in (st, quote, snap, src))
            data = None
            if not snap.startswith('.ufo/waves/round-31/') or '..' in snap.split('/'):
                fail.append('R3 snapshot outside .ufo/waves/round-31/')
            else:
                data = show(lane, rev, snap)
                if data is None:
                    fail.append('R3 snapshot absent at revision')
                elif hashlib.sha256(data).hexdigest() != q['pin']:
                    fail.append('R3 snapshot sha256 differs from pin')
                    data = None
            nq = len(quote.split())
            if not (6 <= nq <= 25):
                fail.append(f'R4 quote has {nq} words')
            if not isinstance(line, int) or isinstance(line, bool) or line < 1:
                fail.append('R4 line is not a positive int')
            elif data is not None:
                lines = data.decode('utf-8', 'replace').splitlines()
                if line > len(lines) or not quote.strip() or quote.strip() not in lines[line - 1]:
                    fail.append('R4 quote not at cited line')
            if not re.fullmatch(r'S\d{3}', src):
                fail.append('R5 source id malformed')
            else:
                if registry_rows(reg_base, src):
                    fail.append('R5 source row exists at base')
                rr = registry_rows(reg_rev, src)
                if len(rr) != 1:
                    fail.append(f'R5 {len(rr)} registry rows for {src}')
                else:
                    cells = status_cell(rr[0])
                    if 'mined' not in cells:
                        fail.append('R5 status cell is not mined')
                    if (URL + q['file']) not in rr[0] or q['pin'] not in rr[0]:
                        fail.append('R5 registry row lacks frozen URL or sha256')
            sl = skill_lines(skill, qid)
            if len(sl) != 1:
                fail.append(f'R6 {len(sl)} SKILL.md lines for {qid}')
            elif not has_token(sl[0], q['tokens']):
                fail.append('R6 SKILL.md line lacks a novelty token')
            if not has_token(quote, q['tokens']):
                fail.append('R6 quote lacks a novelty token')
            if not has_token(st, q['tokens']):
                fail.append('R6 statement lacks a novelty token')
            if len(st.split()) < 12:
                fail.append('R7 statement under 12 words')
            cands = set(words(st))
            cands |= {p for w in list(cands) for p in re.split(r'[-/.]', w) if p}
            digests = {hashlib.sha256((SALT + ' ' + w).encode()).hexdigest()[:16] for w in cands}
            for n, group in enumerate(KEYHASH[qid], 1):
                if not digests.intersection(group):
                    fail.append(f'R7 sealed answer-key group {n} missing')
            if shares_run(st, quote, 5):
                fail.append('R7 statement shares a 6-word run with the quote')
        ok = not fail
        count += ok
        print(json.dumps({'id': qid, 'new_sourced': ok, 'fail': fail}), flush=True)
    print(json.dumps({'predicate': 'new_sourced', 'new_sourced': count, 'of': len(QUESTIONS),
                      'revision': rev, 'base': BASE, 'counter_sha256': sha}))
    return 0 if count == len(QUESTIONS) else 1


if __name__ == '__main__':
    sys.exit(main())
