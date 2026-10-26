VERDICT: defect-found

Seat GateBoundary, item G-6. All four gates run at the dispatch tip
`2e1c2a40c13dc52e155d89e72f3fdd560db7399a` and at the declared base
`0eff65b21bb81195ee06c96a83afbd7a07e52eef`. No gate regressed between the two revisions, and
three of four read exactly what the lane expects. The defect is not in the gate code: it is in the
round-39 wave's declaration contract, which makes every honest `Scope: executed=…` trailer a
`SCOPE-EXEC-UNAUTHORIZED` red — a red the wave creates and cannot pass. Second finding: the
pause-gate docstring contradicts its own evaluator about the `unverified` verdict.

## 1. Exit codes (process exit, not a pipeline)

| tool | mode | at `2e1c2a40` | at `0eff65b2` |
|---|---|---|---|
| check-boundary-contract | `--revision` | **0** PASS, 6/6 decisions, findings [] | **0** PASS, 6/6, findings [] |
| check-pause-gate | `--revision` | **1** FAIL, `premises_verified` 4/5, finding `GATE-PREMISE P3:verdict-unverified-not-counted` | **1** FAIL, 4/5, same single finding |
| check-seat-scope | `--revision … --wave .ufo/waves/round-39/w1` | **2** CANNOT_EVALUATE, `E-SEAT-SOURCE-MISSING` | **2** CANNOT_EVALUATE, `E-SEAT-SOURCE-MISSING` |
| check-seat-scope | `--worktree --wave .ufo/waves/round-39/w1` | **1** FAIL, 70 seats: MISSING 57 / UNDECLARED 13 / UNAUTHORIZED 0 (06:06Z) | n/a (worktree is one state) |
| check-path-reconciliation | `--revision` | **0** PASS, both cohorts explained, unexplained 0 | **0** PASS, unexplained 0 |

Selftests (hermetic, exit codes taken directly): boundary **0** PASS 28/28, pause-gate **0** PASS
24/24, seat-scope **0** PASS 54/54 (`CHECK_SEAT_SCOPE_SELFTEST: PASS (54 cases, 54 passed, 0
failed)`), path-reconciliation **0** PASS 40/40. Receipts:
`.ufo/waves/round-39/w1/GateBoundary/*.selftest.json`.

Note on the first attempt: `check-seat-scope.py --revision <hex>` without `--wave` is rejected by
design — `tools/check-seat-scope.py:245-246` returns `E-CLI`, emitted as exit 2 with
`"revision": "worktree"`. That is a usage rule, not a red; the table above supplies `--wave`.

## 2. Per-gate detail

**Boundary contract — green, unchanged.** `tools/check-boundary-contract.py:88-136` validates the
six decisions against `corpus/knowledge/seat-boundary-r22.json`, the prose table, the S083/S084 rows
and the host-limit JSON. At both revisions: `{"status": "PASS", "validated_boundary_decisions": 6,
"total_decisions": 6, "findings": []}`. Round 39 edits `corpus/SOURCES.md` (+7/−1) but touches
neither S083 nor S084 — the diff shows only S208's `used-by` cell gaining
`corpus/knowledge/pacman-transaction-order-r39.md` and S213–S218 appended — so the row checks at
`tools/check-boundary-contract.py:111-115` are untouched, and no duplicate S id was introduced
(`findings: []` at tip). No new red.

