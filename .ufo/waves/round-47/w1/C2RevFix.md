VERDICT: supports

Item: C2-R1 — review of the C2 fix in tools/tsukuroi-census.sh, base 916019057147d7e9ba6b137647b2cee26decf4b8 vs freeze 77e9e2b2e96b85d8f048ae2087e246a542b71611. Per-change verdicts below, then the three design questions.

# 0. Byte scope reviewed

`git -C …/tsukuroi-shokunin diff 91601905..77e9e2b -- tools/tsukuroi-census.sh` has exactly four hunks (receipt: `.ufo/waves/round-47/w1/C2RevFix/census.diff`):

1. header comment, freeze lines 408–412 (read-only guarantee paragraph)
2. `--selftest` usage text, freeze lines 598–602
3. `st_base` guard at the top of `run_selftest`, freeze lines 2050–2059
4. two `(R47-C2)` selftest cases, freeze lines 3473–3482

`git -C …/tsukuroi-shokunin diff 77e9e2b..HEAD --stat -- tools/tsukuroi-census.sh` is empty (lane HEAD f6bc6d056ebdf79a585745d4292faf90ae12d9fd): the working-tree script is byte-identical to the freeze, so the reviewed bytes are the counted bytes.

# 1. Per-change verdicts

## 1.1 st_base guard (freeze:2050–2059) — CORRECT, keep

```
local st_base=${TMPDIR:-/tmp}
case "$st_base" in
  *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;
esac
work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")
```

- The bracket expression `[!A-Za-z0-9._/+-]` is character-for-character the refusal class of `root_locator_class` (freeze:850–866, `*[!A-Za-z0-9._/+-]*) printf 'unsafe'`). I property-tested the equivalence: 104 probes (space, `=`, tab, newline, both quotes, backslash, DEL, non-ASCII `é`, glob metacharacters `* ? [ ]`, and a full printable-ASCII 33–126 sweep) plus in-charset controls — the guard falls back to /tmp exactly when the locator would refuse the derived fixture root. Receipt: `.ufo/waves/round-47/w1/C2RevFix/equiv-probe.sh` (+ `rlc-fn.sh`, the extracted classifier), output line: `EQUIVALENCE: guard fallback == locator refusal on all 104 probes; in-charset controls stay absolute`.
- The mktemp suffix `tsukuroi-r3-2-selftest.XXXXXX` (hyphen, dots, alnum) is itself entirely in-charset, so `root_locator_class "$work"` cannot disagree with the guard's decision.
- `st_base` is declared `local` and referenced only at freeze:2055–2059; `work` is assigned only here and every `$work` use (freeze:2063–3481) lies inside `run_selftest` (2048–3487). Nothing leaks to live mode.

Design question — is /tmp fallback right vs the two alternatives?

- **(i) fail fast on unsafe TMPDIR: rejected.** The hermetic selftest grades the census, not the caller's environment; round-46 w1/C1ExecRerunB (.ufo/waves/round-46/w1/C1ExecRerunB.md:112) shows the environmental red (149 failed) blocked a wave while saying nothing about census behavior. Fallback keeps the 162 case verdicts hermetic and the operator experience clean. The guard comment's "149" is historically accurate (C1ExecRerunB observed 149 failed; my base rerun under the round-47 counting command reproduces exactly 149 failed of 162).
- **(ii) space-free subdir under TMPDIR: does not solve the problem.** If `TMPDIR="/x y"`, any subdir `/x y/clean` still contains the space and is still refused by the locator; only whole-path sanitization or /tmp fallback works. The fixture tree is a few KB of text stubs, cleaned by the EXIT trap, and the pre-fix default location when TMPDIR is unset was already /tmp — no size, security, or behavioral regression.
- Residual observation, not a defect against this claim: a *relative* TMPDIR (e.g. `TMPDIR=.`) passes the charset guard but yields a relative `$work`, and then new case 1 fails red (1 case, loud) rather than falling back. Pre-existing posture — base did the same minus the pin — and the declared counting command uses an absolute TMPDIR. A future hardening could extend the fallback to `*/*`-absence; out of scope here.

## 1.2 Two (R47-C2) cases (freeze:3473–3482) — CONTRACT PINS, keep

