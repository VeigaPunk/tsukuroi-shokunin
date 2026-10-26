# C2RevenStaged — receipts

All commands below were run read-only from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` or the frozen
directories. No lane file was written except this seat's own report and this directory. No git/jj command was run.
No scratch clone, no fixture, no tool install. Scratch dir: none created, nothing to remove.

## 1. Candidate bytes (match the round-38 review)

```
$ sha256sum /home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/pacman-hook-timing-r25.md
e18c146e733d3cab4bcc82c2ba30b9a571791ec132f7988cd93481b079f09324  .../pacman-hook-timing-r25.md
```
Reference: `.ufo/waves/round-38/w1/AsmRevTiming.md:7` (same hash).

## 2. Frozen inputs intact

```
$ cd .ufo/waves/round-39/frozen/src && sha256sum -c SHA256SUMS        # (per-file sums, all OK)
$ cd .ufo/waves/round-39/frozen/txcapture && sha256sum -c MANIFEST.sha256
capture-meta.txt: OK
hook-owners.tsv: OK
hook-when.tsv: OK
pacman.log: OK
```

## 3. Host recomputation from the frozen `pacman.log` (my own model, not the counter)

Model: a window opens at `[PACMAN] Running`; the commit phase is `transaction started` .. `transaction
completed|failed|interrupted`.

```
windows 86 started 60 scriptlet_in 189 scriptlet_out 252 total 441 hookruns 295 hookruns_inside 0
```
→ TO1's "60 transactions … 86 windows … 0 `running` lines inside a commit phase" and TO8's "252 of 441" reproduce.

```
windows 86 with_started 60 both 0 rem_only 7 rem_windows 7
sample rem_only [{'cmd': "Running 'pacman -R --noconfirm hopper'", 'rem': 1, ...},
                {'cmd': "Running 'pacman -Rns --noconfirm quickshell'", 'rem': 4, ...}]
$ grep -c '\[ALPM\] removed ' pacman.log   -> 28
```
→ TO2's "0 of 60" and "28 removed lines … removal-only" reproduce (28 lines from 7 removal-only windows).

TO5 host cell, read as "the owner's first-ever-install window":

```
pre hooks 17 owners: ['dkms','gdk-pixbuf2','glib2','glibc','gtk3','kernel-modules-hook','lib32-glib2',
 'lib32-glibc','limine-mkinitcpio-hook','limine-snapper-sync','mkinitcpio','openssh','texinfo']
ran in first-install window: []
did not run: 17
pre 17  first-install window uses an alternate root: 7
 ['10-glibc-remove-locale-archive.hook','11-glibc-remove-ldconfig-cache.hook',
  '12-glibc-remove-iconvconfig-cache.hook','60-mkinitcpio-remove.hook',
  'gio-remove-module-cache.hook','glib-remove-compiled-schemas.hook','texinfo-remove.hook']
