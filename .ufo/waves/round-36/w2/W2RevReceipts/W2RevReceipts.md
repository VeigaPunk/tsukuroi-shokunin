# W2RevReceipts — receipt conformance sweep (round 36, wave 2)

Written 2026-10-24T04:38:33Z, counts re-based 04:40:01Z from `date -u +%H:%M:%SZ`. Lane `tsukuroi-shokunin`, HEAD
detached at `c052bb7d41ced49aa888817069afd804eccfecf1` (master `8d5fa7fe27c336d602a463519e839e932d26301d`
is the wave-2-spec child; `git ls-files` therefore reflects the change commit). Sweep run
2026-10-24T04:39:16Z (`receipts-sweep.json` → `summary.generated_utc`); an earlier sweep at
04:36:58Z read 77 files / 16 conformant, the drift being wave-2 seats writing while this seat
ran (W2LiveOracle, W2MutAttrgetter, W2MutPathCopy, W2MutTool4/6 appeared between the two).
Every number below is the 04:39:16Z sweep; the raw per-file rows are in `receipts-sweep.json`
/ `receipts-sweep.jsonl`.

## 1. Canonical shape used (tools/run-receipt.py, QUALITY 77)

Header (first line): `{"receipt":1,"revision","tool_revision","tool","lane_branches","tool_sha256","argv","started_utc"}`
— `revision` names the cited hash, `tool_sha256` is the digest of the exact bytes that ran,
`tool_revision` names the revision those bytes came from.
Footer (last line): `{"receipt_end":1,"exit_code","timed_out","stderr_tail","finished_utc"}`.
The tool's stdout sits between the two lines. Source: `tools/run-receipt.py:15-18,112-117`.

The ticket's shape rule (revision ∈ {`6d76fb20…`, `1e926801195e…`, `c052bb7d41ce…`}, tool sha256
in the header, footer exit_code) is the same predicate restricted to this round.

## 2. Counts (82 `*.jsonl` under `.ufo/waves/round-36/`, own seat excluded)

| bucket | files | header+footer conformant |
|---|---:|---:|
| **committed (tracked)** — `l1/` | **6** | **0** |
| untracked — `w1/ExecGateBaselines` | 7 | 7 |
| untracked — `w1/ExecBeforeDesign` | 1 | 1 |
| untracked — `w1/ExecLiveViewDesign` | 2 | 1 |
| untracked — `w1/MutProbeDraft` | 44 | 0 |
| untracked — `w2/` seat outputs | 22 | 8 |
| **total** | **82** | **17** |

- Conformant and committed: **0 of 17**. Every conformant receipt is untracked seat output.
- Committed non-conformant: **6 of 6** — the entire `l1/` set committed by the freeze commit
  `1e926801195e304950e3eb9d2525ef8bbc245089`.
- Non-conformant total: 65 (6 tracked, 59 untracked).
- Footer exit tally over the 17 conformant: `0` ×12, `1` ×5. Header revisions: 9 ×
  `6d76fb20…`, 8 × `c052bb7…`. No header cites `1e926801…` (the freeze commit is cited by no
  receipt at all).
- Digest check: 17/17 conformant receipts' `tool_sha256` equals
  `sha256(git cat-file blob <tool_revision>:<tool>)` — 0 mismatches, 0 uncheckable.

## 3. Findings (severity order)

### F1 — HIGH: the six committed claim receipts violate the receipt shape; the claimed "exit 0" is recorded nowhere

Tracked files (all committed in the freeze commit, `git ls-files`):

```
.ufo/waves/round-36/l1/dev-claim-final.jsonl
.ufo/waves/round-36/l1/dev-r33claim-final.jsonl
.ufo/waves/round-36/l1/dev-r33claim-final2.jsonl
.ufo/waves/round-36/l1/dev-r33claim-final3.jsonl
.ufo/waves/round-36/l1/dev-r33claim-final4.jsonl
.ufo/waves/round-36/l1/sens-mutattr.jsonl
```

