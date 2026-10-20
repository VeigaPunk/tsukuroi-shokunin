#!/usr/bin/env python3
"""Narrow, read-only round-13 correction-conformance gate (not a semantic proof).

Exit 0 clean, 1 failed conformance, 2 could-not-evaluate. The tree and --revision
paths share evaluate(); --selftest uses in-memory doc fixtures plus a mktemp git
sandbox for revision binding and the CLI. --revision binds through the shared
tools/_revision.py (round 18): --branch is checked first, then REV must be 7-64 hex
naming one commit that is an ancestor of refs/heads/<branch> (and of
refs/remotes/origin/<branch> when that ref exists). The first binding failure is the
only finding (exit 2). The worktree default reports the branch tip for information
only. One JSON object on stdout. No writes.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import namedtuple
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True  # read-only gate: no tools/__pycache__ in the lane
import _revision  # noqa: E402  shared landed-revision binding (tools/_revision.py)

PASS, FAIL, CANNOT = 0, 1, 2
R12_MD = "corpus/knowledge/root-dac-decision-r12.md"
R12_JSON = "corpus/knowledge/root-dac-decision-r12.json"
R13_MD = "corpus/knowledge/root-dac-correction-r13.md"
R13_JSON = "corpus/knowledge/root-dac-correction-r13.json"
FILES = (R12_MD, R12_JSON, R13_MD, R13_JSON)
ROOT = Path(__file__).resolve().parents[1]
HEADING = "## Round-13 correction — superseded unit-read-only universal"
R13_ID = "R13-DAC-EXCLUSIVITY"
MECHS = ("BindReadOnlyPaths=", "TemporaryFileSystem=", "RootDirectory=", "RootImage=")
OLD = re.compile(r"only\s+`?(?:ProtectSystem=)?strict`?\s*(?:\(?\s*or\s+(?:an?\s+)?`?ReadOnlyPaths=`?"
                 r"(?:\s+(?:entry|entries))?(?:\s+covering\s+`?/?`?)?\s*\)?)?\s*"
                 r"(?:would|could|can)\s+(?:make|produce)[^.\n]{0,160}?(?:read-only|EROFS)", re.I)
OVER = re.compile(r"\b(?:proves?|establishes?|guarantees?)\b[^.\n]{0,60}\bgeneral\b[^.\n]{0,40}correctness", re.I)
DELIM = re.compile(r"\|(?:\s*:?-{3,}:?\s*\|)+")

Finding = namedtuple("Finding", "id site detail", defaults=("",))
DocSet = namedtuple("DocSet", "md12 json12 md13 json13")
Result = namedtuple("Result", "code findings count")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail
def plain(text):
    return " ".join(str(text).replace("`", "").split())
def section(text, heading):
    lines = text.splitlines()
    if heading not in lines:
        return None
    start = lines.index(heading)
    body = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body)
def md_sites(text):
    out = {}
    for line in text.splitlines():
        if OLD.search(line):
            site = "R13" if re.search(r"\*\*R13\b", line) else (
                "CURRENT-HOST" if re.search(r"For reference|current[- ]host", line, re.I) else "UNANCHORED")
            out[site] = out.get(site, 0) + 1
    return out
def json_sites(doc):
    for branch in doc.get("branches") or []:
        if isinstance(branch, dict) and branch.get("id") == "B2":
            if isinstance(branch.get("limit"), str) and OLD.search(branch["limit"]):
                return {"B2-LIMIT": 1}
    return {}
def notice_issues(block):
    text = plain(block)
    checks = (
        ("id", R13_ID in text),
        ("sites", all(re.search(p, text, re.I) for p in (
            r"current[- ]host", r"worked[- ]example", r"\bR13\b", r"\bB2\b", r"decision[-_ ]procedure"))),
        ("pointer", "root-dac-correction-r13.md" in text and "root-dac-correction-r13.json" in text),
        ("scope", "ProtectSystem=no" in text and "ReadOnlyPaths=" in text
         and bool(re.search(r"(?:does not|do not)\s+exclude|exclude[sd]?\s+only", text, re.I))),
    )
    return [name for name, ok in checks if not ok]
def json12_issues(doc):
    out = []
    if doc.get("superseded_by") != R13_JSON:
        out.append("superseded_by")
    notice = plain(doc.get("correction_notice", ""))
    if not (re.search(r"\bB2\b", notice) and re.search(r"interpretation|limit", notice, re.I)):
        out.append("correction_notice")
    return out
def strict_ok(text):
    low = plain(text).lower()
    return "full does not cover /" in low and bool(
        re.search(r"strict[^.]{0,100}except[^.]{0,120}/dev/[^.]{0,60}/proc/[^.]{0,60}/sys/", low))
def namespace_ok(text):
    low = plain(text).lower()
    return bool(re.search(r"private\s+(?:mount\s+)?namespace", low)) and bool(
        re.search(r"unobserved|invisible|cannot exclude|not observed", low))
def md13_issues(text):
    low, lines, out = plain(text).lower(), text.splitlines(), []
    pos = -1
    for heading in ("# Root-DAC unit-read-only correction (round 13)",
                    "## Corrected claim (ProtectSystem= scope)",
                    "## Retained alternate mechanisms",
                    "## Historical cause remains unknown",
                    "## QUALITY check"):
        try:
            pos = lines.index(heading, pos + 1)
        except ValueError:
            out.append("heading:" + heading)
    checks = (
        ("mechanisms", all(m in text for m in MECHS)),
        ("scope", "protectsystem=no" in low and "readonlypaths=" in low and "not excluded by" in low),
        ("nonexhaustive", "non-exhaustive" in low or "not the only" in low),
        ("strict", strict_ok(text)),
        ("namespace", namespace_ok(text)),
        ("source", "s041" in low),
        ("tables", len([l for l in lines if DELIM.fullmatch(l.strip()) and l.count("|") == 5]) >= 2),
    )
    out += [name for name, ok in checks if not ok]
    if any(OLD.search(line) for line in lines):
        out.append("active-exclusive")
    if OVER.search(plain(text)):
        out.append("overclaim")
    return out
def json13_issues(doc):
    alts = doc.get("retained_alternatives")
    effects = " ".join(a.get("effect", "") for a in alts if isinstance(a, dict)).lower() if isinstance(alts, list) else ""
    got = {a.get("mechanism"): a.get("intrinsically_read_only") for a in alts if isinstance(a, dict)} if isinstance(alts, list) else {}
    scope = plain(doc.get("scope", ""))
    strict = plain(" ".join([str(doc.get("full_vs_strict", ""))] + list(doc.get("preserved_exceptions") or []))).lower()
    namespace = (doc.get("unknowns") or {}).get("unit_private_namespace", "")
    universal = doc.get("corrected_universal") or {}
    fixture = doc.get("fixture_identity") or {}
    parent_scope = plain(doc.get("ro_parent_scope", "")).lower()
    claims = plain(doc.get("alternatives_scope", "") + " " + doc.get("claim_scope", "")).lower()
    checks = (
        ("correction_id", doc.get("correction_id") == R13_ID),
        ("scope", bool(re.search(r"\bnarrow\b", scope, re.I)) and bool(re.search(r"not a proof of general semantic correctness", scope, re.I))),
        ("alternatives", isinstance(alts, list) and len(alts) == 4),
        ("alternatives:flags", got == {m: m == "BindReadOnlyPaths=" for m in MECHS}),
        ("alternative:bind", "read-only bind" in effects and "erofs" in effects),
        ("alternative:tmpfs", all(x in effects for x in ("tmpfs", "include ro", "read-only by default", "does not"))),
        ("alternative:root-view", effects.count("not intrinsically read-only") >= 2),
        ("strict-exceptions", all(x in strict for x in ("full does not cover /", "except", "/dev/", "/proc/", "/sys/"))),
        ("namespace", namespace_ok(namespace)),
        ("source", isinstance(universal.get("text"), str) and "S041" in (universal.get("source_ids") or [])),
        ("fixture", fixture.get("executed_root_owned_fixture") is False),
        ("parent-scope", "resolved parent" in parent_scope and ("b4" in parent_scope or "eexist" in parent_scope)),
        ("nonexhaustive", "non-exhaustive" in claims or "not the only" in claims),
    )
    out = [name for name, ok in checks if not ok]
    active = [scope, claims, universal.get("text", ""), strict, plain(namespace), parent_scope,
              plain(fixture.get("statement", "")), plain(doc.get("historical_cause", ""))]
    if isinstance(alts, list):
        active += [a.get("effect", "") for a in alts if isinstance(a, dict)]
    if any(OLD.search(v) for v in active if isinstance(v, str)): out.append("active-exclusive")
    if any(OVER.search(v) for v in active if isinstance(v, str)): out.append("overclaim")
    return out
def evaluate(docs):
    findings = []
    if docs.md12 is None or docs.json12 is None:
        return Result(CANNOT, [Finding("E-R12-MISSING", "r12", "r12 MD/JSON absent")], 0)
    try:
        j12 = json.loads(docs.json12)
    except json.JSONDecodeError as exc:
        return Result(CANNOT, [Finding("E-R12-JSON-PARSE", R12_JSON, str(exc)[:120])], 0)
    md, js = md_sites(docs.md12), json_sites(j12)
    if "CURRENT-HOST" not in md or "R13" not in md:
        findings.append(Finding("R12-MD-HISTORY-MISSING", R12_MD, "old site statements absent"))
    if "B2-LIMIT" not in js:
        findings.append(Finding("R12-JSON-HISTORY-MISSING", R12_JSON, "old B2 limit absent"))
    notice = section(docs.md12, HEADING)
    if notice is None:
        findings.append(Finding("R12-MD-NOTICE-MISSING", HEADING, "notice absent"))
    else:
        findings += [Finding("R12-MD-NOTICE", n, "notice pin absent") for n in notice_issues(notice)]
    for name in json12_issues(j12):
        findings.append(Finding("R12-JSON-SUPERSEDED" if name == "superseded_by" else "R12-JSON-NOTICE",
                                name, "supersession pin absent"))
    kinds = {"active-exclusive": "EXCLUSIVE", "overclaim": "OVERCLAIM"}
    md_ok = json_ok = False
    if docs.md13 is None:
        findings.append(Finding("R13-MD-MISSING", R13_MD, "correction MD absent"))
    else:
        issues = md13_issues(docs.md13)
        md_ok = not issues
        findings += [Finding(f"R13-MD-{kinds.get(i, 'PIN')}", i, "MD pin absent") for i in issues]
    if docs.json13 is None:
        findings.append(Finding("R13-JSON-MISSING", R13_JSON, "correction JSON absent"))
    else:
        try:
            j13 = json.loads(docs.json13)
        except json.JSONDecodeError as exc:
            findings.append(Finding("E-R13-JSON-PARSE", R13_JSON, str(exc)[:120]))
            return Result(CANNOT, findings, 0)
        issues = json13_issues(j13)
        json_ok = not issues
        findings += [Finding(f"R13-JSON-{kinds.get(i, 'PIN')}", i, "JSON pin absent") for i in issues]
    md_notice = not any(f.id.startswith("R12-MD-NOTICE") for f in findings)
    json_notice = not any(f.id.startswith("R12-JSON-SUPERSEDED") or f.id.startswith("R12-JSON-NOTICE") for f in findings)
    active = []
    if not (md_notice and md_ok and json_ok):
        active += ["md:" + s for s in sorted(md)]
        findings += [Finding(f"R12-MD-EXCLUSIVE-{s}", R12_MD, f"count={md[s]}") for s in sorted(md)]
    if not (json_notice and md_ok and json_ok):
        active += ["json:" + s for s in sorted(js)]
        findings += [Finding(f"R12-JSON-EXCLUSIVE-{s}", R12_JSON, f"count={js[s]}") for s in sorted(js)]
    if active:
        findings.append(Finding("UNIT_READONLY_FALSE_UNIVERSAL", "r12-active", ",".join(active)))
    code = FAIL if findings else PASS
    return Result(code, findings, 1 if code == PASS else 0)
def payload(result, revision, branch, branch_tip):
    return {"status": {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[result.code],
            "revision": revision, "branch": branch, "branch_tip": branch_tip,
            "correction_count": result.count,
            "scope": "narrow-conformance-not-semantic-proof",
            "findings": [{"id": f.id, "site": f.site, "detail": f.detail}
                         for f in sorted(result.findings)]}
def emit(result, revision, branch, branch_tip=None):
    print(json.dumps(payload(result, revision, branch, branch_tip), sort_keys=True))
    return result.code
def read_tree(repo, path):
    target = repo / path
    try:
        if not target.is_file():
            return None
        return target.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise Cannot("E-READ-FAILED", path, str(exc)[:120])
GIT_TIMEOUT = 30
def git(repo, *args, identity=None):
    env = {**_revision.clean_env(), **(identity or {})}
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(repo), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
                              timeout=GIT_TIMEOUT)
    except subprocess.TimeoutExpired:
        raise Cannot("E-GIT-TIMEOUT", "git", f"git command exceeded {GIT_TIMEOUT}s")
    except OSError as exc:
        raise Cannot("E-GIT-FAILED", "git", str(exc)[:120])
def read_git(repo, commit, path):
    proc = git(repo, "show", f"{commit}:{path}")
    if proc.returncode == 0:
        try:
            return proc.stdout.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Cannot("E-READ-FAILED", path, str(exc)[:120])
    error = proc.stderr.decode("utf-8", "replace")
    if re.search(r"does not exist|exists on disk, but not in|not in '", error, re.I):
        return None
    raise Cannot("E-GIT-READ-FAILED", path, error.strip()[:120])
def run_gate(repo, revision, branch):
    """(Result, revision, branch_tip). --revision binds through tools/_revision.py and its
    RevisionError becomes the single CANNOT finding; revision None reads the worktree, where
    the branch tip is informational only."""
    label, tip = ("worktree" if revision is None else revision), None
    try:
        if revision is None:
            tip = _revision.branch_tip(repo, branch)
            docs = DocSet(*[read_tree(repo, p) for p in FILES])
        else:
            try:
                bound = _revision.bind(repo, revision, branch)
            except _revision.RevisionError as exc:
                tip = _revision.branch_tip(repo, branch)
                raise Cannot(exc.fid, exc.site, exc.detail) from None
            label, tip = bound.sha, bound.branch_tip
            docs = DocSet(*[read_git(repo, bound.sha, p) for p in FILES])
    except Cannot as exc:
        return Result(CANNOT, [Finding(exc.fid, exc.site, exc.detail)], 0), label, tip
    return evaluate(docs), label, tip


OLDMD = ("For reference, only `strict` (or a `ReadOnlyPaths=` entry covering `/`) would make `/` read-only "
         "through the unit.\n- **R13 — full makes `/` read-only.** Rejected: Only `strict` or a `ReadOnlyPaths=` "
         "entry covering `/` could produce a B2-family `EROFS` for `/` through the unit.\n")
OLDJSON = {"branches": [{"id": "B2", "limit": "so only strict or a ReadOnlyPaths= entry can make / read-only through the unit"}]}
NOTICE = ("**R13-DAC-EXCLUSIVITY** supersedes current-host, worked-example step 3, R13, B2 interpretation/limit and "
          "decision-procedure step 2; root-dac-correction-r13.md and root-dac-correction-r13.json. "
          "ProtectSystem=no and empty ReadOnlyPaths= exclude only those, not B2.")
MD13 = ("source: S041\n# Root-DAC unit-read-only correction (round 13)\n"
        "## Corrected claim (ProtectSystem= scope)\n"
        "BindReadOnlyPaths= TemporaryFileSystem= RootDirectory= RootImage=; not excluded by ProtectSystem=no and "
        "empty ReadOnlyPaths=; ProtectSystem=full does not cover /; ProtectSystem=strict except /dev/, /proc/ and "
        "/sys/; illustrative and non-exhaustive.\n| a | b | c | d |\n|---|---|---|---|\n| e | f | g | h |\n"
        "|---|---|---|---|\n## Retained alternate mechanisms\n## Historical cause remains unknown\n"
        "The private mount namespace is unobserved; a host findmnt cannot exclude it.\n## QUALITY check\n")
def alt(name, flag, effect):
    return {"mechanism": name, "intrinsically_read_only": flag, "effect": effect, "source_id": "S041"}


JSON13 = {
    "correction_id": R13_ID, "round": "round-13",
    "scope": "narrow; not a proof of general semantic correctness",
    "claim_scope": "ProtectSystem= and ReadOnlyPaths= are not the only unit-side mechanisms.",
    "alternatives_scope": "illustrative and non-exhaustive",
    "corrected_universal": {"text": "BindReadOnlyPaths= TemporaryFileSystem= RootDirectory= RootImage=; not excluded by ProtectSystem=no and empty ReadOnlyPaths=; non-exhaustive", "source_ids": ["S041"]},
    "full_vs_strict": "ProtectSystem=full does not cover /; ProtectSystem=strict except /dev/, /proc/ and /sys/.",
    "preserved_exceptions": ["ProtectSystem=strict except /dev/, /proc/ and /sys/."],
    "retained_alternatives": [alt("BindReadOnlyPaths=", True, "read-only bind mounts; EROFS indicator"),
                              alt("TemporaryFileSystem=", False, "tmpfs options can include ro; does not make tmpfs read-only by default"),
                              alt("RootDirectory=", False, "path view; not intrinsically read-only"),
                              alt("RootImage=", False, "path view; not intrinsically read-only")],
    "fixture_identity": {"executed_root_owned_fixture": False, "derived_identity": True, "executed_fixture_parent": "derived caller-owned uid-1000 parent"},
    "ro_parent_scope": "resolved parent directory; existing target is B4 (EEXIST)",
    "unknowns": {"unit_private_namespace": "private mount namespace unobserved; host findmnt cannot exclude it"},
    "historical_cause": "unknown",
}
def corrected_docs():
    return DocSet(
        OLDMD + "\n" + HEADING + "\n\n" + NOTICE + "\n",
        json.dumps(dict(OLDJSON, superseded_by=R13_JSON,
                        correction_notice="B2 interpretation/limit replaced; ProtectSystem=no and ReadOnlyPaths= "
                                          "do not exclude alternatives.")),
        MD13, json.dumps(JSON13))
def doc_cases():
    base, cases = corrected_docs(), []

    def add(name, docs, code, ids=(), count=None):
        cases.append((name, docs, code, set(ids), count))

    def mutant(name, fn, ids):
        doc = copy.deepcopy(JSON13)
        fn(doc)
        add(name, base._replace(json13=json.dumps(doc)), FAIL, ids, 0)

    add("baseline", DocSet(OLDMD, json.dumps(OLDJSON), None, None), FAIL,
        {"R12-MD-EXCLUSIVE-CURRENT-HOST", "R12-MD-EXCLUSIVE-R13", "R12-JSON-EXCLUSIVE-B2-LIMIT",
         "R12-MD-NOTICE-MISSING", "R12-JSON-SUPERSEDED", "R13-MD-MISSING", "R13-JSON-MISSING",
         "UNIT_READONLY_FALSE_UNIVERSAL"}, 0)
    add("corrected", base, PASS, (), 1)
    mutant("remove-alternative", lambda d: d["retained_alternatives"].pop(0), {"R13-JSON-PIN"})
    mutant("rootdirectory-intrinsic", lambda d: d["retained_alternatives"][2].__setitem__("intrinsically_read_only", True), {"R13-JSON-PIN"})
    mutant("tmpfs-default-read-only", lambda d: d["retained_alternatives"][1].__setitem__("intrinsically_read_only", True), {"R13-JSON-PIN"})
    mutant("namespace-certain", lambda d: d["unknowns"].__setitem__("unit_private_namespace", "private namespace identical to host"), {"R13-JSON-PIN"})
    mutant("closed-list-restored", lambda d: d.__setitem__("claim_scope", "Only ProtectSystem=strict or ReadOnlyPaths= can make / read-only through a unit."), {"R13-JSON-EXCLUSIVE"})
    mutant("strict-drop", lambda d: d.__setitem__("full_vs_strict", "ProtectSystem=full covers /."), {"R13-JSON-PIN"})
    add("notice-missing", base._replace(md12=OLDMD), FAIL,
        {"R12-MD-NOTICE-MISSING", "R12-MD-EXCLUSIVE-CURRENT-HOST", "UNIT_READONLY_FALSE_UNIVERSAL"}, 0)
    add("superseded-wrong", base._replace(json12=json.dumps(dict(OLDJSON, superseded_by="other.json",
        correction_notice="B2 interpretation/limit replaced."))), FAIL,
        {"R12-JSON-SUPERSEDED", "R12-JSON-EXCLUSIVE-B2-LIMIT", "UNIT_READONLY_FALSE_UNIVERSAL"}, 0)
    add("malformed-r13-json", base._replace(json13="{"), CANNOT, {"E-R13-JSON-PARSE"}, 0)
    add("history-deleted", DocSet(
        OLDMD.replace("only `strict` (or a `ReadOnlyPaths=` entry covering `/`) would make `/` read-only through the unit", "x")
             .replace("Only `strict` or a `ReadOnlyPaths=` entry covering `/` could produce a B2-family `EROFS` for `/` through the unit.", "x"),
        json.dumps({"branches": [{"id": "B2", "limit": "x"}]}), MD13, json.dumps(JSON13)),
        FAIL, {"R12-MD-HISTORY-MISSING", "R12-JSON-HISTORY-MISSING"}, 0)
    add("table-broken", base._replace(md13=MD13.replace("|---|---|---|---|\n", "|---|\n", 1)), FAIL, {"R13-MD-PIN"}, 0)

    return cases


SANDBOX_IDENTITY = {
    "GIT_AUTHOR_NAME": "root-dac-selftest", "GIT_AUTHOR_EMAIL": "selftest@example.invalid",
    "GIT_COMMITTER_NAME": "root-dac-selftest", "GIT_COMMITTER_EMAIL": "selftest@example.invalid",
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
}
def sandbox_git(repo, *args):
    proc = git(repo, *args, identity=SANDBOX_IDENTITY)
    if proc.returncode != 0:
        raise Cannot("E-SANDBOX-GIT", " ".join(args),
                     proc.stderr.decode("utf-8", "replace").strip()[:120])
    return proc.stdout.decode("utf-8", "replace").strip()
def doc_files(docs):
    return {path: text for path, text in zip(FILES, docs) if text is not None}
def sandbox_commit(repo, files):
    for path, text in files.items():
        (repo / path).parent.mkdir(parents=True, exist_ok=True)
        (repo / path).write_text(text, encoding="utf-8")
    sandbox_git(repo, "add", "--", *files)
    sandbox_git(repo, "commit", "-q", "-m", "selftest " + " ".join(files))
    return sandbox_git(repo, "rev-parse", "HEAD")
def binding_cases():
    """Shared binding through run_gate() and a copied CLI in a mktemp lane; a refusal is one id."""
    out = []
    tmp = Path(tempfile.mkdtemp(prefix="root-dac-bind-"))
    try:
        root = tmp / "lane"
        root.mkdir()
        sandbox_git(root, "init", "-q", "-b", "master")
        c1 = sandbox_commit(root, doc_files(DocSet(OLDMD, json.dumps(OLDJSON), None, None)))
        bare = tmp / "origin.git"
        bare.mkdir()
        sandbox_git(bare, "init", "-q", "--bare")
        sandbox_git(root, "remote", "add", "origin", str(bare))
        sandbox_git(root, "push", "-q", "origin", "master")
        c2 = sandbox_commit(root, doc_files(corrected_docs()))

        def case(name, rev, code, ids=(), branch="master", **want):
            result, revision, tip = run_gate(root, rev, branch)
            got = [f.id for f in result.findings]
            bound_ids = got if code == CANNOT else [i for i in got if i in _revision.IDS]
            problems = [] if result.code == code else [f"exit={result.code}/{code}"]
            if bound_ids != list(ids):
                problems.append("ids=" + ",".join(got) + " want=" + ",".join(ids))
            for key, value in (("revision", revision), ("tip", tip), ("count", result.count)):
                if key in want and want[key] != value:
                    problems.append(f"{key}={value}/{want[key]}")
            out.append((name, problems))

        def refused(name, rev, fid, branch="master", **want):
            case(name, rev, CANNOT, [fid], branch, **want)

        refused("revision-not-pushed", c2, _revision.E_NOT_PUSHED, revision=c2, tip=c2)
        sandbox_git(root, "push", "-q", "origin", "master")
        case("revision-landed-tip", c2, PASS, revision=c2, tip=c2, count=1)
        case("revision-short-tip", c2[:8], PASS, revision=c2, tip=c2)
        case("revision-upper-hex", c2.upper(), PASS, revision=c2)
        case("revision-reads-landed-parent", c1, FAIL, revision=c1, tip=c2, count=0)
        sandbox_git(root, "checkout", "-q", "--detach", c2)
        c3 = sandbox_commit(root, {"c.txt": "three\n"})
        sandbox_git(root, "checkout", "-q", "master")
        # Round 18: first failure only (round 17 also reported E-REVISION-NOT-PUSHED here).
        refused("revision-unlanded-single-id", c3, _revision.E_NOT_LANDED, revision=c3, tip=c2)
        for label, rev in (("head", "HEAD"), ("at", "@"), ("at-parent", "@-"), ("ref-name", "master"),
                           ("full-ref", "refs/heads/master"), ("short-hex", c1[:6]),
                           ("range", f"{c1[:8]}..{c2[:8]}"), ("trailing-slash", f"{c2[:8]}/"),
                           ("empty", ""), ("sixty-five", "a" * 65), ("unknown", "0" * 40)):
            refused(f"revision-{label}", rev, _revision.E_INVALID)
        for label, branch in (("range", "a..b"), ("slash", "master/"), ("space", "bad branch"),
                              ("dash", "-x"), ("head", "HEAD"), ("empty", ""), ("lock", "x.lock")):
            refused(f"branch-invalid-{label}", c2, _revision.E_BRANCH_INVALID, branch, tip=None)
        # Round 18: an absent branch is E-BRANCH-MISSING (round 17 said E-REVISION-NOT-LANDED).
        refused("branch-missing", c2, _revision.E_BRANCH_MISSING, "nosuch", tip=None)
        refused("branch-missing-nested", c2, _revision.E_BRANCH_MISSING, "feature/x")
        refused("precedence-branch-before-revision", "HEAD", _revision.E_BRANCH_INVALID, "a..b")
        refused("precedence-revision-before-missing", "HEAD", _revision.E_INVALID, "nosuch")
        refused("precedence-unknown-before-missing", "0" * 40, _revision.E_INVALID, "nosuch")
        refused("precedence-missing-before-landed", c3, _revision.E_BRANCH_MISSING, "nosuch")
        (tmp / "blob").write_text("not a commit\n", encoding="utf-8")
        sandbox_git(root, "update-ref", "refs/remotes/origin/master",
                    sandbox_git(root, "hash-object", "-w", str(tmp / "blob")))
        refused("git-failed-origin-blob", c2, _revision.E_GIT, tip=c2)
        refused("precedence-landed-before-origin", c3, _revision.E_NOT_LANDED)
        sandbox_git(root, "update-ref", "refs/remotes/origin/master", c2)
        case("worktree", None, PASS, revision="worktree", tip=c2, count=1)
        case("worktree-branch-informational", None, PASS, branch="a..b", revision="worktree", tip=None)

        here = Path(__file__).resolve()
        (root / "tools").mkdir()
        for source in (here, here.parent / "_revision.py"):
            shutil.copy2(source, root / "tools" / source.name)

        def cli(name, argv, code, ids=(), **want):
            try:
                proc = subprocess.run([sys.executable, str(root / "tools" / here.name), *argv],
                                      cwd=str(root), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, env=_revision.clean_env(), timeout=120)
            except (subprocess.TimeoutExpired, OSError) as exc:
                out.append((name, [f"run={exc}"[:120]]))
                return
            try:
                doc = json.loads(proc.stdout.decode("utf-8", "replace"))
            except json.JSONDecodeError:
                doc = None
            doc = doc if isinstance(doc, dict) else {}
            got = [f.get("id") for f in doc.get("findings") or [] if isinstance(f, dict)]
            problems = [] if proc.returncode == code else [f"exit={proc.returncode}/{code}"]
            if got != list(ids):
                problems.append("ids=" + ",".join(map(str, got)) + " want=" + ",".join(ids))
            problems += [f"{key}={doc.get(key)}/{value}" for key, value in want.items()
                         if doc.get(key) != value]
            out.append((name, problems))

        cli("cli-landed-tip", ["--revision", c2], PASS, revision=c2, branch_tip=c2)
        cli("cli-unlanded-single-id", ["--revision", c3], CANNOT, [_revision.E_NOT_LANDED])
        cli("cli-branch-before-revision", ["--revision", "HEAD", "--branch", "a..b"], CANNOT,
            [_revision.E_BRANCH_INVALID])
        cli("cli-branch-dash", ["--revision", c2, "--branch=-x"], CANNOT, [_revision.E_BRANCH_INVALID])
        cli("cli-worktree", [], PASS, revision="worktree", branch_tip=c2)
        sandbox_git(root, "remote", "remove", "origin")
        case("revision-no-remote", c2, PASS, revision=c2, tip=c2)
        sample = payload(Result(PASS, [], 1), c2, "master", c2)
        missing = {"status", "revision", "branch", "branch_tip", "correction_count",
                   "scope", "findings"} - set(sample)
        problems = ["missing=" + ",".join(sorted(missing))] if missing else []
        if sample.get("branch") != "master" or sample.get("branch_tip") != c2:
            problems.append("payload-branch")
        out.append(("payload-shape", problems))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out
def selftest():
    passed, failures = 0, []
    cases = doc_cases()
    for name, docs, code, want, count in cases:
        result = evaluate(docs)
        got = {f.id for f in result.findings}
        problems = []
        if result.code != code:
            problems.append(f"exit={result.code}/{code}")
        if want - got:
            problems.append("missing=" + ",".join(sorted(want - got)))
        if code == PASS and result.findings:
            problems.append("unexpected=" + ",".join(sorted(got)))
        if count is not None and result.count != count:
            problems.append(f"count={result.count}/{count}")
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))
        else:
            passed += 1
    try:
        extra = binding_cases()
    except Cannot as exc:
        print(f"CHECK_ROOT_DAC_CORRECTION_SELFTEST: FAIL (could not evaluate revision binding: "
              f"{exc.fid} {exc.detail})")
        return CANNOT
    for name, problems in extra:
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))
        else:
            passed += 1
    total = len(cases) + len(extra)
    if failures:
        print(f"CHECK_ROOT_DAC_CORRECTION_SELFTEST: FAIL ({total} cases, {passed} passed)")
        print("\n".join("  " + f for f in failures))
        return FAIL
    print(f"CHECK_ROOT_DAC_CORRECTION_SELFTEST: PASS ({total} cases, {passed} passed, 0 failed)")
    return PASS
def main(argv=None):
    parser = argparse.ArgumentParser(description="Narrow read-only round-13 correction conformance gate.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--revision", metavar="REV",
                       help="a 7-64 hex commit; must be landed on --branch")
    group.add_argument("--selftest", action="store_true", help="fixture suite plus a mktemp git sandbox")
    parser.add_argument("--branch", default="master",
                        help="landing branch checked with merge-base (default: master)")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    result, revision, tip = run_gate(ROOT, args.revision, args.branch)
    return emit(result, revision, args.branch, tip)


if __name__ == "__main__":
    sys.exit(main())
