# systemd 262 rejects `journalctl -F`/`-N` combined with journal-limiting options (round 36, C2 exploratory)

source: S199 (systemd NEWS at the pinned `v262` tag, opened and pinned by `SrcSystemdNews` this round — supersedes S024, the mutable main URL, which stays queued and unchanged; `NEWS:129-133`, "CHANGES WITH 262" > "Feature Removals and Incompatible Changes:", fetched bytes sha256 `a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657`); S198 (`journalctl(1)` at systemd 262 — `https://man.archlinux.org/man/journalctl.1`, footer `systemd 262.1`, sha256 `aaae4efa61ff9c56e6249feb2f4527db57f1a4beb0eac4ad1eeb111a4bbb83c2`, opened by `SrcJournalctlMan` this round); the tag's own source bytes `src/journal/journalctl.c` (sha256 `285b3d0c…d5d0ab`, lines 958-960) and `src/journal/journalctl-filter.c` (sha256 `480f7a03…72f48`, lines 26-43); live read-only matrix on this host, 54 cells, `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json` (host systemd `262 (262-1-arch)`, `pacman -Q systemd` = `systemd 262-1`; the 4 `merged_*` cells re-run here from the `ExecC2Live` peer matrix, whose 6 overlapping cells agree on exit code and stderr byte count; the 15 `live_*` cells backfilled so every decision-table row names a cell)
verified-at: 2026-10-23
recheck: on-release (systemd major bump; re-run the matrix commands)

Status: exploratory note for round 36's C2 (axis depth). It documents one systemd 262 behaviour and the lane's exposure to it. It changes no tool, no census arm and no `SKILL.md` line, and claims no ordinal move.

## The rejection

Exact stderr line, byte-for-byte (83 characters + trailing newline = 84 stderr bytes), and the exit code:

```
-F/--field= and -N/--fields cannot be combined with options that limit the journal.
```

**Exit code 1** (`EINVAL`, via `log_error_errno(SYNTHETIC_ERRNO(EINVAL), …)` at `src/journal/journalctl.c:958-960`), guarded by `IN_SET(arg_action, ACTION_LIST_FIELDS, ACTION_LIST_FIELD_NAMES) && field_list_has_scope_options()`. Two failure texts must not be confused: the **scope rejection** above (exit 1) fires only when `-F`/`-N` is combined with a journal-limiting option; the **extraneous-argument** error `Extraneous arguments starting with '…'` (exit 1) fires for other misuse — e.g. `-N PRIORITY,MESSAGE` (`-N/--fields` takes **no** argument; it lists every field name in use), or a positional `FIELD=VALUE` match supplied alongside `-F`.

## Decision table

`REJECT` = exit 1 with the scope-rejection line; `WORK` = exit 0. Every row was run read-only on this host **and every row names its cell**; the last column is the `cell` field of `matrix-mini.json` (same seat dir), re-runnable from that cell's recorded `argv`.

