# RerunCoredumpReconcile — live rerun of the C2 note's host table (round 34, w2)

All times UTC, 2026-10-23. Read-only host actions. Counts only: no MESSAGE text, no stack
frames and no crashed-process command lines are reproduced here or in the report.

Host: Linux 7.2.11-arch1-1, systemd 262 (262-1-arch), journalctl 262, Python 3.14.8, git 2.56.0.
Boot 0 start: 2026-10-22T07:55:24Z (epoch 1792655724, `/proc/stat` btime). Disk: 155G free on /fast
at start; scratch use 471,241,148 bytes.

Note under test: `corpus/knowledge/coredump-count-unit-r34.md` at 879daa95b898b5c624c609eced31f7d0d5b933e8
(blob sha256 8c92629f4098d1159a0b69d4c445b4ba5743e3ad2d8e56b51d973edd7d6d1684). Its `recheck:`
line 5 was run verbatim. The committed host table and reading rule are what §1-§6 compare against.

## §1 Sample table — census arm reproduction

Capture: `timeout 300 journalctl -b -p err -o json --no-pager` (stderr 0 bytes every run, so the
census `cap` stdout+stderr merge is identical). Classes: the awk at `tools/tsukuroi-census.sh:1401-1412`
copied verbatim (coredump first, then kernel, else other). Kinds: the note's line-5 pipeline,
reduced to counts.

| sample (UTC) | err entries | coredump | kernel | other | classes sum | dumped text | null | terminated | handler | kinds sum |
|---|---|---|---|---|---|---|---|---|---|---|
| note 08:44:09Z | 1621 | — | — | — | — | 183 | 69 | 1365 | 4 | 1621 |
| note 08:48:49Z | 1635 | — | — | — | — | 183 | 69 | 1379 | 4 | 1635 |
| 09:18:14Z | 1832 | 1654 | 177 | 1 | 1832 | 198 | 73 | 1379 | 4 | 1654 |
| 09:22:08Z | 1832 | 1654 | 177 | 1 | 1832 | 198 | 73 | 1379 | 4 | 1654 |
| 09:24:26Z | 1832 | 1654 | 177 | 1 | 1832 | 198 | 73 | 1379 | 4 | 1654 |
| 09:27:19Z | 1833 | 1655 | 177 | 1 | 1833 | 198 | 73 | 1380 | 4 | 1655 |

MESSAGE_ID `fc2e22bc6ee647b6b90729ab34a250b1` count: 1650 at 09:18:14Z, 1651 at 09:27:19Z; coredump
entries without a MESSAGE_ID (handler errors, priority 3): 4 at both.

Verbatim line-5 procedure run at ~09:26Z on a fresh live read: 4 distinct output lines, 1655 rows:
198 `dumped core.`, 1380 `terminated abnormally ...`, 73 `null`, 4 other (handler). Output saved as
`recheck-raw-t3.txt` (sha256 feb86eceecb0642e862a0caddf85c2bd50964b7f4934d42c67b790a56c4ec992).

## §2 `--all` view (same stream, 09:18:14Z, `journalctl -b -p err -o json --all --no-pager`)

1832 lines (same entry set as default), classes identical 1654/177/1. Within the coredump class:

| kind | count |
|---|---|
| summary `dumped core.`, reduced by the note's sed | 269 |
| summary `dumped core.`, NOT reduced (process name contains `)`) | 2 |
| summary `terminated abnormally without generating a coredump.` | 1379 |
| handler error (priority 3, no MESSAGE_ID) | 4 |
| MESSAGE null | 0 |

Messages over 4096 UTF-8 bytes in the coredump class: 73. Default-JSON nulls: 73. Cursor join
exact: common 73, only-null 0, only-big 0. So the null set and the oversize set are the same set.

## §3 Identifier class (`journalctl -b -t systemd-coredump -o json --all --no-pager`)

| capture (UTC) | prio2 `coredump-submit.c:793` | prio3 `coredump-receive.c:100` | prio6 `coredump-kernel-helper.c:49` | prio6 `coredump-submit.c:270` | total | census share |
|---|---|---|---|---|---|---|
| 09:19:47Z | 1650 | 4 | 1654 | 1379 | 4687 | 35.29% |
| 09:27:19Z | 1651 | 4 | 1655 | 1380 | 4690 | 35.29% |

