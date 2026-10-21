# FxC1Prereg — falsification review of the C1 preregistration binding

Reviewed target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-edit-contract.py`
(reviewed against the integrated landed state `5a25c88b77f52e940bcad87825c4ac1cd529470d`, wave baseline `ae01e50f582016384e620022be38bf5367000e2e`).
Declared SHA256 `620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081` is treated as supplied identity: not computed, not listed, not executed.
Method: static read of the seven declared files only. No command, import, hash, test or lint was run; no fetch of any kind. Every result below is a code-reading trace and is labelled accordingly.

---

## 1. Attacked claim

**C1** (`depth`, metric `validated_edit_decisions`, before 0 → target 8) and, specifically, the preregistration binding that C1 rests on:

> the eight structured-edit authority decisions are *preregistered* in `.ufo/waves/round-23/preregister.json` (`edit_decisions`), and the gate `tools/check-edit-contract.py` compares the knowledge decisions against that preregistration.

Two sub-claims were attacked separately:

- **C1.a** — the `edit_decisions` comparison is *exact* for order, case and extra rows.
- **C1.b** — *a later preregister edit cannot silently move the target.*

C1's own preregistered scope is in `preregister.json` → `claims[0]`:
`{"id":"C1","axis":"depth","metric":"validated_edit_decisions","before":0,"target":8,"command":"python3 tools/check-edit-contract.py --revision <REV>"}`.

**Outcome: C1.a survives the bounded search; C1.b is falsified outside `edit_decisions`** (four concrete holes below, F1–F4). The gate is a declared *audit* artifact only; nothing here is native runtime enforcement, and no seat should read it as such.

---

## 2. The binding, as actually implemented

`evaluate()` in the reviewed tool contains exactly one preregister check:

```python
pre = json.loads(preregister, object_pairs_hook=unique) if preregister is not None else None
declared = pre.get('edit_decisions') if isinstance(pre, dict) else None
if declared != [list(e[:3]) for e in EXPECTED]:
    add('EDIT-POLICY-SOURCE', PREREGISTER)
