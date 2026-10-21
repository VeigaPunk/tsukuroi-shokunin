# FxC2SchemaV2 — falsification of v2 seat-binding manifest validation

Seat: `FxC2SchemaV2` (round-23, attempt 1, FALSIFY wave, leaf member — no subagent dispatch)
Target: `.ufo/waves/round-23/candidate/tools/check-seat-bindings.py` (declared SHA256 `4e00ab1f…cf3d6`; digest supplied, **not** independently computed — no hash/ls/wc/import/run performed)
Baseline for comparison: `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py` (r22 policy surface)
Supporting reads: `preregister.json`, `build/bindings.json` (landed, 64 seats), `candidate/collect.py`, `candidate/.ufo/waves/round-23/measure/l1-mutation.json`

## Attacked claim

**C2 — "New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim."**
Preregister metric: `structured_edit_mode`, before `0` → target `1`.

Sub-claims I attacked, exactly as briefed:
1. exact seat key set (v2)
2. `edit_paths` ⊆ `read_paths` **and** ⊆ `write_paths`
3. uniqueness (paths, seat names, trace names, agent ids)
4. `local()` on every declared path
5. "a v1 manifest that gains edit authority"

Explicitly **not** attacked here (other seats' lanes): the eight C1 edit-contract decisions in `check-edit-contract.py` (its worktree draft is outside this seat's read scope), the C3 path-census ledger, the "no native restrictive taskset" claim (I make **no** runtime-enforcement claim: the tool's own `SCOPE` string says "Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness").

## Method (NO-EXEC / NO-FETCH)

Static only. I did not execute the checker, did not import it, did not hash it, and did not read any file outside my declared read paths. The "search" below is therefore a **bounded enumeration of the validator's own predicates** (i.e. the complete set of ways a manifest can enter `evaluate()` and reach an edit grant), each resolved by reading the exact source lines, plus a structural read of the one landed v2 manifest. Every falsifier I state is a **constructed input**, not an executed one — I mark each as such.

## Verdict on the primary attack

**The C2 grant invariant holds. I found no manifest that grants v2 edit authority beyond `read_paths ∩ write_paths`, and no v1 manifest that gains edit authority.** What I did find are four defects that do not break that invariant but do bear on the *operability/calibration* of the C2 measurement, ranked below.

### Why no unauthorized grant exists (bounded enumeration of grant entry points)

Grant path in the candidate: `evaluate()` → `classify(..., allow_structured_edit=v2)` (line 186) → `classify_edit(args, binding)` (lines 76-77) → allow iff `value in binding['edit_paths']` (line 128). So an edit is authorized **iff** its `path` string is an exact element of that seat's `edit_paths`.

`allow_structured_edit` is a single manifest-level boolean, `v2 = isinstance(data, dict) and data.get('schema') == 'tsukuroi-seat-bindings-v2'` (line 144), and the schema gate admits only `'tsukuroi-seat-bindings-v1'` / `'…-v2'` (line 145). It is never read from a seat row or an event (`classify`'s docstring, lines 62-66; falsified by selftest rows `v2-row-marker` line 331 and `v2-events-trace-marker` line 337). Therefore the only way to reach `classify_edit` is a manifest whose top-level `schema` is the v2 string, and every seat in such a manifest is then forced through the v2 block.

Seat-level v2 predicate (lines 157-161), all four briefed properties:

| property | code | result |
|---|---|---|
| exact seat key set | `set(seat) != {'name','root','read_paths','write_paths','edit_paths','commands','fetches'}` (158) | any extra/missing key ⇒ `ValueError` ⇒ whole-manifest `SCOPE-SCHEMA` (exit 2). A row-level `allow_structured_edit` marker cannot survive. |
| `edit_paths` ⊆ `read_paths` | `p not in seat['read_paths']` (160) | exact string membership; enforced |
| `edit_paths` ⊆ `write_paths` | `p not in seat['write_paths']` (160) | exact string membership; enforced |
| uniqueness | `len(edits) != len(set(edits))` (159); `len(paths) != len(set(paths))` (154) | enforced; unhashable elements raise `TypeError` ⇒ fail-closed `SCOPE-SCHEMA` |
| `local()` | `not local(p)` (160) and `local(p)` for read/write (154) | enforced on every declared path |
| seat identity | name regex, `seat['name'] in bound`, `root == LANE`, `commands == []`, `fetches == []` (148) | enforced; no seat can carry command or fetch authority |
| top-level key set | `set(data) != {'schema','seats'}` (145) | no top-level default/alias channel |
| duplicate JSON keys | `json.loads(..., object_pairs_hook=unique)` (142) | `ValueError` ⇒ `SCOPE-SCHEMA` |

Consequences I could not defeat:
- **A v1 manifest cannot gain edit authority.** With `schema == '…-v1'`, `v2` is `False`, so `allow_structured_edit` is `False` and an `edit` request falls through to the tool allow-list (line 78) and returns `SCOPE-TOOL-UNKNOWN` (exit 1) — never `classify_edit`. A v1 seat that *carries* an `edit_paths` field gains nothing, because the field is simply never consulted in v1 mode (selftest `v1-extra-edit-field-no-grant`, line 334, and `v1-edit-continuity`, line 335, assert exactly this).
- **The v1/r22 policy surface is byte-for-byte equivalent in behaviour.** The only delta between snapshot and candidate `classify()` is the added `allow_structured_edit` parameter and the `tool == 'edit' and allow_structured_edit` branch (76-77); with the flag `False` the two are behaviourally identical, and `structured_edit_mode` is emitted only `if v2` (205-206), so a v1 run's result shape is unchanged. This supports C2's "legacy schema-v1 policy and historical reds unchanged" clause.
- **The landed v2 manifest is itself valid** against every predicate above. `build/bindings.json` (64 seats) has, per seat, `edit_paths` exactly equal to `write_paths`, and every `write_paths` element also present in `read_paths`; every path is lane-local with no `..`/`.`/empty/`*?[];:` components; `commands`/`fetches` are `[]` everywhere. So the landed manifest grants no edit authority beyond read∩write, and grants no command/fetch authority at all.

**Smallest in-scope remedy for the primary attack: none required.** The v2 grant predicate is sound as written.

---

## Findings by severity

### F1 — HIGH · one edit argument key outside the checker's two shapes voids the entire 64-seat audit (and zeroes the C2 metric)

`classify_edit` accepts exactly two closed key shapes (line 116: `EDIT_SHAPES = ({'path','stream_content'}, {'path','old_string','new_string'})`, minus an optional `i`), and raises `ValueError` for anything else (lines 121-122). `evaluate()` converts that raise into a per-event `SCOPE-SCHEMA` (187-188), and **any** `SCOPE-SCHEMA` finding forces `code = 2` for the *whole* run (194), with `request_audit_mode = 0` and `structured_edit_mode = int(code != 2) = 0` (203, 206). One seat's single odd request therefore destroys the auditability of all 64 seats.

**The two landed components maintain two different whitelists over the same recorded event, and they disagree.** `collect.py:48-51` projects `edit` (alongside `read`/`grep`/`glob`/`write`) with a *shared* key set:

```python
if tool in ('read', 'grep', 'glob', 'write', 'edit'):
    known = {'i', 'path', 'pattern', 'case', 'gitignore', 'skip', 'hidden', 'limit', 'content', 'stream_content', 'old_string', 'new_string'}
    # Retain argument-key presence, never bodies, queries, patterns or other values.
    projected = {key if key in known else '__unknown_argument__': None for key in args}
```

Two concrete divergences, both visible in the landed files:

1. **`replace_all` is erased, and the erasure then trips the shape check.** `replace_all` is a real, documented parameter of the harness `edit` tool (its own specification names it for rename-across-file). It is **not** in `collect.py`'s `known` set, so a recorded edit carrying it is collapsed to the sentinel `'__unknown_argument__'` (`collect.py:51`). The auditor then computes `set(args) - {'i'}` = `{'path','old_string','new_string','__unknown_argument__'}` (four keys) — in neither `EDIT_SHAPES` member ⇒ `ValueError` (122) ⇒ `SCOPE-SCHEMA` (188) ⇒ **run exit 2, `CANNOT_EVALUATE`, `structured_edit_mode` 0**. The projector deliberately erased a real key; the auditor then read the erasure as an unknown shape. Generalised: **any** `edit` argument outside `{i, path, stream_content, old_string, new_string}` becomes cohort-fatal, whether the key is a real harness parameter (`replace_all`) or an adapter artefact.
2. **`'content'` is name-preserved by the projector but shape-rejected by the auditor.** `'content'` *is* in `known`, so it survives projection *by name* for an `edit` event, whereas `EDIT_SHAPES` has no `{'path','content'}` member. So the projector's `known` set for `edit` is a strict **superset** of the auditor's accepted shapes, and the two components disagree about which key names are legitimate for an `edit` — one calls the key known, the other calls the shape unknown. This divergence is **latent**: it becomes a live cohort-fatal event only if a recorded `edit` carries a `content` key, which I could not check (Verification gaps 1 and 3). The `replace_all` divergence in (1) is the one whose trigger is a *documented, default-valued* parameter of the tool the wave actually used.

**Blast-radius regression versus v1.** In the snapshot (r22) checker, `edit` is simply not in the allowed tool list, so it returns `SCOPE-TOOL-UNKNOWN` — a per-event *violation* (exit 1), with the rest of the cohort still audited. In the v2 checker, an `edit` event whose body key the auditor does not recognise is escalated to `SCOPE-SCHEMA`, which is cohort-fatal. r23 therefore raises the consequence of an unrecognized edit body from "one seat's violation" to "the whole wave is `CANNOT_EVALUATE` and C2 reports 0". The v2 path is the *new* code and therefore carries the new blast radius.

**Concrete falsifier (constructed, NOT executed):** one event in the round-23 events file of the form
`{'tool':'edit','args':{'path': <a declared edit target>, 'old_string': …, 'new_string': …, 'replace_all': false}}`
⇒ projection yields `{'path':…, 'old_string':None, 'new_string':None, '__unknown_argument__':None}` ⇒ `set(args) - {'i'}` ∉ `EDIT_SHAPES` ⇒ `SCOPE-SCHEMA` ⇒ **run exit 2, `CANNOT_EVALUATE`, `structured_edit_mode` 0** — a single structured edit request against a perfectly declared target, with an *optional* flag at its default value, zeroes C2 for the entire wave. Whether any round-23 seat actually issued such a call is **unverified**: `round-23/*/events.json` is outside this seat's read scope (Verification gap 1). The second divergence (`content`) does not depend on that at all — it is a pure two-file inconsistency, present in the landed artifacts as they stand.

**Smallest in-scope remedy:** make an unknown shape fail *locally* rather than cohort-wide. Change `classify_edit` so an unrecognized shape returns a per-event finding (a distinct id such as `SCOPE-EDIT-SHAPE-UNKNOWN`) instead of raising, so one request is attributed to its own seat rather than voiding the cohort. Independently, reconcile the two whitelists: add `replace_all` (and, if the projector is to keep it, a `{'path','content'}` member) so the projector stops erasing a real key into a shape the auditor must reject. The per-event-finding change is the load-bearing half; the whitelist reconciliation removes the specific triggers. Note that the per-event change also aligns this tool with C1's own vocabulary: preregister decision `OPAQUE_PATCH = UNKNOWN` ("Missing structured target is not inferred from opaque patch text") is an **UNKNOWN verdict for that request**, whereas here an opaque/foreign edit shape aborts the whole run — a different and strictly harsher outcome for the same input class. (The C1 checker's own handling of `OPAQUE_PATCH` could not be read: `worktrees/ExecEditContract/draft/check-edit-contract.py` is outside this seat's read scope, so I state the cross-tool tension only on the `check-seat-bindings.py` side, which is fully evidenced above.)

### F2 — MEDIUM · v2 narrows the *edit* channel but not the mutation capability, and the narrowing is non-discriminating on landed data

The v2 predicate constrains only `edit_paths` (158-161). The `write` tool remains governed solely by `binding['write_paths']` (line 107), and the v2 validator does **not** require `write_paths ⊆ read_paths` nor `edit_paths == write_paths`. Two consequences:

1. **Latent gap (not realized in the landed manifest).** A manifest that satisfies every v2 predicate may still declare `write_paths ⊋ read_paths` — a *write-only* file. A seat can mutate that file with `write`+`content` and the audit records no finding, while `edit` to the same file is correctly `SCOPE-EDIT-DENIED` (selftest `v2-write-only-target`, line 305). So the v2 invariant is enforced in one direction (edit ⊆ read∩write) and not in the other (write ⊆ read). I checked the landed `build/bindings.json` seat-by-seat: every seat's `write_paths` elements also appear in its `read_paths`, so this direction is *satisfied in fact* and the gap is a **validator** gap, not a live violation in r23's own data. It nonetheless means the seat binder cannot detect a write-only mutation in any future wave, even though C1's decision table treats "read authority never grants a write" as a first-class rule.
2. **The new authority is non-discriminating on landed data.** For all 64 seats in `build/bindings.json`, `edit_paths == write_paths` element-for-element (verified seat-by-seat across the file, including the three `Exec*` seats whose two-element lists are identical in both fields). No real seat has a write target outside its edit targets. Consequently C2's new authority is exercised **only** by synthetic selftest fixtures (the `v2` fixture seat, lines 294-296: `read_paths [src, target, other, 'skill://godspeed']`, `write_paths [target, w-only.md]`, `edit_paths [target]`; the discriminating cases `v2-read-only-target`/`v2-write-only-target`, lines 304-305), never by a landed seat — the v2 code path is *reachable* but never *discriminating* on real data.

   Note the fixture's own shape: it deliberately places `w-only.md` in `write_paths` **without** it appearing in `read_paths` (line 295), and the `v2-write-only-target` case (305) asserts that `edit` to it is `SCOPE-EDIT-DENIED`. So the author *modelled* the write-only state in the fixture and *chose* to deny it for `edit` — while leaving the `write` channel at line 107 free to hit the very same path, and while the manifest validator never forbids that state. The asymmetry is thus a live design gap, not an oversight of the fixture.

**Smallest in-scope remedy:** in the v2 block, additionally require `set(write_paths) ⊆ set(read_paths)` (one line, reusing the already-validated lists) so the seat's mutation surface is read-bounded in both directions; and record per-seat whether `edit_paths == write_paths` in the result rows so the audit's own output shows whether the new authority was discriminating for that seat rather than being silently equivalent to v1 write authority. The first half closes a validator gap that r23's data happens not to exercise; the second half is what makes C2's operability claim falsifiable on real data rather than on fixtures.

### F3 — LOW-MEDIUM · the C2 metric is satisfiable by the schema string alone, and reads `1` even on a FAIL run (vacuous denominator)

`structured_edit_mode = int(code != 2)` (206) is `1` for any v2 manifest whose audit did not hit the `CANNOT_EVALUATE` path — **whether or not any structured edit was observed, whether or not any seat has non-empty `edit_paths`, and whether or not the audit passed**. Two consequences follow directly from line 206:

1. **Vacuous denominator.** The per-seat v2 predicate permits `edit_paths == []` (159-160 are vacuous over an empty list), and selftest `v2-empty-edit-paths` (332) confirms an empty list is a *valid* v2 seat — that case's expected exit is `1` and its expected mode is `1`, i.e. the author asserts the metric reads `1` on a manifest whose edit authority is empty.
2. **The metric reads `1` on a FAIL run.** `code == 1` (a `FAIL` with violations) satisfies `int(code != 2) == 1`. So `structured_edit_mode = 1` and `status = 'FAIL'` can be true simultaneously. The metric is named `structured_edit_mode` and the preregister scope is "audit authority for exact predeclared structured edit targets" — but the value distinguishes only "the v2 code path was reachable and the run was decidable" from "the run was undecidable". It does not distinguish "authority was granted, exercised, and correctly adjudicated" from "authority was never exercised" or from "an edit was denied".

Consequence: C2's target of `1` is reachable with **zero** structured-edit authority in force and zero structured edits adjudicated. The metric measures *mode activation*, not the operability of the authority it names.

**Smallest in-scope remedy:** emit two companion counters in the result — `structured_edit_observed` (events that reached `classify_edit`) and `structured_edit_denied` (of those, how many were denied) — so `structured_edit_mode` has a non-vacuous denominator, or state in the C2 claim that the metric denotes *mode activation* only. Either is a claim-scoping decision for the planner; the falsification-relevant point is that the current metric cannot distinguish "v2 authority exercised" from "v2 label with no authority", and cannot distinguish PASS from FAIL.

### F4 — LOW · v1 seat key sets are not closed (no grant, but a silently ignored declaration)

The exact-key-set discipline (158) applies **only** `if v2:`. A v1 manifest seat may carry any extra field — including `edit_paths` or `allow_structured_edit` — and the v1 validator accepts it without comment (148-156), because v1 never checks `set(seat)`. The field is inert (v1 ⇒ `allow_structured_edit` is `False` ⇒ any `edit` request returns `SCOPE-TOOL-UNKNOWN`, exit 1, and the seat's `edit_paths` field is never read), so this is **not** a grant.

Residual, bounded by mitigation: an operator reading a v1 manifest that contains `edit_paths` could believe edit authority is granted when the tool treats `edit` as an unknown tool. The mismatch does surface — but only if an `edit` is actually attempted, and then as `SCOPE-TOOL-UNKNOWN` (a *violation*, exit 1), not as a manifest finding. So the declaration is silently ignored at manifest level and only incidentally contradicted at request level.

**Smallest in-scope remedy — and a tension I must flag rather than paper over:** the obvious fix, rejecting a v1 seat whose key set is not exactly `{'name','root','read_paths','write_paths','commands','fetches'}`, would convert a currently-*accepted* v1 manifest into `SCOPE-SCHEMA` (exit 2) — and C2's scope requires "legacy schema-v1 policy and historical reds unchanged". So that fix is safe only if no r22 v1 seat carries an extra key, which I could not check (Verification gap 6). The lower-risk form is to **report** the ignored v1 fields (e.g. a `v1_ignored_fields` entry in the result) so the manifest's own declaration is visible, while leaving every v1 verdict byte-identical. I recommend that form; the stricter form is contingent on the r22 check.

---

## Residual risk (explicitly out of scope, stated so it is not mistaken for a clean bill)

- **`local()` is lexical, not resolved.** It rejects control/format characters, `*?[];:`, backslash, and `.`/`..`/empty components, and requires the `LANE + '/'` prefix (33-36). It does **not** resolve the filesystem, so a declared path whose on-disk identity differs from its spelling — a symlink, a case-insensitive-filesystem alias, a Unicode-normalization variant, a trailing-slash form — is not detected. This is consistent with the tool's declared `SCOPE` ("not ... symlink/effect proof"), but it means "exact predeclared target" is exact only at the request-spelling level: the check is exact *string* membership (128), and a spelled-differently target is denied rather than widened, so the exposure is a declared-path/real-file mismatch, not a spelling bypass.
- **Directory expansion is unobservable to this tool.** `read_paths` entries must be `local()` strings; nothing requires them to be files. A directory entry would let `glob`/`grep` on that directory enumerate files outside `read_paths` (the checker only compares the request's own path string, lines 105-113). No landed `read_paths` entry is a directory (all are files under `build/`, `sources/`, `snapshot/`, `packs/`, `frozen/`), so this is latent, not realized. `skill://godspeed` is the one deliberately non-`local()` sentinel permitted, and only in `read_paths` (line 154) — it can never enter `edit_paths` (160 requires `local(p)`), and `write`/`edit` to it are denied (selftest `skill-write` 259, `v2-spelling-skill://godspeed` 307).
- **Manifest↔event seat-name coupling.** The audit binds a trace seat to a manifest seat by `name` only; the manifest carries no agent id. The two files must come from the same bound revision — `main()` does enforce that (both `git_read(binding.sha, …)` under one `_revision.bind`, lines 388-391), and a mismatched wave pairing is detected as `SCOPE-TRACE-MISSING` ⇒ exit 2 rather than silently passing. Preregister's C2 command leaves `<WAVE>` as a placeholder; picking the wrong wave yields exit 2, not a false PASS.
- **Error containment is cohort-wide by design, on both the event side and the manifest side.** On the event side, any single `SCOPE-SCHEMA` (F1) or incomplete seat zeroes `request_audit_mode` and `structured_edit_mode` for all seats; the per-seat rows (`rows`, 193) still exist, but `request_audit_mode = 0` marks the whole result as non-auditable. On the manifest side, the seat loop is all-or-nothing: one seat with an unexpected key set, a duplicate path, a non-local path, or an `edit_paths` entry outside read∩write raises `ValueError` (149, 154, 158, 160), which is caught at 195 and yields one `SCOPE-SCHEMA` finding at site `'input'` with `code = 2` — the whole 64-seat manifest is unevaluable because of one malformed seat, and `seats_bound` falls back to `locals().get('bound', {})` (198), i.e. the count of seats validated *before* the failure. There is no per-seat manifest diagnostic, so a malformed manifest cannot be repaired by identifying the offending seat. This is a deliberate fail-closed design and I make no claim against it as an authority property — but it is the mechanism that makes F1 and F3 cohort-fatal rather than seat-local, and it is why the manifest-side remedy for F1/F2 must be *validation-side* (per-seat diagnostics) rather than merely stricter rules.

## Verification gaps (things I could not check from this seat's declared read scope)

1. **`round-23/build/events.json` and `round-23/falsify/events.json` are not in my read paths.** Therefore: (a) I could not confirm whether any recorded `edit` event carries `replace_all` (F1's trigger) — F1 is stated as a *constructed* falsifier; (b) I could not confirm how many seats actually exercised `edit` at all, which is what F3's denominator claim turns on.
2. **`round-23/falsify/bindings.json` is not in my read paths** — I verified the *build* manifest only. F2's "no landed seat discriminates" claim is verified for `build/bindings.json` (64 seats) and is **[INFERENCE]** for the falsify-wave manifest, which I could not read.
3. **`round-23/sources/structured-edit-observations.json` and `sources/edit-decision-policy.json` are not in my read paths** — I could not cross-check the `EDIT_SHAPES` vocabulary against the observed recorded argument keys (the source of truth for whether `replace_all`/`content` actually occur), nor against C1's eight decisions. F1's severity depends on (1) and (3).
4. **`worktrees/ExecEditContract/draft/check-edit-contract.py` and `worktrees/ExecEditAudit/draft/check-seat-bindings.py` are not in my read paths** — I could not read the *landed* (as opposed to `candidate/`) checker to confirm the candidate copy is the landed copy, nor read C1's checker to confirm its `OPAQUE_PATCH = UNKNOWN` treatment.
5. **The declared SHA256 was not independently computed** (per the brief: no hashing of the target). All my findings are anchored to *read source lines* of `candidate/tools/check-seat-bindings.py`, not to a digest match.
6. **r22 legacy manifests (`snapshot/r22/{build,falsify}/bindings.json`) are not in my read paths** — F4's remedy ("confirm no r22 v1 seat carries extra keys") could not be performed here.
7. **No execution of any kind**: the checker was not run, the selftest was not run, no mutant was re-run. The `l1-mutation.json` record (27/27 killed, 10 of them against `check-seat-bindings.py`, including mutants on `allow_structured_edit` gating and on the `read_paths`/`write_paths` subset conditions) is cited as the author's own evidence; I did not re-derive it. My findings are *outside* that mutant set — the mutation campaign never exercised `replace_all`/`content` shape coverage or the `write_paths ⊄ read_paths` asymmetry, which is consistent with F1/F2 being live.

## Smallest in-scope remedy, consolidated

| ID | severity | one-line remedy | file |
|---|---|---|---|
| F1 | HIGH | make an unrecognized edit *shape* a per-event finding (e.g. `SCOPE-EDIT-SHAPE-UNKNOWN`) instead of a raise, so one request cannot void the 64-seat cohort; and reconcile the two whitelists so `collect.py` stops erasing `replace_all` into a shape the auditor must reject | `candidate/tools/check-seat-bindings.py:116-122`, `candidate/collect.py:48-51` |
| F2 | MEDIUM | in the v2 block also require `set(write_paths) ⊆ set(read_paths)`; record per seat whether `edit_paths == write_paths` | `candidate/tools/check-seat-bindings.py:157-161,193` |
| F3 | LOW-MED | emit `structured_edit_observed` / `structured_edit_denied` counters, or narrow the C2 metric's claim text to "mode activation, and it reads 1 on FAIL too" | `candidate/tools/check-seat-bindings.py:205-206`; `preregister.json` C2 scope |
| F4 | LOW | close the v1 seat key set (or report ignored v1 fields) so a v1 manifest's `edit_paths` cannot sit silently unenforced | `candidate/tools/check-seat-bindings.py:148-156` |

**Primary attack result: no falsifier found for the briefed invariant.** The C2 v2 grant predicate — exact seat key set, `edit_paths` ⊆ `read_paths` ∩ `write_paths`, uniqueness, `local()`, and v1 non-escalation — holds under every bounded enumeration of the manifest's entry surface that I could construct from the source, and the landed `build/bindings.json` conforms to it. The defects above attack C2's *operability and calibration* (F1, F2, F3), not its *authority* semantics. F1 is the material one: it is sufficient on its own to make the C2 metric report `0` for a wave in which any seat used the harness `edit` tool with its documented `replace_all` flag at its default value, and it is a *new* blast radius introduced by r23's v2 path (in r22 the same request was a per-seat violation, not a cohort-wide `CANNOT_EVALUATE`).

**One-line summary for the planner:** the v2 authority gate is sound; the v2 *reporting surface* is not — the shape check is cohort-fatal where it should be seat-local (F1), the write channel is not read-bounded (F2), and the metric that names the authority cannot tell an exercised authority from an empty one, nor PASS from FAIL (F3).

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2schemav2
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
