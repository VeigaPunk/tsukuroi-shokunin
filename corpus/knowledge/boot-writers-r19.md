source: own-work S066 .ufo/waves/round-19/l1-capture/host-capture-r19.txt; S067 host-capture-r19b.txt; S068 host-capture-r19c.txt (read-only L1 captures 2026-10-20); docs S070 systemd.service(5) ExecStopPost=; S071 systemd.timer(5) OnBootSec=/OnUnitActiveSec=/AccuracySec=; S072 systemd-run(1) --unit=/--collect; S073 snapper(8) PLUGINS v0.13.2; S074 limine-snapper-sync README 1.32.1 § Core sync system line 826; S075 limine-entry-tool README 1.40.0 § Arch Linux line 258; code S076 limine-snapper-sync commit 754090077de4 (issue 4 fix: sync after cleanup); existing S007 pacman.conf(5) HookDir and S008 alpm-hooks(5) OVERRIDING HOOKS
verified-at: 2026-10-20T17:58-03:00 capture
recheck: 30d; procedure: re-run `.ufo/waves/round-19/l1-capture/capture-r19.sh`, `capture-r19b.sh` and `capture-r19c.sh` (read-only: each header states no pacman, sudo, limine-update, limine-snapper-sync, service action or /boot write; each prints `$ cmd`, output, `[rc=N]`), then `python3 tools/check-boot-writers.py --revision <REV>` (REV = a landed hex revision per corpus/QUALITY.md criterion 27). The lane user cannot stat /boot without sudo; this recheck uses no sudo.

# /boot writers for /boot/limine.conf — round 19 (C2)

Authority: observation from three read-only captures taken 2026-10-20 17:55–17:58 -03:00 and packaged files on the host. Nothing here authorizes a package, service, hook, initramfs, bootloader or /boot change. Tags: [obs] = read from a named line; [inf] = inference from named lines; [unk] = not captured.

Line references: `r19:N` = host-capture-r19.txt:N; `r19b:N` = host-capture-r19b.txt:N; `r19c:N` = host-capture-r19c.txt:N. Packaged-file lines cite `file:N`. In r19b, `cat -n` output is numbered from the header: plugin file line N = r19b:1093+N; watcher line N = r19b:1246+N; the four hook files are numbered continuously from r19b:1399 (cat line N = r19b:1399+N).

## Writer classes

### W-SNAPPER-CLEANUP
- Trigger: [obs] `snapper-cleanup.timer` with `OnBootSec=10m` and `OnUnitActiveSec=1h` (r19:227-228), enabled (r19:203); next run 18:07:16 (r19:265).
- Mechanism: [obs] drop-in `/usr/lib/systemd/system/snapper-cleanup.service.d/limine-snapper-override.conf` adds `ExecStartPre=-touch /run/limine-snapper-cleanup.lock` (r19:258), `ExecStopPost=-rm -f` (r19:259) and `ExecStopPost=limine-snapper-sync` (r19:260; no `-` prefix). The sync runs when the cleanup service stops.
- Signature: [obs] journal `_SYSTEMD_UNIT=snapper-cleanup.service`, MESSAGE `Updated: /boot/limine.conf`; eight rows, 10:07:03 to 17:07:16 (r19c:13-20). These lines carry no `Copied:` or `Saved:` (r19:446-521; r19:541-560).
- Writes: [obs] /boot/limine.conf only, as far as the captured lines show.

