# R49CritAdjB — C2-B7: are the ten OUT anchors still the best locators?

VERDICT: supports

The anchor set is still true. All ten `OUT-0NN` quotes are present verbatim at today's
sibling tips, at the same line number as their pins, once per file, under the same
title heading, and every pin is an ancestor of its tip (append-only drift). Nine rows
need no change; `OUT-009` keeps its pin and the *ownership question* stays with the
owner (protocol integrator) per the R20 correction. Nothing is re-pinned.

Measured at **2026-10-28T17:17:49Z** (`date -u`) against lane freeze
`55c07cd3f8bff2e12117c34d57b4c618de74d85c`. Receipts:
`.ufo/waves/round-49/w1/R49CritAdjB/adjacency-drift-r49-b7.json` (per-row machine
record) and `.../commands-r49-b7.txt` (commands and observed output).

## Method (all read-only; no lane or sibling mutation)

- Pins, digests and the published quote/heading text: `git -C
  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 55c07cd3:PROVINCE.md`
  — anchor table `PROVINCE.md:121-130`, limits paragraph `:132`, portable digests
  `:134-146`, R20 correction `:148-152`.
- Tip of each recipient: `git -C …/<sib>-shokunin rev-parse HEAD`.
  `rev-parse --abbrev-ref HEAD` returns `HEAD` (detached) in all eight sibling repos,
  so the branch name is not the locator; the branch tips agree with the detached HEAD
  (mori/kama/kagi/mado/kumitate/tameshi on `master`, kaidoku/revenger on `main`).
- Quote located in today's bytes: `git -C …/<sib>-shokunin show <tip>:PROVINCE.md`,
  exact-substring match, counted, and line-numbered.
- Pin reachability: `git -C …/<sib>-shokunin merge-base --is-ancestor <pin> <tip>`.
- Meaning drift: `git -C …/<sib>-shokunin diff <pin>:PROVINCE.md <tip>:PROVINCE.md`,
  with each deletion inspected, plus a class-context read of the tip preamble.
- Pin portability: `sha256(git show <pin>:PROVINCE.md)` compared with the digest the
  lane publishes at `PROVINCE.md:137-146` — **10/10 MATCH**.

## The ten rows

`quote at tip` = yes (verbatim, exactly once) / no / moved. Line = pin→tip.
`ADJ class at tip` cites the recipient's own tip bytes.

| Anchor | ADJ | Sibling file @ pin | Pin → tip | Commits since pin | Quote at tip | Line | ADJ class still in tip file | Recommend |
|---|---|---|---|---|---|---|---|---|
| OUT-001 | Core | `mori-shokunin/PROVINCE.md` @ `91940fa339e3` | `91940fa339e3` → `325f7e639916` | 503 | yes | 9→9 | yes — mori owns kill/OOM journal classes + cgroup `memory.events`; its `tip:13` still refuses OS package/systemd/driver/boot to tsukuroi | keep pin |
| OUT-002 | ADJ-01 | `kama-shokunin/PROVINCE.md` @ `e75cf680b534` | → `7ee8cbdf160f` | 400 | yes | 12→12 | yes — `served-model-id reconciliation` row intact; `tip:44` keeps the boundary “is the thing at this baseURL the model this config believes it is” and refuses only model *quality* | keep pin |
| OUT-003 | ADJ-02 | `kagi-shokunin/PROVINCE.md` @ `c2cab35bc92e` | → `69b61db46be4` | 63 | yes | 3→3 | yes — domain line unchanged; `tip:10-17` round-18 erratum (janitor substrate absent) predates the pin | keep pin |
| OUT-004 | ADJ-03 | `mado-shokunin/PROVINCE.md` @ `a4046a821608` | → `3b55b6e91e40` | 380 | yes | 6→6 | yes — config plane unchanged; `tip:34` “unit-state rows sit next to tsukuroi's unit-health ground, which stays tsukuroi's”; `tip:96` cites OUT-004 directly | keep pin |
| OUT-005 | ADJ-04 | `mori-shokunin/PROVINCE.md` @ `91940fa339e3` | → `325f7e639916` | 503 | yes | 8→8 | yes — `tip:25` same-boot journal-window probe now recorded as admitted round 16 (strengthened, not narrowed) | keep pin |
| OUT-006 | ADJ-05 | `kumitate-shokunin/PROVINCE.md` @ `1770305fae20` | → `14057f3e3899` | 285 | yes | 3→3 | yes — domain line unchanged (`tip:3`) | keep pin |
| OUT-007 | ADJ-05 | `mori-shokunin/PROVINCE.md` @ `91940fa339e3` | → `325f7e639916` | 503 | yes | 12→12 | yes — `tip:12` still refuses dispatch/orchestration mechanism → kumitate | keep pin |
| OUT-008 | ADJ-06 | `kaidoku-shokunin/PROVINCE.md` @ `d1d981d2cc04` | → `c0112995817b` | 332 | yes | 3→3 | yes — `tip:3`; `tip:125` confirms “Full-system upgrades go through tsukuroi-shokunin's update-safety gate first” | keep pin |
| OUT-009 | ADJ-06 | `revenger-shokunin/PROVINCE.md` @ `cf02419276e5` | → `6defe31e4af9` | 104 | yes | 3→3 | yes as a locator — but tsukuroi's own R20 correction (`PROVINCE.md:148-152`) supersedes its “Revenger owns” proposition, and kaidoku `tip:3` still declares the same RE scope | hand to the owner (pin unchanged) |
| OUT-010 | ADJ-07 | `tameshi-shokunin/PROVINCE.md` @ `01d586ddbc5f` | → `9cf0146b94dd` | 401 | yes | 7→7 | yes — `tip:14` still refuses product domains and keeps “the reusable craft” | keep pin |

