#!/usr/bin/env python3
"""Narrow, read-only round-17 freshness-recheck gate.

Bounded conformance, never host truth and never an update-safety verdict:
every record of corpus/knowledge/freshness-recheck-r17.json (schema
tsukuroi-freshness-recheck-v1) claims that one current-use observation in a
knowledge file went stale after the 2026-10-20 09:15 full upgrade and was
answered by an appended dated notice.  At --revision the registry must be
an object with exactly {schema, records}, records must be an array of
objects with exactly the eight declared string fields, ids must be
R17-FRESH-NN and unique, and paths must be lane-relative .md files under
corpus/knowledge/.  For each record the target file must still start with
its bytes at baseline 6923fe0b…(append-only history), baseline_quote must
be an exact substring of the baseline file and still be present, the
notice_heading must be one Markdown heading line occurring exactly once
after the baseline boundary and never at baseline, that notice section
must contain observed_now and capture_ref, and the cited capture line (a
lane round-17 capture at that same revision) must contain capture_quote.
Missing target files and unreadable captures are findings, not passes.

--registry-from <hex> compares that revision's records against the
--revision target files and reports STALE-UNFLAGGED for every record whose
baseline_quote is present while its notice_heading is absent.  Running
`--revision <baseline> --registry-from <landing>` therefore shows the
baseline defect is real; in that mode resolved_records counts records that
are not stale and the exit status is 1 when any defect is demonstrated.

Revision binding: --revision and --registry-from admit only 7-64 hex
(HEAD, @ and refs are E-REVISION-INVALID), must resolve to commits that
are ancestors of refs/heads/<branch> (default master, else
E-REVISION-NOT-LANDED), and when refs/remotes/origin/<branch> exists must
also be ancestors of it (else E-REVISION-NOT-PUSHED).  JSON carries
revision, branch, branch_tip, resolved_records and record_count.

Exit 0 pass, 1 failed, 2 could-not-evaluate.  No writes, no network, no
host queries.  --selftest is hermetic (in-memory fixtures plus one mktemp
git repository for the binding contract).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import namedtuple
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
ROOT = Path(__file__).resolve().parents[1]
BASE = "6923fe0bd3add04fc90f3bc3522895b27cf44bbe"
REGISTRY = "corpus/knowledge/freshness-recheck-r17.json"
SCHEMA = "tsukuroi-freshness-recheck-v1"
CAPTURES = (".ufo/waves/round-17/l1-capture/boot-chain-capture.txt",
            ".ufo/waves/round-17/l1-capture/fresh-capture.txt")
REV = re.compile(r"^[0-9a-fA-F]{7,64}$")
BRANCH = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,200}$")
ID = re.compile(r"^R17-FRESH-\d{2}$")
PATH = re.compile(r"^corpus/knowledge/[A-Za-z0-9._-]+\.md$")
HEADING = re.compile(r"^#{1,6} \S.*$")
FIELDS = ("id", "path", "baseline_quote", "stale_reason", "observed_now",
          "capture_ref", "capture_quote", "notice_heading")
SCOPE = ("dated freshness re-verification only; historical captures stay historical; "
         "no package, service or boot action is authorized")

Finding = namedtuple("Finding", "id site detail")
DocSet = namedtuple("DocSet", "registry targets bases captures compare")
Result = namedtuple("Result", "code findings resolved total stale")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def heading_hits(text, heading):
    """Line indexes where the exact heading appears outside fenced code."""
    out, fence = [], False
    for index, line in enumerate(text.splitlines()):
        stripped = line.strip()
        if stripped.startswith("```"):
            fence = not fence
            continue
        if not fence and line.rstrip() == heading:
            out.append(index)
    return out


def region(lines, start):
    """End index (exclusive) of the section opened at heading line start."""
    fence = False
    for index in range(start + 1, len(lines)):
        stripped = lines[index].strip()
        if stripped.startswith("```"):
            fence = not fence
            continue
        if not fence and stripped.startswith("#"):
            return index
    return len(lines)


def suffix_heading_line(text, heading, start):
    """Line index of the unique outside-fence heading at or after start."""
    offset, fence = 0, False
    for index, line in enumerate(text.splitlines(keepends=True)):
        stripped = line.strip()
        if stripped.startswith("```"):
            fence = not fence
        elif not fence and offset >= start and line.rstrip() == heading:
            return index
        offset += len(line)
    return None


def dedupe(findings):
    return [Finding(*key) for key in
            sorted({(f.id, f.site, f.detail) for f in findings})]


def registry_issues(doc):
    """Schema/field findings plus the id-mapped records and declared count."""
    out = []
    if not isinstance(doc, dict):
        return ([Finding("R17-FRESH-SCHEMA", REGISTRY, "top-level object required")],
                {}, False, 0)
    if doc.get("schema") != SCHEMA:
        out.append(Finding("R17-FRESH-SCHEMA", REGISTRY,
                           f"schema {SCHEMA} required"))
    extra = sorted(set(doc) - {"schema", "records"})
    if extra:
        out.append(Finding("R17-FRESH-SCHEMA", REGISTRY,
                           "extra top-level keys=" + ",".join(extra)))
    records = doc.get("records")
    if not isinstance(records, list):
        out.append(Finding("R17-FRESH-SCHEMA", REGISTRY, "records array required"))
        return out, {}, False, 0
    declared = len(records)
    if not records:
        out.append(Finding("R17-FRESH-EMPTY", REGISTRY,
                           "records must be a non-empty array"))
    structural = not any(f.id == "R17-FRESH-SCHEMA" for f in out)
    counts = {}
    for obj in records:
        if isinstance(obj, dict) and isinstance(obj.get("id"), str):
            counts[obj["id"]] = counts.get(obj["id"], 0) + 1
    for rid, occurrences in sorted(counts.items()):
        if occurrences > 1:
            out.append(Finding("R17-FRESH-ID", f"{REGISTRY}:{rid}",
                               f"duplicate id occurrences={occurrences}"))
    mapped = {}
    for index, obj in enumerate(records):
        site = f"{REGISTRY}:{index}"
        if not isinstance(obj, dict):
            out.append(Finding("R17-FRESH-FIELD", site, "record is not an object"))
            continue
        rid = obj.get("id")
        if isinstance(rid, str) and rid:
            site = f"{REGISTRY}:{rid}"
        missing = [f for f in FIELDS
                   if not isinstance(obj.get(f), str) or not obj[f].strip()]
        extra_fields = sorted(set(obj) - set(FIELDS))
        if missing or extra_fields:
            out.append(Finding("R17-FRESH-FIELD", site,
                               ("missing=" + ",".join(missing) if missing else "")
                               + (" extra=" + ",".join(extra_fields)
                                  if extra_fields else "")))
            continue
        if not ID.fullmatch(rid):
            out.append(Finding("R17-FRESH-ID", site,
                               "id must be R17-FRESH-NN (two digits)"))
            continue
        if counts[rid] > 1:
            continue
        if not PATH.fullmatch(obj["path"]):
            out.append(Finding("R17-FRESH-PATH", site,
                               "path must be corpus/knowledge/<name>.md"))
            continue
        mapped[rid] = obj
    return out, mapped, structural, declared


def record_issues(rid, obj, docs):
    """Append-only history, quote, notice, and capture-line findings."""
    out = []
    path = obj["path"]

    def add(fid, where, detail):
        out.append(Finding(fid, where, detail))

    text, base = docs.targets.get(path), docs.bases.get(path)
    if text is None:
        add("R17-FRESH-TARGET-MISSING", path, "file absent at --revision")
        return out
    if base is None:
        add("R17-FRESH-BASELINE-MISSING", path, "file absent at baseline")
        return out
    quote, heading = obj["baseline_quote"], obj["notice_heading"]
    if not text.startswith(base):
        add("R17-FRESH-HISTORY", path,
            "bytes before the appended notice differ from baseline")
    if quote not in base:
        add("R17-FRESH-QUOTE-BASELINE", path,
            "baseline_quote is not a substring of the baseline file")
    if quote not in text:
        add("R17-FRESH-QUOTE", path, "baseline_quote no longer present at --revision")
    if "\n" in heading or not HEADING.fullmatch(heading):
        add("R17-FRESH-NOTICE-FORM", path,
            "notice_heading must be one Markdown heading line")
        return out
    if heading_hits(base, heading):
        add("R17-FRESH-NOTICE-BASE", path, "notice_heading already present at baseline")
    appended = text.startswith(base)
    suffix = text[len(base):] if appended else text
    after = heading_hits(suffix, heading)
    if not after:
        add("R17-FRESH-NOTICE", path,
            "notice heading absent from the appended suffix")
    elif len(after) > 1:
        add("R17-FRESH-NOTICE-DUP", path,
            f"notice heading occurrences after baseline={len(after)}")
    if after:
        start = suffix_heading_line(text, heading, len(base) if appended else 0)
        lines = text.splitlines()
        section = ("\n".join(lines[start:region(lines, start)])
                   if start is not None else "")
        missing = [name for name, value in
                   (("observed_now", obj["observed_now"]),
                    ("capture_ref", obj["capture_ref"]))
                   if value not in section]
        if missing:
            add("R17-FRESH-NOTICE-CONTENT", path,
                "notice section lacks " + ",".join(missing))
    ref = obj["capture_ref"]
    cap_path, sep, line_text = ref.rpartition(":")
    if not sep or not line_text.isdigit() or int(line_text) < 1:
        add("R17-FRESH-CAPTURE-REF", path,
            "capture_ref must be <lane-relative capture path>:<positive line>")
    elif cap_path not in CAPTURES:
        add("R17-FRESH-CAPTURE-REF", path,
            "capture path is not a lane round-17 capture")
    else:
        capture = docs.captures.get(cap_path)
        if capture is None:
            add("R17-FRESH-CAPTURE-MISSING", cap_path,
                "capture file absent at --revision")
        else:
            lines = capture.splitlines()
            line_number = int(line_text)
            if line_number > len(lines):
                add("R17-FRESH-CAPTURE-LINE", cap_path,
                    f"line {line_number} beyond EOF={len(lines)}")
            elif obj["capture_quote"] not in lines[line_number - 1]:
                add("R17-FRESH-CAPTURE-QUOTE", cap_path,
                    "capture_quote is not a substring of the cited line")
    return out


def evaluate(docs):
    if docs.registry is None:
        if docs.compare:
            return Result(CANNOT, [Finding("E-REGISTRY-MISSING", REGISTRY,
                                           "registry absent at --registry-from")],
                          0, 0, None)
        return Result(FAIL, [Finding("R17-FRESH-MISSING", REGISTRY,
                                     "registry absent at --revision")], 0, 0, None)
    try:
        doc = json.loads(docs.registry)
    except json.JSONDecodeError as exc:
        return Result(CANNOT, [Finding("E-REGISTRY-PARSE", REGISTRY,
                                       str(exc)[:100])], 0, 0, None)
    findings, records, structural, declared = registry_issues(doc)
    if not structural:
        return Result(FAIL, dedupe(findings), 0, declared,
                      0 if docs.compare else None)
    if docs.compare:
        resolved = stale = 0
        for rid in sorted(records):
            obj = records[rid]
            text = docs.targets.get(obj["path"])
            if text is None:
                findings.append(Finding("R17-FRESH-TARGET-MISSING", obj["path"],
                                        "file absent at --revision"))
                continue
            quote, heading = obj["baseline_quote"], obj["notice_heading"]
            if quote in text and not heading_hits(text, heading):
                stale += 1
                findings.append(Finding(
                    "STALE-UNFLAGGED", obj["path"],
                    f"{rid}: baseline quote present and notice heading absent"))
            elif quote in text:
                resolved += 1
        return Result(FAIL if findings else PASS, dedupe(findings),
                      resolved, declared, stale)
    resolved = 0
    for rid in sorted(records):
        issues = record_issues(rid, records[rid], docs)
        findings += issues
        if not issues:
            resolved += 1
    findings = dedupe(findings)
    return Result(FAIL if findings else PASS, findings, resolved, declared, None)


def emit(result, revision, branch, branch_tip):
    status = {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[result.code]
    payload = {"status": status,
               "revision": revision,
               "branch": branch,
               "branch_tip": branch_tip,
               "resolved_records": result.resolved,
               "record_count": result.total,
               "scope": SCOPE,
               "findings": [{"id": f.id, "site": f.site, "detail": f.detail}
                            for f in result.findings]}
    if result.stale is not None:
        payload["stale_records"] = result.stale
    print(json.dumps(payload, sort_keys=True))
    return result.code


def git_in(root, *args, isolate=False):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C"})
    if isolate:
        env["GIT_CONFIG_GLOBAL"] = os.devnull
        env["GIT_CONFIG_SYSTEM"] = os.devnull
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(root), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=env, timeout=30)
    except subprocess.TimeoutExpired:
        raise Cannot("E-GIT-TIMEOUT", "git", "git command exceeded 30s")
    except OSError as exc:
        raise Cannot("E-GIT-FAILED", "git", str(exc)[:120])


def git(*args):
    return git_in(ROOT, *args)


def read_git(commit, path):
    proc = git("show", f"{commit}:{path}")
    if proc.returncode == 0:
        try:
            return proc.stdout.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Cannot("E-READ-FAILED", path, str(exc)[:120])
    error = proc.stderr.decode("utf-8", "replace")
    if re.search(r"does not exist|exists on disk, but not in|not in '", error, re.I):
        return None
    raise Cannot("E-GIT-READ-FAILED", path, error.strip()[:120])


def resolve_in(root, rev):
    proc = git_in(root, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if proc.returncode != 0:
        raise Cannot("E-REVISION-INVALID", "revision",
                     f"{rev[:64]} is not a commit")
    return proc.stdout.decode("ascii", "replace").strip()


def branch_tip_in(root, branch):
    proc = git_in(root, "rev-parse", "--verify", "--quiet",
                  f"refs/heads/{branch}")
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("ascii", "replace").strip()


def is_ancestor(root, sha, ref):
    return git_in(root, "merge-base", "--is-ancestor", sha, ref).returncode == 0


def branch_finding(branch):
    if (not BRANCH.fullmatch(branch) or ".." in branch or "@{" in branch
            or branch.endswith("/") or branch.endswith(".lock")):
        return "E-BRANCH-INVALID"
    return None


def bind(root, rev, branch):
    """Resolve rev and require it landed on refs/heads/<branch> (and origin)."""
    if not REV.fullmatch(rev):
        raise Cannot("E-REVISION-INVALID", "revision",
                     "7-64 hex commit required; HEAD, @ and refs are rejected")
    problem = branch_finding(branch)
    if problem:
        raise Cannot(problem, "branch", "safe ref component required")
    sha = resolve_in(root, rev)
    branch_ref = f"refs/heads/{branch}"
    if branch_tip_in(root, branch) is None or not is_ancestor(root, sha, branch_ref):
        raise Cannot("E-REVISION-NOT-LANDED", "revision",
                     f"{sha[:12]} is not an ancestor of {branch_ref}")
    origin_ref = f"refs/remotes/origin/{branch}"
    if git_in(root, "rev-parse", "--verify", "--quiet", origin_ref).returncode == 0:
        if not is_ancestor(root, sha, origin_ref):
            raise Cannot("E-REVISION-NOT-PUSHED", "revision",
                         f"{sha[:12]} is not an ancestor of {origin_ref}")
    return sha


def probe_paths(text):
    """Lane-relative target paths declared by a registry text, when parseable."""
    paths = set()
    if not text:
        return paths
    try:
        doc = json.loads(text)
    except json.JSONDecodeError:
        return paths
    records = doc.get("records") if isinstance(doc, dict) else None
    if not isinstance(records, list):
        return paths
    for obj in records:
        if isinstance(obj, dict):
            path = obj.get("path")
            if isinstance(path, str) and PATH.fullmatch(path):
                paths.add(path)
    return paths


def revision_finding(rev):
    return None if REV.fullmatch(rev) else "E-REVISION-INVALID"


def build_parser():
    parser = argparse.ArgumentParser(
        description="Narrow read-only round-17 freshness-recheck gate.",
        exit_on_error=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision", metavar="REV",
                       help="7-64 hex commit; reads immutable objects only")
    group.add_argument("--selftest", action="store_true",
                       help="hermetic fixture and binding suite")
    parser.add_argument("--registry-from", metavar="REV",
                        help="compare that revision's records against the "
                             "--revision files; emits STALE-UNFLAGGED")
    parser.add_argument("--branch", default="master",
                        help="landed branch the revision must be an ancestor "
                             "of (default master)")
    return parser


def cli_finding(argv):
    try:
        args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit):
        return "E-CLI"
    if args.selftest and args.registry_from:
        return "E-CLI"
    return None


def fixture_data():
    p1 = "corpus/knowledge/update-safety-v3.md"
    p2 = "corpus/knowledge/driver-firmware-plane.md"
    cap_fresh, cap_boot = CAPTURES[1], CAPTURES[0]
    base1 = ("# Update safety v3\n\n## 5. Risk-ordered operations table\n\n"
             "| 1 | Do nothing now | `-Syu` would be INERT: 0 candidates by "
             "three probes |\n")
    base2 = ("# Driver firmware plane\n\nNVIDIA 610.57.04 on 7.2.3; dkms for "
             "7.1.4.\n")
    quote1 = "`-Syu` would be INERT: 0 candidates by three probes"
    quote2 = "NVIDIA 610.57.04 on 7.2.3"
    heading1 = "## R17-FRESHNESS — dated host re-verification (2026-10-20)"
    heading2 = "## R17-FRESHNESS — driver plane re-verification (2026-10-20)"
    fresh = ("capture header\n"
             "2464:[2026-10-20T09:15:31-0300] [PACMAN] starting full system "
             "upgrade\n$ dkms status\n")
    boot = "$ uname -r\n7.2.11-arch1-1\n"
    notice1 = (f"\n{heading1}\n\n"
               f"- `{quote1}` was current-use at baseline; the executed upgrade "
               "supersedes it.\n"
               f"- [obs] 09:15:31 starting full system upgrade; ref {cap_fresh}:2.\n"
               "- Historical captures stay historical; nothing here authorizes "
               "package/service/boot action.\n")
    notice2 = (f"\n{heading2}\n\n"
               f"- `{quote2}` was current-use at baseline.\n"
               f"- [obs] running `7.2.11-arch1-1`; ref {cap_boot}:2.\n"
               "- Historical captures stay historical.\n")
    record1 = {"id": "R17-FRESH-01", "path": p1,
               "baseline_quote": quote1,
               "stale_reason": "the executed 09:15 upgrade superseded this reading",
               "observed_now": "starting full system upgrade",
               "capture_ref": f"{cap_fresh}:2",
               "capture_quote": "[PACMAN] starting full system upgrade",
               "notice_heading": heading1}
    record2 = {"id": "R17-FRESH-02", "path": p2,
               "baseline_quote": quote2,
               "stale_reason": "610.57.04 superseded by 615.78.08",
               "observed_now": "7.2.11-arch1-1",
               "capture_ref": f"{cap_boot}:2",
               "capture_quote": "7.2.11-arch1-1",
               "notice_heading": heading2}
    registry = {"schema": SCHEMA, "records": [record1, record2]}
    return {"p1": p1, "p2": p2, "cap_fresh": cap_fresh, "cap_boot": cap_boot,
            "base1": base1, "base2": base2, "heading1": heading1,
            "notice1": notice1, "notice2": notice2,
            "targets": {p1: base1 + notice1, p2: base2 + notice2},
            "bases": {p1: base1, p2: base2},
            "captures": {cap_fresh: fresh, cap_boot: boot},
            "registry": registry}


def binding_sandbox():
    """Hermetic mktemp repository exercising landed/pushed/origin binding."""
    out = []
    tmp = tempfile.mkdtemp(prefix="freshness-r17-")
    try:
        root = Path(tmp)

        def run(*args):
            return git_in(root, *args, isolate=True)

        if run("init", "-q", "-b", "master").returncode != 0:
            return [("sandbox-init", "git init failed")]

        def commit(message):
            return run("-c", "user.name=R17", "-c", "user.email=r17@example.invalid",
                       "-c", "commit.gpgsign=false", "commit", "--quiet",
                       "--allow-empty", "-m", message)

        if commit("one").returncode != 0:
            return [("sandbox-commit", "git commit failed")]
        c1 = run("rev-parse", "HEAD").stdout.decode().strip()
        run("update-ref", "refs/remotes/origin/master", c1)
        if commit("two").returncode != 0:
            return [("sandbox-commit2", "git commit failed")]
        c2 = run("rev-parse", "HEAD").stdout.decode().strip()
        run("checkout", "-q", "-b", "side", c1)
        if commit("three").returncode != 0:
            return [("sandbox-commit3", "git commit failed")]
        c3 = run("rev-parse", "HEAD").stdout.decode().strip()
        run("checkout", "-q", "master")

        def expect(rev, want):
            try:
                sha = bind(root, rev, "master")
            except Cannot as exc:
                return None if exc.fid == want else f"got {exc.fid}, want {want}"
            if want is not None:
                return f"resolved {sha[:8]}, want {want}"
            return None if sha == resolve_in(root, rev) else "wrong sha"

        out.append(("sandbox landed", expect(c1, None)))
        out.append(("sandbox abbreviated", expect(c1[:7], None)))
        out.append(("sandbox not-pushed", expect(c2, "E-REVISION-NOT-PUSHED")))
        out.append(("sandbox not-landed", expect(c3, "E-REVISION-NOT-LANDED")))
        out.append(("sandbox head-rejected", expect("HEAD", "E-REVISION-INVALID")))
        out.append(("sandbox unknown-rejected",
                    expect("0" * 40, "E-REVISION-INVALID")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out


def selftest():
    data = fixture_data()
    p1, p2 = data["p1"], data["p2"]
    cap_fresh, cap_boot = data["cap_fresh"], data["cap_boot"]
    base1, base2 = data["base1"], data["base2"]
    heading1 = data["heading1"]
    notice1 = data["notice1"]
    targets = data["targets"]
    clean = data["registry"]

    def registry(**over):
        doc = json.loads(json.dumps(clean))
        doc.update(over)
        return json.dumps(doc)

    def record(index, **over):
        doc = json.loads(json.dumps(clean))
        doc["records"][index].update(over)
        return json.dumps(doc)

    def drop(index, key):
        doc = json.loads(json.dumps(clean))
        doc["records"][index].pop(key)
        return json.dumps(doc)

    def fixture(**over):
        docs = {"registry": json.dumps(clean), "targets": dict(targets),
                "bases": dict(data["bases"]), "captures": dict(data["captures"]),
                "compare": False}
        docs.update(over)
        return DocSet(**docs)

    bad_path_ref = f"corpus/knowledge/update-safety-v3.md:2"
    bad_line_ref = f"{cap_fresh}:0"
    eof_ref = f"{cap_fresh}:9"
    based = base1.replace("## 5.", f"{heading1}\n\n## 5.")

    cases = [
        ("clean", fixture(), PASS, set(), 2, None),
        ("compare-baseline", fixture(targets={p1: base1, p2: base2}, bases={},
                                     captures={}, compare=True),
         FAIL, {"STALE-UNFLAGGED"}, 0, 2),
        ("compare-landing", fixture(compare=True), PASS, set(), 2, 0),
        ("compare-missing-target",
         fixture(targets={p1: targets[p1], p2: None}, bases={}, captures={},
                 compare=True),
         FAIL, {"R17-FRESH-TARGET-MISSING"}, 1, 0),
        ("compare-partial", fixture(targets={p1: targets[p1], p2: base2},
                                    bases={}, captures={}, compare=True),
         FAIL, {"STALE-UNFLAGGED"}, 1, 1),
        ("registry-missing", fixture(registry=None),
         FAIL, {"R17-FRESH-MISSING"}, 0, None),
        ("registry-missing-compare", fixture(registry=None, compare=True),
         CANNOT, {"E-REGISTRY-MISSING"}, 0, None),
        ("registry-malformed", fixture(registry="{"),
         CANNOT, {"E-REGISTRY-PARSE"}, 0, None),
        ("schema-wrong", fixture(registry=registry(schema="tsukuroi-freshness-v0")),
         FAIL, {"R17-FRESH-SCHEMA"}, 0, None),
        ("schema-extra-key", fixture(registry=registry(notes="x")),
         FAIL, {"R17-FRESH-SCHEMA"}, 0, None),
        ("records-not-list", fixture(registry=registry(records="x")),
         FAIL, {"R17-FRESH-SCHEMA"}, 0, None),
        ("records-empty", fixture(registry=registry(records=[])),
         FAIL, {"R17-FRESH-EMPTY"}, 0, None),
        ("field-missing", fixture(registry=drop(0, "stale_reason")),
         FAIL, {"R17-FRESH-FIELD"}, 1, None),
        ("field-extra", fixture(registry=record(0, note="x")),
         FAIL, {"R17-FRESH-FIELD"}, 1, None),
        ("id-malformed", fixture(registry=record(0, id="R17-FRESH-1")),
         FAIL, {"R17-FRESH-ID"}, 1, None),
        ("id-duplicate", fixture(registry=record(1, id="R17-FRESH-01")),
         FAIL, {"R17-FRESH-ID"}, 0, None),
        ("path-absolute", fixture(registry=record(0, path="/etc/mkinitcpio.conf")),
         FAIL, {"R17-FRESH-PATH"}, 1, None),
        ("quote-absent-everywhere",
         fixture(registry=record(0, baseline_quote="quote absent from both files")),
         FAIL, {"R17-FRESH-QUOTE-BASELINE", "R17-FRESH-QUOTE"}, 1, None),
        ("history-rewritten",
         fixture(targets={p1: (base1 + notice1).replace(
             "## 5. Risk-ordered operations table", "## 5. Risk table", 1),
             p2: targets[p2]}),
         FAIL, {"R17-FRESH-HISTORY"}, 1, None),
        ("target-missing", fixture(targets={p1: None, p2: targets[p2]}),
         FAIL, {"R17-FRESH-TARGET-MISSING"}, 1, None),
        ("baseline-missing", fixture(bases={p1: None, p2: base2}),
         FAIL, {"R17-FRESH-BASELINE-MISSING"}, 1, None),
        ("notice-absent", fixture(targets={p1: base1, p2: targets[p2]}),
         FAIL, {"R17-FRESH-NOTICE"}, 1, None),
        ("notice-duplicated", fixture(targets={p1: base1 + notice1 + notice1,
                                               p2: targets[p2]}),
         FAIL, {"R17-FRESH-NOTICE-DUP"}, 1, None),
        ("notice-at-baseline", fixture(targets={p1: based, p2: targets[p2]},
                                       bases={p1: based, p2: base2}),
         FAIL, {"R17-FRESH-NOTICE-BASE", "R17-FRESH-NOTICE"}, 1, None),
        ("notice-form", fixture(registry=record(0, notice_heading="R17 title")),
         FAIL, {"R17-FRESH-NOTICE-FORM"}, 1, None),
        ("notice-content-observed",
         fixture(registry=record(0, observed_now="40 packages upgraded")),
         FAIL, {"R17-FRESH-NOTICE-CONTENT"}, 1, None),
        ("notice-content-ref",
         fixture(targets={p1: (base1 + notice1).replace(
             f"ref {cap_fresh}:2.", "ref omitted."), p2: targets[p2]}),
         FAIL, {"R17-FRESH-NOTICE-CONTENT"}, 1, None),
        ("capture-ref-path",
         fixture(registry=record(0, capture_ref=bad_path_ref),
                 targets={p1: (base1 + notice1).replace(f"{cap_fresh}:2",
                                                        bad_path_ref),
                          p2: targets[p2]}),
         FAIL, {"R17-FRESH-CAPTURE-REF"}, 1, None),
        ("capture-ref-line-zero",
         fixture(registry=record(0, capture_ref=bad_line_ref),
                 targets={p1: (base1 + notice1).replace(f"{cap_fresh}:2",
                                                        bad_line_ref),
                          p2: targets[p2]}),
         FAIL, {"R17-FRESH-CAPTURE-REF"}, 1, None),
        ("capture-missing", fixture(captures={cap_boot: data["captures"][cap_boot]}),
         FAIL, {"R17-FRESH-CAPTURE-MISSING"}, 1, None),
        ("capture-line-eof",
         fixture(registry=record(0, capture_ref=eof_ref),
                 targets={p1: (base1 + notice1).replace(f"{cap_fresh}:2",
                                                        eof_ref),
                          p2: targets[p2]}),
         FAIL, {"R17-FRESH-CAPTURE-LINE"}, 1, None),
        ("capture-quote", fixture(registry=record(
            0, capture_quote="[PACMAN] no such text")),
         FAIL, {"R17-FRESH-CAPTURE-QUOTE"}, 1, None),
        ("partial-record", fixture(targets={p1: targets[p1], p2: base2}),
         FAIL, {"R17-FRESH-NOTICE"}, 1, None),
    ]
    checks = [
        ("revision HEAD", revision_finding("HEAD"), "E-REVISION-INVALID"),
        ("revision at-sign", revision_finding("@"), "E-REVISION-INVALID"),
        ("revision short", revision_finding("abc123"), "E-REVISION-INVALID"),
        ("revision ref", revision_finding("refs/heads/master"),
         "E-REVISION-INVALID"),
        ("revision hex", revision_finding("a" * 40), None),
        ("branch ok", branch_finding("master"), None),
        ("branch ok slash", branch_finding("release/r17"), None),
        ("branch dotdot", branch_finding("feat/../x"), "E-BRANCH-INVALID"),
        ("branch option", branch_finding("-evil"), "E-BRANCH-INVALID"),
        ("branch empty", branch_finding(""), "E-BRANCH-INVALID"),
        ("cli none", cli_finding([]), "E-CLI"),
        ("cli both", cli_finding(["--selftest", "--revision", "a" * 40]), "E-CLI"),
        ("cli registry only", cli_finding(["--registry-from", "a" * 40]), "E-CLI"),
        ("cli registry with selftest",
         cli_finding(["--selftest", "--registry-from", "a" * 40]), "E-CLI"),
    ]
    passed, failures, total = 0, [], 0
    for name, docs, code, want, count, stale in cases:
        total += 1
        result = evaluate(docs)
        problems = []
        if result.code != code:
            problems.append(f"exit={result.code}/{code}")
        got = {f.id for f in result.findings}
        if got != want:
            problems.append("ids=" + ",".join(sorted(got))
                            + " want=" + ",".join(sorted(want)))
        if result.resolved != count:
            problems.append(f"resolved={result.resolved}/{count}")
        if result.stale != stale:
            problems.append(f"stale={result.stale}/{stale}")
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))
        else:
            passed += 1
    for name, got, want in checks:
        total += 1
        if got == want:
            passed += 1
        else:
            failures.append(f"{name}: {got}/{want}")
    for name, problem in binding_sandbox():
        total += 1
        if problem is None:
            passed += 1
        else:
            failures.append(f"{name}: {problem}")
    if failures:
        print(f"CHECK_FRESHNESS_R17_SELFTEST: FAIL ({total} cases, {passed} passed)")
        print("\n".join("  " + item for item in failures))
        return FAIL
    print(f"CHECK_FRESHNESS_R17_SELFTEST: PASS ({total} cases, {passed} passed, "
          "0 failed)")
    return PASS


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit):
        return emit(Result(CANNOT, [Finding("E-CLI", "cli",
                                            "--revision REV or --selftest required")],
                           0, 0, None), "worktree", "master", None)
    if args.selftest:
        if args.registry_from:
            return emit(Result(CANNOT, [Finding("E-CLI", "cli",
                                                "--registry-from requires --revision")],
                               0, 0, None), "worktree", args.branch, None)
        return selftest()
    branch = args.branch
    revision = args.revision
    tip = branch_tip_in(ROOT, branch) if not branch_finding(branch) else None
    try:
        if branch_finding(branch):
            raise Cannot("E-BRANCH-INVALID", "branch", "unsafe or empty branch name")
        revision = bind(ROOT, args.revision, branch)
        source = revision
        if args.registry_from:
            source = bind(ROOT, args.registry_from, branch)
        tip = branch_tip_in(ROOT, branch)
        registry_text = read_git(source, REGISTRY)
        if args.registry_from and registry_text is None:
            return emit(Result(CANNOT, [Finding("E-REGISTRY-MISSING", REGISTRY,
                                                "registry absent at --registry-from")],
                               0, 0, None), revision, branch, tip)
        paths = probe_paths(registry_text)
        targets = {path: read_git(revision, path) for path in paths}
        bases = ({} if args.registry_from
                 else {path: read_git(BASE, path) for path in paths})
        captures = ({} if args.registry_from
                    else {path: read_git(revision, path) for path in CAPTURES})
        docs = DocSet(registry_text, targets, bases, captures,
                      bool(args.registry_from))
    except Cannot as exc:
        return emit(Result(CANNOT, [Finding(exc.fid, exc.site, exc.detail)],
                           0, 0, None), revision, branch, tip)
    except Exception as exc:  # no traceback: unreadable input is CANNOT
        return emit(Result(CANNOT, [Finding("E-INTERNAL", "gate",
                                            str(exc)[:120])],
                           0, 0, None), revision, branch, tip)
    try:
        result = evaluate(docs)
    except Exception as exc:
        return emit(Result(CANNOT, [Finding("E-INTERNAL", "gate",
                                            str(exc)[:120])],
                           0, 0, None), revision, branch, tip)
    return emit(result, revision, branch, tip)


if __name__ == "__main__":
    sys.exit(main())
