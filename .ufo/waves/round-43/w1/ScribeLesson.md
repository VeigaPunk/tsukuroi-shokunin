VERDICT: draft

# ScribeLesson — F-3: draft of `corpus/lessons/round-43.md` § `## Mistakes` and § `## Routed defects (round-42 spot-check)`

Lane tsukuroi, round 43, wave w1, leaf seat. Drafted 2026-10-26 against base
`6951ead90566b2d74f7c45b4efca29246badad64` and implementation `717b716a8943151ace8657e0ca23d7d9b8434f26`. Nothing here
was written into the lane; the two sections below are exact Markdown for the L1 to append to
`corpus/lessons/round-43.md`. Style and column set follow `corpus/lessons/round-42.md` (`| ID | Class | Evidence |
Captured-by | Fix (and how it is shown able to fail) |`; routed defects as a numbered list of bold ids).

Mining brief: four rows come from the round-42 closure `corpus/lessons/round-42-verifier-spotcheck.md` — §1 Notes N1,
N2, N3 and §6 item 2 — none of which round 42's own lesson carries (its twelve rows are
`R42-OBSERVED-CHANNEL, ADOPTED-UNREAD, HERESTRING-TEMPFILE, SUP-UNCOVERED, VERDICT-MENTION,
C1-SELFTEST-UNMEASURED, C1-P6-NOT-NEUTRAL, BATTERY-SUMMARY-COLLISION, FREEZE-CENSUS-LIVE-PATH,
C1-SCRATCH-FALLBACK-TMP, COUNTER-SIGINT-LEAK, C1-CLASS-UNSWEPT`). The fifth row is this seat's own measurement of a
round-42 lesson row, with the red-before command run at the base.

## Draft — exact Markdown for `corpus/lessons/round-43.md`

