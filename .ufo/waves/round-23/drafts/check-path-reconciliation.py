#!/usr/bin/env python3
"""C3 (round 23): exhaustive rough-versus-lane path-cohort reconciliation.

Recomputes the per-event cohort ledger for the two fixed r22 lanes (build,
falsify) from frozen historical bytes only, then requires exact equality with
the committed reconciliation record at
``.ufo/waves/round-23/path-reconciliation.json``.

Rough classifier: the bounded CloseKaidoku22 census algorithm, reimplemented
literally (``strip_sel`` regex, then one path failure per event via ``break``).
Its per-lane path totals are given observations recorded in the frozen
manifest: build 25, falsify 33.

Canonical classifier (old-v1 literal authority, independently authored): an
event is path-denied exactly when one of its path components fails exact
read/write membership after stripping valid selector tokens.  Selector tokens
are ``raw`` and the digit/range family ``\\d[\\d\\-+,:]*`` / ``-\\d+`` /
``\\d+-``, repeatable in any order at the tail, so ``:raw:N-M`` and ``:N-M:raw``
are both valid — the exact mixed-order pair the rough regex cannot strip.
Skill URIs are literal members; dot segments, control characters and
off-roster spellings are never members, so component-level rejection collapses
to exact membership and is checked as an explicit guard.  The canonical
per-event denial set is verified against the retained audit SCOPE-PATH-DENIED
sites (build 23, falsify 29).

Dispositions are bounded: ``non-path`` (exec/unknown cohorts), ``agreement``
(rough and canonical and the retained lane agree, denied or clean),
``selector-normalization`` (rough-only flag the v1 grammar strips away) and
``unit-difference`` (any leftover event-level/component-level disagreement; a
lane containing one is unexplained).  Net arithmetic is reported as computed;
component counting may cancel, so no "exactly N unique records" claim is
forced.

Exit convention: 0 clean, 1 failed, 2 could-not-evaluate.  All frozen input
bytes are hashed before any evaluation; a digest mismatch is SNAPSHOT-TAMPERED
with exit 2.  A missing reconciliation record is unexplained_cohorts=2, exit 1,
RECONCILIATION-MISSING.  Source-only outputs; this gate never executes,
imports or verifies historical seat content, and never reads new C1/C2
production files.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True
import _revision

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECORD = ".ufo/waves/round-23/path-reconciliation.json"
DEFAULT_FROZEN = ".ufo/waves/round-23/frozen/reconciliation-inputs.json"
LANES = ("build", "falsify")
SCHEMA_FROZEN = "tsukuroi-reconciliation-inputs-v1"
SCHEMA_RECORD = "tsukuroi-path-reconciliation-v1"
SCHEMA_EVENTS = "tsukuroi-seat-events-v1"
SCHEMA_BINDINGS = "tsukuroi-seat-bindings-v1"
PATH_TOOLS = ("read", "grep", "glob", "write")
ROUGH_STRIP = re.compile(r":(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$")
CANON_TOKEN = re.compile(r":(?:raw|\d[\d\-+,:]*|-\d+|\d+-)$")
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
HEX64 = re.compile(r"[0-9a-f]{64}")


def snapshot_paths(wave):
    base = ".ufo/waves/round-23"
    return {"events": f"{base}/snapshot/r22/{wave}/events.json",
            "bindings": f"{base}/snapshot/r22/{wave}/bindings.json",
            "audit": f"{base}/snapshot/r22/{wave}/audit.json"}


def has_controls(value):
    return any(unicodedata.category(char) in ("Cc", "Cf", "Cs", "Zl", "Zp")
               for char in value)


def safe_path(path):
    return (isinstance(path, str) and bool(path) and not path.startswith("/")
            and "\\" not in path and not has_controls(path)
            and all(part not in ("", ".", "..") for part in path.split("/"))
            and not PurePosixPath(path).is_absolute())


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def strict_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object)


def strip_rough(value):
    """Exact bounded rough algorithm: one regex, no component work."""
    return ROUGH_STRIP.sub("", value)


def strip_canonical(value):
    """Old-v1 selector tokens, repeatable in any order at the tail."""
    base = value
    while True:
        stripped = CANON_TOKEN.sub("", base, count=1)
        if stripped == base:
            return base
        base = stripped


def path_components(tool, raw):
    """Rough splitting unit: grep and glob accept ';'-joined paths."""
    if tool in ("grep", "glob"):
        return str(raw).split(";")
    return [str(raw)]


def component_rejected(component):
    """Dot/control spellings are never v1 members; reject before stripping."""
    parts = component.split("/")
    return has_controls(component) or not component or \
        any(part in ("", ".", "..") for part in parts)


def canonical_bad_indices(tool, components, binding):
    """Indices of components failing v1 literal authority for this tool."""
    if tool == "write":
        members, strip = binding.get("write_paths") or [], False
    else:
        members, strip = binding.get("read_paths") or [], tool in ("read", "grep")
    bad = []
    for index, component in enumerate(components):
        if component in members:
            continue
        if component_rejected(component):
            bad.append(index)
            continue
        candidate = strip_canonical(component) if strip else component
        if candidate not in members:
            bad.append(index)
    return bad


def rough_first_bad(tool, components, binding):
    """Rough membership: first failing component wins, then break."""
    members = binding.get("write_paths") if tool == "write" \
        else binding.get("read_paths")
    for component in components:
        candidate = strip_rough(component) if tool in ("read", "grep") \
            else component
        if candidate not in members:
            return component
    return None


def identity_digest(wave, seat, index, tool, raw):
    payload = json.dumps([wave, seat, index, tool, raw],
                         sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def event_raw(e):
    args = e.get("args") if isinstance(e.get("args"), dict) else {}
    return str(args.get("path", ""))


def derive(wave, events, bindings, audit):
    """Reproducible cohort ledger for one wave; L1 constructs records from it.

    events/bindings are the parsed frozen snapshot objects, audit the parsed
    frozen lane audit.  Rows cover every event, including non-path events.
    """
    table = {s["name"]: s for s in bindings["seats"]}
    retained = {}
    for finding in audit.get("findings") or []:
        if finding.get("id") != "SCOPE-PATH-DENIED":
            continue
        site = finding.get("site")
        if not isinstance(site, str) or ":" not in site:
            raise ValueError(f"malformed audit site {site!r}")
        seat, _, number = site.rpartition(":")
        if seat not in table or not number.isdigit():
            raise ValueError(f"audit site outside roster: {site!r}")
        retained.setdefault((seat, int(number)), 0)
        retained[(seat, int(number))] += 1
    rows = []
    for seat in events["seats"]:
        binding = table[seat["name"]]
        for index, e in enumerate(seat.get("events") or []):
            tool = e.get("tool")
            raw = event_raw(e)
            if tool in PATH_TOOLS:
                components = path_components(tool, raw)
                first_bad = rough_first_bad(tool, components, binding)
                bad = canonical_bad_indices(tool, components, binding)
            else:
                components, first_bad, bad = [], None, []
            rough_flag = first_bad is not None
            kept = retained.get((seat["name"], index), 0)
            if tool not in PATH_TOOLS:
                disposition = "non-path"
            elif rough_flag and bad and kept:
                disposition = "agreement"
            elif not rough_flag and not bad and not kept:
                disposition = "agreement"
            elif rough_flag and not bad and not kept:
                disposition = "selector-normalization"
            else:
                disposition = "unit-difference"
            if tool == "bash":
                rough = "exec"
            elif tool not in PATH_TOOLS:
                rough = "unknown"
            elif rough_flag:
                rough = "path"
            else:
                rough = "clean"
            rows.append({
                "seat": seat["name"],
                "index": index,
                "tool": tool,
                "identity": identity_digest(wave, seat["name"], index, tool, raw),
                "rough_class": rough,
                "rough_first_bad": first_bad,
                "rough_path_failures": 1 if rough_flag else 0,
                "canonical_bad_indices": bad,
                "canonical_path_failures": len(bad),
                "retained_sites": kept,
                "disposition": disposition,
            })
    return {
        "wave": wave,
        "rough_path_events": sum(r["rough_path_failures"] for r in rows),
        "retained_path_sites": sum(r["retained_sites"] for r in rows),
        "rows": rows,
    }


def lane_valid(ledger, expected):
    """Bounded validation; a lane explains its cohort only when every row fits."""
    if ledger["rough_path_events"] != expected["rough_as_reported"]:
        return False
    if ledger["retained_path_sites"] != expected["lane_retained"]:
        return False
    for row in ledger["rows"]:
        if row["disposition"] == "non-path":
            if row["canonical_path_failures"] or row["retained_sites"]:
                return False
        elif row["disposition"] == "selector-normalization":
            if not (row["rough_path_failures"] and not row["canonical_path_failures"]
                    and not row["retained_sites"]):
                return False
        elif row["disposition"] == "agreement":
            denied = bool(row["canonical_path_failures"]) or bool(row["retained_sites"])
            if denied and not (row["rough_path_failures"]
                               and row["canonical_path_failures"]
                               and row["retained_sites"]):
                return False
            if not denied and row["rough_path_failures"]:
                return False
        else:
            return False
    return True


def check_roster(events, bindings, audit):
    """Roster identity across events, bindings and audit; raises on mismatch."""
    event_names = [s.get("name") for s in events.get("seats") or []]
    binding_names = [s.get("name") for s in bindings.get("seats") or []]
    audit_names = [s.get("name") for s in audit.get("seats") or []]
    if not all(isinstance(n, str) and NAME.fullmatch(n) for n in event_names):
        raise ValueError("invalid seat name in events")
    if sorted(event_names) != sorted(binding_names) or \
            sorted(event_names) != sorted(audit_names):
        raise ValueError("seat roster differs across events/bindings/audit")
    if len(set(event_names)) != len(event_names):
        raise ValueError("duplicate seat name")


def parse_snapshot(raw, schema):
    data = strict_json(raw)
    if not isinstance(data, dict) or data.get("schema") != schema:
        raise ValueError(f"expected schema {schema}")
    return data


def parse_audit(raw):
    """The frozen lane audits carry no schema field; shape only."""
    data = strict_json(raw)
    if not isinstance(data, dict) or not isinstance(data.get("findings"), list) \
            or not isinstance(data.get("seats"), list):
        raise ValueError("invalid audit shape")
    return data


def evaluate(frozen_raw, record_raw, read_bytes):
    """Hash every frozen input first; then recompute and require equality."""
    findings = []

    def add(fid, site):
        findings.append({"id": fid, "site": site})

    def finish(code, unexplained, extra=None):
        payload = {"status": ("PASS", "FAIL", "CANNOT_EVALUATE")[code],
                   "unexplained_cohorts": unexplained, "findings": findings,
                   "scope": "frozen r22 path-cohort reconciliation; not relabeled "
                            "violations, enforcement or trace completeness"}
        payload.update(extra or {})
        return code, payload

    try:
        frozen = parse_snapshot(frozen_raw, SCHEMA_FROZEN)
        inputs = frozen.get("inputs")
        expected = frozen.get("expected")
        if not isinstance(inputs, dict) or not inputs or \
                not isinstance(expected, dict) or set(expected) != set(LANES) or \
                not all(isinstance(expected[w], dict) for w in LANES):
            raise ValueError("invalid frozen manifest shape")
    except (ValueError, TypeError, UnicodeError) as exc:
        add("FROZEN-SCHEMA", str(exc)[:100])
        return finish(2, len(LANES))
    for relpath, digest in inputs.items():
        if not safe_path(relpath) or not isinstance(digest, str) \
                or not HEX64.fullmatch(digest):
            add("FROZEN-SCHEMA", relpath)
            return finish(2, len(LANES))
        try:
            data = read_bytes(relpath)
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
            add("SNAPSHOT-READ-FAILED", relpath)
            return finish(2, len(LANES), {"detail": str(exc)[:100]})
        if data is None or hashlib.sha256(data).hexdigest() != digest:
            add("SNAPSHOT-TAMPERED", relpath)
    if findings:
        return finish(2, len(LANES))
    try:
        blobs = {rel: read_bytes(rel) for rel in inputs}
        lanes = {}
        for wave in LANES:
            paths = snapshot_paths(wave)
            events = parse_snapshot(blobs[paths["events"]], SCHEMA_EVENTS)
            bindings = parse_snapshot(blobs[paths["bindings"]], SCHEMA_BINDINGS)
            audit = parse_audit(blobs[paths["audit"]])
            check_roster(events, bindings, audit)
            lanes[wave] = derive(wave, events, bindings, audit)
    except (ValueError, TypeError, KeyError, UnicodeError) as exc:
        add("SNAPSHOT-SCHEMA", str(exc)[:100])
        return finish(2, len(LANES))
    source_counts = {w: expected[w].get("rough_as_reported") for w in LANES}
    lane_counts = {w: expected[w].get("lane_retained") for w in LANES}
    for wave in LANES:
        if not isinstance(source_counts[wave], int) or \
                not isinstance(lane_counts[wave], int):
            add("FROZEN-SCHEMA", wave)
            return finish(2, len(LANES))
        if lanes[wave]["rough_path_events"] != source_counts[wave] or \
                lanes[wave]["retained_path_sites"] != lane_counts[wave]:
            add("LANE-CENSUS-MISMATCH", wave)
    if record_raw is None:
        add("RECONCILIATION-MISSING", DEFAULT_RECORD)
        return finish(1, len(LANES))
    try:
        record = parse_snapshot(record_raw, SCHEMA_RECORD)
        record_lanes = record.get("lanes")
        declared_unexplained = record.get("unexplained_cohorts")
        declared_sources = record.get("source_counts")
        declared_lanes = record.get("lane_counts")
        if not isinstance(record_lanes, dict) or set(record_lanes) != set(LANES):
            raise ValueError("record lanes must cover build and falsify")
        for counts, label in ((declared_sources, "source_counts"),
                              (declared_lanes, "lane_counts")):
            if not isinstance(counts, dict) or set(counts) != set(LANES) or \
                    not all(isinstance(v, int) for v in counts.values()):
                raise ValueError(f"invalid declared {label}")
        if not isinstance(declared_unexplained, int) or \
                not 0 <= declared_unexplained <= len(LANES):
            raise ValueError("invalid declared unexplained_cohorts")
    except (ValueError, TypeError, UnicodeError) as exc:
        add("RECONCILIATION-SCHEMA", str(exc)[:100])
        return finish(2, len(LANES))
    unexplained = 0
    for wave in LANES:
        if record_lanes[wave] != lanes[wave]:
            add("RECONCILIATION-MISMATCH", wave)
            unexplained += 1
            continue
        if not lane_valid(lanes[wave], expected[wave]):
            add("COHORT-UNEXPLAINED", wave)
            unexplained += 1
    if declared_unexplained != unexplained:
        add("RECONCILIATION-ARITHMETIC", "unexplained_cohorts")
    if declared_sources != source_counts or declared_lanes != lane_counts:
        add("RECONCILIATION-ARITHMETIC", "declared counts")
    return finish(1 if findings else 0, unexplained)


def git_read(rev, path):
    proc = subprocess.run(["git", "--no-pager", "-C", str(ROOT), "show",
                           f"{rev}:{path}"], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=_revision.clean_env(),
                          timeout=30)
    if proc.returncode:
        exists = subprocess.run(["git", "--literal-pathspecs", "--no-pager",
                                 "-C", str(ROOT), "ls-tree", "-z", rev, "--",
                                 path], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                env=_revision.clean_env(), timeout=30)
        if exists.returncode == 0 and not exists.stdout:
            return None
        raise RuntimeError(f"cannot read committed {path}")
    return proc.stdout


def _fixture_lane():
    """One literal wave fixture; identical bytes stand in for both lanes.

    Hand-derived expectations (no execution): rough path events 4
    (Alpha:3 write-other, Beta:1 raw-first selector, Beta:2 and Beta:3 grep);
    retained sites 3 (Alpha:3, Beta:2, Beta:3); Beta:0 range-first selector is
    rough-clean; Alpha:1 range-then-raw is rough-clean; per-component canonical
    count 2 on Beta:3 against one rough failure and one retained site.
    """
    events = {"schema": SCHEMA_EVENTS, "seats": [
        {"name": "Alpha", "events": [
            {"tool": "read", "args": {"path": "/r/a.json"}},
            {"tool": "read", "args": {"path": "/r/a.json:2-4:raw"}},
            {"tool": "read", "args": {"path": "/r/b.md:raw"}},
            {"tool": "write", "args": {"path": "/w/other.md"}},
            {"tool": "bash", "args": {"command": ""}},
            {"tool": "edit", "args": {"path": "/w/a.md"}},
        ]},
        {"name": "Beta", "events": [
            {"tool": "read", "args": {"path": "/r/b.md:2-4:raw"}},
            {"tool": "read", "args": {"path": "/r/b.md:raw:2-4"}},
            {"tool": "grep", "args": {"path": "/r/a.json;/w/secret.md"}},
            {"tool": "grep", "args": {"path": "/r/a.json;/n1;/n2"}},
            {"tool": "read", "args": {"path": "/r/a.json:5-9,20-22"}},
        ]}]}
    bindings = {"schema": SCHEMA_BINDINGS, "seats": [
        {"name": "Alpha", "read_paths": ["/r/a.json", "/r/b.md", "skill://g"],
         "write_paths": ["/w/a.md"]},
        {"name": "Beta", "read_paths": ["/r/a.json", "/r/b.md", "skill://g"],
         "write_paths": ["/w/a.md"]}]}
    audit = {"findings": [
        {"id": "SCOPE-TOOL-UNKNOWN", "site": "Alpha:5"},
        {"id": "SCOPE-PATH-DENIED", "site": "Alpha:3"},
        {"id": "SCOPE-PATH-DENIED", "site": "Beta:2"},
        {"id": "SCOPE-PATH-DENIED", "site": "Beta:3"}],
        "seats": [{"name": "Alpha"}, {"name": "Beta"}]}
    return events, bindings, audit


def selftest():
    failures = []
    observations = []
    events, bindings, audit = _fixture_lane()
    lanes = {wave: derive(wave, events, bindings, audit) for wave in LANES}
    expected = {w: {"rough_as_reported": 4, "lane_retained": 3} for w in LANES}
    inputs = {
        ".ufo/waves/round-23/snapshot/r22/build/events.json": "f" * 64,
        ".ufo/waves/round-23/snapshot/r22/build/bindings.json": "e" * 64,
        ".ufo/waves/round-23/snapshot/r22/build/audit.json": "d" * 64,
        ".ufo/waves/round-23/snapshot/r22/falsify/events.json": "c" * 64,
        ".ufo/waves/round-23/snapshot/r22/falsify/bindings.json": "b" * 64,
        ".ufo/waves/round-23/snapshot/r22/falsify/audit.json": "a" * 64,
        ".ufo/waves/round-23/sources/r22-rough-census.txt": "0" * 64}
    frozen = {"schema": SCHEMA_FROZEN,
              "baseline": "ae01e50f582016384e620022be38bf5367000e2e",
              "inputs": inputs, "expected": expected, "scope": "fixture"}

    def surfaces():
        return {
            ".ufo/waves/round-23/snapshot/r22/build/events.json":
                json.dumps(events).encode(),
            ".ufo/waves/round-23/snapshot/r22/build/bindings.json":
                json.dumps(bindings).encode(),
            ".ufo/waves/round-23/snapshot/r22/build/audit.json":
                json.dumps(audit).encode(),
            ".ufo/waves/round-23/snapshot/r22/falsify/events.json":
                json.dumps(events).encode(),
            ".ufo/waves/round-23/snapshot/r22/falsify/bindings.json":
                json.dumps(bindings).encode(),
            ".ufo/waves/round-23/snapshot/r22/falsify/audit.json":
                json.dumps(audit).encode(),
            ".ufo/waves/round-23/sources/r22-rough-census.txt": b"rough source\n"}

    def frozen_bytes(files):
        data = copy.deepcopy(frozen)
        for relpath in data["inputs"]:
            data["inputs"][relpath] = hashlib.sha256(files[relpath]).hexdigest()
        return json.dumps(data).encode()

    def run(name, files, record, want_code, want_ids, want_unexplained):
        code, payload = evaluate(frozen_bytes(files),
                                 None if record is None
                                 else json.dumps(record).encode(),
                                 files.get)
        ids = sorted(f["id"] for f in payload["findings"])
        observations.append({"case": name, "exit": code, "finding_ids": ids,
                             "unexplained_cohorts": payload["unexplained_cohorts"]})
        problems = []
        if code != want_code or ids != sorted(want_ids):
            problems.append("exit/findings")
        if payload["unexplained_cohorts"] != want_unexplained:
            problems.append("unexplained_cohorts")
        if problems:
            failures.append(f"{name}: " + ", ".join(problems))

    good_record = {"schema": SCHEMA_RECORD, "unexplained_cohorts": 0,
                   "source_counts": {"build": 4, "falsify": 4},
                   "lane_counts": {"build": 3, "falsify": 3},
                   "lanes": copy.deepcopy(lanes)}
    files = surfaces()
    run("clean", files, good_record, 0, [], 0)

    # mixed selector-order controls: rough strips range-then-raw only
    by_key = {(wave, r["seat"], r["index"]): r
              for wave in LANES for r in lanes[wave]["rows"]}
    if by_key[("build", "Beta", 1)]["disposition"] != "selector-normalization" \
            or by_key[("build", "Beta", 1)]["canonical_path_failures"] \
            or not by_key[("build", "Beta", 1)]["rough_path_failures"]:
        failures.append("mixed-raw-first: wrong classification")
    if by_key[("build", "Beta", 0)]["disposition"] != "agreement" \
            or by_key[("build", "Alpha", 1)]["rough_path_failures"]:
        failures.append("mixed-range-first: rough must strip range-then-raw")
    # per-component canonical counting against one-per-event rough counting
    per_component = by_key[("build", "Beta", 3)]
    if per_component["canonical_bad_indices"] != [1, 2] \
            or per_component["retained_sites"] != 1 \
            or per_component["rough_first_bad"] != "/n1" \
            or per_component["rough_path_failures"] != 1 \
            or per_component["disposition"] != "agreement":
        failures.append("one-per-event-vs-per-component: wrong counts")

    run("missing-record", files, None, 1, ["RECONCILIATION-MISSING"], 2)

    # tamper with the original digest retained: exactly one mismatching input
    tamper_files = surfaces()
    tamper_files[".ufo/waves/round-23/snapshot/r22/build/audit.json"] = b'{"x":1}\n'
    tamper_frozen = copy.deepcopy(frozen)
    for relpath in tamper_frozen["inputs"]:
        tamper_frozen["inputs"][relpath] = \
            hashlib.sha256(tamper_files[relpath]).hexdigest()
    original_audit = hashlib.sha256(surfaces()[
        ".ufo/waves/round-23/snapshot/r22/build/audit.json"]).hexdigest()
    tamper_frozen["inputs"][".ufo/waves/round-23/snapshot/r22/build/audit.json"] = \
        original_audit
    code, payload = evaluate(json.dumps(tamper_frozen).encode(),
                             json.dumps(good_record).encode(),
                             tamper_files.get)
    ids = sorted(f["id"] for f in payload["findings"])
    if code != 2 or ids != ["SNAPSHOT-TAMPERED"]:
        failures.append(f"manifest-tamper: exit={code} ids={ids}")
    observations.append({"case": "manifest-tamper", "exit": code,
                         "finding_ids": ids,
                         "unexplained_cohorts": payload["unexplained_cohorts"]})

    dropped = copy.deepcopy(good_record)
    dropped["lanes"]["build"]["rows"] = dropped["lanes"]["build"]["rows"][1:]
    run("dropped-row", files, dropped, 1,
        ["RECONCILIATION-ARITHMETIC", "RECONCILIATION-MISMATCH"], 1)

    duplicated = copy.deepcopy(good_record)
    duplicated["lanes"]["build"]["rows"].append(
        copy.deepcopy(duplicated["lanes"]["build"]["rows"][0]))
    run("duplicate-row", files, duplicated, 1,
        ["RECONCILIATION-ARITHMETIC", "RECONCILIATION-MISMATCH"], 1)

    wrong_arith = copy.deepcopy(good_record)
    wrong_arith["source_counts"] = {"build": 3, "falsify": 4}
    run("wrong-arithmetic", files, wrong_arith, 1, ["RECONCILIATION-ARITHMETIC"], 0)

    wrong_disp = copy.deepcopy(good_record)
    wrong_disp["lanes"]["build"]["rows"][1]["disposition"] = "unit-difference"
    run("wrong-disposition", files, wrong_disp, 1,
        ["RECONCILIATION-ARITHMETIC", "RECONCILIATION-MISMATCH"], 1)

    bad_unexplained = copy.deepcopy(good_record)
    bad_unexplained["unexplained_cohorts"] = 1
    run("wrong-unexplained", files, bad_unexplained, 1,
        ["RECONCILIATION-ARITHMETIC"], 0)

    unknown_disp = copy.deepcopy(good_record)
    unknown_disp["lanes"]["build"]["rows"][0]["disposition"] = "mystery"
    run("unknown-disposition", files, unknown_disp, 1,
        ["RECONCILIATION-ARITHMETIC", "RECONCILIATION-MISMATCH"], 1)

    roster_files = surfaces()
    roster_events = copy.deepcopy(events)
    roster_events["seats"] = [s for s in roster_events["seats"]
                              if s["name"] != "Beta"]
    roster_files[".ufo/waves/round-23/snapshot/r22/build/events.json"] = \
        json.dumps(roster_events).encode()
    run("roster-mismatch", roster_files, good_record, 2, ["SNAPSHOT-SCHEMA"], 2)

    code, payload = evaluate(frozen_bytes(files), b'{"schema":', files.get)
    ids = sorted(f["id"] for f in payload["findings"])
    if code != 2 or ids != ["RECONCILIATION-SCHEMA"]:
        failures.append(f"malformed-record: exit={code} ids={ids}")
    observations.append({"case": "malformed-record", "exit": code,
                         "finding_ids": ids,
                         "unexplained_cohorts": payload["unexplained_cohorts"]})

    dup_raw = (b'{"schema":"' + SCHEMA_RECORD.encode()
               + b'","unexplained_cohorts":0,"unexplained_cohorts":1,'
               b'"source_counts":{},"lane_counts":{},"lanes":{}}')
    code, payload = evaluate(frozen_bytes(files), dup_raw, files.get)
    ids = sorted(f["id"] for f in payload["findings"])
    if code != 2 or ids != ["RECONCILIATION-SCHEMA"]:
        failures.append(f"duplicate-json-key: exit={code} ids={ids}")
    observations.append({"case": "duplicate-json-key", "exit": code,
                         "finding_ids": ids,
                         "unexplained_cohorts": payload["unexplained_cohorts"]})

    code, payload = evaluate(json.dumps(frozen).encode(),
                             json.dumps(good_record).encode(), files.get)
    ids = sorted(f["id"] for f in payload["findings"])
    if code != 2 or not set(ids) <= {"SNAPSHOT-TAMPERED"}:
        failures.append(f"stale-manifest-digest: exit={code} ids={ids}")
    observations.append({"case": "stale-manifest-digest", "exit": code,
                         "finding_ids": ids,
                         "unexplained_cohorts": payload["unexplained_cohorts"]})

    print(json.dumps({"status": "FAIL" if failures else "PASS",
                      "cases": len(observations),
                      "passed": len(observations) - len(failures),
                      "failures": failures, "observations": observations}))
    return 1 if failures else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--revision")
    choice.add_argument("--selftest", action="store_true")
    parser.add_argument("--branch", default="master")
    parser.add_argument("--record", default=DEFAULT_RECORD)
    parser.add_argument("--frozen", default=DEFAULT_FROZEN)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    if args.selftest:
        return selftest()
    if not safe_path(args.record) or not safe_path(args.frozen):
        print(json.dumps({"status": "CANNOT_EVALUATE", "unexplained_cohorts": 2,
                          "findings": [{"id": "PATH-SPEC-INVALID",
                                        "site": "record/frozen path"}]}))
        return 2
    try:
        binding = _revision.bind(ROOT, args.revision, args.branch)
        code, payload = evaluate(git_read(binding.sha, args.frozen),
                                 git_read(binding.sha, args.record),
                                 lambda path: git_read(binding.sha, path))
        payload.update(revision=binding.sha, branch=binding.branch,
                       branch_tip=binding.branch_tip)
    except _revision.RevisionError as exc:
        code, payload = 2, {"status": "CANNOT_EVALUATE", "unexplained_cohorts": 2,
                            "findings": [{"id": exc.fid, "site": exc.site}]}
    except (OSError, RuntimeError, UnicodeError,
            subprocess.TimeoutExpired) as exc:
        code, payload = 2, {"status": "CANNOT_EVALUATE", "unexplained_cohorts": 2,
                            "findings": [{"id": "E-READ", "site": str(exc)[:120]}]}
    print(json.dumps(payload, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
