# ActiveRefs — round-14 active-reference supersession repair

Seat TsukuroiR14.ActiveRefs (executor), baseline `8606bad4cbc6451ac2890c9f8e2548a36c386db6`.
Append-only routing of R14-VALUE-DOMAIN (S044) and R14-COMMENT-ATTRIBUTION
(S045); no historical bytes rewritten; no gate/build/test/lint/formatter/smoke run.

## Files changed (absolute)

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/root-dac-correction-r13.md`
  — named notice immediately after the provenance trio; appended `## R14 named
  corrections`. Supersedes the MD:97 value-domain cell and the JSON
  `replaced_b2_claims[0]` “option set is not an exhaustive list” ambiguity
  (mechanism examples are non-exhaustive, not the domain or spellings), the
  QUALITY #18 “model triage” clause, and the stale `sources[0]`/`gate_contract`
  readings. S043 stays valid; #6634 deferral vs #8047 reporter wait stated.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/root-dac-correction-r13.json`
  — additive top-level `r14_supersession` (`tsukuroi-r14-supersession-v1`):
  active_corrections, two superseded_loci (MD:97 + JSON:120 twin),
  superseded_contract_values for `sources[0].status`,
  `sources[0].registry_owner`, `gate_contract`, `historical_bytes_preserved`.
  Read-only `jq` parse observed ids exactly the two named, 2 loci, original
  values still `reserved`/`SourceRegistry`/10 headings, new keys exactly the
  seven listed.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-13.md`
  — two append-only attribution notices: before the historical “Rejected: an
  automated `omarchybot` …” paragraph (old line 17) and before the S042 table
  row plus collective-attribution paragraph; row, quote and prose preserved.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md` — round-14 errata
  after the round-13 section.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md` — one round-14
  erratum paragraph.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/README.md` — round-14
  section; round-13 “bot-authority limits” routes to the explicit
  comment-scoped limit.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/snapper-eacces-mechanism.md`
  — round-14 erratum; no procedure added; routes to `SKILL.md:1742-1750`,
  excludes `snapper list-configs`/raw `systemctl cat`, adopts no comment command.
- This report.

## Behavior / active routing

Active pair `corpus/knowledge/source-scope-correction-r14.md` / `.json`.
Superseded: only the two named loci and the metadata/gate-description contract
values. Preserved: S042 immutable row, S043/#6629 disclaimer, host-cause and
maintainer-acceptance rejections, ProtectSystem full/strict teaching, alternate
mechanisms, resolved-parent reading, fixture identity, unknown history.

## Retained evidence

- Read, not edited: `corpus/lessons/round-13-verifier-spotcheck.md:143-165`
  (two defects) and `:243-252` (metadata/gate routing).
- S044 wording per shared interface: ProtectSystem is “a boolean argument or
  the special values "full" or "strict"”. S045: login `omarchybot`, type
  `User`, association `COLLABORATOR`; body VM assertion unverified, Codex
  Medium second opinion, deferral. I did not reopen either URL; source seats
  own fresh access.
- `corpus/lessons/round-14.md`: deferral refers to #6634; #8047 ends “This now
  waits on your answer.” Repo data, no instruction executed.
- JSON integrity: `jq` read-only parse values above (not the lane gate).

## Risks / limitations

- The r14 pair did not yet exist when this seat wrote; pointers are forward
  references per shared interface. Reconcile path/ids/fields if CorrectEntry's
  output differs before commit. I sent CorrectEntry a coordination note.
- “Append errata to the r14 correction” was implemented as errata in the swept
  files routing to the pair, because the pair is outside this seat's write set;
  L1 can lift the notice text into the pair.
- `MD:97` / `JSON:120` are round-13-revision loci; the insert shifts current MD
  numbering and the JSON pointer says so.
- No LOG, SCORECARD, QUALITY, SOURCES or external verifier file touched. Fresh
  source agreement and census were not measured here.

## Tooling

None installed/updated. No privileged probe, package transaction, service
operation or snapper invocation.