- **Case 1** (`root_locator_class "$work"` = `absolute`): pins the behavioral contract "the harness's fixture base is always a valid root override, however dirty TMPDIR is". It is implementation-agnostic — any future rework of base derivation must still yield an absolute-classifiable path. Its discriminating power engages exactly under the declared counting command.
- **Case 2** (`mkdir -p "$work/fx/sp dir/root"` → `unsafe`): pins the classifier contract "whitespace in an override ⇒ unsafe ⇒ BLOCKED before stat, never echoed" that `probe_root_meta` (freeze:882–887) relies on. It complements rather than duplicates the end-to-end case `blocked-root-unsafe-override` (freeze:2977–2981, full PLANE line asserted): case 2 catches a classifier regression even if the end-to-end line format drifts. Placement at the end of the selftest (after all fixture cases, before the summary printf at 3484) touches no other fixture; no glob iterates `$work/fx` (verified by grep), and the EXIT trap removes the tree.
- Empirics, all `LC_ALL=C`, scratch under /fast (receipts `freeze-dirty.log`, `freeze-clean.log`):
  - base under `TMPDIR="$S/t 2"`: `TSUKUROI_CENSUS_SELFTEST: FAIL (162 cases, 13 passed, 149 failed)` — reproduces the C2 defect exactly (149-failure count matches the round-46 observation).
  - freeze under `TMPDIR="$S/t 2"` (the counting command): rc 0, `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`, both R47-C2 lines PASS, all eight `(R46-C1)` lines PASS.
  - freeze under a clean space-free TMPDIR (control): rc 0, PASS 164/164 — the new cases do not false-fail in the default configuration; case arithmetic 162+2=164 confirmed; zero FAIL lines in both freeze runs.

## 1.3 Comment update (freeze:408–412) — ACCURATE, keep

The added sentence ("or /tmp itself when TMPDIR holds characters the root-override locator refuses — R47-C2") matches the guard's semantics as proven by the equivalence probe; it sits inside the read-only-guarantee comment block and changes no behavior. The usage text at 598–602 says the same in one line. Both are truthful descriptions of the new fallback.

# 2. Live-mode non-interference — PROVEN

The claim requires that the guard change no live-mode path; the diff proves it structurally and the call graph confirms it:

- Hunks 1–2 are comment and `--help` usage text (verified in context at freeze:405–413 and 596–604).
- Hunk 3 (`st_base`) and hunk 4 (cases) live entirely inside `run_selftest` (2048–3487), which `main` reaches only from the `--selftest` branch (freeze:3567–3570). Live mode runs the seven probes plus the neutral DRIFT/STORAGE/SCRUB arms and never enters `run_selftest`.
- `root_locator_class` — the live-critical function called by `probe_root_meta` at freeze:882 — is outside all four hunks; identical bytes at base and freeze.
- `census_identity`, the `--identity` path, the exit map (`exit 0/1/2` at freeze:3629–3634), and all PLANE line formats are outside the hunks. Exit map unchanged; `--identity` line shape unchanged (the identity cases are selftest-side and pass unchanged).

# 3. Answers to the item's three questions

1. **/tmp fallback vs alternatives:** fallback is the right design — fail-fast would hostage the hermetic suite to the environment, and a space-free subdir under a dirty TMPDIR still carries the unclassifiable parent path. Guard's charset is provably identical to the locator's refusal class.
2. **Live-mode impact:** none. Only comments/usage/selftest hunks; `st_base`/`work` are selftest-local; `root_locator_class` and all live probes byte-unchanged.
3. **Contract vs implementation:** both new cases pin observable contracts (fixture base always absolute-classifiable; whitespace override always unsafe), not implementation details; case 2 has independent end-to-end backup at freeze:2977–2981.

# 4. What I did not do

- I did not run the live census (read-only by design, but the diff alone proves live non-interference; no live behavior was needed as evidence).
- I did not re-verify the full kill-rule battery (identity byte-identity under live mode, six R46-C1 cases at base) — the dirty-TMPDIR runs cover the selftest-side parts; the L1's counting command seat owns the scored rerun.

No defect found. The fix admits C2 as declared.
