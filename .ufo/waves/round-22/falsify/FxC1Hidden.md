# FxC1Hidden: source-only falsification of check-boundary-contract.py (round 22)

Verdict: FALSIFIED. The property "rows hidden in comments or code fences earn no visible decision credit" does not hold. Five source-level counterexamples follow. F-A and F-B sit inside the named comment and fence mechanisms. F-C, F-D and F-E are the same class through a raw-text check or through constructs the visibility model does not cover.

Axes: fence and comment state fidelity; coverage of non-rendered constructs; visibility of the limit disclosure; selftest coverage.

## Evidence limits

- Target SHA-256 was NOT recomputed. Hashing counts as execution under NO-EXEC. The receipt digest echoes the assignment-declared value. The `#6D78` tag in read output is a snapshot tag, not a digest.
- Target read in full, lines 1-175. Byte scan of declared files (grep): no CR or control bytes. The only non-ASCII bytes in the target are em dashes in selftest strings at lines 106-107. JSON, host file and preregister have no control or non-ASCII bytes.
- Prose `seat-boundary-r22.md` has no comment, fence, raw-HTML or link-definition markers today (grep-verified). Its decision table is at lines 11-18; the limit sentence is at line 22.
- Nothing executed. Fixture verdicts below are expected (intent) or predicted (static trace), not observed.
- `corpus/SOURCES.md` is not a declared read. The source check (lines 77-81, fed by line 164) is not evaluated.
- CommonMark and GFM rules are cited from recall. No spec was fetched (NO-FETCH). The project renderer is not declared; CommonMark/GFM conformance is assumed.
- No installs or updates.

## Mechanism

`visible()` (lines 38-55) is the only visibility model. Per line it handles comment state first (lines 42-47; `continue` on line 47 skips every line in comment mode, fence lines included). It then handles fence state (lines 48-52). Fence close is "any run of three or more of the same character at line start" (lines 48-51): there is no closer-length check, no bare-line check, and any indentation is accepted (`lstrip`, line 41).

Decision credit: `cells` (line 82) feeds `matches == [expected]` (lines 88-89), and `count += 1` (line 92) grants the credit. The limit check (line 93) reads raw `text`, not `visible(text)`.

## Counterexamples

ROWS below means the six decision rows, copied byte-identical from prose lines 13-18. Fixtures are indented four spaces so they cannot be parsed as declarations. Each fixture replaces only the decision table region.

### F-A: fence closed by a shorter run (primary, in scope)

Source: lines 48-51, which keep no fence length.

    ````
    ```
    ROWS
    ````

CommonMark: the opener is four backticks. A closer must be at least four, so line 2 is content and ROWS render as code text. Checker: line 2 matches the same-character rule and closes the fence, so ROWS are visible, six credits.

Other closers the checker accepts and CommonMark does not: a closer with trailing text (for example "```text"), a closer indented four or more spaces, and a shorter tilde run under a longer tilde opener.

### F-B: comment state masks a real fence opener (primary, in scope)

Source: comment logic (lines 42-47) runs before fence logic, and fence lines are skipped in comment mode.

    Note: x <!--
    ```
    -->
    ROWS
    ```

CommonMark: `<!--` with no `-->` in its paragraph is literal text. A fenced block can interrupt a paragraph, so line 2 opens a fence, and `-->` and ROWS are code. Checker: line 1 enters comment mode; line 2 is skipped without touching fence state; line 3 exits comment mode; ROWS are visible, six credits. This variant does not need the F-A closer defect.

### F-C: limit disclosure credited from hidden text (secondary, same root)

Source: line 93 tests `'post-hoc detection, not preventive runtime enforcement' not in text` against raw text.

Fixture: delete the visible sentence at prose line 22 and place only `<!-- post-hoc detection, not preventive runtime enforcement -->` in the file. The selftest `limit` case (line 128) only deletes the phrase, so the hidden form is untested.

### F-D: rows inside raw-text HTML (secondary, unmodeled)

    <style>
    ROWS
    </style>

CommonMark HTML block type 1 (`<style` through `</style>`) emits ROWS raw. Browsers do not display `<style>` text. The checker has no HTML case, so ROWS are visible to it. Display behaviour and sanitizer behaviour are [INFERENCE]. `<script>` has the same form.

