# Limine path pins: who writes them, when they are recomputed, how a stale pin spreads (round 88)

source: S355 (limine-entry-tool 1.40.0 LimineManager.java), S356 (ConfigReader.java + Config.java), S357 (Utility.java), S358 (limine-update + 89-warn-missing-file-hashes + limine-entry-tool.conf), S359 (limine-snapper-sync 1.32.1 KernelReader.java + Limine.java + Hash.java + Config.java); all `mined`; Gate in `corpus/lessons/round-88.md`
recheck: `sudo python3 tools/check-limine-pins.py --live` and the source re-open below, cadence 30d and on any limine-mkinitcpio-hook / limine-snapper-sync update, UKI rebuild or `/boot` incident
verified-at: 2026-11-06
host capture: `.ufo/waves/round-88/before/host/receipt.txt` (2026-11-06T20:53:03-03:00, read-only; `/boot` b2sum list identical before and after)
machine-readable rows: `corpus/knowledge/limine-pin-writers-r88.json`
snapshots: `.ufo/waves/round-88/before/src/` (`URLS.txt`, `SHA256SUMS`; tags 1.40.0 and 1.32.1); the host runs limine-mkinitcpio-hook 1.40.0-2 and limine-snapper-sync 1.32.1-2
companion: `corpus/knowledge/limine-pin-plane-r87.md` (how Limine reads a pin; this entry is the writer side)

## What this plane answers

`limine-pin-plane-r87.md` says how Limine reads a `#<128 hex>` pin and what a mismatch does at boot; its Limits
left the writer side unopened ("The repair command of the host's limine-entry-tool hook was not opened"). This
entry answers four operator questions from the writers' own source at the installed tags: which component writes
a pin and under which setting, how it computes the hash, which command recomputes the main-entry pins, and what
limine-snapper-sync does with a main entry's pin when it adds a snapshot entry. That last answer decides whether
the round-86 incident (both UKIs rewritten in place, main pins on lines 30 and 38 stale) stays on two lines or
spreads into new snapshot entries.

## Rows

Quotes are verbatim from the pinned snapshot; raw line numbers refer to the pinned files. `[obs]` = read on this
host this round; `[src]` = stated by the pinned source; `[inf]` = inference from the source, not executed here.