| limiting option (v262 `field_list_has_scope_options()` term) | CLI form | verdict | evidence pointer |
|---|---|---|---|
| `arg_boot_filter` | `-b`, `--boot=` (any value except `all`) | **REJECT** | `core_boot0`, `core_boot_neg1`, `ext_boot0_F` |
| `arg_invocation` | `--invocation=` | **REJECT** | `live_invocation` (`--invocation=0123456789abcdef0123456789abcdef`) |
| `arg_dmesg` | `-k` | **REJECT** | `ext_kernel_F` (`-b 0 -k -F PRIORITY`) |
| `arg_cursor` | `--cursor=` | **REJECT** | `ext_cursor_F` |
| `arg_after_cursor` | `--after-cursor=` | **REJECT** | `live_after_cursor` |
| `arg_cursor_file` | `--cursor-file=` | **REJECT** | `live_cursor_file` |
| `arg_system_units` | `-u`, `--unit=` | **REJECT** | `core_unit_journald` |
| `arg_user_units` | `--user-unit=` | **REJECT** | `live_user_unit` |
| `arg_syslog_identifier` | `-t`, `--identifier=` | **REJECT** | `live_identifier` (`-t systemd`) |
| `arg_exclude_identifier` | `--exclude-identifier=` | **REJECT** | `live_exclude_id` |
| `arg_priorities` | `-p`, `--priority=` | **REJECT** | `ext_prio_F` |
| `arg_facilities` | `--facility=` | **REJECT** | `live_facility` (`--facility=3`) |
| `arg_since_set` | `--since=` | **REJECT** | `core_since_1h` |
| `arg_until_set` | `--until=` | **REJECT** | `ext_until_F` |
| `arg_pattern` | `--grep=` | **REJECT** | `ext_grep_F` |
| — (no limiting option) | `-F PRIORITY` alone; `-N` alone | **WORK** | `core_plain`, `ext_plain_N` |
| not a limiter | `-n`/`--lines`; `-f`/`--follow`; `-r`/`--reverse`; `-a`/`--all` | **WORK** | `ext_lines1_F`, `ext_lines1_N`, `ext_follow_F`, `ext_reverse_F`, `ext_all_F` |
| not a limiter | `--output-fields=`; `--disk-usage`; `--header`; `--sync` | **WORK** | `live_output_fields`, `ext_diskusage_N`, `ext_header_F`, `ext_sync_F` |
| not a limiter | `--root=`; `-D`/`--directory=`; `--user`; `--system`; `--namespace=` | **WORK** | `ext_root_F`, `ext_dir_F`, `live_user_scope`, `live_system_scope`, `live_namespace` |
| not a limiter | `--boot=all`; `--list-boots`; `--show-cursor`; `--merge` | **WORK** | `live_boot_all` (`--boot=all` sets no boot filter), `live_list_boots`, `live_show_cursor`, `live_merge` |
| not a limiter (does not exempt) | `--quiet` alongside a limiter | **REJECT** (inherits the limiter) | `merged_field_quiet_boot0` (`--quiet -b 0 -F PRIORITY`) |
| — (misuse, not scope rejection) | `-N PRIORITY,MESSAGE` | **REJECT**, but with `Extraneous arguments starting with 'PRIORITY,MESSAGE'` | `merged_fields_default` (54 stderr bytes); `merged_fields_boot0` for `-b 0 -N PRIORITY` (46 bytes) |

`-n` is the counter-example worth naming: `--lines` limits *how much* is printed but does not restrict the journal set, so it is not in the predicate and `-F` with `-n 1` succeeds.

## Safe substitution

v262's own NEWS gives the remedy: "Scripts relying on filtered field lists should be adjusted to query entries explicitly." Query the entries and reduce them locally:

```
journalctl --no-pager -b 0 -o json --output-fields=PRIORITY | jq -r '.PRIORITY' | sort -u
```

Verified live here: exit 0, output `2 3 4 5 6 7` (the distinct `PRIORITY` values in boot 0); the same pipeline with `-b -1` also exited 0 with the same six values. The pattern carries the limiting option (`-b`) *and* the field projection, because `--output-fields=` is not a limiter.

## Consumers in this lane

Every `journalctl` occurrence in `tools/` (`grep -rn journalctl /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/` — 43 hits across 4 files), with its verdict. "Unaffected" means the invocation as written cannot reach the scope rejection, because it never asks for a field list.

