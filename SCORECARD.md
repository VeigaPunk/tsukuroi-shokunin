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

## Round 33 measured outcome

Counting tool: the frozen probe `tools/probe-child-env-allowlist-r33.py` at `9c89ff4f` (sha256 `c24f344b…`), run through `tools/run-receipt.py` with `--tool-revision 9c89ff4f`; every receipt header names the revision and tool digest. Order: control receipts committed at `4e521ce0` (07:17:29Z); the L1 wrote the change after them, landed at `c8fcfbf6` (07:18:06Z); the after receipt followed (`783d79e0`). C1 is sourced on S180: an explicit `env` mapping "used instead of the default behavior of inheriting the current process' environment" (CPython 3.14.8 `subprocess.rst:649-650`), so the landed dict is the whole child environment.

| Claim | Before | After | Author verdict |
|---|---|---|---|
| C1 (operability) `_revision.clean_env()` and v4shapes `ENV` are allow-lists, predicate `leaking` | 15 of 15, harness_errors empty, exit 1 at `9c89ff4f` (`.ufo/waves/round-33/a3w1/C01Before/before-claim.jsonl`; reproduced by wave-2 RerunBeforeIndependent) | 0 of 15, harness_errors empty, exit 0 at `c8fcfbf6` (`.ufo/waves/round-33/a3/after/c1-after-c8fcfbf6.jsonl`); reproduced by wave-2 RerunAfterA and RerunAfterB on fresh draws, git children 279/335/203/226/1176 and every target's stdout digest equal to the before | **target met; one declared control class unscored.** Every scored control that skips the work reads at least 3 of 15 or is a harness error (lesson `corpus/lessons/round-33.md`, section "Pre-data control wave"); the positive control C16 reads 0. Five wave-2 mutants of the landed builders (ambient HOME, one random ambient name, PATH copy, an ambient `**` spread, GIT_CONFIG_GLOBAL dropped) are all killed (12, 12, 12, 3 of 15; 6 of 12 plus a harness error). The declared open adversarial search did not run: both seats were refused by a provider safety filter (holds X01, X02). Wave-2 CritControlCoverage reads the probe's documented read-side limit as still open (a builder that learns it is traced through procfs, S181), with no meeting receipt either way. The counter was also amended (`9c89ff4f`) after attempt-1 seats had scored under `965bc5d9` (lesson R33-AMEND-AFTER-UNCOMMITTED-SCORES). Both questions are the operator's to rule |
| C2 (adjacency, exploratory) per-class kill/OOM boundary note | ADJ-04 names one trigger for all classes; `SHONEN.md` box 4 records the boundary as unexamined | `corpus/knowledge/kill-oom-boundary-r33.md`: 7 class-table rows (every pointer re-opened by wave-2 QB1 to QB7, no fabricated or misaimed pointer), 4 rows for census-read classes added after CritC2Gaps, a routing reading, S182; `PROVINCE.md` append | exploratory; verdict from the named non-author reviewer in the residual call (`.ufo/waves/round-33/a3res/JudgeC2Exploratory.md`) |

No-harm at the tip `eb388c9c` (`.ufo/waves/round-33/a3/gates-eb388c9c24462ab7a5ed01604318117c101a25b3/`), compared with the base receipts at `9c89ff4f` (`.ufo/waves/round-33/a3w1/ExecGateBaselines/`): check-self-assessment 1 → 0; check-registry-coverage 1 → 0; check-pause-gate 1 → 1, the same `GATE-PREMISE P3` finding; report-red-causes 0 → 0; check-recheck-commands 0 → 0; check-adjacency-anchors 0 → 0. All 25 `_revision`-importing selftests are byte-identical to base at `f761fade` (wave-2 SelftestsAfterNoHarm). Two harms appeared at `f761fade` (wave-2 GatesAfterNoHarm) and were repaired before the tip at `3846bd1a`. First, IN-101's quoted expression was removed by C1, so the anchor is now `UNRESOLVABLE`. Second, the C2 note had no `recheck:` line, so one was added.

Ordinal record, round 33 (no ordinal moved): depth 8 → 8; coverage 9 → 9; operability 9 → 9; freshness 9 → 9; calibration 9 → 9; adjacency 8 → 8.

C2 verdict (residual call, named non-author reviewer JudgeC2Exploratory, `.ufo/waves/round-33/a3res/JudgeC2Exploratory.md`): `unprovable-but-better`. Before this round, ADJ-04 had one trigger for every class and the boundary was unexamined; the note now separates overlap, shared surfaces, gaps and the classes that feed the one prepared packet. Three wording corrections that CritC2AddedRows found after the ruling are owed; the judged note is not edited. Routed defect 1 stays open: MutR1CounterV4 passed the repair counter's fixtures and synthetic views with a label-keyed census (lesson R33-FIXTURE-LABEL-SHORTCUT).

### Round 33 — correction to amendment 2 (appended in round 34; round-33 spot-check routed defect 5)

Amendment 2 (`9c89ff4f`, 05:46:01Z) says its two gaps were "found before any attempt-2 control or data". That sentence is true of attempt 2 only and leaves out attempt 1. Attempt-1 seats had already scored under the amendment-1 bytes `965bc5d9` (probe sha256 `38a40583…`): the quarantine archive `/fast/scratch/hyaku/tsukuroi-r33-attempt1-scratch/untracked.tar` (sha256 `921ed24e…`) holds 54 `.jsonl` receipts written 05:06–05:23Z (02:06–02:23 -03:00), among them `w1/CtlOpenSearchRun` (2), `w1/CtlH9SkipWork` and `w1/CtlH7Inherit` (names and times from `tar tvf`). None of them reached the target: the round-33 closure read them untrusted with `tar xOf … | jq` and found no control at 0 leaking or exit 0; the only zero reads were three probe mutants run on mutated probe bytes (`corpus/lessons/round-33-verifier-spotcheck.md` §2, Ruling 1). The amendment only added conditions. The original text above stays as written.

## Round 34 — declaration (2026-10-23, before any seat)

Claim base `2641591e303057cd0f67e190a6bdf7fa91a45c31` (branch tip at dispatch; the round-33 verifier spot-check). Ordinals at the base (`SCORECARD.md:1408`): depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest; saturation 9, so the stagnation nudge does not apply. Round 33 was rejected (`rejected-harmed`) only because its C2 note lacked `source:` and `verified-at:`; its routed repairs come first (below) and are not claims. Shape: one measured claim on operability whose counter is the round-33 probe with a new frozen target set, and one exploratory claim on the lowest axis (depth).

| Claim | Axis (ordinal), surface changed | Before | Declared after-value | Counting command |
|---|---|---|---|---|
| C1 the git child environment of the nine harness-viable lane tools that still build it as a copy of the ambient environment minus `GIT_*` becomes a fixed allow-list | operability 9 → 9; surface: the environment those nine tools hand to their children (`check-boot-chain`, `check-btrfs-repair-r31`, `check-btrfs-space-r30`, `check-locator-clarification`, `check-recheck-commands`, `check-section-citations`, `check-seat-scope`, `check-source-scope-correction`, `measure-update-recheck`); the command that shows it unmoved is the probe itself | L1 development runs of the target set at the base (pre-freeze bytes, not receipts; `.ufo/waves/round-34/l1/dev-base/`): every one of the 27 pairs leaking; the before receipt is wave-1 seat C01Before's | `leaking` 0 of `pairs` 27, `harness_errors` empty, exit 0 | `python3 tools/run-receipt.py --revision <REV> --tool-revision <this commit> --out <file> -- tools/probe-child-env-allowlist-r34.py --revision '{rev}' --lane '{lane}'` → summary fields `leaking`, `pairs`, `harness_errors`, `predicate_label` |
| C2 (exploratory) what the census journal arm's `coredump=` count and the ADJ-04 `class=coredumps value=<m>` handoff value count, against systemd v262's own coredump logging | depth 8 → 8 (exploratory: `unprovable-but-better` only with a named non-author reviewer on record, otherwise `unprovable`); surface: a new knowledge note on the counting unit of an existing census arm, plus an appended `SKILL.md` reading rule; the census code is not changed this round | the census comment `tools/tsukuroi-census.sh:263-267` says "the `systemd-coredump` entry class IS the storm signal", and `SKILL.md` snapshot lines (for example `:541`, `:884`) read `coredump=N` as a number of coredumps; no note says what one counted entry is | a note `corpus/knowledge/coredump-count-unit-r34.md` with the `source:`/`verified-at:`/`recheck:` trio, sourced rows on what systemd-coredump logs per crash, and a dated boot-0 reconciliation of counted entries by message kind | none (exploratory) |

