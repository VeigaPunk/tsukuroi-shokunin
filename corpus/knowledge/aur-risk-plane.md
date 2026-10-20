# AUR-risk plane — the foreign-package register and its risk decision table (S6-1)

source: live read-only probes, host `plazir27`, user `vgpnk`, non-root, one measurement
run 2026-10-14 14:38:09–14:43:01 -0300 — `pacman -Q|-Qe|-Qm|-Qme|-Qi|-Ql|-Qo|-Qu|-Qdtq|-Qmdtq|-Si|-Sl`,
`pacman-conf [--repo=<r>] SigLevel|LocalFileSigLevel|Server`, `tar -tf` over
`/var/lib/pacman/sync/{core,extra,multilib,omarchy,offline}.db`, `/var/log/pacman.log`
(2109 lines, grepped — never quoted from memory), `%VALIDATION%`/`%REASON%`/`%PACKAGER%`
in `/var/lib/pacman/local/<pkg>/desc`, `gpg --homedir /etc/pacman.d/gnupg --verify` on
cached `.sig` files, `git -C ~/.cache/yay/<pkg> log -1 | remote -v | status --porcelain`,
`cat ~/.cache/yay/<pkg>/{PKGBUILD,.SRCINFO}`, `systemctl --user show|status|list-units`,
`journalctl --user`, `stat`, `ls`. No network, no `pacman` transaction, no service
action, no root. Scratch: `/tmp/w6-s61-work/`.
verified-at: 2026-10-14 (single run; every table cell names the probe that produced it.
Errata E-1 records the one collection that was invalidated by a pipe error and re-run.)
recheck: `pacman -Qm` (expect 16) · `pacman -Si <pkg>` per row (expect rc=1 for all 16) ·
`pacman -Qmdtq` (expect empty, rc=1) · `tar -tf /var/lib/pacman/sync/offline.db |
grep -E '^(elephant|omarchy-walker)'` · `git -C ~/.cache/yay/<pkg> log -1 --format='%H %cI %s'` ·
`gpg --homedir /etc/pacman.d/gnupg --verify /var/cache/pacman/pkg/<pkg>.pkg.tar.zst.sig
/var/cache/pacman/pkg/<pkg>.pkg.tar.zst` · per-row operator probes in §6.

Claim tags: **[observed]** = read off a probe in this run · **[inference]** = conclusion
drawn from observations, stated as such · **[unknown]** = not settled, with the probe that
would settle it. Naming note: the round-6 plan draft called this file
`foreign-aur-risk-plane.md`; the S6-1 assignment names `aur-risk-plane.md` — assignment wins.

---

## 0. What "foreign" means here, and the two ways it was measured [observed]

`pacman -Qm` — 16 rows, 2026-10-14. Foreign = installed in the local db, absent from every
**configured** sync db. That definition is load-bearing, so it was re-measured independently
rather than trusted:

| probe | command | result |
|---|---|---|
| A. pacman's own list | `pacman -Qm \| wc -l` | **16** |
| B. set difference vs sync dbs | union of `tar -tf /var/lib/pacman/sync/{core,extra,multilib,omarchy}.db \| grep '/desc$'` → 15651 unique names; `comm -23 <(pacman -Qq \| sort) <(sync-union \| sort)` | **16** |
| cross-check | `diff` of A's names against B's names | **identical, 16/16** |

Context counts, same run: `pacman -Q | wc -l` = **1188**, `pacman -Qe | wc -l` = **207**,
`pacman -Qme` = **3** (the explicit-foreign trio: `android-apktool-bin`, `obsidian-cli-inspector`,
`omarchy-walker`).

Negative claims each carry their sweep:

- **No foreign package is an orphan.** `pacman -Qmdtq` → no output, rc=1. (The host does have
  3 non-foreign orphans: `pacman -Qdtq` → `electron39`, `mbedtls`, `webp-pixbuf-loader`, rc=0.)
- **None of the 16 has ever been upgraded, downgraded or reinstalled since install.**
  `grep -cE "\] (upgraded|downgraded|reinstalled) <pkg> " /var/log/pacman.log` = **0** for each
  of the 16 (and 0 for `(removed|reinstalled)`).
- **None of the 16 has a pending upgrade.** `pacman -Qu | wc -l` = **0**; per-package
  `pacman -Qu <pkg>` printed empty for all 16 — i.e. they are invisible to the upgrade
  resolver, not merely unchanged.

## 1. The register — 16 rows, per package [observed]

`installed` = `pacman -Qi` *Install Date*, corroborated by the `[ALPM] installed` line in
`/var/log/pacman.log`. `upgraded since` = pacman.log upgrade events (all zero, see §0).
`req-by` = `pacman -Qi` *Required By*. `validation` = the local `%VALIDATION%` field.
`payload` = `pacman -Ql` (file counts; all files live under `/usr/`).

