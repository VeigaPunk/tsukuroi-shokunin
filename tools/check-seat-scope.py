#!/usr/bin/env python3
"""Narrow, read-only seat execution-scope gate (QUALITY24 / R16-SEAT-SCOPE).

Turns the round-16 lesson into a machine-checkable red: every seat of a
wave must close its report with a truthful `Scope: executed=...` trailer,
and a non-`none` value is only valid when that seat's dispatched spec
prompt carries the `EXEC-AUTHORIZED` marker. Input is one lane-relative
wave directory holding `swarm-registry.json` and/or `spec.json` plus the
seat reports `<Name>.md`; seat names and roles come from those two files
(registry members union spec items, spec role wins).

Findings: SCOPE-REPORT-MISSING (seat without a report), SCOPE-UNDECLARED
(report with no `^Scope: executed=(.+)$` line; the last matching line
wins), SCOPE-EXEC-UNAUTHORIZED (last declared value is not `none` and the
seat prompt lacks EXEC-AUTHORIZED). A wave with no seats is not a pass.

`--revision <hex>` reads immutable git objects only and binds through
`tools/_revision.py`: Git-valid branch names are checked before revision syntax;
the revision must be 7-64 hex and resolve to a commit. That commit must be an
ancestor of refs/heads/<branch> (default master) and, when
refs/remotes/origin/<branch> exists, also of it. Binding failures report one
typed id (E-BRANCH-INVALID, E-REVISION-INVALID, E-BRANCH-MISSING,
E-REVISION-NOT-LANDED, E-REVISION-NOT-PUSHED, or E-GIT-FAILED).
`--worktree` reads the same files from disk. `--selftest` is hermetic:
in-memory fixtures plus one mktemp git sandbox, never this repository.
Exit 0 clean, 1 findings, 2 could-not-evaluate. No writes, no network, no
host queries.
"""
from __future__ import annotations
import argparse, contextlib, io, json, os, re, shutil, subprocess, sys, tempfile
from collections import namedtuple
from pathlib import Path
sys.dont_write_bytecode = True  # read-only shared-module import
from _revision import RevisionError, bind as bind_revision

PASS, FAIL, CANNOT = 0, 1, 2
ROOT = Path(__file__).resolve().parents[1]
REGISTRY, SPEC = "swarm-registry.json", "spec.json"
EXEC_MARK = "EXEC-AUTHORIZED"
IDS = ("SCOPE-EXEC-UNAUTHORIZED", "SCOPE-REPORT-MISSING", "SCOPE-UNDECLARED")
SCOPE = re.compile(r"^Scope: executed=(.+)$", re.M)
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
WAVE = re.compile(r"^[A-Za-z0-9._-][A-Za-z0-9._/-]*$")
Finding = namedtuple("Finding", "id site role detail")
Seat = namedtuple("Seat", "role prompt")
Result = namedtuple("Result", "code findings seats")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def scope_value(text):
    """Last `Scope: executed=...` line value, or None when no line matches."""
    hits = SCOPE.findall(text)
    return hits[-1].strip() if hits else None


def evaluate(seats, reports):
    """Per-seat verdicts over already-loaded seats and report texts."""
    findings = []
    for name in sorted(seats):
        seat = seats[name]
        site = f"{name}.md"
        text = reports.get(name)
        if text is None:
            findings.append(Finding("SCOPE-REPORT-MISSING", site, seat.role,
                                    "seat report absent"))
            continue
        executed = scope_value(text)
        if executed is None:
            findings.append(Finding("SCOPE-UNDECLARED", site, seat.role,
                                    "no Scope: executed=... line in report"))
            continue
        if executed != "none" and EXEC_MARK not in seat.prompt:
            findings.append(Finding(
                "SCOPE-EXEC-UNAUTHORIZED", site, seat.role,
                f"declared executed={executed[:60]} without EXEC-AUTHORIZED in the seat prompt"))
    findings.sort(key=lambda f: (f.id, f.site))
    return Result(FAIL if findings else PASS, findings, len(seats))


def parse_json(text, fid, site):
    try:
        return json.loads(text)
    except (TypeError, ValueError) as exc:
        raise Cannot(fid, site, f"malformed JSON: {str(exc)[:100]}")