Frozen predicate C1, label `leaking`, the same sentence as round 33 (the constant `PREDICATE` of `tools/probe-child-env-allowlist-r34.py`, asserted at import against the docstring, and every receipt's `predicate_label`): "A (target, channel) pair is leaking when, in its names or quiet run, any traced execve after the target's own first exec carries in its environment any name injected in that run or the exact ambient NAME=VALUE string of that run for any value-channel name (HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, LOGNAME, SHELL), or any traced git execve lacks GIT_CONFIG_NOSYSTEM=1 or GIT_CONFIG_GLOBAL=/dev/null, or the run breaks parity with control run A (exit code, normalised stdout digest, count of successful git execs); or, in its source channel, the target's file or a tools/ module it imports at REV reads the ambient environment, starts a process that inherits it, names /proc/self/status, /proc/self/environ or TracerPid, or uses a construct that hides a read or spawn from the scan."

Counter: `tools/probe-child-env-allowlist-r34.py` at this declaration commit. It is the round-33 probe at `9c89ff4f` with only the docstring header, usage line, VERSION and target sets changed (`diff tools/probe-child-env-allowlist-r33.py tools/probe-child-env-allowlist-r34.py` prints only those lines). Target selection was by a full sweep of `tools/*.py` at the base for the ambient-copy builder (13 files), then harness viability at the base; the four exclusions and their reasons are in the probe docstring. Round-33 routed defect 7 named four of the thirteen.

Pre-data controls (wave 1; the hyaku 01:05Z rule). Each control is one sandbox variant of the nine targets at this commit, scored once with the frozen probe through `run-receipt.py` and committed before the claimed change exists: C01 do-nothing (the before receipt), C02 junk bytes, C03 allow-list label only, C04 deny the four fixed injected names, C05 deny the value-channel names, C06 deny a host-snapshot name list, C07 argv-keyed, C08 scratch-location-keyed, C09 `BASH_ENV`-keyed, C10 tracer-keyed written plainly, C11 inherit (no `env=`), C12 skip the work, C13 content-free empty environment, C14 keyed on the probe's fixture file names (`bashenv.sh`, `env.sh`, `gconv`), C15 half fix (four of nine tools), C17 value-keyed filter, C18 git started through `/bin/git` with the ambient copy kept, and the positive control C16 (the claimed work in a sandbox).

Kill rule (fixed now): if at any point this round a variant that keeps an ambient path in an ordinary untraced run reads `leaking` 0 of 27 with `harness_errors` empty and exit 0 under the frozen probe, C1 is reported not verified. The probe and predicate are not changed after any seat scores. Named limit, carried from round 33 and not built: the read side is open (a target that learns through procfs that it is traced and reads its initial environment there, S181). Round-33 routed defect 4 is scored before the change: three read-only code-reading items each take one rule family of the source and run channels (ambient reads; spawns and `env=` shapes; run-channel carriers, `is_git` and parity normalisation) and list every construct class those rules do not flag, with a one-line example and whether it falls inside the named limit. The count of classes outside the named limit is recorded before the change; each such class is a wave-2 build item against the after bytes, under the kill rule.

Supporting checks for C2 (not a counter): wave 2 re-opens every quote in the note against its saved source, re-runs the boot-0 reconciliation command, and a critic attacks whether the note absorbs mori's coredump classification (OUT-005: mori owns signal-11 coredump classification) instead of explaining this lane's own counting unit.

Sourced claim: C2 rests on source rows opened in wave 1 (systemd v262 coredump source code for its per-crash journal messages, `coredump.conf(5)`, and `journalctl(1)` JSON output for fields it prints as null). S177 (systemd-coredump(5), round 32) is re-opened, not re-registered.

Separability: C1 changes only the nine tools' child-environment builders (and any `_revision.py` byte pins that must follow, none expected because `_revision.py` is not changed); C2 adds one note and a `SKILL.md` append and changes no tool. The probe never reads the note.

Repairs that are not claims (round-33 spot-check §5): (1) QUALITY 8: `source:` and `verified-at:` lines for `corpus/knowledge/kill-oom-boundary-r33.md`, and a gate that fails a knowledge note missing any of the trio, shown red at the base before the fix; (2) the three C2 wording corrections appended to that note; (3) R33-FIXTURE-LABEL-SHORTCUT: a v5 census-handoff counter with distractors that share no label, one synthetic view with the override variable unset and a live view that tolerates journal growth, scored on the round-32 tip census and on the MutR1CounterV4 variant; (4) the open search as code-reading items (above); (5) the amendment-2 correction (appended above); (6) committed digests and a regeneration command for the five round-33 diffs that live only on scratch; (7) carried: C1 covers nine of the thirteen ambient copies; the other four and the rest of the carried list stay owed and are named in the lesson.

Order: this commit; wave 1 (controls, code reading, repairs, C2 sources and host reconciliation, baselines); the L1 commits every control receipt; then the claimed change, its after receipt and the C2 note; then wave 2 (falsify); then the measured outcome, lesson and report.

### Round 34 — pre-data amendment 1 to the C1 counter (2026-10-23 08:52Z; no claimed change and no data step exists)

Wave-1 critic CritC1AxisFit (`.ufo/waves/round-34/w1/CritC1AxisFit.md` finding 3, delivered about 08:47Z) found a control the declared list did not cover and the declaration bytes cannot refuse: replace each target's real work with one `git --version` under a clean fixed environment and a fixed success line. The probe takes control runs A and B from the candidate itself, so such a target sets its own baseline and reads 0 of 27. The L1 built that dummy in its own scratch clone (`b3242da6…`, development, not a receipt) and confirmed the gap's mechanism by reading `parity()`. Under the hyaku 01:05Z rule a claim whose counter a control meets is re-designed before data; this is that re-design.

The amendment adds one clause and changes nothing else: "or control run A breaks base parity with the same target's control run at the claim base (exit code, normalised stdout digest, count of successful git execs, multiset of normalised git argv)". The probe now also runs each target's bytes at the claim base `2641591e` with the same arguments (`--base`, default `CLAIM_BASE`). The label stays `leaking`; targets, channels and the after-value (`leaking` 0 of `pairs` 27, `harness_errors` empty, exit 0) are unchanged. New probe bytes: sha256 `5231dbafc472ff42e041cbaad3f48dd8bd204d58b6ab22e497cf9372b23d6bfd` (VERSION 5), the tool revision of every receipt from here on.

Frozen predicate C1 after amendment 1, label `leaking` (identical in the probe docstring, the constant `PREDICATE` and every receipt's `predicate_label`): "A (target, channel) pair is leaking when, in its names or quiet run, any traced execve after the target's own first exec carries in its environment any name injected in that run or the exact ambient NAME=VALUE string of that run for any value-channel name (HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, LOGNAME, SHELL), or any traced git execve lacks GIT_CONFIG_NOSYSTEM=1 or GIT_CONFIG_GLOBAL=/dev/null, or the run breaks parity with control run A (exit code, normalised stdout digest, count of successful git execs), or control run A breaks base parity with the same target's control run at the claim base (exit code, normalised stdout digest, count of successful git execs, multiset of normalised git argv); or, in its source channel, the target's file or a tools/ module it imports at REV reads the ambient environment, starts a process that inherits it, names /proc/self/status, /proc/self/environ or TracerPid, or uses a construct that hides a read or spawn from the scan."

Disclosure of what had scored before this commit, all under the declaration bytes `35a87374…` (tool revision `6de666c4`): C01Before 27 of 27 (exit 1), C02JunkBytes 27, C03LabelOnlyAllowlist 27, C04DenyInjectFixed 27, C05DenyValueNames 27, C09BashEnvKeyed 21, C10TracerPlain 15, C11InheritNoEnv 21 of 21 plus 2 harness errors, C12SkipWorkSelftest 9 harness errors (exit 2), C13ContentFreeEmptyEnv 15 of 18 plus 3 harness errors, C15HalfFix 16, C17ValueKeyedFilter 27 (all exit 1 unless stated), and the no-harm sets r33claim 0 of 15 and regression 0 of 33; controls C06, C07, C08, C14, C16 and C18 were still running and also score under the declaration bytes. None of them met the after-value. The clause only adds a way for a pair to leak, so every one of these reads at least as high under the amended bytes; the amendment makes the counter harder to meet and cannot rescue any scored control. L1 development runs of the amended bytes (`.ufo/waves/round-34/l1/dev-amend/`, not receipts): the claimed change as drafted in the L1's scratch clone (`e1bec241…`) 0 of 27 with every base-parity list empty; the declaration commit 27 of 27 with every base-parity list empty (the normalisation is stable on unchanged bytes); the dummy 18 of 27 (base parity fires on names and quiet for all nine).

Before the claimed change lands, a residual pre-data control call scores under the amended bytes: the do-nothing before receipt, the dummy under both byte sets, a replay dummy that prints each target's claim-base stdout and makes the same number of `git --version` calls, the positive control, and a re-score of two earlier cheapest controls. The kill rule stands as declared and also covers the dummy and replay: if either reads 0 of 27 under the amended bytes, C1 is reported not verified.

### Round 34 — pre-data amendment 2 to the C1 counter (2026-10-23 ~09:10Z; still no claimed change and no data step)

The declared code-reading items (round-33 routed defect 4) returned before the change: ReadRunChannels names 9 run-channel classes outside the named limit and ReadScanAmbientReads 4 source-channel classes (`.ufo/waves/round-34/w1/ReadRunChannels.md`, `ReadScanAmbientReads.md`; ReadScanSpawnShapes still running). Two of them combine into a builder that keeps an ambient path in ordinary runs and reads 0 under the amendment-1 bytes: an ambient value passed under a new name, read through a stdlib wrapper the source scan does not flag (for example `os.path.expanduser('~')`), and likewise a mutated value-channel value. A spawn through `execveat` and an environment string too long to parse also left no record. Under the declared kill rule each of these would end C1, so the counter is re-designed before data rather than left to fail.

Amendment 2 adds two clauses to the run channels and changes nothing else: a child environment string, under any name, whose value equals the run's TMPDIR or contains another run-unique ambient value of that run (HOME, XDG_CONFIG_HOME and injection-directory paths, the LANG/TZ/TERM/USER/LOGNAME/SHELL words, the injected values); and any `execveat` call or unparseable `execve` record. strace now traces `execve,execveat`. Label, targets, channels and after-value (`leaking` 0 of `pairs` 27, `harness_errors` empty, exit 0) are unchanged. New probe bytes: VERSION 6, sha256 `5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92`, the tool revision of every receipt from this commit on.

Frozen predicate C1 after amendment 2, label `leaking` (identical in the probe docstring, the constant `PREDICATE` and every receipt's `predicate_label`): "A (target, channel) pair is leaking when, in its names or quiet run, any traced execve after the target's own first exec carries in its environment any name injected in that run or the exact ambient NAME=VALUE string of that run for any value-channel name (HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, LOGNAME, SHELL), or carries under any name a value equal to that run's TMPDIR or containing any other run-unique ambient value of that run (its HOME, XDG_CONFIG_HOME and injection-directory paths, its LANG, TZ, TERM, USER, LOGNAME and SHELL words, and its injected values), or the run makes any execveat call or has an execve record the probe cannot parse, or any traced git execve lacks GIT_CONFIG_NOSYSTEM=1 or GIT_CONFIG_GLOBAL=/dev/null, or the run breaks parity with control run A (exit code, normalised stdout digest, count of successful git execs), or control run A breaks base parity with the same target's control run at the claim base (exit code, normalised stdout digest, count of successful git execs, multiset of normalised git argv); or, in its source channel, the target's file or a tools/ module it imports at REV reads the ambient environment, starts a process that inherits it, names /proc/self/status, /proc/self/environ or TracerPid, or uses a construct that hides a read or spawn from the scan."

Scored before this commit under the amendment-1 bytes `5231dbaf…` (residual call `res`, `.ufo/waves/round-34/res/`): R0BeforeAmended 27 of 27 (exit 1, every base-parity list empty); R1DummyBothBytes 0 of 27 under the declaration bytes (it MEETS them, the gap amendment 1 closed) and 18 of 27 under the amendment-1 bytes; R2ReplayDummy (each target prints its claim-base stdout and makes as many `git --version` calls) 18 of 27, stopped only by the git-argv multiset of base parity; R3PositiveAmended 0 of 27 (exit 0; all nine own modes exit 0, only the two btrfs self-hashes differ); R4RescoreCheapest junk 27 and label 27 (no pair stopped leaking). R5ReviewAmendment was still running. Both new clauses only add ways to leak, so no pair that leaked under earlier bytes stops leaking and no scored control can reach 0 under these bytes. L1 development runs of the amendment-2 bytes (`.ufo/waves/round-34/l1/dev-amend2/`): drafted change 0 of 27; declaration commit 27 of 27; dummy 18 of 27; drafted change plus `ZZ_KEY=os.path.expanduser("~")` in boot-chain 3 of 27, caught on names and quiet only by the new any-name clause.

Kill-rule reading, fixed now and not changed later: "keeps an ambient path" means that an ambient environment name or value reaches a child process's environment in an ordinary, untraced run. Passing ambient data through argv, a file, a pipe or a fork without exec is outside this claim, which is about child environments; the named limit stays the S181 read side (a target that learns it is traced). Wave 2 builds the remaining classes the code reading named against the after bytes, under this kill rule.

### Round 34 — correction to the amendment-1 disclosure (appended; residual reviewer R5ReviewAmendment finding 1)

The amendment-1 text lists C07, C08 and C14 among controls "still running". They had already scored under the declaration bytes before the amendment commit (`15c9ac0e`, 08:51:51Z) and their receipts are in that commit: C07ArgvKeyed 15 of 27 (finished 08:47:53Z), C08ScratchLocationKeyed 15 of 27 (08:46:48Z), C14FixtureNameKeyed 21 of 27 (08:47:48Z), all exit 1, none at the after-value. The controls that were still running then and scored later under the declaration bytes: C06HostSnapshotNames 24 of 24 plus one harness error (exit 2), C16PositiveAllowlist 6 of 27 (the seat's own allow-list edit left the four flagged constructs and one Python re-exec), C18GitPathAlias 21 of 21 plus two harness errors (exit 2). R5 also notes (finding 2) that the base-parity clause can turn a target into a harness error, which lowers the summary `leaking` count while raising the exit code; per pair it only adds evidence. The original text stays as written.

## Round 34 measured outcome

Counter: `tools/probe-child-env-allowlist-r34.py` VERSION 6 at `3457f287` (sha256 `5d0d5689…`), through `run-receipt.py --tool-revision 3457f287`. Order: declaration `6de666c4`; wave-1 controls (all under the declaration bytes, none at the target); amendment 1 `15c9ac0e`; residual controls; amendment 2 `3457f287`; the change `df661507`; after receipt.

| Claim | Before | After | Author verdict |
|---|---|---|---|
| C1 (operability) nine tools' child environments become fixed allow-lists, label `leaking` | 27 of 27, exit 1 at `3457f287` (`.ufo/waves/round-34/after/c1-before-a2-3457f287.jsonl`; wave-2 RerunBeforeIndependent reproduces it at `6de666c4`) | 0 of 27, harness_errors empty, exit 0 at `df661507` (`.ufo/waves/round-34/after/c1-after-df661507.jsonl`; RerunAfterA and RerunAfterB reproduce 0 of 27 on fresh draws) | **not verified under the declared kill rule.** Two wave-2 after-mutants keep an ambient path that reaches a child in an ordinary untraced run and still read 0 of 27, harness_errors empty, exit 0: MutAttrgetterCopy (ambient copy read through `operator.attrgetter` of a composed name; `.ufo/waves/round-34/w2/MutAttrgetterCopy.md`) and MutPathCopy (PATH taken from `os.get_exec_path()`; `MutPathCopy.md`). The counter is not amended after data; this is an honest stop. Killed: MutMutatedValue 2, MutPythonReexecInherit 3, MutOneTargetSkipWork 2 (others listed in the lesson) |
| C2 (depth, exploratory) census coredump counting unit | no entry said what one counted entry is beyond "entries by identifier" (`kill-oom-boundary-r33.md` coredump row; `journal-boot-plane.md` §2.2) | `corpus/knowledge/coredump-count-unit-r34.md` (S186-S189, dated reconciliation 1621 = 183 + 69 + 1365 + 4) with wave-2 corrections appended | exploratory; awaits the named non-author reviewer (the closure). Wave-2 CritC2Depth: "adds genuine depth" with eight wording defects, corrected in the note's appended section |

The after value itself stands as a measurement (0 of 27, three independent receipts); what fails is the declared condition that no ambient-keeping variant reads 0. Ordinal record, round 34 (no ordinal moved): depth 8 → 8; coverage 9 → 9; operability 9 → 9; freshness 9 → 9; calibration 9 → 9; adjacency 8 → 8.

Declaration erratum (wave-1 RevProbeR34Diff, wave-2 ScoutRemainingAmbient): the declaration's "a full sweep finds thirteen" ambient-copy files is wrong; the selection sweep was cut by `head -40`. At the base the `os.environ.items()` copy form appears in nineteen `tools/*.py` files; eleven non-target builders remain at the tip. The nine claim targets are unaffected.

Kill-rule reading (wave-2 CritKillRuleReading): ReadRunChannels reported fork-without-exec at 08:50:37Z, before amendment 2 (09:04:36Z) excluded it. The L1's reason: a forked child that never execs is a copy of the target process, whose own environment is ambient by construction and excluded from every clause. The critic judges that exclusion a narrowing; it is recorded, and it does not affect the verdict above, which fails on two in-scope mutants.

## Axes — current self-assessment (round 34)

Appended 2026-10-23 by round 34; supersedes the round-33 table. Ordinals unchanged. Counts that changed: 54 notes (`coredump-count-unit-r34.md`), `SKILL.md` 2942 lines and 730 table lines (round-34 reading rule and round34 registry), 44 lesson files (`round-33-verifier-spotcheck.md`, `round-34.md`).

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 54 notes (`ls corpus/knowledge/*.md`, counted with `wc -l`); `SKILL.md` 2942 `wc -l`; 730 table lines (`grep -c '^[|]' SKILL.md`); `corpus/lessons/` (44 files) (counted with `find corpus/lessons -type f` and `wc -l`); rules added since round 12 cite `corpus/knowledge/*.md` notes, while four standing rules near the top of `SKILL.md` cite none. Ceiling: the depth ordinal was last moved at round 4, and no round from 12 to 24 changed it, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` 256 `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); the census has six planes, each with a landed note (the oom plane is a supporting measurement in `PROVINCE.md`, not a declared surface); the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry but have no census plane. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (101 cases, 101 passed, 0 failed) with exit 0; the live run exits 1 with a six-plane rollup; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes) stand; all 54 notes now carry a `recheck:` line, and the round-1 figure of 25 of 25 per-note rechecks is historical; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop for rounds 1 to 9; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |

## Round 35 — declaration, pre-freeze candidate (2026-10-23, before any seat)

Claim base `b40c01df38eb26f74c095c471efc6d1649b00fd4` (branch tip at dispatch; the round-34 verifier spot-check). Ordinals at the base (`SCORECARD.md:1480`): depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest; saturation 9, so the stagnation nudge does not apply. Rounds 33 and 34 were rejected; both worked the child-environment probes (`tools/probe-child-env-allowlist-r3*.py`). This round's measured claim moves a different surface with a different counter shape (fixture oracle, not a tracer), and the probe work is a routed repair, not a claim.

| Claim | Axis (ordinal), surface changed | Before | Declared after-value | Counting command |
|---|---|---|---|---|
| C1 the census gains a pacnew/pacsave drift arm: one `DRIFT pacnew-plane` line that pairs the readable `/etc` sweep with `pacman.log` and reports skipped unreadable directories (the `PROVINCE.md:21` boundary of the `.pacnew` / `.pacsave` drift surface, which has a knowledge entry but no census plane, `SCORECARD.md:1493` coverage row) | coverage 9 → 9; surface: `tools/tsukuroi-census.sh` gains the arm and its `TSUKUROI_ETC_DIR` seam; the command that shows it unmoved is the counter itself (no `DRIFT pacnew-plane` line: 0 of 24) | label `matches` 0 of 24 at the base (L1 development run, 2026-10-23 10:51Z, not a receipt; the before receipt is wave-1 seat K01DoNothing's) | `matches` 24 of `of` 24, `harness_errors` empty, exit 0, on a fresh seed, at the change commit | `python3 tools/run-receipt.py --revision <REV> --tool-revision <FREEZE> --out <receipt> -- tools/score-pacnew-arm-r35.py --lane '{lane}' --revision '{rev}'` (no `--seed`: the seed is drawn from `os.urandom` and printed in the receipt header) |
| C2 (exploratory) how pacman 7.1 itself creates and logs `.pacnew` and `.pacsave` files: the backup-file hash cases, `NoUpgrade`, removal saves, the unlogged `.pacsave.N` shift, and which of pacdiff's search names pacman no longer makes | depth 8 → 8 (exploratory: `unprovable-but-better` only with a named non-author reviewer on record, otherwise `unprovable`); surface: a new knowledge note plus an appended `SKILL.md` reading rule; no tool changes | `corpus/knowledge/pacnew-plane.md` says where to find the files and that the log is history; no entry says when pacman makes which file, which events it logs, or why a current file can have no log line | a note `corpus/knowledge/pacman-backup-files-r35.md` with `source:`, `verified-at:`, `recheck:` and located quotes from source rows opened this round | none (exploratory) |

Frozen predicate C1 (to be frozen; label `matches`; the same sentence is the constant `PREDICATE` of `tools/score-pacnew-arm-r35.py` and every receipt's `predicate_label`): "A fixture matches when the census at the named revision, run with TSUKUROI_ETC_DIR set to the fixture's etc tree and TSUKUROI_PACMAN_LOG to its log, exits 0, 1 or 2 within 120 s, prints exactly one line that begins `DRIFT pacnew-plane ` whose fields pacnew, pacsave, pacorig, unreadable, log_pacnew, log_pacsave, unlogged and gone each appear once as name=integer and all equal the oracle's values for that fixture, and leaves the fixture's etc tree and log unchanged (bytes, modes and inode change times)."

Counter: `tools/score-pacnew-arm-r35.py` VERSION 1 at this commit. Each run draws a fresh seed and builds 24 fixtures: a random `etc` tree with counted names (`*.pacnew`, `*.pacsave`, `*.pacsave.[0-9]*`, `*.pacorig`, some as symlinks), distractor names (`.pacnew.bak`, `.pacnewer`, `.pacsave~`, `.pacsave.x1` and others), directories with counted-looking names, 0 to 3 unreadable directories (mode 000 or 300) holding a counted-looking file, and a log with pacman's own warning lines (paired, repeated, gone, beneath an unreadable directory) plus distractor lines (`[ALPM-SCRIPTLET]`, non-`/etc` targets, mismatched pairs, `installed as<name>` package lines). Every fixture holds at least one `.pacnew` and one logged `.pacnew` event. The oracle's values exist only in the counter process; no fixture or harness path carries a label. Every probe command seam points at an empty-output stub and every host-path seam at an empty harness directory, so a fixture run reads no host state. The oracle's definitions and their sources are in the counter docstring; the source rows are opened in wave 1.

Freeze rule (round-34 spot-check §5 item 3; written before any seat scores): the counter is frozen at the freeze commit, whose counter bytes must equal the bytes the pre-freeze control wave scored (sha256 in every control receipt). The hyaku 01:05Z pre-data re-design exception is the only way the counter can change: if any control meets the after-value, the counter is re-designed before the freeze, and every control is scored again on the new bytes before the freeze. After the freeze commit the counter, predicate, label, fixture count and after-value do not change.

Kill rule (fixed now): if, after the freeze, any variant of the census that skips part of the claimed work (a field it does not compute from the fixture, a reader it does not run, a value keyed on anything but the fixture's tree and log) reads 24 of 24 with `harness_errors` empty and exit 0 under the frozen counter, C1 is reported not verified.

Pre-freeze controls (wave 1; each a sandbox variant of the census at this commit, scored once with this counter through `run-receipt.py`, receipts committed before the freeze): K01 do-nothing (the before receipt), K02 junk bytes, K03 all-zero line, K04 constant line (the live host's values), K05 log reader only, K06 filesystem reader only, K07 naive `*.pac*` count, K08 keyed on fixture names and shapes, K09 harness snooping (parent process, environment, temp tree, seed recovery), K10 live `/etc` instead of the seam, K11 counts without pairing, K12 `find -type f` (symlinks dropped), K13 pacdiff's exact find expression (directories counted), K14 positive control (a real arm; its patch is the candidate change), K15 one-field mutants of K14 (each field off by one, a duplicate line, a dropped field), K16 an arm that chmods unreadable directories and restores them.

Sourced claim: C1's oracle and C2's note rest on rows opened in wave 1: pacman 7.1.0 `lib/libalpm/add.c` and `remove.c` at the installed commit `54d9411` (`pacman -Q pacman` reads `7.1.0.r9.g54d9411-3`), pacman-contrib 1.13.1 `src/pacdiff.sh.in`, and pacman's own `doc/pacman.8.asciidoc` and `doc/pacman.conf.5.asciidoc` at `54d9411`.

Separability: C1 changes only `tools/tsukuroi-census.sh` (the arm, its seam, its usage text and selftest cases); C2 adds one note and a `SKILL.md` append and changes no tool. The counter never reads the note.

Repairs that are not claims (round-34 spot-check §5): (1) and (2) the child-environment probe: a successor `tools/probe-child-env-allowlist-r35.py` with an untraced view of child environments, scored against the committed MutAttrgetterCopy and MutPathCopy mutants (each must read above 0) and on the r33claim, regression and round-34 target sets at this base (each must read 0), with normalisation fixes for short hashes, fixture paths and `GIT_CEILING_DIRECTORIES`/`$HOME`-derived values; it is not frozen and backs no claim this round; (3) freeze wording (above), the amendment-1 disclosure correction and the fork-without-exec limit; (4) the unreceipted gate line; (5) evidence timestamps; (6) hold and late-evidence accounting; (7) the 22 leftovers, landed with `.ufo/waves/round-34/w2/UNINTEGRATED-AT-FILING.md`; (8) the coredump note remnants; (9) ambient copies outside the round-34 claim (`check-revision-binding.py`, `probe-git-env-leak.py` and the eleven non-target `os.environ.items()` builders).

Order: this commit; wave 1 (controls, positive control, sources, recon, baselines, repairs); the L1 commits every control receipt; the freeze commit; then the change and its after receipt and the C2 note; then wave 2 (falsify); then the measured outcome, lesson and report.

### Round 35 — the C1 counter VERSION 1 is met by a pre-freeze control; redesign before data (2026-10-23, before any freeze and before the claimed change)

Wave-1 control K08FixtureKeyed met VERSION 1 (`tools/score-pacnew-arm-r35.py`, sha256 `19d25d14…`, at `6b4561e4`): `matches` 24 of 24, `harness_errors` empty, exit 0, with a census variant that never pairs the log with the tree and never tests readability, keyed on name lengths (the generator gave gone targets and unreadable directories seven-character names and every other name six; `.ufo/waves/round-35/w1/K08FixtureKeyed.md` finding 2, receipt `K08FixtureKeyed/variant.jsonl`). K15FieldMutants also met it with a log reader that does not check that the warning's two paths pair (`K15FieldMutants.md`). CritClaimDesign (findings 2, 3, 4, 10) and the lane's own QUALITY 82 and 73 add that VERSION 1 has no view the census cannot tell from a fixture, no committed should-fail battery as its measure, and a log-count scope (non-`/etc` events counted) that the declaration called a distractor. Under the hyaku 01:05Z rule a claim whose counter a control meets is re-designed before data; no freeze commit exists and the claimed change does not exist.

VERSION 1 is therefore not C1's counter and is not changed: its bytes and every wave-1 receipt stay committed as evidence of a failed candidate. The candidate counter for C1 is a new file, `tools/score-pacnew-arm-r35b.py` VERSION 2 (this commit; sha256 in the commit's LOG entry), whose docstring, constant `PREDICATE` and receipts carry this sentence (label `matches`):

"A view matches when the census at the named revision exits 0, 1 or 2 within 180 s, prints exactly one line that begins `DRIFT pacnew-plane ` whose fields pacnew, pacsave, pacorig, unreadable, log_pacnew, log_pacsave, unlogged and gone each appear once as name=integer and all equal the oracle's values for that view, leaves the view's etc tree and log unchanged (bytes, modes and inode change times), and, in a stub view, prints every other line except the first exactly as the claim-base census does on the same view with the same exit code; the views are 20 stub views (TSUKUROI_ETC_DIR and TSUKUROI_PACMAN_LOG set, every probe seam stubbed), 3 namespace views (no TSUKUROI_ variable set; a fresh fixture bind-mounted over /etc and /var/log/pacman.log in an unprivileged user and mount namespace, capabilities dropped) and 1 live view (no TSUKUROI_ variable set; the real host, read-only)."

Measure (QUALITY 73): the battery's last line. C1's declared after-value is `candidate_matches` 24 of `of` 24, `control_matches` 24, `should_fail_accepted` 0 of `should_fail` 17, `harness_errors` empty, exit 0, at the change commit. Before: `candidate_matches` 0 at the base (L1 development run below; the before receipt is a wave-2 seat's). The battery inserts into the claim-base census a correct control arm (must match every view) and seventeen should-fail arms, each bending one part of the work: fixture-gated (works only when the seam is set), cached live values, a 64-line log tail, basename-only pair check, gone by `[ -e ]`, decimal-only numbered saves, dangling symlinks only, files and links only (FIFOs dropped), word-split paths, a 2026-only date filter, a basename-only join, global (non-`/etc`) log counts, an arm that exits early, chmod-and-restore of unreadable directories, all-zero, no pairing, and an unpaired log regex. The fixtures force the shapes the wave-1 critics named (symlinks to existing files and directories, a FIFO, `.pacsave.<digit><letters>`, a basename present in two directories with one logged, a gone target whose basename exists elsewhere, a log target that is a directory, a directory-mismatched warning pair, a non-`/etc` warning, long logs with an early event, four timestamp shapes, names with spaces, unreadable modes 000, 300 and 100) and draw every name component the same way, whatever its role. Named limits: a census that inspects its own namespace (uid_map, mountinfo) can tell the namespace view from production; names containing a newline are not generated; the harness-snooping control class (K09) was held by a provider refusal in wave 1 and is not scored by a seat.

Freeze rule and kill rule (fixed now, before any seat scores VERSION 2): the wave-2 pre-freeze control seats score VERSION 2 at this commit; the freeze commit names these bytes. If any control or after-mutant this round that skips or bends part of the work meets the after-value (`candidate_matches` 24 of 24 with `--skip-battery`, `harness_errors` empty, exit 0), or if any should-fail arm is accepted in a battery receipt, C1 is reported not verified. The one exception is a census that tells the namespace view from production by inspecting its own namespace (uid_map, mountinfo, the mount over `/etc`): that is the named limit above, and such a control is reported as reaching the limit, not as a kill. No VERSION 3 will be made this round: after this redesign the counter is not changed again, whatever any seat finds.

L1 development runs of VERSION 2 before this commit (not receipts): at the base, `candidate_matches` 0, `control_matches` 24, and in the first run one should-fail arm (basename-only join) was accepted because no fixture held a gone target whose basename exists elsewhere; that fixture shape was added before this commit (second development run recorded in `.ufo/waves/round-35/l1/`).

### Round 35 — corrections to round-34 records (round-34 spot-check §5 items 3 and 5; drafted by wave-1 ScribeCorrections)

- Amendment-1 disclosure (`SCORECARD.md:1467-1469`): C06HostSnapshotNames, C16PositiveAllowlist and C18GitPathAlias finished at 08:48:26Z, 08:47:01Z and 08:45:22Z (`jq -r 'select(.receipt_end) | .finished_utc'` on `.ufo/waves/round-34/w1/C06HostSnapshotNames/claim.jsonl`, `C16PositiveAllowlist/positive-claim.jsonl`, `C18GitPathAlias/alias-claim.jsonl`), before the amendment-1 commit `15c9ac0e` at 08:51:51Z. The correction's "still running then and scored later" is wrong for all three. CritKillRuleReading's finding stands as a named limit of any successor probe: excluding a fork without exec narrowed the kill rule after it was reported.
- Timestamps: commit `6de666c4` is 08:23:48Z, so the "08:16–08:58Z" window in `.ufo/waves/round-34/l1/dev-base/README.md` straddles the commit; commit `3457f287` is 09:04:36Z, so "~09:08Z" in `l1/dev-amend2/README.md` and "~09:10Z" in the amendment-2 heading (`SCORECARD.md:1455`) are later than the commit that carries them. They are development-note times, not commit or receipt times.
- Freeze wording: the round-34 declaration said "The probe and predicate are not changed after any seat scores" and both amendments broke it. Round 35 states the hyaku 01:05Z exception it uses (above) and limits it to one redesign.


## Round 35 measured outcome

Counter: `tools/score-pacnew-arm-r35b.py` VERSION 2 at `7186722b` (sha256 `7517af92…`), battery mode, through `run-receipt.py --tool-revision 7186722b`. VERSION 1 (`score-pacnew-arm-r35.py`, `19d25d14…`) was met by wave-1 K08FixtureKeyed and K15FieldMutants and retired unchanged before any freeze. Order: candidate declaration `6b4561e4`; wave 1; redesign `7186722b`; wave 2 (pre-freeze controls under VERSION 2, kill rule fixed at `7186722b`); the change `e2f97e6e`; after receipt.

| Claim | Before | After | Author verdict |
|---|---|---|---|
| C1 (coverage) census pacnew/pacsave drift arm | battery at `7186722b`: `candidate_matches` 0 of 24, `control_matches` 24, `should_fail_accepted` 0 of 17, exit 1 (`.ufo/waves/round-35/w2/W2BeforeBattery/before-battery-7186722b.jsonl`) | battery at `e2f97e6e`: `candidate_matches` 24 of 24, `control_matches` 24, `should_fail_accepted` 0 of 17, `harness_errors` empty, exit 0 (`.ufo/waves/round-35/after/c1-after-battery-e2f97e6e.jsonl`, finished 11:54:36Z) | **not verified under the declared kill rule.** Two pre-freeze controls that skip part of the work met VERSION 2 before the change existed: W2TreeKeyed (forced-FIFO signature plus constants for the forced non-regular entries; `.ufo/waves/round-35/w2/W2TreeKeyed/variant.jsonl`, 24 of 24, exit 0) and W2LogKeyed (first-warning gate, 44-line read; `W2LogKeyed/`, 24 of 24, exit 0). W2NsDetect reached the declared named limit. No freeze commit and no VERSION 3 |
| C2 (depth, exploratory) pacman 7.1 backup-file mechanism | no entry read pacman's code for when `.pacnew`/`.pacsave` are made or logged (`pacnew-plane.md`, `package-state-plane.md`) | `corpus/knowledge/pacman-backup-files-r35.md` (S191-S196; NULL-hash branches, NoUpgrade prerequisites, unlogged `.pacsave.N` shift, silent `.pacnew` rewrite as [inf], `.pacorig` retirement), after W2QuoteHash/Remove/Pacdiff re-opened every quote and W2CritC2Depth/W2RevC2Quality corrections | exploratory; awaits the named non-author reviewer (the closure) |

The after value stands as a measurement; what fails is the declared condition that no control that skips work meets the counter. Counter defects found in wave 2 and not repaired (no VERSION 3): W2MutCounter shows the battery does not cover the ctime check or the live view (two counter mutants survive); W2ArmAuditA/B find F04 refused partly for an unrelated regex error, F07 also dropping FIFOs, and eight control/oracle disagreements on inputs the fixtures never generate; W2RevCounterV2 finds the live view's unchanged check compares totals only and the ctime walk stops at unreadable directories; W2SentinelViews finds that a candidate's malformed DRIFT tokens are echoed into receipt `reason` strings (an exfiltration path for names a census reads).

No-harm: census selftest 101 → 105 cases, 105 passed (four new drift cases; every earlier case still passes; one load-dependent failure on the first run, passed on re-run, disclosed above); the base-parity clause of every after-receipt stub view held (no PLANE line, rollup or exit code changed in 20 of 20 stub views); no other tool changed between `7186722b` and `e2f97e6e` (`git diff --stat 7186722b e2f97e6e -- tools/` lists only `tools/tsukuroi-census.sh`). Gate receipts at `6b4561e4` (wave-1 ExecGateBaselines): check-self-assessment exit 1 (K10, inherited from the base), check-registry-coverage exit 1 (the then-unregistered VERSION 1 counter; the round35 registry table now carries both counters), check-pause-gate exit 1 (the same P3 as base), the other four exit 0; no gate receipt exists at the final tip.

Ordinal record, round 35 (no ordinal moved): depth 8 → 8; coverage 9 → 9; operability 9 → 9; freshness 9 → 9; calibration 9 → 9; adjacency 8 → 8.

Planned (round 36): repay the routed counter debts before any re-claim (the round-34 untraced view and VERSION 6 normalisation; a pacnew counter whose forced shapes vary in count and whose battery holds the W2TreeKeyed and W2LogKeyed patches); the five live-tool ambient copies.

## Axes — current self-assessment (round 35)

Appended 2026-10-23 by round 35; supersedes the round-34 table. Ordinals unchanged. Counts that changed: 55 notes (`pacman-backup-files-r35.md`), `SKILL.md` 3009 lines and 784 table lines (round35 registry and DRIFT reading rule), 46 lesson files (`round-34-verifier-spotcheck.md`, `round-35.md`), census selftest 105 cases.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 55 notes (`ls corpus/knowledge/*.md`, counted with `wc -l`); `SKILL.md` 3009 `wc -l`; 784 table lines (`grep -c '^[|]' SKILL.md`); `corpus/lessons/` (46 files) (counted with `find corpus/lessons -type f` and `wc -l`); rules added since round 12 cite `corpus/knowledge/*.md` notes, while four standing rules near the top of `SKILL.md` cite none. Ceiling: the depth ordinal was last moved at round 4, and no round from 12 to 24 changed it, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` 256 `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); the census has six planes, each with a landed note (the oom plane is a supporting measurement in `PROVINCE.md`, not a declared surface); the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry; since round 35 one of them (`.pacnew` / `.pacsave` drift) has a census arm (`DRIFT pacnew-plane`, landed at `e2f97e6e`), whose coverage claim C1 is not verified (kill rule fired), so the ordinal does not move. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (105 cases, 105 passed, 0 failed) at `e2f97e6e` (L1 run `.ufo/waves/round-35/l1/r35-st-after2.txt`; a first run under host load read 104 of 105, `r35-st-after.txt`) with exit 0; the live run exits 1 with a six-plane rollup and one verdict-neutral `DRIFT pacnew-plane` line; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes) stand; all 55 notes now carry a `recheck:` line, and the round-1 figure of 25 of 25 per-note rechecks is historical; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop for rounds 1 to 9; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |


## Capabilities — current (round 35)

Appended 2026-10-23 by round 35. This table supersedes the round-32 table at `SCORECARD.md:1310`; the rows, pointers and first-working rounds are unchanged except the host-census-gate row, whose case count the round-35 census change moved from 101 to 105 (four DRIFT cases; `.ufo/waves/round-35/l1/r35-st-after2.txt`) and whose output gains the `DRIFT pacnew-plane` line. No capability row is added: C1, the drift arm's claim, is not verified this round.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates where the lane learns: `corpus/SOURCES.md` holds opened, tier-scoped rows with anchors, rejections with flips, study paths, a search log and unopened leads, and the row set is checked by the frozen contract's census commands | `corpus/SOURCES.md`; the census commands and their outputs in `.ufo/evidence/round-1-kaika/after.md` (34 rows in that snapshot, malformed 0, no duplicate, enum or missing output; 125 rows at round 25) | fleet r1 (2026-10-19) |
| host-census-gate | Emits a read-only six-plane host verdict and one verdict-neutral `DRIFT pacnew-plane` line (TSUKUROI_CENSUS: HEALTHY, DEGRADED or BLOCKED; exit 0, 1 or 2) with a hermetic 105-case selftest that touches no live host surface | `tools/tsukuroi-census.sh` selftest prints PASS 105/105 rc=0 (105 cases, 105 passed, 0 failed); the live run exits 1 with a six-plane rollup; receipts `.ufo/evidence/round-1-kaika/scout-live.md` and `.ufo/evidence/round-1-kaika/after.md` | lane r2 (census-v1); demonstrated running fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations even on package-probe failure; isolates fixtures and blocks unavailable or non-directory metadata without grading intentional 0555 policy | `.ufo/waves/round-12/resumed/after.json`, `.ufo/waves/round-12/resumed/selftest-after.json`, `.ufo/waves/round-12/resumed/mode-policy-mutant.json`; measured commit `70fede2a7a890cb50a72db2d4230ee541183bf7b` | round 12 |
| boot-chain-audit | Audits every limine entry live and read-only: copies each UKI with a read-only `sudo -n cat`, extracts its initramfs in a private mktemp directory, types the new_root path, binds the firmware-selected entry, and emits a per-entry next-boot verdict plus TSUKUROI_BOOTCHAIN | `tools/boot-chain-audit.sh` live run wrote `.ufo/waves/round-17/l1-capture/audit-live.txt` (6 entries, CONSISTENT, exit 0); its selftest prints PASS total=45 failed=0 | round 17 |

## Round 36 — declaration, pre-freeze candidate (2026-10-23, base `cefe752d`)

Written 2026-10-24T02:33Z (`date -u`, stamped at write time per the round-35 routed
defect 2 fix). Base `cefe752d9facf74113bb00a5925e3bfd0c863659` (round-35 closure tip;
the round-35 spot-check is `corpus/lessons/round-35-verifier-spotcheck.md`, whose §6
routes five defects this round works). Depth and adjacency are tied lowest at 8; none
retired; saturation 9 / window 3 unchanged. Two claims, distinct axes; the depth claim
(C2) carries the lowest-axis duty.

**C1 — operability: the five live tools stop copying the ambient environment into child processes.**
Before: the five tools the round-35 spot-check §6 item 3 names still build a child
environment as a copy of the ambient environment minus a name prefix —
`tools/check-revision-binding.py` (`clean_env()`, `os.environ` minus `GIT_*`),
`tools/check-report-receipts.py` (`find_receipts`, `os.environ` minus `GIT_*`),
`tools/score-census-handoff-r32.py` (`os.environ` minus `TSUKUROI_*`),
`tools/mutants-btrfs-space-r30.py` (`os.environ` minus `GIT_*`),
`tools/run-receipt.py` (`env()`, `os.environ` minus `GIT_*`). Any non-`GIT_*` ambient
name (injected config, secrets, harness variables) reaches every child they spawn.
After: each of the five builds every child environment from a fixed dict display —
`PATH=/usr/bin:/bin`, `LC_ALL=C`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`
(and `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_PAGER=cat` where the
tool already sets them) — retaining only each tool's existing run-private computed
settings (`HOME`/`XDG_CONFIG_HOME` to a private empty dir and `GIT_CEILING_DIRECTORIES`
to the run's scratch parent in `check-report-receipts.py` and `run-receipt.py`).
Counting command (before and after, from the lane root):
`python3 tools/probe-child-env-allowlist-r36.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision <REV> --set livefive --json`
whose last JSON line's `leaking_pairs` is the measure; **before: at least one leaking
pair on every one of the five targets; after: `leaking_pairs` 0 on all five targets,
`harness_errors` empty, exit 0, with the probe's sensitivity checks green (the
committed `MutAttrgetterCopy` and `MutPathCopy` mutants each read above 0 and the
`claim`, `r33claim` and `regression` sets at the base each read 0 in the same run)**.
The probe is the counter; its frozen predicate label is `leaking_pairs`, the same
sentence in this declaration, the probe's `PREDICATE` constant and every receipt.

**C2 — depth (exploratory): the journalctl v262 field/filter rejection, decision-tabled for the lane's journal consumers.**
Before: no lane entry documents systemd 262's rejection of `journalctl -F`/`-N`
combined with options that limit the journal; S024 (queued) asserts the fact without a
pin, an error signature, an exit code, a flag matrix or consumer guidance. After:
`corpus/knowledge/journalctl-v262-field-filter-r36.md` — the exact rejection line
(`-F/--field= and -N/--fields cannot be combined with options that limit the
journal.`), its exit code, the matrix of limiting options verified live and read-only
on this host (`systemd 262 (262-1-arch)`), the safe substitution patterns for the
lane's journal consumers (census arms and tools), and a falsifier section. Prior-state
counting command: `grep -rl "cannot be combined with options that limit the journal"
corpus/knowledge/ SKILL.md` prints nothing at the base. Exploratory: verifies only as
`unprovable-but-better` with the named non-author closure reviewer; no ordinal move is
claimed for a taste-bound note.

Counter and freeze (C1): the counter is `tools/probe-child-env-allowlist-r36.py`,
written in wave 1 as the round-34 probe (`tools/probe-child-env-allowlist-r34.py`,
VERSION 4) plus this paragraph, VERSION 5, the `livefive` set, an untraced view of
child environments and the normalisation fixes — repaying the round-34 spot-check
routed defect 3 (untraced view scored against the committed `MutAttrgetterCopy` and
`MutPathCopy` mutants, each above 0; `claim`/`r33claim`/`regression` sets at the base
each 0; normalisation for short hashes, fixture paths and
`GIT_CEILING_DIRECTORIES`/`$HOME`-derived values, from the round-35
`ExecV6Calibration` receipts). Freeze rule (round-34/35 shape): pre-freeze control
seats score the probe at the base; the freeze commit names the probe bytes
(sha256 in the LOG entry); after the freeze the probe, predicate, label, set and
after-value do not change. Kill rule (fixed before any seat scores the after value):
if any variant of the five tools that skips the fixed-dict work (any builder reading
the ambient environment, any prefix filter, any inheriting spawn) reads 0 leaking
pairs on all five targets with `harness_errors` empty and exit 0 under the frozen
probe, C1 is reported not verified. QUALITY 73/82 shape: the declared measure is the
battery receipt's last line; the `livefive` runs execute the tools against a fresh
exported copy of the lane tree (read-only) — a view the tool cannot tell from
production — and a live read-only view against the real lane checkout is run at the
after state.

Sourced claim: C2 rests on S024 opened this round (re-opened pinned to the systemd
v262 tag) and a new row S198 (journalctl(1) at systemd 262); both quotes are recorded
in the round-36 lesson `## Gate`. Separability: C1 touches only the five tools and the
new probe; C2 adds one knowledge note plus `SKILL.md`/`corpus/README.md`/`SOURCES.md`
rows and changes no tool; the probe never reads the note; each claim verifies without
the other.

Repairs that are not claims (round-35 spot-check §6): (1) the leftover
`.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz` is committed as evidence
in this round's first commit; (2) every heading time this round is pasted from
`date -u +%H:%M:%SZ` at write time (this declaration shows the stamp); (4) the
NoUpgrade/NoExtract correction sweep appends supersession rows naming
`corpus/knowledge/pacman-backup-files-r35.md` to `SKILL.md:397-399`,
`corpus/knowledge/update-safety-note.md:420-424`, `corpus/knowledge/update-safety-v2.md:52`
and `:198` — append-only, history not rewritten; (5) the seven lane gates run at the
first commit that carries the C1 change, not after the outcome commit. Routed debt 3b
(the pacnext VERSION 3 counter) is **not** owed this round: no pacnew claim is made or
re-claimed; the v3 requirement list (from W2MutCounter, W2ArmAuditA/B, W2RevCounterV2,
W2SentinelViews, W2LiveOracle) is recorded in the report as the freeze condition for
any future pacnew re-claim.

Order: this declaration commit (with the tarball); wave 1 (32 seats: controls and
before receipts, probe drafting, C1 patch design, C2 live verification and drafting,
sources, repairs, gate baselines); the L1 commits every wave-1 control receipt; the
freeze commit; the C1 change, its after battery receipt and the C2 note; wave 2 (32
seats: falsify); the measured outcome, lesson, SOURCES/README/SKILL registry rows and
report.

## Round 36 — pre-freeze corrections (2026-10-24T04:22Z, before any after-data seat scored)

Written after wave 1 settled (32/32 seats; 02:43:10Z dispatch) from ReviewDeclaration
(H1/H2/M1-M4), RevProbeLineage (F4/F5), CriticFreeze (NO-GO items), MutProbeDraft (M2/M5,
structural findings 1-2 and the corrected MutPathCopy reading), SimplifierProbe (F1/F4),
ReviewC1Design (F1/F2/B3), CriticClaimShape (15 attack classes), ExecProbeR36 (set viability,
VERSION label) and ExecC1Design (patch states). Nothing below changes the claims' axes,
before-values or the after-value target (leaking 0 on all five livefive targets, harness_errors
[], exit 0, sensitivity conjuncts green).

1. **Counter lineage (H1/F5):** the round-34 probe file at the base is `VERSION = 6`
   (V4@`6de666c4`, V5@`15c9ac0e`, V6@`3457f287`; ExecV6Calibration receipts record
   `probe_version: 6`). The frozen counter is `tools/probe-child-env-allowlist-r36.py`
   **VERSION 7**; the wave-1 draft's "VERSION 5" label moved the counter backwards and is
   superseded. Round-34 amendments 1 (claim-base parity) and 2 (any-name value, execveat,
   unparseable) are carried unchanged.
2. **Frozen predicate sentence (H2/F4)** — verbatim from the probe's `PREDICATE` constant and
   docstring (label `leaking`): "A (target, channel) pair is leaking when, in its names or quiet run, any traced execve after the target's own first exec carries in its environment any name injected in that run or the exact ambient NAME=VALUE string of that run for any value-channel name (HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, LOGNAME, SHELL), or carries under any name a value equal to that run's TMPDIR or containing any other run-unique ambient value of that run (its HOME, XDG_CONFIG_HOME and injection-directory paths, its LANG, TZ, TERM, USER, LOGNAME and SHELL words, and its injected values), or the run makes any execveat call or has an execve record the probe cannot parse, or any traced git execve lacks GIT_CONFIG_NOSYSTEM=1 or GIT_CONFIG_GLOBAL=/dev/null, or the run breaks parity with control run A (exit code, normalised stdout digest, count of successful git execs), or control run A breaks base parity with the same target's control run at the claim base (exit code, normalised stdout digest, count of successful git execs, multiset of normalised git argv); or, in its source channel, the target's file or a tools/ module it imports at REV reads the ambient environment, starts a process that inherits it, names /proc/self/status, /proc/self/environ or TracerPid, or uses a construct that hides a read or spawn from the scan."
3. **Measure (M1/M2):** the counting command is
   `python3 tools/probe-child-env-allowlist-r36.py --revision <REV> --set livefive` (stdout is
   JSONL; the LAST line is the summary). The declared measure is the summary's `leaking` count
   == 0 with `leaking_pairs` == [], `harness_errors` == [], exit 0 and `predicate_label` ==
   `leaking` — the label 31 round-34 receipts carry. The probe has no `--json` flag; the
   declaration's `--json` was wrong.
4. **livefive set + named limit (CriticFreeze, ExecProbeR36, CriticClaimShape):** all five
   declared tools are targets, including `tools/score-census-handoff-r32.py`
   (`--revision {rev} --lane {clone} --scenarios 1 --budget 180 --seed 36`; direct control
   16.77 s). Named limit, recorded before data: that tool's live views read the live journal,
   whose counters drift between back-to-back runs (the tool itself excludes its live counters
   from its own live-parity comparison), so for `livefive` ONLY, within-run A/B and claim-base
   parity diffs are recorded (`parity_diffs`, `base_parity_diffs`) but are not leak evidence;
   every other set keeps the r34 parity rule. The untraced channel observes only children that
   inherit the probe's injected PATH; zero records is UNINFORMATIVE (never a leak, never a
   harness error by itself); the channel's sensitivity is proven by the committed mutant runs
   (MutAttrgetterCopy defeats wrappers with a reapplied fixed PATH and is caught by the
   strace/source channels; MutPathCopy preserves ambient PATH and must read above 0 on the
   untraced channel — MutProbeDraft correction included).
5. **Change-shape corrections (ReviewC1Design F1/F2, SimplifierProbe F1):** (a) the change
   introduces `GIT_CEILING_DIRECTORIES` into `run-receipt.py`'s fixed dict as a computed
   run-private setting — the declaration's "existing" wording was wrong; (b) `LC_ALL=C` is added
   to `check-report-receipts.py`'s fixed dict; (c) `mutants-btrfs-space-r30.py`'s
   `__import__('re')` hiding construct is rewritten as a plain top-level `import re` (the only
   true source-channel hit in the five files). The probe's normalisation excludes computed
   `GIT_CEILING_DIRECTORIES` values and HOME-derived paths, so the retained settings do not
   false-positive (SimplifierProbe: without that exclusion two targets read >0 by construction).
6. **Normalisation (MutProbeDraft finding 2, ExecProbeR36 dev runs, L1 root-cause):** short-hash
   normalisation is the broad form plus `git --disambiguate` prefixes (4-64) in both the text and
   bytes paths; the probe's own run-layout names are normalised (`<ROOT>/<r+12hex>` run dirs and
   `<ROOT>/<RUN>/tree/<fixture>-<8>` tool fixtures, suffix charset `[A-Za-z0-9_]{8}` because
   `tempfile` random names include `_`). Without these the parity self-check misfires on
   run-unique names: receipted dev sequence on final bytes — r33claim read 6 (both scratch-shape
   classes), then 3 after the run-layout rule, then 0 after the underscore fix (receipts
   `.ufo/waves/round-36/l1/dev-r33claim-final*.jsonl`).
7. **SOURCES rows (M3/M4, SentScope, S196/S006 precedent):** row S024 is NOT edited in place
   (registry no-old-row-change discipline); two new rows land with the note in one commit
   (census E11): **S198** journalctl(1) at systemd 262 (semantics only — the page does NOT carry
   the restriction sentence; SrcJournalctlMan F1) and **S199** systemd NEWS pinned at tag v262
   (the prose bullet at NEWS:129-133, sha256 `a494f038…a7657`; supersedes S024 for this note).
   The exact 84-byte rejection line is evidence from `src/journal/journalctl.c:958-960` and the
   shipped binary, attributed as such in the note.
8. **Repair pointer (L1):** routed item (3)'s pacnew VERSION-3 debt is documented at
   `.ufo/waves/round-36/w1/ExecPacnewDebtNote/v3-requirements.md`; no pacnew re-claim is made
   this round, so the debt gates nothing here.
9. **Kill rule, restated frozen:** if, after the freeze, any variant of the five tools that
   skips the fixed-dict work (any builder reading the ambient environment, any prefix filter,
   any inheriting spawn, any hidden read) reads `leaking` 0 on the livefive battery with
   `harness_errors` [] and exit 0 — OR any sensitivity conjunct fails (MutAttrgetterCopy and
   MutPathCopy each read above 0; claim/r33claim/regression sets at the base each read 0) —
   C1 is reported not verified.

Order amended: this corrections commit; the freeze commit (probe bytes + before battery +
sensitivity receipts + live-view before receipt, sha256 in LOG); the change commit (five tools,
the note, S198/S199, the four NoUpgrade appends, SKILL.md round36 registry table, lesson
skeleton, this block); gates at the change commit's first run; the after battery + live-view
after receipt; wave 2 (32 falsify seats); the measured outcome.
## Round 36 measured outcome (2026-10-24T04:39Z, attempt 1 — landed at budget deadline with wave-2 seats still settling)

Claims and verdicts (author-side; every verdict awaits the non-author closure):

- **C1 (operability) — NOT VERIFIED under the declared battery; partial evidence green; two
  sensitivity conjuncts re-stated with live-mode evidence (named limit, post-freeze correction).**
  Landed: the five tools' builders are fixed dicts (AST-verified: no ambient read on any spawn
  path, no inheriting spawn, no hiding construct; compile-clean); the frozen probe VERSION 7
  (sha256 a2a5acac…, freeze 1e926801). Measured after evidence in hand at landing: pristine
  after readings leaking 0 on three of five tools at c052bb7 (W2MutTool2/4/5 receipts),
  the QUALITY-82 production-like live view 0/5 tools leaking canaries at c052bb7
  (W2LiveOracle), no-harm clean (selftest 105/105, battery 10/0/0, livefive receipt check 0 —
  W2ExecCensusSelftest), after-mutants m2/m4/m5 each KILLED by the frozen probe (names/quiet/
  source channels fired; ordinary-run checks confirm real leaks). Outstanding at landing
  (seats still running, inherited): the single full-battery before receipt (W2ReBefore) and
  after receipt (W2ReAfter), after-mutants m1/m3/m6, the regression-set receipt, and the
  kill-rule attack seat W2CritKill, which died at 13s on a provider cyber_policy flag (error
  text recorded; same hold class as round-35 K09HarnessSnoop) — the kill-rule attack class is
  therefore unscored by a seat this round. Sensitivity conjuncts: MutAttrgetterCopy and
  MutPathCopy each read 0 under every frozen-probe invocation (GAP, receipted by
  W2MutAttrgetter/W2MutPathCopy: the probe's fixed invocations never construct the mutated
  git(); the readings are uninformative, not passes) and each reads above 0 under the live-mode
  detector (7/19 canary-carrying children vs 0/19; untraced live 2 records with the exact
  ambient PATH string vs 0) — the conjunct is re-stated as live-mode-detector evidence, the
  same instrument class as the round-34 ordinary-run receipts.
- **C2 (depth, exploratory) — landed; correction-needed per the critic; awaits the named
  non-author closure reviewer.** The note carries the exact rejection line + exit 1/EINVAL,
  the predicate term-by-term table, the -n allowed-silent third state, the scope-allowed
  selectors, the safe substitution and the preventive consumer inventory; W2CritC2Depth rules
  it correction-needed exploratory depth (not expansion): 15 not 16 predicate terms, -F
  truncation vs unchanged -N output under -n, and action overrides misclassified as working
  enumeration must be corrected in place; W2RevC2/W2QuoteNews/W2RevSources seats were still
  running at landing.

Axis scores: no ordinal moves (operability 9, depth 8 — the C2 verdict is carried by the
closure reviewer row, not a number; coverage 9, freshness 9, calibration 9, adjacency 8).
Counts: 56 knowledge notes, corpus/lessons 48 files, SKILL.md 3057 lines / 796 pipe lines,
SOURCES.md 199 rows (S198/S199 added, S024 unchanged; census exit 0).

Repairs landed in the outcome commit: the round-36 registry table carries every round-35 row
plus the probe row with the embedded freeze sha (W2ExecGates/W2ExecCensusEnd found the
two-row table broke check-registry-coverage: 51 missing of 53); this axes row states the
current counts (K07/K10 self-assessment drift repaired); the adjacency sentence on S198 vs
mori S014 (W2ConnAfter) appended to corpus/SOURCES.md; the C2-note corrections pending the
still-running review seats are NOT applied here (they land with the closure or the next
round's repair commit).

Process defects mined into corpus/lessons/round-36.md: R36-DOC-FREEZE (the pre-freeze
corrections were written before the freeze but committed with the change — W2CritFreeze
documentary FAIL; fix: corrections are a commit BEFORE the freeze commit), R36-PLACEHOLDER-TIME
(the LOG '03:5xZ' placeholder — W2SentinelDiff; fix: omit the time if unmeasured), R36-REGISTRY-DROPPED-ROWS (a superseding registry table must carry all prior rows), R36-SPAWN-DROP (W2ScribeRegistry spawn-dropped; recorded with no error text available), R36-CYBER-HOLD (W2CritKill cyber_policy; the kill-rule class stays unscored-by-seat).

Measured commits: declaration 6d76fb20; wave-1 evidence 189d8a08; freeze 1e926801; change
c052bb7d; wave-2 evidence 8d5fa7fe; outcome (this commit).

## Round 36 — verdict-final update (2026-10-24T04:44Z, late wave-2 findings before filing)

W2MutTool1 and W2MutTool3 returned before filing: after-mutants m1 and m3 are KILLED by the
frozen probe (m1: leaking 4, all four channels; m3: leaking 3, names/quiet/source) — with
m2/m4/m5/m6 that is all six after-mutants KILLED, each with an ordinary-run leak check.
W2MutTool3 also lands the decisive counter-reading: at the change commit c052bb7d the frozen
probe's SOURCE channel already reads `leaking 1` on the pristine fifth target
(`tools/score-census-handoff-r32.py:source` — `run_census()` line 489
`Popen(['/usr/bin/bash', script], env=env, …)` where `env` is a function PARAMETER, flagged as
an ambient read; the same file at base 6d76fb20 carried 4 such findings, the change cut them to
1). The source channel cannot tell a parameter named `env` from `os.environ` — a frozen-counter
false-positive class, repairable only by a counter redesign (VERSION 8), not this round.
**Consequence: C1's declared after-value (`leaking` 0 on the full livefive battery) does not hold
at the change commit; C1 is NOT VERIFIED, now by concrete counter-reading, not only by missing
receipts.** The kill rule fired against the claim in its intended direction. W2RevSources:
census exit 0 at 199 rows, S024 untouched (7/8 checks pass). W2QuoteNews: the S199/S198 pins
and all 54 matrix cells reproduce; the C2 corrections (15 terms, empty-value parse edge, pyc
caveat) stand for the closure or the next repair commit.

## Round 36 — final (2026-10-24T04:48Z, all landed seats integrated)

W2ReBefore landed the before battery receipt-backed: at base 6d76fb20 the livefive set reads
**18/20 pairs leaking, all five targets > 0** (its direct invocation also exposed probe bug S1).
W2RevCounter's falsification catalogue is accepted into the round record: S0 after-value false
at c052bb7 (source-channel parameter rule; the production repair  +
 in child_env lands in this commit — F2's harmed systemd plane verified back
to  under child_env, and the unit-level counter reading on the repaired tool is
receipted in  if present else the bg run's seat);
S1 the full-battery invocation crashes on the revision-binding target ( already exists
after clone — probe bug); S3 livefive vacuity (a do-nothing variant reads 0 with parity waived);
S4  is not in OS_AMBIENT so source+untraced are both silent on that shape;
S5 the r33claim 6→3→3→0 receipt sequence is a posteriori across real code fixes (the misfire
classes are receipted, but the freeze-pick is honest only with that sequence visible). C1 final
verdict: **NOT VERIFIED** — before > 0 receipted; after per-tool 0 on four tools + repaired
fifth unit-clean; all six after-mutants KILLED on exercised builders; sensitivity live-mode > 0
receipted for both named mutants; and the counter itself carries S1/S3/S4 defects that make the
declared battery unexecutable/vacuous — VERSION 8 debts, enumerated in
, for a future re-claim. No ordinal moved.
The XDG_RUNTIME_DIR harm repair and the  visibility repair land here as
review-driven repairs (W2RevToolB F2, W2RevToolA H1); C1 is not re-claimed by them.

## Round 37 — declaration, pre-freeze candidate (2026-10-25, base `564db0b614`)

Base `564db0b614b2914de5452f9ebd537a0653ae1de5` (branch tip at dispatch; the round-36 verifier
spot-check commit; origin resolves to the same hash). Ordinals at the base
(`SCORECARD.md:1795-1796`): operability 9, depth 8, coverage 9, freshness 9, calibration 9,
adjacency 8; saturation 9 / window 3, so the stagnation nudge does not waive the lowest-axis duty
(depth and adjacency are tied lowest). Three claims, distinct axes: operability, depth,
calibration. Routed round-36 defects land as repairs inside these claims' commits (probe
VERSION-8 debt is C1; C2-note corrections are C2; the LOG stamp typo is repaired by a LOG append).

**C1 — operability: the round-36 probe's VERSION-8 redesign makes the livefive battery
executable, non-vacuous and leak-discriminating for the five live tools.**

Declared target: `tools/probe-child-env-allowlist-r37.py` (new file, VERSION 8, PREDICATE label
`leaking`, docstring-embedded predicate = the frozen r34 sentence) replaces
`tools/probe-child-env-allowlist-r36.py` VERSION 7 as the round's counter and repairs the four
routed defects:
- S1: direct full-battery invocation crashes (`RuntimeError: cannot create local master branch`,
  probe line 499) on the revision-binding target after clone; the fix restores a runnable direct
  mode.
- S3: livefive vacuity — a do-nothing variant reads leaking 0 with the A/B parity waiver; the fix
  closes the vacuity gate named by the W2RevCounter catalogue (round-36 wave-2 reports).
- S4: the `os.get_exec_path()` ambient PATH shape is invisible to both source and untraced
  channels; the fix adds the channel/shape detection named in the W2RevCounter catalogue.
- Source-channel parameter rule: a function parameter named `env` is flagged as an ambient read;
  the fix resolves parameters from ambient attribute reads (`os.environ`), not from name matches.

Counting command (before and after, from the lane root):
`python3 tools/probe-child-env-allowlist-r37.py --revision <REV> --set livefive`
(the LAST JSONL line is the summary; exit 0 clean, 1 leaking, 2 harness error). Declared measure:
summary `leaking` == 0, `leaking_pairs` == [], `harness_errors` == [], `predicate_label` ==
`leaking`, exit 0. Before (base 564db0b614, with the V7 instrument + defect repros): V7 direct
invocation crashes (S1); the do-nothing vacuity control reads leaking 0 (S3); the source channel
carries the parameter-`env` false-positive class; the full livefive battery runs only through the
receipt wrapper. After (change commit): all four fixes present; the full livefive battery runs
both directly and through `tools/run-receipt.py`; reads `leaking` 0 on all five targets with
`harness_errors` [] and exit 0.

Kill rule (fixed before any seat scores the after value): if any variant of the frozen probe that
skips any of the four fixes (S1 crash path, no vacuity gate, no S4 channel, parameter-name `env`
rule) reads `leaking` 0 on the livefive battery with `harness_errors` [] and exit 0, C1 is
reported not verified. Sensitivity conjuncts: the committed mutant probes (one per fix, sandbox
commits) each read above 0 under the frozen probe; base-set readings (claim/r33claim/regression)
read 0. Do-nothing control: V7 at the base (S1 crash + S3 vacuity reproduced in receipts) cannot
reach the after value. Freeze rule: the freeze commit names the probe bytes (sha256 in the LOG
entry); after the freeze, the probe, predicate, label, livefive set and after-value do not change.
Sourced claim: C1's probe note cites a strace(1) row opened this round (S200-strace) plus the
probe's own-work row (S201-probe), both opened and mined in-round.

**C2 — depth: the round-36 journalctl-v262 note becomes correction-complete per the closure's
routed list.**

Routed defect: round-36 verifier spot-check §6 item 2 (W2CritC2Depth): 15 not 16 predicate terms;
`-F` truncation vs unchanged `-N` output under `-n`; action-override classification. Before:
`corpus/knowledge/journalctl-v262-field-filter-r36.md` carries the 16-term table and lacks the two
rows. After: the note carries exactly the corrected 15-term predicate table, the third-state
(`-n`) row distinguishing `-F` truncation from unchanged `-N` output, and an action-override
classification row; the rejection line stays verbatim. Counter: `tools/check-journalctl-v262-corrections.py`
`--revision <REV>` (selftest + committed-read modes) asserts those three facts at the bound
revision; exit 0 clean, 1 failed, 2 could-not-evaluate. Counting command:
`python3 tools/check-journalctl-v262-corrections.py --revision <REV>`; before at base = exit 1
(note uncorrected); after at the change commit = exit 0. Do-nothing control: the checker on the
uncorrected base note exits 1, so a no-op cannot reach the after state.

**C3 — calibration: a verified-rate ledger matches every declared claim to its measured verdict
across rounds 33–36, implementing considerthese/2026-10-23.md proposal 1 ("Verified-rate ledger").**

Before: no ledger exists (0 rows). After: `corpus/knowledge/verified-rate-ledger-r37.md` carries
one row per claim declared in rounds 33–36 (axis, declared after-state, measured verdict per the
round's outcome / report / verifier spot-check, verdict class verified/not-verified/held/honest-stop
and why), and `tools/check-verified-rate-ledger.py --revision <REV>` reports `mismatches` == 0
(every ledger verdict matches the SCORECARD measured-outcome record and the fleet report's
per-claim verdict lines) and exit 0. Counting command:
`python3 tools/check-verified-rate-ledger.py --revision <REV>`; before = exit 2 (no ledger),
after = exit 0 with mismatches 0. Do-nothing control: an empty ledger fails the checker.

Separability: C1 touches only the new probe and its note/rows; C2 touches only the note
corrections and checker; C3 only the ledger and checker; each claim verifies without the others.

Assimilation (§10): ONE theme — errno discrimination — with THREE package entries admitted from
`merge/tsukuroi/`: `errno-name-discrimination-r25.md`, `mount-errno-contract-r26.md`,
`errno-contract-variance-r37.md`; rows S204/S205/S214/S220/S279–S282/S286/S287 appended
(transformed to fleet schema in scratch, census-validated, collision-guard proven) with
re-grounded Gate quotes. Quarantine slice (12 data rows) hand-checked with a verdict per row.
This rides inside §2b and adds no claim slot.

Order: this declaration commit; wave 1 (32 seats v1: controls and before receipts, V8 design/impl,
correction/ledger drafts, sources/assimilation, baselines); the L1 commits every wave-1 receipt;
the freeze commit (C1 counter bytes + before battery + sensitivity receipts); the change commit
(probe V8, C2 corrections + checker, C3 ledger + checker, SOURCES rows, lesson skeleton, registry
rows); after battery receipts; wave 2 (32 seats v1: falsify); the measured outcome, lesson,
SOURCES/README/SKILL rows and report.

### Round 37 — pre-freeze C3 correction (2026-10-25; before any wave seat scores an outcome)

This correction supersedes the C3 target and counter above; no seat has received or scored
round-37 outcome evidence. The original proposed new ledger/checker (which could not be
independently grounded against a stable complete history across SCORECARD and fleet reports)
is withdrawn before data. C3 instead repairs the calibration mismatch measured by the existing
checker.

**C3 — calibration: the self-assessment checker reports zero mismatches (all 27 fixed checks
match) at the measured round-37 tip.** Before: at base `564db0b614b2914de5452f9ebd537a0653ae1de5`,
`python3 tools/check-self-assessment.py --revision 564db0b614b2914de5452f9ebd537a0653ae1de5`
reported `checked: 27`, `mismatches: 5`, `status: FAIL`, exit 1 (K07-K11: four stale depth
counts and one stale README line count). After: append-only correction of the five current
self-assessment count cells to the measured tip values, then the same command at the measured
round-37 branch-tip revision reports `checked: 27`, `mismatches: 0`, `status: PASS`, exit 0.
The frozen predicate is `mismatches == 0 && checked == 27 && exit == 0`; a no-change control at
the declaration base is 5 mismatches, so the do-nothing target is unreachable. The checker bytes
and fixed 27-check population are unchanged; only the self-assessment values may change, and the
claim's counter output is the predicate.

This is a single calibration claim; the new ledger concept is deferred, not claimed or scored.
The 2026-10-23 considerthese proposal is nevertheless mined as a lesson about converting the
verified-rate idea into a resolvable same-revision mismatch counter; it is not represented as
implemented. All later claim declarations remain as stated unless separately corrected before
outcome scoring.

## Axes — current self-assessment (round 37)

Current assessment at round 37, correcting the superseded round-35 counts at SCORECARD.md:1564-1575; the old table is retained as history. Counts below are re-derived from the round-37 base branch tip before updating this table. Ordinal scores remain unchanged; C3 measures the checker mismatch count, not an ordinal uplift.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 56 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3110 newline characters (`wc -l SKILL.md`) / 839 pipe-prefixed lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 49 files (`find corpus/lessons -type f | wc -l`); four standing rules near the top of SKILL cite no knowledge note; no ordinal move claimed. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 269 newline characters (`wc -l corpus/README.md`); PROVINCE Core, Frontier and Adjacent sections present; six census planes; four declared round-1 read-only surfaces link knowledge; pacnew census arm C1 was not verified in round 35, no coverage ordinal move. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (105 cases, 105 passed, 0 failed); live run exits 1 with six-plane rollup; `--identity` absent. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; dated round-1 D1-D5 rechecks and current recheck procedures remain recorded; captures are dated, not durable host state. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; C3 requires mismatches 0 at the measured round-37 tip; no ordinal uplift. | round 10; unchanged |
| adjacency | 8 | Finding-to-owner ADJ-01..07 table and portable OUT-001..010 anchors remain; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |

## Capabilities — current (round 37)

Append-only copy of the active round-35 capability rows, updated only for current evidence counts.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates where the lane learns: opened tier-scoped rows with anchors, rejections with flips, study paths, search log and unopened leads; checked by the frozen contract census commands | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` (historical snapshot) | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT pacnew-plane line, with a hermetic census selftest | `tools/tsukuroi-census.sh --selftest` prints PASS 105/105 rc=0; live run exits 1; historical receipts `.ufo/evidence/round-1-kaika/scout-live.md` and `after.md` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations even on package-probe failure; isolates fixtures and blocks unavailable or non-directory metadata without grading intentional 0555 policy | `.ufo/waves/round-12/resumed/after.json`, `selftest-after.json`, `mode-policy-mutant.json`; measured commit `70fede2a7a890cb50a72db2d4230ee541183bf7b` | round 12 |
| boot-chain-audit | Audits limine entries read-only: extracts initramfs, types new_root, binds firmware-selected entry and emits per-entry next-boot verdict | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt` (historical capture); selftest PASS total=45 failed=0 | round 17 |

## Axes — current self-assessment (round 37)

Correction to the immediately preceding round-37 axis table: the self-assessment parser requires the literal count phrases shown here. The preceding table is superseded; no historical round is rewritten. This table is the operative current assessment.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 56 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3110 `wc -l` / 839 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 49 files (`find corpus/lessons -type f | wc -l`); four standing rules near the top of SKILL cite no knowledge note; no ordinal move claimed. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 269 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes; four declared round-1 read-only surfaces link knowledge; pacnew census arm C1 was not verified in round 35, no coverage ordinal move. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (105 cases, 105 passed, 0 failed); live run exits 1 with six-plane rollup; `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; dated round-1 D1-D5 rechecks and current recheck procedures remain recorded; captures are dated, not durable host state. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; C3 requires mismatches 0 at the measured round-37 tip; no ordinal uplift. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |

## Capabilities — current (round 37)

Correction to the preceding round-37 capability table after K17/K18 showed that it named absent historical evidence paths. The preceding table is superseded. Paths below are individually backticked and known present at this measured revision.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates where the lane learns: opened tier-scoped rows with anchors, rejections with flips, study paths, search log and unopened leads; checked by the frozen contract census commands | `corpus/SOURCES.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT pacnew-plane line, with a hermetic census selftest | `tools/tsukuroi-census.sh` and `.ufo/evidence/round-1-kaika/scout-live.md` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations even on package-probe failure; isolates fixtures and blocks unavailable or non-directory metadata without grading intentional 0555 policy | `.ufo/waves/round-12/resumed/after.json` | round 12 |
| boot-chain-audit | Audits limine entries read-only: extracts initramfs, types new_root, binds firmware-selected entry and emits per-entry next-boot verdict | `tools/boot-chain-audit.sh` and `.ufo/waves/round-17/l1-capture/audit-live.txt` | round 17 |

### Round-37 capability evidence correction (append-only)

K17 requires the current host-census-gate capability row to state the selftest case count. The operative host-census-gate row above is superseded by this row; its cited paths are unchanged and present.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT pacnew-plane line, with a hermetic selftest that prints PASS (105 cases, 105 passed, 0 failed) | `tools/tsukuroi-census.sh` and `.ufo/evidence/round-1-kaika/scout-live.md` | lane r2; demonstrated fleet r1 |

## Capabilities — complete current table (round 37)

This full table supersedes the partial K17 correction row immediately above; all current capability rows are retained and their evidence paths are explicit. The case count is measured at the recorded revision.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates where the lane learns: opened tier-scoped rows with anchors, rejections with flips, study paths, search log and unopened leads; checked by frozen census commands | `corpus/SOURCES.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT line; hermetic selftest prints PASS (105 cases, 105 passed, 0 failed) | `tools/tsukuroi-census.sh` and `.ufo/evidence/round-1-kaika/scout-live.md` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations even on package-probe failure; isolates fixtures and blocks unavailable/non-directory metadata without grading intentional 0555 policy | `.ufo/waves/round-12/resumed/after.json` | round 12 |
| boot-chain-audit | Audits limine entries read-only: extracts initramfs, types new_root, binds firmware-selected entry and emits per-entry next-boot verdict | `tools/boot-chain-audit.sh` and `.ufo/waves/round-17/l1-capture/audit-live.txt` | round 17 |

### Round-37 source-pointer erratum (append-only; declaration pointer superseded)

The declaration's line “C1's probe note cites a strace(1) row (S200-strace) and own-work row (S201-probe)” is incorrect and is superseded. S200/S201 were assigned during errno assimilation to the mount(2) and Btrfs ioctl sources; they do not cite the probe. C1's claim evidence is the probe and its committed measurements, not an opened external SOURCES row. The §2b sourced-claim requirement is met by C2: its correction rests on existing mined row S199, re-opened and quoted in `corpus/knowledge/journalctl-v262-field-filter-r36.md`'s round-37 addendum and `corpus/lessons/round-37.md` Gate. No claim target, counter or kill rule changes.

## Axes — current self-assessment (round 37 final measured surface)

This current table supersedes the earlier round-37 count snapshots above; each count is re-derived from the committed lane tree at this section's measured revision. Ordinal values remain unchanged; the claim outcomes follow in the round-37 measured-outcome addendum.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 58 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3112 `wc -l` / 841 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 50 files (`find corpus/lessons -type f | wc -l`); four standing rules near the top of SKILL cite no knowledge note; no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 282 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes; four declared round-1 read-only surfaces link knowledge; no new coverage surface claimed. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (105 cases, 105 passed, 0 failed); live run exits 1 with six-plane rollup; `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; dated round-1 D1-D5 rechecks and current procedures remain recorded; captures are not durable host state. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; round-37 C3 requires mismatches 0 at this measured revision; no ordinal uplift. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |

## Round 37 — measured outcome (2026-10-25, author-side; closure verdict pending)

| Claim | Axis | Before → after measurement | Author verdict | Ordinal score delta |
|---|---|---|---|---|
| C1: V8 livefive counter executable and leak-discriminating on five tools | operability | V7 direct livefive at base `564db0b614b2914de5452f9ebd537a0653ae1de5`: exit 1, stdout 0 lines, `RuntimeError: cannot create local master branch` (`.ufo/waves/round-37/before/v7-livefive-base.err`). V8 command `python3 tools/probe-child-env-allowlist-r37.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision 564db0b614b2914de5452f9ebd537a0653ae1de5 --set livefive --scratch /tmp/tsukuroi-r37-v8-baseline` at instrument tip `29b22df142efb5479333af9d57ecbd069462ba05` (probe sha `9aee085b45d7566d6ce398733c10d3d87ae29bce107c4bd13fcdffcb4854b064`): 5 targets, 15 predicate pairs, `leaking=0`, `leaking_pairs=[]`, `harness_errors=[]`, exit 0 (`.ufo/waves/round-37/before/v8-livefive-baseline.jsonl`). | **NOT VERIFIED**: the declared kill rule requires V8 after-mutants for the four fixes; no committed sensitivity receipts were delivered. The after value is observed, but without those controls the claim's predeclared falsification condition has not been discharged. | 0 (no ordinal move) |
| C2: round-36 journalctl note correction-complete | depth | `python3 tools/check-journalctl-v262-corrections.py --revision 564db0b614b2914de5452f9ebd537a0653ae1de5`: 3 clusters, 15 mismatches, FAIL, exit 1 (`.ufo/waves/round-37/before/c2-before.json`). Same counter at `d621b7126e088824fed354e19839a9c1bd4e74f0`: 3 clusters, 0 mismatches, PASS, exit 0 (`.ufo/waves/round-37/after/c2-after-d621b7.json`); `--selftest` 7/7 PASS. | **VERIFIED** under the finite correction checker; no claim that it is a universal semantic parser. | 0 (no ordinal move) |
| C3: self-assessment matches the measured tree | calibration | `python3 tools/check-self-assessment.py --revision 564db0b614b2914de5452f9ebd537a0653ae1de5`: checked 27, mismatches 5, FAIL, exit 1 (`before/c3-before.json`). Same command at `29b22df142efb5479333af9d57ecbd069462ba05`: checked 27, mismatches 0, PASS, exit 0 (`after/c3-after-29b22d.json`). | **VERIFIED** for the checker’s fixed 27-check set at the measured revision. | 0 (no ordinal move) |

The operative current self-assessment table immediately above is measured at `29b22df142efb5479333af9d57ecbd069462ba05`: 58 knowledge notes, SKILL 3112 lines / 841 pipe lines, 50 lesson files and README 282 lines. Other axis ordinals remain depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. No ordinal uplift or host/package/service action is claimed.

### Round 37 — sourced-claim pointer

The round’s sourced claim is C2: existing mined row S199 was opened on 2026-10-25 and its located NEWS quote is recorded in the round-37 correction block and `corpus/lessons/round-37.md` Gate. C1’s planned S200-strace/S201-probe citation is superseded by the preceding source-pointer erratum and is not counted as a sourced claim.

### C3 final remeasurement

Re-run after the round-37 measured-outcome table and lesson were committed: `python3 tools/check-self-assessment.py --revision 6dbfe3274d8afecbfddd40d0c882a174238c638a` reports 27 checks, 0 mismatches, PASS, exit 0 (`.ufo/waves/round-37/after/c3-final-6dbfe.json`). This confirms the final current table at the measured outcome commit; later lane commits add only this receipt/LOG pointer and do not change the table or counted repository values.

### Round-37 assimilation declaration correction (append-only)

The declaration's statement that THREE staged entries were admitted, and its proposed package row ids S204/S205/S214/S220/S279-S282/S286/S287, is superseded by the Gate record. Actual staged disposition: `errno-contract-variance-r37.md` was admitted as the single staged entry; `errno-name-discrimination-r25.md` and the staged `mount-errno-contract-r26.md` were rejected. The lane-authored `mount-errno-contract-r37.md` is a corrected, separately authored note on the same theme, not a package entry. The eight newly appended lane rows are S200-S207, assigned by source document; the renumber map and source quotes are in `corpus/lessons/round-37.md` and `.ufo/waves/round-37/assimilation/SOURCES.append.md`. No axis claim predicate changes.

## Capabilities — current full evidence set (round 37, append-only repair)

This complete table restores the capability evidence pointers present in the prior current table; the shorter round-37 table above had dropped four still-present evidence paths. All pointers below use full repository paths and are confirmed present at the recorded lane tree.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates opened tier-scoped sources with anchors, rejections, paths, search log and unopened leads | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT line; selftest prints PASS (105 cases, 105 passed, 0 failed) | `tools/tsukuroi-census.sh`; `.ufo/evidence/round-1-kaika/scout-live.md`; `.ufo/evidence/round-1-kaika/after.md` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations while preserving fixture isolation and policy boundaries | `.ufo/waves/round-12/resumed/after.json`; `.ufo/waves/round-12/resumed/selftest-after.json`; `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | round 12 |
| boot-chain-audit | Reads and types initramfs root paths against the selected firmware entry, producing a per-entry next-boot verdict | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt` | round 17 |

## Round 37 — post-wave claim adjudication (author-side; no frozen predicates changed)

| Claim | Final author verdict | Evidence / reason |
|---|---|---|
| C1 (operability) | **not verified** | V8's 5-target/15-pair livefive receipt is clean, but the wave's C17 S4 mutant (V-B2) scores `leaking=0`, `harness_errors=[]`, exit 0 with a PATH derived through `shutil.which`; the V8-only `get_exec_path` source addition does not catch it. The declared sensitivity kill condition therefore fires; no V8 mutation receipts justify promotion. See `.ufo/waves/round-37/w1/C17S407.md:15-44` and the committed V8 receipt. |
| C2 (depth) | **not verified** | The finite checker passes 0 mismatches, but it does not assert the declared unchanged rejection-line invariant and its action override check is narrower than the review's order/output cases. The result does not certify the complete declared after-state. See `.ufo/waves/round-37/w1/Review1Causal153.md:60-83`, `Review2Causal254.md:7-10`, `C24ActionOverride12.md:34-80`, and `Build5C237.md:20-24`. |
| C3 (calibration) | **not verified** | The final fixed-27 checker reads 0 mismatches at the measured table, but the self-assessment count rows are coupled to C2/assimilation/lesson/README/SKILL commits, so the claim is not causally separable as frozen. The earlier current capability rows also dropped four existing evidence paths; this appended table restores them. See `.ufo/waves/round-37/w1/Review1Causal153.md:13-39`, `C31Ledger117.md:31-46`, `C34Ledger420.md:27-43`, and `C38Ledger824.md:102-120`. |

All three declared claims are reported honestly; the C2/C3 measurements did reach their counted values, but the reviewers identified missing predicate coverage and causal-separability defects. No ordinal score delta or round admission is claimed. Trend verdicts remain in the round report.

### Round 37 — attempt-2 re-measurement at lane tip `a3cf2efdc09939534fe3b51b1bff6779554b0a39` (no verdict change)

C2 counter: 0 mismatches, exit 0 (`.ufo/waves/round-37/attempt2/c2-at-a3cf2ef.json`). C3 counter: 27 checked, 0 mismatches, exit 0 (`.ufo/waves/round-37/attempt2/c3-at-a3cf2ef.json`). Census: 207 rows, exit 0. The post-wave adjudication above stands: C1, C2 and C3 are **not verified**, and no ordinal moves. Seat-report count is corrected to 62 of 64 (`attempt2/seat-report-count.txt`).

## Round 38 — declaration (fresh-start round, 2026-10-26T04:16Z, base `8bd001f58bfda29c92d90d2a7a413825c0ca9fcb`, before any seat)

Fresh-start round (hyaku run 8): rounds 34–37 were each closed `rejected-honest-stop` on an operability C1 whose
sensitivity or after-state conjunct was never delivered (`corpus/lessons/round-3{4,5,6,7}-verifier-spotcheck.md`).
This round declares two claims whose counters, fixtures, before receipts and do-nothing/junk controls are
committed before any seat or implementation. Lowest non-retired axes: depth 8 and adjacency 8 (tied); C2 works
depth. Saturation 9 / window 3 unchanged; the nudge does not waive the lowest-axis duty.

| Claim | Axis | Surface moved | Counter (frozen; sha256) | Before at base | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | coverage | Storage integrity (btrfs per-device error counters) moves Frontier → Core: the round-26 frontier rule (`corpus/README.md` "becomes Core only after a read-only census arm reads it") is met by a verdict-neutral census arm | `python3 tools/score-storage-arm-r38.py --revision <REV>` (sha256 `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`) | `fixtures_matched 0/10, live_match 0, six_planes_all 1`, FAIL exit 1 (`.ufo/waves/round-38/before/c1-before.json`) | `fixtures_matched == FIXTURES_EXPECTED and live_match == 1 and six_planes_all == 1` (10/10, live 1, six PLANE lines in every run), exit 0 | Any of: a fixture mismatches; the live STORAGE fields differ from the counter's own sysfs reading; any run prints other than six PLANE lines and one rollup; or `--selftest` of the census at the measured revision is not PASS with 0 failed (no-harm conjunct of operability). The counter bytes are never edited this round; a counter defect is reported, not repaired into a pass |
| C2 | depth (sourced) | Update-safety plane: the host's effective ALPM hook order (69 effective hooks from 70 files; override, suffix-ignoring order, phase positions, AbortOnFail/NeedsTargets, Exec) read from libalpm `hook.c` at pacman 54d9411 — the lane held only "override" and "HookDir precedence" (S007/S008), not the order rule | `python3 tools/check-hook-order-r38.py --revision <REV>` (sha256 `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`), input `.ufo/waves/round-38/frozen/hooks-capture/` pinned by MANIFEST sha256 `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd` | entry absent: `rows_matched 0/69, source_ok 0`, FAIL exit 1 (`.ufo/waves/round-38/before/c2-before.json`) | `rows_expected == rows_matched and mismatches == 0 and extra_rows == 0 and source_ok == 1`, exit 0 | Any of: the counter FAILs at the measured revision; the pacman.log run-order oracle (wave seat) finds a logged transaction whose `running '<hook>'` sequence contradicts the entry's positions; a cited S-row quote is absent from the opened source |

Controls, scored with the frozen counters before any seat (`.ufo/waves/round-38/controls/controls.jsonl`, script
`run-controls.sh` sha256 `cba1bec2c3e4130707c2d42e6dfebb0581cc2e23b369e84158b6e054fbfaf3ad`, scratch clone with
origin removed): C1 do-nothing 0/10 FAIL; C1 constant `state=HEALTHY 1/1/0` emitter 2/10 FAIL; C1 naive
nonzero-digit emitter 6/10 FAIL. C2 do-nothing 0/69 FAIL; full-name byte sort (suffix not ignored) 63/69 FAIL;
override ignored 66/69 FAIL; correct table without a sourced row FAIL (source_ok 0); correct table with a sourced
row PASS (the counter can pass). No control meets either target.

Causal separability: C1 touches `tools/tsukuroi-census.sh` and the storage frontier; C2 touches a new knowledge
entry and `corpus/SOURCES.md`; neither counter reads the other's surface. Sourced claim: C2 (rows for libalpm
`hook.c` and `alpm-hooks.5.asciidoc` at 54d9411, opened this round). The C1 verdict rules rest on held rows S128
and S133 (SH1/SH2 of `corpus/knowledge/storage-health-r26.md`). Measured revision: the lane branch tip named in the
round-38 outcome section, declared before the after-run; no self-assessment count is claimed this round.

## Round 38 — pre-seat amendment (2026-10-26T04:32Z, tightening only; no wave seat had scored)

Read after the freeze and after the author's own after-receipts (`.ufo/waves/round-38/after/c1-after-52ffd65.json`,
`c2-after-1fe28e7.json`, both PASS): the lane's own `corpus/QUALITY.md` criteria 80–82 bind these claims and the
declaration above did not meet them. This amendment only ADDS kill conditions; it cannot turn a failing claim
into a pass, and the v1 predicates above stay frozen and unchanged. If the closure rules that a post-receipt
addition is not the claims' rule, the v1 rules stand alone and the receipts below are evidence that the v1 C1
counter is gameable (QUALITY 82), reported as a counter defect, not hidden.

