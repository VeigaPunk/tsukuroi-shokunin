# ScribeWritersEntry — C2 /boot writer attribution (round 19)

Deliverable: `.ufo/waves/round-19/build/drafts/ScribeWritersEntry.knowledge.md` (full `corpus/knowledge/boot-writers-r19.md` text). `<<EVENTS>>` placeholder left for the integrator. S-row IDs are placeholders pending landing.

Findings
- [obs] Count is 13, not 12: 10 journal rows (`host-capture-r19c.txt:11-20`) plus 3 pacman.log rows (`pacman.log` 2021, 3015, 3047 = `host-capture-r19b.txt:1695, 1700, 1702`). The 2026-10-11 row (pacman.log:2021) is missing from `RevPacmanHooks.writers.json`, `RevPlugin.writer.json` (events [11,12]) and `ScribeWritersRecords.events.json` (EV-01..12). Integrator: add an EV-13 for W-MKINITCPIO-HOOK and set attributed_events to 13.
- [obs] W-WATCHER is dormant. The watcher prints the fallback line and exits 0 when inotifywait is absent (`watcher:119-122`, `r19b:1365-1368`). That line appears six times (`r19b:1645, 1655, 1665, 1675, 1678, 1683`). No Updated line is attributed to its unit. ActiveState is not captured.
- [obs] The /etc `90-mkinitcpio-install.hook` shadows the /usr/share copy: ALPM logs one running line per transaction (`r19b:1691, 1693, 1698`). [inf] The /etc copy is the operative one (S008).
- [inf] The plugin guard did not skip either add (`plugin:69,73` = `r19b:1162,1166`). So the sync unit was inactive and no watcher matched at 09:03 and 09:29.
- Rejected: the tail-40 grep (`r19:565-606`) suggested 80-limine-efi-deploy never ran. Rejected: `r19b:1697` shows it ran at 09:18:13; the tail cut it off.
- Peer citation: `SrcSystemdRun.row.md` cites `host-capture-r19c.txt:14-15` for the add-unit names. Those are at lines 11-12; lines 14-15 are cleanup rows. S066 is claimed by three drafts (ScribeSourcesOwn, SrcSnapperPlugins, SrcSystemdRun); integrator to renumber.
- [unk] /boot contents and mtimes (`r19:437-441`); cleanup run at 09:08:04 with no Updated line (`r19c:46-57`); watcher PID 10021 start at 09:10:54 (`r19b:1678`); bodies of limine-install, limine-mkinitcpio-install and limine-mkinitcpio-remove; `/etc/limine-entry-tool.conf` values; pacman.conf HookDir; owner of 99-limine.hook.
- Gate `tools/check-boot-writers.py` does not exist (`tools/` holds check-boot-chain.py and boot-chain-audit.sh). Recheck not run.
- Tools installed or updated: none.
- Answering model: anthropic/claude-haiku-5-5 (workstation context; not independently verified).

Scope: executed=none
