#!/usr/bin/env python
"""win-host-census-r53 — read-only Windows-host state census for tsukuroi-shokunin (round 53).

The lane's first gate for the Windows host (round 53 FRESH-START): the historical
census `tools/tsukuroi-census.sh` probes Arch Linux surfaces (pacman, systemd,
journalctl, btrfs) that do not exist here, and its hermetic selftest does not
complete on this host (40 of 168 cases in 90 s and in 420 s, rc 124). This gate
reads four planes of the current host, read-only, and never writes outside its
process (selftest is pure in-process, no subprocess, no temp tree):

  tools  - declared tool set resolution: required host tools vs Linux-only tools
           (absent Linux tools are the expected state on this host, not a finding)
  path   - PATH health of the view this process sees (os.environ["PATH"],
           os.pathsep-separated): total entries, empty entries, duplicate values,
           entries whose directory does not exist
  python - interpreter identity: `python` must resolve and run; `python3` that
           resolves into a WindowsApps alias directory is the Store stub (rc 49
           when run), reported `stub`, never executed
  git    - git and gh presence and versions, lane commit identity configured

Output grammar (QUALITY 84): only validated tokens are echoed. Host-derived
strings (paths, versions) are classified, counted or regex-validated before they
reach a line; a value that fails its pattern is reported `unreadable`, never
echoed raw. Plane lines, then the rollup:

  PLANE tools  GREEN|DEGRADED|BLOCKED required=N/M linux_absent=N stub=N detail=...
  PLANE path   GREEN|DEGRADED|BLOCKED entries=N missing=N dup_values=N empty=N
  PLANE python GREEN|DEGRADED|BLOCKED python=present|absent|stub python3=...
  PLANE git    GREEN|DEGRADED|BLOCKED git=... gh=... identity=... repo=...
  WIN_CENSUS: HEALTHY|DEGRADED|BLOCKED (tools=... path=... python=... git=...)

Exit map: 0 all planes GREEN; 1 at least one DEGRADED and none BLOCKED;
2 at least one BLOCKED (could-not-evaluate). This is a probe result, not
operator clearance: detection and report only, every repair stays operator-owned.

`--selftest` is hermetic and injects fake resolvers/runners, so it proves the
logic, not the host state; the live run is the host-state reading. Both are
required before the round's C1 claim verifies (SCORECARD "Round 53 —
declaration"). Run with `python` (the real interpreter); `python3` on this host
is the Store stub (rc 49) — that finding is what the python plane reports.
"""
import os
import re
import shutil
import subprocess
import sys

REQUIRED_TOOLS = ["git", "gh", "node", "python", "bash"]
LINUX_ONLY_TOOLS = ["pacman", "systemctl", "journalctl", "btrfs", "nvidia-smi", "jq"]
PROBED_TOOLS = REQUIRED_TOOLS + LINUX_ONLY_TOOLS + ["python3"]
STUB_MARKER = "windowsapps"  # App-execution-alias install root (Store stub class)
VERSION_RE = re.compile(r"^[0-9A-Za-z][0-9A-Za-z ._+:-]{0,48}$")
PLANE_RE = re.compile(r"^PLANE [a-z]+ (GREEN|DEGRADED|BLOCKED) [a-z0-9_]+=[0-9A-Za-z./+=-]+")
EXIT_CLEAN, EXIT_DEGRADED, EXIT_BLOCKED = 0, 1, 2

GREEN, DEGRADED, BLOCKED = "GREEN", "DEGRADED", "BLOCKED"
ORDER = {GREEN: 0, DEGRADED: 1, BLOCKED: 2}


