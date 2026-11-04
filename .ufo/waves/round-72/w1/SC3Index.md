# Round 72 w1 — SC3Index report (index and province drafts)

Host: Linux 7.2.11-arch1-1 (canonical). Lane HEAD `6b426762` (round-72 declaration). Date 2026-11-03.
Scope: four index/province drafts for the modprobe configuration plane plus one registry-row draft.
Drafts only — the L1 is the only writer of the lane tree and the only one who commits. This seat wrote
nothing outside `.ufo/waves/round-72/w1/SC3Index/` and this report.

## Artifacts written

| Path (lane-relative) | sha256 | Holds |
|---|---|---|
| `.ufo/waves/round-72/w1/SC3Index/province.md` | `6bdf9300aeb36239a5473252023333c78f38fd5a40b0e5f6fe7cfe24a66962ae` | PROVINCE round-72 entry: Core now / operator-owned / not claimed, with the counter line |
| `.ufo/waves/round-72/w1/SC3Index/readme-row.md` | `72e97700d6e57e21d3f7c7e01990a93e9e40feb2b893d8559522f8ff83a5db89` | `## Round 72` coverage-map section: note row, counter row, frontier sentence |
| `.ufo/waves/round-72/w1/SC3Index/skill-table.md` | `15e299cbb46c31765d93bbe440364c085d7dbf9f0f82511ae555d65cdb880b7f` | SKILL decision table T1-T7 (7 rows) over the observed modprobe.d shapes |
| `.ufo/waves/round-72/w1/SC3Index/selftest-tally-row.md` | `1bd20ad7c565cd5de7e758290cb01b5255353ed6b5f6be4b8f6d9e536a5c5070` | Replacement `selftest-tally` registry row with `--selftest` in the Self-test column |
| `.ufo/waves/round-72/w1/SC3Index.md` | this file | Report |

## Behavior the drafts assert

- **Province**: Core now is the reading of the kmod configuration surface — SYNOPSIS directory order with
  first-file-of-a-name suppression (MD1), one lexicographic pass with complete/partial replacement (MD2),
  one sorted filename list that rejects a duplicate name (MD3), `/proc/cmdline` parsed after the files
  (MD4), `-n` suppressing execution (MD5), `blacklist` alias-only unless `--use-blacklist` (MD6), grounded
  on the host shape (3 `/etc` names, 5 `/usr/lib` names, `/run` and `/usr/local/lib` absent, `/lib` ->
  `/usr/lib`). Operator-owned: every fragment edit, blacklist change, `MODPROBE_OPTIONS`, module
  load/unload and any `modprobe` run. Not claimed: config-content reading, module internals/RE, blacklist
  refusals, `install`/`softdep`/`weakdep` semantics beyond the manual, `MODPROBE_OPTIONS` measured.
- **README**: one coverage row for `knowledge/modprobe-config-plane-r72.md` naming S301-S303, one row for
  `tools/count-md-rows-r72.py` with its frozen clause set and target, and a frontier sentence that keeps
  the effective per-module configuration, command semantics and blacklist refusals unread.
- **SKILL table**: T1 duplicate name across dirs (MD1, MD3), T2 `/lib` == `/usr/lib` (MD1, MD3),
  T3 install line (MD5), T4 blacklist + real name (MD6), T5 softdep (MD2, MD1), T6 dry-run (MD5),
  T7 cmdline token (MD4). Each row is verdict + operator action; no row authorizes a lane write.
- **Registry row**: the r71 `selftest-tally` row's Self-test cell replaced by `--selftest`, its seven
  named cases and the exit map 0 all pass / 1 a case fails; the core keeps 0/1/2 and the
  no-receipt-line case asserts the core's 2.

## Read-only observations (recorded, not re-verified as claims)

