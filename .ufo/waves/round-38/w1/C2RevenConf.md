VERDICT: supports

# C2-14 — how pacman 54d9411 assembles the hook-directory list, end to end

Item: reverse-engineer the HookDir list assembly and confirm/refute **HO2** in
`corpus/knowledge/pacman-hook-order-r38.md:22`. Answer: system dir always first in the list, therefore
**last** in search order; an explicit `HookDir` **replaces** the `/etc/pacman.d/hooks/` default but can never
displace the system dir; `pacman-conf HookDir` prints the *config* list only and never the libalpm list.
HO2 confirmed, with one wording refinement that is unreachable through `_alpm_trans_commit`.

## Provenance

S208/S210/S211 snapshots used in place and digest-matched to the lane's frozen set
(`.ufo/waves/round-38/sources/SHA256SUMS`): `hook.c` 99f1044b…, `alpm.c` 8bbb0a3c…, `trans.c` 637c1165…,
`alpm-hooks.5.asciidoc` 2970cb35…. Files the seat needs that the frozen set lacks (`conf.c`, `handle.c`, and
the frontend `pacman.c`, `pacman-conf.c`, `util.c`, `alpm_list.c`, `meson.build`) were fetched from
`https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/<path>` on 2026-10-26T04:5xZ; digests recorded in
`.ufo/waves/round-38/w1/C2RevenConf/source-digests.txt` (`conf.c` c265f921…, `handle.c` 3e2a3d55…,
`pacman.c` 197cbc42…, `src/pacman/util.c` 6fcfb7f8…, `alpm_list.c` 3bb690c4…). Installed man page for the
pinned build: `/usr/share/man/man5/pacman.conf.5.gz` (dated Oct 15, pacman 7.1.0.r9.g54d9411-3).

Host queries that follow are read-only (`pacman -Q`, `pacman-conf`); no transaction, package, hook, service or
`/etc` change was made. Full replay: `.ufo/waves/round-38/w1/C2RevenConf/host-observations.txt`.

## Assembly, stage by stage

**0. Build constants** — `meson.build:71` `SYSHOOKDIR = <datarootdir>/libalpm/hooks/`;
`meson.build:77` `HOOKDIR = <sysconfdir>/pacman.d/hooks/`. Two distinct constants for two distinct roles:
`SYSHOOKDIR` is the always-read system dir, `HOOKDIR` is the pacman.conf default.

**1. The system dir is inserted by libalpm itself, before any config is read** — `alpm.c:56-62`: the handle is
created, then `snprintf(hookdir, …, "%s%s", myhandle->root, &SYSHOOKDIR[1])` and
`myhandle->hookdirs = alpm_list_add(NULL, hookdir)` (`:62`). It is the *seed* of the list, so it is the head
element by construction. It is also the only hookdir add that emits no `ALPM_LOG_DEBUG` line — visible in
`pacman -Q --debug`, whose sole hookdir line is the config-derived one:
`debug: option 'hookdir' = /etc/pacman.d/hooks/` (`host-observations.txt:40-41`).

**2. pacman.conf `HookDir` lines accumulate into the *frontend* config list, not the handle** —
`conf.c:666-675`: `strcmp(key, "HookDir")`, then `setrepeatingoption(value, "HookDir", &(config->hookdirs))`
(`:675`). The `resolve_path` call that would have canonicalised it is commented out (`:667-674`), so no
existence check and no absolutisation happen here.

**3. The default is applied only if the config list is still empty** — `conf.c:1370`
`#define SETDEFAULT(opt, val) if(!opt) { opt = val; … }` applied at `conf.c:1409`:
`SETDEFAULT(c->hookdirs, alpm_list_add(NULL, strdup(HOOKDIR)))`. `parseconfig()` fixes the order:
file parse (`:1454`) → `setdefaults()` (`:1457`) → `setup_libalpm()` (`:1461`), so file values are already in
place when the default is considered.

**4. `--hookdir` also lands in the config list before the default is considered** — `pacman.c:483-492`
(`OP_HOOKDIR`) appends `resolve_path(optarg, "--hookdir")` with `alpm_list_add(config->hookdirs, path)`;
`parseargs()` runs at `pacman.c:1220`, `parseconfig()` at `:1284`. Unlike the config path, the CLI path is
`realpath()`d and must exist (`src/pacman/util.c:1974-1983`).

**5. Each config entry is appended to the handle list, one by one** — `conf.c:944-953`
("add hook directories 1-by-1 to avoid overwriting the system directory"): `alpm_option_add_hookdir(handle,
i->data)` in list order. `handle.c:464-478` canonicalises (`canonicalize_path`, `:471`) and then
`handle->hookdirs = alpm_list_add(handle->hookdirs, newhookdir)` (`:475`) — and `alpm_list_add` is
`alpm_list_append` (`alpm_list.c:64-68`), a **tail** insert (`alpm_list.c:70-97`). So the handle list is
`[system] ++ config-in-file-order`, always.

