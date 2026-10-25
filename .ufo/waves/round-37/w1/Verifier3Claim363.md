# Verifier3Claim363 — Independent before-data control audit (item 3/4)

## Target and exact predicate

I selected C3 (calibration), the round-37 correction replacing the withdrawn verified-rate-ledger claim. The frozen predicate in `SCORECARD.md:1958-1968` is `mismatches == 0 && checked == 27 && exit == 0` for `python3 tools/check-self-assessment.py --revision <REV>`. Claimed work: correct five stale current self-assessment count cells (K07-K11) while leaving checker bytes and its 27 checks unchanged.

## Cheapest do-nothing control

Run that checker against the committed declaration baseline itself, without any correction:

```sh
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
python3 tools/check-self-assessment.py --revision 564db0b614b2914de5452f9ebd537a0653ae1de5
```

Observed this round: JSON `revision=564db0b614b2914de5452f9ebd537a0653ae1de5`, `checked=27`, `mismatches=5`, `status=FAIL`; K07-K11 are mismatches. Shell exit: **1**. The committed baseline receipt `.ufo/waves/round-37/before/c3-before.json` records the same revision and counts; its companion `c3-before-exit.txt` says `exit=1`.

This control skips the declared cell corrections entirely. Against the exact frozen conjunction it fails both the zero-mismatch and zero-exit requirements, despite satisfying `checked == 27`. **Target reachable without claimed work? No, not on this frozen baseline revision.** The C3 target is specifically the measured round-37 tip, so baseline red alone does not prove that all alternative/no-op revisions fail; it proves this declared starting revision is red. The after receipt `after-c3-0e5f70.json` is consistent with the claimed endpoint (27 checks, 0 mismatches, PASS), but this audit's control is the baseline, not a substitute for validating the correction's causal provenance.

## Falsification / minimum safe qualification

The declared control is useful and falsifies the simplest do-nothing-on-base strategy. Do not generalize it to “a no-change control at any revision is unreachable”: if a revision already contains corrected values, running the same fixed checker there could meet the predicate without this round doing the work. Freeze/prove the exact pre-correction base as the no-change control and bind the after revision to the append-only correction commit (same checker blob and fixed check population). The SCORECARD declaration's baseline hash and receipt provide that base binding.

Axes impacted: **calibration (C3)** and **claims/falsification**; no C1/C2 conclusion.

Tooling: read `/home/vgpnk/.omp/agent/RULES.md` first. No installation/update performed; no package transaction, host change, lane write, or git/jj state mutation performed. The checker run reads committed bytes only.

Report: `.ufo/waves/round-37/w1/Verifier3Claim363.md`
