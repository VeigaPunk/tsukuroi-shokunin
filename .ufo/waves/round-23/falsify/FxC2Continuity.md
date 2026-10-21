# FxC2Continuity — r23 falsify wave, C2 v1-continuity attack

Seat: FxC2Continuity (leaf reviewer, no subagent dispatch).
Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-seat-bindings.py`
Declared identity (supplied, NOT computed by me): SHA256 `4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6`.
Baseline for the comparison: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py` (the v1 file, 310 lines).
Method: read-only, line-by-line textual comparison of the two files plus grep-anchored structural diffing. **NO-EXEC / NO-FETCH**: no bash, eval, subprocess, import, compile, test, lint, hash, wc or delegation was performed. Every verdict below is by inspection, not by execution. The digest was not independently computed. Godspeed directive was read from the copied local file `.ufo/waves/round-23/sources/godspeed-directive.txt` (the declared `skill://godspeed` path was not fetched).

Attacked claim: **C2** (`axis: operability`, `metric: structured_edit_mode`, before 0 → target 1), specifically its sub-claim *"legacy schema-v1 policy and historical reds unchanged"*, and the C2 metric's own honesty.

---

## 1. Findings by severity

### F1 — MEDIUM — `--selftest` stdout contract drift: the existing `cases` key silently changes meaning (73 → 110)

- Snapshot `tools/check-seat-bindings.py:266` prints:
  `json.dumps({'status': ..., 'cases': len(cases), 'failed': failed, 'observations': observations})`
  → stdout object keys = `{status, cases, failed, observations}`; `cases` = **73** (the v1 control count); every entry of `observations` is a 4-key dict `{case, exit, ids, pass}`.
- Candidate `tools/check-seat-bindings.py:352` prints:
  `json.dumps({'status': ..., 'cases': len(observations), 'v1_cases': len(cases), 'v2_cases': len(v2_cases), 'failed': failed, 'observations': observations})`
  → stdout object keys = `{status, cases, v1_cases, v2_cases, failed, observations}`; `cases` = **110** (total observations), and the v1 count moved to the new key `v1_cases` = 73.
- The `observations` array is now **heterogeneous**: 73 v1 entries `{case, exit, ids, pass}` (candidate `:343`, textually identical to snapshot `:264`) followed by 37 v2 entries `{case, exit, ids, mode, pass}` (candidate `:349`).
- Count derivation (by enumeration of the `case(...)` / `cases.append` / `cases.extend` / `v2case(...)` call sites, no execution): v1 = **73** controls (snapshot `:183`–`:258` = candidate `:218`–`:293`, constant +35 offset, byte-identical text); v2 = **37** (candidate `:301`–`:337` = 6 direct + 9 spelling-loop iterations at `:307` + 6 + 2 + 1 + 2 + 7 + 4). `cases` therefore reports 110 at runtime.
- Why it matters: a v1-era consumer that asserts `selftest['cases'] == 73`, or that requires a uniform observation-entry key set, now fails or silently mis-reads the same key. This is a *self-check harness report* change, not a change to the v1 **audit** output (see §2 — the audit result JSON for a v1 manifest is unchanged). The claim C2 asserts "legacy schema-v1 policy and historical reds unchanged"; the audit policy and the historical reds *are* unchanged, but a v1 self-check report key is not.
- Evidence that the blast radius is currently small but nonzero: `.ufo/waves/round-23/candidate/.ufo/waves/round-23/measure/l1-mutation.json` records the mutation harness consuming only the **exit code** and a `PASS`/`FAIL` string per mutant (`"selftest": "FAIL"`, `"exit": 1`), never the `cases` value. So the landed r23 harness is unaffected; the risk is for any other/future consumer of the selftest stdout.
- Smallest in-scope remedy (one token, in `selftest()` only): restore the v1 meaning of `cases` and expose the new aggregate under a new key —
  `'cases': len(cases), 'total_cases': len(observations), 'v1_cases': len(cases), 'v2_cases': len(v2_cases)`.
  If a uniform observation shape is also wanted, add `'mode': None` to the v1 observation dict at candidate `:343` — but that itself changes the v1 observation shape, so it is *not* the minimal fix and is not recommended under a strict "v1 unchanged" reading.

