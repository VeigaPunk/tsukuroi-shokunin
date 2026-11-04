# ReviewArithmetic — round 77 / w1

Axes: **depth (8, lowest tied)** and **freshness (9)**. Recommendation only; no admission, integration or score uplift.

## Findings, in severity order

**No actionable defect found in the scoped frozen arithmetic claim or the reviewed companion draft.** All six vectors HOLD as finite hypothetical inputs. No false C1 source-interpretation/companion conjunct was identified that triggers the frozen kill rule. This is not a finding that every unrelated declaration assertion or C2 correction is established.

**Historical false literal, correctly targeted by the proposal:** `corpus/SOURCES.md:331`, S320, says the limit uses “the smaller of free space and keep_free.” That is false: pinned `journald-manager.c:168` calls LESS_BY, whose strict comparison/subtraction is at pinned `macro.h:320–326`, especially :325. For A1, minimum would give avail=100, limit=200, available=100; actual source gives 900,1000,900. Reject that old interpretation, not the new frozen C1 claim. Current proposed S325 (`corpus/SOURCES.md:336`) explicitly supersedes S320 and states the three correct operations. The scoped registry diff against base 06f1bbbb803790b35358d277bb7807b82a9fab99 adds S324/S325/S326 without rewriting S320. S325's `patch_min_use` statement is bounded by :185: it never lowers an already higher floor; it is not a guarantee that the final limit exceeds current usage or that vacuum cannot shrink usage.

## Pinned evidence and independent operations

Frozen declaration reviewed from commit `eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5`, SCORECARD addition beginning at :6379. Frozen inputs read from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/before/expected.json`. Sources are the complete frozen snapshots under the same `before/src/` directory, not the counter's expected outputs:

- macro.h SHA-256 `1bd38a180b2cccacf0732e3e5b6388ac3d71e453839236c388501080a11a75b8`.
- journald-manager.c SHA-256 `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`.

Both independently computed digests match `before/src/SHA256SUMS` and expected.json. Upstream source name is `src/fundamental/macro.h`; snapshot basename macro.h is not another upstream path.

Source-transcribed evaluation, independently implemented without importing or running the frozen counter:

1. :168: `a = free > keep_free ? free - keep_free : 0`.
2. :170 and macro.h:338–349: `x = used + a`; `limit = x > max_use ? max_use : x < min_use ? min_use : x`.
3. :171: `available = limit > used ? limit - used : 0`.

All supplied values are nonnegative small uint64 values, `min_use <= max_use`, and every sum is at most 1000. No wrapping addition occurs. Mathematical `max(free-keep_free,0)` describes saturation; literal unsigned subtraction before max would instead wrap, so it is not a safe replacement C expression. For these ordered bounds CLAMP also equals `min(max(x,min_use),max_use)`; it is not merely `min(x,max_use)`, as A5 demonstrates.

| Vector | Inputs (used, free, keep_free, min_use, max_use) | avail | sum | limit | available | Verdict and source branch |
|---|---|---:|---:|---:|---:|---|
| A1 | 100,1000,100,0,2000 | 900 | 1000 | 1000 | 900 | HOLD; subtraction, in-range clamp, subtraction |
| A2 | 100,50,100,0,2000 | 0 | 100 | 100 | 0 | HOLD; below keep_free saturates, final equality saturates |
| A3 | 100,100,100,0,2000 | 0 | 100 | 100 | 0 | HOLD; equality uses zero, not subtraction/wrap |
| A4 | 100,1000,100,0,500 | 900 | 1000 | 500 | 400 | HOLD; upper branch caps sum |
| A5 | 100,50,100,300,2000 | 0 | 100 | 300 | 200 | HOLD; lower branch raises sum despite zero avail |
| A6 | 700,50,100,0,500 | 0 | 700 | 500 | 0 | HOLD; upper branch; limit below used saturates final allowance |

Every input and all three output fields match the frozen tuple; independent command exited 0. A5/A6 would still have the same final limit/available under some wrong minimum interpretations, but their intermediate avail would differ. Reviewing all output fields therefore matters.

## High-first and startup reachability

High is tested **before** low (`macro.h:344–349`). With ordered bounds this does not introduce a conflict. With inverted bounds there is no valid general “between both bounds” interpretation. For example x=100, low=700, high=500 selects low=700, whereas `min(max(x,low),high)` gives 500. Such inputs are outside the declared exercise domain.

A6 is HOLD for arithmetic, **not proof of startup-state reachability**. `journald-manager.c:176–186`, especially :185, assigns `min_use = MAX(min_use, space.vfs_used)`. Starting with the A6 numbers and observed used=700 raises min_use from 0 to 700. Keeping max_use=500 yields inverted bounds, not the frozen A6 input. For x=700,low=700,high=500 the actual high-first macro nevertheless returns 500. The floor alone therefore cannot prove the limit is at least usage. Startup/open callers refresh then patch at :383–386 and :450–453; refresh errors are ignored there, so the patch uses the stored space value, not necessarily a fresh observation. Additional patch callers occur after full rotation at :1662–1668. None of this establishes complete metrics normalization or a live reachable A6 state.

The same caution applies to all vectors: `used` is journal-file block accounting (`journald-manager.c:119–136`), not total filesystem occupation; free is f_bsize*f_bavail (:115). Hypothetical byte inputs need not be realized filesystem observations. Refresh may return 0 from the timestamp cache (:158–159) or return an acquisition error (:161–163) before evaluating/updating these quantities. No allocation success, actual writes, deletion amount, vacuum behavior or host-state inference follows from the six examples.

## Literal and draft review

Read-only draft reviewed: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/w1/ScribeNote/note.md` and `data.json`.

