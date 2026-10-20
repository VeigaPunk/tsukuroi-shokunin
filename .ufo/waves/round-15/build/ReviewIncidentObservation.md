# ReviewIncidentObservation — round 15, C2 observation labels (static)

Scope: static contract review of the C2 observation labels. Read-only. No tests, no builds, no probes, no installs.

## Comparison status

- `host-snapshot.json` is **absent** from `.ufo/waves/round-15/build/` (listing: task-result, validation, dispatch, swarm-registry, spec, start). No snapshot-to-label comparison was possible.
- `corpus/knowledge/partial-upgrade-recheck-r15.{md,json}` do not exist yet. No C2 labels were observed.
- Result: **no label was checked against live evidence.** Everything below is a contract risk, marked as such.

## Contract risks (ordered by impact)

1. **`snapshot_sha256` is required but not declared.** `IncidentMeasure` (dispatch.json task text) says "require C2 JSON snapshot_sha256". The C2 field list in spec.json interfaces is `source_ids, observed_at, evidence_path, observations, decision, limits`. A conformant JSON fails the measure, or the author silently adds a field. Fix: add `snapshot_sha256` to the schema, or remove the requirement.
2. **No exit field in observations.** Observations are `command_key/value/meaning`. The snapshot probes carry `exit`, but `value` alone cannot separate "no result" from "failed query". `pacman -Qu` rc=1 with empty stdout is the normal no-candidates result in this corpus (`driver-firmware-plane.md:181-182`, `aur-risk-plane-ver-s7.md:48`, `host-health-report-r3.md:309`). The same rc=1 pattern is what a failed query would look like without stderr. Fix: each observation carries `exit` and `stderr_empty`; `pending_updates` is "zero" only for exit 1 with empty stderr, "N" only for exit 0, and unknown otherwise. This is the only structural defense against AttackSnapshotTamper's "failed pending query as zero".
3. **"Observation linkage" is undefined.** `IncidentMeasure` must verify linkage, but no rule says how `command_key` maps to snapshot `probes` keys. Fix: each `command_key` must be one of `package_versions, pending_updates, sync_metadata, libinput_log, boot_hook_mentions` and must exist in `probes`; value must be derivable from that probe's stdout.
4. **Timestamp names differ.** Snapshot uses `captured_at`; C2 uses `observed_at`. The measure must "verify timestamp" without saying which pair. Fix: require `observed_at >= captured_at` and state the rule in the schema.
5. **`installed_libinput` overreads.** It is a `pacman -Q` database value (installed file version). The task itself says the running mapped version is NOT measured. Fix: rename to `installed_version_libinput` and write in `meaning` that it is not the running process version.
6. **`pending_updates` is against a stale local DB.** Empty `-Qu` was measured against 36-day-old content stamps in r3 (`host-health-report-r3.md:309-312`). The label must be paired with the `sync_metadata` observation and must say "against local sync DB snapshot", never "current upstream". The spec's "fresh counts may differ" is correct, but nothing enforces it.
7. **Absent package is not zero.** `pacman -Q <pkg>` for a non-installed package returns rc=1 with "was not found" (`aur-risk-plane-ver-s7.md` R1; `driver-firmware-plane.md:178-179`). A `libinput-tools` absence needs a label "not installed", not a count or version.
8. **Glob will not expand under subprocess.** `sync_metadata` is `stat -c %w/%z/%n` on `/var/lib/pacman/sync/*.db`. With a list-argv `subprocess` and no shell, the literal `*.db` is passed to `stat`, which fails. This is a HostSnapshot implementation risk, not verified by running it. Fix: `glob.glob()` in Python, then one `stat` per path with its own exit. `%w` can print `-` when birth time is unavailable; label that as unknown.
9. **`libinput_log` filter term is unverified.** The term `synchronizing-package-lists` (hyphenated) is not in any corpus evidence. The literal log text is not verified here. A zero-match result could be read as "no libinput activity", which is a false absence. Fix: record match count per term plus exit; zero matches means "no matching lines for this term", nothing more. "Latest" needs a stated selection rule.
10. **Hook counts are context, not current.** `boot_hook_mentions` should carry fresh counts only. The prior `btrfs-overlayfs:4` / `plymouth:11` values (`initramfs-v42-sysroot-recovery.md:12`) must not be copied into labels.
11. **Decision must not follow from counts.** `decision=BLOCKED_FOR_AGENT_PACKAGE_ACTION` is a fixed string. The measure's `pending_count=0` must not map to any clear or healthy decision. The task already says "No blanket HEALTHY or authorization"; the schema should say the same.
12. **Source dependency order.** IncidentEntry must cite S047 and S048. SOURCES.md currently ends at S045 (`grep '^| S04[5-8] |'` shows S044 and S045 only). `source_ids` must be checked after SourceRegistry lands, or the measure's source check fails.

## Recommendations

- Add `snapshot_sha256`, `exit`, `stderr_empty` and `probe_key` to the observation schema, or drop the requirements that depend on them. Keep the schema and the measure's checks identical.
- Fix the `observed_at >= captured_at` rule in the schema text, not in code comments.
- Rename `installed_libinput` to `installed_version_libinput`; state "not running version" in its meaning.
- HostSnapshot: use Python `glob`, one `stat` per path, record exit per file, record match counts per log term.
- Sequence: SourceRegistry must land S046-S048 before IncidentEntry's `source_ids` are validated.

## Sources and limits

- Opened and read: `.ufo/waves/round-15/build/{spec,dispatch,validation}.json`, `corpus/lessons/round-14-verifier-spotcheck.md`, `corpus/SOURCES.md` (row grep), corpus knowledge files cited above (own-work host evidence from 2026-10-14 and 2026-10-19; not re-probed).
- Attempted `https://man.archlinux.org/man/pacman.8`: failed (ECONNRESET). No pacman(8) exit-code claim here rests on that page. Exit-code statements rely on corpus observations only.
- Not checked: any live host state; the actual `pacman.log` text; whether the r15 snapshot will be committed.

## Tools

- read, grep (x3), glob (x2) — local reads only.
- URL read attempt (failed).
- Installs or updates: **none**. No package, service, or probe was run.
