VERDICT: draft

Seat AsmPackageScan, item F-4 (round 41 planning input; read-only scan). Receipts: `.ufo/waves/round-40/w1/AsmPackageScan/receipts.md`. Nothing run besides read-only greps, `pacman -Q` (query), `man -P cat`, and two read-only `curl` GETs. No install/upgrade, no host or lane write other than this report and the receipts file. Not done: I did not re-open every staged source; I did not re-run any lane counter; I did not read all 70 staged bodies (read in full: `alpm-package-anatomy-r26.md`, `initramfs-hook-api-r25.md`, `overlayfs-mount-contract-r25.md`; first 8 lines of three others).

## 1. Method

- Staged set: `merge/tsukuroi/MERGE-REPORT.md:7` "proposed knowledge entries: **70**"; `ls` of `.../knowledge/corpus/knowledge/` returns 70 files (matches the report's table, lines 19-88).
- Gate grep: for every staged filename stem, `grep -l -F "<stem>" corpus/lessons/round-3*.md` (receipts, Cmd 1). Round 3x lessons that carry a staged-package Gate: `round-37.md`, `round-38.md`, `round-39.md` plus the matching `*-verifier-spotcheck.md`.
- Province test: `PROVINCE.md` Core (`:6-14`) = pacman state, systemd user units/timers, journal/boot triage, driver/firmware, update-safety; added surfaces (`:18-23`) = Arch News gate, `.pacnew`/`.pacsave`, "Initramfs v42 and boot recovery", "Snapper/rollback net"; round-38/39 promotion (`:199-237`) adds the btrfs error counters and the one mount-table read. Frontier (not Core): scrub record and NVMe SMART (`:212-214`).

## 2. Already adjudicated in a round-3x Gate (5 of 70 — do not re-plan)

| staged file | decision | where |
|---|---|---|
| `errno-contract-variance-r37.md` | admitted (held in lane) | `lessons/round-37.md:74` |
| `errno-name-discrimination-r25.md` | reject; flip stated | `lessons/round-37.md:22`, `:74`; spotcheck `:96` agrees |
| `mount-errno-contract-r26.md` | reject; flip (a)-(d) stated | `lessons/round-37.md:74`; `lessons/round-38.md:53-73` |
| `pacman-hook-timing-r25.md` | reject as staged r38; r39 admits the transaction-order core by re-grounding (`pacman-transaction-order-r39.md`), rejects `:22`,`:26-27` and the CN "independent confirmation" sentence, defers four residual propositions (`NeedsTargets`, `.pacnew` target, cwd `/`, interpreter) — these were then written as `pacman-exec-environment-r40.md` | `lessons/round-38.md:48`; `lessons/round-39.md:45-64` |
| `alpm-package-anatomy-r26.md` | reject; flip "a revision that quotes PKGBUILD(5) for each function's working directory and passes a QUALITY check" | `lessons/round-38.md:49`, `:120`(spotcheck agrees) |

## 3. Staged entries inside Core and not adjudicated (0 hits in `corpus/lessons/round-3*.md`)

Grouped by the PROVINCE surface they would extend. "Tier" is the staged source rows' tier (SOURCES.append.md).

**A. Initramfs v42 and boot recovery (`PROVINCE.md:22`)**
- `initramfs-hook-api-r25.md` (S200 mkinitcpio(8), S210 Arch news) — tier A. Cross-referenced only, never decided: `.ufo/waves/round-38/w1/AsmRevTiming.md:228` ("does not exist in the lane").
- `upstream-release-watch-r25.md` (S096, S097, S110, S111, S210, S211) — mixes landed lane rows with staged S211 (plymouth tag list); `round-39/w1/ScoutQuarantine.md:18` records it as not adopted.
- East-Asian renderings, tier B: `initramfs-hook-api-ja-r26.md` (S216), `initramfs-hook-api-zh-r27.md` (S222), `mkinitcpio-hook-api-zh-r29.md` (S245), `mkinitcpio-42-upgrade-gate-cjk-r26.md` (S216, S221), `plymouth-hook-cjk-r27.md` (S226, S227).
- Plymouth watch chain (staged r37 to r41): `plymouth-release-watch-r37.md`, `-r38.md`, `plymouth-live-tag-instrument-r39.md`, `-r40.md`, `plymouth-release-notes-r41.md` — five entries on one subject; consolidate before any adoption.

**B. Snapper/rollback net and snapshot-boot path (`PROVINCE.md:23`)**
- `overlayfs-mount-contract-r25.md` (S203 kernel `overlayfs.rst` v7.2, S208 zh-hk ArchWiki Snapper; also names landed S021, S036, S042, S045, S098, S111, S112).
- `snapper-rollback-bilingual-r25.md` (S206, S207 SUSE, S213 Oracle) — tier B vendor docs (SLES/Oracle Linux), `ScoutQuarantine.md:18`.
- `snapshot-boot-test-prestate-r41.md` (S309, a campaign capture on shokuknow's own host).
- Amendments to lane entries, own-work sources: `snapshot-boot-preconditions-amend-2026-10-23.md` (S231), `boot-writers-amend-2026-10-23.md` (S242), `errno-falsifier-amend-2026-10-23.md` (S230).
- errno:13 family (extends `snapper-eacces-mechanism.md` surface): `errno-13-operator-state-r39.md`, `-r40.md`, `errno-13-mechanism-r41.md`, `errno-13-observation-status-r42.md`, `errno-symbol-descriptions-r38.md`, `-r40.md`, `-r41.md`, `errno-instrument-absence-r42.md`, `errno-contract-eastasia-r28.md`.

**C. Storage (round-38/39 Core + wave-2 frontier)**
- `btrfs-ioctl-surface-r27.md` (S223 uapi header v7.2), `btrfs-filesystem-troubleshooting-bilingual-r26.md` (S218, S219 SUSE zh/ja), `btrfs-space-repair-amend-2026-10-23.md` (S243, own-work).

**D. pacman state / `.pacnew` (`PROVINCE.md:8-10`, `:21`)**
- `pkgbuild-semantics-zh-r27.md` (S228, S232), `pkgbuild-drift-rules-zh-r29.md` (S246) — tier B renderings of PKGBUILD/pacman docs.

**Outside Core (excluded, 33 files):** `zh-cmpp-*` (9), `zh-cn/tw-tree-contents-*` (4), `zhwiki-*` (3), `translation-*` and `kernel-doc-translation-scope-r28.md` (5), `zh-syscall-*` (4), `zh-overlayfs-rendering-r31.md`, `manpages-mirror-*` (3), `eastern-tradition-host-docs-r44.md`, `lane-harness-selftest-r29.md`, `ext4-*` (2; host root is btrfs, second NVMe is xfs, `PROVINCE.md:214`). That sums the 5 adjudicated + 32 Core-inside above + these; counts are by hand from the list in MERGE-REPORT.md and not machine-checked — treat as ±2.

## 4. Two best candidates

Ranking rule: tier-A sources, a stated flip or a still-unheld ground, host-verifiable today, and no contradiction found against a pinned source.

### Candidate 1 — `initramfs-hook-api-r25.md` (staged 55 lines; never adjudicated)

- **Cited sources (staged rows, SOURCES.append.md:7 and :17).** S200 mkinitcpio(8) https://man.archlinux.org/man/mkinitcpio.8, anchors ABOUT RUNTIME HOOKS / ABOUT INSTALL HOOKS (`add_runscript`) / ABOUT POST HOOKS, mkinitcpio 42.2, man date 2026-10-01; S210 https://archlinux.org/news/mkinitcpio-hook-migration-and-early-microcode/ (2024-03-04, Morten Linderud). Entry text also names S014 (ArchWiki mkinitcpio) and S112 (btrfs-overlayfs hook, lane rows).
- **Ground it adds (per `corpus/README.md`).** The coverage-map row `knowledge/initramfs-v42-sysroot-recovery.md` (README `:19`) rests on S014/S016/S021/S022 and holds no statement of the hook API: grep `run_emergencyhook|run_cleanuphook` over `corpus/` and `SKILL.md` returns nothing; grep `hook-migration|early-microcode|v38` over `corpus/SOURCES.md` and `corpus/knowledge/*.md` returns nothing; `corpus/SOURCES.md:323` still lists "mkinitcpio(8) runtime parameter reference" as an unopened lead. So the entry closes that lead and gives the "Initramfs v42 and boot recovery" surface (`PROVINCE.md:22`) its first tier-A API statement: five runtime hook points in order, cleanup reverse order, `add_runscript` naming rule, and the v38 migration precedent. It is deeper ground on a held Core surface, not a new surface.
- **Checked today (2026-10-26) against the host and the source.**
  - Local `man mkinitcpio` (host mkinitcpio 42.2-1, `pacman -Q`) lines 239-256 carry the five hook points with the staged wording; ordering: "hooks are run in the order that they are defined in the HOOKS variable, except for cleanup hooks which are run in reverse" (local man line 240-241). The emergency hook text ends "this allows boot splash screens to terminate their process, so users will notice the failure" — it supports the entry's splash sentence.
  - Arch news page fetched 2026-10-26T07:16Z, HTTP 200: "2024-03-04 - Morten Linderud"; "moved to the mkinitcpio upstream project. The hooks are: systemd, udev, encrypt,"; "conflicts have been introduced into the respective packages to prevent installing packages". The staged "temporary package conflicts" claim matches.
  - A host column is available for free from files: `/usr/lib/initcpio/hooks/*` define — `plymouth`: run_hook, run_latehook, run_emergencyhook; `btrfs-overlayfs`: run_latehook only; `usr`: run_latehook; `udev`: run_earlyhook, run_hook, run_cleanuphook; `shutdown`: run_cleanuphook; encrypt, btrfs, keymap, consolefont, resume, sleep, memdisk: run_hook. Configured `HOOKS=(base udev plymouth ... encrypt filesystems fsck btrfs-overlayfs)` + `resume` (`/etc/mkinitcpio.conf.d/*`). Meaning: on this host both `/new_root`-sensitive hooks (plymouth, btrfs-overlayfs) act at `run_latehook`, i.e. after root is mounted. That is a host observation derived from file greps, not the staged entry's text — a drafting round must add it with a counter (see risks).
- **Risks.**
  1. Registry collision: staged ids S200 and S210 now name different documents in the lane (`corpus/SOURCES.md:209` S200 = mount(2); `:219` S210 = trans.c at 54d9411); lane ids run to S225, so adoption must be by document from **S226** (round-39 rule, `lessons/round-39.md` Assimilation paragraph).
  2. Stale framing: the staged `ground:` line (`:6`) and the "stranding" paragraph call the v42 two-hook stranding open; `corpus/README.md:149-153` (round 17) records that 42.x keeps `/new_root` as a symlink and both hooks resolve (not boot-tested), and `corpus/README.md:223-231` notes the untested snapshot path is the remaining item. "The lane's own v42 two-hook stranding is the same shape" is an inference, and the staged boundary list does not mention `boot-chain-r17.md`. Any admitted text must restate against r17/r24.
  3. "What the lane did not previously hold" (staged `:10-16`) is partly wrong: the lane holds S014 (ArchWiki runtime hooks) and S112 (hook body); only the man-page-grade API statement is new. Overstated novelty is the QUALITY 14/1 class that rejected its siblings.
  4. No `## QUALITY check` (staged file has 0 `QUALITY` hits; QUALITY 14), the round-38 defect for every staged file.
  5. Recheck drift: S200 is pinned to mkinitcpio 42.2 man date 2026-10-01 and the row says `on-release`; a 42.3/43 release changes it. Also the `[inference]` sentence "hook point a splash process must be able to reach" extends the man page; keep the quote, mark the rest.
  6. Round-39 pattern R39-CONTENT-UNREAD / R39-HOSTCELL-INFERRED-AS-SEEN applies: if a host column is added it needs a counter that reads the hook files, and each host cell must name its command (the `grep -o '^run_[a-z]*hook' /usr/lib/initcpio/hooks/*` form above is one).
- **Suggested shape for round 41.** A lane-authored `initramfs-hook-api-r41.md` with rows HK1-HK5 (one per hook point, source quote at man-page anchor, host cell from `/usr/lib/initcpio/hooks/*`), HK6 cleanup-reverse order, HK7 the v38 precedent with the 2024 date stated, QUALITY section, by-document new rows S226+ for mkinitcpio(8) and the news item.

### Candidate 2 — `alpm-package-anatomy-r26.md` (staged 62 lines; rejected r38 with a stated flip condition)

- **Cited sources (SOURCES.append.md:22 and :24).** S215 alpm-package(7) https://man.archlinux.org/man/alpm-package.7 (CONTENTS; extra/alpm-docs 0.13.0-1); S217 PKGBUILD(5) https://man.archlinux.org/man/PKGBUILD.5 (options, packaging functions, INSTALL/UPGRADE/REMOVE SCRIPTING; Pacman 7.1.0, man date 2026-10-15). Round 38 re-opened both on 2026-10-26 and pinned `doc/PKGBUILD.5.asciidoc` and `scripts/makepkg.sh.in` at 54d9411 (`.ufo/waves/round-38/w1/AsmRevAnatomy.md` §1, receipts in `AsmRevAnatomy/`).
- **Ground it adds (per `corpus/README.md`).** The pacman plane rows (README `:7`, `package-state-plane.md`; `PROVINCE.md:8-9` ".pkg.tar.zst receipt discipline") record measured host state, not packaging doctrine. AsmRevAnatomy §3 F6 found: no lane entry documents the package-file anatomy (`.BUILDINFO`/`.MTREE`/`.PKGINFO` at the root, optional `.INSTALL`, data extracted to root, root ownership) and none documents PKGBUILD(5) semantics (epoch, `install`, `backup`, mandatory fields). Overlap since then, checked today: `pacman-transaction-order-r39.md` TO3/TO4/TO7 hold scriptlet order and argument order (new first, old second) at libalpm source level; `pacman-backup-files-r35.md` holds `backup` → `.pacnew`/`.pacsave`; `pacman-exec-environment-r40.md` EX5 holds `.INSTALL` staging. What is still unheld: the package-file layout (alpm-package(7)), `epoch` and the mandatory-field set, and PKGBUILD(5)'s own upgrade sentence "none of the install or remove functions will be called" (host man line 279 confirms it; TO7 states the same fact only from `remove.c`). So the genuinely new part is roughly the first half of the staged file (`:8-18`, `:44-47`); the six-row scriptlet table (`:30-37`) now duplicates TO3/TO4 and would not count as distinct ground.
- **Risks.**
  1. False sentence at staged `:52-54` ("`package()` runs inside `$pkgdir` under `fakeroot` and the others run inside `$srcdir`") and in staged S217's teaches cell; contradicted by PKGBUILD(5) ("This function is run inside $srcdir"; verify() "is run inside $startdir") and by `makepkg.sh.in:414,452-454,468-470` at 54d9411 (AsmRevAnatomy §3 F1). Host man page agrees with the source (`man PKGBUILD` lines 228-244). The round-38 flip condition requires quoting each function's working directory.
  2. No `## QUALITY check` (0 `QUALITY` hits, QUALITY 14); ground pointer `corpus/README.md:38-42` does not hold the "packaging-and-hook-semantics frontier" (F3 of round 38); "round 1's Arch Dev Blog row" dangles (F4).
  3. Id collision grew since r38: staged S215 and S217 now collide with landed lane rows S215 (remove.c) and S217 (trans.c) (`corpus/SOURCES.md:224`, `:226`), so by-document renumbering from S226 is mandatory.
  4. Overlap risk: with TO3/TO4/TO7/EX5 landed, an entry that restates the scriptlet table is a duplicate; the round-37 flip rule (d) (`lessons/round-38.md:73`) — "adds at least one proposition the admitted entry does not carry" — is the bar. Only package anatomy, epoch and the mandatory fields clear it.
  5. It is rules-only with no host cell (the staged Boundaries say so, `:58`). A host cell is possible read-only, e.g. list a cached package's members from `/var/cache/pacman/pkg/` and check `.PKGINFO`/`.MTREE` at root; I did not run that, so the existence and read permission of such a package are unverified. The round-39 hostcell lesson says to mark the unmeasured case or leave the column out.
  6. Province boundary: doctrine on the receipt side of "pacman state" (AsmRevAnatomy §4 in scope); it must not drift into makepkg/build advice (Core never installs or builds packages, `PROVINCE.md:27-28`).
- **Suggested shape for round 41.** A lane-authored `alpm-package-anatomy-r41.md` that (a) quotes alpm-package(7) for the root-level members and extraction target, (b) states `epoch` and the mandatory fields with PKGBUILD(5) anchors, (c) states the upgrade sentence and points to TO3/TO4/TO7 instead of repeating the table, (d) corrects the working-directory claim with the pinned asciidoc lines (`:345-357` per AsmRevAnatomy), (e) carries a QUALITY section, and opens new rows from S226 pinned at 54d9411/alpm-docs 0.13.0-1.

### Runners-up (one line each)
- `overlayfs-mount-contract-r25.md`: tier-A kernel `overlayfs.rst` v7.2 (S203) is not held in the lane (no `overlayfs.rst` row in `corpus/SOURCES.md`); novelty is real, but the Chinese "systemd-based initramfs unsupported" claim is a tier-B rendering of a 12-month-old revision and the host builds the `sd-btrfs-overlayfs` install hook too (`/usr/lib/initcpio/install/` lists it) while using the busybox flavour — a host column would have to separate those.
- `btrfs-ioctl-surface-r27.md`: S223 uapi header v7.2; overlaps the flip conditions already written for `mount-errno-contract-r26.md` (`lessons/round-38.md:56-73`), so it only helps as the per-ioctl source of those pairs.

## 5. What I did not do
- Did not run `pacman -Qi`/cache reads for a host cell on candidate 2; did not verify host kernel tag vs v7.2 for candidates in B/C.
- Did not re-open S215/S217 (relied on the round-38 re-open; confirmed only the local PKGBUILD(5) man lines and that `alpm-package(7)` is not held in the lane by grep).
- Did not check the 33 "outside Core" entries beyond title/rows from MERGE-REPORT.md; classification of `plymouth-*` as Core is the weakest call (they extend the update-surface watch, not the hook surface) and may be moved out by the planner.
- Counts in §3 are hand-sorted, not scripted.

Tools installed/updated: none.
