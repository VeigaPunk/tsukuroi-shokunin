# Round 29 C1 — draft correction markers O09 to O12 (storage-health-r26.json)

State: draft for the L1 to integrate. Targets `corpus/knowledge/storage-health-r26.json` (four new
objects in a new top-level `corrections_r29` array) and, only if S ids are kept in `basis`, two
`used-by` cells of `corpus/SOURCES.md` (S133, S134: old to new given below). Nothing else changes.

Revision the anchors were checked at: `81a061a67466c5e1be812814a895a4b5ed89b4ff` (declaration commit).
Correction prose for all four was checked against `corpus/knowledge/storage-health-r26.md` at that
revision, lines 128 (SH1 names), 129 (SH5 wording), 133 (SH4 scope and action), 135 (SH3, late wave-2
corrections).

## Exact text to insert

The file ends with these two lines (`corpus/knowledge/storage-health-r26.json:324-325`):

```
 ]
}
```

Replace those two lines with the block below (the trailing ` ],` now closes `corrections_r27`; the new
key follows it, same one-object-per-line style at 2-space indent that `corrections_r27` uses):

```
 ],
 "corrections_r29": [
  {"id": "R29-OWED-O09", "row": "SH1", "field": "statement", "withdrawn_text": "under shorter names (write_errs, read_errs, flush_errs, corruption_errs, generation_errs)", "verdict": "corrected", "now": "Only write, read and flush take shorter names in the sysfs view (write_errs against write_io_errs, and likewise for read and flush); corruption_errs and generation_errs read identically in both views, so two of the five claimed shortenings do not exist. The sysfs comment says the five values are printed at once, while the code makes five reads without a lock, so even that snapshot wording is the comment's intent.", "basis": ["corpus/knowledge/storage-health-r26.md:128", "S133 (Linux v7.2 fs/btrfs/sysfs.c devinfo error_stats: shorter names exist for three of the five counters)"]},
  {"id": "R29-OWED-O10", "row": "SH3", "field": "statement", "withdrawn_text": "systemd sets that attribute on journal files by default", "verdict": "corrected", "now": "Since systemd 220 the NOCOW flag comes from the tmpfiles snippet journal-nocow.conf applied to the journal directories, so active journal files inherit it; systemd v262 clears it, or rewrites a file without it, when the file is archived, so a file-level default set by systemd is the wrong mechanism.", "basis": ["corpus/knowledge/storage-health-r26.md:135", "systemd v262 NEWS and src/shared/journal-file-util.c were read in wave 2 and are not registered in corpus/SOURCES.md, so no S id exists for this claim"]},
  {"id": "R29-OWED-O11", "row": "SH4", "field": "statement", "withdrawn_text": "No scrub record exists on this host", "verdict": "qualified", "now": "Narrowed to what was read on 2026-10-22: no scrub status file and no scrub-started or scrub-finished kernel line in the six retained boots. Older scrubs, or scrubs run with recording disabled, cannot be excluded, so the host-wide absence claim is withdrawn to that reading.", "basis": ["corpus/knowledge/storage-health-r26.md:133"]},
  {"id": "R29-OWED-O12", "row": "SH5", "field": "statement", "withdrawn_text": "FAILED! otherwise", "verdict": "qualified", "now": "The overall-health line is printed only after a successful SMART log read: with no -H, a failed Identify Controller or a failed log read, smartctl prints no overall-health line at all, so a non-zero Critical Warning byte yields the failure verdict only when that read succeeded.", "basis": ["corpus/knowledge/storage-health-r26.md:129", "S134 (smartmontools 7.5 nvmeprint.cpp lines 772-778, 786-788, 833-836: no overall-health line without -H or after a failed log read)"]}
 ]
```

The same four objects alone, as a valid JSON array (for a scripted insert), are in
`.ufo/waves/round-29/w1/ScribeMarkersStorage/corrections_r29.json`.

## SOURCES.md used-by changes (needed only because O09 cites S133 and O12 cites S134)

`corpus/SOURCES.md` rows S133 and S134 currently name only the Markdown companion, while the four
JSON rows cite them (`rows[SH1].sources` = S128, S133, S132 and `quotes[3].source` = S133;
`rows[SH5].sources` = S134, S135 and `quotes[0..2].source` = S134). The lane's own convention for a
paired entry lists both files (S120 to S127 name `memory-pressure-r25.md, memory-pressure-r25.json`),
and `tools/check-storage-health.py:651` accepts a cell with both because it tests
`ENTRY_STEM_RE.search(used_by)` rather than equality (line read; the predicate evaluated to True on
both the old and the new cell text). Change cell 11 of each row:

- S133 (`corpus/SOURCES.md:139`): `corpus/knowledge/storage-health-r26.md` to `corpus/knowledge/storage-health-r26.md, corpus/knowledge/storage-health-r26.json`
- S134 (`corpus/SOURCES.md:140`): `corpus/knowledge/storage-health-r26.md` to `corpus/knowledge/storage-health-r26.md, corpus/knowledge/storage-health-r26.json`

If those two cells are not changed, M6 still passes for O09 and O12 on the `md:LINE` reference alone
(the S ids then land in the counter's `unresolved` list and do not fail the item), so the markers do
not depend on this edit. It is proposed because the registry cell is incomplete either way.

## Why each verdict

- O09 `corrected`: `corpus/knowledge/storage-health-r26.md:128` (RevS133) states only write, read and
  flush have shorter sysfs names, and that `corruption_errs` and `generation_errs` are the same in both
  views; the JSON statement claims all five are shortened. S133 is the sysfs source that the line cites.
- O10 `corrected`: `corpus/knowledge/storage-health-r26.md:135` (RevRowSH3) calls the file-level default
  "stale for systemd 262" and gives the tmpfiles snippet `journal-nocow.conf` mechanism plus the archive
  rule. No registered source covers it (the wave-2 read of systemd v262 NEWS and
  `src/shared/journal-file-util.c` was not registered), so the basis cites the note line only; adding an
  `S###` here would be a fabricated provenance claim.
- O11 `qualified`: `corpus/knowledge/storage-health-r26.md:133` (RevRowSH4) narrows the claim to the
  status file and the kernel lines of the six retained boots and excludes older or recording-disabled
  scrubs.
- O12 `qualified`: `corpus/knowledge/storage-health-r26.md:129` (RevRowSH5) makes the failure output
  conditional on a successful SMART log read, citing S134 lines 772-778, 786-788 and 833-836.

## Validation run in the seat sandbox

An unmodified `81a061a` clone at `/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkersStorage/repo` was
patched with the block above and the two used-by cells, and committed there (scratch commit
`b13b1f7b7cdfc11a7bf733b454432aca961439e3`; a parallel commit `6a331d94` carries the markers with the
old used-by cells). Runs of the declared counter, from the clone:

- before, `--revision 81a061a67466c5e1be812814a895a4b5ed89b4ff`: `marked` 0 of 12, unmarked O01 to O12,
  exit 1. (`corpus/knowledge/storage-health-r26.json` has no `corrections_r29` key.)
- with the draft and the used-by cells: `marked` 4 of 12, O09 to O12 all `ok` (`corrected`,
  `corrected`, `qualified`, `qualified`) with `basis.sources` `["S133"]` and `["S134"]` and
  `basis.unresolved` empty; unmarked O01 to O08; exit 1 (the counter exits 0 only at 12 of 12, and this
  draft covers four items).
- with the draft and the old used-by cells (`6a331d94`): O09 and O12 still `ok`, with `S133` and `S134`
  listed under `basis.unresolved`.

The storage-health counter (`tools/check-storage-health.py`) could not be run end to end on the scratch
commit: it binds the revision to a pushed ref and returned `E-REVISION-NOT-PUSHED` (exit 2), and pushing
is outside this seat's bounds. Its JSON parse path was exercised directly instead: the patched entry
loads with the tool's duplicate-key `object_pairs_hook`, `schema` `tsukuroi-storage-health-r26-v1`, six
rows SH1 to SH6 and four `corrections_r29` objects.

## Counter rules checked by construction

- M1: each anchor is a verbatim substring of the named row field (see `evidence.md`; `grep -cF` = 1 for
  each of the four in the JSON).
- M2: exactly one object per id, in a top-level `corrections_r29` array.
- M3: `withdrawn_text` is copied from the frozen `ITEMS` anchors, and the named row and field hold it.
- M4: verdicts are `corrected`, `corrected`, `qualified`, `qualified`.
- M5: each `now` is over 12 words, contains no anchor as a substring, and is unique across items.
- M6: every item cites `corpus/knowledge/storage-health-r26.md:<line>` with a line that exists at the
  revision; S133 and S134 are `mined` and are named by the used-by change above.
- M7: not applicable, O09 to O12 are not in the kernel-mechanism set.

## Limits

- The four `now` texts restate the Markdown corrections; none was re-derived from a fresh source read
  this round (O10's mechanism is a wave-2 read recorded at md:135, not re-opened here).
- `basis` for O11 rests on a live read recorded on 2026-10-22 at md:133, not on a registered source.
- No lane file outside this seat directory was written; the draft was validated in a sandbox clone at
  `/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkersStorage/repo`.
