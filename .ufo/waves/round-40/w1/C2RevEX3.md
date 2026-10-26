VERDICT: supports

Item C2-EX3 — row EX3 of `corpus/knowledge/pacman-exec-environment-r40.md` judged against the pinned source util.c:688-698.

**Row verdict: `holds`.** Every clause of the rule cell is stated by the pinned source at the cited lines; the source-cell quote is verbatim; the value and host cells do not overstate the source.

Judged file identity: `corpus/knowledge/pacman-exec-environment-r40.md` blob `e7a1ea737795f19ee3a452eb39bb933d985c6506` equals `f951f288483c1af0cef4afd458488b84cf7a2165:corpus/knowledge/pacman-exec-environment-r40.md` (`git rev-parse` + `git ls-files -s`, working tree clean); the EX3 row is line 23 of the file.

## 1. Independent re-open of upstream sources

Fetched 2026-10-26T07:16:18Z–2026-10-26T07:16:22Z (receipts `fetch-start.txt`/`fetch-end.txt` in the seat receipt dir):

- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/util.c
- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/hook.c
- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/trans.c
- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/alpm-hooks.5.asciidoc
- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/meson_options.txt
- https://gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/raw/7.1.0.r9.g54d9411-3/PKGBUILD
- extra, for the two packaging patches the entry's Boundaries name: `.../raw/7.1.0.r9.g54d9411-3/0001-libalpm-invalidate-curl-data-in-child.patch` and `.../0002-libalpm-use-curl-s-effective-url-without-authenticat.patch`

Hash check on all six pinned files: fresh sha256 equals `.ufo/waves/round-40/frozen/src/SHA256SUMS` line for line (util.c `381618b6054859ec76807956328b78b330237273bebe10022a559b243cb5bdd2`); `cd .ufo/waves/round-40/frozen/src && sha256sum -c SHA256SUMS` → `PKGBUILD: OK`, `alpm-hooks.5.asciidoc: OK`, `hook.c: OK`, `meson_options.txt: OK`, `trans.c: OK`, `util.c: OK` (6× OK); `cmp frozen/src/util.c <fresh util.c>` → byte-identical. Receipt: `receipt-sha256.txt`.

## 2. Clause-by-clause judgment of the rule cell

Rule cell (line 23): "Before `execv` the child sets `SHLVL` to 1 when the variable is unset (an inherited value is kept), removes `BASH_ENV` from its environment, sets umask 0022 and resets signal handlers; every other variable of the calling pacman process passes through to the command unchanged"

| # | clause | pinned source | verdict |
|---|---|---|---|
| 1 | runs in the child, before `execv` | util.c:660 `if(pid == 0) {` / :661 `/* this code runs for the child only (the actual chroot/exec) */`; the env block :688-698 ends at `execv(cmd, argv);` :698 | holds |
| 2 | `SHLVL`→1 only when unset; inherited value kept | util.c:692 `setenv("SHLVL", "1", 0);` — third argument 0 = do not overwrite an existing value; intent comment :688-691 ("set SHLVL before running to indicate that it's a child shell") | holds |
| 3 | removes `BASH_ENV` | util.c:694 `unsetenv("BASH_ENV");` | holds |
| 4 | umask 0022 | util.c:695 `umask(0022);` (octal literal 0022) | holds |
| 5 | resets signal handlers | util.c:696 `_alpm_reset_signals();`; definition util.c:579-601: `struct sigaction def = { .sa_handler = SIG_DFL };` then `sigaction(*i, &def, NULL)` over the POSIX signal list | holds |
| 6 | every other variable of the calling pacman process passes through unchanged | child branch :660-702 read line by line (660-670, 671-675, 676-686, 687-693, 689-703): the only environment operations in the fetched libalpm sources are :692/:694 (`grep -nE 'setenv|unsetenv|putenv|clearenv|\benviron\b'` over util.c, hook.c, trans.c → only util.c:692 and util.c:694); `execv` (not `execve`) at :698 passes the caller's `environ` | holds |

## 3. Quote and citation exactness

