# R20-RULE4 — source reconstruction (NO-EXEC)

Axes named: C1 adjacency (8, lowest), C2 operability (9), C3 calibration (9); preregistered ordinal deltas are all 0. This bounded source review establishes no measured axis change.

## Reconstructed contract and control order

The round-19 boot-writers entry attributes observed `/boot/limine.conf` log events; it does not establish file contents. Under `corpus/knowledge/boot-writers-r19.md:86-93`, operator decision items 1–3 classify matching and unmatched `Updated:` events, while item 4 (`:93`) makes the stronger deduction that a snapper-cleanup run with no `Updated:` line is “No write.” Its only example is the 09:08:04 run, whose cause it already marks `[unk]`.

That deduction conflicts with the later-added qualification at `boot-writers-r19.md:160-164`: it states that the tool's message has no content hash and that a silent/no-change path is not excluded; the cause remains unknown. The entry's adjacent limits say `/boot` was not read and no mtime/hash/content is asserted (`:97-101`). The prior verifier spotcheck explicitly resolved intended precedence as “the no-Updated qualification … controls the stronger earlier rule:93,” while identifying the missing explicit pointer as defect 5 (`corpus/lessons/round-19-verifier-spotcheck.md:77`). Thus, before R20, the later qualification was the intended control, but the operator decision list still published the contradictory item-4 conclusion without a local supersession marker.

The minimal correction is a named, append-only supersession of only that item—not a rewrite of the historical rule or a new host claim. It is already present at `boot-writers-r19.md:168-170` as `## R20-RULE4 — named supersession of Operator decision rule item 4`. The body makes the qualification controlling: no captured `Updated:` line means no captured matching log event, not proof of no write or unchanged contents; the evidence is a finite capture, not a content hash or exhaustive filesystem audit. It preserves the 09:08:04 cause as `[unk]`, disclaims conclusions such as lock skip/success/failure/byte change, and authorizes no boot/package/service action. Recommendation: retain this block as written; do not add a competing supersession or erase item 4's history.

The source note reports the 09:08:04 observation at `r19c:46-57` (`boot-writers-r19.md:93,101,164,170`; also `SKILL.md:2035`). I did not open or execute capture/transcript bytes. These references support only the bounded absence of a matching captured log line and the documented unknown cause; they do not establish whether `/boot/limine.conf` was written or unchanged.

## Current-use mentions in the touched surfaces

- `SKILL.md:2035` (R19 E6) says absence of a limine line is not evidence of a **lock skip**, with the 09:03–09:08 cleanup observation still `[unk]`. This rejects one proposed cause, not by itself every possible write or the broad item-4 deduction.
- `SKILL.md:2092` is the direct R20 pointer: it says the named supersession controls the older “No write” rule and that absence does not prove no write/unchanged contents.
- `SKILL.md:2012,2018` gives the event denominator and the observed cleanup writer class; it calls for recording/no action. `SKILL.md:2058` separately treats an hourly-cleanup mtime as expected behavior, not drift. Those are event/mtime expectations, not evidence that a missing log event proves no write.
- `corpus/README.md:184` says S080 keeps the no-write inference rejected and points to the named R20-RULE4 supersession as controlling the stronger historical wording.
- In the boot-writers entry, the competing rule is `:93`; its bounded-content and unknown-cause limits are `:97-101`; the appended qualification is `:160-164`; and the explicit local supersession is `:168-170`.

The related source-history record `corpus/lessons/round-20.md:27,38` identifies S080's pinned baseline source and classifies R20-RULE4 as stale-premise/negative-overclaim, with the named supersession and retained unknown cause as the fix. `corpus/SOURCES.md:87` records S080 as rejected and states that reversal would require independently bound exhaustive write evidence or content comparison for the exact window. The pinned baseline is recorded there as `0cbc34dd6b20896085a8fb07943e3ea4027d8472`; this seat did not independently extract that Git object.

## Confidence and limits

High confidence in the present source text and intended control order: the entry, prior verifier finding, R20 lesson, SKILL pointer, and README pointer agree. No conclusion is made about actual file writes, file contents, or the unresolved 09:08:04 cause. Work was limited to local source reads/searches; no captures were opened, no host/shipped-target probes or tools were run, and no tests/gates were run.

Scope: executed=none