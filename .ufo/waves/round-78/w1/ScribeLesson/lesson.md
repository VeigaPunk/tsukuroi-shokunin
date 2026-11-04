# Round 78 — path-usage examples and operative registry debt

Draft for L1 integration, not an outside verdict. Axes: **depth** (8, lowest tied adjacency) and **operability** (9); no ordinal uplift is inferred. Base `b9019a1d0558241bf67cf31ff90256284d8657af`; frozen claim commit supplied by assignment: `07a607df1a5157daafc91bb5c26858af14415f43`. The declaration is `SCORECARD.md:6497–6540`; exact finite cases, source pins and target are `.ufo/waves/round-78/before/expected.json`. L1 holds planner.

## Gate

This seat read the pinned payloads, not fresh network responses. Upstream v262 line numbers are not verified installed Arch-build anchors. Source digests below are the frozen specification's pins, not new hash executions by this seat.

| Candidate | Located evidence | Gate decision / reason / flip |
|---|---|---|
| S327, upstream path-usage accounting | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c ; pinned `before/journald-manager.c:119–131`, quote `*ret_used += (uint64_t) st.st_blocks * 512UL;` | admit as bounded code teaching: accepted suffix, successful no-follow stat, regular file, allocated blocks. Frozen SHA256 `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`. This is a draft Gate decision, not proof the registry row has landed. |
| Apparent size, suffix alone, or symlink target size determines used bytes | Same pinned source :119–131; `AT_SYMLINK_NOFOLLOW` at :123 and `if (!S_ISREG(st.st_mode))` at :128 | reject: selection and allocated blocks determine this function's contribution; `st_size` is not added. Flip: a relevant version-pinned implementation actually using apparent size or following links. |
| Vacuum and disk-usage measure the same removable set | https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml ; pinned `before/journalctl.xml:969–971`, quote `vacuuming operation only operates on archived journal files.` | reject: the adjacent text expressly includes active files in disk-usage. Flip: a scoped source changing that inclusion/removal relationship. No vacuum was executed. |
| Staged corpus adoption or promotion | `SCORECARD.md:6536–6539`; round-77 lesson :71–83 and outside closure :95–100 | reject while held; flip requires explicit operator release and per-entry source gates, not a finite counter pass. |

U1 contributes 4096 despite apparent size 1048576; U2 contributes 8192. U3's wrong suffix, U4's symlink, U5's directory and U6's failed stat each contribute zero. These are the six frozen hypothetical descriptors, not host observations (`before/expected.json:6–60`). Filesystem free space is separately computed from `ss.f_bsize * ss.f_bavail` (`journald-manager.c:114`); this lesson does not equate it to path usage or infer manager state.

Outside round-78 admit/reject closure is **not evidenced by this seat**. ReviewUsage and ReviewRegistry are author-side wave seats; their assignment, name or prospective report cannot substitute for completed reviews or non-author closure (`SCORECARD.md:6520–6526`). Round-77's former pending language is historical: `corpus/lessons/round-77-verifier-spotcheck.md:5,65–74` records its actual non-author admission and source admit/reject agreement.

## Mistakes

