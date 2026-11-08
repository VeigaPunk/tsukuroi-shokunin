# ReviewCalibration — C2 calibration checker falsification (tsukuroi round 96, wave w1)

Seat: `ReviewCalibration`. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Measured tree at review close: `a814f24d` ("round-96: register the three r96 tools (SKILL.md); A4/A5
narrowings, …"), with the working tree carrying `M SCORECARD.md`, `?? .ufo/waves/round-96/claim-falsification.tsv`;
pre-round tip `73c47107`; freeze commit `38adc4ed`. All receipts below are under
`.ufo/waves/round-96/w1/ReviewCalibration/` and were produced by this seat. No tool was installed or
upgraded (nothing was needed).

Role: attack C2. The C2 target is `tools/check-r96-calibration.py --root R --report F --tsv T` =
`status PASS`, `findings []` at the landed tree; `status FAIL` with F1-F6 present against
`git archive 73c47107`; `--selftest` = `PASS 7/7`; each one-fault fixture fails only its own id.

## 0. Tree state at review close

```
$ git rev-parse HEAD
a814f24dc31270bca4e8999ac3cd907ecd72f100
$ sha256sum tools/check-r96-calibration.py
7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4  tools/check-r96-calibration.py
$ sha256sum -c .ufo/waves/round-96/before/instruments.sha256
17 lines, all OK; exit 0
$ git cat-file -e HEAD:.ufo/waves/round-96/claim-falsification.tsv
fatal: path ... exists on disk, but not in 'HEAD'      # ledger UNTRACKED, present on disk
$ git ls-files -s .ufo/waves/round-96/before/plan-amendments-A1-A2.md   # git blob id (SHA-1)
100644 5eb654757db5e2f38f4b1a98c0bcffb1475c0ad4 0  .ufo/waves/round-96/before/plan-amendments-A1-A2.md
$ sha256sum .ufo/waves/round-96/before/plan-amendments-A1-A2.md
966487d84b76bc53a5dfeefd00aa7719f56445138cf09adab97ba8502f7ea69e   # A1-A5, tracked at HEAD
```

The filed report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-96/tsukuroi.md` exists. The
checker bytes equal the freeze manifest and the HEAD blob. The round-96 ledger is present on disk
with 11 rows (3 `falsifies-wording`, 1 `falsifies-number`, 7 `neutral`, 5 columns, class in column
3) and the filed report states `3 falsifies-wording rows and 1 falsifies-number row` (line 64) —
numerals that agree with the ledger.

**Drift incident (observed, then repaired, disclosed as A2).** At 07:52:30 the live working-tree
checker was `ad894667f951…` — the frozen `7ff63524…` with F3/F4 substring checks wrapped in
`" ".join(text.split())` (`checker-drift-ad894667-vs-frozen.diff`, 27 lines; my copy's hash
`ad894667…`). The lane restored the pinned bytes and reflowed `tools/make-r95-bends.py` instead; at
review close the manifest reads 17/17 OK. Had `ad894667` landed, C2 would be void by its own kill
clause. A2 discloses this; my receipts are the byte-level datum.

## 1. Commands and raw output

### 1.1 Pre-round archive (frozen checker bytes)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ git archive 73c47107 | tar -x -C /fast/scratch/hyaku/tsukuroi-r96/ReviewCalibration/pre
$ python3 .../checker-head.py --root .../pre \
    --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-95/tsukuroi.md \
    --tsv .ufo/waves/round-95/claim-falsification.tsv --json .../pre-head.json
exit=1
status FAIL
F1 QUALITY.md has no criterion 140
F2 receipt .ufo/waves/round-96/before/r95-registry-gate.sha256 missing
F2 SCORECARD.md has no Round 96 section
F3 tools/limine-pin-battery-r95.py still says largest in-bound
F3 tools/make-r95-bends.py does not say boundary member
F3 lesson does not relate the r95 freeze manifest to the edits
F4 README does not scope the sentence to the r94 family roster
F5 tip receipt .ufo/waves/round-96/before/c2-tip-b8f878c8.json missing
F6 report states no falsifies-wording count
F6 report states no falsifies-number count
unreadable 4
```

`pre-head.json` findings are **identical** (id and detail, same order) to the committed
`before/c2-before-73c47107.json`: 10 findings, ids {F1,F2,F3,F4,F5,F6}, status FAIL
(`findings identical: True count 10 10`). The checker bytes are `7ff63524…` = the manifest = HEAD.

### 1.2 After-leg at the live tree, with the filed report and the round-96 ledger

```
$ python3 tools/check-r96-calibration.py --root $LANE \
    --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-96/tsukuroi.md \
    --tsv .ufo/waves/round-96/claim-falsification.tsv --json .../after-landed-live.json
exit=0
{"schema":"tsukuroi-r96-calibration-v1","root":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
 "report":"/home/vgpnk/Projects/shokunin/.ufo/reports/round-96/tsukuroi.md",
 "findings":[],"unreadable":[],"status":"PASS"}
```

The same on a `git archive a814f24d` copy plus the working SCORECARD, lesson, ledger and filed
report (`after-a814-copy.json`): `status PASS findings [] unreadable []`.

### 1.3 `--selftest`

```
$ TMPDIR=.../tmp python3 .../checker-head.py --selftest
clean  PASS
F1     PASS   F2  PASS   F3  PASS   F4  PASS   F5  PASS   F6  PASS
selftest PASS 7/7        exit=0
```

Scratch TMPDIR residue after the run: empty.

Detailed one-fault fixture probe (`selftest-fixture-detail.txt`), reproducing the checker's own six
mutations and printing every finding:

```
clean findings=[] errors=[]
F1 emits 1 finding(s) with ids ['F1']
F2 emits 2 finding(s) with ids ['F2', 'F2']
F3 emits 2 finding(s) with ids ['F3', 'F3']
F4 emits 2 finding(s) with ids ['F4', 'F4']
F5 emits 1 finding(s) with ids ['F5']
F6 emits 1 finding(s) with ids ['F6']
```

### 1.4 F2 hash chain (`f2-hash-chain.txt`)

```
$ git show b8f878c8:tools/check-registry-coverage.py | sha256sum
6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812  -
--- r96 freeze manifest line:
6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812  tools/check-registry-coverage.py
--- before receipt:
6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812  tools/check-registry-coverage.py
--- current bytes:
6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812  tools/check-registry-coverage.py
```

SCORECARD's `## Round 96` void-binding paragraph names the same hash and the guard; the guard is
true: `git diff 73c47107 59cbfe2f -- tools/check-registry-coverage.py` = 0 lines and
`git diff 73c47107 a814f24d -- tools/check-registry-coverage.py` = 0 lines.

### 1.5 F3 substance (`f3-ast-controls.txt`, `r95-tools-landed-vs-b8f878c8.diff`)

```
tools/limine-pin-battery-r95.py committed=7b0bd6b5ce7da00e working=7b0bd6b5ce7da00e MATCH
tools/make-r95-bends.py        committed=b094e4a9ede99129 working=b094e4a9ede99129 MATCH
```

(AST compared with every module/function/class docstring constant blanked; only docstrings moved.
The landed `git diff b8f878c8 59cbfe2f` has exactly two hunks, both inside docstrings.)

### 1.6 F4 substance

`corpus/README.md:1127-1129` reads: "the r94 family roster has no in-bound 9-digit case (its
`--usage-check` does send `999999999.0.0`, so the sentence is scoped to the roster, not the
instrument; r96 routed-5)". The parenthetical is true:
`git show b8f878c8:tools/limine-pin-battery-r94.py | grep 999999999` → `("999999999.0.0", 0)` inside
`usage_check`; the r94 family roster has no 9-digit version (only `REFUSAL_DIGIT10`'s ten-digit
values). `git diff 73c47107 -- .ufo/plans/round-95.md .ufo/waves/round-95/` is empty, so the r95
predicate was not rewritten.

