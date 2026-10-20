# Scout: limine-entry-tool README + boot-writer hooks (C2 source)

Paths below are under `.ufo/waves/round-19/l1-capture/` (read-only captures). Quote line = capture line.

## What writes `limine.conf`

- [obs] `host-capture-r19b.txt:1539` (limine-entry-tool README:225): "This tool generates boot entries only at `$ESP_PATH/limine.conf` and does not touch any other Limine config locations."
  Proposition: the entry tool's sole config write target is `$ESP_PATH/limine.conf`.
- [obs] `r19b:1516` (README:17): "It generates, updates, and removes boot entries with periodic `limine.conf` backups."
- [obs] `r19b:1526` (README:128): "This creates or updates an EFI entry to limine.conf."
- [obs] `r19b:187-188` (README:174-175): "**Tip:** After changing your config in `/etc/default/limine`, just run `limine-update` to apply the changes." / "It will rebuild your initramfs or UKI, similar to reinstalling the kernel."
- [obs] `r19b:179` (README:166): "2. Run `limine-update` to rebuild the initramfs."
  Proposition: entry add/update commands and `limine-update` are the regeneration entry points; `limine-update` is the documented config-apply path. `/usr/bin/limine-update` is a bash script (`host-capture-r19.txt:434`).

## Hook-driven regeneration (pacman)

- [obs] `r19b:1455-1458`: `/etc/pacman.d/hooks/90-mkinitcpio-install.hook` — "Description = Updating linux initcpios...", "When = PostTransaction", "Exec = /usr/share/libalpm/scripts/limine-mkinitcpio-install"; triggers at `r19b:1430-1454` (initcpio/firmware/modules paths, mkinitcpio package).
- [obs] `r19b:1509-1510`: grep of that script, line 27: `BOOT_PATH="$ESP_PATH"`.
  Proposition: pacman-time regeneration is PostTransaction through `limine-mkinitcpio-install`, which takes its target from `ESP_PATH`.
- [obs] `r19b:1700,1702` (pacman.log 3015, 3047): "[ALPM-SCRIPTLET] Updated: /boot/limine.conf", adjacent to "Copied: /tmp/limine-mkinitcpio.*/linux*.efi -> /boot/EFI/Linux/omarchy_*.efi" (`r19b:1699,1701`); also `r19b:1695` (pacman.log 2021).
- [inf] That scriptlet line is emitted by `limine-entry-tool` (or a wrapper invoking it) under `limine-mkinitcpio-install`; the script's own literal strings contain no `limine.conf` (grep at `r19b:1509` matched only line 27), so the exact internal call is not in the capture. [unk]

## Not the conf writer (rejected)

- [obs] `r19b:1427-1428`: `80-limine-efi-deploy.hook` — When = PostTransaction, "Exec = /usr/bin/limine-install"; README (`r19b:1518-1519`, `r19b:1543`) says limine-install copies `${ESP_PATH}/EFI/limine/limine_x64.efi` and overwrites `${ESP_PATH}/EFI/BOOT/BOOTX64.EFI`. [obs] `r19b:1469`: `99-limine.hook` Exec is `/bin/sh -c "/usr/bin/cp ... /boot/EFI/BOOT/..."` (hard-coded `/boot`, EFI files only).
- Rejected: attributing the two ALPM "Updated: /boot/limine.conf" lines to `limine-install` or `99-limine.hook`.

## limine-snapper-sync writer class

- [obs] `r19b:262` (snapper README:249): "This automation generates only the default at `$ESP_PATH/limine.conf` and does not touch any other Limine config locations."
- [obs] `r19b:249` (README:236): "Test running `limine-snapper-sync`. If successful, you should see: `Updated: $ESP_PATH/limine.conf`."
- [obs] `r19b:1685-1686`: `grep -c "Updated: /boot/limine.conf"` = 10; unit split at `host-capture-r19c.txt:11-20`.

## Where ESP_PATH comes from

- [obs] `host-capture-r19.txt:418-420`: `grep -v -E "^[[:space:]]*(#|$)" /etc/default/limine` -> `ESP_PATH="/boot"`.
- [obs] `r19b:331` (snapper README): "The config file is located at `/etc/default/limine` (**Recommend**) or alternatively at `/etc/limine-snapper-sync.conf`"; `r19b:335`: "`/etc/default/limine` takes precedence over `/etc/limine-snapper-sync.conf`."
- [obs] `r19b:1560` (entry-tool README:358): "### If not set, it is found automatically by checking /efi, /boot, /boot/efi, and /limine." Same template text at `r19b:369`.
- [obs] `r19b:1542` (README:260): "If your boot partition is not detected, create or edit `/etc/default/limine` and set `ESP_PATH=` to your FAT32 partition."
- Rejected: `/etc/limine-snapper-sync.conf` as the source — its effective dump (`r19.txt:412-416`) has no `ESP_PATH`.
- [unk] Contents of `/etc/limine-entry-tool.conf` (exists, package `%BACKUP%` entry: `r19.txt:84,131`) are not captured; a second ESP_PATH source cannot be excluded.

Scope note: leaf scout, no shell execution; all evidence from committed read-only captures.

Scope: executed=none
