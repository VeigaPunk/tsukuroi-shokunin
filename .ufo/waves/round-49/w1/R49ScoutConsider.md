VERDICT: draft

# F-1 — considerthese mine (round-49 w1, seat R49ScoutConsider)

Axes used: (1) still unimplemented at freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c`, (2) relevance to C1 scrub-row admission, C3 census fd-band diagnostics, or C2 adjacency pointers, (3) groundable from committed bytes before this wave's attack reports exist, (4) lesson landing with no new claim. A candidate that loses (2) or (3) is listed, not chosen.

Checked set: `ls -l considerthese/` (seven files, 2026-10-19 through 2026-10-26). Newest three read whole: `2026-10-26.md` (mtime Oct 26 14:08), `2026-10-25.md` and `2026-10-24.md` (both mtime Oct 25 15:59). Older four read for context only; none beat the candidate below. Status is `git grep` / `git show` at the freeze, not the mutable worktree.

## Newest three — every self-improvement bullet

| File:line | Proposal | Still unimplemented? | Relevant to C1/C2/C3 or this frontier? |
|---|---|---|---|
| `2026-10-26.md:17` | Burst-aware reading | No. Lesson `corpus/lessons/round-46.md:97` | — |
| `2026-10-26.md:18` | Counter-attack scoreboard | Partial. Tables exist for r40–r42 only (`SKILL.md:3833`, `:3935`; mined `corpus/lessons/round-41.md:99`). No `Arms fielded` row after round 42. Round 47 left it open (`corpus/lessons/round-47.md:71`: "no longitudinal survivor ledger was added; the proposal remains open"). Round 48 adopted nothing (`LOG.md:1698`). | Yes, to all three frozen counters — but r49 beating-arms are not in committed reports yet. Pre-data K-rows are expected FAIL/K-pass (`FROZEN.md:43-50`), not attack arms. |
| `2026-10-26.md:19` | Seat-harm incident log | No. `corpus/lessons/round-45.md:124` | — |
| `2026-10-26.md:20` | Downstream patch-offset check | No. `corpus/lessons/round-42.md:53` | — |
| `2026-10-26.md:21` | Cross-note correction propagation map | No. `corpus/lessons/round-43.md:83` | — |
| `2026-10-25.md:17` | Quiet-day mode | Yes (string only in this note) | No. Reflection-bot housekeeping. |
| `2026-10-25.md:18` | Next-round pickup sheet | Yes | Same job as the carry-over check; subsumed, not a second landing. |
| `2026-10-25.md:19` | Probe lineage table | No. `corpus/lessons/round-38.md:109`, extended `round-40.md:95`; `SKILL.md:3498` | — |
| `2026-10-25.md:20` | Evidence-weight watch | No. `corpus/lessons/round-39.md:94` | — |
| `2026-10-24.md:17` | Upstream release watch | Yes as a general watch. The only other hit is one specific open sentence, `corpus/knowledge/pause-lift-gate-r24.md:90` ("upstream-release watch for removal of the compatibility symlink"). | Marginal. The note names btrfs-progs; this round's C1 is the seven named GR corrections, not a version bump. |
| `2026-10-24.md:18` | Routed-debt carry-over check | Yes. No `### considerthese — routed-debt` section. `carry-over` elsewhere is a different use (companion prose; `tools/check-scrub-admission-r49.py:12` "F1 carry-over" means an inherited counter rule, not an age ledger). | Yes. Best. |
| `2026-10-24.md:19` | Seat-loss tally | Yes | No tie to the three frozen surfaces. |
| `2026-10-24.md:20` | Live-harm flag for env changes | Yes | No. Child-env allow-list arc, not these claims. |
| `2026-10-24.md:21` | Claim-arc length | Yes (title string only in this note) | Yes, weaker. Round-48 C2 is an unclosed scrub-admission goal (`round-48.md:8` FAIL). The carry-over table records that age; a second arc ledger would duplicate it. |

Round 48's scout already recommended the carry-over check (`.ufo/waves/round-48/w2/ScoutConsider.md:106`) and the L1 did not adopt it (`LOG.md:1698`). It is still open at this freeze.

