# Draft — round-89 lesson `## Gate` (seat ScribeLesson)

Measured at lane `665408cc45a88ed49717e22f4593e8e6152ac665`. Every quote below was re-read by this seat in the
pinned snapshot named in the row's anchor (`receipts/quote-verification.txt`, which prints each file with `sed`
line ranges and its `sha256`). The L1's rows already in `corpus/lessons/round-89.md` (lines 29-47) are consistent
with these; the only substantive difference is the REJECT row, where this draft replaces "not cloned by the L1"
with a measured diff (§3).

## 1. Admit rows (S361, S362, S363)

| Candidate | URL, access date, location | Located quote (≤25 words) | Decision, reason and flip |
|---|---|---|---|
| S361 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/protos/chainload.c, 2026-11-06, raw 414-437 | "panic(true, \"efi: Failed to open image with path `%s`. Is the path correct?\", image_path);" (raw 435; sha256 `316eb17d…` of the pinned copy) | ADMIT, UF5/UF6. The only statement of what an unopenable `path:` does to an `efi` entry — the protocol of all six host entries (`receipt.txt:4-9`). Raw 423-424 carries the Secure-Boot comment UF6 quotes; raw 430-434 is the `uri_open` whose NULL reaches the panic. Flip: a `limine` upgrade that changes `chainload()`'s failure path (recheck `on-release`). |
| S362 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/panic.s2.c, 2026-11-06, raw 18-29, 70-100 | "print(\"Press a key to return to %s.\", booting_from_editor ? \"editor\" : \"menu\");" (raw 78; sha256 `0233d557…`) | ADMIT, UF7. Turns the gate's consequence word `panic` into the operator-visible effect: menu return at raw 78-82, halted machine at raw 87-100; raw 18-29 clears `allow_menu` under measured boot. Flip: as S361. |
| S363 (new, own-work/A) | `.ufo/waves/round-89/before/host/receipt.txt`, captured 2026-11-06T21:52:29-03:00 (read-only `sudo -n grep`, `ls`, `od`, `pacman -Q`) | "29:  protocol: efi" (receipt line 4) | ADMIT, UF2/UF5/UF7/UF8 host values. Six `protocol: efi` lines (receipt 4-9), `hash_mismatch_panic: no` (3), no `measured_boot` key (3-10), `/sys/class/tpm/` empty (11-14), `SecureBoot` byte `00` (15-16), `limine 12.9.4-1` (17-18). Flip: any `/boot/limine.conf` rewrite (recheck `30d`). |

Quote-length check (this seat): S361 14 words, S362 11 words, S363 2 words.

## 2. Anchor changes, old→new (verified field by field in `receipts/sources-anchor-diff.txt`)

`old` = `git show dfeaab29:corpus/SOURCES.md`; `new` = `master`.

| Row | Anchor: old → new | teaches | used-by | status / opened / recheck |
|---|---|---|---|---|
| S350 (`SOURCES.md:361`) | `… 111-113, 134, 152-156, 210, …` → `… 111-113, 134, 152-156, 157-160 (measured_boot), 210, …` | unchanged | + `corpus/knowledge/limine-uri-failure-r89.md` | unchanged `mined` / 2026-11-06 / `on-release` |
| S351 (`SOURCES.md:362`) | `28-104 (uri_resolve: last #, 128 hex)` → adds `; 46-63 silent false on no ( or no ):/`; inserts `109-243 (hdd/odd/guid/uuid/fslabel/tftp/boot dispatchers; boot(N) = partition N on the boot drive)`; `344-362 (resource dispatch)` → `344-366 (resource dispatch, unknown resource not valid)`; inserts `372-376 (Secure Boot no-hash rule)` | **unchanged** ("the hash is after the last # …") | + the r89 entry | unchanged |
| S353 (`SOURCES.md:364`) | `1711-1717` → `1711-1717, 1719-1730 (measured_boot: config yes or Secure Boot active, off without TPM/CC)` | unchanged | + the r89 entry | unchanged |

Anchor lines verified in the pinned files: S350 157-160 is the `measured_boot` bullet; S351 109-121 is
`parse_bios_partition`'s "Drive number cannot be omitted" (119), 220-243 is `uri_boot_dispatch`, 344-366 ends at
`URI_ERROR("Resource \`%s\` not valid.", resource)` (364); S353 1719-1730 sets `measured_boot` and clears it when
`!tpm_present()`. The three new rows S361-S363 are `mined` (`30d` for S363, `on-release` for the two code rows).

Two notes for the registry text:
- S351's `teaches` is **not** changed by this round, although the entry's UF1-UF4 state more than the `teaches`
  cell does; if the L1 widens it, the widening is a r89 decision, not a fact of the diff.
- S350's anchor line 210 is the `#hash` grammar sentence; the r89 entry cites 157-160 only.

## 3. REJECT candidate (strengthened)

| Candidate | URL, access date, location | Located quote (≤25 words) | Decision, reason and flip |
|---|---|---|---|
| REJECTED: Limine's **trunk** branch (`https://raw.githubusercontent.com/limine-bootloader/limine/trunk/common/protos/chainload.c`) as a source for this host's behaviour | fetched read-only 2026-11-06 (HTTP 200, 18463 B, sha256 `68d56ee4f3aedd2bcef604bb1331a05988b53a08f416254f12f5f514c465c5b3`, kept at `receipts/trunk/`) | same sentence at a different line: "panic(true, \"efi: Failed to open image with path `%s`. Is the path correct?\", image_path);" (trunk **450** vs pinned v12.9.4 **435**) | REJECT for rows: the host runs limine 12.9.4-1 (`receipt.txt:18`); trunk differs from the installed tag in three hunks, two of them behavioural — it roots the EFI file path with a `\` and grows the UTF-16 buffer by one (`(original_path_chars + 2)`, `efi_file_path[0] = '\\'`), and it clamps an extended-partition `sect_count` to the disk end. Reading trunk would attribute to the host code the host does not run, and would shift every cited raw line by ~15. Flip: a host upgrade past 12.9.4 → re-pin at the new tag (`on-release`). |

Evidence: `receipts/trunk-vs-tag.txt` (sha256 pair, both `grep -n "Failed to open image"` readings, `diff -u` =
3 hunks) and `receipts/trunk/limine-trunk-common_protos_chainload.c`.
