VERDICT: defect-found

Seat C2CritEX4, item C2-22, attack on EX4 of `corpus/knowledge/pacman-exec-environment-r40.md` (lane master
`f951f288483c1af0cef4afd458488b84cf7a2165`; entry row at `:24`, derived item at `:35`, boundaries `:38-47`;
authored at `bf23805`). Read-only review: the lane, its Git index and jj state were not touched; all variants ran
in a scratch clone that has been removed. No tool was installed (nothing needed).

## 1. Answers to the four questions

**(a) Is SCRIPTLET_SHELL the interpreter for every install scriptlet, or can a package override it?**
Yes for every invocation of `_alpm_runscriptlet`, and a package has no override:
- `trans.c:357-358` `strcpy(arg0, SCRIPTLET_SHELL); strcpy(arg1, "-c");` and `trans.c:410`
  `_alpm_run_chroot(handle, SCRIPTLET_SHELL, argv, NULL, NULL)` — the same constant is the exec path and `argv[0]`,
  so both legs (copy from the local DB, `is_archive == 0`; extract from the package file, `is_archive == 1`) and
  every phase go through it.
- Build-time only: `pacman.conf(5)` has 0 occurrences of "scriptlet" (`zcat ... | grep -c -i scriptlet` → 0);
  `pacman(8)` offers `--noscriptlet` only; `/usr/include/alpm.h` has 0 occurrences of "shell"; `strings /usr/bin/pacman`
  has 0 occurrences of "ScriptletShell".
- The `.INSTALL` is **sourced** (`. %s`), not executed, so a shebang in it is inert. Measured with the exact command
  shape in scratch: a file whose first line is `#!/bin/false`, mode 0644, still defined and ran all six functions
  (`host-experiments.txt` §A).

The wording "every install scriptlet" is nonetheless imprecise in scope: a run is skipped by
`ALPM_TRANS_FLAG_NOSCRIPTLET` (`pacman --noscriptlet`), and by the two short-circuits `trans.c:351`
(`!is_archive && !grep(filepath, script)`) and `trans.c:392` (`is_archive && !grep(scriptfn, script)`), i.e. when
the phase function is absent from the file. Separately, the path is resolved **inside** the installation root after
the optional chroot (`util.c:677-687`), so a `--root` target without `/usr/bin/bash` fails the scriptlet at
`execv` with `call to execv failed` (`util.c:698-700`). None of these is an override of the chosen interpreter.

**(b) Does `. <scriptlet>; <function> <new> [<old>]` match `trans.c:400-406` exactly, and which arguments for
`pre_install`, `post_upgrade`, `pre_remove`?**
The *template* matches exactly — `trans.c:401-402` `. %s; %s %s %s` over `scriptpath, script, ver, oldver` and
`:404-405` `. %s; %s %s`; `<scriptlet>` is the in-chroot path from EX5, not the package path. The *placeholder
names* do not: `<new version>` is false for the removal phases.
- Measured, exact form, six phases (`host-experiments.txt` §A): `pre_install 1=[2.0-1] 2=[]`,
  `post_install 1=[2.0-1] 2=[]`, `pre_upgrade 1=[2.0-1] 2=[1.0-1]`, `post_upgrade 1=[2.0-1] 2=[1.0-1]`,
  `pre_remove 1=[1.0-1] 2=[]`, `post_remove 1=[1.0-1] 2=[]`.
- Host documentation says the same: `PKGBUILD(5)` (decompressed) `:544` "Run right before files are removed. One
  argument is passed: old package full version string." and `:549` for `post_remove`; `:524`/`:529` "new package
  full version string" for the install pair; `:534`/`:539` "new package full version string, old package full
  version string". `/usr/share/pacman/proto.install:27` and `:32` say `arg 1: the old package version` for the
  removal pair.
- Caller: `corpus/knowledge/pacman-transaction-order-r39.md:30` (TO7) quotes `remove.c:699-733`
  `_alpm_runscriptlet(handle, scriptlet, "pre_remove", pkgver, NULL, 0)` — `ver` is the removed package's version
  and `oldver` is NULL. `trans.c`'s own parameters are named `ver` and `oldver`, so `<version> [<old version>]` is
  the faithful template.
- Also measured: file-level scriptlet code sees no positional parameters (`count=0`); the versions exist only
  inside the called function. The template is therefore correct only if read as the function's arguments.

**(c) Is "bash-only syntax in a scriptlet depends on this packaging choice" a fair consequence?**
Not for this build, and it locates the real consequence in the wrong place.
- `/bin/sh` on this root is a symlink to bash (`ls -l /bin/sh` → `/bin/sh -> bash`), and bash invoked as `sh` runs
  in POSIX mode (`set -o | grep posix` → `on`) yet still parses bash syntax: measured
  `x=(1 2); [[ 1 == 1 ]]` → `array+[[ ok] 2` under `/bin/sh`. So at the upstream default `/bin/sh` a bash-only
  scriptlet would still parse on Arch; the flag does not gate bashisms here.
