#!/usr/bin/env python3
"""Read-only counting probe: are the --revision gates bound to a landed revision,
and do they all bind the same way?

Round-17 wave 2 widened the count from the five legacy gates to every tools/*.py gate
with --revision (nine at 90037c2); `legacy_bound` keeps the five-tool continuity count.
Round 18 adds `consistent_tools`: wave-2 FxSimplifyBind found six same-input
divergences between the nine copied binding checks, and the shared module
tools/_revision.py replaces the copies. The judge below keeps its own independent
binding code on purpose: it grades the tools and must not share what it grades.

Measured continuity set: the nine original tools named in TOOLS. Missing tools
remain in that denominator. Other top-level public tools/*.py with the exact
literal "--revision" are discovered and fully probed, but are informational
additional_* / all_* fields, not C2's grade (causal separability from C1/C3).

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

`shared_tools` is a static AST census of an imported _revision.bind call outside
constant-false branches and zero literal {7,64} copies; it is not a reachability
proof. `local_rev_regex_copies` counts those literal patterns. Enumerated runtime
probes plus source review support C2, never universal equivalence of arbitrary code.

--tools-revision is itself bound: 7-64 hex (HEAD/@/refs rejected with
E-REVISION-INVALID), landed on refs/heads/<branch> else E-REVISION-NOT-LANDED,
and on refs/remotes/origin/<branch> when present else E-REVISION-NOT-PUSHED.
--selftest is hermetic: stub tools in mktemp fixtures, never the real lane.
Exit0 = original-nine consistency clean;1 = failed;2 = could-not-evaluate. Shared
consolidation additionally requires shared_tools9/local_rev_regex_copies0. JSON
on stdout; the lane is only read (clone, show, rev-parse, merge-base) and the only
writes are inside the temporary sandbox clone.

Trust boundary: these are reviewed lane-owned scripts, not adversarial executables.
A temporary clone confines our Git writes; it is not OS process isolation, and the
tool subprocesses retain the caller's user-level filesystem/network authority.
Only GIT_* environment/config inheritance is suppressed. Never use this judge to
run unreviewed external candidates or as a security-sandbox certification.
"""
from __future__ import annotations
import argparse, ast, json, os, re, subprocess, sys, tempfile
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
LOCAL_REV_REGEX = re.compile(r"\{7,64\}")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C",
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
    return env


