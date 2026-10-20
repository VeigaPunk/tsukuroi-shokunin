# CorrectionGate — round 14 source-scope conformance checker

status: implemented, not executed (L1 owns all runs).
write: `tsukuroi-shokunin/tools/check-source-scope-correction.py` (new, only file changed).
## Contract

- CLI: `--revision REV` (`HEAD` or 4-64 hex, resolved to a commit; committed blobs) or
  `--selftest` (in-memory literals only). Default reads the worktree.
- Exit `0` clean / `1` failed / `2` cannot evaluate. Malformed CLI emits `E-CLI` JSON and exits 2;
  invalid revision `E-REVISION-INVALID`; read/IO/git failures `E-READ-FAILED` /
  `E-GIT-READ-FAILED` / `E-GIT-TIMEOUT`; malformed r14 JSON `E-R14-JSON-PARSE`; unexpected
  evaluation errors bounded `E-INTERNAL` (no traceback exit 1).
- stdout JSON, stable keys: `status`, `revision` (`worktree` or resolved commit),
  `correction_count` (0..2), `findings[]` of `{id, site, detail}` sorted by id/site/detail.
- Missing r14 files at a baseline revision are FAIL (`R14-MD-MISSING` / `R14-JSON-MISSING`),
  not CANNOT_EVALUATE.
## Predicates (bounded, not semantic)

- JSON: schema `tsukuroi-source-scope-correction-v1`; `corrections` exactly two objects; fields
  id/supersedes/source_id/url/location/quote/replacement; ids exactly `R14-VALUE-DOMAIN` +
  `R14-COMMENT-ATTRIBUTION`; S044 + systemd.exec.5 / S045 + exact comment endpoint; supersedes
  r13 MD:97 / S042; quote 1..25 whitespace words.
- Domain pins: `ProtectSystem=`, documented values/domain, boolean, full, strict, non-exhaustive
  scoped to mechanisms/examples. Attribution pins: comment id, User, COLLABORATOR, unverified,
  Codex, second opinion, maintainer deferral, rejected host cause.
- MD: `source:` / `verified-at:` / `recheck:` first; three named headings; section pins;
  `recheck:` must not name snapper/sudo/systemctl/journalctl/pacman; theorem/guarantee language
  rejected unless locally negated.
- History: r13 row `| r12 MD:41-42 | ... the value set is not exhaustive` and the lesson
  `self-described model-generated triage from an API account` must remain; a removing edit yields
  `R14-HISTORY-REWRITTEN` / `R14-LESSON-HISTORY-REWRITTEN`.
- Notices: marker must precede the historical site; r13 notice needs the ID, a 97/r12 MD:41-42
  pointer, supersede wording and value-set language; lesson notice needs the ID, S042+S045,
  supersede wording and an explicit self-description denial.
- Registry: S042 historical fields unchanged (`R14-SOURCES-IMMUTABLE`); S045 must start
  `supersedes S042`, be community/C rejected, carry the comment id, explicitly deny the
  self-description, and distinguish `unverified` plus second-opinion/Codex and host-cause rejection
  (`R14-SOURCES-SUPERSESSION`).
- Restoration: exact old domain phrase in replacement, or `self-described ... model-generated /
  automated triage` in replacement or an unmarked MD paragraph, fails
  `R14-VALUE-DOMAIN-RESTORED` / `R14-COMMENT-ATTRIBUTION-RESTORED`.
- Baseline without notices yields stable `VALUE_DOMAIN_OVERCLAIM` and
  `COMMENT_ATTRIBUTION_OVERCLAIM`.
- `correction_count` is per-site resolution: valid correction object + notice + retained historical
  phrase + target (S045 relation for attribution) + no MD site finding. It is not `len(corrections)`.
- Disclaimer transfer: only the exact `nothing was run` S043 phrase is rejected; mere
  `#6629 is separate / not transferred` wording is allowed.
## Selftest (14 independent literal cases, exact ID sets + counts)

baseline (7 IDs, 0), clean (none, 2), restored-domain (PIN+RESTORED, 1),
restored-attribution (PIN+RESTORED, 1), missing-notice (4 IDs, 0), malformed-json
(E-R14-JSON-PARSE, 0), oversized-quote (R14-QUOTE-WORDS, 1), sources-immutable
(R14-SOURCES-IMMUTABLE, 2), wrong-id (R14-CORRECTION-ID, 1), top-level-array
(SCHEMA+COUNT+ID, 0), recheck-host-command (R14-MD-RECHECK, 2),
history-domain-rewritten (REWRITTEN+NO-NOTICE, 1), lesson-history-rewritten
(REWRITTEN+NO-NOTICE+OVERCLAIM, 1), notice-after-site (NO-NOTICE+OVERCLAIM, 1).
## Static read of landed integration (gate not run)

- `corpus/knowledge/root-dac-correction-r13.md:5` notice precedes the MD:97 row and contains
  R14-VALUE-DOMAIN, r12 MD:41-42, supersede and value-set wording. `corpus/lessons/round-13.md:17,66`
  notices precede the preserved paragraph with R14-COMMENT-ATTRIBUTION, S042/S045 and a denial.
- `corpus/SOURCES.md:51` S045 is community/C/rejected, starts `supersedes S042`, includes comment
  6071740243, an explicit denial, `unverified`, second opinion and host-cause rejection; S042 retains
  its original phrase.
- `source-scope-correction-r14.{md,json}`: two corrections, exact URLs/supersedes, quotes 11 and
  9 words, replacement pins present; no active restored phrase in a static read. On that reading the
  gate should resolve both sites (count 2); static compatibility, not a measured PASS.
## Limitations / risks

- Conformance only: no source truth, quote wording or #6634-referent check; DomainCritic/QuoteReview
  carry those readings. The gate reads local blobs; S045/registry claims are not checked against GitHub.
- Notice position is enforced (marker before historical row): moving a notice after its defect row
  turns the gate red; current placement satisfies it.
- Replacement token pins are deliberately lexical; alternative phrasing outside the pinned
  vocabulary fails rather than being silently admitted.
- Size: 474 non-blank lines including 14 fixtures and cannot-evaluate guards, above the 250-line
  preference; kept for explicit contract coverage rather than abstraction.
## Tooling record

installed/updated: none.
