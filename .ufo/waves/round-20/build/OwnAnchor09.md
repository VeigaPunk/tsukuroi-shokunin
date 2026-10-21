# OwnAnchor09 — C1 source/ownership review of OUT-009 (revenger)

NO-EXEC seat: read/grep/glob only. Digests, counts and line numbers are quoted from records as
recorded; nothing was recomputed, no gate run, no live sibling state read.

## Records reviewed
- Registry `corpus/knowledge/adjacency-anchors-r19.json:112-123` — OUT-009: province_pointer
  `../revenger-shokunin/PROVINCE.md:3-7,19-25`; sibling `revenger`/`PROVINCE.md`;
  pin `cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97`; recorded blob sha256
  `63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f`; snapshot
  `.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md`; heading
  `# revenger province`; quote `Owns: reverse engineering of shipped artifacts` at quote_line 3;
  proposition "Revenger owns shipped-artifact reverse engineering (binaries, packages, APKs) with
  an observation/inference/unknown evidence ledger; tsukuroi tracks state only."
- Census `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json:2981-3006` — same
  pointer/pin/digest/snapshot; ranges `[[3,7],[19,25]]`; branch `main`; sibling_line_count 32;
  `cited_text_at_tip` for both ranges. Registry and census agree on every shared field.
- Province `PROVINCE.md:51` (ADJ-06): cites both
  `../kaidoku-shokunin/PROVINCE.md:3-6,88-100` and `../revenger-shokunin/PROVINCE.md:3-7,19-25`;
  recipient "protocol integrator — kaidoku/revenger ownership unresolved". Frontier arbitration
  `PROVINCE.md:79-80`. Portable-anchors section from `PROVINCE.md:108`: preamble
  "This section grants no authority and is an ownership locator, not a repair mandate" (:117);
  OUT-009 row :129 (same quote and byte-identical proposition as the registry); limits paragraph;
  portable-digests list carries the same full pin + `63acc3d0…19f` for OUT-009.

## Pinned declaration reopened (read tool)
Snapshot `.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md`, 32 lines, read whole:
- :1 heading `# revenger province` — matches registry heading.
- :3-7 Owns paragraph with exact classes: native binaries, managed assemblies,
  **Electron/JavaScript packages**, Android APKs, archives, firmware, browser/Electron runtime
  evidence; REA skill/toolset; evidence-ledger discipline (observation/inference/unknown, Evidence IDs).
- :9-16 read-only Sources list; :18-24 Refuses paragraph; :25-32 writes-only boundary: writes only
  `revenger-shokunin/`; domain source checkouts, shared fleet state and sibling repositories remain
  read-only; no push, routing or substrate/package remediation.
- Quote check: the recorded quote is a verbatim prefix of snapshot :3; quote_line 3 is inside range
  3-7. Census `cited_text_at_tip` "3-7" and "19-25" match the snapshot bytes as read ("19-25" ends
  mid-sentence "…under the current interactive", consistent with range end 25).

## Verbatim quote vs proposition vs permission
- **Verbatim quote** (sibling's own words, attributed): `Owns: reverse engineering of shipped
  artifacts`. The "Owns" is Revenger's self-declaration, not a tsukuroi award.
- **Proposition** (tsukuroi's summary, `PROVINCE.md:129` = registry proposition, byte-identical).
  Two defects:
  1. *Owner selection*: "Revenger owns" restates the self-declaration as a settled award,
     contradicting `PROVINCE.md:79-80` ("The integrator must arbitrate this shared scope; tsukuroi
     neither picks an owner nor absorbs it") and ADJ-06's unresolved recipient. Round-19
     `falsify/FxConnOverlap.md` already classified OUT-009 "OVERLAP — direct contradiction / owner
     selected": kaidoku declares the same domain at its recorded pin
     (`…/siblings/kaidoku/d1d981d2cc04/PROVINCE.md:3-6`, recorded, not reopened here).
  2. *Scope broadening*: "(binaries, packages, APKs)" shortens the pinned "Electron/JavaScript
     packages" to arbitrary packages.
- **Permission**: none. Locator only (:117). The snapshot grants Revenger only its own repo; no
  target invocation or configuration/service/package/boot/sibling-file write authority is derivable
  from the quote or the proposition.

## Unsupported scope or authority
- Found exactly where R20-OUT009 says: the proposition's unqualified "Revenger owns"
  (arbitration not done) and the "packages" shorthand (broader than pinned "Electron/JavaScript
  packages"). No other unsupported authority in the record: pin, digest, heading, quote and ranges
  carry only declaration/refusal/write-boundary text.
- Residual, recorded and unchanged here: pointer range 19-25 ends mid-sentence; snapshot lines
  26-32 complete the write restriction (round-19 OutAnchor09/FxOut009 noted the same). The pointer
  stays at its pinned ranges.

## Does R20-OUT009 affect this row?
Yes — this row only, and only its proposition wording.
- `PROVINCE.md:148-152` (`## R20 ownership clarification — OUT-009`) supersedes only the
  proposition's "Revenger owns" wording and the "packages" paraphrase; the quoted declaration,
  pinned bytes, ADJ-06/Frontier arbitration and the other nine locators remain controlling. The
  same correction text is at `.ufo/waves/round-20/ownership-correction.txt:1` (the gate's persisted
  expected text; observed prose here, not a measurement of gate success).
- Recommendation: keep the OUT-009 locator row (pin, heading, quote, ranges) unchanged at retained
  pinned scope; treat the proposition as superseded by the R20 section, not rewritten in place
  (append-only discipline; the round-19 section declares itself append-only). This matches the
  preregister C1 scope ("Explicit sibling-declaration wording for OUT-009 at retained pinned scope,
  no integrator arbitration or write authority") and the R20-OUT009 lesson row
  (`corpus/lessons/round-20.md:37`). Other anchors are out of scope and untouched.

## Limitations
- All digests/counts quoted as recorded; registry, census and PROVINCE portable digests agree with
  each other. No hash recomputation, no gate or selftest run, no host probe.
- Sibling bytes were read from the round-19 captured snapshot only, not from the live revenger
  checkout; pins are stale by design once a sibling commits again (PROVINCE limits paragraph), and
  any later handoff re-reads the live declaration.

Scope: executed=none
