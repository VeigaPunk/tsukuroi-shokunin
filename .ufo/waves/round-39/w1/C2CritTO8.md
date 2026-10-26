VERDICT: supports

# C2-7 — attack on TO8's host consequence

Row under attack (corpus/knowledge/pacman-transaction-order-r39.md:31, frozen claim, commit 4078eb2):

> TO8 | … | S216 util.c:521-528 … | 252 of 441 `[ALPM-SCRIPTLET]` lines in the frozen pacman.log lie outside
> every commit phase, so they are hook output, not scriptlet output

Claim attacked: cross the tag line's phase and you cross its producer. I tried to put an install-scriptlet
line outside a commit window (failed/interrupted windows, commands with no `transaction started`, log
rotation, interleaved processes) or a hook line inside one. **Every route is closed in this capture, and
the source closes the ones the capture cannot exercise.** No misattribution in the ten sampled lines or in
the remaining 242.

Evidence base (read-only):
- log `.ufo/waves/round-39/frozen/txcapture/pacman.log`, sha256 `0845c1df…b1a4fc67` (matches
  `MANIFEST.sha256`), 3254 lines, mtime 2026-10-25 13:12:06.98 per `capture-meta.txt:2`
- `hook-when.tsv` sha256 `5d56d412…a24d34c41`
- source snapshots `.ufo/waves/round-39/frozen/src/{trans,hook,util,add,remove}.c` (pinned 54d9411)
- reproducible receipt: `.ufo/waves/round-39/w1/C2CritTO8/to8-attack.py`, output
  `.ufo/waves/round-39/w1/C2CritTO8/to8-attack.out`
  (`cd .ufo/waves/round-39/w1/C2CritTO8 && python3 to8-attack.py > to8-attack.out`, exit 0)

## 1. The 252/441 count recomputed

State machine identical to `tools/check-transaction-order-r39.py:105-130` (`Running '…'` → pre,
`transaction started` → commit, `completed|failed|interrupted` → post):

```
commands 86   transactions_started 60   completed 60   failed/interrupted 0
scriptlet_total 441   inside 189   outside 252
running '<hook>' lines while state==commit: 0
[PACMAN] Running lines while state==commit: 0
```

441 = `grep -c ALPM-SCRIPTLET` (441), so the counter's regex loses nothing; 189+252 = 441. The literal
`252 of 441` therefore matches the log, and the doc's cell carries exactly that string (line 31).

Inside-side sanity: all 189 inside lines sit directly under an `installed`/`upgraded` line
(161 / 28, no exceptions, no inside line whose block antecedent is a `running '…'` line), i.e. they are
package-scriptlet output — e.g. `[ALPM-SCRIPTLET] gpg: setting ownertrust to 4` at
`pacman.log:202` in archlinux-keyring's post_install (after `installed archlinux-keyring`, pacman.log:197)
inside the base transaction, and `==> NOTICE: tar backup/restore
scripts have been moved` at `pacman.log:1441` after `upgraded tar` (pacman.log:1440) inside
`transaction started` (pacman.log:1424)…`transaction completed`.

## 2. Outside-side attribution: 252/252 land in a hook block, 0 orphans

Block model (`running '<name>'` + the immediately following contiguous ALPM-SCRIPTLET lines; hooks are
serial — hook.c:651-660 logs `running '%s'...` at hook.c:653 then runs the hook at hook.c:660):

```
outside lines mapped to a hook block: 252 / 252
hook blocks with output: 50      distinct hook names: 15
post-tx lines: 243 (48 blocks)   pre-tx lines: 9 (2 blocks, 71-dkms-remove.hook)
When-vs-position mismatches against hook-when.tsv: 0
nearest-antecedent classes for the 252: {'hook': 252} — zero preceded by a PACMAN/ALPM non-hook line
per hook: 90-mkinitcpio-install 147, 20-systemd-sysusers 23, 80-limine-efi-deploy 17,
70-dkms-install 12, 10-linux-modules-post 10, 71-dkms-remove 9, 30-systemd-daemon-reload-system 7,
10-glibc-locale-gen 6, dbus-reload 5, 35-systemd-udev-reload 4, 90-update-appstream-cache 4,
30-systemd-daemon-reload-user 3, walker-restart 3, 25-systemd-sysctl 1, luarocks-make-manifest-5.1 1
```

## 3. Ten sampled lines, each attributed by its neighbouring `running` line

