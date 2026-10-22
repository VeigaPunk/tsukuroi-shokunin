# SentinelResidualEnv — C2 re-attack after the config isolation (round 29, wave 2)

Verdict: partly holds. At `10d5288fc1051364e711203855e7c53710dfcc21` the three fixed tools are genuinely immune to the four config-file channels wave 1 turned into code execution, but the isolation is config-file-shaped only: a `git` earlier on PATH still redirects their writes, the per-user attributes file still truncates their fixture archives, enclosing-repo discovery with unchecked init status is untouched, and the declared counter's own harness still runs foreign config. All experiments ran under `/fast/scratch/hyaku/tsukuroi-r29/SentinelResidualEnv/`; no `GIT_*` variable and no PATH entry pointed inside the lane or the fleet repo, and no git write was run in either.

Revision checked read-only: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C repo rev-parse HEAD` → `10d5288fc1051364e711203855e7c53710dfcc21`. Tool tree extracted with `git archive 10d5288f` into `B/tree` (B = `/fast/scratch/hyaku/tsukuroi-r29/SentinelResidualEnv`). Fixed code under test: `tools/check-adjacency-overlap.py:114-117`, `tools/mutants-adjacency-overlap.py:18-21`, `tools/mutants-kernel-taint.py:32-35` (from the clone: `dict({k: v for k, v in os.environ.items() if not k.startswith('GIT_')}, **{'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_SYSTEM': os.devnull})`).

Harness validity (control): with `HOME` holding `[core] hooksPath = B/exp2/hooks`, a plain `git commit --allow-empty` fired the post-commit hook, `B/exp2/HOOKLOG` = 1 line. Every "hookfires=0" below is therefore a real absence of execution, not a broken detector.

## 1. CLOSED — global `core.hooksPath` (wave-1 finding 1, HIGH)

`env -i PATH=/usr/bin:/bin LC_ALL=C HOME=B/exp2/home_plain python3 tree/tools/check-adjacency-overlap.py --selftest` → `rc=0`, `anchored_rows 6`, **hookfires=0**. Pre-fix this ran 43 times (wave-1 finding 1). The same poison against `tools/mutants-kernel-taint.py --base 10d5288f --counter-rev 10d5288f --lane B/repo` → `control_verified_rows 6`, `should_fail_accepted 0`, hookfires=0.

## 2. CLOSED — `$XDG_CONFIG_HOME/git/config`, `includeIf`, `init.templateDir` (wave-1 findings 1, 2)

- XDG-only poison (`HOME` clean, `XDG_CONFIG_HOME=B/exp2/xdg` with `core.hooksPath`): `--selftest` `rc=0`, hookfires=0.
- `includeIf "gitdir:/fast/scratch/**"` → `core.hooksPath`: `rc=0`, hookfires=0.
- `HOME` with `[init] templateDir = B/exp2/tmpl` (containing `hooks/post-commit`): `rc=0`, hookfires=0, against both `check-adjacency-overlap.py --selftest` and `mutants-kernel-taint.py`.
- Mechanism check: `env -i … HOME=B/exp2/home_plain GIT_CONFIG_GLOBAL=/dev/null XDG_CONFIG_HOME=B/exp2/xdg git config --get core.hooksPath` → `rc=1` (no value), so `GIT_CONFIG_GLOBAL=/dev/null` suppresses `$HOME/.gitconfig` *and* the XDG file, as wave-1 observed.
- Both batteries keep their declared controls under the poison: adjacency `control_live_anchored_rows 6`, `should_fail_accepted 0` of 24; kernel `control_verified_rows 6`, `should_fail_accepted 0` of 5.

## 3. CLOSED — `GIT_CONFIG_COUNT` and the prefix-wide `GIT_*` removal (wave-1 finding 4)

`HOME` clean, `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath GIT_CONFIG_VALUE_0=B/exp2/hooks` → `--selftest` `rc=0`, hookfires=0. The tools' dict comprehension covers the whole `GIT_*` namespace, so `GIT_OBJECT_DIRECTORY`, `GIT_COMMON_DIR`, `GIT_NAMESPACE`, `GIT_AUTHOR_*`, `GIT_TEMPLATE_DIR` and `GIT_CONFIG_GLOBAL` are all dropped before each git call. The probe is answered for exactly its declared three variables: `python3 repo/tools/probe-git-env-leak.py --revision 10d5288f --lane B/repo --scratch B/exp2/scratch` → `{"targets": 8, "leaking": 0, "leaking_tools": [], "harness_errors": [], "probe_sha256": "46a55ce7b4ad3fa46d873aab6461ee067d67e22b0c2c4f0c508b2969827fcf80"}`, exit 0.

## 4. OPEN (HIGH for the class, MEDIUM for the repro) — a `git` wrapper on PATH still redirects the tools' writes (wave-1 finding 3)

The scrub happens inside the tool; a wrapper earlier on PATH re-injects the variables afterwards, so no `GIT_*` removal can reach it.

Exploit path: `B/shim/git` = `exec env GIT_DIR=B/exp2/canaryPATH/.git GIT_WORK_TREE=B/exp2/canaryPATH /usr/bin/git "$@"` (also appends `"$*"` to `B/exp2/SHIMLOG`). With `PATH=B/shim:/usr/bin:/bin` and a canary holding one staged, uncommitted file `STAGED`:

- `python3 tree/tools/check-adjacency-overlap.py --selftest` → `rc=1`, 278 shim calls (`SHIMLOG`), and the **canary advanced** `9dc47e7460e796ee19eab59a1745f47ef2b7b543` → `37821098a85a1f4c1eab76289aac51f0ac8434d9`, new commit `3782109 fixture`; the tool's own fixture commits landed in the canary. The run is loud (`anchored_rows 0`, every case `pass:false`) because read paths are redirected too, but the write class of the round-28 incident reproduced: a stranger's repository took the tool's commits.
- `tools/mutants-kernel-taint.py` under the same shim → `rc=1`, `subprocess.CalledProcessError … 'git', '-C', …/repo', 'rev-parse', '--verify', '10d5288f…^{commit}' … exit status 128`; canary unchanged (`d83004e3…` before and after). A commit-only shim (`GIT_DIR`/`GIT_WORK_TREE` injected only when `commit` appears in argv) also failed loudly (`CalledProcessError … 'commit', '-q', '-m', 'base export 10d5288f…' … exit status 128`), canary unchanged. So on this tool the channel currently aborts rather than writes, because every read is `check=True`; it is not closed, only noisy.

