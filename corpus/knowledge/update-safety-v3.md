# Update-safety v3 — the AUR watch arm's live data joined: which foreign packages have updates pending today, risk-class first (TSUKUROI-S8-3)

source: live read-only probes, host `plazir27`, user `vgpnk` (non-root), single pass
2026-10-14 16:12:58–16:18:07 -03 (19:12:58–19:18:07Z); scratch `/tmp/w8-s83-tsukuroi/`
(files + md5 in §8). Verbs run: `tools/tsukuroi-census.sh` (live, read-only), `pacman
-Q|-Qq|-Qm|-Qme|-Qmdtq|-Qdtq|-Qi|-Qkk|-Qu|-Si|-Sl|-Slq`, `pacman -Sup --print-format` and
`pacman -Suu --print-format` (plan-only family — no transaction, no download, no db write),
`pacman-conf`, `stat`, `md5sum`, `sha256sum`, `bsdtar -tf` over `offline.db`, `diff`/`sort`,
`git -C` reads of the two `~/.cache/yay/` clones and of this repo, `systemctl --user` /
`journalctl --user` reads. No `-Sy` / `-Syu` (only the literal `--print` forms); nothing
installed, upgraded, removed or restarted; no AUR RPC; no network; no external site; no root;
no host file written outside the scratch dir.

**Read-only contract held** [observed: `git status --porcelain` empty at 19:13:03Z before the
battery and byte-identical after at 19:13:07Z / 19:14:56Z / 19:15:25Z; `/var/lib/pacman/db.lck`
absent at every check (19:13:03Z, 19:13:07Z, 19:13:50Z); the five sync `.db` files' birth and
content stamps are the ones every earlier pass read — no refresh, no write; `pacman.log` md5
`e452d910…`, 2109 ln, mtime 2026-10-13 16:37:59, unchanged all pass].

Tags: **[observed]** = measured in this window, command named · **[inference]** = drawn from
observations, stated as such · **[unknown]** = named gap with the probe that would settle it.

Predecessor: `corpus/knowledge/update-safety-v2.md` (S7-3; md5
`92803aea74ebeb1598fa4f450489e5d2`, 353 lines) — v3 is its **re-run with the watch arm's live
data joined**, not a rewrite. Every class, hold, path and hazard row v2 carries is re-measured
here; where this note reuses a v2 posting it cites it (§5, §6). The r2 note
(`update-safety-note.md` `5cc3067f…`, 478 ln) and the r6 register (`aur-risk-plane.md`
`1a584300…`, 341 ln) remain the class owners; this note owns only the join. v2's pass was
15:19–15:26 -03 the same calendar day, ~46 min before this one, so reproducing its readings is
expected, not independent confirmation (v2 §1's own caveat, re-applied).

## 0. What "the AUR watch arm" is — and the one question v3 answers

- **The arm.** `tools/tsukuroi-census.sh`'s **foreign watch arm** (round 7, lane S7-1; its
  verifier calls it "the AUR-arm", `aur-risk-plane-ver-s7.md:1,10`). It folds live
  `pacman -Qm` against an accepted baseline — default the embedded r6 snapshot (census
  `:238-253`), overridable via `TSUKUROI_FOREIGN_BASELINE` (census `:227-235`) — and prints
  `foreign=<n>(known/new/drift/gone) base=<src>` on the packages plane (census `:59-68`,
  `:414-470`). Fail-closed: a new/drifted/gone row or a missing baseline is DEGRADED, never a
  pass; the baseline can split the report, never lower a verdict.
- **The live data joined here** is my own live run of the landed revision at
  **2026-10-14T19:13:03Z** (§1). The revision is the round-7 landing, **committed** at HEAD
  `aa136d6` — same bytes as the round-7 SKILL append's pin (S7-4: `e2c4558a…`, 1472 ln),
  which was uncommitted at that append's write time; VER-S7 verified an **earlier,
  1186-line** revision (`821acc24…`) of the same file, so its pin and mine are different
  revisions by design (§8). Stable across this pass.
- **The question v3 answers**, per the assignment: *which foreign packages have updates
  pending TODAY, risk-class first*. "Pending today" is defined operationally as: some channel
  that can supply the package resolves, **today**, a version newer than the installed one —
  checked (a) against every configured repo, and (b) against the only locally retained
  AUR-side record, the `~/.cache/yay/` clone tips. Upstream AUR state itself is out of
  province (no network, no AUR RPC), and is tagged **[unknown]** wherever it would matter.
- **Why v3 exists.** v2's risk-ordered table could only cite the r6 register's classes; the
  arm landed the same hour and its live fold was joined into no update-safety artifact. v3 is
  that join, plus the official-space pending rows (§4) recomputed the same minute.

## 1. The arm's live reading, verbatim (join source) [observed]

My run, `bash tools/tsukuroi-census.sh`, 2026-10-14T19:13:03Z, rc=1 — packages line and
rollup line verbatim:

