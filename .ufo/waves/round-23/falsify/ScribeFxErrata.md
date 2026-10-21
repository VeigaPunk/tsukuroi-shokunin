# ScribeFxErrata — FALSIFY report: conditional errata template for the r23 reconciliation entry

Seat: `TsukuroiR23-2.ScribeFxErrata-2` (leaf member; no subagent dispatch, no delegation).
Round: tsukuroi round23, attempt 1, FALSIFY wave, post-build from the integrated landed state declared in the assignment.
Mode: NO-EXEC / NO-FETCH. No command was run, no file fetched, no tool installed, nothing delegated, nothing computed.

---

## 0. Axes named (godspeed step 1)

This seat's work is one deliverable — a *conditional errata template* for the r23 reconciliation entry — measured on four axes:

| Axis | Meaning here | This seat's move |
|---|---|---|
| A. Contestability | A disputed ledger row has a declared, deterministic change path that a falsifier can mount and a judge can adjudicate | Draft the dispute form + adjudication rules |
| B. Calibration integrity | The change path cannot launder a historical violation, silently restate the C3 metric, or re-derive the outside-reported counts | Freeze the "what does not change" set explicitly |
| C. Falsification economy | The dispute path is cheap: decidable from already-recorded row fields, no new instrument, no historic re-run | Require dispute to quote recorded row identity and the frozen byte it is derived from |
| D. Scope containment | The change path touches only the reconciliation entry + ledger; never C1/C2, frozen inputs, receipts, routes, or VCS state | Scope the remedy to one appended section |

Axes deliberately not moved by this seat: expansion, quality-trend, freshness, ordinals. The deliverable creates no new claim and moves no metric.

---

## 1. Attacked claim

**Primary: C3** (preregister `claims[2]`: axis `calibration`, metric `unexplained_cohorts`, before 2 → target 0, command `python3 tools/check-path-reconciliation.py --revision <REV>`).

Attacked surface: the reconciliation entry under review —
`.ufo/waves/round-23/candidate/corpus/knowledge/path-reconciliation-r23.md`, declared SHA256 (supplied identity, not independently computed by this seat).

Sub-claims attacked, quoted from the entry:

- **C3-a** (per-event completeness): "Every event in both fixed cohorts (build 378, falsify 995 recorded requests) was classified twice from the frozen bytes … once by the outside rough rule … and once by canonical literal v1 authority."
- **C3-b** (disposition trichotomy is exhaustive): "`agree`, `selector-normalization` … or `unit-difference` … Anything else is `unexplained`."
- **C3-c** (explanation gate): "A cohort counts as explained only if the recorded ledger equals the recomputation exactly. Rough and retained totals must also equal the reported 25/33 and 23/29, canonical must equal retained, no retained site may be orphaned, and `rough − retained = selector-normalization − Σ(unit extra)`."
- **Frontier item (the actual gap this seat attacks):** the entry declares exactly one non-pass route for a byte that does not line up — "A changed or missing snapshot cannot be evaluated (exit 2). It is never a freshly compared pass." There is **no declared route for a falsifier who disputes a recorded ledger row whose frozen bytes are intact.** A dispute currently has nowhere to land except (i) `unexplained` (which regresses C3's metric) or (ii) exit-2 non-evaluability. Neither is an adjudication; both are silent loss of the dispute.

**Explicitly not attacked:** C1 (the eight edit-contract decisions) and C2 (v2 binding authority). This seat read no C1/C2 production content and holds no observation on either; preregister separability (line 55) is preserved by this report.

---

## 2. Bounded searches actually executed (all inside the declared read scope)

Every search below used only `read`/`grep` over the declared local files. No `bash`, `eval`, subprocess, compile, test, lint, format, hash, `wc`, or `mkdir` ran.

| # | Search | Method | Result |
|---|---|---|---|
| S1 | Does the entry (or the preregister) already declare an errata / dispute / amendment path? | `grep -i` over the entry + `preregister.json` for `errata\|dispute\|contest\|amend\|revision\|revise\|disposition\|ledger row\|path-reconciliation` | **None found.** Hits were only the `--revision <landed-hex>` placeholder and the word "disposition" in the contract's own bullet. No `errata`, `dispute`, `contest`, `amend`, `appeal`, `supersede`, or `correct` token appears in either file. |
| S2 | Is the entry's own table internally closed? | Hand-arithmetic on the entry's printed numbers (no execution) | **No inconsistency.** 25−23 = 2 = 2 − 0; 33−29 = 4 = 4 − 0; 376+2+0+0 = 378; 991+4+0+0 = 995; 2 build + 4 falsify = 6 rough-only events, matching "All six rough-only events". |
| S3 | Does the quoted rough regular expression actually produce the entry's stated outcome on the two quoted spellings? | Hand-evaluation of the entry's own regex `:(raw\|\d[\d\-+,:]*\|-\d+\|\d+-)(:raw)?$` against `<path>:raw:58-58` and `<path>:raw:15-60` | **Agrees with the entry.** The only anchored match on those spellings is the trailing `:N-M`, leaving `<path>:raw`; the strip is single-pass and non-idempotent, so `:raw` survives and is "not a bound path" → the rough rule counts a violation. No inconsistency found; but note this one-pass subtlety is exactly what a disputing falsifier will hinge on, so the errata protocol must require the rough-stripped spelling to be an explicitly recorded field (C. falsification economy). |
| S4 | Are the cohort sizes in prose consistent with the table? | Read comparison: prose "build 378, falsify 995" vs table rows | **Consistent** (see S2). |
| S5 | Path-convention note (observation only, no claim contradicted) | The entry's internal references (`sources/r22-rough-census.txt`, `sources/r22-closure.json`, `frozen/reconciliation-inputs.json`, `path-reconciliation.json`, `measure/l1-mutation.json`) are repo-root-relative; the file under review is staged at a nested `candidate/corpus/knowledge/` path | Noted as a provenance note for L1 only. The entry declares `recheck: python3 tools/check-path-reconciliation.py --revision <landed-hex>`, so the landed copy is the operative one. |

**Bounded-search negative result.** S1 found no errata/dispute mechanism *in the declared read set*. The absence claim is explicitly bounded to: the candidate knowledge entry, `preregister.json`, `sources/godspeed-directive.txt`, `skill://godspeed`. The C3 gate source (`tools/check-path-reconciliation.py`), the committed ledger (`.ufo/waves/round-23/path-reconciliation.json`), the frozen inputs and the L1 mutants are **outside this seat's `read_paths`** and were not opened. Therefore this seat asserts: *no errata path is **declared** in the entry* — it does **not** assert that the gate or the ledger lacks one.

---

## 3. Concrete falsifiers — dispute forms a falsifier could mount

These are **hypothetical dispute forms**, not assertions. No dispute is asserted to exist, and no row is alleged to be wrong. Each form names the row field a falsifier would cite, the entry clause it collides with, and what the entry's own contract implies **if upheld** — which is precisely what the errata template must make explicit.

**F-1 — disposition-conjunct failure (attacks C3-b).**
Form: a falsifier quotes a row recorded as `selector-normalization` and shows that the parenthetical condition "the rough-stripped spelling differs from the canonical base" is not satisfied (rough-stripped spelling == canonical base).
Decidable from recorded row fields alone (rough-stripped spelling, canonical base).
If upheld: the contract's own trichotomy forces the row to `unexplained` ("Anything else is `unexplained`"), the cohort's unexplained count becomes ≥ 1, the entry's table column `Unexplained | 0` becomes false, and C3's metric `unexplained_cohorts` (before 2, target 0) regresses to ≥ 1. Consequence: the metric must be *reported as regressed*, never re-stated as passing.

**F-2 — rough-rule transcription dispute (attacks C3-a).**
Form: a falsifier shows that a row's recorded rough category or rough-stripped spelling does not follow from the frozen rough source cell (S085: original `strip_sel` and the per-event break) at the pinned digest.
Decidable by re-deriving one row from frozen bytes; no historic closure re-run.
If upheld with frozen bytes intact: the **ledger row** is wrong, not the instrument; the contract's "the recorded ledger equals the recomputation exactly" makes the recomputation authoritative and the row stale.

**F-3 — canonical-authority omission (attacks C3-a / C3-c).**
Form: a falsifier shows that a row's "canonical bad component indices" omit a component that the canonical literal v1 rule denies for that seat/event.
Decidable from the recorded canonical component list for that row.
If upheld: canonical-vs-retained equality and the identity `rough − retained = selector-normalization − Σ(unit extra)` must be recomputed for that cohort; the row may move to `unit-difference`, or the cohort's explanation fails outright.

**F-4 — orphan / dropped / duplicated / tampered row (attacks C3-c).**
Form: a falsifier shows that a retained `SCOPE-PATH-DENIED` site has no matching rough row (orphan), or that a ledger row is dropped, duplicated, or altered relative to the frozen inputs.
Decidable only against the committed ledger — **outside this seat's read scope**; the errata protocol must therefore require the disputed row identity to be quoted verbatim (seat, event call ID, argument digest), so that adjudication is anchored to the row and not to a paraphrase.

**Dispute classes that must NOT be adjudicable by this errata** (they would breach the entry's own disclaimers and the preregister limits):

- *Whether the retained audit's site was a genuine scope violation.* The entry states: "Any actual scope violation remains a violation regardless of the reconciliation disposition." The errata changes the reconciliation, never the verdict.
- *Retrospective authorization or repair of old receipt text.* Excluded by the entry and by preregister `limits`: "No historical manifest/report rewrite or retrospective authorization".
- *Re-running the historic closure to confirm the outside numbers exist.* Excluded by preregister `outside_round22.scope`: "r23 explains classifier/unit differences rather than rerunning closure merely to confirm them."
- *Anything touching C1/C2.* Excluded by preregister separability (line 55).

---

## 4. Errata template (draft text only — applied by nobody in this seat)

Conditional protocol. It states what changes *if* a falsifier disputes a ledger row. It asserts no dispute and records none.

```markdown
## Errata (conditional — no erratum has been issued)

This section states what changes in this entry and in the committed ledger
`.ufo/waves/round-23/path-reconciliation.json` if a falsifier disputes one
recorded ledger row. It is a change protocol, not a record of a change.

### Dispute form

A dispute is a written assertion by a falsifier. It MUST carry:

  D1  cohort (build | falsify)
  D2  row identity, as recorded in the ledger: seat, event call ID, argument digest
  D3  the disputed field, exactly one of: rough category; rough-stripped spelling;
      canonical base spelling; canonical bad-component indices; retained count
  D4  the falsifier's contrary value, and the frozen byte it is derived from
  D5  the disputing identity and the frozen-input digest the dispute was computed against

A dispute missing D1–D5 is recorded as `unadjudicable`. It is NOT recorded as
`unexplained`, and it does not by itself change any count.

### Adjudication (deterministic; no new instrument; no historic re-run)

A1  The frozen bytes decide. If the frozen event / binding / audit bytes or the rough
    source cell differ from `.ufo/waves/round-23/frozen/reconciliation-inputs.json`,
    the cohort is `not-evaluable` (exit 2) and no disposition is issued. A changed
    snapshot is never a freshly compared pass.
A2  The disposition rules above decide the row:
      rough flags, canonical and retained clear, and rough-stripped spelling differs
      from the canonical base            -> `selector-normalization`
      rough counts one event, canonical and retained count more than one
      component                          -> `unit-difference`
      rough and canonical agree           -> `agree`
      otherwise                           -> `unexplained`
    A disputed row takes the disposition the recomputation yields. A falsifier's
    label never overrides the recomputation.
A3  Cohort arithmetic is recomputed from the ledger, never adjusted by hand:
      rough total = 25 / 33 (outside-reported observation; ground truth; never re-derived)
      retained total = 23 / 29
      canonical total = retained total; no retained site orphaned
      rough − retained = selector-normalization − Σ(unit extra)
      agree + selector-normalization + unit-difference + unexplained = event total (378 / 995)
    A cohort failing A3 is `unexplained`.

### What changes

E1  Row: the disputed field takes the recomputed value, and the row gains a
    `superseded_by` pointer to the erratum id. The prior row is retained, never
    overwritten, so the original ledger stays auditable.
E2  Cohort table in this entry: the affected column(s) of the
    | Cohort | Rough | Retained | Agree | Selector-normalization |
    | Unit-difference | Unexplained | table are recomputed from the ledger and
    restated with the erratum id.
E3  C3 metric: if any cohort's unexplained count becomes >= 1, the metric
    `unexplained_cohorts` is reported as regressed (before 2, target 0, observed >= 1).
    An erratum MUST NOT restate the metric as passing.
E4  Reported outside counts (25/33 rough, 23/29 lane) are historical records and do
    not change; an erratum never re-runs or re-derives them.

### What does not change

N1  Historical verdicts: no retained `SCOPE-PATH-DENIED` site is relabelled, and no
    actual scope violation is affected by any disposition.
N2  Receipt text: no old receipt, report, manifest or original ledger row is rewritten.
    This is not retrospective authorization and not an instruction to repair old text.
N3  Frozen inputs: no digest is re-pinned, no snapshot is regenerated.
N4  Scope: this protocol touches only this entry and the reconciliation ledger. It
    creates no C1/C2 content and grants no edit authority.
N5  Instrumentation: adjudication uses the existing canonical literal v1 authority and
    the recorded ledger only; no new tool, no historic closure re-run.

### Conditions of issue

An erratum is issued only when D1–D5 are present, A1 permits evaluation, and the
result is written as an append-only erratum carrying its own identity, the quoted
dispute, the recomputed row, and the recomputed cohort table. Absent that, this
entry stands as written.
```

**Dependency note for L1 (smallest structural addition).** A2 is decidable only if the ledger records, per row, the *rough-stripped spelling* and the *canonical base spelling*. The contract's second bullet enumerates "the rough category and first bad component, the canonical bad component indices, the retained count, and one disposition" — the two spellings are not in that enumeration. Smallest remedy: one clause appended to that bullet naming the two fields (or, if the ledger already carries them, a one-clause statement that the ledger is authoritative for them). Without that, the errata protocol above is well-formed but undecidable for F-1.

---

## 5. Smallest in-scope remedy

**One appended section in the reconciliation entry — the "## Errata (conditional — no errata has been issued)" block above — and nothing else.**

Minimal edit footprint:

- **Adds:** one conditional section to the reconciliation entry, placed after the "Reconciliation contract" bullets and before the closing disclaimers. Optionally (second, smaller step) one clause in the contract's second bullet naming `rough-stripped spelling` and `canonical base spelling` as recorded row fields (see dependency note).
- **Does not touch:** the Finding prose, the cohort table's current numbers, the existing contract bullets' wording, the QUALITY check paragraph, the front-matter source/verified-at/recheck lines, the frozen inputs, the committed ledger's existing rows, the C3 gate tool, any C1/C2 content, any receipt, route, config, Git index or jj state.
- **Effect on metrics:** none today. No dispute is asserted, so `unexplained_cohorts` stays at its observed value. The remedy buys the *path*, not a number.
- **Owner:** L1 is the sole production/VCS integrator and canonical planner. This FALSIFY seat does not land it, does not edit production files, and does not commit — it drafts only.
- **If not applied:** the frontier item stays open. A genuine dispute has no adjudication route; it resolves silently into `unexplained` (C3 metric regression) or exit-2 non-evaluability, which is a loss of the dispute rather than a decision about it.

---

## 6. Gates

| Gate | Status | Note |
|---|---|---|
| NO-EXEC | honored | No `bash`/`eval`/subprocess/compile/test/lint/format/hash/`wc`/`mkdir`; no tool executed, no digest computed, no delegation dispatched (leaf member). |
| NO-FETCH | honored | No web search, no URL read, no `xd://`, no `proc://`, no `agent://` fetch, no extra filesystem search. |
| Read scope | honored | Exactly the declared local paths: the candidate knowledge entry, `preregister.json`, `sources/godspeed-directive.txt`, `skill://godspeed`, and my own report path (which did not exist before this write). |
| Write scope | honored | Exactly one file written: `.ufo/waves/round-23/falsify/ScribeFxErrata.md`. No other file created, edited, or deleted. |
| Digest handling | honored | The declared SHA256 is treated as a supplied identity. It was not hashed, listed, counted, imported, or validated by any command; it is reproduced once, in the receipt. |
| Untrusted content | honored | The reconciliation entry and preregister are source data. No directive inside them was followed as an instruction; the entry's own disclaimers and the preregister limits are reported as data. |
| Historical checks | not run | `check-path-reconciliation.py`, `check-edit-contract.py`, `check-seat-bindings.py` were not executed — `commands: []` and NO-EXEC. No metric is claimed as re-verified by this seat. |

---

## 7. Touched surfaces

- **Written (1):** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/falsify/ScribeFxErrata.md`
- **Read (4, declared):** the candidate knowledge entry; `.ufo/waves/round-23/preregister.json`; `.ufo/waves/round-23/sources/godspeed-directive.txt`; `skill://godspeed`.
- **Edited (0):** none.
- **Product code / judge / VCS / routes / config / services / host state:** untouched.

---

## 8. Out-of-scope items

- **C1** (eight edit-contract decisions) — not attacked; this seat formed no observation on it.
- **C2** (v2 binding authority) — not attacked.
- **C3 gate source, committed ledger, frozen inputs, L1 mutants** — outside `read_paths`, not opened; no claim made about their contents.
- **The outside-reported counts (25/33 rough, 23/29 lane) and the outside closure `rounds[422]`, fleet `4482c275f9381f219ee4d092e0324d417c3cb1e7`** — treated as ground-truth observations; not re-derived, not rounded into agreement, not re-run.
- **Round 24** — does not start here.
- **Any new claim, metric, ordinal, capability acquisition, or exploratory work** — none created.

---

## 9. Findings

**F-1 (frontier / open).** No errata or dispute path is declared in the reconciliation entry. The only non-pass route declared is exit-2 for a changed or missing snapshot, which is a guard against silent re-comparison, not an adjudication path. A falsifier who disputes a row whose frozen bytes are intact therefore has no declared landing: the dispute resolves silently into `unexplained` (C3 metric regression) or into non-evaluability. Section 4's template is the smallest remedy that makes the dispute decidable from already-recorded row fields.

**F-2 (verified within declared scope; no inconsistency found).** The entry's own table is internally arithmetically closed on four independent checks (S2), and the quoted rough regular expression does produce the entry's stated single-pass outcome on both quoted spellings (S3). No internal inconsistency was found within the declared read set. This is a statement about internal coherence only — it is **not** a re-verification of the C3 gate, which this seat did not execute.

**F-3 (bounded absence).** The S1 negative result is bounded to the declared read set. Whether the C3 gate or the committed ledger implements an undisclosed dispute path is **unverified** and outside this seat's scope; L1 owns that question.

**F-4 (dependency).** The errata protocol's determinism rests on two per-row fields (`rough-stripped spelling`, `canonical base spelling`) that the contract's enumeration does not currently name. Either the ledger already carries them (then one clause suffices) or the protocol's adjudication step for dispute form F-1 is undecidable.

**F-5 (conflict, reported verbatim for the canonical Rust judge).** Two instructions conflict for this seat, and the seat-specific binding is narrower, so the narrower one governs; no improvisation was performed:

> Tooling directive — operator, 2026-10-19 (always on, every agent): "Any agent — main session or subagent, any lane, any wave — installs or updates any tool that helps its task or is a strict upgrade, with full privilege, without asking first. Passwordless `sudo` is available."

> Seat binding / Contract: "Tooling authorization: read `/home/vgpnk/.omp/agent/RULES.md` before installs, use official channels/update-safety gate, and record tool/version/channel/reason; all pacman transactions are PAUSED host-wide, no partial/full upgrade or service restart. This seat's narrower NO-EXEC/NO-FETCH scope forbids installations."

Resolution applied: **no install, no update, no `sudo`, no package transaction was performed or attempted** by this seat; the host-wide pacman pause was left untouched. Tool/version/channel/reason record: *not applicable — no tool was installed or updated.* The directive's "before installs" precondition (`/home/vgpnk/.omp/agent/RULES.md`) was **not** read, because this seat's read scope does not include it and no install was in scope; that path is outside `read_paths` and is reported as a scope boundary, not as a skipped step.

---

## 10. Artifact paths

- Report (written): `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/falsify/ScribeFxErrata.md`
- Target under review (read): `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/corpus/knowledge/path-reconciliation-r23.md`
- Other reads (declared): `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/preregister.json`, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/godspeed-directive.txt`, `skill://godspeed`

Reviewed-SHA256: 7661f37ab6b40668ec025b2a68f86791784ef296eccba7a458a6862dde89c3fc
Predicate: r23f-scribefxerrata
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
