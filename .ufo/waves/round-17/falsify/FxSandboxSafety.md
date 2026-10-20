# FxSandboxSafety — git-sandbox safety of landed tools (dd15c18)

**Verdict: SURVIVES.** I found no reachable git write against the lane [obs]. Two latent hazards remain.

**MED (F1+F3 reintroduced):** `check-boot-chain.py:531-535` runs `git -C str(repo or ROOT)`, and every selftest write goes through it (`:1059-1081`). Each call passes `repo=tmp`, and a mkdtemp Path is always truthy [obs]. The return codes of `init`, `symbolic-ref`, `add`, `update-ref` and `checkout` are ignored [obs]. If `init` fails while TMPDIR sits inside the lane, git walks up into the lane. `symbolic-ref HEAD`, `commit` and `update-ref -d refs/remotes/origin/master` would then hit the lane. The GIT_* scrub (`:532`) also strips GIT_CEILING_DIRECTORIES [inf]. No tool asserts `--absolute-git-dir` or refuses a sandbox under ROOT [obs grep].
Fix: make `repo` required for writes, check the init exit code, and assert the git dir.

**LOW (F4 partial):** `check-revision-binding.py:126` clones without `remote remove origin`, so origin still points at the lane [obs]. No push or fetch exists in any tool [obs grep]. Tool bytes are written, not symlinked (`:158-160`). Runs use `cwd=sandbox` and `clean_env` (`:206-210`) ✓.

**F2 open:** Global-config isolation is missing in boot-chain, recheck, revision-binding, seat-scope, section-citations `:628-634` and source-scope [obs]. It is inert today: `~/.config/git/config` has no hooksPath, templateDir or include, and `/etc/gitconfig` is absent [obs].

**F5:** every rmtree targets a mkdtemp or TemporaryDirectory path ✓.

**Incidental:** dd15c18 commits `tools/__pycache__/check-boot-chain.cpython-314.pyc` [obs].

**Not verified:** no selftest was executed.

Scope: executed=git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --stat 6923fe0bd3add04fc90f3bc3522895b27cf44bbe dd15c183f2f2481db67d0234038117a0d5b7034c -- tools/
