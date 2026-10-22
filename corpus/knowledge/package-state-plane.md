# Package-state plane — measured anchors (TSUKUROI-1)

Measured: 2026-10-14 09:53–10:02 -0300, host `plazir27`, user `vgpnk`
(non-root), Arch Linux rolling, kernel 7.2.3-arch1-3, pacman 7.1.0.r9.g54d9411-2
(libalpm 16.0.1). All probes read-only. Qkk runs executed with warm page
cache; scratch evidence in `/tmp/tsukuroi-*` (ephemeral — key excerpts
embedded below). Claims are tagged [observed] / [inference] / [unknown].

## Fact — /etc/pacman.conf: no version pins, one soft-trust repo [observed]

`/etc/pacman.conf` is 30 lines. Effective values re-read via `pacman-conf`
(merged config, non-root safe):

| line | directive | effective (`pacman-conf`) |
|---:|---|---|
| 4–6 | `Color`, `ILoveCandy`, `VerbosePkgLists` | cosmetic |
| 7 | `HoldPkg = pacman glibc` | `pacman\|glibc` |
| 8 | `Architecture = auto` | `x86_64` |
| 9 | `CheckSpace` | active |
| 10 | `ParallelDownloads = 5` | 5 |
| 11 | `DownloadUser = alpm` | pacman 7 download sandbox user |
| 15 | `SigLevel = Required DatabaseOptional` | global |
| 16 | `LocalFileSigLevel = Optional` | local files |
| 19–26 | `[core]`, `[extra]`, `[multilib]` | via `/etc/pacman.d/mirrorlist` |
| 28–30 | `[omarchy]` | `SigLevel = Optional TrustAll`, `Server = https://pkgs.omarchy.org/stable/$arch` |

- `pacman-conf IgnorePkg` / `IgnoreGroup` print empty — no pins/holds beyond
  `HoldPkg`. Nothing here blocks an `-Syu` of any package.
- `/etc/pacman.d/mirrorlist` is one line (58 B):
  `Server = https://stable-mirror.omarchy.org/$repo/os/$arch`. core/extra/
  multilib all resolve through that omarchy-hosted mirror.
- `[omarchy]` is the only repo with non-default SigLevel. Its packages ARE
  signed: `gpg --verify` on cached `walker-2.17.0-1` → `Good signature from
  "Omarchy <pkgs@omarchy.org>"` (EDDSA `40DFB630…80CAC571`, made 2026-07-26).
  `Optional TrustAll` means pacman does not require that signature.
- [inference] Distribution trust here concentrates in the omarchy channel
  (single mirror + soft-trust repo); the stock `Required` level still covers
  core/extra/multilib content.
- [unknown] Whether `stable-mirror` lags upstream Arch (needs network; out
  of scope for read-only rounds).

## Fact — census: 1188 installed, 16 foreign [observed]

`pacman -Q | wc -l` = 1188; `pacman -Qe` = 207 explicit (981 deps derived);
`pacman -Qm` = 16 foreign; `pacman -Qme` = 3 explicit foreign.

```
android-apktool-bin 3.0.3-1          elephant-runner 2.21.0-1
elephant 2.21.0-1                    elephant-symbols 2.21.0-1
elephant-bluetooth 2.21.0-1          elephant-todo 2.21.0-1
elephant-calc 2.21.0-1               elephant-unicode 2.21.0-1
elephant-clipboard 2.21.0-1          elephant-websearch 2.21.0-1
elephant-desktopapplications 2.21.0-1  obsidian-cli-inspector 1.0.3-1
elephant-files 2.21.0-1              omarchy-walker 1.0.0-2
elephant-menus 2.21.0-1
elephant-providerlist 2.21.0-1
```

- Explicit-foreign: `android-apktool-bin`, `obsidian-cli-inspector`,
  `omarchy-walker` (meta; the 13 `elephant-*` are its deps).
- `omarchy-walker` declares the elephant family as Depends On (`pacman -Qi`).
- Provenance split:
  - apktool + obsidian-cli: yay build caches exist
    (`~/.cache/yay/<pkg>/`); installed 2026-10-13 13:52 / 16:21. [observed]
  - elephant family + omarchy-walker: NOT in the omarchy sync db
    (`pacman -Si elephant` → not found; `pacman -Sl omarchy | grep elephant`
    → empty), no yay cache; installed 2026-10-03 17:44:26 (setup day) and
    cached in `/var/cache/pacman/pkg/` WITH `.sig` files. Packager: "Unknown
    Packager". [observed] Channel that supplied them: [unknown].