- **C1 / QUALITY 82 (R32-FIXTURE-GATEABLE).** The v1 counter drives the arm through `TSUKUROI_BTRFS_SYSFS`
  fixtures and its live leg has one constant answer on this host. Control receipt
  (`.ufo/waves/round-38/controls/controls-q82.jsonl`, script `run-controls-q82.sh` sha256
  `5469e59a5474881a2575a2f122e1bf278ea0c8e46ff925843dd494a634e4f5d6`): a **fixture-gated arm** (real logic only
  when the override is set, constant `HEALTHY 1/1/0` otherwise) scores **v1 PASS 10/10, live 1** — the v1 counter
  cannot tell it from the real arm. Added conjunct: `python3 tools/score-storage-arm-r38-q82.py --revision <REV>`
  (sha256 `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3`) runs the census with no override
  inside `unshare -rm` with a per-run random tree bind-mounted over the production path `/sys/fs/btrfs` (3 views:
  all-zero, forced-nonzero, random). Predicate `ns_views_matched == VIEWS and ns_available == 1`. Controls under it:
  fixture-gated 0/3 FAIL, cached-live 1/3 FAIL, real arm (`52ffd65`) 3/3 PASS. **C1 kill rule, added:** C1 is not
  verified unless the Q82 counter PASSes at the measured revision.
