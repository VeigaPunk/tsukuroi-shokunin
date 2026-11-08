# SOURCES row drafts — seat ScoutURI, round-91 w1 (C2 sources, URI-resolution half)

Scout seat. **Drafts only** — `corpus/SOURCES.md` was NOT edited; the L1 decides what lands.

Id convention: the registry's highest used id at the time of writing is **S376**, so the next free ids
are S377 onward. The rows below are therefore drafted with the ids S377-S379 marked **TBD** — the L1
should re-check the registry for ids claimed by another seat in this wave before landing them.

Every "teaches" cell below is limited to what this seat actually read or measured. Where a claim is
inference rather than observation it says so.

## Already registered — no new row needed

The three primary sources for this seat's rows are already in the registry as **S374** (`common/lib/uri.c`),
**S375** (`common/protos/chainload.c`) and **S376** (`common/lib/config.c`), added in round 91. This seat
read all three and re-verified their pinned snapshots byte-for-byte against the upstream v12.9.4 raw URLs
and against a fresh tag clone; the checks are in `receipt-uri-resolve.txt` §1. No new row is proposed for
them; the anchors are confirmed correct.

## Draft rows for sources not yet in the registry

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S377 (TBD) | Limine v12.9.4 `common/menu.c` — https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/menu.c | code | A | Which config key selects the entry's boot protocol, and which protocol strings reach the EFI chainloader | tag v12.9.4 (clone HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c`), raw lines 2429-2432 (`char *proto = config_get_value(config, 0, "PROTOCOL");` and the "Boot protocol not specified" panic), 2456-2460 (the UEFI branch dispatching `efi_chainload`/`efi`/`uefi` to `chainload`); sha256 `628001e88564525f8d1e0e6193ea86145e5613eaea97c04110545cd182168f95` (identical to the lane's r87/r90 pins of this file) | the protocol key is read from the entry body and the three efi protocol names are the ones that reach `chainload` on UEFI, which is the set the gate treats as efi image entries | mined | 2026-11-07 | on-release | corpus/knowledge/limine-unverified-image-r91.md |
| S378 (TBD) | Limine v12.9.4 `common/entry.s3.c` — https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/entry.s3.c | code | A | What Limine's own `secure_boot_active` flag means, as opposed to the firmware's Secure Boot variable | tag v12.9.4 (clone HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c`), raw lines 72-73 (read the firmware `SecureBoot` variable) and 77-79 (set `secure_boot_active` only when `SetupMode == 0` or `SetupMode` is unreadable); **not pinned in `.ufo/waves/round-91/after/src-c2/` this round** — sha256 `9aef63d37c75…` recorded in `receipt-uri-resolve.txt` §1 for a future pin | Limine treats Secure Boot as active only when the firmware reports `SecureBoot == 1` and `SetupMode == 0`, so the firmware flag alone does not settle the question; on top of that `init_config` clears the flag when no config checksum is enrolled (config.c 491-492) | mined | 2026-11-07 | on-release | corpus/knowledge/limine-unverified-image-r91.md |
| S379 (TBD) | ScoutURI's own compiled harness over the pinned Limine v12.9.4 `uri_resolve` — `.ufo/waves/round-91/w1/ScoutURI/uri_resolve_probe.c` (and `uri_resolve_probe_argv.c`) | own-work | A | Which of `uri_resolve`'s failures are message-free, and what the resolver returns for a value with shape but no `#` | the harness compiles `uri.c` raw lines 32-107 verbatim out of the pinned snapshot `.ufo/waves/round-91/after/src-c2/limine-v12.9.4-common_lib_uri.c` (sha256 `e06cac1212fec55150c109843e22dfe01cd618d4e81235e357d9a256e2a2ed6f`) and re-implements upstream's `URI_ERROR`/`panic` semantics as a stub; two variants are built, one with upstream's noreturn `panic` and one with `URI_ERROR` demoted to print-only; outputs in `receipt-uri-resolve.txt` §2 and §3 | exactly three of `uri_resolve`'s failures are message-free (no `(`, no `):/`, empty path); a value with shape but no `#` returns true with `hash == NULL`; a malformed hash is a loud `URI_ERROR` (panic on a required key), not a silent failure | mined | 2026-11-07 | on-release | corpus/knowledge/limine-unverified-image-r91.md |

## Notes for the L1

- **S378 is not pinned.** `common/entry.s3.c` is not among the three files in
  `.ufo/waves/round-91/after/src-c2/`, so a row pointing at it would cite a file the lane has not frozen.
  Either pin it (add to `src-c2/` and the SHA256SUMS there) or cite the pinned `common/lib/config.c`
  (S376, which carries the `init_config` half at 491-492) and mark the firmware half as read-from-clone.
  This seat's UR23 row depends on that choice, and the row's source column already says
  "not pinned in this round".
- **S379 is own-work and cites a wave-local artifact.** Its durability is the wave directory's; that is
  the same shape as the existing own-work rows (e.g. S371, a host-receipt row).
- The registry's `Paths` and `Search log` sections were not touched by this seat.
