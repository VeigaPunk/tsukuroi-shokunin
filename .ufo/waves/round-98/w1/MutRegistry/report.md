# Round 98 / wave w1 — seat MutRegistry

Mutation test of the two r98 instruments: `tools/check-registry-content-r98.py` (C2, freshness 9)
and `tools/limine-pin-battery-r98.py` (C1, depth 8). One-fault mutants were emitted in
`/fast/scratch/hyaku/tsukuroi-r98/MutRegistry` (never in the lane), each substitution asserted to
match exactly once, and every mutant was run against the same legs the instruments' own gates use:
the checker's `--selftest` plus the landed surface and the three doctored revisions D1/D2/D2lie;
the battery's landed gate plus the N07/N08 bends, plus `--selftest --reference` where it completed.

Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Frozen instrument manifest verified
27/27 OK at the seat's last measurement (`receipts/instruments-final.txt`). Lane tool bytes were
never edited; the pristine copies match the manifest lines exactly.

## 0. Verdict

- **Baselines reproduce both claims' after-states exactly.** Battery on the landed gate: `met
  105/105`, 420 cases, 0 error rows. N07: `103/105` unmet, `failed_families` exactly
  `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`. N08: `104/105` unmet, exactly
  `[LEADING-ZERO-NORMALIZE]`. Checker: `--selftest PASS 14/14`; landed tip `1cfeb5d5`
  `PASS 7/7 findings 0`; D1 `FAIL` one `RC-BEND-SPAN`; D2 `PASS`; D2lie `FAIL` one `RC-BEND-SPAN`;
  coverage `PASS 157/157 findings 0` on base, D1 and D2.
- **C2: 7 of 8 checker mutants killed; M08 dies exactly as the claim says.** The r98 `--selftest`
  reads `FAIL 12/14` on M08 with both gap cases red (`span-gap` emits `RC-VALUE-MISMATCH`,
  `span-gap-lie` emits nothing); the same mutation on the r97 checker reads `PASS 12/12`. The only
  survivor is M07 (ancestor check), which is outside `--selftest`'s construction and unobservable
  on any leg that inspects an ancestor — probed with a non-ancestor commit: pristine `rc 2`, M07
  `rc 0`.
- **C1: 2 of 5 battery mutants killed, 3 survive.** B04 is killed by the N07 leg (`104/105 [Z]`
  where pristine reads `103/105 [LZ, Z]`); B05 is killed by the landed and reference legs
  (`104/105 [Z]` where pristine reads `105/105`). **B01, B02 and B03 survive every committed leg**:
  each removes a metadata assertion that no bend in the r98 leg set exercises, and the battery's
  own selftest cannot see an assertion removal because its 12 lie kinds contain no
  `limine_version`/`visibility_era` member.
- **M09 answer:** the reverted capture is killed by the selftest, but only by **`span-gap`**
  (`FAIL 13/14`, got `RC-CELL-MISSING`); `span-gap-lie` still passes, and the D2 leg also kills it
  (`FAIL` where r98 must read `PASS`).
- **M10** is killed by both gap cases (`FAIL 12/14`) and by the D2/D2lie inversion.

## 1. Setup, instrument bytes, fixture revisions

```
$ mkdir -p /fast/scratch/hyaku/tsukuroi-r98/MutRegistry/{pristine,mutants,mutants-battery,receipts,work}
$ cp <lane>/tools/{check-registry-content-r98.py,limine-pin-battery-r98.py,check-registry-content.py,check-limine-pins.py} \
     /fast/scratch/hyaku/tsukuroi-r98/MutRegistry/pristine/
