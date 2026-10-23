# RevHeaderGate — review of tools/check-knowledge-header.py at 879daa95

VERDICT: the gate answers every assigned question as designed — it fails a note
missing `source:` or `verified-at:` (base receipt exit 1, 11 findings over 10
notes), binds the revision through `tools/_revision.py`, runs every git child
under the fixed allow-list, applies the corpus's own last-occurrence supersede
convention, and its should-fail selftest cases are real; four low-severity
residuals below, none of which changes the verdict.

1. [obs] **Missing-key failure works and was shown red before the fix, as the
   routed defect requires** (round-33 spot-check §5 item 1: "fails a knowledge
   entry missing either field, and show it red before the fix"). `evaluate()`
   emits one `KNOWLEDGE-HEADER-MISSING` per absent key, and `run()` maps any
   finding to FAIL/exit 1 (`tools/check-knowledge-header.py:205-221, :270-308`).
   Receipt at the base `.ufo/waves/round-34/w1/ExecHeaderGate/base-6de666c.
   stdout.json`: exit 1, `kill-oom-boundary-r33.md` flagged separately for
   `source:` and `verified-at:` (the round-33 defect note). Tip receipt
   `.ufo/waves/round-34/w2/GatesAfterNoHarm/tip-check-knowledge-header.jsonl`:
   exit 0, `note_count` 54, `complete_count` 54, `clean_count` 54, `findings` [].

2. [obs] **Revision binding is the shared module.** The gate imports
   `_revision` from `<lane>/tools` after a bootstrap that requires
   `tools/_revision.py` to exist there (`:70-83`), calls `_revision.bind(repo,
   revision, branch)` and converts `RevisionError` to a single CANNOT finding
   (`:289-300`); `branch_tip` is recovered for the payload (`:291-295`). This is
   the QUALITY 28 pattern and matches `check-recheck-commands.py:918-920`.
   Mutation-seat evidence confirms the refusal classes work end to end
   (`E-REVISION-NOT-LANDED`, `E-LANE-UNRESOLVED` in
   `w1/ExecHeaderGate/exits.txt` runs 6-7).

3. [obs] **Its own git child environment is the fixed allow-list.** The only
   `subprocess.run` in the file (`:110-112`) passes
   `env=_revision.clean_env()` — the literal six-key dict
   {`PATH`=`/usr/bin:/bin`, `GIT_OPTIONAL_LOCKS`=`0`, `GIT_PAGER`=`cat`,
   `LC_ALL`=`C`, `GIT_CONFIG_NOSYSTEM`=`1`, `GIT_CONFIG_GLOBAL`=`/dev/null`} —
   to `ls-tree`, `cat-file` and `show`. No ambient name is read anywhere in the
   gate (no `os.environ`/`getenv`); selftest sandbox git calls use the same
   `git()` helper (`:362-365`). `sys.dont_write_bytecode` (`:44`) keeps the
   import read-only. [inf] The gate is not among the nine C1 probe targets, so
   this is observed conformance with the same idiom, not probe coverage.

4. [obs] **The last-occurrence rule is load-bearing on real notes, and the
   early-bad/late-good case is the convention, not a hole.** Nineteen notes
   carry two `source:` lines, fourteen two `verified-at:`, fifteen two
   `recheck:` at the tip. In every sampled pair the FIRST line is the stale or
   pointer-only one and the LAST is operative — e.g.
   `journal-boot-plane.md` `recheck:` :9 ("Appendix probe command set", no
   cadence) vs :441 ("30d; procedure: …"), `pause-lift-gate-r24.md` :3
   (prose, no cadence) vs :94 ("on-release"), `aur-risk-plane.md` :15 vs :347
   ("90d"). A first-occurrence rule would mark at least four long-standing
   admitted notes red. The corpus texts themselves say "supersedes the
   pointer-only `recheck:` line above" (`adjacency-handoffs-fleet-r1.md:222`,
   `aur-risk-plane.md:348`), and `check-recheck-commands.py:441-450` implements
   the identical last-line rule. The dangerous direction is still caught: a
   late BAD value is operative and fails. So an early bad value plus a late
   good one passes only when the corpus intends the later line to supersede —
   no defect. [inf] Residual ambiguity: two genuine, non-superseding
   `verified-at:` lines would silently resolve to the later one; the corpus has
   no such note today.

