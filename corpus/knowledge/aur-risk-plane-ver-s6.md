# VER-S6 — independent recompute of two AUR-risk rows (confirm/refute)

source: independent read-only probes by the VER-S6 seat, host `plazir27`, user `vgpnk`,
non-root, own commands run 2026-10-14 17:39:47Z–17:54:55Z (14:39–14:54 -03) — i.e. starting
1 min 38 s after the author's own run window opened and continuing 11 min 54 s past its close
(`aur-risk-plane.md` header: 14:38:09–14:43:01 -03), on the same host but with the verifier's
own commands; overlaps are concurrent live reads, not copied results.
Target of verification: `corpus/knowledge/aur-risk-plane.md` (341 `wc -l` newlines, no final
newline — 342 lines as read; md5
`1a584300f6b07da78bc8332f04b4fd30`, mtime 14:44 -03) + the receipt block of
`corpus/knowledge/foreign-provenance-r6.md` (§5).
Picked packages: **`android-apktool-bin`** (channel B, AUR-local) and **`omarchy-walker`**
(channel A, offline-exile) — one per class, chosen by the verifier, not by the author.
Scratch: `/tmp/w6-tsukuroi-vers6/` (probe transcripts `probe-*.txt`, `verify-*.txt`).
**Verdict: CONFIRMED, 2/2 rows; 0 claims refuted; 2 documentation deltas, 1 live-drift
note.** No file was edited; no transaction, no `-Sy`, no service action, no network.
Claim tags as in the register: [observed] / [inference] / [unknown].

## 1. Row 1 — `android-apktool-bin 3.0.3-1` (register §1 line 64, §3, R1/R2/R5/R9)

| register claim | the verifier's own probe | verifier's result | verdict |
|---|---|---|---|
| channel "B AUR-local" | `grep -n "android-apktool-bin" /var/log/pacman.log` | `:2090` = `[PACMAN] Running 'pacman -U --needed --noconfirm --config /etc/pacman.conf -- /home/vgpnk/.cache/yay/android-apktool-bin/android-apktool-bin-3.0.3-1-any.pkg.tar.zst'`, `:2096` = the `-D --asexplicit` line, both `2026-10-13T13:52:59-0300` | CONFIRMED |
| installed 2026-10-13 13:52:59 | `pacman -Qi` Install Date + `%INSTALLDATE%` epoch in `/var/lib/pacman/local/android-apktool-bin-3.0.3-1/desc` | `Tue 13 Oct 2026 01:52:59 PM -03`; epoch → `2026-10-13T16:52:59Z` | CONFIRMED |
| upgraded/downgraded/reinstalled since: never | `grep -cE "\] (upgraded\|downgraded\|reinstalled\|removed) android-apktool-bin " /var/log/pacman.log` | `0` | CONFIRMED |
| req-by 0 | `pacman -Qi` Required By | `None` | CONFIRMED |
| validation `none` | `%VALIDATION%` block in local `desc`; `pacman -Qi` | block = `none`; `Validated By: None` | CONFIRMED |
| payload 2 files, jar 14.76 MiB | `pacman -Ql android-apktool-bin`; `stat` | listing = 5 dirs + `/usr/bin/apktool`, `/usr/share/java/android-apktool/apktool.jar`; jar `15478013 B` = 14.76 MiB | CONFIRMED |
| R1 no update path | `pacman -Si android-apktool-bin` rc | rc=1, `error: package 'android-apktool-bin' was not found`; name absent from the 15651-name sync union | CONFIRMED |
| R2 unreviewable artifact | no `.sig` beside either yay artifact; `LocalFileSigLevel` | `ls *.sig` → ENOENT both caches; `packageOptional/PackageTrustedOnly` | CONFIRMED |
| R5 runtime code | payload above (1 wrapper script + 1 jar) | fires | CONFIRMED |
| R9 stale artifact 1 d | Build Date `Tue 13 Oct 2026` vs 2026-10-14 | 1 d | CONFIRMED |
| §3 clone HEAD `92ce7df1…`, `2026-09-28T17:22:27+03:00`, `update to v3.0.3` | `git -C ~/.cache/yay/android-apktool-bin log -1 --format='%H %cI %s'` | `92ce7df1217deb19fab6e899a3772459f4198bdc 2026-09-28T17:22:27+03:00 update to v3.0.3` | CONFIRMED |
| §3 clone clean, `.SRCINFO` 3.0.3-1 = installed | `git status --porcelain`; `grep pkgver .SRCINFO` | porcelain = 0 lines; `pkgver = 3.0.3`, `pkgrel = 1` | CONFIRMED |
| §3 remote `aur.archlinux.org/android-apktool-bin.git` | `git remote -v` | same URL | CONFIRMED |
| §3 sha256 pins `dbf930b0…f9423`, `48a5c9d6…b63bae` | `grep sha256sums PKGBUILD` | `dbf930b076c6b9be08d57c449cacefc3bdd6b71ebd59b3066fc0e1f5b14f9423`, `48a5c9d664c88c8beac4a85461e84437d104a42dac6334322a3bafca12b63bae` | CONFIRMED |
| §3 two `# Maintainer:` lines | `grep -i maintainer PKGBUILD` | lines 1–2 name two humans | CONFIRMED |
| §3 "the package ships the downloaded jar" | `sha256sum /usr/share/java/android-apktool/apktool.jar` | `dbf930b0…f9423` — **equal to `sha256sums[0]`**, i.e. the installed bytes match the pinned upstream payload | CONFIRMED |
| receipt artifact `e83409b290bae6be` | `sha256sum ~/.cache/yay/android-apktool-bin/android-apktool-bin-3.0.3-1-any.pkg.tar.zst` | prefix `e83409b290bae6be` | CONFIRMED |

