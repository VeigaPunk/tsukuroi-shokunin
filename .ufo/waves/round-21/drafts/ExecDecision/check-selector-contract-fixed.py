#!/usr/bin/env python3
"""Finite check of the corrected five-row selector source contract.

This gate checks the committed corrected JSON, Markdown and source-registry records.
It does not execute Git selector cases, prove free-text semantics generally, or certify
consumer behavior or host health. Copy to tools/ before running: ROOT and the shared
_revision import intentionally use the production tools/ layout.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import _revision

ROOT = Path(__file__).resolve().parents[1]
DATA = "corpus/knowledge/selector-contract-r21-corrected.json"
TEXT = "corpus/knowledge/selector-contract-r21-corrected.md"
SOURCES = "corpus/SOURCES.md"
PASS, FAIL, CANNOT = 0, 1, 2
STATUS = ("PASS", "FAIL", "CANNOT_EVALUATE")
SCHEMA_ID = "SELECTOR-CONTRACT-SCHEMA"
MISSING_ID = "SELECTOR-CONTRACT-MISSING"
MISMATCH_ID = "SELECTOR-CONTRACT-MISMATCH"
E_READ = "E-READ"
SCHEMA = "tsukuroi-selector-contract-v1"
REQUIRED_ROOT = frozenset(("schema", "sources", "decisions"))
REQUIRED_DECISION = frozenset(("class", "outcome", "finding", "source", "rationale", "policy"))
EXPECTED = {
    "commit": ("accept-if-landed-and-pushed", None, "S082"),
    "tree": ("refuse", "E-REVISION-INVALID", "S081"),
    "blob": ("refuse", "E-REVISION-INVALID", "S081"),
    "tag-to-commit": ("accept-if-landed-and-pushed", None, "S081"),
    "tag-to-noncommit": ("refuse", "E-REVISION-INVALID", "S081"),
}
SOURCE_URLS = {
    "S081": "https://git-scm.com/docs/gitrevisions/2.56.0",
    "S082": "https://git-scm.com/docs/git-rev-parse/2.56.0",
}
TABLE_HEADER = (
    "class / row id",
    "git type proposition",
    "lane outcome",
    "refusal finding",
    "git source and separate policy",
)
POLICY_EXCLUSION = (
    "those object-prefix/ancestry/push restrictions come from the lane's evidence contract, not these manuals"
)


def result(rows, findings, code=None):
    if code is None:
        code = FAIL if findings else PASS
    return code, {
        "status": STATUS[code],
        "decision_rows": rows,
        "decision_total": len(EXPECTED),
        "findings": findings,
        "scope": "five corrected source-grounded decisions; not consumer behavior or host health",
    }


def fail(fid, detail, code=FAIL):
    return result(0, [{"id": fid, "detail": detail}], code)


def _pairs_without_duplicates(pairs):
    result_object = {}
    for key, value in pairs:
        if key in result_object:
            raise ValueError(f"duplicate JSON key: {key}")
        result_object[key] = value
    return result_object


def _clean_git_env():
    env = _revision.clean_env()
    env["GIT_NO_LAZY_FETCH"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def git_read(revision, path):
    """Read one fixed committed path, returning None only when that path is absent."""
    args = ["git", "--no-pager", "-C", str(ROOT), "show", f"{revision}:{path}"]
    proc = subprocess.run(
        args,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_clean_git_env(),
        timeout=30,
        check=False,
    )
    if proc.returncode:
        exists = subprocess.run(
            ["git", "--no-pager", "-C", str(ROOT), "ls-tree", "-z", revision, "--", path],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=_clean_git_env(),
            timeout=30,
            check=False,
        )
        if exists.returncode == 0 and not exists.stdout:
            return None
        raise RuntimeError(f"cannot read committed {path}")
    return proc.stdout.decode("utf-8")


def _source_registry_ok(registry):
    registry_rows = {}
    for line in registry.splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) == 13 and cells[1] in SOURCE_URLS:
            source_id = cells[1]
            if source_id in registry_rows:
                return False
            registry_rows[source_id] = cells
    for source_id, url in SOURCE_URLS.items():
        cells = registry_rows.get(source_id)
        if not cells or url not in cells[2] or cells[4] != "A" or cells[8] != "mined":
            return False
    return True


def _normalize(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"[*_~]", "", text)
    text = text.replace("–", "-").replace("—", "-").replace("’", "'")
    return " ".join(text.split()).casefold().strip()


def _normalize_class(text):
    value = _normalize(text)
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def _visible_lines(markdown):
    """Remove HTML comments and fenced code before examining prose or tables."""
    markdown = re.sub(
        r"<!--.*?(?:-->|\Z)",
        lambda match: " " + ("\n" * match.group(0).count("\n")),
        markdown,
        flags=re.DOTALL,
    )
    visible = []
    fence_char = None
    fence_size = 0
    for line in markdown.splitlines():
        fence = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence_char is None:
            if fence:
                fence_char = fence.group(1)[0]
                fence_size = len(fence.group(1))
                continue
            visible.append(line)
            continue
        if fence:
            marker = fence.group(1)
            if marker[0] == fence_char and len(marker) >= fence_size and not fence.group(2).strip():
                fence_char = None
                fence_size = 0
        continue
    return visible


def _section(lines, title):
    wanted = _normalize(title)
    start = None
    level = None
    for index, line in enumerate(lines):
        heading = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading and _normalize(heading.group(2)) == wanted:
            start = index + 1
            level = len(heading.group(1))
            break
    if start is None:
        return None
    section_lines = []
    for line in lines[start:]:
        heading = re.match(r"^\s{0,3}(#{1,6})\s+", line)
        if heading and len(heading.group(1)) <= level:
            break
        section_lines.append(line)
    return "\n".join(section_lines)


def _has_nested_recursive(text):
    normalized = _normalize(text)
    return bool(re.search(r"\bnest\w*\b", normalized) and re.search(r"\brecur\w*\b", normalized))


def _policy_prose_ok(markdown):
    lines = _visible_lines(markdown)
    section = _section(lines, "Located Git propositions versus lane policy")
    if section is None:
        return False
    text = _normalize(section)
    required = (
        "dereference the object at <rev> recursively until an object of type <type> is found",
        "or the object cannot be dereferenced anymore (in which case, barf)",
        "a commit-ish (i.e. a commit, or an annotated tag that points at a commit)",
        "the source field in each json row supports only its git type proposition",
        "its separate policy field cites quality27/36 and the shared binder",
        "hexadecimal object-only selection",
        "first-failure diagnostics",
        "lane-branch ancestry",
        "conditional origin-ref ancestry",
        POLICY_EXCLUSION,
        "only when that ref exists",
        "an absent origin tracking ref does not itself cause refusal",
    )
    return all(phrase in text for phrase in required)


def _table_cells(line):
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    body = stripped[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [cell.strip() for cell in body.split("|")]


def _is_separator(cells):
    return len(cells) == 5 and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def _contract_table(markdown):
    lines = _visible_lines(markdown)
    matches = []
    for index, line in enumerate(lines):
        cells = _table_cells(line)
        if cells is None or len(cells) != 5:
            continue
        if tuple(_normalize(cell) for cell in cells) != TABLE_HEADER:
            continue
        if index + 1 >= len(lines):
            return None
        separator = _table_cells(lines[index + 1])
        if separator is None or not _is_separator(separator):
            return None
        rows = []
        malformed = False
        for row_line in lines[index + 2:]:
            if not row_line.strip():
                break
            row_cells = _table_cells(row_line)
            if row_cells is None:
                break
            if len(row_cells) != 5:
                malformed = True
                break
            rows.append(row_cells)
        matches.append((rows, malformed))
    if len(matches) != 1:
        return None
    rows, malformed = matches[0]
    if malformed:
        return None
    return rows


def _markdown_rows_ok(markdown):
    rows = _contract_table(markdown)
    if rows is None:
        return False
    by_class = {}
    for cells in rows:
        name = _normalize_class(cells[0])
        if name in by_class:
            return False
        by_class[name] = cells
    if set(by_class) != set(EXPECTED):
        return False

    for name, (outcome, finding, source) in EXPECTED.items():
        cells = by_class[name]
        if _normalize(cells[2]) != outcome:
            return False
        if finding is not None and _normalize(cells[3]) != finding.casefold():
            return False
        if _normalize(cells[4]) != f"{source.casefold()}; quality27/36":
            return False
        if name == "tag-to-commit" and not _has_nested_recursive(cells[1]):
            return False
    return True


def evaluate(raw, markdown, registry):
    if raw is None or markdown is None:
        return fail(MISSING_ID, "corrected decision data or Markdown is absent")
    try:
        data = json.loads(raw, object_pairs_hook=_pairs_without_duplicates)
    except (ValueError, TypeError):
        return fail(SCHEMA_ID, "invalid JSON or duplicate object key", CANNOT)
    if not isinstance(data, dict) or data.get("schema") != SCHEMA or not REQUIRED_ROOT.issubset(data):
        return fail(SCHEMA_ID, "invalid contract root shape", CANNOT)
    if "supersedes" in data and (not isinstance(data["supersedes"], str) or not data["supersedes"].strip()):
        return fail(SCHEMA_ID, "supersedes must be non-empty text when present", CANNOT)
    if not isinstance(data["sources"], list):
        return fail(SCHEMA_ID, "sources must be a list", CANNOT)
    if data["sources"] != ["S081", "S082"]:
        return fail(MISMATCH_ID, "exact S081/S082 source identities required")
    if registry is None or not _source_registry_ok(registry):
        return fail(MISMATCH_ID, "opened tier-A/mined S081 and S082 registry rows required")
    decisions = data["decisions"]
    if not isinstance(decisions, list):
        return fail(SCHEMA_ID, "decisions must be a list", CANNOT)
    for row in decisions:
        if not isinstance(row, dict):
            return fail(SCHEMA_ID, "each decision must be an object", CANNOT)
        if not REQUIRED_DECISION.issubset(row):
            return fail(SCHEMA_ID, "decision requires class, outcome, finding, source, rationale, and policy", CANNOT)
        if not isinstance(row["class"], str) or not isinstance(row["outcome"], str):
            return fail(SCHEMA_ID, "decision class and outcome must be text", CANNOT)
        if row["finding"] is not None and not isinstance(row["finding"], str):
            return fail(SCHEMA_ID, "decision finding must be text or null", CANNOT)
        if not isinstance(row["source"], str) or not isinstance(row["policy"], str):
            return fail(SCHEMA_ID, "decision source and policy must be text", CANNOT)
        if not isinstance(row["rationale"], str) or not row["rationale"].strip():
            return fail(SCHEMA_ID, "decision rationale must be non-empty text", CANNOT)

    classes = [row["class"] for row in decisions]
    if len(set(classes)) != len(classes) or set(classes) != set(EXPECTED):
        return fail(MISMATCH_ID, "exactly five unique fixed decision classes required")

    findings = []
    valid = 0
    for row in decisions:
        name = row["class"]
        outcome, finding, source = EXPECTED[name]
        row_ok = (
            row["outcome"] == outcome
            and row["finding"] == finding
            and row["source"] == source
            and row["policy"] == "QUALITY27/36"
        )
        if name == "tag-to-commit":
            row_ok = row_ok and _has_nested_recursive(row["rationale"])
        if row_ok:
            valid += 1
        else:
            findings.append({"id": MISMATCH_ID, "detail": name})
    if not _policy_prose_ok(markdown):
        findings.append({"id": MISMATCH_ID, "detail": "lane policy must remain separate from Git propositions"})
    if not _markdown_rows_ok(markdown):
        findings.append({"id": MISMATCH_ID, "detail": "five-column Markdown decision table does not match fixed cells"})
    if findings:
        return result(valid, findings)
    return result(valid, [])


# Literal fixture: intentionally independent of EXPECTED and in the real five-column form.
SAMPLE = {
    "schema": "tsukuroi-selector-contract-v1",
    "supersedes": "fixture provenance representation only",
    "sources": ["S081", "S082"],
    "decisions": [
        {"class": "commit", "outcome": "accept-if-landed-and-pushed", "finding": None, "source": "S082", "policy": "QUALITY27/36", "rationale": "Git defines an existing commit as commit-ish; lane ancestry applies, and pushed means ancestor of the local origin tracking ref only when that ref exists."},
        {"class": "tree", "outcome": "refuse", "finding": "E-REVISION-INVALID", "source": "S081", "policy": "QUALITY27/36", "rationale": "Any tree is not commit-ish; the lane policy supplies the refusal code."},
        {"class": "blob", "outcome": "refuse", "finding": "E-REVISION-INVALID", "source": "S081", "policy": "QUALITY27/36", "rationale": "A blob is not commit-ish; the lane policy supplies the refusal code."},
        {"class": "tag-to-commit", "outcome": "accept-if-landed-and-pushed", "finding": None, "source": "S081", "policy": "QUALITY27/36", "rationale": "Annotated tags including nested annotated tags peel recursively to a commit; lane ancestry applies, and the origin tracking ref is checked only when present."},
        {"class": "tag-to-noncommit", "outcome": "refuse", "finding": "E-REVISION-INVALID", "source": "S081", "policy": "QUALITY27/36", "rationale": "An annotated tag ending at tree or blob cannot peel to the requested commit type; the lane supplies the refusal code."},
    ],
}
SAMPLE_MARKDOWN = """# R21-TYPE-PROVENANCE — corrected decision contract

