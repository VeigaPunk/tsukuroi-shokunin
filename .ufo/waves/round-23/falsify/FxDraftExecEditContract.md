# FxDraftExecEditContract — falsification report (tsukuroi round23 attempt1, FALSIFY wave)

Seat: `TsukuroiR23-2.FxDraftExecEditContract-2` (leaf; no subagents dispatched).
Post-build review from integrated landed state `5a25c88b77f52e940bcad87825c4ac1cd529470d`; baseline `ae01e50f582016384e620022be38bf5367000e2e`.

## 0. What was read, and what was not

Landed target (supplied identity, **not** recomputed — no hashing, listing, wc, import, compile, test or lint was performed; seat scope is NO-EXEC/NO-FETCH):

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-edit-contract.py` (283 lines, read in full).
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/worktrees/ExecEditContract/draft/check-edit-contract.py` (360 lines, read in full) — the independent wave-1 draft by seat `ExecEditContract`.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/ExecEditContract.md` (draft's own build report).
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/preregister.json` (C1 claim, `edit_decisions`, sources).
- `skill://godspeed` and the round-23 copy of the directive.

**Not readable under this seat's binding** (and therefore unverified — see §7): `corpus/knowledge/structured-edit-r23.json`, `corpus/knowledge/structured-edit-r23.md`, `corpus/SOURCES.md` at the landed revision, `.ufo/waves/round-23/sources/structured-edit-observations.json`, `.ufo/waves/round-23/sources/edit-decision-policy.json`, `tools/_revision.py`.

Axes named for this seat: **A1** decision fidelity, **A2** finding-id/disposition taxonomy, **A3** control strength (evidence / source / prose / preregister), **A4** metric + payload contract, **A5** selftest coverage. All findings below are static-reading findings with literal cases; nothing was executed.

## 1. Headline

The **subject matter of C1 is identical on both sides**. The eight decision tuples `(id, decision, reason, evidence, policy)`, the `LIMIT` scope sentence, the `SOURCES.md` S086 row grammar (exactly one row, 11 cells, path cell after `' — '`, cells 2:4 `own-work|A`, cell 7 `mined`, no backslash), the `visible()`/`table_cells()` Markdown carrier (byte-identical), the `unique()` duplicate-key hook, the `git_read()` revision binding, the CLI surface (`--revision` / `--branch master` / `--selftest`, mutually exclusive, exit classes 0/1/2), the decision-count metric name `validated_edit_decisions`, the "exactly one visible prose row per decision, tuple-equal" rule, and the "any non-`EDIT-DECISION-MISMATCH` finding zeroes the count" rule are **all the same on both sides**. There is **no divergence in the eight decisions themselves**.

Every divergence is in the **audit wrapped around those decisions**: the corpus document contract, the evidence audit, the finding taxonomy, the dispositions, the payload, and the selftest. On balance the landed tool is the stronger artifact on the corpus-shape and preregister axes, but it is **weaker than the independent draft on the evidence axis** (scope pinning, per-observation provenance, adapter-step validation, per-observation attribution) and it **mislabels evidence-source defects as corpus-schema defects** (§2 D6, D7).

## 2. Every semantic divergence

Notation: **L** = landed `candidate/tools/check-edit-contract.py`; **D** = wave-1 draft `worktrees/ExecEditContract/draft/check-edit-contract.py`.

### D1 — Per-row extra field is accepted by the draft, rejected by the landed tool (landed right)

- **L** (`evaluate`): `set(row) == {'id','decision','reason','evidence','policy'}` → a row with a sixth key fails `correct` → `EDIT-DECISION-MISMATCH`, exit **1**, `validated_edit_decisions` 7.
- **D**: only `tuple(row.get(k) for k in FIELDS) == expected` → extra keys are invisible.

Literal case — corpus row:

```json
{"id":"DECLARED_EDIT","decision":"ALLOW","reason":"Exact target is predeclared for edit and for both read and write","evidence":"S086","policy":"round23-preregister","enforcement":"native"}
```

- **L** → `EDIT-DECISION-MISMATCH` (site `DECLARED_EDIT`), exit 1, count 7.
- **D** → exit 0, `PASS`, count 8.

**Verdict: landed right.** The tool's own `LIMIT` sentence forbids any native-enforcement claim; a row carrying an extra `enforcement: native` field is exactly the smuggle the key-set check exists to stop. The draft's key-agnostic row acceptance is a **draft defect** (a false PASS). The landed selftest already pins this case (`extra-row-field`).