```markdown
## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R43-SIB-PIN-UNREPORTED | scope | Round 42's incidents section names mori's moved pin (`.ufo/reports/round-42/tsukuroi.md:135`) and no tameshi pin: `grep -c tameshi` on that report prints 0, while `w2/AdjMoriPin.md` §3 found the live `tameshi-shokunin/corpus/knowledge/service-optin-protocol.md:153` pin (census `915-970`, now `921-976`) moved by the same round — one of three sibling pins missing while the section read complete (`round-42-verifier-spotcheck.md` §1 N1) | QUALITY 69 (a sibling pointer is replayed by quote and pinned blob and recorded `RESOLVES`/`DRIFTED`; a moved sibling pin is not absorbed silently) | The report carries a pin sweep: every sibling `path:line` this round's diff moved, its base and tip line numbers, and a `RESOLVES`/`DRIFTED` class. Able to fail: `grep -c 'service-optin-protocol.md:153' .ufo/reports/round-42/tsukuroi.md` → 0 (red); the same command against the report this round lands must print ≥ 1 |
| R43-MORI-ARITH | number-drift | The mori handoff states two deltas for one pin without naming their referents: §2 "Net +6 … (base: 1097-1112)" and "only the coordinate is stale (+3)", and §3 item 1 "stale by +3". Measured: the census content is at `tools/tsukuroi-census.sh:1097` at `c8efaa3f` and `:1103` at `6951ead9` (+6), while mori's live pin prints `1100-1115` (`mori-shokunin/PROVINCE.md:287`), already 3 high against the base content (+3). Each delta is true against its own starting line only, and cross-applying either lands 3 off — the closure read this as a self-contradiction (N2) | QUALITY 21 (a reader line number needs its snapshot) | One sentence per coordinate, with its starting line named: "content `1097-1112` at `c8efaa3f` → `1103-1118` at `6951ead9` (+6); the printed pin `1100-1115` is 3 high against the base content and 3 low at the tip". Able to fail: `test $((1097+3)) -eq 1103` and `test $((1100+6)) -eq 1103` both exit 1, while `test $((1100+3)) -eq 1103` and `test $((1097+6)) -eq 1103` exit 0 — the same `+3` is false and true depending on the unstated referent |
| R43-VERDICT-JSON-UNBOUND | vacuous | The wave-2 binding read a plain first line, so an output that is a JSON object bound nothing unless it carried `verdict_line`: `C2RevSC1` and `C2RevSC4` each carried `"verdict": "holds"` (`jq -r '.results[]\|select(.name=="C2RevSC1")\|.output' w2-results.json`, line 5; `round-42-verifier-spotcheck.md` §1 N3), and `declared_line('{"verdict": "holds"}')` returns `None` | QUALITY 90 (an anchored declared line, a mention counts for nothing) named no accepted serialization, so a JSON-only output fell outside both of its clauses | The seat prompt names one asserted form, `ROW SR<n> VERDICT: <holds\|partly\|fails>`, carried as the JSON `verdict_line` field or the output's first non-blank line, with the committed report's first line identical; only that form binds, and a record carrying both `verdict_line` and `verdict` binds `verdict_line` and ignores the other field. Able to fail: the N3 form binds nothing (`declared_line` → `None`, the anchored `re.fullmatch` false) while `{"verdict_line": "ROW SR3 VERDICT: holds"}` binds; a seat emitting only `verdict` leaves `verdicts_ok` one short (controls K6 and K13: `verdicts_ok 2` of 3) and the predicate FAILs |
| R43-CAP-HEADER-DUP | landing | The round-42 capabilities table repeats its header row: `SCORECARD.md:2630` and `:2632` both read `\| Capability \| What it can now do \| Evidence pointer \| First-working round \|`, so the second renders as a data row. Heading-bounded count: 2 for round 42, 1 for round 41 (`round-42-verifier-spotcheck.md` §6 item 2) | none — no criterion reads a rendered table | The round-43 append-only table carries one header row. Able to fail: the heading-bounded `awk` that prints 2 for round 42 (red) must print 1 for round 43; at draft time the section does not exist (`grep -c` → 0), so this round owes the fixed table rather than a repair |
| R43-CENSUS-PROBE-COORDS | reference-drift | `R42-C1-CLASS-UNSWEPT` names single-line probes at `:931, :969, :1051, :1426, :1501`; all five are `$CAP_OUT`-piped-`head -n1` readers only at `44766208`. At `6951ead9` they sit at `:934, :972, :1054, :1429, :1504`, and the five named lines hold `done)`, a blank, `smi_rc=$CAP_RC`, `if have "$SYSTEMCTL"`, `ts=${#timers[@]}`. The proposition (five readers survive) is true; the coordinates are not | QUALITY 21 | Cite the readers by content (`$CAP_OUT` piped into `head -n1`) plus the measured revision, and re-resolve the five coordinates each round. Able to fail: `sed -n '931p;969p;1051p;1426p;1501p' tools/tsukuroi-census.sh \| grep -c 'head -n1'` → 0 (red) while `grep -n 'head -n1' tools/tsukuroi-census.sh` returns `:934, :972, :1054, :1429, :1504` |

## Routed defects (round-42 spot-check)

1. **R42-C2-REGROUND — text re-grounded, counted reads pending.** C2 lands `corpus/knowledge/btrfs-scrub-record-r43.md`
   (131 lines; `## SR1` :17, `## SR3` :45, `## SR6` :80) on S237, S240 and S241, and the round-42 entry now opens with
   its supersession pointer at :4, inside the first 20 lines, which the frozen counter reads as `pointer_ok`. At
   `717b716` `python3 tools/check-scrub-record-r43.py --revision 717b716a…` returns `rows 3, quotes_ok 3, props_ok 3,
   host_ok 3, sources_ok 1, verdicts_ok 0, novelty_base_hits 0, pointer_ok 1`, FAIL exit 1: the only unmet conjunct is
   the counted verdicts, which bind wave-2 seats `C2RevSR<n>`/`C2CritSR<n>` (`check-scrub-record-r43.py:27,283-284`),
   and `w2-dispatch.json` does not exist yet. Until wave 2 binds them the entry is not a verified C2 outcome.
2. **R42-CAP-HEADER-DUP — not done; owed to this round's append-only table.** No round-43 capabilities section exists
   at draft time (`grep -c 'Capabilities — current full evidence set (round 43)' SCORECARD.md` → 0; `SCORECARD.md` ends
   at the declaration, :2684), and the duplication still stands at :2630/:2632. The round-43 table must carry one
   header, shown by the same heading-bounded `awk` returning 1.
3. **R42-ADJ-TAMESHI-UNREPORTED — not done; owed to the report.** No wave-1 seat names the pin
   (`grep -rn tameshi .ufo/waves/round-43/w1/*.md` → nothing), and no lane report has landed
   (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-43/` holds other lanes, no `tsukuroi.md`). The handoff must name
   `tameshi-shokunin/corpus/knowledge/service-optin-protocol.md:153` (census `915-970` → `921-976`) and restate the
   mori coordinates with their referents named (row R43-MORI-ARITH).
4. **R42-C1-COUNTER-AMEND — arms a–e in place (d by code read), f–g open.** (a) production-identity legs: the frozen counter
   runs its namespace legs at the caller's uid/gid (`score-bootinputs-r43.py:84`, `setpriv --reuid/--regid`) with
   values drawn per run (`random.Random(os.urandom(16))`, :289), and both receipts read
   `identity ['1000','1000','1000'], identity_ok 1`; (b) frozen gate controls K3 uid-gated, K4 env-gated, K5
   name-gated, K6 `-maxdepth 0` and K10 missing-point pre-filter all FAIL, K8/K9 PASS, `should_fail_accepted 0`
   (`controls/battery-summary-c1.jsonl`), K7 mount-table-gated recorded open; (c) `--scratch` is required — the counter
   without it exits 2 ("the following arguments are required: --scratch", observed); (d) SIGINT/SIGTERM handlers are
   installed (`score-bootinputs-r43.py:247-251`) — read, not exercised by this seat; (e) the routed boot-chain
   fail-open is fixed: `inputs_newer_than` (:463) decides on find's output, `boot_inputs_newer` calls it with the same
   eight start points (:494), and the selftest goes 45 → 48 with `correct 8 → 16`, `selftest_r43 0 → 3`, FAIL → PASS
   (`before/c1-before.jsonl`, `after/c1-after-717b716.jsonl`). **Not done:** the `:743` lookup's selftest case and the
   single-line probe readers — `tools/tsukuroi-census.sh` is untouched this round (empty `git diff --numstat
   6951ead9 717b716a -- tools/tsukuroi-census.sh`), still 129 `check` lines (the round-42 closure's 129 → 132-case
   tally), and the five `$CAP_OUT`-piped-`head -n1`
   readers survive at :934, :972, :1054, :1429, :1504. Reason: C1's declared surface this round is
   `tools/boot-chain-audit.sh` only (declaration, causal separability).
5. **R42-VERDICT-FORM — done on the counter side; the prompt clause is unobserved.** One asserted form binds:
   `declared_line` (:157) takes the JSON `verdict_line` field when the output parses as an object, else the first
   non-blank line; `bound` (:178) requires `re.fullmatch(r'ROW (SR\d) VERDICT: (holds|partly|fails)')` for that row
   (:189) plus an identical first line in the committed report; seats are `C2RevSR<n>`/`C2CritSR<n>` with residual
   reviewer `C2ResSR<n>`. Controls K6 (mention-not-assertion) and K13 (`verdict_line` holds, report first line
   differs) both FAIL with `verdicts_ok 2` (`controls/battery-summary-c2.jsonl`). Red-before for the N3 form is row
   R43-VERDICT-JSON-UNBOUND. The wave-2 dispatch does not exist yet, so whether the prompt names the form to the
   counted seats cannot be checked here; the wave-1 `C2Draft*` tasks carry no verdict instruction by design.
```

## Evidence — red-before states run by this seat

All commands ran from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (read-only) and are transcribed to
`.ufo/waves/round-43/w1/ScribeLesson/receipt-lesson-commands.txt`.

| Row | Red-before command | Observed |
|---|---|---|
| R43-SIB-PIN-UNREPORTED | `grep -c 'tameshi' .ufo/reports/round-42/tsukuroi.md`; `grep -c 'service-optin-protocol.md:153'` same file | `0`; `0` — while :135 names the mori pin |
| R43-MORI-ARITH | `git show c8efaa3f:tools/tsukuroi-census.sh \| grep -n 'Round-7 addition, lane S7-2'` vs the same at `6951ead9`; `grep -n 1100-1115 mori-shokunin/PROVINCE.md`; the four `test $((…))` pairs | `1097`, `1103`; pin prints `1100-1115` at :287; `1097+3`→1, `1100+6`→1, `1100+3`→0, `1097+6`→0 |
| R43-VERDICT-JSON-UNBOUND | `declared_line('{"verdict": "holds"}')` imported from `tools/check-scrub-record-r43.py` | `None`; `{"verdict_line": "ROW SR3 VERDICT: holds"}` → `ROW SR3 VERDICT: holds`; both-fields record → `verdict_line` wins; mention-first-line → no fullmatch |
| R43-CAP-HEADER-DUP | heading-bounded `awk '/^\| Capability \|/{c++}'` per capabilities section | round 41 → `1`, round 42 → `2`, round 43 → section absent (`grep -c` → 0) |
| R43-CENSUS-PROBE-COORDS | `sed -n '931p;969p;1051p;1426p;1501p' tools/tsukuroi-census.sh \| grep -c 'head -n1'`; `grep -n 'head -n1' tools/tsukuroi-census.sh` | `0`; sites at `:934, :972, :1054, :1429, :1504`; at `44766208` the five named lines each match (five×`1`) |

Routed-defect state, measured at `717b716`:

| Defect | State | Evidence |
|---|---|---|
| 1 R42-C2-REGROUND | text landed, verdicts pending | counter JSON: `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, verdicts_ok 0, novelty_base_hits 0, pointer_ok 1`, FAIL exit 1; `w2-dispatch.json` absent |
| 2 R42-CAP-HEADER-DUP | not done | no round-43 capabilities section; round-42 dup at :2630/:2632 |
| 3 R42-ADJ-TAMESHI-UNREPORTED | not done | no `tameshi` in `w1/*.md`; no `tsukuroi.md` under `.ufo/reports/round-43/` |
| 4 R42-C1-COUNTER-AMEND | arms a–e in place (d by code read), f–g open | after receipt `identity_ok 1, correct 16, selftest_r43 3, PASS`; base `correct 8, selftest_r43 0, FAIL`; no-`--scratch` exit 2; census untouched, 129 `check` lines, five readers at :934…:1504 |
| 5 R42-VERDICT-FORM | counter side done | `declared_line` :157, `bound` :178, fullmatch :189; K6/K13 `verdicts_ok 2` → FAIL |

## Findings (not verdicts on others' claims)

- `tools/check-scrub-record-r43.py` binds `verdict_line` and ignores a contradicting `verdict` field in the same JSON
  object (measured: `{"verdict_line": "ROW SR3 VERDICT: holds", "verdict": "fails"}` → `ROW SR3 VERDICT: holds`). The
  declared form is one field by design, but a record carrying both is scored on the field the seat chose, not the one
  the orchestrator read. Recorded here because seat C2-7's brief targets exactly that shape.
- The round-42 C2 after receipt binds no verdicts for `C2RevSC1`/`C2RevSC4` (closure N3), and the round-43 counter
  rejects the `"verdict"` form — so a seat following the old habit contributes `verdicts_ok 0` and the predicate FAILs
  rather than silently passing.
- The routed counter-amendment's census half is untouched at `717b716`; the five readers `R42-C1-CLASS-UNSWEPT` named
  survive, so that row's subject is open while its coordinates are stale.

## Limits — what this seat did not do

- Did not write, edit or commit anything in the lane; no report, ledger, lesson or scorecard byte was changed.
- Did not re-run the C1 counter or the census selftest (receipts cited as committed evidence; the census selftest is
  ~25 s and out of this item's ask). Did not run the round-42 C1 counter.
- Did not exercise SIGINT against the C1 counter; arm (d) is a code read.
- Did not verify SR1/SR3/SR6 quotes against the frozen sources (other seats own that); no claim here rests on them
  beyond the counter's own conjuncts.
- The wave-2 dispatch and results do not exist at draft time, so defect 5's prompt clause and any counted outcome are
  unobserved by construction.
- `R42-CAP-HEADER-DUP` and `R42-ADJ-TAMESHI-UNREPORTED` are stated as owed work, not as fixes; no green state exists
  for either yet.

## Receipts

- `.ufo/waves/round-43/w1/ScribeLesson/receipt-lesson-commands.txt` — the five red-before command blocks with output.
- `.ufo/waves/round-43/w1/ScribeLesson/receipt-verdict-form.txt` — `declared_line` probe over all four forms.
- `.ufo/waves/round-43/w1/ScribeLesson/c2-at-717b716.json` — the C2 counter's JSON at the implementation commit.
- `.ufo/waves/round-43/w1/ScribeLesson/noscratch.err` — the no-`--scratch` refusal (exit 2).
