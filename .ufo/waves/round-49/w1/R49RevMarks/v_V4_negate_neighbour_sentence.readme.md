# tsukuroi-shokunin — corpus

## Coverage map

| Note | Holds | Sources |
|---|---|---|
| `knowledge/package-state-plane.md` | pacman plane measured anchors: trust surface (`/etc/pacman.conf` — no version pins, single omarchy mirror, `[omarchy] SigLevel = Optional TrustAll`), census (1188 installed / 207 explicit / 16 foreign / 3 orphans), sync-db birth-vs-mtime trap (dbs born 2026-10-11 12:54:13.542; mtimes are upstream stamps), keyring (184 pub / 230 sub) + cache shape (8.6 G, never pruned), `-Qkk` rc semantics (0 = none, 1 = ≥1 altered) + non-root benign-altered decision table + full-sweep decomposition (86 backup-diff / 36 non-root / 17 metadata-drift lines; one content signal `powerprofilesctl`), unknowns (elephant channel provenance, root `-Qkk` delta) | live read-only probes 2026-10-14, host `plazir27`, non-root; commands embedded per section; landed round 1 |
| `knowledge/systemd-user-plane.md` | systemd user plane: manager state (both scopes `running`), unit inventory (`~/.config/systemd/user/` 7 units + 1 drop-in + 5 symlinks; `/usr/lib/systemd/user/` ships 109), timer plane (`ai-usage.timer` only active, `Result=success`), condition-gated units, boot err classes (entry-count discipline — line counts are a trap), coredump census (198 this boot: godot 142, node 47), method lessons, unknowns/errata | `systemctl --user` / `journalctl` / `coredumpctl` probes 2026-10-14; landed round 1 |
| `knowledge/driver-firmware-plane.md` | nvidia driver + firmware plane: loaded module census (`lsmod`), driver presence (`nvidia-open-dkms` 610.57.04, upgraded 2026-10-11), GSP firmware shape (presence/sizes only, contents never read), boot err/warn classes via `journalctl -k`, update candidates, obs/inf/unk split, errata (stale `7.1.4-arch1-1` dkms registration; unowned `nvidia.ko.zst` pacman cannot verify) | `lsmod`/`dkms status`/`modinfo`/`nvidia-smi --query-*` probes 2026-10-14; landed round 1 |
| `knowledge/update-safety-note.md` | update-safety plane, the `-Syu` go/no-go decision table: candidates empty three ways (`-Qu` rc=1 empty; `pacman -Sup --print-format` 0 lines; `expac -Q` vs `pacman -Sl` version join 1171 equal / 0 behind / 1 ahead — `1password-beta`, an operator provenance question); why empty ≠ up to date (channel-freshness gate: sync dbs born 2026-10-11, `-Sy` never run since); touch map (size/coupling of a candidate set); pins/holds (no IgnorePkg; `HoldPkg = pacman glibc` measured + what HoldPkg does not mean); shadowing/downgrade trap; hazard inventory feeding the decision table; obs/inf/unk split; append-only errata; boundary notes (`walker-restart.hook` root-exec reported → kagi/operator, not absorbed) | `pacman -Qu` / `pacman -Su* --print*` / `expac`-vs-`-Sl` join probes 2026-10-14 10:44:35–10:51:13, host `plazir27`, non-root; `pacman -Sy`/`-Syu` never run (the one non-obvious verb `-Su* --print*` builds a plan, no transaction); landed round 2 (TSUKUROI-R2-2) |
| `../tools/tsukuroi-census.sh` (round-2 gate, TSUKUROI-R2-1) | the lane's first executable health gate (census-v1, 744 lines / 743 `wc -l` newlines, md5 `7a3d3b94ecd73fbe1a9a98e9dc88b92f`): three owned planes probed read-only, emits `TSUKUROI_CENSUS: HEALTHY`/`DEGRADED`/`BLOCKED` + firmware-style exit map (0/1/2, worst-plane rollup); bounded `-Qkk` sample (default 8 — drift decides, sample rc never does), timer scan capped, kernel-ring error classes at entry count (oom/io/gpu/other), systemd scope `degraded`→DEGRADED refinement recorded at `:54-57`; hermetic `--selftest` on a fixture dispatcher asserting exit code + verdict + plane substring + fixture byte-unchanged (zero mutation) | plan `../plans/round-2.plan.md:3-9`; selftest re-run by scribe 2026-10-14: rc=0, `17 cases, 17 passed, 0 failed`; live re-run rc=1 → `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED)`; live mode writes nothing |
| `../tools/tsukuroi-census.sh` (round-3 gate, TSUKUROI-R3-2 — supersedes the v1 row above) | census-v2, the journal/boot plane joins the census (plan anchor `../plans/round-3.plan.md:3-11`; +259/−26 lines over v1): four owned planes, same vocabulary + exit map; new journal arms — boot record (`--list-boots` index-0 line), boot target (`systemctl is-active graphical.target`), boot err **entries** at `-o json` count with disjoint classes (coredump > kernel > other), failed-services history derived from the same journal stream (names units reset since — history the systemd plane cannot see), timer drift (enabled user timer not `ActiveState=active`); `coredumpctl` deliberately not probed (table parsing is the measured trap; the `systemd-coredump` entry class is the storm signal); kernel entries deliberately double-counted by drivers + journal, distinct value = non-kernel classes + boot record/target + timer armed-state (`:107-109`); anti-claim v2: journal unreadable read-only → the arm fails closed `BLOCKED`, remaining planes still report | plan `../plans/round-3.plan.md`; 976 lines, md5 `41953ee9f2099281c91759249fe8708f`; selftest re-run by scribe 2026-10-14 15:55Z: rc=0, `26 cases, 26 passed, 0 failed` (17 legacy + 9 journal); live re-run rc=1 → `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)`; live mode writes nothing (`git status` identical before/after, `/tmp/tsukuroi-b4-r3b-scratch/gate.out`) |
| `knowledge/journal-boot-plane.md` | journal/boot plane, the round-3 freshness move: 13-boot retained-journal census (per-boot err entries 1–168, boot 0 storm-dominated: 247→251 during capture, ≈207 coredumps); the boot-gap question measured for **every** retained boot — kernel phase = first-record monotonic − 0.81…0.84 s (12/12) with boot 0 wall-clock cross-anchor ±1 s, so the 4 m 03 s kernel phase is real elapsed time and the var-log.mount-delay hypothesis is refuted (mount happens at userspace 2.845 s, after PID1 logging start); leading hypothesis now initramfs/LUKS dwell [inference, unproven; crypttab BLOCKED shape-only]; failed-service history **0 unit failures in 13 retained boots** (strict pattern 0; 36 broad matches all portal RealtimeKit warnings); system timer plane 5/5 `Result=success`, every trigger inside its declared randomization/accuracy window; vendor-wants nuance (`disabled` ≠ will-not-run); `limine-snapper-sync` self-claim vs empty `snapper list-configs` reported to the update-safety plane, not absorbed; method lessons (entries-not-lines ≈256:1, `-g` no-match prints `-- No entries --` on stdout, monotonic timestamps are not deltas, pipelines hide rc, counts drift live in a storm); append-only errata; unknowns (dwell mechanism, `PM: Image not found` writer, effective journald retention) | `journalctl`/`systemctl show`/`systemd-analyze`/`coredumpctl`/`bootctl`/`getfacl` read-only probes 2026-10-14 11:39–11:58, host `plazir27`, non-root, no sudo; landed round 3 (TSUKUROI-R3-1, 411 ln, md5 `16d4047e8b03deec69773d2cc0b1b75c`) |
| `knowledge/host-health-report-r3.md` | the lane's end-to-end SHONEN task: census-v2 + the four plane notes + the update-safety note driven into one host-health snapshot — verdict board over the 5 surfaces (packages DEGRADED, systemd HEALTHY, drivers DEGRADED, journal DEGRADED, update-safety DEGRADED, rollup exit 1), **20 finding→action pairs** where every DEGRADED finding carries its measured evidence and its exact operator unblock action (P1–P5 packages, D1–D3 drivers, J1–J5 journal, U1–U8 update-safety), one-line receipts for HEALTHY planes, 15-row unknowns register with owners, measured read-only contract (`git status` before/after identical), per-artifact provenance with md5 + line counts, append-only errata (mid-flight gate revision consumed as settled v2, recorded not laundered) | live run 2026-10-14, gate census-v2 consumed at 14:57:13Z + v1 pre-revision snapshot 14:39:26Z, host `plazir27`, non-root; landed round 3 (TSUKUROI-R3-3, 462 ln, md5 `d701cf6f630363ce3228260ee17226a4`) |
| `knowledge/executor-test-sufficiency.md` | the no-oral-context test record (box-3 evidence): one executor seat ran census-v2 with `SKILL.md` alone (round-2 revision `f80b4afdf7e3c44f19a1bb04a2f9d1c1`, 444 ln) as the only reference; per-step sufficiency **7 `SUFFICIENT` / 3 `PARTIAL` / 3 `MISSING`** — the MISSING steps were exactly the v2 coverage (journal field rules S5d, post-verdict contract S6, the unresolved "20-min cap" item S8 recorded-not-invented), plus doc-staleness findings (S0 revision pin mismatch, S2 selftest count, S3 four-plane contract) produced by polling that confirmed the doc sync had not landed; findings kept intact here, fixes landed as the `SKILL.md` round-3 append (census-v2 sync, journal field map, scope fix 4-of-5, post-verdict contract, executor checklist); post-fix re-test not yet run | test run 2026-10-14 15:25:54–15:25:57Z (+PHASE B source cross-check; poll logs 14:40–15:29), host `plazir27`; landed round 3 (TSUKUROI-R3-4, 219 ln, md5 `4b2c1d3612db7db1477da92aaec39862`) |
| `knowledge/adjacency-handoffs-fleet-r1.md` + `.json` | Steered fleet round-1: source-backed ADJ-01..07 analysis-recipient contracts, persisted source digests, one OS-to-mori observation packet, GPU/helper negative controls and explicit lifecycle/ownership limits; inherited province/skill edits are not this round's authorship | `knowledge/adjacency-handoffs-fleet-r1.md` §2–§5; `lessons/round-1.md` Gate; historical rows above remain historical captures |
| `knowledge/arch-news-gate-2026.md` | the "read before upgrading" news gate (new surface, fleet round 1): 20 Arch news items 2025-01-01→2026-10-19 checked against this host by `pacman -Q`; 0 confirmed unconditional next-upgrade interventions, conditional checks kept explicit; operator action follows ArchWiki doctrine (full `-Syu`, never bare `-Sy`) | `../SOURCES.md` S001–S005, S010; re-run 2026-10-19 |
| `knowledge/pacnew-plane.md` | config drift `.pacnew`/`.pacsave` (new surface): log census 3 `.pacnew` / 0 `.pacsave` vs filesystem census of the same 3 files (12 unreadable dirs skipped and named); why both methods are needed (log is history, not state) | `../SOURCES.md` S010, S011, S032; re-run 2026-10-19 |
| `knowledge/initramfs-v42-sysroot-recovery.md` | boot recovery + initramfs build path (new surface): busybox-flavor evidence from the drop-ins, mkinitcpio v42 `/sysroot` change vs two `/new_root`-hardcoding hooks (`btrfs-overlayfs`, `plymouth`) [inf consequence], recovery entry points by stage; TPM2-news reading rejected | `../SOURCES.md` S002, S014–S017, S021, S022, S025, S026; re-run 2026-10-19 |
| `knowledge/snapper-eacces-mechanism.md` | rollback net: candidate mechanism for the recurring `errno:13` (`/` 0555 + `CapabilityBoundingSet=CAP_SYS_ADMIN` drops CAP_DAC_OVERRIDE) [inf, operator falsifier given], the `-Qkk` blind spot for `/`, ESP 2.0G vs ≥4 GiB recommendation; `@.snapshots` cause rejected | `../SOURCES.md` S019, S020, S023, S027, S028; re-run 2026-10-19 |
| `knowledge/adjacency-recheck-2026-10-19.md` | ADJ-01..07 source re-check: 1/8 original pins match the 2026-10-19T22:57:14Z committed-head snapshot, 8/8 cited anchors still hold; one committed mori recipient response is recorded without inferring acceptance/resolution | sibling `PROVINCE.md` HEAD bytes; kaika committed receipt sweep and the appended recheck in this entry |

