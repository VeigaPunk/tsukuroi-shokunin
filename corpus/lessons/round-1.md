# Steered fleet round-1 — handoff evidence, not table credit

Date: 2026-10-15. This is the current fleet round-1 after the historical lane-r11/training-r10 closeout, not a rewrite of training round-1. Source evidence: `../knowledge/adjacency-handoffs-fleet-r1.md` §1–§5, its JSON ledger, and the fleet report `.ufo/reports/round-1/tsukuroi.md` once committed after the lane work. The report is the delivery receipt, not a prerequisite claimed to exist here.

## Gate

- Candidate admitted: the seven source-cited **analysis-recipient** contracts and the sanitized observation packet `TSUKUROI-F1-MEM-01`. Sources, byte fingerprints, exact capture window/commands/exits, retained OS scope and unknowns are persisted in the knowledge note/ledger. This establishes a bounded handoff contract; only the memory-to-mori case was exercised as an observation/request.
- Candidate rejected: treating GPU availability as proof of endpoint readiness or served-model identity. R1DriverPacket obtained a successful `nvidia-smi` query, but no endpoint symptom, serving-unit observation or endpoint evidence. The note §3 boundary control records the negative result, not an invented incident.
- Candidate rejected: treating the memory seat's "background-noise" wording as a measured health threshold. It supplied no applicable threshold or baseline. The admitted packet keeps exact gauges and PSI readings and explicitly does not prove either harmful pressure or a fresh OOM. Root `memory.events` absence is not zero.
- Candidate rejected: crediting the inherited `PROVINCE.md`/`SKILL.md` table edits as this session's authorship, multiplying one packet by its copies/probes/lifecycle states, or upgrading an author-side acknowledgement to recipient acceptance. The note §1 records inherited-byte hashes; §3/§4 keeps one stable packet identity and separate lifecycle states.
- Spot-check: **no independent non-author admit/reject spot-check obtained**. R1Reviewer/R1Critic and all other dispatched seats are author-side advisory evidence, not an outside learning or promotion verifier. Their bounded source/claim findings are incorporated; no `[x]` credit follows.

## Understanding and limits

Route the **question**, not the executable. OS diagnosis stays here; endpoint reconciliation, credential-flow reasoning, visible desktop behavior, fleet correlation, dispatch semantics and reusable test methodology belong to named analysis recipients. Overlapping RE declarations remain an integrator question. Sharing evidence grants neither ownership nor permission to remediate.

A record count is not an axis-score formula. The scorecard's limited 7→8 adjacency assessment requires the persisted contract and one verified packet actually cited in the committed fleet report; it claims no accepted route, recipient replay, wave causation or promotion. Other scores are intentionally unchanged, not freshly re-certified.

Trend verdicts for this move: **expansion improved** (new adjacency contract/evidence entry); **quality improved** (previous dangling named evidence target now has exact source/packet support); **discernment unchanged** (no outside admit/reject spot-check). These judgments apply only to this admitted material, not a retrospective clean bill for the historical corpus.