### 1.7 F5 re-run (`f5-registry-b8f878c8-rerun.json`)

```
$ python3 tools/check-registry-coverage.py --revision b8f878c88fa795fbf20d6129807dfc5222e5fadf
{"branch":"master","branch_tip":"59cbfe2f4b96a73c2697cf81eb989e1d72e276fd",
 "counts":{"findings":0,"missing":0,"registered":151,"rows_total":151,"tools_total":151},
 "findings":[],"revision":"b8f878c88fa795fbf20d6129807dfc5222e5fadf","status":"PASS"}
status MATCH  revision MATCH  branch MATCH  counts MATCH  findings MATCH
branch_tip now=59cbfe2f4b96a73c2697cf81eb989e1d72e276fd receipt=73c47107e8bda79375517ee24ec3c13688586305
```

### 1.8 Attacks (all run against the frozen checker `7ff63524…` on copies of the measured tree)

| attack | result | receipt |
|---|---|---|
| QUALITY 140 names `round-95.md`, `M1`, "development run" but states no rule | `PASS`, `findings []` | `atk-quality-a814.json` |
| SCORECARD Round 96 section mentions `void`, `git diff`, `check-registry-coverage.py` but binds nothing | `PASS`, `findings []` | `atk-scorecard-a814.json` |
| SCORECARD without a Round 96 section (control) | `F2 SCORECARD.md has no Round 96 section` | `atk-scorecard-missing.json` |
| tip receipt `revision: b8f878c8deadbeef…`, fabricated counts | `PASS`, `findings []` | `atk-tip-a814.json` |
| tip receipt `revision: deadbeef…` (control) | `F5 tip receipt is not the r95-tip PASS 151/151 receipt` | `atk-tip-wrongrev-a814.json` |
| report: "3 `falsifies-wording`" first, then the wrong numeral "4 `falsifies-wording`" (the real ledger has 3) | `PASS`, `findings []` | `atk-f6-firstmatch-a814.json` |
| report: "4 `falsifies-wording`" only (control against the real 3) | `F6 report says 4 falsifies-wording, tsv has 3` | `atk-report-numeric4-a814.json` |
| report: "0 `falsifies-wording`, 0 `falsifies-number`" with the real 3/1 ledger in column 2 | `PASS`, `findings []` | `atk-f6-column-a814.json` |
| zero one receipt-hash hex digit (A1 datum) | two findings, ids `['F2','F2']` | `atk-f2-two.json` |
| append a module-level assignment to `tools/limine-pin-battery-r95.py` | `PASS`, `findings []` (AST DIFFER) | `atk-f3-code.json`, `f3-ast-controls.txt` |
| README with the scoped phrase plus a wrapped over-scope sentence | `PASS`, `findings []` | `atk-f4-wrap.json` |

