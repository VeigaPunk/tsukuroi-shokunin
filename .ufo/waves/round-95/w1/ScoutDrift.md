# ScoutDrift — planning data-walk and drift checks (round 95, wave w1)

Seat `ScoutDrift` (scout, axis `calibration`). Lane root
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch `master`, jj-colocated; git HEAD detached — no
mutating git/jj command was run). Freeze commit `2abddda5`, wave-dispatch commit `884ed06b`, tip observed
`a302e688`.

Full report with every command, raw output, PASS/FAIL per line and the receipts list:
**`.ufo/waves/round-95/w1/ScoutDrift/report.md`** (31 KB).
Receipts: `.ufo/waves/round-95/w1/ScoutDrift/` — `claim-diff-claimsjson-vs-planfrozen.txt`,
`receipt-01-claim-texts.txt`, `receipt-03-manifest-verify.txt`, `receipt-04-registry-rows.txt`,
`receipt-05-ready-artifacts.txt`, `receipt-06-wave-shape.txt`, `receipt-07-r94-routed-ledger.txt`,
`receipt-08-frontier-check.txt`.

Scratch `/fast/scratch/hyaku/tsukuroi-r95/ScoutDrift` deleted before this seat yielded. No tool installed
or upgraded (pacman paused host-wide); `python3` 3.14.8, `git` 2.56.0; no instrument edited; no write outside
this seat's dir and this file.

## 1. Claim-text diff — claims.json vs `before/plan-frozen.md` vs the live plan

`before/plan-frozen.md` is **byte-identical to the live plan at `884ed06b`** (`41b15c4e…` both) and is
re-pinned in lockstep at every amendment commit (`2abddda5` → `6d060775…`, `a2ed6eee` → `46e6f268…`,
`884ed06b` → `41b15c4e…`). It is therefore a **mirror, not an independent freeze**.

`claims.json` vs the plan's C1/C2 sentences — every divergence is a **recorded amendment**, not drift:

| field | divergence | record |
|---|---|---|
| C1 predicate | only `9DIGIT:` vs `9DIGIT :` and a period (similarity 0.9805) | same sentence |
| C1 target / kill | the plan's C1 row body still carries the pre-A1 text | **A1** supersedes ("The live sentences are these (and `claims.json`)") |
| C2 predicate / target / kill | claims.json says `PASS`; the plan's C2 row body (lines 74/80/84) says `clean` | **A2** supersedes; the gate's own token is `PASS` (measured: `status: "PASS"`, findings 0, missing 0, tools_total 151, registered 151, `--selftest` PASS 23/23) |
| live plan only | **A3** (post-scoring narrowing of C1's predicate) and **A4** (post-scoring narrowing of C2's predicate and void clause) | both present in the working tree, **uncommitted** at measurement time (`git log -1 -- .ufo/plans/round-95.md` = `884ed06b`) |

`claims.json`'s C1 target/kill match A1's quoted live sentences up to quoting style (`['…']` vs `["…"]`),
`x3` vs `×3`, and one content point: claims.json carries the parenthetical "(the family does not exist there)"
which A1's quoted sentence omits — a gloss carried from the plan's pre-A1 body, not a widening.

## 2. Findings (calibration)

- **F1 (high)** — the **frozen** `claims.json` C1 predicate still says `999999999.9.9` is "the largest
  in-bound member of the gate's published 1-9-digit component cap". `w1/ReviewBattery.md` F1 (cited by A3)
  falsifies that superlative: the cap is per component, so `999999999.999999999.999999999` is in-bound and
  the landed gate accepts it. `claims.json` is manifest-pinned, so C1's kill rule ("void if any instrument
  byte differs") bars editing it — which is why A3 is a plan-only narrowing. **A3/A4 were uncommitted in the
  working tree while this seat measured** (working-tree sha `88137e04…` vs frozen `41b15c4e…`).
- **F2** — the r95 plan (disposition 7) and the r95 lesson name r93 routed 5 as `VERDICT-INCOMPLETE`, but
  r93's own routed 5 is "Probe grammar leniency (suffix / extra components)"
  (`corpus/lessons/round-93-verifier-spotcheck.md:110`), and `VERDICT-INCOMPLETE` appears in **no** spot-check
  §6 in `corpus/lessons/` — only in the new `round-95.md`. The M12 half is right; the label has no antecedent.
