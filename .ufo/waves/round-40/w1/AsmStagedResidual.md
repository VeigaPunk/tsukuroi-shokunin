VERDICT: defect-found

# F-2 — the four residual mechanism propositions (`pacman-hook-timing-r25.md:41-51`)

Seat `AsmStagedResidual` (leaf), item F-2. Candidate
`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/pacman-hook-timing-r25.md`,
sha256 `e18c146e733d3cab4bcc82c2ba30b9a571791ec132f7988cd93481b079f09324` (recomputed; matches the dispatch
hash) — the same bytes round 38 refused and round 39 deferred at `corpus/lessons/round-39.md:56`.

Judged surface: exactly the four propositions that row names — `:42-43` (`NeedsTargets`→stdin), `:44-45`
(`.pacnew` trigger target), `:47-48` (scriptlet cwd and "must be absolute"), `:50-51` (global interpreter).
Not judged here: the `AbortOnFail` / PostTransaction sentences on `:41-45`, and the Chinese-rendering section.

Ground: `corpus/knowledge/pacman-exec-environment-r40.md` (commit `bf23805`, EX1-EX8 at `:21-28`) read
against the pinned snapshots `.ufo/waves/round-40/frozen/src/` — `sha256sum -c SHA256SUMS` → all six OK —
plus `add.c` from the round-39 snapshot (`fd313629…`, equal to S213's declared hash) and the own-work
capture `.ufo/waves/round-40/frozen/hostcap/` (`sha256sum -c MANIFEST.sha256` → 3 OK). Receipts with all
commands and outputs: `AsmStagedResidual/receipts.txt` in this directory.

## 1. Judgments

| # | staged proposition (line) | judgment | re-grounded by | reason in one line |
|---|---|---|---|---|
| P1 | "`NeedsTargets` passes the matched trigger targets to the hook on **stdin**" (`:42-43`) | **admit** | EX6 — S223 `hook.c:469-490`, `:519-526`; doc S224 `:91-93` | True as written; the short form is the man page's own wording. Carry EX6's completion (union over triggers, `strcmp` sort, de-duplication, one per line, EOF without `NeedsTargets`) |
| P2 | "A file extracted with the `.pacnew` extension triggers the hook on the **original** file name" (`:44-45`) | **admit** | EX8 — S223 `hook.c:265-278`, `:305-339` | True: the match input is the package file list, never the on-disk name, and `hook.c` never consults NoUpgrade. One completion required: which acquisition set the name lands in (Install / Upgrade / Remove) |
| P3 | "`.INSTALL` functions execute in the system root (`/`), so every path inside them must be absolute" (`:47-48`) | **admit-with-correction** | EX1 — S221 `util.c:628`, `:679`, `:683`; EX5 — S222 `trans.c:361-377`, `:397-401` | The cwd half is right; the inference is **not**. A cwd of `/` makes every path installation-root-relative; a relative path resolves there and names the same file as the absolute form. "System root" is also the target root under `--root`, not the booted `/` |
| P4 | "the shell interpreter is chosen globally by the distribution and cannot be selected per package" (`:50-51`) | **admit** | EX4 — S219 `meson_options.txt:17`, S220 `PKGBUILD:115`, S222 `trans.c:341`, `:357-358`, `:400-406`, S225 | True: `SCRIPTLET_SHELL` is a compile-time option, one value for the whole libalpm. Completion: the file is *sourced*, so its own `#!` is inert; a package may still exec any interpreter inside a function |

Net lane action if these are carried: P1, P2 and P4 need no new prose — the entry already carries them at
EX6, EX8 and EX4 with derived items 3-5 (`entry:34-36`); P2 needs the set mapping added and, if the
man-page caveat sentence is to be quoted, S224's scope cell widened (D3 below). P3 must be carried **only**
in corrected form; the entry today states the mechanism (EX1) and is silent on absoluteness, so the staged
inference would be an import, not a restatement.

## 2. Does "must be absolute" follow from a cwd of `/`? — No

The mechanism, read end to end:

* parent: `chdir(handle->root)` — `util.c:628`;
* child: `chroot(handle->root)` only when the root is not `/` — `util.c:679`;
* child: `chdir("/")` — `util.c:683`;
* child: `execv(cmd, argv)` — `util.c:698`.

So the command always starts with cwd `/` *inside the installation root*. Path resolution of a relative
pathname starts at the cwd; therefore `usr/bin/foo` and `/usr/bin/foo` name the same object inside that root,
in both the `root = /` and the `--root` case. Nothing in `_alpm_run_chroot` or `_alpm_runscriptlet` inspects
or rewrites the paths a scriptlet's functions use, and every other candidate base is eliminated:

* the caller's cwd is discarded (parent `chdir(handle->root)` at `util.c:628`; the child never inherits it);
* the scriptlet's temporary directory is not the cwd — the file is sourced by an absolute path made from the
  temp dir with the root prefix chopped (`trans.c:397-401`);
* `$0` is the shell binary, not the scriptlet (`argv[0]` = `SCRIPTLET_SHELL`, `trans.c:341`, `:357`,
  `:400-406`), so there is no script-relative base either.

What the mechanism does imply is the *opposite* of the staged sentence: every path is
installation-root-relative, and a relative path silently means "from `/` of that root". That is why an
absolute path is the safe convention (and why `--root` transactions still name `/usr/...` correctly), not
because a relative one fails. The lane's own admitted row already says this in its host cell —
`entry:21`, EX1: "A hook or scriptlet that uses relative paths resolves them from `/` on this host". The
staged inference contradicts the row the round-40 entry was built to carry.

One adjacent place where "absolute" *is* practically required, worth not conflating: hook `Exec` commands
also run through `_alpm_run_chroot`, and the child calls `execv` (`util.c:698`), which performs no `PATH`
search. A first word without a slash is resolved as `/`-relative and a bare name therefore lands on `/name`;
that, not the scriptlet cwd, is where absolute `Exec` paths are load-bearing. The host capture's hooks use
`/usr/share/libalpm/scripts/limine-snapper-lock` and `/bin/sh -c ...` for exactly this reason
(`hostcap/hooks-needstargets.tsv`).

## 3. Proposition-by-proposition evidence

### P1 — `NeedsTargets` on stdin: admit (EX6)

* Feed callback: `hook.c:469-490`, one target per line (`buf[len++] = '\n'` at `:476`); the loop advances
  `*pos` and the parent keeps calling it, so the whole list is written.
* Order and de-duplication: `alpm_list_msort(hook->matches, …, strcmp)` and `_alpm_strlist_dedup` at
  `hook.c:519-526` (`:492-506` is the dedup body); the sorted, unique list is passed to `_alpm_run_chroot`
  at `:525-526`.
* Union over triggers: `_alpm_hook_triggered` loops every trigger (`hook.c:427-442`) and each match call
  joins its saved lists into `hook->matches` (`_save_matches`, `:341-349`; package matcher joins at
  `:412-414`). The early `return 1` at `:433-435` fires only when `needs_targets` is unset, so for a
  `NeedsTargets` hook all triggers contribute.
* Target kind: package names for `Type = Package` (`hook.c:371-410`), package-archive paths for
  `Type = Path` (`:265-306`).
* Doc, in S224's declared cell: `alpm-hooks.5.asciidoc:91-93` "Causes the list of matched trigger targets to
  be passed to the running hook on 'stdin'".
* Host: 14 of 69 effective hook files carry `NeedsTargets`
  (`awk -F'\t' 'NR>1{n++; if($3==1)k++} END{print n, k}' hostcap/hooks-needstargets.tsv` → `69 14`).

Nothing in the staged sentence is false. Its completion is exactly EX6, which already states it; derived
item 3 (`entry:34`) is the carried form.

### P2 — `.pacnew` triggers on the original name: admit (EX8), with one completion

* The match input is the file list of the package being added, `pkg->files[f].name` (`hook.c:265-278`).
  The only option consulted is `alpm_option_match_noextract` (`:271`); `grep -ic 'noupgrade' hook.c` → `0`,
  so the extraction outcome for a protected file cannot change what is matched.
* The suffix is attached at extraction, to the listed name: `strcpy(filename + filename_len, ".pacnew")`
  (`add.c:318-323`; pacnew event and the "installed as %s.pacnew" message at `:339-351`). Because matching
  runs on file-list names, the matched name is the pre-suffix one.
* Doc: `alpm-hooks.5.asciidoc:126-128` "When installing or upgrading a file that is extracted with a
  '.pacnew' extension, the original file name is used in triggering the hook."
* **Completion required** (the sentence as written is true of the *name*, but not sufficient to say the
  hook fires): the matched name is placed in the `install`, `upgrade` or `remove` list, and paths present in
  both the old and new file lists are moved to `upgrade` (`hook.c:305-339`, `upgrade = alpm_list_add(upgrade,
  path)` at `:321`); the hook runs only for an `Operation` covering that list (acquisition-set expression
  `:339-341`; `_save_matches` guard `:344-349`). Consequence: on the ordinary upgrade that leaves
  `<name>.pacnew`, the target is an **upgrade** target, so a hook declaring only `Operation = Install` does
  not fire. EX8 and derived item 5 (`entry:36`) omit this; it is a precision gap, not a falsehood.

### P3 — scriptlet cwd and the absoluteness inference: admit-with-correction (EX1, EX5)

* Working directory: `util.c:628`, `:679`, `:683` (see §2). Cwd is `/` for hook `Exec`, install scriptlets
  and `ldconfig` alike (EX1), because all three go through `_alpm_run_chroot`.
* Staging: `<root>/tmp` requested at 01777 when missing, private `tmp/alpm_XXXXXX` via `mkdtemp`
  (`trans.c:361-371`), scriptlet as `.INSTALL` (`:375-377`), sourced by the shell as
  `. <scriptpath>; <function> <ver> [<oldver>]` (`:400-406`), file and directory removed afterwards, both
  failures warned (`:412-420`). `scriptpath` is `scriptfn + strlen(handle->root) - 1`, i.e. an absolute path
  *inside* the chroot (`:397-398`) — libalpm making its own argument absolute is not a requirement on the
  author's paths.
* Correction (exact, for the lane): replace the staged sentence with "`.INSTALL` functions run with working
  directory `/` inside the installation root — the parent changes into that root, the child chroots into it
  only when it is not `/`, then changes to `/` (`util.c:628`, `:679`, `:683`) — and the scriptlet is sourced
  by an absolute path in that root (`trans.c:397-401`). Every path inside a function is therefore
  installation-root-relative: a relative path resolves from that `/` and names the same file as the absolute
  form, and what is ruled out is any other base (the caller's cwd, the scriptlet's temporary directory, or
  `$0`), not relative paths as such."
* Two reasons the staged half-sentence still needs a change beyond dropping the inference: (a) "system root"
  is wrong for `--root` — the chroot target is `handle->root`, so an absolute `/usr/...` in a scriptlet is
  the *target* root's `/usr`, not the booted system's; (b) it omits the staging location that the same
  contract sentence depends on (EX5), which is where the "no other base" argument gets its force.

### P4 — interpreter fixed globally: admit (EX4)

* Build knob: `option('scriptlet-shell', type : 'string', value : '/bin/sh', …)` (`meson_options.txt:17`,
  upstream default); Arch's `build()` passes `-Dscriptlet-shell=/usr/bin/bash` (`PKGBUILD:115`).
* Use: `strcpy(arg0, SCRIPTLET_SHELL); strcpy(arg1, "-c")` and `. <scriptlet>; <fn> <ver>` as `argv[2]`,
  executed by `_alpm_run_chroot(handle, SCRIPTLET_SHELL, argv, NULL, NULL)` (`trans.c:341`, `:357-358`,
  `:400-406`, `:410`). The scriptlet is *sourced* by that shell, so its own `#!` line is never consulted —
  there is no exec of the scriptlet file.
* Host: the installed `libalpm.so.16.0.1` (sha256 `1bc59ef4…`, equal to `capture-meta.txt`) carries
  `/usr/bin/bash` at dump line 1277; the full 1713-string dump contains no string equal to `/bin/sh`
  (`grep -c '^/bin/sh$'` → `0`). The capture's two indices (1263 `/usr/bin/ldconfig`, 1277
  `/usr/bin/bash`) are reproduced exactly by `strings -a … | grep -n -E '/usr/bin/(bash|ldconfig)'`.
