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
| calibration | 9 | `calibration-synthesis.md` (463 `wc -l`) — the claim→re-measure→append→supersede→rule loop for rounds 1 to 9; errata kept visible rather than rewritten (r1's four retractions; the "5-plane" numerals; the AUD-X7 credit correction — appended precision in this record's LOG entry); `closeout-r11.md` §3 register. Ceiling: the D13 verification debts still open (`closeout-r11.md` §3.2). | r10 |
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

### Round 24 measured outcome — original C1 target missed

Initial integrated measurement at `22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0`, same two declared after-values:

| Claim | Before | After | Author verdict |
|---|---|---|---|
| C1, calibration 9 → 9 | tool absent at `f169b3ba`, exit 2, no measured value (absence recorded as 0) | `attributed_findings` 268, but only 267 of 268 meet the original conjunction of cause and recorded tool operation; one finding is inherently seat-level | **missed / honest stop**, target unchanged. Not a successful 0→268 under the original wording |
| C2, originally freshness (actual 9 → 9) | new checker reports GATE-MISSING over base bytes; the corpus already gave dated verdicts for P1 and P3, so the declared prose baseline was 2 of 5 rather than 0 | 5 premises with valid evidence links, P1 changed, P2 cleared, P3 changed, P4 changed, P5 changed; verdict truth and source fit require review | bounded sourced improvement, subject to closure; original before-value and lowest-axis declaration were wrong |

The original C2 after-target remains 5. The later depth rebooking is not used to erase the original lowest-axis miss: freshness and calibration were both 9, while depth and adjacency were 8. No ordinal score changed. The source and self-binding hardening after wave 2 is measured again at the final production revision; receipts name that revision.

The observed new knowledge supersedes the stable-mirror lag unknown, the round-18 pending-count UNKNOWN, and current-reading 1password-beta trap statements. Repeating the round-17 supersessions of 413 and pending mkinitcpio is not claimed as a new quality gain. Expansion remains unchanged; quality improves only at those marked loci; discernment is provisional, based on learning from the outside line-52 correction. No capability or outside SHONEN tick is added.

Final wave-2 verdict correction: RevP3Hooks demonstrated that P3 cannot count as changed while its snapshot-boot half is unverified. The JSON now marks P3 unverified; C2 therefore ends **4 of the original target 5, missed / honest stop**. C1 likewise ends 267 of the original 268-with-operation target. Neither target is narrowed. C1 also fails claim-sizing as a calibration claim: its count is finding attribution, not SCORECARD/SHONEN mismatches. The round is handed off as an honest stop, not self-admitted.

Correction to line 734's old round-23 wording: the exact extra key `replace_all` is an author-written summary attribution, not recoverable from the retained event, which stores `__unknown_argument__`. Frozen red inputs and historical results are unchanged.

Final measurements at pushed production revision `44e95428e7081f79cb81b788ca3ece16c1540fb9`: C1 command exits 0, cause attribution 268, recorded operations 267, seat-level 1, frozen checker CANNOT_EVALUATE/exit 2, native completed 76 versus trace complete 75. C2 command exits 1, premises_verified 4, finding P3:verdict-unverified-not-counted; the declared target stays 5. New-tool selftests pass 12 and 24 cases respectively; registry passes 26 of 26 with audit-live-map errors 0. Receipts: `.ufo/waves/round-24/measure/final/receipt.json`. No score or capability addition. Planned: hand this round to a fresh non-author closure; do not start another round.

## Round 25 — declaration, attempt 1 (2026-10-22)

Claim base `b9046016831237cd04d38da11ba76e50d5380c53` (branch tip at dispatch). Round 24 was closed rejected-honest-stop (`corpus/lessons/round-24-verifier-spotcheck.md`); this round repairs its routed defects 1 to 6 first. Routed defect 7 (P3, snapshot boot) needs an operator-authorized boot and is not claimed. Ordinals at the base, read from the latest move records rather than from the stale round-11 axes table: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. The lowest axes are depth and adjacency at 8.

Two causally separable claims. C1 reads only SCORECARD.md, SHONEN.md and repository state at a named revision. C2 reads only this round's host capture, newly opened sources and its own entry.

| Claim | Axis (ordinal) | Before at `b9046016` | Declared after-value | Counting command (tool from the measured commit, data from `<REV>`) |
|---|---|---|---|---|
| C1 self-assessment mismatch count (calibration; repair of routed defect 1) | calibration 9 → 9 | the number the tool reports at `b9046016` (hand count by the L1 predicts 12 of 23) | 0 of the 23 fixed checks K01 to K23 mismatch, exit 0 | `python3 tools/check-self-assessment.py --revision <REV>` → field `mismatches` |
| C2 memory-pressure reading and oomd decision entry (learning claim; sourced; PROVINCE core: OOM and memory plane) | depth 8 → 8 (tied lowest) | 0 verified rows (entry and checker absent) | 6 verified rows, MP1 to MP6, exit 0 | `python3 tools/check-memory-pressure.py --revision <REV>` → field `verified_rows` |

**C1 check set, fixed now.** The current axes table is the last table under the last heading that starts `## Axes — ` in SCORECARD.md at `<REV>`. K01 to K06: the score of each axis (depth, coverage, operability, freshness, calibration, adjacency) equals the after-value of the last ordinal transition `<axis> N → M` recorded for that axis on any SCORECARD line outside that table. K07: the depth row's `N notes` equals the count of `corpus/knowledge/*.md`. K08: its `` `SKILL.md` N `wc -l` `` equals the line count of SKILL.md. K09: its `N table lines` equals the count of SKILL.md lines that start with `|`. K10: its `corpus/lessons/` file count equals the files under `corpus/lessons/`. K11: the coverage row's `` `corpus/README.md` … N `wc -l` `` equals that file's line count. K12: the coverage row's statement about PROVINCE.md Core, Frontier and Adjacent sections matches whether all three headings exist. K13: the operability row's `N cases` equals the case count printed by `bash tools/tsukuroi-census.sh --selftest` run on `git archive <REV>` in a temporary directory. K14: the operability row's statement about a `--identity` mode matches whether `tools/tsukuroi-census.sh` contains `--identity`. K15: the adjacency row's statement about a formal overlap table matches whether PROVINCE.md holds a table with header `| ID | Finding`. K16 to K19: in the last table under the last heading that starts `## Capabilities`, each of the four rows sources-registry, host-census-gate, root-metadata-observer and boot-chain-audit names only repository paths that exist at `<REV>`, and the host-census-gate row's stated case count equals K13's observed count. K20 to K23: each of the four SHONEN.md boxes names only repository paths that exist at `<REV>`, and no box is `[x]` without a named non-author verifier. A fact the row does not state counts as a mismatch. The ordinal checks test agreement with the lane's own later move records, not an outside judgment.

**C2 rows, fixed now.** MP1 the meaning of the `some` and `full` lines of system memory pressure. MP2 the `total` field is cumulative stall time, so a dated incident needs two reads and a difference. MP3 per-cgroup `memory.pressure` files and how they relate to `/proc/pressure/memory`. MP4 what `ManagedOOMMemoryPressure=` and `ManagedOOMSwap=` values `auto` and `kill` mean for systemd-oomd, and what that means on this host, where systemd-oomd is inactive and disabled. MP5 the systemd-oomd default limits for memory pressure, its duration and swap use, for the installed systemd 262. MP6 kernel OOM kill evidence (`oom_kill` counters) is separate from pressure stall evidence. A row counts only if it carries a verdict and action; at least one source that is a `mined` SOURCES row whose used-by names the entry and that was either opened 2026-10-22 or had its `recheck` updated in place this round with the change logged old → new in `corpus/lessons/round-25.md` (this answers routed defect 5); a located quote of at most 25 words recorded in that lesson's Gate; at least one pointer into `.ufo/waves/round-25/capture/capture.txt` (sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`) whose line text is unique in the capture and is not a section header, command echo or exit line; and a SKILL.md decision-table row, appended this round, that names the row id.

A miss on either value is an honest stop; neither target will be narrowed. No exploratory claim, capability acquisition, ordinal change, retirement, package transaction, sync, service start or restart, boot action or configuration write. The L1 holds the planner seat.

Inherited leftovers resolved at round start (not authored by this round): three tracked round-24 files restored from `master` (`.ufo/waves/round-24/w1/ExecPauseGateChecker/check-pause-gate.py`, `.ufo/waves/round-24/w1/RevGateSchema.md`, `.ufo/waves/round-24/w1/ScribeGateEntry/pause-lift-gate-r24.json`; the discarded diff had sha256 `0a215d80…`) and two untracked files deleted (`.ufo/waves/round-24/w1/ScribeGateEntry/p2-measured-probe.txt` sha256 `2eb7ab53…`, `zero-probes-measured.txt` sha256 `5266b654…`).

### Round 25 declaration refinements after the first wave-1 falsifiers (appended 2026-10-22; targets unchanged)

Wave-1 seats CritC1Sizing, CritC2Rows, CritC2Learning and ConnSiblingOverlap found ambiguities that could let either count pass by construction. The declared after-values (C1: 0 of 23 in field `mismatches`; C2: 6 in field `verified_rows`) are not changed. Every refinement below is stricter than the text above and was fixed before either tool was run on a round-25 revision.

- C1 ordinal reference (K01 to K06): the last match, by line order on SCORECARD lines outside the current axes table, of `\b<axis>\b[^0-9|→\n]{0,12}?(\d{1,2})\s*(?:→|->)\s*(\d{1,2})` with both numbers from 0 to 10. So `coverage rows 10 → 15` is not an ordinal, and `freshness (actual 9 → 9` is. The tool prints the line it used. These six checks test agreement with the lane's own records and are labelled so.
- C1 fixed tokens. K12: stated absent when the coverage row contains `Core/Frontier/Adjacent not landed`, stated present when it contains `Core, Frontier and Adjacent sections present`. K14: `` `--identity` not landed `` or `` `--identity` landed ``; observed present only when `tools/tsukuroi-census.sh` has a case arm matching `^\s*--identity\)`. K15: `no formal overlap table` or `formal overlap table present`; observed present when PROVINCE.md has a line starting `| ID | Finding`. Any other wording is unstated, which is a mismatch.
- C1 path grammar (K16 to K23): Capabilities cells are read from backticked spans, SHONEN boxes from bare tokens. A token is a path when it contains `/` or ends in `.md`, `.json`, `.py`, `.sh` or `.txt`, after one brace group is expanded. A row or box that names no path is a mismatch. A box marked `[x]` must contain `non-author verifier:` and a name.
- C1 setup errors: no axes table, a missing axis row, a missing named capability row or fewer than four SHONEN boxes exits 2 (could not evaluate), never a zero-mismatch pass.
- C1 and C2 stay causally separable: C1 checks whatever counts the measured revision holds, so it would verify at a revision without C2 if the table states that revision's counts. Because C2 changes the counts, C1 is measured at the final revision only.
- C2 capture pointers: each pointer names a line and a token of at least 3 characters; it counts only if the line is unique in the capture, is not a header, command echo or exit line, contains a letter or digit, and contains its token.
- C2 scope: the frozen capture never read earlyoom, which is active and enabled (supplementary read-only capture `.ufo/waves/round-25/capture/capture-earlyoom.txt`, sha256 `7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309`, also holding empty `OOMRules=` on the four units). It is context only, not a counting input; no row may conclude that nothing watches memory before the kernel. MP1, MP2, MP3 and MP6 restate ground the sibling lane mori already holds (`mori-shokunin/corpus/knowledge/system-pressure-r24.md` at `4f05dd5a`); the entry cites mori for those general facts and keeps only the OS-triage and systemd-oomd consequence here (PROVINCE row ADJ-04).

## Axes — current self-assessment (round 25)

Appended 2026-10-22 by the round-25 C1 repair (routed defect 1 in
`corpus/lessons/round-24-verifier-spotcheck.md`). This table supersedes the
round-11 table above as the lane's current self-assessment; the round-11 table
stays in the file as the historical record of that round. Each score is the
lane's current ordinal. The counts that checks K07 to K15 read carry their
counting command; the other prose in a cell is descriptive and was reviewed by
wave-2 RevC1TableByHand, not counted. C1 repairs the measurement, it does not move an
ordinal: the six scores below are the same ordinals the lane's later move
records carry. The counts were filled by the L1 at the measured revision with the command named in the same cell.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 47 notes (`ls corpus/knowledge/*.md`, counted with `wc -l`); `SKILL.md` 2355 `wc -l`; 297 table lines (`grep -c '^[|]' SKILL.md`); `corpus/lessons/` (26 files) (counted with `find corpus/lessons -type f` and `wc -l`); rules added since round 12 cite `corpus/knowledge/*.md` notes, while four standing rules near the top of `SKILL.md` cite none. Ceiling: the depth ordinal was last moved at round 4, and no round from 12 to 24 changed it, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` 231 `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); the census has six planes, each with a landed note (the oom plane is a supporting measurement in `PROVINCE.md`, not a declared surface); the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry but have no census plane. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (97 cases, 97 passed, 0 failed) with exit 0; the live run exits 1 with a six-plane rollup; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes) stand; all 47 notes now carry a `recheck:` line, and the round-1 figure of 25 of 25 per-note rechecks is historical; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop for rounds 1 to 9; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; this round's C1 makes the lane's own table measurable against repository state. Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |

Scores are ordinals carried by the lane's own records, not a fresh measurement of
this round. Re-run the counting commands at the revision being claimed before treating any number here as
current.

## Capabilities — current (round 25)

Appended 2026-10-22 with the round-25 C1 repair. This table restates the four
capability rows of the round-11 section at `SCORECARD.md:157` against the
repository state at the final measured revision. No capability row is added or
removed this round and no row claims a new capability: the round-25 tools are
gates, not capabilities. Each path pointer was re-checked against the round-25
claim base with git cat-file, and the host-census-gate case count was re-measured
by running the census selftest against a git archive of the revision.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates where the lane learns: `corpus/SOURCES.md` holds opened, tier-scoped rows with anchors, rejections with flips, study paths, a search log and unopened leads, and the row set is checked by the frozen contract's census commands | `corpus/SOURCES.md`; the census commands and their outputs in `.ufo/evidence/round-1-kaika/after.md` (34 rows in that snapshot, malformed 0, no duplicate, enum or missing output; 125 rows at round 25) | fleet r1 (2026-10-19) |
| host-census-gate | Emits a read-only six-plane host verdict (TSUKUROI_CENSUS: HEALTHY, DEGRADED or BLOCKED; exit 0, 1 or 2) with a hermetic 97-case selftest that touches no live host surface | `tools/tsukuroi-census.sh` selftest prints PASS 97/97 rc=0 (97 cases, 97 passed, 0 failed); the live run exits 1 with a six-plane rollup; receipts `.ufo/evidence/round-1-kaika/scout-live.md` and `.ufo/evidence/round-1-kaika/after.md` | lane r2 (census-v1); demonstrated running fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations even on package-probe failure; isolates fixtures and blocks unavailable or non-directory metadata without grading intentional 0555 policy | `.ufo/waves/round-12/resumed/after.json`, `.ufo/waves/round-12/resumed/selftest-after.json`, `.ufo/waves/round-12/resumed/mode-policy-mutant.json`; measured commit `70fede2a7a890cb50a72db2d4230ee541183bf7b` | round 12 |
| boot-chain-audit | Audits every limine entry live and read-only: copies each UKI with a read-only `sudo -n cat`, extracts its initramfs in a private mktemp directory, types the new_root path, binds the firmware-selected entry, and emits a per-entry next-boot verdict plus TSUKUROI_BOOTCHAIN | `tools/boot-chain-audit.sh` live run wrote `.ufo/waves/round-17/l1-capture/audit-live.txt` (6 entries, CONSISTENT, exit 0); its selftest prints PASS total=45 failed=0 | round 17 |

Rows enter only through a round that demonstrates the capability running; none
enter through this rollout. The boot-chain-audit selftest count in the round-11
table (44 of 44) is superseded here by the landed round-17 measurement of 45
cases with 45 passed and 0 failed, and the host-census-gate count is the current
97 cases, not the 80 of the round-11 table.

### Round 25 measured outcome

Measured at the final production revision, the commit that carries this section (its hash is recorded in `LOG.md` and the fleet report, since a commit cannot name itself). Receipts: `.ufo/waves/round-25/measure/final2/`. Earlier measurements at `5e7c04ecb02735491456de2b8bc44550d0db4609` are in `.ufo/waves/round-25/measure/`.

| Claim | Before at `b9046016` | After | Author verdict |
|---|---|---|---|
| C1 self-assessment mismatches (calibration, ordinal unchanged at 9) | exit 1, 13 of 23 (K02 K04 K06 K07 K08 K09 K10 K11 K12 K13 K15 K17 K21) | exit 0, 0 of 23 | declared target met by the declared command; wave 2 found the zero partly by construction: K01, K04 and K05 resolve to this round's own declaration text, and 2 of the 13 base mismatches were path-grammar artifacts (K21 fixed by a one-phrase SHONEN.md rewording). Eleven stale facts were repaired |
| C2 memory-pressure entry (depth, ordinal unchanged at 8) | exit 2, CAPTURE-MISSING, 0 rows | exit 0, 6 of 6 rows with complete evidence links | declared target met; wave 2 showed the checker counts evidence links, not verdict truth (MutC2Rules 8 of 17 killed); per-row reviewers found MP2 and MP6 hold and MP1, MP3, MP4, MP5 partly hold; corrections are appended to the entry |