def classify_path_entries(entries, exists):
    """Count PATH health facts. Values are counted, never returned for echoing."""
    seen = {}
    empty = missing = 0
    for i, entry in enumerate(entries):
        if entry == "":
            empty += 1
            continue
        seen.setdefault(entry, []).append(i)
        try:
            ok = exists(entry)
        except OSError:
            ok = False
        if not ok:
            missing += 1
    dup_positions = sorted(i for positions in seen.values() if len(positions) > 1 for i in positions)
    return {
        "total": len(entries),
        "empty": empty,
        "missing": missing,
        "dup_values": sum(1 for p in seen.values() if len(p) > 1),
        "dup_positions": dup_positions,
    }


def path_plane(path_value, exists=os.path.isdir, pathsep=None):
    pathsep = pathsep or os.pathsep
    facts = classify_path_entries(path_value.split(pathsep), exists)
    verdict = GREEN if (facts["empty"] == 0 and facts["missing"] == 0 and facts["dup_values"] == 0) else DEGRADED
    line = "PLANE path %s entries=%d missing=%d dup_values=%d empty=%d" % (
        verdict, facts["total"], facts["missing"], facts["dup_values"], facts["empty"])
    return verdict, line, facts


def classify_tool(name, resolver):
    """-> (state in present|absent|stub, raw path or None). The raw path is
    classified, never echoed: only its state reaches the grammar."""
    found = resolver(name)
    if not found:
        return "absent", None
    normed = str(found).replace("\\", "/").replace("//", "/").lower()
    if STUB_MARKER in normed:
        return "stub", found
    return "present", found


def tools_plane(resolver):
    states = {t: classify_tool(t, resolver)[0] for t in PROBED_TOOLS}
    required_present = sum(1 for t in REQUIRED_TOOLS if states[t] == "present")
    linux_absent = sum(1 for t in LINUX_ONLY_TOOLS if states[t] == "absent")
    stubs = sorted(t for t in PROBED_TOOLS if states[t] == "stub")
    missing_required = [t for t in REQUIRED_TOOLS if states[t] != "present"]
    if missing_required:
        verdict = BLOCKED if "git" in missing_required else DEGRADED
    elif stubs:
        verdict = DEGRADED
    else:
        verdict = GREEN
    line = "PLANE tools %s required=%d/%d linux_absent=%d stub=%d" % (
        verdict, required_present, len(REQUIRED_TOOLS), linux_absent, len(stubs))
    return verdict, line, {"stubs": stubs, "required_missing": missing_required}


def run_first_line(cmd, runner):
    """Run a version command read-only; return a validated version token.

    `git --version` -> `git version 2.55.0.windows.3` -> `2.55.0.windows.3`;
    `gh --version` first line carries a trailing `(date)` token, so the scan
    takes the last token that matches VERSION_RE, never an unmatched one."""
    try:
        proc = runner(cmd)
    except (OSError, subprocess.SubprocessError):
        return "absent"
    if proc.returncode != 0:
        return "unreadable"
    first = (proc.stdout or "").splitlines()
    line = first[0].strip() if first else ""
    for token in reversed(line.split()):
        if VERSION_RE.match(token):
            return token
    return "unreadable"


def git_plane(runner, repo_ok, config_reader):
    git_v = run_first_line(["git", "--version"], runner)
    gh_v = run_first_line(["gh", "--version"], runner)
    git_state = BLOCKED if git_v == "absent" else (DEGRADED if git_v == "unreadable" else GREEN)
    gh_state = GREEN if gh_v not in ("absent", "unreadable") else DEGRADED
    try:
        identity = "set" if config_reader("user.name") and config_reader("user.email") else "unset"
    except Exception:
        identity = "unset"
    repo_state = "yes" if repo_ok else "no"
    verdict = max(
        [git_state, gh_state] + ([DEGRADED] if identity == "unset" or not repo_ok else []),
        key=lambda v: ORDER[v])
    line = "PLANE git %s git=%s gh=%s identity=%s repo=%s" % (verdict, git_v, gh_v, identity, repo_state)
    return verdict, line, {}


