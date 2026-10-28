VERDICT: supports

Seat R49RevAdjA — C2-B4, semantic review of the ADJ → OUT remap in `PROVINCE.md`.
Bytes under test: lane `tsukuroi-shokunin`, freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c`,
base `6256760d1382ce4ce20fcba830d4b2912cfbf12b`. All lane bytes read with
`git -C …/tsukuroi-shokunin show <rev>:<path>`; nothing in the lane was written, staged or checked
out. Scratch: `/fast/scratch/hyaku/tsukuroi-r49/R49RevAdjA/` (removed at the end). Receipts:
`.ufo/waves/round-49/w1/R49RevAdjA/{receipt-locators.tsv,receipt-checks.tsv,receipt-pointers.tsv,pinned-PROVINCE.md.txt}`.

## 1. Answer in one paragraph

The remap is semantically **correct and locator-preserving**: for each of the seven rows, the old
ownership cell carried exactly the range string(s) that the cited anchor's registry
`province_pointer` still carries (`receipt-locators.tsv`, column `locator_preserved` = True for
7/7; every other cell byte-identical). So each cell now names the round-19 anchor whose provenance
*is* the old locator — no pointer was dropped, widened or narrowed, and no class, recipient or
handoff-evidence cell moved. Every quoted sentence exists verbatim once at its cited pinned line,
and every pinned commit resolves with the registry sha256 (`receipt-checks.tsv`). Six of the seven
rows are also semantically supported by the quoted sentence itself. **ADJ-04 is the one row whose
quoted sentence carries only half of the recipient's need** (the kill half; the host-pressure /
fleet-correlation half is carried by mori's preamble but not by OUT-005's quote), and OUT-001 — the
Core pointer that names fleet correlation — is neither cited nor *citable* in that cell under the
counted predicate. Details and exact proposed text in §4.

## 2. Checks run (read-only)

1. `git -C … diff 6256760d… 55c07cd… -- PROVINCE.md` — the diff touches only the seven last cells
   plus one appended `## Round 49` section (lines 297-320); the anchor table (108-146) and its rows
   are unchanged; no bare `*.md:N[-M]` survives in any ownership cell (all seven cells are
   `` `OUT-00N` `` lists).
2. For each anchor row (PROVINCE.md:121-130): pinned commit exists in the sibling repo, blob
   sha256 equals the registry `sibling_blob_sha256`, and the ≤25-word quote is an exact substring of
   the cited line — `receipt-checks.tsv`: `quote_hits_pin=1` for all ten; quote lines
   9/12/3/6/8/3/12/3/3/7 respectively. Word counts 17/9/11/6/7/12/9/11/6/9 (all ≤25).
3. Old-vs-new locator identity per row via the registry `province_pointer`
   (`receipt-locators.tsv`).
4. Every one of the ten registry `province_pointer` strings still occurs in the frozen PROVINCE.md
   (`receipt-pointers.tsv`): OUT-001's only at line 33 (the retained Core pointer paragraph,
   `../mori-shokunin/PROVINCE.md:6-16`), OUT-002..OUT-010 only inside the new Round-49 note
   (lines 301-305). **That restatement in the note is load-bearing**: `check-adjacency-anchors.py`
   fails `ANCHOR-POINTER-MISSING` (line 635) when a registry `province_pointer` no longer appears in
   `PROVINCE.md`, and the seven cells used to be the only home of those strings. Removing the note
   would turn C2's `anchors_checker_rc == 0` leg red.
5. Quote survival at the siblings' current tips (`receipt-checks.tsv`, `quote_hits_tip`): all eight
   sibling repositories have moved past their pins (mori 325f7e639916, kama 7ee8cbdf160f, kagi
   69b61db46be4, mado 3b55b6e91e40, kumitate 14057f3e3899, kaidoku c0112995817b, revenger
   6defe31e4af9, tameshi 9cf0146b94dd), yet all ten quotes still occur once, at the same line
   numbers. The anchors are therefore currently *operative* declarations, not only historical
   snapshots — which is what the ADJ rows need. (Sibling repos are live; one tip moved between two
   of my own calls, so treat tips as "observed at read time".)
