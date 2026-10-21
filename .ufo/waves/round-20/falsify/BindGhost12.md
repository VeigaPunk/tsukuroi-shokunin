# BindGhost12: 12-hex ghost branch and lightweight-tag fixtures (binder and independent judge)

Seat: TsukuroiR19Recovery.BindGhost12 (reviewer, leaf, NO-EXEC). Round 20, attempt 1. Baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472`.

Candidate read (read-only):
- `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py` (383 lines)
- `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py` (1124 lines)
- the nine original consumers in the same `tools/` directory

## Verdict

- **Binder 12-hex fixtures are correct by source.** Both refs point to the landed tip, no object matches the selector at construction, and the expected result is exactly `E-REVISION-INVALID` (exact tuple comparison). A ref-first fallback would fail them.
- **Judge 12-hex equivalents have correct fixture logic but cannot produce a verdict.** The object-selector path raises `TypeError` at `check-revision-binding.py:594`, after the ghost probes have run and before they are returned. `--object-selectors` cannot report the C2 metric, and `--selftest` cannot complete.
- Gaps: F1 (blocking), F2 (selftest cannot pass even after F1), F3 to F11 below.
- Nothing was executed. F1 and F2 are deterministic from source. F6 and the Git behaviour in F10 are inferences.

## Method and limits

- Tools: read, grep, glob, write (this report only). No bash, eval, git, tests, or builds. Nothing in the lane or the candidate was modified.
- `lsp`: not exposed in this seat's tool surface. Caller and definition evidence is literal text grep, not semantic proof.
- Git behaviour cited from the local Git 2.56.0 manual pages: `gitrevisions(7)` (`/usr/share/man/man7/gitrevisions.7.gz`) and `git-rev-parse(1)` (`/usr/share/man/man1/git-rev-parse.1.gz`).
- Lane build reports (`.ufo/waves/round-20/build/`) were treated as claims. Where they cite pre-candidate lines, they are marked stale below.
- Commit identity and cleanliness of the candidate worktrees were not verified (no git).

## Confirmed (source-level, not executed)

- **Binder branch ghost.** Master is `tip` (`_revision.py:221-228`). Ghost `000000000000` is chosen with no object prefix match (`:268-271`). `refs/heads/<ghost>` is created at `tip` (`:272`). `bind(repo, ghost)` is expected to be `("err", E-REVISION-INVALID)` (`:273`). Comparison is exact (`expect`, `:198-208`).
- **Binder lightweight-tag ghost.** `refs/tags/<ghost>` is created at `tip` (`:275`), with expectation `:276`. Ghost branch deleted first (`:274`), tag deleted after (`:277`).
- **Mechanism.** `bind()` (`:172-192`) never resolves the raw revision as a ref. `_object_commit` (`:112-146`) uses only `rev-parse --disambiguate=<lowercased>` (`:119`) and `cat-file`. Remaining `rev-parse` calls take fixed `refs/heads/<branch>` or `refs/remotes/origin/<branch>` strings or a resolved full OID (`:100`, `:139-140`, `:150`).
- **Judge branch ghost.** The sandbox has master = origin = `tip` (`prepare`, `:233-242`). Ghost is chosen against `object_ids` and absent from heads and tags (`:502-512`). `create_ref(head_ref, tip)` (`:516`), `exact_refusal` (`:518`), cleanup in `finally` (`:519-520`).
- **Judge lightweight-tag ghost.** `create_ref(ghost_tag_ref, tip)` (`:521`), `exact_refusal` (`:523`), cleanup (`:524-525`).
- **Exactness of refusal.** `exact_refusal` (`:473-477`) requires exit 2, `binding_ids == [E-REVISION-INVALID]` and `finding_count == 1`.
- **Consumer error path (nine tools).** Each consumer converts `RevisionError` into one CANNOT finding with the binding id. Evidence: check-boot-chain `:1573-1584`; check-freshness-r17 `:773`, `:792-796`; check-section-citations `:913`, `:923-927`; check-root-dac-correction `:274-282`; check-recheck-commands `:747-750`, `:759-763`; check-seat-scope `:262-264`, `:663-665`; measure-update-recheck `:476-479`, `:769-772`; check-source-scope-correction `:639-641`, `:647-649`; check-locator-clarification `:784-788`, `:793-795`. Limit: the error-path structure was read in each file, but each `emit()` exit mapping was not re-read.
- **Sensitivity of binder fixtures.** A ref-first fallback (for example `_object_commit(...) or _commit(repo, revision)`) would return `tip` for the ghost, yield `("ok", None)`, and fail `:273` and `:276`.

## Findings (by severity)

### F1. Blocking. The judge's object-selector path raises `TypeError` before any ghost verdict is returned

- `check-revision-binding.py:393` defines `accepted(sandbox, name, rev, expect_sha)`, four parameters.
- `:479-480` defines `exact_accept(revision, expected_sha)`, which calls `accepted(sandbox, name, revision, expected_sha, branch)`, five arguments.
- First call on the path: `:594` (`cases["real_prefix_shadow_branch"] = exact_accept(shadow, tip)`). Same arity error at `:599`, `:608-609`, `:615-618`.
- The ghost probes (`:514-525`, `:527-540`, `:542-574`) run before `:594`, but `object_selector_probes` never reaches `return cases` (`:632`). Their results are discarded.
- Propagation: `measure()` has no handler around the tool loop (`:664-666`). `main()` catches generic exceptions (`:1114-1118`) and emits `CANNOT_EVALUATE` with `E-INTERNAL`, exit 2, zero object-selector tools. In `selftest()`, the object-selector check (`:1025`) is protected only by `except Cannot` (`:1086`). `main()` calls `return selftest()` (`:1106-1107`) with no handler, so `--selftest` exits 1 with a traceback.
- Certainty: deterministic by Python call semantics. Not observed. The build brief says "Add hermetic selftests but NEVER run them" (`.ufo/waves/round-20/build/dispatch.json:426`), so this is the first place the defect would surface.
- Falsifier: `check-revision-binding.py --tools-revision <landed hex> --object-selectors` (expected to produce E-INTERNAL, not 9/9); and `--selftest` (expected traceback).

### F2. High. The object-selector stub is lowercase-only, so the 9/9 selftest expectation cannot pass even after F1

- Stub `HEX = r"[0-9a-f]{%d,%d}"` (`:775`). Gate `if not re.fullmatch(HEX, rev)` (`:810-812`) runs before the object-selector branch (`:813`).
- `uppercase_object` is `exact_accept(tip.upper(), tip)` (`:615`). Every object-selector stub returns `E-REVISION-INVALID`, exit 2, so `accepted` reports `ok=False` (`:395-401`).
- `object_selector_ok` is the AND of all cases (`:668-669`), so the stub scores 0 of 9. The selftest expects 9 of 9 (`:1026-1030`).
- Contract mismatch: the real consumers accept uppercase (`_revision.py:41` and judge `:82`, both `[0-9a-fA-F]`), so the stub models a different contract from the one under test.
- Falsifier: the selftest itself, once F1 is fixed. Fix direction is `[0-9a-fA-F]` in the stub.

### F3. Medium. `exact_accept` adds `exit == PASS`, contradicting the predicate the oracle names

- `:479-482` sets `ok = accepted.ok and exit == 0`. `accepted` (`:393-401`) uses `code != CANNOT and json revision == expected`.
- `.ufo/waves/round-20/build/OracleC2.md:23-25` specifies "Exit other than 2 under the existing `accepted()` predicate" for the prefix-shadow and uppercase rows.
- Consequence: a consumer that binds the correct object but reports a content FAIL (exit 1) at the measured tip is counted as a C2 failure. Whether any of the nine exits 1 at the tip was not checked. [INFERENCE on impact]
- Falsifier: a consumer returning exit 1 with JSON `revision == tip` must count as accepted under the oracle; under `:481` it does not.

### F4. Low. The ghost refusal oracle does not check that the refusal carries no bound SHA

- `refused()` (`:383-390`) returns exit, finding, binding ids, count and ok. It never reads JSON `revision`. `exact_refusal` (`:473-477`) adds only the id and count checks.
- Oracle text: `.ufo/waves/round-20/build/OracleC1.md:35` ("exit 2, E-REVISION-INVALID, one refusal finding; no bound SHA") and `OracleC2.md:21` ("must not bind the branch target").
- Current state: by source reading of the nine consumers (list above), refusals print the raw selector, `None`, or a label such as `unbound` or `worktree`. No current violation was shown. The judge cannot detect one.
- Falsifier: a consumer that prints `revision: <tip>` alongside E-REVISION-INVALID passes `exact_refusal` today.

### F5. Medium. No red control: nothing proves object-selector grading fails a ref-aliasing consumer

- The object-selector selftest (`:1021-1031`) asserts only the all-pass `object-selector` stub.
- The only ref-aliasing stub is `unbound` (`:803-805`, plain `rev-parse rev^{commit}`). It is used for non-graded `check-extra.py` (`:1023`) and in discover-unbound (`:1014-1019`), never for the nine.
- The consistency grader has negative controls: `tip-only`, `no-origin`, `head-only`, `echo` (`:1033-1040`), and `legacy`, `double`, `extra-finding`, `require-origin` (`:970-973`).
- Falsifier: set one of the nine to `unbound` under `--object-selectors`. A correct grader gives `object_selector_tools == 8`, status FAIL, and `ghost_hex_branch.ok == False` and `ghost_hex_tag.ok == False`. No such assertion exists.

### F6. Medium. The judge's own `--tools-revision` binding has no ghost or abbreviated-hex fixture

- `bind()` (`:192-208`) is object-first (`:197`). `measure()` uses it at `:637` to pin the commit that all nine are measured at.
- Selftest bind cases (`:1043-1062`): `HEAD`, `@`, `refs/heads/master` (rejected by the regex at `:195`), `"0"*40` (no ref), branch-syntax cases, missing branch, absent repository, unlanded full SHA, not-pushed full SHA. None creates a same-named ref for an abbreviated selector, and none checks a 7 to 39 hex positive.
- By enumeration, reverting `bind()` to `rev_parse(repo, rev)` (`:130-136`, still in the file) would leave every selftest result unchanged. [INFERENCE by enumeration; not executed]
- Falsifier: in a fresh fixture, create `refs/heads/<12hex>` and `refs/tags/<12hex>` at tip, then assert `bind_error(fx, "<12hex>") == ID_INVALID`. Also assert `bind(fx, tip[:8]) == tip`.

### F7. Low. Ghost namespace coverage omits three of the six lookup rules

- Git's `<refname>` lookup order (`gitrevisions(7)`, SPECIFYING REVISIONS, items 1 to 6): `$GIT_DIR/<refname>`, `refs/<refname>`, `refs/tags/<refname>`, `refs/heads/<refname>`, `refs/remotes/<refname>`, `refs/remotes/<refname>/HEAD`.
- Binder ghosts cover heads (`_revision.py:272`) and tags (`:275`). Judge ghosts cover heads (`check-revision-binding.py:516`) and tags (`:521`). Full-length variants cover tags only (`:535`, `:549-552`).
- Current exposure: none shown, because the candidate never resolves the raw revision as a ref (`_revision.py:119`, judge `:141`). The gap is regression coverage. A future fallback to `refs/remotes/<g>`, `refs/<g>` or `refs/remotes/<g>/HEAD` would pass both fixtures.

### F8. Low. The ghost is always all-zero, so letter-bearing and uppercase ghosts are never exercised

- `_revision.py:270` and judge `:507` take the first candidate `"0"*12`. It is skipped only if an object begins with twelve zeros.
- Lowercasing (`_revision.py:119`, judge `:141`) is therefore never tested against a ghost spelled with letters. All-zero spelling makes case folding an identity.

### F9. Low. "No object matches" is asserted once, at construction

- `_revision.py:268-271` and judge `:502-510` take one inventory. Judge annotated tag objects are created afterwards (`:550-554`), and nothing re-checks the 12-hex precondition.
- Effect of a late collision: a single match would bind an object and fail the probe, so it is not a silent pass. The precondition is still not asserted at the point of refusal. Probability is negligible (about 2^-48 per object). Cheap to close with an explicit empty `--disambiguate` assertion before each refusal.

### F10. Low. Spec drift on ghost length. The candidate's 12-hex choice is the discriminating one

- `.ufo/waves/round-20/build/BindGhostBranch.md:7-9` specifies a lowercase 40-hex ghost branch. The candidate uses 12-hex for branch and tag (`_revision.py:270`, judge `:507`), and 40-hex only for tags (`_revision.py:278-308`, judge `:527-574`).
- `gitrevisions(7)` describes a full 40-byte hex as "the full SHA-1 object name", but does not state precedence against refs. Source-level understanding is that Git resolves full-length hex as an object ID before consulting refs (`get_oid_basic`). [INFERENCE from Git source; not in the local manual pages] If so, a 40-hex ghost branch would not discriminate against the baseline, and 12-hex is the correct choice.
- Action: record the deviation from BindGhostBranch.md in the round record.

### F11. Low (adjacent, judge). `lane_tip` resolves an unvalidated `--branch` as a ref expression on the CANNOT path

- `lane_tip` (`check-revision-binding.py:211-215`) calls `rev_parse(repo, f"refs/heads/{branch}")` (`:131` appends `^{commit}`). It does not call `validate_branch`.
- `main()` calls `lane_tip(ROOT, args.branch)` on the `Cannot` path (`:1111-1112`). That path is reached when `bind()` rejects the branch (`measure` `:637`, `validate_branch` `:194`).
- Example: `--branch 'master~1'` gives E-BRANCH-INVALID, and the CANNOT payload's `branch_tip` becomes the parent commit. Informational only; no gate verdict reads it. [by source; not executed]

### Stale evidence (info)

- `.ufo/waves/round-20/build/BindGhostBranch.md:15-17`, `BindGhostTag.md:12,14,18` and `ConnSourceLimits.md:78` describe the judge's `bind` as `rev_parse`-based at `check-revision-binding.py:130-176`. In the candidate, `bind()` is object-first (`:192-208`), and sandbox setup is at `:233-242`, not `:201-210`. Do not cite these as current evidence.

## Residual risk and verification gaps

- Nothing was executed. F1 and F2 are deterministic by source. F6 and the Git behaviour in F10 are inferences.
- The judge selftests were not run by design (`dispatch.json:426`). The first execution will expose F1.
- Candidate identity was not verified (no git). The `/tmp` worktrees were read as they stand.
- `lsp` unavailable. Grep is textual; dynamic imports or `getattr` access would not be seen.
- The 40-hex ghost branch, tag and annotated fixtures belong to other seats (BindGhost40Light, BindGhost40Annotated). They share F1, F2 and F4 and were not analysed here.
- Discovered tools are not graded by ghost probes (`:658`, `:664`). This includes `check-registry-coverage.py`, the C3 gate, which binds through `_revision` (`check-registry-coverage.py:17`, `:314`).

## Non-claims

- No host, package, boot or live-system safety is claimed. Boot images remain UNKNOWN; no clearance is given.
- Nothing was installed or updated. No tooling changes were made.

Scope: executed=none
