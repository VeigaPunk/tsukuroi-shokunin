VERDICT: supports

## Scope and axes
Axes: depth, C1, bindcheck. Item W-B1 only; revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0. No actionable finding in the three assigned comparisons. This recommendation is not a counted verdict or admission.

## Evidence
All receipt paths below are relative to this report's sibling directory `R52RevHashBind/`.

1. Independently extracted frozen entry bytes with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:corpus/knowledge/btrfs-scrub-grounding-r45.md`. Split at LF, take each exact `## GR<n>` header through the line before the next `## ` heading, preserve every line including blank lines, join with LF without appending LF, then SHA256. Results:

| Row | Entry lines (inclusive) | Independent SHA256 |
|---|---|---|
| GR1 | 14-102 | 98fa4e07768d240eaf5ea2cce13ce0623fdb756054e5df9f7b9fe68ab2e63987 |
| GR2 | 103-238 | 9fd581a0c9d02b02100b6a15648b7c6e4be896ac746ed09303a88dc8a24f0ec5 |
| GR3 | 239-324 | 0405f38a5783c49b6c078b118c9868543eb494b43f8b1c5e6c14284a123b9eac |

Command `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r52.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0 --section-hash --no-base-check` returned 0, `structural_ok: 1`, `problems: []`, and exactly those three hashes. Raw command/output: `R52RevHashBind/section-counter.json`. Independent comparison: `R52RevHashBind/binding-comparison.json` (`counter_equal: true`).

2. Command `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/lint-grounding-r51.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0 --emit-gaps` returned 0. Its six list lines are byte-equal, in order, to the frozen entry's `### Range gaps (R51)` list at corpus/knowledge/btrfs-scrub-grounding-r45.md:369-374:

```text
- S237 scrub.c: 421, 439, 442, 1247, 1292-1293, 1546, 1710
- S240 ioctl.c: 3076-3078, 3080-3082, 3084-3085, 3087-3090, 3093-3095, 3109-3110, 3115, 3190
- S242 scrub.c: 1400-1401, 3081, 3094-3139, 3250-3253
- S243 sysfs.c: 78, 1288, 1302, 2015, 2019
- S246 kstrtox.c: 70, 75, 77
- S247 dev-replace.c: 309, 970, 1197, 1236-1242
```

Raw command/output: `R52RevHashBind/emit-gaps.json`. Both literal lists and `gap_lists_equal: true`: `R52RevHashBind/binding-comparison.json`.

3. All 18 counted task prompts in the observed `.ufo/waves/round-52/w1-dispatch.json` contain the matching independently derived row hash: six prompts per row. Receipt `R52RevHashBind/binding-comparison.json` records each seat, role, expected hash and match; `all_18_prompt_hashes_match: true`. The same hashes match the frozen record at `.ufo/waves/round-52/frozen/FROZEN.md:47-50` read with `git show` at the named freeze. This checks the section hash communicated to the cohort, not a separate whole-prompt digest. The dispatch is a post-freeze observational artifact, not claimed present in the freeze commit; its observed file digest is retained in the receipt.

Executed tool files were compared byte-for-byte against their frozen blobs: both equal. SHA256s: check-scrub-admission-r52.py `bd5563af9b4a978552130e15d583614000e225fb7fb3f7c2e1c193dba7c08a80`; lint-grounding-r51.py `9a9a1a9d305da97ab862f441ec94c6cca04bd27cea7dbc3e21832fb51c9e14bb`. See receipt `tool_provenance`.

## Residual risk and verification gaps
- `--emit-gaps` emits the computed list; its zero exit is not asserted to prove a full lint PASS. No unrequested full admission, selftest, C2/C3, runtime/rerouting, saturation, or resume-continuity check was run.
- LSP device unavailable: `read xd://lsp` returned `No such tool`. No semantic caller/definition/diagnostic claim is made; this assignment compares frozen data and prescribed command outputs only.
- No tools installed; no tracked files modified. Scratch `/fast/scratch/hyaku/tsukuroi-r52/R52RevHashBind/` was removed after receipts were saved (observed `scratch_removed True`).

## Self-evaluation
Accuracy 4/5: exact byte comparisons and recorded command outputs; live dispatch cannot establish future immutability. Completeness 5/5: all three W-B1 checks have receipts. Clarity 4/5: detailed provenance makes the report longer than the core finding. Actionability 5/5: no proposed amendment needed for these bindings. Conciseness 4/5: literal list retained for auditability. Overall 4.4/5. Highest-value improvement: L1 should bind the observed dispatch in its named integration revision; do not interpret this snapshot as future binding. Would the user agree? Expected yes, for the explicitly scoped comparisons.
