## Btrfs repair and maintenance decisions — round 31

These decision lines summarize btrfs-progs v7.1 documentation on shared extents and defragmentation, zero-log and checker repair, mount options, device replacement, and trim (`Defragmentation.rst:24-27`; `btrfs-rescue.rst:123-152`; `btrfs-check.rst:12-18,29-33`; `ch-mount-options.rst:33-43,89-101,131-159`; `btrfs-replace.rst:20-38`; `Trim.rst:12-43`). They state documented behavior, not a diagnosis of a particular host [inf] (`btrfs-check.rst:12-18,29-33`). Mori's runway row names `df -P` for the fleet root and `/tmp`, and its explicit boundary says “Never threshold the btrfs chunk percent”; this tsukuroi section records repair and maintenance decisions only and sets no runway threshold [inf] (`mori-shokunin/SKILL.md:19,415-418`).

| id | situation | decision | source |
|---|---|---|---|
