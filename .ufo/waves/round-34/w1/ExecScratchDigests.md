All five oversize "mutant vs frozen" diffs regenerate byte-for-byte from committed lane bytes: 5 of 5 sha256 matches, 0 mismatches, each regenerated in a disposable sandbox clone; the scratch files are now redundant and need not be cited again.

1. [obs] The five files, with size and sha256 as read on 2026-10-23:
   - `.ufo_waves_round-33_a3w2_MutAfterDropGlobal_mutant-vs-frozen.patch` 3088823 `0cc2aa31b3fcb8d677bf69417b3591c3f001b80018d94ba522f370df222a77d0`
   - `.ufo_waves_round-33_a3w2_MutAfterHomeKeep_variant-vs-frozen.patch` 3088905 `702eed9ebc4802b3c9aed75ab9dfb90c3e1f862eae5451d5b2787e03f302b85a`
   - `.ufo_waves_round-33_a3w2_MutAfterOneNameCopy_mutant-vs-frozen.patch` 3089115 `bdb62e5f8772f8f46ecd6cca4a4f539c2fc638515b7b4c9f0e9f7082ef6ec835`
   - `.ufo_waves_round-33_a3w2_MutAfterPathCopy_frozen-to-mutant.patch` 3088859 `21b8f79d21432f28dc733624c8d42926225010dd71e7a1c33c165e1fcf140bad`
   - `.ufo_waves_round-33_a3w2_MutAfterV4Spread_variant-vs-frozen.patch` 3088930 `3cfb5a669b99d4c519f1a8785f90e152581cda366113b9186d2354851ce393a7`
   Evidence: `sha256sum` and `stat -c '%n %s'` over `/fast/scratch/hyaku/tsukuroi-r33a3/oversize/.*.patch`, exit 0; the files are dotfiles, which is why plain `*.patch` does not list them.

2. [obs] Each file is exactly `git diff 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0 <sandbox mutant commit>`, the command the seats recorded. HomeKeep's committed preparation record shows both captures, `git diff 9c89ff4f… 16f2455f…` → `variant-vs-frozen.patch` and `git diff c8fcfbf6… 16f2455f…` → `mutation-vs-landed.patch` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/MutAfterHomeKeep/preparation.json`, last two `events`). PathCopy records the same for `9c89ff4f… 021be23` and pins the result at `21b8f79d…`, 3088859 bytes (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/MutAfterPathCopy/commands.txt:11-12`). All five patches are therefore the full 9c89ff4f→c8fcfbf6 history (347 diff sections: 338 files under `.ufo/waves/round-33/a3w1/` and `a3/`, 9 elsewhere) plus one mutation, which is why each is about 3 MB.

3. [obs] Four variants are reproduced exactly from committed bytes: re-issue the committed mutation-only patch on the committed parent `c8fcfbf6`, and the resulting file equals the sha256 that the seat's committed evidence records, and the resulting tree equals the tree of the seat's original sandbox commit:
   - DropGlobal: patch `.ufo/waves/round-33/a3w2/MutAfterDropGlobal/mutant-vs-landed.patch` (blob `23103946…`, sha256 `a0d5a3f0…`) → file `050ca5de…`, tree `a7b14cdf…` = commit `7d82afb3…`'s tree.
   - HomeKeep: patch `.../MutAfterHomeKeep/mutation-vs-landed.patch` (blob `e37db327…`, sha256 `75a40afb…`) → file `212d5c01…`, tree `ae9981d6…` = commit `16f2455f…`'s tree.
   - OneNameCopy: patch `.../MutAfterOneNameCopy/mutation-only.patch` (blob `6c38faa6…`, sha256 `08bc928f…`) → file `557d9267…`, tree `aff12d5a…` = commit `43aad3aa…`'s tree.
   - V4Spread: patch `.../MutAfterV4Spread/mutant-only.patch` (blob `1b96866b…`, sha256 `f9734289…`) → file `16c354de…`, tree `c1f47750…` = commit `711daccc…`'s tree.
   The patch blobs are identical at `ca768636` and at the claim base `6de666c427ba9aa6b4350561980bde8d0e7c261d` (`git rev-parse <rev>:<path>` for each; exit 0). The expected file hashes come from committed seat evidence: `MutAfterDropGlobal/hashes-mutated.txt:1`, `MutAfterHomeKeep/preparation.json` `mutated_sha256`, `MutAfterOneNameCopy/mutant-hashes.json` `stdout`, `MutAfterV4Spread/ordinary-mutated.json` `stdout.source_sha256`.

