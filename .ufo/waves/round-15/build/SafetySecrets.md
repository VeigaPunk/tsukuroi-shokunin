# SafetySecrets — round 15 credential/auth/db/raw-config review of planned evidence paths

Sentinel, report-only; reviewed 2026-10-20 (snapshot captured_at `2026-10-20T07:44:39Z`). Axis: depth.
Verdict: **no credential, auth, private-db or raw-config exposure found or planned**. Two low findings and one
provenance mislabel. Forbidden files (`~/.omp/agent/agent.db*`, RULES.md, auth/credential files, `/etc/pacman.conf`,
pacman.log itself) were **not opened** by me.

## Planned paths reviewed (spec.json items, 64 prompts; regex path extraction)
| Path / probe | Reads | Secret/config risk | Observed |
|---|---|---|---|
| `host-snapshot.json` (HostSnapshot) | 5 fixed `/bin/sh -c` literals | none: no interpolated input → no injection | SHA256 `b101f374…6ea81` recomputed = HostSnapshot.md; 0 hits across 12 secret regexes (sk-/gh*_/xox/AKIA/Bearer/PEM/JWT/JSON key-value secret/agent.db/auth.json·netrc·id_rsa/env-token/.omp); 0 `/home/`, 0 URLs |
| `package_versions`, `pending_updates` | `pacman -Q …`, `pacman -Qu` (local+sync DB, no network/lock) | none | 4 lines; 413 lines, 0 not matching `name old -> new` |
| `sync_metadata` | `stat -c '%w\|%z\|%n' /var/lib/pacman/sync/*.db` — metadata only, no DB bytes | low disclosure: 5th repo name `openai-chatgpt` (non-official) derived from pacman.conf | no Server/URL copied |
| `libinput_log` | `grep -nE 'libinput\|synchronizing package lists' /var/log/pacman.log` | **F1 low** | 16 lines; 1 `[PACMAN] Running` argv line (2429) |
| `boot_hook_mentions` | 2 package-owned `/usr/lib/initcpio/hooks/*` files, matching lines only | none; path matches prior corpus (`initramfs-v42-sysroot-recovery.md:12`), no `/etc/initcpio` gap | 2 lines, `/new_root` only |
| C1/C2 MD+JSON, `C1SourceWitness.json`, SOURCES S046–S048 | public man/wiki pages | none (no auth, no query tokens) | not yet written at review time |
| `tools/check-locator-clarification.py`, `tools/measure-update-recheck.py` | git blobs / committed snapshot | **F2 low** (arg injection if pattern not reused) | not yet written |
| `swarm-registry.json` (0600), `dispatch.json`, `spec.json`, `task-result.json` | wave bookkeeping | none | registry shape `schema/wave/createdAt/updatedAt/reportDir/members{kind,agentId,role,item,axes}`; only hits are prohibition text (`~/.omp/agent/agent.db*`, RULES.md, "Passwordless sudo" ×128, `"tokens": 0` counters). Rounds 12–14 committed the same 0600 registries |

## Findings
**F1 (low) — log filter copies operator argv; snapshot limit text says "no argv".** Exploit path: the unanchored
`libinput` grep retains any `[PACMAN] Running '…'` line whose arguments mention libinput — e.g. a future
`pacman -U https://user:token@host/libinput-….pkg.tar.zst` or a `/home/…` path would be committed verbatim.
Today's line is benign (`pacman -S --needed --noconfirm libinput libinput-tools`) and is the incident's core
evidence, so keep it. Also all 11 sync markers were kept although the plan said "latest" (over-collection, harmless).
Smallest remediation: C2 quotes line 2429 as *logged command string* (correct `HostSnapshot.md:56` "no … argv" in
LOG/C2 limits); future captures anchor to `\[ALPM\] (installed|upgraded|downgraded|removed) libinput` plus Running
lines with tokens containing `://` or `/` redacted, and only the last sync marker.

**F2 (low, preventive) — revision argument injection in new git-reading tools.** If a tool passes an unvalidated
`--revision` like `--output=/tmp/x` into `git show REV:path`, git parses it as an option and writes a file (no-write
contract broken). Existing `tools/check-source-scope-correction.py:26,377,521` already blocks this: `REV=^(?:HEAD|[0-9a-fA-F]{4,64})$`
fullmatch, then `rev-parse --verify --quiet REV^{commit}`, list-argv `subprocess.run` (no shell). Both new tools
must reuse that exact pattern; reviewers should grep for it. Snapshot path in the measure must be the fixed
`evidence_path`, never a JSON-supplied path (else C2 JSON could point the probe at an arbitrary file).

**F3 (calibration, sent to TsukuroiR15.IncidentEntry) — timestamp field mislabel.** `HostSnapshot.md:13,52-54` calls
`%z` "mtime" and says `%y`/ctime are absent. stat(1) (coreutils 9.11): `%z` = "time of last status change" (ctime),
`%y` = "time of last data modification". So ctime was captured; **mtime (%y) is the missing field**. C2 `meaning`
must not say mtime. [INFERENCE] pacman sets downloaded DB mtime from the server, so the upstream-side timestamp
is exactly the uncaptured field — SyncTimestamp's domain; no recapture requested.

## Recommendations (no edits made)
1. C2 JSON: store pending **count** (413) and named boot-chain lines, not the 413-line list; bind `snapshot_sha256`.
2. If the `openai-chatgpt` repo needs explanation, use `pacman-conf --repo-list` (names only, per pacman-conf(8)
   "List configured repositories."); never copy `/etc/pacman.conf`/`pacman.d` Server lines — private repos can
   embed credentials in URLs. This round: do not probe; ADJ-02 → kagi only if a credential question arises.
3. `swarm-registry.json` 0600 needs no action: no secret content, and git records it as 644 regardless.

## Limits
- Pattern scans are bounded regex sets, not proof of absence of every secret form; values were never printed
  (counts and masked context only). C1/C2 pair, C1SourceWitness.json and both tools did not exist at review time
  and are reviewed only as plans. pacman.log, sync DB contents and pacman.conf were not read by me.
- Disclosure: I ran one read-only `pacman -Qo /usr/bin/stat /usr/bin/pacman-conf` (owners: coreutils 9.11-2,
  pacman 7.1.0.r9.g54d9411-2) and read `man stat`/`man pacman-conf` — local package-DB/doc reads, no state change;
  strictly this exceeds "only HostSnapshot runs probes". No other host command, no network fetch.
- Tools installed or updated: **none**. No `pacman -S/-Sy/-Syu/-U/-R`, sudo, service or snapper action. No tests,
  build, lint or verification run.
