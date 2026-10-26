VERDICT: draft
# CritTrendFinal — round 43, wave w2 (falsify): the three LEARNING.md trend verdicts

Item N-9 (draft of the round-43 trend verdicts at tip `8acf0b02`):
**expansion unchanged; quality improved iff the C2 counted reads hold (else harmed-provisional unless marked before closure); discernment unchanged (outside spot-check still owed).**
Vocabulary per LEARNING.md:28-29 (improved / harmed / unchanged / unprovable-but-better). Assumption per the item: C1 PASS (verified by the C1 seats of this wave; I did not run the heavy C1 counter). C2 is left conditional on the counted reads; both branches are given.

## Assumptions and scope

- Lane tip under test: `8acf0b022586a0f3164c77659fb96ba5f90949b6` (round-43 w2 spec/dispatch commit). Base `6951ead90566b2d74f7c45b4efca29246badad64`.
- Trend table read from the fleet `LEARNING.md:31-35` (expansion/quality/discernment observables and improved/harmed conditions), vocabulary at `:28-29`, the "growth without quality is a trade" rule at `:37-38`, and the outside-check rule at `:40-48`.
- The only knowledge change from base to tip is the new entry `corpus/knowledge/btrfs-scrub-record-r43.md` (+154 lines) plus a one-line supersession pointer appended to `corpus/knowledge/btrfs-scrub-record-r42.md` (header) — `git diff --stat 6951ead9 8acf0b02` shows no other `corpus/knowledge/` change. C1 is a tool repair (`tools/boot-chain-audit.sh`), not an admitted knowledge entry. So the round's learning signal rests on the r43 entry (and on how it treats the r42 entry's withdrawn/narrowed rows).

## Expansion — unchanged

The r43 entry is **not** admitted on uncovered coverage-map ground; it deepens a held line.

1. The scrub-record line is held by the coverage map before this round: the round-26 Frontier notice introduces storage integrity as a frontier area (`corpus/README.md:241-244`), and the round-42 coverage note already holds the scrub-record surface with a row for `knowledge/btrfs-scrub-record-r42.md` (`corpus/README.md:406-414`, "round 42 deepens it from source, it does not enter new coverage-map ground"). The r43 entry's own scope line says the same: "Scope: the storage-integrity frontier, scrub record line (`PROVINCE.md` Frontier; `corpus/README.md` `## Frontier`)" (`btrfs-scrub-record-r43.md:9-10`).
2. The tip's authoritative round-43 coverage note closes the question explicitly: "Frontier: the scrub record stays Frontier (no census arm reads it); round 43 re-grounds it from source and adds the kernel-side privilege fact (S240), it enters no new coverage-map ground" (`corpus/README.md:424-425`). PROVINCE's round-43 note repeats it: "The scrub record stays Frontier … The promotion condition (a read-only census arm) is unchanged" (`PROVINCE.md:245-253` at tip). No Frontier→Core move and no SCORECARD capability row were added.
3. S240 is a new source row (Linux `fs/btrfs/ioctl.c`, `mined` at entry, SOURCES row S240) and it grounds a fact not previously held as verified (the w1 novelty seat C2CritNovelty confirms the SR6 mechanism tokens are absent at base outside the uncounted corrections). But "new kind of source" is only an **observable** feeding expansion; the improved condition is conjunctive: "net new admitted entries on uncovered ground, each citing its coverage-map row" (`LEARNING.md:33`). The entry's ground (scrub record) is covered; the kernel-side fact is a deeper statement about the same held line, not a new surface. This is the overclaim the item asks me to attack: adding a newly sourced fact to a held frontier line is depth (quality signal), not expansion.
4. Harm branch: no admitted entry fails the bar it was admitted under this round (the only admission candidate is the r43 entry; its gate is C2 below). So expansion is not harmed either.

## Quality — improved iff C2 PASS; if C2 FAIL, not improved, harmed unless marked before closure

The improved condition requires "a weaker entry is superseded by a stronger one, or stale entries re-verify, with no admitted entry failing its re-check" (`LEARNING.md:34`).