### D2 — Extra top-level key: exit 1 semantics vs exit 2, and a split disposition

- **L**: `set(data) != {'schema','decisions','source_path','scope'}` → `ValueError` → `EDIT-SCHEMA`, exit **2** (`CANNOT_EVALUATE`), site `DATA`.
- **D**: no top-level key set is checked → the same document passes, exit 0.

**Verdict: landed right on detection, wrong on disposition (low severity).** An overclaiming top-level key (e.g. `"native_enforcement": true`) is the *same class* of defect as an overclaiming `scope` string, which both sides report as exit **1** `EDIT-LIMIT-MISSING`. The landed tool splits that class across exit 1 (scope) and exit 2 (any other extra key). Smallest remedy: test the overclaim/extra-key case separately from the malformed-JSON case and report exit 1 with a dedicated id.

### D3 — Corpus document contract: two mutually exclusive schemas (unverifiable from this seat)

- **L**: `schema == 'tsukuroi-edit-policy-v1'` **and** top-level key set `{schema, decisions, source_path, scope}` **and** `source_path == EVIDENCE`.
- **D**: `schema == 'tsukuroi-edit-contract-v1'`, no top-level key set, no `source_path`.

These are mutually exclusive: a corpus entry satisfying one is rejected by the other with `EDIT-SCHEMA` exit 2. **Neither side can be declared right from this seat**, because the corpus entry is outside the read binding (§7). The literal falsifier for the landed tool is:

> read `corpus/knowledge/structured-edit-r23.json` at `5a25c88b`; if `schema != "tsukuroi-edit-policy-v1"` or `source_path` is absent, the landed tool returns exit 2 `EDIT-SCHEMA` and C1's metric can never reach 8 — C1 falsified.

**Verdict: unresolved dependency; the effective contract is whichever the landed corpus satisfies.** Note the asymmetry in the draft's own build report: the draft *transcribed* the primary source's schema string `tsukuroi-edit-policy-v1` as the primary source's identity, then invented a *different* schema string `tsukuroi-edit-contract-v1` for the corpus entry. One of the two is a guess. The landed tool's choice is at least the one co-located with the primary source's declared schema, so it is the safer default, but it must be checked against the corpus bytes.

### D4 — Evidence argument-key shapes: draft too lax, landed too rigid

- **L** (`evidence_ok`): the set of observed argument-key shapes (minus `i`) must equal exactly `{{path,stream_content},{path,old_string,new_string}}` → otherwise `EDIT-EVIDENCE`, exit 1, site `S086`.
- **D**: each observation needs a non-empty, duplicate-free, control-free key list containing `path`; **any** other keys are allowed.

Literal case — an observation with `"argument_keys": ["path","patch"]` (an opaque-patch style call):

- **L** → `EDIT-EVIDENCE`, exit 1.
- **D** → accepted; if nothing else differs, exit 0 `PASS`.

**Verdict: landed right in kind, draft wrong.** The draft's rule proves nothing about *structured* edit metadata — an observation with keys `["path","patch","body"]` passes the draft, so the word "structured" in the C1 scope is unverified. But the landed rule is over-tight in two literal ways:

1. It demands **both** declared shapes be present. A revision whose observation set records only one shape flips the audit to exit 1 with the coarse id `EDIT-EVIDENCE` and no per-observation site (landed selftest `evidence-one-shape` pins this as a *failure*, so the rigidity is intentional).
2. It rejects a legitimate opaque-patch observation — the very case the decision table names (`OPAQUE_PATCH` → `UNKNOWN`, i.e. "the target cannot be inferred from opaque patch text"). The tool refuses as *invalid evidence* a record of the case its own decision row describes.

**Verdict on the equality itself: the subset rule is the correct one.** "Every observed shape must be one of the declared structured shapes" (⊆) plus "at least one observation exists" is the correct contract; the coverage of both declared shapes is a property of the *evidence source*, not of the *tool's* validity, and belongs in the evidence author's contract, not in the audit's pass/fail. If the equality is kept, at minimum split the finding id so "unknown shape" and "declared shape not observed" are distinguishable — both exit 1, different ids — because they demand different fixes.

### D5 — Evidence scope string is not audited at all by the landed tool (draft right) — **strongest falsifier against the landed tool**

- **L** (`evidence_ok`): checks `schema`, `observations`, and per-observation fields. It **never reads the evidence file's own `scope`**.
- **D** (`audit_evidence`): `evidence_data.get('scope') != EVIDENCE_SCOPE` → `EDIT-EVIDENCE-SCOPE`, exit 1, site `S086`.