### F2 — LOW — selftest exit status now couples the v1 and v2 control suites

- `failed = sum(not o['pass'] for o in observations)` (candidate `:351`; snapshot `:265`) is computed over the **combined** observation list, so a v2-only regression turns the historically-v1 self-check into exit 1, and vice versa.
- The v1 control suite can no longer be isolated from the exit code alone. It *is* recoverable from the payload (the 73 v1 entries keep their `pass` flag and remain the first 73 elements of `observations`), so this is a coupling, not a loss of information.
- Remedy (optional, same `selftest()` scope): also emit `'failed_v1'` / `'failed_v2'` (or a per-suite `status`) so the v1 suite's own status is directly readable. Not required for C2 to hold.

### F3 — LOW (calibration honesty, C2 metric) — `structured_edit_mode` is a schema-presence flag, numerically identical to the pre-existing `request_audit_mode`

- Candidate `:199-206`: `result['request_audit_mode'] = int(code != 2)` and, for v2 manifests only, `result['structured_edit_mode'] = int(code != 2)` — the **same expression**. The new key is present iff the manifest schema string is `tsukuroi-seat-bindings-v2` (`v2 = isinstance(data, dict) and data.get('schema') == 'tsukuroi-seat-bindings-v2'`, candidate `:144`).
- Consequence: the C2 metric (before 0 → target 1) measures *"a v2-schema manifest was evaluated"*, not *"structured edit authority was exercised"*. A v2 manifest with **zero** edit requests still yields `structured_edit_mode = 1`. The key carries no information beyond `request_audit_mode` + the manifest's schema string.
- This is consistent with the preregister's own framing (`C2.scope`: "New explicit schema-v2 audit authority for exact predeclared structured edit targets"), so it is not a false claim, but any report that says "structured_edit_mode = 1" as evidence that edits were audited would overstate. The v2 *behaviour* is genuinely exercised by the tool's own v2 controls (candidate `:301`–`:337`), so the capability claim stands; only the production metric is coarse.
- Remedy (optional, in `evaluate()`): if the metric is meant to evidence authority *use*, gate it on the presence of at least one evaluated `edit` event rather than on schema presence, e.g. `structured_edit_mode = int(code != 2 and any_edit_event_seen)`. If it is meant to stay a schema marker, the build report must not present it as "edits audited".

### F4 — INFO — the `v2_cases` bucket contains two v1-schema controls, and those two are the ones that kill the v1-continuity mutants

- Candidate `:334` (`v1-extra-edit-field-no-grant`) and `:335` (`v1-edit-continuity`) are v1-**schema** manifests hosted in the `v2_cases` list. So `v2_cases` = 37 overstates the v2-specific count (35 are v2-specific; 2 are v1-continuity controls), and the true v1-schema assertion count is 73 + 2 = 75.
- These two are load-bearing for the v1 claim: per `l1-mutation.json`, mutant 0 (`if tool == 'edit' and allow_structured_edit:` → `if tool == 'edit':`) and mutant 9 (`== 'tsukuroi-seat-bindings-v2'` → `.startswith('tsukuroi-seat-bindings-v')`) are both reported killed; by inspection, each is killed **only** by the v1-continuity controls (mutant 0 by `:335`, which then reaches `classify_edit` on a v1 binding and diverges from the expected `SCOPE-TOOL-UNKNOWN`; mutant 9 by `:334`/`:335`, which would otherwise see `structured_edit_mode` present in a v1 result).
- Label nit only; no behavioural change. Noted so the `v2_cases` number is not quoted as "37 v2 controls" without the caveat.

### F5 — INFO (positive finding, no defect) — a v1 manifest cannot acquire edit authority by adding a field

This is the strongest positive continuity result and it is *load-bearing*, not incidental:

- `allow_structured_edit` is set **only** at candidate `:186` (`classify(event.get('tool'), event.get('args'), binding, allow_structured_edit=v2)`), and `v2` is derived **only** from the top-level manifest schema string (`:144`). No seat field, no event field, no row marker can raise it. The `classify` docstring states this contract explicitly (`:62-65`).
- A v1-schema manifest that carries an extra `edit_paths` seat key is **accepted** (the `if v2:` authority block at `:156-162` is skipped for v1) but **inert**: `edit` still falls through to `SCOPE-TOOL-UNKNOWN` at `:78-79`, exactly as in the snapshot (`:72-73`). Pinned by candidate `:334`.
- A v2-schema seat carrying a forged `allow_structured_edit` marker is rejected wholesale by `set(seat) != {...}` (`:159`) → `SCOPE-SCHEMA` → exit 2. Pinned by candidate `:331`.
- `classify_edit` is unreachable from any v1 code path. Pinned by candidate `:335` and by mutant 0 being killed.

### F6 — INFO (observation, cross-referenced, not this seat's axis) — a v2 manifest with any extra seat key is CANNOT_EVALUATE, not a targeted finding

`set(seat) != {'name','root','read_paths','write_paths','edit_paths','commands','fetches'}` (`:159`) makes *any* unexpected seat key — including a benign metadata key — fail the whole manifest with `SCOPE-SCHEMA` / exit 2, rather than producing a per-seat finding. This is strict and intentional (it is what makes the "no forged marker" property in F5 hold), but it converts a benign schema drift into a total evaluation failure for the wave. Flagged to the C2 authority reviewer (FxC2Mode / FxC2Recursion) rather than resolved here.

---

## 2. The v1 audit path is unchanged — line-by-line diff result

Method: full raw read of both files, then a region-by-region comparison, with grep-anchored line numbers as an independent check of the region boundaries.