## Quality bar

See `QUALITY.md` (admits only falsifiable, source-cited claims;
rejection kept as evidence of taste).

## Frontier

- Recipient-side replay, acknowledgement/acceptance and closure of the memory
  observation packet are unverified; author-side advisory seats are not outside
  promotion or admit/reject spot-checks.
- Shipped-artifact RE ownership is contested between kaidoku and revenger.
  Route an actual internals question to the protocol integrator before analysis.
- This entry does not backfill the historical index or re-certify older numeric
  captures. Re-read sibling declarations before another handoff.

- Pending `mkinitcpio` 42 upgrade strands two `/new_root` hooks (`initramfs-v42-sysroot-recovery.md`):
  watch upstream `btrfs-overlayfs` / `plymouth` hooks on-release; omarchy issue leads in `SOURCES.md`.
- The `errno:13` mechanism stays [inf] until the operator runs the falsifier in
  `snapper-eacces-mechanism.md`; a census arm for root-dir mode (`-Qkk` cannot see `/`) is carried debt.
- Where to learn more: `SOURCES.md` (registry, three study paths, search log, unopened leads).

## Erratum (2026-10-19, fleet round 1) — superseded claim in the journal-boot row

The `knowledge/journal-boot-plane.md` row above still reads "failed-service history **0 unit
failures in 13 retained boots**". That claim was refuted in round 4: `LOG.md:167` records 4
capitalized-pattern failure records found by the r4 sweep (r4-refuted). The row text stays as
written (append-only); this erratum supersedes it. Retention has also moved: 9 retained boots —
`journalctl --list-boots --no-pager | tail -n +2 | wc -l` 2026-10-19
(`../.ufo/evidence/round-1-kaika/scout-live.md`).

## Round 12 — depth refinement and root metadata

| Note | Holds | Sources |
|---|---|---|
| `knowledge/root-dac-decision-r12.md` and `.json` | Separate ordinary-mkdir indicator families for DAC/search, target mount/namespace, bounded credentials and target existence; explicit residual/unknown class and historical-attribution limits | SOURCES S027/S028/S034/S035/S038–S040; `lessons/round-12.md` Gate |

This deepens the existing rollback-net surface; it is not uncovered coverage
or a resolved host repair. The earlier Frontier root-mode debt is superseded
by the packages-plane metadata arm in `tools/tsukuroi-census.sh`.
The old `test -w` falsifier is superseded by the round-12 erratum in
`knowledge/snapper-eacces-mechanism.md`: a permission proxy is not proof of
subvolume causality. The opened systemd `root.conf` rule sets `/` to `0555`;
unowned does not mean policy-free. Exact historical failing syscall/path,
runtime credentials and incident-time target state remain frontier. Opened
issue leads S036/S037 are retained rejections, not causes or upgrade clearance.

## Round 13 — correction superseding the round-12 unit-path procedure

| Note | Holds | Sources |
|---|---|---|
| `knowledge/root-dac-correction-r13.md` and `.json` | Active correction R13-DAC-EXCLUSIVITY: ProtectSystem-only comparison, alternative bind/tmpfs read-only mechanisms, unmeasured private-path view, fixture-identity and bot-authority limits; supersedes the rejected round-12 B2 claims, not the historical failure evidence | S028/S041; source attribution superseding S042/S043; `lessons/round-13.md` |

This repairs knowledge on the existing rollback-net surface, not a new
coverage surface or a repaired host. The root-metadata capability and
boot-hook upgrade blocker are unchanged. Use the new correction before
consulting the preserved round-12 MD/JSON.

## Round 14 — source-scope corrections superseding two round-13 loci

