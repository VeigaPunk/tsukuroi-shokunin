# MutBattery — mutation test of the round-88 Limine pin battery

Seat `MutBattery` (w1, round 88). Lane `tsukuroi-shokunin`, branch `master`.
The lane tip moved while this seat ran (`1fac4195…` briefed → `45c60ac1…` → `4ef5d916…` → `8189c754…` seen at
exit); every artifact here is pinned by hash, and the battery/counter/roster bytes did not move (hashes below).
Candidate under test: `tools/limine-pin-battery-r88.py`, sha256
`ab6c1b33f84dd252979296d1b56ccea8c5e89af221e02e1ec08ef8e579fac374` — byte-identical to
`git show 5b98ca98:tools/limine-pin-battery-r88.py` and unchanged at exit.
Detector: frozen counter `tools/battery-discrimination-r88.py`, sha256
`7d2073dfd120c8ac5ebaf8c68e7c270f970b5c7a75850561d7ceb9db76c13305` (equals `freeze-manifest.sha256`),
over the frozen 48-gate roster `.ufo/waves/round-88/before/roster/roster-r88.json` (3 POSITIVE, 45 NEGATIVE).
No lane file was written. No host contact, no `sudo`, no `/boot`, no commit, no subagent, no model choice.

**Verdict: 8 of 26 single-point battery mutants killed by the frozen counter; 18 survive.**
Of the 18 survivors: 1 is behaviourally equivalent (M20); 1 is an assertion neither the counter nor the
battery's own `--selftest` can see (M18, `hash_mismatch_panic.value`); 2 are contract-field checks whose only
detector is the selftest (M21 JSON `rc`, M23 exit code); 14 are redundant decoys/keys inside a family the
roster still covers through another line — including every key of `ALL-PIN-KEYS`, whose family the roster
does not need at all (M24, confirmed by a whole-family probe). Five mutants are killed by the counter while
their own `--selftest` reads `PASS 14/14`: the selftest cannot detect a weakened expectation because it
drives only a correct reference gate. Two NEGATIVE gates are covered stochastically (CRLF p=0.6 per case;
`m10`'s non-empty root via a 1-in-6 sample), and on pristine bytes the battery read `38/38 met` against
`N-m22-cr-not-stripped` in 2 of 24 runs — so the frozen counter's three-run predicate carries a measured
several-percent risk of calling a correct battery unmet. One verified patch is proposed for the untested
field; it is not applied.

## 1. Detector baseline (pristine bytes, so a kill is a kill)

```
$ python3 tools/battery-discrimination-r88.py --battery $S/battery-pristine.py --runs 1 --jobs 4 \
      --scratch $S/work --json $S/out/baseline-counter.json
run 1 positives 3/3 negatives 45/45 failures -
verdict met
rc=0        (ELAPSED 90.39; host load ~34, --jobs 4 as the seat spec requires)

$ python3 $S/mut/battery-pristine.py --selftest      # lane-shaped fake root so the reference gate resolves
roster-literal     PASS families_passed=38
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
reference-gate     PASS families_passed=38
lie-exit-code      PASS families_passed=2
lie-rc-field       PASS families_passed=2
lie-line           PASS families_passed=2
lie-consequence    PASS families_passed=30
lie-status         PASS families_passed=36
lie-verdict        PASS families_passed=35
lie-entry          PASS families_passed=2
lie-panic-line     PASS families_passed=25
selftest PASS 14/14
rc=0        (ELAPSED 128.76)
```

The pristine battery is green on both detectors, so every kill below is semantic, not a baseline failure.
Selftest fixture note: a first attempt with the battery one directory above the fake lane printed
`reference-gate FAIL families_passed=missing /fast/…/.ufo/waves/round-88/before/roster/pos-landed-gate-3ba37eb0.py`
and `selftest FAIL 5/6`; the reference path resolves from `dirname(dirname(__file__))` exactly as the
docstring says. That is a scratch-layout artefact, not a battery defect; the run quoted is the corrected one.

## 2. Method

* 26 single-point mutants of the candidate battery. The generator is kept as `mutants/gen.py`; it asserts
  each anchor occurs exactly once, writes the mutant, compiles it, and saves a unified diff
  (`mutants/<name>.diff`). Each mutant is one literal replacement — a deleted decoy/key/pin line, a
  narrowed choice list, or a deleted comparison.
* Six follow-up whole-family probes (P27–P32, `probes/`) that empty one family, to separate "this line is
  redundant" from "this family is not needed".
* Per mutant: the frozen counter once, exactly as the frozen predicate uses it
  (`--battery <mutant> --runs 1 --jobs 4 --scratch <own dir>`), then the mutant's own `--selftest`.
  Per probe: the same two runs. Everything ran under `/fast/scratch/hyaku/tsukuroi-r88/MutBattery`.
* No counter row produced `error:*` (no timeout, no garbled JSON); every kill is a gate that read `met`
  where the roster expects `unmet`.
* Family-level attribution (which family kills which surviving gate) was taken from direct battery runs
  with `--json` case logs (`receipts/attrib-*`), one draw each; where a draw matters it is stated.

## 3. The 26 single-point mutants

"Surviving gates" = NEGATIVE roster gates that now read `met` (the gates the mutant lets through); `-`
means the counter still read 45/45. All mutants kept `positives 3/3`. Full receipts: `receipts/<name>.{counter,selftest}.txt`.

| mutant | single point | counter | surviving gates | mutant `--selftest` |
|---|---|---|---|---|
| `M01-key-spacing-drop-blank-decoy` | KEY-SPACING: delete `decoy(c, "  path : boot():/%s#%s")` | met 45/45 | - | PASS 14/14 |
| `M02-key-spacing-drop-tab-decoy` | KEY-SPACING: delete the `module_path\t:` decoy | met 45/45 | - | PASS 14/14 |
| `M03-no-paren-drop-dollar-decoy` | NO-PAREN: delete the `$boot:/` decoy | met 45/45 | - | PASS 14/14 |
| `M04-no-paren-drop-paren-decoy` | NO-PAREN: delete the `boot)/:/` decoy | met 45/45 | - | PASS 14/14 |
| `M05-first-uri-sep-plain-path` | FIRST-URI-SEP: path `%s):/%s` → `%s_%s` | **unmet 44/45** | `N-g05-last-uri-sep` | PASS 14/14 |
| `M06-paren-path-no-parens` | PAREN-PATH: `EFI/Linux/%s(%d).efi` → `EFI/Linux/%s.efi` | **unmet 43/45** | `N-m05-last-open-paren`, `N-m22-cr-not-stripped`¹ | PASS 14/14 |
| `M07-empty-root-one-resource` | EMPTY-ROOT-RESOURCE: 8 resources → `hdd()` | met 45/45 | - | PASS 14/14 |
| `M08-root-on-boot-no-gzip` | ROOT-ON-BOOT: `gz=c.rng.random() < 0.5` → `gz=False` | met 45/45 | - | PASS 14/14 |
| `M09-panic-key-case-lower-only` | PANIC-KEY-CASE: key choice → `"hash_mismatch_panic"` | **unmet 44/45** | `N-g07-panic-key-case` | PASS 14/14 |
| `M10-sb-flag-zero-absent` | SB-FLAG-ZERO: `c.sbflag = "0"` → `None` | met 45/45 | - | PASS 14/14 |
| `M11-panic-raw-decoy-drop-comment-key` | PANIC-RAW-DECOY: delete `comment: hash_mismatch_panic: no` | met 45/45 | - | PASS 14/14 |
| `M12-conf-unreadable-missing` | CONF-UNREADABLE: `c.conf_dir = True` → `c.conf_missing = True` | **unmet 44/45** | `N-g14-eacces-rc1` | PASS 14/14 |
| `M13-all-pin-keys-drop-global-dtb` | ALL-PIN-KEYS: delete `"global_dtb"` | met 45/45 | - | PASS 14/14 |
| `M14-panic-non-no-one-value` | PANIC-NON-NO: 9 values → `"off"` | met 45/45 | - | PASS 14/14 |
| `M15-entry-label-no-efi-fallback` | ENTRY-LABEL: `("EFI fallback", 1)` → random label | met 45/45 | - | PASS 14/14 |
| `M16-panic-metadata-one-value` | PANIC-METADATA: 4 value variants → `"no"` | met 45/45 | - | PASS 14/14 |
| `M17-r8-ignore-entries` | `r8_ok`: `if ln not in want_entries or label != …:` → `if False:` | **unmet 44/45** | `N-m24-entry-not-tracked` | **FAIL 13/14** (`lie-entry`) |
| `M18-r8-ignore-panic-value` | `r8_ok`: delete the `hash_mismatch_panic.value` comparison | met 45/45 | - | PASS 14/14 |
| `M19-r8-ignore-panic-line` | `r8_ok`: `pm.get("line") == want_panic[0]` → `True` | **unmet 44/45** | `N-m25-panic-line-metadata-zero` | **FAIL 13/14** (`lie-panic-line`) |
| `M20-met-from-len-families` | `met = len(passed) == len(FAMILY_ROSTER)` → `len(FAMILIES)` | met 45/45 | - | PASS 14/14 |
| `M21-drop-rc-field-check` | `run_battery`: drop `got[3] == want[0]` (JSON `rc`) | met 45/45 | - | **FAIL 13/14** (`lie-rc-field`) |
| `M22-cases-per-family-1` | `CASES_PER_FAMILY = 4` → `1` | **unmet 43/45** | `N-g15-no-cr-strip`, `N-m22-cr-not-stripped`¹ | PASS 14/14 |
| `M23-drop-exit-code-check` | `run_battery`: drop `got[0] == want[0]` (process exit) | met 45/45 | - | **FAIL 13/14** (`lie-exit-code`) |
| `M24-all-pin-keys-empty` | ALL-PIN-KEYS: `keys = [...]` → `keys = []` | met 45/45 | - | PASS 14/14 |
| `M25-format-before-resolve-boot` | FORMAT-BEFORE-RESOLVE: unresolvable resource list → `"boot()"` | **unmet 44/45** | `N-g03-format-after-resolve` | PASS 14/14 |
| `M26-optional-hash-format-wallpaper-only` | OPTIONAL-HASH-FORMAT: `("wallpaper","term_font")` → `("wallpaper",)` | met 45/45 | - | PASS 14/14 |

¹ `N-m22-cr-not-stripped` and `N-g15-no-cr-strip` fail only when a conf line carries CR; `WHITESPACE-CRLF`
sets `eol = "\r\n"` with probability 0.6 per case, so a four-case run with no CR lets both gates through
(analytic 0.4⁴ = 2.56%; measured 2/24 runs, section 6). M06's co-failure of `N-m22` is therefore a draw
artefact, not an effect of the PAREN-PATH edit: the same mutant bytes rerun (`probes/M06b-*`) read
`negatives 44/45 failures N-m05-last-open-paren` with the CR gates green. M22's kill is likewise nothing but
that pair (43/45): a one-case battery loses the CR clause 40% of the time, so the kill is luck, not
discrimination.

## 4. What the survivors mean

### 4.1 Lines/families the frozen roster does not need

Attribution is from direct battery runs with case logs (`receipts/attrib-*`).

* **`ALL-PIN-KEYS` is not needed at all.** `M24` (no pin key in the family) still reads 45/45, and the
  surviving gate probe is unambiguous: `M24` vs `g16-drop-global-dtb` → `families_passed 37/38 … failed
  KEY-CASE`. Every key the family exercises is covered elsewhere: `KEY-CASE` pins `kernel_path`/
  `image_path`/`dtb_path`/`global_dtb` (one of four keys per case), `GZ-RAW` pins `module_path`,
  `OPTIONAL-SKIP` pins `wallpaper`/`term_font`, and `HASH-UPPER` pins `path`. `M13` (drop only
  `global_dtb`) survives for the same reason — but that cover is a draw: `M13` vs `g16` reads
  `6 × 37/38 (failed KEY-CASE)` + `4 × 38/38 met` and `M24` vs `g16` reads `7 × 37/38` + `3 × 38/38 met`
  over 10 direct runs each, against the analytic 1−(3/4)⁴ = 68% kill per run.
  So on this roster `g16` is *deterministically* caught only by the line M24 deletes, and the counter's
  `45/45` was that draw landing on `global_dtb`.
* **Decoys inside `KEY-SPACING` and `NO-PAREN` are mutually redundant, not dead.** `M01`–`M04` each delete
  one decoy and still read 45/45; probes P27/P28 empty the families entirely and are killed by
  `N-g01-loose-key` / `N-g02-no-paren`, so the families are load-bearing but each needs only one decoy.
* **`SB-FLAG-ZERO` is duplicated by the 30% random `--secure-boot-enforced 0`.** `M10` (never pass `"0"` in
  that family) survives; `M10` vs `g08-sb-presence` reads `families_passed 33/38 … failed
  HOST-SHAPE,MULTI-FAULT,PANIC-FIRST,PANIC-KEY-CASE,PANIC-NO-ONLY`, i.e. `build()`'s independent 30% coin
  hands `"0"` to mismatch cases in those families and kills `g08` anyway. The deterministic family is the
  safer design, but the roster does not require it.
* **`ROOT-ON-BOOT`'s gzip half is not needed**: `M08` (never set `$` on the non-empty root) survives 45/45;
  no roster gate reads that combination. The `boot(N)` half *is* needed — see P30 in section 5.
* **`PANIC-NON-NO`'s value list is redundant**: `M14` (only `"off"`) survives; `M14` vs
  `g12-any-non-yes-control` is still killed by `PANIC-NO-ONLY` (which samples non-`no` values) and
  `PANIC-NON-NO` itself via the first non-`no` draw.
* **`PANIC-METADATA`'s case variants are redundant**: `M16` survives; `M16` vs `m25-…` still fails 13
  families including `PANIC-METADATA`. Probe P32 (no `hash_mismatch_panic` key at all) also reads 45/45, so
  the family is not needed by this roster; `m25` is caught by any of the other 13 families that carry a
  panic key line.
* **`ENTRY-LABEL`'s fixed `EFI fallback` label is redundant** (`M15`): `m24-entry-not-tracked` fails 36 of
  38 families even under M15 (`families_passed 2/38`) — any family with entry lines catches it.
* **`OPTIONAL-HASH-FORMAT`'s `term_font` half is redundant** (`M26`): `M26` vs
  `g04-hashformat-optional-panic` → `failed OPTIONAL-HASH-FORMAT`, i.e. the `wallpaper` line does the work
  (and `OPTIONAL-SKIP` covers the mismatch half).
* **`EMPTY-ROOT-RESOURCE` needs one resource, not eight** (`M07` survives; `M07` vs
  `g06-any-empty-root` → `failed EMPTY-ROOT-RESOURCE`). P29 shows the family itself is needed.
* **`PANIC-RAW-DECOY`'s `#`/comment decoys are redundant** (`M11` survives; `M11` vs
  `g10-raw-panic-scan` → `failed PANIC-KEY-CASE,PANIC-RAW-DECOY`, and a direct 8-run probe of P31 gives
  `36–37/38, failed PANIC-KEY-CASE[,PANIC-RAW-DECOY]` in 8 of 8 — the mixed-case key defeats the raw scan
  every run).

