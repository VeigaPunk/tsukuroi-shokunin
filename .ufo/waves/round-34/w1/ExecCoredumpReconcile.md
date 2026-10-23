# Seat report — ExecCoredumpReconcile (round 34, wave 1, C2 host reconciliation)

**Verdict: the census `coredump=` (and therefore the ADJ-04 `class=coredumps value=`, the
same variable) equals the total of *all* first-MESSAGE-line kinds — every boot-0 journal
entry whose SYSLOG_IDENTIFIER is `systemd-coredump` — and is not a count of cores dumped.**
Two captures about five minutes apart read `coredump=1621` and `coredump=1635`; the
`dumped core` class stayed at 183 in the default JSON view (252 with `-a`) while the
`terminated abnormally without generating a coredump` class carried the whole +14 drift.

Everything below is read-only host evidence. Commands, UTC timestamps and outputs are in
`.ufo/waves/round-34/w1/ExecCoredumpReconcile/capture.txt` (sha256
`e43892ee4f5727c0dc76201b4508f17988c8d4640d1dfdfbc4217ea1ed95473b`, 20,415 bytes). No stack
frame, command line or crashed-process name is printed here or there.

## Findings

1. [obs] **The arm's capture command and awk were replayed on the same bytes, and a live
   census run agreed.** The arm is `cap "$JOURNALCTL" -b -p err -o json --no-pager` at
   `tools/tsukuroi-census.sh:1395`, then a one-pass awk at `:1403-1408`
   (`/"SYSLOG_IDENTIFIER":"systemd-coredump"/`, then kernel, then other), and
   `JRN_COREDUMPS=$cd_n` at `:1410`. Replay at 2026-10-23T08:44:09Z: `err_n=1777`,
   `coredump=1621 kernel=155 other=1`. A live `bash tools/tsukuroi-census.sh` at
   08:44:32-08:44:37Z (exit 1, DEGRADED) printed
   `PLANE journal: … err=1777 (coredump=1621 kernel=155 other=1)` and
   `HANDOFF ADJ-04 mori class=coredumps value=1621 …`. Second replay at 08:48:49Z:
   `coredump=1635 kernel=157 other=1`; live census at 08:50:32Z printed `coredump=1635` and
   `value=1635`. The handoff value is the plane variable, never a second host read
   (`:1400-1410` comment, `:2781` print) — so the two published numbers are one measurement.
   Pointer: capture.txt §A, §A3, §B, §B2.

2. [obs] **`coredump=` equals the sum of all kinds, exactly, at both captures.** 08:44:09Z:
   183 `dumped core` + 1365 `terminated abnormally without generating a coredump` + 69 JSON
   null MESSAGE + 4 other = 1621. 08:48:49Z: 183 + 1379 + 69 + 4 = 1635. It is *not*
   `dumped core` only (183 of 1621, 183 of 1635 in the default view). Pointer: capture.txt §A
   and §B "kind totals", §C table.

3. [obs] **Drift over 4 min 40 s: all +14 landed in the non-core class; `dumped core` did
   not move.** `dumped-core` 183→183, `json-null` 69→69, `other` 4→4,
   `no-coredump-abnormal` 1365→1379, `err_n` 1777→1793, kernel 155→157. So the census number
   tracks crash reports, most of which explicitly state no core was generated. Pointer:
   capture.txt §C drift table.

4. [obs] **The 69 "JSON null" entries are not a crash class; they are `journalctl`'s default
   JSON truncation of `dumped core` records.** Default `-o json` redacts fields:
   `src/shared/logs-show.c:43` `#define JSON_THRESHOLD 4096U`, `:1124` emits JSON null when
   `strlen(name)+1+size >= JSON_THRESHOLD` and OUTPUT_SHOW_ALL is unset, and `:1219` sets the
   data threshold to 4096 without `-a`. On the same boot at 08:50:22Z with `-a`, the same
   1635 entries classify as 252 `dumped core` + 1379 `terminated abnormally…` + 4 other,
   with 0 nulls; exactly 69 of those 252 messages are ≥4089 chars (= 4096 − len("MESSAGE") −
   1), exactly the 69 nulls; the longest default-view `dumped core` message is 3692 chars.
   `COREDUMP_PROC_MAPS` is null for 1620 of 1635 default-view entries and 4 with `-a`, the
   same effect. Pointer: capture.txt §B2, §C; sources in §D.

