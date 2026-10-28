VERDICT: supports

The frozen C2 matcher counter passed with both a space-bearing TMPDIR and a plain TMPDIR on `/fast/scratch`; both runs reported PASS (168 cases, 168 passed, 0 failed, two runs) and removed their per-run work directory. C3 likewise passed in both TMPDIR configurations. Detailed commands, outputs, hashes, and trace audit are in [evidence.md](.ufo/waves/round-50/w1/R50ExecScratchContract/evidence.md).

- **Scratch writes:** C2 creates its own work directory under `--scratch`, supplies its census selftests a TMPDIR/HOME under that work directory, and removes the work directory in `finally`. Traced runs had no absolute writes under `/tmp` or the lane. The `/proc/self/fd/240` paths resolve to the scratch-resident census fixture tree; after each run the supplied scratch directory had zero children. (Evidence receipt, “Commands and observed counter output” and “Write-location audit”.)
- **C3 writes:** C3's two traces had no mutating syscalls or `/tmp` paths; successful write-intent opens were `/dev/null` only. It invokes the adjacency anchor checker in `--revision` mode, not its fixture-writing `--selftest` mode. (Evidence receipt, “Write-location audit”.)
- **`/tmp` default:** The frozen census still spells `base=${TMPDIR:-/tmp}` at source line 2094; its comments state this applies only when TMPDIR is unset/empty. With TMPDIR set, the dirty-space case uses an alias inside that TMPDIR, and an invalid TMPDIR fails without fallback (frozen source lines 2055-2063, 2119-2135; excerpted during inspection). No tested counter invocation wrote to `/tmp`.
- **Global `/tmp` snapshot caveat:** the requested `find /tmp -newer marker` comparison was noisy/inconclusive because concurrent wave files appeared newer and systemd-private directories denied traversal. The process-scoped strace logs showed zero `/tmp` writes for these runs; see the receipt for exact counts.

No blocker found. No source changes made; only the assigned report and its receipt were written.
