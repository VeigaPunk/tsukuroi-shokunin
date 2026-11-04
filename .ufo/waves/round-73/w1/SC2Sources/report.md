status: complete
verdict: pass — drafts complete; the L1 appended S304-S308 verbatim; C1 target revision not yet committed

# SC2Sources — C1 registry, Gate and search-log draft

Seat: L2, tsukuroi lane round 73 (hyaku run 15), wave w1. Leaf member, no subagent dispatch.
Scope: draft text. This seat appended nothing to the lane and committed nothing.

## Produced

| path | content |
|---|---|
| `.ufo/waves/round-73/w1/SC2Sources/rows.md` | rows **S304-S306** (admitted) and **S307-S308** (REJECTED, with flip conditions), each one line, 11 cells, no `|` in a cell, plus the fetch/measurement log and the pre-append census |
| `.ufo/waves/round-73/w1/SC2Sources/gate.md` | the `## Gate` block for `corpus/lessons/round-73.md` and the rule-5 `## Search log` paragraph, with one ≤25-word located quote per new row, supplementary located quotes, admitted/census/ordering notes, two instrument probes and the instrument-replacement record |
| `.ufo/waves/round-73/w1/SC2Sources/report.md` | this report (same body as `w1/SC2Sources.md`) |

Registry state measured before drafting: 303 rows, last id **S303**, `malformed = 0`, duplicate ids none,
tier `A=287 B=5 C=11`, status `mined=272 queued=5 rejected=26`, 90 knowledge `.md` notes. Collision greps
for the five candidate URLs (`man/systemd.unit.xml`, `src/core/unit.c`, `src/shared/install.c`,
`man.archlinux.org/man/systemd.unit`, the Arch package page) each printed `0`.

## Verification I actually ran

```
# snapshots re-verified against the committed checksum file
cd .ufo/waves/round-73/before/src && sha256sum -c SHA256SUMS      -> 3/3 OK
# declared instrument digests, measured at seat start
542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6  tools/count-ul-rows-r73.py
93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e  tools/check-r72-routed-r73.py
# six note quotes independently re-located; counter predicates replicated
UL1 34 words grounding=18/18 located   UL2 35 words 16/17 located   UL3 38 words 16/18 located
UL4 30 words 11/13 located            UL5 28 words 13/16 located   UL6 30 words 9/11  located
# fixture mirror = lane registry + my five drafted rows + the entry note + committed snapshots
python3 tools/count-ul-rows-r73.py --fixture <mirror>
  UL_ROW ok UL1..UL6
  UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
  UL_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1        rc=0
python3 tools/count-ul-rows-r73.py --selftest      -> 11/11 PASS, rc 0   (declared bytes)
# census on the same mirror: rows 308, malformed 0, duplicate ids none,
#   tier A=292 B=5 C=11, status mined=275 queued=5 rejected=28
# every drafted row line: awk -F'|' -> NF=13 for S304, S305, S306, S307, S308
```

`--fixture` proves the drafted rows bind to the note; it does **not** prove a commit.

## Concurrent landing and instrument replacement (observed 23:12-23:15)

The lane changed underneath this seat; recorded because the C1 evidence depends on it.

- **Rows landed.** `corpus/SOURCES.md` now holds S304-S308 at lines 429-433, 308 rows total. Diff of my
  drafted row lines against the landed ones: **identical** (`ROWS_IDENTICAL`). No id, text or anchor
  changed in the append.
