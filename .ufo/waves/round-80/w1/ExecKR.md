# ExecKR — Round80 w1 — C2 hermetic --selftest for tools/count-kr-rows-r69.py

- Seat: ExecKR (leaf, no dispatch). Execution class: **EXEC-AUTHORIZED**.
- Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. Base 467a9b7891a5939dab8460ec6f591fbb16bd82e9; frozen 61ec89ec6e6f284b6fba2127721359e6931a5789. Production HEAD observed aad05ef173176cf5223f7c315297240c2db1abe2 (read-only check; no git mutation anywhere).
- Axes: depth (selftest drives the actual public evaluator end-to-end incl. exit predicate and stable finding ids, proven by a red-before mutation control), operability (machine-checkable receipt matching the round80 instrument, replacement registry cell drafted to the exact interface the instrument greps).
- RULES.md read; no tools installed, no pacman transaction, no sudo, no host service touched.

## Deliverables (all beneath the lane root)

| Path | What |
|---|---|
| `.ufo/waves/round-80/w1/ExecKR/count-kr-rows-r69.py` | Full repaired source (sha256 `908592d2f8a209fdd070c6adc3157f04d69fcfe6815bda5ceb3d9981848ac97d`). |
| `.ufo/waves/round-80/w1/count-kr-rows-r69.py.receipt.json` | Binding receipt: tool_sha256 of those bytes, argv `["python3","tools/count-kr-rows-r69.py","--selftest"]`, rc 0, passed 10, failed 0, red-before block. |
| `.ufo/waves/round-80/w1/ExecKR/selftest.{stdout,stderr,rc,argv}.txt` | Complete green-run stdout (all 10 case lines + `SELFTEST: PASS (10 cases, 10 passed, 0 failed)`), empty stderr, rc 0, exact argv/cwd. |
| `.ufo/waves/round-80/w1/ExecKR/red-before.{stdout,stderr,rc,mutation}.txt` | Mutated control: rc 3, `SELFTEST: FAIL (10 cases, 4 passed, 6 failed)`, per-case failures named. |
| `.ufo/waves/round-80/w1/ExecKR/tool.sha256.txt` | Digests: original production bytes `54304628a4fe1523ae519f0a41a82d89f81ef04453c7557a50efa5143dd8bc7d` (unchanged, verified), final repaired bytes (above, three identical copies). |
| `.ufo/waves/round-80/w1/ExecKR/receipt.copy.json` | Copy of the receipt for seat-local provenance. |

## Behavior of the repaired tool (production semantics preserved)

- Existing modes untouched: `--revision`/`--lane`/`--snapshots` evaluate exactly as before (KR_ROW ok/fail:<clause> lines, `KR_ROWS=n KR_VERIFIED=v`, rc 0 iff all verified and ≥5; unreadable evidence → `KR_ERROR …` rc 2). Only delta: `--revision` requirement is now enforced by `parser.error` when `--selftest` is absent — usage stays rc 2, message "--revision is required".
- New `--selftest`: hermetic; builds one throwaway fixture repo under `tempfile.TemporaryDirectory`. The fixture and the spawned CLI run under a **fixed allowlisted environment** (`PATH` pinned to `/usr/bin:/bin` — trust is scoped to the system git binary, not to any filesystem confinement; the fixture runs with this process's permissions — `HOME`/`TMPDIR` pointed into the sandbox, `GIT_CONFIG_NOSYSTEM=1`, fixture identity, `LC_ALL`) — no ambient variable (`GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_DIR`/`GIT_WORK_TREE`, `GIT_CONFIG_COUNT`/`GIT_CONFIG_PARAMETERS`, `GIT_TEMPLATE_DIR`, user `PATH` entries) is copied, so neither index/object redirection, user templates/hooks, nor a substituted git can enter the fixture (same approach as `tools/_revision.py`'s clean env). `git -C ABS` for every operation, `rev-parse --show-toplevel` asserted equal to the fixture dir before any write; commits occur only inside the scratch fixture — the authorized exception. The public CLI is invoked by subprocess (`sys.executable <this file> …`), i.e. the real evaluator incl. `main()` and its exit codes, not helper-only assertions. 10 cases, each asserting rc AND stable finding text:
  1. positive: 5 verified rows + a fenced decoy row that must be ignored → rc 0, `KR_ROWS=5 KR_VERIFIED=5`, five `KR_ROW KR00n ok`.
  2. missing-note (registry-only commit) → rc 1, `KR_ROWS=0 KR_VERIFIED=0`.
  3. missing-snapshot → rc 1, `KR_ROW KR004 fail:snapshot`, `KR_VERIFIED=4`.
  4. wrong-source: `source=S902` exists in SOURCES.md but outside the `## Registry` heading → rc 1, `KR_ROW KR001 fail:source`.
  5. wrong-quote → rc 1, `KR_ROW KR001 fail:quote`.
  6. digest-mismatch (well-formed 64-hex, wrong value) → rc 1, `KR_ROW KR001 fail:digest`.
  7. malformed-cells (5 cells) → rc 1, `KR_ROW KR001 fail:cells`.
  8. unknown revision → rc 2, stderr `KR_ERROR missing revision:`.
  9. absent snapshot dir → rc 2, stderr `KR_ERROR missing snapshot directory:`.
  10. usage without `--revision` → rc 2, argparse usage/error on stderr.
  Any case failure → rc 3; harness faults (git/OSError/timeout) print `SELFTEST: FAIL (harness …)` and return 3 — no swallowed exceptions, no fabrication.
