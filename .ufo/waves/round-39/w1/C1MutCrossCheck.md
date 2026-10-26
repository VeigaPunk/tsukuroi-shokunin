VERDICT: defect-found

Item C1-5 — mutation test of the round-39 mount-table guard in `probe_storage_arm`
(tools/tsukuroi-census.sh at 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82, block at lines
1903-1916; R38-ABSENT-ROOT). Two of six mutants (d: devn guard, e: dropped
`blocked -eq 0` conjunct) SURVIVED both the census selftest and the frozen r39 counter.
That is a test-power finding on the harnesses, not a falsification of the C1 claim; per
seat role it does not authorize any contract change.

# Setup (what ran)

- Mutants were applied only to throwaway `git clone -q --shared` copies of the lane under
  `/fast/scratch/hyaku/tsukuroi-r39/C1MutCrossCheck/` (one clone per mutant), committed on
  master with fixture identity `fixture C1MutCrossCheck <c1mutcrosscheck@fixture.invalid>`
  after `git rev-parse --show-toplevel` equality checks; every variant changed exactly one
  file (seat receipt changed-files.txt lists `tools/tsukuroi-census.sh` 6 times, nothing else).
- The lane itself was never modified: sha256 of tools/tsukuroi-census.sh was
  `e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d` before the runs
  (receipts/hashes-before.txt line 1) and identical after (receipts/restore.sha line 4).
  The census blob at 49cc53c, at clone tip 394e1ba4 (HEAD of each clone, verified with
  `git diff --quiet 49cc53c... HEAD -- tools/tsukuroi-census.sh` per clone), and in the
  worktree are byte-identical.
- Counter provenance: worktree tools/score-storage-hidden-r39.py sha256
  `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973` equals
  `git show 6a08925daa30767809eb13bb4b01448ff954d46a:tools/score-storage-hidden-r39.py`
  (both hashes observed), so the frozen counter bytes were the detector. Invocation:
  `python3 tools/score-storage-hidden-r39.py --repo <clone> --revision <mutant sha> --scratch
  /fast/scratch/hyaku/tsukuroi-r39/C1MutCrossCheck/s`; selftest: `TMPDIR=<scratch> bash
  <clone>/tools/tsukuroi-census.sh --selftest`.
- Baseline gate: pristine clone at 394e1ba4 → selftest PASS (117 cases, 117 passed, 0 failed;
  base.selftest.log line 120) and counter PASS (hidden 2/2, views 3/3, fixtures 5/5, live 1/1,
  six_planes_all 1; base.counter.json). A pass on pristine is the precondition for calling any
  mutant run below a kill. Consistent with the lane's own controls (controls/controls.jsonl:
  C1-K0-do-nothing FAIL hidden=0/2 fixtures=2/5; C1-K4-candidate PASS).
- `unshare -rm` + tmpfs smoke check passed before the runs (`NS-OK` observed); no tool was
  installed or upgraded for this item; no pacman transaction, no host mutation.

# Per-mutant results (KILLED/SURVIVED per harness)

Pristine census sha256 in every row below: `e5666331caf08477…`; mutant file hashes in
receipts/hashes-before.txt lines 2-7. Full outputs: receipts/<tag>.selftest.log,
receipts/<tag>.counter.json, receipts/<tag>.patch.

| # | Mutant (single point) | Variant commit | Selftest (117 cases) | Frozen counter | Verdict |
|---|---|---|---|---|---|
| a | `:1910` `[ "$mt" -gt 0 ]` → `-gt 1` | cc6a2be8aaee1dab3d837f3eff21afe133eaa86d | FAIL 115/117 — `storage-hidden-absent`, `storage-hidden-empty` | FAIL — fixtures 3/5: F2-absent-root-btrfs-mounted and F5-empty-root-btrfs-mounted got `HEALTHY 0/0/0` (mut-a.counter.json) | KILLED / KILLED |
| b | `:1908` match 2nd mounts field `_mp` instead of 3rd `fst` | e759793ad03f0a1792d18f5883cba93d43f10fdb | FAIL 115/117 — same two cases | FAIL — hidden 0/2 (H1+H2 got `HEALTHY 0/0/0`) and fixtures 3/5 (F2, F5) | KILLED / KILLED |
| c | `:1911-1913` unreadable-mounts else branch → `:` | f442f35c75a92569bf65b596eb4c9d9020aefd0b | FAIL 116/117 — `storage-mounts-unreadable` | FAIL — fixtures 4/5: F3-absent-root-mounts-unreadable got `HEALTHY 0/0/0` (expected BLOCKED detail=mounts:unreadable) | KILLED / KILLED |
| d | `:1903` guard `[ "$fsn" -eq 0 ]` → `[ "$devn" -eq 0 ]` | 13f94f93a6600764759223cc13492d848d6923f0 | PASS 117/117 | PASS — all legs (hidden 2/2, views 3/3, fixtures 5/5, live 1/1) | SURVIVED / SURVIVED |
| e | `:1903` guard drops `&& [ "$blocked" -eq 0 ]` | 1b6139e79acbe7e35b2139fd86f2ae4fcd10b596 | PASS 117/117 | PASS — all legs | SURVIVED / SURVIVED |
| f | `:1910` detail token `mounts:btrfs-without-sysfs` → `…sysxf` | 9a287a33db9097a266e33d640ffb79348d03825f | FAIL 115/117 — `storage-hidden-absent`, `storage-hidden-empty` | FAIL — hidden 0/2 + fixtures 3/5 (F2, F5): got `detail=mounts:btrfs-without-sysxf` | KILLED / KILLED |

