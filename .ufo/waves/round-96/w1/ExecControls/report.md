# ExecControls — round 96 w1 (C2 one-fault controls)

Seat: `ExecControls`, role executor, axis **calibration**. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Work executed in-seat: the lane tool set does not grant `task`, so the one-labrat allowance was not
used and every run below is mine.
Scratch root (deleted before yield): `/fast/scratch/hyaku/tsukuroi-r96/ExecControls`.
Receipts: `.ufo/waves/round-96/w1/ExecControls/receipts/` (this directory). Python 3.14.8, no tool
installs or upgrades, no pacman transaction, no write outside this seat directory and scratch.

## 1. Instrument state at measurement time

Two passes were necessary because the lane moved while pass 1 ran. Both are reported raw.

**Pass 1 (started ~07:52 -0300) — tree carrying a post-freeze checker edit**

| item | sha256 |
|---|---|
| `tools/check-r96-calibration.py` (worktree, mtime 07:47:39, size 13579, `git status` ` M`) | `ad894667f951d2cc900ca240509c56207f7dee486448ac8782a2808fc13aa1d9` |
| freeze-manifest pin for the same path | `7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4` |
| `git show HEAD:tools/check-r96-calibration.py` | `7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4` |

**Pass 2 / final (07:56 -0300) — repaired tree; this is the authoritative measurement**

| item | sha256 |
|---|---|
| `tools/check-r96-calibration.py` (worktree; committed at `59cbfe2f`, equals the freeze pin) | `7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4` |
| freeze-manifest pin | same — `manifest_pin_matches_worktree_checker: True` |
| all 17 manifest entries re-measured | 17 × `OK`, 0 × `DIFF` (`receipts/instruments-state.txt`) |
| `tools/make-r95-bends.py` (r95/r96 fix, not pinned by the r96 manifest) | `bbcb18f3c2b1c80e6ed375249bffb53fcc1def7d1043bb2e75e1452ba1003da7` |
| `tools/limine-pin-battery-r95.py` (r95/r96 fix, not pinned) | `e19d3c0b50aa07dba3ab8b5646314d39ab9bb721e754eaa8bd4c3fb96de9dcf5` |
| `.ufo/waves/round-96/claim-falsification.tsv` | **absent** at measurement (wave in flight) |

Raw: `receipts/instruments-state.txt`.

Post-measurement invariant (`receipts/post-check-head-59cbfe2f.txt`): at the C2-repairs commit
`59cbfe2f` all 11 pass-2 input files are byte-identical to the `base2` snapshot (`changed=0`; the r96
ledger is `SAME-ABSENT` on both sides), so the pass-2 receipts remain valid at the committed tree.

## 2. Commands run

Fixture roots (scratch only; every mutation asserts exactly one substitution match, like
`tools/make-r96-bends.py`; nothing under the lane is written):

```
mkdir -p <scratch>/base2/.ufo/waves/round-96
cp -a corpus tools SCORECARD.md <scratch>/base2/
cp -a .ufo/waves/round-96/before <scratch>/base2/.ufo/waves/round-96/
cp -a .ufo/waves/round-96/claims.json <scratch>/base2/.ufo/waves/round-96/
cp -a <scratch>/base2 <scratch>/R1 && python3 .../mutate.py <scratch>/R1 M1   # ... R1..R6, U1..U5
python3 .ufo/waves/round-96/w1/ExecControls/run-matrix-r2.py                  # cwd = lane root
python3 tools/check-r96-calibration.py --root <root> [--report <root>/report.md] --json <receipt>
python3 tools/check-r96-calibration.py --selftest
```

Mutation (one reverted fix each, `receipts/mutations.log`):

