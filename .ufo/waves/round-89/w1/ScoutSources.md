# ScoutSources — round-89 wave w1 — seat report

Seat: ScoutSources (scout). Scope: re-open the C2 entry's sources live and close the entry's
Limits; report freshness against upstream Limine.

Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`
→ `665408cc45a88ed49717e22f4593e8e6152ac665` (exit 0).
Candidate commit under test: `81f68d0053213400a5495b5fb5722c4dcb1cfc53` (entry
`corpus/knowledge/limine-uri-failure-r89.md`, `.json` rows UF1-UF8).

**No lane file was edited.** Everything this seat wrote is under
`.ufo/waves/round-89/w1/ScoutSources/` (this report's sibling directory) plus this report.

## 1. Verdict per check

| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | Clone `v12.9.4` at the tag, record HEAD | **pass** | HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c` — matches the entry's `snapshots:` line and the r89/r87 pins |
| 2 | `cmp` r89 pins (`chainload.c`, `panic.s2.c`) vs clone | **pass** | both IDENTICAL; sha256 `316eb17d…` / `0233d557…` = the lane's `SHA256SUMS` |
| 3 | `cmp` r87 pins (`uri.c`, `config.c`, `menu.c`, `CONFIG.md`) vs clone | **pass** | all four IDENTICAL; sha256 match the r87 `SHA256SUMS` and S351/S352/S353/S350 |
| 4 | Fetch the two raw URLs in r89 `URLS.txt`, record HTTP status + sha256 | **pass** | both HTTP 200; sha256 = the pinned files' sha256 exactly |
| 5 | Close Limit "the `limine`/`linux`/`multiboot` protocols' own failure messages were not read" | **closed** | read at the tag; candidate rows SR5, SR6 (per-protocol wording differs; a non-required `limine` internal module only warns) |
| 6 | Close Limit "`volume_get_by_coord`, `volume_get_by_guid`, `volume_get_by_fslabel` … were not opened" | **closed** | read at the tag, `common/lib/part.s2.c` 1035-1074; candidate rows SR1, SR2, SR3 |
| 7 | Close Limit "`tpm_present()` … was not opened" | **closed** | read at the tag, `common/lib/tpm.c` 113-115; candidate row SR4 — it is a **firmware** question (`EFI_TCG2_PROTOCOL`/`EFI_CC_MEASUREMENT_PROTOCOL` located by `gBS->LocateProtocol`), so the host's empty `/sys/class/tpm/` is *not* the same signal the entry's UF8 leans on |
| 8 | Read the `limine` (limine.c 627) and `linux` x86 (linux_x86.c 270) `uri_open` failure sites | **done** | limine.c 632 `panic(true, "limine: Failed to open executable with path \`%#\`. …")`; linux_x86.c 277 `panic(true, "linux: Failed to open kernel with path \`%#\`. …")` |
| 9 | Did upstream change `chainload.c` 414-437 since v12.9.4? | **no** | v12.9.4 raw 414-437 ≡ v12.9.6 raw 429-452, `diff` exit 0 (line offsets only); `refs/heads/trunk` carries the same bytes |
| 10 | Did upstream change `panic.s2.c`'s menu-return rule since v12.9.4? | **no** | v12.9.4 raw 71-92 ≡ v12.9.6 raw 79-100, `diff` exit 0. v12.9.5 added only a screen clear before the PANIC line under the UEFI fallback terminal |
| 11 | Freshness of the *rest* of the entry's sources | **drift found** | upstream v12.9.5 (2026-10-27) and v12.9.6 (2026-10-27) post-date the pinned v12.9.4 (2026-10-19); SR13-SR17 record five behavioural changes that touch what the entry says |
| 12 | Host reach re-check (read-only) | **consistent** | `pacman -Q limine` → `limine 12.9.4-1`; `/sys/class/tpm/` empty; `SecureBoot-8be4df61-…` efivar 5 bytes `06 00 00 00 00` (attributes `0x00000006`, data byte `00` = off); `SetupMode-…` the same 5 bytes `06 00 00 00 00` (data byte `00` = user mode). `/boot/limine.conf` is root-only (`Permission denied`, exit 1) — the L1's committed receipts were used instead, as the bounds require |

## 2. Counts

