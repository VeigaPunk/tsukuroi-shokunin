# MutateShared

Axes challenged: operability (C2 refusal semantics), calibration (bounded evidence). Model: `openai-codex/gpt-6.1-sol`.

[obs] Own `--no-hardlinks` clone `/tmp/tsukuroi-r18-mutate-shared.B3RTEkBf`, detached at `51dd9eeaa305539fa3cfc6ee275978dc18043b79`; origin removed. Only its `tools/_revision.py` implementation was mutated; fixtures unchanged.

Detector: `python3 /tmp/tsukuroi-r18-mutate-shared.B3RTEkBf/tools/_revision.py --selftest` (60-second bound).

[obs] Seven sequential runs: pristine, M1, restored/pristine, M2, restored/pristine, M3, restored. Exits: **0,1,0,1,0,1,0**. All four pristine/restored outputs:
`REVISION_SELFTEST: PASS (37 cases, 37 passed, 0 failed)`.
All three mutant outputs:
`REVISION_SELFTEST: FAIL (37 cases, 36 passed, 1 failed)`.

1. **M1, killed.** `/tmp/tsukuroi-r18-mutate-shared.B3RTEkBf/tools/_revision.py:132-134`: moved branch validation after revision-syntax refusal. Caught:
   `precedence-branch-first: got=('err', 'E-REVISION-INVALID') want=('err', 'E-BRANCH-INVALID')`.
   Mutated SHA-256: `a723698dd6b2c03e920516c76e24d9f37c6f9586a25bf5f0fc13d2bc7114f9fc`.
2. **M2, killed.** `/tmp/tsukuroi-r18-mutate-shared.B3RTEkBf/tools/_revision.py:118`: replaced fatal merge-base refusal with `return False`. Caught:
   `git-failed-origin-blob: got=('err', 'E-REVISION-NOT-PUSHED') want=('err', 'E-GIT-FAILED')`.
   Mutated SHA-256: `c9fd7e69572aadd813776f3016da26c710c0554327bb1104910b8fd83f73f879`.
3. **M3, killed.** `/tmp/tsukuroi-r18-mutate-shared.B3RTEkBf/tools/_revision.py:142-149`: moved local-ancestor refusal after remote checks. Caught:
   `unlanded-single-id: got=('err', 'E-REVISION-NOT-PUSHED') want=('err', 'E-REVISION-NOT-LANDED')`.
   Mutated SHA-256: `1237e18dad2ffb60f93b4ef9fa3030d6344c90f39110410fb56b026fcfec3da1`.

[obs] Before every mutation and after every restoration, file SHA-256 was exactly `8425a3c3716ba8d19883b9fa30e0c8e6d594f5a9a724baf001c35f32b0c7432f`. Exact bytes restored after each failed detector. No production edits, fixture weakening, installations, or admission judgment.

Scope: executed=mktemp -d; git clone --no-hardlinks; git checkout --detach; git remote remove origin; sha256sum ×7; python3 /tmp/tsukuroi-r18-mutate-shared.B3RTEkBf/tools/_revision.py --selftest ×7.
