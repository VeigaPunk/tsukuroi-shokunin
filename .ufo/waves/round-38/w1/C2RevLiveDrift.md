VERDICT: supports

Item C2-9 — live drift + 12-row spot check against `corpus/knowledge/pacman-hook-order-r38.md`.
Date of all live checks: 2026-10-26 (this session).

## 1. Live drift: host hooks vs frozen capture

Chain: manifest digest observed now equals the digest the doc claims.
- `sha256sum .ufo/waves/round-38/frozen/hooks-capture/MANIFEST.sha256` →
  `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`
  = claim at `corpus/knowledge/pacman-hook-order-r38.md:3`.
- Capture provenance: `capture-meta.txt:1` "captured 2026-10-26T04:11:58Z host=plazir27 read-only"; `:3` `pacman 7.1.0.r9.g54d9411-3`; `:5` `pacman-conf HookDir` → `/etc/pacman.d/hooks/`. Doc `:4` says "verified-at: 2026-10-26 (capture 2026-10-26T04:11:58Z)". No drift in provenance.

Command and observed output:

```
$ cd /usr/share/libalpm/hooks && sha256sum *.hook | sed 's#  #  usr-share-libalpm-hooks/#' \
  > live-usr.txt
$ cd /etc/pacman.d/hooks && sha256sum *.hook | sed 's#  #  etc-pacman.d-hooks/#' > live-etc.txt
$ diff <(LC_ALL=C sort -k2 MANIFEST.sha256) <(LC_ALL=C sort -k2 live-usr.txt live-etc.txt)
NO-DIFFERENCE
```

Counts observed: live usr 67, live etc 3, manifest usr 67, manifest etc 3 (70 total both sides).
No extra or missing files; `find /usr/share/libalpm/hooks /etc/pacman.d/hooks -maxdepth 1 ! -name '*.hook'`
found 0 non-`.hook` entries in each dir, so the `*.hook` glob missed nothing.

**Result: zero live drift.** All 70 live hook files are byte-identical (sha256) to the frozen
capture taken 2026-10-26T04:11:58Z (`capture-meta.txt:1`). (Receipts:
`.ufo/waves/round-38/w1/C2RevLiveDrift/live-{usr,etc,sha256-sorted}.txt`.)

## 2. Twelve-row spot check vs live `[Action]`

Agreement criterion: table `when`/`dir` must equal the live `When =`; table `abort`/`needs` must
match absence/presence of `AbortOnFail`/`NeedsTargets`; table `exec` must equal the live `Exec =`
or be its leading token (the table stores the interpreter/binary; e.g. row `99-limine` stores
`/bin/sh` for a longer `/bin/sh -c ...` line — same convention used throughout the table).

Selection covers every named category: row for the etc 90-mkinitcpio-install file (the usr twin is
masked, see §3), 99-limine, walker-restart, the three -32 pairs (6 rows), two NeedsTargets rows,
and the first and last Pre rows. Doc lines below are in
`corpus/knowledge/pacman-hook-order-r38.md`; live lines are in the named file.

| doc:line | row (when pos name dir abort needs exec) | live evidence | result |
|---|---|---|---|
| :34 | Pre 1 `10-glibc-remove-locale-archive.hook` usr no no `/usr/bin/rm` | `/usr/share/libalpm/hooks/10-glibc-remove-locale-archive.hook:9-10` Exec=`/usr/bin/rm --force /usr/lib/locale/locale-archive`, When=PreTransaction; no NeedsTargets/AbortOnFail | **agree** |
| :35 | Pre 2 `10-limine-snapper-lock.hook` usr no yes `/usr/share/libalpm/scripts/limine-snapper-lock` | `/usr/share/libalpm/hooks/10-limine-snapper-lock.hook:13-15` When=PreTransaction, Exec same, NeedsTargets; no AbortOnFail | **agree** |
| :69 | Post 26 `90-mkinitcpio-install.hook` **etc** no yes `/usr/share/libalpm/scripts/limine-mkinitcpio-install` | `/etc/pacman.d/hooks/90-mkinitcpio-install.hook:29-31` When=PostTransaction, Exec same, NeedsTargets; no AbortOnFail | **agree** |
| :71 | Post 28 `99-limine.hook` etc no no `/bin/sh` | `/etc/pacman.d/hooks/99-limine.hook:9-10` When=PostTransaction, Exec=`/bin/sh -c "cp ... BOOTIA32.EFI ... BOOTX64.EFI ..."` (prefix `/bin/sh`); no NeedsTargets/AbortOnFail | **agree** |
| :75 | Post 32 `fontconfig.hook` usr no no `/usr/bin/fc-cache` | `/usr/share/libalpm/hooks/fontconfig.hook:13-14` When=PostTransaction, Exec=`/usr/bin/fc-cache -s` (prefix); no NeedsTargets/AbortOnFail | **agree** |
| :76 | Post 33 `fontconfig-32.hook` usr no no `/usr/bin/fc-cache-32` | `/usr/share/libalpm/hooks/fontconfig-32.hook:13-14` When=PostTransaction, Exec=`/usr/bin/fc-cache-32 -s` (prefix); none | **agree** |
| :79 | Post 35 `gio-querymodules.hook` usr no no `/usr/bin/gio-querymodules` | `/usr/share/libalpm/hooks/gio-querymodules.hook:10-11` When=PostTransaction, Exec=`/usr/bin/gio-querymodules /usr/lib/gio/modules` (prefix); none | **agree** |
| :80 | Post 36 `gio-querymodules-32.hook` usr no no `/usr/bin/gio-querymodules-32` | `/usr/share/libalpm/hooks/gio-querymodules-32.hook:10-11` When=PostTransaction, Exec=`/usr/bin/gio-querymodules-32 /usr/lib32/gio/modules` (prefix); none | **agree** |
| :81 | Pre 13 `gio-remove-module-cache.hook` usr no no `/usr/bin/rm` | `/usr/share/libalpm/hooks/gio-remove-module-cache.hook:8-9` When=PreTransaction, Exec=`/usr/bin/rm --force /usr/lib/gio/modules/giomodule.cache` (prefix); none | **agree** |
| :82 | Pre 14 `gio-remove-module-cache-32.hook` usr no no `/usr/bin/rm` | `/usr/share/libalpm/hooks/gio-remove-module-cache-32.hook:8-9` When=PreTransaction, Exec=`/usr/bin/rm --force /usr/lib32/gio/modules/giomodule.cache` (prefix); none | **agree** |
| :99 | Pre 17 `texinfo-remove.hook` usr no yes `/bin/sh` (last Pre; NeedsTargets) | `/usr/share/libalpm/hooks/texinfo-remove.hook:8-10` When=PreTransaction, Exec=`/bin/sh -c 'while read -r f; do install-info --delete ...'` (prefix), NeedsTargets; no AbortOnFail | **agree** |
| :101 | Post 52 `walker-restart.hook` etc no no `/home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker` | `/etc/pacman.d/hooks/walker-restart.hook:10-11` When=PostTransaction, Exec exact match; none | **agree** |