* The sentence is true and, as EX4 says, its practical consequence is that bash-only syntax in a scriptlet
  is a function of the packaging choice, not of the package. Completion worth carrying: "cannot be selected
  per package" holds for the shell that runs the functions; a function may still invoke any interpreter
  itself.

## 4. Divergences and provenance gaps found

| # | finding | evidence | disposition suggested |
|---|---|---|---|
| D1 | The staged "so every path inside them must be absolute" does not follow from cwd `/` and is **contradicted by the entry's own EX1 host cell** | `r25:47-48` vs `entry:21` ("A hook or scriptlet that uses relative paths resolves them from `/` on this host"), `util.c:683`, `:698`; §2 | carry P3 only corrected; do not let the inference into the entry |
| D2 | "system root (`/`)" names the wrong root under `--root`: the chroot target is `handle->root`, and a scriptlet's absolute path is that root's | `util.c:679`, `trans.c:397-401`, EX1 value cell `entry:21` | use "installation root" |
| D3 | The only documentary sentence for P2 sits **outside S224's declared anchor/scope cell** (61-67, 83-85, 91-93), and the suffix-forming code sits outside S213's (466-474, 616-648, 655-695) | `alpm-hooks.5.asciidoc:126-128`; `add.c:318-323`; S224/S213 rows in `corpus/SOURCES.md:233`, `:222`; round-39 already flagged `:126-129` at `lessons/round-39.md:56` and S224 included `:91-93` but not the caveat | cheapest close: widen S224's scope cell to `CAVEATS` 124-129 (row already re-checks on pacman release); otherwise a new row. Read-only seat: not done |
| D4 | EX8 / derived item 5 say a `.pacnew` outcome "still triggers the original path" without the acquisition-set mapping; an `Operation = Install`-only hook does not fire on the ordinary `.pacnew` upgrade | `hook.c:305-339`, `:339-341`, `:344-349`; `entry:28`, `entry:36` | add the set mapping to EX8 (proposed text in §5) |
| D5 | The capture's strings file is a 2-line filtered extract and `capture-meta.txt` records no command, so "lacks `/bin/sh`" is not checkable from the capture alone; I re-checked it against the installed library | `hostcap/libalpm-shell-strings.txt` (2 lines), `capture-meta.txt` (no commands); my dump: 1713 strings, 0 exact `/bin/sh`, indices 1263/1277 reproduced with `/usr/bin/(bash\|ldconfig)` | record the extraction command in the next capture (evidence weight, not a claim error) |
| D6 | The candidate's own source S209 (`extra/alpm-docs 0.13.0-1`) is not installed here and the three fetch routes failed (ECONNRESET twice, HTTP 404); P4 stands on S219/S220/S222/S225, so nothing is lost, but S209 could not be re-opened | `pacman -Q alpm-docs` → "package 'alpm-docs' was not found"; receipts §6 | none for P4's admission; note it if S209 is ever carried |