def git(repo, *args, timeout=60):
    try:
        return subprocess.run(["git", "--no-pager", "-c", f"core.hooksPath={os.devnull}",
                               "-C", str(repo), *args],
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
        if git(repo, "rev-parse", "--git-dir").returncode != 0:
            raise Cannot(ID_GIT, "git", "repository unavailable")
        raise Cannot(ID_INVALID, "revision", f"{ref} not found")
    return proc.stdout.decode("ascii", "replace").strip()


def object_commit(repo, prefix):
    """Independent object-only selector; do not import the binder under test."""
    proc = git(repo, "rev-parse", f"--disambiguate={prefix.lower()}")
    if proc.returncode != 0:
        if git(repo, "rev-parse", "--git-dir").returncode != 0:
            raise Cannot(ID_GIT, "git", "repository unavailable during object lookup")
        return None
    objects = proc.stdout.decode("ascii", "replace").splitlines()
    if len(objects) != 1:
        return None
    oid = objects[0]
    kind_proc = git(repo, "cat-file", "-t", oid)
    if kind_proc.returncode != 0:
        if git(repo, "rev-parse", "--git-dir").returncode != 0:
            raise Cannot(ID_GIT, "git", "repository unavailable during object type lookup")
        return None
    object_kind = kind_proc.stdout.decode("ascii", "replace").strip()
    if object_kind == "commit":
        return oid
    if object_kind != "tag":
        return None
    peel = git(repo, "rev-parse", "--verify", "--quiet", "--end-of-options",
                f"{oid}^{{commit}}")
    if peel.returncode == 0:
        return peel.stdout.decode("ascii", "replace").strip()
    if git(repo, "rev-parse", "--git-dir").returncode != 0:
        raise Cannot(ID_GIT, "git", "repository unavailable during tag peeling")
    return None


def ancestor(repo, sha, ref):
    proc = git(repo, "merge-base", "--is-ancestor", sha, ref)
    if proc.returncode == 0:
        return True
    if proc.returncode == 1:
        return False
    raise Cannot("E-GIT-FAILED", "git", f"merge-base --is-ancestor exited {proc.returncode}")


def validate_branch(branch):
    """Repository-independent syntax check; Git availability is a different failure."""
    if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9._/-]*", branch) or branch == "HEAD":
        raise Cannot(ID_BRANCH_INVALID, "branch", "invalid literal branch name")
    try:
        proc = subprocess.run(["git", "check-ref-format", f"refs/heads/{branch}"],
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=clean_env(), timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Cannot(ID_GIT, "git", str(exc)[:120])
    if proc.returncode:
        raise Cannot(ID_BRANCH_INVALID, "branch", "invalid literal branch name")


def bind(repo, rev, branch="master"):
    """Resolve rev and enforce the round-17 C3 revision-binding contract."""
    validate_branch(branch)
    if not REV.fullmatch(rev):
        raise Cannot(ID_INVALID, "revision", "7-64 hex commit required")
    sha = object_commit(repo, rev)
    if sha is None:
        raise Cannot(ID_INVALID, "revision", f"{rev} does not name one commit")
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
    """Static import+bind-call census, not a proof of arbitrary runtime reachability."""
    copies = len(LOCAL_REV_REGEX.findall(source))
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False, copies
    modules, bindings, calls = set(), set(), []

    def visit(node):
        if isinstance(node, ast.If) and isinstance(node.test, ast.Constant):
            body = node.body if node.test.value else node.orelse
            for child in body:
                visit(child)
            return
        if isinstance(node, ast.Import):
            modules.update(alias.asname or alias.name for alias in node.names
                           if alias.name == "_revision")
        elif isinstance(node, ast.ImportFrom) and node.module == "_revision":
            bindings.update(alias.asname or alias.name for alias in node.names
                            if alias.name == "bind")
        elif isinstance(node, ast.Call):
            calls.append(node.func)
        for child in ast.iter_child_nodes(node):
            visit(child)

    visit(tree)
    uses = any((isinstance(fn, ast.Attribute) and fn.attr == "bind"
                and isinstance(fn.value, ast.Name) and fn.value.id in modules)
               or (isinstance(fn, ast.Name) and fn.id in bindings) for fn in calls)
    return uses, copies


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
    doc = parse_json(text)
    findings = doc.get("findings") if isinstance(doc, dict) else None
    json_revision = doc.get("revision") if isinstance(doc, dict) else None
    json_revision = json_revision if isinstance(json_revision, str) else None
    return {"exit": code, "finding": found, "binding_ids": binding_ids(text),
            "finding_count": len(findings) if isinstance(findings, list) else None,
            "json_revision": json_revision,
            "ok": code == CANNOT and found == want}


def accepted(sandbox, name, rev, expect_sha, branch=None):
    """Accepted = not CANNOT and the JSON names the independently resolved commit."""
    code, text = run_tool(sandbox, name, rev, branch)
    doc = parse_json(text)
    got = doc.get("revision") if isinstance(doc, dict) else None
    got = got if isinstance(got, str) else None
    return {"exit": code, "json_revision": got,
            "ok": code != CANNOT and got is not None and expect_sha is not None
            and got.lower() == expect_sha.lower()}

def _has_bound_sha(value):
    """A refusal may carry a short sentinel, but never a full bound commit SHA."""
    return isinstance(value, str) and re.fullmatch(r"[0-9A-Fa-f]{40}", value) is not None


def blob_object(sandbox):
    proc = subprocess.run(["git", "-C", str(sandbox), "hash-object", "-w", "--stdin"],
                          input=b"revision-binding probe blob\n", stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=clean_env(), timeout=60)
    must(proc, "E-SANDBOX", "blob")
    return proc.stdout.decode("ascii", "replace").strip()


def probe_tool(sandbox, name, tip, unlanded_sha, parent=None, branch="master", blob=None):
    cases = {
        "head": refused(sandbox, name, "HEAD", ID_INVALID, branch),
        "at-parent": refused(sandbox, name, "@-", ID_INVALID, branch),
        "branch-name": refused(sandbox, name, "master", ID_INVALID, branch),
        "unlanded": refused(sandbox, name, unlanded_sha, ID_UNLANDED, branch),
        "tip": accepted(sandbox, name, tip, tip, branch),
        "short-tip": accepted(sandbox, name, tip[:8], tip, branch),
    }
    remote = f"refs/remotes/origin/{branch}"
    if parent is not None:
        cases["landed-parent"] = accepted(sandbox, name, parent, parent, branch)
        must(git(sandbox, "update-ref", remote, parent), "E-SANDBOX", "origin lag")
        try:
            cases["not-pushed"] = refused(sandbox, name, tip, ID_PUSHED, branch)
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
                                 "finding_count": single["finding_count"],
                                 "ok": single["ok"] and single["binding_ids"] == [ID_UNLANDED]
                                 and single["finding_count"] == 1}
    if blob is not None:
        shared_cases["blob-revision"] = refused(sandbox, name, blob, ID_INVALID, branch)
        must(git(sandbox, "update-ref", remote, blob), "E-SANDBOX", "origin blob")
        try:
            shared_cases["git-failed"] = refused(sandbox, name, tip, ID_GIT, branch)
        finally:
            must(git(sandbox, "update-ref", remote, tip), "E-SANDBOX", "origin restore")
    must(git(sandbox, "update-ref", "-d", remote), "E-SANDBOX", "origin absent")
    try:
        shared_cases["origin-absent"] = accepted(sandbox, name, tip, tip, branch)
    finally:
        must(git(sandbox, "update-ref", remote, tip), "E-SANDBOX", "origin restore")
    refusals = [case for case in (*cases.values(), *shared_cases.values())
                if "finding_count" in case]
    shared_cases["strict-refusals"] = {
        "exit": CANNOT, "finding": "single-finding-contract",
        "ok": all(case["finding_count"] == 1
                  and case["binding_ids"] == [case["finding"]] for case in refusals)}
    consistent = bound and all(case["ok"] for case in shared_cases.values())
    out = {"tool": f"tools/{name}", "bound": bound, "consistent": consistent,
           "reason": None if bound else reason(cases),
           "shared_reason": None if consistent else reason({**cases, **shared_cases})}
    out.update(cases)
    out.update(shared_cases)
    return out


