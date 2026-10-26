VERDICT: draft

# Seat MineStreak — item D-5 (mine mistakes): rows for the round-34..37 rejection streak

Scope: draft at most four `## Mistakes` rows (class · evidence pointer · captured-by · fix) for the four successive
`rejected-honest-stop` closures, using the C1 sections of `corpus/lessons/round-3{4,5,6,7}-verifier-spotcheck.md`,
`corpus/QUALITY.md`, the round-38 declaration and the round-38 control/before receipts. Read-only: no lane file was
edited, no counter, census, probe or gate was executed, no scratch dir was created, nothing installed. I did not
judge C1 or C2 and issue no closure verdict.

## 1. What the streak actually is (measured, from the four spot-checks)

| Round | C1 ground of rejection | Evidence |
|---|---|---|
| 34 | declared kill rule fired: two mutants that keep an ambient path read `leaking` 0 of 27, `harness_errors` [], exit 0 | `corpus/lessons/round-34-verifier-spotcheck.md:67`; `:143` not admitted |
| 35 | `W2TreeKeyed` and `W2LogKeyed` scored 24 of 24 under VERSION 2 **before the change existed** | `corpus/lessons/round-35-verifier-spotcheck.md:33`; `:26` NOT VERIFIED |
| 36 | declared after-value (0 on all five targets) falsified by the frozen counter — `score-census-handoff-r32.py:source` reads 1 | `corpus/lessons/round-36-verifier-spotcheck.md:38`, `:54`, `:112` |
| 37 | sensitivity conjunct undelivered (no V8 per-fix mutant); the kill evidence is a **V7** run | `corpus/lessons/round-37-verifier-spotcheck.md:39`, `:40`, `:115` |

Two classes carry all four verdicts: a should-fail variant reads **at** the frozen target (`survivor`), and the
counter's observation channel cannot see the mechanism it claims to measure (`vacuous`). Two more classes recurred
in the same four records without deciding a verdict: evidence attributed to an object it does not measure
(`attribution`) and round work not where the round says it is (`landing`). Four rows, one per class.

Why it recurred: each round minted a fresh, locally scoped id for the counter defect (`R34-COUNTER-READ-SIDE-GAPS`
at `corpus/lessons/round-34.md:59`, `R35-V1-QUALITY-73-82` and `R35-V2-FORCED-SHAPE-CONSTANTS` at
`corpus/lessons/round-35.md:43-44`, `R36-INVOCATION-GAP`/`R36-SOURCE-ENV-PARAM` at `corpus/lessons/round-36.md:116,118`,
and **no** round-37 row at all — its `## Mistakes` carries five ids, `corpus/lessons/round-37.md:34-36,102-103`,
none about the undelivered conjunct recorded at `:58`). No frozen id list carried the debt forward, although
QUALITY 76 exists for exactly that (`corpus/QUALITY.md:145`) and the lane used it in round 29
(`SCORECARD.md:1103`, `:1118`). Sweep for the absence: `grep -nE '^\|[[:space:]]*\*{0,2}O[0-9]{2}'
corpus/lessons/round-3[4-7]*.md | wc -l` → `0`.

## 2. Proposed text — `## Mistakes` (paste-ready)

Column order follows the lane's existing tables (`corpus/lessons/round-34.md:57`), which carry the four
CORPUS.md fields plus a stable id.

