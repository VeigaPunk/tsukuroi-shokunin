source: S212 in `corpus/SOURCES.md` — own-work capture only; no libalpm row cited
verified-at: 2026-10-26

# Control: cheap table

## Effective hook order (r38 capture)

| when | pos | name | dir | abort | needs | exec |
|---|---|---|---|---|---|---|
| PostTransaction | 1 | 10-glibc-locale-gen.hook | usr | no | no | `/usr/bin/locale-gen` |
| PreTransaction | 1 | 10-glibc-remove-locale-archive.hook | usr | no | no | `/usr/bin/rm` |
| PreTransaction | 2 | 10-limine-snapper-lock.hook | usr | no | yes | `/usr/share/libalpm/scripts/limine-snapper-lock` |
| PostTransaction | 2 | 10-linux-modules-post.hook | usr | no | no | `/bin/sh` |
| PreTransaction | 3 | 10-linux-modules-pre.hook | usr | no | no | `/bin/sh` |
| PreTransaction | 4 | 10-openssh-mark-sshd-for-restart.hook | usr | no | no | `/usr/bin/systemctl` |
| PostTransaction | 3 | 11-glibc-ldconfig.hook | usr | no | no | `/usr/bin/ldconfig` |
| PreTransaction | 5 | 11-glibc-remove-ldconfig-cache.hook | usr | no | no | `/usr/bin/rm` |
| PostTransaction | 4 | 12-glibc-iconvconfig.hook | usr | no | no | `/usr/bin/iconvconfig` |
| PreTransaction | 6 | 12-glibc-remove-iconvconfig-cache.hook | usr | no | no | `/usr/bin/rm` |
| PostTransaction | 5 | 12-lib32-glibc-iconvconfig.hook | usr | no | no | `/usr/bin/iconvconfig` |
| PreTransaction | 7 | 12-lib32-glibc-remove-iconvconfig-cache.hook | usr | no | no | `/usr/bin/rm` |
| PostTransaction | 6 | 20-systemd-sysusers.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PostTransaction | 7 | 21-systemd-tmpfiles.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PostTransaction | 8 | 25-systemd-binfmt.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PostTransaction | 9 | 25-systemd-catalog.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PostTransaction | 10 | 25-systemd-hwdb.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PostTransaction | 11 | 25-systemd-sysctl.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PostTransaction | 12 | 30-systemd-daemon-reload-system.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PostTransaction | 13 | 30-systemd-daemon-reload-user.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PostTransaction | 14 | 30-update-mime-database.hook | usr | no | no | `/usr/bin/env` |
| PostTransaction | 15 | 35-systemd-enqueue-marked.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PostTransaction | 16 | 35-systemd-udev-reload.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PostTransaction | 17 | 35-systemd-update.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PostTransaction | 18 | 36-systemd-modules-load.hook | usr | no | no | `/usr/bin/systemctl` |
| PostTransaction | 19 | 40-fontconfig-config.hook | usr | no | yes | `/usr/share/libalpm/scripts/40-fontconfig-config` |
| PostTransaction | 20 | 40-update-ca-trust.hook | usr | no | no | `/usr/bin/update-ca-trust` |
| PostTransaction | 21 | 60-depmod.hook | usr | no | yes | `/usr/share/libalpm/scripts/depmod` |
| PreTransaction | 8 | 60-limine-mkinitcpio-remove-pre.hook | usr | no | yes | `/usr/share/libalpm/scripts/limine-mkinitcpio-remove` |
| PreTransaction | 9 | 60-mkinitcpio-remove.hook | usr | no | yes | `/usr/share/libalpm/scripts/mkinitcpio` |
| PostTransaction | 22 | 70-dkms-install.hook | usr | no | yes | `/usr/share/libalpm/scripts/dkms` |
| PreTransaction | 10 | 70-dkms-upgrade.hook | usr | no | yes | `/usr/share/libalpm/scripts/dkms` |
| PostTransaction | 23 | 70-openssh-restart-sshd.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PreTransaction | 11 | 71-dkms-remove.hook | usr | no | yes | `/usr/share/libalpm/scripts/dkms` |
| PostTransaction | 24 | 80-limine-efi-deploy.hook | usr | no | no | `/usr/bin/limine-install` |
| PostTransaction | 25 | 90-limine-mkinitcpio-remove-post.hook | usr | no | no | `/usr/share/libalpm/scripts/limine-mkinitcpio-remove` |
| PostTransaction | 26 | 90-mkinitcpio-install.hook | etc | no | yes | `/usr/share/libalpm/scripts/limine-mkinitcpio-install` |
| PostTransaction | 27 | 90-update-appstream-cache.hook | usr | no | no | `/usr/bin/appstreamcli` |
| PostTransaction | 28 | 99-limine.hook | etc | no | no | `/bin/sh` |
| PostTransaction | 29 | dbus-reload.hook | usr | no | no | `/usr/share/libalpm/scripts/systemd-hook` |
| PostTransaction | 30 | dconf-update.hook | usr | no | yes | `/usr/share/libalpm/scripts/dconf-update` |
| PostTransaction | 31 | detect-old-perl-modules.hook | usr | no | no | `/usr/share/libalpm/scripts/detect-old-perl-modules.sh` |
| PostTransaction | 32 | fontconfig.hook | usr | no | no | `/usr/bin/fc-cache` |
| PostTransaction | 33 | fontconfig-32.hook | usr | no | no | `/usr/bin/fc-cache-32` |
| PostTransaction | 34 | gdk-pixbuf-query-loaders.hook | usr | no | no | `/usr/bin/gdk-pixbuf-query-loaders` |
| PreTransaction | 12 | gdk-pixbuf-remove-loaders-cache.hook | usr | no | no | `/usr/bin/rm` |
| PostTransaction | 35 | gio-querymodules.hook | usr | no | no | `/usr/bin/gio-querymodules` |
| PostTransaction | 36 | gio-querymodules-32.hook | usr | no | no | `/usr/bin/gio-querymodules-32` |
| PreTransaction | 13 | gio-remove-module-cache.hook | usr | no | no | `/usr/bin/rm` |
| PreTransaction | 14 | gio-remove-module-cache-32.hook | usr | no | no | `/usr/bin/rm` |
| PostTransaction | 37 | glib-compile-schemas.hook | usr | no | no | `/usr/bin/glib-compile-schemas` |
| PreTransaction | 15 | glib-remove-compiled-schemas.hook | usr | no | no | `/usr/bin/rm` |
| PostTransaction | 38 | gtk-query-immodules-3.0.hook | usr | no | no | `/usr/bin/gtk-query-immodules-3.0` |
| PreTransaction | 16 | gtk-remove-immodules-cache.hook | usr | no | no | `/usr/bin/rm` |
| PostTransaction | 39 | gtk-update-icon-cache.hook | usr | no | yes | `/usr/share/libalpm/scripts/gtk-update-icon-cache` |
| PostTransaction | 40 | gtk4-querymodules.hook | usr | no | yes | `/usr/share/libalpm/scripts/gtk4-querymodules` |
| PostTransaction | 41 | gvfsd.hook | usr | no | no | `/bin/sh` |
| PostTransaction | 42 | luarocks-make-manifest-5.1.hook | usr | no | no | `/usr/bin/luarocks-admin` |
| PostTransaction | 43 | luarocks-make-manifest-5.2.hook | usr | no | no | `/usr/bin/luarocks-admin` |
| PostTransaction | 44 | luarocks-make-manifest-5.3.hook | usr | no | no | `/usr/bin/luarocks-admin` |
| PostTransaction | 45 | luarocks-make-manifest-5.4.hook | usr | no | no | `/usr/bin/luarocks-admin` |
| PostTransaction | 46 | luarocks-make-manifest-5.5.hook | usr | no | no | `/usr/bin/luarocks-admin` |
| PostTransaction | 47 | man-db-remove-cache.hook | usr | no | no | `/usr/bin/rm` |
| PostTransaction | 48 | nvimdoc.hook | usr | no | no | `/usr/share/libalpm/scripts/nvimdoc` |
| PostTransaction | 49 | shared-mime-info-remove-cache.hook | usr | no | no | `/usr/bin/sh` |
| PostTransaction | 50 | texinfo-install.hook | usr | no | yes | `/bin/sh` |
| PreTransaction | 17 | texinfo-remove.hook | usr | no | yes | `/bin/sh` |
| PostTransaction | 51 | update-desktop-database.hook | usr | no | no | `/usr/bin/update-desktop-database` |
| PostTransaction | 52 | walker-restart.hook | etc | no | no | `/home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker` |

## Control notes

- [obs] table only; no rule text, no source reading.
