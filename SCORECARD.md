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
| boot-chain-audit | Audits every limine entry live and read-only: copies each UKI via `sudo -n cat`, extracts its initramfs in a private mktemp dir, types `/new_root`, binds the firmware-selected entry, and emits a per-entry next-boot verdict plus `TSUKUROI_BOOTCHAIN` | `bash tools/boot-chain-audit.sh --live` → `.ufo/waves/round-17/l1-capture/audit-live.txt` (6 entries, CONSISTENT, rc 0); `--selftest` 44/44 | round 17 |

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

### Round-13 measured outcome

| Claim | Axis | Ordinal delta | Measured before → after | Verdict |
|---|---|---|---|---|
| C1 R13-DAC-EXCLUSIVITY | depth | 8→8 (0) | correction_count0→1; gate exit1→0; baseline `9574a189a758251da5957eee8ff0f38ba2d03c7f` → implementation `c35d3567d1c8b5d4b45c0ff82201966b76cbd786` | improved, author-verified; fresh independent closure pending |

Counting command: `python tools/check-root-dac-correction.py --revision
<revision>`. Baseline output is retained in
`.ufo/waves/round-13/correction/verification.json`, measured with evaluator
at `44677cce26b3bedf93a6609374ffa54dde59552f`; final output and the corrected
13/13 selftest are in `verification-fixed.json`, measured at `c35d356`.
The only intervening code delta corrected a selftest's expected finding,
not production evaluation. Red baseline explicitly names the old false
universal, not just a missing successor. A red baseline versus a clean
correction demonstrates narrow conformance; separately reopened S041 and
L1 source comparison support the substantive source claim.

