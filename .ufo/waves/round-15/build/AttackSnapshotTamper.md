# AttackSnapshotTamper — C2 measure tamper / failure-as-zero attack (round 15)
Seat TsukuroiR15.AttackSnapshotTamper (critic, read-only). Axes: freshness (C2), calibration guard.
`tools/measure-update-recheck.py` absent at review end → static counterexamples vs dispatched contract, real snapshot
and landed `corpus/knowledge/partial-upgrade-recheck-r15.json` (04:48). No measure/test executed.

## Evidence (observed)
- Snapshot 18318 B, sha256 `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`; untracked, not ignored,
  no `.gitattributes`, `core.autocrlf` unset (blob = worktree bytes). Five probes {command,exit,stdout,stderr}, all exit 0,
  stderr ''. -Qu 413 lines, 413/413 match `^\S+ \S+ -> \S+( \[ignored\])?$`, 0 ignored, no libinput row.
- C2 JSON: `snapshot_sha256` equals raw-byte digest; `observed_at`==`snapshot_captured_at`==captured_at `2026-10-20T07:44:39Z`;
  evidence_path exact; no duplicate keys (checked with object_pairs_hook).
- pacman v7.1.0 `src/pacman/query.c`: L421-422 `if(check_syncdbs(1, 1)) { return 1;` under op_q_upgrade; L448-449
  `if(!match) { ret = 1;`. Local pacman(8) v7.1.0 documents no exit statuses; `-u`: "works best if the sync database is refreshed using -Sy."
- Python: `json.loads('{"exit":1,"exit":0}')`→exit 0; NaN accepted; `False == 0`, `isinstance(False,int)` True; `len(''.split('\n'))==1`;
  `json.dumps(obj,indent=2)+'\n'` reproduces snapshot bytes today (a reserialization digest would coincidentally pass).

## Counterexamples — each must not yield a countable record
1. **Failed -Qu as zero.** Exit 1 = no-match AND sync-DB failure. Zero only if `type(exit) is int`, exit==1, stdout=='' and
   stderr==''; exit1+stdout (impossible for -Qu), exit≥2/negative/null/missing, nonempty stderr → exit2 CANNOT.
2. **Missing probe/exit.** `.get('exit',0)`, `.get('pending_updates',{})`, `exit:false` pass silently. Require 5 keys,
   exactly 4 fields, `type(exit) is int`, str stdout/stderr, exact contract command string (reject `-Qqu`, `--ignore`, `cat old`).
3. **Duplicate key + reserialized digest.** Tampered `"exit":1,…"exit":0` parses to 0 and reserialized digest equals the
   honest one. Hash raw `git show REV:path` bytes; reject duplicate keys and NaN/Infinity.
4. **Digest mismatch as finding-only.** Mismatch/non-lowercase-64-hex/prefix or case-folded compare → exit2, record_count 0.
5. **Changed snapshot/mixed source.** JSON at REV + worktree snapshot lets post-commit recapture pass. Both from same REV;
   evidence_path compared as constant, never followed (`..`/absolute/alternate). Emit digest + resolved 40-hex rev.
6. **Half-absence as baseline.** count0 exit0 only when BOTH absent; one present, or git error other than missing path → exit2.
7. **Echoed JSON values.** JSON carries its own `exit`/`stderr_empty`/`value`; measure must recompute pending_count
   (splitlines+regex) and installed_libinput from snapshot; disagreement or duplicate/unknown command_key → finding.
8. **Stale substitution invisible to count.** 413 equals historical pending413. Require captured_at UTC `Z`,
   ≥ `2026-10-20T07:25:17Z` (log l.2432), ≤ REV committer time; installed_libinput == last logged `libinput (… -> V)`.
9. **String time ordering.** pacman.log mixes offsets: l.415 `2026-10-03T20:42:20+0000` sorts after l.771
   `2026-10-03T17:44:21-0300` yet is ~2 min earlier. Parse offsets or use line order.
10. **Latent probe conflation (current data unaffected).** boot_hook_mentions `if grep …; else echo 'no … match'` turns
   grep exit 2 into "no match" with loop exit 0. Today stderr '' and both hooks match `/new_root`; consumers: stderr ≠ '' → CANNOT.

## Landed C2 pair defects (IncidentEntry-owned; not edited) — re-scanned after owner fixes
- D1 FIXED: sync_metadata meaning paired UTC clock `17:11:00.026135178` with `-0300` (=20:11Z); now raw `14:11:00.026135178 -0300`.
- D2 FIXED: JSON pending meaning, MD:36 and MD:63-64 R15-BOUNDARIES 3 now "stale DB entry is not newer than installed"
  (was an equality claim; -Qu absence shows only not-newer). Re-read after owner's final edit.
- Pins re-verified after edits: raw digest match, observed_at==snapshot_captured_at==captured_at, evidence_path exact,
  5 command_key==probe_key, int exit equal, stderr_empty consistent, no duplicate keys. Historical rc1-empty -Qu
  (update-safety-note.md:23) was corroborated by `-Sup` and a version join — precedent that rc1 alone is not proof.

## Smallest safe correction
Measure: items 1–6 fail closed (exit2, record_count 0, pending_count null); 7–9 findings; 10 limit line. Label
pending_count "local -Qu vs sync DBs last synced 2026-10-18T14:11:00-0300". No HEALTHY/clearance/ABI/process claim.
Digest proves JSON↔snapshot consistency at REV, not that the self-asserted capture is true host state.

## Impacted axes / coordination
freshness, calibration; others untouched. Items 1–9 sent to `TsukuroiR15.IncidentMeasure`; D1/D2 to `TsukuroiR15.IncidentEntry`.

## Limits
Measure code not reviewed (absent). Exit semantics from v7.1.0 source, no pacman run, no host commands, no tests.
Historical 413 provenance not re-derived (AttackStaleCounts lane).

## Tools
Read-only: python3 stdlib, sha256sum, git check-ignore/status/ls-files/config, man, curl (gitlab raw). Installs: none.
