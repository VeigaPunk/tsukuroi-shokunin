# VERSION 3 pacnew counter requirements for any future re-claim

**Status:** requirements only; this seat did not implement or score VERSION 3. Round 36 explicitly says the pacnew VERSION 3 counter is not owed: no pacnew claim is made or re-claimed this round. These are freeze conditions for a later claim, not evidence that any condition is already met.

The V2 outcome is not a re-claim basis: the round-35 lesson records that W2TreeKeyed and W2LogKeyed each scored 24/24; W2LiveOracle later produced two additional 24/24 live-gate controls. The lesson says C1 is not verified and no VERSION 3 was made. See `corpus/lessons/round-35.md:36,44,64` and `SCORECARD.md:1673-1677`.

## Must-pass claim and receipt gate

Before any future data scoring, freeze the complete V3 counter, predicate, fixtures/generator, should-fail set and decision rule. Do not revise them after scoring begins. A re-claim requires a committed, full V3 receipt with the frozen 24-view after-value (`candidate_matches=24`, `of=24`), `control_matches=24`, `should_fail_accepted=0` over the explicitly enumerated battery, empty `harness_errors`, and exit 0. Record the should-fail denominator and every per-view result; a zero accepted count with missing rows or a failed/missing live row is not a pass. Any skipped-work control meeting the after-value, or any should-fail acceptance, kills the re-claim. Preserve the V2 rule's sole named limit only if explicitly frozen: a census identifying the namespace from its own `uid_map`, `mountinfo`, or `/etc` mount is reported as reaching that limit, not as a kill. Any change to that exception must be declared before data scoring.

**Evidence:** V2’s frozen kill rule is in `SCORECARD.md:1536-1538`; V2's before receipt is `.ufo/waves/round-35/w2/W2BeforeBattery/before-battery-7186722b.jsonl`. The V2 after-value and kill-rule failure are summarized in `SCORECARD.md:1553-1556` and `corpus/lessons/round-35.md:36,64`.

## Required V3 properties

### 1. Remove fixed-count forced-shape labels

For every forced fixture-shape category, draw its multiplicity from a range whose support includes **0 and at least 2** (with 1 also possible); do not contribute a hard-coded per-fixture constant. This includes the forced non-regular tree entries (the `.pacnew` symlink, `.pacsave` symlink, dangling `.pacorig` symlink and `.pacnew` FIFO), and the forced collision/directory-target structures. Apply the same rule to forced log-event roles: in particular, do not always put one qualifying warning first and then append an identifying filler suffix. Retain generator evidence showing each category can occur at 0 and 2+ across cases, while still checking oracle values for every generated case.

**Evidence:** R35-V2-FORCED-SHAPE-CONSTANTS, `corpus/lessons/round-35.md:44`; W2TreeKeyed's four fixed non-regular contributions and forced tree patterns, `.ufo/waves/round-35/w2/W2TreeKeyed.md:3,32,40` and its 24/24 receipt `.ufo/waves/round-35/w2/W2TreeKeyed/variant.jsonl`; W2LogKeyed's fixed first event and filler layout, `.ufo/waves/round-35/w2/W2LogKeyed.md:3,34-36` and its 24/24 receipt `.ufo/waves/round-35/w2/W2LogKeyed/variant.jsonl`.

### 2. Add the four surviving census patches to the should-fail battery

Retain and score each exact saved patch as a separate should-fail entry, not a reconstructed approximation:

1. `W2TreeKeyed/variant.patch` — tree-shape key plus constant contributions.
2. `W2LogKeyed/variant.patch` — first-warning gate and 44-line prefix.
3. `W2LiveOracle/livecache-variant.patch` — host `/etc/pacman.conf` gate and cached live totals.
4. `W2LiveOracle/cwdgate-variant.patch` — `$PWD/pacman.log` gate and cached live totals.

Each must be refused by the V3 battery, with no acceptance. The livecache and cwdgate cases must be rejected by live-view evidence, not merely by a namespace/stub failure. Do not accept a battery result whose live row was skipped. Keep the prior should-fail battery arms; record the new total denominator explicitly.

**Evidence:** `.ufo/waves/round-35/w2/W2TreeKeyed/variant.jsonl` and `variant.patch`; `.ufo/waves/round-35/w2/W2LogKeyed/variant.jsonl` and `variant.patch`; `.ufo/waves/round-35/w2/W2LiveOracle/livecache-variant.jsonl`, `livecache-variant.patch`, `cwdgate-variant.jsonl`, and `cwdgate-variant.patch`. Each live-gate receipt reports 24/24 with empty harness errors and exit 0 (`W2LiveOracle.md:80-98`).

### 3. Make the ctime guard independently observable and mutation-sensitive

