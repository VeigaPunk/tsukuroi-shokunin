source: S282 — systemd v262 release notes (https://api.github.com/repos/systemd/systemd/releases/tags/v262, section "## Changes in the TPM Subsystem:", NvPCR bullet); own-work probes `.ufo/waves/round-65/probes/`
verified-at: 2026-11-03 (host plazir27, Arch, kernel 7.2.11-arch1-1, systemd 262.1-1)
recheck: on-release — the next systemd release, or any firmware TPM2 appearance / UKI rebuild-path change, re-fires the applicability watch (SY4 falsifier)

# systemd 262 NvPCR/UKI requirement — this host's applicability (round 65)

Reading plane: what systemd v262 changed about NvPCR anchoring and UKI
signing, and whether any of it binds THIS host's boot chain (limine +
mkinitcpio-built UKIs, no TPM2). Detection and report only; nothing is
built, signed, or configured. Cross-round link: S279 (mkinitcpio v42.2
release notes, r64) quoted the same change from the installer side — this
note measures the requirement's host-side applicability.

| id | row | ground | receipt |
|---|---|---|---|
| SY1 | The v262 requirement. "For NvPCRs to work, all NvPCR definitions (/usr/lib/nvpcr/*.nvpcr) must now be shipped in the UKI. The UKI must also embed a signed PCR policy that is bound to the initrd boot phase and with the "initrd" policy reference. This can be created by supplying the --sign-initrd-pcrs option to ukify." (S282, "Changes in the TPM Subsystem", first bullet; the 23-word Gate quote counted by `wc -w`.) Same bullet: NvPCRs not defined/initialized in the initrd fail lazy init at extend (systemd-pcrextend); existing NvPCRs auto-upgrade and the old "anchor secret" in /var/lib + ESP is removed. Corroboration on this host: the shipped `hardware.nvpcr` carries `"orderly" : false` — the same body's later bullet ("The 'hardware' NvPCR will now disable by default"). S279's installer-side wording matches (mkinitcpio v42.2 ships systemd-tpm2-setup-early.service + systemd-pcrnvdone.service; "systemd v262 requires that the UKI must be signed with a PCR policy and there is still no solution for that without using ukify"). | `.ufo/waves/round-65/before/s282-v262-body.md` (release JSON sha256 `008e1265…babce0b`); `probes/r65-nvpcr.txt` |
| SY2 | Host firmware state: TPM2 Support **no**; Secure Boot **disabled**; Measured UKI **no** (bootctl, unprivileged fields) AND no `/dev/tpm*` node exists — there is no TPM on this machine, so no NvPCR can ever be extended here today. | `probes/r65-bootctl.txt`, `probes/r65-tpm2-units.txt` |
| SY3 | Host build/boot state: limine boots **UKIs** — `protocol: efi` entries pathing `boot():/EFI/Linux/omarchy_linux.efi` (+ the `-lts` variant and limine-snapshot copies), images built 2026-10-20 (the mkinitcpio-42.2 upgrade day), 281-290 MB each; `/etc/mkinitcpio.d/` presets dir EMPTY (the UKIs are built by the omarchy/limine-entry-tool flow — the exact builder is an unknown this round); ukify ABSENT (`systemd-ukify` not installed, binary not on PATH); `/usr/lib/nvpcr/` EXISTS with 4 defs (cryptsetup, hardware, login, verity), each `pacman -Qo`-owned by systemd 262.1-1; 4 `/etc/mkinitcpio.conf.d/` drop-ins; 12 hooks, 2 name `/new_root` (r64 MK2). | `probes/r65-limine-conf.txt`, `probes/r65-boot-inventory.txt`, `probes/r65-ukify.txt`, `probes/r65-nvpcr.txt`, `probes/r65-mkinitcpio-conf.txt` |
| SY4 | Applicability verdict: the requirement's failure mode — NvPCRs failing lazy init at a runtime `systemd-pcrextend` — is UNREACHABLE on this host today: NvPCRs live in the TPM2 and this machine has none (SY2), so no extend can be attempted and whether the UKIs embed the `/usr/lib/nvpcr/` defs is currently unobservable. The exposure is real but latent: the host boots mkinitcpio-built UKIs (SY3) while ukify — the only documented way to create the signed initrd-phase PCR policy — is not installed, so a firmware TPM2 would surface a real gap (rebuild the UKIs with the defs embedded and a signed policy, or forgo NvPCR features). Falsifier (re-fires the watch, on-release): `/dev/tpm*` appearing or bootctl reporting TPM2 Support yes; any unit attempting `systemd-pcrextend` against these NvPCR names; a UKI rebuild path claiming NvPCR support. | SY2 + SY3 receipts; verdict re-derived from S282 text |
| SY5 | Unknowns: the exact builder of `/EFI/Linux/omarchy_linux.efi` (presets empty; omarchy/limine-entry-tool flow not probed); whether the current UKIs embed the 4 `.nvpcr` defs (needs a UKI content read — a /boot binary read beyond this round's receipt scope, and moot without TPM2); the v262 `credentials_boot_policy=` default "relaxed" is unexercised here (no TPM2 → strict/tofu cannot differ). | `probes/r65-boot-inventory.txt`; this row states the unmeasured halves |

Boundary: this note holds boot-chain STATE (what the requirement demands,
what the host has). It names no binary internals — UKI content analysis
and any RE-class question stay with ADJ-06 (kaidoku/revenger, ownership
unruled); pressure attribution stays mori's (ADJ-04). No package, service,
boot or firmware action is authorized by this note.