- `yay 13.0.1` installed (AUR helper); `paru` absent. [observed]
- `pacman -Qu` = 0 rows vs sync db (local ≤ sync versions for everything).

## Fact — sync/local db state, and the mtime trap [observed]

- All four configured sync dbs were **born** 2026-10-11 12:54:13.542:
  `core.db`, `extra.db`, `multilib.db`, `omarchy.db` (`stat -c '%w'`).
  Their mtimes differ and are server-side: core `2026-09-08 15:23:46`,
  extra `:47`, multilib `:45`, omarchy `2026-10-11 10:16:17`.
  ⇒ pacman preserves upstream file mtimes on download; **mtime ≠ datetime
  of the local sync**. Use `%w` (birth) or `%z` (ctime) for arrival dating.
  [observed; corrected a first-pass misread of mtimes — see Errata]
- `offline.db` (304318 B) born 2026-10-03 17:41:33 (installer day), mtime
  2026-07-20; not in any `[section]` — `pacman -Sl offline` → `error:
  repository "offline" was not found`. Dead leftover file; not queried by
  pacman. [observed]
- Local db: `/var/lib/pacman/local` holds 1188 dirs == 1188 pkgs; 1 file
  (`ALPM_DB_VERSION`, content `9`); no package dir lacks `desc` [observed].
  ⚠ a naive `comm` of `ls` dirs (`name-version`) against `pacman -Qq`
  (`name`) is invalid — do not use; count instead (see Errata).
- Last local-db write: inode mtime 2026-10-13 16:37:59 (= newest cache
  arrival, `git-filter-repo-2.47.0-3`). [observed]

## Fact — keyring: initialized, populated 2026-10-11 [observed]

- `/etc/pacman.d/gnupg`: master key minted **2026-10-03** (rsa4096,
  `Pacman Keyring Master Key <pacman@localhost>`, [ultimate]); `pubring.gpg`
  (1376743 B) and `trustdb.gpg` (13440 B) mtime **2026-10-11 16:14:29** ≈
  `archlinux-keyring 20260902-1` install time (16:14:27) — i.e. last
  populate/update ≈ install day of that package.
- `pacman-key --list-keys`: rc=0 (non-root, read-only), **184 pub**, 230 sub.
  Hygiene note: no `pubring.kbx`; `secring.gpg` present but 0 B; a
  `pubring.gpg~` backup exists.
- Bracket tags in the listing (counts tag lines, incl. uid/sub rows — not
  key counts): `[unknown] 190, [full] 84, [expired] 67, [revoked] 35,
  [marginal] 35, [undef] 33, [ultimate] 1`. Tagged expired/revoked keys are
  normal shape for a distro keyring that carries historical revocations;
  not a defect signal by themselves. [observed + interpretation note]
- Non-root stderr on listing: `gpg: Note: trustdb not writable` — listing
  works read-only; `--refresh-keys` / `--populate` need root. [observed]
- `openpgp-revocs.d/` and `private-keys-v1.d/` are mode 700 root — not
  readable at this privilege level (shape-only; not read). [observed]
- `pacman-key` master key age is ~11 days; last data update ≈ Oct 11.

## Fact — cache shape: 8.6 G, 1568 archives, arrival-dated by ctime [observed]

- `/var/cache/pacman/pkg`: `du -sh` = **8.6 G** (excludes 3 unreadable
  `download-*` subtrees, see below); dir birth 2026-10-03 17:41:30
  (install day).
- Composition: 1568 `*.pkg.tar.zst` + 1568 `*.sig` (1:1, every archive
  paired) + 0 `.part` in the readable tree.
- Arrival dating by ctime (`-newerct` buckets, boundary = install 2026-10-03
  17:41:31 and last sync 2026-10-11 12:54:15):
  - before install: **0**
  - install window (Oct 3 → Oct 11 sync): **1034**
  - after last sync: **534**
  - oldest arrival: `linux-7.1.4.arch1-1` @ 2026-10-03 17:41:47
    (superseded by installed 7.2.3.arch1-3 from Oct 11)
  - newest arrival: `git-filter-repo-2.47.0-3` @ 2026-10-13 16:37:59
