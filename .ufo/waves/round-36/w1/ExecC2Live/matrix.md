# systemd 262 `journalctl -F` / `-N` live matrix

Version first line: `systemd 262 (262-1-arch)` (exit 0, stderr 0 bytes). `journalctl --no-pager --list-boots` returned indices `-4, -3, -2, -1, 0` (exit 0, stderr 0); boot `-1` exists. Every requested matrix command was run read-only with stdout/stderr captured; tails are last 8 stdout lines. `matrix.json` holds argv, stdout byte/line counts, tails, stderr byte counts/tails, return codes and verdicts for each cell.

The exact limiting-option diagnostic is 84 stderr bytes:

> `-F/--field= and -N/--fields cannot be combined with options that limit the journal.`

| Invocation | stdout tail | stderr bytes / tail | exit | Verdict |
|---|---|---:|---:|---|
| `journalctl --no-pager -F PRIORITY` | `5, 6, 2, 4, 7, 3` | 0 / empty | 0 | Work |
| `journalctl --no-pager -N PRIORITY,MESSAGE` | empty | 54 / `Extraneous arguments starting with 'PRIORITY,MESSAGE'` | 1 | Reject: invalid `-N` usage, not the limit-combination error |
| `journalctl --no-pager -b 0 -F PRIORITY` | empty | 84 / exact limiting-option diagnostic above | 1 | Reject: field/limit combination |
| `journalctl --no-pager -b 0 -N PRIORITY` | empty | 46 / `Extraneous arguments starting with 'PRIORITY'` | 1 | Reject: invalid `-N` usage, not the limit-combination error |
| `journalctl --no-pager -b -p err -F PRIORITY` | empty | 84 / exact limiting-option diagnostic above | 1 | Reject: field/limit combination |
| `journalctl --no-pager --since '1 hour ago' -F PRIORITY` | empty | 84 / exact limiting-option diagnostic above | 1 | Reject: field/limit combination |
| `journalctl --no-pager -u systemd-journald -F PRIORITY` | empty | 84 / exact limiting-option diagnostic above | 1 | Reject: field/limit combination |
| `journalctl --no-pager -b 0 -o json -F PRIORITY` | empty | 84 / exact limiting-option diagnostic above | 1 | Reject: field/limit combination; `-b` is present |
| `journalctl --no-pager -b -1 -F PRIORITY` | empty | 84 / exact limiting-option diagnostic above | 1 | Reject: field/limit combination; boot `-1` exists |
| `journalctl --no-pager --quiet -b 0 -F PRIORITY` | empty | 84 / exact limiting-option diagnostic above | 1 | Reject: field/limit combination; `-b` is present |

## Disambiguating controls

| Invocation | stdout tail | stderr bytes / tail | exit | Verdict |
|---|---|---:|---:|---|
| `journalctl --no-pager -N` | `CURRENT_USE_PRETTY, DBUS_BROKER_MESSAGE_TYPE, DISK_AVAILABLE, DBUS_BROKER_LAUNCH_ARG0, LIMIT, AVAILABLE, COREDUMP_CONTAINER_CMDLINE, COREDUMP_FILENAME` | 0 / empty | 0 | Work; `-N/--fields` takes no positional field list |
| `journalctl --no-pager -b 0 -N` | empty | 84 / exact limiting-option diagnostic above | 1 | Reject: field/limit combination |
| `journalctl --no-pager -p err -F PRIORITY` | empty | 84 / exact limiting-option diagnostic above | 1 | Reject: priority limit alone is sufficient |
| `journalctl --no-pager --quiet -F PRIORITY` | `5, 6, 2, 4, 7, 3` | 0 / empty | 0 | Work; `--quiet` alone is not the limiter |
| `journalctl --no-pager -o json -F PRIORITY` | `5, 6, 2, 4, 7, 3` | 0 / empty | 0 | Work; `-o json` alone is not the limiter |