## 2. Row 2 — `omarchy-walker 1.0.0-2` (register §1 line 79, §2, R1/R4/R5/R8/R9/R10/R12)

| register claim | the verifier's own probe | verifier's result | verdict |
|---|---|---|---|
| channel "A offline-exile" | `tar -tzf /var/lib/pacman/sync/offline.db \| grep omarchy-walker`; `pacman -Sl offline` | `omarchy-walker-1.0.0-2/desc` present; `pacman -Sl offline` rc=1 `repository "offline" was not found`; `/etc/pacman.conf` sections `[options]:3 [core]:19 [extra]:22 [multilib]:25 [omarchy]:28` | CONFIRMED |
| installed 2026-10-03 17:44:26 | log `:1110`; `%INSTALLDATE%` | `[2026-10-03T17:44:26-0300] [ALPM] installed omarchy-walker (1.0.0-2)`; epoch → `2026-10-03T20:44:26Z` (receipt line 1110 = my line 1110) | CONFIRMED |
| no `pacman -U` anywhere for channel A | `grep -cE "Running 'pacman -U.*(elephant\|omarchy-walker)"` | `0`; the install is the tail of the `-S` at log `:484` (`[2026-10-03T17:42:38-0300] [PACMAN] Running 'pacman -S --noconfirm --needed 1password-beta …'`) | CONFIRMED |
| upgraded since: never | same grep battery as Row 1 | `0` | CONFIRMED |
| req-by 0, meta package, 0 files, 0.00 B | `pacman -Qi`; `pacman -Ql` | Required By `None`; `-Ql` no output; Installed Size `0.00 B` | CONFIRMED |
| validation `sha256 pgp` | `%VALIDATION%` block | `sha256 pgp` | CONFIRMED |
| trust surface: `Good signature from "Omarchy <pkgs@omarchy.org>"`, keyid `F0134EE680CAC571`, sig 2025-11-21 | `gpg --homedir /etc/pacman.d/gnupg --verify /var/cache/pacman/pkg/omarchy-walker-1.0.0-2-x86_64.pkg.tar.zst.sig …` | `Signature made Fri 21 Nov 2025 12:54:47 PM -03`, `using EDDSA key 40DFB630FF42BCFFB047046CF0134EE680CAC571`, Good [full] (same for `elephant-2.21.0-1` at 2026-04-15 11:58:28) | CONFIRMED |
| R4 dead channel | `zstd -dc omarchy.db \| tar -t \| grep -c '/desc$'` + greps | 231 entries; `grep -i elephant` → 0; `omarchy-walker` → 0; `walker-2.17.0-1` present | CONFIRMED |
| R5/R8 no code, blast radius 0 | payload above; Required By | fires exactly as stated | CONFIRMED |
| R9 327 d (Build Date 2025-11-21) | `pacman -Qi` Build Date; date arithmetic | `Fri 21 Nov 2025 12:54:18 PM -03` → 327 d to 2026-10-14 | CONFIRMED |
| R10 crossing: `walker 2.16.2-1 → 2.17.0-1` @ 2026-10-11 16:14:39; snapshot carries 2.16.2-1 | log grep; `tar -tzf offline.db \| grep '^walker-'` | `:1943 [2026-10-11T16:14:39-0300] [ALPM] upgraded walker (2.16.2-1 -> 2.17.0-1)`; `walker-2.16.2-1/desc` present | CONFIRMED |
| R12 wiring unowned | `pacman -Qo` on unit + autostart; `stat` | both `error: No package owns …`; `~/.config/autostart/walker.desktop` `138 B, 2026-10-03 17:44:36.747 -03` | CONFIRMED |
| §2 offline.db 304318 B, birth 2026-10-03 17:41:33, 1275 entries | `stat -c '%w'`; `tar -tzf … \| grep -c '/desc$'` | size 304318; birth `2026-10-03 17:41:33.994891750 -0300`; mtime `2026-07-20 21:11:36`; 1275 entries | CONFIRMED |
| §2 the 14 are in the cache | `ls /var/cache/pacman/pkg \| grep -cE '^(elephant\|omarchy-walker).*pkg.tar.zst$'` | 14 archives + 14 `.sig` (13 elephant + omarchy-walker); mtimes `2026-04-16 20:01:19–25` and `2025-11-21 12:55:36` match the receipt's claim | CONFIRMED |
| receipt `451b74fc6deba2bf`; offline.db declared SHA256/CSIZE match the archive | `sha256sum`; `tar -xzOf offline.db omarchy-walker-1.0.0-2/desc` | archive prefix `451b74fc6deba2bf`; declared `451b74fc6deba2bf…2edadd` = on-disk hash, `%CSIZE%` 7033 = on-disk size (same for `elephant`: `25e1f983046f3491…` / 8450500) | CONFIRMED |