| package | ver | channel | installed | upgraded since | req-by | validation | payload |
|---|---|---|---|---|---|---|---|
| android-apktool-bin | 3.0.3-1 | B AUR-local | 2026-10-13 13:52:59 | never | 0 | `none` | 2 files: `/usr/bin/apktool`, `/usr/share/java/android-apktool/apktool.jar` (14.76 MiB) |
| elephant | 2.21.0-1 | A offline-exile | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `/usr/bin/elephant` (20.86 MiB) |
| elephant-bluetooth | 2.21.0-1 | A | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `/usr/lib/elephant/bluetooth.so` (21.81 MiB) |
| elephant-calc | 2.21.0-1 | A | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `calc.so` (21.78 MiB) |
| elephant-clipboard | 2.21.0-1 | A | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `clipboard.so` (24.34 MiB) |
| elephant-desktopapplications | 2.21.0-1 | A | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `desktopapplications.so` (22.37 MiB) |
| elephant-files | 2.21.0-1 | A | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `files.so` (23.67 MiB) |
| elephant-menus | 2.21.0-1 | A | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `menus.so` (21.65 MiB) |
| elephant-providerlist | 2.21.0-1 | A | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `providerlist.so` (21.83 MiB) |
| elephant-runner | 2.21.0-1 | A | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `runner.so` (21.81 MiB) |
| elephant-symbols | 2.21.0-1 | A | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `symbols.so` (62.50 MiB) |
| elephant-todo | 2.21.0-1 | A | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `todo.so` (30.72 MiB) |
| elephant-unicode | 2.21.0-1 | A | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `unicode.so` (23.88 MiB) |
| elephant-websearch | 2.21.0-1 | A | 2026-10-03 17:44:26 | never | 1 (omarchy-walker) | `sha256 pgp` | `websearch.so` (21.87 MiB) |
| obsidian-cli-inspector | 1.0.3-1 | B AUR-local | 2026-10-13 16:21:20 | never | 0 | `none` | `/usr/bin/obsidian-cli-inspector` (3.33 MiB) |
| omarchy-walker | 1.0.0-2 | A offline-exile | 2026-10-03 17:44:26 | never | 0 | `sha256 pgp` | **no files** (0.00 B meta package) |

Footprint: elephant family **339.09 MiB** (sum of the 13 *Installed Size* values above),
+ AUR pair 18.09 MiB → **357.18 MiB** of the installed set is foreign [observed, arithmetic
on the column above]. Every one of the 16 reports `Packager: Unknown Packager` and
`Install Script: No`; no package's file list contains a path outside `/usr/`; and no
`/var/lib/pacman/local/<pkg>-*/install` file exists for any of them [observed].

Two of the 16 are not AUR packages at all: the 14 channel-A packages were installed from a
**repository** (see §2). "Foreign" here means "no configured repo can claim it", which is a
weaker statement than "came from the AUR" — the register keeps them separate for that reason.

## 2. Channel A — offline-exile (14 packages) [observed, with one inference]

Evidence chain:

1. **The transaction was a repo install, not a file install.** `/var/log/pacman.log:484`
   (2026-10-03T17:42:38): `Running 'pacman -S --noconfirm --needed 1password-beta 1password-cli
   aether alacritty … omarchy-walker … yay zoxide'` — one ~150-target installer transaction.
   There is **no** `[PACMAN] Running 'pacman -U …'` line anywhere for the elephant family or
   `omarchy-walker`; the per-package `[ALPM] installed` lines at `:1096–1110` are the tail of
   that `-S`. So at install time these names resolved through some configured repository.
2. **That repository was `offline.db`.** `/var/lib/pacman/sync/offline.db` (304318 B, gzip tar,
   birth 2026-10-03 17:41:33 = 1 minute before the transaction, mtime 2026-07-20 = upstream
   build stamp) lists **1275** entries including `elephant-2.21.0-1`, all twelve
   `elephant-*-2.21.0-1`, `omarchy-walker-1.0.0-2` and `walker-2.16.2-1` — i.e. **exactly the
   versions that are installed**. `[inference]` channel = the installer's local snapshot repo;
   the version match is the anchor, and no other candidate exists (the four configured dbs
   contain none of the elephant names; `pacman -Sl omarchy | grep -i elephant` → empty).
3. **The channel is dead.** `offline.db` is not a configured repository: `/etc/pacman.conf`
   sections are `[options] [core] [extra] [multilib] [omarchy]` (lines 3/19/22/25/28) and
   `pacman -Sl offline` → `error: repository "offline" was not found` (rc=1). The live omarchy
   channel still carries the *dependency* `walker-2.17.0-1` but **not** `elephant*` and not
   `omarchy-walker` (`tar -tf /var/lib/pacman/sync/omarchy.db | grep '/desc$'` → 231 entries,
   grep for `elephant`/`omarchy-walker` → nothing).
   ⇒ consequence: `-Syu` can neither upgrade nor **reinstall/repair** these 14. If a file is
   damaged or deleted, no configured repo can supply it back.

Trust surface of channel A — signatures exist and verify:

- `gpg --homedir /etc/pacman.d/gnupg --verify /var/cache/pacman/pkg/elephant-2.21.0-1-x86_64.pkg.tar.zst.sig …`
  → `Signature made Wed 15 Apr 2026 11:58:28 AM -03`, `using EDDSA key
  40DFB630FF42BCFFB047046CF0134EE680CAC571`, `Good signature from "Omarchy <pkgs@omarchy.org>" [full]`.
  Sig packet issuer for `omarchy-walker-1.0.0-2` is the same keyid `F0134EE680CAC571`
  (sig created 2025-11-21) [observed].
- The same key signs the live omarchy repo, and `[omarchy]` is the one repo with a relaxed
  policy: `pacman-conf --repo=omarchy SigLevel` → `PackageOptional PackageTrustAll
  DatabaseOptional DatabaseTrustAll`, while core/extra/multilib inherit the global
  `PackageRequired PackageTrustedOnly DatabaseOptional DatabaseTrustedOnly`.
  ⇒ the signatures on channel A are **real but not policy-required** — they were present in
  the snapshot, and pacman would have accepted the same packages unsigned [observed + inference].

`omarchy-walker` is a pure meta package (`pacman -Ql` → no files) whose `Depends On` is
unversioned: `walker elephant elephant-bluetooth elephant-calc elephant-clipboard
elephant-desktopapplications elephant-files elephant-menus elephant-providerlist
elephant-runner elephant-symbols elephant-todo elephant-unicode elephant-websearch`.
That single unversioned edge is the reason all 13 elephant packages show `req-by = 1`, and it
is also why nothing can detect the version crossing described in §4.

## 3. Channel B — AUR-local (2 packages) [observed]

Both were installed as **files**, and the log names the exact artifact:

- `android-apktool-bin` — `/var/log/pacman.log` (2026-10-13T13:52:59):
  `Running 'pacman -U --needed --noconfirm --config /etc/pacman.conf --
  /home/vgpnk/.cache/yay/android-apktool-bin/android-apktool-bin-3.0.3-1-any.pkg.tar.zst'`
  then `Running 'pacman -D --asexplicit -q --noconfirm --config /etc/pacman.conf --
  android-apktool-bin'`.
- `obsidian-cli-inspector` — same shape at 2026-10-13T16:21:20, artifact
  `…/obsidian-cli-inspector-1.0.3-1-x86_64.pkg.tar.zst`, then `pacman -D -q --asexplicit`.
- `--config /etc/pacman.conf` and the follow-up `-D --asexplicit` are the yay (AUR helper)
  idiom; `yay 13.0.1-1` is installed, `paru` is not [observed]. `[inference]` the builder was yay.

AUR provenance, read from the still-present build clones (no network used):

| package | AUR clone HEAD | commit date | subject | `.SRCINFO` pkgver vs installed | clone state |
|---|---|---|---|---|---|
| android-apktool-bin | `92ce7df1217deb19fab6e899a3772459f4198bdc` | 2026-09-28T17:22:27+03:00 | `update to v3.0.3` | 3.0.3-1 = 3.0.3-1 | clean (`git status --porcelain` empty) |
| obsidian-cli-inspector | `ce7b42588bd4f64af509e8b4a336a149ca93f3ca` | 2026-03-08T07:56:23Z | `Update to obsidian-cli-inspector-v1.0.3` | 1.0.3-1 = 1.0.3-1 | 2 untracked build artifacts only, `PKGBUILD` unmodified |

Fetch remotes: `https://aur.archlinux.org/android-apktool-bin.git` and
`https://aur.archlinux.org/obsidian-cli-inspector.git`. Both clones equal the version that is
installed and their working trees carry no local PKGBUILD edits ⇒ the installed binaries were
built from the committed PKGBUILD [observed]. Whether that commit is still the AUR tip, and
whether either package is flagged out-of-date upstream, needs the AUR web API — **out of scope
for this round (no external sites)** → [unknown], probe in §6.

Trust surface of channel B — there is no signature at any point:

- `%VALIDATION%` = `none` for both; `pacman -Qi … Validated By: None`; no `.sig` beside either
  artifact in `~/.cache/yay/<pkg>/` nor in `/var/cache/pacman/pkg/` (neither package has an
  archive there at all — the only copies are the yay build outputs).
- The policy that lets that pass silently is `LocalFileSigLevel = PackageOptional
  PackageTrustedOnly` (`pacman-conf LocalFileSigLevel`) — optional, so a missing signature on
  `pacman -U` is not an error [observed].
- What partially compensates: both PKGBUILDs pin their upstream payload by sha256:
  - apktool: `source=(https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_3.0.3.jar,
    apktool)` with `sha256sums=('dbf930b0…f9423','48a5c9d6…b63bae')`; the package ships the
    downloaded jar plus a wrapper script, `arch=any`.
  - obsidian-cli-inspector: `source=(obsidian-cli-inspector-1.0.3.tar.gz::https://github.com/
    jingyi-zhao-01/obsidian-cli-inspector/archive/refs/tags/obsidian-cli-inspector-v1.0.3.tar.gz)`
    `sha256sums=('561a5301…dfa4f')`, `makedepends=(cargo gcc pkgconf)`, `depends=(sqlite)`,
    `options=(!lto !debug)`, build is `cargo build --release --locked`; `arch=x86_64`.
  ⇒ the fetched bytes cannot silently change; the residual trust is **the PKGBUILD text itself**
  (which runs arbitrary shell as `vgpnk` at build time) plus its AUR maintainer.
