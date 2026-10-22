# ExecBootChainAudit — C2/P3 capability run (round 24, wave 1)

Verdict: `tools/boot-chain-audit.sh` selftest passes (45/45) and the live audit of the host exits 0 with summary `TSUKUROI_BOOTCHAIN: CONSISTENT`; the boot chain is byte-path-consistent for every 42.2 image (init mounts `/sysroot`, `image /new_root` is a symlink to sysroot, both hooks still address `/new_root`), the snapshot-2 entries carry the same 42.2 images, and the one remaining old-image snapshot entry (snapshot 1, 41.1) is a real-directory pre-42 layout that is itself consistent with its own `/new_root` init. The firmware-selected entry `//linux` is not certified BOOTED-OBSERVED today: rule 2's boot-input freshness clause fails because `/usr/lib/modules/.old` carries an mtime 19 seconds after boot start. Exit codes: selftest 0, live 0.

## Artifacts (all under the lane repo)

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecBootChainAudit/selftest.out` — selftest stdout, 52 bytes, sha256 `50054561f68fe1c3b97f12722b18050d9ea43e357f2ba36605fbf641d2c2ede8`.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecBootChainAudit/selftest.err` — empty, 0 bytes.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecBootChainAudit/selftest.exit` — `exit=0`.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecBootChainAudit/live.out` — live TSV + counts + summary, 2084 bytes, sha256 `c1b4971335d40a0937b81e7d2bc973bc8d00480fd33766989e419221d54978d0`.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecBootChainAudit/live.err` — empty, 0 bytes.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecBootChainAudit/live.exit` — `exit=0`.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecBootChainAudit/transcript.txt` — both commands, exit codes, output digests, repeat runs, and the read-only supporting probes.

## Findings

1. [obs] Selftest: `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=45 failed=0`, exit 0. Repeat run produced the identical stdout digest (sha256 `50054561…`), confirming hermetic determinism. (`live.out`/`selftest.out` above; exit 0 in `selftest.exit`.)

2. [obs] Live audit: exit 0, summary `TSUKUROI_BOOTCHAIN: CONSISTENT`, counts `entries=6 kernels=5 booted=0 path-aliased=3 pre42=1 untested=1 not-kernel=1 unknown=0 b2_mismatch=0` (`live.out` line 8–9). No EVALUATION-ERROR, no b2 mismatch, no unclassified combination: all six limine `path:` records were evaluated (`sudo -n cat -- /boot/limine.conf | grep -c 'path:'` = 6).

3. [obs] Per-entry verdicts (live.out lines 2–7):
   - `//linux` (`/EFI/Linux/omarchy_linux.efi`, sha256 `2e9c9bdc…`, uname `7.2.11-arch1-1`) → **PATH-ALIASED-EMULATED**, selected=true.
   - `//linux-lts` (`/EFI/Linux/omarchy_linux-lts.efi`, sha256 `2d49da06…`, uname `6.18.57-2-lts`) → **UNTESTED**, selected=false.
   - `///2026-10-20 09:29:19 ////linux` (snapshot 2, rootflags `subvol=/@/.snapshots/2/snapshot`) → **PATH-ALIASED-EMULATED**.
   - `///2026-10-20 09:29:19 ////linux-lts` (snapshot 2) → **PATH-ALIASED-EMULATED**.
   - `///2026-10-20 09:03:02 ////linux` (snapshot 1, rootflags `subvol=/@/.snapshots/1/snapshot`) → **CONSISTENT-PRE42**.
   - `/EFI fallback` (`/EFI/BOOT/BOOTX64.EFI`) → **NOT-A-KERNEL-ENTRY**.

4. [obs] Entries carrying 42.2 images with the new_root symlink: `//linux`, `//linux-lts`, snapshot-2/linux, snapshot-2/linux-lts. All four have `VERSION=42.2`, `init_sysroot_refs=7`, `init_new_root_refs=0`, `image_new_root=symlink->sysroot`, `latehooks=plymouth btrfs-overlayfs`, both hook roots `/new_root` (live.out lines 2–5). Independent corroboration: `sudo -n lsinitcpio -l` on the current UKI and on the snapshot-2 copy lists `new_root` (symlink, no trailing slash) and `sysroot/`; the installed `/usr/lib/initcpio/init` has 7 `sysroot` and 0 `new_root` references; `/usr/lib/initcpio/functions:1213` is `ln -s "sysroot" "$buildroot/new_root"`; hooks `btrfs-overlayfs:4` and `plymouth:11` still name `/new_root` (same lines as committed capture `.ufo/waves/round-24/capture/l1/capture.txt` lines 93–94 and 117).

5. [obs] Snapshot entries still carrying older images: exactly one — `///2026-10-20 09:03:02 ////linux` (snapshot 1). It holds `VERSION=41.1`, uname `7.2.3-arch1-3`, `init_sysroot_refs=0`, `init_new_root_refs=7`, `image_new_root=directory`, verdict CONSISTENT-PRE42 (live.out line 6). Corroborated by `sudo -n lsinitcpio -l` on the snapshot-1 image listing `new_root/` as a directory with no `sysroot/` entry. Snapshot 2 (both kernels) holds the 42.2 symlink images, so snapshot 2 is not an "older image" snapshot. There is no snapshot-1/linux-lts entry in the menu (only 6 path records).

