# ScribeLesson — round 90 w1 report

Seat: ScribeLesson (scribe). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, branch master,
measured at `ce89df93e5f576c5c236d4547299e9ea954e8853` (== HEAD; pre-round tip `c0f91856`, freeze `6511437e`).
No lane file was edited; no `sudo`, no host write, no git/jj mutation in the lane. All runs were made from
`git clone --shared` at `/fast/scratch/hyaku/tsukuroi-r90/ScribeLesson/lane` (HEAD `ce89df93`), then copied here.

## Deliverable

- `.ufo/waves/round-90/w1/ScribeLesson/draft-mistakes.md` — the round-90 lesson `## Mistakes` draft: one row
  (`R89-EMPTY-RUNS-MET`) in the required `class · evidence · captured-by · fix · shown-able-to-fail` shape, plus
  QUALITY 130 as a live proposal.
- `.ufo/waves/round-90/w1/ScribeLesson/receipts/` — `commands.txt` (full transcript), `new-runs0.out/.err`,
  `old-battery-runs0.out/.err`, `old-counter-runs0.out`, `old-counter-runs0.json`.

## What was mined and why

**`R89-EMPTY-RUNS-MET` — an instrument's CLI accepts a degenerate argument that makes the verdict vacuous.**
The r89 counter (`tools/battery-discrimination-r89.py` at `7f3f30b3`) declares `--runs` at `:275` with no floor,
builds zero runs at `:303`, and computes `met` at `:307-308` through `all()` over an empty sequence; `:322` maps
`met` to rc 0. The r89 battery (`tools/limine-pin-battery-r89.py:1112`, `:1128`, `:1135`) has the same shape.
It was filed by wave seat CriticClaims (`.ufo/waves/round-89/w1/CriticClaims.md:104-113`), routed by the r89
spot-check (`corpus/lessons/round-89-verifier-spotcheck.md:127-128`, "count `--runs 0` as void"), and carried in
the r89 lesson only as routed `R89-R1` (`corpus/lessons/round-89.md:81`) — never as a Mistakes row, and no
QUALITY criterion 1-129 captures it (`none`; nearest 114/116/126 cover frozen controls, digest input and control
verdicts, not the counting argument's domain).

The alternative class ("two consecutive rejections from meta-instruments", r88/r89) was rejected as already
captured by QUALITY 126/129 and named in the r90 declaration; mining it would duplicate a rule.

## Shown able to fail (measured)

| State | Command | Observed |
|---|---|---|
| old, r89 battery | extracted `7f3f30b3:tools/limine-pin-battery-r89.py`, `--gate tools/check-limine-pins.py --runs 0` | **rc 0**, stdout empty, stderr empty (vacuous pass) |
| old, r89 counter | extracted `7f3f30b3:tools/battery-discrimination-r89.py`, `--battery tools/limine-pin-battery-r89.py --runs 0 --jobs 2` | **`verdict met`, rc 0**; JSON `"runs": []`, `"verdict": "met"`, `"error_rows": 0` |
| new, r90 | `tools/limine-pin-battery-r90.py --gate tools/check-limine-pins.py --runs 0` | **rc 2**, stdout empty, usage on stderr |

The r90 guard is at `tools/limine-pin-battery-r90.py:1572` (`if not a.gate or a.runs < 1: … return 2`), the usage
line at `:112` declares `--runs N>=1`, and the battery bytes are the frozen digest
`8f0daee82b9d487b5412a45ec1b8cf74c4e037e87d67213f756f1f850fb303e5`
(`.ufo/waves/round-90/before/freeze-manifest.sha256:1`, identical at `6511437e` and `ce89df93`). The extracted r89
battery is the pinned r89 bytes (`3bae11e9…`, matching the r89 spot-check's digest); the extracted counter is
`c666323a…`, matching the frozen r89 counter digest.

## QUALITY 130 draft

`A count that bounds an instrument's evidence is refused before the predicate is evaluated when it empties the
evidence set (R89-EMPTY-RUNS-MET)`: zero/negative CLI counts that empty the run list are a usage error (rc 2, no
verdict line) raised before any fixture or candidate, never `all()` over an empty sequence; the freeze carries one
committed control per refused value. Red = the r89 pair above; green = the r90 guard above. Full house-style text
(red, green, not-116/not-126, shown-able-to-fail, residual) is in `ScribeLesson/draft-mistakes.md`.

## Findings / limits

1. The guard is **measured but not regression-controlled**: the r90 freeze has no control that invokes it
   (`before/controls/run-controls.sh:22` runs only `--runs 3`). The draft routes `K3-runs0-usage` to the next freeze;
   I did not add it (lane files are read-only to this seat).
2. The r89 counter is retired unmodified; `R89-R1` stays routed. The fix lives in the r90 instrument, not in the
   old file — do not read the old counter as repaired.
3. I did not run the 73-family battery, re-score C1, or judge C2: out of scope for this seat, and no pass is claimed.
4. No tool was installed or upgraded; no model was chosen; no subagent was spawned; nothing was committed.

## Verdict

`draft-mistakes.md` written with one mined mistake (`R89-EMPTY-RUNS-MET`, captured-by `none`) and QUALITY 130;
old state fails (rc 0 / `verdict met`) and new state passes (rc 2, no verdict line) on the frozen r90 bytes at
lane `ce89df93`. Residual control gap routed, not fixed.
