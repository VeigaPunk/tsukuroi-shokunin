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
 3. revision uniquely matches an object ID, then peels to a commit else E-REVISION-INVALID
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

import hashlib
import os
import re
import subprocess
import sys
import tempfile
from collections import namedtuple
from pathlib import Path

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
    if any(location == root or location.startswith(root + os.sep)
           for location in (os.getcwd(), os.path.abspath(__file__), tempfile.gettempdir())
           for root in ("/fast/scratch", "/tmp")):
        env = {"PATH": "/usr/bin:/bin", "LC_ALL": "C"}
    else:
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C",
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
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
    """Commit sha or None for an unresolved/non-commit object in a readable repository."""
    proc = _git(repo, "rev-parse", "--verify", "--quiet", "--end-of-options", f"{ref}^{{commit}}")
    if proc.returncode == 0:
        return proc.stdout.decode("ascii", "replace").strip()
    # A malformed/ambiguous/non-commit selector can produce a fatal rev-parse
    # status too. Distinguish it from an unavailable repository without parsing
    # localized stderr; bind() consistently classifies it as INVALID.
    repo_check = _git(repo, "rev-parse", "--git-dir")
    if repo_check.returncode == 0:
        return None
    raise RevisionError(E_GIT, ref, f"repository unavailable: {_err(repo_check)}")