- Maintainer surface, as visible in the clone: `android-apktool-bin/PKGBUILD` opens with two
  `# Maintainer:` lines naming humans; `obsidian-cli-inspector/PKGBUILD` has **no** maintainer
  comment at all [observed].
- `~/.cache/yay/vcs.json` = `{}` (2 B) ⇒ no VCS (`-git`) foreign packages are tracked by the
  helper; `completion.cache` is 2.68 MB and stale-capable, not a provenance record.

## 4. The risk decision table — what makes a foreign package risky *here* [measured]

Each row is a risk invariant with the probe that decides it and this host's measured value.
Nothing in this table is asserted from convention; every "fires/does not fire" comes from §0–§3.

| # | invariant (the risky property) | probe | measured on this host |
|---|---|---|---|
| R1 | **no update path** — no configured repo can upgrade *or reinstall* it | `pacman -Si <pkg>` rc, per package | **fires for 16/16** (rc=1, "was not found"); `pacman -Qu` prints none of them |
| R2 | **unreviewable artifact** — installed without signature or validation record | `%VALIDATION%` / `Validated By` | fires for **2/16** (channel B = `none`); not for channel A (`sha256 pgp`, verified Good) |
| R3 | **unattributable packager** — no nameable builder | `%PACKAGER%` | fires 16/16 — **but has no discriminating power here**: 36/1188 installed packages carry `Packager: Unknown Packager`, and those 36 are exactly the foreign 16 **plus** the 20 omarchy-repo packages (all of `1password-beta asdcontrol cliamp hyprland-preview-share-picker limine-mkinitcpio-hook limine-snapper-sync localsend omarchy-keyring omarchy-nvim python-terminaltexteffects spotify tobi-try ttf-ia-writer typora tzupdate ufw-docker walker xdg-terminal-exec yaru-icon-theme yay` report `Repository: omarchy`). Use R2, not R3, to rank foreign risk |
| R4 | **dead-channel exile** — the supplying channel no longer exists | channel still configured? channel still lists the name? | fires for **14/16** (channel A: `offline.db` unconfigured, `pacman -Sl offline` rc=1, and the live omarchy db lists `walker` but no `elephant*`/`omarchy-walker`) |
| R5 | **runtime code, not data** — executes as the user or is loaded by a live daemon | `pacman -Ql` payload + running units | fires **14/16**: 12 × `.so` under `/usr/lib/elephant/`, 1 × `/usr/bin/elephant`, plus the 2 channel-B binaries; `omarchy-walker` contributes no code (0 files) |
| R6 | **install-time code execution** — `install` scriptlet in the package | `%INSTALL%` / `/var/lib/pacman/local/<pkg>-*/install` | fires **0/16** (all `Install Script: No`, no `install` file on disk) |
| R7 | **writes outside `/usr`** — payload that can pre-seed config | `pacman -Ql` paths | fires **0/16** (every path under `/usr/`) |
| R8 | **blast radius** — how much else depends on the row | `pacman -Qi` *Required By* | 13 rows at **1** (all = `omarchy-walker`), 3 rows at **0** (`omarchy-walker`, `android-apktool-bin`, `obsidian-cli-inspector`). No user-installed package depends on any foreign row |
| R9 | **stale artifact** — age of the build vs today | `Build Date` (pacman) − 2026-10-14 | `omarchy-walker` **327 d** (2025-11-21), elephant family **182 d** (2026-04-15), AUR pair **1 d** (2026-10-13) |
| R10 | **version crossing** — a foreign row depends on a repo package that has since moved past the snapshot and no version bound exists to catch it | dependency edge + pacman.log upgrade history | fires **14/16**: `omarchy-walker` → `walker` (unversioned); `walker` was upgraded `2.16.2-1 → 2.17.0-1` on 2026-10-11 16:14:39 (`offline.db` snapshot carries `walker-2.16.2-1`). The 13 elephant rows sit downstream of the same crossing via the meta package |
| R11 | **dependency satisfaction** — is anything already broken/unsatisfied | `pacman -T <all 16>` | rc=**0**, no output: every dependency of all 16 resolves today; `walker` is still present, so R10 has not (yet) produced an unsatisfied dependency |
| R12 | **wiring outside the package db** — who restarts/reinstalls the thing | `pacman -Qo` on unit/autostart files | fires **16/16**: `~/.config/systemd/user/elephant.service` → `error: No package owns …`; `~/.config/autostart/walker.desktop` (138 B, 2026-10-03 17:44) is a user file. Removing any foreign row leaves the wiring in place and failing |

### Reading it as a decision (per class, not per package)