### W-SNAPPER-PLUGIN
- Trigger: [obs] snapper post-actions for subvolume `/` only (plugin:18, r19b:1111); dispatch `create-snapshot-post` to `run_sync add` (plugin:135-136, r19b:1228-1229).
- Guard: [obs] skip when `systemctl is-active limine-snapper-sync.service` (plugin:69, r19b:1162) or `pgrep -f limine-snapper-watcher` matches (plugin:73, r19b:1166).
- Mechanism: [obs] `systemd-run --unit=limine-snapper-${op}-${SNAP_ID}-$$ … --collect` runs `limine-snapper-sync --add <id>` (plugin:92 and :85, r19b:1185 and 1178). `$$` is the plugin shell PID: unit `limine-snapper-add-1-5846` was created by plugin PID 5846; the sync child was PID 5929 (r19c:11).
- Signature: [obs] unit `limine-snapper-add-<id>-<pid>.service` (r19c:11-12; deactivation r19c:65-68); `Copied:`, `Saved:` and `Updated:` lines from the same PID (r19c:23-25, 39-42).
- Writes: [obs] /boot/limine.conf; copies of `/boot/EFI/Linux/omarchy_linux.efi` and `omarchy_linux-lts.efi` into `/boot/<machine-id>/limine_history/`; `snapshots.json` (r19c:23-25, 39-41). The copy source is the actual UKI path.
- Events: 2. add-1 at 09:03:03 follows `snapper -c root create` at 09:03:02 (r19c:27-29). add-2 at 09:29:19 shares the second with `snapper -c root create … pre-aur-elephant-2.22.1` (r19c:43). [inf] The link is time coincidence plus the sudo record, not a process identity.
- [inf] Neither add was skipped by the guard, so `limine-snapper-sync.service` was inactive and no watcher process matched at 09:03:02 and 09:29:19.

### W-WATCHER (dormant)
- Unit: [obs] `limine-snapper-sync.service` enabled (r19:193, :213), `ExecStart=limine-snapper-watcher`, `Restart=on-failure` (r19:161-162), WantedBy multi-user (r19:210). [unk] ActiveState (r19:208-214 captures enablement only).
- Mechanism: [obs] the watcher runs an initial sync when `/.snapshots` is missing (watcher:114-117, r19b:1360-1363). When `inotifywait` is absent it prints `inotifywait is not installed. Falling back to Snapper plugin integration.` and exits 0 (watcher:119-122, r19b:1365-1368). The monitor loop that would write (watcher:125-134, r19b:1371-1380) is not reached in that case.
- Signature: [obs] fallback line at 08:11:47, 22:48:24, 06:37:55, 08:58:01, 09:10:54 and 09:57:11 (r19b:1645, 1655, 1665, 1675, 1678, 1683). Boot-time initial-sync attempts at 22:48, 06:37 and 08:58 failed `create-config` with errno 13 (r19b:1647-1654, 1657-1664, 1667-1674; failure lines 1650, 1660, 1670) and logged no `Updated:` line.
- Writes: none attributed in the captured window. All ten journal `Updated:` events are on `snapper-cleanup.service` or `limine-snapper-add-*` (r19c:11-20).
- [inf] Dormant: the script exits after the fallback message, so the unit should not stay active. [unk] Why watcher PID 10021 started at 09:10:54 (r19b:1678): the sudo filters of capture-r19c.sh:18-19 do not cover that minute.

