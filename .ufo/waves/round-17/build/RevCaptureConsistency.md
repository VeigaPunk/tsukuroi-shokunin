# RevCaptureConsistency — internal consistency of boot-chain-capture.txt

Line refs are capture lines unless prefixed `conf:` (its limine.conf line numbers).

## Inconsistencies / unproven
**B1 (L126 vs L143,L147,L153)** — `cut -c1-200` is false. History path text alone is 151–155 chars, leaving ≤45 hash chars under a 200-char cut; 66–70 are printed, so those lines are ≥219 chars. Full-hash equality is therefore unproven for conf:50/56/64 (prefix-only: 70/66/70 chars, all matching).
**B2 (L106,L108)** — limine.conf 12:07:06 and `/boot/loader` 09:57:10 postdate boot start (L10); both freshness sweeps (L157-158, L256) exclude `/boot`. L157 `find boot-chain inputs …` is not a runnable command yet asserts rc=0; L255 mis-cites line 158; L256's literal `<same three trees>` makes 58674 unreproducible.
**B3 (L101)** — `/boot` mtime = epoch 0, unusable for ordering; all 13 `/boot` mtimes have even seconds ⇒ 2-s FAT resolution; `/boot` fstype never captured (L13 covers `/` only).
**B4 (L107)** — limine.conf.old 09:03:02 predates the 12:07:06 rewrite; that writer is unattributed (journal ends 09:58, L75).
**B5 (L154 vs L132/L136)** — snapshot-1 cmdline drops the cryptdevice options and adds `root=/d…`; every snapshot cmdline truncates before `rootflags`, so per-snapshot subvol is unverified.
**B6 gaps** — fallback entry (L155-156) has no hash and was never listed; `/boot/EFI` nlink 5 (L105) ⇒ ≥1 uninspected subdir; `default_entry: 2`→entry mapping is [inf]; no ESP free space.
**B7 (L6 vs L10)** — uptime 09:57:08 vs journal 09:57:09: 1 s rounding, benign.

## Holds
1. sha256=filename: 2e9c (L171=L115=L124), 2d49 (L187=L116=L125), 0f1e (L203=L114).
2. conf:30=full b2sum (L131/L172); conf:38=full b2sum (L135/L188) ⇒ loader hash checks pass.
3. Live ≡ snapshot-2: equal sha256+size (L124/L115 284439552; L125/L116 281318912), equal member hashes (L182-184/L230-232) — content, not inode.
4. init 62fcc3a9 + hooks eeac1ed/de852646 identical in all 5 images and on host (L251-253) ⇒ 41.1 and 42.2 both carry /new_root hooks; only init differs (9a25937d, L214).
5. "0 /new_root" (L175,191,223,239) is init-scoped: host init has exactly 7 `/sysroot` refs (L24-30) and 0 `/new_root`; hooks add 2 (L20-21, L179-180).
6. 5 kernel entries (L129,133,141,145,151) ↔ 4 distinct images ↔ 5 extract blocks (L170,186,202,218,234); no lts under snapshot-1 (installed 09:16:29, L46).
7. Dates/descriptions = snapper (L139/L166, L149/L167); ro=true both (L160-161).
8. `/proc/cmdline` (L12) = `//linux` prefix (L132); `rootflags=subvol=@` ⇒ current boot is live root.
9. nlink arithmetic: `/boot` 5 = 3 subdirs (L103,105,108); limine_history 2; EFI/Linux 2 ⇒ listings complete.

Scope: executed=none
