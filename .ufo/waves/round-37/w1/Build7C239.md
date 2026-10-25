# Build7C239 — design item 7/12: C2 action-override fixture

- Seat: `Build7C239` (executor), tsukuroi lane round 37 wave 1, attempt 1.
- Axis: operability; build: C2 action-override fixture. Milestone: independent runnable design.
- Scope: read-only lane use; deliverable = an isolated runnable check (gate) plus a precise
  patch proposal in this seat directory. No lane/fleet/sibling/source repo mutated; no
  pacman/host change; no delegation; no background jobs; no wave spawns.

## Tooling record (per RULES.md)

Read first: `/home/vgpnk/.omp/agent/RULES.md` lines 1-14 (tooling directive). No tool
installed or updated; no pacman (transactions paused host-wide, none used); no git/jj
write anywhere outside the mktemp fixture repos described below. All lane reads were
`read`/`grep`/`git show` (immutable) or live read-only `journalctl` queries.

## Evidence opened this round (all actually read/run; quotes located)

1. `SCORECARD.md:1909-1916` — routed defect: "action-override classification. Before:
   `corpus/knowledge/journalctl-v262-field-filter-r36.md` carries the 16-term table and
   lacks the two rows. After: the note carries exactly the corrected 15-term predicate
   table, the third-state (`-n`) row …, and an action-override classification row; the
   rejection line stays verbatim."
2. `.ufo/waves/round-36/w2/W2CritC2Depth/c2-depth-ruling.md` §5, lines 87-101 — the
   correction spec: "separate **action overwritten / last action selected** from genuine
   accepted field-enumeration scope selectors. Preserve exact argv order. Describe the
   scope list as 'not rejected by this guard,' not as blanket success or
   output-preservation guidance." Also lines 89-93: matrix `live_list_boots` =
   `journalctl --no-pager -F PRIORITY --list-boots` "exits 0 but produces 541 stdout
   bytes, not the plain field list's 12. … `-F` assigns `ACTION_LIST_FIELDS`, then
   `--list-boots` assigns `ACTION_LIST_BOOTS`."
3. `.ufo/waves/round-36/w1/SrcSystemdNews/journalctl.v262.c` — action assignments:
   `--list-boots` → `ACTION_LIST_BOOTS` (lines 812-814); `--disk-usage` → `ACTION_DISK_USAGE`
   (824-826); `--sync` → `ACTION_SYNC` (856-858); `--header` → `ACTION_PRINT_HEADER`
   (877-879); guard `IN_SET(arg_action, ACTION_LIST_FIELDS, ACTION_LIST_FIELD_NAMES) &&
   field_list_has_scope_options()` + `log_error_errno(SYNTHETIC_ERRNO(EINVAL), …)`
   (lines 958-960).
4. Current note, `corpus/knowledge/journalctl-v262-field-filter-r36.md` lines 42 & 44 —
   the two misclassifying rows: "not a limiter | `--output-fields=`; `--disk-usage`; `--header`; `--sync` | **WORK** …" and "not a limiter | `--boot=all`; `--list-boots`; `--show-cursor`; `--merge` | **WORK** …".
5. `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json` — cell `live_list_boots`
   (argv `journalctl --no-pager -F PRIORITY --list-boots`, exit 0, stdout 541 bytes);
   `ext_header_F` / `ext_sync_F` / `ext_diskusage_N` (action flag **before** `-F`/`-N`;
   `-F`/`-N` last → field output).
6. Live read-only probes on this host, `journalctl --version` → `systemd 262 (262-1-arch)`;
   table in `patch-proposal.md` (8 argv rows with exit/stdout, incl. previously unmeasured
   order pairs `-F PRIORITY --disk-usage`, `-F PRIORITY --header`, `--list-boots -F
   PRIORITY`).
7. `.ufo/waves/round-36/lessons/round-36-verifier-spotcheck.md` lines 64-66 — corrections
   "recorded but **not yet applied**".

## Deliverable: the gate

`Build7C239/check_c2_action_override.py` — standalone stdlib Python (no deps), read-only.
```
python3 check_c2_action_override.py --note <PATH>            # worktree note file
python3 check_c2_action_override.py --revision <REV> --lane <ROOT> [--branch master]
                                                             # immutable committed-read
python3 check_c2_action_override.py --selftest               # hermetic suite
```
Exit: 0 PASS, 1 FAIL, 2 CANNOT_EVALUATE. Assertions:

- `A-reject-line-verbatim` — exact 84-byte scope-rejection sentence still present.
- `B-action-override-row` — ≥1 decision-table row carries an action flag +
  last-action-selected/override phrasing + output-identity ("boot table"/"disk usage"/
  "header information"/not field list) + order markers.
