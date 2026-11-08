# ExecDoNothing — round 97 w1 — do-nothing blindness control

Seat: ExecDoNothing. Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Scratch: `/fast/scratch/hyaku/tsukuroi-r97/ExecDoNothing` (deleted before yield).
No tools installed or upgraded; no pacman, no sudo, no git/jj mutation.

## Axes named

- **axis A — control integrity**: the bytes that ran are the r96 landed bytes, and the
  manifest still pins them.
- **axis B — blindness**: the r96 103-family battery reads `met 103/103` on the landed
  gate and on both r97 bends.
- **axis C — superset scoring**: the r97 105-family battery still scores every r96 family.

All three improve or hold; nothing below changes any lane file.

## 1. Control bytes (expected: `f06d90ae…`, byte-identical to the r96 landed instrument)

```
$ sha256sum .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py
f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba  .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py
$ git show 38adc4ed:tools/limine-pin-battery-r96.py > <scratch>/r96-landed.py
$ sha256sum <scratch>/r96-landed.py
f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba  <scratch>/r96-landed.py
$ cmp .ufo/…/controls/do-nothing-battery-r96.py <scratch>/r96-landed.py && echo CMP_BYTE_IDENTICAL
CMP_BYTE_IDENTICAL
$ git diff 38adc4ed HEAD -- tools/limine-pin-battery-r96.py | wc -l
0
```

`38adc4ed` is the r96 freeze commit that last touched the r96 instrument
(`git log --format='%H %s' -- tools/limine-pin-battery-r96.py`).

**PASS** — hash equals the frozen value; `cmp` byte-identical; zero diff r96-tip..HEAD.
Receipt: `dn-control-bytes.txt`.

## 2. Control on the landed gate (expected: `met 103/103` ×3, 0 error rows)

```
$ python3 .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py \
    --gate tools/check-limine-pins.py --runs 3 --work <scratch>/gate \
    --json .ufo/waves/round-97/w1/ExecDoNothing/dn-gate.json
families_passed 103/103 verdict met failed -
families_passed 103/103 verdict met failed -
families_passed 103/103 verdict met failed -
EXIT:0
```

Receipt parse (`dn-gate.json`, list of 3 runs):

```
met 103/103 failed [] rows 412 err 0
met 103/103 failed [] rows 412 err 0
met 103/103 failed [] rows 412 err 0
```

**PASS** — 3× `met`, 103/103, `failed_families []`, 412 case rows (103x4), 0 error rows.

## 3. Control on each bend ×3 (expected: `met 103/103` ×3, 0 error rows each)

```
$ python3 …/do-nothing-battery-r96.py \
    --gate .ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py \
    --runs 3 --work <scratch>/N05 --json …/dn-N05-z-cap-8.json
families_passed 103/103 verdict met failed -   (x3)
EXIT:0
```

```
$ python3 …/do-nothing-battery-r96.py \
    --gate .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py \
    --runs 3 --work <scratch>/N06 --json …/dn-N06-leading-zero-reject.json
families_passed 103/103 verdict met failed -   (x3)
EXIT:0
```

Receipt parses:

```
== dn-N05-z-cap-8            met 103/103 failed [] rows 412 err 0   (x3)
== dn-N06-leading-zero-reject met 103/103 failed [] rows 412 err 0   (x3)
```

**PASS (both bends)** — the r96 103-family roster is blind to `N05-z-cap-8` and to
`N06-leading-zero-reject`: neither bend moves a single family.

Structural corroboration (`roster-compare.txt`): the r96 instrument's only 9-digit
spellings put the cap in X (`"9"*9 + ".9.9"`) or Y (`12.999999999.4`,
`0.999999999.0`) — no third-component 9-digit value, so `N05`'s Z bound has no case
to bite. The r96 *roster* has no leading-zero family at all.

## 4. `--usage-check` on the control (item expected: `12.9.6.1` and `999999999.0.0`, no 9-digit Z, no leading-zero value)

```
$ python3 …/do-nothing-battery-r96.py --gate tools/check-limine-pins.py \
    --usage-check --work <scratch>/usage-gate
EXIT:0
```

Case list and result (`dn-usage-case-list.txt`, 15 cases, all ok, schema
`tsukuroi-limine-pins-usage-r96-v1`):

