#!/usr/bin/env python3
"""Check the fixed five-row selector contract at one landed revision.

The gate reads only the two named committed blobs with `git show`; it does not fetch
source documents or exercise Git's selector behavior. `_revision.bind` supplies the
shared object-ID and landed binding. A missing origin tracking ref is not evidence of
push and is therefore refused by this lane's stricter acceptance policy.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
STATUS = {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}
CONTRACT_JSON = "corpus/knowledge/selector-contract-r21.json"
CONTRACT_MARKDOWN = "corpus/knowledge/selector-contract-r21.md"
SCHEMA_ID = "SELECTOR-CONTRACT-SCHEMA"
MISSING_ID = "SELECTOR-CONTRACT-MISSING"
MISMATCH_ID = "SELECTOR-CONTRACT-MISMATCH"
PASS_ID = "SELECTOR-CONTRACT-PASS"
ROOT_KEYS = frozenset(("schema_version", "sources", "rows"))
SOURCE_KEYS = frozenset(("id", "url", "section"))
ROW_KEYS = frozenset(("id", "class", "outcome", "finding", "rationale", "source", "proposition"))
SOURCE_RECORDS = {
    "S081": {
        "url": "https://git-scm.com/docs/gitrevisions/2.56.0",
        "section": "SPECIFYING REVISIONS",
    },
    "S082": {
        "url": "https://git-scm.com/docs/git-rev-parse/2.56.0",
        "section": "--verify",
    },
}
# This policy map is deliberately independent of the input JSON and companion draft.
EXPECTED_ROWS = {
    "commit": {
        "class": "commit",
        "outcome": "accept-if-landed-and-pushed",
        "finding": None,
        "proposition": "Commit object IDs may select commits; acceptance additionally requires landed and pushed ancestry.",
    },
    "tree": {
        "class": "tree",
        "outcome": "refuse",
        "finding": "E-REVISION-INVALID",
        "proposition": "Tree object IDs are not commits and are refused.",
    },
    "blob": {
        "class": "blob",
        "outcome": "refuse",
        "finding": "E-REVISION-INVALID",
        "proposition": "Blob object IDs are not commits and are refused.",
    },
    "tag-to-commit": {
        "class": "tag-to-commit",
        "outcome": "accept-if-landed-and-pushed",
        "finding": None,
        "proposition": "Annotated tag object IDs peeling to commits are commit-ish; acceptance additionally requires landed and pushed ancestry.",
    },
    "tag-to-noncommit": {
        "class": "tag-to-noncommit",
        "outcome": "refuse",
        "finding": "E-REVISION-INVALID",
        "proposition": "Annotated tag object IDs peeling to non-commits are refused.",
    },
}


def _repo_root():
    """Find the repository whether this draft is run in place or promoted to tools/."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "tools" / "_revision.py").is_file():
            return parent
    raise RuntimeError("cannot locate shared tools/_revision.py")


ROOT = _repo_root()
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
from _revision import (  # noqa: E402
    E_GIT,
    E_NOT_PUSHED,
    RevisionError,
    bind as bind_revision,
)


class GateError(Exception):
    def __init__(self, code, finding_id, site, detail):
        super().__init__(detail)
        self.code = code
        self.finding_id = finding_id
        self.site = site
        self.detail = detail


def _result(code, finding_id, detail="", site="selector-contract", decision_rows=0):
    finding = []
    if code != PASS:
        finding = [{"id": finding_id, "site": site, "detail": detail[:160]}]
    return {
        "exit_code": code,
        "status": STATUS[code],
        "id": finding_id,
        "decision_rows": decision_rows,
        "findings": finding,
    }


def _clean_git_env():
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update({
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_PAGER": "cat",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "LC_ALL": "C",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_TERMINAL_PROMPT": "0",
    })
    return env


def _git(root, *args):
    try:
        return subprocess.run(
            ["git", "--no-pager", "-C", str(root), *args],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=_clean_git_env(),
            timeout=60,
            check=False,
        )
    except subprocess.TimeoutExpired:
        raise GateError(CANNOT, E_GIT, "git", "git read exceeded 60 seconds")
    except OSError as exc:
        raise GateError(CANNOT, E_GIT, "git", str(exc)[:120])


def _read_committed_file(root, revision, path):
    """Read a fixed path from an immutable commit; distinguish absence from read failure."""
    proc = _git(root, "show", "--format=", f"{revision}:{path}")
    if proc.returncode == 0:
        return proc.stdout

    tree = _git(root, "ls-tree", "-r", "--name-only", "-z", revision, "--", path)
    if tree.returncode != 0:
        raise GateError(CANNOT, E_GIT, path, "cannot inspect the committed contract tree")
    names = {name for name in tree.stdout.decode("utf-8", "replace").split("\0") if name}
    if path not in names:
        raise GateError(FAIL, MISSING_ID, path, "required committed contract file is absent")
    raise GateError(CANNOT, E_GIT, path, "git show failed for a committed contract file")


def _unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def _reject_json_constant(value):
    raise ValueError(f"non-JSON constant: {value}")


