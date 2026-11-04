#!/usr/bin/env python3
"""Count only KR rows satisfying the round-69 frozen evidence clauses.

Reads Git objects and snapshot files only; creates no temporary files.

`--selftest` runs a hermetic suite that drives this public CLI, by subprocess,
against a throwaway fixture repository (fixed allowlisted environment with no
ambient Git controls, fixed identity) and
asserts the exit code and the stable KR_ROW/KR_ERROR findings of every case;
it prints `SELFTEST: PASS/FAIL (N cases, N passed, N failed)` and exits 0 on
success, 3 when any case fails. Usage and could-not-evaluate semantics are
unchanged: exit 2, never a traceback.
"""
import argparse
from collections import Counter
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

NOTE = "corpus/knowledge/kernel-taint-plane-r69.md"
REGISTRY = "corpus/SOURCES.md"


def unfenced(text):
    """Yield lines outside CommonMark backtick/tilde fences (0-3 spaces)."""
    fence = None
    for line in text.splitlines():
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) +
                            "{" + str(fence[1]) + r",}[ \t]*", line):
                fence = None
            continue
        opening = re.match(r" {0,3}(`{3,}|~{3,})(.*)$", line)
        if opening and (opening[1][0] != "`" or "`" not in opening[2]):
            fence = (opening[1][0], len(opening[1]))
            continue
        yield line


def registry_ids(text):
    ids = set()
    in_registry = False
    for line in unfenced(text):
        heading = re.match(r" {0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading:
            if heading[2] == "Registry":
                in_registry = True
                level = len(heading[1])
            elif in_registry and len(heading[1]) <= level:
                in_registry = False
        if in_registry:
            row = re.match(r" {0,3}\|\s*(S[0-9]{3,})\s*\|", line)
            if row:
                ids.add(row[1])
    return ids


def git(lane, *args):
    return subprocess.run(["git", "-C", str(lane), *args],
                          capture_output=True, text=True, encoding="utf-8")


def default_lane():
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    return Path(__file__).resolve().parent.parent


def evaluate(note, sources, snapshots):
    rows = []
    for line in unfenced(note):
        if line.startswith("| KR"):
            cells = [cell.strip() for cell in line.split("|")[1:]]
            if cells and not cells[-1]:
                cells.pop()
            rows.append(cells)
    counts = Counter(cells[0] for cells in rows)
    verified = 0
    results = []
    for cells in rows:
        ident = cells[0]
        clause = None
        if len(cells) != 6:
            clause = "cells"
        elif not re.fullmatch(r"KR[0-9]+", ident):
            clause = "id"
        elif counts[ident] != 1:
            clause = "unique-id"
        elif len(cells[1].split()) < 12:
            clause = "statement"
        elif not re.fullmatch(r"source=S[0-9]{3,}", cells[2]) or cells[2][7:] not in sources:
            clause = "source"
        else:
            name = cells[3].removeprefix("snapshot=")
            if (not cells[3].startswith("snapshot=") or not name or
                    name in (".", "..") or Path(name).name != name):
                clause = "snapshot"
            else:
                try:
                    data = (snapshots / name).read_bytes()
                except OSError:
                    clause = "snapshot"
                else:
                    digest = cells[4].removeprefix("digest=")
                    if (not cells[4].startswith("digest=") or
                            not re.fullmatch(r"[0-9a-f]{64}", digest) or
                            hashlib.sha256(data).hexdigest() != digest):
                        clause = "digest"
                    else:
                        quote = re.fullmatch(r'quote="(.*)"', cells[5])
                        if not quote or not 1 <= len(quote[1].split()) <= 25:
                            clause = "quote"
                        else:
                            try:
                                text = data.decode("utf-8")
                            except UnicodeError:
                                clause = "quote"
                            else:
                                if " ".join(quote[1].split()) not in " ".join(text.split()):
                                    clause = "quote"
        if clause is None:
            verified += 1
        results.append(f"KR_ROW {ident} " + ("ok" if clause is None else f"fail:{clause}"))
    print(f"KR_ROWS={len(rows)} KR_VERIFIED={verified}")
    print("\n".join(results), end="\n" if results else "")
    return 0 if len(rows) == verified and verified >= 5 else 1


SELFTEST_SNAPSHOTS = {
    "kr-a.txt": "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu",
    "kr-b.txt": "The taint flag turns when a proprietary module loads and the ring stays tainted.",
    "kr-c.txt": "Restart conditions: oneshot services never restart, and manual stops suppress restart.",
}
SELFTEST_REGISTRY = (
    "# Fixture sources\n\n"
    "## Registry\n\n"
    "| S901 | https://fixture.invalid/kernel-taint-r69 | docs | A | "
    "selftest fixture source pinning the round-69 knowledge note |\n\n"
    "## Later heading\n\n"
    "The registry section ended above, so this decoy id is not one:\n"
    "| S902 | https://fixture.invalid/decoy | docs | A | decoy row outside the Registry section |\n"
)
SELFTEST_STATEMENT = ("The statement clause needs at least twelve words to keep "
                      "this row verifiable")


def _selftest_env(sandbox):
    """Fixed allowlisted environment; no ambient variable leaks in.

    PATH is pinned to /usr/bin:/bin (trust is scoped to the system git binary,
    not to any filesystem confinement — the fixture runs with this process's
    permissions), HOME and TMPDIR point into the throwaway sandbox, so neither
    user global git config (hooks, init.templateDir) nor system config can
    reach the fixture and stray config writes stay inside it. GIT_INDEX_FILE,
    GIT_OBJECT_DIRECTORY, GIT_DIR/GIT_WORK_TREE, GIT_CONFIG_COUNT,
    GIT_CONFIG_PARAMETERS and GIT_TEMPLATE_DIR are absent by construction.
    """
    return {
        "PATH": "/usr/bin:/bin",
        "HOME": str(sandbox),
        "TMPDIR": str(sandbox),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_AUTHOR_NAME": "selftest-fixture",
        "GIT_AUTHOR_EMAIL": "selftest-fixture@invalid",
        "GIT_COMMITTER_NAME": "selftest-fixture",
        "GIT_COMMITTER_EMAIL": "selftest-fixture@invalid",
        "GIT_AUTHOR_DATE": "2005-04-07T22:13:13+00:00",
        "GIT_COMMITTER_DATE": "2005-04-07T22:13:13+00:00",
        "LC_ALL": "C",
    }


def _selftest_git(env, repo, *args):
    done = subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, encoding="utf-8",
                          env=env, timeout=60)
    if done.returncode:
        raise RuntimeError("fixture git " + args[0] + " failed: " +
                           done.stderr.strip()[:160])
    return done.stdout.strip()


