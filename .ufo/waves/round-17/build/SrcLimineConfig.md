# SrcLimineConfig — limine CONFIG.md semantics (R17)

[obs] Opened https://github.com/limine-bootloader/limine/blob/trunk/CONFIG.md 2026-10-20; reader fetched https://raw.githubusercontent.com/limine-bootloader/limine/trunk/CONFIG.md. Fragments: "Options → Miscellaneous" (`default_entry`, `hash_mismatch_panic`), "Paths".

`default_entry` — "Can be a 1-based entry index (e.g. `1`), or an entry path"; "A value that does not name a bootable entry still counts as set, but disables autoboot" — "that covers ... an index naming a directory."

CONFIG.md never says whether directory rows consume an index. Source does: `print_tree` numbers each non-skipped row depth-first, directories included, recursing only when expanded (common/menu.c:1289-1388); a numeric value is decremented once (:1906-1908; identical at v12.9.3). So captured `default_entry: 2` (boot-chain-capture.txt:3), with rows 1 `/+Omarchy` (:21, expanded by `+`) and 2 `//linux` (:25, 7.2.11 UKI, `#8222…`), selects `//linux` — the kernel the host booted at 09:57 [obs].

`hash_mismatch_panic: no` — "do not panic if there is a hash mismatch for a file"; "A warning is printed and Limine then waits for a keypress: `Y` continues the boot, any other key returns to the menu." "Forced to `yes` when Secure Boot is active and a config hash is enrolled."

Path hashes: "64 hexadecimal characters is standard BLAKE3, 128 is BLAKE2b, and 256 is extended-output BLAKE3." Captured 128-hex suffixes are BLAKE2b, equal to capture b2sums [obs].

Not established: Secure Boot/enrolled-hash state here; OneShot/remember_last_entry precedence; on-disk config beyond the L1 capture; hash-to-UKI match; trunk-vs-12.9.3 drift; whether any mismatch occurs.

Scope: executed=none
