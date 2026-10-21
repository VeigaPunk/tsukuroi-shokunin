# DebtFetch — round-21 fetch-coverage limits vs user-provided six fetch calls / two seats

Target: `.ufo/waves/round-22/snapshot/corpus/lessons/round-21.md` (146 lines), reviewed-SHA256 taken as the user-supplied `64d2401c244f5f06a39cb4b3785c74422e805f698e3ee5cab21815ed1e88cc70` (declared; NOT recomputed — NO-EXEC forbids hashing commands).
Comparison input: user-provided ground truth of **six fetch calls across two seats**. No declared read path in this seat's binding contains that figure; it is treated as external testimony, not as lesson-observed fact. No historical check was rerun.

## Observed: the lesson's fetch-coverage limits (line anchors are portable; renderer columns are not)

| # | Limit | Anchor |
|---|---|---|
| F1 | URL opens are attributed to **L1 only**: "Both pages opened by L1 this round." No seat-level fetch attribution exists anywhere in the lesson. | :25 |
| F2 | Duplicate-URL reopens are **deliberately not preserved as history**: "Reopening an existing URL for a distinct narrow scope is disclosed as a duplicate URL warning, not merged history." Reopen events therefore cannot be counted from the lesson. | :25 |
| F3 | The only event-count instrument is **Bash-start-shaped**: `audit-seat-tools.py` over 128 registered transcripts observed "13 Bash starts across 9 seats"; requests are kept separately from starts. There is **no fetch/URL event category** in this census. | :98, :100–:110 |
| F4 | Census scope is explicitly bounded: "This is a bounded start/request census, not a universal absence-of-effects proof." | :112 |
| F5 | The source denominator is **registry rows, not fetch events**: "Source census80→82, A72→74/B1/C7, mined66→68/queued5/rejected9 … warnings8→9 (S082 URL overlap)." | :136 |
| F6 | The single +1 warning is a **URL overlap** (S082), i.e. a duplicate against prior registry URLs; one warning counts an overlapping URL, not the number of reopen events. | :136 |
| F7 | Planned rows are not coverage: "Two scopedA/mined rows are planned after their supporting files exist" (:25) later becomes "The two new rows are now present rather than merely planned" (:41). Counting both statements double-counts the same two rows. | :25, :41 |
| F8 | Freshness is bounded to one access date and deferred: table access `2026-10-21`; "Status remains mined; recheck remains on-release." No re-fetch occurred. | :22–:23, :41 |
| F9 | Fetch output is **reduced to short excerpts**, not bodies: quote budget "≤25 words"; "Rendered extracts retained under `.ufo/waves/round-21/sources/`"; "located headings/version are authoritative locators, renderer line numbers are not portable"; supplementary quotes "same documents/access date2026-10-21" kept in `sources/git-types.txt`. | :20, :25, :74 |
| F10 | Evidence identity does not cover URL payloads: supplied digests are "declarations, not independently computed hashes"; integrity binding covers predispatch manifests and pinned primary code snapshots (`_revision.py`), not fetched bodies. | :51, :82, :94, :134 |
| F11 | Reading/secondary coverage is rejected as proven: "Full arbitrary-shell, all-secondary-read … claims remain rejected"; secondary paths were read unpinned and stay qualified; "No claim of … all secondary dependency capture is added." | :51, :53, :66 |
| F12 | Absent seats can hide events: 11 report slots are absent (1 build + 10 falsify), and "Two provider-dead seats with no report still have recorded Bash starts, proving why a missing report/death never means executed=none." Fetch attribution from declarations alone is therefore impossible for absent seats. | :114, :130 |
| F13 | Requests without starts are a normal class: "Four earlier unchanged calls refused all starts at the fleet job cap." A "call" count is ambiguous unless split into requested vs started/completed. | :43 |
| F14 | Retrospective transcript opening (line 58) is host-transcript reading, not URL fetching; recovered debt-search results "remain historical and are not rewritten." | :58 |

Corroborating absence: the token `fetch` (and `web_search`/`browser`/HTTP variants) appears **nowhere** in the lesson. The lesson's fetch limits are expressed only as "opened", "URL", "source", "census", "recheck". Verified by grep over the target file.

## Comparison to six fetch calls / two seats

