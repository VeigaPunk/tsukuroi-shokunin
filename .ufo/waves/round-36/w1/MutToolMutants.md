# MutToolMutants — round-36 wave 1 (C1 after-mutant design)

Seat: `MutToolMutants` (mutation-tester). Lane: `tsukuroi-shokunin`.
Claim axis: C1 (operability) — the five live tools stop copying the ambient environment into
child processes. Deliverable: the six after-mutant patches for wave 2, plus the evidence that
each is a real leak.

Date (UTC): 2026-10-24. Times pasted from `date -u +%H:%M:%SZ` at write time.

## Result

Six unified diffs against the **changed tree** (base + `c1-five-tools.diff`) are written in
`.ufo/waves/round-36/w1/MutToolMutants/`: `mutant-1.diff` … `mutant-6.diff`, plus `mutants.md`,
`restoration.json`, `detector-det2.py`, `detector-results.json`, `samples.json`,
`detector-runall.py`. No production file was edited; every byte this seat wrote is inside its own
seat directory.

Each mutant restores exactly one ambient-copy builder, and each is a **real** leak — measured,
not inferred.

| id | file | site | ambient copy restored | child that receives it | pristine → mutant (marker leaks) |
|---|---|---|---|---|---|
| m1 | `tools/check-revision-binding.py` | `clean_env()` | `os.environ` minus `GIT_*` | `git --no-pager -c core.hooksPath=… -C <repo>` | 0 → 6 (and 0 → 9358 on `--selftest`) |
| m2 | `tools/check-report-receipts.py` | `find_receipts()` env | `os.environ` minus `GIT_*` | `git -c user.name=tsukuroi-round30-receipt-check -C <lane>` | 0 → 2 |
| m3 | `tools/score-census-handoff-r32.py` | `live_check()` env | `os.environ` minus `TSUKUROI_*` | `/usr/bin/bash <census>.sh` → `journalctl`, `head`, `tr`, `date` | 0 → 1699 |
| m4 | `tools/mutants-btrfs-space-r30.py` | `run_case()` env | `os.environ` minus `GIT_*` | `/usr/bin/python3 …/check-btrfs-space-r30.py --tree …` | 0 → 84 |
| m5 | `tools/run-receipt.py` | `env()` | `os.environ` minus `GIT_*` | `git -C <lane> rev-parse …`, clone/`ls-files`, then the receipted tool | 0 → 16 |
| m6 | `tools/check-report-receipts.py` | fixed dict `PATH` | ambient `PATH` only, `os.environ["PATH"]` | `git -c user.name=… -C <lane>` — PATH value only | PATH 0 → 4 (no marker, by design) |

## Method

Detector: `detector-det2.py`. It runs the target under
`strace -f -e trace=execve -v -s 8192` — the same execve-environment mechanism the frozen probe
uses (`tools/probe-child-env-allowlist-r34.py`: "observes every process a target starts with
`strace -f -e trace=execve -v`, so it reads each child's real argv and environment"). The ambient
environment carries a run-unique marker name `R36LEAKMARK=leak-<pid>`; a child whose traced envp
carries it received it from the ambient environment. The detector also reports any child whose
`PATH` is not the fixed `/usr/bin:/bin`.

Each mutant was run three ways: **pristine changed tree** → **mutant tree** → **restored**
(reverse-apply). Results:

* m1–m5: marker leaks 0 on pristine, >0 on mutant. Same command, same exit code.
* m6: marker leaks 0 on both (it copies a *value*, not a *name*); the non-fixed-PATH count is 0 on
  pristine and 4 on mutant. m6 is the shape that closes round 34's `MutPathCopy` gap
  (`.ufo/waves/round-34/w2/MutPathCopy.md`, `leaking=0/27`) — `os.environ["PATH"]` yields the
  *exact* ambient PATH string the probe's PATH value channel matches.
* The pristine non-zero PATH counts (m3: 481, m5: 3) are the tools' **own** run-private PATHs
  (the census stub dir; git's own `/usr/lib/git-core:` prefix on its upload-pack children). They
  carry no marker, so the marker column is the clean ambient-copy signal.
* Every mutated file compiles (`py_compile` rc=0).
* Restoration: `git apply -R` rc=0 for all six; after reverse-apply every `tools/*.py` file is
  byte-identical to the changed tree (`restored_exactly_to_changed_tree: true` ×6, in
  `restoration.json`). Each mutant touches exactly one of the five files.

## Findings

* **F-1 — the input diff needs `--unidiff-zero` (L1 apply step).**
  `ExecC1Design/c1-five-tools.diff` was **absent** when this seat started (the directory did not
  exist) and was read in three states while its peer wrote it: md5 `f8992249…` (111 lines,
  `git apply` → `corrupt patch at …:75`), an intermediate 114-line state (`patch -p1` →
  `Hunk #1 FAILED at 437`, `malformed patch at line 64`), and the final md5
  `a2eebc9915e0c5649f893199dd0faadb` (129 lines). The final file is **zero-context**: plain
  `git apply --check` rejects it (`patch failed: tools/check-revision-binding.py:52`,
  `… score-census-handoff-r32.py:440`, `… mutants-btrfs-space-r30.py:8`), while
  `git apply --unidiff-zero` applies it cleanly (rc=0) and `patch -p1` applies it with fuzz 2/1.
  The L1 should apply it with one of those modes — or regenerate it with context — and should
  re-check its md5 at apply time rather than trusting a copy taken earlier in wave 1.
  **The mutant diffs in this seat were regenerated against the tree produced by the final md5
  state**, and all six apply to it with plain `git apply`.
* **F-2 — m6 is a value leak, not a name leak.** If wave 2 reads m6 as surviving, the frozen
  probe's PATH value channel is not firing; that re-opens the round-34 `MutPathCopy` gap and is a
  claim-level finding for C1's kill rule, not a defect in m6.
* **F-3 — the `livefive` run-receipt target's tool child exits 2.** The r36 probe draft's
  `livefive` set runs `tools/run-receipt.py … -- tools/probe-child-env-allowlist-r34.py --version`;
  the r34 probe rejects `--version` (`error: the following arguments are required: --revision`),
  so that child exits 2 in every run. The leak measurement for run-receipt is unaffected — the git
  children it starts beforehand still leak — but the target's exit code is not a clean 0 and the
  argument should be fixed before the after-battery receipt is taken.
* **F-4 — base provenance.** The changed tree was built from lane HEAD
  `189d8a080ba8d508d5faab12cad9e688aee91dab`. The five tool files there are byte-identical to
  the declaration commit `6d76fb20f6ecbc940e5c8fff36c74060c885e161` (`git diff --name-only` over
  those five paths between the two commits → empty output), so the mutants are diffs against the
  declaration's base for the five tools.

## Scope and honesty notes

* This seat designed patches and measured leaks; it did **not** run the frozen r36 probe, which
  does not exist in the lane yet (drafts only: `.ufo/waves/round-36/w1/MutProbeDraft/` and
  `…/ExecProbeR36/`). The expected `leaking_pairs` outcome for each mutant is stated in
  `mutants.md` §4 as an expectation, not as an observation.
* m1's and m5's exit code 2 is unrelated to the leak (m1: the tool's revision gate returns
  `E-REVISION-INVALID`; m5: the receipted r34 probe rejects `--version`). The same exit code
  appears on the pristine tree, so it is not a mutant-induced change.
* No VCS-mutating command was run; no lane file outside this seat's directory was written.

Installs: none.