## Mistakes

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | Measurement-method errata: sync DB mtime→birth, journal lines→entries, unit-file count 136→133, rollback-net inference retracted | `SKILL.md:218-232` | QUALITY #2–3 | Already corrected in the appended method errata; retain command-level anchors. |
| M2 | Census md5-prefix transcription candidate (`7a3d3b94ed…` vs `…ec…`) | `LOG.md:68-71` | QUALITY #4 | Keep both values visible; never rewrite the recorded candidate. |
| M3 | Overbroad negative claim: 0 unit failures in 13 boots, later refuted by 4 records | `LOG.md:96` vs `LOG.md:167` (not `:176`); `corpus/knowledge/journal-boot-plane.md:424-426` | `SKILL.md:1440-1442` (partial: empty-proof, not a general sweep) | QUALITY #9 requires the negative-claim sweep. |
| M4 | Unresolvable “20-min cap” preserved as unknown rather than invented | `corpus/knowledge/executor-test-sufficiency.md:185-192`; `SKILL.md:543-547` | `SKILL.md:543-547` | Carried debt: define or retire U1; owner: integrator (`SKILL.md:710-713`). |
| M5 | Hardening gap reported honestly: tameshi's independent sweep closed 1/4 survivor classes | `LOG.md:168`; `SKILL.md:706-709` | `SKILL.md:706-709` | Carry the remaining survivor-closure debt with tameshi; preserve the two-pin rule. |
| M6 | Memory-arm admission awaited non-author verification, later closed by VER-S8 | `LOG.md:170-171` (not `:178-179`); `SKILL.md:1473-1476` | `SKILL.md:1473-1476` | Closure is the landed `corpus/knowledge/memory-arm-ver-s8.md`; keep non-author replay as the gate. |
| M7 | Plane-count and verification-credit restatements drifted across rounds | `LOG.md:172-173,226-231` | `SKILL.md:1443-1446` | Preserve the appended precision and move all live counts together. |
| M8 | Malformed SCORECARD tables persisted across rounds before repair | `corpus/knowledge/closeout-r11.md:249-254`; `LOG.md:220-225` | none | QUALITY #10 checks changed table column structure before a correction commit. |
| M9 | Round-10 6/10 mutation result was only attested in a code comment; independent replay remains owed | `SKILL.md:1498-1504` | `SKILL.md:1473-1476` | Carried debt: independent replay; owner: next non-author verifier, assigned by the integrator. |
| M10 | 18-vs-19 `-Qkk` summary split remains unresolved | `SKILL.md:233-235` | `SKILL.md:233-235` | Carried debt: root re-run, not hand reconciliation; owner: authorized operator (elevation-gated register row 1). |
| M11 | Commit `9b70381` landed eight files without its required `LOG.md` entry | `git -C <wt> show --stat --oneline 9b70381` (no `LOG.md`); `AGENTS.md:3` | none | QUALITY #11 requires the matching evidence-bearing LOG entry in the landing commit. |
| M12 | README retained a correction already made to the underlying journal note | `corpus/README.md:13`; `corpus/knowledge/journal-boot-plane.md:424-426` | none | QUALITY #10 requires sweeping every mention in README, SKILL, and knowledge before commit. |
| M13 | Contract-key drift: at base, 6 notes lacked `source:`, 11 lacked `verified-at:`/`recheck:`, and no `recheck:` used a date/cadence | `.ufo/evidence/round-1-kaika/before.md:85-111`; `SKILL.md:710-713` | none | Claim C appends the missing key blocks; QUALITY #8 makes the date-or-cadence contract explicit. |
| D1/MC1 | Operator advice contradicted Arch maintenance doctrine; bare `-Sy` appeared in nine advice hits | `.ufo/evidence/round-1-kaika/before.md:218-231`; `corpus/knowledge/closeout-r11.md:225-226` | none | QUALITY #6 requires S010-aligned pacman advice and forbids recommending bare `pacman -Sy`. |
| D2/MC2 | Hook-precedence unknown remained open although the local note had already recorded the collision | `corpus/knowledge/degraded-triage-r4.md:369-371,546-547` | none | QUALITY #8 requires a relevant log/journal sweep before retaining an unknown; Claim C erratum D2 records the resolved evidence. |
| D3/MC3 | EACCES was narrowed without measuring `/` DAC mode/owner/ACL alongside unit restrictions | `corpus/knowledge/degraded-triage-r4.md:315-325` | none | QUALITY #13 pairs DAC facts with `CapabilityBoundingSet` and `ProtectSystem`; retain the separate root-mode census debt. |
| D4/MC4 | Missing `checkupdates` was treated as an unreadable mechanism | `corpus/knowledge/update-safety-note.md:378-381` | none | QUALITY #12 requires reading upstream source or a man page before tagging the mechanism `[inference]`. |
| D5 | Effective HOOKS were attributed to `/etc/mkinitcpio.conf` instead of the drop-ins | `corpus/knowledge/journal-boot-plane.md:244-245`; `corpus/knowledge/degraded-triage-r4.md:358-371` | QUALITY #2 (partial: an anchor existed, but it was not the effective source) | Claim C erratum D5 corrects the effective-source citation; QUALITY #7 requires applicable anchors. |
| D6 | Package verification and the census cannot see `/` mode because the root directory is unowned | `corpus/knowledge/package-state-plane.md:146-175`; `.ufo/evidence/round-1-kaika/before.md:204-215` (baseline DAC sweep only) | none | Carried debt: add a future census arm; method question to tameshi via ADJ-07 (owner: tameshi); QUALITY #13 records the blind spot. |

### Pattern

