VERDICT: supports

Item C2-14 — the Arch patches applied on top of 54d9411 do not touch any statement the
EX1–EX8 rows rest on, and the installed `libalpm.so.16.0.1` agrees with the EX rows at
string level and (for EX1/EX2/EX3/EX4/EX5/EX6/EX7) at instruction level. One patch does
land *inside* the cited util.c window (610–760): it inserts 5 lines after util.c:675 and
shifts every later util.c anchor by +5. Nothing it inserts changes a single EX value.

All work read-only on the lane; no git/jj/pacman/service/sysfs/mount action; scratch was
`/fast/scratch/hyaku/tsukuroi-r40/C2RevenPatches/` (removed before this report was
written); receipts under `.ufo/waves/round-40/w1/C2RevenPatches/`.

## 1. Provenance of the four patches (all fetched from the pinned tag)

Fetch commands (all 2026-10-26, HTTP 200, `curl -fsSL`):

    B=https://gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/raw/7.1.0.r9.g54d9411-3
    curl -fsSL -o 0001-libalpm-invalidate-curl-data-in-child.patch \
         "$B/0001-libalpm-invalidate-curl-data-in-child.patch"        # 987 bytes
    curl -fsSL -o 0002-libalpm-use-curl-s-effective-url-without-authenticat.patch \
         "$B/0002-libalpm-use-curl-s-effective-url-without-authenticat.patch"  # 2272 bytes
    curl -fsSL -o commit-354a300c...patch \
         https://gitlab.archlinux.org/pacman/pacman/-/commit/354a300cd26bb1c7e6551473596be5ecced921de.patch   # 5738
    curl -fsSL -o commit-f4bdb774...patch \
         https://gitlab.archlinux.org/pacman/pacman/-/commit/f4bdb77470528019aaba4d8b8f947e918c6db17d.patch   # 4792

`sha256sum` of the four downloads, compared with `.ufo/waves/round-40/frozen/src/PKGBUILD:61-65`:

| patch | sha256 (observed) | PKGBUILD sum line | match |
|---|---|---|---|
| revertme-makepkg-remove-libdepends-and-libprovides | `b3bce9d662e189e8e49013b818f255d08494a57e13fc264625f852f087d3def2` | :62 | yes |
| patch-reproducible-builds | `de428b496a825772ef49ec5555a386a4b23ffa10b9dfd9907f0671d5c1dc2178` | :63 | yes |
| 0001-libalpm-invalidate-curl-data-in-child | `9a734e5d75be603d58aa92e8d29a15466b3ac2af6b7d6f6728dd5c3e5ed8758d` | :64 | yes |
| 0002-libalpm-use-curl-s-effective-url-without-authenticat | `021893dd44ec23251cfc0f2b81c12d832927ea60095d4d2956d9760e8bbfaa58` | :65 | yes |

The two commit-URL downloads are byte-identical to the stored patch files, so the commit
`.patch` URLs are the same artefacts the PKGBUILD sums cover. The apply path is
`PKGBUILD:81-104`: `git rebase "${_git_patch_level_commit}"` (`:86`, = 54d9411,
`PKGBUILD:9`), then every `source[]` entry matching `.patch` is applied — `revertme-*`
with `patch -RNp1` (`:99`), the rest with `patch -Np1` (`:102`). The four patches above
are therefore the *complete* patch set; nothing else is applied to the tree.

## 2. Full file and hunk inventory (`.ufo/.../w1/C2RevenPatches/hunk-inventory.txt`)

