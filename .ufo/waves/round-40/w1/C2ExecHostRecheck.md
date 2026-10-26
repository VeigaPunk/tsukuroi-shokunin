VERDICT: supports

# C2-15 — live re-derivation of the frozen host capture

Item: re-derive `.ufo/waves/round-40/frozen/hostcap/` read-only and compare with the
declared C2 values (14 NeedsTargets effective hooks of 69; libalpm string index 1277).
Seat: C2ExecHostRecheck (L2, round 40 / hyaku run 8). Lane tip at dispatch
`f951f288483c1af0cef4afd458488b84cf7a2165`.

Result: **every frozen value reproduces exactly on the live host at 2026-10-26T07:15Z;
no drift since the 06:54:46Z capture.**

## 1. Host identity (same build the capture names)

`pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3`
`sha256sum /usr/lib/libalpm.so.16.0.1` → `1bc59ef4cee493246db69c9466970de01d24fdc32a4a4c18c77063af66705e90`
`pacman -Qo /usr/lib/libalpm.so.16.0.1` → `is owned by pacman 7.1.0.r9.g54d9411-3`
Both match `frozen/hostcap/capture-meta.txt:2-4`.

## 2. MANIFEST digests — all verify

```
$ cd .ufo/waves/round-40/frozen/hostcap && sha256sum -c MANIFEST.sha256
capture-meta.txt: OK
libalpm-shell-strings.txt: OK
hooks-needstargets.tsv: OK
```
The three data files are the whole directory (besides the manifest itself). The manifest
file digest also matches the value the corpus doc pins:
`sha256sum hostcap/MANIFEST.sha256` → `57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5`,
equal to `corpus/knowledge/pacman-exec-environment-r40.md:1`. Adjacent check, pinned
upstream snapshots: `cd .ufo/waves/round-40/frozen/src && sha256sum -c SHA256SUMS` → all six
`OK` (PKGBUILD, alpm-hooks.5.asciidoc, hook.c, meson_options.txt, trans.c, util.c).

## 3. Effective hook set — 69, override applied, identical to the frozen TSV

Method: baseline map from `/usr/share/libalpm/hooks/*.hook`, overlaid by basename with
`/etc/pacman.d/hooks/*.hook`, matching libalpm's loader: `hook.c:594-597`
(`if(find_hook(hooks, entry->d_name)) … "skipping overridden hook"`), where `find_hook`
compares `hook->name` (`hook.c:461-472`) and hook dirs are read in the order given by
pacman.conf — `/etc/pacman.d/hooks` before `/usr/share/libalpm/hooks`
(`alpm-hooks.5.asciidoc:35-39`). Live `/etc/pacman.conf` has no `HookDir` override
(only `[options]` at line 3), so the defaults hold.

Counts: `/usr/share/libalpm/hooks/*.hook` = **67**, `/etc/pacman.d/hooks/*.hook` = **3**,
overlap by basename = **1** (`90-mkinitcpio-install.hook`) → **69 effective hooks**.
No non-`.hook` entries and no subdirectories in either dir (`find … ! -name '*.hook'` empty),
so nothing is silently skipped.

Field-exact diff of my live table against `frozen/hostcap/hooks-needstargets.tsv`
(name, needs_targets, exec; 69 data rows each):

```
$ diff frozen.k3 live.k3 && echo IDENTICAL
IDENTICAL
```

Override is real, not cosmetic — the shadowed `/usr/share` copy differs in both triggers and
Exec (`diff -u /usr/share/libalpm/hooks/90-mkinitcpio-install.hook /etc/pacman.d/hooks/90-mkinitcpio-install.hook`):
`/usr/share` runs `Exec = /usr/share/libalpm/scripts/mkinitcpio install` and also triggers on
`usr/lib/systemd/systemd-udevd`, `usr/bin/mdadm`, `usr/lib/libcryptsetup.so`, … ; the effective
`/etc` copy runs `Exec = /usr/share/libalpm/scripts/limine-mkinitcpio-install` with 7 fewer
paths (`/etc/pacman.d/hooks/90-mkinitcpio-install.hook:30-31`).

### 14 effective hooks carrying `NeedsTargets` — names and Exec lines (verbatim)

| # | hook (effective path) | Exec |
|---|---|---|
| 1 | /usr/share/libalpm/hooks/10-limine-snapper-lock.hook | `/usr/share/libalpm/scripts/limine-snapper-lock` |
| 2 | /usr/share/libalpm/hooks/40-fontconfig-config.hook | `/usr/share/libalpm/scripts/40-fontconfig-config /etc/fonts/conf.d` |
| 3 | /usr/share/libalpm/hooks/60-depmod.hook | `/usr/share/libalpm/scripts/depmod` |
| 4 | /usr/share/libalpm/hooks/60-limine-mkinitcpio-remove-pre.hook | `/usr/share/libalpm/scripts/limine-mkinitcpio-remove pre` |
| 5 | /usr/share/libalpm/hooks/60-mkinitcpio-remove.hook | `/usr/share/libalpm/scripts/mkinitcpio remove` |
| 6 | /usr/share/libalpm/hooks/70-dkms-install.hook | `/usr/share/libalpm/scripts/dkms install` |
| 7 | /usr/share/libalpm/hooks/70-dkms-upgrade.hook | `/usr/share/libalpm/scripts/dkms -D remove` |
| 8 | /usr/share/libalpm/hooks/71-dkms-remove.hook | `/usr/share/libalpm/scripts/dkms remove` |
| 9 | **/etc**/pacman.d/hooks/90-mkinitcpio-install.hook | `/usr/share/libalpm/scripts/limine-mkinitcpio-install` |
| 10 | /usr/share/libalpm/hooks/dconf-update.hook | `/usr/share/libalpm/scripts/dconf-update` |
| 11 | /usr/share/libalpm/hooks/gtk-update-icon-cache.hook | `/usr/share/libalpm/scripts/gtk-update-icon-cache` |
| 12 | /usr/share/libalpm/hooks/gtk4-querymodules.hook | `/usr/share/libalpm/scripts/gtk4-querymodules` |
| 13 | /usr/share/libalpm/hooks/texinfo-install.hook | `/bin/sh -c 'while read -r f; do if test -f "$f"; then install-info "$f" /usr/share/info/dir 2> /dev/null; fi; done'` |
| 14 | /usr/share/libalpm/hooks/texinfo-remove.hook | `/bin/sh -c 'while read -r f; do install-info --delete "$f" /usr/share/info/dir 2> /dev/null; done'` |

