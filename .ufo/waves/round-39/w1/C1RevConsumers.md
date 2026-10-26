VERDICT: supports

# Item C1-14 — every consumer of the STORAGE line vs the round-39 tokens (seat C1RevConsumers)

Scope: every consumer of the census `STORAGE btrfs-device-stats` line in the lane — programmatic
parsers under `tools/`, the operator decision table in `SKILL.md`, and `corpus/knowledge` — checked
against the round-39 tokens `detail=mounts:btrfs-without-sysfs` / `detail=mounts:unreadable` and the
new BLOCKED-on-absent-root rule (implementation `49cc53c7`). The census is byte-identical from the
implementation commit to the tip I tested: `git log --oneline 49cc53c7..HEAD -- tools/tsukuroi-census.sh`
prints nothing (run 2026-10-26), so tip `394e1ba4` carries the declared implementation bytes. The lane
tip moved after dispatch (`2e1c2a40` → `394e1ba4`, the w1-spec commit); that does not affect this item.

Method: read-only on the lane. Every verdict below carries a code citation; those marked RUN also carry
a counter/selftest execution in a scratch clone (`/fast/scratch/hyaku/tsukuroi-r39/C1RevConsumers/clone`,
`git clone -q --shared`, origin removed, `git rev-parse --show-toplevel` verified equal to the clone).
Counter bytes I ran are the frozen ones: `sha256sum` → `score-storage-hidden-r39.py`
`75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`, `score-storage-arm-r38.py`
`e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`, `score-storage-arm-r38-q82.py`
`a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3` — matching the declared/registry
digests; `git log 6a08925..HEAD` and `git log 7cbaeb6..HEAD` for those files show no later change
(the q82 file's only commit after `7cbaeb6` is its creation at `9c9bb64`). Receipts `e1.out`–`e5.out`
are in this seat dir. No tools were installed or updated; no pacman, no sudo, no host mutation.

## 1. Programmatic consumers

### 1.1 `tools/score-storage-arm-r38.py` (frozen round-38 gate) — verdict CHANGES, by construction
- Parse: unaffected. `LINE_RE` ends `(?: .*)?$` (`tools/score-storage-arm-r38.py:54-56`), so any
  `detail=` suffix — including the two new tokens — still matches; `parse()` (:164-171) extracts only
  state/filesystems/devices/nonzero.
- Verdict: changes. Fixture `F06-no-btrfs-root` expects `('HEALTHY', 0, 0, 0)` on an absent root
  (:82), and the census child env sets only PATH/LC_ALL/HOME/TMPDIR plus `TSUKUROI_BTRFS_SYSFS`
  (:154-161) — no `TSUKUROI_PROC_MOUNTS`, so the child reads the host's real `/proc/self/mounts`,
  which lists 4 btrfs mounts on this host (`awk '$3=="btrfs"' /proc/self/mounts | wc -l` → 4, run
  2026-10-26). Under the round-39 guard (`tools/tsukuroi-census.sh:1903-1914`: fires when
  `fsn -eq 0 && blocked -eq 0`, reads `$PROC_MOUNTS`) that child now prints
  `... state=BLOCKED ... detail=mounts:btrfs-without-sysfs`.
- RUN e1: `python3 tools/score-storage-arm-r38.py --repo <clone> --revision 394e1ba4… --scratch …`
  → exit 1, `fixtures_matched: 9`, `live_match: 1`, `six_planes_all: 1`; the F06 entry reads
  expected `["HEALTHY",0,0,0]`, got `["BLOCKED",0,0,0]`, storage_lines
  `["STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs"]`
  (e1.out). So the counter FAILs with 9/10 fixtures matched — exactly the "FAILs 9/10 by
  construction" that SKILL.md's round-39 consumer note predicts (:3221-3224).
- RUN e2 (contrast): the same counter at base `0eff65b2` → exit 0, `fixtures_matched: 10`,
  `live_match: 1` (e2.out) — the counter is intact at round-38-lineage revisions, supporting the
  note's "valid at its round-38 revisions (`b0005ae9`)".
- The lane predicted this change before implementing it: `corpus/lessons/round-38.md:88`
  (R38-ABSENT-ROOT) — "a mounts cross-check would change the frozen F06 reading". Not a defect of
  the round-39 claim; it is the documented cost of closing the false all-clear.

### 1.2 `tools/score-storage-arm-r38-q82.py` (frozen round-38 q82 gate) — unaffected
- Parse: reuses the v1 model's `parse` (`tools/score-storage-arm-r38-q82.py:122`), the same loose
  regex as 1.1 — new tokens parse.
- Verdict: unchanged. `draw_tree` (:68-78) always creates 1–3 fsid dirs, each with ≥1
  `devinfo/<devid>/error_stats`; the guard only fires when `fsn -eq 0` (census :1903), so a root
  with fsid entries never reads the mount table and the guard cannot fire in any q82 view.
- RUN e3: `python3 tools/score-storage-arm-r38-q82.py --repo <clone> --revision 394e1ba4…` →
  exit 0, `ns_views_matched: 3`, `ns_available: 1` (e3.out).

### 1.3 `tools/score-storage-hidden-r39.py` (new round-39 gate) — aligned consumer of the new tokens
- Stricter parse: its `LINE_RE` requires the tail to be exactly ` detail=<non-space>` when present
  (:58-59). The arm's tokens are space-free fixed reason tokens (devid is integer-validated and
  never echoed, census :1872-1874; reason tokens are literals at :1909/:1912), so every arm line
  parses. A detail containing a space would fail this counter while passing 1.1's — no arm path
  can produce one.
