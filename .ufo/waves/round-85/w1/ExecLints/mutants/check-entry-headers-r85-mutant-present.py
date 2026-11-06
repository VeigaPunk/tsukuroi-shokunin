#!/usr/bin/env python3
"""Entry-header check (round 85; bounded first-12-lines window, path-scoped).

Round-84 spot-check routed defect 1: `corpus/knowledge/hibernate-resume-plane-r84.md`
landed with `verified-at:` only. QUALITY 8 requires `source:` and `recheck:` as well,
and the corpus convention is that a reader sees them at the top of the note, before
the body — a `recheck:` buried at line 76 is not a header a reader finds.

Rule (frozen for round 85): for every PATH named on the command line, read the blob
with `git show REV:PATH` and report one finding per absent key when the file carries
no line starting at column 0 with `source:` or no line starting at column 0 with
`recheck:` **within its first 12 physical lines** (1..12 inclusive, end-of-file
shorter than that included).

Reuse, not duplication: `tools/check-knowledge-header.py` (QUALITY 8, rounds 33-34)
already owns the lane's header grammar — column 0 only, outside ``` / ~~~ fences, the
last occurrence operative. This check imports that module's `header_lines` parser
and applies only what the lane gate does not: the first-12-lines window, an explicit
PATH list, and the `source:`/`recheck:` subset (the lane gate also demands a dated
`verified-at:` across the whole note). It is a bounded companion, not a replacement;
if the parser module cannot be loaded the check refuses (rc 2) rather than growing a
second copy of the grammar.

Exit: 0 every named file carries both lines in its window; 1 at least one finding;
2 could-not-evaluate (bad revision, unreadable blob, parser module unavailable,
malformed CLI). JSON on stdout, sorted keys. Read-only: git plumbing reads only,
nothing on disk or in the repository is written (`sys.dont_write_bytecode`).

Usage:
    python3 check-entry-headers-r85.py --revision <REV> PATH [PATH ...] [--lane REPO]
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import importlib.util
import json
import re
import subprocess
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
WINDOW = 12
KEYS = ("source", "recheck")
MISSING = "ENTRY-HEADER-MISSING"
REV = re.compile(r"[0-9a-fA-F]{4,64}\Z")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def git(repo, *args):
    proc = subprocess.run(
        ["git", "--no-pager", "-C", str(repo), *args],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=60)
    return proc


def repo_root(explicit):
    if explicit:
        root = Path(explicit).resolve()
        if not root.is_dir():
            raise Cannot("E-REPO", str(root), "--lane is not a directory")
        return root
    proc = git(Path.cwd(), "rev-parse", "--show-toplevel")
    if proc.returncode != 0:
        raise Cannot("E-REPO", str(Path.cwd()),
                     "cwd is not inside a git work tree; pass --lane")
    return Path(proc.stdout.decode("utf-8", "replace").strip())


def load_parser(repo):
    """Import the lane's own header grammar; never re-implement it here."""
    path = repo / "tools" / "check-knowledge-header.py"
    if not path.is_file():
        raise Cannot("E-REUSE", str(path),
                     "lane header gate absent; refusing to invent a second grammar")
    spec = importlib.util.spec_from_file_location("_r85_lane_header", path)
    if spec is None or spec.loader is None:
        raise Cannot("E-REUSE", str(path), "module spec could not be built")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except SystemExit as exc:  # the lane gate refuses an unresolved lane at import
        raise Cannot("E-REUSE", str(path), f"import refused: {exc}")
    except Exception as exc:  # noqa: BLE001 - any import failure is could-not-evaluate
        raise Cannot("E-REUSE", str(path), f"import failed: {exc}"[:160])
    parser = getattr(module, "header_lines", None)
    if not callable(parser):
        raise Cannot("E-REUSE", str(path), "header_lines parser not exported")
    return parser


def safe_path(text):
    path = text.strip()
    if not path or path.startswith("/") or ".." in Path(path).parts \
            or path.endswith("/"):
        raise Cannot("E-PATH-INVALID", text, "PATH must be a repo-relative file path")
    return path