## Best ONE candidate

- **File / date:** `considerthese/2026-10-24.md:18`, file dated 2026-10-24, committed `f0b8f7a5` 2026-10-24T09:32:49-03:00 (`git log -1` at the freeze).
- **Exact words (18):** "check whether the following round closed each one and report what is carried over and for how long".
- **What it would change:** each lesson already has a one-round disposition table. Nothing consolidates a debt's open round, last naming, and whether the next round closed it. This round is that check for two routed leftovers: GR1/GR2 admission (round-48 C2 FAIL) and the stale `/tmp` comment plus silent fd-band exhaustion (round-48 C1 PASS with those defects left outside the predicate). C2 adjacency (bare `*.md:N-M` ranges → OUT anchors) is a new surface in the round-49 LOG entry, not a row of this ledger, unless a later grep finds a prior routed id. I did not find one.
- **What to open to ground it:** `corpus/lessons/round-48.md:8` (C2 FAIL: GR1 one `partly`, GR2 two `partly`, `marks_ok=0`; C1 PASS but "fd band 240–249 exhausts fail-closed without a summary") and `:31` (`R48-C1-STALE-TMPDIR-COMMENT`, "Next round correct the comment; routed"). `LOG.md:1702` is the round-49 heading; the motivating paragraph under it names C1 as those GR corrections and C3 as the stale `/tmp` comment and fd-band diagnostics. `FROZEN.md:15` and `:17` are the counters that would close them. Do not count ages from this scout's prose; re-count lesson files at integration. Binding shape already accepted: `corpus/lessons/round-45.md:124` (seat-harm rows bound to a cite and a verbatim quote).
- **QUALITY criterion or lesson, no new claim?** Lesson only. Same landing as round 41's scoreboard note and round 46's burst-reading note: a `### considerthese — …` section in `corpus/lessons/round-49.md`. Not a QUALITY.md row. Criteria 88–90 already govern counter controls (`corpus/QUALITY.md` items 88, 89, 90; item 90 is at line 177 of the freeze file). This proposal is a closure ledger, not a frozen predicate. No new claim: it does not change `check-scrub-admission-r49.py`, `check-adjacency-table-r49.py`, or `check-fd-band-r49.py`.

### Exact proposed text

```
### considerthese — routed-debt carry-over check (`considerthese/2026-10-24.md:18`, filed 2026-10-24)

Mined: "check whether the following round closed each one and report what is carried over and for how long."
Per-round disposition tables name a state, not an age. Rows below cite the line that opened the debt and the line that names it this round. "Addressed" means this round's frozen claim names it; it is not a measured close.

| Debt | Opened | Named this round | State |
|---|---|---|---|
| GR1/GR2 scrub-row admission (GR3 held) | `corpus/lessons/round-48.md:8` (C2 FAIL, `marks_ok=0`) | C1, LOG.md round-49 motivating paragraph; `FROZEN.md` C1 row | addressed, not yet measured |
| Stale census `/tmp` comment | `corpus/lessons/round-48.md:31` (`R48-C1-STALE-TMPDIR-COMMENT`, "Next round") | C3, same LOG paragraph; `FROZEN.md` C3 row | addressed, not yet measured |
| Fd band 240–249 exhausts with no summary | `corpus/lessons/round-48.md:8` (inside the C1 PASS bullet) | C3, same | addressed, not yet measured |
| Counter-attack scoreboard after round 42 | `corpus/lessons/round-47.md:71` ("remains open") | not a round-49 claim | open — r40–r42 tables stand (`SKILL.md:3833`, `:3935`); no later `Arms fielded` row |

Rule taken: a debt marked routed is named again in this table at the next integration, with opened-line and named-line cites. An age is the count of lesson files between those cites, not a number copied from a prior scout. The scoreboard continuation stays a row here until attack reports exist to fill `Arms fielded`; pre-data K-pass fixtures are not attack arms (`FROZEN.md`: K-pass runs are never the claim's measurement).
```

## Not done

Did not run the three counters, did not count attack arms in `.ufo/waves/round-43` through `round-48`, and did not re-resolve every debt older than round 48. Those ages are not in the proposed table.