The C2 run at `c93bd70f` crashed (traceback in `tools/check-memory-pressure.py` `recheck_log` on a lesson prose line with an S-id and the word recheck but no arrow); the lesson line was reworded and the measurement re-run. The checker is not changed after measurement; its hardening is a round-26 item. No ordinal, capability or retirement changes. Planned: hand this round to a fresh non-author closure.

## Round 26 — declaration, attempt 1 (2026-10-22)

Claim base `e9f5356cd68c9281d07a22e54d1bfd72b12306ac` (branch tip at dispatch, 2026-10-22T13:33:23Z). Round 25 was admitted (`corpus/lessons/round-25-verifier-spotcheck.md`); its eight routed defects are each fixed or explained in this round's lesson. Ordinals at the base, read from the round-25 current axes table and the move records: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. The lowest axes are depth and adjacency at 8.

Canonical protocol files read before any wave of this round (routed defect 6; sha256 of the bytes read, `kimi-shokunin` checkout at `e737d2ea97f6b0198503e077676c3f2ea07974a9`, read 13:34Z to 13:37Z, before this declaration was committed and before any wave was validated):

- `skills/shokunin/SKILL.md` 34be71885eb8bedaf16bd27e5e62741d95500904c696ef436349ea00b7477475
- `skills/shokunin/protocol/PROTOCOL.md` 622b29a043046f0b3b3c7a2240fe62ab516898922885685dd8d89f50b1739fd0
- `skills/shokunin/protocol/PROTOCOL-APPENDIX.md` 90fc91af3c7467a1e131a9164717f81c3ee7ddff3e7bd357cb5e5f9aad322e30
- `skills/shokunin/protocol/MISSION.md` 38a8c15ab1220d4c0fad165729dce681ce2d58a6e54f807e4ceb8364ece94071
- `skills/shokunin/protocol/AXES.md` 04ea5c9e89c91cef645536ab56863ebb014dce617e7083e54968092968a7d993
- `skills/shokunin/protocol/CORPUS.md` b6ed4476b0d1a5a3176ce728e4eb44997bddfa6dfb9fdb2f1a15e81d3f0821bf
- `skills/shokunin/protocol/LEARNING.md` 3ff7ab4da9f3ce448477872af62c8d74ad0671e0d5bfc29a4ca8945bd8865964

Two causally separable claims. C1 reads only this round's storage capture, newly opened sources, their committed snapshots and its own entry. C2 reads only SCORECARD.md, SHONEN.md and repository state at a named revision.

| Claim | Axis (ordinal) | Before at `e9f5356c` | Declared after-value | Counting command (tool from the measured commit, data from `<REV>`) |
|---|---|---|---|---|
| C1 storage-integrity entry: btrfs device errors, scrub, and NVMe health (learning claim; sourced; new PROVINCE frontier area) | depth 8 → 8 (tied lowest) | 0 verified rows (entry and checker absent) | 6 verified rows, SH1 to SH6, exit 0 | `python3 tools/check-storage-health.py --revision <REV>` → field `verified_rows` |
| C2 self-assessment mismatch count, check set v2 (calibration; repairs routed defects 3 and 7) | calibration 9 → 9 | the number the v2 tool reports at `e9f5356c` (hand count by the L1 predicts 3 of 27: K10, K24, K26) | 0 of the 27 fixed checks K01 to K27 mismatch, exit 0 | `python3 tools/check-self-assessment.py --revision <REV>` → field `mismatches` |

**C1 rows, fixed now.** SH1 what the five btrfs per-device error counters (write, read, flush, corruption, generation) count, and that the sysfs `error_stats` file and the `btrfs device stats` query report the same counters. SH2 those counters persist across mounts until an explicit reset, so a non-zero value is not a dated incident; a dated incident comes from the kernel's per-error log line. SH3 what scrub verifies and when it can repair: with the data profile `single` a data checksum error is detected but not repaired, and the `dup` metadata profile keeps a second copy. SH4 the scrub record on this host: no scrub statistics exist and the shipped monthly `btrfs-scrub@.timer` is disabled, so stored data has never been verified end to end. SH5 how `smartctl` derives the NVMe overall-health result and which fields (critical warning, available spare against its threshold, percentage used, media and data integrity errors) decide it. SH6 the NVMe lifetime counters (unsafe shutdowns, power cycles, media errors, error log entries) are cumulative over the device's life, not dated incidents.

A C1 row counts only if all of these hold at `<REV>`: the entry `corpus/knowledge/storage-health-r26.json` holds exactly the ids SH1 to SH6, each once (a duplicate id is an error, never a second count); the row has a non-empty statement, a verdict (`HEALTHY`, `DEGRADED`, `BLOCKED` or `UNVERIFIED`) and an action; every source it cites is a `corpus/SOURCES.md` row with status `mined`, opened `2026-10-22` and `used-by` naming `corpus/knowledge/storage-health-r26.md`, and at least one cited source is tier A; it carries at least one quote of at most 25 words whose whitespace-normalised text is a substring of the committed snapshot `.ufo/waves/round-26/sources/<S###>.*` whose sha256 is written in that source's anchor cell, and the same quote text appears in that source's row of the lesson `## Gate` table (a quote mismatch blocks the row; it is never only a finding); it carries at least one capture pointer (line number and token of at least 3 characters) into `.ufo/waves/round-26/capture/capture.txt`, pinned at sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd`, whose line is unique in the capture, is not a `### ` header, a `$ ` command echo or an `[exit ` line, and contains the token; and `SKILL.md` has a table line whose first cell is exactly the row id inside the section `## Storage integrity — round 26`. A missing capture, a capture with a different digest or a missing entry exits 2 (could not evaluate), never a pass.

The capture script is `.ufo/waves/round-26/capture/capture.sh` (sha256 `81234ae10ddf197aa49cac5ba11220f5f4cca481653155e75ee12439e3675364`), run once by the L1 at 2026-10-22T13:39:52Z. Its only sudo uses are read-only queries (`btrfs device stats` without `-z`, `btrfs scrub status`, `smartctl -H -A` without `-i`, `nvme smart-log`, `ls`, `journalctl`); no scrub was started, no counter was reset and no service, configuration or package changed.

**C2 check set v2, fixed now.** K07 to K23 are unchanged from the round-25 declaration and its refinements. Two changes:

- K01 to K06 (routed defect 3, self-reference). The declaring round N is the number in the heading of the current axes table, which must read `## Axes — current self-assessment (round N)`; a heading without a round number exits 2. The ordinal reference is the last match of the round-25 refinement regex on SCORECARD lines outside that table, excluding every line inside a section whose heading (any level) names round N (`Round N` or `round N` as a whole number), unless that heading also contains `measured outcome`. So a declaring round's own declaration and refinement prose can never satisfy its own ordinal check; only its measured outcome can record a move.
- K24 to K27 (new; routed defect 7). For SHONEN boxes 1 to 4: every `corpus/knowledge/*.md` path the box names exists at `<REV>` and carries no supersession marker, meaning none of its first 20 lines matches the case-insensitive word `superseded`. A box citing a superseded note is a mismatch.

Live-count drift (routed defect 3, second half): the round-26 axes table will state the counts at the revision that adds it and says so; the tool always measures at the revision given, so a later commit cannot change the measured result, and every later round re-measures.

A miss on either value is an honest stop; neither target will be narrowed. No exploratory claim, capability acquisition, ordinal change, retirement, package transaction, sync, scrub, counter reset, service start or restart, boot action or configuration write. The L1 holds the planner seat. P3 (snapshot boot) stays operator-owned and is not claimed.

### Round 26 declaration refinements after the first wave-1 falsifiers (appended 2026-10-22; targets unchanged)

Wave-1 seats CritClaimSizing, CritLearningFrontier, CritC2Construction, SrcSmartNvmeprint, SrcBtrfsScrubUnit, SrcBtrfsScrubDoc, SrcKernelVolumes and SrcNvmeLifetimeFields found wording that their sources contradict, and rule gaps that would let a count pass by construction. The declared after-values are not changed: C1 stays 6 verified rows SH1 to SH6 in field `verified_rows`; C2 stays 0 of 27 in field `mismatches`. Each item below was fixed before either tool was run on a round-26 data revision.

- SH5 wording (SrcSmartNvmeprint, CritLearningFrontier). smartmontools 7.5 `nvmeprint.cpp` prints PASSED exactly when the critical-warning byte is zero (S134 lines 450-451 and 840-842). Available spare against its threshold reaches the result only through critical-warning bit 0x01; percentage used and media and data integrity errors are printed but never decide it. The declaration's parenthetical list of deciding fields was a pre-source assumption and is withdrawn; row SH5 states the source behaviour.
- SH3 wording (CritLearningFrontier, SrcBtrfsScrubDoc). Scrub repairs only from a replicated profile (S139, `Documentation/ch-scrub-intro.rst` lines 13-15, which `btrfs-scrub.rst` includes at line 12); file data with the NOCOW attribute has no checksums and is not verified by scrub (S139 lines 21-24), and systemd sets that attribute on journal files (S139 line 35); the `dup` metadata copies sit on one device and an SSD may store them as one physical copy (S130 lines 639-640). SH3 states these limits instead of an unqualified "detected but not repaired".
- SH4 wording. "Stored data has never been verified end to end" is withdrawn as broader than the evidence. SH4 says no scrub record exists on this host (`no stats available`, `/var/lib/btrfs` absent, where status files live per S139 lines 71-72) and the shipped monthly timer instance for `/` is disabled; ordinary reads also verify checksums (S139 lines 17-18), so the host verdict is `UNVERIFIED`, not `DEGRADED`. The capture line `Error summary: no errors found` is not a health reading and no row cites it as one.
- SH2 wording (SrcKernelVolumes). The kernel prints the same `bdev ... errs:` text at error time (error level, rate limited) and at mount time (info level, only when a counter is non-zero; S132 lines 8422-8456). Only an error-time line dates an incident.
- SH6 wording (SrcNvmeLifetimeFields). The current NVMe Base Specification 2.4 names the field Unexpected Power Losses and notes it was previously named Unsafe Shutdowns; its increment condition is narrow, so 200 is not a count of host-visible crashes.
- Meaning of "verified row". A row is verified when its statement and evidence pass the row rule; its host verdict (`HEALTHY`, `DEGRADED`, `BLOCKED` or `UNVERIFIED`) is the row's reading of the host, not the counting criterion. SH4's `UNVERIFIED` is a verified finding that integrity is unverified.
- Source identities. S131 is the Arch packaging copy of `btrfs-scrub@.timer` at btrfs-progs `7.1-1` (upstream v7.1 ships no unit; the bytes equal the installed unit). S135 is the NVM Express Base Specification 2.4 PDF (sha256 `fe7647532c06859f2952d9db1f90165aa3e9375343d588d5444253f7dbb2c9bd`); a quote cannot be a substring of compressed PDF bytes, so the committed snapshot is lines 21270-21560 of its `pdftotext` (poppler 26.08.0, no flags) rendering, whose full sha256 is `c39f3403106ca496dff79a3b2b4860bf1b422a6695e49e7b5d9fef15787fe20e`; the anchor carries all three digests. S139 (new) is btrfs-progs v7.1 `Documentation/ch-scrub-intro.rst`.
- Lesson path. The Gate table the C1 tool reads is `corpus/lessons/round-26.md`.
- C2, K01 to K06 (CritC2Construction finding 2 and 4; stricter). The exclusion of only round N let earlier rounds' plan prose certify ordinals, and at a final revision the round-25 counterexample lines (792, 793, 807) returned. The ordinal reference is now only SCORECARD lines inside a section whose heading contains `measured outcome`, from any round; all declaration, refinement, correction and move-log prose is excluded. An axis with no transition in any measured-outcome section is a mismatch (`no dated move record`), not exit 2. The heading of the current axes table must still name its round. This binds ordinals to dated move records as routed defect 3 asked. What it proves: the current table agrees with the latest dated measured-outcome record; it does not prove an ordinal is deserved.
- C2 before-value, measured: the v2 tool (sha256 `77c946a91635ab76aa9869a786e4d206d37b3e52c00b80ec1f4c09a17be0c26d`) reports 5 of 27 at `e9f5356c` (K02 and K06 `no dated move record`, K10 lesson files 26 stated against 27, K24 and K26 `corpus/knowledge/root-dac-decision-r12.md` superseded at line 7), exit 1. The hand prediction of 3 is superseded by this measurement.
- C2 limits (CritClaimSizing, CritC2Construction). K24 to K27 detect a supersession notice in a cited note's first 20 lines, which is where this lane puts whole-note notices (`root-dac-decision-r12.md:7`); appended statement-level errata, `.json` companions and box 4's citation of a superseded PROVINCE paragraph are not counted. Box 4's evidence line is still repaired in text, and the lesson says that repair is not counted.
- Tool pinning. Both counting tools are committed in a commit before any round-26 entry, table or SOURCES row: `tools/check-storage-health.py` sha256 `6aadca511ca664b641c2a0b920a51c65057b53520fdf9a09108d6839d7bcf367` (41-case selftest, exit 0) and `tools/check-self-assessment.py` sha256 `77c946a91635ab76aa9869a786e4d206d37b3e52c00b80ec1f4c09a17be0c26d` (13-case selftest, exit 0). The measured revision must carry these bytes; any later change to either tool is disclosed and re-measured.
- Separability, corrected (CritClaimSizing). C1's new files change counts that C2's K07 to K11 read, so C2 is measured at the final revision only; C1 reads nothing C2 changes.

## Round 26 correction to the round-25 record — two in-place edits, not one (appended 2026-10-22)

Routed defect 1 of `corpus/lessons/round-25-verifier-spotcheck.md`. Round 25 made two in-place edits to files this lane keeps append-only or canonical, and its lesson section "Record of the one in-place edit" named only the second, so that record was incomplete.

1. `SCORECARD.md:51`, the calibration row of the round-11 axes table, changed in commit `c93bd70f`. Original wording at `b9046016`: "the claim→re-measure→append→supersede→rule loop with its mismeasure rows". Wording after `c93bd70f`: "the claim→re-measure→append→supersede→rule loop for rounds 1 to 9". The original stands as the round-11 record; the round-25 wording is withdrawn as an undisclosed in-place rewrite. This correction is appended and line 51 is not edited again.
2. `SHONEN.md` box 2 evidence line, `observation/request` changed to `observation and request` (disclosed in the round-25 lesson).

Sweep that finds them: `git diff -U0 b9046016 e9f5356c -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md | grep -E '^-[^-]'` prints exactly these two removed lines. Round 26's own in-place edits are the three SHONEN.md evidence lines of boxes 1, 3 and 4, recorded in `corpus/lessons/round-26.md`.


## Axes — current self-assessment (round 26)

Appended 2026-10-22 by round 26. This table supersedes the round-25 table as the lane's current self-assessment; the earlier tables stay as historical records. The ordinals are unchanged from round 25 (no claim of this round moves an ordinal); the counts that checks K07 to K15 read were filled by the L1 at the revision that adds this table, with the command named in each cell, and hold at that revision. A later commit changes them; re-run `python3 tools/check-self-assessment.py --revision <REV>` before treating any count here as current.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 48 notes (`ls corpus/knowledge/*.md`, counted with `wc -l`); `SKILL.md` 2415 `wc -l`; 336 table lines (`grep -c '^[|]' SKILL.md`); `corpus/lessons/` (28 files) (counted with `find corpus/lessons -type f` and `wc -l`); rules added since round 12 cite `corpus/knowledge/*.md` notes, while four standing rules near the top of `SKILL.md` cite none. Ceiling: the depth ordinal was last moved at round 4, and no round from 12 to 24 changed it, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` 244 `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); the census has six planes, each with a landed note (the oom plane is a supporting measurement in `PROVINCE.md`, not a declared surface); the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry but have no census plane. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (97 cases, 97 passed, 0 failed) with exit 0; the live run exits 1 with a six-plane rollup; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes) stand; all 48 notes now carry a `recheck:` line, and the round-1 figure of 25 of 25 per-note rechecks is historical; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop for rounds 1 to 9; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; this round's C1 makes the lane's own table measurable against repository state. Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |

### Round 26 measured outcome

Measured at the revisions named; receipts in `.ufo/waves/round-26/measure/` (JSON output and an `.exit` file with the command and exit code for each run). The counting tools are the bytes pinned at `4de2b6b1c0cde1f7c7ca9e5727965bcf6aa6ba9e`.

| Claim | Before at `e9f5356c` | After | Author verdict |
|---|---|---|---|
| C1 storage-integrity entry (depth, tied lowest; learning claim; sourced) | exit 2, `SH-CAPTURE-MISSING`, 0 verified rows (`measure/c1-e9f5356c.json`) | exit 0, 6 of 6 rows SH1 to SH6 verified at `ef72f10d79c5b9fee3655e432da52d054b7a018d` (`measure/c1-ef72f10d.json`) | declared target met by the declared command; subject to the falsify wave and the non-author closure |
| C2 self-assessment mismatches, check set v2 (calibration) | exit 1, 5 of 27 (K02, K06, K10, K24, K26; `measure/c2-e9f5356c.json`) | measured at the revision that adds this section; value and hash in `LOG.md` and the round report (a commit cannot name itself) | pending measurement |

