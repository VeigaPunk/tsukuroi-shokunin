#!/usr/bin/env python3
"""Narrow, read-only round-13 correction-conformance gate (not a semantic proof).

Exit 0 clean, 1 failed conformance, 2 could-not-evaluate. The tree and --revision
paths share evaluate(); --selftest uses in-memory fixtures only. No writes.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import subprocess
import sys
from collections import namedtuple
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
R12_MD = "corpus/knowledge/root-dac-decision-r12.md"
R12_JSON = "corpus/knowledge/root-dac-decision-r12.json"
R13_MD = "corpus/knowledge/root-dac-correction-r13.md"
R13_JSON = "corpus/knowledge/root-dac-correction-r13.json"
HEADING = "## Round-13 correction — superseded unit-read-only universal"
R13_ID = "R13-DAC-EXCLUSIVITY"
MECHS = ("BindReadOnlyPaths=", "TemporaryFileSystem=", "RootDirectory=", "RootImage=")
VALID_REV = re.compile(r"^(?:HEAD|[0-9a-fA-F]{4,64})$")
OLD = re.compile(r"only\s+`?(?:ProtectSystem=)?strict`?\s*(?:\(?\s*or\s+(?:an?\s+)?`?ReadOnlyPaths=`?"
                 r"(?:\s+(?:entry|entries))?(?:\s+covering\s+`?/?`?)?\s*\)?)?\s*"
                 r"(?:would|could|can)\s+(?:make|produce)[^.\n]{0,160}?(?:read-only|EROFS)", re.I)
OVER = re.compile(r"\b(?:proves?|establishes?|guarantees?)\b[^.\n]{0,60}\bgeneral\b[^.\n]{0,40}correctness", re.I)
DELIM = re.compile(r"\|(?:\s*:?-{3,}:?\s*\|)+")

Finding = namedtuple("Finding", "id site detail", defaults=("",))
DocSet = namedtuple("DocSet", "md12 json12 md13 json13 source")
Result = namedtuple("Result", "code findings count source")


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
        return Result(CANNOT, [Finding("E-R12-MISSING", "r12", "r12 MD/JSON absent")], 0, docs.source)
    try:
        j12 = json.loads(docs.json12)
    except json.JSONDecodeError as exc:
        return Result(CANNOT, [Finding("E-R12-JSON-PARSE", R12_JSON, str(exc)[:120])], 0, docs.source)
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
            return Result(CANNOT, findings, 0, docs.source)
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
    return Result(code, findings, 1 if code == PASS else 0, docs.source)
def emit(result):
    status = {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[result.code]
    print(f"CHECK_ROOT_DAC_CORRECTION: {status} correction_count={result.count} source={result.source} "
          f"scope=narrow-conformance-not-semantic-proof findings={len(result.findings)}")
    for f in sorted(result.findings):
        print(f"F {f.id} site={f.site} detail={json.dumps(f.detail)}")
    return result.code
def read_tree(repo, path):
    target = repo / path
    try:
        if not target.is_file():
            return None
        return target.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise Cannot("E-READ-FAILED", path, str(exc)[:120])
def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C"})
    return subprocess.run(["git", "--no-pager", "-C", str(repo), *args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
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
def resolve(repo, rev):
    proc = git(repo, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if proc.returncode != 0:
        raise Cannot("E-REVISION-INVALID", "revision", "HEAD or hex commit required")
    return proc.stdout.decode("ascii", "replace").strip()


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
        MD13, json.dumps(JSON13), "selftest")
def selftest():
    base, cases = corrected_docs(), []

    def add(name, docs, code, ids=(), count=None):
        cases.append((name, docs, code, set(ids), count))

    def mutant(name, fn, ids):
        doc = copy.deepcopy(JSON13)
        fn(doc)
        add(name, base._replace(json13=json.dumps(doc)), FAIL, ids, 0)

    add("baseline", DocSet(OLDMD, json.dumps(OLDJSON), None, None, "selftest"), FAIL,
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
        json.dumps({"branches": [{"id": "B2", "limit": "x"}]}), MD13, json.dumps(JSON13), "selftest"),
        FAIL, {"R12-MD-HISTORY-MISSING", "R12-JSON-HISTORY-MISSING"}, 0)
    add("table-broken", base._replace(md13=MD13.replace("|---|---|---|---|\n", "|---|\n", 1)), FAIL, {"R13-MD-PIN"}, 0)

    passed, failures = 0, []
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
    if failures:
        print(f"CHECK_ROOT_DAC_CORRECTION_SELFTEST: FAIL ({len(cases)} cases, {passed} passed)")
        print("\n".join("  " + f for f in failures))
        return FAIL
    print(f"CHECK_ROOT_DAC_CORRECTION_SELFTEST: PASS ({len(cases)} cases, {passed} passed, 0 failed)")
    return PASS
def main(argv=None):
    parser = argparse.ArgumentParser(description="Narrow read-only round-13 correction conformance gate.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--revision", metavar="REV", help="HEAD or a 4-64 hex commit")
    group.add_argument("--selftest", action="store_true", help="in-memory fixture suite")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    repo, source = Path(__file__).resolve().parents[1], "tree"
    try:
        if args.revision:
            source = "revision:invalid"
            if not VALID_REV.fullmatch(args.revision):
                raise Cannot("E-REVISION-INVALID", "revision", "HEAD or hex commit required")
            source = f"revision:{args.revision}"
            commit = resolve(repo, args.revision)
            source = f"revision:{commit}"
            docs = DocSet(*[read_git(repo, commit, p) for p in (R12_MD, R12_JSON, R13_MD, R13_JSON)], source)
        else:
            docs = DocSet(*[read_tree(repo, p) for p in (R12_MD, R12_JSON, R13_MD, R13_JSON)], source)
    except Cannot as exc:
        return emit(Result(CANNOT, [Finding(exc.fid, exc.site, exc.detail)], 0, source))
    return emit(evaluate(docs))


if __name__ == "__main__":
    sys.exit(main())