The fixture-integrity predicate must cover the full tree and log, including paths, bytes, modes, symlink targets and inode change times. It must observe ctimes of descendants inside unreadable directories as well as the locked directory itself; restoring bytes and mode must not hide a child ctime change. Include a chmod/restore fixture that changes ctime while preserving the visible byte/mode state. In the counter-mutation sensitivity suite, dropping the ctime comparison must be detected by the ctime witness itself: do not let an unrelated missing-DRIFT-line or failed-live path mask the lost guard. Require a retained result demonstrating that the drop-ctime counter mutant is killed.

**Evidence:** `.ufo/waves/round-35/w2/W2MutCounter/drop-ctime.jsonl` records the V2 counter mutation surviving (23 synthetic accepts; `should_fail_accepted=0`; live then fails for `drift_lines=0`). `.ufo/waves/round-35/w2/W2ArmAuditB/assigned-battery-summary.json:120-151` records F14 chmod/restore changing unreadable-directory ctimes and being refused as fixture-mutated. The unobserved locked-child ctime gap is the static review finding in `.ufo/waves/round-35/w2/W2RevCounterV2.md:5` (no dedicated child-ctime runtime receipt was produced).

### 4. Treat the live view as a real integrity and computation check

The live-view unchanged predicate must compare a complete pre/post snapshot of the live tree and log (including unrelated files, bytes, modes and ctimes), not merely equality of the eight oracle totals. Require a present, validated live result row on every score. Add both counter mutations to sensitivity testing: dropping the live execution/judgment must not earn a match, and dropping the ctime guard must not be masked by the live path. The live gate patches in requirement 2 must fail even when ordinary host contents or the scorer's working directory distinguish the live view. Prove this using a controlled live-equivalent view that does not write to the real host; a constant cached from the current host is not a live-computation test.

**Evidence:** `.ufo/waves/round-35/w2/W2MutCounter/skip-live-view.jsonl:439-441` shows the omitted live view had no row yet escaped the declared battery acceptance count; `.ufo/waves/round-35/w2/W2MutCounter/drop-ctime.jsonl:436,455,459` shows its live failure masking the ctime survivor. `.ufo/waves/round-35/w2/W2RevCounterV2.md:3` identifies count-only live integrity; `.ufo/waves/round-35/w2/W2LiveOracle.md:82-104` explains why both cached controls evade V2. Live write behavior was not exercised in these read-only reviews; V3 must supply safe controlled-view evidence.

### 5. Prevent malformed-DRIFT-token exfiltration through parser errors and receipts

Never interpolate a candidate-controlled field value into a parse reason, JSON row, scorer output or `run-receipt.py` receipt. Malformed values must produce a fixed, non-sensitive error code/message (the field name may be reported, but not its raw value). Add a committed adversarial receipt using a synthetic canary token, and demonstrate that the token is absent from all scorer stdout, JSON reasons and final receipt bytes while the malformed row is rejected. Do not read or use real host credentials as a test payload.

**Evidence:** `.ufo/waves/round-35/w2/W2SentinelViews.md:5` and `.ufo/waves/round-35/w2/W2ArmAuditB/counter-v2.py.txt:400-401` identify the raw value interpolation; the report notes `run-receipt.py` persists scorer stdout verbatim. **Gap:** this was a code-path inference, not a reproduced exfiltration; no malformed-token/canary receipt is retained. The V3 canary receipt is required evidence, not a claim that a leak was measured.

### 6. Repair the F04/F07 battery entries into isolated one-bend tests

- **F04-basename-pair:** the should-fail mutant must change only full-path pairing to basename pairing. Its witness must show that same-basename paths in different directories are incorrectly joined, while a valid top-level `/etc/name` event is still counted and a `prefixname.pacnew` suffix lookalike is not accepted. Do not credit the V2 F04 result as a clean kill: it rejects valid top-level inputs and also has a suffix-regex false positive.
- **F07-dangling-symlinks-only:** the should-fail mutant must isolate omission of non-dangling symlinks without also dropping FIFOs or other non-directory special entries. Include independent witnesses for the symlink bend and preservation of the forced FIFO. Do not credit the V2 F07 result as an isolated kill: its `-type f -o -xtype l` replacement loses the FIFO too.

Both must be represented in the V3 battery with complete fields and the intended semantic refusal, not syntax/exit/missing-line failure.

**Evidence:** F04 contamination and witness outputs are `.ufo/waves/round-35/w2/W2ArmAuditA.md:11-12`, `.ufo/waves/round-35/w2/W2ArmAuditA/probe-mutated.jsonl`, `base-top-level-valid.json`, and `base-suffix-not-basename.json`; the full battery rows are `.ufo/waves/round-35/l1/dev-v2-run2-base.jsonl:7,45,102,121,178,254,311,349,368,406`. F07's collateral FIFO loss is `.ufo/waves/round-35/w2/W2ArmAuditA.md:17` and `.ufo/waves/round-35/l1/dev-v2-run2-base.jsonl:10-11`.

### 7. Resolve and receipt all eight control/oracle disagreement classes

