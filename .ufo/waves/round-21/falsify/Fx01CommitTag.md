# Fx01CommitTag · check-locator-clarification.py × annotated_tag_to_commit (falsify, source-only)

Reviewed-SHA256: cd24d07ce71e3a3c5cff92802b69f3b2630aa5942a437ad00e53469387b05814
Predicate: check-locator-clarification.py-annotated_tag_to_commit-candidate-control

Candidate revision 0a14952b59d20179e1c813af58befaecd6992a17. Primary receipt binds only the named primary file `candidate/tools/check-locator-clarification.py` (SHA256 above, per `candidate-files.json`). Auxiliary frozen snapshot dependencies read, not bound by this receipt: `candidate/tools/_revision.py` (06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf), `candidate/tools/check-revision-binding.py` (0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6), `candidate/corpus/lessons/round-21.md`, `candidate/SCORECARD.md`/`SKILL.md` (claim lines only). Build oracle compared: `.ufo/waves/round-21/build/Oracle01NestedTag.md` (closest same-consumer oracle; no Oracle01CommitTag exists in `build/`). No moving draft/production file used for any verdict.

## Axes

- **C1 depth** — does the consumer reach the tag's terminal commit through the shared binder, and is the accepted SHA attributable to that peel?
- **C2 operability** — does the new `--object-target-types` row actually observe this consumer on an independently created tag→commit object with full-SHA grading, fresh sandbox, unique prefix, no host read?
- **C3 calibration** — expected result fixed from source; mutant proposed, not executed.

## 1. Consumer propagation (frozen candidate source, observed by reading)

- `build_parser` :472–481: `--revision` mutually exclusive with `--selftest`; `--branch` default `master`.
- `main` :780–790: `args.revision`, `args.branch` pass verbatim to `_revision.bind(ROOT, args.revision, branch)` (:784). `ROOT = Path(__file__).resolve().parents[1]` (:23) → the sandbox clone, since the judge runs `sandbox/tools/<name>` (judge :362). `import _revision` (:19) resolves from the script dir, i.e. the sandbox worktree checked out at tip (judge `prepare` :234); `sys.dont_write_bytecode = True` (:18).
- Refusal path :785–788 + :793–795: `RevisionError` → informational `branch_tip` → `Cannot(fid, site, detail)` → one finding, exit 2, JSON `revision` = raw selector (:787).
- Accept path :789–790: `revision, tip = binding.sha, binding.branch_tip`; the four corpus files are read with `read_git(revision, path)` → `git show <sha>:<path>` (:459–469). Exit = `evaluate` code 0/1 (:800–804); exceptions collapse to CANNOT/2 (:796–798, :801–803), never a traceback exit 1.
- `payload`/`emit` :427–436: one JSON line, keys `branch, branch_tip, correction_count, findings, revision, status`.
- Consumer selftest `BINDING_WANTS`/`binding_cases` :555–656: branch/landing/push/git-failed rows plus one `main` refusal (`binding-main-single-id`); **no object-type or tag rows**, and no row checks `main`'s accepted `revision` field.

Binder (`_revision.py`): `bind` :172–192 — `validate_branch` → `REV` 7–64 hex → `_object_commit` :112–146 (`--disambiguate` exactly one object → `cat-file -t` → `tag` → `rev-parse --verify --quiet --end-of-options <oid>^{commit}`) → landed on `refs/heads/<branch>` → pushed when `refs/remotes/origin/<branch>` exists. Binder selftest already fixes this class: `annotated-tag-full-object-id` and `annotated-tag-object-prefix` expect `.sha == tip` (:360–361).

## 2. Source prediction for this row (not observed)

For selectors {full tag OID, unique tag prefix} of a fresh annotated tag whose target is the landed+pushed tip commit: exit 0 or 1 (corpus-dependent), never 2; JSON `revision` = tip full 40-hex lowercase; `branch` = `master`; `branch_tip` = tip. Matches Oracle01NestedTag §2 accept contract specialised to chain length 1; its consumer line citations (:771–804, :784, :427–436, :459–469, :555–570) agree with the frozen candidate line numbers I read.

## 3. Judge row `target_type_probes` (candidate `check-revision-binding.py`)

