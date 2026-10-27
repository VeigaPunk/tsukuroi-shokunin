VERDICT: supports

# C1-8 — kill rules `check-adjacency-anchors PASS->FAIL` and `a census line at or before :3383 moves`

Seat C1ExecAdjacency. Read-only on lane content; all scratch under
`/fast/scratch/hyaku/tsukuroi-r46/C1ExecAdjacency/` (removed at exit). Receipts:
`.ufo/waves/round-46/w1/C1ExecAdjacency/` (`anchors-2042117c.jsonl`, `anchors-a4477049.jsonl`,
`lines.txt`, `pins.txt`, `census-base.sh`, `census-impl.sh`).

Revisions: base `2042117cfb724170772f4c128cc2ddba0b61d817`, implementation
`a44770491eb5ca15ce9f8b3207309d1af683ffaf` (lane tip, `git -C … rev-parse HEAD` = a4477049…).

## (a) check-adjacency-anchors: PASS at both, and the payload is identical

Commands (both revisions already reachable; no push needed):

```
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/run-receipt.py \
  --revision 2042117cfb724170772f4c128cc2ddba0b61d817 \
  --out .ufo/waves/round-46/w1/C1ExecAdjacency/anchors-2042117c.jsonl \
  -- tools/check-adjacency-anchors.py --revision '{rev}'
# same with --revision a44770491eb5ca15ce9f8b3207309d1af683ffaf -> anchors-a4477049.jsonl
```

Observed (both): driver exit `exit_code: 0`; checker row `"status": "PASS"`, `"findings": []`,
and the counts object is **field-for-field identical** between the two receipts:

```
"counts": {"inbound_by_class": {"DRIFTED": 17, "RESOLVES": 96, "UNRESOLVABLE": 1},
           "inbound_by_scope": {"historical": 89, "operative": 25},
           "inbound_classified": 114, "inbound_total": 114,
           "live_object_checked": 10, "live_object_match": 10,
           "outbound_portable": 10, "outbound_total": 10}
```

Machine comparison of the two receipt payloads (`python3` over the two `.jsonl` files): `status equal: True`,
`counts equal: True`, `findings equal: True (len 0)`, `keys differing: ['revision']` — i.e. the IMPL changes add
**zero** new adjacency drift. Kill clause (a) `check-adjacency-anchors.py goes PASS → FAIL`: not tripped.

The registry row that covers the census is the only one:
`corpus/knowledge/adjacency-anchors-r19.json` → `IN-109 tameshi 153 tools/tsukuroi-census.sh [[915, 970]] DRIFTED
operative` (read by `python3` over the registry: `rows naming tsukuroi-census.sh: 1`). Range `915-970` is untouched by
the IMPL diff, and its pre-existing `DRIFTED` class is counted 17 at base and 17 at IMPL, so the diff neither hides nor
adds drift there.

## (b) Census lines at or before :3383: no line moves; three lines are replaced in place

Hunk headers, `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff -U0 BASE IMPL -- tools/tsukuroi-census.sh | grep '^@@'`:

```
@@ -455 +455 @@ VERSION='census-v2'
@@ -594 +594 @@ usage() {
@@ -605 +605 @@ Verdict line: TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED (packages=.. systemd=..
@@ -3383,0 +3384,66 @@ STUB
@@ -3388,0 +3455,38 @@ STUB
@@ -3391 +3495 @@ main() {
@@ -3393,0 +3498 @@ main() {
@@ -3407,0 +3513,8 @@ main() {
```

Four `c` hunks at 455/594/605 are one-for-one (`-455 +455`), so nothing is inserted or deleted at or before 3383.
Byte-level proof over the first 3383 lines of both revisions (`lines.txt`; per-line sha256 over
`git show <rev>:tools/tsukuroi-census.sh`):

```
compared lines: 3383 3383
differing: [455, 594, 605]
line3383 base==impl (blank): True b''
```

Both first-3383 slices are exactly 3383 lines (`wc -l` of `sed -n '1,3383p'` = 3383 in both), so 3380 of 3383 lines
are byte-identical and the boundary line 3383 (blank) is unchanged; the first insertion starts at 3384. Size bookkeeping
closes: base 3485 lines → IMPL 3598 lines, +113 = +66 +38 +1 +8 from the hunks; base `main()` at 3391 is IMPL 3495
(3391+104, 104 = 66+38). Census sha256: base `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc`,
IMPL `d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa`.

