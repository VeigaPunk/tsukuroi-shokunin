# C1/C2 causal separability — W2CritSeparability

Axes: **calibration, claims**. Review target: `c052bb7d41ced49aa888817069afd804eccfecf1`; counter freeze: `1e926801195e304950e3eb9d2525ef8bbc245089`; declaration/base: `6d76fb20f6ecbc940e5c8fff36c74060c885e161`.

Repository prefix for the source references below: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`.

## Finding summary

**[inf] The declared C1 measurement and C2's journalctl observation are causally separable.** No semantic dependency on the C2 note was found in C1's exercised modes, and C2's recorded matrix invokes journalctl directly rather than the five changed tools. This is a source/evidence review, not a new ablation-battery result or an admission judgment.

Three qualifications prevent stronger wording:

1. “The battery never reads the note” is literally too strong: it archives and copies the entire tree, including the note. No direct reference or evidence-bearing parse was found.
2. “The after receipt does not change” can mean only the **declared measurement projection**, not byte identity of the receipt.
3. The two local C2 matrices are **absent from the target commit**, and their machine records do not identify a measured repository revision. Base execution is asserted by the wave-1 scribe report, not independently revision-bound by those JSON files.

## 1. Probe references and the strongest counterexample

Executed the specialized grep over `tools/probe-child-env-allowlist-r36.py` with:

```text
corpus|knowledge|journalctl-v262|S198|S199|SOURCES|SKILL\.md
```

Result: **No matches found**. A read-only `git diff --exit-code c052bb7d... -- <probe and five tools>` was empty and exited 0, tying the inspected working files to the assigned commit. The freeze-to-change probe diff was also empty and exited 0. Probe SHA-256:

```text
a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a
```

However, `export_tree()` at probe lines 420–424 runs unrestricted `git archive <rev>` and extracts it; `one_run()` at 486–509 clones/checks out or copies that tree. A targeted archive listing at the assigned commit returned:

```text
corpus/
corpus/knowledge/
corpus/knowledge/journalctl-v262-field-filter-r36.md
```

Therefore the expected no-match grep is **not proof of byte-nonaccess**: the note's bytes travel through the harness. This is a concrete counterexample to the literal no-read wording, not a demonstrated causal coupling of the claims.

The evidence-bearing source channel is narrower: `source_findings()` at 1053–1083 starts at the selected target and follows existing `tools/<module>.py` imports. It does not scan knowledge notes. The livefive target list is fixed at 226–252, not derived from corpus rows.

**Smallest safe correction:** describe the boundary as “C1 does not parse or use C2's note as measurement evidence; whole-tree transport includes it.” Do not change the frozen probe merely to make the literal wording true.

## 2. C1's actual target-input boundaries

| Livefive target/mode | Relevant inputs observed in source | Consequence for a C2-only removal |
|---|---|---|
| `check-revision-binding.py --object-target-types` | `tools/` sources at the selected revision; Git object/ref fixtures; original-nine consumer tests. `target_type_measure()` 805–853 and `target_type_probes()` 692–759. Accepted commit-tag fixtures point at the selected revision's first parent. | At c052bb7d that parent is freeze `1e926801...`, before the C2 note. The selected tip's tree identity can change, but the predicate is object type/binding, not C2 content. A newly committed revert also changes the first parent; that is an additional intervention, not a controlled byte-identical replay. |
| `check-report-receipts.py --report ...` | The probe writes its own fixed report (`write_livefive_report()`, 468–474). `find_receipts()` reads only `.ufo/waves/` candidates (309–365). | C2's knowledge note, registry and README rows are outside the receipt-candidate tree. |
| `score-census-handoff-r32.py --scenarios 1 --seed 36` | `export_census()` 433–450 archives only `tools/tsukuroi-census.sh`; fixture files and live host journal views are created/read by the scorer. | No C2 document parse. The census blob is identical at declaration/base and change: `10b6d47046c9523bfeefd56c76a06ecc59ea5e01`. Live-host drift remains the already declared limit. |
| `mutants-btrfs-space-r30.py` default battery | `run_case()` 319–374 builds its own fixture corpus, SKILL and SOURCES; the child counter receives `--tree <synthetic case>` and `--base-sources <synthetic file>`. | Its `corpus/SOURCES.md` and `SKILL.md` strings are **synthetic fixtures**, not reads of the real C2 rows. |
| `run-receipt.py ... check-report-receipts.py --selftest` | Clones/checks out the tool revision (85–99); runs the child with a fixed environment (104–107). The selected child selftest is in-memory report/receipt fixtures (`check-report-receipts.py` 379–425). | Checkout transports C2 bytes, but the exercised selftest does not consume them. |

## 3. C2's independence from the five-tool change

Inspected:

- `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json`: 54 recorded cells, `journalctl_binary` `/usr/bin/journalctl`, systemd 262 version, argv/exit/stderr/stdout records.
- `.ufo/waves/round-36/w1/ExecC2Live/matrix.json`: requested matrix plus controls, each invoking `journalctl` directly.
- `.ufo/waves/round-36/w1/ReviewC2Draft/matrix.sh`: direct journalctl probes, no call to a C1 tool.
- `ScribeC2Draft/ScribeC2Draft.md:3–4,18–24,114–125`: names declaration/base `6d76fb20...`, records the executed matrix and the base prior-state search.

A specialized grep of both matrix JSON files for `tools/|check-revision-binding|check-report-receipts|score-census|mutants-btrfs|run-receipt|revision|base` returned **No matches found**. The journalctl observations are host-binary behavior, not output of the five changed Python tools. The C1 change alters neither `/usr/bin/journalctl` nor the census blob. **[inf] Reinstating the five tools' base bytes would not invalidate those matrix observations.** The note's consumer sweep concerns journalctl argv; C1 changes child-environment construction, not those journalctl selectors.

### Provenance limitation at the assigned commit

`git ls-tree -r --name-only c052bb7d... -- <absolute ScribeC2Draft directory> <absolute ExecC2Live directory>` returned no paths. The committed note cites `ScribeC2Draft/matrix-mini.json` at its line 127, but neither cited matrix is in that commit. They are locally available and were inspected; this is **not** a missing-local-artifact claim.

The matrix JSON files do not carry a measured Git revision. Thus “the matrix ran at base” is supported by the scribe's explicit report plus the wave-1 context, but is not independently authenticated by a revision-bound machine receipt. Do not promote that assertion to stronger provenance than the artifacts provide.

**Smallest safe correction:** include the cited matrix bytes and their report in the evidence closure, pin their hashes, and distinguish the report-asserted base from a machine-recorded execution revision. If an independently revision-bound receipt is required, capture one separately; do not rewrite the original capture as though it had that metadata.

## 4. C2 revert: what can and cannot remain invariant

C2's claim-bearing changes are the new note and its additions to `SKILL.md`, `corpus/README.md` and `corpus/SOURCES.md`. The NoUpgrade supersession appends and shared round accounting are not themselves C2's field/filter measurement. Removing the C2 additions while retaining C1's tools, frozen probe, existing receipt fixtures and reference bindings removes no input used to construct the five child environments or compute source findings.

**[inf] Under that controlled intervention, C1's declared outcome should remain:**

```json
{"leaking":0,"leaking_pairs":[],"harness_errors":[],"predicate_label":"leaking"}
```

with exit 0 and the same five-target/four-channel coverage, **if those conditions hold for the original after run**. This review does not assert that an unrun after or C2-revert battery passed. It identifies why the C2 documents are not a cause of that outcome.

The **whole receipt cannot be invariant**. The probe summary includes `revision` and a random `scratch` path (1268–1271); individual rows carry random injections and execution observations. A committed revert changes revision/tree object identities, and `check-revision-binding` additionally uses the selected commit's first parent. The census target reads a changing live journal. These are reasons not to demand byte identity, not evidence that C1 uses C2's knowledge content. Within-run parity differences are already recorded-not-evidence for livefive.

**Smallest safe correction:** compare the frozen declared projection and required coverage/exit, preserving the probe hash, rather than claiming unchanged receipt bytes. Any stronger empirical revert assertion requires an actual sandbox capture; none was run by this seat.

## Scope and disposition

- Strongest local counterexample: whole-tree archive transport reads the note's bytes despite a clean direct-reference grep.
- Concrete fixable defect: the note's local matrix evidence is not carried by c052bb7d's Git tree; base provenance is report-level rather than machine-bound.
- No observed counterexample establishes a causal dependency between C1's leak measure and C2's matrix. The narrower separability conclusion is source-reasoned **[inf]**, not a canonical judgment.
- Exercised checks: read-only Git identity/diff/tree/archive queries, specialized greps, source/receipt reads, SHA-256 hashing. No full battery, ablation sandbox, build, test, judge or other model/runtime invocation was performed.
- No production/index/ref mutation; no delegation; no tool installation or update.

Report: `.ufo/waves/round-36/w2/W2CritSeparability`
