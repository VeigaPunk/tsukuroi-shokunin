# C2 candidate SOURCES rows — seat ScoutChainload, round 91 w1

One draft row per source opened for the chainload half of
`corpus/knowledge/limine-unverified-image-r91.md`. Ids are TBD for the L1 to assign; the three
pinned Limine sources already have registry rows S374 (uri.c), S375 (chainload.c) and S376
(config.c) at `corpus/SOURCES.md:385-387`, so those three are marked "already registered — anchor
extension proposed" rather than re-proposed. Everything else is a new row.

## Already registered — anchor/extension proposals

### S375 (Limine v12.9.4 `common/protos/chainload.c`) — extend the anchor set
- **Existing**: tag v12.9.4 (clone HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c`), raw lines
  414-421 (PATH then IMAGE_PATH), 423-427 and 437 (secure_boot_active cleared around uri_open),
  430-435 (NULL -> panic Failed to open image); pinned snapshot
  `.ufo/waves/round-91/after/src-c2/limine-v12.9.4-common_protos_chainload.c`
  sha256 `316eb17df996f91252791b1351e8f88c027ceeb8535becc1a247d614d8b5e1a7`.
- **Proposed anchor addition**: raw line 507 (`gBS->LoadImage(0, efi_image_handle,`) — the firmware
  call that actually verifies the Secure Boot signature of the chainloaded application, and raw lines
  511 / 520 / 545 (`panic(false, "efi: LoadImage failure (%X)" …)`, the three non-menu panics of the
  efi chainload path, `allow_menu == false` → `System halted.`).
- **Proposed "teaches" addition**: an `efi` entry's image path is read from the ENTRY BODY
  (`config_get_value(config, 0, "PATH")`, 415; `IMAGE_PATH`, 417 — index 0 = first match), the body
  being `selected_menu_entry->body` (menu.c 2349 → 2460), a private copy (config.c 377-380); and
  `chainload()` itself performs NO hash check — the only comparison is inside `uri_open`
  (uri.c 663), so a `#`-less value is never digest-checked by Limine.

### S374 (Limine v12.9.4 `common/lib/uri.c`) — extend the anchor set
- **Existing**: tag v12.9.4, raw lines 32-107 (uri_resolve: resource/root/path/hash split, return
  false without a message at 49, 62, 74, 91, 99), 335-336 (uri_open: uri_resolve false -> return
  NULL), 372-376 (secure_boot_active && hash == NULL -> URI_ERROR); pinned snapshot
  `.ufo/waves/round-91/after/src-c2/limine-v12.9.4-common_lib_uri.c`
  sha256 `e06cac1212fec55150c109843e22dfe01cd618d4e81235e357d9a256e2a2ed6f`.
- **Proposed anchor addition**: raw lines 378-381 (`hash_buf` filled only `if (hash != NULL)`),
  483-488 (`} else if (hash != NULL) { hash_fh = blake2b_open(top); …`), 662-664
  (`if (hash_fh != NULL && !blake2b_check_hash(hash_fh, hash_buf) && !uri_hash_mismatch(uri))`),
  301-317 (`uri_hash_mismatch`: panic vs the Y-prompt), 21-27 (`URI_ERROR` panics for a
  non-optional resource).
- **Proposed "teaches" addition**: with `hash == NULL` (a URI-shaped value with no `#`) NO BLAKE2b
  comparison happens at all — `hash_buf` is never filled, no hashing filter is installed, and the
  final check is skipped; the file is opened and its bytes used as-is.

### S376 (Limine v12.9.4 `common/lib/config.c`) — extend the anchor set
- **Existing**: tag v12.9.4, raw lines 642-650 (init_config: cut buffer at newline before first
  entry line, guard `c > config_addr` skips cut when first line is entry), 686-720 (config_get_entry:
  entry body boundaries), 778-818 (config_get_value: first matching key wins); pinned snapshot
  `.ufo/waves/round-91/after/src-c2/limine-v12.9.4-common_lib_config.c`
  sha256 `aafc9c410a250efc9674e3c93e839d32ae2731ba2ca60bb7f5edd7ad5828fba8`.
- **Proposed anchor addition**: raw line 640 (`menu_tree = create_menu_tree(NULL, 1, 0);`) — the
  menu tree (and hence the per-entry body copies at 377-380) is built BEFORE the global cut at
  642-650, which is why the cut reaches only `config_get_value(NULL, …)` reads; raw line 700
  (an entry header is a `/` that starts a line) and raw line 714 (an entry body ends at the next
  line-starting `/`).
- **Proposed "teaches" addition**: `init_config` strips CR and leading blanks from every line
  (raw 527-552) BEFORE the cut, so a `path:` line that was indented in the file is at column 0 in
  the buffer `config_get_value` scans, and a key inside an entry body is at column 0 of that body
  too — the V1 cut is about WHICH LINES the global scan can reach, not about indentation.

## New rows proposed by this seat

### TBD-A — Limine v12.9.4 `common/menu.c` (the global reads and the protocol dispatch)
- **URL**: https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/menu.c
- **kind**: code · **tier**: A
- **anchor**: tag v12.9.4 (clone HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c`), raw lines 1711-1717
  (`hash_mismatch_panic` read with `config == NULL`; forced true under Secure Boot), 1719-1728
  (`measured_boot` read with `config == NULL`; forced true under Secure Boot; forced false without a
  TPM/CC interface), 2429 (`char *proto = config_get_value(config, 0, "PROTOCOL");`), 2456-2460
  (`efi_chainload` / `efi` / `uefi` -> `chainload(config, cmdline)`), 2349
  (`boot(selected_menu_entry->body);` — the entry body handed to `boot`), 2468
  (`panic(true, "Unsupported protocol specified.");`).
- **teaches**: the two keys C2's entry needs — `hash_mismatch_panic` and `measured_boot` — are read
  from the GLOBAL buffer only (`config == NULL`), so the V1 cut decides their value; and an `efi`
  entry's own body is what `chainload` reads `PATH`/`IMAGE_PATH` from, so the body is unaffected by
  that cut. This row is the source of the CC7/CC8 rows.
- **note**: `common/menu.c` is already registered as S353 (raw 1711-1717, 1719-1730) and pinned at
  `.ufo/waves/round-91/before/src/limine-v12.9.4-common_menu.c`
  sha256 `628001e88564525f8d1e0e6193ea86145e5613eaea97c04110545cd182168f95`. **Recommend extending
  S353's anchor with 2429, 2456-2460, 2349, 2468 instead of registering a new row** — the L1 decides.

### TBD-B — Limine v12.9.4 `common/lib/panic.s2.c` (what a panic does on screen)
- **URL**: https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/panic.s2.c
- **kind**: code · **tier**: A
- **anchor**: tag v12.9.4, raw lines 18 (`noreturn void panic(bool allow_menu, const char *fmt, ...)`),
  23-29 (under measured boot `allow_menu` is cleared), 71-85 (`Press a key to return to menu.` then
  `menu(false)`; UEFI requires `efi_boot_services_exited == false`), 93-99 (`System halted.`).
- **teaches**: the difference the C2 entry must draw between the two `efi` image-line failure
  shapes — `chainload.c 435` panics with `allow_menu == true` (menu return), while the LoadImage
  failure at chainload.c 511 panics with `allow_menu == false` (`System halted.`); and that measured
  boot turns the first into a halt as well (panic.s2.c 26-28).
- **note**: already registered as S362 (raw 18-29, 70-100) and pinned at
  `.ufo/waves/round-91/before/src/limine-v12.9.4-common_lib_panic.s2.c`
  sha256 `0233d557db8fdf96918350a305cde91a8a4aca33216d2ac8c712cf47c79a3ff1`. **Recommend extending
  S362's anchor (add 71-85 and 93-99 as separate anchors, and the `allow_menu` distinction) rather
  than a new row.**

### TBD-C — Limine v12.9.4 upstream tag / clone provenance (own-work)
- **URL**: https://github.com/limine-bootloader/limine (tag `v12.9.4`)
- **kind**: code (repository) · **tier**: A
- **anchor**: `git clone --depth 1 --branch v12.9.4` → HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c`,
  commit subject `docs/ChangeLog: Update for 12.9.4`; `cmp` of the clone's
  `common/protos/chainload.c`, `common/lib/config.c`, `common/lib/uri.c`, `common/menu.c`,
  `common/lib/panic.s2.c` against `.ufo/waves/round-91/after/src-c2/` and
  `.ufo/waves/round-91/before/src/` → byte-identical.
- **teaches**: the pinned snapshot used for every C2 row is the upstream v12.9.4 tree, not a local
  modification — the provenance check behind "verified byte-identical to the clone".
- **note**: the clone HEAD is already cited inside S361/S374/S375/S376. If the L1 wants the clone step
  itself as a row, it can reuse that shape; I mark it TBD rather than proposing a duplicate.

### TBD-D — round-91 read-only host receipt (own-work)
- **path**: `.ufo/waves/round-91/before/host/receipt.txt`
- **kind**: own-work · **tier**: A
- **anchor**: lines 2-3 (`pacman -Q limine` → `limine 12.9.4-1`), 4-5 (`/sys/class/tpm/` empty),
  6-7 (SecureBoot efivar: attr `06`, data byte `00` = off), 9-20 (the six `protocol: efi` lines and
  their six image lines; **each image-line excerpt is cut at 140 columns**), 23 (the r91 gate summary
  `verdict DEGRADED rc 1 on_panic menu findings ['LP-MISMATCH line 30', 'LP-MISMATCH line 38']`).
- **teaches**: the host values for the C2 entry: six `efi` entries, one of whose image lines
  (72) carries no `#` hash at all; Secure Boot off; no TPM. Plus the caveat that the per-line
  capture is truncated (CC9): the visible `#` fragments are 93 and 89 hex chars of a required 128,
  and the cut hides the `#` of lines 50/56/64 entirely.
- **note**: the receipt is an own-work artefact; the L1 may fold it into the existing own-work row
  pattern (S363/S371 style) rather than minting a new id.

### TBD-E — round-17 boot-chain capture (own-work, prior round) — needed only to disprove CC9
- **path**: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt`
- **kind**: own-work · **tier**: A
- **anchor**: line 155 (`67:/EFI fallback` — the entry line 72 belongs to), line 156
  (`72:path: boot():/EFI/BOOT/BOOTX64.EFI`), lines 143/147/153 (lines 50/56/64 at their FULL 230
  characters, each with a `#` and a 128-hex BLAKE2b pin at column ~160), line 21
  (`21:/+Omarchy` — the first entry header, so the global section is lines 1-20).
- **teaches**: the counter-evidence for CC9 — the r91 receipt's 140-column cut makes lines 50/56/64
  look unpinned, and only this fuller capture shows they are pinned; and it fixes where the host's
  global section ends (first entry header at line 21), which is what makes `hash_mismatch_panic: no`
  at line 8 a GLOBAL value.
- **note**: already registered as S051. **Recommend citing S051 rather than minting a new row.**

## Registry arithmetic

Existing rows reused/extended: S351 (uri.c), S353 (menu.c), S361 (chainload.c), S362 (panic.s2.c),
S363/S371 (host receipts, own-work), S051 (boot-chain capture, own-work). Existing rows whose
anchors need the round-91 additions: S374, S375, S376 (all at `corpus/SOURCES.md:385-387`).
New rows proposed: 1 (`common/menu.c` dispatch anchors) IF the L1 prefers a new row over extending
S353; 0–1 others, all of which duplicate existing rows under a different id and are therefore
recommended as anchor extensions instead.