**6. Search order is the reverse of that list** — `hook.c:540`:
`for(i = alpm_list_last(handle->hookdirs); i; i = alpm_list_previous(i))`. First directory opened wins a name:
`find_hook(hooks, entry->d_name)` at `:588` skips a file whose name is already registered (`:588-591`,
"skipping overridden hook"). Non-`.hook` names are filtered at `:582-586`, directories at `:593-603`,
parse/validate at `:609-615`, registration at `:617-618`. readdir order inside a directory is irrelevant
because the merged list is re-sorted at `:633-634` with `_alpm_hook_cmp` (`:443-455`), and phase/trigger
filtering happens afterwards (`:636-642`).

## Direct answers

1. **Is the system dir always first?** Yes in the list — it is the seed element (`alpm.c:62`) and nothing in
   the pacman frontend prepends to `handle->hookdirs`: the only frontend mutation is
   `alpm_option_add_hookdir` at `conf.c:948`. `pacman -Q --verbose` prints the handle list
   (`pacman.c:1313-1317`) and shows it exactly: `Hook Dirs : /usr/share/libalpm/hooks/  /etc/pacman.d/hooks/`
   (`host-observations.txt:10-11`). "First" is therefore *lowest* precedence, because enumeration is reverse
   (`hook.c:540`). It can only be dropped through the library API (`alpm_option_set_hookdirs`
   `handle.c:480-494`, `alpm_option_remove_hookdir` `handle.c:496-514`) — [INFERENCE] no pacman CLI path
   reaches either: `grep -n 'hookdir' src/pacman/pacman.c` yields only the help line `:219`, the `OP_HOOKDIR`
   case `:483-492`, the option table `:1025`, and the verbose printer `:1314`.

2. **Does an explicit `HookDir` replace the default or add to it?** It **replaces** `/etc/pacman.d/hooks/`
   (guarded `SETDEFAULT`, `conf.c:1370` + `:1409`) and can never replace the system dir (which is not in
   `config->hookdirs` at all). Observed:
   `pacman-conf --config t1.conf HookDir` → `/custom/a/` `/custom/b/` (two explicit lines, both kept, in file
   order); `--config t2.conf` (`[options]` only) → `/etc/pacman.d/hooks/`; handle view for t1 →
   `Hook Dirs : /usr/share/libalpm/hooks/  /custom/a/  /custom/b/` (`host-observations.txt:13-15`, `:18`,
   `:24-25`). Neither config path must exist — `pacman -Q --verbose --config t1.conf` succeeds although
   `/custom/a` does not exist; the CLI form rejects a missing dir instead (`failed to resolve path
   '/custom/z' passed to '--hookdir'`, `:36-37`). The installed man page states the same three facts: "Add
   directories to search
   for alpm hooks **in addition to the system hook directory (/usr/share/libalpm/hooks/)**. The default is
   /etc/pacman.d/hooks. Multiple directories can be specified with hooks in later directories taking
   precedence over hooks in earlier directories" (`/usr/share/man/man5/pacman.conf.5.gz:103-104`).
   `--hookdir` behaves like a config line: `pacman -Q --verbose --hookdir /var/lib/pacman` →
   `Hook Dirs : /usr/share/libalpm/hooks/  /var/lib/pacman/` — the `/etc` default is gone (`:33-34`).

3. **`pacman-conf HookDir` vs the libalpm list.** `pacman-conf` prints `config->hookdirs`
   (`pacman-conf.c:262` in `dump_config`, `:362-363` in the by-name path; `show_list_str` iterates the list),
   i.e. the *frontend* list after `SETDEFAULT` and after `prepend_sysroot` (`conf.c:1337-1339`, called at
   `:1429`). It never consults `alpm_option_get_hookdirs`. Consequences, all observed: on this host
   `pacman-conf HookDir` → `/etc/pacman.d/hooks/` only, while the handle list has both dirs; and if the
   operator writes the system dir into pacman.conf it appears in both and is **duplicated** in the handle
   list (`Hook Dirs : /usr/share/libalpm/hooks/  /usr/share/libalpm/hooks/  /x/y/`, `:27-28`) — harmless,
   since the second pass finds every name already registered at `hook.c:588`.
   Side note for `--sysroot`: config hookdirs get the sysroot prefix (`prepend_sysroot`, `:1337-1339`;
   observed `pacman-conf --sysroot <scratch>/sys --config /etc/pacman.conf HookDir` →
   `/fast/scratch/.../sys/custom/a/`), while the system dir is built from the *alpm root*
   (`alpm.c:61`, root passed from `conf.c:907` `alpm_initialize(config->rootdir, …)`) and is not relative to
   the root path, per the man page note at `pacman.conf.5.gz:105`.
   `canonicalize_path` only appends a trailing `/` (`handle.c:417-431`) — it neither resolves symlinks nor
   absolutises, so a relative `HookDir = relhooks` survives into the handle as `relhooks/`
   (`host-observations.txt:30-31`) and would be opened relative to the pacman process CWD at `hook.c:554`,
   contrary to the man page's "NOTE: this is an absolute path" (`pacman.conf.5.gz:105`). [INFERENCE] enforces
   nothing in code; not exercised in a transaction here.

## HO2 — confirmed, with one refinement

