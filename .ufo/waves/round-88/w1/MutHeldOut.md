# MutHeldOut — held-out mutation test of the round-88 Limine pin battery

Seat `MutHeldOut`, Tsukuroi round 88, wave w1. Lane `tsukuroi-shokunin` (branch `master`, jj-colocated).
Lane revision measured: `1fac4195243e55e7d9d8a2eddd653443d8559bff`
(`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`).
No host contact, no `sudo`, no `/boot` access, no lane edit, no git/jj mutation, no commit.
Scratch was `/fast/scratch/hyaku/tsukuroi-r88/MutHeldOut` (disposable; receipts copied here first, then removed).

## 0. Inputs under test (digests verified with Python `hashlib`)

| object | path | sha256 |
|---|---|---|
| gate under test (roster POSITIVE, r87 landed gate at `3ba37eb0`) | `.ufo/waves/round-88/before/roster/pos-landed-gate-3ba37eb0.py` (12,821 bytes) | `e3b0fab4f2d276fe579b64ce5c8741a065bd9afe281257d38aa2209062407352` |
| r88 battery (candidate) | `tools/limine-pin-battery-r88.py` (38 families × 4 cases) | `ab6c1b33f84dd252979296d1b56ccea8c5e89af221e02e1ec08ef8e579fac374` |
| r87 battery (do-nothing control, 22 families × 4 cases) | `tools/limine-pin-battery-r87.py` | `f2551c8e8386d599e3c2aca8888d5fbb0351a5a399dc43dc448556e99361989d` |
| frozen counter | `tools/battery-discrimination-r88.py` | `7d2073dfd120c8ac5ebaf8c68e7c270f970b5c7a75850561d7ceb9db76c13305` |

The gate digest equals the `roster-r88.json` entry `P-landed-gate`; all 48 roster gate digests in
`roster-r88.json` were re-verified (0 mismatches; 3 POSITIVE, 45 NEGATIVE). The working-tree r88 battery
differs from candidate `5b98ca98c9a19641e77832bc57579d95fa5571a3` by zero bytes
(`git diff --stat 5b98ca98 -- tools/limine-pin-battery-r88.py` printed nothing). Python 3.14.8.

The pristine gate copy in scratch and the copy in this seat dir are byte-identical before and after the
probe: sha256 `e3b0fab4…07352` both times; the gate was never edited, only read and copied
(each mutant is a separate file). Scratch is declared disposable by the tasking.

## 1. Method

- 24 single-point mutants (`mutants/`, generator `gen.py`): each is a copy with exactly one literal
  replacement; the generator asserts the anchor occurs exactly once before writing, and writes a unified
  diff (`mutants/h*.diff`). All 24 are byte-new relative to every file in the frozen roster (checked by
  sha256; the roster already contains r87 MutGate `m01-m30` and the forger set `g00-g16`).
- Hand probe (`probe.py`, `probe-results.json`): 25 hand-built fixtures covering `= ` separator, digit
  decoys, tab-after-colon, tab indent, empty hash, 129-char hash, last-character hash flip, `$` gzip
  marker, `boot(2)` root, empty path, uppercase optional key, optional bad-format, uppercase panic key,
  `nope` panic value, missing file, 128-char non-hex hash, CRLF, pin under a `/+` entry, uppercase
  `BOOT()`, upper-case pin key, directory `--conf`, stored path containing `):/`, and flag `0`.
  Comparison uses the battery-visible tuple `(process rc, verdict, sorted pins (line,status,consequence),
  rc field, entry map, hash_mismatch_panic)`. **23 mutants differ from pristine on at least one fixture;
  one (`h02`) equals pristine on all 25 and is reported EQUIVALENT.**
- Detection: the same bounded detector on pristine and each mutant — the full frozen family rosters, 3 runs
  each, `--runs 3`, separate `--work` per invocation:
  `python3 <lane>/tools/limine-pin-battery-r88.py --gate <mutant> --runs 3 --work …` and the same with
  `limine-pin-battery-r87.py`. 17,280 battery cases total. Nothing else was run (no counter, no host tool).