| site | invocation | verdict |
|---|---|---|
| `tools/tsukuroi-census.sh:971` | `$JOURNALCTL -k -b -p err -o json --no-pager` | unaffected (no `-F`/`-N`); every option it does use is a limiter, so adding `-F` here would reject |
| `tools/tsukuroi-census.sh:986` | `$JOURNALCTL -k -b -o json --no-pager` | unaffected |
| `tools/tsukuroi-census.sh:1081` | `$JOURNALCTL -k -b -p err -o json --no-pager --grep "$CLASS_OOM"` | unaffected |
| `tools/tsukuroi-census.sh:1087` | `$JOURNALCTL -b -o json --no-pager --grep "$CLASS_OOM_SYS"` | unaffected |
| `tools/tsukuroi-census.sh:1093` | `$JOURNALCTL -b -o json --no-pager --grep "$CLASS_SIGKILL"` | unaffected |
| `tools/tsukuroi-census.sh:1225` | `$JOURNALCTL --list-boots --no-pager` | unaffected |
| `tools/tsukuroi-census.sh:1246` | `$JOURNALCTL -k --grep "$CLASS_OOM" -o short-iso-precise --no-pager` | unaffected |
| `tools/tsukuroi-census.sh:1258` | `$JOURNALCTL --grep "$CLASS_OOM_SYS" -o short-iso-precise --no-pager` | unaffected |
| `tools/tsukuroi-census.sh:1263` | `$JOURNALCTL --grep "$CLASS_SIGKILL" -o short-iso-precise --no-pager` | unaffected |
| `tools/tsukuroi-census.sh:1364` | `$JOURNALCTL --list-boots --no-pager` | unaffected |
| `tools/tsukuroi-census.sh:1402` | `$JOURNALCTL -b -p err -o json --no-pager` | unaffected |
| `tools/tsukuroi-census.sh:1412` | `$JOURNALCTL -b -n 1 -o json --no-pager` | unaffected |
| `tools/tsukuroi-census.sh:1883-1900` | fixture `journalctl` stub dispatching on `args` | unaffected today; a `-F`/`-N` invocation falls to the `*)` default arm and returns the *wrong* fixture (`journal-all.json`) rather than an error — a fixture would not catch this regression class |
| `tools/score-census-handoff-r32.py:150-165` | fixture `journalctl` stub, same shape | same verdict as the census stub |
| `tools/score-census-handoff-r32.py:708-731` | `LIVE_WRAPPER` — `exec /usr/bin/journalctl "$@"` (pass-through) | unaffected today; inherits whatever the census asks, so it is affected the moment an arm adds `-F` |
| `tools/check-boot-chain.py:870` | `$ journalctl --list-boots --no-pager \| tail -3` inside a fixture-capture **string** | not an invocation (docstring text); unaffected |
| `tools/check-source-scope-correction.py:174` | `journalctl` as one word in a scope regex | not an invocation; unaffected |

**No lane tool uses `-F` or `-N` today.** The exposure is prospective and sharpest in one place: the census `cap()` helper merges stderr into stdout (`CAP_OUT=$("$@" 2>&1)`, `tools/tsukuroi-census.sh:541-546`) and the grep arms accept rc 1 as "0 entries" (`case "$CAP_RC" in 0 | 1)`, `:1247-1251`). Measured here: a `--grep` arm that *did* carry `-F` returns rc 1 **and** the rejection line on stderr, which `cap()` folds into the captured output, where it is counted as one journal line. Replicated with the census's own counting expression: the plain `--grep` no-match case yields the sentinel `-- No entries --` (1 line); the `--grep` + `-F` case yields the rejection sentence (1 line) — the same count from a completely different cause. A future census arm adding `-F` would report a plausible non-zero count instead of failing closed. This is a hazard statement about a hypothetical arm, not a defect in a shipped arm; no such arm exists.

## Prior state

Before this note, no lane entry documented this rejection. Counting command, run at the base commit `6d76fb20f6ecbc940e5c8fff36c74060c885e161` and re-run in the working tree:

```
$ grep -rl "cannot be combined with options that limit the journal" corpus/knowledge/ SKILL.md
$ echo $?
1
```

No output, exit 1 — the string appears in no knowledge entry and in no `SKILL.md` line. A whole-repo sweep at the same base finds exactly one further hit, in the round-36 declaration itself, `SCORECARD.md:1632`, where the same string appears inside the C2 prior-state counting command. The declaration named the string; no entry documented the behaviour. That is the gap this note closes.

## Falsifier

Falsified if any of these is observed on this host (systemd 262):

1. `journalctl --no-pager -b 0 -F PRIORITY` exits 0, exits non-1, or prints anything but the scope-rejection line. The counter is the exit code **and** the exact 84 stderr bytes.
2. `journalctl --no-pager --since '1 hour ago' -F PRIORITY` behaves differently from the `-b 0` cell. Both must reject, both setting a term of the predicate.
3. `journalctl --no-pager -F PRIORITY` (no limiter) rejects — falsifying the table's first row and the "safe substitution" reading.
4. `journalctl --no-pager -n 1 -F PRIORITY` rejects, or `-b 0 -n 1 -F PRIORITY` succeeds — falsifying the predicate reading.
5. The scope-rejection string is found in `journalctl(1)` at 262. It is **not** in the Arch 262.1 page nor in `man/journalctl.xml` at the `v262` tag (both grep counts 0); it lives in the source and in the shipped binary. A future 262.x man page documenting it would make this note's source attribution stale.
6. The v262 `NEWS` file turns out to carry the exact scope-rejection sentence. It does not: `NEWS` says only that `-F` is rejected "together with filters such as unit, boot, time, cursor or grep filters". The exact string is the runtime error, not the prose.

