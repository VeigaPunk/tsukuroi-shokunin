VERDICT: supports

Item C1-4 — mutation test of the round-39/40 STORAGE mount-table cross-check guards and
branches at f951f288483c1af0cef4afd458488b84cf7a2165, plus independent confirmation that the
counter's excluded mutant (guard `$fsn` -> `$devn`) is equivalent. All six assigned mutants
are KILLED by the census `--selftest`; the excluded mutant could not be made to change the
STORAGE line by any fixture I could construct, and is unreachable-divergent by the code's
structure. The C1 claim's guard/branch coverage holds.

# Method

- Scratch clone, never the lane: `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r40/C1HeldOutGuards/clone && git -C <clone> remote remove origin`; `git -C <clone> rev-parse --show-toplevel` printed the clone dir itself; `git -C <clone> rev-parse HEAD` = f951f288483c1af0cef4afd458488b84cf7a2165 (matches dispatch tip). Pristine census sha256
  `032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733` (identical to the lane copy).
- Detector: `bash <variant>.sh --selftest` with `PATH=/usr/bin:/bin LC_ALL=C HOME=<run> TMPDIR=<run>/tmp`, cwd `/` — mirroring the frozen counter's runner (tools/score-selftest-literals-r40.py:92-104). Bounded at 180 s, run in its own session; on timeout SIGKILL to my own process group only (no pattern kills). Each mutant was applied as an exact substring replacement to a **copy**; the clone's census file was never modified.
- Restoration evidence: sha256 of the clone census before and after all runs = `032faa8f…` (summary.json `restored_equal: true`), and the detector re-run on the restored bytes also passes (receipts/restored.out).
- Baseline: `TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)` — receipts/baseline.out. A baseline failure would have made every mutant inconclusive; it passed, twice.

# Mutant results (arm = probe_storage_arm, tools/tsukuroi-census.sh:1865-1925; arm not modified — mutants applied to scratch copies)

| id | exact change (line) | verdict | deciding case (receipt) |
|----|---------------------|---------|--------------------------|
| Ga | drop `[ -f "$PROC_MOUNTS" ]`: line 1911 becomes `if mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null) && [ -n "$mtab" ]; then` | KILLED (hang; SIGKILL at my 180 s cap, rc 137) | `storage-mounts-fifo` (census.sh:2999-3002): the census `cat`s the FIFO and blocks forever; receipts/Ga-drop-file-guard.out ends after the `storage-mounted-populated` ok line with no FAIL line and no final PASS line |
| Gb | drop `[ -n "$mtab" ]`: line 1911 becomes `if [ -f "$PROC_MOUNTS" ] && mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null); then` | KILLED (rc 1) | `storage-mounts-empty` (census.sh:3004-3007): empty file passes the guard, loop counts 0, prints `HEALTHY filesystems=0 devices=0 nonzero=0` where `…state=BLOCKED … detail=mounts:unreadable$` is pinned |
| Gc | swap the two detail tokens: `mounts:btrfs-without-sysfs,` ↔ `mounts:unreadable,` (lines 1915/1917; token-level, commas included, each unique in the file) | KILLED (rc 1, 7 cases) | `storage-hidden-absent` (census.sh:2986-2989) decides: mt>0 branch now writes `mounts:unreadable`, so the pinned `detail=mounts:btrfs-without-sysfs$` misses. Full fail list in receipts/gc2-fixed.out: hidden-absent, hidden-empty, mounts-unreadable, fifo, empty, varied-home, varied-multi |
| Gd | `blocked=1` -> `blocked=0` in the unreadable branch: line 1917 becomes `blocked=0; detail+='mounts:unreadable,'` | KILLED (rc 1) | `storage-mounts-unreadable` (census.sh:2981-2983): state flips to HEALTHY with the detail still printed; pinned `state=BLOCKED … detail=mounts:unreadable$` misses |
| Ge | read `/proc/mounts` instead of `$PROC_MOUNTS`: line 1911 becomes `if [ -f /proc/mounts ] && mtab=$(cat -- /proc/mounts 2>/dev/null) && [ -n "$mtab" ]; then` | KILLED (rc 1) | `storage-absent` (census.sh:2932-2934) decides on this host: the arm reads the host's real mount table (4 btrfs lines: `grep -c btrfs /proc/mounts` = 4) instead of the fixture table. Direct mechanism check (same env as the selftest's check, minimal fixture): pristine → `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0`; mutant → `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` |
| Gf | round-38 root:unreadable branch reordered after the table read: the `if [ -d "$root" ] && { [ ! -r … ] …}` branch (census.sh:1870-1872) moved to execute after the `if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]` block (1906-1919); loop branch demoted from `elif` to `if`; single body | KILLED (rc 1, exactly 1 case) | `storage-root-unreadable-mounted` (census.sh:3079-3083, round-40 fixture): table read now runs first and appends `mounts:btrfs-without-sysfs`, so the pinned `detail=root:unreadable$` misses. Notably the R38 case `storage-root-unreadable` (3005-3008 region) still passes under the clean reorder — only the round-40 fixture catches this mutant |