- Supersession side (holds regardless of the counted reads): the r43 entry re-grounds the r42 entry's withdrawn SC1/SC3 text and the SC4 running-state narrowing as SR1/SR3/SR6, each against pinned source lines (`btrfs-scrub-record-r43.md:10-13`; r42 header pointer "superseded-in-part: round 43"; lesson `round-43.md:36-62` records the L1's per-adopted-sentence source-line check — the "Entry gate (C2)", QUALITY 91). The w1 novelty seat's epistemic point stands: the r42 corrections "carry no counted verdict" and were never read by a counted seat (`btrfs-scrub-record-r42.md:170-175`), so the r43 rows are the first counted, quote-bound, digest-checked statement — a weaker statement superseded by a stronger one.
- The false/stale predecessor content is **marked**, not left unmarked: the r42 corrections section, the r42 header pointer, the README/PROVINCE/SKILL pointers all closed by this round (lesson `round-43.md:75-85`, considerMap; `PROVINCE.md:245-253`). So no "found false and left unmarked" harm exists for the predecessor.
- Re-check of the admitted candidate (the conditional): the frozen counter at tip `8acf0b02` exits 1: `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, novelty_base_hits 0, pointer_ok 1, verdicts_ok 0` — every conjunct holds except `verdicts_ok`, which counts only this wave's six counted C2 seats (C2RevSR1/3/6, C2CritSR1/3/6) and is 0 because those reads are in flight (receipt `CritTrendFinal/c2-counter-at-tip.json`).
  - **Branch C2 PASS** (all six counted verdicts hold → `verdicts_ok 3`): the r43 entry passes its re-check, no admitted entry fails its re-check, and the weaker→stronger supersession stands → **quality improved**.
  - **Branch C2 FAIL** (any bound `fails`, `partly` without residual `holds`, or unbound counted seat — the declared kill rule): the r43 entry fails its re-check. Then quality is **not improved**; per `LEARNING.md:34` it is **harmed** if the failure is left unmarked at closure (the round would close `rejected-honest-stop` like round 42, which is the marking path), and otherwise stays pending/unchanged until the failing text is withdrawn or corrected like round 42's SC1/SC3.

## Discernment — unchanged (no outside check yet)

- The improved branch requires the outside spot-check to agree with the gate on admits *and* rejects, or a disagreement to become a lesson adding a grounded QUALITY criterion (`LEARNING.md:35`). The round-43 lesson's Spot-check section is "Pending the non-author closure" with only candidates named (`round-43.md:87-89,129-133`); there is no `corpus/lessons/round-43-verifier-spotcheck.md` (the only round-43 lesson file is `round-43.md`). The six counted C2 reads are lane-dispatched seats — "A subagent the lane dispatched is still the lane" (`LEARNING.md:45-46`) — so they are not an outside check.
- Harm branch: `corpus/QUALITY.md` is unchanged from base to tip (`git diff 6951ead9 8acf0b02 -- corpus/QUALITY.md` empty), so no criterion was added without a lesson, and no disagreement is left unlearned because none has been recorded yet. → **unchanged**, provisional on the non-author closure (a later disagreement could still move it, per `LEARNING.md:40-48`). It is not `unprovable-but-better`: that vocabulary requires a named non-author reviewer judging the change better with reasons on record (`LEARNING.md:46-48`), which does not exist for round 43.

## Answers to the item's three attacks

1. "Is the r43 entry 'uncovered coverage-map ground' (expansion) or deepening (quality)?" — Deepening. Evidence: coverage-map row for the scrub record exists since round 42 on a frontier line held since round 26 (`corpus/README.md:241-244,406-414`); tip texts explicitly state "it enters no new coverage-map ground" (`corpus/README.md:424-425`; `PROVINCE.md:245-253`); the entry scopes itself to the scrub-record line; S240 adds a kernel-source-grounded fact inside that held line. Any claim that the r43 entry is expansion ground is an overclaim.
2. "Did any admitted entry fail its re-check?" — The only admission candidate (r43 entry) has its re-check (the frozen C2 counter) in flight: at tip, all conjuncts but `verdicts_ok` hold; the counted reads determine it. Branch C2 PASS → none fails; branch C2 FAIL → the entry fails, and quality follows the harmed/unchanged branch above. The predecessor r42 entry's false rows are marked, not left unmarked.
3. "Does the discernment trend have an outside check yet?" — No. See Discernment above.

## What I did not do

- Did not run the heavy C1 counter (taken as PASS per the item; the C1 seats measure it).
- Did not run or read the six counted C2 verdict seats (they were in flight; the branches above cover both outcomes).
- No host mutation, no git/jj mutation, no lane file edits except this report and its receipt; scratch held under `/fast/scratch/hyaku/tsukuroi-r43/CritTrendFinal/` and removed at exit (receipt copied to `w2/CritTrendFinal/`).
- Installs: none (no tooling change needed).