`knowledge/source-scope-correction-r14.md` and `.json` carry
**R14-VALUE-DOMAIN** and **R14-COMMENT-ATTRIBUTION**. They supersede only the
round-13 ProtectSystem “value set is not exhaustive” cell (the documented
option domain is boolean or `full`/`strict`; mechanism non-exhaustiveness is
separate, S044) and the #8047 comment's “self-described model-generated
automated triage” wording (verified account fields are not a generation
claim; the VM assertion is unverified; the maintainer deferral concerns #6634
and #8047 waits on the reporter; #6629's disclaimer is not transferred, S045).
The round-13 row's “bot-authority limits” phrase now routes to this explicit
comment-scoped limit: account identity is not generation method or maintainer
acceptance. The remaining round-13 technical teaching, fixture-identity limits
and historical S042 row stay active; no new coverage surface or host repair is
claimed.

## Round 15 — portable locators and the dated update-safety recheck

`knowledge/source-locator-clarification-r15.md` and `.json` carry
**R15-LOCATOR** and **R15-POSITIVE-DOMAIN**. They withdraw only the
renderer-unqualified `rendered lines 1266-1267` supplemental locator (r14 MD
source-object, JSON `corrections[0].location` and `sources[0].anchor`) in
favour of the stable SANDBOXING > ProtectSystem= heading plus the observed
footer version, and replace the unswept “documents no further values” sentence
with the quoted positive definition. The r14 11-word quote, technical teaching
and #8047 correction stay exact; appended notices are in
`knowledge/source-scope-correction-r14.md` § R15 supersession and its
`r15_supersession` JSON key. QUALITY criteria 21–22 govern future locators and
absence claims.

`knowledge/partial-upgrade-recheck-r15.md` and `.json` (schema
`tsukuroi-partial-upgrade-recheck-v1`) replace the 2026-10-14 `INERT` /
“Do nothing now” current-use reading in `update-safety-note.md`,
`update-safety-v2.md`, `update-safety-v3.md` and `host-health-report-r3.md`;
those historical bytes stay. The dated 2026-10-20 recheck binds
`.ufo/waves/round-15/build/host-snapshot.json` and decides
`BLOCKED_FOR_AGENT_PACKAGE_ACTION`: the pending partial-upgrade assessment is
operator-only, no agent package or service action is authorized, and
mkinitcpio-42 `/new_root` hook compatibility remains an untested risk with no
clearance. No host repair is claimed.

The C1 checker `tools/check-locator-clarification.py` is a gate (0/1/2,
`--selftest`); `tools/measure-update-recheck.py` is a read-only counting probe,
not a verdict gate — its exit 0 is not “clean”. Registry rows are in
`../SKILL.md` § Round 15.

## Round 16 — citation-only section/table repair

`knowledge/section-citation-errata-r16.md` and `.json` carry two named
corrections, R16-BOARD-SECTION and R16-RANK-SECTION, sourced by S050.
Host-health's R15 notice points to `## 0. Verdict board` row5, not §1;
update-safety-v3's R15 notice points to its `## 5. Risk-ordered operations
table (recommendation only — nothing here was run)` rank1, not §7.
The original notices and tables remain, with appended citation-only errata.
Legitimate explicit references to v2's §7 are unchanged.

This strengthens held update-safety documentation, not the coverage map
or Frontier. A citation verdict resolves committed locations only, never
refreshes the 2026-10-14 captures or retained round15 snapshot, and is not
the update-safety/health gate. R15 current-use supersession and operator
recovery ownership remain. No agent package or service action is authorized.
Gate registry: `../SKILL.md` § Round 16; lesson and actual outcomes:
`lessons/round-16.md`, `.ufo/waves/round-16/`.

## Round 17 — boot chain after the mkinitcpio 42.2 upgrade

`knowledge/boot-chain-r17.md` and `.json` give a next-boot verdict for every limine entry
from extracted UKI initramfs images (typed `new_root` entries, init root references, hook
paths, hashes) bound to the firmware loader variables of the current boot. The Frontier
bullet above (“Pending `mkinitcpio` 42 upgrade strands two `/new_root` hooks”) is
superseded for this host: the upgrade ran on 2026-10-20 and 42.x keeps `/new_root` as a
symlink to `/sysroot`, so both hooks resolve (namespace emulation; not boot-tested).
Watch item that remains: upstream may drop the compatibility symlink; recheck
`tools/boot-chain-audit.sh --live` on every mkinitcpio release. Six older entries carry
appended `R17-FRESHNESS` notices (`knowledge/freshness-recheck-r17.json`, 48 records);
five carry `R17-RECHECK — steer-safe procedure` blocks. Lesson: `lessons/round-17.md`.


## Round18 — correction closure and current-use continuation

Held surfaces, not new coverage: `knowledge/boot-chain-r17.md` now carries four named R18 corrections (12-package argv, both-UKI init/hook citations, live UKI mtime); S051 remains image evidence, S058 tagged-source scope, S064 precise loader-variable/header evidence. `tools/check-boot-chain.py --statement-corrections` checks the fixed four propositions; generic notice conformance is not semantic proof.

`knowledge/freshness-recheck-r18.json` records49 primary notices in the eight routed files plus39 neighboring current-use restatements (88 records across17 paths). Original dated snapshots remain intact. Runtime earlyoom/zswap and package-directory observations are S060, not historical OOM attribution; Snapper config presence does not certify rollback; pending updates remain unknown. All new findings remain detection-and-report; package/service/boot actions stay operator-owned.

One shared `../tools/_revision.py` replaces the nine copied consumer binders; independent judge checks original-nine consistency, shared static call census and zero local literal copies, reporting additional discovered tools separately. The latest `../SKILL.md` registry supersedes old counts and the non-normative r16 JSON-oracle description. Historical Frontier bullets about pending42, root metadata and source ownership remain superseded by their explicit later entries, not silently rewritten. No frontier ground moves into core and no SHONEN promotion is claimed.


## Round18 final candidate scope — supersedes intermediate counts

The build88 and later93 record counts are intermediate same-round snapshots, not final measurements. Final candidate `knowledge/freshness-recheck-r18.json` has97 records across17paths:49 primary plus48 supplementary neighboring current-use notices. Current pending/foreign/explicit/repository/cache/snapshot questions are bounded unknowns where the captures do not answer them. S065 is retrospective ALPM event/completion evidence, not a package-manager execution; source registry59→65 adds six scopedA/mined rows. Final immutable command results, source digests and actual verdicts reside under `.ufo/waves/round-18/measure/final/` after L1 verification. No uncovered ground, new capability or operator action is credited by these counts.

The latest complete SKILL registry is operative; all earlier registry rows are explicitly historical/non-operative. Final C1 uses fixed correction metadata via --registry-from; C2 distinguishes consistency from consolidation; C3 is notice/source conformance for declared loci, never a host-wide truth certificate.


## Round19 — adjacency anchors and /boot writers

C1 (adjacency anchors) extends the coverage-map row `knowledge/adjacency-recheck-2026-10-19.md`. That row already holds the ADJ-01..07 source re-check: 1/8 original pins match the 2026-10-19T22:57:14Z committed-head snapshot, and 8/8 cited anchors still hold. The 8 are sibling lanes. The re-read names ten ranges (kama; kagi twice; mado; mori twice; kumitate; kaidoku; revenger; tameshi). Outbound portable anchors — exact heading, exact ≤25-word quote, pinned sibling commit, blob sha256 — deepen the line-range ownership pointers in `PROVINCE.md` (QUALITY 21). Those ten pointer tokens are the seven ADJ ownership cells, with ADJ-05 and ADJ-06 split, plus the Core mori cite. Inbound classification of sibling pointers into this lane is the direction that row does not hold. It answers the existing Frontier requirement to re-read drifted sibling declarations before another handoff. It does not extend `knowledge/adjacency-handoffs-fleet-r1.md`: no new ADJ id, no recipient acceptance or resolution, no replay. This is deepening of held adjacency ground (quality trend). It is not uncovered ground and it adds no coverage-map row.

C2 (/boot writers) extends the coverage-map row `knowledge/initramfs-v42-sysroot-recovery.md` through `knowledge/boot-chain-r17.md`. Round 17 left boot-chain off this map when it superseded that row's mkinitcpio-42 Frontier bullet, and rounds 17 and 18 both kept expansion unchanged. One `Updated: /boot/limine.conf` write is already attributed there to limine-snapper-sync during snapper-cleanup (S056). The round-18 operator note says the hourly rewrite is expected automation and a `/boot` write source boot-chain audits should expect. Binding each limine.conf update in the round-19 captures to a named writer class, mechanism line and signature deepens that held boot surface (quality trend). It is not uncovered ground. The journal-boot row names `limine-snapper-sync` and does not absorb it; that refusal stands. The snapper errno:13 row is unchanged. The `PM: Image not found` writer stays a separate unknown. An empty corpus hit for `ExecStopPost` and `limine-snapper-override` means those mechanism lines are not yet prose here; missing strings are not a new coverage-map surface. No host repair, package action or `/boot` write is claimed.

Measured counts for both are recorded in `SCORECARD.md` Round 19 and `.ufo/waves/round-19/measure/`; C2 counts 13 events, not the 12 first declared (2026-10-11 pacman.log 2021 was missed by the declaration).

## Round20 — attributed ownership and actual operative contracts

`knowledge/contract-corrections-r20.md` deepens held adjacency/boot/tooling ground, not new coverage. S077 explains object-prefix enumeration versus commit-ish peeling; S078 preserves the exact attributed Revenger declaration without awarding contested ownership; S079 grounds the audit's actual live0/2 map. S080 keeps the no-write inference rejected. PROVINCE's named R20-OUT009 clarification and boot-writers' named R20-RULE4 supersession control the stronger historical wording.

SKILL's new highest round20 registry separates live audit0/2 from selftest1; the false round19 operative-repair assertion and non-append-only historical-cell exception are expressly disclosed. Finite object-selector and execution-log controls do not imply arbitrary-shell enforcement or global registry-semantic proof. Measurements, source census and final wave accounting belong to the retained round20 ledger/scorecard/report, never an unrun-check assumption.

Frontier boundaries remain: Kaidoku/Revenger ownership arbitration is unresolved; no handoff receipt becomes acceptance/resolution. Public hook-body inspection does not bind boot-image contents or certify next boot; historical RED/UNKNOWN and package-recovery ownership remain unchanged. No package/service/kernel/initramfs/bootloader/mount/reboot action or capability acquisition is authorized.

## Round21 — target-type decisions and review identity

`knowledge/selector-contract-r21.md` and `.json` deepen the existing revision-bound evidence-tooling surface with five source-grounded decisions: commit/tree/blob/tag-to-commit/tag-to-noncommit (S081/S082). `tools/check-selector-contract.py` counts the finite declared contract; `tools/check-revision-binding.py --object-target-types` separately exercises actual original-nine consumer CLIs. The old round20 `--object-selectors` case set/count is preserved, and missing matrix availability is not a claim that unchanged binder behavior was wrong.

`tools/check-review-snapshots.py` binds declared primary snapshot SHA-256 and exact predicate to preregistered review receipts. It neither proves reading nor command nonexecution. Every missing or malformed report remains disclosed; known provider deaths are not replaced. Round20's13 missing build reports,20 malformed trailers and retroactive build reservation stay historical process defects, not newly cleared passes. Lessons/QUALITY42–44 capture prevention and required failing controls.

This is held-ground quality/depth, not uncovered coverage or a frontier graduation. Kaidoku/Revenger arbitration, recipient acceptance/resolution and host package/service/boot authority remain external and unchanged. Actual measurements are in SCORECARD Round21 and the committed round21 measurement ledger; no pending result is preclaimed.

### R21-TYPE-PROVENANCE — active corrected entry

`knowledge/selector-contract-r21-corrected.md` and `.json` now supersede the original r21 representation: exact located typed-recursion/failure/commit-ish quotations and separate per-row Git source/QUALITY27/36 policy fields. The original entry/data and all frozen review snapshots remain historical. The checker binds the corrected visible five-column table; a source-contract count is not a universal semantic certificate.

The new five-class consumer mode uses a non-tip landed commit for positive tags, exact refusal diagnostics, actual tag-target headers and finite prefix/ref-shadow/mutation controls. Original round20 matrix and shared binder are unchanged. C3 preserves primary receipt binding and explicit dead-seat reds; actual recorded tool use overrides a literal none declaration. Falsify's disclosed Bash deviations remain scope/calibration debt, not approved verification or erased evidence. Final measurements, integrity comparisons, report settlement and tool-call metadata are recorded separately in the round21 ledger.

## Round22 — bounded seat-scope evidence on held ground

`knowledge/seat-boundary-r22.md` and `.json` deepen held source/evidence-operability ground with six explicit source-only decisions (S083/S084). `../tools/check-seat-bindings.py` judges recorded request spellings against predispatch prompt declarations; `../tools/check-review-cohort.py` measures the fixed receipt cohort without waiving strict faults. The decision gate, request audit and receipt accounting have independent content inputs; common revision-binding infrastructure does not make their predicates interchangeable.

This is prompt policy plus post-hoc detection, not native runtime prevention: task tools adds extras and exposes no restrictive per-seat allowlist. Complete trace metadata means the available recorded terminal trace was parsed, not proof of universal recorder completeness or operation effects. Receipt `delivered_conformant` means receipt-well-formed only; actual out-of-scope calls still override false none assertions. All historical receipt faults, execution/fetch debt and provider failures remain visible. No native-tool ownership, host recovery action, new coverage-map ground, frontier graduation, repertoire row or outside promotion is claimed. The highest round22 SKILL registry is operative; measurements belong to SCORECARD and the committed round22 ledger.

## Non-author round23 verification

`lessons/round-23-verifier-spotcheck.md` records Main's independent claim judgment:
C1 document depth and C3 fixed-cohort calibration improve within their bounds;
original C2 all-round assurance remains unprovable, so the round is not admitted.
Original grammar, red/incomplete evidence and historical expectations are preserved.
This operator verification record adds no capability or native restriction; accounting
closure remains a separate required step.



## Frontier notice — round 24 (2026-10-22)

Append-only; the bullets above stay as written. The `Pending mkinitcpio 42 upgrade` bullet is superseded: mkinitcpio 42.2-1 is installed, every 42.2 image links `new_root` to `sysroot`, and boot 0 shows plymouth reaching the real root. The open frontier item is narrower: the btrfs-overlayfs snapshot-boot path on a 42.2 image is untested. The `sync dbs born 2026-10-11, -Sy never run since` line is also historical: the host follows the omarchy stable snapshot, which advanced on 2026-10-22 04:40 UTC. Evidence and sources S087-S103: `knowledge/pause-lift-gate-r24.md` and `.json` (counting command `python3 tools/check-pause-gate.py --revision <commit>`).

| Note | Holds | Sources |
|---|---|---|
| `knowledge/pause-lift-gate-r24.md` and `.json` | Dated verdicts for the five premises of the host-wide pacman pause: pending set against the current mirror snapshot, partial-upgrade residue, `/new_root` hooks under mkinitcpio 42, database freshness and upgrade target, rollback paths and transactions during the pause | S087-S103; `lessons/round-24.md` Gate |

### Round-24 notice erratum after falsification

This is stronger evidence on an existing Core surface, not new coverage or a frontier promotion. The open boot work includes both the untested snapshot path and the round-17 watch for upstream removal of the `/new_root` compatibility symlink (lines 152-153). Round 17 had already superseded the pending-upgrade phrasing at lines 149-151. Boot 0 supporting Plymouth reaching the real root is an inference, not a directly logged initramfs result. The old “`-Sy` never run since” line is falsified by the logged bare sync at round-24 `l1-4/capture.txt:221`, not by mirror promotion. The old installed/package figures at the start of this index are dated historical captures; current package-state observations are in `knowledge/pause-lift-gate-r24.md`, including its wave-2 corrections.

## Round 26 — storage integrity (frontier area of the OS substrate)

Append-only; the coverage map and Frontier bullets above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/storage-health-r26.md` and `.json` | New ground: six sourced rows on btrfs integrity and NVMe health. SH1 the five per-device error counters and their two views; SH2 the counters are a stored lifetime total, only error-level kernel lines date an error; SH3 scrub repairs only from a replica, so `single` data errors are uncorrectable and NOCOW file data is not verified; SH4 no scrub record exists on this host (`UNVERIFIED`); SH5 smartctl's PASSED is the Critical Warning byte alone; SH6 NVMe lifetime counters, including Unexpected Power Losses (labelled Unsafe Shutdowns), are not dated events | S128 to S135, S139; `lessons/round-26.md` Gate; capture `.ufo/waves/round-26/capture/capture.txt` |

### Frontier (round-26 addition)

- Storage integrity is a frontier area, not Core: it becomes Core only after a read-only census arm reads it (shape proposed in `.ufo/waves/round-26/w1/ScoutHostSurfaces.md`). Disk-space runway stays with mori; scrub runs, counter resets, profile changes and firmware updates stay operator-owned.
- The unopened lead at `SOURCES.md` line 214 (btrfs scrub documentation and btrfs-progs release notes) is now opened and mined as S129 and S139 for btrfs-progs v7.1.

### Round-26 correction after wave 2 (appended 2026-10-22)

The Frontier bullet above overstates the lead it closes: of the unopened lead in `SOURCES.md` (`## Leads (unopened)`, the firmware and Btrfs bullet, line 226 at `7dfea924` after the round-26 rows were inserted, not line 214), only the btrfs scrub documentation was opened (S129, S139). The btrfs-progs 7.x release notes and the ArchWiki Fwupd page were not opened (wave-2 CritTrendVerdicts, CritLearningClaim).

## Round 27 — kernel taint (deeper entry inside the driver and firmware area)

| Note | Holds | Sources |
|---|---|---|
| `knowledge/kernel-taint-r27.md` and `.json` | What this host's taint number 12288 means (O and E only), how the kernel sets O and E at module load, why a DKMS-signed module still sets E in permissive mode, the per-module taint file, that taint is never cleared while the kernel runs, and what it means for upstream bug reports; six rows KT1 to KT6 with operator actions | S140-S145; `lessons/round-27.md` Gate |

This is deeper ground inside the existing driver and firmware Core area (`PROVINCE.md` Core), not a new frontier area: `knowledge/driver-firmware-plane.md` already recorded the two taint lines on 2026-10-13 without their mechanism (wave-1 CritLearningFrontier and CritClaimSizing).

## Round 36 — child-environment hygiene for the five live tools; journalctl v262 field/filter rejection (2026-10-24)

Append-only. C1 (operability): the five live tools the round-35 spot-check routed build every child
environment from a fixed dict, counted by the frozen probe `tools/probe-child-env-allowlist-r36.py`
VERSION 7 (`--set livefive`; measure `leaking` 0, sensitivity battery committed under
`.ufo/waves/round-36/l1/`). C2 (depth, exploratory): `knowledge/journalctl-v262-field-filter-r36.md`
— the v262 rejection of `journalctl -F`/`-N` combined with limiting options (16-term predicate,
`-n` third state, scope selectors allowed), sourced on S198/S199. Sources: S198 journalctl(1) at
262; S199 systemd NEWS pinned at tag v262 (supersedes S024 for the note, S024 unchanged).
| Note | Holds | Sources |
|---|---|---|
| `knowledge/journalctl-v262-field-filter-r36.md` | The v262 scope-rejection of `journalctl -F`/`-N`: exact line, exit 1/EINVAL, the 16-term `field_list_has_scope_options()` predicate term-by-term, the `-n` allowed-silent third state, scope selectors that remain allowed, the safe substitution pattern, preventive consumer guidance (no lane tool uses `-F`/`-N`) | S198, S199; `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json` |

## Round 37 — errno discrimination on existing snapshot and journal ground

| Note | Holds | Sources |
|---|---|---|
| `knowledge/mount-errno-contract-r37.md` | Operation-specific mount and Btrfs snapshot errno classes on the existing snapshot-boot frontier; source behavior is not used to infer the cause of a historical host log | S200, S201; `lessons/round-37.md` Gate |
| `knowledge/errno-contract-variance-r37.md` | errno significance vs call return, portability of numeric mappings, host-specific EACCES=13 binding, and the boundary that an old empty retained-journal window does not prove repair | S202-S207; `lessons/round-37.md` Gate |

These entries deepen the existing errno/snapshot frontier (`corpus/README.md:38-42,151-153`); they add no new coverage surface or host repair. The generic errno-name entry in the staged package was rejected in the round Gate for overlap and absent explicit QUALITY check; it remains unadopted.

## Round 37 correction to the round-36 journalctl note

The round-36 row above is historical for the initial note. `knowledge/journalctl-v262-field-filter-r36.md` now carries an append-only round-37 correction: the source predicate has 15 terms (not 16), `-n` truncates saved `-F` output but left saved `-N` output unchanged, and `--list-boots` replaces field-list action rather than yielding field values. The prior S024/round-1 teaching is acknowledged; S199 remains the pinned source row. Counter: `tools/check-journalctl-v262-corrections.py --revision <REV>`; it checks the correction block only, not live journalctl behavior.

## Round 38 — storage arm in the census; effective ALPM hook order (2026-10-26)

Append-only; the coverage map and Frontier bullets above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `../tools/tsukuroi-census.sh` (`probe_storage_arm`, round-38 C1) | The verdict-neutral storage-integrity arm: one `STORAGE btrfs-device-stats state=… filesystems=N devices=N nonzero=N [detail=…]` line from the five counters of every `<fsid>/devinfo/<devid>/error_stats` under `/sys/fs/btrfs`; BLOCKED when a reading is impossible, DEGRADED on a nonzero stored total, HEALTHY otherwise; never in the rollup | S128, S133; `knowledge/storage-health-r26.md` SH1/SH2; `../SKILL.md` "Storage integrity arm — round 38" |
| `knowledge/pacman-hook-order-r38.md` | The host's effective ALPM hook order at pacman 54d9411 (69 effective hooks from 70 files; 17 Pre, 52 Post; one override; 0 masks; 0 `AbortOnFail`) and rules HO1–HO7 (suffix-ignoring order, last-directory-first override, triggerless masks, `AbortOnFail`, Pre-scan failure blocks the transaction, Post only after a completed commit, candidates vs triggered subset), with the round-38 correction block | S208–S212; `lessons/round-38.md` Gate |

### Frontier notice — round 38

The round-26 condition ("becomes Core only after a read-only census arm reads it") is met for the btrfs
per-device error counters only; the scrub record and NVMe SMART stay Frontier (`../PROVINCE.md`
"Round-38 promotion — R38-STORAGE-CORE"). Measured with `../tools/score-storage-arm-r38.py` and the
production-path conjunct `../tools/score-storage-arm-r38-q82.py` at the revision named in `../SCORECARD.md`
"Round 38 — measured outcome". The round-19 override reading (`knowledge/boot-writers-r19.md:37`, [inf]) is now
source-backed by HO2. Known limit carried to the frontier: an absent `/sys/fs/btrfs` reads `HEALTHY 0/0/0`, so a
namespace that hides it gives a false all-clear.

## Round 39 — transaction order; hidden storage root

Append-only (drafted by wave seat C2ScribeReadme, integrated by the L1); the coverage map and Frontier bullets above stay as written. The C2 entry deepens the held
update-safety plane (`../PROVINCE.md` Core) and is not new coverage; the C1 change is an operability repair
inside the round-38 storage arm above, not a new coverage surface.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/pacman-transaction-order-r39.md` | The libalpm transaction order TO1–TO8 at pacman `54d9411` (installed `7.1.0.r9.g54d9411-3`), deepening the update-safety plane whose within-phase hook order is `knowledge/pacman-hook-order-r38.md` (HO1–HO7): Pre hooks before `transaction started`, Post after `transaction completed` (TO1); sync removals before adds (TO2); per package `pre_install`/`pre_upgrade` → files and database entry → `installed`/`upgraded` line → `post_install`/`post_upgrade` (TO3); new version first, old second in scriptlet arguments (TO4); hook directories re-read per phase, so a hook first installed in a transaction is no Pre candidate (TO5); `ldconfig` once, skipped on an interrupted commit (TO6); removal order `pre_remove` → files → `removed` → `post_remove`, with neither scriptlet nor `removed` line for an upgrade's old half (TO7); every chroot child's output line tagged `ALPM-SCRIPTLET`, which is not "install scriptlet" (TO8). Frozen capture: 86 `[PACMAN] Running` windows, 60 started transactions, 28 `removed` lines, 252 of 441 `ALPM-SCRIPTLET` lines outside commit phases, 17 Pre hook files owned by packages first installed in a transaction (consistency, not proof), 0 of 60 transactions mixing removals and adds; S217 supersedes the round-38 S210 anchor | S208, S213–S218; `.ufo/waves/round-39/frozen/txcapture/` (MANIFEST pinned in the note's `source:` line); `../SCORECARD.md` "Round 39 — declaration" |

### Frontier notice — round 39

The round-38 notice above (`corpus/README.md:300-301`) carried one known limit — "an absent `/sys/fs/btrfs` reads `HEALTHY 0/0/0`, so a namespace that hides it gives a false all-clear" — and C1 closes it for a btrfs mount that the process's mount table lists: since `../tools/tsukuroi-census.sh` `probe_storage_arm` at commit `49cc53c7`, a sysfs root that is absent or holds no fsid entry reads `HEALTHY 0/0/0` only when the mount table (`/proc/self/mounts`, override `TSUKUROI_PROC_MOUNTS`) lists no btrfs mount; with one listed the STORAGE line is `state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs`, and an unreadable table is `state=BLOCKED … detail=mounts:unreadable` (`../PROVINCE.md` "Round-39 limit closure — R38-ABSENT-ROOT"). Core now additionally holds that one read of the mount table, read for this guard only and not a new owned surface, and the line stays verdict-neutral; `../tools/score-storage-hidden-r39.py` counts it under the frozen predicate — hidden 2/2, three views built on tmpfs inside `unshare -rm` from stdin (closing R38-Q82-LEAK), fixtures 5/5, live 1, six planes 1 — with the author receipt `.ufo/waves/round-39/after/c1-after-49cc53c.jsonl` PASS. **Still Frontier, unchanged:** the scrub record and NVMe SMART (`../PROVINCE.md:234-235`). **Remaining limit:** the namespace-sensitive behaviour cannot be told apart on this host, whose live answer is constant `HEALTHY 1/1/0`, and no host-side injection is authorized; the round-38 v1 counter's fixture F06 encodes the superseded rule and fails 9/10 at post-C1 revisions by construction (`../SCORECARD.md:2232-2234`).

The Sources pointer for the new row also includes `lessons/round-39.md` Gate (rows S213–S218) and the round-39 wave-1 correction block appended to the entry (TO5 discriminating instance, TO3 verbs, TO8 stderr).

## Round 40 — the libalpm execution environment for hooks and scriptlets (2026-10-26)

Append-only (drafted by wave seat C2ScribeReadme, integrated by the L1); the coverage map and Frontier bullets above
stay as written. The C2 entry deepens the held update-safety plane (`../PROVINCE.md` Core) and is not new coverage: it
states what a hook command or an install scriptlet finds when it starts, where `knowledge/pacman-hook-order-r38.md`
states which hooks run in what order within a phase and `knowledge/pacman-transaction-order-r39.md` states where the
phases and scriptlets sit in a transaction and how their output is logged.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/pacman-exec-environment-r40.md` | The environment a hook command or an install scriptlet finds when it starts, at pacman `54d9411` as built by Arch `7.1.0.r9.g54d9411-3`, deepening the update-safety plane whose within-phase hook order is `knowledge/pacman-hook-order-r38.md` (HO1–HO7) and whose transaction position is `knowledge/pacman-transaction-order-r39.md` (TO1–TO8): working directory `/` (EX1); stdout and stderr merged on one socket with stdin a second socket the parent closes at once, so a command without a `NeedsTargets` input callback reads end-of-file (EX2); `SHLVL` set to 1 only when unset, `BASH_ENV` removed, umask 0022, every other inherited variable passed through (EX3); scriptlets run as `/usr/bin/bash -c '. <scriptlet>; <function> <new version> [<old version>]'`, the upstream build default being `/bin/sh` (EX4); the scriptlet staged at `<root>/tmp/alpm_XXXXXX/.INSTALL` and removed afterwards (EX5); `NeedsTargets` stdin sorted, de-duplicated across triggers, one target per line (EX6); the `running` line logged before `Depends` is checked, an unmet `Depends` skipping the command and aborting only a PreTransaction hook carrying `AbortOnFail` (EX7); `Path` triggers matching file-list names, skipping `NoExtract` and ignoring `NoUpgrade`, so a `.pacnew` outcome still matches (EX8). Host values: 14 of 69 effective hook files carry `NeedsTargets`, the same count round 38 measured (a cross-capture agreement, not proof), and the installed `libalpm.so.16.0.1` holds `/usr/bin/bash` at strings index 1277 and no `/bin/sh` (consistency with EX4, not execution evidence). The four residual mechanism propositions round 39 deferred (`corpus/lessons/round-39.md:56`) are answered here — four re-grounded, plus one derived inference rejected (`corpus/lessons/round-40.md` Gate) | S219–S225; `.ufo/waves/round-40/frozen/src/` (SHA256SUMS, FETCH.txt) and `.ufo/waves/round-40/frozen/hostcap/` (MANIFEST sha256 `57888c10…`); `../SCORECARD.md` "Round 40 — declaration"; counter `../tools/check-exec-environment-r40.py` (sha256 `d4a2bb94…`), author receipt `.ufo/waves/round-40/after/c2-after-bf23805.jsonl` PASS (`rules_verified 8`, `counts_ok 2`, `novelty_base_hits 0`) at `bf23805` |

### Frontier notice — round 40

Round 40 promotes nothing. The entry is held update-safety Core depth, and no Frontier area moves: the round-26
condition for a Frontier area to become Core needs a read-only census arm (`corpus/README.md:243`), which this round
does not add, and the storage items are unchanged — the scrub record and NVMe SMART stay Frontier
(`../PROVINCE.md:234-236`) and the namespace-sensitive STORAGE reading keeps its limit (`corpus/README.md:315`).

Three limits the entry names itself stay open (`knowledge/pacman-exec-environment-r40.md:38-45`). First, the environment
that reaches pacman itself — sudo's `env_reset`, a systemd unit — is unread, so EX3 bounds the pass-through at pacman's
own process. Second, EX1–EX3 and EX5 have no host instance: observing them needs a running transaction, and the fleet's
pacman pause stands (`knowledge/pause-lift-gate-r24.md:7-12`, which authorizes no lane to run a transaction), so those
four rows rest on the pinned source alone. Third, the two Arch packaging patches that touch libalpm (`PKGBUILD:54-55`) are
named for review with their file scope not established. One further unobservable branch is not stated in the entry: EX7's
abort path has no instance here, because 0 of the 17 Pre hooks carry `AbortOnFail` as round 38 measured
(`knowledge/pacman-hook-order-r38.md:24`) and the round-40 capture re-measures only the `NeedsTargets` column
(`.ufo/waves/round-40/frozen/hostcap/hooks-needstargets.tsv:1`). A transaction-time observation of EX1–EX3, EX5 or that
branch is therefore operator-owned, not a lane action. The boundary with the lane's own tooling is the round-36
child-environment probe, which covers five lane tools and not ALPM's chroot children (`corpus/README.md:258-266`).

The Sources pointer for the new row also includes `lessons/round-40.md` Gate (rows S219–S225 and the assimilation
re-grounding of the four deferred propositions).

The Sources pointer also covers S226 (alpm-hooks.5 CAVEATS, added by the wave corrections appended to the entry) and the S208/S209 used-by additions logged in `lessons/round-40.md` Gate.

## Round 41 — ALPM package anatomy; four mount-table cases in the census selftest (2026-10-26)

Append-only (drafted by wave seat C2ScribeReadme, integrated by the L1); the coverage map and Frontier bullets above
stay as written. The C2 entry deepens the held pacman-state plane (`../PROVINCE.md:8-9`, "`.pkg.tar.zst` receipt
discipline") on its package-file side and is not new coverage: it states what a package archive carries, what libalpm
requires of it on load and what install keeps in the local database, where `knowledge/pacman-transaction-order-r39.md`
(TO1–TO8) states where a package's scriptlets and files sit in a transaction, `knowledge/pacman-exec-environment-r40.md`
states the environment they run in, and `knowledge/pacman-backup-files-r35.md` states how `backup` files become
`.pacnew`/`.pacsave`. The C1 change adds four mount-table cases to the census `--selftest` (`run_selftest`;
`probe_storage_arm` untouched, commit `568c397d`, +27 lines in one hunk), a test-surface repair inside the round-38
storage arm above, not a new coverage surface.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/alpm-package-anatomy-r41.md` | The package-file side of the pacman-state plane at pacman `54d9411` as built by Arch `7.1.0.r9.g54d9411-3`, with alpm-package(7) from `extra/alpm-docs 0.13.0-1`, deepening the plane whose transaction position is `knowledge/pacman-transaction-order-r39.md` (TO1–TO8), whose exec environment is `knowledge/pacman-exec-environment-r40.md` and whose `backup` handling is `knowledge/pacman-backup-files-r35.md`: the format's required root members `.BUILDINFO` `.MTREE` `.PKGINFO` plus optional `.INSTALL` (PA1); libalpm requires only `.PKGINFO` on load — a file with no `.PKGINFO` root entry fails with "missing package metadata", an empty name or version is refused, a version without a dash is refused, `.MTREE` is read only on a full load and `.BUILDINFO` is passed over like every other unhandled dot file (PA2); makepkg lists with `LC_COLLATE=C` and bash `dotglob`, so the dot files sort ahead of the data files and the metadata sits at the beginning of the archive (PA3), while the partial load's stop is the loader's — the first non-dot entry after `.PKGINFO` (`be_package.c`, S228); install keeps `.INSTALL`/`.CHANGELOG`/`.MTREE` as `install`/`changelog`/`mtree` (mode 0644) in the local database entry and skips every other root dot file, `.PKGINFO` and `.BUILDINFO` included (PA4); `.MTREE` is a gzip mtree listing that excludes itself (PA5); `pacman -Qkk` runs `check_pkg_full` on the kept mtree, and a missing or unopenable mtree returns 0 with the "no mtree file" notice (silent under `--quiet`), so the package adds zero errors (PA6); PKGBUILD(5)'s Packaging Functions section gives the working directory of the five functions it names — `package()`/`prepare()`/`build()`/`check()` in `$srcdir`, `verify()` in `$startdir`, `package()` under fakeroot — and none for the split `package_<name>()` or `pkgver()` (PA7, packaging-side); vercmp order — epoch (absent = 0), then version, then release only when both carry one, so any epoch 1 build outranks every epoch 0 build and `1.0` equals `1.0-5` (PA8); the host column reads this host's local database (1409 entries: mtree 1409 of 1409, install 51 of 1409, changelog 0, dot files 0, mtree gzip 1409 of 1409, self-listed 0), its `vercmp` and its `man PKGBUILD` | S227–S236 in `../SOURCES.md` (nine pinned upstream documents — alpm-package(7), `be_package.c`, `makepkg.sh.in`, `add.c`, `check.c`, `PKGBUILD.5.asciidoc`, `version.c`, `be_local.c`, `query.c` — plus the own-work capture `.ufo/waves/round-41/frozen/hostcap/`, `MANIFEST.sha256`); `lessons/round-41.md` Gate (rows S227–S236 and the assimilation re-grounding that meets round 38's flip); counter `../tools/check-package-anatomy-r41.py` (frozen at `e479fdc5`, sha256 `c83e29a4…`); `../SCORECARD.md` "Round 41 — declaration" |

### Frontier notice — round 41

Round 41 promotes nothing, and the C2 entry is Core depth rather than new ground. The pacman-state plane was Core before
this round — `../PROVINCE.md:8-9` owns "pacman state (`pacman -Qkk` verify loops, foreign/AUR census, `.pkg.tar.zst`
receipt discipline)" — and the row above states the package-file side of that ownership, beside the plane's older anchor
`knowledge/package-state-plane.md` (`corpus/README.md:7`). What is new is the statement, not the surface: the lane held
how a transaction orders a package's scriptlets and files, the environment they run in and how `backup` files drift
(`knowledge/alpm-package-anatomy-r41.md:7-13`), and no statement of the archive itself, so PA1–PA8 are the first statement
of it on an already-owned surface. Seven of the eight rows are host-state depth — a package file as a receipt (PA1–PA3,
PA5), the local database (PA4), the `-Qkk` loop (PA6) and the version comparison (PA8); PA7 states a build recipe, is
retained for the round-38 flip condition (`corpus/lessons/round-38.md:49`) and is not counted here as Core depth. No
Frontier area moves: the round-26 rule is that a Frontier area becomes Core only after a read-only census arm reads it
(`corpus/README.md:243`), and nothing here adds one — C1 edits `run_selftest` only and leaves `probe_storage_arm` as it
stood (`../SCORECARD.md` "Round 41 — declaration"), so the storage items are unchanged as well (the scrub record and NVMe
SMART stay Frontier, `../PROVINCE.md:234`; the namespace-sensitive STORAGE reading keeps its limit, `corpus/README.md:315`).

Three limits stay open. First, PA2 and PA3 are recorded host-unmeasured in the entry
(`knowledge/alpm-package-anatomy-r41.md:27-28`): the package cache is empty and the fleet's pacman pause stands
(`knowledge/pause-lift-gate-r24.md:11-12`, which authorizes no lane to run a transaction). Part of that moved anyway: the
wave's PA2 verdict seat measured the load path read-only on scratch package files with `pacman -Qp` — no cache and no
transaction — and found three conditions the row does not name, the loader's exact match on the `.PKGINFO` entry name
among them (`.ufo/waves/round-41/w1/C2RevPA2b.md`), so that cell records the author's method, not a limit of the
read-only lane; PA3's archive order stays unmeasured. Second, PA6's zero-error branch has no instance here — the kept
mtree is present for 1409 of 1409 entries (`knowledge/alpm-package-anatomy-r41.md:31`) — and the same check fires for a
package file queried with `-Qp`, where no kept mtree exists to check (`.ufo/waves/round-41/w1/C2RevPA6b.md`). Third, the
cache-shape anchor in the round-1 row above (`corpus/README.md:7`, "cache shape (8.6 G, never pruned)") is history, not
current state; it stays as written, and a package-file observation of PA2 or PA3 is operator-owned, not a lane action.
The round's per-row credit is the wave's read and not a promotion: a row counts only with a committed reviewer verdict
file (`QUALITY 81`, `knowledge/alpm-package-anatomy-r41.md:59`), and the round's non-author closure is pending
(`lessons/round-41.md:64`).

The Sources pointer for the new row also includes `lessons/round-41.md` Gate (rows S227–S236 and the assimilation
re-grounding of the staged `alpm-package-anatomy-r26.md` theme, which admits PA1, PA7 and PA8 re-grounded and keeps the
`package()`-in-`$pkgdir` sentence rejected).

## Round-42 coverage note (appended 2026-10-26)

| Entry | What it adds | Sources / evidence |
|---|---|---|
| `knowledge/btrfs-scrub-record-r42.md` | Storage-integrity frontier, scrub record: SC1 file name, `_tmp`-then-rename and `flock(LOCK_EX\|LOCK_NB)`; SC2 `scrub status:1` per-device `\|key:value` format; SC3 the start process writes it, recording disabled on mkdir or first-write failure, running state from `BTRFS_IOC_SCRUB_PROGRESS`; SC4 status fold (finished = every recorded device, canceled = any, `interrupted`, `no stats available`, `ENOENT` = no history); SC5 per-device `scrub_speed_max` (btrfs-progs 6.6.3) | S237, S238, S239; `lessons/round-42.md` Gate; capture `.ufo/waves/round-42/frozen/hostcap/capture.txt` |

Frontier: the scrub record stays Frontier (no census arm reads it); round 42 deepens it from source, it does not
enter new coverage-map ground (the scrub record has been a Frontier line since round 26). The btrfs-progs release-notes
half of the round-26 lead is now opened for the 6.6.3 scrub entries (S238); the ArchWiki Fwupd page stays unopened.

## Round-43 coverage note (appended 2026-10-26)

| Entry | What it adds | Sources / evidence |
|---|---|---|
| `knowledge/btrfs-scrub-record-r43.md` | Storage-integrity frontier, scrub record, re-grounded: SR1 the record write discipline (`_tmp` opened without `O_TRUNC`, renamed only after a successful write, never unlinked; the trailing-bytes consequence marked [inference]); SR3 what `btrfs scrub resume` writes (`scrub_resumed_stats`) and when recording failures are printed (`do_print`, `-B`); SR6 why an unprivileged `btrfs scrub status` never reads `running` (`BTRFS_IOC_SCRUB_PROGRESS` needs `CAP_SYS_ADMIN`) | S237 (btrfs-progs v7.1 `cmds/scrub.c`), S240 (Linux v7.2.11 `fs/btrfs/ioctl.c`), S241 (own-work capture); counter `tools/check-scrub-record-r43.py` |

The round-42 row above lists SC1-SC5 as that entry's holdings; SC1 and SC3 stand withdrawn and SC4/SC5 are narrowed
(its header line 4 and "Corrections — round-42 wave 2"); read the write-discipline, resume and running-state points
from the round-43 entry. Frontier: the scrub record stays Frontier (no census arm reads it); round 43 re-grounds it
from source and adds the kernel-side privilege fact (S240), it enters no new coverage-map ground.

## Round-44 coverage note (appended 2026-10-26)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-43 notes above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `../tools/tsukuroi-census.sh` (`probe_scrub_record`, round-44 C1) | The verdict-neutral scrub-record arm: one `SCRUB btrfs-scrub-record state=NONE\|RECORDED\|BLOCKED dir=absent\|present\|unreadable records=N tmp=N sockets=N unreadable=N orphan=N limited=N timers=N [detail=…]` line from names and stat only under `/var/lib/btrfs` (records, `_tmp`, sockets; unreadable and orphan counts), each fsid's `devinfo/<devid>/scrub_speed_max` (nonzero = limited, listed in `detail`) and the enabled `btrfs-scrub@<instance>.timer` links under `timers.target.wants`; BLOCKED when a reading is unavailable, RECORDED when record/tmp/socket names exist | contract `tools/tsukuroi-census.sh:384-412`; PROVINCE round-44 section |
| `knowledge/btrfs-scrub-record-r44.md` | SR7 the scrub-progress success direction (0 only while `dev->scrub_ctx` is attached; `-ENOTCONN` idle; `-ENODEV` unknown devid; device replace runs through the same `btrfs_scrub_dev`); SR8 `scrub_speed_max` (`BTRFS_ATTR_RW` 0644, `%llu` read, `memparse` write, 0 = no limit, in-memory only); SR9 the Arch-packaged `btrfs-scrub@.timer`/`.service` (monthly, `Persistent=true`, `btrfs scrub start -B %f`, `KillSignal=SIGINT` → the foreground `BTRFS_IOC_SCRUB_CANCEL`, a canceled record) | entry header and rows at the measured revision |

### Frontier notice — round 44

The round-26 condition at `corpus/README.md:243` is met for the unprivileged scrub-record view only: the census now
reads the record directory by name and stat, the per-device limit and the enabled timer instances, so that part of
the storage-integrity frontier moves Frontier → Core (`../PROVINCE.md` "Round-44 promotion — R44-SCRUB-VIEW"). The
record's content (SR1, a 0600 root-written file opened under `flock(LOCK_EX|LOCK_NB)`), the running state (SR6
`CAP_SYS_ADMIN`; SR7 0 only while a scrub context is attached, so a progress socket is a reading, not the running
state) and NVMe SMART/Health (SH5/SH6) stay Frontier; running, canceling, resuming or limiting a scrub, enabling its
timer, resetting the error counters, profile changes, firmware, LUKS and any repair stay operator-owned. Measured
with `../tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR>` at the revision named in `../SCORECARD.md`
"Round 44 — measured outcome"; the depth entry is counted by `tools/check-scrub-record-r44.py --revision <REV>`
(predicate rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3
and novelty_base_hits == 0 and pointer_ok == 1), its three row verdicts binding only from the round-44 wave-2
reviewer and critic seats. Known limit: an absent sysfs root with no record reads `limited=0` (the `STORAGE`
mount-table guard flags a hidden sysfs), a record's readability is counted and its content never read, and the arm's
namespace legs leave the mount-table, `uid_map` and script-path channels open. Host at the measured revision:
`NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`, consistent with S245.

## Round-45 coverage note (appended 2026-10-27)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-44 notes above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/btrfs-scrub-grounding-r45.md` | Grounds the three round-44 `[inference]` marks: GR1 the `scrub_speed_max` write parse (`memparse`: one letter of `K M G T P E`, 1024 per step, base-0 radix, bare newline = 0 = no limit); GR2 the device replace's two `btrfs_scrub_dev(..., false, true)` call sites, the `EINPROGRESS` a scrub start for a present, writeable non-target device gets while a replace is started or suspended (after the `-ENODEV`/`-EROFS`/`-EIO` device checks), and the unprivileged sysfs view of a replace; GR3 systemd v262's stop sequence for the packaged service (SIGINT from `KillSignal=`, SIGCONT, SIGKILL if a process remains after `TimeoutStopUSec=5s`), with the `canceled` write inside that window left undecided | S246-S249; `.ufo/waves/round-45/frozen/src/SHA256SUMS` and `hostcap/capture.txt` (sha256 `f5958a83…`); `tools/check-scrub-grounding-r45.py --revision <REV>` |

Frontier: nothing moves. The round-44 promotion (the unprivileged record-directory view is Core) stands; the record's
content, the running state and NVMe SMART/Health stay Frontier, and running, canceling, resuming or limiting a scrub
stay operator-owned (`:443-444`). The three row verdicts bind only from the counted reviewer and critic seats of wave
a2w1 and, for a `partly`, the residual of wave a2r1 (`SCORECARD.md` "Round 45 — attempt-2 rebinding"). Round 45 bound none of them: the depth gate FAILED (`verdicts_ok` 0)
and GR1-GR3 are pending, not admitted (entry section "Gate status — round 45").

## Round-46 coverage note (appended 2026-10-27)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-45 notes above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/census-identity-r46.md` | The census `--identity` line (round-46 C1, routed debt D12): one `TSUKUROI_CENSUS_IDENTITY:` line naming sha256, md5, bytes and newline count of the bytes bash executes, read through the unique close-on-exec script descriptor of 10 or more that resolves to the invoked path; `unverifiable` for stdin, pipes, a path relinked after open, an ambiguous or inherited descriptor; the `git log` loop that maps the sha256 to commits | S250 (GNU bash 5.3 `shell.c`, `general.c`, `general.h`), S251 (`proc_pid_fd(5)`) |

Round-44 status (routed defect D1): the row above for `knowledge/btrfs-scrub-record-r44.md` (`:434`) and the
"Frontier notice — round 44" paragraph (`:440-452`) present SR7-SR9 without their gate result. Round 44's depth gate
FAILED (`tools/check-scrub-record-r44.py --revision fbfef071`: `verdicts_ok 0`,
`corpus/lessons/round-44-verifier-spotcheck.md:84,133`); SR7, SR8 and SR9 are pending, not admitted. Frontier: nothing
moves this round; the census identity is a property of the gate, not a new host surface.

## Round-49 coverage note

`knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3 are admitted round 49 on the wave `w1` cohort's 18 bound seat verdicts, all `holds`, at least three credited per row on the frozen row hashes, and not on outside review or any host observation. The rows were unadmitted in rounds 45-48 and stay pending for the round-48 GR2 defect.
