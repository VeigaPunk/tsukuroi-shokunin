# foreign/AUR provenance & freshness receipt — 16 packages (TSUKUROI-R6-S6-2)

source: live read-only probes, host `plazir27`, user `vgpnk` (non-root), window
2026-10-14 17:38:21Z – 17:41Z. Probes: `pacman -Qm[q]`/`-Qi`/`-Si`/`-Sl`,
reads of `/var/log/pacman.log` (md5 `e452d910…`, digest taken twice),
`bsdtar` reads of the sync dbs, `stat`, `sha256sum`, `gpg --verify` in a
scratch GNUPGHOME imported from the host keyring, `git` reads of the yay
build clones. No network probe (no external sites); nothing installed,
upgraded, removed or restarted; no host file written — the only writes in
the run are inside `/tmp/w6-tsukuroi-s62/` (scratch TSVs, scratch GnuPG home).
Companion planes: `package-state-plane.md:42-89` (census + sync-db mtime trap,
its channel row is *closed* here — see §8 E1), the sibling risk plane
`foreign-aur-risk-plane.md` (S6-1, owns risk classes; this note does not
duplicate them). The round-6 plan's freshness axis (S6-2) is this file.

verified-at: 2026-10-14 17:38:21Z – 17:41Z (live snapshot; values will move)
recheck: §7. Notation: **[obs]** measured · **[inf]** inference · **[unk]** unknown.
All counts carry their command; every foreign number below is *re-measured in
this run* — nothing is quoted from earlier census notes or reports.

## 1. As-of census and the log as the history record

- **[obs]** `pacman -Qmq | wc -l` → **16** at 17:38:21Z; re-run 17:40:47Z →
  16 (`pacman -Qq | wc -l` → 1188 installed, context only).
- **[obs]** Install reason per package (`pacman -Qi`, field *Install Reason*):
  **3 explicit** — `omarchy-walker`, `android-apktool-bin`,
  `obsidian-cli-inspector` — and **13 dependencies** (all elephant family,
  pulled in by `omarchy-walker` in the same transaction). Full column §5.
- **[obs]** `/var/log/pacman.log` is the host's *entire* pacman history:
  first line `[2026-10-03T20:41:33+0000] [PACMAN] Running 'pacman
  -b /mnt//var/lib/pacman/ -r /mnt -Sy … base sudo linux-firmware …'` (the
  installer bootstrap, written into the target root), last line
  `[2026-10-13T16:37:59-0300] [ALPM] running '35-systemd-update.hook'…`.
  Single file, no rotation (`ls /var/log/pacman.log*` → 1 file, no `.gz`):
  **md5 `e452d910de724ac016c2d019f9e1ec45`, 2109 lines, 157286 B**, mtime
  2026-10-13 16:37:59 -0300. Digest unchanged between the two reads in the
  window → the history below is complete from install day to now.
- **[obs]** Complete event set for all 16 foreign packages across that whole
  history — probe: `grep -nE '\[ALPM\] (installed|upgraded|downgraded|reinstalled|removed) (<the 16 names>) ' /var/log/pacman.log`:

  | event class | count | where |
  |---|---|---|
  | `installed` | 16 (each package exactly once) | log 1096–1110 (14 pkgs, 2026-10-03T17:44:26-0300), 2093, 2100 |
  | `upgraded` / `downgraded` / `reinstalled` / `removed` | **0** | — |
  | `pacman -D --asexplicit` marks | 2 | log 2096, 2103 |

  ⇒ No foreign package has ever been updated, downgraded or removed since its
  single install event. "Foreign version drift" does not exist on this host;
  the only variable is *channel* freshness (§4).

## 2. Channel A — the 14 install-day packages: the `offline.db` chain

### 2.1 The surviving channel artifact

- **[obs]** `/var/lib/pacman/sync/offline.db` — 304318 B, root:root 644,
  **birth 2026-10-03 17:41:33.994 -0300** (2 m 53 s *before* the install
  transaction that landed the set), mtime 2026-07-20 21:11:36 (upstream
  stamp — same trap family as the other sync dbs), **1275 package dirs**
  (`bsdtar -tf … | grep -c '/$'`).