def load_seats(reg_text, spec_text):
    """Registry members union spec items; roles and prompts merged by name."""
    if reg_text is None and spec_text is None:
        raise Cannot("E-SEAT-SOURCE-MISSING", "seats",
                     "neither swarm-registry.json nor spec.json")
    seats = {}
    if spec_text is not None:
        spec = parse_json(spec_text, "E-SPEC-PARSE", SPEC)
        if not isinstance(spec, dict):
            raise Cannot("E-SPEC-SHAPE", SPEC, "top level is not an object")
        items = spec.get("items", [])
        if not isinstance(items, list):
            raise Cannot("E-SPEC-SHAPE", SPEC, "items is not a list")
        for item in items:
            if not isinstance(item, dict):
                raise Cannot("E-SPEC-SHAPE", SPEC, "item is not an object")
            name = item.get("name")
            if not isinstance(name, str) or not NAME.fullmatch(name):
                raise Cannot("E-SEAT-NAME", SPEC, "item name is not a safe report stem")
            role = item.get("role") if isinstance(item.get("role"), str) else None
            prompt = item.get("prompt") if isinstance(item.get("prompt"), str) else ""
            seats[name] = Seat(role, prompt)
    if reg_text is not None:
        reg = parse_json(reg_text, "E-REGISTRY-PARSE", REGISTRY)
        if not isinstance(reg, dict):
            raise Cannot("E-REGISTRY-SHAPE", REGISTRY, "top level is not an object")
        members = reg.get("members", {})
        if not isinstance(members, dict):
            raise Cannot("E-REGISTRY-SHAPE", REGISTRY, "members is not an object")
        for name, member in members.items():
            if not isinstance(name, str) or not NAME.fullmatch(name):
                raise Cannot("E-SEAT-NAME", REGISTRY, "member name is not a safe report stem")
            role = member.get("role") if isinstance(member, dict) else None
            role = role if isinstance(role, str) else None
            if name in seats:
                if seats[name].role is None and role is not None:
                    seats[name] = seats[name]._replace(role=role)
            else:
                seats[name] = Seat(role, "")
    if not seats:
        raise Cannot("E-NO-SEATS", "seats", "no seats in registry or spec")
    return seats


def analyse(reg_text, spec_text, reports):
    return evaluate(load_seats(reg_text, spec_text), reports)


def emit(result, revision, branch, branch_tip, wave):
    status = {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[result.code]
    counts = {fid: 0 for fid in IDS}
    for finding in result.findings:
        counts[finding.id] = counts.get(finding.id, 0) + 1
    payload = {
        "status": status,
        "revision": revision,
        "branch": branch,
        "branch_tip": branch_tip,
        "wave": wave,
        "seat_count": result.seats,
        "counts": counts,
        "findings": [{"id": f.id, "site": f.site, "role": f.role, "detail": f.detail}
                     for f in result.findings],
        "scope": "seat execution-scope declarations only; not a host, build or test verdict",
    }
    print(json.dumps(payload, sort_keys=True))
    return result.code


def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C"})
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(root), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=env, timeout=30)
    except subprocess.TimeoutExpired:
        raise Cannot("E-GIT-TIMEOUT", "git", "git command exceeded 30s")
    except OSError as exc:
        raise Cannot("E-GIT-FAILED", "git", str(exc)[:120])


def wave_key(path):
    text = str(path).strip()
    if not text or text.startswith("/") or "\\" in text or not WAVE.fullmatch(text):
        raise Cannot("E-WAVE-INVALID", "wave", "lane-relative wave directory required")
    parts = [part for part in text.split("/") if part not in ("", ".")]
    if not parts or ".." in parts:
        raise Cannot("E-WAVE-INVALID", "wave", "lane-relative wave directory required")
    return "/".join(parts)


def read_git(root, commit, path):
    proc = git(root, "show", f"{commit}:{path}")
    if proc.returncode == 0:
        try:
            return proc.stdout.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Cannot("E-READ-FAILED", path, str(exc)[:120])
    error = proc.stderr.decode("utf-8", "replace")
    if re.search(r"does not exist|exists on disk, but not in|not in '|bad object", error, re.I):
        return None
    raise Cannot("E-GIT-READ-FAILED", path, error.strip()[:120])