- **F3** — the r95 report says the `fam_auto_probe_shapes` stderr correction "is recorded in the lesson"; it
  is not (`grep -c AUTO-PROBE-SHAPES corpus/lessons/round-95.md` → 0), and the false sentence "The stderr
  shape belongs to the gate's selftest, not this family" is still byte-identical in the r95 battery at
  `tools/limine-pin-battery-r95.py:1726` while the fixture does emit stderr (`:1718`, `:1935–1937`).
- **F4** — `.ufo/waves/round-95/w1.ready` is committed at the tip, but `w1.ready.dispatched` is **untracked**;
  rounds 84–93 track both. One `git add` at settle closes the plan's own disposition 2.
- **F5** — the plan's C2 row body still reads `status` `clean` against A2's `PASS` (readability; already
  flagged as `w1/CriticClaims.md` finding (c)).
- **F6** — the frozen copy mirrors the live plan (verifies by construction, not by freeze), and the registry
  gate and `SKILL.md` are pinned nowhere, so C2's original void clause had no referent (A4 re-binds it; the
  hole is inherited from r94's manifest).
- **F7** — `w1-spec.json`'s top-level `axes` omits `adjacency` although the ConnectorOverlap item carries it.

## 3. Freeze manifest at the current tree

`sha256sum -c .ufo/waves/round-95/before/instruments.sha256` → **9/9 OK, exit 0**.
`before/freeze-manifest.sha256` is byte-identical to `instruments.sha256` and also verifies exit 0.
The manifest names **0** live-plan entries and **1** frozen-copy entry (`before/plan-frozen.md`) — the r94
defect (a manifest that names the live plan and therefore `FAILED` at the tip) is structurally closed: the live
plan has since moved and the manifest still verifies. Residual (F6): the copy is re-pinned per amendment, so
verification is by construction; and `tools/check-registry-coverage.py` is pinned nowhere
(`grep -c` → 0), which is what A4's re-binding fixes.

## 4. r94 spot-check §6 routed items 1–10

| # | item | state | closing artifact / why open |
|---|---|---|---|
| 1 | registry rows | **closed** | `SKILL.md:5934–5937` at `a302e688`; `limine-pins` reads ``default `auto` `` and `39 fixtures`; gate `PASS 151/151`, selftest 23/23. Caveat (A4): the gate certifies presence, not content — the false cells (ReviewRegistry) sit outside C2's two certified cells |
| 2 | `.ready` bookkeeping | **half** | `w1.ready` committed; `w1.ready.dispatched` untracked (F4) |
| 3 | freeze manifest vs plan | **closed** | manifest names the copy, not the live plan; exit 0 (§3) |
| 4 | do-nothing arithmetic + stderr clause | **closed** | r95 report:78 and lesson:210 — `97/98 unmet`, stderr-only fake refused (`p.stdout` only) |
| 5 | report prose counts | **closed** | r95 report:79 — every count copied from a named artifact and re-counted before filing |
| 6 | uncited final commit `029f6629` | **closed** | named at r95 report:238 and :80; the r94 report is not rewritten (0 occurrences) |
| 7 | r93 routed-item mapping | **OPEN** | F2 — unsourced `VERDICT-INCOMPLETE` label |
| 8 | battery docstring vs fixture | **HALF** | `REFUSAL_DIGIT9` now referenced (`r95 battery:1715`); the stderr sentence is unchanged and its "lesson correction" is absent (F3) |
| 9 | coverage gaps | **closed as routed** | `<= 8` gate killed by `N05-strict-8`; the `12.9.6.1` extra-component shape stays on the Frontier (README:1147, lesson:211) |
| 10 | contested scope | **carried** | operator-owned, reported not absorbed (lesson:185, :212) |

## 5. Frontier check (round-94 bullets)

None of the three round-94 Frontier bullets is contradicted.
- The AUTO-fake leakage-disclosure paragraph and the `--usage-check` roster are **byte-identical** in the r95
  battery, so the accepted row `("999999999.0.0", 0)` survives byte-for-byte.