Before using the shell control as a control oracle, pin explicit expected values for each class below and make the control and independent oracle agree with the declared contract. If a class is intentionally outside scope, declare and justify that boundary before scoring; do not silently use a known-disagreeing control as a positive control. Retain a per-class receipt with both outputs and the rationale for the selected contract.

| # | Input class | V2 disagreement recorded | Retained evidence |
|---|---|---|---|
| 1 | Mode-000 unreadable directory named `can't-read`, with a valid logged descendant | oracle `unreadable=1,gone=0`; control `unreadable=1,gone=1` | `.ufo/waves/round-35/w2/W2ArmAuditB/unreadable-diagnostics.json:3-18`; `W2ArmAuditB.md:23` |
| 2 | Mode-000 unreadable directory with special characters and trailing backslash (`a*[b]?#\\`) | oracle `unreadable=1,gone=0`; control `unreadable=1,gone=1` | `.ufo/waves/round-35/w2/W2ArmAuditB/control-oracle-special-locked-name.json:22-50`; `unreadable-diagnostics.json:21-36` |
| 3 | Existing pathname contains literal separator phrase ` installed as ` | oracle `log_pacnew=0,gone=0`; control `log_pacnew=1,gone=1` | `.ufo/waves/round-35/w2/W2ArmAuditB/custom-initial-console.txt:7`; `W2ArmAuditB.md:25` |
| 4 | Existing pathname contains literal separator phrase ` saved as ` | oracle `log_pacsave=0,gone=0`; control `log_pacsave=1,gone=1` | `.ufo/waves/round-35/w2/W2ArmAuditB/custom-initial-console.txt:8`; `W2ArmAuditB.md:25` |
| 5 | ETC seam root has trailing slash | oracle `unlogged=0,gone=0`; control `unlogged=1,gone=1` | `.ufo/waves/round-35/w2/W2ArmAuditB/custom-initial-console.txt:9`; `W2ArmAuditB.md:27` |
| 6 | ETC seam root is a symlink | oracle `pacnew=1,gone=0`; control `pacnew=0,gone=1` | `.ufo/waves/round-35/w2/W2ArmAuditB/custom-initial-console.txt:10`; `W2ArmAuditB.md:27` |
| 7 | CRLF log line | oracle `log_pacnew=1,unlogged=0`; control `log_pacnew=0,unlogged=1` | `.ufo/waves/round-35/w2/W2ArmAuditB/control-oracle-input-classes-continued.json:4-53`; `W2ArmAuditB.md:29` |
| 8 | Synthetic paired warning whose source is exactly `/etc/` | oracle `log_pacnew=1,gone=1`; control `log_pacnew=0,gone=0` | `.ufo/waves/round-35/w2/W2ArmAuditB/control-oracle-input-classes-continued.json:109-156`; `W2ArmAuditB.md:29` |

These are eight completed disagreement classes, not eight successful V2 checks. The input-class JSON records are marked `development_only`; they are retained evidence of disagreement, not a re-claim receipt. V3 needs its own frozen expected-value receipts.

### 8. Make generated forced paths collision-safe

Randomized shape multiplicities must not turn a collision into a missing shape or harness error. Use unique/checked destinations or retry, then assert each requested shape exists with the intended type and count before scoring. A zero-count shape must construct cleanly; multi-instance cases must not overwrite or collide. Reject the fixture as a harness error if its declared shape inventory does not match reality.

**Evidence:** `.ufo/waves/round-35/w2/W2RevCounterV2.md:7` identifies silent `write()` collisions and unguarded forced constructors; the review explicitly says this was a static risk and generated no fixture. W2TreeKeyed's fixed forced shapes and score are retained at `.ufo/waves/round-35/w2/W2TreeKeyed.md:3,32` and `W2TreeKeyed/variant.jsonl`. **Gap:** no collision reproduction receipt exists.

### 9. Keep error receipts schema-stable (low-priority review debt)

Preflight failures should retain the normal summary keys (`candidate_matches`, `of`, battery fields where applicable) alongside `harness_errors` and `exit_code`; consumers must be able to distinguish failure without special-case parsing. This is lower priority than the false-acceptance, integrity, oracle and disclosure gates above.

**Evidence:** `.ufo/waves/round-35/w2/W2RevCounterV2.md:9` (static review; no dedicated preflight-error receipt).

## Evidence limits to carry forward

- The V2 tree/log/live-gate scores are direct committed receipts; they establish surviving controls, not V3 success.
- The ctime drop and live-view omission are direct mutation receipts; the locked-descendant ctime gap and live count-only integrity defect are static review findings and still need safe V3 tests.
- The malformed-token leak is an `[inf]` code-path finding; no canary/exfiltration receipt exists. No real credential bytes were read or copied here.
- The F04/F07 full-battery rows and the eight class captures establish contaminated battery behavior and control/oracle disagreements. They do not establish that V3 has repaired them.
- Collision and preflight-schema concerns are static findings without direct runtime receipts.
