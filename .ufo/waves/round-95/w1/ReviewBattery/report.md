# ReviewBattery — seat report (round 95, wave w1)

Seat: `ReviewBattery` (reviewer, leaf; no subagent dispatch). Lane root:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Scratch:
`/fast/scratch/hyaku/tsukuroi-r95/ReviewBattery` (removed on exit). Receipts: this directory.
Scoped findings (variant table, clause verdicts, findings F1-F4): `../ReviewBattery.md`.

Tools installed/updated: none (no pacman, no uv/npx, no binary written). All runs use the lane's
`python3` and `bwrap` (`/usr/bin/bwrap`, present).

## 1. Instrument identity (before and after the attack)

```
$ sha256sum tools/check-limine-pins.py tools/limine-pin-battery-r95.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
a51dca18d3c7641664a2f64476a7abc2bb14ff1133772f109ac73490828b9ebb  tools/limine-pin-battery-r95.py
$ sha256sum -c .ufo/waves/round-95/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r95.py: OK
tools/make-r95-bends.py: OK
.ufo/waves/round-95/before/controls/bends/N05-strict-8.py: OK
.ufo/waves/round-95/before/controls/count-runs.py: OK
.ufo/waves/round-95/before/controls/do-nothing-battery-r94.py: OK
.ufo/waves/round-95/before/controls/do-nothing-gate-r94.py: OK
.ufo/waves/round-95/claims.json: OK
.ufo/waves/round-95/before/plan-frozen.md: OK
```

(Run twice: at seat start and after the last battery run. No instrument byte changed; the gate is
never edited — variants are copies.)

## 2. Variant construction (scratch only)

```
$ S=/fast/scratch/hyaku/tsukuroi-r95/ReviewBattery
$ mkdir -p "$S/work"
$ for v in a b c d; do cp tools/check-limine-pins.py "$S/variant-$v.py"; done
$ cp tools/check-limine-pins.py "$S/variant-e.py"    # after e/f were added
$ cp tools/check-limine-pins.py "$S/variant-f.py"
$ diff -u tools/check-limine-pins.py "$S"/variant-*.py > "$S"/variant-*.diff
```

One-clause edits (the edit tool, one clause per file; receipts `variant-a.diff` … `variant-f.diff`,
sources `variant-a.py` … `variant-f.py`):

| variant | clause | diff hunk |
|---|---|---|
| a | keep `len(p) <= 9`, reject exactly `(999999999,9,9)` | `+ if tuple(int(p) for p in parts) == (999999999, 9, 9): return None` at gate 101-102 |
| b | accept it, force era A when X has 9 digits | `era_b = version >= VISIBILITY_ERA_SPLIT and not (len(str(version[0])) == 9)` |
| c | accept it, clamp era tuple to `(12,9,5)` when X has 9 digits | `era_version = (12, 9, 5) if len(str(version[0])) == 9 else version` |
| d | accept it, echo `limine_version: "12.9.4"` when X has 9 digits | return dict, gate 316 |
| e | report `on_panic: "halt"` when X has 9 digits | return dict, gate 323 |
| f | accept 9-digit X, bend only the Y-component bound to `<= 8` | gate 99-100 |

## 3. Fixture soundness (battery's own `Case`, reproduced in scratch)