- **[obs]** It is **not configured**: `grep -n offline /etc/pacman.conf` →
  rc=1 (`[options]`/`[core]`/`[extra]`/`[multilib]`/`[omarchy]` at lines
  3/19/22/25/28); `pacman -Sl offline` → `error: repository "offline" was not
  found`. Leftover sync db, not queried by the current config.

### 2.2 What the log shows (install-time transaction)

- **[obs]** `[PACMAN] Running 'pacman -S --noconfirm --needed 1password-beta
  … omarchy-walker …'` at 2026-10-03T17:42:38-0300 (log 484; `omarchy-walker`
  named explicitly, the elephant family not). Transaction started 17:44:16
  (log 485), `walker 2.16.2-1` installed 17:44:26 (log 1095), the 13 elephant
  packages 17:44:26 (log 1096–1109), `omarchy-walker 1.0.0-2` 17:44:26
  (log 1110), transaction completed 17:44:28 (log 1220).
- **[obs]** `walker` (a *sync* package today, in `[omarchy]`) was installed in
  that same transaction at 2.16.2-1 — the version `offline.db` carries
  (`walker-2.16.2-1/` present) — and only later moved to 2.17.0-1 (§4).

### 2.3 Per-package chain, 14/14 — db → artifact → signature → keyring

Probe per package (`$p`, `$v` = installed name-version):

1. `bsdtar -xOf /var/lib/pacman/sync/offline.db "$p-$v/desc"` — entry exists
   for all 14 (`elephant-2.21.0-1/` … `omarchy-walker-1.0.0-2/`); declared
   `%CSIZE%` == byte size of the retained artifact and declared `%SHA256SUM%`
   == `sha256sum` of that artifact. **14/14 both checks** (prefixes in §5;
   full hashes reproduce with the §7 commands).
2. `gpg --verify <pkg>.pkg.tar.zst.sig <pkg>.pkg.tar.zst` in a scratch
   GNUPGHOME with the signer key exported from `/etc/pacman.d/gnupg` →
   **14/14 `GOODSIG`**, issuer `F0134EE680CAC571`, fingerprint
   `40DFB630FF42BCFFB047046CF0134EE680CAC571` = **`Omarchy <pkgs@omarchy.org>`**
   (uid tagged `[full]` in the host keyring: self-signature 2025-08-28 +
   signature by `Pacman Keyring Master Key <pacman@localhost>` 2026-10-03).
   Representative full verify: `Signature made Wed 15 Apr 2026 11:58:28 AM
   -03 … Good signature from "Omarchy <pkgs@omarchy.org>"`.
3. Artifact retention: all 14 `.pkg.tar.zst` + `.sig` are still in
   `/var/cache/pacman/pkg/` (the exact files installed; `pacman -Qi`
   `Validated By: SHA-256 Sum Signature`, `Packager: Unknown Packager` —
   same string inside `.PKGINFO`). Cache mtimes: elephant family
   `2026-04-16 20:01:19–25 -0300`, `omarchy-walker 2025-11-21 12:55:36 -0300`
   → **the offline repo's assembly times, not install times** (see §6 d).
4. Independent date anchor: `/var/lib/pacman/local/<pkg>-<ver>/` mtimes are
   `2026-10-03 17:44:26.<188–426>` for all 14, matching the log and
   `pacman -Qi Install Date` to the second.

### 2.4 Channel identification

- **[inf]** High confidence: the 14 were resolved from `offline.db` at
  install. (i) It is the only sync db that ever contained the set: core/
  extra/multilib are older, and `omarchy.db` was **born 2026-10-11
  12:54:13.542**, i.e. *eight days after* the install; `pacman -Si <pkg>`
  rc=1 for all 16 today. (ii) The installed artifacts' SHA-256 equal the
  hashes `offline.db` itself declares (2.3.1). (iii) The db's birth precedes
  the install by 2 m 53 s and it carries the exact name-versions incl. the
  `walker` dependency.
