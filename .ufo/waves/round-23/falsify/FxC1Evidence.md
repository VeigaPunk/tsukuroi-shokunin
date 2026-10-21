# FxC1Evidence — falsify `evidence_ok()` (round23 attempt1)

Attacked claim: **C1** (`validated_edit_decisions` = 8), specifically the S086 evidence leg of `tools/check-edit-contract.py` (`evidence_ok`, lines 96–112), its docstring "S086 proves only observed metadata shapes and adapter steps", and the prose claim in `corpus/knowledge/structured-edit-r23.md` line 7: "Recorded native steps include report reads/writes under the same parent call ID."

Verdict: **falsified as an overclaim, but the defect is fixable.** This is not a tradeoff the canonical judge has to reject. The eight decision rows are separately bound to the preregister policy, so they are not invalidated. The gate does validate the argument-key *shapes*. It validates nothing about the *adapter steps*, and the real S086 data does not support the "same parent call ID" expansion sentence. Every mutation listed below leaves `EDIT-EVIDENCE` unraised, so `validated_edit_decisions` stays at 8.

Method: a static read of the bound files only (NO-EXEC). Every acceptance listed below is derived by tracing the predicate in lines 96–112 by hand. None of it was run. [INFERENCE] marks anything that depends on transcripts I cannot open.

## Evidence from the landed S086 data

- **CritRuntime** (`structured-edit-observations.json` lines 9 and 18–29): `request_line` is 15, but its `recorded_starts` are at line 12 (`read …/CritRuntime.md:raw`) and line 13 (`write …/CritRuntime.md`). Both starts come **before** the request they are supposed to belong to. The start objects carry no `call_id`. Nothing in the file ties them to `toolu_014nToY7USd3cckcqeieNJ4o`. [INFERENCE] They may be the seat's own earlier read and write calls rather than an expansion of this edit, or the recorder's line numbering may not follow request order. The file cannot tell these apart.
- **OraclePathArtifact** (lines 31–99): three edits of the `old_string`/`new_string` shape. Each records exactly one start, `edit` at `request_line`+1. **None records a read start.**
- Net result: a read accompanies an edit in only 1 of 4 rows, and that row is temporally inverted. No row links a start to its parent call ID. So the "reads/writes under the same parent call ID" sentence is not established by S086. The `WRITE_ONLY_EDIT` read requirement is therefore *policy only*, as the md's second paragraph correctly says, and it is not observed adapter behaviour.
- The CritRuntime read uses the selector spelling `<target>:raw`. Under `EDIT_TRAVERSAL` ("no … alternate spelling expands the target list"), a strict literal C2 audit of this real expansion would either have to reject it or normalise `:raw`. [INFERENCE] This is a cross-claim risk for C2, outside this seat's read set.

## Observation mutations `evidence_ok` accepts and should not

All of these pass the per-row predicate (lines 103–111) and the shape-set equality (line 112):

1. **The content of starts is unchecked.** Only `isinstance(list) and non-empty` is tested (line 108). The gate accepts `recorded_starts: [null]`, `[1]`, `[{}]`, `[{"tool":"bash","path":"/etc/shadow"}]`, or a start whose `path` is a different seat's file or a URL. The selftest "clean" fixture (lines 183–187) itself uses starts with no `line` or `path`. The stream_content row has only `{'tool':'write'}` and no read. So the selftest certifies as clean exactly what the prose claims is absent.
2. **Order and attribution are unchecked.** You can set every start `line` to 1, set `request_line` to 999, delete `request_line` and `call_id`, duplicate one `call_id` across rows, or swap the CritRuntime and OraclePathArtifact start lists. All of these are accepted. They are provenance and identity mutations.
3. **Body can be smuggled through extra keys.** There is no exact-key check on rows, starts or the top level. Adding `"new_string": "<report text>"` or `"stream_content": …` as a row field, or `"content"` inside a start, is accepted even though `body_fields` still says "omitted; no report text copied". Adding `"native_enforced": true` or `"effect_verified": true` is also accepted.
4. **The file's own `scope` limit is unchecked.** You can delete the observation file's `scope` (line 101) or rewrite it to "proves native permission enforcement and effects". Both are accepted. `accessed` is likewise unchecked. Compare: the policy JSON's `scope` *is* pinned (line 153).
5. **Path spelling is checked only for a `LANE` prefix and the absence of `/../`** (line 107). The gate accepts `LANE + 'x/..'` (a trailing dot-segment that resolves to the lane root), `LANE + '.ufo/./…'`, `LANE + '.ufo//…'`, a `:raw` suffix, bare `LANE` (a directory), and an embedded newline or NUL. It also accepts any in-lane target such as `LANE + '.git/config'` or `LANE + 'corpus/SOURCES.md'`, which falsely records production edits as observed. The evidence gate thus admits exactly the alternate spellings that `EDIT_TRAVERSAL` forbids.
6. **Identity is unchecked.** The gate accepts a `transcript_sha256` of `'a'*64` on every row, or the same agent with different digests, or different agents with the same digest. It also does not check that `seat`/`agent` are present. Some non-mutation inputs go down the wrong path: a non-string `transcript_sha256` or a non-dict row raises TypeError inside `re.fullmatch` or the indexing, which comes out as `EDIT-SCHEMA` with code 2 instead of `EDIT-EVIDENCE`. That is a misclassification, not an acceptance.

What the gate does reject (bounded search, no falsifier found): a wrong `tool`; duplicate or extra argument keys; a missing shape; an empty or non-list `observations`; a wrong schema; duplicate JSON keys; a copied `body_fields`; an outside-lane path or one containing `/../`; a non-hex digest.

## Impacted axes

- **depth (C1):** the evidence leg is decorative for steps. The score of 8 is unaffected by any of the mutations above.
- **calibration/provenance:** the docstring and md line 7 claim adapter steps under a parent call ID, but the data shows inverted ordering and no linkage.
- **operability (C2, cross-claim [INFERENCE]):** the real expansion spelling `:raw` is in tension with `EDIT_TRAVERSAL`.
- **frontier:** none.

## Smallest safe correction (in-scope, two files plus selftest)

1. **In `evidence_ok`, check keys exactly:**
   - top level must be `{schema, accessed, observations, scope}`, with `scope` equal to the file's literal limit;
   - each row must be `{seat, agent, transcript_sha256, request_line, call_id, tool, argument_keys, path, body_fields, recorded_starts}`, with `request_line` a positive int, `call_id` a non-empty str and unique;
   - each start must be `{line, tool, path}`, with `line` an int, `tool` in `{read, write, edit}`, and `path` in `{row.path, row.path + ':raw'}`.
2. **Reject non-canonical row paths.** Reject a row `path` whose canonical form differs from its literal spelling: no `/./`, `//`, a trailing `/..` or `/.`, a `:` selector, or a control character.
3. **Do not encode an ordering claim the data contradicts.** Narrow md line 7 and the docstring to something like: "Recorded starts are listed per observation without a parent call ID; their ordering relative to the request is not established (CritRuntime starts at lines 12–13 precede request line 15); a read start is observed only for the stream_content shape, never for old/new_string edits; the read requirement is lane policy." Do not add a `line > request_line` check, because it would fail the real S086 data. That failure would itself be the falsifier.
4. **Add selftest mutants** for each item above. Replace the fixture's bare `{'tool':'write'}` starts with full `{line, tool, path}` objects that mirror the real shapes: read `:raw` plus write for stream_content, a single edit for old/new.

Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-fxc1evidence
Scope: executed=none

Lane bounds: leaf member — no subagent dispatch.