| Region | Snapshot | Candidate | Verdict |
|---|---|---|---|
| Module docstring, imports, `sys.dont_write_bytecode`, `import _revision` | `:1-17` | `:1-17` | **identical** (offset 0) |
| `ROOT`, `LANE`, `SCOPE` constants | `:15-17` | `:15-17` | **identical** — `SCOPE` string unchanged, so every v1 result still carries the same scope disclaimer |
| `unique()`, `controls()`, `local()`, `repo_path()`, `requested_path()` | `:20-58` | `:20-58` | **identical** (offset 0) |
| `classify()` signature | `:61` `classify(tool, args, binding, depth=0)` | `:61` `classify(tool, args, binding, depth=0, allow_structured_edit=False)` | new 5th parameter, **default `False`** → all existing positional/keyword call sites keep v1 behaviour; 4th positional (`depth`) is untouched |
| `classify()` body — exec/fetch denial, unknown-tool, arg-shape, parallel recursion, path allowlist | `:62-107` | `:62-113` | **identical** apart from the inserted branch below and the added `allow_structured_edit` argument forwarded to child recursion (`:89`) |
| *(new)* structured-edit branch | — | `:76-77` | `if tool == 'edit' and allow_structured_edit: return classify_edit(args, binding)` — inserted **after** the exec/fetch denials and **before** the unknown-tool fallback, and gated on the flag, which is `False` for every v1 manifest ⇒ v1 `edit` still yields `SCOPE-TOOL-UNKNOWN` (`:78-79`), as in snapshot `:72-73` |
| *(new)* `EDIT_SHAPES` + `classify_edit()` | — | `:116-130` | new symbols; reachable only via the gated branch above |
| `evaluate()` — manifest/trace parse, `unique()` duplicate-key rejection | `:117-122` | `:141-147` | v1 identical except two added lines: `v2 = False` (`:140`) and `v2 = isinstance(data, dict) and data.get('schema') == 'tsukuroi-seat-bindings-v2'` (`:144`) |
| `evaluate()` — schema acceptance | `:119` `data.get('schema') != 'tsukuroi-seat-bindings-v1'` | `:146` `data.get('schema') not in ('tsukuroi-seat-bindings-v1','tsukuroi-seat-bindings-v2')` | **widened, not weakened**: a v1-schema manifest is accepted exactly as before; a v2-schema manifest is newly accepted (this is the intended C2 change). No v1 manifest changes status |
| `evaluate()` — seat identity/root/allowlist + read/write path validation | `:123-131` | `:148-155` | **identical**; the v1 path still has no seat key-set restriction, as in the snapshot |
| *(new)* v2 edit-authority block | — | `:156-162` | guarded by `if v2:` — **never executes for a v1 manifest** |
| `evaluate()` — trace schema, seat/agent identity, event loop, finding ids, `violations` accounting, `code` computation | `:132-162` | `:163-194` | **identical** (constant +31/+32 offset); same finding ids `SCOPE-SCHEMA`, `SCOPE-PATH-DENIED`, `SCOPE-EXEC-DENIED`, `SCOPE-FETCH-DENIED`, `SCOPE-TOOL-UNKNOWN`, `SCOPE-TRACE-MISSING`, `SCOPE-TRACE-INCOMPLETE`, `SCOPE-BINDINGS-MISSING`; same exit-code rule (`:194`) |
| `evaluate()` — `except` path (`SCOPE-SCHEMA`/`input`, `code = 2`, `bound = locals().get('bound', {})`) | `:163-166` | `:195-198` | **identical** |
| `evaluate()` — returned result object | `:167-172` (inline literal) | `:199-204` (`result = {...}`) | **same 11 keys, same values, same semantics** for a v1 manifest: `status, request_audit_mode, seats_bound, requests_total, violations, incomplete_seats, missing_seats, present_incomplete_seats, seats, findings, scope`. `main()` emits `json.dumps(result, sort_keys=True)` in both files, so the v1 audit stdout is byte-identical |
| `evaluate()` — `manifest is None` early return | `:114-115` | `:137-138` | **identical**, including the deliberately reduced key set (no `violations`/`seats`) |
| *(new)* `structured_edit_mode` | — | `:205-206` | emitted **only** `if v2:` ⇒ absent for every v1 manifest, exactly as in the snapshot |
| `selftest()` — v1 fixture + the 73 v1 control cases | `:177-258` | `:212-293` | **byte-identical** (constant +35 offset across the whole block); same names, same expected exit codes, same expected finding ids, same order |
| `selftest()` — v1 observation construction & pass rule | `:259-265` | `:338-343` | **byte-identical**: `{'case','exit','ids','pass'}` and `pass = code == expected and all(item in ids for item in required)` |
| *(new)* v2 fixture + 37 v2 controls + v2 observation loop | — | `:294-337`, `:344-350` | new; the v2 loop adds the stricter `(expected != 0 or not ids)` non-vacuity rule and the `mode_ok` check — applied **only** to v2 cases |
| `selftest()` — printed summary | `:266` | `:352` | **CHANGED** — see F1 |
| `git_read()` | `:270-278` | `:356-364` | **identical** |
| `main()` — argparse, defaults (`--branch master`, `--manifest .ufo/waves/round-22/build/bindings.json`, `--events .ufo/waves/round-22/build/events.json`), exit codes, `json.dumps(result, sort_keys=True)` | `:280-306` | `:366-392` | **identical**; the r22 v1 defaults are unchanged, so an r22-era invocation still audits a v1 manifest with unchanged output |
| file length | 310 | 396 | +86 = 6 (`classify`) + 17 (`EDIT_SHAPES`/`classify_edit`) + 9 (`evaluate` v2) + 2 (`structured_edit_mode`) + 44 (v2 controls) + 8 (v2 observation loop/print) — accounted |

### The 73 v1 controls, individually