- It pins the new grammar: `HIDDEN_LINE` (:60-61), fixtures F2/F3/F5 expecting the two new tokens
  (:71-77), and asserts the guard does NOT fire where it must not — views and the live leg require
  `'mounts:' not in detail` (:223, :261).
- RUN e5: `python3 tools/score-storage-hidden-r39.py --repo <clone> --revision 394e1ba4…` →
  exit 0 PASS: hidden 2/2, views 3/3, fixtures 5/5, live 1, six_planes 1 (e5.out).

### 1.4 `tools/score-census-handoff-r32.py` (frozen round-32 gate) — the line is invisible to it
- `parse_output` collects only `PLANE `, `TSUKUROI_CENSUS:` and `HANDOFF ` lines
  (`tools/score-census-handoff-r32.py:504-512`); the STORAGE line is none of these, and the frozen
  predicate (:77-84) compares PLANE lines, the rollup and the exit code against base `58cc2e0b` —
  never the STORAGE line. Its fixtures are oom/journal scenarios; the census child reads the real
  `/sys/fs/btrfs`, which has fsid entries on this host, so the guard never fires in its runs.
  No parse or verdict change. (Code-verified, not run: the 24-scenario battery is out of proportion
  to a parse that provably never sees the line.)

### 1.5 `tools/score-pacnew-arm-r35b.py` (frozen round-35 gate) — already failing, unchanged by r39
- `others()` returns every non-`DRIFT pacnew-plane ` line (:407-408) and the run fails with
  `base parity` when those differ from claim base `b40c01df` (:432-433) — the STORAGE line is
  included, so this gate has read base-parity failures at every revision since `52ffd65`. The
  round-39 tokens change the line's content only in hidden-root scenarios and cannot flip the
  verdict back to passing. Already recorded in the round-38 consumer note (SKILL.md:3147-3149).

### 1.6 The census's own selftest (in-file consumer) — coherent
- The check harness wires `TSUKUROI_PROC_MOUNTS="$FX/mounts"` for every case
  (`tools/tsukuroi-census.sh:2159-2161`), and `fx_default` writes a mounts fixture with no btrfs
  (:2029-2030, comment "round 39: … no btrfs mount, so an absent sysfs root stays 0/0/0") — so the
  round-38 absent-root case (:2926-2927, expects `HEALTHY 0/0/0`) keeps passing, and the four new
  round-39 cases pin the new tokens (:2976-2977 hidden-absent, :2981-2982 hidden-empty,
  :2986-2987 mounts-unreadable, :2991-2992 populated root never reads the table).
