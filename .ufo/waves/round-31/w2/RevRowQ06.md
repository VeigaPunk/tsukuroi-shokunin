# RevRowQ06 — C1 row Q06 (nodatacow) per-row review

Verdict: **holds**. The quote is verbatim at the cited line of the pinned v7.1 bytes,
every clause of the statement, the SKILL.md line and the decision-table row is supported by
the cited source lines 131-159, the frozen question is fully answered, and the row adds
facts beyond the held neighbour SH3 (in-place-update semantics plus NOCOW attribute
assignment, compression disabled, partial-write risk) — it is not a restatement of SH3.

Reviewed at lane revision `f3a5723a988bf1c2835985880e7a38d477462cd0`, base
`2077e2fa4fa70ea79aa77b6d91f4acd35bc54897`. No LSP device is available in this
environment, so all evidence is textual (git show / git grep / sed / sha256sum / curl);
none of the files under review is code that a language server would index.

## Findings

1. [obs] Source pin integrity and quote verbatimness.
   - `curl -sL https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-mount-options.rst` → saved at `.ufo/waves/round-31/w2/RevRowQ06/ch-mount-options.rst.raw`, sha256 `aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f`, 557 lines. This equals the committed snapshot `.ufo/waves/round-31/w1/ScribeSrcMountOpts/ch-mount-options.rst` (same sha256, run with `sha256sum`), equals the frozen pin `aac3b1b...` in `tools/check-btrfs-repair-r31.py` (QUESTIONS['Q06']), and equals the sha256 in the SOURCES row S167 (`corpus/SOURCES.md:261`, mined, with the URL) and the round-31 lesson row (`corpus/lessons/round-31.md:14`).
   - Quote `*Nodatacow* implies *nodatasum*, and disables *compression*.` is a verbatim substring of line 135: `sed -n '135p' ch-mount-options.rst.raw | grep -cF '*Nodatacow* implies *nodatasum*, and disables *compression*.'` prints 1. The JSON row's `line` is 135 (`corpus/knowledge/btrfs-repair-r31.json:54`).

2. [obs] Clause-by-clause source support (cited range `ch-mount-options.rst:131-159`).
   - "With nodatacow, newly created files use in-place updates instead of copy-on-write" — supported by lines 134 ("Enable data copy-on-write for newly created files." — datacow semantics the option toggles off), 135 (implies/disable) and 141 ("Updates in-place improve performance for workloads that do frequent overwrites"). [inf] "instead of copy-on-write" is an entailment of 134+141, not a verbatim phrase; it contradicts nothing and loses no branch.
   - "and receive the NOCOW attribute" — line 136 ("All files created under *nodatacow* are also set the NOCOW file attribute").
   - "it implies nodatasum" — line 135 verbatim.
   - "so these files lack data checksums" — lines 148 ("Enable data checksumming for newly created files."), 150 ("under *nodatasum* inherit the 'no checksums' property"). [inf] The inheritance clause at 150 applies to files created under nodatasum; since nodatacow implies nodatasum (135), files created under nodatacow are covered. Fair, no lost branch.
   - "and compression is disabled" — line 135 verbatim; also notes at 139 and 154.
   - "Frequent overwrites may perform better" — line 141 ("improve performance for workloads that do frequent overwrites"); "may" is a correct softening.
   - "but interruption by system crash or device failure can leave partial writes" — lines 142-143 ("at the cost of potential partial writes, in case the write is interrupted (system crash, device failure)").
   - No "only"/"always" claims appear in the row (QUALITY 66 check). The source's other statements (defaults `(default: on)`, slight performance gain at 156-158, the chattr manref) are not contradicted by the row.
   - Question "What does the nodatacow mount option give up on btrfs?" — answered in full: it names the losses (copy-on-write → in-place updates, checksums, compression) and the consequence (partial-write risk), i.e. the three sealed answer-key areas are all addressed. No part of the question is left unanswered.

3. [obs] SKILL.md line (`SKILL.md:2685`): "Weigh nodatacow's loss of copy-on-write, checksums, and compression against possible partial writes after interruption by a crash or device failure. | S167 lines 131-159" — every element maps to the lines above (134-136, 139, 141-143); the cited range matches the source range used. Exactly one `| [R31-Q06] ` line exists at REV (`git grep -c -F '| [R31-Q06] ' f3a5723a -- SKILL.md` → 1, outside code fences per the section shown at 2674-2688).