- **[unk]** The install-time pacman config is gone (`/tmp/pacman.conf.Cab7`
  etc. from the bootstrap line → `ls /tmp/pacman.conf.*` → absent), so the
  repo stanza name/`SigLevel` actually used for resolution cannot be re-read;
  the identification rests on the surviving db and the signature. Whether the
  offline channel was itself refreshed at any point is [unk] (§8 U4).

## 3. Channel B — the yay-local pair: AUR build chain

Both packages: no `.sig` beside the artifact (`Validated By: None`,
`Packager: Unknown Packager` in `pacman -Qi` and `.PKGINFO`); the build
artifacts and their sources are retained inside `~/.cache/yay/<pkg>/`.

**android-apktool-bin 3.0.3-1** (explicit)

- **[obs]** log 2090: `pacman -U --needed --noconfirm --config /etc/pacman.conf
  -- /home/vgpnk/.cache/yay/android-apktool-bin/android-apktool-bin-3.0.3-1-any.pkg.tar.zst`
  at 2026-10-13T13:52:59-0300; install line 2093 same second; `-D --asexplicit`
  line 2096. Artifact `.PKGINFO builddate` 2026-10-13T13:52:58-0300 (build
  1 s before install).
- **[obs]** Artifact sha256 `e83409b290bae6be118841b17a7168bbc183ec85586e9f6e71a4af1ba84edbd2`.
- **[obs]** AUR clone: `origin https://aur.archlinux.org/android-apktool-bin.git`;
  HEAD `92ce7df1217deb19fab6e899a3772459f4198bdc`, committed
  `2026-09-28T17:22:27+03:00` ("update to v3.0.3"); `git status --porcelain`
  empty; tracked files `.SRCINFO .gitignore LICENSE PKGBUILD apktool` (the
  downloaded jar is gitignored). The on-disk PKGBUILD read is therefore the
  AUR-tracked HEAD content.
- **[obs]** Source cross-check against that PKGBUILD: `apktool_3.0.3.jar`
  sha256 `dbf930b076c6b9be08d57c449cacefc3bdd6b71ebd59b3066fc0e1f5b14f9423`
  == `sha256sums[0]`; tracked `apktool` script sha256
  `48a5c9d664c88c8beac4a85461e84437d104a42dac6334322a3bafca12b63bae`
  == `sha256sums[1]`. Both `match`.

**obsidian-cli-inspector 1.0.3-1** (explicit)

- **[obs]** log 2097: `pacman -U --noconfirm --config /etc/pacman.conf --
  /home/vgpnk/.cache/yay/obsidian-cli-inspector/obsidian-cli-inspector-1.0.3-1-x86_64.pkg.tar.zst`
  at 2026-10-13T16:21:20-0300; install line 2100; `-D --asexplicit` line
  2103. `.PKGINFO builddate` 2026-10-13T16:20:56-0300 (build 24 s before
  install).
- **[obs]** Artifact sha256 `a6ec77fab6e3d3a7a5b50a959422f6dab9b42356c426e053ab8649891a431959`.
- **[obs]** AUR clone: `origin https://aur.archlinux.org/obsidian-cli-inspector.git`;
  HEAD `ce7b42588bd4f64af509e8b4a336a149ca93f3ca`, committed
  `2026-03-08T07:56:23Z` ("Update to obsidian-cli-inspector-v1.0.3");
  tracked files `.SRCINFO PKGBUILD`; `git status --porcelain` →
  `?? obsidian-cli-inspector-1.0.3-1-x86_64.pkg.tar.zst`,
  `?? obsidian-cli-inspector-1.0.3.tar.gz` (build output + fetched source
  inside the clone).
- **[obs]** Source cross-check: `obsidian-cli-inspector-1.0.3.tar.gz` sha256
  `561a53019bdc3c0d5e964c87e85832c1b273b7e2d30a2907bda18a94b61dfa4f`
  == the PKGBUILD's single `sha256sums` entry. `match`.

