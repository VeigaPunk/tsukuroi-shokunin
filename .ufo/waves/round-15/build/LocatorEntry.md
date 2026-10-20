# LocatorEntry — round 15 C1/locator + positive domain

## Files changed

- `corpus/knowledge/source-locator-clarification-r15.md` (new): provenance trio, `## R15-LOCATOR`, `## R15-POSITIVE-DOMAIN`, `## QUALITY check` with 22-row criterion table.
- `corpus/knowledge/source-locator-clarification-r15.json` (new): schema `tsukuroi-locator-clarification-v1`; exactly two corrections, seven keys each; no extra top-level keys.
- `.ufo/waves/round-15/build/LocatorEntry.md` (this report).

No other file edited. SOURCES/LOG/SCORECARD/SKILL/r14 pair untouched by this seat.

## Behavior

- R15-LOCATOR withdraws only the r14 supplemental locator `"rendered lines 1266-1267"` as reader-dependent, in `source-scope-correction-r14.md` source-object sentence, JSON `corrections[0].location` and `sources[0].anchor`. Active locator is the stable `SANDBOXING > ProtectSystem=` heading plus quote, footer revision and access date. The quote and proposition are not withdrawn.
- R15-POSITIVE-DOMAIN carries only the positive 11-word argument definition and the retained `full`/`strict` coverage teaching. The r14 negative clause is quoted, marked withdrawn/superseded; no exhaustive parser, documentation-absence or undocumented-value claim is made.
- Both corrections now carry the same verbatim 11-word r14 definition sentence, byte-aligned between MD and JSON (≤25 words); neither JSON `location` contains a line number. The LOC record's quote is the r14 located quote, so its replacement claim "the located quote and its proposition are unchanged" is literally true.

## Retained evidence

- Page: https://man.archlinux.org/man/systemd.exec.5, native HTML fetched 2026-10-20 over HTTPS, body 293394 bytes, footer `systemd 262.1`.
- § SANDBOXING, § ProtectSystem= first definition: `Takes a boolean argument or the special values "full" or "strict".` (11 words; the LOC and POS quote). Following sentence recorded as context only: `If true, mounts the /usr/ and the boot loader directories (/boot and /efi) read-only for processes invoked by this unit.` (20 words).
- Locator relies only on the heading path, the located 11-word quote, the footer version and the access date; no fragment or line-number fact is asserted.
- S046 row observed at `corpus/SOURCES.md:52`, kind docs, tier A, status mined; row authored by SourceRegistry, not this seat.
- r14 notices staged by ActiveRefs were read: MD `## R15 supersession` and JSON `r15_supersession` name both IDs and the canonical pair.
- Peer static reads: LocatorGate reports the pair matches the checker predicates as written; ReviewC1JSON confirmed MD/JSON LOC quote identity at the earlier 20-word form; ReviewGateRegistry then found the semantic mismatch (LOC quote was not the r14 located quote), fixed here by making both corrections carry the 11-word r14 sentence. No peer executed the checker; this is peer-reported, not an execution result.

## Recommendations

- Treat `SANDBOXING > ProtectSystem=` + the 11-word sentence + footer revision + access date as the canonical locator for S046; a future offset is admissible only with its reader/renderer named and a retained snapshot.
- Let L1 run `tools/check-locator-clarification.py` once at the integrated revision; do not widen the r14 checker, whose predicates do not cover this debt.
- Keep the positive definition as the admission basis; if a future round wants a completeness claim, it needs its own command, scope, date and sweep record.
- Do not tie the 262.1 footer to the installed host package; S046 is documentation evidence.

## Limits / risks

- 262.1 is the man-page footer revision, not an installed-package measurement; no host query was run for C1. Host package version and any renderer line offset are out of scope here.
- The r14 citation and the verifier lesson's reader place the entry at different offsets (both directly read); this pair therefore cites no offset and allows no corrected number as the active locator.
- Checker `tools/check-locator-clarification.py` was read statically but not executed; no PASS/red-green result is claimed. L1 owns execution and the final cross-file sweep.
- No package transaction, service action, sudo, snapper call, credential read, source-supplied command or verification run was performed. No child agent dispatched.
- Tools installed/updated: **none**.
