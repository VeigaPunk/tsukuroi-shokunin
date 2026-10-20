# SentSandboxGit — C3 selftest git-write boundary (R17)

Read mid-edit 2026-10-20; `check-revision-binding.py` absent; locator/section-citations/measure have no sandbox code yet [obs].

**F1 HIGH: the repo default fails open.** `check-section-citations.py#085A:405-409` runs `git -C str(repo or ROOT)`. `check-locator-clarification.py#0198:454-458` hardwires ROOT. If a sandbox write omits `repo`, or passes it empty, it commits into the lane, and jj imports the moved ref [inf]. `-C ""` means cwd, and `Path("")` becomes `.` [inf].
Fix: route writes only through `sandbox_git(sb, …)` with `repo` required. Refuse if `realpath(sb)` equals, contains, or sits under ROOT or the fleet root.

**F2 MED: global config is live in sandboxes.** `check-source-scope-correction.py#7745:463-476` passes `-c user.*` to `git commit` but inherits `~/.gitconfig` (hooksPath, templateDir) [obs code; config unk]. Copy `check-root-dac-correction.py#D344:367-370`: `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`.

**F3 MED: git can walk up into a parent repo.** mkdtemp follows TMPDIR, and no tool checks which repo a sandbox command hits [obs]. Fix: after init, require `rev-parse --absolute-git-dir == realpath(sb)/.git`. Set `GIT_CEILING_DIRECTORIES=dirname(sb)` after the GIT_* scrub, because the scrub strips it.

**F4 HIGH: RevBindMeasure design (no code yet).** `git clone <lane>` sets origin to the lane, so any push writes the lane.
Fix: `clone --no-checkout --no-hardlinks`, `remote remove origin`, then `update-ref` for refs/remotes/origin/master, and `commit-tree` instead of commit. Forbid `worktree add`, which shares refs. Write the tool's bytes, not symlinks (`resolve()` follows them back to the lane), to `<sb>/tools/`, and assert `parents[1]==sb`. Run `sys.executable -I` with cwd=sb. Clone carries no `.jj` (`.jj/.gitignore` is `/*`) [obs]. Never copytree.

**F5 LOW:** only rmtree the path mkdtemp returned (root-dac:394,440 and source-scope:461,596 comply) [obs].

Scope: executed=none
