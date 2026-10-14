# Update-safety note — measured `-Qu` candidates, touch map, `-Syu` decision table (TSUKUROI-R2-2)

Measured 2026-10-14 10:44:35–10:51:13 -0300, host `plazir27` (DMI `MS-7E59`,
`chassis_type` 3 = desktop), user `vgpnk` (non-root), Arch rolling, kernel
`7.2.3-arch1-3`, pacman 7.1.0.r9.g54d9411-2 (libalpm 16.0.1), boot 2026-10-13
11:02 (uptime 23 h 51 m). Claims tagged [observed] / [inference] / [unknown].
Scratch: `/tmp/tsukuroi-r2-2-scratch/` (ephemeral — key outputs embedded below).

**Read-only contract held.** Every command here is a query; nothing was synced,
installed, upgraded, removed, or restarted. `pacman -Sy` and `pacman -Syu` were
**never run** — the lane's boundary rule (`SKILL.md:151-153`, `PROVINCE.md:16-17`).
The one non-obvious verb is `pacman -Su* --print*`, which builds a *plan* and
prints it: no transaction, no download, no db write [observed: rc=0 with 0 lines,
and no `/var/lib/pacman/db.lck` was created]. `checkupdates` is **absent**
(`pacman -Q pacman-contrib` → `error: package 'pacman-contrib' was not found`);
installing it is out of province, so the `-Qu` route is the one used and the
upstream-comparison route is handed to the operator (§7).

## 1. The candidate list, three ways — all empty [observed]

