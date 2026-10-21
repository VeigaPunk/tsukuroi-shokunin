# FxC2Prefix — exact-file admission vs prefix and child spellings

- Target: `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py` (candidate tree)
- Target digest (declared by assignment): c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4 — not recomputed here, no execution is permitted.
- Attack predicate: the allowed filename used as a prefix (`P + '-extra'`) or as a parent (`P + '/child'`) must not be admitted as the exact file `P`.
- Verdict: the predicate holds for every spelling examined. No source-visible over-acceptance was found.

## Source-visible code path

1. `local` (lines 33-36) requires `path.startswith(LANE + '/')` (LANE at line 16), bans `\` and `*?[];:`, bans control/format/surrogate/line-separator characters, and bans empty, `.` and `..` components.
2. `requested_path` (lines 43-56) rejects URL/host:port spellings, special-cases the literal skill URI at 48-49, strips a trailing read selector at 50-53, then applies `local` at 54-55.
3. `classify` (lines 60-92) splits `;` only for grep/glob (line 84), normalizes read spellings at line 87, and has exactly one acceptance branch: exact list membership at lines 90-91; failure appends `SCOPE-PATH-DENIED`.
4. No `fnmatch`, `commonpath`, `normpath`, `realpath`, `is_relative_to`, glob match, or per-entry `startswith` is applied to request or binding paths. The only `resolve()` in the file is on the script's own `ROOT` (line 15). Verified by grep over the target.
5. Binding validation (lines 109-114) requires every declared read/write path to pass `local()` (or be the literal skill URI in read paths only). A declared name therefore can never contain `:`, so selector stripping can only remove a trailing `:...` suffix; it can never synthesize a declared string from a longer or child spelling.

## Why prefix and child cannot count as exact

- Prefix: `P + '-extra'` passes `local()` (still under LANE, no forbidden character or component) but is not equal to any declared string, so line 90 denies it.
- Child: `P + '/child'` passes `local()` but is not equal to any declared string, so line 90 denies it.
- Selector-normalized variants fail identically because the only normalization deletes a trailing selector: `P + '-extra' + ':1-5'` reduces to `P-extra`, and `P + '/child' + ':raw'` reduces to `P/child`; both then fail exact membership. A colon left in the base is rejected by `local()` (line 35).
- Traversal and glob spellings (`P + '/../sibling'`, `P + '/./x'`, `P + '//x'`, `P + '/**'`) are stopped earlier by `local()`'s component and character filters.
- A non-ASCII colon (U+FF1A) is not matched by the ASCII selector regex and cannot equal `P`, so it is denied.
- Read selector ranges (`P + ':1-5'`, fixture line 164 expecting exit 0) are intentionally the same file with a range/mode, not a different file; that case is outside the attack's meaning of prefix/child.

## Expected fixture verdict vs observed runtime

Source-derived expectations, no fixture invocation:

| Fixture case | Lines | Expected exit | Expected finding | Expected pass |
|---|---|---|---|---|
| read `src + '-extra'` | 173-174 | 1 | SCOPE-PATH-DENIED | PASS |
| read `src + '/child'` | 173-174 | 1 | SCOPE-PATH-DENIED | PASS |
| write `report + '.extra'` | 175-176 | 1 | SCOPE-PATH-DENIED | PASS |
| write `report + '/child'` | 175-176 | 1 | SCOPE-PATH-DENIED | PASS |
| grep `src + ';/outside'` | 177 | 1 | SCOPE-PATH-DENIED | PASS |
| whole selftest | 154-198 | 0 overall | all cases pass | PASS expected |

Non-vacuity: `local()` returns True for all four suffix/child spellings, so their denial can only come from the exact-membership line 90, not from the character/component filters.

Mutant discrimination: replacing line 90 with `any(path.startswith(p) for p in declared)` would admit both `-extra` and `/child` and return exit 0, contradicting the expected exit 1; a child-only predicate (`p + '/'`) would also be caught by the `/child` case. Both prefix-matching mutants fail the fixture.

Attribution caveat: `path-LANE/../sibling/file`, `path-LANE/x/../source`, `path-LANE/./source`, `path-LANE/**`, `path-source`, `path-xd://tool`, `path-artifact://a` are all denied before membership by the LANE-prefix, component, or character filters. They do not isolate the exact-file rule; only the four `-extra`/`/child` cases do, and those share the `SCOPE-PATH-DENIED` id with the earlier filters, so output alone does not name the firing rule.

Observed runtime: none. This seat is NO-EXEC with empty command and fetch lists; the selftest was not run and no exit code, stdout, or JSON was observed. Every verdict above is source-derived, not observed.

## Residual limits, not predicate failures

- Spellings only: symlinks, hardlinks, case-insensitive or Unicode-normalizing filesystems, and reader-side normalization are not detected. Target line 17 explicitly disclaims symlink/effect proof and reading proof.
- A declared path naming a directory is admitted exactly; children of that directory are denied (fail-closed).
- `read skill://godspeed:1-5` is denied because the skill special case at 48-49 precedes selector stripping: a false-negative, fail-closed, not an over-acceptance.
- Extra `args` keys alongside `path` are ignored; this predicate covers file exactness only.
- The declared digest could not be recomputed under NO-EXEC, so the reviewed bytes are pinned only by the assignment's declared value.

Confidence: high on the source-visible predicate, because acceptance is a single exact list membership with no path normalization; medium on fixture exit codes, because they were not executed.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2prefix
Scope: executed=none
