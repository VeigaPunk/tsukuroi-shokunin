# Seat ExecControl — round 100 / w1 — C1's do-nothing control (r98) against the two echo bends

Assignment: the r98 battery (`8198bd84…`, the do-nothing control) must be **blind** to the
`N13-y-echo` lie and only **partly sighted** on `N12-x-echo`, in both the canonical and the
`git clone --shared` layout, `--runs 3`, 0 error rows.

## Axes (named before measuring)

- **A1 identity** — the control's bytes are the frozen bytes (three independent sources agree).
- **A2 discrimination** — each leg reads the verdict/`failed_families` the claim predicts.
- **A3 layout invariance** — the same readings from the lane tree and from a shared clone.
- **A4 error hygiene** — zero non-null `error` rows in every run.

Moves kept: the three canonical legs and the three clone legs (each is an independent
`--runs 3` batch); every one improves A3/A4 evidence and none harms A1/A2. Nothing was
retried toward a pass: the six readings below are the first and only batches run.

## 1. Control identity — PASS (three sources, one digest)

```
$ sha256sum .ufo/waves/round-100/before/controls/do-nothing-battery-r98.py tools/limine-pin-battery-r98.py
8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87  .ufo/waves/round-100/before/controls/do-nothing-battery-r98.py
8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87  tools/limine-pin-battery-r98.py
$ git show ce73ccaf…:tools/limine-pin-battery-r98.py | sha256sum
8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87  -
$ sha256sum <clone>/tools/limine-pin-battery-r98.py
8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87  <clone>/tools/limine-pin-battery-r98.py
```

Manifest line for the same file, from `.ufo/waves/round-100/before/instruments.sha256`:
`8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87  tools/limine-pin-battery-r98.py`
— **PASS** (four sources: manifest, lane copy, pre-round tip blob, clone copy).

Article identity (unchanged gate + the two bends, both one changed line):

