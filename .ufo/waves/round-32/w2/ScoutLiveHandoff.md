# ScoutLiveHandoff — integrated census at b8bf1507, live host, and the mori side

Verdict: the census at the lane tip emits exactly the two declared HANDOFF lines on the live
host, every field is either a literal constant, an integer count, or a `journalctl --list-boots`
date bound (no process name, path, argv or unit name anywhere), the kill-events `window=` field
carries the oom plane's own window under the documented space-to-colon substitution, and mori's
committed HEAD contains no reader for such a line — nothing that would break, and nothing that
would consume it.

1. [obs] The census script extracted from the tip and run live on the host exits 1 (DEGRADED)
   in 3.20 s with empty stderr and prints 10 lines: header, six `PLANE` lines, two `HANDOFF`
   lines, rollup. Script: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/ScoutLiveHandoff/census.sh`
   sha256 `7daa2ccbbded3a931abdbd76cb8ad34ccbe596f6dabc3524c519cc123e44e7b5` (from
   `git show b8bf150722a2261c80ab2ce012de3690ba732eeb:tools/tsukuroi-census.sh`); output
   `.../ScoutLiveHandoff/census-live.out` sha256 `a8a90330f3c17d903f3789c49f27328136d7f41db034616d9b0ea4fd68ccd3b0`.
   Command: `bash census.sh > census-live.out 2> census-live.err`, exit 1, `census-live.err` 0 bytes.

2. [obs] The HANDOFF lines with every whitespace-delimited field, from
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/ScoutLiveHandoff/census-live.out:8-9`:
   - line 8: `HANDOFF ADJ-04 mori class=kill-events value=2 kind=dated-event state=prepared window=boots=6:2026-10-19..2026-10-22 source=journal-window`
     — fields: `[1]=HANDOFF [2]=ADJ-04 [3]=mori [4]=class=kill-events [5]=value=2
     [6]=kind=dated-event [7]=state=prepared [8]=window=boots=6:2026-10-19..2026-10-22
     [9]=source=journal-window`.
   - line 9: `HANDOFF ADJ-04 mori class=coredumps value=187 kind=dated-event state=prepared scope=boot0-merged selector=SYSLOG_IDENTIFIER`
     — fields: `[1]=HANDOFF [2]=ADJ-04 [3]=mori [4]=class=coredumps [5]=value=187
     [6]=kind=dated-event [7]=state=prepared [8]=scope=boot0-merged [9]=selector=SYSLOG_IDENTIFIER`.
   Both sit after the six PLANE lines and before the rollup, as the census header
   (`census.sh:51-73`) declares.

3. [obs] Window comparison: the PLANE oom line's window is `boots=6 2026-10-19..2026-10-22`
   (`census-live.out:7`) and the HANDOFF kill-events window is `boots=6:2026-10-19..2026-10-22`
   (`census-live.out:8`). The two are equal after the documented space-to-colon substitution
   (`census.sh:499-500` comment; code `census.sh:2778` `${OOM_WINDOW// /:}`): boot count `6`
   and both date bounds `2026-10-19..2026-10-22` are identical; only the separator differs.
   Checked programmatically: `normalized equal: True; boots equal: True; dates equal: True`.
   The window is built at `census.sh:1222` (`OOM_WINDOW="boots=$boots $win_first..$win_last"`)
   from `journalctl --list-boots --no-pager` fields `$4` and `$8` of integer-index lines
   (`census.sh:1210-1217`); live `--list-boots` rows show `[4]=2026-10-19 [8]=2026-10-19`,
   `[4]=2026-10-19 [8]=2026-10-20` — dates, not the boot id (`$2`).

4. [obs] No process name, path, argv or unit name in either line, verified field-by-field
   against the emitting code: `value=` on the kill-events line is `OOM_CLUSTERS`, the integer
   minute-cluster count (`census.sh:1257`), printed at `census.sh:2776-2778`; `value=` on the
   coredumps line is `JRN_COREDUMPS`, the integer count of boot-0 err entries whose
   `"SYSLOG_IDENTIFIER":"systemd-coredump"` (`census.sh:1402-1410`), printed at
   `census.sh:2780-2782` — the string `systemd-coredump` never appears in the line, only the
   selector field name `SYSLOG_IDENTIFIER`; `window=` is dates only (finding 3); every other
   field is a literal constant. The only two `printf 'HANDOFF'` sites are `census.sh:2777` and
   `census.sh:2781` (grep), so no other emission path exists. The line carries no
   `systemd-coredump@…service` unit name, no `/…` path, no argv.