Ordinal record, round 26 (dated move record that checks K01 to K06 read; no ordinal moved this round): depth 8 → 8; coverage 9 → 9; operability 9 → 9; freshness 9 → 9; calibration 9 → 9; adjacency 8 → 8. The depth ordinal stays 8: C1 adds one sourced entry with six rows on new ground, which the round-25 depth row's ceiling (ordinal last moved at round 4) does not by itself lift; an uplift would need a separate measured claim. Coverage and adjacency had no earlier ordinal transition inside any measured-outcome section (`measure/c2-e9f5356c.json`, K02 and K06), so this line is their first dated record.

### Round 26 falsify-wave outcome (appended 2026-10-22, before closure)

Wave 2 (35 seats, four dead at start) attacked revision `7dfea9244a84a0e2439f0698e54491e5d7b7c467`. Neither declared after-value changed; neither target is narrowed.

- C1: re-derived 6 of 6 by the pinned tool; L1 mutation run 20 of 20 rule mutants killed (`.ufo/waves/round-26/l1-mutation/`). Row truth, reviewed row by row: every row's evidence links hold, and several statements needed appended corrections (entry section "Wave-2 corrections"): SH6's Unexpected Power Losses trigger omitted a branch and its verdict is split (`UNVERIFIED` for the power-loss count); SH4's "ordinary reads do verify checksums" and SH2's "only on an explicit reset" were withdrawn as universals; SH1, SH3 and SH5 wording narrowed. The declaration refinement's phrase "ordinary reads also verify checksums (S139 lines 17-18)" is withdrawn the same way. The count proves complete evidence links, not true statements; truth rests on the reviewers and the appended corrections.
- C2: 0 of 27 by the declared command. What it proves (wave-2 CritCalibrationClaim): the 21 observed-state checks K07 to K27 moved from 3 mismatches (K10, K24, K26) to 0; K01 to K06 compare the table with an ordinal-record line written by this round in the same commit, so they show self-agreement only, and K02 and K06 were cleared by that line. Under the rule as declared at `b13e991f` (before the refinement) the measured move is also 3 to 0. QUALITY 65 records the fix owed (an ordinal check never reads its own round's record).
- No ordinal moves. No capability enters the table.

## Axes — current self-assessment (round 26)

Re-stated 2026-10-22 after the wave-2 repair commit `75449b13526a57378bfbb6bce929c360ad4c8842`, whose appended notes changed two counts the earlier round-26 table states (`SKILL.md` 2415 to 2418 lines, `corpus/README.md` 244 to 248 lines; `.ufo/waves/round-26/measure/c2-75449b13.json`, K08 and K11). This table supersedes the earlier round-26 table; the ordinals are unchanged, and the counts hold at the revision that adds this table.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 48 notes (`ls corpus/knowledge/*.md`, counted with `wc -l`); `SKILL.md` 2418 `wc -l`; 336 table lines (`grep -c '^[|]' SKILL.md`); `corpus/lessons/` (28 files) (counted with `find corpus/lessons -type f` and `wc -l`); rules added since round 12 cite `corpus/knowledge/*.md` notes, while four standing rules near the top of `SKILL.md` cite none. Ceiling: the depth ordinal was last moved at round 4, and no round from 12 to 24 changed it, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` 248 `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); the census has six planes, each with a landed note (the oom plane is a supporting measurement in `PROVINCE.md`, not a declared surface); the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry but have no census plane. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (97 cases, 97 passed, 0 failed) with exit 0; the live run exits 1 with a six-plane rollup; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes) stand; all 48 notes now carry a `recheck:` line, and the round-1 figure of 25 of 25 per-note rechecks is historical; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop for rounds 1 to 9; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; this round's C1 makes the lane's own table measurable against repository state. Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |

## Round 27 — declaration, attempt 1 (2026-10-22)

Claim base `3beab8ddcf4ed2ae9fdf12eab6ac7f840c74e333` (branch tip at dispatch, 2026-10-22T15:51Z; it carries the round-26 non-author spot-check). Round 26 was admitted (`corpus/lessons/round-26-verifier-spotcheck.md`); its routed defects 1 to 5 are each fixed or explained in `corpus/lessons/round-27.md`. Ordinals at the base, from the round-26 measured-outcome ordinal record (`SCORECARD.md:960`): depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. The lowest axes are depth and adjacency at 8; this round works both. Calibration was claimed in rounds 25 and 26 and is not claimed here.

Canonical protocol files (kimi-shokunin checkout `e737d2ea97f6b0198503e077676c3f2ea07974a9`), sha256 at about 15:54Z, before this declaration and before any wave. All seven are byte-identical to the values recorded in the round-26 declaration (`SCORECARD.md:880-886`): SKILL.md `34be7188…7475`, PROTOCOL.md `622b29a0…9fd0`, PROTOCOL-APPENDIX.md `90fc91af…e30`, MISSION.md `38a8c15a…071`, AXES.md `04ea5c9e…a7d993`, CORPUS.md `b6ed4476…21bf`, LEARNING.md `3ff7ab4d…8964`.

Frozen read-only capture for C1: `.ufo/waves/round-27/capture/capture.sh` (sha256 `ba43d83756b1de7868d8ee75019f4123dcaf8d7d8cb4c0a647d2398d94511369`), output `.ufo/waves/round-27/capture/capture.txt` (sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`), run by the L1 at 2026-10-22T15:55:13Z with no sudo (a run 12 seconds earlier lacked the package line and was overwritten before commit). It records `/proc/sys/kernel/tainted` = 12288, per-module taint `OE` on nvidia, nvidia_drm, nvidia_modeset and nvidia_uvm, `sig_enforce` N, the kernel module-signing configuration, `modinfo` fields (signer "DKMS module signing key"), the owning packages, and two kernel journal lines from boot 0.

Two causally separable claims. C1 reads only its entry, this round's capture, sources, snapshots, Gate and SKILL section. C2 reads only its register, a committed snapshot of one mori blob, the lane files its rows point at, and one PROVINCE section.

| Claim | Axis (ordinal) | Before at `3beab8dd` | Declared after-value | Counting command (tool from the measured commit, data from `<REV>`) |
|---|---|---|---|---|
| C1 kernel-taint entry: what this host's taint value means, which modules set it and why, and what an operator does with it (learning claim; sourced; new PROVINCE frontier area) | depth 8 → 8 (tied lowest) | 0 verified rows (entry and checker absent) | 6 verified rows, KT1 to KT6, exit 0 | `python3 tools/check-kernel-taint.py --revision <REV>` → field `verified_rows` |
| C2 adjacency overlap register with mori's admitted entry `userspace-oom-killers-r26.md` at mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` (inbound pointers into this lane replayed, overlaps classified with an owner, reported not absorbed) | adjacency 8 → 8 (tied lowest) | 0 anchored rows (register and checker absent) | 6 anchored rows, OV1 to OV6, exit 0 | `python3 tools/check-adjacency-overlap.py --revision <REV>` → field `anchored_rows` |

**C1 rows, fixed now (questions only; mechanism wording is pre-source under QUALITY 63).** KT1 how the integer in `/proc/sys/kernel/tainted` encodes taint flags and what this host's 12288 decodes to. KT2 what the out-of-tree flag means and when the kernel sets it. KT3 what the unsigned-module flag means, when the kernel sets it, and why a module whose `modinfo` names a signer can still set it. KT4 what the per-module `/sys/module/<name>/taint` letters mean, and which modules and packages carry them on this host. KT5 whether and how a taint flag is cleared (reboot, module unload, sysctl write). KT6 what a taint flag means for a kernel bug report or oops reading, and the operator's action.

A C1 row counts only if all of these hold at `<REV>`: `corpus/knowledge/kernel-taint-r27.json` holds exactly the ids KT1 to KT6, each once (a duplicate is an error, never a second count); the row has a non-empty statement, a verdict (`HEALTHY`, `DEGRADED`, `BLOCKED` or `UNVERIFIED`) and an action; every source it cites is a `corpus/SOURCES.md` row with status `mined`, opened `2026-10-22` and `used-by` naming `corpus/knowledge/kernel-taint-r27.md`, and at least one cited source is tier A; it carries at least one quote of at most 25 words whose whitespace-normalised text is a substring of the committed snapshot `.ufo/waves/round-27/sources/<S###>.*` whose sha256 is written in that source's anchor cell, and the same text equals the located-quote cell of a row for that source in the `## Gate` table of `corpus/lessons/round-27.md` after one outer pair of straight quotes or backticks is removed (the cell is read by header position, so unquoted, quoted and backticked cells all work; routed defect 3 and QUALITY 64); it carries at least one capture pointer to a line of `capture.txt` (sha256 above) that is not a `### `, `$ ` or `[exit ` line, occurs once in the file, and contains the pointer's token of at least 3 characters; and its id is the first cell of a table row inside the `SKILL.md` section `## Kernel taint — round 27`.

**C2 rows, fixed now.** A C2 row counts only if all of these hold at `<REV>`: `corpus/knowledge/adjacency-mori-oom-r27.json` holds exactly the ids OV1 to OV6, each once; the row names sibling `mori`, the sibling commit above and a sibling path, and a committed snapshot `.ufo/waves/round-27/siblings/mori/<sibling path>` whose sha256 equals the row's `sibling_blob_sha256`; the row's `heading` is a line of that snapshot starting with `#`, and it is the nearest such line at or above `quote_line`; the row's sibling quote has at most 25 words and its whitespace-normalised text is a substring of the normalised snapshot text from `quote_line` through `quote_line + 2`; the row's lane side is either a lane path with a quote of at most 25 words found (normalised) in that file at `<REV>`, or `null` only when the class is `LANE-GAP`; the class is one of `INBOUND-RESOLVES`, `INBOUND-DRIFTED`, `AGREES`, `CONFLICTS`, `LANE-GAP`; the owner is one of `mori`, `tsukuroi`, `contested`; the action is non-empty; and the id is the first cell of a table row inside the `PROVINCE.md` section `## Adjacent — mori userspace OOM killers (round 27)`. When the sibling repository is present at `/home/vgpnk/Projects/shokunin/mori-shokunin`, the checker also requires `git cat-file -p <commit>:<path>` bytes to equal the snapshot (else it reports `sibling-unavailable` and still checks the snapshot).

Separability: C1 changes no file that C2 reads, and C2 changes no file that C1 reads (C2's lane-side quotes point at files outside the C1 set). Both are measured at the final revision as well.

Routed round-26 defects (each fixed or explained in the round-27 lesson, none is a claim): 1 appended correction markers in `corpus/knowledge/storage-health-r26.json`; 2 QUALITY 65 in `tools/check-self-assessment.py` (ordinal checks read only measured-outcome records of rounds earlier than the declaring round, heading match anchored); 3 the Gate-column fix in `tools/check-storage-health.py` with QUALITY 64 selftest cell shapes, disclosed and re-measured; 4 the two 0-byte `.err` files are deleted from the working tree (they were never tracked) and validator stderr goes to `/fast/scratch/hyaku/tsuku27/`; 5 any text added to a seat's task is put into the spec before validation, and the only post-validation addition is the one `solutionSpace` string per task that the host task tool requires, recorded per wave.

Counters are committed before the data they count. A miss on either value is an honest stop; neither target will be narrowed. No exploratory claim, capability acquisition, ordinal change, retirement, package transaction, service action, module load or unload, sysctl write, boot action or configuration write. The L1 holds the planner seat. P3 (snapshot boot) stays operator-owned and is not claimed.

### Round 27 declaration refinements after the first wave-1 falsifiers (appended 2026-10-22; targets unchanged)

Wave-1 CritLearningFrontier, CritClaimSizing, ConnSiblingOverlap, CritAdjacencyMove, RevC1RuleGaps and RevC2RuleGaps read the declaration and the drafts. The declared after-values are not changed: C1 stays 6 verified rows KT1 to KT6 in field `verified_rows`; C2 stays 6 anchored rows OV1 to OV6 in field `anchored_rows`.

- C1 is not a "new PROVINCE frontier area": `corpus/knowledge/driver-firmware-plane.md` lines 101-106 already held both taint lines (2026-10-13), inside the driver and firmware Core area. That phrase is withdrawn. C1 is deeper ground inside an existing Core area: the mechanism, the decoding, the per-module reading, persistence and the operator actions are new. No PROVINCE paragraph was written for C1; its coverage row is in `corpus/README.md`.
- Separability, as landed: the C1 commits `75f410c8` and `b1647ff2` change `tools/check-kernel-taint.py`, `corpus/SOURCES.md`, `corpus/lessons/round-27.md`, the two kernel-taint entry files, `SKILL.md`, `corpus/knowledge/driver-firmware-plane.md`, `corpus/README.md` and `.ufo/` evidence; none of these is read by the C2 counter. The C2 commits `dd94cb1f` and `75784ea4` change `tools/check-adjacency-overlap.py`, the two register files, `PROVINCE.md` and `corpus/knowledge/memory-pressure-r25.md`; none of these is read by the C1 counter.
- What C2 counts (RevC2RuleGaps, CritAdjacencyMove): anchors that resolve against the pinned snapshot and the lane, a fixed vocabulary and a PROVINCE row. It does not check that a class or owner is the right judgement, that the lane side is the exact file mori names, or that the PROVINCE table agrees with the register. The rows are overlap sites, not only mori's explicit pointers: two rows (OV1, OV2) replay pointers, four classify topical overlaps. Class judgements rest on wave-1 ConnMoriInbound's replay and are attacked row by row in wave 2.
- C2 counter tightening, written into the counter before its data: the snapshot of the pinned path must also have the pinned sha256 `a5368ee7…0b29d`, and a `..` path segment is refused. These can only refuse a count.
- C1 counter: the code requires the entry quote to equal the Gate located-quote cell (the declared rule); its module docstring R4 still says "appears in". Disclosed in the lesson (R27-CHECKER-DOC-LAG); the counter bytes are not changed after pinning.
- Learning claim: C1 (deeper Core ground, sourced). C2 is the adjacency move; it is not offered as the learning claim.

## Axes — current self-assessment (round 27)

Appended 2026-10-22 by round 27 (attempt 2). This table supersedes the round-26 tables as the lane's current self-assessment; the earlier tables stay as historical records. The ordinals are unchanged (no claim of this round moves an ordinal; calibration is not claimed). Only counts change: the round-27 commits added two knowledge notes and two lesson files and grew `SKILL.md` and `corpus/README.md`, so the round-26 table read 5 stale counts (K07 to K11) at `099c7b3f` (wave-2 CritAxisHarm; `.ufo/waves/round-27/w2a2/CritAxisHarm.md` finding 6). The counts below were filled by the L1 at the revision that adds this table, with the command named in each cell; re-run `python3 tools/check-self-assessment.py --revision <REV>` before treating any count here as current.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 50 notes (`ls corpus/knowledge/*.md`, counted with `wc -l`); `SKILL.md` 2486 `wc -l`; 381 table lines (`grep -c '^[|]' SKILL.md`); `corpus/lessons/` (30 files) (counted with `find corpus/lessons -type f` and `wc -l`); rules added since round 12 cite `corpus/knowledge/*.md` notes, while four standing rules near the top of `SKILL.md` cite none. Ceiling: the depth ordinal was last moved at round 4, and no round from 12 to 24 changed it, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` 256 `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); the census has six planes, each with a landed note (the oom plane is a supporting measurement in `PROVINCE.md`, not a declared surface); the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry but have no census plane. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (97 cases, 97 passed, 0 failed) with exit 0; the live run exits 1 with a six-plane rollup; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes) stand; all 50 notes now carry a `recheck:` line, and the round-1 figure of 25 of 25 per-note rechecks is historical; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop for rounds 1 to 9; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; this round's C1 makes the lane's own table measurable against repository state. Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |

### Round 27 measured outcome

Counting tools are the bytes committed before their data: `tools/check-kernel-taint.py` at `75f410c825a941f819717e4183bcc82f9c368469`, `tools/check-adjacency-overlap.py` at `dd94cb1f`; neither changed after (wave-2 RerunC1, MutC2Counter). Receipts: `.ufo/waves/round-27/measure/` (attempt 1) and `.ufo/waves/round-27/measure/a2-start/` and `a2-final/` (attempt 2).

| Claim | Before at `3beab8dd` | After | Author verdict |
|---|---|---|---|
| C1 kernel-taint entry (depth, tied lowest; learning claim; sourced S140 to S145) | exit 2, `KT-CAPTURE-MISSING`, 0 verified rows (`measure/c1-3beab8dd.json`) | exit 0, 6 of 6 rows KT1 to KT6 at `b1647ff2` and at `099c7b3f` (`measure/a2-start/check-kernel-taint.py.json`); re-measured after the wave-2 corrections at the revision that adds this section (value and hash in `LOG.md` and the round report) | declared target met by the declared command. The count proves complete evidence links, not true statements: wave-2 row reviewers found narrowed branches and unmarked inferences in KT1 to KT6, each corrected by the appended section "Wave-2 corrections" of the entry and its JSON companion; KT3 stays `UNVERIFIED` |
| C2 mori overlap register (adjacency, tied lowest) | exit 2, 0 anchored rows (`measure/c2-3beab8dd.json`) | exit 0, 6 of 6 rows OV1 to OV6 at `75784ea4` and at `099c7b3f` (`measure/a2-start/check-adjacency-overlap.py.json`); re-measured at the revision that adds this section | declared target met by the declared command, as a count of anchors only: wave-2 CritC2Tool and MutC2Counter show the pinned counter also scores 6 on 19 of 24 should-fail register mutants (extra rows, self-sourced lane quotes, unconstrained `LANE-GAP`), none used by the live rows; class and owner rest on RevRowOV1 to RevRowOV6. The register's "pointers replayed" wording is narrowed to OV1 and OV2 |

Ordinal record, round 27 (dated move record that checks K01 to K06 read from round 28 on; no ordinal moved this round): depth 8 → 8; coverage 9 → 9; operability 9 → 9; freshness 9 → 9; calibration 9 → 9; adjacency 8 → 8. Depth stays 8: C1 is deeper sourced ground inside the existing driver and firmware Core area, not new ground. Adjacency stays 8: C2 records overlap sites and two drifted or resolving inbound pointers, and its outbound items for mori are reported in the round report, not acknowledged.

### Round 27 falsify-wave outcome (appended 2026-10-22, attempt 2, before closure)

Attempt 1's wave 2 (36 seats) produced no reports: the omp process restarted at 17:26Z (`.ufo/waves/round-27/w2/swarm-registry.json`, every agent id null). Attempt 2 dispatched a fresh falsify wave of 44 seats (30 reviewer, 8 critic, 4 mutation-tester, 1 connector, 1 scout) against `099c7b3f` (`.ufo/waves/round-27/w2a2/`). Neither declared after-value changed and neither target is narrowed.

- Harm found and repaired in this round: the registry-coverage gate read FAIL (2 missing rows) at `099c7b3f` because the two new counters had no registry row (`measure/a2-start/registry-099c7b3f.json`); the round-27 registry table in `SKILL.md` restores it. The round-26 axes table read 5 stale counts; the table above restates them. The OV5 correction had reached `memory-pressure-r25.md` but not its JSON companion, and one SH6 withdrawal had not reached `storage-health-r26.json`; both companions now carry markers (QUALITY 67).
- Not repaired, disclosed: the C1 and C2 counter rule gaps (pinned bytes; lesson Mistakes R27-COUNTER-PERMISSIVE); `tools/check-self-assessment.py` misses hyphenated headings such as `### Round-13 measured outcome` and its docstring still states the pre-QUALITY-65 rule; the selftest lacks the three cases MutSelfAssessQ65 names.

## Round 28 — declaration, attempt 1 (2026-10-22)

Claim base `3b9e0430b88d01415c241dd5a18b8939b8a520ac` (branch tip at dispatch, 18:50Z; it carries the round-27 non-author spot-check). Ordinals at the base, from the round-27 ordinal record (`SCORECARD.md:1043`): depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. The lowest axes are depth and adjacency at 8; this round works both, through the two counters that measure them. Both claims repair routed defects of the round-27 spot-check (`corpus/lessons/round-27-verifier-spotcheck.md:100-101`); calibration is not claimed (rounds 25 and 26 claimed it). Short box (dispatch 18:46Z, report due 19:35Z): two small claims.

| Claim | Axis (ordinal) | Before | Declared after-value | Counting command |
|---|---|---|---|---|
| C1 the adjacency counter `tools/check-adjacency-overlap.py` refuses the 24 should-fail register shapes of round-27 CritC2Tool (QUALITY 72; routed defect 2), while the live register keeps its count | adjacency 8 → 8 | 19 of 24 accepted with the counter at `dd94cb1f` over data `3b9e0430` | 0 of 24 accepted, and `control_live_anchored_rows` 6 with exit 0 | `python3 tools/mutants-adjacency-overlap.py --base <REV> --counter-rev <REV>` → last line, fields `should_fail_accepted` and `control_live_anchored_rows` |
| C2 the kernel-taint counter `tools/check-kernel-taint.py` refuses the five should-fail shapes routed by the round-27 spot-check (routed defect 3: a one-word quote, twice; a quote from a source the row does not cite) and found by CritC1Tool as tool bugs (a Gate table under a heading that only contains "gate"; a Gate row whose source id sits in a non-source cell), while the live entry keeps its count | depth 8 → 8 | 5 of 5 accepted with the counter at `75f410c8` over data `3b9e0430` | 0 of 5 accepted, and the unmutated control keeps `verified_rows` 6 with exit 0 | `python3 tools/mutants-kernel-taint.py --base <REV> --counter-rev <REV>` → last line, fields `should_fail_accepted` and `control_verified_rows` |

"Accepted" means exit 0 with the full count (6) in any run of that mutant. C1's 24 shapes are the round-27 CritC2Tool `driver.py` mutants of kind should-fail plus its `driver2.py` altered-pinned-snapshot mutant, carried byte-for-byte as the mutate functions of `tools/mutants-adjacency-overlap.py`; each runs with the live mori repository and with an empty sibling root. C2's five shapes are CritC1Tool's `generic_word_quote`, `generic_word_quote_the`, `quote_from_uncited_rejected_source`, `gate_heading_investigate` and `gate_source_from_location_cell` (`.ufo/waves/round-27/w2a2/CritC1Tool/mutants.out` lines 2, 3, 16, 17, 18).

Separability: C1 changes only `tools/check-adjacency-overlap.py` and adds its battery; C2 changes only `tools/check-kernel-taint.py` and adds its battery. Neither battery reads the other counter.

Disclosure (before any commit of this round): the L1 ran the uncommitted C1 counter through the battery once during development at about 18:56Z (0 of 24 accepted, control 6). The declared value is the one stated above; it is re-measured at the round's commits by the counting command, and wave seats re-run it.

Other routed items: 1 the Gate of `corpus/lessons/round-28.md` records at least one reject or defer decision with its reason; 7 QUALITY 69 names its lesson id. Routed 4 and 6 are not claimed and stay owed; routed 5 and 8 are mori's or the operator's. No exploratory claim, no ordinal change, no package transaction, no service, module, sysctl, boot or configuration action. The L1 holds the planner seat.

### Round 28 measured outcome

Counting tools are the battery and counter bytes at each named revision; the batteries rebuild every mutant from `git archive` of `--base` in a private temporary directory. Receipts: `.ufo/waves/round-28/measure/` (at `79d4264d`) and `.ufo/waves/round-28/measure/final/` (at `9a0654ba8eb053a39e6374a97a25d91f6464b965`, the last counter revision).

| Claim | Before | After | Author verdict |
|---|---|---|---|
| C1 adjacency counter refuses the 24 should-fail register shapes | 19 of 24 accepted, counter `dd94cb1f` over data `3b9e0430` and over data `9a0654ba` (`measure/c1-before-dd94cb1f-on-3b9e0430.jsonl`, `measure/final/c1-before-dd94cb1f-on-9a0654ba.json`) | 0 of 24 accepted, `control_live_anchored_rows` 6, exit 0, at `79d4264d` and at `9a0654ba` (`measure/c1-after-79d4264d.jsonl`, `measure/final/c1-after-9a0654ba.jsonl`); `should_pass_accepted` 4 | declared target met by the declared command. Wave-1 seats reproduced it (RerunC1Battery) and showed each of B1 and B4 refuses its family by itself (RevFamilyB1, RevFamilyB4). Limits: CritC1NewShapes found 21 further padding shapes the f8e3a8f2 counter accepts; the `./` path, mixed-fence and four-space shapes are now refused (43-case selftest), the rest (duplicated anchors, self-sourced PROVINCE quotes, withdrawn markers, clipped words) stay open and are listed in `corpus/lessons/round-28.md`. The 0 of 24 was first observed in development before the declaration commit (disclosed; lesson Mistakes R28-RUN-BEFORE-DECLARATION) |
| C2 kernel-taint counter refuses the five routed should-fail shapes | 5 of 5 accepted, counter `75f410c8` over data `3b9e0430` and over data `9a0654ba` (`measure/c2-before-75f410c8-on-3b9e0430.jsonl`, `measure/final/c2-before-75f410c8-on-9a0654ba.json`) | 0 of 5 accepted, `control_verified_rows` 6, exit 0, at `79d4264d` and at `9a0654ba` (`measure/c2-after-79d4264d.jsonl`, `measure/final/c2-after-9a0654ba.jsonl`); 52-case selftest | declared target met by the declared command, measured after the counter commit. Eight other CritC1Tool shapes stay accepted (`other_accepted`), outside the declared set |

Wave-1 changes to the counters after their first commits (each disclosed in the lesson): C1 B3 now checks only the lines the quote occupies, the LANE-GAP cap is dropped, B5 refuses unnormalised paths, B7 handles fences, indentation, duplicates and decorated cells, and three old selftest cases were restored to discriminate (CritAxisHarm finding 3); C2 R4b compares normalised source ids (CritC2RuleDesign finding 2). The declared after-values were re-measured at `9a0654ba` with the same commands.

Contested framing (wave-1 CritClaimSizing, not resolved by the author): both claims change checking tools, which AXES.md may read as operability rather than depth and adjacency; if so they are one claim on an axis at 9 and the lowest-axis duty is unmet. The author's reading is that each counter is the measuring instrument of its axis's latest claim (`SCORECARD.md:995-996`); the operator rules. No target is narrowed.

Ordinal record, round 28 (no ordinal moved): depth 8 → 8; coverage 9 → 9; operability 9 → 9; freshness 9 → 9; calibration 9 → 9; adjacency 8 → 8.

## Axes — current self-assessment (round 28)

Appended 2026-10-22 by round 28. This table supersedes the round-27 table as the lane's current self-assessment; the ordinals are unchanged. Only the depth row's counts change: the round-27 spot-check added a 31st lesson file after the round-27 table was written (`check-self-assessment.py` K10 mismatch at the base `3b9e0430`), and round 28 adds `corpus/lessons/round-28.md` and the round28 registry table in `SKILL.md`. Counts were filled by the L1 at the revision that adds this table; re-run `python3 tools/check-self-assessment.py --revision <REV>` before treating any count here as current.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 50 notes (`ls corpus/knowledge/*.md`, counted with `wc -l`); `SKILL.md` 2531 `wc -l`; 416 table lines (`grep -c '^[|]' SKILL.md`); `corpus/lessons/` (32 files) (counted with `find corpus/lessons -type f` and `wc -l`); rules added since round 12 cite `corpus/knowledge/*.md` notes, while four standing rules near the top of `SKILL.md` cite none. Ceiling: the depth ordinal was last moved at round 4, and no round from 12 to 24 changed it, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` 256 `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); the census has six planes, each with a landed note (the oom plane is a supporting measurement in `PROVINCE.md`, not a declared surface); the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry but have no census plane. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (97 cases, 97 passed, 0 failed) with exit 0; the live run exits 1 with a six-plane rollup; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes) stand; all 50 notes now carry a `recheck:` line, and the round-1 figure of 25 of 25 per-note rechecks is historical; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop for rounds 1 to 9; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; this round's C1 makes the lane's own table measurable against repository state. Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |

## Round 29 — declaration, attempt 1 (2026-10-22)

Claim base `16e9ab2abfac430b4e960e8ce64b90420f602342` (branch tip at dispatch, 19:46Z). Ordinals at the base (`SCORECARD.md:1090-1095`): depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. Depth and adjacency are tied lowest; C1 works depth. Axis framing (open round-28 dispute, CritClaimSizing): each claim is placed on the axis its counting command measures. C1's command counts corrected domain statements, each tied to a cited source or capture (AXES.md depth: "verifiable technical detail ... cited sources"). C2's command counts lane tools whose git runs follow an inherited environment, a runnable-artifact behaviour (AXES.md operability). No calibration claim (rounds 25 and 26 claimed it). Both counters are committed in this declaration commit, before any counted run.

| Claim | Axis (ordinal) | Before | Declared after-value | Counting command |
|---|---|---|---|---|
| C1 the twelve owed statements of the round-27 spot-check routed defects 4 and 5 (`corpus/lessons/round-27-verifier-spotcheck.md:102-103`), frozen as O01 to O12 in the counter, each carry one source-backed correction marker; O01 to O04 (the "+200 band scanned first" kernel OOM victim-selection reading) need an `S###` source opened this round | depth 8 → 8 | measured at the declaration commit | `marked` 12 of 12, exit 0 | `python3 tools/check-owed-statements-r29.py --revision <REV>` → last line, field `marked` |
| C2 the eight lane tools that run git writes (frozen list in the probe) no longer follow an inherited `GIT_DIR`, `GIT_WORK_TREE` or `GIT_INDEX_FILE` (routed defect 2 of the round-28 spot-check, widened from the two batteries to every tool with a sandbox git write) | operability 9 → 9 | measured at the declaration commit | `leaking` 0 of `targets` 8, `harness_errors` empty, exit 0 | `python3 tools/probe-git-env-leak.py --revision <REV>` → last line, fields `leaking`, `targets`, `harness_errors` |

Sizing. C1: the twelve anchors were screened as verbatim substrings of their files at the base before this commit (`grep -cF` → 1 each for the six Markdown anchors; for the six JSON anchors the named row field holds the text). C2: the eight targets were screened by their control runs only (no canary): each exits 0 from a `git archive 16e9ab2a` export (the six `--selftest` runs in 0 to 1 s, the batteries in 3 to 4 s). No canary run and no counter run happened before this commit. If the before-value of C2 is below 2 (SentinelBattery showed both batteries leak, `.ufo/waves/round-28/w1/SentinelBattery.md` finding 3), C2 has nothing to fix and lands as not verified.

Separability: C1 changes only corpus files, `SKILL.md` and `corpus/SOURCES.md`; C2 changes only `tools/*.py`. The C1 counter reads no tool behaviour and the probe reads no corpus file.

Routed items of the round-28 spot-check (`corpus/lessons/round-28-verifier-spotcheck.md:87-95`) that are not claims: 1 a C2 battery receipt at the tip counter `99f35675…` (`.ufo/waves/round-29/measure/r28-c2-battery-at-16e9ab2a.jsonl`, run during screening from an export of the base: 0 of 5, control 6); 3 the R4a two-word half gets selftest cases that kill MutC2Counter m1 and m7; 4 the C1 padding shapes; 5 carried round-27 defect 6 (self-assessment tool); 6 RevFamilyB2's lost B2-family review is redone in wave 1; 7 is answered by the framing above. No exploratory claim, no ordinal change, no package transaction, no service, module, sysctl, boot or configuration action. The L1 holds the planner seat.

### Round 29 measured outcome

Counting tools are the counter and probe bytes at each named revision; receipts under `.ufo/waves/round-29/measure/` (before, at the declaration commit `81a061a67466c5e1be812814a895a4b5ed89b4ff`), `measure/c1-after-*` and `c2-after-*` (at `409ceed4`) and `measure/final/` (at `75257ea68b1b5c87b429a221bee4d1f8e5d7f54a`). Seat evidence: `.ufo/waves/round-29/w1/` (35 seats) and `w2/` (37 seats).

| Claim | Before | After | Author verdict |
|---|---|---|---|
| C1 (depth) twelve owed statements carry a source-backed correction marker | `marked` 0 of 12 at `81a061a67466c5e1be812814a895a4b5ed89b4ff` (declared counter `5b6cf227…`; also 0 under versions 2 and 3) | `marked` 12 of 12 at `409ceed4` and at `75257ea68b1b5c87b429a221bee4d1f8e5d7f54a`, exit 0, under the declared counter, version 2 (`c3f9cfe7…`) and version 3 (`1c37d492…`) | declared target met. The counter was tightened twice after attacks (wave-1 CritOwedCounterShapes: declared counter accepts 20 of 25 battery shapes; wave-2 CritOwedV2Shapes: version 2 accepts 18 of 19 landed-marker shapes); version 3 accepts 0 of 29 and 0 of 19 with controls 12 (`final/c1-battery-v3.jsonl`, `final/c1-landed-battery-v3.jsonl`). Reviewer judgment per marker (wave 2): eleven hold, O07 partly held and was repaired. Only O01 to O04 add new sourced detail (S148, S149); O05 to O12 carry corrections already argued in the Markdown companions into `SKILL.md` and the JSON files (QUALITY 67), or close an `[unk]` from an existing capture (O08); the framing contest stays with the operator |
| C2 (operability) the eight frozen git-writing tools no longer follow an inherited `GIT_DIR`, `GIT_WORK_TREE` or `GIT_INDEX_FILE` | `leaking` 3 of 8 at `81a061a67466c5e1be812814a895a4b5ed89b4ff` (the adjacency selftest helper and both batteries; probe `46a55ce7…`) | `leaking` 0 of 8, `harness_errors` empty, exit 0, at `409ceed4`, `10d5288f` (wave-2 RerunProbe, CritClaimFraming2) and `75257ea68b1b5c87b429a221bee4d1f8e5d7f54a` | declared target met. The set is the eight tools matched by the frozen grep; three leaked (as exit-code divergences; the canary was never written), five never did. Each fix is load-bearing (wave-2 MutScrubAdjBattery, MutScrubKtBattery, MutScrubAdjSelftest: reverting it makes the probe flag the tool). Outside the set, 0 of 12 further git-writing selftests leak (RevProbeOutsideSet). Not closed: PATH `git` wrappers, a per-user attributes file, enclosing-repo discovery, the probe's inherited `HOME` (SentinelResidualEnv) |