$ sha256sum pristine/*
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  check-limine-pins.py
2daf59267ed923370fd825c21d9ac33ec2fbe95f58216a125a5346b7540cb3a6  check-registry-content-r97.py
5bb1441eed435b407d3650af92f12f73f41f05ff45a5ad0b031d20c898abcc1e  check-registry-content-r98.py
8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87  limine-pin-battery-r98.py
```

Each sha equals its `.ufo/waves/round-98/before/instruments.sha256` line, so every measurement
below is against the frozen bytes.

The doctored surfaces were rebuilt in a scratch clone (the frozen
`before/fixtures/build-doctored-fixture-r98.sh` was **not executed** — it writes into
`before/fixtures/`; its steps were replayed verbatim against my own clone, including its
exactly-once assertions):

```
$ git clone --shared --bare -q <lane> $S/origin.git
$ git -C $S/origin.git update-ref refs/heads/master b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a
$ git clone -q $S/origin.git $S/clone
$ [ "$(git -C $S/clone rev-parse --show-toplevel)" = "$S/clone" ]   # asserted; exit 0
$ cp pristine/check-registry-content-{r98,r97}.py $S/clone/fixture/   # checker rides at fixture/
# D1: SKILL.md "r96 VARIANTS N01-N04" -> "r96 VARIANTS N01,N03" (count asserted == 1)
# D2: SKILL.md reset to base, drop N02/N04 VARIANTS entries, row -> comma form (count == 1)
# D2lie: row -> "r96 VARIANTS N01-N03" (count == 1)
$ git -C $S/clone -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local commit ...
base  b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a  tree 7466b5a1…
D1    fa4438950f8479ed87eb928686b6d30af96d23ac  tree 294c7dbe…
D2    53745bd75b3e52f4d5e8b6fa0f90785d78cd64bb  tree 1e6d6896…
D2lie 949e4a4223d87a260a2da0e794e77e5139aae6f0  tree d476e358…   (`receipts/doctored-revisions.txt`)
```

The frozen fixture commit hashes (`aab954f1…`, `d17ebc5…`, `3155fd3…`) are not in the lane object
database (the builder pushed them to its own scratch origin), so byte-identity could not be
re-asserted by hash; the recipe text and its exact-count doctors are identical. Disclosure: to let
the unchanged coverage gate (`_revision.bind` rule 6) certify the doctored revisions, the scratch
clone's `refs/remotes/origin/master` was pointed at D2lie (`git -C $S/clone update-ref …`); no
ref in the lane was touched and no commit was pushed anywhere outside the scratch clone.

## 2. Byte-level anchors (QUALITY 141)

`receipts/byte-offsets.txt`, offsets are `bytes.find` on the pinned bytes:

| instrument | site | byte offset |
|---|---|---|
| checker (24839 B, 5bb1441e…) | `derived = derive(binding, tree, work)` | 15608 |
| | `if declared != derived:` | 15993 |
| | `if not matches:` | 14702 |
| | `highest = max(number for number, _ in headings)` | 5780 |
| | `p = self._git("merge-base", "--is-ancestor"` | 10967 |
| | `if numbers != list(range(numbers[0], …))` | 8901 |
| | `"capture": r"VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))"` | 12754 |
| | `return ",".join(labels)` | 8975 |
| battery (115812 B, 8198bd84…) | `if c.check_echo and not (…)` | 98004 |
| | `if c.check_era and got[10] != (…)` | 98097 |
| | Z family `_era_first_line_panic(c, Z_DIGIT9…)` | 81794 |
| | LZ family `_era_first_line_panic(c, LEADING_ZERO_VALUES…)` | 83011 |
| | `return tuple(int(p) for p in version.split(".")) >= (12, 9, 5)` | 25050 |
| | `LIE_KINDS = (` | 106583 |

## 3. Baselines (pristine instruments)

| leg | expected (claim) | observed | verdict |
|---|---|---|---|
| checker `--selftest` | PASS 14/14 rc 0 | `selftest PASS 14/14`, rc 0 | PASS |
| checker `--revision base` (clone) | PASS 7/7 0 findings | `status PASS bindings 7/7 findings 0`, rc 0 | PASS |
| checker `--revision 1cfeb5d5` (real lane tip) | PASS 7/7 0 findings | `status PASS bindings 7/7 findings 0`, rc 0 | PASS |
| checker `--revision D1` | FAIL, exactly one `RC-VALUE-MISMATCH` | `1 findings`, `RC-BEND-SPAN states 'N01,N03' … derives 'N01-N04'`, rc 1 | PASS |
| checker `--revision D2` | PASS 7/7 | `status PASS … findings 0`, rc 0 | PASS |
| checker `--revision D2lie` | FAIL, exactly one `RC-VALUE-MISMATCH` | `1 findings`, `states 'N01-N03' … derives 'N01,N03'`, rc 1 | PASS |
| coverage gate base/D1/D2 | PASS 157/157 0 findings | `registered 157, tools_total 157, findings 0` ×3 | PASS |
| battery landed gate | met 105/105, 0 error rows | `105/105 verdict met`, cases 420, error_rows 0 | PASS |
| battery N07 | unmet 103/105 `[LZ, Z]`, 0 error rows | `103/105 … failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z`, 0 error rows | PASS |
| battery N08 | unmet 104/105 `[LZ]`, 0 error rows | `104/105 … failed LEADING-ZERO-NORMALIZE`, 0 error rows | PASS |

Receipts: `baseline-selftest.txt`, `baseline-{base,D1,D2,D2lie}.{txt,json}`,
`baseline-lane-tip.*`, `baseline-coverage-*.txt`, `baseline-{landed,N07,N08}.{txt,json}`.

The battery legs are `--runs 1` (the claim's 3-run loop is executor work; one run is sufficient to
classify a mutant, and the L1 capped the matrix at the emitted runs).

## 4. Checker mutants (`tools/check-registry-content-r98.py`)

Baseline for the comparison column: selftest `PASS 14/14` rc 0 · base `PASS` · D1 `FAIL 1` ·
D2 `PASS` · D2lie `FAIL 1`. All mutants one hunk (`receipts/checker-hunks.txt`).

| id | clause | selftest | base | D1 | D2 | D2lie | killed / survived | class |
|---|---|---|---|---|---|---|---|---|
| M01 | `derive()` returns the declared value (derivation vacuous) | **FAIL 3/14** | PASS 7/7 | PASS (blind) | PASS | PASS (blind) | **KILLED** | — |
| M02 | `declared != derived` branch deleted | **FAIL 4/14** | PASS | PASS (blind) | PASS | PASS (blind) | **KILLED** | — |
| M04 | `RC-ROW-MISSING` guard removed | **rc 1, `TypeError: object of type 'NoneType' has no len()`** | PASS | FAIL 1 | PASS | FAIL 1 | **KILLED** (crash on `row-missing`) | — |
| M06 | first exact heading, not the unique highest | PASS 14/14 | **FAIL 0/7, 7 findings** | **FAIL 0/7** | **FAIL 0/7** | **FAIL 0/7** | **KILLED** by every revision leg | — |
| M07 | `--revision` ancestor check skipped | PASS 14/14 | PASS | FAIL 1 | PASS | FAIL 1 | **SURVIVED** | outside-scope |
| M08 | `derive_variant_span` first-label-only | **FAIL 12/14** (`span-gap` → `RC-VALUE-MISMATCH`; `span-gap-lie` → `[]`) | PASS | FAIL 1 | **FAIL 1** (must PASS) | **PASS** (must FAIL 1) | **KILLED** (both gap cases + D2 inversion) | — |
| M09 | capture reverted to `N\d+-N\d+` | **FAIL 13/14** — only `span-gap` red (`RC-CELL-MISSING`) | PASS | FAIL 1 | **FAIL 1** (must PASS) | FAIL 1 | **KILLED** (`span-gap`, D2) | — |
| M10 | comma branch always derives `N01-N03` | **FAIL 12/14** (`span-gap` → mismatch; `span-gap-lie` → `[]`) | PASS | FAIL 1 | **FAIL 1** (must PASS) | **PASS** (must FAIL) | **KILLED** (both gap cases, D2/D2lie) | — |

Notes on the kill directions:

- **M08 vs the r97 checker:** the same one-line mutation applied to
  `before/controls/do-nothing-checker-r97.py` reads `selftest PASS 12/12` (rc 0,
  `receipts/M08-on-r97-selftest.txt`). The r98 gap cases are what turn the verdict.
- **M09** is the direct answer to "does the selftest kill the reverted capture, and which cases?":
  yes, but only `span-gap`, because with the comma-stating row no longer captured the checker emits
  `RC-CELL-MISSING` (expected `[]`). `span-gap-lie` still passes: the contiguous row is captured and
  the *pristine* derivation still returns the comma form, so that case cannot discriminate the
  capture revert on its own.
- **M06** turns all four revision legs red with 7 `RC-ROW-MISSING` findings (the first exact heading
  in `SKILL.md` is the round-18 table, which does not carry the four bound rows); the selftest's
  fixtures have one heading each, so it stays green.

## 5. Battery mutants (`tools/limine-pin-battery-r98.py`)

Baseline: landed `met 105/105` · N07 `103/105 [LZ, Z]` · N08 `104/105 [LZ]`. All mutants one hunk
(`receipts/battery-hunks.txt`).

| id | clause | landed | N07 | N08 | selftest | killed / survived | class |
|---|---|---|---|---|---|---|---|
| B01 | `meta_ok` ignores `check_echo` | met 105/105 | 103/105 `[LZ, Z]` (same) | **met 105/105** (pristine: unmet 104/105 `[LZ]`) | stopped at the wave cap, no tally (`selftest-aborted.txt`) | **SURVIVED** | genuine hole |
| B02 | `meta_ok` ignores `check_era` | met 105/105 | **met 105/105** (pristine: unmet 103/105 `[LZ, Z]`) | 104/105 `[LZ]` (same) | stopped at the wave cap, no tally (`selftest-aborted.txt`) | **SURVIVED** | genuine hole |
| B03 | Z family `check_echo` reset to False | met 105/105 | 103/105 `[LZ, Z]` (same) | 104/105 `[LZ]` (same) | stopped at the wave cap, no tally (`selftest-aborted.txt`) | **SURVIVED** | genuine hole |
| B04 | LZ family `check_era` reset to False | met 105/105 | **104/105 `[Z]`** (pristine: 103/105 `[LZ, Z]`) | 104/105 `[LZ]` | stopped at the wave cap, no tally (`selftest-aborted.txt`) | **KILLED** by N07 | — |
| B05 | `era_b()` inverts for the 9-digit Z spelling | **unmet 104/105 `[Z]`** (must be 105/105) | 103/105 `[LZ, Z]` | **103/105 `[LZ, Z]`** (pristine: 104/105 `[LZ]`) | stopped at the wave cap, no tally (`selftest-aborted.txt`) | **KILLED** by landed (and by the selftest's reference leg by construction) | — |

Kill directions:

- **B04** removes the LZ era assertion; the N07 bend lies the era for both spellings, so where the
  pristine battery loses both families (`103/105`), the mutant loses only Z (`104/105`). The N07
  leg changes in the direction the clause protects → killed.
- **B05** changes the battery's *expected* era for `12.9.999999999`, so the landed gate drops from
  `met 105/105` to `unmet 104/105 [REFUSAL-VERSIONS-9DIGIT-Z]` → killed by the landed leg; the
  `--reference` leg of the selftest would see the same 104/105 and fail the reference-gate row.
- **B01** is invisible to every bend: N07 only lies the era and the mutant still checks the era
  (`103/105` unchanged); N08 normalizes the echo, and with `check_echo` ignored the LZ family no
  longer fails, so **N08 reads `met 105/105`** where the claim requires `unmet 104/105`. The battery
  thus loses exactly the r97 A7 witness it was built to add.
- **B02** is invisible to N07: with `check_era` ignored the field lie no longer reads unmet, so
  **N07 reads `met 105/105`** where the claim requires `unmet 103/105`.
- **B03** is invisible to both committed bends: N08's normalization is the identity on the Z
  spellings (`12.9.999999999`, `0.9.999999999`), so only the LZ family can fail N08 and the reading
  is unchanged (`104/105 [LZ]`); N07 still fails Z through `check_era` (`103/105` unchanged).

## 6. Genuine survivors — diffs and the artefact that would catch each

### M07 — outside-scope survivor (checker)

```diff
--- pristine/check-registry-content-r98.py
+++ mutants/M07.py
@@ -223,9 +223,7 @@
         p = self._git("rev-parse", "--verify", self.revision + "^{commit}", check=False)
         if p.returncode != 0:
             raise TableError("revision %r does not resolve" % self.revision)
-        p = self._git("merge-base", "--is-ancestor", self.revision, self.branch, check=False)
-        if p.returncode != 0:
-            raise TableError("revision %r is not an ancestor of %s" % (self.revision, self.branch))
+        pass  # M07: ancestor check skipped
```

Why it survives: `--selftest` constructs only `Tree(root)` fixtures (`--root` mode), so the
`--revision`/ancestor path is unreachable there, and every doctored leg inspects an ancestor of
`master`. Proof the mutant is non-equivalent (`receipts/probe-nonancestor.txt`): a tree-identical
non-ancestor commit `dc4dd208…` (`commit-tree` in the scratch clone; `merge-base --is-ancestor` →
rc 1) reads `CANNOT-EVALUATE … rc=2` on the pristine checker and `status PASS bindings 7/7
findings 0 rc=0` on M07. This is the same class the r97 seat found; the artefact that would catch
it is the non-ancestor leg (`c2-nonancestor`, expecting rc 2), which is outside `--selftest` by
construction.

### B01 — genuine hole (battery)

```diff
@@ -2160,8 +2160,8 @@
 def meta_ok(c, got):
     """r96: an explicit-version case asserts the echo/source leg and/or the era leg it declares."""
-    if c.check_echo and not (got[8] == c.version and got[9] == "flag"):
-        return False
+    if False:  # B01: check_echo ignored (echo/source never asserted)
+        pass
     if c.check_era and got[10] != ("12.9.5+" if c.era_b() else "pre-12.9.5"):
         return False
     return True
```

Artefact that would catch it: a metadata member in the battery selftest's lie set — e.g.
`LIE_KINDS += ("echo",)` whose wrapper rewrites `out["limine_version"]` (a `"v"` prefix). The
already-emitted probe (`receipts/lie-*`, `lie.progress`) shows the direction: with an `echo` lie
wrapped around the unchanged gate the pristine battery reads `unmet` with the three `check_echo`
families failing (`EXPLICIT-VERSION-ECHO`, `LEADING-ZERO-NORMALIZE`,
`REFUSAL-VERSIONS-9DIGIT-Z`), while B01 reads them all as passing (`95/105 → 98/105`, the five
usage families fail identically in both because the probe wrapper is not transparent to refusal
rows — the delta, not the absolute count, is the evidence).

### B02 — genuine hole (battery)

```diff
@@ -2162,8 +2162,8 @@
     if c.check_echo and not (got[8] == c.version and got[9] == "flag"):
         return False
-    if c.check_era and got[10] != ("12.9.5+" if c.era_b() else "pre-12.9.5"):
-        return False
+    if False:  # B02: check_era ignored (visibility_era never asserted)
+        pass
     return True
```

Artefact: `LIE_KINDS += ("era",)` rewriting `out["visibility_era"]` to its opposite. Probe delta:
pristine `unmet` with `EXPLICIT-VERSION-ERA`, `LEADING-ZERO-NORMALIZE`,
`REFUSAL-VERSIONS-9DIGIT-Z` failing (`97/105`) versus B02 where all three pass (`100/105`).

### B03 — genuine hole (battery, targeted)

```diff
@@ -1819,7 +1819,7 @@
     asserts the echo … closing the r97 A7 limit (a field-only lie read 105/105 on the r97 battery)."""
-    c.check_echo = True
+    c.check_echo = False  # B03: Z family echo assertion reset
     c.check_era = True
     _era_first_line_panic(c, Z_DIGIT9[c.index % len(Z_DIGIT9)])
```

Artefact: a **Z-targeted** echo witness, because the generic `echo` lie cannot see this mutant —
the other two `check_echo` families (EXPLICIT-VERSION-ECHO, LEADING-ZERO-NORMALIZE) still fail the
generic lie, so the battery still reads `unmet`. A lie mode that prefixes `limine_version` only
when the third component is `999999999` (or an N09 bend normalizing exactly the Z spellings)
separates them: the probe shows the pristine battery failing `REFUSAL-VERSIONS-9DIGIT-Z`
(`P-echo-z 99/105`) while B03 passes the Z family (`B03-echo-z 100/105`, the same five usage
families failing in both). Adding that mode to `LIE_KINDS` is the one-line selftest fix; a bend
would have to be emitted by a later round's generator, not this one.

## 7. Can the battery's own selftest see a metadata assertion? (B01–B05)

**No.** Two receipts:

1. **Static (decisive):** `receipts/lie-kind-coverage.txt` — the battery's selftest lie set is
   `LIE_KINDS` with 12 members (`exit-code, rc-field, line, consequence, status, verdict, entry,
   panic-line, panic-value, on-panic, bad-resource, missing-panic`); the `LIE_WRAPPER` body
   between byte 104760 and `SELFTEST_GATES` contains **0** occurrences of `limine_version` and
   **0** of `visibility_era`. The `--reference` leg can only assert that the reference gate reads
   `met`; B01/B02/B03/B04 leave that gate's answers untouched, so the reference leg is green.
   Assertion *removal* is therefore unobservable to `--selftest` by construction: the only way it
   could see a metadata assertion is through a lie kind that mutates those two fields, and there is
   none.
2. **Empirical (bend legs):** the emitted mutants produce the expected blind readings — B01 N08
   `met 105/105`, B02 N07 `met 105/105`, B03 both legs identical to pristine — while B04 is caught
   only by N07 and B05 only by the landed/reference expectation. The five `--selftest --reference`
   runs were already executing when the wave's seat cap was applied and were stopped with no tally
   (`selftest-aborted.txt`, `selftest-inflight.txt`: the PIDs and elapsed times at the stop; all
   `B0x-selftest.txt` files are 0 bytes, so no selftest receipt is claimed). The classification
   does not depend on them: no lie kind mutates the two fields B01/B02/B03 stop asserting, the
   `--reference` row only asserts that the unchanged reference gate reads `met`, and B05 is already
   killed by the landed leg.

Consequence for C1 (reported, not fixed here): the r98 claim's sentence says both families set
`check_echo`/`check_era`. The `check_era` half has a witness only through N07, and the Z-family
`check_echo` half has **no** witness in the committed leg set — B03 removes it and every committed
receipt is byte-identical.

## 8. Restoration and cleanup

- Lane tools never edited: final `sha256sum -c` → 27/27 OK (`receipts/instruments-final.txt`);
  lane hashes `battery 8198bd84…`, `checker 5bb1441e…`, `gate 7d79ac29…` unchanged from the freeze.
- No file written outside the seat dir and the scratch root; the scratch root
  `/fast/scratch/hyaku/tsukuroi-r98/MutRegistry` was deleted before yield
  (`receipts/scratch-deletion.txt`).
- Tooling: nothing installed or upgraded (python3 3.14.8, git, bwrap from the host).
- Disclosure: the scratch clone received the fixture commits and the `update-ref` operations
  described in §1; no lane ref, commit, index or worktree was mutated, and nothing was pushed.

## 9. Receipts (all under `.ufo/waves/round-98/w1/MutRegistry/receipts/`)

`instruments-final.txt`, `doctored-revisions.txt`, `byte-offsets.txt`, `lie-kind-coverage.txt`,
`baseline-selftest.txt`, `baseline-{base,D1,D2,D2lie,lane-tip}.{txt,json}`,
`baseline-coverage-{base,D1,D2}.txt`, `baseline-{landed,N07,N08}.{txt,json}`,
`battery-legs-summary.txt`, `checker-summary.txt`, `checker-hunks.txt`, `battery-hunks.txt`,
`mutants-{checker,battery}-manifest.txt`, `M0x.diff`, `M0x-selftest.txt`,
`M0x-{base,D1,D2,D2lie}.{txt,json}`, `M08-on-r97-selftest.txt`, `probe-nonancestor*`,
`B0x.diff`, `B0x.progress`, `B0x-{landed,N07,N08}.{txt,json}`, `selftest-aborted.txt`,
`selftest-inflight.txt`, the zero-byte `B0x-selftest.txt` (the stopped runs),
`lie-*`, `lie.progress`, the emitters (`make_*_mutants.py`, `offsets.py`, `summarize_runs.py`) and
the runner scripts (`run_one.sh`, `run_checker_mutants.sh`, `run_lie.sh`, `make_diffs.sh`,
`make_bdiffs.sh`).

{"seat":"MutRegistry","verdict":"findings","notes":"Baselines reproduce C1 (landed 105/105; N07 103/105 [LZ,Z]; N08 104/105 [LZ]) and C2 (selftest 14/14; D1 FAIL 1 RC-BEND-SPAN; D2 PASS; D2lie FAIL 1; coverage 157/157 on base/D1/D2). C2 7/8 killed; M08 dies as claimed (r98 selftest FAIL 12/14 both gap cases; r97 PASS 12/12); M07 survives outside-scope (non-ancestor probe pristine rc2 vs mutant rc0). M09 killed by span-gap only (13/14, RC-CELL-MISSING) and by D2; M10 killed by both gap cases. C1 2/5 killed: B04 by N07 (104/105 [Z]); B05 by landed (104/105 [Z]). Genuine survivors B01 (N08 met 105/105), B02 (N07 met 105/105), B03 (both bends byte-identical to pristine). The battery selftest cannot see a metadata assertion: LIE_KINDS has 12 members, 0 occurrences of limine_version/visibility_era; artefact = echo/era lie kinds (probe deltas recorded), plus a Z-targeted echo lie for B03. Five mutant selftests were in flight at the wave cap; classification does not depend on them."}
