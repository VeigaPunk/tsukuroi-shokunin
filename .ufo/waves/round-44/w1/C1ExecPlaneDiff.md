VERDICT: supports

# C1-4 — kill rule "a PLANE line, the rollup line or the exit code changes": live back-to-back diff of base vs measured revision

Item: export the census at `98020ece0674e0b569ee23aed10ffbee355b248e` (base) and
`7e081698d4fc3c4ea944884fd093058de9909de1` (measured), run both on the live host three times
alternating, drop the header (timestamp) and the SCRUB line, diff. Any other difference must be
shown to recur between two runs of *the same* revision (live drift) or it falsifies.

Result: after dropping the header and the SCRUB line, **the two revisions are indistinguishable**
— every remaining difference is confined to four live kernel counters on the `PLANE drivers` line,
and the identical set of substitutions also appears between two runs of the same revision. Exit
code is `2` in all six runs. The kill rule does not fire.

## 1. Provenance of the two scripts

Exported read-only from the lane object store into scratch (no lane write):

```
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 98020ece0674e0b569ee23aed10ffbee355b248e:tools/tsukuroi-census.sh > base.sh
git -C ... show 7e081698d4fc3c4ea944884fd093058de9909de1:tools/tsukuroi-census.sh > impl.sh
```

- `base.sh` 3220 lines, sha256 `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9`
- `impl.sh` 3396 lines, sha256 `fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c`
  (file `script-sha256.txt` in the receipt dir)

Path-independence of the exported copy: `SELF` is used only inside the selftest path
(`impl.sh:457`, consumers `impl.sh:2286,2333`); live mode never reads it, so running the copies
from scratch measures the same live-mode code the lane would run.

Measured revision's emit site — the new line sits after STORAGE and before the rollup, exactly as
declared (`impl.sh:3371-3378`):

```
3371  probe_storage_arm
3372  printf '%s\n' "$STORAGE_LINE"
3375  probe_scrub_record
3376  printf '%s\n' "$SCRUB_LINE"
3378  local roll=HEALTHY
```

## 2. Run protocol

Driver `probe.sh` (receipt dir), `TMPDIR=/fast/scratch/hyaku/tsukuroi-r44/C1ExecPlaneDiff/s`,
`cd` into scratch, `/usr/bin/bash <rev>.sh > out-<rev>-<n>.txt 2> err-<rev>-<n>.txt`, exit code
captured to `rc-<rev>-<n>.txt`. Order base, impl, base, impl, base, impl. Observed header
timestamps (`run-order-headers.txt`) prove the alternation:

```
base-1  tsukuroi-census census-v2 — host=plazir27 — 2026-10-27T00:06:31Z — read-only
impl-1  tsukuroi-census census-v2 — host=plazir27 — 2026-10-27T00:06:33Z — read-only
base-2  tsukuroi-census census-v2 — host=plazir27 — 2026-10-27T00:06:36Z — read-only
impl-2  tsukuroi-census census-v2 — host=plazir27 — 2026-10-27T00:06:38Z — read-only
base-3  tsukuroi-census census-v2 — host=plazir27 — 2026-10-27T00:06:41Z — read-only
impl-3  tsukuroi-census census-v2 — host=plazir27 — 2026-10-27T00:06:43Z — read-only
```

Raw line counts: base 12, impl 13 — one extra line, and it is the SCRUB line (§5). stderr was
0 bytes in all six runs. Whole-batch wall time 14.0 s (`time bash probe.sh`, `real 0m13.982s`).

## 3. Line sequence (after dropping the header) — identical shapes

base: `PLANE packages`, `PLANE systemd`, `PLANE drivers`, `PLANE journal`, `PLANE update-safety`,
`PLANE oom`, `HANDOFF ADJ-04 mori class=kill-events`, `HANDOFF ADJ-04 mori class=coredumps`,
`DRIFT pacnew-plane`, `STORAGE btrfs-device-stats`, `TSUKUROI_CENSUS`
impl: the same eleven plus `SCRUB btrfs-scrub-record` between `STORAGE` and `TSUKUROI_CENSUS`.

## 4. Diff after dropping the header line and the SCRUB line

### 4a. Masked comparison: the four live counters are the *only* thing that ever differs

