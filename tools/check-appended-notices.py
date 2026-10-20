#!/usr/bin/env python3
"""Read-only structural verifier for append-only round-18 correction notices.

This gate checks authenticated registry records against immutable Git blobs. It
proves the declared bytes, append boundary, notice section, and cited capture
line; it does not establish source truth or completeness of defect coverage.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import subprocess
import sys
sys.dont_write_bytecode = True
import tempfile
from collections import Counter, namedtuple
from pathlib import Path

from _revision import (E_GIT, RevisionError, bind, clean_env)

PASS, FAIL, CANNOT = 0, 1, 2
BASELINE = "842a5312b704b5cda10fd80ec1fdee5fb381ba97"
SCHEMA = "tsukuroi-appended-notices-v1"
DEFAULT_REGISTRY = "corpus/knowledge/freshness-recheck-r18.json"
ROOT = Path(__file__).resolve().parents[1]
RECORD_FIELDS = frozenset(("id", "path", "baseline_quote", "reason", "now",
                           "capture_ref", "capture_quote", "notice_heading"))
TOP_FIELDS = frozenset(("schema", "baseline", "records"))
ID_RE = re.compile(r"^(?:R18-CORR-[0-9]{2}|R18-FRESH-[A-Za-z0-9._-]+-[0-9]{2})$")
HEADING_RE = re.compile(r"^#{1,6} [^\r\n].*$")
ATX_RE = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*#*\s*$")
COMPONENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
CAPTURE_RE = re.compile(
    r"^\.ufo/waves/round-[1-9][0-9]*/l1-capture/[A-Za-z0-9][A-Za-z0-9._-]*$")

Finding = namedtuple("Finding", "id site detail")
Result = namedtuple("Result", "code findings resolved record_count distinct_paths", defaults=(0,))
Loaded = namedtuple("Loaded", "data issue")


class DuplicateJSONKey(ValueError):
    pass


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKey(f"duplicate key {key!r}")
        result[key] = value
    return result


def _finding(fid, site, detail):
    return Finding(fid, str(site), str(detail)[:240])


def _dedupe(findings):
    seen, result = set(), []
    for item in findings:
        key = (item.id, item.site, item.detail)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def _safe_components(path):
    if not isinstance(path, str) or not path or path.startswith("/") or "\\" in path:
        return False
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        return False
    if parts[0] == ".ufo":
        return len(parts) > 1 and all(COMPONENT_RE.fullmatch(part) for part in parts[1:])
    return all(COMPONENT_RE.fullmatch(part) for part in parts)


def safe_record_path(path):
    if path == "SKILL.md":
        return True
    prefix = "corpus/knowledge/"
    if not isinstance(path, str) or not path.startswith(prefix):
        return False
    name = path[len(prefix):]
    return ("/" not in name and name.endswith(".md")
            and COMPONENT_RE.fullmatch(name) is not None)


def safe_registry_path(path):
    return (_safe_components(path) and path.endswith(".json"))


def safe_capture_path(path):
    return _safe_components(path) and CAPTURE_RE.fullmatch(path) is not None


def distinct_path_count(records):
    return len({item["path"] for item in records
                if isinstance(item, dict) and isinstance(item.get("path"), str)})


def registry_scope(registry_path):
    name = registry_path.rsplit("/", 1)[-1]
    if name == "statement-corrections-r18.json":
        return "CORR", frozenset(("corpus/knowledge/boot-chain-r17.md",))
    if name == "freshness-recheck-r18.json":
        return "FRESH", None
    return None, None


def _git(root, *args):
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(root), *args],
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=clean_env(), timeout=60)
    except subprocess.TimeoutExpired as exc:
        raise RevisionError(E_GIT, "git", f"git {args[0]} exceeded 60s") from exc
    except OSError as exc:
        raise RevisionError(E_GIT, "git", str(exc)[:120]) from exc

def _git_detail(proc):
    return proc.stderr.decode("utf-8", "replace").strip()[:120] or f"exit={proc.returncode}"


class GitReader:
    """Read regular committed blobs only; never follow working-tree symlinks."""

    def __init__(self, root):
        self.root = Path(root)
        self.cache = {}

    def read(self, revision, path):
        key = (revision, path)
        if key in self.cache:
            return self.cache[key]
        listing = _git(self.root, "ls-tree", "-z", "--full-tree", revision, "--", path)
        if listing.returncode:
            raise RevisionError(E_GIT, path, "git ls-tree failed: " + _git_detail(listing))
        entries = []
        for item in listing.stdout.split(b"\0"):
            if not item:
                continue
            try:
                metadata, name = item.split(b"\t", 1)
                mode, kind, _oid = metadata.split(b" ", 2)
            except ValueError:
                raise RevisionError(E_GIT, path, "git ls-tree returned malformed entry")
            if name.decode("utf-8", "replace") == path:
                entries.append((mode, kind))
        if not entries:
            loaded = Loaded(None, "missing")
        elif len(entries) != 1 or entries[0][0] not in (b"100644", b"100755") or entries[0][1] != b"blob":
            loaded = Loaded(None, "unsafe")
        else:
            shown = _git(self.root, "show", f"{revision}:{path}")
            if shown.returncode:
                raise RevisionError(E_GIT, path, "git show failed: " + _git_detail(shown))
            loaded = Loaded(shown.stdout, None)
        self.cache[key] = loaded
        return loaded


class MemoryReader:
    """In-memory immutable snapshots used only by --selftest."""

    def __init__(self, values):
        self.values = dict(values)

    def read(self, revision, path):
        return self.values.get((revision, path), Loaded(None, "missing"))

    def set(self, revision, path, data=None, issue=None):
        self.values[(revision, path)] = Loaded(data, issue)


def _string_field(value):
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        value.encode("utf-8", "strict")
    except UnicodeEncodeError:
        return False
    return True


def _heading_positions(text, heading):
    return [index for index, line in enumerate(text.splitlines()) if line == heading]


def _heading_section(text, index, heading):
    lines = text.splitlines()
    match = ATX_RE.fullmatch(heading)
    level = len(match.group(1)) if match else 6
    end = len(lines)
    for pos in range(index + 1, len(lines)):
        found = ATX_RE.fullmatch(lines[pos])
        if found and len(found.group(1)) <= level:
            end = pos
            break
    return "\n".join(lines[index + 1:end])




def _record_findings(record, revision, baseline_revision, reader, compare):
    path = record["path"]
    rid = record["id"]
    findings = []
    base_loaded = reader.read(baseline_revision, path)
    target_loaded = reader.read(revision, path)
    if base_loaded.issue == "missing":
        findings.append(_finding("NOTICE-BASELINE-MISSING", path,
                                  "file absent at registry baseline"))
    elif base_loaded.issue == "unsafe":
        findings.append(_finding("NOTICE-PATH-UNSAFE", path,
                                  "baseline path is not a regular file"))
    if target_loaded.issue == "missing":
        findings.append(_finding("NOTICE-TARGET-MISSING", path,
                                  "file absent at target revision"))
    elif target_loaded.issue == "unsafe":
        findings.append(_finding("NOTICE-PATH-UNSAFE", path,
                                  "target path is not a regular file"))
    if base_loaded.data is None or target_loaded.data is None:
        return findings

    base_bytes, target_bytes = base_loaded.data, target_loaded.data
    if not target_bytes.startswith(base_bytes):
        findings.append(_finding("NOTICE-HISTORY", path,
                                  "target bytes do not start with baseline bytes"))
    quote = record["baseline_quote"].encode("utf-8")
    if quote not in base_bytes:
        findings.append(_finding("NOTICE-QUOTE-BASELINE", path,
                                  "baseline_quote is not an exact baseline substring"))
    quote_in_target = quote in target_bytes
    if not quote_in_target:
        findings.append(_finding("NOTICE-QUOTE-TARGET", path,
                                  "baseline_quote is absent from target bytes"))

    try:
        base_text = base_bytes.decode("utf-8", "strict")
        target_text = target_bytes.decode("utf-8", "strict")
    except UnicodeDecodeError:
        findings.append(_finding("NOTICE-TEXT-ENCODING", path,
                                  "baseline or target bytes are not valid UTF-8"))
        return findings

    heading = record["notice_heading"]
    if _heading_positions(base_text, heading):
        findings.append(_finding("NOTICE-HEADING-BASE", path,
                                  "notice_heading already occurs at baseline"))
    occurrences = _heading_positions(target_text, heading)
    if compare and not occurrences:
        if quote_in_target:
            findings.append(_finding("STALE-UNFLAGGED", path,
                                      f"{rid}: old quote is present and notice heading is absent"))
        return findings
    if not occurrences:
        findings.append(_finding("NOTICE-HEADING-MISSING", path,
                                  "notice heading absent at target revision"))
        return findings
    if len(occurrences) != 1:
        findings.append(_finding("NOTICE-HEADING-DUP", path,
                                  f"exact notice heading occurrences={len(occurrences)}"))
    if not target_bytes.startswith(base_bytes):
        # The history finding above already records why no suffix is trustworthy.
        return findings

    body = _heading_section(target_text, occurrences[0], heading)
    missing_content = [field for field, value in (("now", record["now"]),
                                                   ("capture_ref", record["capture_ref"]))
                       if value not in body]
    if missing_content:
        findings.append(_finding("NOTICE-CONTENT", path,
                                  "notice section lacks " + ",".join(missing_content)))

    ref = record["capture_ref"]
    capture_path, separator, line_text = ref.rpartition(":")
    positive_line = line_text.lstrip("0")
    if (not separator or not re.fullmatch(r"[0-9]+", line_text)
            or not positive_line or not safe_capture_path(capture_path)
            or capture_path == path):
        findings.append(_finding("NOTICE-CAPTURE-REF", path,
                                  "capture_ref must cite a safe round capture file and positive line"))
        return findings
    capture_loaded = reader.read(revision, capture_path)
    if capture_loaded.issue == "missing":
        findings.append(_finding("NOTICE-CAPTURE-MISSING", capture_path,
                                  "cited capture absent at target revision"))
        return findings
    if capture_loaded.issue == "unsafe":
        findings.append(_finding("NOTICE-CAPTURE-UNSAFE", capture_path,
                                  "cited capture is not a regular committed file"))
        return findings
    lines = capture_loaded.data.splitlines()
    maximum = str(len(lines))
    beyond_eof = (len(positive_line) > len(maximum)
                  or (len(positive_line) == len(maximum) and positive_line > maximum))
    if beyond_eof:
        findings.append(_finding("NOTICE-CAPTURE-LINE", capture_path,
                                  f"line {line_text} beyond EOF={len(lines)}"))
    else:
        line_number = int(positive_line)
        if record["capture_quote"].encode("utf-8") not in lines[line_number - 1]:
            findings.append(_finding("NOTICE-CAPTURE-QUOTE", capture_path,
                                      "capture_quote is not an exact substring of cited line"))
    return findings


def missing_registry(compare, path):
    if compare:
        return Result(CANNOT, [_finding("E-REGISTRY-MISSING", path,
                                        "registry absent at --registry-from")], 0, 0)
    return Result(FAIL, [_finding("NOTICE-MISSING", path,
                                  "registry absent at --revision")], 0, 0)


def evaluate(registry_bytes, revision, reader, compare=False, registry_path=DEFAULT_REGISTRY):
    if registry_bytes is None:
        return missing_registry(compare, registry_path)
    try:
        text = registry_bytes.decode("utf-8", "strict")
        doc = json.loads(text, object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError, DuplicateJSONKey, ValueError) as exc:
        return Result(CANNOT, [_finding("E-REGISTRY-PARSE", registry_path, str(exc))], 0, 0)

    records = doc.get("records") if isinstance(doc, dict) else None
    record_count = len(records) if isinstance(records, list) else 0
    distinct_paths = distinct_path_count(records) if isinstance(records, list) else 0
    if not isinstance(doc, dict) or set(doc) != TOP_FIELDS:
        return Result(FAIL, [_finding("NOTICE-SCHEMA", registry_path,
                                      "top-level object must have exactly schema, baseline, records")],
                      0, record_count, distinct_paths)
    if doc.get("schema") != SCHEMA or doc.get("baseline") != BASELINE:
        return Result(FAIL, [_finding("NOTICE-SCHEMA", registry_path,
                                      f"schema must be {SCHEMA} and baseline must be {BASELINE}")],
                      0, record_count, distinct_paths)
    if not isinstance(records, list):
        return Result(FAIL, [_finding("NOTICE-SCHEMA", registry_path,
                                      "records must be an array")], 0, 0, 0)
    if not records:
        return Result(FAIL, [_finding("NOTICE-EMPTY", registry_path,
                                      "records array must not be empty")], 0, 0, 0)

    candidates, structural = [], []
    for index, item in enumerate(records):
        site = f"{registry_path}:records[{index}]"
        if not isinstance(item, dict) or set(item) != RECORD_FIELDS:
            structural.append(_finding("NOTICE-FIELDS", site,
                                       "record must have exactly the eight declared keys"))
            continue
        if any(not _string_field(item.get(field)) for field in RECORD_FIELDS):
            structural.append(_finding("NOTICE-FIELDS", site,
                                       "all eight record values must be nonempty UTF-8 strings"))
            continue
        if not ID_RE.fullmatch(item["id"]):
            structural.append(_finding("NOTICE-ID", site,
                                       "id must be R18-CORR-NN or R18-FRESH-<seat>-NN"))
            continue
        candidates.append((index, item))

    families = {item["id"].split("-")[1] for _, item in candidates}
    required_family, allowed_paths = registry_scope(registry_path)
    family_problem = None
    if len(families) > 1:
        family_problem = "one registry cannot mix R18-CORR and R18-FRESH ids"
    elif required_family and families and families != {required_family}:
        family_problem = f"{registry_path.rsplit('/', 1)[-1]} requires R18-{required_family} ids"
    if family_problem:
        findings = list(structural)
        findings.append(_finding("NOTICE-ID-FAMILY", registry_path, family_problem))
        return Result(FAIL, _dedupe(findings), 0, record_count, distinct_paths)

    id_counts = Counter(item["id"] for _, item in candidates)
    quote_counts = Counter((item["path"], item["baseline_quote"])
                           for _, item in candidates)
    duplicate_ids = {rid for rid, count in id_counts.items() if count > 1}
    duplicate_quotes = {pair for pair, count in quote_counts.items() if count > 1}

    findings = list(structural)
    resolved = 0
    for index, record in candidates:
        site = f"{registry_path}:records[{index}]"
        if record["id"] in duplicate_ids:
            findings.append(_finding("NOTICE-ID-DUP", site,
                                     f"duplicate id {record['id']}"))
            continue
        if (record["path"], record["baseline_quote"]) in duplicate_quotes:
            findings.append(_finding("NOTICE-QUOTE-DUP", site,
                                     "path and baseline_quote pair is duplicated"))
            continue
        if not safe_record_path(record["path"]):
            findings.append(_finding("NOTICE-PATH", site,
                                     "path must be SKILL.md or corpus/knowledge/<name>.md"))
            continue
        if allowed_paths is not None and record["path"] not in allowed_paths:
            findings.append(_finding("NOTICE-PATH-SCOPE", site,
                                     "statement corrections may target only boot-chain-r17.md"))
            continue
        if not HEADING_RE.fullmatch(record["notice_heading"]):
            findings.append(_finding("NOTICE-HEADING-FORM", site,
                                     "notice_heading must be one Markdown ATX heading line"))
            continue
        per_record = _record_findings(record, revision, doc["baseline"], reader, compare)
        findings.extend(per_record)
        if not per_record:
            resolved += 1
    return Result(FAIL if findings else PASS, _dedupe(findings), resolved,
                  record_count, distinct_paths)


def emit(result, revision, branch, branch_tip):
    status = {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[result.code]
    payload = {"status": status, "revision": revision, "branch": branch,
               "branch_tip": branch_tip, "resolved_records": result.resolved,
               "record_count": result.record_count,
               "distinct_paths": result.distinct_paths,
               "findings": [{"id": item.id, "site": item.site, "detail": item.detail}
                            for item in result.findings]}
    print(json.dumps(payload, sort_keys=True))
    return result.code


def build_parser():
    parser = argparse.ArgumentParser(
        description="Read-only structural verifier for appended correction notices.",
        exit_on_error=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision", metavar="REV",
                       help="7-64 hex commit landed and pushed on the selected branch")
    group.add_argument("--selftest", action="store_true", help="hermetic fixture suite")
    parser.add_argument("--branch", default="master",
                        help="landed branch for revision binding (default master)")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY,
                        help="lane-relative registry JSON path")
    parser.add_argument("--registry-from", metavar="REV",
                        help="read registry from this bound revision and compare its claims")
    return parser


def cli_finding(argv):
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit):
        return "E-CLI"
    if args.selftest and args.registry_from:
        return "E-CLI"
    return None


def _emit_cannot(fid, site, detail, revision, branch, branch_tip):
    return emit(Result(CANNOT, [_finding(fid, site, detail)], 0, 0),
                revision, branch, branch_tip)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit) as exc:
        if isinstance(exc, SystemExit) and exc.code == 0:
            return 0
        return _emit_cannot("E-CLI", "cli", "--revision REV or --selftest required",
                            None, "master", None)
    if args.selftest:
        if args.registry_from:
            return _emit_cannot("E-CLI", "cli", "--registry-from is not valid with --selftest",
                                None, args.branch, None)
        return selftest()

    binding = None
    try:
        # _revision.bind performs branch validation before revision validation.
        binding = bind(ROOT, args.revision, args.branch)
        registry_binding = (bind(ROOT, args.registry_from, args.branch)
                            if args.registry_from is not None else binding)
        if not safe_registry_path(args.registry):
            return _emit_cannot("E-REGISTRY-PATH", "registry",
                                "registry must be a safe lane-relative .json path",
                                binding.sha, binding.branch, binding.branch_tip)
        reader = GitReader(ROOT)
        registry_loaded = reader.read(registry_binding.sha, args.registry)
        if registry_loaded.issue == "missing":
            result = missing_registry(args.registry_from is not None, args.registry)
            return emit(result, binding.sha, binding.branch, binding.branch_tip)
        if registry_loaded.issue == "unsafe":
            fid = "E-REGISTRY-UNSAFE" if args.registry_from is not None else "NOTICE-REGISTRY-UNSAFE"
            code = CANNOT if args.registry_from is not None else FAIL
            return emit(Result(code, [_finding(fid, args.registry,
                                               "registry is not a regular committed file")], 0, 0),
                        binding.sha, binding.branch, binding.branch_tip)
        result = evaluate(registry_loaded.data, binding.sha, reader,
                          args.registry_from is not None, args.registry)
        return emit(result, binding.sha, binding.branch, binding.branch_tip)
    except RevisionError as exc:
        return _emit_cannot(exc.fid, exc.site, exc.detail,
                            binding.sha if binding else None,
                            args.branch, binding.branch_tip if binding else None)


# ---- Hermetic selftests ---------------------------------------------------


def _fixture_data():
    target_rev = "a" * 40
    path1, path2 = "SKILL.md", "corpus/knowledge/sample.md"
    cap1 = ".ufo/waves/round-18/l1-capture/host-capture-r18.txt"
    cap2 = ".ufo/waves/round-18/l1-capture/knowledge-capture.txt"
    base1 = b"# Skill\n\nCurrent-use statement: package version 41.1 is installed.\n"
    base2 = b"# Sample\n\nThe current release is 6.8.\n"
    quote1 = "Current-use statement: package version 41.1 is installed."
    quote2 = "The current release is 6.8."
    heading1 = "## R18-FRESHNESS — current package observation"
    heading2 = "## R18-FRESHNESS — current release observation"
    ref1, ref2 = f"{cap1}:2", f"{cap2}:3"
    notice1 = (f"\n{heading1}\n\nThe old statement is historical; now: package version 42.2.\n"
               f"Capture {ref1} records the current observation.\n"
               "Historical snapshots are preserved; this supersedes current-use only.\n"
               "Read-only scope; no package or reboot clearance.\n")
    notice2 = (f"\n{heading2}\n\nNow: the current release is 7.2.11.\n"
               f"Capture {ref2} records the current observation.\n"
               "Historical snapshots are preserved; this supersedes current-use only.\n"
               "Read-only scope; no package or reboot clearance.\n")
    records = [
        {"id": "R18-FRESH-BuildNoticeGate-01", "path": path1, "baseline_quote": quote1,
         "reason": "the current-use statement requires a correction",
         "now": "package version 42.2", "capture_ref": ref1,
         "capture_quote": "package version: 42.2", "notice_heading": heading1},
        {"id": "R18-FRESH-BuildNoticeGate-02", "path": path2, "baseline_quote": quote2,
         "reason": "the current release observation is stale",
         "now": "the current release is 7.2.11", "capture_ref": ref2,
         "capture_quote": "current release 7.2.11", "notice_heading": heading2},
    ]
    doc = {"schema": SCHEMA, "baseline": BASELINE, "records": records}
    values = {
        (BASELINE, path1): Loaded(base1, None),
        (BASELINE, path2): Loaded(base2, None),
        (target_rev, path1): Loaded(base1 + notice1.encode(), None),
        (target_rev, path2): Loaded(base2 + notice2.encode(), None),
        (target_rev, cap1): Loaded(b"header\npackage version: 42.2\n", None),
        (target_rev, cap2): Loaded(b"header\nline two\ncurrent release 7.2.11\n", None),
    }
    return {"target_rev": target_rev, "path1": path1, "path2": path2,
            "cap1": cap1, "cap2": cap2,
            "base1": base1, "base2": base2, "quote1": quote1, "quote2": quote2,
            "heading1": heading1, "heading2": heading2, "notice1": notice1,
            "notice2": notice2, "ref1": ref1, "ref2": ref2, "doc": doc,
            "values": values}


def _json_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")


def _clone_doc(doc):
    return json.loads(json.dumps(doc))


def _binding_selftest():
    passed = []
    with tempfile.TemporaryDirectory(prefix="check-appended-notices-") as temp:
        repo = Path(temp) / "repo"
        repo.mkdir()

        def run(*args):
            proc = subprocess.run(["git", "-C", str(repo), *args],
                                  stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, env=clean_env(), timeout=60)
            if proc.returncode:
                raise RuntimeError(proc.stderr.decode("utf-8", "replace")[:200])
            return proc.stdout.decode("ascii", "replace").strip()

        run("init", "--quiet", "--initial-branch=master")
        run("config", "user.name", "Selftest")
        run("config", "user.email", "selftest@example.invalid")

        (repo / "SKILL.md").write_bytes(b"reader fixture\n")
        capture_rel = ".ufo/waves/round-18/l1-capture/sample.txt"
        capture_file = repo / capture_rel
        capture_file.parent.mkdir(parents=True)
        capture_file.write_bytes(b"capture header\ncapture data\n")
        symlink = repo / "corpus/knowledge/escape.md"
        symlink.parent.mkdir(parents=True)
        symlink.symlink_to("../../../../outside")
        run("add", "SKILL.md", capture_rel, "corpus/knowledge/escape.md")
        run("commit", "--allow-empty", "--quiet", "-m", "base")
        tip = run("rev-parse", "HEAD")
        tree = run("rev-parse", "HEAD^{tree}")
        run("update-ref", "refs/remotes/origin/master", tip)
        blob_reader = GitReader(repo)
        passed.append(("gitreader-regular-root",
                       blob_reader.read(tip, "SKILL.md") == Loaded(b"reader fixture\n", None)))
        passed.append(("gitreader-regular-nested",
                       blob_reader.read(tip, capture_rel)
                       == Loaded(b"capture header\ncapture data\n", None)))
        passed.append(("gitreader-symlink", blob_reader.read(
            tip, "corpus/knowledge/escape.md") == Loaded(None, "unsafe")))
        passed.append(("gitreader-missing", blob_reader.read(
            tip, "corpus/knowledge/missing.md") == Loaded(None, "missing")))
        try:
            bound = bind(repo, tip, "master")
            passed.append(("binding-clean", bound.sha == tip))
        except RevisionError as exc:
            passed.append(("binding-clean", f"unexpected {exc.fid}"))

        checks = [
            ("branch-before-revision", "HEAD", "bad//branch", "E-BRANCH-INVALID"),
            ("revision-invalid", "HEAD", "master", "E-REVISION-INVALID"),
            ("branch-missing", tip, "missing", "E-BRANCH-MISSING"),
        ]
        for name, revision, branch, expected in checks:
            try:
                bind(repo, revision, branch)
                got = None
            except RevisionError as exc:
                got = exc.fid
            passed.append((name, got == expected if got == expected else f"{got}/{expected}"))

        orphan = run("commit-tree", tree, "-m", "unlanded")
        try:
            bind(repo, orphan, "master")
            got = None
        except RevisionError as exc:
            got = exc.fid
        passed.append(("revision-not-landed", got == "E-REVISION-NOT-LANDED"
                       if got == "E-REVISION-NOT-LANDED" else got))

        run("commit", "--allow-empty", "--quiet", "-m", "local only")
        local_only = run("rev-parse", "HEAD")
        try:
            bind(repo, local_only, "master")
            got = None
        except RevisionError as exc:
            got = exc.fid
        passed.append(("revision-not-pushed", got == "E-REVISION-NOT-PUSHED"
                       if got == "E-REVISION-NOT-PUSHED" else got))

        try:
            bind(Path(temp) / "missing", tip, "master")
            got = None
        except RevisionError as exc:
            got = exc.fid
        passed.append(("git-failed", got == "E-GIT-FAILED" if got == "E-GIT-FAILED" else got))
    return passed


def selftest():
    data = _fixture_data()
    target_rev = data["target_rev"]
    default_registry = _json_bytes(data["doc"])

    def reader():
        return MemoryReader(data["values"])

    def mutate_record(index, **changes):
        doc = _clone_doc(data["doc"])
        doc["records"][index].update(changes)
        return doc

    cases = []
    cases.append(("clean-two-records", default_registry, reader(), False,
                  PASS, set(), 2, 2))
    cases.append(("registry-missing-at-revision", None, reader(), False,
                  FAIL, {"NOTICE-MISSING"}, 0, 0))
    cases.append(("registry-missing-from", None, reader(), True,
                  CANNOT, {"E-REGISTRY-MISSING"}, 0, 0))
    wrong_schema = _clone_doc(data["doc"])
    wrong_schema["schema"] = "wrong"
    cases.append(("malformed-schema", _json_bytes(wrong_schema), reader(), False,
                  FAIL, {"NOTICE-SCHEMA"}, 0, 2))
    extra_top = _clone_doc(data["doc"])
    extra_top["extra"] = "not allowed"
    cases.append(("malformed-top-keys", _json_bytes(extra_top), reader(), False,
                  FAIL, {"NOTICE-SCHEMA"}, 0, 2))
    missing_key = _clone_doc(data["doc"])
    del missing_key["records"][0]["reason"]
    cases.append(("malformed-record-keys", _json_bytes(missing_key), reader(), False,
                  FAIL, {"NOTICE-FIELDS"}, 1, 2))
    extra_key = mutate_record(0, unrecognized="x")
    cases.append(("malformed-record-extra-key", _json_bytes(extra_key), reader(), False,
                  FAIL, {"NOTICE-FIELDS"}, 1, 2))
    bad_id = mutate_record(0, id="R18-FRESH-BuildNoticeGate-1")
    cases.append(("malformed-id", _json_bytes(bad_id), reader(), False,
                  FAIL, {"NOTICE-ID"}, 1, 2))
    duplicate_id = _clone_doc(data["doc"])
    duplicate_id["records"][1]["id"] = duplicate_id["records"][0]["id"]
    cases.append(("duplicate-id", _json_bytes(duplicate_id), reader(), False,
                  FAIL, {"NOTICE-ID-DUP"}, 0, 2))
    mixed_ids = _clone_doc(data["doc"])
    mixed_ids["records"][0]["id"] = "R18-CORR-01"
    cases.append(("mixed-record-prefixes", _json_bytes(mixed_ids), reader(), False,
                  FAIL, {"NOTICE-ID-FAMILY"}, 0, 2))
    duplicate_quote = _clone_doc(data["doc"])
    duplicate_quote["records"][1]["path"] = data["path1"]
    duplicate_quote["records"][1]["baseline_quote"] = data["quote1"]
    cases.append(("duplicate-path-quote", _json_bytes(duplicate_quote), reader(), False,
                  FAIL, {"NOTICE-QUOTE-DUP"}, 0, 2))
    bad_quote = mutate_record(0, baseline_quote="quote not present anywhere")
    cases.append(("quote-mismatch", _json_bytes(bad_quote), reader(), False,
                  FAIL, {"NOTICE-QUOTE-BASELINE", "NOTICE-QUOTE-TARGET"}, 1, 2))
    bad_capture_zero = mutate_record(0, capture_ref=f"{data['cap1']}:0")
    zero_reader = reader()
    zero_target = data["base1"] + data["notice1"].replace(
        data["ref1"], f"{data['cap1']}:0").encode()
    zero_reader.set(target_rev, data["path1"], zero_target)
    cases.append(("capture-zero", _json_bytes(bad_capture_zero), zero_reader, False,
                  FAIL, {"NOTICE-CAPTURE-REF"}, 1, 2))
    eof_ref = f"{data['cap1']}:999999"
    eof_doc = mutate_record(0, capture_ref=eof_ref)
    eof_reader = reader()
    eof_reader.set(target_rev, data["path1"],
                   data["base1"] + data["notice1"].replace(data["ref1"], eof_ref).encode())
    cases.append(("capture-line-beyond-eof", _json_bytes(eof_doc), eof_reader, False,
                  FAIL, {"NOTICE-CAPTURE-LINE"}, 1, 2))
    traversal = mutate_record(0, path="corpus/knowledge/../../outside.md")
    cases.append(("path-traversal", _json_bytes(traversal), reader(), False,
                  FAIL, {"NOTICE-PATH"}, 1, 2))
    symlink_reader = reader()
    symlink_reader.set(BASELINE, data["path1"], issue="unsafe")
    cases.append(("symlink-baseline-refused", default_registry, symlink_reader, False,
                  FAIL, {"NOTICE-PATH-UNSAFE"}, 1, 2))
    capture_traversal = mutate_record(0, capture_ref="../private.txt:1")
    cases.append(("capture-path-traversal", _json_bytes(capture_traversal), reader(), False,
                  FAIL, {"NOTICE-CONTENT", "NOTICE-CAPTURE-REF"}, 1, 2))
    self_ref = f"{data['path1']}:1"
    self_capture = mutate_record(0, capture_ref=self_ref)
    self_capture_reader = reader()
    self_capture_reader.set(target_rev, data["path1"],
                            data["base1"] + data["notice1"].replace(
                                data["ref1"], self_ref).encode())
    cases.append(("self-capture-rejected", _json_bytes(self_capture),
                  self_capture_reader, False, FAIL, {"NOTICE-CAPTURE-REF"}, 1, 2))
    corpus_ref = f"corpus/knowledge/sample.md:1"
    corpus_capture = mutate_record(0, capture_ref=corpus_ref)
    corpus_reader = reader()
    corpus_reader.set(target_rev, data["path1"],
                      data["base1"] + data["notice1"].replace(
                          data["ref1"], corpus_ref).encode())
    cases.append(("corpus-capture-rejected", _json_bytes(corpus_capture),
                  corpus_reader, False, FAIL, {"NOTICE-CAPTURE-REF"}, 1, 2))
    shared_doc = _clone_doc(data["doc"])
    shared_heading = "## R18-FRESHNESS — grouped current observations"
    shared_doc["records"][0]["notice_heading"] = shared_heading
    shared_doc["records"][1]["path"] = data["path1"]
    shared_doc["records"][1]["notice_heading"] = shared_heading
    shared_base = data["base1"] + f"\n{data['quote2']}\n".encode()
    shared_notice = (f"\n{shared_heading}\n\n"
                     f"Now: {shared_doc['records'][0]['now']}; capture {data['ref1']}.\n"
                     f"Now: {shared_doc['records'][1]['now']}; capture {data['ref2']}.\n"
                     "Historical snapshots are preserved; current-use only is superseded.\n"
                     "Read-only scope; no package or reboot clearance.\n")
    shared_reader = reader()
    shared_reader.set(BASELINE, data["path1"], shared_base)
    shared_reader.set(target_rev, data["path1"], shared_base + shared_notice.encode())
    cases.append(("shared-heading-one-section", _json_bytes(shared_doc), shared_reader, False,
                  PASS, set(), 2, 2))

    cross_file_doc = _clone_doc(data["doc"])
    cross_file_doc["records"][1]["notice_heading"] = data["heading1"]
    cross_file_reader = reader()
    cross_notice2 = data["notice2"].replace(data["heading2"], data["heading1"])
    cross_file_reader.set(target_rev, data["path2"],
                          data["base2"] + cross_notice2.encode())
    cases.append(("shared-heading-cross-file", _json_bytes(cross_file_doc),
                  cross_file_reader, False, PASS, set(), 2, 2))

    heading_reader = reader()
    heading_reader.set(target_rev, data["path1"],
                       data["base1"] + data["notice1"].encode() + data["notice1"].encode())
    cases.append(("heading-duplicate-in-target", default_registry, heading_reader, False,
                  FAIL, {"NOTICE-HEADING-DUP"}, 1, 2))
    removed_reader = reader()
    removed_reader.set(target_rev, data["path1"], data["base1"])
    cases.append(("notice-removed", default_registry, removed_reader, False,
                  FAIL, {"NOTICE-HEADING-MISSING"}, 1, 2))
    nonappend_reader = reader()
    rewritten = data["base1"].replace(b"Current-use statement", b"Rewritten statement")
    nonappend_reader.set(target_rev, data["path1"], rewritten + data["notice1"].encode())
    cases.append(("nonappend-history", default_registry, nonappend_reader, False,
                  FAIL, {"NOTICE-HISTORY", "NOTICE-QUOTE-TARGET"}, 1, 2))
    compare_reader = reader()
    compare_reader.set(BASELINE, data["path1"], data["base1"])
    compare_reader.set(target_rev, data["path1"], data["base1"])
    compare_reader.set(target_rev, data["path2"], data["base2"])
    compare_reader.set(BASELINE, data["path2"], data["base2"])
    cases.append(("compare-real-stale", default_registry, compare_reader, True,
                  FAIL, {"STALE-UNFLAGGED"}, 0, 2))
    no_capture_reader = reader()
    no_capture_reader.set(target_rev, data["cap1"], issue="missing")
    cases.append(("capture-missing", default_registry, no_capture_reader, False,
                  FAIL, {"NOTICE-CAPTURE-MISSING"}, 1, 2))
    bad_capture_quote = mutate_record(0, capture_quote="no such captured value")
    cases.append(("capture-quote", _json_bytes(bad_capture_quote), reader(), False,
                  FAIL, {"NOTICE-CAPTURE-QUOTE"}, 1, 2))
    duplicate_json = b'{"schema":"x","schema":"y"}'
    cases.append(("duplicate-json-key", duplicate_json, reader(), False,
                  CANNOT, {"E-REGISTRY-PARSE"}, 0, 0))
    wrong_baseline = _clone_doc(data["doc"])
    wrong_baseline["baseline"] = "0" * 40
    cases.append(("baseline-identity", _json_bytes(wrong_baseline), reader(), False,
                  FAIL, {"NOTICE-SCHEMA"}, 0, 2))

    failures, passed, total = [], 0, 0
    for name, raw, source, compare, want_code, want_ids, want_resolved, want_count in cases:
        total += 1
        got = evaluate(raw, target_rev, source, compare)
        got_ids = {item.id for item in got.findings}
        problems = []
        if got.code != want_code:
            problems.append(f"exit={got.code}/{want_code}")
        if got_ids != want_ids:
            problems.append("ids=" + ",".join(sorted(got_ids))
                            + " want=" + ",".join(sorted(want_ids)))
        if got.resolved != want_resolved:
            problems.append(f"resolved={got.resolved}/{want_resolved}")
        if got.record_count != want_count:
            problems.append(f"record_count={got.record_count}/{want_count}")
        if name == "clean-two-records" and got.distinct_paths != 2:
            problems.append(f"distinct_paths={got.distinct_paths}/2")
        if name == "duplicate-path-quote" and got.distinct_paths != 1:
            problems.append(f"distinct_paths={got.distinct_paths}/1")
        if name == "shared-heading-one-section" and got.distinct_paths != 1:
            problems.append(f"distinct_paths={got.distinct_paths}/1")
        if name == "shared-heading-cross-file" and got.distinct_paths != 2:
            problems.append(f"distinct_paths={got.distinct_paths}/2")
        if problems:
            failures.append(name + ": " + "; ".join(problems))
        else:
            passed += 1

    corrections_path = "corpus/knowledge/boot-chain-r17.md"
    corrections_registry = "corpus/knowledge/statement-corrections-r18.json"
    correction_doc = _clone_doc(data["doc"])
    correction_record = correction_doc["records"][0]
    correction_record["id"] = "R18-CORR-01"
    correction_record["path"] = corrections_path
    correction_record["notice_heading"] = "## R18-CORRECTION — boot-chain statement count"
    correction_notice = data["notice1"].replace(data["heading1"],
                                                 correction_record["notice_heading"])
    correction_reader = reader()
    correction_reader.set(BASELINE, corrections_path, data["base1"])
    correction_reader.set(target_rev, corrections_path,
                          data["base1"] + correction_notice.encode())
    correction_doc["records"] = [correction_record]
    total += 1
    got = evaluate(_json_bytes(correction_doc), target_rev, correction_reader,
                   registry_path=corrections_registry)
    if (got.code, {item.id for item in got.findings}, got.resolved,
            got.record_count, got.distinct_paths) == (PASS, set(), 1, 1, 1):
        passed += 1
    else:
        failures.append("correction-registry-scope: "
                        f"{got.code}/{got.findings}/{got.resolved}/"
                        f"{got.record_count}/{got.distinct_paths}")

    correction_bad_path = _clone_doc(correction_doc)
    correction_bad_path["records"][0]["path"] = data["path1"]
    total += 1
    got = evaluate(_json_bytes(correction_bad_path), target_rev, reader(),
                   registry_path=corrections_registry)
    got_ids = {item.id for item in got.findings}
    if (got.code, got_ids, got.resolved, got.distinct_paths) == (
            FAIL, {"NOTICE-PATH-SCOPE"}, 0, 1):
        passed += 1
    else:
        failures.append("correction-path-scope: "
                        f"{got.code}/{got_ids}/{got.resolved}/{got.distinct_paths}")

    cli_cases = [
        ("cli-none", [], "E-CLI"),
        ("cli-selftest-with-compare", ["--selftest", "--registry-from", "a" * 40], "E-CLI"),
        ("cli-normal", ["--revision", "a" * 40], None),
    ]
    for name, argv, expected in cli_cases:
        total += 1
        got = cli_finding(argv)
        if got == expected:
            passed += 1
        else:
            failures.append(f"{name}: {got}/{expected}")

    missing_path = "corpus/knowledge/check-appended-notices-selftest-missing-842a.json"
    main_cases = [
        ("missing-at-resolved-revision",
         ["--revision", BASELINE, "--registry", missing_path], FAIL, "NOTICE-MISSING"),
        ("missing-registry-from",
         ["--revision", BASELINE, "--registry", missing_path,
          "--registry-from", BASELINE], CANNOT, "E-REGISTRY-MISSING"),
    ]
    for name, argv, expected_code, expected_id in main_cases:
        total += 1
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(argv)
        try:
            payload = json.loads(output.getvalue())
            ids = [item.get("id") for item in payload.get("findings", [])]
            good = (code == expected_code and ids == [expected_id]
                    and payload.get("revision") == BASELINE
                    and payload.get("branch_tip") is not None
                    and payload.get("record_count") == 0)
        except (json.JSONDecodeError, AttributeError, TypeError):
            good = False
        if good:
            passed += 1
        else:
            failures.append(f"{name}: exit={code}, output={output.getvalue()[:200]}")

    for name, ok in _binding_selftest():
        total += 1
        if ok is True:
            passed += 1
        else:
            failures.append(f"{name}: {ok}")

    if failures:
        print(f"CHECK_APPENDED_NOTICES_SELFTEST: FAIL ({total} cases, {passed} passed)")
        print("\n".join("  " + item for item in failures))
        return FAIL
    print(f"CHECK_APPENDED_NOTICES_SELFTEST: PASS ({total} cases, {passed} passed, 0 failed)")
    return PASS


if __name__ == "__main__":
    sys.exit(main())