- What the flag actually selects is POSIX mode — and that is what makes EX3 load-bearing. Measured: bash
  non-interactive honours `BASH_ENV` (`BASH_ENV=... /usr/bin/bash -c 'echo body'` → `BASHENV-RAN body`), while
  `bash --posix` and `/bin/sh` do not (`body` only). Under the upstream default the `unsetenv("BASH_ENV")` at
  `util.c:694` would be inert; under `/usr/bin/bash` it is required. Other measured POSIX-mode difference:
  `local` outside a function is rejected under `/bin/sh`.
- The sentence is fair only as a cross-distro statement (a build whose `/bin/sh` is dash), which is outside what
  this entry documents for this host.
- No packaging document carries the interpreter either way: `PKGBUILD(5)` has **0** occurrences of "shell" in the
  whole page; `/usr/share/makepkg` has 0 "scriptlet" references; `/usr/bin/makepkg:710` merely collects
  `install/.INSTALL` into the package (`for i in 'changelog/.CHANGELOG' 'install/.INSTALL'`), and its only install
  lint checks that the file exists (`/usr/share/makepkg/lint_pkgbuild/install.sh:2-4`). So the interpreter is a
  build option (S219:17, S220:113-115) plus the binary's string, not a packaging-documented contract, and the
  consequence clause should not read as if packaging settled it.

**(d) Does makepkg / PKGBUILD(5) state the scriptlet shell?**
No. `PKGBUILD(5)` states the *arguments* (five lines quoted above) and nothing about the interpreter; makepkg
never runs or parses the install file at build time. The corpus's only warrant for the consequence is the meson
option plus `strings`; that is enough for the value `/usr/bin/bash`, not for the causal claim as written.

## 2. Counterexamples (strongest available from local evidence)

1. **`pre_remove` has no "new version".** Measured `pre_remove 1=[1.0-1] 2=[]` and `post_remove 1=[1.0-1] 2=[]`
   under the exact `. <file>; <fn> <arg>` form; `PKGBUILD(5):544,:549` and `proto.install:27,:32` call that one
   argument the *old* package version; r39 TO7 passes `pkgver, NULL`. A reader following EX4's `<new version>`
   writes `$1` as "the new version" in `pre_remove`, where no new package exists.
2. **bashisms survive `/bin/sh` on this root.** `/bin/sh -> bash`, arrays and `[[ ]]` parse in POSIX mode, so the
   stated dependency of bash-only syntax on the packaging flag does not hold for the build under review; what the
   flag changes is POSIX mode, which is precisely why EX3's `BASH_ENV` removal matters (bash reads `BASH_ENV`,
   `bash --posix` and `/bin/sh` do not — both directions measured).
3. **Scope:** "every install scriptlet" ignores `ALPM_TRANS_FLAG_NOSCRIPTLET` and the two `grep` short-circuits
   (`trans.c:351`, `:392`), and the interpreter is looked up inside the target root (`util.c:698-700`), which the
   row does not say.

## 3. What survives attack

- EX4's value `/usr/bin/bash` and its provenance: `PKGBUILD:113-115` (the flag itself is on line 115; the cited
  range contains it), `meson_options.txt:17` default `/bin/sh`, `trans.c:357-358`, `:400-406`, `:410`.
- The host cell: `strings /usr/lib/libalpm.so.16.0.1 | grep -n /usr/bin/bash` → `1277:/usr/bin/bash` (index
  matches), and `strings ... | grep -c /bin/sh` → `0`; libalpm sha256 `1bc59ef4…` matches `capture-meta.txt`.
  One evidence nit: the negative half ("lacks `/bin/sh`") has no witness inside S225, a two-line filtered dump;
  it holds on the binary. Optional: add the `grep -c` recheck to the entry's `recheck:` line.
- No duplicate authority or identity change is introduced by the row; hooks are correctly outside it — hook
  `Exec` commands are exec'd from the wordsplit argv with no shell (`hook.c:525`, `:528` pass `hook->cmd[0]`), so
  "bash-only syntax" would in any case be a scriptlet-only statement.

## 4. Impacted axes

| axis | impact |
|---|---|
| C2 depth — rule fidelity | EX4 rule cell carries one false placeholder (`<new version>`) for two of six phases |
| C2 depth — consequence | the `BASH_ENV`/POSIX-mode coupling between EX4 and EX3 is missing and the stated consequence is inverted for this root |
| C2 provenance | interpreter has no packaging-document warrant (PKGBUILD(5) silent); the consequence should cite the build option, not "this packaging choice" |
| C2 scope | skip conditions (`NOSCRIPTLET`, absent function) and root-resolved exec path absent |
| counter | correction verified counter-green; none of the frozen gate inputs (value cell, tokens, quote, host cell) is weakened |