6. [obs] The firmware-selected entry today is `//linux` (`LoadererEntrySelected=Omarchy.linux`, `LimineLastBootedEntry=Omarchy/linux`). Both recent boots — −1 at 2026-10-20 09:57:09 and 0 at 2026-10-22 04:55:41 — ran kernel `7.2.11-arch1-1`, matching the `//linux` image's uname and sha256 `2e9c9bdc…` whose file mtime (2026-10-20 09:26:22) precedes both boot starts. [inf] These two boots executed the audited 42.2 `//linux` image (the booted file's sha is not separately observable from an unprivileged shell; the tool carries that class via rule 2, which does not fire today — see finding 7).

7. [obs] Rule 2 (BOOTED-OBSERVED) is not reachable today for `//linux`: the condition requires `boot_inputs_newer == 0`, but `find /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d /etc/default/limine /etc/limine-snapper-sync.conf /usr/lib/initcpio /usr/lib/modules -newermt "@1792655724"` returns `/usr/lib/modules/.old` (mtime 2026-10-22 04:55:43) — 19 seconds after boot start (btime 1792655724 = 2026-10-22 04:55:24). The image mtime (1792499182) is before btime, so the mtime clause passes; the freshness clause fails. The tool therefore falls through to rule 4 → PATH-ALIASED-EMULATED (same image facts, no boot proof; `tools/boot-chain-audit.sh:761–764`). This differs from the round-17 corpus record, which listed `linux` as BOOTED-OBSERVED — i.e. the round-17 verdict class is not reproduced by the current tool on the current host state. [inf] `/usr/lib/modules/.old` is the modules-cleanup directory (`linux-modules-cleanup.service` ExecStart rsyncs unowned kernel module trees into it with `rsync -AHXal "<i>" /usr/lib/modules/.old/`); its mtime is refreshed during/before boot 0, so rule 2's sweep sees a newer input on this host after every boot. This is a tool-vs-host interaction to flag, not a boot-chain defect: it only blocks the *observed-boot* certificate, not the image-path consistency verdicts.

8. [obs] The `snapshot_ro` column reads `-` for both snapshot entries today (live.out lines 4–5). The tool runs `btrfs property get -t subvol <path> ro` unprivileged (`tools/boot-chain-audit.sh:404–426`); unprivileged it fails with `ERROR: Could not open: Permission denied` (`/.snapshots` is root-only). With `sudo -n`, the same probe returns `ro=true` for both snapshot 1 and snapshot 2 subvolumes, matching the round-17 corpus's recorded `true`. This column is report-only per the tool's schema and is not a verdict input, so it does not affect the summary.

9. [obs] `/boot/limine.conf` was rewritten today at 2026-10-22 05:05:39 by `limine-snapper-sync` after `snapper-cleanup` (journal at 05:05:39: `Updated: /boot/limine.conf`). The audited menu (6 path records) is the post-boot-0 menu; limine.conf is deliberately excluded from rule 2's input set (the tool's documented design), so the rewrite does not change verdicts. The current menu still contains snapshot 1 and snapshot 2 entries and both kernels.

10. [obs] Read-only guarantee held: no pacman transaction, no service restart, no /boot write, no config write; the only privileged steps were `sudo -n cat`/`sudo -n stat`/`sudo -n lsinitcpio -l`/`sudo -n btrfs property get` reads; no private mktemp trees remained (`ls -d /tmp/tmp.* | wc -l` = 0). Both runs re-executed identically (repeat-run digests equal).

11. [unk] The tool cannot certify sha-equality between the file that booted and the currently-pinned `//linux` image (rule 2 unreachable, finding 7), so "both completed boots ran the audited bytes" is [inf], not observed, on this run.

## Risks / notes for the L1

- The CONSISTENT summary is not evidence that boot 0 was *observed* to succeed at the UKI/root-mount level; it is a byte-level path-consistency statement. The selected entry is PATH-ALIASED-EMULATED (image `new_root` → sysroot symlink), not BOOTED-OBSERVED.
- If the gate premise P3 wants "two completed boots on 42.2 images", the boot completion facts are in the committed capture (boots −1 and 0, `.ufo/waves/round-24/capture/l1/capture.txt` lines 15–16; kernel `7.2.11-arch1-1` both boots) and in journal, not in this tool's verdicts, because rule 2 is currently blocked by `/usr/lib/modules/.old` (finding 7).
- The round-17 corpus entries in `corpus/knowledge/boot-chain-r17.json` show `snapshot_ro: true`; the current tool prints `-` (finding 8). If the L1 wants the `ro` column populated, the tool would need a privileged `btrfs property get` (or the L1 captures it separately, as in round 17).

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/boot-chain-audit.sh,/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/boot-chain-r17.json,/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/boot-chain-r17.md,/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/capture/l1/capture.txt,/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1-spec.json; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecBootChainAudit.md,/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecBootChainAudit/{selftest.out,selftest.err,selftest.exit,live.out,live.err,live.exit,transcript.txt}; executed=bash tools/boot-chain-audit.sh --selftest (exit 0), bash tools/boot-chain-audit.sh --live (exit 0), repeat runs of both (exit 0), read-only probes (sudo -n stat / lsinitcpio -l / btrfs property get / cat /boot/limine.conf; find -newermt; stat; systemctl cat; journalctl reads)
Installs: none
