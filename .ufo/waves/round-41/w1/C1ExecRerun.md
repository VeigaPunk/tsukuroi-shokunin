VERDICT: supports

Seat C1ExecRerun, item C1-1 (independent re-run of the round-41 C1 counter at implementation revision
568c397). Everything below is a command I ran and its observed output. I ran the counter exactly once
(`--jobs 4`) and ran no other selftest, no controls and no C2 check.

## 1. Tool hash — matches the declaration in three independent places

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum tools/score-selftest-mounts-r41.py
8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c  tools/score-selftest-mounts-r41.py
$ git show e479fdc54d0977ccd8112a42d8d139baaebcb02e:tools/score-selftest-mounts-r41.py | sha256sum
8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c  -
$ git show 568c397da11339aed65181be598414f268835555:tools/score-selftest-mounts-r41.py | sha256sum
8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c  -
$ git diff --stat e479fdc54d0977ccd8112a42d8d139baaebcb02e 71851d636ab1bffaf8fee5016617c88878a666f1 -- tools/score-selftest-mounts-r41.py tools/_revision.py
(no output: counter and its _revision helper are byte-identical from the frozen counter commit to the
dispatch tip 71851d63)
$ git status --porcelain tools/_revision.py tools/score-selftest-mounts-r41.py
(no output: neither file is dirty in the worktree)
```

Claimed sha256 `8306d999...7355c` is confirmed against both the frozen counter commit and the
implementation revision. The counter's import graph (`tools/_revision.py`) is also unchanged, so the
hash pins the behaviour that produced the receipts.

## 2. The single run

```
$ export TMPDIR=/fast/scratch/hyaku/tsukuroi-r41/C1ExecRerun/s
$ python3 tools/score-selftest-mounts-r41.py --revision 568c397da11339aed65181be598414f268835555 \
    --scratch /fast/scratch/hyaku/tsukuroi-r41/C1ExecRerun/s --jobs 4
