VERDICT: defect-found

## Scope and method

Attacked the frozen C2 verdict-binding detector with forged a2w1 records in scratch clones of the lane; no counter code was changed. Used the `controls-a2` candidate surface and mirrored its a2w1 `records()` construction (`controls-a2/run_controls_c2.py:76-110`; candidate source path is set at line 61). The counter's binding path requires the exact task/result `(name, agent)` pair, extracts only JSON object's `verdict_line`, checks the first line, checks same-row machine-shaped contradictions, then compares the report's first line (`tools/check-scrub-grounding-r45.py:220-271`). The explicit contract is documented at `tools/check-scrub-grounding-r45.py:28-44`.

Counter SHA-256 observed before probing: `a1eb402dffae97fcefd9bd539529f1cacc5034419b6de06e1f8ac1c08d011331` (matches the frozen hash in the assignment). The attempt-2 battery's summary reported `{"should_fail_accepted": 0, "control_accepted": 1}`. My pristine all-holds forged control `P0-all-holds` returned PASS / exit 0 with holds bound for all six seats. I ran 35 probe variants in isolated cloned fixtures; each result's full counter JSON, output status, commit id, and forged-record SHA-256 values are in `C2MutBinding/probes.jsonl`. The restored rerun is in `C2MutBinding/probes-restored.jsonl`.

## Findings

**Three clear binding gaps (survived; counter accepted the forged records as PASS):**

- `P3c-cyrillic-O-contradiction`: first line says `ROW GR1 VERDICT: holds`; the next line says `RОW GR1 VERDICT: fails` with Cyrillic U+041E in `ROW`. `ANY_VERDICT_RE` does not see the look-alike contradiction, so `C2RevGR1` binds `holds`; counter output PASS / exit 0. This evades a human-visible opposite verdict using the requested Unicode-lookalike class.
- `P7a-dup-under-other-role`: an extra `C2RevGR1` result under `agent: critic` asserts GR1 fails. It is ignored while the intended `(C2RevGR1, reviewer)` entry binds holds; counter PASS / exit 0. The result list is only required to have exactly one match for each expected pair; it does not reject a second same-name entry under another role (`bound`, lines 250-263).
- `P11-json-sibling-key-contradiction`: output object has `verdict_line: ROW GR1 VERDICT: holds` and a sibling `note` saying `ROW GR1 VERDICT: fails`. `declared_text()` returns only `verdict_line` for object outputs (lines 227-234), so the contradiction scan never sees `note`; counter PASS / exit 0.

**Additional accepted opposing evidence / interpretation-sensitive cases:**

- `P8-prose-contradiction`: report starts `ROW GR1 VERDICT: holds` but its body explicitly says the row does not hold and recommends fails. Counter PASS / exit 0: the implementation only detects another machine-shaped `ROW ... VERDICT:` line, not natural-language contradiction (`contradicts`, lines 240-242; report check, lines 265-270). This meets the assignment's body-prose attack, but whether prose must be machine-checked is a contract interpretation; the counter's documented contract specifically names a contradicting `ROW ... VERDICT:` line.
- `P12-cross-row-contradiction`: GR1 holds record contains a machine-shaped GR2 fails line; counter PASS / exit 0 because `contradicts()` only rejects contradictions for the currently-bound row (lines 240-263). This is a cross-row coverage gap if records must not carry contradictory claims about other rows.
- `P5a-newline-vl-no-verdict-key`: a JSON `verdict_line` containing `ROW GR2 VERDICT: holds\nextra detail` binds holds and passes when its report has the same first line. The first-line rule permits this; with a `verdict` key, the analogous newline is rejected by `declared_text()`'s fullmatch check (P5b FAIL). This is an asymmetry, not an accepted opposite verdict by itself.

**Attacks that were rejected (counter FAIL / exit 1):**

CRLF in output/report first lines (`P1a-c`), BOM in report/verdict line (`P2a-b`), full-width digit, Cyrillic letters and full-width colon in the actual verdict (`P3a-b,d-e`), zero-width space or NUL in verdict (`P4a-d`), newline-bearing contradictory verdict line (`P5c`), JSON string containing JSON (`P6`), duplicate same-role result (`P7b`), trailing period (`P9`), lowercase `row` (`P10`), verdict-key case mismatch, non-string verdict_line/output, double-space/tab, duplicate dispatch task and duplicate JSON key (`P13-19`) all failed to bind the targeted seat. The plain JSON-string verdict sanity case `P6b` and unrelated foreign-name result `P7c` passed as expected.

## Pristine/restored evidence

The second full run rebuilt the fixtures from the frozen candidate and repeated the control. `P0-all-holds` returned PASS / exit 0 again. Its dispatch, results, and six report SHA-256 values are byte-for-byte identical across the initial and restored run (`P0` entries in both receipt JSONL files; the script printed `P0 record hashes identical: True`). The P0 record hashes include dispatch `0fc6e6079972a37235814f568b14d46a07218d9c07481534e77fec626073b389` and results `b72963b2cb0fb684630785f6d97a5dae15bb1634ddfb33305c1d64fddaceaf7b`; report hashes are recorded per path in the receipts. Scratch directory `/fast/scratch/hyaku/tsukuroi-r45/C2MutBinding` was removed after copying receipts.

No source-code mutant was applied: this was a record-binding attack battery as assigned. No tools were installed; no host or lane tracked files were changed.

Receipts: `.ufo/waves/round-45/a2w1/C2MutBinding/probes.jsonl` and `.ufo/waves/round-45/a2w1/C2MutBinding/probes-restored.jsonl`.