- mtime vs ctime example: `aalib-1.4rc5-19` mtime 2025-11-09 (upstream
  build stamp) but ctime 2026-10-03 17:44 (actual download). The mtime span
  2025-11-09..2026-10-09 is upstream build dates, **not** cache age.
  [observed; same mechanism proven on sync dbs]
- Largest 5 (`du -m … | sort -rn | head`): jdk21-openjdk 335M,
  nvidia-utils 610.57.04 301M, nvidia-utils **610.43.03** 301M (superseded
  copy), noto-fonts-cjk 189M, 1password-beta 187M. Superseded duplicates
  are cached (nvidia 610.43.03 vs installed 610.57.04) — cache is
  never-pruned accumulation.
- 3 leftover `download-*` dirs, mode 700 `alpm:alpm` (owner = DownloadUser,
  pacman.conf:11): mtimes 2026-10-11 10:31, 2026-10-13 13:52, 2026-10-13
  16:21 — the last two correlate with the yay installs of that day.
  Contents not readable at vgpnk level → [unknown], and true cache size is
  ≥ 8.6 G.
- `paccache` not installed (`pacman-contrib` absent) → no pruning tooling;
  consistent with the 11-month accumulation.

## Fact — `pacman -Qkk` sample (timed, bounded) [observed]

Command form per package: `timeout 45 pacman -Qkk <pkg>` (wall from
`date +%s%N`). rc semantics: 0 = no altered files; 1 = ≥1 altered file;
backup-file diffs alone do NOT set rc (glibc/pambase prove rc=0 with diffs).

| package | total files | rc | wall | notable output |
|---|---:|---:|---:|---|
| pacman | 426 | 0 | 18 ms | backup: `/etc/pacman.conf` (mtime/size/sha) |
| glibc | 1637 | 0 | 88 ms | backup: `/etc/locale.gen` |
| systemd | 1909 | **1** | 70 ms | `warning: /var/log/journal (GID mismatch)` — 1 altered |
| linux | 7705 | 0 | 403 ms | clean |
| omarchy-walker | 0 | 0 | 6 ms | meta package, no files |
| android-apktool-bin | 7 | 0 | 12 ms | clean (AUR bin, mtree present) |

Extra probes for the non-root false-positive class (same form): `sudo`
244 files rc=1 21 ms — `warning: /etc/sudoers (failed to calculate SHA256
checksum)` (file is 440 root:root, unreadable by vgpnk); `shadow` 534 rc=1
27 ms — `/etc/default/useradd` (600 root:root) same class; `pambase`
rc=0 with `/etc/pam.d/system-auth` backup diffs.

## Fact — `pacman -Qkk` full sweep (bounded 240 s; completed in 17 s) [observed]

`timeout 240 pacman -Qkk > /tmp/tsukuroi-qkk-full.txt 2>&1` → **rc=1,
wall ≈17 s**, 1332 raw lines, all 1188 packages covered. Non-tty output
interleaves progress with `\r`: normalize with `tr '\r' '\n'` before
parsing (1184/1188 summaries parse cleanly: 1166 × 0 altered + 18 × ≥1
altered; 4 packages' summary lines were lost or malformed in the
interleave, fragments seen for groff and libplacebo). Costs on this host (1188
pkgs, warm cache): a full verify is ~17 s — cheap enough as a routine gate;
cold-cache cost [unknown].

Classified after normalization:

- **Backup-file diffs (benign, user config): 86 lines** (mtime/size/sha
  triplets; e.g. 31 × "Modification time mismatch"). These are expected
  edits (`/etc/pacman.conf`, `/etc/locale.gen`, `/etc/systemd/logind.conf`,
  `/etc/pam.d/system-auth`, …) and do not set rc=1.
- **Non-root artifacts — needs a root run to resolve (36 lines):**
  - 32 × `(failed to calculate SHA256 checksum)` in 10 packages:
    cups 10, ufw 8, filesystem 6, audit 2, cups-browsed 1, cups-pdf 1,
    dbus 1, openssh 1, shadow 1, sudo 1.
  - 4 × `(Permission denied)`: amd-ucode `/boot/amd-ucode.img`,
    asdcontrol `/etc/sudoers.d/50-asdcontrol`, cups `/var/cache/cups/rss`,
    `/var/spool/cups/tmp`.