- Candidate rows written: **22** (`SR1`–`SR22`), in
  `.ufo/waves/round-89/w1/ScoutSources/proposed-rows.md`.
  - 17 `[src]` at the installed tag v12.9.4 (of which 4 close the entry's three Limits), 5 `[src freshness]` at v12.9.5 / v12.9.6 / trunk.
  - Every quote machine-verified: whitespace-normalised substring of the named file, ≤25 words.
- Receipts written to disk under this seat's directory:
  `receipt-clone.txt`, `receipt-cmp-urls.txt`, `receipt-upstream-drift.txt`,
  `receipt-release-dates.txt`, `receipt-host-recheck.txt`.
- Files compared byte-for-byte: 6 lane pins vs the tag clone (all identical).
- Raw URLs fetched: 2 (both HTTP 200).
- Upstream trees cloned (read-only, shallow, in scratch): v12.9.4 tag, v12.9.5 tag, default branch `refs/heads/v12.x`, `refs/heads/trunk`.

## 3. What the candidate rows add (depth)

The entry's rows are correct as far as they go; the rows below extend them, and three of them
narrow a claim the entry states without its exception.

- **SR1/SR2/SR3** — the volume layer is where a lookup dies: `volume_get_by_coord` matches on
  drive index + optical flag + partition and returns NULL with no message; `volume_get_by_guid`
  matches the volume GUID *or* its partition GUID; `volume_get_by_fslabel` compares
  **case-insensitively** (`strcasecmp`) — the one case-insensitive comparison in the layer.
  This is the Limit the entry flagged as unverified ("UF4's 'not found returns NULL' is the
  dispatcher's visible behaviour, not the volume layer's") — now it is the volume layer's.
- **SR4** — `tpm_present()` is true iff the *firmware* exposed an EFI TCG2 or CC measurement
  protocol (`tpm.c` 68-72, 113-115; `tpm.c` is `#if defined (UEFI)` only). The host receipt's
  empty `/sys/class/tpm/` is a Linux-side signal and does not answer it.
- **SR7** — `uri_resolve` has a **third** silent failure the entry does not list: an empty path
  after `):/` (uri.c 72-74) also returns false with no message and reaches the same
  "Failed to open image" panic.
- **SR8** — a malformed pin is its **own** panic with its own message ("Blake2b hash must be 128
  characters long", uri.c 89-101), not the "Failed to open image" panic and not a silent NULL.
- **SR9** — `boot(N)`'s partition number is parsed with `strtoui` and never validated as a whole
  string; only `val > 256` is rejected. `boot(x):/` silently opens partition 0, and `boot(1abc):/`
  opens partition 1. (Emulated `strtoui`/`digit_to_int` against the tagged source: `"x"→0`,
  `"1abc"→1`, `"-1"→0`, `"0x2"→0`, `"257"→257`.)
- **SR10** — a hash mismatch is a panic only when `hash_mismatch_panic` is set; Secure Boot
  forces it on (menu.c 1714-1716), and with the value `no` it is a prompt whose `Y` continues the
  boot with the mismatching file. This is the mechanism behind the round-86 `prompt` consequence.
- **SR11** — Limine's "Secure Boot is active" is narrower than the firmware's flag:
  `init_config` clears `secure_boot_active` when the config carries no enrolled checksum
  (config.c 491-492; USAGE.md 52-56).
- **SR12** — `measured_boot`'s value is compared with `strcmp` (only exact lower-case `yes`
  enables it) while `hash_mismatch_panic` uses `strcasecmp`: the two global booleans of one config
  are parsed by different rules.
- **SR18/SR19** — the halt half of UF7 is a UEFI statement: under BIOS the same
  `allow_menu == false` path prints "Press CTRL+ALT+DEL to reboot." and calls `rm_hcf()`; and the
  measured-boot force-off sits inside `#if defined (UEFI)`.
- **SR20** — under Secure Boot with an enrolled config hash, an `efi` entry whose pin is present
  but **wrong** still panics: `chainload()`'s clearing of `secure_boot_active` waives only the
  no-hash rule, while the mismatch check reads `hash_mismatch_panic`, which Secure Boot forces
  true.
- **SR21** — a `panic(true, …)` returns to the menu only while the firmware's boot services are
  still up (`efi_boot_services_exited == false`); a panic raised after the handoff halts the
  machine even with no measured boot.
- **SR22** — the panic text differs in what it shows the operator: `efi` prints the path with
  `%s`, so the screen **keeps** the `#<blake2b>` pin, while `linux`/`limine`/`multiboot` print
  with `%#`, whose handler (print.s2.c 180-202) cuts the string at the last `#` and hides it.

## 4. Freshness (upstream drift since the pin)

Upstream `v12.9.4` was published 2026-10-19; `v12.9.5` and `v12.9.6` were both published
2026-10-27 (GitHub releases API). The host still runs `limine 12.9.4-1` **and the Arch `extra`
repository still carries only `12.9.4-1`** (`pacman -Si limine` → `Version : 12.9.4-1`,
read-only, no transaction), so the pinned tag remains the ground for this host today and the
distro has not yet imported the two newer releases. But the entry's `recheck:` line ("on any
`limine` package update") is now live, and five upstream changes touch what the entry says:

- **SR13** — v12.9.5 added a Fast-Boot retry under UEFI: a volume that is not found makes Limine
  connect all disks and search again. It wraps `hdd()`, `odd()`, `guid()`/`uuid()` and
  `fslabel()` — **not** `boot()`, which still looks the volume up once.
- **SR14** — the two rules the entry is built on (`chainload()`'s failure path, `panic()`'s
  menu-return rule) are **byte-identical** at v12.9.4 and v12.9.6/trunk. This is the strongest
  "the entry still holds" evidence available without booting.
- **SR15** — v12.9.6 changed the config grammar: global options must come before the first menu
  entry and any that follow it are ignored. A `hash_mismatch_panic: no` that ever sat after the
  first entry would be silently dropped by an upgrade, turning the round-86 `prompt` consequence
  into a panic. On this host the key is at line 8 of `/boot/limine.conf` (r88/r89 receipts), i.e.
  before the first entry, so the host is not exposed today — but the migration is not silent-safe.
- **SR16** — v12.9.5 changed `limine_efi_vendor_guid`, so an upgrade stops reading the
  last-booted entry written by the older build.
- **SR17** — v12.9.5 changed measured boot's TPM handling: a full event log now counts the
  component as measured with one warning.

Also worth the L1's attention: upstream **removed** the `uri.c` "No resource specified for URI"
`URI_ERROR` branch (present at v12.9.4 uri.c 339-342, gone in v12.9.5+) — in v12.9.4 that branch
is unreachable anyway, because `uri_resolve` returns false before it whenever the URI has no `(`.

## 5. Limits of this seat's own report

- Nothing was booted; no Limine binary was executed. All behaviour claims are read from source at
  a named tag and, where marked `[src freshness]`, at a named upstream commit.
- `git ls-remote` and the GitHub releases API were reachable, but the releases API returned
  `504 Gateway Time-out` on three consecutive retries late in the round
  (`.ufo/waves/round-89/w1/ScoutSources/receipt-release-dates.txt`); the release dates quoted
  above are the ones the same API returned earlier in this round, and the tag/branch commit ids
  come from `git ls-remote`, which succeeded.
- `/boot/limine.conf` is not readable without `sudo`, and `sudo` is forbidden to this seat; the
  host facts come from the L1's committed receipts (r89 `before/host/receipt.txt`, r88
  `before/host/receipt.txt`) plus the read-only `pacman -Q`, `/sys/class/tpm/` and
  `/sys/firmware/efi/efivars/` reads re-run here.
- The `strtoui` edge cases in SR9 were obtained by re-implementing the tagged `strtoui` and
  `digit_to_int` in Python (the tagged C source was read line by line), not by running Limine.
- I make no judgment on the entry's depth or on C2's verdict: a wave seat is the lane
  (LEARNING.md §Discernment), and the non-author hyaku closure owns that.

## 6. Files

- Report: `.ufo/waves/round-89/w1/ScoutSources.md`
- Candidate rows: `.ufo/waves/round-89/w1/ScoutSources/proposed-rows.md`
- Receipts: `.ufo/waves/round-89/w1/ScoutSources/receipt-clone.txt`,
  `receipt-cmp-urls.txt`, `receipt-upstream-drift.txt`, `receipt-release-dates.txt`,
  `receipt-host-recheck.txt`
- Scratch used and removed: `/fast/scratch/hyaku/tsukuroi-r89/ScoutSources` (clones only).

## 7. Refused / not done

- No lane file edited (no patch proposed into `corpus/`); the C2 entry, the `.json` rows and
  `corpus/SOURCES.md` are untouched.
- No commit, push, or any mutating git/jj command in the lane or anywhere else.
- No `sudo`, no write to `/boot`, `/efi`, `/etc`, `/usr`, `/var`, `/sys` or `/proc`, no objcopy /
  strip / sbsign / ukify / limine / pacman, no sysctl change, no service restart, no pacman
  transaction. Tooling installed: none.
- The C1 battery/counter was not run — it is out of this seat's scope and the freeze forbids
  re-scoping it.
