#!/usr/bin/env python3
"""Read-only verifier for round-19 /boot/limine.conf writer attribution.

The registry and its capture/SOURCES evidence are read from --registry-from
(or --revision); the cited knowledge entry is always read from --revision.
Only committed Git blobs are read. No host state is consulted or modified.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter, namedtuple
from pathlib import Path

sys.dont_write_bytecode = True
from _revision import RevisionError, bind, clean_env

PASS, FAIL, CANNOT = 0, 1, 2
SCHEMA = "tsukuroi-boot-writers-r19-v1"
DEFAULT_REGISTRY = "corpus/knowledge/boot-writers-r19.json"
SOURCES_PATH = "corpus/SOURCES.md"
ROOT = Path(__file__).resolve().parents[1]
TOP_FIELDS = frozenset(("schema", "knowledge_entry", "captures",
                        "event_sources", "writers", "events"))
CAPTURE_FIELDS = frozenset(("path", "sha256"))
EVENT_SOURCE_FIELDS = frozenset(("capture", "probe", "pattern"))
WRITER_FIELDS = frozenset(("id", "name", "trigger", "mechanism_refs",
                           "signature", "writes", "sources"))
MECHANISM_FIELDS = frozenset(("capture", "line", "quote"))
SIGNATURE_FIELDS = frozenset(("kind", "value"))
EVENT_FIELDS = frozenset(("id", "capture", "line", "quote", "writer"))
WRITER_ID = re.compile(r"^W-[A-Za-z0-9][A-Za-z0-9_-]*$")
EVENT_ID = re.compile(r"^EV-[0-9]{2}$")
SOURCE_ID = re.compile(r"^S[0-9]{3}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9._-]+$")
SIGNATURE_KINDS = frozenset(("journal-unit", "journal-unit-regex",
                             "alpm-scriptlet"))

Finding = namedtuple("Finding", "id site detail")
Result = namedtuple("Result", "code findings counts")
Loaded = namedtuple("Loaded", "data issue")


class DuplicateJSONKey(ValueError):
    pass


class GitReadError(Exception):
    pass


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKey(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _finding(fid, site, detail):
    return Finding(str(fid), str(site), str(detail)[:240])


def _dedupe(findings):
    seen, result = set(), []
    for item in findings:
        key = (item.id, item.site, item.detail)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return sorted(result, key=lambda item: (item.id, item.site, item.detail))


def _safe_path(value, suffix=None):
    if (not isinstance(value, str) or not value or value.startswith("/")
            or "\\" in value or "\x00" in value):
        return False
    parts = value.split("/")
    if any(part in ("", ".", "..") or not SAFE_COMPONENT.fullmatch(part)
           for part in parts):
        return False
    return suffix is None or value.endswith(suffix)


def _git(root, *args):
    try:
        proc = subprocess.run(["git", "--no-pager", "-C", str(root), *args],
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=clean_env(), timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GitReadError(str(exc)[:180]) from exc
    return proc


class GitReader:
    """Read regular committed blobs only; never read the working tree."""

    def __init__(self, root):
        self.root = Path(root)
        self.cache = {}

    def read(self, revision, path):
        key = (revision, path)
        if key in self.cache:
            return self.cache[key]
        if not _safe_path(path):
            loaded = Loaded(None, "unsafe")
            self.cache[key] = loaded
            return loaded
        listed = _git(self.root, "ls-tree", "-z", revision, "--", path)
        if listed.returncode:
            raise GitReadError(listed.stderr.decode("utf-8", "replace")[:180]
                               or f"ls-tree exit={listed.returncode}")
        entries = [entry for entry in listed.stdout.split(b"\0") if entry]
        if not entries:
            loaded = Loaded(None, "missing")
            self.cache[key] = loaded
            return loaded
        if len(entries) != 1 or b"\t" not in entries[0]:
            loaded = Loaded(None, "unsafe")
            self.cache[key] = loaded
            return loaded
        metadata, name = entries[0].split(b"\t", 1)
        fields = metadata.split()
        if (name != path.encode("utf-8") or len(fields) != 3
                or fields[0] not in (b"100644", b"100755")
                or fields[1] != b"blob"):
            loaded = Loaded(None, "unsafe")
            self.cache[key] = loaded
            return loaded
        blob = _git(self.root, "cat-file", "blob", fields[2].decode("ascii"))
        if blob.returncode:
            raise GitReadError(blob.stderr.decode("utf-8", "replace")[:180]
                               or f"cat-file exit={blob.returncode}")
        loaded = Loaded(blob.stdout, None)
        self.cache[key] = loaded
        return loaded


def _empty_counts():
    return {"events_total": 0, "attributed_events": 0, "writer_classes": 0,
            "writers_with_events": 0, "unattributed": 0}


def _result(code, findings, counts=None):
    return Result(code, _dedupe(findings), _empty_counts() if counts is None else counts)


def _as_text(data):
    return data.decode("utf-8", "strict")


def _row_shape(item, expected, site, findings, label):
    if not isinstance(item, dict) or set(item) != expected:
        findings.append(_finding("REGISTRY-SCHEMA", site,
                                 f"{label} must have exactly {', '.join(sorted(expected))}"))
        return False
    return True


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _source_statuses(text):
    statuses = {}
    for line in text.splitlines():
        match = re.match(r"^\|\s*(S[0-9]{3})\s*\|", line)
        if not match:
            continue
        cells = line.split("|")
        if len(cells) > 8:
            statuses[match.group(1)] = cells[8].strip()
    return statuses


def _signature_matches(signature, line):
    kind, value = signature["kind"], signature["value"]
    if kind == "journal-unit":
        return value in line
    if kind == "journal-unit-regex":
        return re.search(value, line) is not None
    if kind == "alpm-scriptlet":
        return "[ALPM-SCRIPTLET]" in line
    return False


def evaluate(registry_bytes, registry_revision, target_revision, reader,
             registry_path=DEFAULT_REGISTRY):
    findings = []
    counts = _empty_counts()
    try:
        doc = json.loads(_as_text(registry_bytes), object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError, DuplicateJSONKey, ValueError) as exc:
        return _result(CANNOT, [_finding("E-REGISTRY-PARSE", registry_path, str(exc))])

    if not isinstance(doc, dict) or set(doc) != TOP_FIELDS:
        return _result(FAIL, [_finding("REGISTRY-SCHEMA", registry_path,
                                       "top-level object must have exactly schema, knowledge_entry, captures, event_sources, writers, events")])
    if doc.get("schema") != SCHEMA:
        return _result(FAIL, [_finding("REGISTRY-SCHEMA", registry_path,
                                       f"schema must be {SCHEMA}")])
    if not _safe_path(doc.get("knowledge_entry"), ".md"):
        findings.append(_finding("REGISTRY-SCHEMA", f"{registry_path}:knowledge_entry",
                                 "must be a safe lane-relative Markdown path"))
    for field in ("captures", "event_sources", "writers", "events"):
        if not isinstance(doc.get(field), list):
            findings.append(_finding("REGISTRY-SCHEMA", f"{registry_path}:{field}",
                                     "must be an array"))
        elif not doc[field]:
            findings.append(_finding("REGISTRY-SCHEMA", f"{registry_path}:{field}",
                                     "must not be empty"))
    if findings:
        return _result(FAIL, findings)

    captures = {}
    for index, item in enumerate(doc["captures"]):
        site = f"{registry_path}:captures[{index}]"
        if not _row_shape(item, CAPTURE_FIELDS, site, findings, "capture"):
            continue
        path, digest = item.get("path"), item.get("sha256")
        if not _safe_path(path) or not isinstance(digest, str) or not SHA256.fullmatch(digest):
            findings.append(_finding("REGISTRY-SCHEMA", site,
                                     "path must be safe and sha256 must be 64 lowercase hex digits"))
            continue
        if path in captures:
            findings.append(_finding("REGISTRY-SCHEMA", site,
                                     f"duplicate capture path {path}"))
            continue
        captures[path] = digest

    # Integrity is checked before interpreting any capture contents.
    for path, expected in sorted(captures.items()):
        try:
            loaded = reader.read(registry_revision, path)
        except GitReadError as exc:
            return _result(CANNOT, [_finding("CAPTURE-READ-FAILED", path, str(exc))])
        if loaded.issue:
            return _result(CANNOT, [_finding("CAPTURE-MISSING" if loaded.issue == "missing"
                                             else "CAPTURE-UNSAFE", path,
                                             "capture is absent or is not a regular committed file")])
        actual = hashlib.sha256(loaded.data).hexdigest()
        if actual != expected:
            return _result(CANNOT, [_finding("CAPTURE-TAMPERED", path,
                                             f"sha256 expected {expected}, observed {actual}")])

    capture_lines = {}
    for path in captures:
        try:
            capture_lines[path] = _as_text(reader.read(registry_revision, path).data).splitlines()
        except UnicodeDecodeError as exc:
            return _result(CANNOT, [_finding("CAPTURE-ENCODING", path,
                                             f"capture is not UTF-8 at byte {exc.start}")])

    source_rows = {}
    try:
        sources_loaded = reader.read(registry_revision, SOURCES_PATH)
    except GitReadError as exc:
        sources_loaded = Loaded(None, "error")
        findings.append(_finding("SOURCES-READ-FAILED", SOURCES_PATH, str(exc)))
    if sources_loaded.issue:
        findings.append(_finding("SOURCES-UNAVAILABLE", SOURCES_PATH,
                                 "committed SOURCES.md is absent or not a regular file"))
    else:
        try:
            source_rows = _source_statuses(_as_text(sources_loaded.data))
        except UnicodeDecodeError as exc:
            findings.append(_finding("SOURCES-ENCODING", SOURCES_PATH,
                                     f"SOURCES.md is not UTF-8 at byte {exc.start}"))

    try:
        knowledge_loaded = reader.read(target_revision, doc["knowledge_entry"])
    except GitReadError as exc:
        knowledge_loaded = Loaded(None, "error")
        findings.append(_finding("KNOWLEDGE-READ-FAILED", doc["knowledge_entry"], str(exc)))
    knowledge_text = ""
    if knowledge_loaded.data is not None:
        try:
            knowledge_text = _as_text(knowledge_loaded.data)
        except UnicodeDecodeError as exc:
            findings.append(_finding("KNOWLEDGE-ENCODING", doc["knowledge_entry"],
                                     f"knowledge entry is not UTF-8 at byte {exc.start}"))

    writers = {}
    writer_ok = {}
    writer_published = {}
    for index, item in enumerate(doc["writers"]):
        site = f"{registry_path}:writers[{index}]"
        if not _row_shape(item, WRITER_FIELDS, site, findings, "writer"):
            continue
        wid = item.get("id")
        if not isinstance(wid, str) or not WRITER_ID.fullmatch(wid):
            findings.append(_finding("REGISTRY-SCHEMA", site, "writer id must match W-<id>"))
            continue
        if wid in writers:
            findings.append(_finding("WRITER-ID-DUPLICATE", site, f"duplicate writer id {wid}"))
            continue
        if (not _nonempty(item.get("name")) or not _nonempty(item.get("trigger"))
                or not isinstance(item.get("mechanism_refs"), list)
                or not isinstance(item.get("writes"), list)
                or not isinstance(item.get("sources"), list)):
            findings.append(_finding("REGISTRY-SCHEMA", site,
                                     "writer name/trigger and mechanism_refs/writes/sources have invalid types"))
            continue
        sig = item.get("signature")
        if not _row_shape(sig, SIGNATURE_FIELDS, f"{site}:signature", findings, "signature"):
            continue
        if (not isinstance(sig.get("kind"), str) or sig.get("kind") not in SIGNATURE_KINDS
                or not _nonempty(sig.get("value"))):
            findings.append(_finding("REGISTRY-SCHEMA", f"{site}:signature",
                                     "signature kind/value is invalid"))
            continue
        if sig["kind"] == "journal-unit-regex":
            try:
                re.compile(sig["value"])
            except re.error as exc:
                findings.append(_finding("REGISTRY-SCHEMA", f"{site}:signature",
                                         f"invalid journal-unit-regex: {exc}"))
                continue
        writers[wid] = item
        published = wid in knowledge_text
        writer_published[wid] = published
        valid = True
        if not published:
            findings.append(_finding("WRITER-UNPUBLISHED", wid,
                                     f"{wid} is absent from {doc['knowledge_entry']} at --revision"))
            valid = False
        if not item["mechanism_refs"]:
            findings.append(_finding("WRITER-MECHANISM-MISSING", wid,
                                     "writer must cite at least one mechanism_ref"))
            valid = False
        for ref_index, ref in enumerate(item["mechanism_refs"]):
            ref_site = f"{wid}:mechanism_refs[{ref_index}]"
            if not _row_shape(ref, MECHANISM_FIELDS, ref_site, findings, "mechanism_ref"):
                valid = False
                continue
            capture = ref.get("capture")
            line_no, quote = ref.get("line"), ref.get("quote")
            lines = capture_lines.get(capture) if isinstance(capture, str) else None
            if (lines is None or not _positive_int(line_no) or not _nonempty(quote)
                    or line_no > len(lines) or quote not in lines[line_no - 1]):
                findings.append(_finding("MECHANISM-QUOTE-MISSING", ref_site,
                                         "quote is not an exact substring of its cited capture line"))
                valid = False
        for write_index, write in enumerate(item["writes"]):
            if not _nonempty(write):
                findings.append(_finding("REGISTRY-SCHEMA", f"{wid}:writes[{write_index}]",
                                         "write target must be nonempty text"))
                valid = False
        if not item["writes"]:
            findings.append(_finding("REGISTRY-SCHEMA", f"{wid}:writes",
                                     "writes must not be empty"))
            valid = False
        if not item["sources"]:
            findings.append(_finding("WRITER-SOURCE-MISSING", wid,
                                     "writer must cite at least one SOURCES row"))
            valid = False
        for source_index, source in enumerate(item["sources"]):
            ref_site = f"{wid}:sources[{source_index}]"
            if (not isinstance(source, str) or not SOURCE_ID.fullmatch(source)
                    or source_rows.get(source) not in ("queued", "mined")):
                findings.append(_finding("WRITER-SOURCE-MISSING", ref_site,
                                         "source id must resolve to a queued|mined row in committed corpus/SOURCES.md"))
                valid = False
        writer_ok[wid] = valid

    event_sources = []
    for index, item in enumerate(doc["event_sources"]):
        site = f"{registry_path}:event_sources[{index}]"
        if not _row_shape(item, EVENT_SOURCE_FIELDS, site, findings, "event_source"):
            continue
        capture, probe, pattern = item.get("capture"), item.get("probe"), item.get("pattern")
        if (not isinstance(capture, str) or capture not in capture_lines
                or not _nonempty(probe) or not _nonempty(pattern)):
            findings.append(_finding("REGISTRY-SCHEMA", site,
                                     "capture must be declared; probe and pattern must be nonempty"))
            continue
        event_sources.append(item)

    enumerated = {}
    for index, source in enumerate(event_sources):
        site = f"{registry_path}:event_sources[{index}]"
        path = source["capture"]
        lines = capture_lines[path]
        probe_line = "$ " + source["probe"]
        starts = [pos for pos, line in enumerate(lines) if line == probe_line]
        if not starts:
            findings.append(_finding("EVENT-PROBE-MISSING", site,
                                     "exact '$ <probe>' line not found in declared capture"))
            continue
        for start in starts:
            end = next((pos for pos in range(start + 1, len(lines))
                        if lines[pos].startswith("[rc=")), None)
            if end is None:
                findings.append(_finding("EVENT-SOURCE-TERMINATOR-MISSING", site,
                                         "probe block has no following [rc=] line"))
                end = len(lines)
            for pos in range(start + 1, end):
                line = lines[pos]
                if source["pattern"] in line:
                    enumerated[(path, pos + 1)] = line

    event_items = []
    event_ids = Counter()
    for index, item in enumerate(doc["events"]):
        site = f"{registry_path}:events[{index}]"
        if not _row_shape(item, EVENT_FIELDS, site, findings, "event"):
            continue
        eid = item.get("id")
        if not isinstance(eid, str) or not EVENT_ID.fullmatch(eid):
            findings.append(_finding("REGISTRY-SCHEMA", site, "event id must match EV-NN"))
            continue
        event_ids[eid] += 1
        event_items.append((index, item))
    for index, item in event_items:
        if event_ids[item["id"]] > 1:
            findings.append(_finding("EVENT-ID-DUPLICATE", f"{registry_path}:events[{index}]",
                                     f"duplicate event id {item['id']}"))

    claims = {}
    writers_with_events = set()
    event_valid = {}
    for index, event in event_items:
        site = f"{registry_path}:events[{index}]"
        capture, line_no = event.get("capture"), event.get("line")
        location = (capture, line_no)
        location_valid = isinstance(capture, str) and _positive_int(line_no)
        if location_valid:
            claims.setdefault(location, []).append((index, event))
        else:
            findings.append(_finding("REGISTRY-SCHEMA", site,
                                     "event capture and positive line number are required"))
        source_line = enumerated.get(location) if location_valid else None
        physical_lines = capture_lines.get(capture) if isinstance(capture, str) else None
        physical_line = (physical_lines[line_no - 1]
                         if physical_lines is not None and _positive_int(line_no)
                         and line_no <= len(physical_lines) else None)
        valid = source_line is not None
        if not valid:
            findings.append(_finding("EVENT-NOT-IN-SOURCE", site,
                                     "event location is not an enumerated pattern line inside its probe block"))
        if physical_line is None or not _nonempty(event.get("quote")) or event["quote"] not in physical_line:
            findings.append(_finding("EVENT-QUOTE-MISSING", site,
                                     "quote is not an exact substring of the event line"))
            valid = False
        writer_id = event.get("writer")
        writer = writers.get(writer_id) if isinstance(writer_id, str) else None
        if writer is None:
            findings.append(_finding("EVENT-WRITER-UNKNOWN", site,
                                     f"writer {writer_id!r} is not declared"))
            valid = False
        else:
            writers_with_events.add(writer_id)
            signature = writer["signature"]
            if physical_line is not None and not _signature_matches(signature, physical_line):
                findings.append(_finding("EVENT-SIGNATURE-MISMATCH", site,
                                         f"event line does not satisfy {signature['kind']} signature"))
                valid = False
            if not writer_ok.get(writer_id, False):
                valid = False
        published = event["id"] in knowledge_text
        if not published:
            findings.append(_finding("EVENT-UNPUBLISHED", event["id"],
                                     f"{event['id']} is absent from {doc['knowledge_entry']} at --revision"))
            valid = False
        if event_ids[event["id"]] > 1:
            valid = False
        event_valid[index] = valid

    unattributed = 0
    attributed = 0
    for location, line in sorted(enumerated.items()):
        line_claims = claims.get(location, [])
        if len(line_claims) == 0:
            findings.append(_finding("EVENT-UNATTRIBUTED", f"{location[0]}:{location[1]}",
                                     "enumerated /boot/limine.conf write line has no event claim"))
            unattributed += 1
        elif len(line_claims) > 1:
            findings.append(_finding("EVENT-DUPLICATE", f"{location[0]}:{location[1]}",
                                     f"enumerated event line has {len(line_claims)} event claims"))
            unattributed += 1
        elif event_valid.get(line_claims[0][0], False):
            attributed += 1
        else:
            unattributed += 1

    published_writer_classes = sum(
        1 for wid, writer in writers.items()
        if writer_published.get(wid, False) and bool(writer.get("mechanism_refs")))
    counts = {"events_total": len(enumerated),
              "attributed_events": attributed,
              "writer_classes": published_writer_classes,
              "writers_with_events": len(writers_with_events),
              "unattributed": unattributed}
    return _result(FAIL if findings else PASS, findings, counts)


def emit(result, revision, branch, branch_tip):
    status = {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[result.code]
    payload = {"status": status, "revision": revision, "branch": branch,
               "branch_tip": branch_tip, "counts": result.counts,
               "findings": [{"id": item.id, "site": item.site, "detail": item.detail}
                            for item in result.findings]}
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return result.code


def _emit_cannot(fid, site, detail, revision, branch, branch_tip):
    return emit(_result(CANNOT, [_finding(fid, site, detail)]),
                revision, branch, branch_tip)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Verify round-19 /boot/limine.conf writer attribution.",
        exit_on_error=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision", metavar="REV",
                       help="7-64 hex commit landed and pushed on the selected branch")
    group.add_argument("--selftest", action="store_true",
                       help="run hermetic Git-fixture tests")
    parser.add_argument("--branch", default="master",
                        help="landed branch for revision binding (default master)")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY,
                        help="lane-relative registry JSON path")
    parser.add_argument("--registry-from", metavar="REV",
                        help="read registry, captures and SOURCES.md at this bound revision")
    return parser


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        with contextlib.redirect_stderr(io.StringIO()):
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
        binding = bind(ROOT, args.revision, args.branch)
        registry_binding = (bind(ROOT, args.registry_from, args.branch)
                            if args.registry_from is not None else binding)
        if not _safe_path(args.registry, ".json"):
            return _emit_cannot("E-REGISTRY-PATH", "registry",
                                "registry must be a safe lane-relative .json path",
                                binding.sha, binding.branch, binding.branch_tip)
        reader = GitReader(ROOT)
        try:
            loaded = reader.read(registry_binding.sha, args.registry)
        except GitReadError as exc:
            return _emit_cannot("E-REGISTRY-READ-FAILED", args.registry, str(exc),
                                binding.sha, binding.branch, binding.branch_tip)
        if loaded.issue:
            return _emit_cannot("E-REGISTRY-MISSING" if loaded.issue == "missing"
                                else "E-REGISTRY-UNSAFE", args.registry,
                                "registry is absent or not a regular committed file",
                                binding.sha, binding.branch, binding.branch_tip)
        result = evaluate(loaded.data, registry_binding.sha, binding.sha, reader,
                          args.registry)
        return emit(result, binding.sha, binding.branch, binding.branch_tip)
    except RevisionError as exc:
        return _emit_cannot(exc.fid, exc.site, exc.detail,
                            binding.sha if binding else None,
                            args.branch, binding.branch_tip if binding else None)


# ---- Hermetic Git-fixture selftests ---------------------------------------


def _fixture_git(root, *args):
    proc = subprocess.run(["git", "--no-pager", "-C", str(root), *args],
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=clean_env(), timeout=60)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace")[:180]
                           or f"git {args[0]} exit={proc.returncode}")
    return proc.stdout.decode("ascii", "replace").strip()


def _fixture_snapshot(root, capture_text, events=None, signature=None,
                      mechanism_quote=None, sources=None, knowledge=None,
                      keep_digest=True):
    capture_path = "l1-capture/capture.txt"
    capture_file = root / capture_path
    capture_file.parent.mkdir(parents=True, exist_ok=True)
    capture_file.write_text(capture_text, encoding="utf-8")
    digest = hashlib.sha256(capture_file.read_bytes()).hexdigest()
    registry = {
        "schema": SCHEMA,
        "knowledge_entry": "corpus/knowledge/boot-writers-r19.md",
        "captures": [{"path": capture_path,
                      "sha256": digest if keep_digest else "0" * 64}],
        "event_sources": [{"capture": capture_path, "probe": "journal probe",
                           "pattern": "Updated: /boot/limine.conf"}],
        "writers": [{"id": "W-01", "name": "Snapper cleanup sync",
                     "trigger": "cleanup stop hook",
                     "mechanism_refs": [{"capture": capture_path, "line": 1,
                                         "quote": mechanism_quote or "# mechanism: snapper-cleanup.service"}],
                     "signature": signature or {"kind": "journal-unit",
                                                 "value": "snapper-cleanup.service"},
                     "writes": ["/boot/limine.conf"],
                     "sources": sources or ["S001"]}],
        "events": events if events is not None else [
            {"id": "EV-01", "capture": capture_path, "line": 3,
             "quote": "Updated: /boot/limine.conf", "writer": "W-01"}],
    }
    registry_file = root / DEFAULT_REGISTRY
    registry_file.parent.mkdir(parents=True, exist_ok=True)
    registry_file.write_text(json.dumps(registry, sort_keys=True), encoding="utf-8")
    sources_file = root / SOURCES_PATH
    sources_file.parent.mkdir(parents=True, exist_ok=True)
    sources_file.write_text(sources if isinstance(sources, str) else
                            "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
                            "|---|---|---|---|---|---|---|---|---|---|---|\n"
                            "| S001 | fixture | code | A | test | line 1 | writer | mined | today | 90d | — |\n",
                            encoding="utf-8")
    knowledge_file = root / registry["knowledge_entry"]
    knowledge_file.parent.mkdir(parents=True, exist_ok=True)
    knowledge_file.write_text(knowledge if knowledge is not None else
                              "W-01 EV-01\n", encoding="utf-8")
    _fixture_git(root, "add", "-A")
    _fixture_git(root, "commit", "-m", "fixture snapshot")
    return _fixture_git(root, "rev-parse", "HEAD")


def _invoke_fixture(revision, registry_from=None):
    argv = ["--revision", revision, "--branch", "master"]
    if registry_from is not None:
        argv.extend(("--registry-from", registry_from))
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        code = main(argv)
    return code, json.loads(output.getvalue())


def selftest():
    global ROOT
    original_root = ROOT
    passed, failures = [], []
    cases = 11
    try:
        with tempfile.TemporaryDirectory(prefix="check-boot-writers-",
                                         dir=str(original_root)) as temp:
            fixture = Path(temp)
            _fixture_git(fixture.parent, "init", "--quiet", "--initial-branch=master", str(fixture))
            _fixture_git(fixture, "config", "user.name", "Boot writer selftest")
            _fixture_git(fixture, "config", "user.email", "boot-writers-selftest@example.invalid")
            (fixture / "README.fixture").write_text("offline fixture\n", encoding="utf-8")
            _fixture_git(fixture, "add", "README.fixture")
            _fixture_git(fixture, "commit", "-m", "fixture baseline without knowledge entry")
            baseline = _fixture_git(fixture, "rev-parse", "HEAD")

            ROOT = fixture
            line = "2026-10-20 snapper-cleanup.service Updated: /boot/limine.conf"
            clean_text = ("# mechanism: snapper-cleanup.service\n$ journal probe\n"
                          + line + "\n[rc=0]\n")
            clean = _fixture_snapshot(fixture, clean_text)

            def check(name, revision, expected_code, expected_finding=None,
                      registry_from=None, expected_attributed=None):
                code, payload = _invoke_fixture(revision, registry_from)
                ids = {item["id"] for item in payload["findings"]}
                ok = code == expected_code and payload["status"] == {
                    PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[expected_code]
                if expected_finding is not None:
                    ok = ok and expected_finding in ids
                if expected_attributed is not None:
                    ok = ok and payload["counts"]["attributed_events"] == expected_attributed
                if ok:
                    passed.append(name)
                else:
                    failures.append(f"{name}: exit={code} findings={sorted(ids)} counts={payload['counts']}")

            check("clean", clean, PASS, expected_attributed=1)
            tampered = _fixture_snapshot(fixture, clean_text.replace("2026-10-20", "2026-10-21"),
                                          keep_digest=False)
            check("tampered capture", tampered, CANNOT, "CAPTURE-TAMPERED")
            extra = _fixture_snapshot(fixture, clean_text.replace(
                "[rc=0]", "2026-10-20 snapper-cleanup.service Updated: /boot/limine.conf\n[rc=0]"))
            check("extra unclaimed event line", extra, FAIL, "EVENT-UNATTRIBUTED")
            duplicate_events = [
                {"id": "EV-01", "capture": "l1-capture/capture.txt", "line": 3,
                 "quote": "Updated: /boot/limine.conf", "writer": "W-01"},
                {"id": "EV-02", "capture": "l1-capture/capture.txt", "line": 3,
                 "quote": "Updated: /boot/limine.conf", "writer": "W-01"},
            ]
            duplicate = _fixture_snapshot(fixture, clean_text, events=duplicate_events,
                                          knowledge="W-01 EV-01 EV-02\n")
            check("duplicate claim", duplicate, FAIL, "EVENT-DUPLICATE")
            outside_text = clean_text + "2026-10-20 snapper-cleanup.service Updated: /boot/limine.conf\n"
            outside_events = [{"id": "EV-01", "capture": "l1-capture/capture.txt", "line": 5,
                               "quote": "Updated: /boot/limine.conf", "writer": "W-01"}]
            outside = _fixture_snapshot(fixture, outside_text, events=outside_events)
            check("event outside probe block", outside, FAIL, "EVENT-NOT-IN-SOURCE")
            wrong_signature = _fixture_snapshot(fixture, clean_text,
                                                signature={"kind": "journal-unit",
                                                           "value": "different.service"})
            check("wrong signature", wrong_signature, FAIL, "EVENT-SIGNATURE-MISMATCH")
            missing_mechanism = _fixture_snapshot(fixture, clean_text,
                                                  mechanism_quote="absent mechanism text")
            check("missing mechanism quote", missing_mechanism, FAIL, "MECHANISM-QUOTE-MISSING")
            unknown_source = _fixture_snapshot(fixture, clean_text, sources=["S999"])
            check("unknown source id", unknown_source, FAIL, "WRITER-SOURCE-MISSING")
            unpublished = _fixture_snapshot(fixture, clean_text, knowledge="EV-01\n")
            check("unpublished writer", unpublished, FAIL, "WRITER-UNPUBLISHED")
            # The selected target predates the entry; registry and evidence are read
            # from the later bound revision exactly as --registry-from specifies.
            check("registry-from with unpublished baseline", baseline, FAIL,
                  "WRITER-UNPUBLISHED", registry_from=clean, expected_attributed=0)
            code, payload = _invoke_fixture("bad-revision")
            if code == CANNOT and payload["status"] == "CANNOT_EVALUATE" \
                    and any(item["id"] == "E-REVISION-INVALID" for item in payload["findings"]):
                passed.append("bad revision")
            else:
                failures.append(f"bad revision: exit={code} payload={payload}")
    except Exception as exc:
        failures.append(f"fixture setup: {type(exc).__name__}: {str(exc)[:180]}")
    finally:
        ROOT = original_root
    if len(passed) + len(failures) != cases:
        failures.append(f"case accounting mismatch: {len(passed)} passed + {len(failures)} failures, expected {cases}")
    if failures:
        print(f"FAIL ({cases} cases, {len(passed)} passed, {len(failures)} failed)")
        for failure in failures:
            print(f"  {failure}")
        return FAIL
    print(f"PASS ({cases} cases, {len(passed)} passed, 0 failed)")
    return PASS


if __name__ == "__main__":
    sys.exit(main())
