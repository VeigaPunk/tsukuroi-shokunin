# W2RevC2 — review of the C2 knowledge note (round 36, wave 2)

Target bytes: `c052bb7d41ced49aa888817069afd804eccfecf1:corpus/knowledge/journalctl-v262-field-filter-r36.md`
sha256 `0077b6cf7e81ef243997fe5bd8559f5e21569290f271b2f60cb0cd1b57a8a8bf` (blob hash equals the working-tree hash).
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Evidence captured up to 04:41:08Z
(pasted from `date -u +%H:%M:%SZ`).

The note does not exist at the declaration base `6d76fb20f6ecbc940e5cfff36c74060c885e161` or at the
freeze commit `1e926801195e304950e3eb9d2525ef8bbc245089` (`git cat-file -e` → rc 128 for both); it is new
in the change commit. Reviewed against the two receipt sources the claim names:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json`
(54 cells) and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ExecC2Live/matrix.json`
(10 cells), plus the wave-1 review at
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ReviewC2Draft/ReviewC2Draft.md`.

Provenance: this seat's brief explicitly requires the decision table to cover `-n` (allowed-silent third
state) and the scope selectors `-D/--file/--root/--system/--user`. The wave-1 review
(`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ReviewC2Draft/ReviewC2Draft.md`)
is evidence for the checks it ran — notably its live `--file` table row at
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ReviewC2Draft/ReviewC2Draft.md:61`
— not a canonical acceptance list. B2's blocking rank therefore rests on the brief's explicit requirement plus the landed row's
incompleteness; B1, B3, B4 and B5 rest on cells and greps I inspected myself. Where a finding relies on a
wave-1 run rather than my own, it says so.

## Verdict

**Not admissible as-is.** Five blocking findings, all receipt/coverage defects that a reader can confirm
without new measurement. Everything the note does assert with a cell pointer holds: 40 distinct cell
pointers in the decision table all resolve, all 10 peer-matrix runs map to a note cell and agree on exit
code and stderr bytes, the rejection line and guard are exact, and the header trio passes the lane gate.

## BLOCKING

### B1 — the `-n` "allowed, output silently altered" third state is still missing (wave-1 B1, unclosed)

The table has only `REJECT` / `WORK` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/journalctl-v262-field-filter-r36.md:19`),
and line 41 files `-n`/`--lines` as plain `WORK`. The caption at `:48` says only that `--lines` "limits
*how much* is printed", never that it truncates the **field list**; the table verdict therefore hides the
exact hazard wave 1 blocked on.

Receipts in `matrix-mini.json`:

| cell | argv | exit | stdout_bytes |
|---|---|---|---|
| `core_plain` | `journalctl --no-pager -F PRIORITY` | 0 | 12 (six values) |
| `ext_lines1_F` | `journalctl --no-pager -n 1 -F PRIORITY` | 0 | **2 (one value, `stdout_head` `["5"]`, sha `f0b5c2c2…`) ** |
| `ext_plain_N` | `journalctl --no-pager -N` | 0 | 2882 |
| `ext_lines1_N` | `journalctl --no-pager -n 1 -N` | 0 | 2882 (identical) |

So `-n` silently shrinks the `-F` value list from six values to one (and does nothing to `-N`). The note's
own registry row already advertises the missing state:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/README.md:269` — "the `-n` allowed-silent third
state". The note does not deliver it, so the README row is false as landed.

This is truncation, not action replacement: `-F` stays the active action (`arg_action =
ACTION_LIST_FIELDS`, `journalctl.c:806`) and `-n` sets `arg_lines` (`journalctl.c:221`); the value list is
shortened. Action-replacing options are a different mechanism and are filed as M8.

Fix: add a third verdict, e.g. `WORK-ALTERED`, with the two `-n` cells, and state: `-F -n 1` prints 1 of
6 values (`ext_lines1_F` 2 bytes vs `core_plain` 12), while `-N -n 1` is unchanged (2882 =
`ext_plain_N`). The registry row `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/README.md:269`
then stops overclaiming.

### B2 — `--file` (valid path) is absent from the table and from both matrices (wave-1 B2, unclosed)