| class | rows | fires | the actual risk on this host | operator action |
|---|---|---|---|---|
| **A offline-exile** (13 elephant + omarchy-walker) | 14 | R1, R4, R5, R10 | code loaded by a live user service, supplied by a channel that no longer exists, and one unversioned edge to a package the channel has already moved past. If `walker`'s ABI/API moved, the providers fail **at load time inside `elephant.service`**, which systemd silently restarts (`Restart=on-failure`, `RestartUSec=100ms`) — a break shows up as a dead launcher, not as a pacman error. Repair path: none from a repo ⇒ keep a copy of the 14 archives + sigs (they are in `/var/cache/pacman/pkg/` today) before anyone prunes that cache | snapshot-preserve `offline.db` + the 15 archives; re-test the launcher after any `walker` upgrade; if the channel is truly retired, treat the 14 as vendor-vendored software, not Arch packages |
| **B AUR-local** | 2 | R1, R2, R5 | no signature ever existed; update path is yay 13.0.1-1 (itself from the omarchy repo, `Validated By: SHA-256 Sum Signature`). Residual risk is review-on-update: the next `yay -Syu` rebuilds whatever the AUR PKGBUILD says at that moment, with `LocalFileSigLevel = PackageOptional` letting the result in unsigned again. Both current PKGBUILDs pin upstream sha256; `obsidian-cli-inspector`'s declares no maintainer | before the next AUR update: diff the PKGBUILD against the clone in `~/.cache/yay/<pkg>/`, confirm the sha256 pins changed coherently with `pkgver`, then build. Do not "fix" the missing signature by relaxing policy — record the decision instead |
| **B AUR-local that stopped being supplied** | 0 | — | `android-apktool-bin` and `obsidian-cli-inspector` are both still ordinary AUR packages as far as a local probe can tell; their AUR-side liveness is [unknown] | §6 probes |

**R3's lesson, kept:** on an omarchy host `Packager: Unknown Packager` distinguishes the
*channel*, not the trust level. A count of "unknown packager" packages is 36/1188 here and
would be misleading as a risk score; the field that separates channel A from channel B is
`%VALIDATION%` (14 rows signed, 2 rows `none`).

## 5. Live exposure state and the one recorded degradation event [observed]

The stack is not inert: it is running now.

- `systemctl --user status elephant.service` → `active (running) since Wed 2026-10-14 13:11:08 -03`,
  `Main PID 1203474`, 29 tasks, 45.5 M memory (peak 370.8 M). Unit file
  `~/.config/systemd/user/elephant.service` (not package-owned), `Restart=on-failure`,
  `WantedBy=graphical-session.target`.
- `systemctl --user list-units --all | grep -iE 'elephant|walker'` →
  `app-walker@autostart.service  loaded active running` and `elephant.service loaded active running`.
- Today's boot: `journalctl --user -b | grep -ic elephant` = **132** lines, of which
  `grep -iE 'error|fail|panic|warn'` = **0**. Provider load list from the 13:11 startup includes
  `runner symbols todo unicode websearch menus providerlist desktopapplications files clipboard`
  plus `bluetooth available="bluetoothctl not found. disabling"` (a provider self-disabling for a
  missing external tool, not a load failure).

Exactly one failure event exists in the user journal for this stack:

```
Oct 11 16:14:34 plazir27 systemd[1582]: elephant.service: Main process exited, code=exited, status=1/FAILURE
Oct 11 16:14:34 plazir27 systemd[1582]: elephant.service: Failed with result 'exit-code'.
Oct 11 16:14:34 plazir27 systemd[1582]: elephant.service: Scheduled restart job, restart counter is at 1.
```

Timeline around it (same journal/pacman.log, 2026-10-11): `16:14:34` the running instance exits
`status=1` → `16:14:35` systemd restarts it and it loads **all** providers cleanly
(`startup=147.923584ms`) → `16:14:39` `[ALPM] upgraded walker (2.16.2-1 -> 2.17.0-1)`.
The journal contains **no** diagnostic line from the failing instance — it produced nothing
between 16:13:30 and the exit — so the cause is **[unknown]**; the correlation with the
transaction is real, the causal claim is not made. What *is* measured: the failure was
recovered automatically, and the foreign stack has run since without a repeat
(one restart counter total, `restart counter is at 1`).

Note for anyone re-dating these packages: `/usr/bin/walker` has filesystem mtime
`Jul 26 21:42` although it was installed 2026-10-11 — pacman preserves upstream build stamps.
Use `Install Date`, not mtime (same trap as the sync dbs, already recorded in
`package-state-plane.md`).

## 6. Operator probes (read-only; the ones that would settle the remaining questions)

Paste-safe, no root, no transaction, no network:

```bash
# 1. re-take the census and diff it against this register (16 rows expected)
pacman -Qm | awk '{print $1}' | sort > /tmp/fp.txt; wc -l < /tmp/fp.txt
# 2. per-row "no update path" (expect rc=1 for every row)
while read -r p _; do pacman -Si "$p" >/dev/null 2>&1; echo "$p rc=$?"; done < <(pacman -Qm)
# 3. orphan sweep (expect empty, rc=1)
pacman -Qmdtq; echo rc=$?
# 4. channel A still resident? (expect the elephant/omarchy-walker names at the installed versions)
tar -tf /var/lib/pacman/sync/offline.db | grep -E '^(elephant|omarchy-walker)'
# 5. channel B provenance (expect the same two commits as §3)
git -C ~/.cache/yay/android-apktool-bin log -1 --format='%H %cI %s'
git -C ~/.cache/yay/obsidian-cli-inspector log -1 --format='%H %cI %s'
# 6. signature verification of channel A (expect Good signature from "Omarchy <pkgs@omarchy.org>")
gpg --homedir /etc/pacman.d/gnupg --verify /var/cache/pacman/pkg/elephant-2.21.0-1-x86_64.pkg.tar.zst.sig \
    /var/cache/pacman/pkg/elephant-2.21.0-1-x86_64.pkg.tar.zst
```

Questions only the operator can put to the network (deliberately **not** run this round):
AUR liveness/out-of-date flags for the two channel-B packages; whether the omarchy channel
intends to re-publish `elephant*`/`omarchy-walker`; whether `walker` 2.17.0 still loads
elephant 2.21.0 providers by design.

## 7. Unknowns and out-of-reach (reported, not absorbed)

1. **Linkage/ABI reality of the 12 provider `.so` files vs `walker` 2.17.0** — whether the
   recorded provider sets still resolve at the symbol level. This is ELF/linkage internals,
   explicitly out of tsukuroi's province and excluded by this round's anti-claim: no
   `readelf`/`ldd`. Row R10 therefore stays **"version crossing observed, breakage unproven"**.
   → route the question to **kaidoku / revenger**, do not answer it here. A non-ELF,
   tsukuroi-legal substitute exists and was not needed today: watch
   `journalctl --user -b | grep -i elephant` after a `walker` upgrade.
2. **Cause of the 2026-10-11 16:14:34 `elephant.service` exit(1)** — journal has no cause line;
   the failing build's own output is absent. Probe: none read-only beyond what was run; next
   occurrence should be captured with `journalctl --user -u elephant.service -o short-precise
   --since …` immediately.
3. **AUR-side liveness** of `android-apktool-bin` / `obsidian-cli-inspector` (tip commit,
   out-of-date flag, maintainer activity) — needs aur.archlinux.org; out of scope (no external
   sites). Local evidence only proves the local clone state.
4. **Whether channel A packages were ever in the *online* omarchy repo** (i.e. withdrawn since
   2026-10-03, or never published) — needs omarchy's repo history/network; the local snapshot
   cannot distinguish "removed" from "never had it".
5. **True cache size**: 3 `download-*` subtrees under `/var/cache/pacman/pkg/` are mode 700
   `alpm:alpm` and unreadable at `vgpnk` level; whether the 15 channel-A archives + sigs are
   complete there is verified only for the files that are world-readable (they are).
6. **Whether `walker`-adjacent breakage could be caught earlier**: `pacman -T` (R11) is rc=0 and
   will stay rc=0 across an ABI change, because the only constraint is the unversioned
   `Depends On: walker`. No local probe can convert R10 into a checked dependency — this is a
   design property of the meta package, not a measurement gap.

## 8. Forward spec — what this register implies for the census (written, not implemented)

`tools/tsukuroi-census.sh` (foreign-count arm at `:303-325`; `degraded-foreign` fixture at
`:820-822`) today reports `foreign=<count>` and forces `PKG_V=DEGRADED` for any non-zero count.
The register above is the evidence that a bare count cannot distinguish "signed, running,
recoverable-in-place" from "unsigned AUR build with no signature ever". The S6-1 assignment
writes only this file, so the gate change is specified here rather than made:

- add a machine-readable baseline (`corpus/knowledge/aur-risk-plane.tsv` or an embedded block)
  with one row per foreign package: `name  version  class  validation  first_seen`;
- census reads the baseline and reports `foreign=16 known=16 new=0 drift=0` instead of `16`;
- fail-closed semantics: a package **absent** from the baseline (new foreign), or present with a
  **different version**, must keep the DEGRADED verdict — the baseline may split the report,
  never downgrade a verdict (this is the anti-claim in the round-6 plan, restated);
- three selftest fixtures: baseline-hit (HEALTHY-equivalent note), baseline-new (DEGRADED),
  version-drift (DEGRADED).

## Errata (append-only)

- **E-1** 2026-10-14 — first `pacman -Qi` collection was written through
  `… | tee qi-all.txt | head -120`: `head` closed the pipe, `tee` died on SIGPIPE, and the file
  held only ~120 lines (it ended mid-package at `elephant-menus`). The register's Build Date /
  Installed Size / Required By cells were therefore re-collected into a complete 176-line file
  before any of them were used. No claim in this document rests on the truncated collection.
  [observation]