```
'12.9'         want 64 rc 64 ok True
'abc'          want 64 rc 64 ok True
'12.9.6.1'     want 64 rc 64 ok True
''             want 64 rc 64 ok True
'999999999999…len=5004' want 64 rc 64 ok True
'1234567890.0.0'        want 64 rc 64 ok True
'0.1234567890.0'        want 64 rc 64 ok True
'999999999.0.0'         want 0  rc 0  ok True
'12.9.4'       want 0  rc 0  ok True
'12.9.5'       want 0  rc 0  ok True
'13.0.0'       want 0  rc 0  ok True
'12.09.4'      want 0  rc 0  ok True
'00.00.00'     want 0  rc 0  ok True
'auto'         want None rc 0 ok True
None           want None rc 0 ok True
verdict met
```

Expected-line verdict:

- sends `12.9.6.1` → **PASS** (present, rc 64).
- sends `999999999.0.0` → **PASS** (present, rc 0).
- no 9-digit Z → **PASS** (only 9-digit components are X `999999999` and Y `1234567890`,
  the latter refused; the third component is never 9 digits).
- “no leading-zero value” → **FAIL, the run wins**: the list sends `12.09.4` and
  `00.00.00` with `want_rc 0`. `12.09.4` is literally one of C1's
  `LEADING-ZERO-NORMALIZE` members.

Consequence measured, not inferred — the usage leg is a *partial* leading-zero
discriminator already in the r96 instrument:

```
$ … do-nothing-battery-r96.py --gate bends/N05-z-cap-8.py --usage-check
N05-z-cap-8 EXIT:0 verdict met failing []
$ … do-nothing-battery-r96.py --gate bends/N06-leading-zero-reject.py --usage-check
N06-leading-zero-reject EXIT:1 verdict unmet
failing [('12.09.4', 0, 64), ('00.00.00', 0, 64)]
```

So: blind on the scored 103-family roster (the clause C1 freezes), **not** blind in
`--usage-check` to `N06`. `N05` is blind in both legs (no 9-digit Z anywhere).

## 5. r97 battery still scores the r96 roster (expected: 105/105 met ×3)

```
$ python3 tools/limine-pin-battery-r97.py --gate tools/check-limine-pins.py \
    --runs 3 --work <scratch>/r97-gate --json …/c1-r97-gate.json
families_passed 105/105 verdict met failed -   (x3)
EXIT:0
```

Receipt parse: 3 runs, `met 105/105`, `failed_families []`, 420 case rows (105x4),
0 error rows.

AST roster comparison (`roster-compare.txt`):

```
r96 roster len: 103
r97 roster len: 105
r96 subset of r97: True
missing from r97: []
added by r97: ['REFUSAL-VERSIONS-9DIGIT-Z', 'LEADING-ZERO-NORMALIZE']
order-preserving prefix: True
```

**PASS** — `105 = 103 + 2`, r96’s roster preserved in order, all r96 families scored.

## 6. Manifest check at scoring time

```
$ sha256sum -c .ufo/waves/round-97/before/instruments.sha256
… 19 entries: OK
.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh: FAILED
sha256sum: WARNING: 1 computed checksum(s) did NOT match
```

The same command read **20/20 OK** at session start (08:50). The fixture file now hashes
`e4cf82a0f4c6307e057fd0b75c7bcadb21eb6c972859cd3ba1c837eccc74081f` against the pinned
`c2ecf729…`, `git status --porcelain` shows ` M`, mtime 08:52:21. Capture:
`fixture-drift-capture.txt` (diff: +6 lines pinning the fixture base to `f48d1642` and
recording the checker digest).

Every instrument this seat measured is unaffected and still `OK`: `check-limine-pins.py`
(`7d79ac29…`), `limine-pin-battery-r97.py` (`e678c34f…`), `make-r97-bends.py`,
`check-registry-content.py`, `check-registry-coverage.py`, `check-r96-calibration.py`,
`do-nothing-battery-r96.py` (`f06d90ae…`), both bends, plans, claims.
No file outside this seat dir and scratch was written by this seat.

## Findings

- **F1 (wording vs bytes, non-C1).** The seat item’s usage-check expectation (“no
  leading-zero value”) is false: `12.09.4` and `00.00.00` are sent with `want_rc 0`, and
  the r96 usage leg therefore reads `unmet` on `N06-leading-zero-reject`. C1’s frozen
  do-nothing reading is the 103-family roster, which is blind; the blindness statement
  must be scoped to that leg, not to the whole instrument.
