# Update-safety v2 — r2 note re-run, AUR risk classes joined, risk-ordered install table (TSUKUROI-R7-S7-3)

source: live read-only probes, host `plazir27`, user `vgpnk` (non-root), single pass
2026-10-14 18:19–18:26Z (15:19–15:26 -03); scratch `/tmp/w7-s73-tsukuroi/` (files named
in §9). Verbs run: `pacman -Qu`, `pacman -Sup --print-format`, `pacman -Syu
--print-format`, `pacman -Suu --print-format` (plan-only family — no transaction, no
download, no db write; `db.lck` checked absent before and after each), `pacman
-Q|-Qe|-Qm|-Qmdtq|-Qdtq|-Qi|-Qkk`, `pacman -Si|-Sl`, `pacman-conf`, `stat`, `grep` /
`md5sum` over `/var/log/pacman.log`, `bsdtar -tf` over the sync dbs, `git -C` reads of
the two yay build clones, `sha256sum`, `systemctl --user` / `journalctl --user` reads.
No `-Sy` / `-Syu` was run; nothing installed, upgraded, removed or restarted; no
external site; no root; no host file written outside the scratch dir.

**Read-only contract held** [observed: `git status --porcelain` empty at pass start and
after; `/var/lib/pacman/db.lck` absent at every check; five `.db` files in
`/var/lib/pacman/sync/` byte-unchanged].

This note is the **re-run** of `corpus/knowledge/update-safety-note.md` (TSUKUROI-R2-2;
md5 `5cc3067fec33d261d8bff6a5c7e8ac48`, 478 ln — unchanged since landing) with the
round-6 **AUR risk classes joined**: the register `corpus/knowledge/aur-risk-plane.md`
(S6-1; md5 `1a584300f6b07da78bc8332f04b4fd30`, 341 ln per `wc -l`) and its provenance
receipt `corpus/knowledge/foreign-provenance-r6.md` (TSUKUROI-R6-S6-2; md5
`1b8f47a2a807fc8bd2fc7302f15577c8`, 307 ln). Mandate: `plans/round-7.plan.md` claim (b)
(md5 `bb9159549bfdad7516af381f6f12965d`, 160 ln). Claim (a) of that plan — the censused
5th plane — is a sibling lane's deliverable and is **not** carried in this file (§10).

Tags: **[observed]** = measured in this window, command named · **[inference]** =
drawn from observations, stated as such · **[unknown]** = named gap with the probe that
would settle it.

Round-6 landing state read at this pass [observed]: HEAD `dc3436d` (`probation round 6
(training r5)`), `git status --porcelain` empty; register + receipt + verifier note +
OOM plane committed. **Unlanded from round 6's own measure:** no machine-readable
baseline file exists (`ls corpus/knowledge/*.tsv` → no such file; `grep -n baseline
tools/tsukuroi-census.sh` → only the comment at `:43`), and the census is still the 4-plane
`e9327046b05b5c71e07fe511ad7e82dd`, 1032 ln. Named debt, not smoothed (§10).

## 1. Re-run receipts — r2 pin vs v2 value

All r2 values are citations of the landed note; all v2 values are this window's
measurements (`/tmp/w7-s73-tsukuroi/`, files in §9). "same" means same value *and* same
meaning.