Totals: quote at tip 10/10 yes, 0 no, 0 moved; pin digest 10/10 match; pin ancestor
10/10 true; recommendations 10 × keep pin (OUT-009 additionally handed to the owner
for the ownership question, not for the locator).

## Strongest counterexample attempted

**Hypothesis:** a pin 400–500 commits behind (mori) cannot still be the *best*
locator; the drift must eventually reword the sentence, relocate it, or change the
recipient's class, at which point the pin becomes a historical relic and the row needs
`re-pin` or an owner handoff.

**Test and result — refuted on the available evidence.**

- The largest drift is mori +362/−7 (121 → 476 lines) and kaidoku +273/−5
  (162 → 430). Every deletion in each pin→tip diff was inspected; none touched a
  quoted line, and all ten quotes occur exactly once at the tip.
- Line position is unchanged in all ten (§ table). No `##` heading intervenes before
  any quote (first `##` after the quote in every file: mori 20, kama none, kagi 8,
  mado 86, kumitate 8, kaidoku 38, revenger none, tameshi 22), so the recorded
  `Heading` is still the enclosing section.
- The class, not just the string, survives: each recipient's tip either keeps the
  ownership sentence (all ten) or adds a reciprocal statement that agrees with the
  ADJ boundary — mori refuses OS state to tsukuroi (`tip:13`), mado keeps unit health
  tsukuroi's (`tip:34`), kaidoku routes upgrades to tsukuroi (`tip:125`), tameshi
  refuses product domains and calls gate ownership unchanged (`tip:14`).
- Pins were not orphaned by history rewrites: `merge-base --is-ancestor <pin> <tip>`
  returned 0 for all ten, so the drift is additive on the same line of development
  and the lane's `_live_object_hash` reachability leg still holds.

**Second counterexample (a live one):** the tip is a moving target. tameshi's `HEAD`
moved *during this seat* from `631cd645` to `9cf0146b94dd`; OUT-010 resolves at line 7
on both. That is the design working — the pin is immutable, the tip is not — and it is
why no row should be re-pinned to a tip.

## Scope limit the C2 predicate cannot see

No counter in the lane tests tip drift, and this is consistent with the claim, not a
defect in it:

- `tools/check-adjacency-anchors.py` checks the quote and heading against the lane's
  committed snapshot (`record["snapshot"]`, `:615-646`) and computes the registry
  digest from `git show <sibling_commit>:<path>` (`:456`) — pinned bytes only.
  `tools/check-adjacency-table-r49.py:13` calls the live-sibling leg “a cross-check,
  never the only leg”, and that leg resolves the *pinned* commit.
- The lane's last recorded tip re-read is
  `corpus/knowledge/adjacency-recheck-2026-10-19.md` (fleet round 1). This report is
  the current one; the pin table above supersedes its 8-sibling table for today.

So `C2` proves the locators resolve against the frozen bytes and the registry digests;
it cannot prove they are still true at the recipient. This table supplies that leg and
does **not** move the predicate (`adj_rows == 7 and linked_rows == 7 and bare_ranges ==
0 and anchors_ok == 7 and registry_ok == 7 and anchors_checker_rc == 0` remains the
right gate for the anchor *mechanism*).

