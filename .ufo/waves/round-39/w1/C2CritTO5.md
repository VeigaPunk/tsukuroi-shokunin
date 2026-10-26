VERDICT: defect-found

# Seat C2CritTO5 — attack on TO5's host column (item C2-6)

Target: `corpus/knowledge/pacman-transaction-order-r39.md:28`, TO5 last cell (host column), and the
boundary bullet at `:49-50`. Read-only on the lane; scratch under
`/fast/scratch/hyaku/tsukuroi-r39/C2CritTO5/` (removed at the end); receipts in
`.ufo/waves/round-39/w1/C2CritTO5/`.

## Summary

The two counting sentences of the host column **hold** (I re-derived 17/17 and the no-run claim).
The **reason given** for the hedge does not apply to all 17: 16 instances are vacuous, **one is
discriminating** — `10-limine-snapper-lock.hook` would have run in the very transaction that
installs its package, and the capture contains a same-hook control (it does run in Pre once on
disk) plus a Post-phase twin in the same transaction. The boundary bullet's blanket claim that
"the capture cannot separate 'the hook file was absent' from 'its triggers did not match'"
(`:49-50`) is **false for that instance**. The entry therefore under-claims, it does not overclaim;
its conclusion ("consistent, not proof") survives for a different reason than the one stated.

## A. Re-derivation of the 17 (holds)

Live scan, same dirs as the capture (`capture-meta.txt:3-5`):

- `/usr/share/libalpm/hooks`: 67 `*.hook`; `/etc/pacman.d/hooks`: 3 `*.hook`
  (`ls /usr/share/libalpm/hooks/*.hook | wc -l` = 67; `ls /etc/pacman.d/hooks/*.hook | wc -l` = 3).
- Files with `When = PreTransaction`: **17**, identical to the `PreTransaction` rows of
  `frozen/txcapture/hook-when.tsv` (checked by enumerating `grep -l "When *= *PreTransaction" *.hook`
  and diffing names). The three `/etc` hooks are all `PostTransaction`.
- Every one of the 17 owners has an `installed <pkg> (` line in `frozen/txcapture/pacman.log`;
  none of the 17 first appears as `upgraded`. So the sentence "17 PreTransaction hook files on this
  host are owned by a package that the capture shows first installed in some transaction" is true —
  and it is the whole Pre set, not a filtered subset, so the number is not evidence of a selection.

First-install transactions (`derive.py` / `table.py`, receipt `derivation-output.txt`). All six are
**install-only** (installed/upgraded/removed, `txstat.py`):

| window | first log line | command | adds–upg–rem |
|---|---|---|---|
| w0 | pacman.log:1 | `pacman -b /mnt/… -r /mnt -Sy … base …` | 157–0–0 |
| w5 | pacman.log:414 | `pacman -b /mnt/… -r /mnt -Sy …` (second bootstrap, config Dcus) | 38–0–0 |
| w7 | pacman.log:484 | `pacman -S --needed 1password-beta … kernel-modules-hook …` | 689–0–0 |
| w8 | pacman.log:1261 | `pacman -S --needed linux-headers nvidia-open-dkms …` | 60–0–0 |
| w10 | pacman.log:1344 | `pacman -S --needed limine-snapper-sync limine-mkinitcpio-hook` | 2–0–0 |
| w27 | pacman.log:2130 | `pacman -S --needed steam` | 32–0–0 |

"none of the 17 ran in that transaction's Pre phase" — **holds**. Pre phase = lines between the
`[PACMAN] Running` line and `transaction started`: w0 none (3), w5 none (416), w7 none (485),
w8 none (1262), w10 none (1345), w27 exactly one, `running '10-limine-snapper-lock.hook'...` at
pacman.log:2131 — which is not the owner hook of that window (`gio-remove-module-cache-32.hook`,
owner lib32-glib2, installed pacman.log:2148).

## B. Counterfactual: would each hook have matched, had the file existed?