| Row | Statement | Source, raw lines | Quote (≤25 words) | Host value (2026-11-06) |
|---|---|---|---|---|
| PW1 | [src] limine-entry-tool reads its settings in four layers, lowest priority first: `/usr/share/limine-entry-tool.d/`, `/etc/limine-entry-tool.conf`, `/etc/limine-entry-tool.d/`, then `/etc/default/limine` (highest). | S356 ConfigReader.java 28-32 | "loadConfigFile(Config.DEFAULT_CONFIG_FILE_PATH); // 4. Highest priority" | [obs] `/etc/limine-entry-tool.conf:84` `ENABLE_VERIFICATION=yes` (byte-identical to the 1.40.0 package file, sha256 `44207b64…`); `/etc/default/limine` sets no `ENABLE_VERIFICATION`; `/etc/limine-entry-tool.d/` holds only `resume.conf`; `/usr/share/limine-entry-tool.d/` absent |
| PW2 | [src] Pins are written only when `ENABLE_VERIFICATION` is `yes` (case-insensitive) AND the `b2sum` command exists; otherwise the tool writes the path with no `#` at all. The default is off. | S356 ConfigReader.java 173-177, Config.java 7, 19 | "Config.ENABLE_VERIFICATION = Utility.isCommandPresent(Config.HASH_COMMAND) && \"yes\".equalsIgnoreCase(enableVerification);" | [obs] effective `yes` (PW1); `b2sum` is `/usr/bin/b2sum` (coreutils 9.12-2) |
| PW3 | [src] The pin is appended to the `path:` line of a UKI entry and to every `module_path:` and the `path:` of a kernel+initramfs entry; `cmdline:` and `comment:` lines never get one. | S355 LimineManager.java 325, 329, 331, 353, 359-372 | "bootConfig.add(Config.SPACES + Limine.PATH + \" \" + config.pathFunction() + ukiEspPath + this.b2sum(ukiFullPath));" | [obs] both main entries are UKIs; only their `path:` lines carry pins (lines 30, 38) |
| PW4 | [src] The hash is the `b2sum` command's output (BLAKE2b-512, matching Limine's 128-hex rule), computed twice in parallel; on disagreement it retries, and after the last retry it logs "Hardware is faulty" and still returns the first result. | S357 Utility.java 118-175; S356 Config.java 7 | "CompletableFuture<String> hashFuture1 = CompletableFuture.supplyAsync(() -> blake2sum(absoluteFilePath));" | — |
| PW5 | [src] The packaged repair command is `limine-update`: it runs `limine-install --no-efi-register` and then `limine-mkinitcpio` with the caller's arguments, which is the path that re-adds entries and so rewrites their pins from the files as they are then. limine-entry-tool 1.40.0 has no hash-only refresh option (its `Main.java` options are add/remove/scan/tree/cmdline). | S358 limine-update 16-28; S355 LimineManager.java 353 | "limine-mkinitcpio \"$@\"" | [obs] installed `/usr/bin/limine-update` sha256 `55b7d578…` = the 1.40.0 file |
| PW6 | [src] limine-snapper-sync builds a snapshot entry from the main entry's `path:` line: it cuts the first `#hex` run off that line and appends that same text to the history-file path it writes. It never recomputes the BLAKE2b. | S359 KernelReader.java 154-157, 175-179, 196-213; Limine.java 28 | "String snapshotPathValue = Utility.buildPath(config.machineID(), Config.HISTORY_FOLDER, fileHashName + blake2sum);" | [obs] existing history pins (lines 50, 56, 64) date from 2026-10-20, before the incident; r87 read them OK |
| PW7 | [src] The history file is named after the current file's content hash (`HASH_FUNCTION`, default SHA-256), computed fresh at sync time. Its integrity check compares that name suffix with the content, never the `#` pin. | S359 KernelReader.java 196-209; Hash.java 60-66; Config.java 46 | "return !hashedFilePath.endsWith(hashSum);  // true = corrupted" | [obs] history names end `_sha256_<64 hex>` |
| PW8 | [inf] Consequence on this host: until the main pins are recomputed (PW5), every snapshot entry limine-snapper-sync adds for `linux` or `linux-lts` carries the stale main pin (`b990d8c6…`/`a68c281d…`, PW6) next to a history copy of the rewritten UKI (`57f5eb94…`/`eff78d32…`, PW7), so it reads `LP-MISMATCH` (`prompt` under `hash_mismatch_panic: no`). The stale pin spreads with each new snapshot; the hourly "Updated" runs leave the main pins as they are. Not executed: no snapshot was created this round. | PW6, PW7; r87 LP5/LP8 | — | [obs] journal: limine-snapper-sync "Updated: /boot/limine.conf" at 19:27:27 and 20:27:30; main pins unchanged at 20:53 (lines 30/38 still `b990d8c6…`/`a68c281d…`) |
| PW9 | [src] The hook that warns about missing hashes fires only when Secure Boot is on, config enrollment is on, verification is off and UKIs are off; with UKIs on, as here, no such warning is shown. | S358 89-warn-missing-file-hashes 19-25 | "Limine v12 requires verification hashes for all loaded files except EFI chainload." | [obs] `/etc/default/limine:8` `ENABLE_UKI=yes` |

## Operator actions

1. Read-only check first (r87): `sudo python3 tools/check-limine-pins.py --live`. rc 1 with lines 30 and 38
   `LP-MISMATCH` is the incident state; any further `LP-MISMATCH` on a snapshot line is PW8 happening.
2. Repair the source of the spread, not the copies: recompute the main pins with `sudo limine-update` (PW5). It
   re-adds the entries from the UKIs as they are then, so it accepts the rewritten UKI bytes (PE header changed,
   payload unchanged per r86's control copy) as trusted, and it also runs `limine-install --no-efi-register`.
   The alternative of hand-editing the pins accepts the same bytes. Either way, the trust decision is the
   operator's (L0 `tsukuroi | round-86 | HOST INCIDENT`).
3. After the repair, snapshot entries created between the incident and the repair keep their stale copied pins
   (PW6 copies text, it never recomputes). Re-run step 1 and list them. Re-creating or removing those snapshot
   entries is a separate operator decision.
4. Keep `ENABLE_VERIFICATION=yes` effective (PW1/PW2): turning it off makes the next rewrite drop every pin
   silently, which hides an in-place write instead of showing it.

## Limits

- PW8 is an inference from source; no snapshot was created on this host this round (that would be a host write).
- The body of `limine-mkinitcpio` and `limine-install` was not opened; PW5 rests on `limine-update` calling them
  and on LimineManager writing the pin when an entry is (re-)added.
- `HASH_FUNCTION` overrides in `/etc/default/limine` (PW7) were not set on this host; other values (`blake3`,
  `xxhash`) change only the history file name, not the copied `#` pin.
- The upstream sources are tag 1.40.0 and 1.32.1; the installed builds are native binaries, compared here only by
  the packaged script and config bytes (PW1, PW5), not by binary provenance.
