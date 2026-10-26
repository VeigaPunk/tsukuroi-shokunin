VERDICT: supports

Seat C2CritTO3, item C2-8: attack TO3 and TO7 empirically on the frozen transaction capture. No
counterexample found for either row. Two findings that narrow the claim without killing it: (a) the
pre-scriptlet half of TO3's host column has **zero** host instances in this capture, and the log's line
order cannot attribute a pre-scriptlet's output to its package at all; (b) TO7's scriptlet-ordering half
(`pre_remove` → files → `removed` → `post_remove`) also has zero host instances because none of the 28
removals printed anything. The account of the *observed* instances is exact: 29 output blocks, 189
scriptlet lines, every one of them after its own package's line and before the next package's line.

Read-only work: no lane file touched except this report and the receipt dir, no git/jj command, no
pacman (all transactions paused), no sudo, no mount outside nothing (no namespace used), no tool
installed (python3 3.14.8 already present; `python3 -V`). Scratch
`/fast/scratch/hyaku/tsukuroi-r39/C2CritTO3` removed at the end; receipts in
`.ufo/waves/round-39/w1/C2CritTO3/`.

## Provenance

- Capture: `.ufo/waves/round-39/frozen/txcapture/`. `sha256sum -c MANIFEST.sha256` → all four members
  `OK`; `sha256sum MANIFEST.sha256` = `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4`
  — identical to the pin in `corpus/knowledge/pacman-transaction-order-r39.md:3`. `pacman.log` itself:
  `0845c1df31fcccd1b629f3b5c8190c037a572bbfbd6d9e11f81be635b1a4fc67`, 3254 lines (`wc -l`).
- Source spot-checks against `.ufo/waves/round-39/frozen/src/{add.c,remove.c}` (line numbers below).
- Local package database read (read-only) as the independent oracle for "which package's `install` file
  could have printed this": `/var/lib/pacman/local/<pkg>/install`, 51 files present, `<pkg>/desc`
  `%NAME%`/`%VERSION%` used to pair name and version exactly (version numbers contain `:`/`-`, so the
  directory name must not be split).

## Method

Parsed the log into 86 `[PACMAN] Running '…'` windows → 60 windows each holding exactly one
`transaction started`/`transaction completed` pair and 26 windows holding none; 0 `interrupted`/`failed`.
Inside each commit phase a **block** is a package line (`installed|upgraded|reinstalled|removed`,
`add.c:618,626,630`; `remove.c:722`) plus every following line up to the next package line. A block's
`out` lines are `[ALPM-SCRIPTLET]` lines; its `other` lines are anything else (only `[ALPM] warning:` in
practice). Scripts and machine-readable dumps: `w1/C2CritTO3/{parse,analyze,attr,postcheck,siltest,verbaware,to7check,final}.py`,
`blocks.json`, `phases.json`, `attr.json`, `stats.txt`, `adjacency.txt`.

Structural counts (`final.py`, `stats.txt`): 3254 log lines, 2288 package event lines (1437 `installed`,
821 `upgraded`, 28 `removed`, 2 `reinstalled`), 441 `[ALPM-SCRIPTLET]` lines of which **189 lie inside a
commit phase** and 252 outside — this independently reproduces TO8's host count (441 total, 252 outside
the commit phases).

## TO3 — "post-scriptlet output follows its own line, precedes the next package's line"

Result: **holds on all observed instances; no counterexample.**

1. Of 2288 blocks, 29 carry scriptlet output, 189 lines total. For **29/29** the first output line is
   the very next line after the package line (`adjacency.txt`), and **0/29** output runs are interrupted
   by any other log line (`final.py`: "blocks whose output run is interrupted by other log lines: 0").
   So the output both starts immediately after its own line and ends before the next package line.
2. **0** `[ALPM] running '<hook>'` lines fall inside any commit phase (`final.py`), so no scriptlet line
   in a commit phase is hook output re-labelled — the ALPM-SCRIPTLET lines in the commit are scriptlet
   output only.
3. Content attribution against the owner's own `install` file at the *matched* version:
   **53 of 189** lines are verbatim substrings of the block owner's `install` file, and
   **0** are verbatim substrings of some other package's file (i.e. no line whose literal text belongs to
   a different package than the block owner). Examples: `pacman.log:2061-2064` — `installed
   java-runtime-common (3-6)` then the three `echo` lines of its `post_install`
   (`/var/lib/pacman/local/java-runtime-common-3-6/install:9-11`); `pacman.log:123-124` — `installed
   systemd (261.1-1)` then `Initializing machine ID from random generator.`, which is
   `systemd-machine-id-setup` called by `post_install` (`/var/lib/pacman/local/systemd-262-1/install:28`);
   `pacman.log:1441-1450` — the `tar` `post_upgrade` notice (`tar-1.35-5/install`).
   The remaining 136 lines are helper output, and every one sits in a block whose `install` file calls
   that helper: `Creating group/user …` 68, `Created symlink …` 10 (systemd `systemctl`/`systemd-sysusers`;
   `systemd-262-1/install:20,33`), `gpg:`/`==>`/`-> Locally signed` 45 (archlinux-keyring/omarchy-keyring/
   chatgpt-bin; `chatgpt-bin-…/install` calls `pacman-key --init/--add/--lsign-key`), 8 blank lines inside
   multi-line banners, 3 `::` lines from `asdcontrol 1:0.6.0-1` whose current db entry (1:0.6.0-2) shipped
   no `install` file, 1 `java-runtime-common` line whose shell quoting breaks verbatim matching.