def _selftest_commit(env, repo, files, message):
    """Write files and commit; assert the fixture toplevel before mutating."""
    top = _selftest_git(env, repo, "rev-parse", "--show-toplevel")
    if Path(top).resolve() != repo.resolve():
        raise RuntimeError("fixture toplevel is not the fixture repository: " + top)
    for rel, data in sorted(files.items()):
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    _selftest_git(env, repo, "add", "-A", "--", ".")
    _selftest_git(env, repo, "-c", "commit.gpgsign=false",
                  "commit", "-q", "-m", message)
    return _selftest_git(env, repo, "rev-parse", "HEAD")


def _selftest_note(rows, fenced_decoy=False):
    text = "# Kernel taint plane (selftest fixture)\n\n" + "\n".join(rows) + "\n"
    if fenced_decoy:
        text += ("\n```text\n| KR900 | a fenced decoy row must stay invisible to the "
                 "unfenced reader |\n```\n")
    return text


def _selftest_row(ident, digest, source="S901", snapshot="kr-a.txt",
                  quote="alpha beta gamma delta"):
    return (f"| {ident} | {SELFTEST_STATEMENT} | source={source} | "
            f"snapshot={snapshot} | digest={digest} | quote=\"{quote}\" |")


def _selftest_run():
    tool = Path(__file__).resolve()
    cases, failures = [], []
    with tempfile.TemporaryDirectory(prefix="count-kr-rows-r69-selftest-") as tmp:
        root = Path(tmp).resolve()
        env = _selftest_env(root)
        snapshot_data = {name: text.encode("utf-8")
                         for name, text in SELFTEST_SNAPSHOTS.items()}
        digests = {name: hashlib.sha256(data).hexdigest()
                   for name, data in snapshot_data.items()}
        repo = root / "repo"
        repo.mkdir(parents=True)
        _selftest_git(env, repo, "init", "-q", "-b", "master")
        rev0 = _selftest_commit(env, repo,
                                {"corpus/SOURCES.md": SELFTEST_REGISTRY.encode("utf-8")},
                                "fixture registry only")
        rev1 = _selftest_commit(env, repo, {
            NOTE: _selftest_note([
                _selftest_row("KR001", digests["kr-a.txt"]),
                _selftest_row("KR002", digests["kr-b.txt"], snapshot="kr-b.txt",
                              quote="proprietary module loads"),
                _selftest_row("KR003", digests["kr-a.txt"],
                              quote="iota kappa lambda mu"),
                _selftest_row("KR004", digests["kr-c.txt"], snapshot="kr-c.txt",
                              quote="oneshot services never restart"),
                _selftest_row("KR005", digests["kr-b.txt"], snapshot="kr-b.txt",
                              quote="ring stays tainted"),
            ], fenced_decoy=True).encode("utf-8"),
        }, "fixture note with five verified rows")

        def snapdir(name, members):
            path = root / name
            path.mkdir()
            for fname, data in members:
                (path / fname).write_bytes(data)
            return path

        snaps_full = snapdir("snaps-full", snapshot_data.items())
        snaps_short = snapdir("snaps-short",
                              [("kr-a.txt", snapshot_data["kr-a.txt"]),
                               ("kr-b.txt", snapshot_data["kr-b.txt"]),
                               ("decoy.txt", b"decoy\n")])

        def case(name, argv, want_rc, stdout_finds=(), stderr_finds=()):
            done = subprocess.run([sys.executable, str(tool), *argv],
                                  capture_output=True, text=True,
                                  encoding="utf-8", env=env, timeout=120,
                                  cwd=str(root))
            problems = []
            if done.returncode != want_rc:
                problems.append(f"rc {done.returncode} != {want_rc}")
            for token in stdout_finds:
                if token not in done.stdout:
                    problems.append("stdout missing " + repr(token))
            for token in stderr_finds:
                if token not in done.stderr:
                    problems.append("stderr missing " + repr(token))
            cases.append(name)
            if problems:
                failures.append(f"{name}: " + "; ".join(problems))
                print(f"selftest {name}: FAIL ({'; '.join(problems)})", file=sys.stderr)
            else:
                print(f"selftest {name}: ok")

        case("positive", ["--revision", rev1, "--lane", str(repo),
                          "--snapshots", str(snaps_full)], 0,
             ("KR_ROWS=5 KR_VERIFIED=5", "KR_ROW KR001 ok", "KR_ROW KR002 ok",
              "KR_ROW KR003 ok", "KR_ROW KR004 ok", "KR_ROW KR005 ok"))
        case("missing-note", ["--revision", rev0, "--lane", str(repo),
                              "--snapshots", str(snaps_full)], 1,
             ("KR_ROWS=0 KR_VERIFIED=0",))
        case("missing-snapshot", ["--revision", rev1, "--lane", str(repo),
                                  "--snapshots", str(snaps_short)], 1,
             ("KR_ROWS=5 KR_VERIFIED=4", "KR_ROW KR004 fail:snapshot",
              "KR_ROW KR001 ok"))
        wrong_source = _selftest_note([
            _selftest_row("KR001", digests["kr-a.txt"], source="S902"),
            _selftest_row("KR002", digests["kr-b.txt"], snapshot="kr-b.txt",
                          quote="proprietary module loads"),
            _selftest_row("KR003", digests["kr-a.txt"], quote="iota kappa lambda mu"),
            _selftest_row("KR004", digests["kr-c.txt"], snapshot="kr-c.txt",
                          quote="oneshot services never restart"),
            _selftest_row("KR005", digests["kr-b.txt"], snapshot="kr-b.txt",
                          quote="ring stays tainted"),
        ]).encode("utf-8")
        rev2 = _selftest_commit(env, repo, {NOTE: wrong_source}, "wrong source row")
        case("wrong-source", ["--revision", rev2, "--lane", str(repo),
                              "--snapshots", str(snaps_full)], 1,
             ("KR_ROWS=5 KR_VERIFIED=4", "KR_ROW KR001 fail:source"))
        wrong_quote = _selftest_note([
            _selftest_row("KR001", digests["kr-a.txt"], quote="absent omega nowhere"),
            _selftest_row("KR002", digests["kr-b.txt"], snapshot="kr-b.txt",
                          quote="proprietary module loads"),
            _selftest_row("KR003", digests["kr-a.txt"], quote="iota kappa lambda mu"),
            _selftest_row("KR004", digests["kr-c.txt"], snapshot="kr-c.txt",
                          quote="oneshot services never restart"),
            _selftest_row("KR005", digests["kr-b.txt"], snapshot="kr-b.txt",
                          quote="ring stays tainted"),
        ]).encode("utf-8")
        rev3 = _selftest_commit(env, repo, {NOTE: wrong_quote}, "wrong quote row")
        case("wrong-quote", ["--revision", rev3, "--lane", str(repo),
                             "--snapshots", str(snaps_full)], 1,
             ("KR_ROWS=5 KR_VERIFIED=4", "KR_ROW KR001 fail:quote"))
        bad_digest = _selftest_note([
            _selftest_row("KR001", "0" * 64),
            _selftest_row("KR002", digests["kr-b.txt"], snapshot="kr-b.txt",
                          quote="proprietary module loads"),
            _selftest_row("KR003", digests["kr-a.txt"], quote="iota kappa lambda mu"),
            _selftest_row("KR004", digests["kr-c.txt"], snapshot="kr-c.txt",
                          quote="oneshot services never restart"),
            _selftest_row("KR005", digests["kr-b.txt"], snapshot="kr-b.txt",
                          quote="ring stays tainted"),
        ]).encode("utf-8")
        rev4 = _selftest_commit(env, repo, {NOTE: bad_digest}, "digest mismatch row")
        case("digest-mismatch", ["--revision", rev4, "--lane", str(repo),
                                 "--snapshots", str(snaps_full)], 1,
             ("KR_ROWS=5 KR_VERIFIED=4", "KR_ROW KR001 fail:digest"))
        malformed = _selftest_note([
            f"| KR001 | {SELFTEST_STATEMENT} | source=S901 | "
            f"snapshot=kr-a.txt | digest={digests['kr-a.txt']} |",
            _selftest_row("KR002", digests["kr-b.txt"], snapshot="kr-b.txt",
                          quote="proprietary module loads"),
            _selftest_row("KR003", digests["kr-a.txt"], quote="iota kappa lambda mu"),
            _selftest_row("KR004", digests["kr-c.txt"], snapshot="kr-c.txt",
                          quote="oneshot services never restart"),
            _selftest_row("KR005", digests["kr-b.txt"], snapshot="kr-b.txt",
                          quote="ring stays tainted"),
        ]).encode("utf-8")
        rev5 = _selftest_commit(env, repo, {NOTE: malformed}, "malformed row")
        case("malformed-cells", ["--revision", rev5, "--lane", str(repo),
                                 "--snapshots", str(snaps_full)], 1,
             ("KR_ROWS=5 KR_VERIFIED=4", "KR_ROW KR001 fail:cells"))
        case("missing-revision", ["--revision", "0" * 40, "--lane", str(repo),
                                  "--snapshots", str(snaps_full)], 2, (),
             ("KR_ERROR missing revision:",))
        case("missing-snapshot-dir", ["--revision", rev1, "--lane", str(repo),
                                      "--snapshots", str(root / "snaps-absent")],
             2, (), ("KR_ERROR missing snapshot directory:",))
        case("usage-requires-revision", [], 2, (), ("usage:", "--revision"))
    total, passed = len(cases), len(cases) - len(failures)
    status = "PASS" if not failures else "FAIL"
    print(f"SELFTEST: {status} ({total} cases, {passed} passed, {len(failures)} failed)")
    return 0 if not failures else 3


