2026-11-03T22:36:40Z

# E1Probe — C2 gate drafted, red-before proven (round 68 / w1)

Scope: build the C2 reference gate as a draft and prove it red-before and
green-live in a sandbox clone. Lane base 42400ec6. No tracked file touched.

## Delivered

- Draft tool: `.ufo/waves/round-68/drafts/c2/check-knowledge-refs-r68.py`
  `TOOL_SHA256=d4390b7aa2c7fa1418ea5ff078f95c3faef19c6d12ecb6473d426a90fe7858d5`
  (23984 bytes; read-only; `sys.dont_write_bytecode`; header gate's
  `_revision` bootstrap, fence and column-zero rules; LAST unfenced column-0
  `source:` line; `\bS\d{3,}\b`; registry ids from `^\|\s*(S\d{3,})\s*\|`;
  `KNOWLEDGE-REF-DANGLING` one per (note, id); exit 0/1/2, JSON on stdout).
- Receipts: `.ufo/waves/round-68/probes/c2-selftest.txt`,
  `c2-live-base.json`, `c2-red-before.txt` (each starts with a UTC timestamp).
- Report: `.ufo/waves/round-68/drafts/c2/E1-report.md`.

## Evidence

Selftest (hermetic fixture repo under `TMPDIR=$S`; 19 cases):
```
$ TMPDIR=$S python3 .../check-knowledge-refs-r68.py --selftest
{"selftest": {"cases": 19, "failures": [], "passed": 19, "status": "PASS"}}
rc=0
```
Cases a-h of the item plus 11 more; every case asserts exit code and finding id
(refs too for DANGLING). SELFTEST=19/19 rc=0.

Live base (sandbox clone `git clone --shared` + `checkout -q 42400ec6`):
```
$ python3 $S/lane/tools/check-knowledge-refs-r68.py --revision 42400ec6 --lane $S/lane
status=PASS finding_count=0 note_count=85 sourced_count=85 ref_count=247
registry_id_count=285 dangling_count=0
rc=0
```
LIVE_BASE_RC=0 LIVE_FINDINGS=0.

Red-before (fixture commit `a0ba15cce8075ff8600201dca79451733bcf3c22` on
throwaway branch `r68-red-before`; master stays 3f6edcc9). Note
`corpus/knowledge/s999-fixture-r68.md` line 3 `source: S999 — fixture (never a
registry row)`:
```
(i)  header gate  --revision a0ba15cce807 --branch r68-red-before  -> rc=0, finding_count=0, note_count=86
(ii) new gate     --revision a0ba15cce807 --branch r68-red-before  -> rc=1,
     [{"id":"KNOWLEDGE-REF-DANGLING","ref":"S999",
       "site":"corpus/knowledge/s999-fixture-r68.md",
       "detail":"source: line 3 cites S999, absent from corpus/SOURCES.md at the revision"}]
control: new gate with default master -> rc=2 E-REVISION-NOT-LANDED (fixture never entered master)
```
REDBEFORE_HEADER_RC=0 REDBEFORE_NEW_RC=1. The round-66 routed gap (§3 of the
quality rule: `source: S999` passes the header gate) is reproduced and closed.

## Deviations, with reasons

1. Red-before binds `--branch r68-red-before`: `_revision.bind` requires the
   revision be landed on the named branch, and the fixture deliberately is not
   merged into master (control above shows master refuses it).
2. Receipts prepend a UTC timestamp; the selftest ran with `TMPDIR=$S` per the
   item's own fixture instruction. Tool output otherwise unmodified.
3. Payload counters are ref-specific (`sourced_count`, `ref_count`,
   `dangling_count`, `registry_id_count`); header gate's `complete_count` /
   `clean_count` have no meaning here. Findings additionally carry `ref`.
4. A registry with zero `| S<digits> |` rows is CANNOT_EVALUATE
   (E-PATH-MISSING), not a vacuous pass — fail-closed beyond the frozen text.
5. `S2Scout-gate-rules.md` appeared mid-item; read and reconciled before the
   selftest run, no rule conflict.

## Integration notes for the L1

- Copy the draft to `tools/check-knowledge-refs-r68.py`; nothing else is needed
  (no new import, `_revision` is already in `tools/`).
- At base 42400ec6 the gate is green with 85 notes / 247 refs / 285 registry ids,
  so landing it adds no finding to the corpus as it stands.
- If a future note cites an id whose registry row lands in the same commit, the
  gate resolves it at that revision — no ordering hazard inside one commit.

## Keys

SELFTEST=19/19 rc=0
LIVE_BASE_RC=0
LIVE_FINDINGS=0
REDBEFORE_HEADER_RC=0
REDBEFORE_NEW_RC=1
TOOL_SHA256=d4390b7aa2c7fa1418ea5ff078f95c3faef19c6d12ecb6473d426a90fe7858d5