- `killed` below means the 3-run invocation read `unmet` in at least one run (the battery's own aggregate);
  `SURVIVED` means `met` in all three runs. Per-run `families_passed` is shown as three comma-separated
  values. 4 mutant streams ran concurrently; the whole sweep took 227 s.

Baseline on pristine bytes (a mutant reading is only meaningful against this):

```
$ python3 <lane>/tools/limine-pin-battery-r88.py --gate $S/pristine.py --runs 3 --work $S/work/base88 --json $S/base88.json
families_passed 38/38 verdict met failed -
families_passed 38/38 verdict met failed -
families_passed 38/38 verdict met failed -
rc=0
$ python3 <lane>/tools/limine-pin-battery-r87.py --gate $S/pristine.py --runs 3 --work $S/work/base87 --json $S/base87.json
families_passed 22/22 verdict met failed -
families_passed 22/22 verdict met failed -
families_passed 22/22 verdict met failed -
rc=0
```

## 2. Results

Line numbers are in `.ufo/waves/round-88/before/roster/pos-landed-gate-3ba37eb0.py` (the gate bytes under test).

| mutant | gate:line | rule (mutated clause) | probe fixture that differs | r87 families_passed (3 runs) | r88 families_passed (3 runs) | r87 | r88 | equivalent? | r88 families that failed (union) |
|---|---|---|---|---|---|---|---|---|---|
| `h01-key-sep-equals` | 53 | R1 key directly followed by `:` | key-eq-sep | 22, 22, 22 | 38, 38, 38 | SURVIVED | SURVIVED | yes | - |
| `h02-keychars-digits` | 40 | R1 key charset letters/underscore | **none — EQUIVALENT** | 22, 22, 22 | 38, 38, 38 | SURVIVED | SURVIVED | EQ | - |
| `h03-value-lstrip-spaces-only` | 55 | R1 skip blanks (space+tab) after `:` | value-tab | 21, 21, 21 | 37, 37, 37 | killed | killed | yes | WHITESPACE-CRLF |
| `h04-strip-spaces-only` | 47 | R1 strip leading/trailing space+tab per line | indent-tab | 21, 21, 21 | 37, 37, 37 | killed | killed | yes | WHITESPACE-CRLF |
| `h05-hash-empty-ignored` | 119 | R2/R3 an empty hash is still a pin | empty-hash | 21, 21, 21 | 37, 38, 37 | killed | killed | yes | OPTIONAL-HASH-FORMAT |
| `h06-hash-len-at-least` | 127 | R3 hash exactly 128 characters | hash-129 | 21, 22, 22 | 38, 36, 36 | killed | killed | yes | FORMAT-BEFORE-RESOLVE, HASH-LENGTH, OPTIONAL-HASH-FORMAT |
| `h07-hash-prefix-64` | 156 | R5 full-digest comparison | hash-prefix-late-flip | 11, 11, 12 | 18, 17, 17 | killed | killed | yes | 21 families (ALL-PIN-KEYS, ENTRY-LABEL, FIRST-URI-SEP, …) |
| `h08-dollar-kept` | 132 | R4 leading `$` gzip marker dropped | gz-marker | 21, 21, 21 | 37, 37, 37 | killed | killed | yes | GZ-RAW |
| `h09-root-ignored-on-boot` | 133 | R4 `boot` with NON-empty root is LP-UNRESOLVED | root-on-boot2 | 21, 21, 22 | 35, 35, 36 | killed | killed | yes | EMPTY-ROOT-RESOURCE, ROOT-ON-BOOT, UNRESOLVED |
| `h10-empty-path-pin-ignored` | 119 | R2 a pin with an empty path is still a pin | empty-path | 22, 22, 22 | 38, 38, 38 | SURVIVED | SURVIVED | yes | - |
| `h11-optional-case-sensitive` | 125 | R6 optional keys matched per R1 (case-insensitive) | optional-upper-wallpaper | 22, 22, 22 | 38, 38, 38 | SURVIVED | SURVIVED | yes | - |
| `h12-format-optional-panic` | 128 | R6 LP-HASH-FORMAT on wallpaper/term_font → skip | optional-format-wallpaper | 22, 22, 22 | 37, 37, 37 | SURVIVED | killed | yes | OPTIONAL-HASH-FORMAT |
| `h13-panic-key-case` | 115 | R1/R6 `hash_mismatch_panic` key case-insensitive | panic-key-upper | 22, 22, 22 | 37, 37, 37 | SURVIVED | killed | yes | PANIC-KEY-CASE |
| `h14-sb-zero-inverted` | 269 | R6/R7 `--secure-boot-enforced 0` not enforced | sb-flag-zero | 21, 21, 21 | 33, 32, 34 | killed | killed | yes | 7 families (SB-FLAG-ZERO, SECUREBOOT, PANIC-*, HOST-SHAPE) |
| `h15-panic-startswith-no` | 121 | R6 panic value equal to `no` (not a prefix) | panic-value-nope | 22, 22, 22 | 37, 36, 37 | SURVIVED | killed | yes | PANIC-NO-ONLY, PANIC-NON-NO |
| `h16-missing-consequence-none` | 146 | R6 LP-MISSING → `not-modelled` | missing-file | 20, 20, 20 | 36, 36, 36 | killed | killed | yes | MISSING, MULTI-FAULT |
| `h17-hash-nonhex-skipped` | 127 | R3 hash must be hex | hash-nonhex-128 | 21, 21, 21 | 35, 35, 35 | killed | killed | yes | FORMAT-BEFORE-RESOLVE, HASH-NONHEX, OPTIONAL-HASH-FORMAT |
| `h18-cr-split-lines` | 106 | R7/R8 1-based PHYSICAL line numbering | crlf | 21, 21, 21 | 37, 37, 37 | killed | killed | yes | WHITESPACE-CRLF |
| `h19-entry-plus-kept` | 109 | R8 entry label strips one leading `+` | entry-plus | 22, 22, 22 | 38, 38, 38 | SURVIVED | SURVIVED | yes | - |
| `h20-resource-case-insensitive` | 133 | R4 resource names are case-sensitive | resource-upper | 22, 22, 22 | 38, 38, 38 | SURVIVED | SURVIVED | yes | - |
| `h21-conf-except-filenotfound` | 101 | R7 any unreadable `--conf` → CANNOT-EVALUATE | conf-dir | 22, 22, 22 | 37, 37, 37 | SURVIVED | killed | yes | CONF-UNREADABLE |
| `h22-first-uri-sep-rfind` | 63 | R2 path starts after the FIRST `):/` | first-uri-sep | 22, 22, 22 | 37, 37, 37 | SURVIVED | killed | yes | FIRST-URI-SEP |
| `h23-key-lookup-as-written` | 117 | R1/R2 pin keys matched case-insensitively | key-upper | 21, 21, 21 | 37, 37, 37 | killed | killed | yes | KEY-CASE |
| `h24-term-font-dropped` | 38 | R6 `term_font` is an optional key | optional-mismatch-term-font | 21, 21, 21 | 35, 35, 35 | killed | killed | yes | ALL-PIN-KEYS, OPTIONAL-HASH-FORMAT, OPTIONAL-SKIP |

Counts: 24 mutants (23 behaviourally distinct, 1 equivalent). r88 killed **18/23** distinct mutants;
r87 killed **13/23**. Five distinct mutants survive **both** batteries; five are killed by r88 only
(`h12`, `h13`, `h15`, `h21`, `h22`). The only battery case errors in 17,280 cases are the 12 intended
crash cases of `h21` on `CONF-UNREADABLE` (4 cases × 3 runs, `bad-output: JSONDecodeError … IsADirectoryError`),
which is the contract's kill, not a flake; no timeouts anywhere. `h02` is equivalent: allowing digits in
`KEYCHARS` can only produce keys that are not in `PIN_KEYS` and is not in `hash_mismatch_panic` either, so
no input can observe it (25/25 probe fixtures identical, including digit decoys `path2:` / `2path:` that
the r88 `KEY-SPACING` family itself writes).

## 3. Survivors — coverage findings (both batteries read `met`)

All five are behavioural on a hand-built input and violate a written R1/R2/R4/R6/R8 clause; neither the
r87 nor the r88 family roster writes the triggering input. The roster is frozen this round, so these are
findings for the L1, not edits.

1. **`h01-key-sep-equals` (R1, gate:53).** Mutant accepts `=` as the key separator.
   Probe `path= boot():/a.efi#<correct>`:
   `pristine (0,'HEALTHY',[])` vs `mutant (0,'HEALTHY',[(2,'OK','none')])`.
   Only `KEY-SPACING` (`tools/limine-pin-battery-r88.py:521`) writes near-miss separators, and it writes
   `path :`, `module_path\t:`, `kernel-path:`, `path2:` — never `key=`. No case in 38×4×3 runs caught it.
2. **`h10-empty-path-pin-ignored` (R2, gate:119).** Mutant drops a pin whose stored path is empty.
   Probe `path: boot():/#<128 hex>`: `pristine (1,'DEGRADED',[(2,'LP-MISSING','not-modelled')])` vs
   `mutant (0,'HEALTHY',[])`. No family emits an empty path; `MISSING` (`…r88.py:275`) always pins a
   named file. A gate that silently drops such a line reads HEALTHY where the rule set says DEGRADED.
3. **`h11-optional-case-sensitive` (R6, gate:125).** Mutant matches `OPTIONAL_KEYS` against the key
   as written. Probe `WALLPAPER: boot():/a.efi#<bad>`:
   `pristine (1,'DEGRADED',[(1,'LP-MISMATCH','skip')])` vs `mutant (…,'LP-MISMATCH','panic')`.
   `OPTIONAL-SKIP` (`…r88.py:418`) and `OPTIONAL-HASH-FORMAT` (`:556`) only write lower-case keys;
   `KEY-CASE` only exercises path-valued keys. R6 optionality is keyed on the R1 (case-insensitive) key.
4. **`h19-entry-plus-kept` (R8, gate:109).** Mutant does not strip a leading `+` from an entry label.
   Probe `/+Global` directly followed by a pin: `pristine entry → "Global"`, `mutant entry → "+Global"`.
   `ENTRY-LABEL` (`…r88.py:675`) writes one `/+label` line but always follows it with another entry
   before any pin, so the global entry's label is never asserted. R8 says the `+` is stripped.
5. **`h20-resource-case-insensitive` (R4, gate:133).** Mutant lower-cases the resource name.
   Probe `path: BOOT():/a.efi#<correct>`: `pristine (2,'CANNOT-EVALUATE',LP-UNRESOLVED)` vs
   `mutant (0,'HEALTHY',[(2,'OK','none')])`. Neither `EMPTY-ROOT-RESOURCE` (`:586`) nor `UNRESOLVED`
   (`:370`) draws an upper-case resource name (`Boot2()` does not expose lower-casing because it stays
   unrecognised either way).

Informational coverage additions (not applied; they would change the frozen roster):
`KEY-SPACING` add an `=` decoy; `MISSING` (or a new `EMPTY-PATH`) draw `boot():/#<hash>`; the optional
families draw key case from `{wallpaper, WALLPAPER, Wallpaper}`; `ENTRY-LABEL` pin directly under the
`/+label` line; `EMPTY-ROOT-RESOURCE`/`UNRESOLVED` add `BOOT()`/`Boot()`.

## 4. What r88 certifies that r87 does not (held-out evidence)

Five distinct mutants survive the r87 battery in all three runs and are killed by the r88 battery in all
three runs, each by exactly one new family:

```
h12-format-optional-panic  r87 22/22,22/22,22/22 met  | r88 37/38,37/38,37/38 unmet OPTIONAL-HASH-FORMAT
h13-panic-key-case         r87 22/22,22/22,22/22 met  | r88 37/38,37/38,37/38 unmet PANIC-KEY-CASE
h21-conf-except-filenotfound r87 22/22,22/22,22/22 met | r88 37/38,37/38,37/38 unmet CONF-UNREADABLE
h22-first-uri-sep-rfind    r87 22/22,22/22,22/22 met  | r88 37/38,37/38,37/38 unmet FIRST-URI-SEP
h15-panic-startswith-no    r87 22/22,22/22,22/22 met  | r88 37/38,36/38,37/38 unmet PANIC-NO-ONLY,PANIC-NON-NO
```

`h15` is the r87 sampling weakness the r88 docstring names: r87's `PANIC-NO-ONLY` draws its non-`no`
half from six values (`nope` among them) with probability ½ per case, so 12 cases in three runs missed it;
r88's `PANIC-NON-NO` (`…r88.py:664`) writes `nope`/`none`/`no-`/`noo` every run and killed it 3/3.
`h09` is the same story for R4: r87's `UNRESOLVED` family samples `boot(N)` (1 of 6 resources) and failed
only 2 of 3 runs, while r88's `ROOT-ON-BOOT` (`:597`) is deterministic (3/3, plus
`EMPTY-ROOT-RESOURCE`). `h14` is killed by both, but r87 only through `SECUREBOOT`: the mutant inverts the
explicit `1` as well, so the r87 family catches the mutant for the wrong reason — r88 additionally pins the
`0` case through `SB-FLAG-ZERO` (`:617`) and the panic families.