The recurring root is a closure gap: method observations, unavailable probes, and draft citations could remain unverified or incorrectly carried into operator-facing claims (M1, M3, M11–M13; D1–D5).
Append-only discipline preserved superseded facts, but did not ensure every index mention was swept or make source freshness computable (M2, M12–M13).
Where an answer depended on host state or package ownership, the base tree retained the uncertainty or method scope but not the full underlying probe output (D2, D6); those remain an erratum and an owned future-arm debt, not a new in-repo measurement.
Pointer audit: the r4 correction is `LOG.md:167` (STATE's `:176` is not that correction), and the r8 memory-arm closure is `LOG.md:170-171` (STATE's `:178-179` is the r11 seat list); `pacman.log:1989-1990` is a host path absent from `<wt>`, so D2 cites its resolving local defect anchors instead.


## Gate — fleet round 1 continuation (kaika, 2026-10-19)

Round claims: A adjacency (ledger source-current + lifecycle states), B coverage + capability
`sources-registry`, C freshness (D1–D5 errata + appended contract keys). Evidence:
`../../.ufo/evidence/round-1-kaika/` (before.md, scout-live.md, reviewer-quotes.md,
critic-preland.md, connector-overlap.md, adjacency-pins.txt, sources-quotes.md, after.md).

- Admitted: `../knowledge/arch-news-gate-2026.md`, `../knowledge/pacnew-plane.md`,
  `../knowledge/initramfs-v42-sysroot-recovery.md`, `../knowledge/snapper-eacces-mechanism.md`
  (uncovered ground per the ART §1.2 sweeps, all 0 at base; connector sweep found no sibling
  claiming any of the four — `connector-overlap.md`), `../knowledge/adjacency-recheck-2026-10-19.md`,
  and `../SOURCES.md` (34 rows; contract census clean). Each entry opens with
  `source:`/`verified-at:`/`recheck:` and carries a `## QUALITY check` against criteria 1–13.
- Rejected (kept): S029 Arch Security Tracker (stale for installed versions); S030 W1
  synthesized answer (contradicted by S020); S033 this round's re-run synthesized answer
  (calls mode 555 a read-only mount, advises sudo overrides/restarts); reading R5 "mkinitcpio ≥42
  TPM2 news applies" (busybox `encrypt`, no TPM2 — `initramfs-v42-sysroot-recovery.md`
  § Rejected readings); reading R6 "pre-existing `@.snapshots` explains errno 13" (EACCES, not
  "already exists" — `snapper-eacces-mechanism.md` § Rejected readings); ART K3 "upstream delta
  via the archlinux.org JSON API" deferred, not admitted: network reads of a live service sit
  outside `PROVINCE.md`'s read-only host-probe boundary until the operator rules (L0 question in
  the round report).
- Legacy-addendum exception (stated, not hidden): the 25 base notes receive their
  `source:`/`verified-at:`/`recheck:` keys as an appended `## Contract keys` block at end of file,
  not as opening lines — `CORPUS.md` "opens with" is met only by the five new entries; rewriting
  the openings would break append-only. Appended `verified-at:` values are the notes' original
  measurement dates unless the block names a 2026-10-19 re-run.
- Spot-check: **no independent non-author admit/reject spot-check obtained in-round**; reviewer
  and critic seats are author-side. Non-author verification is owed by the orchestrator after
  landing (≥1 admit, ≥1 reject, ≥3 SOURCES rows re-opened, every counting command re-run).

### New SOURCES rows — URL, access date, quote with location (contract rule 1)