**Interpretation:** the specified `-N PRIORITY,MESSAGE` and `-N PRIORITY` forms do not test the limit-conflict behavior: `-N/--fields` takes no field-name argument, and both specified commands fail first on extraneous positional arguments. The no-argument `-N` control succeeds, while `-b 0 -N` produces the exact 84-byte limit-conflict error. For the two `-F` matrix rows that also include `-o json` or `--quiet`, separate controls show those modifiers alone work; the accompanying `-b` is limiting.

## Lane tools sweep

Search scope: recursive `tools/**/*.py` and `tools/**/*.sh` literal `journalctl` search, followed by the census's `JOURNALCTL` variable-use search. No executable lane call uses `-F`, `--field`, `-N` or `--fields`. The production census call sites below are **not field-list mode**, so the observed `-F`/`-N` incompatibility does not apply. These source calls were not individually executed as part of the matrix; verdict is structural, not a separate live result.

| File:line | Flag set / invocation | Verdict under the matrix |
|---|---|---|
| `tools/tsukuroi-census.sh:971` | `-k -b -p err -o json --no-pager` | Not rejected by this field-list rule; no `-F/-N` |
| `tools/tsukuroi-census.sh:986` | `-k -b -o json --no-pager` | Not rejected by this field-list rule; no `-F/-N` |
| `tools/tsukuroi-census.sh:1081` | `-k -b -p err -o json --no-pager --grep "$CLASS_OOM"` | Not rejected by this field-list rule; no `-F/-N` |
| `tools/tsukuroi-census.sh:1087` | `-b -o json --no-pager --grep "$CLASS_OOM_SYS"` | Not rejected by this field-list rule; no `-F/-N` |
| `tools/tsukuroi-census.sh:1093` | `-b -o json --no-pager --grep "$CLASS_SIGKILL"` | Not rejected by this field-list rule; no `-F/-N` |
| `tools/tsukuroi-census.sh:1225` | `--list-boots --no-pager` | Not rejected by this field-list rule; no `-F/-N` |
| `tools/tsukuroi-census.sh:1246` | `-k --grep "$CLASS_OOM" -o short-iso-precise --no-pager` | Not rejected by this field-list rule; no `-F/-N` |
| `tools/tsukuroi-census.sh:1258` | `--grep "$CLASS_OOM_SYS" -o short-iso-precise --no-pager` | Not rejected by this field-list rule; no `-F/-N` |
| `tools/tsukuroi-census.sh:1263` | `--grep "$CLASS_SIGKILL" -o short-iso-precise --no-pager` | Not rejected by this field-list rule; no `-F/-N` |
| `tools/tsukuroi-census.sh:1364` | `--list-boots --no-pager` | Not rejected by this field-list rule; no `-F/-N` |
| `tools/tsukuroi-census.sh:1402` | `-b -p err -o json --no-pager` | Not rejected by this field-list rule; no `-F/-N` |
| `tools/tsukuroi-census.sh:1412` | `-b -n 1 -o json --no-pager` | Not rejected by this field-list rule; no `-F/-N` |
| `tools/score-census-handoff-r32.py:713` | `/usr/bin/journalctl "$@"` via `exec` in the `-k` branch | Dynamic pass-through; verdict depends on caller argv. Census callers above do not pass `-F/-N`. |
| `tools/score-census-handoff-r32.py:715` | `/usr/bin/journalctl "$@"` (rewritten to a filter pipeline in the mutant wrapper) | Dynamic pass-through; no fixed field-list flags; census caller has no `-F/-N`. |
| `tools/score-census-handoff-r32.py:717` | `/usr/bin/journalctl "$@"` via `exec` fallback | Dynamic pass-through; verdict depends on caller argv. Census callers above do not pass `-F/-N`. |

Other grep hits were not executable invocations: `tools/check-boot-chain.py:870` is a captured transcript fixture; `tools/check-source-scope-correction.py:174` matches command names in a lint rule; `tools/score-census-handoff-r32.py:150-169` is the fixture dispatcher, while lines 183/188 and 469 describe stub setup. No rejecting `-F/-N` invocation was found in the lane tools sweep.