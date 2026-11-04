# SC4Index — index / province / skill drafts for the round-71 module-parameter plane

Seat: L2 scribe, round 71 (hyaku run 15), wave w1 — drafts only, no lane-tree write.
Base read: `SCORECARD.md` "Round 71 — declaration" at `0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e`
(`git show 0fcfca31:SCORECARD.md`, read-only). Nothing in this seat is a measurement of the note, the
counter's live run, or the census.

## Behavior

Three draft artifacts, each follow-the-file style, written under `.ufo/waves/round-71/w1/SC4Index/`:

1. `coverage.md` — `## Round 71 — kernel module-parameter plane` plus the coverage map. The primary row
   names `knowledge/module-parameter-plane-r71.md` and S297-S300 and condenses MP1-MP6; a second row names
   `tools/count-mp-rows-r71.py` and its frozen sha256 `fa67d4de…48bc` with the six clause families the
   declaration fixes. Host readings (136 modules / 829 files, `nvidia_drm` 0444 `modeset=Y`, `nvidia_uvm`
   0644, `btrfs read_policy` absent, `/proc/cmdline` token-free, 3+4 modprobe.d files) are attributed to
   `before/host.txt`.
2. `province.md` — `## Round-71 entry — R71-MODPARAM-VIEW`: Core now (the reading, MP1-MP6 in plain
   language), Operator-owned (writing any parameter, modprobe.d edits, load/unload, blacklist changes, with
   an explicit "the lane never …" list), Not claimed (no module internals, no RE — tied to the existing
   `Refuses` line — plus no per-type value vocabulary, absence ≠ unset, a writable mode ≠ an accepted
   store, route attribution only by `/proc/cmdline` token). The `Counted by` line carries `<REV>` as an
   owed placeholder, never a claimed measurement.
3. `skill.md` — `## Module-parameter surface — decision table (round 71)`, 9 rows S1-S9 binding an observed
   `/sys/module/<name>/parameters/<p>` shape (or a kernel-ring/`/proc/cmdline` shape) to a verdict, an
   operator action and the MP id(s) it rests on, preceded by a "no row authorizes a write" boundary
   sentence and followed by three named limits that are deliberately *not* rows.

## Gates / checks I ran (read-only; no product verification)

- `git show 0fcfca31:SCORECARD.md` → the declaration section, including the frozen C1 sentence list.
- `head -6 .ufo/waves/round-71/before/control/battery.txt` → the control line's per-row binding
  `MP1,MP2→S297 params.c | MP3→S298 moduleparam.h | MP4,MP5→S299 main.c | MP6→S300 kernel-parameters.rst`.
  This is the independent confirmation of my id→claim mapping; I did not assume it from prose alone.
- Snapshots read at `before/src/`: `params.c:560-600,600-690,820-835,161-270,270-335`, `main.c:3370-3415,
  3540-3585`, `moduleparam.h:95-130`, `kernel-parameters.rst:14-40`.
- `sha256sum tools/count-mp-rows-r71.py` → `fa67d4deb5f01a5124120276a8571fa36c7367d9db711ceb39bc1ca6fded48bc`,
  equal to the declared freeze.
- Scratch audit `/fast/scratch/hyaku/tsukuroi-r71/SC4Index/audit.py` over the three drafts:
  `SKILL_TABLE_ROWS=9`, all rows 5 cells (no stray pipe in a cell), `ROWS_WITHOUT_ID=[]`,
  `CITED_IDS=MP1,MP2,MP3,MP4,MP5,MP6`, `WRITE_SYNTAX_HITS=0` (no `echo -n`, no `> /sys/`, no `> /proc/`),
  `STALE_CASE_TALLIES=0` (no selftest figure anywhere — the D1 defect class is avoided, not repeated).
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain` was not needed for writes: I
  wrote only the four paths named in this seat. No git/jj mutation, no lane-tree file.

## Touched surfaces

Only `.ufo/waves/round-71/w1/SC4Index/{coverage.md,province.md,skill.md}` and this report
`.ufo/waves/round-71/w1/SC4Index.md`. No product code, no registry, no counter, no scratch left behind.

## Findings (for the L1 / note author)

1. **Note absent at my run time.** `corpus/knowledge/module-parameter-plane-r71.md` did not exist when this
   seat ran, so every note/row/S-id reference in the drafts is forward-looking and must land in one commit
   with S297-S300. My row ids follow the declaration's clause order and the battery control's snapshot
   binding; if SC1Entry reorders rows, the `Rests on` column must be re-mapped, not re-worded.
2. **S7 is grounded depth the six rows do not state.** `parse_args` records `ERR_PTR(ret)` on a rejected
   value and `load_module` takes the `coming_cleanup` path (`main.c:3561-3567`), so a *known* parameter with
   an invalid value fails the load, while an unknown one (MP4) does not. Unless SC1Entry says otherwise, this
   stays a table row resting on MP3 with MP4 as contrast — an operator-facing distinction the note may want
   to add in its own words (I do not amend the frozen predicate).
3. **S5 is the same class.** `param_attr_show` returns `-EPERM` when `ops->get` is NULL (`params.c:563-573`),
   so a visible `0444` file can refuse every read. Kept as a row resting on MP3 (get optional), with the
   `param_check_unsafe` `-EPERM` path (`params.c:587-598`) named in the limits instead, because MP1-MP6 do
   not describe it.
4. **README's coverage map is three columns** (`| Note | Holds | Sources |`), not two; I followed the file's
   actual shape under the heading the seat spec fixed. The note path in that cell is `corpus/`-relative, as
   every existing row is.
5. **No selftest or census figure appears in any draft**, so this seat contributes nothing to the D1 stale
   tally class; the province `Counted by` line names a tool and a placeholder, not a number.

## Known limits

These are proposals, not measurements: I did not run the frozen counter against a note, did not run the
census selftest, and did not fetch or re-verify the four snapshots (S1Scout's item). The table's operator
actions are read-only by construction; nothing here grants a write, a load, a blacklist change or a
modprobe.d edit.

## Artifact paths

- `.ufo/waves/round-71/w1/SC4Index/coverage.md`
- `.ufo/waves/round-71/w1/SC4Index/province.md`
- `.ufo/waves/round-71/w1/SC4Index/skill.md`
- `.ufo/waves/round-71/w1/SC4Index.md` (this report)

KEY=VALUE: TABLE_ROWS=9, CITED_IDS=MP1,MP2,MP3,MP4,MP5,MP6, WRITE_CLAIMS=0