| root | fix reverted | file before → after |
|---|---|---|
| R1 | QUALITY criterion 140 renamed `999. **` (F1) | `corpus/QUALITY.md` 10d6a08d… → 37783baa… |
| R2 | one hex digit of the receipt hash corrupted (F2) | `before/r95-registry-gate.sha256` 8702e01a… → 59bd3226… |
| R3 | "largest in-bound member" restored (F3) | `tools/limine-pin-battery-r95.py` e19d3c0b… → 7f71fd18… |
| R4 | "the before instrument has no in-bound…" restored (F4) | `corpus/README.md` 02a52605… → 4c876f52… |
| R5 | tip receipt `"status":"PASS"` → `"FAIL"` (F5) | `before/c2-tip-b8f878c8.json` c569dc79… → cda0bc38… |
| R6 | r95 ledger copied to the r96 ledger path + report says `2 falsifies-wording` (F6) | ledger 7c15d8c5… (r95 bytes) |
| U1 | receipt hash correct, `## Round 96` cut from SCORECARD | `SCORECARD.md` 211d2bcc… → 0f37951b… |
| U2 | r95 ledger + report says `9 falsifies-wording` / `0 falsifies-number` | report 32fe921f… |
| U3 | r95 ledger + report names no count | report 2f2faa40… |
| U4 | r95 ledger + report matches its counts `6` / `1` | report d494b6cb… |
| U5 | receipt correct, its pin line cut from the freeze manifest | `instruments.sha256` 295464e9… → de289d91… |

## 3. Raw results — pass 2 (authoritative, checker = freeze pin)

`receipts/matrix-r2.json`, `receipts/matrix-r2.stdout.txt`, per-root `receipts/r2-*.json`.

```
base2 exit=0 status=PASS ids=[] n=0
R1    exit=1 status=FAIL ids=F1 n=1
R2    exit=1 status=FAIL ids=F2 n=2
R3    exit=1 status=FAIL ids=F3 n=1
R4    exit=1 status=FAIL ids=F4 n=1
R5    exit=1 status=FAIL ids=F5 n=1
R6    exit=1 status=FAIL ids=F6 n=1
U1    exit=1 status=FAIL ids=F2 n=1
U2    exit=1 status=FAIL ids=F6 n=2
U3    exit=1 status=FAIL ids=F6 n=2
U4    exit=0 status=PASS ids=[] n=0
U5    exit=1 status=FAIL ids=F2 n=1
```

Finding details verbatim (`receipts/r2-<root>.json`):

```
R1  F1 QUALITY.md has no criterion 140
R2  F2 receipt hash != current tools/check-registry-coverage.py
R2  F2 the r96 freeze manifest does not pin the receipt hash
R3  F3 tools/limine-pin-battery-r95.py still says largest in-bound
R4  F4 README does not scope the sentence to the r94 family roster
R5  F5 tip receipt is not the r95-tip PASS 151/151 receipt
R6  F6 report says 2 falsifies-wording, tsv has 6
U1  F2 SCORECARD.md has no Round 96 section
U2  F6 report says 9 falsifies-wording, tsv has 6
U2  F6 report says 0 falsifies-number, tsv has 1
U3  F6 report states no falsifies-wording count
U3  F6 report states no falsifies-number count
U5  F2 the r96 freeze manifest does not pin the receipt hash
```

Selftest, pinned bytes: `clean PASS / F1..F6 PASS / selftest PASS 7/7`, exit 0
(`receipts/selftest.r2-pinned.txt` = the committed `7ff63524…` bytes at pass 2; identical output from
the pass-1 `current` and `frozen` binaries, exit 0 each, in `receipts/selftest.current.txt` and
`receipts/selftest.frozen.txt`).

## 4. Raw results — pass 1 (tree carrying the post-freeze checker edit)

Two binaries were run on the same pass-1 roots: the worktree bytes (`current`, ad894667…) and the
freeze-pinned bytes (`frozen`, 7ff63524…, re-extracted with `git show HEAD:…`).
`receipts/matrix.json`, `receipts/matrix.stdout.txt`, per-root `receipts/<root>.{current,frozen}.json`.

```
base  current  exit=0 status=PASS ids=[] n=0
base  frozen   exit=1 status=FAIL ids=F3 n=1
M1    current  exit=1 FAIL ids=F1 n=1      M1    frozen FAIL ids=F1,F3 n=2
M2    current  exit=1 FAIL ids=F2 n=2      M2    frozen FAIL ids=F2,F3 n=3
M3    current  exit=1 FAIL ids=F3 n=1      M3    frozen FAIL ids=F3 n=2
M4    current  exit=1 FAIL ids=F4 n=2      M4    frozen FAIL ids=F3,F4 n=2
M5    current  exit=1 FAIL ids=F5 n=1      M5    frozen FAIL ids=F3,F5 n=2
M6    current  exit=1 FAIL ids=F6 n=1      M6    frozen FAIL ids=F3,F6 n=2
S1    current  exit=1 FAIL ids=F2 n=1      S1    frozen FAIL ids=F2,F3 n=2
S2    current  exit=1 FAIL ids=F6 n=2      S2    frozen FAIL ids=F3,F6 n=3
S2b   current  exit=1 FAIL ids=F6 n=2      S2b   frozen FAIL ids=F3,F6 n=3
S3    current  exit=0 PASS ids=[] n=0      S3    frozen FAIL ids=F3 n=1
S4    current  exit=1 FAIL ids=F2 n=1      S4    frozen FAIL ids=F2,F3 n=2
```