Literal case — the evidence source's scope replaced with an overclaim:

```json
{"schema":"tsukuroi-structured-edit-observations-v1","scope":"native permission enforcement proves every decision","observations":[ ...unchanged... ]}
```

- **L** → no finding; exit 0 `PASS` (assuming the corpus and SOURCES rows are clean).
- **D** → `EDIT-EVIDENCE-SCOPE`, exit 1.

**Verdict: draft right.** The landed tool pins the no-enforcement scope of the corpus JSON (`data['scope'] == LIMIT`) and of the corpus prose (the `PROSE_LIMIT` phrase) but leaves the *one third-party observation file it is auditing* unchecked for the very claim its own docstring disclaims. The landed docstring says the evidence "proves only observed metadata shapes and adapter steps; lane policy is separate" — that is a claim about the evidence file's authority, and the tool never tests the evidence file's authority statement. This is a control regression relative to the independent draft, and it is the literal falsifier I would run first.

### D6 — Evidence provenance and adapter-step validation were dropped by the landed tool (draft right)

The landed audit validates: `tool == 'edit'`, `argument_keys` shape/distinctness, `body_fields` marker, `path` prefix, `recorded_starts` non-emptiness, `transcript_sha256` 64-hex. It does **not** validate: `seat`, `agent`, `call_id`, `request_line`, and — despite the docstring naming "adapter steps" — **the content of any step in `recorded_starts`**.

The strongest literal case is the **landed tool's own selftest fixture**. The landed selftest's evidence fixture is:

```json
{"schema":"tsukuroi-structured-edit-observations-v1","observations":[
 {"tool":"edit","argument_keys":["path","stream_content"],"path":"<lane>/x/A.md","body_fields":"omitted; no report text copied","recorded_starts":[{"tool":"write"}],"transcript_sha256":"aaaa…"},
 {"tool":"edit","argument_keys":["i","new_string","old_string","path"],"path":"<lane>/x/B.md","body_fields":"omitted; no report text copied","recorded_starts":[{"tool":"edit"}],"transcript_sha256":"bbbb…"}]}
```

Run against the **draft's** auditor, these very bytes fail with `EDIT-EVIDENCE-SHAPE` (site `observations[0]`) for three independent reasons: no `scope` key at all (`EDIT-EVIDENCE-SCOPE`), no `seat`/`agent`/`call_id`/`request_line`, and steps with no positive-int `line` and no `path` (`_is_step` fails). Against the **landed** auditor they pass. Additional literal cases the landed tool accepts with exit 0: `recorded_starts: [{"tool": 5}]`; an observation with no `seat`/`agent`/`call_id`/`request_line` at all.

**Verdict: draft right.** Two distinct losses:

1. **Authority/traceability loss.** Without `seat`/`agent`/`call_id`/`request_line`, an observation cannot be attributed to the seat that made the edit call, so the audit cannot say *whose* edit was observed — the per-seat framing the round's contract language leans on. The draft's site naming (`site = obs['seat']`) exists precisely for that.
2. **Docstring/implementation contradiction in the landed tool.** `evidence_ok`'s docstring claims the audit covers "adapter steps"; the implementation only checks that `recorded_starts` is a non-empty list. A step of `{"tool": 5}` — or `{}` — is accepted as a recorded adapter step.

### D7 — Raised evidence errors are misreported as corpus-schema errors (draft right)

Any exception raised inside the landed `evidence_ok` propagates to the outer `except (ValueError, TypeError, KeyError, UnicodeError, AttributeError)`, which reports **`EDIT-SCHEMA`, site `DATA`** (the corpus knowledge JSON) and exit **2** `CANNOT_EVALUATE`.

Literal cases:

| Evidence defect | Landed result | Draft result |
|---|---|---|
| `"transcript_sha256": 12345` (present, wrong type) → `re.fullmatch` raises `TypeError` | `EDIT-SCHEMA` / site `DATA` / exit 2 | `EDIT-EVIDENCE-SHAPE` / site `observations[0]` / exit 1 |
| observation without `"argument_keys"` → `KeyError` | `EDIT-SCHEMA` / site `DATA` / exit 2 | `EDIT-EVIDENCE-SHAPE` / exit 1 |
| observation without `"path"` → `KeyError` | `EDIT-SCHEMA` / site `DATA` / exit 2 | `EDIT-EVIDENCE-SHAPE` / exit 1 |
| evidence file without `"observations"` → `KeyError` | `EDIT-SCHEMA` / site `DATA` / exit 2 | `EDIT-EVIDENCE-SHAPE` / exit 1 |
| observation without `"transcript_sha256"` (key absent → `''`) | `EDIT-EVIDENCE` / site `S086` / exit 1 | `EDIT-EVIDENCE-SHAPE` / exit 1 |

