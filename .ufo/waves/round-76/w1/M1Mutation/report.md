# M1Mutation — round 76 w1

Verdict: the eight requested JD clause mutants and eight closure-clause mutants are killed; three additional semantic mutants survive. No claim verdict is inferred. Unchecked: committed/live C1/C2 correctness and source-semantic review.

Axes: depth, freshness, attack. Frozen instruments match both declared SHA-256 digests. No tools installed or upgraded.

## Method
JD frozen validated draft + frozen source snapshots + captured working registry; C2 synthetic positive control from frozen detector selftest. Fixture results are instrument coverage only, not live committed claim validation.

Each independent case runs the identical CLI detector on pristine, mutated, then exactly restored fixture bytes with a 30-second subprocess bound and explicit TMPDIR. Six workers operate on disjoint scratch directories. Every pristine/restored run returned 0; every complete file-hash manifest restored exactly. No baseline failures or inconclusive cases. Snapshots, real notes and instruments remain unmodified.

Commands (absolute paths in execution): `python /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/count-jd-rows-r76.py --fixture <isolated-case>`; `python /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-r75-routed-r76.py --root <isolated-case>`.

## JD mutation table

Overall kill rate: 8/9 (88.9%). Requested structural-clause subset: 8/8 (100%).

| ID | Mutation | Expected | Observed | Verdict |
|---|---|---|---|---|

| JD-short | Statement shortened to eleven words | reject (rc=1) | rc=1 JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0; line 10: short statement (11 < 12) | killed |

| JD-quote-absent | Replace quote with absent four-word quotation | reject (rc=1) | rc=1 JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0; line 10: quote not located in snapshot journald.conf.xml | killed |

| JD-quote-26 | Replace quote with source-verbatim 26 words | reject (rc=1) | rc=1 JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0; line 10: quote length out of bounds (26) | killed |

| JD-id-gap | Rename JD8 to JD9 | reject (rc=1) | rc=1 JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0; line 0: non-contiguous IDs: [1, 2, 3, 4, 5, 6, 7, 9] | killed |

| JD-unregistered | Replace first S318 with S999 | reject (rc=1) | rc=1 JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=5 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0; line 10: source S999 not in registry | killed |

| JD-reuse-five | Replace JD3 content with JD1 content, retaining JD3 ID; all four distinct snapshots remain | reject (rc=1) | rc=1 JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0; line 15: snapshot journald.conf.xml cited 5 > 4 | killed |

| JD-digest | Swap first digest to zeroes | reject (rc=1) | rc=1 JD_ROWS=7 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=2 met=0; line 10: digest mismatch for journald.conf.xml;   line 0: non-contiguous IDs: [2, 3, 4, 5, 6, 7, 8] | killed |

| JD-host | Remove observed host literal | reject (rc=1) | rc=1 JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=0 JD_MALFORMED=1 met=0; line 0: host block missing literal 148.6M | killed |

| JD-semantic | Change default SystemMaxFiles 100 to 101, preserving real quote | reject (rc=1) | rc=0 JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1;  | survived |

## Closure mutation table

Overall kill rate: 8/10 (80.0%). Requested structural-clause subset: 8/8 (100%).

| ID | Mutation | Expected | Observed | Verdict |
|---|---|---|---|---|

| C2-supersede | Delete superseding source row | reject (rc=1) | rc=1 ROUTED_STALE=1 ROUTED_OK=7/8; R76-S314-SUPERSEDE reason=rows path=corpus/SOURCES.md missing=supersedes S314 row | killed |

| C2-jt5 | Change eight items to nine | reject (rc=1) | rc=1 ROUTED_STALE=1 ROUTED_OK=7/8; R76-JT5-COUNT reason=need path=corpus/knowledge/systemd-job-transaction-plane-r75.md missing=eight comma-separated items | killed |

| C2-mistake | Drop one of five mistakes | reject (rc=1) | rc=1 ROUTED_STALE=1 ROUTED_OK=7/8; R76-R75-MISTAKE-COUNT reason=count path=corpus/lessons/round-75.md rows=4 | killed |

| C2-receipt | Corrupt receipt success count | reject (rc=1) | rc=1 ROUTED_STALE=1 ROUTED_OK=7/8; R76-R75-RECEIPT-REPOINT reason=need path=.ufo/waves/round-76/before/recheck-r75-at-tip.txt missing=ROUTED_OK=4/4 | killed |

| C2-marker | Remove one carried marker | reject (rc=1) | rc=1 ROUTED_STALE=1 ROUTED_OK=7/8; R76-WAVE-MARKERS reason=markers missing=.ufo/waves/round-66/w1.ready.dispatched | killed |