5. [obs] Count cross-checks on the live run: HANDOFF kill-events `value=2` equals the oom
   plane's `clusters=2` (`census-live.out:7`); HANDOFF coredumps `value=187` equals the journal
   plane's `coredump=187` (`census-live.out:5`). Recorded receipt
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/measure/after-4ac5ebaa/c1-declared.jsonl`
   has 24 scenario lines `{"routed": true}` and summary `{"predicate_label": "routed",
   "routed": 24, "scenarios": 24, "live_consistent": true, "harness_errors": 0,
   "seed": "6e66742619cc00ff"}` — consistent with what I observed live (non-vacuous: 2 dated
   clusters and 187 coredump entries).

6. [obs] Do-nothing control at the base, live: the base census
   (`git show 58cc2e0bfaa4580d47f6817537c8d5c82dbe9c92:tools/tsukuroi-census.sh`,
   `census-base.sh` sha256 `d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e`)
   exits 1 with **0** HANDOFF lines (`grep -c '^HANDOFF'` → 0;
   `census-base-live.out` sha256 `60fc0cc5a9a0e69e52f37f0754f219897eb510591f3aab172332391e8b42ff3c`).
   Diff of base vs tip output with the HANDOFF lines removed: the only difference is the
   `PLANE drivers` line, whose live counters drifted between the two back-to-back runs
   (C5_pswp 7418067→7417997, C6_psi_full_total_us 632606890→632587874, C6_avail_kb
   19936648→20566428, C6_shmem_kb 129680→106836); the `PLANE oom` line, the `PLANE journal`
   line, the rollup line and the exit code are byte-identical (`diff` prints nothing for each;
   "oom lines identical", "journal lines identical", "rollup identical"). That is exactly the
   live comparison set of the frozen scorer (`tools/score-census-handoff-r32.py:748-751`: oom
   and journal PLANE lines, rollup, exit code), so the live conjunct is satisfied by
   construction on this host.

7. [obs] Mori's repo at HEAD contains nothing that would read such a line. The assigned
   command `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -i 'HANDOFF\|tsukuroi' HEAD`
   exits 0 with 7822 lines of matches, all prose or identifiers, none a parser. Targeted
   searches, each run separately with its own exit code, all rc=1 (no match):
   `'^HANDOFF'`, `'HANDOFF ADJ'`, `'HANDOFF' -- tools`, `'ADJ' -- tools`, `'class=kill-events'`,
   `'class=coredumps'`, `'kind=dated-event'`, `'state=prepared'`, `'window=boots='`,
   `'ADJ-04 mori'`. The 155 files matching case-insensitive `handoff` are wave notes, dispatch
   JSON, a `mori-interactive-round-handoff-v1` schema in `.ufo/round-2/`, `corpus/QUALITY.md:154`
   (criterion 51) and lesson prose — e.g. `HEAD:.ufo/waves/round-32/r1/AttackCopies.md:132`
   `## Bounds and handoff`, `HEAD:.ufo/waves/round-32/w1/SrcCurlMan.md:86` `## 7. Handoff for L1`;
   no reader. `tsukuroi-census` appears only as prose references (`HEAD:.ufo/waves/round-24/w1/ConnectSiblingPsi.md:43`,
   `HEAD:PROVINCE.md:287`); `tools/mori-census.sh` mentions tsukuroi only as the `owner=tsukuroi`
   routing string for non-fleet units (`HEAD:tools/mori-census.sh:1493,1495`), and
   `tools/mori-round13/14-regressions.py` only as expected `owner=tsukuroi` text.

8. [obs] The census header's citation resolves lane-locally, and the claim it grounds is true
   of mori's bytes: `git -C tsukuroi-shokunin ls-files .ufo/waves/round-32/w1/ConnSiblingOverlap.md`
   exits 0 (the file is in the tsukuroi lane; mori's round-32 tree holds `ConnectorSiblings.md`,
   not that name), and its line 33 says "mori counts by structured MESSAGE_ID per scope and
   never sums the scopes", citing mori's `tools/mori-census.sh:954-955`; mori's
   `tools/mori-census.sh:950-957` shows exactly those MESSAGE_ID queries
   (`coredump_notice MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 notice`) under a header that
   reads "never summed". So the census's own caveat that its `value=` is not comparable to
   mori's counts is grounded in mori's committed counting rule.

9. [inf] The line is prepared but unconsumed: mori's committed HEAD has no code path that
   reads `HANDOFF` lines, so `state=prepared` is honest — nothing on the receiving side reports,
   acknowledges or accepts it, matching mori `PROVINCE.md:71`, which still records only the
   older packet `TSUKUROI-F1-MEM-01` as `prepared`. A future mori reader would need to be
   written; nothing existing would break or misparse the line.

10. [unk] Whether mori's uncommitted working tree or a future mori round adds a reader (I read
    committed HEAD only, as assigned); whether any consumer outside mori (another lane, a
    report tool) parses the line (outside this seat's question). The only asymmetry found in
    the line itself is the documented `:`-for-space window separator (finding 3), which a
    naive cross-line string equality against the PLANE oom window would miss.

Artifacts under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/ScoutLiveHandoff/`:
`census.sh`, `census-live.out`, `census-live.err`, `census-base.sh`, `census-base-live.out`,
`tip-nohandoff.out`, `base-nohandoff.out`. Commands executed: `git show <rev>:tools/tsukuroi-census.sh`,
`bash census.sh` (tip, exit 1) and `bash census-base.sh` (base, exit 1) on the live host,
`diff`/`grep`/`python3 -c` over the captured outputs, `journalctl --list-boots --no-pager`,
and the read-only mori greps in finding 7. No lane file outside this seat was edited; no git or
jj write command ran anywhere; no counter was executed.

Scope: read=tsukuroi lane (census.sh at b8bf1507 and 58cc2e0b, after-4ac5ebaa receipt, w1/ConnSiblingOverlap.md, scorer live-conjunct lines), mori-shokunin HEAD (greps), live host journalctl --list-boots; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/ScoutLiveHandoff.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/ScoutLiveHandoff/{census.sh,census-live.out,census-live.err,census-base.sh,census-base-live.out,tip-nohandoff.out,base-nohandoff.out}; executed=git show, bash census.sh, bash census-base.sh, sha256sum, diff, grep, python3 -c, journalctl --list-boots --no-pager, git grep (read-only)
Model: charm-hyper/deepseek-v4.1-flash
Installs: none