def tree_paths(root, commit, wave):
    proc = git(root, "ls-tree", "-r", "--name-only", "-z", commit, "--", wave)
    if proc.returncode != 0:
        raise Cannot("E-GIT-READ-FAILED", wave,
                     proc.stderr.decode("utf-8", "replace").strip()[:120])
    return {p for p in proc.stdout.decode("utf-8", "replace").split("\0") if p}


def read_file(path):
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError) as exc:
        raise Cannot("E-READ-FAILED", path.name, str(exc)[:120])


def build_parser():
    parser = argparse.ArgumentParser(
        description="Narrow read-only seat execution-scope gate.",
        exit_on_error=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision", metavar="HEX",
                       help="7-64 hex commit; reads immutable git objects only")
    group.add_argument("--worktree", action="store_true", help="read wave files from disk")
    group.add_argument("--selftest", action="store_true", help="hermetic fixture suite")
    parser.add_argument("--wave", metavar="DIR", help="lane-relative wave directory")
    parser.add_argument("--branch", default="master", metavar="REF",
                        help="branch the revision must be landed on (default master)")
    return parser


def args_issue(args):
    """CLI policy shared by main() and the selftest seam."""
    if args.selftest:
        return "E-CLI" if args.wave is not None else None
    if args.wave is None:
        return "E-CLI"
    return None


def cli_issue(argv):
    try:
        args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit):
        return "E-CLI"
    return args_issue(args)


def collect(wave, revision, branch, root=ROOT):
    """(seats, reports, revision display, branch tip) for one wave."""
    if revision is not None:
        try:
            bound = bind_revision(root, revision, branch)
        except RevisionError as exc:
            raise Cannot(exc.fid, exc.site, exc.detail) from exc
        sha, tip = bound.sha, bound.branch_tip
        seats = load_seats(read_git(root, sha, f"{wave}/{REGISTRY}"),
                          read_git(root, sha, f"{wave}/{SPEC}"))
        listing = tree_paths(root, sha, wave)
        reports = {name: (read_git(root, sha, f"{wave}/{name}.md")
                          if f"{wave}/{name}.md" in listing else None)
                   for name in seats}
        return seats, reports, sha, tip
    base = root / wave
    if not base.is_dir():
        raise Cannot("E-WAVE-MISSING", wave, "wave directory absent")
    seats = load_seats(read_file(base / REGISTRY), read_file(base / SPEC))
    reports = {name: read_file(base / f"{name}.md") for name in seats}
    return seats, reports, "worktree", None


def sandbox():
    """Fresh mktemp repository with a landed tip, a side commit and a wave tree."""
    root = Path(tempfile.mkdtemp(prefix="seat-scope-"))
    try:
        def run(*args):
            proc = git(root, *args)
            if proc.returncode != 0:
                raise RuntimeError(proc.stderr.decode("utf-8", "replace").strip())
            return proc.stdout.decode("ascii", "replace").strip()

        run("init", "-q", ".")
        run("symbolic-ref", "HEAD", "refs/heads/master")
        run("config", "user.email", "seat-scope@example.invalid")
        run("config", "user.name", "seat scope selftest")
        run("commit", "-q", "--allow-empty", "-m", "base")
        base = run("rev-parse", "HEAD")
        wave = root / ".ufo/waves/demo"
        wave.mkdir(parents=True)
        (wave / REGISTRY).write_text(json.dumps(
            {"schema": "ufo-swarm-registry-v1",
             "members": {"Alpha": {"role": "executor"}, "Beta": {"role": "scout"}}}))
        (wave / SPEC).write_text(json.dumps({"items": [
            {"name": "Alpha", "role": "executor", "prompt": ""},
            {"name": "Beta", "role": "scout", "prompt": ""}]}))
        (wave / "Alpha.md").write_text("body\n\nScope: executed=none\n")
        run("add", "-A")
        run("commit", "-q", "-m", "wave-partial")
        partial = run("rev-parse", "HEAD")
        (wave / "Beta.md").write_text("body\n\nScope: executed=none\n")
        run("add", "-A")
        run("commit", "-q", "-m", "wave-clean")
        tip = run("rev-parse", "HEAD")
        run("checkout", "-q", "-b", "side", base)
        run("commit", "-q", "--allow-empty", "-m", "unlanded")
        side = run("rev-parse", "HEAD")
        run("checkout", "-q", "master")
        tools = root / "tools"
        tools.mkdir()
        shutil.copyfile(Path(__file__), tools / "check-seat-scope.py")
        shutil.copyfile(Path(__file__).with_name("_revision.py"), tools / "_revision.py")
        return root, base, tip, side, partial, tip
    except Exception:
        shutil.rmtree(root, ignore_errors=True)
        raise