## 3. Cross-cutting claims re-measured (not taken on trust)

- `pacman -Qm` = **16**, `-Qme` = **3**, `pacman -Q` = **1188**, `pacman -Qe` = **207** [observed].
- 15651-name sync union; the 16 are absent from it; `pacman -Qu` empty rc=1; `pacman -T <all 16>` rc=0 [observed].
- 16 install-log lines, one per foreign package, same seconds as `Install Date`; upgrade/
  downgrade/reinstall/removed counts `0` for all 16; no `install` scriptlet file and 16/16
  `Install Script  : No` [observed].
- R3's "36 = the foreign 16 + these 20" — block-wise extraction of `Packager: Unknown Packager`
  gave exactly the register's 20 names (foreign 16 removed): `1password-beta asdcontrol cliamp
  hyprland-preview-share-picker limine-mkinitcpio-hook limine-snapper-sync localsend
  omarchy-keyring omarchy-nvim python-terminaltexteffects spotify tobi-try ttf-ia-writer
  typora tzupdate ufw-docker walker xdg-terminal-exec yaru-icon-theme yay` [observed].
- Live exposure: `elephant.service` active/running since `2026-10-14 13:11:08 -03`, MainPID
  `1203474`, `Restart=on-failure`, `RestartUSec=100ms`, `WantedBy=graphical-session.target`;
  `app-walker@autostart.service` active/running; journal this boot `grep -ic elephant` = **132**,
  error-class = **0**; the Oct 11 failure block matches verbatim (`Main process exited,
  code=exited, status=1/FAILURE` / `Failed with result 'exit-code'` / `restart counter is at 1`);
  the `bluetoothctl not found. disabling` line **is** present at the 13:11:08 startup (PID
  1203474) — attribution to that startup confirmed [observed].
- Receipt anchors: `/var/log/pacman.log` md5 `e452d910de724ac016c2d019f9e1ec45`, 2109 lines —
  byte-exact match, so the receipt's line numbers are reproducible [observed].

## 4. Deltas the verifier found (kept, not smoothed)

- **D1 (documentation, not a row):** the round-6 plan names the register
  `corpus/knowledge/foreign-aur-risk-plane.md`; the artifact landed as
  `corpus/knowledge/aur-risk-plane.md`. The register self-documents the rename (`:23-24`,
  "assignment wins"); the plan/record text still says the old name. Fix belongs to the author
  or the round record — the verifier does not edit either.
- **D2 (wording):** §4's operator-action cell says "the 15 archives", §7.5 says "the 15
  channel-A archives", while §4's own first sentence says "the 14 archives". Measured:
  **14** archives + 14 sigs under `^(elephant|omarchy-walker)`, plus 2 `walker` archives
  (`2.16.2-1`, `2.17.0-1`). "15" is only reconcilable by counting `walker-2.16.2-1`, which is
  not channel A (the live omarchy db supplies `walker`). The executable claim (preserve the
  channel-A set + `offline.db`) is unaffected.
- **D3 (live drift, expected):** register §5 quotes `45.5 M memory (peak 370.8 M)`. My later
  read: `MemoryCurrent=56696832` (54.1 MiB), `MemoryPeak=388915200` (370.9 MiB), `TasksCurrent=29`.
  Memory is a moving value; the monotonic peak only grew between the two reads. Not a
  disagreement — recorded so nobody re-dates the row from a second number.

## 5. Spot-checks (the three the seat was asked for, verbatim results)

1. `sha256sum /usr/share/java/android-apktool/apktool.jar` →
   `dbf930b076c6b9be08d57c449cacefc3bdd6b71ebd59b3066fc0e1f5b14f9423` = PKGBUILD `sha256sums[0]`
   → the "installed bytes = pinned upstream payload" chain holds across build→install.
2. `gpg --homedir /etc/pacman.d/gnupg --verify omarchy-walker-1.0.0-2-x86_64.pkg.tar.zst.sig …`
   → Good, `F0134EE680CAC571`, sig 2025-11-21 12:54:47 -03 → channel-A trust row is real, and
   the archive's cache mtime is 12:55:36 -03 the same day (49 s later) — plausible same-event.
3. `pacman -Qdtq` → `electron39`, `mbedtls`, `webp-pixbuf-loader`, rc=0, and `pacman -Qmdtq`
   → empty rc=1 → "no foreign package is an orphan, but the host does have 3 non-foreign
   orphans" is exactly right.

## 6. Not re-verified by this seat (stated so the verdict is not overread)

- The 13 individual elephant rows were checked at class level (sum of Installed Size =
  **339.09 MiB**, matching §1 exactly; `elephant` itself checked cell-by-cell) — not
  one-by-one for every payload/req-by cell.
- `obsidian-cli-inspector`: verified install timestamp, `%VALIDATION% = none`, clone HEAD
  `ce7b4258…`, `.SRCINFO` 1.0.3-1, artifact prefix `a6ec77fab6e3d3a7` — but not its row cell
  set in full.
- §5's journal readings other than the ones listed; §7's unknowns (linkage/ABI, AUR-side
  liveness, online-omarchy history) are [unknown] and stay out of reach — no `readelf`/`ldd`,
  no network, by discipline.
- The register's errata E-1/E-2 describe its own collection accidents; not re-run.

## 7. Mutation statement

Every command above is a read: `pacman -Q*`, `pacman -Si/Sl/T`, `pacman-conf`, `grep/stat/tar`
on `/var/lib/pacman` and `/var/log`, `gpg --verify`, `systemctl --user show/status`,
`journalctl --user`, `git -C … log/status/remote`, `sha256sum`, `ls`. No transaction, no
`-Sy`, no unit action, no root, no network. The only two writes by this seat are the scratch
transcripts under `/tmp/w6-tsukuroi-vers6/` and this report file. Verdict: the two recomputed
rows are **confirmed as written**; the register's risk decision table is not merely
self-consistent, it reproduces from independent probes on the same host.

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — independent `pacman -Q*`/`-Si`/`-Sl`/`-T`, package-file and sync-db reads, and `/var/log/pacman.log` probes on host `plazir27`, 2026-10-14; S032 `/var/log/pacman.log`.
verified-at: 2026-10-14 (the verifier's independent probe window recorded in this note).
recheck: 180d; procedure: §§1–5 rerun the two package spot-checks and cross-cutting probes; retain the explicit not-reverified boundary.
