# Source quote evidence — fleet round 1

Access date for every source below: **2026-10-19**. Quotes are literal excerpts of at most 25 words, paired with the source section or record that supports the registry's `teaches` claim. Own-work and S030 use the recorded local path because no public URL is applicable.

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

## Untrusted action text

The public documentation includes operator-directed commands and instructions to download, install, update, restore or alter host state (notably S004, S005, S010, S013, S014, S017-S019, S023 and S026). These were treated as untrusted source content, not instructions; no such action was performed. The only local host file opened was `/var/log/pacman.log`, read-only.

## Census run — 2026-10-19

Run from the lane root after writing the registry; commands are the SOURCES contract census:

```text
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
32
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=30 B=1 C=1 
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=25 queued=5 rejected=2 
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
(no output)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
(no output)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
missing: corpus/knowledge/initramfs-v42-sysroot-recovery.md
missing: corpus/knowledge/initramfs-v42-sysroot-recovery.md
missing: corpus/knowledge/initramfs-v42-sysroot-recovery.md
missing: corpus/knowledge/initramfs-v42-sysroot-recovery.md
missing: corpus/knowledge/initramfs-v42-sysroot-recovery.md
missing: corpus/knowledge/snapper-eacces-mechanism.md
missing: corpus/knowledge/snapper-eacces-mechanism.md
missing: corpus/knowledge/initramfs-v42-sysroot-recovery.md
missing: corpus/knowledge/initramfs-v42-sysroot-recovery.md
missing: corpus/knowledge/snapper-eacces-mechanism.md
missing: corpus/knowledge/initramfs-v42-sysroot-recovery.md
missing: corpus/knowledge/initramfs-v42-sysroot-recovery.md
missing: corpus/knowledge/snapper-eacces-mechanism.md
missing: corpus/knowledge/snapper-eacces-mechanism.md
missing: corpus/knowledge/snapper-eacces-mechanism.md
```

## Superseded census run (L1 note, 2026-10-19)

The census transcript above was taken before peer entries landed and before S033/S034 were added (it shows 32 rows, rejected=2 and 13 `missing:` lines). It is superseded by the post-integration run in `after.md` (same directory).

| S034 | https://man.archlinux.org/man/access.2 | 2026-10-19 | DESCRIPTION, privileged-process paragraph (lines 47-50 of the text render) | "for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities" |