## QUALITY check

Criterion 1 (falsifiable): §Falsifier states six observable conditions, each a command plus an expected exit code or byte string. Criterion 2 (source): every decision-table row names a matrix cell; each cell records `argv`, exit code, stderr bytes, stdout byte count and stdout sha256; the note names S199, S198 and the two v262 source files with digests. Criterion 3 (observation/inference/unknown separation): the rejection line and the table are observations from executed commands; the term-to-CLI mapping is anchored to `journalctl-filter.c:26-43` and each term separately confirmed live; the `cap()` hazard is labelled a hazard about a hypothetical arm, since no such arm exists. Criterion 7 (S-row, tier A): S199 and S198 are both tier A docs. Criterion 8 (source/verified-at/recheck): all three header lines present, ISO date, `on-release` cadence. Criterion 9 (negative claims carry a bounded sweep): the prior-state claim carries its grep command, scope and base commit, and its one whole-repo exception is named (`SCORECARD.md:1632`). Criterion 14 (explicit QUALITY check): this section. Criterion 26 (no package-manager invocation in a `recheck` procedure): the procedure names no package manager and the note contains none.

## Unknowns

- [unk] Whether any systemd release after 262 restores the silently-ignored-filter behaviour or keeps the rejection. Upstream NEWS gives no forward statement beyond v262 and the change is not marked a Future Feature Removal, so permanence is not established.
- [unk] Behaviour on systemd versions before 262 — not tested on this host (it runs 262). The NEWS entry's presence at the `v262` tag and absence at `v261` (reported by `SrcJournalctlMan`) is a source-level statement, not a measurement.
- [inf] Whether a lane consumer will ever add `-F`/`-N`. No current arm does; the `cap()` hazard is a projected consequence, not an observed failure.
- [unk] Whether the `ExecC2Live` seat's `matrix.json` carries cells this note still lacks. It was absent when this seat began at 02:47Z and appeared at 02:58Z; its 10 cells were merged then — 6 overlap this note's matrix and agree on exit code and stderr byte count, and the 4 peer-only cells were re-run here as `merged_*` rather than transcribed. Any later revision of that file is not covered.
- [inf] That the man page's silence is deliberate upstream rather than an oversight; the sources show only that the sentence is absent.

## Sources

- S199 — systemd NEWS, pinned at tag `v262` (`NEWS:129-133`): the prose statement of the change and the "query entries explicitly" remedy. Supersedes S024 (the mutable main NEWS URL, left queued and unchanged) for this note, per the round-36 pre-freeze corrections item 7.
- S198 — `journalctl(1)` at systemd 262 (Arch, footer `systemd 262.1`): the `-N`/`-F` semantics and the §COMMANDS text. It does **not** carry the restriction.
- systemd `v262` `src/journal/journalctl.c` (958-960): the guard, the exact rejection string, the `EINVAL` origin.
- systemd `v262` `src/journal/journalctl-filter.c` (26-43): `field_list_has_scope_options()`, the 16-term limiting-option predicate.
- `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json`: the 54-cell live matrix (6 required core cells, 29 extended, 4 `merged_*` re-run from the `ExecC2Live` peer matrix, 15 `live_*` backfilled for the single-row evidence pointers), each with exit code, stderr bytes, stdout byte count and stdout sha256.

## Round 37 correction — predicate count, output states, action precedence and prior teaching

This addendum supersedes the active decision claims above where they say **16 terms**, describe `-n` as one undifferentiated `WORK` state, classify `--list-boots` as working field enumeration, or say no lane entry already carried the rejection. The original round-36 bytes and its saved measurements are retained as history.

### Predicate: 15 terms