Wave-1 B2 required `-D`, **`--file`**, `--root`, `--system`, `--user` (and `--namespace`) shown as
allowed. `-D`, `--root`, `--system`, `--user`, `--namespace` are covered at note `:43` with cells
`ext_dir_F`, `ext_root_F`, `live_system_scope`, `live_user_scope`, `live_namespace`. `--file` is not
covered anywhere:

- `grep -c -- "--file"` → **0** in
  `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json`
  and **0** in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ExecC2Live/matrix.json`;
- the note text contains no `--file` occurrence.

The predicate itself has no file term (`src/journal/journalctl-filter.c:27-41`), so `--file` belongs in the
"not a limiter" row; the note's row `:43` lists every other scope selector and omits exactly this one.
Provenance: the exit-0 / not-rejected fact for `--file` is the wave-1 review's own live table
(`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ReviewC2Draft/ReviewC2Draft.md:61`,
`-F _TRANSPORT --file …/system.journal`, rc 0), **not** its `matrix.out` — that file records only
`--file /nonexistent` rc 1 "Failed to open files" (`ReviewC2Draft/matrix.out:19`, `matrix.sh:21`), which
exercises the open path, not the guard. What I measured myself is the absence of any `--file` cell in
both matrices and of any `--file` occurrence in the note. My seat brief names `--file` explicitly;
independently, the row is incomplete without it, and the fix needs a real journal path (a `/nonexistent`
cell proves nothing about the guard).
Fix: add a cell `ext_file_F` (`journalctl --no-pager --file /var/log/journal/<machine-id>/system.journal
-F PRIORITY`, expect exit 0) and add `--file=` to the `:43` row.

### B3 — the safe-substitution section's "Verified live here" has no receipt

Note `:58`: "Verified live here: exit 0, output `2 3 4 5 6 7` … the same pipeline with `-b -1` also exited
0 with the same six values." The prescribed pipeline is `journalctl --no-pager -b 0 -o json
--output-fields=PRIORITY | jq -r '.PRIORITY' | sort -u` (`:55`).

No receipt exists: the string `jq` and the string `sort -u` do not occur in `matrix-mini.json`
(`grep`/python containment: both False), and `ExecC2Live/matrix.json` has no such cell either (its 10
runs are listed in the table below). This is the note's own admission rule (QUALITY 2, measured anchor)
and the wave brief's rule ("every mechanism claim must cite a receipt … in `ExecC2Live/` or
`ScribeC2Draft/matrix-mini.json`"). Fix: add two cells (e.g. `subst_boot0`, `subst_boot_neg1`) recording
argv, exit, stderr bytes and stdout sha256 — or mark the claim `[inf]` and drop "Verified live here".

### B4 — the `cap()` hazard's "Measured here … Replicated" has no receipt

Note `:84` claims a measurement: a `--grep` arm carrying `-F` "returns rc 1 **and** the rejection line",
`cap()` folds stderr into stdout, "the plain `--grep` no-match case yields the sentinel `-- No entries --`
(1 line); the `--grep` + `-F` case yields the rejection sentence (1 line) — the same count from a
completely different cause."

No receipt: `No entries` and `CAP_OUT` do not occur in `matrix-mini.json`; no cell encodes the counting
expression; `ExecC2Live` has no grep/no-match cell. `ext_grep_F`
(`journalctl --no-pager --grep foo -F PRIORITY`, exit 1, 84 stderr bytes) does exist and is the natural
receipt for the `-F` half, but the paragraph does not name it, and the comparison run (plain `--grep`
no-match, 1 line) is nowhere recorded. This is a prescriptive hazard future arms are asked to trust, so
it cannot stay unreceipted. Fix: record both runs as cells and name them here, or demote the measured
half to `[inf]` while keeping the source-backed part (cap() lines
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:541-546` and `:1246-1251` are
correctly cited).

### B5 — prior-state claim is broader than its sweep and is contradicted by `corpus/lessons/round-1.md`