Routed repairs (not claims): R4a selftest case (m1 and m7 now fail the selftest, RevR4aFix); `check-self-assessment.py` hyphenated headings, docstring and four cases (RevSelfAssessFix); the C2 battery receipt at the round-28 tip counter (`measure/r28-c2-battery-at-16e9ab2a.jsonl`); the lost RevFamilyB2 review redone (RevFamilyB2Redo). Routed defect 4 (adjacency padding shapes) was landed at `10d5288f` and reverted at `75257ea68b1b5c87b429a221bee4d1f8e5d7f54a` after wave-2 CritPaddingOverStrict showed it refuses 15 of 19 correct register variants and still accepts 24 new padding shapes; owed.

Axis framing (operator ruling pending, round-28 routed 7): each claim is placed on the axis its counting command measures; this is the author's reading, not an answer to the open question. Wave-1 CritAxisFraming and wave-2 CritClaimFraming2 argue that most of C1's twelve items are companion carry-over rather than depth.

Ordinal record, round 29 (no ordinal moved): depth 8 → 8; coverage 9 → 9; operability 9 → 9; freshness 9 → 9; calibration 9 → 9; adjacency 8 → 8.

## Axes — current self-assessment (round 29)

Appended 2026-10-22 by round 29. This table supersedes the round-28 table as the lane's current self-assessment; the ordinals are unchanged. Only the depth row's counts change: `SKILL.md` gains the OOM victim-selection section, the O05 marker and the round29 registry table, and `corpus/lessons/` gains the round-28 spot-check and `round-29.md`. Counts were filled by the L1 at the revision that adds this table; re-run `python3 tools/check-self-assessment.py --revision <REV>` before treating any count here as current.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 50 notes (`ls corpus/knowledge/*.md`, counted with `wc -l`); `SKILL.md` 2598 `wc -l`; 460 table lines (`grep -c '^[|]' SKILL.md`); `corpus/lessons/` (34 files) (counted with `find corpus/lessons -type f` and `wc -l`); rules added since round 12 cite `corpus/knowledge/*.md` notes, while four standing rules near the top of `SKILL.md` cite none. Ceiling: the depth ordinal was last moved at round 4, and no round from 12 to 24 changed it, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` 256 `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); the census has six planes, each with a landed note (the oom plane is a supporting measurement in `PROVINCE.md`, not a declared surface); the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry but have no census plane. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (97 cases, 97 passed, 0 failed) with exit 0; the live run exits 1 with a six-plane rollup; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes) stand; all 50 notes now carry a `recheck:` line, and the round-1 figure of 25 of 25 per-note rechecks is historical; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop for rounds 1 to 9; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; this round's C1 makes the lane's own table measurable against repository state. Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |

## Round 30 — declaration, attempt 1 (2026-10-22)

Claim base `fbfec6bdf8833e7513732a06000801a8ee9b690b` (branch tip at dispatch, 20:57Z). Ordinals at the base (`SCORECARD.md:1133-1138`): depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. Depth and adjacency are tied lowest; C1 works depth. Following the round-29 spot-check ruling (C1DepthFraming: only O01–O04 were new depth), C1 adds new sourced host knowledge on a surface the lane has not covered — btrfs space allocation and ENOSPC — instead of carrying existing corrections into companions: `Global reserve`, `unallocated` and the allocation sysfs files have 0 hits in `SKILL.md`, `corpus/knowledge/` and `corpus/SOURCES.md` at the base (`grep -rl`). Both counting tools and the C1 battery are committed in this declaration, before any counted run.

| Claim | Axis (ordinal) | Before | Declared after-value | Counting command |
|---|---|---|---|---|
| C1 ten frozen btrfs space questions D01–D10 (D01 unallocated space and ENOSPC, D02 global reserve, D03 balance usage filters, D04 metadata DUP, D05 block-group reclaim, D06 the allocation sysfs directory, D07 snapshots keep extents allocated, D08–D10 host metadata, data/unallocated and global-reserve values from a read-only sysfs capture) each answered by one row of `corpus/knowledge/btrfs-space-r30.json` that quotes a `mined` source opened this round at a cited snapshot line and has one `| [R30-Dnn] ` decision-table line in `SKILL.md` (rules R1–R9 in the counter docstring) | depth 8 → 8 | measured at the declaration commit | `verified` 10 of 10, exit 0 | `python3 tools/check-btrfs-space-r30.py --revision <REV>` → last line, field `verified` |
| C2 the eleven frozen git-writing lane tools (the round-29 eight plus `check-self-assessment.py --selftest` and both round-29 owed-statement batteries) stop following the three residual git channels of the round-29 spot-check routed defect 4 — a `git` wrapper on `PATH`, per-user git files under `HOME`/`XDG_CONFIG_HOME` (config, hooks path, ignore, attributes), and an enclosing repository — 33 (tool, channel) pairs | operability 9 → 9 | measured at the declaration commit | `leaking` 0 of `pairs` 33, `harness_errors` empty, exit 0 | `python3 tools/probe-git-env-residual-r30.py --revision <REV>` → last line, fields `leaking`, `pairs`, `harness_errors` |

Sizing and fail conditions. C1: the counter reads 0 at the base by construction (no JSON file); its battery `tools/mutants-btrfs-space-r30.py` (QUALITY 73) is committed with it: control 10 on a synthetic fixture, 46 should-fail shapes (including the round-29 spot-check routed-2 shapes: `<!-->` before a hidden comment, list-prefixed and indented markers, extra JSON keys such as `"status": "withdrawn"`, italic, bold and unbalanced-asterisk ids) and 6 should-pass shapes; a miss on any of the ten frozen questions is an honest stop. C2: if the before-value is below 3 leaking pairs, C2 has too little to fix and lands as not verified; the probe's control run no longer inherits the caller's `HOME` (the fourth round-29 residual item).

Separability: C1 changes only `corpus/`, `SKILL.md` and round-30 wave evidence; C2 changes only the eleven target tools. The C1 counter reads no tool behaviour and the probe reads no corpus file.

Routed items of the round-29 spot-check (`corpus/lessons/round-29-verifier-spotcheck.md:144-154`) that are not claims: 1 committed receipts for the v4 batteries (digest `3516d579…`), the declared round-29 counter (`5b6cf227…`) at a tip-equal revision, and a revision field in selftest receipts, plus every "Gates at" row of this round's report backed by a committed receipt naming its revision; 2 v4 battery shapes for `<!-->`, list-indented code, extra JSON metadata values and the italic id; 3 adjacency padding shapes; 4 is claim C2; 5 the depth framing statement (only O01–O04 are depth); 6 committed receipts for the sandbox-only round-29 mutation tests. No exploratory claim, no ordinal change, no package transaction, no service, module, sysctl, boot, balance or configuration action. The L1 holds the planner seat.

### Round 30 measured outcome

Counting tools are the declared bytes (counter v1 and probe at `8fb2cef0`) run through `tools/run-receipt.py`; every receipt header names the revision and tool digest. Before receipts: `.ufo/waves/round-30/measure/c1-before-8fb2cef0….jsonl`, `c2-before-8fb2cef0….jsonl`. After receipts at `a3f19372`: `.ufo/waves/round-30/measure/after-a3f19372/`; final-tip receipts: `.ufo/waves/round-30/measure/final/`. Seat evidence: `.ufo/waves/round-30/w1/` (35 seats) and `w2/` (46 seats).

| Claim | Before | After | Author verdict |
|---|---|---|---|
| C1 (depth) D01-D10 sourced btrfs space rows | `verified` 0 of 10 at `8fb2cef0` (declared v1 `1bf7ee14…`) | `verified` 10 of 10, exit 0, under declared v1 and under v2 (`4953203d…`) at `a3f19372` and at the final tip (`measure/final/`); wave-2 RerunC1Counters reproduced every number | declared target met. Limits (wave 2): a sourceless fixture also reaches 10 of 10 under v1 and v2 (CritClaimFraming2), so the count measures provenance and format, not depth; per-row review: D01, D09 hold, D07 and D08 held after wording fixes; firm new depth is D01, D02, D03, D07 with D05 thin; D04 and D06 restate round 26; D08-D10 are captures; S154, S155, S158 are re-reads of round-26 bytes. v2 still accepts 33 new shapes and refuses 9 legitimate layouts (wave-2 CritCounterV2); no v3 this round |
| C2 (operability) eleven tools x three residual git channels | `leaking` 17 of 30 pairs plus one harness error (exit 2) at `8fb2cef0`; honest before at least 19 of 33 (wave-1 CritClaimFraming, CritProbeDesign) | `leaking` 0 of 33, `harness_errors` [], exit 0 at `a3f19372` (declared probe `c8f61996…`), reproduced at `29bf87fa` by wave-2 RerunC2Probe and at the final tip | declared target met. Each fix is load-bearing on its channel except check-freshness-r17's HOME override, whose user-files channel never leaked (wave-2 MutScrubChannels). Not seen by the probe: stdout-only hollow fixes, LD_PRELOAD, a dropped `.git` pointer (SentinelGitEnv3, SentinelProbeHollow); owed |

Routed repairs (not claims): round-29 v4 battery and declared-counter receipts (`w1/ExecReceiptsR29/`); counter v5 and the v4-shapes battery (`85712671`); adjacency padding shapes (`7165f11e`, 53 of 53 refused, 19 of 19 variants accepted); sandbox mutant receipts (`w1/MutReceiptsR29/`); depth framing statement in `corpus/lessons/round-30.md`. `tools/check-report-receipts.py` was repaired after wave-2 RevReportReceipts showed it self-satisfied on seat reports; it still fails the round-29 report (25 of 25) and over-reports legacy receipts that carry no run-receipt header.

Ordinal record, round 30 (no ordinal moved): depth 8 → 8; coverage 9 → 9; operability 9 → 9; freshness 9 → 9; calibration 9 → 9; adjacency 8 → 8.

## Axes — current self-assessment (round 30)

Appended 2026-10-22 by round 30. This table supersedes the round-29 table; the ordinals are unchanged. Only the depth row's counts change: `corpus/knowledge/` gains `btrfs-space-r30.md`, `SKILL.md` gains the btrfs space section and the round30 registry table, and `corpus/lessons/` gains the round-29 spot-check and `round-30.md`. Re-run `python3 tools/check-self-assessment.py --revision <REV>` before treating any count here as current.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 51 notes (`ls corpus/knowledge/*.md`, counted with `wc -l`); `SKILL.md` 2672 `wc -l`; 517 table lines (`grep -c '^[|]' SKILL.md`); `corpus/lessons/` (36 files) (counted with `find corpus/lessons -type f` and `wc -l`); rules added since round 12 cite `corpus/knowledge/*.md` notes, while four standing rules near the top of `SKILL.md` cite none. Ceiling: the depth ordinal was last moved at round 4, and no round from 12 to 24 changed it, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` 256 `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); the census has six planes, each with a landed note (the oom plane is a supporting measurement in `PROVINCE.md`, not a declared surface); the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry but have no census plane. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (97 cases, 97 passed, 0 failed) with exit 0; the live run exits 1 with a six-plane rollup; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes) stand; all 51 notes now carry a `recheck:` line, and the round-1 figure of 25 of 25 per-note rechecks is historical; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop for rounds 1 to 9; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; this round's C1 makes the lane's own table measurable against repository state. Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |

## Round 30 — declaration, attempt 1 (2026-10-22)

Claim base `fbfec6bdf8833e7513732a06000801a8ee9b690b` (branch tip at dispatch, 20:57Z). Ordinals at the base (`SCORECARD.md:1133-1138`): depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. Depth and adjacency are tied lowest; C1 works depth. Following the round-29 spot-check ruling (C1DepthFraming: only O01–O04 were new depth), C1 adds new sourced host knowledge on a surface the lane has not covered — btrfs space allocation and ENOSPC — instead of carrying existing corrections into companions: `Global reserve`, `unallocated` and the allocation sysfs files have 0 hits in `SKILL.md`, `corpus/knowledge/` and `corpus/SOURCES.md` at the base (`grep -rl`). Both counting tools and the C1 battery are committed in this declaration, before any counted run.

| Claim | Axis (ordinal) | Before | Declared after-value | Counting command |
|---|---|---|---|---|
| C1 ten frozen btrfs space questions D01–D10 (D01 unallocated space and ENOSPC, D02 global reserve, D03 balance usage filters, D04 metadata DUP, D05 block-group reclaim, D06 the allocation sysfs directory, D07 snapshots keep extents allocated, D08–D10 host metadata, data/unallocated and global-reserve values from a read-only sysfs capture) each answered by one row of `corpus/knowledge/btrfs-space-r30.json` that quotes a `mined` source opened this round at a cited snapshot line and has one `| [R30-Dnn] ` decision-table line in `SKILL.md` (rules R1–R9 in the counter docstring) | depth 8 → 8 | measured at the declaration commit | `verified` 10 of 10, exit 0 | `python3 tools/check-btrfs-space-r30.py --revision <REV>` → last line, field `verified` |
| C2 the eleven frozen git-writing lane tools (the round-29 eight plus `check-self-assessment.py --selftest` and both round-29 owed-statement batteries) stop following the three residual git channels of the round-29 spot-check routed defect 4 — a `git` wrapper on `PATH`, per-user git files under `HOME`/`XDG_CONFIG_HOME` (config, hooks path, ignore, attributes), and an enclosing repository — 33 (tool, channel) pairs | operability 9 → 9 | measured at the declaration commit | `leaking` 0 of `pairs` 33, `harness_errors` empty, exit 0 | `python3 tools/probe-git-env-residual-r30.py --revision <REV>` → last line, fields `leaking`, `pairs`, `harness_errors` |

Sizing and fail conditions. C1: the counter reads 0 at the base by construction (no JSON file); its battery `tools/mutants-btrfs-space-r30.py` (QUALITY 73) is committed with it: control 10 on a synthetic fixture, 46 should-fail shapes (including the round-29 spot-check routed-2 shapes: `<!-->` before a hidden comment, list-prefixed and indented markers, extra JSON keys such as `"status": "withdrawn"`, italic, bold and unbalanced-asterisk ids) and 6 should-pass shapes; a miss on any of the ten frozen questions is an honest stop. C2: if the before-value is below 3 leaking pairs, C2 has too little to fix and lands as not verified; the probe's control run no longer inherits the caller's `HOME` (the fourth round-29 residual item).

Separability: C1 changes only `corpus/`, `SKILL.md` and round-30 wave evidence; C2 changes only the eleven target tools. The C1 counter reads no tool behaviour and the probe reads no corpus file.

Routed items of the round-29 spot-check (`corpus/lessons/round-29-verifier-spotcheck.md:144-154`) that are not claims: 1 committed receipts for the v4 batteries (digest `3516d579…`), the declared round-29 counter (`5b6cf227…`) at a tip-equal revision, and a revision field in selftest receipts, plus every "Gates at" row of this round's report backed by a committed receipt naming its revision; 2 v4 battery shapes for `<!-->`, list-indented code, extra JSON metadata values and the italic id; 3 adjacency padding shapes; 4 is claim C2; 5 the depth framing statement (only O01–O04 are depth); 6 committed receipts for the sandbox-only round-29 mutation tests. No exploratory claim, no ordinal change, no package transaction, no service, module, sysctl, boot, balance or configuration action. The L1 holds the planner seat.

## Round 31 — declaration, attempt 1 (2026-10-22)

Claim base `2077e2fa4fa70ea79aa77b6d91f4acd35bc54897` (branch tip at dispatch, 22:38Z). Ordinals at the base (`SCORECARD.md:1174-1179`): depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. Depth and adjacency are tied lowest; C1 works depth. Round 30 was rejected as an honest stop because its depth counter could not fail on depth: a sourceless fixture reached its target (`corpus/lessons/round-30-verifier-spotcheck.md`, section 2, C1). This declaration therefore names the surface each claim changes, freezes one predicate per claim, and commits the cheapest do-nothing controls scored under that predicate before any seat produces data (addendum section 9).

