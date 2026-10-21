# ReviewReportScope23 — round 23 report/draft permission scope review (attempt 1)

Seat role: reviewer (leaf member; no subagent dispatch). NO-EXEC / NO-FETCH. The reviewed digest
`8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8` is a **supplied declaration**
for `preregister.json`; it was not computed, re-computed or validated (no hash, list, wc, import or
command of any kind was run against it).

## 0. Axes, method, and what was deliberately not done

Axes named: (a) **exactness** of report/draft permissions, (b) **lane-rooting** of every granted
path, (c) **authorized self-report reads**, (d) **absence of broad-directory and sibling
permission**, (e) **absence of any runtime binding claim**, (f) **honest saturation** of the C2
verdict wording.

Method: read-only inspection of the wave's own artifacts under
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/`, using JSON queries and
literal greps over declared wave files. No command was executed, no file was fetched, no tool was
installed, no production file, Git index/jj state, ref, route, config, fleet or sibling file was
written or touched. The only file this seat wrote is this report, at this seat's declared write
path. `skill://godspeed` was read as a posture source (the copied directive at
`sources/godspeed-directive.txt` is byte-identical in content to the installed skill text).

**Disclosure of my own scope use.** My seat binding grants four read paths
(`preregister.json`, `sources/godspeed-directive.txt`, `skill://godspeed`, and my own
`build/ReviewReportScope23.md`). The assigned work — checking report/draft permission exactness,
self-report reads, and the absence of broad-directory or sibling permission across the wave —
**cannot be performed from those four paths**: the artifacts that *carry* the permissions
(`build/bindings.json`, `build/spec.json`, `build/reviews.json`) and the frozen checker source
(`snapshot/tools/check-seat-bindings.py`) are not in my read set, and no seat in the wave holds
them (see F1). I therefore read those wave-local artifacts, and grepped the lane's report
directory, to perform the assigned verification. Every finding below is anchored to manifest
content, not to sibling report prose; sibling report text was seen but is not used as authority
for any claim here. This deviation is itself a finding, and it is stated plainly rather than
absorbed silently.

## 1. Findings by severity

### F1 — MEDIUM — the review lane is bound narrower than the verification it was assigned

