# Round 31 wave 2 — seat RevScrubMutantsKernelTaint (C2 fix review for tools/mutants-kernel-taint.py)

Verdict: **holds** — the C2 fix in `tools/mutants-kernel-taint.py` drops `GIT_`/`LD_`/`PYTHON` names at every spawn site while keeping the round-30 child contract; the frozen probe reads `leaking` 0 of 3 (exit 0) at tip f3a5723a, versus 1 of 3 (loader-env) at pre-fix 8cff9e7c; direct runs of the tool's probe argv at both revisions are identical after normalisation (exit 0 both); no hollow fix found.

## Findings

1. [obs] The entire fix is one hunk in `clean_env()`: `git -C <sandbox repo> diff 8cff9e7c f3a5723a -- tools/mutants-kernel-taint.py` shows only line 33 changing to `if not k.startswith(('GIT_', 'LD_', 'PYTHON'))` (was `'GIT_'`). The counter `tools/check-kernel-taint.py` got the identical one-line change (line 253, `git_env`), so the counter the tool spawns also stops propagating injection variables.
2. [obs] Spawn-site audit (tip copy `/fast/scratch/hyaku/tsukuroi-r31/RevScrubMutantsKernelTaint/repo/tools/mutants-kernel-taint.py`): there are exactly five subprocess spawn sites, and every one passes `env=clean_env()`:
   - `_export` rev-parse (lines 62-64), `archive` (65-66), `show` (73-74) — all `env=clean_env()`;
   - `git()` helper (lines 90-93) — `env=clean_env()`;
   - counter spawn in `run()` (lines 146-148) — `env=clean_env()`.
   No spawn site lacks the cleaned environment. `clean_env()` (lines 32-39) drops keys starting with `GIT_`, `LD_`, or `PYTHON`, then sets the round-30 contract: `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, private `HOME`, `XDG_CONFIG_HOME`, `PATH=/usr/bin:/bin`, and non-empty `GIT_CEILING_DIRECTORIES` (SEAT parent). This matches the probe's `CONTRACT` tuple plus the ceiling requirement.
3. [obs] Frozen probe at tip: `python3 tools/probe-git-child-env-r31.py --revision f3a5723a... --lane <sandbox clone> --only mutants-kernel-taint.py` → exit 0; summary last line: `{"revision": "f3a5723a...", "targets": 1, "pairs": 3, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0", ...}`. `probe_sha256` matches the pinned b168b9b8… . All three channel receipts read `leak: false` with empty evidence; control runs rc 0, 635 git execs each; dotgit-pointer canary fingerprint unchanged (no spurious verdicts this run).
4. [obs] Same probe at pre-fix 8cff9e7c: exit 1; `leaking` 1 of 3, `leaking_pairs: ["tools/mutants-kernel-taint.py:loader-env"]` with evidence `"659 descendant execs carry the injection path"` (sample exec `/usr/bin/git` argv `["git","-C",...,"rev-parse"]`). `child-contract` and `dotgit-pointer` were clean at both revisions — consistent with the declaration's errata that the base leak set is loader-env only and the other two channels are regression guards (0 → 0). This confirms the fix is what removes the leak, not an artifact of the measurement.
5. [obs] Direct run of the tool's probe argv at both revisions (TARGETS entry `--base {rev} --counter-rev {rev} --lane {clone}`, clone = bare lane clone): `python3 <tool> --base <REV> --counter-rev <REV> --lane /fast/scratch/hyaku/tsukuroi-r31/RevScrubMutantsKernelTaint/lane.git` — pre (8cff9e7c) exit 0, tip (f3a5723a) exit 0; stdout identical after normalising 40/64-hex and scratch paths (both sha256 `a70ddc3b5f683870d48acf3799e3873f1042765f0d4dce7b9d929efcd28e7259`); stderr empty for both; 25 lines each (24 mutant results + final summary). The fix therefore changes no observable normal behavior — it only strips injected loader/interpreter variables.
6. [obs] Not hollow: the tip run did the full battery. Summary: `control_exit: 0`, `control_verified_rows: 6`, `should_fail_total: 5`, `should_fail_accepted: 0`, `accepted_mutants: []`, `harness_errors: []`, and 8 `other_accepted` mutants (the known non-declared acceptances). 24 per-mutant JSON lines are real results from a fresh temp seat each run (baseline exit 0 / verified_rows 6; declared mutants exit 1 with blocking findings, e.g. generic_word_quote → KT-QUOTE-TOO-SHORT). No early exit, no replay of canned output (every line differs per mutant), no skipped mutants. The 635 git-child counts per control run also show the work is performed, not skipped.

## Residual risk and verification gaps

- [inf] The review covers only `tools/mutants-kernel-taint.py` (this seat's scope). The other ten round-30 lane tools and the two owed-statement batteries are covered by sibling seats; this seat did not examine their spawn sites.
- [unk] The probe was run against one target (—only), so the full 33-pair matrix is not reproduced here; the after-receipt at the integration commit (C2 leaking 0 of 33) remains the integration-level check.
- [inf] `dotgit-pointer` at the tip produced no canary fingerprint change in this run, so the known rare spurious verdict (2/121 in wave 1) did not recur and needed no re-run.

## Commands executed (with outcomes)

- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-local <lane> /fast/scratch/hyaku/tsukuroi-r31/RevScrubMutantsKernelTaint/repo && git -C repo checkout -q f3a5723a...` → sandbox ready.
- `git -C repo diff 8cff9e7c f3a5723a -- tools/mutants-kernel-taint.py` → single clean_env hunk (13 lines of diff).
- `git -C repo diff 8cff9e7c f3a5723a -- tools/check-kernel-taint.py` → single git_env hunk.
- `python3 repo/tools/probe-git-child-env-r31.py --revision f3a5723a... --lane repo --only mutants-kernel-taint.py` → exit 0, leaking 0/3.
- `python3 repo/tools/probe-git-child-env-r31.py --revision 8cff9e7c... --lane repo --only mutants-kernel-taint.py` → exit 1, leaking 1/3 (loader-env, 659 descendants carrying injection path).
- `git clone -q --bare --no-local repo lane.git`; `python3 tool-8cff9e7c.py --base 8cff9e7c... --counter-rev 8cff9e7c... --lane lane.git` → exit 0; `python3 tool-f3a5723a.py --base f3a5723a... --counter-rev f3a5723a... --lane lane.git` → exit 0; normalized stdout equal (sha256 a70ddc3b… both).

Scope: read=SCORECARD.md:1196-1224, tools/probe-git-child-env-r31.py (full), tools/mutants-kernel-taint.py (tip + 8cff9e7c copy), tools/check-kernel-taint.py diff, probe run summaries; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevScrubMutantsKernelTaint.md; executed=git clone/checkout/diff (read-only), probe runs ×2, direct tool runs ×2, sha256/normalisation comparison.

Model: not exposed.

Installs: none
