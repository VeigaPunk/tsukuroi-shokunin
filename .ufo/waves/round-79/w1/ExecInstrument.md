# ExecInstrument — round-79 w1 — hermetic selftests for the two round-72 gate tools

claim=C2 operability (routed item 2: both round-72 gate tools gain a real `--selftest` with hermetic fixtures)
verdict=pass (deliverable complete and green with red-before evidence; two honest deviations recorded below, neither inside my two files)

## Files changed (exactly the two owned files; nothing else in the lane touched)

- `tools/check-r71-routed-r72.py` — sha256 `3060dcfe4f126d3eb6474a1f543bf415a3996065c410e9a898f70d22588c5175`
- `tools/count-md-rows-r72.py` — sha256 `58f7397ea39186afc8f2e476391715d3d482c9c1139d72e44023364be845063c`
- diffstat: 2 files changed, 411 insertions(+), 4 deletions(-). The 4 deletions are the replaced
  argparse mains and import lines. Frozen `evaluate`/`readers`/`counter_summary` bodies are
  byte-identical; the C2 kill rule "an altered frozen checker" is respected.

## Behavior added

- `--selftest` joins `--revision`/`--fixture` in a mutually exclusive argparse group. Default
  invocations are unchanged: no-arg / `--revision` / `--fixture` paths take the old code
  (rc 0 clean-or-met, rc 1 stale-or-missed; `--selftest --revision X` is argparse rc 2).
- Selftest builds a private fixture tree under `mkdtemp(dir=realpath($TMPDIR))`. Unset TMPDIR,
  TMPDIR under `/tmp`, or a missing TMPDIR prints the stable line
  `HARNESS-TMPDIR-REFUSED reason=tmpdir-unset|tmpdir-under-tmp|tmpdir-missing` and exits 2.
- Cases print `SELFTEST <case> rc=<rc> PASS|FAIL` (plus a captured-output dump on FAIL) and a
  closing `SELFTEST: PASS|FAIL (N cases, N passed, N failed)`. Exit 0 all-pass, 3 any-fail.
  A selftest failure is rc 3, never 2.
- Fixture trees are removed before exit; the only writes are inside the explicit TMPDIR.

## Evidence (full argv/stdout in `ExecInstrument/receipts.json`)

| Run | rc | Result |
|---|---|---|
| `check-r71-routed-r72.py --selftest` | 0 | `SELFTEST: PASS (8 cases, 8 passed, 0 failed)` |
| `count-md-rows-r72.py --selftest` | 0 | `SELFTEST: PASS (23 cases, 23 passed, 0 failed)` |
| both tools, `env -u TMPDIR` / `TMPDIR=/tmp` | 2 | `HARNESS-TMPDIR-REFUSED reason=…` |
| both tools, `--selftest --revision HEAD` | 2 | argparse conflict error |
| `check-registry-coverage.py --revision afe1f26…` | 1 | FAIL, 2 findings — see deviation 1 |
| `check-r71-routed-r72.py --revision afe1f26…` | 0 | `ROUTED_STALE=0` (receipt/scorecard/note all ok) |
| `count-md-rows-r72.py --revision afe1f26…` | 0 | `MD_ROWS=6 MD_VERIFIED=6 … met=1` |
| red-before check (mutated copy in scratch) | 3 | `SELFTEST: FAIL (9 cases, 5 passed, 4 failed)` |
| red-before count (mutated copy in scratch) | 3 | `SELFTEST: FAIL (23 cases, 4 passed, 19 failed)` |

Coverage of the required case classes:

- check tool (8 cases): clean pass; every stable finding id it emits — `ROUTED_RECEIPT missing`,
  `missing revision token`, `ROUTED_RECEIPT mismatch`, `ROUTED_SCORECARD missing`,
  `ROUTED_NOTE missing` (no section; and missing-token variant `missing: five`); malformed
  fixture (erratum quoted inline so no real heading opens the block); accepted variant
  (re-punctuated scorecard, backticked receipt path, lowercase `erratum` heading, extra prose
  in the receipt) still rc 0.
- count tool (23 cases): clean pass; malformed fixture (`| MD9 | oops |`); accepted variant
  (shuffled row order, triple-spaced quote, prose between rows, anchor-cell variant) still
  met=1; and one case per emittable finding id: `MD_NOTE absent` / `MD_REGISTRY absent` /
  `MD_MAP absent` (rc 128), `MD_MAP malformed`, `malformed-row`, `duplicate-id`,
  `statement-words=`, `statement-grounding=0/`, `snapshot-absent`, `digest-mismatch`,
  `map-digest`, `map-url`, `quote-absent`, `quote-words=`, `source-unregistered`,
  `source-kind=own-work`, `source-not-bound`, `anchor-not-bound`, `ids-not-contiguous`,
  `snapshot-reuse modprobe.conf=3`.

Red-before (mutation testing of the selftest's own sensitivity, scratch copies under
`/fast/scratch/hyaku/tsukuroi-r79/ExecInstrument`, both since deleted with the scratch tree):

- check tool, one clause mutated: `counter_summary` cmd → `["/bin/true", …]` (receipt
  re-derivation broken). Selftest goes red exactly on the receipt-derivation surface:
  `harness-counter-unavailable`, `clean-pass`, `receipt-mismatch`, `accepted-variant` fail;
  9 cases, 5 passed, 4 failed, rc 3.
- count tool, one clause mutated: `if CAND_RE.match(line):` → `if False and CAND_RE.match(line):`
  (row scan disabled). Every row-derived case fails with `MD_ROWS=0`; 23 cases, 4 passed,
  19 failed, rc 3.

## Deviations and limits (honest)

1. `check-registry-coverage.py --revision afe1f26…` did **not** return PASS 0 findings as my
   item expected: rc 1, two `REGISTRY-ROW-MISSING` findings for `tools/check-gate-standard-r79.py`
   and `tools/measure-unit-deps-r79.py`. Neither finding names my two tools (their operative
   rows exist and bind). The two missing rows are the round-79 instruments themselves — the
   SKILL.md registry surface belongs to the registry seat / integration commit, not this seat.
   Recorded, not fixed.
2. The `quote-pipe` finding id in the frozen count tool is unreachable by construction: a pipe
   inside the quote makes `line.count("|") == 8`, so the line is reported as `malformed-row`
   before the quote checks run. The case `quote-pipe-dead-branch` asserts exactly that
   (`malformed-row` present, `quote-pipe` forbidden) instead of pretending the id is emittable.
   Frozen logic left untouched; flagged here for the record.
3. The check tool's receipt-ok cases re-derive through the frozen `counter_summary()`, which is
   lane-anchored by design ("a fixture proves text shape only"). A relocated copy of the tool
   without the lane goes red via `harness-counter-unavailable` — the check-tool red run doubles
   as the demonstration. In-lane runs are unaffected.

## Tooling

No tool installed or updated (python3 3.14.8 already present; host pacman pause honored — no
pacman transaction attempted).

Scratch `/fast/scratch/hyaku/tsukuroi-r79/ExecInstrument` deleted before yield. No git
mutations anywhere; the only writes were the two owned tools, this report and
`ExecInstrument/receipts.json`.