`field_list_has_scope_options()` has **15 OR terms**, not 16: `arg_boot_filter`, `arg_invocation`, `arg_dmesg`, `arg_cursor`, `arg_after_cursor`, `arg_cursor_file`, `arg_system_units`, `arg_user_units`, `arg_syslog_identifier`, `arg_exclude_identifier`, `arg_priorities`, `arg_facilities`, `arg_since_set`, `arg_until_set`, and `arg_pattern` (`journalctl-filter.c:26-43` in the pinned v262 source snapshot). The outer selected-action guard is separate and is not a sixteenth predicate term.

### `-n`: distinct observed outputs for `-F` and `-N`

| Exact saved argv | Observed v262 result | Evidence |
|---|---|---|
| `journalctl --no-pager -n 1 -F PRIORITY` | accepted (exit 0); `-F` value list is truncated to one value (`5`) | `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json`, cell `ext_lines1_F`: stdout 2 bytes |
| `journalctl --no-pager -n 1 -N` | accepted (exit 0); `-N` field-name output is unchanged from plain `-N` | same matrix, `ext_lines1_N` and `ext_plain_N`: both 2882 bytes and identical stdout SHA-256 `3480f2aac48ee794f741dfd7dbffa31c86d933df70482db14adf5e57dfc2f20a` |

Thus `-n` is not a scope limiter, but the two enumeration actions have different output effects under it. These are saved 2026-10-23 host observations, not a universal output-length guarantee.

### Action replacement is not field enumeration

The saved `live_list_boots` cell uses `journalctl --no-pager -F PRIORITY --list-boots`, exits 0 and prints 541 bytes of boot-list output; it does not produce the field-value list. In the pinned v262 parser, `-F` sets `arg_action = ACTION_LIST_FIELDS` at `journalctl.c:805-809`, then `--list-boots` replaces it with `ACTION_LIST_BOOTS` at `:812-814`. The guard applies to the action selected after parsing. Therefore the result means the later action won, not that `-F` plus a limiter enumerated fields. Do not classify `--list-boots` as a successful field-enumeration exception.

### Prior state and source attribution

The broad sentence in the original `## Prior state` is superseded. The exact v262 NEWS rejection was already recorded in `corpus/lessons/round-1.md:111` and in SOURCES row S024 (queued; its earlier mutable pin remains withdrawn). This note adds the pinned/re-opened S199 provenance, the runtime signature and exit, the 15-term implementation boundary, the observed output distinctions, and the action-precedence correction; it does not newly discover the rejection. S199 was re-opened on 2026-10-25 at `https://raw.githubusercontent.com/systemd/systemd/v262/NEWS`; its located quote is “journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters.” (`CHANGES WITH 262`, lines 129-133, 16 words). S199 remains the existing mined row; no SOURCES status/recheck/used-by cell changed.

### QUALITY check for this correction

QUALITY 1-3, 7 and 14: pass — the finite predicate is pinned to source lines; the two `-n` output states and action replacement are separated as saved observations; prior NEWS teaching is acknowledged; S199 is reopened and its located quote resolves. No new host behavior, field-enumeration capability, coverage surface, or ordinal move is claimed.

## Round 37 correction — predicate count, output states, action precedence and prior teaching

This addendum supersedes the active decision claims above where they say **16 terms**, describe `-n` as one undifferentiated `WORK` state, classify `--list-boots` as working field enumeration, or say no lane entry already carried the rejection. The original round-36 bytes and its saved measurements are retained as history.

### Predicate: 15 terms

`field_list_has_scope_options()` has **15 OR terms**, not 16: `arg_boot_filter`, `arg_invocation`, `arg_dmesg`, `arg_cursor`, `arg_after_cursor`, `arg_cursor_file`, `arg_system_units`, `arg_user_units`, `arg_syslog_identifier`, `arg_exclude_identifier`, `arg_priorities`, `arg_facilities`, `arg_since_set`, `arg_until_set`, and `arg_pattern` (`journalctl-filter.c:26-43` in the pinned v262 source snapshot). The outer selected-action guard is separate and is not a sixteenth predicate term.

### `-n`: distinct observed outputs for `-F` and `-N`