- **F2 (frozen-manifest drift, C2 surface).** `before/fixtures/build-doctored-fixture.sh`
  changed during the wave (+6 lines, sha `e4cf82a0…` vs pinned `c2ecf729…`). It is not a
  C1 instrument, but `sha256sum -c` no longer reads clean for the manifest as a whole.
  Not repaired here (out of seat scope; frozen dir is read-only for this seat).

## Blindness leg verdict

**Holds, as frozen:** on the landed gate and on both bends the r96 control reads
`met 103/103` in all three runs with 0 error rows (9 runs, 0 failures), and the r97
battery scores the landed gate `105/105` ×3 with the r96 roster intact. Qualified by F1
for the instrument’s separate `--usage-check` leg.

## Receipts (all under `.ufo/waves/round-97/w1/ExecDoNothing/`)

`dn-control-bytes.txt`, `dn-gate.json`, `dn-N05-z-cap-8.json`,
`dn-N06-leading-zero-reject.json`, `dn-usage-gate.json`, `dn-usage-case-list.txt`,
`dn-usage-check.txt`, `dn-usage-N05-z-cap-8.json`, `dn-usage-N06-leading-zero-reject.json`,
`c1-r97-gate.json`, `roster-compare.txt`, `fixture-drift-capture.txt`.

## Adjudication (L1)

Both findings are adjudicated. Raw readings above are unchanged; this section is appended
as the L1's record and the pointers it cites were re-verified read-only by this seat.

- **F1 — fixture drift (the L1 labels it F1; labelled F2 in the raw rows above).** The
  `before/fixtures/build-doctored-fixture.sh` change (`c2ecf729…` -> `e4cf82a0…`) was the
  L1's post-freeze C2 recipe correction, pinning the fixture's clone base to `f48d1642`
  so a re-run reads the coverage gate's correct `PASS 154/154` rather than its own
  `REGISTRY-ROW-MISSING` (post-freeze `tools_total` is 157). Recorded as **A1** in
  `.ufo/waves/round-97/before/plan-amendments-r97.md`. The four scoring instruments, both
  bends and the three do-nothing copies are byte-identical to the freeze manifest; the
  corrected set is re-pinned in
  `.ufo/waves/round-97/before/instruments-r97-after-fixture-pin.sha256`, which this seat
  re-ran read-only at adjudication time: 20/20 `OK`. C1's void clause is evaluated on
  that file with A1 as its narrowing pointer. No seat wrote into `before/`; the writes
  were the L1's.
- **F2 — usage-check scope (the L1 labels it F2; labelled F1 in the raw rows above).**
  Recorded as **A3** in the same amendments file. The blindness receipt is the ROSTER leg
  (`--runs 3`, `met 103/103`, 0 error rows, 9/9 runs above); the r96 `--usage-check`
  already sends `12.09.4` and `00.00.00` and reads `unmet` on N06, so the leading-zero
  class is a roster-level closure (QUALITY 136), while no r96 leg sends a 9-digit Z value
  — the Z class is new at both levels. The two raw rows this seat measured,
  `[('12.09.4', 0, 64), ('00.00.00', 0, 64)]` (from `dn-usage-N06-leading-zero-reject.json`),
  are the evidence A3 cites.

{"seat":"ExecDoNothing","verdict":"findings","notes":"Do-nothing clause holds on the frozen 103-family leg: control sha256 f06d90ae matches and cmp is byte-identical to 38adc4ed:tools/limine-pin-battery-r96.py (0-line diff); control reads met 103/103 x3 with 0 error rows on the landed gate, on N05-z-cap-8 and on N06-leading-zero-reject (9 runs, 0 failures); r97 battery reads met 105/105 x3, 420 rows, 0 error rows on the landed gate and its roster is r96's 103 in order plus the two new families. Usage scope (raw row label F1; L1 A3): the item's claim that --usage-check carries no leading-zero value is false - it sends 12.09.4 and 00.00.00 with want_rc 0 and reads unmet on N06 (12.09.4 rc 64, 00.00.00 rc 64), met on N05; blindness is roster-level and the Z class is new at both levels. Fixture drift (raw row label F2; L1 A1): before/fixtures/build-doctored-fixture.sh moved c2ecf729 to e4cf82a0 by the L1's own C2 recipe correction, so the freeze manifest read 19 OK / 1 FAILED at scoring time; all C1 instruments remained OK, the corrected set is re-pinned in before/instruments-r97-after-fixture-pin.sha256 (20/20 OK, re-run by this seat), and C1's void clause is evaluated on that file with A1 as its pointer. No tools installed; no git/jj mutations; scratch removed."}
