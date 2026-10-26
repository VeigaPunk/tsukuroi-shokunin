VERDICT: supports
# Seat C1RevIntegration — item F-7: diff review `447662088dfd3155e31aed239179a79c1d1046c7..78abb8b5cdc9da511b4fc523e661517a68dd33d3 -- tools/tsukuroi-census.sh`

Scope: the four hunks of that file diff (receipt `f7.diff`, 62 lines; 29 changed lines). Bash `GNU bash, version 5.3.20(1)-release`, awk `GNU Awk 5.4.1` (receipt `versions-qm.txt`). `447662088` is an ancestor of `78abb8b` (`git merge-base --is-ancestor` → ok); `78abb8b` is the round-42 integration commit whose message names exactly these census changes.

## 0. Kill rule — PASS

Function map of the tip blob (receipt `funcmap.txt`, awk over function-header lines): `probe_packages` 654–816, `probe_update_safety` 1555–1822, `run_selftest` 1934–3128, `main` 3129+. The four hunks sit at new-file lines 691–703 and 743 (both inside `probe_packages`, confirmed by the `@@ ... probe_packages()` headers in `f7.diff`) and 2190–2196 and 2568–2585 (both inside `run_selftest`; the nearest preceding headers are `run_selftest()` :1934 and the next function `main()` :3129). No hunk touches `probe_update_safety` or anything else; the file diff contains exactly these four hunks.

## 1. The awk error test (:697–703) — equivalent, SIGPIPE-free, D1 removed

Old form (at 447662088): `grep -q '^error:' <<<"$s_out"` + note from `grep -m1`. New form: `err_line=$(printf '%s\n' "$s_out" | awk '/^error:/ { if (!p) { print; p = 1 } } END { if (!p) exit 1 }')` in an `if` condition.

- **Status as condition under `set -euo pipefail`**: the script sets `set -euo pipefail` at :423; an assignment-in-condition suspends `set -e`, and the new awk reads to EOF in all paths (no early `exit` outside `END`), so `printf` can never SIGPIPE; pipeline status is purely awk's 0/1. Verified: every A-case below ran the new form verbatim under `set -euo pipefail`.
- **First-line note equivalence with `grep -m1`**: receipt `exp.out` A1–A9 — old vs new identical (`SAME`) on: no error; empty string; only-newline; error first/mid; two errors (both `error: one` — first wins); CR-prefixed error after the census' pre-existing `tr '\r' '\n'` (`s_out` normalization at :686 exists identically in the old blob, so CR input reaches both forms identically); ~350 KB buffer with error first (A8) and error last (A9). NUL-in-buffer (A9b): both forms emitted the same truncated note `error: nul` — no delta observed.
- **D1 (wave-1 C1RevFix) removed at this site**: no here-string remains on the probe buffer, so no bash temp file and no ENOSPC fail-open. The in-suite regression case `blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1)` (:2353, ~300 KB sample) passes on the tip copy: `PASS ... (exit 2, BLOCKED)` (`selftest.out`:20).

## 2. The :743 lookup without `exit` — first-wins preserved, kill reproduced and fixed

Old: `awk -v n="$nm" '$1 == n {print $2; exit}'`; new: `'$1 == n && !f { print $2; f = 1 }'` (:746).

- **Duplicate names: first wins in both forms.** `exp.out` B1: baseline `alpha 1.0-1 / beta 2.0-1 / alpha 9.9-9`, n=alpha → old `1.0-1`, new `1.0-1`. B2: no match → empty in both (`foreign_new` unchanged).
- **The claimed kill mechanism is real**: `exp.out` B3 — 84 012-byte baseline, match on line 1, `set -euo pipefail`: old form's script dies `exit=141`; new form `exit=0` with the same `bn=[1.1-1]`. B4: late match (`extra/pad03999`) on the same baseline → `bn=[1.0-2]`, i.e. the full read stays correct.
- Trade-off (deliberate, commented at :746): each live name now rescans the whole baseline (O(N·Q) instead of early exit). Baselines are operator-maintained files; not a defect.

## 3. The selftest ABSENT arm here-string (:2193) — fix justified; residual is bounded and harness-only

Old: `printf '%s\n' "$out" | grep -qE -- "${re#ABSENT:}"` in an `if`; new: `grep -qE -- "${re#ABSENT:}" <<<"$out"`.