### F-E: rows inside a link-definition comment (secondary, unmodeled)

Preceded by a blank line:

    [//]: # (
    ROWS
    )

CommonMark: a link reference definition with a multi-line parenthesised title. Definitions are never rendered, and ROWS are title text. Checker: no line starts with `<!--` or a fence, so ROWS are visible, six credits. This is the common Markdown comment idiom.

## Expected, observed and predicted verdicts

| Fixture | Expected verdict | Observed | Static-trace prediction |
|---|---|---|---|
| F-A | FAIL, exit 1, six BOUNDARY-DECISION-MISMATCH, validated 0 | not observed (NO-EXEC) | PASS, exit 0, validated 6; conditional on SOURCES.md source check |
| F-B | FAIL, exit 1, six BOUNDARY-DECISION-MISMATCH, validated 0 | not observed (NO-EXEC) | PASS, exit 0, validated 6; conditional as above |
| F-C | FAIL, exit 1, BOUNDARY-LIMIT-MISSING | not observed (NO-EXEC) | PASS, exit 0, no LIMIT finding; conditional as above |
| F-D | FAIL under rendered visibility; PASS under the literal comment/fence model | not observed (NO-EXEC) | PASS, exit 0, validated 6; conditional as above |
| F-E | FAIL under rendered visibility; PASS under the literal comment/fence model | not observed (NO-EXEC) | PASS, exit 0, validated 6; conditional as above |

Impact: C1 (`validated_boundary_decisions`, preregister line 5) reaches its target of 6 with rows that are code text (F-A, F-B) or not displayed (F-D, F-E). C1 overstates depth under these forms.

## Selftest gap

Selftest is at lines 103-137; cases at lines 109-129. Covered: whole-prose comment wrap (123), whole-prose fence wrap (124), wrong table (125), source missing (126), host overclaim (127), limit phrase deletion (128). Not covered: any of F-A to F-E, interleaved comment and fence state, a shorter closer, or a hidden limit sentence. Coverage is read from source; selftest was not run.

## Bounded holds (not falsified)

- A row whose `<!--` and `-->` lie on its own line, or inside a block comment spanning lines, is never credited (lines 42-47, 54).
- A row inside a well-formed fence (same-character closer, length at least the opener, bare line, at most three spaces of indentation) with no earlier unterminated `<!--` is never credited.
- Duplicate or hidden copies cannot inflate the count: exactly one visible match per ID is required (line 89).
- JSON alone earns no visible credit: `count` requires the prose match (lines 88-92).
- Rows must start at column 0 with `|` (line 82). Indented rows are never credited.

## Conservative deviations (false FAIL direction, not credit)

- N1: any line containing `<!--` is hidden whole (lines 42-43, 54), including visible text before the marker.
- N2: an unterminated `<!--` in visible prose hides every line until one contains `-->`. This can hide all six rows.
- N3: fence openers at any indentation count (lines 40-41). CommonMark treats four-plus-space-indented fence lines as indented code.
- N4: a `<!--` inside a fence leaves checker fence state open after the `-->`, hiding later visible rows.
- N5: a backtick info string containing backticks is treated as a fence. CommonMark does not.
- N6 (precision, visible text): no GFM header or delimiter check (line 82), so six pipe lines outside a table are credited. The text is visible, so this is not hidden credit.

## Other observations

- The source check (line 77) has no leading-pipe filter. The `visible()` defects F-A, F-B, F-D and F-E apply equally to S083/S084 presence credit [INFERENCE; SOURCES.md not read].
- `--branch` (line 155) is caller-selected, so "landed" is only as strong as the branch chosen. Out of this attack's scope.

## Recommended direction (no edit made)

Replace the line-state `visible()` with a CommonMark/GFM parse at the pinned revision. Failing that, fail closed on: any `<!--` outside block start; any fence whose closer does not match CommonMark; any raw-HTML block or link definition in the decision file. Check the limit sentence against visible text. Add F-A to F-E as negative fixtures before C1 is trusted.

Reviewed-SHA256: 1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485
Predicate: r22-fxc1hidden
Scope: executed=none

Lane bounds: leaf member — no subagent dispatch.
