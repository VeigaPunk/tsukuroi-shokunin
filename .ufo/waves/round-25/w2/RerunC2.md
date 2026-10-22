# Round 25 wave 2 — RerunC2: C2 memory-pressure measurement

Verdict: partly holds. The reruns and receipts reproduce exactly and the six quotes are real, but the before-value 0 is a non-evaluation sentinel, and the PASS counts evidence links rather than sourced learning.

The before-value 0 is true only as an absence fact: no entry, checker, capture or source rows exist at the base. The receipt is exit 2 (CANNOT_EVALUATE), and the 0 is a literal in the error path. The checker's PASS also accepts an unrelated source, an invented or missing entry quote, or a one-word prose token, and a defective duplicate row still yields PASS.

## 1. Reruns match the receipts [obs]

- `cmp` returned SAME for `measure/c2-b9046016.json`, `measure/c2-5e7c04ec.json` and `measure/c2-selftest.txt` against my fresh runs in `w2/RerunC2/run-*.out`.
- `--revision b9046016831237cd04d38da11ba76e50d5380c53`: exit 2, status CANNOT_EVALUATE, verified_rows 0, finding CAPTURE-MISSING at `.ufo/waves/round-25/capture/capture.txt`.
- `--revision 5e7c04ecb02735491456de2b8bc44550d0db4609`: exit 0, status PASS, verified_rows 6, no findings. The observed capture digest e60f1bbc…447136 equals the pinned digest.
- `--selftest`: exit 0, cases 32, failed 0.
- `--revision 6c580b155840c8750a7bb5f14dcb8e48913d0073`: exit 2, status CANNOT_EVALUATE, verified_rows 0, finding ENTRY-MISSING at `corpus/knowledge/memory-pressure-r25.json`. This matches the expectation.
- The working-tree checker is byte-identical to the committed blob at 5e7c04ec (sha256 077bd484…), so the measured tool is the committed one.

## 2. Mutation results (in memory, no lane write) [obs]

I called the checker's own `evaluate()` on the 5e7c04ec bytes with one change at a time. Scripts: `w2/RerunC2/harness.py` and `harness2.py`; output: `harness.out` and `harness2.out`.

## 3. Findings, most material first

