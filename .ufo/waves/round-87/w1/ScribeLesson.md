# ScribeLesson — round-87 w1 (draft only; the L1 lands)

Seat: ScribeLesson (scribe, leaf). Judged on depth; milestone C2 `corpus/knowledge/limine-pin-plane-r87.md`
LP1-LP8. Lane revision measured: `cefb4188b484329c4908a19a277f8fb120fb4f56` (`git -C
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`, rc 0, `receipts/r01`). Freeze `5eb8b157`,
candidate `a097bd9d`, entry `cefb4188`; citations are by hash. At measurement the lane working tree carries
` M corpus/QUALITY.md` (`git diff --stat` → `1 file changed, 3 insertions(+)`, the 124 text at
`corpus/QUALITY.md:285`) and the untracked `corpus/lessons/round-87.md`; this seat read both and authored neither.

## What this seat did

Read, not re-ran: `corpus/lessons/round-86.md` (M3, `Routed to round 87`), `corpus/lessons/round-86-verifier-spotcheck.md`
§5 routed 1-5, `corpus/QUALITY.md` 99/120-123 and the tail 60 lines, `SCORECARD.md` "Round 87 — declaration",
`.ufo/waves/round-86/w1-spec.json` and `.ufo/waves/round-87/w1-spec.json` (wave contexts), the r86/r87 freeze
control summaries and the r86 controls receipt, the r86 `ScoutHost.md` §0 and
`ScoutHost/objcopy-incident/CURRENT-HASHES.txt`, `.ufo/waves/round-87/after/live-receipt.txt`,
`.ufo/waves/round-87/before/host/receipt.txt`, `.ufo/waves/round-87/before/freeze-manifest.sha256`,
`tools/limine-pin-battery-r87.py` (docstring R1-R7, family map, `fam_host_shape`) and `tools/check-limine-pins.py`
(docstring exit map), the `resume-gate-battery-r86` registry row at `SKILL.md:5920` and the `Round-81/71
correction` blocks at `SKILL.md:5925` and `:5936`.

Ran (read-only, receipts `r01`-`r10`): `git rev-parse/log/status/diff/show` in the lane and in the fleet root,
`grep`, `sed`, `sha256sum`, and one `diff <(git show …) <(git show …)` over two fleet-root commits of a filed
report. **No battery, gate or `--selftest` was executed by this seat**; every score quoted in the drafts is read
from a committed receipt or a wave-seat receipt. No `sudo`, no `/boot` or `/efi` access, no writer tool
(`objcopy`/`strip`/`sbsign`/`ukify`/`mkinitcpio`/`limine*`/`bootctl`/`efibootmgr`), no subagent, no tool
installed or upgraded, no scratch dir left behind.

## Deliverables

| # | Draft | File | State |
|---|---|---|---|
| 1 | `corpus/QUALITY.md` criterion 124 `R87-BOOT-NO-INPLACE-WRITER` | `ScribeLesson/01-quality-124-draft.md` | complete: paste-ready text in the 120-123 form (predicate, `Captured by:`, red/green fenced block, `Shown able to fail:`, `Lesson:`); two repairs over the working-tree draft (exit map instead of "rc 0 or name the pins"; committed controls instead of a hypothetical) |
| 2 | `corpus/lessons/round-87.md` `## Mistakes` rows | `ScribeLesson/02-mistakes-round87-draft.md` | complete: M1 `R87-INTENT-RULE-NOT-TOOL-RULE` (the round-86 incident class) and M2 candidate `R87-FILED-BYTES-SWEEP-NOT-RUN` (the r86 spot-check §5.4 rewrite); a third candidate (r86 routed 3) is deliberately *not* a row — it is repaired by deliverable 3 |
| 3 | appended `SKILL.md` correction `R87-REG-1` for the `resume-gate-battery-r86` row | `ScribeLesson/03-registry-correction-draft.md` | complete: superseded sentence quoted, all twelve controls' values and failed-family sets quoted from `.ufo/waves/round-86/before/controls/controls-summary.txt` (committed at `2f67de80`), placement and form notes |

