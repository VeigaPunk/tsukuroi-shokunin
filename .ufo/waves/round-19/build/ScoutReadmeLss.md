# ScoutReadmeLss — packaged-doc sync statements (C2)

README 1.32.1-2, captured `host-capture-r19b.txt:13-970`; quotes verbatim.

1. `:23` "synchronizing snapshot boot entries with Btrfs snapshots and updating the bootloader configuration accordingly" — [obs] sync program, not snapper, rewrites boot config.
2. `:66` "Automatically updates snapshot boot entries in real time without scanning all subvolumes or snapshots" — [obs] incremental/event-driven; no periodic scan documented.
3. `:849` "Snapper plugin integration for snapshot create, modify, delete, and rollback events" — [obs] plugin is the event channel; cleanup deletes reach sync.
4. `:852` "Debounce mechanism to group multiple snapshot deletions/modifications into a single sync" — [obs] delete bursts coalesce; invocations ≠ writes.
5. `:882` "MAX_SNAPSHOT_ENTRIES=auto to auto-remove older snapshot boot entries based on boot partition usage limit" — [obs] limit pruning inside a sync, same write path.
6. `:888` "Two ways to monitor snapshot changes: `limine-snapper-watcher` or Snapper plugin integration" — [obs] alternatives, not additive.

`:861` (deleted snapshots remove entries) reinforces #3.

Absences:
- [obs] README never mentions `snapper-cleanup.service` or `limine_history` (grep `:13-970` empty); `cleanup` only `:892`, `:904`, `:951`. Journal `limine_history` copies at `:1635-1637`, "Updated: /boot/limine.conf" `:1638`.
- [inf] Cleanup path: delete snapshot → `delete-snapshot-post` → `--debounce` sync → limine.conf write; watcher skips on `/run/limine-snapper-cleanup.lock` (`:1373-1374`).
- [unk] README states no service periodicity/activation; unit file needed.

Proposed SOURCES row (planner assigns id, next free S066): own-work packaged doc `/usr/share/doc/limine-snapper-sync/README.md`, capture `:13-970`, supporting C2 writer attribution.

Scope: executed=none
