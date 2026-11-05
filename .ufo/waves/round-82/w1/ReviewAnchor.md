# ReviewAnchor — attack on C1 (depth), round 82

Seat: ReviewAnchor (reviewer). Read-only in the lane; this file is the only lane write.
Own reader: `/fast/scratch/hyaku/tsukuroi-r82/ReviewAnchor/reader.py` (does not import the
lane counter). Its output: `reader2.out` in the same dir (run against the worktree
after-state). Scratch removed before yield.

## Inputs and state observed

- Snapshot `.ufo/waves/round-81/before/src/systemd.mount.xml`: 707 raw lines, sha256
  `afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394` — matches the JSON
  `snapshot_sha256` (reader line 2: `matches JSON snapshot_sha256: True`).
- Tag-stripped per line, the file has 703 lines (reader line 4). The DOCTYPE (raw 2-3) and
  the `<ulink>` (raw 84-85) are the only merges before the MT spans, so the strip offset is a
  constant +2 for every cited span at raw 135 and below (reader lines 6-15).
- **State at review time is not the committed lane tip.** `git status`: `M corpus/knowledge/
  mount-unit-fstab-plane-r81.json`, `M ...r81.md`, `M tools/count-mount-rows-r81.py`,
  `M tools/measure-round81.py`, `M SCORECARD.md` — uncommitted, from ExecAnchor / ExecMutCount /
  ExecMutMeasure / ScribeOrdinal. Worktree JSON sha256
  `9254af96c520d9f44f17f5122fc47b646e777fcd00b28dabacae19199a2ddf4a`. The C1 no-work control
  at `d5b3e134` (`controls.txt`) is still the committed baseline. Nothing below is a claim about
  a committed revision.
- My first reader run printed the pre-candidate numbers, then the JSON changed under it. Those
  first-run outputs were from a reader bug (word index not mapped to line number) and are
  discarded; the reported results come from the fixed reader run against the worktree state
  above.

## Reader output — 8 rows (candidate state in the worktree)

Command: `python3 reader.py` (scratch). Each row: quote occurrences in the strip,
`cited == first occurrence`, and the raw span printed tag-stripped per line.

| row | cited (JSON) | occurrences in strip | cited == located | quote starts/ends on cited first/last | raw span printed |
|---|---|---|---|---|---|
| MT1 | [135,138] | [(135,138)] | yes | yes / yes | 135 "Mount units referring to local file systems automatically gain" … 138 "mount options among nofail, x-systemd.wanted-by=," |
| MT2 | [502,503] | [(502,503)] | yes | yes / yes | 502 "With nofail, this mount will be only wanted, not required, by" / 503 "local-fs.target or remote-fs.target. Moreover, the mount unit is not" |
| MT3 | [486,487] | [(486,487)] | yes | yes / yes | 486 "With noauto, the mount unit will not be added as a dependency for" / 487 "local-fs.target or remote-fs.target. This means that it" |
| MT4 | [491,492] | [(491,492)] | yes | yes / yes | 491 "Note that if x-systemd.automount (see above) is used, neither" / 492 "auto nor noauto have any effect. The matching automount unit will" |
| MT5 | [234,236] | [(234,236)] | yes | yes / yes | 234 "In the created mount unit, configures a" / 235 "Before= or After=" / 236 "dependency on another systemd unit, such as a mount unit." |
| MT6 | [339,341] | [(339,341)] | yes | yes / yes | 339 "Configure how long systemd should wait for a" / 340 "device to show up before giving up on an entry from" / 341 "/etc/fstab. Specify a time in seconds or" |
| MT7 | [198,201] | [(198,201)] | yes | yes / yes | 198 "Configures a Requires= and" / 199 "an After= dependency between the created" / 200 "mount unit and another systemd unit, such as a device or mount" / 201 "unit. The argument should be a unit name, or an absolute path" |
| MT8 | [259,260] | [(259,260)] | yes | yes / yes | 259 "In the created mount unit, configures a WantedBy= or" / 260 "RequiredBy= dependency on another unit. This option may be specified more than once." |

Hazard scan over quotes and cited raw lines: none (`reader2.out:106-107`). No quote contains
`&`, `<`, `>` or `|`; no entity or tag splits inside a cited span.

## Decision-table cross-check (.md vs JSON)

`reader2.out:109-119`: all eight `S331 :N-M` anchors in `corpus/knowledge/mount-unit-fstab-plane-r81.md`
(lines 19-26) match the JSON `lines` exactly. No JSON row missing from the table; no mismatch.
Also: no residual round-81 coordinates remain in the .md body. The only `S331` occurrences in
the .md are the header (line 3), the table, and the new "Coordinate convention" section
(line 30+). The `S332` measured legs (MT2 [136,145], MT5 [69,70], MT6 [124,127]) are unchanged
and remain stripped-file coordinates of the generator capture, which is a different document.

## Ambiguity sweep (falsification attempts)

1. **Ambiguous quote (occurs twice)?** No. Each of the eight quotes has exactly one occurrence
   in the line-preserving strip (`reader2.out`, "occurrences in strip"). The counter's
   `text.find` first-occurrence rule therefore never selects between two candidates. [Scope:
   strip-level. I did not run a separate raw-file-without-strip occurrence count.]