The three in-place lines are exactly the replacement pairs the round's own frozen control declares
(`.ufo/waves/round-46/controls/make_c1_variant.py:12-17`: `SELF_OLD/NEW`, `USAGE_OLD/NEW`, `EXIT_OLD/NEW`), and its
docstring states the intended convention verbatim: "*Every edit sits at or after the selftest's last check_cli case
(census :3382 at base) or replaces a line in place (usage :594, :605), so no line at or before :3383 moves (adjacency
anchor IN-109 and sibling pins stay put)*" (`make_c1_variant.py:5-7`). Checked mechanically with those constants:

```
SELF  base==OLD: True | impl==NEW: True | impl!=base: True     (455)
USAGE base==OLD: True | impl==NEW: True | impl!=base: True     (594)
EXIT  base==OLD: True | impl==NEW: True | impl!=base: True     (605)
```

Stronger: rebuilding the declared candidate from the base bytes reproduces the IMPL census **byte-for-byte** —

```
python3 .ufo/waves/round-46/controls/make_c1_variant.py candidate census-base.sh cand-impl.sh
sha256sum cand-impl.sh census-impl.sh   -> d925839c…2cfa both
cmp cand-impl.sh census-impl.sh && echo CANDIDATE_BYTES_IDENTICAL_TO_IMPL=yes   -> CANDIDATE_BYTES_IDENTICAL_TO_IMPL=yes
```

Base → IMPL for the three lines (verbatim, `lines.txt`):

| line | base | impl |
|---|---|---|
| 455 | `SELF=${BASH_SOURCE[0]}` | `SELF=${BASH_SOURCE[0]:-}  # round 46 (C1): empty when the script is read from stdin (--identity: unverifiable)` |
| 594 | `usage: tsukuroi-census.sh [--selftest] [--sample N] [--help]` | `usage: tsukuroi-census.sh [--selftest] [--sample N] [--identity] [--help]` |
| 605 | `Exit map:     0 HEALTHY \| 1 DEGRADED \| 2 BLOCKED (worst plane wins; usage errors also 2)` | same + `; --identity alone prints one TSUKUROI_CENSUS_IDENTITY line naming the executed script bytes, exit 0, no host probe` |

**Reading of "moves", stated explicitly so the L1 can rule.** Positional reading (no line at or before 3383 changes
index; nothing before 3384 is added, deleted or reordered): **holds** — 3380/3383 lines byte-identical, 3383 blank in
both, insertions begin at 3384. Byte-identity reading (any content change at or before 3383): **trips on 455, 594, 605**,
all three being the round's declared in-place usage/`SELF`/exit-map edits. The round's frozen control states the
positional convention, and the three lines carry no adjacency anchor (the only census anchor, IN-109, is `915-970`), so I
report the positional reading as the supported one and flag the strict reading here rather than silently choosing it.

## (c) Sibling pin sweep `tsukuroi-census.sh:<n>`

Command (read-only, tracked files only, every lane repo except tsukuroi):

```
for r in /home/vgpnk/Projects/shokunin/*-shokunin; do git -C $r grep -n -o -I -E 'tsukuroi-census\.sh:[0-9]+(-[0-9]+)?'; done
```

20 repos scanned, **278 pin occurrences** (`pins.txt`), maximum genuine pin **:2659** (mori
`.ufo/waves/round-17/build/OverlapTsukuroi.md:100`; then mado `.ufo/waves/round-24/w1/reports/ConnSiblingOverlap.md:54`
`:2235`, tameshi `.ufo/waves/round-48/a2w1/T48A2ConnFleetFlaky.md:24` `:2175`).

- Pins with n ≥ 3384: **none genuine**. A naive filter returns two, both false positives — the blob-prefix form
  `repo:path:blobhex` in tameshi provenance traces (`tsukuroi-shokunin:tools/tsukuroi-census.sh:084951be`,
  `:165307` at `.ufo/evidence/round-17/coldread/traces/{CR26/05-pin-provenance.json,RR2/15.json}:6`); the digits are
  an abbreviated object name, not a line.