Observed nuance worth keeping: for mut-a the hidden namespace legs did NOT decide the kill on
this host — H1/H2 still emitted `detail=mounts:btrfs-without-sysfs` because the namespace
mount table here carries ≥2 btrfs subvolume mounts, so `-gt 1` still fires. The deterministic
deciders for (a) were the single-btrfs-line fixtures F2/F5 and the two selftest cases. On a
host with exactly one btrfs mount the hidden legs alone would miss this mutant.

# The two coverage findings (surviving mutants)

1. mut-d (fsn → devn): equivalent-in-practice mutant. `devn` only increments inside an fsid
   directory's devinfo loop (tools/tsukuroi-census.sh:1867-1868), so in every state where the
   guard is reachable with `blocked=0`, `fsn=0 ⇔ devn=0`; and `fsn≥1 ∧ devn=0` always sets
   `blocked=1` via `no-devinfo` (:1892-1893). Neither harness can distinguish the two texts.
   Finding: the selftest and counter cannot pin WHICH zero-count variable guards the mount
   table — a refactor that switches the guard to a wrong-but-same-behavior variable is
   invisible. Low severity (behavior today is identical); noted as test-power only.
2. mut-e (dropped `blocked -eq 0`): genuine untested conjunct. The mutant only diverges in the
   state `blocked=1 ∧ fsn=0` (reachable as root:unreadable) with a btrfs line in the mount
   table: pristine prints `detail=root:unreadable`, mutant prints
   `detail=root:unreadable,mounts:btrfs-without-sysfs`. No harness constructs that state: the
   selftest's root-unreadable case keeps `fx_default`'s mounts fixture, which has no btrfs
   line (tools/tsukuroi-census.sh:2035-2036 `printf 'proc /proc proc rw,nosuid 0 0\n/dev/fx0
   / ext4 rw,relatime 0 0\n' > "$d/mounts"`), and the counter's FIXTURES
   (score-storage-hidden-r39.py:44-50) have no unreadable-root entry. The state stays BLOCKED
   either way (detail-token drift only), so the claim's predicate still holds; severity low,
   but the `blocked -eq 0` conjunct is currently untested by construction. Planner input (not
   a contract change): one selftest case pairing `chmod 000 "$FX/btrfs"` with a btrfs mounts
   line, asserting `^STORAGE … detail=root:unreadable$`, would kill it.

# Restoration evidence

- mut-f's clone was returned to pristine bytes: `git checkout <base rev> -- tools/…`, commit
  df646e29c15dbfeeea279badc26a95305ad3275e; file sha256 returned to
  `e5666331caf08477…` and `cmp` reports byte-identical to the pristine clone
  (receipts/restore.sha, lines 1-3: "RESTORED bytes identical to pristine").
- Both detectors re-run on the restored bytes: selftest PASS 117/117, counter PASS all legs
  (restore.counter.json) — the detectors pass on pristine, fail on mutant, pass again on
  restored.
- No mutant, fixture, or clone ever touched the lane, the fleet repo, or the host; all seven
  clones plus scratch were removed after receipts were copied to this seat dir
  (.ufo/waves/round-39/w1/C1MutCrossCheck/).

# Not done

- Only the six requested mutants were run; no additional mutants (e.g. an inverted fstype
  comparison or a mounts-file parse split) were probed.
- The counter's live leg depends on this host's real /sys/fs/btrfs and /proc/self/mounts; its
  PASS values are environment-dependent (it passed identically in the lane's own controls).