**Verdict: draft right.** The landed tool attributes evidence-source defects to the corpus knowledge file and upgrades them from FAIL(1) to CANNOT_EVALUATE(2). Two harms: (i) the finding's `site` names a file that is not at fault, so a falsification/fix round is sent to the wrong artifact; (ii) the disposition changes — an auditable failure becomes "cannot evaluate". Note the landed tool's own fifth input surface (the preregister) has the same misattribution: `json.loads(preregister, …)` raising inside the same `try` reports `EDIT-SCHEMA` / site `DATA`.

### D8 — CANNOT_EVALUATE payloads omit the C1 metric keys (draft right)

- **L**: `except _revision.RevisionError` → `payload = {'status': 'CANNOT_EVALUATE', 'findings': [...]}`; `except (OSError, RuntimeError, subprocess.TimeoutExpired)` → `{'status': 'CANNOT_EVALUATE', 'findings': [...]}`. Neither carries `validated_edit_decisions`, `total_decisions`, or `scope`.
- **D**: both error payloads carry `validated_edit_decisions: 0` and `total_decisions: 8` (still no `scope`).

**Verdict: draft right.** C1's preregistered metric *is* `validated_edit_decisions`; the metric key must exist on every payload the tool prints, otherwise the collector must special-case the two error paths (and the tool's own `evaluate` return always includes the key — the omission is an inconsistency between the success path and the error path of the same program). Smallest remedy: build both error payloads with `validated_edit_decisions=0`, `total_decisions=len(EXPECTED)`, `scope=LIMIT`. (Both sides additionally omit `scope` on error paths — a shared minor gap, included in the same remedy.)

### D9 — Prose disclaimer: two different required strings (landed accepted in kind; corpus-compatibility risk)

- **L**: `PROSE_LIMIT = 'It is not native permission enforcement'` must appear in `'\n'.join(visible(text))` → else `EDIT-LIMIT-MISSING`, exit 1.
- **D**: the **full `LIMIT` sentence** (`'Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof.'`) must appear in the visible prose → else `EDIT-LIMIT-MISSING`, exit 1.

Literal case — corpus prose ending with the `LIMIT` sentence only (no `It is not native permission enforcement` phrase):

- **L** → `EDIT-LIMIT-MISSING`, exit 1 (a correct corpus fails).
- **D** → exit 0.

And the reverse: prose with the phrase only → L passes, D fails.

**Verdict: the landed requirement is acceptable in kind** (a canonical disclaimer phrase is a weaker but more robust contract than demanding the JSON scope sentence be duplicated verbatim in prose), **but the two contracts are a hard fork on the corpus bytes** and the landed one is the effective one. Both sides share the deeper weakness in **D13**. Note also that the landed `visible()` correctly hides an HTML-commented or fenced disclaimer (landed selftest `hidden-limit` covers this) — that behaviour is identical on both sides.

### D10 — Evidence finding taxonomy: three ids collapse into one (draft right)

- **L**: every evidence problem is one id `EDIT-EVIDENCE`, site `S086`.
- **D**: `EDIT-EVIDENCE-MISSING` (site = evidence path), `EDIT-EVIDENCE-SCOPE` (site `S086`), `EDIT-EVIDENCE-SHAPE` (site = seat, or `observations[i]`).

**Verdict: draft right.** A single id cannot distinguish "the file is absent" from "the file's scope overclaims" from "observation 3 has a bad shape", and loses the per-observation site. For a falsification wave the per-seat site is the operative diagnostic.

### D11 — Preregister binding exists only on the landed side (landed right)

- **L**: reads `.ufo/waves/round-23/preregister.json` and requires `pre['edit_decisions'] == [list(e[:3]) for e in EXPECTED]` → else `EDIT-POLICY-SOURCE` (site = preregister path), exit 1. Missing preregister at the audited revision → `git_read` returns `None` → `EDIT-POLICY-SOURCE`, exit 1.
- **D**: no preregister surface at all; the authority is only the tool's own constant.