## Verdict per check

- **(a) QUALITY 124 — drafted and grounded.** Every leg names a committed artifact: the r86 intent bound
  (`grep -c 'IS FORBIDDEN FOR EVERY SEAT'` → 0, `r06`); the absence of any `/boot` digest list in round 86
  (`grep -rl 'b2sum' .ufo/waves/round-86/` → no path, rc 1, `r07`); the two `objcopy` calls and the 5-byte blast
  radius (`ScoutHost.md:19-27`, `:33-34`, `r07`); the post-hoc mismatch (`/boot/limine.conf:30` pin `b990d8c6…`
  vs file `57f5eb94…`, `:38` `a68c281d…` vs `eff78d32…`, mtimes `2026-11-06 18:11:22`, `r05`); the r87 bound
  (count 1, `r06`); the r87 before/after list digest `0f6acc28…0028` twice with `cmp: identical` and the live
  gate rc 1 naming `LP-MISMATCH line 30/38` (`r05`); and the two committed controls that reject a blind check
  (`K1` 0/22, `f1-constant-healthy` 0/22 with `HOST-SHAPE` among the failed families, `r03`).
- **(b) Mistakes rows — drafted with evidence pointers.** M1's `Captured-by` cell says what actually caught it
  (the seat's own disclosure plus the L1 re-check; the four nearest criteria 26/99/118/122 govern other things)
  rather than manufacturing a criterion. M2's evidence is the fleet-root pair `909fad00`→`dd58ef82`: one line
  rewritten 85 s after filing; QUALITY 99's own sweep on the pair reads `1` removed line where `0` is required
  (`r08`). M2 is marked **candidate** — the L1 decides whether it lands.
- **(c) Registry correction — drafted with the exact sets.** Ten of N01-N10 read `29 29 29` and each fails one
  family; N11 `28 28 28` fails `DECOYS-R86,PREC-DECOYS` (2); N12 `26 26 26` fails
  `DECOYS-R86,EMPTY-RESUME,HR-NO-RESUME-ARG,PREC-NO-RESUME-ARG` (4) (`r04`, read from the committed summary).
  The row's range `26-29/30` stands; only `each failing exactly its property family` is superseded. The
  parenthetical in `controls-receipt.txt:9-10` and the `CriticClaims.md:115-116` table already carry the sets,
  which is why the fix is an append, not a new claim.
- **Unrun checks are not passes.** This seat ran no scored instrument; the C1 battery and the live gate readings
  quoted are other agents' receipts. The drafts therefore make no claim about the landed tip beyond what those
  receipts state.

## Findings routed to the L1 (no lane edit made)

1. **`corpus/QUALITY.md` working-tree 124 (uncommitted, `:285`): two legs need repair.**
   - The sentence "After any suspected `/boot` change, `sudo python3 tools/check-limine-pins.py --live` must read
     rc 0 or name the mismatched pins" is self-contradictory: naming the mismatches *is* rc 1. Proposed
     replacement: "reads rc 0 when every pin's file hashes to its `#<blake2b>` suffix, rc 1 naming each
     mismatched/missing/malformed pin, rc 2 when the conf is unreadable or a pin cannot be resolved"
     (`tools/check-limine-pins.py:22-23`).
   - The `Shown able to fail` parenthetical "(a check that could not see the incident would read rc 0)" is a
     hypothetical; QUALITY 122's discipline is a committed control. Proposed replacement: the committed
     `f1-constant-healthy` `0 0 0`/22 (with `HOST-SHAPE` among the failed families) and `K1` `0 0 0`/22 from
     `.ufo/waves/round-87/before/controls/controls-summary.txt`, plus the live rc 1 as the positive reading.
   The full paste-ready text with both repairs is `ScribeLesson/01-quality-124-draft.md`.
2. **`.ufo/waves/round-86/w1/ScoutHost.md:23` mislabels the pin algorithm.** The headline table heads its first
   value "sha256 before (recorded in `/boot/limine.conf`)" and its second "sha256 after my objcopy". The pin is a
   **BLAKE2b-512** digest — the same file proves it at `:51` and `:82-84`, and
   `objcopy-incident/CURRENT-HASHES.txt` labels the 128-hex live values BLAKE2b-512 — while the after column holds
   64-hex values, so the two columns are not comparable digit-for-digit. The filed report must not be edited
   (QUALITY 99). Proposed appended erratum text, for the r87 lesson or a `SKILL.md`-style correction block:

   ```text
   Erratum (round 87) — `.ufo/waves/round-86/w1/ScoutHost.md:23-25`. The headline table heads its pin column
   "sha256 before (recorded in `/boot/limine.conf`)"; that value is a BLAKE2b-512 digest (the same file proves it
   at `:51` and `:82-84`; `objcopy-incident/CURRENT-HASHES.txt` labels the live 128-hex values BLAKE2b-512). The
   "after my objcopy" column holds 64-hex values and is not comparable with the pin; the BLAKE2b-512 values of the
   two live files are `57f5eb94…` and `eff78d32…`. The filed report is not edited.
   ```
3. **Registry correction placement.** The draft is a new level-2 section (the `Round-81 correction` form,
   `SKILL.md:5925-5934`), not a table row, so `check-registry-coverage.py`'s row parser is untouched; still, run
   `python3 tools/check-registry-coverage.py --revision <landed tip>` at landing (the round's own precedent:
   QUALITY 121).
4. **Nothing else found.** The r87 lesson's `## Gate` and registry-changes rows were read and not contradicted by
   any receipt this seat opened; no claim in them is repeated here as verified.

## Receipts (this directory)

| Receipt | Content |
|---|---|
| `r01-revision.txt` | `rev-parse master` `cefb4188…`, `log -4`, `status --porcelain` |
| `r02-quality.txt` | QUALITY numbering `120-124`, the uncommitted 124 diff (3 lines) |
| `r03-controls87.txt` | r87 freeze controls summary, all 22-family sets, three runs each |
| `r04-controls86.txt` | r86 near-miss N01-N12 rows + `controls-receipt.txt:8-12` |
| `r05-receipts.txt` | live receipt and host receipt, verbatim |
| `r06-sudo-bounds.txt` | r86 vs r87 wave-context `sudo` sentences; `grep -c` 0 vs 1 |
| `r07-incident.txt` | `ScoutHost.md:17-32`, `CURRENT-HASHES.txt`, the empty `b2sum` grep (rc 1) |
| `r08-report-rewrite.txt` | fleet-root report commits, `git show --stat dd58ef82`, the one-line diff, the 99 sweep count |
| `r09-freeze.txt` | freeze manifest; battery sha256 `f2551c8e…989d` (matches), gate sha256 `bbcc874a…b73c` |
| `r10-gate-family.txt` | gate exit map (`tools/check-limine-pins.py:22-23`), `FAMILIES` map with `HOST-SHAPE` |

## Refusals and bounds

- No lane file edited; the drafts sit only under `.ufo/waves/round-87/w1/ScribeLesson/`. No `git`/`jj` mutation
  anywhere (the fleet-root reads are `show`/`diff`/`log` only); no commit, push, publish or deploy.
- No `sudo`; no `/boot` or `/efi` access; no writer tool invoked; no sysctl, `/sys` or `/proc` write; no
  `pacman`/`uv`/`npm` install (nothing needed installing, so nothing to record under the tooling rule).
- No battery, gate or selftest executed; no number in the drafts is this seat's re-measurement of another
  agent's instrument.
- No subagent, no `agent://all`, no model choice. Scratch `/fast/scratch/hyaku/tsukuroi-r87/ScribeLesson` was
  created, its `rec/` copied to `ScribeLesson/receipts/`, and the scratch tree removed.