Each is bare probe stdout: no `receipt`, `revision`, `tool`, `tool_revision`, `tool_sha256`
header; no `receipt_end`, `exit_code` footer (`receipts-sweep.json`, rows with `tracked=true,
header_ok=false, footer_ok=false`). The probe's own summary line carries `revision` and
`probe_sha256` (e.g. `dev-claim-final.jsonl` last line: `revision 6d76fb20…`, `probe_sha256
a2a5acac…`, `leaking 0`, `harness_errors []`) but no process status. `dev-r33claim-final.err`
is empty; no `.exit`/rc file exists beside them.

Consequence: `LOG.md:1377` states "dev-claim-final.jsonl (claim set at 6d76fb20: leaking 0,
harness_errors [], **exit 0**)" and the same for `dev-r33claim-final4.jsonl`. The exit code is
a stated result with no receipt field — the exact R30-UNRECEIPTED-GATES class QUALITY 77 was
written for. The probe's exit convention (`tools/probe-child-env-allowlist-r36.py:1275-1277`:
2 on harness errors, 1 on leaking, 0 clean) means a bare last line cannot distinguish
"leaking 0, exit 0" from "leaking 0, exit 2 on a harness error".

Related, same class: the receipts cite `revision: 6d76fb20…` while the probe bytes they name
(`sha256 a2a5acac…`) do not exist at `6d76fb20` — `git cat-file -e 6d76fb20:tools/probe-child-env-allowlist-r36.py`
fails; the bytes first appear in `1e926801195e…` (`sha256 a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a`
at both `1e926801` and `c052bb7d`). Without a `tool_revision` field a reader cannot tell the
scored base from the bytes' revision — which is what the header's two revision fields exist to
separate. The probe's `revision` argument is the scored target, so this is not a false claim,
but it is an unrecorded distinction in a receipt whose whole purpose is that distinction.

### F2 — HIGH: six receipts cite revisions absent from the lane; all are sandbox mutant commits, and the committed one does not identify its mutant

`git cat-file -e <rev>^{commit}` fails for every one of these (sweep `absent_revs`):

| receipt | cited `revision` | `base` field |
|---|---|---|
| `.ufo/waves/round-36/l1/sens-mutattr.jsonl` (committed) | `f84d4bd9b7fbf15aa4d1838c5b6486006912f0d8` | `6d76fb20…` ok |
| `.ufo/waves/round-36/w2/W2MutTool2/probe-mutant.jsonl` | `25d958ac77adc47b772c0e018c906e2473d059e1` | `c052bb7d…` ok |
| `.ufo/waves/round-36/w2/W2MutTool4/probe-m4.jsonl` | `7b945d5bef23c33b74dfb2acb1e61d8a6736f69e` | `6d76fb20…` ok |
| `.ufo/waves/round-36/w2/W2MutTool5/m5-mutant-probe.jsonl` | `1abff51d4c141d5d528578f2fc5ca25aeab3a6a0` | `6d76fb20…` ok |
| `.ufo/waves/round-36/w2/W2MutAttrgetter/probe-claim-mutant.jsonl` | `b73c2b390b9bb8c5c2d6ad8564ab04c2da2086bf` | `6d76fb20…` ok |
| `.ufo/waves/round-36/w2/W2MutPathCopy/probe-mutant.jsonl` | `763e46b98c98deb7745daf92f2e7147ce14b4c58` | `6d76fb20…` ok |

For a mutant clone the named revision is absent *by construction*; that is admissible only if
the receipt carries the mutant's identity so the run is reproducible from in-lane bytes.
`w2/W2MutTool1` does this (`mutant-1.diff`, `mutant.commit.txt`, `mutant.sha`); `W2MutTool2`
has `mutant-2.diff`; `W2MutTool4/5/6` and `W2MutAttrgetter`/`W2MutPathCopy` had no diff artifact
at sweep time. The committed `sens-mutattr.jsonl` does not: its five JSONL lines name
`tools/check-section-citations.py` and the scratch path `/tmp/r36-mutattr-run/sf5ee873e2c0f-…`,
but no diff, no mutant digest, and the scratch directory is gone (`/tmp/r36-mutattr-run` now
empty). The committed receipt for the MutAttrgetterCopy sensitivity conjunct is therefore
**unreproducible and revision-absent**.

### F3 — HIGH (claim integrity): the committed sensitivity receipt reads 0, and the claim requires it above 0

