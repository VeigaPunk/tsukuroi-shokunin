VERDICT: defect-found

Seat R51Simplifier, wave w1, item N-9. Scope: the five round-51 tools and controls/battery.py at 2732ee6c06108c031c4d8043239b994e0504eb2f. Read-only; nothing edited, nothing run beyond `git show <REV>:<path>` and reads of my scratch copies.

## Evidence base and what was not done

- Bytes read with `git -C <lane> show 2732ee6c…:<path>` into scratch, then `cat -n`. Line numbers below are the revision's line numbers.
- All six files are frozen (`.ufo/waves/round-51/frozen/FROZEN-hashes.txt`, lines 1-6). Every proposal below therefore touches frozen bytes. Classes used:
  - [B] behaviour-identical for every counted command and every counted output field: needs a re-freeze in the pre-w2 amendment commit (L1 decision).
  - [D] documentation or echoed-text only; no counter reads the field: needs re-freeze, L1 decision.
  - [U] UNSAFE (frozen): changes a counted verdict or a leg a predicate reads. Surfaced, not proposed as a deletion.
- NOT run: no selftest, no counter, no battery, no pyflakes. The execution class names only the reads in this item. Dead-code and import findings are from reading; I did not confirm that `R50.*` symbols referenced by the adjacency tool exist in `check-adjacency-table-r50.py` (not in scope).
- [INFERENCE] markers are for conclusions drawn from code without a run.

## A. Calibration defects (ranked; the axis the lead judges on)

C-1 [U] `tools/score-counter-cheats-r51.py:134` — `r50_cheats_rejected == 0` is satisfied by a crashed sensitivity control. Only `rc == 1 and verdict == FAIL` increments `rejected['r50']`. If the round-50 counter errors (rc 2, verdict FAIL) or emits ERROR on a cheat, nothing is counted and the leg reads 0, which the predicate accepts. The r51 leg at :134 is not symmetric: a crash there lowers `cheats_rejected` and fails. Surface: the sensitivity control should require that each r50 cheat run produced a measurement (`rc in (0,1)` and verdict PASS or FAIL), then count rejections. [INFERENCE from code; not run.]

C-2 [D]+[U] `tools/check-selftest-matcher-r51.py:55-56` vs `:183` and `tools/score-counter-cheats-r51.py:88,72` — the echoed predicate says `pass_runs == 2`; the code enforces `pass_runs == a.runs` (`:183`), and the counted C2 command runs with the scorer default `--runs 1` (`:88`, passed at `:72`). So the counted C2 run enforces `pass_runs == 1`, not the 2 named in the claim text and the docstring (`:22`, `:31`). Either the echo is wrong (text fix, class [D]) or the frozen claim is wrong (requires `--runs 2` default and a second selftest per cheat, class [U]). L1 must choose before w2; the claim text and the code cannot both stand.

