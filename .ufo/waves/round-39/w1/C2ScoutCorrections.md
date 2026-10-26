VERDICT: defect-found

Seat C2ScoutCorrections, item C2-14 (corrections sweep against TO1–TO8). Read-only; nothing in the lane edited. Line numbers are of the working tree at HEAD 394e1ba (SKILL.md and PROVINCE.md carry uncommitted round-39 C1 appends after line 3203 only; every line cited below is above that).

## Basis (what I re-derived before judging)

- `[ALPM-SCRIPTLET]` is the tag `_alpm_chroot_process_output` puts on every line a chroot child prints: `alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);` — `.ufo/waves/round-39/frozen/src/util.c:527`. Hooks reach it via `_alpm_run_chroot` (`hook.c:525-528`), `ldconfig` via `util.c:833`. The child's stdout **and** stderr are dup'd onto that pipe (`util.c:665-666`), and the child's own failure text (`could not change the root directory`, `call to execv failed`) is `fprintf(stderr…)` in the child, so it too is logged as `ALPM-SCRIPTLET` (`util.c:680,684,700`). Only libalpm's parent-side `_alpm_log(ERROR…)` lines (`command failed to execute correctly` `util.c:789`; `unable to run hook … could not satisfy dependencies` `hook.c:513`; hook validation errors) are stderr-only.
- Phase positions: Pre hooks before `transaction started` (`trans.c:201-208`), Post hooks after `transaction completed` (`trans.c:235-239`). Reproduced from the frozen capture (`receipts.txt`, sha256 of the frozen log 0845c1df…): 441 `ALPM-SCRIPTLET` lines, 252 outside every commit window — matches TO8's host cell.
- Host witnesses used below (frozen `pacman.log`): `transaction completed` 1950 → `running '70-dkms-install.hook'` 1977 → `ALPM-SCRIPTLET ==> dkms install … nvidia/610.57.04 -k 7.1.4-arch1-1` 1978 and `-k 7.2.3-arch1-3` 1979; `running '90-mkinitcpio-install.hook'` 2983 → `ALPM-SCRIPTLET Updated: /boot/limine.conf` 3015, 3047 (and 1989 → 2021). Genuine package scriptlet output also exists inside the commit (e.g. tar NOTICE 1441-1450 between `transaction started` 1424 and `transaction completed` 1950), so the tag cannot be read either way without position.

## Findings — statements TO8 (and TO1) correct

Ranked: W = wrong as written; L = loosely worded (true only under a reading the text does not state).

### 1. W — `SKILL.md:3198-3200` (limits bullet of the round-38 hook-order section)
Current text: "**Silence in `pacman.log` is weak evidence.** Only `alpm_logaction` lines reach it (`hook.c:653`; `trans.c:208`, `:231`, `:235`); validation and exec failures are stderr-only, so a missing log line never proves a hook succeeded."
Why wrong: the cited list is not the set of log writers. A hook's own stdout/stderr, including exec-failure text from the child, reaches `pacman.log` as `ALPM-SCRIPTLET` lines (`util.c:527`, `:666`, `:700`), tagged with no hook name. The conclusion (silence is weak evidence) stands; the premise and the "exec failures are stderr-only" half do not.
Append-only correction sentence: "Round-39 correction (TO8): the line list above is incomplete — every line a hook prints, stdout and stderr, and the child-side text of an exec or chroot failure reaches `pacman.log` as `[ALPM-SCRIPTLET]` (`util.c:527`, `:666`, `:700`) under the hook's `running '<name>'...` line; only libalpm's own parent-side errors (`command failed to execute correctly`, dependency and validation errors) stay on stderr, so a hook that fails before it prints anything still leaves no log line."

### 2. W (partly) — `SKILL.md:3183` (HO6 row, "Meaning" cell tail)
Current text: "…a Post hook's own failure is dropped (`trans.c:238`) and reaches stderr, not `pacman.log`".
Why: the exit status is dropped and libalpm's "command failed" line is stderr-only, but whatever the failed hook printed is logged as `[ALPM-SCRIPTLET]` after its `running` line (TO8). Read as "nothing of a failed Post hook reaches the log" it is false.
Append-only correction sentence: "Round-39 correction (TO8): a failed Post hook's exit status is dropped and libalpm's failure message is stderr-only, but any text the hook printed is in `pacman.log` as `[ALPM-SCRIPTLET]` lines after its `running '<name>'...` line (`util.c:527`); look there for the cause."

