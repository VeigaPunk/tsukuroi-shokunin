#!/usr/bin/env python3
"""Count the verified premises of the round-24 pause-lift update-safety gate entry.

The counting rule is the one declared with claim C2 in SCORECARD.md, section
"Round 24 — declaration, attempt 2", amended per RevGateSchema-2:

  A premise counts only if its verdict is one of the decided verdicts cleared,
  still-holds or changed (an `unverified` verdict is a valid schema value but
  does not count); it carries at least one value anchor — a unique,
  non-boilerplate evidence line inside its value-section set, or a zero-form
  echo-and-exit pair (a `$ ` command echo line N plus the `exit=` line N+1,
  both in the value-section set, needles equal to their full lines); every
  evidence pointer resolves at the revision (line exists, exact substring
  present, needle unique unless part of a zero pair); evidence lines that begin
  with the capture's boilerplate (`### `, `$ `, `exit=`) are not anchors and
  are rejected unless they form a zero pair; every listed source id is a
  single, unique row of corpus/SOURCES.md at the revision whose status cell is
  `mined`, whose `used-by` cell names the premise id (pause-lift-gate-r24#Px),
  and whose `opened` cell contains 2026-10-22; any finding forces the gate to
  fail; and evidence that is not inside the declared capture must be pinned by
  sha256 in the gate's `pins` map.

Every byte is read from the git object database at the bound revision (`git
cat-file blob`, read-only). The host is never probed, no package state is
re-measured, and nothing here lifts or justifies lifting the pacman pause.

Exit codes:
  0  premises_verified == 5 and premises_total == 5, no findings, valid document
  1  the gate entry is missing or malformed, a premise does not count, or any
     finding is present
  2  the revision cannot be bound or read (could not evaluate)

Scope: a count of evidence links in committed bytes. Not runtime prevention,
not a no-harm proof, not an authorization of any package transaction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True

SCHEMA = 'tsukuroi-pause-gate-v1'
GATE = 'corpus/knowledge/pause-lift-gate-r24.json'
SOURCES = 'corpus/SOURCES.md'
SELF_PATHS = (GATE, 'corpus/knowledge/pause-lift-gate-r24.md')
IDS = ('P1', 'P2', 'P3', 'P4', 'P5')
VERDICTS = ('cleared', 'still-holds', 'changed', 'unverified')
DECIDED_VERDICTS = ('cleared', 'still-holds', 'changed')
SOURCES_DATE = '2026-10-22'
ROW = re.compile(r'^\|\s*(S\d{3})\s*\|')
SECTION_HEADER = re.compile(r'^### (.+)$')
BOILERPLATE = ('### ', '$ ', 'exit=')
# Value-section set per premise (RevGateSchema-2 finding N1a).
SECTION_MAP = {
    'P1': {'pending', 'pending-count', 'pending-repos', 'checkupdates-temp-db'},
    'P2': {'local-newer-than-sync'},
    'P3': {'hooks-new-root', 'buildroot-symlink', 'init-root', 'boots',
            'boot0-root-mount', 'plymouth-boot0', 'plymouth-boot-1',
            'loader-entry', 'cmdline-boot-flags', 'boot-chain-installed'},
    'P4': {'sync-db-mtime', 'sync-db-ctime-birth', 'stable-mirror-headers',
            'mirror-servers', 'repo-servers', 'pacman-log-last-sync',
            'pacman-commands-since-pause'},
    'P5': {'cache-entries', 'cache-package-files',
            'sudo-package-commands-since-pause', 'paccache-runs-since-pause',
            'pacman-log-since-pause', 'pacman-commands-since-pause',
            'foreign-new', 'snap-pac', 'snapper-list'},
}
SCRATCH = Path('/fast/scratch/hyaku/tsuku24-ExecPauseGateChecker')


def find_root():
    """The lane root: the nearest ancestor that holds tools/_revision.py."""
    starts = []
    for origin in (Path.cwd(), Path(__file__)):
        try:
            starts.append(origin.resolve())
        except OSError:
            continue
    for start in starts:
        for candidate in (start, *start.parents):
                return candidate
    return Path.cwd().resolve()


ROOT = find_root()
sys.path.insert(0, str(ROOT / 'tools'))
import _revision  # noqa: E402  (the import path depends on ROOT)


class DuplicateKey(ValueError):
    """A repeated object key in a JSON document."""

    def __init__(self, key):
        super().__init__(f'duplicate JSON key: {key}')
        self.key = key


def unique(pairs):
    """object_pairs_hook that rejects a repeated key instead of keeping the last."""
    out = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKey(key)
        out[key] = value
    return out


def lane_relative(path):
    """True when `path` is a lane-relative path that cannot escape the lane."""
    if not isinstance(path, str) or not path or path.startswith('/'):
        return False
    return '..' not in path.split('/')


def normalized(path):
    """A comparable form of a lane-relative path."""
    return posixpath.normpath(path) if isinstance(path, str) else None


def in_capture(path, capture):
    """True when `path` is the declared capture file or lives under it."""
    target, base = normalized(path), normalized(capture)
    if not target or not base:
        return False
    return target == base or target.startswith(base.rstrip('/') + '/')


class Reader:
    """Reads committed blobs of one revision of one repository."""

    def __init__(self, repo, sha):
        self.repo = str(repo)
        self.sha = sha
        self._cache = {}

    def read(self, path):
        if not lane_relative(path):
            return None
        if path in self._cache:
            return self._cache[path]
        proc = subprocess.run(['git', '--no-pager', '-C', self.repo, 'cat-file', 'blob',
                               f'{self.sha}:{path}'],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=_revision.clean_env(), timeout=30)
        text = proc.stdout.decode('utf-8', 'replace') if proc.returncode == 0 else None
        self._cache[path] = text
        return text


def source_rows(text):
    """Map a source id to every registry row: (opened, status, used_by)."""
    out = {}
    for line in (text or '').splitlines():
        match = ROW.match(line)
        if not match:
            continue
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if len(cells) < 11:
            continue
        out.setdefault(match.group(1), []).append(
            (cells[8], cells[7], cells[10]))
    return out


def capture_sections(text):
    """Return [(start_line, name), ...] for every `### ` section header."""
    sections = []
    for index, line in enumerate((text or '').splitlines(), start=1):
        match = SECTION_HEADER.match(line)
        if match:
            sections.append((index, match.group(1).strip()))
    return sections


def section_of(sections, line):
    """Name of the section holding 1-based `line`, or None."""
    name = None
    for start, section_name in sections:
        if start <= line:
            name = section_name
        else:
            break
    return name


def pinned(reader, gate, path):
    """Non-capture evidence is allowed only when pinned by sha256 in the gate."""
    pins = gate.get('pins') if isinstance(gate, dict) else None
    text = reader.read(path)
    if text is None:
        return None, 'evidence-file-absent-at-revision'
    if not isinstance(pins, dict) or path not in pins:
        return None, 'evidence-non-capture-unpinned'
    digest = hashlib.sha256(text.encode('utf-8', 'replace')).hexdigest()
    if pins[path] != digest:
        return None, 'evidence-non-capture-pin-mismatch'
    return text, None


def resolve_pointer(pointer, reader, index, capture, capture_text, sections, gate):
    """Resolve one evidence pointer against the committed bytes."""
    detail = {'index': index, 'path': None, 'line': None, 'contains': None,
              'resolved': False, 'in_capture': False, 'section': None,
              'line_text': None, 'problem': None}
    if not isinstance(pointer, dict) or set(pointer) != {'path', 'line', 'contains'}:
        detail['problem'] = 'evidence-shape'
        return detail
    path, line, needle = pointer['path'], pointer['line'], pointer['contains']
    detail.update(path=path if isinstance(path, str) else None,
                  line=line if isinstance(line, int) and not isinstance(line, bool) else None,
                  contains=needle if isinstance(needle, str) else None)
    if not lane_relative(path):
        detail['problem'] = 'evidence-path-not-lane-relative'
        return detail
    if path in SELF_PATHS:
        detail['problem'] = 'evidence-self-referential'
        return detail
    if not isinstance(needle, str) or not needle.strip():
        detail['problem'] = 'evidence-substring-empty'
        return detail
    if len(needle) < 3:
        detail['problem'] = 'evidence-needle-short'
        return detail
    if type(line) is not int or line < 1:
        detail['problem'] = 'evidence-line-not-positive-int'
        return detail
    if in_capture(path, capture):
        if capture_text is None:
            detail['problem'] = 'evidence-capture-absent'
            return detail
        text = capture_text
        detail['in_capture'] = True
    else:
        text, problem = pinned(reader, gate, path)
        if text is None:
            detail['problem'] = problem
            return detail
    lines = text.splitlines()
    if line > len(lines):
        detail['problem'] = 'evidence-line-out-of-range'
        return detail
    observed = lines[line - 1]
    detail['line_text'] = observed
    detail['file_text'] = text
    if needle not in observed:
        detail['problem'] = 'evidence-substring-absent'
        return detail
    detail['resolved'] = True
    if detail['in_capture']:
        detail['section'] = section_of(sections, line)
    return detail


def zero_pair(points):
    """Return the (echo, exit) details of a zero-form pair, if any.

    A zero form is a `$ ` command echo line N plus the `exit=` line N+1, with
    no lines between, both inside the premise's value-section set and each
    needle equal to its full line.
    """
    by_line = {p['line']: p for p in points if p['resolved'] and p['in_capture']}
    for line, point in by_line.items():
        text = point.get('line_text') or ''
        if not text.startswith('$ '):
            continue
        mate = by_line.get(line + 1)
        if not mate:
            continue
        mate_text = mate.get('line_text') or ''
        if not mate_text.startswith('exit='):
            continue
        if point.get('contains') != text.strip():
            continue
        if mate.get('contains') != mate_text.strip():
            continue
        return point, mate
    return None


def check_premise(premise, reader, gate, dates, capture, capture_text, sections, seen_ids):
    """Apply the counting rule to one premise entry."""
    problems = []
    detail = {'id': None, 'premise': None, 'verdict': None, 'verified': False,
              'problems': problems, 'evidence': [], 'sources': [], 'capture_line': False}
    if not isinstance(premise, dict):
        problems.append('premise-not-an-object')
        return detail
    pid = premise.get('id')
    detail['id'] = pid if isinstance(pid, str) else None
    detail['verdict'] = premise.get('verdict') if isinstance(premise.get('verdict'), str) else None
    text = premise.get('premise')
    detail['premise'] = text if isinstance(text, str) else None
    if pid not in IDS:
        problems.append('id-not-in-p1-p5')
    elif pid in seen_ids:
        problems.append('id-duplicate')
    else:
        seen_ids.add(pid)
    if not isinstance(text, str) or not text.strip():
        problems.append('premise-text-missing')
    limits = premise.get('limits')
    if not isinstance(limits, str) or not limits.strip():
        problems.append('limits-missing')
    verdict = premise.get('verdict')
    if verdict not in VERDICTS:
        problems.append('verdict-not-in-vocabulary')
    elif verdict not in DECIDED_VERDICTS:
        problems.append('verdict-undecided')

    evidence = premise.get('evidence')
    points = []
    if not isinstance(evidence, list) or not evidence:
        problems.append('evidence-empty')
    else:
        for index, pointer in enumerate(evidence):
            point = resolve_pointer(pointer, reader, index, capture, capture_text, sections, gate)
            detail['evidence'].append(point)
            if not point['resolved']:
                problems.append(point['problem'])
            elif point['in_capture']:
                detail['capture_line'] = True
                points.append(point)
        pair = zero_pair(points) if points else None
        allowed = SECTION_MAP.get(pid, set())
        anchor = None
        if pair is None:
            for point in points:
                line_text = point.get('line_text') or ''
                if line_text.startswith(BOILERPLATE):
                    continue
                if point.get('section') not in allowed:
                    continue
                needle = point.get('contains') or ''
                file_text = point.get('file_text') or ''
                if file_text.count(needle) != 1:
                    continue
                anchor = point
                break
            if anchor is None:
                problems.append('no-value-anchor')

    sources = premise.get('sources')
    if not isinstance(sources, list) or not sources:
        problems.append('sources-empty')
    else:
        listed = []
        for sid in sources:
            row = {'id': sid if isinstance(sid, str) else None, 'opened': None,
                   'status': None, 'used_by': None, 'ok': False}
            detail['sources'].append(row)
            if not isinstance(sid, str) or sid not in dates:
                problems.append(f'source-missing:{sid}')
                continue
            rows = dates[sid]
            if len(rows) > 1:
                problems.append(f'source-duplicate-rows:{sid}')
                continue
            opened, status, used_by = rows[0]
            row.update(opened=opened, status=status, used_by=used_by)
            if status != 'mined':
                problems.append(f'source-status-not-mined:{sid}')
                continue
            if not re.search(rf'pause-lift-gate-r24(\.(json|md))?#{re.escape(pid)}', used_by):
                problems.append(f'source-used-by-not-this-premise:{sid}')
                continue
            if SOURCES_DATE not in opened:
                problems.append(f'source-opened-on-another-date:{sid}')
                continue
            if sid in listed:
                problems.append(f'source-duplicated:{sid}')
                continue
            listed.append(sid)
            row['ok'] = True
    if capture and not detail['capture_line']:
        problems.append('no-resolvable-capture-line')
    detail['verified'] = not problems
    return detail


def evaluate(reader):
    """Count the premises of the gate entry at the reader's revision."""
    findings = []
    result = {'gate': GATE, 'sources': SOURCES, 'sources_opened_date': SOURCES_DATE,
              'capture': None, 'document_valid': False, 'premises_total': 0,
              'premises_verified': 0, 'premises_unverified': 0, 'verdicts': {},
              'premises': [], 'findings': findings}

    def add(fid, site, detail_text=None):
        finding = {'id': fid, 'site': site}
        if detail_text:
            finding['detail'] = detail_text
        findings.append(finding)

    raw = reader.read(GATE)
    if raw is None:
        add('GATE-MISSING', GATE, 'the gate entry is not present at the revision')
        return result
    try:
        gate = json.loads(raw, object_pairs_hook=unique)
    except DuplicateKey as exc:
        add('GATE-JSON-DUPLICATE-KEY', GATE, str(exc))
        return result
    except ValueError as exc:
        add('GATE-JSON', GATE, str(exc))
        return result
    if not isinstance(gate, dict):
        add('GATE-SCHEMA', GATE, 'the gate entry is not a JSON object')
        return result
    if gate.get('schema') != SCHEMA:
        add('GATE-SCHEMA', GATE, f'schema is {gate.get("schema")!r}, expected {SCHEMA!r}')
        return result
    captured_at = gate.get('captured_at')
    if not isinstance(captured_at, str) or not captured_at.strip():
        add('GATE-SCHEMA', GATE, 'captured_at is missing or not a string')
        return result
    result['captured_at'] = captured_at
    capture = gate.get('capture')
    if not lane_relative(capture):
        add('GATE-CAPTURE', GATE, 'capture is missing or not a lane-relative path')
        return result
    result['capture'] = capture
    capture_text = reader.read(capture)
    if capture_text is None:
        add('GATE-CAPTURE', capture, 'the declared capture is not present at the revision')
    sections = capture_sections(capture_text) if capture_text is not None else []
    premises = gate.get('premises')
    if not isinstance(premises, list):
        add('GATE-SCHEMA', GATE, 'premises is missing or not a list')
        return result

    dates = source_rows(reader.read(SOURCES))
    seen = set()
    for premise in premises:
        detail = check_premise(premise, reader, gate, dates, capture, capture_text,
                               sections, seen)
        result['premises'].append(detail)
        for problem in detail['problems']:
            add('GATE-PREMISE', f'{detail["id"] or "?"}:{problem}')
    result['premises_total'] = len(premises)
    result['premises_verified'] = sum(1 for d in result['premises'] if d['verified'])
    result['premises_unverified'] = sum(
        1 for d in result['premises'] if d.get('verdict') == 'unverified')
    for d in result['premises']:
        verdict = d.get('verdict')
        if verdict:
            result['verdicts'][verdict] = result['verdicts'].get(verdict, 0) + 1
    if sorted(d['id'] for d in result['premises'] if d['id']) != list(IDS):
        add('GATE-PREMISE-SET', ','.join(sorted(str(d['id']) for d in result['premises'])),
            'the premises are not exactly P1..P5')
    for sid, rows in sorted(dates.items()):
        if len(rows) > 1:
            add('GATE-SOURCE-DUPLICATE', sid, f'{len(rows)} registry rows')
    result['document_valid'] = not any(f['id'] in ('GATE-MISSING', 'GATE-JSON',
                                                    'GATE-JSON-DUPLICATE-KEY', 'GATE-SCHEMA',
                                                    'GATE-CAPTURE')
                                        for f in findings)
    return result