The frozen binary's single extra finding on every pass-1 root was, verbatim:

```
F3: tools/make-r95-bends.py does not say boundary member
```

because the r96 correction wrapped the two words (`refuses a boundary` / `member (first
component…`). Probe `S5` (`s5-rewrap.py`, `receipts/S5.*`) rewrapped only that header, keeping
every word and changing no code path: the file's sha256 became
`bbcb18f3c2b1c80e6ed375249bffb53fcc1def7d1043bb2e75e1452ba1003da7`, and **both** binaries then read
`S5 current exit=0 PASS findings=[]` / `S5 frozen exit=0 PASS findings=[]`. With that same rewrap,
the pinned binary read exactly one id on each one-fault fixture
(`receipts/T{M1..M6}.frozen.json`):

```
M1 frozen FAIL ids=['F1'] n=1   M2 frozen FAIL ids=['F2'] n=2   M3 frozen FAIL ids=['F3'] n=1
M4 frozen FAIL ids=['F4'] n=1   M5 frozen FAIL ids=['F5'] n=1   M6 frozen FAIL ids=['F6'] n=1
```

At 07:54:00 the worktree was repaired in exactly this way (checker restored to the pinned
`7ff63524…`, `make-r95-bends.py` rewrapped to `bbcb18f3…`), which is the state pass 2 measures.
Nothing in this seat edited a lane file.

## 5. PASS/FAIL per expected line (seat item, judged on calibration)

| # | expected (seat item / C2 predicate) | observed (pass 2) | verdict |
|---|---|---|---|
| 1 | six scratch roots with exactly one fix reverted each, from the current tree's inputs | R1-R6 built from `base2`; `mutate.py` asserts exactly one match per edit; before→after sha256 in `receipts/mutations.log` | **PASS** |
| 2 | each root fails exactly its own id (clean: none) | base2 `[]` exit 0; R1 `{F1}` R2 `{F2}` R3 `{F3}` R4 `{F4}` R5 `{F5}` R6 `{F6}`, each exit 1 | **PASS** |
| 2a | finding count per root | R2 emits two F2 findings and R4 one F4 finding under the pinned (line-based) bytes — id set is still exactly `{F2}` / `{F4}`; counts recorded, not rounded | **PASS** (id-level, as frozen) |
| 3 | receipt whose hash is the current gate's but SCORECARD section missing still fails | U1 → `F2 SCORECARD.md has no Round 96 section`, exit 1 | **PASS** |
| 4 | report whose counts match no ledger still fails | U2 (9/0) → two F6; U3 (no counts) → two F6; both exit 1 | **PASS** |
| 5 | selftest 7/7 | `selftest PASS 7/7`, exit 0 | **PASS** |
| 6 | C2 "before" leg (all six classes on 73c47107 + r95 report/ledger) | not this seat's item; `receipts/instruments-state.txt` records the pre-round artifact hash `c2-before-73c47107.json` = manifest OK | not measured here |

## 6. Findings (raw)

- **D1 — the freeze-manifest divergence was live for ~6 minutes and is now gone.** At pass 1,
  `tools/check-r96-calibration.py` was `ad894667…` while the manifest pinned `7ff63524…` (its own
  uncommitted flattening edit, mtime 07:47:39, after the freeze commit `38adc4ed` 07:46:47). C2's
  kill rule voids on that condition, and under the pinned bytes the then-tree read F3. Both numbers
  and both readings are in `receipts/matrix.json` and `receipts/instruments-state.txt`. Pass 2
  measures the repaired tree: checker = pin, 17/17 manifest entries OK. Recorded so the scorer can
  bind the C2 void clause to the bytes that were scored, not to my pass-1 snapshot.