Trigger text read from the live files (`/usr/share/libalpm/hooks/<name>`), matching semantics from
the pinned source: `_alpm_hook_trigger_match_pkg` frozen/src/hook.c:363-416 (a package with no
`oldpkg` is an INSTALL match; `targets` are `fnmatch`ed against the package name; REMOVE needs
`trans->remove`), `_alpm_hook_trigger_match_file` hook.c:258-355 (an `install` path is an UPGRADE
only if the same path is also in the remove set), `_alpm_hook_run_hook` Depends gate
hook.c:507-517.

| # | hook (live [Trigger]) | owner | owner's first `installed` | that tx | would it have matched? | ran in that Pre? | discriminating |
|---|---|---|---|---|---|---|---|
| 1 | `10-glibc-remove-locale-archive`: Package/Remove `glibc` | glibc | :9 (w0) | 157–0–0 | no — `Remove` vs install-only, `trans->remove` empty | no | no |
| 2 | `10-limine-snapper-lock`: Package/Install+Upgrade+Remove `*`, no Depends, NeedsTargets | limine-snapper-sync | :1346 (w10) | 2–0–0 | **yes** — `*` matches both targets, both `oldpkg==NULL` → INSTALL | no (nothing between :1344 and :1345) | **YES** |
| 3 | `10-linux-modules-pre`: Path/Install+Upgrade `usr/lib/modules/*/vmlinuz`, Depends `rsync` | kernel-modules-hook | :965 (w7) | 689–0–0 | no — the `vmlinuz`-bearing events are `linux` at pacman.log:246, `linux-lts` at :2540 and the `linux` upgrade at :2855, none of them in w7 (name scan of the 689 adds finds only `kernel-modules-hook`); and `rsync` is installed at :964 **inside this transaction**, so Depends is unmet at Pre (hook.c:509-516) | no | no |
| 4 | `10-openssh-mark-sshd-for-restart`: Package/Upgrade `openssh` | openssh | :725 (w7) | 689–0–0 | no — `Upgrade` vs install-only | no | no |
| 5 | `11-glibc-remove-ldconfig-cache`: Package/Remove `glibc` | glibc | :9 (w0) | 157–0–0 | no | no | no |
| 6 | `12-glibc-remove-iconvconfig-cache`: Package/Remove `glibc` | glibc | :9 (w0) | 157–0–0 | no | no | no |
| 7 | `12-lib32-glibc-remove-iconvconfig-cache`: Package/Remove `lib32-glibc` | lib32-glibc | :1273 (w8) | 60–0–0 | no | no | no |
| 8 | `60-limine-mkinitcpio-remove-pre`: Path/Remove `usr/lib/modules/*/modules.builtin` | limine-mkinitcpio-hook | :1347 (w10) | 2–0–0 | no — remove path set empty | no | no |
| 9 | `60-mkinitcpio-remove`: Path/Remove `…/vmlinuz`; Package/Remove `mkinitcpio`,`mkinitcpio-git` | mkinitcpio | :245 (w0) | 157–0–0 | no — the `vmlinuz` from :246 is in the install set, remove set empty | no | no |
| 10 | `70-dkms-upgrade`: Path/Upgrade `usr/src/*/dkms.conf` … Depends `dkms` | dkms | :1265 (w8) | 60–0–0 | no — install∩remove empty (`nvidia-open-dkms` is new at :1272); Depends `dkms` not in the local db at Pre | no | no |
| 11 | `71-dkms-remove`: Path/Remove same targets, Depends `dkms` | dkms | :1265 (w8) | 60–0–0 | no | no | no |
| 12 | `gdk-pixbuf-remove-loaders-cache`: Package/Remove `gdk-pixbuf2` | gdk-pixbuf2 | :521 (w7) | 689–0–0 | no | no | no |
| 13 | `gio-remove-module-cache-32`: Package/Remove `lib32-glib2` | lib32-glib2 | :2148 (w27) | 32–0–0 | no | no | no |
| 14 | `gio-remove-module-cache`: Package/Remove `glib2` | glib2 | :104 (w0) | 157–0–0 | no | no | no |
| 15 | `glib-remove-compiled-schemas`: Package/Remove `glib2` | glib2 | :104 (w0) | 157–0–0 | no | no | no |
| 16 | `gtk-remove-immodules-cache`: Package/Remove `gtk3` | gtk3 | :541 (w7) | 689–0–0 | no | no | no |
| 17 | `texinfo-remove`: Path/Remove `usr/share/info/*` | texinfo | :445 (w5) | 38–0–0 | no — remove set empty (the info files of :445 are in the install set) | no | no |

