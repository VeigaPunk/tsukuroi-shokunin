# M1Mutation — round 75 w1
Verdict: COMPLETE battery; C1 7 built / 3 killed / 4 survived; C2 5 built / 2 killed / 3 survived. Inconclusive: 0.
Unchecked: no integrated-tip claim adjudication (outside seat scope). All assigned mutation probes and scratch cleanup completed.
Axes: operability, C1 depth, C2 freshness, mutation coverage.

## Method and detector
Frozen programs loaded from declaration commit `1e2bb29cb452d49822e35ada0f5fad419b19e24c`; their SHA-256 values exactly match the declaration. No lane program or sibling source was edited.
Executed `python3 <copy> --selftest` and `python3 <copy> --fixture <C1 mirror>` / `--root <C2 mirror>` with explicit TMPDIR in this seat scratch. Each subprocess bounded to 30 seconds; at most four concurrent processes.
C1 mirror copied from E1Counter; C2 mirror copied from E2Routed after each owner announced readiness. These are fixture/draft mirrors, not evidence that the repairs are committed. Mirrors stayed unchanged.
Pristine selftests each passed 13/13 (rc 0). Pristine mirrors passed C1 6/6 and C2 4/4 (rc 0). All 12 restored copies repeated both passing detectors.
A mutant is killed only when the detector differs from its successful pristine control. A surviving mutant is an instrument-coverage gap, NOT a failure of C1 or C2.

## Kill matrix
| Instrument | Mutant | Selftest rc | Killing case / survivor | Mirror rc |
|---|---|---:|---|---:|
| count-jt-rows-r75.py | digest-check | 3 | DIGEST-SWAP | 0 |
| count-jt-rows-r75.py | snapshot-reuse | 0 | SURVIVED | 0 |
| count-jt-rows-r75.py | quote-minimum | 0 | SURVIVED | 0 |
| count-jt-rows-r75.py | contiguous-ids | 0 | SURVIVED | 0 |
| count-jt-rows-r75.py | own-work | 3 | OWN-WORK-SOURCE | 0 |
| count-jt-rows-r75.py | registry-duplicate | 0 | SURVIVED | 0 |
| count-jt-rows-r75.py | exact-line-quote | 3 | CONTROL | 1 |
| check-r74-routed-r75.py | verb | 3 | NO-VERB | 0 |
| check-r74-routed-r75.py | window | 0 | SURVIVED | 0 |
| check-r74-routed-r75.py | round65 | 0 | SURVIVED | 0 |
| check-r74-routed-r75.py | backtick | 3 | AXES-NO-COMMAND | 0 |
| check-r74-routed-r75.py | wrong-unit | 0 | SURVIVED | 0 |

Only exact-line-quote also fails the valid mirror, with all six quotes rejected. The other 11 mirror runs pass (valid positive fixtures do not distinguish weakened clauses).

## Exact mutations
- `count-jt-rows-r75.py` / **digest-check**: `if not isinstance(snap_info, dict) or snap_info.get("sha256") != digest:` → `if not isinstance(snap_info, dict):`.
- `count-jt-rows-r75.py` / **snapshot-reuse**: `if reuse_count[snap] > MAX_SNAPSHOT_REUSE:` → `if False:`.
- `count-jt-rows-r75.py` / **quote-minimum**: `MIN_QUOTE_WORDS = 4` → `MIN_QUOTE_WORDS = 1`.
- `count-jt-rows-r75.py` / **contiguous-ids**: `if parsed_rows != list(range(1, len(parsed_rows) + 1)):` → `if False:`.
- `count-jt-rows-r75.py` / **own-work**: `if rinfo["kind"] not in KINDS:` → `if rinfo["kind"] not in KINDS and rinfo["kind"] != "own-work":`.
- `count-jt-rows-r75.py` / **registry-duplicate**: `if reg_dups:` → `if False:`.
- `count-jt-rows-r75.py` / **exact-line-quote**: `if quote_norm and quote_norm not in normalize_ws(snap_text):` → `if quote_norm and quote_norm not in snap_text.splitlines():`.
- `check-r74-routed-r75.py` / **verb**: `return any(v in low for v in VERBS)` → `return True`.
- `check-r74-routed-r75.py` / **window**: `WINDOW = 80` → `WINDOW = 1000`.
- `check-r74-routed-r75.py` / **round65**: `if "round 65" not in block.lower() and "round-65" not in block.lower():` → `if False:`.
- `check-r74-routed-r75.py` / **backtick**: `if not BACKTICK.search(row):` → `if False:`.
- `check-r74-routed-r75.py` / **wrong-unit**: `need_all=["SC3Index"], need_any=` → `need_all=[], need_any=`.
- Digest-check additionally replaces the independent byte-hash equality condition with `if False:`; both equalities implement the one removed digest-validation clause. The map-type guard remains.