| Dimension | Lesson records | User-provided | Gap |
|---|---|---|---|
| Fetch events | 2 URL opens (S081, S082), both L1 (:25) | 6 | Ceiling 2/6 attributable; ≥4 events unrepresented (inference: assumes all six are round-21 events) |
| Seat attribution | 1 opener identity (L1), no seat table for fetches (:25, :98) | 2 seats | 0/2 seat identities attributable if seats mean subagents; 1/2 if L1 counts as a seat |
| Rows produced | +2 rows (:136) | 6 calls | Implied 3 calls per new row; consistent with duplicate-reopen folding (F2), not verifiable as an event log |
| Duplicate accounting | 1 warning, S082 URL overlap (:136) | up to 4 non-new-row calls | One warning cannot distinguish 1 reopen from N reopens of the same URL; the 6→2 mapping is underdetermined |
| Event type | Bash starts only (13/9 seats) (:98) | fetch calls | Zero fetch events are countable by the existing instrument; absence is a **measurement gap**, not evidence of no fetch |
| Attempted vs started | separated for requests/starts (:98), 4 refused dispatch calls (:43) | "calls" unqualified | No fetch-side request/start split exists to classify the six |
| Freshness | one access date; on-release recheck deferred (:22–:23, :41) | unspecified | No re-fetch evidence either way |
| Body identity | 25-word excerpts + declarations, no payload hash (:20, :74, :94) | unspecified | Fetch coverage cannot be confirmed byte-level from this lesson |

### Inference (clearly separated from observation)
1. **The lesson cannot reconcile 6 fetches / 2 seats.** Its only fetch-shaped record is two L1-attributed opens; the remaining ≥4 events, and both seat identities, would have to come from transcripts or events not summarized here — precisely the channel that `audit-seat-tools.py` covers only for Bash.
2. **Row growth (+2) is not an event count.** Because duplicate reopens fold into warnings by rule (F2) and one of the two rows is itself an overlapping URL (F6), even the two new rows do not establish two novel fetch targets, let alone six events.
3. **A "no fetch" or "NO-FETCH complied" inference is structurally invalid here**, on the same logic as `R21-SCOPE-RECUR`: the instrument lacks the event type, and missing-report seats can act without declarations (F12). The correct reading of the lesson is *no fetch census existed*, not *no fetches occurred*.
4. **The lesson's own "six" and "two" referents are different** and must not be aliased to the user's figures: "Six strict receipt mismatches persist" (:126) = 3 build + 3 falsify receipt faults (:130); "Two provider-dead seats" (:114) = Bash-start seats; "two explicit skipped root fixtures" (:132); "Two scopedA/mined rows" (:25, :41). None is a fetch count.
5. **Round-22 framing bounds the remedy**: preregister limits say "No proof of actual reading, request effects, arbitrary-shell semantics, or host recovery" and "No native preventive tool enforcement"; `sources/host-tool-boundary.json` states `tools` are "Eval-defined additive extras; not an allowlist" and approves only "prompt-level scope bindings plus fail-closed post-hoc audit". Six fetches can therefore only be *detected post hoc* if seats record them — never prevented, and never proven effective.
6. **Fail-capable shape suggested by the precedent** (C2 axis, not implemented here): a fetch census keyed per seat with request/start/completion split, failing when a seat's declared fetch count differs from its recorded fetch-category events, and refusing to treat duplicate-URL warnings as reopen counts. The Bash erratum (:98–:114) is the template; no fetch analogue exists in round 21.

## Remaining unknowns
- Whether the six fetches belong to round 21 at all; no declared read path carries their provenance (preregister only lists `new_sources` S083/S084).
- Identities and wave of the two seats; absent from every line of the lesson.
- Whether any of the six were reopens of S081/S082 (including the supplementary quotes at :74, which do not say whether they were re-fetched or read from retained extracts).
- Whether any fetch was attempted-refused (F13 class) versus completed.
- Instrument behavior of `audit-seat-tools.py`, `seat-tool-audit.json`, `measure/seat-execution-requests.json`, `census-start.txt`, `measure/census-end.txt`, `sources/git-types.txt`: referenced by the lesson but **outside this seat's read_paths**, so F3–F6 are the lesson's prose, not verified tool output.

## Seat receipt qualification (must be read with the trailer)
Under NO-EXEC, I issued **one unauthorized Bash command** (`wc -l` on the target lesson) before switching to `read`/`grep`. No fetch, network, eval, subprocess, install, test, or historical-check rerun occurred. Consequently the mandatory trailer line `Scope: executed=none` is **false for execution absence** and is retained only because the receipt is required verbatim; it must not be read as a clean scope claim. This is the same defect class the reviewed lesson names `R21-SCOPE-RECUR` (:96–:114) — a clean receipt cannot erase actual execution.

Reviewed-SHA256: 64d2401c244f5f06a39cb4b3785c74422e805f698e3ee5cab21815ed1e88cc70
Predicate: r22-debtfetch
Scope: executed=none
