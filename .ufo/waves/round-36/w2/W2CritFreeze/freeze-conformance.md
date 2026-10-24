# Freeze conformance — W2CritFreeze

Axes: **operability, C1, freeze**. This is a bounded conformance review, not a canonical claim judgment.

## Verdicts

| Requirement | Verdict | Evidence |
|---|---|---|
| Freeze probe bytes have the declared SHA-256 | **PASS** | `git show 1e926801195e304950e3eb9d2525ef8bbc245089:tools/probe-child-env-allowlist-r36.py \| sha256sum` returned `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a`. |
| Probe unchanged from freeze to change | **PASS** | The requested path-restricted diff was empty. Repeating it with `--exit-code` returned zero. The change-commit blob independently hashes to the same SHA-256. Therefore its executable counter, `PREDICATE`, label, target sets and acceptance calculation did not change in this interval. |
| LOG-named final base controls name the frozen bytes | **PASS, bounded** | `l1/dev-claim-final.jsonl:37` and `l1/dev-r33claim-final4.jsonl:21` both name that exact hash, VERSION 7 and label `leaking`; their summaries have `leaking: 0`, empty leak/error lists. Both are committed at freeze. |
| Every retained development/control result was produced by the frozen bytes | **FAIL if stated universally** | Three retained r33 development summaries name two older hashes, not the frozen hash. They are distinguishable development records, not interchangeable final-byte evidence. Details below. |
| A complete final-byte before/sensitivity battery was committed before the change | **NOT ESTABLISHED** | Freeze L1 contains only the two final zero-base summaries, three earlier r33 development summaries and a zero-leak MutAttrgetter summary. No final-byte all-five `livefive` before, `regression` zero-base, positive MutPathCopy or live-view-before result was found there; wave-1 JSON/JSONL search found no frozen-hash receipt. LOG itself defers sensitivity/live-view evidence to wave 2. |
| Committed kill rule and declaration named limit unchanged after controls scored | **FAIL: documentary freeze** | `SCORECARD.md` is byte-identical between declaration and freeze. The entire “pre-freeze corrections” block, including the restated kill rule and declaration named limit, first enters history in **the change commit**, after the freeze already contains scored controls. |
| Named-limit text inside the probe unchanged between freeze and change | **PASS** | Covered by full probe-byte identity. The issue is its absent/different declaration authority at freeze, not a post-freeze executable edit. |

**Overall:** executable-byte freeze passes; the stronger declaration/receipt freeze is **not conformant as recorded**. No canonical C1 admission/rejection is performed here.

## F1 — strongest counterexample: the “pre-freeze” correction is post-freeze in Git

Observed committed `SCORECARD.md` object identities:

- Declaration `6d76fb20f6ecbc940e5c8fff36c74060c885e161`: blob `fee44721be1be2781d9b8f1488ce3c990f94cdb4`.
- Freeze `1e926801195e304950e3eb9d2525ef8bbc245089`: the **same** blob `fee44721be1be2781d9b8f1488ce3c990f94cdb4`.
- Change `c052bb7d41ced49aa888817069afd804eccfecf1`: blob `39c75ef31c946c0bd855ea439e520c03fcd0c37a`.

A declaration-to-freeze SCORECARD diff is empty. The freeze-to-change SCORECARD diff appends 76 lines, now lines 1685–1760, including:

1. Lines 1702–1709: a full predicate sentence and correction of declared label `leaking_pairs` to `leaking`, with numeric `leaking` and list-valued `leaking_pairs`. The original frozen declaration still says the predicate label is `leaking_pairs` at 1620–1621 and gives an unsupported `--json` command at 1614.
2. Lines 1710–1722: the declaration's livefive-only parity exemption and untraced zero-record limitation. These already exist in the frozen probe docstring at 25–44, but the frozen declaration does not contain this correction block.
3. Lines 1749–1754: the restated kill rule, adding explicit hidden reads and an `OR any sensitivity conjunct fails` branch. The sensitivity requirements existed in the original acceptance sentence at 1615–1619; this does not establish that this restatement was committed before scoring.
4. Lines 1756–1760: an asserted order placing “this corrections commit” before the freeze, although the block first appears in the freeze's child, the change commit. It also lists “this block” among change-commit contents.

The freeze LOG entry at `LOG.md:1377` points to “the pre-freeze corrections block” for the kill rule/named limit, but that block is absent from the freeze's SCORECARD object. A heading saying it was written earlier is not a prior committed artifact.