- note.md:9–14 accurately identifies pinned paths, digests, line ranges and the three manager quotes; macro expression really is at snapshot :325, not :320 (which names the public macro).
- :18–26 correctly distinguishes local avail from final available, describes high-first CLAMP, orders the bounds and disclaims arbitrary uint64 overflow safety.
- :34–46 contains all six correct input/output rows and matching explanations. A5's 200 allowance is not a claim that 200 bytes physically exist or can be allocated.
- :48–52 explicitly disclaims reachable startup-normalized A6, universal arithmetic oracles and live manager observations. Its hypothetical min_use=700 example is accurate. No false companion literal found.
- data.json:6–11 has the six exact objects and source list S324/S325. Additional top-level metadata is present; the frozen instrument checks the row objects and source list, not exclusive top-level keys.

The frozen declaration's quoted :168/:170/:171/:325 literals, high-first description, finite-example boundary and intended S320 supersession HOLD. The instrument (`evaluate`, lines 41–52) compares source IDs, snapshot digests and six typed row objects; it does not execute source, read the companion, or establish source-reading effort. The declaration explicitly says reviewer interpretation is separate, so a matching counter result is not substituted for this review. C1 mechanical comparison is independent of C2's lesson path; C2 text semantics, historical registry/collision counts and process chronology are outside this arithmetic seat's verification, not silently certified.

## Commands, exits and limits

- `sha256sum` on both absolute pinned source paths: exit 0; digests above.
- Read-only `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -t eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5`: commit. An initial fleet-root object query failed; project query succeeded.
- Read-only `git show` for the frozen declaration and instrument: exit 0. An instrument copy was held only in owned scratch.
- `env TMPDIR=/fast/scratch/hyaku/tsukuroi-r77/ReviewArithmetic/tmp python3 -c ...`: source-transcribed conditional subtraction/high-first clamp recomputation of all six inputs, comparing all output fields; exit 0. Output: A1 (900,1000,900), A2 (0,100,0), A3 (0,100,0), A4 (900,500,400), A5 (0,300,200), A6 (0,500,0), all HOLD. No counter import or answer-key-as-source inference.
- Read-only `git diff 06f1bbbb803790b35358d277bb7807b82a9fab99 -- corpus/SOURCES.md`: exit 0; actual correction reviewed above.
- LSP prerequisite attempted via `read xd://lsp`: no such mounted tool. Status/references/definition/diagnostics unavailable. Text searches only located definitions/callers; they are not semantic reference-completeness proof.
- Initial source-hash command could not start because scratch cwd was absent; created owned scratch then succeeded. Initial digest-manifest read used the parent directory; corrected to before/src/SHA256SUMS. No tool installation/update occurred.
- Owned scratch `/fast/scratch/hyaku/tsukuroi-r77/ReviewArithmetic` deleted with `rm -rf --` (exit 0) before final report. No production writes, git mutations, service operations, raw journal reads or delegated work.

Residual risk: this is read-only source/draft review, not final committed artifact admission. No C1 counter, full manager executable, compiler probe or host check was run by this seat; such checks were not substituted for the required independent arithmetic. Resume/rerouting/saturation runtime claims are not changed by these corpus proposals and are not certified here.

Self-evaluation: accuracy 4 (source and arithmetic checked; no full lifecycle execution), completeness 4 (all assigned vectors/literals reviewed; final integration not owned), clarity 4 (separates arithmetic/state), actionability 4 (source-bound recommendation; final closure operator-held), conciseness 4 (detailed command and boundary receipts retained). Overall 4.0. Improvement priority: final reviewer should apply this literal review to the integrated companion/source rows, without broadening the frozen predicates. User agreement is expected on scoped arithmetic, not inferred for admission.
