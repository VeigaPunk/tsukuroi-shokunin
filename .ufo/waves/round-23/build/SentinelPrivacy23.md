# SentinelPrivacy23

## Axes
- Confidentiality and data minimization
- Auditability and provenance
- Scope and enforcement credibility

## Finding
**Severity: Low for the inspected snapshot; residual session-retention risk remains unassessed.** The inspected structured-edit observation contains request metadata and adapter paths, not captured edit bodies. This is not evidence that the underlying sessions, other recorders, or every adapter omit those bodies.

**Exploit path:** If a session/adapter recorder serializes structured-edit argument values (for example, patch text, `new_string`, or `stream_content`), a user or agent can inadvertently place a credential or private report text there; any command/environment capture could similarly retain sensitive values if enabled. A reader of such retained records could recover those values. This is a conditional risk only: the permitted snapshot does not show such values or establish that any recorder retains them.

**Evidence:** `sources/structured-edit-observations.json` records only argument keys for the observed `edit` requests (lines 11–17, 37–45, 60–68, 83–91), labels body fields as omitted/no report text copied, and records paths, call IDs, transcript digests, agent IDs, and line numbers (lines 8–27, 34–51, 57–74, 80–97). Its scope explicitly excludes universal tool semantics and proof of reading/effects (line 101). The preregistration states raw command/fetch body content is not copied and disclaims runtime/effect/reading/recorder-completeness claims (lines 110–115); its listed checker commands are command templates, not captured invocations or environment values (lines 26–53). No raw sessions were inspected. The permitted evidence therefore supports “not present in this snapshot,” not “never retained.”

**Impact:** No credential, report-body, command-body, or environment value is exposed by the reviewed snapshot. Retained call IDs, transcript hashes, agent IDs, and absolute user-home paths do create linkability and disclose local path layout, even without bodies. If a separate recorder stores argument values, secrets/report contents could persist in its records; that impact is not established here.

**Smallest remediation:** Keep the structured evidence as an allowlist of seat/tool, argument-key names, ordered adapter operations, and repository-relative target paths; omit call/agent identifiers and absolute home prefixes unless required for a documented audit join. Represent body handling only as a boolean/status, never by copying values. Preserve a stable source digest only where the audit needs it. Do not present omission from this snapshot as native redaction or runtime prevention.

## Fail-capable privacy fixtures
Add serialization/collector tests with synthetic canaries (never real credentials) placed separately in patch/edit body values, report text, command-body values, and environment values. Each fixture must assert that no canary or raw value occurs anywhere in serialized evidence and that only the approved metadata allowlist is emitted. Include a deliberately leaking serializer fixture that must fail, plus variants using nested fields and alternate body-bearing argument names so a renamed field cannot silently bypass the assertion. Include a path fixture that fails on an absolute home-directory prefix while retaining the expected repository-relative path. These tests can establish the tested collector behavior only; they do not establish universal tool semantics or native per-seat enforcement.

Reviewed-SHA256: 19d85129bf0f7fd71f5aea93c35660b21d305150500dc63b58104019851af12a
Predicate: r23-sentinelprivacy23
Scope: executed=none