### W-MKINITCPIO-HOOK
- Hook: [obs] `/etc/pacman.d/hooks/90-mkinitcpio-install.hook`, owned by limine-mkinitcpio-hook 1.40.0-2 (r19:87); PostTransaction; Exec `/usr/share/libalpm/scripts/limine-mkinitcpio-install` (r19:397; r19b:1458).
- Shadowing: [obs] same-name `/usr/share/libalpm/hooks/90-mkinitcpio-install.hook` (Exec `mkinitcpio install`, r19b:1506). ALPM prints one `running '90-mkinitcpio-install.hook'` per transaction (r19b:1691, 1693, 1698). The UKI build text is limine's (r19:576-597). [inf] The /etc copy is the operative one (S008; precedence per S007; pacman.conf HookDir not captured [unk]).
- Effective config: [obs] `ESP_PATH="/boot"`, `ENABLE_UKI=yes`, `CUSTOM_UKI_NAME="omarchy"` (r19:420, :423-424).
- Mechanism: [obs] the script text has no `cp`, `Copied`, `Updated` or limine.conf write; its one /boot-related line is `BOOT_PATH="$ESP_PATH"` (r19b:1510). [inf] The writes happen in a binary the script invokes. The package owns `limine-entry-tool` (r19:91); its README says it "generates, updates, and removes boot entries with periodic `limine.conf` backups" (README:17, via r19b:1512-1633) and copies the UKI to `$ESP_PATH/EFI/Linux/` (README:108). [unk] the invoked binary body is not captured.
- Signature: [obs] ALPM-SCRIPTLET `==> Creating unified kernel image`, `Copied: /tmp/limine-mkinitcpio.*/linux.efi -> /boot/EFI/Linux/omarchy_linux.efi`, `Updated: /boot/limine.conf` (pacman.log 3012-3015, 3044-3047; r19:576-578, 595-597). Same pattern on 2026-10-11 (pacman.log 2020-2021; r19b:1694-1695).
- Writes: [obs] `/boot/EFI/Linux/omarchy_linux.efi`, `omarchy_linux-lts.efi`, `/boot/limine.conf`.
- Events: 3 (10-11 16:16:36; 10-20 09:18:18; 10-20 09:18:24).

### W-LIMINE-EFI-COPY
- Hook: [obs] `/etc/pacman.d/hooks/99-limine.hook`; Install/Upgrade of package `limine`; PostTransaction; Exec `/bin/sh -c "/usr/bin/cp …BOOTIA32.EFI /boot/EFI/BOOT/ && …BOOTX64.EFI /boot/EFI/BOOT/"` (r19:399-403; r19b:1469). [unk] owner: not in the limine-snapper-sync or limine-mkinitcpio-hook file lists (r19:15-68, r19:72-131); the limine package list is not captured (r19:8-9 names the package only).
- Invocation: [obs] `running '99-limine.hook'` on 2026-10-11 (pacman.log 2024; r19b:1696) and 2026-10-20 (pacman.log 3050; r19b:1703). [inf] ALPM runs a hook only when its target matched, so `limine` was in those transactions.
- Signature: none. [inf] `cp` without `-v` prints nothing; the full-log grep for `-> /boot/` returns no copy line (r19b:1688).
- Writes: /boot/EFI/BOOT/BOOTIA32.EFI and BOOTX64.EFI. Not limine.conf. [unk] completion: no exit status is logged.

### W-LIMINE-EFI-DEPLOY
- Hook: [obs] `/usr/share/libalpm/hooks/80-limine-efi-deploy.hook`, owned by limine-mkinitcpio-hook (r19:125); Install/Upgrade of limine, limine-git, limine-dev, limine-mkinitcpio-hook(-git); PostTransaction; Exec `/usr/bin/limine-install` (r19:359-367; r19b:1428).
- Invocation: [obs] `running '80-limine-efi-deploy.hook'` at pacman.log 1352 (2026-10-03), 1983 (10-11) and 2977 (10-20) (r19b:1690, 1692, 1697).
- Writes: [inf] EFI binaries under /boot/EFI. README:37 names `EFI/limine/limine_x64.efi`; README:43 names an overwrite of `EFI/BOOT/BOOTX64.EFI` (limine-entry-tool README, r19b:1512-1633). [unk] whether that overwrite is enabled: `/etc/limine-entry-tool.conf` content is not captured (r19:131 names the backup only).
- Signature: [obs] none. limine-install prints no `-> /boot/` line in the captured windows (r19b:1688).
- Events: 0 limine.conf writes.

