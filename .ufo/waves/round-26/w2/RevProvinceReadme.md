# RevProvinceReadme: review of the round-26 PROVINCE paragraph and corpus/README.md section

Verdict: partly holds. The cited mori line is accurate and mori claims no btrfs integrity or NVMe health, but "free-capacity reporting remains mori's" overreaches against tsukuroi's own surfaces, the privilege and NVMe-device scope is unstated, the README row reshapes some entry details, and the frontier-to-core condition is not concrete.

Reviewed bytes: measured revision 7dfea9244a84a0e2439f0698e54491e5d7b7c467, extracted with git archive to /fast/scratch/hyaku/tsuku26/w2/RevProvinceReadme/rev. Lane HEAD is 7f9f08894fce41146f76fa5c3f3282037211555a, one commit later. That commit does not touch PROVINCE.md, corpus/README.md or the storage entry (git diff --stat over those four paths printed nothing, exit 0), so the reviewed text is still current.

## Findings

### 1. High. The frontier-to-core condition is not concrete

- Evidence: PROVINCE.md:169-170 says "This area becomes Core only after a census arm exists". corpus/README.md:243 says it "becomes Core only after a read-only census arm reads it". Both are at the measured revision.
- Missing from both: a named arm, script or plane; a selftest case count and exit code; a mapping from verdicts to census states; a privilege policy (finding 3); a scope (finding 4); an admission step; and a statement of which gate governs after promotion.
- The census has three states, "HEALTHY | DEGRADED | BLOCKED — three states" (SKILL.md:27). The entry has four, adding UNVERIFIED (storage-health-r26.json lines 19-24). The wave-1 proposal maps UNVERIFIED to DEGRADED with an unverified(...) field (.ufo/waves/round-26/w1/ScoutHostSurfaces.md:173-175). The committed text does not record that choice.
- The lane's own admission rule is absent. The SCORECARD round-26 measured outcome row for C1 says the result is "subject to the falsify wave and the non-author closure". PROVINCE.md does not name that step.
- The gate named at PROVINCE.md:171-173 counts entry rows (verified_rows). It does not measure a census arm, so after promotion it is unclear what it would count.
- The only shape on record is a proposal: "proposal only; nothing implemented" (ScoutHostSurfaces.md:160).
- The two documents also disagree. PROVINCE says a census arm "exists"; the README says one "reads it".
- [inf] A scaffold arm would satisfy the condition as written. A concrete condition would name the plane and script at a revision, the selftest count and exit 0, the verdict mapping, the privilege handling, the device scope, a non-author admission record, and the gate that applies after promotion.

### 2. High. "Free-capacity reporting remains mori's" is contradicted by tsukuroi's own surfaces

- Evidence in tsukuroi: SKILL.md:125 is a Headroom step that runs df -h / /boot. SKILL.md:155 and :206 list df among the permitted read-only commands.
- corpus/knowledge/update-safety-note.md:176-177 reads "Space is not the gate" and reports /boot at 1.8 G available with CheckSpace on. Line 351 records a space check with result PASS.
- corpus/knowledge/snapper-eacces-mechanism.md:15 reports /boot at 2.0G total, 279M used and 1.8G available, and compares the ESP size with a 4 GiB recommendation.
- Evidence in mori: mori's own declared runway is narrower. mori PROVINCE.md:10 and :26, and SKILL.md:19, name df -P on the fleet root and /tmp only. None of the three text sources claims /, /boot or /fast.
- Quoted at PROVINCE.md:165-166: "disk-space runway and free-capacity reporting remain mori's". The sentence is broader than the mori text it cites.
- [inf] The fleet root (/home, /dev/mapper/root[/@home]) and / (/dev/mapper/root[/@]) are subvolumes of one btrfs filesystem (findmnt; /proc/mounts lines 7 and 24). Mori's df on the fleet root and tsukuroi's df on / therefore read the same pool, and two lanes report it.
- Suggested wording: mori owns the runway rows for the fleet root and /tmp. Tsukuroi keeps the -Syu space gate and the headroom reading for / and /boot. /fast is named as unowned by default.