- **Old form fail-open verified**: under `set -u -o pipefail` (the harness runs `set -uo pipefail`, :1946, inside the script's :423 `set -euo pipefail`), 1.14 MB `$out` with the pattern on line 1: 20/20 runs reported `OLD:absent` although the pattern was present (`exp2.out` D1) — grep finds the match early, exits, `printf` SIGPIPEs, pipefail flips the condition. The new form answers `NEW:present` (D2) and agrees on truly-absent small input (D3/D4). The in-code comment "a SIGPIPE'd pipe here read 'absent' (fail-open)" is accurate.
- **Residual (not a defect of this diff, measured)**: a >64 KiB here-string needs a bash temp file; on a full TMPDIR bash errors and the here-string reads empty → fail-open again, deterministically: private `unshare -rm` + 64 KiB tmpfs as TMPDIR, 1.14 MB pattern-present buffer → `cannot create temp file for here-document: No space left on device` + `VERDICT:absent(FAIL-OPEN)` (`exp2.out` D6; small-buffer control D7 correct; normal-TMPDIR control D8 correct; TMPDIR=/nonexistent falls through, D5 correct — matches wave-1 C1RevFix's fallback chain). Reachability in the suite: instrumented copy of the tip census (one added `printf 'OUTLEN %d' "${#out}"` after the `rc=$?`/`set -e` pair at :2176–2177) over the full selftest: max `$out` = 2 656 bytes; the only two ABSENT cases (:2889, :2924, both `ABSENT:^HANDOFF`) measure 2 465/2 466 bytes — ~25× under the 64 KiB threshold. The harness already requires a writable TMPDIR (`work=$(mktemp -d "${TMPDIR:-/tmp}/...")` :1936), and the fail direction is a silently skipped must-not-match in the test harness, never a live-host verdict.

## 4. The two new -Sup selftest cases (:2571–2586) — regexes exact, mutants bound

- Case `degraded-update-sup-disagree-large`: qu empty rc=1 → `qu_state=empty` (:1619–1620); sup 4 002 lines (~88 KB) enters the empty-vs-sup arm :1665–1669 → `disagree[qu=0 sup=4002]`, `cand=4002`, names from sup's first 3 repo-stripped entries (:1666–1667) = `alpha,beta,pad00000` (`sub(/^[^/]+\//,"")` on `fixture/alpha`, `extra/beta`, `extra/pad00000`). Emission format `qu=rc=$qu_rc/$qu_n; sup=$sup_n$disagree` (:1818) and `REQUIRES-PREP(candidates=$cand join_behind=$behind${cand_names:+ names=[$cand_names]})` (:1805) match the asserted regex exactly.
- Case `degraded-update-qu-sup-mismatch-large`: qu rc=0/2 → `qu_state=cand` (:1621–1622), sup 4 002 ≠ 2 enters :1670–1676 → `disagree[qu=2 sup=4002]`, cand recomputed to 4 002 with sup-side names.
- **Both pass on the tip copy**: `PASS degraded: -Qu empty against a large -Sup keeps the disagree names (R42-C1) (exit 1, DEGRADED)` and `PASS degraded: -Qu/-Sup count mismatch ... (exit 1, DEGRADED)` (`selftest.out`:54–55); full run `TSUKUROI_CENSUS_SELFTEST: PASS (132 cases, 132 passed, 0 failed)`, exit 0 (base at wave 1 was 130 — +2, exactly these cases).
- **They bind the wave-1 survivors**: C1MutSelftest reported mutants 4/5 (the disagree-arm `cand_names` `head -n3` reverts at its green :1638-1639/:1644-1645) SURVIVED the 130-case suite; the comment "the equal-count case above never enters them" is structural — that case has qu rc=0/4002 and sup=4002, so neither `qu_state=empty` nor `sup_n != qu_n` fires. Both new cases drive their arm with an ~88 KB sup side, where a `head -n3` revert dies with the B3-proven exit 141 (wrong exit → case fails) and any name/disagree corruption trips the asserted regex tokens (`candidates=4002`, `names=[alpha,beta,pad00000]`, `disagree[qu=… sup=4002]`).

## 5. Findings by severity

**Defects: none found.** Every itemized check (§1–§4) supports the diff; the tip selftest is green (132/132) with the instrumented run reproducing it.

**Minor / residual (out-of-diff observations, no action required for F-7):**
1. The new comment at :695–697 says "no here-string either (a here-string over 64 KiB is a temporary file, which breaks the no-write contract…)" — accurate for this site, but the same function still feeds probe buffers through here-strings at :754 (`done <<< "$CAP_OUT"`, pacman -Qm output) and :761 (`done <<< "$base_txt"`), and live-path here-strings exist at :1830/:1855 (pre-existing, identical in the old blob — verified). For a >64 KiB buffer those re-open the letter of the "never writes anything" contract (:8–9) and the same ENOSPC fail-open class. Reachability today: `pacman -Qm` on this host measures 21 lines/539 bytes (`versions-qm.txt`), far under the threshold; wave-1 C1RevFix already recorded the :1830/:1855 exposure as pre-existing.
2. The ABSENT-arm here-string retains the theoretical ENOSPC fail-open for >64 KiB `$out` (§3, D6-proven mechanism) — harness-only, measured suite max 2 656 bytes, selftest already requires a writable TMPDIR.

## 6. Verification gaps (checks not run)

- I did not run the frozen C1 counter `tools/score-size-invariance-r42.py` (owned by another seat; my item is the diff review).
- I did not run the live census against the host and did not test bash versions other than 5.3.20 (temp-file/fallback chains are bash-version-dependent; wave-1 C1RevFix pinned the same bash 5.3.20).
- The old-form fail-open count (20/20) is timing-dependent in principle; the receipt run is the recorded observation (`exp2.out` D1), and the deterministic ENOSPC variant (D6) does not depend on timing.
- CR handling was tested through the census' own `tr '\r' '\n'` pre-normalization (:686, pre-existing); raw-CRLF delivery to the `^error:` match was not separately tested because no code path can reach the test without that `tr`.

## Receipts (this dir, all < 2 MB)

`f7.diff` (the reviewed diff) · `exp.sh`/`exp.out` (A/B battery: equivalence, duplicate names, 141 kill repro) · `exp2.sh`/`exp2.out` (D battery: pipefail fail-open, ENOSPC via private tmpfs, controls) · `selftest.out` (tip selftest, 132/132 PASS) · `selftest-inst.out` + `selftest-inst.err` (instrumented rerun; per-case `$out` sizes) · `funcmap.txt` · `versions-qm.txt`. Scratch `/fast/scratch/hyaku/tsukuroi-r42/C1RevIntegration` removed after copying; no lane file outside the report and receipts was created or modified; no host mutation (the tmpfs experiment ran inside `unshare -rm`).