| Exact saved argv | Observed v262 result | Evidence |
|---|---|---|
| `journalctl --no-pager -n 1 -F PRIORITY` | accepted (exit 0); `-F` value list is truncated to one value (`5`) | `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json`, cell `ext_lines1_F`: stdout 2 bytes |
| `journalctl --no-pager -n 1 -N` | accepted (exit 0); field-name output is unchanged from plain `-N` | same matrix, `ext_lines1_N` and `ext_plain_N`: both 2882 bytes and identical stdout SHA-256 `3480f2aac48ee794f741dfd7dbffa31c86d933df70482db14adf5e57dfc2f20a` |

Thus `-n` is not a scope limiter, but the two enumeration actions have different output effects under it. These are saved 2026-10-23 host observations, not a universal output-length guarantee.

### Action replacement is not field enumeration

The saved `live_list_boots` cell uses `journalctl --no-pager -F PRIORITY --list-boots`, exits 0 and prints 541 bytes of boot-list output; it does not produce the field-value list. In the pinned v262 parser, `-F` sets `arg_action = ACTION_LIST_FIELDS` at `journalctl.c:805-809`, then `--list-boots` replaces it with `ACTION_LIST_BOOTS` at `:812-814`. The guard applies to the action selected after parsing. Therefore the result means the later action won, not that `-F` plus a limiter enumerated fields. Do not classify `--list-boots` as a successful field-enumeration exception.

### Prior state and source attribution

The broad sentence in the original `## Prior state` is superseded. The exact v262 NEWS rejection was already recorded in `corpus/lessons/round-1.md:111` and in SOURCES row S024 (queued; its earlier mutable pin remains withdrawn). This note adds the pinned/re-opened S199 provenance, the runtime signature and exit, the 15-term implementation boundary, the observed output distinctions, and the action-precedence correction; it does not newly discover the rejection. S199 was re-opened on 2026-10-25 at `https://raw.githubusercontent.com/systemd/systemd/v262/NEWS`; its located quote is “journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters.” (`CHANGES WITH 262`, lines 129-133, 16 words). S199 remains the existing mined row; no SOURCES status/recheck/used-by cell changed.

### QUALITY check for this correction

QUALITY 1-3, 7 and 14: pass — the finite predicate is pinned to source lines; the two `-n` output states and action replacement are separated as saved observations; prior NEWS teaching is acknowledged; S199 is reopened and its located quote resolves. No new host behavior, field-enumeration capability, coverage surface, or ordinal move is claimed.

## Round 38 correction — duplicate round-37 block