### 3. High. Privilege is not stated for the new probes

- Evidence: the frozen capture script runs sudo -n for btrfs device stats, btrfs scrub status, ls on /var/lib/btrfs, journalctl, smartctl and nvme smart-log (.ufo/waves/round-26/capture/capture.sh:28, :30, :31, :39, :41, :45-46, :48, :50).
- Without sudo the NVMe facts fail. smartctl -H -A /dev/nvme0n1 prints "Permission denied" and exits 2. nvme smart-log exits 1. The superblock read is also denied (ScoutHostSurfaces.md:101-113, findings 6 and 7).
- The arm proposal says the arm must never call sudo (ScoutHostSurfaces.md:202-203). It also says that without a privileged companion capture the plane reads DEGRADED on every run on this host (ScoutHostSurfaces.md:231-235).
- PROVINCE.md:8 describes the Core surfaces as "all read-only probes". PROVINCE.md:164 says "the same boundary that governs the Core surfaces above applies here". Neither says that the storage probes need privilege, so a reader would assume unprivileged reads.
- Consequence: the census cannot reach HEALTHY from its own reads, which decides whether "census arm exists" gives a usable plane.

### 4. Medium. The NVMe scope is unstated, and one NVMe controller has no health reader

- Evidence: the host has two NVMe controllers. /proc/mounts line 26 mounts /boot from /dev/nvme0n1p1. Line 27 mounts /tmp from /dev/nvme1n1p1 (xfs). Line 28 mounts /fast from /dev/nvme1n1p2 (xfs).
- The capture reads only /dev/nvme0n1 and /dev/nvme0 (capture.sh:48 and :50).
- PROVINCE.md:162-163 says "the NVMe SMART/Health lifetime fields". corpus/README.md:239 says "NVMe health". Entry line 45 says "one NVMe SSD under LUKS". None of them names the device.
- The wave-1 scout saw the second controller and warned that its health must not be attributed to the root filesystem (ScoutHostSurfaces.md:131-143). That warning did not reach the committed text.
- [inf] /fast/scratch/hyaku, the scratch tree named for this review's writes, sits on nvme1n1p2. Neither the tsukuroi capture nor the mori PROVINCE reads that controller's health. Mori claims write averages, not health, and tsukuroi's Core driver plane names no storage device.
- Within the root controller, the SH6 row does not carry Data Units Written (capture.txt:190, 47,275,631 [24.2 TB]). Percentage Used (capture.txt:188, 2%) appears only as an action in SH5. "Lifetime fields" in PROVINCE.md:163 reads wider than the six rows.

### 5. Medium. Mori's /tmp premise is stale, and its disk row may now measure an NVMe partition

- Evidence: systemctl show tmp.mount (exit 0) reports What=/dev/nvme1n1p1, Type=xfs, FragmentPath=/run/systemd/generator/tmp.mount and ActiveEnterTimestamp=Thu 2026-10-22 04:55:42 -03.
- Mori's most recent live receipt in its tree, mori-shokunin/.ufo/waves/round-13/evidence/live-measurement.json line 15 (ts 2026-10-20T04:33:08Z), reads io_avg_unavailable=tmpfs:not-a-block-device.
- Mori's own corpus says /tmp is tmpfs: corpus/README.md:161-162 ("the second default target /tmp is tmpfs on this host") and corpus/knowledge/surfaces-r7.md:157 ("/tmp is tmpfs here").
- [inf] Mori's device lookup (tools/mori-census.sh:1872-1876 resolves /dev/* sources) would now find nvme1n1p1 in /proc/diskstats (present at read time, line 5). Its /tmp row would then report a write average on an NVMe partition, not a reason string. I did not run mori's census to confirm this.
- [unk] Whether mori has recorded a live row since 04:55 -03 on 2026-10-22.
- This does not change ownership. It means mori's premise is out of date, and the tsukuroi paragraph does not mention the change.