- HEAD is the declaration commit; `git cat-file -p 6b426762:tools/check-selftest-tally.py` hashes to the
  declared base digest `b0f839e3...66c6d`. The working tree carries uncommitted C2/C3 work:
  `tools/check-selftest-tally.py` -> `e47baa781ed4f45c9b5d6fcbc384718ad13db0bc376e9152f0ab98b45e25274d`,
  `SCORECARD.md` +11 lines, `corpus/knowledge/module-parameter-plane-r71.md` +12 lines.
- `corpus/knowledge/modprobe-config-plane-r72.md` exists in the working tree with MD1-MD6; the frozen
  counter's `--revision HEAD` receipt in `.ufo/waves/round-72/w1/SC1Entry/counter-run.txt` reads
  `MD_NOTE absent` rc 128 (that receipt is SC1Entry's; not rerun here). The tree note differs from
  SC1Entry's draft only in MD1's quote sentence (both locate verbatim in the snapshot).
- `tools/count-md-rows-r72.py` hashes to the declared `d615c653...706a6`.
- `tools/check-selftest-tally.py --selftest` was run once with `TMPDIR` in this seat's scratch: seven
  `PASS (SELFTEST-<id>)` lines, `SELFTEST: PASS (7 cases, 7 passed, 0 failed)`, rc 0; the tool removed
  its own temp root (scratch empty afterwards).

## Gates and landing dependencies for the L1

- C1 needs the note committed first; the counter is then run at the measured revision (target
  `MD_ROWS=6 MD_VERIFIED=6 MD_SOURCES=3 MD_SNAPSHOTS=3 MD_MALFORMED=0`, `met=1`). The README/PROVINCE
  drafts assume the note and S301-S303 registry rows land in the same change.
- The SKILL table and the registry row are append-only continuations; the registry row is a new row for
  the same name, so the L1 should place it under this round's registry heading, not rewrite the r71 row.
- The province section carries no `R72-...` promotion id (the declaration names none); the L1 may name
  one when landing.

## Findings (reported, not fixed — outside this seat's write scope)

1. **MD5's printing half is stronger than the snapshot shows.** The tree note's MD5 statement reads "If
   dry_run is set, the install path prints out the command and returns before system executes it...".
   In `modprobe.c` (snapshot): `SHOW` returns early unless `do_show` or `verbose > DEFAULT_VERBOSE`
   (`:150`); `do_show` is set only by `-D` (`:819-822`); `-n` sets only `dry_run` (`:836-838`); the only
   `system()` site is `command_do` (`:297-304`), called only for the remove path (`:463`). The install
   path is executed inside libkmod, which is not in the snapshot set. The no-execution half is grounded
   (remove `:298-299` and `:623-624`; help text `:128`). The drafts therefore state suppression plus
   conditional printing and record the gap; the note's wording is the reviewers'/L1's to correct.
2. `corpus/knowledge/modprobe-config-plane-r72.md` header reads `verified-at: round-72 declaration
   \`6b42676\`` — a 7-hex string, not the 8-hex prefix `6b426762` of the declaration commit.
3. `--selftest`'s fixture parent is `$TMPDIR` with a hardcoded fallback `/fast/scratch/hyaku`
   (`tools/check-selftest-tally.py`, `selftest()`), not `/tmp`; no C2 predicate breach, but a reviewer
   may want the fallback named or refused.
4. The registry row is pinned to the working-tree instrument, not a committed blob; if the landed case
   set changes, the row's case count and summary line move with it (noted inside the row file).

## Out of scope / not done

No lane-tree, registry, note, SCORECARD or tool edits; no git/jj mutation; no `modprobe` execution; no
config-fragment content read; no sibling-lane or `merge/tsukuroi/` read (assimilation closed); no subagent
dispatch; no package/tool install (none needed). Scratch `/fast/scratch/hyaku/tsukuroi-r72/SC3Index`
created and removed.

TABLE_ROWS=7
CITED_IDS=MD1,MD2,MD3,MD4,MD5,MD6,MP5,S301,S302,S303
WRITE_CLAIMS=0