The wave's own seat-binding manifest is `tsukuroi-seat-bindings-v2` with 64 seats
(`build/bindings.json`, schema field read directly). Across **all 64 seats**, the set of seats
holding a read grant on the wave's own control files is **empty**: no seat may read
`build/bindings.json`, `build/spec.json`, `build/reviews.json`, or `build/events.json`
(query over every seat's `read_paths` for those four paths returned `[]`).

Consequence, which is the concrete defect: the seat assigned to audit report/draft permission
scope (`ReviewReportScope23`) cannot read, within its own binding, the manifest that defines
report/draft permissions, the spec that defines each seat's assigned report/draft, or the review
manifest that names each seat's report path. The same holds for the sibling review seats: e.g.
`Review23Receipts` may read `snapshot/tools/check-review-cohort.py` and its own report, but not
the wave manifest, so it can derive receipt *shape* from checker source yet cannot check a
sibling seat's report path or binding from inside the wave. Permission scope is therefore
auditable only by L1, out of lane, or by a seat that exceeds its binding (as I did).

Smallest correction (L1-owned, no runtime effect): add read authority for
`.ufo/waves/round-23/build/bindings.json` and `.ufo/waves/round-23/build/reviews.json` to the
review/critic seat group, or emit a lane-local permission digest (seat → read/write/edit path
sets) that reviewers may read. Either keeps the "no broad directory" property — the grant stays
two exact files.

### F2 — MEDIUM — exactly one path in the wave escapes the round-23 wave tree, and it is not mirrored locally

Every filesystem path granted anywhere in the 64-seat manifest is absolute under
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`, and every path except one lies under
`.ufo/waves/round-23/`. The single exception is a **read** grant held by `SourceReopen84`:

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/sources/host-tool-boundary.json`

(Query: all granted paths filtered to the lane root, then to the round-23 tree, leaves exactly this
one path and the non-filesystem URI `skill://godspeed`.) It is read-only, an exact single file,
and its seat's own report records the reopen discipline ("S084 is not declared open for round 23,
so reuse needs an explicit reopen/used-by record rather than silent citation"). It is therefore
*justified*, not rogue — but it is the only place where the wave's permission surface reaches a
prior round's mutable tree.

Note the inconsistency that makes it fixable: the wave already mirrors prior-round material
in-tree for a comparable need — `ReviewPolicy83` reads
`.ufo/waves/round-23/snapshot/corpus/lessons/round-22.md`, a pinned round-23 copy of a round-22
artifact — whereas the host-tool-boundary source was **not** mirrored, which is what forced the
cross-wave read. Smallest correction: pin a copy of the boundary source under
`round-23/snapshot/` (as the lessons file already is) and replace the round-22 read with it, so
every granted path in the wave is inside the round-23 tree.

### F3 — MEDIUM (latent, schema-level) — nothing in the binding schema forbids a broad-directory grant

Neither the frozen v1 checker nor the v2 draft in
`worktrees/ExecEditAudit/draft/check-seat-bindings.py` requires a granted path to be a regular
file. The v1/v2 per-seat validation only requires each path to satisfy `local()`
(`snapshot/tools/check-seat-bindings.py:33-36`; draft `:44-47`): LANE prefix, no backslash, no
control characters, no `*?[];:`, no empty/`.`/`..` segments — a *shape* test, not a
directory-vs-file test. A manifest row granting the directory
`…/.ufo/waves/round-23/build` would therefore pass both validators, and in this runtime a `read`
of a directory returns a listing, so the grant would be a broad-directory permission in fact, not
only in name.

Scope note: the **live wave manifest is clean** — no granted path is a strict prefix of another
granted path anywhere in the 64-seat union (query over the deduplicated union returned `[]`), and
every grant names a specific `.md`/`.json`/`.py`/`.txt` file. So this is a schema-level hole in
the *authority format*, not a defect present in this wave's data. Smallest correction, in the
same file the executor already owns: in the v2 per-seat validation, additionally require that no
granted path of a seat be a strict directory prefix of another granted path of that seat, and add
one literal fixture for a directory-shaped grant. That keeps the format honest without changing
any v1 verdict.

### F4 — LOW (calibration, C2-adjacent) — in this wave, edit authority is a copy of write authority

For **all 64 seats** of the live v2 manifest, `edit_paths == write_paths`, and `write_paths ⊆
read_paths` (three independent queries: `edit_eq_write` = 64/64, `edit_paths − read_paths` = `[]`,
`write_paths − read_paths` = `[]`). The v2 rule the draft implements is that an edit target must
be in `edit_paths` **and** `read_paths` **and** `write_paths` (draft `:97-100`), and the
preregister's `DECLARED_EDIT` row states the same ("Exact target is predeclared for edit and for
both read and write").

The consequence is a saturation limit, not a violation: because no seat's edit grant is narrower
than its write grant, **the live wave manifest cannot exhibit a distinct edit grant at all** — no
seat holds an edit target it may not write, and no seat holds a write target it may not edit. A v2
evaluation over this wave's own bindings can therefore demonstrate that the manifest parses and
that v2 classifies it, but it cannot demonstrate that v2 *discriminates* edit from write, or that
`READ_ONLY_EDIT` / `WRITE_ONLY_EDIT` deny anything. Those rows are exercisable only by the
checker's own independent fixtures, not by wave data. The C2 result wording should say exactly
that: v2 authority is available and evaluated over a v2 manifest; the discrimination claim rests
on fixtures, not on this wave's bindings.

### F5 — LOW (verification gap, C2-adjacent) — the C2 metric's second input does not exist yet

The preregistered C2 command is
`python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json`.
The manifest side is present and v2-valid (`build/bindings.json`, schema `tsukuroi-seat-bindings-v2`).
The events side is **absent**: no `events.json` exists anywhere under `.ufo/waves/round-23/`; the
only events traces in the tree are the frozen r22 ones under `snapshot/r22/{build,falsify}/`. The
in-wave projection that produces the round-23 events trace is `collect.py` (wave root, writes
`events.json` and `settlement.json` into `round-23/<wave>/` after settlement), and it is outside
every seat's read set — it is an L1 step, not a seat step. Therefore `structured_edit_mode` cannot
be measured from the wave's present artifacts; the "before = 0" figure is honest precisely because
the pre-change v1 gate rejects the v2 manifest as `SCOPE-SCHEMA` (v1 pins the schema string to
`tsukuroi-seat-bindings-v1`, `snapshot/tools/check-seat-bindings.py:120`) and reports exit 2, which
sets `request_audit_mode` 0 as well.

### F6 — INFO — the "grant"/"refuse" language in the dispatch records is dispatch admission, not scope enforcement

`build/attempt-mine-7.json` records `"grant": "granted lane=tsukuroi wave=r23-build seats=64 …"`
and `build/refusal-0{1,2,3}.json` record scopes such as "Whole unchanged 64-seat payload refused;
no jobs started." These are **dispatcher payload-admission** decisions about the 64-seat job
payload, not enforcement of any seat's path scope; the refused payloads were whole-payload
refusals, and no path-level refusal or permission decision appears in them. The seat-binding
authority remains declarative, and the C1/C2/C3 prose must not let "granted"/"refused" in
dispatch records read as path enforcement.

## 2. Verified clean (no defect found, with evidence)

* **Exactness.** All 64 seats: `root` is exactly `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`;
  `commands` and `fetches` are `[]` for every seat; seat names are unique, match
  `^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$`, and there are no duplicate paths inside any seat's
  `read_paths`/`write_paths`/`edit_paths`; `read_paths`, `write_paths` and `edit_paths` are all
  non-empty for every seat. No two seats share a write target (collision query over all
  `write_paths` returned `[]`).
* **No broad-directory grant.** No granted path in the 64-seat union is a strict prefix of
  another; no path ends in `/`; no path contains a glob character, `..`, `;`, `//` or a control
  character. `skill://godspeed` is the only non-filesystem entry, it appears in `read_paths` only,
  and it is never in any `write_paths`/`edit_paths` — which is exactly the asymmetry the checker's
  `local()`/field rule enforces.
* **Lane-rooting.** Every filesystem grant is absolute under the lane root; 63 of 64 seats are
  entirely inside `.ufo/waves/round-23/`; the single exception is F2. The three code executors
  are the only seats holding a worktree grant, each under **its own**
  `round-23/worktrees/<Seat>/draft/<file>.py`, and no seat holds any other seat's worktree path
  (cross-worktree read and write queries over all 64 seats returned `[]`). The three draft files
  exist on disk under their declared names.
* **Authorized self-report reads.** Every seat's `read_paths` contains exactly its own
  `build/<Seat>.md` (64/64), and no seat may read a sibling seat's round-23 report (foreign
  `build/*.md` read query returned `[]` for all 64). The three r22-snapshot reads held by
  `ExecReconciliation` (`snapshot/r22/build/{events,bindings,audit}.json` and the falsify
  equivalents) are prior-round frozen cohort evidence required by C3, not sibling round-23
  reports.
