# ExecRegistry — round 79 wave w1 (seat report)

claim=C2
verdict=MEASURED-MET for the ExecRegistry share — `duplicates=0 shape_ok=2/2 met=1` on the worktree and on a committed fixture at the current tree; `check-registry-coverage --revision` PASS with 119/119 registered and zero findings. The wave-level C2 verdict is the main agent's gate run, not this seat's.

Scope: `SKILL.md` only. Receipts: `ExecRegistry/receipts.json` (argv, cwd, rc, stdout, stderr, sha256; both the pre- and post-ExecInstrument runs).

## Axes
- **Legibility (C2, QUALITY 70):** four non-operative continuation tables are marked, so they stop counting as current rows.
- **Truthfulness (C2):** the two frozen gate rows and the two new r79 gate rows describe interfaces the tools now expose.

## Changes to SKILL.md (8 added, 2 replaced, 0 other lines)
`git diff --numstat -- SKILL.md` → `8 2 SKILL.md`. Post-edit line numbers:

| line | change |
|---|---|
| 5896 | `check-r71-routed-r72`: self-test cell `none: no self-test mode` → `python3 tools/check-r71-routed-r72.py --selftest`; verdict map gains `3 self-test failed (--selftest)`. Replaced in place. |
| 5901 | `count-md-rows-r72`: same edit; code 2 and code 128 unchanged. Replaced in place. |
| 5904 | **added** `measure-unit-deps-r79` (gate; `--revision <REV>`; 0 met / 1 failed / 2 binding refused / 3 self-test failed; selftest `--selftest`, 32 cases; pinned expected.json sha256 `0c09c7a4…add21`, snapshot sha256 `eb9479bea…714c6`; read-only). |
| 5905 | **added** `check-gate-standard-r79` (gate; `--revision <REV>` or `--root <DIR>`; same 0/1/2/3 shape; selftest `--selftest`, 8 cases; read-only). |
| 5977 | `> NON-OPERATIVE — carried for history; the round-71 table is the sole operative registry.` under `## Round 72 — selftest-tally registry row continuation (append-only)` |
| 6014 | same marker under `## Round 73 — registry continuation for the two round-73 instruments (append-only)` |
| 6092 | same marker under `### Round-76 instrument registry (append-only continuation)` |
| 6100 | same marker under `## Gate and probe registry — round 77 addition` |

No historical row was removed or rewritten. The r72/r73 selftest-TMPDIR wording in `count-ul-rows-r73` and `count-uf-rows-r74` is untouched.

SKILL.md sha256: freeze/pre-edit `6b3c64a3bc57664a55ebdb3477d7d94152932489845ca903c0f7de0ad1e38418`; post-edit `97716dd920cca67f3c948ebed02f5a29b56a3afce3e8f93c2b82a449f2a8054d`.

## Measured results
Timeline, each run on the state shown; full stdout in receipts.json.

| state | command | rc | result |
|---|---|---|---|
| freeze `afe1f26…` (pre-edit) | `check-gate-standard-r79.py --revision afe1f…` | 1 | `duplicates=6 shape_ok=0/2 met=0` — matches the declared before-values |
| freeze | `check-registry-coverage.py --revision afe1f…` | 1 | FAIL, two `REGISTRY-ROW-MISSING` (`check-gate-standard-r79.py`, `measure-unit-deps-r79.py`); 117/119 registered |
| worktree, post-SKILL-edit, pre-ExecInstrument tools | `check-gate-standard-r79.py --root .` | 1 | `duplicates=0 shape_ok=0/2` |
| same, fixture `a4d1deb…` (freeze tools + patched SKILL.md, committed on master in scratch) | `check-registry-coverage.py --revision a4d1deb…` | 1 | 119/119 registered, `missing=0`; two `REGISTRY-SELFTEST-UNRESOLVED` at SKILL.md:5896 and :5901 (tools then had no `--selftest`) |
| same fixture | `check-gate-standard-r79.py --revision a4d1deb…` | 1 | `duplicates=0 shape_ok=0/2 met=0` |
| **post-ExecInstrument tree, fixture `020d849…`** (worktree SKILL.md + tools copied and committed on master in scratch) | `check-registry-coverage.py --revision 020d849…` | **0** | **PASS**, 119/119 registered, zero findings |
| same fixture | `check-gate-standard-r79.py --revision 020d849…` | **0** | **`duplicates=0 shape_ok=2/2 met=1`** |
| **post-ExecInstrument worktree** | `check-gate-standard-r79.py --root .` | **0** | **`duplicates=0 shape_ok=2/2 met=1`** |
| worktree | `check-line-endings-r64.py --check` | 0 | `CHECK_LINE_ENDINGS: PASS (395 file(s) checked, 0 violation(s))` |
| worktree | `check-gate-standard-r79.py --selftest` | 0 | `SELFTEST total=8 passed=8 failed=0` |
| worktree | `measure-unit-deps-r79.py --selftest` | 0 | `SELFTEST total=32 passed=32 failed=0` |

