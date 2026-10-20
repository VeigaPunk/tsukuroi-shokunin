# FxBranchEdge — shared branch-validation literals + git error classification (source-only)

Worktree HEAD: 68a8ae035fde33360cbbe21dc92ca0eacf0a5b33 (`.git/HEAD`). No execution.

**Verdict: SURVIVES** for the scoped source review. Post-integration runtime: **UNPROVEN** — author selftest/mutation evidence is pinned at prerequisite 51dd9ee; the final execution ledger is pending and was not fabricated.

Acceptance set = regex ∩ ¬`"HEAD"` ∩ check-ref-format (`tools/_revision.py:42,86,89,94`); branch checked before revision (`:135-138`). Judge keeps an identical independent triple first (`tools/check-revision-binding.py:149-153`, same `REV` `:82`). Per literal:
- `feature/x`: accepted when the ref exists; absent → E-BRANCH-MISSING (selftest `branch-nested-missing` `_revision.py:216`).
- `HEAD`: explicit reject (`:86`). `@`: first-char class rejects.
- `a..b`, trailing `master/`, space, `x.lock`, `.hidden`, `-x`, `""`: each rejected by regex or ref-format (shared selftests; judge probes `check-revision-binding.py:387-391`).
Never accepts an invalid name; stricter than git for some valid names (ASCII class) — sound direction, documented (`_revision.py:85`).

Classification matches S061/S062: merge-base rc∈{0,1}→bool else E-GIT-FAILED (`:119-122`; judge `:138-144`); ref-parse rc∈{0,1} else E-GIT-FAILED (`:112-115`); fatal selector in a readable repo → None → per-site INVALID/MISSING (`:98-109`); unreadable repo → E-GIT-FAILED (selftests `git-failed-origin-blob:234`, `not-a-repo:236`); timeout/OSError → E-GIT-FAILED (`:77-80,:92-93`). `clean_env` strips `GIT_*`, sets NOSYSTEM/GLOBAL (`:62-65`). One finding per refusal by construction.

Residual, no in-scope defect: (1) judge `rev_parse`/`ref_exists` (`:126-133`) map any fatal to INVALID/absent, unlike shared — off-probe divergence; judge claims probe-bounded support only (header `:35-38`). (2) judge timeout id E-GIT-TIMEOUT (`:112-113`) vs shared E-GIT-FAILED — judge-internal. (3) tag→blob branch tip yields MISSING "branch ref absent" — contract step 4 (`:18`) conformant.

Evidence read: MutateShared.md 37/37 pristine ×4 @51dd9ee, M1–M3 36/37 exit1 killed, pristine SHA restored; RerunHarness-selftest.txt 40/40 exit0; RerunHarness.md "No post-integration revision was measured". Worktree `_revision.py` byte-identity to that pristine SHA not checkable without execution.

Scope: executed=none