Impact: a tool-manager or logging wrapper that pins `GIT_DIR` gets the tool's writes; the probe cannot see it because the probe varies only the three variables. Smallest remediation: resolve the binary (`/usr/bin/git` or `shutil.which` on a fixed path) and write with explicit `--git-dir=<sbx>/.git --work-tree=<sbx>`, which beat inherited environment (wave-1 finding 5, verified there).

## 5. OPEN (MEDIUM) — the per-user attributes file still shapes the tools' `git archive`, and crashes both batteries and the probe

`GIT_CONFIG_GLOBAL=/dev/null` does not govern `$HOME/.config/git/attributes`; only `core.attributesFile` (config) or the compiled default path does, and `GIT_ATTR_NOSYSTEM` covers the *system* file only.

Evidence, running the tools' exact env dict with `HOME=B/exp2/homeattr` where `B/exp2/homeattr/.config/git/attributes` holds `* export-ignore`:
- `git -C B/repo archive 10d5288f` → 10,240 bytes (`rc=0`) versus **68,587,520 bytes** with a clean `HOME`. The whole export is emptied.
- `python3 repo/tools/probe-git-env-leak.py --revision 10d5288f --lane B/repo --scratch B/exp2/scratch4 --only tools/check-freshness-r17.py` → `probe_rc=1`, traceback `tarfile.ReadError: file could not be opened successfully … end of file header`. The declared counter cannot report at all.
- `python3 tree/tools/mutants-kernel-taint.py --base 10d5288f --counter-rev 10d5288f --lane B/repo` → `battery_rc=1`, same `tarfile.ReadError`.

Impact: not code execution and not a silent pass — every consumer of `git archive` dies loudly, so a poisoned host cannot fake a count, but the C2 measurement becomes unavailable and unattributable (the failure looks like a harness bug). Smallest remediation: add `HOME=<empty sandbox dir>` and `XDG_CONFIG_HOME=<same>` to the hermetic dict in all three tools and the probe, which also removes the `hooksPath`/`templateDir`/attributes question in one move.

## 6. OPEN (LOW; reachability of the harmless variant) — enclosing-repo discovery and unchecked `git init` status (wave-1 finding 5)

`check-adjacency-overlap.py:373-390` (`_fixture`) calls `git(repo, 'init', '-q')`, then `add -A` and `commit` without checking any return code; the env carries no `GIT_CEILING_DIRECTORIES` (it would be scrubbed anyway). With no `.git` present, `git -C <subdir>` discovers upward:

- `git -C B/exp2/canaryENC2/lane rev-parse --git-dir` under the tool env → `B/exp2/canaryENC2/.git`, `rc=0`; then `add -A`, `commit -qm fixture` → `rc=0` each and the enclosing repo advanced `6fb24338c4970c42a9a197eb012fa44a4328e768` → `99dd1a19a3d8b7c8bdb68ece917b1c2aa093fe89`, `99dd1a1 fixture`.
- [obs] The wall is thinner than it looks in one direction: a *file* named `.git` in the fixture path makes every command fail (`fatal: invalid gitfile format`), so a half-initialised fixture refuses instead of escaping. [inf] The silent path therefore needs an `init` that fails while the directory stays writable (ENOSPC, ACL, immutable `.git`); no such path was demonstrated inside these three tools, so this stays a mechanism, not an observed leak.
- [obs] `TMPDIR` alone: `TMPDIR=B/exp2/canaryTMP/scratchtmp` (inside a repo) → `--selftest` `rc=0`, canary HEAD unchanged `4435f281…`, no residue in `scratchtmp`; the nested `git init` succeeds, so the sandbox nests and is deleted. `TMPDIR` is a hazard only together with an init failure (previous bullet).

## 7. OPEN (MEDIUM for measurement integrity) — the declared counter's own harness still inherits `HOME`

`tools/probe-git-env-leak.py:` `clean_env()` (from the tip blob) removes `GIT_*` and sets `GIT_CONFIG_NOSYSTEM=1` and `LC_ALL=C` only — no `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM`, no `HOME` override — and `make_canary`, the `git archive` extraction, `git clone --bare` and every `fingerprint()` call run under it.

- `env -i PATH=/usr/bin:/bin LC_ALL=C HOME=B/exp2/home_plain python3 repo/tools/probe-git-env-leak.py … --only tools/check-freshness-r17.py` → `{"targets": 1, "leaking": 0, "harness_errors": []}` while `B/exp2/HOOKLOG` gained **1 line**: foreign config code ran inside the counter's own harness, unrecorded. Wave-1's hang (a self-committing hook, 44,868 commits) is unchanged by this code path: nothing in `clean_env()` suppresses `core.hooksPath`.
- The probe therefore reports "leaking 0 of 8" and "harness_errors empty" on a host whose `~/.gitconfig` executes code on every commit. The 0 of 8 above is evidence about the tools, not about the counter's independence.
- Smallest remediation: run the probe's own git calls under the same hermetic dict proposed in finding 5, and make the poisoned-`HOME` variant an extra target dimension so the counter measures the class it now claims.

## 8. Observations that are not risks

- [obs] The fix's `os.devnull` sentinel works as intended on git 2.56.0 (`git version 2.56.0`): both the `$HOME/.gitconfig` and the XDG config are invisible (`git config --get core.hooksPath` `rc=1`), which is what closes findings 1, 2 and 4.
- [obs] The tools do not set `LC_ALL`; only the probe does. No failure attributable to locale was observed in these runs; it stays a reproducibility nit, not a finding.
- [obs] The three tools pass the scrubbed dict to their `python3` children (`mutants-kernel-taint.py:1124`), so the counter process itself also runs without inherited `GIT_*` — the closure is transitive where the child is started by a fixed tool, and not transitive to the PATH/attributes channels, which are not `GIT_*`.
- [unk] Whether C2's wording ("no longer follow an inherited `GIT_DIR`, `GIT_WORK_TREE` or `GIT_INDEX_FILE`") is meant to cover PATH, attributes, TMPDIR and discovery. On the literal wording the claim holds at the tip; on the SentinelGitEnv finding set it holds only for the variable and config-file channels, and findings 4, 5, 6 and 7 stand outside it.

Scope: read=lane `10d5288fc1051364e711203855e7c53710dfcc21` read-only (SCORECARD.md round-29 declaration, corpus/lessons/round-29.md, tools/check-adjacency-overlap.py, tools/mutants-adjacency-overlap.py, tools/mutants-kernel-taint.py, tools/probe-git-env-leak.py, .ufo/waves/round-29/w1/SentinelGitEnv.md); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/SentinelResidualEnv.md; executed=git clone/checkout of the lane into /fast/scratch/hyaku/tsukuroi-r29/SentinelResidualEnv/repo (read-only thereafter), git archive into tree/, selftest runs of check-adjacency-overlap.py and both batteries under poisoned HOME/XDG/includeIf/templateDir/GIT_CONFIG_COUNT/PATH shims/TMPDIR/attributes, one full probe-git-env-leak.py run at the tip plus two single-target poisoned runs, all git writes confined to canaries under /fast/scratch/hyaku/tsukuroi-r29/SentinelResidualEnv/exp2 (canaryPATH, canaryBATT, canaryC, canaryTMP, canaryENC, canaryENC2, c1)
Model: not exposed
Installs: none
