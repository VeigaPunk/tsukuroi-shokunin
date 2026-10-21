# SentinelNoEffects23 — edit-authority boundary

**Severity: Informational / low.** The reviewed declarations expressly limit their authority; no runtime enforcement defect is demonstrated by these files. The main risk is overclaiming what an audit decision means.

**Exploit path (conditional, not observed):** A consumer treats `DECLARED_EDIT: ALLOW` as a command to execute, as proof that a request was blocked or contained, or as proof that the target was actually read. It then accepts an opaque patch with no structured target (`OPAQUE_PATCH: UNKNOWN`), lets an adapter perform additional reads or writes without checking each one (`EXPANSION: CHECK_EACH`), or treats an external URI as a filesystem target. The policy supplies classification data, not a mechanism that blocks those requests or constrains their effects. No reviewed evidence shows a consumer doing this, so this is a misuse path, not a demonstrated exploit.

**Evidence and exact refusal boundary:**

- `.ufo/waves/round-23/sources/edit-decision-policy.json` identifies itself as `tsukuroi-edit-policy-v1` and scopes itself to “Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof.”
- Its `DECLARED_EDIT` result is `ALLOW` only when the exact target is predeclared for edit and both read and write. `UNDECLARED_EDIT`, `READ_ONLY_EDIT`, and `WRITE_ONLY_EDIT` are `DENY`; `EDIT_TRAVERSAL` and `EDIT_EXTERNAL` are `DENY`; `OPAQUE_PATCH` is `UNKNOWN` when a structured target is missing; `EXPANSION` is `CHECK_EACH` for each recorded adapter read or write.
- `.ufo/waves/round-23/preregister.json` says C1 is a source-grounded decision contract, not repaired runtime behavior (lines 26–35); C2 is schema-v2 audit authority, with opaque body data and no native enforcement/effects claim (lines 37–44); and the limits explicitly exclude native restrictive tools, runtime prevention, effect/reading/recorder-completeness proof, and universal tool/patch semantics (lines 110–115). The prereg also says the legacy schema-v1 policy remains unchanged (lines 37–44).

**Impact:** Presenting these decisions as runtime gates, effect containment, evidence that a read occurred, or permission for host actions would fabricate enforcement or provenance. In particular, `ALLOW` describes only declared structured-target metadata; it does not license command execution, fetching, or other host action. Neither `UNKNOWN` nor `CHECK_EACH` is a blanket allow.

**Smallest remediation:** No change to the reviewed policy is indicated. Keep consumer/report wording at “audit decision for structured target metadata”; do not claim request prevention, effect containment, read proof, or host-action authorization. Preserve `UNKNOWN` and per-adapter `CHECK_EACH` rather than promoting either to permission.

Reviewed-SHA256: f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805
Predicate: r23-sentinelnoeffects23
Scope: executed=none