- **Metadata drift (visible non-root) — 17 lines, the triage list:**

| class | path (package) | actual fs state |
|---|---|---|
| Permissions ×8 | `/boot` (filesystem, amd-ucode) | 700 root:root |
| | `/usr/bin/op` (1password-cli) | 2755 root:onepassword-cli |
| | `/opt/1Password/1Password-BrowserSupport` (1password-beta) | 2755 root:onepassword |
| | `/usr/lib/utempter/utempter` (libutempter) | 2755 root:utmp |
| | `/etc/cups/{classes,printers,subscriptions}.conf` (cups) | reported only |
| GID ×4 | same `op`, `1Password-BrowserSupport`, `utempter` above; `/var/log/journal` (systemd) | journal: 981 (`systemd-journal`) |
| File type ×3 | `/etc/resolv.conf` (filesystem) | symlink → `/run/systemd/resolve/stub-resolv.conf` |
| | `Yaru … go-next/go-previous-symbolic.svg` (yaru-icon-theme) | symlinks → Adwaita |
| Symlink path ×2 | `/usr/lib/jvm/default`, `default-runtime` (java-runtime-common) | both → `java-21-openjdk`, retargeted Oct 12 |
| mtime/size/sha non-backup ×7 | `/etc/passwd` (filesystem, Size) | accounts added — expected |
| | `/etc/ufw/user.rules` (ufw, Size) | user-edited rules |
| | `/usr/bin/powerprofilesctl` (**mtime + size + sha**, power-profiles-daemon) | content differs from package — strongest content-drift signal this run |

- **18 packages with ≥1 altered file:** cups(12), ufw(8), filesystem(8),
  yaru-icon-theme(2), java-runtime-common(2), audit(2), amd-ucode(2),
  then 1 each: systemd, sudo, shadow, power-profiles-daemon, openssh,
  libutempter, dbus, cups-pdf, asdcontrol, 1password-cli, 1password-beta.
  1166 summary lines report 0 altered. No non-backup SHA mismatch was
  observed other than `powerprofilesctl` — i.e. no broad content
  corruption; the rc=1 sweep result decomposes into ~20 real metadata
  drifts + ~36 privilege artifacts above. [observation + inference]

### Reading `-Qkk` output as non-root (decision table)

| message class | meaning | action |
|---|---|---|
| `backup file: … (Modification time/Size/SHA256 mismatch)` | user-edited config | ignore (expected); rc stays 0 |
| `(failed to calculate SHA256 checksum)` | file unreadable at current privilege | re-run as root before judging |
| `(Permission denied)` | unreadable dir/path | re-run as root |
| `(GID\|UID\|Permissions mismatch)` | fs metadata ≠ package db | triage list above; several are setgid binaries with dynamic groups |
| `(File type/Symlink path mismatch)` | regular-file↔symlink or retargeted symlink | verify the retarget was deliberate (jvm/resolv.conf classes) |
| `(SHA256 checksum mismatch)` on non-backup file | content differs | investigate first (this run: only `powerprofilesctl`) |

## Errata / method corrections (append-only)

- 2026-10-14 — First-pass reconciliation of `/var/lib/pacman/local` dirs vs
  `pacman -Qq` via `comm` was **invalid**: dir names are `name-version`,
  `-Qq` prints `name`, so the diff printed every package (false alarm).
  Correct method: count dirs (1188) vs pkgs (1188). Rejected output kept
  for taste.
- 2026-10-14 — Cache/sync "age" read from mtimes was wrong: pacman
  preserves upstream mtimes on download (proven by sync-db birth 2026-10-11
  vs mtime 2026-09-08). Use `%w`/`%z` (birth/ctime) for arrival dating.
- 2026-10-14 — Full `-Qkk` sweep output must be `tr '\r' '\n'`-normalized
  before parsing; raw line counts undercount package summaries.

### Wave-1 errata applied (2026-10-14 10:47–10:52 -0300, re-measured; append-only)