### 4.2 Selftest gaps (counter kills, own selftest passes)

Five semantic kills with `selftest PASS 14/14`: `M05`, `M06`, `M09`, `M12`, `M25` (`M22`'s kill is the CR
draw, also with a passing selftest). Root cause is structural: the only positive control is a *correct*
gate, so a weakened expectation still matches it; only a one-field lie wrapper can catch a deleted
assertion, and `LIE_KINDS` covers exit-code/rc-field/line/consequence/status/verdict/entry/panic-line but
not `hash_mismatch_panic.value`. This is the r87 routed R87-R1 direction (a selftest that passes on a
never-`met` mutant): the selftest cannot see a weakened family, and the battery's assurance argument
therefore rests on the frozen counter, exactly as the C1 declaration says. Reported as a limitation, not as
a C1 defect.

### 4.3 An assertion with no detector at all

`M18-r8-ignore-panic-value` deletes the `hash_mismatch_panic.value` comparison and **both** detectors stay
green (counter 45/45, selftest 14/14). `m25` only zeroes the reported line; no lie wrapper flips the value.
The battery asserts a field that nothing tests. Patch in section 7.

### 4.4 Counter-blind contract checks (selftest catches)

`M21` (JSON `rc`) and `M23` (exit code) survive the roster and fail the selftest on
`lie-rc-field`/`lie-exit-code`. That is the intended division of labour — the frozen roster has no gate
whose exit code and `rc` field disagree — and is listed so these survivors are not read as holes.