Tally: 13 `Operation = Remove` only, 2 `Operation = Upgrade` only → the operation filter alone
rejects their owner's install-only transaction; 1 (`10-linux-modules-pre`) fails on targets and on
Depends; **1 matches**.

## C. The discriminating instance, with controls

`10-limine-snapper-lock.hook` (live: `Operation = Upgrade|Install|Remove`, `Type = Package`,
`Target = *`, `When = PreTransaction`, `Exec = /usr/share/libalpm/scripts/limine-snapper-lock`,
`NeedsTargets`, **no Depends**).

Counterfactual for pacman.log:1344-1348: transaction adds `limine-snapper-sync` (:1346) and
`limine-mkinitcpio-hook` (:1347), both with `oldpkg == NULL`; `fnmatch("*", name)` matches; the
trigger carries INSTALL → `install` list non-empty → `_alpm_hook_triggered` returns 1
(hook.c:363-440); no Depends, so `_alpm_hook_run_hook` would have executed it (hook.c:507-517).
Had the file been on disk at Pre time, it would have logged `running '10-limine-snapper-lock.hook'...`
before `transaction started`. It did not: the Pre phase of w10 is empty (pacman.log:1344 → :1345).
The Pre abort path cannot explain it either: hook.c:629 skips the whole Pre phase when any dir
stat/parse/`opendir` fails, and every such failure logs `[ALPM] error: …`; the capture contains
**zero** `[ALPM] error` lines and no `unable to run hook … could not satisfy dependencies` line
(`grep -n "unable to run hook\|error:" pacman.log` → nothing), so the Pre phase completed cleanly.

Controls, all from the same frozen log:

1. **Same hook, present, same transaction class** — `pacman -S --needed steam` (install-only,
   32 adds), pacman.log:2130-2132: `running '10-limine-snapper-lock.hook'...` at :2131, before
   `transaction started` at :2132. So `_alpm_hook_run(PRE)` *is* called on install-only `-S`
   transactions and this hook's trigger does fire there.
2. **Immediately after the install** — next invocation, `pacman -U 1password-beta`
   (pacman.log:1397), Pre run at :1398. It matched a package unrelated to limine, which also
   shows the hook file installed by 1.30.1 already had the broad `Target = *`; version drift to the
   live 1.32.1 file cannot explain the w10 miss.
3. **Post twin in the same transaction** — `80-limine-efi-deploy.hook`, owner
   `limine-mkinitcpio-hook` (installed pacman.log:1347), ran at pacman.log:1352 in w10's Post
   phase. Its file also appeared only with that commit, and the Post scan saw it.

So the capture does separate "absent" from "triggers did not match" for instance 2, and the
Pre-miss/Post-hit pair inside one process also rules out a one-time parse reused for Post.

## D. Is "consistent, not proof" accurate, or does it overclaim?

- **It does not overclaim.** The conclusion is right: a log cannot exclude a hypothetical
  implementation that deliberately withholds hooks shipped by the transaction's own targets; only
  the source settles the mechanism.
- **Its stated reason is wrong for 1 of 17 and vacuous for 16.** "a Pre hook whose triggers did not
  match would not have run either" describes 16 instances; for `10-limine-snapper-lock.hook` the
  triggers *would* have matched, so the non-run is evidence, not a coincidence.
- **The boundary bullet (`:49-50`) is false as a blanket statement**: "the capture cannot separate
  'the hook file was absent' from 'its triggers did not match'" — it can, for the one instance
  above.
