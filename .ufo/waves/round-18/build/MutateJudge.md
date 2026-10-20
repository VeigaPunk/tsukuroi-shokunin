# MutateJudge — patchless bounded probes

[obs] Axes challenged: C2 operability and judge calibration; no ordinal claim. Model: openai-codex/gpt-6.1-sol. No installations.

[obs] Sandbox `S=/tmp/tsukuroi-r18-mutate-judge-QRXd9I08`, cloned `--no-hardlinks`, detached at `51dd9eeaa305539fa3cfc6ee275978dc18043b79`, origin removed. `T=/tmp/tsukuroi-r18-mutate-judge-QRXd9I08/tools/check-revision-binding.py`. Production and fixtures were untouched.

[obs] Same detector throughout: `python3 T --selftest`. Expected: pristine/restored exit 0; each mutant rejected. Initial pristine and all three restored runs exited 0 with identical output:

```text
CHECK_REVISION_BINDING_SELFTEST: PASS (40 cases, 40 passed, 0 failed)
```

| Mutant: exact original site | Actual output / caught finding | Verdict |
|---|---|---|
| `/tmp/tsukuroi-r18-mutate-judge-QRXd9I08/tools/check-revision-binding.py:345`: delete branch-first probe | Exit 1; traceback `KeyError: 'branch-first'` at mutated :644. No normal selftest summary or stable finding-id. | Killed, crash-shaped |
| `/tmp/tsukuroi-r18-mutate-judge-QRXd9I08/tools/check-revision-binding.py:351`: drop binding-ID equality; accept doubles | Exit 1; `CHECK_REVISION_BINDING_SELFTEST: FAIL (40 cases, 38 passed)`; `shared-double-bound-not-consistent: got=(True, True, 9, 9, 0) want=(True, False, 9, 8, 1)`; `shared-double-failing-probes: got=set() want={'single-id'}`. | Killed |
| `/tmp/tsukuroi-r18-mutate-judge-QRXd9I08/tools/check-revision-binding.py:355`: expected `ID_GIT` → `ID_PUSHED` | Exit 1; `CHECK_REVISION_BINDING_SELFTEST: FAIL (40 cases, 29 passed)`; 11 failures, including `all-consistent: got=(0, 9, []) want=(9, 9, [])`. | Killed |

[obs] SHA-256 before **every** mutation and after **every** restoration:
`0110c0b83e2cfe8368eed94b751043f82d6e2561c0c084c43ab2e27a2f4bf590`.
Mutated hashes, table order:
1. `dc4467c73ccf73ee78f7b5ff74cc678bb8cdd9a29da7b4122f58f1f9594ac0c0`
2. `f7cefaa409bca23f15460ddffbb83a574600e0c4f3000623758c820bd25529fa`
3. `00d2c4f57f7b7e3b3ab006b0e43c788fd1d49d37df7d7f8d12825904aed74afd`

[obs] Three isolated kills; zero survivors/inconclusive. Exact bytes restored; no patch retained. No integration/admission performed.

Scope: executed=mktemp -d; git clone --no-hardlinks --no-checkout; git -C S checkout --detach 51dd9eeaa305539fa3cfc6ee275978dc18043b79; git -C S remote remove origin; python3 T --selftest ×7; sha256sum T ×7. All execution sandbox-only.
