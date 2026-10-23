# W2RevC2Remnants — review of the ScribeC2Remnants coredump-note correction draft

Reviewed: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ScribeC2Remnants/C2-correction-block-draft.md`
against `corpus/knowledge/coredump-count-unit-r34.md` body lines 5, 11, 15, 42, 59, 72, 77 (read this session) and
`corpus/lessons/round-34-verifier-spotcheck.md` §5 item 8. Host: systemd 262 (262-1-arch), read-only.

**Verdict: the draft SATISFIES spot-check §5 item 8.** All three body remnants (lines 11, 15, 59) are corrected,
append-only, with sourced wording, and its replacement `recheck:` procedure reproduces the null/handler split:
I executed its four commands verbatim on this host; all four exited 0 (cmd1 1690 summaries / 81 `MESSAGE=null` /
1609 printed; cmd2 306 "dumped core" / 1384 "terminated abnormally…" / 0 null under `--all`; cmd3 1694 identifier
entries = 1690 summary-ID + 4 no-`MESSAGE_ID` + 0 other; cmd4 coredumpctl 1828 records = 1777 `none` + 50
`missing` + 1 `present`). Evidence: `.ufo/waves/round-35/w2/W2RevC2Remnants/recheck-rerun-output.txt` and
`recheck-draft.sh` (sha256 `c56b06ee57a49c12741793a1a61898c3e3dd16de648a56ba4d93165a7f77df41`).

## Findings

1. **[pass] Line-11 remnant corrected, append-only, sourced.** The draft withdraws "no lane entry said what one
   counted entry is" and cites `kill-oom-boundary-r33.md` and `journal-boot-plane.md:79-106`. Both pointers check
   out: kill-oom-boundary row 27 reads "boot-0 `-p err` entries with `SYSLOG_IDENTIFIER=systemd-coredump`"
   (grep hit, `corpus/knowledge/kill-oom-boundary-r33.md`), and journal-boot-plane.md:79-106 is "### 2.1 Entries
   vs lines, again" with err-entries vs raw-lines and the `systemd-coredump` class row (read this session). The
   draft's internal cross-refs are exact: body line 72 is the "One summary record per crash overstates S186"
   correction and body line 77 the prior-coverage bullet (numbered read of the note).

2. **[pass] Line-15 remnant corrected via the existing body-line-72 correction; inherited anchors are verbatim-true.**
   The draft restates the narrower reading (at most one summary per crash the handler processes to the relevant
   point) instead of re-anchoring inline — weaker but correct sourcing, since body line 72 carries the anchors and
   they verify in the pinned S186 bytes (`.ufo/waves/round-34/w1/SrcCoredumpCode/coredump-submit.c`, sha256
   `54ce1240…`, equal to the round-34 pin): 660-661 early `return r;`, 681-683
   `return log_error_errno(r, "Failed to drop privileges: %m");`, 704-720 summary build with the ternary at 711,
   793-806 `sd_journal_sendv` failure path (`:806` "Failed to log coredump"). [obs]

3. **[pass] Line-59 remnant corrected.** Body line 42 indeed paraphrases with citations (mori `PROVINCE.md:8-9,24`,
   `SKILL.md:31`) and contains no quotation, so "mori's scope is quoted" is wrong and the replacement "Mori's scope
   is referenced, not changed." is accurate. No new source needed; verifiable from the note's own text. [obs]

4. **[pass] Recheck replacement reproduces the null/handler split — executed, not just read.** All four commands
   run clean (rc=0 each, `bash -o pipefail` pipelines): default-JSON null vs printed `MESSAGE` under the summary
   `MESSAGE_ID` (81 null), `--all` wording split with 0 nulls, identifier-entry classes separating the 4 handler
   no-`MESSAGE_ID` records (stable across both runs, matching S189's handler-error class), and coredumpctl
   `corefile` states. The split arithmetic holds (1690 = 306 + 1384; 1694 = 1690 + 4 + 0). This is exactly what
   the old line-5 pipeline could not do; the draft's criticism of the old pipeline is accurate. [obs]

5. **[pass] Every option used exists in the installed 262 `--help` (checked against live help, read-only).**
   journalctl: `--boot[=ID]`, `--priority=RANGE`, `--no-pager`, `--output=json` (json in the mode list),
   `--output-fields=LIST` ("verbose/export/json modes"), `-a --all`, positional `MATCH…` FIELD=VALUE matches — all
   present. coredumpctl: `-q --quiet`, `--no-pager`, `--json=FORMAT (pretty, short, or off)`, `list` — all present.
   `--boot=0` verified to select the current boot: its first record's `_BOOT_ID` `6a7f4fdf…` equals list-boots
   index 0, i.e. the census's boot-0. `coredumpctl --json=short` emits one JSON array, so the draft's jq unwrap
   guard fires correctly (first_keys shows lowercase `corefile`, which the `.corefile // .COREFILE` fallback
   reads). [obs]