| # | log line | line text (truncated) | `running` line | hook | position / declared When |
|---|---|---|---|---|---|
| 1 | 253 | `Creating group 'alpm' with GID 970.` | 252 | 20-systemd-sysusers.hook | post-tx / PostTransaction |
| 2 | 402 | `Creating user 'avahi' … with UID 969` | 400 | 20-systemd-sysusers.hook | post-tx / PostTransaction |
| 3 | 1328 | `  Skipped: Running in chroot.` | 1327 | 30-systemd-daemon-reload-system.hook | post-tx / PostTransaction |
| 4 | 1376 | `  -> Running build hook: [modconf]` | 1362 | 90-mkinitcpio-install.hook | post-tx / PostTransaction |
| 5 | 1960 | `+ rm -rf /usr/lib/modules/backup` | 1955 | 10-linux-modules-post.hook | post-tx / PostTransaction |
| 6 | 2008 | `  -> Running build hook: [encrypt]` | 1989 | 90-mkinitcpio-install.hook | post-tx / PostTransaction |
| 7 | 2948 | `+ KVER=7.2.3-arch1-3` | 2946 | 10-linux-modules-post.hook | post-tx / PostTransaction |
| 8 | 2998 | `  -> Running build hook: [kms]` | 2983 | 90-mkinitcpio-install.hook | post-tx / PostTransaction |
| 9 | 3026 | `==> WARNING: Possibly missing firmware for module: 'xhci_pci_renesas'` | 2983 | 90-mkinitcpio-install.hook | post-tx / PostTransaction |
| 10 | 3124 | `Running as unit: run-p371567-i306456.service; …` | 3123 | walker-restart.hook | post-tx / PostTransaction |

Content matches producer in all ten: sysusers `Creating group/user`, systemd's own chroot skip line,
mkinitcpio's `-> Running build hook`/firmware warning, `10-linux-modules-post.hook`'s traced shell
(`+ KVER=…`, `+ rm -rf …`), and `systemd-run`'s `Running as unit:` from `walker-restart.hook`.
Neighbour context, e.g. `pacman.log:251-254`:

```
251 [ALPM] transaction completed
252 [ALPM] running '20-systemd-sysusers.hook'...
253 [ALPM-SCRIPTLET] Creating group 'alpm' with GID 970.
254 [ALPM-SCRIPTLET] Creating user 'alpm' (Arch Linux Package Management) with UID 970 and GID 970.
```

**Misattribution found in the sample: 0. In the full 252: 0.**

## 4. The four escape routes, each tested

**(a) Failed / interrupted windows — 0 markers in this capture, closed by source.**
`grep -cE '\[ALPM\] transaction (failed|interrupted)' pacman.log` → `0`; 60 `started` / 60 `completed`.
`trans.c:216` and `trans.c:224` log `transaction failed` and `return -1` *before* any
`_alpm_hook_run(POST)`; `trans.c:231` logs `transaction interrupted` in the branch that also skips
Post hooks (Post hooks only in the `else` at `trans.c:235-239`). The only other writers after a marker are
therefore nothing at all until the next command. Any scriptlet output of an aborted transaction is read to
EOF inside the window, before the marker.