```
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16); pins=none; holds=pacman glibc; db.lck=absent)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

Reading the foreign field for the join:

- `foreign=16` — sixteen foreign (non-repo) packages installed, unchanged.
- `known=16 new=0 drift=0 gone=0` — **every one of the 16 equals its accepted baseline row
  (name and version); nothing new arrived, nothing moved version, nothing disappeared.**
- `base=r6(16)` — the fold ran against the embedded r6 snapshot, not an external file.
- The same field printed by a sibling lane's live run 2.5 min earlier (SCR-S8's
  `gate-run.out`, 19:10:28Z, read-only): `foreign=16(known=16 new=0 drift=0 gone=0)
  base=r6(16)` — the arm's reading is stable across the round-8 opening window [observed,
  quoted from that lane's scratch; same host and revision, so corroboration of stability only,
  not an independent method].

The arm is the only executable watching this set; its fold is the join source for §3.

## 2. The 16, re-derived without the arm [observed]

Three arm-independent reproductions, so the §3 table does not rest on the gate:

| method | my command | my result |
|---|---|---|
| pacman's own foreign list | `pacman -Qm` rc=0 | **16 rows**, the 16 names in §3, versions as in §3 |
| baseline identity | extract census `:238-253` to `bl-extract.txt`, `diff` vs live `pacman -Qm` | **diff empty**; and the two files are **byte-identical** — both md5 `bde5487579e57c044768112d17e54ab4` (the same md5 VER-S7 extracted from the 1186-line revision) |
| no channel resolves them | loop over the 16: `pacman -Si "$p"` | **rc=1 ×16** — no configured repo (`core extra multilib omarchy`) can see any of them |
| class split at version level | `bsdtar -tf offline.db \| grep '^(elephant\|omarchy-walker)'` = 28 lines (14 `<pkg>-<ver>/` + 14 `desc`); the 2 AUR-local names | **14 in `offline.db` / 2 not** — reproduces the r6 register's `offline-exile` (14) vs `aur-local` (2) split at version level (VER-S7 §3's method, re-run today) |
| context | `pacman -Qq` 1188 · `pacman -Qmdtq` rc=1 empty · `pacman -Qme` rc=0 = 3 (`android-apktool-bin`, `obsidian-cli-inspector`, `omarchy-walker`) · `pacman -Qdtq` rc=0 = 3 orphans (`electron39`, `mbedtls`, `webp-pixbuf-loader`) | all equal v2 §1 rows 8/9 |

Per-package cells re-measured today: `Validated By` = `None` for the 2 `aur-local`
(`android-apktool-bin`, `obsidian-cli-inspector`), `SHA-256 Sum  Signature` for the other 14;
`pacman -Qkk android-apktool-bin obsidian-cli-inspector omarchy-walker elephant` → rc=0,
`0 altered` on each; installed size sum of the 16 = **357.18 MiB** (v2's figure reproduced);
`omarchy-walker` 1.0.0-2 is a 0 B meta package whose `Depends On` is exactly `walker` + the 13
`elephant*` packages, all unversioned.

## 3. Risk-class-first table — the 16 foreign packages, updates pending TODAY

Ordering: **risk class first**, per the assignment; within the class, v2's risk rank
(`update-safety-v2.md:244-260`) and then name order. Class definitions are the r6 register's
(`aur-risk-plane.md:212-221`), re-derived in §2. "Path" = what an update could even travel on;
"pending TODAY" = per the §0 definition.

| # | package (version today) | class | path today | **updates pending TODAY** |
|---:|---|---|---|---|
| 1 | `android-apktool-bin` 3.0.3-1 | `aur-local` | yay → AUR (external; absent from every repo) | **no measurable update pending** — last-fetched AUR tip == installed; AUR delta since 2026-10-13 **[unknown]** |
| 2 | `obsidian-cli-inspector` 1.0.3-1 | `aur-local` | yay → AUR | **no measurable update pending** — same; AUR delta since 2026-10-13 **[unknown]** |
| 3 | `elephant` 2.21.0-1 | `offline-exile` | none | **n/a — no route** (not updateable at all) |
| 4 | `elephant-bluetooth` 2.21.0-1 | `offline-exile` | none | n/a — no route |
| 5 | `elephant-calc` 2.21.0-1 | `offline-exile` | none | n/a — no route |
| 6 | `elephant-clipboard` 2.21.0-1 | `offline-exile` | none | n/a — no route |
| 7 | `elephant-desktopapplications` 2.21.0-1 | `offline-exile` | none | n/a — no route |
| 8 | `elephant-files` 2.21.0-1 | `offline-exile` | none | n/a — no route |
| 9 | `elephant-menus` 2.21.0-1 | `offline-exile` | none | n/a — no route |
| 10 | `elephant-providerlist` 2.21.0-1 | `offline-exile` | none | n/a — no route |
| 11 | `elephant-runner` 2.21.0-1 | `offline-exile` | none | n/a — no route |
| 12 | `elephant-symbols` 2.21.0-1 | `offline-exile` | none | n/a — no route |
| 13 | `elephant-todo` 2.21.0-1 | `offline-exile` | none | n/a — no route |
| 14 | `elephant-unicode` 2.21.0-1 | `offline-exile` | none | n/a — no route |
| 15 | `elephant-websearch` 2.21.0-1 | `offline-exile` | none | n/a — no route |
| 16 | `omarchy-walker` 1.0.0-2 | `offline-exile` | none | **n/a — no route**; carries the `walker` provider edge (R10) |

Per-row evidence, shared by class (all [observed], this pass):

- **Rows 1–2 (`aur-local`)** — `pacman -Si` rc=1 both; `Validated By: None` both; last-fetched
  AUR tip measured in the retained build clones: `git -C ~/.cache/yay/android-apktool-bin`
  HEAD = `master` = `origin/master` = `92ce7df1217deb19fab6e899a3772459f4198bdc`
  (2026-09-28T17:22:27+03:00, "update to v3.0.3"), `PKGBUILD` `pkgver=3.0.3` `pkgrel=1`;
  `obsidian-cli-inspector` HEAD = `ce7b42588bd4f64af509e8b4a336a149ca93f3ca`
  (2026-03-08T07:56:23Z, "Update to …v1.0.3"), `pkgver=1.0.3` `pkgrel=1`. Both clones carry
  **no `FETCH_HEAD`** — no fetch since the clone; the tip equals the installed version, so no
  pending update was recorded at the last AUR contact (the operator's 2026-10-13 installs,
  `pacman.log:2090,2097`). Built artifacts still match the r6 receipt:
  `sha256 e83409b290bae6be118841b17a7168bbc183ec85586e9f6e71a4af1ba84edbd2` /
  `a6ec77fab6e3d3a7a5b50a959422f6dab9b42356c426e053ab8649891a431959`. Remotes unchanged
  (`https://aur.archlinux.org/<pkg>.git`).
