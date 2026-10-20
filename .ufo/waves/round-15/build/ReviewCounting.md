# ReviewCounting — round-15 planned measurement commands

Scope: review of the two planned measurement commands against "correction count vs source truth" and "observation presence vs health". Report only. No code, docs, or host state changed.

Target commands (spec only; neither file exists yet):
- C1: `tools/check-locator-clarification.py` (LocatorGate) — `dispatch.json:623`
- C2: `tools/measure-update-recheck.py` (IncidentMeasure) — `dispatch.json:648`

## Findings

**F1 (High) — C2 digest requirement has no schema field.** IncidentMeasure must "require C2 JSON snapshot_sha256" (`dispatch.json:648`). The C2 schema contract lists only `source_ids, observed_at, evidence_path, observations, decision, limits` (`spec.json:3`; same in `dispatch.json:613`). `snapshot_sha256` is defined nowhere. Effect: every valid C2 pair exits 2, or the digest binding is silently never tested. Also the timestamps differ: C2 uses `observed_at`, snapshot uses `captured_at`, and the measure says only "timestamp". Fix: add `snapshot_sha256` to the C2 schema in IncidentEntry and `tsukuroi-partial-upgrade-recheck-v1` before coding, and name the pair explicitly (`observed_at >= captured_at`).

**F2 (High) — absence reports as a pass-shaped result.** `Before absence yields count0 exit0` (`dispatch.json:648`). "No C2 record yet" therefore has the same exit code as "record present, pending_count 0". The output has no status field, so a consumer reading exit 0 as clean cannot tell them apart. Fix: emit `status` ∈ {`ABSENT`, `PRESENT_VERIFIED`, `CANNOT_EVALUATE`}; `ABSENT` must never map to pass.

**F3 (High) — the measure carries no health statement.** The output fields `record_count, pending_count, installed_libinput, source_ids, revision, findings` (`dispatch.json:648`) measure presence and version only. Health is not in the output and not disclaimed in it, though the prose says "no blanket HEALTHY". `pending_count` is a capture-time count from `pacman -Qu`, not a current one, and no field carries snapshot age. Fix: add `health: "not_assessed"` as a constant field, `captured_at`, and `snapshot_age_s`. When the `pacman -Qu` probe exit is non-zero, set `pending_count: null`, never 0 (AttackSnapshotTamper covers this path).

**F4 (High) — `correction_count` is structural conformance, not source truth.** The planned gate prints `revision/correction_count/findings/status` (`dispatch.json:623`). Its template, `tools/check-source-scope-correction.py`, computes `correction_count` as a conjunction of structural predicates (`:324-331`, emitted at `:336`). Its own docstring says "Not a semantic proof" (`:4-5`). The predicates compare committed bytes to committed bytes (quote substrings, URL strings, notice presence). No network is used, so the quotes are never checked against the live source. The r14 JSON says the same: "no source-truth enforcement claim" (`source-scope-correction-r14.json:6`). The planned gate does not say this. Fix: name the field `conforming_correction_count`, or add `"source_truth": "not_evaluated"` plus a pointer `{path, sha256}` to `C1SourceWitness.json`. Source truth stays a dated witness, not a tool output.

**F5 (Medium) — record presence and conformance are not separated.** LocatorGate counts "two shared correction IDs" and also requires "both supersession notices in r14 MD/JSON". The spec does not say whether `correction_count` is conjunctive with the notices. The r14 pattern is conjunctive, so baseline gives 0 and a clean run gives 2. The spec leaves this open. Fix: output both `records_present` (presence) and `conforming_correction_count` (presence plus predicates plus notices), and selftest both. The r14 lesson already warns: "Presence alone does not prove resolution" (`corpus/lessons/round-14-verifier-spotcheck.md:109`).

**F6 (Medium) — worktree default can count uncommitted state.** LocatorGate defaults to the worktree; IncidentMeasure requires a committed REV. Worktree counts can include unreviewed edits. Fix: output `resolved_sha` and `worktree_dirty`. Final/baseline numbers must come from committed SHAs only.

**F7 (Low) — exit-code semantics differ across the two siblings.** LocatorGate uses 0 clean / 1 failed / 2 cannot-evaluate. The measure uses 0 for absent. Use one table for both.

**F8 (Low) — the probe has no tamper fixtures.** `No selftest obligation for probe` (`dispatch.json:648`). The paths most likely to be misread (absent, malformed, digest mismatch, failed `pacman -Qu`) are the ones that most need fixtures. Minimal fixtures are enough.

## What is sound

- The gate's baseline expectation (FAIL, count 0, LOCATOR_UNQUALIFIED) makes the count non-vacuous, provided the conjunctive form is kept (F5).
- IncidentMeasure says "PROBE not truth gate" and "No blanket HEALTHY or authorization" (`dispatch.json:648`). Keep that wording.
- Both specs forbid writes and host commands outside the approved probe list.

## Recommendations (ordered)

1. Fix F1 in the C2 schema before any coding (blocks the measure).
2. Adopt the F2/F3 status and health fields in the measure spec.
3. Rename or annotate `correction_count` (F4); split presence from conformance (F5).
4. Pin committed SHAs and dirty state in both outputs (F6).
5. Unify exit codes (F7) and add tamper fixtures (F8).
6. In LOG/SCORECARD, label the metric "structurally conforming records", never "verified corrections" or "healthy".

## Limits and verification gaps

- Neither tool exists yet; findings come from the dispatch/spec text and the r14 checker as template.
- `host-snapshot.json` and the C2 pair do not yet exist in `.ufo/waves/round-15/build/`, so observation linkage was not checked against real data.
- Source truth was not checked: no URL was reopened by this seat. The r14 "verified" statements were read from the committed JSON/lesson only.
- Nothing was executed. No tests, builds, lint, or smoke runs. No claim that any check passes.

Tools: read, glob, grep only. Installs/updates: none. Host commands: none. Package actions: none.
