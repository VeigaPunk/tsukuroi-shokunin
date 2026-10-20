# SentHostSafety — r17 (boot-chain-audit contract spec.json:20; L0 option b)

Tool (not yet written):
1. HIGH [obs] upstream lsinitcpio `-a` runs `. "$workdir/initcpio/config"` (raw.githubusercontent.com/archlinux/mkinitcpio/master/lsinitcpio, analyze_image, 2026-10-20). Never `-a`/source image files; regex-parse; selftest `$(touch canary)` stays absent.
2. HIGH root writes (`sudo -n objcopy` out-path) into user mktemp: symlink clobber; root leftovers defeat trap. Root only `sudo -n cat -- "$efi" >copy`; hash/extract copy unprivileged; refuse EUID 0.
3. HIGH `path: boot():/../etc/shadow` copies secrets. Accept `^boot\(\):/[A-Za-z0-9._/-]+(#[0-9a-f]{128})?$`, no `..`, realpath under /boot; guid()/BOOTX64.EFI (capture:156) NOT-A-KERNEL pre-read.
4. MED TOCTOU: limine-snapper-sync enabled (fresh-capture:47-48). Re-hash source at end; flock-probe /run/lock/boot-partition.lock (limine-mutex:18) only if present.
5. MED `lsinitcpio -x` extracts to CWD: `cd "$d" || exit 2`; TMPDIR="$tmp"; one entry at a time (/tmp inodes, l0-questions.md:46); chmod u+w before rm.
6. MED no /sysroot-hooks rule (boot-chain-r17.json:28-42): unknown→exit 2.

Option (b) (l0-questions.md:60):
7. HIGH vgpnk-staged /etc installs (capture:83-97). Root copies the package hook, edits line 4, verifies one-line diff, root:root 0644.
8. HIGH limine-update replaces the only BOOTED-OBSERVED image; #1/#2 cleanup=number (capture:166-167) prunable. Pin #1; audit; attended reboot.
9. MED [inf] sha-named history (capture:114-116): #2 stays degraded. /etc shadows package (functions:977); record eeac1ed3, drop after upstream.

[unk] snapshot-description sanitizing; NUMBER_LIMIT. Seat-scope breach: two bash calls below (read-only, no host probe).

Scope: executed=sed -n 60p /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md | fold -w 400,true
