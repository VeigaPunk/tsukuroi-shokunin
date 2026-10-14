# SHONEN — tsukuroi-shokunin (probation checklist)

Seed checklist (verbatim shape per PROTOCOL.md; `<name>` -> tsukuroi):

- [~] SKILL craft — `SKILL.md` holds real decision tables / error patterns /
  checklists for the domain, every rule citing a source (asserted by the lane,
  TSUKUROI-B4 scribe 2026-10-14; evidence: 5-plane `HEALTHY`/`DEGRADED`/`BLOCKED`
  decision table incl. the journal/boot row `SKILL.md:43`, the 11-step
  update-safety checklist, census-gate semantics + round-3 append
  (`SKILL.md:447-543`: census-v2 sync, journal field map, post-verdict contract,
  executor checklist) — every rule cited to `corpus/knowledge/*.md`, whose md5s
  the round-3 report §5 pins and this scribe re-hashed reproducibly
  (2026-10-14 15:55Z); round-1 audits re-verified anchors+counts (commit
  `55b2186`); citations executed end-to-end by the round-3 no-oral-context test
  (`corpus/knowledge/executor-test-sufficiency.md` §3-§4). `[x]` owed to the
  non-author promotion review.)
- [~] End-to-end task — one domain task executed start-to-finish and logged
  (asserted by the lane, TSUKUROI-B4 scribe 2026-10-14; verifier of the run:
  the e2e report's own measured read-only contract + this scribe's re-runs;
  evidence: `corpus/knowledge/host-health-report-r3.md` — census-v2 + four
  plane notes + update-safety note driven into one host-health snapshot,
  verdict board over 5 surfaces, 20 finding→action pairs, 15-row unknowns
  register; logged in `LOG.md` round 3; scribe re-ran the gate + headline
  probes 2026-10-14 15:55Z — selftest 26/26 rc=0, live rc=1 DEGRADED, counts
  drifted as the live coredump storm predicts, zero repo mutation
  (`/tmp/tsukuroi-b4-r3b-scratch/`, ephemeral). `[x]` owed to the non-author
  promotion review.)
- [~] No-oral-context — a fresh agent can execute the instructions from
  `SKILL.md` alone (asserted by the lane, TSUKUROI-B4 scribe 2026-10-14;
  verifier of the test: the executor seat ran census-v2 with `SKILL.md` as the
  only reference, 2026-10-14T15:25Z — record
  `corpus/knowledge/executor-test-sufficiency.md`, per-step tally 7 SUFFICIENT
  / 3 PARTIAL / 3 MISSING; the gaps were v1-vs-v2 staleness, fixed same round
  by the `SKILL.md` round-3 append (census-v2 pins, journal field map,
  post-verdict contract, executor checklist); **post-append re-test not yet
  run** — this box asserts the corrected document, the record keeps the
  pre-fix tally. `[x]` owed to the non-author promotion review, which should
  include that re-test.)
- [~] PROVINCE accuracy — `PROVINCE.md` matches observed reality; no
  cross-domain bleed (asserted by the lane, TSUKUROI-B4 scribe 2026-10-14;
  evidence: `PROVINCE.md` unchanged since round 0 (`git log --follow
  PROVINCE.md` = `aea5fa2` only) and matches measured reality — package/
  systemd/journal-boot/driver probes answer as owned; round-3 work honored the
  boundaries: all probes read-only, privilege gates (`/boot`, crypttab, dmesg)
  recorded BLOCKED never escalated, coredump storm / `walker-restart.hook` /
  GSP questions reported to owning lanes, not absorbed
  (`host-health-report-r3.md` §2.4 J1, U7, unknowns 5+13;
  `journal-boot-plane.md` §3.1, §7). `[x]` owed to the non-author promotion
  review.)

Header pins: PROTOCOL.md lines 419-428 (seed), lines 430 (mark spec).
