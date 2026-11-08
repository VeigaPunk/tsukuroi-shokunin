# ExecCalibration — round 96 w1 (C2 counter: six routed r95 mismatch classes)

Seat: `ExecCalibration` (executor, axis calibration). Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Final measurement HEAD: `59cbfe2f4b96a73c2697cf81eb989e1d72e276fd` (detached; landed commit
"round-96: C2 repairs …", 07:54:23). Earlier in-flight measurements were at `b0bf1be9` (dirty tree).
Tools: `Python 3.14.8`, `git 2.56.0`; no installs; pacman untouched; no git/jj mutation (read-only git only).
Receipts: `.ufo/waves/round-96/w1/ExecCalibration/`. Scratch: `/fast/scratch/hyaku/tsukuroi-r96/ExecCalibration`
(deleted after this report).

## Final readings at the landed tree (HEAD `59cbfe2f`, re-run on request)

### Reading 1 — instrument freeze holds

```
sha256sum -c .ufo/waves/round-96/before/instruments.sha256   # in state-at-measurement-final.txt
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r96.py: OK
tools/make-r96-bends.py: OK
tools/check-r96-calibration.py: OK          # was FAILED in the in-flight tree
tools/check-registry-coverage.py: OK
... (every .ufo/ line and every control/bend line: OK)
sha256sum tools/check-r96-calibration.py
7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4  tools/check-r96-calibration.py
git show 59cbfe2f:tools/check-r96-calibration.py | sha256sum
7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4  -
```

0 FAILED; the working bytes equal the manifest line equal the committed blob. The C2 void condition
("differs from the freeze manifest at scoring time") does not hold.

### Reading 2 — selftest

```
python3 tools/check-r96-calibration.py --selftest
clean  PASS
F1     PASS
F2     PASS
F3     PASS
F4     PASS
F5     PASS
F6     PASS
selftest PASS 7/7
```

Exit 0 (`c2-selftest-final.stdout`). The freeze-manifest copy (`frozen-checker-7ff63524.py`, sha256
verified) gives the same `selftest PASS 7/7` (`c2-selftest-frozenchecker.stdout`).

### Reading 3 — pre-round tree FAIL with all six classes

```
mkdir -p /fast/scratch/hyaku/tsukuroi-r96/ExecCalibration/before
git archive 73c47107e8bda79375517ee24ec3c13688586305 | tar -x -C /fast/scratch/hyaku/tsukuroi-r96/ExecCalibration/before
python3 tools/check-r96-calibration.py --root /fast/scratch/hyaku/tsukuroi-r96/ExecCalibration/before \
  --tsv .ufo/waves/round-95/claim-falsification.tsv \
  --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-95/tsukuroi.md \
  --json .ufo/waves/round-96/w1/ExecCalibration/c2-before-final.json
```

Exit 1 (`c2-before-final.json`): `status FAIL`, 10 findings, ids `F1 F2 F3 F4 F5 F6`, 4 unreadable
(the four r96-only files absent in the r95 archive):

```
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
```

The same run with the freeze-manifest checker copy on the same archive reproduces the L1's committed
reference exactly (`c2-before-frozenchecker.json` vs `before/c2-before-73c47107.json`):

```
findings equal: True
unreadable equal: True
status equal: True
reference findings: 10 mine: 10
root mine: /fast/scratch/hyaku/tsukuroi-r96/ExecCalibration/before
root ref : /fast/scratch/hyaku/tsukuroi-r96/before-root
```

### Reading 4 — current tree PASS (no `--report`, as the seat item specifies)

```
python3 tools/check-r96-calibration.py --root . --json .ufo/waves/round-96/w1/ExecCalibration/c2-after-landed.json
HEAD 59cbfe2f4b96a73c2697cf81eb989e1d72e276fd
7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4  tools/check-r96-calibration.py
{"schema":"tsukuroi-r96-calibration-v1","root":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
 "report":null,"findings":[],"unreadable":[],"status":"PASS"}
```

Exit 0. (HEAD and the checker hash are written into the same receipt, `c2-after-landed.stdout`.)

### Reading 5 — commit-local instrument deltas

```
git show 59cbfe2f:tools/make-r95-bends.py | grep -c 'boundary member'      -> 1   (contiguous on line 6)
git show 59cbfe2f:tools/limine-pin-battery-r95.py | grep -c 'largest in-bound' -> 0
git diff --stat 73c47107..59cbfe2f -- tools/check-registry-coverage.py     -> (empty; 0 lines)
```

