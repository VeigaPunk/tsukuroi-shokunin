#!/usr/bin/env python3
"""Check declared review byte/predicate identity, never actual reading or nonexecution."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

sys.dont_write_bytecode = True
import _revision

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ".ufo/waves/round-21/reviews.json"


def safe_path(path):
    return (isinstance(path, str) and bool(path) and not path.startswith("/")
            and "\\" not in path and all(part not in ("", ".", "..") for part in path.split("/"))
            and not PurePosixPath(path).is_absolute())


def evaluate(raw, read_bytes):
    findings = []
    pinned, total, distinct = 0, 0, 0
    code = 0
    def add(fid, site):
        findings.append({"id": fid, "site": site})
    if raw is None:
        add("REVIEW-MANIFEST-MISSING", DEFAULT)
        code = 1
    else:
        try:
            data = json.loads(raw)
            reviews = data.get("reviews") if isinstance(data, dict) else None
            if (not isinstance(data, dict) or data.get("schema") != "tsukuroi-review-snapshots-v1"
                    or not isinstance(reviews, list) or not reviews):
                raise ValueError("invalid manifest shape")
            names, reports = set(), set()
            for row in reviews:
                if (not isinstance(row, dict) or not isinstance(row.get("name"), str)
                        or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", row["name"])
                        or row["name"] in names or not safe_path(row.get("report"))
                        or row["report"] in reports or not safe_path(row.get("source"))
                        or not isinstance(row.get("sha256"), str)
                        or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"])
                        or not isinstance(row.get("predicate"), str) or not row["predicate"]
                        or any(c in row["predicate"] for c in "\r\n")):
                    raise ValueError("invalid/duplicate review identity or path")
                names.add(row["name"])
                reports.add(row["report"])
            total = len(reviews)
            distinct = len({row["source"] for row in reviews})
            for row in reviews:
                start = len(findings)
                source = read_bytes(row["source"])
                report = read_bytes(row["report"])
                if source is None or hashlib.sha256(source).hexdigest() != row["sha256"]:
                    add("REVIEW-SNAPSHOT-MISMATCH", row["name"])
                if report is None:
                    add("REVIEW-REPORT-MISSING", row["name"])
                else:
                    text = report.decode("utf-8")
                    lines = text.splitlines()
                    digest_lines = [line for line in lines if line.startswith("Reviewed-SHA256:")]
                    predicate_lines = [line for line in lines if line.startswith("Predicate:")]
                    scope_lines = [line for line in lines if line.startswith("Scope:")]
                    if digest_lines != ["Reviewed-SHA256: " + row["sha256"]]:
                        add("REVIEW-SNAPSHOT-MISMATCH", row["name"])
                    if predicate_lines != ["Predicate: " + row["predicate"]]:
                        add("REVIEW-PREDICATE-MISMATCH", row["name"])
                    if scope_lines != ["Scope: executed=none"]:
                        add("REVIEW-SCOPE-MISMATCH", row["name"])
                if len(findings) == start:
                    pinned += 1
            code = 1 if findings else 0
        except (ValueError, TypeError, UnicodeError) as exc:
            add("REVIEW-MANIFEST-SCHEMA", str(exc)[:100])
            code = 2
    return code, {"status": ("PASS", "FAIL", "CANNOT_EVALUATE")[code],
                  "distinct_source_files": distinct,
                  "pinned_reviews": pinned, "total_reviews": total, "findings": findings,
                  "scope": "primary snapshot and predicate declarations only; not proof of reading, chronology or command nonexecution"}


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
    return proc.stdout


def selftest():
    sha = hashlib.sha256(b"fixed source\n").hexdigest()
    manifest = {"schema": "tsukuroi-review-snapshots-v1", "reviews": [
        {"name": "One", "report": "wave/One.md", "source": "snapshot/tool.py",
         "sha256": sha, "predicate": "fixed-five-decisions"}]}
    report = (f"Reviewed-SHA256: {sha}\nPredicate: fixed-five-decisions\nScope: executed=none\n").encode()
    files = {"snapshot/tool.py": b"fixed source\n", "wave/One.md": report}
    cases = [("clean", manifest, files, 0, set()),
             ("missing-manifest", None, files, 1, {"REVIEW-MANIFEST-MISSING"}),
             ("missing-report", manifest, {"snapshot/tool.py": b"fixed source\n"}, 1, {"REVIEW-REPORT-MISSING"}),
             ("source-tamper", manifest, {**files, "snapshot/tool.py": b"changed\n"}, 1, {"REVIEW-SNAPSHOT-MISMATCH"}),
             ("report-digest", manifest, {**files, "wave/One.md": report.replace(sha.encode(), b"0" * 64)}, 1, {"REVIEW-SNAPSHOT-MISMATCH"}),
             ("predicate", manifest, {**files, "wave/One.md": report.replace(b"fixed-five-decisions", b"other")}, 1, {"REVIEW-PREDICATE-MISMATCH"}),
             ("scope-period", manifest, {**files, "wave/One.md": report.replace(b"executed=none", b"executed=none.")}, 1, {"REVIEW-SCOPE-MISMATCH"}),
             ("duplicate-digest", manifest, {**files, "wave/One.md": report + f"Reviewed-SHA256: {sha}\n".encode()}, 1, {"REVIEW-SNAPSHOT-MISMATCH"})]
    for name, mutate in (("duplicate", lambda d: d["reviews"].append(d["reviews"][0])),
                         ("traversal", lambda d: d["reviews"][0].update(source="../sibling")),
                         ("absolute", lambda d: d["reviews"][0].update(report="/tmp/report")),
                         ("empty", lambda d: d.update(reviews=[]))):
        data = copy.deepcopy(manifest)
        mutate(data)
        cases.append((name, data, files, 2, {"REVIEW-MANIFEST-SCHEMA"}))
    failures = []
    for name, data, surfaces, want_code, want_ids in cases:
        raw = json.dumps(data) if data is not None else None
        code, payload = evaluate(raw, surfaces.get)
        if code != want_code or {row["id"] for row in payload["findings"]} != want_ids:
            failures.append(name)
    print(json.dumps({"status": "FAIL" if failures else "PASS", "cases": len(cases),
                      "passed": len(cases) - len(failures), "failures": failures}))
    return 1 if failures else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--revision")
    choice.add_argument("--selftest", action="store_true")
    parser.add_argument("--branch", default="master")
    parser.add_argument("--manifest", default=DEFAULT)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    if args.selftest:
        return selftest()
    if not safe_path(args.manifest):
        print(json.dumps({"status": "CANNOT_EVALUATE", "pinned_reviews": 0,
                          "findings": [{"id": "REVIEW-MANIFEST-SCHEMA", "site": "manifest path"}]}))
        return 2
    try:
        binding = _revision.bind(ROOT, args.revision, args.branch)
        code, payload = evaluate(git_read(binding.sha, args.manifest),
                                 lambda path: git_read(binding.sha, path))
        payload.update(revision=binding.sha, branch=binding.branch, branch_tip=binding.branch_tip)
    except _revision.RevisionError as exc:
        code, payload = 2, {"status": "CANNOT_EVALUATE", "pinned_reviews": 0,
                            "findings": [{"id": exc.fid, "site": exc.site}]}
    except (OSError, RuntimeError, UnicodeError, subprocess.TimeoutExpired) as exc:
        code, payload = 2, {"status": "CANNOT_EVALUATE", "pinned_reviews": 0,
                            "findings": [{"id": "E-READ", "site": str(exc)[:120]}]}
    print(json.dumps(payload, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