4. Three near-counterexamples were run down and all resolve under `add.c:642`
   (`is_upgrade ? "post_upgrade" : "post_install"`), i.e. they confirm rather than damage TO3:
   - `pacman.log:2277` `upgraded ufw-docker (251123-1 -> 251123-2)` with **no** output, although the
     current `install` file's `post_install` starts with an unconditional `echo`: ufw-docker defines
     `post_install` only, so an upgrade runs `post_upgrade` (absent) and is silent.
   - `pacman.log:2510` `installed glusterfs (1:11.2-2)` with no output, although `glusterfs-1:11.2-2/install`
     is an unconditional `post_upgrade` echo: an install runs `post_install` (absent). glusterfs was
     never upgraded in the capture, so that echo never had an occasion.
   - `pacman.log:2664` `upgraded cups (2:2.4.19-1 -> 2:2.4.20-1)` with no output, although
     `cups-2:2.4.20-1/install:8` defines `post_upgrade`: both of its echo branches are gated
     `[[ $(vercmp … $2) = 1 ]]` and false for `$2 = 2:2.4.19-1`.
   A verb-aware re-test (choose `post_install` for `installed`, `post_upgrade` for `upgraded`) of every
   block whose `(name, target version)` exists in the current db: 13 output blocks, all 13 with a `post_*`
   function; the 3 blocks whose relevant post function's first statement is an unconditional
   `echo`/`printf`/`cat` all produced output; **0 contradictions** (`verbaware.py`).
5. Independent probe of the *internal* order (files written before the log line): all 7 `[ALPM] warning:`
   lines precede the package line whose extraction emitted them — `5`→`installed filesystem` (6),
   `249`→`installed amd-ucode` (250), `1427` (`/etc/locale.gen`)→`upgraded glibc` (1428),
   `1645-1646` (`/etc/tpm2-tss/…`)→`upgraded tpm2-tss` (1647), `1716`→`upgraded amd-ucode` (1717),
   `2547`→`upgraded amd-ucode` (2548). None appears after its own package's line, matching
   `add.c:560` (`extract_single_file`, where the warning is emitted at `add.c:191`) → `add.c:599`
   (`_alpm_local_db_write`) → `add.c:630` (log line).
6. **Finding (gap, not falsification): the pre half has zero host instances.** No `[ALPM-SCRIPTLET]`
   line in any commit phase precedes the first package line of that phase (`analyze.py`: "events before
   first package in phase: []"), so nothing in the capture is pre-scriptlet output. The plausible
   printers are all gated off: `limine`'s `pre_upgrade` echo needs `$2 < 12.0.0-1` and the two upgrades
   were `12.5.1-1 → 12.8.0-1` (`pacman.log:1882`) and `12.8.0-1 → 12.9.3-1` (`pacman.log:2851`);
   `java-runtime-common`'s `pre_upgrade` is `grep`-gated and it was only installed (`pacman.log:2061`);
   `ca-certificates-utils` (the only other unconditional-print `pre_upgrade`) was installed, not upgraded
   (`pacman.log:73`); `grep -c` for the literal pre texts (`limine >= 12`, `_JAVA_AWT_WM_NONREPARENTING`,
   `has been renamed to`) in `pacman.log` returns nothing.
   Worse for any positional argument: a pre-scriptlet's output for package *k* is logged after package
   *k−1*'s line, i.e. it lands in *k−1*'s block. The capture therefore cannot attribute a pre-scriptlet's
   output at all; TO3's clause "a pre-scriptlet's output precedes the line" is true by source
   (`add.c:466-474` runs before `add.c:485/503`), but no line of this log evidences it, and block
   adjacency would misattribute it. This is a precision defect in the host cell, not in the rule.
7. Related consequence of block adjacency, observed but harmless here: the 7 warning lines of step 5 (in
   6 blocks) land in the *previous* package's block (`iana-etc` 4, `btrfs-progs` 248, `iana-etc` 1426, `libksba` 1644,
   `aether` 1715, `alsa-card-profiles` 2546 — `blocks.json`), because extraction of package *k* runs
   between *k−1*'s log line and *k*'s. Any future check that asserts "everything in a block belongs to
   that package" would break on warnings and on a printing `pre_*`; it does not break on this capture's
   scriptlet lines.

## TO7 — `removed` vs upgrades

Result: **holds; no counterexample.**