Each of the 14 has exactly one `NeedsTargets` line and exactly one `Exec` line (no second
`Exec =` continuation in any of them), so the TSV's one-Exec-per-row shape is lossless.

**Raw-file count is 15, effective count is 14** — `NeedsTargets` appears in 15 `.hook`
files on disk (14 under `/usr/share`, 1 under `/etc`) because the overridden
`/usr/share/…/90-mkinitcpio-install.hook` carries it too but is never parsed. The frozen
"14 of 69" is correct only under the override rule; a naive `grep -r` over both dirs reports
15. That is precisely the C2 claim's point, and it is load-bearing here.

Token form check: `grep -rhoP '^NeedsTargets\s*$'` over both dirs → `15 NeedsTargets`
(one line each, no trailing-space or case variants), and no `NeedsTargets` appears inside a
comment (`grep -rn -i needstargets … | grep '#':` → none). The libalpm parser compares the
key literally (`hook.c:232`, `strcmp(key, "NeedsTargets") == 0`), so exact-case occurrences
are what count — all 14 effective ones qualify.

## 4. libalpm shell strings — index 1277 reproduces; `/bin/sh` is genuinely absent

Probe: `strings -a /usr/lib/libalpm.so.16.0.1 > live.txt` (GNU strings, binutils 2.47;
`LC_ALL=C`), 1713 lines total, then exact whole-line match.

* `/usr/bin/bash` → line **1277** (frozen: 1277). Same with `strings -d` and with default
  flags; identical under `LC_ALL=C`.
* `/usr/bin/ldconfig` → line **1263** (frozen anchor row: 1263).
* `/bin/sh` → **absent**, exit 1. `/usr/bin/sh` → absent. Raw byte scan for NUL-terminated
  literals confirms it: `b'/usr/bin/bash\x00'` found once at file offset **228470**
  (`0x37c76`), `b'/bin/sh\x00'` and `b'/usr/bin/sh\x00'` at **zero** offsets. No line
  containing `bin/sh` exists anywhere in the strings dump.

So the frozen file's shape is right: two rows (anchor + bash), no `/bin/sh` row, and the
EX4 host cell "carries `/usr/bin/bash` … and lacks `/bin/sh`"
(`pacman-exec-environment-r40.md:24`) is exactly what the live binary shows. The mechanism
is the packaging flag, not a bug: Arch builds with `-Dscriptlet-shell=/usr/bin/bash`
(`frozen/src/PKGBUILD:115`), overriding the upstream meson default `value : '/bin/sh'`
(`frozen/src/meson_options.txt:17-18`). Only the configured shell is compiled in, so the
upstream default never becomes a literal in this build.

**Index fragility (note for future rounds):** `1277` is a 1-based line number in
`strings(1)` output — it depends on binutils' string-extraction order and on the binary
build, so it is not a stable identifier across binutils or pacman versions. The
version-independent anchor for the same fact is file offset **228470** / `.rodata` vaddr
`0x37c76` of the sha256-pinned `libalpm.so.16.0.1`. Either way the frozen capture is
accurate for this host/build.

Cross-check that the two shell facts coexist without contradiction: 7 of the 69 effective
hooks invoke a shell in *their own Exec text* — `/bin/sh` ×6
(10-linux-modules-pre/post, 99-limine, gvfsd, texinfo-install/remove) plus `/usr/bin/sh` ×1
(shared-mime-info-remove-cache). Those paths come from the hook file, parsed by pacman and
executed as given; they never pass through libalpm's `SCRIPTLET_SHELL` literal, which is why
`/bin/sh` appearing in hooks and not appearing in `libalpm.so` is consistent.

## 5. Freshness

No hook file changed after the capture: `find /etc/pacman.d/hooks /usr/share/libalpm/hooks
-name '*.hook' -newermt '2026-10-26T06:54:46Z'` → empty (newest hook mtime overall is
2026-10-12T12:15:42Z). Combined with the field-exact TSV diff, the captured content and the
live content are the same, not merely the same count.

## 6. What I did not do

No counter was run (gate execution belongs to the parent), no package/service/hook/sysfs
touch, no `pacman` transaction, no sudo. I did not execute any hook. Hook *trigger* matching
semantics were not exercised live — only the loader/override rule was confirmed against the
pinned `hook.c`; the census fixtures covering that are C1's surface.

## Receipts

`.ufo/waves/round-40/w1/C2ExecHostRecheck/`:
`effective-hooks-live.tsv` (my re-derived 69-row table), `diff-frozen-vs-live.txt`,
`libalpm-shell-strings-live.txt` (indices + byte offset), `strings-a-libalpm-16.0.1.txt`
(full 1713-line dump), `manifest-verify.txt`.
Scratch `/fast/scratch/hyaku/tsukuroi-r40/C2ExecHostRecheck/` removed after copying
(`rm -rf`; verified gone). No tool installs or upgrades were needed.