Note `:88`: "Before this note, no lane entry documented this rejection." The counting command that
follows sweeps only the exact runtime string
(`cannot be combined with options that limit the journal`), and for that exact string the sweep is sound:
at `6d76fb2`, `git grep` returns exactly one hit, `SCORECARD.md:1632` (verified). But the sentence's
subject is the rejection, not the byte string, and one lane entry does document it:

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-1.md:111` — S024 row quoting
  "journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep
  filters." with pin `a923ab5ed1481512be6fb52aaa5086d0fef6878f`. (The same file's status paragraph,
  `round-1.md:127-129`, records that S024's anchor was later "stripped of commit pins that did not
  reproduce", so the pin is historical, not reproducible authority — cite the entry, not the pin.)

The note never mentions `round-1.md`; its QUALITY claim at `:111` ("its one whole-repo exception is named
(`SCORECARD.md:1632`)") is therefore false as a statement about the rejection. This is the same defect
wave 1 filed as blocking (ReviewC2Draft B4), unfixed.

Second defect in the same paragraph: "run at the base commit … and re-run in the working tree" (`:88`).
At the revision that carries the note, the command cannot return exit 1 — `git grep -l` at `c052bb7`
over `corpus/knowledge/ SKILL.md` returns the note itself (`corpus/knowledge/journalctl-v262-field-filter-r36.md`).
Say "pre-landing tree" or drop the re-run clause.

Fix: reword to "no lane entry carried the runtime line, exit code or flag matrix", cite
`corpus/lessons/round-1.md:111` as the prior prose record, and keep the exact-string sweep as the narrower
receipt it is. The declaration's Before text (`SCORECARD.md`, L1-owned) needs the same scoping.

## MINOR

### M1 — the predicate is 15 terms, not 16

Note `:126` ("the 16-term limiting-option predicate") and the registry rows
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/README.md:264` and `:269` ("16-term predicate").
The captured v262 predicate has 15 OR terms:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ScribeC2Draft/journalctl-filter-c-predicate.txt`
and `.../SrcSystemdNews/journalctl-filter.v262.c:27-41` (`arg_boot_filter`, `arg_invocation`, `arg_dmesg`,
`arg_cursor`, `arg_after_cursor`, `arg_cursor_file`, `arg_system_units`, `arg_user_units`,
`arg_syslog_identifier`, `arg_exclude_identifier`, `arg_priorities`, `arg_facilities`, `arg_since_set`,
`arg_until_set`, `arg_pattern`). The table itself is right: it has 15 limiter rows (`:23-39`). Correct
three sites, not the table.

### M2 — consumer inventory: "43 hits across 4 files" and "every occurrence" are imprecise

`:62` says every `journalctl` occurrence in `tools/` is covered by the table. Measured at HEAD:

- `grep -rn journalctl tools/` → **53** lines / **5** files, because the gitignored
  `tools/__pycache__/score-census-handoff-r32.cpython-314.pyc` matches; `--exclude-dir=__pycache__` gives
  **43 / 4**, matching the note. Add the exclusion (or `-I`) so the recorded command reproduces.
- "Every occurrence" is overbroad: `tsukuroi-census.sh` has 28 matching lines but the table lists 13
  (invocations + one fixture range). Not listed, for example: `:407`
  `JOURNALCTL=${TSUKUROI_JOURNALCTL:-journalctl}`, `:1911` fixture command list, `:2046`/`:2282`/`:2283`/
  `:2414`/`:2585` selftest env, and comment lines. The table covers every **invocation site**, which is
  the preventive point; say that.

### M3 — the fixture-regression sentence only holds for a flag-only invocation

`:82` says "a `-F`/`-N` invocation falls to the `*)` default arm and returns the *wrong* fixture
(`journal-all.json`)". In `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:1883-1902`
the `journalctl)` case tests `*--grep*`, `*--list-boots*`, `*"-p err"*` and `*"-n 1"*` **before** `*)`. A
future arm that appends `-F` to an existing arm (the realistic regression) matches that arm's earlier
case and returns its fixture, not `journal-all.json`. The conclusion (the fixture cannot catch the
regression class) holds; qualify the mechanism. The score stub
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-census-handoff-r32.py:150-165` has the same
shape, so the "same verdict" line is fine.

### M4 — `--machine=` / `--image=` neither tested nor marked