def passed(result):
    """Exit 0 only for five decided premises out of five, no findings, valid doc."""
    return (result.get('document_valid') is True
            and not result.get('findings')
            and result.get('premises_verified') == 5
            and result.get('premises_total') == 5)


def run(repo, revision, branch='master'):
    """Bind the revision and count the premises over its committed bytes."""
    binding = _revision.bind(repo, revision, branch)
    result = evaluate(Reader(repo, binding.sha))
    result['revision'] = binding.sha
    result['branch'] = binding.branch
    result['status'] = 'PASS' if passed(result) else 'FAIL'
    return (0 if passed(result) else 1), result


def git(repo, *args):
    proc = subprocess.run(['git', '-C', str(repo), '-c', 'user.name=selftest',
                           '-c', 'user.email=selftest@invalid', '-c', 'commit.gpgsign=false',
                           *args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=_revision.clean_env(), timeout=60)
    if proc.returncode != 0:
        raise RuntimeError(f'git {args[0]} exited {proc.returncode}: '
                           f'{proc.stderr.decode("utf-8", "replace").strip()[:160]}')
    return proc.stdout.decode('utf-8', 'replace')


def sandbox_repo(root, files):
    """Create a git repository holding `files` and return its head commit."""
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', 'init', '--quiet', '--initial-branch=master', str(root)],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   env=_revision.clean_env(), timeout=60, check=True)
    for relative, content in files.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
    git(root, 'add', '-A')
    git(root, 'commit', '--quiet', '-m', 'round-24 pause gate fixture')
    return git(root, 'rev-parse', 'HEAD').strip()


def sources_fixture():
    rows = ['| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |',
            '|---|---|---|---|---|---|---|---|---|---|---|']
    for pid in IDS:
        rows.append(f'| S9{IDS.index(pid)+1:02d} | pause gate fixture row for {pid} | docs | A | round-24 gate fixture | row S9{IDS.index(pid)+1:02d} | the opened cell of a fixture row | mined | 2026-10-22 | 90d | corpus/knowledge/pause-lift-gate-r24.md#{pid} |')
    rows.append('| S909 | pause gate fixture, opened earlier | docs | A | round-24 gate fixture | row S909 | the opened cell of a fixture row | mined | 2026-10-19 | 90d | corpus/knowledge/pause-lift-gate-r24.md#P1 |')
    rows.append('| S910 | pause gate fixture, rejected | docs | A | round-24 gate fixture | row S910 | a recorded refutation | rejected | 2026-10-22 | 90d | corpus/knowledge/pause-lift-gate-r24.md#P1 |')
    rows.append('| S911 | pause gate fixture, unused | docs | A | round-24 gate fixture | row S911 | a row used elsewhere | mined | 2026-10-22 | 90d | corpus/knowledge/other.md |')
    rows.append('| S912 | pause gate fixture, wrong premise | docs | A | round-24 gate fixture | row S912 | a row bound to P2 | mined | 2026-10-22 | 90d | corpus/knowledge/pause-lift-gate-r24.md#P2 |')
    return ('\n'.join(rows) + '\n')


SOURCES_FIXTURE = sources_fixture()

CAPTURE_FIXTURE = (
    '### time\n2026-10-22\n'
    '### pending\n$ pacman -Qu\n1password-beta 1.0-1 -> 1.1-1\n'
    '### pending-count\n$ pacman -Qu | wc -l\n3\n'
    '### pending-repos\n$ for p in $(pacman -Qqu); do printf "%s " "$p"; done\n1password-beta omarchy\n'
    '### local-newer-than-sync\n$ pacman -Sl | sed -n "s/.*/&/p" | while read -r repo name syncv localv; do [ "$(vercmp "$localv" "$syncv")" -gt 0 ] && echo "$repo $name sync=$syncv local=$localv"; done; true\nexit=0\n'
    '### boot-chain-installed\nboot-chain-installed line\n'
    '### boot-chain-sync\nboot-chain-sync line\n'
    '### boots\nboots line\n'
    '### boot0-root-mount\nboot0-root-mount line\n'
    '### plymouth-boot0\nplymouth-boot0 line\n'
    '### plymouth-boot-1\nplymouth-boot-1 line\n'
    '### loader-entry\nloader-entry line\n'
    '### cmdline-boot-flags\ncmdline-boot-flags line\n'
    '### hooks-new-root\n$ grep -n "/new_root" /usr/lib/initcpio/hooks/* 2>/dev/null; true\nbtrfs-overlayfs:4\nplymouth:11\n'
    '### hooks-config\nhooks-config line\n'
    '### init-root\ninit-root line\n'
    '### buildroot-symlink\n$ grep -rn "new_root" /usr/lib/initcpio/functions 2>/dev/null; true\nln -s "sysroot"\n'
    '### pacman-log-since-pause\ninstalled zcode (3.16.2-1)\n'
    '### pacman-log-last-sync\n3189:[2026-10-21T20:32:00-0300]\n'
    '### mirror-servers\nServer = https://stable-mirror.omarchy.org/$repo/os/$arch\n'
    '### repo-servers\nInclude = /etc/pacman.d/mirrorlist\n'
    '### sync-db-mtime\n$ stat -c "%y %n" /var/lib/pacman/sync/core.db\n2026-10-17 22:37:29.000000000 -0300 /var/lib/pacman/sync/core.db\n'
    '### sync-db-ctime-birth\nsync-db-ctime-birth line\n'
    '### stable-mirror-headers\nstable-mirror-headers line\n'
    '### cache-file-count\n4\n'
    '### cache-entries\n$ ls -la /var/cache/pacman/pkg\ntotal 0\n'
    '### cache-package-files\n$ find /var/cache/pacman/pkg -maxdepth 1 -name "*.pkg.tar*" | wc -l\n0\n'
    '### pacman-commands-since-pause\npacman -U --needed\n'
    '### sudo-package-commands-since-pause\nsudo pacman -U\n'
    '### foreign-new\nforeign-new line\n'
    '### snap-pac\nsnap-pac line\n'
    '### snapper-list\nsnapper-list line\n'
    '### paccache-runs-since-pause\npaccache -rk1\n'
    '### checkupdates-temp-db\ncheckupdates rows=134\n'
)

CAPTURE_PATH = '.ufo/waves/round-24/capture/l1-4/capture.txt'


def line_of(text, needle):
    lines = text.splitlines()
    match = [i for i, line in enumerate(lines, start=1) if needle in line]
    if len(match) != 1:
        raise AssertionError(f'needle not unique in fixture: {needle!r} -> {match}')
    return match[0]


def gate_fixture(mutate=None, raw=None):
    """The pristine gate document, optionally mutated."""
    capture = CAPTURE_FIXTURE
    body = {'schema': SCHEMA, 'captured_at': '2026-10-22T08:19:59Z',
            'capture': CAPTURE_PATH, 'premises': []}
    specs = {
        'P1': ('pending', '1password-beta 1.0-1 -> 1.1-1'),
        'P2': ('local-newer-than-sync', None),
        'P3': ('hooks-new-root', 'btrfs-overlayfs:4'),
        'P4': ('sync-db-mtime', '2026-10-17 22:37:29.000000000 -0300 /var/lib/pacman/sync/core.db'),
        'P5': ('cache-entries', 'total 0'),
    }
    for pid in IDS:
        section, value = specs[pid]
        if value is not None:
            evidence = [{'path': CAPTURE_PATH, 'line': line_of(capture, value),
                         'contains': value}]
        else:
            lines = capture.splitlines()
            echo_idx = next(i for i, l in enumerate(lines) if l.startswith('$ pacman -Sl'))
            exit_idx = next(i for i, l in enumerate(lines) if l.strip() == 'exit=0')
            evidence = [{'path': CAPTURE_PATH, 'line': echo_idx + 1,
                         'contains': lines[echo_idx].strip()},
                        {'path': CAPTURE_PATH, 'line': exit_idx + 1,
                         'contains': lines[exit_idx].strip()}]
        body['premises'].append({
            'id': pid,
            'premise': f'{pid} fixture premise',
            'verdict': 'changed',
            'evidence': evidence,
            'sources': [f'S9{IDS.index(pid)+1:02d}'],
            'limits': 'fixture only',
        })
    if mutate:
        mutate(body)
    return raw if raw is not None else json.dumps(body)


def selftest():
    """Drive the checker over sandbox repositories; every mutant must be caught."""
    root = SCRATCH
    try:
        root.mkdir(parents=True, exist_ok=True)
        probe = root / '.writable'
        probe.write_text('probe', encoding='utf-8')
        probe.unlink()
    except OSError:
        import tempfile
        root = Path(tempfile.mkdtemp(prefix='tsuku24-pause-gate-'))
    base = {'corpus/SOURCES.md': SOURCES_FIXTURE, CAPTURE_PATH: CAPTURE_FIXTURE}

    def drop_premise(body):
        body['premises'].pop()

    def bad_verdict(body):
        body['premises'][0]['verdict'] = 'safe'

    def undecided_verdict(body):
        for premise in body['premises']:
            premise['verdict'] = 'unverified'

    def line_out_of_range(body):
        body['premises'][0]['evidence'][0]['line'] = 9999

    def substring_absent(body):
        body['premises'][0]['evidence'][0]['contains'] = 'zzz-not-in-the-capture'

    def needle_short(body):
        body['premises'][0]['evidence'][0]['contains'] = 'ab'

    def needle_boilerplate(body):
        needle = '### sync-db-mtime'
        body['premises'][0]['evidence'][0]['line'] = line_of(CAPTURE_FIXTURE, needle)
        body['premises'][0]['evidence'][0]['contains'] = needle

    def need_duplicated(body):
        p = body['premises'][0]['evidence'][0]
        p['line'] = line_of(CAPTURE_FIXTURE, 'boots line')
        p['contains'] = 'line'

    def source_missing(body):
        body['premises'][0]['sources'] = ['S999']

    def source_other_date(body):
        body['premises'][0]['sources'] = ['S909']

    def source_rejected(body):
        body['premises'][0]['sources'] = ['S910']
    def source_unused(body):
        body['premises'][0]['sources'] = ['S911']
    def source_wrong_premise(body):
        body['premises'][0]['sources'] = ['S912']

    def source_duplicate_row(body):
        pass  # handled by extra SOURCES fixture below

    def bad_schema(body):
        body['schema'] = 'tsukuroi-pause-gate-v0'

    def capture_absent(body):
        body['capture'] = '.ufo/waves/round-24/capture/l1/missing.txt'

    def duplicate_id(body):
        body['premises'][1]['id'] = 'P1'

    def limits_absent(body):
        body['premises'][0].pop('limits')

    def premise_text_absent(body):
        body['premises'][0].pop('premise')

    def section_mismatch(body):
        body['premises'][0]['evidence'][0]['line'] = line_of(CAPTURE_FIXTURE, 'boots line')
        body['premises'][0]['evidence'][0]['contains'] = 'boots line'

    def anchor_boilerplate_line(body):
        needle = '$ pacman -Qu | wc -l'
        body['premises'][0]['evidence'][0]['line'] = line_of(CAPTURE_FIXTURE, needle)
        body['premises'][0]['evidence'][0]['contains'] = needle

    def zero_pair_broken(body):
        body['premises'][1]['evidence'] = [
            {'path': CAPTURE_PATH, 'line': line_of(CAPTURE_FIXTURE, '$ pacman -Sl'),
             'contains': '$ pacman -Sl'}]

    def evidence_outside_capture(body):
        body['premises'][0]['evidence'][0]['path'] = 'corpus/SOURCES.md'
        body['premises'][0]['evidence'][0]['line'] = line_of(SOURCES_FIXTURE, 'S901')
        body['premises'][0]['evidence'][0]['contains'] = 'S901'

    def self_evidence(body):
        body['premises'][0]['evidence'][0]['path'] = GATE
        body['premises'][0]['evidence'][0]['line'] = 1
        body['premises'][0]['evidence'][0]['contains'] = 'schema'

    cases = [
        ('pristine', {}, 0, None),
        ('missing-premise', {'mutate': drop_premise}, 1, 'GATE-PREMISE-SET'),
        ('bad-verdict', {'mutate': bad_verdict}, 1, 'verdict-not-in-vocabulary'),
        ('all-unverified', {'mutate': undecided_verdict}, 1, 'verdict-undecided'),
        ('evidence-line-out-of-range', {'mutate': line_out_of_range}, 1,
         'evidence-line-out-of-range'),
        ('substring-absent', {'mutate': substring_absent}, 1, 'evidence-substring-absent'),
        ('needle-short', {'mutate': needle_short}, 1, 'evidence-needle-short'),
        ('needle-boilerplate', {'mutate': needle_boilerplate}, 1,
         'no-value-anchor'),
        ('needle-not-unique', {'mutate': need_duplicated}, 1,
         'no-value-anchor'),
        ('source-missing', {'mutate': source_missing}, 1, 'source-missing:S999'),
        ('source-opened-on-another-date', {'mutate': source_other_date}, 1,
         'source-opened-on-another-date:S909'),
        ('source-status-rejected', {'mutate': source_rejected}, 1,
         'source-status-not-mined:S910'),
        ('source-used-by-other', {'mutate': source_unused}, 1,
         'source-used-by-not-this-premise:S911'),
        ('source-used-by-wrong-premise', {'mutate': source_wrong_premise}, 1,
         'source-used-by-not-this-premise:S912'),
        ('duplicate-json-key', {'raw': '{"schema":"tsukuroi-pause-gate-v1",'
                                      '"schema":"tsukuroi-pause-gate-v1",'
                                      '"captured_at":"2026-10-22T08:19:59Z",'
                                      f'"capture":"{CAPTURE_PATH}",'
                                      '"premises":[]}'}, 1, 'GATE-JSON-DUPLICATE-KEY'),
        ('wrong-schema', {'mutate': bad_schema}, 1, 'GATE-SCHEMA'),
        ('capture-absent', {'mutate': capture_absent}, 1, 'GATE-CAPTURE'),
        ('duplicate-premise-id', {'mutate': duplicate_id}, 1, 'GATE-PREMISE-SET'),
        ('limits-absent', {'mutate': limits_absent}, 1, 'limits-missing'),
        ('premise-text-absent', {'mutate': premise_text_absent}, 1,
         'premise-text-missing'),
        ('section-mismatch', {'mutate': section_mismatch}, 1, 'no-value-anchor'),
        ('anchor-boilerplate-line', {'mutate': anchor_boilerplate_line}, 1,
         'no-value-anchor'),
        ('zero-pair-broken', {'mutate': zero_pair_broken}, 1, 'no-value-anchor'),
        ('evidence-outside-capture', {'mutate': evidence_outside_capture}, 1,
         'evidence-non-capture-unpinned'),
        ('self-referential-evidence', {'mutate': self_evidence}, 1,
         'evidence-self-referential'),
    ]

    observations = []
    for name, options, want_code, want_marker in cases:
        files = dict(base)
        files[GATE] = gate_fixture(**options)
        repo = root / f'case-{name}'
        if repo.exists():
            subprocess.run(['rm', '-rf', str(repo)], check=True)
        sha = sandbox_repo(repo, files)
        code, result = run(repo, sha)
        sites = [f'{f["id"]} {f["site"]} {f.get("detail", "")}' for f in result['findings']]
        marker_seen = want_marker is None or any(want_marker in site for site in sites)
        counted = result['premises_verified'] == 5 and result['premises_total'] == 5
        observations.append({'case': name, 'exit': code, 'want_exit': want_code,
                              'premises_total': result['premises_total'],
                              'premises_verified': result['premises_verified'],
                              'document_valid': result['document_valid'],
                              'marker': want_marker, 'marker_seen': marker_seen,
                              'findings': sites,
                              'pass': code == want_code and marker_seen and (want_code == 0) == counted})

    # Finding-forces-exit-1: an unused duplicate registry row.
    files = dict(base)
    files['corpus/SOURCES.md'] = SOURCES_FIXTURE + (
        '| S901 | duplicate unused row, stale | docs | A | round-24 gate fixture | row A | n/a | mined | 2026-10-19 | 90d | corpus/knowledge/other.md |\n')
    files[GATE] = gate_fixture()
    repo = root / 'case-unused-duplicate-row'
    if repo.exists():
        subprocess.run(['rm', '-rf', str(repo)], check=True)
    sha = sandbox_repo(repo, files)
    code, result = run(repo, sha)
    sites = [f["id"] for f in result['findings']]
    observations.append({'case': 'unused-duplicate-row', 'exit': code, 'want_exit': 1,
                          'premises_total': result['premises_total'],
                          'premises_verified': result['premises_verified'],
                          'document_valid': result['document_valid'],
                          'marker': 'GATE-SOURCE-DUPLICATE',
                          'marker_seen': 'GATE-SOURCE-DUPLICATE' in sites,
                          'findings': sites,
                          'pass': code == 1 and 'GATE-SOURCE-DUPLICATE' in sites})

    # An unreadable revision is a distinct outcome: exit 2, cannot evaluate.
    try:
        _revision.bind(root / 'case-pristine', '0' * 40)
        unreadable = {'case': 'unreadable-revision', 'exit': None, 'pass': False}
    except _revision.RevisionError as exc:
        unreadable = {'case': 'unreadable-revision', 'exit': 2, 'finding': exc.fid,
                      'pass': exc.fid == _revision.E_INVALID}
    observations.append(unreadable)

    failed = sum(1 for o in observations if not o.get('pass'))
    summary = {'status': 'FAIL' if failed else 'PASS', 'cases': len(observations),
               'failed': failed, 'sandbox': str(root), 'observations': observations}
    print(json.dumps(summary, indent=1, sort_keys=True))
    return int(bool(failed))


def main(argv=None):
    parser = argparse.ArgumentParser(description=(__doc__ or '').splitlines()[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--revision', help='7-64 hex commit of the lane')
    mode.add_argument('--selftest', action='store_true')
    parser.add_argument('--branch', default='master')
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    if args.selftest:
        return selftest()
    try:
        code, result = run(ROOT, args.revision, args.branch)
    except _revision.RevisionError as exc:
        print(json.dumps({'status': 'CANNOT_EVALUATE', 'revision': args.revision,
                          'premises_total': 0, 'premises_verified': 0, 'premises': [],
                          'findings': [{'id': exc.fid, 'site': exc.site,
                                        'detail': exc.detail}]}, sort_keys=True))
        return 2
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status': 'CANNOT_EVALUATE', 'revision': args.revision,
                          'premises_total': 0, 'premises_verified': 0, 'premises': [],
                          'findings': [{'id': 'GATE-READ', 'site': str(exc)[:200]}]},
                         sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