| Class / id | Evidence | Captured-by | Fix and demonstrated red-before boundary |
|---|---|---|---|
| landing — R77-REGISTRY-PLACEMENT | `corpus/lessons/round-77.md:168–184`; `SCORECARD.md:6472–6487` | QUALITY 70, operative registry checker | The descriptive addition header did not register the tool. The historical repair inserted its row in the exact operative contiguous table: historical measured receipt had 11 findings / 9 missing; support retained 10 inherited findings / 8 missing, not a clean gate. Outside closure :63 agrees. This is a demonstrated prior repair, not a new r78 result. |
| carried-debt — R78-INHERITED-REGISTRY | Outside round-77 closure :63,95–100; `before/controls.json`, `C2-do-nothing` | QUALITY 70; round-78 C2 | Frozen base command `python3 tools/check-registry-coverage.py --revision b9019a1d0558241bf67cf31ff90256284d8657af` records 10 findings, exit 1: eight missing rows and two missing code-2 verdict classes. Repair must register the missing paths and truthful maps while retaining existing tools. Target zero is not an observed after value here. |
| review-conformance — R78-MISSING-BINDING | Round-77 lesson :151–156; outside closure :63,98; `tools/measure-journal-usage-r78.py:40–70` | QUALITY 81; fresh C1 predicate | Fresh predicate now requires exact data, per-case holds, artifact digest, unique ReviewUsage reviewer-role result and verdict-byte digest in that result. Recorded pre-data scripted fetch-and-fill without review scores 0/rc1; fabricated review without orchestrator result also 0/rc1 (`before/controls.json`). These controls demonstrate refusal of missing evidence, not authenticity. No frozen r77 instrument is retrofitted. |
| scope — R78-BOUND-NOT-AUTHENTIC | `SCORECARD.md:6520–6526`; counter :54–69 | QUALITY 81 and the declaration's explicit limit | A wholly fabricated verdict plus fabricated orchestrator bundle remains open. Recorded selftests refuse wrong role, lost result and failed row and accept a complete synthetic control (`before/controls.json:10`). That positive synthetic case is not evidence of a real reviewer reading. Human source/companion review and outside closure remain distinct requirements. |

The frozen controls record 15/15 same-reader selftests, exit 0; the base C1 command `python3 tools/measure-journal-usage-r78.py --revision b9019a1d0558241bf67cf31ff90256284d8657af` records 0/rc1. Both do-nothing controls fail their target. This seat read those receipts and implementation; it did not execute the controls. No final C1 count, registry result, mutation total, wave settlement, census total or structural total is guessed.

## Source propagation boundary

This round deepens existing journald ground, not new coverage (`SCORECARD.md:6520`; existing allocated-block teaching `SKILL.md:6068`). Source propagation for L1 is the S327 registry row, `corpus/knowledge/journald-path-usage-r78.{md,json}`, its bounded SKILL pointer, and the lesson/scorecard records declared in C1; naming them here does not claim their integration. The JSON is byte-bound to ReviewUsage's verdict, but companion prose is not read by the numeric predicate (`measure-journal-usage-r78.py:17–19,40–70`), so any adopted prose changes require substantive source re-reading rather than reusing a JSON digest as a prose verdict.

The prior false minimum proposition remains append-only history, explicitly superseded by S325, not silently erased. The existing propagation map is `corpus/lessons/round-77.md:53–69`; round-77 outside closure :48–52 independently accepted the actual correction. No claim here extends that sweep to uninspected current carriers or edits outside evidence scope. QUALITY 108 remains the standing correction-propagation rule; this draft invents no competing criterion.

## Frontier, reflection and holds

Assimilation: **none**. No staged package bytes are adopted; package/id-drift and promotion holds are not answered by this lesson (`round-77.md:73–78`; `SCORECARD.md:6536–6539`). Current final counts and collision totals are not known to this seat and are not extrapolated from r77.

Latest lane proposal file discovered and read: `considerthese/2026-10-26.md:15–21`. It labels its ideas proposed-only at origin. This round records already-implemented reflection, not a new adoption: counter-attack scoreboard exists in `SKILL.md:3833–3838,5603–5608`; downstream patch-offset boundary is QUALITY 103; cross-note correction propagation is QUALITY 108. Burst-aware reading and seat-harm log are listed ideas in that file, not newly implemented actions claimed by this draft. The prior lesson's statement that all five were already implemented (`round-77.md:124`) is a historical author-side report; this seat does not independently elevate the two unchecked implementations.

PROVINCE.md and SHONEN.md are intentionally unchanged by this seat: neither finite examples nor registry discoverability grants frontier promotion, authority transfer or whole-SKILL execution. The prior outside closure expressly leaves coverage, adjacency and expansion unchanged and promotion ungranted (`round-77-verifier-spotcheck.md:13–14,80–100`); C1/C2 remain depth and operability only. No outside verdict or adoption is self-awarded.