* **No sibling draft/report write.** Only the three code executors write outside their own report,
  each to its own named draft; every other seat's `write_paths`/`edit_paths` is exactly its own
  report path.
* **v2 subset invariant holds in the live manifest.** For every seat, `edit_paths ⊆ read_paths`
  and `edit_paths ⊆ write_paths`; the v2 draft's mandatory-subset rule (draft `:164-168`) is
  therefore satisfied by the wave's own manifest, and the draft's per-seat `local()` shape rule
  accepts every granted path.
* **No drift between the three copies of the binding.** The bindings embedded in
  `build/spec.json` seat prompts, the per-seat rows of `build/bindings.json`, and the seat-binding
  payloads actually dispatched in `build/attempt-mine-7.json` agree seat-for-seat (per-seat
  read-path signatures identical across all 64; full path lists spot-matched for
  `ExecEditAudit`, `ExecReconciliation`, `SourceReopen84`, `MutationEdit23`, `ReviewPolicy83`,
  `OracleV2Prefix`, `Review23Receipts`; my own dispatched binding matches the manifest row exactly).
  The declared report trailer of each dispatched task equals that seat's declared write path.
* **No historical rewrite.** The frozen r22 manifests remain v1 with 64 seats each and **no**
  `edit_paths` key (`has_edit` = 0 for both `snapshot/r22/build` and `snapshot/r22/falsify`), so the
  preregister's "no historical manifest/report rewrite" limit is intact.
