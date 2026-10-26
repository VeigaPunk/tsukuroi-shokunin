VERDICT: draft

Seat AsmGate, round 43 w1, item F-7. Read-only evaluation of `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/` (MERGE-REPORT.md/.json, `knowledge/` 70 files, `SOURCES.append.md` 147 rows S200-S346). Receipts: `.ufo/waves/round-43/w1/AsmGate/` (`receipts.txt`, `quarantine-slice`, `reg-ids`, `staged-ids`, `collisions`, fetched `mkinitcpio.8.raw`, `scrub-intro.rst`, `journal.html`). Access date for every URL below: 2026-10-26. No campaign tool run; nothing written outside my report/receipts; scratch `/fast/scratch/hyaku/tsukuroi-r43/AsmGate` removed.

## Recommendation (one line)

**Adopt candidate: `knowledge/corpus/knowledge/initramfs-hook-api-r25.md`, conditional** on the five conditions in section 4. It matches the *boot-chain inputs* surface, not scrub or pipefail. **Reject: `ext4-journal-guarantee-r32.md`** (section 5). `Assimilation: none` applies only if the L1 will not carry the conditions; no staged entry is adoptable as staged (0 of 70 staged files carry a `## QUALITY check`, QUALITY 14).

## 1. Theme sweep (btrfs scrub / boot-chain inputs / pipefail)

- `grep -ciE "scrub|pipefail|newermt|boot-chain" MERGE-REPORT.json MERGE-REPORT.md` → 0 and 0.
- Over `knowledge/` + `SOURCES.append.md`: `pipefail`, `boot_inputs`, `newermt`, `boot-chain` → 0 hits. `scrub` → only `ext4-journal-guarantee-r32.md:6,37,48` and `SOURCES.append.md:76` (S269 teaches cell). No staged entry touches the scrub status-file write discipline, `scrub resume`, or `BTRFS_IOC_SCRUB_PROGRESS` (SR1/SR3/SR6). So nothing staged bears on C2's rows or C1's `find | grep -q` fail-open.
- Nearest staged match to "boot-chain inputs": `initramfs-hook-api-r25.md` (names the mkinitcpio input search paths). Nearest to "scrub": `ext4-journal-guarantee-r32.md`. Known-bad from round 42 and unchanged: `btrfs-ioctl-surface-r27.md:14,31-32` still says "close the btrfs ioctl surface" / "stable and enumerable — a caller can be identified from its ioctl number alone" (round-42 AsmGate P2/P3 rejection stands; scrub trio BTRFS_IOC_SCRUB/_PROGRESS/_CANCEL absent from its table).

## 2. Quarantine slice (derived)

Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (exists via `merge/tsukuroi/../../.ufo/…`), sha256 `5afe1810…d833`. Command: `awk -F'|' -v l='tsukuroi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'` → **12 rows** in `w1/AsmGate/quarantine-slice`; `cmp` equal to `.ufo/waves/round-41/assimilation/quarantine-slice`. Rows: S211, S213 (`payload-absent`); S225 ("could not be fetched"); S230, S231, S242, S243, S244, S249, S250, S251, S252 ("gate block named no locator"). **None of the 12 is S200 or S210, the two ids the adopt candidate cites** (its `source:` lines), and its rows are not in the slice; the candidate's cited sources are therefore not quarantined. (Slice ids are id-level facts from the register; I did not re-check whether the register's S-ids denote the staged or the lane's rows beyond the unchanged slice.)

## 3. Id collision check (reg-ids vs staged-ids)

Extractor `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]+' | sort`. Lane `git show 7d0ed1c2:corpus/SOURCES.md` → 241 ids (S001-S241); `SOURCES.append.md` (sha256 `7914d3b9…8406`) → 147 ids (S200-S346). `comm -12` → **42 collisions, S200-S241** (`w1/AsmGate/collisions`). Concretely for the candidate: staged S200 = mkinitcpio(8) but lane S200 = mount(2) (`corpus/SOURCES.md:209`); staged S210 = Arch news mkinitcpio hook migration but lane S210 = libalpm `trans.c` (`corpus/SOURCES.md:219`). Landing the entry or rows without renumbering silently re-points the entry's two citations at the wrong sources. Staged S269/S270 (ext4) do not collide with lane ids. Lane round-43 added S240/S241 since round 41's 37-id list, so any earlier-recorded collision list is stale (now 42).