```
$ cd $S/probe && python3 ../fixture_probe.py
== fixture 1 conf lines (family REFUSAL-VERSIONS-9DIGIT, version '999999999.9.9')
 1 | /0m-04tw
 2 |   protocol: efi
 3 |   path: boot():/-zz3vodwqrj.efi#fdba4b2d…133038
 4 | hash_mismatch_panic: no
 5 | /xqdmh
 6 |   protocol:	efi
 7 |   path: boot():/zgc1ooi6/2adq_3ns.efi#16ef51c0…158ad92
== fixture 1 expectations
finish()      : (1, 'DEGRADED', [(3, 'LP-MISMATCH', 'panic'), (7, 'OK', 'none')])
want_on_panic : menu
r1_panic()    : None
global_lines  : []
era_b()       : True
first line starts with '/': True
== fixture freshness (two builds, same family)
conf byte-identical: False
file-name sets intersect: []
== direct gate runs on fixture 1 with --limine-version '999999999.9.9'
landed     rc=1 verdict=DEGRADED pins=[(3, 'LP-MISMATCH', 'panic'), (7, 'OK', 'none')] on_panic=menu visibility_era=12.9.5+ limine_version=999999999.9.9 source=flag
variant-a  rc=64 stdout=<non-JSON> stderr='…check-limine-pins: --limine-version must be X.Y.Z or auto'
variant-b  rc=1 verdict=DEGRADED pins=[(3, 'LP-MISMATCH', 'prompt'), (7, 'OK', 'none')] on_panic=menu visibility_era=pre-12.9.5 limine_version=999999999.9.9 source=flag
variant-c  rc=1 verdict=DEGRADED pins=[(3, 'LP-MISMATCH', 'panic'), (7, 'OK', 'none')] on_panic=menu visibility_era=12.9.5+ limine_version=999999999.9.9 source=flag
variant-d  rc=1 verdict=DEGRADED pins=[(3, 'LP-MISMATCH', 'panic'), (7, 'OK', 'none')] on_panic=menu visibility_era=12.9.5+ limine_version=12.9.4 source=flag
```

Era discriminator (same fixture, landed gate; `era-discriminator.txt`):

```
version=12.9.4           rc=1 verdict=DEGRADED era=pre-12.9.5  pins=[(3, 'LP-MISMATCH', 'prompt'), (7, 'OK', 'none')]
version=12.9.5           rc=1 verdict=DEGRADED era=12.9.5+     pins=[(3, 'LP-MISMATCH', 'panic'), (7, 'OK', 'none')]
version=12.9.6           rc=1 verdict=DEGRADED era=12.9.5+     pins=[(3, 'LP-MISMATCH', 'panic'), (7, 'OK', 'none')]
version=999999999.9.9    rc=1 verdict=DEGRADED era=12.9.5+     pins=[(3, 'LP-MISMATCH', 'panic'), (7, 'OK', 'none')]
```

Gate path (quoted in `gate-code-excerpt.txt`): `parse_limine_version` 91-103 accepts three ASCII-digit
components with `len(p) <= 9`; `VISIBILITY_ERA_SPLIT = (12, 9, 5)` 104; `era_b = version >= split` 193;
first-entry scan 216-220 and `in_global = False` for line 1 in era B 223-226; the `hash_mismatch_panic`
read is gated on `in_global` 235-236; `prompt` 258; mismatch consequence 305-306; JSON
`visibility_era` 318. The fixture's expected `panic` is therefore the visibility rule's answer, and the
12.9.4 row shows the same file would answer `prompt` in era A (the fixture discriminates).

## 4. Battery runs (exact commands, raw result lines)

```
$ python3 tools/limine-pin-battery-r95.py --gate <G> --runs 1 --work $S/work-<name> --json $S/battery-<name>.json
$ python3 .ufo/waves/round-95/before/controls/count-runs.py $S/battery-<name>.json --family REFUSAL-VERSIONS-9DIGIT
```

(landed/variant-a..f run in parallel; N05/r94 controls and ×3 legs in a second parallel batch)

| gate (`--gate`) | r95 battery `--runs 1` | r95 `--runs 3` | r94 do-nothing battery |
|---|---|---|---|
| landed `tools/check-limine-pins.py` | `met` 99/99, failed `[]`, 0 errors | `met` 99/99 ×3, failed `[]`, 0 errors | `met` 98/98, 0 errors, 0 family rows |
| variant-a | `unmet` 98/99, failed `["REFUSAL-VERSIONS-9DIGIT"]`, 4 errors | — | `met` 98/98 |
| variant-b | `unmet` 98/99, failed `["REFUSAL-VERSIONS-9DIGIT"]`, 0 errors | — | `met` 98/98 |
| variant-c | `met` 99/99, failed `[]`, 0 errors | — | `met` 98/98 |
| variant-d | `met` 99/99, failed `[]`, 0 errors | — | `met` 98/98 |
| variant-e | `unmet` 98/99, failed `["REFUSAL-VERSIONS-9DIGIT"]`, 0 errors | — | `met` 98/98 |
| variant-f | `met` 99/99, failed `[]`, 0 errors | — | `met` 98/98 |
| `before/controls/bends/N05-strict-8.py` | `unmet` 98/99, failed `["REFUSAL-VERSIONS-9DIGIT"]`, 4 errors | `unmet` 98/99 ×3, 4 errors each | `met` 98/98 |

