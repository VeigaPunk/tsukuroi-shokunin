# Sweep11 — C3 per-surface recon: initramfs-v42-sysroot-recovery.md

Target `corpus/knowledge/initramfs-v42-sysroot-recovery.md`; working bytes equal baseline 842a5312 (`git diff --stat` empty). Result: **bounded no-notice**. Zero new stale current-use statements; no `.append.txt` or `.records.json` written. Integrator must not count this surface.

Checked current-use guidance:

- `recheck:` header :3 — its `pacman -Q` is already superseded by baseline `## R17-RECHECK` :74-81; the non-pacman probes remain valid. S052/S060.
- Installed-package row :9 — all five old values are already named by `## R17-FRESHNESS` :63-67. R18 confirms `mkinitcpio-42.2-1` (`host-capture-r18.txt:34`), `snapper-0.13.2-1` (:37), `limine-snapper-sync-1.32.1-2` (:31); no contradiction. S060.
- :11 "configuration evidence, not an unpack/inspection" and :14 future-upgrade/silent-no-op — already superseded by R17-FRESHNESS :70 and R17-SYMLINK :83-85. S051/S059.
- Recovery table :20-24 — still live. Installed 42.2 UKIs are busybox (`HOOKS="udev plymouth keymap consolefont encrypt resume"`, `boot-chain-capture.txt:177`), and upstream `raw/v42.2/init` plus `init_functions` still accept `break=premount`, bare `break`/`break=y`, and `break=postmount`, resuming on exit. S051.
- Falsifier :32 — its "No image rebuild or test boot" half is already noticed at :71; the prediction it qualifies is withdrawn at :83. Not current-use guidance.
- R5 :28 — consistent with the systemd-free HOOKS at `boot-chain-capture.txt:177`. S051.

Rejected as defects: dated 2026-10-19 `[obs]` rows and the historical 41.1 image are true at their dates; append-only notices preserve them. Not current host claims.

Evidence limits: plymouth and limine-mkinitcpio-hook are absent from R18's selective package listing; their latest observed values remain R17 `fresh-capture.txt:17-18` (S052). Whether they changed after R17 is `[unk]`, but no stale quote follows. OverlayFS behavior in the current boot remains unobserved in R18; R17-SYMLINK's withdrawal stands, not a new claim.

Scope: executed=read-only git (rev-parse/log/status/diff) and file reads; no host probes, no gates.