5. [obs] **The should-fail selftest cases are real.** Each should-fail case
   commits a fixture note to a hermetic mktemp repository, runs `run()` in
   process, and asserts exit code AND finding ids AND a detail substring AND
   counts — e.g. `missing-source`/`missing-verified-at`/`missing-recheck`
   (`:411-421`), `verified-at:` undated and impossible `2026-13-45`
   (`:423-430`), `recheck:` without date or cadence (`:431-433`), fenced-only
   keys (backtick and tilde, `:439-443`), mid-line keys (`:445-447`), indented
   key (`:449-450`), plus binding refusals (`:457-475`). A case that failed for
   the wrong reason still mismatches id/detail/counts. Receipts: selftest
   25/25 PASS pristine, and MutHeaderGateKeys' `m1` mutant (dropping
   `verified-at` from KEYS) exits 1 — the suite kills a real mutant.
   Pass-direction fixtures also pin last-occurrence in BOTH directions
   (`appended-block-supersedes-pointer`, `last-recheck-is-operative`,
   `:444-448`, `:453-455`).

6. [obs] **Low — `source:` has no value rule.** `RULES` maps `source` to `None`
   (`:202`): a bare `source:` line or `source: x` satisfies the gate. QUALITY 8
   requires the field's presence; sibling seat MutHeaderGateShortcut owns the
   junk-value question. Recorded here as a named residual gap, not a routed-
   defect failure.

7. [obs] **Low — docstring overclaim on fence parity.** The docstring (`:18-20`)
   says fenced keys "is not a header — the same rule `check-recheck-commands.py`
   applies". That sibling's `recheck_line` (`check-recheck-commands.py:448-449`)
   does NOT exclude fenced blocks; the new gate is stricter (a `recheck:` only
   inside a fence counts as MISSING). The divergence is fail-safe (red, never a
   pass) and self-tested, but the docstring misstates the sibling rule.

8. [obs] **Low — `has_date` accepts any line containing one real calendar
   date.** A `verified-at:` carrying `2026-13-45, corrected 2026-10-23` passes
   (`:181-188` iterates all matches and needs only one valid); the intent is
   "carries an ISO date", and the detail message for a value with ONLY an
   impossible date ("ISO date is not a calendar date") exists, so the residual
   is a sloppy-value tolerance consistent with last-occurrence philosophy.
   [inf] Also, `complete_count` counts presence, not validity — a naming nit,
   `clean_count` is the strict figure.

9. [obs] **Low — `--lane` is parsed twice, inconsistently.** `_lane_flag`
   (`:61-67`) takes the FIRST `--lane` (and a trailing bare `--lane` becomes
   `""` → `Path("")` → cwd) to locate `tools/_revision.py`, while argparse
   takes the LAST for `repo` (`:286`). With two different `--lane` values the
   module and the repo can diverge; still bounded, since the module path must
   hold `_revision.py`. No seat-visible effect on the documented CLI.

10. [inf] **`import _revision` binds the worktree's bytes, not the bound
    revision's.** Same convention as the sibling gates (`check-recheck-commands
    .py:54-55`); under run-receipt the tool runs from a private clone at the
    tool revision so the two coincide. A dirty worktree `_revision.py` changes
    gate behaviour without changing the receipt's `tool_revision` — carried
    convention debt, not a new defect.

Residual risk: low. The routed defect is closed with the required red-before/
green-after evidence, the only value-bearing rules behave as documented, and
every residual above either fails safe or matches corpus convention. No further
actionable finding in scope.

Scope: read=committed bytes at 879daa95/3457f287/6de666c via read-only git
(show, log, ls-tree, grep, diff, rev-parse) of tools/check-knowledge-header.py,
tools/_revision.py, tools/check-recheck-commands.py, tools/check-seat-scope.py,
SCORECARD declaration, corpus/QUALITY.md:1-63,
corpus/lessons/round-33-verifier-spotcheck.md, corpus/knowledge notes, SKILL.md
registry rows, LOG.md, and the wave receipts under .ufo/waves/round-34/w1 and
w2 (jq/grep/sha256sum text filters only; the gate and its selftest were never
executed by this seat — NO-EXEC); wrote=.ufo/waves/round-34/w2/RevHeaderGate.md
and .ufo/waves/round-34/w2/RevHeaderGate/evidence.md; executed=none
Model: devin/swe-2 (workstation context)
Installs: none

Scope: executed=none
