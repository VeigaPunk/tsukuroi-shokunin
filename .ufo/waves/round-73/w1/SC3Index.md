# Round 73 w1 — SC3Index report (index and province drafts)

Host: Linux 7.2.11-arch1-1 (canonical), systemd 262 (262.1-1-arch). Lane HEAD at first read
`8eeadcb92ad5362cae155e1903cdf11b52a5ac5d` — **not** the round-73 declaration commit `7493713`; the tree
also carried uncommitted C1/C2 work (note untracked, `corpus/SOURCES.md` with S304-S306, both instruments
` M`). Date 2026-11-03.

Scope: four index/doc drafts for the systemd unit-load merge plane plus two registry continuation rows,
written as text for the L1. No lane-tree, note, registry, SCORECARD or tool edit; no git/jj mutation; no
unit action; no subagent dispatch. This seat wrote only `.ufo/waves/round-73/w1/SC3Index/` and this report.
Scratch `/fast/scratch/hyaku/tsukuroi-r73/SC3Index` created, used and removed.

## Artifacts written

| Path (lane-relative) | sha256 | Holds |
|---|---|---|
| `.ufo/waves/round-73/w1/SC3Index/deltas.md` | `ae5ec446c07fb8f0e8a86818a6c47f95c7674a5810a1f4fdab380921fff35c45` | All four drafts in labelled fenced blocks, the selector/placement rules, the landing checklist (§E) and the findings (§F) |
| `.ufo/waves/round-73/w1/SC3Index/skill-decision-table.md` | `982f1b31928956ad363366d328e2d4c5089f9dba85b0b5514bacb19f7dfb4b1c` | `## Round 73 — the systemd unit-load merge plane (decision table)`: six symptoms T1-T6, mechanism + rule row + read-only check, named limits |
| `.ufo/waves/round-73/w1/SC3Index/skill-registry-rows.md` | `a683ef1696edf46d1ce5bd751ad3c615ef47ee36d433c9fc549f6f5371624468` | `## Round 73 — … registry row continuation (append-only)` with two single-header tables: `count-ul-rows-r73` and `check-r72-routed-r73` |
| `.ufo/waves/round-73/w1/SC3Index/province.md` | `1f10b4520f4f05b93eaa8aa86fd1fd7d14473f447953f32f05fd40b9ba58612c` | `## Round-73 entry — R73-UNIT-LOAD-VIEW`: Core now (reading + repair table) / Still Frontier / Operator-owned / Mori's / counter line |
| `.ufo/waves/round-73/w1/SC3Index/readme.md` | `a07b7f7bf889088d14c93cd1452874ff7725541eb5b544448a0841084f962177` | `## Round 73 — systemd unit-load merge plane (C1), the three routed repairs (C2)`: coverage rows (note, S304-S306, counter, SKILL, PROVINCE) and the frontier sentence |
| `.ufo/waves/round-73/w1/SC3Index/SC3Index.md` | binding file (`status: complete`, verdict sentence) | — |
| `.ufo/waves/round-73/w1/SC3Index.md` | this file | Report |

Every fenced block in `deltas.md` was re-extracted programmatically into the per-target files, so the
digests above are the exact bytes the L1 would paste; a pipe-count check over every table in the four
drafts reports no inconsistent row (headers and body rows agree in every table).

## Behavior the drafts assert

- **Decision table (A, six rows, as assigned).** T1 ignored drop-in -> a drop-in of the same basename is
  read from the highest-precedence directory (`/etc` over `/run` over `/usr/lib`), different names merge in
  one lexicographic pass parsed after the unit file, and drop-ins outrank the unit file wherever located
  (UL2, UL1 for the fragment under the set); if the file is already in the manager's set the cause is T3,
  not precedence. T2 override lost on update -> a drop-in outranks the **whole unit file** including an
  `/etc` unit-file copy, so copying the unit file does not displace a vendor drop-in and the durable copy is
  a same-named `/etc` drop-in (UL2). T3 changed-on-disk -> drop-in list differs or a drop-in is newer,
  masked drop-ins omitted (UL3), check `NeedDaemonReload`. T4 masked -> empty fragment or `/dev/null`
  symlink while the fragment path is null or empty, `LoadState=masked` (UL4, UL5), host `passim.service`.
  T5 masked-but-enabled -> `is-enabled` reports `masked` (rc 1), `UnitFileState` and `LoadState` both
  `masked`, and the `enabled` word is the **PRESET** column of `list-unit-files` (UL4, UL5 + host reading).
  T6 instance without a file -> template fragment resolution and instance-then-template drop-in lookup
  (host H4/H5; documented in the S304 paragraph but no UL row states it, and the row says so). No row
  authorizes a unit action; every row names a read-only check.