- **C2 / QUALITY 80–81.** Novelty swept as facts at base (`.ufo/waves/round-38/before/c2-novelty-sweep.txt`:
  0 base hits for `ignores the suffix`, `_alpm_hook_cmp`, `TRANS_HOOK_FAILED`, `failed to run transaction hooks`,
  `triggerless`, `AbortOnFail`, `PostTransaction hooks`, `hookdirs`, `alphabetical order`; the 11 `transaction
  completed` hits are pacman.log line quotes, not the HO6 rule). The scripted non-reader control is the full-name
  sort table (63/69, FAIL, `controls.jsonl`); the correct-table control PASSes because the table is rule-derived,
  so the table conjunct measures the order rule, not reading. **C2 kill rule, added (QUALITY 81 per-row
  verdict):** each rule row HO1–HO7 needs a committed reviewer verdict file from a seat that did not write the
  entry (wave items C2RevHookC, C2RevOtherSrc, C2CritHO5, C2CritHO6, C2RevenConf); any HO row judged false against
  the pinned source at its cited lines kills C2. Per LEARNING.md a dispatched seat is still the lane, so these
  verdicts are author-side; the closure's re-open is the non-author check.

## Round 38 — measured outcome (2026-10-26, author-side; non-author closure pending)

Measured revision: `b0005ae9f56fd5a006fc5ec026578c88e2b64b26` (lane tip before this section; this append and the LOG
entry change no file either counter or the self-assessment counts read). Receipts under `.ufo/waves/round-38/after/`.

| Claim | Axis | Before (base `8bd001f5`) | After (`b0005ae9`) | Kill rules | Author verdict | Ordinal |
|---|---|---|---|---|---|---|
| C1 storage counters Frontier → Core | coverage | v1 `fixtures_matched 0/10, live_match 0`, FAIL exit 1 (`before/c1-before.json`) | v1 10/10, live 1, six 1, PASS exit 0 (`after/c1-final-b0005ae.json`); amendment conjunct Q82 `ns_views_matched 3/3`, PASS exit 0 (`after/c1-q82-final-b0005ae.json`); census `--selftest` PASS 113/113 (`after/selftest-final-b0005ae.txt`) | none fired: fixtures, live leg, plane count, selftest and Q82 all hold | **verified under the frozen predicate and the pre-seat conjunct**, with two recorded counter defects: the v1 counter alone admits a fixture-gated arm (closed by Q82) and the Q82 counter admits four adversarial arms that read the view tree through leaked paths (`w1/Q82Attack.md`; lesson R38-Q82-LEAK, next-round fix). Known semantic limit: an absent sysfs root reads HEALTHY 0/0/0 (R38-ABSENT-ROOT) | coverage 9 → 9 (no ordinal uplift) |
| C2 effective ALPM hook order | depth (sourced: S208–S212) | entry absent, `rows_matched 0/69`, `source_ok 0`, FAIL exit 1 (`before/c2-before.json`) | 69/69, mismatches 0, extra 0, `source_ok 1`, PASS exit 0 (`after/c2-final-b0005ae.json`) | none fired: pacman.log oracle 60 transactions, 109 phases, 0 violations (`w1/C2ExecLogOracle.md`); no HO row judged false (HO5, HO6 partly hold in host cells, corrected append-only in the entry) | **verified**; counter gaps recorded: a stripped entry citing only S212 also passes (`w1/CritControlsC2.md`), and dropping an S-id from `source:` survives (`w1/C2MutEntry.md`) — the HO rows are judged by the per-row rule, not by the counter | depth 8 → 8 (no ordinal uplift) |

Causal separability re-checked by `w1/CritSeparability.md` (each predicate passes with the other claim absent). No
axis harmed: `w1/RevNoHarmAxes.md`; the adjacency-anchors gate red caused by the census line shift was repaired in
`02eeed07` (lesson R38-ANCHOR-SHIFT); the frozen round-35 probe `score-pacnew-arm-r35b.py` now reads base-parity
failures at post-`52ffd65` revisions by construction (recorded in `SKILL.md` "Storage integrity arm — round 38").
Sources: 207 → 212 rows, `sources-census.sh validate` exit 0 (`after/sources-census-final.txt`). Assimilation:
none admitted (two staged candidates refused, `corpus/lessons/round-38.md` Gate).

## Axes — current self-assessment (round 38 final measured surface)

Each count is re-derived from the committed lane tree at `b0005ae9`; ordinals unchanged.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 59 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3201 `wc -l` / 861 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 52 files (`find corpus/lessons -type f | wc -l`); round-38 C2 verified, no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 301 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus the verdict-neutral STORAGE line (btrfs error counters moved to Core, round 38 C1). | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (113 cases, 113 passed, 0 failed); live run exits 1 with six-plane rollup; `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; dated round-1 D1-D5 rechecks and current procedures remain recorded; captures are not durable host state. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; mismatches 0 required at the round-38 tip. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |

## Capabilities — current full evidence set (round 38)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates opened tier-scoped sources with anchors, rejections, paths, search log and unopened leads | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT and STORAGE lines; selftest prints PASS (113 cases, 113 passed, 0 failed) | `tools/tsukuroi-census.sh`; `.ufo/evidence/round-1-kaika/scout-live.md`; `.ufo/evidence/round-1-kaika/after.md` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations while preserving fixture isolation and policy boundaries | `.ufo/waves/round-12/resumed/after.json`; `.ufo/waves/round-12/resumed/selftest-after.json`; `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | round 12 |
| boot-chain-audit | Reads and types initramfs root paths against the selected firmware entry, producing a per-entry next-boot verdict | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt` | round 17 |
| storage-error-counter-reader | Reads every btrfs device's five error counters from sysfs and prints one verdict-neutral STORAGE line (HEALTHY/DEGRADED/BLOCKED with nonzero pairs and reason tokens), demonstrated on fixtures, the live host and production-path namespace views | `tools/tsukuroi-census.sh`; `.ufo/waves/round-38/after/c1-final-b0005ae.json`; `.ufo/waves/round-38/after/c1-q82-final-b0005ae.json` | round 38 |

- **planned (next round):** fix the Q82 view leak (tmpfs-built views inside the namespace, the four `Q82Attack` arms as
  committed should-fail controls) and the absent-root rule (a `/proc/self/mounts` cross-check under a new frozen counter);
  adjacency (lowest with depth at 8) via a sibling acknowledgement of the storage/hook boundary.
- **retired:** none.

## Round 39 — declaration (2026-10-26T06:20Z, base `0eff65b21bb81195ee06c96a83afbd7a07e52eef`, before any seat)

Round 38 was admitted (`corpus/lessons/round-38-verifier-spotcheck.md`). This round takes the planned row: the two
storage-arm defects that closure routed (§6.1 R38-Q82-LEAK, §6.2 R38-ABSENT-ROOT) and one depth claim. Lowest
non-retired axes: depth 8 and adjacency 8 (tied); C2 works depth. Saturation 9 / window 3 unchanged. Counters,
frozen inputs and registry rows landed first in freeze commit `6a08925daa30767809eb13bb4b01448ff954d46a`; the before
receipts were written by `tools/run-receipt.py` at the base with `--tool-revision 6a08925d`, so each names the
revision, the tool and its sha256 (routed defect §6.5).

| Claim | Axis | Surface moved | Counter (frozen; sha256) | Before at base | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | operability | The census STORAGE arm stops reading a hidden or absent btrfs sysfs root as a clean disk: with no fsid under the root and a btrfs mount in the mount table (`TSUKUROI_PROC_MOUNTS`, default `/proc/self/mounts`) it prints `state=BLOCKED … detail=mounts:btrfs-without-sysfs`; an unreadable table prints `detail=mounts:unreadable`. Its production-path views are tmpfs mounts built inside the child namespace from stdin (no host path) | `python3 tools/score-storage-hidden-r39.py --revision <REV>` (sha256 `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`) | `hidden_matched 0, views_matched 3, fixtures_matched 2, live_match 1, six_planes_all 1`, FAIL exit 1 — both hidden legs read `HEALTHY 0/0/0` (`.ufo/waves/round-39/before/c1-before.jsonl`) | `hidden_matched == 2 and views_matched == 3 and fixtures_matched == 5 and live_match == 1 and six_planes_all == 1`, exit 0 | Any of: a hidden leg, view, fixture or the live leg mismatches; a run prints other than six PLANE lines; the census `--selftest` fails any case; any of the four round-38 Q82 leak arms ported onto the C1 commit PASSES the counter (they must fail the views conjunct) |
| C2 | depth (sourced) | Update-safety plane: the libalpm transaction order TO1–TO8 at pacman 54d9411 — Pre hooks before `transaction started`, removals before adds, per-package scriptlet/file/log order, scriptlet arguments, hook directories re-read per phase, `ldconfig` once, removal order, and `ALPM-SCRIPTLET` as the tag of every chroot child's output — in `corpus/knowledge/pacman-transaction-order-r39.md` on rows opened this round | `python3 tools/check-transaction-order-r39.py --revision <REV>` (sha256 `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`), snapshots `.ufo/waves/round-39/frozen/src/` and capture `.ufo/waves/round-39/frozen/txcapture/` (MANIFEST sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4`) | entry absent: `rules_verified 0, source_ok 0, counts_ok 0`, FAIL exit 1 (`.ufo/waves/round-39/before/c2-before.jsonl`) | `rules_verified == 8 and duplicate_rows == 0 and duplicate_headings == 0 and source_ok == 1 and counts_ok == 2 and oracle_violations == 0`, exit 0 | Any of: the counter fails; a `running` line inside a commit phase (oracle); **any TO row judged false against the pinned source at its cited lines by a wave reviewer seat (QUALITY 81 per-row verdict; the counter checks that the quote is at the lines, not that the rule is true)** |

Controls, scored with the frozen counters before any seat (`.ufo/waves/round-39/controls/controls.jsonl`; script
`run-controls.sh` + `c1_variant.py`, scratch clone with origin removed; entry variants under `controls/c2-entries/`):
C1 do-nothing (base) hidden 0/2, fixtures 2/5 FAIL; fixture-gated cross-check (only when the override is set) hidden
0/2 FAIL; over-block (BLOCKED on every empty root) fixtures 4/5 FAIL; mountinfo-keyed (detects the counter's tmpfs
instead of reading btrfs mounts) fixtures 2/5 FAIL; candidate PASS. C2 do-nothing 0/8 FAIL; rows citing only the
own-work row 0/8 FAIL; line references shifted by 40 0/8 FAIL; S213 dropped from `source:` 5/8 FAIL; rules block
duplicated (8 rows, 1 heading) FAIL; host counts wrong (counts_ok 0) FAIL; candidate PASS. The three round-38 C2
counter gaps (§6.3) are the E1, E3 and E4 controls. No control meets either target.

Predicted side effect, declared now: the round-38 v1 counter's fixture F06 (absent root under the override, real
`/proc/self/mounts` listing btrfs) encodes the superseded R38-ABSENT-ROOT rule, so at post-C1 revisions it reads
BLOCKED and `score-storage-arm-r38.py` FAILs 9/10 by construction; the round-38 claim stays measured at `b0005ae9`.

Causal separability: C1 touches `tools/tsukuroi-census.sh` (and the IN-109 anchor its line shift moves); C2 touches a
new knowledge entry and `corpus/SOURCES.md`; neither counter reads the other's surface. Sourced claim: C2 (S213–S218
opened this round; S217 is the `supersedes S210 —` row the round-38 closure routed, §6.4). Measured revision: the
lane branch tip named in the round-39 outcome section, declared before the after-run.

## Round 39 — measured outcome (2026-10-26, author-side; non-author closure pending)

Measured revision: `a2d7aad740977088ff9fc70ed36d3ef978b27e81` (integration commit after the 70-seat wave; this section,
the LOG entry and the final receipts change no file either counter reads). Receipts under `.ufo/waves/round-39/after/`,
each written by `tools/run-receipt.py` (revision, tool, tool_sha256, tool_revision `6a08925d`).

| Claim | Axis | Before (base `0eff65b2`) | After | Kill rules | Author verdict | Ordinal |
|---|---|---|---|---|---|---|
| C1 hidden or absent sysfs root is not a clean disk | operability | hidden 0/2, views 3/3, fixtures 2/5, live 1, six 1, FAIL exit 1 (`before/c1-before.jsonl`) | hidden 2/2, views 3/3, fixtures 5/5, live 1, six 1, PASS exit 0 at `49cc53c7` (`after/c1-after-49cc53c.jsonl`) and at `a2d7aad7` (`after/c1-final-a2d7aad.jsonl`); census `--selftest` PASS 119/119 (`after/selftest-final-a2d7aad.txt`) | none fired: every leg matched; six PLANE lines in every run; selftest 119/119; the four round-38 leak arms on `49cc53c7` all FAIL (views 0/3, 1/3, 0/3, 0/3; `w1/C1LeakArms/scores.jsonl`) | **verified under the frozen predicate and kill rules**, with three recorded counter-sensitivity defects: arms keyed on a literal common to every fixture (`subvolid=256`, `/dev/mapper/root`) also PASS (`w1/C1CritControl.md`; lesson R39-FIXTURE-MONOCULTURE, QUALITY 87); an arm that detects the namespace and lies only on the host's constant live answer PASSes (`w1/C1DetectHonest.md`; unclosable read-only on this host, `PROVINCE.md` remaining limit); the views conjunct had no pre-data control (R39-VIEW-CONTROL-UNREACHABLE; the wave's leak arms show it moves). Post-wave hardening (FIFO or empty mount table → `mounts:unreadable`, `w1/C1SentMounts.md`) landed in `a2d7aad7` and the predicate was re-measured there | operability 9 → 9 (no ordinal uplift) |
| C2 libalpm transaction order TO1–TO8 | depth (sourced: S208, S213–S218) | entry absent, `rules_verified 0, source_ok 0, counts_ok 0`, FAIL exit 1 (`before/c2-before.jsonl`) | 8/8, duplicates 0/0, `source_ok 1`, `counts_ok 2`, oracle 0, PASS exit 0 at `4078eb23` (`after/c2-after-4078eb2.jsonl`) and at `a2d7aad7` (`after/c2-final-a2d7aad.jsonl`) | none fired: no TO row judged false (eight rows `holds` from C2RevTransSync, C2RevAddC, C2RevRemoveUtil, C2RevHookC, C2ExecLogOracle, C2RevSourcesRows; `partly` on TO3 completeness and TO5's host column, both corrected append-only in the entry); 0 `running` lines inside a commit phase | **predicate met, but the target is defective**: the counter never reads the rule cell, so an entry with no rule text (or the opposite rule) and the same citations scores 8/8 PASS (`w1/C2CritAxis.md` X-empty, X-false; `w1/C2CritControl.md`). By the claim-sizing rule the counter alone does not establish the depth move; the rule content rests on the per-row reviewer verdicts. Reported for the closure to rule (lesson R39-CONTENT-UNREAD, QUALITY 87) | depth 8 → 8 |

Causal separability: `w1/CritSeparability.md` (each counter passes with only its own commit on the declaration and fails
without it). No-harm: `w1/RevNoHarmAxes.md` (all six axes); lane gates at `a2d7aad7` — registry-coverage, knowledge-header,
adjacency-anchors (IN-109 repinned 2425 → 2452), section-citations, appended-notices, boot-writers, recheck-commands all
PASS exit 0 (`after/gates-final-a2d7aad.txt`); self-assessment: see the table below and `after/self-assessment-final.json`.
Declared side effect observed: the round-38 v1 counter's F06 reads BLOCKED after `49cc53c7` (`w1/C1ExecR38Counters.md`,
`w1/C1CritAxis.md`), pinned historical in `SKILL.md` "Historical instrument pins — round 39". Sources: 212 → 218 rows,
census exit 0 (`after/sources-census-final.txt`). Assimilation: the staged `pacman-hook-timing-r25.md` is admitted by
re-grounding only (no staged row, id or text adopted), its interpretive sentences rejected (`corpus/lessons/round-39.md`
Gate).

## Axes — current self-assessment (round 39 final measured surface)

