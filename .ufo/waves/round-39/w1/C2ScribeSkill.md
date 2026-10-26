VERDICT: draft

Item C2-21 — a `SKILL.md` section `## Transaction order — round 39`: one decision table for the update-safety
plane built from TO1–TO8 of `corpus/knowledge/pacman-transaction-order-r39.md`. The draft below is written to be
appended at the end of `SKILL.md` (after the round-39 storage section, which begins at `SKILL.md:3205`; file is
3224 lines and ends with a newline). Nothing in the lane was modified: all reads, one read-only awk
re-derivation and four `stat`/`ls` host probes; no clone, no mutator, no install.

## What I did

1. Read the C2 entry whole (`corpus/knowledge/pacman-transaction-order-r39.md:1-58`), the source rows
   (`corpus/SOURCES.md:217-227`), the round-38 hook section this one must sit beside (`SKILL.md:3151-3203`)
   and the round-39 storage section that already ends the file (`SKILL.md:3205-3224`).
2. Re-read every TO row's cited lines in the pinned snapshots (`.ufo/waves/round-39/frozen/src/`) and confirmed
   each quoted string is at the cited line; receipt `.ufo/waves/round-39/w1/C2ScribeSkill/anchors.txt`.
3. Re-derived the two host counts the table leans on from the frozen capture, plus one the entry states
   (“no transaction both removes and adds”) that I wanted independent of the prose;
   receipt `.ufo/waves/round-39/w1/C2ScribeSkill/phase-placement.txt`.
4. Re-hashed the snapshots, the counter and the capture manifest against the declared pins;
   receipt `.ufo/waves/round-39/w1/C2ScribeSkill/pins.txt`.
5. Took four read-only host probes the table's “check” cells prescribe, to avoid recommending a check that is
   `BLOCKED` for a non-root seat; receipt `.ufo/waves/round-39/w1/C2ScribeSkill/host-probes.txt`.

## Evidence

Digests re-read 2026-10-26 (`.ufo/waves/round-39/w1/C2ScribeSkill/pins.txt:2-9`) — all match the declaration:
`add.c fd3136…`, `hook.c 99f104…`, `remove.c a052d4…`, `sync.c 6b2973…`, `trans.c 637c11…`, `util.c 381618…`,
`tools/check-transaction-order-r39.py f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`,
`txcapture/MANIFEST.sha256 cb5cb4f4…` (manifest also lists `pacman.log 0845c1df…`).

Host counts, re-derived in this seat from `.ufo/waves/round-39/frozen/txcapture/pacman.log`
(`.ufo/waves/round-39/w1/C2ScribeSkill/phase-placement.txt:2-4,7`):

```
windows=86 started=60 completed=60 other_end=0
running_pre=59 running_in_commit=0 running_post=236
scriptlet_in_commit=189 scriptlet_outside=252 total_scriptlet=441
windows=86 both_remove_and_add=0
```

This agrees with the entry's TO1 (0 `running` lines inside a commit), TO2 (0 of 60 both removes and adds) and
TO8 (252 of 441 outside every commit phase) host columns, and adds the 189-inside split the draft quotes.

Source anchors re-read at 54d9411 (`anchors.txt`): `trans.c:202` Pre call, `:208` `transaction started`,
`:216`/`:224` `transaction failed`, `:231` `transaction interrupted`, `:235` `transaction completed`, `:238`
Post call; `add.c:472-473` `_alpm_runscriptlet(… newpkg->version, oldpkg ? oldpkg->version : NULL, 1)`,
`:618`/`:626`/`:630` log lines, `:641` local-db `install` path, `:658` `skip_ldconfig`, `:673` interrupted
return, `:679-682` set interrupted + skip, `:689-691` `_alpm_ldconfig`; `remove.c:711` `pre_remove`, `:722`
`removed %s (%s)`, `:731` `post_remove`; `util.c:527` `alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line)`;
`sync.c:1340` comment, `:1345` remove, `:1354` upgrade; `hook.c:540` `alpm_list_last(handle->hookdirs)`, `:554`
`opendir` inside the loop, `:525`/`:528` `_alpm_run_chroot`. Log exemplar at
`.ufo/waves/round-39/frozen/txcapture/pacman.log:123-124` is `installed systemd (261.1-1)` then
`[ALPM-SCRIPTLET] Initializing machine ID from random generator.`

Host probes (`host-probes.txt`), read-only, non-root: `/var/lib/pacman/local/systemd-262-1/install` is
`-rw-r--r-- root root` (the TO4 `$1`/`$2` check is readable without privilege); `/etc/ld.so.cache` is
`2026-10-25 13:36:22.090610104 -0300`; `/var/lib/pacman/db.lck` absent (rc=2 from `ls`). The cache mtime is 24
minutes *after* the frozen log's last write (`capture-meta.txt:2`, mtime `2026-10-25 13:12:06.981386572 -0300`),
so the draft states the cache mtime as a witness, not as proof — and the log's `+0000` against `stat`'s local
zone as a conversion trap.