## Lesson-ready named gaps (coverage findings only)
- **C1-REUSE-CONFOUNDED**: SNAPSHOT-REUSE-3 changes a gamma row to alpha without grounding its statement in alpha; token checks still reject it after the reuse cap is disabled. Use an otherwise valid three-use row distribution.
- **C1-QUOTE-MINIMUM-UNTESTED**: lowering 4 words to 1 survives; no located quote below four words is tested.
- **C1-CONTIGUITY-CONFOUNDED**: NON-CONTIGUOUS changes JT1 to JT2, so the independent duplicate-id check still rejects it. Use six distinct, non-contiguous ids.
- **C1-REGISTRY-DUPLICATE-CONFOUNDED**: duplicate S401 is built from the S403 row and overwrites its URL/anchor; independent provenance checks still reject it. Duplicate an identical registry row to isolate uniqueness.
- **C2-WINDOW-UNPINNED**: DECOY-DISTANT uses `(WINDOW + 5)`, so widening WINDOW moves the test farther away too; its content also lacks a correction verb. Pin the fixture distance independently and satisfy all other clauses.
- **C2-ROUND65-UNTESTED**: no case removes only the superseded round-65 reference.
- **C2-WRONG-UNIT-CONFOUNDED**: DEATH-WRONG-UNIT replaces SC3Index throughout the lesson, including the independently required wording report path; dropping the death unit check remains undetected. Change only the death block.
These findings have been sent to the round-75 lesson scribe; main integration owns corpus/lessons/round-75.md. No shared lesson was edited by this seat.