- `C-no-blanket-work` — no WORK row groups an action flag without the override explanation.
- `D-limiter-rows-15` — the 15 `field_list_has_scope_options()` rows survive (non-regression).

## Measured behavior (observed, this round)

| run | result |
|---|---|
| `--selftest` (embedded baseline/corrected/derived fixtures + mktemp git sandbox, top-level verified equal to fixture root before each commit) | `CHECK_C2_ACTION_OVERRIDE_SELFTEST: PASS (6 cases, 6 passed, 0 failed)`, exit 0 |
| `--note` on the **unchanged baseline** (real lane file) | **FAIL**, exit 1: `A` PASS, `B` FAIL (no action-override row), `C` FAIL (2 blanket WORK rows: `--disk-usage; --header; --sync` and `--list-boots` … `| **WORK** |`), `D` PASS |
| `--revision 0e5f70fadba12bc9bbb9db564c2262c2c0194535 --lane <lane>` (committed-read at lane HEAD) | **FAIL**, exit 1, same findings — gate also fails on the bound revision, not just the worktree |
| `--note` on the **after-state** note (patch proposal applied in mktemp) | **PASS**, exit 0 (A/B/C/D all PASS; 3 action-override rows found) |
| `--revision <after-sha> --lane <fixture-repo>` (committed-read) | **PASS**, exit 0 |
| `--revision 0000…0 --lane <fixture-repo>` (non-landed) | `CANNOT_EVALUATE [E-REVISION-INVALID]`, exit 2 |

## What the check measures (before → after)

- **Before (baseline)**: the note's decision table groups `--list-boots`, `--disk-usage`,
  `--header`, `--sync` under "not a limiter → WORK", which is wrong as a *classification*:
  those four are action flags that replace `-F`/`-N` when they come later on the command
  line, so exit 0 then means the *other action ran* (boot table / disk usage / header /
  sync output), not that field enumeration succeeded. The gate fails on the missing
  action-override row (B) and on the two blanket WORK rows (C).
- **After (corrected note)**: the table carries three new rows (action override, last
  action selected; same for `--disk-usage`/`--header`/`--sync`; reverse-order row showing
  `-F`/`-N` last still yields genuine field enumeration and a still-applicable guard),
  the "not a limiter" rows retain only true non-action options (`--output-fields=`,
  `--root=`, `-D`, `--user`, `--system`, `--namespace=`, `--boot=all`, `--show-cursor`,
  `--merge`), the rejection line stays verbatim, and the 15 limiter rows are untouched.
  The gate measures exactly that state.

## Limits / risks

- The gate is content-conformance, not a semantic proof; it checks the note's decision
  table, not journalctl's binary (live probes in `patch-proposal.md` back the row
  semantics on this host, systemd 262).
- Live `journalctl -F PRIORITY --list-boots` today produced 262 bytes of boot table (the
  r36 matrix recorded 541 on 2026-10-23); the class (boot-table output, not field list) is
  what the classification and the guard rely on, not the byte count — the proposed row
  cites output identity ("boot table"), not a fixed byte count.
- Companion items (Build5C237/Build6C238) cover the 15-term count and the `-n` three-state
  rows; this gate keeps the 15-row guard (D) to avoid overlap regression.
- No lane file was touched; the only git repositories used were fresh `mktemp` fixtures
  whose top-level was verified equal to the fixture root before every commit.

## Artifacts

- `Build7C239.md` (this report)
- `Build7C239/check_c2_action_override.py` (runnable gate)
- `Build7C239/patch-proposal.md` (precise before→after patch wording + live evidence table)

---

Final answer (≤6 lines):

1. Built an isolated runnable gate for the C2 action-override classification correction.
2. On the unchanged baseline (worktree and lane HEAD 0e5f70f) it FAILS exit 1: no
   action-override row, two blanket WORK rows misclassifying `--list-boots`/`--disk-usage`/
   `--header`/`--sync`.
3. The after-state it measures: decision table with last-action-selected rows (order-
   preserved), true non-action rows only, rejection line verbatim, 15 limiter rows intact.
4. Corrected-note fixture passes the gate (worktree and committed-read, exit 0); selftest
   6/6; non-landed revision → exit 2.
5. Patch proposal with live evidence (systemd 262 probes) is in `Build7C239/patch-proposal.md`.
6. No lane/fleet/sibling writes, no installs, no pacman/host changes; fixture git only in
   mktemp with top-level verified before commits.
