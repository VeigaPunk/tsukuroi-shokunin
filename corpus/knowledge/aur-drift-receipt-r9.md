# AUR-drift receipt — the watch's first census re-run vs the r6 baseline: explicit no-drift (S9-3, round 9)

source: live read-only probes, host `plazir27`, user `vgpnk` (non-root), window
**2026-10-14 19:58:19Z – 19:59:27Z** (-0300 16:58–16:59). Probes: `bash tools/tsukuroi-census.sh`
(live, rc=1) and `--selftest` (rc=0), `pacman -Qm` (rc=0), `pacman -Qmdtq` (rc=1),
`pacman -Qme` (rc=0), `pacman -Qu` (rc=1), `md5sum`/`wc -l`/`stat` on the census and
`/var/log/pacman.log`, `diff` of the live `-Qm` rows against (a) the census's embedded
`R6_FOREIGN_BASELINE` and (b) the register's §1 rows (name+version projection), `grep` event
sweeps over `/var/log/pacman.log`, `git status`/`git rev-parse` in the repo. No `pacman`
transaction, no `-Sy`/`-Syu`, no service action, no root, no network, no external site.
Scratch `/tmp/w9-tsukuroi-s93/`. Zero host mutation: `/var/lib/pacman/db.lck` absent before and
after; repo tree byte-identical (0 `git status --short` lines before and after the gate run).
Revision under test: HEAD `72b038d` (round-8 commit, tree clean), census
`e2c4558a3ae4ddd2eca67e8f4d64281c` / sha256 `bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55`,
1472 `wc -l`, 73 919 B — identical to the round-7 landed pin (`SKILL.md:855-865`), i.e. round 8
did not touch the gate.
Dispatch frame: lane assignment **S9-3** — "the AUR watch's first drift event: with the census
re-run, any foreign-package drift vs the r6 baseline gets its first real receipt (or an explicit
no-drift receipt)". Wave plan: `plans/round-9.plan.md` (md5 `3a59d2edd068abf6281d7701d261ea5c`,
270 `wc -l`) — cited as a plan, never as landed state.
verified-at: 2026-10-14 19:58:19Z – 19:59:27Z (one window; **every value a capture — re-run,
never quote**).
recheck: §6.
Notation: **[obs]** measured in this window · **[inf]** inference, stated as such ·
**[unk]** not settled, with the probe that would settle it. Line numbers are `wc -l` conventions
unless stated.

## 0. Verdict — the explicit no-drift receipt [obs]

**The first census re-run against the r6 baseline, on the landed round-8 revision, reads
`foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16)`.** In the arm's own semantics: every live
`pacman -Qm` row matches its baseline row at the same version; no new foreign name arrived; no
baseline row changed version; no baseline row left the installed set.

The reading is confirmed three independent ways in this window:

| # | comparison | result |
|---|---|---|
| 1 | live `pacman -Qm` (16 rows) vs the census's **embedded** snapshot `R6_FOREIGN_BASELINE` (census `:238-253`) | `diff` rc=0 — byte-identical, including order |
| 2 | live `pacman -Qm` vs the **register's** §1 rows (`aur-risk-plane.md:64-79`, name+version projection) | `diff` rc=0 |
| 3 | the gate's own classification (`foreign=16(known=16 new=0 drift=0 gone=0)`) and the raw reads below | consistent; no non-empty class to name |

What this is not: it is **not** a claim that the foreign set is correct, current, or safe — §3
separates those. It is exactly: no change in the foreign set's name/version rows between the r6
measurement (2026-10-14 17:38–17:43Z) and this run (19:58:19Z), as seen by `pacman -Qm`.

## 1. The live run (verbatim) [obs]