## 2. PASS/FAIL per expected line

| expected | observed | verdict |
|---|---|---|
| pre-archive `73c47107` + r95 report/ledger: FAIL, at least one finding in each F1-F6 | FAIL, 10 findings, ids {F1..F6}, identical to `before/c2-before-73c47107.json` | **PASS** |
| after: `status PASS`, `findings []` at the landed tree | live tree + filed report + round-96 ledger: `PASS []`, `unreadable []`; `a814f24d` archive copy: `PASS []` | **PASS** (ledger still untracked — see F-a) |
| `--selftest` reads `PASS 7/7` | `selftest PASS 7/7`, exit 0 | **PASS** |
| each one-fault fixture fails exactly its own finding (clean: none) | clean `[]`; id sets are singletons; raw finding counts are 1,2,2,2,1,1 (F2/F3/F4 emit two findings of their own id) | **PASS only under A1's id narrowing; literal frozen wording FAILS** |
| F1 substantive rule citing round-95.md M1 and a development run | criterion 140 is a real admission rule; lesson M1 says what it cites | **PASS** (checker accepts a rule-free stub — finding) |
| F2 receipt hash = `git show b8f878c8:… | sha256sum` = freeze manifest line | all four hashes equal `6fcb2d0a…` | **PASS** (SCORECARD half is token-checked — finding) |
| F3 only docstring/comment lines moved | AST with docstrings blanked: MATCH for both tools; diff = two docstring hunks | **PASS** (checker is blind to code edits — finding) |
| F4 sentence reads scoped in context | scoped; parenthetical factually true | **PASS** (line-sensitive guard — finding) |
| F5 re-run compared with the committed tip receipt | `PASS` 151/151, findings 0; every field matches but `branch_tip` (run-time) | **PASS** (receipt not bound to tool bytes — finding) |
| F6 report parser cannot pass a wrong count | two false-acceptance passes reproduced | **FAIL** |

## 3. Findings by severity

**MEDIUM**

1. **F6 false acceptance in the first-match direction (the disclosed limit covers only the other
   direction).** `re.search(r"(\d+)\s+`?<class>", text)` binds the first numeral anywhere in the
   report. A report that states the truthful count first ("3 `falsifies-wording`") and a wrong
   numeral later ("4 `falsifies-wording` rows point at A2/A3/A4") passes
   (`atk-f6-firstmatch-a814.json` PASS), because the ledger paragraph is never located. A5/SCORECARD
   disclose that a truthful report quoting the r95 wrong count first is *rejected*; the converse
   (a wrong count later is *accepted*) is not covered, and the F1-F6 docstring still says
   "the report's falsification-ledger sentence states the verdict-class counts". Receipts:
   `atk-f6-firstmatch-a814.json`, `atk-report-numeric4-a814.json`.