- **Registry rows (B).** `count-ul-rows-r73` as a gate: entry `--revision <REV>` (or `--fixture <DIR>`),
  map 0 met / 1 missed incl. `UL_MAP malformed` / 2 `$TMPDIR` unusable or `/tmp` under `--selftest` /
  3 self-test failed / 128 note-registry-map absent, **twelve** self-test cases with their tokens, the full
  frozen clause set in Pinned values, write scope `$TMPDIR` only. `check-r72-routed-r73` as a gate:
  0 clean / 1 stale with the eight `reason=` tokens / 2 only under `--selftest` / 3 self-test failed,
  **eleven** cases in the current construction (`93f034e3…` had five), and a pinned-values cell that
  requires the digest to be re-read from the committed blob because wave 1 moved the file. The section
  explicitly refuses to create a `## Gate and probe registry — round73 superseding current rows` heading:
  under the operative selector that would become the table and drop every carried row, so the r71 table
  stays operative with a continuation section (the round-72 precedent).
- **Province (C).** Core now = the documented load path, drop-in merge and precedence, reload freshness
  rule, both mask forms and the `masked`/`masked-runtime` split, the alias parse; plus the six-symptom
  repair table. Still Frontier = the effective merged value of a named unit on this host, host-build line
  numbers, the instance-only directory leg, `SYSTEMD_UNIT_PATH`'s replacement leg, masks outside
  `/etc/systemd/system`, the alias host blank, and `.wants` survival behind a mask. Operator-owned = mask,
  unmask, enable, disable, edit, `daemon-reload`, start, stop. Mori's unchanged.
- **README (D).** Round-73 section with the note row (UL1-UL6 in one cell), the S304-S306 row naming the
  counter's binding condition (v262 raw URL in the source cell, snapshot basename in the anchor cell), the
  counter row with its frozen clause set and digest discipline, a SKILL pointer and a PROVINCE pointer, then
  the frontier sentence. Notes 90 -> 91 and registry 303 -> 306 are stated as the declaration states them.

## Read-only observations (recorded, not re-verified as claims)

- **C1 counter.** Declaration digest `542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6`
  (409 lines). `--selftest` then printed eleven `PASS (SELFTEST-<ID>)` lines (CONTROL, SHORT, UNREGISTERED,
  QUOTE, FIVE, DUPID, REUSE, UNGROUNDED, MALFORMED, DIGEST, OWNWORK), `SELFTEST: PASS (11 cases, 11 passed,
  0 failed)`, rc 0. Later in the wave the file moved to
  `84501ab8d4968293de8b38f68a9f53d658535d90df8191cbd96a20df98e94832` (423 lines) with a twelfth case
  `EMPTYQUOTE` (`quote-words`): `SELFTEST: PASS (12 cases, 12 passed, 0 failed)`, rc 0.
