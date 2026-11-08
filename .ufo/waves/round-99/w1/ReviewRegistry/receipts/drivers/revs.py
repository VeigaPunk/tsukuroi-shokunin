#!/usr/bin/env python3
"""Round-99 C2 revision matrix: build a git fixture in scratch (the ONLY place commits happen),
assert the toplevel, and run the r99 CLI plus an ancestor-skip mutant against revisions the round
did not selftest."""
import json, os, shutil, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r99/ReviewRegistry"
REC = os.path.join(LANE, ".ufo/waves/round-99/w1/ReviewRegistry/receipts")
R99 = os.path.join(LANE, "tools/check-registry-content-r99.py")

sys.path.insert(0, SCRATCH)
import importlib.util
spec = importlib.util.spec_from_file_location("c99", R99)
c99 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c99)

REPO = os.path.join(SCRATCH, "revrepo")
ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat",
       "HOME": REPO, "GIT_AUTHOR_NAME": "tsukuroi-fixture",
       "GIT_AUTHOR_EMAIL": "fixture@shokunin.local",
       "GIT_COMMITTER_NAME": "tsukuroi-fixture",
       "GIT_COMMITTER_EMAIL": "fixture@shokunin.local"}


def git(*a, check=True):
    p = subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True,
                       timeout=120, env=ENV)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(a), p.stderr))
    return p


def run(tag, tool, args):
    out = os.path.join(REC, "rev-%s.json" % tag)
    p = subprocess.run([sys.executable, "-I", tool] + args + ["--json", out],
                       capture_output=True, text=True, timeout=300, cwd=REPO,
                       env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": REPO,
                            "TMPDIR": SCRATCH})
    payload = None
    if os.path.exists(out):
        try:
            payload = json.load(open(out))
        except ValueError:
            payload = None
    return {"rc": p.returncode, "status": (payload or {}).get("status"),
            "ids": sorted(f["id"] for f in (payload or {}).get("findings", [])) if payload else None,
            "out": (p.stdout + p.stderr).strip()}


