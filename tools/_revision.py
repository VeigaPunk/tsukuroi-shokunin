#!/usr/bin/env python3
"""Shared landed-revision binding for every tsukuroi `--revision` tool (QUALITY 27, round 18).

Round 17 bound nine tools to landed commits by copying the check into each one; wave-2
FxSimplifyBind found six same-input divergences between the copies (branch validation,
check precedence, merge-base rc>=2, double findings, missing branch, branch strings such
as `a..b` or `master/`).  This module is the single implementation those tools import.
The judge, `tools/check-revision-binding.py`, keeps its own independent copy on purpose:
it grades the tools and must not share the code it grades.

Contract — checks run in this order, the first failure wins, and a failure is exactly one
`RevisionError` (one finding id, exit class 2 = could-not-evaluate):

 1. branch   matches `[A-Za-z0-9_][A-Za-z0-9._/-]*`, is not `HEAD`, and passes
             `git check-ref-format refs/heads/<branch>`          else E-BRANCH-INVALID
 2. revision is 7-64 hex (`HEAD`, `@`, `@-`, ref names, ranges)   else E-REVISION-INVALID
 3. `<revision>^{commit}` resolves to exactly one commit           else E-REVISION-INVALID
 4. `refs/heads/<branch>` resolves to a commit                     else E-BRANCH-MISSING
 5. the commit is an ancestor of `refs/heads/<branch>`             else E-REVISION-NOT-LANDED
 6. when `refs/remotes/origin/<branch>` exists, the commit is an
    ancestor of it                                                 else E-REVISION-NOT-PUSHED

Any git failure — `merge-base --is-ancestor` exiting >= 2 (for example an origin ref that
names a non-commit), a timeout, or git missing — is E-GIT-FAILED, never "not an ancestor".

The module only reads (`check-ref-format`, `rev-parse`, `merge-base`); it never writes a
ref, the index or the worktree.  `python3 tools/_revision.py --selftest` runs a hermetic
suite over one mktemp repository and prints `REVISION_SELFTEST: PASS (<n> cases ...)`.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from collections import namedtuple
from pathlib import Path

EXIT = 2
REV = re.compile(r"^[0-9a-fA-F]{7,64}$")
BRANCH = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9._/-]*$")
E_BRANCH_INVALID = "E-BRANCH-INVALID"
E_INVALID = "E-REVISION-INVALID"
E_BRANCH_MISSING = "E-BRANCH-MISSING"
E_NOT_LANDED = "E-REVISION-NOT-LANDED"
E_NOT_PUSHED = "E-REVISION-NOT-PUSHED"
E_GIT = "E-GIT-FAILED"
IDS = (E_BRANCH_INVALID, E_INVALID, E_BRANCH_MISSING, E_NOT_LANDED, E_NOT_PUSHED, E_GIT)

Binding = namedtuple("Binding", "sha branch branch_tip origin_tip")


class RevisionError(Exception):
    """One binding failure: `fid` is the finding id, `site` where, `detail` why."""

    def __init__(self, fid, site, detail):
        super().__init__(f"{fid} {site}: {detail}")
        self.fid, self.site, self.detail = fid, site, detail


def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C"})
    return env


def _git(repo, *args, timeout=60):
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(repo), *args],
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=clean_env(), timeout=timeout)
    except subprocess.TimeoutExpired:
        raise RevisionError(E_GIT, "git", f"git {args[0]} exceeded {timeout}s")
    except OSError as exc:
        raise RevisionError(E_GIT, "git", str(exc)[:120])


def _err(proc):
    return proc.stderr.decode("utf-8", "replace").strip()[:120] or f"exit={proc.returncode}"


def validate_branch(branch):
    """Raise E-BRANCH-INVALID unless `branch` is a plain, well-formed local branch name."""
    if not isinstance(branch, str) or not BRANCH.fullmatch(branch) or branch == "HEAD":
        raise RevisionError(E_BRANCH_INVALID, "branch", f"invalid branch name {branch!r}"[:120])
    try:
        proc = subprocess.run(["git", "check-ref-format", f"refs/heads/{branch}"],
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=clean_env(), timeout=30)
    except (subprocess.TimeoutExpired, OSError) as exc:
        raise RevisionError(E_GIT, "git", f"check-ref-format failed: {exc}"[:120])
    if proc.returncode != 0:
        raise RevisionError(E_BRANCH_INVALID, "branch", f"git check-ref-format rejects {branch!r}"[:120])


def _commit(repo, ref):
    """Commit sha of `ref`; None when it does not resolve (rc 1); E-GIT-FAILED on a git fatal."""
    proc = _git(repo, "rev-parse", "--verify", "--quiet", "--end-of-options", f"{ref}^{{commit}}")
    if proc.returncode == 0:
        return proc.stdout.decode("ascii", "replace").strip()
    if proc.returncode == 1:
        return None
    raise RevisionError(E_GIT, ref, f"rev-parse exited {proc.returncode}: {_err(proc)}")


def _exists(repo, ref):
    proc = _git(repo, "rev-parse", "--verify", "--quiet", "--end-of-options", ref)
    if proc.returncode in (0, 1):
        return proc.returncode == 0
    raise RevisionError(E_GIT, ref, f"rev-parse exited {proc.returncode}: {_err(proc)}")


def _ancestor(repo, sha, ref):
    proc = _git(repo, "merge-base", "--is-ancestor", sha, ref)
    if proc.returncode in (0, 1):
        return proc.returncode == 0
    raise RevisionError(E_GIT, ref, f"merge-base --is-ancestor exited {proc.returncode}: {_err(proc)}")


def branch_tip(repo, branch="master"):
    """Informational branch tip; never raises (None when absent or unreadable)."""
    try:
        validate_branch(branch)
        return _commit(repo, f"refs/heads/{branch}")
    except RevisionError:
        return None


def bind(repo, revision, branch="master"):
    """Bind `revision` to a landed (and, with an origin ref, pushed) commit on `branch`."""
    validate_branch(branch)
    if not isinstance(revision, str) or not REV.fullmatch(revision):
        raise RevisionError(E_INVALID, "revision", "7-64 hex commit required")
    sha = _commit(repo, revision)
    if sha is None:
        raise RevisionError(E_INVALID, "revision", f"{revision} does not name one commit")
    local = f"refs/heads/{branch}"
    tip = _commit(repo, local)
    if tip is None:
        raise RevisionError(E_BRANCH_MISSING, local, "branch ref absent")
    if not _ancestor(repo, sha, local):
        raise RevisionError(E_NOT_LANDED, local, f"{sha[:12]} is not an ancestor")
    remote = f"refs/remotes/origin/{branch}"
    origin = None
    if _exists(repo, remote):
        if not _ancestor(repo, sha, remote):
            raise RevisionError(E_NOT_PUSHED, remote, f"{sha[:12]} is not an ancestor")
        origin = _commit(repo, remote)
    return Binding(sha, branch, tip, origin)


def selftest():
    passed, failures = 0, []

    def expect(name, call, want):
        nonlocal passed
        try:
            got = call()
            got = ("ok", got) if want[0] == "ok" else ("ok", None)
        except RevisionError as exc:
            got = ("err", exc.fid)
        if got == want:
            passed += 1
        else:
            failures.append(f"{name}: got={got!r} want={want!r}")

    def run(repo, *args):
        proc = subprocess.run(["git", "-C", str(repo), "-c", "user.name=rev", "-c",
                               "user.email=rev@invalid", "-c", "commit.gpgsign=false", *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=clean_env())
        if proc.returncode != 0:
            raise RuntimeError(f"git {args}: {_err(proc)}")
        return proc.stdout.decode().strip()

    with tempfile.TemporaryDirectory(prefix="tsukuroi-revision-st-") as tmp:
        repo = Path(tmp) / "r"
        subprocess.run(["git", "init", "--quiet", str(repo)], check=True, env=clean_env())
        run(repo, "symbolic-ref", "HEAD", "refs/heads/master")
        run(repo, "commit", "--quiet", "--allow-empty", "-m", "base")
        base = run(repo, "rev-parse", "HEAD")
        run(repo, "commit", "--quiet", "--allow-empty", "-m", "tip")
        tip = run(repo, "rev-parse", "HEAD")
        run(repo, "checkout", "--quiet", "--detach", tip)
        run(repo, "commit", "--quiet", "--allow-empty", "-m", "unlanded")
        unlanded = run(repo, "rev-parse", "HEAD")
        ok = lambda sha: ("ok", sha)  # noqa: E731
        err = lambda fid: ("err", fid)  # noqa: E731

        # no origin ref: landed commits bind, every refusal is a single typed id
        expect("tip", lambda: bind(repo, tip).sha, ok(tip))
        expect("short-tip", lambda: bind(repo, tip[:8]).sha, ok(tip))
        expect("landed-parent", lambda: bind(repo, base).sha, ok(base))
        expect("upper-hex", lambda: bind(repo, tip.upper()).sha, ok(tip))
        expect("tip-fields", lambda: tuple(bind(repo, tip)[1:]), ok(("master", tip, None)))
        for label, rev in (("head", "HEAD"), ("at", "@"), ("at-parent", "@-"),
                           ("branch-name", "master"), ("ref", "refs/heads/master"),
                           ("six-hex", tip[:6]), ("range", f"{base[:8]}..{tip[:8]}"),
                           ("trailing-slash", f"{tip[:8]}/"), ("empty", ""),
                           ("sixty-five", "a" * 65), ("unknown", "0" * 40)):
            expect(f"rev-{label}", lambda rev=rev: bind(repo, rev), err(E_INVALID))
        expect("unlanded", lambda: bind(repo, unlanded), err(E_NOT_LANDED))
        for label, br in (("range", "a..b"), ("slash", "master/"), ("space", "bad branch"),
                          ("dash", "-x"), ("at", "@"), ("head", "HEAD"), ("empty", ""),
                          ("lock", "x.lock"), ("dot", ".hidden")):
            expect(f"branch-{label}", lambda br=br: bind(repo, tip, br), err(E_BRANCH_INVALID))
        # precedence: branch before revision, revision syntax before branch existence
        expect("precedence-branch-first", lambda: bind(repo, "HEAD", "a..b"), err(E_BRANCH_INVALID))
        expect("precedence-rev-before-missing", lambda: bind(repo, "HEAD", "nosuch"), err(E_INVALID))
        expect("branch-missing", lambda: bind(repo, tip, "nosuch"), err(E_BRANCH_MISSING))
        expect("branch-nested-missing", lambda: bind(repo, tip, "feature/x"), err(E_BRANCH_MISSING))
        expect("branch-tip-info", lambda: branch_tip(repo, "master") == tip
               and branch_tip(repo, "nosuch") is None and branch_tip(repo, "a..b") is None, ok(True))

        # origin ref present: pushed binds, lagging origin refuses with exactly one id
        run(repo, "update-ref", "refs/remotes/origin/master", base)
        expect("not-pushed", lambda: bind(repo, tip), err(E_NOT_PUSHED))
        expect("pushed-parent", lambda: bind(repo, base).sha, ok(base))
        expect("unlanded-single-id", lambda: bind(repo, unlanded), err(E_NOT_LANDED))
        run(repo, "update-ref", "refs/remotes/origin/master", tip)
        expect("pushed-tip", lambda: bind(repo, tip).origin_tip, ok(tip))

        # merge-base rc>=2 is a git failure, never "not an ancestor"
        blob = subprocess.run(["git", "-C", str(repo), "hash-object", "-w", "--stdin"],
                              input=b"blob\n", stdout=subprocess.PIPE, env=clean_env(),
                              check=True).stdout.decode().strip()
        run(repo, "update-ref", "refs/remotes/origin/master", blob)
        expect("git-failed-origin-blob", lambda: bind(repo, tip), err(E_GIT))
        run(repo, "update-ref", "refs/remotes/origin/master", tip)
        expect("not-a-repo", lambda: bind(Path(tmp) / "absent", tip), err(E_GIT))

    total = passed + len(failures)
    status = "PASS" if not failures else "FAIL"
    print(f"REVISION_SELFTEST: {status} ({total} cases, {passed} passed, {len(failures)} failed)")
    for line in failures:
        print(f"  {line}", file=sys.stderr)
    return 0 if not failures else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(selftest())
    print("usage: python3 tools/_revision.py --selftest  (import bind() from the tools)",
          file=sys.stderr)
    sys.exit(64)