- **The note landed is not the entry draft.** `corpus/knowledge/systemd-unit-load-plane-r73.md` now
  carries frontmatter (`source:`, `verified-at:`, `recheck:`), re-measured host readings and six
  restated UL rows. It differs from `w1/L1Entry/note.md` in every row. I re-ran the counter against the
  **landed** note: `UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `met=1`, rc 0 —
  the S304/S305/S306 mapping and every anchor still bind, so the row draft survives the note rewrite.
- **Both instruments were replaced.** At seat start they hashed to the declared digests
  (`542f9c29…`, `93f034e3…`); at 23:15 they read
  `84501ab8d4968293de8b38f68a9f53d658535d90df8191cbd96a20df98e94832` (counter, mtime 23:14:42) and
  `328a6bf60c5237fe4ba857b36d2b4401833a61b933f735ec468139b7531a03fe` (checker, mtime 23:12:19), and
  `git rev-parse HEAD` reads `8eeadcb92ad5362cae155e1903cdf11b52a5ac5d`, not the declaration commit
  `7493713`. I edited neither file. The current counter's `--selftest` reads **12/12 PASS** (the declared
  one had 11 cases, so the suite grew). The old→new digest record and the before-control re-run are the
  L1's obligation under the declaration's frozen rule; my probe outputs below were produced with the
  declared bytes.
- **No target revision yet.** At `--revision HEAD` the current counter prints
  `UL_NOTE absent path=corpus/knowledge/systemd-unit-load-plane-r73.md`, rc 128;
  `git cat-file -e HEAD:corpus/knowledge/systemd-unit-load-plane-r73.md` -> `fatal: … exists on disk, but
  not in 'HEAD'`; `git show HEAD:corpus/SOURCES.md | grep -c '^| S30[4-8] '` -> `0`. Both the note and the
  rows are uncommitted at `8eeadcb9`, so C1 has no measured revision yet.

## Findings

- **F1 anchor binding — held.** Removing `src/core/unit.c` from the S305 `anchor` cell of a fixture
  mirror produced `UL_ROW fail UL3 anchor-not-bound`, `UL_ROW fail UL4 anchor-not-bound`,
  `UL_VERIFIED=4`, `met=0`, rc 1. The anchor cells drafted here are load-bearing.
- **F2 statement grounding — survived.** Replacing a statement with generic systemd vocabulary
  ("The unit file path and service system name are checked in the load directory before the install
  operation completes and the system reads the manager state") while keeping the real located quote read
  `UL_ROW ok UL5 source=S306 snapshot=install.c`, `UL_ROWS=6 UL_VERIFIED=6`, `met=1`, rc 0. On a 140 KB C
  file the 6-token / 50 %-share test is satisfiable without doing the work, so a scripted writer that
  copies located quotes can mint a content-free statement. Recorded as a reach limit of the frozen
  predicate, not repaired (the instrument may not be edited here). The drafted statements are not
  vacuous: grounding 18/18, 16/17, 16/18, 11/13, 13/16, 9/11, and every specific clause was located by
  hand (`install.c:2369`, `:2387`, `:2437-2445`; `unit.c:3874-3876`, `:3905-3911`, `:1439-1451`).
- **F3 the Arch package page is not byte-reproducible.** Two consecutive fetches: `200 101009` both
  times, sha256 `a058f5bd…68be07` then `2cb1b0c2…379727`; `diff` is one hunk `2966c2966`, a per-response
  CSP `nonce`. S308 therefore claims **no** content digest and states the non-reproducibility instead.
- **F4 the rendered man page is markup-different.** Raw tag-free `grep -F` counts: `override files with
  the same name in` -> 1, `lexicographic order, regardless of` -> 2, `contents of this variable overrides
  the unit load path` -> 0 (1 only after tag stripping). The render cannot stand in for the pinned XML
  bytes — the recorded reason for rejecting S307.
- **F5 draft defect, self-caught.** My first write of S308 carried an invented sha256
  ("8a3e1c7b… pending re-read") that I had never measured. Replaced with the two measured digests and
  the CSP-nonce explanation before any yield. Class: `attribution` — a number stated without its command.
- **F6 instrument replacement, recorded not judged.** The two frozen instruments and HEAD changed during
  the round (digests above). This is an event for the L1 and the critic, not a claim by this seat about
  the repair's correctness; the only thing I measured is that the current counter still reads the C1
  target on the landed tree and still passes its own selftest 12/12.

## Overlap and dependencies (for the L1)

- Sibling `w1/L1Sources/gate.md` drafts a Gate/search log with the same 5 identified / 5 screened / 3
  included / 2 excluded counts and the same S307/S308 ids. My `gate.md` adds one required located quote
  per new row with verified line numbers (UL2 spans `systemd.unit.xml:238-239`; the masked branch is
  `unit.c:3874-3876`; the generator refusal is `install.c:348`), the admitted/census tables, the two
  instrument probes and the instrument-replacement record. The ids agree, so either text can be taken
  without renumbering.
- **Commit requirement.** The three admitted rows name
  `corpus/knowledge/systemd-unit-load-plane-r73.md` in `used-by`; the note and the rows must land in one
  commit. At `8eeadcb9` neither is committed and the counter reads `UL_NOTE absent`.
- One rejection satisfies R72-GATE-NO-REJECT; S307 and S308 are both drafted, so the L1 can take either
  (ids stay contiguous as `S304-S307` or `S304-S308`).
- Not done here, by scope: committing, writing `corpus/lessons/round-73.md`, editing the
  `corpus/SOURCES.md` search log, the C2 checker run, and the `--revision` re-run of the final instrument.

## Bounds observed

No `git add/commit/stash/checkout/reset/push`, no `jj` mutation, no unit action, no pacman transaction, no
tool install, no write outside this seat's wave dir and `/fast/scratch/hyaku/tsukuroi-r73/SC2Sources`
(deleted; verified absent), no `agent://all`. The lane-side changes listed above are other seats'.

## Artifact paths

- `.ufo/waves/round-73/w1/SC2Sources/rows.md`
- `.ufo/waves/round-73/w1/SC2Sources/gate.md`
- `.ufo/waves/round-73/w1/SC2Sources/report.md`
- `.ufo/waves/round-73/w1/SC2Sources/SC2Sources.md` (binding file)
- `.ufo/waves/round-73/w1/SC2Sources.md` (this report at the trailer path)
