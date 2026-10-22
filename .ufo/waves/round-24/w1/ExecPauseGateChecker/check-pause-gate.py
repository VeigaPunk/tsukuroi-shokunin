#!/usr/bin/env python3
"""Count the verified premises of the round-24 pause-lift update-safety gate entry.

The counting rule is the one declared with claim C2 in SCORECARD.md, section
"Round 24 — declaration, attempt 2", amended per RevGateSchema-2:

  A premise counts only if its verdict is one of the decided verdicts cleared,
  still-holds or changed (an `unverified` verdict is a valid schema value but
  does not count); every evidence line exists at the revision and contains its
  exact substring, and the substring is not capture boilerplate and occurs
  exactly once in its file; at least one evidence pointer resolves into the
  capture section mapped to that premise; and every listed source id is a
  single, unique row of corpus/SOURCES.md at the revision whose fields are
  `mined` and whose `used-by` cell contains pause-lift-gate-r24, with an
  `opened` cell that contains 2026-10-22.

Every byte is read from the git object database at the bound revision (`git
cat-file blob`, read-only). The host is never probed, no package state is
re-measured, and nothing here lifts or justifies lifting the pacman pause.

Exit codes:
  0  premises_verified == 5 and premises_total == 5, and the document is valid
  1  the gate entry is missing or malformed, or a premise does not count
  2  the revision cannot be bound or read (could not evaluate)

Scope: a count of evidence links in committed bytes. Not runtime prevention,
not a no-harm proof, not an authorization of any package transaction.
"""
from __future__ import annotations