Wave-1 record sources: `SKILL.md:206-233` (errata/pending), `LOG.md:33-38`
(open list), `CORPUS.md:17` (field contract). All probes re-run read-only at
the times shown; scratch `/tmp/tsukuroi-r2-3-work/`. Numbers below are today's
re-measurements, not the note's.

- 2026-10-14 — **full sweep re-measured**: `timeout 240 pacman -Qkk >
  /tmp/tsukuroi-r2-3-work/qkk-full.txt 2>&1` → rc=1, 1332 raw lines, wall
  **15.34 s** (note: ~17 s). CR bytes in this output = **0** (`grep -c $'\r'`),
  yet 6 summaries are spliced by interleaved `warning:` output and 2 are
  name-split: `cups-browsed: 36 totalwarning: …` (`qkk-full.txt:116`),
  `pipewire-als` … `a: 12 total files, 0 altered files` (:954-958), `xx` …
  `hash: 27 total files, 0 altered files` (:1308-1310). The `tr '\r' '\n'`
  correction above is therefore necessary but **not sufficient** on this run;
  a splice-aware parse is required. [observation]
- 2026-10-14 — **18-vs-19 resolved by measurement** (`SKILL.md:228-230` said
  "resolve by root re-run"): strict-complete summaries 1182 = 1164 × `0 altered`
  + **18 × ≥1 altered** (same 18 packages as :207-211); the orphan fragment
  ` files, 1 altered file` (:121, between cups-browsed's truncated line and
  cups-filters) restores **cups-browsed = 1** → **19** packages with ≥1 altered
  [inference: fragment attribution by alphabetical position, as in the round-1
  scribe reconciliation]. `libplacebo: 48 total fi…` (:676) and
  `msgpack-c: 34 total f…` (:865) lose the altered field this run → exact count
  is ≥19. No drift; the delta was a parse artifact. [observation + inference]
- 2026-10-14 — **sync-db births re-measured identical**: core/extra/multilib/
  omarchy `%w` = 2026-10-11 12:54:13.542054496; `offline.db` `%w` =
  2026-10-03 17:41:33.994891750, mtime 2026-07-20, 304318 B, still not a
  configured repo (`pacman -Sl offline` → not found) — carries the round-1
  "offline.db coverage" open item (`LOG.md:28-31`). [observation]
- 2026-10-14 — **root `-Qkk` delta still open**: resolving probe remains an
  operator root run; today's non-root re-run reproduces the same failed-calc /
  permission-denied classes (:184-190). No sudo used; privilege gate recorded,
  not escalated. [unknown]
- 2026-10-14 — **judgment-class erratum — rollback net retracted.** The wave-1
  first-pass inference (snapshot coverage from `snapper`/`limine-snapper-sync`
  + pacman hook) is withdrawn: `snapper list-configs` → empty table, rc=0,
  while `snapper 0.13.1-3` and `limine-snapper-sync 1.31.0-1.1` are installed →
  no rollback net is configured. Kept as erratum, not laundered into the body.
  [inference → retracted]
- 2026-10-14 — **field-contract erratum**: this note opens with measured-date
  prose, not the contracted literal keys (`CORPUS.md:17`, `LEARNING.md:59-60`).
  Contract-satisfying values, appended (header rewrite deferred — append-only):
  `source:` live read-only probes, host `plazir27`, non-root; `verified-at:`
  2026-10-14 (wave-1 audits) + this errata re-measure; `recheck:` full
  `pacman -Qkk` sweep; `stat -c '%w' /var/lib/pacman/sync/*.db`; `pacman -Qu`.
  [observation]

## Unknowns (open probes)

1. Root-run `-Qkk` deltas for the 32 failed-calc + 4 permission-denied
   lines (expected to clear; may reveal further drift).
2. Expected GID/mode values behind the mismatches — local `mtree` files
   carry no uid/gid fields, so the comparison source for `(GID mismatch)`
   is unverified.
3. Contents/size of the 3 `download-*` dirs (700 alpm; true cache size may
   exceed 8.6 G).
4. Channel that supplied elephant-* / omarchy-walker (not current sync db,
   not yay cache; sigs present in cache); whether they were removed from
   the omarchy repo since 2026-10-03.
5. Upstream freshness of the omarchy stable mirror (needs network;
   `-Qu`=0 only proves local == sync-db).
