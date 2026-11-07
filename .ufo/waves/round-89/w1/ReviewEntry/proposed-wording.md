# ReviewEntry — proposed wording (patches for the L1 to apply or drop)

All patches are against `corpus/knowledge/limine-uri-failure-r89.md` (and mirrored in
`limine-uri-failure-r89.json` if accepted). Old text quoted exactly as on disk at master `665408cc`.

## P1 — UF1 statement (label honesty + self-consistency)

OLD (UF1 statement, md table and json "statement"):

    [src] Every URI error goes through `URI_ERROR`, which panics unless the URI was opened through
    `uri_open_optional` (the optional-resource path); only then does it print and return. So any URI failure on
    a required key (`path:`, `kernel_path:`, `module_path:`) is a panic, and the same panic carries a hash
    mismatch under `hash_mismatch_panic: yes`.

PROPOSED:

    [src] Every raised URI error message goes through `URI_ERROR`, which panics unless the URI was opened
    through `uri_open_optional` (the optional-resource path); only then does it print and return — a failed
    resolution can also return NULL with no message (UF4/UF5). [src] So a URI failure on an `efi` entry's
    `path:` is a panic (chainload.c 434-435), and the same panic path carries a hash mismatch under
    `hash_mismatch_panic: yes` (uri.c 301-305). [inf] The same is expected for `kernel_path:`/`module_path:`;
    their `uri_open` callers are listed in Limits, not opened.

Reason: silent-NULL paths (uri.c 239-240, 194-196, 185-186, 368-370) do not go through `URI_ERROR`; the
kernel_path/module_path callers are outside the pinned set, so that clause cannot be [src].

## P2 — UF3 nit (PXE redirect covers boot(N) too)

OLD: `on a PXE boot \`boot()\` is redirected to \`tftp\``
PROPOSED: `on a PXE boot \`boot()\` and \`boot(N)\` are redirected to \`tftp\` (uri.c 221-222, before the
\`s_part\` check)`

## P3 — UF6 addition (SB forces hash_mismatch_panic; mismatch then panics)

Append to the UF6 statement, after "the code only waives the missing-hash rule.":

    Under Secure Boot, menu.c also forces `hash_mismatch_panic` on (menu.c 1714-1717, S353), so a present-pin
    mismatch there is a `URI_ERROR` panic, not the Y-prompt.

Reason: closes the misreading that a mismatch under SB would still prompt; S353 is already pinned and its
registry anchors already include 1711-1717.

## P4 — UF8 TPM hedge

OLD: `an empty \`/sys/class/tpm/\` shows Linux has no TPM device, which is what Limine's \`tpm_present()\`
would also need; not executed at boot.`
PROPOSED: `an empty \`/sys/class/tpm/\` shows Linux has no TPM device — evidence (not a firmware probe) that
Limine's \`tpm_present()\` would also come up empty; not executed at boot.`

## P5 — header `source:` line (align with registry S351)

OLD: `new anchors 18-26, 46-63, 109-271, 344-376, 696-708`
PROPOSED: `anchors used: 18-26, 46-63, 109-243, 301-305, 344-366, 372-376, 696-710 (registry S351)`

Reason: 18-26 is a pre-existing r87 anchor; 109-271 and 696-708 match neither the registry (109-243, 696-710)
nor anything the rows cite. Same line, cosmetic: describe the capture as S363 does — "`sudo -n grep` of
`/boot/limine.conf`, plus `ls` of `/sys/class/tpm/`, `od` of the SecureBoot efivar, `pacman -Q limine`".

## Not proposed (checked, no change needed)

- UF2, UF4, UF5, UF7: no wording change.
- SOURCES S361-S363 and the S350/S351/S353 anchor edits: correct as written.