- Pins covering 3383 or 3384: **none**. Pins covering 455: **none**.
- Pins covering 594 / 605: **2, one claim duplicated** —
  `kama-shokunin/.ufo/waves/round-20/build/advice/ConnectTsukuroi.md:8` and
  `kama-shokunin/.ufo/waves/round-20/build/out/ConnectTsukuroi/ConnectTsukuroi.md:8`, both
  "`tools/tsukuroi-census.sh:594-613` runs `pacman -Qkk` on the bounded package sample; `nonroot_artifacts` is counted
  from that output's checksum/permission warnings."
  Content at the pin: base 594 = `usage: tsukuroi-census.sh [--selftest] [--sample N] [--help]`, base 602 =
  `  --sample N   packages plane: size of the pacman -Qkk sample (default 8)`, base 715 = `cap "$PACMAN" -Qkk "${names[@]}"`;
  IMPL 594 = the extended usage line and 605 = the extended exit-map line, so the claim was already imprecise at base
  (the only `-Qkk` token inside 594-613 is the usage sentence at 602, and the actual probe is at 715) and the IMPL edit
  changes two of the thirteen lines the pin covers (`diff` of the two 594-613 slices → `1c1` usage, `12c12` exit map)
  without changing that judgement.
- Fleet root (`/home/vgpnk/Projects/shokunin`, a repo, tracked files) also cites census lines in `MANIFEST.json:25118`
  (`:1855-1901`, `:453`), `.ufo/waves/kaika-w1/tsukuroi-state.md:45` (`:2377-2392`),
  `.ufo/waves/kaika-w3/tsukuroi-critic.md:63` (`:441-446`), `.ufo/waves/shokunin12h-20261014-p4-mori-r1/members/BoundaryRefusal.md:284`
  (`:327,331`) — all < 3383 and none touching 455/594/605, so all resolve identically at base and IMPL.
  `/home/vgpnk/Projects/shokuknow` (read-only) pins only the round-10 defects table (`:473, :281, :434-452, :578, :615,
  :210, :160, :935, :967, :487-493`) — unaffected.

## Pre-existing (not caused by this diff) lane claims on the three changed lines

Reported only so the L1 is not surprised; all three are already stale at **base**, i.e. the IMPL edit neither introduces
nor repairs them:

- `.ufo/waves/round-40/w1/RoutedCensusExit.md:57` — "`rank()` maps an unknown verdict to **9** (`tools/tsukuroi-census.sh:594`)".
  `rank()` is at `:620` at both base and IMPL (unchanged); 594 is the usage line at base too.
- `.ufo/waves/round-43/w2/AdjFinal.md:54` — puts `PRESSURE_FILE=${TSUKUROI_PRESSURE_FILE:-/proc/pressure/memory}` at
  "**`:455`**" at revision `8acf0b02`; at base and IMPL that assignment is at `:483` and 455 is `SELF=…`. The note names its
  own revision, so it is a historical measurement, not a live pin.
- `.ufo/waves/round-45/a2w1/C1ExecFullLarge/base-large-xtrace.{head,trace}:4` — `+rev/base/tools/tsukuroi-census.sh:455: SELF=…`,
  an execution trace of base bytes, not a pointer.

## Not done / limits

- I ran no census selftest and no C1/C2 counter (other seats own those; the census selftest is a 45 s, ~6-CPU run and this
  seat's rule is one at a time). The line-shape / live-exit kill clause is therefore **not** covered by me.
- Sibling sweep is `git grep` over tracked files of `*-shokunin` plus the fleet root and shokuknow; untracked sibling
  scratch files were not swept.
- The interpreter's `diff` on this host rejects GNU `--old-line-format` (`diff: unexpected argument
  '--old-line-format' found`), so the per-line identity proof is a Python sha256 comparison of the two 3383-line slices,
  corroborated by a plain `diff` whose only hunks are `455c455`, `594c594`, `605c605` (`lines.txt`).
- No tool installed or upgraded; nothing mutated in the lane, the fleet repo, any sibling, `/etc`, `/var/lib`, sysfs, units
  or timers. Scratch `/fast/scratch/hyaku/tsukuroi-r46/C1ExecAdjacency/` removed after the receipts were copied into the
  seat directory.