```

Two facts follow from the code, not from intent:

1. **The preregister is never compared to the corpus.** The corpus (`corpus/knowledge/structured-edit-r23.json`), the corpus prose table, and `preregister.json` are each compared *independently* against the hard-coded `EXPECTED` tuple in the tool. There are **three** copies of the eight decisions (tool constant, corpus JSON, preregister) plus a fourth (the prose table), and the tool constant is the effective authority. The preregister is a **tripwire**, not the authority.
2. **Only three of the five decision fields are bound by the preregister.** `e[:3]` binds `id`, `decision`, `reason`. The corpus rows' `evidence` (`S086`) and `policy` (`round23-preregister`) fields are pinned only by `EXPECTED`, never by the preregister.

The preregister is read at the **same revision** as everything else (`git_read(binding.sha, PREREGISTER)`), so it is revision-pinned, not live-filesystem-read. That part of the binding is sound.

---

## 3. C1.a — is the comparison exact for order, case and extra rows? YES (no bypass found)

Bounded static search over every mutation axis of `edit_decisions` that reaches `declared != [list(e[:3]) for e in EXPECTED]`. Python list `!=` is element-wise `==` over ordered sequences, and `str.__eq__` is exact and case-sensitive, so:

| Mutation of `preregister.json` → `edit_decisions` | Resulting comparison | Gate outcome (trace) |
|---|---|---|
| row order permuted | ordered list compare fails | `EDIT-POLICY-SOURCE`, exit 1 — **and the tool's own selftest covers exactly this** (`policy-source-swap`, expected exit 1 / `EDIT-POLICY-SOURCE`) |
| decision value case changed (`ALLOW`→`allow`) | element-wise `!=` | `EDIT-POLICY-SOURCE`, exit 1 (logic-exact; **no selftest mutant**) |
| reason text changed | element-wise `!=` | `EDIT-POLICY-SOURCE`, exit 1 (no selftest mutant) |
| 9th row appended (extra row) | length differs | `EDIT-POLICY-SOURCE`, exit 1 (no selftest mutant) |
| row shortened/lengthened (extra field in a row) | element-wise `!=` | `EDIT-POLICY-SOURCE`, exit 1 (no selftest mutant) |
| `edit_decisions` replaced by a dict / non-list | `!=` against list | `EDIT-POLICY-SOURCE`, exit 1 |
| key removed | `pre.get(...)` → `None` | `EDIT-POLICY-SOURCE`, exit 1 |
| duplicate `edit_decisions` key in JSON | `unique()` raises `ValueError` | caught → `EDIT-SCHEMA`, exit 2 |
| preregister file absent at bound revision | `git_read` → `None` | `declared=None` → `EDIT-POLICY-SOURCE`, exit 1 (loud) |
| preregister not a JSON object | `isinstance(pre, dict)` false | `declared=None` → `EDIT-POLICY-SOURCE`, exit 1 |

**Bounded search result: no bypass found.** Every deviation of `edit_decisions` — order, case, value, extra row, extra field, missing key, wrong type, duplicate JSON key, absent file — produces a non-zero exit and a named finding. The `!=` comparison cannot be satisfied by a reordered, re-cased, extended or retyped preregister.

Two honest caveats on that verdict:

- The **executed** evidence for exactness is the tool's own selftest, and it covers only **two** of these axes: order reversal and absence (`policy-source-swap`, `policy-source-missing`). Case mutation, extra row, extra field, changed reason and wrong type are **not** selftest mutants (F5).
- The corpus side is *stricter* than the preregister side in one respect and *looser* in another: the corpus JSON enforces exactly eight unique ids and an exact 5-key row shape, but its **row order is free** (`by_id` mapping), whereas the preregister's order is pinned. That asymmetry is defensible (the preregister is a sequence, the corpus is a set), but it means "order-exact" is a property of the preregister, not of the corpus.

---

## 4. C1.b — can a later preregister edit silently move the target? YES — four surfaces

The gate binds exactly one field of `preregister.json`: `edit_decisions`. Everything else the preregister asserts — the claim block that *defines the target*, the declared baseline, the schema identity, the limits — is read by nobody in this tool. Each of the following is a **silent** move: the gate's output is byte-identical before and after, and it still reports `{"status":"PASS","validated_edit_decisions":8,"total_decisions":8}`.

### F1 (medium-high) — the preregistered C1 *target* is unbound; the metric is duplicated, never cross-checked

`preregister.json` → `claims[0]` states `metric: "validated_edit_decisions"`, `before: 0`, `target: 8`, `axis: "depth"`, `command: "python3 tools/check-edit-contract.py --revision <REV>"`. The tool independently hard-codes the metric name `'validated_edit_decisions'` and `len(EXPECTED) == 8`. **No statement in the reviewed file compares the two copies.** `pre['claims']` is never read.

Consequence: a later preregister edit that rewrites `claims[0]` — `target: 8 → 4`, `metric: "validated_edit_decisions" → "denied_decisions"`, `before: 0 → 8`, or a swapped `command` — is completely invisible. The gate keeps printing `validated_edit_decisions: 8` while the preregistered target now reads 4. The number the wave reports as C1's achieved metric and the number the preregister calls the target can drift apart with **no signal at all**.

This is the direct answer to the attack question: **the `edit_decisions` tripwire holds, but the tripwire is not on the field that defines the target.**

### F2 (medium) — the validated preregister bytes are never reported; the live file can drift from them silently

The payload is `{status, validated_edit_decisions, total_decisions, findings, scope, revision, branch, branch_tip}`. It carries **no digest and no content of the preregister it compared**, nor of `DATA`, `PROSE`, `SOURCES` or `EVIDENCE`. The gate validates the **committed blob at the bound revision**; the wave-level `preregister.json` that seats, prompts and humans read is the **working-tree file**. Nothing binds the two, and the PASS payload cannot be used to tell which bytes were compared.

So: after the landed state is recorded, editing the live `preregister.json` (or leaving it edited while re-running the gate at the old revision) yields a PASS payload indistinguishable from the unedited run. The gate is revision-pinned — good — but it does not *report* what it pinned, so a reader cannot detect the divergence. (This is not a bypass of the eight decisions; it is an unbindable report of the binding itself.)

### F3 (medium) — extra decision rows in the corpus prose pass the gate

`evaluate()` computes `matches = [r for r in cells if r and r[0] == ident]` **only for the eight `EXPECTED` ids**, and requires `matches == [list(expected)]` per id. It never constrains the rest of the prose table. A prose file that keeps all eight rows exactly and **adds a ninth decision row** with a new id (e.g. `| NATIVE_ENFORCE | ALLOW | ... | S086 | round23-preregister |`) is reported as `PASS`, `validated_edit_decisions: 8`.

The corpus JSON cannot do this (strict 8-unique-id + exact key-set check) and the preregister cannot do this (length-exact list). The **prose — the human-readable artifact that states the lane's edit authority — is the one surface where the declared decision set can be widened without a finding.** That is exactly the "silently move the target" shape, one layer below `edit_decisions`.

### F4 (medium-low) — the preregister's baseline, schema and the corpus's provenance pointers are all unbound

- `pre['baseline']` (`ae01e50f582016384e620022be38bf5367000e2e`) is never read by the gate. A later edit re-pointing the declared baseline compiles to a different commit and the gate is silent.
- `pre['schema']` (`tsukuroi-round23-preregister-v1`) is never read. The corpus knowledge JSON is strict about its own `schema` (`tsukuroi-edit-policy-v1` must be exact); the preregister's schema is not checked at all.
- The corpus rows' `policy` cell is the literal `round23-preregister`. **That identifier resolves to nothing checkable**: no artifact in the reviewed set is keyed by it (the preregister's own schema string is `tsukuroi-round23-preregister-v1`). The policy pointer is verified only against the tool's own constant, i.e. it is self-referential.
- The prose's own provenance line (`source: S086 — .ufo/waves/round-23/sources/structured-edit-observations.json`, `policy: .ufo/waves/round-23/preregister.json edit_decisions`) and its `source snapshot baseline ae01e50f...` sentence are **not checked at all** — the prose could point at a different evidence file or a different baseline and still pass.

Net: the *preregistration* is enforced only where the tool happens to look. The wave's claim that these decisions were fixed in advance rests on commit/creation order and on the diff, not on a mechanism.

---

## 5. Additional defects found while tracing (lower severity)

- **F5 (low) — selftest coverage gap.** `selftest()` mutates the preregister in exactly two ways: order reversal and `None`. The specific properties the attack asks about — **case** exactness and **extra rows** — are asserted by my trace but are **not** selftest mutants, so the tool's own executed evidence does not establish them. Neither are: extra field in a preregister row, changed reason text, preregister as a dict, extra prose decision row (F3), `pre['baseline']`/`pre['schema']` mutation (F4).
- **F6 (low) — `--help` exits 0 with no payload.** `main()` does `except SystemExit as exc: return 0 if exc.code == 0 else 2`. argparse's `--help`/`-h` exits 0, so `python3 tools/check-edit-contract.py --help` returns **exit status 0 with no JSON on stdout**. A harness that keys on exit status alone would score that as a pass with no measurement. (Unknown-argument and missing-required-argument paths correctly return 2.)
- **F7 (low, diagnosability) — "absent at revision" and "content mismatch" share one finding id.** `git_read()` returns `None` both for "path not tracked at this revision" and for "path is a tree", and `evaluate()` maps `None` and a mismatching list to the same `EDIT-POLICY-SOURCE` / site `PREREGISTER`. If the wave's preregister is not tracked in git at the bound revision, the operator gets a finding indistinguishable from a benign content edit. Loud, but undiagnosable.
- **F8 (low) — the evidence packet is less strict than the knowledge packet.** `evidence_ok()` requires `schema` and `observations` but does **not** assert a key set, while the knowledge JSON does (`set(data) != {'schema','decisions','source_path','scope'}` → `EDIT-SCHEMA`). A later edit could add a field such as `native_enforcement` to `structured-edit-observations.json` and the gate would not notice. (`evidence_ok` does correctly reject body text, unknown argument keys, out-of-lane paths, `/../`, wrong tool and non-64-hex transcript digests.)

---

## 6. Landed-state spot checks (facts read, not executed)

Read-only verification of the candidate bytes the gate would compare. Each is a fact about the files, not a claim that the gate was run.

- `corpus/knowledge/structured-edit-r23.json` — top-level key set is exactly `{schema, decisions, source_path, scope}`; `schema` = `tsukuroi-edit-policy-v1`; `source_path` = `.ufo/waves/round-23/sources/structured-edit-observations.json`; `scope` string is byte-equal to the tool's `LIMIT`; eight decisions, ids unique, each row exactly the five keys `id/decision/reason/evidence/policy`, and every field byte-equal to the corresponding `EXPECTED` entry (`evidence` = `S086`, `policy` = `round23-preregister`). → the corpus side of the binding should hold.
- `corpus/knowledge/structured-edit-r23.md` — the decision table has exactly the eight expected rows in the expected cell content; the limit sentence `It is not native permission enforcement` is present in visible prose; the table header/separator rows do not collide with any decision id.
- `corpus/SOURCES.md` — exactly **one** row whose first cell is `S086` (line 93); it has 11 cells; cell 1 ends with ` — .ufo/waves/round-23/sources/structured-edit-observations.json`; cells 2–3 are `own-work` / `A`; cell 7 is `mined`; no cell contains a backslash. → the `EDIT-SOURCE` check should not fire. (The `S085` row mentions `S086` inside its own cell, but its first cell is `S085`, so it does not enter the `found` set.)
- `.ufo/waves/round-23/sources/structured-edit-observations.json` — four observations, all `tool: "edit"`, all `body_fields` = `omitted; no report text copied`, all paths under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/` with no `/../`, all `transcript_sha256` 64-hex; the two observed shapes are `{path, stream_content}` and `{path, old_string, new_string}` → `evidence_ok` should hold.
- `.ufo/waves/round-23/preregister.json` — `edit_decisions` is an eight-element list of three-element lists whose contents and order are byte-equal to `[list(e[:3]) for e in EXPECTED]`. → `EDIT-POLICY-SOURCE` should not fire on content grounds.

