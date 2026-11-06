# Limine path pins: grammar, hashing, mismatch consequence (round 87)

source: S350 (Limine v12.9.4 CONFIG.md), S351 (common/lib/uri.c), S352 (common/lib/config.c), S353 (common/menu.c), S354 (binutils objcopy manual); all `mined`; Gate in `corpus/lessons/round-87.md`
recheck: `sudo python3 tools/check-limine-pins.py --live` and `python3 tools/check-limine-pins.py --selftest`, cadence 30d and on any limine package update, kernel/UKI rebuild or `/boot` incident
verified-at: 2026-11-06
host capture: `.ufo/waves/round-87/before/host/receipt.txt` (2026-11-06T19:04:43-03:00, read-only); live gate run `.ufo/waves/round-87/after/live-receipt.txt` (2026-11-06T19:13:00-03:00, `/boot` b2sum list identical before and after)
machine-readable rows: `corpus/knowledge/limine-pin-plane-r87.json`
gate: `tools/check-limine-pins.py` (round-87 C1); battery `tools/limine-pin-battery-r87.py`
snapshots: `.ufo/waves/round-87/before/src/` (tag v12.9.4, `SHA256SUMS`); the host runs limine 12.9.4-1

## What this plane answers

`/boot/limine.conf` on this host pins each UKI with `#<128 hex>` after its path. The lane's boot gates
(`check-boot-chain.py`, `check-boot-writers.py`) compare committed captures and a stored hash prefix; none of them
hashes the file a pin names. This plane says how Limine reads a pin, what it hashes, and what happens at boot when
the bytes no longer match. That is the state the round-86 incident left behind (`objcopy` rewrote both UKIs in
place, `corpus/lessons/round-86.md` M3).

## Rows

Quotes are verbatim from the pinned snapshot (whitespace-normalized joins of consecutive lines; `…` marks skipped
lines). Raw line numbers refer to the pinned files.

| Row | Statement | Source, raw lines | Quote (≤25 words) | Host value (2026-11-06) |
|---|---|---|---|---|
| LP1 | A config key is matched case-insensitively and only at the start of a line, directly followed by `:`. Leading and trailing blanks and CRs are stripped first. A `#` line therefore never holds a key. | S352 527-551, 798-799 | "if (!strncasecmp(&config[i], key, key_len) && config[i + key_len] == ':') { if (i && config[i - 1] != SEPARATOR)" | keys are lower-case, indented by 2 or 5 spaces |
| LP2 | The keys that take a path are `path` and its aliases `kernel_path`/`image_path`, plus `module_path`, `dtb_path`, `global_dtb`, `wallpaper` and `term_font`. A `#...` inside `cmdline` or `comment` is not a pin. | S350 111-113, 134, 210, 267-268, 272-274, 295-308, 330-350; S351 28-32 | "`kernel_path` - Alias of `path`." | only `path:` lines carry pins |
| LP3 | The hash is everything after the **last** `#` of the URI, so a `#` inside a file name is part of the path. It must be exactly 128 hex characters, in either case; anything else is a URI error. | S351 78-101 | "for (int i = (int)strlen(uri) - 1; i >= 0; i--) { … if (strlen(uri + i) != 128) {" | 5 pins, all 128 lower-case hex |
| LP4 | The hash is BLAKE2b-512 over the file as stored on the partition. For a gzip (`$`) resource it covers the compressed bytes and is checked before decompression. | S350 446-447, 456-462; S351 344, 403-470 | "the hash covers the whole file as stored on disk (its compressed bytes, including anything after the gzip data)" | no `$` resource |
| LP5 | On a mismatch Limine panics unless `hash_mismatch_panic` is `no` (case-insensitive). The value is read from the first occurrence in the file. With `no`, it prints a warning and waits: `Y` (or `y`) boots the file anyway, and any other key returns to the menu. | S353 1711-1712; S351 301-312; S352 798-802 | "hash_mismatch_panic = hash_mismatch_panic_str == NULL \|\| strcasecmp(hash_mismatch_panic_str, \"no\") != 0;" | line 8 `hash_mismatch_panic: no` → prompt |
| LP6 | Secure Boot with an enrolled config hash forces panic and turns off the editor. Without an enrolled hash, Limine treats Secure Boot as inactive. A wallpaper or font that fails is skipped (optional resource), in either mode. | S353 1714-1717; S350 152-156, 451-455; S351 18-26, 302, 696-702 | "Forced to `yes` when Secure Boot is active and a config hash is enrolled." | SecureBoot efivar data byte 0 (off) |
| LP7 | `objcopy` given only an input file rewrites that file. Even `--dump-section`, which only reads a section out, rewrites the UKI it reads, and the BLAKE2b of the whole file changes. Probe with an explicit output file, or not as root on `/boot` at all. | S354 section `infile outfile` (raw HTML lines 188-191 and 634 of the pinned snapshot) | "If you do not specify outfile, objcopy creates a temporary file and destructively renames the result with the name of infile." | r86 ScoutHost 18:11:22 rewrote both UKIs (5 PE header bytes each) |
| LP8 | This host's state: both kernel entries (`linux`, `linux-lts`, lines 30 and 38) MISMATCH. Next boot of either shows the Y/any-key prompt, not a panic. The three snapshot-history pins (lines 50, 56, 64) are OK and boot without a prompt. The fallback `/EFI/BOOT/BOOTX64.EFI` has no pin. | gate `--live` (this round) | "LP-MISMATCH line 30", "LP-MISMATCH line 38" | `57f5eb94…` vs pin `b990d8c6…`; `eff78d32…` vs pin `a68c281d…` |