2026-10-26T18:04:04Z ... RC=0 ... 2026-10-26T18:11:43Z
real 7m39.722s  user 42m58.391s  sys 35m11.390s   (stderr empty)
```

Receipt (self-describing, header + verbatim counter stdout):
`.ufo/waves/round-41/w1/C1ExecRerun/c1-rerun-568c397.jsonl`
sha256 `6a50efa3c2dd8893e80f5a3d6d21b0fbb55905c56a97d18df5e858f5134c3949`; embedded counter payload
sha256 `5cfba59c68fdbd50c3f09b05e1d0bf42914766153ae4ed14f881891c65b87597` (62215 bytes).
Field-by-field comparison artefact: `.ufo/waves/round-41/w1/C1ExecRerun/field-compare.json`
sha256 `4eddd14252f666f492e34757b8d8c72a73537335292e3c07481591cbad10c0ae`.

Observed predicate inputs at 568c397:

| field | value |
|---|---|
| revision | `568c397da11339aed65181be598414f268835555` |
| branch_tip (observed) | `71851d636ab1bffaf8fee5016617c88878a666f1` |
| baseline | `PASS (128 cases, 128 passed, 0 failed)`, exit 0, pass true |
| baseline_labels | 128 |
| capture_pass | 1 |
| neutral_pass | 3 (N1-rename-counter, N2-double-bracket, N3-awk-field all pass, occurrences 1) |
| decoy_pass | 1 (D-all-mutant-texts, pass, occurrences 1) |
| mutants_applied | 13 (all occurrences 1) |
| survivors | 0 (`survivor_names: []`) |
| params | 4 |
| result / exit | PASS / 0 |

All 13 frozen mutants `killed == true` with `confirmed == true` and non-empty `confirm_labels`:
M1-VA-device-literal, M2-VB-root-mountpoint, M3-VC-substring-btrfs, M4-VG-subvolid-256,
M5-a-grep-count, M6-b-fstype-casefold, M7-e-guard-drops-blocked, M8-subvol-at-literal,
M9-last-line-only, H5-mountpoint-absolute, H6-source-devonly, H9-subvolkey-option,
H10-count-exactly-one.

The four declared table shapes are attributed to the four new cases by name and fixture capture:

```
P1-mountpoint-not-absolute -> ["healthy rollup: a btrfs line whose mountpoint is not absolute still counts, BLOCKED (R41-C1 H5)"]
P2-source-not-dev          -> ["healthy rollup: a btrfs line whose source is not under /dev still counts, BLOCKED (R41-C1 H6)"]
P3-no-subvol-option        -> ["healthy rollup: a btrfs line with no subvol= option still counts, BLOCKED (R41-C1 H9)"]
P4-two-btrfs-lines         -> ["healthy rollup: two btrfs lines are still btrfs without sysfs, BLOCKED (R41-C1 H10)"]
```

## 3. Comparison with the author receipt `.ufo/waves/round-41/after/c1-after-568c397.jsonl`

Author receipt header read structurally: `revision 568c397...`, `tool_revision e479fdc...`,
`tool_sha256 8306d999...7355c`, `argv --revision 568c397... --scratch .../L1/rr-c1a --jobs 6 --timeout 1500`,
`started_utc 2026-10-26T17:17:35Z`; embedded body `result PASS`, `exit 0`.

Every predicate-relevant field is **identical** between that receipt and my re-run:
`revision`, `baseline` (same `PASS (128 cases, 128 passed, 0 failed)`, exit 0, cases 128),
`baseline_pass 1`, `capture_pass 1`, `neutral_pass 3`, `decoy_pass 1`, `mutants_applied 13`,
`survivors 0`, `survivor_names []`, `params 4`, `result PASS`, `exit 0`, all four `param_cases` label
lists (byte-identical), and for each of the 16 runs: `occurrences`, `pass`, `exit`, `cases`,
`killed`, `confirmed`, `confirm_labels`. No difference in any of those.

Only non-predicate detail differs, in the *initial* (unconfirmed) run's failing-case count and summary
line of six mutants, because host-dependent, non-mount arms fail or pass per run:

```
H9-subvolkey-option   fail_count author 2 / rerun 1   last: 126 passed,2 failed -> 127 passed,1 failed
M2-VB-root-mountpoint fail_count author 6 / rerun 5   last: 122 passed,6 failed -> 123 passed,5 failed
M4-VG-subvolid-256    fail_count author 6 / rerun 5   last: 122 passed,6 failed -> 123 passed,5 failed
M5-a-grep-count       fail_count author 2 / rerun 1   last: 126 passed,2 failed -> 127 passed,1 failed
M8-subvol-at-literal  fail_count author 5 / rerun 6   last: 123 passed,5 failed -> 122 passed,6 failed
M9-last-line-only     fail_count author 3 / rerun 2   last: 125 passed,3 failed -> 126 passed,2 failed
```

Cause, from the receipts' `first_fails`: the extra author-side failures are host-read arms, e.g.
`FAIL healthy: a dated kill event routes one kill-events handoff ... (R32-C1): hostname override not
honoured` (author M2) and `FAIL healthy: privilege artifacts counted, not drift (D05): hostname
override not honoured` (author M9); these do not appear in my run, and mine shows no non-mount label
anywhere. This cannot move a kill verdict, which needs a baseline label failing twice
(`failed_base_labels` intersect, `tools/score-selftest-mounts-r41.py:190-200`, applied at
`:264-272` and `:287`): across all 13 mutants in my run there are **0 non-mount labels** in any `confirm_labels`.
For H5/H6/H9/H10 the confirm set is exactly the one intended case:

```
H5-mountpoint-absolute -> ["healthy rollup: a btrfs line whose mountpoint is not absolute still counts, BLOCKED (R41-C1 H5)"]
H6-source-devonly      -> ["healthy rollup: a btrfs line whose source is not under /dev still counts, BLOCKED (R41-C1 H6)"]
H9-subvolkey-option    -> ["healthy rollup: a btrfs line with no subvol= option still counts, BLOCKED (R41-C1 H9)"]
H10-count-exactly-one  -> ["healthy rollup: two btrfs lines are still btrfs without sysfs, BLOCKED (R41-C1 H10)"]
```

So the four held-out mutants die on the new mount-table cases specifically, not on collateral.
Neither run needed the serial retry (`retried` absent on every record in both receipts).

## 4. Comparison with `.ufo/waves/round-41/before/c1-before.jsonl` (base 0e5805a)

Read structurally; header `revision 0e5805a1f149bd2ed9fe0db2e0a832afb034a835`,
`tool_sha256 8306d999...7355c`, `argv ... --jobs 6 --timeout 1500`. Body: `result FAIL`, `exit 1`,
`baseline PASS (124 cases, 124 passed, 0 failed)`, `mutants_applied 13`, `neutral_pass 3`,
`decoy_pass 1`, `params 0`, and

```
survivor_names ['H10-count-exactly-one', 'H5-mountpoint-absolute', 'H6-source-devonly', 'H9-subvolkey-option']
```

which is exactly the declared "before: survivors 4 (H5, H6, H9, H10), params 0, FAIL". The 124 -> 128
baseline case delta equals the four added cases. My re-run at 568c397 therefore differs from the before
receipt in precisely the direction claimed: those four mutants flip from `pass:true, killed:false` to
`pass:false, killed:true, confirmed:true`, params 0 -> 4, FAIL -> PASS.

## 5. Implementation-shape spot check (read-only, `git show`)

```
$ git diff --stat 0e5805a 568c397 -- tools/tsukuroi-census.sh
 tools/tsukuroi-census.sh | 27 +++++++++++++++++++++++++++
 1 file changed, 27 insertions(+), 0 deletions(-)