Each count is re-derived from the committed lane tree at the round-39 LOG/SCORECARD commit; ordinals unchanged.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 60 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3322 `wc -l` / 885 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 54 files (`find corpus/lessons -type f | wc -l`); round-39 C2 predicate met with a target defect, no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 317 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus the verdict-neutral STORAGE line, whose absent-root reading now cross-checks the mount table (round 39 C1). | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (119 cases, 119 passed, 0 failed); live run exits with the six-plane rollup; `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; round 39 re-opened libalpm at 54d9411 for six files and corrected TO1/TO8 statements in seven older notes append-only. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; mismatches 0 required at the round-39 tip (the round-38 K10 red, lessons 52 → 53 from the round-38 spot-check, is repaired by this table). | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; recipient acknowledgement and independent replay are unverified; round-39 sibling sweep found no crossing (`.ufo/waves/round-39/w1/ConnSiblings.md`). | fleet round 1; unchanged |

## Capabilities — current full evidence set (round 39)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates opened tier-scoped sources with anchors, rejections, paths, search log and unopened leads | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT and STORAGE lines; selftest prints PASS (119 cases, 119 passed, 0 failed) | `tools/tsukuroi-census.sh`; `.ufo/evidence/round-1-kaika/scout-live.md`; `.ufo/evidence/round-1-kaika/after.md` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations while preserving fixture isolation and policy boundaries | `.ufo/waves/round-12/resumed/after.json`; `.ufo/waves/round-12/resumed/selftest-after.json`; `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | round 12 |
| boot-chain-audit | Reads and types initramfs root paths against the selected firmware entry, producing a per-entry next-boot verdict | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt` | round 17 |
| storage-error-counter-reader | Reads every btrfs device's five error counters from sysfs and prints one verdict-neutral STORAGE line (HEALTHY/DEGRADED/BLOCKED with nonzero pairs and reason tokens), demonstrated on fixtures, the live host and production-path namespace views; since round 39 an absent or empty root is cross-checked against the mount table | `tools/tsukuroi-census.sh`; `.ufo/waves/round-38/after/c1-final-b0005ae.json`; `.ufo/waves/round-38/after/c1-q82-final-b0005ae.json`; `.ufo/waves/round-39/after/c1-final-a2d7aad.jsonl` | round 38 |

- **planned (next round):** a C2 counter amendment that reads the rule cell (QUALITY 87: a required proposition token per TO
  row and the frozen X-empty / X-false fixtures as should-fail controls) plus the residual staged propositions
  (`NeedsTargets` on stdin, `.pacnew` trigger target, scriptlet cwd, interpreter) on new rows from S219; for C1, mount-table
  fixtures that vary device, subvolume and option literals (QUALITY 87 b); adjacency (tied lowest with depth at 8).
- **retired:** none.

## Round 40 — declaration (2026-10-26, base `53b294a274656be6479aadf2ec2fee890ded77ce`, before any seat)

Round 39 was admitted (`corpus/lessons/round-39-verifier-spotcheck.md` §4). This round takes the planned row: the two
counter defects that closure routed (§6.1 R39-CONTENT-UNREAD, §6.2 R39-FIXTURE-MONOCULTURE), the residual staged
propositions on new rows from S219, and no adjacency claim (a sibling acknowledgement cannot be produced by this lane;
adjacency stays unclaimed and is not harmed). Lowest non-retired axes: depth 8 and adjacency 8 (tied); C2 works depth.
Saturation 9 / window 3 unchanged. Counters, pinned sources, the host capture and the two registry rows landed first in
freeze commit `a447b67b2502bae1e96fda341ae5ad32243ae524`. Every timestamp in this section is the time it was written;
the commit time is the authority (round-39 routed defect §6.3).

| Claim | Axis | Surface moved | Counter (frozen; sha256) | Before at base | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | operability | The census `--selftest` (`tools/tsukuroi-census.sh` `run_selftest`, not `probe_storage_arm`) gains mount-table fixtures that vary device, mountpoint, options, subvolume, line position and fstype case, plus an unlistable root with btrfs mounted, so the literal-keyed and guard arms of the round-39 STORAGE cross-check fail it | `python3 tools/score-selftest-literals-r40.py --revision <REV> --scratch <DIR>` (sha256 `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159`): nine frozen mutants M1–M9 (round-39 VA, VB, VC, VG, MutParse (a), (b), MutCrossCheck (e), plus `subvol=/@`-keyed and last-line-only), three neutral rewrites, self-reference guard | `baseline_pass 1, neutral_pass 3, mutants_applied 9, survivors 9, selfref 5`, FAIL exit 1 (`.ufo/waves/round-40/controls/controls.jsonl` C1-K0) | `baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and survivors == 0 and selfref == 5` | any surviving mutant, a failing neutral rewrite or baseline, an unappliable mutant (the arm itself changed), or `selfref != 5` at the measured revision; a held-out literal-keyed mutant that a wave seat writes and the selftest lets through is reported as a counter-sufficiency defect, not a kill |
| C2 | depth (sourced) | Update-safety plane: what a hook command or install scriptlet finds when it starts (pacman 54d9411 as built by Arch 7.1.0.r9.g54d9411-3) — EX1 working directory `/`, EX2 merged stdout/stderr and stdin end-of-file, EX3 `SHLVL`/`BASH_ENV`/umask 0022, EX4 scriptlet shell `/usr/bin/bash` (upstream default `/bin/sh`), EX5 `tmp/alpm_XXXXXX/.INSTALL` staging, EX6 `NeedsTargets` stdin sorted and de-duplicated, EX7 `running` logged before `Depends` is checked, EX8 `Path` triggers on file-list names (NoExtract skipped, NoUpgrade ignored) — in `corpus/knowledge/pacman-exec-environment-r40.md` on rows S219–S225 opened this round | `python3 tools/check-exec-environment-r40.py --revision <REV>` (sha256 `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d`); reads the RULE cell (source-derived value, frozen proposition tokens, negation words, paraphrase) — QUALITY 87 | entry absent, `rules_verified 0, source_ok 0, counts_ok 0, novelty_base_hits 0`, FAIL exit 1 (controls C2-K0) | `rules_verified == 8 and duplicate_rows == 0 and duplicate_headings == 0 and source_ok == 1 and counts_ok == 2 and novelty_base_hits == 0` | any EX row judged `fails` against its pinned source lines by a wave reviewer (with lines), or an Arch packaging patch shown to change a cited line, or the predicate FAIL at the measured revision |

Controls, scored with the frozen counters before any seat (`.ufo/waves/round-40/controls/controls.jsonl`, script
`run_controls.py`, scratch clones with origin removed; candidate files digested in `candidate-sha256.txt`):
C2 do-nothing (base) FAIL; X-empty (rule cells `RULE NOT SUPPLIED`, source/value/host kept) 0/8 FAIL; X-false by
negation 0/8 FAIL; X-false by wrong values 0/8 FAIL; own-work-only sources 0/8 FAIL; rows re-pointed to the held rows
S208/S216/S217 0/8 FAIL; scripted writer (quote copied as the rule plus every frozen token) 0/8 FAIL; rules block
duplicated FAIL; candidate PASS. C1 do-nothing (base) survivors 9 FAIL; five added cases of the one round-39 literal
shape (QUALITY 87 b) survivors 9 FAIL; self-reading selftest FAIL (selfref 6, and its own baseline fails — this arm does
not isolate the self-reference guard; recorded, a wave item attacks it); arm rewritten instead of the selftest
(mutants unappliable 2/9) FAIL; candidate PASS. No control meets either target.

Equivalent mutant, excluded and named in the counter: guard `$fsn` → `$devn` (round-39 MutCrossCheck (d)); `devn > 0`
implies `fsn > 0`, and `fsn > 0` with `devn == 0` sets `blocked=1` (no-devinfo) before the guard.

Causal separability: C1 touches only `run_selftest` in `tools/tsukuroi-census.sh`; C2 touches a new knowledge entry
and `corpus/SOURCES.md`; neither counter reads the other's surface. Sourced claim: C2 (S219–S225 opened this round).
Measured revision: the lane branch tip named in the round-40 outcome section.

### Round 39 — gates-receipt disclosure correction (append-only; round-39 closure §6 item 4, `corpus/lessons/round-39-verifier-spotcheck.md:189`)

Appended by round-40 seat RoutedGatesRow. This adds a disclosure; no earlier line is rewritten.

The round-39 measured-outcome paragraph names seven gates "all PASS exit 0" and cites `after/gates-final-a2d7aad.txt`
(`SCORECARD.md:2253-2255`). The cited receipt holds eight gate rows. Its eighth, `:2`, is `check-self-assessment rc=1`,
and that 427-byte line ends inside the first `checks` entry, so the row carries the header fields but not the seven
check ids:

> `check-self-assessment rc=1 {  "revision": "a2d7aad740977088ff9fc70ed36d3ef978b27e81",  "checked": 27,  "mismatches": 7,  "status": "FAIL",  "declaring_round": 38,  "axes_heading": "## Axes \u2014 current self-assessment (round 38 final measured surface)",  "reference_lines": 444,  "checks": [   {    "id": "K01",    "subject": "depth score equals the after-value of the last recorded depth ordinal transition",    "stated": 8,`

(`.ufo/waves/round-39/after/gates-final-a2d7aad.txt:2`, quoted to end of line.) The other seven rows are `rc=0`
(`:1`, `:3`-`:8`). One row of the eight was therefore red in the file the sentence cited.

Why it was red: `a2d7aad7` precedes `eeba342e`, the commit that appended the round-39 axes table (heading
`## Axes — current self-assessment (round 39 final measured surface)`, `:2262`). At `a2d7aad7` the last axes table on
file was still the round-38 one at `:2181`, with count cells 59 notes, 3201 `SKILL.md` lines, 861 table lines, 52
lesson files, 301 `corpus/README.md` lines and 113 census cases (`:2187-2189`, `:2199`); the checker compared those
stale cells with the round-39 tree and reported seven mismatches — K07 59 against 60, K08 3201 against 3322, K09 861
against 885, K10 52 against 54, K11 301 against 317, K13 and K17 113 against 119. Re-running the same tool at
`a2d7aad7` in round 40 reproduces `checked 27, mismatches 7, FAIL`, exit 1, with exactly those seven ids
(`python3 tools/check-self-assessment.py --revision a2d7aad740977088ff9fc70ed36d3ef978b27e81`; receipt
`.ufo/waves/round-40/w1/RoutedGatesRow/check-a2d7aad.json`).

The final self-assessment run is green: `after/self-assessment-final.json:2-6` reads
`"revision": "eeba342ea06ad0069899b3b8b4bbea6af98df610"`, `"checked": 27`, `"mismatches": 0`, `"status": "PASS"`,
`"declaring_round": 39`, and a round-40 re-run at `eeba342e` reproduced those fields equal dict-for-dict
(`check-eeba342.json`). The red row is a pre-`eeba342e` artefact of the stale round-38 table, not an overclaim in the
round-39 records.

Two limits, stated rather than implied. First, the calibration row's parenthetical at `:2272` names only K10 and states
lessons 52 → 53, while the receipt's red is seven checks (listed above) and the observed lesson count at `a2d7aad7` is
54. Second, this section records round 39 only: the round-39 table is stale at the round-40 tip by construction, because round 40 has not yet appended its own table, and no green-at-tip claim is made here. Line numbers in this section are those of the tree before the section was inserted; `:2262` and `:2272` shift by its length.

### Round-39 receipt-provenance scoping correction (append-only; routed defect §6.5)

The measured-outcome paragraph at `SCORECARD.md:2245` says "Receipts under `.ufo/waves/round-39/after/`, each written
by `tools/run-receipt.py` (revision, tool, tool_sha256, tool_revision `6a08925d`)". The universal quantifier is wrong
and that reading is superseded; no file and no measurement changes. The check is
`for f in .ufo/waves/round-39/after/*; do head -1 "$f" | grep -o tool_sha256 || echo NO-HEADER; done`: 4 hits, 5
`NO-HEADER`, over 9 files. The sentence was already false when written, not merely overtaken: `git ls-tree` at
`eeba342e`, the commit that introduced it, lists 7 files, of which `gates-final-a2d7aad.txt`,
`selftest-49cc53c.txt` and `selftest-final-a2d7aad.txt` had no header.

Scoped correctly, the evidence classes are:

- **Four `tools/run-receipt.py` receipts**, fully bound: `after/c1-after-49cc53c.jsonl`,
  `after/c1-final-a2d7aad.jsonl` (tool `tools/score-storage-hidden-r39.py`, `tool_sha256`
  `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`), `after/c2-after-4078eb2.jsonl`,
  `after/c2-final-a2d7aad.jsonl` (tool `tools/check-transaction-order-r39.py`, `tool_sha256`
  `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`). Each header names the measured `revision`,
  `tool_revision` `6a08925daa30767809eb13bb4b01448ff954d46a`, the tool and its digest, and each footer carries
  `exit_code`; both digests equal the tool bytes at `6a08925d`.
- **Four direct tool-output captures with no tool digest**, each naming the revision it measured in content:
  `after/gates-final-a2d7aad.txt` (8 gate rows, every row naming `a2d7aad740977088ff9fc70ed36d3ef978b27e81`, five as
  `revision` and three as `branch_tip`), `after/self-assessment-final.json` (`"revision"` and `"requested_revision"`
  `eeba342ea06ad0069899b3b8b4bbea6af98df610`, 27 checked, 0 mismatches), `after/selftest-final-a2d7aad.txt` (line 1
  names `a2d7aad7` and `PASS (119 cases, 119 passed, 0 failed)`), and `after/sources-census-final.txt` (line 1 names
  the command and lane tip `eeba342e`).
- **One capture that names no revision in content**: `after/selftest-49cc53c.txt`, a single line
  (`PASS (117 cases, 117 passed, 0 failed)`) whose only revision hint is the 7-hex filename. It is not cited by the
  round-39 outcome section, so no claimed number rests on it.

Two of the file names disagree with the revision their content measures: `self-assessment-final.json` and
`sources-census-final.txt` are named `-a2d7aad` and measure `eeba342e`. The `a2d7aad7` self-assessment reading is the
second row of `gates-final-a2d7aad.txt` (`check-self-assessment rc=1`, 7 mismatches), superseded at `eeba342e` as
§6.4 records.

Read for scope, the sentence at `SCORECARD.md:2215-2216` ("the before receipts were written by
`tools/run-receipt.py` … so each names the revision, the tool and its sha256") is bounded the same way: of the three
files in `before/`, `c1-before.jsonl` and `c2-before.jsonl` are headered bindings to the frozen counters, and
`before/sources-census-start.txt` is a fleet-script capture with no header and no tool digest.

No claim measurement, counter, frozen predicate, kill rule, axis ordinal or capability row changes; the four receipts
the outcome table cites for C1 and C2 are unchanged and remain bound to the frozen tool bytes.

Erratum: the round-39 declaration heading above states 2026-10-26T06:20Z but its commit `93fddb2c` is committed 2026-10-26T05:59:31Z, and the round-40 declaration heading states no clock time; the commit time is the authority (R40-HEADING-TIMES, LOG entry; drafted by wave seat RoutedTimestamps).

## Round 40 — measured outcome (2026-10-26, author-side; non-author closure pending)

Measured revisions: C1 at `c707e356c2911646f7304d706eb77d118e510610` (implementation) and C2 at
`bf2380503b8e4a5d33162026854b0b7b66d18b86` (implementation), both re-measured at the integration commit
`aad01138d544878a64ff97927708c94a79432a3a`. Every claim receipt is a `tools/run-receipt.py` receipt (header: revision,
tool, tool_sha256, tool_revision `a447b67b`); gate receipts carry the header with the gate's own revision.

| Claim | Axis | Before (base `53b294a2`) | After | Kill rules | Author verdict | Ordinal |
|---|---|---|---|---|---|---|
| C1 selftest kills the literal-keyed and guard mutants | operability | `baseline_pass 1, neutral_pass 3, mutants_applied 9, survivors 9, selfref 5`, FAIL exit 1 (`before/c1-before.jsonl`) | `survivors 0`, baseline `PASS (124 cases, 124 passed, 0 failed)`, neutral 3/3, applied 9/9, selfref 5, PASS exit 0 at `c707e35` (`after/c1-after-c707e35.jsonl`) and at `aad01138` (`after/c1-final-aad0113.jsonl`); re-run by seats C1ExecRerun, C1RevCounter, C1CritAxis | none fired: no frozen mutant survives, baseline and neutrals pass, selfref 5; the arm is byte-identical to the base (`w1/C1ExecR39Counters.md`) and the round-39 C1 counter still PASSes | **verified under the frozen predicate**, with counter-sufficiency defects recorded (R40-ANSWER-KEY): a one-line prologue reading the arm (`declare -f`, `${0}`, `${BASH_ARGV0}`) passes with no fixture (`w1/C1CritControl.md`); held-out mutants H5, H6, H9 survive but key on properties every kernel-produced btrfs line has (`w1/C1HeldOutMutants.md`); M6 is killed only by a forged `BTRFS` table (`w1/C1CritEquivalence.md`) | 9 → 9 |
| C2 libalpm exec environment EX1–EX8 | depth (sourced: S219–S225; S226 added by the corrections) | entry absent, `rules_verified 0, source_ok 0, counts_ok 0, novelty_base_hits 0`, FAIL exit 1 (`before/c2-before.jsonl`) | `rules_verified 8, source_ok 1, counts_ok 2, novelty_base_hits 0`, no duplicates, PASS exit 0 at `bf23805` (`after/c2-after-bf23805.jsonl`) and at `aad01138` (`after/c2-final-aad0113.jsonl`) | none fired: no row judged `fails` (per-row reviewers C2RevEX1–EX8: EX1–EX4 and EX6–EX8 `supports`, EX5 `partly`); no packaging patch changes a cited statement (`w1/C2RevenPatches.md`; one patch shifts util.c lines after :675 by +5, appended to the entry) | **predicate met; the counter's content check is falsified** (R40-ANSWER-KEY): a token-list writer and affirmatively false rules pass it (`w1/C2CritControl.md`, `w1/C2CritXFalse.md`), so depth rests on the per-row verdicts — EX1, EX2, EX3, EX6 hold; EX4, EX5, EX7, EX8 partly, corrected append-only (EX5's `/tmp is a tmpfs` host sentence withdrawn as false; EX4 removal arguments; EX7 lookup time and Post `AbortOnFail`; EX8 install-versus-upgrade match) | 8 → 8 |

Causal separability: `w1/CritSeparability.md` (each counter PASSes with only its own commit cherry-picked onto the
declaration and FAILs without it). No-harm: `w1/RevNoHarmAxes.md` (additions only across the five round commits);
lane gates at `aad01138` — section-citations, appended-notices, recheck-commands, adjacency-anchors, boot-writers,
registry-coverage, knowledge-header all exit 0 (`after/gate-*-aad0113.jsonl`), round-39 C2 counter exit 0
(`after/r39-c2-aad0113.jsonl`); self-assessment: see the table below and `after/self-assessment-final.jsonl`.
Sources: 218 → 226 rows, census exit 0 (`after/sources-census-final.txt`). Assimilation: four staged residual
propositions of `pacman-hook-timing-r25.md` admitted by re-grounding (one with correction), one inference rejected; no
staged row, id or text adopted (`corpus/lessons/round-40.md` Gate). Evidence weight: `.ufo/waves/round-40/` about 4 MB,
no file above 2 MB.

## Axes — current self-assessment (round 40 final measured surface)

Each count is re-derived from the committed lane tree at the round-40 integration commit `aad01138`; ordinals unchanged.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 61 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3559 `wc -l` / 928 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 56 files (`find corpus/lessons -type f | wc -l`); round-40 C2 predicate met with a falsified content check, no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 353 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus the verdict-neutral STORAGE line; round 40 deepens held update-safety ground, no Frontier move. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (124 cases, 124 passed, 0 failed); live run exits with the six-plane rollup; `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; round 40 re-opened pacman 54d9411 (`util.c`, `trans.c`, `hook.c` byte-identical to round 39's snapshots) and the round-39 counters still PASS at `aad01138`. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; mismatches 0 required at the round-40 tip (the round-39 K10 red, lessons 54 → 55 from the round-39 spot-check, is repaired by this table). | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; recipient acknowledgement and independent replay are unverified; round-40 sibling sweep found no crossing (`.ufo/waves/round-40/w1/ConnSiblings.md`). | fleet round 1; unchanged |

## Capabilities — current full evidence set (round 40)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates opened tier-scoped sources with anchors, rejections, paths, search log and unopened leads | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT and STORAGE lines; selftest prints PASS (124 cases, 124 passed, 0 failed) | `tools/tsukuroi-census.sh`; `.ufo/evidence/round-1-kaika/scout-live.md`; `.ufo/evidence/round-1-kaika/after.md` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations while preserving fixture isolation and policy boundaries | `.ufo/waves/round-12/resumed/after.json`; `.ufo/waves/round-12/resumed/selftest-after.json`; `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | round 12 |
| boot-chain-audit | Reads and types initramfs root paths against the selected firmware entry, producing a per-entry next-boot verdict | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt` | round 17 |
| storage-error-counter-reader | Reads every btrfs device's five error counters from sysfs and prints one verdict-neutral STORAGE line (HEALTHY/DEGRADED/BLOCKED with nonzero pairs and reason tokens), demonstrated on fixtures, the live host and production-path namespace views; since round 39 an absent or empty root is cross-checked against the mount table, and since round 40 its selftest varies the mount-table literals | `tools/tsukuroi-census.sh`; `.ufo/waves/round-38/after/c1-final-b0005ae.json`; `.ufo/waves/round-38/after/c1-q82-final-b0005ae.json`; `.ufo/waves/round-39/after/c1-final-a2d7aad.jsonl`; `.ufo/waves/round-40/after/c1-final-aad0113.jsonl` | round 38 |

- **planned (next round):** amend both round-40 counters under QUALITY 88 — C1: a selfref guard over the executed
  selftest (not a regex over its text), a stderr-capturing receipt, and the held-out mutants H5/H6/H9 plus the
  `declare -f` prologue as frozen should-fail arms; C2: a per-row proposition check that refuses the token-list writer
  and the `w1/C2CritXFalse` entries as frozen controls. Plus `tools/check-self-assessment.py --scratch` (R40-TMP-MISROOT).
  Lowest axes: depth 8 and adjacency 8 (tied); candidate depth theme `alpm-package-anatomy-r26.md` from
  `merge/tsukuroi/` (`w1/AsmPackageScan.md`).
- **retired:** none.

## Round 41 — declaration (2026-10-26, base `0e5805a1f149bd2ed9fe0db2e0a832afb034a835`, before any seat)

Round 40 was admitted (`corpus/lessons/round-40-verifier-spotcheck.md` §3). This round takes the planned row: the
round-40 closure's routed defect R40-ANSWER-KEY for both counters (§6.1) plus §6.2 (stderr FAIL lines, scratch on
Ctrl-C), with the candidate depth theme `alpm-package-anatomy-r26.md` from `merge/tsukuroi/`. Lowest non-retired axes:
depth 8 and adjacency 8 (tied); C2 works depth; adjacency stays unclaimed and is not harmed. Saturation 9 / window 3
unchanged. Counters, pinned sources, the host capture and the two registry rows landed first in freeze commit
`e479fdc54d0977ccd8112a42d8d139baaebcb02e`. The commit time of this section is its authority (R40-HEADING-TIMES).

| Claim | Axis | Surface moved | Counter (frozen; sha256) | Before at base | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | operability | The census `--selftest` (`tools/tsukuroi-census.sh` `run_selftest`; `probe_storage_arm` unchanged) gains four mount-table cases — a btrfs line whose mountpoint is not absolute, one whose source is not under `/dev`, one with no `subvol=` option, a table with two btrfs lines — so the round-40 held-out survivors H5, H6, H9 and the count-direction mutant H10 fail it | `python3 tools/score-selftest-mounts-r41.py --revision <REV> --scratch <DIR>` (sha256 `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`): 13 frozen mutants (round-40 M1-M9, H5, H6, H9, H10), three neutral rewrites, one decoy carrying every mutant text in a dead here-document, kill attribution on baseline labels confirmed by a second run, one retry for failed non-mutant runs, fixture capture for the four declared table shapes | see `before/c1-before.jsonl` (expected `survivors 4` H5/H6/H9/H10, `params 0`, FAIL) | `baseline_pass == 1 and neutral_pass == 3 and decoy_pass == 1 and mutants_applied == 13 and survivors == 0 and params == 4` -> PASS, exit 0, at the C1 implementation commit and at the round tip | the predicate is false at either revision; or `probe_storage_arm` differs from the base; or the round-40 C1 counter (`score-selftest-literals-r40.py`) stops passing at the tip |
| C2 | depth (sourced) | Pacman-state plane, package-file side: `corpus/knowledge/alpm-package-anatomy-r41.md` PA1-PA8 — the format's required root members (alpm-package(7)), what libalpm requires on load (only `.PKGINFO`), makepkg's dot-files-first order and the partial-load stop, the three members install keeps in the local database, `.MTREE` as a self-excluding gzip mtree, `pacman -Qkk`'s zero-error branch for a missing mtree, PKGBUILD(5) function working directories, and vercmp order — on rows S227-S236 opened this round | `python3 tools/check-package-anatomy-r41.py --revision <REV>` (sha256 `c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`): source-derived value, frozen proposition relations, negation words, a frozen source window per row, new mined upstream rows, six host values from the frozen capture, and per-row committed reviewer verdict files (`.ufo/waves/round-41/w1/C2RevPA<n>*.md`, `residual/`) | entry absent, `rules_verified 0, verdicts_ok 0, host_ok 0, source_ok 0`, FAIL exit 1 (`before/c2-before.jsonl`) | `rules_verified == 8 and verdicts_ok == 8 and host_ok == 6 and source_ok == 1 and duplicate_rows == 0 and duplicate_headings == 0 and novelty_base_hits == 0` -> PASS, exit 0, at the commit that lands the wave's verdict files and at the round tip | the predicate is false; or any committed verdict file for a row reads `VERDICT: fails` (the counter refuses the row); or a row verdict stays `partly` without a later `holds` after an appended correction |

The C2 lexical checks are shape gates, declared as such: a writer that concatenates the frozen RELATIONS literals and
the derived values passes them (control C2-K2 below, `rules_verified 8`), so the read is the per-row reviewer verdict
(QUALITY 81), which the predicate requires. Verdict files are written by wave seats (non-author for the rows; still the
lane for discernment, LEARNING.md) and committed unedited as wave evidence.

Pre-data controls, scored with the frozen counters at the freeze commit before any seat (script
`.ufo/waves/round-41/controls/run_controls.py`, fixture clones with origin removed; candidate digests in
`controls/candidate-sha256.txt`; outputs `controls/controls-c1.jsonl`, `controls/controls-c2.jsonl`):
C2 — K0 do-nothing FAIL (0/0/0/0); K1 the round-40 token writer (value + NATO filler, first 4-25 word line of each file
as the quote, all-holds fixture verdicts) FAIL `rules_verified 0` (windows and relations); K2 relation-literal writer, no
verdicts, FAIL `rules_verified 8, verdicts_ok 0` (the recorded lexical bypass); K3 X-false by swapped pairings FAIL
`rules_verified 6`; K4 X-false by negation FAIL `rules_verified 6`; K5 candidate with one `fails` verdict FAIL
`verdicts_ok 7`; K6 candidate without verdicts FAIL `verdicts_ok 0`; K7 candidate with one `partly`-only row FAIL
`verdicts_ok 7`; K8 candidate with all-holds fixture verdicts PASS. C1 — see the C1 control lines appended below.

C1 pre-data controls (appended before any seat; frozen counter at `e479fdc5`; the serial runner was stopped during its
first control and re-launched per control with `--names`, a filter added to `run_controls.py` for that purpose):
K0 do-nothing is the before receipt itself (`before/c1-before.jsonl`: `baseline_pass 1, neutral_pass 3, decoy_pass 1,
mutants_applied 13, survivors 4` — H5, H6, H9, H10 — `params 0`, FAIL); K1 the round-40 `declare -f` prologue keyed on
every mutant's text, on the base census, FAIL (`decoy_pass 0`, survivors 13 — its one-case FAIL summary carries no
baseline label, so no kill is attributed; `controls/C1-K1-declare-f-prologue-on-base.jsonl`); K2 the candidate without
its no-`subvol=` case (violates exactly one declared parameter) FAIL (`survivors 1` H9, `params 3`;
`controls/C1-K2-candidate-without-H9-case.jsonl`); K3 the same prologue on the candidate FAIL (`decoy_pass 0`,
`controls/C1-K3-declare-f-prologue-on-candidate.jsonl`); K4 the candidate is the after receipt at the C1 implementation
commit `568c397d` (`after/c1-after-568c397.jsonl`: survivors 0, params 4, PASS). Recorded limit: a self-reader that
strips here-documents before grepping is not refused by the decoy (wave item C1CritDecoy attacks it).

## Round 41 — measured outcome (2026-10-26, author-side; non-author closure pending)

Every claim receipt is a `tools/run-receipt.py` receipt (header: revision, tool, tool_sha256, tool_revision `e479fdc5`).

| Claim | Axis | Before (base `0e5805a1`) | After | Kill rules | Author verdict | Ordinal |
|---|---|---|---|---|---|---|
| C1 census selftest kills H5, H6, H9, H10 | operability | `baseline_pass 1, neutral_pass 3, decoy_pass 1, mutants_applied 13, survivors 4` (H5, H6, H9, H10), `params 0`, FAIL exit 1 (`before/c1-before.jsonl`) | `survivors 0, params 4`, baseline `PASS (128 cases, 128 passed, 0 failed)`, PASS exit 0 at `568c397d` (`after/c1-after-568c397.jsonl`), re-run by seat C1ExecRerun (`w1/C1ExecRerun.md`, every field equal); final receipt at the integration commit `d7bf279f`: `after/c1-final-d7bf279.jsonl` | none fired: `probe_storage_arm` byte-identical to the base (`w1/C1ExecPriorCounters.md`), the round-40 C1 counter PASSes at the dispatch tip (same census bytes) | **verified under the frozen predicate; counter sufficiency falsified** — a here-document-stripping text gate plus one shared fixture line passes the predicate with no new case (`w1/C1CritDecoy.md`); forged FAIL labels are credited (`w1/C1CritLabels.md`). The landed bytes are four fixture cases and no self-reading construct (`w1/C1RevFixtures.md`, `w1/C1CritAxis.md` §1; residual C1RevDiffRead) | 9 → 9 |
| C2 ALPM package anatomy PA1-PA8 | depth (sourced: S227-S236) | entry absent, `rules_verified 0, verdicts_ok 0, host_ok 0, source_ok 0`, FAIL (`before/c2-before.jsonl`) | `rules_verified 8, verdicts_ok 8, host_ok 6, source_ok 1`, no duplicates, novelty 0, PASS exit 0 at `d7bf279f` (`after/c2-after-d7bf279.jsonl`); at the implementation commit `9cc9aa77` all terms but verdicts (`after/c2-impl-9cc9aa7.jsonl`) | no `fails` verdict (16 wave verdict files: 11 `holds`, 5 `partly`); the five `partly` rows (PA2, PA3, PA5, PA6, PA7) carry appended corrections (`20c327b3`) and residual re-reads `residual/C2RevPA{2,3,5,6,7}c.md` — their outcome is recorded in the addendum below | **predicate met; verdict gate shown not to be an authorship check** (planted verdict files pass it, `w1/C2CritControl.md`); content read by 16 seats, novelty: 3 rows new, 4 partly held, 0 held (`w1/C2ScoutNovelty.md`); empirical probes support PA2, PA3, PA6, PA8 (`w1/C2LabratArchive.md`, `C2LabratOrder.md`, `C2LabratQkk.md`, `C2LabratVercmp.md`) | 8 → 8 |

Causal separability: `w1/CritSeparability.md`. No-harm: `w1/RevNoHarmAxes.md`; seven lane gates exit 0 at the dispatch tip
(`w1/GateAllRegistry.md`); self-assessment see the table below. Sources: 226 → 236 rows, census exit 0, W04 39 → 40 (S230,
declared distinct scope from S213; `w1/RoutedW04.md`). Assimilation: staged `alpm-package-anatomy-r26.md` re-grounded
(PA1, PA7, PA8 admitted as lane text; the `$pkgdir` sentence and the ground pointer rejected; `w1/AsmGate.md`).
considerthese: `considerthese/2026-10-26.md` proposal "Counter-attack scoreboard" landed as `SKILL.md`
"Counter-attack scoreboard — rounds 40-41". Routed fix R40-TMP-MISROOT shown able to fail
(`w1/RoutedSelfAssessScratch.md`: old tool 1153 `/tmp` mkdirs by the census child, new tool 0 with scratch TMPDIR).

## Axes — current self-assessment (round 41 final measured surface)

Each count is re-derived from the committed lane tree at the round-41 outcome commit (the commit that lands this table); ordinals unchanged.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 62 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3847 `wc -l` / 956 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 58 files (`find corpus/lessons -type f | wc -l`); round-41 C2 predicate met at `d7bf279f` with five second-read `partly` verdicts answered by appended corrections; no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 404 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus the verdict-neutral STORAGE line; round 41 deepens held pacman-state ground (package-file side), no Frontier move. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (128 cases, 128 passed, 0 failed); live run exits with the six-plane rollup; `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; round 41 re-fetched its nine pinned pacman/alpm-docs URLs byte-identical (`w1/C2ExecLiveSources.md`) and the round-39 and round-40 C1 counters still PASS (`w1/C1ExecPriorCounters.md`). | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; mismatches 0 required at the round-41 outcome commit (the round-40 table's seven stale cells at `d7bf279f`, K07-K11, K13, K17, are repaired by this table). | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; recipient acknowledgement and independent replay are unverified; round-41 sibling sweep (`.ufo/waves/round-41/w1/ConnSiblings.md`). | fleet round 1; unchanged |

## Capabilities — current full evidence set (round 41)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates opened tier-scoped sources with anchors, rejections, paths, search log and unopened leads | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT and STORAGE lines; selftest prints PASS (128 cases, 128 passed, 0 failed) | `tools/tsukuroi-census.sh`; `.ufo/evidence/round-1-kaika/scout-live.md`; `.ufo/evidence/round-1-kaika/after.md` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations while preserving fixture isolation and policy boundaries | `.ufo/waves/round-12/resumed/after.json`; `.ufo/waves/round-12/resumed/selftest-after.json`; `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | round 12 |
| boot-chain-audit | Reads and types initramfs root paths against the selected firmware entry, producing a per-entry next-boot verdict | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt` | round 17 |
| storage-error-counter-reader | Reads every btrfs device's five error counters from sysfs and prints one verdict-neutral STORAGE line (HEALTHY/DEGRADED/BLOCKED with nonzero pairs and reason tokens), demonstrated on fixtures, the live host and production-path namespace views; since round 39 an absent or empty root is cross-checked against the mount table, since round 40 its selftest varies the mount-table literals, and since round 41 four held-out table shapes | `tools/tsukuroi-census.sh`; `.ufo/waves/round-38/after/c1-final-b0005ae.json`; `.ufo/waves/round-38/after/c1-q82-final-b0005ae.json`; `.ufo/waves/round-39/after/c1-final-a2d7aad.jsonl`; `.ufo/waves/round-40/after/c1-final-aad0113.jsonl`; `.ufo/waves/round-41/after/c1-after-568c397.jsonl` | round 38 |

- **planned (next round):** (1) operability — fix the census packages-plane pipefail wrong verdict at
  `tools/tsukuroi-census.sh:692` (R41-CENSUS-PIPEFAIL-692) with a selftest case carrying a large error-bearing `-Qkk`
  sample, red before the fix; (2) a counter amendment under QUALITY 89 — C2 verdict files bound to the orchestrator's
  results record (seat name, agent id, final output equal to the committed file), C1 kills attributed only to cases that
  own the fixture table, and the mirror-evasion controls (here-document-stripping self-reader; relation-literal writer
  with planted verdicts) frozen as should-fail; (3) depth, the lowest axis with adjacency: the storage scrub-record
  leads (`w1/ConnFrontier.md` §5). The round-40 sweep's unrecorded candidates (`w1/MistakesSweep.md` §4) stay open.
- **retired:** none.

### Round 41 — residual addendum (appended after both WAVE-DONE messages; no table above is rewritten)

Residual call: 6 reviewer seats (`residual-dispatch.json`, `residual-results.json`). Row re-reads after the appended
corrections: PA2 `holds`, PA3 `holds`, PA5 `holds`, PA7 `holds`, **PA6 `partly`** (`residual/C2RevPA6c.md`: the correction
names two of the three NULL paths of `_cache_mtree_open`; the allocation-failure path `be_local.c:263-265` is missing).
C1 structural read: `residual/C1RevDiffRead.md` `supports` (four `check` cases, no self-reading construct, held-out kills
on their own R41 cases, arm byte-identical). C1 final receipt at `d7bf279f`: PASS, survivors 0, params 4
(`after/c1-final-d7bf279.jsonl`). Self-assessment at `64f9062e`: 27 checked, 0 mismatches (`after/self-assessment-final.jsonl`).

Verdict consequence, applied as declared: the C2 kill rule "a row verdict stays `partly` without a later `holds` after an
appended correction" **fires for PA6**, so **C2 is not verified** although its frozen predicate is met at `d7bf279f`. A
third correction bullet naming the missing path is appended to the entry; it was written after the residual verdict and
carries no verdict, so it does not reverse this outcome. C1: verified under the frozen predicate, with the counter's
sufficiency falsified (`w1/C1CritDecoy.md`) and the landed bytes read structurally by a non-author seat.
Round total: 80 seats (w1 74 + residual 6), every seat settled with a report.

## Round 42 — declaration (2026-10-26, base `c8efaa3f120834541f8de1e5e0367e8d1593bae6`, before any seat)

Round 41 was closed `rejected-honest-stop` (`corpus/lessons/round-41-verifier-spotcheck.md` §3: C1 verified, C2's
declared kill rule fired on PA6). The base is the lane tip at round start as `jj-lane.sh state` printed it
(`local=c8efaa3f…`, routed defect R41-BASE-MISREAD). This round takes the planned row items (1) and (3) and folds
item (2) into both counters (routed defect R41-GUARD-BYPASS, QUALITY 89): C1 is scored by a metamorphic oracle that
holds no expected verdict, C2's verdicts count only through the orchestrator's dispatch and results records.
Ordinals at base: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. Depth and adjacency
are tied lowest; C2 works depth; adjacency stays unclaimed and must not be harmed. Saturation 9 / window 3 unchanged.
The commit time of this section is its authority (R40-HEADING-TIMES).

| Claim | Axis | Surface moved | Counter (frozen; sha256) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | operability | The census packages and update-safety planes under `set -o pipefail` (`tools/tsukuroi-census.sh`): the early-reader pipelines at :692/:694 (`printf … \| grep -q`/`grep -m1` on the merged `-Qkk` sample, R41-CENSUS-PIPEFAIL-692) and :1621, :1635, :1641, :1652 (`printf … \| head` on the `-Qu`/`-Sup`/`-Suu` lists) give a wrong verdict or kill the census (exit 141) once a probe prints more than the pipe buffer; the round fixes them and adds a selftest case carrying a large error-bearing `-Qkk` sample | `python3 tools/score-size-invariance-r42.py --revision <REV> --scratch <DIR>` (sha256 `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03`): ten small/large fixture twins (P1-P6 `-Qkk`, U1-U4 update lists; 1 MiB of verdict-neutral, marker-free padding; signal before, inside and after it; large twin first; per-run error token) built from the BASE census's own dispatcher and `fx_default`, compared byte for byte (U pairs with integers normalised); three production-path legs N1/N3/N6 inside `unshare -rm` with a stub bind-mounted over `/usr/bin/pacman` and no `TSUKUROI_*` override (QUALITY 82/85); selftest; default-fixture equality with the base | `invariant 3` (P2, P4, P5; P1/P3/P6 read HEALTHY where BLOCKED is due, U1-U4 exit 141), `ns_invariant 0`, `selftest_pass 1`, `default_equal 1`, FAIL | **PASS iff cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1**, at the implementation commit and at the tip | predicate false at the tip; or `git diff <base> <tip> -- tools/tsukuroi-census.sh` has a hunk outside `probe_packages`, `probe_update_safety` and `run_selftest`; or the round-41 C1 counter `tools/score-selftest-mounts-r41.py` stops passing at the tip |
| C2 | depth (sourced) | Storage-integrity frontier, scrub record: `corpus/knowledge/btrfs-scrub-record-r42.md` SC1-SC5 — the record file's name and tmp-then-rename/flock write discipline, its `scrub status:1` line format, who writes it and when recording is disabled (and that running state comes from the kernel ioctl), how status folds device lines (finished = all, canceled = any, `interrupted`, `no stats available`), and the per-device `scrub_speed_max` limit — on rows S237 (btrfs-progs v7.1 `cmds/scrub.c`), S238 (v7.1 `CHANGES`) and S239 (own-work host capture), opened this round | `python3 tools/check-scrub-record-r42.py --revision <REV>` (sha256 `dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f`): per row a quote on its named line of a digest-pinned snapshot with at least one quote inside the row's frozen source window, the row's frozen token (absent at the base), a host line naming an existing line of the pinned capture, the registry rows new, `mined`, opened 2026-10-26 and used-by the entry; verdicts bound through `w2-dispatch.json` + `w2-results.json` + the committed report (seats `C2RevSC<n>` reviewer and `C2CritSC<n>` critic; a `partly` needs a bound residual `C2RevSC<n>c` `holds`) | entry absent: `rows 0`, FAIL | **PASS iff rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and sources_ok == 1 and verdicts_ok == 5 and novelty_base_hits == 0**, at the tip | predicate false; or any bound verdict reads `fails`; or a `partly` row without a bound residual `holds` (inside the predicate); or the non-author closure finds a row false against its pinned snapshot |

Both counters write nothing outside `--scratch`/`$TMPDIR` (C1) or nothing at all (C2), and remove their scratch on exit
and on SIGINT/SIGTERM. C2's lexical checks are shape gates, declared as such: control C2-K1 below (a scripted writer
whose quotes are copied from the windows) passes every lexical conjunct; only the bound verdicts read the rows. The
committed-bytes predicate cannot tell forged orchestrator records from real ones (control C2-K3 passes it); the
counter therefore also reports, outside the predicate, `transcripts_bound`: how many bound verdict lines occur in the
seat's own transcript under `~/.omp/agent/sessions` (host-local, written by omp, not by the lane).

Pre-data controls (the battery; scored with the frozen counters at the freeze commit before any seat; scripts
`.ufo/waves/round-42/controls/run_controls_c1.py` sha256 `259a9a9760e4e6be6b906e66467cc70e6b862472cba6b329ef8891763d4a1091`
and `run_controls_c2.py` sha256 `b85bbaa566c862a36be6a78425cec81ca2be5d3b06b68206a2b575664041cb2f`; fixture clones with origin
removed; outputs and the battery's last-line `should_fail_accepted` / `control_accepted` fields in
`.ufo/waves/round-42/controls/`):
C1 — K0 do-nothing (base census); K1 size-gate (BLOCKED whenever the sample exceeds 64 KiB); K2 head-truncation; K3
head+tail truncation; K4 packages-only fix (update plane untouched: exactly one declared surface missing); K5
padding-filter mirror evasion (drops warning and zero-altered lines, keeps the early readers); K7 fixture-gated fix
(only when `TSUKUROI_FIXTURE` is set); K8 cached-live (K7 plus a replay cache under `$HOME`): each must FAIL; K6 the
candidate fix must PASS. C2 — K0 do-nothing; K1 scripted writer + planted verdict files; K2 K1 + forged results
without dispatch tasks; K4 forged records with one `fails`; K5 forged records with one unanswered `partly`: each must
FAIL; K3 forged dispatch + results must PASS (reachability and the recorded limit, `transcripts_bound 0`).
Expected battery lines: C1 `should_fail_accepted 0, control_accepted 1`; C2 `should_fail_accepted 0, control_accepted 1`.

## Round 42 — measured outcome (2026-10-26, author-side; non-author closure pending)

Every claim receipt is a `tools/run-receipt.py` receipt (header: revision, tool, tool_sha256, tool_revision
`a84fc9de`). Waves: `w1` 43 seats (build + first falsifiers), `w2` 34 seats (falsify, ten counted C2 reads); no residual
call; round total 77 seats, every seat settled with a report (`w1-results.json`, `w2-results.json`).

| Claim | Axis | Before (base `c8efaa3f`) | After | Kill rules | Author verdict | Ordinal |
|---|---|---|---|---|---|---|
| C1 census early readers under pipefail | operability | `invariant 3` (P2, P4, P5), `ns_invariant 0`, `selftest_pass 1`, `default_equal 1`, FAIL exit 1 (`before/c1-before.jsonl`) | PASS exit 0 at `44766208` (`w1/C1ExecRerun/c1-after-4476620.jsonl`) and at the integration commit `78abb8b5`: `invariant 10, ns_invariant 3`, selftest `PASS (132 cases, 132 passed, 0 failed)`, `default_equal 1` (`after/c1-after-78abb8b.jsonl`; re-run `w2/C1FinalRerun.md`); census bytes unchanged since `78abb8b5` | none fired: every census hunk lies in `probe_packages`, `probe_update_safety` or `run_selftest` (`w1/C1ExecDiffScope.md`, `w2/C1RevIntegration.md`); the round-41 C1 counter PASSes at `78abb8b5` (`after/r41-c1-counter-78abb8b.jsonl`) | **verified under the frozen predicate; counter sufficiency falsified** — censuses fixed only under `TSUKUROI_FIXTURE`-or-uid-0, only for the fixture package names, or behind a padding-grammar filter also PASS (`w1/C1CritNsView.md`, `w1/C1CritEvasion.md`, `w1/ConnClaims.md`, rebuilt on the tip `w2/C1CritFinalEvasion.md`); a production-identity leg (uid 1000 via `setpriv`, outside the predicate) shows the tip fixed and the gated arm not (`w2/C1FinalProdIdentity.md`) | 9 → 9 |
| C2 btrfs scrub record SC1-SC5 | depth (sourced: S237-S239) | entry absent: `rows 0`, FAIL exit 1 (`before/c2-before.jsonl`) | `rows 5, quotes_ok 5, novelty_ok 5, host_ok 5, sources_ok 1, verdicts_ok 1, novelty_base_hits 0`, FAIL exit 1 at `342d1049` (`after/c2-after-342d104.jsonl`; `transcripts_bound 8` of 8) | **fired**: bound `fails` — SC1 (C2CritSC1), SC3 (C2RevSC3, C2CritSC3); SC4, SC5 `partly` without residual | **not verified** (honest stop); the false sentences are withdrawn in the entry's "Corrections — round-42 wave 2"; two of them were adopted wave-1 notes (R42-ADOPTED-UNREAD, QUALITY 91) | 8 → 8 |

Causal separability: `w1/CritSeparability.md` (the counters read disjoint inputs). No-harm: `w2/CritNoHarmFinal.md`,
`w2/GateFinal.md` (the three wave-1 bookkeeping regressions — adjacency anchor IN-109, registry rows for the two new
counters, self-assessment counts — repaired; the self-assessment row below is re-derived at the outcome commit). Sources:
236 → 239 rows, census exit 0, W04 40 → 40. considerthese: "Downstream patch-offset check" landed as appended notes in the
r38, r39 and r41 entries and a SKILL note. Assimilation: evaluated (`w1/AsmGate.md`), nothing adopted. Routed defect
R41-PA6-UNJUDGED: PA6 `holds` as corrected (`w1/PA6Verdict.md`).

## Axes — current self-assessment (round 42 final measured surface)

Each count is re-derived from the committed lane tree at the round-42 outcome commit (the commit that lands this table); ordinals unchanged.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 63 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3956 `wc -l` / 984 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 60 files (`find corpus/lessons -type f | wc -l`); round-42 C2 not verified (bound `fails` on SC1 and SC3); no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 414 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus the verdict-neutral STORAGE line; round 42 deepens the Frontier scrub-record line from source, no Frontier move. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (132 cases, 132 passed, 0 failed); live run exits with the six-plane rollup; `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; round 42 re-fetched its two pinned btrfs-progs URLs byte-identical (`w1/C2ExecLiveSources.md`), re-opened S237-S239 (`w2/SrcReopenS237..9.md`), and marked the Arch packaging offsets of the r38/r39/r41 pacman pins. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; mismatches 0 required at the round-42 outcome commit. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; the round-42 census edit moved mori's `PROVINCE.md:287` pin (reported, `w2/AdjMoriPin.md`); recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |

## Capabilities — current full evidence set (round 42)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates opened tier-scoped sources with anchors, rejections, paths, search log and unopened leads | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT and STORAGE lines; selftest prints PASS (132 cases, 132 passed, 0 failed) | `tools/tsukuroi-census.sh`; `.ufo/evidence/round-1-kaika/scout-live.md`; `.ufo/evidence/round-1-kaika/after.md` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations while preserving fixture isolation and policy boundaries | `.ufo/waves/round-12/resumed/after.json`; `.ufo/waves/round-12/resumed/selftest-after.json`; `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | round 12 |
| boot-chain-audit | Reads and types initramfs root paths against the selected firmware entry, producing a per-entry next-boot verdict | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt` | round 17 |
| storage-error-counter-reader | Reads every btrfs device's five error counters from sysfs and prints one verdict-neutral STORAGE line (HEALTHY/DEGRADED/BLOCKED with nonzero pairs and reason tokens), demonstrated on fixtures, the live host and production-path namespace views; since round 39 an absent or empty root is cross-checked against the mount table, since round 40 its selftest varies the mount-table literals, since round 41 four held-out table shapes | `tools/tsukuroi-census.sh`; `.ufo/waves/round-38/after/c1-final-b0005ae.json`; `.ufo/waves/round-38/after/c1-q82-final-b0005ae.json`; `.ufo/waves/round-39/after/c1-final-a2d7aad.jsonl`; `.ufo/waves/round-40/after/c1-final-aad0113.jsonl`; `.ufo/waves/round-41/after/c1-after-568c397.jsonl` | round 38 |

- **planned (next round):** (1) operability — amend the C1 counter under QUALITY 90: production-path legs at uid 1000
  (`setpriv`) with per-run fixture names, frozen controls for the fixture-or-uid-0, data-gated and padding-filter arms,
  refuse to run without `--scratch`; fix `tools/boot-chain-audit.sh:480-487` (`find -quit | grep -q` under pipefail)
  with a red-before case; a selftest case for the `:743` baseline lookup; (2) depth — re-ground SC1 and SC3 of
  `btrfs-scrub-record-r42.md` as new rows with counted reads (or a scrub-record census arm as Frontier→Core,
  `w2/ConnRound43.md`), with the C2 binding anchored to the first line (QUALITY 90).
- **retired:** none.

## Round 43 — declaration (2026-10-26, base `6951ead90566b2d74f7c45b4efca29246badad64`, before any seat)

Round 42 was closed `rejected-honest-stop` (`corpus/lessons/round-42-verifier-spotcheck.md` §3: C1 verified, C2's
declared kill rule fired on SC1/SC3). The base is the lane tip at round start as `jj-lane.sh state` printed it
(`local=6951ead9…`, which carries that spot-check). This round takes the planned row's items (1, narrowed) and (2):
C1 fixes the routed boot-chain fail-open (R42-C1-COUNTER-AMEND item 5), C2 re-grounds the withdrawn SC1/SC3 text
(R42-C2-REGROUND) with the anchored verdict binding (R42-VERDICT-FORM, QUALITY 90). Ordinals at base: depth 8,
coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest; C2 works
depth; adjacency stays unclaimed (a recipient action is not lane-producible) and must not be harmed. Saturation 9 /
window 3 unchanged. The commit time of this section is its authority (R40-HEADING-TIMES).

| Claim | Axis | Surface moved | Counter (frozen; sha256) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | operability | `tools/boot-chain-audit.sh` `boot_inputs_newer` (base :480-487): `find <8 start points> -newermt @btime -print -quit 2>/dev/null \| grep -q .` under `set -uo pipefail` (:139) reads "no input newer" whenever find exits 1 (a missing start point or an unreadable directory listed before the match), so the BOOTED-OBSERVED gate (`newer = 0`) passes while an input IS newer. The fix decides on find's output (new helper `inputs_newer_than`), plus three `R43-C1` selftest cases (45 → 48) | `python3 tools/score-bootinputs-r43.py --revision <REV> --scratch <DIR>` (sha256 `886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f`): 16 production-path cases in a private user+mount namespace at the caller's uid/gid (subuid map + `setpriv`, QUALITY 85/90), values drawn per run; a live leg against an independent walk; the script's own selftest | FAIL: `correct` < 16 (the masked cases read 0), `selftest_r43 0` | **PASS iff cases == 16 and correct == 16 and identity_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r43 >= 2** at the measured revision | a census-plane or other function body of `boot-chain-audit.sh` changes outside `inputs_newer_than`, `boot_inputs_newer` and `run_selftest`; or the round-42 C1 counter / census selftest regresses at the measured revision |
| C2 | depth (sourced: S240 opened this round) | `corpus/knowledge/btrfs-scrub-record-r43.md` rows SR1 (write discipline: `_tmp` opened `O_WRONLY\|O_CREAT` without `O_TRUNC`, renamed only after a successful write, never unlinked), SR3 (resume carries the interrupted record's counters and `t_start` through `scrub_resumed_stats`; later recording failures print only under `do_print`/`-B` and do not assign `err`), SR6 (running state only from `BTRFS_IOC_SCRUB_PROGRESS`, which returns EPERM without `CAP_SYS_ADMIN`: an unprivileged status never reads `running`), on S237 (round-42 scrub.c snapshot, re-opened), S240 (Linux v7.2.11 `fs/btrfs/ioctl.c`, new) and S241 (own-work host capture, new); plus a header pointer in the round-42 entry | `python3 tools/check-scrub-record-r43.py --revision <REV>` (sha256 `b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854`): quotes on named lines of digest-pinned snapshots with id↔file match and windows; proposition tokens in the statement cell; host lines; registry; novelty outside the round-42 uncounted corrections; pointer; per row two counted wave-2 seats (`C2RevSR<n>` reviewer, `C2CritSR<n>` critic) bound through `w2-dispatch.json` + `w2-results.json` (declared verdict line = JSON `verdict_line` field, else the output's first non-empty line) and the committed report's first line | FAIL: `rows 0` | **PASS iff rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1** at the measured revision | any bound `fails`; a `partly` without a bound residual `C2ResSR<n>` reading `holds`; an unbound counted seat |

C2's lexical checks are shape gates, declared as such (control C2-K1, a scripted writer, passes every lexical
conjunct; only the bound verdicts read the rows). The committed-bytes predicate cannot tell forged orchestrator
records from real ones (control C2-K3 passes it); `transcripts_bound` is reported outside the predicate. C1's
namespace legs leave the mount-table, uid_map and script-path channels open (QUALITY 90 "named open"); control C1-K7
(a fix gated on tmpfs at /etc in the mount table) passes and is recorded as that limit.

Pre-data controls (scored with the frozen counters before any seat; scripts
`.ufo/waves/round-43/controls/run_controls_c1.py` sha256 `8eb691711eefda48c3e557c06ac4b156299e2829e2688a893b84ad7b4a131493`
and `run_controls_c2.py` sha256 `7564862737a027b5efa31e849fd73bc7b543ade1968744d401bb10e723f4184f`; candidate bytes
`controls/candidate-boot-chain-audit.sh` sha256 `3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74` and
`controls/c2-candidate/`): C1 — K0 do-nothing, K1 constant 1, K2 /etc start points dropped, K3 uid-gated, K4
env-gated, K5 name-gated (/etc/crypttab), K6 `-maxdepth 0`, K10 missing-point pre-filter (an unreadable directory
still masks): each must FAIL; K8 candidate and K9 `{ find … || true; } | grep -q .` must PASS; K7 mount-gated recorded.
C2 — K0 do-nothing, K1 scripted writer + planted reports, K2 K1 + results without dispatch, K4 one `fails`, K5 one
`partly` without residual, K6 mention-not-assertion, K7 content-free statements, K8 SR6 without the S240 quotes, K9 a
quote line shifted, K10 id↔file mismatch, K11 no pointer, K12 S240 `queued`, K13 report first line differs: each must
FAIL; K3 forged records must PASS (recorded limit). Battery lines: C1 `should_fail_accepted 0, control_accepted 1`;
C2 `should_fail_accepted 0, control_accepted 1` (`controls/battery-summary-c1.jsonl`, `battery-summary-c2.jsonl`).

Causal separability: C1 touches `tools/boot-chain-audit.sh` only; C2 touches the r43 entry, the r42 entry's header
line, `corpus/SOURCES.md` and frozen snapshots. Neither counter reads the other's surface.

## Round 43 — measured outcome (2026-10-26, author-side; non-author closure pending)

Every claim receipt is a `tools/run-receipt.py` receipt (header: revision, tool, tool_sha256, tool_revision
`fe357001`). Waves: `w1` 44 seats (build + first falsifiers), `w2` 34 seats (falsify, six counted C2 reads), one residual
call of 2 reviewer seats (the counted residual read `C2ResSR3` and a fix re-check); round total 80 seats, every seat
settled with a report (`w1-results.json`, `w2-results.json`, `residual-results.json`); no dead seat. Measured revision:
`c3954913f6b376b4f9ff3d596f1eaefc6846e937` (the commit carrying the residual records).

| Claim | Axis | Before (base `6951ead9`) | After (`c3954913`) | Kill rules | Author verdict | Ordinal |
|---|---|---|---|---|---|---|
| C1 boot-input freshness under pipefail | operability | FAIL: `cases 16, correct 8` (the six `miss/etc/*-newer`, `multi-miss-deep-modules-newer`, `unreadable-dir-modules-newer` read 0), `selftest_r43 0`, selftest `PASS total=45` (`before/c1-before.jsonl`) | PASS: `cases 16, correct 16, identity_ok 1, live_agree 1, selftest_pass 1, selftest_r43 4`, selftest `PASS total=49 failed=0` (`after/c1-after-c395491.jsonl`); also PASS at `717b716a` (`after/c1-after-717b716.jsonl`, 48 cases) and three times at `8acf0b02` (`w2/C1FinalRerun.md`) | none fired: only `inputs_newer_than` (new), `boot_inputs_newer`, `run_selftest` change (`w2/C1FinalKillRule.md` per-function sha256); the round-42 C1 counter PASSes and the census selftest prints `PASS (132 cases, 132 passed, 0 failed)` at `8acf0b02`, census bytes unchanged since the base | **verified under the frozen predicate** | 9 → 9 |
| C2 scrub record re-grounded SR1, SR3, SR6 | depth (sourced: S240 opened this round; S237, S241) | FAIL: `rows 0` (`before/c2-before.jsonl`) | PASS: `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, verdicts_ok 3, novelty_base_hits 0, pointer_ok 1` (`after/c2-after-c395491.jsonl`); bound verdicts SR1 holds/holds, SR3 holds/partly + residual `C2ResSR3` holds, SR6 holds/holds; `transcripts_bound 7` of 7 when run with the host session dir (`after/c2-after-c395491-direct.json`; 0 under run-receipt's private HOME) | none fired: no bound `fails`; the one `partly` (SR3 skip condition, `w2/C2CritSR3.md` item 6) was narrowed against scrub.c:1430-1437 and re-read `holds` by the bound residual; no unbound counted seat; the six outputs carry no second verdict line (L1 audit, lesson Entry gate) | **verified under the frozen predicate** | 8 → 8 |

No count-to-ordinal scale exists (round-12 note); both claims move their axis without an ordinal change. Causal
separability: `w2/CritSeparabilityFinal.md` (each counter scored on the other claim's partial tree). No-harm:
`w2/CritNoHarmFinal.md` (no deleted file; SCORECARD, PROVINCE, README, SOURCES changes append-only or used-by only;
the round-42 entry gains one header line), `w2/RegistryFinal.md` (registry 68/68 PASS after the round43 table), sources
census exit 0 (`w2/SourcesCensusFinal.md`). Recorded limits (not claimed): C1's namespace legs leave the mount-table,
uid_map, script-path and cwd channels open (K7 PASS), and the counter does not exercise the empty-btime branch, a widened
comparison or every start point's membership (`w1/C1MutFix.md`, `w2/C1MutFinal.md`); C2's binding accepts a padded or
blank-line-prefixed verdict line and ignores a JSON `verdict` field beside `verdict_line` (`w1/C2MutBinding.md`), and its
lexical checks are shape gates. considerthese: "Cross-note correction propagation map" (2026-10-26) built for the
round-42 corrections and closed by append-only pointers. Assimilation: none (evaluated, `w1/AsmGate.md`). Routed
defects: R42-C2-REGROUND, R42-CAP-HEADER-DUP, R42-ADJ-TAMESHI-UNREPORTED (report handoff), R42-VERDICT-FORM done;
R42-C1-COUNTER-AMEND done for the boot-chain fail-open and the counter items, the census `:743` case and single-line
readers routed on (lesson). The C1 row of the declaration names three `R43-C1` selftest cases (45 → 48); the
integration added a fourth (`R43-C1-missing-start-point-silent`, 49) after wave 1 (`w2/CritCalibration.md`).

## Axes — current self-assessment (round 43 final measured surface)

Each count is re-derived from the committed lane tree at the round-43 outcome commit (the commit that lands this table); ordinals unchanged.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 64 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 4112 `wc -l` / 1067 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 62 files (`find corpus/lessons -type f | wc -l`); round-43 C2 verified (SR1, SR3, SR6 bound holds; SR3 through the residual); no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 425 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus the verdict-neutral STORAGE line; the scrub record stays Frontier (round 43 re-grounds it from source, no Frontier move). | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (132 cases, 132 passed, 0 failed); `bash tools/boot-chain-audit.sh --selftest` prints `PASS total=49 failed=0`; round-43 C1 verified (boot-input freshness decides on find's output); `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; round 43 re-fetched S237 and S240 byte-identical (`w1/C2ExecLiveSources.md`, `w2/SrcReopenS237.md`, `w2/SrcReopenS240.md`), re-ran the S241 capture (`w2/SrcReopenS241.md`) and checked the Arch kernel patch set (no `fs/` file). | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; mismatches 0 required at the round-43 outcome commit. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; round 43 moved no live sibling pin (four frozen sibling records pin `boot-chain-audit.sh` lines, reported, `w2/AdjFinal.md`) and restates the round-42 tameshi and mori handoffs; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |

## Capabilities — current full evidence set (round 43)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates opened tier-scoped sources with anchors, rejections, paths, search log and unopened leads | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT and STORAGE lines; selftest prints PASS (132 cases, 132 passed, 0 failed) | `tools/tsukuroi-census.sh`; `.ufo/evidence/round-1-kaika/scout-live.md`; `.ufo/evidence/round-1-kaika/after.md` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations while preserving fixture isolation and policy boundaries | `.ufo/waves/round-12/resumed/after.json`; `.ufo/waves/round-12/resumed/selftest-after.json`; `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | round 12 |
| boot-chain-audit | Reads and types initramfs root paths against the selected firmware entry, producing a per-entry next-boot verdict; since round 43 its boot-input freshness check decides on find's output, so a missing start point or unreadable directory no longer opens the BOOTED-OBSERVED gate | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt`; `.ufo/waves/round-43/after/c1-after-c395491.jsonl` | round 17 |
| storage-error-counter-reader | Reads every btrfs device's five error counters from sysfs and prints one verdict-neutral STORAGE line (HEALTHY/DEGRADED/BLOCKED with nonzero pairs and reason tokens), demonstrated on fixtures, the live host and production-path namespace views; since round 39 an absent or empty root is cross-checked against the mount table, since round 40 its selftest varies the mount-table literals, since round 41 four held-out table shapes | `tools/tsukuroi-census.sh`; `.ufo/waves/round-38/after/c1-final-b0005ae.json`; `.ufo/waves/round-39/after/c1-final-a2d7aad.jsonl`; `.ufo/waves/round-40/after/c1-final-aad0113.jsonl`; `.ufo/waves/round-41/after/c1-after-568c397.jsonl` | round 38 |

One header row (R43-CAP-HEADER-DUP; QUALITY 92): `awk '/^## Capabilities — current full evidence set \(round 43\)/{f=1;next} /^## /{f=0} f&&/^\| Capability \|/{n++} END{print n+0}' SCORECARD.md` prints 1.

- **planned (next round):** (1) coverage — a verdict-neutral scrub-record census arm for the unprivileged-readable
  subset (directory, file stat, `scrub_speed_max`; never the running state, SR6) as Frontier → Core;
  (2) depth — the ioctl success direction (`btrfs_scrub_progress`, Linux `fs/btrfs/scrub.c`) as a sourced row;
  (3) operability — the routed census items (`:746` lookup selftest case past the pipe buffer, the five single-line
  probe readers). Draft text: `.ufo/waves/round-43/w2/ConnRound44.md`.
- **retired:** none.

## Round 44 — declaration (2026-10-26, base `98020ece0674e0b569ee23aed10ffbee355b248e`, before any seat)

Round 43 was admitted (`corpus/lessons/round-43-verifier-spotcheck.md` §2-§4). The base is the lane tip at round start as
`jj-lane.sh state` printed it (`local=98020ece…`, which carries that spot-check). This round takes the planned row's
items (1) and (2); item (3) (the census `:746` lookup case and the five single-line probe readers) stays routed: a third
claim on the census file would share C1's surface (causal separability) and the round prefers two claims. Ordinals at
base: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest;
C2 works depth; adjacency stays unclaimed (recipient-side acknowledgement is not lane-producible, `PROVINCE.md:77-79`)
and must not be harmed. Saturation 9 / window 3 unchanged. Routed defect R43-SR1-LIMITS-CONTRADICTION is repaired
outside both claims (an appended correction in the r43 entry; no counter reads it). The commit time of this section is
its authority (R40-HEADING-TIMES).

| Claim | Axis | Surface moved | Counter (frozen; sha256) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | coverage | The scrub-record line of the storage-integrity frontier (`PROVINCE.md:212-214`, round-42/43 notes `:239-254`; `corpus/README.md` Frontier) moves Frontier → Core for the unprivileged view: `tools/tsukuroi-census.sh` gains `probe_scrub_record` and one verdict-neutral line `SCRUB btrfs-scrub-record state=NONE\|RECORDED\|BLOCKED dir=absent\|present\|unreadable records=N tmp=N sockets=N unreadable=N orphan=N limited=N timers=N [detail=…]` printed after STORAGE and before the rollup; it reads `/var/lib/btrfs` by name and stat only (records, `_tmp` files, progress sockets, unreadable and orphan counts), each device's sysfs `scrub_speed_max`, and the `btrfs-scrub@*.timer` links under `timers.target.wants`; never content, never an ioctl, never the running state (SR6); plus nine `R44-C1` selftest cases (132 → 141) | `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR>` (sha256 `1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388`): 16 production-path cases in a private user+mount namespace (tmpfs over `/sys/fs/btrfs`, `/var/lib`, `/etc/systemd/system` filled from stdin; caller uid/gid via subuid map + `setpriv`; no override variable; every value drawn per run, the host's own fsid mixed in), a wired leg (full census in a drawn namespace view: exactly one SCRUB line, equal to the oracle, between STORAGE and the rollup), a live leg (full live census vs an independent Python walk) and the census selftest | FAIL: no SCRUB line (`correct 0`, `wired_ok 0`, `live_agree 0`), selftest PASS 132, `selftest_r44 0` | `cases == 16 and correct == 16 and identity_ok == 1 and wired_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r44 >= 6` | any PLANE line, the rollup line or the census exit code changes on the live host between base and the measured revision; any frozen predecessor storage counter (`score-storage-arm-r38.py`, `-r38-q82.py`, `score-storage-hidden-r39.py`, `score-size-invariance-r42.py`) FAILs at the measured revision where it PASSes at base; the arm writes or creates a file in live mode |
| C2 | depth (sourced: S242, S243, S244 opened this round) | New entry `corpus/knowledge/btrfs-scrub-record-r44.md` rows SR7 (the scrub-progress success direction: `btrfs_scrub_progress` returns 0 only while `dev->scrub_ctx` is attached, `-ENOTCONN` for an idle device, `-ENODEV` for an unknown devid; the ioctl copies back only on 0), SR8 (`scrub_speed_max`: `BTRFS_ATTR_RW` mode 0644, `%llu\n` read, `memparse` write with `-EINVAL` on trailing text, 0 = no limit in the throttle), SR9 (the Arch-packaged `btrfs-scrub@.timer`/`.service`: monthly, `Persistent=true`, `WantedBy=timers.target`, `btrfs scrub start -B %f` with `KillSignal=SIGINT`, whose foreground handler issues `BTRFS_IOC_SCRUB_CANCEL`), on S237, S240 (re-opened), S242 (Linux v7.2.11 `fs/btrfs/scrub.c`), S243 (`fs/btrfs/sysfs.c`), S244 (Arch btrfs-progs packaging 7.1-1) and S245 (own-work host capture); plus a header pointer in the r43 entry | `python3 tools/check-scrub-record-r44.py --revision <REV>` (sha256 `c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059`): quotes at digest-checked snapshot lines inside frozen windows with the per-row required files, proposition tokens in the statement cell, host lines on existing capture lines, new mined source rows, novelty tokens (ENOTCONN, memparse, KillSignal) with 0 base hits, the r43 pointer, and the wave-2 verdicts of `C2RevSR<n>`/`C2CritSR<n>` bound through `w2-dispatch.json`, `w2-results.json` and the report's raw first line — a JSON output with a contradictory `verdict` key, a padded line or a blank-line-prefixed output binds nothing (closes the two round-43 binding gaps) | FAIL: `rows 0` | `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1` | any bound counted verdict `fails`; a `partly` with no bound residual `holds`; a counted seat whose output carries a second verdict line contradicting the bound one (audited by hand) |

C2's lexical checks are shape gates (control C2-K1, a scripted writer, passes quotes, props and sources; only the bound
verdicts read the rows). The committed-bytes predicate cannot tell forged orchestrator records from real ones (control
C2-K3 passes it); `transcripts_bound` is reported outside the predicate. C1's namespace legs leave the mount-table,
uid_map and script-path channels open (QUALITY 90 "named open"); control C1-K7 (the real arm only when
`/proc/self/mountinfo` shows tmpfs on `/var/lib`) is recorded as that limit.

Pre-data controls (scored with the frozen counters before any seat; scripts
`.ufo/waves/round-44/controls/run_controls_c1.py` sha256 `f30f5fd90d9a85990b1a1a7581b463b81eb46383b3e790ac266fc4a1881dd1e2`
and `run_controls_c2.py` sha256 `ad7845c461a678284638bdc56c66f7ab92650aa3c52f70643989142b86c46522`; candidate bytes
`controls/candidate-tsukuroi-census.sh` sha256 `fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c` and
`controls/c2-candidate/`): C1 — K0 do-nothing, K1 constant emitter, K2 env-gated, K3 uid-gated, K4 count-only (no
readability), K5 no orphan check, K6 `_tmp` counted as a record, K10 name-gated (the host's own fsid), K11 the
selftest parameter (five `R44-C1` labels), K12 unwired (main never prints), K13 misplaced (before STORAGE): each must
FAIL; K8 candidate must PASS; K7 mount-gated recorded. C2 — K0 do-nothing, K1 scripted writer, K2 K1 + results
without dispatch, K4 one `fails`, K5 one `partly` without residual, K6 mention-not-assertion, K7 content-free, K8 SR7
without ioctl.c, K9 a quote line shifted, K10 id↔file mismatch, K11 no pointer, K12 S242 `queued`, K13 report first
line differs, K14 padded verdict line, K15 blank-line-prefixed verdict, K16 contradictory JSON `verdict`, K17 S244
only in the source line's prose, K18 SR9 without a host line: each must FAIL; K3 forged records and K19 `partly` +
bound residual `holds` must PASS. Battery lines: `controls/battery-summary-c1.jsonl`, `battery-summary-c2.jsonl`
(each `should_fail_accepted 0, control_accepted 1`).

Causal separability: C1 touches `tools/tsukuroi-census.sh` only (plus its promotion notes in PROVINCE/README after
measurement); C2 touches the r44 entry, the r43 entry's header line, `corpus/SOURCES.md` and frozen snapshots. Neither
counter reads the other's surface: the C1 counter scores the census at REV; the C2 counter reads the entry, the
registry, the snapshots and the wave-2 records at REV.

## Round 44 — measured outcome (2026-10-26, author-side; non-author closure pending)

Measured revision `fbfef071e5aa88df03027716e1e1e0cc7982ab1c` (wave-2 integration); frozen counters unchanged since
the freeze commit `1d2afffe` (sha256 as declared). Receipts: `.ufo/waves/round-44/after/c1-final-fbfef071.jsonl`,
`c2-final-fbfef071.jsonl` (both via `tools/run-receipt.py`); before receipts `.ufo/waves/round-44/before/`.

| Claim | Axis | Before (base `98020ece`) | After (`fbfef071`) | Predicate | Verdict |
|---|---|---|---|---|---|
| C1 | coverage | FAIL: no SCRUB line (`correct 0`, `wired_ok 0`, `live_agree 0`, `selftest_r44 0`) | PASS: cases 16, correct 16, identity_ok 1, wired_ok 1, live_agree 1, selftest_pass 1 (148/148), selftest_r44 16 | as declared | **PASS** — kill rules not fired: PLANE/rollup/exit unchanged base vs tip (w2/C1ExecFinalPlaneDiff, only live PSI/memory drift that recurs within one revision), predecessor storage counters unchanged (w2/C1ExecFinalPrior), live arm window read-only (29 syscalls, w2/C1ExecFinalLiveRead) |
| C2 | depth | FAIL: rows 0 | FAIL: rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, novelty_base_hits 0, pointer_ok 1, **verdicts_ok 0** | as declared | **FAIL** — the counted wave-2 seats read SR7 holds/holds, SR8 partly(rev)/holds(crit), SR9 partly(rev)/holds(crit); no residual seat ran, so SR8 and SR9 fail the partly rule; SR7's reviewer output was a JSON string (not an object) and SR9's critic JSON carried a contradictory `verdict: supports` — both unbound by design (controls K14-K16); SR7 also lacks a bound reviewer |

C2 kill rule: no bound counted verdict `fails`. The two `partly` narrowings (SR8 host reading names the fsid, not "the
root filesystem"; the `memparse` suffix semantics marked [inference]; SR9 timer-only package ownership) were applied
after the counted reads at `fbfef071`; they are unjudged by any counted seat and the claim stays FAIL. Depth ordinal
unchanged (8). C1 moves the unprivileged scrub-record view Frontier → Core (`PROVINCE.md` "Round-44 promotion");
coverage stays 9 (saturation band).
Recorded counter limits from the waves (open, routed to round 45): C1 live leg accepts a gated constant (script-path
and process-ancestry channels PASS the frozen counter: w2/C1CritFinalEvasion; w1/C1CritEvasion F1); C2 json
last-wins duplicate keys, CR-stripping and substring quotes (w1/C2MutBinding, w1/C2RevCounter F1/F2); the glob
mutant g1 survived both counter and selftest at `8eee79db` and is now killed by the selftest fixture
`btrfs-scrub@home-timer` (148/148 at `fbfef071`).
No-harm: 0 deleted files; SCORECARD append-only; sources census exit 0 (`after/sources-census-final.txt`);
registry coverage 70/70 at `3a1c6b5c` onward (red 68/70 between the declaration and `3a1c6b5c`, the round-27 class,
repaired); adjacency anchor IN-109 moved by the census insertions (w2/CritNoHarmFinal) — recorded, routed;
self-assessment re-derived in the table below. **retired:** none.

## Axes — current self-assessment (round 44 final measured surface)

Each count is re-derived from the committed lane tree at the round-44 outcome commit (the commit that lands this table); ordinals unchanged.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 65 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 4230 `wc -l` / 1156 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 64 files (`find corpus/lessons -type f | wc -l`); round-43 C2 verified (SR1, SR3, SR6 bound holds; SR3 through the residual); no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 452 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus the verdict-neutral STORAGE line; the scrub record's unprivileged view is Core since round 44 (SCRUB line; content and running state stay Frontier; earlier: the scrub record stayed Frontier (round 43 re-grounds it from source, no Frontier move). | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (148 cases, 148 passed, 0 failed); `bash tools/boot-chain-audit.sh --selftest` prints `PASS total=49 failed=0`; round-43 C1 verified (boot-input freshness decides on find's output); `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; round 43 re-fetched S237 and S240 byte-identical (`w1/C2ExecLiveSources.md`, `w2/SrcReopenS237.md`, `w2/SrcReopenS240.md`), re-ran the S241 capture (`w2/SrcReopenS241.md`) and checked the Arch kernel patch set (no `fs/` file). | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; mismatches 0 required at the round-44 outcome commit. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; round 43 moved no live sibling pin (four frozen sibling records pin `boot-chain-audit.sh` lines, reported, `w2/AdjFinal.md`) and restates the round-42 tameshi and mori handoffs; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |

## Capabilities — current full evidence set (round 44)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates opened tier-scoped sources with anchors, rejections, paths, search log and unopened leads | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT, STORAGE and SCRUB lines; selftest prints PASS (148 cases, 148 passed, 0 failed) | `tools/tsukuroi-census.sh`; `.ufo/evidence/round-1-kaika/scout-live.md`; `.ufo/evidence/round-1-kaika/after.md` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations while preserving fixture isolation and policy boundaries | `.ufo/waves/round-12/resumed/after.json`; `.ufo/waves/round-12/resumed/selftest-after.json`; `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | round 12 |
| boot-chain-audit | Reads and types initramfs root paths against the selected firmware entry, producing a per-entry next-boot verdict; since round 43 its boot-input freshness check decides on find's output, so a missing start point or unreadable directory no longer opens the BOOTED-OBSERVED gate | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt`; `.ufo/waves/round-43/after/c1-after-c395491.jsonl` | round 17 |
| storage-error-counter-reader | Reads every btrfs device's five error counters from sysfs and prints one verdict-neutral STORAGE line (HEALTHY/DEGRADED/BLOCKED with nonzero pairs and reason tokens), demonstrated on fixtures, the live host and production-path namespace views; since round 39 an absent or empty root is cross-checked against the mount table, since round 40 its selftest varies the mount-table literals, since round 41 four held-out table shapes | `tools/tsukuroi-census.sh`; `.ufo/waves/round-38/after/c1-final-b0005ae.json`; `.ufo/waves/round-39/after/c1-final-a2d7aad.jsonl`; `.ufo/waves/round-40/after/c1-final-aad0113.jsonl`; `.ufo/waves/round-41/after/c1-after-568c397.jsonl` | round 38 |

One header row (R43-CAP-HEADER-DUP; QUALITY 92): `awk '/^## Capabilities — current full evidence set \(round 43\)/{f=1;next} /^## /{f=0} f&&/^\| Capability \|/{n++} END{print n+0}' SCORECARD.md` prints 1.

- **planned (next round):** (1) coverage — a verdict-neutral scrub-record census arm for the unprivileged-readable
  subset (directory, file stat, `scrub_speed_max`; never the running state, SR6) as Frontier → Core;
  (2) depth — the ioctl success direction (`btrfs_scrub_progress`, Linux `fs/btrfs/scrub.c`) as a sourced row;
  (3) operability — the routed census items (`:746` lookup selftest case past the pipe buffer, the five single-line
  probe readers). Draft text: `.ufo/waves/round-43/w2/ConnRound44.md`.
- **retired:** none.

## Round 45 — declaration (2026-10-27, base `5bbd5ff588120fd8e7c744695351a6978b4241c1`, before any seat)

Round 44 was closed `rejected-harmed` (`corpus/lessons/round-44-verifier-spotcheck.md` §2: C1 coverage verified, C2
depth FAIL, adjacency harmed by the unrepinned IN-109 anchor). The base is the lane tip at round start as `jj-lane.sh
state` printed it (`local=5bbd5ff5…`, which carries that spot-check). Ordinals at base: depth 8, coverage 9,
operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest; C2 works depth. Adjacency
stays unclaimed: the round repairs its round-44 harm (routed defect D1, IN-109 `found_line` 2468 → 2582, committed
with this declaration before any seat) and C1 carries the adjacency gate as a kill rule, so a census edit that moves an
anchored line without a repin fails C1 (the round-44 mistake, shown able to fail by control C1-K7). Saturation 9 /
window 3 unchanged. Gates at base (receipts `.ufo/waves/round-45/before/`): adjacency anchors FAIL (IN-109),
self-assessment FAIL 1 mismatch (K10, the closure's spot-check file makes 65 lessons), census selftest PASS 148/148,
sources census exit 0. The planned row of round 44 was stale (D4); this round takes its item (3) as C1 and replaces its
items (1)-(2) (landed or failed in round 44) with C2, which grounds the three `[inference]` marks of the round-44 entry.

| Claim | Axis | Surface moved | Counter (frozen) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | operability | `tools/tsukuroi-census.sh`: the five production readers that keep the first line of a captured output (`probe_systemd` `state` and the timer `Result` `r`, `probe_drivers` `driver`, `probe_journal` `t_word` and the timer `ActiveState` `r`) stop using `printf '%s\n' "$CAP_OUT" \| head -n1` in an assignment, which under `set -euo pipefail` kills the census with exit 141 once the output passes the pipe buffer (R41-CENSUS-PIPEFAIL-692 class, routed since round 42); six selftest cases labelled `(R45-C1)` put the deciding first line before ~150 KB of padding, and the sixth drives the foreign-baseline lookup (full read since round 42) past the pipe buffer with the deciding row last | `python3 tools/score-census-readers-r45.py --revision <REV> --scratch <DIR>` (legs: lexical, per-site equivalence against the base statement on drawn outputs up to 300 KB, selftest, six revert mutants, adjacency gate) | FAIL: lexical_hits 5, equiv_ok 0, selftest_r45 0, revert_killed 0, adjacency_ok 0 | `lexical_hits == 0 and sites_found == 5 and equiv_ok == 5 and selftest_pass == 1 and selftest_r45 >= 6 and revert_killed == 6 and adjacency_ok == 1` | any PLANE, HANDOFF, DRIFT, STORAGE, SCRUB or TSUKUROI_CENSUS line changes shape or the live exit code changes between base and the measured revision (other than live drift that recurs between two runs of one revision); any predecessor census counter (`score-scrub-arm-r44.py`, `score-storage-arm-r38.py`, `score-storage-arm-r38-q82.py`, `score-storage-hidden-r39.py`, `score-size-invariance-r42.py`, `score-bootinputs-r43.py`) goes PASS → FAIL; the census writes a file in live mode |
| C2 | depth (sourced: S246, S247, S248, S249 opened this round) | New entry `corpus/knowledge/btrfs-scrub-grounding-r45.md` rows GR1 (`memparse` as the `scrub_speed_max` write parser: base-0 radix, so a leading `0` is octal; one `K`..`E` suffix in either case, each a factor of 1024; overflow to `ULLONG_MAX`; trailing text `EINVAL`; a bare newline clears the limit), GR2 (a device replace runs `btrfs_scrub_dev` with `is_dev_replace` true on the source devid, and any non-replace scrub of that filesystem is refused with `EINPROGRESS` while `btrfs_dev_replace_is_ongoing`), GR3 (`systemctl stop` of the packaged scrub service under systemd v262: `KillSignal=SIGINT` to the whole control group, then SIGCONT, then SIGKILL after `TimeoutStopSec=`; on this host 5 s from the unowned drop-in `10-faster-shutdown.conf` `DefaultTimeoutStopSec=5s`), each grounding one round-44 `[inference]`; an appended `## Round-45` section in the round-44 entry (gate status pending, pointer); SOURCES rows S246-S249, used-by edits on S237, S242, S243, S244 | `python3 tools/check-scrub-grounding-r45.py --revision <REV>` (row quotes on digest-checked snapshots with a substantial-quote rule, proposition tokens, host lines, registry read inside `## Registry` with duplicate ids fatal, base ancestry required, novelty tokens, pointer, and per-row bound verdicts of the counted seats `C2RevGR<n>`/`C2CritGR<n>` in wave `w1` with residual `C2ResGR<n>` in wave `r1`) | FAIL: rows 0 | `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1` | any bound counted verdict `fails` without a bound residual `holds`; `novelty_base_hits > 0`; the round-43 sourced counter (`check-scrub-record-r43.py`) goes PASS → FAIL; a re-fetch of S246-S248 differs from `SHA256SUMS` |

Pre-data controls (scored with the frozen counters before any seat; scripts and candidate bytes under
`.ufo/waves/round-45/controls/`): C1 — K0 do-nothing, K1 `| head -1` evasion, K2 constant writer, K3 conversions
without cases, K4 cases without conversions, K5 S5 without the trailing-blank strip, K6 vacuous cases, K7 unrepinned
anchor drift (one line above the IN-109 case), K10 fixture-gated conversion: each must FAIL; K8 candidate and K9 the
`sed -n 1p` full-read alternative must PASS. C2 — K0 do-nothing, K1 scripted writer, K2 K1 + results without dispatch,
K4 one `fails`, K5 one `partly` without residual, K6 mention-not-assertion, K7 content-free statements, K8 GR2 without
dev-replace.c, K9 a quote line shifted, K10 id↔file mismatch, K11 no pointer, K12 S246 `queued`, K13 report first line
differs, K14 padded verdict line, K15 blank-line-prefixed verdict, K16 contradictory JSON `verdict`, K17 S247 dropped
from the source line, K18 GR3 without a host line, K20 gutted quote, K21 doctored duplicate registry row, K22
duplicate row in a fence, K23 duplicate `verdict_line` keys, K24 top-level array results, K25 orphan repository, K27 a
later contradicting verdict line, K28 held SR8 knowledge restated as GR1, K29 quotes as statements: each must FAIL;
K3 forged records, K19 `partly` + bound residual `holds` and K26 JSON-string outputs must PASS (K3 is the standing
limit: committed bytes cannot tell forged orchestrator records from real ones; `transcripts_bound` is reported
outside the predicate). Battery lines: `controls/battery-summary-c1.jsonl`, `battery-summary-c2.jsonl`.

Recorded limits (not claimed): C1's equivalence leg scores each site's first physical line only (a conversion split
over lines is scored on its first line); the seven masked or process-substitution `| head` readers (`:707`, `:832`,
`:997`, `:1196`, `:1517`, `:1531`, `:1817`) cannot kill the census (their status is ignored or `|| true`) and are not
claimed; the readers are latent defects on this host, whose outputs are far below the pipe buffer. C2's verdicts are
seat verdicts (the lane), not outside review.

Causal separability: C1 touches `tools/tsukuroi-census.sh` (and depends on the D1 anchor repin committed with this
declaration); C2 touches the r45 entry, the r44 entry's appended section, `corpus/SOURCES.md` and frozen snapshots.
Neither counter reads the other's surface: the C1 counter scores the census and the anchor gate at REV; the C2 counter
reads the entry, the registry, the snapshots and the wave records at REV.

### Round 45 — attempt-2 rebinding (2026-10-27, before any seat scored)

Attempt 1 (L1 `TsukuroiR45`) died with the orchestrator session at 2026-10-26 23:57:36 -03 while its one v2 wave `w1`
was filling (14/66 seats spawned and killed, 52 never spawned, 0 outputs, 0 reports: `.ufo/waves/round-45/w1-results.json`,
`w1.ready.dispatched` ABANDONED); the orchestrator salvage commit `5b3029bf` holds those records. No seat scored. The
dispatcher never takes a spent `.ready` twice, so attempt 2 (L1 `TsukuroiR45a2`) dispatches the same items as wave
`a2w1` (residual, if any, `a2r1`). The C2 counter's two wave-name literals follow: `tools/check-scrub-grounding-r45.py`
now binds the counted seats to `a2w1` and residuals to `a2r1` (constants `VERDICT_WAVE`, `RESIDUAL_WAVE`; sha256
`7e373196…f70d` at the freeze → `a1eb402d…1331`); predicate, kill rule, target, seat names, roles and every other byte
of the rule are unchanged. The C1 counter is unchanged (sha256 `fe0e31e2…bd50`). Receipts in
`.ufo/waves/round-45/controls-a2/`: the C2 battery re-run with the rebound names gives field-identical results on all 30
controls (`should_fail_accepted` 0, K3/K19/K26 PASS as before), and the salvage tip `5b3029bf` scores FAIL
`verdicts_ok` 0 under both the frozen and the rebound counter (attempt-1 `w1` records bind nothing).

## Round 45 — measured outcome (2026-10-27, author-side; non-author closure pending)

Measured revision `44560592857660a20c6a2b296fa14fa7a90464b5` (integration of wave `a2w1` and residual `a2r1`); C1 counter sha256 `fe0e31e2…3250bd50`
unchanged since the freeze `ea6e0ee3`; C2 counter `a1eb402d…d011331` (the attempt-2 rebinding `057c1804` of the frozen
`7e373196…f70d`). Receipts: `.ufo/waves/round-45/after/c1-final-44560592.jsonl`, `c2-final-44560592.jsonl` (both via
`tools/run-receipt.py`); before: `controls/C1-K0.jsonl` (the base bytes), `before/c2-before-a2.jsonl`.

| Claim | Axis | Before (base `5bbd5ff5`) | After (`44560592`) | Predicate | Verdict |
|---|---|---|---|---|---|
| C1 | operability | FAIL: lexical_hits 5, equiv_ok 0, selftest_r45 0, revert_killed 0, adjacency_ok 0 | PASS: lexical_hits 0, sites_found 5, equiv_ok 5, selftest_pass 1 (154/154), selftest_r45 6, revert_killed 6, adjacency_ok 1 | as declared | **PASS** — kill rules not fired (`a2w1/C1ExecPlaneDiff.md`, `C1ExecPriorStorage.md`, `C1ExecPriorRecent.md`, `C1ExecLiveRead.md`; census bytes unchanged after `18389f44`) |
| C2 | depth | FAIL: rows 0 | FAIL: rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, novelty_base_hits 0, pointer_ok 1, **verdicts_ok 0** | as declared | **FAIL** — no counted verdict bound: C2RevGR1 died without a yield; the five other counted yields are unbindable shapes (JSON objects with `verdict` and no `verdict_line`, or text whose first line is not the verdict line); the orchestrator kept no output for them (`a2w1-results.json` `output` null). Scored with the yields recovered verbatim from the transcripts the binding is still 0 (`a2w1/L1-recovery/`). GR1-GR3 pending |

C2 kill rules: no bound counted `fails`; `novelty_base_hits` 0; `check-scrub-record-r43.py` PASS at base and at
`44560592` (`a2w1/RevGatesAll/`, `after/gate-check-scrub-record-r43-44560592.jsonl`); S246-S248 re-fetched
byte-identical to `SHA256SUMS` (`a2w1/C2ExecLiveSources.md`). The report first lines of the counted seats read GR1
`holds` (critic), GR2 `partly`/`partly`, GR3 `holds`/`holds`; GR2 was narrowed twice after them and read by the
uncounted residual seats (`a2r1/ResRevGR2.md` `holds`, `a2r1/ResCritGR2.md` one finding, applied at `cd1b3a03`).
No ordinal moves: depth stays 8, operability stays 9 (saturation band).
No-harm at `44560592` (`after/gate-*-44560592.jsonl`): registry coverage PASS 72/72 (the 70/72 FAIL that the two new
counters opened at `18389f44`, `a2w1/RevGatesAll.md`, closed by the round45 table at `0503400b`); knowledge-header,
appended-notices, section-citations, adjacency-anchors, adjacency-overlap PASS; scrub-record-r44, edit-contract and
review-snapshots FAIL as at base; sources census exit 0, 40 W04, 249 rows (`after/sources-census-final.txt`); every
round-45 change to an older file is an append, except the new-this-round rows S246/S247 (teaches, ranges) and the
round-45 SKILL sections. Self-assessment: re-derived in the table below. **retired:** none.

## Axes — current self-assessment (round 45 final measured surface)

Each count is re-derived from the committed lane tree at the round-45 outcome commit (the commit that lands this table); ordinals unchanged.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 66 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 4424 `wc -l` / 1241 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 66 files (`find corpus/lessons -type f | wc -l`); round-43 C2 verified (SR1, SR3, SR6 bound holds; SR3 through the residual); round-44 SR7-SR9 and round-45 GR1-GR3 pending (their depth gates FAILED on binding); no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 466 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus the verdict-neutral STORAGE line; the scrub record's unprivileged view is Core since round 44 (SCRUB line; content and running state stay Frontier; earlier: the scrub record stayed Frontier (round 43 re-grounds it from source, no Frontier move). | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (154 cases, 154 passed, 0 failed); `bash tools/boot-chain-audit.sh --selftest` prints `PASS total=49 failed=0`; round-43 C1 verified (boot-input freshness decides on find's output); round-45 C1 PASS (five first-line readers by parameter expansion, six `(R45-C1)` cases past the pipe buffer); `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; round 45 re-fetched S237 and S242-S244 byte-identical (`a2w1/SrcGateReopen.md`) and re-ran the S249 capture (`a2w1/C2ExecHostRecheck.md`); round 43 re-fetched S237 and S240 byte-identical (`w1/C2ExecLiveSources.md`, `w2/SrcReopenS237.md`, `w2/SrcReopenS240.md`), re-ran the S241 capture (`w2/SrcReopenS241.md`) and checked the Arch kernel patch set (no `fs/` file). | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; mismatches 0 required at the round-45 outcome commit. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; the round-44 IN-109 harm repaired by the round-45 repin (`check-adjacency-anchors.py` PASS at `44560592`); round 43 moved no live sibling pin (four frozen sibling records pin `boot-chain-audit.sh` lines, reported, `w2/AdjFinal.md`) and restates the round-42 tameshi and mori handoffs; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |

## Capabilities — current full evidence set (round 45)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates opened tier-scoped sources with anchors, rejections, paths, search log and unopened leads | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT, STORAGE and SCRUB lines; selftest prints PASS (154 cases, 154 passed, 0 failed) | `tools/tsukuroi-census.sh`; `.ufo/evidence/round-1-kaika/scout-live.md`; `.ufo/evidence/round-1-kaika/after.md` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations while preserving fixture isolation and policy boundaries | `.ufo/waves/round-12/resumed/after.json`; `.ufo/waves/round-12/resumed/selftest-after.json`; `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | round 12 |
| boot-chain-audit | Reads and types initramfs root paths against the selected firmware entry, producing a per-entry next-boot verdict; since round 43 its boot-input freshness check decides on find's output, so a missing start point or unreadable directory no longer opens the BOOTED-OBSERVED gate | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt`; `.ufo/waves/round-43/after/c1-after-c395491.jsonl` | round 17 |
| storage-error-counter-reader | Reads every btrfs device's five error counters from sysfs and prints one verdict-neutral STORAGE line (HEALTHY/DEGRADED/BLOCKED with nonzero pairs and reason tokens), demonstrated on fixtures, the live host and production-path namespace views; since round 39 an absent or empty root is cross-checked against the mount table, since round 40 its selftest varies the mount-table literals, since round 41 four held-out table shapes | `tools/tsukuroi-census.sh`; `.ufo/waves/round-38/after/c1-final-b0005ae.json`; `.ufo/waves/round-39/after/c1-final-a2d7aad.jsonl`; `.ufo/waves/round-40/after/c1-final-aad0113.jsonl`; `.ufo/waves/round-41/after/c1-after-568c397.jsonl` | round 38 |

One header row (R43-CAP-HEADER-DUP; QUALITY 92): `awk '/^## Capabilities — current full evidence set \(round 45\)/{f=1;next} /^## /{f=0} f&&/^\| Capability \|/{n++} END{print n+0}' SCORECARD.md` prints 1.

- **planned (next round):** (1) depth — re-bind GR1-GR3 under a counter whose counted channel the seat writes
  verbatim (the report first line, QUALITY 93) with pre-data controls for the yield shapes of rounds 44-45, so the
  pending rows can be admitted or refused; (2) operability — the round-45 C1 review gaps: case-level CR/blank pinning
  at `:1003`/`:1085`-class sites and a declared kill-rule universe (`a2w1/C1CritCases.md`, `C1RevKillRules.md`);
  (3) calibration — the counter-review survivors of `a2w1/C2MutBinding.md` (look-alike contradiction, cross-role
  duplicate, sibling JSON key). Routed: R45-D7-CITATION-HALF-CLOSED.
- **retired:** none.

## Round 46 — declaration (2026-10-27, base `2042117cfb724170772f4c128cc2ddba0b61d817`, before any seat)

Round 45 was closed `rejected-honest-stop` (`corpus/lessons/round-45-verifier-spotcheck.md` §2: C1 operability
improved; C2 depth FAIL, `verdicts_ok` 0, because no counted yield bound; nothing harmed). The base is the lane tip at
round start (`jj-lane.sh state`: `local=2042117c…`, it carries that spot-check). Ordinals at base: depth 8, coverage 9,
operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency tied lowest; C2 works depth. Saturation 9 /
window 3 unchanged. Round-start receipts (`.ufo/waves/round-46/before/`): sources census exit 0, 249 rows, 40 W04, run by
this attempt at its own start (routed D4); the round-45 C2 counter's non-verdict legs at base: rows 3, quotes_ok 3,
props_ok 3, host_ok 3, sources_ok 1, novelty 0, pointer_ok 1, verdicts_ok 0 (`c2r45-legs-base.json`). The round-45
planned row's item (1) is C2; item (2) (case-level CR pinning at the converted readers) and item (3) (counter-review
survivors) are not taken: C1 takes instead the operability ceiling every axes table since round 11 names, D12
`--identity` not landed.

| Claim | Axis | Surface moved | Counter (frozen) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | operability (capability `census-identity`; sourced: S250, S251 opened this round) | `tools/tsukuroi-census.sh` gains `--identity` (routed debt D12, open since round 10: `closeout-r11.md:42-44`, `:261-262`): one stdout line `TSUKUROI_CENSUS_IDENTITY: version=… sha256=… md5=… bytes=… lines=… planes=… exit_map=… verified=…` naming the bytes the running bash process executes, read through the script descriptor bash holds (S250 `shell.c:1700`, `general.c:696-700`) re-opened as `/proc/$$/fd/<n>` (S251) and only when it resolves to the invoked file; a script read from stdin or a pipe prints `unverifiable` for the four byte fields and `verified=no`; `--identity` takes no other argument; selftest cases labelled `(R46-C1)`; new entry `corpus/knowledge/census-identity-r46.md` | `python3 tools/score-census-identity-r46.py --revision <REV> --scratch <DIR>` (legs: identity line vs the counter's own digests of REV's census bytes, an appended-line copy, a symlink, stdin and process-substitution with a decoy `bash` file in cwd, a file replaced after bash opened it, CLI refusals, no write in cwd/TMPDIR, selftest PASS and `(R46-C1)` PASS lines) | FAIL: identity_ok 0 (`--identity` is an unknown argument, exit 2) | `identity_ok == 1 and tracks_ok == 1 and symlink_ok == 1 and unverifiable_ok == 1 and cli_ok == 1 and nowrite_ok == 1 and selftest_pass == 1 and selftest_r46 >= 4` | any PLANE, HANDOFF, DRIFT, STORAGE, SCRUB or TSUKUROI_CENSUS line changes shape or the live exit code changes between base and the measured revision (other than live drift that recurs between two runs of one revision); any of these census counters goes PASS → FAIL base → measured revision: `score-census-readers-r45.py`, `score-scrub-arm-r44.py`, `score-bootinputs-r43.py`, `score-size-invariance-r42.py`, `score-selftest-mounts-r41.py`, `score-selftest-literals-r40.py`, `score-storage-hidden-r39.py`, `score-storage-arm-r38-q82.py`, `score-pacnew-arm-r35b.py`, `score-census-handoff-r32.py` (this list is the whole kill universe; `score-storage-arm-r38.py` is FAIL at base and stays outside it); the census writes a file in live or identity mode; `check-adjacency-anchors.py` goes PASS → FAIL; a census line at or before `:3383` moves |
| C2 | depth (sourced: S246-S249) | `corpus/knowledge/btrfs-scrub-grounding-r45.md` rows GR1-GR3 (pending since round 45) are admitted: counted seats re-read each row against its digest-checked snapshots and write their verdict as the first two lines of their own report file, bound to the exact row bytes; on PASS the entry gains `## Gate status — round 46 (GR1-GR3 admitted)`, `SKILL.md` a `## Scrub grounding — round 46 admission` section and `corpus/README.md` an `admitted round 46` line | `python3 tools/check-scrub-admission-r46.py --revision <REV>` (legs: the frozen round-45 counter run from REV (sha256 `a1eb402d…1331`) for every non-verdict leg; per row the counted seat universe `V46RevGR<n>a/b` (reviewer), `V46CritGR<n>a/b` (critic) and residual `V46ResRevGR<n>` (reviewer), `V46ResCritGR<n>` (critic), bound by seat name across every round-46 `<wave>-dispatch.json` (no wave name is bound, routed D5) plus its `<wave>-results.json` entry and its report `.ufo/waves/round-46/<wave>/<seat>.md` whose first line is exactly `ROW GR<n> VERDICT: <holds|partly|fails>` and second line exactly `SECTION SHA256: <hex>`; admission marks) | FAIL: r45_legs_ok 1, verdicts_ok 0, marks_ok 0 | `r45_legs_ok == 1 and verdicts_ok == 3 and marks_ok == 3` (a row is ok when no bound seat reads `fails` on any bytes and at least two bound seats on the row's current bytes all read `holds`) | any bound counted `fails`; a GR row changed without every bound verdict on its current bytes re-read; `check-scrub-record-r43.py` goes PASS → FAIL; S246-S248 no longer re-fetch byte-identical to `.ufo/waves/round-45/frozen/src/SHA256SUMS` |

Pre-data controls (scored with the frozen counters before any seat; scripts and candidate bytes under
`.ufo/waves/round-46/controls/`): C1 — K0 do-nothing (base bytes), K1 constant writer (the base file's true digests
hardcoded), K2 path hasher (hashes `$SELF` without the descriptor check), K3 identity without `(R46-C1)` cases, K5 line on
stderr, K6 `grep -c .` line count, K7 a banner line, K9 `--identity` silently beating other flags: each must FAIL; K8 the
candidate must PASS (`battery-summary-c1.jsonl`). C2 — K0 do-nothing, K1 marks only, K2 reports without dispatch, K4 a
`partly` on current bytes, K5 stale hashes, K6 JSON first line, K7 preamble line, K8 a `fails` on old bytes, K9 a name
outside the universe, K10 a seat dispatched in two waves, K11 wrong agent, K12 a contradicting verdict line, K13
content-free body, K14 no `file:line` citation, K16 a broken quote (round-45 legs), K17 no results file, K19 a duplicate
JSON key, K20 CR on the first line, K21 verdicts without marks: each must FAIL; K3 forged records (the standing limit:
committed bytes cannot tell forged orchestrator records from real ones), K15 the same under an arbitrary wave name (D5)
and K18 `partly` on old bytes answered by both residual seats on amended bytes must PASS (`battery-summary-c2.jsonl`).

Pre-freeze counter fix (before any seat): the first C1 counter draft let control K2 (a path hasher) PASS, because
with `${BASH_SOURCE[0]:-}` the stdin and pipe cases never name a regular file, so hashing the path and hashing the
descriptor agree there (`controls/battery-summary-c1-draft1.jsonl`, K2 `as_expected` false). The frozen counter adds
the case that separates them — the script renames a decoy over its own path on its first line, so the path names new
bytes while bash still reads the old inode — and K2 now FAILs (`battery-summary-c1.jsonl`, 9/9 as expected). The
candidate gained the matching selftest case. C2 battery: 22/22 as expected (`battery-summary-c2.jsonl`).

Seat verdict channel (routed: R45-C2-BINDING-CHANNEL, orchestrator note of the round-46 dispatch): the counter reads
only the seat's own report file. The wave spec states the two exact first lines and nothing a seat yields is read.

Causal separability: C1 touches `tools/tsukuroi-census.sh`, the new identity entry and S250/S251; C2 touches the r45
entry's appended gate section, a SKILL section and a README line. The C1 counter reads only the census at REV; the C2
counter reads the entry, the registry, snapshots, SKILL.md, README and the round-46 wave records. Neither reads the
other's surface.

## Round 46 — measured outcome (2026-10-27, author-side; non-author closure pending)

C1 measured at `61e067408ad73c144e42ea8f2ec5ed3f333d7e2e` (census sha256 `ac4e38ff…f48e`; counter sha256 `7c406eb5…54ba`
unchanged since the freeze `72cc2609`); C2 measured at the outcome commit (receipt `.ufo/waves/round-46/after/c2-final.jsonl`;
counter `28c409be…11d8` unchanged since the freeze). Before receipts: `.ufo/waves/round-46/before/c1-before-base.jsonl`,
`c2-before-base.jsonl`.

| Claim | Axis | Before (base `2042117c`) | After | Predicate | Verdict |
|---|---|---|---|---|---|
| C1 | operability (capability `census-identity`) | FAIL: identity_ok 0, cli_ok 0, unverifiable_ok 0, selftest_r46 0 | PASS: identity_ok 1, tracks_ok 1, symlink_ok 1, unverifiable_ok 1, cli_ok 1, nowrite_ok 1, selftest_pass 1 (162/162), selftest_r46 8 (`.ufo/waves/round-46/l1/c1-61e06740.jsonl`; also PASS at `a4477049`, `l1/c1-impl-a4477049.jsonl`) | as declared | **PASS** — kill rules: PLANE/rollup lines and exit 2 unchanged base vs final apart from drivers mem counters that also differ between two base runs (`l1/planediff/`); no live write (`w1/C1ExecLiveWrite.md`); adjacency anchors PASS and lines ≤3383 moved only in place (`w1/C1ExecAdjacency.md`); counters PASS→PASS where measured (`w1/C1ExecPriorC.md`, `l1/killrule/`) |
| C2 | depth | FAIL: r45_legs_ok 1, verdicts_ok 0, marks_ok 0 | FAIL: r45_legs_ok 1, verdicts_ok 2 (GR1, GR3), marks_ok 0 | as declared | **FAIL** — GR2 read `partly` on its narrowed bytes by `r1/V46ResCritGR2.md`; no counted seat left (R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT). No admission mark written; GR1-GR3 pending |

No ordinal moves: operability stays 9 (saturation band; the D12 ceiling is closed), depth stays 8. **retired:** none.

## Axes — current self-assessment (round 48 final measured surface)

Re-stated 2026-10-28 at the round-48 final tree; ordinals unchanged. Depth C2 did not verify, so no depth increase; C1 operability and C3 calibration are measured separately in the Round 48 outcome below. Counts re-derived with commands in each cell.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 67 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 4546 `wc -l` / 1323 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 72 files (`find corpus/lessons -type f | wc -l`); GR1-GR3 admission C2 FAIL at frozen counter; no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 480 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus verdict-neutral STORAGE; no coverage claim this round. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (166 cases, 166 passed, 0 failed) at round-48 freeze; `--identity` landed (feature present; round-46 admission withdrawn because the r40 kill rule fired); `bash tools/boot-chain-audit.sh --selftest` prints `PASS total=49 failed=0`; TMPDIR behavior receipt `.ufo/waves/round-48/after/c1-final.json`. | round 11 (terminal closeout); unchanged |
| freshness | 9 | S240 `ioctl.c` live re-open 2026-10-28, byte-identical to pinned snapshot; S251 proc-fd page re-opened by w2 seat; S253 Issue 8 opened; end census exit 0. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision 71493caa5cf5dce1c109b69ba526989d17723a7d` → checked 27, mismatches 0, PASS (`.ufo/waves/round-48/after/c3-final.json`); before restatement K10/K13/K17 = 3. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (PROVINCE `| ID | Finding` table; findings ADJ-01..07); portable OUT-001..010 anchors remain; `check-adjacency-anchors.py --revision d7843b3a` PASS after IN-109 found_line 2593→2642 repin. | fleet round 1; unchanged |

## Capabilities — current full evidence set (round 48)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates opened tier-scoped sources with anchors, rejections, paths, search log and unopened leads | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT, STORAGE and SCRUB lines; selftest prints PASS (166 cases, 166 passed, 0 failed) at round-48 freeze | `tools/tsukuroi-census.sh`; `.ufo/evidence/round-1-kaika/scout-live.md`; `.ufo/evidence/round-1-kaika/after.md`; `.ufo/waves/round-48/after/c1-final.json` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations while preserving fixture isolation and policy boundaries | `.ufo/waves/round-12/resumed/after.json`; `.ufo/waves/round-12/resumed/selftest-after.json`; `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | round 12 |
| boot-chain-audit | Reads and types initramfs root paths against the selected firmware entry, producing a per-entry next-boot verdict; since round 43 its boot-input freshness check decides on find's output | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt`; `.ufo/waves/round-43/after/c1-after-c395491.jsonl` | round 17 |
| storage-error-counter-reader | Reads every btrfs device's five error counters from sysfs and prints one verdict-neutral STORAGE line, demonstrated on fixtures, the live host and namespace views | `tools/tsukuroi-census.sh`; `.ufo/waves/round-38/after/c1-final-b0005ae.json`; `.ufo/waves/round-41/after/c1-after-568c397.jsonl` | round 38 |

- **planned (next round):** depth — correct GR1/GR2 clauses identified by the round-48 counted critics and use a counter that consumes the actual orchestrator `w2-results.json` schema; operability — correct the stale `/tmp` comment and add summary diagnostics for fd-band exhaustion; calibration — retain the 27-check zero-mismatch state at the next landed revision.
- **retired:** none.


## Round 47 — declaration (2026-10-27, base `916019057147d7e9ba6b137647b2cee26decf4b8`, before any seat)

Fresh-start round: rounds 44, 45 and 46 were closed `rejected-harmed`, `rejected-honest-stop`,
`rejected-harmed` (their spot-checks read before any claim was declared). Ordinals at base: depth 8,
coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency tied lowest;
C1 works depth (the round-46 planned row item 1), C2 works operability (item 2). Saturation 9 / window 3.
Round-start receipts (`.ufo/waves/round-47/before/`): sources census exit 0 at this attempt's own start
(routed D4); C1 before at base: `verdicts_ok 0, marks_ok 0`; C2 before at base: selftest under a
space `TMPDIR` FAILs 13/162 (149 failed, rc 1), space-free PASS 162/162.

| Claim | Axis | Surface moved | Counter (frozen) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | depth | `corpus/knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3 admitted: GR2 amended pre-wave per `r1/V46ResCritGR2.md` (the filesystem-closing `-EAGAIN` return scrub.c:3094-3095 leads the ordering; the suspend sentence narrowed to the unmount path dev-replace.c:1143-1144), then counted seats re-read each row and bind verdicts as the first two lines of their own reports; the rule is sized for two amendment rounds (per-row admission; residual generations `R47Res{,2}{Rev,Crit}GR<n>`) and the counter closes `w1/C2RevCounter.md` F1-F3 and `w1/C2CritControls.md` K22/K23 | `python3 tools/check-scrub-admission-r47.py --revision <REV>`; predicate `structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3` (F1: fail closed on an inner `## ` line or a duplicated row header; F2: marks pinned exact / negation-rejecting; F3: parse failures degrade to leg results, never empty stdout; K22: every entry Quote verified on its digest-pinned snapshot and every counted report citation must resolve; K23: bound report bodies pairwise distinct) | FAIL: `verdicts_ok 0, marks_ok 0` | PASS: all four legs 1/3/3/3 with the entry, SKILL.md and README marks written only after the counted seats bind | Live census output digits-stripped byte-identical base vs final; GR1/GR3 section hashes equal to base; adjacency anchors gate PASS; predecessor scrub counters (r42-r45) PASS→PASS where measured; sources census exit 0 at round end |
| C2 | operability (sourced: S252 opened this round) | `tools/tsukuroi-census.sh` selftest path contract (round-46 wave finding `w1/C1ExecRerunB.md`, planned row item 2): the harness builds its fixture tree under a `TMPDIR` that `root_locator_class` deliberately refuses (whitespace), so a space in TMPDIR failed 149 selftest cases at base; the harness now derives a classifiable fixture base (falling back to /tmp) and gains two `(R47-C2)` cases pinning the contract | `S=/fast/scratch/hyaku/tsukuroi-r47/c2-verify; mkdir -p "$S/t 2"; env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" bash tools/tsukuroi-census.sh --selftest` → `TSUKUROI_CENSUS_SELFTEST: PASS` rc 0 (case count 164 = 162 + 2 new) | FAIL: `PASS (13 cases, 13 passed…)` form reads `FAIL (162 cases, 13 passed, 149 failed)` rc 1 | PASS 164/164 rc 0 under a space TMPDIR, and PASS 164/164 space-free | Live census output digits-stripped byte-identical base vs final; `--identity` line shape unchanged (one `TSUKUROI_CENSUS_IDENTITY` line, `verified=yes`); all six `(R46-C1)` cases still pass; census exit map 0/1/2 unchanged; no committed tool writes under a hardcoded /tmp |

Pre-data controls (scored with the frozen counters before any seat; fixtures and scripts under
`.ufo/waves/round-47/controls/`): C1 — K0 do-nothing (base bytes → FAIL), K1 marks-only (marks
written with no counted seats → FAIL), K22a a counted report citing `cmdline.c:999999` (nonexistent
line → row not bound), K23a two byte-identical bound reports (→ `distinct_bodies false`), F1a an
inner `## ` line inside GR1 (→ `structural_ok 0`), F1b a duplicated `## GR2` header (→
`structural_ok 0`), F2a negating SKILL/README marks (`## Scrub grounding — round 47 admission
(WITHHELD…)` / `remains unadmitted round 47` → no credit), F3a a 200 000-deep nested dispatch JSON
(counter still prints one JSON line, exit ≠ 0 with in-band error): each must FAIL as declared;
K-pass the full candidate with forged valid holds is proven by the live integration itself, not by a
fixture. C2 — K0 do-nothing (base census under space TMPDIR → FAIL), K1 live output only (no
selftest change → still FAIL), K2 the guard removed but the pinning cases kept (cases must fail
under a space TMPDIR → FAIL), K-pass candidate → PASS. Receipts: `controls/battery-summary-r47.jsonl`.

## Round 46 — verifier correction (recorded in round 47)

The round-46 author-side C1 `PASS` and capability `census-identity` are superseded by the non-author spot-check at `corpus/lessons/round-46-verifier-spotcheck.md` §2: the frozen r40 kill term was not satisfied (PASS→FAIL), so C1 is **not verified** and the capability's admission is withdrawn. The implementation remains present, but no repertoire credit is claimed until a new round verifies it.

The round-46 C2 final receipt is `verdicts_ok 1, marks_ok 0` (`.ufo/waves/round-46/after/c2-final.jsonl`), not 2; GR1 was unbound because the required `w1-results.json` was absent. Round 46 remains `rejected-harmed`; no retrospective PASS or depth admission is claimed. The fixed 27-check self-assessment did not read these outcome rows, which is now explicit in the calibration evidence above.

## Round 47 — wrap status (2026-10-27; superseded only by a later settled verifier)

C1 depth is **not verified**: the counted GR2 critic `R47CritGR2a` reads the unmount-suspend wording as false (`w1/R47CritGR2a.md`), and the frozen K22 map omits S240 `ioctl.c:3190` cited in that report (`controls/k22-s240-map.txt`). The corrected GR2 text is present in the working tree but no settled residual cohort re-read it. C2's target is measured PASS (164/164 under a spaced TMPDIR; `.ufo/waves/round-47/before/selftest-space-after.txt`), but its frozen kill rule is **not verified** because the fix falls back to `/tmp` when the supplied TMPDIR contains characters the root locator refuses (`w1/C2ExecRerunA.md`); no admission is claimed. Round-47 axis ordinals remain unchanged; no capability is added. `WAVE-DONE w1` / `w1-results.json` were not received at wrap, so seat deaths and the final counted cohort remain unknown.

## Round 48 — declaration (attempt 2, 2026-10-28, base `5fdf062f969292736e36513e39f98b1b8de43635`, before any seat of the counted wave)

Fresh-start round (rounds 44-47 closed `rejected-harmed`, `rejected-honest-stop`, `rejected-harmed`, `rejected-honest-stop`).
Ordinals at base: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8 (depth and adjacency tied lowest).
Saturation 9 / window 3 (no waiver). **Attempt-1 incident (disclosed, void):** attempt 1 dispatched a 32-seat `w1` before any
freeze (wrong base `76819197` in its context vs the lane tip `5fdf062f`, no counter file, empty `frozen/src`); the orchestrator stopped
its seats; `.ufo/waves/round-48/w1*` are incident evidence only and are never scored. Attempt 2 froze claims, counters and controls
first (freeze commit named in `.ufo/waves/round-48/frozen/FROZEN.md`) and dispatches ONE v2 wave `w2`.
Round-start receipts: sources census exit 0 (`.ufo/waves/round-48/before/sources-census-start.txt`); C1 before at base: counter FAIL
(`controls/battery-summary-r48-c1.jsonl` K0); C2 before at base: counter FAIL (`controls/battery-summary-r48-c2.jsonl` K0);
C3 before at base: `check-self-assessment.py` mismatches 1 (K10).

| Claim | Axis | Surface moved | Counter (frozen) | Before at base | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | operability (sourced: new rows for proc_pid_fd(5) and the Bash manual, opened this round) | `tools/tsukuroi-census.sh` selftest TMPDIR contract: a TMPDIR with refused characters is reached through a `/proc/self/fd/24x` alias INSIDE that TMPDIR (the round-47 `st_base=/tmp` fallback, R47-C2-TMPDIR-FALLBACK, is removed); INT/TERM exit 130/143 with the fixture removed; a nonexistent TMPDIR fails fast; two `(R48-C2)` cases | `python3 tools/score-selftest-tmpdir-r48.py --revision <REV>` (wrapper-logged fixture location, six selftest runs) | FAIL at base blob sha256 `adb1b4ce…ceb41`: loc_ok 3, term_ok 0, static_ok 0, pass_ok 0 (164 cases) | `pass_ok == 4 and loc_ok == 4 and clean_ok == 4 and failfast_ok == 2 and term_ok == 1 and static_ok == 1` on the frozen blob sha256 `375aa737…2426` (166 cases under TMPDIR unset, /tmp, scratch, spaced) | any selftest case fails; the fixture lands under /tmp when TMPDIR is a writable non-/tmp directory; the live census output (digits stripped) or exit code differs from base; a predecessor check PASS->FAIL (adjacency anchors repinned in the implementation commits) |
| C2 | depth (lowest-tied axis; sourced: S237, S240, S242-S249 re-opened live this round) | `corpus/knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3 admitted by counted seats of ONE wave: 18 seats `R48RevGR<n>{a,b,c}` / `R48CritGR<n>{a,b,c}` bind through their own report files; GR2 already carries the round-47 correction; the K22 snapshot map gains S240 `ioctl.c`; a negative on the current row hash blocks the row whatever its citations | `python3 tools/check-scrub-admission-r48.py --revision <REV>` | FAIL at base: `structural_ok 1, quotes_ok 3, verdicts_ok 0, marks_ok 0` | `structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3` (row hashes frozen: GR1 `fe77ac76…`, GR2 `e0b391e1…`, GR3 `43430a14…`) | any counted seat on the current hash reads `partly`/`fails` (the claim FAILS honestly, no re-amend this round); the entry rows edited after the freeze; any predecessor scrub counter PASS->FAIL |
| C3 | calibration | SCORECARD self-assessment restated at round end against observed state: the lesson-file count (stated 70, observed 71 at base) and the census case count (164 -> 166 after C1) | `python3 tools/check-self-assessment.py --revision <REV>` (27 fixed checks, counter file unchanged this round) | FAIL at base: mismatches 1 (K10); 3 (K10, K13, K17) at the implementation commit until restated | status PASS, `checked` 27, `mismatches == 0` at the round's final lane revision | any axis ordinal raised without its counting command; `checked != 27` |

Pre-data controls (frozen counters; receipts under `.ufo/waves/round-48/controls/`): C1 — K0 base blob (FAIL), K2 the fix with the /tmp fallback restored (FAIL: loc_ok 3, static_ok 0), K3 the fix with the INT/TERM exit traps reverted (FAIL: term_ok 0), K4 base with only the usage text edited (FAIL), K-pass the fix (PASS) — `battery-summary-r48-c1.jsonl`. C2 — K0 do-nothing, K1 marks-only, K2 forged stale hash, K3/K3b/K3c/K3d a bound negative (bad citation / clean citations / self-contradiction / two-byte body) still blocks, K4 byte-identical bodies, K5 reviewers only, K6 unpinned citations, K7 reports without dispatch, K8 negating README mark, F1a stray `## ` header, K9 synthetic full cohort PASS — `battery-summary-r48-c2.jsonl`. C3 — K0 base, K0b implementation commit, K1 lesson count only, K2 case count only (all FAIL), K9 both fixed (PASS) — `battery-summary-r48-c3.jsonl`. Two defects of the counters' first drafts were caught by this battery before data (lesson `round-48.md` `## Mistakes`).

Assimilation: none this round (claims frozen before assimilation could be scoped; the staged `merge/tsukuroi` package keeps its 53 id collisions S200-S252 with the lane registry — `.ufo/waves/round-48/assimilation/collisions`; nothing is appended from it). `considerthese/`: one proposal mined by a wave scout, landed only if the lane's own bar grounds it.

## Round 48 — measured outcome (attempt 2; author-side, non-author closure pending)

Freeze `ae99f021b76f8eb1c8805d32d80644464afb1ff6`; counted wave `w2`, validated v2, 71 seats (reviewer 16, critic 14, executor 15, scout 15, mutation-tester 4, sentinel 2, connector 2, scribe 3; attack roles 34/71 = 47.9%; no deaths reported). L1 held the planner seat. Attempt-1 `w1` was invalid, stopped by the orchestrator, and void; see `.ufo/waves/round-48/w1/INCIDENT.md`. No residual call.

| Claim | Frozen before → measured after | Verdict | Axis effect |
|---|---|---|---|
| C1 operability | `score-selftest-tmpdir-r48.py --revision ae99f021…` → `pass_ok=4, loc_ok=4, clean_ok=4, failfast_ok=2, term_ok=1, static_ok=1`, `PASS`; receipt `.ufo/waves/round-48/after/c1-final.json`; census blob sha256 `375aa737…e2426` | **PASS** | operability unchanged ordinal (9, saturation); capability already existed, behavior hardened; no axis harmed observed. |
| C2 depth | `check-scrub-admission-r48.py --revision 76066487…` → `structural_ok=1, quotes_ok=3, verdicts_ok=1, marks_ok=0`, `FAIL`; `.ufo/waves/round-48/after/c2-final.json`. GR1 and GR2 have current-hash `partly` reports; GR3 holds. No round-48 marks added. | **FAIL** | depth unchanged (8); no admission / no axis move. |
| C3 calibration | `check-self-assessment.py --revision 71493caa…` → checked 27, mismatches 0, PASS (`after/c3-final.json`, measured at `71493caa5cf5dce1c109b69ba526989d17723a7d`); pre-restatement 3 | **PASS** | calibration remains ordinal 9; mismatch count reaches zero. |

No ordinal score changes. C2's misses are not narrowed: counted findings remain in `.ufo/waves/round-48/w2/R48CritGR1a.md`, `R48RevGR2a.md` and `R48CritGR2a.md`; no entry, SKILL, or README admission mark was written. S240 was opened live by the L1 and is the source for the GR2/ioctl clause. C1's source phrase in the frozen declaration is more specific than the landed registry changes: existing S251 was re-opened (not a new id), S253 and S255 were newly admitted, S254 rejected; all are recorded in `corpus/SOURCES.md` and the round lesson.

Trend verdicts: expansion **unchanged** (no new knowledge entry admitted); quality **improved** (C1's TMPDIR behavior and checks passed; C2 remains unadmitted); discernment **improved** (the frozen C2 counter refuses the partly rows and the calibration table mismatch count is 0). Non-author spot-check remains pending.

## Round 49 — declaration (2026-10-28, base `6256760d1382ce4ce20fcba830d4b2912cfbf12b`, before any seat)

Ordinals at base: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8 (depth and adjacency
tied lowest). Saturation 9 / window 3. Round 48 closed C1 operability PASS, C2 depth FAIL (GR1/GR2 `partly`), C3
calibration PASS. Round-start receipt: sources census exit 0 (`.ufo/waves/round-49/before/sources-census-start.txt`).
Frozen record (predicates, cohort, hashes, controls): `.ufo/waves/round-49/frozen/FROZEN.md`.
Round shape: ONE v2 wave (`w1`) sized 64–128; the L1 holds the planner seat.

| Claim | Axis | Surface moved | Counter (frozen) | Before at base | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | depth (lowest tied) | `corpus/knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3: the seven corrections the round-48 counted seats named land before the freeze (GR1 `0X` prefix + host-reading inference mark; GR2 `is_valid` gate, cancel-sentence subject, suspend-path range/effects, `ioctl.c:3132`, `-ENODEV` devid), then a fresh 18-seat cohort of one wave re-reads the corrected rows `holds` | `python3 tools/check-scrub-admission-r49.py --revision <REV>` | `corr_ok 0, verdicts_ok 0, seats_ok 0, marks_ok 0` → FAIL | `structural_ok == 1 and corr_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3`; row hashes GR1 `3a2ba180…`, GR2 `d4296085…`, GR3 `43430a14…` | any bound-format negative on the current row hash blocks the row; a citation that does not resolve earns no credit; two byte-identical bodies fail the row |
| C2 | adjacency (lowest tied) | `PROVINCE.md` ADJ-01..07 **Ownership source**: bare sibling `*.md:N-M` ranges (9 occurrences) replaced by `OUT-002`…`OUT-010`, each anchor's ADJ class / pinned commit / heading / ≤25-word quote and the registry blob sha256 checked | `python3 tools/check-adjacency-table-r49.py --revision <REV>` | `bare_ranges 9, linked_rows 0` → FAIL | `adj_rows == 7 and linked_rows == 7 and bare_ranges == 0 and anchors_ok == 7 and registry_ok == 7 and anchors_checker_rc == 0` | a row kept on a bare range, an OUT id not naming that ADJ class, or a registry digest that does not match fails the counter |
| C3 | operability (sourced: S255 re-opened 2026-10-28) | `tools/tsukuroi-census.sh`: stale `builds a /tmp fixture tree` comment removed; the alias resolver records `ST_BASE_ERR` and `run_selftest` prints the named `fd band … exhausted` diagnostic; one new `(R49-C3)` selftest case proves the exhausted-band path under a two-descriptor band | `python3 tools/check-fd-band-r49.py --revision <REV>` | `stale_ok 0, diag_ok 0, band_ok 0, cases 166` → FAIL | `stale_ok == 1 and diag_ok == 1 and band_ok == 1 and cases == 167` | a run that prints 166 cases, a kept stale comment, or a missing diagnostic fails; the diagnostic case must fail under a band-free mutant |

Pre-data controls (frozen counters, receipts `.ufo/waves/round-49/controls/battery-summary-r49-c{1,2,3}.jsonl`):
C1 K0/K1/K2/K3/K4/K5/K6 must FAIL and K-pass PASS; C2 K0/K1/K2/K3 FAIL, K-pass PASS; C3 K0/K1/K2 FAIL, K-pass PASS.
Causal separability: C1 reads only the entry + cohort + marks; C2 only `PROVINCE.md` + the anchor registry; C3 only
the census blob. No claim's counter reads another's bytes.

## Axes — current self-assessment (round 49 final measured surface)

Re-stated 2026-10-28 at the round-49 final tree; ordinals unchanged. No axis is claimed as moved: C1 did not admit
(the counted cohort bound one `partly` on GR2), C2 and C3 landed and are measured in the Round 49 outcome below.
Counts re-derived with the commands in each cell.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 67 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); `SKILL.md` 4572 `wc -l` / 1323 table lines (`grep -c '^\|' SKILL.md`); `corpus/lessons/` 73 files (`find corpus/lessons -type f \| wc -l`); GR1-GR3 still pending: the round-49 cohort read GR1 holds 6/6, GR3 holds 6/6, GR2 holds 5/6 with one bound `partly` (`CritGR2b`) on the [inference] mark's ioctl conjunct. | round 4; unchanged |
| coverage | 9 | `corpus/README.md` 500 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus verdict-neutral STORAGE; no coverage claim this round. | round 11 (terminal closeout); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (167 cases, 167 passed, 0 failed) at round 49 (`.ufo/waves/round-49/after/c3-final.json`); `--identity` landed; `bash tools/boot-chain-audit.sh --selftest` `PASS total=49 failed=0`. | round 11 (terminal closeout); unchanged |
| freshness | 9 | S246, S247, S248, S243, S240, S249 and S251 re-opened live by round-49 seats 2026-10-28 (byte-identical pins); S255 re-opened by the L1 byte-identically; end census exit 0 (`.ufo/waves/round-49/after/sources-census-end.txt`). | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <round-49 final measured revision>` → checked 27, mismatches 0 after the restatement below; before the restatement 2 (K13 lesson-file count 72 = 72, K17 census case count 166 → 167 in the capabilities row). | round 10; unchanged |
| adjacency | 8 | formal overlap table present (PROVINCE `| ID | Finding`); ADJ-01..07 ownership cells cite `OUT-002`…`OUT-010` and no bare sibling range (`python3 tools/check-adjacency-table-r49.py --revision <REV>`); `check-adjacency-anchors.py` PASS at the same revision after two IN-109 found_line repins this round (2642→2660→2671). | fleet round 1; unchanged |

## Capabilities — current full evidence set (round 49)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates opened tier-scoped sources with anchors, rejections, paths, search log and unopened leads | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT, STORAGE and SCRUB lines; the selftest prints PASS (167 cases, 167 passed, 0 failed) at round 49 and its alias resolver names descriptor-band exhaustion (`fd band … exhausted`) and a malformed band (`err=fd-band-invalid`) instead of failing silently | `tools/tsukuroi-census.sh`; `.ufo/waves/round-49/after/c3-final.json`; `.ufo/waves/round-49/before/c3-at-base.json` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations while preserving fixture isolation and policy boundaries | `.ufo/waves/round-12/resumed/after.json`; `.ufo/waves/round-12/resumed/selftest-after.json`; `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | round 12 |
| boot-chain-audit | Reads and types initramfs root paths against the selected firmware entry, producing a per-entry next-boot verdict; since round 43 its boot-input freshness check decides on find's output | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt`; `.ufo/waves/round-43/after/c1-after-c395491.jsonl` | round 17 |
| storage-error-counter-reader | Reads every btrfs device's five error counters from sysfs and prints one verdict-neutral STORAGE line, demonstrated on fixtures, the live host and namespace views | `tools/tsukuroi-census.sh`; `.ufo/waves/round-38/after/c1-final-b0005ae.json`; `.ufo/waves/round-41/after/c1-after-568c397.jsonl` | round 38 |

- **planned (next round):** depth — apply the one remaining GR2 defect the round-49 cohort named (the `[inference]`
  mark still claims the ioctl side is unpinned although `ioctl.c` is pinned at S240; exact replacement is in
  `.ufo/waves/round-49/w1/R49CritGR2b.md` defect 1) and add `S240` to the entry's `source:` line and QUALITY item 7
  (defect 2), then re-read GR2 with a NEW cohort; operability — harden `check-fd-band-r49.py` (a spaced-TMPDIR PASS
  leg, a diagnostic-not-in-comment leg) and `check-scrub-admission-r49.py` (a `--dispatch-file` override; a
  distinct-bodies rule that ignores whitespace padding); adjacency — re-pin or hand over the anchors the round-49
  drift seat (`R49CritAdjB`) reports as stale at the current sibling tips, and keep the IN-109 repin inside the same
  commit as the census edit (this round needed two).
- **retired:** none.