- **[obs]** Update path measured: `yay` is the only AUR tool present
  (`13.0.1-1`, `Install Date 2026-10-11 16:14:39-0300`, log 1948 upgraded
  `12.6.0-1 -> 13.0.1-1`; 12.6.0-1 itself came from `offline.db` at install —
  `yay-12.6.0-1/` present there). `yay` is served by `[omarchy]`
  (`pacman -Sl omarchy` row, `Validated By: SHA-256 Sum Signature`) ⇒ the
  helper's own freshness is maintained by the omarchy channel, and *these
  two packages'* freshness is whatever the operator's next `yay -Syu` does.
- **[unk]** Whether the PKGBUILD was inspected before building — no record on
  host; whether AUR upstream has moved since the clone — needs network
  (out of reach here, no external probes). §8 U2/U3.

## 4. Freshness asymmetry — what moved, what did not

Ages at 2026-10-14T17:41Z, from install timestamps (§5):

- the 14 install-day packages: **10 d 20 h** since install; newest event any
  of them has is that install — none has ever been upgraded.
- `android-apktool-bin`: **1 d 0 h 48 m**; `obsidian-cli-inspector`: **22 h 20 m**.

Split freshness inside the frozen set [obs]: the dependency `walker` moved
`2.16.2-1 -> 2.17.0-1` (log 1943, 2026-10-11T16:14:39-0300, from `[omarchy]`
— `omarchy.db` born 12:54:13 that day), while all 13 elephant providers and
`omarchy-walker` stayed at the install-day versions. So `walker` is newer than
the provider set it loads — the compatibility question is the sibling plane's
(and linkage/oracle evidence is out of province — §8 U6), but the *freshness*
fact stands: one half of the pair followed the omarchy channel, the other
half was left on the offline snapshot.

Channel-reachability today [obs]: `pacman -Si <pkg>` rc=1 for **all 16** →
an `-Syu` cannot move any of them. The 14 have **no update path at all**
(source db orphaned, not configured); the 2 only via `yay` (AUR).

Two different freshness clocks [obs], both in §5:
*installation age* (§5 col `install_utc`) vs *artifact age* (build dates):
elephant family built 2026-04-15T14:45:28Z → installed 171 d later; the whole
offline repo's elephant artifacts are now **182 d** old. `omarchy-walker`
built 2025-11-21T15:54:18Z → installed 316 d later; now **327 d** old.
The AUR pair shows the opposite shape: built 1 s / 24 s before install.

Host-wide activity for context [obs]: last `-Syu` command
2026-10-11T16:13:19-0300 (log 1414); last pacman write
2026-10-13T16:37:59-0300 (`git-filter-repo`, log 2104 ff.) → **no pacman
activity on 2026-10-14** before this probe.

## 5. Receipt (machine-readable)

```
# foreign provenance + freshness receipt — plazir27 — measured 2026-10-14T17:38–17:41Z
# source log: /var/log/pacman.log md5=e452d910de724ac016c2d019f9e1ec45 lines=2109
# offline.db: /var/lib/pacman/sync/offline.db birth=2026-10-03T17:41:33.994-0300 csize+sha256 match 14/14
# signer (14/14): GOODSIG F0134EE680CAC571 "Omarchy <pkgs@omarchy.org>" fpr=40DFB630FF42BCFFB047046CF0134EE680CAC571
# fields: pkg | version | install_utc | reason | channel | log_line | artifact_sha256[:16] | sig
android-apktool-bin                | 3.0.3-1  | 2026-10-13T16:52:59Z | explicit | yay-local   | 2093 | e83409b290bae6be | no-sig
elephant                           | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1096 | 25e1f983046f3491 | GOODSIG
elephant-bluetooth                 | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1097 | edd752f900cc96a6 | GOODSIG
elephant-calc                      | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1098 | 59d016845c6ccb4b | GOODSIG
elephant-clipboard                 | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1100 | 6e77d819bfa5dd14 | GOODSIG
elephant-desktopapplications       | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1101 | b899c6ed352341f3 | GOODSIG
elephant-files                     | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1102 | 47a315a156c1d93c | GOODSIG
elephant-menus                     | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1103 | 80310cccf329947b | GOODSIG
elephant-providerlist              | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1104 | fd0f6071478d9aa8 | GOODSIG
elephant-runner                    | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1105 | ab7227b7d29e1883 | GOODSIG
elephant-symbols                   | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1106 | 4156ed22775f853c | GOODSIG
elephant-todo                      | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1107 | 824f5eb6ba567a87 | GOODSIG
elephant-unicode                   | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1108 | 643502ad8317b747 | GOODSIG
elephant-websearch                 | 2.21.0-1 | 2026-10-03T20:44:26Z | dep      | offline.db  | 1109 | 7ec991202f42bd4b | GOODSIG
obsidian-cli-inspector             | 1.0.3-1  | 2026-10-13T19:21:20Z | explicit | yay-local   | 2100 | a6ec77fab6e3d3a7 | no-sig
omarchy-walker                     | 1.0.0-2  | 2026-10-03T20:44:26Z | explicit | offline.db  | 1110 | 451b74fc6deba2bf | GOODSIG
# artifact paths: /var/cache/pacman/pkg/<pkg>-<ver>-x86_64.pkg.tar.zst (14 offline)
#                 ~/.cache/yay/<pkg>/<pkg>-<ver>-(any|x86_64).pkg.tar.zst (2 yay-local)
# full sha256: sha256sum <artifact>; offline declarations: bsdtar -xOf …/offline.db <pkg>-<ver>/desc
```

