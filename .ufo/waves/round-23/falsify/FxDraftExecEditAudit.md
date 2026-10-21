# FxDraftExecEditAudit — wave-1 draft vs landed candidate (round23 attempt1, falsify wave)

Seat: `TsukuroiR23-2.FxDraftExecEditAudit-2`. Lane bounds: leaf member — no subagent dispatch.

Target: landed `tools/check-seat-bindings.py` at `.ufo/waves/round-23/candidate/tools/check-seat-bindings.py`, declared SHA256 `4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6` (supplied identity; never hashed, listed, imported, compiled or run).
Comparator: independent wave-1 draft `.ufo/waves/round-23/worktrees/ExecEditAudit/draft/check-seat-bindings.py` plus its seat report `.ufo/waves/round-23/build/ExecEditAudit.md`.
Baseline `ae01e50f582016384e620022be38bf5367000e2e`; integrated landed state `5a25c88b77f52e940bcad87825c4ac1cd529470d`.

## Method and honesty bounds

- NO-EXEC / NO-FETCH honored: zero commands, zero fetches, zero delegations. The declared digest was accepted as supplied identity and never validated by computation.
- Both bound files were read **in full, as raw line ranges** (`candidate/...:raw:1-200` and `:raw:200-400`; `worktrees/.../draft/...:raw:1-200` and `:raw:200-420`), plus `preregister.json` (raw), `build/ExecEditAudit.md` (raw) and `sources/godspeed-directive.txt`.
- **No LSP server is available to this seat**: the seat tool inventory exposes no `lsp` device, and `xd://` plus `bash`/`eval` are forbidden by the seat's narrower NO-EXEC/NO-FETCH scope. Definition/caller/diagnostic checks were therefore done by whole-file reading of the two bound files, not by a semantic index; nothing below is presented as grep-level proof of semantic absence. The claim "no other caller exists" is scoped to those two files.
- This seat edits only its own report. No production file, Git index/refs state, route, or host state was touched. A verdict here is a recommendation, never an admission or an integration.

## Claim attacked

**C2** (axis operability, metric `structured_edit_mode` 0 → 1): "New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim."

C2 is coupled to **C1** (axis depth, metric `validated_edit_decisions` 0 → 8): the canonical eight-row decision table in `preregister.json` (`edit_decisions`) is the same table the seat-binding audit must be able to *express* for its recorded requests. The attack below is therefore aimed at the decision/ID/exit fidelity of the v2 structured-edit path, and at the controls that pin it.

## Divergences (candidate = landed, draft = wave-1)

### D1 — Alternate-spelling edit targets collapse three decision rows into one finding ID — **Medium**

Literal case (both sides, same event, same binding, `edit_paths = ['/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/drafts/A.md']`, args `{'path': '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/drafts/./A.md', 'stream_content': <opaque>}`):

- candidate `classify_edit`: skips `requested_path` entirely; the literal string is not an element of `edit_paths` → `['SCOPE-EDIT-DENIED']`, exit **1**.
- draft `classify` (edit branch): `requested_path(args['path'])` → `local()` rejects the `.` component → `['SCOPE-PATH-DENIED']`, exit **1**.

Same class of divergence for every non-`local()` spelling, all of which the candidate labels `v2-spelling-*` and asserts as `SCOPE-EDIT-DENIED` in its own selftest (candidate lines with `v2-spelling-`): dot segment `/drafts/./A.md`, traversal `/x/../drafts/A.md`, trailing slash `/drafts/A.md/`, double slash `//drafts/A.md`, selector suffix `:raw`, relative spelling `drafts/A.md`, upper-cased spelling, and internal URI `xd://edit`. Draft asserts `SCOPE-PATH-DENIED` for the same literals (fixtures `v2-edit-dot-segment`, `v2-edit-traversal`, `v2-edit-internal-uri`, `v2-edit-selector-spelling`). URLs agree on both sides (`SCOPE-FETCH-DENIED`).

