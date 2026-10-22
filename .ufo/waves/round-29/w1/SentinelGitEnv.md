# SentinelGitEnv — C2 residual-risk review (round 29, wave 1)

Verdict: partly holds, and as worded it can be certified while the round-28 incident class recurs. The three leaking tools at `81a061a67466c5e1be812814a895a4b5ed89b4ff` pass the caller's whole environment to git (no `env=` at all), so any remediation narrower than a hermetic git environment leaves reachable write-redirect and code-execution channels that the frozen C2 probe never varies: `$HOME`/`$XDG_CONFIG_HOME` git config (`core.hooksPath`, `init.templateDir`, `includeIf`), PATH's `git`, `TMPDIR`, and enclosing-repo discovery through unchecked git exit status. All experiments ran under `/fast/scratch/hyaku/tsukuroi-r29/SentinelGitEnv/`; no GIT_* variable was ever pointed inside the lane or the fleet repo, and no git write command was run in either.

Evidence pointers name files under `/fast/scratch/hyaku/tsukuroi-r29/SentinelGitEnv/` (B) unless absolute. Lane read-only tip checked: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C B/repo rev-parse HEAD` → `81a061a67466c5e1be812814a895a4b5ed89b4ff`.

## 1. HIGH — a global `core.hooksPath` runs arbitrary code on every sandbox commit, after a full GIT_* scrub

The three tools call git through helpers that inherit the environment: `tools/check-adjacency-overlap.py:76` (`subprocess.run(['git','-C',repo]+args, …)`, no `env=`), `tools/mutants-adjacency-overlap.py:67-73` (`sh()`/`g()`), `tools/mutants-kernel-taint.py:78-80` (`git()`). `tools/probe-git-env-leak.py:57-59` (`clean_env()`) removes every `GIT_*` and sets `GIT_CONFIG_NOSYSTEM=1` but leaves `HOME`/`XDG_CONFIG_HOME` untouched, so the declared fix target ("no inherited GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE") is met while `$HOME/.gitconfig` still decides what runs during the tools' own fixture commits.

Exploit path: `[core] hooksPath = <dir>` in `~/.gitconfig` (or `$XDG_CONFIG_HOME/git/config`), hook body `git -C <any repo> commit --allow-empty`. Every fixture commit in the tools' temp sandboxes executes it with the full inherited environment; the round-28 incident (a seat writing into the lane) needs only the hook's `git -C` path to name the lane.

Evidence:
- `env -i PATH=… HOME=B/exp/home1 LC_ALL=C GIT_CONFIG_NOSYSTEM=1 python3 B/repo/tools/check-adjacency-overlap.py --selftest` → `rc=0`, and `B/exp/HOOKLOG` holds 43 lines `hook-fired …/poison/post-commit` (43 fixture commits, one hook run each). Control with clean `HOME` writes no log.
- `$XDG_CONFIG_HOME/git/config` alone (clean `HOME`) → `rc=0`, `B/exp/HOOKLOG` 43 fires again.
- `includeIf "gitdir:/fast/scratch/…/**"` with `path = cond.inc` carrying `core.hooksPath` is honoured (`git -C B/exp/probe-sbx config --get core.hooksPath` → `…/poison`), so the hook can be made path-conditional on the sandbox location.
- Per-tool attribution: `B/exp/HOOKLOG6` (40 lines) records `fired pwd=/tmp/tmp*/lane` — the hook ran inside the tools' own fixtures, not in my harness.
- The C2 probe scores this as clean: with the same poisoned `HOME`, `python3 B/repo/tools/probe-git-env-leak.py --revision 81a061a… --only tools/check-freshness-r17.py` prints `"leak": false`, while the hook advanced a stand-in repo (`B/exp/standin` `3c00152` → `2e935b3`). The counter's model is GIT_* only, so "leaking 0 of 8" is compatible with foreign code executing on every commit.

Impact: arbitrary command execution at the privilege of the seat, on every tool run, and a lane-write path of exactly the round-28 class, invisible to both counters. Requires the tool to be run with a poisoned user config, which the lane cannot control; a shared host or a seat with a customised `~/.gitconfig` is enough.

Smallest remediation: give every git call in the three tools a hermetic environment — drop all `GIT_*`, add `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_ATTR_NOSYSTEM=1`, and set `HOME` to the sandbox. Verified: under exactly that env, `check-adjacency-overlap.py --selftest` → `rc=0` with 0 hook fires (`B/exp/HOOKLOG9` 43 → 0 for the same config). This also removes host-config sensitivity: with `commit.gpgsign=true`, `gpg.program=/bin/false` in `HOME`, `check-adjacency-overlap.py --selftest` fails all 43 cases (`rc=1`, `"failed": 43`) on the unfixed code, so the selftests' verdicts currently depend on the operator's `~/.gitconfig` even when no hook is involved.

## 2. HIGH — `init.templateDir` from global config is copied into every sandbox by `git init`

`git init` (e.g. `tools/check-adjacency-overlap.py:259`, `tools/mutants-kernel-taint.py:87`) copies templates from `init.templateDir`, which is a global-config setting and survives any GIT_* scrub. A template carrying `hooks/post-commit` puts the hook *inside* the sandbox, so every later commit in that sandbox runs it, including commits made after the tool returns while the `--keep` sandbox survives.

Evidence: `HOME` with `[init] templateDir = B/exp/tmpl` (only `hooks/post-commit` inside), full GIT_* scrub → `--selftest` `rc=0`, `B/exp/HOOKLOG2` 43 fires. Same remediation as finding 1 (`GIT_CONFIG_GLOBAL=/dev/null` drops the setting); a belt-and-braces `git -C <sbx> config core.hooksPath <empty>` after init does not cover it, because the hook file itself is already in the sandbox.

## 3. MEDIUM — PATH's `git` is a redirect channel no GIT_* scrub touches, and the counter cannot see it

If an earlier `git` on PATH is a wrapper that sets `GIT_DIR`/`GIT_WORK_TREE`, the tools' sandbox writes land in the wrapper's target even after a perfect env scrub, because the scrub happens in the tool and the wrapper re-injects afterwards.

Evidence: `B/exp/shim4/git` = `exec env GIT_DIR=B/exp/canary5/.git GIT_WORK_TREE=B/exp/canary5 /usr/bin/git "$@"`. Running `git init -q sbx2` then `git commit -qm from-sandbox` with only that shim on PATH: `B/exp/canary5` went from no HEAD to `0b68935 from-sandbox`, while `sbx2` had no HEAD at all (the `init` itself was redirected). The probe's control and canary runs share one PATH, so this class is invisible to `probe-git-env-leak.py` by construction (`tools/probe-git-env-leak.py:144-160` varies only GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE).

Impact: presupposes a wrapper (tool-manager shim, logging wrapper) that sets GIT_DIR; severity below findings 1-2, but it is the same write class and no counter covers it. Remediation: fingerprint by explicit arguments, not environment — see finding 5.

## 4. MEDIUM — C2's literal scope (three variables) is insufficient; `GIT_CONFIG_COUNT` alone resurrects arbitrary config

If the fix unsets only `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, as C2 is worded, then `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath GIT_CONFIG_VALUE_0=<dir>` injects config into every git invocation without touching any file, and `GIT_OBJECT_DIRECTORY`, `GIT_COMMON_DIR`, `GIT_NAMESPACE`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_AUTHOR_*`/`GIT_COMMITTER_*`, `GIT_TEMPLATE_DIR` and `GIT_CONFIG_GLOBAL` remain inherited.

Evidence: with only those three variables removed and `GIT_CONFIG_COUNT` set to `core.hooksPath`, `--selftest` → `rc=0`, `B/exp/HOOKLOG3` 43 fires — identical to finding 1. `pass_env` must therefore enumerate by prefix (`k.startswith('GIT_')`), not by name; `clean_env()` in the probe already does this, so the probe's fix and the tools' fix must agree on the stricter shape.

## 5. MEDIUM — enclosing-repo discovery plus unchecked exit status: a fixture that fails to init commits into whatever repo is above it

`tools/check-adjacency-overlap.py:75-76` returns git's `CompletedProcess` and both `_fixture` (`:259-273`) and the mutants' `g()` ignore failures in places, so a `repo` path that is not a repo root silently commits into the enclosing repository. `git -C` only chdirs; discovery walks up with no `GIT_CEILING_DIRECTORIES` (scrubbed anyway).

Evidence: `B/exp/canary2` at `88fd814`, then full-scrub `git -C B/exp/canary2/sub add -A` and `commit -qm stray` → `8896495 stray` on `canary2`, i.e. the enclosing repo's HEAD advanced from a path that looked like a scratch subdirectory. `TMPDIR` is inherited and unscrubbed, so `TMPDIR=<lane>` puts the tool's `tempfile.mkdtemp()` sandboxes inside the lane worktree; when `git init` there succeeds the writes are nested and transient (observed: `B/exp/canary3` HEAD unchanged, no residues after a clean `rc=0` run), but any init failure then lands commits in the lane itself.

Smallest remediation (verified): write with explicit arguments, not environment or discovery — `git --git-dir=<sbx>/.git --work-tree=<sbx> add/commit`. Under `GIT_DIR=B/exp/canary5/.git GIT_WORK_TREE=B/exp/canary5`, `git --git-dir=B/exp/sbx3/.git --work-tree=B/exp/sbx3 commit -qm sbx3-only` produced `sbx3` HEAD `be65240` and left `canary5` at `0b68935`. Command-line options beat inherited environment and skip discovery. Pair it with a checked `rev-parse --git-dir` that must equal `<sbx>/.git` before any write.

## 6. LOW — the probe's leak predicate has blind spots: refs/HEAD/index/objects only, and rc equality

`fingerprint()` (`tools/probe-git-env-leak.py:67-79`) hashes HEAD, all refs, object and ref *filenames*, index and packed-refs, but not `.git/config`, reflogs, or worktree files; `leak` is `canary_changed or canary_rc != control_rc` (`:157-160`). A write that only edits the canary's config or worktree, or a tool that swallows git's error and simply does nothing (`check-adjacency-overlap.py:76` never checks), scores `leak: false`. Example from finding 5's mechanism: a redirect that leaves the canary index clean aborts harmlessly (`nothing to commit, working tree clean`) and looks like no leak, while the same code path with a dirty index writes a stranger's commit (finding 5's `canary5` repro).

Smallest remediation: add `.git/config`, `logs/**` and a hash over the canary worktree files to the fingerprint; add a variant canary with a staged-but-uncommitted file so a redirected `commit` has something to commit.

## 7. LOW — the probe inherits operator config in its own harness, including an availability hazard

`clean_env()` keeps `HOME`, `XDG_CONFIG_HOME`, `TMPDIR` and PATH for the probe's own `git init/clone/archive` and `make_canary` calls. With a global `hooksPath` whose hook itself commits, each hook-triggered commit re-fires the hook: my first `probe-git-env-leak.py` run (single target, poisoned `HOME`) hung and was killed at 300 s, and the stand-in repo reached 44,868 commits (`git -C B/exp/standin rev-list --count HEAD`) before I removed it. The counter can therefore time out or spin on a host whose `~/.gitconfig` sets a committing hook, rather than reporting a result.

Smallest remediation: run the probe harness itself under the same hermetic env as finding 1, and keep the poisoned-config variant as an explicit *additional* target dimension (HOME, PATH, TMPDIR) so the counter measures the class it claims to measure.

## 8. Observations that are not risks

- [obs] Global `core.worktree = <canary>` in `~/.gitconfig` did not redirect: `git -C B/exp/probe-sbx status --porcelain` reported `?? z` from the sandbox worktree, not the canary's contents. No finding.
- [obs] `GIT_CONFIG_GLOBAL=/dev/null` does suppress both `$HOME/.gitconfig` and `$XDG_CONFIG_HOME/git/config` (`git config --get core.hooksPath` → rc 1 in all three layouts), so the remediation in finding 1 is sufficient for the config channel; it does not cover PATH (finding 3) or `TMPDIR` (finding 5).
- [inf] Lane-local `.git/config` of a `--lane` clone is caller-controlled, but `git clone` writes a fresh config, and the tools only `rev-parse`/`archive`/`show` from it; no execution path found there. Worth re-checking if a future target adds `checkout`/`fetch`/`status` against `--lane`.
- [obs] Tools are already host-config-sensitive before any security argument: `commit.gpgsign=true` plus a failing `gpg.program` makes `check-adjacency-overlap.py` fail 43 of 43 cases while `check-freshness-r17.py`, `check-kernel-taint.py` and `check-memory-pressure.py` still report `PASS` — so a hermetic env is also the fix for reproducible verdicts.
- [unk] Whether the L1 intends C2's assertion to cover the hook/PATH/TMPDIR channels; the declaration text names only the three variables, so findings 1-3 and 5 are outside the frozen counter's claim and must be decided explicitly rather than inferred.

## In-flight note (observed, not reviewed as a claim)

[obs] The lane's uncommitted fix at review time scrubs the whole `GIT_*` namespace by prefix in all three tools (`env={k: v for k, v in os.environ.items() if not k.startswith('GIT_')}`, plus a shared `clean_env()` in both batteries) and passes it to the `python3` children too. That closes finding 4 and the inherited-variable half of C2, but it leaves `HOME`, `XDG_CONFIG_HOME`, `TMPDIR`, PATH and the system config untouched, so findings 1, 2, 3, 5 and 7 survive verbatim: the 43 hook fires reproduce unchanged against a helper that only filters `GIT_*`. To close them the same dict must also carry `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_ATTR_NOSYSTEM=1` (and `LC_ALL=C` for reproducible verdicts, matching `probe-git-env-leak.py:57-59`), and the write path should pass `--git-dir=<sbx>/.git --work-tree=<sbx>` plus a checked `rev-parse --git-dir`.

Scope: read=lane at 81a061a read-only (SCORECARD.md round-29 declaration, tools/probe-git-env-leak.py, tools/check-adjacency-overlap.py, tools/mutants-adjacency-overlap.py, tools/mutants-kernel-taint.py, .ufo/waves/round-29/measure/c2-before-81a061a67466c5e1be812814a895a4b5ed89b4ff.jsonl); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/SentinelGitEnv.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/SentinelGitEnv/commands.txt; executed=git clone/checkout and all git writes only inside /fast/scratch/hyaku/tsukuroi-r29/SentinelGitEnv (canaries canary, canary2, canary3, canary4, canary5, sbx1, sbx2, sbx3, standin), python3 runs of the three tools and probe-git-env-leak.py from that clone, read-only git -C on the lane clone; no git or jj write command in the lane or the fleet repo, no GIT_* pointed inside either
Model: not exposed
Installs: none
