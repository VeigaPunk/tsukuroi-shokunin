# CritDefaultEntryProof — falsify "default `linux` entry BOOTED-OBSERVED"

**Counterexample [obs]:** rule 2 requires that no boot-chain input be newer than the boot start (boot-chain-r17.json:25). `/boot/limine.conf` was modified at 12:07:06, after the boot that started at 09:57:09 (capture:106,10). The no-newer-input sweeps leave out `/boot` (capture:157 unexpanded; 256). The writer is [unk]: there is no pacman or sudo record (the sudo window ends at 09:58, capture:75), and `.old` is still dated 09:03 (:107). So `default_entry: 2` (:127) is today's file, not the one Limine read.

**Holds [inf]:** the booted image. Kernel 7.2.11 with root `/@` (:5,14) rules out linux-lts and snapshot-2. Directory mtimes are 09:26:22 and 09:29:18 (:122,112), and the history copy is byte-equal to the UKI (:219).
**Unobserved:** the entry that booted. The cmdline is identical for `//linux` and `//linux-lts` (:131,136). The menu, editor and one-shot paths all bypass default_entry. Limine CONFIG.md v12.x (accessed 2026-10-20): "LoaderEntryOneShot request takes precedence over this option". In menu.c the index counts the expanded `/+Omarchy` row, so 2 = `//linux` [obs, source].
**Shadow config [unk]:** the firmware boots `\EFI\limine\limine_x64.efi` (pacman.log:1359), and Limine reads that directory's `limine.conf` before this one. `/boot/EFI/limine` was never listed.

**Next default boot differs if:** limine.conf is rewritten again, `remember_last_entry: yes` is set (lines 4–20 unread, :126), a one-shot entry or BootNext is set, or a UKI is rebuilt.
**Anomaly [unk]:** `/boot/loader` mtime is 09:57:10 (:108). That is 1 s after kernel start, before an interactive LUKS unlock could finish.

**Smallest correction:** relabel the verdict BOOTED-IMAGE-OBSERVED. Capture the efivars LoaderEntrySelected, LimineLastBootedEntry and LoaderInfo (bli.c; menu.c:2344), plus limine.conf in full and `/boot/EFI/limine`.
Axes: C1 depth, provenance.

Scope: executed=true