- That bullet is now **qualified**, not contradicted: the cap is per component, so the accepted leg is
  "X-certified only" (r95 README bullet 1; the knowledge entry's Limits) — the same fact that falsified F1.
- **No corpus reading asserts an 8-digit accepted boundary.** `raw 8-9` (SOURCES.md:394,
  limine-version-probe-r93.md:21,65) is the ChangeLog's raw **line range**; `<= 8` is a **mutant** bound
  (the r94 over-strict gate, the N05 bend, mutant M01) — never a claim about the published cap.

## 6. Wave shape and attack share

13 seats (4 executor, 2 scout, 2 scribe, 2 reviewer, 1 critic, 1 mutation-tester, 1 connector).
**Attack share 4/13 = 30.8 %** by the floor's own role list (reviewer, critic, mutation-tester, labrat —
`scripts/hyaku/lane-addendum.md`, run-15) and **5/13 = 38.5 %** by the falsification ledger's role set
(`scripts/hyaku/prefile-falsification.py:58`, which counts the connector). The **floor is ≥25 %**; the wave
meets it on both counts (3 seats would have been 23.1 %). Band 8–16 ✔, L2 floor 8 ✔, connector seats 1 ≤ 2 ✔.

{"seat":"ScoutDrift","verdict":"findings","notes":"Full report + 8 receipts in .ufo/waves/round-95/w1/ScoutDrift/. claims.json vs before/plan-frozen.md: every divergence is a recorded amendment (A1/A2 in the frozen copy; A3/A4 in the live plan), no unrecorded drift; the frozen copy is a byte-identical mirror of the live plan, re-pinned per amendment. FINDINGS: F1 (high) frozen claims.json C1 predicate still says 'the largest in-bound member', falsified by ReviewBattery F1 (cap is per component; 999999999.999999999.999999999 in-bound and accepted); claims.json is manifest-pinned so C1's kill rule bars editing it, and A3/A4 were UNCOMMITTED in the working tree at measurement. F2 r95 plan/lesson name r93 routed 5 as VERDICT-INCOMPLETE but r93's routed 5 is 'Probe grammar leniency' and that token appears in no spot-check section 6. F3 the r95 report says the fam_auto_probe_shapes stderr correction is in the lesson; it is not (grep -c AUTO-PROBE-SHAPES corpus/lessons/round-95.md = 0) and the false sentence is byte-identical in the r95 battery at :1726. F4 w1.ready.dispatched untracked while rounds 84-93 track both. F5 plan's C2 row body still reads 'status clean' vs A2's PASS. F6 frozen copy mirrors the live plan (verifies by construction) and the registry gate/SKILL.md are pinned nowhere, so C2's original void clause had no referent (A4 re-binds; inherited from r94). F7 w1-spec axes omits adjacency although ConnectorOverlap carries it. MEASURED: sha256sum -c before/instruments.sha256 = 9/9 OK exit 0; freeze-manifest byte-identical and also exit 0; 0 live-plan entries, 1 frozen-copy entry, so the r94 manifest-FAILED defect is structurally closed. r94 routed 1-10: 1 closed, 2 half, 3 closed, 4 closed, 5 closed, 6 closed, 7 OPEN, 8 half, 9 closed-with-Frontier-carry, 10 carried. FRONTIER: no round-94 bullet contradicted; leakage paragraph and usage roster byte-identical; the 999999999.0.0 accepted row survives byte-for-byte, now qualified as X-certified-only (same fact as F1); no corpus reading asserts an 8-digit accepted boundary ('raw 8-9' is the S383 ChangeLog raw line range, '<= 8' a mutant bound). WAVE: 13 seats; attack share 4/13 = 30.8% (floor's role list) and 5/13 = 38.5% (ledger role set) against the >=25% floor in scripts/hyaku/lane-addendum.md run-15 - met on both counts; band 8-16 OK, L2 floor 8 OK, 1 connector <= 2. No tool installed or upgraded (pacman paused host-wide); python3 3.14.8, git 2.56.0; scratch deleted; no mutating git/jj command; no instrument edited."}
