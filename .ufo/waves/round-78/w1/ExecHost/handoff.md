# ExecHost operator handoff

Each executed probe: rc 0; receipt UTC 2026-11-04T18:26:34Z (post-operation).
Exact commands and limitations are in report.md; retained evidence is in receipts/.
No machine-id names, journal basenames, or journal messages are included.

| Trigger | Action | Outcome | Operator handoff |
|---|---|---|---|
| Version grounding | pacman -Q systemd | systemd 262.1-1 | Package identity only; upstream source identity not proven. |
| Filesystem accounting | stat -f /var/log/journal | btrfs, 4096-byte blocks; available 186252614 blocks | Capacity snapshot, not a keep-free policy decision. |
| Journal usage | journalctl --disk-usage, user and sudo -n | Both 193.4M | Rounded outputs agree; scope equality not established. |
| File accounting | Python scandir/no-follow stat, immediate directories | 2 directories, 16 regular .journal files; allocated 202866688 B; apparent 268435456 B; ignored/error buckets zero | Aggregate only; no per-file uniformity or health claim. |
| Config recheck | systemd-analyze cat-config, exact five-directive output filter | Active SystemMaxUse=256M, RuntimeMaxUse=64M; remaining safe fields commented | On-disk settings only. Complete config transiently captured before filtering; see disclosed limitation. |
| Domain task completed | Preserve sanitized receipts and remove own scratch | No vacuum/rotate/flush/restart or package transaction performed | Accounting alone supplies no authorization to change retention. Any cleanup requires a separately authorized operator decision. |

No cleanup recommendation or daemon-health verdict follows from this snapshot.
The sudo metadata fallback was not needed and was not executed. Additional lane
bookkeeping and tool supervision behavior are disclosed in report.md.