**(b) Commands with no `transaction started` — 26 commands, 0 scriptlet lines.**
`commands_without_transaction` = lines 1413, 2096, 2103, 2110, 2129, 2251, 2286, 2287, 2422, 2461, 3091,
3125, 3169, 3177, 3178, 3186, 3187, 3188, 3190, 3191, 3206, 3213, 3232, 3233, 3245, 3246 (`-D`, `-Sw`,
`-Sc`, `-Scc`, `-Sy`, and four `-S`/`-Syu` invocations that exited before a commit (1413, 2110, 2251,
2286; e.g. pacman.log:2110). Sum of
`[ALPM-SCRIPTLET]` lines inside those 26 windows: **0**. Scriptlets only run from
`add.c:472`/`add.c:644`/`remove.c:711`/`remove.c:731` → `trans.c:410`, all inside `_alpm_sync_commit` /
`_alpm_remove_packages`, i.e. between `started` and the terminal marker (trans.c:208-235). Same for
`ldconfig` (add.c:691, remove.c:794 → util.c:833), so ldconfig output cannot be outside either.

**(c) Log rotation — no cut inside a phase or hook block.**
First line is a command (`[PACMAN] Running 'pacman -b /mnt/… base …'`), last line is
`[ALPM] running '35-systemd-update.hook'...` with no output, and the file's mtime equals the last log
timestamp, so neither head nor tail is a truncation point. The one visible seam is a timezone/root join:
`pacman.log:478` `running 'texinfo-install.hook'...` (+0000, the `-r /mnt` install) → `pacman.log:479`
`[PACMAN] Running 'pacman -S --noconfirm --needed gum'` (−0300). The seam is at a command boundary:
no transaction and no hook block spans 478/479. Outside-line split: 37 lines in the +0000 region,
215 in the −0300 region.

**(d) Interleaved processes — no evidence, and serial by construction.**
Offset-aware timestamp parse: **0 inversions** over 3254 lines. **0** `[PACMAN] Running` lines inside a
commit window, and **0** inside a hook block (which is why every one of the 252 has a hook antecedent).
`running` lines while in commit: **0**. Hooks run serially (hook.c:651-660 loop), so the nearest preceding
`running` line is the only possible producer of the following block. A grandchild outliving its hook
cannot leak into the window: `_alpm_run_chroot` reads the child pipe to EOF, so its output is consumed
before the hook call returns (util.c:521-529 writer; hook.c:525-528 routes hook output there).

**(e) The reverse direction — a hook line inside a commit phase: 0.**
All 189 inside lines have an `installed`/`upgraded` antecedent, never a `running '…'` one; no
`_alpm_hook_run` call site exists inside the window (only trans.c:202 Pre and trans.c:238 Post, both
outside `started`/marker). The sole writer of the tag is util.c:527 (`_alpm_chroot_process_output`,
util.c:521), i.e. every `[ALPM-SCRIPTLET]` line is a chroot child's output, and the only chroot children
are hooks (outside), scriptlets and ldconfig (inside).

## 5. Caveats — none of them move the number

1. **9 of the 252 are PreTransaction output**, not Post: `71-dkms-remove.hook` (declared
   `PreTransaction` in hook-when.tsv), `pacman.log:1421` (2 lines, `pacman.log:1422-1423`) and
   `pacman.log:2470` (7 lines, `pacman.log:2471-2477`), each followed by `transaction started`
   (`pacman.log:1424`, `pacman.log:2479` after `texinfo-remove.hook` at 2478). They are hook
   output outside the window; a reader who takes the 252 as "post-transaction hook output" would be wrong
   about those nine.
2. **Name-level, not file-level, attribution.** `90-mkinitcpio-install.hook` exists twice —
   `/usr/share/libalpm/hooks` (owner mkinitcpio) and `/etc/pacman.d/hooks` (owner
   limine-mkinitcpio-hook), both `PostTransaction` (hook-when.tsv / hook-owners.tsv). The log carries only
   the name, so the 147 lines cannot be split between the two files. No transaction ran both back to back
   (the only consecutive same-name `running` pair in the log is `35-systemd-update.hook` at 304/311, both
   silent). Content points both ways (`Building UKI …` / `omarchy_hooks.conf` is the limine hook), so
   per-file counts would be an over-claim; per-hook counts are not.
3. **Content cannot decide the producer; only the window can.** `Creating group …` appears both outside
   (sysusers hook, `pacman.log:253`) and inside (systemd's own install scriptlet in the base install,
   `pacman.log:125-144` after `installed systemd`), and `gpg:` (26 lines) is inside-only. The claim is safe
   because it uses phase, not text — but any reuse of this number as "these lines look like hook output"
   would be unsound.
4. **Scope of the source check**: the six frozen files only. No `_alpm_hook_run` caller outside trans.c
   exists in that set; a caller elsewhere upstream would need the wider tree.

## 6. Impacted axes and smallest safe correction

- Axis: C2 depth. The attack returns no counterexample: the count is exact under the counter's own window
  rule, and the attribution survives all 252 lines plus the ten sampled. The four named escape routes are
  empty in this capture (0 failed/interrupted windows, 0 scriptlet lines in the 26 no-transaction commands,
  no rotation cut, 0 interleavings), and source closes the route the capture cannot exercise.
- **Smallest safe correction: none required.** The cell's number and wording stand as written; the only
  wording nit that would not disturb the counter-checked substring `252 of 441` is "…lie outside every
  commit phase (9 of them before `transaction started`), so they are hook output" — optional, and not a
  defect.

TO8: holds — util.c:527 (sole `ALPM-SCRIPTLET` writer; quote present within the cited 521-528 range), host-consequence count reproduced 252/441 at pacman.log:253-479
