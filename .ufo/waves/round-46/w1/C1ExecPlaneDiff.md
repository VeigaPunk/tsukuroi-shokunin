VERDICT: supports

# C1-3 — kill rule "a PLANE/HANDOFF/DRIFT/STORAGE/SCRUB/TSUKUROI_CENSUS line changes shape or the live exit code changes"

**Result: the kill rule did NOT fire.** Base `2042117c` and implementation `a4477049` produce the
same live census line set, the same line shapes, and the same exit code. The only live output
difference is value drift inside the `mem=` arm of `PLANE drivers:`, and every one of those
drifting fields also drifts between two runs of a *single* revision (both directions measured),
which is exactly the "drift recurring within one revision" exemption.

## Artifacts (read-only evidence)

Exports (`git -C <lane> show <rev>:tools/tsukuroi-census.sh`), byte digests observed:

```
237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc  base.sh   (2042117cfb724170772f4c128cc2ddba0b61d817)  3485 lines
d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa  impl.sh   (a44770491eb5ca15ce9f8b3207309d1af683ffaf)  3598 lines
```

Receipts, this seat dir `.ufo/waves/round-46/w1/C1ExecPlaneDiff/`:
`base.sh`, `impl.sh`, `script.diff`, `run-{B1,B2,B3,I1,I2,I3}.{out,err,rc}`,
`pairwise-diff.txt`, `rc-and-shape.txt`.

## Method

Scratch `/fast/scratch/hyaku/tsukuroi-r46/C1ExecPlaneDiff/`, `TMPDIR` set inside it, cwd inside it,
`bash ./<rev>.sh` with **no flags**, alternating back to back in the order
B1, I1, B2, I2, B3, I3 (three live runs per revision, interleaved). Each run ~8.0 s
(`time` on B1: `real 0m8.000s`). stdout and exit code captured separately; stderr captured
(0 bytes in all six runs). Diff performed after `tail -n +2` (header line carries a UTC timestamp).

Header, all six runs (only the timestamp varies — expected, not a shape change):

```
run-B1: tsukuroi-census census-v2 — host=plazir27 — 2026-10-27T05:22:35Z — read-only
run-I1: tsukuroi-census census-v2 — host=plazir27 — 2026-10-27T05:22:54Z — read-only
run-B2: …05:23:01Z   run-I2: …05:23:08Z   run-B3: …05:23:15Z   run-I3: …05:23:22Z
```

## Exit code — unchanged

```
run-B1 rc=2 lines=13   run-I1 rc=2 lines=13
run-B2 rc=2 lines=13   run-I2 rc=2 lines=13
run-B3 rc=2 lines=13   run-I3 rc=2 lines=13
```

All six runs: 13 stdout lines (header + 12 census lines), 0 stderr bytes, exit 2.
(`rc-and-shape.txt`.) Exit 2 = BLOCKED, and it is host state, not the revision: both revisions
report `PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: openai-chatgpt: missing
required signature; …)` and `PLANE update-safety: BLOCKED (status=BLOCKED; qu=rc=1/2 …)`
(`run-B1.out:2`, `run-B1.out:6`; identical in `run-I1.out:2,6`).

## Line set and order — unchanged

Prefix sequence, identical in every run (`cut -d: -f1 run-*.body`):

```
PLANE ×6 → HANDOFF ×2 → DRIFT → STORAGE → SCRUB → TSUKUROI_CENSUS
```

Same count, same order, same family names in base and impl.

## Shape — unchanged

Values masked with `sed -E 's/=[^ ;)]*/=<v>/g'`, then diffed. Every pair, including all
cross-revision pairs, is **IDENTICAL** (`rc-and-shape.txt`):

```
B1 vs I1: IDENTICAL   B2 vs I2: IDENTICAL   B3 vs I3: IDENTICAL
B1 vs B2: IDENTICAL   B1 vs B3: IDENTICAL   I1 vs I2: IDENTICAL   I1 vs I3: IDENTICAL
```

This masks values but preserves key names, key order, separators and every literal
(`[unknown: accepted noise floor]`, `guards=max/max oom.group=0`, `r6 vocab: …`), so a field
rename, reorder, addition, deletion or punctuation change would have shown.

## The one differing line, and why it is exempt

Every pairwise diff is exactly `3c3` — body line 3, `PLANE drivers:` (`pairwise-diff.txt`):

```
B1 vs B2: 3c3   B1 vs B3: 3c3   I1 vs I2: 3c3   I1 vs I3: 3c3   B1 vs I1: 3c3   B2 vs I2: 3c3   B3 vs I3: 3c3
```

Body lines 1,2,4,5,6,7,8,9,10,11,12 (both `PLANE systemd/journal/update-safety/oom`, both
`HANDOFF`, `DRIFT`, `STORAGE`, `SCRUB` and the `TSUKUROI_CENSUS:` rollup) are **byte-identical
across all six runs**. In particular the four verdict-neutral arms named in the kill rule are
byte-identical, not merely shape-equal:

```
DRIFT pacnew-plane pacnew=3 pacsave=0 pacorig=0 unreadable=11 log_pacnew=3 log_pacsave=0 unlogged=0 gone=0 log=ok
STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0
SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0
TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)
```

Field-level drift in the `mem=[DEGRADED] …` arm (diff of parsed `k=v` pairs against B1):

