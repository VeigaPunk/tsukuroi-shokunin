# Seat ExecRegistry — round 99, wave w1

Role: executor (leaf). Target: **measure C2** — the landed registry-content binding, the two capture
closures (hybrid / same-cell restatement), the M07 ancestor kill, and the coverage gate.
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Pinned tip `f107da3afe511f7db8cdc30235a992b774903158`.
Scratch root: `/fast/scratch/hyaku/tsukuroi-r99/ExecRegistry` (deleted after the receipts were
copied; every witness cited below is a file **under this seat dir**).

No tool was installed or upgraded; `pacman` was not touched (host-wide pause). All commands ran with
`TMPDIR` pointed at the scratch root.

---

## 0. Instrument integrity (before any measurement)

```
$ cd tsukuroi-shokunin && sha256sum -c .ufo/waves/round-99/before/instruments.sha256
tools/limine-pin-battery-r99.py: OK
tools/make-r99-bends.py: OK
tools/check-registry-content-r99.py: OK
tools/check-limine-pins.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
tools/limine-pin-battery-r98.py: OK
tools/check-registry-content-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-99/before/controls/do-nothing-checker-r98.py: OK
.ufo/waves/round-99/before/controls/bends/N09-y-era.py: OK
.ufo/waves/round-99/before/controls/bends/N11-x-era.py: OK
.ufo/waves/round-99/before/dev/make-fixtures.py: OK
.ufo/waves/round-95/before/controls/count-runs.py: OK
.ufo/plans/round-99.md: OK
EXIT=0
```

Re-verified **after** all measurements (`instruments-recheck.txt`): rc 0, **16 lines OK**, so the
`void` clause of C2 does not trigger and no measurement is read across a byte change.

Measured at the same time (`span-binding-bytes.txt`), the two capture forms — the r99 change is the
boundary guard plus `unique`:

```
tools/check-registry-content-r98.py:261   "capture": r"VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))", "derive": "variant_span",
tools/check-registry-content-r99.py:281   "capture": r"VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))(?![0-9,-])", "derive": "variant_span",
tools/check-registry-content-r99.py:282   "unique": True, "tool": "tools/make-r96-bends.py"},
```

---

## 1. Landed surface — both checkers at the pinned pre-round tip

```
$ python3 tools/check-registry-content-r99.py --revision f107da3afe511f7db8cdc30235a992b774903158 \
    --json <seat>/c2-content-tip.json
registry-content: status PASS bindings 7/7 findings 0
RC=0
$ python3 tools/check-registry-content-r98.py --revision f107da3afe511f7db8cdc30235a992b774903158 \
    --json <seat>/c2-content-tip-r98.json
registry-content: status PASS bindings 7/7 findings 0
RC=0
```

Receipts: `landed-two-checkers.txt`, `c2-content-tip.json` (`status PASS`, `bindings 7`,
`findings []`), `c2-content-tip-r98.json` (`status PASS`, `bindings 7`, `findings []`).

## 2. Fixtures (the two capture closures)

```
$ python3 .ufo/waves/round-99/before/dev/make-fixtures.py /fast/scratch/hyaku/tsukuroi-r99/ExecRegistry/fixtures
built .../fixtures/clean
built .../fixtures/hybrid
built .../fixtures/restated
built .../fixtures/gap
RC=0
```

Eight legs, `--root <fixture>` (`fx-legs.txt`; one JSON per (checker, fixture)):