## 5. Exact proposed text (for the lane's admission)

**P1 (admit, EX6) — carry as EX6; no change needed.** For completeness, the sentence an entry should hold:

> `NeedsTargets` feeds the hook its matched trigger targets on stdin — package names for `Type = Package`,
> package-archive paths for `Type = Path` — as the union over all of the hook's triggers
> (`hook.c:427-442`, joins `:341-349` and `:412-414`), sorted with `strcmp` and de-duplicated, one target
> per line (`:519-526`; feed loop `:469-490`, newline `:476`). A hook without `NeedsTargets` gets the closed
> stdin of EX2.

**P2 (admit, EX8) — the staged sentence plus the set mapping:**

> A `Path` trigger is matched against the package's file-list names, never against names on disk, so a file
> that pacman writes out with a `.pacnew` suffix still matches under its listed name (`hook.c:265-278`
> consults only `NoExtract`; the suffix is attached at extraction, `add.c:318-323`). The matched name counts
> toward the hook's Install, Upgrade or Remove set according to where it lands in the old and new file
> lists — a name present in both is moved to `upgrade` (`hook.c:305-339`) — and the hook runs only for an
> `Operation` that covers that set (`:339-341`, `:344-349`).

**P3 (admit-with-correction, EX1 + EX5) — replacement for `r25:47-48`:**