```markdown
## Mistakes — round-34..37 rejection streak (mined at round 38)

| ID | Class | Evidence pointer | Captured-by | Fix, and how round 38 shows it able to fail |
|---|---|---|---|---|
| R38-STREAK-SURVIVOR | survivor | A variant that skips the claimed work reads at the frozen target, and the round learns it after the claim: round 34 MutAttrgetterCopy and MutPathCopy read `leaking` 0 of 27 with `harness_errors` [] and exit 0 (`corpus/lessons/round-34-verifier-spotcheck.md:67`; `corpus/lessons/round-34.md:49`); round 35 W2TreeKeyed and W2LogKeyed read 24 of 24 under VERSION 2 before the change existed (`corpus/lessons/round-35-verifier-spotcheck.md:33`; `corpus/lessons/round-35.md:44`); round 36's declared after-value of 0 on all five does not hold — `tools/score-census-handoff-r32.py:source` reads 1 (`corpus/lessons/round-36-verifier-spotcheck.md:38`); round 37 commits no V8 per-fix mutant, so the declared sensitivity conjunct is unmet (`corpus/lessons/round-37-verifier-spotcheck.md:39`) | QUALITY 73 (`corpus/QUALITY.md:141`) and QUALITY 82 (`corpus/QUALITY.md:161`). Round 35 already minted this class as R35-V1-QUALITY-73-82 (`corpus/lessons/round-35.md:43`) and it recurred three times under new ids | The declaration's counting command is a committed should-fail battery whose last line carries `should_fail_accepted`, and every new counter adds a fixture-gated variant to it. Round 38 shows controls able to fail: `C2-plain-sort` 63/69 with `extra_rows 6`, `C2-no-override` 66/69 with `extra_rows 3`, `C2-no-source` 69/69 with `source_ok 0`, `C1-constant-emitter` 2/10, `C1-naive-emitter` 6/10 with `six_planes_all 0` — all FAIL, exit 1 (`.ufo/waves/round-38/controls/controls.jsonl:2,3,4,7,8`) — while `C2-correct` PASSes (`:5`). Not yet shown: the fixture-gated survivor still reads v1 PASS 10/10 (`controls-q82.jsonl:1`), and no round-38 counter has a `--selftest` or a `should_fail_accepted` field, so QUALITY 73's measure clause is not adopted |
| R38-STREAK-VACUOUS | vacuous | The counter's observation channel cannot see the mechanism, so a clean reading is true for an arm that reaches it by an unnamed or value-carried route: round 34's probe scans construct names, so `operator.attrgetter` and `os.get_exec_path` reads score 0 in an untraced run (`corpus/lessons/round-34.md:59`); round 36 carries vacuity S3, the `get_exec_path` silent channel S4 and the parameter-named-`env` source rule (`corpus/lessons/round-36-verifier-spotcheck.md:52`, `:102`); round 37's V-B2 kill evidence is a V7 run plus a source-set emulation, with no V8 dynamic-channel run (`corpus/lessons/round-37-verifier-spotcheck.md:40`) | `none` — no numbered criterion requires a view in which the scored mechanism's observation channel is exercised. QUALITY 82 (`corpus/QUALITY.md:161`) reaches only counters that build their own fixtures and QUALITY 80 (`:153`) only do-nothing controls; round 34's capturer is the declaration's own kill rule (`corpus/lessons/round-34.md:59`) | Score the arm in a view it cannot tell from production, with the expected answer drawn per run. Round 38 shows both directions: the fixture-gated arm reads v1 PASS 10/10 with `live_match 1` but `ns_views_matched 0`, `ns_available 1` under the production-path view (`.ufo/waves/round-38/controls/controls-q82.jsonl:1`); the cached-live arm reads 1/3 FAIL (`:2`); the real arm reads 3/3 PASS with a per-run `seed` (`:3`); at base the v1 live leg reads `live_match 0` (`.ufo/waves/round-38/before/c1-before.json:8`) |
| R38-STREAK-ATTRIBUTION | attribution | Evidence is attributed to a claim it does not measure: round 34 states "Gates at `a8b46ac8`, all exit 0" while no gate receipt names `a8b46ac8` (`corpus/lessons/round-34-verifier-spotcheck.md:33`); round 37 offers a V7 receipt (`probe_version 7`, sha `a2a5acac…`) as kill evidence for a V8 claim whose frozen sha is `9aee085b…` (`corpus/lessons/round-37-verifier-spotcheck.md:40`, `:128`); the same records mis-count their own rosters — "the other 12" lists 13, and the heading says "2 provider refusals" over three holds (`:191`, `:192`) | QUALITY 77 (`corpus/QUALITY.md:147`) | Every revision-cited result ships as a `tools/run-receipt.py` receipt whose header names `revision`, `tool`, `tool_sha256` and `tool_revision`; a receipt naming other bytes is not evidence for the claim, and a run under another version is re-run, never cited. Round 38 shows the binding in the declaration only: the declared digests equal the bytes (`sha256sum` → `e649bfb3…`, `a183ff58…`, `60e3635b…`, `cba1bec2…`, `5469e59a…`), but `before/c1-before.json:2-5` and `before/c2-before.json:2-5` carry counter, revision, `branch_tip` and predicate with no `tool_sha256`, and `controls.jsonl` score objects carry no revision because the runner projects a key subset (`run-controls.sh:27-28`). No round-38 control can fail on a mis-bound receipt — debt, not a demonstrated fix |
| R38-STREAK-LANDING | landing | The round lands with work that is not where it says, or lands it twice: round 35's outcome commit `95684c65` carries four gate reds it caused, repaired only at `199beb97` (`corpus/lessons/round-35-verifier-spotcheck.md:91`), and a tarball sits untracked at closure (`:87`; `corpus/lessons/round-36.md:110`); round 34 closes with 22 untracked wave-2 paths (`corpus/lessons/round-34-verifier-spotcheck.md:14`, `:194`); round 37's correction block is appended twice, headings at note lines 129 and 158 (`corpus/lessons/round-37-verifier-spotcheck.md:62`), and its C2 counter was amended twice after the change commit with no freeze sha (`:63`); the round-36 lesson carries its `## Mistakes` section twice — `corpus/lessons/round-36.md:39` and `:106`, with `R36-TARBALL-LEFTOVER` duplicated at `:43` and `:110` (the two tables differ only in a column header, the same variant-copy shape as the round-37 note block) | `none` — QUALITY 60 (`corpus/QUALITY.md:124`) is nearest, but its sweep prints only removed or changed lines (`grep -E '^-[^-]'`), so an addition made twice is invisible to it; no criterion requires `untracked=0` at closure or a freeze commit for counter bytes | Closure-state checks land in the same commit as the claim: `git status --porcelain` empty, per-heading occurrence count 1, counter bytes frozen in a commit that precedes the change commit. Round 38 shows a duplicate/extra refusal for table rows: the C2 counter folds duplicates into the extra count (`dups = len(got) - len(gs)` at `tools/check-hook-order-r38.py:200`, `dups == 0` in the pass test at `:205`, `'extra_rows': len(extra) + dups` at `:209`), and `controls.jsonl:2,3` FAIL with `extra_rows 6` and `extra_rows 3`. Not shown: no committed control isolates a duplicate row, the block-duplication shape stays invisible because `entry_rows` stops at the next `## ` (`tools/check-hook-order-r38.py:147`), and at this reading `.ufo/waves/round-38/after/` is untracked (`git status --porcelain -- .ufo/waves/round-38`), so the round's own after receipts are not yet landed |
```

## 3. Able-to-fail status, stated per row (what round 38 does and does not show)

1. **SURVIVOR — partly demonstrated.** The v1 battery is genuinely pre-data: `controls.jsonl` and `run-controls.sh`
   land in the freeze commit `7cbaeb6` (2026-10-26T01:16:08-03:00), before the C1 change `52ffd65` (01:18:12) and
   the C2 change `1fe28e7` (01:21:20) — `git log --format='%h %cI' -- .ufo/waves/round-38/controls/controls.jsonl`.
   Five should-fail controls read below target and the accept control passes, which is the shape QUALITY 73 names.
   Three limits, none of them hidden by the declaration:
   - the sixth should-fail shape, the fixture-gated arm, still reads v1 PASS 10/10 (`controls-q82.jsonl:1`), so the
     survivor class is *live in round 38's own v1 counter* and is caught only by the added Q82 conjunct;
   - `controls-q82.jsonl` and `run-controls-q82.sh` land in `9c9bb64` (01:32:13), i.e. **10–14 minutes after both
     change commits** — that battery is post-data. The pre-seat amendment discloses this ("Read after the freeze and
     after the author's own after-receipts") and only tightens, but it cannot be offered as a pre-data control;
   - QUALITY 73's literal measure ("its declared measure is the battery's last-line field (`should_fail_accepted`)")
     is not adopted: `grep -n "selftest\|should_fail\|battery" tools/score-storage-arm-r38.py
     tools/score-storage-arm-r38-q82.py tools/check-hook-order-r38.py` prints nothing, so QUALITY 72's selftest
     cases are absent too and the declaration's measure stays the bare counter's fields.
2. **VACUOUS — demonstrated in both directions.** `controls-q82.jsonl:1` is the only round-38 receipt where two
   counters disagree on the same arm (v1 PASS 10/10, production-path view 0/3), which is exactly the read-side gap
   that four rounds recorded but none could exhibit as a failing control. `:2` (1/3) refuses a cached live answer and
   `:3` (3/3, per-run seed `e9019669…`) shows the live view cannot be pre-baked. `before/c1-before.json:8`
   (`live_match 0` at base) rules out a constant-pass live leg.
3. **ATTRIBUTION — not demonstrated.** The proof of a fix here would be a receipt that *fails* when its version is
   wrong. Round 38 has none: the receipts carry no `tool_sha256`, `controls.jsonl` carries no revision, and the
   declaration's digests are the only binding. Verified positively that those digests are honest (`sha256sum` equals
   `e649bfb3…`, `a183ff58…`, `60e3635b…`, `cba1bec2…`, `5469e59a…`, matching the SCORECARD declaration), so this is
   a missing header, not a wrong claim.
4. **LANDING — demonstrated for rows only.** `extra_rows` including `dups` (`tools/check-hook-order-r38.py:200,205,209`)
   is a real duplicate refusal, and `controls.jsonl:2,3` show extras refused. It does not reach the R37 shape (a
   duplicated prose block with its own `## ` heading) because the parser breaks at the next `## ` (`:147`), and no
   control isolates a duplicate row — the 6 and 3 extras in those controls come from wrong sort and ignored override.
   `.ufo/waves/round-38/after/` being untracked at this reading is the same class in the current round; the round is
   mid-flight (wave 1 running), so a filing-time commit closes it and this is a snapshot, not a closure finding.

