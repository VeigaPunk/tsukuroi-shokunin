# OUT-005 — source/ownership review

**Axis:** C1 adjacency. **Finding:** bounded unchanged; read the proposition as journal-record/event classification, not core-dump internals or permission to act.

**Evidence observed.** `corpus/knowledge/adjacency-anchors-r19.json:61-71` records OUT-005 against Mori `PROVINCE.md:3-16`, pinned commit `91940fa339e38006f8db5bd7d78bb6f037f4d016`, recorded blob SHA-256 `73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130`, and snapshot `.ufo/waves/round-19/l1-capture/siblings/mori/91940fa339e3/PROVINCE.md`. These commit/digest values are reported as recorded; not recomputed here. The portable table repeats the proposition at `corpus/knowledge/adjacency-anchors-r19.md:85`.

The pinned declaration at `.ufo/waves/round-19/l1-capture/siblings/mori/91940fa339e3/PROVINCE.md:6-10` says “**Owns (read-only probes)**” and includes “kill/OOM-related catalog-ID records and signal-11 coredump records from independently labeled user/system journals”; lines 12-16 refuse OS package, systemd, driver/firmware and boot-state ownership and say Mori reads journal/cgroup events as fleet evidence, never owns OS state, and performs “Detection and report only — never remediation.” Line 18 says “Out of province → report, never absorb.” The registry quote at line 69 is verbatim for the quoted records phrase.

**Quote vs. proposition vs. permission.** The registry proposition at line 71 adds “classification” and the fleet-attribution boundary; these are summary/inference, not verbatim quotation. The declaration supports read-only collection/reporting and interpretation of the specified journal records as fleet evidence. It does not authorize remediation or ownership of OS state. “Classification” is bounded if it means categorizing those journal records; it is unsupported if read as analysis of core-dump contents or binary internals.

**R20-OUT009 relation.** `.ufo/waves/round-20/ownership-correction.txt:1` clarifies that OUT-009 is Revenger's sibling declaration about reverse engineering shipped artifacts, not a Tsukuroi ownership grant; Kaidoku/Revenger arbitration remains unresolved and no writes are authorized. This does not substantively change OUT-005's journal-record boundary. It reinforces that OUT-005 must not be stretched into a core-dump-internals handoff or permission claim. Recommend retaining OUT-005 unchanged, with the bounded reading of “classification” above.

**Limit:** This review reopens the retained snapshot and checks the portable anchor only; it does not verify the sibling's current declaration or recompute the recorded digest.

Scope: executed=none