- **E-2** 2026-10-14 — a proposed per-package sweep (`for n in $(comm …); do pacman -Si "$n";
  done`, ~1046 invocations) was started and then **stopped** and replaced by the batched
  sync-db-union diff in §0 B, which answers the same question in 0.08 s. The stopped run made
  no writes and produced no output used here. [observation]

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — read-only pacman foreign-package/config queries, sync-db reads and package signature checks on host `plazir27`, 2026-10-14; S032 `/var/log/pacman.log`.
verified-at: 2026-10-14 (the register's original measurement window recorded in this note).
recheck: 90d; procedure: §7's explicit foreign-package, repo-resolution, orphan and provenance probe set.
supersedes the pointer-only recheck: line above.


## R18-FRESHNESS — context package count (2026-10-20)

Now (2026-10-20): 1395 local-db package entries (directory count, not pacman -Q).

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:25 (S060).

Historical snapshot preserved: the 2026-10-14 text above is unchanged and stays true at its date. This notice supersedes it for current use only. Read-only scope; no package, reboot or service clearance.

## R18-FRESHNESS — orphan set (2026-10-20)

Now (2026-10-20): S065 records removal of mbedtls and electron39 at08:14:13 and webp-pixbuf-loader at09:39:21. Those removal events do not classify the current orphan set, which was not queried here [Supporting capture context: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:4-8, .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:89-94].

Capture: .ufo/waves/round-17/l1-capture/boot-chain-capture.txt:57 (S051).

Historical snapshot preserved: the 2026-10-14 text above is unchanged and stays true at its date. This notice supersedes it for current use only. Read-only scope; no package, reboot or service clearance.


- Checked byte anchor for R18-FRESH-NoticeAur-02: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:6 (supporting command/output context remains above).
## R18-FRESHNESS — upgrade history of the register (2026-10-20)

Now (2026-10-20): S065 records base elephant upgraded2.21.0-1→2.22.1-1 at09:31:03 and the ALPM transaction completed09:31:04; S060 separately lists elephant-2.22.1-1 in local metadata. These are historical package events, not current unit/ABI/repair clearance [Supporting capture context: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:40-69, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39].

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:72 (S060).

Historical snapshot preserved: the 2026-10-14 text above is unchanged and stays true at its date. This notice supersedes it for current use only. Read-only scope; no package, reboot or service clearance.


- Checked byte anchor for R18-FRESH-NoticeAur-03: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:43 (supporting command/output context remains above).
## R18-FRESHNESS — no pacman -U line (2026-10-20)

Now (2026-10-20): S060 records the two pacman -U invocation headers; S065 separately supplies ALPM completion records for elephant09:31:04 and zcode13:23:09. Header text alone was insufficient, and no client exit status or zcode foreign classification is claimed [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:70-74, .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:40-69, .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:97-101].

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:73 (S060).

Historical snapshot preserved: the 2026-10-14 text above is unchanged and stays true at its date. This notice supersedes it for current use only. Read-only scope; no package, reboot or service clearance.


- Checked byte anchor for R18-FRESH-NoticeAur-04: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:69 (supporting command/output context remains above).
## R18-FRESHNESS — offline.db snapshot (2026-10-20)

Now (2026-10-20): offline.db is absent from the 2026-10-20 sync directory listing (core.db, extra.db, multilib.db, omarchy.db, openai-chatgpt.db); the 1275-entry snapshot is not on disk at R18 [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:48-55].

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:54 (S060).

Historical snapshot preserved: the 2026-10-14 text above is unchanged and stays true at its date. This notice supersedes it for current use only. Read-only scope; no package, reboot or service clearance.

## R18-FRESHNESS — elephant register row (2026-10-20)

Now (2026-10-20): base elephant metadata is2.22.1-1 and S065 records an upgrade from2.21.0-1, so the historical upgraded-since=never field is superseded for that package. S065 contains thirteen elephant-family upgraded events, separate from installed debug packages [Supporting capture context: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:43-69, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39].

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:30 (S060).

Historical snapshot preserved: the 2026-10-14 text above is unchanged and stays true at its date. This notice supersedes it for current use only. Read-only scope; no package, reboot or service clearance.

## R18-FRESHNESS — R1 update-path count (2026-10-20)

Now (2026-10-20): R1 repository-resolution count was not remeasured and is [unk] for current use; the sync directory lists omarchy.db with mtime2026-10-20 09:09:26 -0300, which is not proof of local metadata refresh time.

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:45 (S060).

Historical snapshot preserved: the 2026-10-14 text above is unchanged and stays true at its date. This notice supersedes it for current use only. Read-only scope; no package, reboot or service clearance.

## R18-FRESHNESS — R2 validation count (2026-10-20)

Now (2026-10-20): S065 identifies thirteen elephant-family events as upgraded, not reinstalled, and records ALPM transaction completion. Current %VALIDATION% fields were not read by these captures and remain unknown here [Supporting capture context: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:43-69].

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:72 (S060).

Historical snapshot preserved: the 2026-10-14 text above is unchanged and stays true at its date. This notice supersedes it for current use only. Read-only scope; no package, reboot or service clearance.

## R18-FRESHNESS — running state (2026-10-20)

Now (2026-10-20): S065 confirms the historical elephant-family package upgrade events; present unit activity and running-process versions remain unknown because package events do not answer those questions [Supporting capture context: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:43-69].

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:72 (S060).

Historical snapshot preserved: the 2026-10-14 text above is unchanged and stays true at its date. This notice supersedes it for current use only. Read-only scope; no package, reboot or service clearance.

## R18-FRESHNESS — configured sync databases (2026-10-20)

Now (2026-10-20): pacman.conf was not re-read at R18; the sync directory holds openai-chatgpt.db (mtime 2026-10-16) and no offline.db, so the four-section list is [unk] for current use [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:48-55].

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:53 (S060).

Historical snapshot preserved: the 2026-10-14 text above is unchanged and stays true at its date. This notice supersedes it for current use only. Read-only scope; no package, reboot or service clearance.

## R18-RECHECK — steer-safe procedure

Appended 2026-10-20 by the tsukuroi round-18 build; earlier bytes unchanged. Supersedes the recheck: line at :15, the recheck: line at :347 (its pointer to the §6 and §7 probe set), and the pacman-invoking probes at :265-280, for any round whose steer forbids running pacman (QUALITY 26). File reads replace them; the substitution is recorded in that round's report. Read-only; no package, reboot or service clearance.

Procedure (file reads only):

- `ls -1 /var/lib/pacman/local` — installed census by directory name; the version is the suffix. Replaces the count probes at :15 and :36-40.
- `cat /var/lib/pacman/local/<pkg>-<ver>/desc` — per package: %VALIDATION%, %PACKAGER%, %INSTALLDATE%, %REASON%. Replaces the install-date and validation probes in §0 and §4 R2-R3.
- `grep -E "\[ALPM\] (installed|upgraded|downgraded|reinstalled|removed) " /var/log/pacman.log` — install and upgrade history per package name. Replaces the upgrade-count probe at :48-50.
- `grep -E "\[PACMAN\] Running" /var/log/pacman.log` — transaction headers, including -U and -Rns lines. Replaces the search at :98.
- `ls -1 /var/lib/pacman/sync` — repository databases present. Replaces the configured-section probe at :109.
- `tar -tf /var/lib/pacman/sync/omarchy.db | grep -E "^(elephant|omarchy-walker)"` — repository entries for the register names; repeat for each other .db file. Replaces the per-row repository-resolution probe at :197 and the offline.db probe at :273.
- `grep -A1 "^%REASON%" /var/lib/pacman/local/*/desc` — dependency-installed candidates for the orphan sweep. Reverse-dependency confirmation is [unk] until checked against the depends files.
- `git -C ~/.cache/yay/<pkg> log -1 --format='%H %cI %s'` — AUR clone head for channel B.

Not replaced: the pending-upgrade count (-Qu) and the unit state of elephant.service. Both are [unk] under this procedure; read the unit file with cat ~/.config/systemd/user/elephant.service if the unit definition is needed.


## R18-FRESHNESS — remaining AUR classification neighbors (2026-10-20)

Sources S060/S065. The R4/section2 no-repair, R5 runtime, R9 age and orphan claims are retained as dated historical measurements; their current-use interpretations are superseded below.

- R18-FRESH-SUPPLEMENT-41: R4 and section2 channel/no-repair conclusions are historical repository/configuration observations, not a current reachability result. S060 supplies directory inventory only; neither S060 nor S065 reruns package/repository resolution. Present dead-channel membership is unknown [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:48-55]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:53.

- R18-FRESH-SUPPLEMENT-42: the historical R5 payload/runtime classification has not been remeasured; S065 package-upgrade events do not prove current payload or running units. Keep the historical enumeration separate from present runtime state [Supporting capture context: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:43-69]. Capture: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:43.

- R18-FRESH-SUPPLEMENT-43: the historical182-day elephant build-age reading is tied to the old version/date. S060 observes base elephant2.22.1-1, but replacement build dates were not captured here; current build ages are unknown [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:30.

- R18-FRESH-SUPPLEMENT-44: the old assertion that no foreign package is an orphan is a dated classification, not a current orphan census. S065 proves specific removal events but not present foreign/orphan membership; that membership remains unmeasured here [Supporting capture context: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:4-8, .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:89-94]. Capture: .ufo/waves/round-18/l1-capture/pacman-events-r18.txt:6.

No package/upgrade/restart or repair action is authorized.


## R18-ARITHMETIC — historical R5 enumeration

The old R5 row at201 says14/16 but literally enumerates12provider packages +1base elephant +2channel-B packages:15, not14. Counting command: `python3 -c 'print(12 + 1 + 2)'` (round18 immutable evidence runner retains its observed output). This corrects the historical arithmetic, not current payload, unit activity or foreign membership. The old row and its measurement date remain intact; do not carry either its old count or its old runtime classification forward as current. Source: original R5 row201, exact enumeration; FxFresh02's counterexample.

The orphan notice also supersedes current use of both claims at46–47; it is not a present orphan census. The no-update-route notices cover section2 and R1/R4 broadly, not only a single quoted table cell. S065 adds actual ALPM event evidence for the historical removals/upgrades; where a narrower S060-only notice says an invocation does not establish completion, that evidence limitation remains true of S060 but the S065 companion now resolves the specified historical event.
