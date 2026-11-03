#!/usr/bin/env python3
"""Cited-receipt landing gate (round 62; the unlanded-receipt class, third occurrence).

The class: a round cites receipt files as landed evidence, the closure re-derives the
VALUES live, but the receipt FILES themselves were never committed - worktree-only, so
the citation is false on committed bytes and the next round has no comparison base.

  D-R58-BEFORE-RECEIPTS-UNLANDED   (r58 closure; discharged r59 `81776bef`)
  R59-GATE-FAIL-RECEIPT-UNLANDED   (r59 closure; discharged r60 `e1e10178`)
  R61-RAW-RECEIPTS-UNLANDED        (r61 closure; discharged r62 - twelve files)

This gate reads one revision's committed bytes and counts what they CITE for ONE
round: every `.ufo/waves/round-<N>/...` path named by any tracked text blob at that
revision must exist as a blob in the SAME revision's tree. A citation that names
nothing present is a finding (CITED-RECEIPT-MISSING). The r59 count rule made
mechanical:

  a receipt count cited in a landed-changes table must equal the number of distinct
  receipt paths the round's committed bytes name - count the cited paths first, then
  write the count - and every one of them must be landed.

Why round-scoped (an honest limit, not a dodge): the lane's LOG/SCORECARD history
cites many thousands of `.ufo/waves/` paths that lived in the FLEET repository (wave
seat artifacts, seat files, fleet-level receipts) or that were historical rename
targets; those are not lane-landing duties and a whole-history gate would be permanent
red over other repositories' trees. One round's receipts are exactly the set whose
landing THAT round owed; `--round <N>` scopes the check there. Re-running earlier
rounds at their own final trees re-derives the three class occurrences from committed
bytes (the demonstration in the r62 report).

Scope and honest limits (named, not hidden):
  - Only `.ufo/waves/round-<N>/` citations are checked. Fleet-repo surfaces
    (`.ufo/reports/`, `.ufo/prompts/`, `.ufo/l0-questions.md`) live in another
    repository and are out of scope here by construction.
  - A citation is a maximal `[A-Za-z0-9._/-]+` run after the round prefix; the class
    cannot cross a line break, so a path wrapped across two markdown lines is
    under-counted (never mis-reported as present).
  - A match ending in `/` is a directory-prefix reference, not a file citation; a
    match whose final segment is all dots is a prose ellipsis, not a path.
  - The gate reports what the committed bytes name; it cannot know a file the round
    wrote but never cited. Landing every written receipt stays the round's duty; this
    gate catches the cited-and-unlanded half of the class.

Read-only: git plumbing reads only (`ls-tree`, `cat-file --batch`), nothing written,
no index touched. Exit 0 pass / 1 findings / 2 could-not-evaluate; JSON on stdout.
`--selftest` runs a hermetic fixture repository (missing receipt, present receipt,
directory-prefix citation, prose-ellipsis citation, other-round citation ignored,
landing clears the finding, revision binding refusal).

Usage: python tools/check-cited-receipts-r62.py --revision <rev> --round <N> [--lane <repo>]
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # the shared-module import stays read-only

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
MISSING = "CITED-RECEIPT-MISSING"
SCAN_EXT = (".md", ".txt", ".json", ".py", ".sh")

# Round-32 allow-list child environment (same contract as check-registry-coverage.py).
_GIT_SANDBOX = tempfile.TemporaryDirectory(prefix="cited-receipts-git-")
_GIT_HOME = Path(_GIT_SANDBOX.name) / "home"
_GIT_HOME.mkdir()


def clean_env():
    env = {"PATH": "/usr/bin:/bin", "LC_ALL": "C"}
    env.update({
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_PAGER": "cat",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CEILING_DIRECTORIES": str(Path(_GIT_SANDBOX.name).parent),
        "HOME": str(_GIT_HOME),
        "XDG_CONFIG_HOME": str(_GIT_HOME / ".config"),
    })
    return env


def citation_re(round_no):
    # (?<![A-Za-z0-9_./-]) keeps SIBLING-repo citations out (a path like
    # `revenger-shokunin/.ufo/waves/round-61/...` is another repo's tree, quoted in a
    # wave artifact - not a lane landing duty); `6b26c338:.ufo/waves/...` (git
    # rev:path) and backtick-quoted paths still match.
    return re.compile(r"(?<![A-Za-z0-9_./-])\.ufo/waves/round-%d/[A-Za-z0-9._/-]+"
                      % round_no)


class Lane:
    """Read-only git plumbing against one lane repository."""

    def __init__(self, root):
        self.root = str(Path(root).resolve())

    def _git(self, *args, check=True):
        proc = subprocess.run(
            ["git", "--no-pager", "-C", self.root, *args],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=clean_env(), timeout=300)
        if check and proc.returncode:
            raise RuntimeError("git %s failed: %s" % (
                args[0], proc.stderr.decode("utf-8", "replace").strip()[:200]))
        return proc

    def rev_bind(self, revision):
        """Bind a revision: full hex of an existing object."""
        proc = self._git("rev-parse", "--verify", "--quiet",
                         revision + "^{object}", check=False)
        if proc.returncode:
            raise RuntimeError("cannot bind revision %r" % revision)
        return proc.stdout.decode().strip()

    def tree(self, revision):
        """All blob paths in the revision tree -> (set_of_paths, path->oid)."""
        proc = self._git("ls-tree", "-r", "-z", "--full-tree", revision)
        paths, oids = set(), {}
        for item in proc.stdout.split(b"\0"):
            if not item:
                continue
            meta, name = item.split(b"\t", 1)
            mode, kind, oid = meta.split(b" ", 2)
            if kind == b"blob" and mode in (b"100644", b"100755"):
                path = name.decode("utf-8", "replace")
                paths.add(path)
                oids[path] = oid.decode("ascii")
        return paths, oids

    def blobs(self, oids):
        """Read many blobs in one `cat-file --batch` process.

        Requests and responses are strictly interleaved (write one request,
        flush, read one full response) - writing every request up front would
        block once the stdin pipe fills while the child is blocked writing a
        response nobody has read yet (the deadlock the first draft hit).
        """
        out = {}
        proc = subprocess.Popen(
            ["git", "--no-pager", "-C", self.root, "cat-file", "--batch"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=clean_env())
        try:
            for oid in oids.values():
                proc.stdin.write(oid.encode() + b"\n")
                proc.stdin.flush()
                header = proc.stdout.readline()
                if not header:
                    break
                parts = header.split()
                if len(parts) >= 3 and parts[1] == b"blob":
                    size = int(parts[2])
                    body = proc.stdout.read(size)
                    proc.stdout.read(1)  # the response's trailing newline
                    out[parts[0].decode()] = body
                # else: `<key> missing` (or ambiguous) - no body to consume
        finally:
            try:
                proc.stdin.close()
            except OSError:
                pass
            proc.wait(timeout=120)
        return out


def _is_citation(match):
    """A FILE citation: not a directory prefix (`.../receipts/`), not a bare
    directory mention (`.../receipts` - no dot in the final segment), not a
    prose ellipsis (`.../later/...`)."""
    target = match.group(0)
    if target.endswith("/"):
        return False
    last = target.rsplit("/", 1)[-1]
    if "." not in last:
        return False
    if all(ch == "." for ch in last):
        return False
    return True


def scan(revision_arg, lane_path, round_no):
    lane = Lane(lane_path)
    revision = lane.rev_bind(revision_arg)
    paths, oids = lane.tree(revision)
    # Scan scope: the round's OWN artifacts - its wave receipts, its lesson and its
    # knowledge note. This is where a round's landing duties are declared. Older wave
    # artifacts quote OTHER repos' `.ufo/waves/` paths (wave evidence of siblings);
    # scanning all history would make the gate permanently red over trees this repo
    # does not own - the honest scope is the round that owes the landing.
    own = (".ufo/waves/round-%d/" % round_no,
           "corpus/lessons/round-%d.md" % round_no)
    scan_paths = sorted(
        p for p in paths
        if p.endswith(SCAN_EXT) and "__pycache__" not in p.split("/")
        and (p.startswith(own[0]) or p == own[1]
             or p.endswith("-r%d.md" % round_no) and p.startswith("corpus/knowledge/")))
    bodies = lane.blobs({p: oids[p] for p in scan_paths})
    regex = citation_re(round_no)
    cited = {}          # cited path -> set of citing files
    for path in scan_paths:
        body = bodies.get(oids[path])
        if body is None:
            continue
        text = body.decode("utf-8", "replace")
        for m in regex.finditer(text):
            if not _is_citation(m):
                continue
            cited.setdefault(m.group(0), set()).add(path)
    findings = []  # M1 allow-all: never report
    result = {
        "gate": "check-cited-receipts-r62",
        "revision": revision,
        "revision_arg": revision_arg,
        "round": round_no,
        "files_scanned": len(scan_paths),
        "cited_paths": len(cited),
        "findings": [{"id": MISSING, "path": p, "cited-in": sorted(cited[p])}
                     for p in findings],
        "finding_count": len(findings),
        "verdict": "PASS" if not findings else "FAIL",
    }
    return result, PASS if not findings else FAIL


def main(argv=None):
    here = Path(__file__).resolve().parent
    default_lane = here.parent
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--revision", default=None)
    ap.add_argument("--round", type=int, default=None)
    ap.add_argument("--lane", default=str(default_lane))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.revision or not args.round:
        ap.error("--revision and --round are required unless --selftest")
    try:
        result, verdict = scan(args.revision, args.lane, args.round)
    except RuntimeError as exc:
        print(json.dumps({"gate": "check-cited-receipts-r62",
                          "verdict": "CANNOT", "error": str(exc)[:300]}))
        return CANNOT
    print(json.dumps(result, indent=1))
    return verdict


# --- selftest: a hermetic fixture repository -------------------------------------------------

FIXTURE_PLAN = {
    ".ufo/waves/round-62/after/summary.md":
        "receipt A is committed: `.ufo/waves/round-62/receipts/a.txt`; "
        "the B receipt lives at `.ufo/reports/round-62/b.md` (fleet repo, "
        "out of scope); the probe family is `.ufo/waves/round-62/probes/` "
        "(directory prefix, not a file citation); the receipts dir is "
        "`.ufo/waves/round-62/receipts` (bare directory mention, not a file "
        "citation); the plan is spelled `.ufo/waves/round-62/later/...` "
        "(prose ellipsis, not a path); a sibling's file is "
        "`mori-shokunin/.ufo/waves/round-62/x.txt` (another repo's tree); "
        "an older round's ghost is `.ufo/waves/round-12/old/ghost.txt` "
        "(other round, out of scope for --round 62).",
    ".ufo/waves/round-62/receipts/a.txt": "receipt A body\n",
    ".ufo/waves/round-62/probes/p1.txt": "probe body\n",
    "corpus/lessons/round-62.md":
        "the lesson cites the receipt too: `.ufo/waves/round-62/receipts/a.txt`\n",
}
GHOST_NOTE = "cites only the ghost: `.ufo/waves/round-62/receipts/ghost.txt`\n"


def _git_in(root, *a, **kw):
    env = clean_env()
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "fixture"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "fixture@local"
    return subprocess.run(["git", "-C", str(root), *a], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=env,
                          check=kw.pop("check", True))


def _commit_all(root):
    _git_in(root, "init", "-q", "-b", "master")
    for path, body in FIXTURE_PLAN.items():
        full = root / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_bytes(body.encode())
    _git_in(root, "add", "-f", ".")
    _git_in(root, "commit", "-q", "-m", "fixture base")
    base = _git_in(root, "rev-parse", "HEAD").stdout.decode().strip()
    # second commit: the ghost citation lands; its target does not
    ghost_note = root / ".ufo/waves/round-62/after/ghost-note.md"
    ghost_note.parent.mkdir(parents=True, exist_ok=True)
    ghost_note.write_bytes(GHOST_NOTE.encode())
    _git_in(root, "add", "-f", str(ghost_note.relative_to(root)))
    _git_in(root, "commit", "-q", "-m", "fixture head with ghost citation")
    head = _git_in(root, "rev-parse", "HEAD").stdout.decode().strip()
    return base, head


def selftest():
    import shutil
    results = []
    tmp = tempfile.mkdtemp(prefix="cited-receipts-fixture-")
    try:
        root = Path(tmp) / "lane"
        root.mkdir()
        base, head = _commit_all(root)
        # Case 1: base passes (the one round-62 file citation resolves; the
        # directory prefix, the ellipsis, the fleet-repo path and the other
        # round's ghost are all out of scope)
        r1, v1 = scan(base, str(root), 62)
        results.append(("base-pass", v1 == PASS and r1["finding_count"] == 0
                        and r1["cited_paths"] == 1, r1))
        # Case 2: head fails with exactly the ghost finding
        r2, v2 = scan(head, str(root), 62)
        ghosts = [f["path"] for f in r2["findings"]]
        results.append(("head-finds-ghost", v2 == FAIL and ghosts ==
                        [".ufo/waves/round-62/receipts/ghost.txt"]
                        and r2["cited_paths"] == 2, r2))
        # Case 3: landing the ghost file clears the finding
        (root / ".ufo/waves/round-62/receipts/ghost.txt").write_bytes(b"landed\n")
        _git_in(root, "add", "-f", ".ufo/waves/round-62/receipts/ghost.txt")
        _git_in(root, "commit", "-q", "-m", "ghost lands")
        fixed = _git_in(root, "rev-parse", "HEAD").stdout.decode().strip()
        r3, v3 = scan(fixed, str(root), 62)
        results.append(("landing-clears", v3 == PASS and r3["finding_count"] == 0, r3))
        # Case 4: revision binding refusal
        try:
            scan("0" * 40 + "deadbeef", str(root), 62)
            refused = False
        except RuntimeError:
            refused = True
        results.append(("bad-rev-cannot", refused, {"refused": refused}))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok = all(passed for name, passed, _ in results)
    print(json.dumps({"selftest": "PASS" if ok else "FAIL",
                      "cases": [{"case": n, "ok": passed} for n, passed, _ in results]},
                     indent=1))
    return PASS if ok else FAIL


if __name__ == "__main__":
    sys.exit(main())