## 4. Adopt candidate: `initramfs-hook-api-r25.md`

Staged text: five runtime hook points in order, `add_runscript` naming guarantee, install/runtime hook search paths, v38 hook-migration precedent.

**Source check (QUALITY 91: candidate, not evidence) against fetched bytes** `mkinitcpio.8.raw` sha256 `3f274415…d90f` (header "mkinitcpio 42.2", date 2026-10-01; `pacman -Q mkinitcpio` → 42.2-1 on host):
- Hook points and order: ABOUT RUNTIME HOOKS lists `run_earlyhook`, `run_hook`, `run_latehook`, `run_cleanuphook`, `run_emergencyhook` ("hooks are run in the order that they are defined in the HOOKS variable, except for cleanup hooks which are run in reverse"). Matches the staged text.
- `run_latehook`: "Functions of this name will be run after root has been mounted." `run_emergencyhook`: "run before the emergency shell launched in case of boot failure". Match.
- `add_runscript`: "The name of the script is guaranteed to match the name of the hook the script is called from." Matches.
- Paths (FILES): `/etc/initcpio/install`, `/usr/lib/initcpio/install` build hooks; `/etc/initcpio/hooks`, `/usr/lib/initcpio/hooks` runtime; also `/etc/initcpio/post`, `/usr/lib/initcpio/post` (post hooks) and `/etc/mkinitcpio.d` (presets) — the staged entry omits post and presets.
- v38 news (S210): "several hooks previously provided by Arch packages have been moved to the mkinitcpio upstream project. The hooks are: systemd, udev, encrypt, sd-encrypt, lvm2 and mdadm_udev" and "temporary conflicts have been introduced". Matches (page dated 2024-03-04).

**Novelty (QUALITY 68 sweep):** `grep -rnE "run_earlyhook|run_latehook|run_emergencyhook|run_cleanuphook|add_runscript" corpus SKILL.md PROVINCE.md README.md` → only `initramfs-v42-sysroot-recovery.md:14,52` (a `run_latehook` mention) and plymouth hook rows S022/S097/S111; no row lists the five hook points or cites mkinitcpio(8). `corpus/SOURCES.md:339` has only an unopened lead for mkinitcpio(8). The ground is new.

**PROVINCE scope:** in-province, Core: `PROVINCE.md:22` ("Initramfs v42 and boot recovery — Inspect effective mkinitcpio drop-ins, hooks and recovery stages; never rebuild or boot"). The entry is documentation knowledge only; it adds no action.

**QUALITY bar (criteria applied, status as staged):**
- 2/7/19/21: sources named with S-row, tier A, heading, version/date — ok except ids collide (section 3).
- 8: `verified-at` and `recheck: on-release` present — ok.
- 9: its negative "held no statement of the hook API" has no sweep command/date — fails as staged; section above supplies the sweep to cite.
- 14: no `## QUALITY check` section — fails; required before an admit.
- 21/32: `ground:` cites `corpus/README.md:38-42,151-153` as bare line ranges and the cited bullet is superseded by the README erratum ("the upgrade ran on 2026-10-20 and 42.x keeps `/new_root` as a symlink to `/sysroot`"), so a stale premise.
- 66: "The lane's own v42 two-hook stranding is the same shape" states the pre-upgrade premise; for this host (42.2-1 installed) it is superseded.

**Conditions to adopt (all required):** (1) renumber S200/S210 (and their `source:` lines, used-by) to free ids ≥ S242 (staged ids S242+ also exist, so allocate against the lane, not the package); (2) add a `## QUALITY check` evaluating 7, 8, 9, 14, 19, 21, 66, 68; (3) replace the README line-range `ground:` with quote-anchored pointers and rewrite the "stranding is the same shape" sentence to the post-upgrade state; (4) add the post-hook and `/etc/mkinitcpio.d` rows from FILES or scope the statement to "build and runtime hooks"; (5) re-quote against 42.2 at landing (recheck on-release).