def python_plane(runner, resolver):
    py_state, _ = classify_tool("python", resolver)
    py3_state, _ = classify_tool("python3", resolver)
    runs = "no"
    if py_state == "present":
        try:
            proc = runner(["python", "-c", "import sys"])
            runs = "yes" if proc.returncode == 0 else "no"
        except (OSError, subprocess.SubprocessError):
            runs = "no"
    if py_state != "present" or runs == "no":
        verdict = BLOCKED
    elif py3_state == "stub":
        verdict = DEGRADED
    else:
        verdict = GREEN
    line = "PLANE python %s python=%s runs=%s python3=%s" % (verdict, py_state, runs, py3_state)
    return verdict, line, {}


def rollup(planes):
    worst = max((ORDER[p] for p in planes.values()), default=ORDER[BLOCKED])
    verdict = {v: k for k, v in ORDER.items()}[worst]
    body = " ".join("%s=%s" % (name, state) for name, state in sorted(planes.items()))
    return verdict, "WIN_CENSUS: %s (%s)" % (verdict, body)


def live_census(repo_dir, out):
    """Read the real host. Read-only: version probes, which(), isdir only."""
    def runner(cmd):
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    def config_reader(key):
        proc = subprocess.run(["git", "config", "--get", key], capture_output=True,
                              text=True, timeout=30, cwd=repo_dir)
        return proc.stdout.strip() if proc.returncode == 0 else ""

    resolver = shutil.which
    planes = {}
    lines = []
    verdict, line, _ = tools_plane(resolver)
    planes["tools"] = verdict
    lines.append(line)
    verdict, line, _ = path_plane(os.environ.get("PATH", ""))
    planes["path"] = verdict
    lines.append(line)
    verdict, line, _ = python_plane(runner, resolver)
    planes["python"] = verdict
    lines.append(line)
    verdict, line, _ = git_plane(runner, os.path.isdir(os.path.join(repo_dir, ".git")), config_reader)
    planes["git"] = verdict
    lines.append(line)
    roll_verdict, roll_line = rollup(planes)
    for line in lines:
        out.write(line + "\n")
    out.write(roll_line + "\n")
    return {ORDER[p] for p in planes.values()}.pop() if len({ORDER[p] for p in planes.values()}) == 1 else \
        max(ORDER[p] for p in planes.values())