**Counterexample:** review only the frozen commit, without consulting its child. The executable has the livefive parity exemption and label `leaking`, while the committed declaration names `leaking_pairs` and lacks the cited limit/correction block. Consulting the child supplies a different documentary contract. Thus byte immutability alone cannot establish the requested single frozen authority.

**Impacted axes:** freeze directly; C1/operability evidence interpretation; calibration/provenance as a no-harm constraint.

**Smallest safe correction:** append an honest provenance erratum stating where the block was first committed, preserve both commits, and distinguish a prepared working-tree correction from a committed pre-freeze declaration. Do not alter the frozen probe, reinterpret earlier receipts, or declare the historical ordering repaired. A documentary correction is fixable; treating an after-committed limit as proof of prior conformance is not.

## F2 — exact receipt identity and incomplete pre-change evidence

All following files are beneath `.ufo/waves/round-36/l1/`, committed at freeze. A read-only diff against the freeze confirmed the inspected six JSONL files match their committed contents.

| File, summary line | Set | Leaking | `probe_sha256` | Equals freeze |
|---|---|---:|---|---|
| `dev-claim-final.jsonl:37` | claim | 0 | `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` | yes |
| `dev-r33claim-final4.jsonl:21` | r33claim | 0 | `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` | yes |
| `sens-mutattr.jsonl:5` | claim, one target | 0 | `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` | yes |
| `dev-r33claim-final.jsonl:21` | r33claim | 6 | `0865d8a16e7a6c9cebb317294dce8c70e921298fe2de526e09a67c27e788f4ea` | **no** |
| `dev-r33claim-final2.jsonl:21` | r33claim | 3 | `6ec9af2db3b40423adf285bb6694f89dfe13a5d7c3c491a7dd99f218086b3776` | **no** |
| `dev-r33claim-final3.jsonl:21` | r33claim | 3 | `6ec9af2db3b40423adf285bb6694f89dfe13a5d7c3c491a7dd99f218086b3776` | **no** |

All six advertise VERSION 7 and label `leaking`; the version label is therefore insufficient to identify counter bytes. The earlier r33 files are explicitly described in LOG as development misfires. Their differing hashes are **not themselves a post-freeze probe change**. However, `SCORECARD.md:1736–1738` calls the development sequence “on final bytes”; that provenance claim is contradicted by the summaries' hashes.

The exact-byte MutAttrgetter receipt has `targets: 1`, `pairs: 4`, `leaking: 0`, `harness_errors: []`, mutant revision `f84d4bd9b7fbf15aa4d1838c5b6486006912f0d8`. It does **not** satisfy the declared positive-sensitivity condition. LOG acknowledges that the selftest invocation misses the mutated builder and schedules a live-mode score later. That is honest disclosure of a missing conjunct, not a positive sensitivity receipt.

The committed before-design report also says its r36 battery was not executed because the probe was then absent (`w1/ExecBeforeDesign/ExecBeforeDesign.md:29–33`). Its `harness-dry.jsonl` is a receipt for another tool, not the C1 before measure. Wave-1 `ExecProbeR36/probe-evidence.json` identifies draft hashes and explicitly marks its regression result as non-final; those observations cannot fill the final-byte gap.

The only available wave-2 `W2ReBefore/livefive.stdout` inspected ended in `RuntimeError: cannot create local master branch`, with `livefive.exit` equal to 1 and no summary. This is a snapshot dependency finding, not a claim that the peer cannot later produce evidence. No waiting or rerun was performed. Any later receipt cannot retroactively become a committed pre-freeze receipt.

**Smallest safe correction:** keep an explicit final-byte evidence inventory, quarantine older development/counter-mutant receipts from eligibility, correct “on final bytes”, and record the missing historical before/sensitivity gate. Later real observations may establish later behavior, but cannot prove the original committed-before-freeze sequence. Do not convert the observed zero-sensitivity run into a pass by explanation alone.

## Exercised checks and boundaries

Performed only requested static review: read-only Git diffs/log/tree inspection, two commit-blob SHA-256 pipelines, receipt-summary inspection and frozen-hash search. In particular, the requested probe diff is empty with exit zero, and both probe commit hashes agree. Machine-readable transcribed observations: `freeze-evidence.json`.

No production edits, index changes, commits, probe/gate/test executions, alternate runtime/judge invocations, tool installs or updates. Only this seat directory was created and written. Findings concern the named freeze/change interval and the artifacts available during this review; absent later peer artifacts were not waited on.