### 6. Medium. /boot and /fast have no named owner or handoff path

- Mori's default runway targets are the fleet root and /tmp (mori PROVINCE.md:26). /boot (vfat, the 2G ESP) and /fast (xfs) are not targets.
- The tsukuroi Adjacent table has no capacity row. The ADJ-04 row covers "Host pressure or a kill signal" only. A tsukuroi-observed capacity finding has no named route.
- Suggested fix: add a capacity handoff row, or state that capacity findings stay with tsukuroi where the lane already owns the space gate.

### 7. Low. "The scrub record the filesystem keeps" is inaccurate

- PROVINCE.md:161 says the lane reads "the scrub record the filesystem keeps".
- The entry says btrfs-progs keeps the status files in /var/lib/btrfs (entry line 57: "/var/lib/btrfs, where btrfs-progs keeps scrub.status.<UUID> files, does not exist"). The capture lists that directory with sudo (capture.sh:31). The scout found it absent (ScoutHostSurfaces.md:47-66).
- So the census path would be a userspace directory. The paragraph does not name it.

### 8. Low. Four different lists of operator-owned actions

- PROVINCE.md:167-168: "filesystem repair, running a scrub, resetting an error counter and firmware updates".
- corpus/README.md:243: "scrub runs, counter resets, profile changes and firmware updates".
- Entry line 9: "filesystem repair, scrub runs, counter resets or firmware updates".
- Entry JSON line 26: "Scrub runs, counter resets, timer enablement, profile changes and firmware updates".
- One canonical list should replace the four.

### 9. Low. The README row mostly matches the entry, with four differences

- Matches: six rows (entry lines 13-95). The source list "S128 to S135, S139" equals entry line 1, the lesson's admitted rows (corpus/lessons/round-26.md:9) and SOURCES rows at corpus/SOURCES.md:134-145. The capture path and its sha256 002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd match entry line 1 and JSON line 11; I recomputed the hash (sha256sum, exit 0). The "lessons/round-26.md Gate" pointer resolves (lesson line 5).
- Difference 1: README:239 says "scrub repairs only from a replica". Entry line 43 adds that the dup metadata copies sit on one device and an SSD may store them as one physical copy. The README drops that caveat.
- Difference 2: README:239 says "NVMe health" with no device scope (finding 4).
- Difference 3: entry lines 99-106 ("How this changes OS triage" and "Adjacent") make claims that are not rows and that the gate does not count. One is a journal-boot claim from a wave-1 scout file. The other is a sibling-ownership claim from a wave-1 connector file. The README does not repeat them. The sibling claim holds for mori (finding 11).
- Difference 4: the README calls the entry "six sourced rows". That is accurate for the rows, but the reader cannot tell which entry claims the gate counts.

### 10. Low. Frontier placement and pointer form

- The paragraph is a standalone section (PROVINCE.md:154) with no frontier ID, outside the "## Frontier" section. The README puts its bullets under "### Frontier (round-26 addition)" (README:241). The two frontier lists are not one list.
- "../mori-shokunin/PROVINCE.md:26" is a bare line pointer. PROVINCE.md:112-113 says round-19 ownership text is cited "never by line number". The pointer resolves today, because mori's working tree equals its HEAD (cmp exit 0) and line 26 is the resource-runway bullet. It is not portable.

### 11. Low. Device write averages are mori's, and the storage paragraph does not say so

- Mori's since-boot average counts every write to dm-0, the btrfs device under the fleet root (mori corpus/knowledge/surfaces-r7.md:153-154, and mori PROVINCE.md:26).
- It measures write volume, not wear or health. One sentence in the paragraph would stop a reader from taking a write average as an NVMe health reading.