remaining host-root instances: 10
```
(`-r /mnt` bootstrap window e.g. `pacman -b /mnt//var/lib/pacman/ -r /mnt … base sudo linux-firmware mkinitcpio
linux …`.) 17/17 consistent, but only 10 informative on the host root — the qualification in report §7.3.

TO3's host cell:
```
$ sed -n '123,124p' pacman.log
[2026-10-03T20:41:59+0000] [ALPM] installed systemd (261.1-1)
[2026-10-03T20:41:59+0000] [ALPM-SCRIPTLET] Initializing machine ID from random generator.
```

Unowned hook files (P1 owner-cell correction):
```
$ grep -P '\t-$' hook-owners.tsv
69:/etc/pacman.d/hooks/99-limine.hook	-
70:/etc/pacman.d/hooks/walker-restart.hook	-
```

## 4. Source reads (line numbers verified by numbering each region)

- `trans.c`: Pre phase + `RET_ERR` :201-204; `STATE_COMMITTING` :206; `"transaction started"` :208; remove/sync
  commit and `"transaction failed"` :212-228; `"transaction interrupted"` :230-231; `"transaction completed"` and
  Post call :233-239; `_alpm_runscriptlet` :337; `SCRIPTLET_SHELL` + `-c` :357-358; tmpdir under root :360-367;
  copy/extract `.INSTALL` :375-387; "chop off the root" :397-398; argument order `ver`/`oldver` :400-406;
  `_alpm_run_chroot` :410.
- `add.c`: `.pacnew` extraction and warning :318-350; fake remove of the old package :484-485; db write :599;
  `upgraded %s (%s -> %s)` :630; post scriptlet :638-647; loop + `skip_ldconfig` :669-692; pre scriptlet :467-474;
  log switch :616-636.
- `sync.c`: `_alpm_sync_commit` :1336; comment :1340; `_alpm_remove_packages` :1345; `_alpm_upgrade_packages` :1354.
- `remove.c`: pre_remove :706-713 (`:711`); file removal :716-719; `removed` :721-724 (`:722`); post_remove
  :726-733 (`:731`); `newpkg` guard :698-714 (upgrade half).
- `util.c`: `_alpm_chroot_process_output` :521-528 (`:527` ALPM-SCRIPTLET); `_alpm_run_chroot` :610 with stdin
  callback doc :606; `chdir(handle->root)` :628; `chroot` skipped for `/` then `chdir("/")` :677-683; `_alpm_ldconfig`
  :816-833.
- `hook.c`: `_alpm_hook_validate` :113-147 (triggerless :119-123; AbortOnFail-on-Post is a **warning** :141-143);
  file trigger match on `pkg->files` :258-295; package trigger match :363-417; `_alpm_hook_cmp` :443-455 (`:449`
  comment, `:450` strncmp, `:451-452` tie-break); `depends` gate :509-517; `needs_targets` stdin callback :519-529;
  `_alpm_hook_run` :532; dir loop :540; `opendir` :554; same-name skip :588-591; parse/validate failure :609-615;
  Pre abort on parse error :629-631; sort + `when`/`triggered` filter :633-642; run loop, `abort_on_fail` :660-662,
  Pre-only break :667-669.
- `alpm-hooks.5.asciidoc` (round-38 snapshot): dirs :35-37; order :38-39; `When=` required :80-81; AbortOnFail
  :87-89; NeedsTargets/stdin :91-93; OVERRIDING HOOKS :98-100; CAVEATS `.pacnew` :124-127; removal triggers
  :128-129; PostTransaction not run :131-132.

## 5. Devblog attribution (P5/P6)

Frozen page `.ufo/waves/round-38/w1/AsmS202Devblog/page.html`, tag-stripped text:
```
'On scripts and hooks 2026-08-09 16 min David Runge , Arne Christian Beer …'          (offset 438)
'… Documentation At the time of writing, we are missing a documented ordering system for alpm-hooks(5) in the
distribution to establish ranges of number prefixes for specific tasks. …'           (offset 22247)
grep 'alphabet' -> ABSENT
grep 'author'   -> ABSENT
```

## 6. Registry / coverage checks

```
$ grep -n "devblog\|alpm-install-scriptlet\|archlinuxcn\|alpm-hooks" corpus/SOURCES.md
14:| S008 | alpm-hooks(5) — https://man.archlinux.org/man/alpm-hooks.5       # OVERRIDING HOOKS only
218:| S209 | alpm-hooks(5) source at pacman 54d9411 … DESCRIPTION lines 34-39 and AbortOnFail lines 87-89
$ grep -n "^| S21[5-9]" corpus/SOURCES.md   -> S215 remove.c, S216 util.c, S217 trans.c, S218 capture; no S219+
$ ls corpus/knowledge/ | grep -i "initramfs\|errno-name"
initramfs-v42-sysroot-recovery.md          # `initramfs-hook-api-r25.md` absent
$ ls corpus/lessons/                        -> up to round-38.md; `round-39.md` absent
$ sed -n '36,44p' corpus/README.md          -> mkinitcpio-42 watch, errno:13 item, pointer line
$ sed -n '74,82p' PROVINCE.md                -> Frontier: recipient ack, Kaidoku/revenger scope
$ awk 'NR==22' corpus/lessons/round-37.md   -> reject row for errno-name-discrimination-r25.md
$ awk 'NR==25' corpus/lessons/round-38.md   -> "CORPUS.md rule 2 lets only status, recheck and used-by change in place"
```

## 7. Tools installed / upgraded

None. No pacman, no uv, no npm, no binary fetched.
