#!/usr/bin/env python3
"""Check preregistered source-byte and review-predicate receipts at a landed revision.

The manifest is ``.ufo/waves/round-21/reviews.json`` by default and has schema
``tsukuroi-review-snapshots-v1``. Each declared source is read as a committed Git
blob and checked against its lowercase SHA-256. Its committed report must contain
one exact standalone ``Reviewed-SHA256``, ``Predicate``, and ``Scope`` receipt.
Only immutable objects at the commit accepted by ``tools/_revision.py`` are read;
there is no worktree mode.

The manifest is expected to have been committed as preregistration before review;
that chronology comes from the committed preregistration/spec, not mutable file
or commit timestamps, and is not independently established by this gate. Receipts
are declarations: they do not prove the reviewer read those bytes or that no
command ran. Exit 0 is clean, 1 is a declared review finding, and 2 means the
manifest or evidence could not be evaluated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import namedtuple
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
REVISION_TOOLS = ROOT / ".ufo" / "waves" / "round-21" / "snapshot" / "tools"
sys.path.insert(0, str(REVISION_TOOLS))
from _revision import RevisionError, bind as bind_revision, clean_env

PASS, FAIL, CANNOT = 0, 1, 2
SCHEMA = "tsukuroi-review-snapshots-v1"
DEFAULT_MANIFEST = ".ufo/waves/round-21/reviews.json"
PATH_CHARS = re.compile(r"^[A-Za-z0-9._/-]+$")
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REVIEW_KEYS = {"name", "report", "source", "sha256", "predicate"}
MANIFEST_KEYS = {"schema", "reviews"}
Finding = namedtuple("Finding", "id site detail")
Review = namedtuple("Review", "name report source sha256 predicate")
Result = namedtuple("Result", "code pinned_reviews total_reviews findings")


class Cannot(Exception):
    def __init__(self, fid, site, detail, total_reviews=0):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail
        self.total_reviews = total_reviews


def safe_path(value, site, total_reviews=0):
    """Accept one conservative repository-relative Git path, never traversal."""
    if (not isinstance(value, str) or not value or not PATH_CHARS.fullmatch(value)
            or value.startswith("/")):
        raise Cannot("REVIEW-PATH-INVALID", site,
                     "lane-relative path required", total_reviews)
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise Cannot("REVIEW-PATH-INVALID", site,
                     "empty, dot, and parent path components are forbidden",
                     total_reviews)
    return value


def _object_no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON member {key!r}")
        result[key] = value
    return result


def load_manifest(raw):
    """Parse and validate every declared row; malformed rows are never skipped."""
    try:
        text = raw.decode("utf-8")
        manifest = json.loads(text, object_pairs_hook=_object_no_duplicates)
    except (AttributeError, UnicodeDecodeError, ValueError) as exc:
        raise Cannot("REVIEW-MANIFEST-INVALID", "manifest",
                     f"invalid UTF-8/JSON: {str(exc)[:100]}") from exc

    declared = manifest.get("reviews") if isinstance(manifest, dict) else None
    total = len(declared) if isinstance(declared, list) else 0
    if (not isinstance(manifest, dict) or set(manifest) != MANIFEST_KEYS
            or manifest.get("schema") != SCHEMA
            or not isinstance(declared, list)):
        raise Cannot("REVIEW-MANIFEST-INVALID", "manifest",
                     "expected schema and reviews list", total)

    reviews = []
    names = set()
    for index, row in enumerate(declared):
        site = f"reviews[{index}]"
        if not isinstance(row, dict) or set(row) != REVIEW_KEYS:
            raise Cannot("REVIEW-MANIFEST-INVALID", site,
                         "row must contain exactly name, report, source, sha256, predicate",
                         total)
        name = row["name"]
        if not isinstance(name, str) or not NAME.fullmatch(name):
            raise Cannot("REVIEW-MANIFEST-INVALID", f"{site}.name",
                         "unsafe review name", total)
        if name in names:
            raise Cannot("REVIEW-DUPLICATE-NAME", f"{site}.name",
                         f"duplicate review name {name!r}", total)
        names.add(name)
        report = safe_path(row["report"], f"{site}.report", total)
        source = safe_path(row["source"], f"{site}.source", total)
        digest = row["sha256"]
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            raise Cannot("REVIEW-MANIFEST-INVALID", f"{site}.sha256",
                         "lowercase SHA-256 digest required", total)
        predicate = row["predicate"]
        if (not isinstance(predicate, str) or not predicate
                or any(ord(char) < 32 or ord(char) == 127 for char in predicate)):
            raise Cannot("REVIEW-MANIFEST-INVALID", f"{site}.predicate",
                         "nonempty single-line predicate required", total)
        reviews.append(Review(name, report, source, digest, predicate))
    return reviews


def _one_exact_receipt(text, label, expected):
    prefix = label + ":"
    values = [line for line in text.splitlines() if line.startswith(prefix)]
    return len(values) == 1 and values[0] == expected


def evaluate(manifest_bytes, objects):
    """Evaluate against a path-to-blob-bytes fixture or committed blob map."""
    if manifest_bytes is None:
        return Result(FAIL, 0, 0, [Finding(
            "REVIEW-MANIFEST-MISSING", "manifest", "manifest absent at bound revision")])
    try:
        reviews = load_manifest(manifest_bytes)
    except Cannot as exc:
        return Result(CANNOT, 0, exc.total_reviews, [
            Finding(exc.fid, exc.site, exc.detail)])

    findings = []
    pinned = 0
    cannot = False
    for review in reviews:
        source = objects.get(review.source)
        if source is None:
            findings.append(Finding(
                "REVIEW-SNAPSHOT-MISMATCH", review.source,
                f"committed source missing; expected SHA-256 {review.sha256}"))
        else:
            actual = hashlib.sha256(source).hexdigest()
            if actual == review.sha256:
                pinned += 1
            else:
                findings.append(Finding(
                    "REVIEW-SNAPSHOT-MISMATCH", review.source,
                    f"expected {review.sha256}, committed source is {actual}"))

        report = objects.get(review.report)
        if report is None:
            findings.append(Finding(
                "REVIEW-REPORT-MISSING", review.report,
                f"report declared by review {review.name!r} is absent"))
            continue
        try:
            text = report.decode("utf-8")
        except UnicodeDecodeError:
            findings.append(Finding(
                "REVIEW-SNAPSHOT-MISMATCH", review.report,
                "committed report is not valid UTF-8"))
            continue

        expected_hash = f"Reviewed-SHA256: {review.sha256}"
        if not _one_exact_receipt(text, "Reviewed-SHA256", expected_hash):
            findings.append(Finding(
                "REVIEW-SNAPSHOT-MISMATCH", review.report,
                f"requires exactly one standalone {expected_hash!r} line"))
        expected_predicate = f"Predicate: {review.predicate}"
        if not _one_exact_receipt(text, "Predicate", expected_predicate):
            findings.append(Finding(
                "REVIEW-PREDICATE-MISMATCH", review.report,
                f"requires exactly one standalone {expected_predicate!r} line"))
        expected_scope = "Scope: executed=none"
        if not _one_exact_receipt(text, "Scope", expected_scope):
            findings.append(Finding(
                "REVIEW-SCOPE-MISMATCH", review.report,
                f"requires exactly one standalone {expected_scope!r} line"))

    code = CANNOT if cannot else FAIL if findings else PASS
    return Result(code, pinned, len(reviews), findings)


def git(root, *args):
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(root), *args],
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=clean_env(), timeout=30)
    except subprocess.TimeoutExpired:
        raise Cannot("REVIEW-GIT-FAILED", "git", "git command exceeded 30s")
    except OSError as exc:
        raise Cannot("REVIEW-GIT-FAILED", "git", str(exc)[:120])


def committed_blob(root, revision, path):
    """Return regular-file bytes from the immutable tree, or None if absent."""
    listing = git(root, "ls-tree", "-z", "--full-tree", revision, "--", path)
    if listing.returncode != 0:
        detail = listing.stderr.decode("utf-8", "replace").strip()[:120]
        raise Cannot("REVIEW-GIT-FAILED", path, detail or "git ls-tree failed")
    path_bytes = path.encode("ascii")
    for entry in listing.stdout.split(b"\0"):
        if not entry:
            continue
        try:
            header, entry_path = entry.split(b"\t", 1)
            mode, kind, oid = header.split()
        except ValueError:
            raise Cannot("REVIEW-GIT-FAILED", path, "malformed git ls-tree output")
        if entry_path != path_bytes:
            continue
        if mode not in (b"100644", b"100755") or kind != b"blob":
            return None
        blob = git(root, "cat-file", "blob", oid.decode("ascii"))
        if blob.returncode != 0:
            detail = blob.stderr.decode("utf-8", "replace").strip()[:120]
            raise Cannot("REVIEW-GIT-FAILED", path, detail or "git cat-file failed")
        return blob.stdout
    return None


def build_parser():
    parser = argparse.ArgumentParser(
        description="Check committed review source and predicate receipts.",
        exit_on_error=False)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--revision", metavar="HEX",
                       help="7-64 hex commit; reads immutable Git objects only")
    modes.add_argument("--selftest", action="store_true",
                       help="run hermetic in-memory fixtures")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST, metavar="PATH",
                        help=f"lane-relative committed manifest (default {DEFAULT_MANIFEST})")
    parser.add_argument("--branch", default="master", metavar="REF",
                        help="branch the revision must be landed on (default master)")
    return parser


def emit(result, revision=None, branch=None, branch_tip=None, manifest=None):
    status = {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[result.code]
    payload = {
        "status": status,
        "revision": revision,
        "branch": branch,
        "branch_tip": branch_tip,
        "manifest": manifest,
        "pinned_reviews": result.pinned_reviews,
        "total_reviews": result.total_reviews,
        "findings": [
            {"id": finding.id, "site": finding.site, "detail": finding.detail}
            for finding in result.findings
        ],
        "evidence_class": "committed source-byte hashes and self-reported predicate/scope receipts",
        "limits": [
            "does not prove that a reviewer read the pinned bytes",
            "does not independently prove that no command ran",
            "does not verify chronology from timestamps or discover unlisted reports",
        ],
    }
    print(json.dumps(payload, sort_keys=True))
    return result.code


def selftest():
    source_path = "src/example.py"
    report_path = "reviews/Example.md"
    source = b"def answer(): return 42\n"
    digest = hashlib.sha256(source).hexdigest()
    predicate = "C3-example-predicate"

    def row(name="Example", report=report_path, source_name=source_path,
            sha=digest, pred=predicate):
        return {"name": name, "report": report, "source": source_name,
                "sha256": sha, "predicate": pred}

    def manifest(rows):
        return json.dumps({"schema": SCHEMA, "reviews": rows},
                          sort_keys=True).encode("utf-8")

    def report_text(reviewed=digest, pred=predicate,
                    scope="Scope: executed=none"):
        return (f"Reviewed-SHA256: {reviewed}\nPredicate: {pred}\n"
                f"{scope}\n").encode("utf-8")

    base_objects = {source_path: source,
                    report_path: report_text()}
    duplicate_rows = [row(), row(name="Example")]
    traversal_rows = [row(source_name="../src/example.py")]
    cases = [
        ("clean", manifest([row()]), base_objects, PASS, []),
        ("manifest-missing", None, {}, FAIL, ["REVIEW-MANIFEST-MISSING"]),
        ("tampered-source", manifest([row()]),
         {**base_objects, source_path: b"def answer(): return 43\n"},
         FAIL, ["REVIEW-SNAPSHOT-MISMATCH"]),
        ("wrong-report-digest", manifest([row()]),
         {**base_objects, report_path: report_text(reviewed="0" * 64)},
         FAIL, ["REVIEW-SNAPSHOT-MISMATCH"]),
        ("wrong-predicate", manifest([row()]),
         {**base_objects, report_path: report_text(pred="different-predicate")},
         FAIL, ["REVIEW-PREDICATE-MISMATCH"]),
        ("missing-report", manifest([row()]), {source_path: source},
         FAIL, ["REVIEW-REPORT-MISSING"]),
        ("scope-period", manifest([row()]),
         {**base_objects, report_path: report_text(scope="Scope: executed=none.")},
         FAIL, ["REVIEW-SCOPE-MISMATCH"]),
        ("duplicate-name", manifest(duplicate_rows), base_objects,
         CANNOT, ["REVIEW-DUPLICATE-NAME"]),
        ("path-traversal", manifest(traversal_rows), base_objects,
         CANNOT, ["REVIEW-PATH-INVALID"]),
        ("malformed-json", b'{"schema":', {},
         CANNOT, ["REVIEW-MANIFEST-INVALID"]),
        ("malformed-row", manifest([{"name": "Example"}]), {},
         CANNOT, ["REVIEW-MANIFEST-INVALID"]),
    ]
    passed, failures = 0, []
    for name, manifest_bytes, objects, want_code, want_ids in cases:
        result = evaluate(manifest_bytes, objects)
        got_ids = sorted(finding.id for finding in result.findings)
        problems = []
        if result.code != want_code:
            problems.append(f"exit={result.code}/{want_code}")
        if got_ids != sorted(want_ids):
            problems.append("ids=" + ",".join(got_ids) + "/want="
                            + ",".join(sorted(want_ids)))
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))
        else:
            passed += 1

    if failures:
        print(f"CHECK_REVIEW_SNAPSHOTS_SELFTEST: FAIL ({len(cases)} cases, "
              f"{passed} passed, {len(failures)} failed)")
        print("\n".join("  " + failure for failure in failures))
        return FAIL
    print(f"CHECK_REVIEW_SNAPSHOTS_SELFTEST: PASS ({len(cases)} cases, "
          f"{passed} passed, 0 failed)")
    return PASS


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:
        if not exc.code:
            return PASS
        result = Result(CANNOT, 0, 0, [Finding(
            "REVIEW-CLI", "cli", "--revision HEX or --selftest required")])
        return emit(result)
    if args.selftest:
        return selftest()

    revision, branch, branch_tip = args.revision, args.branch, None
    manifest_path = None
    try:
        manifest_path = safe_path(args.manifest, "manifest")
        try:
            bound = bind_revision(ROOT, revision, branch)
        except RevisionError as exc:
            raise Cannot(exc.fid, exc.site, exc.detail) from exc
        revision, branch_tip = bound.sha, bound.branch_tip
        manifest_bytes = committed_blob(ROOT, revision, manifest_path)
        objects = {}
        if manifest_bytes is not None:
            try:
                reviews = load_manifest(manifest_bytes)
            except Cannot:
                reviews = []
            for review in reviews:
                for path in (review.source, review.report):
                    if path not in objects:
                        objects[path] = committed_blob(ROOT, revision, path)
        result = evaluate(manifest_bytes, objects)
    except Cannot as exc:
        result = Result(CANNOT, 0, exc.total_reviews, [
            Finding(exc.fid, exc.site, exc.detail)])
    except Exception as exc:
        result = Result(CANNOT, 0, 0, [
            Finding("REVIEW-INTERNAL", "gate", str(exc)[:120])])
    return emit(result, revision, branch, branch_tip, manifest_path)


if __name__ == "__main__":
    sys.exit(main())
