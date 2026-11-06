# ExecLints — round 87 w1: lane conformance lints at the current tip

Seat: executor (leaf). Axis: operability. All runs read-only, in a `git clone --shared` of the lane;
nothing in the lane, `/boot`, `/efi`, `/sys`, `/proc` was written, no `sudo`, no objcopy/strip/sbsign/
ukify/mkinitcpio/limine*/bootctl/efibootmgr/pacman was run. No tool was installed or upgraded.

Lane revision measured: `cefb4188b484329c4908a19a277f8fb120fb4f56` (`git -C …/tsukuroi-shokunin rev-parse master`).
Clone: `/fast/scratch/hyaku/tsukuroi-r87/ExecLints/lane` (removed at exit). Receipts:
`.ufo/waves/round-87/w1/ExecLints/receipts/` (01-10, verbatim stdout + `RC=`).

## Verdicts

| # | Check | Command (cwd = the clone) | Verdict | rc |
|---|---|---|---|---|
| 1a | registry coverage, literal dispatch form | `python3 tools/check-registry-coverage.py --revision master` | CANNOT_EVALUATE — `E-REVISION-INVALID` "7-64 hex commit required" | 2 |
| 1b | registry coverage, documented form | `python3 tools/check-registry-coverage.py --revision cefb4188…` | **FAIL** — 136 registered / 138 tools, 2 `REGISTRY-ROW-MISSING` | 1 |
| 2a | knowledge header, literal dispatch form | `python3 tools/check-knowledge-header.py --revision master` | CANNOT_EVALUATE — `E-REVISION-INVALID` | 2 |
| 2b | knowledge header, documented form | `python3 tools/check-knowledge-header.py --revision cefb4188…` | **PASS** — 103/103 notes clean, 0 findings | 0 |
| 2c | entry header of `corpus/knowledge/limine-pin-plane-r87.md` | same run, note extract | **PASS** — `problems: []`, keys at lines 3/4/5 | 0 |
| 3 | census selftest | `bash tools/tsukuroi-census.sh --selftest` | **PASS** — `TSUKUROI_CENSUS_SELFTEST: PASS (218 cases, 218 passed, 0 failed)` | 0 |
| 4 | fleet sources census | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | **clean** — 52 `W04` warnings, no `E`-codes, `ok` for the lane registry | 0 |
| 5 | drafted registry rows (fixture only) | `python3 tools/check-registry-coverage.py --revision 4d11e4cd… --branch fixture-rows` | **PASS** — 138/138 registered, 0 findings | 0 |
| 6 | supplementary: recheck commands | `python3 tools/check-recheck-commands.py --revision cefb4188…` | FAIL — 3 findings, all pre-existing at `220c86e3…` | 1 |

`--revision master` (the literal command in the dispatch) is refused by design, not a defect:
`tools/_revision.py:1-30` fixes the contract as "revision is 7-64 hex … else E-REVISION-INVALID", and
both tools import that binding. The documented CLI is a hex commit; 1b/2b are the same checks at the
same tip. No patch proposed — the dispatch line, not the tool, was wrong.

## 1. Registry coverage — the two new tools have no operative row

Verbatim (`receipts/01-registry-coverage.txt`):

```
$ python3 tools/check-registry-coverage.py --revision cefb4188b484329c4908a19a277f8fb120fb4f56
{"branch":"master","branch_tip":"cefb4188b484329c4908a19a277f8fb120fb4f56","counts":{"findings":2,"missing":2,"registered":136,"rows_total":136,"tools_total":138},"findings":[{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/check-limine-pins.py"},{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/limine-pin-battery-r87.py"}],"revision":"cefb4188b484329c4908a19a277f8fb120fb4f56","status":"FAIL"}
RC=1
```

Both round-87 tools lack a SKILL.md registry row. Drafted rows (verbatim, 8-column format copied from
the `resume-gate-battery-r86` and `hibernate-resume` rows) and the insertion point are in
`.ufo/waves/round-87/w1/ExecLints/registry-rows.md`.

Insertion point: `SKILL.md:5922` (`| nonauthor-label | gate | …`), **before** the blank line at
`SKILL.md:5923`. The operative table is the `## Gate and probe registry — round71 superseding current
rows` section at `SKILL.md:5777`; `_operative_rows` selects the highest-numbered matching heading and
stops the table at the first blank line. Two traps, both measured:

- rows appended after the blank line are invisible: first fixture attempt read `registered 136 /
  tools_total 138` with both findings still present;
- a new `## Gate and probe registry — round87 superseding current rows` section carrying only the two
  rows reads `registered 2 / tools_total 138`, 136 findings, rc 1 (`receipts/10-new-section-counter-test.txt`).
  A new section is only valid if it carries all 138 rows.