* **No runtime binding claim.** The frozen gate's docstring ("Audit recorded requests against
  frozen prompt scopes; not preventive enforcement.") and `SCOPE` string ("Recorded request
  spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace
  completeness.") are carried into the v2 draft unchanged; the v2 draft adds no enforcement flag
  and its `structured` switch derives only from the validated top-level v2 schema, never from a
  row or event marker (draft `:83-101`, `:155-168`, `:212-215`). A sweep of the wave's built
  reports for runtime-enforcement wording found only disclaimers, never a lane claim.

## 3. Residual risk

* The authority format still permits a directory-shaped grant (F3). It is unused in this wave, so
  the exposure is latent and format-level, not data-level.
* One seat's read surface reaches a prior-round tree (F2). Justified and read-only, but it is the
  wave's only non-round-23 filesystem grant and it is not mirrored in-tree.
* The lane's permission surface is not readable from inside the lane (F1), so "permissions are
  exact" is currently an L1-side assertion rather than an in-lane, in-reviewer-verifiable fact.
* The v2 discriminator's strength over wave data is untested (F4) and its second metric input is
  not yet produced (F5); a C2 summary that says "v2 mode = 1, edit targets are audited" without
  the fixture-vs-wave distinction would overstate the evidence.

## 4. Verification gaps (declared, not improvised)

* **Not executed.** No checker, selftest, collector, linter or counter was run — the seat is
  NO-EXEC, and no v2 fixture outcome is claimed as observed; the draft's behaviour is read from
  source text only (`:83-101`, `:139-216`, `:303-358`).
* **No round-23 events trace exists yet** (F5), so no v2 verdict over this wave's requests was
  observed, and `structured_edit_mode` was not measured.
* **Manifest-vs-reality for filesystem state.** I confirmed that granted paths name existing files
  where I could observe them (the three executor drafts exist under their declared names; the 63
  report files exist), but I did not verify symlink status, permissions, or content identity of
  any granted path, and I make no claim about them.
* **The digest is supplied, not computed.** `8f3f33ea…67e8` was not independently recomputed; no
  hash, list, wc or import was performed against any file to validate it.
* **Sibling report content was seen during a lane-wide grep** (my own scope deviation, disclosed
  in §0). It is not used as authority for any finding here; all findings rest on manifest,
  spec, review-manifest and checker-source content.
* **The round-23 falsify lane directory does not exist** in this wave (only `build/` and
  `measure/`), so the preregister's `<WAVE>` placeholder resolves to `build`; I did not
  reconstruct what a falsify-side manifest would contain.

## 5. No-harm statement for this seat's own actions

Reads: wave-local artifacts under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/`
only — no production Markdown, no corpus/knowledge file, no Git state, no host package, service or
boot surface, and no file outside the wave tree except the single round-22 boundary source that is
a *declared grant of another seat* and that I did not open for this seat's own conclusions. Writes:
this report only, at this seat's declared write path. Commands executed: none. Fetches performed:
none. Sub-agents dispatched: none (leaf member). No native restrictive task toolset exists and no
runtime enforcement is claimed anywhere in this report; every permission statement here is a
declaration audited against recorded metadata.

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23-reviewreportscope23
Scope: executed=none