- **Independently created actual typed object** — `tag("commit", tip)` :697 runs `git tag -a r21-target-check-locator-clarification-commit -m commit <tip>` (:685–692, `tag.gpgSign=false`, fixed identity) and returns `rev-parse --verify <ref>^{tag}` (:694), so the selector is a real `tag` object ID created by the judge, not resolved by the binder under test. Target type is guaranteed by construction from `tip` (a commit), not separately asserted via `cat-file -p` — acceptable.
- **Accepted expected full commit SHA** — class `"annotated_tag_to_commit": (commit_tag, tip)` :703; `accepted()` :395–404 requires `exit != CANNOT` and `json_revision.lower() == tip.lower()`. `tip` comes from the judge's own independent `bind(lane, tools_rev)` (:742 → `object_commit` :139–166 returns the full OID), so a short/echoed SHA cannot pass. Exact refusal ID/count is not applicable to this accept class.
- **Unique prefix sanity** — :711–718: width 7..39, unique across the post-creation `cat-file --batch-all-objects` inventory (:705–707, which includes dangling tag objects from earlier tools, consistent with `--disambiguate`'s universe), no `refs/heads/<p>`/`refs/tags/<p>` collision, else `Cannot E-SANDBOX`. Both selectors observed; `ok = all(rows)` :730–732.
- **Fresh sandbox** — `target_type_measure` :743–746: `TemporaryDirectory` + `clone_lane --no-tags` + `prepare` (detached tip, `refs/heads/master` = tip, origin remote removed, `refs/remotes/origin/master` = tip). One sandbox per measure call, shared sequentially by the nine tools; per-tool tag names are distinct and refs are deleted in `finally` (:734–736). Tag objects stay dangling but cannot affect a full-OID selector and are counted in the prefix inventory.
- **No host read (judge/row side)** — row commands all target the sandbox; `run_tool` uses `cwd=sandbox`, `clean_env()` (GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null). The lane is only read by orchestration (`bind`, `clone_lane`, `lane_tip`), not by the row.
- **Limit (consumer side, observed in source)**: the consumer's own `git()` :447–449 rebuilds env as `os.environ` minus every `GIT_*` key, which **drops the judge's GIT_CONFIG_GLOBAL/GIT_CONFIG_NOSYSTEM**; the accept path's four `read_git` calls therefore read host `~/.gitconfig`/system git config ([INFERENCE] from Git's default config search; not executed). `_revision._git` keeps isolation (:62–66). Impact is false-red risk (a hostile host config could make `git show` fail → exit 2), not false-green; outside the target-type predicate but contrary to a strict "no host read" reading of the accept observation.
- **Old matrix unchanged / continuity** — this class duplicates the round-20 `object_selector_probes` rows `annotated_tag_object` / `annotated_tag_prefix` (:631–632) and `full_tag_object_id_ref_shadow` (:616–626), all single-level tag→tip. It is continuity, **not new coverage**. `object_selector_probes` still spans :475–673, the same range Oracle01NestedTag cites for the pinned round-20 judge (line-range concordance only, not byte equality). `--object-target-types` and `--object-selectors` are mutually exclusive (:1391–1395); `target_type_measure` never calls `probe_tool` or `object_selector_probes`.
- **C2 framing** — `target_type_mode = int(available)` is a finite AST census (:750–759); `behavioral_tools` is reported separately (:774); SCORECARD :648 already supersedes the 0→9 headline. Mode 0→1 is one availability flip, not ninefold behavioral uplift.

## 4. Concrete false-green (proposed mutant, NOT executed)

**Defect within this predicate: the row's expected commit is the branch tip, so it cannot attribute an accepted SHA to the tag's peeled target.** `commit_tag` targets `tip` (:697) and `refs/heads/master` = `refs/remotes/origin/master` = `tip` (`prepare` :234–241), so expected commit ≡ branch tip ≡ JSON `branch_tip`.

**Mutant M-TipSub** (check-locator-clarification.py :789):
`revision, tip = binding.sha, binding.branch_tip` → `revision, tip = binding.branch_tip, binding.branch_tip`

Source predictions:
- `annotated_tag_to_commit`, both selectors: binder still validates and binds; consumer emits `revision = tip` → `accepted` ok → **row green**.
- `nested_tag_to_commit` (expected tip): green. `nonempty_tree`, `tag_to_blob`, `tag_to_tree`: refusal comes from the untouched `bind` → `E-REVISION-INVALID`, single finding → green. So `behavior_ok` = True and `target_type_tools` stays 9/9 under `--object-target-types` — **false-green for the whole new matrix**.
- `object_selector_probes`: every `exact_accept` expects `tip` (:608, :613, :622, :629–632) → survives. Consumer selftest: no accepted-`revision` row → survives. Existing stubs `tip-only`/`unbound`/`head-only` (:957–973) also pass this row in isolation; nothing in the selftest witnesses that this row can fail.
- Killed only by the default `measure` path's `probe_tool` `landed-parent` (`accepted(parent, parent)` :427), and only when the measured tip has a first parent (:799). That is old-matrix continuity, not this control.

Severity: low for the unchanged shared binder (the mutant is a consumer-side wiring error, which the old default matrix catches), but the predicate as written over-claims: "accepted expected full commit SHA" is not discriminating when that SHA equals the branch tip. Minimal remedy (proposal only): create the commit tag on a landed, pushed non-tip commit (e.g. `tip^1`, already required as the decoy in `object_selector_probes` :477–479) and expect that commit, so `revision` must differ from `branch_tip`; add a selftest stub that emits `branch_tip` and assert this row fails.

Mutants checked and found **not** defects within this predicate: generic `^{}` peel for tags (correct for a commit target; killed by `tag_to_tree`/`tag_to_blob`, selftest :1239–1250); selector echo (revision = tag OID ≠ tip → fail); ref-alias `rev^{commit}` (passes this row but fails refusal rows and old `ghost_*` rows); one-level peel (identical to recursive for chain length 1; nested row's concern).

## 5. Observations / inferences / limits

- **Observed (source reading)**: all line citations above in the frozen candidate snapshots; Oracle01NestedTag content.
- **[INFERENCE]**: Git default config search when GIT_CONFIG_GLOBAL is unset; `git tag -a <name> <sha>` creates a tag object of type commit; M-TipSub outcomes above are source predictions.
- **Limits**: nothing executed; no candidate output observed; receipt binds declared primary bytes only and does not prove reading. Not outside closure; no promotion claimed. No tool installed or updated (NO-EXEC seat; none needed).

Scope: executed=none