**Landed-state provenance pointers are consistent**: corpus JSON `source_path`, prose header `source:` line, and the S086 registry cell all name the same evidence file; the prose `policy:` line names the same preregister file I read. No same-identity rerouting found among the four artifacts.

**One cross-seat note (not my claim to close):** the S086 row's `used-by` cell names `corpus/lessons/round-23.md`. Existence of that path is outside my declared read scope and is unverified here — flagging it for the C3 path-census seat rather than asserting it.

---

## 7. Smallest in-scope remedies

Ordered by how much of the "silent move" surface each closes. All are edits to the reviewed tool only; none require new evidence, a new source, or native capability.

1. **Bind the claim block (closes F1, the real hole).** In `evaluate()`, compare the preregister's C1 claim to constants — `id == 'C1'`, `axis == 'depth'`, `metric == 'validated_edit_decisions'`, `before == 0`, `target == 8` — and add a distinct finding id (e.g. `EDIT-CLAIM-BINDING`) instead of silently accepting drift. Smallest form: one equality test plus one finding id.
2. **Report what was compared (closes F2).** Add the SHA-256 of the compared `preregister`, `DATA`, `PROSE` and `EVIDENCE` bytes to the payload (hash the in-memory bytes; no external command, no new dependency), plus the resolved git root. Then a working-tree/committed-blob divergence is visible in the receipt instead of invisible.
3. **Pin the preregister's own identity (closes part of F4).** Assert `pre.get('schema') == 'tsukuroi-round23-preregister-v1'` and `pre.get('baseline') == 'ae01e50f582016384e620022be38bf5367000e2e'` (both already present in the file), and make the corpus's `policy` cell resolvable — either point it at the preregister path, or derive `POLICY` from the preregister instead of hard-coding `round23-preregister`.
4. **Enforce exactly eight prose decision rows (closes F3).** Locate the table whose header row is exactly `['ID','Decision','Reason','Evidence','Policy']` and require its body to be exactly the eight expected rows (set equality + count 8), so a ninth decision row cannot be added without a finding.
5. **Extend the selftest to cover the attacked axes (closes F5).** Add mutants for: preregister decision case change; preregister ninth row; preregister row with an extra field; preregister changed reason; preregister as a dict; preregister `baseline`/`schema` mutation; extra prose decision row. Each must exit non-zero with its expected finding id. This turns my static trace into executed, tool-owned evidence — which is what the "exact for order, case and extra rows" claim actually needs.
6. **Never exit 0 without a payload (closes F6).** Return `2` on argparse `SystemExit`, or print a `CANNOT_EVALUATE` payload before returning.
7. **Distinguish absence from mismatch (closes F7).** Give `git_read`'s `None` its own finding id (e.g. `EDIT-PREREGISTER-ABSENT`) so "not tracked at this revision" is separable from "content changed".
8. **Optional (F8).** Assert `set(data) == {'schema','accessed','observations','scope'}` in `evidence_ok()`, matching the knowledge packet's strictness.

