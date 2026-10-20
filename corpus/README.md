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
