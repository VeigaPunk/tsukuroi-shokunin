VERDICT: defect-found — the C2 counter measures correctly on the freeze bytes (claim C2 PASS), and I reproduce the frozen legs, but the counter carries one HIGH and several MEDIUM/LOW defects, each shown by a fixture in this report.

Scope: `tools/check-selftest-matcher-r50.py` at `8029cdba1049df25632c91a23c8db4eefb54be5f` (extracted to `R50RevCounterC2/counter.py`, sha256 over the blob not recomputed — `git show` bytes were used verbatim) vs its docstring and the FROZEN C2 row. Bytes under test: `tools/tsukuroi-census.sh` at freeze (sha256 `aeda2cbc…0245dc`, matches `freeze-counter.json:census_sha256`) and at base `b866a1d3` (`4e032bcb…a4c2`, matches `.ufo/waves/round-50/before/c2-at-base.json`).

## 0. Frozen measurement reproduced

`python3 counter.py --revision 8029cdba… --lane <lane> --scratch <dir>` → rc 0, 57 s wall, one selftest-bearing command at a time. Legs: `idiom_sites 0, base_misses 20, full_misses 0, cases 168, pass_runs 2, case_ok 1` → PASS (receipt `freeze-counter.json`; both `run_detail` runs `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` + `(R50-C2)` PASS line). Base census at `b866a1d3` → rc 1, legs `idiom_sites 7, cases 167, case_ok 0` → FAIL, matching the FROZEN "Before at base" column and `before/c2-at-base.json` byte-for-byte (`census_sha256` equal). The counter does the thing the claim needs — on the bytes it was written for.

Axes I varied: pattern fidelity (does `IDIOM_RE` catch defect-class forms), provenance (does the receipt name the bytes read), run-consistency (legs that read only the last run or any run), and the sensitivity controls (probe honesty, `pass_runs` arithmetic, `cases` pinning).

## 1. Findings, by severity

### HIGH-1 — the counter is a shape test: a 5-line stub census passes all six legs

`tools/check-selftest-matcher-r50.py:127` only requires one output line that `startswith('PASS ')` and contains `(R50-C2)`, plus the summary regex match and zero idiom sites. Fixture `R50RevCounterC2/stub.sh` (5 lines, runs no matcher, no fixture tree, no census logic at all) → `verdict PASS` rc 0 (`f1-stub.json`, legs `idiom_sites 0, base_misses 20, full_misses 0, cases 168, pass_runs 2, case_ok 1`). Command: `python3 counter.py --revision 0000…000 --census-file $S/fx/stub.sh --scratch …`.

This is exactly the routed defect the round-49 verifier named for the sibling counter — `corpus/lessons/round-49-verifier-spotcheck.md` §7 item 4: "`check-fd-band-r49.py`: add the spaced-TMPDIR PASS leg and a 'diagnostic not merely in a comment' leg (`R49CritFdB` cheat Pb: a 19-line 'liar' census passes)". The r50 counter reproduces that defect class on the new legs: nothing ties `case_ok` to code that *executes* the (R50-C2) case. A census that prints the four expected strings passes.

### HIGH-2 — `IDIOM_RE` is literal-form brittle: 7 semantically-identical defect forms score `idiom_sites 0`, two demonstrated on the real census

`counter.py:53`: `printf '%s\\n' "\$(?:out|pkgline)" \| (?:grep -q|head -n1|grep [^\n]*\| head -n1)`. Coverage matrix (`idiom-matrix.out`): it matches only `printf '%s\n' "$out|$pkgline"` with that exact quoting, spacing and flag spelling. These defect-class forms all score **0**:

| form | still SIGPIPEs? | measured false-miss/20 |
|---|---|---|
| `printf '%s\n' "${out}" \| grep -q` | yes | 20/20 (`probe2.out` run B/C — the re-run landed 20/20 for braced) |
| `printf "%s\n" "$out" \| grep -q` | yes | 19/20 |
| `printf '%s\n' "$out" \| grep -m1` | yes | 20/20 |
| `printf '%s\n' "$out"|grep -q` (no space) | yes | same class (not separately measured — identical pipeline) |
| `printf '%s\n' "$CAP_OUT" \| head -n1` | yes | the round-42 comment at freeze census `:3435` names exactly this var |
| `echo "$out" \| grep -q` | yes | same writer-side SIGPIPE class |
| `printf '%s\n' "$out" \| grep --quiet` | yes | spelling variant |