| id | source URL or own-work path | access date | quote location | quote (≤25 words) |
|---|---|---|---|---|
| S001 | https://archlinux.org/news/ | 2026-10-19 | Arch Linux News Archives; dated feed row | “2026-09-22 — Mkinitcpio >=42 requires manual intervention for TPM2-based unlocking of LUKS devices” |
| S002 | https://archlinux.org/news/mkinitcpio-42-requires-manual-intervention-for-tpm2-based-unlocking-of-luks-devices/ | 2026-10-19 | Article, PCR condition | “If you configured the systemd hook and unlock LUKS partitions, that depend on these values, you need to re-enroll the TPM2 in use.” |
| S003 | https://archlinux.org/news/active-aur-malicious-packages-incident/ | 2026-10-19 | Article, final advisory paragraph | “We continue to encourage all users of AUR packages to review all PKGBUILD and install script changes when updating, especially during this time.” |
| S004 | https://archlinux.org/news/recent-services-outages/ | 2026-10-19 | Workarounds during service disruption | “Please default to the mirrors listed in the pacman-mirrorlist package during an outage.” |
| S005 | https://archlinux.org/news/manual-intervention-for-pacman-700-and-local-repositories-required/ | 2026-10-19 | Article, pacman 7.0 local repository notice | “pacman has added support for downloading packages as a separate user with dropped privileges.” |
| S006 | https://gitlab.archlinux.org/pacman/pacman/-/raw/master/NEWS | 2026-10-19 | NEWS, 7.0.0 | “Download files to a temporary directory owned by DownloadUser” |
| S007 | https://man.archlinux.org/man/pacman.conf.5 | 2026-10-19 | OPTIONS > HookDir; Pacman 7.1.0 man-page footer | “Multiple directories can be specified with hooks in later directories taking precedence over hooks in earlier directories.” |
| S008 | https://man.archlinux.org/man/alpm-hooks.5 | 2026-10-19 | OVERRIDING HOOKS; Pacman 7.1.0 man-page footer | “Hooks may be overridden by placing a file with the same name in a higher priority hook directory.” |
| S009 | https://gitlab.archlinux.org/pacman/pacman-contrib/-/raw/master/src/checkupdates.sh.in | 2026-10-19 | SYNC branch; commit ea3ed064f0cc071f843e18741e74138b6421959e | `ln -s "${DBPath}/local" "$CHECKUPDATES_DB"` |
| S010 | https://wiki.archlinux.org/title/System_maintenance?oldid=885170 | 2026-10-19 | Avoid certain pacman commands; oldid 885170 | “never run pacman -Sy; instead, always use pacman -Syu.” |
| S011 | https://wiki.archlinux.org/title/Pacman/Pacnew_and_Pacsave?oldid=869214 | 2026-10-19 | Why these files are created; oldid 869214 | “These files require manual intervention from the user and it is good practice to handle them right after every package upgrade or removal.” |
| S012 | https://wiki.archlinux.org/title/Official_repositories_web_interface?oldid=867367 | 2026-10-19 | Package information > Details; oldid 867367 | “Syntax: /repository/architecture/package/json/” |
| S013 | https://wiki.archlinux.org/title/Arch_Linux_Archive?oldid=879665 | 2026-10-19 | Restore all packages to a specific date; oldid 879665 | “restore all your packages at a precise moment” |
| S014 | https://wiki.archlinux.org/title/Mkinitcpio?oldid=886405 | 2026-10-19 | Runtime customization; oldid 886405 | “launches an interactive shell which can be used for troubleshooting purposes” |
| S015 | https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/releases/v40 and https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/releases/v42 | 2026-10-19 | v42 release notes, Changes in mkinitcpio; tag commit 11e3db210891b2d89a8d01ef33baa684beca1dbe | “Busybox-based init now uses /sysroot as the root mountpoint just like the systemd-based one.” |
| S016 | https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42/init | 2026-10-19 | v42 `init`, root-mount code | `# Mount root at /sysroot` |
| S017 | https://wiki.archlinux.org/title/Unified_kernel_image?oldid=886457 | 2026-10-19 | Preparing a unified kernel image > mkinitcpio; oldid 886457 | “mkinitcpio will assemble the UKI itself unless systemd-ukify is installed.” |
| S018 | https://wiki.archlinux.org/title/Limine?oldid=887253 | 2026-10-19 | Snapper snapshot integration for Btrfs; oldid 887253 | “Providing 3 different methods for restoring a system snapshot: rsync, replace or native snapper.” |
| S019 | https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/README.md | 2026-10-19 | Description > What it does; README commit 4695dd1c2cf9c9b8bcf1c174a9c8593f666d7b66 | “The tool provides rsync, replace or snapper (opensuse) to restore a selected snapshot”; “After restoring, a ‘backup’ snapshot entry is added to Limine” |
| S020 | https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/install/arch-linux/usr/lib/systemd/system/limine-snapper-sync.service | 2026-10-19 | Security hardening block; commit cd909745ad4ee136aaf4adca6d018e72df81c740 | `CapabilityBoundingSet=CAP_SYS_ADMIN` |
| S021 | https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs | 2026-10-19 | `root_mnt` assignment and `findmnt` failure branch; commit 3c011dc2aebc0346f5e1d5dc2132a2a5f6c71169 | `root_mnt="/new_root"`; `|| return 0` |
| S022 | https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook | 2026-10-19 | `run_latehook`; commit df088501c9bf9b28b98ba58e7049ec8026edd8f8 | `plymouth update-root-fs --new-root-dir=/new_root` |
| S023 | https://wiki.archlinux.org/title/Snapper?oldid=870168 | 2026-10-19 | Creating a new configuration; oldid 870168 | “the @.snapshots subvolume will already be mounted to /.snapshots, and the snapper create-config command will fail” |
| S024 | https://raw.githubusercontent.com/systemd/systemd/main/NEWS | 2026-10-19 | CHANGES WITH 262; NEWS commit a923ab5ed1481512be6fb52aaa5086d0fef6878f | “journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters.” |
| S025 | https://man.archlinux.org/man/systemd-debug-generator.8 | 2026-10-19 | KERNEL COMMAND LINE > systemd.break=; systemd 262.1 man-page footer | “The option prefixed with ‘rd.’ is honored only in the initrd, while the one without prefix is only honored on the host.” |
| S026 | https://wiki.archlinux.org/title/General_troubleshooting?oldid=882746 | 2026-10-19 | Recovery shells and Fixing a broken system; oldid 882746 | “rescue launches a shell shortly after the root file system is remounted read/write”; `arch-chroot -S /mnt` |
| S027 | https://man.archlinux.org/man/capabilities.7 | 2026-10-19 | Capabilities list > CAP_DAC_OVERRIDE; Linux man-pages 6.19 | “Bypass file read, write, and execute permission checks.” |
| S028 | https://man.archlinux.org/man/systemd.exec.5 | 2026-10-19 | CapabilityBoundingSet=; systemd 262.1 man-page footer | “Controls which capabilities to include in the capability bounding set for the executed process.” |
| S029 | https://security.archlinux.org/ | 2026-10-19 | Issues table, AVG-2893 systemd row | `“257.6-1”; “Vulnerable”` |
| S030 | /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/fleet-ledger/.ufo/waves/kaika-w1/tsukuroi-art.md | 2026-10-19 | §6 R3, line 393; no equivalent web_search tool mounted | “Your service has `CapabilityBoundingSet=CAP_DAC_OVERRIDE`” |
| S031 | tools/tsukuroi-census.sh | 2026-10-19 | CLI help, lines 441-446 | “--selftest hermetic fixture-tree test of every verdict arm” |
| S032 | /var/log/pacman.log | 2026-10-19 | Line 1427, transaction at 2026-10-11T16:14:18-0300 | `[ALPM] warning: /etc/locale.gen installed as /etc/locale.gen.pacnew` |
| S034 | https://man.archlinux.org/man/access.2 | 2026-10-19 | DESCRIPTION, privileged-process paragraph (lines 47-50 of the text render) | "for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities" |
| S033 | own-work: L1 `web_search` re-run, recorded in `../SOURCES.md` § Search log | 2026-10-19 | synthesized answer, "Root Causes" item 2 | "A root directory mounted read-only (mode 555) will prevent subvolume creation." |