All 4687/4690 have `SYSLOG_IDENTIFIER=systemd-coredump` exactly. The priority-6 records are 64-255
bytes each. First word: 1654 start `Process` (kernel helper; of these, the 1652 whose prefix parses
with the note's non-greedy pattern continue with `terminated`, the other 2 carry `)` in the name),
1379 start `Resource`. `coredump-submit.c:270` is the
`log_info_errno(... "Resource limits disable core dumping for process "PID_FMT" (%s).")` early
return for `context->rlimit < page_size()` (saved source, sha256 54ce12400ce7e7c5ec4f8a6acdeac58659780434ed964f9c941f82ec11d0e538).
No priority-7 (debug) records exist in this boot.

## §4 Event joins (counts only)

- Terminated summaries (1379) vs `coredump-submit.c:270` RLIMIT info records (1379): embedded
  crash-PID sets are identical (`pids-terminated.txt` and `pids-rlimit.txt` have the same sha256,
  9ce28f4f67903dd265e2438c7db3fa33b8bc76144d3d2061dcf83316bdd170b1). Temporal join: 1379 pairs,
  0 summaries without a preceding info, 0 PIDs with multiple summaries, 0 PIDs with multiple info
  records; every pair delta is 0.000 s (`__MONOTONIC_TIMESTAMP` equal).
- Dumped summaries (271 unique PIDs) vs kernel-helper info (1654 unique PIDs): 271 common, 0
  only-dumped, 1383 only-helper. Terminated PIDs are all inside the kernel-helper set.
  Summaries (1650) + handler errors (4) = kernel-helper records (1654) at 09:19:47Z; and
  1651 + 4 = 1655 at 09:27:19Z.
- The 4 kernel-helper PIDs outside the summary PID set equal the handler-error count at both
  samples; handler messages embed no crash PID, so the association is arithmetic only.

## §5 coredumpctl (`coredumpctl list --since=@<boot epoch> --no-pager --no-legend`)

| capture (UTC) | records | COREFILE=none | notes |
|---|---|---|---|
| 09:22:54Z | 1650 | 1650 | census at 09:22:08Z was 1654; delta 4 = handler errors |
| 09:28:28Z | 1651 | 1651 | census at 09:27:19Z was 1655; delta 4 = handler errors |

The row's shape ("records; records whose corefile is none") still holds; both numbers moved.
Signal column was not interpreted (mori owns crash-cause/signal classification, OUT-005).

## §6 Effective configuration (`systemd-analyze cat-config systemd/coredump.conf`, rc 0)

`Storage=none`; `MaxUse=512M`; `KeepFree=8G`; `ProcessSizeMax` not present. Matches the note's
config statement.

## §7 Procedure defect observed

Under `--all`, the note's sed `s/^Process [0-9]+ \([^)]*\) of user [0-9]+ //` fails on 2 of the
271 dumped summaries: their process name is 15 bytes and contains one `)`, so the greedy name
field consumes the wrong span. Result: 269 reduced `dumped core.` lines and 2 raw
`Process <pid> (<name>) of user <uid> dumped core.` lines. Under default JSON those same 2 are
`null`, so no name is printed there, but the default view also cannot report them as dumped.

## §8 Artifacts (scratch, /fast/scratch/hyaku/tsukuroi-r34/RerunCoredumpReconcile/)

Full manifest with bytes and sha256: `MANIFEST.tsv`. Main captures:

| file | bytes | sha256 |
|---|---|---|
| cap-default-t0.jsonl | 17990438 | c1c0b8db75616445332af6c1ae212853ebfd3127d69338dbd04fec32ada9cd77 |
| cap-default-t1.jsonl | 17990438 | 21a44084be5d26988437f9ec7bf9f89a25744423052d8825a7c67581ed957289 |
| cap-default-t2.jsonl | 17990438 | 4ff0e859b68873c6fd02a476495f2bc89b36f394bf3f460ae50e8527269e2400 |
| cap-default-t3.jsonl | 18001072 | 72888034bca724f148bae15371f33e1e85acc465aa8430bf0a941dcc65920014 |
| cap-all-t0.jsonl | 130543066 | 2b2459791c84fcb6b707bf421c343eff5b33ed0084c6db4c7781d3a959985fa3 |
| cap-ident-all-t0.jsonl | 133890493 | 979cb634634b0dd8848c64c611ee5b22af95aaa7de78340d10a5b17dc6abe93a |
| cap-ident-all-t3.jsonl | 133959608 | 3f63f1cd299790f7422a5afa5a2be054acecb9087b4988d7a9c0d373fd4984a3 |
| coredumpctl-boot0-t0.txt | 252450 | 603a8c5a9eb3e81fdf469d33de4e1dba80eaea1fe8867ea5dc53dfd302362bd2 |
| coredumpctl-boot0-t4.txt | 252603 | e838bdbbf0ea2fe8daf552158277c73e188d9700ce4f61323615a7711c4a531e |

Note-version state at end of seat: worktree `corpus/knowledge/coredump-count-unit-r34.md` no longer
matches 879daa95 (worktree sha256 3dcb9ef7aa3872a3be8253daffdb36421326ff98d59982ef8eb4e1ab9312fd3f;
peer edits cite S189 at line 19 and append a "Corrections after wave 2" section). No lane file was
written by this seat.
