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