Demonstrated end-to-end on the real census (not just the regex): `mut.braced.diff` reverts the freeze arm `elif ! out_has 'host=fixture-host'; then` to `elif ! printf '%s\n' "${out}" | grep -q 'host=fixture-host'; then` (one line, executable, the banned idiom verbatim modulo braces). The selftest still passes (small fixtures never fill a pipe), and the counter verdict is **PASS** — `idiom_sites 0`, observed output `{"idiom_sites": 0, "cases": 168, "pass_runs": 2, "case_ok": 1, "verdict": "PASS"}` rc 0, wall 57 s. Same for `mut.dqfmt.diff` (`printf "%s\n"` double-quoted format): PASS, wall 58 s. So a defect the claim says is gone could come back tomorrow in any of seven spellings and the counter would print PASS.

The round-42 comment inside the freeze census itself (`census.freeze.sh:732`) names `| grep -m1` as banned; `IDIOM_RE` has no `-m1`/`--quiet` branch. The comment-skip rule (`counter.py:100-101`, added by freeze amendment 2) correctly suppresses the one verbatim quote at freeze census `:2230` — at freeze `regex hits=1, executable=0` (`idiom-sites-at-revs.out`). At base it scores 7 on 7 executable lines, all enumerated in the same receipt.

### MED-1 — `--census-file` breaks revision provenance: the receipt echoes an unvalidated `--revision` and never names the file

`counter.py:75-83`: the `cat-file -e` existence check runs only `if not a.census_file`; `counter.py:91` then reads the file instead of the revision blob. `f1-stub.json` shows a PASS whose `"revision"` is `0000000000000000000000000000000000000000` — a commit that does not exist — and no output field names the census path. `census_sha256` (`counter.py:132`) does bind the bytes read, so this is softer than the round-49 routed defect ("the receipt names only the `--revision` argument"): the gap is that a receipt reader cannot tell the measurement was file-sourced, and the printed `revision` is meaningless on this path. On the normal path the binding is sound: `git show <rev>:tools/tsukuroi-census.sh` + `census_sha256` (`census.freeze.sh` digest matches the emitted `aeda2cbc…`).

### MED-2 — selftest exit code is recorded but never gated

`counter.py:117-126` stores `p.returncode` in `run_detail` but `pass_runs`/`cases`/`case_ok` read only the summary regex. Fixture `rc-ignored.sh` prints a PASS summary then `exit 1` → **PASS** rc 0 (`f7-rcign.json`, `run_detail[0].rc` shows `1`). The real census's last selftest line is `[ "$FAIL" -eq 0 ]` (`census.freeze.sh:3665-3666`) — if that assertion regressed, or a case passed while a sibling crashed the run, this counter would still PASS.

### MED-3 — `cases` and `case_ok` are last-run / any-run, not per-run

`counter.py:123-128`: `cases = int(m.group(2))` overwrites each loop; `case_ok` is `any(...)` across all runs. Fixture `stateful.sh`: run 1 prints `PASS (167 cases, 167 passed, 0 failed)` with no `(R50-C2)` line; run 2 prints 168 + the case line → **PASS** rc 0 (`f8-state.json`, `run_detail` shows the 167 run verbatim). A suite that lost a case — or the (R50-C2) case itself — on one of the two runs is invisible.

### MED-4 — `--runs 1` silently downgrades `pass_runs`, and the emitted `predicate` string misdescribes the run

`counter.py:130` compares `pass_runs == a.runs` while `PREDICATE` (`counter.py:50`) and the FROZEN row state `pass_runs == 2`. `--runs 1` on the stub → **PASS** rc 0 with `pass_runs 1` while the receipt still prints `predicate: "… pass_runs == 2 …"` (`f4-runs1.json`). The w1 spec itself dispatches `--runs 1` for the D-8 anti-vacuity seat (`make-w1-spec.py` item D-8 line), so the downgrade is exercised in this wave — a single-run PASS would carry a predicate text claiming two.

### LOW-1 — docstring says `6 at base`, the counter scores `7`

`counter.py:16` "(target 0; 6 at base b866a1d3)". Measured: 7 (`idiom-sites-at-revs.out`, `before/c2-at-base.json:idiom_sites=7`, FROZEN row and K0 control both say 7). One line of the docstring is stale; probably authored before the `:2386` `$pkgline` site was counted.

