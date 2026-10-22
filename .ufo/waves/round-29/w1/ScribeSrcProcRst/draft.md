# S148 — Linux v7.2 `Documentation/filesystems/proc.rst` (OOM badness and `oom_score_adj`)

Draft by seat `TsukuroiR29.ScribeSrcProcRst`, round 29 wave 1, 2026-10-22. Nothing here is
applied to `corpus/SOURCES.md` or `corpus/lessons/round-29.md`; the L1 lands it.

## Fetch record

- Source id S148, canonical URL (as reserved in the round-29 brief):
  `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst`.
- **The canonical URL returned HTTP 429** (`429: Too Many Requests`, 199 bytes) to plain
  `curl -sL` twice, 20 s apart, on 2026-10-22; body kept at
  `.ufo/waves/round-29/w1/ScribeSrcProcRst/raw-429-body.txt`. No bot challenge was encountered
  or bypassed.
- Bytes were fetched by plain `curl -sL` from two independent carriers of the same `v7.2` tag,
  both HTTP 200:
  - `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/filesystems/proc.rst?h=v7.2`
    → `proc-kernelorg.rst`
  - `https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/Documentation/filesystems/proc.rst`
    → `S148-proc.rst`
- `cmp proc-kernelorg.rst S148-proc.rst` → identical; both sha256
  `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`, 107560 bytes, 2495 lines.
  The jsDelivr carrier serves the GitHub tag blob, so the hash is the GitHub `v7.2` blob content
  [inf]; the two-carrier agreement is [obs].
- Snapshot path used in the registry row: `.ufo/waves/round-29/w1/ScribeSrcProcRst/S148-proc.rst`.

## 1. Registry row for `corpus/SOURCES.md`

Single line, 11 columns in the order `id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by`. No cell contains a `|`.

| S148 | Linux v7.2 Documentation/filesystems/proc.rst — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst | docs | A | The OOM badness heuristic that selects a victim: the 0-1000 range as an approximate proportion of a task's allowed memory, how oom_score_adj is added and its -1000 to +1000 range, the oom_adj legacy scale and the exported oom_score range, for the host kernel 7.2.11 | tag v7.2, Documentation/filesystems/proc.rst sections 3.1 and 3.2, lines 1761-1766, 1777-1783, 1793-1797 and 1811-1812; raw bytes sha256 e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126; snapshot .ufo/waves/round-29/w1/ScribeSrcProcRst/S148-proc.rst (2495 lines, 107560 bytes); raw.githubusercontent.com answered HTTP 429 to plain curl on 2026-10-22 so the identical bytes came from git.kernel.org plain at h=v7.2 and cdn.jsdelivr.net gh@v7.2 (cmp clean) | Badness is a score from 0 (never kill) to 1000 (always kill) that is roughly a proportion of the allowed memory a task may allocate; /proc/<pid>/oom_score_adj is added to that score before the kill decision, its acceptable values are -1000 to +1000 where -1000 always reports a badness of 0 and so disables oom killing for the task; the exported /proc/<pid>/oom_score includes the adjustment and is therefore effectively in range [0,2000] | mined | 2026-10-22 | on-release | corpus/knowledge/oom-event-plane.md, corpus/knowledge/kill-event-deep-r8.md |

## 2. Lesson Gate row (round-29 candidate gate)

Six columns, the round-28 shape.

| Source | URL | Opened | Located quote (at most 25 words) | Location | Decision |
|---|---|---|---|---|---|
| S148 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst | 2026-10-22 | "The value of /proc/<pid>/oom_score_adj is added to the badness score" | `.ufo/waves/round-29/w1/ScribeSrcProcRst/S148-proc.rst` line 1777, sha256 `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`; the sentence continues on line 1778 with `is used to determine which task to kill.` (quote is the contiguous first clause; see the wrap note below) | admit, `mined`, tier A (upstream kernel documentation for the running 7.2 series); used-by the O01 to O04 correction markers in `corpus/knowledge/oom-event-plane.md` and `corpus/knowledge/kill-event-deep-r8.md` |

Quote verification, run in the snapshot directory:

- `grep -cF "The value of /proc/<pid>/oom_score_adj is added to the badness score" S148-proc.rst`
  → `1` [obs]
- `grep -cF "The value of /proc/<pid>/oom_score_adj is added to the badness score before it is used to determine which task to kill." S148-proc.rst`
  → `0`, because the source wraps the sentence after `before it` [obs]