5. [obs] **The 4 "other" entries are coredump-handler errors, not coredump records.** They
   carry `CODE_FUNC=coredump_receive`, `CODE_LINE=100`, PRIORITY=3, ERRNO, no MESSAGE_ID,
   a 44-char MESSAGE and no COREDUMP_* metadata; v262
   `src/coredump/coredump-receive.c:100` is
   `return log_error_errno(r, "Failed to initialize pidref: %m");`. They inflate the census
   class by 4: `coredump=` minus `coredumpctl`'s boot-window length is 4 at both captures
   (1621−1617, 1635−1631). Pointer: capture.txt §A, §B "kind x MESSAGE_ID", §C.

6. [obs] **One counted entry is one crash-report journal record, one per crash.** All 1617
   (round 1) / 1631 (round 2) records carry MESSAGE_ID `fc2e22bc6ee647b6b90729ab34a250b1` and
   `CODE_FUNC=coredump_submit`, `CODE_LINE=793` (the `sd_journal_sendv` at
   `coredump-submit.c:793`); distinct `(COREDUMP_PID, COREDUMP_TIMESTAMP)` keys numbered
   1617 for the 1617 records at round 1 (the only repeated key group was the 4 `?@?` handler
   errors). The message is built at `coredump-submit.c:709-711` as
   `"Process <pid> (<comm>) of user <uid> %s"` with
   `written ? "dumped core." : "terminated abnormally without generating a coredump."`, and
   installed as `MESSAGE=` at `:727`. The class therefore deliberately mixes both outcomes,
   and one entry per crash means the count is a crash-report count. Pointer: capture.txt §A,
   §B, §D.

7. [obs] **MESSAGE is one string with embedded newlines (stack trace included), so
   first-line classification is the only stable split.** MESSAGE field shape: 1552 string /
   69 null at round 1; lengths: `dumped core` 497–3692 chars default, `terminated
   abnormally…` 90–99, handler error 44. No MESSAGE array shapes occurred. Pointer:
   capture.txt §A "MESSAGE field shape" and §C.

8. [obs] **`coredumpctl` does not accept `-b` in systemd 262, and its list is a
   crash-record list, not a core-file list.** The assigned
   `coredumpctl list -b --json=short --no-pager` exits 1 with
   `coredumpctl: unrecognized option '-b'` (stdout empty; it is an argv error, not a
   permission error). Correct form `coredumpctl list --no-pager --json=short` at 08:44:32Z
   gave 1755 records all boots; the boot-0 epoch window (`--since @1792655741`) gave 1617 at
   08:45:32Z and 1631 at 08:48:49Z — exactly the crash-record counts, not the census totals.
   Every boot-window record has `"corefile":"none"` and `size` null; 0 of those 1617/1631
   values names an existing file; `/var/lib/systemd/coredump` holds 2 stale files dated
   2026-10-20 (names not printed). Why: the host pipes `core_pattern` to systemd-coredump but
   `/etc/systemd/coredump.conf.d/storage.conf` sets `Storage=none`, so no core is stored
   from this boot at all. Pointer: capture.txt §A2, §B(3), §C, §D.

9. [obs] **The default JSON view is order-unstable across runs.** Two `-a` streams of the
   same 1793 entries, 37 s apart and 129,994,747 bytes each, differ in 118,636,290 bytes from
   byte 4: field order is permuted per run. Raw-output digests are therefore not an identity;
   field-level counts are unaffected. Pointer: capture.txt §D2.

