# Round 12 C1 mutation proof — strategy only

Axes: **operability** (the package census actually publishes selected-root metadata and distinguishes owner-write absence) and **depth** (the detector distinguishes a missing probe, reversed write-bit decision, unavailable metadata, and an ignored root override).

## Scope and present-source recheck

This is a parent-run strategy for the post-integration C1 census, not a mutation result. The task explicitly prohibits tests/mutants mid-flight. I did not edit the census, create a mutation snapshot, or run `--selftest`.

Current `tools/tsukuroi-census.sh` SHA-256 is `1045244387ffcd5d3db481dd0d3d30e34097abc24744d954e791b81d28b20c11` (read-only `sha256sum`, exit 0). A targeted source search for `TSUKUROI_ROOT_DIR|root_mode|root_uid|root_gid|owner_write|owner_search` returned **No matches found**. This matches the inherited pre-C1 state recorded in `CensusScribe.md:8-9`; rechecking the bytes now confirms that the integrated mutation anchors do not yet exist. No output from the inherited plan is treated as a new run.

Relevant present-source anchors:

- `.ufo/waves/round-12/spec.json:20` asks for `TSUKUROI_ROOT_DIR` (default `/`), directory validation, actual `root_mode=`, `root_uid=`, `root_gid=` in the packages note, degradation for absent owner write/search, and blocking on unavailable/non-directory metadata. It also requires the root result before package-arm early returns and fixture override coverage.
- `tools/tsukuroi-census.sh:326-353` has no root override yet; `probe_packages()` begins at `:530` and returns early for missing pacman, lock, and local-db errors at `:534-550`.
- The existing selftest seam is `run_selftest()` / `check()` at `:1570-1809`. `fx_default()` creates a fresh passing fixture (`:1662-1746`); `check()` validates exit, rollup, evidence regexes and a fixture-tree hash. Each case is initialized around `:1835-1864`.
- Existing update-safety code calls `stat` for repository/offline-db stamps at `:1336`, `:1341`, `:1415-1416`; any test shim must delegate those unrelated calls.
- `fx_hash()` at `:1748` hashes regular-file contents only. It does not prove fixture directory modes/ownership were unchanged.
- `corpus/QUALITY.md:15-17` requires reporting owner-write/search bits rather than a universal mode policy or process writability, and distinguishes permission layers. This mutation plan does not infer a default `0755` policy.

## Reusable, rejected, and corrected inherited material

- Reuse the four M1–M4 defect ideas and the pristine/mutated/restored protocol in `.ufo/waves/round-12/MutationPlan.md:13-19,21-39` as design only. The inherited file itself labels its runs unrun; its output, hashes and verdicts remain unmeasured.
- Reuse `CensusScribe.md`'s starting-source identity and `FixtureReview.md:18-33,84-107`'s cautions about test seams, content-only fixture hashing, and permission-based cleanup, as historical architecture notes. They are not post-integration verification.
- **Correct the inherited `0744` owner-search case:** `0744` gives the owner all three bits (`rwx`); it does not isolate missing owner search. It must not be used as evidence for an owner-search branch. If that branch is retained as extra coverage, `0655` has owner `rw-` and group/other `r-x`, but the owner running `find "$FX"` cannot traverse it. The integrated selftest must place it outside the hashed tree or account for traversal and restore permissions before cleanup. That extra branch is not needed to kill the four mutants below.
- Strengthen M1 with a non-default positive fixture mode as well as the required `0755`/`0555` pair: e.g. assert a fixture deliberately set to `0751` reports `root_mode=751` and its fixture UID/GID. This guards against a missing probe masked by copied/default field values; it does not declare `0751` the host default.

## Parent's bounded protocol

After C1 is integrated, operate only on a disposable isolated snapshot, never the repository's shipping file. Pin the pristine snapshot SHA-256. Run the same detector on pristine bytes, each single-defect mutant made from a fresh pristine copy, and restored pristine bytes:

`bash <snapshot>/tools/tsukuroi-census.sh --selftest`

Record complete detector output and exit status plus SHA-256 for pristine, each mutant, and restored bytes. Capture the restored hash even if a detector fails; it must equal the pinned pristine hash. Only call a mutant **KILLED** when pristine and restored controls pass and the owning assertion fails in the mutant; green mutant = **SURVIVED**; red control or a case that does not reach the mutated branch = **INCONCLUSIVE**. A selftest case should assert the `PLANE packages:` evidence and rollup/exit rather than relying on a helper return or root token count alone. Do not compare with live `/` metadata.

