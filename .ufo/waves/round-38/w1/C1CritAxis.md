VERDICT: defect-found

Seat C1CritAxis, item C1-6 (attack C1's axis label). Read-only on the lane; lane HEAD at review
`5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf`; base `8bd001f5`. Receipts in
`.ufo/waves/round-38/w1/C1CritAxis/` (`commands.txt`, `live.out`, `live-nonzero.out`).

## Short answer to the two questions

- **Does a verdict-neutral STORAGE line satisfy the frontier rule?** For the *surface the claim
  names* — "Storage integrity … moves Frontier → Core" (`SCORECARD.md:2117`) — **no**: the rule's
  subject is the area `PROVINCE.md:156-174` defines (three read families), and its parenthetical
  shape (`.ufo/waves/round-26/w1/ScoutHostSurfaces.md:164-167`) is a *verdict-bearing*
  `PLANE storage` with a rollup term. The delivered line reads one family, one view, and votes on
  nothing. For the *narrower* surface the code actually touches ("the census reads the btrfs
  per-device error counters from sysfs") **yes**: verdict-neutrality is not disqualifying — it is
  the exact r35 DRIFT precedent (`SCORECARD.md:1505`, `SKILL.md:3007-3009`), and the Q82 counter
  proves the read is on the production path (`controls-q82.jsonl`, real arm 3/3 vs fixture-gated
  0/3).
- **Is coverage (not operability) the right axis?** **Yes in kind, no in granularity.** A new
  census read of a previously unread host surface is the "frontier → core / a new tool, operation
  or edge class" case named at `.ufo/prompts/tsukuroi-round-38.md:459-461`; the runnable artifact
  and the 10-fixture battery are the *measurement medium*, and labelling by them would be
  "naming the axis by the number it produces" (`:457`). But the row's before/after are exactly
  those counter numbers (`SCORECARD.md:2117`, cells 4-5: `fixtures_matched 0/10` → `10/10`), and
  the axis sentence is unmeasured prose: **no frozen command reads the coverage map.**

## Strongest argument that C1 does NOT move coverage

Coverage is the map, not the tool. `AXES.md:12` defines coverage as "Fraction of the domain's real
surfaces the skill governs … PROVINCE.md lists every surface"; `AXES.md:71-73` names the
frontier→core move as the thing to "claim and measure like any other claim". Four facts, all at
`5edb6c2`:

1. **The map bytes are unchanged from the base.** `git diff --stat 8bd001f5 5edb6c2 --
   PROVINCE.md corpus/README.md` prints nothing (`commands.txt`, first block). `PROVINCE.md:169-170`
   still reads "This area becomes Core only after a census arm exists; until then it is Frontier",
   and `corpus/README.md:243` still reads "Storage integrity is a frontier area, not Core: it
   becomes Core only after a read-only census arm reads it". The only artifact coverage is scored
   from still says Frontier.
2. **The arm reads one of the three families the same paragraph names.** `PROVINCE.md:156-164`
   puts sysfs `error_stats` *and* `btrfs device stats`, the scrub record (`btrfs scrub status`,
   `btrfs-scrub@.timer`) and NVMe SMART (`smartctl -H -A`, `nvme smart-log`) inside the area.
   Executed code at `5edb6c2` touches exactly one: `git show 5edb6c2:tools/tsukuroi-census.sh |
   grep -cE '^[[:space:]]*[^#[:space:]].*(scrub|smartctl|smart-log|nvme|device stats|findmnt)'`
   → **0**; the sole production read is `error_stats` at `tools/tsukuroi-census.sh:1859`, and the
   remaining hits are selftest fixture writers (`:2885-2915`), plus the comment at `:365`
   "NVMe SMART (SH5/SH6) is not read". Even inside SH1 only the sysfs view is read, not the
   `btrfs device stats` query view.
3. **The rule's own designated shape is verdict-bearing, and the line is not.** The frontier
   bullet's parenthetical points at `ScoutHostSurfaces.md:164-167`: "a seventh plane line,
   `PLANE storage: <VERDICT> (<note>)`, emitted between `drivers` and `journal`, with a matching
   term in the `TSUKUROI_CENSUS` rollup" (its alternative, a `storage=[…]` cell on `drivers`, is
   also a verdict). The delivered `STORAGE_LINE` is defined at `:1884-1885` and printed at `:3008`
   and never referenced again; the rollup at `:3010-3019` reduces six terms and no storage term.
   Demonstrated, not inferred: with a scratch sysfs tree carrying `corruption_errs 1`, the census
   prints `STORAGE … state=DEGRADED …` and an unchanged six-term rollup (`live-nonzero.out:11-12`).
4. **The skill text never learns the line, where r35 taught its DRIFT line.** `grep -n STORAGE
   SKILL.md` → no output; the round-38 `SKILL.md` diff is registry rows only. By contrast
   `SKILL.md:3007-3009` is a whole "Round 35 — reading the census `DRIFT pacnew-plane` line (C1)"
   section. A reader of the province cannot discover a governed storage surface.

Therefore the claim's "Surface moved" cell moves an *area* whose six SH rows stay 5/6 unread
(SH3/SH4 scrub, SH5/SH6 SMART/NVMe) while the map, the teaching text and the verdict path are
byte-identical to the base. What moved is a sub-surface: the SH1 sysfs error-counter view gains a
read-only observation. A parenthetical in the declaration ("(btrfs per-device error counters)",
`SCORECARD.md:2117`) cannot narrow the map's definition; only the append-only map can, and this
round did not append to it.

Secondary defect in the same cell: the sizing rule requires a coverage claim to name "the command
that would show it unmoved" (`tsukuroi-round-38.md:459-461`). C1 names no such command — the
frozen counter is the move-detector (0/10 → 10/10), and neither it nor the Q82 counter reads
`PROVINCE.md`/`corpus/README.md` at all (`grep -n 'PROVINCE\|README' tools/score-storage-arm-r38*.py`
→ empty).

## Command that would show the surface unmoved (proposed for the C1 row)

```sh
D=<clone at 5edb6c2>
git -C "$D" diff --stat 8bd001f5 5edb6c2 -- PROVINCE.md corpus/README.md        # no output: class unchanged
git -C "$D" show 5edb6c2:PROVINCE.md | sed -n '169,170p'                        # still "until then it is Frontier"
git -C "$D" show 5edb6c2:tools/tsukuroi-census.sh \
  | grep -cE '^[[:space:]]*[^#[:space:]].*(scrub|smartctl|smart-log|nvme|device stats|findmnt)'   # 0
TSUKUROI_BTRFS_SYSFS=<fixture with corruption_errs 1> bash tools/tsukuroi-census.sh \
  | grep -E '^(STORAGE|TSUKUROI_CENSUS)'                                        # STORAGE DEGRADED, rollup unchanged
```

The first line shows the *area* unmoved; the third shows the two other read families unread; the
fourth shows the read carries no verdict. Run at `5edb6c2` this seat observed exactly those
outputs (`commands.txt`, `live-nonzero.out:11-12`, `live.out:11-12`).

## Identity / vocabulary finding (supporting, same cell)

The neutral line reuses the census's verdict words (`HEALTHY|DEGRADED|BLOCKED`, header
`tools/tsukuroi-census.sh:353`) on a non-plane line. Live it prints
`STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`
(`live.out:11`) while the round-26 rows it rests on still record SH4 "no scrub record exists on
this host (`UNVERIFIED`)" (`corpus/README.md:239`) and the arm's own header says SMART is not read
(`:365`). The proposal it cites is stricter than the delivery: "Without privileged SMART evidence
the arm can never emit HEALTHY" (`ScoutHostSurfaces.md:220-223`). Nothing is
false inside the line's stated scope (`state` is defined from counters only, `:361-363`), but a
consumer that greps `state=HEALTHY` reads an area-wide clean bill. Smallest fix: either a value set
that cannot be confused with a plane verdict (`counters=zero|nonzero|blocked`) or an explicit
`unverified=[scrub,smart]` field in the line.