```
=== r99 / clean ===     registry-content: status PASS bindings 7/7 findings 0          RC=0
=== r98 / clean ===     registry-content: status PASS bindings 7/7 findings 0          RC=0
=== r99 / hybrid ===    FINDING RC-CELL-MISSING SKILL.md:10 make-r96-bends cell 5 no longer states
                        'VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))(?![0-9,-])'
                        registry-content: status FAIL bindings 6/7 findings 1          RC=1
=== r98 / hybrid ===    registry-content: status PASS bindings 7/7 findings 0          RC=0
=== r99 / restated ===  FINDING RC-CELL-AMBIGUOUS SKILL.md:10 make-r96-bends cell 5 mentions
                        'VARIANTS' 2 times; the first mention is not the cell's value
                        registry-content: status FAIL bindings 6/7 findings 1          RC=1
=== r98 / restated ===  registry-content: status PASS bindings 7/7 findings 0          RC=0
=== r99 / gap ===       registry-content: status PASS bindings 7/7 findings 0          RC=0
=== r98 / gap ===       registry-content: status PASS bindings 7/7 findings 0          RC=0
```

The r98 blind reading is reproduced exactly: r98 `PASS 7/7` on both capture shapes, r99 `FAIL` with
**exactly one** finding and the frozen id on each (`RC-CELL-MISSING` on the hybrid cell
`VARIANTS N01-N04,N05`; `RC-CELL-AMBIGUOUS` on `VARIANTS N01,N03 then VARIANTS N01-N03`).
Both checkers read `PASS 7/7` on `clean` and `gap` (the r97 M08 branch stays green).

## 3. r99 `--selftest`

```
$ python3 tools/check-registry-content-r99.py --selftest
clean                PASS
default-cell         PASS
fixtures-cell        PASS
schema-cell          PASS
roster-pinned-cell   PASS
roster-verdict-cell  PASS
cases-cell           PASS
span-cell            PASS
span-gap             PASS
span-gap-lie         PASS
span-hybrid          PASS
span-restated        PASS
row-missing          PASS
tool-missing         PASS
derivation-lie       PASS
tally-lie            PASS
ancestor             PASS
selftest PASS 17/17
RC=0
```

Receipt `r99-selftest.txt` (all 17 lines). The r98 control in the same environment:
`r98-selftest.txt` → `selftest PASS 14/14`, RC=0.

## 4. M07 mutant (ancestor check skipped)

Both checkers copied byte-identically into scratch, then the two logical statements
(`p = self._git("merge-base", "--is-ancestor", …)` and the `raise TableError`) replaced by
`pass  # M07: ancestor check skipped`:

```
--- tools/check-registry-content-r99.py
+++ mut/m07-r99.py
@@ -243,9 +243,7 @@
         p = self._git("rev-parse", "--verify", self.revision + "^{commit}", check=False)
         if p.returncode != 0:
             raise TableError("revision %r does not resolve" % self.revision)
-        p = self._git("merge-base", "--is-ancestor", self.revision, self.branch, check=False)
-        if p.returncode != 0:
-            raise TableError("revision %r is not an ancestor of %s" % (self.revision, self.branch))
+        pass  # M07: ancestor check skipped
```

Identical hunk against the r98 checker (`m07-mutant-diff.txt`). Mutant digests
(`m07-mutant-sha256.txt`), sources kept as `mut/m07-r99.py`, `mut/m07-r98.py`:

```
1ac9857fbea1b8ac7e8d6395128f175454d801c7e9667bf2202f873c328af441  mut/m07-r99.py
cba14ee1a96a0aef357dbceb96bdc8dd1c90e9c44d8cf2ebd51ddbc68dd7f101  mut/m07-r98.py
```

Selftests (`m07-on-r99-selftest.txt`, `m07-on-r98-selftest.txt`):

