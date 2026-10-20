# Round 12 C1 mutation plan — unrun

Axes: **operability** (root metadata must affect the census) and **depth** (the detector must distinguish the contract branches, not merely print a plausible field).

## Scope and current evidence

This is a strategy for the parent to execute against the **post-integration** census in a disposable snapshot. Per assignment, I did not run the detector or any mutant and did not edit `tools/tsukuroi-census.sh`.

The round-12 Census task contract is in `.ufo/waves/round-12/spec.json:19-24`: `TSUKUROI_ROOT_DIR` defaults to `/`; the selected path is validated; packages output carries `root_mode=`, `root_uid=`, `root_gid=`; absent owner write/search degrades; unreadable metadata or a non-directory blocks; fixture paths are overridden. At inspection, the source was still the pre-C1 2,403-line snapshot: `tools/tsukuroi-census.sh` had no `TSUKUROI_ROOT_DIR`, `root_mode`, `root_uid`, `root_gid`, `owner_write`, or `owner_search` symbols (`grep` result: `No matches found`). Therefore no final root-probe line or mutant patch anchor exists yet; re-read and pin the integrated bytes before crafting each one-line mutation.

Useful pre-integration selftest seams: `tools/tsukuroi-census.sh:1570-1808` builds fixtures and its `check` helper asserts exit, rollup, evidence regexes, and fixture-tree hash stability; `:2338-2403` dispatches `--selftest` and live mode. The package plane currently has early returns at `:534-550`; verify the integrated probe's stated placement before selecting any mutation site. These source line numbers are pre-integration anchors only.

## Parent's bounded protocol

1. After integration, save the exact census bytes and SHA-256, then make an isolated disposable snapshot. Run only `bash <snapshot>/tools/tsukuroi-census.sh --selftest` on the pristine bytes. Record complete stdout/stderr, exit, and hash. A red pristine run makes every mutant result **inconclusive**.
2. For each row below, start from a fresh copy of those exact pristine bytes, apply only that defect, run the same command, capture complete output/exit and mutant hash, then restore the disposable target from the pristine copy even if the detector fails. Run the same detector on restored bytes and record restored SHA-256 plus its output/exit. Do not use the live census, host `/` as an oracle, or the repository file as the mutation target.
3. Adjudicate a mutant `KILLED` only if pristine/restored runs are green and the mutant causes its owning assertion to fail. If it runs green, record `SURVIVED`; if the pristine/restored control fails or the mutation does not reach its owning case, record `INCONCLUSIVE`. Record per-mutant outputs and hashes; do not report a kill-rate as global proof.

Expected control shapes (not observed): pristine and restored selftests exit 0 with `TSUKUROI_CENSUS_SELFTEST: PASS (...)`; a killed single mutant makes its owning case fail and the selftest exit 1. Case count and exact output remain to be measured after integration.

## Four single-defect probes

Use one fixture set with the root override exercised by the selftest. A `0755` directory is a positive permission control, **not** a required default policy. Its expected metadata values should be taken from that fixture (`stat -c '%a %u %g' "$fixture_root"`), not from host `/`. Add/retain the `0555` case to isolate missing owner write while owner search remains; use `0744` to isolate missing owner search while owner write remains. Assert the packages verdict and the rollup/exit (`HEALTHY`/0 for the valid `0755` control; `DEGRADED`/1 for the isolated missing-bit cases), along with the observed root metadata and the exact landed named reason.

| Mutant | Smallest behavior-bearing defect in the integrated source | Owning detector and required outcome |
|---|---|---|
| **M1 — missing probe** | Skip the one root metadata `stat`/probe (leave the surrounding packages path intact). | The valid `0755` fixture must assert actual `root_mode=755`, `root_uid=<fixture uid>`, and `root_gid=<fixture gid>` in the packages note, not merely that some `root_*` token exists. The 0555/0744 cases must also demonstrate their respective named permission findings. Expected mutant result: at least the metadata assertion fails; otherwise the probe is not actually required by the suite. |
| **M2 — inverted owner-write bit** | Reverse only the owner-write-bit predicate, leaving owner-search and error handling untouched. | Run the paired `0755` (owner write present) and `0555` (owner write absent, search present) fixtures. The contract expects the first to stay non-degraded and the second to be `DEGRADED`; the reversed predicate must fail one or both owning assertions. The separate 0744 case prevents accidentally conflating write with search. |
| **M3 — ignore unknown metadata** | Make the root-stat failure arm fall through without the required `BLOCKED` verdict/named unknown. | Use an **existing fixture directory** but force only its metadata `stat` invocation to return nonzero; require `packages=BLOCKED`, overall `BLOCKED`, exit 2, and the integrated named root-metadata-unavailable evidence. A missing path or non-directory alone is not sufficient to kill this mutant: an earlier `-d` validation can block before the stat-failure branch is reached. If the integrated selftest has no way to force a stat failure after directory validation succeeds, add a narrowly scoped `stat` shim for this case (fail only for the selected fixture-root argument; delegate all other stat calls to the resolved real binary) before claiming this mutant tested. |
| **M4 — hardcoded host root** | Replace the env-selected root path with literal `/` so `TSUKUROI_ROOT_DIR` is ignored. | Test both exact fixture metadata on the valid `0755`/`0555` roots and a root override pointing at an ordinary file, which must be `BLOCKED` as non-directory. For a hermetic, decisive path test, use a scoped `stat` shim that delegates the fixture-root call but rejects an unexpected `/` argument; this catches the path substitution without reading host-root metadata or assuming its mode. A valid fixture's computed mode/uid/gid must be asserted exactly. |

Suggested distinct labels, if the integrated labels do not already express these clauses: `healthy: root metadata from fixture`, `degraded: root owner write missing`, `degraded: root owner search missing`, `blocked: root stat unreadable`, and `blocked: root metadata non-directory`. Keep each case consumer-visible: check the packages line and rollup/exit, not a helper return value alone.

## Risks / limits

- Do **not** treat `chmod 000` as a reliable unreadable-stat fixture: privilege/capability differences (especially root-run selftests) can make that path readable. A deliberate stat failure on an existing directory isolates the unknown branch deterministically.
- A missing path can establish fail-closed handling of an unavailable root, but may not exercise the metadata-command error branch; do not count it as M3 evidence without checking control flow.
- The hardcoded-root probe must not compare against a live `/` value. A stat shim which rejects `/` avoids making host mode part of the detector and makes this mutant observable even when host and fixture modes happen to coincide.
- If the final implementation changes its evidence spelling, adapt assertions to the integrated contract; do not invent output strings or pin pre-integration line numbers.

## Actual run / verdict

Detector command: `bash tools/tsukuroi-census.sh --selftest` — **unrun by this seat as explicitly required**; output and exit code: **unrun**. M1–M4 mutations: **unrun**; actual verdicts: **INCONCLUSIVE / no kill or survival claim**. Mutant and restored SHA-256 values: **unmeasured**. No census source bytes or mutation scratch copy were changed by this seat, so there is no restoration result to claim. The parent should fill in those measured fields only after the post-integration disposable-snapshot run.