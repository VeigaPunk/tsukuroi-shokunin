# FxMutCount — SURVIVES this probe; mutant KILLED

Axes: C1 depth (fixed count semantics), detector specificity, sandbox isolation/restoration.

Sandbox: `FxMutCount.zE4gbjNF/repo`, beneath this report directory; unique mktemp clone `--no-hardlinks`, checked out at `68a8ae035fde33360cbbe21dc92ca0eacf0a5b33`, origin removed. Production content was not edited.

Mutant `73e15dfd1092ec4222972f29169fec49dc5e5035`: changed only `corpus/knowledge/statement-corrections-r18.json:10` and matching `corpus/knowledge/boot-chain-r17.md:198`, `plus 12 named packages (B:59)` → `plus 13 named packages (B:59)`. Other three corrections and expected fixtures remained unchanged. Exact two-line diff: `FxMutCount.zE4gbjNF/mutant.patch`.

Expected detector: unchanged `tools/check-boot-chain.py --statement-corrections`, fixed value at `:79`, comparisons `:714-730`; reject the false count with the named finding while resolving the other three.

Observed, each bounded to 30 seconds:

| Immutable input | Exit | Count | Findings |
|---|---:|---:|---|
| Baseline `842a531`, registry `68a8ae0` | 1 | 0 | Four `CORR-R18-CORR-01/02/03/04-UNRESOLVED`; expected absence control |
| Pristine `68a8ae0` | 0 | 4 | `[]` |
| Mutant `73e15df` | 1 | 3 | Only `CORR-R18-CORR-01-UNRESOLVED` |
| Restored `f856724725605d8b0e186ec457d1bca3b2001af5` | 0 | 4 | `[]` |

Mutant detail: “now does not match the fixed correction; notice Now value is missing or wrong”.

Restoration: registry SHA-256 before=after `008d91d46b6582e02ee4376480b796159d6aa43d8e1615cd1d8d0222d319bc91`; Markdown before=after `4e5018ca90f40b7687c74f6688f371677b0eaef4e0cba02bebefe08081c8c9a0`. Detector hash also unchanged. Full commands, outputs, exits and mutated hashes: `FxMutCount.zE4gbjNF/evidence.json`.

Unknowns: other mutants and overall admission unproven; no final-ledger conclusion. No tools installed; no host probes or package/service/boot actions.

Scope: executed=/usr/bin/mktemp -d; /usr/bin/git clone --no-hardlinks --no-checkout, checkout -b FxMutCount, remote remove origin, diff --no-ext-diff --no-textconv --full-index, commit --only twice, rev-parse HEAD twice; /usr/bin/sha256sum thrice; /usr/bin/python3 check-boot-chain.py --statement-corrections four revision-mode runs. Exact absolute commands/cwds/exits: FxMutCount.zE4gbjNF/evidence.json.
