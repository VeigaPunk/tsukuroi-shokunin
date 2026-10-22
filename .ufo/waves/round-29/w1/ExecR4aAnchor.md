done — the R4a two-word floor now has an independent selftest anchor that kills both routed mutants.

1. [obs] In the sandbox copy of `tools/check-kernel-taint.py`, I added `r4a-quote-too-few-words`: a single 14-character token, which meets the 10-character minimum but violates the two-word minimum. The case expects `KT-QUOTE-TOO-SHORT`; no counter rule changed. Evidence: `/fast/scratch/hyaku/tsukuroi-r29/ExecR4aAnchor/repo/tools/check-kernel-taint.py:1342-1347`; patch: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecR4aAnchor/ExecR4aAnchor.patch`.

2. [obs] Red baseline: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 tools/check-kernel-taint.py --selftest` in the unpatched sandbox copy exited 0; output was `{"cases": 55, "failed": 0, ..., "status": "PASS"}`.

3. [obs] The delivered m1 mutant changes `MIN_QUOTE_WORDS` from 2 to 1 at `/fast/scratch/hyaku/tsukuroi-r29/ExecR4aAnchor/m1/repo/tools/check-kernel-taint.py:77` and includes the new case. Its selftest exited 1 (`cases: 56`, `failed: 1`, `status: FAIL`): `r4a-quote-too-few-words` was accepted with exit 0, no findings, and 6 verified rows instead of the expected `KT-QUOTE-TOO-SHORT`.

4. [obs] The delivered m7 mutant removes the word-count half of `min_length` at `/fast/scratch/hyaku/tsukuroi-r29/ExecR4aAnchor/m7/repo/tools/check-kernel-taint.py:715` and includes the new case. Its selftest exited 1 with the same sole failure: `r4a-quote-too-few-words` was accepted with exit 0, no findings, and 6 verified rows instead of the expected finding.

5. [obs] Green patched result: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 tools/check-kernel-taint.py --selftest` in the patched sandbox copy exited 0; output was `{"cases": 56, "failed": 0, ...}`. Artifact hashes: patch `3e744a9af11cc259f62296c58123b3b4806d07b7502ca99445fefd98f78a195c`; m1 script `b5b364f2e94f67aff285dc95e22e680d05d2915b943c650f1c07fbe2deb69ece`; m7 script `938b39fed8fd4dd99d24a1d8a80bbdde3cfab4412f7702fbec579ffb6dc036af`; patched script `5e9ff59696c28f76f42b78bb585a71cf24304f07a212cd6366f06b3a26bfc82f`.

6. [inf] The one-word, long-token fixture is sufficient to independently expose both named regressions because each mutation makes that fixture pass the length check. [unk] No other R4a mutant variants were exercised; this result is scoped to m1 and m7. No blockers.

Scope: read=round-29 declaration, round-28 routed defect and residual m1/m7 evidence, check-kernel-taint.py fixture code; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecR4aAnchor.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecR4aAnchor/ExecR4aAnchor.patch, /fast/scratch/hyaku/tsukuroi-r29/ExecR4aAnchor/m1/repo/tools/check-kernel-taint.py, /fast/scratch/hyaku/tsukuroi-r29/ExecR4aAnchor/m7/repo/tools/check-kernel-taint.py; executed=baseline, m1, m7 and patched `--selftest`; sandbox `git clone`/`checkout`, `git diff`, `sha256sum`
Model: openai-codex/gpt-6-luna
Installs: none