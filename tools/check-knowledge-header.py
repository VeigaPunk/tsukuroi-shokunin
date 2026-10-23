#!/usr/bin/env python3
"""Knowledge-header gate (QUALITY 8; rounds 33-34).

QUALITY 8 (`corpus/QUALITY.md:12`) requires every knowledge entry to carry
`source:`, `verified-at:` and `recheck:` lines, the last with an ISO date or a
cadence (`<N>d` or `on-release`). Round 33 was rejected because its C2 note had
`recheck:` only (`corpus/lessons/round-33-verifier-spotcheck.md` §2, §4, §5): a
written convention no gate enforced. This gate reads every `*.md` under
`corpus/knowledge/` at an immutable revision and reports, per note:

  KNOWLEDGE-HEADER-MISSING  no line starts with `source:`, `verified-at:` or
                            `recheck:` — one finding per absent key.
  KNOWLEDGE-HEADER-VALUE    the operative `verified-at:` line carries no ISO
                            calendar date (YYYY-MM-DD), or the operative
                            `recheck:` line carries neither an ISO date nor a
                            cadence (`<N>d`, `on-release`).

A key counts only at column 0 and outside a fenced code block: an example
inside ``` or ~~~ fences, or a `source:` word mid-sentence, is not a header —
the same rule `tools/check-recheck-commands.py` applies to headings. A key's
operative line is its LAST occurrence, because later lines supersede earlier
pointer lines (the journal-boot-plane convention `check-recheck-commands.py`
follows): a note whose first `recheck:` is a bare section pointer and whose
appended block carries `30d` passes on the appended line. A date is a day the
calendar has; `2026-13-45` satisfies no rule.

`--revision` is bound by the shared `tools/_revision.py` (QUALITY 27: 7-64 hex,
landed on `--branch`, pushed when that branch has an origin ref; one finding,
exit 2). `--lane` selects the repository; the default is the nearest ancestor of
this file that holds `tools/_revision.py`, so both the landed `tools/` copy and
a seat-directory copy work without a cwd. Read-only: git plumbing reads only,
nothing is written (`sys.dont_write_bytecode` keeps the shared import from
dropping a `__pycache__` into the lane).

Exit 0 pass / 1 finding / 2 could-not-evaluate; JSON on stdout.
`--selftest` runs a hermetic fixture repository (should-fail cases for each
missing key, a missing date, a missing cadence, a fenced-only key, a mid-line
key, plus pass cases and the CLI/binding refusals).
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # the shared-module import stays read-only

import argparse
import datetime
import json
import re
import subprocess
import tempfile
from collections import namedtuple
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
KEYS = ("source", "verified-at", "recheck")
SCOPE = "corpus/knowledge"
ISO = re.compile(r"(?<!\d)(\d{4})-(\d{2})-(\d{2})(?!\d)")
CADENCE = re.compile(r"(?<!\w)\d+d(?!\w)")
ON_RELEASE = re.compile(r"\bon-release\b", re.I)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
MISSING = "KNOWLEDGE-HEADER-MISSING"
VALUE = "KNOWLEDGE-HEADER-VALUE"

Finding = namedtuple("Finding", "id site detail")
Note = namedtuple("Note", "path lines problems")


# --- lane bootstrap: resolve the repository, then import the shared binding -------------------
def _lane_flag(argv):
    for index, arg in enumerate(argv):
        if arg == "--lane":
            return argv[index + 1].strip() if index + 1 < len(argv) else ""
        if arg.startswith("--lane="):
            return arg[len("--lane="):].strip()
    return None


def _default_lane():
    for parent in Path(__file__).resolve().parents[:10]:
        if (parent / "tools" / "_revision.py").is_file() \
                and (parent / SCOPE).is_dir():
            return parent
    return None


def _unresolved(detail):
    print(json.dumps({"status": "CANNOT_EVALUATE", "scope": "none: lane unresolved",
                      "findings": [{"id": "E-LANE-UNRESOLVED", "site": "lane",
                                    "detail": detail}]}, sort_keys=True))
    return CANNOT


_FLAG = _lane_flag(sys.argv[1:])
LANE = Path(_FLAG).resolve() if _FLAG else _default_lane()
if LANE is None or not (LANE / "tools" / "_revision.py").is_file():
    raise SystemExit(_unresolved(f"--lane must name a repository with tools/_revision.py"
                                 f" (resolved {LANE})"[:160]))
sys.path.insert(0, str(LANE / "tools"))
import _revision  # noqa: E402  (path bootstrap above)


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def git(repo, *args, timeout=60):
    proc = subprocess.run(["git", "--no-pager", "-C", str(repo), *args],
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=_revision.clean_env(),
                          timeout=timeout)
    return proc


def read_blob(repo, commit, path):
    spec = f"{commit}:{path}"
    kind = git(repo, "cat-file", "-t", spec)
    if kind.returncode != 0:
        return None
    if kind.stdout.decode("ascii", "replace").strip() != "blob":
        raise Cannot("E-PATH-INVALID", path, "not a regular file at revision")
    proc = git(repo, "show", spec)
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()[:120]
        raise Cannot("E-GIT-FAILED", path, detail or "git show failed")
    return proc.stdout


def notes_at(repo, sha):
    listing = git(repo, "ls-tree", "-r", "--name-only", sha, SCOPE)
    if listing.returncode != 0:
        detail = listing.stderr.decode("utf-8", "replace").strip()[:120]
        raise Cannot("E-GIT-FAILED", SCOPE, detail or "git ls-tree failed")
    names = [name for name in listing.stdout.decode("utf-8", "replace").splitlines()
             if name.endswith(".md")]
    if not names:
        raise Cannot("E-PATH-MISSING", SCOPE, f"no *.md under {SCOPE} at revision")
    files = []
    for path in sorted(names):
        raw = read_blob(repo, sha, path)
        if raw is None:
            raise Cannot("E-PATH-MISSING", path, "file absent at revision")
        try:
            files.append((path, raw.decode("utf-8")))
        except UnicodeDecodeError as exc:
            raise Cannot("E-PATH-INVALID", path, f"not UTF-8: {exc}"[:120])
    return files


# --- the rule ---------------------------------------------------------------------------------
def header_lines(text):
    """Map each key to its `(line_number, value)` occurrences at column 0, outside fences."""
    found = {key: [] for key in KEYS}
    fence = None
    for number, raw in enumerate(text.split("\n"), 1):
        line = raw[:-1] if raw.endswith("\r") else raw
        marker = FENCE.match(line)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) \
                    and not line.strip()[len(run):].strip():
                fence = None  # a closing fence carries no info string
            continue
        if fence is not None:
            continue
        for key in KEYS:
            if line.startswith(key + ":"):
                found[key].append((number, line[len(key) + 1:].strip()))
                break
    return found


def has_date(value):
    """True when `value` carries an ISO date whose day the calendar has."""
    for year, month, day in ISO.findall(value):
        try:
            datetime.date(int(year), int(month), int(day))
        except ValueError:
            continue
        return True
    return False


def date_problem(value):
    if has_date(value):
        return None
    if ISO.search(value):
        return "verified-at: ISO date is not a calendar date"
    return "verified-at: carries no ISO date (YYYY-MM-DD)"


def cadence_problem(value):
    if has_date(value) or CADENCE.search(value) or ON_RELEASE.search(value):
        return None
    return "recheck: carries no ISO date, no <N>d cadence and no on-release"


RULES = {"source": None, "verified-at": date_problem, "recheck": cadence_problem}


def evaluate(files):
    findings, notes = [], []
    for path, text in files:
        found = header_lines(text)
        lines, problems = {}, []
        for key in KEYS:
            hits = found[key]
            lines[key] = hits[-1][0] if hits else None
            if not hits:
                detail = f"{key}: no line starts with {key}: (outside fenced blocks)"
                findings.append(Finding(MISSING, path, detail))
                problems.append(detail)
                continue
            rule = RULES[key]
            if rule is None:
                continue
            problem = rule(hits[-1][1])
            if problem:
                findings.append(Finding(VALUE, path, f"{problem} at line {hits[-1][0]}"))
                problems.append(f"{problem} at line {hits[-1][0]}")
        notes.append(Note(path, lines, problems))
    findings = [Finding(*key) for key in sorted({tuple(f) for f in findings})]
    return findings, notes


# --- CLI --------------------------------------------------------------------------------------
def emit(status, revision, branch, branch_tip, origin_tip, findings, notes, out=None,
         message=None):
    payload = {
        "status": status,
        "revision": revision,
        "branch": branch,
        "branch_tip": branch_tip,
        "origin_tip": origin_tip,
        "note_count": len(notes),
        "complete_count": sum(1 for note in notes if all(note.lines[key] for key in KEYS)),
        "clean_count": sum(1 for note in notes if not note.problems),
        "finding_count": len(findings),
        "scope": (f"every *.md under {SCOPE}/ at the bound revision; column-0 header keys "
                  "outside fenced blocks; operative (last) value per key; read-only, no "
                  "host action taken"),
        "findings": [{"id": item.id, "site": item.site, "detail": item.detail}
                     for item in findings],
        "notes": [{"path": note.path, "lines": note.lines, "problems": note.problems}
                  for note in notes],
    }
    if message:
        payload["message"] = message
    print(json.dumps(payload, sort_keys=True), file=out or sys.stdout)
    return {"PASS": PASS, "FAIL": FAIL, "CANNOT_EVALUATE": CANNOT}[status]


def build_parser():
    parser = argparse.ArgumentParser(
        description="Read-only knowledge-header gate (QUALITY 8).", exit_on_error=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision", metavar="REV",
                       help="required: 7-64 hex commit; HEAD/@/refs are rejected")
    group.add_argument("--selftest", action="store_true", help="hermetic fixture suite")
    parser.add_argument("--lane", metavar="REPO", default=None,
                        help="lane repository (default: nearest ancestor with "
                             "tools/_revision.py)")
    parser.add_argument("--branch", default="master", metavar="BRANCH",
                        help="branch the revision must be landed on (default: master)")
    return parser


def run(argv, lane=LANE, out=None):
    try:
        args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit) as exc:
        if isinstance(exc, SystemExit) and not exc.code:
            return 0
        return emit("CANNOT_EVALUATE", "worktree", "master", None, None,
                    [Finding("E-CLI", "cli",
                             "--revision REV or --selftest required")], [], out)
    if args.selftest:
        return selftest(out)
    branch = args.branch
    sha = tip = origin_tip = None
    try:
        repo = Path(args.lane).resolve() if args.lane else Path(lane)
        try:
            binding = _revision.bind(repo, args.revision, branch)
        except _revision.RevisionError as exc:
            try:
                tip = _revision.branch_tip(repo, branch)
            except Exception:  # a missing branch has no tip; the finding stands
                tip = None
            raise Cannot(exc.fid, exc.site, exc.detail) from exc
        sha, tip, origin_tip = binding.sha, binding.branch_tip, binding.origin_tip
        files = notes_at(repo, sha)
        findings, notes = evaluate(files)
    except Cannot as exc:
        return emit("CANNOT_EVALUATE", sha or args.revision or "worktree", branch, tip,
                    origin_tip, [Finding(exc.fid, exc.site, exc.detail)], [], out)
    except (_revision.RevisionError, subprocess.TimeoutExpired, OSError) as exc:
        return emit("CANNOT_EVALUATE", sha or args.revision or "worktree", branch, tip,
                    origin_tip, [Finding("E-GIT-FAILED", "git", str(exc)[:120])], [], out)
    except Exception as exc:  # unreadable input is CANNOT, never a traceback
        return emit("CANNOT_EVALUATE", sha or args.revision or "worktree", branch, tip,
                    origin_tip, [Finding("E-INTERNAL", "gate", str(exc)[:120])], [], out)
    return emit("PASS" if not findings else "FAIL", sha, branch, tip, origin_tip,
                findings, notes, out)


# --- selftest ---------------------------------------------------------------------------------
class _Stdout:
    def __init__(self):
        self.chunks = []

    def write(self, text):
        self.chunks.append(text)

    def flush(self):
        pass

    @property
    def value(self):
        return "".join(self.chunks)


def sandbox_git(repo, *args):
    proc = git(repo, *args)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: "
                           + proc.stderr.decode("utf-8", "replace").strip()[:160])
    return proc.stdout.decode("utf-8", "replace")


def sandbox_commit(repo, tree):
    for name, text in tree.items():
        target = repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    sandbox_git(repo, "add", *sorted(tree))
    sandbox_git(repo, "commit", "-q", "-m", "fixture")
    return sandbox_git(repo, "rev-parse", "HEAD").strip()


def header(source="own-work fixture, 2026-10-23.", verified="2026-10-23",
           recheck="30d; procedure: rerun the fixture probe."):
    return (f"# Fixture note\n\nsource: {source}\nverified-at: {verified}\n"
            f"recheck: {recheck}\n\nBody prose.\n")


def note(text):
    return {f"{SCOPE}/fixture.md": text}


def selftest(out=None):
    out = out or sys.stdout
    failures, total = [], 0

    def case(name, argv, want_code, want_ids, want_details=None, want_counts=None):
        nonlocal total
        total += 1
        buffer = _Stdout()
        try:
            code = run(argv, lane=repo, out=buffer)
            payload = json.loads(buffer.value)
        except Exception as exc:  # a crashed case is a failed case, not a crash
            failures.append(f"{name}: raised {exc!r}")
            return
        problems = []
        if code != want_code:
            problems.append(f"exit={code}/{want_code}")
        findings = payload.get("findings", [])
        got_ids = {item["id"] for item in findings}
        if got_ids != set(want_ids):
            problems.append("ids=" + ",".join(sorted(got_ids))
                            + " want=" + ",".join(sorted(want_ids)))
        if want_code == CANNOT and len(findings) != 1:
            problems.append(f"finding_count={len(findings)}/1")
        if payload.get("status") != {PASS: "PASS", FAIL: "FAIL",
                                     CANNOT: "CANNOT_EVALUATE"}[want_code]:
            problems.append(f"status={payload.get('status')}")
        for fid, needle in (want_details or {}).items():
            hit = [item for item in findings if item["id"] == fid
                   and needle in item["detail"]]
            if not hit:
                problems.append(f"detail[{fid}] lacks {needle!r}")
        for key, value in (want_counts or {}).items():
            if payload.get(key) != value:
                problems.append(f"{key}={payload.get(key)}/{value}")
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))

    repo = Path(tempfile.mkdtemp(prefix="knowledge-header-gate-"))
    try:
        sandbox_git(repo, "-c", "init.defaultBranch=master", "init", "-q")
        sandbox_git(repo, "config", "user.email", "fixture@example.invalid")
        sandbox_git(repo, "config", "user.name", "Fixture")
        sandbox_git(repo, "config", "commit.gpgsign", "false")
        sandbox_git(repo, "config", "core.hooksPath", "/dev/null")
        first = sandbox_commit(repo, note(header()))

        clean = first
        case("clean-note", ["--revision", clean], PASS, set(),
             want_counts={"note_count": 1, "complete_count": 1, "clean_count": 1,
                          "finding_count": 0})
        # 1-3. each absent key is its own finding, named in the detail.
        bare = sandbox_commit(repo, note("# Fixture\n\nrecheck: 30d.\n"))
        case("missing-source-verified-at", ["--revision", bare], FAIL, {MISSING},
             {MISSING: "source:"}, {"finding_count": 2, "complete_count": 0})
        no_source = sandbox_commit(repo, note(
            "# Fixture\n\nverified-at: 2026-10-23\nrecheck: 30d.\n"))
        case("missing-source", ["--revision", no_source], FAIL, {MISSING},
             {MISSING: "source:"}, {"finding_count": 1})
        no_verified = sandbox_commit(repo, note(
            "# Fixture\n\nsource: S999.\nrecheck: 30d.\n"))
        case("missing-verified-at", ["--revision", no_verified], FAIL, {MISSING},
             {MISSING: "verified-at:"}, {"finding_count": 1})
        no_recheck = sandbox_commit(repo, note(
            "# Fixture\n\nsource: S999.\nverified-at: 2026-10-23\n"))
        case("missing-recheck", ["--revision", no_recheck], FAIL, {MISSING},
             {MISSING: "recheck:"}, {"finding_count": 1})
        # 4-6. the value rules.
        undated = sandbox_commit(repo, note(header(verified="yesterday")))
        case("verified-at-without-date", ["--revision", undated], FAIL, {VALUE},
             {VALUE: "verified-at:"}, {"finding_count": 1, "complete_count": 1})
        impossible = sandbox_commit(repo, note(header(verified="2026-13-45")))
        case("verified-at-impossible-date", ["--revision", impossible], FAIL, {VALUE},
             {VALUE: "calendar"}, {"finding_count": 1})
        no_cadence = sandbox_commit(repo, note(header(recheck="rerun the fixture probe.")))
        case("recheck-without-date-or-cadence", ["--revision", no_cadence], FAIL, {VALUE},
             {VALUE: "recheck:"}, {"finding_count": 1})
        # 7-9. accepted recheck values.
        dated = sandbox_commit(repo, note(header(recheck="2026-11-01; rerun once.")))
        case("recheck-iso-date", ["--revision", dated], PASS, set(),
             want_counts={"finding_count": 0})
        release = sandbox_commit(repo, note(
            header(recheck="on-release of the upstream page; rerun then.")))
        case("recheck-on-release", ["--revision", release], PASS, set(),
             want_counts={"finding_count": 0})
        pointer = sandbox_commit(repo, note(
            header(recheck="§4 for the counting command.") + "\n## Appended block\n\n"
            "recheck: 90d; procedure: §4.\n"))
        case("appended-block-supersedes-pointer", ["--revision", pointer], PASS, set(),
             want_counts={"finding_count": 0})
        # 10. keys only inside a fenced block are examples, not headers.
        fenced = sandbox_commit(repo, note(
            "# Fixture\n\n```\nsource: S999.\nverified-at: 2026-10-23\nrecheck: 30d\n"
            "```\n"))
        case("keys-only-in-fence", ["--revision", fenced], FAIL, {MISSING},
             want_counts={"finding_count": 3, "complete_count": 0})
        tilde = sandbox_commit(repo, note(
            "# Fixture\n\n~~~text\nsource: S999.\n~~~\n"))
        case("tilde-fence-only", ["--revision", tilde], FAIL, {MISSING},
             want_counts={"finding_count": 3})
        # 11. keys mid-line are prose, not headers.
        midline = sandbox_commit(repo, note(
            "# Fixture\n\nThe crib said source: S999 and verified-at: 2026-10-23 and "
            "recheck: 30d, but no line starts with them.\n"))
        case("keys-mid-line", ["--revision", midline], FAIL, {MISSING},
             want_counts={"finding_count": 3})
        # 12. indented (four-space) key is a code block, not a header.
        indented = sandbox_commit(repo, note(
            "# Fixture\n\n    source: S999.\n\nverified-at: 2026-10-23\nrecheck: 30d.\n"))
        case("indented-key", ["--revision", indented], FAIL, {MISSING},
             {MISSING: "source:"}, {"finding_count": 1})
        # 13. a clean header next to a non-markdown twin: the twin is out of scope.
        twin = sandbox_commit(repo, {f"{SCOPE}/fixture.md": header(),
                                     f"{SCOPE}/fixture.json": '{"note": "no header"}\n'})
        case("json-twin-out-of-scope", ["--revision", twin], PASS, set(),
             want_counts={"note_count": 1, "finding_count": 0})
        # 14. the operative recheck is the last one, even when the first is red.
        late = sandbox_commit(repo, note(
            header(recheck="rerun the probe.") + "\n## Later\n\nrecheck: on-release.\n"))
        case("last-recheck-is-operative", ["--revision", late], PASS, set(),
             want_counts={"finding_count": 0})
        # 15. binding refusals: non-hex, unlanded, CLI shape.
        sandbox_git(repo, "checkout", "-q", "-B", "side", clean)
        side = sandbox_commit(repo, note(header(source="side branch note, 2026-10-23.")))
        sandbox_git(repo, "checkout", "-q", "master")
        case("revision-symbolic-rejected", ["--revision", "HEAD"], CANNOT,
             {"E-REVISION-INVALID"})
        case("revision-unlanded", ["--revision", side], CANNOT,
             {"E-REVISION-NOT-LANDED"})
        case("branch-missing", ["--revision", clean, "--branch", "absent"], CANNOT,
             {"E-BRANCH-MISSING"})
        case("branch-invalid", ["--revision", clean, "--branch", "HEAD"], CANNOT,
             {"E-BRANCH-INVALID"})
        case("cli-no-mode", [], CANNOT, {"E-CLI"})
        case("cli-both-modes", ["--selftest", "--revision", clean], CANNOT, {"E-CLI"})
        case("cli-bogus-flag", ["--revision", clean, "--bogus"], CANNOT, {"E-CLI"})
        case("cli-branch-without-value", ["--revision", clean, "--branch"], CANNOT,
             {"E-CLI"})
    except Exception as exc:
        failures.append(f"sandbox: {exc!r}")
    finally:
        import shutil
        shutil.rmtree(repo, ignore_errors=True)
    passed = total - len(failures)
    print(json.dumps({"selftest": {"status": "PASS" if not failures else "FAIL",
                                   "cases": total, "passed": passed,
                                   "failures": failures}}, sort_keys=True), file=out)
    return PASS if not failures else FAIL


def main(argv=None):
    return run(sys.argv[1:] if argv is None else argv)


if __name__ == "__main__":
    sys.exit(main())