**The revision form cannot measure the uncommitted worktree.** Both counters bind `--revision` to a landed commit, so the revision rows use a scratch fixture on `master` whose toplevel was verified equal to its directory before each commit. The fixture tools match the lane tools byte-for-byte at the time each fixture was built. The `--root .` rows cover the worktree directly. This split is disclosed.

## Residual findings
1. **Dependency on ExecInstrument's modes.** The two frozen rows now name `--selftest` modes that exist in the current tools (`tools/check-r71-routed-r72.py`: 4 `--selftest` tokens, `tools/count-md-rows-r72.py`: 3 `--selftest`/`SELFTEST` tokens). I did not run those selftests; they are ExecInstrument's verification, and the gate only checks their presence and the `SELFTEST` token. Main agent should run `python3 tools/check-r71-routed-r72.py --selftest` and `python3 tools/count-md-rows-r72.py --selftest` to confirm the rows' self-test claim is backed by a passing mode.
2. **Verdict cell of `measure-unit-deps-r79`.** Code 2 means revision binding refused (`DEPS_BINDING`, verified in source). Code 1 covers both not-met and an unreadable input (`reason=unreadable:…`, verified in source). Recorded as written.
3. **Unrun by this seat:** the `measure-unit-deps-r79` and `check-gate-standard-r79` counters were not run at the post-ExecInstrument revision for C1 (out of my item's scope); only their selftests and the gate's own `--revision`/`--root` paths were run.

## Deviations and hygiene
- No tool installed or updated; no pacman; no `~/.local/bin` write. Nothing to record under the tooling directive.
- No labrat or subagent spawned.
- The `tools/` modifications visible in `git status` (`tools/check-r71-routed-r72.py`, `tools/count-md-rows-r72.py`) are ExecInstrument's, not this seat's. I did not edit `tools/`; I read them only through `grep -c` and `sha256sum`, and ran the gate counters against them.
- Git: read-only in the lane (`rev-parse`, `show`, `archive`, `diff`, `ls-tree`, `merge-base --is-ancestor`, `status`, `branch`, `remote`, `log`). Commits only inside scratch fixtures after verifying `git -C "$D" rev-parse --show-toplevel` equals `$D`. No commit, stage, stash, checkout, reset or push in the lane.
- `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR=/fast/scratch/hyaku/tsukuroi-r79/ExecRegistry` for every run; no `__pycache__` written by this seat.
- A scratch "simulation" (stand-in tokens appended to frozen tool copies) was run before ExecInstrument landed; it is superseded by the real post-ExecInstrument measurement above and is not counted.
- Scratch tree deleted before yield.

## Checks for the main agent
- `python3 tools/check-gate-standard-r79.py --revision <landed REV>` → expect `duplicates=0 shape_ok=2/2 met=1`.
- `python3 tools/check-registry-coverage.py --revision <landed REV>` → expect `status: PASS`, `missing=0`, no findings.
- `python3 tools/check-line-endings-r64.py --check` → PASS (observed).
- `python3 tools/check-r71-routed-r72.py --selftest` and `python3 tools/count-md-rows-r72.py --selftest` → expect exit 0 (ExecInstrument's; not run here).