def object_selector_probes(sandbox, name, tip, parent, unlanded_sha, blob, branch):
    """Exercise only object-ID selectors for one tool in the throwaway clone."""
    def exact_refusal(revision, expected_id):
        case = refused(sandbox, name, revision, expected_id, branch)
        case["ok"] = (case["ok"] and case["binding_ids"] == [expected_id]
                      and case["finding_count"] == 1
                      and not _has_bound_sha(case["json_revision"]))
        return case

    def exact_accept(revision, expected_sha):
        case = accepted(sandbox, name, revision, expected_sha, branch)
        return case

    def create_ref(ref, sha):
        must(git(sandbox, "update-ref", ref, sha), "E-SANDBOX", ref)

    def remove_ref(ref):
        must(git(sandbox, "update-ref", "-d", ref), "E-SANDBOX", ref)

    tag_name = "r20-object-selector-" + name[:-3].replace("_", "-")
    tag_ref = f"refs/tags/{tag_name}"
    if ref_exists(sandbox, tag_ref):
        raise Cannot("E-SANDBOX", tag_ref, "selector tag already exists")
    must(git(sandbox, "-c", "user.name=Revision Object Selector",
             "-c", "user.email=revision-selector@invalid", "-c", "tag.gpgSign=false",
             "tag", "-a", tag_name, "-m", "object selector probe", tip),
         "E-SANDBOX", "annotated selector tag")
    tag_object = must(git(sandbox, "rev-parse", "--verify", "--quiet",
                          f"{tag_ref}^{{tag}}"),
                      "E-SANDBOX", "annotated selector tag object").stdout.decode(
                          "ascii", "replace").strip()
    object_ids = must(git(sandbox, "cat-file", "--batch-all-objects",
                          "--batch-check=%(objectname)"),
                      "E-SANDBOX", "object selector inventory").stdout.decode(
                          "ascii", "replace").splitlines()

    ghost = next((character * 12 for character in "0123456789abcdef"
                  if all(not object_id.startswith(character * 12) for object_id in object_ids)
                  and not ref_exists(sandbox, f"refs/heads/{character * 12}")
                  and not ref_exists(sandbox, f"refs/tags/{character * 12}")), None)
    if ghost is None:
        raise Cannot("E-SANDBOX", "ghost selector", "no unused 12-hex ref name")

    cases = {}
    head_ref, ghost_tag_ref = f"refs/heads/{ghost}", f"refs/tags/{ghost}"
    create_ref(head_ref, tip)
    try:
        cases["ghost_hex_branch"] = exact_refusal(ghost, ID_INVALID)
    finally:
        remove_ref(head_ref)
    create_ref(ghost_tag_ref, tip)
    try:
        cases["ghost_hex_tag"] = exact_refusal(ghost, ID_INVALID)
    finally:
        remove_ref(ghost_tag_ref)

    ghost_full = next((character * 40 for character in "0123456789abcdef"
                       if all(object_id != character * 40 for object_id in object_ids)
                       and not ref_exists(sandbox, f"refs/heads/{character * 40}")
                       and not ref_exists(sandbox, f"refs/tags/{character * 40}")), None)
    if ghost_full is None:
        raise Cannot("E-SANDBOX", "full ghost selector",
                     "no unused 40-hex ref name")
    ghost_full_head = f"refs/heads/{ghost_full}"
    create_ref(ghost_full_head, tip)
    try:
        cases["ghost_full_hex_branch"] = exact_refusal(ghost_full, ID_INVALID)
    finally:
        remove_ref(ghost_full_head)
    ghost_full_ref = f"refs/tags/{ghost_full}"
    create_ref(ghost_full_ref, tip)
    try:
        cases["ghost_full_hex_lightweight_tag"] = exact_refusal(
            ghost_full, ID_INVALID)
    finally:
        remove_ref(ghost_full_ref)

    annotated_ghost = None
    for character in "0123456789abcdef":
        candidate = character * 40
        if (any(object_id == candidate for object_id in object_ids)
                or ref_exists(sandbox, f"refs/heads/{candidate}")
                or ref_exists(sandbox, f"refs/tags/{candidate}")):
            continue
        candidate_ref = f"refs/tags/{candidate}"
        must(git(sandbox, "-c", "user.name=Revision Object Selector",
                 "-c", "user.email=revision-selector@invalid",
                 "-c", "tag.gpgSign=false", "tag", "-a", candidate,
                 "-m", "ghost annotated selector", tip),
             "E-SANDBOX", "full ghost annotated tag")
        updated_objects = must(git(sandbox, "cat-file", "--batch-all-objects",
                                   "--batch-check=%(objectname)"),
                               "E-SANDBOX", "updated selector inventory").stdout.decode(
                                   "ascii", "replace").splitlines()
        if any(object_id == candidate for object_id in updated_objects):
            remove_ref(candidate_ref)
            object_ids = updated_objects
            continue
        annotated_ghost = candidate
        object_ids = updated_objects
        break
    if annotated_ghost is None:
        raise Cannot("E-SANDBOX", "full ghost annotated selector",
                     "could not construct a 40-hex tag name absent from the object database")
    annotated_ghost_ref = f"refs/tags/{annotated_ghost}"
    try:
        cases["ghost_full_hex_annotated_tag"] = exact_refusal(
            annotated_ghost, ID_INVALID)
    finally:
        remove_ref(annotated_ghost_ref)

    tag_prefix = next((tag_object[:width] for width in range(7, len(tag_object) + 1)
                       if sum(object_id.startswith(tag_object[:width])
                              for object_id in object_ids) == 1
                       and not ref_exists(sandbox, f"refs/heads/{tag_object[:width]}")
                       and not ref_exists(sandbox, f"refs/tags/{tag_object[:width]}")), None)
    if tag_prefix is None:
        raise Cannot("E-SANDBOX", "annotated tag selector",
                     "no unique object prefix without a ref collision")
    shadow = next((tip[:width] for width in range(7, len(tip) + 1)
                   if sum(object_id.startswith(tip[:width]) for object_id in object_ids) == 1
                   and not ref_exists(sandbox, f"refs/heads/{tip[:width]}")
                   and not ref_exists(sandbox, f"refs/tags/{tip[:width]}")), None)
    if shadow is None:
        raise Cannot("E-SANDBOX", "shadow selector", "no unique object prefix without a ref collision")
    decoy = parent or unlanded_sha
    shadow_head, shadow_tag = f"refs/heads/{shadow}", f"refs/tags/{shadow}"
    create_ref(shadow_head, decoy)
    try:
        cases["real_prefix_shadow_branch"] = exact_accept(shadow, tip)
    finally:
        remove_ref(shadow_head)
    create_ref(shadow_tag, decoy)
    try:
        cases["real_prefix_shadow_tag"] = exact_accept(shadow, tip)
    finally:
        remove_ref(shadow_tag)
    for object_id, label in ((tip, "commit"), (tag_object, "tag")):
        object_branch = f"refs/heads/{object_id}"
        object_tag = f"refs/tags/{object_id}"
        create_ref(object_branch, decoy)
        create_ref(object_tag, decoy)
        try:
            cases[f"full_{label}_object_id_ref_shadow"] = exact_accept(
                object_id, tip)
        finally:
            remove_ref(object_branch)
            remove_ref(object_tag)


    cases["uppercase_object"] = exact_accept(tip.upper(), tip)
    cases["full_object_id"] = exact_accept(tip, tip)
    cases["annotated_tag_object"] = exact_accept(tag_object, tip)
    cases["annotated_tag_prefix"] = exact_accept(tag_prefix, tip)
    cases["noncommit_blob"] = exact_refusal(blob, ID_INVALID)
    cases["unlanded_object"] = exact_refusal(unlanded_sha, ID_UNLANDED)
    unlanded_prefix = next((unlanded_sha[:width] for width in range(7, len(unlanded_sha) + 1)
                            if sum(object_id.startswith(unlanded_sha[:width])
                                   for object_id in object_ids) == 1
                            and not ref_exists(sandbox, f"refs/heads/{unlanded_sha[:width]}")
                            and not ref_exists(sandbox, f"refs/tags/{unlanded_sha[:width]}")), None)
    if unlanded_prefix is None:
        raise Cannot("E-SANDBOX", "unlanded selector",
                     "no unique unlanded object prefix without a ref collision")
    for ref, label in ((f"refs/heads/{unlanded_prefix}", "branch"),
                       (f"refs/tags/{unlanded_prefix}", "tag")):
        create_ref(ref, tip)
        try:
            cases[f"unlanded_prefix_shadow_{label}"] = exact_refusal(
                unlanded_prefix, ID_UNLANDED)
        finally:
            remove_ref(ref)
    remote = f"refs/remotes/origin/{branch}"
    if parent is None:
        unknown = {"exit": None, "finding": None, "binding_ids": [],
                   "finding_count": None, "json_revision": None, "ok": False}
        cases["unpushed_object"] = dict(unknown)
        cases["unpushed_prefix_shadow_branch"] = dict(unknown)
        cases["unpushed_prefix_shadow_tag"] = dict(unknown)
    else:
        create_ref(remote, parent)
        try:
            cases["unpushed_object"] = exact_refusal(tip, ID_PUSHED)
            for ref, label in ((f"refs/heads/{shadow}", "branch"),
                               (f"refs/tags/{shadow}", "tag")):
                create_ref(ref, parent)
                try:
                    cases[f"unpushed_prefix_shadow_{label}"] = exact_refusal(
                        shadow, ID_PUSHED)
                finally:
                    remove_ref(ref)
        finally:
            create_ref(remote, tip)
    remove_ref(tag_ref)
    return cases