4. [obs] PathCopy is the one variant with no committed mutation patch. Its mutation is stated in committed prose (`.../MutAfterPathCopy.md:3`, `.../MutAfterPathCopy/commands.txt:13`): `clean_env()` returned `os.environ["PATH"]` instead of the fixed `"/usr/bin:/bin"`. The script applies exactly that one substitution to the committed `c8fcfbf6` blob; the result has sha256 `e1f49f1e…` = `hashes.json` `mutant_sha256`, and the resulting tree `f16ec8c9…` equals commit `021be23c…`'s tree. The bytes are therefore verified even though the edit must be re-issued from prose.

5. [obs] Regeneration commands, exactly as run (one per file; first use clones the lane, later uses reuse the clone; push URL is disabled):
   - `bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecScratchDigests/regenerate.sh MutAfterDropGlobal` → 3088823, `0cc2aa31…`, match yes
   - `... regenerate.sh MutAfterHomeKeep` → 3088905, `702eed9e…`, match yes
   - `... regenerate.sh MutAfterOneNameCopy` → 3089115, `bdb62e5f…`, match yes
   - `... regenerate.sh MutAfterPathCopy` → 3088859, `21b8f79d…`, match yes
   - `... regenerate.sh MutAfterV4Spread` → 3088930, `3cfb5a66…`, match yes
   The script (sha256 `ef6fe1ea1c1a899abde4d923c14ca30cd3f0a7f3b9d0a591f86c9365d033fecc`, 5714 bytes) was also run cold with an empty `WORK`: it cloned, built and matched all five again with the same hashes. Observed stdout: `/fast/scratch/hyaku/tsukuroi-r34/ExecScratchDigests/regenerate-run.txt` and `.../cold-run.txt`; regenerated copies are under `/fast/scratch/hyaku/tsukuroi-r34/ExecScratchDigests/regen/patches/`.

6. [obs] Determinism: git 2.56.0, the host version the seats used. The seats' plain command and the script's pinned form (`-c diff.algorithm=histogram -c diff.mnemonicprefix=true -c diff.colormoved=plain`) give the same bytes, and a myers run of the V4Spread diff also gives `3cfb5a66…`, so these diffs are algorithm-insensitive. `git diff <tree> <tree>` emits no commit id, so the clone's new commit id cannot change the bytes; the regenerated trees equal the original ones anyway.

7. [obs] Deliverables: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecScratchDigests/digests.txt` records per file the size, sha256, committed inputs (base commits, mutation patch blob and sha256, evidence hash), the regeneration command, regenerated sha256 and `match: yes`; `regenerate.sh` is the runnable script. The 3 MB outputs were only read and hashed; nothing over 1 MiB was copied or committed.

8. [inf] Residual risk: only PathCopy's mutation input is prose rather than a committed patch, and its reconstruction is pinned by two independent committed values (mutated-file sha256 and tree equality), so a wrong re-issue would be caught. Losing `/fast/scratch/hyaku/tsukuroi-r33a3/oversize/` would cost nothing: every file is regenerable from the lane alone with the recorded command.

9. [obs] This repairs routed defect 6 of the round-33 spot-check (`corpus/lessons/round-33-verifier-spotcheck.md:34` and `:181`): the diffs no longer exist only in scratch; their exact bytes are reproducible from committed bytes. This seat made no C1/C2 judgment and wrote no lane file outside its seat directory and this assigned report.

Scope: read=/fast/scratch/hyaku/tsukuroi-r33a3/oversize/ (5 patches, hashed only), lane commits 9c89ff4f, c8fcfbf6, ca768636 and claim base 6de666c via read-only git, .ufo/waves/round-33/a3w2/MutAfter* committed evidence, corpus/lessons/round-33-verifier-spotcheck.md, corpus/QUALITY.md, round-34 w1-spec; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecScratchDigests/regenerate.sh, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecScratchDigests/digests.txt, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecScratchDigests.md, /fast/scratch/hyaku/tsukuroi-r34/ExecScratchDigests/; executed=timeout-bounded read-only git (show, rev-parse, ls-tree, cat-file, diff), sha256sum, stat, ls, git clone --no-local plus checkout/reset/apply/add/commit/diff and one-line python edit confined to /fast/scratch/hyaku/tsukuroi-r34/ExecScratchDigests/, bash regenerate.sh (twice, one cold)
Model: opencode-go/deepseek-v4.1-flash
Installs: none