- Source-cell quote “/* bash sources $BASH_ENV when run non-interactively */” is verbatim at util.c:693, inside the cited range 688-698. ✓
- Parenthetical line cites: `setenv("SHLVL", "1", 0)` :692 ✓, `unsetenv("BASH_ENV")` :694 ✓, `umask(0022)` :695 ✓, `execv` :698 ✓ — all exact.
- S221 maps to libalpm util.c at 54d9411 with snapshot sha256 `381618b6…` (`corpus/SOURCES.md:230`; SOURCES.md blob `6b2d158116e55d813d496f9f09bb1e8da6a1a9d4` at f951f288, tree clean). ✓

## 4. Value and host cells

- Value cell `SHLVL=1 BASH_ENV=unset umask=0022`: all three tokens are source-derived (:692/:694/:695). Terse per the entry's value-cell convention; the only-if-unset nuance is carried by the rule cell. No overstatement.
- Host clause "Files a hook or scriptlet creates get mode bits under umask 0022 whatever the operator's shell umask": mechanism stated at :695 — the child's umask is set after fork, so it is independent of the invoking shell's umask; applies to hook `Exec` commands and scriptlets alike (both run through `_alpm_run_chroot`, EX1/EX4). Unobserved on this host — consistent with the entry's own Boundaries ("EX1–EX3 and EX5 have no host instance in the capture").
- Host clause "variables exported in the shell that ran pacman (and kept by sudo) reach the command": mechanism stated at :698 (execv passes environ; only SHLVL/BASH_ENV touched). "(and kept by sudo)" reads restrictive/conditional, and the Boundaries declare sudo's `env_reset` outside this entry — hedged, no overstatement.

## 5. Extra checks (Boundaries' named packaging patches; hostcap)

- `0001-libalpm-invalidate-curl-data-in-child.patch` (fetched from the packaging tag; sha256 `9a734e5d75be603d58aa92e8d29a15466b3ac2af6b7d6f6728dd5c3e5ed8758d`) touches `lib/libalpm/util.c` at hunk `@@ -673,6 +673,11 @@ int _alpm_run_chroot(...)`: it inserts `#ifdef HAVE_LIBCURL` / `/* invalidate the curl data - we must not touch it in child */` / `handle->curlm = NULL;` / `#endif` in the child branch after the cwdfd close (old :671-675), before the chroot block. It assigns a handle field — no environment, umask or signal operation — so every EX3 clause also holds for the installed build; in the installed build the block shifts +5 lines (upstream :692 → installed :697), and the row's citations stay pinned to the upstream snapshot (S221), which the entry's Boundaries declare ("their file scope is a wave item, not assumed here").
- `0002-libalpm-use-curl-s-effective-url-without-authenticat.patch` (sha256 `021893dd44ec23251cfc0f2b81c12d832927ea60095d4d2956d9760e8bbfaa58`) touches only `lib/libalpm/dload.c`.
- hostcap `libalpm-shell-strings.txt` is a 2-line filtered extract (`1263:/usr/bin/ldconfig`, `1277:/usr/bin/bash`), not a full strings dump; the absence of `SHLVL`/`BASH_ENV` there is a filter artifact and is neither evidence for nor against EX3 (consistent with Boundaries: no host instance for EX1–EX3/EX5).

## 6. Observation (non-blocking; verdict unaffected)

The source cell's parenthetical lists four actions of the cited range but omits `_alpm_reset_signals()` :696, which the rule cell claims. Optional append-only annotation (not required for the `holds` verdict) — in the source cell replace

    `umask(0022)` :695, `execv` :698)

with

    `umask(0022)` :695, `_alpm_reset_signals()` :696, `execv` :698)

## 7. Not done

- Did not run `tools/check-exec-environment-r40.py` (the counter is another seat's item; my item is the source judgment of the row).
- No host observation of EX3's behavior (pacman transactions are paused host-wide; the entry's Boundaries declare EX1–EX3/EX5 without host instance) — the host cell remains a mechanism-derived prediction.
- Did not audit `src/pacman` (frontend) environ use — outside the row's claim, which is about the calling process's environment passing through `_alpm_run_chroot`; the libalpm side is fully covered.
- No tools installed or upgraded (none needed).

Receipts: `.ufo/waves/round-40/w1/C2RevEX3/` (fetched sources, two patches, fetch timestamps, `receipt-sha256.txt`). Scratch `/fast/scratch/hyaku/tsukuroi-r40/C2RevEX3` removed after the copy.