### W-KERNEL-REMOVE
- Hooks: [obs] `/usr/share/libalpm/hooks/60-limine-mkinitcpio-remove-pre.hook` (PreTransaction, Remove, Target `usr/lib/modules/*/modules.builtin`, Exec `limine-mkinitcpio-remove pre`; r19:354-358, :357) and `90-limine-mkinitcpio-remove-post.hook` (PostTransaction, Remove, Exec `… post`; r19:368-371). Owner limine-mkinitcpio-hook (r19:124, :126).
- Mechanism: [obs] README:142 says removal deletes the kernel entry and its directory; README:156 says it removes the UKI entry and file at `$ESP_PATH/EFI/Linux/${machine_id}_<kernel>.efi` (r19b:1512-1633). [unk] the script body is not captured.
- Signature: none in the captured windows. [obs] the tail-40 grep covers pacman.log 2997-3162 only (r19:565-606). [unk] a full-log sweep for these hook names was not captured.
- Writes: [inf] limine.conf and UKI files on removal.
- Dormant in the captured windows: no removal transaction appears.

## Event table

| Event | Time | Capture line | Signature (unit or ALPM) | Writer |
|---|---|---|---|---|
| EV-01 | 2026-10-11T16:16:36-0300 | `host-capture-r19b.txt:1695` | `[ALPM-SCRIPTLET] (pacman.log 2021)` | W-MKINITCPIO-HOOK |
| EV-02 | 2026-10-20T09:03:03 | `host-capture-r19c.txt:11` | `limine-snapper-add-1-5846.service` | W-SNAPPER-PLUGIN |
| EV-03 | 2026-10-20T09:18:18-0300 | `host-capture-r19b.txt:1700` | `[ALPM-SCRIPTLET] (pacman.log 3015)` | W-MKINITCPIO-HOOK |
| EV-04 | 2026-10-20T09:18:24-0300 | `host-capture-r19b.txt:1702` | `[ALPM-SCRIPTLET] (pacman.log 3047)` | W-MKINITCPIO-HOOK |
| EV-05 | 2026-10-20T09:29:19 | `host-capture-r19c.txt:12` | `limine-snapper-add-2-260668.service` | W-SNAPPER-PLUGIN |
| EV-06 | 2026-10-20T10:07:03 | `host-capture-r19c.txt:13` | `snapper-cleanup.service` | W-SNAPPER-CLEANUP |
| EV-07 | 2026-10-20T11:07:04 | `host-capture-r19c.txt:14` | `snapper-cleanup.service` | W-SNAPPER-CLEANUP |
| EV-08 | 2026-10-20T12:07:07 | `host-capture-r19c.txt:15` | `snapper-cleanup.service` | W-SNAPPER-CLEANUP |
| EV-09 | 2026-10-20T13:07:10 | `host-capture-r19c.txt:16` | `snapper-cleanup.service` | W-SNAPPER-CLEANUP |
| EV-10 | 2026-10-20T14:07:12 | `host-capture-r19c.txt:17` | `snapper-cleanup.service` | W-SNAPPER-CLEANUP |
| EV-11 | 2026-10-20T15:07:12 | `host-capture-r19c.txt:18` | `snapper-cleanup.service` | W-SNAPPER-CLEANUP |
| EV-12 | 2026-10-20T16:07:16 | `host-capture-r19c.txt:19` | `snapper-cleanup.service` | W-SNAPPER-CLEANUP |
| EV-13 | 2026-10-20T17:07:16 | `host-capture-r19c.txt:20` | `snapper-cleanup.service` | W-SNAPPER-CLEANUP |

Registry: `corpus/knowledge/boot-writers-r19.json` (schema tsukuroi-boot-writers-r19-v1); the gate enumerates the `Updated: /boot/limine.conf` lines of the two declared probe blocks itself (r19c:5 journal json probe; r19b:1688 whole-log pacman.log grep) and requires one claim per line. The tag-agnostic journal grep at r19:524-563 (count 10, r19:562-563) is the cross-check that no other identifier logged the same message.

Count: 13 attributed events = 10 journal rows (r19c:11-20) + 3 pacman.log ALPM rows (pacman.log 2021, 3015, 3047 = r19b:1695, 1700, 1702). The declared count of 12 (SCORECARD round-19 declaration) omitted the 2026-10-11 row (pacman.log:2021); ScribeWritersEntry and CritWritersCircular found it, and the measured count is 13. Input set: the journal `grep -c` at r19b:1685-1686 (10) and the full-log grep at r19b:1688 (15 matches, of which 3 are `Updated:`).

