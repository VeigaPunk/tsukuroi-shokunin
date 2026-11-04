# Round 71 — lesson (tsukuroi, hyaku run 15, attempt 1)

author: tsukuroi L1 (round 71), integrating the wave `.ufo/waves/round-71/` (14 seats, one v1 wave).
This skeleton was drafted mid-wave by seat `SC3Lesson`: every cell marked `<wave>` is filled by the L1
at integration, and nothing in this file is an after-measurement.
basis: declaration `0fcfca31` (frozen before data; base `930d5530`); the pre-data receipts in
`.ufo/waves/round-71/before/`; wave results `.ufo/waves/round-71/w1-results.json` and the seat reports
in `.ufo/waves/round-71/{w1,probes}/`.

## Gate

**Trigger and sources.** Four source documents were fetched and read before the declaration text and
committed byte-exact under `.ufo/waves/round-71/before/src/` with `SHA256SUMS` and `SOURCES.json`, all
at Linux stable **v7.2.11** (the host's own kernel), access date **2026-11-04**. Re-verified by this
seat at `0fcfca31`: `sha256sum -c SHA256SUMS` → 4/4 OK, rc 0; `SOURCES.json` holds exactly four map
keys, each digest equal to its file's sha256.

| id (planned) | snapshot | URL | sha256 | rows planned |
|---|---|---|---|---|
| **S297** | `kernel/params.c` (24 289 B) | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/kernel/params.c?h=v7.2.11` | `923610d5de631d8b8dddcb89bf4b0f6932fb0dbf1f500d07453ea0b73b3782a4` | MP1, MP2 |
| **S298** | `include/linux/moduleparam.h` (23 655 B) | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/include/linux/moduleparam.h?h=v7.2.11` | `220f2dac723a7b080211791a33cb3308ed12eaeb2309747232786d786cd14846` | MP3 |
| **S299** | `kernel/module/main.c` (104 325 B) | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/kernel/module/main.c?h=v7.2.11` | `e1e1a1c8a13f3d5e402bb8773b4aea3561dadcdca446b3dfb0482b0ddcb95929` | MP4, MP5 |
| **S300** | `Documentation/admin-guide/kernel-parameters.rst` (5 246 B) | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/kernel-parameters.rst?h=v7.2.11` | `45587d8e411db06dc600550f03236d3b7cbe7ad5bd898dbb9f965934ecd88799` | MP6 |

The four ids are free at base (`corpus/SOURCES.md` reads 296 rows at `930d5530`; zero rows match
`S297`-`S300`), and the row-to-snapshot split above is the one the frozen battery's control fixture
exercises (MP1/MP2 → `params.c`, MP3 → `moduleparam.h`, MP4/MP5 → `main.c`, MP6 →
`kernel-parameters.rst`, max snapshot reuse 2).

**Admitted.** `<wave>` — the four rows are admitted only when the landed note's MP1-MP6 read
`MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0`, `met=1`, rc 0 at the measured
revision under the frozen counter `tools/count-mp-rows-r71.py` (sha256 `fa67d4de…48bc`). The per-row
quote cells, their line anchors and the located-quote check are filled from the note at landing;
snapshot-level provenance is verified above, row-level admission is not yet claimed.

**Rejected.** `<wave>` — one row per refusal, with reason and flip. The r70 pattern expects at least a
duplicate registration byte-identical to a held snapshot, an own-work row (QUALITY 86 forbids it as a
rule row), and a token defined outside the pinned bytes; the wave's actual rejects go here.

**Non-author spot-check.** OWED. The closure judge re-opens the four URLs live and compares the bytes,
digests and located quotes against the committed snapshots, then records its admit/reject agreement
table here. No author-side `[x]` is written.

**Census.** Round start (declaration receipt, `before/absence-controls.txt`): canonical validate rc 0
at 296 registry rows and 88 knowledge notes. Round end after the note and the four rows land:
`<wave>` (expected 300 rows, 89 notes; command
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`).

**QUALITY 98 watch.** `<wave>` — no upstream release fired for the pinned artifacts this round: the
kernel tag is the host's own v7.2.11 and no pinned package moved; confirm at integration.

## Mistakes

- **R71-DECL-BATTERY-COUNT** — class `stale-tally drift` (the r70 D1 family: a prose count the receipt's
  own line contradicts) · evidence: the declaration at `0fcfca31` says "**12 cases: 1 well-formed
  control + 11 mutants**" (`0fcfca31:SCORECARD.md:5467`), while the committed receipt
  `.ufo/waves/round-71/before/control/battery.txt:24` prints `BATTERY cases=11 passed=11 failed=0` with
  11 `[PASS]` lines; the prose names ten mutants; `before/control/battery.py` appends the control into
  `cases` (`:107`, `:103`) and counts `len(cases)` (`:167`), so the receipt's 11 is 1 control + 10
  mutants · captured-by: `SC3Lesson`, this draft (the battery was not re-run) · fix: correct the count
  append-only to "11 cases: 1 control + 10 mutants", or add the missing eleventh mutant in the next
  battery amendment; the frozen predicate is untouched (the battery case count is not a claim
  conjunct), and QUALITY 105's sweep covers the receipt-line diff.
- **R71-D1-STALE-TALLY-OPEN** — class `stale-tally drift` (r70 routed defect 1) · evidence: at
  `0fcfca31` three files still carry the superseded instrument figure — `PROVINCE.md:372`
  "(212 cases, 16 labelled `R70-C2`)", `corpus/README.md:613` "selftest 196 -> 212",
  `SKILL.md:5773-5774` "grows 196 → 212 cases, 16 of them labelled" — while the r70 final receipt
  `.ufo/waves/round-70/after/selftest-after.txt:217` reads `PASS (214 cases, 214 passed, 0 failed)` and
  carries 18 `R70-C2` lines; the diff-scoped sweep prints five mismatches (three case figures, two
  label figures), rc 1, and zero on a corrected control
  (`.ufo/waves/round-71/probes/SC3Lesson/sweep-receipt.txt`) · captured-by: r70 spot-check §5.1;
  re-measured by `SC3Lesson` · fix: append-only corrections in the same commit that touches each file,
  against the final receipt line; status at draft: **open** (three files still carry 212/16). QUALITY
  105 records the pre-report sweep.
- **R71-D2-UNBACKED-RERUN** — class `unbacked final-revision receipt` (r69 D2 / r70 routed defect 2) ·
  evidence: the r70 report's receipt chain (`.ufo/reports/round-70/tsukuroi.md:104-105`) claims a
  cited-receipts PASS "re-run at `79dac76c` (75 files, 42 cited paths)" and `count-xs-rows-r70.py`
  "re-ran 6/6 at `79dac76c`"; the committed receipt is
  `after/cited-receipts-r70-at-50389560c1d8c6fee7c0e348b4469727b4baddcf.txt` (74 files, 42 cited
  paths), and `git ls-tree -r --name-only 79dac76c -- .ufo/waves/round-70/after
  .ufo/waves/round-70/probes` lists no receipt naming `79dac76c` · captured-by: r70 spot-check §5.2;
  re-checked by `SC3Lesson` · fix: commit the receipt at the measured revision or correct the report
  line append-only; status at draft: **open**.
- **R71-D3-SHEBANG-UNCOMMITTED** — class `shebang/source mismatch` (r70 routed defect 3) · evidence:
  `git show 0fcfca31:tools/count-xs-rows-r70.py | head -1` prints `#!/usr/bin/env bash` over Python
  source; the working tree carries the one-line repair (`#!/usr/bin/env python3`) as an **uncommitted**
  modification (`git diff --stat tools/count-xs-rows-r70.py` → 1 insertion, 1 deletion;
  `git status --porcelain` → ` M tools/count-xs-rows-r70.py`) · captured-by: r70 spot-check §5.3;
  re-checked by `SC3Lesson` · fix: commit the shebang line with the next counter amendment; status at
  draft: **repair present, uncommitted** — not citable as landed until the commit exists.
- **`<wave>` — wave-caught rows.** The wave's attack receipts (`w1/<seat>.md`, `probes/<seat>/`) add
  their rows here, one per finding, in the same class / evidence / captured-by / fix form.

Not Mistake rows: the inherited untracked dispatcher markers
(`.ufo/waves/round-66|67/w1.ready.dispatched`) and the open L0 questions (`tsukuroi | round-64`,
`round-60`, `round-57`) are operator/closure items, recorded as routed around rather than answered.

## Considerthese

No proposal is mined this round; the measured status of the four proposals in the latest file
(`considerthese/2026-10-26.md`) is recorded, each verified by a grep at `0fcfca31` rather than
restated:

- **"Counter-attack scoreboard"** — standing `SKILL.md` ledger since r41/r42, resumed at r64: 15
  exact-phrase hits across 7 files (`SKILL.md` 5; `corpus/lessons/` 10 — r41×2, r47, r52, r64×2, r68,
  r70×3); continued by this round's scoreboard rows (`.ufo/waves/round-71/w1/SC3Lesson/quality.md`
  §Scoreboard).
- **"Seat-harm incident log"** — lessons-only per-round tally since r66: 4 exact-phrase hits, all in
  lessons (r45, r66, r67, r70), 0 in `SKILL.md`; this round's tally cell is `<wave>`.
- **"Burst-aware reading"** — one mining record (r46): 2 exact-phrase hits (r46, r70); explicitly not
  a gate.
- **"Cross-note correction propagation map"** — 0 hits for the capitalised phrase; 5 case-insensitive
  "propagation map" hits across 5 lesson files (r43 section, r54 spot-check, r57, r58, r70), recorded
  partial at r43/r54; r57/r58 say "none clears this round's bar". Not adopted.
- (The file's fifth proposal, "Downstream patch-offset check", was adopted at round 69 as QUALITY 103
  — `corpus/QUALITY.md:201`, the r69 lesson and three knowledge notes — and is recorded here so a
  later round does not re-adopt it.)

The scoreboard is a continuation of the r64 ledger, not a new adoption; its round-71 row set is
drafted in `.ufo/waves/round-71/w1/SC3Lesson/quality.md` §Scoreboard with the survivor cells left
empty for the wave.

## Trend verdicts

- **expansion: `<wave>`.** Deciding receipts: the four registry rows S297-S300 (0 such rows at base;
  `corpus/SOURCES.md` 296 rows), the note `corpus/knowledge/module-parameter-plane-r71.md` absent at
  base (rc 128) and 6/6 rows at the measured revision under the frozen counter, and the held-ground
  sweep (`before/novelty-sweep.txt`: `modprobe.d`, `kernel-parameters`, `module_blacklist`, `NVreg`,
  `module_param`, `kernel_param_ops`, `param_attr_store` each 0 hits; 88 notes, none naming the
  surface). Improved only if the note lands 6/6 with the four rows; otherwise unchanged.
- **quality: `<wave>`.** Deciding receipts: D1/D2/D3 land append-only with their correction receipts;
  QUALITY 105 adopted with the sweep's red/green receipt
  (`.ufo/waves/round-71/probes/SC3Lesson/sweep-receipt.txt`); the declaration's battery count
  corrected. The sweep is demonstrated able to fail on r70's own bytes (5 mismatches, rc 1) and pass
  on the corrected control (0, rc 0) — a draft demonstration, not an adoption.
- **discernment: `<wave>`.** The outside non-author admit/reject spot-check is owed by the closure
  judge (`LEARNING.md`: a seat this lane dispatched is still the lane); no author-side `[x]`, and the
  wave's own catches are mined into `## Mistakes` rather than smoothed.

## Seat-harm tally (standing per-round tally, r66 adoption continued)

Round 71: `<wave>` — the sentinel receipt is owed. Running tally since r66: 0, 0, 0, 0, 1 plus this
round.
