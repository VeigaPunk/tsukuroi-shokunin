# What the census coredump count counts (round 34, C2 exploratory, depth)

source: S186 (systemd v262 `src/coredump/coredump-submit.c`, `coredump-context.c`, `coredump-config.c`, `src/systemd/sd-messages.h`); S187 (systemd v262 `coredump.conf(5)`); S188 (systemd v262 `journalctl(1)` and journal export/JSON formats); S177 re-opened (systemd v262 `systemd-coredump(5)`, digest unchanged); host captures `.ufo/waves/round-34/w1/ExecCoredumpReconcile/capture.txt` (2026-10-23 08:44Z and 08:49Z) and `.ufo/waves/round-34/w1/SrcCoredumpConf.md` finding 5
verified-at: 2026-10-23
recheck: on-release of systemd (re-open S186-S188) and 30d for the host counts; procedure: `journalctl -b -p err -o json --no-pager | jq -r 'select(.SYSLOG_IDENTIFIER=="systemd-coredump") | (.MESSAGE // "null" | tostring | split("\n")[0])' | sed -E 's/^Process [0-9]+ \([^)]*\) of user [0-9]+ //' | sort | uniq -c`, then `systemd-analyze cat-config systemd/coredump.conf`

Status: exploratory note for round 34's C2 (axis depth). It explains the counting unit of an existing census arm. It changes no census code and classifies no crash by cause: signal-11 coredump classification belongs to mori (`PROVINCE.md` OUT-005, `:125`), and this note neither counts by signal nor names crashed programs.

## The question

The census journal arm counts, in the boot-0 `journalctl -b -p err -o json` stream, every line that carries `"SYSLOG_IDENTIFIER":"systemd-coredump"` (`tools/tsukuroi-census.sh:1403-1410`). It prints that number twice: as `coredump=N` in the PLANE journal note and, through the same variable `JRN_COREDUMPS`, as `HANDOFF ADJ-04 mori class=coredumps value=N` (`:2780-2782`). The census comment calls this class "the storm signal" (`:263-267`), and `SKILL.md` snapshot lines (for example `:541`, `:884`, `:1214`) read `coredump=N` as a number of coredumps. Before this note, no lane entry said what one counted entry is.

## What systemd v262 logs per crash (sources)

- One summary record per crash, two wordings. `coredump-submit.c` picks the summary text by whether the temporary core write succeeded: `written ? "dumped core." : "terminated abnormally without generating a coredump."` (S186, lines 709-712; `written` set at 645-650). Both wordings go out with the same `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1` and `PRIORITY=LOG_CRIT` (S186, `coredump-context.c:360-361`; `sd-messages.h:41-42`), so `-p err` keeps both.
- "dumped core" is not "a core is stored". After a successful write the file can still be removed by storage policy without resetting `written` (S186, `coredump-submit.c:452-467`, `:652-668`). `coredump.conf(5)`: with `Storage=none`, "the core dumps may be logged (including the backtrace if possible), but not stored permanently" (S187, lines 78-80).
- What makes a crash "without generating a coredump": the write reports failure when `RLIMIT_CORE` is below one page, when both the processing and storage size limits are zero, or when copying the core fails (S186, `coredump-submit.c:265-277`, `:350-354`). No rate limit chooses between the two wordings in that branch.
- Why some records have no text in the census capture: `journalctl -o json` prints a field larger than 4096 bytes as null unless `--all` is given (S188, `journalctl.xml:591-593`). A "dumped core" summary that carries a long backtrace crosses that size.
- Records under the same identifier that are not crash summaries: the receiving handler logs its own errors under `SYSLOG_IDENTIFIER=systemd-coredump` at priority 3 without a `MESSAGE_ID` (ExecCoredumpReconcile, v262 `coredump-receive.c:100`, read in that seat; not a registered row).

## Reconciliation on this host (dated snapshot, 2026-10-23; re-run, never quote as current)

Effective configuration: `/etc/systemd/coredump.conf.d/storage.conf` sets `Storage=none`; `limit.conf` sets `MaxUse=512M`, `KeepFree=8G`; `ProcessSizeMax` is not set (SrcCoredumpConf finding 5).