Every mutant run's last line and first FAIL labels are in receipts/*.out; machine-readable
summary (hashes, rc, timed flags, tails) in receipts/summary.json.

# Discarded first constructions (my own bugs — recorded, corrected, re-run)

- Gc first attempt swapped the two whole lines (the `mt>0` guard line and the else-branch body) instead of the tokens. That made the then-branch set `blocked=1; detail+='mounts:unreadable,'` **unconditionally** for any readable non-empty table, and moved the `mt>0` conditional into the else branch — 10 failures including `storage-absent`, which a true token swap cannot touch (confirmed by instrumented scratch copies dumping the per-case STORAGE line: pristine `state=HEALTHY …nonzero=0` vs bad-swap `state=BLOCKED … detail=mounts:unreadable`, receipts/debug-pristine.out, receipts/debug-gc.out). Discarded; the token-level swap above is the intended mutant.
- Gf first attempt double-appended the token (`detail=root:unreadable,root:unreadable`): my moved-branch slice already contained the original body line and I appended it a second time. Discarded; the single-body reorder above is the intended mutant (receipts/Gf-DISCARDED-double-body.out, receipts/debug-gf.out).

Both corrected runs are the ones scored above (receipts/gc2-fixed.out, receipts/gf2-fixed.out).

# Excluded mutant (guard `$fsn` -> `$devn`, line 1906): equivalent — attempt and confirmation

The counter excludes exactly this mutant with the reason "devn > 0 implies fsn > 0, and fsn > 0
with devn == 0 sets blocked=1 first" (tools/score-selftest-literals-r40.py:23-25). I tried to
break it independently:

- Structural argument from the code: `devn` is incremented only at census.sh:1880, inside the
  per-fsid loop, after `fsn` was incremented at 1877 — so `devn>0 ⟹ fsn>0`. If `fsn>0` while
  `devn=0`, every fsid dir had zero counted devinfo entries, so census.sh:1903
  (`if [ "$nd" -eq 0 ]; then blocked=1; …no-devinfo…`) already set `blocked=1`, making the
  unchanged second conjunct `[ "$blocked" -eq 0 ]` false under both the original and the mutant.
  The two guard predicates `(fsn=0 ∧ blocked=0)` and `(devn=0 ∧ blocked=0)` therefore agree on
  every reachable state; the divergent states (`fsn=0 ∧ devn>0`, `fsn>0 ∧ devn=0 ∧ blocked=0`)
  are unreachable.
- Empirical attempt (four sysfs fixtures, pristine vs guard-mutant census, same env as the
  selftest's check; receipts/excluded-mutant-ab.json, all four `identical: true`):
  - E1 fsn=1 devn=0 (fsid dir, no devinfo): both → `state=BLOCKED filesystems=1 devices=0 nonzero=0 detail=11111111:-:no-devinfo`
  - E2 fsn=0 (no btrfs root), btrfs-free table: both → `state=HEALTHY filesystems=0 devices=0 nonzero=0`
  - E3 fsn=1 devn=1 clean + btrfs in table: both → `state=HEALTHY filesystems=1 devices=1 nonzero=0` (table never read)
  - E4 adversarial: fsid dir whose devinfo holds only a **broken symlink** (glob expands, `[ -e ]` fails, entry never counted): both → `state=BLOCKED filesystems=1 devices=0 nonzero=0 detail=11111111:-:no-devinfo`
- Conclusion: no fixture can make this mutant change the STORAGE line; the counter's exclusion
  is justified. This is a structural unreachability argument plus a four-fixture empirical
  check, not an exhaustive search over all fixture spaces.

# Bounds / not done

- I did not run the frozen counter `score-selftest-literals-r40.py` itself (already scored with
  pre-data controls per the declaration; not this item), did not touch any other census arm,
  the lane working tree, Git index/jj state, sibling lanes, or the host (no installs, no sudo,
  no pacman, no service changes; the only host reads were /proc/mounts and the read-only
  census probes during the direct Ge/A-B runs).
- Ga's kill is a hang-kill (bounded timeout), not an assertion failure: no FAIL line exists for
  it; the deciding case is pinned by the last completed ok line plus the case order at
  census.sh:2999-3002.
- Lane footprint: only `.ufo/waves/round-40/w1/C1HeldOutGuards.md` and the receipts under
  `.ufo/waves/round-40/w1/C1HeldOutGuards/`. Pre-existing unrelated dirt observed in lane
  status (modified `.ufo/waves/round-40/make-w1-spec.py`, untracked `w1.ready.dispatched`) is
  not mine and was left untouched. Scratch `/fast/scratch/hyaku/tsukuroi-r40/C1HeldOutGuards`
  is removed after this report; no tool installs were made (none needed).
