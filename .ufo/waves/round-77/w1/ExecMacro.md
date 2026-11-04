# ExecMacro — round 77 / w1

## Verdict

**PASS, bounded arithmetic probe: six pinned arithmetic vectors match (6/6).** Axes: depth (8, lowest tied) and freshness (9); no ordinal uplift or production-integration verdict is claimed. C2 remains exactly “three exact corrective blocks exist” and was not evaluated by this seat.

Read the round-77 declaration at frozen revision `eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5` using read-only `git show` (exit 0), and the frozen expected.json and source ranges. Base: `06f1bbbb803790b35358d277bb7807b82a9fab99`.

## Method and retained evidence

All paths below are absolute. Durable directory:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/w1/ExecMacro/`.

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/w1/ExecMacro/probe.c`: generated GNU C program, includes the **full** pinned header directly by absolute path. All five numeric inputs per vector are uint64_t, initialized with UINT64_C. Actual LESS_BY and CLAMP macros are invoked; neither is reimplemented.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/w1/ExecMacro/receipts.json`: exact argv, shell-quoted commands, cwd, TMPDIR, exit, stdout/stderr for compiler version, hashes, both compile attempts, execution and cleanup; per-vector expected/actual comparisons. Probe SHA256: `e828a8e9c00a00f90ebe1c35b27b7b24ff7b800d8861cbb7d630706854ce4a80`.
- Expected.json SHA256: `1469154cf9ce2b3c8bcaf6d8ee6698cca912c8ba8ea7e21452b47a5d31fa8694`.
- macro.h SHA256: `1bd38a180b2cccacf0732e3e5b6388ac3d71e453839236c388501080a11a75b8`.
- journald-manager.c SHA256: `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`.

Both observed source hashes match SHA256SUMS and expected.json pins. The expressions follow journald-manager.c:168,170–171. Source :176–185 separately shows startup min_use patching; this probe does not execute it.

## Commands and exits

Every compiler/probe command used cwd and explicit TMPDIR `/fast/scratch/hyaku/tsukuroi-r77/ExecMacro`. Compiler: `/usr/bin/gcc --version` → **GCC 16.2.1 20260810**, exit 0. `/usr/bin/sha256sum` over the three absolute source/expectation paths → exit 0 (complete command and output in receipts).

Initial compile (exit **1**, no output program run):
```
/usr/bin/gcc -std=gnu11 -Wall -Wextra -Werror /fast/scratch/hyaku/tsukuroi-r77/ExecMacro/probe.c -o /fast/scratch/hyaku/tsukuroi-r77/ExecMacro/probe
```
The complete header requires its build metadata macro RELATIVE_SOURCE_PATH at :518; the failure was an undefined build prerequisite, not an arithmetic mismatch. After inspecting :480–535, supplied that string through the compiler command without altering any source, vector, predicate or arithmetic expression:
```
/usr/bin/gcc -std=gnu11 -Wall -Wextra -Werror '-DRELATIVE_SOURCE_PATH=""' /fast/scratch/hyaku/tsukuroi-r77/ExecMacro/probe.c -o /fast/scratch/hyaku/tsukuroi-r77/ExecMacro/probe
/fast/scratch/hyaku/tsukuroi-r77/ExecMacro/probe
```
Configured compile **exit 0**, stderr empty; program **exit 0**, stderr empty. Comparison checked exactly six lines in A1–A6 order, each with its exact id and all three decimal outputs equal to frozen expectations:

| Vector | avail | limit | available | Match |
|---|---:|---:|---:|---|
| A1 | 900 | 1000 | 900 | yes |
| A2 | 0 | 100 | 0 | yes |
| A3 | 0 | 100 | 0 | yes |
| A4 | 900 | 500 | 400 | yes |
| A5 | 0 | 300 | 200 | yes |
| A6 | 0 | 500 | 0 | yes |

A1 is unconstrained growth; A2/A3 distinguish below/equal keep_free and saturate avail to zero; A4 hits the upper clamp; A5 hits the lower clamp even with zero avail; A6 saturates remaining allowance when used exceeds the clamped limit. This is subtraction, not min(free, keep_free).

## Cleanup, boundaries and risks

After durable C and receipts were saved, `/usr/bin/rm -r -- /fast/scratch/hyaku/tsukuroi-r77/ExecMacro` ran from the durable seat directory, **exit 0**. Scratch and its executable were removed. No other scratch or service was touched. No tools installed/upgraded; no privileged commands, package transactions, production edits, commits, pushes, delegation, credential reads or raw journal-message reads. No whole-repo checks were run.

Only these six small non-overflowing uint64_t vectors, with min_use <= max_use, were exercised. No universal arithmetic proof, live manager state, startup-normalized metric reachability, C2 correctness, production counter success or admission is implied. Parent retains production integration and the frozen revision-based C1/C2 gates. No blocking prerequisite remains for this bounded item. LSP was not exposed among available tools; no symbol refactor was performed.

Self-evaluation: accuracy 4/5 (finite inputs only); completeness 5/5 (C source, compiler, commands/exits, exact comparison and cleanup retained); clarity 4/5 (full diagnostic lives in JSON rather than prose); actionability 4/5 (reproduction requires recreating the removed private scratch); conciseness 4/5 (absolute paths are necessarily repeated). Overall 4.2/5. Prioritized improvements: retain machine-readable commands (done), distinguish compile prerequisite failure from numeric mismatch (done). Would the user agree: expected, given the explicitly bounded acceptance and retained failure.
