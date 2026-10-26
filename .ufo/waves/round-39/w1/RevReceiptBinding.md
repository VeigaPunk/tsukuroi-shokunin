VERDICT: defect-found

Item R-10 (routed defect 5). Routed defect: `corpus/lessons/round-38-verifier-spotcheck.md:182` —
"**Receipt binding** (R38-STREAK-ATTRIBUTION, self-filed): before receipts and `controls.jsonl` carry no
`tool_sha256` or revision. Bind every receipt to tool bytes." This seat audited every receipt under
`.ufo/waves/round-39/before/`, `.ufo/waves/round-39/after/` and `.ufo/waves/round-39/controls/`.
Result: the five counter receipts and `controls.jsonl` are fully bound and every declared sha256 equals the
frozen bytes; **two receipt-class artifacts are unbound** (`before/sources-census-start.txt`,
`after/selftest-49cc53c.txt`).

## 1. Inventory and classification

All files under the three dirs (glob, this session):

| File | Class | Binding |
|---|---|---|
| `before/c1-before.jsonl` | run-receipt.py receipt | BOUND — verified |
| `before/c2-before.jsonl` | run-receipt.py receipt | BOUND — verified |
| `before/sources-census-start.txt` | tool-output capture (fleet `scripts/sources-census.sh`) | **UNBOUND** |
| `after/c1-after-49cc53c.jsonl` | run-receipt.py receipt | BOUND — verified |
| `after/c2-after-4078eb2.jsonl` | run-receipt.py receipt | BOUND — verified |
| `after/selftest-49cc53c.txt` | selftest receipt (census `--selftest`) | **UNBOUND** |
| `controls/controls.jsonl` | 12 control rows | BOUND — verified |
| `controls/run.out` | console copy | byte-identical to `controls.jsonl` (`cmp` → `IDENTICAL`), same bound content |
| `controls/run.err` | stderr log | empty (read, 0 bytes of content) |
| `controls/run-controls.sh`, `controls/c1_variant.py` | control scripts (inputs, not receipts) | n/a |
| `controls/c2-entries/{E1..E6}/{SOURCES.md,entry.md}` | control fixture inputs, not receipts | n/a |

Receipt format authority: `tools/run-receipt.py:13-17` (header carries `revision`, `tool_revision`, `tool`,
`tool_sha256`, `argv`); the hash is taken from the tool file checked out at `tool_revision`
(`tools/run-receipt.py:87` checkout, `:96-97` sha256, `:104-105` header). Item text: `.ufo/waves/round-39/w1-spec.json:675`.

## 2. Bound receipts — field-by-field

All four jsonl headers name both revisions and the tool digest (read `:raw:1-1` of each):

| Receipt | `revision` (lane rev under test) | `tool_revision` | `tool` | `tool_sha256` |
|---|---|---|---|---|
| `before/c1-before.jsonl:1` | `0eff65b21bb81195ee06c96a83afbd7a07e52eef` | `6a08925daa30767809eb13bb4b01448ff954d46a` | `tools/score-storage-hidden-r39.py` | `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973` |
| `before/c2-before.jsonl:1` | `0eff65b21bb81195ee06c96a83afbd7a07e52eef` | `6a08925daa30767809eb13bb4b01448ff954d46a` | `tools/check-transaction-order-r39.py` | `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e` |
| `after/c1-after-49cc53c.jsonl:1` | `49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82` | `6a08925daa30767809eb13bb4b01448ff954d46a` | `tools/score-storage-hidden-r39.py` | `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973` |
| `after/c2-after-4078eb2.jsonl:1` | `4078eb236c7c67f343c76956c587d0a356e0bf5c` | `6a08925daa30767809eb13bb4b01448ff954d46a` | `tools/check-transaction-order-r39.py` | `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e` |

