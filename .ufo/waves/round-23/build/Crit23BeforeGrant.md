# Crit23BeforeGrant — round 23 attempt 1, pre-grant critique of preregister.json

Seat: TsukuroiR23-2.Crit23BeforeGrant-7 (critic, leaf). NO-EXEC, NO-FETCH. No installs, no commands, no hashing.
Inputs read: preregister.json, sources/godspeed-directive.txt (used in place of skill://godspeed, which the read tool here cannot resolve), sources/r22-closure.json, sources/structured-edit-observations.json. The bound draft path build/Crit23BeforeGrant.md did not exist before this write, so it is the output only.

## Verdict

The preregistration has three fixable binding defects and one internal policy contradiction that comes straight from the round-22 source data. None of them need the judge to reject the round. All of them must be fixed before grant: once seats act on the grant, any later fix is retrospective. The strongest falsifier is F1.

## Axes

- C1 depth (`validated_edit_decisions`, 0 → 8)
- C2 operability (`structured_edit_mode`, 0 → 1)
- C3 calibration (`unexplained_cohorts`, 2 → 0)
- Cross-cutting: byte identity, predicate/placeholder binding, slot event ordering, separability (one authority per rule)

## Findings

### F1 — `:raw` read-selector contradiction between DECLARED_EDIT, EDIT_TRAVERSAL and EXPANSION (C1, C2, C3; fixable, strongest)

Counterexample from source data. In structured-edit-observations.json, CritRuntime's `edit` (call `toolu_014nToY7USd3cckcqeieNJ4o`, request line 15) has the exact target `.../round-22/build/CritRuntime.md`. The adapter recorded two starts for it: `read` of `.../CritRuntime.md:raw` (line 12), then `write` of `.../CritRuntime.md` (line 13).

Applied as preregistered, the rows give contradictory results:
- DECLARED_EDIT → ALLOW, because the exact target is in the read, write and edit lists.
- EXPANSION → CHECK_EACH, so the recorded `read` of `CritRuntime.md:raw` is scoped separately.
- EDIT_TRAVERSAL → DENY, because "no ... alternate spelling expands the target list". `CritRuntime.md:raw` is a different spelling of the declared target and does not match it exactly.

So a fully declared stream-content edit is ALLOWed at the request and DENYed on its own adapter read. The preregister contains no selector-normalization rule (`:raw`, `:N-M`) that breaks the tie. Each checker would have to pick a normalization after seeing the data. That is unregistered analyst freedom on exactly the dimension being measured.

Duplicate authority. r22-closure.json `verification.rechecks` puts the rough-versus-lane gap (25/33 against 23/29) down to "selector-normalization differences". C3 reconciles that gap. C1 and C2 need the same normalization function to decide F1's case. The `separability` field says C3 "never reads new C1/C2 production content", but the normalization rule is shared logic. If C1/C2 and C3 each define it, there are two authorities for one fact, and they can disagree without any checker noticing.

Smallest safe correction: before grant, preregister one selector-normalization rule, in a single place, that C1, C2 and C3 all cite. For example: strip a trailing `:raw` or `:<int>-<int>` selector before exact comparison; any other suffix → UNKNOWN. Add F1's call as a fixture whose expected outcome is ALLOW for both the request and each recorded start.

### F2 — The C1 count of 8 is self-fulfilling and only partly source-grounded (C1 depth; fixable)

- `edit_decisions` holds exactly eight rows, and the target is 8. A checker that counts or copies these rows reaches the target from the preregister itself. That is premature saturation.
- `EXPANSION → CHECK_EACH` is a rule for iterating over recorded starts, not an ALLOW/DENY/UNKNOWN authority decision. Counting it as one of eight "authority decisions" inflates depth.
- C1 is scoped as "source-grounded", but the S086 observations only show edits to exact declared report paths (via `path` + `stream_content` or `old_string`/`new_string`) and their adapter expansions. They contain no opaque patch, traversal, external URI, read-only edit or write-only edit, so at least 5 of the 8 rows (READ_ONLY_EDIT, WRITE_ONLY_EDIT, OPAQUE_PATCH, EDIT_TRAVERSAL, EDIT_EXTERNAL) have no observed basis. The r22 internal-URI finding was a read, not an edit.

Smallest safe correction: label each row `observed` (citing transcript_sha256 and call_id) or `synthetic` (citing a fixture). Require each decision to have a mutant that flips its outcome and makes the checker fail. Either reclassify EXPANSION as a procedure rule and lower the target to 7, or state why it counts as a decision.

### F3 — Unbound placeholders and a predicate with no preregistered source (C1–C3 and receipt binding; fixable)

- All three commands use `<REV>`, and C2 also uses `<WAVE>` (`.ufo/waves/round-23/<WAVE>/bindings.json` and `events.json`). Nothing fixes the wave set or the revision choice in advance. A checker could run against whichever wave or revision is green. The same setup in r22 produced "violations41/46" across two waves, so the wave choice changes the outcome.
- The preregister has no seat or predicate registry. This seat's predicate is defined only in the assignment text. A predicate absent from the preregistered bytes cannot be checked against them.
- There is no `attempt` field. An attempt-2 run reusing these bytes would accept attempt-1 receipts as replays.

Smallest safe correction: an addendum, committed before grant, that lists the exact wave values (for example `build` and `falsify`), defines `<REV>` as the single landed L1 integration commit, adds `"attempt": 1`, and lists the seat predicates.

### F4 — The reported digest is supplied, not observed, and the sources are not byte-pinned (byte binding; fixable)

- This seat's digest receipt repeats the declared SHA256 8f3f33ea…e8. It was not computed from the bytes read. Under NO-EXEC it cannot be. The receipt therefore shows that a digest was supplied, not which bytes were reviewed. Counterexample: preregister.json changes in the worktree between declaration and read (a time-of-check/time-of-use gap). The receipt is unchanged while the reviewed bytes differ.
- The preregister pins none of its own inputs. `sources_opened` lists S085 and S086 as prose labels with no path or digest. C3 promises "frozen digests", but no digest of r22-closure.json, structured-edit-observations.json, or the 128 r22 jsonl transcripts appears in the preregister. Only the individual observations carry `transcript_sha256`.
- `outside_round22` cites manifest entry 422 and commit 4482c275…, but neither value appears in sources/r22-closure.json. That file's `commit` field is the lane commit ae01e50f…. So no declared source lets anyone check that this snapshot is entry 422 at that commit.

Smallest safe correction: the judge binds every receipt to the git blob ID of preregister.json at a named commit, recomputed by the judge and not taken from the receipt. The addendum pins a sha256 for each sources/* file and names S085 → sources/r22-closure.json and S086 → sources/structured-edit-observations.json. Any snapshot that claims to be entry 422 at 4482c275 carries those two values.

### F5 — Slot event ordering rests on timestamps (ordering; fixable)

- The preregister has no ordering structure: no slot sequence, no grant event, and no rule that critic reports (this seat is named "BeforeGrant") must exist before the executor grant. r22's ordering proof was timestamp-only: "Preregistration 415ac3a (11:38:32-03) ... earlier than first build seat session (14:41:12Z)". That compares a git commit date, which can be set freely (GIT_COMMITTER_DATE), with a session clock, with a 2m40s margin.
- Counterexample: commit a preregister after seats start but backdate its date, and the timestamp check still passes. Separately, the digest receipt is written at the end of a seat, so it shows the digest existed before the receipt, not before the grant.

Smallest safe correction: prove order by content addressing, not by clock.
1. The preregister commit (plus addendum) is an ancestor of the commit that adds the seat assignments.
2. The executor-grant record names the content digest of each before-grant critic report.
3. C2's `events.json` is derived from the raw transcripts by their recorded transcript_sha256 and recomputed by the judge, not written by L1. This also removes L1 self-certifying, since L1 already writes the plan, the integration and the bindings.

### F6 — C3's exhaustive per-event reconciliation rests on a source with totals only (C3 calibration; tradeoff the judge must police)

The rough census (25/33) exists only as totals in a prose cell ("approximate own path-binding census"). It has no event list. An event-level reconciliation therefore has to rebuild the rough census, and many event sets give the same totals. The gaps (2 for build, 4 for falsify) could be "explained" by offsetting errors, for example +3 −1. Counting `unexplained_cohorts` per cohort hides this: one cohort can be counted explained while individual events are not.

Smallest safe correction: C3 must label the rebuilt rough event set as a reconstruction hypothesis, list each event's membership in both censuses (not just the arithmetic of the gap), and report as UNKNOWN any event whose rough-census membership cannot be tied to the source. If C3 claims event-level identity for the rough census, the judge must reject that claim rather than accept a match on totals.

## Non-findings, checked

- The `outside_round22` trends (expansion unchanged, quality unchanged, discernment improved) and both path counts (rough 25/33, lane 23/29) match r22-closure.json.
- `limits` keep native enforcement, runtime prevention and round 24 out of scope. That is consistent with r22's ADMITTED-not-enforcement note, so there is no false enforcement claim.
- `ordinal_delta: 0` with all ordinals unchanged is internally consistent.

## Tooling

No installs or updates. This seat's NO-EXEC and NO-FETCH scope forbids them.

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23-crit23beforegrant
Scope: executed=none