Masking `C5_pswp=…`, `C6_avail_kb=…`, `C6_psi_full_total_us=…`, `C6_shmem_kb=…` on the `PLANE
drivers` line and sha256-ing the remaining 11 lines:

```
base-1  9ea737f7688a368e594eafbc5ac9453644e2a3b7c2e8f53c458aa9f8f8abd2e3
base-2  9ea737f7688a368e594eafbc5ac9453644e2a3b7c2e8f53c458aa9f8f8abd2e3
base-3  9ea737f7688a368e594eafbc5ac9453644e2a3b7c2e8f53c458aa9f8f8abd2e3
impl-1  9ea737f7688a368e594eafbc5ac9453644e2a3b7c2e8f53c458aa9f8f8abd2e3
impl-2  9ea737f7688a368e594eafbc5ac9453644e2a3b7c2e8f53c458aa9f8f8abd2e3
impl-3  9ea737f7688a368e594eafbc5ac9453644e2a3b7c2e8f53c458aa9f8f8abd2e3
```

One hash for all six runs, both revisions: `diff` over masked files is empty, and token counts
per line are equal in every pair (no field added or removed anywhere). PLANE verdicts, PLANE
notes, both HANDOFF lines, `DRIFT pacnew-plane`, `STORAGE btrfs-device-stats`, the rollup and
its parentheses are byte-identical across all six runs.

### 4b. Token substitutions, all nine base×impl pairs (`fielddiff.txt`)

```
### base-1 vs impl-1
  line[PLANE drivers:]: token substitutions=4
    C5_pswp=484282/1803297  ->  C5_pswp=484287/1803297
    C6_psi_full_total_us=51072073  ->  C6_psi_full_total_us=51072135
    C6_avail_kb=19741148  ->  C6_avail_kb=19730472
    C6_shmem_kb=5372;  ->  C6_shmem_kb=5368;
  (all other lines byte-identical)
### base-2 vs impl-2
  line[PLANE drivers:]: token substitutions=3
    C5_pswp=484292/1803297  ->  C5_pswp=484297/1803297
    C6_psi_full_total_us=51073323  ->  C6_psi_full_total_us=51078207
    C6_avail_kb=19742652  ->  C6_avail_kb=19017764
  (all other lines byte-identical)
### base-3 vs impl-3
  line[PLANE drivers:]: token substitutions=4
    C5_pswp=484304/1803297  ->  C5_pswp=484310/1803297
    C6_psi_full_total_us=51084781  ->  C6_psi_full_total_us=51084785
    C6_avail_kb=19623888  ->  C6_avail_kb=19748324
    C6_shmem_kb=5396;  ->  C6_shmem_kb=5372;
  (all other lines byte-identical)
```

The remaining six cross-pairs (`base-1 vs impl-2`, `base-1 vs impl-3`, `base-2 vs impl-1`,
`base-2 vs impl-3`, `base-3 vs impl-1`, `base-3 vs impl-2`) report the same field names and 3–4
substitutions each; full transcript in the receipt `fielddiff.txt`. Field name set over all nine
pairs, and over all fifteen pairs: exactly
`{C5_pswp, C6_psi_full_total_us, C6_avail_kb, C6_shmem_kb}`.

### 4c. The same differences recur between two runs of the *same* revision

```
base-1 vs base-2  fields=[C5_pswp, C6_avail_kb, C6_psi_full_total_us]               (3 subs)
base-1 vs base-3  fields=[C5_pswp, C6_avail_kb, C6_psi_full_total_us, C6_shmem_kb]  (4 subs)
base-2 vs base-3  fields=[C5_pswp, C6_avail_kb, C6_psi_full_total_us, C6_shmem_kb]  (4 subs)
impl-1 vs impl-2  fields=[C5_pswp, C6_avail_kb, C6_psi_full_total_us, C6_shmem_kb]  (4 subs)
impl-1 vs impl-3  fields=[C5_pswp, C6_avail_kb, C6_psi_full_total_us, C6_shmem_kb]  (4 subs)
impl-2 vs impl-3  fields=[C5_pswp, C6_avail_kb, C6_psi_full_total_us, C6_shmem_kb]  (3 subs)
```

So "explained by live drift between runs" is shown directly, not inferred: base↔base and
impl↔impl differ in the same four fields, with no revision in the picture.

### 4d. The drift has the shape of a monotone kernel counter, not of a revision effect