With the rows appended to the round71 table (fixture commit `4d11e4cd…`, delta `SKILL.md | 3 ++-`,
2 insertions 1 deletion, no other file): `{"counts":{"findings":0,"missing":0,"registered":138,
"rows_total":138,"tools_total":138},"findings":[],"status":"PASS"} RC=0`.

## 2. Knowledge header — PASS, including the round-87 entry

```
{"branch": "master", "branch_tip": "cefb4188…", "clean_count": 103, "complete_count": 103, "finding_count": 0, "findings": [], "note_count": 103, "origin_tip": "cefb4188…", "status": "PASS"}
RC=0
limine entry: [{'lines': {'recheck': 4, 'source': 3, 'verified-at': 5}, 'path': 'corpus/knowledge/limine-pin-plane-r87.md', 'problems': []}]
```

`corpus/knowledge/limine-pin-plane-r87.md` carries `source:` (line 3), `recheck:` (line 4) and
`verified-at: 2026-11-06` (line 5) at column 0, all outside fences; the gate reports no problem.

## 3. Census selftest — PASS

```
TSUKUROI_CENSUS_SELFTEST: PASS (218 cases, 218 passed, 0 failed)
RC=0
```

218 `PASS` lines, 0 `FAIL` lines (`receipts/05-census-selftest.txt`).

## 4. Sources census — clean for the lane

```
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
RC=0
```

52 `W04` duplicate-URL warnings (pre-existing, warnings do not change status), no `E01`-`E12`, and no
`S350`-`S354` row appears in any finding — the five round-87 sources are cleanly registered.

## 5. Supplementary — recheck commands (not in the seat's named list)

`python3 tools/check-recheck-commands.py --revision cefb4188…` → rc 1, 3 findings, all
`RECHECK-FORBIDDEN-INVOCATION` "recheck procedure invokes pacman":
`corpus/knowledge/journald-retention-plane-r76.md:5`, `corpus/knowledge/kernel-taint-plane-r69.md:3`,
`corpus/knowledge/mkinitcpio42-onrelease-r64.md:3`. The same three are present at the pre-round tip
`220c86e315b727696d7c5efeaa7febea6b005e4a` (`receipts/08-recheck-pre-round.txt`), so they are carried,
not introduced by round 87. The new limine entry is not among them: `clean_count` 83 → 84 and
`file_count` 102 → 103 across the round, and its `recheck:` directive is `sudo python3
tools/check-limine-pins.py --live` — `sudo` is not in the gate's forbidden list, but that directive is
operator-only (every seat this round is forbidden `sudo`), so the entry's recheck cannot be executed by
a seat. Recorded as an operability observation, not a defect: the entry's own operator-action section
already scopes the live run to the operator.

## Instrument identity (context for the drafted row)

```
f2551c8e8386d599e3c2aca8888d5fbb0351a5a399dc43dc448556e99361989d  tools/limine-pin-battery-r87.py
bbcc874ac8143ffb9bd97e4d3e2dfd934af3d6573f741d8b8ee3c00ecda9b73c  tools/check-limine-pins.py
```

The battery hash equals the value in `.ufo/waves/round-87/before/freeze-manifest.sha256`
(`receipts/09-instrument-sha256.txt`), so the sha256 published in the drafted row is the frozen one.
Both selftests at the tip: `check-limine-pins.py --selftest` → `selftest PASS 14/14` rc 0;
`limine-pin-battery-r87.py --selftest` → `selftest PASS 5/5` rc 0 (`receipts/04-selftests.txt`).

## Files written

- `.ufo/waves/round-87/w1/ExecLints.md` (this report)
- `.ufo/waves/round-87/w1/ExecLints/registry-rows.md` (both drafted rows + insertion point + verification)
- `.ufo/waves/round-87/w1/ExecLints/receipts/01-10` (verbatim command output with `RC=`)

No lane file was edited. Nothing was committed, pushed, or run outside the scratch clones
(`$S/lane` read-only, `$S/fixture` for the row-placement experiment only, both removed).

Provenance note: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain` at the end
of this seat shows ` M corpus/QUALITY.md` plus the untracked `w1-*` dispatch files. Neither is this
seat's: every read above was taken from the clone at `cefb4188…`, and this seat wrote only the three
paths listed here.

## Risks

1. The two `REGISTRY-ROW-MISSING` findings are the only lane-conformance red at the tip; they are
   closed by landing the two drafted rows in the round71 table, not by a new registry section.
2. The round-77 heading (`SKILL.md:6127`) is invisible to the parser (space in "round 77"); any future
   round that adds a section must match `^## Gate and probe registry — round([0-9]+) superseding
   current rows$` exactly and carry every row.
3. The three carried `RECHECK-FORBIDDEN-INVOCATION` findings are outside this round's scope and were
   not repaired.