- No `_revision` import exists in this tool (verified by import grep); nothing was copied for it.

## Red-before control (test has teeth)

Mutation: `evaluate()` tail `return 0 if len(rows) == verified and verified >= 5 else 1` → `return 0`. Result: rc 3, 4 passed, 6 failed — every rc-1 expectation fails, proving the suite exercises the public exit predicate. Evidence: `red-before.*.txt`.

## Receipt corroboration (results outputs are corroboration only; receipt + source are binding)

Against the round80 instrument's C2 criteria: digest matches final bytes, argv exact, rc 0, passed int ≥ 4, failed 0, blob contains `--selftest` and `SELFTEST`, production tool bytes unchanged — all OK (programmatic check, rc 0).

## Draft replacement registry cell (TRUTHFUL; registry NOT edited by this seat)

The instrument requires the single `| count-kr-rows-r69 |` row of the fixed `## Gate and probe registry — round71 superseding current rows` section to have 8 cells, cells[1] `gate`, cells[3] containing `3 self-test failed`, cells[4] exactly `` `python3 tools/count-kr-rows-r69.py --selftest` ``. Replacement row (replaces the current round-71 row in place, other cells carried verbatim):

```
| count-kr-rows-r69 | gate | `python3 tools/count-kr-rows-r69.py --revision <REV> [--snapshots <DIR>] [--lane <repo>]` | 0 predicate `KR_ROWS == KR_VERIFIED and KR_VERIFIED >= 5`; 1 at least one row fails a clause; 2 could-not-evaluate (revision binding, unreadable registry, missing snapshot directory) or usage; 3 self-test failed | `python3 tools/count-kr-rows-r69.py --selftest` | Round-69 C1: per row it resolves the `source=` id against the registry at the revision, pins the named snapshot's sha256, and locates the quote in those bytes; the statement clause is a word count only, so a filler statement with a real source/digest/quote still verifies (named limit), and a PASS does not prove a sentence true; selftest: 10 hermetic public-CLI cases on one throwaway fixture repo (positive incl. fenced decoy, missing note, missing snapshot, wrong source outside the Registry heading, wrong quote, digest mismatch, malformed cells, unknown revision, absent snapshot dir, usage), red-before exit-predicate mutation rc 3 | committed reads only; selftest fixture commits confined to a throwaway temp repo | tsukuroi (round 69 C1; round 80 C2 selftest) |
```

Landing note for L1: the receipt binds `tool_sha256` to the exact bytes at `.ufo/waves/round-80/w1/ExecKR/count-kr-rows-r69.py`; those bytes must land at `tools/count-kr-rows-r69.py` unchanged for the instrument's digest equality to hold.

## Risks / limits

- The selftest proves counter mechanics (clauses, digests, quote containment, section scoping, exit predicate), not source entailment of the real round-69 note — consistent with the round80 declaration's separation of finite equality from authenticity.
- `--selftest` runs `git` subprocesses; on a host without git it fails loudly rc 3 (harness branch) rather than silently passing.
- Sibling seat owns `check-transaction-order-r39.py`; C2 count reaches 2 only when both land.

## Verification for main agent

Only the authorized runs were executed (green selftest, red-before control, receipt corroboration). Suggested integration checks: `python3 tools/measure-round80.py --fixture <prepared tree>` for C2 after both tools + receipts + registry row land; no other gates run by this seat.

Scope: executed=`mkdir -p /fast/scratch/hyaku/tsukuroi-r80/ExecKR/{lane/tools,red} + cp tool`; `python3 -m py_compile tools/count-kr-rows-r69.py` (scratch); `python3 tools/count-kr-rows-r69.py --selftest` (scratch lane root, rc 0); `sha256sum` copies; `cp` final to w1/ExecKR; `python3 red/count-kr-rows-r69.py --selftest` (scratch root, rc 3); receipt corroboration `python3` read-only check of w1 artifacts; `rm -rf /fast/scratch/hyaku/tsukuroi-r80/ExecKR`. Fixture git ops (init/add/commit/rev-parse, fixed identity) executed inside the selftest's own TemporaryDirectory only. No production, registry, SKILL.md, LOG.md, or sibling writes; no installs. Rework after ReviewMatrix static finding (ambient GIT_* leak): scratch recreated from the w1 deliverable, `_selftest_env` replaced by a fixed allowlist (no `dict(os.environ)`), docstring updated; green selftest re-run rc 0 (10/10), red control re-run rc 3 (6 failed), receipt + digests re-bound to `44b62b3353b8a30bdadcb25a70e8a481c6f83c2cfc433c2d78a79116d789d88e`, corroboration re-run OK (incl. `dict(os.environ)` absent from blob), scratch deleted again. Second rework after ReviewMatrix follow-up (inherited-PATH trust claim): `PATH` pinned to `/usr/bin:/bin` (matching `_revision.clean_env`), docstring restates trust scoping to the system git binary without filesystem-confinement claims; green selftest re-run rc 0 (10/10), red control re-run rc 3 (6 failed), receipt + digests re-bound to `908592d2f8a209fdd070c6adc3157f04d69fcfe6815bda5ceb3d9981848ac97d`, corroboration re-run OK (incl. `path_pinned` check), scratch deleted again.
