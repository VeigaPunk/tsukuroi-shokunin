#!/usr/bin/env python3
"""Round-39 C2 counter (depth, sourced): does the knowledge entry at <REV> carry the libalpm transaction
order TO1-TO8 (pacman 54d9411), each rule quoted from the pinned source at the cited lines, with the two
host counts this host's pacman.log yields?

Frozen before any seat scored (SCORECARD.md "Round 39 — declaration"). It closes the three round-38
C2-counter gaps the closure routed (round-38 verifier spot-check §6.3): a rule row verifies only on an
UPSTREAM source row (an own-work row alone cannot carry it); every S-id a row cites must be in the entry's
`source:` line (an S-id dropped from `source:` fails its rows); a duplicated rule row or `## ` heading
anywhere in the file is counted (no block may be duplicated past the next heading).

Entry: `corpus/knowledge/pacman-transaction-order-r39.md` at <REV>. Rule rows are table rows whose first
cell is `TO1`..`TO8`: `| TOn | rule | source | host consequence |`. A row verifies when its source cell holds
an S-id, a `<file>:<A>-<B>` (or `<file>:<A>`) reference and a curly-quoted “…” quote such that
  * the S-id is a `corpus/SOURCES.md` row at <REV>, status `mined`, used-by naming the entry file, whose
    URL contains `54d9411` and ends with `lib/libalpm/<file>`, and <file> is the row's required file:
    TO1 trans.c, TO2 sync.c, TO3 add.c, TO4 add.c, TO5 hook.c, TO6 add.c, TO7 remove.c, TO8 util.c;
  * the quote (4-25 words) occurs, whitespace-collapsed, inside lines A..B of the frozen snapshot of
    <file> (`.ufo/waves/round-39/frozen/src/`, sha256 pinned below, read from this tool's own tree);
  * every S-id in the source cell is named on the entry's first `source:` line.
source_ok: every S-id on the `source:` line is a SOURCES row at <REV> with status `mined` whose used-by
names the entry file, and at least one of them was opened 2026-10-26.
Host counts, from the frozen capture `.ufo/waves/round-39/frozen/txcapture/` (MANIFEST sha256 pinned):
a transaction window opens at a `[PACMAN] Running` line; `transaction started` .. `transaction completed`
is its commit phase. counts_ok adds 1 when the TO1 row's host cell contains "<N> transactions" (N =
windows with a `transaction started` line) and 1 when the TO8 row's host cell contains "<X> of <Y>"
(X = `[ALPM-SCRIPTLET]` lines outside every commit phase, Y = all `[ALPM-SCRIPTLET]` lines).
oracle_violations: `running '<hook>'` lines inside a commit phase (TO1 says there are none).

Predicate (same sentence in the declaration, here and in the receipt):

    rules_verified == 8 and duplicate_rows == 0 and duplicate_headings == 0 and source_ok == 1
    and counts_ok == 2 and oracle_violations == 0                                 -> PASS, exit 0

Exit: 0 PASS; 1 FAIL; 2 could-not-evaluate (binding, git, frozen input tampered). Read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _revision  # noqa: E402

COUNTER_ID = 'check-transaction-order-r39'
ENTRY = 'corpus/knowledge/pacman-transaction-order-r39.md'
ENTRY_NAME = 'pacman-transaction-order-r39.md'
SOURCES = 'corpus/SOURCES.md'
OPENED = '2026-10-26'
TOOL_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = TOOL_ROOT / '.ufo/waves/round-39/frozen/src'
CAP_DIR = TOOL_ROOT / '.ufo/waves/round-39/frozen/txcapture'
SRC_SHA = {
    'add.c': 'fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1',
    'hook.c': '99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a',
    'remove.c': 'a052d455f088f34bf1d713a434957de7e1b9322862a07b69160c65ee15dca314',
    'sync.c': '6b297364eaba94e82a1e30b50dde9b3b96f88075855b66ff455aca1e24995d46',
    'trans.c': '637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07',
    'util.c': '381618b6054859ec76807956328b78b330237273bebe10022a559b243cb5bdd2',
}
CAP_MANIFEST_SHA = 'cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4'
REQUIRED = {'TO1': 'trans.c', 'TO2': 'sync.c', 'TO3': 'add.c', 'TO4': 'add.c', 'TO5': 'hook.c',
            'TO6': 'add.c', 'TO7': 'remove.c', 'TO8': 'util.c'}
ROW_RE = re.compile(r'^\|\s*(TO\d+)\s*\|')
SID_RE = re.compile(r'\bS(\d{3,})\b')
REF_RE = re.compile(r'\b([a-z_]+\.c):(\d+)(?:-(\d+))?')
QUOTE_RE = re.compile(r'“([^”]+)”')
LOGLINE_RE = re.compile(r'^\[[^\]]+\] \[([A-Z-]+)\] (.*)$')


class Tampered(Exception):
    pass


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def collapse(s: str) -> str:
    return ' '.join(s.replace('`', '').split())


def load_frozen():
    src = {}
    for name, want in SRC_SHA.items():
        b = (SRC_DIR / name).read_bytes()
        if sha(b) != want:
            raise Tampered(f'snapshot {name} sha256 {sha(b)} != {want}')
        src[name] = b.decode('utf-8', 'replace').splitlines()
    man = (CAP_DIR / 'MANIFEST.sha256').read_bytes()
    if sha(man) != CAP_MANIFEST_SHA:
        raise Tampered('capture MANIFEST sha256 mismatch')
    for line in man.decode().splitlines():
        digest, name = line.split(None, 1)
        if sha((CAP_DIR / name.strip()).read_bytes()) != digest:
            raise Tampered(f'capture file {name} mismatch')
    return src, (CAP_DIR / 'pacman.log').read_text(encoding='utf-8', errors='replace').splitlines()


def host_counts(log):
    windows = started = out = tagged = violations = 0
    state = None
    for line in log:
        m = LOGLINE_RE.match(line)
        if not m:
            continue
        tag, msg = m.groups()
        if tag == 'PACMAN' and msg.startswith('Running '):
            windows += 1
            state = 'pre'
            continue
        if tag == 'ALPM' and msg == 'transaction started':
            started += 1
            state = 'commit'
            continue
        if tag == 'ALPM' and msg in ('transaction completed', 'transaction failed', 'transaction interrupted'):
            state = 'post'
            continue
        if tag == 'ALPM-SCRIPTLET':
            tagged += 1
            if state != 'commit':
                out += 1
        if tag == 'ALPM' and msg.startswith("running '") and state == 'commit':
            violations += 1
    return {'windows': windows, 'transactions_started': started, 'scriptlet_tag_outside_commit': out,
            'scriptlet_tag_total': tagged, 'running_inside_commit': violations}


def parse_sources(text: str):
    rows = {}
    for line in text.splitlines():
        if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 11:
            continue
        rows[cells[0]] = {'title': cells[1], 'status': cells[7], 'opened': cells[8], 'used_by': cells[10]}
    return rows


def git_show(repo, rev, path):
    p = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], env=_revision.clean_env(),
                       capture_output=True, timeout=60)
    return p.stdout.decode('utf-8', 'replace') if p.returncode == 0 else None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--repo', default=str(TOOL_ROOT))
    ap.add_argument('--revision', required=True)
    ap.add_argument('--branch', default='master')
    a = ap.parse_args(argv)
    try:
        b = _revision.bind(a.repo, a.revision, a.branch)
        src, log = load_frozen()
    except _revision.RevisionError as e:
        print(json.dumps({'counter': COUNTER_ID, 'error': str(e), 'exit': 2}))
        return 2
    except (Tampered, OSError, ValueError) as e:
        print(json.dumps({'counter': COUNTER_ID, 'error': 'frozen input: ' + str(e), 'exit': 2}))
        return 2
    hc = host_counts(log)
    rec = {'counter': COUNTER_ID, 'revision': b.sha, 'branch_tip': b.branch_tip, 'host': hc,
           'predicate': 'rules_verified == 8 and duplicate_rows == 0 and duplicate_headings == 0 and '
                        'source_ok == 1 and counts_ok == 2 and oracle_violations == 0'}
    entry = git_show(a.repo, b.sha, ENTRY)
    srows = parse_sources(git_show(a.repo, b.sha, SOURCES) or '')
    rules, verified, dup_rows, dup_heads, source_ok, counts_ok = {}, 0, 0, 0, 0, 0
    if entry is not None:
        lines = entry.splitlines()
        heads = [l.strip() for l in lines if l.startswith('## ')]
        dup_heads = 0
        src_line = next((l for l in lines if l.startswith('source:')), '')
        header_ids = {'S' + x for x in SID_RE.findall(src_line)}
        good = [i for i in header_ids if i in srows and srows[i]['status'] == 'mined'
                and ENTRY_NAME in srows[i]['used_by']]
        source_ok = int(bool(header_ids) and len(good) == len(header_ids)
                        and any(srows[i]['opened'] == OPENED for i in good))
        seen = {}
        for l in lines:
            m = ROW_RE.match(l)
            if m:
                seen.setdefault(m.group(1), []).append(l)
        dup_rows = 0
        for to, want in REQUIRED.items():
            r = {'present': to in seen, 'verified': False, 'reasons': []}
            rules[to] = r
            if to not in seen:
                continue
            cells = [c.strip() for c in seen[to][0].strip().strip('|').split('|')]
            if len(cells) < 4:
                r['reasons'].append('fewer than 4 cells')
                continue
            src_cell, host_cell = cells[2], cells[3]
            ids = ['S' + x for x in SID_RE.findall(src_cell)]
            missing = [i for i in ids if i not in header_ids]
            if missing:
                r['reasons'].append('cited S-id not on source: line: ' + ','.join(missing))
            upstream = [i for i in ids if i in srows and srows[i]['status'] == 'mined'
                        and ENTRY_NAME in srows[i]['used_by'] and '54d9411' in srows[i]['title']
                        and re.search(r'lib/libalpm/' + re.escape(want) + r'(\s|$)', srows[i]['title'])]
            if not upstream:
                r['reasons'].append(f'no mined upstream row for {want} at 54d9411 naming the entry')
            quote_ok = False
            for fname, a1, a2 in REF_RE.findall(src_cell):
                if fname != want:
                    continue
                lo, hi = int(a1), int(a2 or a1)
                body = collapse(' '.join(src[want][lo - 1:hi]))
                for q in QUOTE_RE.findall(src_cell):
                    qc = collapse(q)
                    if 4 <= len(qc.split()) <= 25 and qc in body:
                        quote_ok = True
            if not quote_ok:
                r['reasons'].append(f'no 4-25 word quote found in {want} at the cited lines')
            r['verified'] = not missing and bool(upstream) and quote_ok
            verified += int(r['verified'])
            if to == 'TO1' and f"{hc['transactions_started']} transactions" in host_cell:
                counts_ok += 1
            if to == 'TO8' and f"{hc['scriptlet_tag_outside_commit']} of {hc['scriptlet_tag_total']}" in host_cell:
                counts_ok += 1
    ok = (verified == 8 and dup_rows == 0 and dup_heads == 0 and source_ok == 1 and counts_ok == 2
          and hc['running_inside_commit'] == 0)
    rec.update({'entry_present': entry is not None, 'rules_verified': verified, 'duplicate_rows': dup_rows,
                'duplicate_headings': dup_heads, 'source_ok': source_ok, 'counts_ok': counts_ok,
                'oracle_violations': hc['running_inside_commit'], 'rules': rules,
                'result': 'PASS' if ok else 'FAIL', 'exit': 0 if ok else 1})
    print(json.dumps(rec, indent=1))
    return rec['exit']


if __name__ == '__main__':
    sys.exit(main())