Bodies match the declared before/after values: `before/c1-before.jsonl:8-13` hidden_matched 0, views 3,
fixtures 2, live 1, six_planes 1, FAIL; footer `:156` exit_code 1. `before/c2-before.jsonl:14-20` entry_present
false, rules 0, source_ok 0, counts_ok 0, FAIL; footer `:25` exit_code 1. `after/c1-after-49cc53c.jsonl:8-13`
hidden 2, views 3, fixtures 5, live 1, six_planes 1, PASS; footer `:156` exit_code 0.
`after/c2-after-4078eb2.jsonl:14-20,63` entry_present true, rules_verified 8, source_ok 1, counts_ok 2,
oracle_violations 0, PASS; footer `:66` exit_code 0. All match `SCORECARD.md:2220-2221` and the dispatch spec.

`controls.jsonl:1-12`: every row carries `counter`, `counter_sha256`, `revision`. The 5 C1 rows carry
`75a9e8ab…973`, the 7 C2 rows `f1c97836…91e`. `C1-K0`/`C2-K0` name revision `6a08925d…` (lane-resolvable);
the 10 variant rows name revisions that exist only in the discarded scratch clone (see §5).

## 3. sha256 equals the frozen bytes — the core check

Commands run against the lane's object database (read-only `git show`; observed outputs):

```
$ git show 6a08925daa30767809eb13bb4b01448ff954d46a:tools/score-storage-hidden-r39.py | sha256sum
75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973  -
$ git show 6a08925daa30767809eb13bb4b01448ff954d46a:tools/check-transaction-order-r39.py | sha256sum
f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e  -
$ sha256sum tools/score-storage-hidden-r39.py tools/check-transaction-order-r39.py   # working tree
75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973  tools/score-storage-hidden-r39.py
f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e  tools/check-transaction-order-r39.py
```

Machine-checked (receipt kept at `.ufo/waves/round-39/w1/RevReceiptBinding/binding-audit.json`):
`frozen_hashes_match_declaration`, `working_tree_equals_frozen`, `all_receipt_tool_sha256_equal_frozen` (4/4
headers), `all_control_counter_sha256_equal_frozen` (12/12 rows) — all true.

Cross-checks that close the loop:
- Declared pins: `SCORECARD.md:2220` (`75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`),
  `SCORECARD.md:2221` (`f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`); identical at the
  declaration commit (`git show 93fddb2c…:SCORECARD.md | grep -n '75a9e8ab\|f1c97836'` → lines 2220, 2221) and
  `git diff --stat 93fddb2c… -- SCORECARD.md` is empty (working tree == declaration commit).
- No counter drift freeze→tip: `git diff --stat 6a08925d… 2e1c2a40… -- tools/score-storage-hidden-r39.py
  tools/check-transaction-order-r39.py tools/run-receipt.py` → empty, exit 0.