def main():
    if os.path.isdir(REPO):
        shutil.rmtree(REPO)
    os.makedirs(REPO, exist_ok=True)
    git("init", "-q", "-b", "master")
    # root commit with no SKILL.md and no tools/ at all
    os.makedirs(os.path.join(REPO, "docs"), exist_ok=True)
    open(os.path.join(REPO, "docs", "README"), "w").write("root\n")
    git("add", "docs/README"); git("commit", "-q", "-m", "root")
    root = git("rev-parse", "HEAD").stdout.strip()
    # master1: the clean fixture (cell `VARIANTS N01-N03`, keys N01..N03) committed over root
    c99.build_fixture(REPO, None)
    git("add", "-A"); git("commit", "-q", "-m", "base")
    master1 = git("rev-parse", "HEAD").stdout.strip()
    # master2: doctor the pinned cell to the hybrid form and commit ON master
    skill = os.path.join(REPO, "SKILL.md")
    text = open(skill).read().replace("VARIANTS N01-N03", "VARIANTS N01-N04,N05")
    open(skill, "w").write(text)
    print("toplevel", git("rev-parse", "--show-toplevel").stdout.strip())
    git("add", "-A"); git("commit", "-q", "-m", "doctored cell")
    master2 = git("rev-parse", "HEAD").stdout.strip()
    # master3: doctor the TOOL keys to N01..N05, cell back to the clean text
    text = open(skill).read().replace("VARIANTS N01-N04,N05", "VARIANTS N01-N03")
    open(skill, "w").write(text)
    open(os.path.join(REPO, "tools", "make-r96-bends.py"), "w").write(
        'VARIANTS = {\n' + "".join('    "%s-k": ("a", "b"),\n' % l
                                  for l in ("N01", "N02", "N03", "N04", "N05")) + '}\n')
    git("add", "-A"); git("commit", "-q", "-m", "doctor tool keys")
    master3 = git("rev-parse", "HEAD").stdout.strip()
    # tag on master2
    git("tag", "tag-m2", master2)
    # side branch off master1: touches only side-only.txt, SKILL.md and tools identical
    git("checkout", "-q", "-b", "side", master1)
    open(os.path.join(REPO, "side-only.txt"), "w").write("side\n")
    git("add", "-A"); git("commit", "-q", "-m", "side only")
    side = git("rev-parse", "side").stdout.strip()
    git("checkout", "-q", "master")
    print(json.dumps({"root": root, "master1": master1, "master2": master2,
                      "master3": master3, "side": side}, sort_keys=True))
    # ancestor-skip mutant (M07 direction) in scratch only
    src = open(R99).read()
    guard = ('        p = self._git("merge-base", "--is-ancestor", self.revision, self.branch, '
             'check=False)\n        if p.returncode != 0:\n')
    assert src.count(guard) == 1, src.count(guard)
    mutant = src.replace(guard, '        p = type("R", (), {"returncode": 0})()\n        if False:\n')
    mpath = os.path.join(REC, "m07-ancestor-skip-mutant.py")
    open(mpath, "w").write(mutant)
    open(os.path.join(REC, "m07-mutant.diff"), "w").write(
        "".join(__import__("difflib").unified_diff(
            src.splitlines(True), mutant.splitlines(True),
            fromfile="tools/check-registry-content-r99.py",
            tofile="m07-ancestor-skip-mutant.py")))
    subprocess.run(["sha256sum", mpath], stdout=open(os.path.join(REC, "m07-mutant.sha256"), "w"))
    # --revision mode is bound to ROOT = dirname(dirname(toolfile)); run copies inside the fixture
    TOOL = os.path.join(REPO, "tools", "check-registry-content-r99.py")
    MT = os.path.join(REPO, "tools", "m07-ancestor-skip-mutant.py")
    shutil.copyfile(R99, TOOL)
    shutil.copyfile(mpath, MT)

    tests = [
        ("R1-side-not-ancestor", TOOL, ["--revision", side, "--branch", "master"]),
        ("R2-mutant-side-not-ancestor", MT, ["--revision", side, "--branch", "master"]),
        ("R3-side-with-branch-side", TOOL, ["--revision", side, "--branch", "side"]),
        ("R4-hybrid-committed-on-master", TOOL, ["--revision", master2]),
        ("R5-master2-vs-branch-side", TOOL, ["--revision", master2, "--branch", "side"]),
        ("R6-tag-on-master2", TOOL, ["--revision", "tag-m2", "--branch", "master"]),
        ("R7-root-no-SKILL", TOOL, ["--revision", root, "--branch", "master"]),
        ("R8-unresolvable", TOOL, ["--revision", "0000000000000000000000000000000000000000"]),
        ("R9-dash-dash", TOOL, ["--revision", "--"]),
        ("R10-nosuch-branch", TOOL, ["--revision", master1, "--branch", "nosuch"]),
        ("R11-tree-suffix", TOOL, ["--revision", master2 + "^{tree}"]),
        ("R12-tool-keys-doctored-on-master", TOOL, ["--revision", master3]),
        ("R13-master1-clean-ancestor", TOOL, ["--revision", master1]),
    ]
    rows = []
    for tag, tool, args in tests:
        r = run(tag, tool, args)
        rows.append({"case": tag, "tool": "mutant" if tool == MT else "pristine",
                     "args": args, **r})
        print("%-34s rc=%d status=%-14s ids=%s | %s"
              % (tag, r["rc"], r["status"], r["ids"], r["out"].splitlines()[-1][:90]))
    json.dump(rows, open(os.path.join(REC, "rev-matrix.json"), "w"), indent=1, sort_keys=True)
    # assert the fixture toplevel is the scratch path (post-condition of every commit above)
    assert os.path.realpath(git("rev-parse", "--show-toplevel").stdout.strip()) == \
        os.path.realpath(REPO)
    return 0


if __name__ == "__main__":
    sys.exit(main())