| C2-carrier | Break one of three drift carriers | reject (rc=1) | rc=1 ROUTED_STALE=1 ROUTED_OK=7/8; R76-JD-CONFIG-DRIFT reason=need path=corpus/knowledge/degraded-triage-r4.md missing=SystemMaxUse=256M | killed |

| C2-quality | Remove cadence from criterion 109 | reject (rc=1) | rc=1 ROUTED_STALE=1 ROUTED_OK=7/8; R76-QUALITY-109 reason=need path=corpus/QUALITY.md missing=cadence | killed |

| C2-wording | Broaden narrowed knowledge wording | reject (rc=1) | rc=1 ROUTED_STALE=1 ROUTED_OK=7/8; R76-QUALITY-WORDING reason=need path=corpus/lessons/round-76.md missing=no admitted knowledge entry is left failing its own re-check | killed |

| C2-receipt-negated | Prefix success receipt lines with NOT TRUE while retaining checked literals | reject (rc=1) | rc=0 ROUTED_STALE=0 ROUTED_OK=8/8;  | survived |

| C2-quality-negated | Negate criterion obligation while preserving all trigger words | reject (rc=1) | rc=0 ROUTED_STALE=0 ROUTED_OK=8/8;  | survived |

## Survivor analysis / lesson-ready coverage debt

- **JD-semantic:** `SystemMaxFiles` default changes from 100 to 101, retaining the correct source quote. The lexical-token/shared-ratio predicate does not discriminate numeric truth. Format-check limit, acceptable only when explicitly named; source-semantic reading remains required. This is not evidence of a defect in the real note.

- **C2-receipt-negated:** success receipt is prefixed `NOT TRUE:` while `met=1` remains present. Substring matching does not authenticate a receipt or interpret negation. Format-check limit, explicitly named; compare the actual bounded instrument rerun outputs rather than treating receipt tokens as provenance.

- **C2-quality-negated:** `requires a recheck command with a cadence` becomes `does not require a recheck command with a cadence`. The `round-76.md`/`recheck`/`cadence` checks do not discriminate normative meaning. Format-check limit, explicitly named; human criterion review remains necessary.

Route these three findings as **instrument-coverage debt in the round-76 lesson**, not as C1/C2 claim verdicts. No claim failure is established by synthetic fixture survivors; no contract or instrument was changed. The lesson itself is sibling-owned and intentionally unchanged by this seat.

The reuse-five mutant retains eight rows and all four sources/snapshots; its sole finding is reuse >4. The 26-word quote is verbatim in the snapshot and fails only length. The eleven-word statement fails only length. Digest corruption has one mutated clause but also causes the expected downstream ID-gap finding because that row is excluded from parsed rows.

## Selftests (exact stdout; both rc=0, empty stderr)

`count-jd-rows-r76.py` SHA-256 `549f6ba352284d44d7462954d1de36d2134bab73b0440e4e011b9017ec58fe4f`
```text
SELFTEST: PASS (14 cases, 14 passed, 0 failed)
```

`check-r75-routed-r76.py` SHA-256 `01e12e6a57211f80d2f9e042a336cf7ebe933b0560fecedef0411fe158ffe3d7`
```text
SELFTEST: PASS (10 cases, 10 passed, 0 failed)
```

## Actual pristine / mutated / restored output

Complete per-file before/mutated/restored SHA-256 manifests and stdout/stderr are preserved in `evidence.json`. These include every control dependency, not just the changed file. All 19 cases have exact manifest equality before/restored.

### JD-short

`corpus/knowledge/journald-retention-plane-r76.md`
- before: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`
- mutated: `7258829aa0a274fc59f99291ad87a66c63392fe7404e2d68aa8d1f1708bce234`
- restored: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`

baseline rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

mutated rc=1
```text
stdout:
JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0
stderr:
  line 10: short statement (11 < 12)
```

restored rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

### JD-quote-absent

`corpus/knowledge/journald-retention-plane-r76.md`
- before: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`
- mutated: `1e8f320bba0bc8cfbe4aaf921d1e0b8f62467ce0a3b0dcc70b2ca30d79185ed8`
- restored: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`

baseline rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

mutated rc=1
```text
stdout:
JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0
stderr:
  line 10: quote not located in snapshot journald.conf.xml
```

restored rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

### JD-quote-26

`corpus/knowledge/journald-retention-plane-r76.md`
- before: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`
- mutated: `5d6414c807acf25eaac9c64b2746b398125e903879811ee202a9f0b73fccf8d0`
- restored: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`

baseline rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

mutated rc=1
```text
stdout:
JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0
stderr:
  line 10: quote length out of bounds (26)
```

restored rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

### JD-id-gap

`corpus/knowledge/journald-retention-plane-r76.md`
- before: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`
- mutated: `7e54b93298c54eae7c9fd978c93697a7ccae1b0c6f2bcdbe0578d43b77cf86b3`
- restored: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`