- Receipt immutability: all three dirs are tracked lane content; `git status --porcelain` on them is empty;
  `git log --diff-filter=A` shows before/+controls/ added at `93fddb2c` ("round-39: declaration, before
  receipts and pre-seat controls") and after/ added at `2e1c2a40` ("round-39: author after receipts …");
  `git diff --stat 2e1c2a40… HEAD` on the three dirs is empty — audited bytes are the committed bytes.
- Revision resolution: `git cat-file --batch-check` over all 16 named revisions → the six round-level revs
  (base `0eff65b2`, freeze `6a08925d`, `49cc53c7`, `4078eb23`, tip `2e1c2a40`, decl `93fddb2c`) all `commit`;
  the ten control variant revs all `missing` (§5). Ancestry: `merge-base --is-ancestor` →
  base→freeze→49cc53c→4078eb2→tip all ancient; decl `93fddb2c` ancient to tip.
- Controls integrity by construction: `run-controls.sh:8-13` clones the lane, checks out master at the freeze,
  removes origin; `:33` hashes the counter file in that clone (`sha256sum "$D/$counter"`); `c1_variant.py`
  patches only `tools/tsukuroi-census.sh` (K1/K2/K3 string replaces; K4 copies the candidate) — the counter
  bytes in the clone are the freeze bytes, so `counter_sha256` is trustworthy.

## 4. Unbound receipts (the finding)

**U1. `.ufo/waves/round-39/before/sources-census-start.txt` — no revision, no tool sha256, no command line.**
35 lines: 33 `W04 … duplicate url … across scopes` warnings, one `ok` line, `exit=0` (read in full; `grep -c
W04` → 33). No header of any kind. Emitter identified by precedent: round-19's equivalent artifact records the
invocation `$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root … tsukuroi` and a
`lane tip:` line (`.ufo/waves/round-19/measure/census-start.txt:2,13`) — the round-39 copy dropped both, so the
lane state the census describes is inference, not binding. The emitter is a fleet-level script outside the
lane, so `run-receipt.py` cannot wrap it (it requires the tool to be a tracked lane file,
`tools/run-receipt.py:90-93`). Added in the freeze commit `6a08925d` (`git log --diff-filter=A`).

**U2. `.ufo/waves/round-39/after/selftest-49cc53c.txt` — no revision field in content, no tool sha256.**
Exactly 1 line: `TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)`. The only revision hint is
the 7-hex short hash in the filename. Emitter: `tools/tsukuroi-census.sh:3001-3003` (the `--selftest` summary
printf; usage `:561-567`, `run_selftest` `:1923`). This is a direct recurrence of a routed defect class the
lane already fixed twice: round-29 routed item 1 demanded "a revision field in selftest receipts"
(`SCORECARD.md:1153`), and round 30's outcome states "every receipt header names the revision and tool digest"
via `tools/run-receipt.py` (`SCORECARD.md:1157`). The counter does not run the selftest (no `selftest` match in
`tools/score-storage-hidden-r39.py`), so this file is the only evidence of the 117-case selftest run and it
binds neither the census bytes it exercised nor the revision.

Both files sit in the receipt directories and document tool runs; under routed defect 5's own language
("Bind every receipt to tool bytes") they are unbound receipts. Neither unbinds the five counter receipts or
`controls.jsonl`, which are the files the round-38 routing named by name.

## 5. Residual risk / verification gaps

- 10 of 12 `controls.jsonl` rows name revisions that resolve only in the discarded scratch clone
  (`cat-file --batch-check` → `missing`; by design, `run-controls.sh:8-13`, "scratch clone with origin
  removed", `SCORECARD.md:2223-2224`). Their `counter_sha256` binds the counter, and the variant definitions
  survive in `controls/c1_variant.py` + `controls/c2-entries/`, so the controls are re-runnable — but the
  named variant revision hashes themselves are unverifiable in the lane. Accepted form per the item
  ("the controls' counter_sha256 field"); noted as a verifiability limit, not counted as unbound.
- Not done (binding audit only): I did not re-run either counter or the census selftest, did not judge any
  TO row (no `TO<n>` lines — not a TO-judging seat), did not verify `.ufo/waves/round-39/frozen/src/SHA256SUMS`
  or the txcapture MANIFEST pin `cb5cb4f4…` (outside the three named dirs), and did not audit the counters'
  internal logic.
- Timeline context (not a defect): before receipts 05:47–05:48Z, after receipts 05:59–06:00Z, declaration
  commit 06:20Z — the declaration documents runs it postdates; "before any seat" refers to wave-1 L2 seats.

## 6. Proposed remediation (proposal only; this seat is read-only)

- U2: re-issue the selftest receipt through the lane's own binder, e.g.
  `python3 tools/run-receipt.py --revision 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82 --tool-revision 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82 --out .ufo/waves/round-39/after/selftest-49cc53c.jsonl -- tools/tsukuroi-census.sh --selftest`
  (header then names revision + census-script digest), and drop or mark the bare `.txt` as superseded.
- U1: prepend a binding line naming the exact command, the lane revision measured, and the fleet script's
  sha256 (run-receipt.py cannot wrap a fleet-level tool); or move the capture under a run-receipt receipt that
  records it as argv output.

## Tooling record

No tool installed or upgraded (none needed); no host mutation; no sudo; no pacman transaction. Scratch
`/fast/scratch/hyaku/tsukuroi-r39/RevReceiptBinding/` was created and removed empty at finish; kept receipt:
`.ufo/waves/round-39/w1/RevReceiptBinding/binding-audit.json`.