| patch | file | hunks |
|---|---|---|
| 0001 | `lib/libalpm/util.c` | `@@ -673,6 +673,11 @@ int _alpm_run_chroot(...)` |
| 0002 | `lib/libalpm/dload.c` | `@@ -507,6 +507,7 @@`, `@@ -609,6 +610,7 @@`, `@@ -629,8 +631,11 @@` (all in `curl_check_finished_download`) |
| revertme | `doc/PKGBUILD.5.asciidoc` | `@@ -187,11 +187,6 @@`, `@@ -245,10 +240,6 @@` |
| revertme | `scripts/makepkg.sh.in` | `@@ -463,121 +463,6 @@ run_package()`, `@@ -617,9 +502,6 @@ write_pkginfo()` |
| reproducible-builds | `lib/libalpm/add.c` | `@@ -412,6 +412,29 @@` (adds `static time_t get_install_time(void)`), `@@ -591,7 +614,7 @@` (`newpkg->installdate = get_install_time();`) |
| reproducible-builds | `test/pacman/README` | `@@ -294,6 +294,7 @@` |
| reproducible-builds | `test/pacman/meson.build` | `@@ -277,6 +277,7 @@` |
| reproducible-builds | `test/pacman/pmrule.py` | `@@ -108,6 +108,9 @@` |
| reproducible-builds | `test/pacman/pmtest.py` | `@@ -92,6 +92,7 @@`, `@@ -299,7 +300,7 @@` |
| reproducible-builds | `test/pacman/tests/source_date_epoch_install.py` | new file, `@@ -0,0 +1,12 @@` |

Files touched by the whole set: `util.c`, `dload.c`, `add.c`, `doc/PKGBUILD.5.asciidoc`,
`scripts/makepkg.sh.in`, five test files. **Not touched: `trans.c`, `hook.c`,
`meson_options.txt`, `doc/alpm-hooks.5.asciidoc`, `lib/libalpm/handle.h`.**

## 3. Overlap with the four cited regions

- `util.c:610-760` — **yes, one hunk overlaps.** `@@ -673,6 +673,11 @@` inserts after
  frozen util.c:675 (blank line following `close(cwdfd); }`):
  `#ifdef HAVE_LIBCURL` / `/* invalidate the curl data - we must not touch it in child */` /
  `handle->curlm = NULL;` / `#endif` / blank.
- `trans.c:337-428` — no. Nothing in the set touches `trans.c`. (That window is
  `_alpm_runscriptlet`: `SCRIPTLET_SHELL` at trans.c:361, `"tmp/alpm_XXXXXX"` at :370,
  `"%s/.INSTALL"` at :380.)
- `hook.c:258-530` and `:640-668` — no. Nothing in the set touches `hook.c`. (`running
  '%s'...` hook.c:653, `could not satisfy dependencies` hook.c:514.)
- `meson_options.txt` — no. `scriptlet-shell` default `/bin/sh` stands
  (meson_options.txt:17); the Arch value comes from `PKGBUILD:115`
  `-Dscriptlet-shell=/usr/bin/bash`, i.e. the build flags, not a patch.

### 3.1 Consequence for line citations (apply checked, not assumed)