## 5. Smallest safe correction (tested)

Applied to a scratch clone of the lane (`git clone -q --shared`, toplevel-verified, fixture identity), committed as
`96fd45d6fe33dbd9ea1c8ace4551d0df7229b7a3` on top of `f951f28`, and scored with the frozen counter
`tools/check-exec-environment-r40.py --repo <clone> --revision 96fd45d --branch master`:
`result PASS, exit 0, rules_verified 8, counts_ok 2, source_ok 1, novelty_base_hits 0`, `EX4: verified true,
reasons []` (`variant-counter.json`). Full patch in `variant.diff`.

Replacement for the EX4 rule cell (value, source and host cells unchanged):

> Arch builds pacman with `-Dscriptlet-shell=/usr/bin/bash`, so every install, upgrade and removal scriptlet that
> libalpm runs starts as `/usr/bin/bash -c '. <scriptlet>; <function> <version> [<old version>]'` through
> `_alpm_run_chroot`; the path is fixed at build time by the packaging and the `.INSTALL` file is sourced, so a
> shebang in it stays inert; `<version>` is the caller's `ver`: the new full version for `pre_install`/`post_install`,
> new then old for `pre_upgrade`/`post_upgrade`, the removed package's version for `pre_remove`/`post_remove`
> (TO4, TO7; PKGBUILD(5) 520-549); the upstream build default is `/bin/sh` (S219 meson_options.txt:17), which this
> root links to bash, so the flag selects POSIX mode (making the `BASH_ENV` removal of EX3 load-bearing) rather than
> bash-only syntax support

Derived item `:35` replacement:

> 4. Scriptlets: `/usr/bin/bash` on Arch, in the non-POSIX mode that makes the `BASH_ENV` removal of item 1
>    necessary, sourced from a private directory under `<root>/tmp` that is removed afterwards (EX4, EX5).

New Boundaries bullet (after `:43-44`):

> - EX4 describes a scriptlet that runs: `ALPM_TRANS_FLAG_NOSCRIPTLET` (`pacman --noscriptlet`) skips it, and a
>   `.INSTALL` that does not carry the phase function short-circuits before the source (trans.c:351, :392). The
>   interpreter path is resolved inside the installation root after the optional chroot, so a `--root` target whose
>   `/usr/bin/bash` is absent fails the scriptlet with `call to execv failed` (util.c:698-700). The build option is
>   the only statement of the interpreter (S219, S220): the host `PKGBUILD(5)` §INSTALL/UPGRADE/REMOVE SCRIPTING
>   (decompressed lines 514-550) gives the arguments per phase, `makepkg` copies `install/.INSTALL` into the package
>   (makepkg:710) without naming a shell, and `pacman.conf(5)` has no scriptlet key (`pacman(8)`: `--noscriptlet`
>   only).

Why this is the smallest safe form: it changes only the rule cell, one derived bullet and one boundaries bullet;
it keeps every frozen gate token (`/usr/bin/bash`, `/bin/sh`, `-c`), the derived value cell `/usr/bin/bash`, the
PKGBUILD `:113-115` quote, the S-id set and the EX4 host cell, adds no negation word and no self-quote, and it
introduces no new authority — `PKGBUILD(5)` and TO4/TO7 are host/corpus documents that already exist.

Optional addendum (not needed to pass, orthogonal to this item): the version strings are interpolated into the
`-c` string unquoted (`trans.c:401-405`), so they are shell words rather than bash argv; for built packages this is
bounded by `lint_pkgbuild/pkgver.sh:41` ("not allowed to contain colons, forward slashes, hyphens or whitespace"),
a hand-built package being outside that bound.

## 6. What I did not do

Did not run a real pacman transaction (transactions are paused on this host), did not execute any libalpm code path
beyond the reproduced `bash -c` command shape, did not run the C1 census or any other lane counter, did not edit,
stage, commit or clean anything in the lane, did not read or write `/home/vgpnk/Projects/shokuknow`, did not touch
the host beyond read-only `strings`/man-page reads and scratch-filesystem `bash` runs under
`/fast/scratch/hyaku/tsukuroi-r40/C2CritEX4` (removed; receipts copied to this seat directory).

Receipts: `host-experiments.txt` (six-phase argument run, POSIX/`BASH_ENV` measurements, `/bin/sh` symlink, libalpm
strings), `doc-evidence.txt` (PKGBUILD(5) 514-550, proto.install, makepkg:710, absence checks), `variant.diff`,
`variant-counter.json`.