**Wrap note (important for M3-style exactness elsewhere):** this file wraps prose at about 79
columns, so most sentences here are not single-line substrings. The Gate quote above is the
maximal contiguous prefix of the decisive sentence, verified by `grep -cF`. The source lines are:

```
1777: The value of /proc/<pid>/oom_score_adj is added to the badness score before it
1778: is used to determine which task to kill.  Acceptable values range from -1000
```

## 3. Extraction — every victim-selection sentence, with source lines

Each sentence below occupies the stated lines. Sentences are shown with the source's line wraps
joined by single spaces for readability; the exact wrapped slice of each was located in
`S148-proc.rst` programmatically and occurs **exactly once** in the file (all 25 checked). The
section headings are line 1755 (`3.1 /proc/<pid>/oom_adj & /proc/<pid>/oom_score_adj - Adjust the
oom-killer score`) and line 1804 (`3.2 /proc/<pid>/oom_score - Display current oom-killer
score`).

### 3.1 Badness as a proportion of allowed memory

| Lines | Sentence |
|---|---|
| 1757-1759 | These files can be used to adjust the badness heuristic used to select which process gets killed in out of memory (oom) conditions. |
| 1761-1762 | The badness heuristic assigns a value to each candidate task ranging from 0 (never kill) to 1000 (always kill) to determine which process is targeted. |
| 1762-1764 | The units are roughly a proportion along that range of allowed memory the process may allocate from based on an estimation of its current memory and swap use. |
| 1765-1766 | For example, if a task is using all allowed memory, its badness score will be 1000. |
| 1766-1766 | If it is using half of its allowed memory, its score will be 500. |
| 1768-1769 | The amount of "allowed" memory depends on the context in which the oom killer was called. |
| 1769-1771 | If it is due to the memory assigned to the allocating task's cpuset being exhausted, the allowed memory represents the set of mems assigned to that cpuset. |
| 1771-1772 | If it is due to a mempolicy's node(s) being exhausted, the allowed memory represents the set of mempolicy nodes. |
| 1772-1774 | If it is due to a memory limit (or swap limit) being reached, the allowed memory is that configured limit. |
| 1774-1775 | Finally, if it is due to the entire system being out of memory, the allowed memory represents all allocatable resources. |

### 3.2 Adding the value, and the -1000 to +1000 range

| Lines | Sentence |
|---|---|
| 1777-1778 | The value of /proc/<pid>/oom_score_adj is added to the badness score before it is used to determine which task to kill. |
| 1778-1779 | Acceptable values range from -1000 (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX). |
| 1779-1781 | This allows userspace to polarize the preference for oom killing either by always preferring a certain task or completely disabling it. |
| 1781-1783 | The lowest possible value, -1000, is equivalent to disabling oom killing entirely for that task since it will always report a badness score of 0. |
| 1785-1786 | Consequently, it is very simple for userspace to define the amount of memory to consider for each task. |
| 1786-1789 | Setting a /proc/<pid>/oom_score_adj value of +500, for example, is roughly equivalent to allowing the remainder of tasks sharing the same system, cpuset, mempolicy, or memory controller resources to use at least 50% more memory. |
| 1789-1791 | A value of -500, on the other hand, would be roughly equivalent to discounting 50% of the task's allowed memory from being considered as scoring against the task. |

### 3.3 Legacy `oom_adj` and the `CAP_SYS_RESOURCE` floor

| Lines | Sentence |
|---|---|
| 1793-1794 | For backwards compatibility with previous kernels, /proc/<pid>/oom_adj may also be used to tune the badness score. |
| 1794-1796 | Its acceptable values range from -16 (OOM_ADJUST_MIN) to +15 (OOM_ADJUST_MAX) and a special value of -17 (OOM_DISABLE) to disable oom killing entirely for that task. |
| 1796-1797 | Its value is scaled linearly with /proc/<pid>/oom_score_adj. |
| 1799-1800 | The value of /proc/<pid>/oom_score_adj may be reduced no lower than the last value set by a CAP_SYS_RESOURCE process. |
| 1800-1801 | To reduce the value any lower requires CAP_SYS_RESOURCE. |

### 3.4 What `/proc/<pid>/oom_score` exports (section 3.2)

| Lines | Sentence |
|---|---|
| 1806-1808 | This file can be used to check the current score used by the oom-killer for any given `<pid>`. |
| 1808-1809 | Use it together with /proc/<pid>/oom_score_adj to tune which process should be killed in an out-of-memory situation. |
| 1811-1812 | Please note that the exported value includes oom_score_adj so it is effectively in range [0,2000]. |

