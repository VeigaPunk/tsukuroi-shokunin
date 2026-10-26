VERDICT: supports

Item C2-EX1 — row EX1 of `corpus/knowledge/pacman-exec-environment-r40.md` at the pinned lane tip
`f951f288483c1af0cef4afd458488b84cf7a2165` (read via `git show f951f288…:corpus/knowledge/pacman-exec-environment-r40.md`;
doc line 21). Verdict against the pinned source: **holds** — every clause of the rule, value and host
cells is grounded in `lib/libalpm/util.c` at pacman `54d9411`, and the quoted line is byte-exact at the
cited line. No correction text required.

## Provenance re-check (independent of the freeze)

- Frozen snapshots intact: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-40/frozen/src/` → all six
  files OK (PKGBUILD, alpm-hooks.5.asciidoc, hook.c, meson_options.txt, trans.c, util.c).
- Upstream re-opened by this seat with `curl -fsSL` at **2026-10-26T07:18:30Z**: pacman `54d9411`
  `lib/libalpm/{util.c,hook.c,trans.c}`, `doc/alpm-hooks.5.asciidoc`, `meson_options.txt`, and
  `archlinux/packaging` pacman tag `7.1.0.r9.g54d9411-3` `PKGBUILD`. All six sha256 match the frozen
  `SHA256SUMS` (`sha256sum -c`: six × OK). Receipts: `.ufo/waves/round-40/w1/C2RevEX1/`
  (`fetch-and-hashes.txt`, `run-chroot-lines.txt`, `quote-check.txt`).
- Host: `pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3` (the doc's build).

## Clause-by-clause (doc line 21; line numbers = pinned util.c at 54d9411)

1. "Every command libalpm runs through `_alpm_run_chroot` (hook `Exec` commands, install scriptlets and
   `ldconfig`)" — holds. The pinned tree has exactly three `_alpm_run_chroot` call sites (grep over the
   three pinned files): hook.c:525 and hook.c:528 (both branches of `_alpm_hook_run_hook`;
   `hook->cmd` is the Exec line's wordsplit, hook.c:234-239; missing Exec errors at hook.c:134);
   trans.c:410 (`_alpm_runscriptlet` runs `SCRIPTLET_SHELL`); util.c:833 (`_alpm_ldconfig` runs
   `LDCONFIG` with argv[0] "ldconfig", util.c:832).
2. "starts in working directory `/`" — holds. Parent `chdir(handle->root)` at util.c:628 precedes
   `fork()` at :653; the child reaches `execv` at :698 only after the unconditional `chdir("/")` at
   :683. root = "/": the child inherits cwd `/` from the parent's :628. root ≠ "/": `chroot` at :679
   then `chdir("/")` at :683 lands it at `/` inside the new root. Every earlier failure path prevents
   the command from starting (goto cleanup at :631, :643, :649, :657; child `exit(1)` at :681, :686,
   execv-failure path :700), so no executed command starts anywhere else.
3. "the parent first changes into the installation root" — holds. util.c:628
   `if(chdir(handle->root) != 0)` runs before fork :653; failure logs "could not change directory to %s"
   and goes to cleanup (:629-631), so the command never runs.
4. "the child calls chroot only when that root differs from `/`" — holds. util.c:679
   `if(strcmp(handle->root, "/") != 0 && chroot(handle->root) != 0)` — the short-circuit `&&` skips
   chroot when root is "/", and the source says so in words: comment util.c:677-678 "don't chroot() to
   \"/\": this allows running with less caps when the caller puts us in the right root". QUALITY 66's
   requirement that "only" have a source sentence saying so is met by :679 plus that comment.
5. "the child then changes its directory to `/`" — holds. util.c:683 `if(chdir("/") != 0)` is
   unconditional in the child, immediately after the chroot branch and before SHLVL/BASH_ENV/umask/
   execv (:692-:698). Both branches of the two-branch condition are kept in the rule (QUALITY 66).
- Value cell `/` — consistent with clauses 2-5.
- Source cell "S221 util.c:677-687 “if(strcmp(handle->root, "/") != 0 && chroot(handle->root) != 0) {”
  (parent `chdir(handle->root)` :628; child `chdir("/")` :683)" — holds. The quote is byte-exact at
  util.c:679 (`cmp` clean after stripping leading tabs; `quote-check.txt`); :679 lies inside the cited
  677-687; :628 and :683 are the exact lines of the two named calls.
- Host cell "A hook or scriptlet that uses relative paths resolves them from `/` on this host
  (root `/`, so no chroot call happens)" — holds as a derivation. Effective root on this host:
  `pacman-conf RootDir` → `/` (observed 2026-10-26); `/etc/pacman.conf` sets no RootDir;
  grep RootDir over `/etc/pacman.d` → no matches. With root "/", util.c:679 short-circuits, so no
  chroot call happens — exactly as the cell states; the child's cwd is `/`, so relative paths resolve
  from `/`.

## Residual findings (outside EX1's scope, routed for L1)

- `corpus/SOURCES.md` line 230 (row S221) states "`_alpm_run_chroot` lines 610-760". In the same
  pinned snapshot the function spans util.c:610-814 (cleanup label :804, closing brace :814; the next
  function `_alpm_ldconfig` begins at :820 with its `_alpm_run_chroot` call at :833). Every individual
  micro-citation in the S221 cell that this item touches (628, 665-667, 679, 683, 692, 694, 695, 698)
  is correct; only the extent figure "610-760" is short by 54 lines (the parent's poll/waitpid/cleanup
  tail). Exact proposed text for a SOURCES.md owner seat, append-only: change "lines 610-760" to
  "lines 610-814" in the S221 anchor cell. No EX1 text change proposed — EX1 holds.

## Not done / limits

- No counters were run (not in this item); EX1 was judged only against the pinned sources and read-only
  host inspection.
- No live transaction was executed (host pacman transactions are paused; the doc's Boundaries, doc
  lines 43-44, likewise carries no host instance for EX1). The host-cell root-`/` claim rests on
  read-only config inspection, not on a captured transaction.
- S221's ":722-726 stdin end closed" figure was not re-checked here (EX2's row; another seat's scope).
- No tools installed or upgraded by this seat.