2. **F6 column-index hole.** The TSV counter is hard-coded to column index 2. A ledger with the class
   in column 2 (3 wording + 1 number) plus a report saying "0 `falsifies-wording` rows and 0
   `falsifies-number` rows" passes (`atk-f6-column-a814.json` PASS). The round-96 ledger happens to
   use the expected 5-column shape (class in column 3: `3/1/7`), so the hole is latent this round,
   but the checker never validates the ledger's header/column order.
3. **F5 receipt is a bare JSON.** The tip receipt is checked only for `status`, a
   `revision.startswith("b8f878c8")` prefix and three counts. A hand-written
   `{"status":"PASS","revision":"b8f878c8deadbeef…","counts":{…151,151,0…}}` passes
   (`atk-tip-a814.json`); `missing`/`rows_total` are unchecked and the receipt names no
   `tool_sha256`, command, or run time. The re-run shows the substantive fields match, but the
   checker cannot tell a measured receipt from a fabricated one. A truly wrong revision fails
   (`atk-tip-wrongrev-a814.json`), so the prefix is the only guard.
4. **F2's SCORECARD half is token-shaped.** A `## Round 96` section that merely mentions `void`,
   `git diff` and `check-registry-coverage.py` passes (`atk-scorecard-a814.json` PASS). Only the
   receipt-hash chain is substantive; the "binding" sentence itself is unchecked. (Removing the
   section fails: `atk-scorecard-missing.json`.)
5. **The round-96 ledger is not committed yet.** `git cat-file -e HEAD:.ufo/waves/round-96/claim-falsification.tsv`
   → "exists on disk, but not in 'HEAD'"; `git status` shows it `??`. The C2 target says "the
   committed round-96 ledger". The after-leg passes with the file on disk; the landing condition is
   the commit.
6. **F1 is token-shaped (declared limit).** A QUALITY block containing `round-95.md`, `M1` and
   "development run" with no rule passes (`atk-quality-a814.json` PASS). The landed criterion 140 is
   a real rule (verified), and A5/SCORECARD declare F1 a substring condition; the instrument still
   does not enforce "rule".

**LOW**

7. **A1-A5 are not in the plan's amendment slot.** The plan (`38adc4ed`, hash `5d389241…` matching
   the manifest) still ends at "Amendments are appended here (A1, A2, …)"; the amendments live in
   `before/plan-amendments-A1-A2.md` (tracked at HEAD, sha256 `966487d8…`, five sections, cited by
   the SCORECARD's measured-outcome section). The lane's rounds 92-94 appended amendments to
   `.ufo/plans/round-9N.md`, so this is a traceability deviation from the plan's own mechanism and
   its precedent; the narrowing is landed and referenced, not hidden. A1 is nevertheless required:
   the selftest's F2/F3/F4 mutants each emit two findings of their id
   (`selftest-fixture-detail.txt`), so the literal frozen target fails without the id narrowing.
8. **F3 is blind to code (declared limit).** The F3 checks grep docstring text; appending a
   module-level assignment to `tools/limine-pin-battery-r95.py` still passes (`atk-f3-code.json`;
   the AST of the same file DIFFERs, `f3-ast-controls.txt`). The landed bytes are docstring-only
   (verified), and A5/SCORECARD declare the blindness.
9. **F4's over-scope guard is line-sensitive (declared limit).** The pre-round sentence wraps
   between "has no" and "in-bound", so the frozen checker's second F4 check does not fire on the
   archive it targets (`pre-head.json` has one F4 finding, not two). A README that keeps the scoped
   phrase and adds a wrapped over-scope sentence passes (`atk-f4-wrap.json`).
10. **Transient instrument drift (declared, A2).** The live checker was `ad894667…` (a post-freeze
    whitespace-flattening edit) when this seat read it; it made F3 pass on a wrapped docstring and
    changed the pre-archive reading from 10 to 12 findings (`pre-wt.json`). The pinned bytes are
    restored (manifest 17/17 OK); recorded because the C2 void clause hinges on exactly this byte.

## 4. Residual risk and verification gaps

- The after-leg is measured on the working tree with the filed report and an **uncommitted** ledger;
  if the ledger's bytes change at landing (or the report's numerals change), F6's agreement is not
  re-established by anything in this seat.