## 4. What S148 establishes for O01 to O04, and what it does not

The four frozen anchors (read-only from the lane at the dispatch state, `grep -cF` → 1 each):

- O01 `corpus/knowledge/oom-event-plane.md:116` — "exactly the band the kernel scans first"
- O02 `corpus/knowledge/oom-event-plane.md:349` — "the +200 band is chosen first"
- O03 `corpus/knowledge/kill-event-deep-r8.md:147` — "under a kernel OOM the scan prefers the higher-scored, larger-RSS tasks first"
- O04 `corpus/knowledge/kill-event-deep-r8.md:260` — "the +200 band is scanned first"

What S148 supports [obs, from the sentences above]:

- The selection quantity is a continuous per-task score, 0 to 1000, computed as a proportion of
  that task's allowed memory from "an estimation of its current memory and swap use" (1761-1764).
  Nothing in the file describes discrete bands or a scan that visits one band first.
- `oom_score_adj` is **added** to that score (1777-1778); its range is -1000 to +1000 (1778-1779);
  -1000 makes the task always report a badness of 0, which disables killing it (1781-1783).
- `oom_score_adj` acts as an offset on a continuous scale: +500 is described as roughly letting
  other tasks use 50% more memory, and -500 as discounting 50% of the task's allowed memory
  (1786-1791).
- The value the corpus quotes from `/proc/<pid>/oom_score` **already contains** the adjustment and
  is therefore in range [0,2000], not [0,1000] (1811-1812). So a measured `oom_score` of 200 for a
  task at `oom_score_adj` +200 corresponds to a raw badness near 0, not to a special selection
  band.

What S148 does not establish [unk]:

- The selection loop, its ordering, and tie-breaking. The file says the score is used "to determine
  which process is targeted" (1761-1762) but never states "highest wins" or any iteration order;
  that is `mm/oom_kill.c`, reserved this round as S149 and outside this seat's slice.
- Any preference for larger RSS. RSS can only enter through "an estimation of its current memory
  and swap use" (1763-1764); the file makes no ranking claim for it. O03's "larger-RSS tasks first"
  is therefore not supported by S148 [inf].

Recommended verdicts, for the executor who writes the markers: `qualified` for O01, O02, O04 (the
adjustment is a scalar added to a 0-1000 proportional score, and the exported score already mixes
the two, so the "+200 band" reading is a misreading of the exported value rather than a described
kernel mechanism), and `qualified` for O03 (the score ordering is documented in substance, the
RSS clause is not). A `rebutted` verdict on the scan order would overreach on S148 alone, because
the file is silent on order [inf].

Mechanical constraints the landing markers inherit from `tools/check-owed-statements-r29.py`
(`M1` to `M7`, docstring at lines 18-38; parser at lines 90-186): one marker line per id in the
exact shape `[R29-OWED-<id>] verdict: <v> | original: "<anchor>" | now: <text> | basis: <refs>`;
`now` at least 12 words, not containing the anchor, unique across all twelve; `basis` must name
`S148`, whose row above is `mined` and whose used-by names both target basenames, so the S148
reference alone satisfies M6 and, for O01 to O04, M7. Candidate `now` texts (distinct, each 22 to
25 words, none containing its anchor; the L1 or executor must still check uniqueness against
O05 to O12):

- O01: "The selection score is a continuous 0-1000 badness value, a proportion of allowed memory, to which oom_score_adj is added; the documentation names no scanned band."
- O02: "A +200 adjustment raises a task's badness by 200 points on a 0-1000 scale rather than defining a band the kernel visits first."
- O03: "The score reflects memory and swap use as a proportion of allowed memory; this text gives no scan order and no larger-RSS preference."
- O04: "The kernel adds oom_score_adj to a per-task badness score between 0 and 1000; the documentation describes no scanned +200 band."

## 5. Limits

- The canonical `raw.githubusercontent.com` URL could not be fetched (HTTP 429); the row records
  that honestly and names the two byte-identical carriers. [obs]
- Sentence boundaries were split on a period followed by whitespace, which is exact for this
  section (no abbreviations), and each raw slice was asserted to occur once in the file. [obs]
- The bearing section's verdict recommendation is an inference from documentation text, not a
  reading of `mm/oom_kill.c`; the reserved S149 is the decisive source for scan order. [inf]
- No lane file was edited by this seat; the rows above are draft text only.