They appear nowhere in the note (`grep` rc 1) and in no cell. Wave-1 M3 asked for honesty marks on
selectors that could not be classified (root/remote paths). Add `[unk]` lines to §Unknowns, or a cell
with a valid target.

### M5 — the QUALITY 26 gloss is falsified by the note's own header

`:111` says "Criterion 26 (no package-manager invocation in a `recheck` procedure): the procedure names
no package manager and **the note contains none**." The criterion
(`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:36`) constrains `recheck:`
procedures only, and the note's `recheck:` line satisfies it. But the note's header (`:3`) records
"`pacman -Q systemd` = `systemd 262-1`", so "the note contains none" is false, and the measurement has no
capture id or steer-safe substitution (criterion 26 requires copying the read and recording the
substitution). The fact is redundant: `journalctl --version` already yields `systemd 262 (262-1-arch)`
(`matrix-mini.json` `journalctl_version_first_line`). Fix: drop the `pacman -Q` phrase; if kept, record
it as a prior capture, not a round-36 invocation.

### M6 — the positional `FIELD=VALUE` failure mode is unreceipted and points at the wrong guard

`:30` claims the extraneous-argument error "fires for … a positional `FIELD=VALUE` match supplied
alongside `-F`." No cell exercises it, and §Sources cites only `journalctl.c:958-960`; the extraneous
guard is at `journalctl.c:953-956` (captured in
`.../w1/SrcSystemdNews/journalctl.v262.c`). It is source-supported but neither receipted nor anchored at
the right lines. Add the line range and mark the example `[inf]`, or run
`journalctl --no-pager -F PRIORITY FOO=bar` (expect 1, `Extraneous arguments …`).

### M7 — falsifier 4's combined clause was never run

`:105`: "`journalctl --no-pager -n 1 -F PRIORITY` rejects, or `-b 0 -n 1 -F PRIORITY` succeeds". The
first half is receipted (`ext_lines1_F` exit 0, not falsified); the second half has no cell. The predicate
predicts REJECT (the `-b` term is set regardless of `-n`), but the note presents the combination as a
reading without marking it `[inf]`. This is also exactly the combination the `cap()` hazard imagines
(limiter + `-F`), so it is worth one cell.

### M8 — action precedence is undocumented; four cited cells never execute the named action

The v262 parser assigns `arg_action` per option, last assignment wins: `-N` `journalctl.c:802`, `-F`
`:806`, `--list-boots` `:813`, `--disk-usage` `:825`, `--sync` `:856`, `--header` `:877-878`. The cells
cited in table rows `:42` and `:44` therefore do not exercise the named non-field option:

- `live_list_boots` (`-F PRIORITY --list-boots`): `--list-boots` assigns the action last → boot list
  (541 stdout bytes), no field enumeration.
- `ext_diskusage_N` (`--disk-usage -N`): `-N` last → field names (2882 bytes), no disk usage.
- `ext_header_F` (`--header -F PRIORITY`): `-F` last → values (12 bytes), no header.
- `ext_sync_F` (`--sync -F PRIORITY`): `-F` last → `--sync` never runs.

The rows' `WORK` verdict (exit 0) remains correct because the guard at `journalctl.c:958` runs before
dispatch — so "not a limiter" holds — but the table must not be read as "the field list and that option
both execute". In particular `--sync` is a write request (`OPTION_LONG("sync", …, "Synchronize unwritten
journal messages to disk")`, `journalctl.c:856`); this ordering bypasses it, so the row is not evidence
that `--sync` is read-only or safe in any order. For contrast, `-n` is not an action assignment (B1).

Fix: one sentence on last-action-wins precedence plus, per cell, which action executed; or reorder the
argv and record the action that actually ran.

## Verified clean (do not re-litigate)

- Rejection line exact: 83 characters + LF = 84 stderr bytes (python `len` 83/84); `rejection_exit_code`
  1, `rejection_line_bytes_with_newline` 84 in `matrix-mini.json`; every limiter cell records
  `stderr_text` equal to the line, `rejection_line_present: true`, `stdout_bytes: 0`.