### 3. W — `corpus/knowledge/driver-firmware-plane.md:79-80`
Current text: "`[2026-10-11T16:14:37-0300] [ALPM] upgraded nvidia-open-dkms (610.43.03-3 -> 610.57.04-1)`; DKMS scriptlets built `nvidia/610.57.04` for `7.1.4-arch1-1` and `7.2.3-arch1-3` on the same day."
Why wrong: the builds were run by `70-dkms-install.hook`, a PostTransaction hook (`pacman-hook-order-r38.md:63`), after `transaction completed` — frozen log 1950, 1977, 1978, 1979. They are not install scriptlets and the "upgraded" line at 1911 is not where they ran. (`degraded-triage-r4.md:229-230` already has the correct hook attribution; this row contradicts it.) Lines 276-283 already supersede the versions but not the word.
Append-only correction sentence: "Round-39 correction (TO8, TO1): the `dkms install` builds of 2026-10-11 were run by the PostTransaction hook `70-dkms-install.hook` after `transaction completed` (`pacman.log` 1950, 1977-1979 of the frozen copy), not by DKMS install scriptlets; the `[ALPM-SCRIPTLET]` tag on their output marks chroot-child output, not a package scriptlet."

### 4. L — "in the transaction" for PostTransaction hooks (order contradicted by TO1)
TO1: the Post phase runs after `transaction completed` is logged, and on this host 0 `running '<hook>'` lines fall inside a commit window. A reader taking "in the transaction" as the logged `transaction started`…`completed` window, or as a guarantee that follows the commit, is wrong; an interrupted or failed commit runs no Post hook (HO6).
Locations and current text:
- `corpus/knowledge/update-safety-note.md:235` — "**user-owned, operator-writable script run by root inside the transaction**" (walker-restart.hook; PostTransaction, `pacman-hook-order-r38.md:101`).
- `corpus/knowledge/update-safety-note.md:298-300` — "a wave that raises `linux` triggers the dkms rebuild + initramfs hook in the same transaction."
- `corpus/knowledge/update-safety-v2.md:219` and `corpus/knowledge/update-safety-v3.md:240` — "a kernel-raising wave rebuilds in-transaction via `90-mkinitcpio-install.hook`."
- `corpus/knowledge/host-health-report-r3.md:321-322` — "a kernel-raising wave triggers the DKMS rebuild + initramfs hooks in the same transaction."
- `corpus/knowledge/degraded-triage-r4.md:357-358` — "a kernel wave means initramfs + UKI + DKMS in one transaction."
Judgement: loosely worded. True at the level of one `pacman` command (one `[PACMAN] Running` window); not true of the logged transaction window, and silent about the dependency on the commit finishing. The 70-dkms-install and 90-mkinitcpio-install hooks are Post (`pacman-hook-order-r38.md:63,69`); their output lands after `transaction completed` (frozen log 1950→1977, 2983→3015).
Append-only correction sentence (same text for each location): "Round-39 clarification (TO1, TO8): these hooks are PostTransaction hooks; they run after `transaction completed` is logged, within the same `pacman` command but not inside the logged `transaction started`…`completed` window, and none of them runs if the commit is interrupted or fails (`trans.c:230-239`, HO6); their output is logged as `[ALPM-SCRIPTLET]`."
The `update-safety-note.md:235` row needs only: "… run by root after `transaction completed` (PostTransaction, TO1), not inside the commit."

### 5. L — "ALPM-SCRIPTLET events / writes" for hook output (boot-writer attribution)
All three limine events sit after `transaction completed` and after `running '90-mkinitcpio-install.hook'` (frozen log 1989→2021; 2983→3015, 3047), so they are PostTransaction-hook output, not scriptlet output. The wording is loose, not false: the surrounding rows already name the hook as the writer class.
- `SKILL.md:2012` — "plus 3 ALPM-SCRIPTLET events in the whole pacman.log (`r19b:1695`, `1700`, `1702`; pacman.log 2021, 3015, 3047)"
- `SKILL.md:2022` — writer-table row heading "`ALPM-SCRIPTLET] Copied: … ] then `ALPM-SCRIPTLET] Updated: /boot/limine.conf`" (row body correctly says W-MKINITCPIO-HOOK)
- `corpus/QUALITY.md:70` — "ALPM-SCRIPTLET writes at pacman.log 2021, 3015, 3047"
- `corpus/knowledge/boot-writers-r19.md:40` ("Signature: [obs] ALPM-SCRIPTLET `==> Creating unified kernel image`…"), `:68,70,71` (event-table cells "`[ALPM-SCRIPTLET] (pacman.log …)`"), `:91`
- `corpus/knowledge/boot-writers-r19.json:176,203,227,256` — signature `kind: "alpm-scriptlet"` (a schema token also used for `running '<name>'` values at 204, 228, 257, i.e. for hook markers; cannot be appended in JSON — gate `tools/check-boot-writers.py:196-197` matches only the `[ALPM-SCRIPTLET]` token)
- `corpus/lessons/round-19.md:13` — "3 ALPM-SCRIPTLET events (S067); hook identity for ALPM events is [inf]"
Append-only correction sentence (one note in `boot-writers-r19.md`, referenced from the others): "Round-39 clarification (TO8, TO1): `[ALPM-SCRIPTLET]` is the log tag for every line libalpm's chroot children print — hooks, install scriptlets and `ldconfig` — not a marker of an install scriptlet; the three events (pacman.log 2021, 3015, 3047) are PostTransaction-hook output: each lies after `transaction completed` and after its transaction's `running '90-mkinitcpio-install.hook'...` line (frozen capture lines 1950/1989/2021 and 2941/2983/3015, 3047). That the hook is `90-mkinitcpio-install.hook` rests on the `running` header line preceding the output, and its Exec on the hook file; the tag itself identifies neither."
For `lessons/round-19.md:13` the "[inf]" label on hook identity stands for *which* hook; that the output is hook output (not scriptlet output) is now source-backed (TO8 + position).