Enumerated from the shared block (snapshot `:183`–`:258` ≡ candidate `:218`–`:293`): `clean-read`, `qualified`, `selector`, `skill`, `write-exact`, `bash`, `eval`, `task`, `fetch-https://example.invalid`, `fetch-HTTPS://EXAMPLE.INVALID/:1-5`, `fetch-http://127.0.0.1/`, `fetch-localhost:9222/`, `web_search`, `browser`, `browser.navigate`, 9 × `path-*` (`-extra`, `/child`, `/../sibling/file`, `/x/../source`, `/./source`, `source`, `xd://tool`, `artifact://a`, `/**`), 3 × `write-*` (`.extra`, `/child`, `/production`), `semicolon`, `unknown`, `bad-args`, `parallel-exec`, `parallel-fetch`, `parallel-local`, `parallel-malformed`, `missing-trace`, `incomplete`, `duplicate`, `unknown-seat`, `empty-trace`, `nonempty-fetch-allowlist`, `missing-manifest`, `duplicate-json-key`, `read-write-only`, `write-read-only`, `qualified-write`, `skill-write`, `skill-other`, `skill-selector`, `extra-argument`, `qualified-parallel`, `null-exec-args`, `mixed-parallel`, `incomplete-exec`, `malformed-before-exec`, `duplicate-bound-path`, `duplicate-bound-name`, `bad-bound-name`, `duplicate-valid-json`, `duplicate-trace-name-only`, `grep-nonvacuity`, `glob-nonvacuity`, `semicolon-first-denied`, `grep-selector`, `linear-invalid-selector`, `double-slash`, `extra-url-key`, `fetch-with-extra-key`, `nested-exec`, `depth-exhausted`, `foreign-root`, `nonempty-commands`, `actual-null-exec-args`, `trace-sidecar` = **73**, unchanged in name, order, expected exit and expected finding id.

All 73 execute against **v1-schema** manifests (the `binding` fixture is `tsukuroi-seat-bindings-v1`; `missing-manifest` passes `None`; `duplicate-json-key` and `duplicate-valid-json` fail to parse/reject before any schema is honoured), so `v2` is `False` for every one of them and the entire v1 code path — the path proven textually identical in §2 — is the one under test. **No v1 control's expected outcome can have changed.** (No execution was performed; this is an inspection verdict.)

### Bounded search that found no other v1 change

I searched the candidate for every v1-visible surface and found no further divergence: (a) all `SCOPE-*` finding ids in the candidate are the snapshot's seven ids plus the new `SCOPE-EDIT-DENIED` (candidate `:129`), which is emitted only from `classify_edit`, i.e. only on the v2 path — so no new id can appear in a v1 result; (b) the `local()` / `repo_path()` / `requested_path()` path predicates are byte-identical, so v1 path spelling decisions (selectors, `skill://godspeed`, URL forms, dot segments, `;` splitting, control characters) are unchanged; (c) the CLI surface, defaults and exit codes of `main()` are byte-identical; (d) `git_read()` and the `_revision` binding call are unchanged, so the same revision-resolution semantics apply; (e) the v1 audit result object has the same 11 keys with the same values, and `main()` sorts keys, so the v1 audit stdout is byte-identical.

---

## 3. Cross-check against the landed r23 v2 manifest

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/bindings.json` is `"schema": "tsukuroi-seat-bindings-v2"` with 60 seats, each carrying `name`, `root` (= `LANE`), `read_paths`, `write_paths`, `edit_paths`, `commands: []`, `fetches: []`.

- Every seat's `edit_paths` entries are literal `LANE`-prefixed paths, are also present in the same seat's `read_paths` and `write_paths`, and are not `skill://godspeed` — so the v2 authority rule at candidate `:156-162` is satisfied by the landed manifest as written (checked by inspection of all 60 seats).
- `commands` and `fetches` are empty for every seat (grep for non-empty `commands`/`fetches` in the manifest: no matches), so the v1 identity/root/allowlist rule at `:149` also holds.
- Seat names match `[A-Za-z0-9][A-Za-z0-9._-]{0,127}` and are unique.
- This seat's own binding conforms to the same rule: its `edit_paths` entry (`…/round-23/falsify/FxC2Continuity.md`) is present in both its `read_paths` and its `write_paths` — the literal per-seat v2 binding is narrower than the generic role defaults, as the contract requires.