def selftest(out):
    """20 hermetic cases over injected resolvers/runners. No subprocess, no writes."""
    class FakeProc:
        def __init__(self, rc=0, out=""):
            self.returncode = rc
            self.stdout = out

    cases = []
    isdir = lambda p: p in ("/ok/a", "/ok/b", "/ok/c")

    def case(name, got, want):
        cases.append((name, got == want, name + ": got %r want %r" % (got, want)))

    # path plane (POSIX ':' fixtures; os.pathsep is ';' on Windows, so pass it)
    v, _, f = path_plane("/ok/a:/ok/b:/ok/c", exists=isdir, pathsep=":")
    case("path-clean-zero", (f["total"], f["missing"], f["dup_values"], f["empty"], v), (3, 0, 0, 0, GREEN))
    v, _, f = path_plane("/ok/a:/ok/b:/ok/a", exists=isdir, pathsep=":")
    case("path-dup-detected", (f["dup_values"], f["dup_positions"]), (1, [0, 2]))
    v, _, f = path_plane("/ok/a:/gone:/ok/c", exists=isdir, pathsep=":")
    case("path-missing-detected", (f["missing"], v), (1, DEGRADED))
    v, _, f = path_plane("/ok/a::/ok/c", exists=isdir, pathsep=":")
    case("path-empty-entry", (f["empty"], v), (1, DEGRADED))
    # grammar: a raw value with newline/space/= must not reach the output
    verdict, line, _ = path_plane("/ok/a:x\ny=bad:/ok/c", exists=isdir, pathsep=":")
    case("grammar-single-line", (len(line.splitlines()), "\n" in line), (1, False))
    # tools plane
    res_all = lambda t: "/opt/%s.exe" % t if t in REQUIRED_TOOLS or t == "python3" else None
    v, line, f = tools_plane(res_all)
    case("tools-all-required", (v, f["required_missing"], f["stubs"]), (GREEN, [], []))
    res_no_gh = lambda t: None if t == "gh" else res_all(t)
    v, line, f = tools_plane(res_no_gh)
    case("tools-required-absent-degraded", (v, f["required_missing"]), (DEGRADED, ["gh"]))
    res_no_git = lambda t: None if t == "git" else res_all(t)
    v, line, f = tools_plane(res_no_git)
    case("tools-git-absent-blocked", v, BLOCKED)
    res_stub = lambda t: "C:/Users/u/AppData/Local/WindowsApps/python3.EXE" if t == "python3" else res_all(t)
    v, line, f = tools_plane(res_stub)
    case("tools-stub-classified", (v, f["stubs"]), (DEGRADED, ["python3"]))
    res_linux_gone = lambda t: res_all(t)
    v, line, f = tools_plane(res_linux_gone)
    case("tools-linux-absent-expected", v, GREEN)
    # python plane
    run_ok = lambda cmd: FakeProc(0, "OK\n")
    v, line, _ = python_plane(run_ok, res_stub)
    case("python-stub-degraded", v, DEGRADED)
    v, line, _ = python_plane(run_ok, lambda t: None)
    case("python-blocked-when-absent", v, BLOCKED)
    run_fail = lambda cmd: FakeProc(49, "")
    v, line, _ = python_plane(run_fail, res_all)
    case("python-blocked-when-run-fails", v, BLOCKED)
    res_plain = lambda t: "/opt/python.exe" if t == "python" else None
    v, line, _ = python_plane(run_ok, res_plain)
    case("python-green-plain", v, GREEN)
    # git plane
    runner_ok = lambda cmd: FakeProc(0, "git version 2.55.0.windows.3\n" if cmd[0] == "git" else "gh version 2.101.0\n")
    v, line, _ = git_plane(runner_ok, True, lambda k: "tsukuroi" if k == "user.name" else "tsukuroi@shokunin.local")
    case("git-green", v, GREEN)
    runner_raises = lambda cmd: (_ for _ in ()).throw(OSError("boom"))
    v, line, _ = git_plane(runner_raises, True, lambda k: "")
    case("git-blocked-on-error", v, BLOCKED)
    v, line, _ = git_plane(runner_ok, True, lambda k: "")
    case("git-degraded-identity-unset", v, DEGRADED)
    v, line, _ = git_plane(runner_ok, False, lambda k: "tsukuroi" if k == "user.name" else "tsukuroi@shokunin.local")
    case("git-degraded-repo-absent", v, DEGRADED)
    # rollup + determinism
    case("rollup-degraded", rollup({"tools": GREEN, "path": DEGRADED, "python": GREEN, "git": GREEN}),
         (DEGRADED, "WIN_CENSUS: DEGRADED (git=GREEN path=DEGRADED python=GREEN tools=GREEN)"))
    case("rollup-blocked-wins", rollup({"tools": GREEN, "path": GREEN, "python": BLOCKED, "git": GREEN})[0], BLOCKED)

    passed = sum(1 for _, ok, _ in cases if ok)
    for name, ok, msg in cases:
        out.write("%s %s\n" % ("PASS" if ok else "FAIL", name))
        if not ok:
            out.write("  %s\n" % msg)
    out.write("WIN_CENSUS_SELFTEST: %s (%d cases, %d passed, %d failed)\n"
              % ("PASS" if passed == len(cases) else "FAIL", len(cases), passed, len(cases) - passed))
    return EXIT_CLEAN if passed == len(cases) else EXIT_DEGRADED


def main(argv):
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if "--selftest" in argv:
        return selftest(sys.stdout)
    if argv:
        sys.stderr.write("usage: win-host-census-r53.py [--selftest]\n")
        return EXIT_BLOCKED
    return live_census(repo_dir, sys.stdout)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
