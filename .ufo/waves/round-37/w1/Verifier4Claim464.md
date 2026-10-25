# Verifier4Claim464 — Independent pre-data control audit (item 4/4)

**Seat:** Verifier4Claim464 (critic). **Axes:** C3 calibration (self-assessment mismatch
repair, 27 fixed checks). **Milestone:** Independent before-data control audit.

## Claim audited (C3, one distinct claim)

Build8C340 (design item 8/12) and Build9C341 (control 9/12) claim:

> At the declaration base `564db0b…`, `tools/check-self-assessment.py` runs 27 fixed
> checks (K01–K27), reports exactly 5 mismatches (K07–K11), status FAIL, exit 1.
> Applying the five-cell correction to the round-35 axes table (depth row: 55→56
> notes, 3009→3110 `SKILL.md` lines, 784→839 table lines, 46→49 lesson files;
> coverage row: 256→269 `corpus/README.md` lines) makes the same 27 checks report
> 0 mismatches, status PASS, exit 0.

**Frozen predicate (from the checker, verified by execution):** `status == "PASS"` iff
`mismatches == 0`; `EXIT_PASS=0` iff PASS, `EXIT_MISMATCH=1` iff mismatch; `checked=27`
for the round-35 axes heading (`K01–K27` in `tools/check-self-assessment.py` lines
74-76, 810; `evaluate()` / `main()`).

## Do-nothing control (cheapest, skips all declared work)

Cheapest control that skips the declared work — no fixture, no `git archive`, no
patch, no checker execution — and scores the frozen predicate from **committed
baseline bytes only** (`.ufo/waves/round-37/before/c3-before.json`):

```sh
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); mm=[c["id"] for c in d["checks"] if c["status"]!="match"]; print("checked=%d mismatches=%d status=%s ids=%s"%(d["checked"],len(mm),d["status"],",".join(mm)))' \
  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-37/before/c3-before.json
```

**Observed output:** `checked=27 mismatches=5 status=FAIL ids=K07,K08,K09,K10,K11`
**Exit:** 0.

## Verdict

- The after-target (**0 mismatches / PASS / exit 0**) is **NOT reachable without the
  claimed work**: the committed baseline bytes score FAIL with exactly the five
  mismatches, and no subset of the five-cell correction reaches PASS (see below).
  The C3 correction claim is non-vacuous and **holds** against a do-nothing control.
- Command, output, and exit are recorded above; the control is reproducible.

## Evidence (all observed this round)

| # | Command | Output | Exit |
|---|---------|--------|------|
| 1 | `git -C <lane> archive 564db0b… \| tar -x -C <fixture>`; commit; `python3 tools/check-self-assessment.py --repo <fixture> --revision <HEAD>` | `status=FAIL checked=27 mismatches=5`, ids `K07..K11`, stated/observed `55/56, 3009/3110, 784/839, 46/49, 256/269`; stderr empty | **1** |
| 2 | five-cell patch (verified exactly as Build9C341 lines 92-100), commit, same checker | `status=PASS checked=27 mismatches=0`, remaining ids `[]`; stderr empty | **0** |
| 3 | depth-row-only patch (4 cells), same checker | `status=FAIL checked=27 mismatches=1`, ids `['K11']` | 1 |
| 4 | coverage-row-only patch (1 cell), same checker | `status=FAIL checked=27 mismatches=4`, ids `['K07','K08','K09','K10']` | 1 |
| 5 | do-nothing control (above) | `checked=27 mismatches=5 status=FAIL ids=K07..K11` | 0 |

- Fixture: fresh `mktemp` repo `/tmp/v4c464-fixture.xd9d6S`; top-level verified equal to
  fixture root before any commit; lane touched only via read-only `git archive` /
  `rev-parse`; no lane/fleet/sibling writes. Tool bytes at `564db0b` equal worktree
  (`sha256` `1e1ab611…` both), so runs 1-4 use the frozen tool.
- Run 1 output matches the canonical committed receipt exactly
  (`matches_canonical_receipt=True` vs `before/c3-before.json`); the exit file
  `before/c3-before-exit.txt` (`exit=1`) matches run 1.

## Finding on Build8C340's retained log (claims vs evidence)

Build8C340's seat log (`Build8C340/run.log`) records `exit=0` for the baseline run and
then `FATAL: baseline must exit 1`. This is a **harness artifact**, not a checker
failure: `run_check()` wraps the checker in `out="$(python3 …)" || true` and its last
command is `printf`, so `$?` is always 0. The checker's real exit at the baseline is 1
(run 1, and the committed `c3-before-exit.txt`). The seat's logged FATAL therefore does
not falsify the claim; the underlying checker behavior supports it. Smallest safe
correction: make `run_check()` propagate the checker exit (e.g., capture `$?` before
`|| true`, or drop the `|| true`), so the retained log's `exit=` line measures the
checker.

## Conclusion

One distinct C3 claim audited. The frozen predicate is byte-faithful to the committed
baseline receipt; the cheapest do-nothing control skips all declared work and cannot
reach the after-target (still `5` mismatches from committed bytes); partial corrections
each leave exactly their unpatched cells mismatched. Target reachability without claimed
work: **NO** — the claim holds, no premature saturation, no duplicate authority.