- Finding 1: if the filed report keeps a wrong numeral anywhere after a correct one, the checker
  still passes; the ledger-sentence guarantee rests on the author, not the instrument.
- `before/plan-amendments-A1-A2.md` is tracked at HEAD but sits outside the plan's amendment slot;
  a scorer reading only `.ufo/plans/round-96.md` sees no A1-A5.
- `instruments.sha256` does not authenticate itself; the chain rests on the frozen commits
  `38adc4ed`/`b0bf1be9`/`a814f24d` and the git history.
- `c2-tip-b8f878c8.json` is reproducible in every field except `branch_tip`, which is run-time
  (`73c47107` then, `59cbfe2f` at my re-run). Any byte-equality test on that file fails by design.

## 5. Receipts (all written by this seat)

`instruments-check.txt`, `pre-head.json/.txt`, `pre-wt.json/.txt`,
`current-head-r95report.json/.txt`, `current-wt-r95report.json/.txt`,
`after-frozen-checker.json/.txt`, `after-drifted-checker.json/.txt`,
`after-fixed-frozen.json/.txt`, `after-head-frozen.json/.txt`,
`after-landed-live.json/.txt`, `after-a814-copy.json/.txt`,
`live-noreport.json/.txt`, `live-with-synthetic.json/.txt`,
`selftest-head.txt`, `selftest-wt.txt`, `selftest-head-tmpdir.txt`, `selftest-fixture-detail.txt`,
`f2-hash-chain.txt`, `f3-ast-docstring-equivalence.txt`, `f3-ast-controls.txt`,
`r95-tools-vs-b8f878c8.diff`, `r95-tools-landed-vs-b8f878c8.diff`,
`checker-bytes.txt`, `checker-drift-vs-HEAD.diff`, `checker-drift-ad894667-vs-frozen.diff`,
`f5-registry-b8f878c8.json/.err`, `f5-registry-b8f878c8-rerun.json/.err`,
`atk-quality-a814.json/.txt`, `atk-scorecard-a814.json/.txt`, `atk-scorecard-missing.json/.txt`,
`atk-tip-a814.json/.txt`, `atk-tip-wrongrev-a814.json/.txt`,
`atk-f6-firstmatch-a814.json/.txt`, `atk-report-numeric4-a814.json/.txt`,
`atk-f6-column-a814.json/.txt`, `atk-f2-two.json/.txt`, `atk-f3-code.json/.txt`,
`atk-f4-wrap.json/.txt`, plus the earlier `atk-*-head` and `atk-report-firstmatch` receipts from the
same checker bytes (`7ff63524…`, identical before and after the tree advanced).

Scratch root `/fast/scratch/hyaku/tsukuroi-r96/ReviewCalibration` is removed before yielding; no
scratch path is cited as evidence.

{"seat":"ReviewCalibration","verdict":"findings","notes":"After-leg PASS [] at the measured tree (a814f24d) with the filed round-96 report and the 3-wording/1-number ledger; pre-archive reproduces the frozen 10-finding FAIL exactly; selftest 7/7; instrument bytes = manifest 7ff63524 (17/17 OK, drift ad894667 reverted and disclosed as A2). Substantive repairs verified: F2 hash chain 6fcb2d0a = b8f878c8 blob = manifest = current; F3 AST with docstrings blanked MATCH on both r95 tools; F4 scoped and factually true (usage_check sends 999999999.0.0); F5 re-run PASS 151/151 matches the tip receipt but for run-time branch_tip. Remaining findings: F6 accepts a report that states the right count first and a wrong numeral later (3 then 4 against a 3-row ledger), and a 0/0 report against a class-in-column-2 ledger; F5 accepts a fabricated receipt whose revision merely starts b8f878c8; F2's SCORECARD binding is token-only; F1 is token-only (declared limit); F3 is blind to code edits (declared); F4's guard is line-wrapped-blind (declared); A1-A5 live in a tracked side file, not the plan's amendment slot (A1 is required: the selftest's F2/F3/F4 mutants emit two findings of one id); the round-96 ledger is still untracked, so the target's 'committed ledger' clause awaits the commit."}
