# Patch proposal — C2 action-override classification (design item 7/12, Build7C239)

Target (read-only source of truth): `corpus/knowledge/journalctl-v262-field-filter-r36.md`,
Decision table section (`## Decision table` … `## Safe substitution`). This is a
proposal only — nothing in the lane is changed by this seat.

## Why

The round-36 verifier spot-check routed defect (SCORECARD.md:1909-1916) requires an
"action-override classification row". W2CritC2Depth (c2-depth-ruling.md §5, lines
87-101) specifies it: separate **action overwritten / last action selected** from
**genuine accepted field-enumeration scope selectors**; preserve exact argv order;
describe the scope list as "not rejected by this guard", not blanket success.

Baseline rows that misclassify (current note):

```
| not a limiter | `--output-fields=`; `--disk-usage`; `--header`; `--sync` | **WORK** | `live_output_fields`, `ext_diskusage_N`, `ext_header_F`, `ext_sync_F` |
| not a limiter | `--boot=all`; `--list-boots`; `--show-cursor`; `--merge` | **WORK** | `live_boot_all` (`--boot=all` sets no boot filter), `live_list_boots`, `live_show_cursor`, `live_merge` |
```

`--disk-usage`, `--header`, `--sync`, `--list-boots` are action flags
(`src/journal/journalctl.c` at v262: `--list-boots` → `ACTION_LIST_BOOTS` lines
812-814; `--disk-usage` → `ACTION_DISK_USAGE` 824-826; `--sync` → `ACTION_SYNC`
856-858; `--header` → `ACTION_PRINT_HEADER` 877-879). Each *replaces* `arg_action`;
when one appears **after** `-F`/`-N`, the guard `IN_SET(arg_action,
ACTION_LIST_FIELDS, ACTION_LIST_FIELD_NAMES) && field_list_has_scope_options()`
(journalctl.c:958-960) has no field-list action to fire on, so exit 0 means the
*other action ran* — not that field enumeration succeeded.

## Proposed patch (table rows)

Replace the two rows above with:

```
| not a limiter | `--output-fields=`; `--root=`; `-D`/`--directory=`; `--user`; `--system`; `--namespace=` | **WORK** | `live_output_fields`, `ext_root_F`, `ext_dir_F`, `live_user_scope`, `live_system_scope`, `live_namespace` |
| not a limiter | `--boot=all`; `--show-cursor`; `--merge` | **WORK** | `live_boot_all` (`--boot=all` sets no boot filter), `live_show_cursor`, `live_merge` |
| action override — last action selected | `--list-boots` **after** `-F`/`-N` (e.g. `-F PRIORITY --list-boots`) | exit 0, but output is the **boot table**, not the field list; `--list-boots` replaced the `-F` action (`ACTION_LIST_BOOTS`, journalctl.c:812-814), so the guard at :958 has no field-list action to fire on | `live_list_boots` |
| action override — last action selected | `--disk-usage`, `--header`, `--sync` **after** `-F`/`-N` | exit 0, but output is that action's own output (disk usage line / header information / sync notice), not the field list; the action flag is overwritten (journalctl.c:824-826, 877-879, 856-858) | `live_diskusage_F`, `live_header_F` (probed 2026-10-25) |
| action override — last action selected (reverse order) | `-F`/`-N` **after** an action flag (e.g. `--list-boots -F PRIORITY`, `--disk-usage -N`, `--header -F PRIORITY`) | exit 0 **and** genuine field enumeration: the field action is selected last, so the guard still applies when a limiter is present | `ext_diskusage_N`, `ext_header_F`, `ext_sync_F` |
```

The rejection line stays verbatim; the 15 limiter rows are untouched.

## Evidence the after-state row relies on (observed 2026-10-25, systemd 262)

| argv (read-only) | exit | stdout | meaning |
|---|---|---|---|
| `journalctl --no-pager -F PRIORITY` | 0 | 12 B, values 2 4 5 6 7 3 | genuine field enumeration |
| `journalctl --no-pager -F PRIORITY --list-boots` | 0 | 262 B boot table (IDX BOOT ID …) | action replaced → not field output |
| `journalctl --no-pager --list-boots -F PRIORITY` | 0 | 12 B values | reverse order → field action last |
| `journalctl --no-pager --disk-usage -F PRIORITY` | 0 | 12 B values | reverse order → field action last |
| `journalctl --no-pager -F PRIORITY --disk-usage` | 0 | 61 B "Archived and active journals take up 56M…" | action replaced |
| `journalctl --no-pager --header -F PRIORITY` | 0 | 12 B values | reverse order → field action last |
| `journalctl --no-pager -F PRIORITY --header` | 0 | 5198 B header info | action replaced |
| `journalctl --no-pager -F PRIORITY -b 0` | 1 | stderr 84 B rejection line | guard applies when field action is final |