1. **Medium-high: the PASS counts evidence links, not sourced learning.** [obs, reproduced by mutation]
   - Mutation M8: row MP6 (oom_kill counters) cites only S123 (systemd `oomd-manager.c`, mode `auto`). Result: exit 0, PASS, verified_rows 6. The only finding is MP-QUOTE-SOURCE-UNKNOWN, which is non-blocking.
   - Mutation M9: row MP6 cites only S120 (systemd `oomd.conf` defaults). Result: exit 0, PASS, 6.
   - Mutation M1: MP1's first entry quote is replaced by an invented sentence, "The kernel chooses one victim process when pressure exceeds ninety percent." Result: exit 0, PASS, 6. The only finding is MP-QUOTE-MISMATCH, non-blocking.
   - Mutation M2: MP1's entry `quotes` list is emptied. Result: exit 0, PASS, 6.
   - Mutation M7: the three S115 table quote rows are deleted from the lesson (see finding 3). Result: exit 0, PASS, 6.
   - Cause: rule R2 (sources) and rule R3 (a Gate quote for one of the row's sources), as written in `tools/check-memory-pressure.py:4-18`, check the registry row and the lesson's Gate, not whether the source matches the row. The checks that compare the entry's quotes with the Gate are declared non-blocking at `:599-600` and `:603-605`, so the entry's `quotes` field does not affect the count.
   - Current effect: none on the 6. I verified all 17 entry quotes against their own fetched source (finding 5). The defect is that "verified" in SCORECARD.md:793 and the claim text overstate what is checked. Accurate wording is "6 rows whose registry, lesson and pointer links resolve".

2. **Medium: a defective duplicate row leaves the status at PASS.** [obs, reproduced]
   - Mutation M5: a second MP2 row is appended with empty statement, verdict and action, and with no sources, pointers or quotes. Result: exit 0, status PASS, verified_rows 6. The same output lists blocking findings for that row: MP-ROW-ID-DUPLICATE, MP-ACTION-EMPTY, MP-VERDICT-EMPTY, MP-STATEMENT-EMPTY, MP-SOURCES-EMPTY, MP-CAPTURE-POINTER-MISSING and MP-QUOTE-MISSING.
   - Cause: a duplicate id is flagged at `tools/check-memory-pressure.py:536-537`, but only an unknown or missing id set sets `global_blocked` (`:666-668`). The exit is `0 if verified_rows == 6` (`:670-672`), so the extra row's blocking findings never reach the exit code.
   - The selftest has no duplicate-row case (its cases run from line 842 to line 943).

3. **Medium: rule R3 can be met by a one-word prose token.** [obs, reproduced]
   - Line 9 of the lesson Gate section reads "Admitted rows (all `mined`, opened 2026-10-22, …): S115 to S124 …" (`corpus/lessons/round-25.md:9` at 5e7c04ec). The parser at `tools/check-memory-pressure.py:338-346` treats any non-table Gate line with an S-id and a backtick span as a located quote, so S115 gains the one-word quote "mined".
   - Mutation M7: with the real S115 quote rows deleted, MP1 still verifies (exit 0, PASS, 6).
   - Current effect: none on the count. MP1 and MP2 also cite real S115 and S116 quotes, and no other row relies on this token.

4. **Medium (the before-value): 0 at the claim base is a sentinel, not a measured zero.** [obs, with inference]
   - The declaration says "0 verified rows (entry and checker absent)" (SCORECARD.md:793). The absence part is true at b9046016. `git cat-file -e` exits 128 for `corpus/knowledge/memory-pressure-r25.json`, `corpus/knowledge/memory-pressure-r25.md`, `corpus/lessons/round-25.md`, `tools/check-memory-pressure.py` and `.ufo/waves/round-25/capture/capture.txt`. `corpus/SOURCES.md` at b9046016 has no S115–S125 row; its highest id is S114.
   - The receipt does not measure that absence. The checker reads the capture first (`:469-471`), so the base run stops at CAPTURE-MISSING before it looks at any entry. Every error path returns `'verified_rows': 0` as a literal (`:465-466` in `cannot()`, `:475-476` for CAPTURE-TAMPERED). A missing entry, a malformed entry and a missing capture therefore print the same 0.
   - Honest label: "not evaluable (exit 2, CAPTURE-MISSING at the base); zero rows exist", with the delta read as "not evaluable to 6". No ordinal moves.
   - [obs] The claim base b9046016 is authored by `protocol-shokunin` (`git log -1 --format=%an`). The lane's own later commits, 6c580b15, 0cd9b28 and 5e7c04e, are by `tsukuroi-shokunin`.

5. **Low-medium: one of ten registry pins is mistyped (S120); the checker never reads pins.** [obs, reproduced]
   - I fetched the ten raw URLs for S115–S124 with plain `curl` (HTTP 200 each), via `w2/RerunC2/fetch_pins.py`. The bytes are saved under `w2/RerunC2/src/`.
   - Nine registry `raw bytes sha256` pins match the fetched bytes exactly.
   - S120 does not. `corpus/SOURCES.md:126` at 5e7c04ec pins 36ae3e474a6e5632**d4a6**1ae9…926617. The fetched bytes hash to 36ae3e474a6e5632**a4d6**1ae9…926617. The two differ only at 1-based hex positions 17 and 19, which are swapped. `sha256sum` on the saved file confirms the second value.
   - The S120 quotes are present at the cited lines: "Defaults to 90%." at line 172, "Defaults to 60%." at line 190 and "Defaults to 30 seconds when unset or 0." at line 202 of `w2/RerunC2/src/S120.raw`. So the content is right and the pin is a transposition typo [inf]. The checker has no source-digest check.

6. **Low: MP1 relies on a source its row does not list.** [obs]
   - MP1's statement says the systemd-oomd limit is "documented as the share of time in a 10 second window" and cites "oomd.conf(5)" as an inference (labelled as such). Its `sources` list contains only S115.
   - The 10-second wording is in S120 (`w2/RerunC2/src/S120.raw` lines 95 and 183). Because S120 is not listed under MP1, the checker cannot see that link.

7. **Informational (inherent): statement truth is not checked.** [obs]
   - Mutation M3: MP5's statement is replaced by a false one ("systemd-oomd kills a unit at 99 percent memory pressure over 5 seconds by default."). Result: exit 0, PASS, 6. The checker's scope note (`:34-36`) says it counts links only. The MP5 statement as written matches the sources: 60 percent and 30 seconds at S120 lines 190 and 202, and the compiled-in constants at S124 lines 26–27.

8. **Informational: the selftest cannot see these defects.** [obs]
   - The 32 selftest cases cover quote length, pointer shape, capture tampering, missing inputs and an unknown row id. None covers a duplicate row (finding 2), an entry quote that differs from the Gate or is missing (finding 1), a source unrelated to the row (finding 1) or a non-quote token (finding 3). A PASS from `--selftest` says nothing about these.

## 4. What holds [obs]

- The reruns and the 6c580b15 run reproduce the receipts (section 1).
- The capture digest matches the pin. The capture lines cited by the entry say what the entry says: `capture.txt:73` is `inactive` for `systemd-oomd.service` (exit 3); `:106-108` are the commented compile-time defaults `#SwapUsedLimit=90%`, `#DefaultMemoryPressureLimit=60%` and `#DefaultMemoryPressureDurationSec=30s`; `:14-15` hold the totals behind the MP2 ratio, 40856373 / 41385384 = 0.987, which is correct.
- All 17 entry quotes are present in their own fetched source. All Gate quotes for S115–S124 are present in their fetched source, except "mined" (finding 3). Output: `w2/RerunC2/quotes_check.out`.

## 5. Residual risk and verification gaps

- I spot-checked the six rows rather than re-deriving every statement. MP2 arithmetic and the MP4 and MP6 statements were not re-derived from the capture beyond the pointers.
- S125 (mori sibling) was checked by grep only. The wording "records what those files are, exactly which shapes the kernel emits" appears at mori `corpus/knowledge/system-pressure-r24.md:46` at 4f05dd5a; the opening words are probably on line 45, which I did not open. No row cites S125, so the count is unaffected.
- The source tags v7.2 and v262 were fetched today. Byte equality is evidence for those tags only.
- I did not run the C1 checker or the census; they belong to other seats.

## 6. Suggested handling for the L1 (no edit made here)

- Record C2's before-value as "not evaluable (exit 2); zero rows exist", not as a measured 0.
- Describe the six rows as "6 linked rows" until the checker blocks on entry-quote mismatch, rejects non-quote tokens, checks that each row's quote source is in its row's source list, and flags any duplicate row id as blocking.
- Correct the S120 pin at `corpus/SOURCES.md:126` to the fetched digest after a fresh fetch.

Scope: read=SCORECARD.md (round-25 sections at :784-813 and :815-861), tools/check-memory-pressure.py, tools/_revision.py (hash only), measure/c2-*.json and c2-selftest.txt, capture/capture.txt, lane git objects at b9046016, 6c580b15 and 5e7c04ec (corpus entry, lesson, SOURCES.md, SKILL.md), mori-shokunin git object at 4f05dd5a, and public raw.githubusercontent.com files for S115–S124; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RerunC2.md and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RerunC2/ (run-*.out and .err, harness.py, harness.out, harness2.py, harness2.out, quotes_check.py, quotes_check.out, fetch_pins.py, src/S115.raw to S124.raw, lesson-5e7c04ec.md, sources-5e7c04ec.md); executed=python3 tools/check-memory-pressure.py with --revision b9046016831237cd04d38da11ba76e50d5380c53, --revision 5e7c04ecb02735491456de2b8bc44550d0db4609, --revision 6c580b155840c8750a7bb5f14dcb8e48913d0073 and --selftest; cmp; sha256sum; git cat-file, show, log, rev-list, rev-parse and merge-base (read-only); git -C mori-shokunin cat-file and show (read-only); curl -sSL for ten public raw.githubusercontent.com URLs; python3 harness, quote-check and entry-quote scripts run in memory without writing lane files

Model: not exposed

Installs: none
