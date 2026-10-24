# journalctl inventory — lane tools + two knowledge notes

Stamp: 02:51:05Z (`date -u +%H:%M:%SZ` at mkdir). Host: `systemd 262 (262-1-arch)`, read at 02:47:29Z. Scan root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools` (`*.py`, `*.sh` only). 63 lines contain the string `journalctl`, in 6 files. None of those lines contain `-F`, `--field=`, `-N`, or `--fields`.

Rule used for the class column (systemd v262, not a paraphrase). Gate, `src/journal/journalctl.c:958-960` at tag `v262`:

```c
if (IN_SET(arg_action, ACTION_LIST_FIELDS, ACTION_LIST_FIELD_NAMES) && field_list_has_scope_options())
        return log_error_errno(SYNTHETIC_ERRNO(EINVAL),
                               "-F/--field= and -N/--fields cannot be combined with options that limit the journal.");
```

`-N`/`--fields` sets `ACTION_LIST_FIELD_NAMES` (`journalctl.c:801-803`). `-F`/`--field=` sets `ACTION_LIST_FIELDS` (`journalctl.c:805-810`). The limiter predicate is `field_list_has_scope_options` (`src/journal/journalctl-filter.c:26-43`):

```c
bool field_list_has_scope_options(void) {
        return
                arg_boot_filter ||          /* -b/--boot, --this-boot */
                arg_invocation ||           /* --invocation=, -I */
                arg_dmesg ||                /* -k/--dmesg */
                arg_cursor ||               /* --cursor= */
                arg_after_cursor ||         /* --after-cursor= */
                arg_cursor_file ||          /* --cursor-file= */
                !strv_isempty(arg_system_units) ||      /* -u/--unit= */
                !strv_isempty(arg_user_units) ||        /* --user-unit= */
                !strv_isempty(arg_syslog_identifier) || /* -t/--identifier= */
                !strv_isempty(arg_exclude_identifier) ||/* -T/--exclude-identifier= */
                arg_priorities != 0 ||      /* -p/--priority= */
                !set_isempty(arg_facilities) ||         /* --facility= */
                arg_since_set ||            /* --since= */
                arg_until_set ||            /* --until= */
                arg_pattern;                /* -g/--grep= */
}
```

Class:

- **working** — the surviving action is not `-F`/`-N`, or it is and `field_list_has_scope_options()` is false. Does not print the rejection line.
- **rejecting** — surviving action is `-F` or `-N` and at least one predicate bit above is set. stderr is exactly `-F/--field= and -N/--fields cannot be combined with options that limit the journal.` and rc=1.
- **would-reject** — this invocation is working today, but adding `-F` or `-N` while leaving that action in force would reject, because a predicate bit is already set.

Not limiters (source absent from the predicate; live rc=0 with `-N` on this host, 02:49–02:50Z): `-n`/`--lines`, `-o`/`--output`, `--no-pager`, `--all`, `--output-fields` (this is not `-F`/`--field=`), `-r`/`--reverse`, `--user`, `--system`, `--disk-usage`. `--list-boots` is a different action (`ACTION_LIST_BOOTS`); whichever of `-N` and `--list-boots` is parsed last wins, and neither order prints the rejection line (live: `--list-boots -N` printed field names, 167 lines, first `_PID`; `-N --list-boots` printed the boot table, 6 lines).

A different rc=1, not this rule: `journalctl --grep` with no match exits 1 and writes no stderr (census comment `tsukuroi-census.sh:192`, rechecked live below). `FIELD=VALUE` matches together with `-N` fail earlier, at `journalctl.c:953-956`, with `Extraneous arguments starting with '…'` (live: `-N --no-pager SYSLOG_IDENTIFIER=kernel`).

## 1. Real executions in tools/ — 12 `cap` calls, all working

All twelve are `cap "$JOURNALCTL" …` in `tools/tsukuroi-census.sh`. `JOURNALCTL=${TSUKUROI_JOURNALCTL:-journalctl}` at line 407. Grep constants: `CLASS_OOM` line 472 `Out of memory|oom-kill|oom_reaper`; `CLASS_OOM_SYS` line 476 `kernel OOM killer killed some processes`; `CLASS_SIGKILL` line 477 `status=9/KILL|Failed with result '(signal|oom-kill)'`.

Live column: this host, stdout discarded, 02:50:42Z for the six `--grep` rows; 02:49Z for the other six. `stderr` empty and rc=1 means no match, not the v262 rejection.

| file:line | function | full flag set | predicate bits | class | live |
|---|---|---|---|---|---|
| `tools/tsukuroi-census.sh:971` | `probe_drivers` | `-k -b -p err -o json --no-pager` | `-k` `-b` `-p` | working; would-reject | rc=0, stderr empty |
| `tools/tsukuroi-census.sh:986` | `probe_drivers` | `-k -b -o json --no-pager` | `-k` `-b` | working; would-reject | rc=0, stderr empty |
| `tools/tsukuroi-census.sh:1081` | `probe_mem_arm` | `-k -b -p err -o json --no-pager --grep 'Out of memory\|oom-kill\|oom_reaper'` | `-k` `-b` `-p` `--grep` | working; would-reject | rc=1, stderr empty (no match) |
| `tools/tsukuroi-census.sh:1087` | `probe_mem_arm` | `-b -o json --no-pager --grep 'kernel OOM killer killed some processes'` | `-b` `--grep` | working; would-reject | rc=0, stderr empty |
| `tools/tsukuroi-census.sh:1093` | `probe_mem_arm` | `-b -o json --no-pager --grep "status=9/KILL\|Failed with result '(signal\|oom-kill)'"` | `-b` `--grep` | working; would-reject | rc=0, stderr empty |
| `tools/tsukuroi-census.sh:1225` | `probe_oom_plane` | `--list-boots --no-pager` | none | working; not would-reject (`--list-boots` replaces the action) | rc=0, stderr empty |
| `tools/tsukuroi-census.sh:1246` | `probe_oom_plane` | `-k --grep 'Out of memory\|oom-kill\|oom_reaper' -o short-iso-precise --no-pager` | `-k` `--grep` | working; would-reject | rc=0, stderr empty |
| `tools/tsukuroi-census.sh:1258` | `probe_oom_plane` | `--grep 'kernel OOM killer killed some processes' -o short-iso-precise --no-pager` | `--grep` | working; would-reject | rc=0, stderr empty |
| `tools/tsukuroi-census.sh:1263` | `probe_oom_plane` | `--grep "status=9/KILL\|Failed with result '(signal\|oom-kill)'" -o short-iso-precise --no-pager` | `--grep` | working; would-reject | rc=0, stderr empty |
| `tools/tsukuroi-census.sh:1364` | `probe_journal` | `--list-boots --no-pager` | none | working; not would-reject | rc=0, stderr empty |
| `tools/tsukuroi-census.sh:1402` | `probe_journal` | `-b -p err -o json --no-pager` | `-b` `-p` | working; would-reject | rc=0, stderr empty |
| `tools/tsukuroi-census.sh:1412` | `probe_journal` | `-b -n 1 -o json --no-pager` | `-b` (`-n` is not a bit) | working; would-reject | rc=0, stderr empty |

### Journal arm (`probe_journal`, lines 1351-1412)

The arm's own `journalctl` calls are only the last three rows: `--list-boots --no-pager`, then `-b -p err -o json --no-pager`, then (only when that stream is empty) `-b -n 1 -o json --no-pager`. No `-F`, no `-N`, no `--field=`, no `--fields`. Arms 4 and 5 of the same function read the already-captured stream and call `systemctl`, not `journalctl`. Header comments at lines 240 and 242 match those flags; they do not add `-F`/`-N` either.

Zero rejecting invocations in `tools/`.

## 2. Passthrough — not a flag set of its own

`tools/score-census-handoff-r32.py` `LIVE_WRAPPER` (lines 707-718, rewritten at 723-727) execs `/usr/bin/journalctl "$@"` (or pipes it through `awk` for the `-b -p err -o json` shape). It adds no flags. The forwarded argv is whatever the census passed, i.e. the twelve rows above. Class of the wrapper itself: working, because it cannot introduce `-F`/`-N`.

## 3. String mentions in tools/ — not invocations

| file:line | what it is | flags, if a command is written | class if it were executed |
|---|---|---|---|
| `tools/check-boot-chain.py:870` | fixture transcript string `"$ journalctl --list-boots --no-pager \| tail -3"` | `--list-boots --no-pager` | working |
| `tools/check-source-scope-correction.py:174` | regex alternation naming the binary | none | n/a |
| `tools/score-census-handoff-r32.py:150-169` | fixture stub `case` on args; never execs the real binary | matches `--grep`, `-o short-iso-precise`, `--list-boots`, `-p err`, `-k`, `-n 1` | n/a (stub) |
| `tools/score-census-handoff-r32.py:183,188,469,796,799` | command name / `TSUKUROI_JOURNALCTL` path | none | n/a |
| `tools/score-pacnew-arm-r35.py:58`, `tools/score-pacnew-arm-r35b.py:77` | env-var name in a list | none | n/a |
| `tools/tsukuroi-census.sh:153,171,192,209,224,240,242,258` | comments | see §1; comments omit `--no-pager` on some rows the code includes | same as the matching `cap` row |
| `tools/tsukuroi-census.sh:364,407,966-989,1077,1080,1216-1229,1357-1368,1406` | variable, `have` checks, note strings | none beyond the `cap` rows in §1 | n/a |
| `tools/tsukuroi-census.sh:1883-1900` | selftest fixture dispatcher, same shape as the handoff stub | matches the census arg shapes; no `-F`/`-N` | n/a (stub) |
| `tools/tsukuroi-census.sh:1911,2046,2282,2283,2414,2585` | stub symlink name, env override, selftest expectations | none | n/a |

## 4. `corpus/knowledge/journal-boot-plane.md` — commands the note assumes

None use `-F`/`-N`. Class is by the predicate applied to the written flags. These were not re-run in this seat (the note's own capture is 2026-10-14). `-g` is `--grep` (`journalctl.c:614`).

| line | flag set | predicate bits | class |
|---|---|---|---|
| 14, 28, 388 | `--list-boots --no-pager` | none | working |
| 15, 388 | `--disk-usage` | none | working |
| 29, 83, 389 | `-b <n or bare> -p err -o json --no-pager` | `-b` `-p` | working; would-reject |
| 60, 216, 400 | `-b <n> -o short-monotonic --no-pager` | `-b` | working; would-reject |
| 65, 401 | `--no-pager -g 'PM: Image'` | `-g` | working; would-reject |
| 70 | `-b -n 2` | `-b` | working; would-reject |
| 75 | `--user` | none (`--user` is not a predicate bit; live `-N --user` rc=0) | working |
| 84, 390 | `-b -p err --no-pager` | `-b` `-p` | working; would-reject |
| 87, 391 | `-b -o json --no-pager` | `-b` | working; would-reject |
| 115, 392 | `-b -p warning -o json --no-pager` | `-b` `-p` | working; would-reject |
| 121 | `-b -p warning --no-pager` | `-b` `-p` | working; would-reject |
| 141 | `-b -o short-iso -g 'No Snapper config'` | `-b` `-g` | working; would-reject |
| 156-158, 397 | `--no-pager -p warning -g '<failed-unit pattern>' -o json` | `-p` `-g` | working; would-reject |
| 162 | `--user` plus the same sweep (ellipsis in the note) | `--user` is not a bit; `-p`/`-g` if carried over are | working; would-reject if `-p` or `-g` is kept |
| 171 | `-g` with no match (documents the stdout `-- No entries --` trap) | `-g` | working; would-reject |
| 180, 190 | `-b -g 'Startup finished'` / `-b <n> -g 'Startup finished'` | `-b` `-g` | working; would-reject |
| 298 | `-k` (fallback named, flags not otherwise given) | `-k` | working; would-reject |
| 399 | `--no-pager -g 'Startup finished'` | `-g` | working; would-reject |
| 402 | `--no-pager -g 'hibernation entry\|hibernation exit'` | `-g` | working; would-reject |
| 3, 302, 423, 439 | the word `journalctl`, no flags | none | n/a |

## 5. `corpus/knowledge/coredump-count-unit-r34.md` — commands the note assumes

`--output-fields` is not `-F`/`--field=`. `SYSLOG_IDENTIFIER=` and `MESSAGE_ID=` are match arguments, not `-F`. None of these commands are rejecting.

| line | flag set | predicate bits | class |
|---|---|---|---|
| 5 | `-b -p err -o json --no-pager` (then `jq`) | `-b` `-p` | working; would-reject. Same shape as the journal arm at `tsukuroi-census.sh:1402`, which live-ran rc=0 |
| 11 | `-b -p err -o json` (describes the census arm; the code also passes `--no-pager`) | `-b` `-p` | working; would-reject |
| 18 | `-o json`, and `--all` as the documented exception (S188 `journalctl.xml:591-593`) | none | working |
| 93 | `--boot=0 --priority=err --no-pager --output=json --output-fields=SYSLOG_IDENTIFIER,MESSAGE_ID,MESSAGE,PRIORITY` plus matches `SYSLOG_IDENTIFIER=systemd-coredump` `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1` | `--boot` `--priority` | working; would-reject if `-F`/`-N` were added. `--output-fields` does not cause it. A reduced live stand-in `--boot=0 --priority=err --output=json --output-fields=PRIORITY --no-pager -n 1` rc=0, stderr empty (02:49Z) |
| 99 | same as 93 plus `--all` | `--boot` `--priority` | working; would-reject |
| 105 | same as 99 but one match (`SYSLOG_IDENTIFIER=systemd-coredump` only) | `--boot` `--priority` | working; would-reject |
| 3, 47, 65, 118, 120 | citations of `journalctl(1)` / `--all` / `--output-fields`, no combined `-F`/`-N` command | none | n/a |

Adding `-N` to rows 93/99/105 would not be the limiter error first: match arguments on a non-show action die at `journalctl.c:953-956` (`Extraneous arguments…`), observed live for `SYSLOG_IDENTIFIER=kernel`.

## 6. Live rejection checks (this host, stdout discarded or line-counted only)

Rejection line observed, rc=1, for: `-N -b`, `-N -p err`, `-N -k`, `-N --grep=…`, `-N -g …`, `-N --boot=0`, `-N --priority=err`, `-N --since=today`, `-N --until=now`, `-N --dmesg`, `-F PRIORITY -b`, `-F PRIORITY -k -b -p err -o json`.

rc=0 (not the rejection) for: `-N`, `-F PRIORITY`, `-N -o json`, `-N -n 1`, `-N -n all`, `-N --all`, `-N --output-fields=PRIORITY`, `-N -r`, `-N --user`, `-N --system`, `-N --disk-usage`, `-F PRIORITY --output-fields=PRIORITY`, and every census flag set in §1.

No tool was installed. No production file was written.