## Operator actions

1. Read-only check first: `sudo python3 tools/check-limine-pins.py --live`. rc 1 lists every mismatched pin, its
   entry name and its consequence (`prompt`, `panic`, `skip`).
2. On this host, until it is repaired: when the warning appears at boot, `Y` boots the main entry anyway. A
   snapshot entry boots without a prompt, but it boots an older kernel (LP8).
3. Repair is operator-owned: either regenerate the UKIs and their pins with the host's limine-entry-tool hook
   (the hook that wrote the pins, S075), or replace each pin with the current BLAKE2b of the file
   (`b2sum`). Choosing the second accepts the rewritten bytes as trusted. Re-run step 1: it must read rc 0.
   This plane does not name the hook command (not opened this round; see Limits).
4. Never point `objcopy` at a `/boot` file without an explicit output file (LP7). Before and after any `sudo` probe,
   record `find /boot -type f -print0 | sort -z | xargs -0 b2sum` and `cmp` the two lists (QUALITY 124).

## Limits

- Not modelled by the gate: macro expansion (`${NAME}`); Secure Boot's rule that every unhashed path panics
  (S350 451-455); what a missing file does under each protocol; a `cmdline` value that is itself URI-shaped.
- An enrolled config hash cannot be seen from Linux userspace by the gate. `--live` reads Secure Boot as enforced
  whenever the efivar says it is on (the stricter reading).
- Limine trunk (after v12.9.4) also accepts BLAKE3 pins, told apart by length: trunk `CONFIG.md` raw 446-450 and
  `common/lib/uri.c` raw 92 ("Hash must be 64 BLAKE3, 128 BLAKE2b, or 256 BLAKE3 characters long"), opened
  2026-11-06 and kept as context only in `.ufo/waves/round-87/after/src-trunk/` (rejected as a source for this host,
  lesson Gate). v12.9.4 accepts only 128 hex characters (S351 89-91). Re-pin on a limine upgrade.
- The gate reads a pin whose path leaves the `--esp` root (`..` components or a symlink pointing outside) as
  `LP-UNRESOLVED` rc 2 and never hashes the outside file (hardening at landing, wave seat ReviewGate; not a Limine
  rule taken from a source).
- The repair command of the host's limine-entry-tool hook was not opened this round.