Remedies 1–4 are the ones that materially close the "a later preregister edit silently moves the target" surface; 5–8 are hardening and diagnosability.

---

## 8. Residual risk and verification gaps

- **Nothing was executed.** This review is a static trace of the reviewed file plus four reads of the candidate bytes. The tool's own selftest — the only executed evidence — covers only order reversal and preregister absence, so the **case** and **extra-row** verdicts in §3 are my code-reading conclusions, not tool-observed results. Remedy 5 is what converts them.
- **`_revision.bind` semantics are unverified.** Whether the binding enforces ancestry against the preregister's declared baseline, and how a stale `--branch` tip is handled, could not be read (`_revision.py` is outside my declared read scope). The payload's `branch_tip` field hints at a staleness check; unconfirmed.
- **Git-root resolution is unverified.** `ROOT` is the `candidate/` directory and every path in the tool is git-root-relative. If `candidate/` is its own git root, then `.ufo/waves/round-23/preregister.json` must exist in the committed candidate tree; if it is not, the paths resolve against the enclosing `tsukuroi-shokunin` repository and the wave-level files I read are the ones compared. I could not probe `.git` presence (undeclared path, no execution). Either way the outcome is loud — `git_read` returning `None` yields `EDIT-POLICY-SOURCE`, exit 1 — so this is a reachability risk for C1's target, not a silent-pass risk.
- **The prose limit check is presence-only.** `PROSE_LIMIT not in '\n'.join(visible(text))` proves the required sentence is present; it cannot detect a contradicting over-claim elsewhere in the prose. The prose's own QUALITY section is the mitigation, and it is honest — but the gate cannot falsify it.
- **The "Policy" identifier is dangling** (F4): `round23-preregister` names no artifact key that the gate resolves, so the policy column is self-referential rather than externally anchored.
- **No native enforcement is claimed or implied anywhere in this review.** The gate is a declared, post-hoc, structured-metadata auditor; the corpus prose and the tool's `LIMIT` string both say so, and this report asserts no more.

**Verdict:** C1.a (exactness of the `edit_decisions` comparison) survives the bounded search with no bypass found. C1.b (a later preregister edit cannot silently move the target) is **falsified**: the tripwire is on `edit_decisions` only, while the preregistered target itself (`claims[0].metric/before/target`), the preregister's baseline and schema, the reported identity of the compared bytes, and the exact row count of the corpus prose table are all unbound — F1 is the concrete falsifier (rewrite `claims[0].target` and the gate's PASS output is unchanged), F3 is the second (add a ninth prose decision row and the gate still reports eight validated decisions). The smallest in-scope remedy is remedy 1 (one comparison against the C1 claim block), followed by remedy 5 so the exactness claim is backed by executed tool-owned mutants rather than by review reading.

  Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
  Predicate: r23f-fxc1prereg
  Scope: executed=none
