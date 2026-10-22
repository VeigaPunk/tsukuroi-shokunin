# pacman.log census — round-24 wave 1, seat ExecPacmanLogCensus

Source file: `/var/log/pacman.log` (read-only; no package transaction, sync,
service restart, cache write or configuration write was performed by this seat).

- Assigned read range: line 2463 to end of file (file has 3191 lines).
- Pause-window start (the marking boundary): **2026-10-20T09:40:00-0300**.
- `PRE-WINDOW` = record timestamp is earlier than 2026-10-20T09:40:00-0300.
- `POST-WINDOW` = record timestamp is at or after 2026-10-20T09:40:00-0300.
- The mado round-15 libinput incident that triggered the pause ruling is at
  2026-10-20T04:25:16-0300 (`/var/log/pacman.log:2429`), which is before the
  assigned read range; it is cited here only as the incident anchor and is
  listed in the context section below, not counted as an in-range row.
- One context line (`2462`) is listed separately because it sits one line above
  the assigned start and carries the operator's full-upgrade argv that the
  window boundary is defined against.

## Counts

| Measure | Value |
|---|---|
| `[PACMAN] Running` command lines in range 2463–3191 | 19 |
| ALPM installed records | 61 |
| ALPM upgraded records | 426 |
| ALPM downgraded records | 0 |
| ALPM removed records | 18 |
| Total ALPM package records in range | 505 |
| PRE-WINDOW package records | 500 |
| POST-WINDOW package records | 5 |
| ALPM transaction start/completed markers in range | 20 |

`downgraded` is zero across the whole file, not only in range: `grep -c downgraded
/var/log/pacman.log` exits 1 with no output. The two `reinstalled` records in the
file (lines 2359 and 2365, 2026-10-19T10:03) are outside the assigned range and
are not listed here.

## Section A — every `[PACMAN] Running` command line in range

| # | Log line | Timestamp (-0300) | Window | Operation class | Command line |
|---|---|---|---|---|---|
| A1 | 3064 | 2026-10-20T09:27:39-03:00 | PRE-WINDOW | install-from-repo | `pacman -S --needed --noconfirm fwupd` |
| A2 | 3085 | 2026-10-20T09:29:39-03:00 | PRE-WINDOW | install-from-repo | `pacman -S --noconfirm --config /etc/pacman.conf -- extra/go` |
| A3 | 3091 | 2026-10-20T09:29:40-03:00 | PRE-WINDOW | dependency-flag (no package change) | `pacman -D -q --asdeps --noconfirm --config /etc/pacman.conf -- go` |
| A4 | 3092 | 2026-10-20T09:31:03-03:00 | PRE-WINDOW | install-local-package | `pacman -U --noconfirm --config /etc/pacman.conf -- /home/vgpnk/.cache/yay/elephant/elephant-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant/elephant-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-clipboard/elephant-clipboard-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-clipboard/elephant-clipboard-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-runner/elephant-runner-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-runner/elephant-runner-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-calc/elephant-calc-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-calc/elephant-calc-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-providerlist/elephant-providerlist-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-providerlist/elephant-providerlist-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-symbols/elephant-symbols-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-symbols/elephant-symbols-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-files/elephant-files-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-files/elephant-files-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-websearch/elephant-websearch-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-websearch/elephant-websearch-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-desktopapplications/elephant-desktopapplications-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-desktopapplications/elephant-desktopapplications-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-bluetooth/elephant-bluetooth-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-bluetooth/elephant-bluetooth-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-unicode/elephant-unicode-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-unicode/elephant-unicode-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-todo/elephant-todo-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-todo/elephant-todo-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-menus/elephant-menus-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-menus/elephant-menus-debug-2.22.1-1-x86_64.pkg.tar.zst` |
| A5 | 3125 | 2026-10-20T09:31:04-03:00 | PRE-WINDOW | dependency-flag (no package change) | `pacman -D -q --asdeps --noconfirm --config /etc/pacman.conf -- elephant elephant-debug elephant-clipboard elephant-clipboard-debug elephant-runner elephant-runner-debug elephant-calc elephant-calc-debug elephant-providerlist elephant-providerlist-debug elephant-symbols elephant-symbols-debug elephant-files elephant-files-debug elephant-websearch elephant-websearch-debug elephant-desktopapplications elephant-desktopapplications-debug elephant-bluetooth elephant-bluetooth-debug elephant-unicode elephant-unicode-debug elephant-todo elephant-todo-debug elephant-menus elephant-menus-debug` |
| A6 | 3126 | 2026-10-20T09:31:04-03:00 | PRE-WINDOW | remove | `pacman -R -s -u --noconfirm --config /etc/pacman.conf -- go` |
| A7 | 3132 | 2026-10-20T09:38:33-03:00 | PRE-WINDOW | remove | `pacman -Rns --noconfirm btrbk elephant-bluetooth-debug elephant-calc-debug elephant-clipboard-debug elephant-debug elephant-desktopapplications-debug elephant-files-debug elephant-menus-debug elephant-providerlist-debug elephant-runner-debug elephant-symbols-debug elephant-todo-debug elephant-unicode-debug elephant-websearch-debug` |
| A8 | 3152 | 2026-10-20T09:39:21-03:00 | PRE-WINDOW | remove | `pacman -Rns --noconfirm gst-plugin-gtk hyprwayland-scanner webp-pixbuf-loader` |
| A9 | 3161 | 2026-10-20T13:23:08-03:00 | POST-WINDOW | install-local-package | `pacman -U --needed --noconfirm --config /etc/pacman.conf -- /home/vgpnk/.cache/yay/zcode/zcode-3.16.2-1-x86_64.pkg.tar.zst` |
| A10 | 3169 | 2026-10-20T13:23:09-03:00 | POST-WINDOW | dependency-flag (no package change) | `pacman -D -q --asexplicit --noconfirm --config /etc/pacman.conf -- zcode` |
| A11 | 3170 | 2026-10-21T17:55:56-03:00 | POST-WINDOW | install-local-package | `pacman -U --noconfirm --config /etc/pacman.conf -- /home/vgpnk/.cache/yay/tizen-sdb/tizen-sdb-2.3.2-3-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/tizen-sdb/tizen-sdb-debug-2.3.2-3-x86_64.pkg.tar.zst` |
| A12 | 3177 | 2026-10-21T17:55:56-03:00 | POST-WINDOW | dependency-flag (no package change) | `pacman -D --asdeps -q --noconfirm --config /etc/pacman.conf -- tizen-sdb-debug` |
| A13 | 3178 | 2026-10-21T17:55:56-03:00 | POST-WINDOW | dependency-flag (no package change) | `pacman -D -q --asexplicit --noconfirm --config /etc/pacman.conf -- tizen-sdb` |
| A14 | 3179 | 2026-10-21T18:07:37-03:00 | POST-WINDOW | install-local-package | `pacman -U --noconfirm --config /etc/pacman.conf -- /home/vgpnk/.cache/yay/openssl-1.0/openssl-1.0-1.0.2.u-7-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/openssl-1.0/openssl-1.0-debug-1.0.2.u-7-x86_64.pkg.tar.zst` |
| A15 | 3186 | 2026-10-21T18:07:37-03:00 | POST-WINDOW | dependency-flag (no package change) | `pacman -D -q --asdeps --noconfirm --config /etc/pacman.conf -- openssl-1.0-debug` |
| A16 | 3187 | 2026-10-21T18:07:37-03:00 | POST-WINDOW | dependency-flag (no package change) | `pacman -D -q --asexplicit --noconfirm --config /etc/pacman.conf -- openssl-1.0` |
| A17 | 3188 | 2026-10-21T20:32:00-03:00 | POST-WINDOW | sync-only (databases) | `pacman -Sy --noconfirm` |
| A18 | 3190 | 2026-10-22T04:10:08-03:00 | POST-WINDOW | cache-clean (all packages) | `pacman -Scc --noconfirm` |
| A19 | 3191 | 2026-10-22T04:10:19-03:00 | POST-WINDOW | cache-clean (all packages) | `pacman -Scc` |

Full untruncated argv for the two long lines (entries A4 at log line 3092 and
A5 at log line 3125):

**Line 3092** (entry A4, 2026-10-20T09:31:03-03:00):

```
pacman -U --noconfirm --config /etc/pacman.conf -- /home/vgpnk/.cache/yay/elephant/elephant-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant/elephant-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-clipboard/elephant-clipboard-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-clipboard/elephant-clipboard-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-runner/elephant-runner-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-runner/elephant-runner-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-calc/elephant-calc-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-calc/elephant-calc-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-providerlist/elephant-providerlist-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-providerlist/elephant-providerlist-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-symbols/elephant-symbols-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-symbols/elephant-symbols-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-files/elephant-files-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-files/elephant-files-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-websearch/elephant-websearch-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-websearch/elephant-websearch-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-desktopapplications/elephant-desktopapplications-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-desktopapplications/elephant-desktopapplications-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-bluetooth/elephant-bluetooth-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-bluetooth/elephant-bluetooth-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-unicode/elephant-unicode-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-unicode/elephant-unicode-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-todo/elephant-todo-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-todo/elephant-todo-debug-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-menus/elephant-menus-2.22.1-1-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/elephant-menus/elephant-menus-debug-2.22.1-1-x86_64.pkg.tar.zst
```

**Line 3125** (entry A5, 2026-10-20T09:31:04-03:00):

```
pacman -D -q --asdeps --noconfirm --config /etc/pacman.conf -- elephant elephant-debug elephant-clipboard elephant-clipboard-debug elephant-runner elephant-runner-debug elephant-calc elephant-calc-debug elephant-providerlist elephant-providerlist-debug elephant-symbols elephant-symbols-debug elephant-files elephant-files-debug elephant-websearch elephant-websearch-debug elephant-desktopapplications elephant-desktopapplications-debug elephant-bluetooth elephant-bluetooth-debug elephant-unicode elephant-unicode-debug elephant-todo elephant-todo-debug elephant-menus elephant-menus-debug
```

## Section B — every ALPM installed / upgraded / downgraded / removed record in range

