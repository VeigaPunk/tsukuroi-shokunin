ReviewSource — proposed edits (NOT applied; lane is read-only for this seat)
=============================================================================
Anchors are line numbers at rev ce89df93e5f576c5c236d4547299e9ea954e8853. Everything below is a
proposal for the L1; the frozen battery (sha256 8f0daee8…) and the candidate gate must not change
inside round 90. Findings F1/F2/F3/F4 are explained in .ufo/waves/round-90/w1/ReviewSource.md.

P1 (F1, high) — tools/limine-pin-battery-r90.py:90-92 (R10) replace
  "  R10 on_panic (...): the
     top-level object MUST carry "on_panic" (not checked when --conf is unreadable). Measured boot
     is requested when the FIRST `measured_boot` key line in the whole file (R1 rules, key
     case-insensitive) has a value exactly `yes` (strcmp, case-sensitive), or when
     --secure-boot-enforced 1."
with
  "  R10 on_panic (...): ...
     Measured boot is requested when the FIRST `measured_boot` key line Limine can see (R1 rules,
     key case-insensitive) has a value exactly `yes` (strcmp, case-sensitive), or when
     --secure-boot-enforced 1. Limine reads that key from config_addr, which init_config truncates
     at the newline before the first entry line (config.c 643-650), so only the global section
     counts; when the file's first line is itself an entry line the guard at 648 leaves the whole
     file visible and every `measured_boot` line in every body counts."

P2 (F1, high) — tools/limine-pin-battery-r90.py:62-63 (R6) replace
  "else `prompt` when the FIRST `hash_mismatch_panic` key line in
     the whole file (R1 rules) has a value equal to `no` case-insensitively, else `panic`."
with
  "else `prompt` when the FIRST `hash_mismatch_panic` key line Limine can see (R1 rules) has a
     value equal to `no` case-insensitively, else `panic`; the visibility rule is R10's (global
     section only unless the file starts with an entry line; config.c 643-650, menu.c 1711-1712)."

P3 (F1, high) — the model and the two families, if the L1 wants the battery to test Limine rather
than itself:
  - tools/limine-pin-battery-r90.py:215-228 (`r1_panic`) and 281-287 (`r1_first`): scan only the
    lines before the first entry line; if line 1 is an entry line, scan the whole file.
    (`want_on_panic` 312-318 uses r1_first, so it follows automatically.)
  - 1211-1220 `fam_measured_in_entry`: with a `header()` line first the expectation becomes
    `menu` (tpm 1), not `halt`; keep a second family with no header whose expectation is `halt`.
  - 1251-1259 `fam_panic_after_pin`: with a header line first the expected consequence of the
    mismatch is `panic` (no prompt), not `prompt`; keep a headerless variant expecting `prompt`.
  - The gate, tools/check-limine-pins.py:136-157: stop recording `measured_boot` /
    `hash_mismatch_panic` once an entry line has been seen, unless line 1 is an entry line.

P4 (F2, medium) — battery R9 last sentence, tools/limine-pin-battery-r90.py:87 replace
  "The image line need not be a pin; only a pin on it gets R6's missing -> panic."
with
  "The image line need not be a pin; a pin on it gets R6's missing -> panic, and a value on it that
     is not a pin (no '(', no '#', or empty) still goes to uri_open and panics at chainload.c 435,
     so the gate must not read HEALTHY on such a conf even though it reports only pins."

P5 (F3, low) — pin common/lib/tpm.c (R10's "TPM/CC interface" and C2's tpm_present() rest on it):
  add to .ufo/waves/round-90/before/src/URLS.txt
    https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/tpm.c
  and to SHA256SUMS
    d6892d0b430c7639ad7e10d98715d4953892e81e9bfe9d7381c366cf0743f090  limine-v12.9.4-common_lib_tpm.c
  (Optionally common/protos/efi_boot_entry.c, for the efi_boot_entry question:
   URL https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/protos/efi_boot_entry.c)

P6 (F4, low) — tools/check-limine-pins.py:139: `... .strip()) or entry` keeps the previous label
  for a bare "/" line; R8 defines the label as the stripped line text, so drop `or entry` (or state
  in R8 that an empty label inherits the previous one — no fixture exercises it).

P7 (F5, info) — no change: wallpaper/term_font are parsed from the global (truncated) config by
  menu_init_term -> gterm_init(NULL, ...) (menu.c 1407-1422, 2017; gterm.c 805-855). A wallpaper or
  term_font pin inside an entry body is never opened; "skip" remains the right consequence, but for
  the reason "never read", not "optional open".

Also worth adding to R9's limits (no code change needed): Limine's `config_get_entry` skips the line
after a bare "/" entry line (the `do p++` at config.c 704-706 starts testing at f+2), so that line
belongs to no body; no frozen fixture produces a bare "/".
