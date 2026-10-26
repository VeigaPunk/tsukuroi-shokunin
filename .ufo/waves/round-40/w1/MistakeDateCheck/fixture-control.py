#!/usr/bin/env python3
"""Fixture control for check_heading_dates.py (scratch only; not lane evidence).

Builds throwaway git repos under the scratch dir with controlled commit times and
shows the checker both passes a consistent fixture and fails a violating one.
"""
import os
import shutil
import subprocess
import sys
import tempfile

CHECKER = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-40/w1/MistakeDateCheck/check_heading_dates.py"
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r40/MistakeDateCheck"
ENV = dict(
    os.environ,
    GIT_AUTHOR_NAME="fixture",
    GIT_AUTHOR_EMAIL="fixture@shokunin.local",
    GIT_COMMITTER_NAME="fixture",
    GIT_COMMITTER_EMAIL="fixture@shokunin.local",
    GIT_OPTIONAL_LOCKS="0",
)


def run(cmd, cwd=None, env=None):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env or ENV)
    return proc


def commit(repo, when, message):
    env = dict(ENV, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
    proc = run(["git", "-C", repo, "commit", "-q", "-m", message], env=env)
    if proc.returncode != 0:
        raise SystemExit("commit failed: %s" % proc.stderr)


def new_repo():
    repo = tempfile.mkdtemp(prefix="fx.", dir=SCRATCH)
    run(["git", "-C", repo, "init", "-q"])
    top = run(["git", "-C", repo, "rev-parse", "--show-toplevel"]).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise SystemExit("toplevel mismatch: %r != %r" % (top, repo))
    return repo


def write(repo, name, text):
    with open(os.path.join(repo, name), "w", encoding="utf-8") as handle:
        handle.write(text)


def check(repo, *extra):
    proc = run([sys.executable, CHECKER, "--repo", repo, "--rev", "HEAD", *extra])
    return proc


def line(tag, proc):
    out = proc.stdout.strip().splitlines()
    print("[%s] exit=%d %s" % (tag, proc.returncode, out[-1] if out else "(no stdout)"))
    for row in out[:-1]:
        print("    " + row.replace("\n", "\n    "))
    for err in proc.stderr.strip().splitlines():
        print("    stderr: " + err)


repos = []
try:
    # ---- fixture A: consistent -> exit 0 -------------------------------
    a = new_repo()
    repos.append(a)
    write(a, "SCORECARD.md",
          "## Round 1 — declaration (2026-01-01T00:00Z, same minute as commit)\n"
          "body\n")
    write(a, "LOG.md",
          "## Round 1 — log (2025-12-31T23:00Z, stamped early)\nbody\n")
    run(["git", "-C", a, "add", "SCORECARD.md", "LOG.md"])
    commit(a, "2026-01-01T00:00:30+00:00", "consistent")
    line("A-consistent", check(a, "--json", os.path.join(SCRATCH, "fxA.json")))
    line("A-consistent-require2", check(a, "--require-timed", "2"))

    # ---- fixture B: one heading stamped ahead -> exit 1 -----------------
    b = new_repo()
    repos.append(b)
    write(b, "SCORECARD.md", "## Round 1 — declaration (2026-01-01T00:00Z, fine)\nbody\n")
    write(b, "LOG.md", "## Round 1 — log (2026-01-01T00:00Z, fine)\nbody\n")
    run(["git", "-C", b, "add", "SCORECARD.md", "LOG.md"])
    commit(b, "2026-01-01T00:00:00+00:00", "base")
    write(b, "LOG.md",
          "## Round 1 — log (2026-01-01T00:00Z, fine)\nbody\n\n"
          "## Round 2 — log (2026-01-02T00:05Z, stamped ahead of its commit)\nbody\n")
    run(["git", "-C", b, "add", "LOG.md"])
    commit(b, "2026-01-02T00:00:00+00:00", "ahead")
    line("B-stamped-ahead", check(b, "--json", os.path.join(SCRATCH, "fxB.json")))
    line("B-match-round1", check(b, "--match", r"Round 1"))
    line("B-match-round9-vacuous", check(b, "--match", r"Round 9", "--require-timed", "1"))

    # ---- fixture C: equality at second precision -> exit 0 -------------
    c = new_repo()
    repos.append(c)
    write(c, "SCORECARD.md", "## Round 3 — exact second (2026-01-03T00:00:00Z)\nbody\n")
    write(c, "LOG.md", "## Round 3 — log (2026-01-03T00:00:00Z)\nbody\n")
    run(["git", "-C", c, "add", "SCORECARD.md", "LOG.md"])
    commit(c, "2026-01-03T00:00:00+00:00", "exact")
    line("C-exact-second", check(c))

    # ---- fixture D: missing file -> exit 2 -----------------------------
    d = new_repo()
    repos.append(d)
    write(d, "SCORECARD.md", "## Round 4 — only one file (2026-01-04T00:00Z)\nbody\n")
    run(["git", "-C", d, "add", "SCORECARD.md"])
    commit(d, "2026-01-04T00:00:00+00:00", "single file")
    line("D-missing-log", check(d))
finally:
    for repo in repos:
        shutil.rmtree(repo, ignore_errors=True)
