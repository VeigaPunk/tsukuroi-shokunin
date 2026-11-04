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
| cited-receipt-landing-gate | Verifies at any revision that every `.ufo/waves/round-<N>/...` FILE path the round's own committed artifacts cite (wave receipts + round lesson + round knowledge note) exists as a blob in that same revision's tree — the unlanded-receipt class's cited-and-unlanded half caught mechanically before closure (the r59 count rule made executable); sibling-repo citations, directory prefixes, bare directory mentions and prose ellipses are documented non-citations; a receipt retained in scratch and never path-cited (the r59 occurrence) is the gate's named limit | `python tools/check-cited-receipts-r62.py --selftest` → JSON PASS 4 cases rc 0 (`.ufo/waves/round-62/after/cited-receipts-selftest-at-work.json`); demonstrations from the committed tool (`.ufo/waves/round-62/after/cited-receipts-*.json`): r61@`52d9ba1a` FAIL 3 (the class caught), r58@`c2e32b00` FAIL 1, r59@`35c2748f` PASS 0 (the named limit), r61/r62@work PASS 0 and r61/r62@final PASS 0; measured commit `f3f648123c907dd09b53caa1ac009a67598506ee` | round 62 |
| line-endings-guard | Detects and localizes CR bytes in the lane's guarded tracked text files (the host-transition CRLF class that E12-floods the canonical census), with a 7-case hermetic selftest covering the exit-code contract and the guarded-set membership predicates, and mutant-killing coverage proven against a 5-mutant battery | `python3 tools/check-line-endings-r64.py --selftest` → `CHECK_LINE_ENDINGS_SELFTEST: PASS (7 cases, 7 passed, 0 failed)` rc 0; `--check` → `CHECK_LINE_ENDINGS: PASS (330 file(s) checked, 0 violation(s))` rc 0 (`.ufo/waves/round-64/after/{c1-guard-selftest,c1-guard-check,c1-selftest-coverage-fix}.txt`); battery `.ufo/waves/round-64/after/mutation/mutation-report.txt` | round 64 |

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
| win-host-census | Reads the Windows host's tool presence, PATH health, interpreter identity (real `python` vs the Store `python3` alias stub) and git/gh state as four verdict planes with a hermetic 20-case selftest | `python tools/win-host-census-r53.py --selftest` rc 0 (`.ufo/waves/round-53/after/win-census-selftest.txt`); live `.ufo/waves/round-53/after/win-census-live.txt` | 53 |
| receipt-run | Runs any host-state measurement under a wall-clock budget and writes its raw receipt (argv, start/end UTC, duration, rc or `rc=timeout` + `timeout_after_s`, verbatim CRLF-preserving stdout/stderr) directly into a lane-tree path — the scratch-deleted-receipt defect class (closure `5cbcb06e` defect 3) is closed by instrument, not procedure | `python tools/receipt-run.py --selftest` rc 0, 7 cases (`.ufo/waves/round-54/after/receipt-run-selftest.txt`); first working use = the D7 re-derivations `.ufo/waves/round-54/d7-receipts/` (90 s + 420 s raw receipts, both `rc=timeout`) | 54 |
| drift-recheck-loop | Re-verifies all 12 drift-register rows against their recorded observations with one read-only command (10 host probes + 2 doc rows), rc 0 iff no drift; a drift line is honest output owed an appended correction | `bash tools/recheck-drift-r54.sh --receipt <path>` rc 0, `RECHECK_DRIFT: PASS (12 rows, 10 host-probed match, 2 doc rows, 0 drift)` (`.ufo/waves/round-54/after/recheck-drift-r54.txt`) | 54 |

- **planned (next round):** depth — apply the one remaining GR2 defect the round-49 cohort named (the `[inference]`
  mark still claims the ioctl side is unpinned although `ioctl.c` is pinned at S240; exact replacement is in
  `.ufo/waves/round-49/w1/R49CritGR2b.md` defect 1) and add `S240` to the entry's `source:` line and QUALITY item 7
  (defect 2), then re-read GR2 with a NEW cohort; operability — harden `check-fd-band-r49.py` (a spaced-TMPDIR PASS
  leg, a diagnostic-not-in-comment leg) and `check-scrub-admission-r49.py` (a `--dispatch-file` override; a
  distinct-bodies rule that ignores whitespace padding); adjacency — re-pin or hand over the anchors the round-49
  drift seat (`R49CritAdjB`) reports as stale at the current sibling tips, and keep the IN-109 repin inside the same
  commit as the census edit (this round needed two).
- **retired:** none.

## Round 49 — measured outcome (author-side; non-author closure pending)

Freeze `55c07cd3`; wave `w1` validated at `32a85560` (73 seats, policy v2, 37 attack seats = 50.7%); integrated at
`823425c5`; receipts in `.ufo/waves/round-49/after/`; frozen record `.ufo/waves/round-49/frozen/FROZEN.md`;
pre-data batteries `.ufo/waves/round-49/controls/battery-summary-r49-c{1,2,3}.jsonl` (all declared controls failed,
every K-pass passed). Wave accounting: 73 dispatched, 73 results entries, 73 reports, 0 dead seats, no residual
call. L1 held the planner seat.

| Claim | Frozen predicate → measured | Verdict | Axis effect |
|---|---|---|---|
| C1 depth | `python3 tools/check-scrub-admission-r49.py --revision 823425c5` → `structural_ok 1, corr_ok 1, quotes_ok 3, verdicts_ok 0, seats_ok 18, marks_ok 0` → FAIL (`.ufo/waves/round-49/after/c1-final.json`). Two independent causes, both reported: (a) `R49CritGR2b` bound `partly` on the GR2 `[inference]` mark (it still claims the ioctl side is unpinned although `ioctl.c` is pinned at S240 and the row cites it), which blocks GR2; (b) the frozen counter's citation leg rejects any `path.ext:NNN` that is not a pinned snapshot file, so 17 of the 18 reports are unbound for credit (they cite `entry.md`, `FETCH.txt`, the counter, and other notes) even though their file-format verdicts are 17 `holds` / 1 `partly`. No admission mark was written. | **FAIL** | depth unchanged (8); the seven round-48-named corrections are in the bytes (`corr_ok 1`) and GR1/GR3 now read `holds` 6/6 each. |
| C2 adjacency | `python3 tools/check-adjacency-table-r49.py --revision 823425c5` → `adj_rows 7, linked_rows 7, bare_ranges 0, anchors_ok 7, registry_ok 7, anchors_checker_rc 0` → PASS (`.ufo/waves/round-49/after/c2-final.json`); before at base `bare_ranges 9, linked_rows 0` (`.ufo/waves/round-49/before/c2-at-base.json`). | **PASS** | adjacency unchanged (8); the ADJ ownership table now cites portable anchors. Named limit: the counter is a shape test — `R49CritAdjA` and `R49RevAdjB` show a stub table passes it; the content leg is the existing `check-adjacency-anchors.py` (which caught the freeze-revision IN-109 drift). |
| C3 operability | `python3 tools/check-fd-band-r49.py --revision 823425c5` → `stale_ok 1, diag_ok 1, band_ok 1, cases 167` → PASS (`.ufo/waves/round-49/after/c3-final.json`); before at base `stale_ok 0, diag_ok 0, band_ok 0, cases 166` (`.ufo/waves/round-49/before/c3-at-base.json`). | **PASS** | operability unchanged (9, saturation); no new capability row. A HIGH regression the round introduced (`R49RevFdA` D1: a dirty TMPDIR made `--selftest` FAIL) was reproduced, fixed in `0732903`, and re-verified with the predecessor counter `score-selftest-tmpdir-r48.py --cases 167` → `pass_ok 4, loc_ok 4, clean_ok 4, failfast_ok 2, term_ok 1, static_ok 1`, PASS (`.ufo/waves/round-49/after/r48-tmpdir-counter-at-e1.json`). |

Calibration: `python3 tools/check-self-assessment.py` → `checked 27, mismatches 0, PASS` at the round's final revision
(`.ufo/waves/round-49/after/calibration-final.json`); before the restatement 4 (K08 SKILL line count, K11 README line
count, K14 `--identity` phrasing, K15 overlap-table phrasing — all four created by this round's own appends, and the
freeze-time count was 2, K13/K17: the declaration's "3" was wrong, corrected by name in `corpus/lessons/round-49.md`).

Sources: S255 `used-by` appended (`corpus/lessons/round-48.md` → `…, corpus/lessons/round-49.md`); no row added this
round, no duplicate id, census exit 0 at start and end. `proc_pid_fd(5)` was opened and refused as the traversal
source: it documents the symlink and `type:[inode]` text but not a child path component after `/proc/self/fd/<n>`.

Trend verdicts: expansion **unchanged** (no new knowledge entry admitted, no new source row); quality **improved**
(C2 and C3 measured PASS, C3's own regression found and closed by an independent predecessor counter, and the GR rows
re-read clean by a 18-seat cohort where round 48 could not); discernment **improved** (the cohort caught a real
overreach the author had just written, the frozen counter was shown to be forgeable by three seats, and calibration
restates to zero mismatches).

## Round 50 — declaration (2026-10-28, base `b866a1d3d26616119a089f1a69b080136becc17b`, before any seat)

Ordinals at base: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8 (depth and adjacency
tied lowest, so the lowest-axis duty binds). Saturation 9 / window 3 (no waiver). Round 49 closed
`rejected-honest-stop` (C2 adjacency PASS, C3 operability PASS, C1 depth FAIL on a bound `partly`). Round-start
receipts (`.ufo/waves/round-50/before/`): sources census exit 0 at this attempt's own start (255 rows, 40 W04);
C2 at base `idiom_sites 7, base_misses 20/20, full_misses 0, cases 167, case_ok 0` (`.ufo/waves/round-50/before/c2-at-base.json`).
Frozen record (predicates, row hashes, cohort, controls): `.ufo/waves/round-50/frozen/FROZEN.md`.
Round shape: ONE v2 wave (`w1`) sized 64–128; the L1 holds the planner seat.

| Claim | Axis | Surface moved | Counter (frozen) | Before at base | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | depth (lowest tied) | `corpus/knowledge/btrfs-scrub-grounding-r45.md`: the four corrections `R49CritGR2b` named land before the freeze (the `[inference]` mark narrowed to btrfs-progs printing; S240 in the `source:` line and QUALITY item 7; the `dev-replace.c:1128` quote exact; the S247/S240 range gaps declared in Limits); the counter's citation leg binds real reports (lane artifacts + >=2 distinct row sources) and its distinct-bodies leg ignores whitespace padding; a fresh 18-seat cohort of one wave re-reads GR1-GR3 | `python3 tools/check-scrub-admission-r50.py --revision <REV>` | `corr_ok 0, verdicts_ok 0, seats_ok 0, marks_ok 0` → FAIL | `structural_ok == 1 and corr_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3`; row hashes GR1 `3a2ba180…`, GR2 `a2e955ce…`, GR3 `43430a14…` | any bound-format negative on the current row hash blocks the row; a cohort on defective bytes fails `corr_ok` |
| C2 | operability (sourced: S256 opened this round) | `tools/tsukuroi-census.sh` selftest harness: `printf '%s\n' "$out" \| grep -q` / `\| head -n1` under `set -euo pipefail` replaced by a full-read matcher (`buf_has`/`out_has`), and one `(R50-C2)` case pins 20 trials on a 200 KB buffer (167 → 168 cases) | `python3 tools/check-selftest-matcher-r50.py --revision <REV> --scratch <DIR>` | `idiom_sites 7, cases 167, case_ok 0` → FAIL | `idiom_sites == 0 and base_misses > 0 and full_misses == 0 and cases == 168 and pass_runs == 2 and case_ok == 1` | a census that keeps the pipe idiom scores `idiom_sites > 0`; a run printing 167 cases fails; the probe must show the base idiom can false-miss |
| C3 | adjacency (lowest tied) | `tools/check-adjacency-table-r50.py`: content legs (registry digest + heading + quote against the pinned sibling blob; the quote again at the sibling's live tip) and a `stub_fails` leg that separates a shape-valid stub from the real table (routed V5) | `python3 tools/check-adjacency-table-r50.py --revision <REV>` | `quote_at_pin_ok 0, live_quote_ok 0, stub_fails 0` (legs absent at r49) → FAIL | `adj_rows == 7 and linked_rows == 7 and bare_ranges == 0 and anchors_ok == 7 and registry_ok == 7 and anchors_checker_rc == 0 and quote_at_pin_ok == 9 and live_quote_ok >= 8 and stub_fails == 1` | a wrong-class row, a mutated digest or a drifted quote fails its leg; a counter that cannot fail a stub scores 0 |

Pre-data controls (frozen counters; receipts `.ufo/waves/round-50/controls/battery-summary-r50-c{1,2,3}.jsonl`):
C1 K0/K1/K2/K3/K4/K5/K6/K7 must FAIL and K-pass PASS; C2 K0/K1/K2 FAIL, K-pass PASS; C3 K1/K2/K3 FAIL, K-pass PASS.
Causal separability: C1 reads the entry + cohort + marks; C2 reads the census blob; C3 reads `PROVINCE.md` + the
anchor registry + the sibling repos. No claim's counter reads another's surface.

Assimilation: none this round — the staged `merge/tsukuroi` package still collides with the lane registry
(`.ufo/waves/round-50/assimilation/collisions`); nothing is appended from it. `considerthese/`: one proposal mined
by a wave scout, landed only if the lane's own bar grounds it.

## Round 50 — measured outcome (author-side; non-author closure pending)

Freeze amendment `8029cdba1049df25632c91a23c8db4eefb54be5f`; wave spec/dispatch commit
`39e694934cf6c56434987edc730e8b3580a251f3`; one v2 wave `w1`, 71 seats, 71 results entries, 64 report files,
0 dead seats, no residual call. Seven settled seats have a final output in `w1-results.json` but no
`<seat>.md` report file: `R50MutCounterC`, `R50ScoutLiveTip`, `R50RevCounterC3`, `R50ExecPriorCounters`,
`R50Simplifier`, `R50CritGR2Host`, `R50RevScopeSiblings`. No seat replacement was made.

| Claim | Frozen predicate → measured | Verdict | Axis effect |
|---|---|---|---|
| C1 depth | `python3 tools/check-scrub-admission-r50.py --revision 8029cdba --wave-dir .ufo/waves/round-50/w1 --results-file .ufo/waves/round-50/w1-results.json --dispatch-file .ufo/waves/round-50/w1-dispatch.json` → `structural_ok 1, corr_ok 1, quotes_ok 3, verdicts_ok 0, seats_ok 18, marks_ok 0`, FAIL (`.ufo/waves/round-50/after/c1-final.json`) | **FAIL** — all three rows blocked by bound-format `partly`: GR1 one (cmdline.c:147 quote omits `* `); GR2 four (`R50RevGR2c`, `R50CritGR2a/b/c`, misattributed `by SR7`, overbroad ioctl inference, incomplete S242 range list, progress-query context wording); GR3 six (S237 list omits `scrub.c:439` and `:1546`). No admission mark written. | depth unchanged (8); no row admitted; no axis score moves |
| C2 operability | `python3 tools/check-selftest-matcher-r50.py --revision 8029cdba --scratch <DIR>` → `idiom_sites 0, base_misses 19/20, full_misses 0, cases 168, pass_runs 2, case_ok 1`, PASS; both runs `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` (`after/c2-final.json`) | **PASS measured, with instrument limits** — the live frozen census executes the new case and both full selftests pass; `R50CritCheatC2` and `R50RevCounterC2` show a 5-/12-line liar census can satisfy the counter, and an equivalent `${out}` pipe idiom can evade its lexical detector. | operability ordinal remains 9; no new capability row |
| C3 adjacency | `python3 tools/check-adjacency-table-r50.py --revision 8029cdba` → `adj_rows 7, linked_rows 7, bare_ranges 0, anchors_ok 7, registry_ok 7, anchors_checker_rc 0, quote_at_pin_ok 9, live_quote_ok 9, stub_fails 1`, PASS (`after/c3-final.json`) | **PASS measured, with instrument limits** — the default lane table's nine cited anchors match their pinned sibling digests/quotes and live-tip quotes; `R50CritCheatC3` shows a caller-supplied adapted stub and a false displayed OUT-009 pin can still pass. | adjacency ordinal remains 8; no new surface claimed |

No ordinal score changes. No claim is admitted as a round-level improvement because C1's frozen predicate fails.
C1's four round-49 corrections are real, but the new counted cohort found remaining defects and one new overreach
in the narrowed ioctl mark. No depth admission marks were written. C2/C3 predicates PASS on their measured bytes,
but their counter-cheat limits are disclosed rather than smoothed.

## Axes — current self-assessment (round 50 final measured surface)

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 67 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); `SKILL.md` 4594 `wc -l` / 1326 table lines (`grep -c '^\|' SKILL.md`); `corpus/lessons/` 75 files (`find corpus/lessons -type f \| wc -l`); GR1-GR3 remain pending under C1 (`verdicts_ok 0`); no ordinal move. | round 4; unchanged |
| coverage | 9 | `corpus/README.md` 522 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; no surface promotion. | round 11; unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` → PASS (168 cases, 168 passed, 0 failed); `--identity` landed; `bash tools/boot-chain-audit.sh --selftest` `PASS total=49 failed=0`; `check-fd-band-r49.py` accepts later case additions while retaining R49-C3. | round 11; unchanged |
| freshness | 9 | S240 re-opened byte-identically at sha256 `7b3488f2…ba01`; S256 opened 2026-10-28; sources census exit 0 at start and end. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision 9c5d6b436e599c7809ffe458e973cd14d410bb51` → checked 27, mismatches 0; no ordinal move. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (PROVINCE `| ID | Finding`); C3 measured 9/9 pinned quotes/digests and 9/9 live-tip quotes; caller-supplied C3 overrides can still score fabricated input (`R50CritCheatC3.md`). | fleet round 1; unchanged |

## Capabilities — current full evidence set (round 50)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates opened tier-scoped sources with anchors, rejections, paths, search log and unopened leads | `corpus/SOURCES.md`; `.ufo/evidence/round-1-kaika/after.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT, STORAGE and SCRUB lines; selftest prints PASS (168 cases, 168 passed, 0 failed); its full-read selftest matcher is covered by `(R50-C2)` | `tools/tsukuroi-census.sh`; `.ufo/waves/round-50/after/c2-final.json` | lane r2; demonstrated fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations while preserving fixture isolation and policy boundaries | `.ufo/waves/round-12/resumed/after.json`; `.ufo/waves/round-12/resumed/selftest-after.json`; `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | round 12 |
| boot-chain-audit | Reads and types initramfs root paths against the selected firmware entry, producing a per-entry next-boot verdict; since round 43 its boot-input freshness check decides on find's output | `tools/boot-chain-audit.sh`; `.ufo/waves/round-17/l1-capture/audit-live.txt`; `.ufo/waves/round-43/after/c1-after-c395491.jsonl` | round 17 |
| storage-error-counter-reader | Reads every btrfs device's five error counters from sysfs and prints one verdict-neutral STORAGE line, demonstrated on fixtures, the live host and namespace views | `tools/tsukuroi-census.sh`; `.ufo/waves/round-38/after/c1-final-b0005ae.json`; `.ufo/waves/round-41/after/c1-after-568c397.jsonl` | round 38 |

- **planned (next round):** depth — correct GR1's missing `* ` prefix; complete S242/S237 range-gap disclosures; remove the `by SR7` misattribution and narrow the ioctl inference to the call path and copy-back; correct the progress-query context wording; then re-read all affected rows with a new counted cohort. Operability — harden C1/C2/C3 counters against fabricated results, liar census output, equivalent pipe spellings and override-fed fake sibling roots; retain C2's end-to-end matcher case. Adjacency — bind each displayed OUT row's sibling path/commit/quote to its registry record and require source-specific meaningful quotes, not any substring. Keep the round-50 source-range/exact-line mistake as QUALITY 94.
- **retired:** none.

### Sources & frontier status

Registry: 255 → 256 rows; one tier-A documentation row S256 added; S240 `used-by` appended from
`corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/lessons/round-48.md`
to those three plus `corpus/knowledge/btrfs-scrub-grounding-r45.md`; no status/recheck cell changed.
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
exit 0 at start and end (40 W04 warnings; 256 rows at end). No Frontier row advanced. Assimilation: none; 57 id
collisions; `considerthese/2026-10-26.md` counter-attack scoreboard proposal was mined but not implemented.

### Trend verdicts

- expansion: **unchanged** — no new knowledge entry admitted and no province Frontier row moved; the SOURCES row
  is curation, not an expansion claim.
- quality: **harmed** — the round's correction narrowed the GR2 `[inference]` mark but still overstates the
   ioctl path before the `btrfs_scrub_dev` call (`R50CritGR2a/b`); GR1-GR3 remain pending and no admission
   mark was written. The defect is named in the round-50 gate status and lesson, but the erroneous clause remains
   in the frozen row for next-round correction.
- discernment: **unprovable-but-better** — the counted cohort exposed provenance/quote defects and the C2/C3
  attackers falsified counter assumptions, and QUALITY 94 records the lesson; these are lane-dispatched seats,
  not the required independent non-author sample. External closure remains pending.

## Round 51 — declaration (2026-10-28, base `c0ad548a93425a3bf8813d28d92f26fe2f64b9d4`, before any seat)

Ordinals at base: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8 (depth and adjacency
tied lowest, so the lowest-axis duty binds). Saturation 9 / window 3 (no waiver). Rounds 47-50 each closed
`rejected-honest-stop` on C1 depth; round 50's closure routed the defects below. Round-start receipts
(`.ufo/waves/round-51/before/`): sources census exit 0 (256 rows, 40 W04); `check-self-assessment.py` at base
`checked 27, mismatches 1` (K10: the lesson-file count, 75 stated vs 76 files — the closure's own spot-check file);
`check-registry-coverage.py` at base `missing 6`. Frozen record: `.ufo/waves/round-51/frozen/FROZEN.md`.
Round shape: TWO v1 waves (`w1` build + uncounted pre-read + attacks; `w2` counted cohort + falsify), 64-128 seats
total; the L1 holds the planner seat.

| Claim | Axis | Surface moved | Counter (frozen) | Do-nothing control at base | Target (predicate) |
|---|---|---|---|---|---|
| C1 | depth (lowest tied; sourced S237 S240 S242 S243 S246 S247 S248) | `btrfs-scrub-grounding-r45.md` GR1-GR3: GR2 rewritten, GR1 quote leader, `### Range gaps (R51)` block; counted w2 18-seat cohort | `python3 tools/check-scrub-admission-r51.py --revision <REV> --wave-dir .ufo/waves/round-51/w2 --results-file .ufo/waves/round-51/w2-results.json --dispatch-file .ufo/waves/round-51/w2-dispatch.json` | `lint_ok 0, quotes_ok 2, verdicts_ok 0, seats_ok 0, marks_ok 0` | `structural_ok == 1 and lint_ok == 3 and quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3` |
| C2 | operability (census-gate instrument; sourced S256) | matcher counter hardened against a liar census, respelled pipes and a neutered harness | `python3 tools/score-counter-cheats-r51.py --revision <REV> --scratch <DIR>` | round-50 counter rejects 0 of 4 cheats | `real_pass == 1 and cheats == 4 and cheats_rejected == 4 and r50_cheats_rejected == 0` |
| C3 | adjacency (lowest tied) | displayed anchors and digest list bound to the registry; override cannot print PASS | `python3 tools/check-adjacency-table-r51.py --revision <REV>` | round-50 counter passes a false displayed OUT-009 commit (`r50_blind 1`) | the r50 legs plus `display_bound_ok == 10 and quote_specific_ok == 10 and digests_bound_ok == 10 and display_forge_fails == 1 and override_blocked == 1 and r50_blind == 1` |

Pre-data controls (frozen counters; receipts `.ufo/waves/round-51/controls/battery-summary-r51-*-c{1,2,3}.jsonl`):
C1 K0-K8 must FAIL and K-pass PASS; C2 K0 FAIL and K-pass PASS; C3 K0-K5 must not PASS (CONTROL-FAIL or
OVERRIDE-NOT-MEASURED) and K-pass PASS.
Causal separability: C1 reads the entry + snapshots + cohort; C2 reads the census blob; C3 reads `PROVINCE.md`, the
registry and sibling repos. C2 and C3 are instrument claims; the census, `PROVINCE.md` and the registry are not changed.

## Round 52 — declaration (2026-10-30, base `cc88b81d78bcbe06bce3f6bf722a108432ad276f`, before any seat)

Ordinals at base: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8 (depth and adjacency
tied lowest, so the lowest-axis duty binds). Saturation 9 / window 3 (no waiver). Rounds 49-51 each closed
`rejected-honest-stop` on the C1 depth claim; round 51's closure routed the resume point (dispatch the counted
cohort, produce a valid C2 receipt in an undisturbed scratch, measure all three claims at one named revision) and
four defects (r51 leftovers, the missing r51 lesson/LOG entry, the stale axes restatement, SHONEN re-filing) — all
four are landed in this round's freeze commit. Round-start receipts (`.ufo/waves/round-52/before/`): sources census
exit 0 at start; C1 at base `lint_ok 3, quotes_ok 3, verdicts_ok 0, seats_ok 0, marks_ok 0` FAIL (`c1-at-base.json`);
C3 at base full-legs PASS with `r50_blind 1` (`c3-at-base-r52.json`); `check-self-assessment.py` at base
`checked 27, mismatches 3` (K08 SKILL lines 4594 vs 4605, K09 table lines 1326 vs 1337 — the r51 registry rows — and
K10 lessons 75 vs 77; restated below, before the wave); `check-registry-coverage.py` at base PASS 88/88.
Frozen record: `.ufo/waves/round-52/frozen/FROZEN.md`. The counted row bytes are the
round-51 AMENDMENT-1 bytes, unchanged since `6abef5d0` (`git diff 6abef5d0 cc88b81d -- corpus/knowledge/btrfs-scrub-grounding-r45.md`
is empty); section hashes at the freeze: GR1 `98fa4e07…63987`, GR2 `9fd581a0…4f0ec5`, GR3 `0405f38a…b9eac`
(`python3 tools/check-scrub-admission-r52.py --revision <FREEZE> --section-hash`).

Round shape: ONE v2 wave `w1` (band 64-128) of **64 seats** — the counted 18-seat cohort plus build, attack,
frontier and verification items; ≥25% attack roles (reviewer/critic/mutation-tester); the L1 holds the planner seat.
The wave dispatches only after this freeze commit; nothing scores before it.

| Claim | Axis | Surface moved | Counter (frozen) | Do-nothing control at base | Target (predicate) |
|---|---|---|---|---|---|
| C1 | depth (lowest tied; sourced S237 S240 S242 S243 S246 S247 S248; row bytes = the r51 amendment) | rows GR1-GR3 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` read `holds` by a fresh counted 18-seat cohort in `w1`; the three round-52 admission marks land only on three clean counted rows | `python3 tools/check-scrub-admission-r52.py --revision <REV>` (defaults read `.ufo/waves/round-52/w1-results.json` and `-dispatch.json` at REV; seat universe `R52RevGR<n>{a,b,c}`/`R52CritGR<n>{a,b,c}`) | base bytes, no cohort: `verdicts_ok 0, seats_ok 0, marks_ok 0` FAIL (`before/c1-at-base.json`) | `structural_ok == 1 and lint_ok == 3 and quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3` |
| C2 | operability (instrument-measurement completion; sourced S256 and, this round, S257) | a VALID receipt of the round-51 5-cheat scorer (`tools/score-counter-cheats-r51.py`), in an undisturbed scratch, at the integrated revision — the round-51 amend1 attempt is committed broken (ERROR rows; spot-check defect e; bytes at `.ufo/waves/round-52/inherited/`) | `python3 tools/score-counter-cheats-r51.py --revision <REV> --scratch <DIR>` | skip the run: no valid receipt exists (the only committed one is broken; the r51 spot-check graded C2 `unprovable`) | `real_pass == 1 and cheats == 5 and cheats_rejected == 5 and r50_cheats_rejected == 0`; kill: any ERROR row, any unrejected cheat, or a scratch disturbed between run and receipt |
| C3 | adjacency (lowest tied; instrument-measurement completion) | the round-51 counter measured at ONE named integrated revision with its full leg set — r51 closed with no named-revision measurement (only battery K-pass rows) | `python3 tools/check-adjacency-table-r51.py --revision <REV>` | at base the counter already PASSES all legs (`before/c3-at-base-r52.json`) — the unreachable part is the receipt at the integrated revision with the battery re-run green; skip the round and no such receipt exists | the full r51 predicate (`adj_rows == 7 … and recipient_ok == 7`) PASS at the named revision; kill: any leg failing at that revision |

Pre-data controls: the C1 battery re-derived for the round-52 counter (`.ufo/waves/round-52/controls/battery.py`,
26 controls, run at the freeze after the commit, before dispatch); the C2 and C3 batteries are the round-51 ones
re-run at the freeze (their instruments are reused, not refrozen). Causal separability unchanged: C1 reads the
entry + snapshots + cohort + marks; C2 reads the census blob and its scratch; C3 reads `PROVINCE.md`, the anchor
registry and sibling repos. No counter reads another claim's surface.

Frontier step: S257 (GNU Bash Reference Manual, Pipelines) opened 2026-10-30 and registered `queued` this round;
C2 is the sourced claim resting on it (with S256); the lesson's Gate records URL, access date and the located
quote. Assimilation: none (the staged `merge/tsukuroi` package still collides with the lane registry — 57 ids —
and no entry is adopted this round). `considerthese`: the still-unimplemented counter-attack-scoreboard proposal
(`considerthese/2026-10-26.md`) is landed this round as a lesson table with a verification seat.

## Axes — current self-assessment (round 52 frozen surface)

Restated 2026-10-30 at the round-52 freeze tree; ordinals unchanged (no axis moved before data). Counts re-derived
with the commands in each cell at the freeze tree (K08 4605→4606 and K09 1337→1338 are the round-51 registry rows
plus this round's `scrub-admission-r52` row; K10 77→78 adds the post-hoc `corpus/lessons/round-51.md`).

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 67 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); `SKILL.md` 4606 `wc -l` / 1338 table lines (`grep -c '^\|' SKILL.md`); `corpus/lessons/` 78 files (`find corpus/lessons -type f \| wc -l`); GR1-GR3 pending under C1 (`verdicts_ok 0`, `before/c1-at-base.json`); no ordinal move. | round 4; unchanged |
| coverage | 9 | `corpus/README.md` 522 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; no surface promotion. | round 11; unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` → PASS (168 cases, 168 passed, 0 failed); `--identity` landed; `bash tools/boot-chain-audit.sh --selftest` `PASS total=49 failed=0`; `check-fd-band-r49.py` accepts later case additions while retaining R49-C3. | round 11; unchanged |
| freshness | 9 | S240 re-opened byte-identically at sha256 `7b3488f2…ba01` (r51 spot-check §4, agree); S257 opened 2026-10-30; sources census exit 0 at round start (`.ufo/waves/round-52/before/sources-census-start.txt`). | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <FREEZE>` → 27 checked, 0 mismatches after this restatement (receipt committed with the wave evidence); at base before the restatement: 3 (K08, K09, K10). | round 10; unchanged |
| adjacency | 8 | formal overlap table present (PROVINCE `\| ID \| Finding`); C3 legs all green at base with `r50_blind 1` (`before/c3-at-base-r52.json`); caller-supplied C3 overrides can still score fabricated input (`R50CritCheatC3.md`). | fleet round 1; unchanged |

## Round 52 — measured outcome (author-side; non-author closure pending)

Freeze `ff9470ea`; wave evidence `4ee3226d`; ONE v2 wave `w1` of 64 seats (attack roles 42/64 =
65.6%), WAVE-DONE received before filing. Wave accounting: 64 dispatched, 64 results entries, 58
report files, no duplicate names, no residual call. **Dead/file-less seats (4):** `R52CritGR1b`,
`R52CritGR3b` (counted cohort; full transcripts, no report file — cut mid-turn),
`R52CritLimits`, `R52ScoutArch` (empty output; provider loss). Two further seats ended mid-turn with
partial output and no report (`R52MutScorer`, `R52CritHoleC3Relink`) — their items are named
unverified. No seat was replaced (orchestrator recovery boundary).

| Claim | Frozen predicate → measured | Verdict | Axis effect |
|---|---|---|---|
| C1 depth | `python3 tools/check-scrub-admission-r52.py --revision ff9470ea --wave-dir .ufo/waves/round-52/w1 --results-file .ufo/waves/round-52/w1-results.json --dispatch-file .ufo/waves/round-52/w1-dispatch.json` → `structural_ok 1, lint_ok 3, quotes_ok 3, verdicts_ok 1, seats_ok 16, marks_ok 0`, FAIL (`.ufo/waves/round-52/after/c1-at-freeze.json`). GR1 `holds` by all five bound seats; GR2 blocked by all six bound seats — one clause family: entry lines 233-235 say a resume-suspended replace "shows in neither" attribute, contradicted for `replace_target` (the resume-failure branch sets SUSPENDED without clearing REPLACE_TGT, dev-replace.c 1235-1242; the mount-time restore re-sets it when a target is present, 170-174/196-210); GR3 blocked `partly` by three (the SIGINT handler-window sentence overstates: the sigaction result is discarded at scrub.c 1546, and thread-creation failures jump to `out` at 1712, bypassing the 1710 reset). `R52CritGR1b`/`R52CritGR3b` never wrote report files → `seats_ok 16`. No admission mark written; the entry's round-52 Gate-status section records outcome + replacement texts. | **FAIL** | depth unchanged (8); rows stay pending; the fix set is two single-clause amendments |
| C2 operability | `python3 tools/score-counter-cheats-r51.py` → `real_pass 1, cheats 5, cheats_rejected 5, r50_cheats_rejected 0` — the valid 5-cheat receipt (seat run at the freeze `.ufo/waves/round-52/w1/R52ExecValidC2/c2-scorer.json`; L1 run `after/c2-final.json`, revision `ff9470ea`; scorer inputs byte-identical from the freeze through the integration commit, proof diff in `after/`). Limits unchanged from round 51 and named: override-injection forgery of the C1 counter (R52CritForgeC1a), F5/mutant-replay name-recognition reproducers and honest-respell false negatives (R52RevHoleC2EQ). | **PASS measured** | operability unchanged (9, saturation); no new capability row; the routed round-51 defect (broken amend1 receipt) is closed with a valid one |
| C3 adjacency | `python3 tools/check-adjacency-table-r51.py --revision ff9470ea` → full-leg PASS (`adj_rows 7, linked_rows 7, anchors_ok 7, registry_ok 7, quote_at_pin_ok 9, live_quote_ok 9, stub_fails 1, display_bound_ok 10, quote_specific_ok 10, digests_bound_ok 10, display_forge_fails 1, override_blocked 1, r50_blind 1, anchor_rows_exact 1, adj_exact 1, bare_all 0, ancestry_ok 10, recipient_ok 7`) at the named revision; battery 15/15 at the freeze. Limit: 6 of 9 r51 counter mutants survive the battery (R52MutAdj) — detector limits, disclosed. | **PASS measured** | adjacency unchanged (8); the routed round-51 defect (no named-revision measurement) is closed |

Round-level admission: **not admitted** — C1 fails; C2/C3 are instrument-measurement completions and
move no ordinal. No axis harmed: operability's instruments measured green; the entry gained an honest
Gate-status section; SOURCES gained one correctly-anchored row (anchor defect found by R52ScoutS257
and fixed before the commit); PROVINCE untouched.

## Axes — current self-assessment (round 52 final measured surface)

Restated 2026-10-30 at the round-52 final tree; ordinals unchanged. Counts re-derived with the
commands in each cell (K10 78 → 79 adds `corpus/lessons/round-52.md`; SKILL/README unchanged since
the freeze).

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 67 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); `SKILL.md` 4606 `wc -l` / 1338 table lines (`grep -c '^\|' SKILL.md`); `corpus/lessons/` 79 files (`find corpus/lessons -type f \| wc -l`); GR1-GR3 pending: round-52 counted cohort bound `verdicts_ok 1, seats_ok 16` (`.ufo/waves/round-52/after/c1-at-freeze.json`); no ordinal move. | round 4; unchanged |
| coverage | 9 | `corpus/README.md` 522 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; no surface promotion. | round 11; unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` → PASS (168 cases, 168 passed, 0 failed); `--identity` landed; `bash tools/boot-chain-audit.sh --selftest` `PASS total=49 failed=0`; the 5-cheat scorer receipt valid at the round-52 integration revision (`.ufo/waves/round-52/after/c2-final.json`). | round 11; unchanged |
| freshness | 9 | S240 re-opened byte-identically at sha256 `7b3488f2…ba01` (r51 spot-check §4); S257 opened 2026-10-30 and mined; sources census exit 0 at start, freeze and round end. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <integration commit>` → 27 checked, 0 mismatches (restated here); at the r52 base before restatement: 3 (K08, K09, K10). | round 10; unchanged |
| adjacency | 8 | formal overlap table present (PROVINCE `\| ID \| Finding`); C3 full-leg PASS at the named revision with `r50_blind 1` (`after/c3-final.json`); 6 of 9 counter mutants survive the battery (R52MutAdj) — disclosed. | fleet round 1; unchanged |

- **planned (next round):** depth — amend the two named clauses (GR2's resume-suspended observability
  sentence; GR3's SIGINT handler-window sentence) using the replacement texts the cohort proposed
  (`R52RevGR2{a,b,c}.md`, `R52RevGR3{a,c}.md`, `R52CritGR3c.md`), re-hash, and re-count with a fresh
  18-seat cohort under the QUALITY 96 write-first rule; report the two lost seats' items
  (`R52CritLimits`, `R52ScoutArch`) and the two mid-turn seats (`R52MutScorer`, `R52CritHoleC3Relink`)
  as unverified work if not re-run. Adjacency — fold the six surviving C3-counter mutants
  (R52MutAdj) into the disclosed-limits list or the battery, owner's choice next round.
- **retired:** none.

## Round 53 — declaration (2026-10-31, base `d4f2ffe17a461140017ad596f73d0f2d9d8d6c22`, FRESH-START host, written before any measurement)

FRESH-START round on a new host: this is Windows 10.0.26200 x64 under Git Bash (MSYS/Cygwin bash 5.3.15);
the Arch Linux host the rounds 1-52 instruments assume is gone. Last three closures were
`rejected-honest-stop` (r50, r51, r52), all on the C1 depth claim (`corpus/knowledge/btrfs-scrub-grounding-r45.md`
GR1-GR3 + a counted 18-seat cohort). Fresh-start spot-check of the three rejections, and what is ruled out:

- **Ruled out — r52's planned depth resume** (amend GR2's resume-suspended-observability clause and GR3's
  SIGINT handler-window sentence, re-count with a fresh 18-seat cohort). The counted-cohort wave machinery
  (AgentSwarm dispatch, `w1-dispatch.json`/`w1-results.json` via the hyaku driver) is absent on this host and in
  this session's toolset, so `seats_ok == 18` in the frozen predicate of `check-scrub-admission-r52.py` can never
  be measured here; the claim's verdict could not be produced, only asserted. A do-nothing control cannot reach
  it, but neither can this round; it stays queued behind the operator (L0 question filed this round).
- **Ruled out — re-declaring C2/C3-style instrument-measurement completions** on the r51 counters: r52 already
  measured both PASS (do-nothing control reached them — no fresh axis-move), and their receipts bind r50-r52
  wave bytes that are not re-runnable here.
- **Ruled out — claiming the old census (`tools/tsukuroi-census.sh`) as operability evidence on this host:**
  measured at round start, its hermetic `--selftest` does not complete — 40 of 168 cases in 90 s (rc 124) and
  still incomplete at 420 s (rc 124, 40 PASS lines, 0 FAIL before the cut), so the historical 168-case PASS
  cannot be reproduced here. Recorded as a drift finding (C3), not smoothed into a claim.
- Lowest-axis duty: depth and adjacency are tied lowest at 8; **C2 works depth**. Saturation 9 / window 3; not
  every axis sits at the line, so no stagnation-nudge waiver applies. The L2 floor (MISSION.md ≥8 in one
  batched AgentSwarm call) has no dispatch surface on this host — recorded as an absent surface, not silently
  skipped; this round is single-session inline per its prompt (§3 helpers optional).

Ordinals at base: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. All three claims
are measured on THIS host against committed bytes; repair actions stay operator-gated (read-only probes and
documented repair plans only).

| Claim | Axis | Surface moved | Counting command | Do-nothing control at base | Target (predicate) |
|---|---|---|---|---|---|
| C1 | operability (capability acquisition) | `tools/win-host-census-r53.py` — the lane's first gate for this Windows host: four planes (`tools` tool presence, `path` health, `python` interpreter identity, `git`/`gh` state), plane lines + `WIN_CENSUS` rollup, exit map 0 clean / 1 degraded / 2 could-not-evaluate, hermetic `--selftest` over injected resolvers; registry row and capabilities row land the same round | `python tools/win-host-census-r53.py --selftest` (last line `WIN_CENSUS_SELFTEST: PASS (N cases, N passed, 0 failed)`, rc 0); live: `python tools/win-host-census-r53.py` (rc matches the rollup rule) | at base the tool does not exist: `git cat-file -e d4f2ffe1:tools/win-host-census-r53.py` exits 128; the counting command exits 2 (`can't open file`) | selftest `cases == N and passed == N` rc 0 AND the live run emits all four plane lines with rc matching the rollup; disclosed limit: the selftest injects resolvers (logic proof), the live leg is the host-state reading |
| C2 | depth (lowest tied, 8; sourced S258 S259, opened this round) | `corpus/knowledge/windows-host-plane-r53.md` — sourced decision table for the Windows host tool-state plane, ≥6 rows each with a named error signature and an S-row or dated host capture: the `python3` WindowsApps alias stub (rc 49), `where.exe` current-directory+PATH+PATHEXT search (S258), per-session fnm shim dirs in PATH, duplicate PATH values, PATH entries whose directory is absent, the `python` vs `python3` interpreter naming (S259) | `grep -c "^| W" corpus/knowledge/windows-host-plane-r53.md`; header duty: `python tools/check-knowledge-header.py --worktree` | the file is absent at base: `grep -c` exits 2 (0 rows); 0 sourced Windows-host rows exist in the corpus (`grep -rl "WindowsApps" corpus/knowledge/` at base is empty) | rows ≥ 6 AND the knowledge-header gate reads 0 findings AND every row cites S258/S259 or a dated capture command; depth ordinal unchanged (8) — the move is recorded in the move log, not the ordinal |
| C3 | freshness | `corpus/knowledge/host-transition-drift-r53.md` — dated drift register: every Linux-only surface the operative census/SKILL checklist names, probed against this host with the measured command, observed result and recheck cadence; `PROVINCE.md` gains the dated host-transition record (protocol correction, §6 absent-surface rule) and the correction is logged | `grep -c "^| D" corpus/knowledge/host-transition-drift-r53.md` | the register is absent at base: `grep -c` exits 2 (0 flagged items); PROVINCE.md at base names zero surfaces that resolve on this host | rows ≥ 8 AND every row carries its probe command, observed result and capture date AND the PROVINCE correction is logged in LOG.md; freshness ordinal unchanged (9, saturated) |

Causal separability: C1 reads its own tool + the live host; C2 reads its entry + SOURCES + the header gate; C3
reads its register + PROVINCE.md + the measured probe results. No claim's counter reads another claim's surface.
All three are single-session inline (no wave dispatch exists on this host); the counted-cohort depth resume stays
operator-gated. Frontier step this round: SOURCES rows S258 (Microsoft Learn, `where`) and S259 (Python 3.13
Windows docs) opened by the L1; C2 is the sourced claim. Assimilation: `considerthese/` mined; no proposal
adopted (all four open ones are calibrated to the old host's wave machinery). Round-start census: exit 0,
40 W04 (`.ufo/waves/round-53/before/sources-census-start.txt`).

## Round 53 — measured outcome (2026-10-31, author-side; non-author closure pending)

Base `d4f2ffe1`; declaration commit `b3421a8d`; work commit `9160ffb85bd6ebd841d71c560637de4c7aebcb64`. Single-session inline
round: the counted-cohort wave machinery has no dispatch surface on this host (recorded absent; L0
question filed), so no wave seats were dispatched and no claim binds a cohort. All measurements run on
this host against the working tree at the work commit.

| Claim | Counting command → measured | Verdict | Axis effect |
|---|---|---|---|
| C1 operability (capability acquisition) | `python tools/win-host-census-r53.py --selftest` → `WIN_CENSUS_SELFTEST: PASS (20 cases, 20 passed, 0 failed)` rc 0 (`.ufo/waves/round-53/after/win-census-selftest.txt`); live `python tools/win-host-census-r53.py` → `WIN_CENSUS: DEGRADED (git=GREEN path=DEGRADED python=DEGRADED tools=DEGRADED)` rc 1, all four planes (`.ufo/waves/round-53/after/win-census-live.txt`). Before at base `d4f2ffe1`: `git cat-file -e` exits 128, command rc 2 (`before/c1-at-base.txt`). | **PASS measured** — the capability runs, its output verifies, the row entered the capabilities table the same round | operability unchanged (9, saturated); acquisition recorded |
| C2 depth (lowest tied, 8; sourced S258 S259 opened this round) | `grep -c "^| W" corpus/knowledge/windows-host-plane-r53.md` → **7** (target ≥6); base: rc 2, 0 rows and `grep -rl WindowsApps corpus/knowledge/` empty (`before/c2-at-base.txt`); header duty: `python tools/check-knowledge-header.py` at the work commit; every row cites S258/S259 or a dated capture | **PASS measured** | depth unchanged (8) — the move is the sourced decision table, not the ordinal |
| C3 freshness | `grep -c "^| D" corpus/knowledge/host-transition-drift-r53.md` → **12** (target ≥8); base: rc 2, 0 rows (`before/c3-at-base.txt`); every row carries probe + observed + date; PROVINCE dated correction logged in LOG.md | **PASS measured** | freshness unchanged (9, saturated); the dated register + correction is the move |

Named limits: `check-self-assessment.py` is could-not-evaluate on this host (K13 runs the census
selftest; the selftest stalls at case 41 — 40 PASS / 0 FAIL at 90 s and 420 s budgets, rc 124, D7); the checker run itself measured TimeoutExpired at its own 900 s budget (`.ufo/waves/round-53/after/self-assessment-at-work.txt`, rc 1);
the K07-K12 counts were recomputed manually with the same commands and the axes table restated to
them below. The old census 168-case PASS stays a Linux-host fact, not citable here. D12 second-session
behavior: labeled inference.

## Axes — current self-assessment (round 53 final measured surface)

Restated 2026-10-31 at the round-53 final tree; ordinals unchanged (all three claims are measured
moves that do not re-rank the saturated axes; the depth move is the sourced entry, not a number).
Counts re-derived with each cell's command at this tree.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 69 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); `SKILL.md` 4627 `wc -l` / 1339 table lines (`grep -c '^\|' SKILL.md`); `corpus/lessons/` 81 files (`find corpus/lessons -type f \| wc -l`); the sourced Windows-host plane W1-W7 landed round 53 (round-53 measured outcome); GR1-GR3 of the scrub entry remain pending behind the operator-gated cohort resume; no ordinal move. | round 4; round-53 entry added, ordinal unchanged |
| coverage | 9 | `corpus/README.md` 522 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; the round-53 host-transition correction records the current host's surfaces without re-homing any row. | round 11; unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` → PASS (168 cases, 168 passed, 0 failed) on its Linux host class (non-runnable here — stalls at case 41, D7); `python tools/win-host-census-r53.py --selftest` → PASS (20 cases, 20 passed, 0 failed) on this host; `--identity` landed; live census DEGRADED rc 1 (`.ufo/waves/round-53/after/win-census-live.txt`). | round 11; round-53 gate added, ordinal unchanged |
| freshness | 9 | drift register D1-D12 with dated probes (`corpus/knowledge/host-transition-drift-r53.md`); S258/S259 opened 2026-10-31; sources census exit 0 at round start and end (`.ufo/waves/round-53/{before,after}/sources-census-*.txt`). | fleet round 1; round-53 register added, ordinal unchanged |
| calibration | 9 | the axes table above restated to counts recomputed on this host; `python tools/check-self-assessment.py` cannot evaluate here (K13 needs the census selftest, non-runnable — named limit, round-53 measured outcome); at the r52 close the checker read 27 checked, 0 mismatches on its host. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (PROVINCE `\| ID \| Finding`); no sibling scope touched this round; the host transition absorbs nothing (drift register D10 routes the surface split by question). | fleet round 1; unchanged |

- **planned (next round):** operator-gated first — the L0 question (wave-dispatch surface) decides
  whether the r52 depth resume (amend GR2/GR3, fresh 18-seat cohort) is reachable; if the lane stays
  on this host: extend `win-host-census-r53` with the two PATH repairs' verification arms (RP1/RP2
  post-state probes), source the `fnm` session-dir behavior (D12) from a second session, and port the
  drift register's recheck loop into a committed probe so D1-D7 re-verify by one command.
- **retired:** none.

## Round-54/30 duplicate-section deduplication — correction (round 55; names every superseded copy)

This SCORECARD carried four UNMARKED duplicate level-2 headings when round 55 opened (each a
section reposted under the byte-identical heading with no in-body supersession marker — the defect
class that produced routed defect 1 of closure `59a62bfe`). Repair R1 removes the superseded copy
of each and names it here — not a silent delete:

1. "## Round 54 — declaration (2026-10-31, base `5cbcb06e…`, written before any measurement)" —
   twice at the closure tip (`59a62bfe`, lines 3505 and 3565; both copies landed at `f24ca241`).
   Removed copy: the FIRST. The two copies differed by exactly one word, verified by `diff` before
   removal: the removed copy's claim-C2 surface cell read "MSYS `/opt` mangling of
   `schtasks /query`"; the retained copy reads "MSYS `/query` mangling of `schtasks /query`",
   which matches the measured T1 signature (`ERROR: Invalid argument/option -
   'C:/Program Files/Git/query'.`, receipt
   `.ufo/waves/round-54/after/services-probes/t1-msys-mangled-error.txt`). No other byte differed
   between the copies. The authoritative section is the one that follows this block.
2. "## Round 30 — declaration, attempt 1 (2026-10-22)" — twice (worktree lines 1140 and 1181 when
   this repair opened). Removed copy: the SECOND, a byte-exact 15-line PREFIX repost of the first
   (verified: `b == a[:len(b)]` over the two section bodies), carrying no unique content. The
   authoritative section is the first, which also carries the round-30 measured-outcome subsection.

Three further duplicate-heading pairs were found by the same sweep and are NOT duplicates in
content — they are this file's older declared-correction convention, where the LATER copy's body
explicitly names and corrects its predecessor ("This table supersedes the earlier round-26 table";
"Correction to the immediately preceding round-37 axis table"; "Correction to the preceding
round-37 capability table"): "## Axes — current self-assessment (round 26)" (the later copy
restates only the two counts the wave-2 repair commit changed), "## Axes — current self-assessment
(round 37)" and "## Capabilities — current (round 37)" (each a correction to the preceding table).
They stay; removing them would delete historical rows the correcting copies do not restate.
Uniqueness with declared supersession is enforced from this round forward by
`tools/check-scorecard-unique-sections.py` (claim C3): it fails on any duplicate `##` heading pair
where NEITHER body declares the supersession.
## Round 54 — declaration (2026-10-31, base `5cbcb06e026720adf3d1eb8cf3c8dabab4dac72e`, written before any measurement)

Context: r53 was admitted (closure `5cbcb06e`); the four routed defects of that closure are this
round's repairs first (R1-R4 below; repairs are not claims, per the r33/r34 precedent). The rendered
prompt's §7 FRESH-START block names the three prior `rejected-honest-stop` closures (r50 `72c114a5`,
r51 `daf5b626`, r52 `5b147403`, all in the fleet repo); spot-checked this round — the common binding
of all three is the counted-cohort depth resume, and the declared round rules out:

- **Ruled out — r52's counted-cohort depth resume (amend GR2/GR3, fresh cohort).** Still unreachable:
  this session has no subagent/wave dispatch surface (no AgentSwarm call available; L0 question filed
  round 53, unanswered — routed around, never treated as answered). A do-nothing control cannot reach
  the claim, but neither can this round; asserting `seats_ok` would be fabrication.
- **Ruled out — re-claiming r53's admitted moves** (win-host-census, windows-host-plane, drift
  register): they landed, verified, and a do-nothing control already reaches them — no fresh axis-move.
- **Ruled out — r53's planned "RP1/RP2 post-state verification arms"** for `win-host-census-r53`: the
  PATH/alias repairs are operator-gated and unexecuted, so post-state arms can only re-report today's
  DEGRADED state — nothing falsifiable moves. Deferred until the operator runs RP1/RP2.
- **Ruled out — sourcing D12's fnm second-session behavior**: requires a second concurrent session;
  this session is single and inline. Cannot be measured honestly here.
- **Ruled out — claiming the old census 168-case PASS as operability here** (r53's ruling stands): D7
  says it does not reproduce; this round re-derives its raw budget receipts as a repair, not a claim.

Reachable moves declared below. Lowest-axis duty: depth and adjacency are tied lowest at 8; **C2 works
depth**. Saturation 9 / window 3; not every axis sits at the line, so no stagnation-nudge waiver
applies. L2 floor (MISSION.md ≥8 in one batched AgentSwarm call): absent surface on this host —
recorded, routed around. Ordinals at base: depth 8, coverage 9, operability 9, freshness 9,
calibration 9, adjacency 8; none retired. Repairs R1-R4 (routed defects from closure `5cbcb06e`,
status-neutral, not claims):

- **R1** — S259 locator correction: closure verified against the raw page that the S259 Gate quote
  lives in §4.2 (The Microsoft Store package), not §4.6.2 (Finding the Python executable). Fix: new
  row **S260** whose `teaches` opens `supersedes S259 —` (contract v1 rule 2; census E04's supersedes
  exemption), written after re-opening the live page this round; the round-54 lesson carries the
  correction entry naming the superseded text — the round-53 lesson bytes are never rewritten.
- **R2** — Gate word-count drift, same correction entry: recount by command gives S258 = **18** words
  (stated 24), S259 = **20** words (stated 21); both ≤25 so the contract bound holds; old→new recorded.
- **R3** — D7/W5 raw budget receipts: re-derived this round under the same budgets (90 s, 420 s) with
  raw outputs committed at `.ufo/waves/round-54/d7-receipts/` — receipts live in the lane tree, never
  scratch; C1's instrument produces them.
- **R4** — D-row dating form: the drift register gains an appended dated correction block giving
  D1-D12 in-row probe dates (append-only; the original table bytes stay untouched).

| Claim | Axis | Surface moved | Counting command | Do-nothing control at base | Target (predicate) |
|---|---|---|---|---|---|
| C1 | operability (capability acquisition) | `tools/receipt-run.py` — a budgeted command runner that writes raw receipts into the lane tree (command argv, start/end ISO-8601, duration, rc or `timeout_after=<budget>s`, verbatim stdout/stderr), hermetic `--selftest` over an injected runner; first working use = the D7 budget re-derivations (R3) committed at `.ufo/waves/round-54/d7-receipts/` | `python tools/receipt-run.py --selftest` (last line `RECEIPT_RUN_SELFTEST: PASS (N cases, N passed, 0 failed)`, rc 0); `ls .ufo/waves/round-54/d7-receipts \| wc -l`; `grep -c "^rc=" .ufo/waves/round-54/d7-receipts/d7-selftest-90s.txt` | at base the tool does not exist: `git cat-file -e 5cbcb06e:tools/receipt-run.py` exits 128; the receipts dir does not exist | selftest PASS rc 0 AND ≥2 D7 receipts present, each naming its budget and rc/timeout line AND stdout captured verbatim (PASS-line count matches the recorded D7 signature class); capability row enters the SCORECARD table the same round |
| C2 | depth (lowest tied, 8; sourced S261 S262, opened this round) | `corpus/knowledge/windows-services-plane-r54.md` — sourced decision table for the Windows service + scheduled-task plane (the operable analog of the ABSENT D2 systemd plane): ≥6 rows T1-T7+, each with a named error signature, every row citing S261/S262 or a dated host capture; includes the measured doc-vs-host divergences (MSYS `/query` mangling of `schtasks /query`; `sc` inside powershell.exe silently aliasing to Set-Content and writing a file; `sc` rc 36 for win32 1060; the documented `type= interact` error not firing on this host) | `grep -c "^| T" corpus/knowledge/windows-services-plane-r54.md`; header duty: `python tools/check-knowledge-header.py --worktree` | the file is absent at base: `git cat-file -e 5cbcb06e:corpus/knowledge/windows-services-plane-r54.md` exits 128; `grep -c` exits 2 (0 rows) | rows ≥ 6 AND the knowledge-header gate reads 0 findings AND every row cites S261/S262 or a dated capture command; depth ordinal unchanged (8) — the move is the sourced entry, not the ordinal |
| C3 | freshness | `tools/recheck-drift-r54.sh` — the drift register's recheck loop ported into one committed read-only command: re-runs the D1-D6 `command -v` probes, the D7 90 s budget leg, D8 interpreter identity, D9 via the census path plane, D12 node-shim shape, and greps the register + PROVINCE for the D10/D11 doc rows; emits one `D<k> match\|drift\|doc-row` line per register row and rc 0 iff no drift; receipt committed at `.ufo/waves/round-54/after/recheck-drift-r54.txt` | `bash tools/recheck-drift-r54.sh` (rc 0; 12 lines matching `^D[0-9]+ `); before: script absent at base (rc 128), the command exits 127 | at base the script does not exist and the register's recheck loop exists only as prose in three files | rc 0 AND 12 row lines AND every host-probed row reads `match` on this host-day (a `drift` line is honest output and would owe an appended register correction — expected none) |

Causal separability: C1 reads its own tool + its receipts; C2 reads its entry + SOURCES + the header
gate; C3 reads its script + the register + PROVINCE + the host — C3's D7 leg uses plain `timeout` +
shell redirect, NOT C1's instrument, and its 420 s leg is covered by R3's separately committed
receipt (pointer, disclosed), so no claim's counter reads another claim's surface. All three are
single-session inline; the counted-cohort resume stays operator-gated. Frontier step: S260
(supersedes-S259 correction), S261 (Microsoft Learn `schtasks query`), S262 (Microsoft Learn
`sc.exe query`) — S261/S262 opened this round; C2 is the sourced claim. Round-start census: exit 0,
40 W04 (`.ufo/waves/round-54/before/sources-census-start.txt`). Assimilation: `considerthese/` mined
(2026-10-26 "cross-note correction propagation map" — its core move is applied once inside R1's
correction entry: dependent surfaces enumerated and each confirmed corrected; the full map is not
built this round); nothing else adopted.

## Round 54 — measured outcome (2026-10-31, author-side; non-author closure pending)

Declaration `13554741`; work `f24ca241`; work-amend1 `0cd50d45` (registry rows fixed from the
coverage gate's four findings — kind `probe` not `instrument`, census path de-spelled from the
recheck row, verdict code 2 added). All measurements run on THIS host at the work tip `0cd50d45`
(counting battery: `.ufo/waves/round-54/after/c1-c2-c3-counts-at-work.txt`); before-receipts at the
declaration commit (`.ufo/waves/round-54/before/c{1,2,3}-at-base.txt`, each rc 128 = absent).

| Claim | Counting command → measured | Verdict | Axis effect |
|---|---|---|---|
| C1 operability (capability acquisition) | `python tools/receipt-run.py --selftest` → `RECEIPT_RUN_SELFTEST: PASS (7 cases, 7 passed, 0 failed)` rc 0; `ls .ufo/waves/round-54/d7-receipts \| wc -l` → **2**; `grep -c "^rc=" d7-selftest-90s.txt` → **1** (`rc=timeout`, `timeout_after_s=90`; 420 s receipt likewise `rc=timeout`, timeout_after_s=420). Before at `13554741`: `git cat-file -e` rc 128 (`before/c1-at-base.txt`), receipts dir absent. | **PASS measured** — the capability runs, its output verifies, the row entered the capabilities table the same round; first working use is repair R3 | operability unchanged (9, saturated); acquisition recorded |
| C2 depth (lowest tied, 8; sourced S261 S262 opened this round) | `grep -c "^| T" corpus/knowledge/windows-services-plane-r54.md` → **8** (target ≥6); base: rc 2, 0 rows (`before/c2-at-base.txt`); header duty `python tools/check-knowledge-header.py --revision 0cd50d45` → PASS, 70 notes, 0 findings (`.ufo/waves/round-54/after/knowledge-header-at-work.txt`); every row cites S261/S262 or a dated capture | **PASS measured** | depth unchanged (8) — the move is the sourced decision table, not the ordinal |
| C3 freshness | `bash tools/recheck-drift-r54.sh --receipt .ufo/waves/round-54/after/recheck-drift-r54.txt` → rc 0, `RECHECK_DRIFT: PASS (12 rows, 10 host-probed match, 2 doc rows, 0 drift)`, 12 `^D[0-9]` lines. Before at `13554741`: script absent, rc 128 (`before/c3-at-base.txt`); the recheck loop existed only as prose in three files. | **PASS measured** — 10/10 host probes match their recorded observations on this host-day; no correction owed | freshness unchanged (9, saturated); the executable recheck loop + receipt is the move |

Repairs landed (routed defects of closure `5cbcb06e`, not claims): **R1** S260 correction row
(`grep -c "supersedes S259" corpus/SOURCES.md` → 1; locator §4.6.2 → §4.2, verified by re-opening
the live page this round); **R2** word-count correction recorded in the round-54 lesson (S258
24 → 18, S259 21 → 20, both recounted by `wc -w`, both ≤25 so the contract bound holds); **R3** the
D7/W5 raw budget receipts re-derived and committed (`.ufo/waves/round-54/d7-receipts/`, 90 s and
420 s, both rc=timeout — today's partial counts 5 and 30 PASS lines vs r53's 40/40 are wall-clock
facts of session load, same drift class: stall, no FAIL, no summary line); **R4** the D-register's
appended dated-correction block gives D1-D12 in-row probe dates (`grep -c "^D[0-9]"` → 12) while the
original table bytes stay untouched.

Named limits: the D7 90 s/420 s receipts record UTC stamps that cross into 2026-11-01Z (local date
2026-10-31, UTC-07:00); the 90 s receipt's duration_s=112.8 includes the child-kill grace — the
budget and the timeout verdict are what the receipt asserts. `check-self-assessment.py` remains
could-not-evaluate on this host (K13 needs the census selftest; non-runnable — named limit, r53).
The registry-coverage gate found four defects in the first registry rows (work `f24ca241` FAIL
receipt superseded by the amend `0cd50d45` PASS receipt: 92 tools / 92 rows / 0 findings); the FAIL
receipt was overwritten in place by the PASS run at the amended tip — the FAIL JSON is quoted in
LOG.md and the lesson records the class.

## Axes — current self-assessment (round 54 final measured surface)

Restated 2026-10-31 at the round-54 final tree `0cd50d45`; ordinals unchanged (all three claims are
measured moves on saturated or lowest axes; the depth move is the sourced entry, not a number).
Counts re-derived with each cell's command at this tree.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 70 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); `SKILL.md` 4653 `wc -l` / 1341 `grep -c '^\|' SKILL.md` lines; `corpus/lessons/` 83 files at the outcome tree (`find corpus/lessons -type f \| wc -l`; 82 at the work tree `0cd50d45` + this round's lesson); the sourced services/tasks plane T1-T8 landed round 54 (round-54 measured outcome); GR1-GR3 of the scrub entry remain pending behind the operator-gated cohort resume; no ordinal move. | round 4; round-54 entry added, ordinal unchanged |
| coverage | 9 | `corpus/README.md` 522 `wc -l` (unchanged — no surface map row added; the services/tasks plane documents the current host inside the province's round-53 host-transition record); PROVINCE Core, Frontier and Adjacent sections present. | round 11; unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` PASS (168/168) on its Linux host class (non-runnable here, D7); `python tools/win-host-census-r53.py --selftest` PASS (20/20); `python tools/receipt-run.py --selftest` PASS (7/7) round 54; live census DEGRADED rc 1; registry-coverage 92/92 at `0cd50d45`. | round 11; round-54 probes added, ordinal unchanged |
| freshness | 9 | drift register D1-D12 re-verified by one committed command, 0 drift (`.ufo/waves/round-54/after/recheck-drift-r54.txt`); S260 correction row + in-row dating block land the routed locator/dating fixes; sources census exit 0 at round start and end (`.ufo/waves/round-54/{before,after}/sources-census-*.txt`, 40 → 41 W04 warnings, the +1 the S260 same-URL correction row, warning-class). | fleet round 1; round-54 recheck loop added, ordinal unchanged |
| calibration | 9 | the axes table above restated to counts recomputed on this host; `python tools/check-self-assessment.py` cannot evaluate here (K13, named limit); the gate-found registry-row defects were recorded, not smoothed (r54 lesson R54-REGISTRY-KIND). | round 10; unchanged |
| adjacency | 8 | formal overlap table present; no sibling scope touched; the services/tasks plane is the lane's own host-operability domain on the current host (PROVINCE round-53 record); nothing absorbed. | fleet round 1; unchanged |

- **planned (next round):** operator-gated first — the L0 wave-dispatch question still decides the
  r52 depth resume; if the lane stays on this host: source the fnm session-dir behavior (D12) from a
  second session when one exists, extend `recheck-drift-r54.sh` with a `--budget` flag so the D7 leg
  can take the 420 s budget without editing the script, and give `win-host-census-r53` a
  `--receipt` mode routed through `receipt-run.py` so the live reading commits itself the same way.
- **retired:** none.

## Round 55 — declaration (2026-10-31, base `59a62bfe07bbf109a59d92d220afee1fd10fd8eb`, written before any measurement)

Context: r54 was admitted (closure `59a62bfe`, non-author verifier spot-check). That closure routed
three defects; they are this round's repairs first (R1-R2 below; repairs are not claims, per the
r33/r34 precedent), and its two standing scope L0s are routed around, never treated as answered. The
rendered prompt's §7 FRESH-START block names the three prior `rejected-honest-stop` closures (r50
`72c114a5`, r51 `daf5b626`, r52 `5b147403`, all in the fleet repo); spot-checked this round against
committed bytes — r50's `.ufo/waves/round-50/after/c1-final.json` reads `verdicts_ok 0, marks_ok 0,
seats_ok 18` (the honest FAIL), r51's `before/c2-cheats-at-amend1.json` does not exist at
`c0ad548a` (`git cat-file -e` fails — the live-peer output was never committed, as the closure
said), r52's `.ufo/waves/round-52/after/c1-final.json` reads `seats_ok 16` with 58 seat files vs the
18-seat frozen predicate — and the declared round rules out:

- **Ruled out — the counted-cohort depth resume (r50/r51/r52's common binding: amend GR2/GR3, fresh
  18-seat cohort through check-scrub-admission-r5x).** Still unreachable: this host exposes no
  wave/AgentSwarm dispatch surface (L0 `tsukuroi | round-53` stands unanswered — routed around,
  never treated as answered). A do-nothing control cannot reach the claim, but neither can this
  round; asserting `seats_ok` would fabricate.
- **Ruled out — re-claiming r53/r54's admitted moves** (win-host-census-r53, the T1-T8 services
  plane, the D1-D12 recheck loop): landed, verified, and a do-nothing control already reaches them —
  no fresh axis-move.
- **Ruled out — r53-planned RP1/RP2 post-state verification arms** for `win-host-census-r53`: the
  operator-gated PATH/alias repairs remain unexecuted, so post-state arms can only re-report today's
  DEGRADED state — nothing falsifiable moves. Deferred until the operator runs RP1/RP2.
- **Ruled out — sourcing D12's fnm second-session behavior**: requires a second concurrent session;
  this session is single and inline. Cannot be measured honestly here.
- **Ruled out — claiming a bare re-run of `recheck-drift-r54.sh` or a re-fetch of S261/S262 as a
  freshness move**: a do-nothing control reaches a pure re-run; freshness gains no new move this
  round (the round works operability, depth and calibration instead).
- **Carried, not claimed** (r54 planned list): `win-host-census-r53 --receipt` mode routed through
  `receipt-run.py` (C1 exercises the instrument on the T-probe set first), and
  `recheck-drift-r54.sh --budget <s>` (the 420 s leg stays covered by the r54 committed receipt).
  Both stay on the planned list for r56.

Reachable moves declared below. Lowest-axis duty: depth and adjacency are tied lowest at 8; **C2
works depth**. Saturation 9 / window 3; a capability entered the table in r54, so the stagnation
nudge does not apply. L2 floor (MISSION.md ≥8 in one batched AgentSwarm call): absent surface on
this host — recorded, routed around. Ordinals at base: depth 8, coverage 9, operability 9,
freshness 9, calibration 9, adjacency 8; none retired. Repairs R1-R2 (routed defects of closure
`59a62bfe`, status-neutral, not claims):

- **R1 — SCORECARD duplicate declaration (routed defect 1).** The section "Round 54 — declaration
  (2026-10-31, base `5cbcb06e…`)" appears TWICE at the closure tip (landed at `f24ca241`; verified
  by this round's `diff` of the two copies: exactly one word differs — the first copy's C2 row reads
  "MSYS `/opt` mangling", the second copy reads "MSYS `/query` mangling", which matches the
  measured T1 signature `Invalid argument/option - 'C:/Program Files/Git/query'`). Fix: keep exactly
  one authoritative copy (the `/query` wording), remove the superseded duplicate, and land a
  correction block naming the superseded text — not a silent delete.
- **R2 — S262 field-name correction row (routed defect 3).** S262's `teaches` names the display
  fields WIN32_EXIT_CODE / SERVICE_EXIT_CODE (matching every measured receipt, e.g.
  `t4-sc-active.txt`), while the page's Remarks literally read "WIN32_EXIT_B, SERVICE_EXIT_B" — a
  typo on the page. Fix: a SOURCES correction row written after re-opening the live page this round,
  recording the divergence; S262 stands for all other content (no supersedes — the row is right
  about the tool).

| Claim | Axis | Surface moved | Counting command | Do-nothing control at base | Target (predicate) |
|---|---|---|---|---|---|
| C1 | operability | The round-54 T-probe receipts become self-describing: the whole probe set re-derived through `tools/receipt-run.py` and committed at `.ufo/waves/round-55/reissued-r54/` — each receipt carries its own verdict metadata (command argv, budget, start/end UTC, duration, `rc=`, stream sizes), closing routed defect 2 (the r54 receipts are output-only; `t7-powershell-sc-alias-stdout.txt` is 0 bytes) | before: `grep -h "^rc=" .ufo/waves/round-54/after/services-probes/* \| wc -l` → 0 across 12 files; `wc -c < .ufo/waves/round-54/after/services-probes/t7-powershell-sc-alias-stdout.txt` → 0. after: `ls .ufo/waves/round-55/reissued-r54/* \| wc -l` → N; `grep -l "^rc=" .ufo/waves/round-55/reissued-r54/* \| wc -l` → N (all) | at base the reissued dir does not exist and no instrument re-issues the set; the r54 receipts stay output-only forever | N ≥ 10 receipts AND every one carries `^rc=` AND the re-derived t7 stdout receipt records `rc=0`, `stdout_bytes=0` and the full argv in its header (the 0-byte no-metadata class closed); the r54 receipts stay untouched |
| C2 | depth (lowest tied, 8; sourced S263 S264, opened this round) | `corpus/knowledge/windows-services-plane-r55.md` — sourced decision-table rows for the service-control extended query/config surface (`sc queryex`, `sc qc`), each row a named error signature citing S263/S264 (Microsoft Learn pages opened this round) or a dated receipt under `.ufo/waves/round-55/services-probes/` (its own dir, distinct from C1's); header duty `python tools/check-knowledge-header.py --revision <work>` | `grep -c "^| T" corpus/knowledge/windows-services-plane-r55.md`; header duty as above | the file is absent at base: `git cat-file -e 59a62bfe:corpus/knowledge/windows-services-plane-r55.md` exits 128; `grep -c` exits 2 (0 rows) | rows ≥ 3 AND the knowledge-header gate reads 0 findings AND every row cites S263/S264 or a dated receipt; depth ordinal unchanged (8) — the move is the sourced entry, not the ordinal |
| C3 | calibration | SCORECARD round-section uniqueness becomes an enforced invariant: `tools/check-scorecard-unique-sections.py` (gate; exit 0 every `^## ` heading unique, 1 on any duplicate with line numbers, 2 could-not-evaluate; hermetic `--selftest`); repair R1 is the gate's first real catch — a defect class the lane shipped twice and the non-author closure had to find | before: `git cat-file -e 59a62bfe:tools/check-scorecard-unique-sections.py` exits 128; `grep -c "^## Round 54 — declaration" SCORECARD.md` → 2. after: `grep -c` → 1 (R1 landed); `python tools/check-scorecard-unique-sections.py --selftest` → PASS rc 0; worktree run rc 0 | at base the gate does not exist and nothing on this host would flag the next duplicated SCORECARD section | selftest PASS rc 0 AND the worktree/committed SCORECARD run exits 0 AND `grep -c "^## Round 54 — declaration" SCORECARD.md` = 1 with the correction block naming the superseded duplicate; calibration ordinal unchanged (9, saturated) |

Causal separability: C1 reads only its reissued dir + the base-committed r54 receipts; C2 reads its
own knowledge file + SOURCES + the header gate + its own probe receipts in
`.ufo/waves/round-55/services-probes/` (a directory C1 never writes); C3 reads SCORECARD + its own
gate (its R1 precondition is a repair, not a claim). No claim's counter reads another claim's
surface. All three are single-session inline; the counted-cohort resume stays operator-gated.
Frontier step: S263 (`sc.exe queryex`), S264 (`sc.exe qc`) — Microsoft Learn pages opened this
round; S265 (correction note on S262, R2); C2 is the sourced claim. Round-start census: exit 0,
41 W04 (`.ufo/waves/round-55/before/sources-census-start.txt`). Assimilation: `considerthese/`
mined (latest 2026-10-26; the cross-note correction propagation map was partially applied in r54;
no still-unimplemented proposal clears this round's bar — the R1 dedupe is routed-repair work, not
an adopted proposal); nothing adopted.

## Round 55 — measured outcome (2026-10-31, author-side; non-author closure pending)

Declaration `76b9d9e5`; work `3ac4b124`. All measurements run on THIS host at the work tip
`3ac4b124` (counting battery: `.ufo/waves/round-55/after/c1-c2-c3-counts-at-work.txt`); before-
receipts at the declaration commit (`.ufo/waves/round-55/before/c{1,2,3}-at-base.txt`).

| Claim | Counting command → measured | Verdict | Axis effect |
|---|---|---|---|
| C1 operability | before (`before/c1-at-base.txt`): `grep -h "^rc=" .ufo/waves/round-54/after/services-probes/* \| wc -l` → **0** across the 12 output-only r54 receipts; `wc -c` of `t7-powershell-sc-alias-stdout.txt` → **0**; reissued dir absent. After: `ls .ufo/waves/round-55/reissued-r54/* \| wc -l` → **11**; `grep -l "^rc=" … \| wc -l` → **11** (every receipt self-describing); the re-derived t7 stdout receipt carries `command=powershell … sc query wuauserv`, `rc=0`, `stdout_bytes=0` — the 0-byte no-metadata class closed; rc verdicts in the receipts: t1 rc=1 (mangled T1 signature byte-matched), t3 rc=1, t5 **rc=36** (the value the r54 closure had to re-derive by hand), t6 rc=0 (divergence reproduces), t4-sc-active 109 SERVICE_NAME blocks / t4-sc-all 273 (host drift, documented class; wuauserv reads `4 RUNNING` today vs r54's `1 STOPPED` — drift, not smoothing); r54 receipts untouched (`git diff 59a62bfe 3ac4b124 -- .ufo/waves/round-54` empty). | **PASS measured** | operability unchanged (9, saturated); the receipt-run capability's second working use, and the routed-defect-2 rule now applied by default |
| C2 depth (lowest tied, 8; sourced S263 S264 opened this round) | before: file absent at base, rc 128 / grep rc 2 (`before/c2-at-base.txt`). After: `grep -c "^| T" corpus/knowledge/windows-services-plane-r55.md` → **4** (target ≥3); python row check: 4/4 rows cite S263/S264/S265 or a dated capture; header duty `python tools/check-knowledge-header.py --revision 3ac4b124` → PASS, 71 notes, 0 findings (`.ufo/waves/round-55/after/knowledge-header-at-work.txt`); SOURCES rows 262 → **265** (S263, S264, S265). Measured signatures: queryex adds PID + FLAGS and a wait-hint states line (T9); nonexistent-service = FAILED 1060 rc 36 for both queryex (T10) and qc (T12, function line `[SC] OpenService FAILED 1060:` vs query's `EnumQueryServicesStatus:OpenService`); qc shows START_TYPE + BINARY_PATH_NAME and codes TYPE differently from query (`20 WIN32_SHARE_PROCESS` vs `30 WIN32`, T11); S264's Remarks field list omits START_TYPE (doc-list incompleteness, recorded). | **PASS measured** | depth unchanged (8) — the move is the sourced entry, not the ordinal |
| C3 calibration | before: gate absent at base, rc 128 (`before/c3-at-base.txt`); `grep -c "^## Round 54 — declaration" SCORECARD.md` → **2**. After: `grep -c` → **1** (R1); `python tools/check-scorecard-unique-sections.py --selftest` → `SCORECARD_UNIQUE_SECTIONS: PASS (5 cases, 5 passed, 0 failed)` rc 0; the gate on the COMMITTED blob (`git show 3ac4b124:SCORECARD.md` → `--file`) reads ok rc 0 (`.ufo/waves/round-55/after/scorecard-unique-sections-at-work.txt`); worktree == committed (`git diff 3ac4b124 -- SCORECARD.md` empty). The gate's first real sweep found the routed r54 pair AND an unmarked round-30 declaration prefix-repost (removed, named) AND three legacy marked pairs (kept — see R1). | **PASS measured** | calibration unchanged (9, saturated); SCORECARD shape is now gate-enforced instead of prose |

Repairs landed (routed defects of closure `59a62bfe`, not claims): **R1** the SCORECARD dedupe —
the unmarked r54 declaration pair (one-word divergence, kept copy = `/query` wording matching the
measured T1 signature) and an unmarked round-30 declaration prefix-repost (`b == a[:len(b)]`, no
unique content) removed and named in the correction block "Round-54/30 duplicate-section
deduplication — correction"; the three legacy declared-correction pairs (r26 axes, r37 axes, r37
capabilities) stay, each already superseded in-body by its correcting copy — the sweep that found
them is what reshaped C3's predicate (lesson R55-ZERO-DUP-PREDICATE). **R2** SOURCES row S265 (the
page-side typo note; S262 stands). **Routed defect 2** (route T-probes through receipt-run) is C1's
surface: 11/11 reissued receipts carry rc/argv metadata.

Named limits: the C1 re-derivations are TODAY's captures, not r54's (service state and counts drift
with the host — wuauserv RUNNING vs STOPPED, 109 vs 110 active services, 273 total unchanged); the
claim's surface is the receipt METADATA, which is complete. S263/S264 are archived (2012-R2
library) pages, recorded as such in the rows and the knowledge note; the current reference's TOC
gap (no queryex/qc pages) is recorded, not smoothed. T10/T12's rc-36 arithmetic stays labeled
inference (1060 mod 256). `check-self-assessment.py` remains could-not-evaluate on this host (K13,
named limit, unchanged since r53). The L2 floor stays an absent surface, routed around. Gate
receipts at the work tip: registry-coverage PASS 93 tools / 93 rows / 0 findings;
knowledge-header PASS 71 notes / 0 findings; receipt-run selftest PASS 7/7; census start exit 0
(41 W04) → end exit 0 (42 W04, +1 = S265's same-URL warning, warning-class, no E-code).

## Axes — current self-assessment (round 55 final measured surface)

Restated 2026-10-31 at the round-55 final tree `3ac4b124`; ordinals unchanged (all three claims are
measured moves on saturated or lowest axes; the depth move is the sourced entry, not a number).
Counts re-derived with each cell's command at this tree.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 71 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); `SKILL.md` 4677 `wc -l`; `corpus/lessons/` 84 files (`find corpus/lessons -type f \| wc -l`); the sourced services extended-query/config plane T9-T12 landed round 55 (round-55 measured outcome; S263/S264 archive pages); GR1-GR3 of the scrub entry remain pending behind the operator-gated cohort resume; no ordinal move. | round 4; round-55 entry added, ordinal unchanged |
| coverage | 9 | `corpus/README.md` 522 `wc -l` (unchanged — the r55 plane extends the r54 services surface inside the same province record; no map row added or re-homed); PROVINCE Core, Frontier and Adjacent sections present. | round 11; unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` PASS (168/168) on its Linux host class (non-runnable here, D7); `python tools/win-host-census-r53.py --selftest` PASS (20/20); `python tools/receipt-run.py --selftest` PASS (7/7); 11/11 reissued r54 T-probe receipts carry rc/argv metadata (`.ufo/waves/round-55/after/c1-counts.txt`); live census DEGRADED rc 1; registry-coverage 93/93 at `3ac4b124`. | round 11; round-55 reissued-receipt battery added, ordinal unchanged |
| freshness | 9 | drift register D1-D12 re-verified by one committed command, 0 drift (r54 receipt stands; no register change this round); S262 re-opened live this round (S265 correction row), S261 unchanged; sources census exit 0 at round start and end (41 → 42 W04, the +1 warning-class, `.ufo/waves/round-55/{before,after}/sources-census-*.txt`). | fleet round 1; round-55 source re-verification added, ordinal unchanged |
| calibration | 9 | the axes table above restated to counts recomputed on this host; SCORECARD round-section uniqueness now gate-enforced (`tools/check-scorecard-unique-sections.py`, selftest 5/5, committed-blob run ok — `.ufo/waves/round-55/after/scorecard-unique-sections-at-work.txt`); the gate's first sweep caught an unmarked r30 repost the lane had shipped twice; `python tools/check-self-assessment.py` cannot evaluate here (K13, named limit). | round 10; round-55 uniqueness gate added, ordinal unchanged |
| adjacency | 8 | formal overlap table present; no sibling scope touched; the extended services surface stays inside the lane's own host-operability province (PROVINCE round-53 record); nothing absorbed; contested kaidoku/revenger ownership remains unruled (carried, routed around). | fleet round 1; unchanged |

- **planned (next round):** operator-gated first — the L0 wave-dispatch question still decides the
  r52 depth resume; if the lane stays on this host: give `win-host-census-r53` a `--receipt` mode
  routed through `receipt-run.py` (carried from r54's plan; C1 exercised the instrument on the
  T-probe set this round), add `recheck-drift-r54.sh --budget <s>` so the D7 leg can take the 420 s
  budget without editing the script, and extend the services plane's recheck discipline to the r55
  rows (fold T9-T12 into a recheck pass alongside the r54 T1-T8 probes on their 30d cadence).
- **retired:** none.

## Round-52 seat-file count — counting command (round 56; carry-in 1 of closure `aeb268f3`)

The "58 seat files" figure in "Round 55 — declaration" (the r52 spot-check bullet) is a
counting-convention number; this block supplies its command (a count carries its command,
CORPUS round-1 rules):

    git ls-tree -r --name-only HEAD -- .ufo/waves/round-52 | grep -cE "R52[A-Za-z0-9]*\.md$"
    # → 58  (measured 2026-11-01 at `62b47771`; identical at the r55 base `59a62bfe`)

Convention: EVERY seat-report `.md` of the round-52 wave across all role classes (Crit, Rev,
Exec, Scout, Scribe, Sent, Mut, Conn — including `R52CritDecl.md` and `R52CritMistakes.md`),
58 distinct files, each present exactly once. Sub-conventions on the same tree, for
reconciliation: the 18-seat GR cohort glob `R52(Crit|Rev)GR[^/]*\.md$` counts 17 committed —
the 16 bound reports plus the extra `R52CritGR2Host.md`, with `R52CritGR1b.md` and
`R52CritGR3b.md` absent — exactly the two "no report" unbound seats behind `seats_ok 16` in
`.ufo/waves/round-52/after/c1-final.json` (predicate binds `seats_ok == 18`). The
load-bearing values in the r55 declaration (`seats_ok 16`, verdict FAIL, verdicts_ok 1) are
read from that JSON and are exact; only the seat-file figure needed its command named.

## Round 56 — declaration (2026-11-01, base `62b47771…`, written before any measurement)

Context: r55 admitted (non-author verifier spot-check committed at this base, `62b47771`).
Its closure routed four carry-ins; they land first as repairs R1-R4, not claims (r33/r34
precedent): **R1** the r52 seat-file counting command (block above); **R2** the r55 lesson
Gate's explicit zero-rejections line (append-only); **R3** scratch hygiene — the r55 dir was
re-inspected this round: empty at the spot-check's observation, but the closure session
itself wrote `closure.json` there at 06:19Z, after observing it; disposition recorded in the
round report and LOG (this round's own scratch `scratch/tsukuroi-r56` is deleted before
finish); **R4** the W04 watch count noted: **42 at round start**, stable against the r55 end
count (receipt `.ufo/waves/round-56/before/sources-census-start.txt`).

FRESH-START (prompt §7 names r50/r51/r52): the three `rejected-honest-stop` closures
re-spot-checked against committed bytes this round — r50
`.ufo/waves/round-50/after/c1-final.json` reads `verdict FAIL, verdicts_ok 0, marks_ok 0,
seats_ok 18`; r51 `.ufo/waves/round-51/before/c2-cheats-at-amend1.json` does not exist at
`c0ad548a` (`git cat-file -e` rc 128); r52 `.ufo/waves/round-52/after/c1-final.json` reads
`verdict FAIL, verdicts_ok 1, seats_ok 16` (predicate binds `== 18`; unbound
`R52CritGR1b`/`R52CritGR3b`). The declared round rules out:

- **The counted-cohort depth resume** (r50/r51/r52's common binding: amend GR2/GR3, fresh
  18-seat cohort through check-scrub-admission-r5x) — still unreachable: no wave/AgentSwarm
  dispatch surface on this host; L0 `tsukuroi | round-53` stands unanswered, routed around,
  never treated as answered. A do-nothing control cannot reach the claim, but neither can
  this round; asserting `seats_ok` would fabricate.
- **Re-claiming admitted r53/r54/r55 moves** (win-host-census live runs, T1-T8, T9-T12, the
  D1-D12 drift recheck, the uniqueness gate, the reissued receipts): landed, verified, and a
  do-nothing control already reaches them — no fresh axis-move.
- **r53-planned RP1/RP2 post-state verification arms**: the operator-gated PATH/alias repairs
  remain unexecuted; post-state arms could only re-report today's DEGRADED state.
- **Sourcing D12's fnm second-session behavior**: requires a second concurrent session; this
  round is single and inline. Cannot be measured honestly here.
- **A bare re-run of `recheck-drift-r54.sh` or a re-fetch of S261/S262 as THE freshness
  move**: a do-nothing control reaches a pure re-run. (C2 below is not a re-run: the
  executable T1-T12 pass does not exist at base; C1's 420 s D7 leg is a new parameterized
  mode with its own raw receipt, not a repeat of the r54 run.)

Assimilation: `considerthese/` mined (latest 2026-10-26): the five self-improvement ideas are
aggregator/wave-class or Linux-host-class on this host, and the cross-note correction
propagation map was partially applied in r54; none clears this round's bar; nothing adopted.
The shokuknow register is not reachable from this host. L2 floor (MISSION ≥8 in one batched
AgentSwarm call): absent surface, routed around (standing L0 `tsukuroi | round-53`); the
round-1 kaidoku/revenger scope L0 likewise stands, routed around. Lowest-axis duty: depth and
adjacency tied lowest at 8 — **C3 works depth**. Saturation 9 / window 3; no capability entry
is claimed this round, so the stagnation nudge is not invoked. Ordinals at base: depth 8,
coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; none retired.

| Claim | Axis | Surface moved | Counting command | Do-nothing control at base | Target (predicate) |
|---|---|---|---|---|---|
| C1 | operability | The r55 planned instrument surfaces land: `win-host-census-r53.py --receipt <path> [--budget <s>]` — the live census re-run routed THROUGH the receipt-run instrument by import (`run_command`/`build_receipt` reused, not duplicated), so the census writes its own receipt-run-format receipt (argv, budget, start/end UTC, duration, `rc=`, stream sizes, verbatim streams) — and `recheck-drift-r54.sh --budget <s>` — the D7 leg takes its wall-clock budget as a parameter (default 90 preserves today's behavior; the register's 420 s class runs without editing the script). Registry rows updated for both. | before at base: `git show 62b47771:tools/win-host-census-r53.py \| grep -c -- "--receipt"` → **0**; `git show 62b47771:tools/recheck-drift-r54.sh \| grep -c -- "--budget"` → **0** (both verified this declaration). after: each ≥ 1; `python tools/win-host-census-r53.py --receipt <path>` exits with the census rc and the receipt carries `receipt_run=1` + `command=` + `rc=`; `bash tools/recheck-drift-r54.sh --budget 420 --receipt <path>` runs the D7 leg at 420 s | at base no receipt mode and no budget parameter exist; nothing on this host produces a census self-receipt or a parameterized D7 leg | census selftest extended (≥ 24 cases, 0 failed) AND both modes run on THIS host producing receipt-run-format receipts AND the 420 s D7 leg reads `D7 match` (rc 124 partial class) with its raw receipt committed AND `check-registry-coverage` reads 0 findings |
| C2 | freshness | `tools/recheck-services-r56.sh` — the 30d recheck duty that today lives only as prose (`recheck:` lines of both services-plane notes) becomes ONE executable read-only pass over rows T1-T8 (r54 plane) + T9-T12 (r55 plane): per-row `T<k> match\|drift` lines re-running each row's probe and comparing the row's INVARIANT signature (error line, rc family, field presence); drift-class values (task/service counts, STATE/PID) are recorded as evidence, never judged; T7 runs inside a deleted temp cwd (the stray-file probe); `--receipt <path>` writes a lane-tree receipt; rollup `RECHECK_SERVICES: PASS (12 rows, M match, 0 drift)`. Registry row `recheck-services-r56`. | before: `git cat-file -e 62b47771:tools/recheck-services-r56.sh` → rc **128** (verified this declaration); the duty exists only as prose. after: the script runs 12 rows + rollup; receipt committed | at base nothing executable re-verifies T1-T12; prose cannot run | 12 rows judged AND 0 drift (any drift = honest FAIL rc 1 + an appended correction owed, reported as such) AND the receipt carries the full output AND registry-coverage 0 findings |
| C3 | depth (lowest tied, 8; SOURCED — S266 S267 opened this round after this declaration) | `corpus/knowledge/windows-services-config-plane-r56.md` — the service-control CONFIGURATION-CHANGE and FAILURE-ACTION surfaces (`sc config`, `sc failure`/`sc qfailure`), rows T13+, each citing an S-row opened this round or a dated receipt under `.ufo/waves/round-56/services-probes/`; every state-changing form is documented as operator-owned and never executed — the probes are the absence-refused forms (nonexistent service → the 1060 family: mutation refused by absence) and the pure query forms. Header duty `python tools/check-knowledge-header.py --revision <work>`. | before: `git cat-file -e 62b47771:corpus/knowledge/windows-services-config-plane-r56.md` → rc **128** (verified); SOURCES rows **265** (`grep -cE '^\| S[0-9]{3,} \|' corpus/SOURCES.md` spacing-tolerant → 265). after: `grep -c "^| T" <file>` ≥ 3; header gate 0 findings; SOURCES rows ≥ 267 | at base the file, the rows and the S-rows do not exist | rows ≥ 3 AND every row cites S266/S267 or a dated receipt AND knowledge-header gate 0 findings AND depth ordinal unchanged (8) — the move is the sourced entry, not the ordinal |

Causal separability: C1 touches only its two tools + their registry rows + its own receipts
under `.ufo/waves/round-56/receipts/`; C2 adds its own script + its own receipt (it READS the
two knowledge notes, modifies nothing); C3 adds its own knowledge note + SOURCES rows + its
own probe receipts under `.ufo/waves/round-56/services-probes/` (probes C1/C2 never issue).
No claim's counter reads another claim's surface. All three are single-session inline; the
counted-cohort resume stays operator-gated. Frontier step: S266 (`sc config`), S267
(`sc failure`) — Microsoft Learn pages opened this round, after this declaration; C3 is the
sourced claim. Round-start census: exit 0, 42 W04 (all duplicate-URL, warning-class; no
E-code), receipt `.ufo/waves/round-56/before/sources-census-start.txt`.

## Round 56 — measured outcome (2026-11-01, author-side; non-author closure pending)

Declaration `ebaf9856`; work `a4d88715`. All measurements run on THIS host at the work tip
`a4d88715` (counting battery `.ufo/waves/round-56/after/c1-c2-c3-counts-at-work.txt`;
before-counts at base `.ufo/waves/round-56/before/c1-c2-c3-at-base.txt`, plumbing reads of
`62b47771` — the worktree/index views on this host are unreliable, see lesson R56-STALE-DRAFT).

| Claim | Counting command → measured | Verdict | Axis effect |
|---|---|---|---|
| C1 operability | before: `git show 62b47771:tools/win-host-census-r53.py \| grep -c -- "--receipt"` → **0**; `…recheck-drift-r54.sh \| grep -c -- "--budget"` → **0**; the base census rejects all argv (rc 2); the base recheck has no arg validation — `--budget` silently swallowed (corrected note in the before-receipt). After: `--receipt` grep → **7**, `--budget` grep → **5**; `python tools/win-host-census-r53.py --selftest` → `WIN_CENSUS_SELFTEST: PASS (25 cases, 25 passed, 0 failed)`; receipt-mode live run `--receipt .ufo/waves/round-56/receipts/win-census-receipt-mode.txt --budget 120` → census rc **1** (the host's standing DEGRADED reading) with the receipt carrying `receipt_run=1`, full argv, `budget_s=120`, `rc=1`, `stdout_bytes=330`, verbatim planes; D7 420 s leg: `bash tools/recheck-drift-r54.sh --budget 420 --receipt …d7-budget420-summary.txt` → recheck rc **0**, 10 match + 2 doc rows, **0 drift**, `D7 match (timeout rc 124, partial: 18 PASS / 0 FAIL / no summary line; budget 420s…)`; the whole leg routed through receipt-run (`.ufo/waves/round-56/receipts/d7-budget420-raw.txt`: `budget_s=480`, `duration_s=423.7`, `rc=0`); receipt-run selftest 7/7 unchanged. Landing the flag surfaced the host find: the on-disk r54 draft had lost the committed `> "$receipt"` write line — restored with an exit-2 write-failure path (lesson R56-STALE-DRAFT; the committed tree was right). | **PASS measured** | operability unchanged (9, saturated) — the receipt capability's third working use; both r55 planned instrument surfaces landed |
| C2 freshness | before: `git cat-file -e 62b47771:tools/recheck-services-r56.sh` → rc **128**; the duty existed only as the two notes' prose `recheck:` lines. After: first run `bash tools/recheck-services-r56.sh --receipt .ufo/waves/round-56/receipts/recheck-services-t1t12.txt` → rc **0**, `RECHECK_SERVICES: PASS (12 rows, 12 match, 0 drift)`; receipt header `rows=12 matched=12 drift=0`; T2 246 rows (r54's value, stable), T4 active-only **111** vs 273 total (r54: 110 — the documented count-drift class, recorded as evidence, never judged), T9 wuauserv `4 RUNNING`, T11 `START_TYPE 3 DEMAND_START` (value drift-class); every invariant signature held (T1 mangled-option rc 1, T5/T10/T12 the 1060/rc-36 family with qc's own function line, T6 the S262 divergence persists, T7 the stray-file class re-created in a deleted temp cwd, T8 the Enum-overflow negative) | **PASS measured** | freshness unchanged (9, saturated) — the 30d discipline became executable; positively exercised at 0 drift |
| C3 depth (lowest tied, 8; SOURCED S266 S267, opened this round) | before: `git cat-file -e 62b47771:corpus/knowledge/windows-services-config-plane-r56.md` → rc **128**; SOURCES rows **265**. After: `grep -c "^| T" corpus/knowledge/windows-services-config-plane-r56.md` → **4** (T13-T16); knowledge-header gate at the work revision → PASS, **72** notes, **0** findings; SOURCES rows **267** (S266, S267), 0 malformed; every row cites S266/S267 or a dated receipt under `.ufo/waves/round-56/services-probes/`. Measured signatures: the config/failure USAGE GATE (name but no options → usage block, rc **103** — option-validation precedes OpenService; the usage text confirms S266's start= domain and adds type= `userown\|usershare` the page omits); absence-refused changes (`sc config <nonexistent> start= demand`, `sc failure <nonexistent> reset= 30 actions= restart/5000` → `[SC] OpenService FAILED 1060:` + rc **36** — the surface probed with zero mutation risk); the failure QUERY is spelled `qfailure` (wuauserv: RESET_PERIOD 86400, FAILURE_ACTIONS `RESTART -- Delay = 60000 milliseconds.` — the host's own recovery config) while bare `sc failure <svc>` does NOT query on this build (usage rc 103) | **PASS measured** | depth unchanged (8) — the move is the sourced entry, not the ordinal |

Repairs landed (routed carry-ins of the r55 closure, not claims): **R1** the r52 "58 seat files"
counting command — SCORECARD correction block (58 = `git ls-tree -r --name-only HEAD --
.ufo/waves/round-52 \| grep -cE "R52[A-Za-z0-9]*\.md$"`, all role classes; the GR-cohort
sub-convention counts 17 committed, matching `seats_ok 16` + 2 unbound + the Host seat); **R2**
the r55 lesson Gate's explicit zero-rejections line (append-only); **R3** scratch hygiene —
disposition in the round report and LOG (the r55 dir held the closure's own `closure.json`
written after the spot-check's observation; this round's scratch deleted before finish);
**R4** W04 watch: **42 at round start and end**, no growth (the two new rows carry fresh URLs).

Gates at the work tip `a4d88715`: registry-coverage PASS **94 tools / 94 rows / 0 findings**
(`recheck-services-r56` registered); knowledge-header PASS **72 notes / 0 findings**; SCORECARD
uniqueness on the committed blob ok rc 0; receipt-run selftest 7/7; census **exit 0 both passes,
42 W04, no E-code** (receipts `.ufo/waves/round-56/before/sources-census-start.txt`,
`.ufo/waves/round-56/after/sources-census-end.txt`).

Named limits: the receipt-mode census run records TODAY's host state (DEGRADED rc 1 is the
plane's standing reading, not a regression); D7's partial-PASS count (18) is a wall-clock fact
and varies; T13's rc-103 usage gate and T16's qfailure-only query behavior are THIS build's
measurements (Windows 10.0.26200 x64) — the archived S267 page documents set-only syntax and the
tool agrees; the config-surface `type= interact` error sentence (S266, the S262 family) is
UNTESTED here because testing it is a mutation (operator-owned); `check-self-assessment.py`
remains could-not-evaluate on this host (K13, named limit); L2 floor absent surface, routed
around (L0 `tsukuroi | round-53`); the round-1 kaidoku/revenger scope L0 likewise stands, routed
around. Mistakes mined: R56-STALE-DRAFT-REVERT, R56-RECEIPT-FLAG-UNEXERCISED,
R56-UGREP-LEADINGSLASH, R56-USAGE-GATE-ASSUMED-ABSENCE, R56-COPY-RUNS-OUT-OF-TREE
(corpus/lessons/round-56.md).

## Axes — current self-assessment (round 56 final measured surface)

Restated 2026-11-01 at the round-56 final tree `a4d88715`; ordinals unchanged (all three claims
are measured moves on saturated or lowest axes; the depth move is the sourced entry, not a
number). Counts re-derived with each cell's command at this tree.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 72 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); `SKILL.md` 4709 `wc -l`; `corpus/lessons/` 87 files (`find corpus/lessons -type f \| wc -l`); the sourced services config/failure plane T13-T16 landed round 56 (round-56 measured outcome; S266 current + S267 archive); GR1-GR3 of the scrub entry remain pending behind the operator-gated cohort resume; no ordinal move. | round 4; round-56 entry added, ordinal unchanged |
| coverage | 9 | `corpus/README.md` 522 `wc -l`, byte-identical to base (the r56 plane extends the r54/r55 services surface inside the same province record; no map row added or re-homed); PROVINCE Core, Frontier and Adjacent sections present. | round 11; unchanged |
| operability | 9 | `python tools/win-host-census-r53.py --selftest` PASS (25/25, receipt mode included); `python tools/receipt-run.py --selftest` PASS (7/7); `bash -n` rc 0 on both recheck scripts; census receipt-mode receipt + D7-420 s receipts committed (`.ufo/waves/round-56/receipts/`); registry-coverage 94/94 at `a4d88715`; live census DEGRADED rc 1 (standing reading). | round 11; round-56 receipt/budget modes added, ordinal unchanged |
| freshness | 9 | services plane T1-T12 re-verified by one committed command, 0 drift (`.ufo/waves/round-56/receipts/recheck-services-t1t12.txt`); drift register D1-D12 re-verified at the 420 s class, 0 drift; S266/S267 opened live this round; sources census exit 0 at round start and end (42 W04 both, `.ufo/waves/round-56/{before,after}/sources-census-*.txt`). | fleet round 1; round-56 executable recheck pass added, ordinal unchanged |
| calibration | 9 | the axes table above restated to counts recomputed on this host; SCORECARD uniqueness gate ok on the committed blob; all three claims measured with before-receipts at base via plumbing (the worktree view is untrusted this round — lesson R56-STALE-DRAFT); `python tools/check-self-assessment.py` cannot evaluate here (K13, named limit). | round 10; round-56 base-plumbing before-receipts added, ordinal unchanged |
| adjacency | 8 | formal overlap table present; no sibling scope touched; the config/failure surface stays inside the lane's own host-operability province (no sibling absorbed); contested kaidoku/revenger ownership remains unruled (carried, routed around). | fleet round 1; unchanged |

- **planned (next round):** operator-gated first — the L0 wave-dispatch question (`tsukuroi |
  round-53`) still decides the r52 counted-cohort depth resume; if the lane stays on this host:
  give `recheck-services-r56.sh` a per-row raw-receipt mode (route each T-probe through
  `receipt-run.py` so a drift leg ships its own verbatim capture, not only the summary receipt),
  record the recheck cadence dates (r56 = day 0; next services-plane pass due 2026-11-30) in the
  two notes' `recheck:` headers as dated entries, and — if the operator authorizes — exercise the
  config surface's `type= interact` sentence (S266) with a real operator-owned config change as
  the falsification probe the lane cannot run read-only.
- **retired:** none.

## Round 57 — declaration (2026-11-01, base `a36bfaaf…`, written before any measurement)

Context: r56 admitted (non-author verifier spot-check committed at `b1ca23a0`). Its closure routed
one item, landed FIRST as this round's plumbing carry-in (not a claim; r33/r34 precedent): the 14
round-56 receipt files under `.ufo/waves/round-56/{after,receipts,services-probes}/` cited as
committed by `ebaf9856`/`a4d88715`/`ed26680d` but never plumbed (closure defect
R56-RECEIPTS-UNCOMMITTED) — landed as **`a36bfaaf`** (14 files, 312 insertions; contents verified
against every reported value before landing: T1-T12 12/12 drift 0, D7 420 s rc-124 partial 18
PASS/0 FAIL, selftest 25/25, receipt-run 7/7, gates 94/94/0 + 72/0, census 42 W04 exit 0 both
passes, sources 267 rows 0 malformed). This round's base IS that landing; the defect is mined as
R57-CITED-UNCOMMITTED in the round lesson.

FRESH-START (prompt §7 names r50/r51/r52): the three `rejected-honest-stop` closures re-spot-checked
against committed bytes at this base — r50 `.ufo/waves/round-50/after/c1-final.json` reads
`"verdict": "FAIL", "verdicts_ok": 0, "marks_ok": 0` with `seats_ok 18`; r51
`.ufo/waves/round-51/before/c2-cheats-at-amend1.json` is absent at `c0ad548a` (`git cat-file -e`
rc 128); r52 `.ufo/waves/round-52/after/c1-final.json` reads `"verdict": "FAIL", "verdicts_ok": 1,
"seats_ok": 16`, predicate binds `seats_ok == 18`, seat_notes name exactly the two unbound
`R52CritGR1b`/`R52CritGR3b` seats. The declared round rules out:

- **The counted-cohort depth resume** (r50/r51/r52's common binding) — still unreachable: no
  wave/AgentSwarm dispatch surface on this host; L0 `tsukuroi | round-53` stands unanswered, routed
  around, never treated as answered. A do-nothing control cannot reach the claim, but neither can
  this round; asserting `seats_ok` would fabricate.
- **Re-claiming admitted r53-r56 moves** (live census runs, receipt mode, budget mode, T1-T16
  rechecks, the D1-D12 drift pass, the uniqueness gate): landed and verified; a do-nothing control
  already reaches a pure re-run — no fresh axis-move.
- **The operator-gated `type= interact` falsification probe** (S266's documented config-error
  sentence): a real config change is operator-owned; this round appended the L0 request
  (`tsukuroi | round-57`) and routes around it — never executed read-only.
- **Sourcing D12's fnm second-session behavior**: requires a second concurrent session; this round
  is single and inline. Cannot be measured honestly here.
- **A bare re-run of `recheck-services-r56.sh` or `recheck-drift-r54.sh` as THE freshness move**: a
  do-nothing control reaches a pure re-run. (C2 below is not a re-run — the per-row raw-receipt
  mode does not exist at base; C3 is not a re-run — no dated cadence contract exists at base.)

Assimilation: `considerthese/` mined (latest 2026-10-26; seven notes): the self-improvement ideas
remain aggregator/wave-class or Linux-host-class on this host, and the cross-note correction
propagation map was partially applied in r54 — none clears this round's bar; nothing adopted. The
shokuknow register is not reachable from this host. L2 floor (MISSION ≥8 in one batched AgentSwarm
call): absent surface, routed around (standing L0 `tsukuroi | round-53`; the round-1
kaidoku/revenger scope L0 likewise stands). Lowest-axis duty: depth and adjacency tied lowest at 8
— **C1 works depth** (sourced SDDL/metadata plane; the lane's own host province, no sibling scope).
Saturation 9 / window 3; the stagnation nudge is not invoked. Ordinals at base: depth 8, coverage
9, operability 9, freshness 9, calibration 9, adjacency 8; none retired.

| Claim | Axis | Surface moved | Counting command | Do-nothing control at base | Target (predicate) |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S268 S269 to be opened this round AFTER this declaration) | `corpus/knowledge/windows-services-sddl-plane-r57.md` — the service SECURITY-DESCRIPTOR and METADATA-query surface the three prior services notes never touch: `sc sdshow` (the SDDL string — ACE/right/SID grammar), `sc qsidtype`, `sc qdesc`, `sc qtriggerinfo`, `sc enumdepend`, rows T19+, each citing an S-row opened this round or a dated receipt under `.ufo/waves/round-57/services-probes/` (every probe through receipt-run); `sc sdset` documented operator-owned, never executed — only the query forms and the absence-refused nonexistent-service forms run. Header duty `python tools/check-knowledge-header.py --revision <work>`. | before at base (all verified this declaration, receipt `.ufo/waves/round-57/before/c1-c2-c3-at-base.txt`): `git cat-file -e a36bfaaf:corpus/knowledge/windows-services-sddl-plane-r57.md` → rc **128**; SOURCES rows **267**; the negative sweep `git show a36bfaaf:corpus/knowledge/<each of the 3 services notes> \| grep -cE "sdshow\|qsidtype\|qtriggerinfo"` → **0 + 0 + 0**. after: `grep -c "^| T" <note>` ≥ 3; SOURCES rows ≥ 269, 0 malformed; knowledge-header gate 0 findings at the work revision | at base the note, the rows and the S-rows do not exist; no existing note mentions the surface (sweep above) | rows ≥ 3 AND every row cites an opened S-row or a dated receipt AND knowledge-header gate 0 findings AND SOURCES ≥ 269 rows 0 malformed AND depth ordinal unchanged (8) — the move is the sourced entry, not the ordinal |
| C2 | operability | `tools/receipt-write.py` — receipt-run-FORMAT receipts for ALREADY-CAPTURED output: imports `build_receipt` from `receipt-run.py` (one format implementation, never duplicated — the r56 C1 import rule), so any bash-side probe whose exec environment must NOT change can ship verbatim raw receipts; with `--selftest`. Plus `recheck-services-r56.sh --raw-dir <dir>`: each of the 12 legs additionally writes `<dir>/t<k>-raw.txt` through receipt-write (command= the exact probe command text, rc= the leg's own rc, streams verbatim); the judgment logic and the probes' exec environment are UNCHANGED — routing the probes through a python-subprocess runner would change T1's MSYS-mangling signature class (the runner, not bash, would exec the child), so the capture rides alongside, not instead. Registry: `receipt-write-r57` row added; `recheck-services-r56` row annotated in place. | before at base (verified): `git show a36bfaaf:tools/recheck-services-r56.sh \| grep -c -- "--raw-dir"` → **0**; `git cat-file -e a36bfaaf:tools/receipt-write.py` → rc **128**; receipt-run selftest cases at base **7**. after: each grep ≥ 1; one live pass `bash tools/recheck-services-r56.sh --receipt <r> --raw-dir <dir>` → rc 0, `RECHECK_SERVICES: PASS (12 rows, 12 match, 0 drift)`, and `<dir>` holds 12 raw receipts each carrying `receipt_run=1` + `command=` + `rc=`; `python tools/receipt-write.py --selftest` PASS; `python tools/receipt-run.py --selftest` still 7/7; registry-coverage 0 findings | at base no raw-receipt mode and no write-tool exist; the 30d pass ships only its summary receipt | the live pass is 12/12 0 drift AND 12 raw receipts exist with the three key lines each AND receipt-write selftest PASS AND receipt-run selftest 7/7 unchanged AND registry-coverage 0 findings |
| C3 | freshness | Dated cadence contract for the services-plane recheck duty: the THREE services notes (r54 T1-T8, r55 T9-T12, r56 T13-T16) each gain an appended operative `recheck:` line (the header gate reads the LAST `recheck:` line at column 0; the old lines stay — append-only header convention, journal-boot-plane precedent) binding the 30d cadence to day 0 = **2026-11-01** (the committed r56 first-pass receipt `.ufo/waves/round-56/receipts/recheck-services-t1t12.txt`, 07:04:06Z) with the next pass **due 2026-11-30** — lateness becomes observable from committed bytes, which a cadence-only header cannot show. | before at base (verified): `git show a36bfaaf:corpus/knowledge/<note> \| grep -c "next pass due 2026-11-30"` → **0 + 0 + 0** (the three notes). after: each ≥ 1 (total 3); knowledge-header gate 0 findings (each operative `recheck:` still carries cadence + ISO date); old header lines byte-unchanged | at base no note names a due date; nothing on the host can observe recheck lateness from committed bytes | 3 notes carry the dated line AND the knowledge-header gate reads 0 findings AND the r54/r55/r56 original `recheck:` lines remain byte-identical (append-only) |

Causal separability: C1 touches only its new note + SOURCES rows S268/S269 + its probe receipts
under `.ufo/waves/round-57/services-probes/` + a SKILL round-57 section; C2 touches only its new
tool + the recheck script's arg surface + the registry rows + its own run receipts under
`.ufo/waves/round-57/receipts/`; C3 touches only the three notes' `recheck:` header lines. No
claim's counter reads another claim's surface (C2's live pass judges T1-T12 exactly as at base;
C1's note does not modify the recheck script; C3's headers are inert prose for C1/C2). All three
are single-session inline; the counted-cohort resume stays operator-gated. Frontier step: S268
(`sc sdshow`), S269 (SDDL service-object rights) — Microsoft Learn pages to be opened this round,
after this declaration; C1 is the sourced claim. Round-start census: exit 0, 42 W04 (all
duplicate-URL warning class; no E-code), receipt
`.ufo/waves/round-57/before/sources-census-start.txt`.

## Round 57 — measured outcome (2026-11-01, author-side; non-author closure pending)

Declaration `0555a010`; work `19f6b5c8`. All measurements run on THIS host at the work tip
`19f6b5c8` (counting battery `.ufo/waves/round-57/after/c1-c2-c3-counts-at-work.txt`; before-counts
at base `.ufo/waves/round-57/before/c1-c2-c3-at-base.txt`, plumbing reads of `a36bfaaf` — the
worktree/index views on this host are unreliable, lesson R56-STALE-DRAFT).

| Claim | Counting command → measured | Verdict | Axis effect |
|---|---|---|---|
| C1 depth (lowest tied, 8; SOURCED S268-S270, rejection S271, opened after the declaration) | before: `git cat-file -e a36bfaaf:corpus/knowledge/windows-services-sddl-plane-r57.md` → rc **128**; SOURCES rows **267**; negative sweep (sdshow/qsidtype/qtriggerinfo across the 3 prior services notes) → **0+0+0**. After: `grep -c "^| T" corpus/knowledge/windows-services-sddl-plane-r57.md` → **6** (T19-T24); SOURCES rows 267 → **271**, malformed **0** (awk NF!=13); knowledge-header gate at the work revision → PASS, **73** notes, **0** findings. Measured signatures (receipts t19-t28, all through receipt-run): sdshow wuauserv rc 0, `D:`-only 3-ACE SDDL (AU/BA/SY; S269 omitted-components anchor); sdshow nonexistent rc 36 `[SC] OpenService FAILED 1060:`; qsidtype rc 0 `SERVICE_SID_TYPE: UNRESTRICTED`; `qdesc` rc 103 usage gate vs `qdescription` rc 0 (the T13 spelling class); qtriggerinfo rc 0 two GROUP POLICY start triggers; enumdepend rc 0 `entriesread = 0`; sdset nonexistent rc 5 `[SC] OpenSCManager FAILED 5:` Access denied (privilege gate BEFORE service resolution — the assumed 1060 refusal does not fire; mined as R57-SDSET-ASSUMED-ABSENCE); ConvertFrom-SddlString rc 0 confirming the 3-ACE structure with filesystem-vocabulary bit names. Measured-vs-doc: ACE sets cross-checked against S270's default-grants table (BA/SY full Administrators class; AU read/interrogate + a start right; no interactive/service ACEs) — recorded as evidence, provenance [unknown]; the letter mapping stays Sddl.h-anchored [inference] (S271 records the DS-letters name-collision trap) | **PASS measured** | depth unchanged (8) — the move is the sourced entry, not the ordinal |
| C2 operability | before: `git show a36bfaaf:tools/recheck-services-r56.sh \| grep -c -- "--raw-dir"` → **0**; `git cat-file -e a36bfaaf:tools/receipt-write.py` → rc **128**; receipt-run selftest cases at base 7. After: `--raw-dir` grep → **4**; `python tools/receipt-write.py --selftest` → `RECEIPT_WRITE_SELFTEST: PASS (5 cases, 5 passed, 0 failed)` (first run 1/5 — two real defects fixed before landing, kept on record as R57-SELFTEST-WRITTEN-THEN-PASSED); receipt-run selftest still `PASS (7 cases, 7 passed, 0 failed)`; one live pass `bash tools/recheck-services-r56.sh --receipt .ufo/waves/round-57/receipts/recheck-services-raw-summary.txt --raw-dir .ufo/waves/round-57/receipts/raw-t1t12` → rc **0**, `RECHECK_SERVICES: PASS (12 rows, 12 match, 0 drift)`, and the dir holds **12** raw receipts, all 12 carrying `receipt_run=1` + `command=` + `rc=` (rc spread 7×0 / 2×1 / 3×36; this window: active 110, wuauserv STOPPED, START_TYPE DEMAND_START — drift-class, recorded not judged); registry-coverage PASS **95 tools / 95 rows / 0 findings** (`receipt-write-r57` registered, `recheck-services-r56` annotated) | **PASS measured** | operability unchanged (9, saturated) — the write-side receipt capability (capture-and-judge counterpart of receipt-run); the per-row raw-receipt mode landed |
| C3 freshness | before: `git show a36bfaaf:corpus/knowledge/<note> \| grep -c "next pass due 2026-11-30"` → **0 + 0 + 0** (r54/r55/r56 notes). After: each **≥ 1** (counted together with the new r57 note: **4** notes carry the dated line); each note now has exactly 2 `recheck:` lines (old kept byte-identical, new operative last — header gate reads 73/0); the operative lines bind day 0 = 2026-11-01 (the committed r56 first-pass receipt) to next pass due **2026-11-30** | **PASS measured** | freshness unchanged (9, saturated) — the 30d duty became time-falsifiable from committed bytes |

Repairs landed (routed carry-ins, not claims): the r56 closure's R56-RECEIPTS-UNCOMMITTED — the 14
receipt files landed as `a36bfaaf` BEFORE the declaration (this round's base); mined as
R57-CITED-UNCOMMITTED (class `landing`) in the round lesson. New L0 line appended:
`tsukuroi | round-57` (operator authorization requested for the S266 `type= interact`
falsification probe; routed around, never treated as answered).

Gates at the work tip `19f6b5c8`: knowledge-header PASS **73 / 0**; registry-coverage PASS **95/95/0**;
SCORECARD uniqueness on the committed blob ok rc 0; receipt-write selftest 5/5; receipt-run selftest
7/7; census **exit 0 both passes, 42 W04, no E-code** (receipts
`.ufo/waves/round-57/before/sources-census-start.txt`, `.ufo/waves/round-57/after/sources-census-end.txt`).

Named limits: all descriptor/count values are captures of 2026-11-01 (drift-class); the SDDL
letter→SERVICE_* mapping is [inference] anchored to Sddl.h and cross-checked against S270's
default-grants table only (no Learn page documents it; the host decoder names bits in filesystem
vocabulary — measured, t27); T24's rc-5 SCM gate is THIS session's token — an elevated session
would pass the gate, and the change still stays operator-owned; `<showrights>` unexercised (no
diagnosis value named); `check-self-assessment.py` remains could-not-evaluate on this host (K13);
L2 floor absent surface, routed around (L0 `tsukuroi | round-53`); the round-1 kaidoku/revenger
scope L0 likewise stands. Mistakes mined: R57-CITED-UNCOMMITTED, R57-SDSET-ASSUMED-ABSENCE,
R57-SELFTEST-WRITTEN-THEN-PASSED, R57-UGREP-XARGS-ARGS (corpus/lessons/round-57.md).

## Axes — current self-assessment (round 57 final measured surface)

Restated 2026-11-01 at the round-57 final tree `19f6b5c8`; ordinals unchanged (the depth move is
the sourced entry, not a number; operability/freshness are saturated). Counts re-derived with each
cell's command at this tree.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 73 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); `SKILL.md` 4742 `wc -l`; `corpus/lessons/` 89 files (`find corpus/lessons -type f \| wc -l`); the sourced services SDDL/metadata plane T19-T24 landed round 57 (round-57 measured outcome; S268 archive + S269/S270 current; S271 rejection records the letter-collision trap); GR1-GR3 of the scrub entry remain pending behind the operator-gated cohort resume; no ordinal move. | round 4; round-57 entry added, ordinal unchanged |
| coverage | 9 | `corpus/README.md` 522 `wc -l`, byte-identical to base (the r57 plane extends the r54/r55/r56 services surface inside the same province record; no map row added or re-homed); PROVINCE Core, Frontier and Adjacent sections present. | round 11; unchanged |
| operability | 9 | `python tools/receipt-write.py --selftest` PASS (5/5); `python tools/receipt-run.py --selftest` PASS (7/7); `bash -n` rc 0 on the extended recheck script; 12 per-row raw receipts + summary receipt committed (`.ufo/waves/round-57/receipts/`); registry-coverage 95/95 at `19f6b5c8`; live census not re-run this round (no census-surface change; the r56 receipt-mode run stands as its first use). | round 11; round-57 write-side receipt capability added, ordinal unchanged |
| freshness | 9 | services plane T1-T12 re-verified again at the work tip, 0 drift, WITH per-row raw receipts (`.ufo/waves/round-57/receipts/raw-t1t12/`); the three services notes' `recheck:` duty now carries a dated due date (2026-11-30) observable from committed bytes; S268-S271 opened live this round; sources census exit 0 at round start and end (42 W04 both, `.ufo/waves/round-57/{before,after}/sources-census-*.txt`). | fleet round 1; round-57 dated cadence contract added, ordinal unchanged |
| calibration | 9 | the axes table above restated to counts recomputed on this host; SCORECARD uniqueness gate ok on the committed blob; all three claims measured with before-receipts at base via plumbing; the round's own new instrument failed its first selftest 1/5 and the FAIL is kept on record (R57-SELFTEST-WRITTEN-THEN-PASSED) with the fixed tool re-measured 5/5; `python tools/check-self-assessment.py` cannot evaluate here (K13, named limit). | round 10; round-57 honest-selftest-fail-on-record added, ordinal unchanged |
| adjacency | 8 | formal overlap table present; no sibling scope touched; the SDDL/metadata surface stays inside the lane's own host-operability province (no sibling absorbed); contested kaidoku/revenger ownership remains unruled (carried, routed around). | fleet round 1; unchanged |

- **planned (next round):** operator-gated first — the L0 wave-dispatch question (`tsukuroi |
  round-53`) still decides the r52 counted-cohort depth resume, and the new L0 `tsukuroi |
  round-57` decides the S266 `type= interact` falsification probe. If the lane stays on this
  host: extend `recheck-services-r56.sh` with rows T19-T24 so the SDDL/metadata plane joins the
  one-command recheck pass (the raw-receipt mode already exists for it), and record the FIRST
  cadence-dated pass receipt when the 2026-11-30 due date arrives (or before, if a drift fires).
- **retired:** none.

## Round 58 — declaration (2026-11-01, base `5a59f79e…`, written before any measurement)

Context: r57 admitted (non-author verifier spot-check committed at `5a59f79e`). Its closure routed four
status-neutral carry-ins, addressed this round BEFORE the claims: (1) the r57 in-place annotation of the
`recheck-services-r56` registry row — noted as a lesson correction (the convention for registry corrections is
the appended superseding table, the round-18/19/… mechanism; C2 applies that mechanism to the same row this
round); (2) the sed-deleted failure line self-named in `bde06613` — the restated lesson was verified this
round against committed bytes (the after-receipt carries only the replacement line; the lesson says exactly
that), and the rule (append the correction beside the preserved failure, never substitute) binds this round's
receipts; (3) the stale `local master = origin/master = 51199d52` header statement in the r57 report —
superseded minutes later by the same round's correction commit `bde06613` (fleet-repo report, lane cannot
mutate it; the correction block is recorded here and in the round-58 lesson and report); (4) standing L0s
`tsukuroi | round-53` (wave-dispatch surface, `.ufo/l0-questions.md:229`), the round-1 kaidoku/revenger scope
(PROVINCE Frontier), and `tsukuroi | round-57` (S266 interact authorization, `.ufo/l0-questions.md:247`) all
stand unanswered — routed around, never treated as answered.

FRESH-START (prompt §7 names r50/r51/r52): the three `rejected-honest-stop` closures re-spot-checked from
committed bytes at this base (receipt `.ufo/waves/round-58/before/freshstart-spotcheck.txt` + top-level JSON
fields re-parsed): r50 `.ufo/waves/round-50/after/c1-final.json` → `verdict FAIL, verdicts_ok 0, marks_ok 0,
seats_ok 18`; r51 `.ufo/waves/round-51/before/c2-cheats-at-amend1.json` → exists at base but is a **0-byte**
file (committed by `91227829` "round NOT complete: w2 not dispatched" — the battery was never populated),
consistent with the r51 closure's unmeasured verdict; r52 `.ufo/waves/round-52/after/c1-final.json` →
`verdict FAIL, verdicts_ok 1, marks_ok 0, seats_ok 16` (predicate bound 18). Ruled out this round (each for
cause, none reachable by a do-nothing control): (a) the counted-cohort depth resume — still gated on the
absent wave-dispatch surface (L0 round-53); (b) re-claiming any admitted r53-r57 move (live census,
receipt/budget modes, T1-T24) — an admitted move re-claimed is not a move; (c) a bare re-run of
`recheck-services-r56.sh` or `recheck-drift-r54.sh` as THE freshness move — the instruments exist; a re-run is
supporting evidence inside C3, never the move; (d) the `considerthese/` five self-improvement ideas —
aggregator/wave-class or Linux-host-class on this host (mined again this round; nothing adopted).

The r57 planned item (lane stays on this host) is C2 below. The services planes' 2026-11-30 cadence pass is
NOT due today and no drift fired; the census pass C3 runs is the W-plane's own day-0 anchor under its NEW
dated line, not the services-plane cadence pass.

| # | axis | claim | before → after | falsifier | verdict condition |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S272 S273 to be opened this round AFTER this declaration) | `corpus/knowledge/windows-eventlog-plane-r58.md` — the Windows EVENT-LOG triage plane, the current host's analog of the journal/boot plane this lane owns in Core (drift rows D2/D3 name the Linux journal ABSENT here; PROVINCE round-53 host-transition record). Rows E1-E6: channel inventory (`wevtutil el`), newest-first text query on System, the query-absence class on a nonexistent channel, `gli` channel metadata, the level-filtered `/q:` xpath error query (the `journalctl -p err` analog, Git Bash quoting class), and the absence class under `gli` compared with E3's query-leg signature. Every state-changing form (`wevtutil cl` clear-log, log config) is documented operator-owned and never executed. Probes through receipt-run into `.ufo/waves/round-58/eventlog-probes/`. Header duty `python tools/check-knowledge-header.py --revision <work>`. | before at base (verified this declaration, receipt `.ufo/waves/round-58/before/c1-c2-c3-at-base.txt`): `git cat-file -e 5a59f79e:corpus/knowledge/windows-eventlog-plane-r58.md` → rc **128**; negative sweep `git grep -l -i wevtutil <base> -- corpus SKILL.md PROVINCE.md tools` → **0 files** (rc 1); SOURCES rows **271**. after: `grep -c "^| E" <note>` ≥ 3; SOURCES rows ≥ 273, 0 malformed; knowledge-header gate 0 findings at the work revision | at base the note, the rows and the S-rows do not exist; no lane file mentions the surface (sweep above) | rows ≥ 3 AND every row cites an opened S-row or a dated receipt AND knowledge-header gate 0 findings AND SOURCES ≥ 273 rows 0 malformed AND depth ordinal unchanged (8) — the move is the sourced entry, not the ordinal |
| C2 | operability | `tools/recheck-services-r56.sh` extended to the FULL services surface in one command: rows T13-T16 (r56 config/failure plane) and T19-T24 (r57 SDDL plane) join the pass → **22 rows**. Class split per the notes' own operative lines: T19-T23 LIVE re-run (read-only/refusal class: sdshow, sdshow-absent, qsidtype, qdescription-vs-qdesc, qtriggerinfo/enumdepend); T13-T16 + T24 RECEIPT-COMPARED — their probes are config-change-shaped or SCM-write-shaped, so the instrument NEVER re-executes them; it verifies each committed dated receipt (`.ufo/waves/round-56/services-probes/t13-t18`, `.ufo/waves/round-57/services-probes/t27-input-sddl-line.txt` + `t28-…`) still carries the row's invariant signature, failing the row on receipt-missing or signature drift. Registry: the `recheck-services-r56` row is corrected by an APPENDED `## Gate and probe registry — round58 superseding current rows` table (round-46 rows carried verbatim, one row updated) — the r57 carry-in lesson's fix, applied to the same row r57 edited in place. | before at base (verified): `grep -oE 'T[0-9]+ match' tools/recheck-services-r56.sh \| sort -u \| wc -l` → **12**; script mentions T13/T19/receipt-compared → **0**; round-58 registry table → **0**. after: row count **22**; one live pass `bash tools/recheck-services-r56.sh --receipt <r> --raw-dir <dir>` → rc 0, `RECHECK_SERVICES: PASS (22 rows, 22 match, 0 drift)`; `bash -n` rc 0; registry-coverage gate 95 tools / 95 rows / 0 findings against the NEW highest table; the round-46 table byte-unchanged | at base no executable instrument re-verifies T13-T24; no superseding registry table exists | 22 rows judged AND 0 drift (any drift = honest FAIL rc 1 + an appended correction owed, reported as such) AND the receipt carries the full output AND registry-coverage 0 findings AND the round-46 table byte-identical |
| C3 | freshness | The W-plane note (`windows-host-plane-r53.md`) joins the dated cadence contract AND its STALE selftest expectation is corrected by append: the note's operative duty says "expect PASS, **20 cases**" while the instrument has reported **25 cases** since r56's receipt/budget modes (measured at this base: `WIN_CENSUS_SELFTEST: PASS (25 cases, 25 passed, 0 failed)` — note-vs-instrument drift). An operative `recheck:` line is appended (old line byte-unchanged, journal-boot-plane convention): day 0 = 2026-11-01 (the committed r56 receipt-mode receipt `.ufo/waves/round-56/receipts/win-census-receipt-mode.txt`), next pass due **2026-11-30**, operative expectation PASS with **25** cases. Plus the W-plane's first re-verification pass under the new line: fresh selftest 25/25 + a live receipt-mode census run, W-plane verdicts compared against the r56 receipt (drift-class values recorded, never judged). | before at base (verified): `grep -c "next pass due" corpus/knowledge/windows-host-plane-r53.md` → **0**; `grep -c "20 cases" <note>` → **1** (the stale line); instrument selftest → 25 cases. after: the dated line ≥ 1 naming 25 cases; the stale "20 cases" line byte-unchanged (append-only); fresh selftest PASS 25/25 rc 0; a live receipt-mode run committed under `.ufo/waves/round-58/receipts/` | at base no note names a W-plane due date; the note's expectation contradicts the instrument (drift unrecorded) | dated line present AND the old line byte-identical AND fresh selftest PASS 25/25 AND the live receipt committed AND the r56-vs-live verdict comparison recorded (any plane flip = honest record, not smoothed) |

Causal separability: C1 touches only its new note + SOURCES rows; C2 touches only the recheck script + the
appended SKILL registry section; C3 touches only the W-plane note header + fresh receipts. No claim's
verification depends on another having landed. No exploratory claim this round. The r57-ruled-out bare-rerun
class is respected: C3's census pass is the day-0 anchor of a NEW committed cadence line plus a
stale-expectation correction — the pass alone is not claimed.

## Round 58 — measured outcome (2026-11-01, author-side; non-author closure pending)

Measured at work revision `e4e33606` (counting battery `.ufo/waves/round-58/after/c1-c2-c3-counts-at-work.txt`;
before-counts at base `.ufo/waves/round-58/before/c1-c2-c3-at-base.txt`, plumbing reads of `5a59f79e` — the
worktree view is untrusted on this host, r56/r57 lesson). Gates at `e4e33606`: knowledge-header PASS 74/0,
registry-coverage PASS 95/95/0 (round-58 table selected), SCORECARD uniqueness ok rc 0, receipt-run 7/7,
receipt-write 5/5; census exit 0 both passes 42 W04 (intermediate E12 repaired — R58-SOURCES-APPEND-POSITION).

| Claim | Before → after (measured) | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (lowest tied, 8; SOURCED S272 S273 opened after the declaration) | before: `git cat-file -e 5a59f79e:…windows-eventlog-plane-r58.md` → rc **128**; wevtutil sweep **0 files**; SOURCES **271**. After: `grep -c "^| E"` → **6** (E1-E6); SOURCES 271 → **273**, malformed **0** (all inside Registry); knowledge-header gate at the work revision → PASS **74** notes / **0** findings. Measured signatures (receipts e1-e6b, all through receipt-run): `el` rc 0 (1162→1164, drift-class); `qe System /c:3 /rd:true /f:text` rc 0 newest-first Event[N] (S272's example shape); query-absence rc **15007**/159 (15007 mod 256, T5 class) `Failed to open event query.` + `The specified channel could not be found.`; `gli System` rc 0 (numberOfLogRecords/fileSize); level-filter `/q:*[System[(Level=1 or Level=2)]]` rc 0 newest errors; `gli`-absence same message + rc family, function line `Failed to read log status information`; MSYS rewrite `/c:3`→`c:3` rc 87 with the python-spawn boundary nuance (e2/e2b, e3/e3b); bare `cl` usage-refused rc 87 (no mutation possible) | **PASS measured** | depth unchanged (8) — the move is the sourced entry, not the ordinal |
| C2 operability | before: `grep -oE 'T[0-9]+ match' … \| sort -u \| wc -l` → **12** (base; the declared command's after-value is corrected below the table); T13/T19/receipt-compared mentions **0**; round-58 registry table **0**. After: script rows 17 literal + 5 rcr = **22** (combined command); live pass `RECHECK_SERVICES: PASS (22 rows, 22 match, 0 drift)` rc 0; FIRST RUN FAIL 2 drift kept on record (T19 grep-lines-vs-occurrences, T24 input-file-as-receipt — R58-RECHECK-EXTENSION-FIRST-RUN, FAIL receipt + raw captures committed under honest names); 17 raw receipts (live rows only); registry-coverage 95/95/0 against the appended round-58 table; round-46 table byte-identical (sha256 `e290c2b3…` base=work); `bash -n` rc 0 | **PASS measured** | operability unchanged (9, saturated) — the full services surface in one command; the registry-append convention applied to the row r57 edited in place |
| C3 freshness | before: W-plane `next pass due` → **0**; stale `20 cases` line → **1**; instrument selftest → **25** cases (the drift). After: dated operative line → **1** (day 0 = 2026-11-01, due 2026-11-30, expectation **25** cases); old line byte-identical (sha256 `364df0a1…` base=work); stale line still present (append-only); fresh selftest `PASS (25 cases, 25 passed, 0 failed)` rc 0; live receipt-mode census committed, stdout byte-IDENTICAL to the r56 anchor (`WIN_CENSUS: DEGRADED (git=GREEN path=DEGRADED python=DEGRADED tools=DEGRADED)` rc 1) — stability recorded, never smoothed | **PASS measured** | freshness unchanged (9, saturated) — the W-plane cadence became time-falsifiable and its stale expectation corrected by append |

Declared-command correction (R58-DECLARED-COMMAND; appended in the after-battery, never substituted): the
declared C2 counting command counts literal row names only — after-value **17**, not the declared 22; the 22
is measured by the combined command (17 + 5 rcr rows) and by the committed receipt (`rows=22`).

Repairs landed (routed carry-ins, not claims): the round-58 superseding registry table (the r57 in-place
annotation corrected by the convention's own mechanism); the bde06613 rule verified and applied (FAIL
receipts kept, corrections appended); the r57 report stale-header correction block (lesson/SCORECARD/report);
the three standing L0s routed around. An intermediate census pass exit 1 (E12 rows outside Registry) was
repaired in-round and re-passed exit 0 — the committed end receipt is the repaired pass.

## Axes — current self-assessment (round 58 final measured surface)

Restated 2026-11-01 at the round-58 final tree (counts re-derived with each cell's command; ordinals
unchanged — operability/freshness/calibration saturated, depth's move is the sourced entry, coverage/adjacency
untouched this round).

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 74 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); `SKILL.md` 4886 `wc -l`; `corpus/lessons/` 90 files (`find corpus/lessons -type f \| wc -l`); the sourced event-log plane E1-E6 landed round 58 (round-58 measured outcome; S272 current + S273 current, `event-channels` 404 recorded); GR1-GR3 of the scrub entry remain pending behind the operator-gated cohort resume; no ordinal move. | round 4; round-58 entry added, ordinal unchanged |
| coverage | 9 | `corpus/README.md` 522 `wc -l`, byte-identical to base (the r58 plane instruments a province surface — host event-log triage — inside the existing host-transition record; the README map's services rows were never re-homed and the eventlog plane joins the same class; map row addition deferred to a coverage round with its own claim). PROVINCE Core, Frontier and Adjacent sections present. | round 11; unchanged |
| operability | 9 | `bash tools/recheck-services-r56.sh` → `RECHECK_SERVICES: PASS (22 rows, 22 match, 0 drift)` rc 0 (committed receipt); `python tools/receipt-run.py --selftest` PASS 7/7; `python tools/receipt-write.py --selftest` PASS 5/5; `bash -n` rc 0; registry-coverage 95/95/0 at `e4e33606`; first-run FAIL kept on record. | round 11; round-58 22-row extension + appended registry table added, ordinal unchanged |
| freshness | 9 | services plane T1-T24 re-verifiable by one committed command, 0 drift at the r58 pass; W-plane re-verified 2026-11-01, stdout byte-identical to the r56 anchor; five notes now carry dated cadence lines (r54/r55/r56/r57 services + r53 W-plane), next pass due 2026-11-30 observable from committed bytes; S272/S273 opened live this round; sources census exit 0 at round start and end (42 W04 both). | fleet round 1; round-58 W-plane dated cadence + stale-expectation correction added, ordinal unchanged |
| calibration | 9 | the axes table above restated to counts recomputed on this host; SCORECARD uniqueness gate ok; all three claims measured with before-receipts at base via plumbing; the round's own extension failed its first run (2 drift) and the FAIL is on record; the declared counting command's shortfall self-caught and corrected by append (R58-DECLARED-COMMAND); `python tools/check-self-assessment.py` cannot evaluate here (K13, named limit). | round 10; round-58 honest-first-run-FAIL + declared-command correction added, ordinal unchanged |
| adjacency | 8 | formal overlap table present; no sibling scope touched; the event-log surface stays inside the lane's own host-operability province (the journal/boot analog, D2/D3 — no sibling absorbed); contested kaidoku/revenger ownership remains unruled (carried, routed around). | fleet round 1; unchanged |


- **planned (next round):** operator-gated first — the L0 wave-dispatch question (`tsukuroi | round-53`)
  still decides the r52 counted-cohort depth resume, and the L0 `tsukuroi | round-57` decides the S266
  `type= interact` falsification probe. If the lane stays on this host: the event-log plane's E1-E6 join the
  dated recheck discipline (an executable recheck arm for the E-rows, mirroring `recheck-services-r56.sh`,
  receipt-compared where the probe class requires it); the services planes' first cadence-dated pass receipt
  is due 2026-11-30 (or before, if a drift fires); the wevtutil NUL-byte finding wants a parsing rule in the
  plane's probes (strip `\r\0`) before any count is judged.
- **retired:** none.

## Round 59 — declaration (2026-11-01, base `c2e32b00…`, written before any after-measurement)

Carry-ins addressed first (routed from the r58 closure, status-neutral, none claimed): (1)
**D-R58-BEFORE-RECEIPTS-UNLANDED discharged** — the three cited before-receipts were regenerated from the
committed probe definitions and landed at `81776bef` (every r58 declared before-value re-derives: cat-file rc
128, wevtutil sweep 0 files, SOURCES 271, literal T-rows 12, T13/T19/receipt-compared mentions 0, round58
registry heading 0, W-plane dated 0, stale `20 cases` 1, selftest 25/25 rc 0; freshstart r50 FAIL 0/0/18 +
r51 evidence 0 bytes + r52 FAIL 1/0/16; census exit 0, 42 W04, 0 E-code — receipts
`.ufo/waves/round-58/before/{c1-c2-c3-at-base,freshstart-spotcheck,sources-census-start}.txt`; the census
receipt carries a reconciliation header because the 271-row original predates S272/S273 and is not
byte-reproducible after they landed). **Correction appended (never substituted):** the r58 landed-changes
table's "before-receipts (5)" overcounted — committed bytes cite exactly THREE distinct
`round-58/before/` paths; the remaining two of the five are named by no committed pointer, so no receipt can
be regenerated for them without inventing a citation. Every cited pointer now resolves. The r58 report lives
in the FLEET repo (lane-unmutable); this block, the round-59 lesson and the report are the correction
record. (2) The `bde06613` receipt-hygiene rule binds this round's receipts: any first-run FAIL is committed
under its honest name beside the fixed pass; any declared-command shortfall gets an appended correction
beside, never a substitution. (3) Standing L0s routed around, never treated as answered: `tsukuroi |
round-53` (wave-dispatch surface, `.ufo/l0-questions.md:229`), the round-1 kaidoku/revenger scope (PROVINCE
Frontier), `tsukuroi | round-57` (S266 interact authorization, `.ufo/l0-questions.md:247`). No new L0
question owed (nothing operator-gated attempted this round).

FRESH-START (prompt §7 names r50/r51/r52): the three rejected-honest-stop closures re-spot-checked from
committed bytes at THIS base (receipt `.ufo/waves/round-59/before/freshstart-spotcheck.txt`): r50
`.ufo/waves/round-50/after/c1-final.json` → `verdict FAIL, verdicts_ok 0, marks_ok 0, seats_ok 18`; r51
`.ufo/waves/round-51/before/c2-cheats-at-amend1.json` → committed EMPTY (0 bytes, `91227829`); r52
`.ufo/waves/round-52/after/c1-final.json` → `verdict FAIL, verdicts_ok 1, marks_ok 0, seats_ok 16`
(predicate bound 18) — identical to the r58 re-derivation at its base. Ruled out for cause (each for cause,
none reachable by a do-nothing control): (a) the counted-cohort depth resume — still gated on the absent
wave-dispatch surface (L0 round-53); (b) the S266 `type= interact` falsification probe — L0 round-57 still
unanswered; (c) re-claiming any admitted r53–r58 move (census receipt/budget modes, T1–T24 recheck +
`--raw-dir`, E1–E6 first entry, W-plane dated cadence + stale-expectation correction); (d) a bare re-run of
an existing instrument as THE freshness move — the services planes' cadence pass is due 2026-11-30, not
today, and C3's pass below is the day-0 anchor of a NEW operative line, not a bare re-run; (e) the
`considerthese/` self-improvement set — mined again this round (seven notes, latest 2026-10-26, unchanged
set), all aggregator/wave-class or Linux-host-class on this host; nothing adopted. Assimilation: none —
shokuknow unreachable.

The r58 planned lane-host items are C2 and C3 below; C1 is the round's lowest-axis move.

| # | axis | claim | before → after | falsifier | verdict condition |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S274 to be opened this round AFTER this declaration) | `corpus/knowledge/windows-scheduled-task-status-plane-r59.md` — the scheduled-task STATUS triage plane, rows J1-J5: the Status-column vocabulary as observed on this host against the S261/S274 contract; per-task `/fo LIST /v` triage FIELDS' decision grammar (values drift-class, presence invariants); the `/hresult` hex form for Last Result and S274's success/informational/failure vocabulary (0x0 vs the 0x413xx informational class vs nonzero failure); the Disabled class census; the format-switch contract (`/fo` TABLE vs CSV vs LIST row shapes for one task). Extends the r54 plane's T1-T3 (spelling/count/absence) and T2's field-NAMES row with the VALUES' grammar — no state change is ever issued (`/create /run /end /change /delete` stay operator-owned). Probes through receipt-run into `.ufo/waves/round-59/task-probes/`. Header duty `python tools/check-knowledge-header.py --revision <work>`. | before at base (verified this declaration, receipt `.ufo/waves/round-59/before/c1-c2-c3-at-base.txt`): `git cat-file -e c2e32b00:corpus/knowledge/windows-scheduled-task-status-plane-r59.md` → rc **128**; vocabulary sweeps at base, `git grep -l -i "<term>" <base> -- corpus SKILL.md PROVINCE.md tools`: `41303` → **0 files**, `last result` → **0 files**, `task scheduler error` → **0 files** (`hresult` → 2 files: S261's own parameter-row anchor and the r54 lesson quoting it — the NAME only, no value grammar); SOURCES rows **273**. after: `grep -c "^| J" <note>` ≥ 3; SOURCES rows ≥ 274, 0 malformed; knowledge-header gate 0 findings at the work revision | at base the note and the J-rows do not exist; no lane file governs the status/last-result value grammar (sweeps above) | rows ≥ 3 AND every row cites S261 or an opened S-row or a dated receipt AND knowledge-header gate 0 findings AND SOURCES ≥ 274 rows 0 malformed AND depth ordinal unchanged (8) — the move is the sourced entry, not the ordinal |
| C2 | operability | `tools/recheck-eventlog-r59.sh` — the event-log plane's executable recheck arm (the r58 planned item), mirroring `recheck-services-r56.sh`'s conventions (`--receipt <p>` + per-row `E<k> match\|drift` lines + rollup `RECHECK_EVENTLOG: PASS (N rows, M match, 0 drift)`): **11 rows** re-verifying E1-E6 plus the spelling/boundary variants on their invariant signatures — E1 enumeration rc 0 one-name-per-line; E2 newest-first rc 0 `Event[0]` with the NUL-strip parsing rule applied BEFORE any count (`tr -d '\r\0'` — the R58-WEVTUTIL-NUL-RECEIPTS fix bound in code); the E2/E3 bare-spelling variants rc 87 and the E2b/E3b env-in-child-argv variants rc 87 (the MSYS boundary pair); E3 query-absence (rc family 15007/159 + both message lines); E4 metadata field presence (`numberOfLogRecords`/`fileSize`); E5 level-filter rc 0 + Level header; E6 metadata-absence (leg-specific function line + shared message); E6b bare-`cl` usage refusal rc 87. Drift-class values (channel counts, record counts, sizes, timestamps) recorded as evidence, never judged. Registry row lands via the APPENDED `## Gate and probe registry — round59 superseding current rows` table (every round-58 row verbatim + the new row). | before at base (verified): arm `git cat-file -e c2e32b00:tools/recheck-eventlog-r59.sh` → rc **128**; `git grep -c "recheck-eventlog-r59" <base> -- SKILL.md` → **0**; round59 registry heading → **0**. after: one live pass `bash tools/recheck-eventlog-r59.sh --receipt <r>` → rc 0, `RECHECK_EVENTLOG: PASS (11 rows, 11 match, 0 drift)`; `bash -n` rc 0; registry-coverage gate **96 tools / 96 rows / 0 findings** against the appended round-59 table; the round-58 table byte-unchanged | at base no executable instrument re-verifies E1-E6b; no round-59 registry table exists | 11 rows judged AND 0 drift (any drift = honest FAIL rc 1 + an appended correction owed, reported as such) AND registry-coverage 0 findings AND the round-58 table byte-identical AND the receipt carries the full output |
| C3 | freshness | The event-log plane's cadence duty becomes OPERATIVE and is EXECUTED: an appended operative pass block in `corpus/knowledge/windows-eventlog-plane-r58.md` (old bytes byte-identical, sha256 measured base=work) naming the executable arm as the pass instrument, binding the NUL-strip parsing rule into the pass procedure, anchoring day 0 = 2026-11-01 (the r58 probe receipts as the comparison anchor), next pass due **2026-11-30** — plus the plane's FIRST executable re-verification pass under its r58 cadence line, receipted. The pass is produced by C2's arm; the claim is verifiable without C2 having landed (the note's own `recheck:` header procedure — re-run the probes through receipt-run — is the fallback producer), and C2's verdict never cites C3's block. | before at base (verified): operative pass lines in the note → **0** (`grep -c "recheck-eventlog-r59" <note>`); first-pass receipt `git cat-file -e c2e32b00:.ufo/waves/round-59/receipts/recheck-eventlog-11-summary.txt` → rc **128**; the note's r58 cadence line → **1** (stays byte-identical). after: the operative block names the arm → `grep -c "bash tools/recheck-eventlog-r59.sh" <note>` → **1**; old bytes byte-identical (sha256 base=work recorded in the after-battery); first-pass receipt committed `.ufo/waves/round-59/receipts/recheck-eventlog-11-summary.txt` carrying the rollup line and the due date (`grep -c "due 2026-11-30" <receipt>` ≥ 1) | at base no operative pass duty or pass receipt exists for the E-plane; the r58 cadence line named probes, not an instrument | operative block present AND old bytes byte-identical AND first-pass receipt committed with the rollup line AND the r58 header line byte-unchanged (append-only) AND freshness ordinal unchanged (9, saturated) — the move is duty→executed-pass, not the ordinal |

Causal separability: C1 touches only its new note + its SOURCES row; C2 touches only the new arm + the
appended registry table; C3 touches only the appended note block + the pass receipt. No claim's verification
depends on another having landed. No exploratory claim this round. Declared counting commands are each RUN
before the outcome commit cites them (R58-DECLARED-COMMAND rule).

## Round 59 — measured outcome (2026-11-01, author-side; non-author closure pending)

Measured at work revision `2913b75d` with the registry-table repair landing at `c4aa0f5c` (counting battery
`.ufo/waves/round-59/after/c1-c2-c3-counts-at-work.txt`; before-counts at base `.ufo/waves/round-59/before/
c1-c2-c3-at-base.txt`, plumbing reads of `c2e32b00` — the worktree view is untrusted on this host, r56/r57
lesson). Gates at the final tree `c4aa0f5c`: knowledge-header PASS 75/0, registry-coverage PASS 96/96/0,
SCORECARD uniqueness ok rc 0, receipt-run 7/7, receipt-write 5/5; census exit 0 both passes 42 W04 0 E-code.

| Claim | Before → after (measured) | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (lowest tied, 8; SOURCED S274 opened after the declaration) | before at `c2e32b00`: note cat-file rc **128**; vocabulary sweeps 0 files for `41303` / `last result` / `task scheduler error` (`hresult` → 2 files: S261's parameter-row anchor + the r54 lesson quoting it — the NAME only); SOURCES **273**. After at `c4aa0f5c`: `grep -c "^| J"` → **5** (J1-J5); SOURCES 273 → **274**, malformed **0**, S274 inside Registry after S273; knowledge-header gate → PASS **75** notes / **0** findings. Measured signatures (receipts j1-j5+j2b via receipt-run, all rc 0): Status census 246 rows Ready 206 / Disabled 37 / Running 3 (the r54 count 246, drift-class); verbose fields' decision grammar — `Last Result: 0` = last run succeeded (j2b Ready task) vs `Last Result: 267009` on the Running task = SCHED_S_TASK_RUNNING 0x41301 in DECIMAL (0x41301 = 267009, arithmetic [inference]); `/hresult` left the display decimal — measured DIVERGENCE from S261's exit-code-reshaping anchor (the T6 class); Scheduled Task State distinct from Status; format shapes CSV/LIST captured | **PASS measured** | depth unchanged (8) — the move is the sourced entry, not the ordinal |
| C2 operability | before at `c2e32b00`: arm cat-file rc **128**; SKILL mentions **0**; round59 registry heading **0**. After: `bash tools/recheck-eventlog-r59.sh --receipt <r>` → rc 0, `RECHECK_EVENTLOG: PASS (11 rows, 11 match, 0 drift)`; declared counting commands all read **11** (live `| grep -c ' match '`, receipt match lines, receipt row ids, `rows=11`); FIRST RUN FAIL 2 drift kept on record (E2b/E3b called receipt-run without --receipt, guard exit 2 — R59-ARM-FIRST-RUN; a second intermediate misread — receipt-run exits 0 itself — named in the lesson, R59-RECEIPT-RUN-EXITS-ZERO); `bash -n` rc 0; NUL-strip rule bound at capture (tr -d '\r\0' + PIPESTATUS on E2/E5); registry-coverage gate → PASS **96/96/0** at `c4aa0f5c` after the repair (at `2913b75d` it read 95/95/1 — R59-REGISTRY-TABLE-GAP, the extraction's trailing blanks made the parser stop at the gap and silently select the round-58 table; rows made contiguous, no row bytes changed, all 95 round-58 names carried) | **PASS measured** | operability unchanged (9, saturated) — the E-plane's 30d recheck duty made one-command executable, the r58 planned item |
| C3 freshness | before at `c2e32b00`: operative pass lines in the note → **0**; first-pass receipt cat-file rc **128**; the r58 cadence header line present (1). After: operative block appended → `grep -c "bash tools/recheck-eventlog-r59.sh" <note>` → **1**; old bytes byte-identical (sha256 prefix 09e7b6f2… equal base=work, recorded in the battery); first executable pass committed (rollup PASS 11/11 + the FAIL receipt beside it); `grep -c "due 2026-11-30" <note>` → **1** (the operative block carries the due date); the DECLARED receipt-side grep read **0** — the R59-DECLARED-COMMAND-RECEIPT-SIDE correction appended in the battery (the receipt format carries the rollup only; the note-side grep is the corrected target; a `due=` receipt-header line recorded as a planned fix, not smuggled into committed receipt bytes) | **PASS measured** | freshness unchanged (9, saturated) — the E-plane's duty moved from prose to executed-and-receipted, day 0 anchored, next pass due 2026-11-30 |

Declared-command corrections: R59-DECLARED-COMMAND-RECEIPT-SIDE (above, appended in the battery). Repairs
landed (routed carry-ins, not claims): the r58 before-receipts at `81776bef` + the "(5)"-overcount
correction (lesson + SCORECARD declaration + report); the registry-table contiguity repair `c4aa0f5c`; the
three standing L0s routed around. No exploratory claim this round.

## Axes — current self-assessment (round 59 final measured surface)

Restated 2026-11-01 at the round-59 final tree (counts re-derived with each cell's command; ordinals
unchanged — operability/freshness/calibration saturated, depth's move is the sourced entry, coverage/
adjacency untouched this round).

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 75 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); the sourced scheduled-task-status plane J1-J5 landed round 59 (S274 current, the `-codes` 404 recorded); GR1-GR3 of the scrub entry remain pending behind the operator-gated cohort resume; no ordinal move. | round 4; round-59 entry added, ordinal unchanged |
| coverage | 9 | `corpus/README.md` byte-identical to base `c2e32b00` (the r59 plane instruments a province surface — scheduled-task triage — inside the existing host-transition record; map-row addition still deferred to a coverage round with its own claim). PROVINCE Core, Frontier and Adjacent sections present. | round 11; unchanged |
| operability | 9 | `bash tools/recheck-eventlog-r59.sh` → `RECHECK_EVENTLOG: PASS (11 rows, 11 match, 0 drift)` rc 0 (committed receipt + first-run FAIL beside it); `python tools/receipt-run.py --selftest` PASS 7/7; `python tools/receipt-write.py --selftest` PASS 5/5; `bash -n` rc 0; registry-coverage 96/96/0 at `c4aa0f5c`. | round 11; round-59 eventlog arm + appended registry table added, ordinal unchanged |
| freshness | 9 | services plane T1-T24 re-verifiable by one committed command (r58 pass, 0 drift); W-plane re-verified 2026-11-01 (r58 anchor); the event-log plane's pass is now EXECUTED and receipted under its operative block (day 0 = 2026-11-01, next pass due 2026-11-30 observable from committed bytes); six notes carry dated cadence lines; S274 opened live this round; sources census exit 0 at round start and end (42 W04 both). | fleet round 1; round-59 E-plane operative pass added, ordinal unchanged |
| calibration | 9 | the axes table restated to counts recomputed on this host; SCORECARD uniqueness gate ok; all three claims measured with before-receipts at base via plumbing; the round's own arm failed its first run (2 drift) and the FAIL is on record; the declared receipt-side grep shortfall self-caught and corrected by append (R59-DECLARED-COMMAND-RECEIPT-SIDE); `python tools/check-self-assessment.py` cannot evaluate here (K13, named limit). | round 10; round-59 honest-first-run-FAIL + declared-command correction added, ordinal unchanged |
| adjacency | 8 | formal overlap table present; no sibling scope touched; the scheduled-task surface stays inside the lane's own host-operability province (the systemd-timers analog — no sibling absorbed); contested kaidoku/revenger ownership remains unruled (carried, routed around). | fleet round 1; unchanged |


- **planned (next round):** operator-gated first — the L0 wave-dispatch question (`tsukuroi | round-53`)
  still decides the r52 counted-cohort depth resume, and the L0 `tsukuroi | round-57` decides the S266
  `type= interact` falsification probe. If the lane stays on this host: a `due=` line in the
  recheck-eventlog receipt header (the R59-DECLARED-COMMAND-RECEIPT-SIDE proper fix) plus the same for
  `recheck-services-r56.sh` receipts; the task-status plane's J-rows join the executable-recheck discipline
  if a J-probe drift fires (the 2026-11-30 cadence
 pass for the services planes, the E-plane and the J-plane is due 2026-11-30 or on drift); the four
  0x413xx-vs-schtasks-Status mapping cells stay measured-inference until a source naming the CLI's own
  mapping is opened.
- **retired:** none.

## Round 60 — declaration (2026-11-01, base `5dd83fa3` + carry-in `e1e10178`, written before any after-measurement)

Carry-ins addressed first (routed from the r59 closure, status-neutral, none claimed): (1)
**R59-GATE-FAIL-RECEIPT-UNLANDED discharged at `e1e10178`** — the intermediate registry-coverage FAIL
reading (95/95/1 at `2913b75d`, the R59-REGISTRY-TABLE-GAP state) regenerated from the committed gate
code at this base and committed raw under its honest name
`.ufo/waves/round-59/after/registry-coverage-FAIL-at-2913b75d.regenerated-r60.json` (registered 95,
rows_total 95, findings 1 REGISTRY-ROW-MISSING `tools/recheck-eventlog-r59.sh`, status FAIL; PASS 96/96/0
re-run at `c4aa0f5c` and at the base) with the regeneration note naming the routing rule: a gate red
state that is part of a repair story commits its raw receipt beside the correction in the same round,
named FAIL + revision + original-or-regeneration (the r59 original died with the round scratch;
byte-equality to it is not claimed and cannot be checked). (2) **Byte-stable writers** — every append
this round is written in binary mode against the target file's own line-ending convention, and C3 below
lands the verifier instrument that proves it on committed bytes (the tameshi additivity-receipt
convention, routed as the fleet precedent); the carry-in is addressed by practice regardless of C3's
verdict. (3) **Whole-SKILL non-author SHONEN verification (owed since r55)** — operator's call; the L0
question is appended this round (`.ufo/l0-questions.md`, `tsukuroi | round-60`) and the box marks stay
untouched — routed around, never treated as answered. Standing L0s unchanged and routed around:
`tsukuroi | round-53` (wave-dispatch surface, `.ufo/l0-questions.md:229`), the round-1 kaidoku/revenger
scope (PROVINCE Frontier), `tsukuroi | round-57` (S266 interact authorization, `.ufo/l0-questions.md:247`).
No other new L0 question owed.

FRESH-START (prompt §7 names r50/r51/r52): the three rejected-honest-stop closures re-spot-checked from
committed bytes at THIS base (receipt `.ufo/waves/round-60/before/freshstart-spotcheck.txt`, plumbing
reads only): r50 `.ufo/waves/round-50/after/c1-final.json` → `verdict FAIL, verdicts_ok 0, marks_ok 0,
seats_ok 18`; r51 `.ufo/waves/round-51/before/c2-cheats-at-amend1.json` → committed EMPTY (0 bytes);
r52 `.ufo/waves/round-52/after/c1-final.json` → `verdict FAIL, verdicts_ok 1, marks_ok 0, seats_ok 16`
— identical to the r58/r59 re-derivations at their bases. Ruled out for cause (each for cause, none
reachable by a do-nothing control): (a) the counted-cohort depth resume — still gated on the absent
wave-dispatch surface (L0 round-53); (b) the S266 `type= interact` falsification probe — L0 round-57
still unanswered; (c) re-claiming any admitted r53–r59 move (host/services/eventlog/task-status/SDDL
planes, census receipt/budget modes, operative pass blocks, the registry-table and before-receipts
repairs); (d) a bare re-run of an existing instrument as THE freshness move — the services, E-plane and
J-plane cadence pass is due 2026-11-30, not today, and no drift has fired since the r59 verifier's live
re-measurement; (e) the `considerthese/` self-improvement set — re-mined this round (seven notes, latest
2026-10-26, unchanged set), all aggregator/wave-class or Linux-host-class on this host; nothing adopted.
Assimilation: none — shokuknow unreachable.

The r59 planned host items are C2 below (the `due=` receipt-header fix, both arms) and C3's instrument is
the routed byte-stable-writer practice materialized; C1 is the round's lowest-axis move. S275 was opened
LIVE earlier this round than the r59 S274 precedent's post-declaration ordering (fetched 2026-11-01
before this declaration was written) — disclosed here rather than claimed as post-declaration; the row
lands with the work commit, opened this round, quote counted.

| # | axis | claim | before → after | falsifier | verdict condition |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S275 opened this round, see above) | `corpus/knowledge/windows-registry-read-plane-r60.md` — the Windows registry READ plane via `reg.exe query`, rows RG1-RG5, the triage ground under the services' Start/ErrorControl values and the Task Scheduler keys (the lane's own host-operability province — the config store the r54-r59 planes read THROUGH schtasks/sc, now read directly); per S275 (Microsoft Learn `reg query`, Windows Commands, opened 2026-11-01): the named-value query contract (`/v valuename`, omitted → all value names; `/ve` empty-name query), the return-value table (0 Success / 1 Failure — no message text documented, the CLI's own absence message is measured), the `/s` recursion contract, the documented type set (REG_SZ, REG_MULTI_SZ, REG_EXPAND_SZ, REG_DWORD, REG_BINARY, REG_NONE) vs the types observed on a bounded triage key, and the MSYS/bash boundary variants measured on this host. No write surface is probed or authorized (`reg add/delete/copy/save/restore/load/unload` operator-owned; `export`/`compare` out of scope — the plane reads). Probes through receipt-run into `.ufo/waves/round-60/registry-probes/`. Header duty `python tools/check-knowledge-header.py --revision <work>`. | before at base (verified this declaration, receipt `.ufo/waves/round-60/before/c1-c2-c3-at-base.txt`): `git cat-file -e 5dd83fa3:corpus/knowledge/windows-registry-read-plane-r60.md` → rc **128**; vocabulary sweeps at base, `git grep -c -i "<term>" 5dd83fa3 -- corpus SKILL.md PROVINCE.md tools`: `reg query` → **0 files**, `REG_SZ` → **0 files**, `CurrentVersion` → **0 files** (grep rc 1 each); SOURCES rows **274**. after: `grep -c "^| RG" <note>` ≥ 3; SOURCES rows ≥ 275, 0 malformed, S275 inside Registry after S274; knowledge-header gate 0 findings at the work revision | at base the note and the RG-rows do not exist; no lane file governs the registry read surface (sweeps above) | rows ≥ 3 AND every row cites S275 or a dated receipt AND knowledge-header gate 0 findings AND SOURCES ≥ 275 rows 0 malformed AND depth ordinal unchanged (8) — the move is the sourced entry, not the ordinal |
| C2 | operability | The two recheck arms' receipts become SELF-DESCRIBING for the cadence pass (the r59 planned item, the R59-DECLARED-COMMAND-RECEIPT-SIDE proper fix): `tools/recheck-services-r56.sh` and `tools/recheck-eventlog-r59.sh` each gain an optional `--due YYYY-MM-DD` (format-validated `^[0-9]{4}-[0-9]{2}-[0-9]{2}$`, else usage-refusal rc 2 before any probe runs); when present the receipt header carries exactly one added line `due=<value>` before the `---` separator; when absent the receipt shape is byte-identical to the landed r56/r59 conventions (no `due` line — the committed r58/r59 receipts stay reproducible). The due anchor becomes observable from the receipt itself (the pass instrument carries its own next-pass date; the note-side `due 2026-11-30` lines and the receipt-side `due=2026-11-30` are the same anchor in both channels). | before at base (verified, same receipt): `git grep -c 'due=' 5dd83fa3 -- tools/recheck-eventlog-r59.sh tools/recheck-services-r56.sh` → **0** (rc 1); `git grep -c -- '--due' 5dd83fa3 -- tools/` → **0**; committed r59 pass receipt `.ufo/waves/round-59/receipts/recheck-eventlog-11-summary.txt` `grep -c '^due='` → **0**. after: `bash tools/recheck-services-r56.sh --receipt <r1> --due 2026-11-30` → rc 0 `RECHECK_SERVICES: PASS (22 rows, 22 match, 0 drift)`; `bash tools/recheck-eventlog-r59.sh --receipt <r2> --due 2026-11-30` → rc 0 `RECHECK_EVENTLOG: PASS (11 rows, 11 match, 0 drift)`; `grep -c '^due=' <r1>` → **1** with `due=2026-11-30`, same for `<r2>`; a no-flag eventlog run's receipt `grep -c '^due='` → **0** (shape preserved); `bash -n` rc 0 both arms | at base no arm accepts a due anchor and no receipt can carry one | both live passes 0 drift (any drift = honest FAIL rc 1 + an appended correction owed, reported as such) AND `^due=` exactly 1 with the flag and 0 without AND the flag format-refuses malformed values (rc 2) AND `bash -n` rc 0 AND the pass receipts with `due=2026-11-30` committed under `.ufo/waves/round-60/receipts/` |
| C3 | calibration | `tools/append-receipt.py` — the byte-stable append VERIFIER (the routed CRLF carry-in materialized as an instrument; the convention mirrors tameshi r63 `tools/additivity-receipt.py`, the fleet precedent — tsukuroi's own implementation over its own record files, tameshi keeps no gate ownership here, ADJ-07): reads base/tip blobs by git plumbing and prints, per `--file`: byte `prefix_ok`, raw AND CR-normalized old-only/new-only line-membership counts, `eol_rewrite_disclosed` (raw>0 with norm=0), exit 0 clean / 1 violation / 2 usage; `--require-raw` exits 1 on a disclosed rewrite; `--selftest` 5 hermetic arms (clean LF append; CRLF append on a CRLF file; whole-file EOL rewrite — disclosed, and exit 1 under `--require-raw`; content alteration exit 1; deletion exit 1). Applied to THIS round's own record-file appends: raw old-only 0 — the CRLF rewrite is avoided, not normalized away (the r55-r59 plumbing landed SCORECARD/SKILL/SOURCES CRLF-rewritten; this round's appends are byte-pure). New tool → the appended `## Gate and probe registry — round60 superseding current rows` table carries it (96 round-59 rows verbatim + 1 new, contiguous — the R59-REGISTRY-TABLE-GAP rule; gate run BEFORE the work commit cites it). | before at base (verified, same receipt): `git cat-file -e 5dd83fa3:tools/append-receipt.py` → rc **128**; `append-receipt` mentions in SKILL/LOG/SCORECARD → **0**; `round60 superseding` heading → **0** (25 superseding headings at base, latest round59; at base SKILL.md is fully CRLF 5009/5009, SOURCES 377/377, SCORECARD mixed 4178 CR / 4224 LF, LOG all-LF 0 CR). after: `python tools/append-receipt.py --selftest` → `APPEND_RECEIPT_SELFTEST: PASS (5 cases)` rc 0; registry-coverage gate at the work tree → **97 tools / 97 rows / 0 findings**; at the final measured revision `python tools/append-receipt.py --repo . --base 5dd83fa3 --tip <final> --file LOG.md --file SCORECARD.md --file SKILL.md --file corpus/SOURCES.md` → old-only raw **0** norm **0** on all four (LOG/SCORECARD/SKILL additionally byte-prefix true; SOURCES is an insert after S274 — old-only 0, prefix false by position, the R58-SOURCES-APPEND-POSITION rule) | at base no append-verifier exists and the record files carry the r55-r59 CRLF rewrite (counts above) | selftest 5/5 rc 0 AND gate 97/97/0 at the work tree AND the four record pairs measure old-only 0/0 raw and normalized at the final revision AND calibration ordinal unchanged (9, saturated) — the move is receipt honesty on the record appends, not the ordinal |

Causal separability: C1 touches only its new note + its SOURCES row + its probe receipts; C2 touches only
the two arms' flag/receipt-emit code + their run receipts; C3 touches only the new tool + the appended
registry table + the record-file WRITE mechanism this round uses (proven by the receipt, not by the other
claims' content). C1 verifies without C2/C3 (note + row + header gate); C2 verifies without C1/C3 (arms +
receipts); C3's instrument verdict (selftest + gate) verifies without C1/C2, and its applied evidence is
the byte-purity of whatever record appends landed. No exploratory claim this round. Declared counting
commands are each RUN before the outcome commit cites them (the R58-DECLARED-COMMAND rule as corrected by
R59-DECLARED-COMMAND-RECEIPT-SIDE: run the declaration's own command, on the channel it names, before
citing it).

## Round 60 — measured outcome (2026-11-01, author-side; non-author closure pending)

Measured at the work tree `6d65fc0f` (work `bef165c4` + the C1 row-index addendum `6d65fc0f`; counting
battery `.ufo/waves/round-60/after/c1-c2-c3-counts-at-work.txt`; before-counts at base
`.ufo/waves/round-60/before/c1-c2-c3-at-base.txt`, plumbing reads of `5dd83fa3` — the worktree view is
untrusted on this host, r56/r57 lesson). Gates: registry-coverage **97 tools / 97 rows / 0 findings**
PASS and knowledge-header **76 notes / 0 findings / 76 complete** PASS (JSON receipts at the work tree
`bef165c4` under `.ufo/waves/round-60/after/` — the addendum touches neither tools/ nor header keys;
both gates re-run at the final tree in the receipts commit); SCORECARD uniqueness ok rc 0;
`RECEIPT_RUN_SELFTEST: PASS (7 cases)` and `RECEIPT_WRITE_SELFTEST: PASS (5 cases)` unchanged;
`bash -n` rc 0 both arms. The final four-file append-receipt measurement (base `5dd83fa3` → final tree)
lands as a receipt in the immediately-following commit (receipt-after-subject ordering, the tameshi
r63 precedent); the work-tree pairs measured at `6d65fc0f` read old-only 0/0 raw and normalized on
SKILL.md and corpus/SOURCES.md (battery receipt).

| Claim | Before → after (measured) | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (lowest tied, 8; SOURCED — S275 opened live 2026-11-01, before the declaration text, disclosed there) | before at `5dd83fa3`: note cat-file rc **128**; vocabulary sweeps 0 files for `reg query` / `REG_SZ` / `CurrentVersion` (`git grep -c` rc 1 each); SOURCES **274**. After at `6d65fc0f`: `grep -c "^| RG" <note>` → **5** (the declared command's first work-tree run at `bef165c4` read **0** — the note had the RG rows as `##` headings; the row-index decision table is the addendum `6d65fc0f`, FAIL state re-derived from committed bytes and receipted `.ufo/waves/round-60/after/c1-declared-grep-first-run-FAIL-at-bef165c4.txt`, nothing substituted); SOURCES 274 → **275**, malformed **0**, no duplicate ids, S275 inside Registry at line 284 directly after S274; knowledge-header gate PASS **76/0/76**. Measured signatures (receipts rg1-rg5c via receipt-run): named-value rc 0 with the three-column `ProductName REG_SZ <data>` line; missing key AND missing value both rc 1 with the single line `ERROR: The system was unable to find the specified registry key or value.` (S275 documents 0 Success / 1 Failure only — the message text is host-measured, the S274 boundary class); bounded `/s` recursion rc 0; type census on the Schedule service key: 5 types (REG_SZ, REG_DWORD, REG_EXPAND_SZ, REG_MULTI_SZ, REG_BINARY) against S275's six documented `/t` types; **REG_QWORD exists on the host (rg4b) AND `/t REG_QWORD` is ACCEPTED (rg4c rc 0, `End of search: 1 match(es) found.`) — the documentation is the stale side** (the r59 J3 divergence class); the MSYS boundary: bare `/v` fails `Invalid syntax.` rc 1 at the conversion boundary (rg5a), forward-slash key paths refuse `Invalid key name.` rc 1 (rg5b), `/ve` returns the `(Default)` line with the literal `(value not set)` sentinel (rg5c) | **PASS measured** | depth unchanged (8) — the move is the sourced entry, not the ordinal |
| C2 operability | before at `5dd83fa3`: `due=` in either arm **0** (grep rc 1); `--due` in tools/ **0**; the committed r59 pass receipt `^due=` **0**. After: `bash tools/recheck-services-r56.sh --receipt <r1> --due 2026-11-30` → rc 0 `RECHECK_SERVICES: PASS (22 rows, 22 match, 0 drift)`, `grep -c '^due=' <r1>` → **1** with `due=2026-11-30`; `bash tools/recheck-eventlog-r59.sh --receipt <r2> --due 2026-11-30` → rc 0 `RECHECK_EVENTLOG: PASS (11 rows, 11 match, 0 drift)`, `^due=` → **1** with `due=2026-11-30`; the no-flag run → rc 0 11/11/0 with `^due=` **0** (shape preserved); the gate refuses `2026-13-45`, `30d` and `2026-11-3X` with rc **2**, writing NO receipt (the battery's first malformed check leaked a receipt to /tmp under the then shape-only gate — R60-STRAY-RECEIPT, fixed in the same session, stray deleted, receipt re-derivable only from the lane); `bash -n` rc 0 both arms; receipts `.ufo/waves/round-60/receipts/` (3 committed) | **PASS measured** | operability unchanged (9, saturated) — the arms' receipts became self-describing for the 2026-11-30 cadence pass (the r59 planned item, the R59-DECLARED-COMMAND-RECEIPT-SIDE proper fix) |
| C3 calibration | before at `5dd83fa3`: tool cat-file rc **128**; `append-receipt` mentions **0**; `round60 superseding` heading **0**; the record files carried the r55-r59 rewrite (SKILL 5009/5009 CRLF, SOURCES 377/377 CRLF, SCORECARD mixed 4178 CR/4224 LF, LOG all-LF). After: `python tools/append-receipt.py --selftest` → `APPEND_RECEIPT_SELFTEST: PASS (5 cases, 5 passed, 0 failed)` rc 0 (the instrument was reshaped from a first 6-check form to the declared 5-arm semantics BEFORE any commit cited it — no committed byte carries the 6-case string); registry-coverage gate → **97/97/0** at the work trees (all 96 round-59 rows carried verbatim + the one append-receipt row, contiguous); pair measurements on committed bytes: SKILL.md old_only **0/0** prefix **true**, corpus/SOURCES.md old_only **0/0** (mid-file insert after S274, prefix false by position, new_only 1) — exit 0, and **exit 0 under `--require-raw`** (no rewrite to disclose); the final four-file receipt (LOG, SCORECARD, SKILL, SOURCES at base → final tree) lands next commit (receipt-after-subject) | **PASS measured** | calibration unchanged (9, saturated) — the move is receipt honesty on the record appends: this round's appends are byte-pure (the rewrite avoided, not normalized away) |

Declared-command corrections: R60-C1-DECLARED-GREP (the `^| RG` shortfall, fixed by the addendum with the
FAIL receipted at `bef165c4`) and R60-STRAY-RECEIPT (the /tmp leak, fixed by the calendar-range gate) — both
in `corpus/lessons/round-60.md`. Repairs landed (routed carry-ins, not claims): the r59 gate-failure receipt
at `e1e10178`; the byte-stable-writer practice binding every append this round; the SHONEN L0 question
appended and routed around. No exploratory claim this round.

## Axes — current self-assessment (round 60 final measured surface)

Restated 2026-11-01 at the round-60 final tree (counts re-derived with each cell's command; ordinals
unchanged — operability/freshness/calibration saturated, depth's move is the sourced entry, coverage/
adjacency untouched this round).

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 76 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); the sourced registry READ plane RG1-RG5 landed round 60 (S275 current, opened live); GR1-GR3 of the scrub entry remain pending behind the operator-gated cohort resume; no ordinal move. | round 4; round-60 entry added, ordinal unchanged |
| coverage | 9 | `corpus/README.md` byte-identical to base `5dd83fa3` (the r60 plane instruments a province surface — the registry store behind the services/tasks planes — inside the existing host-transition record; map-row addition still deferred to a coverage round with its own claim). PROVINCE Core, Frontier and Adjacent sections present. | round 11; unchanged |
| operability | 9 | `bash tools/recheck-services-r56.sh --due 2026-11-30` → `RECHECK_SERVICES: PASS (22 rows, 22 match, 0 drift)` and `bash tools/recheck-eventlog-r59.sh --due 2026-11-30` → `RECHECK_EVENTLOG: PASS (11 rows, 11 match, 0 drift)` (committed receipts carrying `due=2026-11-30`; shape-preserving no-flag run beside them); `python tools/receipt-run.py --selftest` PASS 7/7; `python tools/receipt-write.py --selftest` PASS 5/5; `bash -n` rc 0 both arms; registry-coverage 97/97/0. | round 11; round-60 due= anchors + append-receipt registered, ordinal unchanged |
| freshness | 9 | the three planes' cadence pass (services T, eventlog E, task-status J) due 2026-11-30 — the due anchor is now observable from the pass receipts themselves (`due=2026-11-30`) and from the notes' operative blocks; six notes + the new registry note (30d, day 0 2026-11-01) carry dated cadence lines; S275 opened live this round; sources census exit 0 at round start and end (42 W04 both). | fleet round 1; round-60 receipt-side due anchor added, ordinal unchanged |
| calibration | 9 | the axes table restated to counts recomputed on this host; SCORECARD uniqueness gate ok; the declared C1 grep shortfall self-caught and repaired with the FAIL receipted (R60-C1-DECLARED-GREP); the /tmp receipt leak self-caught, gate strengthened, stray deleted (R60-STRAY-RECEIPT); this round's record appends verified byte-pure by the new instrument; `python tools/check-self-assessment.py` cannot evaluate here (K13, named limit). | round 10; round-60 honest-first-run-FAIL + stray-receipt repair added, ordinal unchanged |
| adjacency | 8 | formal overlap table present; no sibling scope touched; the registry read plane stays inside the lane's own host-operability province (the store behind its own services/tasks planes — no sibling absorbed); the append-receipt instrument CREDITS tameshi's r63 convention without moving gate ownership (ADJ-07's method-debt named in the tool docstring and the row); contested kaidoku/revenger ownership remains unruled (carried, routed around). | fleet round 1; unchanged |


- **planned (next round):** operator-gated first — the L0 wave-dispatch question (`tsukuroi | round-53`)
  still decides the r52 counted-cohort depth resume, the L0 `tsukuroi | round-57` decides the S266
  `type= interact` falsification probe, and the new `tsukuroi | round-60` decides whether the hyaku
  closure judge's spot-checks may discharge the whole-SKILL SHONEN boxes. If the lane stays on this
  host: the 2026-11-30 three-plane cadence pass (services T-rows, eventlog E-rows, task-status J-rows)
  re-run through the two arms WITH `--due 2026-12-30` (the receipts then self-carry the next anchor);
  the J-plane joins the executable-recheck discipline if a J-probe drift fires; S275 re-open at 180d or
  on upstream change (the REG_QWORD divergence noted in the row is the re-open trigger class); the four
  0x413xx-vs-schtasks-Status mapping cells stay measured-inference until a source naming the CLI's own
  mapping is opened; a `registry-probes` census arm is NOT planned — the plane is probe-receipt based,
  the census integration question stays with a coverage round.
- **retired:** none.
## Round 61 — declaration (2026-11-01, base `6b26c338`, written before any after-measurement)

Carry-ins addressed first (routed from the r60 closure, status-neutral, none claimed): (1) **the bde06613
gate-receipt rule re-applied** — the routed item (the intermediate 95/95/1 registry-coverage FAIL raw JSON,
r59) was discharged at r60's `e1e10178` and its committed receipt is verified PRESENT at this base
(`git cat-file -e 6b26c338:.ufo/waves/round-59/after/registry-coverage-FAIL-at-2913b75d.regenerated-r60.json`
→ rc 0, before-receipt); the rule stays in force this round: any r61 gate red state that is part of a
repair story commits its raw receipt the same round, named FAIL + revision + original-or-regeneration.
(2) **Byte-stable writers (the r60 C3 convention, kept)** — every r61 record-file append is written
binary-mode against the target file's own line-ending convention (SCORECARD/SKILL/SOURCES CRLF;
LOG/README LF), and the r60 instrument proves the property on committed bytes:
`python tools/append-receipt.py --repo . --base <base> --tip <final> --file … --require-raw` old-only 0/0
on every touched pair (the final four-file measurement lands receipt-after-subject, the tameshi r63
precedent — the outcome cannot measure its own commit's bytes before they exist). (3) **Standing L0s
unchanged and routed around, never treated as answered**: `tsukuroi | round-53` (wave-dispatch surface,
fleet `.ufo/l0-questions.md:229`), the round-1 kaidoku/revenger scope (PROVINCE Frontier),
`tsukuroi | round-57` (S266 interact authorization, `:247`), `tsukuroi | round-60` (whole-SKILL SHONEN
verification, `:253`). No new L0 question owed this round.

FRESH-START (prompt §7 names r50/r51/r52): the three rejected-honest-stop closures re-spot-checked from
committed bytes at THIS base (receipt `.ufo/waves/round-61/before/freshstart-spotcheck.txt`, plumbing
reads only): r50 `.ufo/waves/round-50/after/c1-final.json` → `verdict FAIL, verdicts_ok 0, marks_ok 0,
seats_ok 18`; r51 `.ufo/waves/round-51/before/c2-cheats-at-amend1.json` → committed EMPTY (0 bytes);
r52 `.ufo/waves/round-52/after/c1-final.json` → `verdict FAIL, verdicts_ok 1, marks_ok 0, seats_ok 16`
— identical to the r58/r59/r60 re-derivations at their bases. Ruled out for cause (each for cause, none
reachable by a do-nothing control): (a) the counted-cohort depth resume — still gated on the absent
wave-dispatch surface (L0 round-53); (b) the S266 `type= interact` falsification probe — L0 round-57
still unanswered; (c) re-claiming any admitted r53–r60 move (host/services/eventlog/task-status/SDDL/
registry planes, census receipt/budget modes, operative pass blocks, the registry-table and
before-receipts repairs, the `--due` receipt anchors, the append-receipt instrument); (d) a bare re-run
of an existing instrument as THE freshness move — the services/eventlog cadence pass is due 2026-11-30
(the r60 receipts' own `due=` anchors), not today, and no drift has fired since the r60 verifier's live
re-measurement; (e) the `considerthese/` self-improvement set — re-mined this round (seven notes, latest
2026-10-26, unchanged set), all aggregator/wave-class or Linux-host-class on this host; nothing adopted.
Assimilation: none — shokuknow unreachable.

The r60 planned operator-gated items stay gated (all three L0s above); the r60 planned non-gated items
are NOT due today (the 2026-11-30 three-plane cadence pass; the S275 re-open at 180d or upstream change
— neither fired). C1 below is the round's lowest-axis move; C2 materializes the r60 registry plane's
recheck duty (the note's `recheck:` header is prose today — the same gap r59 C2 closed for the E-plane);
C3 lands the coverage-map rows the r60 axes table explicitly deferred ("map-row addition still deferred
to a coverage round with its own claim"). S276 was opened LIVE before this declaration text was written
(fetched 2026-11-01) — disclosed here rather than claimed as post-declaration (the r60 S275 disclosure
precedent); the row lands with the work commit, opened this round, quote counted.

| # | axis | claim | before → after | falsifier | verdict condition |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S276 opened this round, see above) | `corpus/knowledge/windows-driver-query-plane-r61.md` — the Windows driver READ plane via `driverquery.exe`, rows DQ1-DQ5, the triage ground for the installed-device-driver inventory on this host (the lane's driver/firmware province — PROVINCE Core "driver/firmware plane (kernel modules, nvidia driver + GSP firmware presence)" — on the Windows host class, the analog of the Linux lsmod/dkms/nvidia-smi plane). Per S276 (Microsoft Learn `driverquery`, Windows Commands, opened 2026-11-01): the lede ("Enables an administrator to display a list of installed device drivers and their properties."), the syntax `[/fo {table | list | csv}] [/nh] [/v | /si]` (table the default; `/nh` "Not valid if the /fo parameter is set to list"; `/v` "not valid for signed drivers"; `/si` signed drivers), NO return-value table and NO message text documented (host-measured, the S274/S275 absence class). Host-measured signatures (recon this session, formal receipts at the work commit): the CSV inventory is one quoted 4-column header (`"Module Name","Display Name","Driver Type","Link Date"`) plus one quoted row per driver with a trailing space inside the Driver Type cell (`"Kernel "`) — a CSV-parse trap; `/V` widens CSV to 15 quoted columns ending `"Link Date","Path","Init(bytes)"` (Start Mode/State/Status/Accept-Stop the triage columns — the page documents no column set); the refusals `ERROR: Invalid syntax. '<val>' value is not allowed for '/FO' option.` rc 1, `ERROR: Invalid syntax. /NH option is valid only for "TABLE" and "CSV" format.` rc 1 (S276's /nh-list restriction MEASURED — docs and host agree, message text host-measured), `ERROR: Invalid syntax. The verbose option is invalid for signed drivers.` rc 1 (the `/v`-signed restriction MEASURED); `/SI` a plain-text 4-column table (DeviceName, InfName, IsSigned, Manufacturer); the MSYS boundary — bare `/FO` path-converted to `ERROR: Invalid argument/option - 'C:/Program Files/Git/FO'.` rc 1, the `//FO` double-slash escape and `MSYS_NO_PATHCONV=1` both pass (the r60 RG5 class recurring on a SECOND Windows command — a two-command pattern, not a one-off). Local reads only (the remote `/S /U /P` legs out of scope); driverquery has no write verbs — nothing to fence beyond scope. Probes through receipt-run into `.ufo/waves/round-61/driver-probes/`. Header duty `python tools/check-knowledge-header.py --revision <work>`. | before at base (verified this declaration, receipt `.ufo/waves/round-61/before/c1-c2-c3-at-base.txt`): `git cat-file -e 6b26c338:corpus/knowledge/windows-driver-query-plane-r61.md` → rc **128**; vocabulary sweep at base `git grep -c -i driverquery 6b26c338 -- corpus SKILL.md PROVINCE.md tools` → **0 files** (rc 1); SOURCES rows **275**. after: `grep -c "^| DQ" <note>` ≥ 3; SOURCES rows ≥ 276, 0 malformed, S276 at id position directly after S275; knowledge-header gate 0 findings at the work revision | at base the note and the DQ rows do not exist; no lane file governs the driverquery read surface (sweep above) | rows ≥ 3 AND every row cites S276 or a dated receipt AND knowledge-header gate 0 findings AND SOURCES ≥ 276 rows 0 malformed AND depth ordinal unchanged (8) — the move is the sourced entry, not the ordinal |
| C2 | operability | `tools/recheck-registry-r61.sh` — the registry read plane's EXECUTABLE recheck arm (the r59 C2 pattern applied to the newest plane; the r60 note's `recheck:` duty is prose today): 10 rows over RG1-RG5's invariant signatures (R1 the named-value three-column entry shape; R2/R2b the single-message absence class rc 1 for missing key and missing value; R3 bounded `/s` recursion rc 0; R4/R4b/R4c the type-superset census on the Schedule key + REG_QWORD exists on Winlogon + `/t REG_QWORD` accepted rc 0; R5a bare-`/v` MSYS mangling `Invalid syntax.` rc 1; R5b forward-slash key `Invalid key name.` rc 1; R5c `/ve` returns the `(Default)` line rc 0), each judged on its INVARIANT (rc + message/shape), counts and data values drift-class; optional `--due YYYY-MM-DD` (shape + calendar-range gate rc 2 before any probe runs, no receipt written on refusal — the r60 C2 convention verbatim); rollup `RECHECK_REGISTRY: PASS (10 rows, M match, 0 drift)`. New tool → the appended `## Gate and probe registry — round61 superseding current rows` table carries it (97 round-60 rows verbatim + 1 new, contiguous — the R59-REGISTRY-TABLE-GAP rule); gate run BEFORE the outcome cites it. | before at base (verified, same receipt): `git cat-file -e 6b26c338:tools/recheck-registry-r61.sh` → rc **128**; `git grep -c RECHECK_REGISTRY 6b26c338 -- tools SKILL.md` → **0** (rc 1). after: `bash tools/recheck-registry-r61.sh --receipt <r> --due 2026-11-30` → rc 0 `RECHECK_REGISTRY: PASS (10 rows, 10 match, 0 drift)`; `grep -c '^due=' <r>` → **1** with `due=2026-11-30`; a no-flag run's receipt `^due=` → **0** (shape preserved); malformed `--due` refused rc **2** writing NO receipt (lane-tree or no receipt path only — the R60-STRAY-RECEIPT rule); `bash -n` rc 0; registry-coverage gate **98/98/0** at the work tree | at base no committed instrument re-checks the registry plane | 10/10 live match 0 drift (any drift = honest FAIL rc 1 + an appended row correction owed, reported as such) AND `^due=` exactly 1 with the flag and 0 without AND the flag format-refuses malformed values (rc 2) AND `bash -n` rc 0 AND the pass receipts with `due=2026-11-30` committed under `.ufo/waves/round-61/receipts/` AND operability ordinal unchanged (9, saturated) |
| C3 | coverage | `corpus/README.md` Coverage map gains the Windows-host transition rows — the map section the r60 axes table explicitly deferred ("map-row addition still deferred to a coverage round with its own claim"): an appended `## Rounds 53-61 — the Windows host transition` section whose table carries one row per Windows-host knowledge entry (the EIGHT r53-r60 notes + this round's r61 note when it lands beside this claim), each naming the note, what it holds, and its sources. Map governance on held ground — the domain entries already exist; the MAP (the governance surface the coverage axis names) does not list them: the map's latest section is Round 50, the eight Windows notes landed r53-r60 with zero map rows. PROVINCE.md unchanged — no frontier claim; the map catches up to held ground. | before at base (verified, same receipt): `git grep -c 'knowledge/windows-' 6b26c338 -- corpus/README.md` → **0 files** (rc 1); the README's last map section is `## Round 50` (34 `## ` headings; tail confirmed Round-50 prose). after: `grep -c 'knowledge/windows-' corpus/README.md` ≥ **8** (the eight pre-existing notes; 9 when C1 lands in the same round — the measured value is reported as read) AND the new section is an append after the Round-50 section (README is all-LF; byte-prefix true) | at base the map holds zero Windows-host rows while the corpus holds eight Windows-host notes | rows ≥ 8 AND PROVINCE.md byte-identical to base (no frontier claim) AND README old-only 0 (pure append, the append-receipt instrument) AND coverage ordinal unchanged (9, saturated) — the move is map governance, not new ground |

Causal separability: C1 touches only its new note + its SOURCES row + its probe receipts; C2 touches only
the new arm + its SKILL registry-table append + its run receipts; C3 touches only corpus/README.md. C1
verifies without C2/C3 (note + row + header gate); C2 verifies without C1/C3 (arm + receipts + registry
gate — its RG rows re-verify the r60 plane, already committed at base); C3's ≥ 8 verdict verifies without
C1/C2 (the eight base bytes), the ninth row being C1's note named in the same section. No exploratory
claim this round. Declared counting commands are each RUN before the outcome commit cites them (the
R58/R59 declared-command rule): the C1 grep binds to the DELIVERED table shape — the note ships `| DQ`
rows from the first commit (the R60-C1-DECLARED-GREP rule applied at authoring time); the SKILL round-61
section documents all three moves (round documentation, not claim content); the battery receipt lands
with the outcome.## Round 61 — measured outcome (2026-11-01, author-side; non-author closure pending)

Measured at the work tree `abb2a161` (work after declaration `136bfb00`; counting battery
`.ufo/waves/round-61/after/c1-c2-c3-counts-at-work.txt`; before-counts at base
`.ufo/waves/round-61/before/c1-c2-c3-at-base.txt`, plumbing reads of `6b26c338` — the worktree view is
untrusted on this host, r56/r57 lesson). Gates at the work revision: registry-coverage **98 tools /
98 rows / 0 findings** PASS and knowledge-header **77 notes / 0 findings / 77 complete** PASS (JSON
receipts under `.ufo/waves/round-61/after/`); SCORECARD uniqueness ok rc 0;
`RECEIPT_RUN_SELFTEST: PASS (7 cases)`, `RECEIPT_WRITE_SELFTEST: PASS (5 cases)` and
`APPEND_RECEIPT_SELFTEST: PASS (5 cases)` unchanged; `bash -n tools/recheck-registry-r61.sh` rc 0.
The final append-receipt measurement (base `6b26c338` → final tree, five record files) lands as a
receipt in the immediately-following commit (receipt-after-subject ordering, the tameshi r63
precedent); the work-tree pairs measured at `abb2a161` read old-only 0/0 raw and normalized on
SKILL.md, corpus/SOURCES.md and corpus/README.md (SOURCES an insert after S275, README an append —
prefix false by position on both, the R58-SOURCES-APPEND-POSITION rule).

| Claim | Before → after (measured) | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (lowest tied, 8; SOURCED — S276 opened live 2026-11-01 before the declaration text, disclosed there) | before at `6b26c338`: note cat-file rc **128**; vocabulary sweep `driverquery` **0 files** (`git grep -c -i` rc 1); SOURCES **275**. After at `abb2a161`: `grep -c "^| DQ" <note>` → **5** (the declared command's shape — the row-index table shipped in the delivered form at the first commit, the R60-C1-DECLARED-GREP rule applied at authoring time; no FAIL state this round); SOURCES 275 → **276**, 0 duplicate ids, S276 at line 285 directly after S275 (line 284), 11 cells (NF 13 = S275's NF); the Gate quote recounted `wc -w` → **14**; knowledge-header gate PASS **77/0/77**. Measured signatures (receipts dq1-dq5c via receipt-run): CSV inventory rc 0, 412 stdout lines = 1 four-column header + 411 quoted rows with the trailing-space `"Kernel "` Driver Type cell and empty Link Date cells (drift-class); `/FO csv /V` rc 0, 15 quoted columns ending `"Link Date","Path","Init(bytes)"`; invalid `/FO` value → `ERROR: Invalid syntax. 'bogus' value is not allowed for '/FO' option.` rc 1; `/FO LIST /NH` → `ERROR: Invalid syntax. /NH option is valid only for "TABLE" and "CSV" format.` rc 1 (S276's /nh-list restriction MEASURED, docs and host agree, message text host-measured); `/V /SI` → `ERROR: Invalid syntax. The verbose option is invalid for signed drivers.` rc 1 (S276's /v-signed restriction MEASURED); `/SI` rc 0, plain-text 4-column table (159 rows at capture); the MSYS boundary: bare `/FO` mangled at the bash→python boundary (the receipt's own `command=` line records `driverquery 'C:/Program Files/Git/FO' csv`), rc 1 with the Invalid-argument message — the `//FO` escape and the on-invocation `MSYS_NO_PATHCONV=1` both pass rc 0 (dq5b/dq5c) — the RG5 class on a second command | **PASS measured** | depth unchanged (8) — the move is the sourced entry, not the ordinal |
| C2 operability | before at `6b26c338`: tool cat-file rc **128**; `RECHECK_REGISTRY` mentions **0**; no round-61 receipts. After: `bash tools/recheck-registry-r61.sh --receipt <r1> --due 2026-11-30` → rc 0 `RECHECK_REGISTRY: PASS (10 rows, 10 match, 0 drift)`, `grep -c '^due=' <r1>` → **1** with `due=2026-11-30`; the no-flag run → rc 0 10/10/0 with `^due=` **0** (shape preserved); malformed `--due` refused rc **2** with NO receipt (`2026-13-45` calendar-range refusal, `30d` and `2026-11-3X` shape refusals — receipt path checked absent after each, the R60-STRAY-RECEIPT rule); `bash -n` rc 0; registry-coverage gate **98/98/0** at the work revision. First run of the arm FAILED 1 drift (R4) — the type-extraction regex `REG_[A-Z]+` truncated at the underscore (REG_EXPAND_SZ read as REG_EXPAND), an authoring-time artifact, not host drift; FAIL receipt kept under its honest name `recheck-registry-FIRST-RUN-FAIL-at-authoring.txt` (R61-ARM-FIRST-RUN, the r59 rule), fixed run passes 10/10 (the r59 ARM-FIRST-RUN pattern: FAIL beside the pass) | **PASS measured** | operability unchanged (9, saturated) — the r60 registry plane's recheck duty became executable (the r59 C2 pattern on the newest plane) |
| C3 coverage | before at `6b26c338`: `knowledge/windows-` in corpus/README.md **0 files** (rc 1); the map's last section `## Round 50`. After: `grep -c 'knowledge/windows-' corpus/README.md` → **9** (the eight r53-r60 notes + the r61 note, one row each with verified row-ids and source ids); the section is an append after the Round-50 section; PROVINCE.md **blob-identical** to base (`git rev-parse` both revisions → `23198d74…` = `23198d74…`); README old-only 0 at the work-tree pair (the append is pure; the final five-file measurement lands next commit) | **PASS measured** | coverage unchanged (9, saturated) — map governance on held ground; no frontier claim |

Declared-command notes: all three claims' counting commands ran at the work revision on the channels
they name (the battery receipt) — no declared-command FAIL state this round (the C1 grep bound to the
delivered table shape per R60-C1-DECLARED-GREP; the C2 arm's own first-run FAIL is the instrument's
honest first run, receipted and repaired in the same session, R61-ARM-FIRST-RUN). Repairs landed
(routed carry-ins, not claims): the bde06613 rule re-applied (the discharged r59 FAIL receipt verified
present at the base; no r61 gate red state occurred — the arm FAIL is a probe-instrument first run,
not a gate red state, and is receipted regardless); every record append byte-stable (the r60 C3
convention; the final measurement lands next commit). No exploratory claim this round.

## Axes — current self-assessment (round 61 final measured surface)

Restated 2026-11-01 at the round-61 final tree (counts re-derived with each cell's command; ordinals
unchanged — operability/freshness/calibration/coverage saturated, depth's move is the sourced entry,
adjacency untouched this round).

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 77 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); the sourced driver-query plane DQ1-DQ5 landed round 61 (S276 current, opened live); GR1-GR3 of the scrub entry remain pending behind the operator-gated cohort resume; no ordinal move. | round 4; round-61 entry added, ordinal unchanged |
| coverage | 9 | the corpus README Coverage map now carries the Windows-host transition rows (`grep -c 'knowledge/windows-' corpus/README.md` → 9; before 0 at base) — map governance on held ground, the r60-deferred duty; PROVINCE Core, Frontier and Adjacent sections unchanged (blob-identical to base). | round 11; round-61 map rows added, ordinal unchanged |
| operability | 9 | `bash tools/recheck-registry-r61.sh --due 2026-11-30` → `RECHECK_REGISTRY: PASS (10 rows, 10 match, 0 drift)` (committed receipts carrying `due=2026-11-30`; shape-preserving no-flag run beside them; the first-run FAIL receipt kept); `python tools/receipt-run.py --selftest` PASS 7/7; `python tools/receipt-write.py --selftest` PASS 5/5; `bash -n` rc 0; registry-coverage 98/98/0. | round 11; round-61 registry arm added, ordinal unchanged |
| freshness | 9 | the three planes' cadence pass (services T, eventlog E, task-status J) due 2026-11-30 (the r60 receipts' `due=` anchors); the registry plane's recheck duty now executable (this round's arm; its receipts self-carry `due=2026-11-30` matching the r60 note's operative block); the new driver-query note carries its own 30d cadence (day 0 2026-11-01, due 2026-11-30); S276 opened live this round; sources census exit 0 at round start (42 W04, 0 E-code) and at round end (receipt with the final commit). | fleet round 1; round-61 driver-query cadence + registry arm added, ordinal unchanged |
| calibration | 9 | the axes table restated to counts recomputed on this host; SCORECARD uniqueness gate ok; the C2 arm's first-run FAIL self-caught BEFORE any outcome cited it, receipted under its honest name and repaired (R61-ARM-FIRST-RUN); the S276 row's 14-cell delimiter slip self-caught at the awk NF check BEFORE any commit (no committed byte carries the malformed shape); the dq1 first spawn's wrong-var form self-caught at the receipt rc line and re-run correct before commit (R61-SPAWN-VAR-POSITION); `python tools/check-self-assessment.py` cannot evaluate here (K13, named limit). | round 10; round-61 honest-first-run-FAIL + two pre-landing self-catches added, ordinal unchanged |
| adjacency | 8 | formal overlap table present; no sibling scope touched; the driver-query plane stays inside the lane's own driver/firmware province (PROVINCE Core — state and health reading, not shipped-artifact internals; kaidoku/revenger unaffected); the README map rows name only this lane's own notes and sources; contested kaidoku/revenger ownership remains unruled (carried, routed around). | fleet round 1; unchanged |


- **planned (next round):** operator-gated first — the L0 wave-dispatch question (`tsukuroi | round-53`)
  still decides the r52 counted-cohort depth resume, the L0 `tsukuroi | round-57` decides the S266
  `type= interact` falsification probe, and `tsukuroi | round-60` decides whether the hyaku closure
  judge's spot-checks may discharge the whole-SKILL SHONEN boxes. If the lane stays on this host: the
  2026-11-30 cadence pass (services T-rows, eventlog E-rows, task-status J-rows, and NOW the registry
  R-rows through the new arm) re-run through the three arms WITH the next `--due` anchor (the receipts
  then self-carry it); the DQ rows join the executable-recheck discipline only if a DQ-probe drift
  fires (the r59 planned-item pattern, applied to the driver plane); a Windows pagefile/commit-charge
  memory CONFIG read (pagefile location/size via `wmic pagefile`/CIM) is the candidate next plane —
  memory PRESSURE evidence stays mori's (ADJ-04), the config surface is this lane's; S276 re-open at
  180d or on upstream change.
- **retired:** none.

## Round 62 — correction block: the r61 landing-class receipt statements (R61-RAW-RECEIPTS-UNLANDED discharge)

The round-61 rows above (C2 declaration verdict condition "the pass receipts with `due=2026-11-30`
committed under `.ufo/waves/round-61/receipts/`"; C2 outcome "FAIL receipt kept under its honest
name `recheck-registry-FIRST-RUN-FAIL-at-authoring.txt`"; axes-table operability cell "committed
receipts carrying `due=2026-11-30` ... the first-run FAIL receipt kept") asserted committed status
for files that were worktree-only at the r61 head `52d9ba1a` — the r61 closure's defect 1
(R61-RAW-RECEIPTS-UNLANDED, the lane's unlanded-receipt class, third occurrence) and defect 2 (the
landing-class misstatements). Discharged in round 62's carry-in commit `ccfa4706`: all twelve cited
receipts (nine `driver-probes/` dq files + three `receipts/` files) landed byte-identically under
their honest names, nothing substituted; from `ccfa4706` on every statement above holds of committed
bytes and the C2 verdict condition's receipts clause is satisfied. Class rule restated at the
landing: count the cited paths before writing counts — a receipt count cited in a landed-changes
table must equal the number of distinct receipt paths the round's committed bytes name, and every
one must be landed before the round closes. Made mechanical by the round-62 gate
`tools/check-cited-receipts-r62.py` (at `52d9ba1a` --round 61: FAIL naming exactly the three
committed-bytes-named receipts; at the round-62 final tree: PASS). No measurement above changed:
the r61 values were independently re-derived live by the non-author judge from the instruments.

## Round 62 — declaration (2026-11-01, base `bcf1af18` + carry-ins `ccfa4706`/`f47bb0aa`, written before any after-measurement)

Carry-ins addressed FIRST (both landed and pushed before this declaration, neither claimed):
(1) **R61-RAW-RECEIPTS-UNLANDED discharged at `ccfa4706`** — the twelve r61 receipts (nine
`driver-probes/` dq files + three `receipts/` files incl. the FIRST-RUN-FAIL) landed byte-identically
under their honest names (pre-landing `git hash-object` ids in
`.ufo/waves/round-62/carry-in/r61-raw-receipts-landing-note.md`; treecommit reads disk bytes, so
landed = worktree bytes; 12/12 `git cat-file -e` rc 0 verified); the class rule restated at the
landing (the r59 rule, third occurrence of the class): count the cited paths before writing counts —
a receipt count cited in a landed-changes table must equal the number of distinct receipt paths the
round's committed bytes name, and every one of them must be landed before the round closes.
(2) **The landing-class misstatements corrected at `f47bb0aa`** — appended correction blocks in the
r61 lesson and here (the "committed" statements were false at `52d9ba1a`, true from `ccfa4706`; the
interval named), plus the r53 coverage-map row's Note cell now naming the sibling note
`knowledge/host-transition-drift-r53.md` where the D1-D7 table lives (disclosed one-cell repair).
(3) **Standing L0s unchanged and routed around, never treated as answered**: `tsukuroi | round-53`
(wave-dispatch surface, fleet `.ufo/l0-questions.md:229`), round-1 kaidoku/revenger scope (PROVINCE
Frontier), `tsukuroi | round-57` (S266 interact authorization, `:247`), `tsukuroi | round-60`
(whole-SKILL SHONEN verification, `:253`). No new L0 question owed this round. (4) Byte-stable
writers (the r60 C3 convention, kept): SCORECARD/SKILL/SOURCES appends CRLF, LOG/README LF, proven
by the final append-receipt measurement (lands receipt-after-subject, the tameshi r63 precedent).

FRESH-START (prompt §7 names r50/r51/r52): the three rejected-honest-stop closures re-spot-checked
from committed bytes at THIS base (receipt `.ufo/waves/round-62/before/freshstart-spotcheck.txt`,
plumbing reads only): r50 `.ufo/waves/round-50/after/c1-final.json` → `verdict FAIL, verdicts_ok 0,
marks_ok 0, seats_ok 18`; r51 `.ufo/waves/round-51/before/c2-cheats-at-amend1.json` → committed
EMPTY (0 bytes); r52 `.ufo/waves/round-52/after/c1-final.json` → `verdict FAIL, verdicts_ok 1,
marks_ok 0, seats_ok 16` — identical to the r58–r61 re-derivations. Ruled out for cause (none
reachable by a do-nothing control): (a) the counted-cohort depth resume — still gated on the absent
wave-dispatch surface (L0 round-53); (b) the S266 `type= interact` falsification probe — L0
round-57 still unanswered; (c) re-claiming any admitted r53–r61 move (host/services/eventlog/
task-status/SDDL/registry/driver-query planes, census receipt/budget modes, operative pass blocks,
the registry-table and before-receipts repairs, the `--due` receipt anchors, the append-receipt
instrument, the map rows); (d) the 2026-11-30 cadence pass as THE freshness move — not due (the
r60/r61 receipts' own `due=` anchors; today is day 0 of the new plane's cadence, not a due day);
(e) the `considerthese/` self-improvement set — re-mined (seven notes, latest 2026-10-26, unchanged
set since r57), all aggregator/wave-class or Linux-host-class on this host; nothing adopted.
Assimilation: none — shokuknow unreachable.

The r61 planned non-gated candidate becomes C1 (the pagefile/commit-charge memory CONFIG read —
"memory PRESSURE evidence stays mori's (ADJ-04), the config surface is this lane's"). C2
materializes the restated class rule mechanically: the unlanded-receipt class occurred three times
(r58, r59, r61) and each discharge was by hand; the gate is the machine that catches the next one.
S277 was opened LIVE before this declaration text was written (fetched 2026-11-01) — the r60/r61
disclosure order; the row lands with the work commit, quote counted. No exploratory claim this
round.

| # | axis | claim | before → after | falsifier | verdict condition |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S277 opened this round, see above) | `corpus/knowledge/windows-pagefile-config-plane-r62.md` — the Windows pagefile/commit-charge CONFIG READ plane, rows PF1-PF6: the usage counters per S277 (AllocatedBaseSize / CurrentUsage / PeakUsage, each documented units ("megabytes"); AllocatedBaseSize "corresponds to the range established in Win32_PageFileSetting under the InitialSize and MaximumSize properties, set at system startup"); the automatic-management triad (Win32_ComputerSystem.AutomaticManagedPagefile TRUE; Win32_PageFileSetting EMPTY instance set — the system-managed indicator S277 does not document; registry PagingFiles REG_MULTI_SZ `?:\pagefile.sys` the system-managed wildcard form, no explicit sizes); the commit-charge fields (Win32_OperatingSystem TotalVirtualMemorySize / FreeVirtualMemory, KB) recorded drift-class with the ADJ-04 boundary stated in the note (pressure attribution is mori's; raw counters are captures, never judged here); the wmic.exe ABSENCE (bare spawn WinError 2 at CreateProcess; the `cmd /c` refusal receiptable `'wmic' is not recognized...` rc 1 — the D8 tool-absence class, now including a legacy binary). Probes through receipt-run into `.ufo/waves/round-62/probes/`. Header duty `python tools/check-knowledge-header.py --revision <work>`. | before at base (verified this declaration, receipt `.ufo/waves/round-62/before/c1-c2-at-base.txt`): `git cat-file -e bcf1af18:corpus/knowledge/windows-pagefile-config-plane-r62.md` → rc **128**; vocabulary sweep at base `git grep -c -iE 'pagefile|PageFileUsage|AutomaticManagedPagefile' bcf1af18 -- corpus SKILL.md PROVINCE.md tools` → **0 files** (rc 1); SOURCES rows **276**. after: `grep -c '^| PF' <note>` ≥ 4; SOURCES rows ≥ 277, 0 malformed, S277 at id position directly after S276; knowledge-header gate 0 findings at the work revision | at base the note and the PF rows do not exist; no lane file governs the pagefile config-read surface (sweep above) | rows ≥ 4 AND every row cites S277 or a dated receipt AND knowledge-header gate 0 findings AND SOURCES ≥ 277 rows 0 malformed AND depth ordinal unchanged (8) — the move is the sourced entry, not the ordinal |
| C2 | operability | `tools/check-cited-receipts-r62.py` — the round-scoped cited-receipt landing gate (the r59 count rule made mechanical; catches the cited-and-unlanded half of the class before closure): at a revision, scans the round's OWN committed artifacts (its `.ufo/waves/round-<N>/` receipts, `corpus/lessons/round-<N>.md`, its `corpus/knowledge/*-r<N>.md` note) for `.ufo/waves/round-<N>/...` file citations and verifies each against the SAME revision's tree (ls-tree + one `cat-file --batch`, index-free, read-only, the round-32 child-env allow-list); documented exclusions: sibling-repo citations (a `<lane>/.ufo/waves/...` prefix names another repo's tree), directory prefixes and bare directory mentions, prose ellipses; findings = CITED-RECEIPT-MISSING. Named limit stated in the docstring: a receipt retained in scratch and never cited by a resolvable path (the r59 occurrence) is invisible to any path-citation gate — the closure catches that half. | before at base (verified, same receipt): `git cat-file -e bcf1af18:tools/check-cited-receipts-r62.py` → rc **128**; `git grep -c CHECK_CITED_RECEIPTS bcf1af18 -- tools SKILL.md` → **0** (rc 1); and the class itself: the gate run at THIS base `--round 61` → verdict **FAIL, findings 3** naming exactly the three committed-bytes-named r61 receipts (full JSON `.ufo/waves/round-62/before/cited-receipts-at-base-round61.json`) — the defect the carry-in landed by hand at `ccfa4706`, re-derived mechanically at the base. after: `python tools/check-cited-receipts-r62.py --selftest` → PASS 4 cases rc 0; at the r62 final tree `--round 61` → **PASS, 0 findings** (the discharged state) and `--round 62` → **PASS, 0 findings** (this round's receipts landed receipt-after-subject); registry-coverage gate **99/99/0** at the work tree (the new row); the r58 demonstration re-derived (`--round 58` at r58-final `c2e32b00` → FAIL naming `.ufo/waves/round-58/before/sources-census-start.txt`, the in-scope half of that occurrence) | at base no committed instrument checks cited-receipt landing; the class occurred three times (r58/r59/r61) | selftest PASS rc 0 AND --round 61 PASS at the r62 final tree AND --round 62 PASS at the r62 final tree AND registry-coverage 99/99/0 AND operability ordinal unchanged (9, saturated) AND the r59 scratch-retained citation named as the gate's limit in the lesson (honest reach — no claim of total class coverage) |

Causal separability: C1 touches only its new note + its SOURCES row + its probe receipts; C2 touches
only the new tool + its registry-table row + its run receipts. C1 verifies without C2 (note + row +
header gate); C2 verifies without C1 (tool + selftest + final-tree passes + registry gate). No
exploratory claim this round. Declared counting commands are each RUN before the outcome commit
cites them (the R58/R59 declared-command rule); the SKILL round-62 section documents both moves
(round documentation, not claim content); the battery receipt lands with the outcome.

## Round 62 — measured outcome (2026-11-01, author-side; non-author closure pending)

Measured at the work tree `f3f64812` (work after declaration `e50973da`; counting battery
`.ufo/waves/round-62/after/c1-c2-counts-at-work.txt`; before-counts at base
`.ufo/waves/round-62/before/c1-c2-at-base.txt`, plumbing reads of `bcf1af18` — the worktree view is
untrusted on this host, r56/r57 lesson). Gates at the work revision: registry-coverage **99 tools /
99 rows / 0 findings** PASS and knowledge-header **78 notes / 0 findings / 78 complete** PASS (JSON
receipts under `.ufo/waves/round-62/after/`); SCORECARD uniqueness ok rc 0;
`RECEIPT_RUN_SELFTEST: PASS (7 cases)`, `RECEIPT_WRITE_SELFTEST: PASS (5 cases)` and
`APPEND_RECEIPT_SELFTEST: PASS (5 cases)` unchanged; the new gate's `--selftest` PASS 4 cases rc 0;
`python -m py_compile tools/check-cited-receipts-r62.py` rc 0. The class demonstrations re-run from
the committed tool (receipts `.ufo/waves/round-62/after/`): `--round 61` at `52d9ba1a` FAIL 3,
`--round 58` at `c2e32b00` FAIL 1, `--round 59` at `35c2748f` PASS 0 (the named limit), `--round 61`
and `--round 62` at this round's trees PASS 0. The final append-receipt measurement (base `bcf1af18`
→ final tree, five record files; README's disclosed one-cell repair expected as old-only 1 /
new-only 1) lands as a receipt in the immediately-following commit (receipt-after-subject ordering,
the tameshi r63 precedent).

| Claim | Before → after (measured) | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (lowest tied, 8; SOURCED — S277 opened live 2026-11-01 before the declaration text, disclosed there) | before at `bcf1af18`: note cat-file rc **128**; vocabulary sweep `pagefile|PageFileUsage|AutomaticManagedPagefile` **0 files** (`git grep -c -iE` rc 1); SOURCES **276**. After at `f3f64812`: `grep -c '^| PF' <note>` → **6**; SOURCES 276 → **277**, 0 duplicate ids, S277 at line 286 directly after S276 (line 285), 11 cells (NF 13 = S275's NF, awk-verified before the work commit); the Gate quote recounted `wc -w` → **18**; knowledge-header gate PASS **78/0/78**. Measured signatures (receipts pf1-pf7 via receipt-run): `Get-CimInstance Win32_PageFileUsage` rc 0, exactly ONE instance — `Name : C:\pagefile.sys`, `AllocatedBaseSize : 18035`, `CurrentUsage : 4570`, `PeakUsage : 5287` (MB per S277's units, values drift-class); `Get-CimInstance Win32_PageFileSetting` rc 0 with an EMPTY instance set (the system-managed indicator S277 does not document); `(Get-CimInstance Win32_ComputerSystem).AutomaticManagedPagefile` → `True` rc 0; `reg query ...Memory Management /v PagingFiles` rc 0, `REG_MULTI_SZ` data `?:\pagefile.sys` (the system-managed wildcard, no explicit sizes); `Get-CimInstance Win32_OperatingSystem` rc 0, TotalVirtualMemorySize 35161444 / FreeVirtualMemory 1710148 KB at capture (drift-class, ADJ-04-bounded — attribution is mori's, recorded never judged); `wmic pagefile list /format:list` — bare spawn WinError 2 (wmic.exe ABSENT; the receipt-run crash captured as the pf7 meta-receipt, R62-RECEIPT-RUN-SPAWN-FAIL), the `cmd /c` wrapper receipts the refusal `'wmic' is not recognized...` rc 1 | **PASS measured** | depth unchanged (8) — the move is the sourced entry, not the ordinal |
| C2 operability | before at `bcf1af18`: tool cat-file rc **128**; `CHECK_CITED_RECEIPTS` mentions **0**; and the class itself: the gate at THIS base `--round 61` → verdict **FAIL, findings 3** naming exactly the three committed-bytes-named r61 receipts (`.ufo/waves/round-62/before/cited-receipts-at-base-round61.json`) — the defect the carry-in landed by hand at `ccfa4706`, re-derived mechanically. After at `f3f64812`: `python tools/check-cited-receipts-r62.py --selftest` → JSON `selftest PASS` 4 cases rc 0; `--round 61` at the work tree → **PASS, 0 findings** (5 cited paths — the discharged state); `--round 62` at the work tree → **PASS, 0 findings** (8 cited paths — this round's receipts landed with the work commit); the historical demonstrations from the committed tool: `52d9ba1a` `--round 61` → FAIL **3** (the exact three receipt paths), `c2e32b00` `--round 58` → FAIL **1** (`sources-census-start.txt`), `35c2748f` `--round 59` → PASS **0** (the r59 occurrence was scratch-retained and never cited by a resolvable path — the gate's named limit, stated in the docstring and the lesson); registry-coverage gate **99/99/0** at the work revision (the new row contiguous after 98 carried rows) | **PASS measured** | operability unchanged (9, saturated) — the r59 count rule became an executable gate (the class's cited-and-unlanded half is now caught mechanically before closure) |

Declared-command notes: both claims' counting commands ran at the work revision on the channels
they name (the battery receipt) — no declared-command FAIL state this round. Repairs landed (routed
carry-ins, not claims): R61-RAW-RECEIPTS-UNLANDED at `ccfa4706` and the landing-class correction
blocks + r53 map-row sibling pointer at `f47bb0aa`. Three mistakes mined this round
(R62-RECEIPT-RUN-SPAWN-FAIL, R62-BATCH-DEADLOCK, R62-RECEIPT-RUN-TMP-PATH — all
captured-by/evidence/fix in the lesson); the receipt-run spawn-map proper fix is the round-63
planned item. No exploratory claim this round.

## Axes — current self-assessment (round 62 final measured surface)

Restated 2026-11-01 at the round-62 final tree (counts re-derived with each cell's command; ordinals
unchanged — operability/freshness/calibration/coverage saturated, depth's move is the sourced entry,
adjacency untouched this round).

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 78 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); the sourced pagefile-config plane PF1-PF6 landed round 62 (S277 current, opened live); GR1-GR3 of the scrub entry remain pending behind the operator-gated cohort resume; no ordinal move. | round 4; round-62 entry added, ordinal unchanged |
| coverage | 9 | the corpus README Coverage map carries the Windows-host transition rows through r61 (9 rows; `grep -c 'knowledge/windows-' corpus/README.md` → 9); the r53 map row's Note cell now names the sibling drift note (the r61 closure's defect 3, repaired `f47bb0aa`); PROVINCE Core, Frontier and Adjacent sections unchanged (blob-identical to base). | round 11; round-62 map-row repair, ordinal unchanged |
| operability | 9 | `python tools/check-cited-receipts-r62.py --selftest` → PASS 4 cases rc 0; the gate re-derives the class at `52d9ba1a` (FAIL 3) and passes at this round's trees (`--round 61` and `--round 62` PASS 0); `python tools/receipt-run.py --selftest` PASS 7/7; `python tools/receipt-write.py --selftest` PASS 5/5; `python tools/append-receipt.py --selftest` PASS 5/5; `py_compile` rc 0; registry-coverage 99/99/0; knowledge-header 78/0/78. | round 11; round-62 cited-receipts gate added, ordinal unchanged |
| freshness | 9 | S277 opened live this round; the new pagefile note carries its own 30d cadence (day 0 2026-11-01, due 2026-12-01); the three planes' cadence pass (services T, eventlog E, task-status J, registry R) still due 2026-11-30 (the r60/r61 receipts' `due=` anchors — not due today); the DQ rows' 2026-11-30 pass now has its committed comparison base (the carry-in's twelve receipts); sources census exit 0 at round start (42 W04, 0 E-code) and at round end (receipt with the final commit). | fleet round 1; round-62 pagefile cadence + committed DQ base added, ordinal unchanged |
| calibration | 9 | the axes table restated to counts recomputed on this host; SCORECARD uniqueness gate ok; three mistakes self-caught and mined with evidence (R62-RECEIPT-RUN-SPAWN-FAIL — pf7 meta-receipt; R62-BATCH-DEADLOCK — scratch-draft timeout before landing; R62-RECEIPT-RUN-TMP-PATH — the failed immediate read), none after an outcome cited them; the gate's honest reach stated (the r59 scratch-retained occurrence named as invisible to it); `python tools/check-self-assessment.py` cannot evaluate here (K13, named limit). | round 10; round-62 three-catch set added, ordinal unchanged |
| adjacency | 8 | formal overlap table present; no sibling scope touched; the pagefile plane stays inside the lane's own host-operability province with the ADJ-04 boundary WRITTEN INTO the note (pressure attribution is mori's; PF5's counters are captures, never judged); `wmic` absence and the CIM legs name no sibling surface; contested kaidoku/revenger ownership remains unruled (carried, routed around). | fleet round 1; round-62 ADJ-04 boundary restated in the new note, ordinal unchanged |


- **planned (next round):** operator-gated first — the L0 wave-dispatch question (`tsukuroi | round-53`)
  still decides the r52 counted-cohort depth resume, the L0 `tsukuroi | round-57` decides the S266
  `type= interact` falsification probe, and `tsukuroi | round-60` decides whether the hyaku closure
  judge's spot-checks may discharge the whole-SKILL SHONEN boxes. Lane-owned, not gated: (1) the
  R62-RECEIPT-RUN-SPAWN-FAIL proper fix — receipt-run catches child-spawn failure into its documented
  exit map (receipted could-not-evaluate, no traceback) plus the selftest case; (2) the 2026-11-30
  cadence pass (services T-rows, eventlog E-rows, task-status J-rows, registry R-rows) and the
  pagefile note's own 2026-12-01 pass, each through their `--due` anchors; (3) the DQ plane joins the
  executable-recheck discipline only if a DQ-probe drift fires (the r59 planned-item pattern); (4)
  S277 re-open at 180d or on upstream change; (5) candidate next plane: a Windows power/battery
  CONFIG read (`powercfg /q` scheme/substring read-only legs) or the boot-configuration store
  (`bcdedit /enum` read-only), SOURCED, with the MSYS boundary re-armed for its forward-slash flags.
  If the lane stays on this host, none of the operator-gated items move; the lane-owned list is the
  round-63 menu.


## Round 63 â declaration (2026-11-01, base 74f9846a + carry-in caeccef4, written before any after-measurement)

Carry-ins landed first (LOG 'Round 63 â carry-in'): the D1-D12 precision one-cell repair, the
junction-layout naming + byte-identity receipt, the spawn-crash before-state re-derived. FRESH-START
r50/r51/r52 re-spot-checked at the base (receipt .ufo/waves/round-63/before/freshstart-spotcheck.txt:
r50 FAIL verdicts_ok 0 / marks_ok 0 / seats_ok 18; r51 evidence 0 bytes; r52 FAIL 1/0/16) â the
rendered prompt's FRESH-START framing names these as the last three closures; rounds 53-62 have since
been admitted, the framing is stale, and the spot-checks are re-derived anyway with the same move
classes ruled out (see the LOG declaration entry). S278 was opened live BEFORE this text (fetched
2026-11-01: verbatim lede, option table, /query syntax, overlay three-arg form, frontmatter ms.date
2017-10-27). Claims, each causally separable:

- **C1 operability** â tools/receipt-run.py child-spawn failure joins the documented exit map as a
  RECEIPTED could-not-evaluate (the R62-RECEIPT-RUN-SPAWN-FAIL proper fix, the r62 routed planned
  item). Before (re-derived at caeccef4, live): bare absent-executable spawn crashes unhandled
  (FileNotFoundError traceback at CreateProcess), tool exit rc 1 (the map reserves 1 for budget
  expiry), NO receipt written â .ufo/waves/round-63/before/spawn-crash-repro.txt ends
  receipt-run-rc=1 and the named receipt is proven absent. After (declared predicate): the same
  probe exits rc 2 and WRITES a receipt whose header carries rc=spawn-error + spawn_error=1 with the
  OSError text in the stderr section; run_command returns a spawn sentinel, build_receipt gains the
  conditional spawn_error=1 line, execute maps the sentinel to 2; the selftest gains a case
  (spawn-failure-receipted; call-sites 7 -> 8) and prints RECEIPT_RUN_SELFTEST: PASS (8 cases);
  py_compile rc 0; the SKILL registry row superseded with the extended map (extended text occurs
  exactly once â the operative round-63 table; historical tables keep their bytes).
- **C2 depth (lowest tied axis, 8; SOURCED)** â the Windows power-scheme CONFIG read plane,
  corpus/knowledge/windows-power-config-plane-r63.md rows PW1-PW6, per S278 (Microsoft Learn,
  powercfg command-line options, opened live this round): PW1 active-scheme identity; PW2 scheme
  inventory; PW3 available-sleep-states (measured: NO sleep state available on this host, per-state
  reasons); PW4/PW4b/PW4c the idle-threshold decision table (STANDBYIDLE / HIBERNATEIDLE / DISKIDLE:
  units Seconds, min 0x0, max 0xffffffff, increment 1, AC/DC indices); PW5/PW5b/PW5c the MSYS
  slash-flag boundary (/list mangled to a Git-root path rc 1, /a to A:/ rc 1, dash aliases rc 0,
  MSYS_NO_PATHCONV=1 restores the slash form rc 0); PW6 the alias inventory (33 rows; the page
  documents the /aliases command but no names). Predicate: rows >= 4, SOURCES 277 -> 278 with S278
  at id position directly after S277 (NF 13), knowledge-header gate PASS at the work revision, depth
  ordinal unchanged.

No exploratory claim this round. Two genuine verified claims beat a third manufactured one; the
r62 planned menu's remaining lane-owned items are cadence-anchored and not due (2026-11-30 services/
eventlog/task-status/registry passes; 2026-12-01 pagefile note pass; S277 re-open at 180d) or
conditional on absent triggers (DQ executable recheck), so they are routed, not claimed.


## Round 63 — measured outcome (2026-11-01, author-side; non-author closure pending)

Measured at the work tree `82f0e1a9` (declaration `cdfd8b8c`; counting battery
`.ufo/waves/round-63/after/c1-c2-counts-at-work.txt`, plumbing reads of the revision — the worktree
view is untrusted on this host, r56/r57 lesson). Adjacency anchors gate: FAIL at `2ddd5e79` (IN-109 line shifted by the arm), PASS **114/114** at `cecc9e3e` after the re-pin. Gates at the repair revision: knowledge-header PASS
**79 notes / 0 findings / 79 complete** (JSON `.ufo/waves/round-63/after/knowledge-header-at-work.json`,
revision-pinned `82f0e1a9`, the new note listed with no problems); registry-coverage PASS **99 tools /
99 rows / 0 findings** (JSON `.ufo/waves/round-63/after/registry-coverage-at-work.json`); SCORECARD
uniqueness ok rc 0; `RECEIPT_RUN_SELFTEST: PASS (8 cases, 8 passed, 0 failed)`,
`RECEIPT_WRITE_SELFTEST: PASS (5 cases)`, `APPEND_RECEIPT_SELFTEST: PASS (5 cases)` unchanged;
`python -m py_compile` rc 0 across receipt-run/receipt-write/append-receipt/win-host-census-r53; the
SKILL append proven append-only (HEAD bytes a strict byte-prefix of the new file, +73,188 bytes).

| Claim | Before —> after (measured) | Verdict | Axis verdict |
|---|---|---|---|
| C1 operability (the R62-RECEIPT-RUN-SPAWN-FAIL routed fix) | before at `82f0e1a9^` (live repro `.ufo/waves/round-63/before/spawn-crash-repro.txt`; at-base receipt `.ufo/waves/round-63/before/c1-c2-at-base.txt`): bare absent-executable spawn —> unhandled `FileNotFoundError: [WinError 2]` traceback at CreateProcess, tool exit **rc 1** (the map reserves 1 for budget expiry), **NO receipt written** (the named receipt proven absent); `spawn_error` mentions in the tool **0**, selftest call-sites **7**, extended-map text in SKILL **0**. After at `82f0e1a9`: the same probe exits **rc 2** (could-not-evaluate) and WRITES the receipt — header `rc=spawn-error` + `spawn_error=1`, OSError text verbatim in the stderr section (`.ufo/waves/round-63/after/spawn-fail-receipted.txt`, 317 bytes; run receipt `.ufo/waves/round-63/after/c1-after-state.txt`); `RECEIPT_RUN_SELFTEST: PASS (8 cases)` with the new `spawn-failure-receipted` case (call-sites 8); extended-map text exactly **1** occurrence in SKILL.md (the operative round-63 table; the 98 other rows and all historical tables byte-identical) | **PASS measured** | operability unchanged (9, saturated) — the instrument's documented map now covers its observed failure mode; a spawn failure leaves evidence behind |
| C2 depth (lowest tied, 8; SOURCED — S278 opened live 2026-11-01 before the declaration text, disclosed there) | before at `82f0e1a9^`: note cat-file rc **128**; power vocabulary sweep `powercfg|STANDBYIDLE|SCHEME_CURRENT` over `corpus SKILL.md PROVINCE.md tools` **0 files** (rc 1); SOURCES **277**. After at `82f0e1a9`: note `^| PW` row count — **6**; SOURCES 277 —> **278**, S278 at line 287 directly after S277 (286), NF 13, 0 malformed rows, 0 duplicate ids, the insert proven one-row (worktree-minus-S278 sha256 == HEAD blob); the Gate quote `wc -w` — **17 (≤ 25); knowledge-header gate PASS **79/0/79**. Measured signatures (receipts pw1-pw6 via receipt-run): `-getactivescheme` rc 0 (Ultimate Performance, GUID drift-class); `-list` rc 0, 4 schemes + the blank-first-line output shape; `-a` rc 0, 806 bytes, **zero available sleep states** with per-state reason lines; STANDBYIDLE AC `0x00000000` / DC `0x00000258` (=600 s), HIBERNATEIDLE and DISKIDLE AC/DC `0x00000000`, each `Possible Settings units: Seconds`, min `0x0` / max `0xffffffff` / increment `0x1`; the MSYS boundary: bare `/list` arrived as `C:/Program Files/Git/list` rc 1 and bare `/a` as `A:/` rc 1 (the mangled argv visible in the receipts' own `command=` lines; 41-byte `Invalid Parameters -- try "/?" for help` refusal), dash aliases rc 0, `MSYS_NO_PATHCONV=1` restores the slash form rc 0 (806 bytes, shape identical to the dash run); `-aliases` **33** rows (names host-enumerated; the page documents none) | **PASS measured** | depth unchanged (8) — the move is the sourced entry, not the ordinal |

Declared-command notes: both claims' counting commands ran at the work revision on the channels they
name (the battery receipt) — no declared-command FAIL state this round. Carry-ins landed (routed, not
claims): the D1-D12 precision one-cell repair, the junction byte-identity receipt, and the spawn-crash
before-state at `caeccef4`. Three mistakes mined this round (R63-SCRIPT-REWRITE-BLOCK — the SKILL
in-place transform that destroyed the r62 section, reverted before any commit; R63-NONIDEMPOTENT-LANDER
— the doubled S278 insert, removed and proven against HEAD; R63-COUNT-PATTERN-SLOP — over-matching
count patterns, re-taken with exact ones); no-further-mistakes sweep in the lesson. No exploratory
claim this round.

## Axes — current self-assessment (round 63 final measured surface)

Restated 2026-11-01 at the round-63 work tree (counts re-derived with each cell's command; ordinals
unchanged — operability/freshness/calibration/coverage saturated, depth's move is the sourced entry,
adjacency untouched this round).

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 79 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); the sourced power-scheme plane PW1-PW6 landed round 63 (S278 current, opened live); GR1-GR3 of the scrub entry remain pending behind the operator-gated cohort resume; no ordinal move. | round 4; round-63 entry added, ordinal unchanged |
| coverage | 9 | the corpus README Coverage map carries the Windows-host transition rows through r62 (9 rows; `grep -c 'knowledge/windows-' corpus/README.md` —> 9) plus the round-63 precision repair of the r53 map row's Note cell (D1-D12 stated); PROVINCE Core, Frontier and Adjacent sections unchanged (no round-63 writes). | round 11; round-63 map-row precision repair, ordinal unchanged |
| operability | 9 | `python tools/receipt-run.py --selftest` —> PASS 8/8 (the spawn-failure map leg, r63); the live absent-executable probe exits 2 WITH a receipt (`.ufo/waves/round-63/after/spawn-fail-receipted.txt`) where the pre-fix instrument exited 1 with none; `python tools/receipt-write.py --selftest` PASS 5/5; `python tools/append-receipt.py --selftest` PASS 5/5; `python tools/check-cited-receipts-r62.py --selftest` PASS 4/4; `py_compile` rc 0; registry-coverage 99/99/0; knowledge-header 79/0/79. | round 11; round-63 receipt-run spawn-map leg added, ordinal unchanged |
| freshness | 9 | S278 opened live this round; the new power note carries its own 180d cadence (day 0 2026-11-01, due 2027-04-30); the planes' cadence pass (services T, eventlog E, task-status J, registry R) still due 2026-11-30 (not due today), the pagefile note's due 2026-12-01, the drift register's 30d pass due 2026-11-30; the census mirror byte-identity receipted at round start (the junction layout named); sources census exit 0 at round start (42 W04, 0 E-code) and at round end (receipt with the final commit). | fleet round 1; round-63 power cadence + junction byte-identity receipt added, ordinal unchanged |
| calibration | 9 | the axes table restated to counts recomputed on this host; SCORECARD uniqueness gate ok; three mistakes self-caught and mined with evidence (R63-SCRIPT-REWRITE-BLOCK — caught by the script's own post-write check before any commit; R63-NONIDEMPOTENT-LANDER — caught by the immediate duplicate grep; R63-COUNT-PATTERN-SLOP — caught by expect-comment mismatch in the before-receipt), none after an outcome cited them; the destroyed-and-restored SKILL near-miss is disclosed in the lesson, not smoothed. | round 10; round-63 three-catch set added, ordinal unchanged |
| adjacency | 8 | formal overlap table present; no sibling surface touched; the power note restates the ADJ-04 discipline in its scope paragraph (config reads only; attribution stays with its owners); the `powercfg` plane names no sibling surface; contested kaidoku/revenger ownership remains unruled (carried, routed around). | fleet round 1; round-63 ADJ-04 restatement in the new note, ordinal unchanged |


- **planned (next round):** operator-gated first — the L0 wave-dispatch question (`tsukuroi | round-53`)
  still decides the r52 counted-cohort depth resume, the L0 `tsukuroi | round-57` decides the S266
  `type= interact` falsification probe, and `tsukuroi | round-60` decides whether the hyaku closure
  judge's spot-checks may discharge the whole-SKILL SHONEN boxes. Lane-owned, not gated: (1) the
  2026-11-30 cadence pass (services T-rows, eventlog E-rows, task-status J-rows, registry R-rows, the
  drift register's 30d pass) and the pagefile note's own 2026-12-01 pass, each through their due
  anchors; (2) the DQ plane joins the executable-recheck discipline only if a DQ-probe drift fires (the
  r59 planned-item pattern); (3) S277 re-open at 180d (due 2027-04-30, the same day as the power
  note's pass); (4) S278 re-open at 180d or on upstream change; (5) candidate next plane: the
  boot-configuration store (`bcdedit /enum` read-only — likely elevation-gated, which would first
  make it an L0 authorization question) or the Windows Update session plane via read/COM registry legs,
  SOURCED, with the MSYS boundary re-armed per the r63 measured signatures (dash aliases or
  MSYS_NO_PATHCONV=1). If the lane stays on this host, none of the operator-gated items move; the
  lane-owned list is the round-64 menu.


## Round 64 — declaration (2026-11-03, base 44fc183b, written before any after-measurement)

Host transition: run 15 returned the lane to the canonical Linux/omp host; the r53–r63
Windows-era planes stay frozen this round. Round-start conformance sweep: the canonical sources
census exits **rc 1 with 278 E12** — the Windows-era tooling landed CRLF line endings in
`corpus/SOURCES.md` (381/381 lines), `SKILL.md` (5452/5489), `SCORECARD.md` (4654/4701); blob
archaeology pins the origin at round-59 work `2913b75d` (parent `c5a33d08` is 100 % LF). Receipts:
`.ufo/waves/round-64/before/{census-start,crlf-inventory,guard-absent,skill-snapshot-values,c3-note-absent}-receipt.txt`.

| Claim | Axis/type | Before → after (frozen predicate) | Counting command | Kill rule |
|---|---|---|---|---|
| C1 | operability (host-transition gate repair) | census rc 1, E12=278, 0 W04 + guard absent (cat-file rc 128) → census **rc 0, zero E-code** (42 W04 warnings reappear, disclosed), the three files differ from base ONLY by removed CR (`git show <base>:F \| tr -d '\r' \| cmp - F` identical ×3), `python3 tools/check-line-endings-r64.py --selftest` PASS (CRLF-fixture kill + `.ufo/**` allowlist case) and `--check` rc 0, one CR injected in a scratch copy → `--check` non-zero (receipted mutant) | the census command verbatim; the tr-d/cmp triple; the guard selftest/`--check` lines | a content change beyond CR removal is needed → repair wrong, honest stop |
| C2 | freshness (SKILL decision-table snapshot re-measured after the upgrade arc: kernel 7.2.3→7.2.11, mkinitcpio 41.1→42.2, systemd→262, nvidia 610.57.04→615.78.08, sync-db birth 2026-10-11→2026-10-29/11-02) | stored = committed SKILL "Measured 2026-10-14" cells; no drift note (cat-file rc 128) → `corpus/knowledge/host-drift-recheck-r64.md` with `^| DR` rows ≥ 6, each plane/stored(verbatim+anchor)/live/match-or-drift, **≥ 5 rows `drift`**, every live value receipted under `.ufo/waves/round-64/probes/` and committed with-or-before the citing commit (r63 routed defect honored); SKILL dated erratum appended | `grep -c '^| DR' corpus/knowledge/host-drift-recheck-r64.md` ≥ 6; drift-labeled rows ≥ 5 | < 5 drift rows → "no drift found" reported honestly, claim not improved |
| C3 | depth (lowest tied 8; SOURCED — the mkinitcpio-42 on-release watch FIRED, discharged) | note absent (cat-file rc 128); v42.2 notes unopened; installed-hook `/new_root` state unrecorded → `corpus/knowledge/mkinitcpio42-onrelease-r64.md` with `^| MK` rows ≥ 5 (MK1 versions vs r1 pins; MK2 installed-hook residue lines; MK3 prediction state on the current boot; MK4 S002 TPM2 applicability via HOOKS+crypttab, measured; MK5 upstream master vs installed, dated), every row receipted; SOURCES 278 → ≥ 281 (S279 v42.2 release notes tier A docs; S280 supersedes S021 re-pin; S281 supersedes S022 re-pin), S279 directly after S278, NF 13, Gate quotes ≤ 25 words (`wc -w`); knowledge-header gate PASS; README frontier bullet discharge notice appended | `grep -c '^| MK' <note>` ≥ 5; `grep -c '^| S' corpus/SOURCES.md` ≥ 281; header-gate JSON | residue absent or prediction refutes → the note records the refutation; the claim is the sourced measured plane either way |

Ordinals: unchanged this round (saturated axes move at the instrument/entry level); the r62/r63
axes table stays the standing self-assessment until the measured outcome restates it. Assimilation:
the merge package's 147 staged rows start at S200 and collide with the live S200–S278 register —
the §10 id-collision check runs in scratch; mass id drift → L0 question, no adoption this round.
Open L0s (round-53/57/60) stay routed around, never treated as answered.


## Round 64 — measured outcome (2026-11-03, author-side; non-author closure pending)

Measured at the work tree `431f0c9` (declaration `2f3061ef`; counting battery
`.ufo/waves/round-64/after/counting-battery-prework.txt`, gates receipt
`.ufo/waves/round-64/after/gates-at-work-rev.txt` — both committed with the work commit, the r63
routed receipt-discipline defect honored). Gates at the work revision: knowledge-header PASS
**81 notes / 0 findings / 81 complete** (the two new notes listed with no problems);
registry-coverage PASS **100 tools / 100 rows / 0 findings** (the new guard registered in the
round-64 operative registry section); cited-receipts `--round 64` **PASS, 0 findings, 36 cited
paths** (every receipt the round's artifacts cite is in the same tree); scorecard-uniqueness ok;
census validate **rc 0, 0 E-code, 44 W04** (42 pre-existing duplicate-url-across-scope warnings +
2 from C3's re-pin rows, disclosed before landing in the lesson's Gate); guard `--check` PASS 330
files / 0 violations; `git ls-files --eol` = **i/lf w/lf on all three** repaired files (the
durability invariant); `py_compile` rc 0.

| Claim | Before → after (measured) | Verdict | Axis verdict |
|---|---|---|---|
| C1 operability (capability `line-endings-guard` enters the table) | before at `2f3061ef`: census **rc 1, E12=278, 0 W04** (`.ufo/waves/round-64/before/census-start-receipt.txt`); guard absent (cat-file rc 128); the three files CRLF (SOURCES 381/381, SKILL 5452/5489, SCORECARD 4654/4701 lines CR at 44fc183b; 4723/4723 at the fix base — the declaration commit itself added 69 CRLF lines, disclosed R1C1Rev F3). After at `431f0c9`: census **rc 0, 0 E-code, 44 W04**; the three files differ from base ONLY by removed CR (`git show 2f3061ef:F \| tr -d '\r' \| cmp - F` rc 0 ×3; blob stray-CR 0/0/0, size delta == CR count — R1C1Rev's independent byte census); guard `--selftest` **PASS (7 cases, 7 passed, 0 failed)**, `--check` PASS 330/0; the EOF-CR mutant exits 1 naming path/line/offset; the M3/M5 mutants that survived the 5-case selftest are killed by the 7-case one (able-to-fail receipt `after/c1-selftest-coverage-fix.txt`); post-commit `i/lf w/lf` ×3 | improved, author-verified | operability: the lane's executable census gate runs clean on the canonical host again; the repair class is guarded mechanically (ordinal 9 unchanged, saturated) |
| C2 freshness (the SKILL snapshot re-measured) | before at `2f3061ef`: the stored snapshot = committed SKILL bytes ("Measured 2026-10-14", `SKILL.md:44-50`); no drift note (cat-file rc 128). After at `431f0c9`: `corpus/knowledge/host-drift-recheck-r64.md` — **25 DR rows, 20 `drift`, 5 `match`, 0 unknown** (`grep -c '^\| DR'` = 25), every live value receipted (26 receipts under `probes/`, committed with the note); per-plane drift: packages 6/7, systemd 3/4, journal 3/3, drivers 4/4, update-safety 3/6, census rollup 1/1; the SKILL dated erratum appended (points at the note, 30d cadence) | improved, author-verified | freshness: the 20-day-stale snapshot column re-measured with receipts; ordinals unchanged (9, saturated) — the move is the re-verification itself |
| C3 depth (lowest tied axis, 8; SOURCED — S279/S280/S281 opened live 2026-11-03) | before at `2f3061ef`: note absent (cat-file rc 128); v42.2 notes unopened; installed-hook `/new_root` state unrecorded; SOURCES 278. After at `431f0c9`: `corpus/knowledge/mkinitcpio42-onrelease-r64.md` — **6 MK rows** (`grep -c '^\| MK'` = 6), every row receipted (58 mk42 receipts + the labrat report, committed with the note); SOURCES **278 → 281**, S279 at the id position directly after S278 (line 289), NF 13 ×3, 0 malformed, 0 duplicate ids; Gate quotes ≤ 25 words (11/1/3 primary; supporting 14/17/24/7/12/1); R2Sources **ADMIT ×3** (live re-opens, pin freshness, byte-identity, E04-exemption proven both directions); knowledge-header gate PASS; the README round-64 notice appended. **The r1 silent-no-op prediction is REFUTED at mechanism level** (the v42 `new_root → sysroot` compatibility symlink; `hook:14` is the by-design gate on a normal `@` boot) — and the refutation was FIRST recorded at round 17 (`## R17-SYMLINK`, `initramfs-v42-sysroot-recovery.md:83-89`; `corpus/README.md:147-155` superseded the frontier bullet then): the r64 contribution is the post-upgrade measured state, the positive end-to-end emulation, the applicability matrix, and the dated upstream re-pins — disclosed in the note, the README notice, and the lesson (R64-DECLARATION-STALE-PRIOR) | improved (the sourced entry landed), author-verified | depth: the sourced measured plane landed; the ground was r17-held, so the ordinal stays 8 — the move is the entry + re-pins, not new coverage (expansion unchanged) |

Declared-command notes: every counting command ran at the work revision on the channel it names
(the battery + gates receipts); no declared-command FAIL state. Mistakes mined this round (4, all
with committed evidence): R64-CRLF-HOST-DRIFT (+ the three in-wave worktree regressions + the
census default-mode silent-zero finding), R64-DECLARATION-STALE-PRIOR, R64-SELFTEST-COVERAGE-GAP,
R64-JJ-ST-WITHOUT-IGNORE-WC (the L1's own slip, disclosed). No exploratory claim this round.
Assimilation: none from `merge/tsukuroi/` (79 id collisions, L0 `tsukuroi | round-64` filed);
considerthese Counter-attack scoreboard resumed (SKILL.md r64 row, citing
`considerthese/2026-10-26.md` + 2026-11-03).

## Axes — current self-assessment (round 64 final measured surface)

Restated 2026-11-03 at the round-64 work tree (counts re-derived with each cell's command;
ordinals unchanged — operability/freshness/calibration/coverage saturated, depth's move is the
sourced entry on r17-held ground, adjacency untouched this round).

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 81 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); the sourced mkinitcpio-42 plane MK1-MK6 landed round 64 (S279-S281 current, opened live) on ground r17 held — the post-upgrade measured state, the emulation, the applicability matrix, the re-pins; GR1-GR3 of the scrub entry remain pending behind the operator-gated cohort resume; no ordinal move. | round 4; round-64 entry added, ordinal unchanged |
| coverage | 9 | the corpus README Coverage map carries the Windows-host transition rows through r61 plus the round-64 discharge notice on the mkinitcpio frontier bullet; PROVINCE Core, Frontier and Adjacent sections unchanged (no round-64 writes). | round 11; round-64 frontier-bullet notice, ordinal unchanged |
| operability | 9 | `python3 tools/check-line-endings-r64.py --selftest` → PASS 7/7; `--check` → PASS 330/0; the census validate rc 0 (0 E-code, 44 W04) where the round started rc 1 (278 E12); `python tools/receipt-run.py --selftest` PASS 8/8; `python tools/receipt-write.py --selftest` PASS 5/5; `python tools/append-receipt.py --selftest` PASS 5/5; `python tools/check-cited-receipts-r62.py --selftest` PASS 4/4; registry-coverage 100/100/0; knowledge-header 81/0/81. | round 11; round-64 line-endings guard added, ordinal unchanged |
| freshness | 9 | the SKILL decision-table snapshot re-measured with 26 receipts (25 DR rows, 20 drift); S279-S281 opened live this round; the new notes carry their own cadences (drift note 30d due 2026-12-03; mk42 note on-release); the planes' cadence pass (services T, eventlog E, task-status J, registry R) still due 2026-11-30 (not due today); the pagefile note's due 2026-12-01; sources census exit 0 at round end (44 W04, 0 E-code) after the round-start rc 1 repair. | fleet round 1; round-64 snapshot re-measure + new cadences added, ordinal unchanged |
| calibration | 9 | the axes table restated to counts recomputed on this host; SCORECARD uniqueness gate ok; four mistakes self-caught and mined with evidence (the CRLF class with its origin archaeology + the in-wave regressions; the declaration's stale-prior framing — caught in-round by the L1 reading the labrat's precedence note and the README's r17 notice BEFORE the outcome landed; the selftest coverage gap — caught by the mutation battery; the L1's own `jj st` slip — self-disclosed), none after an outcome cited them. | round 10; round-64 four-catch set added, ordinal unchanged |
| adjacency | 8 | formal overlap table present; no sibling surface touched; the mk42 note restates the ADJ-06 (kaidoku/revenger, unresolved) and ADJ-04 (mori) boundaries in its scope paragraph; the drift note routes the oom-kill scopes' attribution to mori; contested kaidoku/revenger ownership remains unruled (carried, routed around). | fleet round 1; round-64 boundary restatements in the two new notes, ordinal unchanged |


- **planned (next round):** operator-gated first — the L0 wave-dispatch question (`tsukuroi | round-53`)
  still decides the r52 counted-cohort depth resume, the L0 `tsukuroi | round-57` decides the S266
  `type= interact` falsification probe, and `tsukuroi | round-60` decides whether the hyaku closure
  judge's spot-checks may discharge the whole-SKILL SHONEN boxes; new this round: `tsukuroi | round-64`
  rules the merge-package id-drift adoption path (79→82 collisions after S279-S281). Lane-owned, not
  gated: (1) the 2026-11-30 cadence pass (services T-rows, eventlog E-rows, task-status J-rows,
  registry R-rows, the drift register's 30d pass) and the pagefile note's 2026-12-01 pass, each
  through their due anchors — the drift note's own 30d pass lands 2026-12-03; (2) the DQ plane joins
  the executable-recheck discipline only if a DQ-probe drift fires; (3) S277/S278 re-opens at 180d
  (due 2027-04-30); (4) S279-S281 re-open on-release (the next mkinitcpio / limine-mkinitcpio-hook /
  plymouth release re-fires the watch — the mk42 note's recheck procedure); (5) the Windows-era
  planes (r53-r63 notes) stay frozen until the lane is dispatched on a Windows host again; their
  cadence passes (2026-11-30) are due regardless of host — an L0 question may be needed if the
  Windows host is unreachable at that date. If the lane stays on this host, the operator-gated items
  do not move; the lane-owned list is the round-65 menu.

## Round 65 — declaration (2026-11-03, base `1bd8e196`, written before any after-measurement)

Lowest non-retired axis: **depth (8, tied with adjacency 8)**; saturation line 9 / window 3
unchanged; none retired; capability `line-endings-guard` entered r64 (inside the stagnation
window), so the nudge does not waive the lowest-axis duty. S282 opened live 2026-11-03 before this
text (r60/r61/r64 disclosure order; receipt `.ufo/waves/round-65/before/s282-open-receipt.txt`).

| # | axis/type | claim | before → after (frozen predicate) | counting command | kill rule |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S282) | `corpus/knowledge/systemd262-uki-pcr-r65.md` — the systemd v262 NvPCR/UKI requirement plane measured against this host's boot chain (rows SY1-SY5: requirement per S282 "Changes in the TPM Subsystem" cross-linked to S279's mkinitcpio-42.2 sentence; host firmware state; host build state; applicability verdict + named falsifier; unknowns) | note absent (cat-file rc 128) + SOURCES 281 → note present, `^| SY` rows ≥ 5, SOURCES ≥ 282 with S282 directly after S281 (NF 13, quote ≤ 25 words), every live value receipted, knowledge-header PASS | `git cat-file -e <rev>:corpus/knowledge/systemd262-uki-pcr-r65.md`; `grep -c '^| SY' <note>`; `grep -cE '^\| S[0-9]{3,}' corpus/SOURCES.md`; the census validate at round end | live-fetch or host-probe contradiction → note states what measured; honest stop |
| C2 | coverage+operability (capability `initramfs-arm`) | `probe_initramfs_arm` + the verdict-neutral `INITRAMFS` line in `tools/tsukuroi-census.sh` — the owned initramfs/boot-recovery surface (fleet r1) gains its census arm; no privilege, no mutation, never rollup/exit input (DRIFT/STORAGE/SCRUB precedent) | `grep -c INITRAMFS` 0 + selftest 168 → label present + selftest ≥ 174 (≥ 6 new hermetic cases) PASS rc 0; live run prints exactly one INITRAMFS line; base rc + existing verdict lines unchanged; registry-coverage + knowledge-header PASS | `grep -c INITRAMFS tools/tsukuroi-census.sh`; `bash tools/tsukuroi-census.sh --selftest` (frozen before: 168 cases) | not hermetic under the existing fixture pattern → honest stop |

Causal separability: C1 touches only its note + its SOURCES row(s) + probe receipts; C2 touches
only the census tool + its selftest cases. Each verifies without the other. Do-nothing controls
receipted at base (`.ufo/waves/round-65/before/absence-controls-receipt.txt`): note cat-file rc
128 / S282 count 0 / INITRAMFS count 0 / selftest 168 — none reaches either target.

Routed repairs this round (not claims): the R64-SPOTCHECK-C1-PROOF re-expression (append-only
erratum; the re-expressed command re-runs green at `431f0c9`), one considerthese proposal mined,
assimilation none (L0 `tsukuroi | round-64` open). Open L0s round-53/57/60 routed around.

## Round 65 — measured outcome (2026-11-03, author-side; non-author closure pending)

Measured at the repair revision `cecc9e3e` (repair commit; counting battery `.ufo/waves/round-65/after/counting-battery-at-repair.txt`; the work-revision pass at `2ddd5e79` is `after/counting-battery-at-work.txt`; earlier battery
`.ufo/waves/round-65/after/counting-battery-at-work.txt`; live census
`.ufo/waves/round-65/after/census-postarm-live.txt`; drift diff
`.ufo/waves/round-65/after/prearm-vs-postarm-live.diff`). Gates at the work revision:
census validate **rc 0, 0 E-code, 44 W04, 282 rows**; knowledge-header **PASS 82/0/82**;
registry-coverage **PASS 100/100/0**; scorecard-unique ok; line-endings check rc 0; selftest
`TSUKUROI_CENSUS_SELFTEST: PASS (177 cases, 177 passed, 0 failed)`.

| Claim | Before → after (measured) | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (lowest tied, 8; SOURCED — S282 opened live 2026-11-03 before the declaration text) | before at `1bd8e196`: note `cat-file` rc **128**; S282 rows **0**; SOURCES **281**. After at `2ddd5e79`: `grep -c '^| SY'` → **5** (SY1-SY5); SOURCES **281 → 282**, S282 at line 292 directly after S281, NF **13**; Gate quote **23** words (`wc -w`); knowledge-header PASS 82/0/82; census validate rc 0, 0 E-code. Predicate met (SY ≥ 5; SOURCES ≥ 282; S282 after S281, NF 13, quote ≤ 25). Applicability measured, not assumed: UKIs boot (limine `protocol: efi` × 6; `ENABLE_UKI=yes` in `/etc/default/limine`), no TPM hardware, no initrd systemd hook, ukify absent → requirement **inert** on this host (SY4); the watch is re-armed by its named falsifiers | improved, author-verified (ordinal unchanged 8) | depth: one sourced entry; the first on-release re-read (v262.1) ran in-round with no change |
| C2 coverage+operability (capability `initramfs-arm`) | before at `1bd8e196`: `grep -c INITRAMFS tools/tsukuroi-census.sh` **0**; selftest **168**; no initramfs plane in the executable census. After at `2ddd5e79`: `grep -c INITRAMFS` **22**; selftest **177** (≥ 174 predicate; 9 new `R65-C2` hermetic cases, `grep -c R65-C2` 13 incl. the A/B neutrality case) PASS rc 0; live run prints **exactly one** `INITRAMFS initramfs-plane mkinitcpio-conf=PRESENT conf_d=4 hooks=12 newroot_latehooks=2 presets=0 ukify=ABSENT unreadable=0`; the verdict-bearing lines are identical to the pre-arm baseline (`DEGRADED (packages=DEGRADED systemd=DEGRADED drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)`, rc 1 both). Neutrality: by construction (the INITRAMFS value is assigned and printed only, never read by the rollup or exit code) and by a selftest A/B on one tree (inputs present vs absent → identical non-INITRAMFS output and exit). Independent double-entry census (L1DoubleCensus): all 7 INITRAMFS fields match a `find`/`stat` ground computed before reading the line (H held) | improved, author-verified | coverage: the initramfs surface now has an executable read; operability: one more runnable arm (verdict-neutral by design) |

Drift disclosure (the critic's predicted false-flag, measured): the pre-arm and post-arm live
outputs differ only in the timestamp and the drivers-plane memory/PSI counters (C4_sweep 222 → 220,
C5_swap_fail, C6_psi_* and C6_avail_kb moved within the minutes between the captures;
`prearm-vs-postarm-live.diff`, 8 lines). No verdict, rc or INITRAMFS-adjacent field changed. The
claim's "existing verdict lines unchanged" clause is read as verdict-line identity, not
byte-identity of host-pressure counters, which are time-varying by design.

Routed repairs (landed in this round, not claims):
- **R64-SPOTCHECK-C1-PROOF** re-expressed — see the erratum block below. Measured at `431f0c9`:
  SOURCES +3/-0, SKILL +120/-1 (EOF artifact), SCORECARD 0/0 (`.ufo/waves/round-65/after/reidentity-at-431f0c9.txt`).
- **considerthese**: "Upstream release watch" (`considerthese/2026-10-24.md:17`) adopted as
  QUALITY criterion **98** (R65-UPSTREAM-WATCH); the sweep found 95 of 281 rows pin an upstream
  version, 212 declare `on-release`, zero executed; the live delta (systemd v262.1, btrfs-progs
  v7.3, Linux 7.2.15, man-pages 6.20) produced one recheck trigger (btrfs-scrub-record-r42.md:184)
  and no rejection.

Learning trends (author-side; non-author spot-check pending):
- **expansion: improved** — the `initramfs-arm` capability enters the table (LEARNING: "a capability
  admitted to SCORECARD.md"); the systemd v262 applicability plane is an admitted entry, although
  its ground (NvPCR/UKI) was touched by r64's installer-side note — stated, not hidden.
- **quality: improved** — the r64 proof wording is corrected by a re-expression that re-runs
  green at the cited revision; criterion 98 turns a proposal into a standing, receipted duty; the
  declaration's "watch fired" framing was not repeated (the on-release re-read ran and changed nothing).
- **discernment: unchanged** — no non-author spot-check has occurred; the attack seats (reviewer,
  critic, mutation-tester) gave verdicts that are evidence, not discernment verdicts.

## Axes — current self-assessment (round 65 final measured surface)

Restated 2026-11-03 at the round-65 work revision (counts re-derived with each cell's command;
ordinals unchanged — operability/freshness/calibration/coverage saturated, depth's move is the
sourced entry, adjacency untouched this round).

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 82 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l`); the sourced systemd v262 applicability plane SY1-SY5 landed round 65 (S282 current, opened live pre-declaration); the mkinitcpio-42 plane (r64) and GR1-GR3 of the scrub entry stay as before; no ordinal move. | round 4; round-65 entry added, ordinal unchanged |
| coverage | 9 | the initramfs surface is now covered by an executable census read (`grep -c INITRAMFS tools/tsukuroi-census.sh` → 22); PROVINCE Core/Frontier/Adjacent unchanged (no round-65 writes). | round 11; round-65 initramfs-arm, ordinal unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` → PASS 177/177 rc 0; live census prints one INITRAMFS line; `python3 tools/check-line-endings-r64.py --check` rc 0; registry-coverage 100/100/0; knowledge-header 82/0/82. | round 11; round-65 initramfs-arm, ordinal unchanged |
| freshness | 9 | S282 re-opened live by three independent seats (sha256 `008e1265…` identical); the upstream sweep re-read the registry's `on-release` pins against live releases (`corpus/lessons/round-65.md`, QUALITY 98); the planes' cadence pass (2026-11-30) still due. | fleet round 1; round-65 on-release re-read + QUALITY 98, ordinal unchanged |
| calibration | 9 | the axes restated to counts recomputed on this host; three mistakes self-caught and mined (R65-SOURCES-INSERT-WRONG-OCCURRENCE, R65-SPEC-SHAPE-DRIFT, R65-LABRAT-ROLE-INVALID) and one draft-verdict-before-probes error (R65-NOTE-VERDICT-BEFORE-PROBES) caught by the declaration's own kill rule. | round 10; round-65 mistake set, ordinal unchanged |
| adjacency | 8 | the C1 note restates the ADJ-06 (kaidoku/revenger) and ADJ-04 (mori) boundaries in its scope paragraph; the C1SiblingScan overlap register is in `.ufo/waves/round-65/drafts/overlap-scan.md` (see the report); contested kaidoku/revenger ownership remains unruled. | fleet round 1; round-65 boundary restatement, ordinal unchanged |

## Capabilities — round 65 entry

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| initramfs-arm | Reports the owned initramfs/boot-recovery surface on the census's verdict-neutral `INITRAMFS` line: mkinitcpio.conf presence, drop-in count, hook count, hooks naming `/new_root`, preset-directory entries, ukify presence and unreadable entries — read-only, no mkinitcpio run, no privilege, never a rollup or exit-code input | `bash tools/tsukuroi-census.sh` → one `INITRAMFS` line (`.ufo/waves/round-65/after/census-postarm-live.txt`); `--selftest` → PASS 177/177 (`.ufo/waves/round-65/after/counting-battery-at-work.txt`); neutrality A/B in the selftest (R65-C2) | round 65 |

## Erratum (round 65) — R64-SPOTCHECK-C1-PROOF: the round-64 C1 identity proof re-expressed

Append-only. Supersedes only the **wording** of the round-64 C1 identity proof in the round-64
"Measured outcome" C1 row (this file, the "Round 64 — measured outcome" section, row C1 — the text
`git show 2f3061ef:F | tr -d '\r' | cmp - F` rc 0 ×3). The normalization fact stands as measured
(stray-CR 381/5452/4723 at `2f3061ef` → 0/0/0 at `431f0c9`; the three files differ from the CR-stripped
base by additions only). The round-64 closure (`corpus/lessons/round-64-verifier-spotcheck.md` §5)
ruled that wording true only against the fix-time worktree: at the cited revision `431f0c9` the
same comparison fails, because that commit also carries the round's additive work.

Re-expressed proof, re-runnable green at the cited revision from committed bytes:

```sh
for F in corpus/SOURCES.md SKILL.md SCORECARD.md; do
  git --no-pager diff --no-index --numstat \
    <(git show 2f3061ef:"$F" | tr -d '\r') <(git show 431f0c9:"$F")
done
# measured 2026-11-03 (host diff is pi-uu-diff, so --numstat via git diff --no-index):
# corpus/SOURCES.md  added=3   removed=0
# SKILL.md           added=120 removed=1  (the -1 is the EOF newline artifact: base's last byte is 0x2e, the removed line equals added line 1)
# SCORECARD.md       added=0   removed=0  (byte-identical)
```

Receipts: `.ufo/waves/round-65/after/reidentity-at-431f0c9.txt`; the wave's independent re-run
`.ufo/waves/round-65/w1-artifacts/E3/routed-repair-receipt.txt` and the attack
`.ufo/waves/round-65/drafts/rev-repair.md` (R2RevRepair: AGREE on command, counts and append-only
safety). The original `cmp -` wording is false at HEAD (rc 1/1/1) and at `431f0c9` (rc 1 for SOURCES
and SKILL); it held only at the fix-time worktree. This erratum does not change the round-64 verdict.


## Round 66 — declaration (2026-11-03, base `c68bfe97`, written before any after-measurement)

Lowest non-retired axis: **depth (8, tied with adjacency 8)**; saturation line 9 / window 3
unchanged; none retired; capability `initramfs-arm` entered r65 (inside the window), so the nudge
does not waive the lowest-axis duty. Two claims on two distinct axes. S283 opened live 2026-11-03
before this text (receipt `.ufo/waves/round-66/before/s283-open-receipt.txt`; the pinned document is
byte-identical to S282's, sha256 `008e1265…`). Do-nothing controls at base:
`.ufo/waves/round-66/before/absence-controls-receipt.txt` (C1 note cat-file rc 128; C2 note rc 128,
`^## Erratum (round 66)` count 0, `2277` present at `adjacency-anchors-r19.md:204`). Census before:
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → rc 0, 0 E-code,
44 W04, 282 rows (`.ufo/waves/round-66/before/census-before-receipt.txt`).

| # | axis/type | claim | before → after (frozen predicate) | counting command | kill rule |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S283) | `corpus/knowledge/systemd262-credentials-boot-policy-r66.md`: the systemd v262 `systemd.credentials_boot_policy=` plane measured against this host. Rows `CB1`–`CB5`: documented mechanism (S283 section "Changes in the system and service manager:"; the four values and the null-key scope); host boot chain (limine `protocol: efi`, UKI presence, stub version); host policy inputs (cmdline token, TPM2 presence, SecureBoot state, each by a no-sudo read); applicability verdict with a named falsifier; unknowns | note absent (cat-file rc 128) and SOURCES 282 → note present, `^\| CB` rows **≥ 5**, SOURCES **≥ 283** with S283 directly after S282 (NF 13, Gate quote ≤ 25 words), every host value receipted, knowledge-header PASS | `git cat-file -e <rev>:corpus/knowledge/systemd262-credentials-boot-policy-r66.md`; `grep -c '^| CB' <note>`; `grep -cE '^\| S[0-9]{3,}' corpus/SOURCES.md`; the census validate and `check-knowledge-header.py` at round end | the option absent from the pinned bytes, or a measured input contradicting the documented semantics → the note states what was measured and the claim stops honestly (no verdict is softened) |
| C2 | adjacency (lowest tied, 8; ceiling read from `AXES.md`: "no formal overlap table") | a **formal, live-verified sibling-ownership table**: `corpus/knowledge/adjacency-recheck-r66.md` with one row per OUT-001…OUT-010 — columns `| AR<n> | OUT-<nnn> | <sibling> | <40-hex live HEAD> | <64-hex blob sha256> | located | <locator> |` — the quote of each `adjacency-anchors-r19.md` anchor located at that sibling's live HEAD; plus an overlap table (ADJ-02 / ADJ-06 / ADJ-04 boundaries for the systemd credential plane, connector-scanned); plus an append-only erratum `## Erratum (round 66)` in `adjacency-anchors-r19.md` superseding the `2277` prose at :204 with the register pin (`found_line` 2822, r65 re-pin) | before: **0** rows with a live-located quote (note absent; erratum 0). After: **located = 10 of 10**, erratum count **1**, `python3 tools/check-adjacency-anchors.py --revision <REV>` PASS | `grep -cE '^\| AR[0-9]+ \| OUT-0[0-9]{2} \| [a-z]+ \| [0-9a-f]{40} \| [0-9a-f]{64} \| located \|' corpus/knowledge/adjacency-recheck-r66.md` → 10; `grep -c '^## Erratum (round 66)' corpus/knowledge/adjacency-anchors-r19.md` → 1; the anchors gate | a sibling HEAD unreadable or a quote unlocated → that row is not `located` and the count is below 10 → the claim stays unverified (never padded, never re-pinned to a convenient quote) |

Causal separability: C1 touches only its note, `corpus/SOURCES.md` (one row) and receipts; C2
touches only its recheck note, the anchors erratum and receipts. Each verifies without the other.
Standing duties this round (not claims): the QUALITY 98 upstream-release watch re-read (receipts);
the r65 routed defect 1 (in-place edit of a filed line) mined as a lesson with a sweep that is shown
able to fail (`## Mistakes`, red-before on `1bd8e196..7ab7c876`); the considerthese proposal "Seat-harm
incident log" (`considerthese/2026-10-26.md:19`) adopted as a standing per-round tally in the round
lesson, grounded in `corpus/lessons/round-39.md` R39-SEAT-PKILL, `round-40.md` R40-TMP-MISROOT and
`round-41.md` R41-TMP-MISROOT-REPEAT, all opened this round. Assimilation: none (L0 `tsukuroi |
round-64` and addendum still open; no operator answer in `.ufo/l0-questions.md`). Routed-not-claimed:
the r65 C2 A/B sensitivity demonstration (a calibration move on a saturated axis, not a claim).

## Erratum (round 66) — declaration provenance: the C2 ceiling is not AXES.md text

Append-only. Supersedes only one parenthetical in the round-66 declaration above: the C2 row's
"ceiling read from `AXES.md`: "no formal overlap table"". No AXES.md revision contains that text
(`grep -n overlap /home/vgpnk/Projects/shokunin/AXES.md` → no match; the same grep over the fleet
HEAD and over the historical AXES.md blobs returns nothing). The phrase is this lane's own round-11
ceiling for the adjacency row (`SCORECARD.md:52`). It was superseded from round 25, when the
adjacency row recorded the formal overlap table as present (`PROVINCE.md:44`, the ADJ-01 to ADJ-07
table), and the operative adjacency ceiling is recipient acknowledgement and independent replay
(`SCORECARD.md` adjacency rows, round 65 surface). Source of the correction: critic seat K1Critic
(`.ufo/waves/round-66/drafts/critic-claims.md`, Attack 1 of C2). The C2 predicate, counter, kill rule
and target are unchanged; the claim's verdict is not affected by the provenance text, which named a
ceiling the predicate never counted.

Routed from the same critic seat: the C2 counted half is a live re-verification of already-reported
anchor quotes, which is freshness's own definition ("stale items flagged or fixed"), and the
overlap table is an uncounted adjacency-shaped half. The claim therefore stands with a named limit
and no ordinal move: adjacency stays 8 (see the round-66 measured outcome).

## Round 66 — measured outcome (2026-11-03, author-side; non-author closure pending)

Measured at the work revision `97dba116` (landing commit; receipts `.ufo/waves/round-66/after/`).
Declared before data at `aa75398e`; the frozen predicates, counters and kill rules are unchanged.

| Claim | Before → after (measured) | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (SOURCED — S283) | before at `c68bfe97`: `git cat-file -e` note → rc **128**; SOURCES **282**. After at `97dba116`: note present (rc 0); `grep -c '^| CB'` → **5** (CB1–CB5, no header row); SOURCES **282 → 283**; S283 at `corpus/SOURCES.md:293` directly after S282 (`:292`); `awk -F'|'` NF **13**; Gate quote **18** words (`wc -w`), located by whitespace-normalised match in the pinned body; census validate rc **0**; knowledge-header PASS 84/0/84 | improved (predicate met; author-side) | depth ordinal **8 → 8** — no uplift claimed (lane convention: a sourced entry does not by itself lift the ordinal; `SCORECARD.md:962` precedent) |
| C2 adjacency (live anchors + overlap + erratum) | before at `c68bfe97`: `adjacency-recheck-r66.md` absent (rc **128**); live-located rows **0**; `## Erratum (round 66)` count **0**; `2277` at `adjacency-anchors-r19.md:204`. After at `97dba116`: frozen row-regex count → **10** (`after/gates-at-work.txt`); located **10/10**; live HEAD object existence **10/10** (`after/c2-existence-at-work.txt`); erratum count **1**; `python3 tools/check-adjacency-anchors.py --revision 97dba116` → status **PASS** (`after/adjacency-at-work.json`) | improved (predicate met; author-side) | adjacency ordinal **8 → 8** — the counted half is live re-verification (freshness-shaped), the overlap table is uncounted, and the recorded ceiling (recipient acknowledgement) is untouched (critic K1, `drafts/critic-claims.md`) |

Counting commands (run at `97dba116`; full outputs in `after/gates-at-work.txt`):

```
git cat-file -e 97dba116:corpus/knowledge/systemd262-credentials-boot-policy-r66.md        -> rc 0
git show 97dba116:corpus/knowledge/systemd262-credentials-boot-policy-r66.md | grep -c '^| CB'  -> 5
git show 97dba116:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3,}'                              -> 283
git show 97dba116:corpus/SOURCES.md | awk -F'|' '/^\| S283 /{print NF}'                        -> 13
git show 97dba116:corpus/knowledge/adjacency-recheck-r66.md | grep -cE '^\| AR[0-9]+ \| OUT-0[0-9]{2} \| [a-z]+ \| [0-9a-f]{40} \| [0-9a-f]{64} \| located \|' -> 10
git show 97dba116:corpus/knowledge/adjacency-anchors-r19.md | grep -c '^## Erratum (round 66)'  -> 1
git -C /home/vgpnk/Projects/shokunin/<sib>-shokunin cat-file -e <HEAD>^{commit}  (10 rows)    -> 10 of 10 rc 0
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi               -> rc 0, E 0, W04 44 -> 45 (the S283 cross-scope duplicate URL)
python3 tools/check-knowledge-header.py --revision 97dba116                                     -> PASS 84/0/84, findings 0
python3 tools/check-registry-coverage.py --revision 97dba116                                    -> PASS 100/100/0
python3 tools/check-line-endings-r64.py --check                                                 -> rc 0
```

Named limits, carried into the closure (none is a harm; each is recorded, not smoothed):

- **C2 counter shape-only (R66-M3).** The frozen row regex counts a row whose 40-hex HEAD names no
  commit (mutant C2-c → 10, rc 0). The object-existence check above was run as **verification of the
  same "live HEAD" predicate**; it is not an amendment of the counter. The resolve-then-count pipeline
  that kills the mutant is proposed for the next round as a frozen-counter amendment
  (`.ufo/waves/round-66/drafts/mutation-battery.md` §6).
- **C1 counter prefix match (R66-M4).** `^| CB` counts any line that begins `| CB`; the note has no header
  row, so 5 means five rows. Amendment proposed: `^\| CB[0-9]+ \|`.
- **C1 sourcing is not counted (critic K1, C1 Attack 2).** The knowledge-header gate checks that
  `source:` is present, not that it names a registered row; a sourceless note with five CB rows
  fails the header gate, but a note with `source: S999` passes it. Sourcing rests on the receipts.
- **C1 ground is not new.** `git grep -c credentials_boot c68bfe97 -- corpus` → one file
  (`corpus/knowledge/systemd262-uki-pcr-r65.md:24`, SY5 unknown). This round takes that unknown forward
  into a dedicated sourced entry; it is not uncovered ground.
- **Host applicability is measured, not decided.** CB4 reads the option as inert on this host (no cmdline
  token; default `relaxed` governs; SecureBoot disabled and no TPM2 device, so the default accept
  condition holds). The UKI interior and the boot partition stay unread (`/boot` is `fmask=0077`; CB5).

Capabilities: none entered this round. The round's outputs are knowledge entries and a live table; no
repertoire row is demonstrated beyond them.

Ordinals: depth **8**, coverage **9**, operability **9**, freshness **9**, calibration **9**, adjacency **8**
— unchanged. Calibration is recorded, not rescored: one declaration-provenance miss (R66-M2, the false
AXES.md attribution, corrected by the erratum above) was caught by a critic seat, not by the lane.
Saturation line **9** and window **3** are unchanged; none retired. The lowest-axis duty is met by both
claims (both on the tied-lowest axes, depth and adjacency at 8).

Learning trends (author-side; a non-author spot-check is pending and owed by the closure judge):
**expansion: improved** — one sourced entry promotes a named unknown (SY5) into a dedicated entry; the
adjacency table is re-verification, not expansion. **quality: improved** — ten anchors re-located at
live HEADs with an existence check, and the stale `2277` cell is superseded by an appended erratum with
no admitted entry failing. **discernment: unchanged** — no non-author spot-check has run; seat attacks
are evidence, not discernment verdicts.

Routed, not claimed: the r65 C2 A/B sensitivity demonstration (calibration on a saturated axis); the two
frozen-counter amendments above; the adjacency-recheck §4 display cell (sentinel observation #5, one
leading space in a backtick cell; no predicate reads it).

## Round 67 — declaration (2026-11-03, base `5abc31d9`, written before any after-measurement)

Lowest non-retired axis: **depth (8, tied with adjacency 8)**; saturation line 9 / window 3 unchanged;
none retired; capability `initramfs-arm` entered r65 (inside the window), so the nudge does not waive
the lowest-axis duty. Two claims on two distinct axes (depth; calibration). Pre-declaration receipts,
disclosed in order: the btrfs-progs v7.3 `scrub.c` and `CHANGES` were fetched and read by the L1 before
this text (`.ufo/waves/round-67/before/src/{FETCH.txt,SHA256SUMS,TAG.txt}`; the QUALITY 98 watch fired on
btrfs-progs 7.3, installed host 7.1-1); the round-66 frozen counters were run against fixtures as
do-nothing controls (`/fast/scratch/hyaku/tsukuroi-r67/l1/controls`, not committed evidence).

| # | axis/type | claim | before → after (frozen predicate) | counting command | kill rule |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S284, S285) | `corpus/knowledge/btrfs-scrub-limit-revert-r67.md`: the btrfs-progs v7.3 change that moves the per-device scrub-limit revert from inside the per-device result loop (v7.1 `scrub.c:1597-1604`) to a loop after all devices finish (v7.3 `scrub.c:1640-1649`), its CHANGES line, the v7.1 bytes it replaces, and this host's applicability (one device, `scrub_speed_max` 0). Rows `SL1`–`SL4` (≥4) | note absent (`git cat-file -e 5abc31d9:…` rc 128) and SOURCES **283** → note present; `grep -cE '^\| SL[0-9]+ \|'` **≥ 4**; `corpus/SOURCES.md` rows **≥ 284** with S284 on the line directly after S283, `awk -F'|' NF == 13`; Gate quote ≤ 25 words; S285 (CHANGES) may follow | `git cat-file -e <rev>:corpus/knowledge/btrfs-scrub-limit-revert-r67.md`; `git show <rev>:corpus/knowledge/btrfs-scrub-limit-revert-r67.md \| grep -cE '^\| SL[0-9]+ \|'`; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3,}'`; the S284 line-number awk check; census validate at round end | the v7.3 revert-after-all-devices block is absent from the re-fetched bytes (sha256 or line mismatch) → honest stop, no row lands |
| C2 | calibration (9; overreach caught) | `tools/check-adjacency-anchors.py`: a register record whose `sibling_commit` does not resolve in its sibling repo is **silently uncounted** (`_live_object_hash` returns None; no finding; `status` stays PASS). Fix: an `ANCHOR-LIVE-OBJECT-UNRESOLVED` finding that makes the gate FAIL, plus one selftest case | before (base `5abc31d9`, sandbox mutant with one fabricated 40-hex `sibling_commit` and matching published digest, `--siblings-root /home/vgpnk/Projects/shokunin`): **status PASS, live_object_checked 9 of 10** → after (patched tool, same mutant): **status FAIL with finding ANCHOR-LIVE-OBJECT-UNRESOLVED**; honest base still **PASS, live_object_checked 10 of 10**; `--selftest` passes with the new case | `python3 tools/check-adjacency-anchors.py --revision <sandbox-rev> --siblings-root /home/vgpnk/Projects/shokunin` (sandbox = `git clone --shared` in scratch; the patched tool is run from the draft path against the sandbox); `… --selftest` | the honest 10/10 base regresses to FAIL, or the new finding fires on a repo that is absent rather than a commit that does not resolve (false positive) → honest stop |

Causal separability: C1 touches only its note, its SOURCES rows and receipts; C2 touches only the
gate tool, its selftest and receipts. Each verifies without the other. Do-nothing controls at base:
C1 note cat-file rc 128, SOURCES 283; C2 base gate on the honest register PASS 10/10 (a do-nothing
tool leaves the mutant PASS, which is the "before" of C2 by measurement, not assertion).

Standing duties this round (not claims): the QUALITY 98 watch re-read for the btrfs scrub entries
(r42/r43) recorded in the lesson Gate; the round-66 routed frozen-counter defect R66-M4 (header-row
`^| CB` inflation) measured on a fixture and, if it kills, carried as the C1 counter's next amendment;
a mistake mined from this round. Assimilation: none (L0 `tsukuroi | round-64` and addendum still open;
no operator answer in `.ufo/l0-questions.md`). considerthese: see the report's Sources & frontier.

Wave w1 (one v1 wave, 11 seats: scout 1, scribe 1, executor 3, connector 1, reviewer 2, critic 1,
mutation-tester 1, sentinel 1; attack share 4/11) spec frozen at `.ufo/waves/round-67/w1-spec.json`.

## Round 67 — measured outcome (2026-11-03; author-side, measured at landing `f9fa49b8`; non-author closure pending)

Declared before data at `071a55c9`; predicates, counters and kill rules unchanged. Work commit `f9fa49b8`
(landing), measured outcome in the commit that adds this block. Wave w1: 11 seats, 0 dead (`w1-results.json`).

| Claim | Before (base `5abc31d9`) → after (`f9fa49b8`), measured | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (SOURCED — S284, S285) | `git cat-file -e 5abc31d9:corpus/knowledge/btrfs-scrub-limit-revert-r67.md` rc **128** → `git cat-file -e f9fa49b8:…` rc **0**; `git show f9fa49b8:corpus/knowledge/btrfs-scrub-limit-revert-r67.md \| grep -cE '^\| SL[0-9]+ \|'` **0 → 4**; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3,}'` **283 → 285**; S284 at `corpus/SOURCES.md:294` directly after S283 (`:293`); `awk -F'|' '/^\| S28[45] /{print NF}'` → **13, 13**; Gate quote **8 words** (`/* Revert to the older scrub limits. */`) and **12 words** (CHANGES:20) | improved (predicate met; author-side) | depth ordinal **8 → 8** (lane convention: a sourced entry does not by itself lift the ordinal) |
| C2 calibration (overreach caught) | sandbox mutant (one fabricated 40-hex `sibling_commit`): base tool **status PASS, live_object_checked 9 of 10** (`probes/e2-mutant-base.json`; battery `probes/e3-battery-base.tsv` M1 PASS). After (patched tool, same mutant): **status FAIL, finding `ANCHOR-LIVE-OBJECT-UNRESOLVED`** (`probes/e2-mutant-patched.json`; battery `probes/e3-battery-patched.tsv` M1 FAIL). Honest base `5abc31d9`: **PASS 10/10** before and after (`probes/e2-honest-base.json`, `final-adjacency-landed.json` at `f9fa49b8`: PASS, live 10, match 10, findings []). Absent sibling directory (battery M4): **PASS, no new finding** (`probes/e2-absent-sibling.json`). Selftest **25/25 → 26/26** (`probes/e2-selftest.txt`) | improved (predicate met) | calibration ordinal **9 → 9** |

Counting commands (run at `f9fa49b8`; outputs in the probe receipts):

```
git cat-file -e f9fa49b8:corpus/knowledge/btrfs-scrub-limit-revert-r67.md        -> rc 0
git show f9fa49b8:corpus/knowledge/btrfs-scrub-limit-revert-r67.md | grep -cE '^\| SL[0-9]+ \|'   -> 4
git show f9fa49b8:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3,}'                                   -> 285
python3 tools/check-adjacency-anchors.py --revision f9fa49b8… --siblings-root /home/vgpnk/Projects/shokunin  -> PASS, live 10/10, rc 0
python3 tools/check-adjacency-anchors.py --selftest                                              -> PASS (26 cases), rc 0
python3 tools/check-knowledge-header.py --revision f9fa49b8…                                      -> PASS, rc 0
python3 tools/check-registry-coverage.py --revision f9fa49b8…                                     -> PASS 100/100/0, rc 0
python3 tools/check-line-endings-r64.py --check                                                   -> PASS 340/0, rc 0
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi                  -> rc 0, W04 45 (unchanged from round 66)
```

Named limits (recorded, not smoothed):

- **C1 counter is shape-only (R67-COUNTER-SHAPE-ONLY).** The frozen SL predicate passes fixtures with duplicate ids,
  a fenced-block row, a prose row and empty evidence cells (M1 battery: 4 of 5 survive the frozen counter). The
  strict counter in the same battery kills all five with the control passing. R1Reviewer verdict FAILS (controls B
  and C pass); K1Critic FALSIFIES A1 (a wrong-URL S284 row satisfies the predicate). The landed rows are real and
  verified by S1Scout (ALL_MATCH), so the verdict rests on the located bytes, not on the counter. Routed: the strict
  counter is the next frozen-counter amendment, declared before data.
- **C1 anchor coverage.** SL1 cites v7.3 lines outside S284's registered 1640-1649 range; SL2 cites v7.1 lines outside
  S237's registered ranges. Pinned bytes match; registry rows are append-only (CORPUS.md rule 2), so the citations are
  named in the note's Limits rather than absorbed into the rows.
- **C2 environment limit.** A depth-1 shallow clone of a sibling trips the new finding on an honest pinned commit
  (`R2Reviewer-c2-attack.md`, SHALLOW_TRIPS yes). The canonical fleet checkouts are full (10/10 resolve). The gate
  reports the environment rather than passing it.
- **C2 scope.** The finding covers an unresolved `sibling_commit` in an existing sibling directory only. An abbreviated
  or uppercase commit is handled by existing checks (M2 already FAILs via OUTBOUND-FIELDS; M3 resolves case-insensitively
  and passes).

Ordinals unchanged: depth **8**, coverage **9**, operability **9**, freshness **9**, calibration **9**, adjacency **8**.
Saturation line **9**, window **3**; none retired. Lowest-axis duty met by C1 (depth, tied lowest at 8).
Capabilities: none entered this round (the outputs are a sourced entry and a gate finding, not a new repertoire row).

Learning trends (author-side; non-author verdict owed by the closure judge): **expansion: improved** — one sourced entry
on uncovered ground (S284/S285, `mined`). **quality: improved** — the adjacency gate fails an unresolvable commit
instead of silently uncounting it (QUALITY 100); the r42/r43 scrub notes were re-read against the v7.3 bytes and
nothing in them is contradicted. **discernment: unchanged** — the attack seats found the C1 counter gap; the lane did not
catch it at write time; the gap is named and routed, not closed.

Routed, not claimed: the strict-counter amendment for the C1 SL predicate; the round-66 counter amendments (AR
resolve-then-count, CB header-row `^\| CB[0-9]+ \|`); the `source:`-value gate gap (K1 C1 Attack 2); the adjacency-recheck
§4 display cell; the r65 C2 A/B demonstration; L0 `tsukuroi | round-64` id-drift (open, unanswered; nothing adopted from
`merge/tsukuroi/`).
## Round 68 — declaration (2026-11-03, base `42400ec6`, written before any after-measurement)

Lowest non-retired axis: **depth (8, tied with adjacency 8)**; saturation line 9 / window 3 unchanged;
none retired. Capability `initramfs-arm` entered r65; r66 and r67 entered none, so the window is at 2 of 3
and the nudge does not waive the lowest-axis duty. Two claims on two distinct axes (depth; operability).

Pre-declaration receipts, disclosed in order: the QUALITY 98 upstream-release watch fired on Linux v7.3
before this text. The L1 fetched the v7.2 and v7.3 bytes of the four v7.2-pinned files and computed their
sha256s (`.ufo/waves/round-68/before/src/{FETCH.txt,SHA256SUMS}`; host state `before/host.txt`). Verdicts
on the five v7.2-pinned registry rows: S138 CHANGED (`a9433bb0…` → `2750c11a…`); S158 CHANGED (`ce146120…`
→ `098cb522…`); S149 and S182 UNCHANGED (`452f1348…` identical); S185 UNCHANGED (`11c6b712…` identical; row
stays `rejected`). Anchor spot-checks: the three S138 anchor quotes are byte-identical in v7.3 at drifted
lines (memory.events 1468 → 1495; oom_kill 1507 → 1533; memory.events.local 1517 → 1544); the S158 v7.3
diff is one comment-only hunk at `:1339`. Census before: rc 0, 0 E-code, 45 W04, 285 rows
(`before/census-before-receipt.txt`). Do-nothing controls at base: note cat-file rc 128; tool cat-file rc 128;
S286/S287 rows 0 (`before/absence-controls-receipt.txt`). C2 live-corpus pre-scan at base: 85 notes, 285
registry ids, 0 dangling operative `source:` S-refs.

| # | axis/type | claim | before → after (frozen predicate) | counting command | kill rule |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S286, S287) | `corpus/knowledge/linux-v73-pinwatch-r68.md`: the QUALITY 98 watch fired on Linux v7.3. The five v7.2-pinned registry rows are re-read against v7.3 bytes, each with a verdict, a located v7.3 anchor and an applicability line; S286 (cgroup-v2.rst @ v7.3) and S287 (fs/btrfs/sysfs.c @ v7.3) are opened as reference rows; the registry rows are never edited in place. Rows `RW1`–`RW6` (≥ 6): RW1 S138 changed (sha pair; memory anchors byte-identical at drifted lines; the changed hunks named and shown outside the memory-controller section); RW2 S158 changed (sha pair; comment-only hunk; registered anchor lines intact); RW3 S149 unchanged; RW4 S182 unchanged (same bytes as S149); RW5 S185 unchanged, stays rejected; RW6 host applicability (installed `linux 7.2.11.arch1-1`; v7.3 not installed, so the v7.2 reference rows stay host-correct; named falsifier: `uname -r` ≥ 7.3 re-opens the rows) | note absent (`git cat-file -e 42400ec6…:corpus/knowledge/linux-v73-pinwatch-r68.md` rc 128) and SOURCES **285** → note present; `grep -cE '^\| RW[0-9]+ \|'` **≥ 6**; SOURCES **≥ 287** with S286 directly after S285 and S287 directly after S286; `awk -F'|' 'NF==13'` on both new rows; each Gate quote ≤ 25 words; receipt `before/src/SHA256SUMS` committed; knowledge-header PASS; census validate rc 0 at round end | `git cat-file -e <rev>:corpus/knowledge/linux-v73-pinwatch-r68.md`; `git show <rev>:corpus/knowledge/linux-v73-pinwatch-r68.md \| grep -cE '^\| RW[0-9]+ \| '`; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3,}'`; `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | any do-nothing control reaches the after-state, or a sha pair does not reproduce → honest stop |
| C2 | operability (9; capability `knowledge-source-ref-gate`) | `tools/check-knowledge-refs-r68.py`: the round-66 routed gap (K1 C1 Attack 2). `tools/check-knowledge-header.py` checks `source:` presence, never that the cited S-ids exist, so `source: S999 …` passes. The new gate reads every `corpus/knowledge/*.md` at `--revision` with the header gate's binding and fence rules, extracts the `S\d{3,}` ids on the operative `source:` line, and reports `KNOWLEDGE-REF-DANGLING` for any id absent from `corpus/SOURCES.md` at that revision. Hermetic `--selftest` with ≥ 8 cases including red cases (dangling id; id only inside a fence ignored; mid-sentence mention ignored; well-formed control passes) | tool absent (`git cat-file -e` rc 128) → tool present; `--selftest` PASS rc 0; on a fixture note citing `source: S999`: header gate rc 0 (passes) and new gate rc 1 with finding `KNOWLEDGE-REF-DANGLING`; live corpus at the work revision: rc 0, 0 findings | `git cat-file -e <rev>:tools/check-knowledge-refs-r68.py`; `python3 tools/check-knowledge-refs-r68.py --selftest`; both gates on the S999 fixture; `python3 tools/check-knowledge-refs-r68.py --revision <rev>` | any live-corpus false positive not repairable in-round → honest stop |

Causal separability: C1 touches only its note, its two SOURCES rows and receipts; C2 touches only the new
tool, its selftest fixtures, its registry row (`SKILL.md`, QUALITY 70) and receipts. Each verifies without
the other. Counter strictness: both new table-row predicates are strict from the start (distinct ids, a
non-empty evidence cell, no fenced-block or prose row). The R67-COUNTER-SHAPE-ONLY strict battery (header-only,
duplicate-id, fenced-row, prose-row, empty-evidence fixtures plus a well-formed control) is committed under
`probes/` before any note exists. Routed and not counted this round: R66-M3 (AR resolve-then-count) and
R66-M4 (CB header-row shape, already answered by the strict regex on the new rows).

Standing duties (not claims): the QUALITY 98 watch re-read (executed; results land in C1); the round-67 routed
defect R67-POSITIVE-CONTROL-COMMAND-MISMATCH is corrected by an appended erratum in the round-68 lesson
(`grep -c -i limit` on r42 prints 14 matching lines; `grep -o -i limit … | wc -l` prints 21 occurrences; the
round-67 Mistakes row cited 21 as a line count); one considerthese proposal mined; assimilation: none (L0
`tsukuroi | round-64` and its addendum remain open and unanswered in `.ufo/l0-questions.md`).

Wave w1: one v1 wave, band 8–16. Seat shape and counts are fixed in `.ufo/waves/round-68/w1-spec.json`.

## Round 68 — declaration errata (append-only; predicate unchanged)

The C1 sentence "changed hunks ... outside the memory-controller section" is
falsified: S1Scout and R1Reviewer measured one of sixteen hunks inside Memory,
changing memory.pressure's documented access mode at v7.3:1939. The declaration's
oom_kill label locator is 1506→1533, not 1507→1533. "The five" means only the five
named rows; R1Reviewer enumerated eleven v7.2-family rows for these files.
The note records the actual scope and the true memory hunk. These corrections do
not amend the frozen content conjunct or its shape-only counting command:
**C1 not verified**. Its row/registry counts remain measurements, not admission.
Evidence: `.ufo/waves/round-68/w1/{S1Scout,R1Reviewer,K1Critic}.md`.

The positive-control erratum lives in `corpus/lessons/round-67.md` as an appended
round-68 block and is mined in `corpus/lessons/round-68.md`; the declaration's
"in the round-68 lesson" wording refers to that mined mistake, not its placement.
The saturation nudge requires all axes saturated, which is false (depth/adjacency
8); a capability is encouraged but not mandated by a three-round window alone.

## Capabilities — round 68 demonstrated entry

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| knowledge-source-ref-gate | Resolves operative source-line S-ids against the same-revision registry; fails dangling references and ignores fenced registry examples | `python3 tools/check-knowledge-refs-r68.py --selftest` PASS 21/21; live base 85 notes/285 ids/0 findings; S999 header PASS/new-gate FAIL in round-68 probes and integration receipts | round 68 |

## Round 68 — measured outcome (2026-11-03, revision `a5fc44a7`)

Declaration `3f6edcc9`; wave w1 settled (WAVE-DONE received), twelve seats, no
reported dead seat; planner held by L1. Role counts: scout2/executor2/scribe2/
connector1/reviewer2/critic1/mutation-tester1/sentinel1; attack 4/12, residual0.

| Claim | Before → after | Verdict |
|---|---|---|
| C1 depth | Base `42400ec6` note absent rc128, SOURCES285; `a5fc44a7` note present, RW6, SOURCES287, S286/S287 adjacent after S285, NF13/13. Strict counter RW_ROWS=6. Eight source digest pairs match; new-row quotes 11/7 words. But the frozen outside-memory conjunct is false: one memory.pressure hunk is inside Memory. | **not verified**, frozen conjunct falsified; no predicate replacement |
| C2 operability / capability | Tool absent → executable gate; selftest21/21 rc0; S999 header PASS/new-gate FAIL. At `a5fc44a7`, gate PASS86 notes/254 refs/287 registry ids/0 findings. | **improved**, author-verified |

Counting commands and digested receipts: `.ufo/waves/round-68/after/`.
`python3 tools/run-receipt.py --revision a5fc44a7 --out <receipt> -- <tool>
--revision a5fc44a7` ran refs, header and registry gates: all rc0; refs-selftest
receipt records21/21. `python3 .ufo/waves/round-68/drafts/c1/count-rw-r68.py
corpus/knowledge/linux-v73-pinwatch-r68.md` → RW_ROWS=6, LAYOUT=8.
Canonical census validate rc0, W04=45, rows287; line-ending guard PASS344/0.
No SHONEN promotion. Ordinals unchanged: depth8, adjacency8, remaining four9.
Expansion improved; quality improved; discernment unchanged (lesson).
Round not admitted author-side because C1 is not verified; operator/closure rules.
Planned: freeze a content-sensitive counter before data, carry S243's stable
watch and R66 AR resolution debt; never alter this round's frozen predicate.

## Round 69 — declaration (2026-11-03, base `acce353b`, written before any after-measurement)

Lowest non-retired axis: **depth (8, tied with adjacency 8)**; saturation line 9 / window 3 unchanged;
none retired. Capability `knowledge-source-ref-gate` entered r68, so the stagnation window is at 1 of 3
and the nudge does not waive the lowest-axis duty. Two claims on two distinct axes (depth; operability).
This round carries the r68 closure routings as work, not as extra claims: the content-sensitive counter is
C1's counting command (R68-SHAPE-ONLY-DECLARED-COUNTER), and the declaration-hygiene criterion is a routed
repair (`corpus/QUALITY.md`, R68 routed item 2).

Pre-declaration receipts, disclosed in order. (a) The two source documents for C1 were fetched and read
before this text and committed as snapshots: Linux v7.2.11 `Documentation/admin-guide/tainted-kernels.rst`
sha256 `727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841` and
`include/linux/vermagic.h` sha256 `0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea`, both
from the stable tree at tag v7.2.11; `sha256sum -c` rc 0 (`.ufo/waves/round-69/before/src/{FETCH.txt,SHA256SUMS}`).
(b) Host capture, read-only (`.ufo/waves/round-69/before/host.txt`): `uname -r` `7.2.11-arch1-1`;
`pacman -Q linux` `7.2.11.arch1-1`; `pacman -Q linux-lts` `6.18.57-2`; `/usr/lib/modules/` holds two trees, each
owned by its package (`pacman -Qo`); `/proc/sys/kernel/tainted` `12288`; the boot's kernel log prints
`Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE`; `modinfo -F vermagic` on the dkms nvidia module
`7.2.11-arch1-1 SMP preempt mod_unload`; `lsmod | wc -l` 132; soft-lockup log lines this boot 0.
(c) QUALITY 98 watch fired on Linux v7.3; S243's v7.2.11 `fs/btrfs/sysfs.c` pin (`ce146120…`) re-read at the
v7.3 stable tag → digest `098cb522…` = **changed**, equal to S287's torvalds-v7.3 pin, the single change being
the comment line outside S243's registered ranges (`.ufo/waves/round-69/before/s243-v73-recheck.txt`).
(d) Canonical census before: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tsukuroi` → rc 0, 287 rows (`.ufo/waves/round-69/before/census-before-receipt.txt`).
(e) Do-nothing controls at base (`before/absence-controls-receipt.txt`): C1 note `cat-file` rc 128; C1 counter
`cat-file` rc 128; `^| KR[0-9]` rows in the tree 0; `grep -c KERNEL tools/tsukuroi-census.sh` 0; selftest
**177** cases; SOURCES 287 rows; S288 and S289 rows 0.

| # | axis/type | claim | before → after (frozen predicate) | counting command | kill rule |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S288, S289) | `corpus/knowledge/kernel-taint-plane-r69.md`: the kernel taint, vermagic and module-tree plane measured against this host, rows `KR1`–`KR5`. Each row is `| KR<n> | <statement, ≥ 12 words> | source=S### | snapshot=<file> | digest=<64-hex> | quote="<text>" |`; the round's **content-sensitive** counter `tools/count-kr-rows-r69.py` is frozen before any note exists and verifies per row: unique id, statement ≥ 12 words, the `source=` id present in `corpus/SOURCES.md` at the measured revision, `digest=` equal to the sha256 of the named committed snapshot under `.ufo/waves/round-69/before/src/`, and `quote=` ≤ 25 words located verbatim in that snapshot | note absent (`git cat-file -e <rev>:corpus/knowledge/kernel-taint-plane-r69.md` rc 128) and counter absent (rc 128), SOURCES **287** → note present at the measured revision, counter present, `KR_ROWS=5 KR_VERIFIED=5` rc 0; `corpus/SOURCES.md` rows **≥ 289** with S288 and S289 on the lines directly after S287, `awk -F'|' '/^\| S28[89] /{print NF}'` = 13, 13; Gate quote ≤ 25 words; knowledge-header gate PASS; canonical census validate rc 0 | `python3 tools/count-kr-rows-r69.py --revision <rev> --snapshots .ufo/waves/round-69/before/src` (print `KR_ROWS` / `KR_VERIFIED`); `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3,}'` | any row failing one clause reads `KR_VERIFIED < 5` → honest stop; the counter's pre-data battery must fail all five malformed fixtures (duplicate id, wrong digest, absent quote, unregistered source id, 7-word statement) while the well-formed control reads 5 — a battery that passes any malformed fixture makes the counter vacuous and C1 is not declared verified |
| C2 | operability (9; capability `kernel-arm`) | `probe_kernel_arm` + one verdict-neutral `KERNEL` line in `tools/tsukuroi-census.sh`: `KERNEL kernel-plane release=<uts> pkg=<name> pkgver=<ver> modules_tree=PRESENT\|ABSENT\|UNKNOWN tainted=<int\|UNKNOWN> taint_bits=<csv\|none\|UNKNOWN> pending=NO\|YES\|UNKNOWN unreadable=<n> [detail=...]`, decoded with the closed bit→log table 0–19 of S288; read-only, no privilege, no package transaction, never a rollup term and never an exit-code input | `grep -c 'KERNEL' tools/tsukuroi-census.sh` **0**, selftest **177** → label present (`grep -c 'KERNEL kernel-plane'` ≥ 1), selftest **≥ 185** PASS rc 0 with ≥ 8 new `R69-C2` hermetic cases; live run prints exactly one `KERNEL` line carrying every field exactly once in contract order; the verdict-bearing lines and the exit code identical to the pre-arm baseline; knowledge-header, registry-coverage and line-endings gates PASS | `grep -c 'KERNEL kernel-plane' tools/tsukuroi-census.sh`; `bash tools/tsukuroi-census.sh --selftest`; `bash tools/tsukuroi-census.sh 2>/dev/null \| grep -c '^KERNEL kernel-plane'` | not hermetic under the existing fixture/override pattern → honest stop; a field absent, duplicated or out of contract order on the live line → honest stop; any rollup or exit-code change → honest stop |

Causal separability: C1 touches only its note, its two SOURCES rows, the new counter and receipts; C2 touches
only `tools/tsukuroi-census.sh`. Each verifies without the other. Counter strictness is frozen here, before any
note or selftest case exists; both new table-row predicates are strict from the start (distinct ids, non-empty
evidence cells, no fenced-block or prose row). Routed repairs this round (not claims): the declaration-hygiene
criterion in `corpus/QUALITY.md` with a receipt applying it to the round-68 declaration; the QUALITY 98 S243
re-read above; one considerthese proposal mined; assimilation: none (L0 `tsukuroi | round-64` and its addendum
remain open and unanswered in `.ufo/l0-questions.md`).

Wave w1: one v1 wave, band 8–16, 13 seats; seat shape and counts are fixed in `.ufo/waves/round-69/w1-spec.json`.

**planned (next round):** R66-M3/M4 frozen-counter amendments where still reachable; the AR resolve-then-count
debt; the kernel arm's second-device and non-systemd-boot coverage; no amendment of this round's frozen predicates.

## Round 69 — measured outcome (2026-11-03, measured revision `7d7d3aee`; author-side, non-author closure pending)

Declared at `920a9eea`; base `acce353b`; measured surface `7d7d3aeecacd8633537bf68427a24a02534884f4`. Wave w1: one v1 wave, **13 seats, 0 dead** (`w1-results.json`, 13/13 settled); scout2 / executor3 / scribe2 / connector1 / reviewer2 / critic1 / mutation-tester1 / sentinel1; attack seats 4/13 = 31 % (≥ 25 %); connector 1; residual 0; the L1 held the planner seat (not a validator role). Two post-wave repairs landed inside the round (see limits): the `pending` derivation (critic K1 A5) and the taint-input normalization (reviewer R2 HIGH).

| Claim | Before (base `acce353b`) → after (measured revision) | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (SOURCED — S288 re-pin, S289) | note `cat-file` rc **128** → present; counter rc **128** → present; SOURCES **287 → 289**; `KR_ROWS=5 KR_VERIFIED=5` rc **0**; S288/S289 on the lines directly after S287; `awk -F'|'` NF **13/13**; knowledge-header PASS **87/87**, 0 findings; refs **0** dangling; cited-receipts round 69 **PASS**; census validate rc **0**, 289 rows | **verified** on the frozen predicate (author-side) | depth **8 → 8**: one new mechanism (the vermagic composition and its `CONFIG` conditionals) and one host binding (tree ownership; the pending candidate set); the seat draft's duplicate taint rows were restructured so four rows are additive and one states the re-grounding. No ordinal uplift claimed |
| C2 operability (capability `kernel-arm`) | `grep -c KERNEL tools/tsukuroi-census.sh` **0**, selftest **177** → label present (`grep -c 'KERNEL kernel-plane'` **20**), selftest **196** PASS rc **0** (19 `R69-C2` cases); live run prints exactly **1** KERNEL line, every field once in contract order; rollup line and exit code (rc 1) identical to the pre-arm baseline; the live diff is timestamps, time-varying counters and the new line only | **verified** | operability **9 → 9** (no uplift; the capability row enters) |

Counting commands (outputs in `.ufo/waves/round-69/after/gates-final.txt` and `gates-at-final.txt`):

```
python3 tools/count-kr-rows-r69.py --revision 7d7d3aee --snapshots .ufo/waves/round-69/before/src  -> KR_ROWS=5 KR_VERIFIED=5, rc 0
git show 7d7d3aee:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3,}'                                    -> 289
git show 7d7d3aee:corpus/SOURCES.md | awk -F'|' '/^\| S2(87|88|89) /{print $2,NF}'                  -> NF 13, 13, 13
bash tools/tsukuroi-census.sh --selftest                                                            -> PASS (196 cases, 196 passed, 0 failed)
bash tools/tsukuroi-census.sh | grep -c '^KERNEL kernel-plane'                                      -> 1
python3 tools/check-cited-receipts-r62.py --revision 7d7d3aee --round 69                           -> PASS, 0 findings
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi                     -> rc 0, 289 rows
```

**Capabilities — round 69 entry.**

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| kernel-arm | Reports the running kernel's operability state on the census's verdict-neutral `KERNEL kernel-plane` line: release, owning package and version, module-tree state, taint mask decoded through the closed 0–19 table, the reboot-pending candidate set and an unreadable count — read-only, unprivileged, one `pacman -Qo`, never a rollup or exit-code input | `bash tools/tsukuroi-census.sh` → one KERNEL line (`after/census-live-postrepair.txt`); `--selftest` → PASS 196/196 (`after/selftest-taint-repair.txt`) | round 69 |

Named limits, recorded and not smoothed:

- **C1's counter is content-sensitive on its evidence legs, not on its statement** (`K1Critic` A2; `M1Mutation` survivors `m1`, `m6`): a filler statement of ≥ 12 words with a real source/snapshot/digest/quote verifies. The five malformed fixtures (duplicate id, wrong digest, absent quote, unregistered id, 7-word statement) each read below the control's 5 (`probes/E2Counter/battery.txt`); the boilerplate fixture reads 5. Routed: a statement-substance clause is a next-round frozen-counter amendment.
- **C1's counter `source=` clause is membership only** (`K1Critic` A4, fatal as worded): any registered id passes. The landed rows cite S288/S289, and a supplementary binding check (`after/c1-source-binding.txt`) shows each row's source registry row carries that row's digest (`BOUND=5/5`) — verification of the same predicate, never an amendment of it.
- **S288 adds no document content**: byte-identical to S140 (`cmp` rc 0). It is admitted as a re-pin at the running tag, with the reason in its teaches cell; depth credit rests on S289 and the host binding, not on S288.
- **The `pending` derivation was under-specified at freeze**: the seat-item transform read `pending=YES` on the installed `linux-lts` pair (critic K1 A5). Repaired inside the frozen grammar as a candidate set (version, every single-dot rewrite, `<version>-lts`) with an LTS `NO` case and a `YES` case; selftest 192 → 194.
- **The arm's taint input was not bounded** (reviewer R2 HIGH): `08` aborted the census (octal) and a 25-digit value fabricated an all-bits decode. Repaired by stripping leading zeros and refusing values wider than the table before any arithmetic; selftest 194 → 196; live line unchanged.
- **Vermagic coverage is two module files**, not the trees, and no foreign-module load was attempted — the cross-tree incompatibility is [inference] from the header rule plus the observed token identity.

Ordinals unchanged: depth **8**, coverage **9**, operability **9**, freshness **9**, calibration **9**, adjacency **8**. Saturation line **9**, window **3**; none retired. The lowest-axis duty is met by C1 (depth, tied lowest at 8); the round's depth verdict is **unchanged**, reported as such. Learning trends (author-side; a non-author spot-check is owed by the closure judge): **expansion: improved** (S289 on ground never held; S288 a stated re-pin; one entry; capability `kernel-arm`); **quality: improved** (the r68 shape-only counter debt answered by a content-sensitive counter frozen before data; QUALITY 102 and 103; two stale kernel-pairing sentences corrected by appended errata; two attack-found defects repaired in-round); **discernment: unchanged** (the lane declared a novelty it did not have and a wave seat caught it; no outside admit/reject spot-check is recorded here).

Planned (next round): a statement-substance clause for the KR counter and a source-to-snapshot binding clause, both frozen before data; R66-M3/M4 where still reachable; the AR resolve-then-count debt; no amendment of this round's frozen predicates.

## Round 70 — declaration (2026-11-03/04, base `b2aa0be0`, written before any after-measurement)

Lowest non-retired axis: **depth (8, tied with adjacency 8)**; saturation line 9 / window 3 unchanged;
none retired. A capability entered at round 69 (`kernel-arm`), so the stagnation window is at 1 of 3 and
the nudge does not waive the lowest-axis duty. Two claims on two distinct axes (depth; operability).

Pre-declaration receipts, disclosed in order; all under `.ufo/waves/round-70/before/`.
(a) Source snapshots fetched and read before this text, committed byte-exact under `before/src/` with
`SHA256SUMS` (`sha256sum -c` rc 0) and `SOURCES.json` (snapshot → URL, tag, access date, digest):
Linux stable v7.2.11 `Documentation/admin-guide/xfs.rst` sha256 `53bda67b…d051c`,
`fs/xfs/xfs_stats.c` sha256 `4b6a9b6c…9e452`, `fs/xfs/xfs_sysfs.c` sha256 `1cbcffa1…a5805`;
xfsprogs v7.2.0 `spaceman/health.c` sha256 `84fdd0be…15950`. `FETCH.txt` records route 1; a second route
is required from the wave's scout before any row is admitted.
(b) Host capture, read-only (`before/host.txt`, `capture.sh`): the host runs
`7.2.11-arch1-1`, `linux 7.2.11.arch1-1`, `xfsprogs 7.2.0-1`; two xfs filesystems —
`/dev/nvme1n1p1` on `/tmp` and `/dev/nvme1n1p2` on `/fast`; `/sys/fs/xfs/<dev>/{stats,error,log}` present
for both, `stats/stats` 34 lines each and 0444, `stats_clear` 0200 on each and on the global
`/sys/fs/xfs/stats`, `/proc/fs/xfs/stat` a symlink to the global stats file, four log files per filesystem
with `log_head_lsn` `cycle:block`, error subtree 7 regular files per filesystem with `-1` retry values;
`xfs_info` geometry per mount; `xfs_spaceman -c health` prints "Health status has not been collected…" for
both mounts.
(c) Held-ground sweep (`before/novelty-sweep.txt`): 18 xfs lines in `corpus/ SKILL.md PROVINCE.md`, all
peripheral (mount type, package list, a `/tmp` correction); `sys/fs/xfs`, `stats_clear`, `log_head_lsn`,
`reserve_grant_head_bytes`, `fail_at_unmount`, `xfs_spaceman`, `max_retries` each **0** hits at base; no
xfs knowledge note exists (`git ls-tree … | grep -i xfs | wc -l` 0); `storage-health-r26.md` holds SH1-SH6
over btrfs and NVMe SMART only.
(d) Do-nothing controls (`before/absence-controls.txt`, base `b2aa0be0`): C1 note `git cat-file -e` rc
**128**, C1 counter rc **128**, `^| XS[n]` rows **0**, `XFS xfs-stats` label **0**, `probe_xfs` **0**,
selftest **196** PASS rc 0, registry **289** rows, canonical census validate rc 0, 87 knowledge notes.
(e) Frozen counter and its pre-data battery: `tools/count-xs-rows-r70.py` sha256
`65065d9d18cea52027619697264de430780e65ff13ab6da2a790c3d2054f6f5c`; battery
`before/control/battery.txt` (8 cases) — well-formed control reads `XS_ROWS=6 XS_VERIFIED=6
XS_SOURCES=4 XS_SNAPSHOTS=4` rc 0; content-free, any-registered-id, digest-swap, quote-absent,
short-statement, five-row and duplicate-id mutants each read below the target and exit 1.
(f) Base live census (`before/census-live-base.txt`): rollup
`TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=DEGRADED drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)`, rc **1**.

| # | axis/type | claim | before → after (frozen predicate) | counting command | kill rule |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — four new registry rows) | `corpus/knowledge/xfs-storage-plane-r70.md` states the XFS sysfs storage plane the lane never held: the per-filesystem and global stats file, one summary line per named counter group with summed per-CPU counters, the four precision counters, the write-only `stats_clear` contract, the log head/tail LSN and grant-head files, the error-configuration tree with the metadata class, and the online health reader's "not collected" state; rows `XS1`–`XS6`, each `| XS<n> | <statement, ≥ 12 words> | source=S### | snapshot=<file> | digest=<64-hex> | quote="<text>" |` | note absent rc 128 and counter absent rc 128 at base → note present, counter present, registry 289 → 293 rows, and the frozen counter prints `XS_ROWS=6 XS_VERIFIED=6 XS_SOURCES=4 XS_SNAPSHOTS=4 XS_TARGET … met=1` rc **0** | `python3 tools/count-xs-rows-r70.py --revision <REV>` | the pre-data battery's control must read 6/6 rc 0 **and** every mutant (content-free statement, any-registered-id, digest-swap, quote-absent, short statement, five rows, duplicate id) must read below the target and exit 1; a mutant meeting the target falsifies the counter |
| C2 | operability (9; capability `xfs-stats-arm`) | one verdict-neutral `XFS xfs-stats mounts=<n> present=<n> absent=<n> unreadable=<n> stats=<n> error=<n> log=<n> detail=<token|none>` line in `tools/tsukuroi-census.sh`, printed after the KERNEL line and before the rollup: distinct xfs mount sources from the mount table (`TSUKUROI_PROC_MOUNTS`), their `/sys/fs/xfs/<dev>` presence (`TSUKUROI_XFS_SYSFS`), readable `stats/stats` files whose first line matches `^[a-z][a-z0-9_]*([ ][0-9]+)+$`, readable regular files under `error/` and `log/`, and a closed-vocabulary detail token set; read-only, unprivileged, never a rollup term and never an exit-code input | label **0**, `probe_xfs` **0**, selftest **196** → label present, exactly **1** live line with every field once in contract order, `mounts` equal to the distinct xfs source count `findmnt -t xfs` reports in the same capture, `stats` ≤ `present`, `error`/`log` equal to the enumerated regular-file counts, rollup line and exit code identical to (f), `--selftest` `PASS (N cases, N passed, 0 failed)` rc 0 with **N ≥ 206** and **≥ 10** `R70-C2` cases | `grep -c 'XFS xfs-stats' tools/tsukuroi-census.sh`; `bash tools/tsukuroi-census.sh --selftest`; `bash tools/tsukuroi-census.sh` | a live line that echoes an unvalidated name, a line that changes the rollup or exit code, a `mounts` count that disagrees with the mount table, or fewer than 10 labelled cases each falsifies the claim |

Causal separability: C1 touches only its note, four registry rows, its counter and receipts; C2 touches only
`tools/tsukuroi-census.sh`. Each verifies without the other. Both predicates are frozen here, before any note,
registry row, census label or selftest case exists; the counter and its battery are committed with this
declaration (round-69 D4's ordering defect answered).

Routed repairs this round as work, not as claims (r69 non-author spot-check, `corpus/lessons/round-69-verifier-spotcheck.md` §6):
D1 appended Gate erratum carrying the URL/access-date/located-quote record for S288/S289; D2 the
`check-cited-receipts-r62.py` PASS receipt committed at the final tree; D3 every receipt bound to the revision
it measured; D4 the freeze-ordering correction above; D5 the three refused r69 candidates landed as
`rejected` registry rows with reason and flip; D6 LOG entries tying the r69 post-landing commits; D7 the LOG
selftest figure corrected to 196. One `considerthese` proposal mined: `considerthese/2026-10-26.md`
"Counter-attack scoreboard". Assimilation: none — the open L0 `tsukuroi | round-64` addendum (82 colliding
staged ids) still rules the merge package quarantined.

Wave w1: one v1 wave, band 8–16, **13 seats**; seat shape and counts are fixed in `.ufo/waves/round-70/w1-spec.json`.

**planned (next round):** the r70 depth entry's row-verdict binding (the XS rows are rules, not admitted
propositions — a counted read of host applicability); R66-M3/M4 frozen-counter amendments where still reachable;
the AR resolve-then-count debt; no amendment of this round's frozen predicates.

## Round 70 — measured outcome (2026-11-04, measured revision `40c35ee7`; author-side, non-author closure pending)

Declared at `1710bd74`; snapshot repair `84e013a7`; base `b2aa0be0`; measured surface
`40c35ee7f197bc5c54f58fc5d2a1e7e4943eae32`. Wave w1: one v1 wave, **13 seats, 0 reported dead**
(`w1-results.json`); scout1 / executor3 / scribe3 / connector1 / reviewer2 / critic1 / mutation-tester1 /
sentinel1; strict attack seats 4/13 = 31 % (>= 25 %); connector 1; residual 0; the L1 held the planner
seat (not a validator role).

| Claim | Before (base `b2aa0be0`) -> after (measured revision) | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (SOURCED — S290-S293) | note `cat-file` rc **128** -> present; counter rc **128** -> present; SOURCES **289 -> 296** (four admitted + D5's three rejected); `XS_ROWS=6 XS_VERIFIED=6 XS_SOURCES=4 XS_SNAPSHOTS=4 XS_TARGET … met=1` rc **0**; every new row `NF=13`; knowledge-header **88/88**, 0 findings; refs **0** dangling; line-endings PASS 352/0; canonical census rc **0** | **verified** on the frozen predicate (author-side) | depth **8 -> 8**: one new mechanism on ground the province called unread (the XFS sysfs stats/log/error plane) plus one capability; no ordinal uplift claimed |
| C2 operability (capability `xfs-stats-arm`) | label **0**, `probe_xfs` **0**, selftest **196** -> label present, exactly **1** live line `XFS xfs-stats mounts=2 present=2 absent=0 unreadable=0 stats=2 error=18 log=8 detail=none`, every field once in contract order; `mounts` equals the distinct xfs source count `findmnt -t xfs` reports in the same capture; per-fs `error=9 log=4 stats_lines=34`; rollup line byte-identical to the base capture and rc **1**; `--selftest` `PASS (214 cases, 214 passed, 0 failed)` rc **0** with **18** `R70-C2` case lines (>= 10) | **verified** on the frozen predicate (author-side); the instrument was repaired inside the round after attack (F2/F3) and the repair is proved able to fail | operability **9 -> 9** (no uplift; the capability row enters) |

Counting commands (outputs in `.ufo/waves/round-70/after/gates-at-40c35ee7.txt`):

```
python3 tools/count-xs-rows-r70.py --revision 40c35ee7            -> 6/6, XS_SOURCES=4 XS_SNAPSHOTS=4, met=1, rc 0
git show 40c35ee7:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3,}'   -> 296
git show 40c35ee7:corpus/SOURCES.md | awk -F'|' '/^\| S29[0-6] /{print $2, NF}' -> seven rows, NF=13 each
bash tools/tsukuroi-census.sh --selftest                          -> PASS (214 cases, 214 passed, 0 failed), rc 0
bash tools/tsukuroi-census.sh | grep -c '^XFS xfs-stats '          -> 1
findmnt -t xfs -o SOURCE | sort -u | wc -l                        -> 2 (== the line's mounts)
diff <(base rollup) <(live rollup)                                -> identical, rc 0
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi -> rc 0, 296 rows
```

**Capabilities — round 70 entry.**

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| xfs-stats-arm | Reports the unprivileged XFS sysfs reading on the census's verdict-neutral `XFS xfs-stats` line: distinct xfs mount sources, their `/sys/fs/xfs/<dev>` presence (partition kept exact), first-line stats parse, recursive readable regular-file counts under `error/` and `log/`, and a closed detail vocabulary — read-only, no xfsprogs call, never a rollup or exit-code input | `bash tools/tsukuroi-census.sh` -> one XFS line (`after/census-live-after.txt`); `--selftest` -> PASS 214/214 with 18 `R70-C2` cases | round 70 |

Named limits, recorded and not smoothed:

- **C2's literal predicate admits a line that does not read the host** (critic `K1Critic` C2-1, fatal as a
  measurement-strength finding): the frozen text binds `mounts == findmnt`, `stats <= present` and the
  live counts, but no `present + absent + unreadable == mounts` clause and no named verifier-side
  enumerator for `error`/`log`. The landed arm keeps that partition by construction and its counts were
  independently enumerated (`probes/E2Capture/host-enum.txt`: 18/8), but the predicate text alone cannot
  distinguish the arm from a constant. Routed: a next-round predicate amendment naming the enumerator and
  the partition (the claim's frozen predicate is not amended here).
- **C1's statement-substance clause is lexical** (`R1Reviewer` M4): three real domain tokens plus nine
  gibberish words reach `grounded()==3`. M5 (a snapshot may be cited three times), M6 (the registry
  `anchor` cell is parsed but never read) and M11 (a space-less `|XS<n>|` row is not counted at all) are
  bookkeeping channels, not content channels; all four are routed to the next frozen-counter amendment.
  M1Mutation's independent 7 counter mutants were all killed, but the committed pre-data battery alone
  kills only 2 of those 7 — the receipt's fixture set is thinner than its clause set.
- **The arm's regular-file enumeration was wrong for two fixture shapes** (`R2Reviewer` F2 dotfile
  undercount, F3 symlink overcount); repaired in-round with `find -type f` semantics and two new cases,
  red-before `.ufo/waves/round-70/probes/L1-redbefore-r70c2.txt` (pre-repair 212/214 with exactly those
  two failing). Neither shape exists under this host's sysfs, so the live line is unchanged.
- **A census selftest case cannot fail a blocking arm** (`M1Mutation` §2): a mutant that reads a FIFO
  hangs the suite rather than reporting FAIL; the real arm never opens a FIFO (`-type f`), but the harness
  has no per-case timeout. Routed: a timeout harness next round.
- **A6 case attribution** (`M1Mutation`): the rollup-term mutant is killed by the pre-existing R39 rollup
  cases and the R70 shape cases, not by the neutrality A/B case, whose fixture journal plane is already
  DEGRADED.
- **Mount-source mapping** (`K1Critic` C2-2, [inference]): `UUID=`, `LABEL=` or `/dev/mapper/<name>` sources
  cannot be mapped to a sysfs kobject name without blkid and read absent; no such mount exists here.
- **The declaration's own receipts carried three defects**, all recorded in the round lesson and QUALITY
  104: the four-snapshot set was three files at the declaring commit (`health.c` at `84e013a7`); the host
  prose said 7 error files per filesystem where the capture lists 9; the novelty command's pathspec was
  dropped in prose. C1's predicate fails closed on the first (`map-digest`) and the measured revision
  carries the full set.

Ordinals unchanged: depth **8**, coverage **9**, operability **9**, freshness **9**, calibration **9**,
adjacency **8**. Saturation line **9**, window **3**; none retired. The lowest-axis duty is met by C1
(depth, tied lowest at 8); the round's depth verdict is **unchanged**, reported as such. Learning trends
(author-side; a non-author spot-check is owed by the closure judge): **expansion: improved** (S290-S293 on
ground never held, one entry, three rejected rows, capability `xfs-stats-arm`); **quality: improved** (the
r69-planned statement-substance and binding clauses answered in a frozen counter; two attack-found arm
defects repaired with red-before proof; PROVINCE promotion; QUALITY 104; the D1 Gate erratum); **discernment:
unchanged** (the wave caught four of the lane's own defects; the outside spot-check is owed).

Planned (next round): a C2 predicate amendment naming the verifier-side enumerator and the partition
invariant; the C1 counter's statement-substance and anchor-binding clauses; a per-case selftest timeout;
R66-M3/M4 where still reachable; the AR resolve-then-count debt; no amendment of this round's frozen
predicates.

## Round 70 — declaration errata (append-only; the frozen predicates are unchanged)

The declaration text at `1710bd74` stays as written. These measured corrections are appended; they amend
prose receipts only, never the C1/C2 predicate, counter or kill rule.

1. **(a) snapshot set.** The declaration names four snapshots as committed at the declaring commit; only
   three were (`SHA256SUMS` 3 lines, `SOURCES.json` 3 keys). `health.c` (digest `84fdd0be…15950`) and its
   map entry landed at `84e013a7`; `sha256sum -c` is 4/4 OK at the measured revision.
2. **(b) host count.** "error subtree 7 regular files per filesystem" is superseded: the committed capture
   and the live tree read **9** per filesystem (1 + 4 handler classes x 2 knobs) and the frozen predicate's
   "enumerated regular-file counts" is **18**, not 14.
3. **(c) novelty command.** The prose command omitted its `-- corpus/knowledge` pathspec; without it the
   declaring commit reads 3 (its own `before/src` files). With the pathspec it reads 0, as the receipt
   `before/novelty-sweep.txt` records, and the substantive proposition holds.
4. **(d) considerthese.** The sentence naming the "Counter-attack scoreboard" as this round's mined
   proposal is withdrawn: it was adopted at round 64 (`SKILL.md:5603`). No proposal is mined this round;
   the scoreboard is continued as the standing ledger, and the measured implementation status per proposal
   is in the round lesson's `## Considerthese`.

## Round 71 — declaration (2026-11-04, base `930d5530`, written before any after-measurement)

Lowest non-retired axis: **depth (8, tied with adjacency 8)**; saturation line **9** / window **3**
unchanged; none retired. A capability entered at round 70 (`xfs-stats-arm`), so the stagnation window is
at 1 of 3 and the nudge does **not** waive the lowest-axis duty. Two claims on two distinct axes
(depth; operability).

Pre-declaration receipts, disclosed in order; all under `.ufo/waves/round-71/before/`.

(a) **Source snapshots** fetched and read before this text, committed byte-exact under `before/src/` with
`SHA256SUMS` (`sha256sum -c` rc 0) and `SOURCES.json` (snapshot → URL, tag, access date, digest), all at
Linux stable **v7.2.11** (the host's own kernel): `Documentation/admin-guide/kernel-parameters.rst`
sha256 `45587d8e…88799`, `kernel/params.c` sha256 `923610d5…782a4`, `include/linux/moduleparam.h`
sha256 `220f2dac…14846`, `kernel/module/main.c` sha256 `e1e1a1c8…95929`. Access date **2026-11-04**.

(b) **Host capture**, read-only (`before/host.txt`, `capture.sh`): kernel `7.2.11-arch1-1`; **136** modules
publish a `parameters` directory and **829** parameter files exist; `nvidia_drm` exposes
`color_pipeline fbdev modeset vblank`, all `-r--r--r--`, `modeset=Y`; `nvidia` exposes 0444
`NVreg_*` parameters; `nvidia_uvm` parameters are `-rw-r--r--` (root-writable) and **no** parameter file
is writable by the unprivileged reader; `/sys/module/btrfs/parameters/read_policy` is **absent**
(the `perm == 0` case S287 names); `modprobe.d` holds 3 files under `/etc` and 4 under `/usr/lib`
(paths and modes only — contents were never read).

(c) **Held-ground sweep** (`before/novelty-sweep.txt`): at base, `modprobe.d`, `kernel-parameters`,
`module_blacklist`, `NVreg`, `module_param`, `kernel_param_ops` and `param_attr_store` each read **0**
file hits across `corpus/ SKILL.md PROVINCE.md`; no knowledge note names the module-parameter surface
(`git ls-tree … | grep -iE 'module|param'` → none); the six notes that mention `/sys/module` read only
`version`/`taint` state.

(d) **Do-nothing controls** (`before/absence-controls.txt`, base `930d5530`): C1 note `git cat-file -e`
rc **128**; C1 counter rc **128**; `^| MP[n]` rows **0**; `R71-C2` labels **0**; per-case-timeout tokens
**0**; selftest **214** PASS rc 0; registry **296** rows; **88** knowledge notes; canonical census
validate rc **0**.

(e) **Frozen counter and its pre-data battery**: `tools/count-mp-rows-r71.py` sha256
`fa67d4deb5f01a5124120276a8571fa36c7367d9db711ceb39bc1ca6fded48bc`; battery
`before/control/battery.txt` (**12 cases: 1 well-formed control + 11 mutants**) — the control reads
`MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0` and `met=1` rc 0; the eleven mutants
(content-free statement, unbound source, absent quote, short statement, five rows, duplicate id,
snapshot reuse 3, ungrounded statement, malformed invisible row, digest swap) each read `met=0` rc 1.

(f) **Baselines**: `before/selftest-base.txt` → `PASS (214 cases, 214 passed, 0 failed)` rc 0;
`before/census-live-base.txt` → `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=DEGRADED
drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)` rc 1; `before/redbefore-timeout.txt`
→ a blocking probe under the selftest's own call shape ends at an **external** 20 s bound with rc **124**
and **0** verdict lines, and the pre-fix census carries 0 `R71-C2` labels and 0 per-case-timeout tokens.

| # | axis/type | claim | before → after (frozen predicate) | counting command | kill rule |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — four new registry rows) | `corpus/knowledge/module-parameter-plane-r71.md` states the kernel module-parameter surface the lane never held: a parameter is visible under `/sys/module/<name>/parameters/` only when its `perm` is nonzero; the file mode **is** the parameter's `perm` and a store handler exists only when a write bit is set; the `kernel_param_ops` contract (set returns 0 or `-errno`, get returns a length or `-errno`, both optional); an unknown parameter is warned and **ignored**, so a typo does not fail the load; `module_blacklist=` refuses the load; and the two specification routes (cmdline `mod.param=v`, modprobe `mod.param=v`) with built-ins requiring the cmdline; rows `MP1`–`MP6`, each `\| MP<n> \| <statement, >= 12 words> \| source=S### \| snapshot=<file> \| digest=<64-hex> \| quote="<text>" \|` | note absent rc **128**, counter absent rc **128**, `^\| MP[n]` rows **0**, registry **296** rows → note present, counter present, `MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0` and `MP_TARGET … met=1`, registry **300** rows | `python3 tools/count-mp-rows-r71.py --revision <REV>`; `git show <REV>:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3,}'` | any row failing a clause, any MP-shaped line that does not parse, one snapshot cited more than twice, fewer than 6 rows / 4 sources / 4 snapshots, or `met=0` → the claim fails |
| C2 | operability (9; capability `selftest-case-timeout`) | `tools/tsukuroi-census.sh` bounds every selftest case: each case child is started in its own process group, polled to a per-case bound (`TSUKUROI_SELFTEST_CASE_TIMEOUT`, default 60 s), killed TERM then KILL when it exceeds it, and reported as a `FAIL` line naming the case and `timeout`; a hermetic self-check case proves the bound fires on a blocking child and does **not** fire on a child that finishes; read-only, no host write, never a verdict term | `R71-C2` labels **0**, per-case-timeout tokens **0**, selftest **214** → labels **>= 3**, selftest `PASS (N cases, N passed, 0 failed)` with **N >= 217**, the suite finishing under an external 300 s bound, and the self-check case asserting both the kill and the no-false-positive arm | `bash tools/tsukuroi-census.sh --selftest \| tail -1`; `grep -c 'R71-C2' tools/tsukuroi-census.sh` | the suite hangs at the external bound, a `R71-C2` case passes with the harness removed (mutation), or the timeout path reports a non-timeout failure → the claim fails |

Causal separability: C1 touches only its note, four registry rows, its counter and receipts; C2 touches
only `tools/tsukuroi-census.sh`. Each verifies without the other. Both predicates are frozen here, before
any note, registry row, census case or receipt exists; the counter and its battery are committed with this
declaration.

Routed repairs this round as work, not as claims (`corpus/lessons/round-70-verifier-spotcheck.md` §5):
D1 the stale selftest tallies in `PROVINCE.md`, `corpus/README.md` and `SKILL.md` corrected append-only
against the final receipt line; D2 the unbacked final-revision re-run claims replaced by committed receipts
at the measured revision; D3 the `count-xs-rows-r70.py` shebang corrected to `python3`; D4 the r70-planned
frozen-counter amendments (statement substance, anchor binding, invisible row, snapshot reuse) carried into
this round's counter. Assimilation: **none** — the open L0 `tsukuroi | round-64` addendum still rules the
merge package quarantined. `considerthese`: no proposal mined; the measured status of the four proposals in
`considerthese/2026-10-26.md` is recorded in the lesson, and the scoreboard is continued as the standing
ledger.

Wave w1: one v1 wave, band 8–16, **14 seats**; seat shape and counts are fixed in
`.ufo/waves/round-71/w1-spec.json`.

**planned (next round):** the C1 counter's remaining bookkeeping channels if attack finds any; the r70
arm's literal-predicate amendment (`present + absent + unreadable == mounts`, a named verifier-side
enumerator for `error`/`log`); the AR resolve-then-count debt; no amendment of this round's frozen
predicates.

## Round 71 — measured outcome (2026-11-04, measured revisions `2959254a` (C1) and `2b358d2d` (C2); author-side, non-author closure pending)

Wave w1: one v1 wave, **14 seats, 0 reported dead** (`w1-results.json`, all 14 outputs non-empty);
scout 1 / executor 3 / scribe 4 / connector 1 / reviewer 2 / critic 1 / mutation-tester 1 / sentinel 1;
strict attack seats 4/14 = 29 % (>= 25 %); connector 1 (<= 2); residual 0; the L1 held the planner seat.

| Claim | Before (base `930d5530`) -> after (measured revision) | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (SOURCED — S297-S300) | note `cat-file` rc **128** -> present; counter rc **128** -> present; registry **296 -> 300** rows; four new rows `NF=13` and `malformed=0`; knowledge notes **88 -> 89**; `MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0`, `met=1`, rc 0 at `2b358d2d`; canonical census validate rc **0** | **verified** on the frozen predicate (author-side) | depth **8 -> 8**: one new mechanism on ground the province never held (the module-parameter surface) plus one capability; no ordinal uplift claimed |
| C2 operability (capability `selftest-case-timeout`) | `R71-C2` labels **0** -> **15** lines / **4** emitted case labels; selftest **214** -> `PASS (218 cases, 218 passed, 0 failed)` rc 0 under an external 300 s bound; the three arms plus the daemonizing-child arm all PASS; live rollup line byte-identical and rc **1**; red-before `before/redbefore-timeout.txt` rc **124** with 0 verdict lines | **verified** on the frozen predicate (author-side); two wave-found gaps repaired in-round (arm_run/identity children unbounded; daemonizing child leaked a descendant) and the repairs proved able to fail | operability **9 -> 9** (no uplift; the capability enters the table) |

Counting commands (outputs in `.ufo/waves/round-71/after/`):

```
python3 tools/count-mp-rows-r71.py --revision 2b358d2d            -> MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 met=1, rc 0
git show 2b358d2d:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3,}'   -> 300
bash tools/tsukuroi-census.sh --selftest                          -> PASS (218 cases, 218 passed, 0 failed), rc 0
grep -c 'R71-C2' .ufo/waves/round-71/after/selftest-after.txt     -> 4
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi -> rc 0
```

**Capabilities — round 71 entry.**

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| selftest-case-timeout | Bounds every census selftest case child: own process group, `/proc`-state liveness (a zombie counts as exited), per-case bound (`TSUKUROI_SELFTEST_CASE_TIMEOUT`, default 60 s), TERM then KILL, rc 124 and a FAIL line naming the case and `timeout`; the process group is killed after every run so a daemonizing child leaves no descendant. Four hermetic `R71-C2` arms prove the kill, the no-false-positive path, the escalation and the descendant reap | `bash tools/tsukuroi-census.sh --selftest` -> PASS 218/218 (`after/selftest-after.txt`); red-before `before/redbefore-timeout.txt` rc 124 | round 71 |

Named limits, recorded and not smoothed:

- **C1's statement-substance clause is lexical** (`probes/L1Channels/semantic-channel.txt`): a row whose
  statement negates its snapshot but keeps the vocabulary reads `met=1`. The counter checks grounding,
  binding and provenance, never entailment; row semantics rest on the non-author review (R1Reviewer's
  three P2 findings, all corrected in the note) and on the closure judge.
- **Eleven of thirteen source-level counter mutants survive** (`probes/E2CounterAttack/score.md`): removing
  one clause usually leaves another that still rejects the matched bad fixture, so the *fixture set* does
  not isolate clauses even though the predicate does. The committed battery catches three of them; the
  duplicate-id case is killed by row count + snapshot reuse, not by its own clause (K1 D4).
- **The harness's own cases cannot see their own removal** (`probes/M1Mutation/score.md`): deleting the
  four `R71-C2` cases makes all eight harness mutants invisible; only the `N >= 217` count target notices.
- **Bound normalization is fail-open by design**: a malformed, empty or zero `TSUKUROI_SELFTEST_CASE_TIMEOUT`
  becomes 60 s rather than disabling the harness (E1Harness's draft fails closed; neither disables the bound).
- **Wave lineage** (`probes/N1Sentinel/audit.md` F3): the C2 harness was implemented by the L1
  (prototype `L1/proto/census.sh`, byte-identical to `db58e7c9`); E1Harness's patch is an independent
  alternative drafted in parallel, not the applied artifact. The post-wave repairs adopt R2Reviewer's
  arm_run/identity and daemonizing-child findings and E1Harness's liveness/grace/rc findings.

## Round 71 — declaration errata (append-only; the frozen predicates are unchanged)

1. **(a) battery count.** The declaration says "12 cases: 1 well-formed control + 11 mutants"; the receipt
   `before/control/battery.txt` prints `BATTERY cases=11 passed=11 failed=0` (1 control + 10 mutants).
   K1Critic D3 and SC3Lesson found it independently.
2. **(b) modprobe.d count.** The declaration says "3 files under `/etc` and 4 under `/usr/lib`"; the
   committed `before/host.txt` lists **3 and 5** (`README`, `bluetooth-usb.conf`, `gsr-nvidia.conf`,
   `nvidia-utils.conf`, `systemd.conf`). K1Critic D1.
3. **(c) absence-control label.** The line "census validate at base: rc=0" names
   `scripts/sources-census.sh validate --root … tsukuroi`, the fleet census, not an entry point of
   `tools/tsukuroi-census.sh`; the command in the receipt is the one that ran. K1Critic D2.
4. **(d) duplicate-id battery case.** That case is killed by `MP_ROWS=7` plus `snapshot-reuse`, not by the
   `duplicate-id` clause; a true `MP1,MP2,MP2,…` fixture does print `duplicate-id` + `ids-not-contiguous`
   (K1Critic D4, E2CounterAttack `battery_bug`).
5. **(e) final instrument figures.** The docs commit `bdaec573` writes "217 cases" and "three `R71-C2`
   cases"; after the wave repairs the final instrument is **218 cases, four `R71-C2` case labels**
   (`after/selftest-after.txt`). The superseded figures stay as filed; this erratum is the correction.

## Round 72 — declaration (2026-11-03, base `a7015d27`, written before any after-measurement)

Lowest non-retired axis: **depth (8, tied with adjacency 8)**; saturation line **9** / window **3**
unchanged; a capability entered at r70 (`xfs-stats-arm`) and r71 (`selftest-case-timeout`), so the
stagnation window is at 2 of 3 and the nudge does **not** waive the lowest-axis duty. Three claims on
three distinct axes (depth; operability; freshness).

Pre-declaration receipts, disclosed in order; all under `.ufo/waves/round-72/before/` at base
`a7015d27`.

(a) **Source snapshots** opened and read before this text, committed byte-exact under `before/src/`
with `SHA256SUMS` (`sha256sum -c` rc 0) and `SOURCES.json` (snapshot → URL, tag, access date, digest),
all at kmod **v34** — the host runs kmod **34.2** (`modprobe --version`): `man/modprobe.d.5.scd`
sha256 `aa1a869e57db31c8187a436b5eab3047394da5fd779794e1cdd4ccad598ee46e`,
`libkmod/libkmod-config.c` sha256 `ae520a0721aad0bc61c7b13369fccf8e46fc408d8c0884fda9260a05da7ceb11`,
`tools/modprobe.c` sha256 `1e8e352634026e6618f37c0aee9974cf51427bfa3a77d12bcd2220ea8a71bf3f`.
Access date **2026-11-03**.

(b) **Host capture**, read-only, paths and modes only — config file contents were never read
(`before/host.txt`, `capture.sh`): kernel `7.2.11-arch1-1`; `/etc/modprobe.d` **3** names
(`disable-usb-autosuspend.conf`, `hid_apple.conf`, `nvidia.conf`); `/usr/lib/modprobe.d` **5** names
(`README` plus four `.conf`); `/run/modprobe.d` and `/usr/local/lib/modprobe.d` **absent**; `/lib`
resolves to `/usr/lib`, so `/lib/modprobe.d` and `/usr/lib/modprobe.d` are **one directory behind two
SYNOPSIS entries**; `/proc/cmdline` carries no `module.parameter` token; **136** `/sys/module/*/parameters`
directories.

(c) **Held-ground sweep** (`before/novelty-sweep.txt`): at base no knowledge note names the surface —
`softdep`, `MODPROBE_OPTIONS`, `showconfig`, `APPLY_BLACKLIST`, `conf_files_insert_sorted` and
`lexicographic` each read **0** file hits under `corpus/knowledge`; the one `modprobe.d` token hit is
the r71 note's MP5 host line, which names paths only; `SKILL.md` **0** hits, `PROVINCE.md` **4**,
`corpus/README.md` **2** (all path/mode boundary prose, no rule row).

(d) **Do-nothing controls** (`before/absence-controls.txt`, base `a7015d27`): C1 note `git cat-file -e`
rc **128**; `^| MD[n]` rows **0**; the frozen counter over the base tree reads `MD_NOTE absent` rc
**128**; `check-selftest-tally.py --selftest` rc **2** with **0** case lines (tool digest
`b0f839e3955529caf560576f02f5c4137a98317d82c90cf1225dffe45d366c6d`); the routed-defect checker at
base reads `ROUTED_STALE=3` rc **1**; registry **300** rows; **89** knowledge notes; canonical census
validate rc **0**.

(e) **Frozen instruments.** `tools/count-md-rows-r72.py` sha256
`d615c653f32a29af3a4355d882041b8543ff56882b3225f7e3eedf173d8706a6`; its battery
`before/control/battery.txt` — **11 cases: 1 well-formed control + 10 mutants**; the control reads
`MD_ROWS=6 MD_VERIFIED=6 MD_SOURCES=3 MD_SNAPSHOTS=3 MD_MALFORMED=0` and `met=1` rc 0, the ten mutants
(short statement, unregistered source, absent quote, five rows, duplicate id, snapshot reuse 3,
ungrounded statement, malformed hidden row, digest swap, own-work source kind) each read `met=0` rc 1.
`tools/check-r71-routed-r72.py` sha256
`df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712`; its battery
`before/control/routed-battery.txt` — **5 cases, 5 passed**: one green control (rc 0) and four mutants
(tampered receipt, missing erratum, missing note correction, missing receipt; each rc 1).

| # | axis/type | claim | before → after (frozen predicate) | counting command | kill rule |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — registry rows S301–S303) | `corpus/knowledge/modprobe-config-plane-r72.md` states the modprobe configuration plane the lane never held: configuration directories are read in the SYNOPSIS precedence order and the first file of a given name suppresses the same name in later directories; files from every directory are processed in one lexicographic order so a later-ordered file partially replaces an earlier one; libkmod inserts config filenames into one sorted list and rejects a second file of the same name; the kernel command line is parsed into the same config object after the files; `-n` prints the plan without executing; blacklist is applied to aliases only unless `--use-blacklist` adds the unconditional flag. Rows `MD1`–`MD6`, one physical line each, exactly 7 pipe cells, no pipe inside a cell: `\| MD<n> \| <statement> \| source=S### \| snapshot=<file> \| digest=<64 hex> \| quote="<verbatim, <=25 words>" \|` | note `cat-file` rc **128**, MD rows **0** → `MD_ROWS=6 MD_VERIFIED=6 MD_SOURCES=3 MD_SNAPSHOTS=3 MD_MALFORMED=0`, `met=1`, rc **0** at the measured revision; registry **300 → 303** rows (three `NF=13` rows, `malformed=0`); knowledge notes **89 → 90**; canonical census validate rc **0** | `python3 tools/count-md-rows-r72.py --revision <REV>`; `git show <REV>:corpus/SOURCES.md \| grep -cE '^\| *S[0-9]{3,}'`; `git ls-tree --name-only <REV>:corpus/knowledge \| grep -c '\.md$'` | any row failing any frozen clause, any malformed MD-shaped line, row count != 6, distinct sources < 3, distinct snapshots < 3, a snapshot cited > 2 times, or the note absent → the claim fails |
| C2 | operability (9; capability `gate-selftest`) | `tools/check-selftest-tally.py` gains a `--selftest` mode: it builds every fixture under `$TMPDIR` (never a hardcoded `/tmp`), runs the checker's own core over them, prints `SELFTEST: PASS (N cases, N passed, 0 failed)` with one named case line each, and exits 0; the cases cover a matching figure (pass), a mismatched figure (fail with a stable finding id), a wrong label count, a superseded-figure quote (skip), an out-of-scope battery figure, and a receipt with no `PASS (N cases, …)` line (rc 2) | `--selftest` rc **2**, **0** case lines at base → rc **0**, `SELFTEST: PASS` with **N >= 7**; red-before `before/control/selftest-redbefore.txt`: a mutant copy whose mismatch branch is disabled fails the suite with a named failing case; the existing r70 self-demo still reads `added_figures_mismatched=0 receipt_cases=214 receipt_labels=18` rc **0** | `python3 tools/check-selftest-tally.py --selftest`; `python3 tools/check-selftest-tally.py --receipt .ufo/waves/round-70/after/selftest-after.txt --label R70-C2 --range 4035c1a0..40c35ee7 -- SCORECARD.md PROVINCE.md corpus/README.md SKILL.md` | `--selftest` rc != 0, N < 7, fewer than one emitted line per case, any case writing under `/tmp`, or the existing self-demo changing verdict → the claim fails |
| C3 | freshness (9) | the two statement/receipt defects routed by the round-71 closure are closed in committed bytes: `.ufo/waves/round-71/after/count-mp-rows-final.txt` exists and its summary lines equal a fresh run of the frozen r71 counter at the single named revision `2b358d2d`; `SCORECARD.md` carries a `## Round 71 — receipt erratum` block naming that receipt and revision; `corpus/knowledge/module-parameter-plane-r71.md` carries an appended correction naming `R71-NOTE-MODPROBE-COUNT`, the **five** `/usr/lib/modprobe.d` paths and the superseded **four** figure | `ROUTED_STALE=3` rc **1** (all three missing) → `ROUTED_STALE=0` rc **0** at the measured revision | `python3 tools/check-r71-routed-r72.py --revision <REV>` | any stale item remains, or the committed receipt does not equal a fresh counter run at `2b358d2d` → the claim fails |

Causal separability: C1 touches only its note, three registry rows, its counter and receipts; C2 touches
only `tools/check-selftest-tally.py`; C3 touches the r71 receipt file, one SCORECARD erratum block and
one appended correction in the r71 note. Each verifies without the other two having landed. All three
predicates are frozen here, before any note, registry row, tool change or correction exists; the three
instruments and their batteries are committed with this declaration.

Routed repairs this round as work, not as claims (`corpus/lessons/round-71-verifier-spotcheck.md` §6):
R71-RECEIPT-MISPATH — the probe pointers are restated correctly in this round's report erratum;
R71-GATE-SELFTEST — worked inside C2; R71-KMOD-LEAD-PATH — C1 opens the real path
(`man/modprobe.d.5.scd` at v34, HTTP 200) and decides the precedence question on its bytes; the r71
reject stays as filed.

Assimilation: **none** — the open L0 `tsukuroi | round-64` addendum still rules the merge package
quarantined. `considerthese`: no proposal mined; the measured status of the proposals in
`considerthese/2026-10-26.md` is recorded in the lesson.

Wave w1: one v1 wave, band 8–16, **12 seats**; seat shape and counts are fixed in
`.ufo/waves/round-72/w1-spec.json`.

**planned (next round):** the C1 counter's lexical-substance channel (a row that negates its snapshot
but keeps the vocabulary reads `met=1`); the `--selftest` mode's own mutants; the r71 report pointer
erratum's closure check; no amendment of this round's frozen predicates.

## Round 71 — receipt erratum (appended round 72, append-only)

The round-71 C1 outcome header names measured revisions `2959254a` (C1) and `2b358d2d` (C2) while the
C1 counting command names `2b358d2d`, and no committed output carried that run (closure routed defect
R71-C1-UNRECEIPTED-RUN). The single C1 measured revision is **`2b358d2d`**: the final run is committed
at `.ufo/waves/round-71/after/count-mp-rows-final.txt` and its summary lines equal a fresh
`python3 tools/count-mp-rows-r71.py --revision 2b358d2d` (`MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4
MP_SNAPSHOTS=4 MP_MALFORMED=0`, `MP_TARGET … met=1`, rc 0). `2959254a` is the note's landing commit,
not a counter run; it is superseded by this erratum and stays visible as filed. Checker:
`python3 tools/check-r71-routed-r72.py --revision <REV>`.

## Round 72 — declaration erratum (append-only; the frozen predicates are unchanged)

1. **(a) the cmdline host fact.** Pre-declaration receipt (b) says "`/proc/cmdline` carries no
   `module.parameter` token". The committed `before/host.txt` contradicts that literal shape: it carries
   four `modname.param` tokens that libkmod's parser accepts — `zswap.enabled=1`,
   `zswap.max_pool_percent=25`, `vt.global_cursor_default=0`, `systemd.show_status=false` (R1Reviewer F1,
   with the parser's state machine at `libkmod-config.c:717-725` and `kmod_config_add_options:610-634`).
   The accurate fact is "no `modprobe.blacklist=` token; four built-in subsystem `name.param` tokens are
   parsed into the config object every run", so MD4 is **active**, not inert, on this host. The frozen
   predicates, targets and kill rules are untouched; `PROVINCE.md` and the note's host line carry the
   corrected sentence.
2. **(b) counter channel, recorded not repaired.** R1Reviewer F4: a registry row with `kind=community`
   and tier A verifies `met=1` — the counter reads `kind` but not `tier`. The frozen counter is not
   amended this round; the channel is carried into the round-72 planned-next-round debt.

## Round 72 — wave erratum (append-only; the frozen predicates are unchanged)

`K1Critic` filed nine defects (D1-D9) against the declaration's prose and its instruments; the wave also
filed three fabrication controls. Dispositions:

1. **(c) D1 — the C2 red-before receipt's provenance.** The frozen C2 row names
   `before/control/selftest-redbefore.txt`, which was not in `6b42676` (the declaration commit omits it;
   the file was committed at `123e1c57`). The reproducible recipe now lands at
   `.ufo/waves/round-72/after/redbefore-mutant.sh`; its committed run
   `.ufo/waves/round-72/after/redbefore-selftest.txt` fails `SELFTEST-MISMATCH` and `SELFTEST-MIXED`
   (`SELFTEST: FAIL (9 cases, 7 passed, 2 failed)`, rc 1). The frozen row is not edited.
2. **(d) D2 — C3's measured scope.** The checker now enumerates the five `/usr/lib/modprobe.d` names
   (R72-C3-TOKEN-LIST); a correction that names the defect and paths is required. A block that names the
   receipt and revision while *denying* the repair still reads `ROUTED_STALE=0` — recorded as a named
   limit: the checker verifies naming, not entailment, and the correction's direction rests on the
   non-author review.
3. **(e) D3 — the cmdline fact** is corrected in item (a) above: four `name.param` tokens are parsed
   (`zswap.enabled`, `zswap.max_pool_percent`, `vt.global_cursor_default`, `systemd.show_status`), so
   MD4's parse is live; no `modprobe.blacklist=` token is present.
4. **(f) D4 — the C2 case set.** The frozen target is `N >= 7`; the landed suite is nine cases whose ids
   are `MATCH`, `MISMATCH`, `LABEL`, `SUPERSEDED`, `OUT-OF-SCOPE`, `NO-RECEIPT`, `GREEN-DIFF`, `MIXED`,
   `HERMETIC`. Named measurements now ride the after receipt: a set-but-missing `$TMPDIR` reads rc 2
   (`SELFTEST-TMPDIR`), the committed red-before recipe reads rc 1, and the `HERMETIC` case asserts the
   fixture root is not under `/tmp` when `TMPDIR` is set. The r70 self-demo is unchanged.
5. **(g) D5 — the battery's duplicate-id case.** The filed case `mutant-duplicate-id` is killed by
   snapshot reuse, not by the id clause (the r71 erratum-(d) class recurring). A true in-place duplicate
   is added post-data as `mutant-duplicate-id-true`; the amended battery reads 12 cases / 12 passed
   (`before/control/battery-amended.txt`) and the new case prints `duplicate-id` + `ids-not-contiguous`
   with `met=0`. The filed 11-case receipt stays as filed.
6. **(h) D6 — stagnation-window arithmetic.** The declaration says "window at 2 of 3". `AXES.md` counts
   rounds *without* a new capability, and the lane's own r68/r70/r71 declarations read "1 of 3" in the
   same position, so the correct reading is **1 of 3**. No duty changes: depth is 8, below the
   saturation line 9, so the lowest-axis duty binds either way.
7. **(i) D7 — the census command is named:** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
   validate --root /home/vgpnk/Projects/shokunin tsukuroi` (rc 0), and the after receipt prints it.
8. **(j) D8 — instrument docstrings.** `battery.py` says "eleven mutants" and builds ten (11 cases);
   `routed-battery.py` says "three red mutants" and defines four (5 cases). The prose is wrong, the
   counts in the declaration are right, and the frozen bytes are not rewritten.
9. **(k) D9 — base vs provenance.** Every `before/` receipt was measured against `a7015d27` and committed
   with the declaration at `6b42676`; the declaration's phrase "all under `before/` at base `a7015d27`"
   conflates the measurement base with the commit that carried the files.

Named limits from the same wave, not repaired: (i) the C1 counter has no entailment channel (a row that
negates its snapshot reads `met=1`; `K1Critic` control 1); (ii) a `kind=community` row at tier A passes
(`R1Reviewer` F4); (iii) the `--selftest` suite tests the tool's own core, so a replacement tool that
prints the expected lines can fake its own verdict (`K1Critic` control 2) — the defence is the committed
expected-verdict and red-before receipts, not the summary line; (iv) C3 accepts a denial block (item 2).

## Round 72 — measured outcome (2026-11-03, measured revision `f79de557b0d556e445be3141a864f6c58c0242fd`; author-side, non-author closure pending)

Wave w1: one v1 wave, **12 seats** (scout 1 / executor 3 / scribe 3 / connector 1 / reviewer 2 /
critic 1 / mutation-tester 1; strict attack seats 4/12 = 33 %; connector 1; the L1 held the planner
seat; residual 0). Seat reports: `S1Scout`, `E1Mirror`, `E2GateSelftest`, `E3Routed`, `SC1Entry`,
`SC2Sources`, `SC3Index`, `C1Connector`, `R1Reviewer`, `R2Reviewer`, `K1Critic`, `M1Mutation` — all
twelve landed substantive files under `.ufo/waves/round-72/{w1,probes}/`.

| Claim | Before (base `a7015d27`) -> after (measured revision) | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (lowest tied, 8; SOURCED — S301-S303) | note `cat-file` rc **128** -> present; MD rows **0** -> 6; counter over the base tree `MD_NOTE absent` rc **128** -> `MD_ROWS=6 MD_VERIFIED=6 MD_SOURCES=3 MD_SNAPSHOTS=3 MD_MALFORMED=0`, `met=1`, rc 0; registry **300 -> 303** (`NF=13` each); knowledge notes **89 -> 90**; canonical census rc **0** | **verified** on the frozen predicate (author-side) | depth **8 -> 8**: one new mechanism on ground the province never held (the configuration surface beside the r71 parameter surface); no ordinal uplift claimed |
| C2 operability (9; capability `gate-selftest`) | `--selftest` rc **2**, **0** case lines -> rc **0**, `SELFTEST: PASS (9 cases, 9 passed, 0 failed)` with nine named ids; missing `$TMPDIR` rc **2**; committed red-before recipe rc **1** with `SELFTEST-MISMATCH` and `SELFTEST-MIXED` failing; r70 self-demo unchanged (`added_figures_mismatched=0 receipt_cases=214 receipt_labels=18`, rc 0) | **verified** on the frozen predicate (author-side); the L1's first fixtureless version was replaced by the wave's file-fixture patch and the suite is shown able to fail | operability **9 -> 9** (no uplift; the capability enters the table) |
| C3 freshness (9) | `ROUTED_STALE=3` rc **1** -> `ROUTED_STALE=0` rc **0**; the receipt's summary equals a fresh `count-mp-rows-r71.py --revision 2b358d2d` run, the SCORECARD erratum names receipt + revision, and the note correction enumerates the five `/usr/lib/modprobe.d` names and the superseded four figure | **verified** on the frozen predicate (author-side); three checker defects the wave found are repaired with probes (`probes/L1C3/probes.txt`) | freshness **9 -> 9** (no uplift; the routed defects close) |

Counting commands (outputs in `.ufo/waves/round-72/after/`):

```
python3 tools/count-md-rows-r72.py --revision f79de557        -> MD_VERIFIED=6 MD_SOURCES=3 MD_SNAPSHOTS=3 met=1, rc 0
git show f79de557:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3,}' -> 303
git ls-tree --name-only f79de557:corpus/knowledge | grep -c '\.md$' -> 90
python3 tools/check-selftest-tally.py --selftest             -> SELFTEST: PASS (9 cases, 9 passed, 0 failed), rc 0
TMPDIR=/nonexistent/x python3 tools/check-selftest-tally.py --selftest -> rc 2
bash .ufo/waves/round-72/after/redbefore-mutant.sh           -> rc 1
python3 tools/check-r71-routed-r72.py --revision f79de557    -> ROUTED_STALE=0, rc 0
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi -> rc 0
```

**Capabilities — round 72 entry.**

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| gate-selftest | A registered gate proves its own behaviour on hermetic fixture files written under `$TMPDIR`: nine named cases, stable finding ids (`SWEEP-MISMATCH`, `SWEEP-LABEL`, `SWEEP-NO-RECEIPT`), an explicit `SELFTEST-TMPDIR` failure with rc 2 when `$TMPDIR` names no directory, and a committed red-before recipe that fails when one arm is disabled | `python3 tools/check-selftest-tally.py --selftest` -> PASS 9/9; `.ufo/waves/round-72/after/redbefore-selftest.txt` rc 1 | round 72 |

Named limits, recorded and not smoothed:

- **C1's statement channel is lexical** (`R1Reviewer` F3, `K1Critic` control 1): a row that negates its
  snapshot while keeping the vocabulary reads `met=1`. The counter checks grounding, binding and
  provenance, never entailment; row semantics rest on R1Reviewer's six `holds` verdicts and the closure
  judge.
- **A `kind=community` row at tier A passes** (`R1Reviewer` F4): the counter reads `kind` but not `tier`;
  carried into the next round's counter debt.
- **Eleven of sixteen C1 source mutants survive the committed battery** (`probes/M1Mutation/score.md`):
  five clause removals are killed by the battery, the rest only by clause-isolated fixtures the battery
  does not carry; the added `mutant-duplicate-id-true` kills the id clause but not `c1-contiguous-drop`.
- **The `--selftest` suite tests the tool's own core** (`K1Critic` control 2): a replacement tool that
  prints the expected lines can fake its own verdict; the defence is the committed expected-verdict and
  red-before receipts, not the summary line.
- **C3 verifies naming, not entailment** (`R2Reviewer` medium, erratum item 2): a block that names the
  receipt and revision while denying the repair still reads `ROUTED_STALE=0`; correction substance rests
  on the non-author review.
- **Wave lineage**: the C1 note and registry rows are the SC1Entry/SC2Sources drafts; the SKILL/PROVINCE/
  README text is the SC3Index drafts; the C2 `--selftest` is E2GateSelftest's patch (the L1's first
  version was fixtureless); the C3 receipt and correction text are E3Routed's drafts; the three C3
  checker repairs answer E3Routed's and R2Reviewer's attacks.

**Tip re-run.** Every counting command above was re-run at the landing tip `1b27bffc` and reads the
same values (`MD_VERIFIED=6 met=1` rc 0; `SELFTEST: PASS (9 cases, 9 passed, 0 failed)` rc 0; missing
`$TMPDIR` rc 2; red-before rc 1; `ROUTED_STALE=0` rc 0; 303 registry rows; 90 notes; census rc 0) —
`.ufo/waves/round-72/after/measure-1b27bffc.txt`.

**C2 instrument superseded in-round (append-only).** The outcome above records the C2 `--selftest` at
nine cases (instrument sha256 `af46203c…`). `E2GateSelftest` then filed a v2 delta closing the case-set
hole `M1Mutation` named: a tenth case, `SELFTEST-CASES`, fails when a declared case row is deleted and
prints observed vs declared ids. The landed tool is **10 cases, 10 passed, 0 failed** (sha256
`f22eb94f1ed86157d94875d0943b5ec62fba8214dd520e7eb4d645969b283464`), its after receipt is
`.ufo/waves/round-72/after/selftest-selftest-after.txt`, and the committed red-before recipe still
fails (`SELFTEST-MISMATCH`, `SELFTEST-MIXED`; rc 1). The frozen target `N >= 7` and the r70 self-demo
(`added_figures_mismatched=0 receipt_cases=214 receipt_labels=18`, rc 0) are unchanged.


## Round 73 — declaration (frozen before data; append-only)

Base `eb1057575d5d8b940c4846e21611674cf5571aea` (round-72 verifier spot-check). **Lowest non-retired
axis: depth (8, tied with adjacency 8)**; saturation line 9, window 3. A capability entered at round 72
(`gate-selftest`), so the stagnation window stands at 1 of 3 and the nudge does **not** waive the
lowest-axis duty. Two claims on two axes: C1 depth, C2 freshness.

**Held-ground sweep (QUALITY 102b; `.ufo/waves/round-73/before/held-ground.txt`, run at the base).**
`git grep -nE 'unit_load_dropin|dropin_paths|unit_need_daemon_reload|null_or_empty|unit_file_mask|
config_parse_alias' -- corpus/ SKILL.md PROVINCE.md` reads **0 lines**; `unit load path`, `unit search
path`, `FragmentPath` and `DropInPaths` read **0 files**; `UnitFileState` reads 4 files and `drop-in` 19
files, but every `corpus/knowledge/` hit is a host observation of a named drop-in file
(`systemd-user-plane.md:29,44`, `kill-event-deep-r8.md:258,263`, `degraded-triage-r4.md:358`) or an
mkinitcpio hook context — none states the systemd merge, precedence or mask rules this round claims.
The ground is therefore **the merge/precedence plane beside held drop-in observations**, not a restated
existing note.

**Sources pinned before the declaration text** (`.ufo/waves/round-73/before/src/`, byte-exact, systemd
**v262**, the tag matching the host's installed 262.1-1-arch):

| snapshot | URL (tag v262) | sha256 |
|---|---|---|
| `systemd.unit.xml` | `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml` | `eb9479be…f82714c6` |
| `unit.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c` | `47e98d39…42a92efcb7` |
| `install.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/install.c` | `c11cd575…e6ef4d` |

`SHA256SUMS` and `SOURCES.json` (map of url + sha256 per snapshot) are committed with them; the counter
pins every digest it accepts. Host readings for the plane are committed in `before/host.txt` (search-path
list, 2 masked units on `/dev/null`, `user@1000.service` reading both a template and a prefix drop-in,
`getty@tty1.service` resolving to `getty@.service`).

**(a) Do-nothing controls** (`before/absence-controls.txt`): the note `git cat-file -e` rc **128**; the
frozen counter over the base tree prints `UL_NOTE absent` rc **128**; `git show eb105757:corpus/README.md
| grep -c 'UL[0-9]'` reads **0**; the routed checker at base reads `ROUTED_STALE=3` rc **1**; registry
**303** rows, **90** knowledge notes, **120** lesson files.

**(b) Frozen instruments.** `tools/count-ul-rows-r73.py` sha256
`542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6`, `--selftest` **11 cases** (1 control
+ 10 mutants: short statement, unregistered source, absent quote, five rows, duplicate id, snapshot reuse
3, ungrounded statement, malformed hidden row, digest swap, own-work source), each mutant asserting a
named finding token, fixtures copied under one `$TMPDIR` root. `tools/check-r72-routed-r73.py` sha256
`93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e`, `--selftest` **5 cases** (control +
lesson/digest/capability missing + an unanchored prose mention that must not satisfy a block check).
**Instrument-change rule for this round, frozen now** (the round-72 routed defect class): if a wave
attack changes either instrument after data, the before control is re-run with the final instrument and
both revisions are cited in an appended erratum naming old→new digests, so the before→after pair is
same-instrument evidence.

| # | axis/type | claim | before → after (frozen predicate) | counting command | kill rule |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S304–S306) | `corpus/knowledge/systemd-unit-load-plane-r73.md` states the systemd unit-load merge plane this lane never held: unit files load from a compiled path where an earlier directory's file overrides the same name lower in the list and `SYSTEMD_UNIT_PATH` replaces the whole path; drop-in `.conf` files merge in alphanumeric order after the unit file, `/etc` beats `/run` beats `/usr/lib`, drop-ins beat unit files wherever located, and different names are ordered lexicographically across directories; a loaded unit needs a daemon reload when its drop-in path list changes or a drop-in is newer than the last reload, and masked drop-ins are omitted from that list; a masked unit stays masked while its fragment path is null or empty, so a zero-size file and a `/dev/null` symlink both keep the masked state; the mask operation writes a `/dev/null` symlink and the install mode distinguishes `masked` from `masked-runtime`; and `[Install] Alias=` is parsed at enable time while an alias to a missing unit is unresolvable and ignored | `UL_NOTE absent` rc **128**, 0 UL rows, registry 303, notes 90 → `UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `met=1`, rc **0**; registry 303 → **306**, notes 90 → **91**, canonical census rc 0 | `python3 tools/count-ul-rows-r73.py --revision <REV>` | any row fails a frozen clause (id, statement words, grounding, source kind, digest/map/URL/anchor binding, quote location or length), fewer than 6 rows / 3 sources / 3 snapshots, or any snapshot cited more than twice → `met=0`, rc 1 |
| C2 | freshness (9) | the three round-72 closure defects routed to this lane close in committed bytes: `corpus/lessons/round-72.md` carries an appended correction naming both superseded sentences ("No capability row enters this round", "nine hermetic cases") and the landed `gate-selftest`/ten-case state; `SCORECARD.md` carries an appended erratum naming `R72-C3-INSTRUMENT-DIGEST-DRIFT` with the instrument digest old→new (`df8a59c7…` → `2610ff43…`) and the same-instrument before/after receipt; and an appended capability refresh restates `gate-selftest` as ten cases with its receipt pointer | `ROUTED_STALE=3` rc **1** (all three items stale) → `ROUTED_STALE=0 ROUTED_OK=3/3` rc **0** | `python3 tools/check-r72-routed-r73.py --revision <REV>` | any item unsatisfied inside an appended line-anchored block → `ROUTED_STALE>0`, rc 1 |

Causal separability: C1 touches only its note, three registry rows and its counter receipts; C2 touches
only the round-72 lesson correction, one SCORECARD erratum block and one appended capability refresh.
Each verifies without the other having landed (the counters are independent and read different files).

Routed repairs this round as work, not as claims: **R72-GATE-NO-REJECT** — this round's Gate records at
least one refused candidate with reason and flip condition (see `corpus/lessons/round-73.md`); the defect
is reported, not folded into C2's predicate, because a sources-gate rejection is produced by C1's work.

Assimilation: **none** — the open L0 `tsukuroi | round-64` rule keeps the `merge/tsukuroi/` package
quarantined (collision set S200–S281 against a registry now at S303); nothing is adopted. `considerthese`:
no proposal is still unimplemented in the latest file (`considerthese/2026-10-26.md`) — the
counter-attack scoreboard (r41+), the seat-harm tally (r66), the downstream patch-offset check (QUALITY
103, r69), the burst-aware reading record (r46) and the cross-note propagation map (r43/r54, recorded
partial) are all accounted for; the status is restated in the lesson.

Wave w1: one v1 wave, band 8–16, **12 seats** (scout 1 / executor 3 / scribe 3 / connector 1 / reviewer
2 / critic 1 / mutation-tester 1; strict attack 4/12 = 33 %); the L1 holds the canonical planner seat.

**planned (next round):** the C1 counter's entailment channel (a row that negates its snapshot reads
`met=1`); the three held drop-in observations (`faster-shutdown.conf`, `app-walker@autostart.service.d/`)
re-bound to the new merge rules as sources; the `install.c` alias rows' host-side blank (no alias symlink
is read this round); no amendment of this round's frozen predicates.

## Round 73 — C2 instrument repair (appended mid-wave; the frozen predicate text is unchanged)

The C2 checker was hardened after the wave's attack receipts, under the declaration's own item (b)
("if a wave attack changes either instrument after data, the before control is re-run with the final
instrument and both revisions are cited in an appended erratum naming old→new digests"). The predicate
sentence, the target `ROUTED_STALE=0` and the kill rule are untouched; only the instrument's bytes moved.

- **old → new.** `tools/check-r72-routed-r73.py` `93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e`
  → `328a6bf60c5237fe4ba857b36d2b4401833a61b933f735ec468139b7531a03fe`.
- **what the attacks proved** (`w1/R2Reviewer/report.md` F2/F4/F6/F7, `w1/E2Routed/receipts/`): the frozen
  bytes matched required tokens as substrings (`often` satisfied "ten"; `…selftest-selftest-after.txt.bak`
  satisfied the receipt path), never read the receipt they named, could not order the two digests, and
  accepted a keyword list with no supersession sentence.
- **what changed.** Tokens now match as whole tokens, and path-shaped tokens additionally reject a
  neighbouring path character (F4, F7); the digest item requires the old digest to precede the new one
  with a direction token between them (F2); the two receipt-bearing items require the named receipt to
  exist at the same revision and report at least ten cases (F4); the lesson item requires a supersession
  verb in its body, id label excluded (F6); `--selftest` grows from five to eleven cases
  (SUPERSTRING, RECEIPT-MISSING, RECEIPT-NINE, SUBSTRING-TEN, DIGEST-REVERSED, VACUOUS).
- **same-instrument before control re-run with the final bytes**
  (`.ufo/waves/round-73/after/c2-before-final-instrument.txt`): `--revision eb105757` →
  `ROUTED_STALE=3` rc 1; `--revision a7015d27` → `ROUTED_STALE=3` rc 1; `--selftest` →
  `SELFTEST: PASS (11 cases, 11 passed, 0 failed)` rc 0.
- **process defect, recorded not smoothed.** The instrument was edited in the worktree before this block
  existed, and `S1Scout` observed two intermediate digests (`316dd51a…`, `f1c4b4d3…`) against the then-
  declared `93f034e3…` and the missing SCORECARD record (`w1/S1Scout/report.md` §8). The class and the fix
  are the round lesson's `R73-INSTRUMENT-MIDWAVE` mistake: the erratum must precede the first repair
  commit and name each intermediate digest, not follow the edit.
- **remaining limit, still not provable lexically.** A block that keeps every token while *denying* the
  repair reads `ROUTED_STALE=0` (R2Reviewer F1/F2 and the round-72 named limit); the direction rests on a
  non-author reading of the landed sentences, which this round records rather than claims.

## Round 72 — instrument digest erratum (appended round 73; R72-C3-INSTRUMENT-DIGEST-DRIFT)

The round-72 declaration froze `tools/check-r71-routed-r72.py` at sha256
`df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712` (`SCORECARD.md:5616`). That value was
the tool's true digest at the declaration commit `6b426762`; the tool then changed in the wave's repair
commit `53bcddef` (`2610ff43…`), changed again at `123e1c57` (`b17fddfa…`), and has been
`2610ff433bf5d4e945ce5b2da0cf168745e4142ecffabc3d160afee33005cdcc` from `7fb35c74` through the present
tip. No erratum recorded the drift; the round-72 erratum described the three repairs (unanchored block,
receipt provenance, five-path token list) without a digest old→new. The instrument moved from
`df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712` to
`2610ff433bf5d4e945ce5b2da0cf168745e4142ecffabc3d160afee33005cdcc`, and this block is the record.

**Same-instrument evidence, re-run with the final instrument**
(`.ufo/waves/round-73/after/r72-c3-same-instrument-before.txt`): `python3
tools/check-r71-routed-r72.py --revision a7015d27` (pre-repair data) reads `ROUTED_STALE=3` rc 1 and
`--revision eb105757` (post-repair data) reads `ROUTED_STALE=0` rc 0, with the tool's bytes
`2610ff43…` on both sides. `--revision` selects only the data revision the tool reads, and the tool
does not exist at `a7015d27` at all (it is a round-72 artifact), so the pair is same-instrument in the
only sense available: one committed instrument, two data revisions. The frozen `df8a59c7…` is
superseded by `2610ff43…`. Counted by `python3 tools/check-r72-routed-r73.py --revision <REV>` (item
DIGEST).

## Capability refresh — round 73 (append-only)

The `gate-selftest` row above (round 72) still reads "nine named cases" and `PASS 9/9`. The landed
instrument prints **ten** cases: `SELFTEST: PASS (10 cases, 10 passed, 0 failed)` (receipt
`.ufo/waves/round-72/after/selftest-selftest-after.txt`, tool sha256 `f22eb94f…`), the tenth being
`SELFTEST-CASES`, which fails when a declared case row is deleted. Read the row with this line as its
current count; the row's own text stays as filed (QUALITY 99). Counted by
`python3 tools/check-r72-routed-r73.py --revision <REV>` (item CAPABILITY).

## Round 73 — final instrument digests (appended after the last repair; append-only)

The instrument-repair block above records the first hardened state (`328a6bf6…` / the counter at
`84501ab8…`). Two later changes landed before this round's commit, both recorded here so every state the
wave observed is named:

| instrument | declared | intermediate | final (committed) | last change |
|---|---|---|---|---|
| `tools/count-ul-rows-r73.py` | `542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6` | `84501ab8d4968293de8b38f68a9f53d658535d90df8191cbd96a20df98e94832` (EMPTYQUOTE repair: `MIN_QUOTE_WORDS=4` + a twelfth selftest case) | `97f6f5ec83401b02d6c83b48bcad27f0f97c06c9e4ad134cc1cbfb202dbb03d0` | exit-map docstring now names 128 and the `--selftest`-only 2 (SC3Index F4) |
| `tools/check-r72-routed-r73.py` | `93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e` | `328a6bf60c5237fe4ba857b36d2b4401833a61b933f735ec468139b7531a03fe` (whole-token and path-token matching, digest direction, receipt existence and count, supersession verb; eleven selftest cases) | `71931c1c225ecda5f8b6529091dc9383542d0c054ae62ff6e0a16f3fbe51496e` | exit-map docstring now says 2 is `--selftest`-only and an absent file is rc 1 (SC3Index F2) |

Every before→after pair in this round was re-run with the FINAL bytes: the C1 before control at `eb105757`
is still `UL_NOTE absent` rc 128 and the after is `met=1` rc 0 (a tighter instrument can only lower the
after, and the six rows pass it); the C2 before control is still `ROUTED_STALE=3` rc 1 at `eb105757` and
`ROUTED_STALE=0` rc 0 after (`.ufo/waves/round-73/after/c2-before-final-instrument.txt`). Selftest tallies
at the final bytes: counter `SELFTEST: PASS (12 cases, 12 passed, 0 failed)`; checker
`SELFTEST: PASS (11 cases, 11 passed, 0 failed)`.

## Round 73 — measured outcome (2026-11-03, measured revision `583eea87627353d6e21037216e316af8e19bdf4d`; author-side, non-author closure pending)

Wave w1: one v1 wave, **12 seats** (scout 1 / executor 3 / scribe 3 / connector 1 / reviewer 2 / critic 1 /
mutation-tester 1; strict attack seats 4/12 = 33 %; connector 1; the L1 held the planner seat; residual 0).
Seat reports under `.ufo/waves/round-73/w1/`; the two v1 instruments were hardened by the wave's own attacks
and their final digests are in "Round 73 — final instrument digests" above.

| Claim | Before (base `eb105757`) -> after (`583eea87`) | Verdict | Axis verdict |
|---|---|---|---|
| C1 depth (lowest tied, 8; SOURCED — S304-S306) | note `cat-file` rc **128** -> present; UL rows **0** -> 6; counter over the base tree `UL_NOTE absent` rc **128** -> `UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `met=1`, rc 0; registry **303 -> 308** (`NF=13` each); knowledge notes **90 -> 91**; canonical census rc **0** | **verified** on the frozen predicate (author-side) | depth **8 -> 8**: one new mechanism on ground the province never held; no ordinal uplift claimed |
| C2 freshness (9) | `ROUTED_STALE=3` rc **1** -> `ROUTED_STALE=0 ROUTED_OK=3/3` rc **0**; each item inside a line-anchored appended block with whole tokens, a digest direction and a receipt reporting ten cases; same-instrument before control re-run with the final bytes at `eb105757` and `a7015d27` (`after/c2-before-final-instrument.txt`); the r72 checker's own 3 -> 0 pair re-run at `a7015d27`/`eb105757` (`after/r72-c3-same-instrument-before.txt`) | **verified** on the frozen predicate (author-side) | freshness **9 -> 9** (no uplift; the routed defects close) |

Counting commands (outputs in `.ufo/waves/round-73/after/`):

```
python3 tools/count-ul-rows-r73.py --revision 583eea87   -> met=1, rc 0
python3 tools/count-ul-rows-r73.py --revision eb105757   -> UL_NOTE absent, rc 128
python3 tools/check-r72-routed-r73.py --revision 583eea87 -> ROUTED_STALE=0 ROUTED_OK=3/3, rc 0
python3 tools/check-r72-routed-r73.py --revision eb105757 -> ROUTED_STALE=3, rc 1
git show 583eea87:corpus/SOURCES.md | grep -cE '^ {0,3}\| *S[0-9]{3,}' -> 308
git ls-tree --name-only 583eea87:corpus/knowledge | grep -c '\.md$' -> 91
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi -> rc 0
```

**No capability row enters this round.** Both instruments are per-round gates whose objects are this round's
note and this round's routed defects; C2 is a repair of an existing gate (`routed-defect checker`), not a new
repertoire entry, and the round adds no reusable mode the lane did not already hold. The counter's twelfth
selftest case and the checker's eleven are counted in their registry rows, not as capabilities.

Named limits, recorded and not smoothed:

- **The C1 counter is a form instrument** (K1Critic D3, R1Reviewer A/B/C/E): grounding is lexical, so a
  word-salad statement, a quote lifted from an unrelated region and an anchor without a line range all read
  `met=1`; row truth rests on R1Reviewer's per-row verdicts (`ROWS_HOLD` 2/6 on the draft, 6/6 after the
  corrections) and on the closure judge, never on the counter alone.
- **The counter carries an admissible answer key** (K1Critic D2): `SAMPLE_ROWS` is in the tool; the landed
  note's rows are not identical to it (`IDENTICAL=0`, `after/final-checks.txt`), but a future writer could copy
  the sample — next round's fix is synthetic self-test snapshots.
- **C2's denial leg is not provable lexically** (R2Reviewer F1/F2): a block that keeps every token while
  denying the repair reads `ROUTED_STALE=0`; direction rests on a non-author reading of the landed sentences.
- **Both instruments were edited mid-wave** (R73-INSTRUMENT-MIDWAVE): the erratum and the final-digest block
  name every intermediate, but the order was wrong and the lesson records it.
- **Wave lineage.** The C1 note and its rows are SC1Entry's draft as corrected by R1Reviewer; the registry
  rows with their refusal measurements are SC2Sources'; the SKILL table, PROVINCE entry and README index are
  SC3Index's drafts with the counts corrected to the final instruments; the C2 repair drafts and tamper
  receipts are E2Routed's and R2Reviewer's; the EMPTYQUOTE repair answers E1Counter; the host readings were
  re-measured by S1Scout, R1Reviewer and SC3Index with no delta.

**planned (next round):** the counter's answer-key channel (synthetic self-test snapshots, K1Critic D2); the
counter's entailment channel (a row whose quote does not support its statement); the duplicate-registry-id
channel E1Counter proved (`§D2`, a later row silently shadows an earlier duplicate); the three held drop-in
observations (`faster-shutdown.conf`, `app-walker@autostart.service.d/`) re-bound to the new merge rules as
sources; no amendment of this round's frozen predicates.

## Round 73 — C2 instrument, final bytes and the r72 digest-order correction (append-only)

Appended after the wave's last attack receipt. Two records are corrected or completed here; no frozen
predicate text changes.

1. **The r72 digest order in "Round 72 — instrument digest erratum" above is wrong.** The correct order of
   committed bytes for `tools/check-r71-routed-r72.py` is: `6b426762` `df8a59c7…` (the declaration's true
   value) → `123e1c57` `b17fddfa…` → `53bcddef` `2610ff43…` → `7fb35c74` through the present tip
   `2610ff43…`. The earlier sentence reverses `123e1c57` and `53bcddef`; `123e1c57` (22:41) is the
   ancestor and `53bcddef` (22:44) its child (`git log --reverse 6b426762..53bcddef` shows
   `123e1c57` first). The erratum's substance — the declaration's digest was true when written and the tool
   drifted afterwards without a record — is unchanged.
2. **The checker's final bytes** are `731841988c6943370bc6e863b7f72cd8bd85a626ec7f2f989eb422b4c6d82f0b`
   (states: declaration `93f034e3…`, hardening `328a6bf6…`, exit-map docstring `71931c1c…`, final below).
   The last repair answers E2Routed's own traps against `71931c1c…`: a correct **absolute** receipt path was
   rejected by the path-token lookbehind (it now permits a preceding `/` while still refusing a longer path
   suffix), a `SELFTEST: FAIL (N cases…)` receipt satisfied the receipt gate (it now requires `PASS`), and a
   bare `## Correction (placeholder)` heading could swallow a later `###` section (blocks are now split at
   `## ` and `### `). `--selftest` grows to **thirteen** cases (RECEIPT-FAIL and PLACEHOLDER added).
3. **Control re-run on the final bytes** (`.ufo/waves/round-73/after/c2-final-instrument.txt`):
   `--revision eb105757` → `ROUTED_STALE=3` rc 1; `--revision a7015d27` → `ROUTED_STALE=3` rc 1;
   `--revision 583eea87` → `ROUTED_STALE=0 ROUTED_OK=3/3` rc 0; `--selftest` →
   `SELFTEST: PASS (13 cases, 13 passed, 0 failed)`; an absolute-receipt fixture reads `ROUTED_STALE=0`.
4. **Still a named limit:** the denial leg. A block that keeps every token while contradicting it reads 0/3
   (R2Reviewer P4b, E2Routed's final message); direction rests on a non-author reading, never on this check.

## Round 73 — instruments at wave close (append-only)

M1Mutation's clause-isolated batteries (38 mutants: 21 against the counter, 17 against the checker) found two
further defects after the block above: the counter crashed with a traceback on a non-map `snapshots` value
(rc 1 instead of a finding), and the checker accepted a defect id placed only in a block heading. Both are
fixed and each carries a new selftest case.

| instrument | state at the block above | final at wave close | what changed |
|---|---|---|---|
| `tools/count-ul-rows-r73.py` | `97f6f5ec…` (12 cases) | `1f22c26b95c52be745a8cdd97ec52ebf06a362f697daf2a8e1e0d77e28f3e643` (13 cases) | non-map `snapshots` now reads `UL_MAP malformed` rc 1 instead of raising; case `MAPLIST` |
| `tools/check-r72-routed-r73.py` | `73184198…` (13 cases) | `ad853877bd4d5117d0ee356f346f3bf515c0b064fd1e9ed8bc670ac97295a281` (14 cases) | required tokens must sit in the block body; only the defect id may label the heading; case `TITLE-TOKEN` |

Re-run at the final bytes (`.ufo/waves/round-73/after/c2-final-instrument.txt`): counter `met=1` rc 0 over
the note, checker `ROUTED_STALE=0 ROUTED_OK=3/3` rc 0 over the landed blocks, `--revision eb105757` still
`ROUTED_STALE=3` rc 1, and both selftests pass (13 and 14 cases). M1Mutation's survivors are six dead or
entailed clauses (own-work arm, map-url, quote-pipe, snapshots conjunct, item-heading anchor, lesson
`need_any`), recorded in `w1/M1Mutation/report.md`.

## Round 74 — declaration (frozen before data; append-only)

Base `d749a625f483c66f2a6f2005db3799630c776bc3` (round-73 verifier spot-check). **Lowest non-retired
axis: depth (8, tied with adjacency 8)**; saturation line 9, window 3. A capability entered at round 72
(`gate-selftest`), so the stagnation window stands at 2 of 3 and the nudge does **not** waive the
lowest-axis duty. Two claims on two axes: C1 depth, C2 freshness.

**Held-ground sweep (QUALITY 102b; `.ufo/waves/round-74/before/held-ground.txt`, run at the base).**
`git grep -nE 'unit_file_find_fragment|unit_ids_map_get|unit_file_build_name_map|unit_type_may_alias|unit_file_resolve_symlink|builtin_unit_lookup' -- corpus/ SKILL.md PROVINCE.md`
reads **0 lines** (exit 1). None states the unit-fragment resolution, alias filtering, or perpetual mask
immunity rules this round claims. The ground is therefore **the unit-fragment resolution plane**, not a
restated existing note.

**Sources pinned before the declaration text** (`.ufo/waves/round-74/before/src/`, byte-exact, systemd
**v262**, the tag matching the host's installed 262.1-1-arch):

| snapshot | URL (tag v262) | sha256 |
|---|---|---|
| `unit-file.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.c` | `141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd` |
| `load-fragment.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/load-fragment.c` | `a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5` |
| `unit-file.h` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.h` | `e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f` |

`SHA256SUMS` and `SOURCES.json` (map of url + sha256 per snapshot) are committed with them; the counter
pins every digest it accepts. Host readings for the plane are committed in `before/host.txt` (search paths,
masked units, template instances, systemd version 262.1-1-arch).

**(a) Do-nothing controls** (`before/absence-controls.txt`): the note `git cat-file -e` rc **128**; the
frozen counter over the base tree prints `UF_MAP absent` rc **128**; `git show d749a625:corpus/README.md
| grep -c 'UF[0-9]'` reads **0**; the routed checker at base reads `ROUTED_STALE=2` rc **1**; registry
**308** rows, **91** knowledge notes, **122** lesson files.

**(b) Frozen instruments.** `tools/count-uf-rows-r74.py` sha256
`94d46a5edfcdc00858a1b1c37bc459322fc7e337fba19cc38a85776d0dd36482`, `--selftest` **13 cases** (1 control
+ 12 mutants: short statement, absent quote, quote words > 25, non-contiguous id, unregistered source,
snapshot reuse > 2, ungrounded statement, malformed row, digest swap, own-work source, duplicate registry id,
non-map mapfile), using synthetic snapshots (no answer key). `tools/check-r73-routed-r74.py` sha256
`2da4ff1fd8e7ed1287230e43769a1d75233b992b9f04eeb77cc981f2677efd77`, `--selftest` **6 cases** (control +
missing lesson block + missing log block + missing both + title-only token + missing superseded count).
**Instrument-change rule for this round, frozen now**: if a wave attack changes either instrument after
data, the before control is re-run with the final instrument and both revisions are cited in an appended
erratum naming old→new digests, so the before→after pair is same-instrument evidence.

| # | axis/type | claim | before → after (frozen predicate) | counting command | kill rule |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S309–S311) | `corpus/knowledge/systemd-unit-fragment-plane-r74.md` states the systemd unit-fragment resolution plane this lane never held: unit search paths are processed in priority order with first-seen name registration ignoring lower duplicate filenames; unit symlinks reject self-aliases, require compatible instance/template types, and restrict aliasing to alias-capable unit types; `unit_type_may_alias` permits aliasing strictly for service, socket, target, device, and volume units; `UnitFileState` distinguishes enabled, linked, and masked states from their runtime variants; a fragment matching `null_or_empty` sets `UNIT_MASKED` and zero mtime except for perpetual units which are immune from masking; missing fragments for system-scope units fall back to `builtin_unit_lookup` while on-disk files and masks unconditionally override built-ins | `UF_NOTE absent` rc **128**; 0 UF rows; registry **308**; notes **91** → `UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0`, `met=1`, rc **0**; registry **313**; notes **92**; census rc **0** | `python3 tools/count-uf-rows-r74.py --revision <REV>`; `git show <REV>:corpus/SOURCES.md \| grep -cE '^ {0,3}\| *S[0-9]{3,}'`; `git ls-tree --name-only <REV>:corpus/knowledge \| grep -c '\.md$'` | any finding > 0, rows != 6, verified != 6, sources < 3, snapshots < 3, census != 0, registry < 313, notes < 92 |
| C2 | freshness (9) | the two round-73 closure defects routed to this lane close in committed bytes: `corpus/lessons/round-73.md` carries an appended correction naming `R73-GATE-QUOTE-LINE-DRIFT` with the S306 quote location install.c:2383 (superseding 2387) and the three S304 corrected line anchors (:368-370, :237-238, :238-239); and `LOG.md` carries an appended correction naming `R73-LOG-COUNT-STALE` with the superseded Round 73 mid-wave counts (12 and 11 cases) and restating the final committed instrument counts (13 and 14 cases) | `ROUTED_STALE=2` rc **1** (both items stale) → `ROUTED_STALE=0 ROUTED_OK=2/2` rc **0** | `python3 tools/check-r73-routed-r74.py --revision <REV>` | any item unsatisfied (`ROUTED_STALE > 0`) |

Causal separability: C1 touches only its note, five registry rows, and its counter receipts; C2 touches
only the round-73 lesson correction and one LOG.md correction entry. Each verifies without the other
having landed (the counters are independent and read different files).

## Round 74 — declaration errata and attack dispositions (append-only)

1. **R74-DECL-ALIAS-SET (R1Reviewer F1).** C1's frozen clause incorrectly says
   "service, socket, target, device, and volume". The pinned `unit-file.h:25-32` says
   SERVICE, SOCKET, TARGET, DEVICE, TIMER, PATH. The note states that true set.
   **C1 as literally declared is not verified, even if the mechanical counter reaches met=1.**
   No replacement predicate, retroactive amendment, or depth score uplift is claimed.
2. **R74-BASE-OID (R1Reviewer F2).** The declaration and dispatch's full base suffix is erroneous:
   `d749a625f483c66f2a6f2005db3799630c776bc3` does not exist. The real base is
   `d749a625b3054b7cb3435983fb9626ab3d0ed0c4`, parent of declaration `e51fb49d`.
   The actual before receipt ran the resolving short `d749a625`; use that real object.
   A missing-object run produces the same counts for the wrong reason (R1Reviewer receipt).
3. **K1Critic D2 (sizing).** Three mined note-grounding sources S309-S311 plus two opened
   refusals S312-S313 produce the frozen five-row registry increase, 308→313. Source count 3
   is not total registry-row count 5; no threshold changes.
4. **K1Critic D1/D7.** The snapshot conjunct is entailed by six rows and reuse cap two;
   the own-work disjunct is entailed by exclusion from KINDS. These are named redundancy,
   not independent sensitivity evidence. The instruments remain frozen unchanged.
5. **R2Reviewer HIGH-1 / E2Routed F1.** A headed EOF LOG correction is shadowed by the
   existing Round-73 block. The landed repair uses E2Routed Form A, an unheaded append
   inside that last block; it is honest append-only prose and meets the frozen checker.
6. **Named limits, not repaired in the frozen instrument:** C1 lexical overlap admits
   negation, unanchored quotes, duplicate content and a scripted non-reader (E1Counter);
   C2 substring matching admits numeric superstrings, inverted direction, wrong tool
   attribution and token dumps (R2Reviewer/K1Critic). C2 selftest contains a literal answer
   key (K1Critic D3). Mechanical success alone is not semantic admission. R1Reviewer
   reviewed the six true rows independently; C2's repair prose is read directly.
7. **Protocol-load defect.** Required protocol/skill loading was completed after freeze
   and dispatch rather than before; that cannot be repaired retroactively. The initial
   wave context also omitted the explicit scratch and pacman guard paragraphs. No package
   transaction or host service write was authorized or executed by the L1. Report these
   conformance defects; do not claim flawless protocol compliance.

## Round 74 — measured outcome (author-side honest stop)

Measured commit `dc5114c5eb8e6349780d7bca8eb6e7470ec55553`; receipt
`.ufo/waves/round-74/after/measure-dc5114c5.txt`. Same frozen instruments at both revisions.

| Claim | Before (real d749a625) | After (dc5114c5) | Score / verdict |
|---|---|---|---|
| C1 depth | UF_MAP absent, rc 128; registry 308, notes 91 | UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0 met=1, rc 0; registry 313, notes 92; census rc 0 | 8→8; **not verified as declared**, wrong volume clause despite mechanical target met |
| C2 freshness | ROUTED_STALE=2 ROUTED_OK=0/2, rc 1 | ROUTED_STALE=0 ROUTED_OK=2/2, rc 0 | 9→9; repair verified mechanically and by direct reading; numerical uplift not claimed |

Commands: `python3 tools/count-uf-rows-r74.py --revision <REV>` and
`python3 tools/check-r73-routed-r74.py --revision <REV>`. Count registry rows by
`git show <REV>:corpus/SOURCES.md` matching `^ {0,3}\| *S[0-9]+ *\|`; count `.md`
names from `git ls-tree --name-only <REV>:corpus/knowledge`. The receipt records exact revisions.
Selftests counter 13/13, checker 6/6; digests remain 94d46a5e… and 2da4ff1f….

No new capability row; no score changes on other axes. Wave 12/12 settled (nine nonempty,
three empty finals), strict attack 4/12, connector 1. WAVE-DONE received before report.
No completed M1Mutation result is inferred. The correct source-backed note remains useful
but cannot retroactively satisfy the false frozen C1 sentence. **Round honest-stop.**