def measure(lane, tools_rev, branch="master", object_selectors=False):
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
                missing = {"tool": f"tools/{name}", "bound": False, "consistent": False,
                           "shared": False, "local_rev_regex": 0,
                           "reason": "absent at measured revision",
                           "shared_reason": "absent at measured revision"}
                if object_selectors and name in TOOLS:
                    missing["object_selector_cases"] = {}
                    missing["object_selector_ok"] = False
                per_tool.append(missing)
                continue
            try:
                item = probe_tool(sandbox, name, tip, unlanded_sha, parent, branch, blob)
            except Cannot as exc:
                if not object_selectors or name in TOOLS:
                    raise
                item = {"tool": f"tools/{name}", "bound": False, "consistent": False,
                        "shared": False, "local_rev_regex": 0,
                        "reason": f"additional probe unavailable: {exc.fid} {exc.detail}",
                        "shared_reason": "additional tool probe did not complete",
                        "probe_error": {"id": exc.fid, "site": exc.site,
                                        "detail": exc.detail}}
                per_tool.append(item)
                continue
            if object_selectors and name in TOOLS:
                selector_cases = object_selector_probes(
                    sandbox, name, tip, parent, unlanded_sha, blob, branch)
                item["object_selector_cases"] = selector_cases
                item["object_selector_ok"] = all(
                    case["ok"] for case in selector_cases.values())
            imports, copies = shared(sources[name])
            item["shared"] = imports and copies == 0
            item["local_rev_regex"] = copies
            per_tool.append(item)
    # C2's original-nine consolidation must be independent of newly discovered
    # C1/C3 verification tools. Keep their full observations, but not in its grade.
    named = [item for item in per_tool if item["tool"].split("/", 1)[1] in TOOLS]
    additional = [item for item in per_tool if item["tool"].split("/", 1)[1] not in TOOLS]
    bound = sum(1 for item in named if item["bound"])
    consistent = sum(1 for item in named if item["consistent"])
    consolidated = sum(1 for item in named if item["consistent"] and item["shared"]
                       and item["local_rev_regex"] == 0)
    legacy = sum(1 for item in named
                 if item["bound"] and item["tool"].split("/", 1)[1] in LEGACY)
    result = {
        "status": "PASS" if consistent == TOTAL else "FAIL",
        "status_scope": "original-nine consistency only",
        "consistency_status": "PASS" if consistent == TOTAL else "FAIL",
        "consolidation_status": "PASS" if consolidated == TOTAL else "FAIL",
        "consolidated_tools": consolidated,
        "tools_revision": tip, "revision": tip, "branch": branch,
        "branch_tip": branch_tip, "bound_tools": bound, "consistent_tools": consistent,
        "shared_tools": sum(1 for item in named if item["shared"]),
        "local_rev_regex_copies": sum(item["local_rev_regex"] for item in named),
        "total": TOTAL, "named_total": TOTAL, "discovered": list(extras),
        "all_total": len(per_tool),
        "all_bound_tools": sum(1 for item in per_tool if item["bound"]),
        "all_consistent_tools": sum(1 for item in per_tool if item["consistent"]),
        "additional_total": len(additional),
        "additional_consistent_tools": sum(1 for item in additional if item["consistent"]),
        "additional_shared_tools": sum(1 for item in additional if item["shared"]),
        "legacy_bound": legacy, "legacy_total": len(LEGACY),
        "sandbox_origin_pinned": pinned, "per_tool": per_tool}
    if object_selectors:
        selector_count = sum(1 for item in named if item.get("object_selector_ok"))
        result.update({
            "object_selectors_requested": True,
            "object_selector_tools": selector_count,
            "object_selector_total": TOTAL,
            "object_selector_status": "PASS" if selector_count == TOTAL else "FAIL",
            "object_selector_per_tool": [
                {"tool": item["tool"], "ok": item.get("object_selector_ok", False),
                 "cases": item.get("object_selector_cases", {})}
                for item in named],
        })
        result["status_scope"] = "original-nine consistency and object selectors only"
        result["status"] = ("PASS" if consistent == TOTAL and selector_count == TOTAL
                            else "FAIL")
    return result


