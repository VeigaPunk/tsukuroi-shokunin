# systemd 262 rejects `journalctl -F`/`-N` combined with journal-limiting options (round 36, C2 exploratory)

source: S024 (systemd NEWS at the pinned `v262` tag, re-opened and pinned by `SrcSystemdNews` this round; `NEWS:129-133`, "CHANGES WITH 262" > "Feature Removals and Incompatible Changes:", fetched bytes sha256 `a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657`); S198 (`journalctl(1)` at systemd 262 — `https://man.archlinux.org/man/journalctl.1`, footer `systemd 262.1`, sha256 `aaae4efa61ff9c56e6249feb2f4527db57f1a4beb0eac4ad1eeb111a4bbb83c2`, opened by `SrcJournalctlMan` this round); the tag's own source bytes `src/journal/journalctl.c` (sha256 `285b3d0c…d5d0ab`, lines 958-960) and `src/journal/journalctl-filter.c` (sha256 `480f7a03…72f48`, lines 26-43); live read-only matrix on this host, 54 cells, `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json` (host systemd `262 (262-1-arch)`, `pacman -Q systemd` = `systemd 262-1`; the 4 `merged_*` cells re-run here from the `ExecC2Live` peer matrix, whose 6 overlapping cells agree on exit code and stderr byte count; the 15 `live_*` cells backfilled so every decision-table row names a cell)
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

Criterion 1 (falsifiable): §Falsifier states six observable conditions, each a command plus an expected exit code or byte string. Criterion 2 (source): every decision-table row names a matrix cell; each cell records `argv`, exit code, stderr bytes, stdout byte count and stdout sha256; the note names S024, S198 and the two v262 source files with digests. Criterion 3 (observation/inference/unknown separation): the rejection line and the table are observations from executed commands; the term-to-CLI mapping is anchored to `journalctl-filter.c:26-43` and each term separately confirmed live; the `cap()` hazard is labelled a hazard about a hypothetical arm, since no such arm exists. Criterion 7 (S-row, tier A): S024 and S198 are both tier A docs. Criterion 8 (source/verified-at/recheck): all three header lines present, ISO date, `on-release` cadence. Criterion 9 (negative claims carry a bounded sweep): the prior-state claim carries its grep command, scope and base commit, and its one whole-repo exception is named (`SCORECARD.md:1632`). Criterion 14 (explicit QUALITY check): this section. Criterion 26 (no package-manager invocation in a `recheck` procedure): the procedure names no package manager and the note contains none.

## Unknowns

- [unk] Whether any systemd release after 262 restores the silently-ignored-filter behaviour or keeps the rejection. Upstream NEWS gives no forward statement beyond v262 and the change is not marked a Future Feature Removal, so permanence is not established.
- [unk] Behaviour on systemd versions before 262 — not tested on this host (it runs 262). The NEWS entry's presence at the `v262` tag and absence at `v261` (reported by `SrcJournalctlMan`) is a source-level statement, not a measurement.
- [inf] Whether a lane consumer will ever add `-F`/`-N`. No current arm does; the `cap()` hazard is a projected consequence, not an observed failure.
- [unk] Whether the `ExecC2Live` seat's `matrix.json` carries cells this note still lacks. It was absent when this seat began at 02:47Z and appeared at 02:58Z; its 10 cells were merged then — 6 overlap this note's matrix and agree on exit code and stderr byte count, and the 4 peer-only cells were re-run here as `merged_*` rather than transcribed. Any later revision of that file is not covered.
- [inf] That the man page's silence is deliberate upstream rather than an oversight; the sources show only that the sentence is absent.

## Sources

- S024 — systemd NEWS, pinned at tag `v262` (`NEWS:129-133`): the prose statement of the change and the "query entries explicitly" remedy.
- S198 — `journalctl(1)` at systemd 262 (Arch, footer `systemd 262.1`): the `-N`/`-F` semantics and the §COMMANDS text. It does **not** carry the restriction.
- systemd `v262` `src/journal/journalctl.c` (958-960): the guard, the exact rejection string, the `EINVAL` origin.
- systemd `v262` `src/journal/journalctl-filter.c` (26-43): `field_list_has_scope_options()`, the 16-term limiting-option predicate.
- `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json`: the 54-cell live matrix (6 required core cells, 29 extended, 4 `merged_*` re-run from the `ExecC2Live` peer matrix, 15 `live_*` backfilled for the single-row evidence pointers), each with exit code, stderr bytes, stdout byte count and stdout sha256.