```
$ python3 mut/m07-r99.py --selftest
clean                PASS
default-cell         PASS
fixtures-cell        PASS
schema-cell          PASS
roster-pinned-cell   PASS
roster-verdict-cell  PASS
cases-cell           PASS
span-cell            PASS
span-gap             PASS
span-gap-lie         PASS
span-hybrid          PASS
span-restated        PASS
row-missing          PASS
tool-missing         PASS
derivation-lie       PASS
tally-lie            PASS
ancestor             FAIL rc=0 registry-content: status PASS bindings 7/7 findings 0
selftest FAIL 16/17
RC=1
$ python3 mut/m07-r98.py --selftest
clean                PASS
default-cell         PASS
fixtures-cell        PASS
schema-cell          PASS
roster-pinned-cell   PASS
roster-verdict-cell  PASS
cases-cell           PASS
span-cell            PASS
span-gap             PASS
span-gap-lie         PASS
row-missing          PASS
tool-missing         PASS
derivation-lie       PASS
tally-lie            PASS
selftest PASS 14/14
RC=0
```

The only red case on r99 is `ancestor`, and its reading is the kill direction: the mutant makes the
non-ancestor leg read rc 0 `PASS` where the frozen expectation is rc 2 `CANNOT-EVALUATE`. On the r98
checker the same mutation is invisible — `PASS 14/14`, the r98 MutRegistry M07 survivor reproduced.

## 5. Independent ancestor probe (pristine vs mutant)

A two-branch fixture repo was built in scratch; the non-ancestor revision is a `commit-tree` child of
`master` (so no checkout/switch was needed). Toplevel asserted before the commit:

```
fixture=/fast/scratch/hyaku/tsukuroi-r99/ExecRegistry/probe/ancestor
master=1d8d7f3b1b7e3cc259611d327f30862900f94c0c
side=50b7647c017a3adfb15e12c953e43e31f76b1d45  (commit-tree child of master, not an ancestor of master)
$ python3 tools/check-registry-content-r99.py --revision 50b764… --branch master
CANNOT-EVALUATE: revision '50b7647c017a3adfb15e12c953e43e31f76b1d45' is not an ancestor of master
RC=2
$ python3 <m07-mutant> --revision 50b764… --branch master
registry-content: status PASS bindings 7/7 findings 0
RC=0
```

Receipts `ancestor-probe-fixture.txt`, `ancestor-probe-pristine.txt`, `ancestor-probe-mutant.txt`.
(First attempt ran the tool from the lane root, where its `ROOT` is the lane and the scratch commit
does not resolve — that run is not cited; the receipt above places the tool inside the fixture, as
the selftest case does.)

## 6. Coverage gate at the pinned tip

`--revision` is the only CLI form (the tool takes no `--json`; stdout is the JSON):

```
$ python3 tools/check-registry-coverage.py --revision f107da3afe511f7db8cdc30235a992b774903158
{"branch":"master","branch_tip":"f107da3afe511f7db8cdc30235a992b774903158",
 "counts":{"findings":0,"missing":0,"registered":160,"rows_total":160,"tools_total":160},
 "findings":[],"revision":"f107da3afe511f7db8cdc30235a992b774903158","status":"PASS"}
RC=0
```

Receipt `coverage-tip.json` (plus `coverage-tip.err`, 0 bytes).

---

## Acceptance, line by line