## PASS/FAIL per expected line

| # | Expected (seat item) | Final measured | Verdict |
|---|---|---|---|
| 1 | Before: `status FAIL`, ≥1 finding in each F1–F6 | FAIL, 10 findings, every id F1–F6 present; reproduces `before/c2-before-73c47107.json` | **PASS** |
| 2 | After (`--root .`, no `--report`): `status PASS`, `findings []`, `unreadable []` | PASS / [] / [] at HEAD `59cbfe2f` with the manifest-pinned checker | **PASS** |
| 3 | `--selftest` PASS 7/7 | `selftest PASS 7/7`, exit 0 | **PASS** |
| 4a | Criterion 140 in `corpus/QUALITY.md`, citing the lesson/M1/a development run | block `140.` present; `round-95.md` True, `M1` True, `development run` True | **PASS** |
| 4b | Receipt hash equals `sha256sum tools/check-registry-coverage.py` | `6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812` both; also pinned in the freeze manifest | **PASS** |
| 4c | Two r95 docstrings corrected | battery: raw `boundary member` (lines 29/32/1694/1708), raw `largest in-bound` = 0; make-r95-bends: raw `boundary member` on line 6, raw `largest in-bound` = 0 | **PASS** |
| 4d | README scoped to the r94 family roster, over-scope gone | `corpus/README.md:1127-1129` scoped; `before instrument has no in-bound` = 0 | **PASS** |
| 4e | Tip receipt is the r95-tip PASS 151/151 receipt | status PASS, revision `b8f878c8…`, counts 151/151, findings 0 | **PASS** |
| 4f | F6 fires exactly its own id on a wrong count | wrong count → exactly `[{F6,"report says 3 falsifies-wording, tsv has 2"}]`; word count → exactly two F6 ("states no … count"); matching control → PASS 0 | **PASS** |

## Six-fix verification detail

- **F1**: `corpus/QUALITY.md` block `140.` exists (regex `^\d+\. \*\*`); block contains `round-95.md`,
  `M1`, `development run`. Lesson line: `Lesson: corpus/lessons/round-95.md Mistakes M1 and Routed 1; routed r95-2.`
- **F2**: `.ufo/waves/round-96/before/r95-registry-gate.sha256` =
  `6fcb2d0a…  tools/check-registry-coverage.py`; `sha256sum tools/check-registry-coverage.py` identical;
  the hash appears in `before/instruments.sha256`; `SCORECARD.md` `## Round 96` contains `void`,
  `git diff`, `check-registry-coverage.py`; `git diff 73c47107..59cbfe2f -- tools/check-registry-coverage.py`
  is empty (the binding is measurable, not asserted).
- **F3**: after the L1 reflow, both r95 files carry the corrected phrase contiguously; neither carries the
  superseded phrase anywhere raw or flattened. The r96 lesson (`corpus/lessons/round-96.md` §"Relation to the
  r95 freeze manifest") relates the r95 manifest to the edited bytes.
- **F4**: current README sentence: `… the r94 family roster has no / in-bound 9-digit case (its --usage-check
  does send 999999999.0.0, so the sentence is scoped to / the roster, not the instrument; r96 routed-5)`.
  The r95 archive carries the over-scope sentence (`the before instrument has no / in-bound 9-digit case`).
- **F5**: tip receipt JSON: `{"status":"PASS","revision":"b8f878c88fa795fbf20d6129807dfc5222e5fadf",
  "counts":{"tools_total":151,"registered":151,"findings":0,...},"findings":[]}`.
- **F6**: scratch ledger `f6-ledger.tsv` (2 `falsifies-wording`, 1 `falsifies-number`), three reports:
  wrong numeric count → exactly one F6 (detail names 3 vs 2); word count "four" → exactly two F6 (unbindable);
  matching "2 … and 1 …" → findings [].

## In-flight deviation that the L1 repaired (recorded, not current)

Measured at HEAD `b0bf1be9` (07:51–07:53), before the repair commit `59cbfe2f`:

- `instruments.sha256` FAILED on `tools/check-r96-calibration.py`: manifest `7ff63524…`, working tree
  `ad894667…` (10-line whitespace-flattening of the F3/F4 probes, uncommitted). C2's void condition was
  tripped at that instant.
- The manifest-pinned bytes then read the current tree as `FAIL` with exactly one finding:
  `F3 "tools/make-r95-bends.py does not say boundary member"` — the r96 wording was line-wrapped
  (`a boundary` / `member`), so the raw substring was absent (`c2-after-noreport-frozenchecker.json`).
- Scratch simulation of the freeze-preserving repair (reflow the docstring + restore the pinned checker)
  read PASS 0 findings under both checker versions (`sim-reflow-frozenchecker.json`,
  `sim-reflow-currentchecker.json`). The L1 then landed exactly that repair in `59cbfe2f`; the three
  readings above are the post-repair re-runs.

Also in flight: the working-tree checker (flattened) read the r95 archive with 12 findings (extra F3/F4 for
the wrapped old phrases), still ≥1 per class; the pinned checker reads 10 (`c2-before.json` vs
`c2-before-frozenchecker.json`) — historical receipts kept, not used for the final table.

## Open dependency

`.ufo/waves/round-96/claim-falsification.tsv` (round-96 ledger) does not exist yet; C2's "with the filed
report and the committed ledger" leg is therefore not runnable by this seat (the seat item's step 2 omits
`--report` by design). The scratch-ledger F6 discrimination above shows the check itself works. The ledger
and the filed report are the L1's filing, exactly as the L1 stated.