6. **[minor] The v262 source-anchor sentence maps 7 items onto 8 ranges.** All eight anchors resolve in the pinned
   bytes (`journalctl-v262.xml`, sha256 `d54bbede…`, byte-identical to both round-34 S188 pins — cmp confirmed):
   44-45 `FIELD=VALUE` verbatim, 284-285 `--boot`, 414-415 `--priority`, 492-497 `-o/--output=` + json term,
   585-593 json-mode paragraph including the 4096-null rule (591-593), 667-677 `--output-fields`, 765-770
   `-a --all`, 825 the `standard-options.xml` no-pager include. coredumpctl-v262.xml: 49 `list`, 92-104 `COREFILE`,
   175-179 the five standard-option includes; standard-options-v262.xml:84-90 defines `--json=short|pretty|off`.
   The draft lists items and ranges in two independent orders, so a one-to-one in-order reading lands one range
   off (the correct assignment gives "JSON output" both 492-497 and 585-593). Reword before landing. [obs]

7. **[minor] Process: unregistered new sources and missing sha256 statements.** The seat saved
   `journalctl-v262.xml` (duplicates registered S188 byte-for-byte — undisclosed), `coredumpctl-v262.xml`
   (sha256 `116d48dc…`, 501 lines) and `standard-options-v262.xml` (sha256 `6d2d5566…`, 164 lines). No SOURCES.md
   row covers coredumpctl(1) or standard-options.xml (S001-S190 checked; S191-S196 are reserved for pacman rows),
   and the draft gives no sha256 for any of the three files despite the lane rule (save fetched bytes + give
   their sha256, disclose duplicates). The block cites coredumpctl(1) lines as evidence, so those rows should be
   registered when the block lands. [obs]

8. **[minor] The replacement silently drops the old procedure's `systemd-analyze cat-config systemd/coredump.conf`
   tail.** That call re-verifies the effective `Storage=none` on which the note's dumped-vs-stored reading depends;
   the four new checks observe journal/coredumpctl state only and would not catch a coredump.conf drift. Keep the
   cat-config call in the replacement. [inf]

9. **[minor/residual] Recheck step 4 is not boot-0-scoped and cannot be in 262.** coredumpctl's `--help` has no
   boot selector (`-S/--since`, `-U/--until`, `--file`, `-D/--directory`, `--root`, `--image` only), so step 4
   counts all recorded boots: 1828 records here vs 1694 boot-0 journal entries in step 3. The draft discloses this
   ("do not equate those totals") — honest — but the note's original corefile row was a boot-0 window
   (`coredumpctl records in the boot-0 window`); the recheck as written reproduces a different quantity and should
   say it replaces that row with an all-boots view (or bound it with `-S`/`-U`). [obs]

10. **[nit] jq guard fails on an empty coredumpctl list.** With zero records, `.[0] | keys` errors ("null has no
    keys"). Irrelevant on this host (1828 records); worth `select(length > 0)` if reused. [inf]

11. **[obs] The draft's own exit-code honesty is vindicated.** It reported two rcs as inferred; my rerun echoes
    rc=0 for all four commands (transcript in the seat dir). Its counts differ from mine only by normal journal
    drift (+1 summary entry, +1 coredumpctl record between the two runs), which supports its "re-run, never quote
    as current" framing.

12. **[pass] The installed man page agrees with the draft's COREFILE state list.** `coredumpctl(1)` (man8 systemd
    262-1) defines exactly `-`, `none`, `present`, `journal`, `truncated`, `error`, `missing` for the `COREFILE`
    column, matching the draft's claim about the v262 manual. [obs]

## Residual risk

- The counts are live-journal snapshots that drift by design; the draft inherits the note's dated-snapshot
  discipline and adds no new external claims beyond the v262 man-page anchors.
- I verified `journalctl-v262.xml` byte-identity with the round-34 S188 pins but did not re-download upstream
  bytes; `coredumpctl-v262.xml` and `standard-options-v262.xml` were not independently re-fetched — their anchor
  contents were instead corroborated against the installed 262 `--help` and man page (finding 5, 12). [inf]
- The line-15 correction rests on body line 72's S186 anchors (verified) rather than restating them; if body line
  72 is ever edited, the new block's wording loses its anchor.

## Verification gaps

- S177 (`systemd-coredump(5)`) and S186's `coredump-context.c`/`sd-messages.h` anchors were taken from the
  round-34 pins (sha `54ce1240…` matches the spot-check's recorded pin); no independent re-download.
- I did not audit the draft's placement/applicability beyond item 8 (e.g. whether the L1's landing flow will also
  register the two new source rows — finding 7 is routed, not resolved here).

Scope: read=C2-correction-block-draft.md; coredump-count-unit-r34.md (lines 1-20, 40-45, 55-60, 70-79); round-34-verifier-spotcheck.md; journal-boot-plane.md:79-106; kill-oom-boundary-r33.md (grep); SOURCES.md (grep rows S023-S190); pinned journalctl-v262.xml (sha d54bbede…), coredumpctl-v262.xml, standard-options-v262.xml, coredump-submit.c (sha 54ce1240…); installed journalctl/coredumpctl --help, --version, man pages; wrote=.ufo/waves/round-35/w2/W2RevC2Remnants.md, .ufo/waves/round-35/w2/W2RevC2Remnants/recheck-draft.sh, .ufo/waves/round-35/w2/W2RevC2Remnants/recheck-rerun-output.txt, /fast/scratch/hyaku/tsukuroi-r35/W2RevC2Remnants/recheck-draft.sh; executed=timeout 900 bash recheck-draft.sh (4 draft commands verbatim + boot-equivalence, json-shape and output-fields probes, all rc=0); sha256sum; grep -n; sed -n; cmp; pacman -Q systemd (read-only)
Model: not exposed
Installs: none