- **The wave-1 note draft** (`.ufo/waves/round-73/w1/L1Entry/note.md`) copied into a private fixture tree
  with three registry rows shaped as the counter requires (source cell = v262 raw URL, anchor cell =
  snapshot basename, kinds `docs`/`code`/`code`) scored, on the declaration counter,
  `UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `UL_TARGET … met=1`, rc 0. With the
  hardened counter, `--fixture` over the **lane working tree** (note + the landed S304-S306 + snapshots)
  printed six `UL_ROW ok` lines, the same five counters and `met=1`, rc 0. Both are working-tree reads, not
  the after receipt. `--fixture` over a tree without the note prints `UL_NOTE absent` rc 128.
- **C2 checker.** At `93f034e3…` (202 lines, the declaration instrument) `--selftest` printed five `PASS`
  lines (CONTROL, LESSON, DIGEST, CAPABILITY, UNANCHORED), rc 0, and `--revision HEAD` printed
  `LESSON-STALE … missing_tokens=2`, `DIGEST-STALE … missing_tokens=1`, `CAPABILITY-STALE …
  missing_tokens=0`, `ROUTED_STALE=3 ROUTED_OK=0/3`, rc 1 — the declared before control, reproduced.
  The file then moved to `316dd51a…` (267 lines) and `328a6bf6…` (279 lines, eleven cases, PASS 11/11).
- **Host re-measurements (read-only, no mutation).** `systemd-analyze unit-paths` -> 12 lines in the
  committed order; `systemctl list-unit-files --state=masked` -> header `UNIT FILE  STATE  PRESET` and rows
  `passim.service masked disabled`, `systemd-networkd-wait-online.service masked enabled`;
  `systemctl show -p UnitFileState -p LoadState` -> `masked`/`masked` for both units;
  `systemctl is-enabled systemd-networkd-wait-online.service` -> `masked`, rc 1;
  `systemctl show -p NeedDaemonReload -p DropInPaths user@1000.service` -> `NeedDaemonReload=no` plus the
  two template-directory drop-ins; `systemctl show -p FragmentPath -p DropInPaths getty@tty1.service` ->
  `/usr/lib/systemd/system/getty@.service` with `DropInPaths=` empty; `/etc/systemd/system/*.d` is 3 dirs,
  `/usr/lib/systemd/system/*.d` is 12, `user@.service.d` exists in both and `user@1000.service.d` in
  neither.

## Findings (reported, not fixed — the instruments are frozen and outside this seat's write scope)

1. **Both instruments moved inside wave 1.** C2 checker: `93f034e3…` (202 lines, five cases, PASS 5/5) ->
   `316dd51a…` (267 lines, eleven cases, `FAIL (SELFTEST-CONTROL) rc=1 expect=0`,
   `SELFTEST: FAIL (11 cases, 10 passed, 1 failed)`, rc 3) -> `328a6bf6…` (279 lines, eleven cases, PASS
   11/11). A byte copy of the then-current file, patched only to print the failing buffer, passed 11/11, so
   the CONTROL failure is a recorded transient output rather than a reproduced suite defect; what is proved
   is that seats read a file being rewritten and that the declaration digest no longer describes it. C1
   counter: `542f9c…` (409 lines, eleven cases) -> `84501ab8…` (423 lines, twelve cases). Both files carry
   ` M`. Under the round's frozen instrument-change rule this forces an appended erratum with old->new
   digests and a same-instrument before-control re-run; draft B therefore pins each construction and
   requires the digest to be re-read from the committed blob.
2. **`check-r72-routed-r73`'s documented exit 2 is unreachable outside `--selftest`.** The header says
   "2 cannot evaluate (a required file is absent, or no readable input)" but `evaluate()` returns only 0 or
   1: a `--root` tree with only the lesson file prints `DIGEST-STALE absent path=SCORECARD.md` and rc 1.
   True for the 202-line and the 279-line versions. Draft B states the observed map.
3. **The wave-1 note draft's H3 host value is wrong.** It says `systemd-networkd-wait-online.service` reads
   `UnitFileState=enabled` beside the mask; measured `UnitFileState=masked`, `is-enabled` prints `masked`
   rc 1, and the `enabled` token is the PRESET column of `list-unit-files`. Draft A's T5 states the
   corrected mechanism; the note's H3 must be corrected before the C1 commit (committed `before/host.txt`
   is consistent with the correction — it records the row verbatim and `UnitFileState=masked`).
4. **`count-ul-rows-r73`'s header omits its 128 code** (the `UL_NOTE`/`UL_REGISTRY`/`UL_MAP` absent code the
   declaration's do-nothing control relies on). Documentation gap; draft B states 128.

Held on the same draft note: the H1 order claim, the H2 mask list, the H4 two-drop-in `DropInPaths`, and the
H5 template resolution all reproduce this seat.

## Gates and landing dependencies for the L1

- C1 needs the note at `corpus/knowledge/systemd-unit-load-plane-r73.md`, **S304-S306** in
  `corpus/SOURCES.md` (source cell carries the v262 raw URL, anchor cell the snapshot basename, kind
  `docs`/`code`/`code`, never `own-work`), and the six rows in the seven-pipe shape with 2+2+2 snapshot
  reuse; then `python3 tools/count-ul-rows-r73.py --revision <REV>` must read the frozen target with
  `met=1`. At this seat's last read the working tree already satisfies that (`met=1` over the tree), but
  the measurement must be at a committed revision and with the committed instrument.
- The registry rows are an append-only continuation section; the r71 table must remain the operative one.
- Draft A, C and D are independent of the tool drift; draft B's digest cells must be re-read against the
  committed blobs, and if the hardened instruments land, their erratum and same-instrument before-control
  re-run are what make the before/after pair citable.
- The note's H3 line needs the correction in Finding 3 before the C1 commit.

## Out of scope / not done

No lane-tree, note, SOURCES, SCORECARD, lesson or tool edit; no commit, add, stash, checkout, reset, push;
no unit action (no mask, unmask, enable, disable, edit, daemon-reload, start, stop); no sibling-lane read;
no MCP or config change; no subagent dispatch; no package/tool install (none needed). Scratch
`/fast/scratch/hyaku/tsukuroi-r73/SC3Index` removed; the only diagnostic copy of the checker lived there
and is gone.

TABLE_ROWS=6
CITED_IDS=UL1,UL2,UL3,UL4,UL5,UL6,S304,S305,S306
WRITE_CLAIMS=0
