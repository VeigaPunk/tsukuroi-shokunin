#!/usr/bin/env python3
"""Finite source-contract gate, not a consumer-execution or host-health certificate."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
import _revision

ROOT = Path(__file__).resolve().parents[1]
DATA = "corpus/knowledge/selector-contract-r21.json"
TEXT = "corpus/knowledge/selector-contract-r21.md"
EXPECTED = {
    "commit": ("accept-if-landed-and-pushed", None),
    "tree": ("refuse", "E-REVISION-INVALID"),
    "blob": ("refuse", "E-REVISION-INVALID"),
    "tag-to-commit": ("accept-if-landed-and-pushed", None),
    "tag-to-noncommit": ("refuse", "E-REVISION-INVALID"),
}


def result(rows, findings, code=None):
    if code is None:
        code = 1 if findings else 0
    return code, {"status": ("PASS", "FAIL", "CANNOT_EVALUATE")[code],
                  "decision_rows": rows, "decision_total": len(EXPECTED),
                  "findings": findings,
                  "scope": "five declared source-grounded decisions; not consumer behavior or host health"}


def evaluate(raw, markdown, registry):
    def fail(fid, detail, code=1):
        return result(0, [{"id": fid, "detail": detail}], code)
    if raw is None or markdown is None:
        return fail("SELECTOR-CONTRACT-MISSING", "decision data or prose absent")
    try:
        data = json.loads(raw)
    except (ValueError, TypeError):
        return fail("SELECTOR-CONTRACT-SCHEMA", "invalid JSON", 2)
    if (not isinstance(data, dict) or data.get("schema") != "tsukuroi-selector-contract-v1"
            or not isinstance(data.get("decisions"), list)):
        return fail("SELECTOR-CONTRACT-SCHEMA", "invalid contract shape", 2)
    rows = data["decisions"]
    if any(not isinstance(row, dict) or not isinstance(row.get("class"), str) for row in rows):
        return fail("SELECTOR-CONTRACT-SCHEMA", "invalid decision shape", 2)
    classes = [row["class"] for row in rows]
    if len(set(classes)) != len(classes) or set(classes) != set(EXPECTED):
        return fail("SELECTOR-CONTRACT-MISMATCH", "exact five unique classes required")
    if data.get("sources") != ["S081", "S082"]:
        return fail("SELECTOR-CONTRACT-MISMATCH", "exact opened source identities required")
    if registry is None:
        return fail("SELECTOR-CONTRACT-MISMATCH", "source registry absent")
    registry_rows = {}
    for line in registry.splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) == 13 and cells[1] in ("S081", "S082"):
            registry_rows[cells[1]] = cells
    urls = {"S081": "https://git-scm.com/docs/gitrevisions/2.56.0",
            "S082": "https://git-scm.com/docs/git-rev-parse/2.56.0"}
    for source, url in urls.items():
        cells = registry_rows.get(source)
        if not cells or url not in cells[2] or cells[4] != "A" or cells[8] != "mined":
            return fail("SELECTOR-CONTRACT-MISMATCH", "opened scoped A/mined source row required")
    valid = 0
    findings = []
    for row in rows:
        name = row["class"]
        outcome, finding = EXPECTED[name]
        prose_rows = [line for line in markdown.splitlines()
                      if line.startswith("| " + name + " |")]
        supported = (len(prose_rows) == 1 and outcome in prose_rows[0]
                     and (finding is None or finding in prose_rows[0]))
        if ((row.get("outcome"), row.get("finding")) != (outcome, finding)
                or row.get("source") not in urls or not isinstance(row.get("rationale"), str)
                or not row["rationale"].strip() or not supported):
            findings.append({"id": "SELECTOR-CONTRACT-MISMATCH", "detail": name})
        else:
            valid += 1
    return result(valid, findings)


def git_read(rev, path):
    proc = subprocess.run(["git", "--no-pager", "-C", str(ROOT), "show", f"{rev}:{path}"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=_revision.clean_env(), timeout=30)
    if proc.returncode:
        exists = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-z", rev, "--", path],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env=_revision.clean_env(), timeout=30)
        if exists.returncode == 0 and not exists.stdout:
            return None
        raise RuntimeError(f"cannot read committed {path}")
    return proc.stdout.decode("utf-8")


def selftest():
    sample = {"schema": "tsukuroi-selector-contract-v1", "sources": ["S081", "S082"],
              "decisions": [{"class": name, "outcome": outcome, "finding": finding,
                             "source": "S081", "rationale": "finite source proposition"}
                            for name, (outcome, finding) in EXPECTED.items()]}
    prose = "\n".join(f"| {name} | {outcome} | {finding} |"
                      for name, (outcome, finding) in EXPECTED.items())
    registry = ("| S081 | https://git-scm.com/docs/gitrevisions/2.56.0 | docs | A | type | typed | learns | mined | 2026-10-21 | on-release | lesson |\n"
                "| S082 | https://git-scm.com/docs/git-rev-parse/2.56.0 | docs | A | type | verify | learns | mined | 2026-10-21 | on-release | lesson |\n")
    cases = [("clean", sample, prose, registry, 0, None),
             ("missing", None, prose, registry, 1, "SELECTOR-CONTRACT-MISSING"),
             ("malformed", "{", prose, registry, 2, "SELECTOR-CONTRACT-SCHEMA"),
             ("missing-markdown", sample, None, registry, 1, "SELECTOR-CONTRACT-MISSING"),
             ("missing-source", sample, prose, "", 1, "SELECTOR-CONTRACT-MISMATCH")]
    for label, mutation in (("missing-row", lambda d: d["decisions"].pop()),
                            ("duplicate", lambda d: d["decisions"].append(d["decisions"][0])),
                            ("tree-accept", lambda d: d["decisions"][1].update(outcome="accept-if-landed-and-pushed")),
                            ("tag-refuse", lambda d: d["decisions"][3].update(outcome="refuse")),
                            ("wrong-source", lambda d: d["decisions"][0].update(source="S999"))):
        data = copy.deepcopy(sample)
        mutation(data)
        cases.append((label, data, prose, registry, 1, "SELECTOR-CONTRACT-MISMATCH"))
    cases.append(("prose-outcome", sample, prose.replace("| tree | refuse", "| tree | accept"),
                  registry, 1, "SELECTOR-CONTRACT-MISMATCH"))
    failures = []
    for label, data, text, sources, expected_code, expected_id in cases:
        raw = json.dumps(data) if isinstance(data, dict) else data
        code, payload = evaluate(raw, text, sources)
        ids = {f["id"] for f in payload["findings"]}
        if code != expected_code or ids != ({expected_id} if expected_id else set()):
            failures.append(label)
    print(json.dumps({"status": "FAIL" if failures else "PASS", "cases": len(cases),
                      "passed": len(cases) - len(failures), "failures": failures}))
    return 1 if failures else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--revision")
    choice.add_argument("--selftest", action="store_true")
    parser.add_argument("--branch", default="master")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        if exc.code == 0:
            return 0
        code, payload = result(0, [{"id": "E-CLI", "detail": "invalid arguments"}], 2)
        print(json.dumps(payload))
        return code
    if args.selftest:
        return selftest()
    try:
        binding = _revision.bind(ROOT, args.revision, args.branch)
        code, payload = evaluate(git_read(binding.sha, DATA), git_read(binding.sha, TEXT),
                                 git_read(binding.sha, "corpus/SOURCES.md"))
        payload.update(revision=binding.sha, branch=binding.branch, branch_tip=binding.branch_tip)
    except _revision.RevisionError as exc:
        code, payload = result(0, [{"id": exc.fid, "detail": exc.detail}], 2)
    except (OSError, RuntimeError, UnicodeError, subprocess.TimeoutExpired) as exc:
        code, payload = result(0, [{"id": "E-READ", "detail": str(exc)[:120]}], 2)
    print(json.dumps(payload, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