6. Whether `/usr/bin/powerprofilesctl` drift is a deliberate omarchy patch
   (operator question).

## Errata (round 4)

- 2026-10-14 (TSUKUROI-ERR-S sweep) — **header pins re-verified, hold.** `pacman -Q pacman`
  → `7.1.0.r9.g54d9411-2`; `pacman --version` → `Pacman v7.1.0 - libalpm v16.0.1`; `uname -r`
  → `7.2.3-arch1-3` — byte-identical to the header pin (`:3-5`). No stale pin on this note.
  [observed]
- 2026-10-14 — **field-contract erratum** (same class as `driver-firmware-plane.md:239`): the
  header carries measured-date prose, not the contracted literal keys (`CORPUS.md:17` — "Each
  `knowledge/` entry opens with `source:`, `verified-at:` and `recheck:`"). Appended values:
  `source:` live read-only probes — `pacman -Q*` / `pacman -Qkk` / `pacman-conf` / `pacman-key`
  / `stat` / `du` on host `plazir27`, user `vgpnk`, non-root; `verified-at:` 2026-10-14 (round-4
  re-check of the header pins only; body captures keep their own stamps); `recheck:`
  `pacman -Q pacman; pacman --version; uname -r` for the header pins + the Appendix probe set.
  [observation]
- 2026-10-14 — **md5-pin consequence:** this append changes this file's md5 and line count, so
  `host-health-report-r3.md` §5's pin for this note (`24eafc4067f6ca7bf3608dfff5ff63d6`, 303
  lines, measured 11:46–11:58) is superseded as of this block; post-append values recorded in
  that report's round-4 errata. [observation]

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — read-only `pacman -Q*`/`-Qkk`, `pacman-conf`, `pacman-key`, sync-db stat and cache-size probes on host `plazir27`, 2026-10-14; S032 `/var/log/pacman.log` where used.
verified-at: 2026-10-14 (the package-state captures and subsequent header-pin rechecks recorded in this note).
recheck: 90d; procedure: `pacman -Q pacman; pacman --version; uname -r` for header pins plus the Appendix probe set.


## R17-RECHECK — steer-safe procedure

Appended 2026-10-20 by the tsukuroi round-17 L1; earlier bytes unchanged. Supersedes the package-manager invocations in this file's `recheck:` line for any round whose steer forbids running pacman (QUALITY 26); file reads replace them and the substitution is recorded in that round's report. Read-only.

- `ls -d /var/lib/pacman/local/pacman-[0-9]*` (version is the directory-name suffix)
- `uname -r`
- Appendix probes that invoke pacman are replaced by reads of `/var/lib/pacman/local/<pkg>-<ver>/desc` and `/var/log/pacman.log`, or recorded as [unk]


## R18-FRESHNESS — local-db entry inventory 1395, not an independent package query

Appended 2026-10-20 by round-18 NoticePackages. Historical snapshots preserved: the bytes quoted above stay unchanged. This notice supersedes that current-use statement only. Read-only scope: no package, reboot, or upgrade clearance.

Current-use statement superseded: "`pacman -Q | wc -l` = 1188". Now: S060 lists1395 local-db entries excluding ALPM_DB_VERSION at16:06. This is a directory inventory, not an independently rerun pacman-Q package count. Supporting context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:24-26

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:25 — "1395". Source S060 (R18 L1 read-only capture).

## R18-FRESHNESS — local DB entry count 1188 to 1395

Appended 2026-10-20 by round-18 NoticePackages. Historical snapshots preserved: the bytes quoted above stay unchanged. This notice supersedes that current-use statement only. Read-only scope: no package, reboot, or upgrade clearance.

Current-use statement superseded: "holds 1188 dirs == 1188 pkgs". Now: The local database holds 1395 non-ALPM_DB_VERSION entries at R18; the 1188 figure is historical.

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:25 — "1395". Source S060 (R18 L1 read-only capture).

## R18-FRESHNESS — sync-directory DB-file inventory, configured set unknown (2026-10-20)

Appended 2026-10-20 by round-18 NoticePackages. Historical snapshots preserved: the bytes quoted above stay unchanged. This notice supersedes that current-use statement only. Read-only scope: no package, reboot, or upgrade clearance.

