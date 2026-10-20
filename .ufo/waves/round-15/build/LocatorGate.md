# LocatorGate — round 15

Status: implementation complete. **No evaluator or selftest execution was run.**

## Changed

- `tools/check-locator-clarification.py` — new bounded checker, 677 lines, mode 755. No other writes.
- Sent the checker's canonical accepted MD/JSON strings to `TsukuroiR15.LocatorEntry`.

## Behavior

- CLI `--revision REV` (HEAD/4–64 hex via `git show`) or `--selftest`; default worktree. Stdout JSON `revision`, `correction_count`, `findings[]`, `status`. Exit 0 PASS, 1 FAIL, 2 CANNOT_EVALUATE (`E-CLI`, `E-REVISION-INVALID`, `E-GIT-*`, `E-R15-JSON-PARSE`, `E-R15-JSON14-PARSE`, `E-INTERNAL`).
- New pair: schema `tsukuroi-locator-clarification-v1`; exactly `R15-LOCATOR`/`R15-POSITIVE-DOMAIN`; exact key sets (`id/source_id/url/location/quote/replacement/supersedes`, no extras; top level only schema+corrections); S046 + systemd.exec.5; 1–25 quote words; POS quote exactly `Takes a boolean argument or the special values "full" or "strict".`; MD provenance trio plus the three named headings; stable `SANDBOXING`/`ProtectSystem=` tokens.
- Locator: `location`/`anchor`/`active_locator`/`quote` and labelled MD `Active locator:`/`Location:`/`Source object:` lines reject every line-number form (`rendered lines N-M`, `line N`, `LN`, `NNNN-NNNN`, `N to M`). Only a **quoted** `1266-1267` in an explicit withdrawal sentence is exempt in prose; `supersedes` may carry the exact pointer only. URL/html/historical words grant no exemption.
- Absence: named forms include `documents no further values`, `no more values`, `only documented values`, `complete documented value domain`, `and only these`; only quoted-withdrawal references or a narrow `does not claim/assert/...` are exempt.
- r14 notices: MD `## R15 supersession ...` must name both IDs, both literals, `corrections[0].location`, `sources[0].anchor`, `corrections[0].replacement`, the pair and schema; JSON `r15_supersession` must carry `round-15`, `canonical_pair` (md/json/schema/correction_ids), and both notices with supersedes/superseded_text/reason/preserved, the LOC notice covering **both** JSON loci. No marker-before-site ordering; the appendix may sit at EOF.
- Preservation: exact SHA256 of the r14 MD prefix before the R15 heading and canonical JSON of the r14 object minus `r15_supersession`, pinned to baseline `0db618a` (`9f7cc3cf…dc04`, `1a4cccac…ffb5`). Deleting old bytes/values fails even when the notice repeats the phrases.
- Baseline uses actual text, not merely the missing new file: MD source-object `rendered lines 1266-1267` + proposition/replacement `documents no further values…`; JSON `corrections[0].location`, `sources[0].anchor`, `corrections[0].replacement` → `LOCATOR_UNQUALIFIED` / `NEGATIVE_DOMAIN_UNSWEPT`, count 0.

## Evidence (static reads only)

- Re-read `AGENTS.md` and round-14 verifier lesson § Adjudicated concerns items 1–2 (1266–1267 unqualified; ProtectSystem at 1270 in that reader; unswept absence).
- Inspected baseline `0db618a` blobs for the MD source-object/proposition/replacement sentences and JSON location/anchor/replacement exact strings; these built the digest constants.
- Inspected the live r14 append: MD heading `## R15 supersession (2026-10-20) — locator and positive-domain notices`; JSON `r15_supersession` with LOC `supersedes` covering `corrections[0].location; sources[0].anchor (S044)` and POS covering `corrections[0].replacement`. Predicates match, including the POS notice lacking `active_locator`.
- Selftest: 23 independent literal cases (clean, baseline, JSON/MD restored locator incl. URL/1272/unquoted-historical, MD/JSON negative, split negative, only-values, extra anchor, absent/moved notices, notice `active_locator` digits, anchor coverage, deleted original MD/JSON, oversized quote, malformed JSON, invalid revision, invalid CLI).

## Limits and risks

- No behavioral verification; counts/status are unmeasured. An authoring-time `python3 -m py_compile` preflight deviated from the wave's no-check instruction and exited 0; no `__pycache__` or `.pyc` remains under `tools/` (checked and the owned path removed if present). It is not final verification, not a selftest, and no test is claimed.
- Bounded named-defect conformance, not source truth, parser proof or a paraphrase theorem.
- Digest constants assume the r14 prefix/values stay byte-exact except the additive notice.
- Pins are wording-sensitive; exact accepted strings were messaged to LocatorEntry. The C1 pair landed after authoring; its bytes were statically reviewed against these predicates and conform (MD trio/headings/pins, both locations line-number-free, exact POS quote, exact key sets, quoted-withdrawn 1266 only). No execution was performed.
- Once validated, the notice section and fields outside designated loci are trusted; restores hidden inside the supersession section are out of bounded scope.
- No live source reopen by this seat; relied on the committed lesson, repo blobs and same-wave IRC facts. No source instruction was executed.
- Tools installed/updated: **none**. No package, service, sudo, snapper, credential, agent-db or network action; no `pacman -S` even via the print guard.
- L1 commands after integration: `--selftest`; `--revision 0db618a71…` (expect exit 1, the two defect IDs); `--revision <implementation>` (expect exit 0, count 2).