def _schema_failure(detail, decision_rows=0):
    return _result(CANNOT, SCHEMA_ID, detail, decision_rows=decision_rows)


def _md_normalize(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"<[^>]*>", " ", text)
    text = re.sub(r"[*_~]", "", text)
    return " ".join(text.split()).casefold()


def _markdown_blocks(text):
    blocks = []
    paragraph = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            if paragraph:
                blocks.append("\n".join(paragraph))
                paragraph = []
            blocks.append(line)
        elif not stripped:
            if paragraph:
                blocks.append("\n".join(paragraph))
                paragraph = []
        elif re.match(r"^\s*#{1,6}\s+", line) and paragraph:
            blocks.append("\n".join(paragraph))
            paragraph = [line]
        else:
            paragraph.append(line)
    if paragraph:
        blocks.append("\n".join(paragraph))
    return blocks


def _markdown_has_row(markdown, row_id, proposition):
    wanted = _md_normalize(proposition)
    id_pattern = re.compile(rf"(?<![a-z0-9_-]){re.escape(row_id)}(?![a-z0-9_-])")
    for block in _markdown_blocks(markdown):
        normalized = _md_normalize(block)
        if wanted not in normalized:
            continue
        if block.lstrip().startswith("|"):
            first_cell = block.strip().strip("|").split("|", 1)[0]
            if _md_normalize(first_cell) == row_id:
                return True
        elif id_pattern.search(normalized):
            return True
    return False


def evaluate(contract_text, markdown_text):
    """Evaluate already-read committed source text without filesystem or Git access."""
    if markdown_text is None:
        return _result(FAIL, MISSING_ID, "required committed Markdown contract is absent", decision_rows=0)
    try:
        contract = json.loads(
            contract_text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_json_constant,
        )
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        return _schema_failure(f"malformed contract JSON: {str(exc)[:120]}")

    raw_rows = contract.get("rows") if isinstance(contract, dict) else None
    decision_rows = len(raw_rows) if isinstance(raw_rows, list) else 0
    if not isinstance(contract, dict) or set(contract) != ROOT_KEYS:
        return _schema_failure("contract must contain exactly schema_version, sources, and rows", decision_rows)
    if type(contract["schema_version"]) is not int or contract["schema_version"] != 1:
        return _schema_failure("schema_version must be integer 1", decision_rows)
    if not isinstance(markdown_text, str):
        return _schema_failure("Markdown contract must be UTF-8 text", decision_rows)

    sources = contract["sources"]
    if not isinstance(sources, list):
        return _schema_failure("sources must be a list", decision_rows)
    source_ids = set()
    for source in sources:
        if not isinstance(source, dict) or set(source) != SOURCE_KEYS:
            return _schema_failure("each source must contain exactly id, url, and section", decision_rows)
        source_id = source["id"]
        if not isinstance(source_id, str) or source_id not in SOURCE_RECORDS or source_id in source_ids:
            return _schema_failure("source IDs must be unique S081/S082 entries", decision_rows)
        source_ids.add(source_id)
        expected_source = SOURCE_RECORDS[source_id]
        if source["url"] != expected_source["url"] or source["section"] != expected_source["section"]:
            return _result(FAIL, MISMATCH_ID, f"source record {source_id} differs from the pinned citation", decision_rows=decision_rows)
    if source_ids != set(SOURCE_RECORDS):
        return _schema_failure("both S081 and S082 source records are required", decision_rows)

    rows = contract["rows"]
    if not isinstance(rows, list):
        return _schema_failure("rows must be a list", decision_rows)
    for row in rows:
        if not isinstance(row, dict) or set(row) != ROW_KEYS:
            return _schema_failure("each row must contain exactly the seven declared fields", decision_rows)
        if not isinstance(row["id"], str):
            return _schema_failure("row id must be text", decision_rows)
        if not isinstance(row["rationale"], str) or not row["rationale"].strip():
            return _schema_failure("row rationale must be non-empty text", decision_rows)
        if not isinstance(row["source"], str) or row["source"] not in source_ids:
            return _schema_failure("row source must reference S081 or S082", decision_rows)

    row_ids = [row["id"] for row in rows]
    if len(row_ids) != len(set(row_ids)):
        return _result(FAIL, MISMATCH_ID, "decision row IDs are not unique", decision_rows=decision_rows)
    if len(rows) != len(EXPECTED_ROWS) or set(row_ids) != set(EXPECTED_ROWS):
        return _result(FAIL, MISMATCH_ID, "contract must contain exactly the five required decision rows", decision_rows=decision_rows)

    for row in rows:
        expected = EXPECTED_ROWS[row["id"]]
        for field in ("class", "outcome", "finding", "proposition"):
            if row[field] != expected[field]:
                return _result(FAIL, MISMATCH_ID, f"row {row['id']} has unsupported {field}", decision_rows=decision_rows)
        if not _markdown_has_row(markdown_text, row["id"], expected["proposition"]):
            return _result(FAIL, MISMATCH_ID, f"Markdown lacks named row {row['id']} or its required proposition", decision_rows=decision_rows)

    return _result(PASS, PASS_ID, decision_rows=decision_rows)


