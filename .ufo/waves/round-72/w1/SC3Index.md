# Round 72 w1 — SC3Index report (index and province drafts)

Host: Linux 7.2.11-arch1-1 (canonical). Lane HEAD `6b426762` (round-72 declaration). Date 2026-11-03.
Scope: four index/province drafts for the modprobe configuration plane plus one registry-row draft.
Drafts only — the L1 is the only writer of the lane tree and the only one who commits. This seat wrote
nothing outside `.ufo/waves/round-72/w1/SC3Index/` and this report.

## Artifacts written

| Path (lane-relative) | sha256 | Holds |
|---|---|---|
| `.ufo/waves/round-72/w1/SC3Index/province.md` | `b9a5a3d74da8005df5ce73591064d900fc84f2a449b80ad5a903a4fcb871e035` | PROVINCE round-72 entry: Core now / operator-owned / not claimed, with the counter line |
| `.ufo/waves/round-72/w1/SC3Index/readme-row.md` | `051f6d13daf96723c69afe766d3636ce1cbd01617f1acc93c9c68cba5a9aedb1` | `## Round 72` coverage-map section: note row, counter row, frontier sentence |
| `.ufo/waves/round-72/w1/SC3Index/skill-table.md` | `15e299cbb46c31765d93bbe440364c085d7dbf9f0f82511ae555d65cdb880b7f` | SKILL decision table T1-T7 (7 rows) over the observed modprobe.d shapes |
| `.ufo/waves/round-72/w1/SC3Index/selftest-tally-row.md` | `ac07480fa323fa1a249ee7692e07c309c24a3fcc73fce150041d3a95bd141607` | Replacement `selftest-tally` registry row with `--selftest` in the Self-test column |
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
- **Registry row**: the r71 `selftest-tally` row's Self-test cell replaced by `--selftest`, its nine
  named cases (eight fixtures plus HERMETIC) and the exit map 0 all pass / 1 a case fails / 2 a
  non-directory `$TMPDIR`; the core keeps 0/1/2 and the NO-RECEIPT case asserts the core's 2.

## Read-only observations (recorded, not re-verified as claims)

- HEAD is the declaration commit; `git cat-file -p 6b426762:tools/check-selftest-tally.py` hashes to the
  declared base digest `b0f839e3...66c6d`. The working tree carries uncommitted C2/C3 work:
  `tools/check-selftest-tally.py` -> `af46203c8ca983841ae5f049e706e5037e416013e72bca03333cbbbfbd5a2abb`
  (it changed twice during the wave: `e47baa78...` with seven cases at 22:38, the current nine-case
  version at 22:42), `SCORECARD.md` +11 lines, `corpus/knowledge/module-parameter-plane-r71.md` +12 lines.
- `corpus/knowledge/modprobe-config-plane-r72.md` exists in the working tree with MD1-MD6; the frozen
  counter's `--revision HEAD` receipt in `.ufo/waves/round-72/w1/SC1Entry/counter-run.txt` reads
  `MD_NOTE absent` rc 128 (that receipt is SC1Entry's; not rerun here). The tree note differs from
  SC1Entry's draft only in MD1's quote sentence (both locate verbatim in the snapshot).
- `tools/count-md-rows-r72.py` hashes to the declared `d615c653...706a6`.
- `tools/check-selftest-tally.py --selftest` was run twice with `TMPDIR` in this seat's scratch: at
  `e47baa78...` it printed seven `PASS (SELFTEST-<id>)` lines (`SELFTEST: PASS (7 cases, 7 passed, 0
  failed)`, rc 0); at `af46203c...` it printed nine (`MATCH`, `MISMATCH`, `LABEL`, `SUPERSEDED`,
  `OUT-OF-SCOPE`, `NO-RECEIPT`, `GREEN-DIFF`, `MIXED`, `HERMETIC`), `SELFTEST: PASS (9 cases, 9 passed, 0
  failed)`, rc 0, and a `TMPDIR=/nonexistent-not-a-dir` run printed `FAIL (SELFTEST-TMPDIR)`,
  `SELFTEST: FAIL (1 cases, 0 passed, 1 failed)`, rc 2. The tool removed its own temp root each time
  (scratch empty afterwards).

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
3. **The C2 instrument moved twice under the wave.** `tools/check-selftest-tally.py` was
   `e47baa78...` with seven cases at 22:38 and `af46203c...` with nine at 22:42; the current version
   honours `$TMPDIR`, falls back to `tempfile.gettempdir()`, refuses a non-directory `TMPDIR` with
   `SELFTEST: FAIL (1 cases, 0 passed, 1 failed)` rc 2, and asserts under-TMPDIR/removal in its HERMETIC
   case. Any registry text must be re-read against the committed blob, not this report; the row's own
   landing note carries the same warning and the observed digest.

## Out of scope / not done

No lane-tree, registry, note, SCORECARD or tool edits; no git/jj mutation; no `modprobe` execution; no
config-fragment content read; no sibling-lane or `merge/tsukuroi/` read (assimilation closed); no subagent
dispatch; no package/tool install (none needed). Scratch `/fast/scratch/hyaku/tsukuroi-r72/SC3Index`
created and removed.

TABLE_ROWS=7
CITED_IDS=MD1,MD2,MD3,MD4,MD5,MD6,MP5,S301,S302,S303
WRITE_CLAIMS=0
