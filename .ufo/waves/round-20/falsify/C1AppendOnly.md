# C1 append-only preservation review

## Scope and axes

Round 20 attempt 1 only. Axis: C1 adjacency, specifically preservation of the inherited PROVINCE prefix and admission of the exact OUT-009 suffix. C2/C3, host state and boot readiness are not assessed. Baseline is `0cbc34dd6b20896085a8fb07943e3ea4027d8472` (`.ufo/waves/round-20/preregister.json:3`); the adjacency candidate is the worktree named at `.ufo/waves/round-20/worktree-bindings.json:6`.

In the citations below, `lane/` means `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`, `adjacency/` means `/tmp/tsukuroi-r20-adjacency-20261021/`, and `binder/` means `/tmp/tsukuroi-r20-binder-20261021/`. The candidate checker was read at tool snapshot `A2D9`.

## Findings by severity

**No actionable append-only preservation defect found in the reviewed source and displayed file contents.** The current candidate contains a full-byte prefix check, not merely presence checks for legacy rows or arbitration wording. This is a source-review recommendation, not an admission or an observed successful evaluation.

### Inherited prefix and appended suffix

- Compared the complete inherited reference `adjacency/PROVINCE.md:1-146` with `lane/PROVINCE.md:1-146`; the displayed text and ordering match throughout. A second inherited reference, `binder/PROVINCE.md:1-146`, matches the adjacency reference. No removed, rewritten or reordered legacy line was found in those comparisons.
- In particular, the Core/refusal text remains at `lane/PROVINCE.md:3-33`; all seven ADJ rows and the handoff checklist remain at `:35-73`; unresolved Kaidoku/Revenger arbitration remains at `:79-80`; the older refinements remain at `:85-106`; and the portable-anchor section, original OUT-009 proposition and ten digest records remain at `:108-146`. The legacy OUT-009 row at `:129` still says “Revenger owns” and “packages”: it has not been repaired by silently rewriting historical evidence.
- The inherited reference ends with the OUT-010 digest at `adjacency/PROVINCE.md:146`. The lane adds only the blank separator at `lane/PROVINCE.md:147`, the named heading at `:148`, the correction at `:150`, and its explanation at `:152`, with intervening blank lines. The appended text explicitly supersedes only the unqualified OUT-009 proposition/package paraphrase, preserves the quoted declaration and pinned evidence, and leaves ADJ-06/Frontier arbitration controlling (`lane/PROVINCE.md:150-152`). It denies ownership-grant and write authority locally rather than deleting the old row.

### Candidate acceptance cannot discard the legacy prefix

- The C1-specific baseline constant is the exact assigned R20 base (`adjacency/tools/check-adjacency-anchors.py:65`). It is separate from the older round-19 registry baseline at `:21`; the prefix comparison uses the former, at `:156`.
- `_ownership_correction` reads that baseline's `PROVINCE.md`, refuses an absent/unsafe baseline, re-encodes the current text as UTF-8, and compares against the baseline's raw bytes (`adjacency/tools/check-adjacency-anchors.py:156-161`). Current text originates from the selected revision, not from `--registry-from` (`:481`); `_text` strictly decodes committed bytes without stripping or newline normalization (`:300-310`). `GitReader` returns the committed blob's byte stdout and rejects nonregular entries (`:264-295`).
- The function requires exactly one clarification heading, then requires `current_data.startswith(baseline_data)` and exact equality of **all remaining bytes** to a single newline plus `OWNERSHIP_SECTION_LINES` plus a terminal newline (`adjacency/tools/check-adjacency-anchors.py:162-175`). The section constants include both the correction and explanatory paragraph (`:43-61`) and match the displayed lane suffix (`lane/PROVINCE.md:148-152`).
- [INFERENCE] Consequently, deleting/reordering any legacy content, editing the historical OUT-009 proposition, moving the clarification into the old prefix, changing legacy whitespace/newlines, or inserting any extra preface/tail cannot produce a C1 acceptance through this path. Prefix changes fail at `:171-172`; an altered or additional suffix fails at `:173-175`. Missing exact heading with an unchanged baseline is the named missing-correction result; missing heading with a modified document is invalid (`:164-168`). Duplicate exact headings are invalid (`:169-170`).
- The successful return of count 1 is after these checks and the pinned snapshot/arbitration checks (`adjacency/tools/check-adjacency-anchors.py:178-196`). The actual evaluation caller invokes this function under `ownership_corrections`, records its count/findings, and returns failure if any findings remain (`:761-766`). CLI wiring passes the requested flag through to that caller (`:787-788,838-839`); raised revision errors become CANNOT_EVALUATE, not success (`:841-848`). No alternate C1 count-1 path was found.

## Residual risk and verification gaps

- The complete available inherited-file prefix and new lane suffix were compared as read-only file text. The two inherited references agree, but their identity with the immutable baseline Git blob and the lane's raw-byte equality to that blob were **not independently measured**. No Git command, hash computation, checker, fixture, test, build, lint, formatter, smoke run, import or subprocess was executed. The byte-level rejection conclusion above is static reasoning from the candidate's code, not captured runtime output.
- This guarantee applies to the preregistered command with `--ownership-corrections` (`lane/.ufo/waves/round-20/preregister.json:10`). Ordinary mode does not execute the prefix check and leaves `ownership_corrections` at 0 (`adjacency/tools/check-adjacency-anchors.py:363-374,761-765`); an ordinary PASS must not be represented as C1 append-only evidence.
- The reviewed enforcement is in the external adjacency candidate. This report does not certify its integration, a committed candidate revision, or the claimed measured 0→1 result.
- LSP availability discovery returned `No such tool: xd://lsp` (mounted devices: `ast_edit`, `debug`). LSP status/references/definition/diagnostics were therefore unavailable; grep was only a locator, and the conclusions rely on the directly read source cited above, not semantic LSP proof.
- No runtime/rerouting/saturation or resume-continuity claim is made. No tool was installed or updated. No host or boot-safety claim is made; boot images remain UNKNOWN, with no clearance.

Scope: executed=none