- **D2 — F6 has no ledger provenance binding.** U4 (r95 ledger copied to the r96 ledger path + a
  report stating its `6 falsifies-wording` / `1 falsifies-number` counts) reads `PASS` with 0
  findings. F6 binds the report sentence to the file at the ledger path, not to a digest or to the
  round that produced it; provenance is bound elsewhere (`scripts/hyaku/prefile-falsification.py`,
  the ledger's own row/attack-seat shape). Raw, not remediated. Consequence for C2's after-leg: the
  r96 ledger is **absent** at measurement, so the after-leg (0 findings with the filed r96 report)
  is not yet evaluable by this checker — it can only be scored once the ledger lands.
- **D3 — F4's second subclause is newline-sensitive in the pinned bytes.** In pass 1, the reverted
  F4 sentence (`... before instrument has no` / `in-bound 9-digit case`) fired only the first F4
  subclause under the pinned line-based bytes (n=1) and both subclauses under the flattened bytes
  (n=2). The id is `F4` either way; no mis-fire, but a one-line revert split across lines cannot
  green F4.
- **D4 — one id can carry two findings.** M2/R2 emits two F2 findings (hash mismatch + manifest not
  pinning the hash) and the pass-1 M4 emitted two F4 findings. "Exactly its own id" is satisfied at
  id-set level; the raw counts are recorded above so no reader takes "one finding" from this report.

## 7. Receipts

All under `.ufo/waves/round-96/w1/ExecControls/`:

- `mutate.py`, `run-matrix.py`, `run-matrix-r2.py`, `s5-rewrap.py` — the exact programs run.
- `receipts/mutations.log` — every applied edit, one-match asserts, before→after sha256.
- `receipts/matrix.json`, `receipts/matrix.stdout.txt` — pass 1, both binaries, argv per run,
  root-input hashes per root.
- `receipts/<root>.{current,frozen}.{json,stdout.txt}` — pass-1 runs (base, M1-M6, S1-S4).
- `receipts/matrix-r2.json`, `receipts/matrix-r2.stdout.txt`, `receipts/r2-*.{json,stdout.txt}` —
  pass 2, the authoritative runs.
- `receipts/selftest.{current,frozen}.txt` — `PASS 7/7`, exit 0.
- `receipts/S5.*`, `receipts/TM{1..6}.frozen.json` — wrap-only repair probe and its one-fault
  comparison under the pinned binary.
- `receipts/instruments-state.txt` — both tree states, all 17 manifest entries re-measured,
  checker-vs-pin equality, ledger presence, read-only `git status`.

## 8. Tooling record

No install or upgrade: Python 3.14.8 (system) sufficed; no pacman transaction; no `uv`/`npx`/
`~/.local/bin` write; nothing written under `tools/`, `corpus/`, `SCORECARD.md`, `LOG.md`,
`.ufo/plans/`, `.ufo/waves/round-96/before/`, `claims.json`, `.ufo/state/`, `.scratch/` or the fleet
repo. Scratch deleted before yield.

{"seat":"ExecControls","verdict":"findings","notes":"C2 one-fault controls pass on the landed tree with the freeze-pinned checker (7ff63524): clean 0 findings (PASS exit 0), R1-R6 each fail exactly F1/F2/F3/F4/F5/F6, selftest 7/7; the two named green-without-work probes still fail (U1 receipt-correct+SCORECARD-missing -> F2; U2/U3 report-vs-ledger mismatch -> F6 x2). Findings: (D1) pass-1 tree carried a post-freeze checker edit ad894667 vs pin 7ff63524 and the pinned bytes read F3 on the then-tree, repaired in-tree at 07:54:00 (checker=pin, make-r95-bends.py rewrapped to bbcb18f3, 17/17 manifest entries OK) - pass 2 measures the repaired tree; (D2) F6 has no ledger provenance binding: the r95 ledger copied at the r96 path with a report matching its 6/1 counts reads PASS (U4), and the r96 ledger is absent at measurement so C2's after-leg is not yet evaluable; (D3) F4's over-scope subclause is newline-sensitive under the pinned bytes; (D4) R2 emits two F2 findings and pass-1 M4 two F4, id sets still exact. Receipts under .ufo/waves/round-96/w1/ExecControls/receipts/."}