def read_text(repo, revision, path):
    spec = f"{revision}:{path}"
    kind = git(repo, "cat-file", "-t", spec)
    if kind.returncode != 0:
        raise Cannot("E-PATH-UNREADABLE", path, "path absent at revision")
    if kind.stdout.decode("ascii", "replace").strip() != "blob":
        raise Cannot("E-PATH-UNREADABLE", path, "not a regular file at revision")
    proc = git(repo, "show", spec)
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()[:120]
        raise Cannot("E-PATH-UNREADABLE", path, detail or "git show failed")
    try:
        return proc.stdout.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Cannot("E-PATH-UNREADABLE", path, f"not UTF-8: {exc}"[:120])


def evaluate(parser, files):
    findings, notes = [], []
    for path, text in files:
        found = parser(text)  # lane grammar: column 0, outside fences, last operative
        lines, problems = {}, []
        for key in KEYS:
            hits = [(number, value) for number, value in found.get(key, [])
                    if number <= WINDOW]
            lines[key] = hits[-1][0] if hits else None
            if hits:  # MUTANT: presence test inverted
                detail = (f"{key}: line starts with {key}: within the first "
                          f"{WINDOW} lines (column 0, outside fenced blocks)")
                findings.append({"id": MISSING, "site": path, "detail": detail})
                problems.append(detail)
        notes.append({"path": path, "lines": lines, "problems": problems})
    return findings, notes


def emit(status, payload):
    payload = dict(payload)
    payload["status"] = status
    print(json.dumps(payload, sort_keys=True))
    return {"PASS": PASS, "FAIL": FAIL, "CANNOT_EVALUATE": CANNOT}[status]


def build_parser():
    parser = argparse.ArgumentParser(
        description="Read-only entry-header check (round 85, first-12-lines window).",
        exit_on_error=False)
    parser.add_argument("--revision", required=True, metavar="REV",
                        help="committed revision (4-64 hex) to read the blobs from")
    parser.add_argument("paths", nargs="+", metavar="PATH",
                        help="repo-relative file path(s) to check")
    parser.add_argument("--lane", default=None, metavar="REPO",
                        help="repository root (default: cwd's git top level)")
    return parser


def main(argv=None):
    try:
        args = build_parser().parse_intermixed_args(argv)
    except (argparse.ArgumentError, SystemExit) as exc:
        return emit("CANNOT_EVALUATE", {
            "scope": "none: malformed CLI",
            "findings": [{"id": "E-CLI", "site": "argv", "detail": str(exc)[:160]}]})

    revision = args.revision.strip()
    if not REV.fullmatch(revision):
        return emit("CANNOT_EVALUATE", {
            "revision": revision, "scope": "none: revision not a hex object id",
            "findings": [{"id": "E-REVISION-INVALID", "site": "revision",
                          "detail": "want 4-64 hex characters, got a symbolic or "
                                    "shortened name"}]})

    try:
        repo = repo_root(args.lane)
        proc = git(repo, "rev-parse", "--verify", "--quiet", revision + "^{commit}")
        if proc.returncode != 0:
            raise Cannot("E-REVISION-INVALID", revision, "not a commit in this repo")
        commit = proc.stdout.decode("ascii", "replace").strip()
        parser = load_parser(repo)
        paths = [safe_path(item) for item in args.paths]
        files = [(path, read_text(repo, commit, path)) for path in paths]
    except Cannot as exc:
        return emit("CANNOT_EVALUATE", {
            "revision": revision, "scope": "none: could-not-evaluate",
            "findings": [{"id": exc.fid, "site": exc.site, "detail": exc.detail}]})

    findings, notes = evaluate(parser, files)
    status = "FAIL" if findings else "PASS"
    return emit(status, {
        "revision": revision,
        "commit": commit,
        "lane": str(repo),
        "window": f"lines 1-{WINDOW} inclusive",
        "path_count": len(notes),
        "finding_count": len(findings),
        "clean_count": sum(1 for note in notes if not note["problems"]),
        "scope": ("named PATH list only; source:/recheck: at column 0 outside fenced "
                  "blocks within the first 12 physical lines; grammar reused from "
                  "tools/check-knowledge-header.py; read-only"),
        "findings": findings,
        "notes": notes,
    })


if __name__ == "__main__":
    sys.exit(main())