`sens-mutattr.jsonl` summary: `{"revision": "f84d4bd9…", "targets": 1, "target_set": "claim",
"pairs": 4, "leaking": 0, "leaking_pairs": [], "harness_errors": []}`. The C1 claim as
assigned states "sensitivity conjuncts: MutAttrgetterCopy/MutPathCopy mutants each read above
0". `LOG.md:1377` discloses the gap honestly — "MutAttrgetterCopy reads 0 under the frozen
probe's claim-set invocation because that tool's --selftest spawns children through a separate
already-fixed sandbox_git and never exercises the mutated git() — an invocation-coverage gap …
wave 2 scores it through the live mode." So at freeze the conjunct was not green; the only
committed evidence for it reads 0. The declaration's own kill rule
(SCORECARD.md round-36 corrections item 9) says "OR any sensitivity conjunct fails
(MutAttrgetterCopy and MutPathCopy each read above 0) … C1 is reported not verified." The
conjunct needs a wave-2 receipt with `leaking > 0` on the mutant; as of the sweep the
`W2MutAttrgetter/probe-claim-mutant.jsonl` exists but has no header/footer (and cites an absent
revision), so it does not close the conjunct under QUALITY 77 either.

### F4 — HIGH (regression, not shape): the change commit turns `check-registry-coverage` red

`w2/W2ExecGates/quality-77-check-registry-coverage.jsonl` is a *conformant* receipt at
`c052bb7d…` with `exit_code 1` and body
`{"branch":"master","branch_tip":"8d5fa7fe…","counts":{"findings":51,"missing":51,"registered":2,"rows_total":2,"tools_total":53}}`.
The same gate read 52/52 exit 0 at `6d76fb20…`
(`w1/ExecGateBaselines/check-registry-coverage.jsonl`, digest `6fcb2d0a…`), and the tool bytes
are byte-identical at both revisions (`sha256 6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812`
at `6d76fb20` and `c052bb7`). Cause: `tools/check-registry-coverage.py:194-211` selects the
single highest-numbered `Gate and probe registry` heading; the change commit adds
`SKILL.md:3050 "## Gate and probe registry — round36 superseding current rows"` holding only
the probe row and the `host-census` row (2 rows). The prose says the round-35 rows are
"retained verbatim", but they are not in the operative section, so the gate sees 2 of 53 and
reports 51 missing. This is a no-harm/gate regression introduced by the change commit's
"registry table" item — an L1 adjudication item, not a receipt-shape item. (Receipt is
untracked wave-2 seat output, stamped 04:34:58Z.)

Inherited reds at the same revision, correctly receipted: `check-pause-gate` exit 1
(P3 unverified, present at `6d76fb20` too) and `check-self-assessment` exit 1 (K10, 46 vs 47,
also present at `6d76fb20`). The registry red is the only *new* one.

### F5 — MEDIUM: 59 untracked non-conformant measurement outputs; the `w1/MutProbeDraft` set also cites an off-set base

`w1/MutProbeDraft` (44 files) and `w1/ExecLiveViewDesign/.../dev-run.jsonl` are bare probe /
runner stdout: no header, no footer. Ten of them (the `clean-*`, `FINAL-clean`, `r33-*` set)
carry `base: 2641591e303057cd0f67e190a6bdf7fa91a45c31` — resolvable in the lane
(`round-33 verifier spot-check`) but outside the three round-36 receipt revisions; one more
(`w2/W2MutPathCopy/probe-baseline.jsonl`) carries `revision: df661507db26e596f3813d9d54283b593f71b49a`,
the in-lane round-34 C1 change commit, again outside the round-36 set. These are
development output (QUALITY 73); the risk is only that a wholesale `git add .ufo/waves/round-36`
by the L1 would commit 59 more non-conformant "receipts" into the evidence set with no label
distinguishing them from admissible ones. Their `probe_sha256` values (`52c5f462…`, `544c5ded…`,
`0865d8a1…`, `6ec9af2d…`) are pre-freeze draft bytes, not the frozen `a2a5acac…`; that is
consistent with the declaration's draft labelling.

### F6 — MEDIUM (dependency/current state): no livefive receipt exists, and the only livefive exit record is a crashed run

The claim's measure is `--set livefive` with `leaking 0`, `harness_errors []`, **exit 0**. At
sweep time no `livefive` receipt exists (committed or untracked) with a footer. The only
livefive exit record is `.ufo/waves/round-36/w2/W2ReBefore/livefive.exit` = `1`, and its
`livefive.stdout` is an uncaught traceback:

