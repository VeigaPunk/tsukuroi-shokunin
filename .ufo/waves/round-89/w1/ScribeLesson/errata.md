# Draft — round-89 lesson `## Errata` (seat ScribeLesson)

The Errata entry the L1 already wrote (`corpus/lessons/round-89.md:51-58`) is correct in substance; this draft
verifies each pointer it makes and adds one provenance fact it leaves out. Measured at lane
`665408cc45a88ed49717e22f4593e8e6152ac665`; receipt `receipts/m2-evidence.txt` §(f)-(g).

## Verification of the existing entry

| Claim in the entry | Verified how | Result |
|---|---|---|
| the seat measured the CR flake as 2 of 24 | `.ufo/waves/round-88/w1/MutBattery.md:23` "`N-m22-cr-not-stripped` in 2 of 24 runs"; `:113` "measured 2/24 runs"; `:285` "CRLF 2/24 met"; `:226-227` "24 runs … **22 × `37/38 … failed WHITESPACE-CRLF`, 2 × `38/38 met`**" | agree, all four pointers |
| the report and lesson said "1 of 8 runs" | `SCORECARD.md:7451`; `corpus/lessons/round-88.md:115`; fleet `.ufo/reports/round-88/tsukuroi.md:66-67` ("the pristine battery read `met` on `N-m22` in 1 of the seat's 8 runs") | agree, three carriers (the fleet report's wording is "1 of the seat's 8 runs") |
| the analytic 0.4⁴ ≈ 2.6 % stands | `MutBattery.md:225` computes it; `:236` gives the predicate-level form "≈ 1 − 0.9744³ = 7.4% chance of being called `unmet`" | agree |
| the r88 battery let `N-g15-no-cr-strip` escape once in six runs (canonical layout run 3) | `.ufo/waves/round-89/before/controls/receipts-canonical/K1-r88-battery.receipt.txt` run 3 lists `N-g15-no-cr-strip`; `grep -c` over the two layouts = canonical 1, clone 0 | agree, exactly 1 of 6 |

## The fact the entry leaves out (worth one clause)

"1 of 8" is not a miscount: it is the seat's **first batch**, printed verbatim in its own receipt. `MutBattery.md:230`
is the command `--runs 8` and `:231-232` its tally "×7 unmet / ×1 met"; the seat then extended the same probe to 24
runs (`:226-227`) and reported 2 of 24. So the correction is a sampling one — the report cited the 8-run batch, whose
1-of-8 and the 24-run 2-of-24 are the same flake — and the erratum reads most cleanly as: "the seat's first batch was
1 of 8; the figure the report should cite is its 24-run sample, 2 of 24 (`MutBattery.md:226-227`), whose
predicate-level consequence the seat states itself at `:236`".

## One more consequence, not in the entry

Both rounds' arithmetic agree, and the r89 battery closes the instance at `tools/limine-pin-battery-r89.py:351`
(`c.eol = "\r\n"  # r89: every case`) — so a successor may cite 2/24 as the r88 rate *without* carrying the 7.4 %
instability forward. The r89 K1 control still shows the r88 battery escaping once, which is exactly why the r89
battery had to change rather than the counter alone.

## Formatting note

The lane's errata are appended, never rewrites (`PROTOCOL.md` §Evidence standard, cited at
`.ufo/waves/round-37/w1/Audit1Protocol157.md:11`): the superseded text stays at `SCORECARD.md:7451`,
`corpus/lessons/round-88.md:115` and `.ufo/reports/round-88/tsukuroi.md:66-67`, and the erratum names them. This
draft does not ask for edits to those three files.