6. Read both checkers at the freeze to know what the counted legs can and cannot decide:
   `tools/check-adjacency-table-r49.py:140-160` (per-row: anchor exists, `anc[1] != row_id`,
   sibling/heading/quote shape, registry hex) and `tools/check-adjacency-anchors.py:447-461`
   (`_live_object_hash`), `:560-652` (outbound record validation, snapshot digest, heading/quote
   containment, `province_pointer` presence, publication) — see §4-F2 for what the "live" leg
   really does.

Not run (and therefore not claimed): the two counters themselves
(`python3 tools/check-adjacency-table-r49.py --revision …`, `tools/check-adjacency-anchors.py
--revision …`) and any `--selftest`; my item authorizes no command beyond the diff review and the
pinned-quote reads, so I re-derived their legs from source instead of re-running them. No edits of
any kind were made.

## 3. Per-row semantic verdict (does the quoted sentence carry the recipient's ownership?)

| Row | Recipient need (trigger) | Cited anchor(s) | Sibling sentence at the quoted line | Verdict |
|---|---|---|---|---|
| ADJ-01 | served-model identity / endpoint wrong | OUT-002 (kama @ e75cf680b534:12) | kama:12 is the artifact cell `GET /v1/models` vs `--alias` vs the configured model id` of the **Owns (surfaces)** row whose surface label is `served-model-id reconciliation` (same line); kama:3-4 Domain "local model serving & endpoint health — … served-model reconciliation". | **supported** (quote is a method fragment; the ownership verb is the same table row's surface label + Domain line, both inside pointer 3-24) |
| ADJ-02 | credential-helper permission / auth-flow question | OUT-003 (kagi @ c2cab35bc92e:3) | kagi:3 "**Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence"; kagi:5 Owns "the domain knowledge … above"; surfaces carry the modes (600/644, `janitor_auth`). | **supported** for the hygiene/permission half; auth-flow ownership is stated literally at kagi:63 ("kagi owns runtime auth and credential custody"), which is **outside** OUT-003's ranges 3-6,10-17,32-34,54 (F3) |
| ADJ-03 | rendering / bindings / menu / idle, config-level | OUT-004 (mado @ a4046a821608:6) | mado:6-9 one sentence: "**Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules, animations), `~/.config/waybar/`, `~/.config/walker/`, … screen/idle behavior (hypridle/hyprlock where present)"; mado:3-4 Domain "desktop & compositor craft … and display behavior". | **supported** (bindings=keybinds; menu=walker; idle=hypridle/hyprlock; rendering=display behavior; all inside 3-16). Quote truncates the sentence mid-parenthetical, so `menu`/`idle` are not visible in the quote cell (F6) |
| ADJ-04 | host pressure **or** kill signal **→ fleet/wave attribution, liveness or progress correlation** | OUT-005 (mori @ 91940fa339e3:8) | mori:8 "kill/OOM-related catalog-ID records and signal-11 coredump records". The needed declarations are mori:3-4 Domain ("fleet & host observability … whether the fleet, its waves and its host are alive and progressing"), mori:6-7 (watchdog liveness, `.ufo/waves/*` settlement), mori:10 (resource runway, lane-silence grading) — all **inside pointer 3-16**, none inside the quote. | **partially/formal-only** — right owner, right bytes by range, but the quoted sentence carries only the kill-evidence half; the attribution half rides the tsukuroi proposition. See F1 |
| ADJ-05 | task/hub dispatch, routing, orchestration semantics | OUT-006 (kumitate @ 1770305fae20:3), OUT-007 (mori @ 91940fa339e3:12) | kumitate:3 "**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime"; mori:12 "**Refuses:** dispatch and orchestration mechanism (→ kumitate)"; corroborating sibling sentence mori:65 "kumitate | Owns OMP task/hub orchestration and wave plan/run/record/collect semantics". | **supported**; "dispatch" is explicit in OUT-007 and routes to kumitate. The literal word "routing" appears in neither quoted sentence (kama:41 has "dispatch/route mechanism (kumitate)") — F4 |
| ADJ-06 | driver/firmware/package mechanism needs shipped-artifact RE | OUT-008 (kaidoku @ d1d981d2cc04:3), OUT-009 (revenger @ cf02419276e5:3) | kaidoku:3 "**Domain:** reverse engineering of shipped artifacts with REA on this Linux"; kaidoku:5 "…archives and packages"; revenger:3 "Owns: reverse engineering of shipped artifacts" with line 4 enumerating "…Android APKs, archives, **firmware**". | **supported** as a pair: packages from kaidoku, firmware from revenger's sentence (line 4, inside 3-7). OUT-009's proposition is partly superseded by the in-document R20-OUT009 note (PROVINCE.md:148-152); ADJ-06's recipient cell already says the ownership is unresolved — F5 |
| ADJ-07 | census blind spot → reusable verification / mutation-testing question | OUT-010 (tameshi @ 01d586ddbc5f:7) | tameshi:7 "**Owns:** the method, documented from the fleet's existing gates as primary surfaces"; tameshi:3-5 Domain "verification-fixture craft — the reusable method of honest checks: hermetic suites, **mutation testing**, fail-closed arms…"; tameshi:14-17 "every lane's gate remains its own". | **supported** (the quote's "the method" is deictic; its antecedent is the Domain lines 3-5, inside pointer 3-18, and 14-17 matches the row's "not transfer of gate ownership") |

No row is misrouted: no wrong sibling, no wrong finding class, no widening or narrowing. The
cardinality of the old cells is preserved (1,1,1,1,2,2,1 anchors). OUT-001 is the only anchor no
ADJ row cites, which is by design ("OUT-001 is the Core pointer", PROVINCE.md:113) — see F1 for the
one place that costs semantics.

## 4. Findings

### F1 (LOW, actionable) — ADJ-04's correlation half is anchored only through the un-cited Core pointer OUT-001

Evidence. ADJ-04's trigger is "Host pressure or a kill signal needs fleet/wave attribution,
liveness or progress correlation" (PROVINCE.md:49). Its only cited anchor is OUT-005, whose quote is
`kill/OOM-related catalog-ID records and signal-11 coredump records` (mori:8) — an evidence-class
sentence. mori's own sentence for the other half of the trigger is the Domain line
"fleet & host observability (森) — whether the fleet, its waves and its host are alive and
progressing" (mori:3-4), and mori:6-7 add watchdog liveness / wave settlement; neither is quoted.
The claim that "fleet attribution is its correlation" exists only in OUT-005's **proposition**, and
the anchor section's own Limits rule says "the quoted words are the sibling's, attributed to it,
never a tsukuroi assertion of sibling authority" (PROVINCE.md:132). The Core-pointer paragraph
immediately above the table is exactly the sentence that carries it in tsukuroi's own voice —
"fleet correlation belongs to mori (`../mori-shokunin/PROVINCE.md:6-16`)" (PROVINCE.md:32-33) — and
its portable form is OUT-001 (quote = journals + cgroup `memory.events` + same-boot window,
mori:9; proposition = "fleet correlation of host pressure is mori's, not OS triage"). ADJ-04 does
not cite OUT-001; `OUT-001` occurs in PROVINCE.md only at :113 (prose), :121 (anchor row) and :137
(digest).

Why it cannot simply be added to the cell. `check-adjacency-table-r49.py:157` requires an anchor's
own ADJ-row cell to equal the citing row (`if anc[1] != row_id:`). OUT-001's ADJ-row cell is
`Core` (PROVINCE.md:121), so writing `` `OUT-005`, `OUT-001` `` into ADJ-04 would yield
`anchors_ok == 6` and fail C2's predicate with the per-row problem "OUT-001 points at 'Core', not
ADJ-04". I did not run the counter (not authorized in this item); the conclusion is read off the
checker source at line 157. Re-labelling OUT-001's cell `Core` → `ADJ-04` would make the counter
pass but misstate the anchor table's documented meaning (PROVINCE.md:110-113) and is not
recommended. Adding a new `OUT-011 | ADJ-04` anchor is the only structural repair, and it would
require a matching outbound entry in the frozen round-19 pointer census
(`.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json`) or the re-checker fails
`OUTBOUND-CENSUS-UNKNOWN`/`OUTBOUND-POINTER-MISMATCH` (check-adjacency-anchors.py:580,584) — i.e.
rewriting a capture. So the cheap, harm-free repair is prose.

Exact proposed text (append to the `## Round 49` note, after PROVINCE.md:320; it lands outside the
ADJ table, so `adj_rows`/`linked_rows`/`bare_ranges`/`anchors_ok`/`registry_ok` are untouched, and
it adds no registry `province_pointer` change, so `ANCHOR-POINTER-MISSING` is unaffected):

```
ADJ-04 note (anchor semantics). OUT-005 quotes mori's kill/OOM half only. The other half of
ADJ-04's trigger — host pressure and fleet/wave attribution — is mori's by the Core pointer
retained above (`../mori-shokunin/PROVINCE.md:6-16`, PROVINCE.md:30-33) and by its portable form
OUT-001, whose quote carries the journals/`memory.events` evidence and whose proposition names
fleet correlation of host pressure. ADJ-04's cell does not name OUT-001 because OUT-001's ADJ-row
cell is `Core` and `tools/check-adjacency-table-r49.py` requires every cited anchor's ADJ-row cell
to name the citing row. Mori's own bytes keep kernel-OOM event-time attribution and fleet
correlation in Frontier (mori `PROVINCE.md` @ `91940fa339e3`:44), so an ADJ-04 handoff asks for
correlation of retained evidence, never an attribution verdict.
```

The last sentence is not padding: mori:44 says "Kernel OOM event-time attribution and fleet
correlation" are **Frontier (FR1)**, with "a host record alone does not prove a fleet-caused kill".
ADJ-04's handoff-evidence cell already asks for correlation only ("Request correlation, not a claim
that a wave caused OOM"), so the row is internally consistent; recording the frontier qualifier
stops a later reader from reading OUT-001's proposition as a held capability.

If a future round ever relaxes the ADJ-row equality, the minimal cell change would be
`| ADJ-04 | … | mori | … | \`OUT-005\`, \`OUT-001\` |` — recorded here only so the option is not
re-discovered; it fails today.

### F2 (INFO) — the new note overstates what the anchor re-checker verifies

PROVINCE.md:319-320 (added by this round) says the existing `tools/check-adjacency-anchors.py`
"still re-checks the anchors against the live sibling bytes". What that file actually does:
`_live_object_hash` (check-adjacency-anchors.py:447-461) runs
`git -C <sibling>-shokunin show <pinned commit>:PROVINCE.md` and compares its sha256 with the pin;
a mismatch only increments `live_object_match` (lines 648-652) and is **never a finding**, and the
sibling's tip is never read. So `anchors_checker_rc == 0` cannot detect post-pin drift; that stays
the Limits rule's job ("the pins are stale by design once a sibling commits again",
PROVINCE.md:132). Practically the risk is nil today — all ten quotes still resolve at the current
tips (§2.5) — so this is a wording accuracy point, not a live defect.

Exact proposed replacement for the parenthetical at PROVINCE.md:319-320:

```
(the existing `tools/check-adjacency-anchors.py` re-reads each anchor's pinned commit from the
sibling repository and only counts a `live_object_match`; sibling tips are never compared and a
mismatch is not a finding, so post-pin drift stays the Limits rule's job)
```

### F3 (INFO) — ADJ-02: the sentence that literally declares auth ownership is outside OUT-003's ranges

ADJ-02's trigger includes "an auth-flow question"; kagi:3 (the quote) names "the-janitor flows,
credential hygiene evidence", while the explicit sentence is kagi:63: "… kagi owns runtime auth and
credential custody" (last line of the pinned file, no trailing newline). OUT-003's registry ranges
are `3-6,10-17,32-34,54`, which exclude line 63. The mapping is still right — "the-janitor flows"
is the auth-broker surface and kama:40-41 independently refuses "credential material & auth flows
(→ kagi)" — but a reader who checks only the pointer ranges will not see the literal claim. No cell
change proposed (changing ranges means editing the round-19 census pointer, per
`OUTBOUND-POINTER-MISMATCH`); if the L1 wants it recorded, one note sentence suffices.

### F4 (INFO) — ADJ-05: "routing" is not in either quoted sentence

OUT-006's quote covers "scopes OMP task/hub"; OUT-007's covers "dispatch and orchestration
mechanism (→ kumitate)". The literal word "routing" appears in neither; the sibling sentence that
carries "route" is kama:41 ("dispatch/route mechanism (kumitate)"), which no ADJ row cites, and
mori:65 (mori's own adjacent table) says kumitate "Owns OMP task/hub orchestration and wave
plan/run/record/collect semantics". Reading "dispatch and orchestration mechanism" as including
routing is fair, so the row is not misrouted; recording kama:41 as a third pointer would need a new
anchor (same census cost as F1) and is not proposed.

Also note for ADJ-05: kumitate's own Core bands do not gate dispatch — the OMP harness contract is
its **Frontier** ground ("not yet gated", kumitate:19) — so a handoff may ask kumitate for
dispatch *analysis*, not for a verified dispatch contract.

### F5 (INFO) — ADJ-06: OUT-009's proposition is partly superseded in the same document

The ADJ-06 cell cites `OUT-009`; OUT-009's proposition reads "Revenger owns shipped-artifact
reverse engineering…", and the in-document `## R20 ownership clarification — OUT-009`
(PROVINCE.md:148-152) "explicitly supersedes only the OUT-009 proposition's unqualified 'Revenger
owns' wording and its broad 'packages' paraphrase" and keeps kaidoku/revenger arbitration open. The
ADJ-06 recipient cell already says "protocol integrator — kaidoku/revenger ownership unresolved",
so there is no contradiction — only a reader-order hazard. An optional cell suffix
"(see `R20-OUT009`)" is predicate-safe (`R20-OUT009` matches neither the `OUT-\d{3}` id scan nor the
`*.md:N` bare-range scan in check-adjacency-table-r49.py:48-49); no change is required.

### F6 (INFO) — quote-form artifacts inherited from round 19, not introduced here

Three quoted cells are fragments rather than ownership sentences: OUT-002 is a table artifact cell
whose surface label sits in the same row; OUT-004 ends mid-parenthetical ("…keybinds, rules,"), so
`waybar`/`walker`/`idle` are outside the quote; OUT-010's "the method" is deictic with its
antecedent on tameshi:3-5. All three resolve correctly at the pinned commit because the anchor
carries file + commit + heading; per the append-only discipline I recommend **not** editing those
quote cells (a changed quote would change what round 19 certified). No action.

## 5. Residual risk and verification gaps

- I did not execute either counter or any selftest (§2). C2's predicate result is taken as claimed,
  not re-measured by me; what I verified independently is the content those legs inspect (locator
  identity, registry pointers present, quote/pin/sha agreement), not the predicate's arithmetic.
- Pins are stale by design; quotes currently also resolve at tips, but the sibling repositories are
  live and one tip moved mid-review, so "operative" is a statement about read time only.
- I read the anchor table as fixed for this round; if the L1 chooses F1's prose repair, the note
  grows and nothing counted changes — that interaction is reasoned from `check-adjacency-table-r49.py`
  (ADJ section ends at the next `## ` heading; only the last cell is scanned) and
  `check-adjacency-anchors.py` (`province_pointer` presence, `_outbound_publication`), both read at
  the freeze. No run backs it, so treat it as a checked-by-reading claim, not an executed one.
- Out of scope and unreviewed: `corpus/knowledge/adjacency-anchors-r19.json` inbound rows, the
  `--ownership-corrections` mode, C1/C3, and any census behaviour.
