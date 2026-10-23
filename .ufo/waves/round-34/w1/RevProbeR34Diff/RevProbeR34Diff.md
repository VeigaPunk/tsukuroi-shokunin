# RevProbeR34Diff — frozen-counter provenance review (round 34 wave 1)

Same content as `.ufo/waves/round-34/w1/RevProbeR34Diff.md` (copy kept in the seat directory per contract).

Verdict: counter provenance VERIFIED with one completeness finding — the r34 probe is byte-identical to the r33 probe except for the five declared areas, the frozen bytes and predicate sentence match the declaration exactly, the nine targets are genuine ambient-copy builders at the base; but the declared sweep denominator "(13 files)" is not reproducible, because two more `tools/*.py` files at the base (`tools/run-receipt.py`, `tools/probe-git-env-residual-r30.py`) match the stated sweep rule shape and are in neither the nine nor the four stated exclusions.

## 1. Blob diff r33 → r34: verified (only the five declared change areas)

Command (exit 0):
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0:tools/probe-child-env-allowlist-r33.py 6de666c427ba9aa6b4350561980bde8d0e7c261d:tools/probe-child-env-allowlist-r34.py`

Result: 1 file changed, 37 insertions(+), 5 deletions(-), exactly five hunks:

1. `@@ -1,5 +1,25 @@` — docstring header paragraph: the r33 title line replaced by the r34 title line, plus the new round-34 paragraph (claims "only these changes: this paragraph, the usage line, VERSION 4, the claim target set and a third set `r33claim`") and the re-stated "Child-process environment allowlist probe v3 (round 33…)" title line.
2. `@@ -94,8 +114,8 @@` — usage line: `r33.py` → `r34.py`, `--set claim|regression` → `--set claim|r33claim|regression`.
3. `@@ -118,6 +138,17 @@` — target sets: nine new `CLAIM_TARGETS` entries inserted before the old five r33 claim entries; the old five entries remain byte-identical context lines, now under the new `R33_CLAIM_TARGETS = (` header.
4. `@@ -139,7 +170,8 @@` — `TARGET_SETS` gains `'r33claim': R33_CLAIM_TARGETS`.
5. `@@ -158,7 +190,7 @@` — `VERSION = 3` → `VERSION = 4`.

No other byte differs: `PREDICATE`, its import-time `assert PREDICATE in ' '.join(__doc__.split())`, `PREDICATE_LABEL = 'leaking'`, `CHANNELS`, `TIMEOUT`, `SYSTEM_GIT`, `KEPT_GIT_SETTINGS`, `VALUE_NAMES`, `NAMED_INJECTED`, `REGRESSION_TARGETS` and every function body are outside any hunk (byte-identical). Both blobs are mode 100755 and end with a newline (no "\ No newline at end of file" marker). `PREDICATE` is byte-equal between r33 and r34 (also confirmed by direct extraction, sha256 `9726dc77fa26dac64ea4535fcfbeb031be26d9bd9dcdb3a8643df446aca83f90` for both — [obs]).

Frozen bytes match the declaration: `git show 6de666c:tools/probe-child-env-allowlist-r34.py | sha256sum` = `35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8` (exactly the declared frozen counter). r33 blob sha256 = `c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd`, matching the r34 docstring's quoted prefix `c24f344b864a13ea…` — [obs].

## 2. Predicate sentence: byte-identical to the probe's `PREDICATE`

The declaration's "Frozen predicate C1" paragraph (SCORECARD.md:1425 at 6de666c) contains the sentence between ASCII double quotes; extracting it and comparing to the probe's `PREDICATE` constant (both via `ast.literal_eval` on `git show` bytes): identical, byte for byte, sha256 `9726dc77fa26dac64ea4535fcfbeb031be26d9bd9dcdb3a8643df446aca83f90` — [obs]. So "the same sentence as round 33" is true (r33 `PREDICATE` is identical too), and the label `leaking` equals `PREDICATE_LABEL`. The import-time docstring assert is unchanged from r33.

## 3. Target selection: the nine are correct; the "(13 files)" sweep denominator is not reproducible

### 3a. The nine are genuine ambient-copy builders at the base (2641591e) — [obs]

Each of the nine contains a dict comprehension over `os.environ.items()` that feeds git children; nine of the ten builder sites filter `GIT_*` only, one filters `GIT_*|LD_*|PYTHON*`:

- `tools/check-boot-chain.py:802` (GIT_-only; `:803` adds GIT_OPTIONAL_LOCKS/GIT_PAGER/LC_ALL)
- `tools/check-btrfs-repair-r31.py:108` (GIT_|LD_|PYTHON)
- `tools/check-btrfs-space-r30.py:96` (GIT_-only)
- `tools/check-locator-clarification.py:448` and `:577` (GIT_-only)
- `tools/check-recheck-commands.py:799` (GIT_-only)
- `tools/check-section-citations.py:406` and `:568` (GIT_-only)
- `tools/check-seat-scope.py:174` (GIT_-only)
- `tools/check-source-scope-correction.py:355` (GIT_-only)
- `tools/measure-update-recheck.py:438` and `:485` (GIT_-only)

The L1 development runs at the base corroborate: `.ufo/waves/round-34/l1/dev-base/rc.txt` lists all nine with rc=1 (leaking), and `dev-base/README.md` says "9 targets leak on all three channels (exit 1)" — [obs]. Harness viability for the nine is evidenced by those runs.

### 3b. The four stated exclusions are supported by committed L1 evidence — [obs]

- `probe-git-env-leak.py:58` (GIT_-only + GIT_CONFIG_NOSYSTEM/LC_ALL): excluded "control runs disagree on stdout"; `dev-base/rc.txt` rc=2, README: "Harness errors (exit 2): probe-git-env-leak (control runs disagree on stdout digest)".
- `check-report-receipts.py:311` (GIT_-only): excluded "starts no git child"; `dev-base/rc.txt` rc=2, README: "check-report-receipts (control run starts no git child)".
- `check-revision-binding.py:104` (GIT_-only): excluded "control run still unfinished after 45 minutes"; README: "check-revision-binding: control run unfinished after about 45 minutes; the L1 cancelled the job (empty files)".
- `mutants-btrfs-space-r30.py:362` (GIT_-only): excluded "no mode starts git"; README: "mutants-btrfs-space-r30 has no git-starting mode and was not run"; code reading confirms the env at `:362-363` feeds a `python3 counter --tree …` child, not git — [obs].

Round-33 spot-check routed defect 7 (corpus/lessons/round-33-verifier-spotcheck.md §5 item 7) names exactly four ambient-copy builders: `check-revision-binding.py:104`, `check-btrfs-space-r30.py:96`, `check-btrfs-repair-r31.py:108`, `probe-git-env-leak.py:58` (RevC1Diff) — so "named four of the thirteen" is accurate: all four are in the thirteen (two in the nine, two excluded). — [obs]

### 3c. Missing from the thirteen: two files match the stated rule shape exactly — [finding]

The docstring's rule (tools/probe-child-env-allowlist-r34.py:5-9) is: "every `tools/*.py` file at the claim base `2641591e` that builds a git child environment as a copy of the ambient environment minus `GIT_*` (the dict comprehension over `os.environ.items()` … a full sweep finds thirteen)".

At the base, two more files satisfy this shape exactly (dict comprehension over `os.environ.items()`, `GIT_*` filter, feeding a `git` child) and appear in neither the nine nor the four exclusions:

1. `tools/run-receipt.py:39` — `env()` builds `{k: v for k, v in os.environ.items() if not k.startswith('GIT_')}` plus fixed GIT_CONFIG_*; it is passed to `git -C <lane> rev-parse --verify <rev>^{commit}` in `resolve()` (run-receipt.py:55-57). That is a git child environment built as ambient minus `GIT_*`.
2. `tools/probe-git-env-residual-r30.py:75` — `probe_env()` builds the same comprehension shape (plus GIT_CONFIG_NOSYSTEM/LC_ALL/HOME/XDG_CONFIG_HOME/TMPDIR); it is passed to `git()` (`SYSTEM_GIT` children) in `make_canary_repo()` and `fingerprint()`.

The strict count is therefore 14 files, not 13. Under the loose shape the nine's own membership forces (check-btrfs-repair-r31's `:108` builder removes `GIT_*|LD_*|PYTHON*` yet is counted), three more shape-matching files exist: `probe-git-child-env-r31.py:88`, `probe-child-env-allowlist-r32.py:111` and the counter itself `probe-child-env-allowlist-r33.py:184` (all `GIT_*|LD_*|PYTHON*` comprehensions feeding child runs that start git) — total 18. Excluding the three probes as measurement apparatus is defensible (the counter cannot target itself), but it is not stated in the docstring, and the exclusion list gives reasons for every other non-claim builder. `score-census-handoff-r32.py:786` filters `TSUKUROI_` only (does not remove `GIT_*`) and feeds a census-script child, so it does not match the rule under either reading — [obs].

No other builder form exists in `tools/*.py` at the base: grep for `environ.copy`, `dict(os.environ`, `{**os.environ`, `env=os.environ`, `os.environ |`, `getenv`, `putenv` returns only docstring/scan-rule text inside the probes, no code — so the dict comprehension is the complete form universe — [obs].

### 3d. Materiality

None for the frozen counter's validity: C1's declared surface is scoped to "the nine harness-viable lane tools" and the after-value counts only the 27 pairs; the probe is frozen and tests exactly those nine. The defect is in the provenance narrative: "a full sweep of `tools/*.py` … (13 files)" (SCORECARD.md:1427) and "a full sweep finds thirteen" (probe docstring line 9) are not reproducible from the stated rule, and after the claimed change lands, `run-receipt.py` and `probe-git-env-residual-r30.py` will still hand ambient-minus-`GIT_*` environments to git children — the same class round-33 defect 7 flagged as "ambient copies outside the claim". Recommend an addendum/amendment noting these two files and why they are outside the C1 surface (receipt harness / superseded probe), without touching the frozen probe or predicate.

## Residual risks and verification gaps

- [unk] The two missed builders' "control run viability" was not re-run (NO-EXEC); their non-viability is plausible (run-receipt requires `--revision/--out/-- <tool>` and has no `--selftest`; residual-r30 has no claim-mode argv) but unstated.
- [unk] `check-revision-binding`'s 45-minute control-run hang is taken from the L1's cancelled-job note; not reproduced.
- No git/JJ writes, no probe execution, no edits to lane files outside the seat/wave evidence directories.

Scope: read=<SCORECARD.md:1422-1444 (round-34 declaration) at 6de666c; tools/probe-child-env-allowlist-r34.py and -r33.py blobs at 6de666c and 9c89ff4f; git grep/ls-tree of tools/ at 2641591e; .ufo/waves/round-34/l1/dev-base/{README.md,rc.txt}; corpus/lessons/round-33-verifier-spotcheck.md §5; run-receipt.py and probe-git-env-residual-r30.py at 2641591e>; wrote=<.ufo/waves/round-34/w1/RevProbeR34Diff.md, .ufo/waves/round-34/w1/RevProbeR34Diff/RevProbeR34Diff.md>; executed=<read-only git (show/diff/grep/ls-tree), sha256sum, ast.literal_eval extraction in the eval kernel; no probe/receipt execution>.
Model: inception/mercury-3
Installs: none
