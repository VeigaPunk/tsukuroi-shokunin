# ScoutRecon — journalctl inventory (C2 recon)

Stamp: 02:51:05Z. Full table: `inventory.md` in this directory. No tool installed. No production file edited.

## Question

Every `journalctl` invocation under `tools/` (`*.py`, `*.sh`): file, line, full flag set, and whether systemd 262 rejects it (`-F`/`-N` combined with an option that limits the journal). Plus the commands assumed by `corpus/knowledge/journal-boot-plane.md` and `corpus/knowledge/coredump-count-unit-r34.md`, and whether `probe_journal` in `tools/tsukuroi-census.sh` uses `-F`/`-N`.

## Observed

Host binary: `systemd 262 (262-1-arch)` at 02:47:29Z. The rejection sentence is in `/usr/bin/journalctl` (`strings`). The predicate is the v262 tag, not the man page (the man page documents `-F` and `-N` and does not list the combination):

- Gate: `src/journal/journalctl.c:958-960` — fires only when the action is `ACTION_LIST_FIELDS` (`-F`/`--field=`, `:805-810`) or `ACTION_LIST_FIELD_NAMES` (`-N`/`--fields`, `:801-803`) **and** `field_list_has_scope_options()` is true.
- Predicate body: `src/journal/journalctl-filter.c:26-43`. Bits: `-b`/`--boot`/`--this-boot`, `--invocation=`/`-I`, `-k`/`--dmesg`, `--cursor=`, `--after-cursor=`, `--cursor-file=`, `-u`/`--unit=`, `--user-unit=`, `-t`/`--identifier=`, `-T`/`--exclude-identifier=`, `-p`/`--priority=`, `--facility=`, `--since=`, `--until=`, `-g`/`--grep=`.
- Not bits, live rc=0 beside `-N` on this host: `-n`, `-o`, `--no-pager`, `--all`, `--output-fields`, `-r`, `--user`, `--system`, `--disk-usage`. `--output-fields` is not `--field=`.
- `--list-boots` is a different action. Last of `-N` and `--list-boots` wins; neither order prints the rejection line (02:50:02Z: `--list-boots -N` → 167 field names, first `_PID`; `-N --list-boots` → 6-line boot table).
- A second rc=1 is not this rule. `--grep` with no match: rc=1, empty stderr (`tsukuroi-census.sh:192`; rechecked). `FIELD=VALUE` on `-N`: `Extraneous arguments starting with '…'` at `journalctl.c:953-956` (live, `SYSLOG_IDENTIFIER=kernel`).

Tools scan: 63 `journalctl` lines, 6 files. Zero lines contain `-F`, `--field=`, `-N`, or `--fields`.

Real executions: 12 `cap "$JOURNALCTL"` calls, all in `tools/tsukuroi-census.sh`, all **working** (no rejection line). Ten of the twelve carry a predicate bit, so they are **would-reject** if `-F` or `-N` were added and stayed the action. The two `--list-boots --no-pager` calls (`:1225` `probe_oom_plane`, `:1364` `probe_journal`) have no predicate bit.

`probe_journal` (`:1352-1412`) calls journalctl three times and never with `-F`/`-N`:

1. `:1364` `--list-boots --no-pager` — live rc=0
2. `:1402` `-b -p err -o json --no-pager` — live rc=0; bits `-b` `-p`; would-reject
3. `:1412` `-b -n 1 -o json --no-pager` (only if the err stream is empty) — live rc=0; bit `-b` only (`-n` is not a bit); would-reject

The other nine calls and the six live `--grep` results (exact `CLASS_*` strings, 02:50:42Z) are in `inventory.md` §1. One of them, `probe_mem_arm:1081`, exited 1 with empty stderr: no match, not the v262 line.

`journal-boot-plane.md` has 19 command rows in `inventory.md` §4. None include `-F`/`-N`. Every row that uses `-b`, `-p`, `-g`/`--grep`, or `-k` is working today and would-reject if `-F`/`-N` were added. `--list-boots`, `--disk-usage`, and bare `--user` would not. Not re-run this seat (note capture is 2026-10-14).

`coredump-count-unit-r34.md` assumes `journalctl -b -p err -o json --no-pager` (line 5; same bits as the journal arm) and three `--boot=0 --priority=err --output=json --output-fields=…` commands with `SYSLOG_IDENTIFIER=` / `MESSAGE_ID=` matches (lines 93, 99, 105). Those are working. `--output-fields` does not trip the rule (reduced live stand-in rc=0). They would-reject if `-F`/`-N` kept the action; adding `-N` actually dies first on the match arguments (`Extraneous arguments`).

`score-census-handoff-r32.py` `LIVE_WRAPPER` (`:713-717`) execs `/usr/bin/journalctl "$@"` and adds no flags.

## Inference

[inf] Nothing in `tools/` is exposed to this rejection until a caller adds `-F` or `-N`. The census flags that would become illegal are exactly the ones that already limit: `-b`, `-p`, `-k`, `--grep`. `--output-fields` plus `FIELD=VALUE` matches, which the coredump note already uses, is the shape that stays legal beside `-b`/`-p`.

[inf] A secondary writeup that treats `--user`, `--system`, `--directory=`, or `--file=` as the v262 limiter set does not match `journalctl-filter.c:26-43`. `--user` and `--system` were live-checked (rc=0 with `-N`). `--directory=` and `--file=` were not live-checked; they are absent from the predicate.

## Unknowns / dependencies

- [unk] Predicate bits the lane never passes were not live-checked: `--invocation`/`-I`, `--cursor`/`--after-cursor`/`--cursor-file`, `-u`, `--user-unit`, `-t`, `-T`, `--facility`. Class for those is the source predicate only.
- [unk] `journal-boot-plane.md:162` writes `journalctl --user …` with an ellipsis. The surrounding sentence points at the line 156 sweep; the flags inside the ellipsis are not spelled out.
- Dependency, absent by design this wave: `corpus/knowledge/journalctl-v262-field-filter-r36.md` does not exist yet. This inventory does not wait on it.
- The twelve census calls were classified by rc and the first stderr line only. Stdout was discarded (or, for the `--list-boots`/`-N` order check, reduced to a line count and a 40-character first line). Journal message bodies were not read.

## Confidence

High on the tools inventory, the journal-arm claim, and the working/would-reject split for every flag set that was live-run. High on the predicate quote (v262 source at the cited lines). Medium on knowledge-note rows that were classified from the predicate and not re-executed (all of `journal-boot-plane.md`; the long `jq` pipelines in the coredump note).