**12/12 rows agree.** No disagreement found; nothing to report as drift in the table itself.

Incidental corroboration from the same grep pass (not a recount): 0 of the 13 inspected files carry
`AbortOnFail`, consistent with doc `:13` ("0 with `AbortOnFail`") and HO4 (`:24`); NeedsTargets
present on exactly the rows that claim it (:35, :69, :99 of my set), consistent with doc `:13`
("14 with `NeedsTargets`") for the sampled subset.

## 3. Both 90-mkinitcpio-install files (HO2 consequence)

The table has only ONE row for the name `90-mkinitcpio-install.hook` — the etc file (:69) — because
HO2 (`:22`) says same-name files: the etc HookDir entry wins and the usr one is masked. Verified on
the live pair:

- `/etc/pacman.d/hooks/90-mkinitcpio-install.hook:30` → Exec
  `/usr/share/libalpm/scripts/limine-mkinitcpio-install` — the winner; row :69 records dir=etc and
  exactly this Exec. sha256 `a0689d02...` = MANIFEST line 1.
- `/usr/share/libalpm/hooks/90-mkinitcpio-install.hook:37` → Exec
  `/usr/share/libalpm/scripts/mkinitcpio install` — different Exec, NeedsTargets at :38; correctly
  absent from the table (no usr row). sha256 `9fc607e8...` = MANIFEST line 40.

So "both files" are accounted for: one effective row + one correctly-masked file, and the live
Exec split is exactly the override the doc describes. This also confirms the doc's count
`69 effective hooks from 70 files (one same-name override)` (`:13`) for this name.

## 4. Not done / residual

- Did not re-run `tools/check-hook-order-r38.py` (doc `:4` recheck command) — that is the C2
  counter's job, not item C2-9.
- Did not verify the remaining 57 table rows or recount NeedsTargets=14/AbortOnFail=0 host-wide;
  §2 is a 12-row spot check by assignment.
- Did not check pacman.log `running` sequences (HO7 oracle, `:27`).
- Live hashing is point-in-time (2026-10-26, this session); a pacman transaction after this check
  can invalidate it. The doc's own recheck trigger ("on-release of pacman for S208–S211", `:4`)
  remains the right guard.
- `pacman -Q pacman` not re-run by me; version claim `7.1.0.r9.g54d9411-3` taken from
  `capture-meta.txt:3` (capture-time), not re-observed today.

## 5. Receipts

- `.ufo/waves/round-38/w1/C2RevLiveDrift/live-sha256-sorted.txt` — live `sha256sum *.hook` for both
  dirs, path-prefixed, `LC_ALL=C sort -k2` (the exact left side of the NO-DIFFERENCE diff).
- `.ufo/waves/round-38/w1/C2RevLiveDrift/live-usr.txt`, `live-etc.txt` — raw per-dir hash outputs.

Scratch `/fast/scratch/hyaku/tsukuroi-r38/C2RevLiveDrift/` removed after receipt copy. No lane
tracked file was read-modified; the only lane writes are this report and the receipt dir. No tools
were installed (none needed); no pacman transaction attempted (host-wide pause honored); no sudo.
