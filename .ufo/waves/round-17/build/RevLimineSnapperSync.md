# RevLimineSnapperSync — snapshot UKI provenance

**Contract [obs]**: snapper `create-snapshot-post` → `limine-snapper-sync --add <id>` (`/usr/lib/snapper/plugins/10-limine-snapper-sync:135-136,84-85`); watcher does the same on inotify CREATE (`/usr/bin/limine-snapper-watcher`); wrapper execs the core (`/usr/bin/limine-snapper-sync:248`).

**Mechanism [obs-src, inf-bin]**: core rebuilds snapshot kernel nodes from the live limine.conf (`LimineReader.java:124`), hashes the live ESP file, not snapshot content (`KernelReader.java:196-199`), naming it `fileName+"_sha256_"+sha256` (`:209`; `Hash.java:11`); `path:` becomes `<machine-id>/limine_history/<fileHashName>#<b2sum>` (`:210`; `ImageDetail.java:48-49`; `Config.java:12`). `historyAddSnapshot` byte-copies `/boot/EFI/Linux/*.efi` there, deduped by name (`SnapshotManager.java:226-238`). Src `https://gitlab.com/Zesko/limine-snapper-sync` tag 1.32.1, `SnapshotManager.java` L238 "Utility.copyFile(sourceFilePath, targetFilePath);" (accessed 2026-10-20).

**Yes [obs]**: `limine_history/…_sha256_2e9c…` mtime 09:29:18 and sha256 identical to `/boot/EFI/Linux/omarchy_linux.efi` (09:26:22) (`l1-capture/boot-chain-capture.txt:114-124,170-174,218-222`); entry #1's `0f1e…` (09:03:02) is VERSION 41.1 (`:117,202-207`). Future snapshots reuse that same copy.

**Divergences**: they inherit the 42.2 `/sysroot`-init vs `/new_root`-hook mismatch; a rebuilt UKI gets a new hash-name and never rewrites old entries (`SnapshotManager.java:183-192`). Only entry #1 (41.1) is consistent.

**Unverified**: 26.1MB core is non-UTF-8; source↔binary binding rests on package 1.32.1-2 + tag 1.32.1 [inf]. Confidence: high.

Scope: executed=none
