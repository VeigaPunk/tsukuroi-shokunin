# IncidentMeasure — round 15 C2 counting probe
Scope: new read-only `tools/measure-update-recheck.py` plus this report. No host
command, test, build, formatter, package/service change, install, sudo, credential
or agent-db access. L1 owns baseline/final runs.

## Interface (coordinated with IncidentEntry)
- Both inputs read from one revision: `corpus/knowledge/partial-upgrade-recheck-r15.json`
  and the constant `.ufo/waves/round-15/build/host-snapshot.json`. Worktree default;
  `--revision REV` resolves HEAD/4–64 hex and reads blobs with `git show` under
  `GIT_OPTIONAL_LOCKS=0`. Git is the only subprocess, only in `--revision` mode.
- stdout fields: status, revision, record_count, pending_count, pending_exit, installed_libinput, installed_libinput_kind, health="not_assessed", source_ids, observed_at, snapshot_captured_at, declared_decision, snapshot_sha256, findings.
- Exit 0: both absent (`ABSENT`, count 0) or one consistent record (`COUNTED`,
  count 1). Exit 2: malformed/incomplete/mismatch or one-of-two absent
  (`CANNOT_EVALUATE`). No exit 1; no health or authorization claim.

## Checks encoded
- Lowercase 64-hex SHA-256 of raw snapshot bytes vs `snapshot_sha256`;
  `evidence_path` equals the constant and is never followed; duplicate keys,
  NaN/Infinity and bool exits rejected.
- `observed_at` strict `YYYY-MM-DDTHH:MM:SSZ`, equal to measured `captured_at`
  (and optional `snapshot_captured_at`), not before sync birth, at least 1 s after
  the last captured `upgraded libinput`.
- `source_ids` are S### with S047/S048/S049 present; extras allowed, order/count
  not fixed.
- One observation per probe key; `probe_key == command_key`; exact snapshot exit
  and stderr-empty equality. Values recomputed, never echoed: `-Qu` row count
  (exit 1 is zero only with empty stdout+stderr; any other nonzero/partial result
  is exit 2, never zero), four `pacman -Q` rows, shared `%w` birth in UTC, last
  upgrade UTC whose target equals installed libinput, hook `name:NN` refs with
  `/sysroot` agreement.
- `decision` fixed to `BLOCKED_FOR_AGENT_PACKAGE_ACTION`; `limits` non-empty.
  No selftest added (no obligation; L1 runs baseline/final).

## Input facts (static inspection; probe not executed)
- JSON: schema `tsukuroi-partial-upgrade-recheck-v1`; source_ids
  `["S047","S048","S049"]`; observed_at == snapshot_captured_at
  `2026-10-20T07:44:39Z`; exact evidence_path; sha256
  `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`;
  fixed decision; 7 limits; 5 observations exit 0/stderr_empty true.
- Snapshot: 18,318 raw bytes, same digest/captured_at; `-Qu` exit 0, 413 rows all
  matching `pkg old -> new [ignored]?`; libinput 1.32.0-1; sync `%w`
  `2026-10-18T17:11:00Z`; line 2432
  `[2026-10-20T04:25:17-0300] upgraded libinput (1.31.3-1 -> 1.32.0-1)`; hooks
  `/new_root` at `btrfs-overlayfs:4`, `plymouth:11`, no `/sysroot`.
- IncidentEntry corrected `libinput_log` to `2026-10-20T07:25:17Z`; snapshot bytes
  are authoritative for recomputation.

## Evidence, limits, tools
- Evidence: input bytes above; IncidentEntry shape/value messages;
  AttackSnapshotTamper list applied (raw digest, one-of-two absent exit 2,
  constant path, bool/NaN/dup rejection, line-wise `-Qu`, recomputed values).
- Limits: round-scoped (five probes, four packages, S047–S049); does not execute
  or re-verify host probes, running mapped libinput, ABI, dependency closure, UI
  health or causality; grants no package action. Digest binds only the filtered
  extract, not raw pacman.log/hook files. Timestamps are capture-time, not
  upstream freshness. Final `--revision` exits 2 unless both files are committed.
  Tools installed/updated: none; host state unchanged.
- Expected, not executed: baseline `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`
  → ABSENT/count 0/exit 0; final → COUNTED/count 1/pending 413/libinput
  1.32.0-1. No test result is claimed.