def selftest():
    """Run the hermetic public-CLI suite; harness faults fail loudly, rc 3."""
    try:
        return _selftest_run()
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"SELFTEST: FAIL (harness {type(exc).__name__}: {str(exc)[:160]})",
              file=sys.stderr)
        return 3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision")
    parser.add_argument("--lane", type=Path, default=default_lane())
    parser.add_argument("--snapshots", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if not args.revision:
        parser.error("--revision is required")
    snapshots = args.snapshots or args.lane / ".ufo/waves/round-69/before/src"
    try:
        revision = git(args.lane, "rev-parse", "--verify", "--end-of-options", args.revision + "^{commit}")
        if revision.returncode:
            raise ValueError("missing revision: " + revision.stderr.strip())
        commit = revision.stdout.strip()
        registry = git(args.lane, "show", commit + ":" + REGISTRY)
        if registry.returncode:
            raise ValueError("unreadable registry: " + registry.stderr.strip())
        if not snapshots.is_dir():
            raise ValueError("missing snapshot directory: " + str(snapshots))
        # Iteration checks directory readability without creating temporary files.
        next(snapshots.iterdir(), None)
        note = git(args.lane, "show", commit + ":" + NOTE)
        if note.returncode:
            present = git(args.lane, "cat-file", "-e", commit + ":" + NOTE)
            if present.returncode == 0:
                raise ValueError("unreadable note: " + note.stderr.strip())
            return evaluate("", registry_ids(registry.stdout), snapshots)
        return evaluate(note.stdout, registry_ids(registry.stdout), snapshots)
    except (OSError, UnicodeError, ValueError) as error:
        print("KR_ERROR " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