| probe (read-only) | result | rc |
|---|---|---|
| `pacman -Qu` | 0 lines (re-run 10:44:35, 10:49:54, 10:51:13) | 1 (`-Qu` empty = expected rc; no candidates vs sync db) |
| `pacman -Sup --print-format '%r/%n %v %s'` (pacman's own `-Su` planner) | 0 lines | 0 |
| version join: installed (`expac -Q '%n\t%v'`, 1188) vs repo-resolved sync db (`pacman -Sl` × 4 repos, 15 663 rows) | 1172 names in sync · **1171 equal** · **0 behind** · **1 ahead** | — |

- 0 behind ⇒ **no package on this host is older than its effective repo entry**;
  the three `-Qu`/`-*p` probes agree.
- 1 ahead ⇒ `1password-beta` installed `8.12.42_32.BETA-32` vs omarchy db
  `8.12.42_32.BETA-1` (`pacman -Si 1password-beta` → Repository = omarchy,
  Download Size 198.57 MiB, Installed Size 579.18 MiB). Plain `-Syu` ignores it;
  **`-Suu` would downgrade it** — see §5.
- Cross-check: `pacman -Qm` names and "installed but in no sync db"
  (`comm -23`) are **identical sets, 16 each** (`diff` clean) [observed].
  The 16 foreign are 13 × `elephant-*` + `omarchy-walker` (walker 1.0.0-2
  `Required By: None`, `Depends On: walker elephant …` all 13), plus
  `android-apktool-bin` (→ `java-runtime>=8`) and `obsidian-cli-inspector`
  (→ `sqlite`).
- ⇒ **An `-Syu` started right now would perform 0 package actions.** That is a
  statement about the *current db content only* — §2 is why it is weak evidence.

## 2. Why "empty" is not "up to date" — channel freshness is the real gate [observed]

| db | birth `%w` | ctime `%z` | mtime `%y` (upstream stamp) | size |
|---|---|---|---|---|
| `core.db` | 2026-10-11 12:54:13.542054496 | 2026-10-11 12:54:13.844054487 | **2026-09-08 15:23:46** | 129 469 B |
| `extra.db` | same | same | **2026-09-08 15:23:47** | 8 900 506 B |
| `multilib.db` | same | same | **2026-09-08 15:23:45** | 84 692 B |
| `omarchy.db` | same | same | 2026-10-11 10:16:17 | 48 989 B |
| `offline.db` | 2026-10-03 17:41:33.994891750 | 2026-10-03 17:41:33.994962839 | 2026-07-20 21:11:36 | 304 318 B |

- The birth stamp of the four live dbs matches `/var/log/pacman.log:1405` —
  `[2026-10-11T12:54:13-0300] [PACMAN] Running 'pacman -Sy --noconfirm fuse2'`
  — i.e. the last refresh was a **partial `-Sy` (no `-u`) three days ago**
  [observed: second-exact match]. No `.db.sig` files exist in
  `/var/lib/pacman/sync/` (5 `.db`, 0 `.sig`) [observed].
- Content age: core/extra/multilib carry a **2026-09-08** server stamp — 36 days
  before this measurement — while omarchy's own db is stamped 2026-10-11 10:16.
  Both live behind different hosts: core/extra/multilib via
  `/etc/pacman.d/mirrorlist:1` → `https://stable-mirror.omarchy.org/$repo/os/$arch`
  (58 B, one line), omarchy via `/etc/pacman.conf:30` →
  `https://pkgs.omarchy.org/stable/$arch`.
- ⇒ **`-Qu` empty proves "nothing newer than a 36-day-old snapshot", not "fully
  current."** Whether upstream Arch has moved since 2026-09-08 is
  **[unknown] — not measurable read-only**; the event that resolves it is the
  operator's next `-Sy`, and that same event is what defines the wave.
- `offline.db` absorbed: it is **inert** — `pacman-conf --repo-list` =
  `core, extra, multilib, omarchy` and `/etc/pacman.conf` has sections at
  `:19/:22/:25/:28` only, no `[offline]`. It cannot shadow or serve anything.
  (Closes the open item carried in `LOG.md:28`.)
- Migration state clean: `/var/lib/pacman/local/ALPM_DB_VERSION` = `9` with
  pacman 7.1.0.r9 [observed] — no db-format conversion is pending.

## 3. Touch map — what a candidate would cost and couple to [observed sizes]

Per-candidate rows do not exist (candidate set empty). What follows is the
class-resolved cost map from the **sync db itself** (`pacman -Si`, effective
repo after precedence, MiB), so any future candidate can be classified in one
lookup. Classes are the ones that carry rebuild/reboot/boot-surface coupling.

**kernel / firmware / boot class** — coupling: `90-mkinitcpio-install.hook`
(initramfs rebuild), `99-limine.hook` (writes `/boot/EFI/BOOT/*.EFI`), dkms (§6).

| package | download | installed |
|---|---|---|
| `linux` | 148.38 | 148.75 |
| `linux-firmware` (meta) | 0.0025 | 0.00 |
| `linux-firmware-intel` | 127.88 | 132.48 |
| `linux-firmware-nvidia` | 98.83 | 103.55 |
| `linux-firmware-atheros` | 51.21 | 51.31 |
| `linux-firmware-mediatek` | 35.76 | 36.99 |
| `linux-firmware-other` | 29.67 | 29.98 |
| `linux-firmware-amdgpu` | 26.27 | 27.04 |
| `linux-firmware-broadcom` | 12.89 | 12.94 |
| `linux-firmware-realtek` | 7.13 | 7.69 |
| `linux-firmware-cirrus` | 2.86 (core) / 2.95 (omarchy, shadowed §5) | 2.88 |
| `linux-firmware-radeon` | 2.31 | 2.30 |
| `linux-firmware-whence` | 0.044 | 0.449 |
| `limine-snapper-sync` (omarchy) | 8.93 | 26.11 |
| `limine-mkinitcpio-hook` (omarchy) | 6.48 | 15.99 |
| `linux-api-headers` | 1.51 | 7.17 |
| `limine` | 0.853 | 5.28 |
| `mkinitcpio-busybox` | 0.278 | 0.524 |
| `mkinitcpio` | 0.068 | 0.214 |

[kernel-class download sum ≈ 561 MiB — computed, not measured]

**nvidia class** — coupling: dkms rebuild + module reload; running X keeps old
modules until reboot.

| package | download | installed |
|---|---|---|
| `nvidia-utils` | 300.73 | 885.66 |
| `lib32-nvidia-utils` | 112.70 | 546.07 |
| `nvidia-open-dkms` | 14.66 | 132.03 |
| `libva-nvidia-driver` | 0.064 | 0.152 |

[nvidia-class sum ≈ 428 MiB download / 1.53 GiB installed — computed]

**libc / toolchain class** — coupling: ldconfig/iconv hooks
(`/usr/share/libalpm/hooks/1{0,1,2}-*glibc*`, 7 hook files), glibc locale-gen;
services keep old mappings until restart.

| package | download | installed |
|---|---|---|
| `glibc` | 10.38 | 50.66 |
| `lib32-glibc` | 3.62 | 19.01 |
| `gcc` | 57.93 | 220.89 |
| `gcc-libs` | 0.0026 | 0.00 |
| `lib32-gcc-libs` | 10.82 | 44.98 |
| `binutils` | 8.20 | 43.76 |

[libc-class sum ≈ 91 MiB download / 379 MiB installed — computed]

**init class** — coupling: `30-systemd-daemon-reload-{system,user}.hook`,
sysusers/tmpfiles/sysctl/catalog/hwdb/binfmt hooks, `35-systemd-update.hook`
(runs on every transaction — seen at `pacman.log:2109`).

| package | download | installed |
|---|---|---|
| `systemd` | 10.38 | 39.48 |
| `systemd-libs` | 1.42 | 3.72 |
| `systemd-sysvcompat` | 0.0064 | 0.0028 |

[init-class sum ≈ 11.8 MiB download / 43.2 MiB installed — computed]

**package-manager / trust class**

| package | download | installed |
|---|---|---|
| `pacman` | 0.946 | 5.04 |
| `archlinux-keyring` | 1.215 | 1.733 |
| `omarchy-keyring` | 0.0063 | 0.00064 |

[pkgmgr-class sum ≈ 2.2 MiB download / 6.8 MiB installed — computed]

`archlinux-keyring` installed = sync = `20260902-1`; keyring census today
184 `pub` / 230 `sub` [`pacman-key --list-keys`, re-derived] — no keyring
blocker for the next refresh [observed].

**graphics / session class** — coupling: running compositor/XDG session keeps
old code until relogin; `walker-restart.hook` restarts the launcher.

| package | download | installed |
|---|---|---|
| `hyprland` | 49.07 | 64.54 |
| `mesa` / `lib32-mesa` | 13.50 / 13.37 | 53.85 / 54.28 |
| `vulkan-radeon` | 3.47 | 18.32 |
| `xorg-server` | 1.575 | 3.95 |
| `vulkan-tools` / `vulkan-icd-loader` / `vulkan-mesa-implicit-layers` | 0.468 / 0.163 / 0.056 | 1.99 / 0.634 / 0.131 |
| `xorg-xwayland` | 1.007 | 2.40 |
| `hyprland-guiutils`, `hyprland-preview-share-picker`, `wayland`, `xorg-*` (10 more members) | ≤ 2.37 each | ≤ 0.876 each |

[graphics-class sum ≈ 87 MiB download / 211 MiB installed — computed]

**Space is not the gate** [observed]: `df -h` → `/` 930 G / 77 G used /
**850 G avail** (9 %), `/boot` 2.0 G / 279 M used / **1.8 G avail** (14 %);
`CheckSpace` is on (`/etc/pacman.conf:9`). Even a same-day kernel+nvidia+libc
wave (≈1.06 GiB download, ≈2.50 GiB installed [computed by summing the tables
above]) fits with room, and the whole-cache rewrite it implies is ≈2.6 G — under
half of the 8.6 G already held in `/var/cache/pacman/pkg`.

**Wave calibration from this host's own history** [observed]: last full
sysupgrade `/var/log/pacman.log:1414` — `2026-10-11T16:13:19 Running 'pacman
-Syu --noconfirm godot blender …'` → `starting full system upgrade` (`:1416`) →
`transaction completed` `2026-10-11T16:14:40` (`:1950`): **81 s** wall for
**505** ALPM actions (upgraded/installed/reinstalled/removed lines in that
window [computed]). A wave here is minutes, not hours; duration is not the risk.

**Regeneration recipe (read-only, copy-paste).** When the set is non-empty:

```bash
pacman -Qu                                  # candidates (empty ⇒ no per-candidate rows exist)
pacman -Qu | awk '{print $1}' | xargs -r pacman -Si \
  | grep -E '^(Name|Repository|Version|Download Size|Installed Size)'   # size/class per candidate
pacman -Sup --print-format '%r/%n %v'       # pacman's own plan, print-only
pacman -Qu | awk '{print $1}' | grep -E '^(linux|linux-firmware|nvidia|lib32-nvidia|glibc|lib32-glibc|systemd|mesa|hyprland|limine|mkinitcpio)'  # class filter
```
Caveat, measured: `--print-format '%s'` printed **`0`** for `nvidia-utils`,
whose real sync download size is 300.73 MiB (`pacman -Sp --print-format
'%r/%n %v %s' nvidia-utils` → `extra/nvidia-utils 610.57.04-1 0`). **`%s` is
not a size field — take sizes from `pacman -Si` only.**

## 4. Pins and holds — measured, plus what `HoldPkg` does not mean [observed]

| source | probe | value |
|---|---|---|
| `/etc/pacman.conf:7` | `pacman-conf HoldPkg` | `pacman glibc` |
| `/etc/pacman.conf:8-11` | `pacman-conf Architecture` | `x86_64`; `CheckSpace`; `ParallelDownloads = 5`; `DownloadUser = alpm` |
| any | `pacman-conf IgnorePkg` | **empty** — no version pins |
| any | `pacman-conf IgnoreGroup` | **empty** |
| any | `pacman-conf NoUpgrade` / `NoExtract` | **empty** |
| `/etc/pacman.conf:15-16` | `SigLevel` / `LocalFileSigLevel` | `Required DatabaseOptional` / `Optional` |
| `/etc/pacman.conf:28-30` | `pacman-conf --repo omarchy SigLevel` | `PackageOptional,PackageTrustAll,DatabaseOptional,DatabaseTrustAll` |
| AUR helper | `yay 13.0.1-1` installed; `~/.config/yay/config.json` **absent**; `paru` not installed | no helper-level pin exists to read |
| `/etc/pacman.d/hooks/` | 3 operator hooks | `90-mkinitcpio-install.hook`, `99-limine.hook`, `walker-restart.hook` — none pins a version; all three couple an upgrade to a side effect |

- **`HoldPkg = pacman glibc` is not a version hold.** It protects those two
  packages from *removal* inside a transaction; it does not stop pacman or glibc
  from being *upgraded* [inference: `pacman.conf(5)` semantics, not exercised on
  this host — an upgrade was never run]. Reading it as a pin is the classic
  misread; the real pins here are the channel and the hooks.
- Hook couplings that will fire in a wave [observed, files read]:
  - `90-mkinitcpio-install.hook` (`:2-30`) — Path triggers
    `usr/lib/modules/*/extramodules/`, `usr/src/*/dkms.conf`,
    `usr/lib/firmware/*`, `usr/lib/initcpio/*` + Package triggers `mkinitcpio`;
    PostTransaction exec `/usr/share/libalpm/scripts/limine-mkinitcpio-install`
    ⇒ **kernel/firmware/dkms upgrade rebuilds the limine initramfs**.
  - `99-limine.hook` (`:2-10`) — on `limine` upgrade copies
    `BOOTIA32.EFI`/`BOOTX64.EFI` into `/boot/EFI/BOOT/` ⇒ the transaction writes
    the boot partition.
  - `walker-restart.hook` (`:2-11`) — on `walker`/`walker-debug`/`elephant*`
    upgrade, PostTransaction execs
    `/home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker` — a
    **user-owned, operator-writable script run by root inside the transaction**
    (file present: 709 B, mode 755) ⇒ cross-domain observation, reported not
    absorbed (secrets/privilege lane is kagi's; the fleet owner decides).
  - `/usr/share/libalpm/hooks/10-limine-snapper-lock.hook` (`:1-15`) —
    `Target = *`, PreTransaction, exec `/usr/share/libalpm/scripts/limine-snapper-lock`
    (10 lines) which sources `/usr/lib/limine/limine-mutex` (1270 B) ⇒
    `flock --timeout=30 /run/lock/boot-partition.lock`. **Every** transaction
    waits ≤ 30 s on the boot-partition lock; on timeout it prints `WARNING:
    Mutex lock timeout` and returns 1, but the hook's last command is
    `mutex_unlock`, so a timeout cannot fail the transaction [inference from the
    two scripts' text; both read in full]. It ran on the last three transactions
    (`pacman.log:2107`, `:2101`, `:2094`…).
- Trust surface, stated exactly: core/extra/multilib inherit
  `Required DatabaseOptional` (`:15`) — signature required for *packages*,
  optional for *databases* (and no `.db.sig` is stored anyway); `[omarchy]`
  overrides to `Optional TrustAll` (`:29`) ⇒ that channel is signature-optional
  *and* trust-any-key. `LocalFileSigLevel = Optional` (`:16`) ⇒ locally supplied
  packages (`pacman -U`) need no signature at all — one plausible path by which
  a local package can end up *ahead* of its channel (§5) [inference; the arrival
  path of `1password-beta` BETA-32 is [unknown]].

## 5. Shadowing and the downgrade trap [observed]

`/etc/pacman.conf:18` states the rule — "pacman searches repositories in the
order defined here" — order `[core]:19 → [extra]:22 → [multilib]:25 →
[omarchy]:28`. So a package present in two repos resolves to the **first**
repo's copy, and a *newer* copy in a lower-priority repo is **shadowed**.
Measured instances (name collisions across repos: **12** names; cross-check:
per-repo rows 297+14 954+181+231 = 15 663 vs `expac -S` distinct names 15 651 —
off by exactly the 12 collisions):

| name | effective (winner) | shadowed copy | shadow verdict |
|---|---|---|---|
| `linux-firmware-cirrus` (installed) | core `20260810-2` | omarchy `20260810-3` | **newer, shadowed** ⇒ why `-Qu` is empty |
| `ghostty`, `-nautilus`, `-shell-integration`, `-terminfo` | extra `1.3.1-2` | omarchy `1.3.1-3` | **newer, shadowed** (not installed) |
| `gpu-screen-recorder` (installed) | extra `6.1.0-1` | omarchy `5.12.3-2` | older, harmless |
| `pinta` (installed) | extra `3.1.2-2` | omarchy `3.1.2-1` | older, harmless |
| `asusctl`, `rog-control-center` | extra `6.4.0-2` | omarchy `6.4.0-1` | older, harmless |
| `intel-lpmd`, `opencode`, `umu-launcher` | extra `0.1.0-4` / `1.18.29-1` / multilib `1.4.4-1` | omarchy `0.1.0-2` / `1.1.51-1` / `1.1.3-1.1` | older, harmless |

⇒ Reading `-Qu` alone will *never* show the omarchy copy of a shadowed name.
Only 26 installed packages come from `[omarchy]` (`pacman -Sl omarchy` ∩
installed), so the blast radius is bounded, but the two soft-trust surfaces (§4)
plus shadowing mean "what the channel offers" ≠ "what `-Qu` says".

**Downgrade trap:** `1password-beta` installed `8.12.42_32.BETA-32` > channel
`8.12.42_32.BETA-1`. Plain `-Syu` leaves it (0 candidates); **`pacman -Suu`
would downgrade it to an older beta** (579.18 MiB installed size to rewrite).
[inference from observed versions + the documented meaning of the second `u`;
the downgrade itself was not run.]

## 6. Update-time hazard inventory (rows the decision table consumes) [observed]

- **No rollback net.** `snapper list-configs` prints a header-only table
  (`Config │ Subvolume`) with rc=0 — **zero configs**; `limine-snapper-sync` is
  `enabled` but `inactive`, and its PreTransaction lock hook still runs. Snapshot
  *tooling* exists without a snapshot *config*: any wave on this host is
  **snapshot-less** (`SKILL.md:45`; re-derived today).
- **Kernel/driver rebuild coupling is live.** `dkms status` =
  `nvidia/610.57.04, 7.2.3-arch1-3, x86_64: installed` **plus** the stale
  `nvidia/610.57.04, 7.1.4-arch1-1 … (Built modules are missing in the kernel
  modules folder)`. `ls /usr/lib/modules/` = `7.2.3-arch1-3` only; `uname -r`
  = `7.2.3-arch1-3`; `pacman -Q linux` = `7.2.3.arch1-3` ⇒ **no kernel reboot is
  pending today**, and a wave that raises `linux` triggers the dkms rebuild +
  initramfs hook in the same transaction. The stale row is evidence that a
  rebuild already failed/abandoned once on this box.
- **Foreign set has no rebuild path.** 16 packages (13 `elephant-*`,
  `omarchy-walker`, `android-apktool-bin`, `obsidian-cli-inspector`) are outside
  every repo; a wave that bumps their linked libs
  (`libqalculate`, `imagemagick`, `fd`, `sqlite`, `java-runtime`) can break them
  silently — [inference]; none of them links glibc/nvidia/kernel directly
  [observed: `pacman -Qi` Depends lines, 16/16 read].
- **Orphans 3** (`electron39 39.8.10-2`, `mbedtls 4.2.0-1`,
  `webp-pixbuf-loader 0.2.7-2`) — removable candidates, not upgrade blockers.
- **Transaction state clean.** No `/var/lib/pacman/db.lck`; `pacman -Dk` →
  `No database errors have been found!` (rc=0); log spans 2026-10-03 20:41:33 →
  2026-10-13 16:37:59 with **20** completed transactions (7 since the last
  wave).
- **Cache / headroom asymmetry.** `du -sh /var/cache/pacman/pkg` = **8.6 G**;
  exactly 1568 `*.pkg.tar.zst` + 1568 `*.sig` + **3** alpm temp dirs
  (3139 entries) — cache is never pruned, so superseded copies accumulate
  (harmless for safety, relevant to space hygiene). The 3 `download-*` dirs are
  `owner=alpm mode=700`, mtimes 2026-10-11 10:31 / 2026-10-13 13:52 /
  2026-10-13 16:21 (aligned with the last install transactions) — **contents
  unreadable non-root** ⇒ shape-only, [unknown] whether they hold partial files.
- **Power: AC-only, no UPS visible.** `/sys/class/power_supply/` is empty and
  DMI chassis type is 3 (desktop) ⇒ a power cut mid-transaction would leave
  `db.lck` and a half-written set; whether a UPS exists is [unknown] (not exposed
  read-only).
- **The box is busy with another workstream.** Load 0.68, memory 30 GiB total /
  10 GiB used / 372 MiB free (24 GiB buff/cache), swap 34 GiB with 710 MiB used;
  process census at 10:51 shows **75 × `ffmpeg`**, 1 × `kimi`, 3 × `strace`.
  Sibling-lane activity is also live: `tools/` appeared in this repo between
  10:44 (`ls` → no such directory) and 10:52 (`git status --short` → `?? tools/`,
  `?? plans/`) — i.e. the round's other lanes are writing while this note was
  measured.

## 7. Decision table — "is it safe to `-Syu` right now?" [arms from the rows above]

Arms (fixed vocabulary, no scalar): `PASS` · `INERT` (transaction would do
nothing) · `REQUIRES-PREP` · `BLOCKED` (probe cannot answer read-only) ·
`UNKNOWN-UPSTREAM` · `DO-NOT`. Composition rule: **the verdict is the strongest
arm fired**, ordered `BLOCKED > UNKNOWN-UPSTREAM > REQUIRES-PREP > INERT > PASS`;
every verdict carries its firing row and measured value so a non-author can
re-derive it.

| # | condition checked | probe | measured 2026-10-14 | arm |
|---:|---|---|---|---|
| 1 | sync-db content age | `stat -c '%w %y' /var/lib/pacman/sync/*.db` | content stamp 2026-09-08 = **36 d** (core/extra/multilib); local fetch 3 d | **UNKNOWN-UPSTREAM** |
| 2 | candidate set (what a refresh would install) | `pacman -Qu`, `-Sup --print-format` | **0 candidates**, 3 probes agree | **INERT** |
| 3 | critical class present in candidates | §3 class filter | none (empty set) | **PASS** |
| 4 | pins/holds declared | `pacman-conf IgnorePkg IgnoreGroup NoUpgrade NoExtract` | all empty; `HoldPkg = pacman glibc` (removal-only) | **PASS** (with §4 misread warning) |
| 5 | rollback net | `snapper list-configs` | **0 configs**; `limine-snapper-sync` enabled/inactive | **REQUIRES-PREP** |
| 6 | kernel/dkms rebuild path | `dkms status`, `ls /usr/lib/modules`, `uname -r` | current kernel covered; stale `7.1.4-arch1-1` row present | **REQUIRES-PREP** |
| 7 | trust surface for the wave | `pacman-conf --repo omarchy SigLevel`, `:16` | omarchy `Optional TrustAll`; `LocalFileSigLevel = Optional`; no `.db.sig` | **REQUIRES-PREP** (accept or re-scope channel) |
| 8 | boot partition pre-verification | `ls /boot` | `Permission denied`, rc=2 (non-root) | **BLOCKED** (operator probe) |
| 9 | space + space-check | `df -h / /boot`, `pacman-conf CheckSpace` | 850 G / 1.8 G free; CheckSpace on | **PASS** |
| 10 | transaction state | `ls /var/lib/pacman/db.lck`, `pacman -Dk`, log | no lock; `-Dk` clean; 20 transactions, 7 since last wave | **PASS** |
| 11 | downgrade trap | version join (§1) | `1password-beta` installed ahead of channel | **DO-NOT** (`-Suu`) |
| 12 | power loss exposure | `/sys/class/power_supply/`, DMI | empty (desktop, AC-only); UPS [unknown] | **PASS** (n/a) |
| 13 | concurrent workloads | `ps -eo comm=`, `git status` | 75 × `ffmpeg`, 1 × `kimi`, sibling lanes writing | **REQUIRES-PREP** (schedule) |
| 14 | upstream delta since the snapshot | — (needs network/`-Sy`) | not measurable read-only | **UNKNOWN-UPSTREAM** |

**Verdict lines (what the table composes to):**

1. **`-Syu` right now, as measured:** `INERT` / safe-by-emptiness — 0 package
   actions; the only effect is that the dbs are refreshed, which is precisely
   the mutation that invalidates row 2 and re-opens rows 1 and 14. Expect
   well under a minute (wave calibration: 81 s for 505 actions).
2. **`-Syu` right after that refresh (the question that matters):**
   **`UNKNOWN-UPSTREAM` + `REQUIRES-PREP`** — the candidate set is decided by the
   mirror snapshot at that moment, and 36 days of drift means kernel / libc /
   driver classes are in scope for it. It cannot be called safe or unsafe from
   this host read-only. Prep before running it: (a) decide the rollback story —
   configure a snapper/limine-snapper-sync config or accept snapshot-less in
   writing (row 5); (b) plan the dkms rebuild verification for the new kernel
   *before* the next reboot (row 6); (c) schedule around the running `ffmpeg`
   workstream and the sibling lanes (row 13); (d) accept the `[omarchy]`
   TrustAll channel or scope it out (row 7).
3. **`-Suu` / `-Syyu`: do not run.** `-Suu` downgrades `1password-beta` to an
   older beta (row 11); `-Syyu` re-downloads 36-day-stamped dbs for no benefit.
4. **The one probe that turns row 14 into a measurement** is upstream
   comparison — operator side only: install `pacman-contrib` and run
   `checkupdates`, or `-Sy` then re-run this note. The lane declines both:
   `checkupdates` is absent and installing it is out of province; `-Sy` is on
   the forbidden list (`SKILL.md:151-152`) [inference: `checkupdates`' internal
   mechanism — its script is not readable here because the package is absent].

## 8. Observation / inference / unknown

- **Observed:** every probe value in §1–§7 (commands and stamps in §10);
  `-Qu` empty ×3; skew census 1171/0/1; 15 663 per-repo rows vs 15 651 distinct;
  12 name collisions with 5 shadowed-newer; 16/16 foreign cross-check;
  36-day content stamp; `.db.sig` absent; `HoldPkg`/`IgnorePkg` values; hook
  texts and the `/run/lock/boot-partition.lock` flock; 81 s / 505 actions wave;
  snapper configs 0; dkms stale row; 8.6 G cache and the 3 alpm temp dirs;
  `/boot` rc=2; power_supply empty; 75 ffmpeg; `tools/` appearing mid-round.
- **Inference (not measured):** repo-order precedence is what makes
  `linux-firmware-cirrus` invisible to `-Qu` (rule at `pacman.conf:18` +
  measured empty `-Qu` + a newer omarchy copy); `HoldPkg` = removal-protection
  only; a dkms rebuild failure would degrade the driver plane at next boot; a
  soname bump in the libs the foreign set links would break it silently;
  `-Suu` would downgrade `1password-beta`; the lock hook cannot fail a
  transaction on timeout.
- **Unknown (open):** upstream Arch delta since 2026-09-08 (needs network);
  whether a UPS exists; contents of the 3 alpm temp dirs; the arrival path that
  left `1password-beta` ahead of its channel; whether the stable mirror's
  2026-09-08 stamp is a snapshot generation date or the upstream file mtime
  (either reading means ≥36 d of content lag, the exact semantics are unproven);
  the boot surface beyond the privilege gate; whether `walker-restart.hook`
  exec'ing a user-owned script as root is intended (operator question).

## 9. Errata / method corrections (append-only)

- 2026-10-14 — **Rejected first-pass candidate (false alarm).** A version join
  built from `expac -S '%n\t%v'` with *last-wins* dict semantics reported
  `BEHIND linux-firmware-cirrus 20260810-2 -> 20260810-3` as a live `-Qu`
  candidate. Wrong: with `pacman.conf:18` precedence (core first) the effective
  entry is core's `20260810-2`, equal to installed. Corrected census:
  1171 equal / **0 behind** / 1 ahead (re-run against a repo-ordered dump,
  `verdict-skew-corrected.txt`). The rejected output is kept — it is what
  exposed the shadowing case of §5.
- 2026-10-14 — **`--print-format '%s'` is not a size.** The regeneration recipe
  first used `%s` for download sizes; measured output was `0` for `nvidia-utils`
  (real: 300.73 MiB). Sizes in §3 all come from `pacman -Si`.
- 2026-10-14 — **Round-1 row refinement, not a contradiction:** `SKILL.md:45`
  names `HoldPkg = pacman glibc` under "pins/holds"; this note keeps the value
  but splits it from the true version pins (`IgnorePkg`/`IgnoreGroup`/
  `NoUpgrade`/`NoExtract`, all empty) and adds the second soft-trust surface
  `LocalFileSigLevel = Optional` (`/etc/pacman.conf:16`), which the round-1 row
  did not name.
- 2026-10-14 — the round's `-Qu` reading is deliberately *not* reconciled with
  the round-1 checklist's "`-Qu` empty rc=1": both are correct and 3 days apart
  only in refresh terms; the value differs in *meaning* (§2), not in digits.
- 2026-10-14 — **Self-audit pass (post-draft, pre-delivery).** §3's class sums
  were re-derived from `class-census.txt` in Python instead of by hand; two
  draft figures were wrong and are corrected in place: nvidia-class installed
  `1.56 GiB` → **1.53 GiB** (1563.91 MiB) and the wave installed total
  `≈2.7 GiB` → **≈2.50 GiB** (2554.53 MiB; download 1080.43 MiB = 1.06 GiB).
  Log citations re-pinned with `grep -n`: lock-hook lines are
  `2073/2091/2098/2105` (the draft's `2094/2101/2107` were the `transaction
  started` lines) and the final transaction spans `2104-2109` (draft said
  `2108-2111`). Lesson kept: hand-summed arithmetic and remembered line numbers
  are not anchors — both were replaced by re-derivation.

## 10. Sources (path:line)

- Config: `/etc/pacman.conf:7,8,9,11,15,16,18,19,22,25,28,29,30`;
  `/etc/pacman.d/mirrorlist:1` (58 B, 1 Server line);
  `/etc/pacman.d/hooks/90-mkinitcpio-install.hook:2-30`,
  `99-limine.hook:2-10`, `walker-restart.hook:2-11`;
  `/usr/share/libalpm/hooks/10-limine-snapper-lock.hook:1-15`,
  `35-systemd-update.hook:1-9`; `/usr/share/libalpm/scripts/limine-snapper-lock`
  (10 lines); `/usr/lib/limine/limine-mutex` (1270 B).
- Log: `/var/log/pacman.log:1405` (`-Sy fuse2`, birth match), `:1414` (last
  `-Syu`), `:1416`, `:1950` (completion, 81 s), `:2073,2091,2098,2105` (lock hook
  on the last four transactions), `:2104-2109` (final transaction 2026-10-13
  16:37, `installed git-filter-repo` at `:2107`).
- Scratch (ephemeral, `/tmp/tsukuroi-r2-2-scratch/`): `qu.txt` (0 lines),
  `qu.err` (0 B), `su-print.txt` (0 lines), `sync-name-ver.txt` + `local-name-ver.txt`
  (the two joins), `verdict-skew.txt` (false-candidate pass) +
  `verdict-skew-corrected.txt` (`common=1172 equal=1171 behind=0 ahead=1`),
  `sl-all.txt` (15 663 rows), `omarchy-installed.txt` (26), `class-census.txt`
  (§3 sizes), `q-foreign.txt`, `qm-names.txt` + `not-in-sync.txt` (diff clean),
  `q-orphan.txt`, `dk.txt`.
- In-lane: `SKILL.md:45` (round-1 update-safety row), `:151-153` (forbidden
  verbs), `:85-135` (11-step checklist this note extends), `LOG.md:28`
  (`offline.db` open item, closed in §2), `corpus/QUALITY.md:1-5` (admission
  bar: every claim falsifiable, sources cited, errata append-only),
  `PROVINCE.md:5-12,16-17`, `plans/round-2.plan.md:9` (this artifact's mandate).
- Sibling notes: `corpus/knowledge/package-state-plane.md` (trust surface,
  keyring, cache), `driver-firmware-plane.md` (dkms/GSP detail),
  `systemd-user-plane.md` (snapper residue).

## 11. Boundary notes for the next pass

- Reported, not absorbed: `walker-restart.hook`'s root-exec of a user-owned
  script (privilege/secrets shape → kagi or the operator); the `1password-beta`
  provenance question; the 3 alpm temp dirs (privilege gate).
- Not written by this lane: a `LOG.md` entry for this artifact (assignment
  constrained this run to the single note file). Round-2 lanes must append one
  per `AGENTS.md:3`.
- This note is a **timestamped snapshot** — nothing here may be quoted as
  current state. Re-measure with §3's recipe and `SKILL.md:85-135`.