## Impacted axes

- **coverage** (primary): the move is partial — SH1 sysfs view only; the area stays Frontier by
  its own map's text.
- **calibration**: the declaration's before/after are counter numbers while the axis sentence is
  unmeasured; no command can show the declared surface unmoved.
- **freshness**: `SKILL.md` teaches r35's DRIFT line (`:3007-3009`) and never teaches the STORAGE
  line; the skill's storage section (`:2361`) still routes the reader to the privileged reads the
  arm does not perform.
- **operability** (not harmed): the live census still prints six `PLANE` lines plus one rollup
  (`live.out:2-7,12`), matching the frozen consumer's requirement
  (`tools/score-census-handoff-r32.py:759`: `if len(b['planes']) != 6`).

## Smallest safe correction

Do not touch the counters, the arm, the fixtures or the Q82 conjunct. Change what the claim says
it moved, and land the byte that makes the class change measurable:

1. Rewrite C1's "Surface moved" cell to the sub-surface and add the falsifier command above.
2. Append one partial-graduation paragraph to `PROVINCE.md` (§ "Round-26 frontier — storage
   integrity") and one line to `corpus/README.md`'s round-26 section: the error-counter sysfs
   surface gains a census arm; the area stays Frontier for the `btrfs device stats` view, the
   scrub record (SH3/SH4) and NVMe SMART (SH5/SH6).
3. Add the `SKILL.md` reading section mirroring r35's (`:3007-3009`): what the line means, that it
   is verdict-neutral, and which SH rows it does not read.
4. If the lane wants the *area* Core this round, implement the proposal's remaining inputs and a
   rollup term — that is a new claim, not a relabel; the pre-seat amendment's controls would then
   need a do-nothing for the vote, not only for the line.

## Proposed exact text (replacement for the C1 "Surface moved" cell)

> C1 | coverage | The btrfs per-device error-counter **sysfs view** (SH1, first view) gains a
> read-only, verdict-neutral census line (`STORAGE btrfs-device-stats …`, `corpus/README.md`
> round-26 rule "a read-only census arm reads it"); the storage-integrity **area stays Frontier**
> for the `btrfs device stats` view, the scrub record (SH3/SH4) and NVMe SMART (SH5/SH6)
> (`PROVINCE.md:156-174`), and the round-26 shape (`ScoutHostSurfaces.md:164-167`, a `PLANE
> storage` with a rollup term) is not delivered this round. coverage 9 → 9. The command that shows
> the area unmoved: `git -C "$D" diff --stat 8bd001f5 <REV> -- PROVINCE.md corpus/README.md`
> (empty) plus `git -C "$D" show <REV>:PROVINCE.md | sed -n '169,170p'` (still Frontier).

## What I did not do

- Did not run `tools/score-storage-arm-r38.py` or `-q82.py`, nor the census `--selftest`; those are
  other seats' items and the author receipts/controls already exist. Their results are cited, not
  re-observed, except the Q82 control file's own lines.
- Ran the live census twice (read-only; `tools/tsukuroi-census.sh` no-flags is documented
  read-only, `:364-365,369`) with `TMPDIR` under `/fast/scratch/hyaku/tsukuroi-r38/C1CritAxis`; it
  created no lane file and wrote nothing under `/tmp`.
- No tool installed, no lane file edited, no git state touched; scratch removed.