1. 28 `removed` lines, all inside 7 commit phases, all removal-only commands:
   phases 2122–2124 `pacman -R hopper` (1 line), 2389–2394 `-Rns quickshell` (4), 2456–2459 `-Rns
   electron39 mbedtls` (2), 3128–3130 `-R -s -u go` (1), 3134–3149 `-Rns btrbk elephant-*-debug` (14),
   3154–3158 `-Rns gst-plugin-gtk hyprwayland-scanner webp-pixbuf-loader` (3), 3249–3253 `-Rns …-debug`
   (3); 1+4+2+1+14+3+3 = 28.
2. **0 of 60** commit phases contain both a `removed` line and an `installed`/`upgraded`/`reinstalled`
   line (`analyze.py`/`to7check.py`); no phase has two events for the same package name. So no upgraded
   package logs `removed` in the same transaction. This also re-confirms TO2's host count (0 of 60) at
   phase level.
3. Version reconciliation: for **28/28** `removed` lines the removed version equals the version last
   logged as installed/upgraded-to (`to7check.py`: "mismatches: 0"). The three names that appear both
   removed and upgraded do so in *different* transactions, each with the matching version:
   `electron39` upgraded to `39.8.10-2` at 1749 → removed `39.8.10-2` at 2458; `gst-plugin-gtk`
   upgraded to `1.28.8-1` at 2714 → removed `1.28.8-1` at 3157; `mbedtls` upgraded to `4.2.0-1` at 1905
   (its successor `mbedtls3 3.6.7-1` installed at 1912) → removed `4.2.0-1` at 2457. No `removed` line
   ever names an old-half version.
4. Source gating matches: `remove.c:698` `if(newpkg)` → only debug log, no `pre_remove`; `:706-713`
   `pre_remove` runs only when `!newpkg`; `:716-719` file removal; `:721-724` `removed` only when
   `!newpkg`; `:726-733` `post_remove` only when `!newpkg`. The upgrade path enters with `newpkg` set
   (`add.c:485` `_alpm_remove_single_package(handle, oldpkg, newpkg, 0, 0)`), so the old half is removed
   with no scriptlet and no `removed` line — exactly TO7's second clause.
5. **Finding (gap, not falsification): TO7's first clause has zero host instances.** All 7 removal
   phases contain **0** `[ALPM-SCRIPTLET]` lines and 0 `running '<hook>'` lines inside the commit
   (`final.py`; `analyze.py` "in-commit event kinds" lists only installed/upgraded/removed/reinstalled/
   warning/SCRIPTLET, and the removal phases contribute no SCRIPTLET). None of the removed packages
   printed from `pre_remove`/`post_remove`, so `pre_remove` → files → `removed` → `post_remove` is
   evidenced only by source (`remove.c:706-733`), not by the log. Removal windows do show the hook
   phases outside the commit in the expected places, e.g. `pacman.log:2121` `running
   '10-limine-snapper-lock.hook'` before `transaction started` (2122), and `pacman.log:2125`
   `running '30-update-mime-database.hook'` after `transaction completed` (2124).

## Limits of this review

- `/mnt/var/lib/pacman/local` does not exist (`ls: cannot access …: No such file or directory`), so the
  chroot transaction at `pacman.log:4-250` (phase 0, 157 package blocks incl. the cited `systemd 261.1-1`) cannot
  be verified against the `install` files that actually ran; its block is consistent by content only.
- Only the 51 currently installed packages carry `install` files (1410 db entries), so verbatim
  attribution is possible for 53 of 189 lines and for 13 of the 29 output blocks at exact version; older versions'
  scriptlets (e.g. `cups 2:2.4.19-1`) are gone. The 136 helper-output lines are attributed by the helper
  their owner calls, not by literal string.
- The declared kill rule stands: `tools/check-transaction-order-r39.py` checks that the quote is at the
  cited lines, not that the rule text is true. This report judges the truth of two rows empirically and
  against source; it did not run that counter (out of scope for this item, and it is the L1's instrument).
- Not done: no live transaction reproduced (no pacman run, transactions paused host-wide); no namespace
  fixture; no hook-phase re-derivation (HO rows are another seat's item).

## Optional tightening (proposed text, host column of TO3)

Replacing the truncated tail of TO3's host cell
(`… pacman.log:123-124 …; a pre-scriptlet's output precedes the line`) with:

> A package's post-scriptlet output follows its own `installed`/`upgraded` line: pacman.log:123-124
> `installed systemd (261.1-1)` then `[ALPM-SCRIPTLET] Initializing machine ID from random generator.`;
> 29 of 2288 commit-phase blocks in the capture carry scriptlet output (189 lines) and every one starts
> on the line after its package's and ends before the next package's. The capture holds **no**
> pre-scriptlet output, so the log cannot demonstrate the pre half by position: a pre-scriptlet's output
> for package *k* is logged after package *k−1*'s line; the pre half rests on add.c:466-474 alone.

## TO rows judged

TO3: holds — add.c:630
TO7: holds — remove.c:722