import argparse
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
# Capture section per premise (RevGateSchema-2 finding 5).
SECTION_MAP = {
    'P1': {'pending', 'pending-count', 'pending-repos'},
    'P2': {'local-newer-than-sync', 'boot-chain-installed', 'boot-chain-sync'},
    'P3': {'boots', 'plymouth-boot0', 'plymouth-boot-1', 'boot-chain-installed',
           'hooks-new-root', 'init-root', 'buildroot-symlink'},
    'P4': {'mirror-servers', 'repo-servers', 'sync-db-mtime', 'pacman-log-last-sync',
           'stable-mirror-headers'},
    'P5': {'cache-file-count', 'cache-package-files', 'cache-entries',
           'pacman-commands-since-pause', 'pacman-log-since-pause',
           'sudo-package-commands-since-pause', 'foreign-new',
           'paccache-runs-since-pause'},
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
            if (candidate / 'tools' / '_revision.py').is_file():
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
        self._kinds = {}

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


def check_evidence(pointer, reader, index, capture, sections):
    """Resolve one evidence pointer against the committed bytes."""
    detail = {'index': index, 'path': None, 'line': None, 'contains': None,
              'resolved': False, 'in_capture': False, 'section': None, 'problem': None}
    if not isinstance(pointer, dict) or set(pointer) != {'path', 'line', 'contains'}:
        detail['problem'] = 'evidence-shape'
        return detail
    path, line, needle = pointer['path'], pointer['line'], pointer['contains']
    detail['path'] = path if isinstance(path, str) else None
    detail['line'] = line if isinstance(line, int) and not isinstance(line, bool) else None
    detail['contains'] = needle if isinstance(needle, str) else None
    if not lane_relative(path):
        detail['problem'] = 'evidence-path-not-lane-relative'
        return detail
    if path in SELF_PATHS:
        detail['problem'] = 'evidence-self-referential'
        return detail
    if not isinstance(needle, str) or not needle.strip():
        detail['problem'] = 'evidence-substring-empty'
        return detail
    needle = needle.strip()
    if len(needle) < 3:
        detail['problem'] = 'evidence-needle-short'
        return detail
    if needle.startswith('###') or needle.lower().startswith('exit='):
        detail['problem'] = 'evidence-needle-boilerplate'
        return detail
    if type(line) is not int or line < 1:
        detail['problem'] = 'evidence-line-not-positive-int'
        return detail
    text = reader.read(path)
    if text is None:
        detail['problem'] = 'evidence-file-absent-at-revision'
        return detail
    lines = text.splitlines()
    if line > len(lines):
        detail['problem'] = 'evidence-line-out-of-range'
        return detail
    if needle not in lines[line - 1]:
        detail['problem'] = 'evidence-substring-absent'
        return detail
    if text.count(needle) != 1:
        detail['problem'] = 'evidence-needle-not-unique'
        return detail
    detail['resolved'] = True
    detail['in_capture'] = in_capture(path, capture)
    if detail['in_capture']:
        detail['section'] = section_of(sections, line)
    return detail


def check_premise(premise, reader, dates, capture, sections, seen_ids):
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
    if not isinstance(evidence, list) or not evidence:
        problems.append('evidence-empty')
    else:
        for index, pointer in enumerate(evidence):
            resolved = check_evidence(pointer, reader, index, capture, sections)
            detail['evidence'].append(resolved)
            if not resolved['resolved']:
                problems.append(resolved['problem'])
            elif resolved['in_capture']:
                detail['capture_line'] = True
        allowed = SECTION_MAP.get(pid, set())
        if not any(pointer['in_capture'] and pointer.get('section') in allowed
                   for pointer in detail['evidence']):
            problems.append('no-capture-section-fit')
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
            if 'pause-lift-gate-r24' not in used_by:
                problems.append(f'source-used-by-not-gate:{sid}')
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
              'premises_verified': 0, 'premises_unverified': 0,
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
        detail = check_premise(premise, reader, dates, capture, sections, seen)
        result['premises'].append(detail)
        for problem in detail['problems']:
            add('GATE-PREMISE', f'{detail["id"] or "?"}:{problem}')
    result['premises_total'] = len(premises)
    result['premises_verified'] = sum(1 for d in result['premises'] if d['verified'])
    result['premises_unverified'] = sum(
        1 for d in result['premises'] if d.get('verdict') == 'unverified')
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
    """Exit 0 only for five decided premises out of five in a valid document."""
    return (result.get('document_valid') is True
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


SOURCES_FIXTURE = (
    '| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
    '|---|---|---|---|---|---|---|---|---|---|---|\n'
    '| S901 | pause gate fixture, opened this round | docs | A | round-24 gate fixture | '
    'row S901 | the opened cell of a fixture row | mined | 2026-10-22 | 90d | '
    'corpus/knowledge/pause-lift-gate-r24.md |\n'
    '| S902 | pause gate fixture, opened earlier | docs | A | round-24 gate fixture | '
    'row S902 | the opened cell of a fixture row | mined | 2026-10-19 | 90d | '
    'corpus/knowledge/pause-lift-gate-r24.md |\n'
    '| S903 | pause gate fixture, rejected | docs | A | round-24 gate fixture | '
    'row S903 | a recorded refutation | rejected | 2026-10-22 | 90d | '
    'corpus/knowledge/pause-lift-gate-r24.md |\n'
    '| S904 | pause gate fixture, unused | docs | A | round-24 gate fixture | '
    'row S904 | a row used elsewhere | mined | 2026-10-22 | 90d | '
    'corpus/knowledge/other.md |\n'
)

CAPTURE_FIXTURE = (
    '### time\n2026-10-22\n'
    '### pending\n1password-beta 1.0-1 -> 1.1-1\n'
    '### pending-count\n3\n'
    '### pending-repos\n1password-beta omarchy\n'
    '### local-newer-than-sync\nlibinput 1.32.0-1\n'
    '### boot-chain-installed\nboot-chain-installed line\n'
    '### boot-chain-sync\nboot-chain-sync line\n'
    '### boots\nboots line\n'
    '### plymouth-boot0\nplymouth-boot0 line\n'
    '### plymouth-boot-1\nplymouth-boot-1 line\n'
    '### hooks-new-root\nbtrfs-overlayfs:4\nplymouth:11\n'
    '### hooks-config\nhooks-config line\n'
    '### init-root\ninit-root line\n'
    '### buildroot-symlink\nln -s "sysroot"\n'
    '### pacman-log-since-pause\ninstalled zcode (3.16.2-1)\n'
    '### pacman-log-last-sync\n3189:[2026-10-21T20:32:00-0300]\n'
    '### mirror-servers\nServer = https://stable-mirror.omarchy.org/$repo/os/$arch\n'
    '### repo-servers\nInclude = /etc/pacman.d/mirrorlist\n'
    '### sync-db-mtime\n2026-10-17 22:37:29.000000000 -0300 /var/lib/pacman/sync/core.db\n'
    '### stable-mirror-headers\nstable-mirror-headers line\n'
    '### cache-file-count\n4\n'
    '### cache-entries\ntotal 0\n'
    '### cache-package-files\n0\n'
    '### pacman-commands-since-pause\npacman -U --needed\n'
    '### sudo-package-commands-since-pause\nsudo pacman -U\n'
    '### foreign-new\nforeign-new line\n'
    '### paccache-runs-since-pause\npaccache -rk1\n'
    '### checkupdates-temp-db\ncheckupdates exit=0 rows=134\n'
)

CAPTURE_PATH = '.ufo/waves/round-24/capture/l1/capture.txt'


def line_of(text, needle):
    lines = text.splitlines()
    for index, line in enumerate(lines, start=1):
        if needle in line:
            return index
    raise AssertionError(f'needle not in fixture: {needle!r}')


def gate_fixture(mutate=None, raw=None):
    """The pristine gate document, optionally mutated."""
    capture = CAPTURE_FIXTURE
    pins = {'P1': '1password-beta 1.0-1 -> 1.1-1', 'P2': 'libinput 1.32.0-1',
            'P3': 'btrfs-overlayfs:4', 'P4': '2026-10-17 22:37:29.000000000 -0300 /var/lib/pacman/sync/core.db',
            'P5': 'total 0'}
    body = {'schema': SCHEMA, 'captured_at': '2026-10-22T08:19:59Z', 'capture': CAPTURE_PATH,
            'premises': []}
    for pid in IDS:
        body['premises'].append({
            'id': pid,
            'premise': f'{pid} fixture premise',
            'verdict': 'changed',
            'evidence': [{'path': CAPTURE_PATH, 'line': line_of(capture, pins[pid]),
                          'contains': pins[pid]}],
            'sources': ['S901'],
            'limits': 'fixture only',
        })
    if mutate:
        mutate(body)
    return raw if raw is not None else json.dumps(body)


def selftest():
    """Drive the checker over sandbox repositories; every mutant must be caught."""
    root = SCRATCH
    try:
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
        body['premises'][0]['evidence'][0]['contains'] = 'exit=0'

    def needle_duplicated(body):
        p = body['premises'][0]['evidence'][0]
        p['line'] = line_of(CAPTURE_FIXTURE, 'boots line')
        p['contains'] = 'line'

    def source_missing(body):
        body['premises'][0]['sources'] = ['S999']

    def source_other_date(body):
        body['premises'][0]['sources'] = ['S902']

    def source_rejected(body):
        body['premises'][0]['sources'] = ['S903']

    def source_unused(body):
        body['premises'][0]['sources'] = ['S904']

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
         'evidence-needle-boilerplate'),
        ('needle-not-unique', {'mutate': needle_duplicated}, 1,
         'evidence-needle-not-unique'),
        ('source-missing', {'mutate': source_missing}, 1, 'source-missing:S999'),
        ('source-opened-on-another-date', {'mutate': source_other_date}, 1,
         'source-opened-on-another-date:S902'),
        ('source-status-rejected', {'mutate': source_rejected}, 1,
         'source-status-not-mined:S903'),
        ('source-used-by-other', {'mutate': source_unused}, 1,
         'source-used-by-not-gate:S904'),
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
        ('section-mismatch', {'mutate': section_mismatch}, 1, 'no-capture-section-fit'),
        ('evidence-outside-capture', {'mutate': evidence_outside_capture}, 1,
         'no-resolvable-capture-line'),
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