def selftest():
    def sheet(*rows):
        return {name: Seat(role, prompt) for name, role, prompt in rows}

    plain = sheet(("Alpha", "executor", ""), ("Beta", "scout", ""))
    done = {"Alpha": "body\n\nScope: executed=none\n", "Beta": "Scope: executed=none"}
    cases = [
        ("clean", plain, done, PASS, set(), 2),
        ("undeclared", plain, {"Alpha": "body only\n", "Beta": done["Beta"]},
         FAIL, {"SCOPE-UNDECLARED"}, 2),
        ("exec-unauthorized", plain,
         {"Alpha": "Scope: executed=git log -1\n", "Beta": done["Beta"]},
         FAIL, {"SCOPE-EXEC-UNAUTHORIZED"}, 2),
        ("exec-authorized", sheet(("Alpha", "executor",
                                   "EXEC-AUTHORIZED: its --selftest only.")),
         {"Alpha": "Scope: executed=python3 gate.py --selftest\n"},
         PASS, set(), 1),
        ("report-missing", plain, {"Alpha": done["Alpha"]},
         FAIL, {"SCOPE-REPORT-MISSING"}, 2),
        ("last-line-clean", sheet(("Alpha", "executor", "")),
         {"Alpha": "Scope: executed=probe\nmid\nScope: executed=none\n"}, PASS, set(), 1),
        ("last-line-unauthorized", sheet(("Alpha", "executor", "")),
         {"Alpha": "Scope: executed=none\nmid\nScope: executed=probe\n"},
         FAIL, {"SCOPE-EXEC-UNAUTHORIZED"}, 1),
        ("empty-value", sheet(("Alpha", "executor", "")),
         {"Alpha": "Scope: executed=\n"}, FAIL, {"SCOPE-UNDECLARED"}, 1),
        ("indented-not-a-line", sheet(("Alpha", "executor", "")),
         {"Alpha": "  Scope: executed=none\n"}, FAIL, {"SCOPE-UNDECLARED"}, 1),
        ("none-with-prose", sheet(("Alpha", "executor", "")),
         {"Alpha": "Scope: executed=none (authorized)\n"},
         FAIL, {"SCOPE-EXEC-UNAUTHORIZED"}, 1),
        ("two-undeclared-count", plain, {"Alpha": "x\n", "Beta": "y\n"},
         FAIL, {"SCOPE-UNDECLARED"}, 2),
    ]
    passed, failures = 0, []
    for name, seats, reports, code, ids, seats_n in cases:
        result = evaluate(seats, reports)
        problems = []
        if result.code != code:
            problems.append(f"exit={result.code}/{code}")
        got = sorted({f.id for f in result.findings})
        if got != sorted(ids):
            problems.append("ids=" + ",".join(got) + " want=" + ",".join(sorted(ids)))
        if result.seats != seats_n:
            problems.append(f"seats={result.seats}/{seats_n}")
        if name == "two-undeclared-count" and len(result.findings) != 2:
            problems.append(f"findings={len(result.findings)}/2")
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))
        else:
            passed += 1

    reg = json.dumps({"schema": "ufo-swarm-registry-v1",
                      "members": {"Alpha": {"role": "critic"}}})
    spec = json.dumps({"items": [{"name": "Alpha", "role": "executor",
                                  "prompt": "read-only"},
                                 {"name": "Gamma", "role": "scout", "prompt": ""}]})
    sourced = [
        ("registry-only", reg, None, {"Alpha": "Scope: executed=none\n"}, PASS, set(), 1),
        ("registry-role-carried", reg, None,
         {"Alpha": "Scope: executed=probe\n"}, FAIL, {"SCOPE-EXEC-UNAUTHORIZED"}, 1),
        ("spec-only", None, spec,
         {"Alpha": "Scope: executed=none\n", "Gamma": "Scope: executed=none\n"},
         PASS, set(), 2),
        ("both-merged", reg, spec,
         {"Alpha": "Scope: executed=none\n"}, FAIL, {"SCOPE-REPORT-MISSING"}, 2),
    ]
    for name, reg_text, spec_text, reports, code, ids, seats_n in sourced:
        try:
            result = analyse(reg_text, spec_text, reports)
        except Cannot as exc:
            result = Result(CANNOT, [Finding(exc.fid, exc.site, None, exc.detail)], 0)
        problems = []
        if result.code != code:
            problems.append(f"exit={result.code}/{code}")
        got = sorted({f.id for f in result.findings})
        if got != sorted(ids):
            problems.append("ids=" + ",".join(got) + " want=" + ",".join(sorted(ids)))
        if result.seats != seats_n:
            problems.append(f"seats={result.seats}/{seats_n}")
        if name == "registry-role-carried" and result.findings:
            if result.findings[0].role != "critic":
                problems.append(f"role={result.findings[0].role}/critic")
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))
        else:
            passed += 1

    broken = [
        ("source-missing", None, None, {}, CANNOT, {"E-SEAT-SOURCE-MISSING"}, 0),
        ("registry-malformed", "{", None, {}, CANNOT, {"E-REGISTRY-PARSE"}, 0),
        ("spec-malformed", None, "[]x", {}, CANNOT, {"E-SPEC-PARSE"}, 0),
        ("spec-items-not-list", None, json.dumps({"items": {}}), {},
         CANNOT, {"E-SPEC-SHAPE"}, 0),
        ("no-seats", json.dumps({"members": {}}), None, {},
         CANNOT, {"E-NO-SEATS"}, 0),
        ("unsafe-seat-name", json.dumps({"members": {"../Escape": {"role": "x"}}}),
         None, {}, CANNOT, {"E-SEAT-NAME"}, 0),
    ]
    for name, reg_text, spec_text, reports, code, ids, seats_n in broken:
        try:
            result = analyse(reg_text, spec_text, reports)
        except Cannot as exc:
            result = Result(CANNOT, [Finding(exc.fid, exc.site, None, exc.detail)], 0)
        problems = []
        if result.code != code:
            problems.append(f"exit={result.code}/{code}")
        got = sorted({f.id for f in result.findings})
        if got != sorted(ids):
            problems.append("ids=" + ",".join(got) + " want=" + ",".join(sorted(ids)))
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))
        else:
            passed += 1

    pure = (("cli-empty", cli_issue([]), "E-CLI"),
            ("cli-revision-without-wave",
             cli_issue(["--revision", "f871697aa0a8ed180771e62d99e3b9559fd5efd1"]), "E-CLI"),
            ("cli-both-modes", cli_issue(["--selftest", "--worktree"]), "E-CLI"),
            ("cli-branch-validation-deferred",
             cli_issue(["--revision", "HEAD", "--wave", ".ufo/waves/demo",
                        "--branch", "a..b"]), None),
            ("cli-dash-branch", cli_issue(["--worktree", "--wave", ".ufo/waves/x",
                                           "--branch", "-bad"]), "E-CLI"))
    for name, got, want in pure:
        if got == want:
            passed += 1
        else:
            failures.append(f"{name}: id={got}/{want}")

    total = len(cases) + len(sourced) + len(broken) + len(pure)
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = emit(evaluate(sheet(("Alpha", "executor", "")),
                             {"Alpha": "Scope: executed=probe\n"}),
                    "abc1234", "master", "def5678", ".ufo/waves/demo")
    try:
        payload = json.loads(buffer.getvalue())
    except ValueError:
        payload = None
    problems = []
    if code != FAIL:
        problems.append(f"exit={code}/{FAIL}")
    if not isinstance(payload, dict):
        problems.append("payload is not JSON")
    else:
        if payload.get("status") != "FAIL":
            problems.append(f"status={payload.get('status')}/FAIL")
        if payload.get("counts") != {"SCOPE-EXEC-UNAUTHORIZED": 1,
                                     "SCOPE-REPORT-MISSING": 0,
                                     "SCOPE-UNDECLARED": 0}:
            problems.append(f"counts={payload.get('counts')}")
        if (payload.get("revision"), payload.get("branch"),
                payload.get("branch_tip")) != ("abc1234", "master", "def5678"):
            problems.append("binding fields not echoed")
        if payload.get("seat_count") != 1:
            problems.append(f"seat_count={payload.get('seat_count')}/1")
    if problems:
        failures.append("emit-shape: " + "; ".join(problems))
    else:
        passed += 1
    total += 1
    try:
        root, base, tip, side, partial, clean = sandbox()
    except Exception as exc:
        print("CHECK_SEAT_SCOPE_SELFTEST: FAIL (sandbox unavailable: "
              f"{str(exc)[:100]})")
        return FAIL
    try:
        def bind_case(name, rev, branch, want, want_sha=None):
            try:
                bound = bind_revision(root, rev, branch)
                got = None
            except RevisionError as exc:
                bound, got = None, exc.fid
            problems = []
            if got != want:
                problems.append(f"id={got}/{want}")
            if want is None and (bound.sha != want_sha or bound.branch_tip != tip):
                problems.append(f"sha={bound.sha}/{want_sha} tip={bound.branch_tip}/{tip}")
            if problems:
                failures.append(f"sandbox-{name}: " + "; ".join(problems))
                return False
            return True

        bound = [
            ("landed", tip, "master", None, tip),
            ("landed-base", base, "master", None, base),
            ("unlanded", side, "master", "E-REVISION-NOT-LANDED", None),
            ("unknown-hex", "0123456789abcdef0123456789abcdef01234567", "master",
             "E-REVISION-INVALID", None),
            ("invalid-branch-range", tip, "a..b", "E-BRANCH-INVALID", None),
            ("invalid-branch-slash", tip, "master/", "E-BRANCH-INVALID", None),
            ("invalid-branch-lock", tip, "master.lock", "E-BRANCH-INVALID", None),
            ("branch-before-revision", "HEAD", "a..b", "E-BRANCH-INVALID", None),
            ("revision-before-missing-branch", "HEAD", "release",
             "E-REVISION-INVALID", None),
            ("branch-missing", tip, "release", "E-BRANCH-MISSING", None),
            ("nested-branch-missing", tip, "feature/x", "E-BRANCH-MISSING", None),
        ]
        for name, rev, branch, want, want_sha in bound:
            passed += bind_case(name, rev, branch, want, want_sha)
        total += len(bound)

        def cli_case(name, rev, branch, want_id=None):
            nonlocal passed, total
            proc = subprocess.run(
                [sys.executable, str(root / "tools" / "check-seat-scope.py"),
                 "--revision", rev, "--wave", ".ufo/waves/demo",
                 "--branch", branch], cwd=root, stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
            try:
                payload = json.loads(proc.stdout.decode("utf-8"))
            except (UnicodeDecodeError, ValueError):
                payload = None
            problems = []
            want_code = PASS if want_id is None else CANNOT
            want_status = "PASS" if want_id is None else "CANNOT_EVALUATE"
            if proc.returncode != want_code:
                problems.append(f"exit={proc.returncode}/{want_code}")
            if not isinstance(payload, dict):
                problems.append("stdout is not JSON")
            else:
                if payload.get("status") != want_status:
                    problems.append(f"status={payload.get('status')}/{want_status}")
                findings = payload.get("findings")
                if want_id is None:
                    if findings != []:
                        problems.append(f"findings={findings!r}/[]")
                elif (not isinstance(findings, list) or len(findings) != 1
                      or not isinstance(findings[0], dict)
                      or findings[0].get("id") != want_id
                      or not isinstance(payload.get("counts"), dict)
                      or payload["counts"].get(want_id) != 1):
                    problems.append(f"findings={findings!r}/one {want_id}")
            if problems:
                failures.append(f"sandbox-{name}: " + "; ".join(problems))
            else:
                passed += 1
            total += 1

        cli_case("cli-clean", tip, "master")
        cli_case("cli-branch-first", "HEAD", "a..b", "E-BRANCH-INVALID")
        cli_case("cli-invalid-revision", "HEAD", "master", "E-REVISION-INVALID")
        cli_case("cli-revision-before-missing-branch", "HEAD", "release",
                 "E-REVISION-INVALID")
        cli_case("cli-invalid-hex", "abc123", "master", "E-REVISION-INVALID")
        cli_case("cli-branch-missing", tip, "release", "E-BRANCH-MISSING")
        cli_case("cli-unlanded-single-id", side, "master", "E-REVISION-NOT-LANDED")

        for name, rev, want, want_seats in (("wave-partial", partial,
                                             {"SCOPE-REPORT-MISSING"}, 2),
                                            ("wave-clean", clean, set(), 2)):
            try:
                seats, reports, got_rev, got_tip = collect(
                    ".ufo/waves/demo", rev, "master", root=root)
                result = evaluate(seats, reports)
                read = None if got_rev == rev and got_tip == tip else "binding"
            except Cannot as exc:
                read, result = exc.fid, None
            problems = []
            if read is not None:
                problems.append(f"read={read}")
            if result is not None:
                ids = sorted({f.id for f in result.findings})
                if ids != sorted(want) or result.seats != want_seats:
                    problems.append("ids=" + ",".join(ids) + " want="
                                    + ",".join(sorted(want))
                                    + f" seats={result.seats}/{want_seats}")
            if problems:
                failures.append(f"sandbox-{name}: " + "; ".join(problems))
            else:
                passed += 1
            total += 1

        if git(root, "update-ref", "refs/remotes/origin/master", base).returncode:
            failures.append("sandbox-origin: update-ref failed")
            total += 2
        else:
            passed += bind_case("not-pushed", tip, "master", "E-REVISION-NOT-PUSHED")
            passed += bind_case("pushed-base", base, "master", None, base)
            cli_case("cli-not-pushed", tip, "master", "E-REVISION-NOT-PUSHED")
            total += 2

        for name, spec_in in (("wave-absolute", "/etc"),
                              ("wave-traversal", ".ufo/../../etc")):
            try:
                wave_key(spec_in)
                got = None
            except Cannot as exc:
                got = exc.fid
            if got == "E-WAVE-INVALID":
                passed += 1
            else:
                failures.append(f"{name}: id={got}/E-WAVE-INVALID")
            total += 1
    finally:
        shutil.rmtree(root, ignore_errors=True)

    if failures:
        print(f"CHECK_SEAT_SCOPE_SELFTEST: FAIL ({total} cases, {passed} passed)")
        print("\n".join("  " + item for item in failures))
        return FAIL
    print(f"CHECK_SEAT_SCOPE_SELFTEST: PASS ({total} cases, {passed} passed, 0 failed)")
    return PASS


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit) as exc:
        if isinstance(exc, SystemExit) and not exc.code:
            return 0
        return emit(Result(CANNOT, [Finding("E-CLI", "cli", None,
                                            "--revision/--worktree/--selftest with --wave")],
                           0), "worktree", "master", None, None)
    if args.selftest:
        return selftest()
    revision_in, branch, wave_arg = args.revision, args.branch, args.wave
    revision, wave, tip = "worktree", None, None
    try:
        issue = args_issue(args)
        if issue:
            raise Cannot(issue, "cli" if issue == "E-CLI" else "branch",
                         "invalid command line")
        wave = wave_key(wave_arg)
        if revision_in is not None:
            revision = revision_in
        seats, reports, revision, tip = collect(wave, revision_in, branch)
        result = evaluate(seats, reports)
    except Cannot as exc:
        return emit(Result(CANNOT, [Finding(exc.fid, exc.site, None, exc.detail)], 0),
                    revision, branch, tip, wave if wave is not None else wave_arg)
    except Exception as exc:  # exit 1 on a traceback would misstate the verdict
        return emit(Result(CANNOT, [Finding("E-INTERNAL", "gate", None, str(exc)[:120])],
                           0), revision, branch, tip, wave)
    return emit(result, revision, branch, tip, wave)


if __name__ == "__main__":
    sys.exit(main())