- **Rows 3–16 (`offline-exile`)** — `pacman -Si` rc=1 ×14; `offline.db` (birth
  2026-10-03 17:41:33.994891750, 304 318 B, md5 `c4b27c3850df414ee956db968c9d5729`, new pin
  this pass) carries `<name>-<version>/` + `desc` for each of the 14; the cached channel-A
  archives remain: `/var/cache/pacman/pkg/` holds 26 `^elephant` entries (13 pkgs × `.zst` +
  `.sig`) and 2 `^omarchy-walker` entries, all 2.21.0-1 / 1.0.0-2. `Validated By: SHA-256 Sum
  Signature` ×14.
- **Row 16's living edge** — `walker` 2.17.0-1 (`[omarchy]`, installed; `Required By:
  omarchy-walker`) crossed the unversioned dependency once already (2.16.2-1 → 2.17.0-1 on
  2026-10-11, R10); the consumer is up right now: `elephant.service` active,
  `app-walker@autostart.service` active, `journalctl --user -b | grep -ic elephant` = 132,
  0 error/fail/panic/warn matches (shape identical to r6 §5 / v2 §4).

**The table's answer, in one sentence.** *Today no foreign package has a measurable update
pending: relative to the accepted baseline nothing has moved (arm: `known=16 new=0 drift=0
gone=0`), no configured channel resolves any of the 16, the two `aur-local` rows show no
update recorded at their last AUR contact, and the fourteen `offline-exile` rows have no
update route at all — for them "pending" is not applicable, only preservation.*

Two consequences carried from the register, re-verified: the update path for the `aur-local`
pair is **review-on-update** (diff the PKGBUILD against the retained clone, confirm the sha256
pins moved coherently with `pkgver`, then build — never blind `yay -Syu`, never "fix" the
missing signature by relaxing policy); the only safe operations for the 14 are preservation and
observation (`aur-risk-plane.md:212-221`, `:287-312`).

Closed class today: **no `unknown-provenance` rows** (the class is a rule run only when a new
foreign arrival appears; today `new=0`), and the one **`out-of-reach`** question (`walker` /
elephant ABI linkage) stays routed to kaidoku/revenger, with the tsukuroi-legal substitute
watch (`journalctl --user -b` elephant lines, above) intact.

## 4. The official space's pending rows, same minute [observed]

The other half of "updates pending today" — the space the arm does not touch:

| probe | result | reading |
|---|---|---|
| `pacman -Qu` (unpiped) | rc=1, **0 lines** | no installed repo package is behind its effective repo entry |
| `pacman -Sup --print-format '%r/%n %v'` | rc=0, **0 lines** | same, second probe |
| version join (`pacman -Q` 1188 × `pacman -Sl` 15 651 names, repo order core>extra>multilib>omarchy first-wins) | common 1172 · **equal 1171 · behind 0 · ahead 1** | 0 behind (third probe); the 1 ahead = `1password-beta` (below) |
| `pacman -Suu --print-format '%r/%n %v'` | rc=0, **1 action**: `omarchy/1password-beta 8.12.42_32.BETA-1` | the downgrade trap, still measured |
| repo collisions with differing versions | **12** names present in >1 repo; **12 differ** | split by direction, below |

- **The ahead row / downgrade trap (U5).** Installed `1password-beta`
  `8.12.42_32.BETA-32` > omarchy's `8.12.42_32.BETA-1`. Plain `-Syu` ignores it; `-Suu`
  would "upgrade" to an older beta — the single action a `-Suu` would perform today.
  `db.lck` absent immediately before and after the print-only invocation.
- **The hidden channel row.** `linux-firmware-cirrus`: installed `20260810-2` (core's entry),
  omarchy holds `20260810-3` — **newer, and invisible to `-Qu`** because core wins the repo
  order. `pacman -Sl omarchy` prints `linux-firmware-cirrus 20260810-3 [installed:
  20260810-2]`: the shadowing is visible in the channel listing, never in `-Qu`. **This is
  the one installed name with a newer version available on the host today.**
- **Sharpening v2's shadow count.** v2 (`:88-92`) counted "5 shadowed-newer names". v3's
  join splits that 5 by install state: **1 installed** (`linux-firmware-cirrus`, above) and
  **4 not installed** (`ghostty`, `ghostty-nautilus`, `ghostty-shell-integration`,
  `ghostty-terminfo`: extra 1.3.1-2 < omarchy 1.3.1-3). The other 7 differing collisions run
  the other way (first repo newer: `asusctl`, `gpu-screen-recorder`, `intel-lpmd`, `opencode`,
  `pinta`, `rog-control-center`, `umu-launcher`) and hide nothing. Both readings are true;
  the installed-state split is the one relevant to "pending today".
- **No update check ran today.** The only in-province evidence of update-check activity:
  `pacman.log` mtime 2026-10-13 16:37:59 and yay's caches (`~/.cache/yay/completion.cache`
  2026-10-13 13:52:58; `vcs.json` `{}`, 2026-10-13 16:21:20; `~/.config/yay/config.json`
  absent). Nothing on the host produced a pending-update signal today except the probes in
  this pass [observed]; the next refresh/check is operator-side (U2).
- **Snapshot freshness for the whole table.** Sync-db births 2026-10-11 12:54:13.542054496
  -03 ×4; content stamps core/extra/multilib 2026-09-08 15:23:45–47 = **36 d 0 h 49 m** old at
  16:13:03 -03; omarchy 2026-10-11 10:16:17; sizes 129 469 / 8 900 506 / 84 692 / 48 989 B;
  `.db.sig` count **0**. Every "0 pending" above is *against these dbs* — "empty ≠ up to
  date" stays the standing caveat (v2 §2).

## 5. Risk-ordered operations table (recommendation only — nothing here was run)

v2 §7's table, re-measured today and joined with §3/§4. Ordered by risk: lowest first. This
lane detects and recommends; the operator acts (`PROVINCE.md:16-17`). "Reach" = what the
operation can actually touch; foreign reach per §3.

| rank | operation / item | class | reach | measured risk on this host (today) | recommendation |
|---:|---|---|---|---|---|
| 1 | Do nothing now | official | — | `-Syu` would be INERT: 0 candidates by three probes; the only effect is the refresh mutation itself, which invalidates the emptiness | No update action is owed today; the gate is the **next refresh**, not a run |
| 2 | Plain `-Syu` after an operator refresh (the wave) | official | core/extra/multilib/omarchy | post-refresh set UNKNOWN-UPSTREAM; 36 d of drift puts kernel/libc/driver classes in scope; wave cost before: 81 s / 505 actions | If currency is wanted: planned window + prep (a)–(d) below, then re-run `-Qu`/`-Sup` **before** the upgrade |
| 3 | `[omarchy]`-sourced rows inside that wave (**26 installed** today) | official, soft-trust | same wave | `SigLevel = PackageOptional PackageTrustAll DatabaseOptional DatabaseTrustAll`; 0 `.db.sig`; 1 installed shadow-hidden candidate (`linux-firmware-cirrus`) + `1password-beta` ahead-of-repo | Decide the channel policy once, in writing; audit via `pacman -Sl omarchy`, not only `-Qu` |
| 4 | AUR-local updates/rebuilds (2 rows, §3 rows 1–2) | `aur-local` | yay only; external; never `-Qu` | no signature ever (`Validated By: None`); `LocalFileSigLevel = PackageOptional PackageTrustedOnly`; last-fetched tips == installed; **no pending update recorded**; AUR delta [unknown] | Review-on-update only: diff PKGBUILD vs the retained clone, confirm sha256 pins moved coherently with `pkgver`, then build |
| 5 | The 14 offline-exile packages (§3 rows 3–16) | `offline-exile` | no path | channel dead (R4); one unversioned `walker` edge already crossed (R10); repair-by-reinstall impossible (R1) | **Preserve, don't update:** the preservation set is `offline.db` (md5 `c4b27c38…`, 304 318 B) + 28 cache entries (14 `.zst` + 14 `.sig`) + the 2 clone trees; copy before any cache prune |
| 6 | Repair-by-reinstall of any of the 16 (or sourcing them somewhere new) | all foreign | none configured | `pacman -Si` rc=1 ×16 — no repo can supply them; improvising a source changes provenance silently | Do not improvise; if a re-source is ever wanted, run the `unknown-provenance` probe order first and let the operator record the decision |
| 7 | `-Suu`, `-Syyu`, any downgrade/force verb | official | all installed | **measured today**: `-Suu --print` = 1 action, the `1password-beta` BETA-32 → BETA-1 downgrade; `-Syyu` rejected by rule (re-downloads 36-day-old dbs) | DO-NOT (verb-level); plain `-Syu` only |
| 8 | Orphan removal (`electron39`, `mbedtls`, `webp-pixbuf-loader`) | official | 3 packages | removables, not upgrade blockers; none foreign | Separate, deliberate decision — keep orphans out of any automatic sweep during a wave window |

Prep (a)–(d) before any wave (v2 `:254`, r2 `:364-373`, unchanged): rollback decision (U1),
dkms/kernel verification plan (U3), schedule under measured load (U8), trust-channel decision
(U4).

## 6. Hazard inventory refresh (U-rows)

- **No rollback net — U1, leading exposure.** `snapper list-configs` → header + rule only
  (2 lines, rc=0, **0 configs**); `limine-snapper-sync` system unit enabled+inactive (v2 §6,
  unchanged). Any wave is snapshot-less.
- **Upstream delta — U2, the real gate.** Dbs refreshed 2026-10-11; content 36 d 0 h old;
  `checkupdates`/`pacman-contrib` absent (installing is out of province, SKILL.md:415). The
  resolving event is operator-side. Today's addition: **no check ran at all** (§4).
- **Kernel/DKMS coupling — U3.** `dkms status` still two rows: stale
  `nvidia/610.57.04, 7.1.4-arch1-1 … (Built modules are missing in the kernel modules
  folder)` beside the current `7.2.3-arch1-3` (v2 §6, identical text). No reboot pending
  today; a kernel-raising wave rebuilds in-transaction via `90-mkinitcpio-install.hook`.
- **Trust surfaces — U4.** `[omarchy]` TrustAll (string measured §4); `LocalFileSigLevel =
  PackageOptional PackageTrustedOnly`; 0 `.db.sig`; `SigLevel = PackageRequired
  PackageTrustedOnly DatabaseOptional DatabaseTrustedOnly`. Still a written accept-or-re-scope
  decision before a wave.
- **Downgrade trap — U5.** Measured again: 1 action (§4).
- **`/boot` privilege gate — U6.** `ls /boot` rc=2 (Permission denied; measured unpiped this
  time) — BLOCKED stands; operator root pre-verify only.
- **`walker-restart.hook` — U7.** Carried: user-owned script exec'd by root in transactions —
  reported to kagi/operator, not absorbed.
- **Workloads — U8.** Re-measure at the decision moment; this pass ran mid-wave with 32
  sibling lanes active (the whole read-only battery, live census included, took 4.6 s wall:
  16:13:03.07 → 16:13:07.70 -03).
- **New named observation this pass — package-level drift on two official packages.** The
  census's bounded 8-sample carries `drift=2[1password-beta,1password-cli]`; `pacman -Qkk`
  on the pair (unpiped **rc=1**, 16:17:16 -03) localizes it to a GID/permissions mismatch
  each: `/opt/1Password/1Password-BrowserSupport` (GID + Permissions mismatch) and
  `/usr/bin/op` (GID + Permissions mismatch) — 1 altered file per package
  (`1password-beta: 122 total files, 1 altered`; `1password-cli: 7 total files, 1 altered`).
  Reported as measured; the cause is not adjudicated here (1Password's own updater/group
  state is out of this lane's probes). An earlier piped read of this probe printed rc=0 —
  that was the pipeline's `tail` rc, the exact trap the house notes warn about; the
  unpiped value above supersedes it.
- **Carried standing rows:** `HoldPkg = pacman glibc` (removal protection, not a version
  hold); IgnorePkg/IgnoreGroup/NoUpgrade/NoExtract all empty; `pacman -Dk` clean (v2; not
  re-run); `db.lck` absent; `/sys/class/power_supply/` empty (UPS [unknown]); `walker
  -restart.hook`; `1password-beta` provenance; root `-Qkk` delta; coredump-storm ownership
  (journal workstream).

## 7. Observation / inference / unknown

- **Observed (this pass).** The §1 live reading and the §2 reproductions; `-Qu` rc=1 empty;
  `-Sup` 0; join 1171/0/1; 12 collisions (5 later-newer / 7 later-older; 1 installed
  hidden candidate); `-Suu --print` 1 action; `db.lck` absent at all checks; `-Qm` 16 +
  byte-identity with the embedded baseline; `-Si` rc=1 ×16; `Validated By` 2 None / 14
  signed; `-Qkk` foreign sample clean; clone tips/refs/no-FETCH_HEAD; artifact sha256s;
  offline.db pin + 28 listing lines; cache counts; log md5/lines/mtime; db births/stamps/
  sizes; `.db.sig` 0; pacman-conf pins; snapper 2-line header; dkms two rows; `/boot` rc=2;
  systemd user running, 0 failed; elephant/walker services active, journal 132/0.
- **Inference (not measured).** The 14 offline-exile channel was `offline.db` (r6's evidence
  chain, not re-litigated); `HoldPkg` is removal-protection only; the GID/permission drift on
  the 1Password pair is likely self-inflicted by its updater (not adjudicated); a
  kernel-raising wave would rebuild the current dkms row but not the stale
  7.1.4 row; a soname bump under the foreign set would break it silently (unversioned edges).
- **Unknown (open).** AUR upstream delta for the 2 `aur-local` (and whether any of the 14
  exists in the AUR at all) — needs network/AUR RPC, out of province; whether the arm's
  revision is touched by lane S8-1 after my pin (selftest-only edits are expected; the *live*
  reading is the pin); whether the update-safety 5th plane lands in any round (today's live
  rollup is 4 planes; the round-8 plan does not claim it); the counter-lifecycle and
  OOM-plane H1–H3 questions (S8-1/S8-2's round, not this note's); contents of privilege-gated
  paths (`/boot`, 3 root-only `download-*` dirs); UPS existence; `walker`↔elephant ABI
  (routed out); `1password-beta` provenance; coredump-storm ownership.

## 8. Sources, pins, scratch, recheck

**Spot-checks (the three this seat was asked for, verbatim results):**

1. **The arm's fold reproduces without the arm.** `pacman -Qm` vs the census's embedded
   baseline block (extracted `:238-253`) → `diff` **empty**, and the two files are
   **byte-identical**: both md5 `bde5487579e57c044768112d17e54ab4` (16 rows; the same md5
   VER-S7 extracted from the earlier revision — the block did not move when the file grew).
2. **No channel resolves any foreign package.** Per-package loop, `pacman -Si` → **rc=1 ×16**
   (§2 table) — and the version-level class split re-derives as 14 in `offline.db` / 2 not.
3. **The only local pending-update signal is negative.** Both clone tips (HEAD = master =
   origin/master; `pkgver`/`pkgrel` in PKGBUILD) **equal the installed versions**, and no
   `FETCH_HEAD` exists in either clone — no update pending as of the last AUR contact
   (2026-10-13). Fourth check, same battery: `-Suu --print` = exactly 1 action with `db.lck`
   absent before/after.

- **In-lane pins (this pass, `md5sum` + `wc -l`, 19:13:03Z):** `tools/tsukuroi-census.sh`
  `e2c4558a3ae4ddd2eca67e8f4d64281c` / 1472 / 73 919 B (mtime 2026-10-14 15:33:21 -03; **the
  round-7 landing, committed** at HEAD `aa136d6` — same bytes as the round-7 SKILL append's
  pin, which was uncommitted then; VER-S7's own pin `821acc24…` / 1186 ln is an **earlier
  revision** of the same file, superseded before the commit) ·
  `SKILL.md` `b2b0f6a78b9d25e833af6bd54ec83227` / 983 · `LOG.md` `e0d92542…` / 170 ·
  `SCORECARD.md` `021bc898…` / 19 · `corpus/README.md` `98bd00668e84f18cf6781718c4d09ea0` /
  20 · `update-safety-v2.md` `92803aea…` / 353 · `aur-risk-plane.md` `1a584300…` / 341 ·
  `aur-risk-plane-ver-s7.md` `4608743d…` / 184 · `oom-event-plane.md` `7e99d712…` / 433 ·
  `update-safety-note.md` `5cc3067f…` / 478 · `plans/round-8.plan.md` `0bef822d…` / 216
  (the round's *main-lane* plan — the OOM watch; **this lane's frame is the round-8 dispatch,
  not that plan**, and nothing in it is quoted as landed here). Counts above are captures —
  re-run, never quote; an unterminated final line means Read counts one more than `wc -l`.
- **New/second pins this pass:** `offline.db` md5 `c4b27c3850df414ee956db968c9d5729`
  (304 318 B); embedded-baseline extract = live `-Qm` = `bde5487579…`; clone HEADs
  `92ce7df1…` / `ce7b4258…`; artifacts `e83409b2…` / `a6ec77fa…`; `pacman.log` `e452d910…`
  2109 ln 157 286 B.
- **Scratch (`/tmp/w8-s83-tsukuroi/`, ephemeral):** `battery1.out`
  `2516d8c08b5b8b8593b244e25034b26c` (pins, live census, pacman probes, foreign cells) ·
  `battery2.out` `acdaac5b3c0a73a3f777786372e9848c` (version join + shadowing join, boot rc,
  preservation pins) · `battery3.out` `81f6bbd1de4ef8ffa248a7f2445ab58a` (baseline extract
  attempt + `-Qkk` sample + clone remotes + status) · `battery4.out` `0fdb51eb…` (omarchy
  installed rows, drift localization, yay config, snapper, walker) · `battery4b.out`
  `7402eaa7…` (offline.db absence of the 2, omarchy-walker deps) · `battery5.out`
  `59dc4db3a486c0842b56af8d67e251a8` (unpiped `-Qkk` rc for the drift pair) ·
  `bl-extract.txt` = `qm-live.txt` = `bde5487579e57c044768112d17e54ab4`.
- **Recheck (compact):** `bash tools/tsukuroi-census.sh` (expect the same `foreign=` field
  unless the set moved) · `pacman -Qm | wc -l` · `pacman -Qu; echo rc=$?` ·
  `pacman -Sup --print-format '%r/%n %v' | wc -l` · `pacman -Suu --print-format '%r/%n %v'`
  (exactly the 1password-beta row) · `for p in $(pacman -Qm | cut -d' ' -f1); do pacman -Si
  "$p" >/dev/null 2>&1; echo "$p rc=$?"; done` · `pacman -Sl omarchy | grep '\[installed'` ·
  `pacman -Qkk 1password-beta 1password-cli; echo rc=$?` (expect rc=1 with the 2 summary
  lines) ·
  `git -C ~/.cache/yay/android-apktool-bin log -1 --format='%H %cI'`;
  `git -C ~/.cache/yay/obsidian-cli-inspector log -1 --format='%H %cI'` ·
  `md5sum /var/lib/pacman/sync/offline.db` · `md5sum /var/log/pacman.log` ·
  `snapper list-configs` · `dkms status`.

## 9. Boundary notes and errata (append-only)

- 2026-10-14 (S8-3) — **write scope.** This lane wrote only this file (assignment). It wrote
  nothing in any sibling repo, ran no mutating verb, and held the scratch to
  `/tmp/w8-s83-tsukuroi/`. Owed by others, recorded not absorbed: (i) the `LOG.md` entry for
  this artifact (`AGENTS.md:3`); (ii) the v2 note's own owed errata pointer (its §10 item (i)
  is still owed — the r2 note stands unchanged at `5cc3067f…`); (iii) the census 5th
  (update-safety) plane — **still unlanded today** (live rollup prints 4 planes; the round-8
  main plan adds the OOM plane, not this one), carried since `plans/round-7.plan.md` claim
  (a) and VER-S7 D4; (iv) `corpus/README.md` coverage rows (rounds 4–8 still absent at
  `98bd0066…`).
- 2026-10-14 (S8-3) — **concurrency recorded, not absorbed.** At this pass the round-8 wave
  was in flight: a sibling scribe lane (`/tmp/w8-scr-s8-tsukuroi/`) had already run the gate
  at 19:10:28Z and pinned the same revision, and lanes S8-1/S8-2/S8-4 (OOM arm verification,
  kill-event deep note, SKILL round-8) were active. The census revision I pinned
  (`e2c4558a…`, 1472 ln, committed `aa136d6`) may gain selftest-only edits later in the round;
  the *live reading* in §1 is this pass's, and later readers must re-run it.
- 2026-10-14 (S8-3) — **relation to v2, stated so nothing reads as a contradiction.** v2's
  "5 shadowed-newer names" is sharpened here to "1 installed + 4 not installed" (§4) — a
  sharper join, not a correction; v2's phrasing remains true as written. v2's §7 ranks are
  reused for the class-first ordering in §3; v2's `-Suu` measured row and U-rows all
  reproduce today. Where any v2 value and this pass's value conflicted, none did.
- 2026-10-14 (S8-3) — **the join's own limit, carried.** The arm's fold is *relative to its
  accepted baseline*: a package that was stale when the baseline was written and stayed stale
  reads `known`, not `pending`. Today's independent negations of "pending" are `-Si` rc=1 ×16
  (no repo) and the clone-tip equality (no AUR record), not the fold alone. Upstream AUR state
  remains read-only-unmeasurable by discipline and is never a pass.
- 2026-10-14 (S8-3) — **post-write observation at 16:18Z, recorded not absorbed.** After this
  note's first write (16:16:53 -03), `git status --porcelain` in the repo shows three
  untracked files: this note, `plans/round-8-record-draft.md` (scribe lane SCR-S8) and
  `plans/round-9.plan.md` (draft lane PREP-S9). **Only this note is this lane's write**; the
  tree was clean at 19:14:56Z immediately before it. Same convention as VER-S7's E-1: a later
  reader must not read concurrent lane movement as a mutation by this seat.
- 2026-10-14 (S8-3) — **two self-audit corrections, stated not smoothed.** (i) §6's drift
  localization first printed `rc=0` — that was the pipeline's `tail` rc; the unpiped
  `pacman -Qkk 1password-beta 1password-cli` rc is **1** (`battery5.out`), and the §6 text now
  carries the unpiped value. (ii) An earlier draft of §0/§8 wrote "identical bytes to VER-S7's
  uncommitted pin" — **wrong**: VER-S7 pinned the 1186-line revision `821acc24…`, superseded
  before the commit; the committed `e2c4558a…` / 1472 ln matches the round-7 **SKILL append's**
  pin instead. Both are corrected in place with the correction named here (the note is not
  append-only in its body — this file is new this round — but the corrections are recorded,
  never silent).

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — read-only pacman package/planner queries, sync-db and pacman-log reads, and census run on host `plazir27`, 2026-10-14; S031 `tools/tsukuroi-census.sh`; S032 `/var/log/pacman.log`.
verified-at: 2026-10-14 (the v3 measurement window recorded in this note).
recheck: 90d; procedure: §8 source/pin and probe ledger; repeat the package/planner join without a transaction.

## R15-UPDATE-STATE (2026-10-20) — current-use supersession

Appended in round 15. The 2026-10-14 bytes above are preserved and remain
historical. The §7 rank 1 row “Do nothing now” (“`-Syu` would be INERT: 0
candidates by three probes”) describes that capture only; it is not a
current-use statement.

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

## R16-RANK-SECTION — citation-only erratum

Appended in round 16. Every byte above, including the R15-UPDATE-STATE
notice, is preserved. That notice's sentence "The §7 rank 1 row "Do nothing
now"" cites the wrong section: in this v3 file the risk-ordered operations
table is §5 ("## 5. Risk-ordered operations table (recommendation only —
nothing here was run)"), whose row `| 1 | Do nothing now |` reads "`-Syu`
would be INERT: 0 candidates by three probes". §7 was the v2 table location
this file re-measured. The quoted "now"/"would be" wording is the
2026-10-14 capture, not a fresh observation. The stable citation is §5
rank 1, not §7.

This erratum supersedes the citation only. The quoted row content and the
R15-UPDATE-STATE current-use supersession routing readers to
`corpus/knowledge/partial-upgrade-recheck-r15.md` / `.json` stand
unchanged. This note makes no fresh host-health observation and authorizes
no package or service action.

No agent install, upgrade, downgrade or service action is authorized.

## R17-FRESHNESS — dated host re-verification (2026-10-20)

Historical captures stay historical: every 2026-10-14 byte above is unchanged and still dated. The bullets below mark only current-use statements that the 2026-10-20 09:15:30 full `-Syu` and the host activity after it superseded. [obs] values come only from `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt` and `.ufo/waves/round-17/l1-capture/fresh-capture.txt`; this seat ran no pacman, so no pending count is re-measured. Nothing here authorizes package, service or boot action.

- §5 row 1: "`-Syu` would be INERT: 0 candidates by three probes" → [obs] full -Syu executed 2026-10-20 09:15:30-0300; the pending set after it is not re-measured (this seat ran no pacman). Capture: .ufo/waves/round-17/l1-capture/boot-chain-capture.txt:59
- §5 row 1: "No update action is owed today" → [obs] the refresh gate was crossed by the full -Syu at 2026-10-20 09:15:30-0300; no current "owed" statement holds. Capture: .ufo/waves/round-17/l1-capture/boot-chain-capture.txt:59
- §5 row 2: "Plain `-Syu` after an operator refresh (the wave)" → [obs] executed: the full -Syu this row planned ran 2026-10-20 09:15:30-0300; its pre-upgrade wave-cost and pending premise are moot. Capture: .ufo/waves/round-17/l1-capture/boot-chain-capture.txt:59
- §5 row 2: "If currency is wanted: planned window" → [obs] the full system upgrade it prescribed started 2026-10-20 09:15:31-0300, before any re-run of -Qu or -Sup. Capture: .ufo/waves/round-17/l1-capture/fresh-capture.txt:8
- §6 U2: "resolving event is operator-side." → [obs] the operator-side sync ran 2026-10-20 09:15:30-0300. Capture: .ufo/waves/round-17/l1-capture/fresh-capture.txt:7
- §6 U2: "Dbs refreshed 2026-10-11; content 36 d 0 h old" → [obs] omarchy sync db mtime is now 2026-10-20 09:09:26 -0300; the content-age figure is not re-measured. Capture: .ufo/waves/round-17/l1-capture/fresh-capture.txt:13
- §6 U1: "(2 lines, rc=0, **0 configs**)" → [obs] snapper list-configs now lists two configs: home (/home) and root (/). Capture: .ufo/waves/round-17/l1-capture/fresh-capture.txt:45
- §6 U1: "Any wave is snapshot-less." → [obs] root config snapshot #2 pre-aur-elephant-2.22.1 exists (2026-10-20 09:29:19 -0300). Capture: .ufo/waves/round-17/l1-capture/boot-chain-capture.txt:167
- §6 U1: "`limine-snapper-sync` system unit enabled+inactive" → [obs] systemctl is-enabled reports limine-snapper-sync.service as enabled; its active state is not re-measured. Capture: .ufo/waves/round-17/l1-capture/fresh-capture.txt:47
- §6 U3: "`dkms status` still two rows" → [obs] dkms status now lists nvidia/615.78.08 installed for 7.2.11-arch1-1; no 610.57.04 or 7.1.4 row appears. Capture: .ufo/waves/round-17/l1-capture/fresh-capture.txt:37
- §6 U3: "No reboot pending" → [obs] current boot (journal boot 0) started 2026-10-20 09:57:09 -03. Capture: .ufo/waves/round-17/l1-capture/boot-chain-capture.txt:10
- §3 row 3: "| 3 | `elephant` 2.21.0-1 |" → [obs] elephant 2.22.1-1 was installed by pacman -U at 2026-10-20 09:31:03-0300 from the yay cache; the other rows are not re-measured. Capture: .ufo/waves/round-17/l1-capture/boot-chain-capture.txt:63
- §3 conclusion: "Today no foreign package has a measurable update" → [obs] one foreign row moved: elephant core is 2.22.1-1 since 2026-10-20 09:31:03-0300; whether any other foreign package now has a pending update is not measured. Capture: .ufo/waves/round-17/l1-capture/boot-chain-capture.txt:63
- §5 row 8: "Orphan removal (`electron39`, `mbedtls`, `webp-pixbuf-loader`)" → [obs] electron39 and mbedtls were removed by pacman -Rns at 2026-10-20 08:14:12-0300, so this row's orphan set is no longer current. Capture: .ufo/waves/round-17/l1-capture/boot-chain-capture.txt:57


## R18-FRESHNESS — sibling current-use restatements (2026-10-20)

Sources S060, S051 and S052. This appended correction supersedes the current-use readings listed below and every repeated current-use restatement of the same premise in this file. Historical measurements remain intact. No package, service, rebuild, boot or rollback action is authorized.

- R18-FRESH-SUPPLEMENT-17: prior locus `It records `pacman -Qu` exit 0 with 413 pending rows against sync DBs born`. Now: the413 pending count remains a dated R15 snapshot. S060 contains no pending-query result, so neither413 norzero is verified as a current pending count by this capture [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:1-99, .ufo/waves/round-18/l1-capture/capture-r18.sh:1-29]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:65.

- R18-FRESH-SUPPLEMENT-18: prior locus ``mkinitcpio 41.1-1` installed with 42.2-1 pending. Decision: `BLOCKED_FOR_AGENT_PACKAGE_ACTION`.`. Now: local-db directory mkinitcpio-42.2-1 is observed; the41.1-installed/42.2-pending current-use premise is superseded. Current pending row, if any, is unmeasured; the R17 image/symlink analysis governs compatibility, not a new upgrade clearance [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:1-99, .ufo/waves/round-18/l1-capture/capture-r18.sh:1-29]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:34.

- R18-FRESH-SUPPLEMENT-26: prior locus ``checkupdates`/`pacman-contrib` absent (installing is out of province, SKILL.md:415). The`. Now: S060 lists pacman-contrib-1.13.1-1 in local metadata and resolves /usr/bin/paccache; old package/paccache-absence guidance is not current. This capture does not query or resolve checkupdates, so its availability and any use elsewhere remain unknown; no installation is advised [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:82-86]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:36.

- R18-FRESH-SUPPLEMENT-27: prior locus `| 5 | The 14 offline-exile packages (§3 rows 3–16) | `offline-exile` | no path | channel dead (R4); one unversioned `walker` edge already crossed (R10); repair-by-reinstall impossible (R1) | **Preserve, don't update:** the preservation set is `offline.db` (md5 `c4b27c38…`, 304 318 B) + 28 cache entries (14 `.zst` + 14 `.sig`) + the 2 clone trees; copy before any cache prune |`. Now: offline.db is absent from the captured sync-directory listing. Preservation/read commands that assume that path exists are not presently runnable there; absence elsewhere, deletion time, cache availability and repository reachability are unknown [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:48-55]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:54.