## Receipts (all under `.ufo/waves/round-96/w1/ExecCalibration/`, written by this seat)

Final (landed tree):
- `state-at-measurement-final.txt` — HEAD, `git status --porcelain`, full `sha256sum -c`, instrument hashes.
- `c2-after-landed.json`, `c2-after-landed.stdout` — header HEAD + checker hash + PASS JSON.
- `c2-selftest-final.stdout` — PASS 7/7.
- `c2-before-final.json`, `c2-before-final.stdout` — FAIL, F1–F6, on the `git archive 73c47107` tree.
- `c2-f6-wrongcount-final.json|.stdout`, `c2-f6-wordcount-final.json|.stdout`,
  `c2-f6-matching-final.json|.stdout` — F6 discrimination with the landed checker.
- `frozen-checker-7ff63524.py`, `frozen-checker-7ff63524.sha256` — the freeze-manifest checker bytes
  (also re-derivable via `git show 38adc4ed:tools/check-r96-calibration.py`).
- `f6-ledger.tsv`, `f6-report-wrong.md`, `f6-report-word.md`, `f6-report-ok.md` — the F6 fixtures.

In-flight (kept as history):
- `state-at-measurement.txt`, `c2-before.json`, `c2-before-frozenchecker.json`,
  `c2-after-noreport.json`, `c2-after-noreport-frozenchecker.json`, `c2-selftest.stdout`,
  `c2-selftest-frozenchecker.stdout`, `sim-reflow-*.json`, `c2-f6-*.json` (pre-final names).

Scratch `/fast/scratch/hyaku/tsukuroi-r96/ExecCalibration` was deleted after writing this report; the
before tree is re-creatable with the exact `git archive` command above.

## Notes

- Axis: calibration (C2). No lane file, instrument, doc, or control was edited by this seat; all writes are
  receipts under this seat dir. No git/jj mutation was run.
- No tool install was needed (stdlib Python only); the host package manager was not touched.

{"seat":"ExecCalibration","verdict":"met","notes":"Final landed-tree readings at HEAD 59cbfe2f with the manifest-pinned checker 7ff63524 (working bytes = committed blob = manifest): instruments.sha256 all OK, --selftest PASS 7/7, current tree PASS findings [] unreadable [], pre-round archive 73c47107 + r95 report/ledger FAIL with F1-F6 all present (10 findings, exactly the L1's committed c2-before receipt); six fixes verified independently (criterion 140 cites round-95.md/M1/development run; receipt hash 6fcb2d0a matches the registry gate and is pinned in the manifest; both r95 docstrings now carry raw 'boundary member' and no 'largest in-bound'; README scoped to the r94 family roster with the over-scope sentence gone; tip receipt b8f878c8 PASS 151/151 findings 0; F6 fires exactly its own id on a wrong numeric count, reports two F6 when the count is unboundable, and is clean on a matching count); git diff 73c47107..59cbfe2f over tools/check-registry-coverage.py is empty. The in-flight deviation (working-tree checker ad894667 vs manifest 7ff63524; pinned bytes one F3 on the wrapped 'boundary member') was repaired by the L1 in 59cbfe2f exactly as simulated; historical receipts retained. Open dependency: the round-96 claim-falsification.tsv is absent, so the committed-ledger F6 leg is the L1 filing."}
