# tameshi-shokunin — Province

**Domain:** verification-fixture craft — the reusable method of honest
checks: hermetic suites, mutation testing, fail-closed arms, verdict-line
discipline, no-permissiveness audits, before/after proof.

**Owns:** the method, documented from the fleet's existing gates as primary
surfaces — `kumitate-shokunin/scripts/*` (six gates with selftest suites +
mutation controls), `kagi-shokunin/corpus/*check*.sh` + census gates,
`kaidoku-shokunin`'s audit-lane pattern (verify: lines, bit-exact evidence
ids), the game lanes' verifier-AGREE loops (fleet root `.ufo/waves/`).
Also: this lane's own corpus and gates.

**Refuses:** product domains — every lane's gate remains its own; tameshi
owns only the reusable craft (a pattern is admitted from evidence in TWO
independent lanes before it is claimed general). Never edits a sibling's
gate code (read-only probes; recommendations travel in round reports).
Credential material (→ kagi), endpoint health (→ kama).

**Out of province → report, never absorb.**

## Core / Frontier / Adjacent (fleet round 1, appended 2026-10-19)

Appended correction; lines 1-20 above are unchanged (they are cited by
line across the lane). Shape: canonical
`kimi-shokunin/templates/mint/PROVINCE.md:6-19`.

**Core** — the method above, plus every surface the lane has actually
measured or now governs: the six recorded mutation legs' gates as
read-only primary surfaces — kumitate `scripts/kimi-census.mjs` and
`scripts/claims-check.mjs`, kagi `corpus/surface-census.sh` and
`corpus/checklist-run.sh`, tsukuroi `tools/tsukuroi-census.sh`, mado
`tools/mado-verify.sh` (`tools/mutate-and-run.sh:84-89`; the "Owns" list
above names only kumitate, kagi, kaidoku and the game lanes — the
tsukuroi and mado gates entered through the round-5/6 service runs);
the mutation service and its opt-in protocol
(`corpus/knowledge/service-optin-protocol.md`); this lane's runner,
corpus and source registry (`corpus/SOURCES.md`).

**Frontier** — F1–F10 in `corpus/README.md` `## Frontier`; ground moves
to Core only through an admitted, source-headed `knowledge/` entry
whose `source:` cites a `mined` `SOURCES.md` row.

**Adjacent** — report, never absorb: every sibling gate's code and
product clauses (owner lane); credential material (kagi); endpoint
health (kama); visual/UI snapshot diffing (rejected row S030 — the
adjacent UI lanes); engine-specific nondeterminism (game lanes).

## Core — round 16 append (2026-10-20)

Appended; lines 1-47 are unchanged. The recorded mutation legs are now
**seven**, not six. The seventh is kumitate `scripts/round-gate.mjs` (rev
`364f1d5954158ef8844bca4a5fef57b05d2f2ca5`, blob sha256
`f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`), ledger leg
`js-round-gate`, probed read-only as a kumitate `scripts/*` primary surface.
It is not a service run and needed no opt-in. `tools/mutate-and-run.sh:84-89`
is the round-1 six-leg anchor; the seven-leg list now sits at `:85-91`.

Corrections to lines 8 and 35 above, appended:

- kumitate carries seven gates, not six: `sources-check.mjs` landed in kumitate
  `1a8eed5` (2026-10-19), after the line-8 survey (Overlap1, ProvinceBox4).
- The round-5 tsukuroi engagement was self-service; only the round-6 mado run
  was a service run (`corpus/knowledge/service-optin-protocol.md:36-37`).
- Line 26's template path resolves as
  `/home/vgpnk/Projects/kimi-shokunin/templates/mint/PROVINCE.md:6-19`.

Wave-2 correction to the round-16 append above (ProvinceAppend): "only the
round-6 mado run was a service run" holds for the round-5/6 pair only. The
round-8 kagi checklist sweep is also recorded as service form
(`corpus/knowledge/mutation-case-kagi-checklist.md:1,5-9`).

## Core — round 18 append (2026-10-20)

Appended; lines above are unchanged. The recorded mutation legs are now
**eight**. The eighth is kumitate `scripts/sources-check.mjs` (rev
`0acb7752d19058b953ebbeba253b1e35f6548de5`, blob sha256
`6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`), ledger leg
`js-sources-check`, probed read-only as a kumitate `scripts/*` primary surface
(lines 7-11); kumitate owns the gate and its contract `kumitate-sources-v1`
(kumitate `PROVINCE.md:15`). Not a service run; no opt-in needed. Survivor
recommendations travel to kumitate in the round report; tameshi never edits
the gate.

## Core — round 21 append (2026-10-21)

F5 finite environment-differential method enters Core through
`corpus/knowledge/hermetic-env-differential.md`, citing mined S079 and S028.
`tools/env-diff.py` compares the frozen nine-file population under seven
profiles; raw output variation and failed/unavailable controls remain
distinct from environment-sensitive outcomes. The six fleet-ledger gates,
reference runner and two later ledger gates are named in that entry and
`corpus/README.md` round21. Unmeasured kumitate survey gates and all other
environments remain unmeasured. No universal hermeticity or determinism
claim follows. The method is held; sibling gate ownership is unchanged.

## Core — round 25 append (2026-10-22)

Appended; lines above are unchanged. The report-interop half of F1 enters
Core through `corpus/knowledge/mte-report-interop.md`, citing mined S086 and
S087 (with S001, S002). `tools/mte-interop.py` emits the eight recorded
ledger legs as mutation-testing-elements reports and checks them with the
official 3.9.0 schema and metrics library. The report format and the official
library are read-only external surfaces; the lane owns only the export method.
NoCoverage classification stays frontier (F1b).

## Core — round 26 append (2026-10-22)

Appended; lines above are unchanged. The recorded mutation legs are now
**nine**. The ninth is kumitate `scripts/cite-check.mjs` (rev
`1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`, blob sha256
`40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`), ledger leg
`js-cite-check`, probed read-only as a kumitate `scripts/*` primary surface
(lines 7-11), entry `corpus/knowledge/mutation-case-kumitate-cite-check.md`
(S088, S089). Not a service run; no opt-in needed. Kumitate owns the gate;
survivor recommendations travel in the round report. Line 101 above ("the
eight recorded ledger legs") reads nine from round 26 on: `tools/mte-interop.py`
now judges all nine.
