# FxBootedObserved — BOOTED-OBSERVED `//linux`

**Verdict:** "this image booted" SURVIVES, [inf] grade only. "Next default boot repeats it" is UNPROVEN.

- [obs] Limine v12.9.3 (`e3aa138`) `bli.c:288` sets `LoaderEntrySelected` without NON_VOLATILE, so the value is from this boot. It names a menu ID, not an image. The path came from the 09:57 limine.conf, which no capture holds (current file 12:07:06 B:106; `.old` 09:03 B:107).
- [inf] Image binding: the only 7.2.11 UKIs are `2e9c…` (B:114-125, 171, 219); uname matches (B:5); cmdline matches (B:12 = S:35). No TPM or StubPcr measurement captured.
- [obs] `hash_mismatch_panic: no` (S:12): a mismatch prompts `Y` instead of panicking (`uri.c:281-293`). So S:34 shows only that the current file matches the current conf; Limine did not enforce it at boot.
- [obs] `default_entry: 2` → `//linux` (`print_tree` counts the `/+Omarchy` directory). No `remember_last_entry`.
- [inf] OneShot was absent at 13:03 (S:97-110) and would preempt `default_entry` (`menu.c:1850`). BootNext/BootOrder were not captured; fwupd was installed 09:27 (B:60).
- [obs] Gaps: the sweep checks mtime only, and pacman preserves package mtimes. `/usr/lib/firmware` is not swept. The B:54 pacman query covers only 07–09h.

**Correction:** gate the next-boot claim on pre-reboot reads: no OneShot/BootNext; `//linux` block and sha256 unchanged.

**Unverified:** host binary behavior; boot keypress; `/boot/loader`.

Deviation: unauthorized exec (doc fetch, mktemp source clone, wc); no lane or host probe.

Scope: executed=curl,grep,sed,mktemp,git clone,git log,tail,ls,head,cut,wc