## Proposed text — exact markdown

Append at end of file (currently line 3224, after the round-39 storage section). Verbatim:

````markdown
## Transaction order — round 39

Appended 2026-10-26 (round-39 C2). The round-38 table above orders the hooks **inside** one phase (HO1–HO7);
this one fixes, for the update-safety plane, what happens **between** the phases and what each line of a
commit proves. Rules TO1–TO8, their quotes, the host derivation and the boundaries:
`corpus/knowledge/pacman-transaction-order-r39.md`
(sources S208 `hook.c`, S213 `add.c`, S214 `sync.c`, S215 `remove.c`, S216 `util.c`, S217 `trans.c` — S217
supersedes S210's anchor — plus S218, the frozen capture `.ufo/waves/round-39/frozen/txcapture/`, MANIFEST
sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4`; libalpm snapshots
`.ufo/waves/round-39/frozen/src/`, digests in `SHA256SUMS`; pacman 54d9411). Detection and report only:
nothing here authorizes a package, hook or transaction action.

Where the lines sit in one transaction (TO1, TO2, TO3, TO6, TO7; S217, S214, S213, S215):

```
[PACMAN] Running '<command>'                 the frontend opens the window
[ALPM] running '<pre-hook>'...               PreTransaction: before the commit exists
[ALPM] transaction started
[ALPM] removed <pkg> (<ver>)                 sync commits only: conflicts/replacements go first
[ALPM] upgraded <pkg> (<old> -> <new>)       one target at a time, in transaction order
[ALPM] transaction completed                 or interrupted / failed: no Post hook then
[ALPM] running '<post-hook>'...              PostTransaction: hook files re-read from disk
```

Measured from the frozen copy (S218, captured 2026-10-26T05:42:12Z; `pacman.log` mtime 2026-10-25
13:12:06): 86 `Running` windows, 60 `transaction started`, 60 `transaction completed`, 0
`interrupted`/`failed`; 59 `running` lines before a `started` line, **0** between `started` and
`completed`, 236 after a `completed`; 441 `[ALPM-SCRIPTLET]` lines, 189 inside a commit and **252**
outside; 28 `removed` lines and 0 windows that both remove and add. That is a snapshot, not current state.

### Symptom → rule → read-only check → operator action

| Symptom (verbatim string or log shape) | Rule | Meaning | Read-only check | Suggested operator action (tsukuroi does not run it) |
|---|---|---|---|---|
| `[ALPM] running '<hook>'...` lines appear before the same window's `transaction started`, and none between `started` and `completed` | TO1 (S217 `trans.c:201-208`) | Both phases are separate calls outside the commit: Pre at `:202` with `RET_ERR(… ALPM_ERR_TRANS_HOOK_FAILED …)`, `transaction started` at `:208`, Post at `:238` after `transaction completed` at `:235`. A Pre `running` line is never part of the commit | `awk` the window between two `Running` lines and count `running` lines on each side of `started` | None — expected shape |
| A `running '<hook>'...` line falls **inside** a commit (between `started` and `completed`/`interrupted`/`failed`) | TO1 (S217 `trans.c:230-241`) | No single pacman process writes one there at 54d9411: it is a Post hook of an earlier window, a second concurrent pacman writing the same log, or a spliced log | Compare its timestamp with the window's `completed` line; `pgrep -a pacman`; baseline: 0 in 60 (S218) | None for the system; record the window as a log-anomaly finding, never as a third hook phase |
| `error: failed to commit transaction (failed to run transaction hooks)` and **no** `transaction started` for that attempt | TO1 (S217 `trans.c:201-204`) with HO5 above | The Pre pass returned at `RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1)` before `STATE_COMMITTING`, so no target was committed and the Post phase does not exist. The validating `[E] …hook…` line is stderr-only | Read forward from the last `Running '<cmd>'`; `ls /var/lib/pacman/db.lck` (absent = no frontend left holding the lock) | Fix or remove the named hook file; the operator re-runs the transaction |
| One sync window holds both `removed` and `installed`/`upgraded` lines | TO2 (S214 `sync.c:1340-1354`) | `_alpm_remove_packages(handle, 0)` at `:1345` runs before `_alpm_upgrade_packages` at `:1354`, so every `removed` line precedes the first add | Per-window `awk`; baseline: 0 of 60 windows has both, and all 28 `removed` lines sit in removal-only windows (S218) | None. An add line before a removal line inside one window is a log anomaly, not a pacman ordering |
| `[ALPM-SCRIPTLET]` lines sit between a package's own `installed`/`upgraded` line and the next package's line | TO3 (S213 `add.c:616-648`, `:669-688`) | Per target: `pre_install`/`pre_upgrade` from the package file (`:466-474`), files and db entry, the `installed`/`upgraded` line (`:618`, `:630`), then `post_install`/`post_upgrade` from the local db's `install` file (`:641`, `:644-645`). Output before the line is the pre half, after it the post half | Adjacency in the window — exemplar `.ufo/waves/round-39/frozen/txcapture/pacman.log:123-124`: `installed systemd (261.1-1)` then `Initializing machine ID from random generator.` — and `stat` the local `install` file | Name the half before proposing a fix: a post-scriptlet failure comes **after** the files and the db entry were written |
| An upgrade scriptlet takes the wrong branch on a version comparison | TO4 (S213 `add.c:470-474`) | Upgrade scriptlets get `newpkg->version` first and `oldpkg ? oldpkg->version : NULL` second (`:472-473`); install scriptlets get the new version only. `$1` is new, `$2` is old | Read `/var/lib/pacman/local/<pkg>-<ver>/install` (read-only; observed `-rw-r--r-- root root` on `/var/lib/pacman/local/systemd-262-1/install`) and how it uses `$1`/`$2`; libalpm supplies the arguments, so the log never shows them | Fix the scriptlet (package update or local rebuild); never infer the arguments from log order |
| A hook shipped by a package installed **in the same transaction** never shows `running '<name>'...` in that transaction's Pre phase | TO5 (S208 `hook.c:540,554`) | `_alpm_hook_run` re-opens each directory on every call (`opendir` at `:554` inside the `alpm_list_last` loop at `:540`), so the Pre scan ran before the package wrote the file. It can still run in the **Post** phase of the same transaction, which re-reads the directories. Host: 17 Pre hooks are owned by a package the capture shows first installed in some transaction, and none ran in that transaction's Pre — consistent, not proof | `pacman -Qo /usr/share/libalpm/hooks/<name>`; grep the window for `installed <owner>`; `grep -n "running '<name>'"` around the window; `hook-owners.tsv` and `hook-when.tsv` in the capture dir | None if its triggers did not match either; a hook that must act before install has to be installed earlier |
| `[ALPM] transaction interrupted` closes a window (no `transaction completed`) | TO6 (S213 `add.c:676-692`) with HO6 above | A target failed to commit: `trans->state = STATE_INTERRUPTED` and `skip_ldconfig = 1` (`:679-682`), so `ldconfig` is skipped (`:689-691`), later targets are not attempted (`:673-675`), `transaction interrupted` is logged (`trans.c:231`) and the Post phase is skipped (`trans.c:238` sits in the `else`). Targets committed before the failure stay installed | The window's last lines; `stat -c '%y' /etc/ld.so.cache` against the window timestamp; `pacman -Q <targets>` for what landed; Post `running` lines absent | The operator re-runs the transaction; after a kernel update, treat the boot artefacts as skewed until a Post hook really runs |
| `[ALPM] transaction failed` closes a window | TO1 (S217 `trans.c:211-228`) | The commit call itself failed (`_alpm_remove_packages` or `_alpm_sync_commit` returned -1), `transaction failed` is logged at `:216`/`:224` and the function returns before the Post phase, so Post hooks do not run. Whether `ldconfig` ran depends on how far the commit got | The line before the failure; the stderr `error: failed to commit transaction (…)`; `pacman -Q <targets>` | Read the stderr class; partial commits are possible because targets commit one at a time |
| A `removed <pkg> (<ver>)` line for the **old half of an upgrade**, or a removal with no `pre_remove`/`post_remove` output | TO7 (S215 `remove.c:699-733`) | `removed %s (%s)` is logged only in `_alpm_remove_single_package` (`:722`); the old version of an upgrade is replaced inside `commit_single_pkg` with neither scriptlet nor log line. A removal that prints nothing simply has a silent or absent scriptlet | `pacman -Q <pkg>`; if it is still installed, the line belongs to another window or another run | Count removals by `removed` lines only; never read an `upgraded` line as a removal |
| `[ALPM-SCRIPTLET]` text appears after `transaction completed`, or outside every commit window | TO8 (S216 `util.c:521-528`; hook path S208 `hook.c:525-528`) | `_alpm_chroot_process_output` logs **every** line a chroot child prints under that tag — Post hooks, Pre hooks, install scriptlets and `ldconfig` alike (`:527`); the tag does not mean "install scriptlet". Host: 252 of 441 tag lines lie outside a commit phase, so they are hook or `ldconfig` output | The nearest preceding `running '<name>'...` names the printing hook; inside a commit, tag lines after the last package's own post-scriptlet output occupy the `ldconfig` slot (`:689-691`) — content decides, the tag does not | Attribute the text to the hook above it; never quote it as the last package's install scriptlet |

### Limits of this table

- **No transaction was run or read live.** Every count above is the frozen copy S218 (captured
  2026-10-26T05:42:12Z; `pacman.log` mtime 2026-10-25 13:12:06), so no row reports current host state.
- **TO2 has no host instance** (0 of 60 windows removes and adds): its row is a shape test that may never
  fire here.
- **TO5's host column is consistency, not proof** — the capture cannot separate "the hook file was absent"
  from "its triggers did not match" (`pacman-transaction-order-r39.md`, Boundaries).
- **`[ALPM-SCRIPTLET]` proves one thing only**: a chroot child printed that line — not which child, not
  success, not that anything was installed.
- **Time zones differ.** `pacman.log` stamps `+0000`; `stat` prints local time (`-0300` here). Convert
  before comparing an `/etc/ld.so.cache` mtime with a window — and note the cache mtime is no proof that a
  transaction's `ldconfig` ran: observed 2026-10-26, the cache is `2026-10-25 13:36:22 -0300`, 24 minutes
  after the frozen log's last write (`13:12:06`), because any tool may run `ldconfig`.
- **A missing log line is weak evidence** — validation and exec failures are stderr-only (round-38 limits).
- **The counter checks citation, not truth**: `check-transaction-order-r39.py` verifies that each TO quote
  sits at its cited lines on a mined upstream row. A review seat that judges a TO row FALSE against the
  pinned source kills the entry (round-39 declaration, QUALITY 81).

Counting: `python3 tools/check-transaction-order-r39.py --revision <REV> [--repo <PATH>]` — 0 when every
TO1–TO8 quote is at its cited lines on a mined upstream row named on `source:`, no duplicate row or
heading, both host counts reproduce and 0 `running` lines fall inside a commit phase; 1 when any of those
fails; 2 on revision, git or tampered-input failure. Round 38's `tools/check-hook-order-r38.py` scores the
hook entry, not this section, and is not re-run here.
````

## Design notes for the L1

- Every row carries **one TO id and one S id** in the Rule cell; the three example shapes the item named are
  rows 7 (TO5), 8 (TO6) and 11 (TO8). Rows 2, 3 and 9 are extra decision shapes the TO table implies but
  does not spell out as a symptom (`running` inside a commit; Pre-phase abort with no `started`;
  `transaction failed`). Row 9's Post-skip is read at `trans.c:211-228`, not
  from a TO row's host column — stated in the cell as source lines, so it cannot be mistaken for a measured
  host instance.
- The table keeps the round-38 section's column order and its “operator action is a suggestion” phrasing, so
  the two sections read as one surface.
- I did **not** add a round-39 registry row: `GateAllRegistry`/`GateRegistrySelf` own that table and
  `SKILL.md:3117` already carries `transaction-order-r39`. No other round-39 SKILL text is touched.

## TO rows I quoted — judgement basis

I judged each row only for **quote-at-cited-lines** against `.ufo/waves/round-39/frozen/src/` (the counter's
own check, QUALITY 81), not for whether the rule's host consequence is measured. All eight held; the derived
sentence in row 9 is from S217 directly, not from a TO row.

TO1: holds — `.ufo/waves/round-39/frozen/src/trans.c:201-208`
TO2: holds — `.ufo/waves/round-39/frozen/src/sync.c:1340-1354`
TO3: holds — `.ufo/waves/round-39/frozen/src/add.c:616-648`
TO4: holds — `.ufo/waves/round-39/frozen/src/add.c:470-474`
TO5: holds — `.ufo/waves/round-39/frozen/src/hook.c:532-560`
TO6: holds — `.ufo/waves/round-39/frozen/src/add.c:676-692`
TO7: holds — `.ufo/waves/round-39/frozen/src/remove.c:699-733`
TO8: holds — `.ufo/waves/round-39/frozen/src/util.c:521-528`

## Artifact paths

- Report: `.ufo/waves/round-39/w1/C2ScribeSkill.md`
- Receipts: `.ufo/waves/round-39/w1/C2ScribeSkill/{phase-placement.txt,anchors.txt,pins.txt,host-probes.txt}`
- Scratch: `/fast/scratch/hyaku/tsukuroi-r39/C2ScribeSkill` was created for `TMPDIR` and left empty; removed at
  exit. No scratch receipt lives on a `/tmp` path.

## Tools

None installed or upgraded (no channel used). Commands: `read`, `grep`, `awk`, `sha256sum`, `sed -n`, `ls`,
`stat`, `wc`; all on lane files or read-only host paths.