baseline rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

mutated rc=1
```text
stdout:
JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0
stderr:
  line 0: non-contiguous IDs: [1, 2, 3, 4, 5, 6, 7, 9]
```

restored rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

### JD-unregistered

`corpus/knowledge/journald-retention-plane-r76.md`
- before: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`
- mutated: `06c92093d0a2cad82184487e3506bee2fdd1fc77881eb7007010234f57215292`
- restored: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`

baseline rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

mutated rc=1
```text
stdout:
JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=5 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0
stderr:
  line 10: source S999 not in registry
```

restored rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

### JD-reuse-five

`corpus/knowledge/journald-retention-plane-r76.md`
- before: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`
- mutated: `58aebff14176990bbcbe34952ec75be2cfd2b7aefa06fd7bd96ccca6b8a9dff4`
- restored: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`

baseline rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

mutated rc=1
```text
stdout:
JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0
stderr:
  line 15: snapshot journald.conf.xml cited 5 > 4
```

restored rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

### JD-digest

`corpus/knowledge/journald-retention-plane-r76.md`
- before: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`
- mutated: `d0a54ba61c65e68b3b3cd050fc63aecb791defa72a67c95ecd7358b5f0ccbefd`
- restored: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`

baseline rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

mutated rc=1
```text
stdout:
JD_ROWS=7 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=2 met=0
stderr:
  line 10: digest mismatch for journald.conf.xml
  line 0: non-contiguous IDs: [2, 3, 4, 5, 6, 7, 8]
```

restored rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

### JD-host

`corpus/knowledge/journald-retention-plane-r76.md`
- before: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`
- mutated: `536f593d02242c9555f14157104e4cc5f68acd490fd54d4683be3b03dfe5d970`
- restored: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`

baseline rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

mutated rc=1
```text
stdout:
JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=0 JD_MALFORMED=1 met=0
stderr:
  line 0: host block missing literal 148.6M
```

restored rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

### JD-semantic

`corpus/knowledge/journald-retention-plane-r76.md`
- before: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`
- mutated: `9c243afb60f3301d74215be613cdcc81b1a2636eaa5a4f42542a8ee81356b072`
- restored: `4313d06ee27579d894225bf92713464404bdd4d19571fd3388f0f569651c4972`

baseline rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

mutated rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

restored rc=0
```text
stdout:
JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1
stderr:
```

### C2-supersede

`corpus/SOURCES.md`
- before: `98be01e5f0cc55129c39a5b845fdb95c1bf631895ce7b9ef09e15e17e174f81a`
- mutated: `fb589b977314be052aeeb191f4d07828efbe86693596f0656099665067083670`
- restored: `98be01e5f0cc55129c39a5b845fdb95c1bf631895ce7b9ef09e15e17e174f81a`

baseline rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

mutated rc=1
```text
stdout:
ROUTED_STALE=1 ROUTED_OK=7/8
stderr:
  R76-S314-SUPERSEDE reason=rows path=corpus/SOURCES.md missing=supersedes S314 row
```

restored rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

### C2-jt5

`corpus/knowledge/systemd-job-transaction-plane-r75.md`
- before: `414c850194d2831a1a97073c0f895e8e201b5c4596c64522fd5e5e102d449524`
- mutated: `56bb94a2aeb86a943ebd80c9f7a1e507460a308a0c0692e6c1f1a93675ef861b`
- restored: `414c850194d2831a1a97073c0f895e8e201b5c4596c64522fd5e5e102d449524`

baseline rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

mutated rc=1
```text
stdout:
ROUTED_STALE=1 ROUTED_OK=7/8
stderr:
  R76-JT5-COUNT reason=need path=corpus/knowledge/systemd-job-transaction-plane-r75.md missing=eight comma-separated items
```

restored rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

### C2-mistake

`corpus/lessons/round-75.md`
- before: `607558f6c12556c8b1433978589c276c15e3b621519df7944098c821aec030d0`
- mutated: `cf8b58dc4c35d3a46bff53d6d5ec5b76a7386c121146f6d6a5c899b329a4720e`
- restored: `607558f6c12556c8b1433978589c276c15e3b621519df7944098c821aec030d0`

baseline rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

mutated rc=1
```text
stdout:
ROUTED_STALE=1 ROUTED_OK=7/8
stderr:
  R76-R75-MISTAKE-COUNT reason=count path=corpus/lessons/round-75.md rows=4
