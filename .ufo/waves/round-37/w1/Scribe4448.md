# Scribe4448 — item 4/8 evidence draft

## Axes
- **C1 operability:** bounded to whether source evidence supports a usable errno discriminator; no probe execution claimed.
- **C2 depth:** preserve distinct errno mechanisms and their claim boundaries.
- **C3 calibration:** distinguish observed errno from candidate cause and unresolved provenance.
- **Frontier:** assess errno discrimination, not host remediation or a source-row admission decision.

## Scope and evidence status
This is a scoped draft from the round-37 staged material, not an independent source census. Opened sibling seat `C22F10.md` records a concrete round-36 correction target (`-F` output under `-n`) and explicitly says that `-n` is not a scope filter; it does not itself establish the errno-frontier entries or their sources. Opened `C26F14.md` likewise addresses that `journalctl` behavior, not errno discrimination. I did not open the candidate errno source pages or external references in this pass, so I cannot propose a SOURCES row or supply an admissible source citation (URL, access date, located quote). No external source was opened by me this round.

## Claim boundaries to preserve (draft/inference)
The assignment names errno discrimination as the frontier theme, but the staged material inspected here does not identify the proposed three entries. Therefore their exact subjects, predicates, source IDs, overlap with existing knowledge, and admission status are **unknown**; no admit/reject/duplicate verdict is warranted. A defensible entry would need to state the operation and observed errno, separate errno observation from causal explanation, identify competing mechanisms that can yield different errno values, and declare what evidence would falsify the proposed cause. In particular, do not infer that an errno alone identifies a root cause, nor treat distinct errno values as interchangeable symptoms. These are review criteria, not claims that any staged row satisfies them.

## Finding
**Unresolved / evidence-limited.** The opened evidence supports no conclusion about whether the three candidate entries are novel, correctly bounded, sourced, or within an existing corpus surface. Treating this as a clean overlap scan or a source-row proposal would exceed the evidence. For C1, a later review should require an observable discriminator with command/context and predicted outcomes rather than an errno-name-only assertion. For C2, keep errno, syscall/operation, mechanism, and confidence as separate claims. For C3, historical-cause attribution remains unknown absent event-to-operation evidence.

## Gates, touched surfaces, and limits
- No gate, probe, campaign tool, checker, or corpus sweep was run by this seat; no PASS/FAIL is claimed.
- Only this assigned seat report is written. No lane content, Git/jj state, fleet repo, sibling lane, or shokuknow content was modified; no fixture Git repository was created.
- Read `/home/vgpnk/.omp/agent/RULES.md` before action. No tool installed or updated; hence no tool/version/channel/reason install record applies. No pacman or host changes.
- Local evidence opened: `.ufo/waves/round-37/w1/C22F10.md` and `.ufo/waves/round-37/w1/C26F14.md`; these concern the journalctl `-n` correction, not the uninspected errno entries.
- No source row proposed: external source requirements (opened this round, URL/date/≤25-word quote) are unmet.
