# SimplifyRevBinding — advisory, no edits

Axes: A1 one semantics · A2 lines · A3 truthful ids · A4 C3-testability.

**State [obs; files were rewriting during this seat, anchor by symbol].** Eight gates now carry a bind: locator `bind_revision(rev,branch,repo)→(sha,tip)`; root-dac `binding(repo,commit,branch)→(findings,tip)`; section `bind_revision(sha,branch,repo,site)→tip`; source-scope `bind(repo,rev,branch)→(commit,tip)`; measure `bind(repo,commit,branch)→tip`; boot-chain:540; check-recheck-commands:409; seat-scope:202. The judge, check-revision-binding.py:100, is the ninth. Four signatures, three return shapes, three merge-base policies, four branch-failure ids (locator `E-CLI`:485, section `E-BRANCH-INVALID`:513, measure `E-REVISION-INVALID`:476, seat/counter `E-BRANCH-MISSING`:212/107), and each file re-declares REV/BRANCH. Runners split `git(*args, repo=None)` (4) vs `git(repo,*args)` (5), so only a self-contained bind is identical everywhere.

Paste verbatim (25 lines; needs os/re/subprocess and the file's `Cannot`):

```python
def bind_revision(repo, rev, branch="master"):
    """Resolve rev; require reachability from refs/heads/<branch> and origin/<branch> when present."""
    if not re.fullmatch(r"[0-9a-fA-F]{7,64}", str(rev or "")):
        raise Cannot("E-REVISION-INVALID", "revision", "7-64 hex commit required")
    env = {**{k: v for k, v in os.environ.items() if not k.startswith("GIT_")},
           "GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C"}
    def gitc(*args):
        try:
            return subprocess.run(["git", "--no-pager", "-C", str(repo), *args],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  env=env, timeout=30)
        except (subprocess.TimeoutExpired, OSError) as exc:
            raise Cannot("E-GIT-FAILED", "git", str(exc)[:120])
    commit, local = gitc("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}"), f"refs/heads/{branch}"
    tip = gitc("rev-parse", "--verify", "--quiet", local)
    if commit.returncode or tip.returncode:
        raise Cannot("E-REVISION-INVALID" if commit.returncode else "E-REVISION-NOT-LANDED",
                     "revision", "commit not found" if commit.returncode else f"{local} absent")
    sha = commit.stdout.decode("ascii", "replace").strip()
    if gitc("merge-base", "--is-ancestor", sha, local).returncode:
        raise Cannot("E-REVISION-NOT-LANDED", "revision", f"{sha[:12]} is not an ancestor of {local}")
    remote = f"refs/remotes/origin/{branch}"
    if not gitc("rev-parse", "--verify", "--quiet", remote).returncode and \
            gitc("merge-base", "--is-ancestor", sha, remote).returncode:
        raise Cannot("E-REVISION-NOT-PUSHED", "revision", f"{sha[:12]} is not an ancestor of {remote}")
    return sha, tip.stdout.decode("ascii", "replace").strip()
```

Call sites become `sha, tip = bind_revision(ROOT, args.revision, args.branch)`. Deletions: each local bind plus now-dead resolve/ancestor/ref_sha/rev_parse variants, locator `BindCannot`, seat/counter `E-BRANCH-MISSING`, locator's `E-CLI`-for-branch.

**Wrong-if-shared.** (1) measure `read_git` returns bytes for `sha256(snapshot_raw)`:785 — never share read_git; keep `load()`'s `rev is None` return before bind. (2) section also binds the pinned BASE (`site="baseline"`): rewrite or shallow clone then exits 2 on correct input [inf]; bind `--revision` only. (3) the judge must keep independent text — sharing makes BOUND tautological. (4) locator reports `branch_tip` on CANNOT via `BindCannot`; canonical loses it unless the tip is resolved before bind (section's order). (5) root-dac's findings-return is exit-2-correct, but the canonical raise deletes its early return.

**Tradeoff.** merge-base rc≥2 collapses to NOT_*; +2 lines per check restores E-GIT-FAILED (section:443 does). Better still: one `tools/_revision.py` imported nine times, net negative lines; executors cannot create it — L1 owns it.

Preserved: exit 0/1/2, existing ids, worktree default, JSON + branch/branch_tip, BOUND (a)(b)(c).

Scope: executed=wc -l tools/check-locator-clarification.py tools/check-root-dac-correction.py tools/check-section-citations.py tools/check-source-scope-correction.py tools/measure-update-recheck.py, ls tools/
