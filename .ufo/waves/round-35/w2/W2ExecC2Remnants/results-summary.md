# Round-35 w2 — W2ExecC2Remnants — recheck of the wave-1 C2 remnants draft commands

Run date: 2026-10-23, host local 08:43–08:57 (-0300), UTC 11:43–11:57.
All four draft commands are read-only, wrapped in `timeout 60`, and were each executed
exactly once for the primary result. No sudo was needed: the journal reads succeeded as
the unprivileged user (`id` → uid=1000(vgpnk) groups 1000(vgpnk),967(docker),992(input),998(wheel)),
so the assignment's `sudo -n journalctl` allowance was not exercised.

The four script files are byte-identical to the draft's four ```sh blocks (verified by
extracting the fenced blocks from
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ScribeC2Remnants/C2-correction-block-draft.md`
and comparing sha256; all four matched):

| script | draft block sha256 prefix | draft line |
|---|---|---|
| cmd1_default_json.sh | 805471015acbef77 | 13 |
| cmd2_all_summary_id.sh | f46428870aa99ed1 | 19 |
| cmd3_all_identifier_entries.sh | 8e0fa5e0c8f72c9f | 25 |
| cmd4_coredumpctl_json.sh | 9b0098bd194e8608 | 31 |

## Primary results (each command run once, 2026-10-23 08:43:07–08:43:10 -0300)

| # | script | exit_code | counts | draft / w1 report counts | verdict |
|---|---|---|---|---|---|
| 1 | cmd1_default_json.sh | 0 | summary_records=1689, null_message=81, printed_message=1608 | 1,689 / 81 / 1,608 (draft:34; w1:9) | SAME |
| 2 | cmd2_all_summary_id.sh | 0 | summary_records=1689, dumped_core=306, no_core_written=1383, null_message=0 | 1,689 / 306 / 1,383 / 0 null (draft:34; w1:11) | SAME |
| 3 | cmd3_all_identifier_entries.sh | 0 | identifier_entries=1693, summary_id=1689, handler_no_message_id=4, other_message_id=0 | 1,693 / 1,689 / 4 / 0 (draft:34; w1:11) | SAME |
| 4 | cmd4_coredumpctl_json.sh | 0 | records=1827; corefile states none=1776, missing=50, present=1; first_keys=[corefile,exe,gid,pid,sig,size,time,uid] | 1,827 / 1,776 / 50 / 1 / 0 other (draft:34; w1:13) | SAME |

All four exit codes are now explicitly captured as 0. The w1 report recorded exit 0 for
commands 1 and 4 only and marked commands 2 and 3 as `[inf]` exit 0 because its wrapper did
not print a numeric status; this run closes that gap.

## Auxiliary read-only checks (not the four draft commands)

| id | what | exit | result |
|---|---|---|---|
| aux_awk_table_parse | the discarded `coredumpctl list` table-column awk parse, re-run once | 0 | rows=1827, every state count 0, corefile_column=6 — reproduces the w1 finding exactly |
| aux_awk_col7 | same table, COREFILE taken as `$(NF-2)` | 0 | rows=1827, none=1776, missing=50, present=1 — matches the JSON query exactly |
| aux_no_id_records | the four identifier entries with no `MESSAGE_ID` | 0 | count=4, all four messages are `Failed to initialize pidref: No such process` (the S189 handler-error class) |
| aux_crosscheck | summary entries with `MESSAGE` longer than 4096 bytes | 0 | over_4096=81, dumped_core_all=306, max MESSAGE length=38160 |
| aux_null_subset | composition of the >4096-byte subset | 0 | 81 of the over-4096 entries are "dumped core.", 0 are "terminated abnormally without generating a coredump." |
| aux_old_pipeline | the superseded header pipeline (note body line 5) | 0 | 1384 "terminated abnormally without generating a coredump." / 226 "dumped core." / 81 "null" / 4 handler errors |
| aux_cmd2_on_default | the draft's cmd2 filter run against default JSON | 5 | jq error: `null (null) and string ("dumped core.") cannot have their containment checked` |
| aux_default_split_fixed | the same split with the null guard `(((.MESSAGE // "")\|split("\n")[0]) // "")` | 0 | n=1691, dumped_printed=226, nocore_printed=1384, nulls=81 |
| aux_priority_scope | identifier entries in boot-0 at all priorities | 0 | 4774 total: prio 2 = 1691, prio 3 = 4, prio 6 = 3079 |
| aux_drift_probe / aux_drift_probe_b | identifier and coredumpctl counts at 08:46:39 and 08:46:43 | 0 | 1694 identifier / 1690 summary / 4 no-id; 1828 coredumpctl records (none 1777) |
| plain journalctl | `journalctl --boot=0 --priority=err ... SYSLOG_IDENTIFIER=systemd-coredump` without MESSAGE_ID | 0 | 1693 identifier entries, matching command 3 |
| census-equivalent grep | `journalctl -b -p err -o json --no-pager \| grep -c '"SYSLOG_IDENTIFIER":"systemd-coredump"'` | 0 | 1693 at 08:44, 1694 at 08:50, 1695 at 08:53 — always equal to command 3's identifier_entries at the same instant |
| boot-window split of coredumpctl | records before/after boot-0 start 2026-10-22T07:55:40Z | 0 | in boot-0: 1690 records, all `none`; before boot-0: 138 records (50 missing, 87 none, 1 present) |

## Files

- Scripts: `cmd1_default_json.sh`, `cmd2_all_summary_id.sh`, `cmd3_all_identifier_entries.sh`,
  `cmd4_coredumpctl_json.sh`.
- Outputs: `outputs/<name>.stdout`, `outputs/<name>.stderr`, `outputs/<name>.rc`.
- Digests: `sha256sums.txt` (sha256 of every saved output file).