## Operator decision rule

Apply to each `/boot/limine.conf` mtime M later than the last pacman transaction T before M. The lane cannot read /boot (r19:437-441), so an operator with sudo applies this rule. mtime alone does not attribute a write; attribution uses the journal and pacman.log.

1. Expected: a journal `Updated: /boot/limine.conf` whose `_SYSTEMD_UNIT` matches `^snapper-cleanup\.service$` or `^limine-snapper-(add|delete|modify)-[0-9]+-[0-9]+\.service$`, within 2 s of M (FAT 2-second timestamps; boot-chain-r17.md:36).
2. Expected: a pacman.log `[ALPM-SCRIPTLET] Updated: /boot/limine.conf` inside a transaction that also has `running '90-mkinitcpio-install.hook'`.
3. Report: any other `Updated: /boot/limine.conf` line, or any `/boot/EFI/Linux/*.efi` change with no pacman hook run in its transaction. An operator-invoked `limine-update` is in this class: the 2026-10-20 09:26:11 UKI rebuild was operator-invoked (boot-chain-r17.md:25-26), so it is reported, not cleared.
4. No write: a snapper-cleanup run with no `Updated:` line is not a write. Example: one run at 09:08:04 logs no limine-snapper-sync line (r19c:46-57); its cause is [unk].

## Limits

- [obs] /boot is root:root 700; `stat` of `/boot/limine.conf` is denied to the lane (r19:437-441). This entry reads no /boot file and states no /boot mtime, hash or content.
- [obs] No current-state certification. The captures were taken at 17:55–17:58 -03:00 and establish events up to then only.
- [obs] Scope: journal since 2026-10-19 00:00 (r19:524; r19c:5); retained boots start 2026-10-19 00:34 (r19b:5-11). pacman.log: full-log grep at r19b:1688 (3169 lines, r19:607-609). Earlier journal is not attributed.
- [inf] `Updated:` is the tool's own log message. The content change is not verified; no hash of limine.conf is captured.
- [unk] Cleanup run at 09:08:04 with no `limine-snapper-sync` line (r19c:46-57). RevCleanupHook's lead [inf]: that run logged the description `Daily Cleanup of Snapper Snapshots` (r19c:47-48) while the 09:03:03 start logged `Hourly` (r19c:46), so a pre-upgrade unit without the ExecStopPost wiring may have been loaded (snapper and limine-snapper-sync were upgraded at ~09:16 in the 09:15 -Syu, boot-chain-r17.md:22); unverified, the unit file loaded at 09:08 is not captured.
- [unk] Watcher PID 10021 start at 09:10:54 (r19b:1678).
- [unk] Watcher ActiveState (r19:208-214 captures enablement only).
- [unk] Bodies of limine-install, limine-mkinitcpio-install and limine-mkinitcpio-remove; the limine-entry-tool README (r19b:1512-1633) is the only description of their writes. Writer attribution inside those binaries is [inf].
- [unk] pacman.conf HookDir; `/etc/limine-entry-tool.conf` effective values; owner and file list of the `limine` package; owner of `99-limine.hook`.
- Supporting note on boot-chain-r17.md:30 (not a rewrite): its [inf] `limine-snapper-sync made the copies` is now [obs] for the 09:29:19 copies. Unit `limine-snapper-add-2-260668`, PID 260715 (r19c:12, 39-41).

## QUALITY check

Criteria evaluated: 1, 2, 3, 7, 8, 9, 25, 30 of corpus/QUALITY.md.