Machine check of the merge semantics over the live directories
(`.ufo/waves/round-38/w1/C2RevenConf/merge-simulation.txt`): usr=67, etc=3, total 70 files → **69** effective
hooks, the overridden names being exactly `90-mkinitcpio-install.hook`, `99-limine.hook`,
`walker-restart.hook`; all three resolve to the `/etc` copy, matching the `dir` column of the table rows
(`pacman-hook-order-r38.md:69,71,101`). The one cross-directory collision is
`90-mkinitcpio-install.hook`; its `/etc` copy is the operative one and carries
`Exec = /usr/share/libalpm/scripts/limine-mkinitcpio-install` versus the shadowed
`Exec = /usr/share/libalpm/scripts/mkinitcpio install` (`host-observations.txt:68-73`; the two files also
differ by digest — `/etc` a0689d02…, `/usr` 9fc607e8…, both matching the frozen capture
`.ufo/waves/round-38/frozen/hooks-capture/MANIFEST.sha256:1`, and live `sha256sum` agrees). This is the third
independent confirmation of the `90-mkinitcpio-install.hook` override after
`degraded-triage-r4.md:617-621` and the r19 [inf] at `boot-writers-r19.md:37`.

The one literal imprecision: "the first file **seen** for a name wins" — the skip at `hook.c:588` tests the
list of *successfully parsed* hooks, and a name is only added at `:617-618` after `parse_ini` **and**
`_alpm_hook_validate` succeed (`:609-615` discards a failing file without registering it). So a broken
higher-priority file does not suppress a lower-priority namesake: the lower one is then parsed and registered,
and `ret` is set to -1 regardless. TRIGGERLESS files are the exception that makes the documented mask work:
`_alpm_hook_validate` returns 0 immediately when `hook->triggers == NULL` (`hook.c:119-123`, the "/dev/null
mask" case documented at `alpm-hooks.5.asciidoc:98-100`), so a mask *is* registered and *does* suppress.
This gap has no reachable host consequence: any discarded `.hook` file sets `ret = -1` (`:613`), and for the
Pre phase `:629-631` aborts the whole run and `trans.c:201-204` turns it into
`ALPM_ERR_TRANS_HOOK_FAILED`, so the Post phase where the fallback could run is never reached (and with
`ALPM_TRANS_FLAG_NOHOOKS` no phase runs at all). Net: HO2's operative content (search last→first, system dir
at the head = lowest precedence, user dirs after it, same-name skip) is correct for every reachable
configuration; only the phrase "seen" should read "successfully parsed".

Suggested replacement for the first sentence of HO2, same citations:
"Directories are enumerated from the **last** list entry to the first; the first **successfully parsed** file
for a name wins and later same-name files are skipped (a file that fails validation never registers, so it
cannot mask)."

## Not done / limits

- I did not run a transaction: the search-order consequence is source-level (`hook.c:540`) plus the handle
  list observed on the host; the per-phase `running '<name>'` oracle belongs to the pacman.log seats.
- I did not test a `/dev/null` mask end to end (no transaction, and creating files in `/etc/pacman.d/hooks`
  is forbidden here); HO3/HO2's mask clause is code-reading at the cited lines.
- No package, hook, service, sysfs or `/etc` change; no `sudo`; nothing installed. Only `gcc`/`pkg-config`
  (already present) were used to build the read-only `alpm_option_get_hookdirs` probe.
- Scratch `/fast/scratch/hyaku/tsukuroi-r38/C2RevenConf/` removed after receipts were copied.

## Receipts — `.ufo/waves/round-38/w1/C2RevenConf/`

`host-observations.txt` (75 lines, replayed `obs.sh`), `merge-simulation.txt` (`merge.py` over the live dirs),
`source-digests.txt`, `probe.c`, `obs.sh`, `merge.py`, `t1.conf`–`t4.conf`.

## Per-row verdicts (rows this seat judged against the pinned source)

- HO1: holds — `lib/libalpm/hook.c:443-455` (suffix stripped, `strncmp` over the shorter length at `:450`,
  shorter-first tie at `:451-452`); merge check reproduces the fontconfig / gio-querymodules /
  gio-remove-module-cache pairs in the stated order (`merge-simulation.txt:5-7`).
- HO2: holds — `lib/libalpm/hook.c:540`, `:588-590`; `lib/libalpm/alpm.c:56-62`; wording refinement above.
- HO3: holds — `lib/libalpm/hook.c:119-123` (triggerless hook validates and is registered, so it never runs
  and does mask; `doc/alpm-hooks.5.asciidoc:98-100`).
- HO4: holds — `lib/libalpm/hook.c:660-669` (`ret = -1` only when `abort_on_fail`, then `break` for the Pre
  phase).
- HO5: holds — `lib/libalpm/hook.c:609-615`, `:629-631`; `lib/libalpm/trans.c:201-204`.
- HO6: holds — `lib/libalpm/trans.c:212-240` (Post hooks only in the non-interrupted `else` after
  `transaction completed`; the `:238` return value is discarded).
- HO7: holds — `lib/libalpm/hook.c:633-634` (msort by `_alpm_hook_cmp`) then `:636-642` (filter by `when` and
  trigger).