Current-use statement superseded: "All four configured sync dbs were **born**". Now: the S060 sync-directory listing contains five .db files, not a reverified count of configured repositories. pacman.conf and current repository configuration were not reread here. Supporting context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:40-55

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:53 — "openai-chatgpt.db". Source S060 (R18 L1 read-only capture).

## R18-FRESHNESS — offline.db absent from sync listing

Appended 2026-10-20 by round-18 NoticePackages. Historical snapshots preserved: the bytes quoted above stay unchanged. This notice supersedes that current-use statement only. Read-only scope: no package, reboot, or upgrade clearance.

Current-use statement superseded: "`offline.db` (304318 B) born 2026-10-03 17:41:33". Now: No offline.db appears in the R18 listing of /var/lib/pacman/sync, which shows six entries. The dead-leftover description of offline.db is historical. [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:48-55]

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:54 — "openai-chatgpt.db.sig". Source S060 (R18 L1 read-only capture).

## R18-FRESHNESS — local-db directory mtime, last content-write time unestablished

Appended 2026-10-20 by round-18 NoticePackages. Historical snapshots preserved: the bytes quoted above stay unchanged. This notice supersedes that current-use statement only. Read-only scope: no package, reboot, or upgrade clearance.

Current-use statement superseded: "Last local-db write: inode mtime 2026-10-13 16:37:59". Now: the local database directory inode mtime is2026-10-20 13:23:08.487645035 -0300; this is not an audit of the latest write to an existing desc file. Exact last local-database write time is unestablished. S060 ends with a13:23:09 pacman-D invocation; S065 separately records zcode ALPM completion13:23:09. Supporting context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:40-41, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:62-66, .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:97-105

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:41 — "2026-10-20 13:23:08.487645035 -0300 /var/lib/pacman/local". Source S060 (R18 L1 read-only capture).

## R18-FRESHNESS — keyring last data update claim not re-established

Appended 2026-10-20 by round-18 NoticePackages. Historical snapshots preserved: the bytes quoted above stay unchanged. This notice supersedes that current-use statement only. Read-only scope: no package, reboot, or upgrade clearance.

Current-use statement superseded: "`pacman-key` master key age is ~11 days; last data update ≈ Oct 11.". Now: Keyring data-update time is not established at R18. /usr/share/pacman/keyrings/archlinux.gpg has filemtime 2026-09-09 04:45:27 -0300, a file timestamp rather than an update or transaction time. The last captured pacman.log event is 2026-10-20 13:23:09 -0300 and does not by itself identify a keyring update. Pubring mtime, keyring install time and master-key age were not measured at R18. [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:62-74]

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:90 — "2026-09-09 04:45:27.000000000 -0300 /usr/share/pacman/keyrings/archlinux.gpg". Source S060 (R18 L1 read-only capture).

## R18-FRESHNESS — installed keyring package 20260902-1 to 20260909-1

Appended 2026-10-20 by round-18 NoticePackages. Historical snapshots preserved: the bytes quoted above stay unchanged. This notice supersedes that current-use statement only. Read-only scope: no package, reboot, or upgrade clearance.

Current-use statement superseded: "`archlinux-keyring 20260902-1` install time (16:14:27)". Now: The installed keyring package at R18 is archlinux-keyring-20260909-1 in the local database, not 20260902-1. Its install time was not measured.

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:28 — "/var/lib/pacman/local/archlinux-keyring-20260909-1". Source S060 (R18 L1 read-only capture).

## R18-FRESHNESS — paccache present, not absent

Appended 2026-10-20 by round-18 NoticePackages. Historical snapshots preserved: the bytes quoted above stay unchanged. This notice supersedes that current-use statement only. Read-only scope: no package, reboot, or upgrade clearance.

Current-use statement superseded: "`paccache` not installed (`pacman-contrib` absent)". Now: /usr/bin/paccache is present at R18 and pacman-contrib-1.13.1-1 is in the local database (capture line 36). The no-pruning-tooling statement is historical; pruning behaviour and cache contents were not re-measured. [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:82-86]

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:83 — "/usr/bin/paccache". Source S060 (R18 L1 read-only capture).

## R18-FRESHNESS — snapper configs present, rollback coverage unmeasured