### Status/recheck/used-by changes in place

None to pre-existing rows — `SOURCES.md` is new this round (rows written once; S032's used-by
was corrected before first commit to drop a path that does not cite it; after the post-landing
review, also before first commit: S010/S031/S032 `used-by` completed with every citing note, S006/S024
anchors stripped of commit pins that did not reproduce, S019 anchor extended to § Requirements, S029
version wording corrected to the installed 261.2-1, S032 anchor extended to the cited lines, and S034
access(2) added because the snapper falsifier relied on it without a row).

- Append-only audit (post-landing reviewer): every modified tracked file keeps its base bytes as a prefix except `corpus/README.md` (five coverage rows inserted inside the index table — an index row is a claim written when its file exists; 0 deleted lines) and `corpus/knowledge/adjacency-handoffs-fleet-r1.json` (keys inserted; 0 deleted lines, `jq empty` passes).
- Integration mistake caught before commit (L1): the errata seat (re-dispatched after a provider
  capacity failure) self-corrected by appending — duplicate `## Contract keys` blocks in 7 notes, a
  `Source-ID clarification` erratum for its own `S032`/`S010` mislabel, and, in `aur-risk-plane.md`,
  a stray tool-output line plus `closeout-r11.md`'s key block (false provenance, flagged by the
  post-landing critic). Because none of it was committed, the L1 consolidated each note to one
  key block and corrected the label in place before the first commit; base bytes stay a prefix.
  Lesson: a seat's in-flight appends are drafts — audit `git diff` block structure before commit
  (QUALITY 10's sweep extended to the round's own additions).