def _object_commit(repo, revision):
    """Resolve object IDs before refs; only a uniquely selected tag may be peeled.

    Enumerate before checking type: filtering ambiguous prefixes to commits would
    silently accept one commit alongside a colliding blob. Return commits by
    their already-confirmed object ID, never by reparsing that full hex as a ref.
    """
    proc = _git(repo, "rev-parse", f"--disambiguate={revision.lower()}")
    if proc.returncode:
        raise RevisionError(E_GIT, "revision", f"object lookup failed: {_err(proc)}")
    objects = proc.stdout.decode("ascii", "replace").splitlines()
    if len(objects) != 1:
        return None

    oid = objects[0]
    kind_proc = _git(repo, "cat-file", "-t", oid)
    if kind_proc.returncode:
        repo_check = _git(repo, "rev-parse", "--git-dir")
        if repo_check.returncode == 0:
            return None
        raise RevisionError(E_GIT, oid, f"repository unavailable: {_err(repo_check)}")
    object_kind = kind_proc.stdout.decode("ascii", "replace").strip()
    if object_kind == "commit":
        return oid
    if object_kind != "tag":
        return None

    peel = _git(repo, "rev-parse", "--verify", "--quiet", "--end-of-options",
                 f"{oid}^{{commit}}")
    if peel.returncode == 0:
        return peel.stdout.decode("ascii", "replace").strip()
    repo_check = _git(repo, "rev-parse", "--git-dir")
    if repo_check.returncode == 0:
        return None
    raise RevisionError(E_GIT, oid, f"repository unavailable: {_err(repo_check)}")


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
    sha = _object_commit(repo, revision)
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

        # Hex-looking references are not revision aliases. Real object prefixes
        # still win over colliding branch/tag names, and annotated tag objects
        # retain their commit-ish peeling behavior.
        all_objects = run(repo, "cat-file", "--batch-all-objects",
                          "--batch-check=%(objectname)").splitlines()
        ghost = next(char * 12 for char in "0123456789abcdef"
                     if all(not oid.startswith(char * 12) for oid in all_objects))
        run(repo, "branch", ghost, tip)
        expect("ghost-hex-branch", lambda: bind(repo, ghost), err(E_INVALID))
        run(repo, "branch", "-D", ghost)
        run(repo, "tag", ghost, tip)
        expect("ghost-hex-tag", lambda: bind(repo, ghost), err(E_INVALID))
        run(repo, "tag", "-d", ghost)
        ghost_full = next(char * 40 for char in "0123456789abcdef"
                          if all(oid != char * 40 for oid in all_objects)
                          and not _exists(repo, f"refs/heads/{char * 40}")
                          and not _exists(repo, f"refs/tags/{char * 40}"))
        run(repo, "branch", ghost_full, tip)
        expect("ghost-full-hex-branch",
               lambda: bind(repo, ghost_full), err(E_INVALID))
        run(repo, "branch", "-D", ghost_full)
        run(repo, "tag", ghost_full, tip)
        expect("ghost-full-hex-lightweight-tag",
               lambda: bind(repo, ghost_full), err(E_INVALID))
        run(repo, "tag", "-d", ghost_full)
        all_objects = run(repo, "cat-file", "--batch-all-objects",
                          "--batch-check=%(objectname)").splitlines()
        annotated_ghost = None
        for char in "0123456789abcdef":
            candidate = char * 40
            if any(oid == candidate for oid in all_objects):
                continue
            if _exists(repo, f"refs/tags/{candidate}"):
                continue
            run(repo, "tag", "-a", candidate, "-m", "ghost annotated tag", tip)
            updated_objects = run(repo, "cat-file", "--batch-all-objects",
                                  "--batch-check=%(objectname)").splitlines()
            if any(oid == candidate for oid in updated_objects):
                run(repo, "tag", "-d", candidate)
                all_objects = updated_objects
                continue
            annotated_ghost = candidate
            all_objects = updated_objects
            break
        if annotated_ghost is None:
            raise RuntimeError("could not construct a 40-hex annotated ghost tag")
        expect("ghost-full-hex-annotated-tag",
               lambda: bind(repo, annotated_ghost), err(E_INVALID))
        run(repo, "tag", "-d", annotated_ghost)
        shadow = next(tip[:width] for width in range(7, len(tip) + 1)
                      if sum(candidate.startswith(tip[:width]) for candidate in all_objects) == 1
                      and not _exists(repo, f"refs/heads/{tip[:width]}")
                      and not _exists(repo, f"refs/tags/{tip[:width]}"))
        run(repo, "branch", shadow, base)
        run(repo, "tag", shadow, base)
        try:
            expect("real-prefix-shadowed-by-branch-and-tag",
                   lambda: bind(repo, shadow).sha, ok(tip))
        finally:
            run(repo, "branch", "-D", shadow)
            run(repo, "tag", "-d", shadow)

        unlanded_prefix = next(
            (unlanded[:width] for width in range(7, len(unlanded) + 1)
             if sum(candidate.startswith(unlanded[:width]) for candidate in all_objects) == 1
             and not _exists(repo, f"refs/heads/{unlanded[:width]}")
             and not _exists(repo, f"refs/tags/{unlanded[:width]}")), None)
        if unlanded_prefix is None:
            raise RuntimeError("could not construct a unique unlanded object prefix")
        run(repo, "branch", unlanded_prefix, tip)
        run(repo, "tag", unlanded_prefix, tip)
        try:
            expect("unlanded-prefix-shadowed-by-branch-and-tag",
                   lambda: bind(repo, unlanded_prefix), err(E_NOT_LANDED))
        finally:
            run(repo, "branch", "-D", unlanded_prefix)
            run(repo, "tag", "-d", unlanded_prefix)

        run(repo, "update-ref", "refs/remotes/origin/master", base)
        run(repo, "branch", shadow, base)
        run(repo, "tag", shadow, base)
        try:
            expect("unpushed-prefix-shadowed-by-branch-and-tag",
                   lambda: bind(repo, shadow), err(E_NOT_PUSHED))
        finally:
            run(repo, "branch", "-D", shadow)
            run(repo, "tag", "-d", shadow)
            run(repo, "update-ref", "refs/remotes/origin/master", tip)
        run(repo, "tag", "-a", "peel-object", "-m", "peel", tip)
        tag_oid = run(repo, "rev-parse", "refs/tags/peel-object^{tag}")
        all_objects = run(repo, "cat-file", "--batch-all-objects",
                          "--batch-check=%(objectname)").splitlines()
        tag_prefix = next(tag_oid[:width] for width in range(7, len(tag_oid) + 1)
                          if sum(candidate.startswith(tag_oid[:width])
                                 for candidate in all_objects) == 1)
        expect("annotated-tag-full-object-id", lambda: bind(repo, tag_oid).sha, ok(tip))
        expect("annotated-tag-object-prefix", lambda: bind(repo, tag_prefix).sha, ok(tip))
        run(repo, "tag", "-a", "peel-nested", "-m", "nested peel", tag_oid)
        nested_tag_oid = run(repo, "rev-parse", "refs/tags/peel-nested^{tag}")
        expect("nested-annotated-tag-object",
               lambda: bind(repo, nested_tag_oid).sha, ok(tip))
        run(repo, "tag", "-d", "peel-nested")
        run(repo, "tag", "-d", "peel-object")
        for object_id, label in ((tip, "commit"), (tag_oid, "tag")):
            branch_ref, tag_ref = f"refs/heads/{object_id}", f"refs/tags/{object_id}"
            run(repo, "update-ref", branch_ref, base)
            run(repo, "update-ref", tag_ref, base)
            try:
                expect(f"full-{label}-object-id-ref-shadow",
                       lambda object_id=object_id: bind(repo, object_id).sha, ok(tip))
            finally:
                run(repo, "update-ref", "-d", branch_ref)
                run(repo, "update-ref", "-d", tag_ref)
        ambiguous_prefix = tag_oid[:4]
        if (run(repo, "cat-file", "-t", tag_oid) != "tag"
                or sum(candidate.startswith(ambiguous_prefix)
                       for candidate in all_objects) != 1):
            failures.append("ambiguous-object-prefix: no unique four-hex annotated-tag seed")
        else:
            for index in range(1_000_000):
                blob_data = f"ambiguous-prefix-{ambiguous_prefix}-{index}".encode()
                blob_oid = hashlib.sha1(
                    b"blob " + str(len(blob_data)).encode() + b"\0" + blob_data).hexdigest()
                if blob_oid.startswith(ambiguous_prefix):
                    break
            else:
                raise RuntimeError("could not construct a four-hex object collision")
            written = subprocess.run(
                ["git", "-C", str(repo), "hash-object", "-w", "--stdin"],
                input=blob_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=clean_env())
            if written.returncode or written.stdout.decode().strip() != blob_oid:
                raise RuntimeError("could not store synthetic ambiguous-prefix blob")
            expect("ambiguous-object-prefix", lambda: _object_commit(repo, ambiguous_prefix),
                   ok(None))

        expect("full-object-id", lambda: bind(repo, tip).sha, ok(tip))

        # merge-base rc>=2 is a git failure, never "not an ancestor"

        blob = subprocess.run(["git", "-C", str(repo), "hash-object", "-w", "--stdin"],
                              input=b"blob\n", stdout=subprocess.PIPE, env=clean_env(),
                              check=True).stdout.decode().strip()
        tree_input = f"100644 blob {blob}\tfixture.txt\n".encode("ascii")
        tree = subprocess.run(["git", "-C", str(repo), "mktree"], input=tree_input,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=clean_env(), check=True).stdout.decode().strip()
        expect("blob-revision-invalid", lambda: bind(repo, blob), err(E_INVALID))
        expect("tree-revision-invalid", lambda: bind(repo, tree), err(E_INVALID))
        for target, label in ((blob, "blob"), (tree, "tree")):
            tag_name = "revision-peel-" + label
            run(repo, "tag", "-a", tag_name, "-m", "tagged " + label, target)
            tag_object = run(repo, "rev-parse", "refs/tags/" + tag_name + "^{tag}")
            expect("annotated-tag-to-" + label + "-invalid",
                   lambda tag_object=tag_object: bind(repo, tag_object), err(E_INVALID))
            run(repo, "tag", "-d", tag_name)
        run(repo, "update-ref", "refs/remotes/origin/master", blob)
        expect("git-failed-origin-blob", lambda: bind(repo, tip), err(E_GIT))
        run(repo, "update-ref", "refs/remotes/origin/master", tip)
        expect("not-a-repo", lambda: bind(Path(tmp) / "absent", tip), err(E_GIT))
        expect("git-config-isolated", lambda: clean_env()["GIT_CONFIG_NOSYSTEM"] == "1"
               and clean_env()["GIT_CONFIG_GLOBAL"] == os.devnull, ok(True))

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
