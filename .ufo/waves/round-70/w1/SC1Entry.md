# SC1Entry — C1 knowledge entry draft XS1-XS6 (round 70, w1)

## Behavior

Drafted `corpus/knowledge/xfs-storage-plane-r70.md` as a six-row C1 entry with the frozen grammar:
`| XS<n> | <statement ≥ 12 words> | source=S### | snapshot=<file> | digest=<64 hex> | quote="<verbatim ≤ 25 words>" |`,
one physical line each, exactly 7 pipes per row, no pipe in any cell, no double quote inside any
quote cell. Rows cover XS1/XS2 `xfs_stats.c` (group-line format with `counter_val` per-CPU u32
summation; four extra-precision lines with `%llu`/`%u` widths), XS3/XS4 `xfs_sysfs.c` (`stats` RO +
`stats_clear` WO rejecting any value but 1 before `xfs_stats_clearall`; four `log/` files with LSN
`cycle:block` and grant heads in bytes), XS5 `xfs.rst` (`/sys/fs/xfs/<dev>/error/<class>/<error>/`
with the single `metadata` class), XS6 `health.c` (`health_f`'s not-collected message and the
`xfs_scrub(8)` advice). Prose below the table: Scope (storage-integrity frontier, second NVMe
device, S128-S139 already hold btrfs/NVMe, no write authorized), six `Host reading.` paragraphs from
`before/host.txt` (34-line stats files, 0200 `stats_clear`, log value shapes, 7 error regular files
per fs, health not collected), Limits (QUALITY 103 tag-vs-host-build line caveat, counters are not
health grades, no unprivileged scrub state, `stats_clear` never written), and the provenance trio
naming S290-S293 plus the capture. Provenance trio placed first per `CORPUS.md` §163 (the contract
requires it to open the entry), not last.

## Gates

- Source reading: all statements/quotes built from the committed snapshots only; snapshot sha256
  recomputed and equal to `before/src/SHA256SUMS` and `SOURCES.json`
  (xfs.rst `53bda67b…d051c`, xfs_stats.c `4b6a9b6c…9e452`, xfs_sysfs.c `1cbcffa1…a5805`,
  health.c `84fdd0be…15950`).
- Frozen counter run on a fixture mirror (`$S/fx` = byte-copy of `before/src` + draft at
  `corpus/knowledge/xfs-storage-plane-r70.md` + `corpus/SOURCES.md` taken from SC2Sources' draft rows
  S290-S293, so the source-to-snapshot binding was exercised against the real admitted rows):

```
XS_ROW ok XS1 source=S291 snapshot=xfs_stats.c
XS_ROW ok XS2 source=S291 snapshot=xfs_stats.c
XS_ROW ok XS3 source=S292 snapshot=xfs_sysfs.c
XS_ROW ok XS4 source=S292 snapshot=xfs_sysfs.c
XS_ROW ok XS5 source=S290 snapshot=xfs.rst
XS_ROW ok XS6 source=S293 snapshot=health.c
XS_ROWS=6 XS_VERIFIED=6 XS_SOURCES=4 XS_SNAPSHOTS=4
XS_TARGET rows=6 verified=6 sources>=4 snapshots>=4 met=1
rc 0
```

- Draft shape re-checked post-write: 6 lines starting `| XS`, each 7 pipes, 6 total `| XS`
  occurrences (no stray row-like prose), quotes located verbatim whitespace-normalized.

## Touched surfaces (writes)

- `.ufo/waves/round-70/w1/SC1Entry-note.md` (the draft; not the landing path).
- `.ufo/waves/round-70/w1/SC1Entry.md` (this report).
- Scratch `/fast/scratch/hyaku/tsukuroi-r70/SC1Entry` (fixture only; deleted before yield).
- Nothing else: `corpus/`, `tools/`, the lane git tree, `.ufo/state`, other waves and sibling lanes
  were not written. No git/jj mutation; no `pacman`; no `sudo`; no tool installs.

## Out of scope

- Landing the note at `corpus/knowledge/xfs-storage-plane-r70.md` (L1 only) and editing
  `corpus/SOURCES.md` (SC2Sources draft; L1 lands).
- C2 census arm, census selftest, mutation battery, host re-measurement, registry rejected rows.
- Machine-readable JSON companion (r26 pattern) is not part of the C1 predicate; not drafted.

## Findings

- `health.c` landed after the declaration commit (lane commit `84e013a7`); its committed digest still
  matches `SOURCES.json` and `S-293`, so the row binds. All four snapshot files are present in
  `before/src` with four SHA256SUMS lines.
- Statement grounding is the fragile clause, not word count: each statement reuses identifiers that
  appear literally in its own snapshot (`xfs_stats_format`, `counter_val`, `per_cpu_ptr`,
  `stats_clear_store`, `xfs_stats_clearall`, `log_head_lsn`, `reserve_grant_head_bytes`,
  `xfs_log_ktype`, `metadata`, `xfs_scrub`, `collected`), giving 5-11 hits per row against the
  required 3.
- Host capture confirms shape only: 30 group lines + 4 precision lines = 34; error tree 7 regular
  files per filesystem; no scrub record exists, so health output is absence of a record, not a
  healthy verdict.
- QUALITY 103 is stated explicitly in Limits: upstream tag anchors are not host-build line numbers;
  host runs `linux 7.2.11.arch1-1` / `xfsprogs 7.2.0-1`.

## Artifacts

- Draft: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-70/w1/SC1Entry-note.md`
- Report: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-70/w1/SC1Entry.md`
- Capture: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-70/before/host.txt`
- Snapshots: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-70/before/src/`

ROWS=6
DRAFT_SHA256=6c98db20568d984c927ce94b96a2310b8162d5c476f4b0ae4844fd1993319a36
COUNTER_OUT=XS_ROWS=6 XS_VERIFIED=6 XS_SOURCES=4 XS_SNAPSHOTS=4 met=1
COUNTER_RC=0
SCRATCH_DELETED=1