**Verdict: landed right.** The preregister carries the same eight `[id, decision, reason]` triples (verified by reading `preregister.json`: `edit_decisions` is a list of eight 3-element lists whose contents match `EXPECTED[:3]` element-for-element and in order). The draft checked that agreement once at build time only — a TOCTOU gap the landed tool closes at run time. Literal case: preregister `edit_decisions` reversed → landed exit 1 `EDIT-POLICY-SOURCE`; draft exit 0 `PASS`.

### D12 — Lane containment of evidence paths exists only on the landed side (landed right in kind, flawed in implementation)

- **L**: `row['path'].startswith(LANE)` with `LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/'`, and `'/../' not in row['path']`.
- **D**: `_text(obs.get('path'))` only — no lane containment, no traversal test.

**Verdict: landed right in kind** (an observation of an out-of-lane edit target does not evidence this lane's structured-edit authority), **but the implementation has two literal defects**:

1. **Checkout-path dependence.** `LANE` is a hardcoded absolute path although `ROOT = Path(__file__).resolve().parents[1]` is already the repo root. A checkout at any other path makes every legitimate observation fail the audit (`EDIT-EVIDENCE`, exit 1) — a false FAIL that no selftest case can catch, since the selftest fixture reuses the same constant.
2. **Incomplete traversal test.** The substring `'/../'` misses a trailing dot-segment. Literal case: `"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.."` — `startswith(LANE)` is true, `'/../'` is absent → **accepted**, yet the path resolves to `/home/vgpnk/Projects/shokunin`, i.e. **outside the lane**. The tool's own decision row `EDIT_TRAVERSAL`/`DENY` ("No dot-segment or alternate spelling expands the target list") is not reflected in the audit that checks the observed targets.

Smallest remedy: `LANE = str(ROOT).rstrip('/') + '/'` and replace the substring test with a normalized-containment test (`os.path.normpath` then `startswith(LANE)`), which rejects the trailing `..` case.

### D13 — Presence-only disclaimer checks cannot detect a contradictory claim (shared weakness)

Both sides test only for the *presence* of a disclaimer. Literal case — corpus prose containing **both** the negative disclaimer and an affirmative claim:

```
It is not native permission enforcement. Native runtime enforcement of edit targets is in force.
```

- **L** → the `PROSE_LIMIT` phrase is present → no finding → exit 0 `PASS`.
- **D** → the `LIMIT` sentence is present → no finding → exit 0 `PASS`.

**Verdict: neither side is right; shared gap.** The C1 scope sentence ("no native enforcement") is therefore not enforced against a document that asserts enforcement in the same breath. Smallest deterministic remedy (both sides): additionally forbid two affirmative literals in the visible prose and in the JSON scope — `'native runtime enforcement'` and `'runtime enforcement of'` — chosen so they cannot match the `LIMIT` sentence (which reads "no native prevention").

### D14 — Selftest metric assertions: landed asserts the count only for the clean case

- **L**: `ok = code == expected_code and (expected_id is None or expected_id in ids) and (expected_code != 0 or result['validated_edit_decisions'] == 8)` — the count is asserted **only** when the expected exit is 0.
- **D**: additionally asserts `validated_edit_decisions == 7` for a table-mismatch case and `== 0` for three non-mismatch-finding cases.

**Verdict: draft right.** The landed selftest cannot detect a regression in the "any non-`EDIT-DECISION-MISMATCH` finding zeroes the count" rule, nor in the partial-count path (e.g. a change that keeps `count` at 8 on a single-row table mismatch would still pass the landed selftest). Smallest remedy: assert `7` for one table-mismatch case and `0` for one `EDIT-SOURCE`/`EDIT-EVIDENCE` case.

### D15 — Selftest coverage: the landed selftest drops the draft's cases

Present in the draft, absent from the landed selftest: `missing-row`, `indented-duplicate`, `evidence-malformed`, `evidence-schema-swap`, `evidence-shape-path-key`, `json-scope-omitted`, malformed-JSON, and a **ninth unique row** (the landed selftest covers duplicate ids but not an extra unique row). The landed selftest also has no case for the missing control `EDIT-EVIDENCE-SCOPE` (D5) and no case that asserts the *absence* of extra finding ids (both sides only assert membership of the expected id).

**Verdict: draft's coverage is the better set** (all literal, all cheap); port the missing cases into the landed selftest, including the new evidence-scope case.

### D16 — Argparse failure prints nothing (shared gap)

`argparse` with no arguments (the mutually exclusive group is `required=True`) raises `SystemExit(2)`; `main` catches it and returns 2 **without printing any payload**. A machine collector therefore sees empty stdout and exit 2, indistinguishable from a crash. Identical on both sides. Smallest remedy: print a `CANNOT_EVALUATE` payload (`fid` `EDIT-ARGV`) before returning 2.

### D17 — CLI surface, exit classes, revision binding: no divergence

`--revision HEX` / `--branch master` (default) / `--selftest`, mutually exclusive; `_revision.bind` + `RevisionError` → exit 2; `git_read` via `git show` with an `ls-tree` existence probe → `None` for an absent path, `RuntimeError('committed read unavailable')` otherwise → exit 2 `EDIT-READ`; `sys.dont_write_bytecode = True` set before `import _revision`; `json.dumps(payload, sort_keys=True)`. Identical on both sides. The landed CLI matches the preregistered C1 command `python3 tools/check-edit-contract.py --revision <REV>` exactly.

## 3. Falsifiers (bounded, literal, none executed)

| # | Falsifier | Expected under the side that is wrong | Side that is wrong |
|---|---|---|---|
| **F1** | Set the evidence source's `scope` to `"native permission enforcement proves every decision"`, everything else clean | **L: exit 0 `PASS`** (no finding); D: exit 1 `EDIT-EVIDENCE-SCOPE` | landed (D5) |
| **F2** | Evidence observation with `"transcript_sha256": 12345` | **L: exit 2 `EDIT-SCHEMA`, site `DATA`**; D: exit 1 `EDIT-EVIDENCE-SHAPE` | landed (D7) |
| **F3** | Evidence observation with `"recorded_starts": [{"tool": 5}]` | **L: exit 0 `PASS`** (steps never inspected, despite the docstring); D: exit 1 `EDIT-EVIDENCE-SHAPE` | landed (D6) |
| **F4** | Evidence observation stripped of `seat`/`agent`/`call_id`/`request_line` | **L: exit 0 `PASS`** (no provenance required, no per-seat site); D: exit 1 `EDIT-EVIDENCE-SHAPE` | landed (D6, D10) |
| **F5** | Corpus decision row carrying a sixth key `"enforcement":"native"` | **D: exit 0 `PASS`**; L: exit 1 `EDIT-DECISION-MISMATCH` | draft (D1) |
| **F6** | Corpus document with a fifth top-level key `"native_enforcement": true` | **D: exit 0 `PASS`**; L: exit 2 `EDIT-SCHEMA` | draft (D2) |
| **F7** | Evidence observation with `"argument_keys": ["path","patch","body"]` | **D: exit 0 `PASS`** (nothing structured is proven); L: exit 1 `EDIT-EVIDENCE` | draft (D4) |
| **F8** | Evidence observation path `"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.."` | **L: exit 0 `PASS`** (escapes the lane, `'/../'` test misses it); D: exit 0 as well (no lane check at all) | both (D12) — landed's control is real but incomplete; draft has none |
| **F9** | Prose containing both the negative disclaimer and "Native runtime enforcement of edit targets is in force." | **L: exit 0 `PASS`**; D: exit 0 `PASS` | both (D13) |
| **F10** | Corpus entry with `"schema": "tsukuroi-edit-contract-v1"` (the draft's contract) | **L: exit 2 `EDIT-SCHEMA`**; D: exit 0 | pending corpus bytes (D3) |
| **F11** | Preregister `edit_decisions` reordered | **D: exit 0 `PASS`**; L: exit 1 `EDIT-POLICY-SOURCE` | draft (D11) |

**Bounded search that found none.** Reading both files end to end, the following are *identical* and were checked line by line: the eight `EXPECTED` tuples and their reasons; `LIMIT`; the `visible()` and `table_cells()` carriers; `unique()`; `git_read()`; the CLI/exit-class convention; the decision-vs-prose comparison rule (`matches == [list(expected)]`); the count-increment rule; the count-reset rule; `total_decisions == 8`; the `SOURCES.md` S086 grammar; the `LIMIT`/`PROSE_LIMIT` string constants' roles; the `--selftest` literal-fixture principle (both build fixtures from literals, not from `EXPECTED`). No divergence was found in the decision table itself, in the corpus-source grammar, in the carrier, in the binding, or in the metric name. The divergence is confined to §2.

## 4. Attacked claim

**C1** — *"Eight finite source-grounded structured-edit authority decisions; new document contract, not eight repaired runtime behaviors."* Metric `validated_edit_decisions` 0 → 8; command `python3 tools/check-edit-contract.py --revision <REV>`; axis `depth`.

Not attacked: **C2** (explicit schema-v2 edit audit authority) and **C3** (path-census ledger) — neither is reachable from this seat's read binding, and this report makes no claim about them. **Frontier**: not attacked.

Claim-level statement of what the falsification found: the C1 *payload* (the eight decisions) is confirmed identical between the independent draft and the landed tool, so C1's substance is **not** falsified. What is falsified is the landed tool's *audit authority* over its own evidence source: F1–F4 show the landed tool can return `PASS` (count 8) on an evidence source that overclaims native enforcement, that carries no per-observation provenance, and whose "adapter steps" are never inspected, and it misattributes evidence-source crashes to the corpus file with exit 2. That is an overstatement of audit authority in exactly the direction the round forbids (never claim runtime enforcement, never claim native restriction).

**Authority caveat carried forward:** both tools audit *declarations* only. Neither enforces anything natively; the round has no native restrictive task toolset. Any C1 report must say "declared audit authority over structured target metadata", not "edit targets are enforced".

## 5. Smallest in-scope remedy (landed tool is the canonical artifact; the draft is superseded)

Ordered by severity, each a localized edit to `tools/check-edit-contract.py`:

- **R1 (D5, high)** — pin the evidence source's own scope. Add `EVIDENCE_SCOPE` (the string the observations file itself declares, per the draft report) and require `data.get('scope') == EVIDENCE_SCOPE` inside `evidence_ok`; emit `EDIT-EVIDENCE-SCOPE`, site `S086`, exit 1. Add the matching selftest case (F1). *Smallest change that restores the lost control.*
- **R2 (D6, D7, high)** — give the evidence audit its own error boundary and its own ids: wrap the evidence parse/audit so any raised exception yields `EDIT-EVIDENCE-SHAPE` (site `S086`) at exit 1, never `EDIT-SCHEMA` at site `DATA`; split `EDIT-EVIDENCE` into `EDIT-EVIDENCE-MISSING` / `EDIT-EVIDENCE-SCOPE` / `EDIT-EVIDENCE-SHAPE`.
- **R3 (D6, medium)** — restore the draft's per-observation validation: require `seat`, `agent`, `call_id` (non-empty, control-free), `request_line` (positive int, bool rejected), and validate every `recorded_starts` entry (dict, int `line` ≥ 1, non-empty control-free `tool` and `path`). Use the observation's `seat` as the finding site. *(This also removes the landed selftest fixture's own shape violations — the fixture must be updated accordingly.)*
- **R4 (D12, medium)** — derive `LANE` from `ROOT` (`str(ROOT).rstrip('/') + '/'`) and replace the `'/../'` substring test with normalized containment (`os.path.normpath`), which rejects a trailing `..`.
- **R5 (D8, D16, medium)** — include `validated_edit_decisions=0`, `total_decisions=len(EXPECTED)` and `scope=LIMIT` in both CANNOT_EVALUATE payloads; print a CANNOT_EVALUATE payload on argparse failure instead of returning 2 silently.
- **R6 (D4, medium)** — replace the shape-set equality with "every observed shape must be one of the declared structured shapes" (⊆, not =), and if the coverage of both declared shapes is to remain a hard requirement, give it its own finding id so the diagnostic says which of the two obligations failed. Keep `EDIT-EVIDENCE-SHAPE` for an unknown shape. *(The landed selftest case `evidence-one-shape` must be re-pinned to match the chosen rule.)*
- **R7 (D9, D13, low-medium)** — decide the prose disclaimer contract once (the landed phrase is acceptable) and add the affirmative-literal prohibition from D13; state the corpus requirement explicitly in the C1 knowledge-author instructions so the corpus prose and the tool agree.
- **R8 (D14, D15, low)** — port the draft's missing selftest cases (`missing-row`, `indented-duplicate`, `evidence-malformed`, `evidence-schema-swap`, `evidence-shape-path-key`, `json-scope-omitted`, extra unique row) and add the metric assertions (`7` for a table mismatch, `0` for a non-mismatch finding); assert absence of unexpected finding ids in at least the clean case.
- **R9 (D2, D10, low)** — give the corpus overclaim/extra-key case exit 1 rather than exit 2, and give the evidence ids per R2.
- **R10 (draft side, only if revived)** — adopt the landed per-row and top-level key sets, the preregister binding, the shape pinning and the `source_path` check; drop the draft's key-agnostic row acceptance (F5–F7).

## 6. Residual risk

1. **Corpus compatibility is unverified from this seat (highest residual risk).** Four literals must line up with the landed corpus bytes or C1 cannot reach 8: `schema == "tsukuroi-edit-policy-v1"`; top-level key set `{schema,decisions,source_path,scope}`; `scope == LIMIT` exactly; and the prose containing `It is not native permission enforcement` verbatim. The draft's competing literals (`tsukuroi-edit-contract-v1`, `LIMIT`-sentence-in-prose) would each fail the landed tool. Until the corpus bytes are read, C1's metric outcome is unproven on either side.
2. **The evidence source's real shape is unverified.** R1 and R3 need the observations file's actual `scope` string and its actual per-observation field set; the draft's report asserts them, this seat could not read the file. If the committed file lacks `seat`/`agent`/`call_id`/`request_line` or uses a different scope sentence, R1/R3 as written would fail a legitimate source — the remedy must be pinned to the file's real bytes, not to the draft's recollection.
3. **The lane prefix.** If the recorded observation paths are not under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`, the landed audit fails a legitimate file today, and R4's `ROOT`-derived lane does not help (the recorded paths are absolute from the recording machine). A future re-record under a different root would need a relative-path normalisation rule.
4. **Payload asymmetry survives until R5.** Any collector reading `payload["validated_edit_decisions"]` must currently special-case the two error paths.
5. **Declaration-only authority.** Even after R1–R9, C1 proves that a document *declares* the eight decisions, that the evidence source *declares* a bounded observation scope, and that the SOURCES row is well-formed. It proves nothing about effects, reads, or native enforcement — and the round has no native restrictive toolset to appeal to. Reports must not drift into enforcement language.
6. **Static review only.** No tool was executed; every claim above is from reading the two sources. The landed selftest's 68 cases and the draft's 38 cases were traced by hand for internal consistency (I traced the landed `clean` fixture to exit 0/count 8 and each mutation case to its expected id and exit); a hand trace is not an execution.

## 7. Verification gaps (could not be closed from this seat)

- `corpus/knowledge/structured-edit-r23.json` at `5a25c88b` — `schema`, top-level key set, `source_path`, `scope`. **Needed to settle D3.**
- `corpus/knowledge/structured-edit-r23.md` at `5a25c88b` — presence of `It is not native permission enforcement`, presence of one visible 5-cell row per decision. **Needed to settle D9 and to confirm C1's metric can reach 8.**
- `corpus/SOURCES.md` at `5a25c88b` — the single 11-cell S086 row. Both tools require it; unverified here.
- `.ufo/waves/round-23/sources/structured-edit-observations.json` — its `scope` string, per-observation field set, `recorded_starts` step shape, and absolute path prefixes. **Needed to pin R1/R3/R4.**
- `.ufo/waves/round-23/sources/edit-decision-policy.json` — the primary source the draft transcribed; the landed tool does not read it at run time (neither does the draft).
- `tools/_revision.py` — `_revision.bind` / `RevisionError.fid` / `clean_env` semantics used by both mains; treated as shared infrastructure per the preregister's "separability" note.
- Execution of either tool (`--selftest`, `--revision <REV>`): not performed — NO-EXEC seat scope.
- The declared SHA256 of the landed tool is a **supplied identity**, not an independently computed one; no hashing, listing, counting, importing, compiling, testing, linting or formatting was performed. No tool installation was performed (this seat's narrower NO-EXEC/NO-FETCH scope forbids installations; nothing was needed).

## 8. Bottom line

The independent wave-1 draft and the landed tool agree on every one of the eight C1 decisions, on the corpus-source grammar, on the carrier, on the binding and on the metric name; the divergence is entirely in the surrounding audit. The landed tool is the stronger artifact on corpus shape (D1, D2) and on preregister binding (D11), and it carries one genuine control regression against the draft — the evidence source's own scope is never audited (D5) — plus three further evidence-axis losses (provenance and step validation dropped, D6; raised evidence errors misattributed to the corpus and re-dispositioned to exit 2, D7; one coarse finding id instead of three with per-observation sites, D10), a metric-key omission on both error paths (D8), an incomplete and checkout-path-dependent lane/traversal control (D12), and weaker selftest assertions and coverage (D14, D15). The falsifier set is F1–F11 above; the smallest in-scope remedy set is R1–R10. C1's *substance* is not falsified by this seat; C1's *audit authority over its evidence source* is.

Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-fxdraftexeceditcontract
Scope: executed=none