Stochastic catches worth recording: `h05` was killed by r88 in 2 of 3 runs through
`OPTIONAL-HASH-FORMAT`, while the empty-hash draw of `HASH-LENGTH` (`n=0`) happened to be absent in those
three runs. An extra six-run probe (receipt `h05-hash-empty-ignored.r88-extra6.out`) shows
`HASH-LENGTH` failing in 5 of 6 runs, so the clause is exercised, just not guaranteed in any given
three-run sample:

```
families_passed 36/38 verdict unmet failed FORMAT-BEFORE-RESOLVE,OPTIONAL-HASH-FORMAT
families_passed 36/38 verdict unmet failed FORMAT-BEFORE-RESOLVE,HASH-LENGTH
families_passed 35/38 verdict unmet failed FORMAT-BEFORE-RESOLVE,HASH-LENGTH,OPTIONAL-HASH-FORMAT
families_passed 36/38 verdict unmet failed HASH-LENGTH,OPTIONAL-HASH-FORMAT
families_passed 35/38 verdict unmet failed FORMAT-BEFORE-RESOLVE,HASH-LENGTH,OPTIONAL-HASH-FORMAT
families_passed 36/38 verdict unmet failed FORMAT-BEFORE-RESOLVE,HASH-LENGTH
```

`h06` (accepts hashes longer than 128) failed r87 only in the first of three runs (`HASH-LENGTH` draws
129 with probability ¼ per case), while r88 failed it in two of three. Both are killed under the battery's any-run rule,
but a single 3-run reading can miss them.