`patch -Np1` against a scratch copy of the frozen tree: `checking file lib/libalpm/util.c`,
exit 0. Re-grepping the patched file (1662 lines, was 1657):

    351:	oldmask = umask(0022);          (unchanged, a different umask use)
    662:		close(0);                 (unchanged)
    678:		handle->curlm = NULL;     <- patch 0001 insertion
    688:		if(chdir("/") != 0) {     (was 683; +5)
    697:		setenv("SHLVL", "1", 0);  (was 692; +5)
    699:		unsetenv("BASH_ENV");     (was 694; +5)
    700:		umask(0022);              (was 695; +5)
    703:		execv(cmd, argv);         (was 698; +5)

So EX rows stated as the range `util.c:610-760` remain true of the installed build, but a
*point* citation to util.c ≥676 would be off by five. `chdir("/")`, `SHLVL`, `BASH_ENV`,
`umask(0022)` and `execv` are not otherwise modified, and the patch adds no code between
them and `execv`.

## 4. Installed binary agrees — the strings check the item asks for

`pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3`;
`/usr/lib/libalpm.so.16.0.1` sha256
`1bc59ef4cee493246db69c9466970de01d24fdc32a4a4c18c77063af66705e90` (identical to the
hostcap receipt `.ufo/waves/round-40/frozen/hostcap/capture-meta.txt:2`), mtime
`2026-10-15 05:27:03 -0300`.

`strings -a /usr/lib/libalpm.so.16.0.1 | grep -n -F …` (full output in
`.ufo/.../w1/C2RevenPatches/binary-strings.txt`):

| probe | observed |
|---|---|
| `/usr/bin/bash` | `1277:/usr/bin/bash` |
| `SHLVL` | `1253:SHLVL` |
| `BASH_ENV` | `1254:BASH_ENV` |
| `could not satisfy dependencies` | `1410:could not satisfy dependencies` |
| `tmp/alpm_XXXXXX` | `1271:%stmp/alpm_XXXXXX` |

Extra probes (same file): `running '%s'...` → 1077; `%s/.INSTALL` → 1272; `NeedsTargets` →
1043; `AbortOnFail` → 1042/1474; `PreTransaction` → 1038; `%s is in NoExtract, skipping
extraction of %s` → 1314. `grep -c -F '/bin/sh'` on the whole string dump → **0**.

The `%stmp/alpm_XXXXXX` prefix form (not a bare `tmp/alpm_XXXXXX`) is exactly the
`snprintf(tmpdir, len, "%stmp/alpm_XXXXXX", handle->root)` of trans.c:370, i.e. `<root>/tmp/alpm_XXXXXX`;
`%s/.INSTALL` immediately next to it at string index 1272 matches trans.c:380. The total
absence of `/bin/sh` from libalpm is the signature of `-Dscriptlet-shell=/usr/bin/bash`
(PKGBUILD:115) replacing the meson default (meson_options.txt:17) — EX4's installed value
is confirmed *and* distinguished from the upstream default.

`NoUpgrade`/`NoExtract` are absent from libalpm but present in `/usr/bin/pacman`
(`523:NoUpgrade`, `524:NoExtract`) — pacman.conf parsing lives in the pacman binary, so
that absence is expected and is not an EX8 gap.

## 5. Binary-level confirmation beyond strings (EX1/EX2/EX3/EX4/EX5/EX6/EX7)

`objdump -d --no-show-raw-insn /usr/lib/libalpm.so.16.0.1` (43007 lines, read-only
disassembly in scratch, excerpts kept in `.ufo/.../w1/C2RevenPatches/disassembly-excerpts.txt`).
The `.so` still carries `.symtab`, so functions are named.

### 5.1 Patch 0001 is compiled into the installed binary

`_alpm_run_chroot` at `0x303c0`. Child path, in address order:

    307b4/307c0/307cc/307d8  close()      x4  (the two socketpairs: TAIL/HEAD each)
    307e2/307e4              close(%ebx)      (cwdfd, if >= 0)
    307f2: movq   $0x0,0x28(%r12)            <- handle->curlm = NULL
    307fb: cmpb   $0x2f,(%rdi)               (handle->root[0] == '/')
    30815: call   chdir@GLIBC  (rdi = 0x367f1)
    30cc1: call   chroot@GLIBC               (non-"/" root branch)

`0x28(%r12)` is `curlm`: field order in `lib/libalpm/handle.h` (54d9411) is `db_local`
(0x00), `dbs_sync` (0x08), `logstream` (0x10), `trans` (0x18), `user` (uid_t, 0x20+pad),
then `#ifdef HAVE_LIBCURL` `CURLM *curlm;` → 0x28. The unpatched source has no store at
that point (frozen util.c:672-679 is `close(cwdfd); }` → comment → chroot), so the
instruction can only come from patch 0001. `HAVE_LIBCURL` is live: `ldd` shows
`libcurl.so.4 => /usr/lib/libcurl.so.4` and `nm -D --undefined-only | grep -c curl` → 14.

### 5.2 EX2 (stdio on one socket pair, stdin on a second)

Three `dup2` calls, targets 1, 2, 0, each with the `EINTR` retry loop the source has:

    30722/3072d/30738  close()              (close(0); close(1); close(2))
    30756: mov $0x1,%esi ; call dup2        → stdout
    3077e: mov $0x2,%esi ; call dup2        → stderr
    3079b: xor %esi,%esi ; call dup2        → stdin

Parent side: when `stdin_cb == NULL` the parent2child head is closed and `parent2child->fd
= -1` before the poll loop (`STOP_POLLING` paths at `0x308aa`/`0x308bb`), matching
util.c:561-570 — the stdin socket is closed at once, no input callback. With
`_alpm_hook_feed_targets` present, the parent writes on it: `send@GLIBC` at `0x30b25` with
the feed callback called through `-0x1878(%rbp)` at `0x30af6`. Output forwarding uses
`alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line)` — the two literals `0x37ad6`
(`ALPM-SCRIPTLET`) and `0x37a71` (`%s`) at `0x30e00/0x30e07` and `0x309e5/0x309ec`.

### 5.3 EX1 and EX3 (cwd `/`, SHLVL, BASH_ENV, umask, execv inherits environment)

    3080e: lea 0x367f1,%rdi   -> bytes at 0x367f0 are "//\0", so 0x367f1 is the string "/"
    30815: call chdir         (cwd "/" after chroot)
    30c24: xor %edx,%edx      (setenv overwrite = 0)
    30c26: lea 0x36046,%rsi   -> byte 0x36046 is '1' (tail of "16.0.1"), i.e. "1"
    30c2d: lea 0x37aac,%rdi   -> "SHLVL"
    30c34: call setenv
    30c3a: lea 0x37ab2,%rdi   -> "BASH_ENV" ; 30c41: call unsetenv
    30c47: mov $0x12,%edi ; 30c4c: call umask     (0x12 = 18 = 0022 octal)
    30c52: call _alpm_reset_signals
    30c57: call _alpm_handle_free   (after curlm was invalidated - the patch's intent)
    30c66/30c69: mov %r14,%rdi (cmd) ; call execv

`execv` (not `execve`/`execle`) is the last call before the "call to execv failed (%s)"
literal (`0x37abb`), so the environment is the parent's — EX3's "execv keeps the rest of
the environment" holds in the binary, and `setenv(..., 0)` cannot overwrite an inherited
SHLVL.

### 5.4 EX4 and EX5 (scriptlet shell and staging path) in `_alpm_runscriptlet`

`_alpm_runscriptlet.isra.0` at `0x31da0`:

    31f12: lea 0x37c1d,%r8     -> "%stmp/alpm_XXXXXX"
    323b9: lea 0x37c76,%rsi    -> "/usr/bin/bash"      (argv[0] = SCRIPTLET_SHELL)
    323c0: call 0x303c0 <_alpm_run_chroot>

The only `/usr/bin/bash` xref in the library is this one, feeding the run_chroot call —
EX4's "shell, not /bin/sh" and EX5's `<root>/tmp/alpm_XXXXXX/.INSTALL` staging are the
installed ones.

### 5.5 EX6 and EX7 (`running` before Depends; sorted, de-duplicated targets)

`_alpm_hook_run` at `0x23730`. Inside the per-hook loop, in address order:

    24190: mov  -0x2118(%rbp),%rax
    24197: lea 0x37012,%rdx   -> "running '%s'..."
    2419e: lea 0x36153,%rsi   -> "ALPM"   (ALPM_CALLER_PREFIX)
    241b1: call *0x43cf8      -> alpm_logaction
    241bd..241e8: event 0x24 (HOOK_RUN_START)
    241ed: call _alpm_db_get_pkgcache_hash     (local pkgcache)
    241fe: r12 = 0x18(%r13)                    (hook->depends)
    24225: call *0x43d68      -> alpm_find_satisfier
    24230/24235: "could not satisfy dependencies" + "unable to run hook %s: %s"

So the `running` log is committed **before** the Depends loop is even entered, and an
unmet Depends reaches the error log without any `_alpm_run_chroot` call on that path
(`0x24281` continues to the next hook / abort bookkeeping). The other xref to that
message, `0x18335`, is inside `alpm_strerror` (the ALPM_ERR_* table), not the hook path.

Run path at `0x24bc6`: `test 0x38(%r13)` (`needs_targets`) → `hook->matches` at `0x28` →
`alpm_list_count` → `alpm_list_msort(..., strcmp)` at `0x24bec` → inlined dedup loop
(`strcmp` `0x24c0f`, `alpm_list_remove_item` + `free` at `0x24c1f`/`0x24c2b`) → store back
`0x28` → `0x24c5e: call _alpm_run_chroot` with `rcx = 0x17080 <_alpm_hook_feed_targets>`
and `r8 = &ctx`. Without `needs_targets`: `0x24c9c: call _alpm_run_chroot` with the
`NULL, NULL` fourth/fifth arguments. Sorted then de-duplicated, then fed on the socket —
EX6 as stated.

## 6. Falsification attempts and consistency checks

- Every patch in `source[]` is accounted for; `prepare()` applies all `.patch` entries and
  nothing else (PKGBUILD:91-104). No fifth patch to hide a change in `hook.c`/`trans.c`.
- `util.c`'s hunk context was matched, not assumed: frozen util.c:673-678 is exactly
  `close(cwdfd);` / `}` / blank / the two comment lines / `/* caller puts us … */`, and
  `patch --dry-run` then real apply both exit 0.
- Patch 0002 preconditions were dry-run against upstream `dload.c` at 54d9411
  (`checking file lib/libalpm/dload.c`, rc 0); its three hunks are confined to
  `curl_check_finished_download`, so they cannot move a hook/scriptlet value.
  Installed `curl 8.23.0-1` is exactly the version named in 0002's commit message, and
  both patch dates (2026-04-30 for 0001, 2026-10-15 for 0002) precede the installed
  `.so` mtime 2026-10-15 05:27.
- 0001's `#ifdef HAVE_LIBCURL` is not dead code: libcurl is a hard `depends` in
  `PKGBUILD:19` and the library is dynamically linked.
- Frozen inputs are the pinned ones: `sha256sum -c .ufo/waves/round-40/frozen/src/SHA256SUMS`
  → `PKGBUILD: OK / alpm-hooks.5.asciidoc: OK / hook.c: OK / meson_options.txt: OK /
  trans.c: OK / util.c: OK`.

## 7. What I did not do

- I did not rebuild `pacman` from source, so "installed binary contains patch 0001" rests
  on the `0x307f2` store + `handle.h` offset argument (§5.1), not on a build.
- I did not execute a real hook or scriptlet (no host mutation; no `unshare` replay was
  needed for this item), so EX1/EX2/EX3/EX6/EX7 are confirmed from instructions and
  literals, not from a runtime trace.
- I did not verify that the `-RNp1` revertme patch applies (only its file/hunk footprint,
  which is what the item asks); it targets `doc/PKGBUILD.5.asciidoc` and
  `scripts/makepkg.sh.in`, neither of which carries an EX value.
- No tool was installed or upgraded for this item.

## 8. Receipts (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-40/w1/C2RevenPatches/`)

- `patches/` — the four fetched patches (987 / 2272 / 5738 / 4792 bytes).
- `binary-strings.txt` — the `strings | grep -n` transcript incl. the extra probes and the zero `/bin/sh` count.
- `disassembly-excerpts.txt` — the single-line objdump excerpts for every address cited above.
- `hunk-inventory.txt` — `diff --git`/`@@` map with per-file sha256.
- `fetch.txt` — URLs, date, sha256 provenance note.
