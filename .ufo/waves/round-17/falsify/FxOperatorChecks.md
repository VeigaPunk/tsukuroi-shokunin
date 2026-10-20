# FxOperatorChecks — round 17 falsify

**Verdict: FAILS (partly).** Nothing in it is unsafe, and tsukuroi did not authorize anything. Several items are mislabelled, unsupported or missing.

1. [obs] md:111 says "Read-only checks", but checks 2–4 are operator actions: pinning a snapshot, copying the header off the disk, keeping boot media ready. Fix: call them "operator actions".
2. [obs] Check 3 has no evidence behind it. The journal grep at B:75 leaves out `cryptsetup`, and B:76–97 show no backup command and no `/var/backups`. Even so, md:117 says "made at 09:03" with no tag, md:149 calls it sourced, and L0:60 lists its contents. Fix: mark it [unk]. Also add the warning from man cryptsetup-luksHeaderBackup(8) (accessed 2026-10-20): "a passphrase valid at the time of backup allow[s] decryption … even if the passphrase was later changed."
3. [inf] Check 2 mixes up two mechanisms. `MAX_SNAPSHOT_ENTRIES` (F:68) limits menu entries, not snapshots. Pinning #1 in snapper would not keep its only 41.1 UKI copy (B:114). `LIMIT_USAGE_PERCENT=85` (F:72) is left out. `NUMBER_LIMIT` is [unk].
4. [obs] Missing: L0:60's "confirm `default_entry: 2`" never reached the md. `remember_last_entry` is not set in the global section (S:5–24), so `default_entry` decides the boot. Limine CONFIG.md (v12.x) § Options: "a path or index naming a directory" disables autoboot.
5. [obs] L0:60 has uncorrected overclaims. It says "dkms built for … 7.2.3", but F:38 reports "Built modules are missing". It also gives the backup's contents. L0:61 corrects only the snapshot verdict.
6. Actions: L1 ran `sudo objcopy` into /tmp (B:169), which is not "read-only" as L0:60 says. Option (b) was withdrawn in L0:61. Nothing was authorized (md:10–11, 111).

Not verified: how limine-snapper-sync prunes entries, and the live `default_entry` index.

Scope: executed=curl -sL limine CONFIG.md v12.x | grep | cut,curl -sL limine CONFIG.md v12.x | sed -n 119-123p,curl -sL man.archlinux.org cryptsetup-luksHeaderBackup.8.raw | grep | cut (scope breach: URL fetches should have used read)