def _fixture_contract():
    sources = [
        {"id": source_id, **record}
        for source_id, record in SOURCE_RECORDS.items()
    ]
    rows = []
    for row_id, expected in EXPECTED_ROWS.items():
        source_id = "S082" if row_id == "commit" else "S081"
        rows.append({
            "id": row_id,
            "class": expected["class"],
            "outcome": expected["outcome"],
            "finding": expected["finding"],
            "rationale": f"{expected['proposition']} Git documentation grounds selector semantics; lane policy adds object identity and landed/pushed ancestry.",
            "source": source_id,
            "proposition": expected["proposition"],
        })
    return {"schema_version": 1, "sources": sources, "rows": rows}


def _fixture_markdown(contract):
    lines = ["# Selector contract", "", "| ID | Proposition |", "|---|---|"]
    for row in contract["rows"]:
        lines.append(f"| {row['id']} | {row['proposition']} |")
    return "\n".join(lines) + "\n"


def selftest():
    base = _fixture_contract()
    cases = []
    cases.append(("clean", base, _fixture_markdown(base), PASS, PASS_ID))

    missing_row = json.loads(json.dumps(base))
    missing_row["rows"].pop()
    cases.append(("missing-row", missing_row, _fixture_markdown(base), FAIL, MISMATCH_ID))

    wrong_tree = json.loads(json.dumps(base))
    next(row for row in wrong_tree["rows"] if row["id"] == "tree")["outcome"] = "accept-if-landed-and-pushed"
    cases.append(("wrong-tree-action", wrong_tree, _fixture_markdown(wrong_tree), FAIL, MISMATCH_ID))

    duplicate = json.loads(json.dumps(base))
    duplicate["rows"].append(dict(duplicate["rows"][0]))
    cases.append(("duplicate", duplicate, _fixture_markdown(duplicate), FAIL, MISMATCH_ID))

    missing_source = json.loads(json.dumps(base))
    del missing_source["rows"][0]["source"]
    cases.append(("missing-source", missing_source, _fixture_markdown(missing_source), CANNOT, SCHEMA_ID))

    wrong_tag = json.loads(json.dumps(base))
    next(row for row in wrong_tag["rows"] if row["id"] == "tag-to-commit")["outcome"] = "refuse"
    cases.append(("wrong-tag-action", wrong_tag, _fixture_markdown(wrong_tag), FAIL, MISMATCH_ID))
    cases.append(("missing-markdown", base, None, FAIL, MISSING_ID))

    failures = []
    for name, contract, markdown, expected_code, expected_id in cases:
        result = evaluate(json.dumps(contract), markdown)
        passed = result["exit_code"] == expected_code and result["id"] == expected_id
        print(f"{'PASS' if passed else 'FAIL'} {name} (exit={result['exit_code']} id={result['id']})")
        if not passed:
            failures.append(name)
    passed_count = len(cases) - len(failures)
    print(f"SELECTOR_CONTRACT_SELFTEST: {'PASS' if not failures else 'FAIL'} ({passed_count}/{len(cases)} cases)")
    return PASS if not failures else FAIL


def _emit(result, revision=None, branch=None, branch_tip=None, origin_tip=None):
    payload = dict(result)
    if revision is not None:
        payload.update({
            "revision": revision,
            "branch": branch,
            "branch_tip": branch_tip,
            "origin_tip": origin_tip,
        })
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return result["exit_code"]


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--revision", metavar="HEX", help="bind a 7-64 digit object ID to the selected branch")
    selector.add_argument("--selftest", action="store_true", help="run hermetic in-memory contract checks")
    parser.add_argument("--branch", default="master", help="local branch name (default: master)")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.selftest:
        return selftest()

    try:
        binding = bind_revision(ROOT, args.revision, args.branch)
    except RevisionError as exc:
        result = _result(CANNOT, exc.fid, str(exc)[:160], site=exc.site)
        return _emit(result, branch=args.branch)

    if binding.origin_tip is None:
        result = _result(
            CANNOT,
            E_NOT_PUSHED,
            "origin tracking ref is absent; pushed ancestry cannot be established",
            site=f"refs/remotes/origin/{binding.branch}",
        )
        return _emit(result, binding.sha, binding.branch, binding.branch_tip, binding.origin_tip)

    try:
        json_bytes = _read_committed_file(ROOT, binding.sha, CONTRACT_JSON)
        markdown_bytes = _read_committed_file(ROOT, binding.sha, CONTRACT_MARKDOWN)
    except GateError as exc:
        result = _result(exc.code, exc.finding_id, exc.detail, site=exc.site)
        return _emit(result, binding.sha, binding.branch, binding.branch_tip, binding.origin_tip)

    try:
        contract_text = json_bytes.decode("utf-8")
        markdown_text = markdown_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        result = _schema_failure(f"contract source is not UTF-8: {str(exc)[:100]}")
        return _emit(result, binding.sha, binding.branch, binding.branch_tip, binding.origin_tip)

    result = evaluate(contract_text, markdown_text)
    return _emit(result, binding.sha, binding.branch, binding.branch_tip, binding.origin_tip)


if __name__ == "__main__":
    sys.exit(main())
