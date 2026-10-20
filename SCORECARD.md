# tsukuroi-shokunin — Scorecard

Lane axes per AXES.md (six-axis vocabulary; primary verdicts per
LEARNING.md trends). Probation rounds 1–3 built the initial measurements;
rounds 4–11 extended them. **This is the terminal refresh** (SCR-S11, the
closeout round — lane round 11 = training r10): the final axes table and the
closeout move-log row land here; the r1–r10 move rows are kept as landed, and
rows 16/21/22 are paren-repaired with their original text preserved.
State at writing (2026-10-14 22:19Z, SCR-S11): repo HEAD `af8adf1`
("probation round 10 (training r9)") with the round-11 work uncommitted in
tree — `git status --porcelain` reads ` M LOG.md`, ` M SCORECARD.md`,
` M SKILL.md` (S11-4's terminal append + post-write addendum, md5 `f7d2be485e11…`, 1631 `wc -l`),
`?? corpus/knowledge/closeout-r11.md`, `?? plans/completion-evidence.md`,
`?? reports/r11-aud-s11.md`; the round-11 integration commit is owed at write
time (round-3 pattern). Counts at that stamp: census md5 `945c76fc…` / 2402 `wc -l`
(selftest executed 80/80 rc=0 by this record); notes 24 (`ls
corpus/knowledge/*.md | wc -l`); `corpus/lessons/` 0 files; the owed contract
items are named in `plans/completion-evidence.md` §3 and this record's LOG
entry.

## Move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 1 | operability | round-0 seed: 22-line `SKILL.md`, 2 headings, no decision table, no runnable probe set (`git show aea5fa2:SKILL.md`) | 5-plane health-verdict decision table (`HEALTHY`/`DEGRADED`/`BLOCKED`) + 11-step read-only update-safety checklist; every command exercised read-only. Scribe re-run 2026-10-14: `pacman -Q \| wc -l`=1188, `-Qe`=207, `-Qm`=16, `-Qdt`=3 (electron39, mbedtls, webp-pixbuf-loader), `pacman -Dk`→clean rc=0, `systemctl --user is-system-running`=running, failed units=0, `journalctl -b -p err -o json --no-pager \| wc -l`=238, `nvidia-smi --query-gpu=name,driver_version --format=csv,noheader`→`NVIDIA GeForce RTX 5070, 610.57.04`, `dkms status`→stale 7.1.4 registration + current 7.2.3 installed | commands as listed (re-executed, not quoted); notes `corpus/knowledge/*.md`; full `-Qkk` sweep re-run rc=1, 1332 lines, ~15 s |
| 1 | freshness | none — lane's first verification pass; no prior measurements to re-check | every SKILL claim anchored to a `corpus/knowledge/` note with measured date + section-level sources; 4 self-corrections landed as append-only errata (sync-db mtime→birth, journal line→entry count, unit-file count 136→133, rollback-net inference retracted). Scribe re-runs reproduce headline values: `stat -c '%w %n' /var/lib/pacman/sync/*.db`→births 2026-10-11 12:54:13.542 (core/extra/multilib/omarchy), `pacman -Qu`→empty rc=1, `pacman-conf IgnorePkg IgnoreGroup`→empty, `ls /var/lib/pacman/db.lck`→absent, `snapper list-configs`→empty; full `-Qkk`: 19 nonzero summaries (18 clean + `cups-browsed` summary split by `\r` interleave) — reconciles note's 18 with TSUKUROI-4's 19 | commands as listed; errata sections of the three notes; `SKILL.md` errata/pending block |
| 2 | operability | round-1 end: verdict vocabulary + decision table existed only as prose (`SKILL.md`, 232 ln) — no command could emit a verdict; each plane had to be probed by hand from the checklist | first executable gate: `tools/tsukuroi-census.sh` census-v1 — `TSUKUROI_CENSUS: HEALTHY`/`DEGRADED`/`BLOCKED`, exit map 0/1/2 (worst-plane rollup); hermetic `--selftest`: **17 cases, 17 passed, 0 failed** (rc=0), fixture byte-unchanged asserted (zero mutation). Scribe live re-run 2026-10-14: rc=1 → `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED)`; packages sample drift 2 (`1password-beta`, `1password-cli`), foreign 16, pins none, holds `pacman glibc`; systemd running, 0 failed, 1/1 enabled timer success; drivers ring `journalctl-k` (`dmesg_restrict=1`), `kerr=38` (oom=1 io=35 gpu=0 other=2), nvidia present, smi 610.57.04, modules 4, nodes 6, pci_10de 2 | `bash tools/tsukuroi-census.sh --selftest` and `bash tools/tsukuroi-census.sh` re-executed by TSUKUROI-SCR 2026-10-14 (raw output `/tmp/tsukuroi-scr-r2b/{selftest,live}.out`); companion note `corpus/knowledge/update-safety-note.md` (TSUKUROI-R2-2); plan `plans/round-2.plan.md` |
| 3 | freshness | round-2 end: the journal/boot plane rested on round-1 single-boot captures — the boot-gap question an open [inference] at `SKILL.md:43` (resume artifact vs journal flush/mount delay), no journal arms in the gate, coredump count a days-old figure (198), failed-service history never swept | the journal/boot plane measured for all **13 retained boots** (`corpus/knowledge/journal-boot-plane.md`, TSUKUROI-R3-1): per-boot err census 1–168 (boot 0 storm-dominated), **kernel phase = first-record monotonic − 0.81…0.84 s (12/12 boots)** with boot 0 wall-clock cross-anchor ±1 s — the 4 m 03 s kernel phase is real elapsed time; var-log.mount delay refuted (mount at userspace 2.845 s, after PID1 logging starts), leading hypothesis now initramfs/LUKS dwell [inference, unproven; crypttab BLOCKED]; failed-service history **0 unit failures in 13 boots**; timer drift 5/5 success inside declared windows; stale figures re-measured instead of quoted — coredumps 198→208→211→220→224 and err 247→251→260→339 across the day (live storm; every count a capture), coredump dir 3.9 G→4.1 G, drivers `other` class 2→65 (15:55Z) — and the plane joined the gate (census-v2), making this freshness move executable: `bash tools/tsukuroi-census.sh` | scribe re-runs 2026-10-14 15:55Z (`/tmp/tsukuroi-b4-r3b-scratch/probes.out`): `journalctl --list-boots --no-pager \| wc -l`=14, err entries=339, kernel err=101, `coredumpctl list --since "2026-10-13 10:57:58" --json=short --no-pager \| jq length`=224, `systemctl is-system-running`=running + 0 failed, `snapper list-configs` header-only rc=0, `systemd-analyze` line byte-identical, `journalctl --disk-usage`=181.3 M, coredump dir 4.1 G; note 411 ln, md5 `16d4047e8b03deec69773d2cc0b1b75c` |
| 3 | depth | round-2 end: plane knowledge lived in five notes + a three-plane gate — no artifact executed the domain task start-to-finish (verdict → measured evidence → operator action), and a post-verdict contract existed nowhere in the lane | the e2e SHONEN task landed (`corpus/knowledge/host-health-report-r3.md`, TSUKUROI-R3-3): census-v2 + four plane notes + update-safety note driven into one host-health snapshot — verdict board over the 5 surfaces (packages DEGRADED, systemd HEALTHY, drivers DEGRADED, journal DEGRADED, update-safety DEGRADED), **20 finding→action pairs** each carrying measured evidence + exact operator unblock (P1–P5, D1–D3, J1–J5, U1–U8), HEALTHY receipts, 15-row unknowns register with owners, measured read-only contract, per-artifact provenance (md5 + lines); companion no-oral-context test (`executor-test-sufficiency.md`, TSUKUROI-R3-4) ran the gate from `SKILL.md` alone — 7 SUFFICIENT / 3 PARTIAL / 3 MISSING, the gaps being exactly the v2 coverage landed same round as the SKILL round-3 append (census-v2 sync, journal field map, post-verdict contract, executor checklist); the dispatch's "20-min cap" item recorded as unresolved, not invented | provenance re-verified by TSUKUROI-B4 scribe 2026-10-14 15:55Z (`/tmp/tsukuroi-b4-r3b-scratch/provenance.out`): all report §5 md5s reproduce (census `41953ee9…`, journal `16d4047e…`, package `24eafc40…`, systemd `26dca9cf…`, driver `a44e9c07…`, update-safety `5cc3067f…`), line counts 976/411/303/247/242/478, HEAD `SKILL.md` = `f80b4afd…` (the round-2 revision the test consumed); live verdict line reproduced rc=1 DEGRADED with drifted counts (err 339, kerr 101, coredumps 224); `pacman -Qkk 1password-beta 1password-cli` rc=1 (1 altered each), foreign=16, installed=1188, dkms stale 7.1.4 row present, `-Qu` rc=1 empty, sync-db births 2026-10-11 12:54:13.542 |
| 4 | freshness + depth | round-3 state | boot plane (299 L) | wave-4 32-lane; VER-S1 |
| 5 | adjacency + operability | round-4 state | own-gate mutation sweep via tameshi's tool (23 defects: 13 killed/10 survived) + 9 hardening selftest cases landed (26->35) | wave-5 32-lane |
| 6 | coverage + freshness | round-5 state | the AUR-risk plane (all 16 foreign packages per-package measured) | wave-6 32-lane (2 lanes rerouted alibaba->hyper) |
| 7 | coverage + operability | round-6 state | AUR watch arm + OOM/memory-pressure arm landed in the census (49 selftest cases) | wave-7 32-lane (3 rerouted alibaba->hyper) |
| 8 | operability | round-7 state | the VER-S8 GAP CLOSED: the OOM/memory arm independently verified (11-mutant replay, 8/8 own-case kills, 9 un-exercised clause sites named as coverage debt) | wave-8 32-lane (2 rerouted alibaba->hyper) |
| 9 | coverage + operability | round-8 state | the 5-plane census landed (update-safety arms — the r7 AUD-X7 gap closed) | wave-9 32-lane (2 rerouted alibaba->hyper) |
| 10 | calibration | round-9 state | the calibration synthesis (measured-vs-believed ledger) | wave-10 32-lane (1 rerouted alibaba->hyper) |
| 11 | operability (terminal closeout) | round-10 state | the terminal closeout: `corpus/knowledge/closeout-r11.md` (S11-1; md5 `d59da63f…`, 403 `wc -l` — the arc 3→4→5(uncommitted, ~12 min)→6 committed planes, the standing cadence, the elevation-gated register) + `SKILL.md` round-11 terminal append + post-write addendum (S11-4; md5 `f7d2be485e11…`, 1631 `wc -l` — handoff pointer, final identity pin, count restatements, terminal-contracts table, D13) + `reports/r11-aud-s11.md` (AUD-S11; both bound claims PASS, drift recorded) + `plans/completion-evidence.md` (PACK-S; contract items L1–L10 measured) + this record: rows 16/21/22 paren-repaired (text verbatim) + the final axes table; owed and named: runbook (HANDOFF.md never realized — `closeout-r11.md` is the reader artifact), PROVINCE Core/Frontier/Adjacent, SHONEN diff, `corpus/lessons/round-11.md`, README rows + `## Frontier`, the non-author runbook test, the landing commit | wave-11 32-lane; VER-S11 (verdict in scratch — no repo report) · AUD-S11 · PACK-S · S11-1 · S11-4 · SCR-S11 (this record) |

## Axes — final self-assessment (landed round 11; each score carries its counting command; measured at `af8adf1` plus the uncommitted round-11 artifacts)

Scores are the lane's first explicit axis scores (rounds 1–10 carried no
numeric scores); each is bounded by its stated ceiling, and the counting
commands were re-executed in this record's window (2026-10-14 21:38–22:11Z).

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 24 notes (`ls corpus/knowledge/*.md \| wc -l`); census 2402 `wc -l` / 80 executed cases (`bash tools/tsukuroi-census.sh --selftest`, re-run by this record) with in-source case labels; `SKILL.md` 1631 `wc -l` / 55 table lines (`grep -c '^\|' SKILL.md`), every rule cited to `corpus/knowledge/*.md`. Ceiling: the r8 sweep's 9 un-exercised clause sites; `corpus/lessons/` never written (0 files). | r4 |
| coverage | 8 | 6 gate planes == the surfaces `PROVINCE.md` owns, each with a landed note — six `PLANE` emitters (`tools/tsukuroi-census.sh:2377-2382`) == six rollup keys (`:2392`); corpus covers AUR/memory/kill-event/boot classes beyond the r1 five. Ceiling: `PROVINCE.md` Core/Frontier/Adjacent not landed; `corpus/README.md` rows stop at r3 (`98bd0066…`, 20 `wc -l`). | r9 |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` → rc=0 `PASS (80 cases, 80 passed, 0 failed)`; `bash tools/tsukuroi-census.sh` → rc=1, six-plane rollup (both re-executed by this record); zero-mutation contract held (`git status` byte-identical; `db.lck` absent). Arc: r2 first gate → r3 census-v2 → r5/r10 hardening (17→26→35→49→74→80 cases) → r7/r9 arms and planes. Ceiling: D12 `--identity` not landed (three-command re-derivation stands). | r11 |
| freshness | 8 | every round's record re-ran its predecessor's pins (LOG rounds 1–10; this record re-ran the gate + probes); receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md`, `closeout-r11.md` §5 recheck block. Ceiling: counts are live captures (coredump dir 764 files / 3.8 G this window); the r10 receipt's own pins were superseded inside its commit — recorded as drift, not smoothed. | r6 |
| calibration | 9 | `calibration-synthesis.md` (463 `wc -l`) — the claim→re-measure→append→supersede→rule loop with its mismeasure rows; errata kept visible rather than rewritten (r1's four retractions; the "5-plane" numerals; the AUD-X7 credit correction — appended precision in this record's LOG entry); `closeout-r11.md` §3 register. Ceiling: the D13 verification debts still open (`closeout-r11.md` §3.2). | r10 |
| adjacency | 7 | reported-not-absorbed rows across the arc: coredump storm → journal workstream + the godot/node/LOVE app lanes; `walker-restart.hook` root-exec → kagi/operator; GSP selection → kaidoku/revenger; contested scope reported, never absorbed (`closeout-r11.md` §3.2; LOG rounds 1–10). Ceiling: no formal overlap table. | r5 |