- Minor: the host column reads as if a subset of 17 was found; it is the complete Pre set (17 of
  17 hook files with `When = PreTransaction`), so the count carries no selectivity.

### Proposed replacement text (host column, cell 5 of TO5, no `|`)

`17 of 17 PreTransaction hook files on this host are owned by a package the capture first installs in one of six install-only transactions (pacman.log:9, :104, :245, :445, :521, :541, :725, :965, :1265, :1273, :1346, :1347, :2148); none ran in its owner's install transaction's Pre phase. Sixteen of the 17 are vacuous: 13 are 'Operation = Remove' and 2 'Operation = Upgrade' only, so the operation filter alone rejects an install-only transaction, and '10-linux-modules-pre.hook' needs 'usr/lib/modules/*/vmlinuz' from a target (the vmlinuz-bearing transactions are pacman.log:246, :2540 and :2855, none of them the transaction that installs kernel-modules-hook) plus 'Depends = rsync', which its own transaction still installs at pacman.log:964. One is discriminating: '10-limine-snapper-lock.hook' ('Type = Package', 'Operation = Install', 'Target = *', no Depends) would have matched the transaction that installs 'limine-snapper-sync' and did not run before 'transaction started' (pacman.log:1344-1345); it does run in Pre of the next invocation (pacman.log:1397-1398) and of a later install (pacman.log:2130-2131), and the same transaction's Post phase ran '80-limine-efi-deploy.hook', whose owner is installed at pacman.log:1347 (pacman.log:1352). The capture therefore separates 'file absent' from 'triggers did not match' for that hook; what it cannot exclude is an implementation that withholds hooks shipped by the transaction's own targets, so the row remains consistency, not proof.`

### Proposed replacement text (boundary bullet, `:49-50`)

`- TO5's host column is consistency, not proof, but not uniformly vacuous: 16 of the 17 instances cannot distinguish "the hook file was absent" from "its triggers did not match" (13 are 'Operation = Remove', 2 'Operation = Upgrade', and '10-linux-modules-pre.hook' needs a kernel target plus 'rsync'), while '10-limine-snapper-lock.hook' ('Target = *', 'Operation = Install') would have run in the transaction that installs it and did not (pacman.log:1344-1345), then runs in Pre as soon as it is on disk (pacman.log:1397-1398, 2130-2131). What the log alone cannot exclude is a design that deliberately withholds hooks shipped by the transaction's own targets; the per-call directory read is settled by the source, not the log.`

## E. Anchor note and what I did not do

- The cited quote is genuine: frozen/src/hook.c:540 contains
  `for(i = alpm_list_last(handle->hookdirs); i; i = alpm_list_previous(i)) {`, inside the cited
  532-560, with `opendir(path)` at hook.c:554 as the cell states; the Pre call site and
  `transaction started` ordering are at frozen/src/trans.c:203-209, Post at trans.c:235-239.
- I did **not** judge the truth of the TO5 rule text beyond the quote's location; the C2 kill rule
  asks reviewers to judge the rule, my item judges the host column.
- I did **not** run pacman, touch the host, install any tool, or use sudo; nothing outside
  `/fast/scratch/.../C2CritTO5/` and the two permitted write paths. Scratch removed after
  receipts were copied. `pacman-conf HookDir` prints `/etc/pacman.d/hooks/`; hooks from
  `/usr/share/libalpm/hooks` demonstrably ran (e.g. pacman.log:1398), so both dirs are in
  `handle->hookdirs`.
- Residual uncertainty I cannot remove from the log alone: whether `/var/log/pacman.log` was
  rotated before 2026-10-03 (the capture copied only the live file, `capture-meta.txt:2`); the
  first line being a fresh `base` bootstrap into `/mnt` makes truncation implausible but unproven,
  and the entry's wording "the capture shows" is already scoped to the file.

TO5: holds — hook.c:540 (quote verbatim inside the cited 532-560; `opendir` at hook.c:554)