**Pause gate — red at base and at tip, identical.** Tip and base both return
`{"status": "FAIL", "premises_total": 5, "premises_verified": 4, "checkupdates_attachment_pinned":
true, "findings": [{"id": "GATE-PREMISE", "site": "P3:verdict-unverified-not-counted"}]}`. The
tool's own guards ran and passed: it would have returned `CANNOT_EVALUATE`
`GATE-BINDER-BYTES`/`GATE-SELF-BINDING` had `tools/_revision.py` or its own blob differed from the
revision (`tools/check-pause-gate.py:245-260`), and it did not. The cause is authored, not drifted:
`corpus/knowledge/pause-lift-gate-r24.json:85` holds `"verdict": "unverified"` for P3 ("mkinitcpio
42 breaks the configured late hooks that still name /new_root"), and
`tools/check-pause-gate.py:35` excludes `unverified` from `COUNTED`, so lines 109-112 append
`verdict-unverified-not-counted`. This is the same known base red the scorecard records at
`SCORECARD.md:1330` ("check-pause-gate stays at its base exit 1 (`GATE-PREMISE`, receipted at
base)"), `SCORECARD.md:1406` ("1 → 1, the same `GATE-PREMISE P3` finding") and
`SCORECARD.md:1558`. Round 39 supplies no SOURCES row P3 reads (its rows are S104/105/106 for P1,
S092/106 P2, S109/095/110/111/112 P3, S099/100/101/114 P4, S107/091/108/113 P5), so no round-39
change can move it. No new red — but see §3.2 for a documentation defect in this gate.

**Seat scope — cannot evaluate at any revision for round 39; red in worktree.** At both revisions
`--revision … --wave .ufo/waves/round-39/w1` gives exit 2,
`{"status": "CANNOT_EVALUATE", "findings": [{"id": "E-SEAT-SOURCE-MISSING", "detail": "neither
swarm-registry.json nor spec.json"}]}`, because neither `.ufo/waves/round-39/w1/swarm-registry.json`
nor `.ufo/waves/round-39/w1-spec.json` is tracked at `2e1c2a40` or at the lane HEAD
`394e1ba4fab39a417abe66a7802f87cf1ff8dd61` (`git status --porcelain` → `?? …/w1/swarm-registry.json`;
`git show 2e1c2a40:.ufo/waves/round-39/w1-spec.json` → "exists on disk, but not in"). The wave root
argument fails the same way (only `revs.json`, `w1-dispatch.json`, `w1-spec.json` on disk, none
tracked at that revision). Control that the tool itself works on a tracked wave: `--revision
2e1c2a40 --wave .ufo/waves/round-38/w1` evaluates — exit 1, 71 seats, `SCOPE-UNDECLARED` 71,
`SCOPE-REPORT-MISSING` 0 — so the round-39 `CANNOT_EVALUATE` is a wave-packaging fact, not a tool
fault. Round 38's registry reached git at its integration commit `b0005ae`, so this is the expected
mid-wave state; it becomes an audit gap only if the integration commit omits the registry.

Worktree mode is the only live view, and it is red and moving:
- 06:04Z: exit 1, 70 seats, `SCOPE-REPORT-MISSING` 69, `SCOPE-UNDECLARED` 1, `SCOPE-EXEC-UNAUTHORIZED` 0.
- 06:06Z: exit 1, 70 seats, `SCOPE-REPORT-MISSING` 57, `SCOPE-UNDECLARED` 13, `SCOPE-EXEC-UNAUTHORIZED` 0.

Every report that exists at 06:06Z lacks the trailer (13 of 13 non-missing reports undeclared; e.g.
`C1ScoutProcMounts.md` ends at "## Not done" with no `Scope:` line). `grep -c "Scope: executed"
.ufo/waves/round-39/w1-spec.json` → **0**, and the same grep on
`.ufo/waves/round-39/w1-dispatch.json` → **0**: no round-39 seat is told to close with the trailer
the gate requires.

**Path reconciliation — green, unchanged.** Both revisions: `{"status": "PASS",
"reconciliation_mode": 1, "findings": [], "cohorts": {"build": {"events": 378, "agree": 376,
"selector-normalization": 2, "unexplained": 0}, "falsify": {"events": 995, "agree": 991,
"selector-normalization": 4, "unexplained": 0}}}`, each `"explained": true`. Every pinned input is
byte-identical base→tip (`.ufo/waves/round-23/frozen/reconciliation-inputs.json`,
`.ufo/waves/round-23/path-reconciliation.json`, the round-22 S085 source cell), so round 39 cannot
have moved it. No new red.

## 3. Round-39 causes of new red

### 3.1 The wave's own declaration contract turns honest trailers red (new red, round-39 cause)

`tools/check-seat-scope.py:41` defines `EXEC_MARK = "EXEC-AUTHORIZED"`; lines 88-91 emit
`SCOPE-EXEC-UNAUTHORIZED` for any non-`none` declaration whose seat prompt lacks it. The round-39
wave has **0 of 70** prompts carrying the marker (checked across `.ufo/waves/round-39/w1-spec.json`,
`w1-dispatch.json` and `.ufo/waves/round-39/w1/swarm-registry.json`) while **36 of 70** prompts
order execution (`C1ExecRerun`, `C1LeakArms`, `C1DetectHonest`, this seat, …). The wave-dir registry
members carry no `prompt` field at all, and there is no `spec.json` inside the wave dir, so at gate
time every seat prompt is the empty string.

Demonstrated on a scratch clone (never in the lane; receipt
`.ufo/waves/round-39/w1/GateBoundary/fixture-demo.txt`): one-seat fixture with the round-39 shape
(registry member without prompt).

| variant | report trailer | prompt | gate |
|---|---|---|---|
| 1 | `Scope: executed=python3, git` | no marker (round-39 shape) | exit 1, `SCOPE-EXEC-UNAUTHORIZED` |
| 2 | same | `EXEC-AUTHORIZED. …` | exit 0, PASS |
| 3 | `Scope: executed=none` | no marker | exit 0, PASS |

Consequence for this round: the only declaration that keeps the gate green is `none`, including for
the 36 seats whose prompts require them to run counters, and for this seat (I ran Python and
read-only git; my trailer below says so and will therefore be reported as
`SCOPE-EXEC-UNAUTHORIZED`). The gate would be measuring a false declaration as clean and an honest
one as a red. Severity is operability, not proof: the tool's own scope line says
`evidence_class: "self-reported declarations; no independent absence-of-execution proof"`. The
marker absence is inherited in shape from rounds 34–38 (`EXEC-AUTHORIZED` count 0 in
`round-34/w1-spec.json` … `round-38/w1-spec.json`), but round 39 is the round in which 36 seats are
ordered to execute and 13 reports are already written, so the red is due now.

### 3.2 Pause-gate docstring contradicts its evaluator (pre-existing, surfaced by this run)

`tools/check-pause-gate.py:4-5` says "A premise counts only if its verdict is one of cleared,
still-holds, changed or unverified", but `tools/check-pause-gate.py:35` sets
`COUNTED = ('cleared', 'still-holds', 'changed')` and lines 109-112 record
`verdict-unverified-not-counted`. A reader of the docstring would expect `premises_verified` 5 and
exit 0 for the shipped gate entry; the tool returns 4 and exit 1 because
`corpus/knowledge/pause-lift-gate-r24.json:85` is `"unverified"`. The selftest pins the code
behaviour (`('unverified-not-counted', …, 1, 4)` at `tools/check-pause-gate.py:214`), so the
docstring is the stale half. Both revisions, so not a round-39 regression — but it is the reason a
reader cannot tell an authored red from a drifted one without reading the source.

## 4. Exact proposed text

For the next wave spec generator, every item prompt (or at minimum the 36 that order commands),
prepended and appended verbatim:

```
EXEC-AUTHORIZED. Close the report with exactly one final line —
`Scope: executed=<comma-separated commands you ran>` — or `Scope: executed=none` if you ran none.
```

and, so that the gate can read the prompts at all, place the spec inside the wave directory as
`spec.json` (`tools/check-seat-scope.py:40`, `REGISTRY, SPEC = "swarm-registry.json", "spec.json"`)
or add a `prompt` field per registry member; `w1-spec.json` at the round root is never read. At
integration, commit `.ufo/waves/round-39/w1/swarm-registry.json` and
`.ufo/waves/round-39/w1-spec.json` so `--revision` mode is evaluable (round-38 precedent: `b0005ae`).

For `tools/check-pause-gate.py:4-5`, replace "one of cleared, still-holds, changed or unverified"
with "one of cleared, still-holds or changed (an `unverified` verdict is valid but is not counted,
and makes the gate exit 1)".

## 5. What I did not do

- No lane file edited, created or deleted; no git/jj mutation; no host or `unshare` probe; no
  package, service, sysfs, mount or `/etc` change; no sudo; nothing installed or upgraded.
- Did not run any gate after the seats finish landing; the worktree numbers above are 06:04Z and
  06:06Z snapshots of a live wave (57 missing, then 13 undeclared) and will move.
- Did not evaluate `check-seat-scope` at an integration revision (none exists yet) and did not
  repair the wave spec, the registry or the pause-gate docstring — L1 owns those files.
- Did not re-measure any axis claim (C1/C2 counters are other seats' items); the byte comparisons in
  `GateBoundary/COMMANDS.txt` are `git show`/`sha256sum` only.

Scope: executed=python3, git (status/ls-tree/show/log/diff/rev-parse), sha256sum, find, grep, mktemp, mkdir, cp, rm