2. **Would a second occurrence change the verdict?** Not applicable: none exists.
3. **Strip-altered characters?** No quote contains entities or `|`. The only tag-adjacent
   content is `x-systemd.*` tokens, which carry no markup. No hazard.
4. **Would a quote shortened to one line still pass? (the question the seat was asked)**
   **Yes — confirmed by fixture.** Scratch fixtures `fx/ctl`, `fx/p1`, `fx/p2`, each run via
   `python3 -B tools/check-anchor-coordinates.py --fixture <dir>`:
   - `ctl` (candidate as-is): `count 8 / target 8 / met`, rc 0.
   - `p1`: MT1 quote replaced by the teaching clause only, `"Before= dependency on local-fs.target
     unless one or more"`, cited `[137,137]`: `count 8 / target 8 / met`, rc 0, MT1 `located [137,137] exact true`.
     The `nofail` / `x-systemd.wanted-by=` / `x-systemd.required-by=` clause the MT1 statement
     asserts is dropped from the quote and the counter does not notice.
   - `p2`: MT2 quote truncated to `"With nofail, this mount will be only wanted, not required, by"`,
     cited `[502,502]`: `count 8 / target 8 / met`, rc 0.
   The predicate tests locate-and-span-equality, not that the quote carries the claim. Shorter,
   less-teaching quotes pass as long as they are a substring on exactly the cited lines.
5. **Does the current MT1 quote already truncate the teaching?** Yes, mildly. The quote stops at
   "among nofail"; the cited line 138 also holds `x-systemd.wanted-by=,` which the statement
   names but the quote does not. The span is still correct because the quote's own extent ends on
   line 138. This is a fidelity gap the counter cannot see, not a coordinate error.
6. **Dead constant.** `WINDOW = 40  # max lines a located quote may span` (`check-anchor-coordinates.py:53`)
   is defined and never used (`grep -n WINDOW` returns only line 53). The docstring implies a span
   cap that does not exist. Minor, but it is a claim the code does not enforce.

## Independent verdict per row

Verdict is on the **worktree candidate**. For the committed state (round-81 numbers) the
counter and I agree on failure too: `controls.txt` shows all eight `cited-range-not-the-quote-span`
at `d5b3e134`, and the JSON diff confirms every old `lines` value differs from the located span by
2-3 lines (e.g. MT1 old `[133,137]` vs located `[135,138]`).

| row | verdict | evidence |
|---|---|---|
| MT1 | agree | cited [135,138] == located, reader2.out:22-23, quote's teaching clause partly absent (see sweep 4-5) |
| MT2 | agree | [502,503] == located, reader2.out:34-35; one-line truncation also passes (p2) |
| MT3 | agree | [486,487] == located, reader2.out:44-45 |
| MT4 | agree | [491,492] == located, reader2.out:54-55 |
| MT5 | agree | [234,236] == located, reader2.out:64-65 |
| MT6 | agree | [339,341] == located, reader2.out:75-76 |
| MT7 | agree | [198,201] == located, reader2.out:86-87 |
| MT8 | agree | [259,260] == located, reader2.out:98-99 |

I disagree with no row. I disagree with the instrument on nothing it measures: its output on
the candidate matches my independent reader on all eight spans. I do disagree that its
predicate is sufficient for the depth C1 claims. The claim is about teaching depth, and the
instrument checks locator correctness only.

## Verdict on whether C1's after-state is a real repair

**Mixed: the coordinate repair is real; the depth repair is not demonstrated.**

- Real: the round-81 defect (cited ranges two lines early, from a stripped-file numbering
  presented as raw) is fixed by renumbering. The quotes already existed in round 81, and the
  new numbers are the raw spans where those same quotes sit (reader2.out:20-103). The .md
  now documents the convention and says so honestly (Coordinate convention section, lines 30-40).
- Not shown: that the rows now carry the teaching. The predicate passes a one-line,
  claim-stripped quote (fixtures p1 and p2). A round that only renumbers passes C1 by
  design, and a shorter quote that drops the nofail/wanted-by clause also passes. The
  depth axis is therefore measured by a counter that can be satisfied without the
  teaching being cited. [INFERENCE] This is the counter-shaped risk: the counter was
  written to catch the round-81 shift, and it does that, but nothing in it ties the quote
  to the MT statement.

## Residual risk and verification gaps

- The candidate is **uncommitted** in the worktree. C1 is not met on any committed revision; the
  L1 must commit it. I did not run `--revision` on a commit (no commit exists).
- Did not verify the `S331` anchors against the installed Arch systemd build (the .md states this
  limit at line ~105); out of C1 scope.
- Did not run the mutation or ordinal instruments (other seats own them).
- `WINDOW` is unused (sweep 6); harmless today, but dead code the docstring describes.

## Tooling

None installed. Read-only: `grep`, `sha256sum`, `git status/diff`, `python3` (stdlib only),
`python3 -B` for the lane counter in fixture mode (no bytecode written).
Scratch dir `/fast/scratch/hyaku/tsukuroi-r82/ReviewAnchor/` removed before yield.
