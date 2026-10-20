# Snapper plugin writer

Model: openai-codex/gpt-6-luna. Author-side draft only; no admission authority.

[obs] `/usr/lib/snapper/plugins/10-limine-snapper-sync` filters to `SUBVOLUME=/` and maps `create-snapshot-post`, `delete-snapshot-post`, and `modify-snapshot-post` to `add`, `delete`, and `modify` respectively (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1110-1112,1227-1235). Add requires `/.snapshots/<id>/info.xml` and skips writable-copy descriptions; add/delete skip when the sync service or watcher is active (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1139-1155,1157-1169).
[obs] The command adds `--add <id>` for add and `--debounce` for delete/modify (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1174-1179). It launches asynchronously through `systemd-run` with unit `limine-snapper-${op}-${SNAP_ID}-$$`; without systemd-run it uses detached `setsid` if available, otherwise backgrounds the command (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1181-1195).

[obs] Journal events show `limine-snapper-add-1-5846.service` and `limine-snapper-add-2-260668.service`, both updating `/boot/limine.conf` (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:11-12). The nearby commands are Snapper create operations (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:29,43).

[inf] Event line 11 is paired with the 09:03:02 create command at line 29; line 12 is paired with the 09:29:19 create command at line 43, based on adjacent timestamps and `add` unit IDs 1 and 2 (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:11-12,29,43). The unit suffix PID differs from each sudo Snapper PID, consistent with the plugin's `$$` being its own shell PID, not the Snapper command PID (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:11-12,29,43; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1183-1188).

[unk] The journal rows do not directly record plugin `ACTION` or `SUBVOLUME`; plugin attribution and root-filter application to each event follow the matching unit pattern and source mechanism.

Scope: executed=none