### 4.5 Equivalent mutant

`M20` (`len(passed) == len(FAMILIES)`) is behaviourally identical because `main()` returns 2 whenever
`tuple(FAMILIES) != FAMILY_ROSTER`; no fixture can distinguish it. Not a gap.

## 5. Whole-family probes (P27–P32)

Each probe removes the family's decisive material; the question is whether the family itself is load-bearing
for the frozen roster. Receipts in `probes/`.

| probe | change | counter | surviving gates | selftest |
|---|---|---|---|---|
| `P27-key-spacing-no-decoys` | KEY-SPACING: delete all four decoys | **unmet 43/45** | `N-g01-loose-key` (+`N-m22` CR flake) | PASS 14/14 |
| `P28-no-paren-no-decoys` | NO-PAREN: delete all three decoys | **unmet 44/45** | `N-g02-no-paren` | PASS 14/14 |
| `P29-empty-root-no-pin` | EMPTY-ROOT-RESOURCE: no unresolved pin | **unmet 44/45** | `N-g06-any-empty-root` | PASS 14/14 |
| `P30-root-on-boot-no-pin` | ROOT-ON-BOOT: no non-empty-root pin | met 45/45 (that draw) | - | PASS 14/14 |
| `P31-panic-raw-no-decoys` | PANIC-RAW-DECOY: drop the `#`/other-key decoys | **unmet 44/45** | `N-g15-no-cr-strip` (CR flake only; `g10` still killed) | PASS 14/14 |
| `P32-panic-metadata-no-panic` | PANIC-METADATA: no panic key line | met 45/45 | - | PASS 14/14 |