- Guard and origin: `journalctl.c:958-960` `IN_SET(arg_action, ACTION_LIST_FIELDS,
  ACTION_LIST_FIELD_NAMES) && field_list_has_scope_options()` → `log_error_errno(SYNTHETIC_ERRNO(EINVAL),
  …)`, captured verbatim in `.../w1/SrcSystemdNews/journalctl.v262.c` lines 958-960.
- All 15 predicate terms have a live cell that rejects with exit 1 / 84 bytes; `--boot=all`
  (`live_boot_all`, 12 bytes, exit 0) and `--quiet` with a limiter (`merged_field_quiet_boot0`, exit 1)
  behave as the note says.
- 40 distinct cell pointers in the table all resolve to `matrix-mini.json` entries; every one of the 54
  cells carries `argv`, `exit`, `stderr_bytes`, `stderr_text`, `stdout_bytes`, `stdout_sha256`.
- Peer cross-check: all 10 `ExecC2Live` runs map to a note cell and agree on exit code and stderr bytes
  (6 pre-existing core cells + 4 `merged_*`), so the note's "6 overlap / 4 re-run" statement holds.
- Extraneous-argument receipts: `merged_fields_default` 54 stderr bytes,
  `Extraneous arguments starting with 'PRIORITY,MESSAGE'`; `merged_fields_boot0` 46 bytes, `… 'PRIORITY'`
  — both as stated.
- Header trio: `tools/check-knowledge-header.py --revision c052bb7…` → `PASS`, 56/56 notes clean,
  findings `[]`, and the note is in scope with keys at lines 3/4/5. `corpus/SOURCES.md:205-206` gives
  S198 and S199 as tier `A`, checked `2026-10-23`, `recheck on-release`, used-by this note — consistent
  with the note's `verified-at: 2026-10-23` and `recheck: on-release`.
- Absence of the rejection string: 0 in the Arch `journalctl(1)` render, 0 in `journalctl-v262.xml`, 0 in
  the full v262 `NEWS` — the note's S198-silence and NEWS-prose claims hold.
- Preventive consumer claim: no lane tool invokes `journalctl` with `-F`/`-N` today
  (`grep -rn -- "--field\|--fields" tools/ --exclude-dir=__pycache__` rc 1, empty;
  `grep -rnE "journalctl[^|;]*( -F | -N )" …` empty). The cited sites verify: census `:971`, `:986`,
  `:1081`, `:1087`, `:1093`, `:1225`, `:1246`, `:1258`, `:1263`, `:1364`, `:1402`, `:1412`, fixture
  `:1883-1900`, `cap()` `:541-546`, `case` `:1247-1251`; score `:150-165`, `:708-731`; boot-chain `:870`
  (string); scope-correction `:174` (regex).
- Prior exact-string sweep at the base: exactly one hit, `SCORECARD.md:1632` — verified. (The overbroad
  sentence around it is B5, not the sweep.)

## Residual risk and verification gaps

- I did not re-execute the journalctl matrix; findings rest on the recorded cells (the note's own
  evidence class) and on read-only source/git/gate checks. No matrix cell was found internally
  inconsistent, so this does not weaken B1-B4. The `--file` exit-0 receipt is wave-1
  `ReviewC2Draft.md:61`'s, not mine and not its `matrix.out` (which has only `/nonexistent` rc 1).
- `--machine=`/`--image=` behaviour remains unmeasured (`[unk]`), as does any journal path not reachable
  read-only by this user. This is M4, not a contradiction of the note.
- Freeze/declaration order (outside this seat's judgment, for the sentinel/critic seats): the
  "pre-freeze corrections" block is not present at `6d76fb2` or at the freeze commit; it is appended at
  `c052bb7` (pure append, `@@ -1682,3 +1682,79 @@`, 0 deletions), with block text `2026-10-24T04:22Z`
  and commit times freeze `01:28:11 -0300`, change `01:28:31 -0300`; the freeze commit is an ancestor.
  The block's own text is what the note cites (item 7, S198/S199), and item 7 exists and matches the
  note's §Sources — flagged only because the label "pre-freeze" cannot be read off the git tree.
- No production file was edited; no VCS mutation; no package manager run; no tool installed.