## Planned / retired

- **planned:** none — the training ladder ends at round 11 (this lane's dispatch frame; nothing here presumes a round 12). The open set — contract items L1–L5/L9 (L6–L8 realized this write: SCORECARD, the SKILL append, the LOG entry), the elevation-gated register, the D13 verification debts, the host unknowns — is enumerated with owners in `plans/completion-evidence.md` §3/§5 and `closeout-r11.md` §3, carried by this record's LOG entry.
- **retired:** none — no axis saturated; none a wrong fit; all six carry landed artifacts.

## Interactive fleet-round-1 continuation — blocked pre-dispatch (2026-10-15)

This appendix supersedes only the old **planned: none / ladder ends** instruction
at lines 54–57 for the current operator program. Historical move rows, scores,
errata and their evidence remain intact. Baseline HEAD:
`0ecf3ff1b0aa312d71899581badc5a9798430369`. The headless launch counter `1`
is not a verified completed-round count. Continue pending **fleet round 1**;
do not relabel it historical round 12 or reuse historical training round 1.

Lowest LIVE axis: **adjacency (7)**; none retired. Intended move: finish the
source-backed analysis-recipient contract and sanitized handoff, then admit only
after a complete authorized 32-seat wave, parent verification and landed report.
Plan: `.ufo/plans/fleet-r1-interactive-wwkd.md`.

| Axis | This attempt's verdict | Evidence / retained ceiling |
|---|---|---|
| depth | unchanged | No new domain implementation or admitted knowledge; inherited corpus stays uncommitted. |
| coverage | unchanged | Same owned OS surfaces; no domain expansion or sibling scope absorbed. |
| operability | unchanged | Existing script unchanged at SHA-256 `1045244387ffcd5d3db481dd0d3d30e34097abc24744d954e791b81d28b20c11`; selftest exit 0, live census exit 1. Re-measurement is not a new gate behavior. |
| freshness | unchanged | Fresh parent captures and source drift are supplemental preflight evidence, not an admitted corpus refresh. |
| calibration | unchanged | No newly independent verifier, promotion credit or re-certification of the legacy numeric scores. |
| adjacency | unchanged | Required wave could not be dispatched through authorized roles; inherited contracts/packet have not been integrated or admitted. |

No scalar replaces these verdicts. Historical ordinal scores stay as previously
reported, **not freshly certified**. No axis is marked harmed by this
preflight-only record; no improved verdict is established, so no round is admitted.

Measured artifact counts, not gain claims:

- `git cat-file -e 0ecf3ff1b0aa312d71899581badc5a9798430369:corpus/knowledge/adjacency-handoffs-fleet-r1.json`
  exited **128**, explicitly naming the path absent from that commit: **0**
  records in this new ledger at the baseline, not zero historical handoffs.
- The inherited `jq` completeness predicate prints **7**, exit **0**, over the
  current uncommitted ledger. Full command/output:
  `.ufo/evidence/fleet-r1-interactive/contract-count.json`. Seven records are not
  seven delivered packets or verified rounds.
- Canonical wave `plan` validation exited **0**, spawn/resume/total **32/0/32**,
  with **32 distinct tasks**. `.ufo/waves/fleet-r1-interactive/plan.validated.json`
  is a plan, **not a launched wave**; native task calls **0**.
- `bash tools/tsukuroi-census.sh --selftest`:
  `TSUKUROI_CENSUS_SELFTEST: PASS (80 cases, 80 passed, 0 failed)`, exit **0**.
- `bash tools/tsukuroi-census.sh`:
  `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=HEALTHY)`,
  exit **1**. Complete emitted summaries/verdicts and stderr are in
  `.ufo/evidence/fleet-r1-interactive/{selftest,live}.json`; raw journal bodies
  are not published. Measurements are against the unchanged script at the
  baseline above, before this record's commit.

Learning trends: **expansion unchanged; quality unchanged; discernment unchanged**.
No new material is admitted, and no non-author admit/reject spot-check occurred.
SHONEN evidence remains author-side `[~]`; nothing is promoted.

### Named debt and next fresh-session action

1. **ROUTE-BINDING / operator or routing integrator.** Effective content roles:
   executor `@m_mid`, scribe `@m_fast`; audits: reviewer/sentinel `@m_mid`,
   critic `@m_strong`; connector `@m_mid`. Required existing-authority bindings:
   content `@m_composer`, audit `@m_grok`, connector `@m_antigravity` with
   `@m_zfl` fallback. Observed `m_antigravity` fallback is empty. Evidence:
   `.ufo/evidence/fleet-r1-interactive/routing.json`. This lane makes no global
   or session routing changes and does not silently substitute models.
2. **SOURCE-DRIFT / next tsukuroi session.** Revenger's province digest changed
   from the inherited pin; current overlap still requires integrator arbitration.
   Re-read current ranges and record a new source-backed correction rather than
   editing inherited history. Parent review and exact hashes:
   `.ufo/evidence/fleet-r1-interactive/parent-review.md`, `source-pins.json`.
3. **DELIVERY-SCOPE / next tsukuroi session + fleet integrator.** Inherited notes
   expect a fleet-root report write; this dispatch only permits lane-local .ufo
   reports. Append the correction when the full wave can run. The integrator,
   not this lane, copies accepted handoff/ledger information into shared state.
4. **INHERITED-WORK / next tsukuroi session.** Preserve the seven inherited paths
   named in `.ufo/evidence/fleet-r1-interactive/inherited.json`, plus the unchanged
   census script. No inherited content is staged by this attempt. Resume review
   only after routing is authorized; obtain a full wave and fresh gates before
   a candidate content commit or admission.

Newly verified completed rounds in this interactive invocation: **0**. This is
one observed blocked attempt, not evidence of three consecutive blocked rounds
or saturation. The at-least-100 verified-round target remains outstanding; no
historical cumulative total is inferred from launch counters or subjects.
No native judge, sound-round, convergence or Sighting-completion claim is made.

- **planned (current):** continue the pending adjacency move in a fresh
  authorized L1 session after ROUTE-BINDING is cleared; do not loop rounds here.
- **retired (current):** none.

Receipt gate remains **blocked / inapplicable to completion of this unrun round**:
the direct Sighting launch metadata has run/session/mission/pane identifiers but
no real queue `taskKey` or producer expected bag. No applicable receipt is minted,
no synthetic task identity is introduced and Sighting is left uncompleted.
The next authorized dispatch must supply its frozen task/prompt/config/report
binding. Exact requests are persisted locally in `.ufo/l0-questions.md`.

Preservation check after the gates: `sha256sum` over all eight entry-pinned paths
and the global config, exit **0**; changed inherited paths **0**, config checksum
matches the entry snapshot. Full command/output/comparison:
`.ufo/evidence/fleet-r1-interactive/{preservation-check,preservation}.json`.

## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates where the lane learns: `corpus/SOURCES.md` — opened, tier-scoped rows with anchors, rejections with flips, study paths, a search log and unopened leads — and checks itself with the frozen contract's 7 census commands | `corpus/SOURCES.md`; census commands + outputs in `.ufo/evidence/round-1-kaika/after.md` (34 rows, malformed 0, no dup/enum/missing output) | fleet r1 (2026-10-19) |
| host-census-gate | Emits a read-only six-plane host verdict (`TSUKUROI_CENSUS: HEALTHY/DEGRADED/BLOCKED`, exit 0/1/2) with a hermetic 80-case `--selftest` | `bash tools/tsukuroi-census.sh --selftest` → PASS 80/80 rc=0; live run rc=1 six-plane rollup — `.ufo/evidence/round-1-kaika/scout-live.md`, `after.md` | lane r2 (census-v1); demonstrated running fleet r1 |
| root-metadata-observer | Emits root mode/uid/gid and owner-bit observations even on package-probe failure; isolates fixtures and blocks unavailable/non-directory metadata without grading intentional 0555 policy | `.ufo/waves/round-12/resumed/{after,selftest-after,mode-policy-mutant}.json`; measured commit `70fede2a7a890cb50a72db2d4230ee541183bf7b` | round 12 |

Rows enter only through a round that demonstrates the capability running
(`AXES.md` §Capabilities); none enter through this rollout.
Fleet round 1 (2026-10-19): the two rows above entered through this round's demonstrated runs
(`.ufo/evidence/round-1-kaika/after.md`, `scout-live.md`), not through the 2026-10-16 rollout.

## Saturation

The lane's saturation line and stagnation window N are to be declared by the
lane on its next round per `AXES.md` §The stagnation nudge; not asserted by this
conformance change.

**Declared fleet round 1 (2026-10-19):** saturation line **9** (an axis at ≥9 counts as
saturated for the nudge); stagnation window **N = 3** rounds without a new capability row.
State at declaration: not every axis ≥9 (depth 8, adjacency 8 after this round), so the
lowest-axis obligation still binds.

## Fleet round 1 — kaika continuation (2026-10-19): claims, measurements, verdicts

Base `9b70381`; before-values pinned by `git archive 9b70381` (`.ufo/evidence/round-1-kaika/before.md`);
after-values re-run on the round-1 commit (hash in `LOG.md`'s round entry; a commit cannot
name itself) — `.ufo/evidence/round-1-kaika/after.md`. Verdicts are **self-assessed, pending
non-author verification** by the orchestrator.

| Claim | Axis | Score | Counting command (from lane root) | Before → after | Evidence |
|---|---|---|---|---|---|
| A | adjacency | 7 → 8 | `jq '[.routes[]\|select(has("state"))]\|length' corpus/knowledge/adjacency-handoffs-fleet-r1.json`; `jq '.source_pin_recheck.anchors_hold_count'` | states 0 → 7; pins re-read at sibling HEAD 0 → 8 (anchors hold 8/8; original-pin matches 5/8, 3 drifts recorded, not repinned) | `corpus/knowledge/adjacency-recheck-2026-10-19.md`; `PROVINCE.md` re-check block; packet TSUKUROI-F1-MEM-01 cited in the round-1 fleet report (`reported` on integrator commit). **Conditional:** the 7→8 stands only once that report is committed (lesson round-1 condition); until then the verdict is `pending` |
| B | coverage (+ capability `sources-registry`) | 8 → 9 | ``grep -c '^\| `' corpus/README.md``; ART §1.2 sweeps (news, pacnew, recovery, DAC) as in `before.md` | coverage rows 10 → 15; sweeps (files, over `corpus SKILL.md PROVINCE.md`) news 0 → 5, pacnew 0 → 6, recovery 0 → 3, ALA 0 → 1, sandbox 0 → 1, DAC 0 → 2; SOURCES rows 0 → 34 (census clean); SKILL update-gate rows 0 → 4 | 4 new entries + `corpus/SOURCES.md` + `SKILL.md` fleet round-1 append |
| C | freshness | 8 → 9 | `grep -lE '^## Erratum \(2026-10-19, fleet round 1\) — D[1-5]' corpus/knowledge/*.md \| wc -l`; per-note last `^recheck:` date/cadence count over the 25 base notes | doctrine/current-art errata 0 → 7 notes (D1–D5 all present); date-or-cadence rechecks 0/25 → 25/25; notes missing `source:` 6 → 0, `verified-at:`/`recheck:` 11 → 0; README r4-refuted row superseded 0 → 1 | errata blocks in the 7 notes; `corpus/README.md` § Erratum; `SKILL.md` erratum to `:391-393` |

Unchanged axes (no harm measured): depth 8, operability 9 (`--selftest` 80/80 rc=0 after),
calibration 9 — the mistakes ledger (`corpus/lessons/round-1.md` § Mistakes, 19 rows) and
QUALITY criteria 5 → 13 are supporting work, not a claimed calibration move. Ceilings carried:
adjacency — no recipient receipt (0 hits) and ADJ-06 still contested; coverage — K3 upstream
delta (network read) awaits an operator boundary ruling; freshness — legacy notes carry keys as
an appended block, not as opening lines (exception stated in the round lesson's Gate).

- **planned (next round):** open the omarchy issue leads (#8047, #6629) against the snapper and
  initramfs entries; a census arm for root-dir mode (`-Qkk` cannot see `/`) with tameshi method
  advice via ADJ-07; the depth axis (now lowest with adjacency at 8).
- **retired:** none.

Measured commit for the fleet round 1 rows above: `549ec0c1394cfa96702a457a19de672cc1754b2f` (`after.md` captured on a tree byte-identical to it).

## Fleet round 1 — post-review claim corrections (2026-10-19)

The original A–C rows above remain as the `549ec0c` measurement snapshot. These reviewed outcomes supersede their verdict bases, measured on post-review correction commit `459e3ceacea6289d74b6e856c5606b83704f32e5`.

- **A — adjacency 7→8, retained on committed recipient evidence.** Route-state labels are not handoff counts, and the uncommitted fleet report is not the basis. The committed mori response is one unique recipient-side packet answer; its parent has no record and its round-12 HEAD has one:

  ```sh
  M=/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/mori-shokunin
  for ref in 20e2255e7b3ebb05a52272f35a996421cab14848 1f07f1dd1eed59f10c4859726e2f780199190b22; do
    if git -C "$M" grep -q 'TSUKUROI-F1-MEM-01' "$ref" -- PROVINCE.md SCORECARD.md LOG.md; then echo 1; else echo 0; fi
  done
  ```

  Output: `0 1`. A committed kaika `*-shokunin` HEAD sweep finds one recipient repo, mori; the three mori files are duplicate records of one response. Its answer is “no retained kill record overlaps” the capture second. The contemporaneous pin recheck is 1/8 original hashes matching, 7/8 drift, with 8/8 cited anchors still in-range; pin equality is not the adjacency measure. No acceptance or resolution is claimed.

- **B — coverage 8→9, plus capability `sources-registry`.** The corrected coverage measure is four newly declared, read-only `PROVINCE.md` surfaces, each linked to one new knowledge entry; it excludes the adjacency README row and treats keyword sweeps as discovery only.

  ```sh
  W=/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/tsukuroi-shokunin
  for ref in 9b70381 459e3ceacea6289d74b6e856c5606b83704f32e5; do
    content=$(git -C "$W" show "$ref":PROVINCE.md)
    a=$(printf '%s\n' "$content" | grep -Fc 'Arch News` upgrade gate')
    b=$(printf '%s\n' "$content" | grep -Fc '.pacnew` / `.pacsave` drift')
    c=$(printf '%s\n' "$content" | grep -Fc 'Initramfs v42 and boot recovery')
    d=$(printf '%s\n' "$content" | grep -Fc 'Snapper/rollback net')
    printf '%s %s %s %s %s total=%s\n' "$ref" "$a" "$b" "$c" "$d" "$((a+b+c+d))"
  done
  ```

  Output: base `0 0 0 0 total=0`; post-review `1 1 1 1 total=4`. The four linked entries exist at the post-review commit and none at base. `sources-registry` remains separately demonstrated by `corpus/SOURCES.md` and the frozen contract census.

- **C — freshness 8→9, retained only for dated D1–D5 errata rechecks.** The matching erratum-note command is `git -C "$W" grep -lE '^## Erratum \(2026-10-19, fleet round 1\) — D[1-5]' <revision> -- 'corpus/knowledge/*.md' | wc -l`; `9b70381` → `459e3ceacea6289d74b6e856c5606b83704f32e5` yields 0→7. The 25 appended legacy contract-key blocks are repair, not 25 fresh verifications.

At the new snapshot, the unchanged D1 literal-text command counts 9→14. The five added matching lines are append-only “Superseded” errata quoting the old advice (`closeout-r11.md`, `degraded-triage-r4.md`, `host-health-report-r3.md`, `update-safety-note.md`, `update-safety-v2.md`), not five new recommendations. `SKILL.md` now records the separate transaction-log commands and unavailable-`checkupdates` branch.

## Round 12 — resumed measured claims (2026-10-20)

Baseline `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`; measured implementation
commit `70fede2a7a890cb50a72db2d4230ee541183bf7b`.
All verdicts below are **author-verified, pending independent hyaku closure**.
No count-to-ordinal-score scale exists; capability/diagnostic gains are
measured without inventing score points. Depth and adjacency were tied
lowest at 8; C2 works depth. Saturation 9/window 3 and retired none remain.

| Claim | Axis/type | Score delta | Falsifiable before → after | Counting command and evidence | Verdict |
|---|---|---|---|---|---|
| C1 | operability / capability root-metadata-observer | 9 → 9 (0; new demonstrated repertoire row) | packages root metadata records 0 → 1; root-presence predicate exit 1 → 0; six plane names/order unchanged | `bash tools/tsukuroi-census.sh`, then anchored field-sequence counter in `.ufo/waves/round-12/resumed/count-commands.json`; captures `before.json`, `live-after.json`, `after.json` | improved, author-verified |
| C2 | depth / sourced diagnostic refinement | 8 → 8 (0; no arbitrary ordinal uplift) | grounded branch records 0 → 4, every cited row mined and linked to the matrix; 10 documented scenarios, not 10 executed host causes | `python -c "$(jq -r .C2_script .ufo/waves/round-12/resumed/count-commands.json)" <revision>`; exact before/after outputs 0/4, both exit 0 in that JSON | improved, author-verified |

C1 is not proved by a token alone: `bash tools/tsukuroi-census.sh --selftest`
ran **97/97**, exit 0, with two explicit skips (non-root-owned fixture and
EACCES/000-parent case). All 80 legacy case labels remain; 17 focused cases
exercise metadata distinctions, unavailable/non-directory/override failures
and package early returns. A single-defect automatic-DEGRADED policy mutant
failed **4** assertions, exit 1, including the stable
`0555 owner-write absent is report-only (R12-C1)` finding. Output:
`selftest-after.json`, `mode-policy-mutant.json`.

C2 needs no census result. Fresh isolated caller-owned ordinary-mkdir
controls returned new-name 0555 → errno 13, existing-name 0555 → errno 17,
0755 → success (`mkdir-controls.json`). Read-only-mount and effective-root
capability scenarios remain source-grounded, not experimentally run.
The inode mode is configured by systemd's tmpfiles policy S039/S040; neither
that fact nor these controls prove the historical Btrfs failure's cause.

Unworked ordinal axes stay depth 8 (worked but not rescored), coverage 9,
freshness 9, calibration 9, adjacency 8; operability stays 9.
No scope transfer or repair is claimed. Gate live exit remains 1/DEGRADED;
the root bits are report-only, while existing package/driver/journal/
update-safety/OOM findings remain visible.

- **planned (current, supersedes historical ladder-end and pending fleet-r1 plans):**
  in the next externally steered round, open operation-specific Btrfs sources
  and the pending boot-hook package evidence; seek failure-time credentials
  only within the operator/read-only boundary. This round does not start it.
- **retired:** none. No saturation waiver or promotion is claimed.

## Round 13 — C1 correction R13-DAC-EXCLUSIVITY (2026-10-20)

**Supersedes the round-12 author-side admission assessment, not its measured
counts.** The independent `corpus/lessons/round-12-verifier-spotcheck.md`
rejected round 12: operability improved, depth harmed, expansion/quality/
discernment harmed. Round-12 C2's 0→4 structural branch counter did not
validate the false exclusive sentence. This correction is a new round and
does not retroactively admit round 12.

Current ordinal scores remain depth8, coverage9, operability9, freshness9,
calibration9, adjacency8 (the later fleet-r1 corrections supersede the
historical terminal table). Depth and adjacency are tied lowest, neither is
retired; the saturation9/window3 nudge does not waive the lowest-axis duty.

One declared claim, **C1/depth**, source-grounded correction on the existing
rollback-net surface: replace active unsupported unit-read-only universality
with a properly scoped ProtectSystem comparison and alternative bind/tmpfs/
path-view mechanisms. Supporting source-attribution and fixture-identity
repairs do not become separate claims. Ordinal delta **8→8 (0)**: no
arbitrary score gain is inferred from correcting a rejected claim.

Counting command: `python tools/check-root-dac-correction.py --revision
<commit>`; before revision `9574a189a758251da5957eee8ff0f38ba2d03c7f`.
The checker is a bounded correction-conformance measure, not proof of all
source semantics. New correction: `corpus/knowledge/root-dac-correction-r13.md`
and `.json`, citing opened S041. Exact before/after output, measured commit
and author-side verdict follow in the measurement appendix. No new
capability table row is claimed merely for writing a checker.

- **planned (current):** seek fresh independent verification of this
  correction, retain failure-time operation/credential/private-namespace
  unknowns and the boot-hook upgrade gate; next work requires a new steer.
- **retired:** none. No promotion or SHONEN `[x]`.
