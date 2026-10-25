# Verifier2Claim262 — Independent pre-data control audit item 2/4 (C3)

Seat: critic Verifier2Claim262 · wave tsukuroi-r37-w1 · milestone: Independent before-data control audit
Date: 2026-10-25 · lane HEAD at run time: `0e5f70fadba12bc9bbb9db564c2262c2c0194535`

## Claim audited (one distinct claim: C3 self-assessment mismatch repair)

- Claim/builder: Build9C341 (`build:C3 baseline control design`) and the wave-level
  before/after receipts. Frozen C3 predicate (quoted from `Build9C341.md:41`,
  opened this round): "Frozen C3 predicate (declaration, `SCORECARD.md`
  round-37 correction section): `mismatches == 0 && checked == 27 && exit == 0`."
- Declared work the control skips: correcting the five stale round-35 axes
  cells K07–K11 in `SCORECARD.md` (`55→56`, `3009→3110`, `784→839`,
  `46→49`, `256→269`; `patch-r35-axes-C3.patch`).

## Cheapest do-nothing control (skips all declared correction work)

Score the frozen predicate on committed baseline bytes only — run the checker
on the round-36 verifier spot-check revision `564db0b` (the frozen before
receipt revision) with no patch, no cell edit, no correction commit:

```
git -C <lane> archive 564db0b614b2914de5452f9ebd537a0653ae1de5 | tar -x -C $FIX
# fresh mktemp repo; top-level verified == fixture root before commit (git rev-parse --show-toplevel)
python3 <lane>/tools/check-self-assessment.py --repo $FIX --revision <baseline_fixture_commit>
```

Observed output (stdout, `before-donothing.json`; stderr 0 bytes):

```
{"revision": "8ef7923…", "checked": 27, "mismatches": 5, "status": "FAIL", "declaring_round": 35, ...}
mismatch ids: K07,K08,K09,K10,K11
exit = 1
```

Exit: **1**. Predicate score: `mismatches==0` false → **FAIL**.

### Reachability verdict

**Target NOT reachable without claimed work.** The do-nothing control fails the
frozen predicate exactly as the committed receipt does: byte-identical per-cell
stated/observed values vs `before/c3-before.json` (K07 55/56, K08 3009/3110,
K09 784/839, K10 46/49, K11 256/269; checked=27, mismatches=5, FAIL; exit=1
matches `before/c3-before-exit.txt`). The five-cell correction is therefore
non-vacuous: the measured red-before state is genuinely present in committed
baseline bytes (`SCORECARD.md` blob `bc2dc8ce28da603c4dd721226cb04711d0d6d3ec`
at 564db0b — matches patch index line `index bc2dc8c..2a51bef`).

## Counterexample resolution (local evidence discrepancy)

`Build8C340/run.log` shows `exit=0 status=FAIL checked=27 mismatches=5` then
`FATAL: baseline must exit 1`. Reproduced the exact sibling harness shape
(`out="$(python3 "$CHECKER" --repo "$FIX" --revision "$1" 2>&1)" || true; printf`):
the checker's exit is swallowed by `|| true` + final `printf`, so `BEFORE_EXIT=$?`
is always 0. Direct invocation of the same checker on the same baseline bytes
exits **1**. The run.log `exit=0` is a harness artifact, not a checker defect;
`c3-before-exit.txt` exit=1 stands.

## Tooling

No installs/updates (RULES.md read first; existing python3/git/bash; no
pacman/host changes). No lane/fleet/sibling writes; fixture git confined to
mktemp; lane read-only (`git archive`/`rev-parse`/`cat-file` only).

## Sources opened this round (2026-10-25, located quotes)

- `tools/check-self-assessment.py:799-810` — "mismatches = sum(1 for record in checks if record['status'] == 'mismatch')" / "return result, (EXIT_PASS if mismatches == 0 else EXIT_MISMATCH)"; `:74-76` EXIT_PASS=0, EXIT_MISMATCH=1.
- `.ufo/waves/round-37/w1/Build9C341.md:41` — frozen predicate quote above; `:47` "Baseline fixture commit `22f1d85` → `rc=1`, checked=27, mismatches=5".
- `.ufo/waves/round-37/before/c3-before.json` / `c3-before-exit.txt` — "mismatches: 5", "status": "FAIL", `exit=1`.
- `.ufo/waves/round-37/w1/Build8C340/c3_mismatch_correction_check.sh:65-70` — `run_check` swallows exit with `|| true` + `printf`; `:94` "FATAL: baseline must exit 1"; `run.log:9-10` observed exit=0.
- `.ufo/waves/round-37/w1/Build9C341/patch-r35-axes-C3.patch:2` — "index bc2dc8c..2a51bef".
