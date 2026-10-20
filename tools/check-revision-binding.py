#!/usr/bin/env python3
"""Read-only counting probe: are the --revision gates bound to a landed revision,
and do they all bind the same way?

Round-17 wave 2 widened the count from the five legacy gates to every tools/*.py gate
with --revision (nine at 90037c2); `legacy_bound` keeps the five-tool continuity count.
Round 18 adds `consistent_tools`: wave-2 FxSimplifyBind found six same-input
divergences between the nine copied binding checks, and the shared module
tools/_revision.py replaces the copies. The judge below keeps its own independent
binding code on purpose: it grades the tools and must not share what it grades.

Measured tools, taken at --tools-revision: the nine named in TOOLS (an absent one
counts unbound, so deleting a tool cannot raise the ratio) plus every other
tools/*.py at that revision whose source contains the argparse literal "--revision"
(this judge and `_`-prefixed modules excluded).

A throwaway clone of the lane gets refs/heads/<branch> set to the measured
commit and one empty commit created on a detached HEAD. Each tool is run in that
sandbox. BOUND (round-17 contract) needs every one of:

  head / at-parent / branch-name  --revision HEAD|@-|master   -> 2, E-REVISION-INVALID
  unlanded                        --revision <unlanded>       -> 2, E-REVISION-NOT-LANDED
  tip / short-tip / landed-parent -> exit != 2 and JSON revision == that commit
  not-pushed  (origin lags one commit)                        -> 2, E-REVISION-NOT-PUSHED

CONSISTENT (round-18 shared contract) is BOUND plus the FxSimplifyBind probes:

  branch-range / branch-slash / branch-space  --branch a..b|master/|"bad branch"
                                                          -> 2, E-BRANCH-INVALID   (D1, D6)
  branch-first  --revision HEAD --branch a..b             -> 2, E-BRANCH-INVALID   (D2)
  git-failed    origin ref names a blob                   -> 2, E-GIT-FAILED       (D3)
  single-id     the unlanded refusal carries exactly one binding finding        (D4)
  branch-missing --branch nosuch                          -> 2, E-BRANCH-MISSING   (D5)

`shared_tools` counts tools that import tools/_revision.py and carry no local copy
of the 7-64 hex revision regex; `local_rev_regex_copies` counts those copies.

--tools-revision is itself bound: 7-64 hex (HEAD/@/refs rejected with
E-REVISION-INVALID), landed on refs/heads/<branch> else E-REVISION-NOT-LANDED,
and on refs/remotes/origin/<branch> when present else E-REVISION-NOT-PUSHED.
--selftest is hermetic: stub tools in mktemp fixtures, never the real lane.
Exit 0 = every measured tool consistent, 1 = fewer, 2 = could-not-evaluate. JSON
on stdout; the lane is only read (clone, show, rev-parse, merge-base) and the only
writes are inside the temporary sandbox clone.
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, tempfile
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
ROOT = Path(__file__).resolve().parents[1]
TOOLS = (
    "check-locator-clarification.py",
    "check-root-dac-correction.py",
    "check-section-citations.py",
    "check-source-scope-correction.py",
    "measure-update-recheck.py",
)
LEGACY = TOOLS
# Round-17 wave-2 (FxC3Gameability): count every tool that defines --revision, not a
# fixed five. Extra argv a tool needs to run at a revision; absent tools are unbound.
R17_GATES = {
    "check-boot-chain.py": (),
    "check-freshness-r17.py": (),
    "check-recheck-commands.py": (),
    "check-seat-scope.py": ("--wave", ".ufo/waves/round-16/build"),
}
EXTRA = {name: () for name in TOOLS}
EXTRA.update(R17_GATES)
TOOLS = TOOLS + tuple(R17_GATES)
TOTAL = len(TOOLS)
JUDGE = "check-revision-binding.py"
REV = re.compile(r"^[0-9a-fA-F]{7,64}$")
ID_INVALID = "E-REVISION-INVALID"
ID_UNLANDED = "E-REVISION-NOT-LANDED"
ID_PUSHED = "E-REVISION-NOT-PUSHED"
ID_BRANCH_INVALID = "E-BRANCH-INVALID"
ID_BRANCH_MISSING = "E-BRANCH-MISSING"
ID_GIT = "E-GIT-FAILED"
BINDING_IDS = (ID_INVALID, ID_UNLANDED, ID_PUSHED, ID_BRANCH_INVALID, ID_BRANCH_MISSING, ID_GIT)
MISSING = re.compile(r"does not exist|exists on disk, but not in|not in '", re.I)
SHARED_IMPORT = re.compile(r"^[ \t]*(?:import _revision\b|from _revision import\b)", re.M)
LOCAL_REV_REGEX = re.compile(r"\{7,64\}")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C"})
    return env


def git(repo, *args, timeout=60):
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(repo), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=clean_env(), timeout=timeout)
    except subprocess.TimeoutExpired:
        raise Cannot("E-GIT-TIMEOUT", "git", f"git {args[0]} exceeded {timeout}s")
    except OSError as exc:
        raise Cannot("E-GIT-FAILED", "git", str(exc)[:120])


def must(proc, fid, site):
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()[:160]
        raise Cannot(fid, site, detail or f"exit={proc.returncode}")
    return proc


def ref_exists(repo, ref):
    return git(repo, "rev-parse", "--verify", "--quiet", ref).returncode == 0


def rev_parse(repo, ref):
    proc = git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    if proc.returncode != 0:
        raise Cannot(ID_INVALID, "revision", f"{ref} not found")
    return proc.stdout.decode("ascii", "replace").strip()


def ancestor(repo, sha, ref):
    proc = git(repo, "merge-base", "--is-ancestor", sha, ref)
    if proc.returncode == 0:
        return True
    if proc.returncode == 1:
        return False
    raise Cannot("E-GIT-FAILED", "git", f"merge-base --is-ancestor exited {proc.returncode}")


def bind(repo, rev, branch="master"):
    """Resolve rev and enforce the round-17 C3 revision-binding contract."""
    if not REV.fullmatch(rev):
        raise Cannot(ID_INVALID, "revision", "7-64 hex commit required")
    sha = rev_parse(repo, rev)
    local = f"refs/heads/{branch}"
    if not ref_exists(repo, local):
        raise Cannot("E-BRANCH-MISSING", local, "branch ref absent")
    if not ancestor(repo, sha, local):
        raise Cannot(ID_UNLANDED, "revision", f"{sha[:12]} not reachable from {local}")
    remote = f"refs/remotes/origin/{branch}"
    if ref_exists(repo, remote) and not ancestor(repo, sha, remote):
        raise Cannot(ID_PUSHED, "revision", f"{sha[:12]} not reachable from {remote}")
    return sha


def lane_tip(repo, branch):
    try:
        return rev_parse(Path(repo), f"refs/heads/{branch}")
    except Cannot:
        return None


def clone_lane(lane, dest):
    try:
        proc = subprocess.run(["git", "clone", "--no-hardlinks", "--quiet", "--no-tags",
                               str(lane), str(dest)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=clean_env(), timeout=180)
    except subprocess.TimeoutExpired:
        raise Cannot("E-CLONE", "lane", "git clone exceeded 180s")
    except OSError as exc:
        raise Cannot("E-CLONE", "lane", str(exc)[:120])
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()[:160]
        raise Cannot("E-CLONE", "lane", detail or "git clone failed")


def prepare(sandbox, tip, branch):
    must(git(sandbox, "checkout", "--quiet", "--detach", tip), "E-SANDBOX", "checkout")
    must(git(sandbox, "update-ref", f"refs/heads/{branch}", tip), "E-SANDBOX", "update-ref")
    # The clone's origin is the lane: drop the remote (SentSandboxGit F4), then recreate
    # only the tracking ref so the not-pushed probe can move it.
    if git(sandbox, "remote").stdout.strip():
        must(git(sandbox, "remote", "remove", "origin"), "E-SANDBOX", "remote remove")
    must(git(sandbox, "update-ref", f"refs/remotes/origin/{branch}", tip),
         "E-SANDBOX", "update-ref")
    return True


def discover(sandbox, tip):
    """Every other tools/*.py at `tip` that defines --revision (judge and `_` modules excluded)."""
    proc = must(git(sandbox, "ls-tree", "--name-only", f"{tip}:tools"), "E-GIT-READ", "tools/")
    found = []
    for name in sorted(proc.stdout.decode("utf-8", "replace").split("\n")):
        if (not name.endswith(".py") or name in TOOLS or name == JUDGE
                or name.startswith("_")):
            continue
        body = must(git(sandbox, "show", f"{tip}:tools/{name}"), "E-GIT-READ", f"tools/{name}")
        if b'"--revision"' in body.stdout:
            found.append(name)
    return tuple(found)


def materialize(sandbox, tip, names=TOOLS):
    absent, sources = set(), {}
    for name in names:
        proc = git(sandbox, "show", f"{tip}:tools/{name}")
        error = proc.stderr.decode("utf-8", "replace")
        if proc.returncode != 0:
            if MISSING.search(error):
                absent.add(name)
                continue
            raise Cannot("E-GIT-READ", f"tools/{name}", error.strip()[:120])
        target = sandbox / "tools" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(proc.stdout)
        target.chmod(0o755)
        sources[name] = proc.stdout.decode("utf-8", "replace")
    return absent, sources


def shared(source):
    """(imports tools/_revision.py, local 7-64 hex regex copies) for one tool source."""
    return bool(SHARED_IMPORT.search(source)), len(LOCAL_REV_REGEX.findall(source))


def probe_commit(sandbox, tip, branch):
    proc = git(sandbox, "-c", "user.name=revision-binding",
               "-c", "user.email=revision-binding@invalid",
               "-c", "commit.gpgsign=false", "commit", "--allow-empty",
               "--no-verify", "--quiet", "-m", "revision-binding probe (unlanded)")
    must(proc, "E-SANDBOX", "probe-commit")
    sha = rev_parse(sandbox, "HEAD")
    if sha == tip or ancestor(sandbox, sha, f"refs/heads/{branch}"):
        raise Cannot("E-SANDBOX", "probe-commit", "probe commit is still landed")
    return sha


def parse_json(text):
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return None


def binding_ids(text):
    """Binding finding ids the tool reported (JSON findings list, else distinct text tokens)."""
    doc = parse_json(text)
    if isinstance(doc, dict) and isinstance(doc.get("findings"), list):
        return [item["id"] for item in doc["findings"]
                if isinstance(item, dict) and item.get("id") in BINDING_IDS]
    return sorted(set(re.findall(r"\bE-[A-Z0-9-]{2,}\b", text)) & set(BINDING_IDS))


def finding_id(text):
    doc = parse_json(text)
    if isinstance(doc, dict) and isinstance(doc.get("findings"), list):
        for item in doc["findings"]:
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                return item["id"]
    match = re.search(r"\bE-[A-Z0-9-]{2,}\b", text)
    return match.group(0) if match else None


def run_tool(sandbox, name, revision, branch=None):
    extra = () if branch is None else ("--branch", branch)
    try:
        proc = subprocess.run([sys.executable, str(sandbox / "tools" / name),
                               "--revision", revision, *extra, *EXTRA.get(name, ())],
                              cwd=str(sandbox), stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=clean_env(), timeout=60)
    except subprocess.TimeoutExpired:
        raise Cannot("E-TOOL-TIMEOUT", f"tools/{name}", "exceeded 60s")
    except OSError as exc:
        raise Cannot("E-TOOL-RUN", f"tools/{name}", str(exc)[:120])
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def reason(cases):
    out = []
    for label, case in cases.items():
        if not case["ok"]:
            out.append(f"{label}:exit={case['exit']},"
                       f"finding={case.get('finding')},revision={case.get('json_revision')}")
    return ";".join(out)


def refused(sandbox, name, rev, want, branch=None):
    code, text = run_tool(sandbox, name, rev, branch)
    found = finding_id(text)
    return {"exit": code, "finding": found, "binding_ids": binding_ids(text),
            "ok": code == CANNOT and found == want}


def accepted(sandbox, name, rev, expect_sha):
    """Accepted = not CANNOT and the JSON names the independently resolved commit."""
    code, text = run_tool(sandbox, name, rev)
    doc = parse_json(text)
    got = doc.get("revision") if isinstance(doc, dict) else None
    got = got if isinstance(got, str) else None
    return {"exit": code, "json_revision": got,
            "ok": code != CANNOT and got is not None and expect_sha is not None
            and got.lower() == expect_sha.lower()}


def blob_object(sandbox):
    proc = subprocess.run(["git", "-C", str(sandbox), "hash-object", "-w", "--stdin"],
                          input=b"revision-binding probe blob\n", stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=clean_env(), timeout=60)
    must(proc, "E-SANDBOX", "blob")
    return proc.stdout.decode("ascii", "replace").strip()


def probe_tool(sandbox, name, tip, unlanded_sha, parent=None, branch="master", blob=None):
    cases = {
        "head": refused(sandbox, name, "HEAD", ID_INVALID),
        "at-parent": refused(sandbox, name, "@-", ID_INVALID),
        "branch-name": refused(sandbox, name, "master", ID_INVALID),
        "unlanded": refused(sandbox, name, unlanded_sha, ID_UNLANDED),
        "tip": accepted(sandbox, name, tip, tip),
        "short-tip": accepted(sandbox, name, tip[:8], tip),
    }
    remote = f"refs/remotes/origin/{branch}"
    if parent is not None:
        cases["landed-parent"] = accepted(sandbox, name, parent, parent)
        must(git(sandbox, "update-ref", remote, parent), "E-SANDBOX", "origin lag")
        try:
            cases["not-pushed"] = refused(sandbox, name, tip, ID_PUSHED)
        finally:
            must(git(sandbox, "update-ref", remote, tip), "E-SANDBOX", "origin restore")
    bound = all(case["ok"] for case in cases.values())
    # Round-18 shared-contract probes (FxSimplifyBind D1-D6).
    shared_cases = {
        "branch-range": refused(sandbox, name, tip, ID_BRANCH_INVALID, "a..b"),
        "branch-slash": refused(sandbox, name, tip, ID_BRANCH_INVALID, "master/"),
        "branch-space": refused(sandbox, name, tip, ID_BRANCH_INVALID, "bad branch"),
        "branch-first": refused(sandbox, name, "HEAD", ID_BRANCH_INVALID, "a..b"),
        "branch-missing": refused(sandbox, name, tip, ID_BRANCH_MISSING, "nosuch"),
    }
    single = cases["unlanded"]
    shared_cases["single-id"] = {"exit": single["exit"], "finding": single["finding"],
                                 "binding_ids": single["binding_ids"],
                                 "ok": single["ok"] and single["binding_ids"] == [ID_UNLANDED]}
    if blob is not None:
        must(git(sandbox, "update-ref", remote, blob), "E-SANDBOX", "origin blob")
        try:
            shared_cases["git-failed"] = refused(sandbox, name, tip, ID_GIT)
        finally:
            must(git(sandbox, "update-ref", remote, tip), "E-SANDBOX", "origin restore")
    consistent = bound and all(case["ok"] for case in shared_cases.values())
    out = {"tool": f"tools/{name}", "bound": bound, "consistent": consistent,
           "reason": None if bound else reason(cases),
           "shared_reason": None if consistent else reason({**cases, **shared_cases})}
    out.update(cases)
    out.update(shared_cases)
    return out


def measure(lane, tools_rev, branch="master"):
    lane = Path(lane).resolve()
    tip = bind(lane, tools_rev, branch)
    branch_tip = lane_tip(lane, branch)
    with tempfile.TemporaryDirectory(prefix="tsukuroi-rebind-") as tmp:
        sandbox = Path(tmp) / "repo"
        clone_lane(lane, sandbox)
        pinned = prepare(sandbox, tip, branch)
        extras = discover(sandbox, tip)
        names = TOOLS + extras
        absent, sources = materialize(sandbox, tip, names)
        parent_proc = git(sandbox, "rev-parse", "--verify", "--quiet", f"{tip}^1^{{commit}}")
        parent = (parent_proc.stdout.decode("ascii", "replace").strip()
                  if parent_proc.returncode == 0 else None)
        unlanded_sha = probe_commit(sandbox, tip, branch)
        blob = blob_object(sandbox)
        per_tool = []
        for name in names:
            if name in absent:
                per_tool.append({"tool": f"tools/{name}", "bound": False, "consistent": False,
                                 "shared": False, "local_rev_regex": 0,
                                 "reason": "absent at measured revision",
                                 "shared_reason": "absent at measured revision"})
                continue
            item = probe_tool(sandbox, name, tip, unlanded_sha, parent, branch, blob)
            imports, copies = shared(sources[name])
            item["shared"] = imports and copies == 0
            item["local_rev_regex"] = copies
            per_tool.append(item)
    total = len(names)
    bound = sum(1 for item in per_tool if item["bound"])
    consistent = sum(1 for item in per_tool if item["consistent"])
    legacy = sum(1 for item in per_tool
                 if item["bound"] and item["tool"].split("/", 1)[1] in LEGACY)
    return {"status": "PASS" if consistent == total else "FAIL",
            "tools_revision": tip, "revision": tip, "branch": branch,
            "branch_tip": branch_tip, "bound_tools": bound, "consistent_tools": consistent,
            "shared_tools": sum(1 for item in per_tool if item["shared"]),
            "local_rev_regex_copies": sum(item["local_rev_regex"] for item in per_tool),
            "total": total, "named_total": TOTAL, "discovered": list(extras),
            "legacy_bound": legacy, "legacy_total": len(LEGACY),
            "sandbox_origin_pinned": pinned, "per_tool": per_tool}


def grade(result):
    return (PASS if result["consistent_tools"] == result["total"] else FAIL), result["status"]


def emit_report(payload, code):
    print(json.dumps(payload, sort_keys=True))
    return code


def cannot_payload(rev, branch, exc):
    return {"status": "CANNOT_EVALUATE", "tools_revision": rev, "revision": None,
            "branch": branch, "branch_tip": None, "bound_tools": 0,
            "consistent_tools": 0, "shared_tools": 0,
            "total": TOTAL, "per_tool": [],
            "findings": [{"id": exc.fid, "site": exc.site, "detail": exc.detail}]}


def build_parser():
    parser = argparse.ArgumentParser(
        description="Read-only revision-binding counting probe over every --revision gate.",
        exit_on_error=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tools-revision", metavar="REV",
                       help="required: 7-64 hex commit landed on the measured branch")
    group.add_argument("--selftest", action="store_true", help="hermetic stub-tool suite")
    parser.add_argument("--branch", default="master",
                        help="landed branch to bind against (default master)")
    return parser


def cli_finding(argv):
    try:
        build_parser().parse_args(argv)
        return None
    except (argparse.ArgumentError, SystemExit):
        return "E-CLI"


STUB = '''#!/usr/bin/env python3
import json, re, subprocess, sys
from pathlib import Path
__SHARED__MODE = "__MODE__"
LEGACY = MODE == "legacy"  # round-17 copies: no branch checks, rc>=2 = not ancestor
HEX = r"[0-9a-f]{%d,%d}" % (7, 64)
ROOT = Path(__file__).resolve().parents[1]
def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
def out(rev, ident=None, code=0, status="PASS"):
    idents = [] if ident is None else ([ident] if isinstance(ident, str) else ident)
    print(json.dumps({"status": status, "revision": rev,
                      "findings": [{"id": i} for i in idents]}))
    sys.exit(code)
argv = sys.argv
rev = argv[argv.index("--revision") + 1]
branch = argv[argv.index("--branch") + 1] if "--branch" in argv else "master"
def tip():
    return git("rev-parse", "refs/heads/master").stdout.strip()
if MODE == "tip-only":  # S1: accepts only the exact branch tip
    if not re.fullmatch(HEX, rev):
        out(rev, "E-REVISION-INVALID", 2, "CANNOT_EVALUATE")
    sha = git("rev-parse", "--verify", "--quiet", rev + "^{commit}").stdout.strip()
    if sha != tip():
        out(rev, "E-REVISION-NOT-LANDED", 2, "CANNOT_EVALUATE")
    out(sha)
if MODE == "head-only":  # S3: rejects only the literal HEAD
    if rev == "HEAD":
        out(rev, "E-REVISION-INVALID", 2, "CANNOT_EVALUATE")
    sha = git("rev-parse", "--verify", "--quiet", rev + "^{commit}").stdout.strip()
    if git("merge-base", "--is-ancestor", sha, "refs/heads/master").returncode != 0:
        out(rev, "E-REVISION-NOT-LANDED", 2, "CANNOT_EVALUATE")
    out(sha)
if MODE == "unbound":
    sha = git("rev-parse", "--verify", "--quiet", rev + "^{commit}").stdout.strip()
    out(sha)
if not LEGACY and (not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9._/-]*", branch)
                   or branch == "HEAD"
                   or git("check-ref-format", "refs/heads/" + branch).returncode != 0):
    out(rev, "E-BRANCH-INVALID", 2, "CANNOT_EVALUATE")
if not re.fullmatch(HEX, rev):
    ident = "E-OTHER-INVALID" if MODE == "wrong-id" else "E-REVISION-INVALID"
    out(rev, ident, 2, "CANNOT_EVALUATE")
sha = git("rev-parse", "--verify", "--quiet", rev + "^{commit}").stdout.strip()
if not sha:
    out(rev, "E-REVISION-INVALID", 2, "CANNOT_EVALUATE")
local, remote = "refs/heads/" + branch, "refs/remotes/origin/" + branch
if not LEGACY and git("rev-parse", "--verify", "--quiet", local + "^{commit}").returncode != 0:
    out(rev, "E-BRANCH-MISSING", 2, "CANNOT_EVALUATE")
def anc(ref):
    code = git("merge-base", "--is-ancestor", sha, ref).returncode
    if code in (0, 1) or LEGACY:
        return code == 0
    out(rev, "E-GIT-FAILED", 2, "CANNOT_EVALUATE")
has_origin = MODE != "no-origin" and git("rev-parse", "--verify", "--quiet",
                                         remote).returncode == 0
if not anc(local):
    if MODE == "double" and has_origin and not anc(remote):
        out(rev, ["E-REVISION-NOT-LANDED", "E-REVISION-NOT-PUSHED"], 2, "CANNOT_EVALUATE")
    out(rev, "E-REVISION-NOT-LANDED", 2, "CANNOT_EVALUATE")
if has_origin and not anc(remote):
    out(rev, "E-REVISION-NOT-PUSHED", 2, "CANNOT_EVALUATE")
out(rev if MODE == "echo" else sha)
'''


def stub_source(mode):
    shared_line = "if False:\n    import _revision\n" if mode == "shared" else ""
    return STUB.replace("__SHARED__", shared_line).replace("__MODE__", mode)


def run_cmd(args, cwd=None):
    return subprocess.run(args, cwd=str(cwd) if cwd else None,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=clean_env(), timeout=120)


def commit_all(root, message):
    args = ["-c", "user.name=revision-binding",
            "-c", "user.email=revision-binding@invalid", "-c", "commit.gpgsign=false"]
    must(run_cmd(["git", "-C", str(root), *args, "add", "-A"]),
         "E-SANDBOX", "fixture add")
    must(run_cmd(["git", "-C", str(root), *args, "commit", "--quiet", "--no-verify",
                  "--allow-empty", "-m", message]), "E-SANDBOX", "fixture commit")
    return rev_parse(root, "HEAD")


def make_fixture(root, modes, return_base=False, extra_files=None):
    root.mkdir(parents=True, exist_ok=True)
    must(run_cmd(["git", "init", "--quiet", str(root)]), "E-SANDBOX", "fixture init")
    must(git(root, "symbolic-ref", "HEAD", "refs/heads/master"),
         "E-SANDBOX", "fixture default branch")
    (root / "README").write_text("fixture\n", encoding="utf-8")
    base = commit_all(root, "base")
    tools = root / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    for name, mode in modes.items():
        path = tools / name
        path.write_text(stub_source(mode), encoding="utf-8")
        path.chmod(0o755)
    for name, text in (extra_files or {}).items():
        (tools / name).write_text(text, encoding="utf-8")
    tip = commit_all(root, "tools")
    return (tip, base) if return_base else tip


def bind_error(repo, rev, branch="master"):
    try:
        bind(repo, rev, branch)
        return None
    except Cannot as exc:
        return exc.fid


def detached_commit(root):
    tip = rev_parse(root, "HEAD")
    must(git(root, "checkout", "--quiet", "--detach", tip), "E-SANDBOX", "fixture detach")
    must(run_cmd(["git", "-C", str(root), "-c", "user.name=revision-binding",
                  "-c", "user.email=revision-binding@invalid",
                  "-c", "commit.gpgsign=false", "commit", "--allow-empty",
                  "--no-verify", "--quiet", "-m", "probe"]), "E-SANDBOX", "fixture probe")
    sha = rev_parse(root, "HEAD")
    if sha == tip or ancestor(root, sha, "refs/heads/master"):
        raise Cannot("E-SANDBOX", "fixture probe", "probe commit is still landed")
    return sha


def selftest():
    passed, failures = 0, []

    def check(name, got, want):
        nonlocal passed
        if got == want:
            passed += 1
        else:
            failures.append(f"{name}: got={got!r} want={want!r}")

    try:
        with tempfile.TemporaryDirectory(prefix="tsukuroi-rebind-st-") as tmp:
            tmp = Path(tmp)
            modes = {name: "bound" for name in TOOLS}

            fx = tmp / "all"
            tip = make_fixture(fx, modes)
            res = measure(fx, tip)
            check("all-bound-count", res["bound_tools"], TOTAL)
            check("all-bound-status", res["status"], "PASS")
            check("all-bound-exit", grade(res)[0], PASS)
            check("all-bound-tools-revision", res["tools_revision"], tip)
            check("all-bound-branch-tip", res["branch_tip"], tip)

            mixed = {name: ("bound" if i < 3 else "unbound")
                     for i, name in enumerate(TOOLS)}
            fx2 = tmp / "mixed"
            tip2 = make_fixture(fx2, mixed)
            res2 = measure(fx2, tip2)
            check("mixed-count", res2["bound_tools"], 3)
            check("mixed-exit", grade(res2)[0], FAIL)
            check("mixed-reasons", [bool(item["reason"]) for item in res2["per_tool"]],
                  [False, False, False] + [True] * (TOTAL - 3))

            fx3 = tmp / "wrong-id"
            modes3 = dict(modes)
            modes3[TOOLS[0]] = "wrong-id"
            tip3 = make_fixture(fx3, modes3)
            res3 = measure(fx3, tip3)
            first = res3["per_tool"][0]
            check("wrong-id-count", res3["bound_tools"], TOTAL - 1)
            check("wrong-id-finding", first["head"]["finding"], "E-OTHER-INVALID")
            check("wrong-id-reason", first["reason"].split(";")[0],
                  "head:exit=2,finding=E-OTHER-INVALID,revision=None")

            fx4 = tmp / "absent"
            tip4 = make_fixture(fx4, {name: "bound" for name in TOOLS[:-1]})
            res4 = measure(fx4, tip4)
            check("absent-tool", (res4["bound_tools"], res4["per_tool"][-1]["reason"]),
                  (TOTAL - 1, "absent at measured revision"))
            check("absent-not-consistent", (res4["consistent_tools"], grade(res4)[0]),
                  (TOTAL - 1, FAIL))

            # Round 18: the shared contract (FxSimplifyBind D1-D6).
            check("all-consistent", (res["consistent_tools"], res["total"], res["discovered"]),
                  (TOTAL, TOTAL, []))
            check("all-shared-census", (res["shared_tools"], res["local_rev_regex_copies"]),
                  (0, 0))
            check("mixed-consistent", res2["consistent_tools"], 3)
            for stub, failing in (("legacy", {"branch-range", "branch-slash", "branch-space",
                                              "branch-first", "branch-missing", "git-failed"}),
                                  ("double", {"single-id"})):
                fxl = tmp / f"shared-{stub}"
                ml = dict(modes)
                ml[TOOLS[0]] = stub
                resl = measure(fxl, make_fixture(fxl, ml))
                item = resl["per_tool"][0]
                bad = {label for label in ("branch-range", "branch-slash", "branch-space",
                                           "branch-first", "branch-missing", "single-id",
                                           "git-failed") if not item[label]["ok"]}
                check(f"shared-{stub}-bound-not-consistent",
                      (item["bound"], item["consistent"], resl["bound_tools"],
                       resl["consistent_tools"], grade(resl)[0]),
                      (True, False, TOTAL, TOTAL - 1, FAIL))
                check(f"shared-{stub}-failing-probes", bad, failing)
            fxd = tmp / "discover"
            md = dict(modes)
            md[TOOLS[0]] = "shared"
            extra = {"check-extra.py": stub_source("bound"),
                     "_helper.py": "# helper\nFLAG = \"--revision\"\n",
                     "plain.py": "print('no revision flag')\n",
                     "notes.txt": "\"--revision\"\n"}
            resd = measure(fxd, make_fixture(fxd, md, extra_files=extra))
            check("discover-extra", (resd["discovered"], resd["total"],
                                     resd["consistent_tools"], grade(resd)[0]),
                  (["check-extra.py"], TOTAL + 1, TOTAL + 1, PASS))
            check("shared-import-census", (resd["shared_tools"],
                                           resd["per_tool"][0]["shared"],
                                           resd["per_tool"][0]["local_rev_regex"]),
                  (1, True, 0))
            check("local-copy-census", shared('REV = re.compile(r"^[0-9a-f]{7,64}$")\n'
                                              "import _revision\n"), (True, 1))
            fxu = tmp / "discover-unbound"
            resu = measure(fxu, make_fixture(fxu, modes,
                                             extra_files={"check-extra.py": stub_source("unbound")}))
            check("discover-unbound-counts", (resu["total"], resu["consistent_tools"],
                                              grade(resu)[0]), (TOTAL + 1, TOTAL, FAIL))

            for stub in ("tip-only", "no-origin", "head-only", "echo"):
                fxs = tmp / f"stub-{stub}"
                ms = dict(modes)
                ms[TOOLS[0]] = stub
                tips = make_fixture(fxs, ms)
                ress = measure(fxs, tips)
                check(f"stub-{stub}-unbound", (ress["per_tool"][0]["bound"],
                                               ress["bound_tools"]), (False, TOTAL - 1))
            check("legacy-count", res["legacy_bound"], len(LEGACY))

            fx5 = tmp / "bind"
            tip5 = make_fixture(fx5, modes)
            check("bind-tip", bind(fx5, tip5), tip5)
            check("bind-head", bind_error(fx5, "HEAD"), ID_INVALID)
            check("bind-at", bind_error(fx5, "@"), ID_INVALID)
            check("bind-ref", bind_error(fx5, "refs/heads/master"), ID_INVALID)
            check("bind-unknown", bind_error(fx5, "0" * 40), ID_INVALID)
            unlanded_sha = detached_commit(fx5)
            check("bind-unlanded", bind_error(fx5, unlanded_sha), ID_UNLANDED)

            fx6 = tmp / "pushed"
            tip6, base6 = make_fixture(fx6, modes, return_base=True)
            must(git(fx6, "update-ref", "refs/remotes/origin/master", base6),
                 "E-SANDBOX", "fixture origin")
            check("bind-not-pushed", bind_error(fx6, tip6), ID_PUSHED)

            check("cli-empty", cli_finding([]), "E-CLI")
            check("cli-both", cli_finding(["--tools-revision", tip5, "--selftest"]), "E-CLI")
            check("cli-ok", cli_finding(["--selftest"]), None)

            payload = cannot_payload("HEAD", "master",
                                     Cannot(ID_INVALID, "revision", "not hex"))
            check("cannot-shape", (payload["status"], payload["bound_tools"],
                                   payload["total"], payload["findings"][0]["id"]),
                  ("CANNOT_EVALUATE", 0, TOTAL, ID_INVALID))
    except Cannot as exc:
        failures.append(f"fixture: {exc.fid} {exc.site} {exc.detail}")

    total = passed + len(failures)
    if failures:
        print(f"CHECK_REVISION_BINDING_SELFTEST: FAIL ({total} cases, {passed} passed)")
        print("\n".join("  " + item for item in failures))
        return FAIL
    print(f"CHECK_REVISION_BINDING_SELFTEST: PASS ({total} cases, {passed} passed, 0 failed)")
    return PASS


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit) as exc:
        if isinstance(exc, SystemExit) and not exc.code:
            return 0
        payload = cannot_payload(None, "master", Cannot("E-CLI", "cli", "invalid arguments"))
        return emit_report(payload, CANNOT)
    if args.selftest:
        return selftest()
    try:
        result = measure(ROOT, args.tools_revision, args.branch)
    except Cannot as exc:
        payload = cannot_payload(args.tools_revision, args.branch, exc)
        payload["branch_tip"] = lane_tip(ROOT, args.branch)
        return emit_report(payload, CANNOT)
    except Exception as exc:  # no traceback exit 1: unreadable input is CANNOT
        payload = cannot_payload(args.tools_revision, args.branch,
                                 Cannot("E-INTERNAL", "probe", str(exc)[:120]))
        return emit_report(payload, CANNOT)
    code, _ = grade(result)
    return emit_report(result, code)


if __name__ == "__main__":
    sys.exit(main())
