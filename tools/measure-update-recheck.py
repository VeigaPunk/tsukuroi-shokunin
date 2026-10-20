#!/usr/bin/env python3
"""Read-only round-15 update-safety recheck counting probe.

One committed C2 record and one captured host snapshot, both read from the same
revision. Exit 0 when the pair is absent (record_count 0, "before") or the
record is internally consistent with the snapshot (record_count 1); exit 2 when
the input is malformed, incomplete or contradicts the snapshot. Absence is a
probe count, never a safety pass. This is not a truth gate: it issues no health,
repair, causality or upgrade-clearance verdict.

No writes. No host-state command is executed: the snapshot is data, and
--revision only reads git blobs with read-only plumbing (GIT_OPTIONAL_LOCKS=0).
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import namedtuple
from datetime import datetime, timedelta, timezone
from pathlib import Path

PASS, CANNOT = 0, 2
ROOT = Path(__file__).resolve().parents[1]
RECORD = "corpus/knowledge/partial-upgrade-recheck-r15.json"
SNAPSHOT = ".ufo/waves/round-15/build/host-snapshot.json"
SCHEMA = "tsukuroi-partial-upgrade-recheck-v1"
DECISION = "BLOCKED_FOR_AGENT_PACKAGE_ACTION"
REQUIRED_KEYS = ("schema", "source_ids", "observed_at", "evidence_path", "snapshot_sha256",
                 "observations", "decision", "limits")
REQUIRED_SOURCES = ("S047", "S048", "S049")
PROBE_KEYS = ("package_versions", "pending_updates", "sync_metadata", "libinput_log",
              "boot_hook_mentions")
PACKAGES = ("libinput", "libinput-tools", "mkinitcpio", "systemd")
REV = re.compile(r"^(?:HEAD|[0-9a-fA-F]{4,64})$")
STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SOURCE_ID = re.compile(r"^S\d{3,}$")
QU_ROW = re.compile(r"^\S+ \S+ -> \S+(?: \[ignored\])?$")
QUERY_ROW = re.compile(r"^(\S+) (\S+)$")
LOG_STAMP = re.compile(r"\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{4})\]")
LOG_UPGRADE = re.compile(r"upgraded libinput \((\S+) -> (\S+)\)")
HOOK_REF = re.compile(r"([A-Za-z0-9_.+-]+):(\d+)")

Finding = namedtuple("Finding", "id site detail")
Assessment = namedtuple("Assessment", "findings record_count pending pending_exit installed "
                                      "sources observed captured decision digest")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def utc_text(value):
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_utc(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def load_json(raw, site, prefix):
    def pairs(items):
        obj = {}
        for key, value in items:
            if key in obj:
                raise Cannot(prefix + "-DUPLICATE", site, f"duplicate key {key!r}")
            obj[key] = value
        return obj

    def constant(token):
        raise Cannot(prefix + "-NONFINITE", site, f"non-finite constant {token}")

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Cannot(prefix + "-READ", site, f"utf-8 decode failed at byte {exc.start}")
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except Cannot:
        raise
    except json.JSONDecodeError as exc:
        raise Cannot(prefix + "-PARSE", site,
                     f"json parse failed at line {exc.lineno} column {exc.colno}: {exc.msg}")


def validate_snapshot(doc):
    if not isinstance(doc, dict):
        raise Cannot("E-SNAPSHOT-SHAPE", SNAPSHOT, "top-level object required")
    captured = doc.get("captured_at")
    if not isinstance(captured, str) or not STAMP.fullmatch(captured):
        raise Cannot("E-SNAPSHOT-CAPTURED", SNAPSHOT,
                     "captured_at must be strict UTC YYYY-MM-DDTHH:MM:SSZ")
    try:
        parse_utc(captured)
    except ValueError:
        raise Cannot("E-SNAPSHOT-CAPTURED", SNAPSHOT, "captured_at is not a calendar-valid stamp")
    probes = doc.get("probes")
    if not isinstance(probes, dict):
        raise Cannot("E-SNAPSHOT-SHAPE", SNAPSHOT, "probes object required")
    for key in PROBE_KEYS:
        probe = probes.get(key)
        if not isinstance(probe, dict):
            raise Cannot("E-SNAPSHOT-PROBE", SNAPSHOT, f"probe {key} absent")
        for field in ("command", "stdout", "stderr"):
            if not isinstance(probe.get(field), str):
                raise Cannot("E-SNAPSHOT-PROBE", SNAPSHOT, f"{key}.{field} string required")
        if not probe["command"].strip():
            raise Cannot("E-SNAPSHOT-PROBE", SNAPSHOT, f"{key}.command empty")
        exitcode = probe.get("exit")
        if isinstance(exitcode, bool) or not isinstance(exitcode, int):
            raise Cannot("E-SNAPSHOT-PROBE", SNAPSHOT, f"{key}.exit plain int required")
    return captured, probes


def parse_packages(probe):
    if probe["exit"] != 0 or probe["stderr"] != "":
        raise Cannot("E-SNAPSHOT-PACKAGES", SNAPSHOT,
                     f"package query failed: exit={probe['exit']} stderr_bytes={len(probe['stderr'])}")
    table = {}
    for line in probe["stdout"].splitlines():
        if not line.strip():
            continue
        match = QUERY_ROW.match(line.strip())
        if not match:
            raise Cannot("E-SNAPSHOT-PACKAGES", SNAPSHOT, f"unexpected package row {line[:60]!r}")
        name, version = match.groups()
        if name in table:
            raise Cannot("E-SNAPSHOT-PACKAGES", SNAPSHOT, f"duplicate package row {name}")
        table[name] = version
    if set(table) != set(PACKAGES):
        raise Cannot("E-SNAPSHOT-PACKAGES", SNAPSHOT,
                     "queried package set must be " + ",".join(PACKAGES))
    return table


def parse_pending(probe):
    exitcode, out, err = probe["exit"], probe["stdout"], probe["stderr"]
    if exitcode == 0 and err == "":
        rows = [line.strip() for line in out.splitlines() if line.strip()]
        for row in rows:
            if not QU_ROW.match(row):
                raise Cannot("E-SNAPSHOT-PENDING", SNAPSHOT, f"unexpected -Qu row {row[:60]!r}")
        return len(rows)
    # pacman -Qu exits 1 for both "no out-of-date packages" and sync-db failure;
    # only an entirely silent exit 1 is countable as zero.
    if exitcode == 1 and out == "" and err == "":
        return 0
    raise Cannot("E-SNAPSHOT-PENDING", SNAPSHOT,
                 f"pending query not countable: exit={exitcode} "
                 f"stdout_bytes={len(out)} stderr_bytes={len(err)}")


def parse_birth(head):
    parts = head.split()
    if len(parts) != 3:
        raise ValueError(head)
    date, clock, offset = parts
    clock, _, fraction = clock.partition(".")
    micros = (fraction or "0")[:6].ljust(6, "0")
    return datetime.strptime(f"{date}T{clock}.{micros}{offset}",
                             "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(timezone.utc)


def parse_sync(probe):
    if probe["exit"] != 0 or probe["stderr"] != "":
        raise Cannot("E-SNAPSHOT-SYNC", SNAPSHOT,
                     f"sync metadata query failed: exit={probe['exit']} "
                     f"stderr_bytes={len(probe['stderr'])}")
    stamps = []
    for line in probe["stdout"].splitlines():
        if not line.strip():
            continue
        fields = line.split("|")
        if len(fields) != 3 or not fields[2].strip().endswith(".db"):
            raise Cannot("E-SNAPSHOT-SYNC", SNAPSHOT, f"unexpected sync row {line[:60]!r}")
        head = fields[0].strip()
        try:
            stamp = parse_birth(head)
        except ValueError:
            raise Cannot("E-SNAPSHOT-SYNC", SNAPSHOT, f"unparseable birth stamp {head[:60]!r}")
        stamps.append(stamp)
    if not stamps:
        raise Cannot("E-SNAPSHOT-SYNC", SNAPSHOT, "sync rows absent")
    if len(set(stamps)) != 1:
        raise Cannot("E-SNAPSHOT-SYNC", SNAPSHOT, "sync database birth stamps differ")
    return stamps[0]


def parse_log(probe):
    if probe["exit"] != 0 or probe["stderr"] != "":
        raise Cannot("E-SNAPSHOT-LOG", SNAPSHOT,
                     f"libinput log query failed: exit={probe['exit']} "
                     f"stderr_bytes={len(probe['stderr'])}")
    found = None
    for line in probe["stdout"].splitlines():
        match = LOG_UPGRADE.search(line)
        if not match:
            continue
        stamp = LOG_STAMP.search(line)
        if not stamp:
            raise Cannot("E-SNAPSHOT-LOG", SNAPSHOT, "upgraded libinput line lacks a timestamp")
        try:
            when = datetime.strptime(stamp.group(1), "%Y-%m-%dT%H:%M:%S%z").astimezone(timezone.utc)
        except ValueError:
            raise Cannot("E-SNAPSHOT-LOG", SNAPSHOT, "unparseable log timestamp")
        found = (when, match.group(2))
    if found is None:
        raise Cannot("E-SNAPSHOT-LOG", SNAPSHOT, "no upgraded libinput line captured")
    return found


def check_hooks(probe):
    if probe["exit"] != 0 or probe["stderr"] != "":
        raise Cannot("E-SNAPSHOT-HOOKS", SNAPSHOT,
                     f"hook query failed: exit={probe['exit']} "
                     f"stderr_bytes={len(probe['stderr'])}")
    if not probe["stdout"].strip():
        raise Cannot("E-SNAPSHOT-HOOKS", SNAPSHOT, "hook stdout empty")


def boot_value_ok(value, stdout):
    sysroot_hit = re.search(r"^\s*\d+:.*/sysroot", stdout, re.M)
    if ("no /sysroot" in value) != (sysroot_hit is None):
        return False
    refs = HOOK_REF.findall(value)
    if re.search(r"^\s*\d+:", stdout, re.M) and not refs:
        return False
    sections = stdout.split("== ")[1:]
    for name, number in refs:
        linked = False
        for chunk in sections:
            header, _, body = chunk.partition("\n")
            if name in header and any(re.match(rf"^\s*{re.escape(number)}:", line)
                                      for line in body.splitlines()):
                linked = True
                break
        if not linked:
            return False
    return True


def record_findings(record, captured, probes, digest, packages, pending, birth, log_when,
                    log_to):
    findings, seen = [], {}
    site = RECORD

    def add(fid, detail, where=site):
        findings.append(Finding(fid, where, detail))

    if not isinstance(record, dict):
        raise Cannot("E-C2-SHAPE", RECORD, "top-level object required")
    for key in REQUIRED_KEYS:
        if key not in record:
            add("R15-C2-KEY", f"required key {key} absent")

    if record.get("schema") != SCHEMA:
        add("R15-C2-SCHEMA", f"schema {SCHEMA} required")

    ids = record.get("source_ids")
    if not isinstance(ids, list) or not ids:
        add("R15-C2-SOURCES", "non-empty source_ids array required")
    else:
        bad = [item for item in ids if not isinstance(item, str) or not SOURCE_ID.fullmatch(item)]
        if bad:
            add("R15-C2-SOURCES", f"non-S### source id {bad[0]!r}"[:120])
        elif len(set(ids)) != len(ids):
            add("R15-C2-SOURCES", "duplicate source id")
        else:
            missing = [item for item in REQUIRED_SOURCES if item not in ids]
            if missing:
                add("R15-C2-SOURCES", "missing required subset " + ",".join(missing))

    observed_raw = record.get("observed_at")
    observed = None
    if not isinstance(observed_raw, str) or not STAMP.fullmatch(observed_raw):
        add("R15-C2-OBSERVED-AT", "strict UTC YYYY-MM-DDTHH:MM:SSZ required")
    else:
        try:
            observed = parse_utc(observed_raw)
        except ValueError:
            add("R15-C2-OBSERVED-AT", "observed_at is not a calendar-valid stamp")
        else:
            if observed_raw != captured:
                add("R15-C2-CAPTURE-LINK",
                    f"observed_at {observed_raw} != snapshot captured_at {captured}")
            if observed < birth:
                add("R15-C2-CAPTURE-LINK", "observed_at precedes sync database birth")
            if observed < log_when + timedelta(seconds=1):
                add("R15-C2-CAPTURE-FLOOR", "observed_at must follow the logged libinput upgrade")
    if "snapshot_captured_at" in record and record.get("snapshot_captured_at") != observed_raw:
        add("R15-C2-CAPTURE-LINK", "snapshot_captured_at differs from observed_at")

    if record.get("evidence_path") != SNAPSHOT:
        add("R15-C2-EVIDENCE-PATH", f"evidence_path must be exactly {SNAPSHOT}")
    declared = record.get("snapshot_sha256")
    if not isinstance(declared, str) or not HEX64.fullmatch(declared):
        add("R15-C2-DIGEST", "lowercase 64-hex snapshot_sha256 required")
    elif declared != digest:
        add("R15-C2-DIGEST", "snapshot_sha256 differs from raw snapshot bytes")

    if record.get("decision") != DECISION:
        add("R15-C2-DECISION", f"decision must be {DECISION}")
    limits = record.get("limits")
    if (not isinstance(limits, list) or not limits
            or any(not isinstance(item, str) or not item.strip() for item in limits)):
        add("R15-C2-LIMITS", "non-empty string limits required")

    observations = record.get("observations")
    if not isinstance(observations, list) or not observations:
        add("R15-C2-OBSERVATIONS", "non-empty observations array required")
        return findings, seen
    for index, item in enumerate(observations):
        where = f"{RECORD}:observations[{index}]"
        if not isinstance(item, dict):
            add("R15-C2-OBSERVATION", "object required", where)
            continue
        key = item.get("command_key")
        if not isinstance(key, str) or key not in PROBE_KEYS:
            add("R15-C2-OBSERVATION", f"unknown command_key {key!r}"[:120], where)
            continue
        if key in seen:
            add("R15-C2-OBSERVATION-DUPLICATE", f"duplicate command_key {key}", where)
            continue
        seen[key] = item
        if item.get("probe_key") != key:
            add("R15-C2-OBSERVATION-LINK", "probe_key must equal command_key", where)
        for field in ("value", "meaning"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                add("R15-C2-OBSERVATION", f"{field} must be a non-empty string", where)
        exitcode = item.get("exit")
        if isinstance(exitcode, bool) or not isinstance(exitcode, int):
            add("R15-C2-OBSERVATION-EXIT", "plain int exit required", where)
        elif exitcode != probes[key]["exit"]:
            add("R15-C2-OBSERVATION-EXIT", "exit differs from snapshot probe", where)
        expected_empty = probes[key]["stderr"] == ""
        if item.get("stderr_empty") is not expected_empty:
            add("R15-C2-OBSERVATION-STDERR", "stderr_empty differs from snapshot probe", where)
    for key in PROBE_KEYS:
        if key not in seen:
            add("R15-C2-OBSERVATION-MISSING", f"no observation for probe {key}")

    def value_issue(key, detail):
        add("R15-C2-VALUE", f"{key}: {detail}", f"{RECORD}:{key}")

    item = seen.get("package_versions")
    if item is not None and isinstance(item.get("value"), str):
        expected = {f"{name} {version}" for name, version in packages.items()}
        segments = {part.strip() for part in re.split(r"[;\n]", item["value"]) if part.strip()}
        if segments != expected:
            value_issue("package_versions", "value segments differ from snapshot rows")
    item = seen.get("pending_updates")
    if item is not None and isinstance(item.get("value"), str):
        if item["value"].strip() != str(pending):
            value_issue("pending_updates",
                        f"declared {item['value'].strip()[:32]!r} != measured {pending}")
    item = seen.get("sync_metadata")
    if item is not None and isinstance(item.get("value"), str):
        if item["value"].strip() != utc_text(birth):
            value_issue("sync_metadata", "declared stamp differs from snapshot birth")
    item = seen.get("libinput_log")
    if item is not None and isinstance(item.get("value"), str):
        if item["value"].strip() != utc_text(log_when):
            value_issue("libinput_log", "declared stamp differs from last logged upgrade")
    if log_to != packages["libinput"]:
        add("R15-C2-LOG-INSTALL", "logged upgrade target differs from installed libinput",
            f"{RECORD}:libinput_log")
    item = seen.get("boot_hook_mentions")
    if item is not None and isinstance(item.get("value"), str):
        if not boot_value_ok(item["value"], probes["boot_hook_mentions"]["stdout"]):
            value_issue("boot_hook_mentions", "declared refs differ from snapshot hook lines")
    return findings, seen


def assess(record_raw, snapshot_raw, digest):
    snap_doc = load_json(snapshot_raw, SNAPSHOT, "E-SNAPSHOT")
    captured, probes = validate_snapshot(snap_doc)
    packages = parse_packages(probes["package_versions"])
    pending = parse_pending(probes["pending_updates"])
    birth = parse_sync(probes["sync_metadata"])
    log_when, log_to = parse_log(probes["libinput_log"])
    check_hooks(probes["boot_hook_mentions"])
    record = load_json(record_raw, RECORD, "E-C2")
    findings, _ = record_findings(record, captured, probes, digest, packages, pending, birth,
                                  log_when, log_to)
    ids = record.get("source_ids") if isinstance(record.get("source_ids"), list) else []
    sources = [item for item in ids if isinstance(item, str)]
    observed = record.get("observed_at") if isinstance(record.get("observed_at"), str) else None
    decision = record.get("decision") if isinstance(record.get("decision"), str) else None
    return Assessment(findings, 0 if findings else 1, pending,
                      probes["pending_updates"]["exit"], packages["libinput"], sources,
                      observed, captured, decision, digest)


def emit(revision, status, findings, assessment=None, digest=None):
    payload = {
        "status": status,
        "revision": revision,
        "record_count": assessment.record_count if assessment else 0,
        "pending_count": assessment.pending if assessment else None,
        "pending_exit": assessment.pending_exit if assessment else None,
        "installed_libinput": assessment.installed if assessment else None,
        "installed_libinput_kind": "pacman -Q database version; not a running-process mapping",
        "health": "not_assessed",
        "source_ids": assessment.sources if assessment else [],
        "observed_at": assessment.observed if assessment else None,
        "snapshot_captured_at": assessment.captured if assessment else None,
        "declared_decision": assessment.decision if assessment else None,
        "snapshot_sha256": assessment.digest if assessment else digest,
        "findings": [{"id": f.id, "site": f.site, "detail": f.detail}
                     for f in sorted(findings, key=lambda f: (f.id, f.site, f.detail))],
    }
    print(json.dumps(payload, sort_keys=True))
    return PASS if status in ("COUNTED", "ABSENT") else CANNOT


def git(repo, *args):
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C"})
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(repo), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=30)
    except subprocess.TimeoutExpired:
        raise Cannot("E-GIT-TIMEOUT", "git", "git command exceeded 30s")
    except OSError as exc:
        raise Cannot("E-GIT-FAILED", "git", str(exc)[:120])


def resolve(repo, rev):
    if not REV.fullmatch(rev):
        raise Cannot("E-REVISION-INVALID", "revision", "HEAD or 4-64 hex commit required")
    proc = git(repo, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if proc.returncode != 0:
        raise Cannot("E-REVISION-INVALID", "revision", "commit not found")
    return proc.stdout.decode("ascii", "replace").strip()


def read_git(repo, commit, path):
    proc = git(repo, "show", f"{commit}:{path}")
    if proc.returncode == 0:
        return proc.stdout
    error = proc.stderr.decode("utf-8", "replace")
    if re.search(r"does not exist|exists on disk, but not in|not in '", error, re.I):
        return None
    raise Cannot("E-GIT-READ", path, error.strip()[:120] or "git show failed")


def read_tree(repo, path):
    target = repo / path
    if not target.exists():
        return None
    if not target.is_file():
        raise Cannot("E-READ", path, "not a regular file")
    try:
        return target.read_bytes()
    except OSError as exc:
        raise Cannot("E-READ", path, str(exc)[:120])


def load(rev):
    if rev is None:
        return "worktree", read_tree(ROOT, RECORD), read_tree(ROOT, SNAPSHOT)
    commit = resolve(ROOT, rev)
    return commit, read_git(ROOT, commit, RECORD), read_git(ROOT, commit, SNAPSHOT)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Read-only round-15 update-safety recheck counting probe.",
        exit_on_error=False)
    parser.add_argument("--revision", metavar="REV",
                        help="HEAD or a 4-64 hex commit; default worktree")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        if not exc.code:
            return 0
        return emit("worktree", "CANNOT_EVALUATE", [Finding("E-CLI", "cli", "invalid arguments")])
    except argparse.ArgumentError:
        return emit("worktree", "CANNOT_EVALUATE", [Finding("E-CLI", "cli", "invalid arguments")])
    revision, digest = args.revision or "worktree", None
    try:
        revision, record_raw, snapshot_raw = load(args.revision)
        if record_raw is None and snapshot_raw is None:
            return emit(revision, "ABSENT", [])
        if record_raw is None:
            raise Cannot("E-C2-RECORD-MISSING", RECORD, "record absent while snapshot exists")
        if snapshot_raw is None:
            raise Cannot("E-SNAPSHOT-MISSING", SNAPSHOT, "snapshot absent while record exists")
        digest = hashlib.sha256(snapshot_raw).hexdigest()
        assessment = assess(record_raw, snapshot_raw, digest)
    except Cannot as exc:
        return emit(revision, "CANNOT_EVALUATE", [Finding(exc.fid, exc.site, exc.detail)],
                    digest=digest)
    except Exception as exc:  # no traceback: unreadable/invalid input is CANNOT
        return emit(revision, "CANNOT_EVALUATE", [Finding("E-INTERNAL", "probe", str(exc)[:120])],
                    digest=digest)
    status = "COUNTED" if not assessment.findings else "CANNOT_EVALUATE"
    return emit(revision, status, assessment.findings, assessment)


if __name__ == "__main__":
    sys.exit(main())