| # | Log line | Timestamp (-0300) | Action | Package and version change | Window |
|---|---|---|---|---|---|
| B1 | 2480 | 2026-10-20T09:16:27-03:00 | upgraded | `tzdata (2026c-1 -> 2026e-1)` | PRE-WINDOW |
| B2 | 2481 | 2026-10-20T09:16:27-03:00 | upgraded | `glibc (2.44+r24+g16be1518495f-1 -> 2.44+r50+g1848099f063e-1)` | PRE-WINDOW |
| B3 | 2482 | 2026-10-20T09:16:27-03:00 | upgraded | `readline (8.3.003-1 -> 8.3.6-1)` | PRE-WINDOW |
| B4 | 2483 | 2026-10-20T09:16:27-03:00 | upgraded | `bash (5.3.15-1 -> 5.3.20-1)` | PRE-WINDOW |
| B5 | 2484 | 2026-10-20T09:16:27-03:00 | upgraded | `libgcrypt (1.12.3-1 -> 1.12.4-1)` | PRE-WINDOW |
| B6 | 2485 | 2026-10-20T09:16:27-03:00 | upgraded | `xz (5.8.3-1 -> 5.8.4-1)` | PRE-WINDOW |
| B7 | 2486 | 2026-10-20T09:16:27-03:00 | upgraded | `zlib (1:1.3.2-3 -> 1:1.3.2-4)` | PRE-WINDOW |
| B8 | 2487 | 2026-10-20T09:16:27-03:00 | upgraded | `systemd-libs (261.2-1 -> 262-1)` | PRE-WINDOW |
| B9 | 2488 | 2026-10-20T09:16:27-03:00 | upgraded | `sqlite (3.53.4-1 -> 3.54.0-1)` | PRE-WINDOW |
| B10 | 2489 | 2026-10-20T09:16:27-03:00 | upgraded | `util-linux-libs (2.42.3-1 -> 2.42.4-1)` | PRE-WINDOW |
| B11 | 2490 | 2026-10-20T09:16:28-03:00 | upgraded | `openssl (3.6.4-1 -> 3.6.5-1)` | PRE-WINDOW |
| B12 | 2491 | 2026-10-20T09:16:28-03:00 | upgraded | `libldap (2.6.13-1 -> 2.7.1-1)` | PRE-WINDOW |
| B13 | 2492 | 2026-10-20T09:16:28-03:00 | upgraded | `libtirpc (1.3.7-1 -> 1.3.8-1)` | PRE-WINDOW |
| B14 | 2493 | 2026-10-20T09:16:28-03:00 | upgraded | `libcap-ng (0.9.5-1 -> 0.9.6-1)` | PRE-WINDOW |
| B15 | 2494 | 2026-10-20T09:16:28-03:00 | upgraded | `pam (1.7.2-2 -> 1.7.3-1)` | PRE-WINDOW |
| B16 | 2495 | 2026-10-20T09:16:28-03:00 | upgraded | `coreutils (9.11-2 -> 9.12-2)` | PRE-WINDOW |
| B17 | 2496 | 2026-10-20T09:16:28-03:00 | upgraded | `util-linux (2.42.3-1 -> 2.42.4-1)` | PRE-WINDOW |
| B18 | 2497 | 2026-10-20T09:16:28-03:00 | installed | `nvme-cli (3.1-1)` | PRE-WINDOW |
| B19 | 2498 | 2026-10-20T09:16:28-03:00 | installed | `smartmontools (7.5-2)` | PRE-WINDOW |
| B20 | 2499 | 2026-10-20T09:16:28-03:00 | upgraded | `ca-certificates-mozilla (3.128-1 -> 3.131-1)` | PRE-WINDOW |
| B21 | 2500 | 2026-10-20T09:16:28-03:00 | upgraded | `leancrypto (1.8.0-1 -> 1.9.1-1)` | PRE-WINDOW |
| B22 | 2501 | 2026-10-20T09:16:28-03:00 | upgraded | `gnutls (3.8.13-2 -> 3.8.13-3)` | PRE-WINDOW |
| B23 | 2502 | 2026-10-20T09:16:28-03:00 | upgraded | `curl (8.22.0-1 -> 8.23.0-1)` | PRE-WINDOW |
| B24 | 2503 | 2026-10-20T09:16:28-03:00 | installed | `libaio (0.3.113-5)` | PRE-WINDOW |
| B25 | 2504 | 2026-10-20T09:16:28-03:00 | upgraded | `expat (2.8.4-1 -> 2.9.0-1)` | PRE-WINDOW |
| B26 | 2505 | 2026-10-20T09:16:28-03:00 | upgraded | `python (3.14.7-1 -> 3.14.8-1)` | PRE-WINDOW |
| B27 | 2506 | 2026-10-20T09:16:28-03:00 | upgraded | `fuse-common (3.18.2-1 -> 3.18.3-1)` | PRE-WINDOW |
| B28 | 2507 | 2026-10-20T09:16:28-03:00 | upgraded | `fuse3 (3.18.2-1 -> 3.18.3-1)` | PRE-WINDOW |
| B29 | 2508 | 2026-10-20T09:16:28-03:00 | installed | `liburcu (0.15.7-1)` | PRE-WINDOW |
| B30 | 2509 | 2026-10-20T09:16:28-03:00 | installed | `rpcbind (1.3.1-3)` | PRE-WINDOW |
| B31 | 2510 | 2026-10-20T09:16:28-03:00 | installed | `glusterfs (1:11.2-2)` | PRE-WINDOW |
| B32 | 2511 | 2026-10-20T09:16:28-03:00 | installed | `fio (3.42-1)` | PRE-WINDOW |
| B33 | 2512 | 2026-10-20T09:16:28-03:00 | upgraded | `device-mapper (2.03.42-1 -> 2.03.43-2)` | PRE-WINDOW |
| B34 | 2513 | 2026-10-20T09:16:28-03:00 | installed | `xfsprogs (7.2.0-1)` | PRE-WINDOW |
| B35 | 2514 | 2026-10-20T09:16:28-03:00 | installed | `earlyoom (1.9.0-1)` | PRE-WINDOW |
| B36 | 2515 | 2026-10-20T09:16:28-03:00 | installed | `iotop-c (1.31-1)` | PRE-WINDOW |
| B37 | 2516 | 2026-10-20T09:16:28-03:00 | installed | `sysstat (12.8.0-1)` | PRE-WINDOW |
| B38 | 2517 | 2026-10-20T09:16:28-03:00 | installed | `python-legacy-cgi (2.6.4-2)` | PRE-WINDOW |
| B39 | 2518 | 2026-10-20T09:16:28-03:00 | installed | `apparmor (4.1.7-1)` | PRE-WINDOW |
| B40 | 2519 | 2026-10-20T09:16:28-03:00 | installed | `judy (1.0.5-10)` | PRE-WINDOW |
| B41 | 2520 | 2026-10-20T09:16:28-03:00 | installed | `lksctp-tools (1.0.21-1)` | PRE-WINDOW |
| B42 | 2521 | 2026-10-20T09:16:28-03:00 | upgraded | `xxhash (0.8.3-1 -> 0.8.4-1)` | PRE-WINDOW |
| B43 | 2522 | 2026-10-20T09:16:28-03:00 | upgraded | `libmd (1.2.0-1 -> 1.3.0-1)` | PRE-WINDOW |
| B44 | 2523 | 2026-10-20T09:16:28-03:00 | installed | `stress-ng (0.22.01-1)` | PRE-WINDOW |
| B45 | 2524 | 2026-10-20T09:16:28-03:00 | upgraded | `perl (5.42.2-2 -> 5.42.3-1)` | PRE-WINDOW |
| B46 | 2525 | 2026-10-20T09:16:28-03:00 | installed | `btrbk (0.32.7-1)` | PRE-WINDOW |
| B47 | 2526 | 2026-10-20T09:16:28-03:00 | upgraded | `libarchive (3.8.9-1 -> 3.8.10-1)` | PRE-WINDOW |
| B48 | 2527 | 2026-10-20T09:16:28-03:00 | upgraded | `gzip (1.14-2 -> 1.15-1)` | PRE-WINDOW |
| B49 | 2528 | 2026-10-20T09:16:28-03:00 | upgraded | `cryptsetup (2.8.7-1 -> 2.8.8-1)` | PRE-WINDOW |
| B50 | 2529 | 2026-10-20T09:16:28-03:00 | upgraded | `hwdata (0.410-1 -> 0.412-1)` | PRE-WINDOW |
| B51 | 2530 | 2026-10-20T09:16:28-03:00 | upgraded | `pcre2 (10.48-1 -> 10.49-1)` | PRE-WINDOW |
| B52 | 2531 | 2026-10-20T09:16:28-03:00 | upgraded | `systemd (261.2-1 -> 262-1)` | PRE-WINDOW |
| B53 | 2539 | 2026-10-20T09:16:29-03:00 | upgraded | `mkinitcpio (41.1-1 -> 42.2-1)` | PRE-WINDOW |
| B54 | 2540 | 2026-10-20T09:16:29-03:00 | installed | `linux-lts (6.18.57-2)` | PRE-WINDOW |
| B55 | 2541 | 2026-10-20T09:16:29-03:00 | upgraded | `pahole (1:1.31-2 -> 1:1.32-1)` | PRE-WINDOW |
| B56 | 2542 | 2026-10-20T09:16:29-03:00 | installed | `linux-lts-headers (6.18.57-2)` | PRE-WINDOW |
| B57 | 2543 | 2026-10-20T09:16:29-03:00 | upgraded | `7zip (26.03-1 -> 26.04-1)` | PRE-WINDOW |
| B58 | 2544 | 2026-10-20T09:16:29-03:00 | upgraded | `adwaita-cursors (50.0-1 -> 51.0-1)` | PRE-WINDOW |
| B59 | 2545 | 2026-10-20T09:16:29-03:00 | upgraded | `adwaita-icon-theme (50.0-1 -> 51.0-1)` | PRE-WINDOW |
| B60 | 2546 | 2026-10-20T09:16:29-03:00 | upgraded | `alsa-card-profiles (1:1.6.8-1 -> 1:1.6.9-1)` | PRE-WINDOW |
| B61 | 2548 | 2026-10-20T09:16:29-03:00 | upgraded | `amd-ucode (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B62 | 2549 | 2026-10-20T09:16:29-03:00 | upgraded | `android-tools (37.0.0-5 -> 37.0.0.p1-1)` | PRE-WINDOW |
| B63 | 2550 | 2026-10-20T09:16:29-03:00 | upgraded | `aom (3.15.0-1 -> 3.15.2-1)` | PRE-WINDOW |
| B64 | 2551 | 2026-10-20T09:16:29-03:00 | upgraded | `libpng (1.6.58-2 -> 1.6.59-1)` | PRE-WINDOW |
| B65 | 2552 | 2026-10-20T09:16:29-03:00 | upgraded | `freetype2 (2.14.3-1 -> 2.15.0-1)` | PRE-WINDOW |
| B66 | 2553 | 2026-10-20T09:16:29-03:00 | upgraded | `libsysprof-capture (50.0-6 -> 51.0-1)` | PRE-WINDOW |
| B67 | 2554 | 2026-10-20T09:16:29-03:00 | upgraded | `glib2 (2.88.3-1 -> 2.90.1-1)` | PRE-WINDOW |
| B68 | 2555 | 2026-10-20T09:16:29-03:00 | upgraded | `xorgproto (2025.1-1 -> 2026.1-1)` | PRE-WINDOW |
| B69 | 2556 | 2026-10-20T09:16:29-03:00 | upgraded | `libx11 (1.8.13-1 -> 1.8.13-2)` | PRE-WINDOW |
| B70 | 2557 | 2026-10-20T09:16:29-03:00 | upgraded | `cairo (1.18.4-1 -> 1.18.6-1)` | PRE-WINDOW |
| B71 | 2558 | 2026-10-20T09:16:29-03:00 | upgraded | `bubblewrap (0.12.0-1 -> 0.13.1-1)` | PRE-WINDOW |
| B72 | 2559 | 2026-10-20T09:16:29-03:00 | upgraded | `jbigkit (2.1-8 -> 2.2-1)` | PRE-WINDOW |
| B73 | 2560 | 2026-10-20T09:16:29-03:00 | upgraded | `libtiff (4.7.2-1 -> 4.7.2-2)` | PRE-WINDOW |
| B74 | 2561 | 2026-10-20T09:16:29-03:00 | upgraded | `glycin (2.1.5-2 -> 2.2.3-1)` | PRE-WINDOW |
| B75 | 2562 | 2026-10-20T09:16:30-03:00 | upgraded | `gdk-pixbuf2 (2.44.7-1 -> 2.44.8-1)` | PRE-WINDOW |
| B76 | 2563 | 2026-10-20T09:16:30-03:00 | upgraded | `harfbuzz (14.4.0-1 -> 14.6.0-1)` | PRE-WINDOW |
| B77 | 2564 | 2026-10-20T09:16:30-03:00 | upgraded | `fribidi (1.0.16-2 -> 1.0.17-1)` | PRE-WINDOW |
| B78 | 2565 | 2026-10-20T09:16:30-03:00 | upgraded | `librsvg (2:2.62.3-1 -> 2:2.63.3-1)` | PRE-WINDOW |
| B79 | 2566 | 2026-10-20T09:16:30-03:00 | upgraded | `openjph (0.31.0-1 -> 0.32.0-1)` | PRE-WINDOW |
| B80 | 2567 | 2026-10-20T09:16:30-03:00 | upgraded | `openexr (3.4.15-1 -> 3.5.2-1)` | PRE-WINDOW |
| B81 | 2568 | 2026-10-20T09:16:30-03:00 | upgraded | `libvips (8.18.6-1 -> 8.18.7-1)` | PRE-WINDOW |
| B82 | 2569 | 2026-10-20T09:16:30-03:00 | upgraded | `hwloc (2.14.0-1 -> 2.15.0-1)` | PRE-WINDOW |
| B83 | 2570 | 2026-10-20T09:16:30-03:00 | upgraded | `appstream (1.2.0-1 -> 1.2.1-1)` | PRE-WINDOW |
| B84 | 2571 | 2026-10-20T09:16:30-03:00 | upgraded | `llvm-libs (22.1.8-2 -> 23.1.3-3)` | PRE-WINDOW |
| B85 | 2572 | 2026-10-20T09:16:30-03:00 | upgraded | `spirv-tools (1:1.4.357.0-1 -> 1:1.4.363.0-1)` | PRE-WINDOW |
| B86 | 2573 | 2026-10-20T09:16:30-03:00 | upgraded | `egl-wayland (4:1.1.22-1 -> 4:1.1.24-1)` | PRE-WINDOW |
| B87 | 2574 | 2026-10-20T09:16:30-03:00 | upgraded | `nvidia-utils (610.57.04-1 -> 615.78.08-1)` | PRE-WINDOW |
| B88 | 2575 | 2026-10-20T09:16:31-03:00 | upgraded | `mesa (1:26.2.2-1 -> 1:26.2.5-1)` | PRE-WINDOW |
| B89 | 2576 | 2026-10-20T09:16:31-03:00 | upgraded | `libevdev (1.13.7-1 -> 1.14.0-1)` | PRE-WINDOW |
| B90 | 2577 | 2026-10-20T09:16:31-03:00 | upgraded | `libwacom (2.19.1-1 -> 2.20.0-1)` | PRE-WINDOW |
| B91 | 2578 | 2026-10-20T09:16:31-03:00 | upgraded | `aquamarine (0.15.0-2 -> 0.15.1-1)` | PRE-WINDOW |
| B92 | 2579 | 2026-10-20T09:16:31-03:00 | upgraded | `libsecret (0.21.7-1 -> 0.21.8.2-1)` | PRE-WINDOW |
| B93 | 2580 | 2026-10-20T09:16:31-03:00 | upgraded | `pacman (7.1.0.r9.g54d9411-2 -> 7.1.0.r9.g54d9411-3)` | PRE-WINDOW |
| B94 | 2581 | 2026-10-20T09:16:31-03:00 | upgraded | `archlinux-keyring (20260902-1 -> 20260909-1)` | PRE-WINDOW |
| B95 | 2585 | 2026-10-20T09:16:32-03:00 | upgraded | `argon2 (20190702-6 -> 20190702-7)` | PRE-WINDOW |
| B96 | 2586 | 2026-10-20T09:16:32-03:00 | upgraded | `dconf (0.49.0-1 -> 51.0-1)` | PRE-WINDOW |
| B97 | 2587 | 2026-10-20T09:16:32-03:00 | upgraded | `gsettings-system-schemas (50.1-1 -> 51.0-1)` | PRE-WINDOW |
| B98 | 2588 | 2026-10-20T09:16:32-03:00 | upgraded | `gsettings-desktop-schemas (50.1-1 -> 51.0-1)` | PRE-WINDOW |
| B99 | 2589 | 2026-10-20T09:16:32-03:00 | upgraded | `at-spi2-core (2.60.6-1 -> 2.62.1-1)` | PRE-WINDOW |
| B100 | 2590 | 2026-10-20T09:16:32-03:00 | upgraded | `libcups (2:2.4.19-1 -> 2:2.4.20-1)` | PRE-WINDOW |
| B101 | 2591 | 2026-10-20T09:16:32-03:00 | upgraded | `md4c (0.5.3-1 -> 0.6.0-2)` | PRE-WINDOW |
| B102 | 2592 | 2026-10-20T09:16:32-03:00 | upgraded | `qt6-translations (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B103 | 2593 | 2026-10-20T09:16:32-03:00 | upgraded | `qt6-base (6.11.2-3 -> 6.12.0-3)` | PRE-WINDOW |
| B104 | 2594 | 2026-10-20T09:16:32-03:00 | upgraded | `attica (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B105 | 2595 | 2026-10-20T09:16:32-03:00 | upgraded | `automake (1.18.1-1 -> 1.19-1)` | PRE-WINDOW |
| B106 | 2596 | 2026-10-20T09:16:32-03:00 | upgraded | `oniguruma (6.9.10-1 -> 6.9.10-3)` | PRE-WINDOW |
| B107 | 2597 | 2026-10-20T09:16:32-03:00 | upgraded | `bat (0.26.1-2 -> 0.26.1-3)` | PRE-WINDOW |
| B108 | 2598 | 2026-10-20T09:16:32-03:00 | upgraded | `libpipewire (1:1.6.8-1 -> 1:1.6.9-1)` | PRE-WINDOW |
| B109 | 2599 | 2026-10-20T09:16:32-03:00 | upgraded | `pipewire (1:1.6.8-1 -> 1:1.6.9-1)` | PRE-WINDOW |
| B110 | 2600 | 2026-10-20T09:16:32-03:00 | upgraded | `libfdk-aac (2.0.3-2 -> 3.0.0-1)` | PRE-WINDOW |
| B111 | 2601 | 2026-10-20T09:16:32-03:00 | upgraded | `pipewire-audio (1:1.6.8-1 -> 1:1.6.9-1)` | PRE-WINDOW |
| B112 | 2602 | 2026-10-20T09:16:32-03:00 | upgraded | `libwireplumber (0.5.17-1 -> 0.5.18-1)` | PRE-WINDOW |
| B113 | 2603 | 2026-10-20T09:16:32-03:00 | upgraded | `wireplumber (0.5.17-1 -> 0.5.18-1)` | PRE-WINDOW |
| B114 | 2604 | 2026-10-20T09:16:32-03:00 | upgraded | `pipewire-jack (1:1.6.8-1 -> 1:1.6.9-1)` | PRE-WINDOW |
| B115 | 2605 | 2026-10-20T09:16:32-03:00 | upgraded | `vulkan-icd-loader (1.4.357.0-1 -> 1.4.363.0-1)` | PRE-WINDOW |
| B116 | 2606 | 2026-10-20T09:16:32-03:00 | upgraded | `glslang (1:1.4.357.0-1 -> 1:1.4.363.0-1)` | PRE-WINDOW |
| B117 | 2607 | 2026-10-20T09:16:32-03:00 | upgraded | `shaderc (2026.3-1 -> 2026.4-1)` | PRE-WINDOW |
| B118 | 2608 | 2026-10-20T09:16:32-03:00 | upgraded | `libplacebo (7.360.1-6 -> 7.360.1-7)` | PRE-WINDOW |
| B119 | 2609 | 2026-10-20T09:16:32-03:00 | upgraded | `sdl3 (3.4.16-1 -> 3.4.18-1)` | PRE-WINDOW |
| B120 | 2610 | 2026-10-20T09:16:32-03:00 | upgraded | `sdl2-compat (2.32.72-1 -> 2.32.74-1)` | PRE-WINDOW |
| B121 | 2611 | 2026-10-20T09:16:32-03:00 | upgraded | `snappy (1.2.2-3 -> 1.3.1-1)` | PRE-WINDOW |
| B122 | 2612 | 2026-10-20T09:16:32-03:00 | upgraded | `srt (1.5.7-1 -> 1.5.7-2)` | PRE-WINDOW |
| B123 | 2613 | 2026-10-20T09:16:32-03:00 | upgraded | `vapoursynth (79-1 -> 80-1)` | PRE-WINDOW |
| B124 | 2614 | 2026-10-20T09:16:32-03:00 | upgraded | `vmaf (3.2.0-1 -> 3.2.1-1)` | PRE-WINDOW |
| B125 | 2615 | 2026-10-20T09:16:32-03:00 | upgraded | `ffmpeg (2:9.0.1-4 -> 2:9.0.2-2)` | PRE-WINDOW |
| B126 | 2616 | 2026-10-20T09:16:32-03:00 | upgraded | `jemalloc (1:5.3.1-3 -> 1:5.4.0-1)` | PRE-WINDOW |
| B127 | 2617 | 2026-10-20T09:16:32-03:00 | upgraded | `opencolorio (2.5.1-1 -> 2.5.1-2)` | PRE-WINDOW |
| B128 | 2618 | 2026-10-20T09:16:32-03:00 | upgraded | `libde265 (1.1.2-1 -> 1.1.3-1)` | PRE-WINDOW |
| B129 | 2619 | 2026-10-20T09:16:32-03:00 | upgraded | `libheif (1.23.4-1 -> 1.23.6-1)` | PRE-WINDOW |
| B130 | 2620 | 2026-10-20T09:16:32-03:00 | upgraded | `openimageio (3.1.12.1-5 -> 3.1.12.1-7)` | PRE-WINDOW |
| B131 | 2621 | 2026-10-20T09:16:32-03:00 | installed | `llvm-lit (23.1.3-3)` | PRE-WINDOW |
| B132 | 2622 | 2026-10-20T09:16:33-03:00 | upgraded | `llvm (22.1.8-2 -> 23.1.3-3)` | PRE-WINDOW |
| B133 | 2623 | 2026-10-20T09:16:33-03:00 | upgraded | `compiler-rt (22.1.8-1 -> 23.1.3-3)` | PRE-WINDOW |
| B134 | 2624 | 2026-10-20T09:16:33-03:00 | upgraded | `clang (22.1.8-1 -> 23.1.3-3)` | PRE-WINDOW |
| B135 | 2625 | 2026-10-20T09:16:33-03:00 | upgraded | `openshadinglanguage (1.15.3.0-1 -> 1.15.7.0-1)` | PRE-WINDOW |
| B136 | 2626 | 2026-10-20T09:16:33-03:00 | upgraded | `python-cattrs (26.2.0-1 -> 26.2.1-1)` | PRE-WINDOW |
| B137 | 2627 | 2026-10-20T09:16:33-03:00 | upgraded | `python-numpy (2.5.3-1 -> 2.5.4-1)` | PRE-WINDOW |
| B138 | 2628 | 2026-10-20T09:16:33-03:00 | upgraded | `suitesparse (7.14.0-1 -> 7.14.1-1)` | PRE-WINDOW |
| B139 | 2629 | 2026-10-20T09:16:33-03:00 | upgraded | `nanobind (3.0.1-1 -> 3.1.0-1)` | PRE-WINDOW |
| B140 | 2630 | 2026-10-20T09:16:33-03:00 | upgraded | `python-more-itertools (11.1.0-1 -> 11.2.0-1)` | PRE-WINDOW |
| B141 | 2631 | 2026-10-20T09:16:33-03:00 | upgraded | `python-platformdirs (4.11.7-1 -> 4.13.0-1)` | PRE-WINDOW |
| B142 | 2632 | 2026-10-20T09:16:33-03:00 | upgraded | `glib-networking (1:2.80.1-1 -> 1:2.90.0-1)` | PRE-WINDOW |
| B143 | 2633 | 2026-10-20T09:16:33-03:00 | upgraded | `libsoup3 (3.6.6-2 -> 3.8.0-1)` | PRE-WINDOW |
| B144 | 2634 | 2026-10-20T09:16:33-03:00 | upgraded | `tinysparql (3.11.1-1 -> 3.12.0-1)` | PRE-WINDOW |
| B145 | 2635 | 2026-10-20T09:16:33-03:00 | upgraded | `gtk-update-icon-cache (1:4.22.4-1 -> 1:4.24.1-1)` | PRE-WINDOW |
| B146 | 2636 | 2026-10-20T09:16:33-03:00 | upgraded | `gstreamer (1.28.6-3 -> 1.28.8-1)` | PRE-WINDOW |
| B147 | 2637 | 2026-10-20T09:16:33-03:00 | upgraded | `orc (0.4.43-1 -> 0.4.44-1)` | PRE-WINDOW |
| B148 | 2638 | 2026-10-20T09:16:33-03:00 | upgraded | `gst-plugins-base-libs (1.28.6-3 -> 1.28.8-1)` | PRE-WINDOW |
| B149 | 2639 | 2026-10-20T09:16:33-03:00 | upgraded | `gst-plugins-bad-libs (1.28.6-3 -> 1.28.8-1)` | PRE-WINDOW |
| B150 | 2640 | 2026-10-20T09:16:33-03:00 | upgraded | `gtk3 (1:3.24.52-1 -> 1:3.24.52-2)` | PRE-WINDOW |
| B151 | 2641 | 2026-10-20T09:16:33-03:00 | upgraded | `gtk4 (1:4.22.4-1 -> 1:4.24.1-1)` | PRE-WINDOW |
| B152 | 2642 | 2026-10-20T09:16:33-03:00 | installed | `ministream (0.99.1-1)` | PRE-WINDOW |
| B153 | 2643 | 2026-10-20T09:16:33-03:00 | upgraded | `libadwaita (1:1.9.3-1 -> 1:1.10.0-1)` | PRE-WINDOW |
| B154 | 2644 | 2026-10-20T09:16:33-03:00 | upgraded | `python-idna (3.19-1 -> 3.20-1)` | PRE-WINDOW |
| B155 | 2645 | 2026-10-20T09:16:33-03:00 | upgraded | `python-urllib3 (2.7.0-1 -> 2.8.0-1)` | PRE-WINDOW |
| B156 | 2646 | 2026-10-20T09:16:34-03:00 | upgraded | `qt6-declarative (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B157 | 2647 | 2026-10-20T09:16:34-03:00 | upgraded | `shiboken6 (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B158 | 2648 | 2026-10-20T09:16:34-03:00 | upgraded | `pyside6 (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B159 | 2649 | 2026-10-20T09:16:34-03:00 | upgraded | `python-markupsafe (3.0.3-1 -> 3.0.4-1)` | PRE-WINDOW |
| B160 | 2650 | 2026-10-20T09:16:34-03:00 | upgraded | `blender (17:5.2.1-2 -> 17:5.2.2-3)` | PRE-WINDOW |
| B161 | 2651 | 2026-10-20T09:16:34-03:00 | upgraded | `bluetui (0.8.1-2 -> 0.8.2-1)` | PRE-WINDOW |
| B162 | 2652 | 2026-10-20T09:16:35-03:00 | upgraded | `breeze-icons (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B163 | 2653 | 2026-10-20T09:16:35-03:00 | upgraded | `nss (3.128-1 -> 3.131-1)` | PRE-WINDOW |
| B164 | 2654 | 2026-10-20T09:16:35-03:00 | upgraded | `minizip (1:1.3.2-3 -> 1:1.3.2-4)` | PRE-WINDOW |
| B165 | 2655 | 2026-10-20T09:16:36-03:00 | upgraded | `chromium (152.0.7977.82-1 -> 154.0.8037.97-1)` | PRE-WINDOW |
| B166 | 2656 | 2026-10-20T09:16:36-03:00 | upgraded | `libwbclient (2:4.24.6-1 -> 2:4.25.0-1)` | PRE-WINDOW |
| B167 | 2657 | 2026-10-20T09:16:36-03:00 | upgraded | `talloc (2.5.0-1 -> 2.5.0-2)` | PRE-WINDOW |
| B168 | 2658 | 2026-10-20T09:16:36-03:00 | upgraded | `cifs-utils (7.5-1 -> 7.9-1)` | PRE-WINDOW |
| B169 | 2659 | 2026-10-20T09:16:36-03:00 | upgraded | `claude-code (2.1.302-1 -> 2.1.304-1)` | PRE-WINDOW |
| B170 | 2660 | 2026-10-20T09:16:36-03:00 | upgraded | `runc (1.5.1-1 -> 1.5.2-1)` | PRE-WINDOW |
| B171 | 2661 | 2026-10-20T09:16:36-03:00 | upgraded | `containerd (2.3.5-1 -> 2.4.2-1)` | PRE-WINDOW |
| B172 | 2662 | 2026-10-20T09:16:36-03:00 | upgraded | `libcupsfilters (2.2.1-2 -> 2.2.1.r32.gd49e9284-1)` | PRE-WINDOW |
| B173 | 2663 | 2026-10-20T09:16:36-03:00 | upgraded | `cups-filters (2.0.1-2 -> 2.0.1-3)` | PRE-WINDOW |
| B174 | 2664 | 2026-10-20T09:16:36-03:00 | upgraded | `cups (2:2.4.19-1 -> 2:2.4.20-1)` | PRE-WINDOW |
| B175 | 2665 | 2026-10-20T09:16:36-03:00 | upgraded | `deno (2.9.6-1 -> 2.9.7-2)` | PRE-WINDOW |
| B176 | 2666 | 2026-10-20T09:16:36-03:00 | upgraded | `dkms (3.4.3-2 -> 3.4.4-1)` | PRE-WINDOW |
| B177 | 2667 | 2026-10-20T09:16:36-03:00 | upgraded | `libpcap (1.10.6-1 -> 1.11.0-1)` | PRE-WINDOW |
| B178 | 2668 | 2026-10-20T09:16:36-03:00 | upgraded | `docker (1:29.7.2-1 -> 1:29.9.1-1)` | PRE-WINDOW |
| B179 | 2669 | 2026-10-20T09:16:36-03:00 | upgraded | `docker-buildx (0.37.0-1 -> 0.38.0-1)` | PRE-WINDOW |
| B180 | 2670 | 2026-10-20T09:16:36-03:00 | upgraded | `docker-compose (5.5.1-1 -> 5.6.0-1)` | PRE-WINDOW |
| B181 | 2671 | 2026-10-20T09:16:36-03:00 | upgraded | `dotnet-host (10.0.11.sdk111-1 -> 10.0.13.sdk113-1)` | PRE-WINDOW |
| B182 | 2672 | 2026-10-20T09:16:37-03:00 | upgraded | `dotnet-runtime-10.0 (10.0.11.sdk111-1 -> 10.0.13.sdk113-1)` | PRE-WINDOW |
| B183 | 2673 | 2026-10-20T09:16:37-03:00 | upgraded | `dotnet-runtime-9.0 (9.0.19.sdk120-1 -> 9.0.21.sdk122-1)` | PRE-WINDOW |
| B184 | 2674 | 2026-10-20T09:16:37-03:00 | upgraded | `dust (1.2.5-1 -> 1.2.6-1)` | PRE-WINDOW |
| B185 | 2675 | 2026-10-20T09:16:37-03:00 | upgraded | `electron43 (43.6.0-1 -> 43.7.11-2)` | PRE-WINDOW |
| B186 | 2676 | 2026-10-20T09:16:37-03:00 | upgraded | `gnome-desktop-common (1:44.5-1 -> 1:51.0-1)` | PRE-WINDOW |
| B187 | 2677 | 2026-10-20T09:16:37-03:00 | upgraded | `gnome-desktop (1:44.5-1 -> 1:51.0-1)` | PRE-WINDOW |
| B188 | 2678 | 2026-10-20T09:16:37-03:00 | upgraded | `gspell (1.14.4-1 -> 1.14.5-1)` | PRE-WINDOW |
| B189 | 2679 | 2026-10-20T09:16:37-03:00 | upgraded | `openssh (10.5p1-1 -> 10.6p1-2)` | PRE-WINDOW |
| B190 | 2680 | 2026-10-20T09:16:37-03:00 | upgraded | `gcr-4 (4.4.0.1-1 -> 4.4.1-1)` | PRE-WINDOW |
| B191 | 2681 | 2026-10-20T09:16:37-03:00 | upgraded | `parted (3.7-1 -> 3.8-1)` | PRE-WINDOW |
| B192 | 2682 | 2026-10-20T09:16:37-03:00 | upgraded | `gvfs (1.60.2-4 -> 1.62.0-3)` | PRE-WINDOW |
| B193 | 2683 | 2026-10-20T09:16:37-03:00 | upgraded | `ghostscript (10.07.1-1 -> 10.08.0-1)` | PRE-WINDOW |
| B194 | 2684 | 2026-10-20T09:16:37-03:00 | upgraded | `evince (1:48.4-1 -> 1:48.4-2)` | PRE-WINDOW |
| B195 | 2685 | 2026-10-20T09:16:37-03:00 | upgraded | `yyjson (0.12.0-1 -> 0.13.0-1)` | PRE-WINDOW |
| B196 | 2686 | 2026-10-20T09:16:37-03:00 | upgraded | `fastfetch (2.68.1-1 -> 2.70.0-1)` | PRE-WINDOW |
| B197 | 2687 | 2026-10-20T09:16:37-03:00 | upgraded | `fcitx5 (5.1.22-1 -> 5.1.23-1)` | PRE-WINDOW |
| B198 | 2688 | 2026-10-20T09:16:37-03:00 | upgraded | `fcitx5-qt (5.1.15-1 -> 5.1.16-2)` | PRE-WINDOW |
| B199 | 2689 | 2026-10-20T09:16:37-03:00 | upgraded | `fluidsynth (2.6.0-1 -> 2.6.1-1)` | PRE-WINDOW |
| B200 | 2690 | 2026-10-20T09:16:37-03:00 | upgraded | `freerdp (2:3.31.1-1 -> 2:3.32.2-1)` | PRE-WINDOW |
| B201 | 2691 | 2026-10-20T09:16:37-03:00 | upgraded | `gst-plugins-base (1.28.6-3 -> 1.28.8-1)` | PRE-WINDOW |
| B202 | 2692 | 2026-10-20T09:16:37-03:00 | upgraded | `verdict (1.4.5-2 -> 1.4.5-3)` | PRE-WINDOW |
| B203 | 2693 | 2026-10-20T09:16:37-03:00 | upgraded | `opencv (5.0.0-9 -> 5.0.0-13)` | PRE-WINDOW |
| B204 | 2694 | 2026-10-20T09:16:37-03:00 | upgraded | `frei0r-plugins (3.5.0-1 -> 3.6.0-1)` | PRE-WINDOW |
| B205 | 2695 | 2026-10-20T09:16:37-03:00 | upgraded | `fzf (0.74.3-1 -> 0.74.5-1)` | PRE-WINDOW |
| B206 | 2696 | 2026-10-20T09:16:37-03:00 | upgraded | `gdb-common (17.2-1 -> 18.1-1)` | PRE-WINDOW |
| B207 | 2697 | 2026-10-20T09:16:37-03:00 | upgraded | `gdb (17.2-1 -> 18.1-1)` | PRE-WINDOW |
| B208 | 2698 | 2026-10-20T09:16:37-03:00 | upgraded | `git (2.55.0-1 -> 2.56.0-1)` | PRE-WINDOW |
| B209 | 2699 | 2026-10-20T09:16:37-03:00 | upgraded | `github-cli (2.100.0-1 -> 2.102.0-1)` | PRE-WINDOW |
| B210 | 2700 | 2026-10-20T09:16:38-03:00 | upgraded | `js140 (140.15.0-1 -> 140.17.0-1)` | PRE-WINDOW |
| B211 | 2701 | 2026-10-20T09:16:38-03:00 | upgraded | `gjs (2:1.88.1-1 -> 2:1.90.1-1)` | PRE-WINDOW |
| B212 | 2702 | 2026-10-20T09:16:38-03:00 | upgraded | `glycin-gtk4 (2.1.5-2 -> 2.2.3-1)` | PRE-WINDOW |
| B213 | 2703 | 2026-10-20T09:16:38-03:00 | upgraded | `gtksourceview5 (5.20.0-1 -> 5.22.0-1)` | PRE-WINDOW |
| B214 | 2704 | 2026-10-20T09:16:38-03:00 | upgraded | `gnome-calculator (50.0-1 -> 51.1-1)` | PRE-WINDOW |
| B215 | 2705 | 2026-10-20T09:16:38-03:00 | upgraded | `gnome-desktop-4 (1:44.5-1 -> 1:51.0-1)` | PRE-WINDOW |
| B216 | 2706 | 2026-10-20T09:16:38-03:00 | upgraded | `gnome-keyring (1:50.0-1 -> 1:51.1-1)` | PRE-WINDOW |
| B217 | 2707 | 2026-10-20T09:16:38-03:00 | upgraded | `libsquish (1.15-8 -> 1.15-9)` | PRE-WINDOW |
| B218 | 2708 | 2026-10-20T09:16:38-03:00 | upgraded | `godot (4.7.2-1 -> 4.7.2-2)` | PRE-WINDOW |
| B219 | 2709 | 2026-10-20T09:16:38-03:00 | upgraded | `gpm (1.20.7.r38.ge82d1a6-6 -> 1.20.7.r38.ge82d1a6-7)` | PRE-WINDOW |
| B220 | 2710 | 2026-10-20T09:16:38-03:00 | upgraded | `gpu-screen-recorder (6.1.0-1 -> 6.1.4-1)` | PRE-WINDOW |
| B221 | 2711 | 2026-10-20T09:16:38-03:00 | upgraded | `graphicsmagick (1.3.48-1 -> 1.3.49-2)` | PRE-WINDOW |
| B222 | 2712 | 2026-10-20T09:16:38-03:00 | upgraded | `groff (1.24.1-1 -> 1.24.2-1)` | PRE-WINDOW |
| B223 | 2713 | 2026-10-20T09:16:38-03:00 | upgraded | `gst-libav (1.28.6-3 -> 1.28.8-1)` | PRE-WINDOW |
| B224 | 2714 | 2026-10-20T09:16:38-03:00 | upgraded | `gst-plugin-gtk (1.28.6-3 -> 1.28.8-1)` | PRE-WINDOW |
| B225 | 2715 | 2026-10-20T09:16:38-03:00 | upgraded | `gst-plugin-pipewire (1:1.6.8-1 -> 1:1.6.9-1)` | PRE-WINDOW |
| B226 | 2716 | 2026-10-20T09:16:38-03:00 | upgraded | `gst-plugins-good (1.28.6-3 -> 1.28.8-1)` | PRE-WINDOW |
| B227 | 2717 | 2026-10-20T09:16:38-03:00 | upgraded | `gum (2.0.0-1 -> 2.0.2-1)` | PRE-WINDOW |
| B228 | 2718 | 2026-10-20T09:16:38-03:00 | upgraded | `gvfs-mtp (1.60.2-4 -> 1.62.0-3)` | PRE-WINDOW |
| B229 | 2719 | 2026-10-20T09:16:38-03:00 | upgraded | `libnfs (6.0.2-5 -> 7.0.2-2)` | PRE-WINDOW |
| B230 | 2720 | 2026-10-20T09:16:38-03:00 | upgraded | `gvfs-nfs (1.60.2-4 -> 1.62.0-3)` | PRE-WINDOW |
| B231 | 2721 | 2026-10-20T09:16:38-03:00 | upgraded | `tevent (1:0.17.2-1 -> 1:0.17.2-2)` | PRE-WINDOW |
| B232 | 2722 | 2026-10-20T09:16:38-03:00 | upgraded | `tdb (1.4.15-1 -> 1.4.15-2)` | PRE-WINDOW |
| B233 | 2723 | 2026-10-20T09:16:38-03:00 | upgraded | `ldb (2:4.24.6-1 -> 2:4.25.0-1)` | PRE-WINDOW |
| B234 | 2724 | 2026-10-20T09:16:38-03:00 | upgraded | `smbclient (2:4.24.6-1 -> 2:4.25.0-1)` | PRE-WINDOW |
| B235 | 2725 | 2026-10-20T09:16:38-03:00 | upgraded | `gvfs-smb (1.60.2-4 -> 1.62.0-3)` | PRE-WINDOW |
| B236 | 2726 | 2026-10-20T09:16:38-03:00 | upgraded | `harfbuzz-icu (14.4.0-1 -> 14.6.0-1)` | PRE-WINDOW |
| B237 | 2727 | 2026-10-20T09:16:38-03:00 | upgraded | `hunspell (1.7.3-1 -> 1.7.5-1)` | PRE-WINDOW |
| B238 | 2728 | 2026-10-20T09:16:38-03:00 | upgraded | `iniparser (4.2.6-2 -> 4.3.2-1)` | PRE-WINDOW |
| B239 | 2729 | 2026-10-20T09:16:38-03:00 | upgraded | `hyprtoolkit (0.5.4-5 -> 0.6.0-1)` | PRE-WINDOW |
| B240 | 2730 | 2026-10-20T09:16:38-03:00 | upgraded | `hyprland-guiutils (0.2.2-3 -> 0.2.2-4)` | PRE-WINDOW |
| B241 | 2731 | 2026-10-20T09:16:38-03:00 | upgraded | `xorg-server-common (21.1.24-1 -> 21.1.25-2)` | PRE-WINDOW |
| B242 | 2732 | 2026-10-20T09:16:38-03:00 | upgraded | `xorg-xwayland (24.1.13-1 -> 24.1.14-1)` | PRE-WINDOW |
| B243 | 2733 | 2026-10-20T09:16:38-03:00 | upgraded | `hyprland (0.56.2-2 -> 0.56.2-4)` | PRE-WINDOW |
| B244 | 2734 | 2026-10-20T09:16:38-03:00 | upgraded | `lib32-glibc (2.44+r24+g16be1518495f-1 -> 2.44+r50+g1848099f063e-1)` | PRE-WINDOW |
| B245 | 2735 | 2026-10-20T09:16:38-03:00 | upgraded | `lib32-util-linux (2.42.3-1 -> 2.42.4-1)` | PRE-WINDOW |
| B246 | 2736 | 2026-10-20T09:16:38-03:00 | upgraded | `hyprland-preview-share-picker (0.2.1-1 -> 0.2.1-3)` | PRE-WINDOW |
| B247 | 2737 | 2026-10-20T09:16:38-03:00 | upgraded | `imagemagick (7.1.2.31-1 -> 7.1.2.34-1)` | PRE-WINDOW |
| B248 | 2738 | 2026-10-20T09:16:38-03:00 | upgraded | `iwd (3.12-1 -> 3.12-2)` | PRE-WINDOW |
| B249 | 2739 | 2026-10-20T09:16:38-03:00 | upgraded | `kconfig (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B250 | 2740 | 2026-10-20T09:16:38-03:00 | upgraded | `kcodecs (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B251 | 2741 | 2026-10-20T09:16:38-03:00 | upgraded | `kguiaddons (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B252 | 2742 | 2026-10-20T09:16:38-03:00 | upgraded | `ki18n (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B253 | 2743 | 2026-10-20T09:16:38-03:00 | upgraded | `kcolorscheme (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B254 | 2744 | 2026-10-20T09:16:38-03:00 | upgraded | `kcoreaddons (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B255 | 2745 | 2026-10-20T09:16:38-03:00 | upgraded | `kwidgetsaddons (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B256 | 2746 | 2026-10-20T09:16:38-03:00 | upgraded | `kconfigwidgets (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B257 | 2747 | 2026-10-20T09:16:38-03:00 | upgraded | `karchive (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B258 | 2748 | 2026-10-20T09:16:38-03:00 | upgraded | `kbookmarks (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B259 | 2749 | 2026-10-20T09:16:38-03:00 | upgraded | `kcompletion (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B260 | 2750 | 2026-10-20T09:16:38-03:00 | upgraded | `kcrash (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B261 | 2751 | 2026-10-20T09:16:38-03:00 | upgraded | `kdbusaddons (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B262 | 2752 | 2026-10-20T09:16:38-03:00 | upgraded | `qt6-svg (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B263 | 2753 | 2026-10-20T09:16:38-03:00 | upgraded | `kiconthemes (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B264 | 2754 | 2026-10-20T09:16:38-03:00 | upgraded | `kitemviews (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B265 | 2755 | 2026-10-20T09:16:38-03:00 | upgraded | `knotifications (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B266 | 2756 | 2026-10-20T09:16:38-03:00 | upgraded | `kjobwidgets (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B267 | 2757 | 2026-10-20T09:16:38-03:00 | upgraded | `kservice (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B268 | 2758 | 2026-10-20T09:16:38-03:00 | upgraded | `kwindowsystem (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B269 | 2759 | 2026-10-20T09:16:38-03:00 | upgraded | `qt6-shadertools (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B270 | 2760 | 2026-10-20T09:16:38-03:00 | upgraded | `qt6-5compat (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B271 | 2761 | 2026-10-20T09:16:38-03:00 | upgraded | `kwallet (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B272 | 2762 | 2026-10-20T09:16:38-03:00 | upgraded | `upower (1.91.3-1 -> 1.91.5-1)` | PRE-WINDOW |
| B273 | 2763 | 2026-10-20T09:16:38-03:00 | upgraded | `solid (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B274 | 2764 | 2026-10-20T09:16:38-03:00 | upgraded | `kio (6.29.0-2 -> 6.31.0-1)` | PRE-WINDOW |
| B275 | 2765 | 2026-10-20T09:16:39-03:00 | upgraded | `kirigami (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B276 | 2766 | 2026-10-20T09:16:39-03:00 | upgraded | `kglobalaccel (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B277 | 2767 | 2026-10-20T09:16:39-03:00 | upgraded | `kxmlgui (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B278 | 2768 | 2026-10-20T09:16:39-03:00 | upgraded | `kcmutils (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B279 | 2769 | 2026-10-20T09:16:39-03:00 | upgraded | `signon-kwallet-extension (26.08.0-1 -> 26.08.2-1)` | PRE-WINDOW |
| B280 | 2770 | 2026-10-20T09:16:39-03:00 | upgraded | `noto-fonts (1:2026.09.01-1 -> 1:2026.10.01-1)` | PRE-WINDOW |
| B281 | 2771 | 2026-10-20T09:16:39-03:00 | upgraded | `qt6-positioning (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B282 | 2772 | 2026-10-20T09:16:39-03:00 | upgraded | `qt6-webchannel (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B283 | 2773 | 2026-10-20T09:16:39-03:00 | upgraded | `qt6-webengine (6.11.2-1 -> 6.11.2-2)` | PRE-WINDOW |
| B284 | 2774 | 2026-10-20T09:16:39-03:00 | upgraded | `kaccounts-integration (26.08.0-1 -> 26.08.2-1)` | PRE-WINDOW |
| B285 | 2775 | 2026-10-20T09:16:39-03:00 | upgraded | `kfilemetadata (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B286 | 2776 | 2026-10-20T09:16:39-03:00 | upgraded | `kpackage (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B287 | 2777 | 2026-10-20T09:16:39-03:00 | upgraded | `syndication (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B288 | 2778 | 2026-10-20T09:16:39-03:00 | upgraded | `knewstuff (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B289 | 2779 | 2026-10-20T09:16:39-03:00 | upgraded | `knotifyconfig (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B290 | 2780 | 2026-10-20T09:16:39-03:00 | upgraded | `qt6-multimedia-ffmpeg (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B291 | 2781 | 2026-10-20T09:16:39-03:00 | upgraded | `qt6-multimedia (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B292 | 2782 | 2026-10-20T09:16:39-03:00 | upgraded | `qt6-speech (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B293 | 2783 | 2026-10-20T09:16:39-03:00 | upgraded | `sonnet (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B294 | 2784 | 2026-10-20T09:16:39-03:00 | upgraded | `ktextwidgets (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B295 | 2785 | 2026-10-20T09:16:39-03:00 | upgraded | `mlt (7.40.0-3 -> 7.42.0-1)` | PRE-WINDOW |
| B296 | 2786 | 2026-10-20T09:16:39-03:00 | upgraded | `kitemmodels (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B297 | 2787 | 2026-10-20T09:16:39-03:00 | upgraded | `purpose (6.29.0-1 -> 6.31.0-1)` | PRE-WINDOW |
| B298 | 2788 | 2026-10-20T09:16:39-03:00 | upgraded | `qqc2-desktop-style (6.29.0-2 -> 6.31.0-1)` | PRE-WINDOW |
| B299 | 2789 | 2026-10-20T09:16:39-03:00 | upgraded | `qt6-networkauth (6.11.2-1 -> 6.12.0-1)` | PRE-WINDOW |
| B300 | 2790 | 2026-10-20T09:16:39-03:00 | upgraded | `kdenlive (26.08.0-1 -> 26.08.2-1)` | PRE-WINDOW |
| B301 | 2791 | 2026-10-20T09:16:39-03:00 | upgraded | `libkdcraw (26.08.0-1 -> 26.08.2-1)` | PRE-WINDOW |
| B302 | 2792 | 2026-10-20T09:16:39-03:00 | upgraded | `krita (6.0.3-2 -> 6.0.4.1-1)` | PRE-WINDOW |
| B303 | 2793 | 2026-10-20T09:16:39-03:00 | upgraded | `lazygit (0.65.0-1 -> 0.66.2-1)` | PRE-WINDOW |
| B304 | 2794 | 2026-10-20T09:16:39-03:00 | upgraded | `less (1:704-1 -> 1:710-1)` | PRE-WINDOW |
| B305 | 2795 | 2026-10-20T09:16:39-03:00 | upgraded | `lib32-openssl (1:3.6.4-1 -> 1:3.6.5-1)` | PRE-WINDOW |
| B306 | 2796 | 2026-10-20T09:16:39-03:00 | upgraded | `lib32-libldap (2.6.13-1 -> 2.7.1-1)` | PRE-WINDOW |
| B307 | 2797 | 2026-10-20T09:16:39-03:00 | upgraded | `lib32-curl (8.22.0-1 -> 8.23.0-1)` | PRE-WINDOW |
| B308 | 2798 | 2026-10-20T09:16:39-03:00 | upgraded | `lib32-expat (2.8.4-1 -> 2.9.0-1)` | PRE-WINDOW |
| B309 | 2799 | 2026-10-20T09:16:39-03:00 | upgraded | `lib32-libpng (1.6.58-2 -> 1.6.59-1)` | PRE-WINDOW |
| B310 | 2800 | 2026-10-20T09:16:39-03:00 | upgraded | `lib32-freetype2 (2.14.3-1 -> 2.15.0-1)` | PRE-WINDOW |
| B311 | 2801 | 2026-10-20T09:16:39-03:00 | upgraded | `lib32-pcre2 (10.48-1 -> 10.49-1)` | PRE-WINDOW |
| B312 | 2802 | 2026-10-20T09:16:39-03:00 | upgraded | `lib32-glib2 (2.88.3-1 -> 2.90.1-1)` | PRE-WINDOW |
| B313 | 2803 | 2026-10-20T09:16:39-03:00 | upgraded | `lib32-libgcrypt (1.12.3-1 -> 1.12.4-1)` | PRE-WINDOW |
| B314 | 2804 | 2026-10-20T09:16:39-03:00 | upgraded | `lib32-xz (5.8.3-1 -> 5.8.4-1)` | PRE-WINDOW |
| B315 | 2805 | 2026-10-20T09:16:39-03:00 | upgraded | `lib32-systemd (261.2-1 -> 262-1)` | PRE-WINDOW |
| B316 | 2806 | 2026-10-20T09:16:39-03:00 | upgraded | `lib32-libpipewire (1:1.6.8-1 -> 1:1.6.9-1)` | PRE-WINDOW |
| B317 | 2807 | 2026-10-20T09:16:40-03:00 | upgraded | `lib32-llvm-libs (1:22.1.8-1 -> 1:23.1.3-1)` | PRE-WINDOW |
| B318 | 2808 | 2026-10-20T09:16:40-03:00 | upgraded | `lib32-spirv-tools (1:1.4.357.0-1 -> 1:1.4.363.0-1)` | PRE-WINDOW |
| B319 | 2809 | 2026-10-20T09:16:40-03:00 | upgraded | `lib32-nvidia-utils (610.57.04-1 -> 615.78.08-1)` | PRE-WINDOW |
| B320 | 2810 | 2026-10-20T09:16:40-03:00 | upgraded | `lib32-mesa (1:26.2.2-1 -> 1:26.2.5-1)` | PRE-WINDOW |
| B321 | 2811 | 2026-10-20T09:16:40-03:00 | upgraded | `lib32-sqlite (3.53.4-1 -> 3.54.0-1)` | PRE-WINDOW |
| B322 | 2812 | 2026-10-20T09:16:40-03:00 | upgraded | `lib32-nss (3.128-1 -> 3.131-1)` | PRE-WINDOW |
| B323 | 2813 | 2026-10-20T09:16:40-03:00 | installed | `lib32-opus (1.6.1-1)` | PRE-WINDOW |
| B324 | 2814 | 2026-10-20T09:16:40-03:00 | upgraded | `lib32-pipewire (1:1.6.8-1 -> 1:1.6.9-1)` | PRE-WINDOW |
| B325 | 2815 | 2026-10-20T09:16:40-03:00 | upgraded | `lib32-vulkan-icd-loader (1.4.357.0-1 -> 1.4.363.0-1)` | PRE-WINDOW |
| B326 | 2816 | 2026-10-20T09:16:40-03:00 | upgraded | `vulkan-mesa-implicit-layers (1:26.2.2-1 -> 1:26.2.5-1)` | PRE-WINDOW |
| B327 | 2817 | 2026-10-20T09:16:40-03:00 | upgraded | `lib32-vulkan-mesa-implicit-layers (1:26.2.2-1 -> 1:26.2.5-1)` | PRE-WINDOW |
| B328 | 2818 | 2026-10-20T09:16:40-03:00 | upgraded | `vulkan-radeon (1:26.2.2-1 -> 1:26.2.5-1)` | PRE-WINDOW |
| B329 | 2819 | 2026-10-20T09:16:40-03:00 | upgraded | `lib32-vulkan-radeon (1:26.2.2-1 -> 1:26.2.5-1)` | PRE-WINDOW |
| B330 | 2820 | 2026-10-20T09:16:40-03:00 | upgraded | `libayatana-appindicator (0.6.0-2 -> 0.6.1-1)` | PRE-WINDOW |
| B331 | 2821 | 2026-10-20T09:16:40-03:00 | upgraded | `libcurl-gnutls (8.22.0-1 -> 8.23.0-1)` | PRE-WINDOW |
| B332 | 2822 | 2026-10-20T09:16:40-03:00 | upgraded | `libfreehand (0.1.3-1 -> 0.1.4-1)` | PRE-WINDOW |
| B333 | 2823 | 2026-10-20T09:16:40-03:00 | upgraded | `libgsf (1.14.58-1 -> 1.14.60-1)` | PRE-WINDOW |
| B334 | 2824 | 2026-10-20T09:16:40-03:00 | upgraded | `libnautilus-extension (50.3.1-1 -> 51.1-1)` | PRE-WINDOW |
| B335 | 2825 | 2026-10-20T09:16:40-03:00 | upgraded | `libnm (1.58.1-1 -> 1.58.1-2)` | PRE-WINDOW |
| B336 | 2826 | 2026-10-20T09:16:40-03:00 | upgraded | `libportal (0.10.0-1 -> 0.11.0-1)` | PRE-WINDOW |
| B337 | 2827 | 2026-10-20T09:16:40-03:00 | upgraded | `libportal-gtk4 (0.10.0-1 -> 0.11.0-1)` | PRE-WINDOW |
| B338 | 2828 | 2026-10-20T09:16:40-03:00 | upgraded | `libqalculate (5.12.0-1 -> 5.13.2-1)` | PRE-WINDOW |
| B339 | 2829 | 2026-10-20T09:16:41-03:00 | upgraded | `libreoffice-fresh (26.8.0-2 -> 26.8.1-1)` | PRE-WINDOW |
| B340 | 2830 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-beetle-pce (20260411.153115.gae99235c2139-1 -> 20260926.103044.gb96c11e095b6-1)` | PRE-WINDOW |
| B341 | 2831 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-beetle-pce-fast (20260828.151513.g2f623abd0332-1 -> 20260925.164010.g1c693c630121-1)` | PRE-WINDOW |
| B342 | 2832 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-beetle-psx (20260902.124635.gb4bca9f86817-1 -> 20260930.052947.ged87921996c6-1)` | PRE-WINDOW |
| B343 | 2833 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-beetle-psx-hw (20260902.124635.gb4bca9f86817-1 -> 20260930.052947.ged87921996c6-1)` | PRE-WINDOW |
| B344 | 2834 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-blastem (20260902.212710.gb4d75247ebad-1 -> 20260926.203644.g1e0de94dc7e6-1)` | PRE-WINDOW |
| B345 | 2835 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-bsnes (1:20260812.183208.g6d19eef5835a-1 -> 1:20260919.203656.g05439f96121d-1)` | PRE-WINDOW |
| B346 | 2836 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-desmume (20260823.072757.g8f6b32cb9a5e-1 -> 20260920.151714.g95b4d798731c-1)` | PRE-WINDOW |
| B347 | 2837 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-dolphin (20260902.223111.ge1e6d25fa139-1 -> 20260927.201651.g4d23cf151640-1)` | PRE-WINDOW |
| B348 | 2838 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-flycast (20260903.141123.g8f511f896042-1 -> 20261001.093226.g04669ebe4164-1)` | PRE-WINDOW |
| B349 | 2839 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-mame (20260820.100011.g24cffe763621-1 -> 20260924.184211.g9069f39340f2-1)` | PRE-WINDOW |
| B350 | 2840 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-mgba (20260403.212340.g6dce57eef127-1 -> 20260917.021300.g7a12d6d4b9ac-1)` | PRE-WINDOW |
| B351 | 2841 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-mupen64plus-next (1:20260806.132731.gf275caf4b2bf-1 -> 1:20261001.093940.g12edd2c74a51-1)` | PRE-WINDOW |
| B352 | 2842 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-nestopia (1:20260830.234256.g50dd0651ab46-1 -> 1:20260925.192050.g8f00f500912a-1)` | PRE-WINDOW |
| B353 | 2843 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-overlays (20260624.142726.gd89fb7f05d65-2 -> 20260914.142923.g42c21b998894-1)` | PRE-WINDOW |
| B354 | 2844 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-parallel-n64 (20260903.191659.g2f3bf60dcd96-1 -> 20260930.000807.g0bd516ee793b-1)` | PRE-WINDOW |
| B355 | 2845 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-ppsspp (20260903.192221.g410939fc5eed-1 -> 20261001.194250.g604333e99827-1)` | PRE-WINDOW |
| B356 | 2846 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-scummvm (20260826.133028.g825fea130aba-1 -> 20260919.115140.gfcbce3ae8152-1)` | PRE-WINDOW |
| B357 | 2847 | 2026-10-20T09:16:41-03:00 | upgraded | `libretro-snes9x (1:20260816.181733.g890b5d445538-1 -> 1:20260919.102324.gfae2fea08f74-1)` | PRE-WINDOW |
| B358 | 2848 | 2026-10-20T09:16:41-03:00 | upgraded | `libsrtp (1:2.8.0-1 -> 1:2.8.1-1)` | PRE-WINDOW |
| B359 | 2849 | 2026-10-20T09:16:41-03:00 | upgraded | `libutf8proc (2.11.3-1 -> 2.12.0-1)` | PRE-WINDOW |
| B360 | 2850 | 2026-10-20T09:16:41-03:00 | upgraded | `libxmp (4.7.2-1 -> 4.7.4-1)` | PRE-WINDOW |
| B361 | 2851 | 2026-10-20T09:16:42-03:00 | upgraded | `limine (12.8.0-1 -> 12.9.3-1)` | PRE-WINDOW |
| B362 | 2852 | 2026-10-20T09:16:42-03:00 | upgraded | `limine-mkinitcpio-hook (1.38.0-1.1 -> 1.40.0-2)` | PRE-WINDOW |
| B363 | 2853 | 2026-10-20T09:16:42-03:00 | upgraded | `snapper (0.13.1-3 -> 0.13.2-1)` | PRE-WINDOW |
| B364 | 2854 | 2026-10-20T09:16:42-03:00 | upgraded | `limine-snapper-sync (1.31.0-1.1 -> 1.32.1-2)` | PRE-WINDOW |
| B365 | 2855 | 2026-10-20T09:16:42-03:00 | upgraded | `linux (7.2.3.arch1-3 -> 7.2.11.arch1-1)` | PRE-WINDOW |
| B366 | 2856 | 2026-10-20T09:16:42-03:00 | upgraded | `linux-firmware-whence (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B367 | 2857 | 2026-10-20T09:16:42-03:00 | installed | `linux-firmware-amd (20260916-1)` | PRE-WINDOW |
| B368 | 2858 | 2026-10-20T09:16:42-03:00 | upgraded | `linux-firmware-amdgpu (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B369 | 2859 | 2026-10-20T09:16:42-03:00 | upgraded | `linux-firmware-atheros (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B370 | 2860 | 2026-10-20T09:16:42-03:00 | upgraded | `linux-firmware-broadcom (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B371 | 2861 | 2026-10-20T09:16:42-03:00 | upgraded | `linux-firmware-cirrus (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B372 | 2862 | 2026-10-20T09:16:42-03:00 | upgraded | `linux-firmware-intel (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B373 | 2863 | 2026-10-20T09:16:42-03:00 | upgraded | `linux-firmware-mediatek (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B374 | 2864 | 2026-10-20T09:16:42-03:00 | upgraded | `linux-firmware-nvidia (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B375 | 2865 | 2026-10-20T09:16:42-03:00 | upgraded | `linux-firmware-other (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B376 | 2866 | 2026-10-20T09:16:42-03:00 | upgraded | `linux-firmware-radeon (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B377 | 2867 | 2026-10-20T09:16:42-03:00 | upgraded | `linux-firmware-realtek (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B378 | 2868 | 2026-10-20T09:16:42-03:00 | installed | `linux-firmware-ti (20260916-1)` | PRE-WINDOW |
| B379 | 2869 | 2026-10-20T09:16:42-03:00 | upgraded | `linux-firmware (20260810-2 -> 20260916-1)` | PRE-WINDOW |
| B380 | 2870 | 2026-10-20T09:16:44-03:00 | upgraded | `linux-headers (7.2.3.arch1-3 -> 7.2.11.arch1-1)` | PRE-WINDOW |
| B381 | 2871 | 2026-10-20T09:16:44-03:00 | upgraded | `lld (22.1.8-1 -> 23.1.3-3)` | PRE-WINDOW |
| B382 | 2872 | 2026-10-20T09:16:44-03:00 | installed | `libmms (0.6.4-6)` | PRE-WINDOW |
| B383 | 2873 | 2026-10-20T09:16:44-03:00 | installed | `libzen (0.4.41-3)` | PRE-WINDOW |
| B384 | 2874 | 2026-10-20T09:16:44-03:00 | installed | `tinyxml2 (11.0.0-2)` | PRE-WINDOW |
| B385 | 2875 | 2026-10-20T09:16:44-03:00 | installed | `libxpm (3.5.19-1)` | PRE-WINDOW |
| B386 | 2876 | 2026-10-20T09:16:44-03:00 | installed | `gd (2.3.3-9)` | PRE-WINDOW |
| B387 | 2877 | 2026-10-20T09:16:44-03:00 | installed | `netpbm (10.86.51-2)` | PRE-WINDOW |
| B388 | 2878 | 2026-10-20T09:16:44-03:00 | installed | `gts (0.7.6.121130-5)` | PRE-WINDOW |
| B389 | 2879 | 2026-10-20T09:16:44-03:00 | installed | `graphviz (16.1.0-1)` | PRE-WINDOW |
| B390 | 2880 | 2026-10-20T09:16:44-03:00 | installed | `libmediainfo (26.10-1)` | PRE-WINDOW |
| B391 | 2881 | 2026-10-20T09:16:44-03:00 | upgraded | `localsearch (3.11.2-1 -> 3.12.0-1)` | PRE-WINDOW |
| B392 | 2882 | 2026-10-20T09:16:44-03:00 | upgraded | `luajit (2.1.1788460057+24c20c9-1 -> 2.1.1791988261+2a8e017-1)` | PRE-WINDOW |
| B393 | 2883 | 2026-10-20T09:16:44-03:00 | upgraded | `mariadb-libs (12.3.3-2 -> 13.0.2-2)` | PRE-WINDOW |
| B394 | 2884 | 2026-10-20T09:16:44-03:00 | upgraded | `mise (2026.9.1-1 -> 2026.10.12-1)` | PRE-WINDOW |
| B395 | 2885 | 2026-10-20T09:16:44-03:00 | upgraded | `msgpack-c (7.0.1-1 -> 7.0.2-1)` | PRE-WINDOW |
| B396 | 2886 | 2026-10-20T09:16:44-03:00 | upgraded | `mujs (1.3.9-1 -> 1.3.10-1)` | PRE-WINDOW |
| B397 | 2887 | 2026-10-20T09:16:44-03:00 | upgraded | `nautilus (50.3.1-1 -> 51.1-1)` | PRE-WINDOW |
| B398 | 2888 | 2026-10-20T09:16:44-03:00 | upgraded | `python-gobject (3.56.3-1 -> 3.58.1-1)` | PRE-WINDOW |
| B399 | 2889 | 2026-10-20T09:16:44-03:00 | upgraded | `nautilus-python (4.1.0-3 -> 4.2.0-1)` | PRE-WINDOW |
| B400 | 2890 | 2026-10-20T09:16:44-03:00 | upgraded | `neovim (0.12.5-1 -> 0.12.6-1)` | PRE-WINDOW |
| B401 | 2891 | 2026-10-20T09:16:44-03:00 | upgraded | `nss-mdns (0.15.1-2 -> 0.15.1-3)` | PRE-WINDOW |
| B402 | 2892 | 2026-10-20T09:16:44-03:00 | upgraded | `nvidia-open-dkms (610.57.04-1 -> 615.78.08-1)` | PRE-WINDOW |
| B403 | 2893 | 2026-10-20T09:16:44-03:00 | upgraded | `obsidian (1.13.7-2 -> 1.14.4-2)` | PRE-WINDOW |
| B404 | 2895 | 2026-10-20T09:16:45-03:00 | upgraded | `omarchy-nvim (2026.8.13-1 -> 2026.9.21-5)` | PRE-WINDOW |
| B405 | 2896 | 2026-10-20T09:16:45-03:00 | upgraded | `pipewire-alsa (1:1.6.8-1 -> 1:1.6.9-1)` | PRE-WINDOW |
| B406 | 2897 | 2026-10-20T09:16:45-03:00 | upgraded | `pipewire-pulse (1:1.6.8-1 -> 1:1.6.9-1)` | PRE-WINDOW |
| B407 | 2898 | 2026-10-20T09:16:45-03:00 | upgraded | `plymouth (26.134.222-2 -> 26.134.222-3)` | PRE-WINDOW |
| B408 | 2899 | 2026-10-20T09:16:45-03:00 | upgraded | `postgresql-libs (18.6-1 -> 18.6-2)` | PRE-WINDOW |
| B409 | 2900 | 2026-10-20T09:16:45-03:00 | upgraded | `python-cairo (1.29.1-1 -> 1.29.2-1)` | PRE-WINDOW |
| B410 | 2901 | 2026-10-20T09:16:45-03:00 | upgraded | `python-cssselect (1.5.0-1 -> 1.6.0-1)` | PRE-WINDOW |
| B411 | 2902 | 2026-10-20T09:16:45-03:00 | upgraded | `python-dbus (1.4.0-2 -> 1.5.0-1)` | PRE-WINDOW |
| B412 | 2903 | 2026-10-20T09:16:45-03:00 | upgraded | `python-filelock (3.31.1-1 -> 4.0.10-1)` | PRE-WINDOW |
| B413 | 2904 | 2026-10-20T09:16:45-03:00 | upgraded | `python-poetry-core (2.4.1-1 -> 2.5.0-1)` | PRE-WINDOW |
| B414 | 2905 | 2026-10-20T09:16:45-03:00 | upgraded | `python-pyserial (3.5-8 -> 3.5-9)` | PRE-WINDOW |
| B415 | 2906 | 2026-10-20T09:16:45-03:00 | upgraded | `python-pyxdg (0.28-7 -> 0.28-8)` | PRE-WINDOW |
| B416 | 2907 | 2026-10-20T09:16:45-03:00 | upgraded | `python-soupsieve (2.9.2-1 -> 2.10-1)` | PRE-WINDOW |
| B417 | 2908 | 2026-10-20T09:16:45-03:00 | upgraded | `qpdf (12.4.1-1 -> 12.4.2-1)` | PRE-WINDOW |
| B418 | 2909 | 2026-10-20T09:16:45-03:00 | upgraded | `radare2 (6.2.0-1 -> 6.2.2-1)` | PRE-WINDOW |
| B419 | 2910 | 2026-10-20T09:16:45-03:00 | upgraded | `retroarch-assets-xmb (1:20260411.201626.gcd17f64cff4e-1 -> 1:20260813.223050.g73106363e14e-1)` | PRE-WINDOW |
| B420 | 2911 | 2026-10-20T09:16:45-03:00 | upgraded | `retroarch-assets-glui (1:20260411.201626.gcd17f64cff4e-1 -> 1:20260813.223050.g73106363e14e-1)` | PRE-WINDOW |
| B421 | 2912 | 2026-10-20T09:16:45-03:00 | upgraded | `retroarch-assets-ozone (1:20260411.201626.gcd17f64cff4e-1 -> 1:20260813.223050.g73106363e14e-1)` | PRE-WINDOW |
| B422 | 2913 | 2026-10-20T09:16:45-03:00 | upgraded | `rsync (3.5.0-1 -> 3.5.1-3)` | PRE-WINDOW |
| B423 | 2914 | 2026-10-20T09:16:45-03:00 | upgraded | `rust (1:1.98.1-1 -> 1:1.99.1-1)` | PRE-WINDOW |
| B424 | 2915 | 2026-10-20T09:16:46-03:00 | upgraded | `signal-desktop (8.26.0-1 -> 8.31.0-2)` | PRE-WINDOW |
| B425 | 2917 | 2026-10-20T09:16:46-03:00 | upgraded | `starship (1.26.0-1 -> 1.27.0-1)` | PRE-WINDOW |
| B426 | 2918 | 2026-10-20T09:16:46-03:00 | upgraded | `strace (7.0-1 -> 7.2-1)` | PRE-WINDOW |
| B427 | 2919 | 2026-10-20T09:16:46-03:00 | installed | `libspelling (0.4.10-1)` | PRE-WINDOW |
| B428 | 2920 | 2026-10-20T09:16:46-03:00 | installed | `papers (51.1-1)` | PRE-WINDOW |
| B429 | 2921 | 2026-10-20T09:16:46-03:00 | upgraded | `sushi (50.0-1 -> 51.2-1)` | PRE-WINDOW |
| B430 | 2922 | 2026-10-20T09:16:46-03:00 | upgraded | `systemd-sysvcompat (261.2-1 -> 262-1)` | PRE-WINDOW |
| B431 | 2923 | 2026-10-20T09:16:46-03:00 | upgraded | `tinyxxd (1.3.16-1 -> 1.3.17-1)` | PRE-WINDOW |
| B432 | 2924 | 2026-10-20T09:16:46-03:00 | upgraded | `tmux (3.7_c-1 -> 3.8-1)` | PRE-WINDOW |
| B433 | 2925 | 2026-10-20T09:16:46-03:00 | upgraded | `usage (5.1.0-1 -> 6.12.1-1)` | PRE-WINDOW |
| B434 | 2926 | 2026-10-20T09:16:46-03:00 | upgraded | `uwsm (0.26.7-1 -> 0.27.1-1)` | PRE-WINDOW |
| B435 | 2927 | 2026-10-20T09:16:46-03:00 | upgraded | `vulkan-swrast (1:26.2.2-1 -> 1:26.2.5-1)` | PRE-WINDOW |
| B436 | 2928 | 2026-10-20T09:16:46-03:00 | upgraded | `vulkan-tools (1.4.357.0-1 -> 1.4.363.0-1)` | PRE-WINDOW |
| B437 | 2929 | 2026-10-20T09:16:46-03:00 | upgraded | `walker (2.17.0-1 -> 2.17.2-1)` | PRE-WINDOW |
| B438 | 2930 | 2026-10-20T09:16:46-03:00 | upgraded | `xdg-dbus-proxy (0.1.8-1 -> 0.1.9-1)` | PRE-WINDOW |
| B439 | 2931 | 2026-10-20T09:16:46-03:00 | upgraded | `webkit2gtk-4.1 (2.52.6-1 -> 2.54.1-1)` | PRE-WINDOW |
| B440 | 2932 | 2026-10-20T09:16:46-03:00 | upgraded | `wireless-regdb (2026.05.30-1 -> 2026.09.03-1)` | PRE-WINDOW |
| B441 | 2933 | 2026-10-20T09:16:46-03:00 | upgraded | `wxwidgets-common (3.2.11-2 -> 3.2.12-1)` | PRE-WINDOW |
| B442 | 2934 | 2026-10-20T09:16:46-03:00 | upgraded | `wxwidgets-gtk3 (3.2.11-2 -> 3.2.12-1)` | PRE-WINDOW |
| B443 | 2935 | 2026-10-20T09:16:46-03:00 | upgraded | `xdg-terminal-exec (0.14.3-1 -> 0.14.3-2)` | PRE-WINDOW |
| B444 | 2936 | 2026-10-20T09:16:46-03:00 | upgraded | `xmlstarlet (1.6.1-6 -> 1.7.0-1)` | PRE-WINDOW |
| B445 | 2937 | 2026-10-20T09:16:46-03:00 | upgraded | `xorg-server (21.1.24-1 -> 21.1.25-2)` | PRE-WINDOW |
| B446 | 2938 | 2026-10-20T09:16:46-03:00 | upgraded | `xorg-server-xvfb (21.1.24-1 -> 21.1.25-2)` | PRE-WINDOW |
| B447 | 2939 | 2026-10-20T09:16:46-03:00 | upgraded | `xournalpp (1.3.7-1 -> 1.3.8-1)` | PRE-WINDOW |
| B448 | 2940 | 2026-10-20T09:16:47-03:00 | upgraded | `yaru-icon-theme (26.04.5.1ubuntu-1 -> 26.10.3-3)` | PRE-WINDOW |
| B449 | 3067 | 2026-10-20T09:27:39-03:00 | installed | `fwupd-efi (1.8-2)` | PRE-WINDOW |
| B450 | 3068 | 2026-10-20T09:27:39-03:00 | installed | `libmbim (1.34.0-1)` | PRE-WINDOW |
| B451 | 3069 | 2026-10-20T09:27:39-03:00 | installed | `libmm-glib (1.24.2-1)` | PRE-WINDOW |
| B452 | 3070 | 2026-10-20T09:27:39-03:00 | installed | `libqrtr-glib (1.4.0-1)` | PRE-WINDOW |
| B453 | 3071 | 2026-10-20T09:27:39-03:00 | installed | `libqmi (1.38.0-1)` | PRE-WINDOW |
| B454 | 3072 | 2026-10-20T09:27:39-03:00 | installed | `passim (0.1.12-1)` | PRE-WINDOW |
| B455 | 3073 | 2026-10-20T09:27:39-03:00 | installed | `fwupd (2.1.8-1)` | PRE-WINDOW |
| B456 | 3088 | 2026-10-20T09:29:40-03:00 | installed | `go (2:1.27.2-1)` | PRE-WINDOW |
| B457 | 3095 | 2026-10-20T09:31:03-03:00 | upgraded | `elephant (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B458 | 3096 | 2026-10-20T09:31:03-03:00 | installed | `elephant-debug (2.22.1-1)` | PRE-WINDOW |
| B459 | 3097 | 2026-10-20T09:31:03-03:00 | upgraded | `elephant-clipboard (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B460 | 3098 | 2026-10-20T09:31:03-03:00 | installed | `elephant-clipboard-debug (2.22.1-1)` | PRE-WINDOW |
| B461 | 3099 | 2026-10-20T09:31:03-03:00 | upgraded | `elephant-runner (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B462 | 3100 | 2026-10-20T09:31:03-03:00 | installed | `elephant-runner-debug (2.22.1-1)` | PRE-WINDOW |
| B463 | 3101 | 2026-10-20T09:31:03-03:00 | upgraded | `elephant-calc (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B464 | 3102 | 2026-10-20T09:31:03-03:00 | installed | `elephant-calc-debug (2.22.1-1)` | PRE-WINDOW |
| B465 | 3103 | 2026-10-20T09:31:03-03:00 | upgraded | `elephant-providerlist (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B466 | 3104 | 2026-10-20T09:31:03-03:00 | installed | `elephant-providerlist-debug (2.22.1-1)` | PRE-WINDOW |
| B467 | 3105 | 2026-10-20T09:31:04-03:00 | upgraded | `elephant-symbols (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B468 | 3106 | 2026-10-20T09:31:04-03:00 | installed | `elephant-symbols-debug (2.22.1-1)` | PRE-WINDOW |
| B469 | 3107 | 2026-10-20T09:31:04-03:00 | upgraded | `elephant-files (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B470 | 3108 | 2026-10-20T09:31:04-03:00 | installed | `elephant-files-debug (2.22.1-1)` | PRE-WINDOW |
| B471 | 3109 | 2026-10-20T09:31:04-03:00 | upgraded | `elephant-websearch (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B472 | 3110 | 2026-10-20T09:31:04-03:00 | installed | `elephant-websearch-debug (2.22.1-1)` | PRE-WINDOW |
| B473 | 3111 | 2026-10-20T09:31:04-03:00 | upgraded | `elephant-desktopapplications (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B474 | 3112 | 2026-10-20T09:31:04-03:00 | installed | `elephant-desktopapplications-debug (2.22.1-1)` | PRE-WINDOW |
| B475 | 3113 | 2026-10-20T09:31:04-03:00 | upgraded | `elephant-bluetooth (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B476 | 3114 | 2026-10-20T09:31:04-03:00 | installed | `elephant-bluetooth-debug (2.22.1-1)` | PRE-WINDOW |
| B477 | 3115 | 2026-10-20T09:31:04-03:00 | upgraded | `elephant-unicode (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B478 | 3116 | 2026-10-20T09:31:04-03:00 | installed | `elephant-unicode-debug (2.22.1-1)` | PRE-WINDOW |
| B479 | 3117 | 2026-10-20T09:31:04-03:00 | upgraded | `elephant-todo (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B480 | 3118 | 2026-10-20T09:31:04-03:00 | installed | `elephant-todo-debug (2.22.1-1)` | PRE-WINDOW |
| B481 | 3119 | 2026-10-20T09:31:04-03:00 | upgraded | `elephant-menus (2.21.0-1 -> 2.22.1-1)` | PRE-WINDOW |
| B482 | 3120 | 2026-10-20T09:31:04-03:00 | installed | `elephant-menus-debug (2.22.1-1)` | PRE-WINDOW |
| B483 | 3129 | 2026-10-20T09:31:04-03:00 | removed | `go (2:1.27.2-1)` | PRE-WINDOW |
| B484 | 3135 | 2026-10-20T09:38:34-03:00 | removed | `elephant-websearch-debug (2.22.1-1)` | PRE-WINDOW |
| B485 | 3136 | 2026-10-20T09:38:34-03:00 | removed | `elephant-unicode-debug (2.22.1-1)` | PRE-WINDOW |
| B486 | 3137 | 2026-10-20T09:38:34-03:00 | removed | `elephant-todo-debug (2.22.1-1)` | PRE-WINDOW |
| B487 | 3138 | 2026-10-20T09:38:34-03:00 | removed | `elephant-symbols-debug (2.22.1-1)` | PRE-WINDOW |
| B488 | 3139 | 2026-10-20T09:38:34-03:00 | removed | `elephant-runner-debug (2.22.1-1)` | PRE-WINDOW |
| B489 | 3140 | 2026-10-20T09:38:34-03:00 | removed | `elephant-providerlist-debug (2.22.1-1)` | PRE-WINDOW |
| B490 | 3141 | 2026-10-20T09:38:34-03:00 | removed | `elephant-menus-debug (2.22.1-1)` | PRE-WINDOW |
| B491 | 3142 | 2026-10-20T09:38:34-03:00 | removed | `elephant-files-debug (2.22.1-1)` | PRE-WINDOW |
| B492 | 3143 | 2026-10-20T09:38:34-03:00 | removed | `elephant-desktopapplications-debug (2.22.1-1)` | PRE-WINDOW |
| B493 | 3144 | 2026-10-20T09:38:34-03:00 | removed | `elephant-debug (2.22.1-1)` | PRE-WINDOW |
| B494 | 3145 | 2026-10-20T09:38:34-03:00 | removed | `elephant-clipboard-debug (2.22.1-1)` | PRE-WINDOW |
| B495 | 3146 | 2026-10-20T09:38:34-03:00 | removed | `elephant-calc-debug (2.22.1-1)` | PRE-WINDOW |
| B496 | 3147 | 2026-10-20T09:38:34-03:00 | removed | `elephant-bluetooth-debug (2.22.1-1)` | PRE-WINDOW |
| B497 | 3148 | 2026-10-20T09:38:34-03:00 | removed | `btrbk (0.32.7-1)` | PRE-WINDOW |
| B498 | 3155 | 2026-10-20T09:39:21-03:00 | removed | `webp-pixbuf-loader (0.2.7-2)` | PRE-WINDOW |
| B499 | 3156 | 2026-10-20T09:39:21-03:00 | removed | `hyprwayland-scanner (0.4.6-1)` | PRE-WINDOW |
| B500 | 3157 | 2026-10-20T09:39:21-03:00 | removed | `gst-plugin-gtk (1.28.8-1)` | PRE-WINDOW |
| B501 | 3164 | 2026-10-20T13:23:08-03:00 | installed | `zcode (3.16.2-1)` | POST-WINDOW |
| B502 | 3173 | 2026-10-21T17:55:56-03:00 | installed | `tizen-sdb (2.3.2-3)` | POST-WINDOW |
| B503 | 3174 | 2026-10-21T17:55:56-03:00 | installed | `tizen-sdb-debug (2.3.2-3)` | POST-WINDOW |
| B504 | 3182 | 2026-10-21T18:07:37-03:00 | installed | `openssl-1.0 (1.0.2.u-7)` | POST-WINDOW |
| B505 | 3183 | 2026-10-21T18:07:37-03:00 | installed | `openssl-1.0-debug (1.0.2.u-7)` | POST-WINDOW |

## Section C — ALPM transaction boundaries in range

| Log line | Timestamp (-0300) | Event | Window |
|---|---|---|---|
| 2479 | 2026-10-20T09:16:27-03:00 | transaction started | PRE-WINDOW |
| 2941 | 2026-10-20T09:16:47-03:00 | transaction completed | PRE-WINDOW |
| 3066 | 2026-10-20T09:27:39-03:00 | transaction started | PRE-WINDOW |
| 3074 | 2026-10-20T09:27:39-03:00 | transaction completed | PRE-WINDOW |
| 3087 | 2026-10-20T09:29:39-03:00 | transaction started | PRE-WINDOW |
| 3089 | 2026-10-20T09:29:40-03:00 | transaction completed | PRE-WINDOW |
| 3094 | 2026-10-20T09:31:03-03:00 | transaction started | PRE-WINDOW |
| 3121 | 2026-10-20T09:31:04-03:00 | transaction completed | PRE-WINDOW |
| 3128 | 2026-10-20T09:31:04-03:00 | transaction started | PRE-WINDOW |
| 3130 | 2026-10-20T09:31:04-03:00 | transaction completed | PRE-WINDOW |
| 3134 | 2026-10-20T09:38:33-03:00 | transaction started | PRE-WINDOW |
| 3149 | 2026-10-20T09:38:34-03:00 | transaction completed | PRE-WINDOW |
| 3154 | 2026-10-20T09:39:21-03:00 | transaction started | PRE-WINDOW |
| 3158 | 2026-10-20T09:39:21-03:00 | transaction completed | PRE-WINDOW |
| 3163 | 2026-10-20T13:23:08-03:00 | transaction started | POST-WINDOW |
| 3165 | 2026-10-20T13:23:09-03:00 | transaction completed | POST-WINDOW |
| 3172 | 2026-10-21T17:55:56-03:00 | transaction started | POST-WINDOW |
| 3175 | 2026-10-21T17:55:56-03:00 | transaction completed | POST-WINDOW |
| 3181 | 2026-10-21T18:07:37-03:00 | transaction started | POST-WINDOW |
| 3184 | 2026-10-21T18:07:37-03:00 | transaction completed | POST-WINDOW |

## Section D — POST-WINDOW rows in full (the only rows at or after 2026-10-20T09:40 -03)

### D1 — POST-WINDOW `[PACMAN] Running` command lines

| # | Log line | Timestamp (-0300) | Operation class | Command line |
|---|---|---|---|---|
| A9 | 3161 | 2026-10-20T13:23:08-03:00 | install-local-package | `pacman -U --needed --noconfirm --config /etc/pacman.conf -- /home/vgpnk/.cache/yay/zcode/zcode-3.16.2-1-x86_64.pkg.tar.zst` |
| A10 | 3169 | 2026-10-20T13:23:09-03:00 | dependency-flag (no package change) | `pacman -D -q --asexplicit --noconfirm --config /etc/pacman.conf -- zcode` |
| A11 | 3170 | 2026-10-21T17:55:56-03:00 | install-local-package | `pacman -U --noconfirm --config /etc/pacman.conf -- /home/vgpnk/.cache/yay/tizen-sdb/tizen-sdb-2.3.2-3-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/tizen-sdb/tizen-sdb-debug-2.3.2-3-x86_64.pkg.tar.zst` |
| A12 | 3177 | 2026-10-21T17:55:56-03:00 | dependency-flag (no package change) | `pacman -D --asdeps -q --noconfirm --config /etc/pacman.conf -- tizen-sdb-debug` |
| A13 | 3178 | 2026-10-21T17:55:56-03:00 | dependency-flag (no package change) | `pacman -D -q --asexplicit --noconfirm --config /etc/pacman.conf -- tizen-sdb` |
| A14 | 3179 | 2026-10-21T18:07:37-03:00 | install-local-package | `pacman -U --noconfirm --config /etc/pacman.conf -- /home/vgpnk/.cache/yay/openssl-1.0/openssl-1.0-1.0.2.u-7-x86_64.pkg.tar.zst /home/vgpnk/.cache/yay/openssl-1.0/openssl-1.0-debug-1.0.2.u-7-x86_64.pkg.tar.zst` |
| A15 | 3186 | 2026-10-21T18:07:37-03:00 | dependency-flag (no package change) | `pacman -D -q --asdeps --noconfirm --config /etc/pacman.conf -- openssl-1.0-debug` |
| A16 | 3187 | 2026-10-21T18:07:37-03:00 | dependency-flag (no package change) | `pacman -D -q --asexplicit --noconfirm --config /etc/pacman.conf -- openssl-1.0` |
| A17 | 3188 | 2026-10-21T20:32:00-03:00 | sync-only (databases) | `pacman -Sy --noconfirm` |
| A18 | 3190 | 2026-10-22T04:10:08-03:00 | cache-clean (all packages) | `pacman -Scc --noconfirm` |
| A19 | 3191 | 2026-10-22T04:10:19-03:00 | cache-clean (all packages) | `pacman -Scc` |

### D2 — POST-WINDOW ALPM package records

| # | Log line | Timestamp (-0300) | Action | Package and version change |
|---|---|---|---|---|
| B501 | 3164 | 2026-10-20T13:23:08-03:00 | installed | `zcode (3.16.2-1)` |
| B502 | 3173 | 2026-10-21T17:55:56-03:00 | installed | `tizen-sdb (2.3.2-3)` |
| B503 | 3174 | 2026-10-21T17:55:56-03:00 | installed | `tizen-sdb-debug (2.3.2-3)` |
| B504 | 3182 | 2026-10-21T18:07:37-03:00 | installed | `openssl-1.0 (1.0.2.u-7)` |
| B505 | 3183 | 2026-10-21T18:07:37-03:00 | installed | `openssl-1.0-debug (1.0.2.u-7)` |

No ALPM `removed`, `upgraded` or `downgraded` record falls after
2026-10-20T09:40:00-0300. Every POST-WINDOW package record is an `installed`
record, and the count is exactly 5.

## Section E — context row outside the assigned range (line 2462)

This line carries the operator's full-upgrade argv. It is one line above the
assigned read start, so it is reported as context rather than as an in-range row.

```
[2026-10-20T09:15:30-0300] [PACMAN] Running 'pacman -Syu --needed --noconfirm nvme-cli smartmontools fio xfsprogs pacman-contrib earlyoom iotop-c sysstat stress-ng btrbk linux-lts linux-lts-headers'
```

| Log line | Timestamp (-0300) | Window |
|---|---|---|
| 2462 | 2026-10-20T09:15:30-03:00 | PRE-WINDOW |

## Section F — operation-class summary over the in-range `[PACMAN] Running` lines

| Operation class | PRE-WINDOW | POST-WINDOW | Total |
|---|---|---|---|
| cache-clean (all packages) | 0 | 2 | 2 |
| dependency-flag (no package change) | 2 | 5 | 7 |
| install-from-repo | 2 | 0 | 2 |
| install-local-package | 1 | 3 | 4 |
| remove | 3 | 0 | 3 |
| sync-only (databases) | 0 | 1 | 1 |

Reading of the POST-WINDOW column for premise P5:

- `install-local-package` = 3 invocations, all `pacman -U` of a locally built `.pkg.tar.zst` from the user's
  yay cache. These changed the installed set: they are the transactions that
  produced the 5 POST-WINDOW `installed` records (each debug sub-package is
  its own installed record).
- `dependency-flag (no package change)` = 5 invocations, all `pacman -D`. These write only the install-reason field of
  the local database; they change no package file and produce no ALPM
  installed/upgraded/removed record.
- `sync-only (databases)` = 1 invocation, `pacman -Sy --noconfirm` at 2026-10-21T20:32:00-03:00.
  It refreshes the sync databases and installs nothing.
- `cache-clean (all packages)` = 2 invocations, all `pacman -Scc` at 2026-10-22T04:10:08-03:00, 2026-10-22T04:10:19-03:00.
  These remove cached package files and install nothing.
- No `remove`, `full-upgrade`, `install-from-repo`, `download-only` invocations fall after the window start.

## Section G — package-cache state read after the POST-WINDOW cache clean

Read-only observation at the end of the census. The `ls | wc -l` shape counts
directory entries, and every one of the four entries is an empty scratch
directory left by a `pacman -U` download step, not a package file.

| Probe | Result |
|---|---|
| `ls /var/cache/pacman/pkg \| wc -l` | 4 (entries) |
| `sudo find /var/cache/pacman/pkg -type f \| wc -l` | 0 (regular files) |
| `sudo find /var/cache/pacman/pkg -name '*.pkg.tar*' \| wc -l` | 0 |
| `sudo find /var/cache/pacman -name '*libinput*' \| wc -l` | 0 |
| entries inside each of the 4 `download-*` directories | 0 each |

The four entries are `download-vcoq00` (2026-10-20 09:31), `download-Lsbwhh`
(2026-10-20 13:23), `download-0jh7Uc` (2026-10-21 17:55) and
`download-r5r0Ix` (2026-10-21 18:07) — one per `pacman -U` invocation in the
census, each owned by `alpm` with mode `drwx------` and each empty.

Consequence for the P5 rollback premise: no cached package file exists, so no
version can be restored from `/var/cache/pacman/pkg`. The count of 4 is a
count of empty scratch directories, not of retained packages.