Appended 2026-10-20 by round-18 NoticePackages. Historical snapshots preserved: the bytes quoted above stay unchanged. This notice supersedes that current-use statement only. Read-only scope: no package, reboot, or upgrade clearance.

Current-use statement superseded: "no rollback net is configured". Now: S060 observes snapper configuration names home/root and settings, not a current snapshot inventory. Earlier R17 captures recorded snapshots#1/#2 ro=true and list-configs home/root; their persistence into R18 and restoration feasibility are not established. Supporting context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:75-81, .ufo/waves/round-17/l1-capture/boot-chain-capture.txt:159-167, .ufo/waves/round-17/l1-capture/fresh-capture.txt:42-46

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:80 — "SNAPPER_CONFIGS="root home"". Source S060 (R18 L1 read-only capture).

## R18-FRESHNESS — kernel pin 7.2.3 to 7.2.11

Appended 2026-10-20 by round-18 NoticePackages. Historical snapshots preserved: the bytes quoted above stay unchanged. This notice supersedes that current-use statement only. Read-only scope: no package, reboot, or upgrade clearance.

Current-use statement superseded: "byte-identical to the header pin (`:3-5`)". Now: uname -r at R18 is 7.2.11-arch1-1, not 7.2.3-arch1-3; the 2026-10-14 header-pin hold is historical. [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:5-7, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:92-96]

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:6 — "7.2.11-arch1-1". Source S060 (R18 L1 read-only capture).

## R18-FRESHNESS — elephant base package 2.21.0 to 2.22.1

Appended 2026-10-20 by round-18 NoticePackages. Historical snapshots preserved: the bytes quoted above stay unchanged. This notice supersedes that current-use statement only. Read-only scope: no package, reboot, or upgrade clearance.

Current-use statement superseded: "elephant 2.21.0-1". Now: The elephant base package is elephant-2.22.1-1 in the local database at R18 (capture line 30), and a pacman -U log entry dated 2026-10-20 09:31:03 -0300 lists elephant-2.22.1-1 among its inputs (capture line 72). The 2.21.0-1 census entry is historical; other elephant-* sub-package versions were not re-measured.

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:30 — "/var/lib/pacman/local/elephant-2.22.1-1". Source S060 (R18 L1 read-only capture).


## R18-FRESHNESS — remaining package census and reachability neighbors (2026-10-20)

Sources S060/S065 and earlier S051/S052. These notices cover the complete named neighboring paragraphs, preserving all original dated receipts.

- R18-FRESH-SUPPLEMENT-45: the old foreign16/explicit-foreign3 and explicit207 figures remain dated observations, not a current classification. S060 counts local-db entries and records later archive names; S065 records package events but neither capture classifies the present foreign/explicit set [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:24-39, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:70-74]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:25.

- R18-FRESH-SUPPLEMENT-46: the old zero-pending readings at71 and302 are not current pending results. S060 contains no pending query result, and S065 historical package events cannot yield current pending updates; current pending count is UNKNOWN, not assertedzero [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:1-99]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:24.

- R18-FRESH-SUPPLEMENT-47: the no-repository/no-yay-cache wording at65–69 and298–300 is historical. S060 records yay-cache archive paths and S065 confirms historical elephant upgrades, but present configured repository membership and archive/cache persistence were not re-probed here [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:70-74, .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:40-69]. Capture: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:43.

- R18-FRESH-SUPPLEMENT-48: S060 lists snapper0.13.2-1 and limine-snapper-sync1.32.1-2 in local metadata and config names home/root. The old versions and empty-config current-use reading at277–279 are superseded; R17 snapshots remain historical observations, not proof of present persistence/restore [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:75-81, .ufo/waves/round-17/l1-capture/boot-chain-capture.txt:159-167]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:31.

No binary package query, configuration write, restart, rebuild or recovery action was performed or authorized by this notice.


## R24 notice — stable mirror lag answered (2026-10-22)

Appended; the `[unknown]` line above stays as written. The omarchy stable mirror holds the Arch snapshot of the current omarchy release and advances only by promotion (S100); its core.db Last-Modified was 2026-10-22 04:40:03 UTC at capture time (S101), after the host's last database download of 2026-10-18. Detail: `corpus/knowledge/pause-lift-gate-r24.md` P4.
