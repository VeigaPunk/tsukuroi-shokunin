VERDICT: draft

# P-4 — `## Hook order — round 38` for `SKILL.md`, with its gate-registry row

Seat DraftSkillHooks, round 38 (hyaku run 8), leaf. Read-only on lane and host; the only files I
created are this report and `.ufo/waves/round-38/w1/DraftSkillHooks/` (receipts). Scratch
`/fast/scratch/hyaku/tsukuroi-r38/DraftSkillHooks/` removed at the end.

## 0. Status correction, before the draft

Two facts change what this item can deliver:

1. **The gate-registry row already exists and is committed.** `SKILL.md:3115` carries
   `| hook-order-r38 | gate | …`, added by commit `5edb6c2` ("round-38: registry rows for
   storage-arm-r38, storage-arm-r38-q82, hook-order-r38 (QUALITY 70)") — `git blame -L
   3100,3115 --porcelain SKILL.md` in a shared scratch clone attributes lines 3113–3115 to
   `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf`. So the deliverable for the row is **not a new row**
   but a verification of the committed one plus one naming amendment (§4). A second row would be a
   duplicate-row defect under `check-registry-coverage.py` (`REGISTRY-ROW-DUPLICATE`).
2. **No `## Hook order — round 38` section exists anywhere in the lane** —
   `grep -rn '## Hook order' SKILL.md` returns nothing; the only round-38 prose gap is this section.
   That is the real work of the item.

The entry the section distils, `corpus/knowledge/pacman-hook-order-r38.md`, is a 109-line addition
at `1fe28e7` with **no later edit** (`git diff --stat 7cbaeb6..HEAD -- corpus/knowledge/pacman-hook-order-r38.md`
→ `109 ++++…`). So the HO5/HO6 wordings attacked by wave-1 seats (§2) are still the live text; the
section below states the corrected readings rather than copying the entry's consequence cells.

## 1. What I ran, and what it says

All read-only; runs from a `--shared` scratch clone, never in the lane work tree except reads.

- **Counter at the C2 implementation commit.** `python3 tools/check-hook-order-r38.py --revision
  1fe28e725be47364fc6033bf81ecabc66ee5fe62` → `rows_expected 69, rows_matched 69, mismatches 0,
  extra_rows 0, source_ok 1, result PASS, exit 0`, source ids S208–S212, `source_problems []`
  (`DraftSkillHooks/receipts.txt` §4). The declared predicate and the registry row's `0` cell are
  therefore satisfied at the implementation revision, not merely asserted.
- **Counter bytes are frozen.** `git show 7cbaeb63:tools/check-hook-order-r38.py | sha256sum` and
  `git show HEAD:…` both `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`
  (matches the declaration and the registry pinned-values cell); `git diff --stat 7cbaeb6..HEAD --
  tools/check-hook-order-r38.py` is empty.
- **Capture digest.** `sha256sum .ufo/waves/round-38/frozen/hooks-capture/MANIFEST.sha256` →
  `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd` (matches entry, row, declaration).
- **CLI shape (registry-row check).** `tools/check-hook-order-r38.py:186-188` accepts `--repo`,
  required `--revision`, and `--branch` (default `master`); there is no `--selftest`, so the row's
  self-test cell ("none: the frozen capture is the measurement") is correct.
- **Controls, read not rerun** (`controls/controls.jsonl`): base `0/69` FAIL; plain-sort `63/69,
  mismatches 6, extra 6` FAIL; no-override `66/69, mismatches 3, extra 3` FAIL; no-source `69/69,
  source_ok 0` FAIL; correct `69/69, source_ok 1` PASS. The row's control cell lists exactly these
  five.
- **Live re-derivation of the header counts** (host reads): 67 `/usr` + 3 `/etc` = 70 files;
  entry rows 17 Pre / 52 Post = 69 effective; `grep -l '^AbortOnFail'` over both dirs → 0 files;
  triggerless files → 0. **`grep -l '^NeedsTargets'` → 15 files, not 14** — resolved, not a defect:
  the 15th is `/usr/share/libalpm/hooks/90-mkinitcpio-install.hook`, which the `/etc` copy overrides
  (HO2), so 14 is the *effective* count; `diff live-needs.txt entry-needs.txt` →
  `10d9 < 90-mkinitcpio-install.hook`. The override is thus independently visible in the counts.
- **HO1 on live files.** `LC_ALL=C ls -1 … | LC_ALL=C sort` orders
  `fontconfig-32.hook fontconfig.hook gio-querymodules-32.hook gio-querymodules.hook
  gio-remove-module-cache-32.hook gio-remove-module-cache.hook` — every `-32` file first — while
  the table puts `fontconfig.hook` (Post 32) before `fontconfig-32.hook` (Post 33). Full-name byte
  sort is a wrong reading of the run order, demonstrably.
- **HO2 on live files.** `/etc/pacman.d/hooks/90-mkinitcpio-install.hook:30 Exec =
  /usr/share/libalpm/scripts/limine-mkinitcpio-install` versus
  `/usr/share/libalpm/hooks/90-mkinitcpio-install.hook:37 Exec = /usr/share/libalpm/scripts/mkinitcpio
  install`; `pacman-conf HookDir` → `/etc/pacman.d/hooks/`.
- **Phase evidence from the host log.** `/var/log/pacman.log:3247-3254`: `Running 'pacman -Rns …'`,
  `running '10-limine-snapper-lock.hook'...` (3248), `transaction started` (3249), removals,
  `transaction completed` (3253), `running '35-systemd-update.hook'...` (3254). One Pre hook, one
  Post hook: the triggered-subset reading (HO7) is observable, and Pre precedes `started`.
  `grep -c "running '"` → 295 lines.
- **HO5 symptom string, primary fetch.** `error.c:106: return _("failed to run transaction
  hooks");` and `sync.c:850: pm_printf(ALPM_LOG_ERROR, _("failed to commit transaction (%s)\n"),`
  at pacman `54d9411`, fetched 2026-10-26T05:07:45Z (`error.c` sha256 `03f2dd96…`, `sync.c`
  `af6f1104…`). My `src/pacman/sync.c` digest equals the `frontend-sync.c` line of seat
  C2CritHO6's `SHA256SUMS.fetched:3` — same bytes, independent fetch, so the string is
  cross-checked by two seats.
- **Per-target commit, verified rather than inherited.** Fetched `lib/libalpm/add.c`
  (sha256 `fd313629…`) and `lib/libalpm/sync.c` (`6b297364…`) at `54d9411`, fetched 2026-10-26 —
  both digests equal seat C2CritHO6's `SHA256SUMS.fetched` lines, so the bytes are the same.
  `add.c:670-687` loops one target at a time, returns early while `state == STATE_INTERRUPTED`
  (673-675, with `ret` still 0 when nothing failed yet), and sets `STATE_INTERRUPTED` on a failed
  target (679-683); `sync.c:1354-1357` returns -1 on that failure. This is what lets the HO6 row say
  "version skew, not nothing happened" and "exit 0 is possible".
- **A gate I hit myself:** `ls -l /boot` → `ls: cannot open directory '/boot': Permission denied`
  (non-root). The HO6 artifact leg is therefore `BLOCKED` read-only, exactly like checklist item 7;
  the draft says so instead of pretending the check is runnable.

## 2. Corrections the draft must carry (peer findings, verbatim paths)

- **HO5:** `C2CritHO5.md:188` — `HO5: partly — .ufo/waves/round-38/sources/hook.c:609-631 (mechanism
  holds as run; the parenthetical at hook.c:119-123 and the "one path" consequence at
  hook.c:554-562 are false as written)`. The mechanism is proved by execution, not reading:
  `C2CritHO5/matrix.txt:7-9` (T1) shows a hook declaring `When = PostTransaction` with no `Exec`
  still returns `rc=-1 errnum=32 str="failed to run transaction hooks"` plus
  `[E] Missing Exec option in hook: /etc/pacman.d/hooks/50-bad-post.hook`. Source side confirmed by
  me: `hook.c:119-123` returns 0 for a triggerless hook *before* the Exec/When checks at
  `hook.c:129-146`, and `hook.c:609-615` parses/validates every candidate regardless of `when`.
- **HO6:** `C2CritHO6.md:203` — `HO6: partly — .ufo/waves/round-38/sources/trans.c:230-241`; the
  report's finding 1 says the three rule clauses hold but "ignored" means *not propagated*, not
  *not logged*, and finding 2 shows the interrupt path returns **0** from `alpm_trans_commit`
  (`trans.c:242-244`) while commits are per-target. I re-read `trans.c:230-244`: Post runs only in
  the `else` of `state == STATE_INTERRUPTED`, after `transaction completed` (235) and guarded by
  NOHOOKS (237), return 0 at 244.

My draft therefore (a) scopes the HO5 parenthetical to files **that have a `[Trigger]` section**,
(b) names two Pre-phase blockers instead of "the one", (c) states the HO6 consequence as version
skew (new modules tree, previous UKI) and adds that a missing Post run can come with exit 0.

## 3. Proposed text A — the section

Placement: insert immediately **before** `## Gate and probe registry — round36 superseding current
rows` (`SKILL.md:3050`), i.e. after the round-36 block, whose last content line is `SKILL.md:3049`
(`for each of the four keys, rc=0).` — the file currently has no blank line between 3049 and the
heading, so the insertion should open with a blank line). That keeps the
established order "round narrative, then the operative registry table", and the heading does not
match the `## Gate and probe registry — round<N>` selector, so
`check-registry-coverage.py`'s highest-table rule is untouched. If the integrator insists on strict
append-only, appending at EOF is equivalent for every checker but reverses that order; either way
this is the only place round-38 prose is missing.

Exact markdown:

```markdown
## Hook order — round 38

Appended 2026-10-26 (round-38 C2). One new read-only surface for the update-safety plane: which ALPM
hooks exist here, in which order they would run, and which of them can stop a transaction. Every
row below is read from the hook files and from pinned pacman `54d9411` source (snapshots
`.ufo/waves/round-38/sources/`, digests in `SHA256SUMS`); no row rests on running a hook, and nothing
here authorizes a package, hook or transaction action.

Measured 2026-10-26 (`.ufo/waves/round-38/frozen/hooks-capture/`, MANIFEST sha256
`da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`): **70 hook files → 69 effective
hooks** (one same-name override), 17 `PreTransaction` + 52 `PostTransaction`, 0 triggerless masks,
0 `AbortOnFail`, 14 effective `NeedsTargets`. Re-derived live in this seat: 67 files in
`/usr/share/libalpm/hooks` + 3 in `/etc/pacman.d/hooks`; 15 files carry `NeedsTargets`, and the
fifteenth is the `/usr` copy of `90-mkinitcpio-install.hook` that the `/etc` copy overrides — 14 is
the effective count, not a miscount. Rules HO1–HO7 and the full 69-row table:
`corpus/knowledge/pacman-hook-order-r38.md`. Gate:
`python3 tools/check-hook-order-r38.py --revision <REV> [--repo <PATH>]`.

Read-only probes used below, all permitted by the boundary rule: `pacman-conf HookDir`, `pacman -Q
linux`, `grep`/`ls`/`stat` on the two hook directories, `/boot` (gated, see limits) and
`/var/log/pacman.log`.

### Symptom → rule → read-only check → operator action

| Symptom (verbatim string or observation) | Rule | Meaning | Read-only check | Suggested operator action (tsukuroi does not run it) |
|---|---|---|---|---|
| `error: failed to commit transaction (failed to run transaction hooks)`, preceded by `[E] Missing Exec option in hook: <path>`, `[E] Missing When option in hook: <path>`, `[E] hook <path> line N: invalid section\|invalid option` | HO5 | The Pre-phase pass failed while parsing or validating candidates: a `.hook` file **that has a `[Trigger]` section** is malformed (`hook.c:129-146`), or a hook directory could not be opened/read (`hook.c:547-560`). `_alpm_hook_run` returns at `hook.c:629-631` before the run loop, so **no Pre hook ran** and the transaction never started (`trans.c:201-204`; `transaction started` at `:208` is never logged) — no target was installed | The `[E]` line is `_alpm_log(ERROR)` and reaches **stderr only**; `pacman.log` gains `alpm_logaction` lines only, so look for the absent `transaction started` rather than for the error: `grep -n 'transaction \(started\|completed\)' /var/log/pacman.log \| tail -2`, `grep -c "running '" /var/log/pacman.log`, `pacman -Q <named targets>` unchanged. Re-read the named file for `[Trigger]`, `When`, `Exec` | Fix or remove the named file; to disarm a hook without deleting it, reduce it to a `[Trigger]`-less stub (that is HO3, valid). While the file stays broken every transaction fails at Pre — including one whose `When` is `PostTransaction`, since all candidates are validated |
| A hook file you added is named in an `[E]` line although it declares `When = PostTransaction` | HO5 | Same failure: `hook.c:609-615` parses and validates every candidate file in either directory with no reference to `when`; the phase gate is only consulted later (`hook.c:629`, `:638`). Executed witness: `C2CritHO5/matrix.txt:7-9` (T1, `50-bad-post.hook`) → `errnum=32` | as above; do not assume "Post hooks cannot block the transaction" | Same fix; a malformed Post hook file blocks every upgrade on this host |
| Two files share a name, or the `running '<name>'...` line shows an `Exec` you did not write | HO2 | Directories are walked **last list entry → first**, and the system directory is the list head, so `/etc/pacman.d/hooks/<name>` wins and the `/usr/share/libalpm/hooks/<name>` copy is skipped (`hook.c:540`, `:588-590`; `alpm.c:59-62`) | `pacman-conf HookDir` (prints `/etc/pacman.d/hooks/`); `ls /usr/share/libalpm/hooks/<name> /etc/pacman.d/hooks/<name>`; `grep -n '^Exec'` in both | Edit the winning file, or rename; note that deleting the `/etc` copy hands the hook back to `/usr`, so a later package update silently restores stock behaviour |
| `-32`/plain pairs (`fontconfig`, `gio-querymodules`, `gio-remove-module-cache`) run in an order that contradicts `LC_ALL=C sort` of the file names | HO1 | Order is a bytewise `strncmp` of the names **without** the `.hook` suffix over the shorter length, shorter name first on a tie (`hook.c:443-455`). `-` (0x2d) sorts before `.` (0x2e), so full-name sort reverses every such pair | Compare against the entry's `## Effective hook order` table, not `sort`: `ls /usr/share/libalpm/hooks \| LC_ALL=C sort` is a different sequence | Rename rather than renumber if a real dependency exists; report the collision — do not reorder `/usr` files |
| A hook file exists but never appears as `running '<name>'...` | HO3 | Read the mask rule first: a hook file with no `[Trigger]` section is valid and never runs (`hook.c:119-123`); 0 such files on this host. Otherwise it is the phase/trigger filter (HO7) or the phase never ran (HO6) | `grep -c '^\[Trigger\]' <file>`; `grep -n "running '<name>'" /var/log/pacman.log \| tail -3`; confirm a `transaction completed` exists for that attempt | Nothing to do if the silence is a deliberate mask; otherwise chase HO6/HO7 |
| A Pre hook exits non-zero and the upgrade continues | HO4 | A Pre hook's non-zero exit aborts only when the hook carries `AbortOnFail`; `AbortOnFail` on a Post hook is rejected with a warning at load (`hook.c:141-146`), and the run loop breaks only for Pre (`hook.c:660-669`). 0 of the 17 Pre hooks here carry it, so **no Pre hook's exit status can stop a transaction on this host**; the only other Pre blocker is HO5's scan error | `grep -l '^AbortOnFail' /usr/share/libalpm/hooks/*.hook /etc/pacman.d/hooks/*.hook` (expect nothing). Distinguish an HO5 abort from an HO4 abort: HO5 leaves a validation `[E]` line and **no** `running '…'` line for the phase; an aborting Pre run logs `running '<name>'...` first (`hook.c:653`) | Treat the failed hook as an ignored warning and check its product by hand; making it fatal needs a vendor file with `AbortOnFail` — not an `/etc` edit |
| After an upgrade the UKI/initramfs predates the installed kernel, a Post hook did not run, and the command exited 0 | HO6 | The Post phase runs only in the `else` of `state == STATE_INTERRUPTED`, after `transaction completed` (`trans.c:230-241`), so a `transaction failed` or `transaction interrupted` runs none of the 52 Post hooks. Commits are per-target (`add.c:670-687`, `sync.c:1336-1357`): a mid-transaction failure leaves already-committed targets (e.g. the new `linux` modules tree) with the **previous** UKI — version skew, not "nothing happened". An interrupt returns 0 from `alpm_trans_commit` (`trans.c:242-244` with `add.c:673-675`), so a missing Post run need not come with a non-zero exit; and a Post hook's own failure is dropped (`trans.c:238`) and reaches stderr, not `pacman.log` | Log leg: `grep -n 'transaction \(started\|completed\|failed\|interrupted\)' /var/log/pacman.log \| tail -4` and check that the Post `running '...'` lines follow the last `transaction completed`. Artifact leg: `pacman -Q linux` versus `stat -c '%y %n' /boot/…` — **BLOCKED** as a non-root user (measured 2026-10-26: `ls: cannot open directory '/boot': Permission denied`), so record `BLOCKED` and hand the probe over | Re-run the boot-artifact producers by hand (`mkinitcpio -P`, `limine-update`) and verify before reboot; the lane never runs them |
| Within one transaction the `running '...'` order disagrees with the table | HO7 | The table is the order of **candidates**; a transaction runs only the triggered subset, in that order, per phase (`hook.c:633-641`). A real sequence is therefore a subsequence of the table order for its phase, and missing hooks are normal. Witness on this host: `/var/log/pacman.log:3248-3254`, one Pre hook before `transaction started`, one Post hook after `transaction completed` | Extract the phase lines (`awk` between `transaction started` and `transaction completed`, plus the `running` lines before `started`), map each name to its `pos` in the entry table, confirm the positions increase within a phase | If positions are not increasing with an unmodified pacman, the entry or the installed pacman has moved: re-run the gate and report, never hand-edit the table |

### Limits of this table

- **No hook was executed for it.** The rows model candidates from files and pinned source; the
  order of hooks inside a real transaction is not produced here (entry `[unk]`), which is why HO7's
  check is a subsequence test on the log rather than a prediction.
- **NOHOOKS is a separate explanation.** A transaction flagged `ALPM_TRANS_FLAG_NOHOOKS` skips both
  phases (`trans.c:201`, `:237`); which pacman option sets that flag is not read here `[unk]`, so "no
  hook ran at all" is not automatically HO6.
- **Permission can mimic HO5.** A root-owned hook directory that the current user cannot open sets
  the same scan error (`hook.c:547-560`); the tell is `[E] error while reading hook …: Permission
  denied` (`C2CritHO5/matrix.txt`, T11). Hand it to the operator; never escalate.
- **Silence in `pacman.log` is weak evidence.** Only `alpm_logaction` lines reach it
  (`hook.c:653`; `trans.c:208`, `:231`, `:235`); validation and exec failures are stderr-only, so a
  missing log line never proves a hook succeeded.
- **`/boot` is unreadable non-root** (checklist item 7): HO6's artifact leg is `BLOCKED` for an
  agent and stays an operator probe.
```

## 4. Proposed text B — the gate-registry row

The committed row, `SKILL.md:3115`, verbatim (8-cell table under `## Gate and probe registry —
round36 superseding current rows`, the operative highest table):

```markdown
| hook-order-r38 | gate | `python3 tools/check-hook-order-r38.py --revision <REV> [--repo <PATH>]` | 0 all 69 rows match the frozen capture and the cited rows are mined, used-by the entry and opened 2026-10-26;1 a missing, wrong, extra or duplicate row or a source problem;2 revision, git or capture_tampered could-not-evaluate | none: the frozen capture is the measurement; controls `.ufo/waves/round-38/controls/controls.jsonl` (base, full-name sort, no override, no source FAIL; correct PASS) | R38 C2 frozen at `7cbaeb63`, sha256 `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`; capture MANIFEST sha256 `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`; libalpm order model of pacman 54d9411 | reads the entry and SOURCES at REV through git and the digest-verified capture from the work tree; no write | tsukuroi |
```

Every cell checks out against the tool and the ledger: entry command matches `:186-188`; the `0`
cell is the `PASS` run in §1 (69/69, `source_ok 1`) and the declared predicate; the `1`/`2` cells
match `controls.jsonl` (FAIL at exit 1) and the docstring's `capture_tampered`/binding/git refusals
(exit 2); self-test is `none` (no `--selftest` in `argparse`); pinned digests re-derived in §1.

One amendment, tightening only — the tool accepts `--branch` and the neighbouring rows name it
(`knowledge-header` row has `[--branch <BRANCH>]`, `kernel-taint` row `[--branch <NAME>]`), so the
Entry cell should read:

```markdown
| hook-order-r38 | gate | `python3 tools/check-hook-order-r38.py --revision <REV> [--repo <PATH>] [--branch <BRANCH>]` | … (rest of the row unchanged) |
```

If the integrator prefers the row byte-identical, that is acceptable — the omission is an
incomplete option list, not a false verdict map — but it should then be recorded as a known gap
rather than silently kept.

## 5. Findings that falsify nothing but must travel

- **`NeedsTargets` 15 files / 14 effective** (§1). I checked this because 15 ≠ the entry's 14; it is
  the HO2 override, so the entry is right and the naive recount is wrong. Worth one clause in the
  entry's header if that file is ever amended; the draft section already states it.
- **The registry row was already committed before this seat** (§0) — the item's premise ("plus a
  gate-registry row") is already satisfied at `5edb6c2`; a new row would have been a duplicate.
- **The HO5/HO6 entry cells are still the attacked wording** (§2); the section deliberately states
  the corrected readings. Repairing the entry itself (rewriting the HO5 parenthetical, the "one
  path" consequence and the HO6 consequence cell) is other seats' work and I did not touch it.

## 6. Not done / limits of this seat

- I judged **no** HO1–HO7 row (other seats own the per-row verdicts). What I did is narrower: I
  re-read the source lines each drafted table row cites, at the frozen snapshots, and confirmed the
  string/line claims (`hook.c:119-123,129-146,443-455,540,547-560,588-590,609-615,629-631,633-641,
  653,660-669`; `trans.c:201-208,230-244`; `alpm.c:59-62`; fetched `error.c:106`, `sync.c:850`).
- I did not run the counter's FAIL direction myself (the five controls are already scored in
  `controls.jsonl`; I read them and did not re-derive them).
- I did not run any hook, transaction, `pacman` install/upgrade, service action or `sudo`; no
  package, hook, sysfs, service, boot or `/etc` change. No tool was installed, so there is no
  tooling record beyond the preinstalled `python3`, `curl`, `git`, `pacman-conf`, `grep`, `ls`.
- I did not edit `SKILL.md` or any other lane file; the section and row exist only as text above.
- Scratch `/fast/scratch/hyaku/tsukuroi-r38/DraftSkillHooks/` (clone, needs diff, live probes) was
  removed after the receipts were copied to
  `.ufo/waves/round-38/w1/DraftSkillHooks/` (`receipts.txt`, `error.c`, `sync.c`).

Receipts: `.ufo/waves/round-38/w1/DraftSkillHooks/receipts.txt` (commands and observed output, 13
sections), `DraftSkillHooks/error.c`, `DraftSkillHooks/sync.c` (fetched 2026-10-26T05:07:45Z with
digests; `add.c`/`lib/libalpm/sync.c` were fetched to scratch only, digests recorded in §12).