## Located Git propositions versus lane policy

S081, SPECIFYING REVISIONS `<rev>^{<type>}`, version2.56.0, opened2026-10-21:

- “dereference the object at <rev> recursively until an object of type <type> is found”
- “or the object cannot be dereferenced anymore (in which case, barf).”

S082, OPTIONS › Options for Output › `--verify`, same version/access date:

- “a commit-ish (i.e. a commit, or an annotated tag that points at a commit)”

The source field in each JSON row supports only its Git type proposition. Its separate policy field cites QUALITY27/36 and the shared binder for hexadecimal object-only selection, first-failure diagnostics, lane-branch ancestry and conditional origin-ref ancestry. Those object-prefix/ancestry/push restrictions come from the lane's evidence contract, not these manuals.

Here `accept-if-landed-and-pushed` is the existing short policy label: “pushed” means ancestor of the locally recorded `refs/remotes/origin/<branch>` only when that ref exists. An absent origin tracking ref does not itself cause refusal. Local tracking state does not certify the live remote service.

## Five fixed decisions

| Class / row ID | Git type proposition | Lane outcome | Refusal finding | Git source and separate policy |
|---|---|---|---|---|
| commit | Existing commit is commit-ish; origin check applies only when the tracking ref exists | accept-if-landed-and-pushed | none on acceptance; other binding failures remain possible | S082; QUALITY27/36 |
| tree | Any tree is not commit-ish; non-empty tree is the measured control | refuse | E-REVISION-INVALID | S081; QUALITY27/36 |
| blob | A blob is not commit-ish | refuse | E-REVISION-INVALID | S081; QUALITY27/36 |
| tag-to-commit | Annotated tags, including nested annotated tags, peel recursively to the terminal commit | accept-if-landed-and-pushed | none on acceptance; other binding failures remain possible | S081; QUALITY27/36 |
| tag-to-noncommit | Annotated tag ending at tree or blob cannot peel to a commit | refuse | E-REVISION-INVALID | S081; QUALITY27/36 |
"""
SAMPLE_REGISTRY = """| S081 | Git revisions — https://git-scm.com/docs/gitrevisions/2.56.0 | docs | A | scoped typed peeling | anchor | proposition | mined | 2026-10-21 | on-release | corpus/knowledge/selector-contract-r21-corrected.md |
| S082 | Git rev-parse — https://git-scm.com/docs/git-rev-parse/2.56.0 | docs | A | scoped verification | anchor | proposition | mined | 2026-10-21 | on-release | corpus/knowledge/selector-contract-r21-corrected.md |
"""


def _json_text(data):
    return json.dumps(data, sort_keys=True)


def _selftest_cases():
    base = copy.deepcopy(SAMPLE)
    cases = [("clean", _json_text(base), SAMPLE_MARKDOWN, SAMPLE_REGISTRY, PASS, None)]

    cases.append(("missing-contract", None, SAMPLE_MARKDOWN, SAMPLE_REGISTRY, FAIL, MISSING_ID))
    cases.append(("missing-markdown", _json_text(base), None, SAMPLE_REGISTRY, FAIL, MISSING_ID))
    cases.append(("malformed-json", "{", SAMPLE_MARKDOWN, SAMPLE_REGISTRY, CANNOT, SCHEMA_ID))
    missing_row = copy.deepcopy(base)
    missing_row["decisions"].pop()
    cases.append(("missing-row", _json_text(missing_row), SAMPLE_MARKDOWN, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))
    wrong_tree = copy.deepcopy(base)
    wrong_tree["decisions"][1]["outcome"] = "accept-if-landed-and-pushed"
    cases.append(("wrong-tree-action", _json_text(wrong_tree), SAMPLE_MARKDOWN, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))
    duplicate = copy.deepcopy(base)
    duplicate["decisions"].append(copy.deepcopy(duplicate["decisions"][0]))
    cases.append(("duplicate-class", _json_text(duplicate), SAMPLE_MARKDOWN, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))
    missing_source = copy.deepcopy(base)
    del missing_source["decisions"][1]["source"]
    cases.append(("missing-source", _json_text(missing_source), SAMPLE_MARKDOWN, SAMPLE_REGISTRY, CANNOT, SCHEMA_ID))
    wrong_tag = copy.deepcopy(base)
    wrong_tag["decisions"][3]["outcome"] = "refuse"
    cases.append(("wrong-tag-action", _json_text(wrong_tag), SAMPLE_MARKDOWN, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))

    wrong_blob_outcome = copy.deepcopy(base)
    wrong_blob_outcome["decisions"][2]["outcome"] = "accept-if-landed-and-pushed"
    cases.append(("wrong-blob-outcome", _json_text(wrong_blob_outcome), SAMPLE_MARKDOWN, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))
    wrong_blob_finding = copy.deepcopy(base)
    wrong_blob_finding["decisions"][2]["finding"] = None
    cases.append(("wrong-blob-finding", _json_text(wrong_blob_finding), SAMPLE_MARKDOWN, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))
    missing_finding = copy.deepcopy(base)
    del missing_finding["decisions"][2]["finding"]
    cases.append(("missing-required-finding", _json_text(missing_finding), SAMPLE_MARKDOWN, SAMPLE_REGISTRY, CANNOT, SCHEMA_ID))
    source_swap = copy.deepcopy(base)
    source_swap["decisions"][0]["source"] = "S081"
    cases.append(("source-swap", _json_text(source_swap), SAMPLE_MARKDOWN, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))
    policy_omission = SAMPLE_MARKDOWN.replace(
        "Those object-prefix/ancestry/push restrictions come from the lane's evidence contract, not these manuals.",
        "These manuals state the lane policy.",
    )
    cases.append(("policy-omission", _json_text(base), policy_omission, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))

    duplicate_json = (
        '{"schema":"tsukuroi-selector-contract-v1",'
        '"schema":"tsukuroi-selector-contract-v1",'
        '"sources":["S081","S082"],"decisions":[]}'
    )
    cases.append(("duplicate-json-key", duplicate_json, SAMPLE_MARKDOWN, SAMPLE_REGISTRY, CANNOT, SCHEMA_ID))

    wrong_column = SAMPLE_MARKDOWN.replace(
        "| tree | Any tree is not commit-ish; non-empty tree is the measured control | refuse | E-REVISION-INVALID | S081; QUALITY27/36 |",
        "| tree | refuse | Any tree is not commit-ish; non-empty tree is the measured control | E-REVISION-INVALID | S081; QUALITY27/36 |",
    )
    cases.append(("wrong-table-column", _json_text(base), wrong_column, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))
    duplicate_variant = SAMPLE_MARKDOWN.replace(
        "| tag-to-commit |",
        "| BLOB | duplicate normalized class | refuse | E-REVISION-INVALID | S081; QUALITY27/36 |\n| tag-to-commit |",
        1,
    )
    cases.append(("duplicate-table-variant", _json_text(base), duplicate_variant, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))
    blob_line = "| blob | A blob is not commit-ish | refuse | E-REVISION-INVALID | S081; QUALITY27/36 |"
    comment_hidden = SAMPLE_MARKDOWN.replace(blob_line, "<!-- " + blob_line + " -->")
    cases.append(("comment-hidden-row", _json_text(base), comment_hidden, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))
    fence_hidden = SAMPLE_MARKDOWN.replace(
        blob_line,
        "```text\n" + blob_line + "\n```",
    )
    cases.append(("fence-hidden-row", _json_text(base), fence_hidden, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))
    nonrecursive = copy.deepcopy(base)
    nonrecursive["decisions"][3]["rationale"] = "Annotated tags peel to a commit; lane ancestry applies."
    nonrecursive_md = SAMPLE_MARKDOWN.replace(
        "Annotated tags, including nested annotated tags, peel recursively to the terminal commit",
        "Annotated tags peel to the terminal commit",
    )
    cases.append(("nonrecursive-tag", _json_text(nonrecursive), nonrecursive_md, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))

    source_column = SAMPLE_MARKDOWN.replace("| blob | A blob is not commit-ish | refuse | E-REVISION-INVALID | S081; QUALITY27/36 |",
                                           "| blob | A blob is not commit-ish | refuse | E-REVISION-INVALID | S082; QUALITY27/36 |")
    cases.append(("table-source-swap", _json_text(base), source_column, SAMPLE_REGISTRY, FAIL, MISMATCH_ID))
    cases.append(("missing-source-registry", _json_text(base), SAMPLE_MARKDOWN, "", FAIL, MISMATCH_ID))
    return cases


def selftest():
    failures = []
    cases = _selftest_cases()
    for label, raw, markdown, registry, expected_code, expected_id in cases:
        code, payload = evaluate(raw, markdown, registry)
        ids = {finding["id"] for finding in payload["findings"]}
        expected_ids = {expected_id} if expected_id else set()
        if code != expected_code or ids != expected_ids:
            failures.append(label)
    print(json.dumps({
        "status": "FAIL" if failures else "PASS",
        "cases": len(cases),
        "passed": len(cases) - len(failures),
        "failures": failures,
    }, sort_keys=True))
    return FAIL if failures else PASS


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
            return PASS
        code, payload = result(0, [{"id": "E-CLI", "detail": "invalid arguments"}], CANNOT)
        print(json.dumps(payload, sort_keys=True))
        return code
    if args.selftest:
        return selftest()
    try:
        binding = _revision.bind(ROOT, args.revision, args.branch)
        code, payload = evaluate(
            git_read(binding.sha, DATA),
            git_read(binding.sha, TEXT),
            git_read(binding.sha, SOURCES),
        )
        payload.update(revision=binding.sha, branch=binding.branch, branch_tip=binding.branch_tip)
    except _revision.RevisionError as exc:
        code, payload = result(0, [{"id": exc.fid, "detail": exc.detail}], CANNOT)
    except (OSError, RuntimeError, UnicodeError, subprocess.TimeoutExpired) as exc:
        code, payload = result(0, [{"id": E_READ, "detail": str(exc)[:120]}], CANNOT)
    print(json.dumps(payload, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