`C5_pswp` is `pswpin/pswpout` read from `$CGROUP_ROOT/$MEM_SLICE/memory.stat`
(`impl.sh:1205-1206`: `ps_in=$(mem_field "$slice/memory.stat" pswpin)`;
`ps_out=$(mem_field ... pswpout)`, emitted at `impl.sh:1261`);
`C6_psi_full_total_us` is `/proc/pressure/memory`'s `full total`
(`impl.sh:1233-1243`), `C6_avail_kb` is `MemAvailable` and `C6_shmem_kb` is `Shmem` from
`/proc/meminfo` (`impl.sh:1231-1232`). Ordered by the header timestamps of §2:

```
run     time (Z)      C5_pswp              C6_psi_full_total_us
base-1  00:06:31      484282/1803297       51072073
impl-1  00:06:33      484287/1803297       51072135
base-2  00:06:36      484292/1803297       51073323
impl-2  00:06:38      484297/1803297       51078207
base-3  00:06:41      484304/1803297       51084781
impl-3  00:06:43      484310/1803297       51084785
```

`pswpout` advances +5 per census run and `psi full total` advances monotonically, in *wall-clock
order across revisions* — i.e. the value is a function of when the run happened, not of which
script ran. Successive `pswpout` increments over the six runs are +5, +5, +5, +7, +6 regardless
of whether the transition crosses revisions (base→impl, impl→base) or not, so the measured
revision does not perturb the counter. The arm also cannot affect the line in its own run: the
mem arm is probed and the drivers line is computed (`impl.sh:3334-3335`) before `probe_scrub_record`
runs at `impl.sh:3375`. `C6_avail_kb`/`C6_shmem_kb` move in both directions (19.74 GB → 19.03 GB
→ 19.75 GB across the six runs) as the machine's page cache moves, which is also why they are
sometimes equal and sometimes not. Independent read of the live counters after the batch confirms
the same counters are moving: `/proc/vmstat` `pswpout 1809274`, `/proc/pressure/memory`
`full ... total=51186104`, `/proc/meminfo` `MemAvailable: 19065244 kB` / `Shmem: 5420 kB` —
all beyond the last census value, i.e. still advancing.

## 5. Exit code — identical

```
rc-base-1=2 rc-base-2=2 rc-base-3=2 rc-impl-1=2 rc-impl-2=2 rc-impl-3=2
```

(2 = BLOCKED, from `packages=BLOCKED` + `update-safety=BLOCKED`; rollup line identical in both:
`TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED
update-safety=BLOCKED oom=DEGRADED)`.)

## 6. The one added line, for completeness

Present only in the measured revision, exactly once, stable content across its three runs, and
positioned after `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`
and before the rollup:

```
SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0
```

Base emits no SCRUB line in any of its three runs. This line is the declared C1 addition and was
dropped per the assignment; it is not a PLANE line, not the rollup, and it changes no exit code
(§4a: the rollup and exit code are unchanged with it present).

## 7. Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w1/C1ExecPlaneDiff/`
(144 KB, 24 files): `out-{base,impl}-{1,2,3}.txt` (raw stdout), `rc-*.txt`,
`norm-out-*.txt` (header+SCRUB dropped), `fielddiff.txt`, `run-order-headers.txt`,
`time-order.txt`, `script-sha256.txt`, `probe.sh`, `SHA256SUMS`. The six stderr captures were
0 bytes each (`wc -c err-*.txt` → all 0) and are not copied.

Scratch `/fast/scratch/hyaku/tsukuroi-r44/C1ExecPlaneDiff/` removed at exit.

## 8. Scope and what I did not do

- Not run: the census selftest, `score-scrub-arm-r44.py`, `check-scrub-record-r44.py`, the
  predecessor storage counters. They belong to other C1-* items; the kill rule I own is the live
  PLANE/rollup/exit-code diff only.
- Not assessed: whether the arm creates a file in live mode (separate kill-rule bullet), the
  `state=` semantics of the SCRUB line, and any wave-2 verdict binding.
- No tool installs, no host mutation: only `git show` (read-only), six census executions
  (read-only by construction), and `cat /proc/{vmstat,meminfo,pressure/memory}`.

## 9. Proposal

No text change. The kill rule stays as written; this item passes.