Readings:

* **P27/P28/P29**: emptying a family lets its forger through, so the family is needed; only its individual
  redundant lines are interchangeable.
* **P30**: the family is the *deterministic* killer of `m10-root-ignored`. Without it the only other killer
  is `UNRESOLVED`'s sampled `boot(2)` (1 of 6 resources × 4 cases). Direct probe, `P30` battery vs
  `m10-root-ignored`, 10 runs: `5 × 37/38 (failed UNRESOLVED)` and `5 × 38/38 met` — a ~50/50 coin
  (analytic kill probability 1−(5/6)⁴ = 51.8%). The counter's `met 45/45` was that draw landing on
  `boot(2)`, not evidence that the clause is covered elsewhere.
* **P31**: the counter's verdict came from the CR flake on `N-g15`, but `g10` was killed in that same run;
  the eight direct runs above show the family's `#`/comment decoys are redundant while the family's role is
  taken by `PANIC-KEY-CASE`.
* **P32**: `m25` is caught by 13 other panic-bearing families, so the roster does not need this family.

## 6. Stochastic coverage — measured on pristine bytes

Two roster clauses are covered only by a coin, not by a deterministic fixture:

1. **CR stripping (`R1`).** `WHITESPACE-CRLF` sets `eol = "\r\n"` with p=0.6 per case; four cases give
   p = 0.4⁴ = 2.56% that a run carries no CR at all, letting `N-g15-no-cr-strip` and
   `N-m22-cr-not-stripped` read `met`. Measured on pristine bytes, 24 runs of the battery against
   `m22-cr-not-stripped`: **22 × `37/38 … failed WHITESPACE-CRLF`, 2 × `38/38 met`** (8.3%; the sample
   cannot separate this from the analytic 2.56%). Verbatim (first batch):
   ```
   $ python3 $S/mut/battery-pristine.py --gate …/m22-cr-not-stripped.py --runs 8 --work $S/work/flake
   families_passed 37/38 verdict unmet failed WHITESPACE-CRLF      (×7)
   families_passed 38/38 verdict met failed -                     (×1)
   rc=1
   ```
   Consequence for the frozen predicate: the counter reads `unmet` if **any** of its three runs has one
   such gate met, so a correct battery has ≈ 1 − 0.9744³ = **7.4%** chance of being called `unmet` by the
   frozen counting command. The claim's three runs were observed green, but the instrument is not stable at
   the percent level. A deterministic fix is one line in `fam_whitespace` (force CRLF on at least one of
   the four cases when `CASES_PER_FAMILY` is used); it is left to the L1 because it changes fixture
   distribution, not behaviour under test.
