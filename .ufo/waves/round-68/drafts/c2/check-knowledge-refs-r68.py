#!/usr/bin/env python3
"""Knowledge source-reference gate (QUALITY 98; round 68).

Round 66 routed a gap: `tools/check-knowledge-header.py` proves a note carries a
`source:` line, but it never checks that the S-ids on that line name rows of
`corpus/SOURCES.md`. A note citing `source: S999` passes the header gate while
the citation resolves to nothing. This gate closes that gap and reports, per note
and per id:

  KNOWLEDGE-REF-DANGLING  an id on the operative `source:` line is absent from
                          `corpus/SOURCES.md` at the bound revision.

Scope is every `*.md` under `corpus/knowledge/` at an immutable revision. A note
with no `source:` line emits no finding here — a missing header is the header
gate's job, not this gate's.

The operative line is the LAST column-0 `source:` line outside a fenced code
block, the same rule `check-knowledge-header.py` applies to its keys: an example
inside ``` or ~~~ fences, an indented line, or a `source:` word mid-sentence is
not a header, and later lines supersede earlier pointer lines. Ids are
`\\bS\\d{3,}\\b` on that one line, so a body sentence that mentions `S999` is
prose, while a four-digit `S0001` is an id like any other.

The registry's id set is the first cell of every `corpus/SOURCES.md` row whose
cell is exactly `S` followed by three or more digits (`^\\| S\\d{3,} \\|`,
surrounding spaces tolerated); a cell such as `S138 extra` does not register
`S138`. A registry with no id row at the revision is CANNOT_EVALUATE, never a
vacuous pass.

`--revision` is bound by the shared `tools/_revision.py` (QUALITY 27: 7-64 hex,
landed on `--branch`, pushed when that branch has an origin ref; one finding,
exit 2). `--lane` selects the repository; the default is the nearest ancestor of
this file that holds `tools/_revision.py`, so both the landed `tools/` copy and
a seat-directory copy work without a cwd. Read-only: git plumbing reads only,
nothing is written (`sys.dont_write_bytecode` keeps the shared import from
dropping a `__pycache__` into the lane).

Exit 0 pass / 1 finding / 2 could-not-evaluate; JSON on stdout.
`--selftest` runs a hermetic fixture repository (a registered set, the round-66
`S999` red, a second dangling id, fenced and mid-line examples, an unsourced
note, a four-digit id, a spaced registry cell, the last-source-wins convention,
a non-exact registry cell, plus CLI/binding refusals).
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # the shared-module import stays read-only

import argparse
import json
import re
import subprocess
import tempfile
from collections import namedtuple
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
SCOPE = "corpus/knowledge"
REGISTRY = "corpus/SOURCES.md"
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
ID = re.compile(r"\bS\d{3,}\b")
ROW = re.compile(r"^\|\s*(S\d{3,})\s*\|")
DANGLING = "KNOWLEDGE-REF-DANGLING"

Finding = namedtuple("Finding", "id site detail ref", defaults=(None,))
Note = namedtuple("Note", "path source_line refs dangling")


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


def registry_ids_at(repo, sha):
    """The id cell of every `corpus/SOURCES.md` row whose cell is exactly S<digits>."""
    raw = read_blob(repo, sha, REGISTRY)
    if raw is None:
        raise Cannot("E-PATH-MISSING", REGISTRY, "file absent at revision")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Cannot("E-PATH-INVALID", REGISTRY, f"not UTF-8: {exc}"[:120])
    ids = set()
    for raw_line in text.split("\n"):
        line = raw_line[:-1] if raw_line.endswith("\r") else raw_line
        match = ROW.match(line)
        if match:
            ids.add(match.group(1))
    if not ids:
        raise Cannot("E-PATH-MISSING", REGISTRY,
                     "no row whose id cell is S<digits> at revision")
    return ids


# --- the rule ---------------------------------------------------------------------------------
def source_line(text):
    """`(line_number, value)` of the LAST column-0 `source:` line outside fences."""
    fence, hits = None, []
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
        if line.startswith("source:"):
            hits.append((number, line[len("source:"):].strip()))
    return hits[-1] if hits else None


def evaluate(files, ids):
    findings, notes = [], []
    for path, text in files:
        hit = source_line(text)
        if hit is None:
            notes.append(Note(path, None, [], []))
            continue
        number, value = hit
        refs = sorted(set(ID.findall(value)))
        dangling = [ref for ref in refs if ref not in ids]
        for ref in dangling:
            findings.append(Finding(
                DANGLING, path,
                f"source: line {number} cites {ref}, absent from {REGISTRY} at the revision",
                ref))
        notes.append(Note(path, number, refs, dangling))
    findings = [Finding(*key) for key in sorted({tuple(item) for item in findings},
                                                key=lambda key: (key[0], key[1], key[2],
                                                                 key[3] or ""))]
    return findings, notes


# --- CLI --------------------------------------------------------------------------------------
def emit(status, revision, branch, branch_tip, origin_tip, findings, notes, out=None,
         message=None, registry_count=0):
    payload = {
        "status": status,
        "revision": revision,
        "branch": branch,
        "branch_tip": branch_tip,
        "origin_tip": origin_tip,
        "note_count": len(notes),
        "sourced_count": sum(1 for note in notes if note.source_line is not None),
        "ref_count": sum(len(note.refs) for note in notes),
        "dangling_count": sum(len(note.dangling) for note in notes),
        "registry": REGISTRY,
        "registry_id_count": registry_count,
        "finding_count": len(findings),
        "scope": (f"every *.md under {SCOPE}/ at the bound revision; the operative (last, "
                  "column-0, unfenced) source: line per note; ids \\bS\\d{3,}\\b on that "
                  f"line only; registry {REGISTRY} rows whose id cell is exactly S followed "
                  "by digits; read-only, no host action taken"),
        "findings": [{"id": item.id, "site": item.site, "detail": item.detail,
                      **({"ref": item.ref} if item.ref else {})} for item in findings],
        "notes": [{"path": note.path, "source_line": note.source_line,
                   "refs": note.refs, "dangling": note.dangling} for note in notes],
    }
    if message:
        payload["message"] = message
    print(json.dumps(payload, sort_keys=True), file=out or sys.stdout)
    return {"PASS": PASS, "FAIL": FAIL, "CANNOT_EVALUATE": CANNOT}[status]


def build_parser():
    parser = argparse.ArgumentParser(
        description="Read-only knowledge source-reference gate (QUALITY 98).",
        exit_on_error=False)
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
    registry_count = 0
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
        ids = registry_ids_at(repo, sha)
        registry_count = len(ids)
        findings, notes = evaluate(files, ids)
    except Cannot as exc:
        return emit("CANNOT_EVALUATE", sha or args.revision or "worktree", branch, tip,
                    origin_tip, [Finding(exc.fid, exc.site, exc.detail)], [], out,
                    registry_count=registry_count)
    except (_revision.RevisionError, subprocess.TimeoutExpired, OSError) as exc:
        return emit("CANNOT_EVALUATE", sha or args.revision or "worktree", branch, tip,
                    origin_tip, [Finding("E-GIT-FAILED", "git", str(exc)[:120])], [], out,
                    registry_count=registry_count)
    except Exception as exc:  # unreadable input is CANNOT, never a traceback
        return emit("CANNOT_EVALUATE", sha or args.revision or "worktree", branch, tip,
                    origin_tip, [Finding("E-INTERNAL", "gate", str(exc)[:120])], [], out,
                    registry_count=registry_count)
    return emit("PASS" if not findings else "FAIL", sha, branch, tip, origin_tip,
                findings, notes, out, registry_count=registry_count)


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


def head(source, verified="2026-10-23",
         recheck="30d; procedure: rerun the fixture probe."):
    return (f"# Fixture note\n\nsource: {source}\nverified-at: {verified}\n"
            f"recheck: {recheck}\n\nBody prose.\n")


def registry(*ids):
    return ("# Fixture source registry\n\n"
            "| id | source | kind | grade | claim | bound | summary | state | checked |"
            " recheck | notes |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|\n"
            + "".join(f"| {i} | fixture row {i} | docs | A | unpinned | fixture |"
                      f" fixture | mined | 2026-10-23 | 30d | — |\n" for i in ids))


def selftest(out=None):
    out = out or sys.stdout
    failures, total = [], 0

    def case(name, argv, want_code, want_ids, want_refs=None, want_counts=None):
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
        if want_refs is not None:
            got_refs = {item["ref"] for item in findings if item.get("ref")}
            if got_refs != set(want_refs):
                problems.append("refs=" + ",".join(sorted(got_refs))
                                + " want=" + ",".join(sorted(want_refs)))
        for key, value in (want_counts or {}).items():
            if payload.get(key) != value:
                problems.append(f"{key}={payload.get(key)}/{value}")
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))

    repo = Path(tempfile.mkdtemp(prefix="knowledge-refs-gate-"))
    try:
        sandbox_git(repo, "-c", "init.defaultBranch=master", "init", "-q")
        sandbox_git(repo, "config", "user.email", "fixture@example.invalid")
        sandbox_git(repo, "config", "user.name", "Fixture")
        sandbox_git(repo, "config", "commit.gpgsign", "false")
        sandbox_git(repo, "config", "core.hooksPath", "/dev/null")
        sandbox_git(repo, "commit", "-q", "--allow-empty", "-m", "base")
        base = sandbox_git(repo, "rev-parse", "HEAD").strip()

        def fresh(tree):
            sandbox_git(repo, "reset", "-q", "--hard", base)
            sandbox_git(repo, "clean", "-qfd")
            return sandbox_commit(repo, tree)

        ids = ("S138", "S149", "S182", "S185")
        # (a) every id on the operative line is a registry row.
        clean = fresh({REGISTRY: registry(*ids),
                       f"{SCOPE}/clean-r68.md":
                       head("S138 S149 (rows in `corpus/SOURCES.md`)")})
        case("all-ids-registered", ["--revision", clean], PASS, set(),
             want_counts={"note_count": 1, "sourced_count": 1, "ref_count": 2,
                          "dangling_count": 0, "finding_count": 0,
                          "registry_id_count": 4})
        # (b) the round-66 gap: source: S999 passes the header gate, dangles here.
        dangling = fresh({REGISTRY: registry(*ids),
                          f"{SCOPE}/dangling-r68.md":
                          head("S999 — fixture (never a registry row)")})
        case("unregistered-id", ["--revision", dangling], FAIL, {DANGLING},
             want_refs={"S999"}, want_counts={"finding_count": 1, "dangling_count": 1})
        # (c) two dangling ids on one line are two findings, not one.
        second = fresh({REGISTRY: registry("S138"),
                        f"{SCOPE}/second-r68.md": head("S138, S998 and S997")})
        case("second-dangling-id", ["--revision", second], FAIL, {DANGLING},
             want_refs={"S997", "S998"}, want_counts={"finding_count": 2, "dangling_count": 2,
                                          "ref_count": 3})
        # (d) an id inside a fenced example is not the operative line.
        fenced = fresh({REGISTRY: registry("S138"),
                        f"{SCOPE}/fenced-r68.md": head("S138")
                        + "\n```text\nsource: S999 — example only\n```\n"})
        case("fenced-id-is-example", ["--revision", fenced], PASS, set(),
             want_counts={"finding_count": 0, "ref_count": 1})
        # (e) an id mid-sentence in the body is prose, not a citation.
        midline = fresh({REGISTRY: registry("S138"),
                         f"{SCOPE}/midline-r68.md": head("S138")
                         + "\nThe crib said S999, but no source: line carries it.\n"})
        case("mid-line-id-is-prose", ["--revision", midline], PASS, set(),
             want_counts={"finding_count": 0})
        # (f) a note with no source: line is the header gate's finding, not this one.
        unsourced = fresh({REGISTRY: registry("S138"),
                           f"{SCOPE}/unsourced-r68.md":
                           "# Fixture note\n\nverified-at: 2026-10-23\nrecheck: 30d.\n\n"
                           "Cited S999 in prose only.\n"})
        case("no-source-line-no-finding", ["--revision", unsourced], PASS, set(),
             want_counts={"finding_count": 0, "sourced_count": 0, "ref_count": 0})
        # (g) S\d{3,} includes four digits; S0001 is not S001.
        four = fresh({REGISTRY: registry("S001"),
                      f"{SCOPE}/four-digit-r68.md": head("S0001 — four digit id")})
        case("four-digit-id-counts", ["--revision", four], FAIL, {DANGLING},
             want_refs={"S0001"}, want_counts={"finding_count": 1})
        # (h) a registry cell with padding still registers its id.
        spaced = fresh({REGISTRY: "# Fixture registry\n\n|   S185   | fixture row |\n",
                        f"{SCOPE}/spaced-r68.md": head("S185")})
        case("spaced-registry-cell", ["--revision", spaced], PASS, set(),
             want_counts={"finding_count": 0, "registry_id_count": 1})
        # (i) the last source: line supersedes an earlier pointer line.
        superseded = fresh({REGISTRY: registry("S138"),
                            f"{SCOPE}/superseded-r68.md": head("S999 — superseded")
                            + "\n## Appended\n\nsource: S138\n"})
        case("last-source-line-operative", ["--revision", superseded], PASS, set(),
             want_counts={"finding_count": 0, "sourced_count": 1})
        # (j) the id cell must be exactly the id; S138 extra registers nothing.
        loose = fresh({REGISTRY: "# Fixture registry\n\n| S149 | fixture row |\n"
                                  "| S138 extra | fixture row |\n",
                       f"{SCOPE}/loose-r68.md": head("S138")})
        case("registry-cell-must-be-exact", ["--revision", loose], FAIL, {DANGLING},
             want_refs={"S138"}, want_counts={"finding_count": 1, "registry_id_count": 1})
        # (k) a registry absent at the revision is unreadable input, never a pass.
        no_registry = fresh({f"{SCOPE}/clean-r68.md": head("S138")})
        case("registry-absent", ["--revision", no_registry], CANNOT, {"E-PATH-MISSING"},
             want_counts={"finding_count": 1})
        # binding and CLI refusals.
        clean_tip = fresh({REGISTRY: registry(*ids),
                           f"{SCOPE}/clean-r68.md": head("S138")})
        sandbox_git(repo, "checkout", "-q", "-B", "side", base)
        side = sandbox_commit(repo, {f"{SCOPE}/side-r68.md": head("S138")})
        sandbox_git(repo, "checkout", "-q", "master")
        case("revision-symbolic-rejected", ["--revision", "HEAD"], CANNOT,
             {"E-REVISION-INVALID"})
        case("revision-unlanded", ["--revision", side], CANNOT, {"E-REVISION-NOT-LANDED"})
        case("branch-missing", ["--revision", clean_tip, "--branch", "absent"], CANNOT,
             {"E-BRANCH-MISSING"})
        case("branch-invalid", ["--revision", clean_tip, "--branch", "HEAD"], CANNOT,
             {"E-BRANCH-INVALID"})
        case("cli-no-mode", [], CANNOT, {"E-CLI"})
        case("cli-both-modes", ["--selftest", "--revision", clean_tip], CANNOT, {"E-CLI"})
        case("cli-bogus-flag", ["--revision", clean_tip, "--bogus"], CANNOT, {"E-CLI"})
        case("cli-branch-without-value", ["--revision", clean_tip, "--branch"], CANNOT,
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