1. Falsifiable. Each class names the line or unit whose presence or absence would falsify it: W-WATCHER by an `Updated:` line attributed to `limine-snapper-sync.service`; the decision rule by an `Updated:` line with neither signature. The recheck commands are re-runnable.
2. Sourced. Each claim cites a capture line, a packaged `file:N`, or a SOURCES row placeholder. The 09:08:04 cleanup run, the 09:10:54 watcher start and the watcher ActiveState are `[unk]`, not asserted.
3. Separated. `[obs]`, `[inf]` and `[unk]` tag every claim. `[inf]` covers the guard-based deduction, the same-name hook override, the silent `cp`, and the ALPM hook-match rule.
7. External claims cite S070-S076 at their anchors (systemd.service ExecStopPost=; systemd.timer Options; systemd-run OPTIONS; snapper(8) PLUGINS; limine-snapper-sync README 1.32.1 line 826; limine-entry-tool README 1.40.0 line 258; commit 754090077de4). The hook-override and HookDir claims cite existing tier A rows S008 and S007, scoped to "OVERRIDING HOOKS" and "HookDir". Effective local configuration is cited: `/etc/default/limine` `ESP_PATH` (r19:420) and the /etc hook override, not the /usr/share default alone. No tier C source supports a claim.
8. `source:`, `verified-at:` (ISO) and `recheck:` (30d, with procedure) are present. The gate step's measured output is in `.ufo/waves/round-19/measure/` at the landed revision named in LOG.md.
9. Negative claims with bounded sweeps. (a) No further `Updated` line in the journal: `journalctl --no-pager -o short-iso --since "2026-10-19 00:00" -t limine-snapper-sync | grep -c "Updated: /boot/limine.conf"` returns 10 (r19b:1685-1686). Scope: retained journal, 2026-10-20. (b) No watcher- or sync-unit write: the json field filter command at r19c:5, rows at r19c:11-20, returns 10 rows, all on `snapper-cleanup.service` or `limine-snapper-add-*`. (c) No `Updated` or copy line outside the three ALPM rows: `grep -n -E "Updated: /boot/limine.conf|-> /boot/|running .99-limine.hook|running .80-limine-efi-deploy.hook|running .90-mkinitcpio-install.hook" /var/log/pacman.log` returns 15 matches (r19b:1688-1703). (d) No watcher write in fallback windows: r19b:1643-1683 shows no `Updated` line. (e) No removal-hook run: r19:565-606 covers pacman.log 2997-3162 only; the full-log sweep is `[unk]`.
25. Not applicable. No next-boot verdict or image-derived claim is made; UKI copies are cited by source path, not by equality.
30. The `Copied:` rows name the actual UKI path `/boot/EFI/Linux/omarchy_linux*.efi` as source (r19c:23, 39-40), not the history copy. No plural image-equality statement is made. Count correction: 13 (not 12), input set as in the Event table section above.

## Mechanism quotes (falsify repair, 2026-10-21)

Appended after the round-19 falsify wave (FxMutWriters survived a mutated mechanism word; QUALITY 33).
Every writer's `mechanism_refs` quote is published verbatim here so the gate can check published
mechanism fidelity, not only writer-id publication. Earlier bytes are unchanged.

**W-SNAPPER-CLEANUP**
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:47` — `usr/lib/systemd/system/snapper-cleanup.service.d/limine-snapper-override.conf`
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:260` — `ExecStopPost=limine-snapper-sync`
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:227` — `OnBootSec=10m`
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:228` — `OnUnitActiveSec=1h`
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:203` — `snapper-cleanup.timer          enabled`

**W-SNAPPER-PLUGIN**
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:42` — `usr/lib/snapper/plugins/10-limine-snapper-sync`
- `.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1185` — `--unit="limine-snapper-${op}-${SNAP_ID}-$$"`
- `.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1228` — `create-snapshot-post)`
- `.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1229` — `run_sync add "${SNAP_ID}"`

**W-WATCHER**
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:161` — `ExecStart=limine-snapper-watcher`
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:193` — `limine-snapper-sync.service    enabled`
- `.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1366` — `info_msg $"inotifywait is not installed. Falling back to Snapper plugin integration."`

