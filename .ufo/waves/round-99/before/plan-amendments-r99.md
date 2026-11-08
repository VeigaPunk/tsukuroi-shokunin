# Round 99 — pre-report amendments (append-only; the frozen bytes stay as pinned)

The frozen declaration is `.ufo/plans/round-99.md` (sha256 `62319128…`, pinned in
`before/instruments.sha256`). This sidecar narrows WORDING only; no target value, counter, kill rule
or instrument byte changes. Every row below names the committed artifact that falsified the frozen
sentence.

## A1 — C2's capture universals are narrowed to the shapes the guard was frozen against

**Frozen sentences (claims.json C2 predicate):** "a hybrid cell (`VARIANTS N01-N04,N05`, the r98 A1
survivor that read PASS 7/7) reads RC-CELL-MISSING and a cell mentioning VARIANTS twice (the r98
same-cell-restatement survivor) reads the new RC-CELL-AMBIGUOUS."

**Falsified by:** `w1/ReviewRegistry.md` §2 rows x1, x2, x3, x4, x5, x10, y1-y4 and
`w1/CriticClaims/receipts/10-xv1-hybrid-then-valid.txt` (`PASS 7/7`),
`10-xv2-space-extra.txt` (`PASS 7/7`), `10-xv3-valid-then-hybrid.txt` (`PASS 7/7`). The universal
is false: the guarded capture binds only shapes whose span token is followed by a character outside
`[0-9,-]` AND whose other `VARIANTS` mentions are themselves capturable.

**Narrowed sentence:** the capture closes exactly these classes, each measured:

| class | shape | r98 | r99 |
|---|---|---|---|
| hybrid span, `,`-joined extra label | `VARIANTS N01-N04,N05` | PASS | `RC-CELL-MISSING` |
| hybrid span, `, ` (comma + space) | `VARIANTS N01-N04, N05` | PASS | `RC-CELL-MISSING` |
| two capturable mentions | `VARIANTS N01,N03 then VARIANTS N01-N03` | PASS | `RC-CELL-AMBIGUOUS` |
| two capturable identical mentions | `VARIANTS N01-N04 and VARIANTS N01-N04` | PASS | `RC-CELL-AMBIGUOUS` |
| second mention in an escaped pipe / tight juxtaposition / backticks | `… \| VARIANTS …`, `…VARIANTS …`, `` … `VARIANTS …` `` | PASS | `RC-CELL-AMBIGUOUS` |

**Named limits (measured green, routed to r100):** an extra label after a space, `;`, `+`, `/` or the
word `and` (`VARIANTS N01-N04 N05`, `…; N05`, `…+N05`, `…/N05`, `… and N05`); a hybrid span paired
with one clean mention (`VARIANTS N01-N04,N05 and VARIANTS N01-N04`); a contradictory second mention
that is not capturable (`… and VARIANTS n01-n03`, `… and VARIANTS N01, N03`); a second span stated in
prose inside the same cell (`VARIANTS N01-N04 (keys N01-N05)`); a letter suffix on the token
(`VARIANTS N01-N04extra`). These read the derived value and PASS. The guard's alphabet is `,` and
`-`; widening it is r100's work, not a re-reading of this round's bytes.

**Unaffected:** C2's frozen TARGET (the two committed fixtures `hybrid` and `restated`, the landed
`PASS 7/7`, the `PASS 17/17` selftest, the M07 kill, the `PASS 160/160` coverage leg) holds exactly
as frozen; the two committed fixtures are rows (a)/(b)/(f) above.

## A2 — the `ancestor` case's coverage is stated as branch-only

**Frozen sentence:** "`--selftest` gains `span-hybrid`, `span-restated` and `ancestor` (14 -> 17)."

**Holds**, but the case pins one branch (a revision that is not an ancestor of the selected branch).
`w1/ReviewRegistry.md` §7 records that five forged PASS shapes (x1-x5, y1-y4, x10) have no selftest
case; the 17 cases pin the three frozen shapes plus the ancestor branch, not the capture's whole
alphabet. Recorded as a limit, not a defect of the frozen target.

## A3 — R99-D1 is a repair, not a claim

The r98 settled-tip coverage figure is re-measured and committed under
`before/r99-d1-coverage-tip-f107da3a.txt` (`PASS 160/160 findings 0`) and
`before/r99-d1-coverage-r98settle-270ca298.txt` (same counts at the r98 settle). The r98
`after/report-draft.md` pointer stays as filed history (append-only); no r98 artifact is edited.

## A4 — "exactly two changes" is narrowed to "two behaviour-bearing changes" (both instruments)

**Falsified by:** `w1/CriticClaims.md` (row set 19/20, instrument diffs). The r98→r99 diff carries,
besides the two declared changes: a payload **schema-token rename** in each instrument
(`tsukuroi-limine-pin-battery-r97-v1` → `…-r99-v1`; `tsukuroi-registry-content-r97-v1` → `…-r99-v1`),
a selftest tempdir-prefix rename in the checker, and one **unreachable** fixture-sentinel entry
(`("ANCESTOR", None, None)` appears in `build_fixture`'s exclusion tuple although no `ANCESTOR`
doctor exists, so it matches nothing).

**Narrowed sentence:** each instrument differs from its r98 predecessor by exactly two
**behaviour-bearing** changes (the ones the claim names), plus a payload schema-token rename and, in
the checker, a tempdir-prefix rename and one unreachable sentinel entry. The schema token is part of
the round's name (`-r99-`), carries no verdict, and is stated here rather than counted as a third
change. The dead sentinel is inert by construction (an exclusion-set member with no matching case)
and is **routed to r100** for removal; it is not edited now because the instrument bytes are pinned
and an edit would void C2's kill rule.