| Expected line | Observed | Verdict | Receipt |
|---|---|---|---|
| r99 landed `PASS 7/7 findings 0` | `PASS bindings 7/7 findings 0`, rc 0 | PASS | `c2-content-tip.json` |
| r98 landed `PASS 7/7` | `PASS bindings 7/7 findings 0`, rc 0 | PASS | `c2-content-tip-r98.json` |
| r98 `PASS 7/7` on `hybrid` (blind) | `PASS 7/7 findings 0`, rc 0 | PASS | `fx-r98-hybrid.json` |
| r98 `PASS 7/7` on `restated` (blind) | `PASS 7/7 findings 0`, rc 0 | PASS | `fx-r98-restated.json` |
| r99 `FAIL` one finding `RC-CELL-MISSING` on `hybrid` | `FAIL 6/7 findings 1`, `RC-CELL-MISSING`, rc 1 | PASS | `fx-r99-hybrid.json` |
| r99 `FAIL` one finding `RC-CELL-AMBIGUOUS` on `restated` | `FAIL 6/7 findings 1`, `RC-CELL-AMBIGUOUS`, rc 1 | PASS | `fx-r99-restated.json` |
| both `PASS 7/7` on `clean` | r99 PASS rc 0 / r98 PASS rc 0 | PASS | `fx-r99-clean.json`, `fx-r98-clean.json` |
| both `PASS 7/7` on `gap` | r99 PASS rc 0 / r98 PASS rc 0 | PASS | `fx-r99-gap.json`, `fx-r98-gap.json` |
| r99 selftest `PASS 17/17` | `PASS 17/17`, rc 0 | PASS | `r99-selftest.txt` |
| M07 on r99 `FAIL 16/17`, only `ancestor` red, reads rc 0 `PASS` | `FAIL 16/17`; `ancestor FAIL rc=0 … status PASS`; rc 1 | PASS | `m07-on-r99-selftest.txt` |
| M07 on r98 `PASS 14/14` (survivor) | `PASS 14/14`, rc 0 | PASS | `m07-on-r98-selftest.txt` |
| coverage `PASS`, `tools_total 160`, `registered 160`, `findings 0` | `status PASS`, `tools_total 160`, `registered 160`, `findings 0`, `missing 0`, `rows_total 160`, rc 0 | PASS | `coverage-tip.json` |
| instruments manifest all OK at scoring time | 16/16 OK (before **and** after the runs) | PASS | `instruments-recheck.txt` |

Target clause of C2 additionally names `bindings 7` on the landed run and the r98 landed `PASS`;
both observed verbatim.

## Risks / notes (not defects in this measurement)

- `--revision` in the content checker resolves its git root from the tool's own location (`ROOT`),
  not from the caller's cwd; a probe run from the lane root reports `does not resolve` for a scratch
  commit. This is instrument behavior, byte-frozen this round, and it is why the probe in §5 runs the
  tool from inside the fixture. Not raised as a finding (out of scope, bytes frozen).
- `check-registry-coverage.py` has no `--json`; a `--json` argument trips the `exit_on_error=False`
  CLI branch and yields `CANNOT_EVALUATE`/`E-CLI`. Recorded because my first invocation hit it; the
  cited receipt is the clean run.
- The fixture driver emits four files; `fx-r98-{clean,hybrid,restated,gap}.json` are byte-identical
  (a `--root` payload carries `revision: null`, 4 rows, no findings) — the four legs were still run
  separately and are cited separately.
- Scratch `/fast/scratch/hyaku/tsukuroi-r99/ExecRegistry` removed after the mutants and probe
  receipts were copied into this seat dir; `mut/m07-{r99,r98}.py` are the exact run bytes (sha256
  above), so the diff is replayable without scratch.
- No axis was touched beyond C2's instruments; nothing under `tools/`, `SKILL.md`, `corpus/`, or the
  frozen wave dirs was written. No git/jj mutation: the only commits were made by `commit-tree`
  inside the scratch fixture repo after `rev-parse --show-toplevel` printed that fixture path.

{"seat":"ExecRegistry","verdict":"met","notes":"C2 measured at f107da3a: r99 landed PASS 7/7 findings 0 (rc0); r98 landed PASS 7/7; fixtures: r98 blind PASS 7/7 on hybrid+restated while r99 FAILs with exactly one finding (RC-CELL-MISSING hybrid, RC-CELL-AMBIGUOUS restated), both PASS on clean+gap; r99 selftest PASS 17/17; M07 mutant (ancestor check replaced by pass) FAIL 16/17 with only ancestor red reading rc 0 PASS, and the same mutant on the r98 checker PASS 14/14 (survivor reproduced); independent two-branch probe: pristine rc 2 CANNOT-EVALUATE 'not an ancestor of master', mutant rc 0 PASS; coverage PASS tools_total 160 registered 160 findings 0 missing 0 at f107da3a; instruments.sha256 16/16 OK before and after the runs."}