Why `attribution` and not `reference-drift` for row 3: the locators resolve; the failure is that the resolved artefact
measures a different object (a V7 probe, a revision no receipt names). `reference-drift` is the class round 37 itself
used for a counter that required a spelling the note did not carry (`corpus/lessons/round-37.md:36`) — a locator
mismatch, a different defect.

## 4. Findings beyond the four rows (report even though they weaken the draft)

- **F1 (QUALITY 76).** The durable repair for the streak is not a fifth row: it is putting these four ids in the
  frozen owed-ledger form the lane already built (QUALITY 76, `corpus/QUALITY.md:145`) and closing each only with a
  marker that quotes the anchor. Without that, round 38's own two counter debts (QUALITY 73's measure clause, the
  receipts' missing digest header) will be re-minted as `R38-…` rows and the class will recur in round 39 exactly as
  it did in 35, 36 and 37.
- **F2 (QUALITY 77 gap in round 38's own receipts).** `before/c1-before.json`, `before/c2-before.json` and
  `controls/controls.jsonl` are plain JSON, not `run-receipt.py` JSONL with a header/footer, so the SCORECARD
  declaration's revision-cited before-values and control scores are not QUALITY-77 receipts. Whether the
  declaration's inline `sha256` satisfies the tool-digest clause is the judge's call; the receipts themselves do not.
- **F3 (pre-seat amendment ordering).** The Q82 counter and its control battery are the strongest able-to-fail
  evidence in the round and were frozen after both change commits. They are admissible only as a tightening; they
  cannot certify that the *claim* was designed against QUALITY 82 before data, which is what QUALITY 73/82 ask of the
  declaration.
- **F4 (row-count discipline).** All four rows are new ids; none duplicates an existing row in
  `corpus/lessons/round-3{4,5,6,7}.md`. Rows 1 and 2 supersede by name `R34-COUNTER-READ-SIDE-GAPS`
  (`round-34.md:59`), `R35-V1-QUALITY-73-82` and `R35-V2-FORCED-SHAPE-CONSTANTS` (`round-35.md:43-44`) and
  `R36-INVOCATION-GAP`/`R36-SOURCE-ENV-PARAM` (`round-36.md:116,118`), and the lesson should say so rather than
  leave five live ids for one class. Related: `corpus/lessons/round-36.md` already contains one duplicated mistake
  section (`:39`, `:106`) with `R36-TARBALL-LEFTOVER` twice (`:43`, `:110`) — so the "mine the streak" section must
  be added once, and the sweep that proves it was added once (`grep -c '^## Mistakes' corpus/lessons/round-38.md`
  → `1`) belongs in the same commit. That sweep is also the missing repair for QUALITY 60, which cannot see a
  duplicated addition.
- **F5 (why the roster counts sit in the `attribution` row, not `number-drift`).** "The other 12" listing 13 and
  "2 provider refusals" over three holds (`corpus/lessons/round-34-verifier-spotcheck.md:191-192`) are claims about
  *which seats produced which evidence* — the count is the surface, the mis-assignment of output is the defect, and it
  is the same defect as citing a V7 run for a V8 claim. `number-drift` would be the right class only if the record had
  named the right seats and got the arithmetic wrong; the review found the roster itself mismatched.

## 5. Limits — what I did not do

- Did not execute any lane tool, counter, probe, gate or census, and did not re-derive any round's control score;
  every control number above is read from the named receipt.
- Did not edit `SCORECARD.md`, `corpus/QUALITY.md`, any lesson or the round-38 entry; the draft is text for the
  lesson author, not a landed section.
- Did not re-open upstream sources and did not judge C1, C2, any HO row or any axis; I have no closure verdict.
- Did not verify the round-38 C2 entry's 69 rows or the census arm's six selftest cases — out of item scope.
- Tooling: nothing installed, no pacman transaction, no host mutation, no scratch dir (nothing to remove).
  Read-only commands used: `read`, `grep`, `sha256sum`, `git log`, `git ls-files`, `git status --porcelain`.

Receipts: `.ufo/waves/round-38/w1/MineStreak/receipts.txt`.