Per-axis author verdicts: depth improved; coverage, operability, freshness,
calibration and adjacency unchanged. The census executable SHA256 remains
`d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e`
at baseline and implementation. No live census rerun or host health
improvement is claimed. Trends: expansion unchanged, quality improved,
discernment improved through outside-disagreement learning (#17/#18).
Outside gate-decision sampling remains a fresh verifier's duty.

## Round 14 — repair-first C1/depth (2026-10-20)

**Supersedes the round13 author-side admission assessment, not its
structural measurements.** Independent
`corpus/lessons/round-13-verifier-spotcheck.md` rejected round13 as harmed:
the replacement MD original line97 misstates ProtectSystem's value domain
and S042 asserts a self-description absent from #8047/comment6071740243.
Round12 and round13 remain rejected; no retrospective admission.

One claim **C1/depth**: named source-grounded corrections
R14-VALUE-DOMAIN and R14-COMMENT-ATTRIBUTION on existing rollback-net
ground. Baseline `8606bad4cbc6451ac2890c9f8e2548a36c386db6`; candidate
`corpus/knowledge/source-scope-correction-r14.md` and `.json`, citing
opened S044 and S045. Falsifiable target: corrected proposition records
0→2 with specific old-defect findings on the red baseline, not merely
missing-successor files. Source agreement is checked separately against
exact located quotes; the bounded executable cannot prove semantic truth.

Depth and adjacency remain tied lowest8; C1 works depth. Mission's
operability/freshness assignment is initial, not an exclusive axis fence
(`MISSION.md` §The axes framework; current SCORECARD owns all six).
Ordinal delta8→8 (0); no new count-to-score mapping. Other axes retain
coverage9/operability9/freshness9/calibration9/adjacency8. Saturation9,
window3, retired none; no waiver or new capability row.

Counting command: `python tools/check-source-scope-correction.py
--revision <commit>`. Same executable is used for both immutable inputs;
its `--selftest` provides isolated exit/finding assertions, not source
approval. New QUALITY19 mines the recurrent claim-exceeds-source class;
QUALITY20 supersedes only criterion18's blanket bot attribution.
R14-S041-METADATA and R14-GATE-CONTRACT are supporting errata, not extra
claim records. Exact measured revision/output follow after execution.

- **planned (current):** seek fresh independent admit/reject source
  sampling of these repairs; retain failure-time operation/credentials/
  private-namespace unknowns and the mkinitcpio42 boot-hook blocker.
  Further domain work requires another external steer.
- **retired:** none. SHONEN remains author-side `[~]`; no promotion.

### Round14 measured outcome

| Claim | Axis | Ordinal delta | Measured before → after | Author-side verdict |
|---|---|---|---|---|
| C1 R14-VALUE-DOMAIN / R14-COMMENT-ATTRIBUTION | depth | 8→8 (0) | resolved correction_count0→2; exit1→0; findings7→0; baseline8606bad4cbc6451ac2890c9f8e2548a36c386db6 → implementation9dd82bceda4cf45c1e1e59e17c996ac898a5ecb7 | improved; independent closure pending |

Counting command: `python tools/check-source-scope-correction.py --revision
<revision>`. Both runs use evaluator SHA256
`0771619dde7cc69fdb37538ad786f293b629f4062167a44a2d9cf4702ec6d428`.
Red includes VALUE_DOMAIN_OVERCLAIM and COMMENT_ATTRIBUTION_OVERCLAIM,
not only missing successor files. `--selftest` exit0/15cases/15passed/
0failed includes restored-defect and notice/history counterexamples.
Exact outputs: `.ufo/waves/round-14/repair/verification.json`.

Source agreement is separate from the lexical checker: correction quotes
of11 and16 words match the reopened sources; comment fields, unverified
VM assertion, second opinion and #6634/#8047 referents are distinct.
History/source/census/safety evidence:
`.ufo/waves/round-14/repair/integration-verification.json`.
Source rows43→45 (A36/B1/C6→A37/B1/C7;
mined31/queued5/rejected7→32/5/8); census exit0 with five disclosed W04s.
No prior source-row mutation, historical text removal or changed census/
old-checker/verifier/SHONEN bytes. All32 seat reports are present.

Per-axis verdicts: depth improved; coverage, operability, freshness,
calibration and adjacency unchanged. Retained scores remain8/9/9/9/9/8
in that axis order; they are not re-certified ordinal measurements.
Trends: expansion unchanged, quality improved, discernment improved by
grounded disagreement-learning. No new repertoire row or uncovered ground.
Fresh independent admit/reject sampling is still required.

## Round 15 — portable locators and update-safety freshness (2026-10-20)

Baseline `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`.
Depth and adjacency remain tied lowest8; C1 works depth. Saturation9,
window3, retired none remain. No arbitrary ordinal uplift or new
capability is claimed.

| Claim | Axis | Score delta | Before → intended after | Counting command |
|---|---|---|---|---|
| C1 R15-LOCATOR / R15-POSITIVE-DOMAIN | depth | 8→8 (0) | resolved routed documentation records0→2, actual original defects and restored-defect fixtures must fail | `python tools/check-locator-clarification.py --revision <commit>` |
| C2 partial-upgrade recheck | freshness | 9→9 (0) | dated round15 evidence-linked incident record0→1, pending/version state tied to capture rather than historical413 context | `python tools/measure-update-recheck.py --revision <commit>` |

Exact measurements and measured implementation revision follow in a new
appendix after execution. C1's checker is bounded documentation conformance,
not a source-semantics theorem; C2's measure is a counting probe, not a
health/upgrade gate. Both work existing owned ground. Neither admits host
repair, running-process version, UI success or a safe upgrade.
Unworked scores coverage9/operability9/calibration9/adjacency8 are retained,
not re-certified. The source-located positive definition and independently
captured package state are causally separable.

- **planned (current):** only finish the externally steered round15 claims
  and independent closure handoff. Preserve historical rejected rounds,
  outstanding operation/credentials/namespace unknowns and boot-hook
  safety blocker; any later round needs a new steer.
- **retired:** none. No SHONEN promotion or independent approval asserted.

### Round15 measured outcome

| Claim | Axis | Ordinal delta | Measured before → after | Author-side verdict |
|---|---|---|---|---|
| C1 R15-LOCATOR / R15-POSITIVE-DOMAIN | depth | 8→8 (0) | resolved correction_count0→2; exit1→0; findings7→0; baseline0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2 → measured942fa0a6525cd67a5b7050965b08375676b294cf | improved, independent closure pending |
| C2 incident update-state recheck | freshness | 9→9 (0) | dated record_count0→1; ABSENT→COUNTED, both exit0; measured baseline0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2 → 6de977d327a7ee831524cfd6a174ab39c7a07498; C2 inputs byte-identical at942fa0a | improved, independent closure pending |

Counting commands are unchanged from the declaration. Exact evidence:
`.ufo/waves/round-15/build/verification-fixed.json` (C1 final evaluator
SHA256, red/green, selftest23/23 exit0) and `verification.json` (C2 plus
preserved initial C1 selftest failure21/23, invalid-CLI2, source census0).
The observed C1 failures were repaired in production classification/count
logic without relaxing expected fixtures. No passing syntax check
substitutes for its executed selftest.

`integration-verification.json` pins both revisions' C1 input digests,
proves C2/SOURCES bytes unchanged after their successful runs, and records
source rows45→49, old-row changes0, protected-file equality, prior-line
preservation and report inventory. C2 snapshot captured2026-10-20T07:44:39Z:
installed libinput1.32.0-1, pending413 against October18 sync metadata,
no health/ABI/running-state verdict and no package-action clearance.
Raw snapshot digest b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81.

Unworked axes coverage/operability/calibration/adjacency unchanged;
no capability, scope expansion, ordinal uplift or promotion. Trends:
expansion unchanged; quality improved; discernment improved through
grounded outside-debt learning (QUALITY21/22). The fresh non-author
admit/reject spot-check remains the independent closure's duty.

- **planned (current, supersedes the implementation declaration):** hand
  the landed round to independent closure and operator recovery/tooling
  decision; no new round is started here. Preserve unresolved incident
  operation/credentials/namespace questions and the boot-hook risk.
- **retired:** none.

## Round 16 — two citation-only repairs (2026-10-20)

Baseline `db68e62065885b3f7463eb0a436c41f0dc3bcde5` includes round15 independent closure. Current external steer is round16. One claim **C1/depth**, R16-BOARD-SECTION and R16-RANK-SECTION: resolved records in `corpus/knowledge/section-citation-errata-r16.json` 0→2, not total historical correction records. The counting command is `python tools/check-section-citations.py --revision <commit>`; same final evaluator on immutable baseline and implementation. Actual old §1/§7 defects must fail, not just missing new files; exact section/table-row bindings and additive target notices must resolve after.

Depth8/adjacency8 tied lowest, C1 works depth. Ordinal depth8→8 (0); retained coverage9/operability9/freshness9/calibration9/adjacency8, not newly certified. No count-to-ordinal conversion, capability, exploratory claim, frontier graduation or recovery authority. Saturation9/window3/retired none.

S050 is own-work evidence for historical section locations, not host health. QUALITY23/24 learn from all four routed round15 debts: two wrong citations, required falsify wave, and seat execution scope. Exact measured outcomes follow after authorized L1 verification; a planned output is not a pass.

- **planned (current):** finish externally steered round16; hand off to independent non-author closure and existing operator recovery decision. No subsequent round starts here.
- **retired:** none.

### Round16 measured outcome

| Claim | Axis | Ordinal delta | Measured before → after | Author-side verdict |
|---|---|---|---|---|
| C1 R16-BOARD-SECTION / R16-RANK-SECTION | depth | 8→8 (0) | correction_count0→2, exit1→0, findings5→0; baseline db68e62065885b3f7463eb0a436c41f0dc3bcde5 → measured db19cc98e091210326382c1ec0b93495fef26be0 | improved; independent closure pending |

Command: `python tools/check-section-citations.py --revision <commit>`, same final evaluator for both revisions. `.ufo/waves/round-16/build/verification-fixed.json` retains red/green and `--selftest` PASS43cases/43passed/0failed. Original `verification.json` retains failed41/43 selftest and successful source census0; production duplicate-binding and row-finding isolation were repaired without weakening expected cases. A count alone is not gate acceptance: the gate exit/findings are also required.

`build/integration-verification.json` records exact source headings/unique rows/quotes, both raw baseline-prefix preservations and12 unchanged protected files. Sources49→50, A41→42/mined36→37; old rows unchanged, malformed0. Author-side depth improved; coverage/operability/freshness/calibration/adjacency unchanged; no new capability or ordinal score. Trends: expansion unchanged, quality improved, discernment improved through grounded outside-citation learning, not swarm size or new independent approval.

Build64 finished with64 lane reports and0 misrooted reports. Planned falsify32 was skipped by the operator's immediate no-new-workers wrap-up; actual total64. This is an explicit override, not a claim that campaign wave2 was optional or that round15 process debt was experimentally fixed. Seat/tooling and raw-directive conformance defects are disclosed in `corpus/lessons/round-16.md`; no package/service/host-recovery action.

## Round 17 — boot chain, freshness, landed revisions (2026-10-20)

Baseline `6923fe0bd3add04fc90f3bc3522895b27cf44bbe`. Steered priority: next-boot safety of this host after the 2026-10-20 09:15 `pacman -Syu` (mkinitcpio 42.2). Three claims, distinct axes, causally separable (each counting command reads only its own files):

- **C1 depth** (tied-lowest with adjacency at 8): next-boot verdict per limine kernel entry from extracted images. Count `verdicted_kernel_entries` by `python3 tools/check-boot-chain.py --revision <commit>`; baseline 0 (BOOTCHAIN-MISSING).
- **C2 freshness**: stale current-use host statements carrying a dated R17 notice validated against baseline bytes and capture lines. Count `resolved_records` by `python3 tools/check-freshness-r17.py --revision <commit>`; baseline 0 (R17-FRESH-MISSING).
- **C3 operability**: revision tools bound to landed branch commits (jj-w1 audit R1/R2). Count `bound_tools` by `python3 tools/check-revision-binding.py --tools-revision <commit>`; baseline 0/5.
- **Capability** (inside C1, not a fourth claim): `boot-chain-audit` — a live read-only audit of every limine entry.

Saturation 9 / window 3 unchanged; retired none. Ordinal changes are proposed in the measured outcome below and stay author-side until non-author closure.

### Round17 measured outcome

Measured at landed `90037c2d67bc076db79e4d4396f0140e3505dabd` against baseline `6923fe0bd3add04fc90f3bc3522895b27cf44bbe`, same evaluator for both revisions, from a fresh clone (`.ufo/waves/round-17/measure/final/`).

| Claim | Axis | Ordinal | Before → after (counting command) | Author-side verdict |
|---|---|---|---|---|
| C1 next-boot verdicts | depth | 8→8 (0) | `verdicted_kernel_entries` 0 → 5, exit 1 → 0 (`python3 tools/check-boot-chain.py --revision <commit>`) | improved |
| C2 freshness notices | freshness | 9→9 (0) | `resolved_records` 0 → 48, exit 1 → 0 (`python3 tools/check-freshness-r17.py --revision <commit>`); baseline-stale proof `--revision 6923fe0 --registry-from 90037c2` → 48 STALE-UNFLAGGED | improved (48 noticed statements in six entries, not total coverage: wave-2 FxUnflagged* list un-noticed stale statements in SKILL.md, host-health-report-r3, journal-boot-plane, package/aur/foreign, oom/kill entries) |
| C3 landed revisions | operability | 9→9 (0) | `bound_tools` legacy five 0 → 5; all nine `--revision` tools 0/9 → 9/9, exit 1 → 0 (`python3 tools/check-revision-binding.py --tools-revision <commit>`) | improved |
| Capability `boot-chain-audit` | (C1) | — | live run `.ufo/waves/round-17/l1-capture/audit-live.txt`: 6 entries, `TSUKUROI_BOOTCHAIN: CONSISTENT`, rc 0; selftest 45/45 | demonstrated |

Selftests at 90037c2 (`measure/final/selftests.txt`): boot-chain 61, freshness 53, recheck 40, seat-scope 42, revision-binding 28, locator 28, root-dac 23, section-citations 61, source-scope 25, update-recheck 13, audit 45 — all PASS. Recheck gate 5 flagged → 0 (5 resolved). No count-to-ordinal conversion; no ordinal raised by the author.

Calibration: the round's first two L0 lines (fleet ac792a7) carried a wrong snapshot verdict and three unsupported facts; corrected in-round (6fe9984, f92afc1, 6a5c8bc) and mined as R17-TYPE-BLIND / R17-L0-OVERCLAIM. Wave-2 critic FxNoHarm judged calibration harmed (residual, correctable); the author reports that verdict for the operator/closure to rule rather than claiming no harm.

- **planned (next round):** C2 continuation — R17 notices for the un-noticed stale statements wave 2 listed (SKILL.md current-use guidance, host-health-report-r3 U1/413, journal-boot-plane snapper lines, package/aur/foreign planes, oom/kill earlyoom/zswap); W04 count now 8 (S058 supersedes S054 by contract).
- **retired:** none. Saturation 9 / window 3; capability row added this round resets the stagnation window.
- **planned (next round, added after wave-2 FxSimplifyBind):** C3 follow-up — one L1-owned `tools/_revision.py` binding module for all nine `--revision` tools; FxSimplifyBind found six same-input divergences outside the probed surface (bad-branch ids, check precedence, merge-base rc≥2 handling, double NOT-LANDED/NOT-PUSHED in root-dac, missing-branch id, branch-string acceptance). The measured 9/9 holds on the probed inputs.

## Round 18 — routed statement repairs, one revision binder, freshness continuation (2026-10-20)

Immutable baseline `842a5312b704b5cda10fd80ec1fdee5fb381ba97`; shared-module prerequisite `51dd9eeaa305539fa3cfc6ee275978dc18043b79`.
Three declared, causally separable claims on distinct axes:

| Claim | Axis | Ordinal delta | Falsifiable measurement / command |
|---|---|---|---|
| C1 boot-chain statement corrections | depth (tied-lowest 8) | 8→8 (0) | Resolved named correction records 0→3 or more; `python3 tools/check-appended-notices.py --revision <commit> --registry corpus/knowledge/statement-corrections-r18.json`; existing verdicts and historical bytes preserved |
| C2 shared revision binding | operability | 9→9 (0) | Same independent judge at baseline: bound9/9, consistent1/9, shared0/9, local regex copies9; target consistent9/9/shared9/9/copies0 among original nine, with all additional discovered tools reported separately; `python3 tools/check-revision-binding.py --tools-revision <commit>` |
| C3 routed stale current-use notices | freshness | 9→9 (0) | Resolved records0→N in eight named files; `python3 tools/check-appended-notices.py --revision <commit> --registry corpus/knowledge/freshness-recheck-r18.json`; baseline comparison with `--registry-from <landing>` must show actual STALE-UNFLAGGED defects, not merely absence of a registry |

C1 and C3 have disjoint registries and target files; the generic notice evaluator is shared verification infrastructure, not either claim's content. C2's continuity denominator is the original nine tools; discovery includes new tools without crediting their existence as consolidation. No capability, coverage growth, exploratory claim, ordinal uplift or host recovery clearance is preclaimed. Saturation9/window3 unchanged; adjacency8 and depth8 are lowest, C1 works depth; retired none.
Wave1 dispatch:81 seats in one validated call; L1 holds planner, ConnPlanner supplies bounded data-walk. Build evidence `.ufo/waves/round-18/build/`.

- **planned (current):** finish only the externally steered round18 claims and all routed round17 defects; measured verdicts follow after integration, then independent closure. No subsequent round starts here.
- **retired:** none.


### Round18 declaration refinements from first falsifiers

C1's final domain counting command is `python3 tools/check-boot-chain.py --revision <commit> --statement-corrections` (fixed four required correction IDs, package argv arithmetic, each UKI digest and live-image mtime evidence); the generic notice checker remains an additional structural check. This replaces the earlier structural-counter-only C1 command, which CritDepth correctly found insufficient. Expected4/4 corrections, not a self-selected3+ subset. C2's claimed original-nine metrics and grade exclude discovered new tools; all discovered results remain separately reported. Shared import/call census is static, not a universal behavior theorem.

C3 correction sweep now includes49 primary records across the eight routed files plus39 neighboring current-use restatements across17 paths total (implementation registry, not an observed pass). Count actual `resolved_records` and `path_count`, keep primary/supplementary ID cohorts separate, and require all primary paths represented. No total-host-freshness or uncovered coverage claim is introduced.

Capability count clarification (supporting defect4 repair, no claim or new row): the historical boot-chain-audit cell at:164 says44/44. Superseded by the existing landed round17 measurement `90037c2`, `.ufo/waves/round-17/measure/final/selftests.txt` audit45/45 and round17 outcome row:520. No ordinal or repertoire credit is inferred from this correction.


### Final measurement contract after falsification

The initial structural C1 count0→3+ and build88-record C3 figures above are superseded for final admission, not rewritten historical snapshots. Required C1 command is `python3 tools/check-boot-chain.py --revision <baseline-or-target> --statement-corrections --registry-from <landed-target>`: fixed metadata held constant must produce four named unresolved corrections before and4/4 after. Structural notice counter is supporting evidence only.

C2 requires `consolidation_status=PASS` / `consolidated_tools=9`, as well as consistent9/shared9/localcopies0 among the original nine. Discovered tools remain fully observed but informational; their failures cannot alter this claim's grade. Refused revision payloads are diagnostics, never measured commit certificates.

Final candidate C3 has93 records across17paths:49 primary across the eight routed files and44 supplementary neighboring restatements. This includes the sar standing row and remaining AUR classification/age/orphan neighbors. No host-wide/corpus-wide freshness completeness is claimed; resolution means source-bounded stale guidance has a validated notice, not that all host questions are answered. Six new A/mined source rows give59→65; S065 resolves retrospective ALPM events, not current pending/repository/ABI/rollback state. Main immutable evidence and final measured verdicts follow after all falsifiers settle. Ordinals and capability roster remain unchanged.


### Round18 measured outcome — author-side, independent closure pending

Baseline `842a5312b704b5cda10fd80ec1fdee5fb381ba97`. Initial immutable full evaluation at `c0f6303f35e15ce113c03f4b6592014b9d8c2472`; only failed/affected checks repaired and measured at `07cc6ea156a633451d7132f4b22b0598fd07e4b8`. Exact initial/final C1 inputs and evaluator hashes match (`.ufo/waves/round-18/measure/repair/input-equality-and-history.json`); C1 is carried, not falsely labelled re-executed at the later hash. Full retained red/green ledger: `.ufo/waves/round-18/measure/final/results.json`.

| Claim | Axis | Ordinal delta | Observed before → after | Command / measured revision | Verdict |
|---|---|---|---|---|---|
| C1 fixed boot statement corrections | depth | 8→8 (0) | correction_count0→4, exit1→0; all4 named baseline defects unresolved with fixed metadata; wrong-count/LTS/source-context/copy-digest controls fail | `python3 tools/check-boot-chain.py --revision <REV> --statement-corrections --registry-from c0f6303f35e15ce113c03f4b6592014b9d8c2472`; measured `c0f6303f35e15ce113c03f4b6592014b9d8c2472`, carried byte-exact to `07cc6ea156a633451d7132f4b22b0598fd07e4b8` | improved, verified author-side |
| C2 one shared binder | operability | 9→9 (0) | consolidated0→9; consistent1→9; shared0→9; localcopies9→0; exit1→0. Original9/9 retained; additional checker1/1 separately clean | `python3 tools/check-revision-binding.py --tools-revision <REV>`; before evaluated by unchanged final judge, after `07cc6ea156a633451d7132f4b22b0598fd07e4b8` | improved, verified author-side |
| C3 bounded current-use notices | freshness | 9→9 (0) | resolved0→97, exit1→0;97 actual stale baseline records,17paths;49primary/eightpaths plus48supplementary. Initial92/97 red retained before five literal-anchor fixes | `python3 tools/check-appended-notices.py --revision <REV> --registry corpus/knowledge/freshness-recheck-r18.json`; baseline comparison adds `--registry-from c0f6303f35e15ce113c03f4b6592014b9d8c2472`; final `07cc6ea156a633451d7132f4b22b0598fd07e4b8` | improved, verified author-side |

All14 isolated selftests reportPASS at their explicitly recorded evaluator revisions. Census reports97 with two explicit fixture skips; no skipped control is presented as exercised. Whole-corpus recheck37files:21clean+16resolved,0findings, exit0. Harness-bound wrapper exec violations0, exit0. Source-predicate-always-true mutant exits1 and bytes restore exactly; source/event count13, R5 literal arithmetic15, protected history/prefix and operative registry checks alltrue. Ten actual bytecode guards refuseHEAD with exit2 and no local pycache; positive control first creates a cache in the isolated clone.

Declaration conformance remains RED, not a domain/host-safety pass: build81 has37 unauthorized command-list declarations,1missing report,4ambiguous trailers,2undeclared; falsify76 has9 unauthorized declarations,2undeclared. These count reported declarations, never verified executions. RerunExecLog is the one unreplaced dead build seat (provider invalid_prompt); falsify has0dead. L1's load-order/tool-use deviations are retained. Independent closure adjudicates no-harm/admission and CritNoHarm's explicit-registry-selector disposition; no outside SHONEN tick, promotion or native-judge result is claimed.

Unworked ordinal axes coverage9/calibration9/adjacency8 remain unchanged, not newly certified. Saturation9/window3, retirednone, no new capability row. Trends author-side: expansionunchanged (held ground), qualityimproved (source-grounded repairs/current-use notices and runnable gates), discernmentimproved (routed outside mistakes become tested criteria). All remain subject to independent closure.

- **planned (current):** hand off this complete externally steered round18 to non-author closure; prior operator recovery/preservation decisions stay operator-owned. No round19 is started.
- **retired:** none.

## Round 19 — adjacency anchors, /boot writer attribution, registry coverage (2026-10-20)

Immutable baseline `452a054677f6b18284917d7c08c45361f91c25ac`. Ordinals at baseline: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; lowest non-retired are depth and adjacency (tied 8). Stagnation nudge does not apply (not every axis ≥ 9; last capability row round 17, window 3). Three declared, causally separable claims on distinct axes, each with its own registry/knowledge/tool:

| Claim | Axis | Falsifiable before → after (counting command) |
|---|---|---|
| C1 bidirectional adjacency anchors | adjacency (tied-lowest 8) | `outbound_portable` 0 → 10 (each PROVINCE.md sibling ownership pointer anchored by exact heading + ≤25-word quote + pinned sibling commit/blob digest, published in an appended PROVINCE section) and `inbound_classified` 0 → 114 (every line-numbered sibling pointer into tsukuroi files classified RESOLVES/DRIFTED/UNRESOLVABLE against the lane tip, operative drifts packaged as owner handoffs); `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <TARGET>]` |
| C2 /boot writer attribution (sourced) | depth (tied-lowest 8) | `attributed_events` 0 → 12 (every `Updated: /boot/limine.conf` line the gate itself enumerates in the round-19 read-only captures bound to one writer class with mechanism line, signature, SOURCES rows and published knowledge); `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <TARGET>]` |
| C3 registry ↔ tools agreement | calibration | baseline-tool registry `missing` 1 → 0 (tools/_revision.py unregistered, round-18 closure defect 2) with kind/self-test/verdict-map consistency findings 0; discovered tools reported separately; `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <BASE>]` |

Sourced claim: C2 rests on rows opened this round (own-work captures `.ufo/waves/round-19/l1-capture/host-capture-r19{,b,c}.txt` and upstream docs). No exploratory claim, no capability preclaimed, no ordinal uplift preclaimed. L1 holds the planner seat; the planning data-walk rides connector ConnPlannerWalk. Build wave: 68 seats in one validated call (`.ufo/waves/round-19/build/`).

- **planned (current):** land C1–C3 and the routed round-18 defects (seat-scope declarations green at dispatch, `_revision.py` row, every L1 host read inside the committed captures, canonical load order first, `/boot` automation expected); measured verdicts follow integration; independent closure decides admission. No round 20 is started.
- **retired:** none. Saturation 9 / window 3 unchanged.

### Round19 declaration refinements from the build wave (appended; the declaration above stands as written)

- C2 count: the declared 0 → 12 omitted the 2026-10-11 ALPM-SCRIPTLET update (pacman.log 2021, in the declared whole-log grep `host-capture-r19b.txt:1688-1704`); the gate enumerates its denominator itself and the measured target is `attributed_events` 13 of `events_total` 13 (ScribeWritersEntry, CritWritersCircular; lesson R19-DECLARED-COUNT). Event sources: the journal json probe (`host-capture-r19c.txt:5`, since 2026-10-19 00:00) and the whole-log pacman.log grep; their windows differ and are stated.
- C1 wording: `inbound_classified` counts line-numbered, repo-prefixed sibling pointers in committed sibling tips (ReviewCensusExtract); 25 operative and 89 historical are reported separately (CritAdjVacuity), and only operative drifts become handoffs. Census v2 corrects four en-dash ranges at the v1-pinned tips.
- C3 separability: the counting command is `--baseline-tools 452a054…`, so `baseline_tools_missing` grades only the 14 baseline tools; the three new gates are reported as `discovered_tools` (CritCalibrationAxis). Kind/verdict-map semantics are not gated; the four corrected cells are source-reviewed only.

### Round19 recovery (attempt 2, operator-authorized)

Attempt 1 was interrupted after landing the production content and the measurement checkpoint; it left the falsify directory empty and wrote no report. Attempt 2 re-verified the checkpoint (extended 32-run ledger, evaluator digests, L1 re-audit of the 10 anchor sha256s and the 10 sibling pins, an inbound-record audit), and prepared and validated a 100-seat falsify wave (`044ab28e218c1e58dd04f37978b1645762a6a403`) but did not dispatch it: the campaign GRANT never arrived (parent eval kernel timeout; its last action a pending config write) and no seat was spawned. The final ledger is measured at `208e256d8c73bc9593f7299b36264f31dc5076a9`. No ordinal, axis assignment or claim text changes from the Round 19 declaration above; the refinement appendix stands as written.

### Round19 falsify wave (appended 2026-10-21; supersedes the "did not dispatch" sentence above)

Main re-issued the GRANT; the wave ran at 72 seats (process job cap; 28 prepared attacks unexecuted). Verified findings forced gate hardening and record corrections at `5a133bc`, and C1/C2/C3 re-measure PASS under the hardened gates with unchanged counts (10/114, 13/13, 0 missing of 14). No ordinal, declaration or refinement changes; the harness now checks more of what the claims assert.

## Round 20 — declaration, attempt 1 (2026-10-21)

Author: TsukuroiR20; immutable baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472` (round19 non-author closure). Work round20 only. Baseline ordinals: depth8, adjacency8, coverage9, operability9, freshness9, calibration9; none retired. C1 works tied-lowest adjacency. Saturation9/window3; no stagnation waiver, new capability, exploratory claim, or ordinal uplift.

| Claim | Axis / ordinal delta | Falsifiable before → after | Counting command |
|---|---|---|---|
| C1 attributed ownership clarification | adjacency 8→8 (0) | `ownership_corrections` 0→1: OUT-009 explicitly reports Revenger's precise sibling declaration, never an ownership award; Kaidoku/Revenger arbitration and the no-write boundary remain | `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections` |
| C2 object-only landed selectors | operability 9→9 (0) | `object_selector_tools` 0→9 for the frozen original-nine matrix (ghost refs, prefix shadows, uppercase, annotated commit tags, blob, unlanded/unpushed); discovered tools separate. Supplementary binder selftests cover non-empty trees, tags to blob/tree and nested tags without changing the preregistered per-consumer cases | `python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors` |
| C3 actual operative live map | calibration 9→9 (0) | `audit_live_map_errors` 1→0: selected highest registry row distinguishes live0/2 from selftest1; named corrections disclose the false round19 repair assertion and the historical SKILL prefix exception | `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map` |

Preregistration: `.ufo/waves/round-20/preregister.json`, written before candidate implementation/output; source-only oracle seats must independently evaluate the expected controls before measurements. Each claim has a separate content locus and finite evaluator mode; shared revision binding is infrastructure, not C1/C3 claim content. No arbitrary-shell, global registry-semantics, current host freshness or boot-readiness certificate is claimed. Supporting repairs: execution-log systemctl mutation discrimination and a named supersession of boot-writers operator rule4; neither grants a package/service/boot action.

- **Measured (code commit `fc2a0085088cedb3ab59dc3fff16523c0f42a6b4`):** C1 `ownership_corrections` 0→1 (exit1 `OWNERSHIP-CORRECTION-MISSING` → exit0); C2 `object_selector_tools` 0/9→9/9 (exit1→0); C3 `audit_live_map_errors` 1→0 (exit1→0). Full receipts: `.ufo/waves/round-20/measure/final-r20c/results.json`; all ordinal deltas remain0.
- **Smoke and suite:** `.ufo/waves/round-20/measure/smoke-final2/results.json` records expected exits for all five changed CLI paths. The final evaluator ran all17 repository tool selftests with exit0; named counts: `_revision`57, revision-binding62, adjacency25, recheck-commands95, registry-coverage23, each zero failures. `round20-prefixes=True`; adjacency legacy exit0 with no default `ownership_corrections` field; end census exit0 with8 existing W04 warnings.
- **Scope gates:** build `seat-scope` exits1 for13 missing reports, the13 known provider-rate-limit deaths; falsify `seat-scope` exits1 for20 annotated `Scope: executed=none.` trailers. Neither is rewritten; the declarations do not independently prove command absence. There are0 `SCOPE-EXEC-UNAUTHORIZED` and0 `SCOPE-UNDECLARED` findings in both captures.
- **C2 limit:** the preregistered per-consumer matrix stays fixed; supplementary shared-binder selftests now cover non-empty trees, tags to blob/tree and nested tags. The original-nine consumer matrix does not establish universal tag-target coverage. No arbitrary-shell, host/boot-readiness, ownership-award, or filesystem-write claim is made.
- **retired:** none. Independent closure and operator recovery/arbitration remain external.

## Round 21 — preregistered target-type and review evidence closure

Baseline `82e519203e676c532b1dc5ea91a85671f2286e7b`; round20 admitted externally at rounds[404]. Three causally separable claims, frozen before candidate outputs in `.ufo/waves/round-21/preregister.json`:

| Claim | Axis | Before → target | Counting command |
|---|---|---|---|
| C1 source-grounded selector type decision contract | depth (tied-lowest8) | validated decision_rows0→5 for commit/tree/blob/tag-to-commit/tag-to-noncommit | `python3 tools/check-selector-contract.py --revision <REV>` |
| C2 consumer target-type controls | operability9 | target_type_tools0→9, new explicitly selected matrix; preserve round20 object-selectors unchanged | `python3 tools/check-revision-binding.py --tools-revision <REV> --object-target-types` |
| C3 review byte/predicate binding | calibration9 | pinned_reviews0→every delivered round21 review, with preregistered snapshot SHA-256 and exact predicate | `python3 tools/check-review-snapshots.py --revision <REV> --manifest .ufo/waves/round-21/reviews.json` |

All ordinal deltas0; adjacency8/coverage9/freshness9 unchanged, saturation9/window3, retired none. No capability, exploratory claim, host-recovery action or global semantic completeness. Historical round20's13 missing reports and20 malformed trailers remain immutable RED; this round demonstrates future prevention without manufacturing dead-seat reports. Reservations must precede dispatch and review digests must precede reviewed outputs. L1 holds canonical planner; independent outside closure remains required.

- **planned (current):** complete only round21, then hand off; never start round22.

### Round21 source-only metric correction (before execution)

Build `CritBaseline.md` and `ConnPlanner.md` correctly reject reading C2's preregistered0→9 as a behavioral repair: the unchanged baseline binder is expected already to handle these types. The original declaration/preregistration stays historical. Final C2 counts **one opt-in mode absent→present**, reports `target_type_tools` as actual behavioral non-regression (expected9→9, not measured yet), and requires a discriminating witness: the exact same tag-to-tree weakening mutant survives the old frozen matrix but fails the new type matrix. Final command remains `python3 tools/check-revision-binding.py --tools-revision <REV> --object-target-types`; `target_type_mode` is counted once, availability and behavior are separate, executing/measured judge digests are emitted. `--selftest` also emits `TARGET_TYPE_WITNESS` old/new kills. No9-fold credit for one availability fact, no old case mutation, no ordinal uplift.

C1's five rows are five explicit decisions, not five depth units. C3 counts primary snapshot/predicate declarations and reports distinct source files beside review count; secondary build consumer/sibling reads were unpinned and remain a disclosed limitation, not retrospectively pinned. C1's evaluator never reads C2 content and C2 never reads the C1 registry; shared semantic expectations do not create a production dependency. No capability acquisition is asserted.

### Round21 measured outcome — admission not self-granted

Same final evaluators measured baseline `82e519203e676c532b1dc5ea91a85671f2286e7b` and landed code `e99303c7ca75363b99a3d1937e65329b815c50f2` in a fresh clone. Full executed command/exit/stdout ledger: `.ufo/waves/round-21/measure/final-r21/results.json`; executable reproduction: `python3 .ufo/waves/round-21/measure/run.py e99303c7ca75363b99a3d1937e65329b815c50f2 <fresh-output-name>`.

| Claim | Axis / ordinal delta | Observed measurement | Author-side verdict |
|---|---|---|---|
| C1 five source-grounded decisions | depth8→8 (0) | `decision_rows`0→5, exit1 SELECTOR-CONTRACT-MISSING→0; `python3 tools/check-selector-contract.py --revision <REV>` reads active corrected JSON/prose/source-policy cells | improved |
| C2 new explicit target-type matrix | operability9→9 (0) | `target_type_mode`0→1, exit1→0; actual `target_type_tools`9→9, not behavioral uplift. `python3 tools/check-revision-binding.py --tools-revision <REV> --object-target-types`; baseline's own old CLI separately exits2 E-CLI | improved |
| C3 every-review primary receipt target | calibration9 retained (delta0; not newly certified) | original build command `python3 tools/check-review-snapshots.py --revision <REV> --manifest .ufo/waves/round-21/reviews.json`:0→60/64, exit1→1. Additional separately frozen falsify manifest:51/64, exit1. Combined111 conforming receipts/128 declared,117 actual report files | unprovable as an improvement/no-harm claim: the declared every-delivered target is falsified by six strict receipt mismatches; no self-admission |

The new evaluator has28/28 isolated cases; review receipt gate24/24; revision judge78/78. All19 tool selftests exit0. The census selftest retains two explicit skipped root fixtures, never counted as exercised. The final ledger matches39/39 expected exit codes, **not39 clean gates**: C3 has three build scope-line mismatches and two falsify scope-line plus one falsify predicate mismatch, beyond known missing reports. Those original reports and both preregistered manifests remain unchanged.

Generic-tag-peel witness: old matrix kills0, new tag-to-blob and tag-to-tree controls each kill the same mutant, observing E-GIT-FAILED instead of required INVALID. Tree-prefix mutant likewise survives old9/9 and fails the new tree class. Legacy default and object-selector modes each remain9/9/exit0. `legacy-continuity.json` proves byte equality for object_selector_probes/measure/probe_tool/grade and the shared binder. Registry19/19, missing0/findings0; actual live-map errors0. Both manifests equal their predispatch committed bytes, both ancestry checks are true, and every primary snapshot matches its pinned original blob (`preregister-integrity.json`).

Independent metadata census observes13 Bash starts across9 NO-EXEC seats, including failed seats, while the old declaration gate reports unauthorized0/malformed0. Thus declarations are not command-absence evidence. Named corrections and exact metadata are in the round lesson and `measure/seat-tool-audit*.json`/`seat-execution-requests.json`. The new strict receipt count and these execution-scope defects remain separate, neither hidden by exit-code matching.

Sources80→82 (A72→74/B1/C7; mined66→68/queued5/rejected9); start/end validation both exit0, warnings8→9 due disclosed S082 URL overlap. New rowsS081/S082, no old-row status/recheck/used-by change, no frontier graduation or repertoire row. All other ordinal axes remain inherited, not re-certified; saturation9/window3, retired none.

- **planned (current):** hand off only round21 to independent non-author closure and the L0 enforced-NO-EXEC toolset decision; no later round starts. No unqualified no-harm or promotion is asserted.

## Round22 — prompt scope and bounded evidence (2026-10-21)

Baseline `894d1e20fb4939b0cc4fadf722c46d1429f257d2`; externally steered round22 only, attempt1. Three distinct, causally separable claims frozen in `.ufo/waves/round-22/preregister.json` before dispatch:

| Claim | Axis / ordinal delta | Falsifiable before → target | Counting command |
|---|---|---|---|
| C1 six source-grounded seat-boundary decisions | depth8→8 (0; tied-lowest) | validated_boundary_decisions0→6, explicit execution/fetch/local-read/report-write/unknown/dead distinctions | `python3 tools/check-boundary-contract.py --revision <REV>` |
| C2 prompt bindings plus fail-closed recorded-request audit | operability9→9 (0) | request_audit_mode0→1; all current seats have predispatch literal path/command/fetch bindings, every available recorded request checked; unknown/incomplete metadata not clean | `python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-22/build/bindings.json --events .ufo/waves/round-22/build/events.json` |
| C3 bounded strict-receipt cohort accounting | calibration9→9 (0) | cohort_accounting_mode0→1; every declared seat classified without dropping dead/faulty receipts; strict conformance count and accounting verdict separate | `python3 tools/check-review-cohort.py --revision <REV> --manifest .ufo/waves/round-22/build/reviews.json --settlement .ufo/waves/round-22/build/settlement.json` |

Main confirms no host-native per-seat allowlist in task; `tools` is additive, not restrictive. The approved achievable scope is prompt-level binding plus post-hoc detection/evidence, **not preventive runtime enforcement**, proof of reading, or absence of request effects. Round21's111/117 strict receipts, six faults,13Bash starts/nine NO-EXEC seats and six fetch calls/two seats remain historical debt, never rewritten. C3 is deliberately bounded to honest cohort accounting, not every receipt conforming. Source rowsS083/S084 opened this round will ground C1.

L1 holds canonical planner; ConnPlanner supplies bounded planning data-walk. Three code writers have actual separate detached worktrees at the observed baseline; source-only seats write only their report. No capability acquisition or exploratory claim, no ordinal uplift; adjacency8/coverage9/freshness9 inherited, retired none, saturation9/window3 unchanged. No round23 is started.

### Round22 falsifier refinements — target counts unchanged

C2's `request_audit_mode=1` requires an evaluable complete available inventory (exit0 or an explicit evaluated violation exit1); malformed/incomplete evidence cannot satisfy it. C3's `cohort_accounting_mode=1` now requires successful finite accounting, with the fixed denominator, settlement report-byte pins, strict findings and all four bucket counts. A mode flag alone is never an acceptance criterion. C1 global source/host/limit failures earn no validated-decision credit even when all six local tuples happen to match.

The original0→6/0→1/0→1 targets and ordinal deltas0 stand. C2 still detects rather than prevents. C3's delivered-conformant bucket means strict primary-source identity plus receipt declarations only, independent of task completion and request compliance. Failed jobs, malformed reports and newly observed scope violations remain disclosed; no no-harm/admission is preclaimed. Native job delivery projections record128outcomes (121completed/7failed), distinct from available recorded tool/request events and provider transcript EOF conventions. Measured verdicts follow the once-final immutable run.

### Round22 measured outcome — bounded instruments verified, conformance remains red

Baseline `894d1e20fb4939b0cc4fadf722c46d1429f257d2`; complete once-final run at `f39e40a4adad5bf02bd9ddcfb2473b93b139595a`. Registry-only repair measured at `cb3ba8a628c9200c65b3c4c5bf6bb317f9cc3cd8`;174claim inputs/evaluators compare byte-identical, so claim results/selftests are carried, **not** falsely labelled rerun atcb3. Evidence: `.ufo/waves/round-22/measure/finalr22/results.json`, `.ufo/waves/round-22/measure/repairr22/results.json`, `.ufo/waves/round-22/measure/round-summary.json`.

| Claim | Axis / ordinal delta | Observed before → after | Verdict and exact bound |
|---|---|---|---|
| C1 fixed policy/source decisions | depth8→8 (0) | validated_boundary_decisions0→6; `python3 tools/check-boundary-contract.py --revision <REV>`; exit1 BOUNDARY-CONTRACT-MISSING→0 | improved, verified author-side; six fixed policy/source/table decisions, not native capabilities or universal prose truth |
| C2 prompt/request scope evidence | operability9→9 (0) | working request_audit_mode0→1 for both waves; `python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-22/<WAVE>/bindings.json --events .ufo/waves/round-22/<WAVE>/events.json`; fully evaluated red exit1→1,378build/995falsify records, no incomplete seats | improved instrumentation verified, **not conformance**:41build/46falsify findings across20/23seats; two forbidden Bash requests/two build seats. No runtime prevention/no-harm pass |
| C3 fixed-cohort strict evidence accounting | calibration9→9 (0) | successful cohort_accounting_mode0→1; `python3 tools/check-review-cohort.py --revision <REV> --manifest .ufo/waves/round-22/<WAVE>/reviews.json --settlement .ufo/waves/round-22/<WAVE>/settlement.json`; exit1→0;128/128accounted | improved, verified at the preregistered bounded target. Strict receipts remain113conformant/121delivered,8faulty,7absent-dead,0absent-unresolved; both strict exits1 |

Prompt declaration count `python3 .ufo/waves/round-22/measure/prompt-bindings-count.py cb3ba8a628c9200c65b3c4c5bf6bb317f9cc3cd8` exits0: each wave64/64specification, rendered and captured-task bindings,64empty command/fetch scopes. This proves literal declarations, not restrictive capabilities or compliance. Record units are1338primary requests plus35additional recorded adapter starts,1373total; not unique operation effects.

All22 isolated tool selftests exit0 atf39 (new28/73/24 cases); collector21/21, fixed candidate/final witnesses6/6, native prefix/outcome replay2/2. Original registry live-map red1 becomes0 atcb3 without changing its checker; registered22/tools22/missing0/findings0. Both legacy original-nine matrices remain clean; frozen manifests/specs/bindings, primary snapshots, registry/settlement identities and original binder/strict/legacy-scope/PROVINCE bytes match their pins. Census82→84, A74→76/B1/C7, mined68→70/queued5/rejected9; old82rows unchanged, newS083/S084, initial/end validate0, nine existing URL warnings unchanged. Census selftest97exercised passes plus2explicit skipped root fixtures.

All other ordinal axes remain inherited, not newly certified; retirednone, saturation9/window3, no repertoire row or frontier graduation. No source-only seat is an outside verifier. Overall no-harm/admission remains **unprovable author-side** because scope violations recur despite literal prompts; Main's approved detection/evidence scope does not authorize calling this runtime enforcement or erase current/historical reds. Independent non-author closure decides progression. No round23 is started.

## Round23 — typed edit authority and independent path reconciliation

Steered round23 attempt1 only; baseline `ae01e50f582016384e620022be38bf5367000e2e`, clean at start. Outside closure `rounds[422]` (CloseKaidoku22, fleet4482c275f9381f219ee4d092e0324d417c3cb1e7) **admitted round22**, resetting its rejection streak. It confirmed the three bounded instruments, judged the two read-only Bash requests process noncompliance rather than axis harm, and set trends expansionunchanged/qualityunchanged/discernmentimproved. That outside quality verdict supersedes round22's author-side improved trend; it does not erase any process red.

Three causally separable claims, frozen before candidate outputs in `.ufo/waves/round-23/preregister.json`:

| Claim | Axis / ordinal delta | Falsifiable before → target | Counting command |
|---|---|---|---|
| C1 typed structured-edit decision contract | depth8→8 (0, tied-lowest) | validated_edit_decisions0→8, source-grounded metadata versus separately declared lane authority | `python3 tools/check-edit-contract.py --revision <REV>` |
| C2 explicit structured-edit audit authority | operability9→9 (0) | structured_edit_mode0→1 for a new schema-v2 manifest; exact predeclared targets require read+write+edit authority, old schema-v1 results unchanged | `python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json` |
| C3 independent outside path-census reconciliation | calibration9→9 (0) | unexplained_cohorts2→0 for fixed round22 build/falsify, exhaustive event/component provenance and arithmetic | `python3 tools/check-path-reconciliation.py --revision <REV>` |

Outside approximate25/33 versus lane23/29 path counts are accepted observations, not retested merely for confirmation. C3 explains policy/normalization/counting-unit differences against frozen round22 inputs; it does not retrospectively authorize an event or alter the original audit. C1 reads no C2 production content; C2 reads explicit v2 declarations/events, not C1; C3 reads old frozen evidence, not new C1/C2 content. Shared revision binding is infrastructure.

All other ordinal scores inherited, retirednone, saturation9/window3 unchanged. No capability acquisition, exploratory claim, native runtime restriction, host/package/service/boot action, retrospective report/binding repair or next round. L1 retains planner; validated build/falsify waves remain author-side only. Current host role steering supersedes the older role map in the prompt; no model parameters or route edits.

### Round23 measured outcome — finite instruments; all-wave C2 assurance unprovable

Frozen targets remain exactly `.ufo/waves/round-23/preregister.json` at56c8ba3840cc506e55c1211d7eed0676e69e7ac6. Repaired implementation measured at `b30a3a34891d730c504bfdbae5dfb1446c91bbff`; completed-wave evidence measured at `90f62f1c84d72e4fdfcd9bfe4fdae1fd7da578c3`. `measure/final/carried-measurement-inputs.json` shows unchanged C1/C3/build-C2 inputs between those commits, not a falsely claimed rerun.

| Claim | Axis / ordinal delta | Actual before → after | Verdict / counting evidence |
|---|---|---|---|
| C1 finite edit decision document contract | depth8→8 (0, tied-lowest) | validated_edit_decisions0→8; exit1→0 | verified author-side atb30; `python3 tools/check-edit-contract.py --revision <REV>` with before56c8ba3; `measure/final/c1-before.json`, c1-after.json. Eight fixed source-vocabulary/separately-authored-policy tuples, not eight behavioral repairs |
| C2 explicit v2 recorded-target audit mode | operability9→9 (0) | baseline tool has no mode (normalized0); build mode1/exit1; falsify mode0/exit2 | **partial/unprovable over all declared round evidence**, not all-wave success: build64complete/1327requests/91edits/257findings; falsify75of76trace-complete/1647requests/63edits/266path findings plus schema+trace defects. `python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json`; build atb30, falsify at90f; all old v1 findings preserved |
| C3 fixed r22 path-census reconciliation | calibration9→9 (0) | unexplained_cohorts2→0; exit1→0 | verified author-side atb30; `python3 tools/check-path-reconciliation.py --revision <REV>` with before56c8ba3; `measure/final/c3-before.json`, c3-after.json. Rough25/33 versus retained23/29 is exactly2+4raw-first selector events, no unit or lane-only delta; all1373fixed records retained |

Real build edit-target observations exercise the v2 mode, and all91supported edit requests have no edit denial. Its257scope findings remain red (253path+4exec). In falsify, FxC3Build08:17 carried the unlisted `replace_all` key; ConnFxPlanner's trace is incomplete despite its observed native completed outcome. The frozen two-shape authority was NOT expanded to turn that run green. No metric or gate was weakened. C2 is not reported as a clean/all-wave0→1; the failed/unprovable evidence remains part of the round. Independent closure decides the original claim's admission; this report does not self-admit the round.

24of24registered tool selftests exited0 atb30, new gates102/121/40cases; collector21/21, final behavioral mutation controls13/13pristine→mutant→restored killed with named failed cases. Current registry24/tools24/missing0/findings0, audit-live-map0. `measure/final/selftests.json` and per-command stdout are authoritative; they are not live host checks. Scope/strict receipt results are separate: all140native seats completed and reported; receipts127well-formed/13faulty, no dead or absent-unresolved; build56/8 and falsify71/5. Native completed does not imply trace-complete or compliant.

Sources84→86, A76→78/B1/C7, mined70→72/queued5/rejected9. Census start/end exit0; all84oldsource row bytes unchanged. AddedS085/S086 are own-work, held-ground instrument sources; no frontier graduation, repertoire row, ordinal change, retirement or outside SHONEN tick. Expansionunchanged, qualityunchanged; discernmentimproved author-side only through the outside-disagreement lesson and discriminating reconciliation/carrier repairs. No global no-harm claim or native enforcement, installs, host/service/package/boot action, new L0 question or next round. Inherited native-NO-EXEC operator/kumitate request remains open.

## Round 24 — declaration, attempt 2 (2026-10-22)

Attempt 1 (a stale 2026-10-21 author identity) was failed at dispatch time by Main and is not resumed. Its pushed data commit `eef0b8e9` (37 fixture files under `.ufo/waves/round-24/fixtures/` and `fixture-data-D-index.json`) is inherited as committed history and is not used by either claim below. The claim base is `f169b3ba9a59abaf3e324c1b591e1e07a4d6003a`. The previous round was closed as rejected-honest-stop (`corpus/lessons/round-23-verifier-spotcheck.md`), so claim C1 repairs its routed defects first. The three previous rounds all worked the seat-audit surface, so the learning claim C2 moves back to the update-safety core of this lane's PROVINCE.

Two causally separable claims. C1 reads only frozen round-23 evidence; C2 reads only this round's host capture and newly opened sources.

| Claim | Axis (ordinal) | Before at `f169b3ba` | Declared after-value | Counting command (over committed bytes at `<REV>`) |
|---|---|---|---|---|
| C1 per-cause report of the frozen round-23 falsify red cohort (repair of the routed defects at spot-check lines 52 and 64) | calibration 9 → 9 | 0 of 268 red findings attributed to a named cause and a recorded tool operation (no such report exists) | 268 of 268 attributed, with status `CANNOT_EVALUATE`, exit 2, the incomplete seat `ConnFxPlanner` and the unrecoverable extra key kept visible | `python3 tools/report-red-causes.py --revision <REV>` → field `attributed_findings` |
| C2 pause-lift update-safety gate entry (learning claim, PROVINCE core: update-safety and package state) | freshness 8 → 8 (tied lowest) | 0 premises of the host-wide pacman pause carry a dated verdict in the lane corpus (the corpus still records 413 pending upgrades and a pending mkinitcpio 42 upgrade) | 5 premises, each with a verdict, a line in the committed round-24 capture and at least one SOURCES row opened this round | `python3 tools/check-pause-gate.py --revision <REV>` → field `premises_verified` |

C2's five premises are fixed now: P1 pending upgrade count; P2 partial-upgrade residue (installed version newer than the sync database); P3 mkinitcpio 42 hooks that still name `/new_root`; P4 sync database freshness and which mirror sets the upgrade target; P5 rollback by package cache and package transactions during the pause. A premise without a source row opened this round, or without a resolvable capture line, does not count. A miss on either value is an honest stop; the targets will not be narrowed.

No exploratory claim, capability acquisition, ordinal change, retirement, package transaction, sync, service restart, boot action or configuration write. The L1 holds the planner seat.

### Round 24 declaration refinements after wave 1 (appended 2026-10-22; targets unchanged)

Wave-1 critics (CritClaimSizing, CritLearningFit, CritC1Construction, RevGateSchema) found defects in the declaration text above. The declared after-values (C1: 268 of 268 in field `attributed_findings`; C2: 5 in field `premises_verified`) are not changed. Corrections:

- C2 axis. Freshness was 9 at the base, not 8; the tied-lowest axes are depth and adjacency at 8. The C2 entry supersedes weaker update-safety statements, which is depth work, so C2 is recorded against **depth 8 → 8 (tied lowest)**. Lesson R24-STALE-PREMISE.
- C2 before-value. The corpus already carried round-17 dated notices that 413 and the pending mkinitcpio 42 upgrade were historical. The re-derivable before-value is the counting command at `f169b3ba`: the checker and the gate entry are absent there, so 0 premises are verified.
- C2 counting rule, made stricter (never looser): the round date 2026-10-22 is fixed in the tool; the capture is pinned to `.ufo/waves/round-24/capture/l1-4/capture.txt` by sha256; each premise needs one capture pointer whose text is unique in the capture and is not a section header, command echo or exit line; every listed source must be a `mined` row opened 2026-10-22 whose used-by names the gate (the declaration said at least one); an `unverified` verdict does not count.
- C1 before-value. The first tool ran from the working tree, so at `f169b3ba` it already printed 268. The tool now reads itself from the revision; at `f169b3ba` it is absent and the command exits 2. C1 is also hardened: input digests pinned to the `f169b3ba` blobs, the 266/1/1 split and the seat `ConnFxPlanner` required, each event finding re-classified by the frozen checker and given a checker-branch subcause.
- C1 wording. One of the 268 findings (`SCOPE-TRACE-INCOMPLETE` on `ConnFxPlanner`) is a seat-level finding with no recorded tool operation. The tool reports it separately (`attributed_with_recorded_operation` 267, `attributed_seat_level` 1). The phrase "and a recorded tool operation" therefore holds for 267 of the 268; the measured outcome will state that, not round it up. "Repair" here means acting on the spot-check's routing for the next round (line 64) and labelling the line-52 name; no round-23 file is changed.
