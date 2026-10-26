VERDICT: defect-found

Item C1-6 — mutation test of the mount-table read in `probe_storage_arm` (tools/tsukuroi-census.sh at 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82). Four mutants built and each run against both frozen detectors. Two killed, two survived with demonstrated separating inputs. The C1 claim itself is not falsified — the arm at 49cc53c implements the fstype-field rule; the defects found are coverage gaps in the two frozen detectors (selftest and counter), and both gaps are in the over-blocking direction (false BLOCKED, never a false all-clear).

## Method

- Target block: tools/tsukuroi-census.sh:1903-1914 at 49cc53c (blob sha256 e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d; the lane file hash is identical before and after this seat's work).
- Harness: one pristine clone + four mutant clones under /fast/scratch/hyaku/tsukuroi-r39/C1MutParse/ (`git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$D"`; `git -C "$D" remote remove origin`; `git -C "$D" rev-parse --show-toplevel` verified equal to $D for every clone; HEAD master @ 394e1ba). Each mutant committed on master with fixture identity `C1MutParse r39w1 fixture <c1mutparse@r39w1.invalid>`; working tree clean after each commit (status --porcelain empty).
- Detectors: (1) `bash <clone>/tools/tsukuroi-census.sh --selftest` with TMPDIR=$S/tmp; (2) the frozen counter tools/score-storage-hidden-r39.py, sha256 75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973 (matches the declared 75a9e8ab prefix), run as `python3 <clone>/tools/score-storage-hidden-r39.py --repo "$D" --revision <mutant sha> --branch master --scratch $S/s`.
- Baseline on pristine bytes (revision 49cc53c, run twice — before and after all mutant runs): selftest exit 0, `TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)`; counter exit 0 PASS, hidden_matched=2 views_matched=3 fixtures_matched=5 live_match=1 six_planes_all=1. Receipts: base-selftest.txt, base-counter.json, base2-selftest.txt, base2-counter.json. With a green baseline, mutant outcomes below are conclusive, not inconclusive.
- No tool was installed or upgraded (none needed); no sudo, no pacman transaction, no host mutation; the only mounts were the counter's own `unshare -rm` tmpfs legs.

## Results

- (a) `grep -c btrfs` anywhere — mutant census.sh:1907 replaces the fstype-field loop with `mt=$(printf '%s\n' "$mtab" | grep -c btrfs || true)`. Selftest PASS 117/117. Counter PASS. **SURVIVED both.**
- (b) case-insensitive fstype — mutant census.sh:1908 `[ "${fst:-}" = btrfs ]` → `[ "${fst,,}" = btrfs ]`. Selftest PASS 117/117. Counter PASS. **SURVIVED both.**
- (c) first line only — mutant adds `break` after the fstype test (mutant census.sh:1909). Selftest FAIL 116/117. Counter PASS. **KILLED by the selftest.**
- (d) hardcoded /proc/mounts — mutant census.sh:1906 `cat -- "$PROC_MOUNTS"` → `cat -- /proc/mounts`. Selftest FAIL 115/117. Counter FAIL (fixtures_matched=3/5). **KILLED by both.**

Mutant commits (scratch clones only): (a) 7e84444dba7d3cb2878406d584cd88cf834d440f, (b) f60f9f4486c74e38edad8c300a4f4e338637efd4, (c) 7951fea8229264eedd0324a076c1611377dfa1b6, (d) 1a8950fe75905427bf673152bce65ac0f4399995. Mutant blob sha256s: (a) 02d65269b9c3cc7dd598c202d7286d54e8a8f62bb6c62fb34dafe2e27ca71d88, (b) ec2b95509099d8cb57b4f81c9a2a6091e777465c7790fab7301f1459fbbd6c20, (c) b9f44808de1aae5644bef2a090ace6d375e693a3d454aca3be683e2a2e8e12c1, (d) 4745eaf4113b9172c9b000f76de8ac7d51f8515a70a581bcc0cfbd0aa0ffa98a. hashes.txt shows each commit's `git show HEAD:tools/tsukuroi-census.sh` lines 1906-1910, proving the counter read the mutated bytes at each --revision.

## Survivor (a) — `grep -c btrfs` matches btrfs anywhere in the line

Why both detectors miss it: every table either detector feeds the arm has "btrfs" only in the fstype field (counter M_BTRFS; selftest fxmt, census.sh:2973) or not at all (M_NONE; fx_default, census.sh:2030), and on this host all four `grep btrfs /proc/self/mounts` hits are fstype-field hits (awk '$3=="btrfs"' | wc -l = 4 = grep -c; observed 2026-10-26). grep's count is a superset of the fstype-field count, so every BLOCKED expectation still matches and every HEALTHY expectation still sees mt=0.

Separating input (receipt sep-demo.txt, run 2026-10-26T06:09:32Z; TSUKUROI_BTRFS_SYSFS absent, TSUKUROI_PROC_MOUNTS overridden):

```
proc /proc proc rw 0 0
/dev/sdb1 /mnt/old-btrfs-mirror ext4 rw,relatime 0 0
```

- pristine: `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0`
- mutant (a): `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs`

The rule keys on the mount's fstype field (census.sh:366 "with a btrfs mount listed"; the loop reads field 3, census.sh:1907-1908); a line whose fstype is ext4 with "btrfs" in the mountpoint (same class: source or option field) is not a btrfs mount. Direction: over-blocking only — the mutant cannot cause the false all-clear the claim guards; it causes false BLOCKEDs.

Where it should live: the selftest. The counter is frozen this round (sha256 pinned in the declaration), and fstype-field precision is arm grammar, which the selftest owns — it already carries the four round-39 mount-table cases at census.sh:2972-2992. Proposed case (NOT applied — read-only seat), inserted after the storage-hidden-empty case (census.sh:2982):

```bash
  case_home='storage-mounts-fstypish'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'proc /proc proc rw 0 0\n/dev/sdb1 /mnt/old-btrfs-mirror ext4 rw,relatime 0 0\n' > "$FX/mounts"
  check 'healthy rollup: btrfs in a non-fstype field is never a btrfs mount (R39-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0$'
```

A future counter revision could pin the same shape as an F6 fixture; the frozen r39 counter must not change this round.

## Survivor (b) — case-insensitive fstype

Why both detectors miss it: every fstype either detector exercises is lowercase (kernel fstype strings are lowercase; M_BTRFS, M_NONE, fx_default and fxmt are all lowercase), so exact-match and case-insensitive agree on every covered input.

Separating input (receipt sep-demo.txt; absent root, TSUKUROI_PROC_MOUNTS overridden):

```
proc /proc proc rw 0 0
/dev/fx0 / BTRFS rw,relatime 0 0
```

- pristine: `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0`
- mutant (b): `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs`

An uppercase fstype can only reach the arm through the TSUKUROI_PROC_MOUNTS override the arm explicitly supports (counter fixtures F1-F5; selftest census.sh:2161), and the pinned grammar is exact `btrfs` (census.sh:1908). Direction: over-blocking only.

Where it should live: the selftest, same reasoning as (a). Proposed case:

```bash
  case_home='storage-mounts-case'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'proc /proc proc rw 0 0\n/dev/fx0 / BTRFS rw,relatime 0 0\n' > "$FX/mounts"
  check 'healthy rollup: fstype match is case-sensitive; BTRFS is not btrfs (R39-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0$'
```

## Killed mutant (c) — first line only

- Selftest killed it: FAIL 116/117; the failing check is `healthy rollup: btrfs mounted with no sysfs root is BLOCKED, never 0/0/0 (R39-C1)` (storage-hidden-absent, census.sh:2974-2977). Its table writes `proc /proc proc rw 0 0` FIRST and the btrfs line second (census.sh:2975), so first-line-only reads fstype=proc → mt=0 → HEALTHY where BLOCKED detail=mounts:btrfs-without-sysfs is required. This is the dangerous direction — a real btrfs mount missed — and the selftest catches it.
- Counter did NOT kill it on this host: counter PASS (hidden 2/2, views 3/3, fixtures 5/5, live 1/1, m-c-counter.json). Reason: the host's first /proc/self/mounts line is `/dev/mapper/root / btrfs ...` (observed 2026-10-26), so H1/H2 still see btrfs on line 1; both btrfs fixtures (F2, F5) use M_BTRFS, which also puts btrfs first; F1/F4's M_NONE starts with `proc /proc proc rw 0 0` → mt=0 → HEALTHY as expected. Robustness note: against first-line mutants the counter's hidden legs are host-table-order-dependent; the selftest is the load-bearing detector for this class. A later counter revision could pin line position by reordering M_BTRFS to put the btrfs line second.

## Killed mutant (d) — hardcoded /proc/mounts

/proc/mounts is a symlink to /proc/self/mounts (`ls -l /proc/mounts` → `self/mounts`), so the mutant is observationally identical wherever TSUKUROI_PROC_MOUNTS is not overridden; the override fixtures are what separate it.

- Selftest killed it: FAIL 115/117, two checks:
  - `healthy: no btrfs sysfs root reads as no btrfs filesystem, 0/0/0 (R38-C1)` (storage-absent, census.sh:2925-2927): the fixture table has no btrfs and expects HEALTHY 0/0/0; the mutant read the host's real table (4 btrfs mounts) → BLOCKED.
  - `healthy rollup: an unreadable mount table with no sysfs root is BLOCKED (R39-C1)` (storage-mounts-unreadable, census.sh:2984-2987): expected detail=mounts:unreadable; the mutant read the readable host table → detail=mounts:btrfs-without-sysfs.
- Counter killed it: FAIL, fixtures_matched=3/5 (m-d-counter.json):
  - F1-absent-root-no-btrfs-mounted: expected HEALTHY 0/0/0, got BLOCKED detail=mounts:btrfs-without-sysfs.
  - F3-absent-root-mounts-unreadable: expected detail=mounts:unreadable, got detail=mounts:btrfs-without-sysfs.
  - F4 survives only because its populated root short-circuits the mount-table block (census.sh:1903 guard `fsn -eq 0 && blocked -eq 0`); F2/F5 coincide with this host's state (host has btrfs → the same BLOCKED line). On a host without btrfs the same mutant would instead be killed by F2/F5 and by the selftest's storage-hidden-absent — killed either way.

## Restoration evidence

- Mutants never touched lane bytes: all four lived in scratch clones. The lane's tools/tsukuroi-census.sh sha256 is e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d before and after all runs (hashes.txt).
- Detector re-run on pristine bytes after all mutant runs: selftest PASS 117/117 (base2-selftest.txt), counter PASS 2/3/5/1/1 (base2-counter.json).
- Scratch /fast/scratch/hyaku/tsukuroi-r39/C1MutParse removed after receipts were copied into the seat dir.
- Pre-existing lane state observed before this seat wrote anything, not mine, left untouched: `git status --porcelain` shows ` M PROVINCE.md` and ` M SKILL.md` (insertions only, +14/+21; lane-predirty.txt).

## Not done

- Only the four assigned mutants were probed; no additional mutant classes (e.g. removing the census.sh:1903 guard) were built.
- The two proposed selftest cases were NOT added (read-only seat; exact text above is a proposal for the author seat).
- The frozen counter was not modified.
