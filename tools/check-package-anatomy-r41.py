#!/usr/bin/env python3
"""Round-41 C2 counter (depth, sourced): does the knowledge entry at <REV> state the ALPM package anatomy
(pacman 54d9411 as built by Arch 7.1.0.r9.g54d9411-3; alpm-package(7) from alpm-docs 0.13.0-1), PA1-PA8,
each rule carrying its frozen proposition, quoted inside the row's frozen source window, on registry rows
opened this round, with the host values this host's capture yields, and each row holding a committed
non-author reviewer verdict?

Frozen before any seat scored (SCORECARD.md "Round 41 — declaration"). Closes the round-40 closure's routed
defect R40-ANSWER-KEY for C2 (corpus/lessons/round-40-verifier-spotcheck.md §6.1; QUALITY 81, 87, 88): the
round-40 counter credited a token-list writer (frozen tokens + filler words, the first 4-25 word line of
each file as the quote) and non-negated false rules 8/8 (.ufo/waves/round-40/w1/C2CritControl.md,
C2CritXFalse.md). This counter is still lexical where it reads text, and says so: what it adds is
  * a frozen source WINDOW per row: the cited `<file>:<A>-<B>` range must lie inside it and the quote must
    be found inside the cited lines, so a header or copyright line elsewhere in the file does not count;
  * frozen RELATIONS per row: ordered regular expressions over the rule cell that state the proposition's
    pairing (which member maps to which database file, which function to which directory, which step comes
    first), so a token list in another order, or a rule that swaps a pairing, fails;
  * VERDICTS (QUALITY 81): a row is credited only when at least one committed reviewer verdict file for it
    at <REV> reads `VERDICT: holds` on its first line, names the row id, and none reads `VERDICT: fails`.
    Files: `.ufo/waves/round-41/w1/C2RevPA<n>*.md` and `.ufo/waves/round-41/residual/C2RevPA<n>*.md`.
    A writer that concatenates the RELATIONS literals and the derived values still passes every lexical
    check (the recorded bypass); the verdict files are the read, the lexical checks are shape gates.
Kept from round 40: value cell equals the value this counter derives from the pinned snapshot; no
negation word in the rule cell; at least 12 words; rule cell does not contain its own quote; the source
cell's S-id is on the entry's `source:` line and is a new `mined` upstream row opened 2026-10-26 whose
source cell names the pinned artifact; source_ok; novelty tokens 0 hits at base.

host_ok, from the frozen capture `.ufo/waves/round-41/frozen/hostcap/` (MANIFEST sha256 pinned): one point
each for PA1, PA4, PA5, PA6, PA7, PA8 when the row's host cell carries the values the capture yields
(HOST_EXPECT below, computed from the capture files, never from the entry).

Predicate (same sentence in the declaration, here and in the receipt):

    rules_verified == 8 and verdicts_ok == 8 and host_ok == 6 and source_ok == 1 and duplicate_rows == 0
    and duplicate_headings == 0 and novelty_base_hits == 0                          -> PASS, exit 0

Usage: check-package-anatomy-r41.py --revision <REV> [--repo <lane>] [--branch master]
Exit: 0 PASS; 1 FAIL; 2 could-not-evaluate (binding, git, frozen input tampered, pattern unmatched).
Read-only.
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

COUNTER_ID = 'check-package-anatomy-r41'
ENTRY = 'corpus/knowledge/alpm-package-anatomy-r41.md'
ENTRY_NAME = 'alpm-package-anatomy-r41.md'
SOURCES = 'corpus/SOURCES.md'
OPENED = '2026-10-26'
BASE = '0e5805a1f149bd2ed9fe0db2e0a832afb034a835'
VERDICT_DIRS = ('.ufo/waves/round-41/w1', '.ufo/waves/round-41/residual')
TOOL_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = TOOL_ROOT / '.ufo/waves/round-41/frozen/src'
CAP_DIR = TOOL_ROOT / '.ufo/waves/round-41/frozen/hostcap'
SRC_SHA = {
    'PKGBUILD.5.asciidoc': '15e8007bb11829b4d0474e647b0d08c2bffdf5191ceac949336de3d14a621154',
    'add.c': 'fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1',
    'alpm-package.7.raw': 'b551bb392f6899c89c4c0d5778c89ad482f0c1251260ccf336bd5b5ed2693c45',
    'be_local.c': '52fc17e6a34209ca93c65413f8f8b1cda863c943154626ccb60fbc6d705bb1bc',
    'be_package.c': '24e5890647f80dd953586d8add314b396d0276a37e2f1468f685e90b809db4d7',
    'check.c': '3f86aa0417963c34f524e6261b6e8150562cf678a8cedaa709ed210236c4d217',
    'makepkg.sh.in': 'd588222586b2432b4169c82e6ebcd464acfdc20a663172fd444b8f98e1104e86',
    'query.c': '1e13d329ac2f57653054192a8eba259849aafe45a4cbfa5f4f833e7f3880ad6a',
    'version.c': 'fa769e3081d25d74132109ca35a1e272a44b1c5674c397f3f2a1acaf3b6ab833',
}
CAP_MANIFEST_SHA = '632ed0443cfb26ef002ebfd2a3a99971221f9129836b63135e0ca6ea41874f89'
# row -> (required file, window lo, window hi)
REQUIRED = {
    'PA1': ('alpm-package.7.raw', 95, 124),
    'PA2': ('be_package.c', 595, 656),
    'PA3': ('makepkg.sh.in', 558, 570),
    'PA4': ('add.c', 168, 189),
    'PA5': ('makepkg.sh.in', 615, 620),
    'PA6': ('check.c', 295, 321),
    'PA7': ('PKGBUILD.5.asciidoc', 345, 377),
    'PA8': ('version.c', 39, 255),
}
ARTIFACT = {
    'alpm-package.7.raw': ('alpm-docs 0.13.0-1', 'man.archlinux.org/man/alpm-package.7'),
    'be_package.c': ('54d9411', 'lib/libalpm/be_package.c'),
    'makepkg.sh.in': ('54d9411', 'scripts/makepkg.sh.in'),
    'add.c': ('54d9411', 'lib/libalpm/add.c'),
    'check.c': ('54d9411', 'src/pacman/check.c'),
    'PKGBUILD.5.asciidoc': ('54d9411', 'doc/PKGBUILD.5.asciidoc'),
    'version.c': ('54d9411', 'lib/libalpm/version.c'),
}
# ordered proposition relations over the collapsed rule cell (backticks removed)
RELATIONS = {
    'PA1': [r'\.BUILDINFO\b.*\.MTREE\b.*\.PKGINFO\b', r'\bmust\b.*\broot\b', r'\boptional\b.*\.INSTALL\b'],
    'PA2': [r'\bonly \.PKGINFO\b', r'\.PKGINFO\b.*\bmissing package metadata\b',
            r'\.MTREE\b.{0,40}\bfull load\b', r'\.BUILDINFO\b.{0,60}\bpassed over\b'],
    'PA3': [r'\bLC_COLLATE=C\b.*\bdotglob\b', r'\bdot files sort ahead of the data files\b',
            r'\bpartial\b.*\bstops\b.*\.PKGINFO\b'],
    'PA4': [r'\.INSTALL becomes install\b', r'\.CHANGELOG becomes changelog\b', r'\.MTREE becomes mtree\b',
            r'\bmode 0644\b', r'\.PKGINFO and \.BUILDINFO included, is skipped\b'],
    'PA5': [r'\bmtree-format listing\b', r'\bgzip\b', r'\bexcludes \.MTREE itself\b',
            r'\bomits its own entry\b'],
    'PA6': [r'-Qkk\b.*\bcheck_pkg_full\b', r'\bcheck_pkg_full\b.*\bmtree\b',
            r'\babsent\b.*\breturns 0\b', r'-Qk \(level 1\) runs the fast check\b'],
    'PA7': [r'package\(\), prepare\(\), build\(\) and check\(\) each run inside \$srcdir\b',
            r'verify\(\) runs inside \$startdir\b', r'package\(\) also runs under fakeroot\b'],
    'PA8': [r'\bthe epoch first\b.*\bthen the version\b.*\bthe release only when both\b',
            r'\babsent epoch counting as 0\b', r'\bepoch 1\b.*\boutranks\b.*\bepoch 0\b',
            r'\b1\.0 equals 1\.0-5\b'],
}
NOVELTY = ['extract_db_file', 'missing package metadata', 'LC_COLLATE=C', 'exclude .MTREE', 'no mtree file',
           'startdir', 'parseEVR', 'reserve all files', 'check_pkg_full', 'hit_mtree']
NEG = re.compile(r"\b(not|never|no|none|nothing|without|instead|unless|cannot|neither|nor)\b|n't\b", re.I)
ROW_RE = re.compile(r'^\|\s*(PA\d+)\s*\|')
SID_RE = re.compile(r'\bS(\d{3,})\b')
REF_RE = re.compile(r'\b([A-Za-z_.0-9-]+):(\d+)(?:-(\d+))?')
QUOTE_RE = re.compile(r'“([^”]+)”')
VERDICT_RE = re.compile(r'^VERDICT: (holds|partly|fails)\s*$')


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
    """Text of the C function `name` (definition line to the next line that is exactly `}`)."""
    m = re.search(r'^[^\n;]*\b' + re.escape(name) + r'\([^;]*?\)\s*\n\{', text, re.M)
    if not m:
        return ''
    end = text.find('\n}\n', m.end())
    return text[m.start():end] if end > 0 else ''


def derive_values(src):
    """Values the frozen patterns derive from the pinned snapshots; None where a pattern does not match."""
    v = {}
    man = src['alpm-package.7.raw']
    i = man.find('must be present at the root')
    j = man.find('Optionally, an', i)
    req = re.findall(r'\\f\(CR(\.[A-Z]+)\\fR', man[i:j]) if i >= 0 and j > i else []
    opt = re.search(r'named \\f\(CR(\.[A-Z]+)\\fR may be present at the root', man[j:j + 300]) if j > 0 else None
    v['PA1'] = f"{' '.join(req)}; optional {opt.group(1)}" if req and opt else None
    ld = func_body(src['be_package.c'], '_alpm_pkg_load_internal')
    pk = re.search(r'if\(strcmp\(entry_name, "(\.[A-Z]+)"\) == 0\) \{[\s\S]*?config = 1;', ld)
    v['PA2'] = (pk.group(1) if pk and 'missing package metadata' in ld
                and 'full && strcmp(entry_name, ".MTREE") == 0' in ld and ld.count('config = 1;') == 1 else None)
    lf = re.search(r'list_package_files\(\) \{([\s\S]*?)\n\}', src['makepkg.sh.in'])
    early = re.search(r'if\(\(!full \|\| hit_mtree\) && config\) \{\s*break;', ld)
    v['PA3'] = ('LC_COLLATE=C dotglob' if lf and 'export LC_COLLATE=C' in lf.group(1)
                and 'shopt -s dotglob' in lf.group(1) and early else None)
    ed = func_body(src['add.c'], 'extract_db_file')
    pairs = re.findall(r'strcmp\(entryname, "(\.[A-Z]+)"\) == 0\) \{\s*dbfile = "([a-z]+)";', ed)
    v['PA4'] = (' '.join(f'{a}={b}' for a, b in pairs) if len(pairs) == 3 and 'skipping extraction' in ed
                and 'archive_entry_set_perm(entry, 0644);' in ed else None)
    mk = src['makepkg.sh.in']
    v['PA5'] = ('gzip mtree without .MTREE' if '--format=mtree' in mk
                and '--exclude .MTREE | gzip -c -f -n > .MTREE' in mk else None)
    cf = func_body(src['check.c'], 'check_pkg_full')
    nm = re.search(r'mtree = alpm_pkg_mtree_open\(pkg\);\s*if\(mtree == NULL\) \{[\s\S]*?"%s: (no mtree file)\\n"'
                   r'[\s\S]*?return 0;', cf)
    q = re.search(r'if\(config->op_q_check == 1\) \{\s*ret = check_pkg_fast\(pkg\);\s*\} else \{\s*'
                  r'ret = check_pkg_full\(pkg\);', src['query.c'])
    v['PA6'] = nm.group(1) if nm and q else None
    pb = src['PKGBUILD.5.asciidoc']
    dirs = {}
    for m in re.finditer(r'^\*(\w+)\(\) Function\*::\n((?:\t.*\n)+)', pb, re.M):
        d = re.search(r'This function is run inside `\$(\w+)`\.', m.group(2))
        if d:
            dirs.setdefault('$' + d.group(1), []).append(m.group(1))
    v['PA7'] = ('; '.join(f"{k}: {' '.join(vv)}" for k, vv in dirs.items())
                if set(dirs) == {'$srcdir', '$startdir'} else None)
    vc = src['version.c']
    pe = func_body(vc, 'parseEVR')
    vp = func_body(vc, 'alpm_pkg_vercmp')
    order = re.search(r'ret = rpmvercmp\(epoch1, epoch2\);\s*if\(ret == 0\) \{\s*ret = rpmvercmp\(ver1, ver2\);'
                      r'\s*if\(ret == 0 && rel1 && rel2\) \{\s*ret = rpmvercmp\(rel1, rel2\);', vp)
    v['PA8'] = ('epoch, then version, then release when both carry one'
                if order and pe.count('epoch = "0";') == 2 else None)
    return v


def host_expect(cap):
    rows = [l.split('\t') for l in cap['localdb-anatomy.tsv'].splitlines()[1:] if l.strip()]
    n = len(rows)
    col = lambda i: sum(int(r[i]) for r in rows)  # noqa: E731
    dot = sum(1 for r in rows if int(r[6]) > 0)
    head = cap['mtree-pacman-head.txt']
    man = cap['man-pkgbuild-runinside.txt'].splitlines()
    vc = [l.strip() for l in cap['vercmp.txt'].splitlines() if l.strip()]
    exp = {
        'PA1': (['./.BUILDINFO', './.PKGINFO', 'pacman 7.1.0.r9.g54d9411-3']
                if './.BUILDINFO ' in head and './.PKGINFO ' in head else None),
        'PA4': [f'mtree {col(3)} of {n}', f'install {col(4)} of {n}', f'changelog {col(5)} of {n}',
                f'dot-files {dot} of {n}'],
        'PA5': [f'gzip {col(7)} of {n}', f'self-listed {col(8)} of {n}'],
        'PA6': [f'mtree {col(3)} of {n}'],
        'PA7': [f"{len(man)} lines", f"{sum('$srcdir' in l for l in man)} `$srcdir`",
                f"{sum('$startdir' in l for l in man)} `$startdir`"],
        'PA8': [l for l in vc if l.startswith(('vercmp 1:1.0-1 2.0-1 ', 'vercmp 0:2.0-1 2.0-1 ',
                                                'vercmp 1.0 1.0-5 '))],
    }
    return exp, {'entries': n}


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
            raise _revision.RevisionError('E-GIT-FAILED', 'novelty', p.stderr.decode()[:200])
        hits[tok] = sum(int(l.rsplit(':', 1)[1]) for l in p.stdout.decode().splitlines() if ':' in l)
    return hits


def verdicts(repo, rev):
    out = {k: {'holds': [], 'partly': [], 'fails': [], 'malformed': []} for k in REQUIRED}
    for d in VERDICT_DIRS:
        p = git(repo, 'ls-tree', '--name-only', f'{rev}:{d}')
        if p.returncode != 0:
            continue
        for name in p.stdout.decode().splitlines():
            m = re.match(r'^C2Rev(PA\d+)[A-Za-z0-9-]*\.md$', name)
            if not m or m.group(1) not in out:
                continue
            body = git_show(repo, rev, f'{d}/{name}') or ''
            first = body.splitlines()[0] if body else ''
            vm = VERDICT_RE.match(first)
            if not vm or not re.search(r'\b' + m.group(1) + r'\b', body):
                out[m.group(1)]['malformed'].append(f'{d}/{name}')
                continue
            out[m.group(1)][vm.group(1)].append(f'{d}/{name}')
    return out


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
    hexp, hmeta = host_expect(cap)
    bad = [k for k in vals if vals[k] is None] + [k for k in hexp if hexp[k] is None]
    if bad:
        print(json.dumps({'counter': COUNTER_ID, 'error': 'frozen pattern unmatched: ' + ','.join(bad), 'exit': 2}))
        return 2
    srcl = {k: v.splitlines() for k, v in src.items()}
    rec = {'counter': COUNTER_ID, 'revision': b.sha, 'branch_tip': b.branch_tip, 'derived': vals,
           'host_expect': hexp, 'host_meta': hmeta, 'novelty': nov,
           'predicate': 'rules_verified == 8 and verdicts_ok == 8 and host_ok == 6 and source_ok == 1 and '
                        'duplicate_rows == 0 and duplicate_headings == 0 and novelty_base_hits == 0'}
    entry = git_show(a.repo, b.sha, ENTRY)
    srows = parse_sources(git_show(a.repo, b.sha, SOURCES) or '')
    base_ids = set(parse_sources(git_show(a.repo, BASE, SOURCES) or ''))
    vd = verdicts(a.repo, b.sha)
    rules, verified, dup_rows, dup_heads, source_ok, host_ok = {}, 0, 0, 0, 0, 0
    verdicts_ok = sum(1 for k in REQUIRED if vd[k]['holds'] and not vd[k]['fails'])
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
        for pa, (want, wlo, whi) in REQUIRED.items():
            r = {'present': pa in seen, 'verified': False, 'reasons': [], 'host_ok': False}
            rules[pa] = r
            if pa not in seen:
                continue
            cells = [c.strip() for c in seen[pa][0].strip().strip('|').split('|')]
            if len(cells) < 5:
                r['reasons'].append('fewer than 5 cells')
                continue
            rule, value, src_cell, host_cell = cells[1], cells[2], cells[3], cells[4]
            rc = collapse(rule)
            if value.replace('`', '').strip() != vals[pa]:
                r['reasons'].append(f'value {value!r} != derived {vals[pa]!r}')
            for rel in RELATIONS[pa]:
                if not re.search(rel, rc):
                    r['reasons'].append(f'relation unmet: {rel}')
            neg = NEG.search(rc)
            if neg:
                r['reasons'].append(f'rule carries negation word {neg.group(0)!r}')
            if len(rc.split()) < 12:
                r['reasons'].append('rule shorter than 12 words')
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
            refs = [(f, int(x), int(y or x)) for f, x, y in REF_RE.findall(src_cell) if f == want]
            for fname, lo, hi in refs:
                if not (wlo <= lo <= hi <= whi):
                    r['reasons'].append(f'cited range {fname}:{lo}-{hi} outside window {wlo}-{whi}')
                    continue
                body = collapse(' '.join(srcl[want][lo - 1:hi]))
                for qt in QUOTE_RE.findall(src_cell):
                    qc = collapse(qt)
                    if 4 <= len(qc.split()) <= 25 and qc in body:
                        quote_ok = True
                        copied = copied or qc in rc
            if not quote_ok:
                r['reasons'].append(f'no 4-25 word quote found in {want} at cited lines inside the window')
            if copied:
                r['reasons'].append('rule cell contains its own quote')
            r['verdicts'] = vd[pa]
            r['verified'] = not r['reasons']
            verified += int(r['verified'])
            if pa in hexp:
                hc = host_cell.replace('`', '')
                r['host_ok'] = all(x.replace('`', '') in hc for x in hexp[pa])
                host_ok += int(r['host_ok'])
    nov_total = sum(nov.values())
    ok = (verified == 8 and verdicts_ok == 8 and host_ok == 6 and source_ok == 1 and dup_rows == 0
          and dup_heads == 0 and nov_total == 0)
    rec.update({'entry_present': entry is not None, 'rules_verified': verified, 'verdicts_ok': verdicts_ok,
                'host_ok': host_ok, 'source_ok': source_ok, 'duplicate_rows': dup_rows,
                'duplicate_headings': dup_heads, 'novelty_base_hits': nov_total, 'rules': rules,
                'verdicts': vd, 'result': 'PASS' if ok else 'FAIL', 'exit': 0 if ok else 1})
    print(json.dumps(rec, indent=1))
    return rec['exit']


if __name__ == '__main__':
    sys.exit(main())