`bash tools/tsukuroi-census.sh`, banner 2026-10-14T19:58:19Z, rc=1, 1.29 s wall, raw capture
`/tmp/w9-tsukuroi-s93/live/census.out`:

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T19:58:19Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16); pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2[user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922897 C5_swap_peak_pct=99% C5_pswp=72355084/95577924 C5_sock_throttled=71107; C6_psi_some_avg300=0.26 C6_psi_full_avg300=0.26 C6_psi_full_total_us=71778194 C6_avail_kb=19624732 C6_shmem_kb=5554852; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=742 (coredump=467 kernel=139 other=136); failedhist=8[app-com.onepassword.OnePassword@autostart.service,app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service,app-walker@autostart.service,init.scope,-.slice,user@1000.service]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

Scope note: this receipt reads **only** the `foreign=` field of the packages line. The
`DEGRADED` verdict rides other fields — the unrelated `1password` `-Qkk` sample drift and the
drivers/journal planes (live coredump storm, moving counts) — none of which is foreign-package
drift. Do not collide them (§3).

## 2. The comparison, row by row [obs]

Live `pacman -Qm`, unpiped, rc=0, 16 rows, captured 19:58:28Z
(`/tmp/w9-tsukuroi-s93/live/qm.out`; md5 of the capture block `bde5487579e57c044768112d17e54ab4`):

```
android-apktool-bin 3.0.3-1
elephant 2.21.0-1
elephant-bluetooth 2.21.0-1
elephant-calc 2.21.0-1
elephant-clipboard 2.21.0-1
elephant-desktopapplications 2.21.0-1
elephant-files 2.21.0-1
elephant-menus 2.21.0-1
elephant-providerlist 2.21.0-1
elephant-runner 2.21.0-1
elephant-symbols 2.21.0-1
elephant-todo 2.21.0-1
elephant-unicode 2.21.0-1
elephant-websearch 2.21.0-1
obsidian-cli-inspector 1.0.3-1
omarchy-walker 1.0.0-2
```

Per-class receipt (the arm's four classes; each non-empty class would be named in the note —
none is):

| class | count | names |
|---|---|---|
| `known` | 16 | all 16 above — each live row matches its baseline row at the same version |
| `new` | 0 | — |
| `drift` | 0 | — |
| `gone` | 0 | — |

The two comparison sides were extracted at 19:58–19:59Z, mechanically:
`diff <(cat qm.out) <(sed -n "/^R6_FOREIGN_BASELINE='/,/'$/p" tools/tsukuroi-census.sh |
sed "1s/^R6_FOREIGN_BASELINE='//; \$s/'\$//")` → rc=0; and the register §1 projection
`awk '/^## 1\. The register/,/^## 2\./' aur-risk-plane.md | grep -E '^\| (android-apktool-bin|
elephant|obsidian-cli-inspector|omarchy-walker)' | …` → `diff` rc=0. (Both extractions kept in
scratch; the register's other sections contain rows with the same names — bio/commit rows — so
the extraction is scoped to §1 on purpose.)

Supporting reads in the same window:

- [obs] `pacman -Qmdtq` → no output, **rc=1** — no foreign orphan (matches r6 §0).
- [obs] `pacman -Qme` rc=0, 3 rows — `android-apktool-bin`, `obsidian-cli-inspector`,
  `omarchy-walker` — exactly the r6 explicit-foreign trio (`aur-risk-plane.md §0`).
- [obs] `pacman -Qu` unpiped rc=1, 0 lines — no pending upgrade for anything, foreign included.
- [obs] `/var/log/pacman.log`: md5 `e452d910de724ac016c2d019f9e1ec45`, 2109 lines, 157 286 B,
  mtime `2026-10-13 16:37:59 -0300` — **byte-identical to the digest the r6 note pinned**
  (`foreign-provenance-r6.md:35`), i.e. the host's entire pacman history has not changed since
  the r6 measurement. 0 lines dated `2026-10-14`; last entry `2026-10-13T16:37:59-0300
  [ALPM] running '35-systemd-update.hook'…`.
- [obs] per-name event sweep over the whole log —
  `grep -cE "\] (upgraded|downgraded|reinstalled|removed) <name> "` = **0 for each of the 16**
  (installation lines excluded, matching the r6 probe's event set). No transaction recorded since
  2026-10-13T16:37:59-0300; nothing the host's own package manager saw could have drifted a row.

Machine-readable receipt:

```
# aur-drift receipt — plazir27 — S9-3 round 9 — measured 2026-10-14T19:58:19Z–19:59:27Z
# census: tools/tsukuroi-census.sh md5=e2c4558a3ae4ddd2eca67e8f4d64281c sha256=bba6cdf6… lines=1472 bytes=73919 HEAD=72b038d
# live run rc=1; foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16)
# baseline: R6_FOREIGN_BASELINE census:238-253 (16 rows) == aur-risk-plane.md §1 :64-79 (name+version)
# live -Qm rc=0 16 rows; diff(live, embedded snapshot)=0; diff(live, register §1 projection)=0
# -Qmdtq rc=1 empty; -Qme rc=0 3 rows (explicit trio); -Qu rc=1 empty
# pacman.log md5=e452d910de724ac016c2d019f9e1ec45 lines=2109 bytes=157286 last=2026-10-13T16:37:59-0300
#   upgrade-class events for the 16 names = 0; log lines dated 2026-10-14 = 0
# db.lck absent before/after; repo tree 0 dirty lines before/after; host files written: none
pkg=android-apktool-bin 3.0.3-1      class=known
pkg=elephant 2.21.0-1                class=known
pkg=elephant-bluetooth 2.21.0-1      class=known
pkg=elephant-calc 2.21.0-1           class=known
pkg=elephant-clipboard 2.21.0-1      class=known
pkg=elephant-desktopapplications 2.21.0-1 class=known
pkg=elephant-files 2.21.0-1          class=known
pkg=elephant-menus 2.21.0-1          class=known
pkg=elephant-providerlist 2.21.0-1   class=known
pkg=elephant-runner 2.21.0-1         class=known
pkg=elephant-symbols 2.21.0-1        class=known
pkg=elephant-todo 2.21.0-1           class=known
pkg=elephant-unicode 2.21.0-1        class=known
pkg=elephant-websearch 2.21.0-1      class=known
pkg=obsidian-cli-inspector 1.0.3-1   class=known
pkg=omarchy-walker 1.0.0-2           class=known
```

## 3. What this receipt does and does not prove [obs/inf/unk]

- [obs] Proves: the live foreign set equals the r6 accepted snapshot row-for-row (name +
  version) at 19:58:19Z; no `new`/`drift`/`gone` class fired; no pacman-log upgrade-class event
  touched any of the 16 since install day.
- [inf] The no-drift reading is not vacuous: the arm's failure classes are exercised by its own
  fixtures (§5) — `new`, version-`drift`, `gone`, and the two fail-closed branches all have
  passing cases; an independent verifier reproduced the fold (VER-S7, §5).
- [obs, scoped] File integrity is a *different* arm: the `-Qkk` sample drift
  `2[1password-beta,1password-cli]` rides the same PLANE line and is **not** foreign drift.
  Foreign drift (a row of the foreign set changed) and file drift (a package's files changed)
  are disjoint claims; this receipt reads only the former.
- [unk] Upstream: what the AUR / omarchy channels hold for these names *now* — not measured (no
  network probe; out of lane). The 14 channel-A packages have no configured repository at all
  (register §2), so `-Syu` can never move them; a `yay`-style rebuild is the only realistic
  drift path, and it would surface as `drift=[name(old->new)]` in the next re-run.
- [unk] Local-db tamper: no probe here attests that `/var/lib/pacman/local` itself is
  untampered — a hand-edited local db could make a changed package read `known`. Named, not
  absorbed; the probe that would settle it (a digest of the local db) does not exist in the gate.
- [obs] Authority: the baseline is a snapshot of the r6 accepted set. "Equals the baseline" is
  not "the set is safe" — risk classification lives in `aur-risk-plane.md §4` and is out of this
  receipt.

## 4. The reading chain (captures, never disagreements) [obs]

| window (UTC) | reading (`foreign=` field) | source |
|---|---|---|
| r6 register measurement 17:38:09–17:43:01Z (14:38–14:43 -0300) | 16 rows, per-package table | `aur-risk-plane.md §1`; `foreign-provenance-r6.md` §1 |
| round-7 landing run 18:39:42Z | `foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16)` | `SKILL.md:874-884` (round-7 append, live block) |
| round-8 landing check 19:10:28Z | same field | `plans/round-8-record-draft.md:158-174` |
| round-9 plan draft pin 19:10:40Z | same field | `plans/round-9.plan.md:199-205` (draft-time capture) |
| **this receipt 19:58:19Z (S9-3)** | same field — first dedicated drift receipt | this file |

- [obs] All five readings agree on the name/version field. Counts that moved between the rows
  (`err=442→742`, coredump 279→467, swap counters) are the journal/drivers planes' live
  environment and are not this arm.
- [inf] This file is the arm's first **dedicated receipt artifact**; the earlier readings exist
  only inline (the round-7 `SKILL.md` append, the round-8 record draft, the round-9 plan pin).
  Round 7 landed the watch (census revision `e2c4558a…`, 49-case selftest); round 8 ran the gate
  but did not land a drift receipt; round 9's re-run is this one.

## 5. Why the no-drift reading can be trusted (fail-closed context, cited) [obs]

- [obs] Selftest, own run 2026-10-14 ≈19:59:21–19:59:27Z (5.33 s), rc=0, verbatim last line:
  `TSUKUROI_CENSUS_SELFTEST: PASS (49 cases, 49 passed, 0 failed)`. The foreign fixtures are the
  6 the round-6 contract required — hit (`tools/tsukuroi-census.sh:1167`), embedded-default
  (`:1173`), `new` (`:1179`), version-`drift` (`:1185`), `gone` (`:1191`), absent-baseline
  (`:1197`) — plus the 16-row literal guard (`:1156-1165`) that makes an edit to the snapshot
  impossible to pass silently.
- [obs] Independent verification: `corpus/knowledge/aur-risk-plane-ver-s7.md` (VER-S7; md5
  `4608743dfa6230e806985d164f3c00f4`, 184 `wc -l`) — verdict **CONFIRMED**; the count and the
  fold reproduce from a non-author's own probes, the embedded baseline equals the register's 16
  rows, and all four fail-closed branches fire and name their class.
- [obs] The arm's shape is fail-closed both ways (census note, `tools/tsukuroi-census.sh:59-68`):
  any `new`/`drift`/`gone` row → DEGRADED with names; an absent/unreadable baseline prints
  `foreign=<n>(base=absent [known/new/drift/gone unknown])` and stays DEGRADED — never HEALTHY
  off a missing baseline; an unreadable `-Qm` prints `foreign=? [pacman -Qm unreadable]`. This
  receipt could have failed visibly; instead every class came back empty.
- [obs] Read-only contract held: `git status --short` 0 lines before and after the gate run; no
  `db.lck` before or after; live mode writes nothing (round-2 guarantee, unchanged).

## 6. Recheck (compact, read-only)

```
cd tsukuroi-shokunin
md5sum tools/tsukuroi-census.sh                     # expect e2c4558a3ae4ddd2eca67e8f4d64281c at HEAD 72b038d
bash tools/tsukuroi-census.sh | grep '^PLANE packages'
pacman -Qm > /tmp/qm.now && wc -l /tmp/qm.now       # expect rc=0, 16 rows
sed -n "/^R6_FOREIGN_BASELINE='/,/'$/p" tools/tsukuroi-census.sh \
  | sed "1s/^R6_FOREIGN_BASELINE='//; \$s/'\$//" > /tmp/base.now
diff /tmp/qm.now /tmp/base.now                      # expect rc=0 (bytes, incl. order)
pacman -Qmdtq; echo "rc=$?"                         # expect rc=1, empty
grep -cE '^\[2026-10-14' /var/log/pacman.log        # expect 0 at this writing
md5sum /var/log/pacman.log                          # expect e452d910de724ac016c2d019f9e1ec45
```

Every step read-only; the `diff` must compare rows as `pacman -Qm` prints them (name + version).

## 7. Unknowns / out of reach (owners)

- Upstream channel state for the 16 (AUR RPC answers / omarchy repo contents) — [unk]; no network
  probe in this land, and an `-Sy` refresh is the first mutating step (refused here). Owner:
  operator.
- Local-db tamper detection — [unk]; no probe exists (see §3). Owner: operator if wanted.
- Whether a future re-run lands a real `new`/`drift`/`gone` event — [unk]; the watch names it
  when it does.
- The register's proposed standalone baseline file (`corpus/knowledge/foreign-aur-baseline.tsv`
  shape) — still does not exist: no `*baseline*` file in the tree at write time and
  `TSUKUROI_FOREIGN_BASELINE` unset in the live run, so `base=` reads `r6(16)`. Owner: the
  register lane, not this receipt.
- Concurrent round-9 lanes may land other artifacts after this window; every pin above is a
  capture at 2026-10-14 19:58–19:59Z, not a claim about later revisions.

## 8. Errata (append-only)

- (new file — nothing to correct yet; append below, never rewrite)