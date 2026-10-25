#!/usr/bin/env python3
"""Round-38 C2 counter (depth): does the knowledge entry at <REV> carry this host's effective
ALPM hook order, row for row, on a source row opened this round?

Frozen before any seat scored (round-38 declaration, SCORECARD.md "Round 38 — declaration").
Predicate, the same sentence in the plan, this code and the receipt label:

    rows_expected == rows_matched and mismatches == 0 and extra_rows == 0 and source_ok == 1  -> PASS, exit 0

Expected rows are computed from the frozen host capture
`.ufo/waves/round-38/frozen/hooks-capture/` (70 hook files copied read-only 2026-10-26T04:11:58Z),
verified first against MANIFEST.sha256 whose own sha256 is pinned below; any mismatch is
`capture_tampered` (exit 2). The model is libalpm at pacman 54d9411 (`lib/libalpm/hook.c`):

  * hook directories in libalpm order [system /usr/share/libalpm/hooks/, HookDir /etc/pacman.d/hooks/];
    `_alpm_hook_run` walks them last to first, so the first file seen for a name wins (`find_hook`);
  * only names ending in `.hook` count; directories are skipped;
  * a hook with no [Trigger] section is a mask: valid, never run (row when=`masked`, pos `-`);
  * order = `_alpm_hook_cmp`: byte strncmp of the names without the `.hook` suffix over the shorter
    length, the shorter name first on a tie;
  * position is 1-based within one When phase (PreTransaction, PostTransaction);
  * abort = `yes` when the AbortOnFail key is present (it only takes effect for PreTransaction),
    needs = `yes` when NeedsTargets is present, exec = the first whitespace token of Exec.

Entry rows are read at <REV> from `corpus/knowledge/pacman-hook-order-r38.md`, section heading
`## Effective hook order (r38 capture)`, table rows `| when | pos | name | dir | abort | needs | exec |`
(dir `usr` or `etc`; backticks stripped; header and separator rows ignored).
source_ok: the entry's first `source:` line names S-ids; every one is a `corpus/SOURCES.md` row at
<REV> with status `mined` whose used-by cell names the entry path, and at least one row was opened
2026-10-26.

Exit: 0 PASS; 1 FAIL; 2 could-not-evaluate (binding, git, capture tampered). Read-only.
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

COUNTER_ID = 'check-hook-order-r38'
CAPTURE = Path('.ufo/waves/round-38/frozen/hooks-capture')
MANIFEST_SHA256 = 'da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd'
DIRS = (('usr', 'usr-share-libalpm-hooks'), ('etc', 'etc-pacman.d-hooks'))  # libalpm list order
ENTRY = 'corpus/knowledge/pacman-hook-order-r38.md'
SECTION = '## Effective hook order (r38 capture)'
SOURCES = 'corpus/SOURCES.md'
ROUND_DATE = '2026-10-26'
SUFFIX = '.hook'
SID = re.compile(r'\bS\d{3,}\b')


def hook_cmp_key(name: str):
    return name[:-len(SUFFIX)].encode()


def alpm_cmp(a: str, b: str) -> int:
    x, y = hook_cmp_key(a), hook_cmp_key(b)
    n = min(len(x), len(y))
    if x[:n] != y[:n]:
        return -1 if x[:n] < y[:n] else 1
    if len(x) != len(y):
        return -1 if len(x) < len(y) else 1
    return 0


def parse_hook(text: str):
    section, when, abort, needs, exec0, triggers = None, None, False, False, None, 0
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('[') and line.endswith(']'):
            section = line[1:-1]
            if section == 'Trigger':
                triggers += 1
            continue
        key, _, value = line.partition('=')
        key, value = key.strip(), value.strip()
        if section != 'Action':
            continue
        if key == 'When':
            when = value
        elif key == 'AbortOnFail':
            abort = True
        elif key == 'NeedsTargets':
            needs = True
        elif key == 'Exec':
            exec0 = value.split()[0] if value.split() else ''
    return when, abort, needs, exec0, triggers


def expected_rows(repo: Path):
    cap = repo / CAPTURE
    man = cap / 'MANIFEST.sha256'
    if not man.is_file() or hashlib.sha256(man.read_bytes()).hexdigest() != MANIFEST_SHA256:
        raise RuntimeError('capture_tampered: MANIFEST.sha256 missing or digest differs')
    pinned = {}
    for line in man.read_text().splitlines():
        digest, _, rel = line.partition('  ')
        pinned[rel] = digest
    seen = {}
    for tag, sub in reversed(DIRS):
        d = cap / sub
        for p in sorted(d.iterdir()) if d.is_dir() else []:
            rel = f'{sub}/{p.name}'
            if not p.name.endswith(SUFFIX) or p.is_dir():
                continue
            if rel not in pinned or hashlib.sha256(p.read_bytes()).hexdigest() != pinned[rel]:
                raise RuntimeError(f'capture_tampered: {rel}')
            if p.name in seen:
                continue
            seen[p.name] = (tag, parse_hook(p.read_text(errors='replace')))
    if len(pinned) != sum(1 for tag, sub in DIRS for p in (cap / sub).iterdir() if p.name.endswith(SUFFIX)):
        raise RuntimeError('capture_tampered: file set differs from manifest')
    import functools
    names = sorted(seen, key=functools.cmp_to_key(alpm_cmp))
    rows, pos = [], {'PreTransaction': 0, 'PostTransaction': 0}
    for n in names:
        tag, (when, abort, needs, exec0, triggers) = seen[n]
        if triggers == 0:
            rows.append(('masked', '-', n, tag, 'yes' if abort else 'no', 'yes' if needs else 'no', exec0 or '-'))
            continue
        pos[when] += 1
        rows.append((when, str(pos[when]), n, tag, 'yes' if abort else 'no', 'yes' if needs else 'no', exec0))
    return rows


def git_show(repo: Path, sha: str, path: str):
    p = subprocess.run(['git', '-C', str(repo), 'show', f'{sha}:{path}'], env=_revision.clean_env(),
                       capture_output=True, timeout=60)
    return p.stdout.decode(errors='replace') if p.returncode == 0 else None


def entry_rows(text: str):
    rows, inside = [], False
    for line in text.splitlines():
        if line.strip() == SECTION:
            inside = True
            continue
        if inside and line.startswith('## '):
            break
        if inside and line.lstrip().startswith('|'):
            cells = [c.strip().strip('`').strip() for c in line.strip().strip('|').split('|')]
            if len(cells) != 7 or cells[0] == 'when' or set(cells[0]) <= set('-: '):
                continue
            rows.append(tuple(cells))
    return rows


def source_check(entry_text: str, sources_text: str | None):
    first = next((l for l in entry_text.splitlines() if l.startswith('source:')), '')
    ids = sorted(set(SID.findall(first)))
    if not ids or sources_text is None:
        return 0, ids, ['no S-id on the source: line' if not ids else 'SOURCES.md missing']
    reg = {}
    for line in sources_text.splitlines():
        cells = [c.strip() for c in line.strip().split('|')]
        if len(cells) == 13 and re.fullmatch(r'S\d{3,}', cells[1]):
            reg[cells[1]] = cells
    problems, today = [], False
    for i in ids:
        c = reg.get(i)
        if c is None:
            problems.append(f'{i} absent')
            continue
        if c[8] != 'mined':
            problems.append(f'{i} status {c[8]}')
        if ENTRY not in c[11]:
            problems.append(f'{i} used-by lacks entry')
        if c[9] == ROUND_DATE:
            today = True
    if not today:
        problems.append(f'no cited row opened {ROUND_DATE}')
    return (0 if problems else 1), ids, problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--repo', default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument('--revision', required=True)
    ap.add_argument('--branch', default='master')
    a = ap.parse_args(argv)
    repo = Path(a.repo)
    try:
        b = _revision.bind(a.repo, a.revision, a.branch)
        exp = expected_rows(repo)
    except (_revision.RevisionError, RuntimeError, OSError) as e:
        print(json.dumps({'counter': COUNTER_ID, 'error': str(e), 'exit': 2}))
        return 2
    text = git_show(repo, b.sha, ENTRY)
    got = entry_rows(text) if text is not None else []
    gs, es = set(got), set(exp)
    dups = len(got) - len(gs)
    matched = len(es & gs)
    mism = sorted(es - gs)
    extra = sorted(gs - es)
    src_ok, ids, problems = source_check(text or '', git_show(repo, b.sha, SOURCES))
    ok = matched == len(exp) and not mism and not extra and dups == 0 and src_ok == 1
    rec = {'counter': COUNTER_ID, 'revision': b.sha, 'branch_tip': b.branch_tip,
           'predicate': 'rows_expected == rows_matched and mismatches == 0 and extra_rows == 0 and source_ok == 1',
           'entry_present': text is not None, 'rows_expected': len(exp), 'rows_matched': matched,
           'mismatches': len(mism), 'extra_rows': len(extra) + dups, 'source_ok': src_ok,
           'source_ids': ids, 'source_problems': problems,
           'result': 'PASS' if ok else 'FAIL', 'exit': 0 if ok else 1,
           'missing_rows_first5': [list(r) for r in mism[:5]], 'extra_rows_first5': [list(r) for r in extra[:5]]}
    print(json.dumps(rec, indent=1))
    return rec['exit']


if __name__ == '__main__':
    sys.exit(main())