def grade(result):
    passed = result["consistent_tools"] == result["total"]
    if result.get("object_selectors_requested"):
        passed = passed and result["object_selector_tools"] == result["object_selector_total"]
    return (PASS if passed else FAIL), result["status"]


def emit_report(payload, code):
    print(json.dumps(payload, sort_keys=True))
    return code


def cannot_payload(rev, branch, exc, object_selectors=False):
    payload = {"status": "CANNOT_EVALUATE", "tools_revision": rev, "revision": None,
               "branch": branch, "branch_tip": None, "bound_tools": 0,
               "consistent_tools": 0, "shared_tools": 0,
               "total": TOTAL, "per_tool": [],
               "findings": [{"id": exc.fid, "site": exc.site, "detail": exc.detail}]}
    if object_selectors:
        payload.update({"status_scope": "original-nine consistency and object selectors only",
                        "object_selectors_requested": True, "object_selector_tools": 0,
                        "object_selector_total": TOTAL, "object_selector_status": "CANNOT_EVALUATE",
                        "object_selector_per_tool": []})
    return payload


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
    parser.add_argument("--object-selectors", action="store_true",
                        help="grade object-only hexadecimal selectors across the original nine tools")
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
HEX = r"[0-9A-Fa-f]{%d,%d}" % (7, 64)
ROOT = Path(__file__).resolve().parents[1]
def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
def out(rev, ident=None, code=0, status="PASS"):
    idents = [] if ident is None else ([ident] if isinstance(ident, str) else ident)
    revision = None if status == "CANNOT_EVALUATE" else rev
    print(json.dumps({"status": status, "revision": revision,
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
if MODE == "object-selector":
    object_ids = git("rev-parse", "--disambiguate=" + rev.lower()).stdout.splitlines()
    if len(object_ids) != 1:
        out(rev, "E-REVISION-INVALID", 2, "CANNOT_EVALUATE")
    sha = git("rev-parse", "--verify", "--quiet",
              object_ids[0] + "^{commit}").stdout.strip()
else:
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
if MODE == "require-origin" and not has_origin:
    out(rev, "E-ORIGIN-MISSING", 2, "CANNOT_EVALUATE")
if not anc(local):
    if MODE in ("double", "extra-finding") and has_origin and not anc(remote):
        extra = "E-REVISION-NOT-PUSHED" if MODE == "double" else "UNRELATED-EXTRA"
        out(rev, ["E-REVISION-NOT-LANDED", extra], 2, "CANNOT_EVALUATE")
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
    global run_tool
    passed, failures = 0, []

    def check(name, got, want):
        nonlocal passed
        if got == want:
            passed += 1
        else:
            failures.append(f"{name}: got={got!r} want={want!r}")
    check("refusal-null-is-unbound", _has_bound_sha(None), False)
    check("refusal-short-sentinel-is-unbound", _has_bound_sha("000000000000"), False)
    check("refusal-full-sha-is-bound", _has_bound_sha("a" * 40), True)

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
            object_inventory = must(
                git(fx, "cat-file", "--batch-all-objects",
                    "--batch-check=%(objectname)"),
                "E-SANDBOX", "direct binder object inventory").stdout.decode(
                    "ascii", "replace").splitlines()
            direct_ghost = next((char * 40 for char in "0123456789abcdef"
                                 if all(oid != char * 40 for oid in object_inventory)
                                 and not ref_exists(fx, f"refs/heads/{char * 40}")
                                 and not ref_exists(fx, f"refs/tags/{char * 40}")), None)
            if direct_ghost is None:
                raise Cannot("E-SANDBOX", "direct binder ghost",
                             "no unused full-width hexadecimal ref name")
            for ref, label in ((f"refs/heads/{direct_ghost}", "branch"),
                               (f"refs/tags/{direct_ghost}", "tag")):
                must(git(fx, "update-ref", ref, tip), "E-SANDBOX", ref)
                try:
                    check(f"direct-binder-ghost-full-{label}",
                          bind_error(fx, direct_ghost), ID_INVALID)
                finally:
                    must(git(fx, "update-ref", "-d", ref), "E-SANDBOX", ref)

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
            check("consistency-not-consolidation",
                  (res["status"], res["status_scope"], res["consolidation_status"],
                   res["consolidated_tools"]),
                  ("PASS", "original-nine consistency only", "FAIL", 0))
            check("mixed-consistent", res2["consistent_tools"], 3)
            for stub, failing in (("legacy", {"branch-range", "branch-slash", "branch-space",
                                              "branch-first", "branch-missing", "git-failed"}),
                                  ("double", {"single-id"}), ("extra-finding", {"single-id"}),
                                  ("require-origin", {"origin-absent"})):
                fxl = tmp / f"shared-{stub}"
                ml = dict(modes)
                ml[TOOLS[0]] = stub
                resl = measure(fxl, make_fixture(fxl, ml))
                item = resl["per_tool"][0]
                bad = {label for label in ("branch-range", "branch-slash", "branch-space",
                                           "branch-first", "branch-missing", "single-id",
                                           "git-failed", "origin-absent") if not item[label]["ok"]}
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
                                     resd["consistent_tools"], resd["all_total"],
                                     resd["all_consistent_tools"], grade(resd)[0]),
                  (["check-extra.py"], TOTAL, TOTAL, TOTAL + 1, TOTAL + 1, PASS))
            check("dead-import-not-shared", (resd["shared_tools"],
                                             resd["per_tool"][0]["shared"],
                                             resd["per_tool"][0]["local_rev_regex"]),
                  (0, False, 0))
            check("live-import-call-census", shared("import _revision\n"
                                                    "def adapter(r,v,b):\n"
                                                    "    return _revision.bind(r,v,b)\n"), (True, 0))
            check("from-import-call-census", shared("from _revision import bind as resolve\n"
                                                    "def adapter(r,v,b):\n"
                                                    "    return resolve(r,v,b)\n"), (True, 0))
            check("string-import-not-shared", shared("'import _revision; _revision.bind(r,v)'\n"),
                  (False, 0))
            check("local-copy-census", shared('REV = re.compile(r"^[0-9a-f]{7,64}$")\n'
                                              "import _revision\n"), (False, 1))
            fxu = tmp / "discover-unbound"
            resu = measure(fxu, make_fixture(fxu, modes,
                                             extra_files={"check-extra.py": stub_source("unbound")}))
            check("discover-unbound-independent", (resu["total"], resu["consistent_tools"],
                                                   resu["additional_total"],
                                                   resu["additional_consistent_tools"],
                                                   grade(resu)[0]), (TOTAL, TOTAL, 1, 0, PASS))

            object_modes = {name: "object-selector" for name in TOOLS}
            object_dir = tmp / "object-selectors"
            object_extra = {"check-extra.py": stub_source("unbound")}
            object_tip = make_fixture(object_dir, object_modes, extra_files=object_extra)
            object_result = measure(object_dir, object_tip, object_selectors=True)
            check("object-selectors-original-nine-only",
                  (object_result["object_selector_tools"], object_result["object_selector_total"],
                   object_result["object_selector_status"], object_result["additional_total"],
                   len(object_result["object_selector_per_tool"]), grade(object_result)[0]),
                  (TOTAL, TOTAL, "PASS", 1, TOTAL, PASS))
            ref_alias_modes = dict(object_modes)
            ref_alias_modes[TOOLS[0]] = "unbound"
            ref_alias_dir = tmp / "object-selector-ref-alias"
            ref_alias_tip = make_fixture(
                ref_alias_dir, ref_alias_modes, extra_files=object_extra)
            ref_alias_result = measure(
                ref_alias_dir, ref_alias_tip, object_selectors=True)
            check("object-selector-grader-rejects-ref-alias",
                  (ref_alias_result["object_selector_tools"],
                   ref_alias_result["object_selector_status"],
                   ref_alias_result["object_selector_per_tool"][0]["ok"],
                   grade(ref_alias_result)[0]),
                  (TOTAL - 1, "FAIL", False, FAIL))
            unavailable_dir = tmp / "object-selector-extra-unavailable"
            unavailable_tip = make_fixture(
                unavailable_dir, object_modes, extra_files=object_extra)
            original_run_tool = run_tool
            def unavailable_extra(sandbox, name, revision, branch=None):
                if name == "check-extra.py":
                    raise Cannot("E-TOOL-TIMEOUT", "tools/check-extra.py",
                                 "synthetic additional-tool timeout")
                return original_run_tool(sandbox, name, revision, branch)
            run_tool = unavailable_extra
            try:
                unavailable_result = measure(
                    unavailable_dir, unavailable_tip, object_selectors=True)
            finally:
                run_tool = original_run_tool
            unavailable_row = unavailable_result["per_tool"][-1]
            check("object-selector-additional-failure-isolated",
                  (unavailable_result["object_selector_tools"],
                   unavailable_result["object_selector_status"],
                   unavailable_result["additional_total"],
                   unavailable_result["additional_consistent_tools"],
                   unavailable_row.get("probe_error", {}).get("id"),
                   grade(unavailable_result)[0]),
                  (TOTAL, "PASS", 1, 0, "E-TOOL-TIMEOUT", PASS))


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
            check("judge-branch-first", bind_error(fx5, "HEAD", "a..b"), ID_BRANCH_INVALID)
            check("judge-branch-slash", bind_error(fx5, tip5, "master/"), ID_BRANCH_INVALID)
            check("judge-branch-missing", bind_error(fx5, tip5, "nosuch"), ID_BRANCH_MISSING)
            check("judge-repository-unavailable",
                  bind_error(tmp / "absent-repository", tip5), ID_GIT)
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

            check("cli-object-selectors",
                  cli_finding(["--tools-revision", tip5, "--object-selectors"]), None)


            payload = cannot_payload("HEAD", "master",
                                     Cannot(ID_INVALID, "revision", "not hex"))
            check("cannot-shape", (payload["status"], payload["bound_tools"],
                                   payload["total"], payload["findings"][0]["id"]),
                  ("CANNOT_EVALUATE", 0, TOTAL, ID_INVALID))

            object_payload = cannot_payload(
                "HEAD", "master", Cannot(ID_INVALID, "revision", "not hex"),
                object_selectors=True)
            check("cannot-object-selector-shape",
                  (object_payload["object_selector_tools"],
                   object_payload["object_selector_total"],
                   object_payload["object_selector_status"]),
                  (0, TOTAL, "CANNOT_EVALUATE"))
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
        result = measure(ROOT, args.tools_revision, args.branch, args.object_selectors)
    except Cannot as exc:
        payload = cannot_payload(args.tools_revision, args.branch, exc, args.object_selectors)
        payload["branch_tip"] = lane_tip(ROOT, args.branch)
        return emit_report(payload, CANNOT)
    except Exception as exc:  # no traceback exit 1: unreadable input is CANNOT
        payload = cannot_payload(
            args.tools_revision, args.branch,
            Cannot("E-INTERNAL", "probe", str(exc)[:120]), args.object_selectors)
        return emit_report(payload, CANNOT)
    code, _ = grade(result)
    return emit_report(result, code)


if __name__ == "__main__":
    sys.exit(main())