## Checked, no correction needed

- `SKILL.md:3177` (HO5 row): "`pacman.log` gains `alpm_logaction` lines only" is correct in that case, because the Pre-scan error returns before any hook runs (`hook.c:629-631`), so no chroot child exists to log.
- `SKILL.md:753`, `aur-risk-plane.md:202`, `aur-risk-plane-ver-s6.md:66`: "install scriptlet" there means a package `install` file (`Install Script: No`), the right object.
- `SKILL.md:2045`/`2043-2046` and `boot-writers-r19.md:91` bracket checks (`ALPM-SCRIPTLET` line between its `running '90-…'` line and the next `[ALPM] running`): consistent with TO1/TO8.
- `pacman-hook-order-r38.md:145`, `:24-26` and S210 row: the `_alpm_trans_commit` anchor defect is already recorded and S217 supersedes; HO6's "S210 trans.c:212-240" range contains the real lines (`trans.c:212-240`), not contradicted by TO1.
- `SKILL.md:3183` "Commits are per-target (`add.c:670-687`, `sync.c:1336-1357`)" agrees with TO2/TO3 (add.c:669-688, sync.c:1336-1356).
- `tools/score-pacnew-arm-r35.py:165`, `r35b.py:306`: fixtures put pacnew text under `[ALPM-SCRIPTLET]` as decoys; the real log has `[ALPM] warning: … installed as … .pacnew` (frozen log 1427), consistent with TO8 (a scriptlet may print such text; it is not libalpm's warning). Out of the swept scope; no action.
- `PROVINCE.md`, `corpus/QUALITY.md` (apart from :70): no statement on scriptlet/hook order or the tag. `PROVINCE.md:22` "hooks" is mkinitcpio initramfs hooks.

## Incidental defects found while sweeping (not corrections to existing claims)

- `corpus/knowledge/pacman-transaction-order-r39.md:17-18` says which r25 propositions are admitted/corrected/rejected "is recorded in `corpus/lessons/round-39.md` Gate"; `corpus/lessons/round-39.md` does not exist at HEAD 394e1ba (`ls corpus/lessons` ends at `round-38.md`; read of the path errors). Either the file is still to land or the pointer dangles.
- `corpus/lessons/round-38.md:48` (outside the swept scope) names the proposition "upgrade order old-Pre → scriptlets → new-Post". TO3/TO5 split the scriptlets around the file writes (pre-scriptlet → files → post-scriptlet), so "→ scriptlets →" is loose for the commit step; the old-Pre/new-Post halves agree with TO5. Append: "Round-39 (TO3, TO5): per package pre-scriptlet → files → post-scriptlet; old hook files run in Pre, upgraded hook files in Post."
- Optional addition to TO8 itself: the row says the tag marks "every output line"; it could add that child-side failure text (`util.c:680,684,700`) is logged under the tag too, which is what makes finding 1 a TO8 consequence.

## Rows judged (against `.ufo/waves/round-39/frozen/src/`)

TO1: holds — trans.c:201-208, 232-239
TO8: holds — util.c:521-528, hook.c:525-528 (ldconfig: util.c:833)

TO2–TO7 were not judged by this seat.

## Not done

- No live `pacman.log` read (only the frozen copy); host line numbers are the frozen capture's.
- Did not search `.ufo/` historical wave artifacts for the loose wording (they are frozen round reports; round-19 files such as `ScoutEntryToolDoc.md:21`, "That scriptlet line is emitted by `limine-entry-tool`", carry the same wording and are not correctable in place).
- No tools installed; no checks other than file reads, a python count of the frozen log, and `ls`.

Receipts: `.ufo/waves/round-39/w1/C2ScoutCorrections/receipts.txt`