## Sources & frontier — adjacency drift check (section for the round-49 report)

This is the round's adjacency drift check; the ten-row table above and the two receipts
(`.ufo/waves/round-49/w1/R49CritAdjB/adjacency-drift-r49-b7.json`,
`.../commands-r49-b7.txt`) are its evidence. Items 1–5 are named Frontier ground, not
claims of ownership or repair authority; none of them moves the C2 predicate.

1. **mori re-pinned and the lane's register is stale.** Mori `tip:66` now cites
   `../tsukuroi-shokunin/PROVINCE.md:8-14`; the re-pin landed at mori `af42101d`
   (2026-10-22, “round-30: routed R7 — PROVINCE stale statements fixed…”). Lane
   8-14 is the owns paragraph, so mori's claim resolves. But the lane's OV2 row
   (`PROVINCE.md:185` @ freeze) still reads “lane PROVINCE lines now 30-33 and 44-53;
   mori re-pins” — superseded bookkeeping. Also mori `tip:288` cites lane `:30-33`,
   which resolves exactly to “fleet correlation belongs to mori”.
2. **Recipient-side use of the anchors.** mado `tip:96` cites “tsukuroi's OUT-004
   routes only this file's lines 3–16”; OUT-004's pinned quote is at mado line 6,
   inside that range — the anchor is being consumed and still matches.
3. **Shared read-only evidence, not contested ownership.** kama names
   `systemctl --user status qwen-coder` as serving evidence (`kama tip:28`) and mado runs
   `systemctl --user is-active` in its own verify script, while tsukuroi retains
   user-unit state. Both siblings are read-only and neither claims unit diagnosis;
   ADJ-01/ADJ-03 wording should not be read as exclusive probe rights.
4. **kagi's substrate is absent** (`tip:10-17`, round-18 erratum, already true at the
   pin). ADJ-02's class stands, but a live helper permission/auth-flow finding may
   have no installed helper to examine — a host fact, not anchor drift.
5. **Lane-side line ranges still resolve** at freeze. `PROVINCE.md:33` cites mori
   `:6-16`; the owns/refuses preamble at mori `tip:6-16` is exactly that content.
   `PROVINCE.md:166` cites mori `:26`; mori `tip:26` is the `SURFACE disk` /
   `SURFACE cgroup` resource-runway bullet.

## Impacted axes

- **adjacency** — no change required; the ten rows hold. New drift receipt recorded.
- **C2** — premise holds and the predicate is untouched; one stale OV2 register line
  observed but outside the ADJ ownership cells and outside the anchor section.
- **drift** — refreshed from 2026-10-19 to 2026-10-28; the only re-pin in the family
  is mori's inbound pointer to the lane.
- **frontier** — items 1–4 above are named ground, not claims.

## Smallest safe correction

1. **No lane byte change for C2.** Do not re-pin: the pins are ancestors, digests
   match, quotes are stable at the same lines, and re-pinning would force a registry
   digest update plus an anchors-checker re-verification with no locator gain.
2. **Record this table in the round-49 report's Sources & frontier section** with the
   two receipt paths above. It is the round's adjacency drift check.
3. **OUT-009:** locator unchanged; the ADJ-06 *recipient* remains unresolved and is
   already routed to the protocol integrator by `PROVINCE.md:148-152`. Do not let the
   valid locator be read as an ownership grant.
4. **Optional, separate from the frozen claims:** if the L1 wants OV2 closed, the
   smallest edit is one appended line *after* the round-27 register (e.g. below
   `PROVINCE.md:189`, outside every C2-checked cell) stating “OV2 resolved: mori
   re-pinned at `af42101d` to `PROVINCE.md:8-14` (owns paragraph)”. Deferring it costs
   nothing and keeps the round's byte scope clean.

## Not done

- The C1/C2/C3 counters and their `--selftest` arms were **not run** — this item's
  execution class authorizes only the named read-only git commands, so no counter
  measurement is claimed here.
- Sibling additions were read through pin→tip diffs plus class-context reads, not a
  full read of every added section; the quoted class and reciprocal boundary
  statements were read in full at each tip.
- Tips are as of the single observation instant; any sibling commit after
  2026-10-28T17:17:49Z is outside this receipt.
