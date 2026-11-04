## Round-72 entry — the modprobe configuration plane enters Core

Append-only; the round-70 and round-71 sections above stay as written. This is a **new area**: the
held-ground sweep at the declaration base `a7015d27` read **0** file hits for `softdep`,
`MODPROBE_OPTIONS`, `showconfig`, `APPLY_BLACKLIST`, `conf_files_insert_sorted` and `lexicographic`
across `corpus/knowledge`, its only `modprobe.d` token hit was the r71 note's MP5 host line (paths only),
and the three `config-plane` filename matches were the Windows planes, not this surface. The entry is
`corpus/knowledge/modprobe-config-plane-r72.md`, rows MD1-MD6, sourced S301-S303 (`man/modprobe.d.5.scd`,
`libkmod/libkmod-config.c`, `tools/modprobe.c` at kmod v34; the host runs kmod 34.2).

**Core now — the reading:** the configuration directories the manual lists in SYNOPSIS
(`/etc/modprobe.d`, `/run/modprobe.d`, `/usr/local/lib/modprobe.d`, `/usr/lib/modprobe.d`,
`/lib/modprobe.d` — the `@SYSCONFDIR@` and `@DISTCONFDIR@` entries resolving to the first and fourth on
this host) are read in that precedence order, and once a file of a given name is loaded any file of the
same name in a later directory is ignored (MD1). Files from every directory are processed in one
lexicographic order, so a configuration file is completely replaced by a higher-priority file of the same
name or partially replaced by a file ordered later (MD2). libkmod inserts configuration filenames into one
sorted list and rejects a second file of the same name at insertion, so a duplicate name is parsed once
(MD3). `/proc/cmdline` is parsed into the same configuration object after the files (MD4). `-n/--dry-run`
executes nothing (MD5). `blacklist` suppresses a module's internal aliases only, and
`--use-blacklist` adds the unconditional probe flag (MD6). The host shape this reading is grounded on:
`/etc/modprobe.d` holds 3 names, `/usr/lib/modprobe.d` 5 names (`README` plus four `.conf`),
`/run/modprobe.d` and `/usr/local/lib/modprobe.d` are absent, `/lib` resolves to `/usr/lib` so
`/lib/modprobe.d` and `/usr/lib/modprobe.d` are one directory behind two SYNOPSIS entries, and
`/proc/cmdline` carries no `module.parameter` token.

**Operator-owned:** editing, creating or removing any file in any `modprobe.d` directory; changing a
blacklist; setting `MODPROBE_OPTIONS`; loading or unloading a module; and running `modprobe` at all,
including `-n`, `-c/--showconfig` and `-r`. The lane reads and records directory paths, modes, filenames
and the documented order; it never opens a configuration fragment's contents, never executes `modprobe`,
and never writes a fragment.

**Not claimed:** no configuration-content reading on this host — the effective line set of any module is
not stated from host bytes, and the precedence and merge are kmod's documented order (MD1-MD4), not a
measured resolution of this host's fragments; no module internals and no binary reverse engineering —
that ground stays with the sibling lanes the adjacency table names; no claim that a blacklist refusal
happened (no blacklist token appears on `/proc/cmdline` and the fragments are unread); no claim about
`install`, `remove`, `softdep` or `weakdep` command semantics beyond the manual's documented shape;
`MODPROBE_OPTIONS` is named as the documented route that can alter the directory list, not measured here.
**Mori's, unchanged:** nothing about capacity or fleet runway is stated here.

Counted by `python3 tools/count-md-rows-r72.py --revision <REV>` (frozen; sha256
`d615c653f32a29af3a4355d882041b8543ff56882b3225f7e3eedf173d8706a6`) with target `MD_ROWS=6 MD_VERIFIED=6
MD_SOURCES=3 MD_SNAPSHOTS=3 MD_MALFORMED=0` and `met=1`, at the revision named in `SCORECARD.md`
"Round 72 — measured outcome".