> `.INSTALL` functions run with working directory `/` inside the installation root — the parent changes into
> that root, the child chroots into it only when it is not `/`, then changes to `/` (`util.c:628`, `:679`,
> `:683`) — and the scriptlet is sourced by an absolute path in that root (`trans.c:397-401`). Every path
> inside a function is therefore installation-root-relative: a relative path resolves from that `/` and
> names the same file as the absolute form, and what is ruled out is any other base (the caller's cwd, the
> scriptlet's temporary directory, or `$0`), not relative paths as such.

Optional one-line guard for `pacman-exec-environment-r40.md` (so the staged inference cannot be imported
later), to sit with EX1's host cell or in `## Boundaries`:

> A cwd of `/` fixes the resolution base; it does not require absolute paths, and no base other than the
> installation root exists (`util.c:628`, `:683`).

**P4 (admit, EX4) — the staged sentence plus its mechanism:**

> The shell that runs the functions is fixed when libalpm is built and is the same for every package:
> `SCRIPTLET_SHELL` comes from a build option whose upstream default is `/bin/sh` (`meson_options.txt:17`)
> and which Arch's PKGBUILD sets to `/usr/bin/bash` (`PKGBUILD:115`); `_alpm_runscriptlet` passes it as
> `argv[0]` with `-c` and the command line `. <scriptlet>; <function> <new version> [<old version>]`
> (`trans.c:341`, `:357-358`, `:400-406`, `:410`), so the scriptlet is sourced and its own `#!` line is
> never consulted. The installed `libalpm.so.16.0.1` carries `/usr/bin/bash` and no `/bin/sh`
> (`hostcap/libalpm-shell-strings.txt:2`; independently re-checked: 0 exact `/bin/sh` strings in the
> 1713-string dump). A package can call any other interpreter from inside a function; it cannot change the
> shell that runs them.

## 6. What I did not do

* No census `--selftest`, no C1 or C2 counter run: this is a judgment item, and every cited line was read in
  the frozen snapshots whose digests I verified (`sha256sum -c`).
* No host mutation of any kind: reads only (`sha256sum`, `strings`, `pacman -Q`), plus the seat scratch dir
  under `/fast/scratch/hyaku/tsukuroi-r40/AsmStagedResidual/`, removed before finishing. No installs, no
  `sudo`, no pacman transaction, no service action.
* No lane, fleet, sibling-lane or `shokuknow` write; no `git`/`jj` command at all.
* The scriptlet man page (`S209`) could not be re-opened (three failed fetches, recorded); no verdict here
  depends on it.
* The remaining sentences on `r25:41-45` (`AbortOnFail`, PostTransaction failure semantics) were not judged
  — outside the assigned four.
* I did not re-derive the SOURCES scope rules; D3/D5 are readings of the committed rows and capture files.

## 7. Confidence

High for P1, P2 and P4: code, build files, doc and a re-verified host value agree. High for the P3
falsification: the mechanism (`chdir("/")` before `execv`, no other base) is explicit in the snapshot and the
lane's own EX1 host cell states the same. Medium for D3/D5, which are provenance-scope readings of
`SOURCES.md` rows and capture metadata rather than mechanism claims. P2's set-mapping completion (D4) is
high confidence from `hook.c:305-321`, `:339-349`.