4. [obs] Decision-table row (`corpus/knowledge/btrfs-repair-r31.md:17`): condition "nodatacow is enabled for newly created files" — [obs] wording wrinkle: the doc words the datacow option as "Enable data copy-on-write for newly created files" (134); "nodatacow is enabled for newly created files" is the row's trigger phrasing, not a source quote, and is not factually wrong. Action cell: "nodatacow implies nodatasum and disables compression" (135) ✓; "in-place updates may improve performance for frequent overwrites but carry a risk of partial writes if interrupted" (141-143) ✓; "nodatasum files inherit the no-checksums property" (150) ✓.

5. [obs] Novelty at base 2077e2fa (sweep `git grep -n -i -F` over SKILL.md, PROVINCE.md, corpus/): frozen tokens `nodatacow` and `nodatasum` → 0 hits each (same result as the declaration sweep and wave-1 MutCounterC1). Synonym/neighbour sweep: `NOCOW` → 10 hits, all in the SH3/S139 cluster (SKILL.md:2367; corpus/knowledge/storage-health-r26.md:43,112,131; corpus/SOURCES.md:145; corpus/README.md:239) — "NOCOW file data ... has no checksums"; `checksum` → hits but none about nodatacow/nodatasum mount semantics; `in-place` → hits only about lane-annotation/QA conventions; `copy-on-write` → 0; `compression` → hits only in calibration notes. So the only held neighbour is SH3's checksum-absence fact.

6. [obs] What Q06 adds beyond SH3 (the wave-1 review question, per `SCORECARD.md` errata item 2 and CritNoveltySemantic recommendation (b)):
   - NEW: mount-option semantics — nodatacow/nodatasum names, nodatacow implies nodatasum, the option applies to newly created files and assigns the NOCOW attribute (in-place updates instead of CoW). SH3 never names a mount option; it treats NOCOW as a file attribute already present.
   - NEW: compression is disabled under nodatacow/nodatasum (135/139/154).
   - NEW: partial-write risk after system crash / device failure (142-143).
   - NOT new (held by SH3): the no-checksums consequence of NOCOW data. The row does not restate SH3 alone — the checksum clause is one of several, and the new facts above are material decision content.

7. [obs] Frozen-predicate mechanics observed as evidence, not as verdict drivers: R3 pin equals snapshot bytes (finding 1); R5 S167 is absent from the base registry (`git grep -F "S167" 2077e2fa -- corpus/SOURCES.md SKILL.md PROVINCE.md corpus` → no hits) and present at REV as mined with the frozen URL and sha256 (SOURCES.md:261); R6 tokens appear in quote, statement and the SKILL line (nodatacow, nodatasum in quote/statement; nodatacow in SKILL line); R8 zero hits at base (finding 5); single row id Q06 (`git grep -c -F '"id": "Q06"' f3a5723a -- corpus/knowledge/btrfs-repair-r31.json` → 1). No sealed keys were recovered or printed.

## Residual risk / verification gaps
- [unk] I did not run the counter itself (leaf seat; the after-receipt already reads C1 new_sourced 8 of 8 at 13ca52d0). Mechanical rule compliance here is verified by direct evidence, not by a counter run.
- [inf] "Instead of copy-on-write" and "lack data checksums" are entailments across adjacent source lines (134/141, 148/150), not single-line verbatim statements; both are correct, but a hyper-literal "every word verbatim" standard would flag them — I judge them supported per QUALITY 66.
- [obs] The wave-1 evidence shows the sealed Q06 key groups were recovered in the dictionary exercise (CritKeyDictionary) and are present in `keymap.json`; that is a declaration transparency point (errata item 4), not a row defect.

Scope: read=corpus/knowledge/btrfs-repair-r31.json, corpus/knowledge/btrfs-repair-r31.md, SKILL.md:2683-2689, corpus/SOURCES.md:261, corpus/lessons/round-31.md:14, SCORECARD.md round-31 declaration + errata (git show at f4861f4d and f3a5723a), tools/check-btrfs-repair-r31.py:1-120, wave-1 reports (ConnSiblingOverlap, CritClaimFraming, CritKeyDictionary, CritNoveltySemantic, MutCounterC1), fetched ch-mount-options.rst lines 124-168; wrote=.ufo/waves/round-31/w2/RevRowQ06.md, .ufo/waves/round-31/w2/RevRowQ06/ch-mount-options.rst.raw (fetched bytes); executed=sandbox clone+checkout (f3a5723a), git show/grep (read-only), curl, sha256sum, sed | grep -cF
Model: inception/mercury-3
Installs: none