**W-MKINITCPIO-HOOK**
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:87` — `etc/pacman.d/hooks/90-mkinitcpio-install.hook`
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:397` — `/etc/pacman.d/hooks/90-mkinitcpio-install.hook:Exec = /usr/share/libalpm/scripts/limine-mkinitcpio-install`
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:420` — `ESP_PATH="/boot"`

**W-LIMINE-EFI-COPY**
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:403` — `/etc/pacman.d/hooks/99-limine.hook:Exec = /bin/sh -c "/usr/bin/cp /usr/share/limine/BOOTIA32.EFI /boot/EFI/BOOT/`

**W-LIMINE-EFI-DEPLOY**
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:367` — `/usr/share/libalpm/hooks/80-limine-efi-deploy.hook:Exec = /usr/bin/limine-install`

**W-KERNEL-REMOVE**
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:357` — `/usr/share/libalpm/hooks/60-limine-mkinitcpio-remove-pre.hook:Exec = /usr/share/libalpm/scripts/limine-mkinitcpio-remove pre`
- `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:371` — `/usr/share/libalpm/hooks/90-limine-mkinitcpio-remove-post.hook:Exec = /usr/share/libalpm/scripts/limine-mkinitcpio-remove post`

## Falsify qualifications (round 19 wave 2, 2026-10-21)

Appended after the seats below; earlier bytes unchanged.
- **Watcher fallback ordering (FxRevWatcher).** The absent-`inotifywait` branch exits before the monitor loop, but an optional initial `limine-snapper-sync` call and the backgrounded pacman-lock cleanup are ordered before that check. "The fallback exits before any write path is reachable" is therefore too strong; none of the retained `Updated:` events is attributed to the watcher.
- **Absence of `Updated:` is not proof of "not a write" (FxRevExecStopPost).** The tool's own message carries no content hash and a silent/no-change path is not excluded; the 09:08:04 cause stays `[unk]`.
- **Published mechanism fidelity (FxMutWriters).** A mutated mechanism word (`ExecStopPost`→`ExecStartPost`) survived the old gate. All writer `mechanism_refs` quotes are now published in the appendix above, and `tools/check-boot-writers.py` rejects an unpublished or altered mechanism quote.
- **Capture hygiene (FxScoutCapture).** `host-capture-r19c.txt` now redacts the operator user token to `[operator]`; the registry capture digest was updated with it.

## R20-RULE4 — named supersession of Operator decision rule item 4

This block supersedes **only item 4 under `## Operator decision rule`**, whose “No write” conclusion is unsupported. Use the round19 `## Falsify qualifications` absence-of-`Updated:` qualification as controlling: **no captured `Updated:` line means no captured matching log event, not proof of no write or unchanged contents**. The source is the finite capture, not a content hash or exhaustive filesystem audit. The 09:08:04 cleanup run's cause remains `[unk]`; absence does not establish a lock skip, successful sync, failure, or a byte change. No boot/package/service action is authorized. This is a documentation correction, not a new host observation.

## Round 38 note — override rule and hook owners (appended 2026-10-26)

The [inf] "The /etc copy is the operative one" for `90-mkinitcpio-install.hook` is now source-backed: hook
directories are searched from the last list entry to the first, the first file seen per name wins, and the system
directory is the list head (HO2 in `corpus/knowledge/pacman-hook-order-r38.md`; S208 `hook.c:540`, `:588-590`;
S211 `alpm.c:56-62`). `/etc/pacman.conf` sets no `HookDir`, so the default `/etc/pacman.d/hooks/` applies. The
[unk] "owner of `99-limine.hook`" resolves: no installed package lists it (and none lists `walker-restart.hook`)
— both are local files — while the `/etc` `90-mkinitcpio-install.hook` is owned by `limine-mkinitcpio-hook`
(`.ufo/waves/round-38/w1/C2CritHO6.md` Finding 6). The text above is not rewritten.