| Claim | Axis (ordinal), surface changed | Before | Declared after-value | Counting command |
|---|---|---|---|---|
| C1 eight frozen btrfs repair and maintenance questions Q01–Q08 (Q01 defragmenting shared extents, Q02 `btrfs rescue zero-log`, Q03 `btrfs check --repair`, Q04 `autodefrag`, Q05 `commit=`, Q06 `nodatacow`, Q07 `btrfs replace`, Q08 trim modes), each answered by one row of `corpus/knowledge/btrfs-repair-r31.json` and one `\| [R31-Qnn] ` decision line in `SKILL.md`, grounded in btrfs-progs v7.1 documentation bytes pinned by sha256 in the counter | depth 8 → 8; surface: `SKILL.md` decision lines and a knowledge entry on btrfs repair and maintenance decisions, a topic with 0 base hits (sweep below) | measured at the declaration commit | `new_sourced` 8 of 8, exit 0 | `python3 tools/check-btrfs-repair-r31.py --revision <REV>` → last line, field `new_sourced` |
| C2 the eleven frozen git-running lane tools of the round-30 probe stop passing loader and interpreter injection variables to their child processes, give every git child the system-scope contract, and keep parity with their control run under a dropped `.git` pointer — 33 (tool, channel) pairs over the channels `loader-env`, `child-contract`, `dotgit-pointer` | operability 9 → 9; surface: the child-process environment the eleven tools build | measured at the declaration commit | `leaking` 0 of `pairs` 33, `harness_errors` empty, exit 0 | `python3 tools/probe-git-child-env-r31.py --revision <REV>` → last line, fields `leaking`, `pairs`, `harness_errors` |

