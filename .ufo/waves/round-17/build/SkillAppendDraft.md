# SkillAppendDraft — round 17 scoped findings

Owned draft: `.ufo/waves/round-17/build/drafts/skill-append.md` (about 60 lines; append to SKILL.md after the round-16 section). Read: SKILL.md:1800–1863; `corpus/knowledge/boot-chain-r17.{md,json}`; `l1-capture/*.txt`; `.ufo/waves/round-17/build/spec.json` (item contracts).

## Findings

- [obs] Registry columns and REV text: SKILL.md:1816–1819 (locator, measure-update-recheck: "REV = `HEAD` or 4–64 hex"); SKILL.md:1857 (section-citations, no REV spec).
- [obs] All five revision tools still admit HEAD: `check-section-citations.py:55`, `check-locator-clarification.py:30`, `check-root-dac-correction.py:27`, `check-source-scope-correction.py:26`, `measure-update-recheck.py:38`. The corrected "7–64 hex landed on master; HEAD rejected" text is marked as true only after RevBind* lands.
- [obs] Next-boot verdicts from `boot-chain-r17.md` decision table: linux BOOTED-OBSERVED; linux-lts UNTESTED; snapshot-2 (both) DEGRADED-PREDICTED; snapshot-1 CONSISTENT-PRE42; efi-fallback NOT-A-KERNEL-ENTRY (boot-chain-r17.md:62–67).
- [obs] Operator checks: boot-chain-r17.md:104–115.

## Questions for L1 (schema, not resolved here)

1. `boot-chain-audit.sh` summary rule (CONSISTENT/DEGRADED/UNKNOWN from per-entry verdicts) is not in spec.json or boot-chain-r17.json; the draft marks it [unk].
2. Spec exit codes for `check-boot-chain.py` give `BOOTCHAIN-MISSING` exit 1, while the gate convention reads unreadable input as exit 2. Decide which wins.
3. `check-root-dac-correction.py` and `check-source-scope-correction.py` have no registry row in SKILL.md:1800–1863. Not checked outside that range.

## Not verified

- None of the new tools (`check-boot-chain.py`, `check-freshness-r17.py`, `check-revision-binding.py`, `check-seat-scope.py`, `check-recheck-commands.py`, `boot-chain-audit.sh`) exists in the worktree yet; registry rows are the contract, not observed behaviour.
- No selftest or command was run.

Tooling: none installed or updated.

Scope: executed=none