| field | B1 | B2 | B3 | I1 | I2 | I3 | drifts within base? | within impl? |
|---|---|---|---|---|---|---|---|---|
| `C5_pswp` | 976241/2966950 | 980396/2975783 | 980980/2977925 | 979278/2975655 | 980875/2977447 | 981562/2980579 | yes | yes |
| `C5_sock_throttled` | 104049 | 104049 | 104049 | 104049 | 104049 | **104054** | no | yes (I1→I3) |
| `C6_psi_some_avg300` | 0.58 | 0.56 | 0.54 | 0.56 | 0.55 | 0.64 | yes | yes |
| `C6_psi_full_avg300` | 0.29 | 0.29 | 0.29 | 0.29 | 0.29 | **0.33** | no | yes (I1→I3) |
| `C6_psi_full_total_us` | 89864539 | 90000495 | 90101491 | 89954310 | 90060733 | 90279718 | yes | yes |
| `C6_avail_kb` | 13076116 | 12281252 | 11878888 | 13181260 | 11977132 | 9025952 | yes | yes |
| `C6_shmem_kb` | 19540 | 43400 | 46928 | 41020 | 50684 | 52360 | yes | yes |

Both fields whose cross-revision delta appears only in I3 (`C5_sock_throttled`, `C6_psi_full_avg300`)
also differ between **I1 and I3 — two runs of one revision** (`diff run-I1.body run-I3.body` shows
`C5_sock_throttled=104049` vs `104054` and `C6_psi_full_avg300=0.29` vs `0.33`). Every drifting
field is therefore monotone live host state (`/proc/meminfo` MemAvailable/Shmem, `/proc/pressure/memory`,
swap counters), not revision behaviour: no field moved in base-and-not-impl or impl-and-not-base.

## Source-line clause "a census line at or before :3383 moves" — not violated

Source diff `script.diff` has exactly five hunks, all 1:1 or insertions **after** base :3396:

```
@@ -452,7 +452,7 @@     (1:1)  SELF=${BASH_SOURCE[0]} -> SELF=${BASH_SOURCE[0]:-}   [impl:455]
@@ -591,7 +591,7 @@     (1:1)  usage: line gains [--identity]                        [impl:594]
@@ -602,7 +602,7 @@     (1:1)  usage Exit map: sentence gains the --identity clause  [impl:605]
@@ -3381,16 +3381,121 @@ (insertion starts after base :3396)
@@ -3405,6 +3510,14 @@  (insertion: --identity dispatch in main())
```

The three pre-:3383 hunks are equal-length replacements, so **no line number at or before :3383
shifts**, and the pre-:3383 line *constructors* are byte-identical at the same line numbers:

```
1898: IDENTICAL   DRIFT_LINE="DRIFT pacnew-plane pacnew=$pn pacsave=$ps pacorig=$po …
1959: IDENTICAL   STORAGE_LINE="STORAGE btrfs-device-stats state=$state filesystems=$f…
2039: IDENTICAL   SCRUB_LINE="SCRUB btrfs-scrub-record state=$state dir=$ds records=$r…
```

The emitters in `main()` did move, but all of them sit **after** :3383, which the clause permits:

```
base: 3430-3435 six PLANE printf   3447/3451 HANDOFF   3457/3461/3465 DRIFT/STORAGE/SCRUB   3475 TSUKUROI_CENSUS
impl: 3543-3548 six PLANE printf   3560/3564 HANDOFF   3570/3574/3578 DRIFT/STORAGE/SCRUB   3588 TSUKUROI_CENSUS
```

Largest emitter line number at or before :3383 is 2039 in both revisions — unchanged.
The three changed lines (455, 594, 605) are the `SELF` default and two `usage:` documentation
strings; none of them is a `PLANE`/`HANDOFF`/`DRIFT`/`STORAGE`/`SCRUB`/`TSUKUROI_CENSUS` output
statement, and none is at a moved position. `SELF` is read only inside the selftest
(`base.sh:2289,2336` → `impl.sh:2289,2336`), so the `:-` default is inert in live mode — confirmed
by the byte-identical live output above.

## Notes, limits, what I did not do

- The host is BLOCKED live (`pacman -Qkk` signature error on `openai-chatgpt`, `pacman -Qu` rc=1/2),
  so the packages and update-safety planes ran their BLOCKED path in both revisions. The differential
  is still valid (same host, interleaved runs), but the HEALTHY-path rendering of those two planes was
  not exercised by a live run here; that is covered by the frozen counter's fixture cases, not by me.
- `TSUKUROI_CENSUS_IDENTITY:` is a new prefix that begins with `TSUKUROI_CENSUS`. It is emitted only
  under `--identity` and is absent from all six no-flag runs (`run-*.out` line count 13), so the
  rollup-line shape is untouched; recorded only as a textual-prefix observation for whoever greps
  `^TSUKUROI_CENSUS` over output.
- Not run by me (other seats own them): the `--identity` selftest cases, the census selftest as a
  whole, `score-census-identity-r46.py`, `check-scrub-admission-r46.py`, `check-adjacency-anchors`,
  and the write-detection clause (whether the census writes a file in live/identity mode). I ran no
  counter and no selftest, so nothing here speaks to those predicates.
- No host mutation, no lane write, no package transaction, no tool install. Scratch removed.