## 5. Bounds and non-claims

- I did not re-scope C1. The frozen counter measures the frozen 48-gate roster; my held-out mutants are
  outside that roster and change no claimed count. This seat answers only "does the candidate battery
  distinguish single-point deviations the roster does not contain?" — it kills 18/23 distinct ones and
  misses five specific clauses (above), of which it inherits three from r87 unchanged (`h01`, `h11`,
  `h19`) and two from a shared unmodelled input (`h10`, `h20`).
- Not tested (outside the battery contract): a gate that behaves differently on its own bytes/file name,
  timeouts (none occurred), concurrency, host path resolution, and any r88 C2 claim (no host fact was
  needed or read beyond the committed receipts).
- Lane files untouched. All writes are in `.ufo/waves/round-88/w1/MutHeldOut/` (this report and artifacts)
  and the scratch dir, which was removed after the receipts were copied.

## 6. Artifacts

```
.ufo/waves/round-88/w1/MutHeldOut.md                        this report
.ufo/waves/round-88/w1/MutHeldOut/pristine.py               gate bytes probed (sha256 e3b0fab4…)
.ufo/waves/round-88/w1/MutHeldOut/mutants/                  24 .py + 24 .diff + manifest.json
.ufo/waves/round-88/w1/MutHeldOut/gen.py                    anchor-count-1 generator
.ufo/waves/round-88/w1/MutHeldOut/probe.py                  hand-fixture probe harness
.ufo/waves/round-88/w1/MutHeldOut/probe-results.json        25 fixtures × 25 gates, full answers
.ufo/waves/round-88/w1/MutHeldOut/receipts/                 48 3-run JSON+stdout receipts, rc.txt,
                                                            h05 extra-6-run receipt
.ufo/waves/round-88/w1/MutHeldOut/base88.json, base87.json  pristine baselines (38/38, 22/22 ×3)
.ufo/waves/round-88/w1/MutHeldOut/table.md                  the table above
.ufo/waves/round-88/w1/MutHeldOut/summary.json              machine-readable per-mutant rows
```

Reproduction (scratch fresh; lane read-only):

```
S=/fast/scratch/hyaku/tsukuroi-r88/MutHeldOut; mkdir -p "$S"
cp <lane>/.ufo/waves/round-88/before/roster/pos-landed-gate-3ba37eb0.py "$S/pristine.py"
python3 <lane>/tools/limine-pin-battery-r88.py --gate "$S/pristine.py" --runs 3 --work "$S/work"
python3 <lane>/tools/limine-pin-battery-r88.py --gate <mutant> --runs 3 --work "$S/work"
python3 <lane>/tools/limine-pin-battery-r87.py --gate <mutant> --runs 3 --work "$S/work"
```