**Side finding (not in C1's frozen claims; for the L1 to route):** the `boot_inputs_newer` start-point set (`tools/boot-chain-audit.sh:494-496`: `/etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d /etc/default/limine /etc/limine-snapper-sync.conf /usr/lib/initcpio /usr/lib/modules`) omits `/etc/initcpio/{install,hooks,post}` and `/etc/mkinitcpio.d`, which mkinitcpio(8) FILES lists as inputs. `grep -n "initcpio" tools/boot-chain-audit.sh` shows `/usr/lib/initcpio` only. On this host those dirs exist and are empty (`ls /etc/initcpio/*`). A user hook added there after boot would not flip the gate. Observed fact: the set excludes them; whether that is intended is **unresolved** (header comment at :58-59 lists the same eight without rationale). This is a coverage-of-inputs question, not the pipefail fail-open C1 fixes; it would be a new defect candidate, not a falsifier of C1.

## 5. Reject: `ext4-journal-guarantee-r32.md` (staged S269/S270, tier A)

Source-checked reasons:
1. **Out of this host's province.** `findmnt -rno TARGET,FSTYPE` → `/ btrfs`, `/home btrfs`, `/var/log btrfs`, `/boot vfat`, `/fast xfs`, `/tmp xfs`: no ext4. The entry itself says "this entry is a *mechanism* entry, not a description of the lane's own host." `PROVINCE.md:154-174` admits btrfs counters, the scrub record and NVMe health to this lane; ext4 appears nowhere in PROVINCE.md (`grep -n -iE "ext4|jbd" PROVINCE.md` → 0). Adopting it enlarges the corpus off-province.
2. **Its btrfs comparison row contradicts this host.** Table "repairs corruption? btrfs: yes, from a replica". `ch-scrub-intro.rst` v7.1 (fetched sha256 `c3b9d344…3485`, equals the S139 row digest) lines 13-15: "On filesystems that use replicated block group profiles (e.g. RAID1), read-write scrub will also automatically repair any damage by copying verified good data". The lane's own `storage-health-r26.md:11` records this host: data profile `single`, metadata/system `dup`, one device; and `:43`: "With the data profile `single` there is one copy, so a data checksum error is detected and reported as uncorrectable, not repaired". The staged "yes" is unscoped, and also "checksums on every block" ignores NOCOW (`ch-scrub-intro.rst` lines 20-23 "the actual file data is not [validated]"). QUALITY 17/66 (conditions kept) and 22. It would land on the Frontier scrub surface this round re-grounds (SR1/SR3/SR6) with an overstated repair claim.
3. **First quote is a splice, not a located quote.** Staged: `> For performance reasons, ext4 by default only writes filesystem metadata` then a new line `> file data blocks are /not/ guaranteed…`. Live page (`journal.html` sha256 `2e6693a2…5649`, banner "The Linux Kernel 7.3.0"): "ext4 by default only writes filesystem metadata through the journal. This means that file data blocks are /not/ guaranteed to be in any consistent state after a crash." The staged block drops "through the journal. This means that" with no ellipsis; QUALITY 19/21 require an exact ≤25-word located quote. The second quote ("The ioctl may be useful when snapshotting a system or for complying with content deletion SLOs.") does match the page (section 3.6.11 Journal Checkpoint).
4. **"No ext4 anywhere" negative** names `findmnt` but no command line, scope or date (QUALITY 9). Also "the three mount options are the whole of the difference" is an exhaustive claim over a positive definition (QUALITY 22).
5. No `## QUALITY check` (QUALITY 14). Source is `…/doc/html/latest/…` (mutable); the pin is only the "7.3.0" banner, which still held on 2026-10-26.

Facts it gets right (do not need a flip): the `data=ordered` default meaning, `data=journal`/`data=writeback` options, `EXT4_IOC_CHECKPOINT` flag names and "cannot both be set", all present on the live page.

## 6. Also rejected (carried): `btrfs-ioctl-surface-r27.md` P2/P3

Unchanged since round 42 (`btrfs-ioctl-surface-r27.md:14,31-32`); see `.ufo/waves/round-42/w1/AsmGate.md` for the pinned-source falsification (`frozen/src/scrub.c:421,965,986,1200,1792` use SCRUB/_CANCEL/_PROGRESS absent from the nine-row table). I re-read only the three lines above, not its table.

## Not done

- Did not re-open S269/S270 rows' `quote` cells against the page beyond the two quotes in the entry; did not verify the other 68 staged entries beyond the theme grep.
- Did not run any census, counter or the lane's gates; did not diff the staged entry against round-42 landed text.
- The "decision whether `/etc/initcpio` belongs in `boot_inputs_newer`" is not made here.
- Tool installs: none. No lane or register file touched.

Report: .ufo/waves/round-43/w1/AsmGate.md
