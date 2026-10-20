# RevL0Accuracy — r17 L0 line, fact-by-fact

Target `.ufo/l0-questions.md:60`. Ev = `l1-capture/boot-chain-capture.txt` (cap:N), `l1-capture/fresh-capture.txt` (fresh:N), `/var/log/pacman.log` (pac:N). S supported · P partly wrong · W wrong · U unsupported by cited evidence.

| # | L0 fact | St | Evidence |
|---|---|---|---|
| 1 | 13 pacman runs 07:45–09:39, all account vgpnk | S | cap:55-67, 13/13 `vgpnk :` |
| 2 | all 13 PWD ~/Documents/nvhelpme | **W** | 4/13 nvhelpme (cap:82,87,95,96); 4 `/home/vgpnk/tmp` (cap:76-79); 5 `/home/vgpnk` (cap:89-93). "RAM NVMe BIOS" unverified |
| 3 | -Syu versions: mkinitcpio 41.1→42.2, linux 7.2.3→7.2.11, systemd 261.2→262, plymouth -2→-3, hook 1.38.0→1.40.0-2, limine 12.8→12.9.3, nvidia 610.57→615.78, linux-lts installed | S | pac:2531,2539,2540,2851,2852,2855,2892,2898 |
| 4 | dkms "built for 7.2.11, 6.18.57-lts, 7.2.3" | P | fresh:38: 7.2.3 = "Built modules are missing"; only two kernel trees (fresh:39-41) |
| 5 | UKIs built 09:18 by hook; rebuilt 09:26:11 by limine-update; not in pacman.log | S | pac:2984-3046; cap:82; log ends 09:39:21 |
| 6 | reboot 09:56; boot 0 09:57:09 on 7.2.11 | S | cap:5,9,10 (uptime -s: 09:57:08) |
| 7 | UKIs VERSION 42.2; init `/sysroot` 7 refs, `/new_root` 0; LATEHOOKS; hook `/new_root` + hashes | S | cap:174-184,190-200 |
| 8 | "the image ships an empty /new_root dir" | **W** | 42.2 `initcpio/functions:1212-1213`: `install -dm755 …/sysroot`; `ln -s "sysroot" …/new_root`. 41.1 was a real dir (cap:213 lists `new_root` only). cap:181 `dirs:` is type-blind |
| 9 | "so findmnt fails and btrfs-overlayfs returns 0 (no overlay)" | **W** | `/new_root` resolves to the `/sysroot` mount; findmnt canonicalizes unless `-C` (findmnt(8)), so `hooks/btrfs-overlayfs:7` matches and `mount --move` also resolves. No-op premise refuted [inf] |
| 10 | upstream master "still /new_root" | P | true of the busybox runscripts, but the same installed package ships `install/sd-btrfs-overlayfs` and `/usr/lib/limine/overlayfs-setup:4` `root_mnt="/sysroot"` (pacman files list) |
| 11 | default 7.2.11 entry booted | P | image boot observed (cap:5,10; UKI mtime 09:26:22 < boot), but `/boot/limine.conf` mtime 12:07:06 > boot (cap:106): captured config ≠ booted config. `default_entry: 2` = `//linux` S (cap:127-129; Limine CONFIG.md: index naming a directory disables autoboot ⇒ dirs are counted) |
| 12 | no boot-chain input newer than boot | P | 0/58674 across 6 named /etc files + initcpio + 2 module trees (cap:256-258); "under /etc" overbroad; `/boot/limine.conf` newer |
| 13 | LUKS unlock + plymouth worked | P | LUKS [inf] from mapper root (cap:13); plymouth unobserved; its `/new_root` target resolves via the link |
| 14 | linux-lts never booted (untested) | S | installed 09:16 (pac:2540); boot 0 is 7.2.11 |
| 15 | snapshot #2 pre-aur-elephant, 42.2 images, ro=true | P | cap:139-143,161; numbering wrong: pre-aur is snapper #2 but limine.conf's **first** snapshot entry (cap:139); pre-nvme is second (cap:149) |
| 16 | \#2 gets no writable overlay; every future entry inherits | **W** | follows only from #8-9 |
| 17 | only snapshot #1 internally consistent | P | 41.1 image + `/new_root` init consistent (cap:206-207,213); contrast with #2 unsupported |
| 18 | `/var/backups/nvme-setup-20261020-090301` | U | absent from both captures; verify before naming it rollback of record |

Net: the URGENT verdict "snapshot boots ≥#2 are degraded because btrfs-overlayfs no-ops" rests on the false `/new_root` premise and must be withdrawn/relabelled; the real residual risk is snapshot #2's frozen 09:19 fstab vs later mountpoint changes, not the overlay. PWD attribution also needs correction.

Not verified: plymouth runtime state; writer of limine.conf at 12:07:06; `/boot/EFI/limine/limine.conf` shadow (CritDefaultEntryProof); backup dir; upstream master (external, SrcOverlayHookUpstream).

Scope: executed=awk