---

## 4. Residual risk and verification gaps

1. **No execution.** All verdicts are by textual inspection. The one claim I could not execute is F1's runtime value (`cases` = 110) and the survival of the 73 v1 controls under the candidate. A single `python3 tools/check-seat-bindings.py --selftest` on the candidate, compared against the snapshot's `--selftest`, would close this; it was not run because this seat is NO-EXEC.
2. **Digest not computed.** `4e00ab1f…` is treated as supplied identity only; I did not hash the file.
3. **`_revision` module not compared.** The candidate's `import _revision` resolves to `candidate/tools/_revision.py`; that path is **not** in this seat's declared `read_paths`, so I could not verify that the candidate and snapshot `_revision.py` are identical, nor that `_revision.bind` semantics are unchanged. The C2 command's revision binding is shared infrastructure per the preregister's `separability` clause, so this is expected to be out of my scope — but it is an unverified dependency of the v1 result's `revision`/`branch`/`branch_tip` fields.
4. **Landed-copy identity unverified.** I did not verify that the candidate copy is byte-identical to the authored draft `.ufo/waves/round-23/worktrees/ExecEditAudit/draft/check-seat-bindings.py` or to the committed revision `5a25c88b77f52e940bcad87825c4ac1cd529470d`; that path is outside my declared read set and the digest is supplied, not computed.
5. **Falsify-wave bindings not inspected.** `.ufo/waves/round-23/falsify/bindings.json` and the falsify `events.json` are outside my declared read set, so I could not check whether the falsify wave's v2 manifest satisfies the authority rule at `:156-162`. If a falsify seat declares an `edit_paths` entry that is not also in its `read_paths` and `write_paths`, the whole falsify-wave manifest evaluates to `SCOPE-SCHEMA` / exit 2 and `structured_edit_mode` would be 0, not 1.
6. **No runtime enforcement is claimed anywhere.** The tool's own `SCOPE` string (`:17`) still says *"Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness."* Nothing in this report asserts native enforcement; the preregister `limits` ("No native per-seat restrictive tool interface exists") stands.
7. **F3's remedy would change the metric definition** and is therefore a decision for the L1 planner, not a unilateral edit: `structured_edit_mode` as a schema marker is consistent with the preregister wording; changing it to an evidence-of-use marker would alter the C2 metric's meaning and require a preregister alignment.

---

## 5. Verdict

- **C2 v1 continuity holds for the audit path.** The v1 evaluation semantics — every finding id, exit code, result key, path predicate, and the 73 v1 controls — are unchanged; the v2 machinery is confined to a schema-gated branch that a v1 manifest cannot reach, and a v1 manifest cannot acquire edit authority by adding a field (F5).
- **One v1-observable change exists, in the self-check report only:** the `cases` key of the `--selftest` stdout changed from 73 to 110 and the v1 count moved to a new `v1_cases` key, with a now-heterogeneous `observations` array (F1, MEDIUM). The smallest in-scope remedy is one token in `selftest()`: keep `'cases': len(cases)` and publish the aggregate as `'total_cases'`.
- **Secondary:** the selftest exit status now couples v1 and v2 suites (F2, LOW, recoverable from the payload); the C2 metric `structured_edit_mode` is numerically identical to `request_audit_mode` and evidences schema presence rather than authority use (F3, LOW, decision for L1); the `v2_cases` bucket holds 2 v1-schema controls (F4, INFO); a v2 manifest with any extra seat key fails wholesale (F6, INFO, cross-referenced to the C2 authority reviewers).
- **Falsifier offered for F1:** compare the stdout object of `python3 tools/check-seat-bindings.py --selftest` between the snapshot and the candidate — the key sets differ (`{status,cases,failed,observations}` vs `{status,cases,v1_cases,v2_cases,failed,observations}`) and `cases` differs (73 vs 110). If an operator requires the v1 self-check report to be byte-identical, that comparison is the falsifier; the remedy above restores it.

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2continuity
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