### LOW-2 — usage string promises `--census-file` alone works; it crashes

`counter.py:36` "--scratch (required unless --census-file is given)" vs `counter.py:84` `os.makedirs(a.scratch, exist_ok=True)` unconditionally → `TypeError: expected str, bytes or os.PathLike object, not NoneType`, rc 2 (`u1-noscratch.json`). Cosmetic — the error is honest and loud — but the documented invocation does not run.

### LOW-3 — `cases == 168` is a freeze, not a property of the fix

`mut.extra.diff` adds one passing case; the suite now prints 169 → **FAIL** rc 1, observed `{"cases": 169, …, "verdict": "FAIL"}` wall 60 s, every other leg green. So the leg is a drift trap: any future round that legitimately grows the selftest must edit this counter's constant or the claim flips to FAIL. This matches the lane's established pattern (round-49's `check-fd-band-r49.py` pinned `TARGET_CASES = 167`, `check-fd-band-r49.py:35`, and round 50 re-pinned it), so it is a deliberate freeze-by-convention rather than a novel defect — but neither the docstring nor the predicate says `168` means "exactly this round's suite", and there is no `>=` leg to absorb growth.

### LOW-4 — `idiom_sites` scope is the whole file, though the docstring says "inside the selftest harness"

`counter.py:100` scans every line of the script; docstring `counter.py:15` claims only the harness. Over-counting is conservative (fails more), so direction is safe; the docstring is imprecise.

### LOW-5 — FROZEN row's "no here-string" is not true of the shipped bytes, and the counter could not see one anyway

FROZEN row C2 describes the replacement as "awk, full read, no early exit, no here-string". The freeze census still runs `grep -qE -- "${re#ABSENT:}" <<<"$out"` at `census.freeze.sh:2408` (the ABSENT arm, annotated "round 42: a SIGPIPE'd pipe here read 'absent' (fail-open)"). Measured: the here-string form false-misses **0/20** (`probe2.out` line E) — no writer process, no SIGPIPE, so not a live defect — but the claim's parenthetical is false of the bytes and `IDIOM_RE` has no `<<<` branch, so the counter could not detect either interpretation.

## 2. Asked questions, answered

- **Does the probe run under `set -o pipefail`?** Yes — `counter.py:57` (`PROBE` body line 2). The probe replica mirrors the census idiom (printf → grep -qE on a 100 KB + marker + 100 KB buffer).
- **Is `base_misses > 0` a real sensitivity control or a flake?** Real. Five independent 20-trial probe runs: `20, 20, 20, 20, 20` (`probe5.out`); the earlier five runs printed `20, 19, 20, 20, 19`. The idiom false-misses ≥19/20 on a 200 KB buffer because `grep -q` exits at the mid-stream match while ~100 KB remain unwritten — far above any plausible threshold of `>0`. But it *is* a replica probe, not the census's own output; the docstring's named limit (`counter.py:29-32`) declares this honestly.
- **`cases == 168` — freeze or drift trap?** Drift trap by mechanism (F3), freeze by established convention (LOW-3).
- **`pass_runs == 2` — could a flaky census pass twice?** Yes: escape probability is `(1−p)²` per-run flake p — a 50 % flake (F6, `f6-flaky.json`) is caught (`pass_runs 1` → FAIL), a 10 % flake escapes with probability 1 %. Two runs is a weak flake control; combined with MED-2/3, each run's verdict is also partially invisible.
- **`--census-file` — does the receipt name the bytes it read?** By digest yes (`census_sha256`), by name/revision no (MED-1) — an improvement over the round-49 sibling but still a false-`revision` field on the file path.
- **Does the regex catch the base sites / false-positive on the round-42 comment?** All 7 base sites caught (`idiom-sites-at-revs.out`); at freeze exactly 1 regex hit, the verbatim quote inside the `:2230` comment, suppressed by the comment rule — no false positive on executable code. The freeze census's own remaining `grep -q`/`head -n1` code lines (`:678, 841, 1034, 1898, 2408, 3495, 3753`) are file reads, here-strings, or `|| true`-masked pipelines — none is the banned `printf | early-exit` class. (Verified by reading each line; `probe2.out` line E shows the here-string class does not false-miss.)

## 3. The grep→awk migration is semantically clean on current patterns

Bonus check, no defect: the census passes only POSIX ERE (`\(`, `+`, `*`, `|`); a scan for GNU-grep-only constructs (`\b \w \s \< \> (?: \d`) across `census.freeze.sh` finds none (the `\<`/`\>` at `:1390` are `[ ]` string comparisons, not regexes). Differential test of the four must-match patterns fed to `out_has`/`buf_has` (`:2396, 2398, 2402` plus the R50-C2 pattern): `grep -qE` and `RE=… awk '$0 ~ ENVIRON["RE"]'` agree on every sample (`/usr/bin/awk → gawk 5.4.1`). The fix does not change what the arms match, only how they read.

## 4. Scratch hygiene

Every counter run removed its `matcher-r50.*` work dir; `find` on all nine scratch roots shows 0 residual entries after exit. Probe scripts were written only under `/fast/scratch/hyaku/tsukuroi-r50/R50RevCounterC2/` (removed after copying receipts). No lane byte, fleet file, or PATH directory was touched; fixture scripts run `bash <file> --selftest` and write only under `--scratch`/`work` (the stateful fixtures write one counter file under my own scratch). One background job (`bg_16136`) ran three counter invocations serially; captured output saved in this file's receipts notes.

## 5. Proposed text (counter-side repairs, if the L1 routes them)

1. Widen `IDIOM_RE` to the defect class, not the spelling: `printf ['"]%s\\n['"] "\$\{?(?:[A-Za-z_]\w*)\}?"\s*\|\s*(?:grep\s+(?:-[a-zA-Z]*q|--quiet|-m1)|head -n1|grep [^\n]*\|\s*head -n1)` — i.e. any variable, both format quotings, all quiet/early-exit grep flags, optional braces and whitespace; add `echo ...\s*\|` and `<<<` as a secondary warning leg.
2. Gate `p.returncode`: `pass_runs += 1 if (m and rc == 0 and PASS and 0 failed)` — record, then require.
3. Per-run legs: `cases_run_ok = all(int(m.group(2)) == 168 for m in runs)` and `case_ok = all(any('(R50-C2)' in ln and ln.startswith('PASS ') for ln in run) for run in runs)`.
4. Provenance: emit `census_source: 'revision-blob' | 'file'`, and when `--census-file` is used either refuse a `--revision` that isn't a readable commit or stamp `revision_validated: 0`.
5. `pass_runs == a.runs` → keep, but derive the printed predicate from `a.runs` (`f'pass_runs == {a.runs}'`), and print a one-line warning when `--runs < 2` weakens the flake control.
6. Docstring fixes: `6 at base` → `7 at base b866a1d3`; usage line → "`--scratch` required (also with `--census-file`)"; add "cases is pinned at 168 — a suite that grows must re-pin".
7. For the stub hole: `case_ok` should additionally require the census *source* to contain an executable `(R50-C2)` arm (e.g. the `buf_has "$r50_probe"`/`r50_t` loop shape), not only printed PASS text — same repair style as routed defect 4 named for `check-fd-band-r49.py`.

## 6. Not done / honesty notes

- I did not run `strace`; the D-13 seat owns the scratch-contract audit. Leftover check above is `find`-based, not syscall-level.
- The `--runs` downgrade (MED-4) is a CLI-surface defect only if an operator passes `--runs 1` for a real measurement; the w1 D-8 item does so, but for a base-control where FAIL is the expected outcome either way.
- `run_detail` was elided from F2/F2b/F3/F5 console prints at collection time by my own printer (`d.pop("run_detail")`); all legs reported from those runs are the complete top-level fields. The four files `mut.*.diff` + the verbatim observed outputs are the receipts for those.
- The lane was read-only throughout; every fixture/counter run executed inside `/fast/scratch/hyaku/tsukuroi-r50/R50RevCounterC2/`, which was deleted after receipts were copied here. No tool installs were needed (system python3 + bash 5.3.20 only).

Receipts in `.ufo/waves/round-50/w1/R50RevCounterC2/`: `counter.py`, `census.{base,freeze}.sh`, `idiom-sites-at-revs.out`, `idiom-matrix.out`, `probe.sh`, `probe5.out`, `probe2.{sh,out}`, `freeze-counter.json`, `f1-stub.json`, `f4-runs1.json`, `f6-flaky.json`, `f7-rcign.json`, `f8-state.json`, `u1-noscratch.json`, `mut.{braced,dqfmt,extra}.diff`, `stub.sh`, `rc-ignored.sh`, `stateful.sh`, `flaky.sh`.