### 12. Low. The proposed arm's inputs include chunk-level figures

- The input row for "btrfs filesystem df --raw /" reads "total=N, used=N" (ScoutHostSurfaces.md:191). Mori's rule says "Never threshold the btrfs chunk percent" (mori SKILL.md:415-418).
- A Core condition should say the arm reads profile identity only.

## Checked and found accurate or consistent

- Mori does not claim btrfs integrity, scrub, error counters, SMART or NVMe health. I searched mori PROVINCE.md, SKILL.md, tools/, corpus/README.md, corpus/knowledge, corpus/lessons and corpus/SOURCES.md. The btrfs hits concern capacity accounting (SKILL.md:415-418) and btrfs quota source rows (corpus/SOURCES.md:85-86, S079 and S080), which belong to the withdrawn round-23 quota work (PROVINCE.md:211-224). The NVMe hits are device names (corpus/knowledge/drift-repin-r20.md:48) and one lesson that reads sectors_written on nvme0n1 (corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md:102). The "scrub" hits are environment scrubbing (tools/mori-census.sh:568).
- The mori citation at PROVINCE.md:26 is accurate (finding 10 records its bare-line form).
- The entry's claim that no sibling owns btrfs integrity or NVMe health holds for mori.

## Residual risk and verification gaps

- I did not run tools/check-storage-health.py or the census. This review checks wording and boundaries, not counts.
- The /tmp change and the write averages are observed at single points in time: tmp.mount at 2026-10-22 04:55 -03, and the live reads at about 13:44 to 13:52 UTC. Later state may differ.
- [unk] Whether df on / and df on /home return identical figures for the shared btrfs pool. I inferred that from the mount table, not from a df comparison.
- I did not search all of mori's .ufo/ wave evidence, which is too large for a complete search. Its hits were limited to disk and diskstats records.
- I read the lane's quality rules only through targeted searches. A stricter promotion rule may exist elsewhere in the lane.

Tools used for the review: read-only git (archive, show, log, diff --stat, rev-parse), cmp, findmnt, lsblk, systemctl show, sha256sum, wc, and file reads and searches. Installs: none.

Scope: read=tsukuroi PROVINCE.md, corpus/README.md, corpus/knowledge/storage-health-r26.md and .json, corpus/knowledge/update-safety-note.md, corpus/knowledge/snapper-eacces-mechanism.md, SKILL.md, corpus/SOURCES.md rows S128-S139, corpus/lessons/round-26.md, the round-26 capture and capture.sh, and w1/ScoutHostSurfaces.md, all at 7dfea9244a84a0e2439f0698e54491e5d7b7c467 via a git archive extract; mori-shokunin PROVINCE.md, SKILL.md, tools/mori-census.sh, corpus README, knowledge, lessons, SOURCES.md and .ufo/waves/round-13/evidence/live-measurement.json; /proc/mounts, /proc/diskstats, lsblk, findmnt and systemd tmp.mount; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RevProvinceReadme.md, /fast/scratch/hyaku/tsuku26/w2/RevProvinceReadme/rev/ (sandbox extract only); executed=git -C tsukuroi archive 7dfea92 | tar -x (exit 0); git -C mori show HEAD:PROVINCE.md | cmp (exit 0); git -C mori log -3 -- PROVINCE.md; git -C tsukuroi rev-parse HEAD and log 7dfea92..HEAD; git -C tsukuroi diff --stat 7dfea92 HEAD -- four paths (empty, exit 0); findmnt -T and -no on five paths; lsblk; systemctl show tmp.mount -p What -p Type -p Where -p ActiveEnterTimestamp -p FragmentPath (exit 0); sha256sum on capture.txt and capture.sh (exit 0); wc -l on capture.sh; file reads and searches
Model: anthropic/claude-haiku-5-5 (workstation context value; no per-seat identity field was exposed)
Installs: none