Frozen predicate C1, label `new_sourced` (the same sentence is in the counter docstring and in every receipt's summary field `predicate`): a frozen question counts as `new_sourced` when its single row in corpus/knowledge/btrfs-repair-r31.json quotes, verbatim at the cited line, a committed snapshot whose sha256 equals the question's frozen pin, cites an S### row that is absent from the base registry and is `mined` at REV with that pin and URL, states a word of every sealed answer-key group in a statement of at least 12 words that shares no 6-word run with the quote, carries a frozen novelty token in quote, statement and its one `| [R31-Qnn] ` SKILL.md line, and every frozen novelty token of the question has 0 hits in the base corpus.

Frozen predicate C2, label `leaking` (the same conditions are in the probe docstring and code; each receipt line carries `leak`): a (tool, channel) pair is `leaking` when, for `loader-env`, any traced execve after the tool's own first exec carries the injected `LD_PRELOAD`/`LD_LIBRARY_PATH`/`PYTHONPATH` path, or the run breaks parity with the control; for `child-contract`, any successful git execve of the control run lacks `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null` or a non-empty `GIT_CEILING_DIRECTORIES`; for `dotgit-pointer`, the canary repository named by a `.git` pointer file in the working directory and in TMPDIR changes, or the run breaks parity with the control. Parity is equal exit code, equal normalised stdout digest and equal count of successful git execs (this closes the round-30 stdout-only gap).

Novelty sweep (QUALITY 68), run before this commit: `git grep -i -F -c -e <token> 2077e2fa -- SKILL.md PROVINCE.md corpus` gives 0 for every frozen novelty token: defragment, reflink, zero-log, log tree, --repair, autodefrag, defragmentation, commit=, periodic transaction commit, nodatacow, nodatasum, btrfs replace, replace start, fstrim. The counter re-runs this sweep on every invocation (rule R8). The six pinned snapshots were opened by the L1 at 22:50Z with plain curl from `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/<file>` (HTTP 200) and equal a v7.1 clone byte for byte.

Do-nothing controls (committed with the before receipts, before wave 1 dispatches; builder `.ufo/waves/round-31/measure/controls/build-c1-controls.py`): K0 the base; K2 the lane's own round-30 rows D01–D08 relabelled (re-scoring held knowledge); K3 real pinned snapshots and well-formed `mined` rows with filler statements (a junk-row commit); K4 K3 with each quote copied as the statement. Sealed controls (their builder's sha256 is committed before data, the file after data): K1 a sourceless forgery (the counter's own bytes as the snapshot, a made-up S900 row, every answer key in the statements) and K5 a reader-written positive control. Expected under the frozen counter: K0–K4 and K1 score below 8; K5 scores 8, which shows the counter can say yes. If any do-nothing control (K0, K1, K2, K3, K4) reaches 8, C1 is withdrawn before data. The answer keys are sealed as salted digests so that a writer who skips the source cannot copy them; the plaintext lands in the round-31 lesson after data and must hash to the committed digests. Declared ceiling: a reader can string the keys with filler, and the 16-hex digests admit a dictionary attack; row truth and usefulness are judged by wave-2 row reviewers, not by the counter.

C2 controls: the base tools are the do-nothing control (its receipt is the before-value). A hollow control — `check-kernel-taint.py` changed to exit 0 with no output whenever `LD_PRELOAD` is set — is built in a sandbox clone and scored under the frozen probe before data; it must read `leaking`. Kill rule: if the before-value is below 3 leaking pairs, C2 has too little to fix and lands as not verified.

Separability: C1 changes only `corpus/`, `SKILL.md` and round-31 wave evidence; C2 changes only the target tools (and `tools/check-owed-statements-r29.py`, whose git children the two owed-statement batteries start). The C1 counter reads no tool behaviour and the probe reads no corpus file.

Routed items of the round-30 spot-check (`corpus/lessons/round-30-verifier-spotcheck.md`, section 5) that are not claims: 1 the able-to-fail depth target is this declaration's C1 design plus QUALITY 80 (a novelty and do-nothing-control criterion grounded in a round-31 Mistakes row); 2 an erratum for the duplicate round-30 declaration at `SCORECARD.md:1181-1194` (appended, never rewritten); 3 the dangling QUALITY 78 and 79 lesson pointers are corrected by an appended note; 4 the three untracked round-30 symlink fixtures are deleted and the three committed `__pycache__/*.pyc` files are removed; 5 the probe gaps are claim C2 (stdout parity, `LD_PRELOAD`/`PYTHONPATH`, dropped `.git` pointer, system-config scope through the child contract); repository-local `include`/`core.fsmonitor` stays owed and is named as such; 6 the carried items stay owed unless a wave-1 seat lands one with a receipt. No exploratory claim, no ordinal change, no package transaction, no service, module, sysctl, boot, balance, scrub, defragment or other btrfs write, and no configuration action. The L1 holds the planner seat.

### Round 31 — errata and clarifications (appended after wave 1, before the after-measurement; no target, counter, probe or predicate changes)

1. Duplicate round-30 declaration (round-30 spot-check routed defect 2). `## Round 30 — declaration, attempt 1` appears twice: lines 1140–1153 and 1181–1194. The second copy was appended by commit `32e5d848` and is byte-identical to the first apart from a trailing blank line. The first copy is authoritative; the second stays in place (append-only).
2. C1 novelty sentence. The declaration's surface cell says "a topic with 0 base hits". What was measured is narrower: the 14 frozen novelty tokens have 0 base hits. Wave-1 CritNoveltySemantic and CritClaimFraming found held neighbours in other words. Q06 is partly held: row SH3 already says NOCOW data has no checksums (`SKILL.md:2367`, `corpus/knowledge/storage-health-r26.md:43`). Q08 is partly held as a host fact: the root filesystem mounts with `discard=async` (`storage-health-r26.md:11`). Q01's premise (snapshots keep shared extents allocated) is held at `corpus/knowledge/btrfs-space-r30.md:28`, and the registered S152 snapshot already contains the defragment-breaks-reflinks sentence outside its cited anchor. Q02, Q03, Q04, Q05 and Q07 have no held neighbour beyond `PROVINCE.md:167-168` ("filesystem repair" is operator-owned), which this round leaves unchanged. Rule R8 measures token novelty, not fact novelty; QUALITY 80 now requires both.
3. C2 before-value. The before receipt at the declaration commit reads `leaking` 11 of 33 (`.ufo/waves/round-31/measure/c2-before-f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c.jsonl`). Every leak is a `loader-env` pair. `child-contract` and `dotgit-pointer` read 0 of 11 each at the base, so they act as regression guards (0 → 0). The change the claim measures is `loader-env` 11 → 0. It is not 33 fixes. None of the 11 base leaks changed an exit code, stdout digest or git exec count: they show the injected path reaching children, not a changed result.
4. Sealed answer keys (wave-1 CritKeyDictionary). A source-free dictionary of 103,090 words recovers every sealed key group (24 of 24), and the question texts alone recover 13 of 24. The declaration's sentence that a writer who skips the source "cannot copy them from this file" is therefore weaker than stated. K1 scores 0 because of the snapshot pin (R3), not the seal. Row truth and novelty rest on the wave-2 per-row reviews, as declared.

### Round 31 — wave-2 corrections (appended; no target, counter, probe or predicate changes)

5. Errata item 1 names the wrong copy. `git blame` attributes lines 1140–1153 to `32e5d848` and lines 1181–1194 to `8fb2cef0`, the round-30 declaration commit (wave-2 RevErrataRecords). So `32e5d848` inserted the earlier copy, and the later copy is the original. The two copies are identical; both stay in place.
6. Errata item 2 overstates "no held neighbour" for Q05 and Q07 (RevErrataRecords). Q07's neighbours are device removal of a missing device (S128 snapshot lines 44–76), `corpus/knowledge/storage-health-r26.md:132` (removal clears error counters) and `SKILL.md:2376` (media errors are "a replacement question for the operator"). Q05's neighbour is `storage-health-r26.md:29` ("transaction commit", in the device-statistics context). None of them states the `btrfs replace` procedure, the target-size rule or the `commit=` option.
7. The declaration says the C1 predicate sentence is "in every receipt's summary field `predicate`". The receipts carry the label `new_sourced`, not the sentence (wave-2 CritQuality80). The sentence appears in the declaration and in the counter docstring only.
8. Wave-1 ExecScrubA also changed `tools/_revision.py`, which is outside the declared C2 target set. Three gates pin its bytes or quote its line (check-pause-gate, report-red-causes, check-adjacency-anchors IN-101), and at `f3a5723a` they could not evaluate or failed (RevScrubSharedRevision). The file was restored from `8cff9e7c` in `b304b8ea`. C2 is measured again at that commit (`.ufo/waves/round-31/measure/final-b304b8ea/`). Mistake R31-SHARED-HELPER-PINNED.
9. Scripted non-reader control K6 (wave-2 CritKeyFillerControl): a script downloads the pinned files, recovers the sealed key words from their own bytes and fills the statements. It reads `new_sourced` 8 of 8 under counter `4f69a109…`, and a human reader accepts 0 of its 8 statements. The declared withdrawal rule named only K0–K4, so it did not fire. Under hyaku addendum §9, though, a no-understanding control reached the target, so the counter alone does not separate fetching from reading. Mistake R31-SCRIPTED-NONREADER; QUALITY 81.
10. The ten new `corpus/SOURCES.md` rows had been appended after `## Leads (unopened)`, outside `## Registry`. The sources census read exit 1 with E12 for S164–S173 at `f3a5723a` (wave-2 RevGatesTip). The rows were moved, unchanged, to follow S163 inside the Registry section. The S171–S173 used-by cells were narrowed to `corpus/lessons/round-31.md`, the only file that cites them (RevSourceS171, RevSourceS172, RevSourceS173).

### Round 31 measured outcome

Counting tools are the declared bytes (counter `4f69a109…` and probe `b168b9b8…`, both at `f4861f4d`), run through `tools/run-receipt.py`; every receipt header names the revision and tool digest. Before receipts: `.ufo/waves/round-31/measure/c1-before-f4861f4d….jsonl` and `c2-before-f4861f4d….jsonl`; controls: `measure/controls/`; after receipts at the integration commit: `measure/after-13ca52d0/`; final receipts at `b304b8ea3c98760bf04e641cf7ae3d94eb77293c` (the last tools/corpus content commit): `measure/final-b304b8ea/`. Seat evidence: `.ufo/waves/round-31/w1/` (33 seats) and `w2/` (40 seats).

| Claim | Before | After | Author verdict |
|---|---|---|---|
| C1 (depth) Q01–Q08 btrfs repair and maintenance rows, predicate `new_sourced` | 0 of 8 at `f4861f4d`; do-nothing controls K0, K1, K2, K3, K4 0 of 8; positive control K5 8 of 8 | 8 of 8, exit 0, at `13ca52d0` and at `b304b8ea` (reproduced by wave-2 RerunC1Counter and every row reviewer) | **not verified.** The declared target is met, but a scripted non-reader control built after data (K6, wave-2 CritKeyFillerControl) also reads 8 of 8: the predicate cannot separate fetching the pinned sources from reading them, so by hyaku addendum §9 the count is not depth evidence. Per-row non-author reviews: seven hold, Q01 partly holds (its fact was already in the base's S152 snapshot bytes). Q04's statement was edited by the L1, who holds the keys, from "64 KiB" to the source spelling "64KiB"; the as-drafted row reads 7 of 8 (`.ufo/waves/round-31/l1/c1-as-drafted-q04-sandbox.jsonl`). Depth reading: `unprovable-but-better` (new sourced decision lines on btrfs repair, row-reviewed), ordinal 8 → 8 |
| C2 (operability) eleven tools × channels loader-env, child-contract, dotgit-pointer | 11 of 33 at `f4861f4d`, every one a loader-env pair (child-contract and dotgit-pointer 0: regression guards); hollow control H1 leaks by parity, genuine H2 reads 0 | 0 of 33, `harness_errors` [], exit 0, at `13ca52d0` and at `b304b8ea` | **target met.** Eleven per-tool reviewers found the fix complete and output-identical; MutScrubChecks and MutScrubBatteries killed every target-filter mutant (the counter-child filter is redundant). Limits: the contract is a deny-list; `BASH_ENV`, `GCONV_PATH` and 36 more names still reach children (SentinelChildEnv), repository-local config is read (SentinelRepoLocal), and the `_revision.clean_env` paths are unpatched after the revert; all owed. Ordinal 9 → 9 |

Round admission (author's reading, the operator rules): every claim must verify; C1 does not, so the round is an honest stop. No axis is harmed: the `tools/_revision.py` change that broke three pinned gates was reverted before the final measurement, and those gates are back at their base results (`measure/final-b304b8ea/gate-*.jsonl`).

Ordinal record, round 31 (no ordinal moved): depth 8 → 8; coverage 9 → 9; operability 9 → 9; freshness 9 → 9; calibration 9 → 9; adjacency 8 → 8.

## Axes — current self-assessment (round 31)

Appended 2026-10-22 by round 31. This table supersedes the round-30 table; the ordinals are unchanged. Only the depth row's counts change: `corpus/knowledge/` gains `btrfs-repair-r31.md`, `SKILL.md` gains the btrfs repair section and the round31 registry table, and `corpus/lessons/` gains the round-30 spot-check and `round-31.md`. Re-run `python3 tools/check-self-assessment.py --revision <REV>` before treating any count here as current.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 52 notes (`ls corpus/knowledge/*.md`, counted with `wc -l`); `SKILL.md` 2743 `wc -l`; 574 table lines (`grep -c '^[|]' SKILL.md`); `corpus/lessons/` (38 files) (counted with `find corpus/lessons -type f` and `wc -l`); rules added since round 12 cite `corpus/knowledge/*.md` notes, while four standing rules near the top of `SKILL.md` cite none. Ceiling: the depth ordinal was last moved at round 4, and no round from 12 to 24 changed it, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` 256 `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); the census has six planes, each with a landed note (the oom plane is a supporting measurement in `PROVINCE.md`, not a declared surface); the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry but have no census plane. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (97 cases, 97 passed, 0 failed) with exit 0; the live run exits 1 with a six-plane rollup; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes) stand; all 52 notes now carry a `recheck:` line, and the round-1 figure of 25 of 25 per-note rechecks is historical; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop for rounds 1 to 9; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; this round's C1 makes the lane's own table measurable against repository state. Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |

## Round 32 — declaration, attempt 1 (2026-10-23)

Claim base `58cc2e0bfaa4580d47f6817537c8d5c82dbe9c92` (branch tip at dispatch, 01:03Z). Ordinals at the base (`SCORECARD.md:1246`, round-31 measured outcome): depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. Depth and adjacency are tied lowest. Rounds 30 and 31 were rejected on one blocker: a depth counter that a content-free control reached (round 30: a sourceless fixture, 10 of 10; round 31: a scripted non-reader, K6, 8 of 8). This round therefore works the other lowest axis, adjacency, and neither claim counts rows of prose: both counters run code and score its observable behaviour on inputs generated at score time.

| Claim | Axis (ordinal), surface changed | Before | Declared after-value | Counting command |
|---|---|---|---|---|
| C1 the host census routes two classes of sibling-owned evidence to mori (`PROVINCE.md` row ADJ-04, anchor OUT-005) by printing a `HANDOFF ADJ-04 mori class=<kill-events\|coredumps> value=<n> kind=dated-event state=prepared` line, while its six PLANE lines, rollup line and exit code stay those of the base census | adjacency 8 → 8; surface: the census's output gains a finding-to-owner handoff line (the ADJ table made executable); the command that shows it unmoved is `bash tools/tsukuroi-census.sh \| grep -c '^HANDOFF'` (0 at the base) | measured at the declaration commit (fresh seed; only scenarios that need no handoff can be routed) | `routed` 24 of 24 with `harness_errors` 0, exit 0, on a fresh seed | `python3 tools/score-census-handoff-r32.py --revision <REV>` → last line, fields `routed`, `scenarios`, `harness_errors` |
| C2 the eleven git-running lane tools of the round-31 probe build their children's environment from an allow-list instead of the round-31 deny-list (`GIT_`/`LD_`/`PYTHON` prefixes), so an arbitrary ambient name no longer reaches any child | operability 9 → 9; surface: the child-process environment the eleven tools build; the command that shows it unmoved is the probe itself (11 of 11 at the base in development) | measured at the declaration commit | `leaking` 0 of `pairs` 11, `harness_errors` empty, exit 0 | `python3 tools/probe-child-env-allowlist-r32.py --revision <REV>` → last line, fields `leaking`, `pairs`, `harness_errors` |

Frozen predicate C1, label `routed` (the same sentence is the docstring's `FROZEN PREDICATE` and the constant `PREDICATE` of `tools/score-census-handoff-r32.py`; every receipt's summary line carries `predicate_label` `routed`): "A scenario is routed when the census at REV, run against that scenario's fixture, prints exactly the set of HANDOFF lines the scenario requires (one class=kill-events line with value equal to the planted dated kill events when there are any, one class=coredumps line with value equal to the planted coredump entries when there are any, no HANDOFF line otherwise, and none for a cumulative counter alone), and its PLANE lines, TSUKUROI_CENSUS line and exit code equal those of the base census 58cc2e0b on the same fixture."

Frozen predicate C2, label `leaking` (the same sentence is the docstring's `FROZEN PREDICATE` and the constant `PREDICATE` of `tools/probe-child-env-allowlist-r32.py`; every receipt's summary line carries `predicate_label` `leaking`): "A target is leaking when, in its ambient-names run, any traced execve after the target's own first exec carries in its environment any injected name (the four named and the eight random names of that run), or the run breaks parity with control run A (exit code, normalised stdout digest, count of successful git execs)." The four named are `BASH_ENV`, `ENV`, `GCONV_PATH` and `PERL5OPT`; the eight random names are drawn fresh per run (2 to 20 characters of `[A-Za-z0-9_]`, mixed case), half with a value that holds no `/`.

Inputs generated at score time (the shortcut guard). C1: 24 scenarios per run from a fresh seed, seven types (none, kill-events, coredumps, both, cumulative-only, cumulative+coredumps, tsukuroi-only), each at least twice, n and m drawn from 1 to 9, random directory names; the expected set lives only in the scorer's memory; the base census must show the planted facts on its PLANE lines or the run is a harness error. C2: the random names exist only for one run, so a deny-list keyed on the probe's names, a rule keyed on values, or a rule keyed on a name shape leaks.

Kill rule and controls (hyaku addendum §9 and the 01:05Z pre-freeze control wave). Before any data seat, fresh critic and mutation-tester seats build, in sandbox clones, the cheapest controls that skip the claimed work and score them under these frozen counters, with receipts committed before data: for C1 the base census (do-nothing), an always-emit census, a census keyed on the cumulative ledger, a census keyed on plane verdicts, junk lines, a census that tries to read the scorer's expectations, a census that counts fixture lines without reading their class, and a census that hands off but also changes a PLANE line; for C2 the base tools (do-nothing), a deny-list extended by the four named names, a hollow fix that exits early when `BASH_ENV` is set, a value-keyed filter, a shape-keyed filter, an empty environment and a ten-of-eleven partial fix. A claim whose target any control meets is re-designed before data or declared exploratory; a miss under these predicates after data is an honest stop and is never re-scaled.

Sourced claim: C2's allow-list contract rests on source rows opened this round in wave 1 (glibc's list of variables dropped for secure execution, the bash manual's `BASH_ENV`, man-pages `environ(7)`); C1's dated-versus-cumulative rule rests on the kernel's `memory.events` and the systemd-coredump documentation, opened the same way.

Separability: C1 changes only `tools/tsukuroi-census.sh` (plus its documentation lines in `SKILL.md` and `PROVINCE.md`); C2 changes only the environment builders of the eleven targets and of `tools/check-owed-statements-r29.py`. The C1 scorer runs only the census; the C2 probe runs only the eleven targets and compares each run with a control at the same revision.

Repairs that are not claims: round-31 spot-check routed defect 4 (base receipts for the gates the report compares with the base) is `.ufo/waves/round-32/measure/base-58cc2e0b/` (eight receipts through `tools/run-receipt.py`, including check-pause-gate exit 1 `GATE-PREMISE` and check-self-assessment exit 1, mismatch K10: the round-31 depth row states 38 lesson files while `corpus/lessons` holds 39 after the round-31 spot-check landed); routed defect 5 (the K6 receipt re-issued through `run-receipt.py`) is a wave-1 item; routed defects 1 and 2 bind no claim this round (no depth claim, no sealed keys); routed defect 3 is in every wave context. No exploratory claim. No ordinal change is declared. No package transaction, service, module, sysctl, boot or filesystem write.

### Round 32 — pre-data amendment to C1's counter (control wave finding; no data seat has run)

Wave-1 seat CritPredicateC1 (pre-data control wave) showed a shortcut the v1 scorer (`b2edc669…`, at `fe1ae02c`) admits: a census that leaves its logic unchanged and prints count-derived HANDOFF lines only when it detects the scorer's fixture (the `TSUKUROI_JOURNALCTL` symlink to `.dispatch`, the `fx<hex>` hostname) reads `routed` 24 of 24 on every seed and prints nothing on the live host. Under addendum §9 the counter is fixed before data. Counter v2 (`tools/score-census-handoff-r32.py`, `VERSION = 2`) keeps every v1 rule and adds one conjunct, so it accepts a subset of what v1 accepts. The frozen predicate C1, label `routed`, now reads (the same sentence is the v2 docstring's `FROZEN PREDICATE` and its `PREDICATE` constant): "A scenario is routed when the census at REV, run against that scenario's fixture, prints exactly the set of HANDOFF lines the scenario requires (one class=kill-events line with value equal to the planted dated kill events when there are any, one class=coredumps line with value equal to the planted coredump entries when there are any, no HANDOFF line otherwise, and none for a cumulative counter alone), and its PLANE lines, TSUKUROI_CENSUS line and exit code equal those of the base census 58cc2e0b on the same fixture. The run counts only when, in addition, the census at REV run once read-only on the live host prints exactly the HANDOFF set implied by its own oom clusters and journal coredump counts, those counts equal the base census's live counts, and they are not both zero."

Declared after-value for C1 (replaces the v1 cell; the target is not narrowed): `routed` 24 of 24, `live_consistent` true, `harness_errors` 0, exit 0, on a fresh seed. A vacuous live check (no dated kill-event cluster and no coredump entry on the host at measurement time) is a harness error, exit 2, and the claim then cannot verify. Development run of v2 at the base: `routed` 10 of 24, `live_consistent` false (the live host shows `clusters=2` and `coredump=170`; the base prints no HANDOFF line), exit 1. Every C1 control is re-scored under v2 before data, and the before receipt is re-issued under v2.

### Round 32 — second pre-data amendment (C1 scorer v3, C2 probe v2; no data seat has run)

Wave-1 seat CritAntiLoop (`.ufo/waves/round-32/w1/CritAntiLoop.md`, findings 4, 7 and 8) showed two more shortcuts before any data seat ran: (a) under C1 v2, a fixture-gated census that prints cached live values (`clusters=2`, `coredump=170`, the values this declaration published) whenever the fixture is absent would pass while those host counts stay unchanged, and v2's live view compared only counts, not the PLANE text, rollup or exit code; (b) under the C2 probe v1, every generated name was 2 to 20 characters long, so a filter keyed on that length range could keep longer unknown names. It also argued that a counter change after control seats scored is contestable under §9's "after any seat has scored"; this record discloses the sequence and the closure rules on it: v1 and v2 scores came only from control seats and the L1's control runs, and every control is re-scored under the final counters before any data seat is dispatched.

C1 scorer v3 (`tools/score-census-handoff-r32.py`, `VERSION = 3`) keeps every fixture rule and replaces the single live view with two read-only live views: plain, and a view whose `TSUKUROI_JOURNALCTL` wraps the real `journalctl` and drops a seeded subset of boot-0 coredump entries (so the expected coredump value changes per run). In each view the census at REV must print the same oom and journal PLANE lines, rollup line and exit code as the base census in that view (the other four PLANE notes carry live counters such as the cgroup sweep that change between two back-to-back runs; they stay compared in full on every fixture scenario, and their verdicts are in the rollup line). The frozen predicate C1, label `routed`, now reads (the same sentence is the v3 docstring's `FROZEN PREDICATE` line and its `PREDICATE` constant): "A scenario is routed when the census at REV, run against that scenario's fixture, prints exactly the set of HANDOFF lines the scenario requires (one class=kill-events line with value equal to the planted dated kill events when there are any, one class=coredumps line with value equal to the planted coredump entries when there are any, no HANDOFF line otherwise, and none for a cumulative counter alone), and its PLANE lines, TSUKUROI_CENSUS line and exit code equal those of the base census 58cc2e0b on the same fixture. The run counts only when, in addition, in each of two read-only live views of the host (plain, and with the boot-0 journal error stream thinned by a seeded subset of its coredump entries), the census at REV prints the same oom and journal PLANE lines, TSUKUROI_CENSUS line and exit code as the base census in that view and exactly the HANDOFF set implied by the base census's oom clusters and journal coredump counts in that view, and the plain view's counts are not both zero." After-value unchanged: `routed` 24 of 24, `live_consistent` true, `harness_errors` 0, exit 0.

C2 probe v2 (`tools/probe-child-env-allowlist-r32.py`): the generator draws four names of length 2 to 20 and four of length 21 to 200; the predicate sentence and the after-value (`leaking` 0 of 11, exit 0) are unchanged. Every C2 control is re-scored under probe v2 before data.
## Axes — current self-assessment (round 32)

Appended 2026-10-23 by round 32. This table supersedes the round-31 table; the ordinals are unchanged (the round-32 measured outcome records no ordinal move). Counts that changed: `SKILL.md` gains the round-32 section and the round32 registry table; `corpus/lessons/` gains the round-31 spot-check and `round-32.md`; the census selftest gains four HANDOFF cases (97 to 101). Re-run `python3 tools/check-self-assessment.py --revision <REV>` before treating any count here as current.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 52 notes (`ls corpus/knowledge/*.md`, counted with `wc -l`); `SKILL.md` 2812 `wc -l`; 628 table lines (`grep -c '^[|]' SKILL.md`); `corpus/lessons/` (40 files) (counted with `find corpus/lessons -type f` and `wc -l`); rules added since round 12 cite `corpus/knowledge/*.md` notes, while four standing rules near the top of `SKILL.md` cite none. Ceiling: the depth ordinal was last moved at round 4, and no round from 12 to 24 changed it, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` 256 `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); the census has six planes, each with a landed note (the oom plane is a supporting measurement in `PROVINCE.md`, not a declared surface); the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry but have no census plane. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (101 cases, 101 passed, 0 failed) with exit 0; the live run exits 1 with a six-plane rollup; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes) stand; all 52 notes now carry a `recheck:` line, and the round-1 figure of 25 of 25 per-note rechecks is historical; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop for rounds 1 to 9; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; this round's C1 makes the lane's own table measurable against repository state. Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |

## Capabilities — current (round 32)

Appended 2026-10-23 by round 32. This table supersedes the round-25 table at `SCORECARD.md:840`; the rows, pointers and first-working rounds are unchanged except the host-census-gate case count, which the round-32 census change moved from 97 to 101 (four HANDOFF cases). No capability row is added: the HANDOFF lines are a census output change measured by claim C1, not a new repertoire entry. Re-run `python3 tools/check-self-assessment.py --revision <REV>` before treating any count here as current.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates where the lane learns: `corpus/SOURCES.md` holds opened, tier-scoped rows with anchors, rejections with flips, study paths, a search log and unopened leads, and the row set is checked by the frozen contract's census commands | `corpus/SOURCES.md`; the census commands and their outputs in `.ufo/evidence/round-1-kaika/after.md` (34 rows in that snapshot, malformed 0, no duplicate, enum or missing output; 125 rows at round 25) | fleet r1 (2026-10-19) |
| host-census-gate | Emits a read-only six-plane host verdict (TSUKUROI_CENSUS: HEALTHY, DEGRADED or BLOCKED; exit 0, 1 or 2) with a hermetic 101-case selftest that touches no live host surface | `tools/tsukuroi-census.sh` selftest prints PASS 101/101 rc=0 (101 cases, 101 passed, 0 failed); the live run exits 1 with a six-plane rollup; receipts `.ufo/evidence/round-1-kaika/scout-live.md` and `.ufo/evidence/round-1-kaika/after.md` | lane r2 (census-v1); demonstrated running fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations even on package-probe failure; isolates fixtures and blocks unavailable or non-directory metadata without grading intentional 0555 policy | `.ufo/waves/round-12/resumed/after.json`, `.ufo/waves/round-12/resumed/selftest-after.json`, `.ufo/waves/round-12/resumed/mode-policy-mutant.json`; measured commit `70fede2a7a890cb50a72db2d4230ee541183bf7b` | round 12 |
| boot-chain-audit | Audits every limine entry live and read-only: copies each UKI with a read-only `sudo -n cat`, extracts its initramfs in a private mktemp directory, types the new_root path, binds the firmware-selected entry, and emits a per-entry next-boot verdict plus TSUKUROI_BOOTCHAIN | `tools/boot-chain-audit.sh` live run wrote `.ufo/waves/round-17/l1-capture/audit-live.txt` (6 entries, CONSISTENT, exit 0); its selftest prints PASS total=45 failed=0 | round 17 |

## Round 32 measured outcome

Counting tools are the final declared bytes (C1 scorer v3 `f45136c3…` and C2 probe v2 `d43f95ed…`, both at `44c8eee5`), run through `tools/run-receipt.py`; every receipt header names the revision and tool digest. Before: `.ufo/waves/round-32/measure/c1-before-*` and `c2-before-*` and the base controls `controls/final/K0/`, `controls/final/H0/`. After at the integration commit `4ac5ebaa`: `measure/after-4ac5ebaa/`; final at `b8bf1507` (tools identical to `4ac5ebaa`): `measure/final-b8bf1507/`; record gates after the wave-2 repairs at `83b017c2`: `measure/final-83b017c2/`. Data seats were dispatched only after the control commits `462e40a7` (C1, 22:59:46-03:00) and `4e685163` (C2, 23:05:54-03:00); every counter change precedes them. The L1 integrated the three executor patches as full-file copies, unchanged.

| Claim | Before | After | Author verdict |
|---|---|---|---|
| C1 (adjacency) census HANDOFF ADJ-04 mori lines, predicate `routed` | base census (`controls/final/K0`): routed 8 of 24, live_consistent false, exit 1 | routed 24 of 24, live_consistent true, harness_errors 0, exit 0 at `4ac5ebaa` and at `b8bf1507`; reproduced by wave-2 RerunC1A on two seeds (one a replay) and cross-checked against independent `journalctl` counts by RerunC1B (no mismatch) | **not verified.** The declared target is met by the data, but a post-data shortcut control meets it too: wave-2 CritC1Shortcut's K11 (`.ufo/waves/round-32/controls/postdata/K11/K11-label-noise-floor.jsonl`) reads routed 24 of 24, live_consistent true, exit 0. K11 routes on the wrong statistics inside fixtures (C1_kernel for clusters, total errors for coredumps, keyed on `TSUKUROI_ROOT_DIR` and the tsukuroi-only `other=1` label) and on cached host constants outside them (clusters 2, errors minus 52). Under hyaku addendum §9 the count is therefore not adjacency evidence. Mistake R32-POSTDATA-SHORTCUT. No rule is changed after data |
| C2 (operability) child-environment allow-list, predicate `leaking` | 11 of 11 at `fe1ae02c` (`measure/c2-before-*`) and at `44c8eee5` (`controls/final/H0`) | 0 of 11, harness_errors empty, exit 0 at `4ac5ebaa` and `b8bf1507`; reproduced by wave-2 RerunC2Probe; round-31 probe still 0 of 33 (`final-b8bf1507/r31-probe-git-child-env.jsonl`, RerunR31Probe) | **target met.** Twelve per-tool reviewers found every spawn site on the allow-list and selftests or probe argv output identical at both revisions. Every pre-data control that skips the work reads 11 (H0, H1, H2, H3, H4) or 1 (H6); the positive control H5 (empty environment) reads 0. Limits: the probe never injects the names on its exclusion list (PATH, HOME, LANG, TZ, TMPDIR, USER, LOGNAME, TERM, SHELL, PWD, LC_*, XDG_*), so it cannot certify which allow-list was chosen (SentinelAllowKeep, CritC2Framing); `tools/_revision.py` `clean_env` and `mutants-owed-statements-r29-v4shapes.py` still copy the ambient environment (owed) |

Round admission (author's reading; the operator rules): every claim must verify; C1 does not, so the round is an honest stop. No axis is harmed at `83b017c2`: the census line shift that made `check-adjacency-anchors` fail at `b8bf1507` (IN-109 `found_line`, wave-2 RevGatesTip) was repaired, and the gate reads exit 0 (`measure/final-83b017c2/`); check-self-assessment moved from exit 1 at the base (K10) to exit 0; check-pause-gate stays at its base exit 1 (`GATE-PREMISE`, receipted at base); report-red-causes, registry-coverage and recheck-commands stay exit 0.

Errata to the round-32 axes table (wave-2 RevScorecardRecords; the table stays as appended): its preamble says `corpus/lessons/` gains the round-31 spot-check this round, but that file landed at the claim base `58cc2e0b`; the calibration row's "this round's C1 makes the lane's own table measurable" is round-31 text carried forward and describes no round-32 claim.

Ordinal record, round 32 (no ordinal moved): depth 8 → 8; coverage 9 → 9; operability 9 → 9; freshness 9 → 9; calibration 9 → 9; adjacency 8 → 8.

## Round 33 — declaration, attempt 1 (2026-10-23)

Claim base `1f521b93387590666bfbe7534708d8f416898424` (branch tip at dispatch, 04:45Z; the round-32 verifier spot-check). Ordinals at the base (`SCORECARD.md:1334`): depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest. Rounds 30 to 32 were rejected because a content-free or post-data shortcut met a counter (depth twice, adjacency once). Anti-loop shape for this round: one measured claim on a surface whose counter runs the claimed code and also reads its source (operability), one exploratory claim on the lowest axis (adjacency) with no counter, and the round-32 routed repairs, which are not claims.

| Claim | Axis (ordinal), surface changed | Before | Declared after-value | Counting command |
|---|---|---|---|---|
| C1 the child-process environment built by `tools/_revision.py` `clean_env()` (shared by the lane's revision-bound gates) and by `tools/mutants-owed-statements-r29-v4shapes.py` comes from an allow-list instead of a copy of the ambient environment minus `GIT_*` (round-32 spot-check routed defect 3) | operability 9 → 9; surface: the environment those two builders hand to every git child; the command that shows it unmoved is the probe itself | development run at the base: `leaking` 15 of 15 (5 targets × channels names, quiet, source), `harness_errors` empty, exit 1; the before receipt is issued through `tools/run-receipt.py` at the base with the probe bytes of this declaration commit | `leaking` 0 of `pairs` 15, `harness_errors` empty, exit 0 | `python3 tools/probe-child-env-allowlist-r33.py --revision <REV>` (default `--set claim`) → last line, fields `leaking`, `pairs`, `harness_errors`, `predicate_label` |
| C2 (exploratory) the kill and OOM classification boundary between this lane and mori, examined per class: for each kill or memory-pressure evidence class this lane's `SKILL.md` and census read, a sourced row of what tsukuroi retains, what goes to mori under ADJ-04, and mori's own declared scope quoted at a pinned mori revision | adjacency 8 → 8 (exploratory: verdict `unprovable-but-better` only with a named non-author reviewer on record; otherwise `unprovable`); surface: `PROVINCE.md` ADJ-04 (one trigger for every class today) gains a per-class boundary note | SHONEN box 4 (`SHONEN.md:12`) records "the kill and OOM classification boundary against SKILL.md:1078-1102 is unexamined"; mori's `PROVINCE.md:8-10` (mori `24603186`) declares "kill/OOM-related catalog-ID records ... cgroup `memory.events` ... memory pressure", the same evidence this lane's kill-event class table reads | a new note `corpus/knowledge/kill-oom-boundary-r33.md` and one appended ADJ-04 pointer in `PROVINCE.md`; no counting command (exploratory) | none (exploratory); supporting checks named below |

Frozen predicate C1, label `leaking` (the same sentence is the docstring's `FROZEN PREDICATE` and the constant `PREDICATE` of `tools/probe-child-env-allowlist-r33.py`, which asserts at import that the two are equal; every receipt's summary line carries `predicate_label` `leaking`): "A (target, channel) pair is leaking when, in its names or quiet run, any traced execve after the target's own first exec carries in its environment any name injected in that run or the exact ambient NAME=VALUE string of that run for any value-channel name (HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, LOGNAME, SHELL), or the run breaks parity with control run A (exit code, normalised stdout digest, count of successful git execs); or, in its source channel, the target's file or a tools/ module it imports at REV reads the ambient environment, starts a process that inherits it, names /proc/self/status, /proc/self/environ or TracerPid, or uses a construct that hides a read or spawn from the scan."

Targets (frozen, `CLAIM_TARGETS`): `tools/_revision.py --selftest`, `tools/check-adjacency-anchors.py --selftest`, `tools/check-boot-writers.py --selftest`, `tools/check-root-dac-correction.py --selftest` (the three tools whose selftest starts git through `clean_env()`), and `tools/mutants-owed-statements-r29-v4shapes.py --base <REV> --counter-rev <REV> --lane <clone>`. Selection was by harness viability at the base only: of fifteen candidates that reach `clean_env()` or the v4shapes builder, nine selftests start no git child and `check-appended-notices.py --selftest` exits 1 under the control environment (development runs under `/fast/scratch/hyaku/tsukuroi-r33-dev/`, to be committed as wave evidence). The probe was developed and run at the base only; no allow-list change exists anywhere when this declaration lands.

Why this counter is not met by a shortcut (hyaku addendum §9 and the 04:45Z leg lesson). Every run draws its injected names, its value-channel values, its run, HOME, TMPDIR and injection directory names and the scratch root name from `os.urandom`, so a filter keyed on a fixed name, value, path or label cannot pass both runs. The quiet run carries none of the four fixed names, so a rule keyed on `BASH_ENV` (or any fixed name) being present leaks there. The source channel reads the target bytes, so a rule keyed on being observed (a tracer check, a scratch-path check, a probe-name check) still fails while its ambient branch exists in the source; a target that hides such a branch from `ast` with a construct the list does not name escapes the source channel (named limit in the docstring). Shapes to be scored before any data step, under the frozen probe through `tools/run-receipt.py`, receipts committed before the claimed change is written: do-nothing (the base), junk (comment and whitespace bytes only), a deny-list extended by the four fixed names, a deny-list extended by the ten value-channel names, a rule keyed on `BASH_ENV` presence, a rule keyed on the tracer (`TracerPid`), a rule keyed on the scratch location, an inheriting spawn (`env=None`), a value-keyed filter (drop values under the scratch parent), a skip-work selftest that exits 0 early, plus an open adversarial search for any variant that keeps an ambient path for real runs and reads 0. If any control reads 0 of 15, C1 is re-designed before data or the round reports it; it cannot become exploratory (C2 holds the one exploratory slot).

Supporting checks for C2 (not a counter; the claim is judged by a non-author reviewer): wave 2 re-opens every quote in the note against its source and every mori pointer at the pinned mori revision, so a fabricated or off-topic source or pointer is caught; a critic attacks whether the note absorbs mori's scope instead of reporting it.

Sourced claims: C1's value channel rests on source rows opened this round in wave 1 (git's own configuration-file lookup through `HOME` and `XDG_CONFIG_HOME`, Python's `subprocess` `env` semantics, POSIX's environment-variable chapter); C2's rows rest on sources opened the same way (systemd-oomd, the kernel OOM-killer and PSI documentation, a userspace OOM daemon).

Separability: C1 changes only the two environment builders (plus the two `_revision.py` byte pins in `tools/check-pause-gate.py` and `tools/report-red-causes.py`, which must follow the new bytes); C2 adds one knowledge note and one `PROVINCE.md` append. The probe runs only the five targets; the C2 note is read by people, not by the probe.

Repairs that are not claims (round-32 spot-check section 5): defect 1, a census-handoff counter v4 that varies both counted classes in its live views and plants distractor errors in every fixture scenario, built in wave 1 and scored on the base census and on the round-32 shortcut K11 (repair evidence for the round-32 record only; the round-32 judgment is not re-opened); defect 2, the probe's value channel (above), with the round-32 regression set (`--set regression`) and the round-32 mutants m3 to m6 re-scored under it; defect 3 is C1; defect 4, an appended erratum to `.ufo/waves/round-32/controls/README.md`; defect 5, no data or counter-builder executor runs outside a validated wave this round: the L1 wrote the probe before wave 1 and writes the C1 change after the control receipts land; defect 6 items are named in the lesson with what was done or why not. No ordinal change is declared. No package transaction, service, module, sysctl, boot or filesystem write.

### Round 33 — pre-control amendment to the C1 probe's source channel (no control, data or seat has scored)

Before any seat was dispatched, the L1 found that the source channel as committed at `c2e69f3e` matched only the dotted names `os.environ` and the like, so `globals()['os'].environ`, `sys.modules['os']` or `getattr(m, 'env' + 'iron')` would hide an ambient read from it. The scan now flags any attribute named `environ`, `environb`, `getenv` or `getenvb` on any object, resolves import aliases, flags non-docstring strings containing `environ`, `getenv` or the tracer strings, and flags the indirect-lookup constructs listed in the probe docstring (`globals`, `locals`, `vars`, `dir`, `getattr` with a non-constant name, `__dict__`, `sys.modules`, `importlib`, `inspect` and others). The predicate sentence, target set, channels and declared after-value (`leaking` 0 of 15, exit 0) are unchanged; the before receipt is issued with the amended bytes. At the base the amended scan reports exactly one finding per target (`tools/_revision.py:63` for the four `_revision` users, `tools/mutants-owed-statements-r29-v4shapes.py:37`), and it reports none for the five round-32 regression targets that do not import `_revision`. A synthetic check (development only, `/fast/scratch/hyaku/tsukuroi-r33-dev/scan/`): an allow-list builder with `os.environ` only in a docstring reads no finding; `globals()['os']`, `sys.modules['os']`, `getattr(m, 'env' + 'iron')`, `from subprocess import run as r; r(['git'])`, `import os as o; o.environ`, `sp.Popen(..., env=None)` and the string `TracerPid` each read a finding. Known limit kept in the docstring: a hiding construct the list does not name escapes the source channel; the control wave's open adversarial search attacks that limit.

### Round 33 — attempt 2: pre-data amendment 2 to the C1 probe (before any attempt-2 seat, control or data step)

Attempt 1 (L1 `TsukuroiR33`) died with the orchestrator process at 05:25:25Z after landing `c2e69f3e` and `965bc5d9`. Its wave-1 seats (dispatched 05:05:58Z) wrote uncommitted files in the lane; attempt 2 (L1 `TsukuroiR33A2`, dispatched 05:26Z) treats them as untrusted scratch: all 170 untracked files were moved out of the lane into `/fast/scratch/hyaku/tsukuroi-r33-attempt1-scratch/untracked.tar` (sha256 `921ed24e…`) and none is cited. No claimed change and no data step exists yet.

Two gaps in the counter as committed at `965bc5d9`, both found before any attempt-2 control or data, are closed here. The claim, its targets, its channels, its label `leaking` and its after-value (`leaking` 0 of `pairs` 15, `harness_errors` empty, exit 0) are unchanged; the predicate sentence gains one clause.

1. Spawn side of an observation-keyed shortcut. A builder could keep an ambient path for ordinary runs and a clean one under the tracer if the inheriting spawn is hidden from the source scan: `getattr(subprocess, 'run')(...)`, a spawn function bound to another name, `env=None if <observed> else {...}`, an `env` name bound to None or to a parameter, a builder that returns None or falls off its end, `env=d.update(...)`, or an import of `asyncio`/`pty`/`multiprocessing` and similar. The source channel now requires every `subprocess` spawn's `env=` value to be a dict display, dict comprehension, `dict(...)`, a `|` of those, a name every binding of which is one of those, or a call of a function the scan reads (a def in the file or a name imported from a `tools/` module, including a `module.attr = function` rebinding) that ends in `return`/`raise` and never returns a value containing None; it flags any uncalled reference to a spawn function, `getattr` with a constant spawn name, a star import from a spawn module, positional spawn arguments, and seventeen more modules (docstring list). The read side is not closed and stays a named limit: a target that learns it is observed, or reads the ambient environment through a path assembled from fragments, with constructs the scan does not name.
2. Content-free builder. An empty environment drops the ambient copy and every setting the base builders hand to git. New clause, inserted after the value-channel clause: "or any traced git execve lacks GIT_CONFIG_NOSYSTEM=1 or GIT_CONFIG_GLOBAL=/dev/null". At the base every git child of the five targets carries both (279, 335, 203, 226, 1176 git children, 0 missing).

Frozen predicate C1 after amendment 2, label `leaking` (identical in the probe docstring's `FROZEN PREDICATE`, the constant `PREDICATE`, which the probe asserts at import, and every receipt's `predicate_label`): "A (target, channel) pair is leaking when, in its names or quiet run, any traced execve after the target's own first exec carries in its environment any name injected in that run or the exact ambient NAME=VALUE string of that run for any value-channel name (HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, LOGNAME, SHELL), or any traced git execve lacks GIT_CONFIG_NOSYSTEM=1 or GIT_CONFIG_GLOBAL=/dev/null, or the run breaks parity with control run A (exit code, normalised stdout digest, count of successful git execs); or, in its source channel, the target's file or a tools/ module it imports at REV reads the ambient environment, starts a process that inherits it, names /proc/self/status, /proc/self/environ or TracerPid, or uses a construct that hides a read or spawn from the scan."

Counting command (unchanged form): `python3 tools/run-receipt.py --revision <REV> --tool-revision <this commit> --out <file> -- tools/probe-child-env-allowlist-r33.py --revision '{rev}' --lane '{lane}'` → summary line fields `leaking`, `pairs`, `harness_errors`, `predicate_label`. L1 development runs of these bytes (not receipts): `.ufo/waves/round-33/l1/dev-a2/README.md` (base 15 of 15 before the kept clause; the empty builder is a harness error, exit 2; a minimal fixed builder in `_revision.py` reads 0 of 6 with the base git counts; the regression set at the base reads 5 of 33, all the source pair of a round-32 tool importing `_revision.py`).

Attempt-2 order: this commit; then one pre-data control wave (fresh seats; every control is a new design or a rescoring under these bytes, never a resend of an attempt-1 task) whose receipts the L1 commits; then the claimed change and its after receipt; then a falsify wave. C2 stays as declared (exploratory, adjacency). A control that meets the frozen target is reported as C1's failure; the counter is not changed after any attempt-2 control scores.

### Round 33 — attempt 3: start (before any attempt-3 seat)

Attempt 2 (L1 `TsukuroiR33A2`) died with the orchestrator process at 06:19:06Z after landing `9c89ff4f`. Its wave a2w1 left 247 uncommitted entries in the lane (the a2w1 spec, dispatch and seat outputs, and a census start file); attempt 3 (L1 `TsukuroiR33A3`, dispatched 06:40Z) treats them as untrusted scratch: they were moved out of the lane into `/fast/scratch/hyaku/tsukuroi-r33-attempt2-scratch/untracked.tar` (sha256 `ab282e1ce37634c5009e95dd7a85747eb6298254746f9d44d4bd8bd5161da489`) and none is cited. Its uncommitted erratum to `.ufo/waves/round-32/controls/README.md` was discarded and re-derived (commit times re-read with `git log -1 --format=%cI` for `462e40a7` and `4e685163`).

The counter is unchanged: probe bytes at `9c89ff4f` (sha256 `c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd`), predicate, label `leaking`, targets, channels and after-value (`leaking` 0 of `pairs` 15, `harness_errors` empty, exit 0) exactly as in amendment 2. The pre-data control wave a3w1 (spec `.ufo/waves/round-33/a3w1-spec.json`, committed with this note) scores fresh control designs under those bytes, including the declared open adversarial search (two seats: X01 read side, X02 spawn side); the L1 writes the claimed change only after the control receipts are committed. If any control that keeps an ambient path for real runs reads 0 of 15, the round reports C1 as not verified under the frozen rule.

## Axes — current self-assessment (round 33)

Appended 2026-10-23 by round 33. This table supersedes the round-32 table; the ordinals are unchanged (the round-33 measured outcome records no ordinal move). Counts that changed: `corpus/knowledge/` gains `kill-oom-boundary-r33.md` (52 to 53 notes, and it carries a `recheck:` line); `SKILL.md` gains the round33 registry table (2812 to 2870 lines, 628 to 678 table lines); `corpus/lessons/` gains `round-33.md` (40 stated at round 32 against 41 present at the round-33 base, now 42; the round-32 row's 40 was stale, base receipt `.ufo/waves/round-33/a3w1/ExecGateBaselines/base-check-self-assessment.jsonl`, K10). The round-32 calibration row's carried-forward sentence about a round-31 claim is dropped. Re-run `python3 tools/check-self-assessment.py --revision <REV>` before treating any count here as current.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 53 notes (`ls corpus/knowledge/*.md`, counted with `wc -l`); `SKILL.md` 2870 `wc -l`; 678 table lines (`grep -c '^[|]' SKILL.md`); `corpus/lessons/` (42 files) (counted with `find corpus/lessons -type f` and `wc -l`); rules added since round 12 cite `corpus/knowledge/*.md` notes, while four standing rules near the top of `SKILL.md` cite none. Ceiling: the depth ordinal was last moved at round 4, and no round from 12 to 24 changed it, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` 256 `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); the census has six planes, each with a landed note (the oom plane is a supporting measurement in `PROVINCE.md`, not a declared surface); the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry but have no census plane. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (101 cases, 101 passed, 0 failed) with exit 0; the live run exits 1 with a six-plane rollup; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes) stand; all 53 notes now carry a `recheck:` line, and the round-1 figure of 25 of 25 per-note rechecks is historical; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop for rounds 1 to 9; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |
