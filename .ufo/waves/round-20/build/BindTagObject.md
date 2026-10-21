# Round 20 · C2 · BindTagObject — independent annotated-tag edge-case design

Seat: TsukuroiR19Recovery.BindTagObject-2 (leaf, read-only, NO-EXEC). Baseline 0cbc34dd6b20896085a8fb07943e3ea4027d8472. Axis C2 operability (`object_selector_tools`, preregistered 0 → 9). Output: fixture design, expected results, source justification, and the smallest wrong implementation the fixture kills. No execution, no fixture built, no candidate edits, no Git/index/ref access.

## 0. What was inspected, and the baseline caveat

- `tsukuroi-shokunin/tools/_revision.py` (tag `#64AF`). Byte-identical tag `#64AF` at `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py`. It contains the object-first resolver `_object_commit` (lines 112–146) and `bind` (172–192). So the lane file currently holds candidate-shaped binder code.
- Lane HEAD per `.git/logs/HEAD`, last entry: `0cbc34dd… → 7f4231401e4918146c4442e8633334231c7d88d6` ("export from jj"). `measure/final-r20/results.json` names `baseline` 0cbc34dd… and `measured_revision` 7f4231401e…. I could not verify from the working tree that HEAD 7f42314 holds the `#64AF` bytes.
- Judge inspected: `tsukuroi-shokunin/tools/check-revision-binding.py` (tag `#79C6`, 1238 lines). The `/tmp` binder copy is a different file (`#083B`, 1230 lines). `measure/run.py:72–78` runs the judge from the measured-revision clone (7f42314) in both phases, with digests at `run.py:62–64`. I read the lane copy and take it to be that revision's judge; this is unverified.
- Baseline `_revision.py` bytes were NOT readable. NO-EXEC rules out `git show 0cbc34dd:tools/_revision.py`, and `.git/objects` is zlib-compressed. Baseline semantics come from OracleC2 (`tools/_revision.py:40-48,134-154`: ordinary `revision^{commit}` resolution) and from the measured `measure/final-r20/c2-before.stdout`.
- BindTagPeel cites a production `_commit` at lines 134–141, and a `git(` helper at `/tmp` lines 291–292, and a four-argument `accepted`. None of that matches the current copies: `_commit` is at 98–109 in both, and no `git(repo` call exists in either `_revision.py`. The lane judge's `accepted` (line 396) takes `branch`, so the arity defect is not present there. I do not carry these forward.

## 1. Findings (severity order)

**F1 High — no tree-object row exists anywhere.** In the object-selector probes the only non-commit row is `noncommit_blob` (`check-revision-binding.py:632`, blob built at :411–416); the shared probe `blob-revision` (:452) is blob-only too. The binder selftest's only non-commit row is `blob-revision-invalid` (`_revision.py:400–403`). A grep of both files finds no tree-object probe, only `ls-tree` and AST identifiers. `preregister.json` `expected.C2` has 10 keys and none for tree or tag-to-non-commit. "Blob/tree does not peel" is therefore unmeasured for trees.

**F2 High — the existing annotated-tag rows are preservation controls, not discriminators.**
- Judge: `annotated_tag_object` (:630) and `annotated_tag_prefix` (:631). The prefix selector (:589–596) explicitly skips any width that collides with a `refs/heads/` or `refs/tags/` name.
- Binder: `annotated-tag-full-object-id` and `annotated-tag-object-prefix` (`_revision.py:360–361`). The prefix (:357–359) has no collision check and no shadow.
- Measured: `c2-before.stdout` is a single 93 KB JSON line. Its first `object_selector_per_tool` entry (match at column ≈619) shows `annotated_tag_object` and `annotated_tag_prefix` as `exit 0, json_revision 0cbc34dd…, ok true` on the baseline tools. In that entry the baseline tools already pass both, so these rows cannot show object-first behaviour. I read only the grep-visible prefix of that line, so other per-tool entries are unverified.

**F3 High — no tag-to-non-commit row, so a one-token peel regression passes every existing row.** Peeling uses `^{commit}` (`_revision.py:139–140`; judge :160–161). The gitrevisions page defines `<rev>^{}` as dereferencing a tag recursively until a non-tag object is found. So `TR^{}` yields the tree SHA. No existing row has a tag whose target is a non-commit. See W2 in §5.

**F4 Medium — the ambiguity row's seed is order-dependent.** `_revision.py:373–376` picks the first object in `--batch-all-objects` order whose 4-hex prefix is unique, then asserts `_object_commit(...) is None` (:393–394). If the seed is a blob or tree, a "count only commit-or-tag" filter also returns None, so the row misses that regression. The docstring at `_revision.py:115–116` names exactly that mistake. Anchoring the seed to an annotated tag makes the kill deterministic (R15).

**F5 Medium — the judge's resolver is a code twin, and it also sets the expected tip.** `check-revision-binding.py:139–166` mirrors `_revision.py:119–146` step for step: disambiguate, `cat-file -t`, `^{commit}`. Also, `measure` computes the expected tip through the judge's own `bind` (`:677` → `:197` → `object_commit`). A shared algorithmic error would shift the expected value. Independence for C2 rows therefore has to come from expectations fixed by construction, never from `object_commit()`.

**F6 Medium — governance: new rows cannot join the graded C2 count.** The evaluator is digest-pinned (`run.py:62–64`) and already measured in `final-r20` (`run.py:70–78`). `preregister.json` says expected outputs were fixed before candidate output. Adding rows now changes the evaluator and the oracle after candidate output was observed. They may only be reported as a separately pre-registered addendum or an informational sub-check.

**F7 Low — shadow decoy falls back to an unlanded commit.** `check-revision-binding.py:603` is `decoy = parent or unlanded_sha`. OracleC2 requires a landed and pushed decoy, so only object identity distinguishes the result. With a root tools revision, the identity check silently degrades to an exit-code check. New shadow rows must use a landed and pushed decoy and return CANNOT when none exists.

**F8 Low — process caveat.** The baseline and candidate identity question (§0) needs L1 to run `git show 0cbc34dd:tools/_revision.py` at integration. I did not run it.

## 2. Synthetic fixture (exact construction, hermetic)

Git is invoked with `-c user.name=… -c user.email=… -c commit.gpgsign=false -c tag.gpgSign=false`, with `GIT_*` env stripped as the judge does now.

1. `git init --quiet r`, then `git symbolic-ref HEAD refs/heads/master`.
2. `git commit --allow-empty -m base` → **C0**. `git commit --allow-empty -m tip` → **C** (master = C).
3. `git update-ref refs/remotes/origin/master C`. C0 and C are now landed and pushed.
4. `git checkout --detach C0`, `git commit --allow-empty -m unlanded` → **U**, then `git checkout --quiet master`. (In the judge, reuse `unlanded_sha`.)
5. Blob: `git hash-object -w --stdin` with stdin bytes `r20 tag-object fixture blob\n` → **B**.
6. Non-empty stored tree: pipe `100644 blob <B><TAB>fixture.txt` followed by a newline into `git mktree` → **R**. Do not use the empty tree `4b825dc…`: git treats it as a built-in object, so its enumeration behaviour is version-dependent [INFERENCE].
7. Annotated tags, each `git tag -a <name> -m "r20 fixture" <object>`. The git-tag synopsis takes `<commit> | <object>`.
   - `r20-tag-object` → target C. Its tag object **T** is `git rev-parse refs/tags/r20-tag-object^{tag}`.
   - `r20-tag-blob` → target B. **TB**.
   - `r20-tag-tree` → target R. **TR**.
   - `r20-tag-unlanded` → target U. **TU**.
   - `r20-tag-nested` → target T (tag of a tag). **TN**.
   - Optional: `r20-tag-unref` → target C, then `git tag -d r20-tag-unref`. The object survives unreferenced. **TX**. Contract-derived, not preregistered.
8. Refresh the inventory only after steps 5–7: `git cat-file --batch-all-objects --batch-check=%(objectname)`. The judge refreshes only at `:509–512` and `:568–577`, so reusing those lists would miss the new objects.
9. Expected constants C, B, R, T, TB, TR, TU, TN, TX come from construction. Never derive them from `bind` or `object_commit`.

**Unique-prefix rule** for X in {T, B, R}: w(X) = min{ w ≥ 7 : exactly one inventory object starts with X[:w], and neither `refs/heads/X[:w]` nor `refs/tags/X[:w]` exists }. Compute w before creating any shadow ref for that row.

**Shadow setup** (R4, R5): `update-ref refs/heads/T[:w] C0` for R4, or `update-ref refs/tags/T[:w] C0` for R5. Delete it afterwards. C0 is landed and pushed. If the tools revision has no parent, return CANNOT. Do not fall back to an unlanded decoy.

**Ambiguity fixture** (R15, binder selftest only): take p = T[:4]. Search bodies `r20-collision-<i>` for i = 0, 1, … until `sha1(b"blob " + len + b"\0" + body)` starts with p. Expect about 2^16 trials. Store with `hash-object -w`. Precondition: exactly one commit-or-tag object (T) starts with p. Then `_object_commit(repo, p)` must return None.

## 3. Expected results

Judge semantics (`:383–404`, `:406–408`, `:480–489`): an accepted row needs exit ≠ 2 and JSON `revision` equal to the expected commit, compared lowercase. A refusal row needs exit 2, finding id equal to the expected one, exactly one binding finding, and a JSON `revision` that is not a 40-hex SHA. Binder rows need `bind(repo, sel).sha == X` or `RevisionError.fid == E_*`.

| Row | Selector | Binder expectation | Tool expectation | Status |
|---|---|---|---|---|
| R1 T-full | T | sha = C | accept, revision = C | existing (judge :630, binder :360); baseline entry 1 measured ok |
| R2 T-upper | T.upper() | sha = C | accept, revision = C | new (cheap) |
| R3 T-prefix | T[:w] | sha = C | accept, revision = C | existing (judge :631, binder :361); baseline entry 1 measured ok |
| R4 T-prefix-branch-shadow | T[:w] with refs/heads/T[:w] → C0 | sha = C, never C0 | accept, revision = C | new; discriminates ref-first spelling resolution |
| R5 T-prefix-tag-shadow | T[:w] with refs/tags/T[:w] → C0 | sha = C, never C0 | accept, revision = C | new |
| R6 TN-nested | TN | sha = C | accept, revision = C | new; positive control for recursive deref |
| R7 TU-unlanded | TU | E-REVISION-NOT-LANDED | exit 2, [E-REVISION-NOT-LANDED], count 1 | new; landing gate applies to the peeled commit |
| R8 TX-unref (optional) | TX | sha = C | accept, revision = C | new; contract-derived, flagged |
| R9 B-full | B | E-REVISION-INVALID | exit 2, [E-REVISION-INVALID], count 1 | existing (judge :632, binder :403) |
| R10 B-prefix (optional) | B[:w] | E-REVISION-INVALID | same as R9 | new |
| R11 R-full | R | E-REVISION-INVALID | same as R9 | new |
| R12 R-prefix | R[:w] | E-REVISION-INVALID | same as R9 | new |
| R13 TB-full | TB | E-REVISION-INVALID | same as R9 | new |
| R14 TR-full | TR | E-REVISION-INVALID | same as R9 | new |
| R15 T4-collision (binder only) | `_object_commit(repo, T[:4])` | returns None | n/a (tool rejects < 7 hex at REV) | new; unit-level only |

R7 detail: the refusal carries `sha[:12]` of the peeled commit U.

## 4. Source justification

Official docs, read from the public pages in this seat:
- gitrevisions (2.56.0 page, https://git-scm.com/docs/gitrevisions). `<sha1>` is "the full SHA-1 object name … or a leading substring that is unique within the repository." `<rev>^{<type>}` dereferences recursively "until an object of type <type> is found or the object cannot be dereferenced anymore (in which case, barf)." `<rev>^{}` "dereference[s] the tag recursively until a non-tag object is found." The `<refname>` rule orders refnames only and does not state how a hex abbreviation competes with a same-named ref.
- git-rev-parse (https://git-scm.com/docs/git-rev-parse). `--disambiguate=<prefix>` lists every object beginning with the prefix, and the prefix "must be at least 4 hexadecimal digits long."
- git-tag (https://git-scm.com/docs/git-tag). Synopsis `git tag … <tagname> [<commit> | <object>]`, so a tag may point at any object type.
- git-mktree (https://git-scm.com/docs/git-mktree). Builds a tree from ls-tree-format input and verifies that each entry's object exists unless `--missing` is given.

Code, lane `tools/_revision.py` (#64AF):
- `_object_commit` (112–146): `--disambiguate` lowercased (119), exactly one object required (123–124), `cat-file -t` (127), commit returned directly (134–135), any non-tag returns None (136–137), tag peeled with `^{commit}` (139–142), unreadable repo raises (143–146).
- `bind` (172–192): None becomes E-REVISION-INVALID (178–179). Landing (184–185) and push (189–190) checks run on `sha`, the peeled commit. `Binding.sha` is that commit (192).

Judge, lane `tools/check-revision-binding.py` (#79C6):
- `object_commit` (139–166) and `bind` (192–208); tag prefix selection (589–596); shadow decoy (597–603); object rows (615–633); tag-name collision raise (497–500); inventory refresh (509–512, 568–577).

Inference, not verified in this NO-EXEC seat: Git's `get_oid_basic` resolves a non-full hex selector through refs before abbreviated object lookup, and resolves a full 40-hex selector object-first. That is why R4 and R5 should fail for spelling-based resolution while full-OID shadows are not new discriminators. The measured judge run is the only verification. [INFERENCE]

## 5. Wrong implementations and kills

- **W2, the smallest kill (new). Killed only by R13 and R14.** Change the tag peel `^{commit}` (`_revision.py:139–140`, judge :160–161) to `^{}`. This is a one-token edit beside the `^{commit}` line. It passes every existing row: R1, R3, the judge's `full_tag_object_id_ref_shadow`, `noncommit_blob`, the binder blob row, and the ambiguity row (which returns None regardless). On TR, `bind` receives the tree SHA. `_ancestor` then fails on a non-commit, giving E-GIT-FAILED or E-REVISION-NOT-LANDED depending on git's merge-base exit code for a non-commit [INFERENCE]. Either way the finding is not E-REVISION-INVALID, so the row fails. TB behaves the same way.
- **W1, already covered.** A tag returns its own OID without peeling. R1 and R3 kill it (sha = T ≠ C; judge revision T ≠ C). It is caught even if merge-base peels tags, because the identity assertion fails. Not a new kill.
- **W4, new kill via R4 and R5.** The tag prefix is resolved by its spelling (`rev-parse <spelling>^{commit}`) rather than by object identity. It returns C0, which fails the sha = C check.
- **W5, new kill via R11 and R12.** A guard that rejects only blobs lets trees fall through and be returned as a SHA. The result is E-GIT-FAILED or E-REVISION-NOT-LANDED. Existing rows are blob-only, so they miss it.
- **W3, new kill via R15 only.** `--disambiguate` results are filtered to commit-or-tag before counting, which is the mistake named at `_revision.py:115–116`. The existing ambiguity row catches it only when its arbitrary seed happens to be a commit or tag.

## 6. Constraints for the later build (not performed here)

- Refresh the inventory after creating any new object. Do not reuse the lists from `:509–512` or `:568–577`.
- Use tag names distinct from `r20-object-selector-<name>`, since `:497–500` raises when that ref exists.
- Do not fall back to `unlanded_sha` as the shadow decoy. Remove `parent or unlanded_sha` at `:603` in the build, or CANNOT when there is no parent.
- Keep R-rows out of `object_selector_tools` unless the oracle is amended before measurement. Report them as a separate informational sub-check, since the judge digest changes.
- If an installed git refuses `git tag -a` on a blob or tree, the fallback is `git mktag` with a hand-written `object`/`type`/`tag`/`tagger` body [INFERENCE; verify at build].

## 7. Limits and residual risk

- Every expected result above is a source-derived prediction. Measured evidence exists only for R1 and R3, and only in the first per-tool baseline entry of `c2-before.stdout` (partially visible). The candidate's `c2-after.stdout` was not read.
- Baseline `_revision.py` bytes were not inspected, and the lane file equals the candidate tag `#64AF` (§0). L1 must run `git show 0cbc34dd:tools/_revision.py` to confirm baseline `^{commit}` behaviour on the prefix-shadow rows.
- Refusal payloads for each of the nine consumers were not inspected individually. The judge's `_has_bound_sha` assumes refusals carry no 40-hex `revision`. I saw only the payload builder at `check-seat-scope.py:157–158`, which sets `"revision"` from a variable. Whether refusals set it to null is unverified.
- No LSP device is available in this seat, so caller and definition claims rest on literal grep only.
- Nothing here addresses host, boot, or live readiness. No clearance is implied.
- No tool was installed or updated in this seat.

Scope: executed=none