- RUN e4: `bash census.sh --selftest` (tip bytes, TMPDIR in scratch) → exit 0,
  `TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)` (e4.out).

## 2. Operator-facing consumers

### 2.1 `SKILL.md` "Storage integrity arm — round 38" — the committed table does NOT cover the new tokens
- The BLOCKED row lists only the five round-38 tokens (`:unreadable` / `:malformed` / `:no-devinfo`
  / `:bad-devid` / `root:unreadable`, SKILL.md:3140) — no `mounts:btrfs-without-sysfs`, no
  `mounts:unreadable`. Row 1 (:3138) still says a namespace that hides `/sys/fs/btrfs` "prints the
  same line" (HEALTHY 0/0/0) — superseded by the round-39 guard whenever the namespace's mount
  table still lists btrfs (the common `unshare -rm` case; the host's 4 btrfs mounts stay visible
  in the child, which is exactly what e1's F06 got). The counting paragraph (:3143-3145) still
  instructs running `score-storage-arm-r38.py`, which at post-r39 revisions FAILs 9/10 by
  construction (e1).
- Remediation is already in flight: the L1 seat holds an uncommitted working-tree append,
  "Storage integrity arm — round 39 (absent or empty sysfs root)" (SKILL.md:3205-3224; +21 lines,
  `git status --porcelain` → ` M SKILL.md`; absent from HEAD — `git show HEAD:SKILL.md | grep -c
  'Storage integrity arm — round 39'` → 0). I checked its three rows (:3214-3216) against the
  implementation and they are accurate, and its F06 consumer note (:3221-3224) matches my e1 run
  (9/10, FAIL). So no SKILL.md draft is needed beyond landing that append; my equivalent draft is
  in §3.1 in case it is dropped.

### 2.2 `PROVINCE.md` — same situation, also covered by the L1's uncommitted append
- The round-38 "Known limit" (:217-218, "an absent sysfs root reads `HEALTHY 0/0/0` … false
  all-clear") is superseded by the uncommitted "Round-39 limit closure — R38-ABSENT-ROOT" section
  (PROVINCE.md:225-235; +14 lines, ` M PROVINCE.md`), which states the new rule and keeps the line
  verdict-neutral. Accurate against the implementation; nothing to draft.

### 2.3 `corpus/README.md` — GAP: stale known-limit sentence, no round-39 append (my draft is §3.2)
- README.md:300 still ends the round-38 frontier notice with "Known limit carried to the frontier:
  an absent `/sys/fs/btrfs` reads `HEALTHY 0/0/0`, so a namespace that hides it gives a false
  all-clear." No round-39 section exists in README (`grep 'Round 39|round-39|mounts:btrfs|
  score-storage-hidden'` over corpus/README.md → no matches, 2026-10-26). SKILL.md and PROVINCE.md
  got supersession notes; README did not. The sentence is false at post-r39 revisions whenever the
  namespace's mount table lists btrfs — the reader is told the arm still gives a false all-clear
  when it now refuses one. Adjacent to this item's enumerated grep surfaces (tools/, SKILL.md,
  corpus/knowledge) but within "every consumer of the STORAGE line in the lane"; flagged for the
  planner, draft provided.

### 2.4 `corpus/knowledge/storage-health-r26.md` — unaffected
- :139-144 references `probe_storage_arm` and the verdict-neutral line; the file makes no
  absent-root or BLOCKED-token claim (grep for `BLOCKED|unreadable|malformed|no-devinfo|bad-devid`
  in the file → no matches). SH1/SH2 counter semantics are untouched by the round-39 tokens.

### 2.5 `QUALITY.md` QUALITY 84 (echoed-token rule) — the new tokens comply
- QUALITY.md:165 requires a tool that prints a parsed `key=value` line to echo only tokens matched
  against a closed pattern, and a host/fixture name that fails the pattern to become "BLOCKED with
  a fixed reason token … never echoed". `mounts:btrfs-without-sysfs` / `mounts:unreadable` are
  fixed reason tokens (census :1909, :1912), not echoed host names — compliant.

## 3. Drafts (exact proposed text)

### 3.1 SKILL.md append-only rows — needed only if the L1's uncommitted append (§2.1) does not land;
it already carries equivalent text, which I verified against the implementation and run e1. Mine:

    ## Storage integrity arm — round 39 (absent or empty sysfs root)

    Appended 2026-10-26 (round-39 C1, commit `49cc53c7`). Supersedes the first row of the round-38
    table above (`state=HEALTHY filesystems=0 devices=0 nonzero=0`), which stays as written. When
    `/sys/fs/btrfs` is absent or holds no fsid entry, the arm now reads the mount table
    (`/proc/self/mounts`, override `TSUKUROI_PROC_MOUNTS`) before it calls the disk clean. A root
    with fsid entries never reads the table.

    | `STORAGE` line | Reading | Action (read-only) |
    |---|---|---|
    | `state=HEALTHY filesystems=0 devices=0 nonzero=0` (since round 39) | No fsid under the root **and** no btrfs mount in this process's mount table: no btrfs is mounted here | None |
    | `state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | btrfs is mounted but its sysfs view is hidden or absent (a namespace, container or a tmpfs over `/sys` or `/sys/fs`); the counters could not be read, so nothing is known about them | Re-run the census in the host's own namespace; there, `ls /sys/fs/btrfs` and `findmnt -t btrfs` must agree. Do not read this as disk corruption |
    | `state=BLOCKED … detail=mounts:unreadable` | No fsid under the root and the mount table could not be read: "no btrfs" cannot be told from "hidden" | Check that `/proc` is mounted in this namespace (`findmnt /proc`) |

    Counting: `python3 tools/score-storage-hidden-r39.py --revision <REV>`. Consumer note: the
    round-38 v1 counter `tools/score-storage-arm-r38.py` fixture F06 encoded the superseded rule;
    at revisions after `49cc53c7` it reads BLOCKED and that counter FAILs 9/10 by construction
    (wave-1 C1RevConsumers, run e1). It stays a round-38 instrument, valid at its round-38
    revisions (`b0005ae9`).

### 3.2 corpus/README.md append-only round-39 notice — not present anywhere yet; this draft is new:

    ### Frontier notice — round 39 (absent or empty sysfs root)

    Append-only; the round-38 known-limit sentence above is superseded here, not deleted. Since
    round-39 C1 (`../tools/tsukuroi-census.sh` `probe_storage_arm`, commit `49cc53c7`), an absent or
    fsid-less `/sys/fs/btrfs` reads `HEALTHY 0/0/0` only when the mount table (`/proc/self/mounts`,
    override `TSUKUROI_PROC_MOUNTS`) lists no btrfs mount; with a btrfs mount listed the STORAGE
    line is `BLOCKED … detail=mounts:btrfs-without-sysfs`, and an unreadable table is
    `BLOCKED … detail=mounts:unreadable` — a namespace that hides sysfs no longer gives a false
    all-clear. Measured with `../tools/score-storage-hidden-r39.py`; operator rows in `../SKILL.md`
    "Storage integrity arm — round 39".

## 4. What I did not do
- Did not run `score-census-handoff-r32.py` or `score-pacnew-arm-r35b.py`: their unchanged verdicts
  follow from their parse code (:504-512 and :407-408/:432-433), and r35b's failing state at
  post-r38 revisions is already recorded (SKILL.md:3147-3149).
- Did not run the C2 transaction-order counter (out of item scope).
- Did not edit any lane file. The SKILL.md/PROVINCE.md round-39 sections are the L1's uncommitted
  working-tree changes; I only read and verified them.
- Scratch `/fast/scratch/hyaku/tsukuroi-r39/C1RevConsumers/` removed after copying receipts
  (`e1.out`–`e5.out`) into this seat dir.