$ git log -1 --format='%H %s' 568c397
568c397da11339aed65181be598414f268835555 round-41: C1 census selftest gains four held-out mount tables (H5, H6, H9, H10)
$ git merge-base --is-ancestor 0e5805a 568c397 && echo ok
ok
```

One hunk only, `@@ -3034,6 +3034,33 @@`, 27 insertions and 0 deletions; `probe_storage_arm`
(`tools/tsukuroi-census.sh:1908-1915` in the file at 568c397) is outside the hunk and untouched, as
declared. The four fixture tables are exactly the declared shapes (`git show 568c397:tools/tsukuroi-census.sh`
lines 3037-3064): `'/dev/vdc1 relative/mnt btrfs ...'` (mountpoint not absolute, H5),
`'UUID=0b1c2d3e-... /data btrfs ...'` (source not under /dev, H6), `'/dev/sdc1 /mnt/plain btrfs rw,commit=60 0 0'`
(no `subvol=` option, H9), and a two-line table `/ btrfs ...` + `/home btrfs ...` (H10). Case labels are
at lines 3042, 3048, 3054, 3061 of that blob.

## 6. Risks / limits of this receipt

- `fail_count` and the `FAIL (N cases, ...)` line of an *unconfirmed* mutant run are not reproducible
  numbers: they move with host-read arms (see §3). Do not use them as stability evidence; use `killed`
  + `confirm_labels`, which were identical here.
- The kill-attribution rule is label intersection across two runs of the same mutant text; a mutant
  whose kill came only from a flaky host arm that happened to fail twice would still be counted. In this
  run that risk is nil for all 13 mutants (0 non-mount confirm labels), but the rule itself is a
  property of the counter, not of this re-run.
- The counter reads the census via `git show <rev>:tools/tsukuroi-census.sh` (`:212-213`), so it did not
  depend on the lane worktree, which at run time carried an unrelated dirty `tools/check-self-assessment.py`
  and untracked `.ufo/waves/round-41/` files.
- Lane tip during my run was `71851d63`; `branch_tip` in my receipt records that value, while the author
  receipt records `c7c40c0f`. Both receipts pin `revision 568c397` for the scored content, and the census
  blob is read at that revision, so the tip difference does not enter the score.
- Not done by me: no direct `--selftest` invocation outside the counter, no controls replay, no C2,
  nothing at base re-run (I relied on the before receipt), no package installs or upgrades (none
  needed). Scratch `/fast/scratch/hyaku/tsukuroi-r41/C1ExecRerun` was removed after the receipt was
  copied; nothing outside my seat dir and this report was written.
