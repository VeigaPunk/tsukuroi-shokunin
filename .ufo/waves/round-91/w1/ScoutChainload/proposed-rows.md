# C2 candidate rows — chainload half (seat ScoutChainload, round 91 w1)

Scope: `corpus/knowledge/limine-unverified-image-r91.md` — what Limine v12.9.4's `chainload()` does
with an `efi` entry's `path:`/`image_path:` value, split by the shape of the value.

All quotes are verbatim from the pinned snapshot
`.ufo/waves/round-91/after/src-c2/limine-v12.9.4-common_{lib/uri.c,lib/config.c,protos/chainload.c}`
(byte-identical to clone `v12.9.4` HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c`, `cmp` = identical,
`sha256` as in `.ufo/waves/round-91/after/src-c2/SHA256SUMS`). Raw line numbers refer to those files.
`[src]` = stated by the pinned source, `[obs]` = read on this host this round, `[inf]` = inference.

## The split the entry must make (the two "unverified image line" shapes are not the same thing)

### CC1 — an `efi` entry's image line is read from the ENTRY BODY, not from the global config
- [src] `chainload()` takes the entry body as its `config` argument and reads `PATH` then `IMAGE_PATH`
  from it: `char *image_path = config_get_value(config, 0, "PATH");` (chainload.c 415) and
  `image_path = config_get_value(config, 0, "IMAGE_PATH");` (chainload.c 417). The body handed in is
  `selected_menu_entry->body` (menu.c 2349 → 2460), a private copy made at config.c 377-380.
- [src] `config_get_value(config, 0, ...)` returns the FIRST match of the key in that body
  (config.c 797-818: the key must start a line, the key text is matched case-insensitively, and
  `if (index--) continue;` makes index 0 the first hit).
- [inf] So whether a value is "the image line" is decided per entry body, and the global-section cut
  (V1) never changes which line of an entry body Limine reads. V1 governs only the keys read with
  `config == NULL` (menu.c 1711, 1720).

### CC2 — a value with NO URI shape is a boot-fatal panic of that entry
- [src] `uri_resolve()` returns false **without any message** for a value with no `(` (uri.c 48-49)
  or with a `(` but no `):/` (uri.c 61-62); `uri_open()` then returns NULL with no message
  (uri.c 335-336: `if (!uri_resolve(uri, &resource, &root, &path, &hash)) { return NULL; }`).
- [src] `chainload()` turns that NULL into a panic:
  `panic(true, "efi: Failed to open image with path `%s`. Is the path correct?", image_path);`
  (chainload.c 435).
- [src] `panic(true, …)` means `allow_menu` is set, so on UEFI (boot services still up) the screen
  shows `Press a key to return to menu.` (panic.s2.c 71-85); under measured boot `allow_menu` is
  cleared first and the machine prints `System halted.` (panic.s2.c 24-29, 93-99).
- [inf] The "no URI shape" value is therefore not an ignorable line: booting that entry panics and
  (without measured boot) drops back to the menu, where another entry can be chosen.

### CC3 — a value WITH URI shape but NO `#hash` opens and boots with no Limine-side integrity check
- [src] `uri_resolve()` succeeds for `boot():/EFI/BOOT/BOOTX64.EFI` and leaves `*hash == NULL`
  (uri.c 44 initialises all four to NULL; the hash loop at uri.c 77-104 only runs when a `#` exists).
  Measured with a verbatim transcription of uri.c 32-107:
  `boot():/EFI/BOOT/BOOTX64.EFI -> TRUE  resource="boot" root="" path="EFI/BOOT/BOOTX64.EFI" hash=(NULL)`
  (harness: `w1/ScoutChainload/urires.c`, copy under `w1/ScoutChainload/`).
- [src] With `hash == NULL` **no BLAKE2b comparison happens at all**: `hash_buf` is only filled under
  `if (hash != NULL)` (uri.c 378-381), the hashing filter is installed only under
  `} else if (hash != NULL) {` (uri.c 483-488), and the final comparison is guarded by
  `if (hash_fh != NULL && !blake2b_check_hash(hash_fh, hash_buf)` (uri.c 662-664).
- [src] `chainload()` itself performs no hash check; the only hash comparison in the whole path is the
  one inside `uri_open` (uri.c 663), driven by the `#hash` in the URI.
- [src] Under Secure Boot the signature check is the FIRMWARE's, not Limine's:
  `The firmware's LoadImage will verify the Secure Boot signature of the chainloaded EFI application`
  (chainload.c 423-425), and the image is handed over with `gBS->LoadImage(0, efi_image_handle,`
  (chainload.c 507).
- [inf] So an unhashed `path:` on an `efi` entry is a SILENT integrity gap, not a boot failure: the
  file is opened and executed without any digest check by Limine. With Secure Boot off, nothing checks
  it at all; with Secure Boot on, the firmware's LoadImage is the only check.

### CC4 — an `efi` image path needs NO hash even under Secure Boot (the rule is waived for this path)
- [src] `chainload()` saves and clears the flag around the open:
  `bool saved_secure_boot_active = secure_boot_active;` (chainload.c 426) / `secure_boot_active = false;`
  (chainload.c 427), restored at `secure_boot_active = saved_secure_boot_active;` (chainload.c 437).
- [src] The only gate on a missing hash is `if (secure_boot_active && hash == NULL) {` →
  `URI_ERROR("Secure Boot is active and URI `%#` has no associated hash!", uri);` (uri.c 372-375) —
  which cannot fire while the flag is cleared.
- [inf] Therefore the "Secure Boot requires a hash" error is reachable for `kernel_path`/`module_path`/
  `image_path` of the other protocols (their `uri_open` callers do not clear the flag) but is
  unreachable for an `efi` entry's own image path. Do not report "unhashed under Secure Boot panics"
  about the `efi` image line.

### CC5 — a `#hash` that is present but malformed is a DIFFERENT panic with a DIFFERENT message
- [src] `uri_resolve()` reaches `if (strlen(uri + i) != 128) {` → `URI_ERROR("Blake2b hash must be
  128 characters long");` (uri.c 89-91) and `URI_ERROR("Blake2b hash contains invalid character at
  position %d", …)` (uri.c 97-99). `URI_ERROR` panics for a non-optional resource (uri.c 21-27).
- [inf] A present-but-malformed hash therefore panics with "Blake2b hash must be 128 characters long",
  NOT with "efi: Failed to open image". The "no URI shape" case (CC2) is the only one that reaches
  chainload.c 435.

### CC6 — `unverified_image_lines` mixes a boot-fatal shape with a silent one; it is a reporting field
- [src] The r91 gate's U1 rule is a REPORTING contract: the value's line number is reported and no
  pin verdict, status, consequence or rc changes (battery r91 U1 text, tools/limine-pin-battery-r91.py
  116-127).
- [obs] Measured with the frozen r91 candidate gate (`d3b0987d:tools/check-limine-pins.py`, sha256
  679d4f0e62cb01f41aa7bab6f97b977da979670d16759f8ec7c82c24970ca94f) on fixtures:
  `path: plainname.efi` → `{"verdict":"HEALTHY","rc":0,"pins":[],"unverified_image_lines":[3]}`;
  `path: boot()plainname.efi` → same shape, `unverified_image_lines:[3]`.
- [obs] The host's own fallback image line is the *unhashed* shape, not the shape-less one:
  `.ufo/waves/round-91/before/host/receipt.txt` line 20 = `72:path: boot():/EFI/BOOT/BOOTX64.EFI`
  (37 characters, complete — the receipt's own per-line capture is cut at 140 columns, see CC9).
- [inf] An operator reading `unverified_image_lines` therefore cannot tell "this entry panics at boot"
  (CC2) from "this entry boots with no digest check" (CC3). The entry should say so; the gate must not
  change the verdict (U1 is frozen for this round).

### CC7 — a mismatch on the `efi` image line is decided by the GLOBAL `hash_mismatch_panic`, not by the entry's own
- [src] `hash_mismatch_panic` is read once, globally:
  `char *hash_mismatch_panic_str = config_get_value(NULL, 0, "HASH_MISMATCH_PANIC");` (menu.c 1711),
  i.e. with `config == NULL` → the global buffer that `init_config` cut (config.c 642-651).
- [src] The mismatch of an `efi` image is detected inside `uri_open` by
  `uri_hash_mismatch()` (uri.c 301-305), which consults that same global and panics via `URI_ERROR`;
  with `hash_mismatch_panic: no` it instead prints `WARNING: Blake2b hash for URI `%#` does not match!`
  and waits for a key (uri.c 307-317).
- [src] The global is also forced on under Secure Boot: `if (secure_boot_active) { hash_mismatch_panic =
  true; editor_enabled = false; }` (menu.c 1714-1717).
- [inf] A `hash_mismatch_panic: no` written INSIDE an `efi` entry body has no effect on that entry's own
  image mismatch — the same V1 visibility rule that governs `measured_boot` governs it here. This is the
  direct V1→C2 link and belongs in the entry.

### CC8 — `measured_boot` decides whether the CC2 panic halts or returns to the menu
- [src] `char *measured_boot_str = config_get_value(NULL, 0, "MEASURED_BOOT");` (menu.c 1720) — again
  the global, cut buffer only; forced true under Secure Boot (menu.c 1722-1724) and forced false when
  the firmware exposes no TPM/CC interface (menu.c 1726-1728).
- [src] `if (measured_boot) { allow_menu = false; }` (panic.s2.c 26-28) → `System halted.` instead of
  `Press a key to return to menu.`
- [obs] This host: `/sys/class/tpm/` is empty and the SecureBoot efivar data byte is `00` (off)
  (`.ufo/waves/round-91/before/host/receipt.txt` lines 5-7) → measured boot off, `on_panic menu`
  (receipt line 23).

### CC9 — the r91 host receipt's per-line capture is truncated at 140 columns; do not read "no `#`" from it
- [obs] In `.ufo/waves/round-91/before/host/receipt.txt` the six image-line excerpts are exactly 140
  characters long (lines 10, 12, 14, 16, 18) — the tail is cut. The visible `#` fragment of line 30 is
  93 hex characters and of line 38 is 89, of a required 128.
- [obs] The round-17 full capture of the SAME file shows lines 50/56/64 at 230 characters with a `#`
  and a 128-hex BLAKE2b pin at column ~160 — so those three lines DO carry pins; the receipt's cut hides
  them (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt` lines 143/147/153, registry S051).
- [inf] The only host image line that is genuinely unhashed is line 72 (`boot():/EFI/BOOT/BOOTX64.EFI`,
  37 characters, inside the receipt's cut). Any entry text asserting that lines 50/56/64 lack a `#`
  would be wrong; re-read them from a fresh read-only capture before claiming so.

### CC10 — where exactly the global section ends (config.c), for the entry's V1 cross-reference
- [src] `init_config()` builds the menu tree first (`menu_tree = create_menu_tree(NULL, 1, 0);`,
  config.c 640) and only then cuts the global buffer: `char *c = config_get_entry(&s, 0);` (config.c
  643), walk back to the entry header's `/` (config.c 645-647), `if (*c == '/' && c > config_addr) {
  c[-1] = 0; }` (config.c 648-650).
- [src] `config_get_entry()` recognises an entry header only by a `/` that starts a line
  (`if ((p - 1) != config_addr && *(p - 2) != '\n')` → config.c 700) and ends an entry body at the next
  line-starting `/` (`if (*p && *(p - 1) != '\n')` → config.c 714).
- [src] Because the cut is applied AFTER `create_menu_tree`, the per-entry bodies are already copied
  (config.c 377-380) and are unaffected; only reads with `config == NULL` see the truncated buffer.
- [inf] The guard `c > config_addr` is exactly the "first line is an entry line" exception: if the file
  begins with the entry header, `c == config_addr` and nothing is cut, so the whole file stays visible
  to `config_get_value(NULL, …)`. Verified with a verbatim transcription of config.c 527-552 + 642-651 +
  686-722 + 778-818 (`w1/ScoutChainload/cfgcut-harness.c`): a first-line `/+Omarchy` header leaves
  53 of 56 bytes visible and a `hash_mismatch_panic: no` AFTER the entry body is still found.

## Host value column (what to write in the "Host value (2026-11-07)" column)

| fact | host value | source of the fact |
|---|---|---|
| host `protocol: efi` lines | 29, 37, 49, 55, 63, 71 (six `efi` entries) | r91 receipt lines 9, 11, 13, 15, 17, 19 |
| host image lines | 30, 38, 50, 56, 64, 72 | same |
| the unhashed image line | `72:path: boot():/EFI/BOOT/BOOTX64.EFI` | r91 receipt line 20 (complete, 37 chars) |
| the entry that line belongs to | `/EFI fallback` (r17 capture line 67) | S051 boot-chain-capture.txt:155 |
| Secure Boot | off (efivar data byte `00`) | r91 receipt lines 6-7 |
| TPM | none (`/sys/class/tpm/` empty) | r91 receipt line 5 |
| `hash_mismatch_panic` | `no` at conf line 8 → global section (before the first entry line) → mismatch PROMPTS | r89 receipt line 3 (own-work prior capture) + r17 capture line 21 shows the first entry header is line 21 |
| `measured_boot` | absent → measured boot off → a panic returns to the menu | r89 receipt lines 3-9 (no measured_boot line) |
| receipt line-width caveat | image-line excerpts cut at 140 columns (see CC9) | r91 receipt lines 10-18 |
