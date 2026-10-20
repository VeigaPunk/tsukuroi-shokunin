#!/usr/bin/env python3
"""Read-only round-15 update-safety recheck counting probe.

One committed C2 record and one captured host snapshot, both read from the same
revision. Exit 0 when the pair is absent (record_count 0, "before") or the
record is internally consistent with the snapshot (record_count 1); exit 2 when
the revision is invalid, unlanded or unpushed, or the input is malformed,
incomplete or contradicts the snapshot. Absence is a probe count, never a
safety pass. This is not a truth gate: it issues no health, repair, causality
or upgrade-clearance verdict.

No writes. No host-state command is executed: the snapshot is data, and
--revision only reads git blobs with read-only plumbing (GIT_OPTIONAL_LOCKS=0).
A revision run additionally requires the resolved commit to descend from
refs/heads/<branch> (default master) and, when that ref exists, from
refs/remotes/origin/<branch>; the payload carries branch and branch_tip.
--selftest writes only under a mktemp git sandbox.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
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
REV = re.compile(r"^[0-9a-fA-F]{7,64}$")
BRANCH = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
DEFAULT_BRANCH = "master"
SELF = Path(__file__).resolve()
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
    def __init__(self, fid, site, detail, revision=None, tip=None):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail
        self.revision, self.tip = revision, tip


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


def emit(revision, status, findings, assessment=None, digest=None, branch=DEFAULT_BRANCH,
         branch_tip=None):
    payload = {
        "status": status,
        "revision": revision,
        "branch": branch,
        "branch_tip": branch_tip,
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
        raise Cannot("E-REVISION-INVALID", "revision", "7-64 hex commit required")
    proc = git(repo, "rev-parse", "--verify", "--quiet", f"{rev.lower()}^{{commit}}")
    if proc.returncode != 0:
        raise Cannot("E-REVISION-INVALID", "revision", "commit not found")
    return proc.stdout.decode("ascii", "replace").strip()


def ref_commit(repo, ref):
    proc = git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("ascii", "replace").strip() or None


def branch_ok(name):
    if not BRANCH.fullmatch(name):
        return False
    if ".." in name or "@{" in name or "//" in name or name.endswith("/"):
        return False
    return all(part and not part.startswith(".") and not part.endswith(".lock")
               for part in name.split("/"))


def bind(repo, commit, branch):
    """Require commit to be a landed (and, when origin exists, pushed) ancestor."""
    if not branch_ok(branch):
        raise Cannot("E-REVISION-INVALID", "branch", "invalid branch name",
                     revision=commit)
    if git(repo, "merge-base", "--is-ancestor", commit,
           f"refs/heads/{branch}").returncode != 0:
        raise Cannot("E-REVISION-NOT-LANDED", "revision",
                     f"not an ancestor of refs/heads/{branch}", revision=commit)
    tip = ref_commit(repo, f"refs/heads/{branch}")
    if tip is None:
        raise Cannot("E-REVISION-NOT-LANDED", "revision",
                     f"refs/heads/{branch} tip unreadable", revision=commit)
    if ref_commit(repo, f"refs/remotes/origin/{branch}") is not None:
        if git(repo, "merge-base", "--is-ancestor", commit,
               f"refs/remotes/origin/{branch}").returncode != 0:
            raise Cannot("E-REVISION-NOT-PUSHED", "revision",
                         f"not an ancestor of refs/remotes/origin/{branch}",
                         revision=commit, tip=tip)
    return tip


def branch_tip(repo, branch):
    if not branch_ok(branch):
        return None
    try:
        return ref_commit(repo, f"refs/heads/{branch}")
    except Cannot:
        return None


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


def load(rev, branch):
    if rev is None:
        return ("worktree", read_tree(ROOT, RECORD), read_tree(ROOT, SNAPSHOT),
                branch_tip(ROOT, branch))
    commit = resolve(ROOT, rev)
    tip = bind(ROOT, commit, branch)
    return commit, read_git(ROOT, commit, RECORD), read_git(ROOT, commit, SNAPSHOT), tip


def sandbox_git(repo, *args):
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C",
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
    proc = subprocess.run(["git", "--no-pager", "-C", str(repo), *args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
                          timeout=30)
    if proc.returncode != 0:
        raise RuntimeError(f"git {args[0]} failed: "
                           f"{proc.stderr.decode('utf-8', 'replace').strip()[:200]}")
    return proc.stdout.decode("ascii", "replace").strip()


def sandbox_commit(repo, message):
    sandbox_git(repo, "-c", "user.name=selftest", "-c", "user.email=selftest@example.invalid",
                "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", message)
    return sandbox_git(repo, "rev-parse", "HEAD")


def selftest():
    """Hermetic suite: in-memory record fixtures plus a mktemp git sandbox."""
    root, passed, total, failures = None, 0, 0, []

    def case(name, problems):
        nonlocal passed, total
        total += 1
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))
        else:
            passed += 1

    try:
        root = Path(tempfile.mkdtemp(prefix="tsukuroi-measure-selftest."))
        repo = root
        sandbox_git(repo, "init", "-q")
        sandbox_git(repo, "symbolic-ref", "HEAD", "refs/heads/master")
        (repo / "a.txt").write_text("0\n")
        sandbox_git(repo, "add", "a.txt")
        base = sandbox_commit(repo, "base")
        (repo / "a.txt").write_text("1\n")
        sandbox_git(repo, "add", "a.txt")
        tip = sandbox_commit(repo, "tip")
        sandbox_git(repo, "checkout", "-q", "--detach", base)
        (repo / "b.txt").write_text("side\n")
        sandbox_git(repo, "add", "b.txt")
        unlanded = sandbox_commit(repo, "unlanded")
        sandbox_git(repo, "checkout", "-q", "master")
        (repo / "tools").mkdir()
        tool = repo / "tools" / "measure-update-recheck.py"
        tool.write_bytes(SELF.read_bytes())

        def run(*args):
            proc = subprocess.run([sys.executable, str(tool), *args],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  cwd=str(repo), timeout=120)
            payload = None
            if proc.stdout.strip():
                try:
                    payload = json.loads(proc.stdout.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    payload = None
            return proc.returncode, payload, proc.stderr.decode("utf-8", "replace")[:200]

        def revision_case(name, argv, want_exit, want_ids, want_revision=None,
                          want_branch=DEFAULT_BRANCH, want_tip=None, want_status=None):
            code, payload, err = run(*argv)
            problems = []
            if code != want_exit:
                problems.append(f"exit={code}/{want_exit} stderr={err!r}")
            if payload is None:
                problems.append("stdout is not JSON")
            else:
                got = {item.get("id") for item in payload.get("findings", [])
                       if isinstance(item, dict)}
                if got != want_ids:
                    problems.append("ids=" + ",".join(sorted(got))
                                    + " want=" + ",".join(sorted(want_ids)))
                if want_revision is not None and payload.get("revision") != want_revision:
                    problems.append(f"revision={payload.get('revision')!r}/{want_revision}")
                if payload.get("branch") != want_branch:
                    problems.append(f"branch={payload.get('branch')!r}/{want_branch}")
                if want_tip is not None and payload.get("branch_tip") != want_tip:
                    problems.append(f"branch_tip={payload.get('branch_tip')!r}/{want_tip}")
                if want_status is not None and payload.get("status") != want_status:
                    problems.append(f"status={payload.get('status')!r}/{want_status}")
            case(name, problems)

        revision_case("head-rejected", ("--revision", "HEAD"), CANNOT,
                      {"E-REVISION-INVALID"}, want_revision="HEAD")
        revision_case("short-hex-rejected", ("--revision", tip[:6]), CANNOT,
                      {"E-REVISION-INVALID"}, want_revision=tip[:6])
        revision_case("landed-tip-accepted", ("--revision", tip), PASS, set(),
                      want_revision=tip, want_tip=tip, want_status="ABSENT")
        revision_case("unlanded-rejected", ("--revision", unlanded), CANNOT,
                      {"E-REVISION-NOT-LANDED"}, want_revision=unlanded)
        revision_case("unknown-branch-rejected", ("--revision", tip, "--branch", "absent"),
                      CANNOT, {"E-REVISION-NOT-LANDED"}, want_revision=tip,
                      want_branch="absent")
        sandbox_git(repo, "update-ref", "refs/remotes/origin/master", base)
        revision_case("not-pushed-rejected", ("--revision", tip), CANNOT,
                      {"E-REVISION-NOT-PUSHED"}, want_revision=tip, want_tip=tip)
        revision_case("worktree-default", (), PASS, set(), want_revision="worktree",
                      want_tip=tip, want_status="ABSENT")

        def fixture():
            captured = "2026-10-20T07:44:39Z"
            birth = "2026-10-18T17:11:00Z"
            logged = "2026-10-20T07:25:17Z"
            packages = ("libinput 1.32.0-1", "libinput-tools 1.32.0-1",
                        "mkinitcpio 41.1-1", "systemd 261.2-1")

            def probe(command, stdout):
                return {"command": command, "exit": 0, "stdout": stdout, "stderr": ""}

            snap = {
                "captured_at": captured,
                "probes": {
                    "package_versions": probe(
                        "pacman -Q libinput libinput-tools mkinitcpio systemd",
                        "".join(row + "\n" for row in packages)),
                    "pending_updates": probe("pacman -Qu", "a 1-1 -> 2-1\nb 3-1 -> 4-1\n"),
                    "sync_metadata": probe(
                        "stat -c '%w|%z|%n' /var/lib/pacman/sync/*.db",
                        "2026-10-18 14:11:00.026135178 -0300|"
                        "2026-10-18 14:11:00.921131413 -0300|"
                        "/var/lib/pacman/sync/core.db\n"),
                    "libinput_log": probe(
                        "grep -nE 'libinput' /var/log/pacman.log",
                        "2429:[2026-10-20T04:25:16-0300] [PACMAN] Running\n"
                        "2432:[2026-10-20T04:25:17-0300] [ALPM] "
                        "upgraded libinput (1.31.3-1 -> 1.32.0-1)\n"),
                    "boot_hook_mentions": probe(
                        "for f in hooks; do echo \"== $f\"; done",
                        "== /usr/lib/initcpio/hooks/btrfs-overlayfs exists\n"
                        '4:\troot_mnt="/new_root"\n'
                        "== /usr/lib/initcpio/hooks/plymouth exists\n"
                        "11:  plymouth update-root-fs --new-root-dir=/new_root\n"),
                },
            }
            snap_raw = json.dumps(snap, indent=1, sort_keys=True).encode()
            digest = hashlib.sha256(snap_raw).hexdigest()
            observations = [
                ("package_versions", "; ".join(packages), "installed database versions"),
                ("pending_updates", "2", "pending rows in the captured metadata"),
                ("sync_metadata", birth, "sync database birth stamp"),
                ("libinput_log", logged, "last logged libinput upgrade"),
                ("boot_hook_mentions",
                 "/new_root (btrfs-overlayfs:4, plymouth:11); no /sysroot",
                 "hook root references"),
            ]
            record = {
                "schema": SCHEMA,
                "source_ids": list(REQUIRED_SOURCES),
                "observed_at": captured,
                "snapshot_captured_at": captured,
                "evidence_path": SNAPSHOT,
                "snapshot_sha256": digest,
                "observations": [
                    {"command_key": key, "probe_key": key, "exit": 0,
                     "stderr_empty": True, "value": value, "meaning": meaning}
                    for key, value, meaning in observations],
                "decision": DECISION,
                "limits": ["selftest fixture; no host state was read"],
            }
            return record, snap_raw, digest

        def assess_case(name, mutate=None, want_ids=(), want_count=1):
            record, snap_raw, digest = fixture()
            if mutate is not None:
                mutate(record)
            encoded = json.dumps(record, sort_keys=True).encode()
            try:
                result = assess(encoded, snap_raw, digest)
            except Cannot as exc:
                case(name, [f"cannot {exc.fid}: {exc.detail}"])
                return
            got = {finding.id for finding in result.findings}
            problems = []
            if got != set(want_ids):
                problems.append("ids=" + ",".join(sorted(got))
                                + " want=" + ",".join(sorted(want_ids)))
            if result.record_count != want_count:
                problems.append(f"count={result.record_count}/{want_count}")
            case(name, problems)

        def mutate_pending(record):
            for item in record["observations"]:
                if item["command_key"] == "pending_updates":
                    item["value"] = "3"

        def mutate_boot(record):
            for item in record["observations"]:
                if item["command_key"] == "boot_hook_mentions":
                    item["value"] = "/sysroot (btrfs-overlayfs:4, plymouth:11); no /new_root"

        def mutate_observed(record):
            record["observed_at"] = "2026-10-20T07:44:40Z"
            record["snapshot_captured_at"] = "2026-10-20T07:44:40Z"

        assess_case("fixture-clean")
        assess_case("fixture-digest-mismatch",
                    lambda record: record.update(snapshot_sha256="0" * 64),
                    ("R15-C2-DIGEST",), 0)
        assess_case("fixture-pending-value", mutate_pending, ("R15-C2-VALUE",), 0)
        assess_case("fixture-boot-sysroot", mutate_boot, ("R15-C2-VALUE",), 0)
        assess_case("fixture-duplicate-observation",
                    lambda record: record["observations"].append(
                        dict(record["observations"][0])),
                    ("R15-C2-OBSERVATION-DUPLICATE",), 0)
        assess_case("fixture-observed-mismatch", mutate_observed,
                    ("R15-C2-CAPTURE-LINK",), 0)
    except Exception as exc:  # sandbox unavailable or fixture bug: selftest fails
        print(f"MEASURE_UPDATE_RECHECK_SELFTEST: FAIL ({total} cases, {passed} passed, "
              f"sandbox {type(exc).__name__}: {str(exc)[:160]})")
        return 1
    finally:
        if root is not None:
            shutil.rmtree(root, ignore_errors=True)
    if failures:
        print(f"MEASURE_UPDATE_RECHECK_SELFTEST: FAIL ({total} cases, {passed} passed)")
        print("\n".join("  " + item for item in failures))
        return 1
    print(f"MEASURE_UPDATE_RECHECK_SELFTEST: PASS ({total} cases, {passed} passed, 0 failed)")
    return PASS


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Read-only round-15 update-safety recheck counting probe.",
        exit_on_error=False)
    parser.add_argument("--revision", metavar="REV",
                        help="7-64 hex commit bound to --branch; default worktree")
    parser.add_argument("--branch", metavar="NAME", default=DEFAULT_BRANCH,
                        help=f"landed branch the revision must descend from "
                             f"(default {DEFAULT_BRANCH})")
    parser.add_argument("--selftest", action="store_true", help="hermetic fixture suite")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        if not exc.code:
            return 0
        return emit("worktree", "CANNOT_EVALUATE", [Finding("E-CLI", "cli", "invalid arguments")])
    except argparse.ArgumentError:
        return emit("worktree", "CANNOT_EVALUATE", [Finding("E-CLI", "cli", "invalid arguments")])
    if args.selftest:
        if args.revision is not None:
            return emit("worktree", "CANNOT_EVALUATE",
                        [Finding("E-CLI", "cli", "--selftest and --revision are exclusive")],
                        branch=args.branch)
        return selftest()
    revision, digest, branch, tip = args.revision or "worktree", None, args.branch, None
    try:
        revision, record_raw, snapshot_raw, tip = load(args.revision, branch)
        if record_raw is None and snapshot_raw is None:
            return emit(revision, "ABSENT", [], branch=branch, branch_tip=tip)
        if record_raw is None:
            raise Cannot("E-C2-RECORD-MISSING", RECORD, "record absent while snapshot exists")
        if snapshot_raw is None:
            raise Cannot("E-SNAPSHOT-MISSING", SNAPSHOT, "snapshot absent while record exists")
        digest = hashlib.sha256(snapshot_raw).hexdigest()
        assessment = assess(record_raw, snapshot_raw, digest)
    except Cannot as exc:
        return emit(exc.revision or revision, "CANNOT_EVALUATE",
                    [Finding(exc.fid, exc.site, exc.detail)], digest=digest,
                    branch=branch, branch_tip=exc.tip if exc.tip is not None else tip)
    except Exception as exc:  # no traceback: unreadable/invalid input is CANNOT
        return emit(revision, "CANNOT_EVALUATE", [Finding("E-INTERNAL", "probe", str(exc)[:120])],
                    digest=digest, branch=branch, branch_tip=tip)
    status = "COUNTED" if not assessment.findings else "CANNOT_EVALUATE"
    return emit(revision, status, assessment.findings, assessment, branch=branch,
                branch_tip=tip)


if __name__ == "__main__":
    sys.exit(main())
