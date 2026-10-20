# FxSentinelL0Advice — operator-advice safety (round 17)

**Boot-break: SURVIVES (low residual).** [obs] The SKILL.md:1872-1887 procedure, boot-chain-r17.md:109-120 and the l0-questions.md:61 correction advise no package, initramfs, bootloader or /boot action. [obs] Option (b) at l0-questions.md:60 (override the hooks with `/sysroot`, then `limine-update`) is still present. It is withdrawn only at :61 ("Option (b) … is NOT needed"). [inf] Running `limine-update` changes the UKI hash, which voids BOOTED-OBSERVED. Fix: mark :60 superseded in place.

**Privileged writes: SURVIVES.** [obs] boot-chain-audit.sh uses `sudo` in three places, all reads: `sudo -n cat` at :252 and :1245, `sudo -n stat` at :420. Its paths are fixed (:143-144, :226-227). It refuses to run as EUID 0 (:1212). `git diff --stat dd15c183` shows no worktree drift in tools/, SKILL.md or boot-chain-r17.md.

**Secret leak: FAILS (medium).** "Copy it off-disk" (boot-chain-r17.md:117; l0:61) says nothing about how to protect the copy. Debian man page cryptsetup-luksHeaderBackup(8), WARNING section (accessed 2026-10-20): "backup file and a passphrase valid at the time of backup allows decryption … even if the passphrase was later changed". [unk] The backup's existence and location are not captured. boot-chain-capture.txt:75-97 has no cryptsetup line. Fix: say to store it encrypted and offline, and to destroy it after any passphrase change.

[obs] The captures are tracked and on origin/master. They hold the PARTUUID and sudo journal lines but no key material.

Scope: executed=awk 'NR==60||NR==61' l0-questions.md,wc -l boot-chain-audit.sh,git ls-files,git remote -v,git check-ignore -v,git branch -r --contains,git diff --stat