2. **Non-empty `boot` root (`R4`).** Deterministic only through `ROOT-ON-BOOT`; the other killer samples
   `boot(2)` once in six per case (section 5). Note the docstring calls this an r87 "sampled draw … covered
   every run by a deterministic family" — P30 shows the family is exactly that deterministic cover.

## 7. Proposed patch (not applied; L1 decides)

`patch/0001-selftest-add-lie-panic-value.patch` — one new lie kind in `LIE_WRAPPER` and `LIE_KINDS`:

```diff
+elif KIND == "panic-value" and isinstance(out.get("hash_mismatch_panic"), dict):
+    v = out["hash_mismatch_panic"].get("value")
+    out["hash_mismatch_panic"]["value"] = "yes" if str(v).lower() == "no" else "no"
...
-LIE_KINDS = ("exit-code", "rc-field", "line", "consequence", "status", "verdict", "entry", "panic-line")
+LIE_KINDS = ("exit-code", "rc-field", "line", "consequence", "status", "verdict", "entry", "panic-line",
+              "panic-value")
```

Verified in scratch (`patch/`, `$S/patch/`):

* patched battery alone → `selftest PASS 15/15` rc 0, with `lie-panic-value PASS families_passed=25`;
* patched battery **plus** the M18 weakening → `lie-panic-value FAIL families_passed=38` and
  `selftest FAIL 14/15` rc 1, proving the new lie detects the deleted comparison.

