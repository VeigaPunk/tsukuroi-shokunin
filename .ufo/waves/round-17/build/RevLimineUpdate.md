# RevLimineUpdate — what `limine-update` did at 09:26

[obs] Journal: `sudo … COMMAND=/usr/bin/limine-update` at 09:26:11 (l1-capture/boot-chain-capture.txt:86); both UKIs rewritten 09:26:16 / 09:26:22 (:124-125); booted 09:57:09 (:10) via that path (:30).

1. limine-update:18 → `limine-install --no-efi-register`: deploys limine_x64.efi and EFI/BOOT fallback unless b2sum identical (/etc/default/limine:11, limine-install:540-542, :404-424, :448-467); no NVRAM write (:560).
2. limine-update:25 → `limine-mkinitcpio` (no args) → `echo rebuild | limine-mkinitcpio-install` (limine-mkinitcpio:26-27).
3. `rebuild` fails `pacman -Q rebuild` (limine-mkinitcpio-install:61) → `rebuild_all=true` (:95-96) → every `/usr/lib/modules/*/modules.builtin` (:103-107): 7.2.11 and 6.18.57-2-lts — every kernel.
4. `ENABLE_UKI=yes` (/etc/default/limine:8) → :296-297: cmdline via `--get-cmdline` (:158), build `/usr/bin/mkinitcpio --kernel … --uki /tmp/…` (:167-180), then `limine-entry-tool --add-uki` (:196-197) copies into /boot/EFI/Linux and rewrites `/boot/limine.conf` (same path logs `Updated: /boot/limine.conf`, pacman.log:3047), maintaining each entry's `#<BLAKE2b>` suffix (:30,38; `ENABLE_VERIFICATION=yes`, /etc/limine-entry-tool.conf:84).
5. Post hooks (:318); 90-limine-enroll-config cannot enroll — `load_config` blanks `ENABLE_ENROLL_LIMINE_CONFIG` (limine-common-functions:143-144).

No pacman.log line is possible: it records only libalpm transaction/hook events, and no hook Exec names limine-update (80-limine-efi-deploy.hook:14; /etc/pacman.d/hooks/90-mkinitcpio-install.hook:30). Log silent 09:18:26→09:27:39 (pacman.log:3064-3065); nested `pacman -Q/-Ql/-Qqo` queries emit nothing [inf].

[unk] Whether 09:26 bytes differ from 09:18 (same paths overwritten); embedded `.cmdline` unread. `/boot/limine.conf` mtime 12:07:06 (:106) postdates 09:26; `limine.conf.old` stayed 09:03:02 (:107) — 6 h backup threshold (/etc/limine-entry-tool.conf:87-91) suppressed a rollback copy [inf].

Scope: executed=grep -nE 'limine|mkinitcpio' /var/log/pacman.log, wc -l on limine scripts, sed -n '3060,3100p' /var/log/pacman.log