## Actual outputs, hashes, and restoration evidence
Frozen before hashes and declaration provenance:
```json
{
  "count-jt-rows-r75.py": {
    "sha256": "5e87238ce6909823797446b5be79194e2f701de46d3c4087ca75f289fca8cd71",
    "revision": "1e2bb29cb452d49822e35ada0f5fad419b19e24c"
  },
  "check-r74-routed-r75.py": {
    "sha256": "4b5c801ce4be7ea7562d9b472ce58badcd113d1062280220500275730f567d2c",
    "revision": "1e2bb29cb452d49822e35ada0f5fad419b19e24c"
  }
}
```
Pristine base-revision control outputs (not counted as kills):
```json
{
  "count-jt-rows-r75.py": {
    "rc": 128,
    "stdout": "JT_MAP absent\n",
    "stderr": ""
  },
  "check-r74-routed-r75.py": {
    "rc": 1,
    "stdout": "ROUTED_STALE=4 ROUTED_OK=0/4\nR74-DEATH-RECEIPT STALE reason=token path=corpus/lessons/round-74.md\nR74-REPORT-WORDING STALE reason=token path=corpus/lessons/round-74.md\nR74-SWEEP-RESIDUE STALE reason=token path=.ufo/waves/round-74/w1/E3HostProbe/receipt-g-landing.txt\nR74-STALE-AXES-TABLE STALE reason=heading path=SCORECARD.md\n",
    "stderr": ""
  }
}
```
Pristine mirror outputs:
```json
{
  "count-jt-rows-r75.py": {
    "rc": 0,
    "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
    "stderr": ""
  },
  "check-r74-routed-r75.py": {
    "rc": 0,
    "stdout": "ROUTED_STALE=0 ROUTED_OK=4/4\n",
    "stderr": ""
  }
}
```
Mutant SHA-256 and exact selftest/mirror stdout, stderr, exit code:
```json
[
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "pristine",
    "sha256": "5e87238ce6909823797446b5be79194e2f701de46d3c4087ca75f289fca8cd71",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "digest-check",
    "sha256": "08903284c19300d4d97699e43616b8c65db230e558175dcf18e7c20aa35db1fb",
    "selftest": {
      "rc": 3,
      "stdout": "SELFTEST: FAIL (13 cases, 12 passed, 1 failed)\n",
      "stderr": "SELFTEST-FAIL DIGEST-SWAP: expected rc 1, got 0 ({'JT_ROWS': 6, 'JT_VERIFIED': 6, 'JT_SOURCES': 3, 'JT_SNAPSHOTS': 3, 'JT_MALFORMED': 0, 'met': 1})\n"
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "snapshot-reuse",
    "sha256": "7b9b9bc202f0fa7e76b66d6849dfe706d1907e9a3717c6f8756f697532a8b6a2",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "quote-minimum",
    "sha256": "00667f82b615ba9137ab4178d358bea4ef6329971dfe8e7da89423d11d43e9ad",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "contiguous-ids",
    "sha256": "56452295be09a1a5a531c843c5dd2ff30d2da707a7fe46798ea18ad95184811a",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "own-work",
    "sha256": "bec2270dbff5433644ea7ced21ecbf0fa5861bc925c242ac741289c48ba5db8d",
    "selftest": {
      "rc": 3,
      "stdout": "SELFTEST: FAIL (13 cases, 12 passed, 1 failed)\n",
      "stderr": "SELFTEST-FAIL OWN-WORK-SOURCE: expected rc 1, got 0 ({'JT_ROWS': 6, 'JT_VERIFIED': 6, 'JT_SOURCES': 3, 'JT_SNAPSHOTS': 3, 'JT_MALFORMED': 0, 'met': 1})\n"
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "registry-duplicate",
    "sha256": "4b687e51964bc8a76ce30181633e6ee5343722bc7b2ac8d57530daff2032db14",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "exact-line-quote",
    "sha256": "107e1dd2e6fb22511c75a30d8e8e3525b0714bc32d53360b651e82d3d15aca70",
    "selftest": {
      "rc": 3,
      "stdout": "SELFTEST: FAIL (13 cases, 12 passed, 1 failed)\n",
      "stderr": "SELFTEST-FAIL CONTROL: expected rc 0, got 1 ({'JT_ROWS': 6, 'JT_VERIFIED': 0, 'JT_SOURCES': 3, 'JT_SNAPSHOTS': 3, 'JT_MALFORMED': 6, 'met': 0})\n"
    },
    "mirror": {
      "rc": 1,
      "stdout": "JT_ROWS=6 JT_VERIFIED=0 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=6 met=0\n",
      "stderr": "  line 4: quote not located in snapshot job.c\n  line 5: quote not located in snapshot job.c\n  line 6: quote not located in snapshot job.h\n  line 7: quote not located in snapshot job.h\n  line 8: quote not located in snapshot transaction.c\n  line 9: quote not located in snapshot transaction.c\n"
    }
  },
  {
    "instrument": "check-r74-routed-r75.py",
    "mutant": "pristine",
    "sha256": "4b5c801ce4be7ea7562d9b472ce58badcd113d1062280220500275730f567d2c",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    }
  },
  {
    "instrument": "check-r74-routed-r75.py",
    "mutant": "verb",
    "sha256": "ab883a0f2bcbde22db7d6cd1a5f946c70f9b23f9890d8ea6e2874a1fb6759f47",
    "selftest": {
      "rc": 3,
      "stdout": "SELFTEST: FAIL (13 cases, 12 passed, 1 failed)\n",
      "stderr": "SELFTEST-FAIL NO-VERB: expected rc 1, got 0\n"
    },
    "mirror": {
      "rc": 0,
      "stdout": "ROUTED_STALE=0 ROUTED_OK=4/4\n",
      "stderr": ""
    }
  },
  {
    "instrument": "check-r74-routed-r75.py",
    "mutant": "window",
    "sha256": "8cdf8377ecd7f28aff4d8b3fd1700d3f023b3c4f1d820733fc4677c1b75adf40",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "ROUTED_STALE=0 ROUTED_OK=4/4\n",
      "stderr": ""
    }
  },
  {
    "instrument": "check-r74-routed-r75.py",
    "mutant": "round65",
    "sha256": "77b9b25e77f92439cd71e088e65ba754805676bd058ee36ed96b64680f6262a4",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "ROUTED_STALE=0 ROUTED_OK=4/4\n",
      "stderr": ""
    }
  },
  {
    "instrument": "check-r74-routed-r75.py",
    "mutant": "backtick",
    "sha256": "89bdebbc7db891c81221ec1f2843a1d5e01687e918c9f6de69f93cd389b6bf7e",
    "selftest": {
      "rc": 3,
      "stdout": "SELFTEST: FAIL (13 cases, 12 passed, 1 failed)\n",
      "stderr": "SELFTEST-FAIL AXES-NO-COMMAND: expected rc 1, got 0\n"
    },
    "mirror": {
      "rc": 0,
      "stdout": "ROUTED_STALE=0 ROUTED_OK=4/4\n",
      "stderr": ""
    }
  },
  {
    "instrument": "check-r74-routed-r75.py",
    "mutant": "wrong-unit",
    "sha256": "ea7b0328c31dc0918647675ccfdad16e98a4dbd4185d109ba231fc3af8108924",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "ROUTED_STALE=0 ROUTED_OK=4/4\n",
      "stderr": ""
    }
  }
]
```
Restored copies: every after hash equals its frozen before hash; the exact same detectors pass:
```json
[
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "digest-check",
    "restored_sha256": "5e87238ce6909823797446b5be79194e2f701de46d3c4087ca75f289fca8cd71",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "snapshot-reuse",
    "restored_sha256": "5e87238ce6909823797446b5be79194e2f701de46d3c4087ca75f289fca8cd71",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "quote-minimum",
    "restored_sha256": "5e87238ce6909823797446b5be79194e2f701de46d3c4087ca75f289fca8cd71",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "contiguous-ids",
    "restored_sha256": "5e87238ce6909823797446b5be79194e2f701de46d3c4087ca75f289fca8cd71",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "own-work",
    "restored_sha256": "5e87238ce6909823797446b5be79194e2f701de46d3c4087ca75f289fca8cd71",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "registry-duplicate",
    "restored_sha256": "5e87238ce6909823797446b5be79194e2f701de46d3c4087ca75f289fca8cd71",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "count-jt-rows-r75.py",
    "mutant": "exact-line-quote",
    "restored_sha256": "5e87238ce6909823797446b5be79194e2f701de46d3c4087ca75f289fca8cd71",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1\n",
      "stderr": ""
    }
  },
  {
    "instrument": "check-r74-routed-r75.py",
    "mutant": "verb",
    "restored_sha256": "4b5c801ce4be7ea7562d9b472ce58badcd113d1062280220500275730f567d2c",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "ROUTED_STALE=0 ROUTED_OK=4/4\n",
      "stderr": ""
    }
  },
  {
    "instrument": "check-r74-routed-r75.py",
    "mutant": "window",
    "restored_sha256": "4b5c801ce4be7ea7562d9b472ce58badcd113d1062280220500275730f567d2c",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "ROUTED_STALE=0 ROUTED_OK=4/4\n",
      "stderr": ""
    }
  },
  {
    "instrument": "check-r74-routed-r75.py",
    "mutant": "round65",
    "restored_sha256": "4b5c801ce4be7ea7562d9b472ce58badcd113d1062280220500275730f567d2c",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "ROUTED_STALE=0 ROUTED_OK=4/4\n",
      "stderr": ""
    }
  },
  {
    "instrument": "check-r74-routed-r75.py",
    "mutant": "backtick",
    "restored_sha256": "4b5c801ce4be7ea7562d9b472ce58badcd113d1062280220500275730f567d2c",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "ROUTED_STALE=0 ROUTED_OK=4/4\n",
      "stderr": ""
    }
  },
  {
    "instrument": "check-r74-routed-r75.py",
    "mutant": "wrong-unit",
    "restored_sha256": "4b5c801ce4be7ea7562d9b472ce58badcd113d1062280220500275730f567d2c",
    "selftest": {
      "rc": 0,
      "stdout": "SELFTEST: PASS (13 cases, 13 passed, 0 failed)\n",
      "stderr": ""
    },
    "mirror": {
      "rc": 0,
      "stdout": "ROUTED_STALE=0 ROUTED_OK=4/4\n",
      "stderr": ""
    }
  }
]
```
Read-only copied mirror content hashes:
```json
{
  "count-jt-rows-r75.py": {
    ".ufo/waves/round-75/before/src/SHA256SUMS": "df0f6c714e084b04c109404249f824c86191647869206e00b2a92b8e4cf14bf6",
    ".ufo/waves/round-75/before/src/SOURCES.json": "18534939f27977ea48fe93b28a9d442550d84c0f9561dd6ae99eb118e62b4841",
    ".ufo/waves/round-75/before/src/job.c": "024a1accfd833223f2913d72e1f106fd40175429d31fcaca2321370fb5a10897",
    ".ufo/waves/round-75/before/src/job.h": "22d7b942426402ddba376c7b713bc9937c2eaa9f5817e8735dec8d5b6cf57c3a",
    ".ufo/waves/round-75/before/src/transaction.c": "c1c704bb4330ffee5203980219adf1ff1e11402a4a02092f471129ff7c5df2f3",
    "corpus/SOURCES.md": "19b0b0da8b4f39adc2f0d7190d48cbfd67f94dee9cc758402f8b491526dc9d49",
    "corpus/knowledge/systemd-job-transaction-plane-r75.md": "46b7a75f70498c2c43650ee852efe929d2613ac06e410eb2912f89e02fe0bbf4"
  },
  "check-r74-routed-r75.py": {
    ".ufo/waves/round-74/w1/E3HostProbe/receipt-g-landing.txt": "f18c8a73c796f3498bce06f9d1d941f9ccf09b3214ffcc18c252e896e3488eaf",
    "SCORECARD.md": "4247c4dd4ddeabed2d22c1b6618720bf7c61a625b8fa608c51a69535c7ce8552",
    "corpus/lessons/round-74.md": "d09df9546157f771a0be55cd234dc32cae289f9937201d50276737dcb3c9b0b3"
  }
}
```

## Scope / self-evaluation
No installs, privileged operations, Git mutations, runtime dispatch, or product-code changes. Only own scratch and this binding report were written.
Accuracy 4/5: exact rc/stdout/stderr/hashes preserved, but mirror bytes are fixture drafts, not integrated claims. Completeness 5/5: all 12 requested mutants and pristine/restored detectors covered. Clarity 4/5: verbose raw evidence is retained for audit. Actionability 5/5: seven named lesson gaps have isolated-test remedies. Conciseness 4/5: restoration records repeat outputs intentionally. Overall 4.4/5. User-agreement check: findings distinguish coverage from claim verdicts. Highest-impact improvement is to isolate the seven confounded/missing negative cases in a subsequent authorized instrument revision, not silently alter this frozen contract.

Cleanup: `rm -rf /fast/scratch/hyaku/tsukuroi-r75/M1Mutation` completed rc 0 after exact-byte restoration and restored detector runs; retained receipts are embedded above.