```
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
eb247e1646d1b421cf047f2b2edeb34423227b5ca056edcaf0712924b3f0331a  …/bends/N12-x-echo.py
e1e5916fad0ee545a0571c852ebf658269322a138e802bcff5e875ab868bebee  …/bends/N13-y-echo.py
diff -u tools/check-limine-pins.py …/bends/N12-x-echo.py  -> 1 removed + 1 added line (the limine_version line)
diff -u tools/check-limine-pins.py …/bends/N13-y-echo.py  -> 1 removed + 1 added line (the limine_version line)
```
**PASS** (each bend's diff is exactly one changed line; the gate's own digest is the manifest's).

## 2. Canonical layout — three legs, `--runs 3`

```
$ python3 .ufo/waves/round-100/before/controls/do-nothing-battery-r98.py \
    --gate tools/check-limine-pins.py --runs 3 \
    --work /fast/scratch/hyaku/tsukuroi-r100/ExecControl/canon-gate \
    --json .ufo/waves/round-100/w1/ExecControl/dn-gate-canonical.json
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -                                   (1m17.5s)

$ … --gate .ufo/waves/round-100/before/controls/bends/N12-x-echo.py … --json …/dn-N12-x-echo-canonical.json
families_passed 104/105 verdict unmet failed EXPLICIT-VERSION-ECHO
families_passed 104/105 verdict unmet failed EXPLICIT-VERSION-ECHO
families_passed 104/105 verdict unmet failed EXPLICIT-VERSION-ECHO              (1m22.2s)

$ … --gate .ufo/waves/round-100/before/controls/bends/N13-y-echo.py … --json …/dn-N13-y-echo-canonical.json
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -                                   (1m22.5s)
```

## 3. Shared-clone layout — same three legs, the clone's own control bytes

```
$ git clone --shared --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
    /fast/scratch/hyaku/tsukuroi-r100/ExecControl/clone
$ git -C <clone> rev-parse --show-toplevel      -> /fast/scratch/hyaku/tsukuroi-r100/ExecControl/clone
$ git -C <clone> rev-parse HEAD                 -> 69474c55eb38632f3e740923b58029dc43e01300 (master, landing tip)
$ sha256sum <clone>/tools/limine-pin-battery-r98.py
8198bd84…  (identical to the control)
$ cd <clone> && python3 .ufo/waves/round-100/before/controls/do-nothing-battery-r98.py \
    --gate tools/check-limine-pins.py --runs 3 --work …/clone-gate --json …/dn-gate-clone.json
families_passed 105/105 verdict met failed -   x3                              (1m49.8s)
$ … --gate .ufo/…/bends/N12-x-echo.py … --json …/dn-N12-x-echo-clone.json
families_passed 104/105 verdict unmet failed EXPLICIT-VERSION-ECHO   x3        (1m50.2s)
$ … --gate .ufo/…/bends/N13-y-echo.py … --json …/dn-N13-y-echo-clone.json
families_passed 105/105 verdict met failed -   x3                              (1m50.1s)
```

## 4. Parse with the round-95 counter

```
$ python3 .ufo/waves/round-95/before/controls/count-runs.py <dn-…json> \
    --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family EXPLICIT-VERSION-ECHO
```

| leg | layout | runs | verdict | families_passed | failed_families | error_rows | named (pass/fail per family) |
|---|---|---|---|---|---|---|---|
| gate | canonical | 3 | met ×3 | 105/105 ×3 | `[]` ×3 | 0 | ECHO 4/0, 9DIGIT 4/0, 9DIGIT-Y 4/0 |
| gate | clone | 3 | met ×3 | 105/105 ×3 | `[]` ×3 | 0 | ECHO 4/0, 9DIGIT 4/0, 9DIGIT-Y 4/0 |
| N12-x-echo | canonical | 3 | unmet ×3 | 104/105 ×3 | `["EXPLICIT-VERSION-ECHO"]` ×3 | 0 | ECHO **3/1**, 9DIGIT 4/0, 9DIGIT-Y 4/0 |
| N12-x-echo | clone | 3 | unmet ×3 | 104/105 ×3 | `["EXPLICIT-VERSION-ECHO"]` ×3 | 0 | ECHO **3/1**, 9DIGIT 4/0, 9DIGIT-Y 4/0 |
| N13-y-echo | canonical | 3 | met ×3 | 105/105 ×3 | `[]` ×3 | 0 | ECHO 4/0, 9DIGIT 4/0, **9DIGIT-Y 4/0** |
| N13-y-echo | clone | 3 | met ×3 | 105/105 ×3 | `[]` ×3 | 0 | ECHO 4/0, 9DIGIT 4/0, **9DIGIT-Y 4/0** |

`count-runs.py` exits 0 on the four `met` batches and **1** on the two `N12` batches — that exit
code is the counter's own contract ("Exit 0 iff every run … meets the frozen targets"), and the
`N12` legs are *supposed* to be unmet here; the JSON is the evidence, not the exit status.

Raw shape of each `case_log` (420 rows per run = 105 families × 4 cases; 1260 rows per batch).

The failing row in every `N12` run is the same one — the X-cap spelling, echo falsified, pins/rc
untouched:

```
family EXPLICIT-VERSION-ECHO, passed=false, error=null
want [1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],"menu"]
got  [1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],1,"menu","999999998.9.9","flag"]
```

The four Y-family rows in every `N13` run carry the Y lie in `got` and still pass, because the r98
family never compares the echo:

```
family REFUSAL-VERSIONS-9DIGIT-Y, passed=true (×4)
want [1,"DEGRADED",[[3,"LP-MISMATCH","panic"],…],"menu"]          <- 4-element want: no echo assertion
got  [1,"DEGRADED",[[3,"LP-MISMATCH","panic"],…],1,"menu","12.999999998.4","flag"]
```

## 5. Discrimination claim — one sentence per leg

- **Landed gate (`7d79ac29…`)**: the r98 control sees the true gate as fully consistent — `met
  105/105` in all six runs, no family in `failed_families`, so every later delta is attributable to
  the article and not to the battery's own state.
- **`N12-x-echo`**: the r98 control catches the X-cap echo lie **only** through
  `EXPLICIT-VERSION-ECHO` (1 of 4 of its cases sends `999999999.9.9`) and is blind to the *same
  spelling* in `REFUSAL-VERSIONS-9DIGIT` (4/4 pass, `check_echo` not set there), so it reads a
  one-family delta `unmet 104/105 ["EXPLICIT-VERSION-ECHO"]` where the r99 battery reads
  `unmet 103/105 ["EXPLICIT-VERSION-ECHO","REFUSAL-VERSIONS-9DIGIT"]`.
- **`N13-y-echo`**: the r98 control cannot see the Y-cap echo lie at all — its
  `REFUSAL-VERSIONS-9DIGIT-Y` family compares rc/pins/era (4/4 pass) and never the
  `limine_version` echo, so it reads `met 105/105` on a gate whose `limine_version` is false exactly
  for `12.999999999.4` and `0.999999999.0`, the met-to-unmet closure the r99 battery supplies.

## 6. Structural reason (why the control is blind where it is)

`python3` scan of `tools/limine-pin-battery-r98.py` top-level family functions for `c.check_echo =
True` / `c.check_era = True` and for the spelling `999999999`:

```
fam_refusal_versions           echo=False era=False mentions999M=True
fam_refusal_versions_9digit    echo=False era=False mentions999M=True    <- X cap, echo unread
fam_explicit_version_echo      echo=True  era=False mentions999M=True    <- the only X-cap echo witness
fam_explicit_version_era       echo=False era=True  mentions999M=False
fam_refusal_versions_9digit_y  echo=False era=False mentions999M=True    <- Y cap, echo unread
fam_refusal_versions_9digit_z  echo=True  era=True  mentions999M=True
fam_leading_zero_normalize     echo=True  era=True  mentions999M=False
```

r98 carries 6 `check_echo/check_era` assignments; r99 carries 10, and in r99 the 9-digit X family
gains `c.check_echo = True` and the Y family gains `c.check_echo = True` + `c.check_era = True`
(r99 docstring: "closing the r98 G6 Y-cap-only era-lie survivor"). The two added echo assertions are
exactly the two families the control misses.

## 7. Guard receipts

```
$ sha256sum -c .ufo/waves/round-100/before/instruments.sha256 | grep -c ': OK'
16            (all 16 pinned entries OK; no FAILED line)
$ python3 tools/check-registry-coverage.py --revision 69474c55eb38632f3e740923b58029dc43e01300
{"branch":"master","branch_tip":"69474c55…","counts":{"findings":0,"missing":0,"registered":165,
 "rows_total":165,"tools_total":165},"findings":[],"revision":"69474c55…","status":"PASS"}
```
Reported as found: **PASS**, 0 findings, 0 missing, 165/165 rows.

Disk guard before the heavy passes: `disk-guard.sh status` ran clean; `/fast` 284 G available.
No tool was installed or upgraded this seat (nothing needed); no pacman transaction was run.

## 8. Findings, limits

- **No finding against the claim**: all six acceptance lines hold; no leg differs, so there is no
  raw-divergence row to report.
- Recorded, not claimed: the r98 control's `N12` reading is a *delta*, never a flip — it is unmet on
  the same spelling the r99 battery is unmet on, differing only in one family. This is the shape the
  round-100 plan's Limits section already names.
- Recorded: the `N12` count receipt exits 1. That is `count-runs.py`'s contract, not a defect of
  the leg; the receipt JSON is kept verbatim (`count-N12-x-echo-{canonical,clone}.json`).
- The clone is a `--shared` clone of the lane at `master` = `69474c55…` (the landing tip), not at
  `ce73ccaf…`; the control's *bytes* there are still `8198bd84…`, which is what the layout test
  exercises. `ce73ccaf…` was used for the third identity source (the pre-round tip blob).
- No mutation, commit, or write outside this seat dir and the scratch dir; no `git`/`jj` mutation
  ran. Scratch `/fast/scratch/hyaku/tsukuroi-r100/ExecControl` was deleted after the receipts were
  copied into this seat dir.

## 9. Receipts (all under `.ufo/waves/round-100/w1/ExecControl/`)

| file | what it is |
|---|---|
| `dn-gate-canonical.json`, `dn-gate-clone.json` | battery JSON, 3 runs each |
| `dn-N12-x-echo-canonical.json`, `dn-N12-x-echo-clone.json` | battery JSON, 3 runs each |
| `dn-N13-y-echo-canonical.json`, `dn-N13-y-echo-clone.json` | battery JSON, 3 runs each |
| `count-{gate,N12-x-echo,N13-y-echo}-{canonical,clone}.json` | `count-runs.py` output per batch |
| `identity-and-guards.txt` | identity, bend digests, diff line counts, manifest, coverage |
| `receipts.sha256` | digests of every receipt above |

## 10. Verdict

```json
{"seat":"ExecControl","verdict":"met","notes":"r98 control = 8198bd84… from four sources; canonical and shared-clone layouts, --runs 3 each: landed gate met 105/105 (6/6 runs), N13-y-echo met 105/105 (6/6, blind), N12-x-echo unmet 104/105 with failed_families exactly [EXPLICIT-VERSION-ECHO] (6/6, never REFUSAL-VERSIONS-9DIGIT); 0 error rows everywhere (7560 case rows); r98 Y family passes 4/4 while carrying the 12.999999998.4 lie in got; instruments manifest 16/16 OK; registry coverage PASS 165/165 at 69474c55"}
```
