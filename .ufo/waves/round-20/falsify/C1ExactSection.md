# C1ExactSection: OUT-009 section gate falsification (round 20, attempt 1)

- Seat: `TsukuroiR19Recovery.C1ExactSection` (leaf; NO-EXEC; read, grep, glob, and this report only; no subagents)
- Target: `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py`: `_ownership_correction` L135-196; constants L43-61; call site L761-764; CLI flag L787-788
- Baseline: `0cbc34dd6b20896085a8fb07943e3ea4027d8472`
- Lane-relative report path per parent clarification.

## Verdict

- **Section gate (title / body / suffix): bounded pass.** No whitespace, duplicate-heading, moved-section, or appended-text variant reaches `return 1, []` (L196). The only accepted committed `PROVINCE.md` is the baseline blob followed by `"\n" + "\n".join(OWNERSHIP_SECTION_LINES) + "\n"` (L173-175).
- **Claim-level counterexample (evidence binding, not a gate evasion):** the claimed `ownership_corrections 0->1` has no bindable witness today. Every revision `bind()` accepts is an ancestor-or-equal of `0cbc34dd`, whose `PROVINCE.md` has no R20 section [INFERENCE: derived from the candidate worktree at that commit; see F1]. The gate therefore returns count 0 and FAIL. See F1.

## How the pass is bounded (source)

1. Baseline bytes: `reader.read(OWNERSHIP_BASELINE, "PROVINCE.md")`, L156-159. This reads commit `0cbc34dd`, not the working tree.
2. Province bytes: `_text(reader, revision, "PROVINCE.md")`, L481. `_text` is L300-305; `GitReader.read` is L264-294. `read` requires a regular committed blob (ls-tree mode 100644/100755 and type blob, L287-289) and returns raw `git show` bytes (L291). `revision` is the sha from `bind()` (L821).
3. Title: exact-line match over `province_text.splitlines()`, L162-163. Zero matches go to L164-168 (MISSING only when bytes equal baseline, otherwise INVALID). Two or more go to L169-170.
4. Prefix: `current_data.startswith(baseline_data)`, L171-172.
5. Body and EOF: `current_data[len(baseline_data):] != expected_suffix`, L173-175.
6. Pass: L196, reached only after the pinned snapshot digest and quote (L178-190) and the ADJ-06 arbitration context (L192-195).

Steps 4-5 force `current_data == baseline_data + expected_suffix`. For a given baseline blob, the accepted set has exactly one element.

## Vector results

| Vector | Attempt | Where it fails | Pass? |
|---|---|---|---|
| Title whitespace | trailing space, NBSP, tab on heading line | L163 misses, so L165/L168 INVALID; if splitlines still matches (CR, U+2028), L174-175 byte check fails | No |
| Body whitespace | double space, trailing space, tab in a section line | L174-175 | No |
| Line endings | CRLF or lone CR in section | L174-175 (no CR in lane file) | No |
| EOF | missing or extra trailing `\n` | L174-175 | No |
| Duplicate heading | second exact copy of heading or section | L169-170; L174-175 | No |
| Near-duplicate heading | `###` level, different dash, trailing space | Not counted by L163; L174-175 rejects extra bytes | No |
| Moved section, before baseline text | section inserted into baseline body | L171-172 | No |
| Moved section, reordered in tail | paragraphs rearranged inside tail | L174-175 | No |
| Appended text after section | new paragraph or section after EOF text | L174-175 | No |
| Text between baseline and section | inserted paragraph before heading | L174-175 | No |
| Heading already in baseline | baseline containing the heading, suffix empty | L169-170, or L174-175 (suffix must be non-empty) | No |
| Working-tree-only text | section present in worktree but not in a commit | Never read: L481 uses the bound blob; `bind()` `_revision.py` L134-154 | Not a pass (F1) |
| Symlink or non-regular blob | `PROVINCE.md` as symlink | L287-289 unsafe, `_text` L304-305 raises, CANNOT | No |
| Textconv, replace, global config | git config, replace refs, `GIT_*` env | `clean_env` `_revision.py` L61-65; see below | No |

