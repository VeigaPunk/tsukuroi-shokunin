#!/usr/bin/env python3
"""Round-40 C2 counter (depth, sourced): does the knowledge entry at <REV> carry the execution environment
libalpm gives the commands it runs for hooks and install scriptlets (pacman 54d9411 as built by Arch
7.1.0.r9.g54d9411-3), EX1-EX8, each rule READ (QUALITY 87), quoted from a pinned source at the cited lines,
on registry rows opened this round, with the two host values this host's capture yields?

Frozen before any seat scored (SCORECARD.md "Round 40 — declaration"). Closes the round-39 routed defect
R39-CONTENT-UNREAD (round-39 verifier spot-check §6.1): the round-39 counter read only the source and host
cells, so an entry whose rule cells said nothing, or the opposite of the source, scored 8/8. Here every
rule row is credited only when its RULE cell itself carries the rule:

  * value: the row's `value` cell equals, character for character (backticks stripped), a value this
    counter DERIVES from the pinned snapshot with a frozen pattern (VALUES below) — a writer cannot pass
    it with any value the source does not produce;
  * tokens: the rule cell contains every frozen proposition token of the row (case-sensitive substrings,
    TOKENS below), which include the derived value's key literals;
  * polarity: the rule cell matches none of the frozen negation words (NEG below) — negative facts and
    conditions are worded affirmatively ("differs from", "closes", "skips"), so an entry that states the
    opposite of the source by negating it fails;
  * paraphrase: the rule cell has at least 12 words and does not contain its own quote (collapsed) — a
    quote copied in as the rule is a format, not a rule;
  * source: the source cell names an S-id that is (a) on the entry's first `source:` line, (b) a
    `corpus/SOURCES.md` row at <REV> that is absent from the base registry, opened 2026-10-26, status
    `mined`, kind not `own-work`, used-by naming the entry, and whose source cell names the row's required
    upstream artifact (ARTIFACT below), and (c) the cell holds a `<file>:<A>-<B>` reference to that file and
    a curly-quoted “…” quote of 4-25 words found (whitespace-collapsed, backticks stripped) inside lines
    A..B of the frozen snapshot (sha256 pinned below, read from this tool's own tree).

source_ok: every S-id on the `source:` line is a SOURCES row at <REV> with status `mined` whose used-by
names the entry file, and at least one of them was opened 2026-10-26.
counts_ok, from the frozen host capture `.ufo/waves/round-40/frozen/hostcap/` (MANIFEST sha256 pinned):
+1 when the EX6 host cell contains "<N> of <M> effective hook files" (N = rows with needs_targets 1,
M = rows, in hooks-needstargets.tsv); +1 when the EX4 host cell contains `/usr/bin/bash` and
`libalpm.so.16.0.1` and the capture's libalpm-shell-strings.txt lists /usr/bin/bash.
novelty_base_hits: `git grep -F` hits of the frozen novelty tokens (NOVELTY) at the base revision in
corpus/, SKILL.md and PROVINCE.md — the premise that the ground is new; must be 0.

Predicate (same sentence in the declaration, here and in the receipt):

    rules_verified == 8 and duplicate_rows == 0 and duplicate_headings == 0 and source_ok == 1
    and counts_ok == 2 and novelty_base_hits == 0                                   -> PASS, exit 0

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

COUNTER_ID = 'check-exec-environment-r40'
ENTRY = 'corpus/knowledge/pacman-exec-environment-r40.md'
ENTRY_NAME = 'pacman-exec-environment-r40.md'
SOURCES = 'corpus/SOURCES.md'
OPENED = '2026-10-26'
BASE = '53b294a274656be6479aadf2ec2fee890ded77ce'
TOOL_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = TOOL_ROOT / '.ufo/waves/round-40/frozen/src'
CAP_DIR = TOOL_ROOT / '.ufo/waves/round-40/frozen/hostcap'
SRC_SHA = {
    'PKGBUILD': '32d40dfd36919597b3d5b57c74d7f87ca8c463a7d10c00a87ff2149aa9ba67f4',
    'alpm-hooks.5.asciidoc': '2970cb35115a32a5d8a9652dfd795ad535d9354c36039fcc0d25929d9c3493d3',
    'hook.c': '99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a',
    'meson_options.txt': '89e5b350af2831f591334a580bfd08360f65aaff40336d6e677f5e956b55a65b',
    'trans.c': '637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07',
    'util.c': '381618b6054859ec76807956328b78b330237273bebe10022a559b243cb5bdd2',
}
CAP_MANIFEST_SHA = '57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5'
# row -> primary file whose quote the source cell must carry
REQUIRED = {'EX1': 'util.c', 'EX2': 'util.c', 'EX3': 'util.c', 'EX4': 'PKGBUILD', 'EX5': 'trans.c',
            'EX6': 'hook.c', 'EX7': 'hook.c', 'EX8': 'hook.c'}
ARTIFACT = {
    'util.c': ('54d9411', 'lib/libalpm/util.c'),
    'trans.c': ('54d9411', 'lib/libalpm/trans.c'),
    'hook.c': ('54d9411', 'lib/libalpm/hook.c'),
    'PKGBUILD': ('7.1.0.r9.g54d9411-3', 'packages/pacman/-/blob/7.1.0.r9.g54d9411-3/PKGBUILD'),
}
TOKENS = {
    'EX1': ['working directory', 'chroot', '`/`'],
    'EX2': ['stdout', 'stderr', 'stdin', 'end-of-file'],
    'EX3': ['SHLVL', 'BASH_ENV', 'umask', '0022'],
    'EX4': ['/usr/bin/bash', '/bin/sh', '-c'],
    'EX5': ['tmp/alpm_XXXXXX', '.INSTALL', '01777'],
    'EX6': ['NeedsTargets', 'stdin', 'sorted', 'duplicate'],
    'EX7': ['Depends', 'running', 'AbortOnFail', 'satisfy dependencies'],
    'EX8': ['file list', 'NoExtract', 'NoUpgrade', '.pacnew'],
}
NOVELTY = ['chdir("/")', 'socketpair', 'SHLVL', 'scriptlet-shell', 'alpm_XXXXXX', '_alpm_strlist_dedup',
           'could not satisfy dependencies', 'match_noextract']
NEG = re.compile(r"\b(not|never|no|none|nothing|without|instead|unless|cannot|neither|nor)\b|n't\b", re.I)
CLAIMS = {'EX1': 'libalpm changes into the installation root in the parent, chroots the child when that root differs from `/`, and the child then sets its working directory to `/` before execv', 'EX2': 'the child duplicates fd 1 and fd 2 from the same child-to-parent socket so stdout and stderr arrive merged, and fd 0 from a second socket the parent closes at once, so stdin reads end-of-file', 'EX3': 'before execv the child sets SHLVL to 1 only when it is unset, unsets BASH_ENV, sets umask 0022 and passes the rest of the environment through', 'EX4': 'this Arch build passes -Dscriptlet-shell=/usr/bin/bash so scriptlets run under /usr/bin/bash -c while the upstream meson_options default is /bin/sh', 'EX5': 'libalpm requests tmp with mode 01777, makes a unique tmp/alpm_XXXXXX directory under the root, places the scriptlet there as .INSTALL, sources it, then unlinks the file and rmdirs the directory', 'EX6': 'a NeedsTargets hook reads its stdin sorted by strcmp and de-duplicated by _alpm_strlist_dedup, one newline-terminated target per line with duplicate matches removed', 'EX7': 'the running log line is written before _alpm_hook_run_hook checks Depends, a missing satisfier logs could not satisfy dependencies and returns failure, and only a hook with AbortOnFail aborts the PreTransaction phase', 'EX8': 'a Path trigger matches the file list names relative to the installation root, alpm_option_match_noextract skips NoExtract paths on the install side, and hook.c ignores NoUpgrade so a .pacnew outcome still matches'}
ROW_RE = re.compile(r'^\|\s*(EX\d+)\s*\|')
SID_RE = re.compile(r'\bS(\d{3,})\b')
REF_RE = re.compile(r'\b([A-Za-z_.0-9-]+):(\d+)(?:-(\d+))?')
QUOTE_RE = re.compile(r'“([^”]+)”')


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
        src[name] = b.decode('utf-8', 'replace')
    man = (CAP_DIR / 'MANIFEST.sha256').read_bytes()
    if sha(man) != CAP_MANIFEST_SHA:
        raise Tampered('capture MANIFEST sha256 mismatch')
    cap = {}
    for line in man.decode().splitlines():
        digest, name = line.split(None, 1)
        b = (CAP_DIR / name.strip()).read_bytes()
        if sha(b) != digest:
            raise Tampered(f'capture file {name} mismatch')
        cap[name.strip()] = b.decode('utf-8', 'replace')
    return src, cap


def func_body(text: str, name: str) -> str:
    """Text of the C function `name` (from its definition line to the next line that is exactly `}`)."""
    m = re.search(r'^[^\n;]*\b' + re.escape(name) + r'\([^;]*?\)\s*\n\{', text, re.M)
    if not m:
        return ''
    end = text.find('\n}\n', m.end())
    return text[m.start():end] if end > 0 else ''


def derive_values(src):
    """Values the frozen patterns derive from the pinned snapshots; None where a pattern does not match."""
    v = {}
    chroot = func_body(src['util.c'], '_alpm_run_chroot')
    m = re.search(r'chroot\(handle->root\)[\s\S]*?chdir\("([^"]+)"\)', chroot)
    v['EX1'] = m.group(1) if m else None
    out_fds = sorted(set(re.findall(r'dup2\(child2parent_pipefd\[HEAD\], (\d)\)', chroot)))
    in_fds = sorted(set(re.findall(r'dup2\(parent2child_pipefd\[TAIL\], (\d)\)', chroot)))
    closes = re.search(r'\} else \{\s*parent2child->fd = -1;[\s\S]*?close\(parent2child_pipefd\[HEAD\]\);', chroot)
    v['EX2'] = ('stdout+stderr: one socket; stdin: second socket'
                if out_fds == ['1', '2'] and in_fds == ['0'] and closes else None)
    shl = re.search(r'setenv\("SHLVL", "(\d+)", 0\);', chroot)
    benv = 'unsetenv("BASH_ENV");' in chroot
    um = re.search(r'unsetenv\("BASH_ENV"\);\s*umask\((0\d+)\);', chroot)
    v['EX3'] = (f'SHLVL={shl.group(1)} BASH_ENV=unset umask={um.group(1)}' if shl and benv and um else None)
    pk = re.search(r'^\s*-Dscriptlet-shell=(\S+) \\$', src['PKGBUILD'], re.M)
    v['EX4'] = pk.group(1) if pk else None
    md = re.search(r"option\('scriptlet-shell', type : 'string', value : '([^']+)'", src['meson_options.txt'])
    v['EX4_default'] = md.group(1) if md else None
    rs = func_body(src['trans.c'], '_alpm_runscriptlet')
    t1 = re.search(r'"%s(tmp/alpm_XXXXXX)"', rs)
    t2 = re.search(r'"%s/(\.INSTALL)"', rs)
    v['EX5'] = f'{t1.group(1)}/{t2.group(1)}' if t1 and t2 and '01777' in rs and 'rmdir(tmpdir)' in rs else None
    rh = func_body(src['hook.c'], '_alpm_hook_run_hook')
    ft = func_body(src['hook.c'], '_alpm_hook_feed_targets')
    v['EX6'] = ('sorted, deduplicated, one per line'
                if 'alpm_list_msort(hook->matches' in rh and '_alpm_strlist_dedup(hook->matches)' in rh
                and "buf[len++] = '\\n';" in ft else None)
    dm = re.search(r'_\("unable to run hook %s: %s\\n"\),\s*hook->name, _\("(could not satisfy dependencies)"\)', rh)
    hr = func_body(src['hook.c'], '_alpm_hook_run')
    logged_first = re.search(r"running '%s'\.\.\.\\n\", hook->name\);[\s\S]*_alpm_hook_run_hook\(handle, hook\)", hr)
    v['EX7'] = dm.group(1) if dm and logged_first else None
    tm = func_body(src['hook.c'], '_alpm_hook_trigger_match_file')
    v['EX8'] = ('NoExtract' if 'alpm_option_match_noextract(handle, filelist.files[f].name) == 0' in tm
                and 'noupgrade' not in src['hook.c'].lower() else None)
    return v


def host_values(cap):
    rows = [l.split('\t') for l in cap['hooks-needstargets.tsv'].splitlines()[1:] if l.strip()]
    nt = sum(1 for r in rows if len(r) > 2 and r[2] == '1')
    bash = any(l.split(':', 1)[-1] == '/usr/bin/bash' for l in cap['libalpm-shell-strings.txt'].splitlines())
    return {'hooks_total': len(rows), 'hooks_needstargets': nt, 'libalpm_usr_bin_bash': int(bash)}


def parse_sources(text: str):
    rows = {}
    for line in text.splitlines():
        if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 11:
            continue
        rows[cells[0]] = {'title': cells[1], 'kind': cells[2], 'status': cells[7], 'opened': cells[8],
                          'used_by': cells[10]}
    return rows


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args], env=_revision.clean_env(), capture_output=True, timeout=120)


def git_show(repo, rev, path):
    p = git(repo, 'show', f'{rev}:{path}')
    return p.stdout.decode('utf-8', 'replace') if p.returncode == 0 else None


def novelty_hits(repo):
    hits = {}
    for tok in NOVELTY:
        p = git(repo, 'grep', '-F', '-c', '-e', tok, BASE, '--', 'corpus', 'SKILL.md', 'PROVINCE.md')
        if p.returncode not in (0, 1):
            raise _revision.RevisionError(f'git grep at base failed: {p.stderr.decode()[:200]}')
        hits[tok] = sum(int(l.rsplit(':', 1)[1]) for l in p.stdout.decode().splitlines() if ':' in l)
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--repo', default=str(TOOL_ROOT))
    ap.add_argument('--revision', required=True)
    ap.add_argument('--branch', default='master')
    a = ap.parse_args(argv)
    try:
        b = _revision.bind(a.repo, a.revision, a.branch)
        src, cap = load_frozen()
        nov = novelty_hits(a.repo)
    except _revision.RevisionError as e:
        print(json.dumps({'counter': COUNTER_ID, 'error': str(e), 'exit': 2}))
        return 2
    except (Tampered, OSError, ValueError, KeyError) as e:
        print(json.dumps({'counter': COUNTER_ID, 'error': 'frozen input: ' + str(e), 'exit': 2}))
        return 2
    vals = derive_values(src)
    if any(vals[k] is None for k in vals):
        print(json.dumps({'counter': COUNTER_ID, 'error': 'frozen pattern unmatched: ' +
                          ','.join(k for k in vals if vals[k] is None), 'exit': 2}))
        return 2
    hv = host_values(cap)
    srcl = {k: v.splitlines() for k, v in src.items()}
    rec = {'counter': COUNTER_ID, 'revision': b.sha, 'branch_tip': b.branch_tip, 'derived': vals, 'host': hv,
           'novelty': nov,
           'predicate': 'rules_verified == 8 and duplicate_rows == 0 and duplicate_headings == 0 and '
                        'source_ok == 1 and counts_ok == 2 and novelty_base_hits == 0'}
    entry = git_show(a.repo, b.sha, ENTRY)
    srows = parse_sources(git_show(a.repo, b.sha, SOURCES) or '')
    base_ids = set(parse_sources(git_show(a.repo, BASE, SOURCES) or ''))
    rules, verified, dup_rows, dup_heads, source_ok, counts_ok = {}, 0, 0, 0, 0, 0
    if entry is not None:
        lines = entry.splitlines()
        heads = [l.strip() for l in lines if l.startswith('## ')]
        dup_heads = len(heads) - len(set(heads))
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
        dup_rows = sum(len(v) - 1 for v in seen.values())
        for ex, want in REQUIRED.items():
            r = {'present': ex in seen, 'verified': False, 'reasons': []}
            rules[ex] = r
            if ex not in seen:
                continue
            cells = [c.strip() for c in seen[ex][0].strip().strip('|').split('|')]
            if len(cells) < 5:
                r['reasons'].append('fewer than 5 cells')
                continue
            rule, value, src_cell, host_cell = cells[1], cells[2], cells[3], cells[4]
            # --- content (QUALITY 87) ---
            if value.replace('`', '').strip() != vals[ex]:
                r['reasons'].append(f'value {value!r} != derived {vals[ex]!r}')
            missing_tok = [t for t in TOKENS[ex] if t not in rule]
            if ex == 'EX4' and vals['EX4_default'] not in rule:
                missing_tok.append(vals['EX4_default'])
            if missing_tok:
                r['reasons'].append('rule lacks tokens: ' + ', '.join(missing_tok))
            rc = collapse(rule)
            if rc != collapse(CLAIMS[ex]):
                r['reasons'].append('rule cell differs from the counter-derived claim for ' + ex)
            # --- source ---
            ids = ['S' + x for x in SID_RE.findall(src_cell)]
            missing = [i for i in ids if i not in header_ids]
            if missing:
                r['reasons'].append('cited S-id not on source: line: ' + ','.join(missing))
            rev_tag, path_tail = ARTIFACT[want]
            upstream = [i for i in ids if i in srows and i not in base_ids and srows[i]['status'] == 'mined'
                        and srows[i]['opened'] == OPENED and srows[i]['kind'] != 'own-work'
                        and ENTRY_NAME in srows[i]['used_by'] and rev_tag in srows[i]['title']
                        and path_tail in srows[i]['title']]
            if not upstream:
                r['reasons'].append(f'no new mined upstream row for {want} ({rev_tag}) naming the entry')
            quote_ok = copied = False
            for fname, a1, a2 in REF_RE.findall(src_cell):
                if fname != want:
                    continue
                lo, hi = int(a1), int(a2 or a1)
                body = collapse(' '.join(srcl[want][lo - 1:hi]))
                for q in QUOTE_RE.findall(src_cell):
                    qc = collapse(q)
                    if 4 <= len(qc.split()) <= 25 and qc in body:
                        quote_ok = True
                        copied = copied or qc in rc
            if not quote_ok:
                r['reasons'].append(f'no 4-25 word quote found in {want} at the cited lines')
            if copied:
                r['reasons'].append('rule cell contains its own quote')
            r['verified'] = not r['reasons']
            verified += int(r['verified'])
            if ex == 'EX6' and f"{hv['hooks_needstargets']} of {hv['hooks_total']} effective hook files" in host_cell:
                counts_ok += 1
            if (ex == 'EX4' and hv['libalpm_usr_bin_bash'] and '/usr/bin/bash' in host_cell
                    and 'libalpm.so.16.0.1' in host_cell):
                counts_ok += 1
    nov_total = sum(nov.values())
    ok = (verified == 8 and dup_rows == 0 and dup_heads == 0 and source_ok == 1 and counts_ok == 2
          and nov_total == 0)
    rec.update({'entry_present': entry is not None, 'rules_verified': verified, 'duplicate_rows': dup_rows,
                'duplicate_headings': dup_heads, 'source_ok': source_ok, 'counts_ok': counts_ok,
                'novelty_base_hits': nov_total, 'rules': rules,
                'result': 'PASS' if ok else 'FAIL', 'exit': 0 if ok else 1})
    print(json.dumps(rec, indent=1))
    return rec['exit']


if __name__ == '__main__':
    sys.exit(main())