The round-37 correction block appears twice in this note, and both copies were introduced by one commit: `543a7ce` (`543a7cee2c5119f42023aa72597ce452d4a060d5`, "round-37: correct journalctl v262 note and add finite counter", 2026-10-25T16:20:15-03:00). Its parent `8936643` holds 127 lines and no such heading, and `git log -G'^## Round 37 correction' -- corpus/knowledge/journalctl-v262-field-filter-r36.md` returns only `543a7ce`, so no later commit repaired or re-added the duplicate (swept 2026-10-26 over this file's full history).

The heading `## Round 37 correction — predicate count, output states, action precedence and prior teaching` sits at line 129 and again at line 158. The first copy occupies lines 129-157; the second occupies lines 158-185 and ends the file. `grep -c '^## Round 37 correction' corpus/knowledge/journalctl-v262-field-filter-r36.md` therefore returns 2, and it returns 2 at `543a7ce`, at the round-37 tip `c231d0b`, at the round-38 base `8bd001f` and at `5edb6c2`, the revision these line numbers were measured at. No commit after `543a7ce` edits this file, and the file is byte-identical at `543a7ce` and `5edb6c2` (sha256 `dedb5c2fa0e0efbad04cc38fd60896c7e479454d4b74f5818d9aa4625281483b`), so the line numbers are stable across that range and this appended block leaves them unchanged.

**Operative block: lines 129-157, the first copy.** Lines 158-185 are a duplicate: they assert nothing the first copy does not assert, so read every citation of "the round-37 correction" against lines 129-157 and treat lines 158-185 as inert history. Nothing is deleted by this correction, which is an append-only block in the sense of QUALITY 4.

The two copies differ in one phrase and one separator. In the `-n` output table the operative copy's `-N` row (line 142) prefixes the words `field-name output` with the code span `` `-N` `` and one space; the duplicate's `-N` row (line 171) begins that same cell at `field-name` directly, without the code span. That 5-byte omission is the only textual difference: `diff <(sed -n '129,157p' corpus/knowledge/journalctl-v262-field-filter-r36.md) <(sed -n '158,185p' corpus/knowledge/journalctl-v262-field-filter-r36.md)` reports one changed line (block-relative 14, note lines 142 and 171) and one deleted blank line (block-relative 29, note line 157, the separator before the duplicate heading). Block sizes are 3629 and 3623 bytes.

Which copy is operative is fixed by the committed conformance gate, not by position. `tools/check-journalctl-v262-corrections.py` requires that code span in the `-N` row (`:53`, selftest case `missing-n-unchanged` at `:115`). Scored on the first copy alone its `evaluate()` returns PASS with 0 findings; scored on the second copy alone it returns FAIL with exactly one `C2-CLAIM-MISSING` finding for the missing phrase; the note as committed at `5edb6c2` returns PASS with 0 findings. The first copy is therefore the load-bearing one, and a later round that deletes the duplicate would lose no gated content.

### QUALITY check for this correction

QUALITY 1-3, 4, 9 and 14: pass — every statement here is about committed bytes and carries its re-runnable command and scope (`grep -n '^## Round 37 correction'`, the `diff` above, `git log -G` over this file's history, and the gate's `--selftest`, which returns 7/7 PASS). The block deletes nothing, separates observation (line numbers, byte counts, diff shape) from inference (none is needed), and claims no new host behaviour, coverage surface or ordinal move.

## Round 38 addendum — precedence in both orders, and the `--list-boots --merge` guard

Re-opened `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c` on 2026-10-26 (1139 lines, sha256 `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab` — the bytes this note already pins), with `src/shared/options.h` (`f56c0cc6…`), `src/shared/options.c` (`110b3029…`) and `man/journalctl.xml` (`d54bbede…`) at the same tag. Host: `systemd 262 (262-1-arch)`. This addendum extends the round-37 correction above; it supersedes nothing in it. Every command below was read-only.

### (a) The losing command is silently discarded, in both orders

Both arms assign `arg_action` unconditionally inside one left-to-right parse loop: `-F/--field=` sets `ACTION_LIST_FIELDS` (`journalctl.c:805-810`, assignment at `:806`), `--list-boots` sets `ACTION_LIST_BOOTS` (`:812-814`, assignment at `:813`). `FOREACH_OPTION_OR_RETURN` is a sequential `for` over `option_parse(...)` (`options.h:255-259`), `optind` advances monotonically, and `shift_arg()` only compacts consumed tokens toward the front of `argv` (`options.c:34-42`, `:375-377`) — the option sequence is preserved, so the rightmost command survives.

No action-conflict diagnostic exists: the only "one of" checks in `parse_argv()` are for journal sources (`:935`) and `--since`/cursor (`:943`). The earlier command produces nothing at all; stdout is byte-identical to the same argv with that command removed.

| argv (`journalctl --no-pager …`) | rc | stdout | equals |
|---|---|---|---|
| `--list-boots -F PRIORITY` | 0 | 11 B, sha256 `cbfedf6a…91e20d` | `-F PRIORITY` — field values; boot list never printed |
| `-F PRIORITY --list-boots` | 0 | 447 B, sha256 `e55209f6…889d0fa2` | `-b 0 --list-boots` — boot table; field list never printed |
| `--list-boots -N` | 0 | 2849 B, sha256 `b07760c5…c9e3329cb` | `-N` |
| `-F PRIORITY -N` | 0 | 2849 B, sha256 `b07760c5…c9e3329cb` | `-N` |
| `-b 0 --list-boots` | 0 | 447 B, sha256 `e55209f6…889d0fa2` | plain `--list-boots` — `-b 0` has no effect on the boot table |

Absolute byte counts and sha256s are host-journal content (2026-10-26 snapshot), so they drift between rounds; the durable claim is the **equality** between an invocation and its one-command-stripped twin. Raw `-F PRIORITY` prints in journal order (`2 4 5 6 7 3`), not sorted — the sorted `2 3 4 5 6 7` in §Safe substitution is that pipeline's `sort -u`, not raw `-F` output.

### (b) `--list-boots --merge` rejects, and order can bypass the rejection

`if ((arg_boot || arg_action == ACTION_LIST_BOOTS) && arg_merge)` (`journalctl.c:962-964`) exits **1** with stderr `Using --boot or --list-boots with --merge is not supported.` (59 chars + newline = 60 bytes), 0 stdout bytes, raised in `parse_argv()` before any journal open (`journalctl.c:1019-1020`). `arg_boot` alone is sufficient: `-b 0 --merge -n 1` (action `SHOW`) rejects with the same line.

Because the guard tests the *selected* action, mixing a field action with `--list-boots` and `--merge` gives either an error or a silent no-op:

| argv (`journalctl --no-pager …`) | rc | stdout | stderr |
|---|---|---|---|
| `--list-boots --merge` | 1 | 0 B | 60 B merge message |
| `-F PRIORITY --list-boots --merge` | 1 | 0 B | 60 B merge message |
| `--list-boots -F PRIORITY --merge` | 0 | 11 B field values | — `--merge` silently ignored |
| `--list-boots -N --merge` | 0 | 2849 B field names | — `--merge` silently ignored |
| `--merge` | 0 | 63753114 B | — (measured once) |

So the string `--list-boots --merge` is a documented rejection (`:962-964`) that any caller defeats by placing `-F` or `-N` after `--list-boots`.

### Guard order decides which error is reported

The field-list scope guard (`:958-960`) precedes the merge guard (`:962-964`): `-F PRIORITY -b 0 --merge` yields the 84-byte `-F/--field= and -N/--fields cannot be combined with options that limit the journal.` line, not the merge line. With (a), one option multiset has three outcomes: `--list-boots -F PRIORITY -b 0` → rc 1 field-list line; `-F PRIORITY --list-boots -b 0` → rc 0 boot table; `-F PRIORITY -b 0 --merge` → rc 1 field-list line.

### The man page does not define precedence

`man/journalctl.xml:886` (§Commands): "The following commands are understood. If none is specified the default is to display journal records:" — nothing on mutual exclusion, on last-wins, or on mixing commands. Last-wins is implementation behaviour, not a documented contract. A caller that needs two reports must issue two `journalctl` invocations; an arm that wants merged output must verify `--merge` took effect, because a field action drops it without a message.

### Falsifier (round 38)

1. `journalctl --no-pager --list-boots -F PRIORITY` exits non-0, or its stdout differs from `journalctl --no-pager -F PRIORITY`.
2. `journalctl --no-pager -F PRIORITY --list-boots` stdout differs from `journalctl --no-pager -b 0 --list-boots`.
3. `journalctl --no-pager --list-boots --merge` exits 0, prints stdout, or its stderr is not the 60-byte merge line.
4. `journalctl --no-pager --list-boots -F PRIORITY --merge` exits non-0 (the bypass is order-sensitive).
5. `parse_argv()` at v262 gains an action-conflict diagnostic (today only `:935` and `:943` exist).
6. A later systemd documents command precedence; the "undocumented" clause here then becomes stale.

### Provenance (round 38)

Live matrix (17 rows: argv, rc, stdout bytes, stdout sha256, stderr bytes, stderr text): `.ufo/waves/round-38/w1/DefJournalDebt/live-matrix.jsonl`. Source excerpts: `.ufo/waves/round-38/w1/DefJournalDebt/journalctl.c-excerpt.txt`. File digests: `.ufo/waves/round-38/w1/DefJournalDebt/provenance.txt`.

### QUALITY note

1 (falsifiable): six conditions above. 2 (source): every claim is a `file:line` at the pinned tag plus an rc/byte/sha256 receipt. 3 (observation vs inference): the tables are executed observations; "no action-conflict diagnostic" is a source statement about the two "one of" checks at `:935` and `:943`, not an inference from silence. 7 (S-row, tier A): the v262 tag sources and `journalctl(1)`-derived `journalctl.xml`. Known limit: the merge-bypass asymmetry is shown on this host's systemd 262 build; no other build was tested.