The proposed file is `patch/proposed-battery.py` for convenience; the diff is the authoritative form. No
lane file was touched.

## 8. Restoration, cleanliness, tooling

* The candidate was copied to scratch and never edited in place. Scratch copy sha256
  `ab6c1b33f84dd252979296d1b56ccea8c5e89af221e02e1ec08ef8e579fac374` before and after the probe; the lane
  file hashes the same at exit:
  ```
  $ sha256sum tools/limine-pin-battery-r88.py tools/battery-discrimination-r88.py
  ab6c1b33f84dd252979296d1b56ccea8c5e89af221e02e1ec08ef8e579fac374  tools/limine-pin-battery-r88.py
  7d2073dfd120c8ac5ebaf8c68e7c270f970b5c7a75850561d7ceb9db76c13305  tools/battery-discrimination-r88.py
  $ git status --porcelain tools/ .ufo/waves/round-88/before/    → empty
  ```
* All fixtures lived under `/fast/scratch/hyaku/tsukuroi-r88/MutBattery`; scratch was removed after the
  receipts were copied here (`mutants/`, `probes/`, `receipts/`, `patch/`, baselines in this directory).
* Tooling: nothing installed or upgraded (no tool was needed). Host read-only throughout; `bwrap` and
  `python3` already present.
* Counts for the L1: 26 single-point mutants (8 killed, 18 survived: 14 redundant-line, 1 equivalent,
  2 selftest-only, 1 undetected field), 6 whole-family probes (4 killed, 2 met), 3 stochastic-coverage or
  draw findings (CRLF 2/24 met; non-empty root 5/10 met without ROOT-ON-BOOT; `g16` 4/10 met without
  `global_dtb` in ALL-PIN-KEYS), 1 verified patch proposal. One mutant (`M22`) was killed by a draw, not by
  discrimination, and is called out as such rather than counted as evidence of sampling strength.
