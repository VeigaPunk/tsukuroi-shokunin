# DecisionSnapshotAge — round 15

Seat TsukuroiR15.DecisionSnapshotAge. Baseline `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`. Report-only: no docs edits, no host probes, no package/service/sudo/credential action, no child or labrat dispatch; tools installed/updated: **none**.

## Concrete decision fragment

Row `R15-SNAPSHOT-AGE` — dates the local sync-DB snapshot. It is a **label/precondition row** for C2's `sync_metadata` and `pending_updates` observations: a timestamp row may never be promoted to a freshness row.

| field | R15-SNAPSHOT-AGE |
|---|---|
| trigger | Any C2 statement that dates the local sync DBs, or derives `fresh`/`current`/`unsafe` from a timestamp; any label pairing pending counts with "upstream" or "now". Applies to every timestamp shape: mtime-only, arrival-only (this wave), full triple, or log-marker-only. |
| required receipt | Exact stat format string; per-file bound values with units and offset; each file listed by configured repo; log term, command, exit, all matched lines, capture instant. Never omit the format string, never coerce `-` to a date. Missing field ⇒ `CANNOT_EVALUATE`. |
| decision | `SNAPSHOT_AGE_MEASURED` with `FRESHNESS_NOT_ESTABLISHED`. Age is `captured_at − local arrival` only. Fixed package decision is unchanged: `BLOCKED_FOR_AGENT_PACKAGE_ACTION`. |
| epistemic state | Timestamps bound **when the local file arrived**, not what the repository contained then or now. Upstream divergence is unknown in both directions. |
| forbidden inference | mtime = sync time; birth/ctime = successful sync; log marker = completed refresh; any of the three = repository freshness guarantee; no later marker = no upstream change. |

### Three evidence planes — this wave's captured values

| plane | captured | what it dates | cannot establish |
|---|---|---|---|
| upstream mtime `%y` | **NOT captured** — probe argv has `%w\|%z\|%n` only | upstream file build/stamp; pacman preserves server mtime on download (`package-state-plane.md:73-81`) | local arrival; current upstream HEAD; content validity |
| local arrival `%w`/`%z` | birth `2026-10-18 14:11:00.026135178 -0300` = `17:11:00.026Z`; ctime `.921`–`.923` (all 5 DBs) | inode creation and final local commit, ~0.9 s apart — a write/rename window [INFERENCE] | sync success; per-repo completeness; later upstream change |
| sync log marker | `:2288 [2026-10-18T14:11:00-0300] [PACMAN] synchronizing package lists`; no later marker in the extract | start of a sync **attempt** | completion/exit (pacman.log marker carries no result in this extract); successful refresh |

Cross-check: marker 2288 and birth `.026` are second-exact at `17:11:00Z`, so together they support "a refresh attempt ran and the DB files were rewritten at 14:11:00 local", not "all five repos synced successfully". Snapshot age from arrival to `captured_at 2026-10-20T07:44:39Z` is **38 h 33 min 39 s**. Offset trap: log lines 2–415 are `+0000`, later lines `-0300`; compare in UTC, never by string order.

### Branch rule

| branch | condition | classification |
|---|---|---|
| B0 only mtime | `%y` provided as the sync stamp | `NOT_DATABLE_AS_ARRIVAL` — no age, no freshness label |
| B1 arrival | `%w` and/or `%z` present and dated | `SNAPSHOT_AGE_MEASURED` (local), age = capture − arrival |
| B2 marker cross-check | latest marker within the arrival second | "refresh attempt" label; success still unproven |
| B3 sync result receipt | sync process's own exit/result captured at invocation + per-repo replacement receipt | `SYNC_RESULT_RECEIPTED` — the only route to "successful sync"; absent here |
| B4 any plane → freshness | no upstream observation of repo state | `FRESHNESS_NOT_ESTABLISHED`; pending count reads "against local DB snapshot arrived `2026-10-18T17:11:00Z`", never "current upstream" |

Machine row (C2 observation label):
`{"id":"R15-SNAPSHOT-AGE","command_key":"sync_metadata","observed_age":"38h33m39s","age_basis":"birth/ctime 2026-10-18T17:11:00Z","mtime":"not_captured","last_sync_marker":"2026-10-18T17:11:00Z","sync_success":"not_established","freshness":"not_established","decision":"BLOCKED_FOR_AGENT_PACKAGE_ACTION"}`

## Evidence

- Retained probe, read only: `host-snapshot.json` `sync_metadata` — `stat -c '%w|%z|%n' /var/lib/pacman/sync/*.db`, exit 0, empty stderr, 5 rows (core, extra, multilib, omarchy, openai-chatgpt). `libinput_log` — `grep -nE 'libinput|synchronizing package lists' /var/log/pacman.log`; matches 2–2288 include 9 sync markers; latest is 2288; transaction lines 2429/2432/2436 at `04:25:16`–`17 -0300` = `07:25:16Z`, 19 m 23 s before capture.
- Established lane teaching: `package-state-plane.md:73-81` — birth/ctime used for arrival because “pacman preserves upstream file mtimes on download; **mtime ≠ datetime of the local sync**”; `update-safety-note.md:44-50` labels `%y` “upstream stamp” and records a second-exact birth↔log match; `SKILL.md:94-96` — “use `%w`/`%z` (birth/ctime), **never `%y`**”; empty `-Qu` proves “nothing newer than the last sync snapshot”.
- Review/adjudication already on record: `ReviewEvidencePins.md` F6 (`%z` is ctime, not mtime; freshness needs mtime); `adjudications.json:12` — birth/ctime and the sync-log attempt are “hints, not successful-sync or upstream-freshness proof”; snapshot bytes unchanged.
- Source rows S047/S048 are doctrine/option scope only: S048 documents `-p/--print` behavior, “not a host transaction result or whether sync metadata is current”. Neither supplies timestamp semantics; no new source search was performed.

## Recommendations for L1

1. Keep the raw triple verbatim in the C2 `sync_metadata` value; put age and its basis in `meaning`; add `mtime: not_captured` explicitly so no reader supplies a phantom mtime.
2. Label pending 413 as “against local DB snapshot arrived `2026-10-18T17:11:00Z`”; the stale DB entry is not newer than installed — never “current upstream”, never HEALTHY.
3. Treat marker absence after 2288 as bounded to this captured extract (pattern, single file, capture instant); it does not cover post-capture, rotation, or upstream movement.
4. Route “successful sync” to a future receipt class (B3). No count, timestamp or marker in this wave qualifies; the package decision stays blocked regardless.
5. If the advisory row is adopted, cite stable file/section names and the probe argv, not rendered line numbers.

## Sources, limits, tools

- Read: wave `host-snapshot.json`, `SyncTimestamp.md`, `ReviewEvidencePins.md`, `adjudications.json`, `HostSnapshot.md`; repo `corpus/knowledge/package-state-plane.md:73-81`, `update-safety-note.md:38-60`, `SKILL.md:90-100`, `SOURCES.md` S047/S048.
- Limits: no host command, no re-stat, no log re-read, no source reopen, no checker or executable written; one snapshot only, so no timestamp-mechanics experiment and no pacman version test. `%w` can print `-` on filesystems without birth support — all five here are dated. The 0.9 s birth→ctime gap explanation is inference, not observed syscall trace. The “no later sync marker” bound is the retained grep output only; no claim about pacman.log failure-line capability is made. This fragment is documentation, not enforcement, and asserts no ordinal or verification result.
- Tools installed/updated: none. No package changes, upgrades, downgrades, removals, service restarts, snapper queries or daemon activation.
