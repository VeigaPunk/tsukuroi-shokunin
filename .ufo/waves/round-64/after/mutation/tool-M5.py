#!/usr/bin/env python3
"""Line-endings guard (round 64; the CRLF-in-canonical-sources class).

The class: a Windows-era work commit (`2913b75d`) landed CRLF line endings in the
lane's three canonical source files (`corpus/SOURCES.md`, `SKILL.md`,
`SCORECARD.md`). Nothing objected, because the round census parsed the files the way
a tolerant reader does; the damage only surfaced when the census started reporting
every visible row as "outside Registry section" - an E12 storm caused by nothing but
a trailing 0x0D on each line.

This guard makes the byte-level invariant mechanical: a tracked text file in the
guarded set must contain no 0x0D byte at all. It does not care whether the CR sits
before a newline, at EOF without a newline, or mid-line - all three are violations,
each one named by path and first offending line.

Guarded set (from `git ls-files`, repo root = --root or cwd):
  - the canonical top-level documents SKILL.md, LOG.md, SCORECARD.md, PROVINCE.md,
    SHONEN.md, MINT.md, AGENTS.md
  - everything under corpus/
  - the top-level tools/*.py checkers
  - everything under plans/

Allow-list: any path with a `.ufo` component is skipped and NEVER flagged. The
`.ufo/waves/` tree stores upstream-fetched HTTP headers, git patches and raw tool
output verbatim; those legitimately carry CRLF and rewriting them would falsify the
capture. A path is allow-listed when `.ufo` appears as any component of its
repo-relative form, so an explicit `--check .ufo/...` argument is skipped too.

Exit codes: 0 clean, 1 violations found, 2 usage or IO error (including git failing to
list the tree - "cannot evaluate" is never reported as "clean").

Read-only by construction: the tool reads bytes and runs `git ls-files`. Its only write
is `--selftest`'s fixture tree, which is created under --work, else $HYAKU_SCRATCH, else
$TMPDIR, and removed in a finally block. /tmp is never hardcoded (a /tmp path is not
citable evidence in this lane); the last-resort default is the operator's scratch
convention /fast/scratch/hyaku.

Usage:
  python3 tools/check-line-endings-r64.py --check [paths...] [--root R] [--work D]
  python3 tools/check-line-endings-r64.py --selftest [--work D]
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

PASS, FAIL, CANNOT = 0, 1, 2

CANONICAL = (
    "SKILL.md",
    "LOG.md",
    "SCORECARD.md",
    "PROVINCE.md",
    "SHONEN.md",
    "MINT.md",
    "AGENTS.md",
)
GUARDED_DIRS = ("corpus/", "plans/")
TOOLS_PY_PREFIX = "tools/"
ALLOW_DIR = ".ufo"

DEFAULT_SELFTEST_BASE = "/fast/scratch/hyaku"
CR = b"\r"
LF = b"\n"


# --------------------------------------------------------------------------- paths

def is_guarded(relpath):
    """True when the repo-relative path belongs to the guarded set."""
    p = relpath.replace(os.sep, "/")
    if p in CANONICAL:
        return True
    if any(p.startswith(prefix) for prefix in GUARDED_DIRS):
        return True
    # M5 guard-set-shrink: tools/*.py is no longer guarded
    return False


def is_allowlisted(relpath):
    """True when the path sits under a TOP-LEVEL `.ufo/` directory.

    Anchored to the leading component on purpose: a nested `.ufo` directory further down
    (`corpus/.ufo/…`) does NOT buy the allowlist, because the guarded tree is exactly
    where a stray capture must not hide. See the symlink case in the round-64 review:
    the allowlist is name-based on the tracked path, so a guarded path can never inherit
    a target's `.ufo` shield.
    """
    parts = relpath.replace(os.sep, "/").split("/")
    return bool(parts) and parts[0] == ALLOW_DIR


def repo_relative(path, root):
    """Best-effort repo-relative form of `path`; absolute fallback outside the root."""
    abspath = os.path.abspath(path)
    rootabs = os.path.abspath(root)
    try:
        common = os.path.commonpath([abspath, rootabs])
    except ValueError:  # different drives / mixed absolute-relative - never on POSIX
        return abspath.replace(os.sep, "/")
    if common == rootabs:
        rel = os.path.relpath(abspath, rootabs)
        return rel.replace(os.sep, "/")
    return abspath.replace(os.sep, "/")


def git_env():
    env = dict(os.environ)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_PAGER"] = "cat"
    env.setdefault("LC_ALL", "C")
    return env


def tracked_files(root):
    """All paths tracked by git at `root`, repo-relative, in git's order."""
    try:
        out = subprocess.run(
            ["git", "-C", root, "ls-files", "-z"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=git_env(),
            check=False,
        )
    except OSError as exc:
        raise RuntimeError("cannot run git: %s" % exc)
    if out.returncode != 0:
        raise RuntimeError(
            "git ls-files failed (rc=%d): %s"
            % (out.returncode, out.stderr.decode("utf-8", "replace").strip())
        )
    return [os.fsdecode(blob) for blob in out.stdout.split(b"\0") if blob]


# --------------------------------------------------------------------------- check

def first_cr(path):
    """Return (line_number, byte_offset) of the first 0x0D, or None when CR-free."""
    line = 1
    offset = 0
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                return None
            idx = chunk.find(CR)
            if idx != -1:
                return line + chunk.count(LF, 0, idx), offset + idx
            line += chunk.count(LF)
            offset += len(chunk)


def check_paths(paths, root):
    """Check paths (relative ones resolve against root).

    Returns (violations, checked, skipped); violations are
    (repo-relative path, 1-based line, byte offset) tuples. A path that cannot be read
    raises - "cannot evaluate" is never folded into "clean".
    """
    violations = []
    checked = 0
    skipped = 0
    for raw in paths:
        path = raw if os.path.isabs(raw) else os.path.join(root, raw)
        rel = repo_relative(path, root)
        if is_allowlisted(rel):
            skipped += 1
            continue
        if os.path.isdir(path):
            raise ValueError("not a file: %s" % rel)
        if not os.path.exists(path):
            raise ValueError("no such file: %s" % rel)
        checked += 1
        hit = first_cr(path)
        if hit is not None:
            violations.append((rel, hit[0], hit[1]))
    return violations, checked, skipped


def guarded_set(root):
    """(guarded paths, allow-listed-tracked count) for the tracked tree at `root`.

    The count is returned rather than dropped so default mode can disclose how much of
    the tree the allowlist set aside; a zero in that field means "nothing was hidden",
    not "nothing was looked at".
    """
    out = []
    allowlisted = 0
    for rel in tracked_files(root):
        if is_allowlisted(rel):
            allowlisted += 1
            continue
        if not is_guarded(rel):
            continue
        out.append(os.path.join(root, rel))
    return out, allowlisted


def report(violations, checked, skipped, default_set_skipped=0):
    if violations:
        print("check-line-endings-r64: %d violation(s)" % len(violations))
        for rel, line, offset in violations:
            print("  %s:%d: CR byte at offset %d" % (rel, line, offset))
    extra = ", %d allow-listed" % skipped if skipped else ""
    verdict = "FAIL" if violations else "PASS"
    print(
        "CHECK_LINE_ENDINGS: %s (%d file(s) checked, %d violation(s)%s)"
        % (verdict, checked, len(violations), extra)
    )
    if default_set_skipped:
        # Disclosure, not a verdict input: the default set is built from `git ls-files`,
        # and .ufo/** captures are excluded by design. Silence here would read as
        # "nothing was set aside", so the count is always printed in default mode.
        print(
            "check-line-endings-r64: %d allow-listed .ufo path(s) skipped (upstream captures)"
            % default_set_skipped
        )
    return FAIL if violations else PASS


# --------------------------------------------------------------------------- selftest

def selftest_base(work):
    """Scratch base for fixtures: --work, then $HYAKU_SCRATCH, then $TMPDIR, then default.

    The default is the operator's scratch convention; /tmp is never assumed, because a
    /tmp path is never citable evidence in this lane.
    """
    base = (
        work
        or os.environ.get("HYAKU_SCRATCH")
        or os.environ.get("TMPDIR")
        or DEFAULT_SELFTEST_BASE
    )
    os.makedirs(base, exist_ok=True)
    return base


def run_selftest(work):
    """Five named fixture cases; every fixture is a plain file tree (no git needed)."""
    base = selftest_base(work)
    fixture_root = tempfile.mkdtemp(prefix="line-endings-selftest-", dir=base)
    cases = []
    try:
        def fixture(name, payload):
            path = os.path.join(fixture_root, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as handle:
                handle.write(payload)
            return path

        # (1) lf-file-passes
        lf = fixture("guarded/lf.md", b"alpha\nbeta\ngamma\n")
        v, checked, skipped = check_paths([lf], fixture_root)
        cases.append(("lf-file-passes", not v and checked == 1))

        # (2) crlf-file-fails-naming-path
        crlf = fixture("guarded/crlf.md", b"alpha\r\nbeta\r\n")
        v, checked, _ = check_paths([crlf], fixture_root)
        named = [row for row in v if row[0].endswith("guarded/crlf.md")]
        cases.append(
            ("crlf-file-fails-naming-path", bool(v) and bool(named) and named[0][1] == 1)
        )

        # (3) allowlisted-ufo-path-ignored
        ufo = fixture(".ufo/waves/capture.headers", b"HTTP/1.1 200 OK\r\nServer: x\r\n")
        v, checked, skipped = check_paths([ufo], fixture_root)
        cases.append(
            ("allowlisted-ufo-path-ignored", not v and checked == 0 and skipped == 1)
        )

        # (4) cr-at-eof-without-newline-flagged
        eof = fixture("guarded/eof.md", b"alpha\nbeta\r")
        v, _, _ = check_paths([eof], fixture_root)
        cases.append(
            (
                "cr-at-eof-without-newline-flagged",
                len(v) == 1 and v[0][1] == 2,
            )
        )

        # (5) cr-midline-flagged
        midline = fixture("guarded/midline.md", b"alpha\rbeta\ngamma\n")
        v, _, _ = check_paths([midline], fixture_root)
        cases.append(("cr-midline-flagged", len(v) == 1 and v[0][1] == 1))
    finally:
        shutil.rmtree(fixture_root, ignore_errors=True)

    print("check-line-endings-r64 selftest (fixtures under %s)" % base)
    passed = 0
    for name, ok in cases:
        print("  %-36s %s" % (name, "PASS" if ok else "FAIL"))
        passed += 1 if ok else 0
    failed = len(cases) - passed
    if failed == 0:
        print(
            "CHECK_LINE_ENDINGS_SELFTEST: PASS (%d cases, %d passed, %d failed)"
            % (len(cases), passed, failed)
        )
        return PASS
    print("CHECK_LINE_ENDINGS_SELFTEST: FAIL (%d cases, %d passed, %d failed)"
          % (len(cases), passed, failed))
    return FAIL


# --------------------------------------------------------------------------- main

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Fail when a guarded tracked file carries a 0x0D byte."
    )
    parser.add_argument("--check", action="store_true", help="run the check")
    parser.add_argument("paths", nargs="*", help="explicit paths (default: guarded set)")
    parser.add_argument("--root", default=None, help="repo root (default: cwd)")
    parser.add_argument("--work", default=None, help="scratch base for --selftest")
    parser.add_argument("--selftest", action="store_true", help="run the fixture suite")
    args = parser.parse_args(argv)

    if args.selftest:
        return run_selftest(args.work)
    if not args.check:
        parser.error("one of --check or --selftest is required")

    root = os.path.abspath(args.root or os.getcwd())
    if not os.path.isdir(root):
        print("check-line-endings-r64: no such directory: %s" % root, file=sys.stderr)
        return CANNOT

    try:
        pre_skipped = 0
        if args.paths:
            targets = args.paths
        else:
            targets, pre_skipped = guarded_set(root)
        violations, checked, skipped = check_paths(targets, root)
    except (OSError, RuntimeError, ValueError) as exc:
        print("check-line-endings-r64: %s" % exc, file=sys.stderr)
        return CANNOT
    return report(violations, checked, skipped, pre_skipped)


if __name__ == "__main__":
    sys.exit(main())