Which side is right: **the draft**. `preregister.json` `edit_decisions` enumerates `EDIT_TRAVERSAL` (row 6, "No dot-segment or alternate spelling expands the target list") and `EDIT_EXTERNAL` (row 7, "Remote or internal URIs do not become filesystem edit targets") as decisions *distinct* from `UNDECLARED_EDIT` (row 2); and the wave-1 seat report's declared policy mapping (`build/ExecEditAudit.md:18`) states `EDIT_TRAVERSAL → SCOPE-PATH-DENIED`, `EDIT_EXTERNAL → SCOPE-FETCH-DENIED / SCOPE-PATH-DENIED`, `UNDECLARED_EDIT / READ_ONLY_EDIT / WRITE_ONLY_EDIT → SCOPE-EDIT-DENIED`. The landed tool makes rows 2, 6 and 7 indistinguishable in its own output, and contradicts the mapping declared in the very report it was integrated from. Note the decision itself is not in doubt: both sides DENY, so this is audit-fidelity loss, not an authority escape.

### D2 — v2 seat key set: candidate adds an undocumented exact-7-key rule; draft does not — **Medium**

Literal case (v2 manifest, seat = `{name, root, read_paths, write_paths, edit_paths, commands, fetches, 'note': 'x'}`):

- candidate: `set(seat) != {'name','root','read_paths','write_paths','edit_paths','commands','fetches'}` → `raise ValueError('v2 edit authority')` → whole-manifest failure: findings `[{'id':'SCOPE-SCHEMA','site':'input'}]`, status `CANNOT_EVALUATE`, exit **2**, `structured_edit_mode` **0** → the C2 metric does **not** reach 1 for that wave.
- draft: extra seat keys are ignored; the seat is validated on `edit_paths` only and evaluated normally.

Which side is right: **the candidate is safe but unjustified and asymmetric**. The wave-1 report lists the v2 rejection reasons exhaustively as "subset violation, duplicates, nonlocal spelling, or missing field" and reserves an exact-key-set rule to the *top level* (`{schema, seats}`); it never claims an exact seat key set, and its "Interpretations flagged for review" list does not mention one. The candidate is also internally asymmetric: the exact-key check runs only under v2, so a **v1** seat may still carry a forged `allow_structured_edit` row field and be silently accepted (no grant results, because the flag is derived only from the top-level schema — but the forgery surface survives). Risk is operational rather than permissive: a single benign extra field on any seat sinks the entire C2 run to `CANNOT_EVALUATE`.

Mitigating evidence (not a proof): the seat binding issued to this seat itself carries exactly `name, root, read_paths, write_paths, edit_paths, commands, fetches`, and its `edit_paths` ⊆ `read_paths` ∩ `write_paths` — so the real producer shape appears to satisfy the candidate's strict rule. The C2 command's actual `bindings.json` is outside this seat's read paths, so producer compatibility is **unverified** here.

### D3 — Dropped negative control for a forged v1 row/event marker — **Low–Medium**

The draft pins `v1-forged-row-marker-no-grant` (v1 binding + event args carrying `allow_structured_edit: True` → exit 1, `SCOPE-TOOL-UNKNOWN`). The candidate's 36 v2 fixtures have no equivalent; it replaced the case with `v2-row-marker` (a v2 *manifest* extra key → exit 2) and `v2-events-trace-marker` (a v2 *event* marker → exit 2 `SCOPE-SCHEMA`). The v1 forgery invariant ("no forged marker grants an edit under v1") is therefore no longer proven by the landed selftest, while the candidate still accepts such a v1 seat (see D2). No current grant results — the flag is top-level-derived on both sides — so this is a control regression, not a behavior divergence.

### D4 — Event-time triple-membership check dropped — **Low (latent)**

Draft `classify` (edit branch) requires `target ∈ edit_paths ∧ read_paths ∧ write_paths`; candidate `classify_edit` requires only `target ∈ edit_paths`. Today this is **not** an observable divergence, because both manifests validate `edit_paths ⊆ read_paths ∩ write_paths` at seat level (verified in both files: candidate `any(not local(p) or p not in seat['read_paths'] or p not in seat['write_paths'] for p in edits)`; draft the same), so the "declared but not writable/readable" class is unreachable on either side. The draft's redundancy is defense-in-depth: if the subset rule is ever relaxed — which is precisely one candidate remedy path for D2 — the candidate would grant an edit to a target that is not writable, while the draft would still deny.

### D5 — v2 semantics are undocumented in the landed file — **Low**

The candidate's module docstring is the legacy one-liner ("Audit recorded requests against frozen prompt scopes; not preventive enforcement.") with no statement of the v2 schema, the `edit_paths` subset rule, or the denial-ID mapping. The draft's docstring documented all of it. The wave-1 report's flagged interpretations (empty `edit_paths` = no edit authority; `structured_edit_mode` absent on v1/missing-manifest results; prefix-spelling → `SCOPE-EDIT-DENIED`) are discoverable only from the report, not from the tool that implements them.

