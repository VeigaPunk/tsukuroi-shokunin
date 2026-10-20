# C2 aux — lss CHANGELOG versions (installed 1.32.1-2)

Source: r19b:971-1091 grep (`head -n 120`; stops at CHANGELOG:359, pre-1.16.1 absent). Model: commandcode/deepseek/deepseek-v4.1-flash.

## Versions

- **1.21.0 (2026-01-24)**, r19b:1053/1056: "The `inotify-tools` package is no longer required; the snapper plugin is used instead." [obs] Switchover version; exact plugin-code introduction [unk] (Added bullets unmatched by grep).
- **1.29.0 (2026-05-19)**, r19b:992/994: "New `--add <ID>` option to prevent out-of-sync issues when many snapshots are added in a very short time." [obs] Also r19b:999: "snapper plugin: Removed the 1-second delay when adding a snapshot..." [inf] `--add` is the floor for observed `limine-snapper-add-*` units (plugin passes it, block r19b:1093-1245, line 85).
- **1.30.0 (2026-06-04)**, r19b:987/989: "`inotifywait` fallback now shows an info message instead of a warning when Snapper plugin integration is active." [obs] Explains boot-time watcher lines (r19b:1645); watcher exits without inotifywait (r19b:1365-1367), so it cannot write /boot here.
- **ExecStopPost / cleanup-time sync absent from slice** [unk]; override package-shipped (r19.txt:45-47), active (r19.txt:256-260), introduction below truncation. Gap, not contradiction.

## Against Goal

- Unit template exact: `--unit="limine-snapper-${op}-${SNAP_ID}-$$"` (plugin line 92); `$$` is the plugin's PID, not the writer PID (add-1-5846 vs 5929, r19c:11) — naming trap only.
- [obs] 2 ALPM-SCRIPTLET writes are not lss's hook: 90-mkinitcpio-install.hook → limine-mkinitcpio-install (r19.txt:397) emitted both (r19.txt:578, 597). lss's 10-limine-snapper-lock.hook only mutex-waits (r19b:1396); README r19b:903 "wait for sync completion" is that wait — do not attribute ALPM writes to lss.
- [obs] Plugin acts only on `SUBVOLUME="/"` (line 18), consistent with 8 cleanup + 2 add rows (r19c:11-20); no visible entry removes watcher or plugin (r19b:888, r19.txt:35).

Scope: executed=none