Provenance of this receipt: every column is a direct read in the window
(`pacman -Qi Install Date` agrees with the log line to the second for all 16);
nothing in it is inherited from a census note. Consumable by the S6-1
baseline plane as the accepted-baseline provenance layer.

## 6. Method notes (kept for the next measurer)

a. **`$p-*` glob trap**: `pacman -Qmq` prints bare `elephant`; `ls -d
   /var/lib/pacman/local/$p-*` then expands to *all* elephant-* dirs and the
   loop mis-reads. Build exact names as `$p-$(pacman -Q $p | cut -d' ' -f2)`.
   The first pass of §2.3 hit this; no number in this note comes from it.
b. **`gpg --verify` output order**: the human-readable stream buries the
   result under trust notes; use `--status-fd` and read the
   `[GNUPG:] GOODSIG`/`BADSIG` row (rc alone is enough for the loop).
c. **Verify in a scratch GNUPGHOME** (`/tmp`, imported from
   `/etc/pacman.d/gnupg`'s public ring) — the host keyring is not writable
   non-root anyway (`gpg: Note: trustdb not writable`), and the scratch home
   makes the probe provably mutation-free.
d. **Cache mtimes are repo-build stamps**, not install times: the elephant
   artifacts carry 2026-04-16 mtimes while their install is 2026-10-03.
   Same trap class as the sync-db mtime trap (`package-state-plane.md:73-83`);
   use `pacman -Qi Install Date` / log lines / local-db dir mtime instead.
e. **Counts drift live**: census (16) re-checked twice 2 min apart; the log
   was hashed before and after the probe window — pin digests when a receipt
   claims completeness.

## 7. Recheck (compact command set)

```sh
pacman -Qmq | wc -l ; pacman -Qm                     # set + versions
md5sum /var/log/pacman.log                           # history pin
grep -nE '\[ALPM\] (installed|upgraded|downgraded|reinstalled|removed) (elephant|elephant-[a-z-]+|omarchy-walker|android-apktool-bin|obsidian-cli-inspector) ' /var/log/pacman.log
stat --format='%n birth=%w size=%s' /var/lib/pacman/sync/offline.db
bsdtar -xOf /var/lib/pacman/sync/offline.db elephant-2.21.0-1/desc | grep -A1 -E '%(CSIZE|SHA256SUM)%'
sha256sum /var/cache/pacman/pkg/elephant-2.21.0-1-x86_64.pkg.tar.zst
GNUPGHOME=<scratch> gpg --batch --verify /var/cache/pacman/pkg/elephant-2.21.0-1-x86_64.pkg.tar.zst.sig /var/cache/pacman/pkg/elephant-2.21.0-1-x86_64.pkg.tar.zst
git -C ~/.cache/yay/<pkg> log -1 --format='%H %cI' ; git -C ~/.cache/yay/<pkg> status --porcelain
sha256sum ~/.cache/yay/apktool… ; # compare with PKGBUILD sha256sums
```

## 8. Unknowns / out of reach (owners)

- **U1** install-time `pacman.conf` (`/tmp/pacman.conf.*`) gone → the exact
  repo name/`SigLevel` used during the 10-03 resolution is unrecoverable;
  channel identification is [inf] from the surviving db + signature (§2.4).
- **U2** whether the operator reviewed the two AUR PKGBUILDs before building —
  not recorded anywhere on the host (owner: operator).
- **U3** AUR upstream state on 2026-10-14 (have versions moved since the
  cloned HEADs?) — requires network; this lane made no external probes.
- **U4** whether `offline.db` was ever refreshed elsewhere (it is orphaned in
  the sync dir; a future installer could overwrite or remove it) — no writer
  evidence on host beyond the birth date.
- **U5** which host/process built and signed the offline repo (signature dates
  only: 2026-04-15 11:58:28 -03 for the elephant set, 2025-11-21 for
  `omarchy-walker`) — not on this host.
- **U6** whether elephant 2.21.0-1 is functionally compatible with walker
  2.17.0-1 (mixed freshness, §4) — needs linkage/runtime evidence; out of
  province for state probes (PROVINCE.md:14-18) → report to kaidoku/revenger
  if the sibling plane escalates it. *Recorded, not absorbed.*

## 9. Errata (append-only)

- **E1** (2026-10-14, S6-2): `package-state-plane.md:69` records the
  install-day channel of the 14 as `[unknown]`. This note closes it to
  **[inf] `offline.db`** with the §2 evidence chain; that file was not edited
  here (this lane writes only its own note — cross-note item for the owner
  lane/scribe to consume or amend).
- **E2** (2026-10-14, S6-2): measurement incident recorded, not laundered —
  the §6(a) `$p-*` glob mis-expansion happened during the first size-chain
  pass; the pass was discarded and re-run with exact dir names. No value in
  this note originates from the failed pass.

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — pacman foreign-package queries, `/var/log/pacman.log`, sync-db archive/stat and signature reads on host `plazir27`, 2026-10-14; S032 `/var/log/pacman.log`.
verified-at: 2026-10-14 (the original live provenance window recorded in this note).
recheck: 90d; procedure: §7 re-run the `pacman -Qm`/`-Si`/`-Qmdtq`, sync-db and package-provenance probes.
supersedes the pointer-only recheck: line above.


## R17-RECHECK — steer-safe procedure

Appended 2026-10-20 by the tsukuroi round-17 L1; earlier bytes unchanged. Supersedes the package-manager invocations in this file's `recheck:` line for any round whose steer forbids running pacman (QUALITY 26); file reads replace them and the substitution is recorded in that round's report. Read-only.

- foreign set without a package query: compare `ls /var/lib/pacman/local` names with `tar -tzf /var/lib/pacman/sync/<repo>.db` entry names for each repo in `/etc/pacman.conf`; a local name absent from every sync listing is foreign
- sync version of one package: `tar -xOzf /var/lib/pacman/sync/<repo>.db <pkg>-<ver>/desc` and read `%VERSION%`
- sync-db age: `stat -c "%y %n" /var/lib/pacman/sync/*.db`
- unneeded-dependency (`-Qdt`) status has no read-only file equivalent short of a dependency walk over `/var/lib/pacman/local/*/desc`; record it as [unk] under such a steer


## R18-FRESHNESS — foreign provenance: history completeness (lines 29-37)

Appended 2026-10-20 by tsukuroi round-18 (seat Foreign). Historical snapshots preserved above; this notice supersedes the current-use statement at lines 29-37 only. Read-only scope: it clears no package, reboot or boot state. Sources: S060 (fresh R18 capture), S032 (pacman log).

- now: /var/log/pacman.log has 3169 lines at 2026-10-20 (wc -l); the 2109-line pin no longer describes the current file.
- capture_ref: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:60 [obs] `3169 /var/log/pacman.log`.
- Basis: the 2026-10-14 "entire history" claim pinned 2109 lines (md5 e452d910...). The log has since grown by 1060 lines; the R18 capture did not hash it, so no new digest is asserted.

## R18-FRESHNESS — foreign provenance: no-update claim (line 47)

Appended 2026-10-20 by tsukuroi round-18 (seat Foreign). Historical snapshots preserved above; this notice supersedes the current-use statement at line 47 only. Read-only scope: it clears no package, reboot or boot state. Sources: S060, S032.

- now: S065 records thirteen elephant-family upgraded events and ALPM completion09:31:04, plus zcode installed13:23:08 and ALPM completion13:23:09. Thus never-updated is not current for the elephant family; zcode was not in the old16-row register and its present foreign class is not inferred [Supporting capture context: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:43-69, .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:97-101]
- capture_ref: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:72 [obs] log 3092 `pacman -U --noconfirm ... elephant-2.22.1-1-x86_64.pkg.tar.zst`; also :73 [obs] log 3161 `pacman -U --needed` for zcode, and :65 [obs] zcode marked --asexplicit at 13:23:09.
- Basis: :30 [obs] local db lists `elephant-2.22.1-1` for the base package and the 2.21.0-1 directory is absent in the same listing. The per-package ALPM event class (upgraded or reinstalled) for each elephant member is [unk]: the capture did not read those log lines. zcode is not among the 16 foreign packages of 2026-10-14 (§5); its foreign classification is [unk] (pacman -Qm not run).

## R18-FRESHNESS — foreign provenance: offline.db channel (line 55)

Appended 2026-10-20 by tsukuroi round-18 (seat Foreign). Historical snapshots preserved above; this notice supersedes the current-use statement at line 55 only. Read-only scope: it clears no package, reboot or boot state. Sources: S060, S032.

- now: offline.db is absent from /var/lib/pacman/sync at 2026-10-20; the directory lists core.db, extra.db, multilib.db, omarchy.db and openai-chatgpt.db. [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:48-55]
- capture_ref: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:48 [obs] `$ ls -1 /var/lib/pacman/sync/`, listing at :49-54.
- Basis: the 2026-10-14 presence, size and birth stamp are historical. Removal time and actor are [unk]; this round did not read the log for them. The sync-db identification in §2 can no longer be re-read from this file.

## R18-FRESHNESS — foreign provenance: no -Syu update path (line 194)

Appended 2026-10-20 by tsukuroi round-18 (seat Foreign). Historical snapshots preserved above; this notice supersedes the current-use statement at line 194 only. Read-only scope: it clears no package, reboot or boot state. Sources: S060, S032.

- now: current repository reachability remains unknown for the old16-row set, including the channel-reachability paragraph at193–195. S065 confirms the historical elephant upgrade events accompanying the09:31 pacman -U invocation, not evidence of a -Syu upgrade of foreign packages; filesystem mtime does not prove a local refresh [Supporting capture context: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:40-69, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:40-55]
- capture_ref: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:45 [obs] omarchy.db mtime; :72 [obs] the pacman -U command line.
- Basis: the 2026-10-14 statement ("pacman -Si rc=1 for all 16") was a point-in-time sync-db observation. pacman -Syu upgrades only packages served by configured sync repos; a package no repo serves changes only via pacman -U, or via an AUR helper that installs built files with pacman -U. Foreign classification is not immutable: a configured repo that begins serving a name removes it from the foreign set. Whether any of the 16 is now repo-served is [unk]; pacman -Si was not run (steer). Who ran the 09:31 pacman -U is not in the capture [unk].


## R18-PRECISION — reachability and transaction scope

The R18 reachability supersession covers the whole current-use paragraph at193–195, including the14-no-path/2-yay-only partition, not only the one quoted sentence. Current repository/configuration resolution was not remeasured by these captures. S060's09:31/13:23 Running headers alone did not establish completion; S065 now independently supplies the elephant upgraded events, zcode installed event and their ALPM transaction-completed records. The later --asexplicit line remains an invocation, not evidence its reason change succeeded. No human actor or current foreign classification is inferred.