| # | pin (r2) | r2 value (10:44–10:51 -03) | v2 value (18:19–18:26Z) | verdict |
|---:|---|---|---|---|
| 1 | `pacman -Qu` | rc=1, 0 lines (`:23`) | rc=1, 0 lines (unpiped) | same |
| 2 | `pacman -Sup --print-format '%r/%n %v'` | rc=0, 0 lines (`:24`) | rc=0, 0 lines | same |
| 3 | version join (installed vs repo-resolved) | 1171 equal / 0 behind / 1 ahead (`:25-31`) | 1188 installed, 15 663 repo rows, common 1172: **1171 / 0 / 1** | same |
| 4 | live sync-db births | 2026-10-11 12:54:13.542054496 ×4 (`:46-49`) | identical ×4 (core/extra/multilib/omarchy) | same — no refresh since |
| 5 | core/extra/multilib content stamp | 2026-09-08 15:23 (`:46-49`) | identical; **36 d 0 h** at 18:23Z | same age class |
| 6 | `offline.db` | birth 2026-10-03 17:41:33.994891750; not configured (`:50,67-69`) | identical; still unconfigured | same |
| 7 | pins | `IgnorePkg`/`IgnoreGroup`/`NoUpgrade`/`NoExtract` empty; `HoldPkg = pacman glibc` (`:208-216`) | identical (all four rc=0 empty; HoldPkg two lines) | same |
| 8 | foreign census | 16 (`:34`) | 16; `comm` cross-check gives the identical 16 names | same |
| 9 | orphans | 3 (`:307-308`) | 3: `electron39`, `mbedtls`, `webp-pixbuf-loader` | same |
| 10 | rollback net | `snapper list-configs` 0 configs (`:289-292`) | 0 configs (header + rule only, 2 lines, rc=0) | same — still open |
| 11 | dkms | stale `7.1.4-arch1-1` row + current `7.2.3` (`:294-300`) | identical two rows, same text | same |
| 12 | cache | 8.6 G, 1568 zst + 1568 sig + 3 alpm temp dirs (`:313-319`) | 8.6 G, 1568 zst, 3139 entries, 3 `download-*` dirs (alpm:alpm 700) | same |
| 13 | `-Suu` downgrade trap | [inference] (`:280-284,374-375`) | **measured**: `-Suu --print-format` rc=0, **1 action** — `omarchy/1password-beta 8.12.42_32.BETA-1` | evidence upgraded |
| 14 | workload contention | 75 × `ffmpeg` at 10:51 (`:324-330`) | no ffmpeg this window; load 3.10/1.21/1.12, top comms `bash` 26, `chromium` 15, `grep` 7 (sibling lanes' probes included) | moved — live value, re-run |
| 15 | boot | boot 2026-10-13 11:02, uptime 23 h 51 m (`:4-5`) | same boot (`boot_id d7f0bc8d938e4249b4a1f250cbfacf58`), uptime 1 d 4 h 22 m at 15:20 -03 | same boot |
| 16 | `/boot` | `ls /boot` rc=2 permission denied (`:350`) | rc=2, `ls: cannot open directory '/boot': Permission denied` | same — BLOCKED stands |

The one **semantic upgrade** is row 13: what r2 could only infer is now a printed plan
(§2.3). Nothing else moved — this host has had no pacman activity since 2026-10-13
16:37:59 (log mtime unchanged, §3), so the re-run reproducing r2 is expected, not
independent confirmation. The freshly joined AUR classes are §4.

## 2. Candidate space, re-run three ways — plus the one verb r2 never ran

### 2.1 The empties [observed]

| probe | result | rc |
|---|---|---|
| `pacman -Qu` (unpiped) | 0 lines | 1 |
| `pacman -Sup --print-format '%r/%n %v'` | 0 lines | 0 |
| `pacman -Syu --print-format '%r/%n %v'` | 0 lines | 1 |
| version join (`expac -Q` 1188 vs `pacman -Sl` ×4 repos 15 663 rows; repo order core>extra>multilib>omarchy, first wins) | 1172 common · 1171 equal · **0 behind** · **1 ahead** | — |

- 0 behind ⇒ nothing installed is older than its effective repo entry; three probes
  agree. 1 ahead ⇒ `1password-beta` installed `8.12.42_32.BETA-32` vs `[omarchy]`
  `8.12.42_32.BETA-1` (re-measured: `pacman -Qi`/`pacman -Si` both name `omarchy`;
  `pacman -Sl omarchy` shows `linux-firmware-cirrus 20260810-3 [installed: 20260810-2]`,
  `walker 2.17.0-1`, `yay 13.0.1-1`).
- `comm -23` cross-check, this pass: installed 1188 names minus sync-union 15 651 names
  = **16**, and the 16 names are identical to `pacman -Qm` (diff clean in the Python
  join; `qm.txt` in scratch). The round-6 receipt's "byte-identical since 09:54" claim
  extends: no foreign version line has moved since.
- Shadowing re-measured, same 12 name collisions and 5 shadowed-newer rows as r2
  (`:262-273`): `linux-firmware-cirrus` (core `20260810-2` < omarchy `20260810-3`) plus
  the `ghostty` quartet (extra `1.3.1-2` < omarchy `1.3.1-3`, not installed).
  `pacman -Sl omarchy` prints `[installed: 20260810-2]` for the cirrus row — that *is*
  the shadowing, visible in the channel listing but never in `-Qu`.

### 2.2 What is an "official candidate" and what is an "AUR-class candidate"

There are two disjoint candidate spaces on this host, and the fix for the r2 note's
open question is to state them separately:

- **Official space** — names resolvable against the 4 configured repos
  (`core`, `extra`, `multilib`, `omarchy`; `pacman-conf --repo-list` → exactly those;
  no `[offline]` section — `grep -c offline /etc/pacman.conf` = 0). Today: 0 candidates.
  After an operator `-Sy` it becomes a real set decided by the mirror snapshot —
  read-only unmeasurable (`UNKNOWN-UPSTREAM`, unchanged from r2 §7 row 14).
- **AUR-class space** — the 2 `AUR-local` foreign packages (§4). They are *never* in
  the official space (`pacman -Si` rc=1 ×16) and never in `-Qu` by construction;
  their only mover is `yay` (external, not the gate's verb).
- **Outside both** — the 14 `offline-exile` rows: no configured repo, no AUR-verified
  provenance, no route at all. They are not candidates; they are held inventory (§4).
- **Hidden in the official space** — the 5 shadowed-newer names: candidates in fact,
  invisible to `-Qu` while repo order stands.

### 2.3 The plan verb r2 inferred — now measured [observed]

`pacman -Suu --print-format '%r/%n %v'` (plan-only; same allowed family as
`-Sup --print*`, `SKILL.md:408-413`) printed exactly one action:

```
omarchy/1password-beta 8.12.42_32.BETA-1
```

⇒ a `-Suu` on this host would perform exactly one "upgrade": the **downgrade** of
`1password-beta` from BETA-32 to an older beta. `db.lck` absent before and after; rc=0.
The r2 row "`-Suu` / `-Syyu`: do not run" (`:374-375`) is now a measured plan, not an
inference. `-Syyu` was not run and stays refused by rule (it re-downloads 36-day-stamped
dbs for no benefit — r2 §7 row 3).

## 3. Channel provenance rows (the facts the census arm folds)

Re-measured this window; these are exactly the rows `plans/round-7.plan.md` claim (a)
specifies the gate to print (birth is authoritative; the log adds the command class).

| row | probe | value |
|---|---|---|
| live db births | `stat -c '%w' /var/lib/pacman/sync/{core,extra,multilib,omarchy}.db` | all four `2026-10-11 12:54:13.542054496 -0300` |
| db content stamps | `stat -c '%y'` | core/extra/multilib `2026-09-08 15:23:4x`; omarchy `2026-10-11 10:16:17` |
| db sizes | `stat -c '%s'` | 129 469 / 8 900 506 / 84 692 / 48 989 B — byte-equal to r2 |
| `.db.sig` files | `ls /var/lib/pacman/sync/` (5 `.db`, no `.sig`) | **0** |
| offline snapshot | `stat` + `bsdtar -tf` + `pacman-conf --repo-list` | present (304 318 B, birth 2026-10-03 17:41:33.994), **unconfigured** → inert, 28 listing lines match `^(elephant\|omarchy-walker)` (13 elephant pkgs + `omarchy-walker`, dir+desc each) |
| last refresh command | `/var/log/pacman.log:1405` | `2026-10-11T12:54:13-0300 Running 'pacman -Sy --noconfirm fuse2'` — **second-exact** with the four db births |
| last full upgrade | `:1414` | `2026-10-11T16:13:19-0300 Running 'pacman -Syu --noconfirm godot blender …'` |
| last `-U` (yay-cache installs) | `:2090`, `:2097` | 2026-10-13 13:52:59 (`android-apktool-bin`), 16:21:20 (`obsidian-cli-inspector`) |
| last transaction | `:2104-2108` | 2026-10-13 16:37:59, `git-filter-repo`, completed — 20 completed transactions in the log, none since |
| log identity | `md5sum`, `wc -l`, `stat` | md5 `e452d910de724ac016c2d019f9e1ec45`, 2109 lines, 157 286 B, mtime 2026-10-13 16:37:59 — unchanged since the round-6 receipt |
| keyring/trust config | `pacman-conf` / `/etc/pacman.conf` | `SigLevel = Required DatabaseOptional` (`:15`), `LocalFileSigLevel = Optional` (`:16`), `[omarchy] SigLevel = Optional TrustAll` (`:29`) |

Log-window note: if the arm's bounded `pacman.log` tail ever misses line 1405 (rotation),
the correct row is `command=unknown` — birth stamps above are the authoritative refresh
anchor, not the log (plan claim (a), restated).

## 4. The AUR-class join — class × update-path truth table

Classes and per-row evidence are the round-6 register's (`aur-risk-plane.md:190-221`,
`:55-89`); the *update-path* column below is this note's addition — what each class's
path can and cannot reach, measured against the configured channel set. The join is the
point of v2: the r2 decision model asked "is it safe to `-Syu` now?"; the r6 classes
answer the follow-up "and what would that `-Syu` never touch?".

| class | n | members | `-Syu` reach | helper (yay) reach | repair path | recheck |
|---|---:|---|---|---|---|---|
| official-sync (all repo-resolved installs, incl. 26 `[omarchy]` rows) | 1172 ∩ repos | — | upgrade + reinstall | n/a | repo | `pacman -Qu`; `-Sup --print-format` |
| `aur-local` | 2 | `android-apktool-bin` 3.0.3-1, `obsidian-cli-inspector` 1.0.3-1 | **none** (`pacman -Si` rc=1 both) | yes — `yay -Syu`/rebuild; review-on-update; upstream state [unknown] (no network) | rebuild from the retained clone in `~/.cache/yay/<pkg>/` (offline, local) | clone HEAD + `sha256sum` artifacts vs `PKGBUILD` `sha256sums` |
| `offline-exile` | 14 | 13 × `elephant*` 2.21.0-1 + `omarchy-walker` 1.0.0-2 | **none** (`pacman -Si` rc=1 ×14) | none configured; a helper *adopting* one of these names would be a provenance change, not an update [unknown whether they exist in the AUR — needs network] | **none from any repo**; the cached channel-A archives (14 `.pkg.tar.zst` + 14 `.sig`, all world-readable) are the only copy | `bsdtar -tf /var/lib/pacman/sync/offline.db \| grep -E '^(elephant\|omarchy-walker)'`; `ls /var/cache/pacman/pkg/` count |
| `unknown-provenance` (rule, 0 rows today) | 0 | — | class must never be guessed | — | probe order, in this order: pacman.log `-U` grep → `~/.cache/yay/<pkg>/` → `pacman -Qi` *Validated By* → `offline.db` listing | the four probes |
| `out-of-reach` (routed, not absorbed) | 1 question | `walker` 2.17.0-1 vs elephant 2.21.0-1 provider load (R10, linkage) | n/a | n/a | → **kaidoku / revenger** (no `readelf`/`ldd` in-province); tsukuroi-legal substitute: `journalctl --user -b \| grep -i elephant` after any `walker` upgrade | that journal watch |

This-window re-measurements behind the table (all [observed]):

- the 16 remain 16 (`pacman -Qm` rc=0; `pacman -Qmdtq` empty rc=1); all 16 still
  `pacman -Si` **rc=1**; `Validated By` fields re-read per package: 14 × `SHA-256 Sum
  Signature` (desc `%VALIDATION%` = `sha256` + `pgp`), 2 × `None`.
- `pacman -Qkk android-apktool-bin obsidian-cli-inspector omarchy-walker elephant` →
  rc=0, `0 altered` on each (the register's R6/R11 sweep clean again).
- AUR pair chain intact: clone HEADs `92ce7df1…` / `ce7b4258…` (identical to the r6
  receipt §5), build artifacts `sha256 e83409b2…` / `a6ec77fa…` equal to the receipt,
  and the fetched sources still match their PKGBUILD pins — `apktool_3.0.3.jar`
  `dbf930b0…f9423` = `sha256sums[0]`, `obsidian-cli-inspector-1.0.3.tar.gz`
  `561a5301…dfa4f` = the single `sha256sums` entry. `yay v13.0.1 - libalpm v16.0.1`;
  `~/.config/yay/config.json` absent (no helper-level pin to read); `paru` not installed.
- Exile chain intact: `offline.db` still carries the installed versions; all 14 archives
  + sigs still in `/var/cache/pacman/pkg/` (28 matching entries); live consumer still up —
  `elephant.service` active, `app-walker@autostart.service` active, `journalctl --user
  -b` elephant lines 132, error/fail/panic/warn matches 0 (identical shape to r6 §5).

**Reading the join as a sentence.** The 16 foreign packages are invisible to every
official candidate probe not because they are current but because no configured channel
can see them (R1); the 2 AUR-local are updateable only outside the gate's vocabulary
(review-on-update), and the 14 offline-exile are not updateable at all — for them the
only safe operations are preservation and observation (R4/R10). The r2 note's
"empty ≠ up to date" (§2) therefore has a second half: **"resolvable ≠ maintainable"** —
an `-Syu` that reports 0 actions says nothing about the 357.18 MiB of installed code no
repo can reach (`aur-risk-plane.md:81-85`).

## 5. Pins and holds, re-run [observed]

| source | probe | value |
|---|---|---|
| `/etc/pacman.conf:7` | `pacman-conf HoldPkg` | `pacman glibc` (removal-protection, **not** a version hold — r2 `:218-222`, unchanged) |
| any | `pacman-conf IgnorePkg` / `IgnoreGroup` / `NoUpgrade` / `NoExtract` | all empty rc=0 — no version pins |
| `/etc/pacman.conf:15-16` | `pacman-conf SigLevel` / `LocalFileSigLevel` | `Required DatabaseOptional` / `Optional` |
| `/etc/pacman.conf:28-30` | `pacman-conf --repo omarchy SigLevel` | `PackageOptional PackageTrustAll DatabaseOptional DatabaseTrustAll` |
| helper | `yay --version` (no transaction verb) | `v13.0.1`; `~/.config/yay/config.json` absent; `paru` absent |

## 6. Hazards / U-row refresh for a planned wave

Hazard inventory re-run (values are this window's; r2 §6 rows in parentheses):

- **No rollback net — U1, leading exposure.** `snapper list-configs` header+rule only
  (2 lines, rc=0, **0 configs**); `limine-snapper-sync` system unit `enabled` +
  `inactive` (no user unit — `systemctl --user is-enabled` → not-found). Any wave is
  snapshot-less.
- **Upstream delta — U2, the real gate.** `-Qu`/`-Sup` empty against content stamps
  `2026-09-08 15:23` = **36 d 0 h** at 18:23Z; `checkupdates` absent (`command -v` rc=1),
  `pacman-contrib` absent (error text); installing it is out of province. The resolving
  event stays operator-side.
- **Kernel/DKMS coupling — U3.** `uname -r` = `pacman -Q linux` = `7.2.3-arch1-3`;
  `/usr/lib/modules/` = `7.2.3-arch1-3` only; `dkms status` still carries the stale
  `nvidia/610.57.04, 7.1.4-arch1-1 … (Built modules are missing in the kernel modules
  folder)` row beside the current one. No reboot pending today; a kernel-raising wave
  rebuilds in-transaction via `90-mkinitcpio-install.hook`.
- **Trust surfaces — U4.** `[omarchy]` `Optional TrustAll`; `LocalFileSigLevel =
  Optional`; no `.db.sig` stored (5 `.db`, 0 `.sig`). Unchanged, still a written
  accept-or-re-scope decision before a wave.
- **Downgrade trap — U5, now measured.** `-Suu --print` = 1 action (§2.3). Plain `-Syu`
  ignores it; `-Syyu` refused by rule.
- **`/boot` privilege gate — U6.** `ls /boot` rc=2 (Permission denied) — the BLOCKED row
  stands; operator root pre-verify only.
- **`walker-restart.hook` — U7.** File unchanged (user-owned script exec'd by root in
  transactions) — reported to kagi/operator, not absorbed.
- **Workloads — U8.** Load 3.10 / 1.21 / 1.12 at 15:20 -03; memory 30.25 GiB total,
  18.88 GiB available, swap 34.25 GiB; process census top: `bash` 26, `chromium` 15,
  `1password` 6 — the 75 × `ffmpeg` wave of r2 is gone, but the sibling lanes are
  running probes; schedule around *whatever* is live, re-measured at the decision moment.
- Other standing rows: no `db.lck`; `pacman -Dk` clean (`No database errors have been
  found!`); 3 non-foreign orphans; cache 8.6 G / 1568 zst / 3 root-only `download-*`
  dirs; `/sys/class/power_supply/` empty (desktop, AC-only; UPS [unknown], unchanged).

Arm composition for the note-level verdict is r2's, unchanged
(`SKILL.md:358-369`): strongest arm fired, `BLOCKED > UNKNOWN-UPSTREAM >
REQUIRES-PREP > INERT > PASS`. Composed today: `-Syu` now = **INERT** (0 candidates);
post-refresh = **UNKNOWN-UPSTREAM + REQUIRES-PREP** (rows §6 U1–U4, U8);
`-Suu`/`-Syyu` = **DO-NOT**. The mapping of these arms into the gate's
HEALTHY/DEGRADED vocabulary is claim (a)'s decision, not this note's.

## 7. Risk-ordered install recommendation table (recommendation only — nothing here was run)

Ordered by risk: lowest first. This lane **detects and recommends**; the operator acts
(`PROVINCE.md:16-17`). No row was executed; the only plan verbs exercised anywhere in
this pass are the `--print` forms named in the header. "Reach" = what the operation can
actually touch, per §4.

| rank | operation / item | class | reach | measured risk on this host | recommendation |
|---:|---|---|---|---|---|
| 1 | Do nothing now | official | — | `-Syu` would be INERT: 0 actions; the only effect would be the refresh mutation itself, which invalidates the emptiness | No update action is owed today; running `-Syu` for "safety" buys nothing — the gate is the *next refresh*, not the run |
| 2 | Plain `-Syu` after an operator refresh (the wave) | official | core/extra/multilib/omarchy | post-refresh set is UNKNOWN-UPSTREAM; 36 d of drift puts kernel/libc/driver classes in scope; wave cost measured before: 81 s / 505 actions | If currency is wanted, refresh in a planned window with prep (a)–(d) from r2 `:364-373` — rollback decision, dkms verification plan, schedule, trust-channel decision — then re-run `-Qu`/`-Sup` **before** the upgrade |
| 3 | `[omarchy]`-sourced rows inside that wave (26 installed) | official, soft-trust | same wave | `SigLevel = Optional TrustAll`; no `.db.sig`; 5 shadowed-newer names are candidates `-Qu` will never show | Decide the channel policy once, in writing: accept TrustAll, or re-scope; and read the channel listing (`pacman -Sl omarchy`), not only `-Qu`, when auditing what the wave would move |
| 4 | AUR-local updates/rebuilds (2) | `aur-local` | yay only; external; never `-Qu` | no signature ever (`Validated By: None`); `LocalFileSigLevel = Optional`; `obsidian-cli-inspector`'s PKGBUILD names no maintainer; upstream AUR state [unknown] | If an AUR update is wanted: diff the PKGBUILD against the retained clone, confirm the sha256 pins moved coherently with `pkgver`, then build — review-on-update, never blind `yay -Syu`; do not "fix" the missing signature by relaxing policy |
| 5 | The 14 offline-exile packages | `offline-exile` | no path | channel dead (R4); one unversioned `walker` edge already crossed (R10, 2.16.2→2.17.0); repair-by-reinstall impossible (R1) | **Preserve, don't update:** copy `offline.db` + the 14 cached archives/sigs before any cache prune; treat as vendor-vendored software; re-test the launcher after any `walker` upgrade (journal watch, §4) |
| 6 | Repair-by-reinstall of any of the 16 (or sourcing them from somewhere new) | all foreign | none configured | no repo can supply them; improvising a source would change provenance silently | Do not improvise: if a package must be re-sourced, run the `unknown-provenance` probe order first and let the operator record the decision — a class is never guessed |
| 7 | `-Suu`, `-Syyu`, any downgrade/force verb | official | all installed | **measured**: `-Suu` = downgrade `1password-beta` BETA-32 → BETA-1, one action | DO-NOT (verb-level); plain `-Syu` only; `-Syyu` adds nothing but 36-day-old dbs |
| 8 | Orphan removal (`electron39`, `mbedtls`, `webp-pixbuf-loader`) | official | 3 packages | removables, not upgrade blockers; none foreign | Separate, deliberate decision — keep orphans out of any automatic sweep during a wave window |

## 8. Observation / inference / unknown

- **Observed (this pass):** every value in §1–§6 with its command; `-Qu` rc=1 empty;
  `-Sup` 0; `-Syu --print` 0/rc=1; **`-Suu --print` 1 action**; join 1171/0/1 (+shadowing
  12/5); 16 foreign + `comm` cross-check; `-Si` rc=1 ×16; `Validated By` 14+2; `-Qmdtq`
  rc=1; orphans 3; dkms two rows; snapper 2-line header; cache 8.6 G/1568 zst/3139
  entries/3 dirs; log md5 `e452d910…` 2109 ln; db births/content stamps; log
  :1405/:1414/:2090/:2097/:2104-2108; clone HEADs + artifact/source sha256 chains;
  qkk 0 altered ×4; services active; journal 132/0 lines; `/boot` rc=2; load/mem;
  `db.lck` absent before/after every plan verb.
- **Inference (not measured):** the 14 offline-exile channel was `offline.db` (register
  keeps this [inf] with its evidence chain — r6 §2.4 / receipt §2.4; not re-litigated
  here); `HoldPkg` = removal-protection only; a dkms rebuild failure would degrade the
  driver plane at next boot; a soname bump under the foreign set would break it silently
  (unversioned edges — R10); if a helper "adopted" an exiled name from the AUR, the
  installed bytes and the new artifact would not be the same lineage — provenance change,
  not update.
- **Unknown (open):** upstream Arch/omarchy delta since 2026-09-08 (**the** gate; needs
  operator `-Sy` or network); AUR-side liveness/tips of the 2 (needs network); whether
  `elephant*`/`omarchy-walker` exist in the AUR at all (would decide whether a helper
  could even see them — needs network); exact historical repo stanza/`SigLevel` used at
  the 10-03 install (installer config gone); whether a UPS exists; contents of the
  privilege-gated `download-*` dirs; ABI compatibility of elephant 2.21.0 with walker
  2.17.0 (routed out); cause of the one 2026-10-11 `elephant.service` exit(1).

## 9. Sources, scratch, recheck

- **In-lane pins (this pass, `md5sum` + `wc -l` at 18:19Z):** `update-safety-note.md`
  `5cc3067fec33d261d8bff6a5c7e8ac48` / 478 · `aur-risk-plane.md`
  `1a584300f6b07da78bc8332f04b4fd30` / 341 · `foreign-provenance-r6.md`
  `1b8f47a2a807fc8bd2fc7302f15577c8` / 307 · `aur-risk-plane-ver-s6.md` `b0de352d…` / 133 ·
  `SKILL.md` `7b5dcf08b3143839301b7044a130a8cf` / 837 · `tools/tsukuroi-census.sh`
  `e9327046b05b5c71e07fe511ad7e82dd` / 1032 (4-plane — claim (a) not landed) ·
  `package-state-plane.md` `ef93f1b78b6a9e17e8c9d096e7852a02` / 323 · `LOG.md`
  `2d6df41d8a77f32c4e7533ce2abb946d` / 169 · `SCORECARD.md` `9b04eb4d…` / 18 ·
  `corpus/README.md` `98bd00668e84f18cf6781718c4d09ea0` / 20 (round-4/5/6 coverage rows
  still absent) · `plans/round-7.plan.md` `bb9159549bfdad7516af381f6f12965d` / 160.
- **Cited lines:** `update-safety-note.md` §1 :19-40, §2 :42-72, §3 :74-202, §4 :204-222,
  §5 :256-284, §6 :286-330, §7 :332-381 (prep list :364-373; `-Suu`/`-Syyu` :374-375),
  §8 :383-405. `aur-risk-plane.md` §0 :28-53, register table :55-89, R-table :190-208,
  class decision :212-221, unknowns/out-of-reach :287-312, census spec :314-329.
  `foreign-provenance-r6.md` receipt :209-236, recheck :264-276. `SKILL.md` rows :41,:45;
  arms section :359; round-6 append :710+.
- **Scratch (`/tmp/w7-s73-tsukuroi/`, ephemeral):** `qu.out/err` (0 lines, 0 B),
  `sup.out`, `syu-print.out` (0), `suu-print.out` (1 line), `local-nv.tsv` (1188),
  `sl-all.txt` (15 663), `qm.txt` (16), `si-rc.txt` (16 × rc=1), `qdtq.txt` (3),
  `qkk.out`, `snapper.out` (2), `batch1..6.out` (raw captures), `batch2.out` carries the
  Python join.
- **Recheck (compact):**
  `pacman -Qu; echo rc=$?` · `pacman -Sup --print-format '%r/%n %v' | wc -l` ·
  `pacman -Suu --print-format '%r/%n %v'` (expect exactly the 1password-beta row) ·
  `stat -c '%w %y' /var/lib/pacman/sync/*.db` · `pacman -Qm | wc -l` ·
  `while read p _; do pacman -Si "$p" >/dev/null 2>&1; echo "$p rc=$?"; done < <(pacman -Qm)` ·
  `bsdtar -tf /var/lib/pacman/sync/offline.db | grep -cE '^(elephant|omarchy-walker)'` ·
  `git -C ~/.cache/yay/android-apktool-bin log -1 --format='%H %cI'`;
  `git -C ~/.cache/yay/obsidian-cli-inspector log -1 --format='%H %cI'` ·
  `snapper list-configs` · `dkms status` · `md5sum /var/log/pacman.log`.

## 10. Boundary notes and errata (append-only)

- 2026-10-14 (S7-3) — **write scope.** This lane wrote only this file (assignment).
  Owed by others, recorded not absorbed: (i) the one-line **errata pointer into the r2
  note** (append-only, `plans/round-7.plan.md` claim (b)) — `update-safety-note.md`
  is unchanged at md5 `5cc3067f…`; (ii) the `LOG.md` entry for this artifact
  (`AGENTS.md:3`); (iii) the census 5th plane + baseline (claim (a), sibling lane —
  and round 6's own baseline remains unlanded, §0 of the header); (iv) `corpus/README.md`
  coverage rows (rounds 4–6, still absent at md5 `98bd0066…`).
- 2026-10-14 (S7-3) — **what v2 does not re-litigate.** The r6 register's provenance
  chains (offline.db inference, AUR clone state) and the r2 note's class-size touch map
  are cited, not re-derived; only their *update-path* consequence is joined here. Where
  r2's value and r6's value conflicted, none did — this pass found no contradiction,
  only the §4 addition.
- 2026-10-14 (S7-3) — **drift caveat.** Values here are a single live snapshot
  (18:19–18:26Z); counts and service states drift (r2 `:477-478`). Re-run, never quote.
  All §1 "same" verdicts are same-as-r2's measurement, not independent re-validation of
  r2's interpretation.
- 2026-10-14 (S7-3) — **method note kept:** `pacman -Suu --print-format` is safe and
  informative *only with a literal `--print`* in the same invocation; this pass ran it
  once, verified `db.lck` absent immediately before and after, and would refuse it
  without the print flag. Pipelines hide rc (r6 §2 lesson re-applied: every rc quoted
  above is the unpiped `pacman` rc).
- 2026-10-14 (S7-3, post-pass observation at 18:26Z) — **concurrent lane landing,
  recorded not absorbed:** while this note was being written, the sibling gate lane wrote
  `tools/tsukuroi-census.sh` (mtime 15:24:40 -03; now 1186 ln, md5
  `821acc24c7a1ccb7591fd9b6e3d22aa4`, `git status` = ` M`, uncommitted) and a scribe lane
  created `plans/round-7-record-draft.md`. The census diff carries the round-6 baseline
  arms — fixture regexes expect `foreign=16(known=16 new=0 drift=0 gone=0) base=file(16)`
  / `base=r6(16)` plus fail-closed `new` / `drift` / `gone` / `base=absent` cases — but no
  baseline `.tsv` file exists in `corpus/knowledge/` yet, and no `PLANE update-safety`
  line appears in the revision read. §0's 4-plane census pin (`e9327046…`, 1032 ln) is
  therefore accurate **as of this note's measurement window only**; the sibling landing
  supersedes it for later readers, and neither sibling file is pinned here beyond this
  observation.

## Erratum (2026-10-19, fleet round 1) — D1: Bare -Sy is not a safe refresh route
Superseded (`corpus/knowledge/update-safety-v2.md:102,280`): “After an operator `-Sy` it becomes a real set decided by the mirror snapshot.”
Correction: use pacman-contrib's `checkupdates` for a safe installed-package update check, or a complete `pacman -Syu`; never advise bare `pacman -Sy`.
Source: S010 https://wiki.archlinux.org/title/System_maintenance § Avoid certain pacman commands: “never run `pacman -Sy`; instead, always use `pacman -Syu`.” S010 § Partial upgrades are unsupported: `checkupdates` safely checks installed-package updates without a system update.
[obs] Host `/var/log/pacman.log`, re-opened 2026-10-19: `grep -nE 'pacman -Sy ' /var/log/pacman.log` → line 1405 (`2026-10-11T12:54:13-0300`, `pacman -Sy --noconfirm fuse2`) and line 2287 (`2026-10-18T14:11:00-0300`, `pacman -Sy --noconfirm`). `grep -nE 'pacman -Syu|Running .pacman -Syu' /var/log/pacman.log` → line 1414 (`2026-10-11T16:13:19-0300`); the first gap is 3h19m06s, while no later full `-Syu` is recorded after line 2287.
S010 https://wiki.archlinux.org/title/System_maintenance § Avoid certain pacman commands; own-work S032 `/var/log/pacman.log` lines 1405, 1414, 2287.

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — pacman planner/package queries, sync database, package/log, and read-only systemd/journal probes on host `plazir27`, 2026-10-14; S010 https://wiki.archlinux.org/title/System_maintenance § Avoid certain pacman commands; S031 `tools/tsukuroi-census.sh`; S032 `/var/log/pacman.log` lines 1405, 1414, 2287 (re-opened 2026-10-19).
verified-at: 2026-10-14 (the v2 capture window recorded in this note; D1 log evidence re-opened 2026-10-19).
recheck: 90d; procedure: §9 source/recheck probe set; repeat read-only planner and package-class probes before a planned wave.

## R15-UPDATE-STATE (2026-10-20) — current-use supersession

Appended in round 15. The 2026-10-14 bytes above are preserved and remain
historical. The §6 composition “Composed today: `-Syu` now = **INERT** (0
candidates)” and the §7 rank 1 row “Do nothing now” (“`-Syu` would be INERT:
0 actions”) describe that capture only; they are not a current-use statement.

For current use on 2026-10-20 read
`corpus/knowledge/partial-upgrade-recheck-r15.md` / `.json` (schema
`tsukuroi-partial-upgrade-recheck-v1`), which binds the read-only snapshot
`.ufo/waves/round-15/build/host-snapshot.json` captured 2026-10-20T07:44:39Z
(SHA256 `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`).
It records `pacman -Qu` exit 0 with 413 pending rows against sync DBs born
2026-10-18T17:11:00Z, `libinput 1.32.0-1` installed after the logged
2026-10-20T04:25:16-0300 `pacman -S` command (upgrade line 04:25:17-0300), and
`mkinitcpio 41.1-1` installed with 42.2-1 pending. Decision: `BLOCKED_FOR_AGENT_PACKAGE_ACTION`.

No agent install, upgrade, downgrade or service action is authorized. The
pending partial-upgrade assessment is operator-only, any full `-Syu` remains
behind the news gate, the two `/new_root`-only hooks leave mkinitcpio-42
compatibility untested with no clearance, and no host repair is claimed.