- R18-FRESH-SUPPLEMENT-28: prior locus `PackageOptional PackageTrustedOnly`; 0 `.db.sig`; `SigLevel = PackageRequired`. Now: the directory includes openai-chatgpt.db.sig;0 total.db.sig is not a current directory inventory. This is not a claim that omarchy.db is signed or that any signature validates. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:54.

- R18-FRESH-SUPPLEMENT-29: prior locus `folder)` beside the current `7.2.3-arch1-3` (v2 §6, identical text). No reboot pending`. Now: current capture lists nvidia/615.78.08 for6.18.57-2-lts and7.2.11-arch1-1, plus7.2.3-arch1-3 with missing built modules. No7.1.4 row is listed, so the old610.57.04/7.1.4 removal action is stale and must not be replayed. No removal or reboot clearance is given [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:5-7, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:92-96]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:95.

- R18-FRESH-SUPPLEMENT-30: prior locus `| 4 | `elephant-bluetooth` 2.21.0-1 | `offline-exile` | none | n/a — no route |`. Now: the later09:31 invocation names elephant-bluetooth2.22.1-1 archives, so the historical no-update-route wording is not a current bounded search result; per-plugin installed/repository state remains unknown because R18 lists only the base elephant package [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:62-74]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:72.


## R18-RECHECK — steer-safe procedure

Supersedes this entry's historical pointer-based recheck procedure for a steer forbidding package-manager execution (QUALITY26). Historical command receipts remain historical; do not run their backticked package commands or the live host census merely by following the old section pointer. This is an actual bounded read/compare procedure, not a whole-host clearance or a new host measurement.

- Read the installed-name/version metadata with `ls -1 /var/lib/pacman/local`; for each package whose recorded field is being rechecked, read its exact `/var/lib/pacman/local/<pkg>-<ver>/desc` and compare name, version, install date, reason and validation fields with the dated table. Directory presence does not certify file integrity or current repository reachability.
- Read repository-file inventory and timestamps with `ls -1 /var/lib/pacman/sync` and `stat -c '%y %n' /var/lib/pacman/sync/*.db`. A filesystem mtime alone does not establish local acquisition or refresh time; its origin is not re-established by this capture; a present database is not proof it is configured.
- Read relevant transaction events using `tail -n 80 /var/log/pacman.log`; distinguish invocation headers from ALPM completion events, preserve capture time and exit status, and never infer a current pending-update count from this history.

Record observed values and unresolved questions separately. Uncaptured pending updates, signature validity, exact foreign/orphan classification, private mount views, historical provenance events and recovery feasibility remain unknown until their own authorized evidence is obtained. No installation, restart, rebuild, subvolume action or boot write is authorized.


## R18-PRECISION — complete elephant-family scope

SUPPLEMENT-30 supersedes current-use no-route/version statements for the entire elephant-family rows111–123, not merely row112. S060's selected local-db listing names the base package; its log line72 separately names plugin archives. S065 now records thirteen actual upgraded elephant-family events and transaction completion09:31:04; neither that history nor the directory listing establishes present repository reachability or the omarchy-walker row124. Current orphan membership, pending updates and recovery feasibility remain unmeasured here.

Earlier R17 'ran/executed' full-upgrade wording denotes the recorded invocation/start plus observed ALPM package changes, not a client exit/health verdict. S065:18 now supplies the historical ALPM transaction-completed record09:16:47. Earlier invocation-only removal/installation attributions must be read with the S065 event records (specific removals6–8/91–94, elephant43–69). These are historical receipts, not a current package-action clearance.

## Round-39 correction (TO1, TO8; append-only)

Round-39 clarification (TO1, TO8): these hooks are PostTransaction hooks; they run after `transaction completed` is logged, within the same `pacman` command but not inside the logged `transaction started`…`completed` window, and none of them runs if the commit is interrupted or fails (`trans.c:230-239`, HO6); their output is logged as `[ALPM-SCRIPTLET]`. It qualifies the "in the transaction" / "in-transaction" / "in one transaction" wording above. Source: `corpus/knowledge/pacman-transaction-order-r39.md` TO1, TO8 (S216, S217).