C-3 [U] `tools/check-scrub-admission-r51.py:218-234`, call at `:246` — `verify_citation` is row-blind. It takes the basename and checks every pinned snapshot with that basename (`cands`, `:219`), so a GR3 seat citing `scrub.c:N` resolves if N exists in S242 (GR2's scrub.c) even though GR3's scrub.c is S237. The lint tool maps basenames per row (`tools/lint-grounding-r51.py:16-17`, `:67-74`); the admission tool does not use that mapping. [INFERENCE] that the S237 and S242 scrub.c lengths or contents differ at the cited numbers; not measured. Fix would pass `LINT.PROSE[row]` in and check only that sid. Changes verdicts, so not proposed as a deletion.

C-4 [U-additive] `tools/check-scrub-admission-r51.py:79-92` and `:224-233` — the lane-artifact citation branch is never positively exercised by any control. Battery K8 (`controls/battery.py:156-159`) fails on the two-row-source rule (`:243-244`) and on identical bodies, not on the lane citation. K-pass uses row citations only. The `outside <path>` branch (`:232`) is also untested. Proposed additive control: a K-lane-pass body citing two row sources plus `entry.md:5`, expected PASS. Changes the frozen controls record, so L1 decision.

C-5 [U-additive] `controls/battery.py:80-87` — the `skill_line`, `readme` and `negate` parameters of `marks()` are never passed by any control (`score()` calls at `:133-159` pass none). So the README-negation branch (`check-scrub-admission-r51.py:309-313`) and the SKILL-missing branch are never measured as failing. Likewise no control isolates the stale-hash branch (`check-scrub-admission-r51.py:357-359`) or structural_ok (`:331`, `row_extent` `:156-165`). Either delete the three unused parameters (simplicity) or add the two controls that would use them (calibration), e.g. `score('K9 README negated', 'FAIL', 'k9', entry, negate='is not admitted round 51')` and a `hashes_used` dict with one wrong GR2 value. Recommendation: add them; the parameters are the only route to those legs.

C-6 [B]+[D] `tools/check-adjacency-table-r51.py:208-211` and `:248-254`, `:256-258` — the override child exits 3 at `:208-211` before any file is read (`:216`). The temp copy written at `:249-251` is therefore inert: `override_blocked` measures the guard flag only, and would be 1 for any path. The docstring (`:25-27`, `:48`) says "a copy of the real bytes", which overstates the leg. Proposal: pass `os.devnull` (same outcome) and say in the docstring that the leg measures the guard. [B] for outputs; frozen bytes.

C-7 [D] `tools/check-scrub-admission-r51.py:77-78` vs `:224-232` — the docstring says "the first one that exists at REV and covers the line wins". The code returns on the first existing candidate (`:227-232`) and never tries later ones. Current outcome unaffected (the round-45 SHA256SUMS exists, so candidates 2-4 are never reached). Fix the comment, or make the loop continue past non-covering candidates (the latter is [U] if any later candidate exists at REV; I did not check).

C-8 [B] `tools/lint-grounding-r51.py:277` and `:323` — `declared_gaps` stores parse failures under the sentinel key `('?', text)` inside the gap map, and `run()`/`lint_legs` test `key[0] == '?'` to recover them (`check-scrub-admission-r51.py:205`). A reader must reverse-engineer this. Replace with a separate `bad_lines` list appended to `gap_extra` with the identical string `? <text>: unparseable`. Counted outputs unchanged.

C-9 [D] `tools/check-selftest-matcher-r51.py:145-146` — the `-1` sentinel and double-search make the probe parse look like two different rules. Harmless as written; flagged only because of C-2's drift risk.

## B. Dead weight and deletions (proposed minimal diffs)

All [B] unless marked. Each needs the re-freeze in the pre-w2 amendment.

D-1 `check-adjacency-table-r51.py` — `adj` is computed and never used.
  - `:237` `adj, anchors = parse_tables(prov)` → `_, anchors = parse_tables(prov)`.
  - Better: delete `adj` from `parse_tables` (`:166`, `:167-170`) and return `anchors` only; then `:237` and `:242` change accordingly.
  - Also move `import tempfile` (`:248`) to the top import block.

D-2 `check-scrub-admission-r51.py` — unused parameters.
  - `bind_seat` (`:265`): `hashes` and `cache` are never read in the body (`:266-302`); delete from the signature and from the call at `:348-349`.
  - `marks_leg` (`:305`): `hashes` never read; delete from the signature and the call at `:375`.
  - `per_row` copy (`:215`): `{k: v for k, v in per[r].items()}` is `per[r]`.
  - `seat_rows` (`:343`, `:352`, `:362`) is the seat-notes list; rename to `seat_notes` (it is already emitted under that key at `:380`).

D-3 `check-scrub-admission-r51.py` — duplicated logic.
  - `snapshots()` (`:181-189`) duplicates `LINT.load_snapshots` (`lint-grounding-r51.py:189-201`) minus its problems list. Same path, same digest test, same decode and split. Replace `:337` with `cache = LINT.load_snapshots(lane, rev)[0]` and delete `:181-189`.
  - `lint_legs` gap comparison (`:201-206`) duplicates `run()`'s gap comparison (`lint-grounding-r51.py:317-324`). Move one `gap_diff(gaps, decl)` into the lint module and call it from both. gap_ok is identical; only the detail strings change ("no gap block" wording at `:199`).
  - `row_extent` (`:156-165`) duplicates `lint:103-109`. Keep the inner-heading check (`:162-164`) by moving it into the lint version and returning a problem string; lint's `analyze` then fails on inner headings, which the admission structural leg already fails (so the predicate is unchanged) [INFERENCE].
  - `CITE` (`:74-76`) is exactly `LINT.PROSE[row]` minus `capture.txt`. Derive it: `tuple(k for k in LINT.PROSE[row] if k != 'capture.txt')`, with a one-line comment that capture.txt is excluded from the 2-source rule.
  - `LANE_FILES['capture.txt']` (`:91`) is unreachable while the S249 digest matches: `cache` holds `(S249, capture.txt)` (`lint:63-64`) and `verify_citation` returns at `:223` before the lane branch. It is reachable only when the digest moved, and then lint already fails (snapshot problem), so the predicate outcome is unchanged. Delete. [B for predicate; the seat_notes text changes in that state.]

D-4 `lint-grounding-r51.py` — flags nothing counted uses.
  - Counted commands use only `--revision` and `--emit-gaps`. Admission imports `analyze` and `declared_gaps`, not `run()`.
  - Delete `--worktree` (`:27`, `:290`, `:349`, `:355-356` → `required=True` on `--revision`), `--entry-file` and `--sources-file` (`:351-352`, `:291-300` → single `read_bytes` for each), and the `rev is None` branch of `read_bytes` (`:90-95`). `--worktree` reads the mutable working tree, which the lane rules say is not evidence.
  - Then `git_show` (`:83-86`) and `read_bytes` (`:89-96`) collapse into one function.
  - `ROWS`-loop in `run()` (`:325-328`) can be `rows_ok = sum(1 for r in ROWS if not per[r]['problems'])`. Cosmetic.

D-5 `check-adjacency-table-r51.py` — override surface not used by the battery or any counted command.
  - `--skip-anchors-check` (`:206-207` clause, `:228-229`, `:305`): no battery call passes it (`battery.py:200-238` uses only `--control`, `--province-file`, `--registry-file`). Deleting it removes the flag and the r50 child argument. [B for counted outputs; CLI change.]
  - Three identical "last stdout line as JSON" blocks (`:231-236`, `:259-262`, `:269-272`) → one helper `last_json(text)`.
  - The temp-file pair (`:249-254`) collapses to one helper `_tmp(text)`, or to `os.devnull` per C-6.

D-6 `check-selftest-matcher-r51.py` — handle hygiene.
  - `open(census).read()` at `:139` and `open(census,'rb').read()` at `:186` leak handles; read the census bytes once with `with`, hash and decode from the same buffer. [B]

D-7 `score-counter-cheats-r51.py` — duplicate writes.
  - `:103-112`: the `real` file and the four fixtures are written by two loops. Fold `real` into one dict. Caution: `len(fx) == 4` (`:141`) and `cheats: len(fx)` (`:137`) must then use the cheats count, not the dict length. Cosmetic; marginal.

D-8 `controls/battery.py` — duplicate loading and writes.
  - `:214-216` reloads `check-adjacency-table-r50.py`, which `adj.R50` already exposes (`check-adjacency-table-r51.py:75`; loaded at battery `:191-193`). Replace with `m50 = adj.R50`. [B]
  - `build_cohort(cohort=False)` (`:48-53`) duplicates the write block of the full path with a different dispatch shape (`context` key). Cosmetic; keep or fold, not a counter change.
  - `_w` (`:163-167`) is defined after its first use at `:138`. Move it up. Cosmetic.
  - Five `assert` control guards (`:137`, `:142`, `:146`, `:209`, `:235`). `python -O` strips them silently, which would make a control stop checking that its mutation applied. Replace with `if … : raise SystemExit`. [B]
  - The three registry and province mutations (`:221-236`) repeat a load-mutate-write pattern; one helper `mutate(text, key, id, field, value)`. Cosmetic.

## C. Reverse-engineering costs a future reader will hit (no deletion; comment or rename)

R-1 `check-scrub-admission-r51.py:299-301` — a contradicting line returns the string `'partly'` as the verdict, so a seat that says `holds` and also `fails` in its body is coerced to `partly`. Name it: a constant `CONTRADICTED = 'partly'` with a comment, or return `'contradicted'` and count it as blocking (same outcome: the branch at `:354-355` tests `in ('partly','fails')`). [B if constant; a changed string is [U]-neutral only if the blocking test is updated in the same edit.]

R-2 `check-scrub-admission-r51.py:265-302` — `bind_seat` returns a 4-tuple from eight call sites, with the verdict in slot 1 and the detail in slot 4. Works; hard to read. Not proposed.

R-3 `check-scrub-admission-r51.py:374` — `seats_ok` counts seats that bound to any verdict, including `partly` and `fails` (the predicate checks `seats_ok == 18`). The name reads as "seats that passed". Rename would change an output key; comment instead. [D]

R-4 `check-adjacency-table-r51.py:185-186` — `load_registry` swallows every exception (`except Exception: pass`) and returns `{}`; a malformed registry then fails `bound`/`registry_ok` with no reason. Not a counter bug; add the exception text to the output. [B-neutral to verdict; output field added.]

R-5 `check-adjacency-table-r51.py:245`/`:273` — `override_blocked` and `r50_blind` stay 0 in `--control` mode, and `ok` ORs `a.control` (`:284`). Output in control mode therefore shows 0 for two legs that were never run. Comment at `:284`. [D]

R-6 `lint-grounding-r51.py:77` vs `check-scrub-admission-r51.py:71` — two citation regexes with different boundary rules (prose with continuations vs report body). Both intentional; say so in one comment each.

R-7 Named predicate strings: the same PREDICATE is duplicated in four files (`check-scrub-admission-r51.py:72-73`, `check-selftest-matcher-r51.py:55-56`, `check-adjacency-table-r51.py:61-65`, `score-counter-cheats-r51.py:140`) and hand-matched to the `ok` expressions. C-2 shows the drift. Suggest one generated line per tool from the leg table, or a test that asserts `PREDICATE` names every term of `ok`. Not proposed (tool standalone-by-design).

## D. Summary of what is dead

- Unused imports: none found in the five tools or the battery.
- Unused constants: none found (checked each module-level name against its uses).
- Unused functions: none found at module level.
- Unused parameters: `bind_seat` `hashes`, `cache` (`check-scrub-admission-r51.py:265`); `marks_leg` `hashes` (`:305`); battery `marks` `skill_line`, `readme`, `negate` are unused by any control (`battery.py:80`; see C-5).
- Unused locals: `adj` (`check-adjacency-table-r51.py:237`).
- Unused code paths: `LANE_FILES['capture.txt']` (`check-scrub-admission-r51.py:91`); `--worktree`, `--entry-file`, `--sources-file` in lint (`lint:291-300`, `:349-352`); `--skip-anchors-check` in adjacency (`:228-229`).

## E. Proposed order for the pre-w2 amendment (L1 decides; all frozen)

1. Do not change C-1, C-2, C-3, C-4 without a decision: they change counted behaviour or the claim text. Record the choice in FROZEN.md.
2. Apply [B]/[D] deletions D-1, D-2, D-3, D-4, D-5, D-6, C-6, C-7, C-8 only together with a re-freeze, and re-run the counted commands once after the amendment (not by me).
3. If C-5 is taken as additive controls, the battery must be re-run at the freeze to record the new controls (battery.py writes the battery-summary files).

## F. Receipts

None written beyond this report. Source copies lived under /fast/scratch/hyaku/tsukuroi-r51/R51Simplifier/src and are removed at finish.