Raw log lines:

```
landed                : families_passed 99/99 verdict met failed -
landed (x3, run 1..3) : families_passed 99/99 verdict met failed -   (three identical lines)
variant-a             : families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT
variant-b             : families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT
variant-c             : families_passed 99/99 verdict met failed -
variant-d             : families_passed 99/99 verdict met failed -
variant-e             : families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT
variant-f             : families_passed 99/99 verdict met failed -
N05-strict-8 r95      : families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT  (x4: x1 + x3)
N05-strict-8 r95 x3   : three identical lines, 4 error rows each
N05-strict-8 r94      : families_passed 98/98 verdict met failed -
landed r94            : families_passed 98/98 verdict met failed -
r94 on variant-a..f   : families_passed 98/98 verdict met failed -   (six runs)
```

Per-case rows for the family (`case-rows.txt`, `case-rows-legs.txt`, `x3-detail.txt`):

```
landed     : 4/4 passed; want [1,'DEGRADED',[[3,'LP-MISMATCH','panic'],[7,'OK','none']],'menu']; got [1,'DEGRADED',…,1,'menu','999999999.9.9','flag']
variant-a  : 0/4 passed; got None; error "bad-output: JSONDecodeError rc=64" on all four (empty JSON output)
variant-b  : 0/4 passed; got [1,'DEGRADED',[[3,'LP-MISMATCH','prompt'],[7,'OK','none']],…]
variant-c  : 4/4 passed; got [1,'DEGRADED',[[3,'LP-MISMATCH','panic'],[7,'OK','none']],…]
variant-d  : 4/4 passed; got [1,'DEGRADED',[[3,'LP-MISMATCH','panic'],[7,'OK','none']],1,'menu','12.9.4','flag']
variant-e  : 0/4 passed; got [1,'DEGRADED',[[3,'LP-MISMATCH','panic'],[7,'OK','none']],1,'halt','999999999.9.9','flag']
variant-f  : 4/4 passed; got [1,'DEGRADED',[[3,'LP-MISMATCH','panic'],[7,'OK','none']],1,'menu','999999999.9.9','flag']
N05 r95 x3 : 0/4 passed per run; error "bad-output: JSONDecodeError rc=64" ×4 per run; err families exactly ['REFUSAL-VERSIONS-9DIGIT']
```

Roster facts (`rosters.txt`): r95 `FAMILY_ROSTER` 99 names, 99 unique, family present exactly once,
`FAMILIES` keys == roster, `CASES_PER_FAMILY = 4`; r94 control roster 98 names, 98 unique, family
present 0 times.

Cap-boundary probes (`boundary-probe.txt`, `middle-bound-probe.txt`):

```
landed 999999999.9.9                 rc=1  verdict=DEGRADED era=12.9.5+   (the family's value)
landed 999999999.999999999.999999999 rc=1  verdict=DEGRADED era=12.9.5+   (true component-wise max, in-bound)
landed 999999999.9.10                rc=1  verdict=DEGRADED era=12.9.5+
landed 12.999999999.999999999        rc=1  verdict=DEGRADED era=12.9.5+
landed 0.999999999.9                 rc=1  verdict=DEGRADED era=pre-12.9.5
landed 1000000000.9.9                rc=64 (ten-digit component refused)
landed 999999999.0.0                 rc=1  verdict=DEGRADED era=12.9.5+
variant-f 0.999999999.9              rc=64 (its bent Y bound); family value 999999999.9.9 rc=1
```

## 5. PASS/FAIL per expected line

C1/A1 target lines (the frozen claim), each re-measured by this seat:

| # | expected | observed | verdict |
|---|---|---|---|
| 1 | landed gate r95 `99/99` met, `failed_families []` | met 99/99 in each of three runs | PASS |
| 2 | landed gate r95 0 error rows | 0 in each of three runs (`x3-detail.txt`) | PASS |
| 3 | N05-strict-8 r95 `98/99` unmet, `failed_families == ["REFUSAL-VERSIONS-9DIGIT"]` | unmet 98/99 ×4 (×1 + ×3), exactly that family | PASS |
| 4 | N05-strict-8 r95 four case rows carry the battery error text (rc 64, no JSON) | 4/run, all `bad-output: JSONDecodeError rc=64` | PASS |
| 5 | N05-strict-8 r94 `met 98/98`, 0 error rows, 0 family rows | met 98/98, 0, 0 | PASS |
| 6 | landed gate r94 `met 98/98`, 0 error rows, 0 family rows | met 98/98, 0, 0 | PASS |
| 7 | family in the r95 roster; absent from the r94 roster | 99/1 present, 98/0 present | PASS |
| 8 | fixtures generated fresh per run | two builds of the same family differ in conf bytes and file names | PASS |
| 9 | fixture's first physical line is an entry label; era B answers `panic` | line 1 `/0m-04tw`; pins `(3, LP-MISMATCH, panic)`; era `12.9.5+`; 12.9.4 answers `prompt` | PASS |
| 10 | canonical `99/99` in every run | ×3 identical | PASS |
| 11 | clone layout | not run by this seat (execution seat's leg) | UNTESTED here |

Attack predictions (not C1 target lines; disagreements are findings):

| variant | prediction | observed | verdict |
|---|---|---|---|
| a | caught (refusal of the in-bound value) | unmet 98/99, 4 errors | PASS |
| b | caught (era-A answer) | unmet 98/99, `prompt` | PASS |
| c | caught if the *mechanism* is enforced | met 99/99 → not caught | FAIL (finding F2) |
| d | caught if the echoed version is asserted | met 99/99 → not caught | FAIL (finding F3) |
| e | caught (`on_panic` field) | unmet 98/99, `halt` | PASS |
| f | caught if the per-component accepted cap is certified | met 99/99 → not caught | FAIL (finding F1) |
| r94 roster | blind to all six variants | met 98/98 for a-f | PASS (blindness confirmed) |

`n05-diff.txt` confirms the bend is one line: `len(p) <= 9` → `len(p) <= 8` with the `# N05` comment.

## 6. Receipts (all under this directory; written by this seat)

- `variant-a.py` … `variant-f.py`, `variant-a.diff` … `variant-f.diff` — the six one-clause gates and
  their diffs against `tools/check-limine-pins.py`.
- `fixture_probe.py`, `fixture-probe.txt`, `era-discriminator.txt` — fixture reproduction, freshness,
  era split.
- `boundary-probe.txt`, `middle-bound-probe.txt` — cap boundary and per-component accepted-side probes.
- `battery-landed.json/.log`, `battery-landed-x3.json/.log`, `battery-variant-a..f.json/.log`,
  `battery-n05-r95.json/.log`, `battery-n05-x3.json/.log`, `battery-n05-r94.json/.log`,
  `battery-landed-r94.json/.log`, `battery-r94-variant-a..f.json/.log`.
- `count-runs.txt`, `case-rows.txt`, `case-rows-legs.txt`, `x3-detail.txt`, `summary.json`,
  `rosters.txt`, `gate-code-excerpt.txt`, `n05-diff.txt`.
- `summarize.py` — regenerates `summary.json` from the battery JSONs.
- `MANIFEST.sha256` — digests of the receipts.

Scratch `/fast/scratch/hyaku/tsukuroi-r95/ReviewBattery` was deleted before this report was filed; the
JSONs' embedded `gate` field names that (now absent) scratch path, and the variant sources are copied
here.

## 7. Verdict

See `../ReviewBattery.md` §5 for the per-clause table. In one line: C1's operational target is
reproduced (landed 99/99 ×3; N05 98/99 ×3 family-only with four rc-64 errors; r94 blindness 98/98);
the wording overstates the cap ("largest in-bound member" is false; the component-wise max is accepted
but untested), and the era mechanism, echoed version, and per-component accepted boundary are
unasserted by the instrument (`findings`, not `unmet`).

{"seat":"ReviewBattery","verdict":"findings","notes":"C1 operational target reproduced (landed 99/99 x3, N05 98/99 x3 family-only with 4 rc64 errors, r94 blindness 98/98, instruments verified 9/9); wording gaps: 'largest in-bound member' falsified (true component-wise max 999999999.999999999.999999999 accepted but unexercised), era mechanism/visibility_era and echoed limine_version unasserted (variants c,d met 99/99), per-component accepted cap only X-certified (variant f met 99/99), on_panic checked but constant; clone leg untested here."}