### D6 — Selftest assertion strength: candidate is stronger — **informational, keep candidate side**

Candidate v2 pass condition adds `(expected != 0 or not ids)` — a case expecting exit 0 must carry **no** finding at all. The draft's v2 loop only requires the expected IDs to be *present*, so a spurious extra finding (e.g. an unexpected `SCOPE-EDIT-DENIED` on a positive case) would still pass the draft's selftest. The candidate's assertion is the correct one. Both v1 loops are equally lax, so no v1 divergence.

### D7 — Fixture inventory / expected-aggregate mismatch — **Low (operational)**

Candidate: 73 v1 + 36 v2 = **109** cases. Draft: 73 + 35 = **108**, and the wave-1 report states the expected integration aggregate as `PASS, cases: 108, failed: 0`. The landed selftest will therefore report `cases: 109`; an integration check that asserts 108 will report a false failure. The candidate also drops the draft's `v2-edit-paths-nonlocal-spelling` fixture (replaced by the equivalent `v2-edit-paths-skill`) and adds `v2-read-only-target` / `v2-write-only-target`.

## Verified equal (no divergence — bounded literal comparison)

- v1 classification for `read`/`grep`/`glob`/`write`/`multi_tool_use.parallel`/`parallel`/`bash`/`eval`/`task`/`web_search`/`browser*`: byte-equivalent logic, including the "known forbidden tool is evidence even when its payload is missing" rule, `functions.` prefix stripping, depth cap 8, selector token validation, `;`-split for grep/glob, and the unknown-key → `SCOPE-SCHEMA` rule.
- Edit argument shape: candidate `set(args) - {'i'} ∈ EDIT_SHAPES` and draft `set(args) ∈ EDIT_SHAPES` accept the **same** key sets (`{path,stream_content}` and `{path,old_string,new_string}`, each optionally `+i`); unknown key, mixed shape, missing body field, non-dict args, missing path and non-string path all yield `SCOPE-SCHEMA` on both sides. OPAQUE_PATCH (row 5) is `SCOPE-SCHEMA` / CANNOT_EVALUATE on both sides, never inferred from body text; body values stay opaque on both sides (candidate fixtures even use `None` and dict values).
- `skill://godspeed` as an edit target → `SCOPE-EDIT-DENIED` on both sides (the draft's `requested_path` exempts only that exact spelling, and it cannot appear in `edit_paths` because `local()` rejects it).
- URL target → `SCOPE-FETCH-DENIED` on both sides, including the `host:port/` form.
- Flag provenance: `allow_structured_edit` is derived only from the validated top-level v2 schema on both sides; no binding-row field and no event argument marker can enable it.
- Parallel and doubly-nested parallel recursion threads the flag on both sides (no bypass through a wrapper).
- `structured_edit_mode` presence/absence: present only for v2 manifests, `1` on exit 0/1, `0` on exit 2; absent for v1, for an unsupported schema (v3), and for a missing manifest — identical on both sides.
- Exit ladder: `2` if any seat is missing/incomplete or any finding is `SCOPE-SCHEMA`, else `1` if any finding, else `0`; `SCOPE-BINDINGS-MISSING` early return at exit 1 — identical on both sides.
- EXPANSION / CHECK_EACH (row 8): neither side models "native extra read/write starts around a structured edit"; adapter read/write events remain independently audited per event on both sides.
- Honesty anchor `SCOPE` string identical on both sides: recorded request spellings only, not runtime prevention, symlink/effect proof, reading proof or universal trace completeness.

## Bounded search — no authority escape found

Search space (static, symbolic, both sides compared side by side):

- argument-shape classes: `EDIT_SHAPES` ± `i`; unknown extra key; missing body field; mixed shapes; non-dict args; missing `path`; non-string `path`.
- path classes: exact declared target; local-but-undeclared (read-only / write-only / unrelated / prefix `X.extra`); non-local spellings (dot segment, `..`, trailing `/`, `//`, `:selector`, relative, upper-cased, glob char, backslash, control char, internal URI `xd://…`); URLs (`https`, `http`, `host:port/`).
- manifest classes: v1 (with and without extra seat fields); v2 valid (`edit_paths ⊆ read ∩ write`, incl. empty `edit_paths`); v2 with missing / duplicate / non-local `edit_paths`; v2 with an extra seat key; v3 schema; missing manifest; malformed JSON / duplicate JSON key.

Result: the **allow sets are identical**. An edit is allowed on both sides iff the target string is exactly an element of the validated `edit_paths` list (itself `local()`, therefore non-URL) *and* the argument key shape is in `EDIT_SHAPES` ± `i`. Because `edit_paths` validation already enforces `⊆ read_paths ∩ write_paths` on both sides, "declared but not readable/writable" is unreachable on both sides. No input class exists in which the landed tool allows an edit the draft denies, or denies one the draft allows; every non-declared, malformed, remote or internal-URI target is denied by both. The divergences above are therefore confined to **finding-ID granularity (D1)**, **manifest strictness (D2)**, **control coverage (D3)** and **documentation/assertion strength (D5–D7)** — not to the allow/deny decision itself.

## Smallest in-scope remedy

One helper call in the landed `classify_edit`, restoring the draft's decision-to-ID mapping while keeping every other candidate behavior:

```python
    value = args.get('path')
    if not isinstance(value, str) or not value:
        raise ValueError('missing explicit edit target')
    target, denial = requested_path(value)          # URL -> SCOPE-FETCH-DENIED, non-local -> SCOPE-PATH-DENIED
    if denial:
        return [denial]
    if (target not in binding['edit_paths'] or target not in binding['read_paths']
            or target not in binding['write_paths']):
        return ['SCOPE-EDIT-DENIED']
    return []
```

This preserves `skill://godspeed` → `SCOPE-EDIT-DENIED`, URL → `SCOPE-FETCH-DENIED`, local-but-undeclared → `SCOPE-EDIT-DENIED`, and restores `SCOPE-PATH-DENIED` for dot-segment/traversal/selector/internal-URI spellings; it also reinstates D4's defense-in-depth for free. Alongside it, three one-line-scoped items: (a) decide D2 — drop the exact seat-key-set clause to match the draft, or keep it and document it in the file docstring plus a benign-extra-key fixture, and state why v1 seats are exempt; (b) restore the draft's `v1-forged-row-marker-no-grant` fixture so the v1 forgery invariant stays pinned; (c) restore the v2 docstring paragraph and correct the expected selftest aggregate from `cases: 108` to the landed fixture count (109 as landed; recompute after the fix). No change is needed to the flag provenance, the exit ladder, the `structured_edit_mode` rules, or any v1 path.

## Residual risk and verification gaps

1. **Nothing was executed** (NO-EXEC). Every exit/ID above is a static reading of both files, not an observed run. L1 must run the landed copy's `--selftest` and confirm `PASS, failed: 0` with the corrected case count, and run the C2 command from the production path.
2. **Producer compatibility for D2 is unverified here**: the round-23 `bindings.json` consumed by the C2 command is outside this seat's read paths. If any seat carries a field outside the 7-key set, the landed tool returns `CANNOT_EVALUATE` and the C2 metric reads 0 — a wave-visible failure mode with no in-tool explanation. This is the single highest-impact residual risk and is cheap to check with one command.
3. **C1↔C2 coupling could not be read**: `tools/check-edit-contract.py` and `sources/edit-decision-policy.json` are outside this seat's read paths, so I cannot confirm whether the C1 checker keys on `SCOPE-PATH-DENIED` for traversal probes. If it does, D1 is a mis-scoring defect on the C1 axis (`validated_edit_decisions` would under-count rows 6 and 7), not merely an audit-fidelity defect; if it does not, D1 is cosmetic-to-moderate. Severity of D1 is stated on the conservative reading and should be re-graded against that file.
4. **Production identity / same-identity rerouting unverified**: the candidate copy resolves `ROOT = .../round-23/candidate` (`parents[1]`), whereas the production copy at `tools/…` resolves `ROOT` to the repository root. `git -C ROOT` resolves to the same repository either way, but `_revision.bind(ROOT, rev, branch)` is handed `ROOT` and is ROOT-sensitive by construction; the two copies were never run side by side (NO-EXEC). No other copy of the tool was searched — the seat scope forbids extra filesystem search, so "no other copy exists" is not claimed.
5. **No semantic index available**: see Method. Absence claims here are scoped to the two bound files.

## Blockers

None. (Gaps 2 and 3 above are undeclared-path reads this seat may not perform; they are reported as gaps, not improvised around.)

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxdraftexeceditaudit
Scope: executed=none