```
RuntimeError: cannot create local master branch   (tools/probe-child-env-allowlist-r36.py:499, via run_target:1137)
```

Under the probe's exit convention that is neither `leaking` nor a recorded `harness_errors`
entry — the harness died before the summary line. Whether the after-state battery can run at
all is therefore open; the claim's after-value has no supporting artifact yet. Recorded as a
dependency on wave-2 seats, not as evidence the claim is false. `w2/W2LiveOracle`'s
`exitcodes.tsv` at sweep time held only `binding 0`, `receipts 0` — no livefive line; its one
conformant receipt is `check-report-receipts` (`capture/quality82-liveview-c052-W2LiveOracle/run-receipt.receipt.jsonl`,
exit 0, `c052bb7d…`), not a livefive measure.

### F7 — LOW (positive control, recorded so the sweep is falsifiable)

The seven `w1/ExecGateBaselines` receipts and their report agree exactly: report row exit
codes and tool sha256s equal the receipt headers 7/7 (`check-self-assessment` 1,
`check-registry-coverage` 0, `check-knowledge-header` 0, `check-recheck-commands` 0,
`check-adjacency-anchors` 0, `report-red-causes` 0, `check-pause-gate` 1), and
`ExecGateBaselines.md:19`'s "5 exit 0, 2 exit 1" matches. This is the shape that satisfies
QUALITY 77; the claim receipts should be re-issued this way (header + stdout + footer) rather
than as bare probe stdout.

## 4. Revision admissibility summary

- Revisions cited in receipt headers: 100% inside the round-36 set — 9 × `6d76fb20…`,
  8 × `c052bb7d…`. None cites `1e926801…`; the freeze commit is receipt-less.
- Revisions cited outside headers: in-lane but off-set: `2641591e…` (a `base` field, 10 records)
  and `df661507…` (a round-34 `revision` field, 1 record); six absent from the lane (table in F2), of which one is committed
  (`sens-mutattr.jsonl`) and four are untracked wave-2 mutant probes.
- No receipt cites a fork/foreign-lane revision. No 40-hex token in any round-36 JSONL fails
  to resolve except the six mutant commits above (scan of every `[0-9a-f]{40}` token, not only
  `revision` keys).

## 5. Residual risk and verification gaps

- **Volatility**: wave 2 was mid-flight. Files appearing after 04:39:16Z are not in this
  sweep; the JSONL is the frozen list, and the 04:36:58Z → 04:39:16Z drift (77 → 82 files,
  16 → 17 conformant) is recorded so the count is not read as final.
- **No gate/measurement receipt is committed at `c052bb7d…`** except the untracked
  `w2/W2ExecGates` set; the declaration's "gates at the change commit's first run" rests on
  uncommitted seat output at sweep time. Until the L1 commits them, the statement has no
  committed receipt.
- **Method limit**: shape, revisions and digests were checked mechanically from the lane's own
  git objects. I did not re-run any tool, did not mutate the lane, and did not use an LSP
  server (no source-server question was in scope; all checks are artifact/serialization
  checks). The one non-shape finding (F4) was confirmed by reading the gate's selection rule
  (`tools/check-registry-coverage.py:194-211`) and `SKILL.md:3050-3072`, not by re-executing
  the gate — it rests on the peer receipt's exit 1 plus the identical tool digest at both
  revisions.
- `sens-mutattr.jsonl`'s scratch (`/tmp/r36-mutattr-run/…`) is deleted, so the cited mutant
  cannot be recovered from the host; only a new wave-2 mutant receipt can close F2/F3.
- No tool installs or upgrades were made (python3, git read-only only).

## 6. Artifacts

- `check_receipts.py` — the sweep (re-runnable; read-only).
- `receipts-sweep.json`, `receipts-sweep.jsonl` — machine evidence, one row per file with
  `header_ok`, `footer_ok`, `tracked`, `revision`, `tool`, `tool_sha256`,
  `tool_sha256_matches_blob`, `exit_code`, `rev_citations`, `rev_states`, `absent_revs`.

Report: `.ufo/waves/round-36/w2/W2RevReceipts/receipts-review.md`