## Four single-defect probes

Use fresh `fx_default` fixtures so other planes are passing and the root case owns the expected rollup. Have the integrated `check()` inject the selected root path for every test invocation. Assert exact observed fields from each fixture (mode as emitted by the integrated `%a` formatting, plus the fixture's UID/GID), the package verdict, final rollup and exit. Keep landed evidence spelling/reason strings as the assertion source; do not invent them from this plan.

| Mutant | One behavior-bearing mutation in the integrated snapshot | Required discriminator / expected mutant failure |
|---|---|---|
| **M1 — omit the root probe** | Remove/skip only the metadata `stat`/probe (or make its result unused), leaving the surrounding packages arm intact. | The positive fixture must assert its exact `root_mode`, `root_uid`, and `root_gid` in the packages line. Include the non-default `0751` sentinel plus the `0755`/`0555` fixtures so a hard-coded field cannot pass by coincidence. The root metadata assertion must fail if the probe is absent; mode-only generic presence is insufficient. |
| **M2 — invert owner-write decision** | Reverse only the owner-write predicate; leave root path selection, owner-search handling, `stat` errors and formatting unchanged. | Pair `0755` (owner write present; packages healthy, overall exit 0 on the clean fixture) with `0555` (owner write absent, owner search present; packages degraded, overall exit 1). The inverted decision must fail at least one exact package verdict/rollup assertion. Assert the observed mode as well so a wrong verdict cannot be confused with the wrong fixture. |
| **M3 — ignore unknown metadata** | Change only the metadata-stat failure arm so it no longer sets the required blocked verdict/named unknown. | Use an existing, ordinary fixture directory that passes any preliminary directory check; force only the selected root-metadata `stat` invocation to fail. Require packages and rollup `BLOCKED`, exit 2, and the integrated named unavailable-metadata reason. A missing path/non-directory is not a substitute: an earlier validation arm can block before the stat-failure behavior is exercised. If there is no narrow stat-command seam, use a temporary PATH shim after inspecting the integrated invocation. It must fail only for the exact fixture-root argument, delegate all other `stat` calls (including existing update-safety calls), and leave fixture validation successful. Do not use `chmod 000` as the unreadability mechanism; privilege/capability differences make that nondeterministic. |
| **M4 — hardcode host `/`** | Change only the root metadata probe's path operand from the selected override to literal `/`, keeping the rest of the arm intact. | Use a non-default fixture override (e.g. `0751`) and require exact fixture metadata and its healthy package result. A narrowly scoped stat shim must reject the literal `/` argument without calling real `stat /`; the mutant then cannot silently pass when live-root metadata happens to resemble fixture values. The shim delegates every non-root argument. If the integrated code performs other path checks, inspect the exact call path before choosing the mutation so the case tests the metadata-probe override rather than unrelated validation. Do not use the live root's mode/UID/GID as the expected value. |

M3/M4 shim mechanics are conditional on the integrated code's actual command resolution: prefer a landed dedicated stat seam if one exists; otherwise use PATH interception only if the probe resolves `stat` through PATH. Keep the wrapper outside the snapshot, fail/reject only the exact target argument, and delegate all other arguments to the resolved real `stat`. If the probe uses an absolute stat path, do not claim a PATH shim would reach it; adapt to the observed integration before running. The current script already has unrelated `stat` calls, so a blanket failure would invalidate the control rather than test C1.

## Risks and actual status

- **No tests or mutants were run here** per the task. `--selftest` output/exit, mutant output/exit, per-mutant verdicts, and mutant/restored hashes are all **unrun/unmeasured**. There is no PASS, kill, survival, or restoration claim.
- The one shell command run by this seat was `sha256sum tsukuroi-shokunin/tools/tsukuroi-census.sh` (exit 0; output recorded above). The targeted source search was the specialized read/search tool and returned “No matches found”; it exposed no process exit code. No installs or updates.
- Because the current source is still the pre-C1 snapshot, exact final mutation anchors, field regexes, case labels, failure reason, stat path resolution, and detector output must be rebound to the integrated bytes before parent execution. This file is strategy, not independent non-author verification.