## A5 — C1's lie-kind closure is stated per FIELD, not per family

**Falsified by:** `w1/CriticClaims/receipts/17-*` — a mutant of the r99 battery with the Z family's
`check_echo` removed still reads `unmet 94/105` on the `lie-limine-version` wrapper, with the Z
family 4/4 green (other families supply the verdict).

**Narrowed sentence:** a field lie anywhere in the roster now reads `unmet` under the two new lie
kinds (measured `93/105` and `95/105` on the pristine instrument); a **per-family** assertion
removal is still invisible to `--selftest --reference` and is seen only by a spelling-targeted bend
(`Md`, the Y family's `check_era` removal, makes `N09-y-era` read `met 105/105` —
`w1/ReviewBattery-9/receipts/mut-Md-y-era-on-N09.json`). The r98 scoreboard's "lie-kind structural
gap" is therefore closed at field level only, and the round says so.

## A6 — seat harm (scratch), disclosed

`w1/CriticClaims.md` §7b: at ~11:23–11:24 -0300 that seat removed its own scratch dir and then ran
`rm -rf /fast/scratch/hyaku/tsukuroi-r99` — the shared parent — deleting sibling scratch dirs
(`ConnectorOverlap`, `MutRegistry`, `ReviewBattery-9`, `ScoutFrontier`, `ScribeKnowledge`,
`ScribeLesson`) and the lane `dev` dir. Four were re-created by their seats; any receipt that lived
only in scratch is lost. Committed evidence was unaffected: every receipt cited in this round had
already been copied into `.ufo/waves/round-99/w1/<Seat>/` or `before/`, which is why the round's
numbers re-derive. The lesson carries the seat-harm row and the isolation rule (a delete must be
asserted to end in `/<SeatName>` before it runs).

### A6a — the L1's own reference-selftest run was a casualty of the same delete

The L1 started `python3 tools/limine-pin-battery-r99.py --selftest --reference
tools/check-limine-pins.py` at 11:02 with `TMPDIR=/fast/scratch/hyaku/tsukuroi-r99/dev`; the delete
above removed its live tempdir and the run died with
`FileNotFoundError: … /limine-battery-selftest-478ev092/…` (receipt
`before/dev/c1-selftest-r99-reference.txt`, 30 lines, rc 1). The leg is therefore **not run** this
round and is not claimed: C1's target requires `--selftest` **without** reference (`PASS 5/5`,
measured) plus the two lie kinds measured directly as gate runs (`93/105` and `95/105`), both of
which stand. The full 14-kind reference leg is carried to r100 as owed evidence.

## A7 — the two lie kinds are roster-scoped, and they cannot see a per-family assertion removal

**Falsified by:** `w1/ReviewBattery.md` (wording finding 1) and `w1/CriticClaims.md` (C1-9). With
**both** metadata assertions disabled, the two lie legs still read `unmet 100/105` and `98/105`;
with a single flag removed they read exactly `93/105` and `95/105` with *identical* family sets to
the pristine instrument. The verdict is therefore supplied by the pre-existing r98 assertions (Z,
LZ, EXPLICIT, AUTO), not by the new X/Y ones.

**Narrowed sentence:** the two new lie kinds make the selftest falsify the two reported fields
*somewhere in the roster*; they do **not** certify that any particular family asserts them, and they
cannot see one family's assertion being removed. The per-family witnesses are the committed bends
alone (`Md`/M4: deleting the Y family's `check_era` makes `N09-y-era` read `met 105/105`;
deleting the X family's `check_era` drops `N11-x-era` from `103/105` to `104/105`). Consequently the
r98 scoreboard's "lie-kind structural gap" is closed only in the "a field lie is now a selftest
kind" sense, and C1's verdict says exactly that.

## A8 — the field closure is roster-finite, and the X leg is a near-twin

**Falsified by:** `w1/ReviewBattery.md` (wording finding 3) — two forgeries read `met 105/105` while
lying: **W1** echoes correctly only for the roster's spellings, and **W2** selects the era from the
first component as text. Also `w1/ReviewBattery.md` finding 4 and `w1/CriticClaims.md`
(twin count).

**Narrowed sentence:** the X/Y field assertions are certified only for the roster's own spellings and
only against a gate that computes the era from the numeric tuple. A gate that lies off-roster, or
that reads the era from one component, still reads `met 105/105`; those are r100's frontier, named
here. And the X leg is a **near-twin** under QUALITY 136: its own answer changes (a real delta), but
the article it detects was already caught by a single `EXPLICIT-VERSION-ERA` case before this round.
The round's genuinely new discrimination is the Y family (r98 `met 105/105` → r99 `unmet 104/105`).

## A9 — the twin-bend receipt is re-pointed to a committed artifact

The frozen declaration cites `before/dev/c1-N10-twin-r98-control.json`, which the L1's own copy step
did not land (the scratch dir was deleted by the A6 harm before the copy). The measurement itself was
re-derived independently by `ScribeLesson`
(`w1/ScribeLesson/receipts/12-N10-twin-batteries.txt`, `receipts/json/N10-{r98-control,r99}.json`)
and now sits at `before/dev/c1-N10-twin-r98-control.json` and
`before/dev/c1-N10-twin-r99.json` (copied byte-exact from that seat's committed receipts). Both read
`unmet 104/105` with exactly `[REFUSAL-VERSIONS-9DIGIT-Z]`, which is the twin finding the declaration
states. No number changes; the pointer is repaired.