```

restored rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

### C2-receipt

`.ufo/waves/round-76/before/recheck-r75-at-tip.txt`
- before: `63bdfa951138ad711eae3792c4d61b2d46b53f65494da9351cb537e8e49f9182`
- mutated: `744076264f1f85db9928c184c2d9c06bde7ac232381cf50cd1604efb6f15dde5`
- restored: `63bdfa951138ad711eae3792c4d61b2d46b53f65494da9351cb537e8e49f9182`

baseline rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

mutated rc=1
```text
stdout:
ROUTED_STALE=1 ROUTED_OK=7/8
stderr:
  R76-R75-RECEIPT-REPOINT reason=need path=.ufo/waves/round-76/before/recheck-r75-at-tip.txt missing=ROUTED_OK=4/4
```

restored rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

### C2-marker

`.ufo/waves/round-66/w1.ready.dispatched`
- before: `ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356`
- mutated: `ABSENT`
- restored: `ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356`

baseline rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

mutated rc=1
```text
stdout:
ROUTED_STALE=1 ROUTED_OK=7/8
stderr:
  R76-WAVE-MARKERS reason=markers missing=.ufo/waves/round-66/w1.ready.dispatched
```

restored rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

### C2-carrier

`corpus/knowledge/degraded-triage-r4.md`
- before: `a3a3410769936682f780b550de010048997d68f1fa5bfe06fee39432b33d802d`
- mutated: `467574398a723950a5da988021ef856553e0441899414f2871b1a7bb75ee9b1d`
- restored: `a3a3410769936682f780b550de010048997d68f1fa5bfe06fee39432b33d802d`

baseline rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

mutated rc=1
```text
stdout:
ROUTED_STALE=1 ROUTED_OK=7/8
stderr:
  R76-JD-CONFIG-DRIFT reason=need path=corpus/knowledge/degraded-triage-r4.md missing=SystemMaxUse=256M
```

restored rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

### C2-quality

`corpus/QUALITY.md`
- before: `83b3f3249203f098d3e283d5bce9d75ca54bcb97b0de13a32f8811c40801d23d`
- mutated: `5d91548c979b95d1d47ae308891ab977f0ef8deae97ed3d9dca466405f68d697`
- restored: `83b3f3249203f098d3e283d5bce9d75ca54bcb97b0de13a32f8811c40801d23d`

baseline rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

mutated rc=1
```text
stdout:
ROUTED_STALE=1 ROUTED_OK=7/8
stderr:
  R76-QUALITY-109 reason=need path=corpus/QUALITY.md missing=cadence
```

restored rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

### C2-wording

`corpus/lessons/round-76.md`
- before: `45b5632f7aa6ec13381f3ad2a43ab1b4be34126dc2ac292dd680eddd3f0e8ac7`
- mutated: `d6cd06257a410668934560ba4be55fe96df9e5a95c510f9feb3358b698c7c67d`
- restored: `45b5632f7aa6ec13381f3ad2a43ab1b4be34126dc2ac292dd680eddd3f0e8ac7`

baseline rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

mutated rc=1
```text
stdout:
ROUTED_STALE=1 ROUTED_OK=7/8
stderr:
  R76-QUALITY-WORDING reason=need path=corpus/lessons/round-76.md missing=no admitted knowledge entry is left failing its own re-check
```

restored rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

### C2-receipt-negated

`.ufo/waves/round-76/before/recheck-r75-at-tip.txt`
- before: `63bdfa951138ad711eae3792c4d61b2d46b53f65494da9351cb537e8e49f9182`
- mutated: `868a538f15029154381734df8e02d2ef0ea916cf6796877e16f9ac7ca923d7c3`
- restored: `63bdfa951138ad711eae3792c4d61b2d46b53f65494da9351cb537e8e49f9182`

baseline rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

mutated rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

restored rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

### C2-quality-negated

`corpus/QUALITY.md`
- before: `83b3f3249203f098d3e283d5bce9d75ca54bcb97b0de13a32f8811c40801d23d`
- mutated: `831016f35ab6949ce23a71ef63b19623d0ab7f8571d60b48399ccaaabfb03994`
- restored: `83b3f3249203f098d3e283d5bce9d75ca54bcb97b0de13a32f8811c40801d23d`

baseline rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

mutated rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

restored rc=0
```text
stdout:
ROUTED_STALE=0 ROUTED_OK=8/8
stderr:
```

## Scope and self-evaluation

No commits, live instrument edits, source-note edits, fleet writes, privileged commands, or secondary runtime invocation. Scratch removed before delivery; retained files are scoped receipts only.

Accuracy 4/5: actual outputs and hashes retained; no live semantic verdict. Completeness 5/5: all eight requested mutations per detector, three extra semantic challenges, both selftests, restoration and cleanup evidence. Clarity 4/5: tables plus full outputs are intentionally redundant for audit. Actionability 4/5: lesson-ready debt supplied, sibling-owned lesson not edited. Conciseness 4/5: detailed evidence is long but bounded. Overall 4.2/5. Improvement: preserve format-versus-truth distinction in the lesson and keep full manifests in the linked JSON. User agreement expected on coverage, not on any untested claim.