Other paths checked:
- Git plumbing: `clean_env()` (`_revision.py` L61-65) strips `GIT_*` and sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`. Lane `.git/config` (17 lines) defines no diff, filter, textconv, or replace sections. `.git/info/` holds only `exclude`. The lane `.git` listing shows no `refs/replace/` and no `packed-refs`. I found no textconv or replacement substitution path.
- Lane section bytes against gate constants: lane `PROVINCE.md:148-152` against L43 and L44-59. The heading em dash is the same code point on both sides (one grep hit each). Curly double quotes match on both sides (`“Revenger owns”`). Apostrophes are ASCII on both sides (no U+2018 or U+2019). No NBSP, en space, ZWSP, BOM, U+2028/2029, U+0085, CR, trailing spaces, code fences, or HTML comments appear in the lane file (whole-file scan). Constant block L43-64 has no unusual spaces. A cross-line grep for `ownership-corrections` followed by a backtick, a period, one newline, and end of file matches the lane file end (L152).

## Findings (severity order)

### F1: High for C1 claim (evidence binding; not a gate evasion)

- `bind()` (`_revision.py` L134-154) accepts a revision only if it is an ancestor-or-equal of `refs/heads/master` (L146-147). Because `origin/master` exists, it must also be an ancestor of `refs/remotes/origin/master` (L148-153). `_ancestor` is `merge-base --is-ancestor` (L118-122). The CLI default is `--branch master` (L789-790).
- Both refs resolve to `0cbc34dd`: `.git/refs/heads/master:1` and `.git/refs/remotes/origin/master:1`, relative to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`.
- The lane HEAD is `0cbc34dd` (`.git/HEAD:1`). The last reflog transition in `.git/logs/HEAD:73` ends at `0cbc34dd`.
- The candidate branch `round20-adjacency-20261021` is `0cbc34dd` (`.git/refs/heads/round20-adjacency-20261021:1`). The candidate worktree HEAD points to that branch (`.git/worktrees/tsukuroi-r20-adjacency-20261021/HEAD:1`).
- The candidate `PROVINCE.md` (`/tmp/tsukuroi-r20-adjacency-20261021/PROVINCE.md`) ends at line 146 (the OUT-010 digest). No R20 heading matches.
- The lane `PROVINCE.md:147-152` holds the only occurrence I found. No git ref or HEAD I could read reaches it.
- The lane production `tools/check-adjacency-anchors.py` has no `_ownership_correction`, no `OWNERSHIP_*` constants, and no `--ownership-corrections`. Its only `ownership` matches are unrelated text at L27 and L326. The gate code is therefore absent from production. [INFERENCE] The candidate branch tip is the baseline, so the gate code is probably uncommitted in the candidate worktree; not byte-checked.
- Consequences:
  - At `0cbc34dd`, the gate returns `(0, OWNERSHIP-CORRECTION-MISSING)` (L165-167), so `evaluate` returns FAIL, exit 1 (L766; codes at L20).
  - Ancestors of `0cbc34dd` return `(0, INVALID)` (L168, L172, L175), also FAIL.
  - Non-ancestors raise E-NOT-LANDED (`_revision.py` L146-147), which `main` turns into CANNOT, exit 2 (L841-844).
- For count 1 to be observable, all of these must happen: commit the section on a branch; land it on `master`; push it to `origin/master` (required by L148-153); and land the gate code in production. None of these was performed or checked (NO-EXEC).
- [INFERENCE] `0cbc34dd:PROVINCE.md` has no R20 section. This is derived from the candidate worktree at HEAD `0cbc34dd` and the lane HEAD, not byte-checked.

### F2: Low (planning hazard): stale "omission" finding

- `.ufo/waves/round-20/build/ConnPlanner.md`, item 3, cites `check-adjacency-anchors.py:123-178` and says `_ownership_correction` "never compares `lines[:start]` against the baseline." The current candidate does compare the prefix (L171-172) and the exact suffix (L173-175). Do not carry this finding forward.
- Its baseline-red expectation (`OWNERSHIP-CORRECTION-MISSING`, count 0) matches current L165-167 by source reading. It was not executed.

### F3: Low (design brittleness; fails closed)

- Count 1 is reachable only when the file ends exactly with the R20 section (L173-175). Any later landed append after that section makes `ownership_corrections` INVALID (count 0, FAIL) at that revision, even if the R20 text is intact. This is not an evasion. A later round's append requires a gate change first.

### F4: Info (measurement semantics)

- `counts["ownership_corrections"]` defaults to 0 (L373). It is written only when `--ownership-corrections` is passed (L761-764; flag L787-788). A run without the flag reports 0 by default, which is not a measurement. With the flag at baseline, the measured result is 0 with FAIL (L165-167).

### F5: Info (committed-blob dependencies not verified)

- The gate also reads committed blobs at the bound revision:
  - registry `corpus/knowledge/adjacency-anchors-r19.json` (`main` L829);
  - census `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json` (L467-474);
  - Revenger snapshot `.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md` (L178-181).
- Missing or unsafe blobs yield INVALID or CANNOT. I did not verify that these are present in the `0cbc34dd` tree (no git object reads).

### F6: Info (outside section gate; not exercised)

- `OWNERSHIP_PIN` (L146-147) and `OWNERSHIP_CENSUS_PIN` (L152-153) compare with Python `!=`. A JSON `3.0` equals the pinned `3`, and `[[3.0,7],[19,25]]` equals `[[3,7],[19,25]]`.
- The section gate's snapshot check takes `quote_line` from the constant (L186), not the registry, so the section gate is unaffected. The type-strictness of the outbound checks in `evaluate` was not inspected.

## Limits and verification gaps

- NO-EXEC: the gate, selftests, git, and jj were not run. Every outcome above is derived from source, refs, logs, and worktree files. Selftests were not treated as evidence (out of scope).
- Lane `PROVINCE.md` lines 1-146 were not byte-compared to `0cbc34dd`. The candidate worktree served as proxy. Any prefix drift is rejected at L171-172 (fails closed). This affects F1's positive path, not the pass verdict.
- jj working-copy state and `refs/jj/keep` objects are unreadable without execution. Bindability is git-ancestry-based (`_revision.py` L146-147), so they cannot change F1.
- Other R20 branch tips (`round20-execscope`, `round20-registry`, `round20-binder`) were not read. Bindable revisions remain ancestors of `0cbc34dd` regardless, because `master` and `origin/master` both point there.
- Boot images remain UNKNOWN; no clearance. No host, boot, or package safety is claimed.

## Installs or updates

- None.

Scope: executed=none