| boot-0 `-p err` entries with `SYSLOG_IDENTIFIER=systemd-coredump` | 08:44:09Z | 08:48:49Z |
|---|---|---|
| census `coredump=` and handoff `value=` (live census runs at 08:44:32Z and 08:50:32Z) | 1621 | 1635 |
| summary "dumped core." (first MESSAGE line, default JSON) | 183 | 183 |
| summary with MESSAGE printed as JSON null (all "dumped core." under `--all`) | 69 | 69 |
| summary "terminated abnormally without generating a coredump." | 1365 | 1379 |
| handler error records (priority 3, no `MESSAGE_ID`) | 4 | 4 |
| sum of the four kinds | 1621 | 1635 |
| `coredumpctl` records in the boot-0 window; records whose `corefile` is `none` | 1617; 1617 | 1631; 1631 |

Evidence: `.ufo/waves/round-34/w1/ExecCoredumpReconcile/capture.txt:34-67` (round 1), `:129-162` (round 2), `:181-185` (corefile field), `:246-266` (drift table and answer). The 14 new entries in five minutes are all "without generating a coredump".

## Reading rule

- Read `coredump=N`, and `class=coredumps value=N` copied from it, as a count of boot-0 error-or-higher journal entries under the `systemd-coredump` identifier. On this host at the capture time, 252 of 1621 were "dumped core" summaries, 1365 were "without generating a coredump" summaries and 4 were handler errors.
- It is not a count of stored or retrievable cores: with `Storage=none` every `coredumpctl` record here has `corefile` `none`. It is not a count of distinct crashing programs or of signal-11 crashes, and it says nothing about cause. A rising value during this capture was driven only by crashes for which no core was written.
- To count crash summaries, select `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1` (S186); to count successful core writes, also split on the summary wording, reading MESSAGE with `--all` (S188). Neither split is implemented in the census; this round changes no census code.
- The handoff packet stays `state=prepared`. Mori declares its own scoped catalog-ID record counts (mori `PROVINCE.md:8-9,24`, `SKILL.md:31` at `f2d28711`, CritC2Absorb finding 4) and no intake contract for `class=coredumps`; this note does not define one. The value is described to mori as entries, not as crashes.

## Unknowns

- [unk] Which of the three failure causes produced the 1365 "without generating a coredump" summaries. `ProcessSizeMax` is unset, so the "both limits zero" cause needs a zero processing limit that this configuration does not set; `RLIMIT_CORE` per crashed process was not read. Reading it would need per-process limits at crash time, which the journal summary does not carry in the fields read here.
- [unk] Whether the 69 null-MESSAGE entries are all "dumped core": the `--all` view printed 252 "dumped core" first lines and 0 nulls (ExecCoredumpReconcile; SrcJournalctlJson finding 3 counts 69 messages over 4096 bytes), which supports it for this capture only.

## QUALITY check

Criteria applied to this entry (`corpus/QUALITY.md`):

- 1-3: each statement is a sourced observation, a dated count with its capture line, or marked [unk]; the reading rule is the only inference and it rests on the S186 branch and the capture.
- 7: external claims cite S186, S187, S188 (tier A, tag v262, line anchors) and S177; no tier-C source.
- 8: `source:`, `verified-at:` and `recheck:` (cadence `on-release` and `30d`) are present.
- 9: the negative statements ("no rate limit chooses the wording", "no note said what one entry is") rest on S186 lines 265-277 and 645-712 and on the ScoutCoredumpReaders sweep (`.ufo/waves/round-34/w1/ScoutCoredumpReaders.md`, commands listed there, 2026-10-23).
- 19 and 66: every source proposition is the one its quoted lines state; "may be logged" is kept as "may", not "is".
- 26: the recheck procedure runs no package, service or boot action.
- 35 and adjacency: no crash-cause, signal or program classification; mori's scope is quoted, not changed.

## Sources

- S186: systemd v262 coredump journal implementation (code, tier A).
- S187: systemd v262 `coredump.conf(5)` (docs, tier A).
- S188: systemd v262 `journalctl(1)` and journal export formats (docs, tier A).
- S177: systemd v262 `systemd-coredump(5)`, re-opened 2026-10-23, digest `56bed6ed…` unchanged (SrcCoredumpCode finding 1).