10. [inf] **Wording for the C2 note.** "`coredump=` counts boot-0 journal entries whose
    SYSLOG_IDENTIFIER is systemd-coredump: one crash-report record per crash (MESSAGE_ID
    fc2e22bc…), either `dumped core` or `terminated abnormally without generating a
    coredump`, plus handler errors; it is a crash-report count, not a coredump count, and
    with `Storage=none` it is unrelated to stored core files." This explains this lane's own
    counting unit and classifies nothing by crash signal or cause (mori OUT-005).

## Sources (external claims) and rechecks

- `source: https://raw.githubusercontent.com/systemd/systemd/v262/src/coredump/coredump-submit.c`
  (34,408 bytes, sha256 `54ce12400ce7e7c5ec4f8a6acdeac58659780434ed964f9c941f82ec11d0e538`),
  lines 709-711, 727, 793; `verified-at: 2026-10-23T08:45Z`; `recheck: on-release`.
- `source: https://raw.githubusercontent.com/systemd/systemd/v262/src/coredump/coredump-receive.c`
  (6,354 bytes, sha256 `48caa3734626c2e44a03caf29234c7e712b2bb16a7d1dd3eec57d0e58bdc1f64`),
  line 100; `verified-at: 2026-10-23T08:45Z`; `recheck: on-release`.
- `source: https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/logs-show.c`
  (87,278 bytes, sha256 `abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f`),
  lines 43, 1124, 1219; `verified-at: 2026-10-23T08:45Z`; `recheck: on-release`.
- `source: local effective configuration` `/proc/sys/kernel/core_pattern` and
  `/etc/systemd/coredump.conf.d/storage.conf` (`Storage=none`), `limit.conf`
  (`MaxUse=512M KeepFree=8G`); `verified-at: 2026-10-23T08:46Z`; `recheck: on-change`.
- Registry: `corpus/SOURCES.md` has 0 rows matching `coredump-submit`, `coredump-receive` or
  `logs-show`; S177 is systemd v262 `man/systemd-coredump.xml` (same project/tag, different
  URL and bytes). These sources duplicate no registered row.
- Installed versions were confirmed before choosing the tag: `journalctl --version` and
  `coredumpctl --version` both `systemd 262 (262-1-arch)`.

## Limits

- [unk] Whether a `dumped core` record always implies the kernel delivered a core payload to
  the handler is not measured here; the source sets the message from its own `written` flag,
  which this seat did not trace. Bounded sweep: the three source files above, the journal's
  per-kind field presence, and `coredumpctl`'s `corefile` field (all `none`).
- [obs] Counts are live snapshots of a crash storm: re-run, never quote as current. The
  +14 drift in 4 min 40 s is the measured rate for this window, not a rate claim.
- [unk] Permission: `coredumpctl` read as user `vgpnk` (groups vgpnk,docker,input,wheel)
  without an error, so no permission denial was observed; the `-b` failure is argv-only.
- I classified nothing by signal or crash cause (mori owns that), and printed no crash
  details; the raw JSON streams stay in scratch and are not committed.

Scope: read=tools/tsukuroi-census.sh (journal arm and ADJ-04 handoff), corpus/QUALITY.md, round-34 declaration from commit 6de666c, corpus/SOURCES.md S177 row, live host journal/coredumpctl/coredump config, systemd v262 coredump-submit.c/coredump-receive.c/logs-show.c/coredump.c; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecCoredumpReconcile/capture.txt, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecCoredumpReconcile.md, scratch under /fast/scratch/hyaku/tsukuroi-r34/ExecCoredumpReconcile/; executed=journalctl (list-boots, -b -p err -o json, with and without -a), coredumpctl list (assigned -b form, plain, --since/--until @epoch), bash tools/tsukuroi-census.sh twice, jq/awk counting, stat/ls on /var/lib/systemd/coredump, curl of four systemd v262 source files
Model: opencode-go/deepseek-v4.1-flash
Installs: none
