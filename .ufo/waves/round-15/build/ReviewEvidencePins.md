# ReviewEvidencePins — host snapshot SHA256 binding (round 15, static review)

Scope: static review of how `host-snapshot.json` is bound (digest + exact captured timestamp) across the wave contract. Nothing executed; no snapshot read or hashed. Target said "do not execute".

## Current state observed
- `.ufo/waves/round-15/build/` lists only: swarm-registry.json, assignments.json, task-result.json, validation.json, dispatch.json, spec.json, start.json. `host-snapshot.json` is **absent** at review time; HostSnapshot is still pending (task-result.json).
- No C2 pair (`corpus/knowledge/partial-upgrade-recheck-r15.{md,json}`) exists yet.

## Findings (by severity)

**F1 high — digest field missing from the C2 contract.**
spec.json `Interfaces` lists the C2 JSON fields as: source_ids, observed_at, evidence_path, observations, decision, limits. No digest, no captured timestamp.
IncidentMeasure (dispatch.json ~L648) requires "C2 JSON snapshot_sha256". IncidentEntry is not told to write it. Result: IncidentMeasure exits 2 on every real run, or IncidentEntry omits the field and the binding is silently absent.
Fix: add `snapshot_path`, `snapshot_sha256`, `snapshot_captured_at` to schema tsukuroi-partial-upgrade-recheck-v1 and to IncidentEntry's required fields. Precedent: r14 `.ufo/waves/round-14/repair/verification.json` pins `evaluator_sha256` as a top-level field next to command/exit/stdout/stderr; use the same style.

**F2 high — digest scope undefined.**
IncidentMeasure says "hash snapshot input"; no spec says over which bytes. Re-serialized JSON hashes differently from the file.
Fix: `snapshot_sha256` = lowercase 64-hex SHA-256 of the raw file bytes as written. The snapshot cannot contain its own hash, so the binding lives only in the C2 JSON and report.

**F3 high — "exact captured timestamp" is not pinned.**
HostSnapshot says only "UTC capture", with no format and no rule for when. C2 uses `observed_at`; snapshot uses `captured_at`. The spec never says they must be equal.
Fix: captured_at = RFC 3339 UTC `YYYY-MM-DDTHH:MM:SSZ`, recorded before the first probe runs. C2 `snapshot_captured_at` must be string-equal to it. Measurer rejects any other format. Per-probe start/end times are optional extras.

**F4 medium — write/read race, no completion gate.**
HostSnapshot and IncidentEntry run in parallel. IncidentEntry is told to "create shared C2 pair when HostSnapshot exists", which is an existence check, not a completion check. A reader can hash a partial file, or hash a file that is later rewritten.
Fix: HostSnapshot writes a temp file, computes the digest, then renames into place. IncidentEntry records the digest it read. Measurer rehashes at run time and compares.

**F5 medium — digest proves bytes, not probe truth.**
A failed probe is still hashed and looks valid. The AttackSnapshotTamper target warns against treating a failed `pacman -Qu` as zero.
Fix: C2 observations must carry each probe's exit and stderr presence. Measurer treats a non-zero exit on pending_updates or package_versions as CANNOT_EVALUATE, not pending=0. Digest bounds only the filtered extract: libinput_log is filtered and boot_hook_mentions is partial. Raw pacman.log is not bound; list this as a limit.

**F6 medium — sync_metadata timestamp fields are not exact.**
`stat -c %w/%z/%n` prints `-` for birth time on filesystems that lack it, and `%z` is ctime, not mtime. Sync freshness needs mtime.
Fix: name the format string in the snapshot, record `-` literally as "unknown", and never coerce it to a timestamp. Prefer `%Y` (epoch mtime) with an explicit key name.

**F7 low — path form.**
evidence_path is repo-relative (`.ufo/waves/round-15/build/host-snapshot.json`). Record that root alongside the digest so a moved file fails the hash, not silently resolves elsewhere.

## Recommendations (ordered)
1. Amend spec.json C2 field list and IncidentEntry requirements to add snapshot_path, snapshot_sha256, snapshot_captured_at (F1).
2. Define sha256 over raw bytes; measurer exit 2 CANNOT_EVALUATE on mismatch, missing field, or non-matching timestamp (F2, F3).
3. Sequence: HostSnapshot atomic write → digest → IncidentEntry reads → IncidentMeasure rehashes (F4).
4. Require exit codes in observations; no zero defaults (F5).
5. Fix the sync_metadata format string and key names (F6).

## Limits
- Static review of repo files only: spec.json, dispatch.json (taskCall and task entries), task-result.json, start.json, r14 verification.json, source-scope-correction-r14.json.
- No hash computed; snapshot absent; no probe run; no test run.
- Recommendations are not applied; owners are IncidentEntry, IncidentMeasure, HostSnapshot and L1.

## Tools
Read, glob, grep only. No installs, updates, or package/service changes. Recorded: tools none.
