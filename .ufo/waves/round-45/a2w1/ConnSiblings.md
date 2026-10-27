VERDICT: no-finding

Seat ConnSiblings-2 — round 45 wave a2w1, item X-2: sibling-overlap scan for the round's
surfaces (godspeed). Scan over sibling lanes only; tsukuroi-shokunin itself was skipped
entirely. Read-only; written nothing except this report and associated receipts.

## Scope (files scanned)

Fleet root: `/home/vgpnk/Projects/shokunin`. 20 sibling lanes, all `*-shokunin` except
`tsukuroi-shokunin`: audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama,
kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi,
tameshi. Per lane, exactly the three surfaces named by the seat: `PROVINCE.md` (20/20 exist),
`SKILL.md` (18/20 exist — audio and game-dev-2d have none), and `corpus/knowledge/` (20/20
exist, 1,132 total files, recursion including nested subdirectories). Total target surface
files: 1,170 files.

Inventory command (bash, existence & file counts):

```bash
for l in /home/vgpnk/Projects/shokunin/*-shokunin; do
  n=$(basename "$l")
  [ "$n" = "tsukuroi-shokunin" ] && continue
  p=no; s=no; k=no; kc=0
  [ -f "$l/PROVINCE.md" ] && p=yes
  [ -f "$l/SKILL.md" ] && s=yes
  if [ -d "$l/corpus/knowledge" ]; then
    k=yes
    kc=$(find "$l/corpus/knowledge" -type f | wc -l)
  fi
  printf '%-20s PROVINCE=%-3s SKILL=%-3s knowledge=%-3s (%d files)\n' "$n" "$p" "$s" "$k" "$kc"
done
```

Inventory output: all 20 lanes `PROVINCE=yes knowledge=yes`; 18 `SKILL=yes`; audio and
game-dev-2d `SKILL=no`. Receipt: `.ufo/waves/round-45/a2w1/ConnSiblings/inventory.txt`.

## Commands (grep and search runs)

Let P be the union (1,170 files) of the 20 `PROVINCE.md` files, 18 `SKILL.md` files, and
1,132 `corpus/knowledge/` files across the 20 sibling lanes. Each term below was searched
over P (receipts in `.ufo/waves/round-45/a2w1/ConnSiblings/commands.sh` and `scan-summary.txt`):

```bash
# 1. memparse
grep -rni 'memparse' P                                      # 0 matches

# 2. scrub_speed_max
grep -rni 'scrub_speed_max' P                              # 0 matches
grep -rni 'scrub_speed' P                                  # 0 matches

# 3. dev-replace / device replace
grep -rniE 'dev[-_]replace|device[[:space:]]+replace|btrfs[[:space:]]+replace' P # 0 matches

# 4. KillSignal
grep -rni 'KillSignal' P                                    # 0 matches

# 5. DefaultTimeoutStopSec
grep -rni 'DefaultTimeoutStopSec' P                         # 0 matches

# 6. faster-shutdown
grep -rni 'faster-shutdown' P                              # 0 matches

# 7. TimeoutStopSec
grep -rni 'TimeoutStopSec' P                               # 0 matches

# 8. SIGPIPE / exit 141 / pipefail early readers
grep -rni 'SIGPIPE' P                                      # 22 matches (mado: 1, mori: 21)
grep -rnE 'exit[[:space:]]*141\b|141\b' P                  # 161 matches (mori has 11 genuine SIGPIPE 141 hits)
grep -rni 'pipefail' P                                     # 24 matches (kagi, kengaku, kumitate, mori)
grep -rnE '\|\s*head\s+-[n]?[0-9]+' P                      # 30 matches (gated scripts, docs, verification recipes)

# 9. tsukuroi census line consumers
grep -rnE 'TSUKUROI_CENSUS|tsukuroi-census' P              # 87 matches (tameshi: 86, mori: 1)
```

## Results

### 1. Contested scope on Round 45 surfaces: NONE

Zero occurrences of every round-45 C2 surface token across all 20 sibling lanes in
`PROVINCE.md`, `SKILL.md`, and `corpus/knowledge/`:
- `memparse`: 0 matches
- `scrub_speed_max` / `scrub_speed`: 0 matches
- `dev-replace` / `dev_replace` / `device replace` / `btrfs replace`: 0 matches
- `KillSignal`: 0 matches
- `DefaultTimeoutStopSec`: 0 matches
- `faster-shutdown`: 0 matches
- `TimeoutStopSec`: 0 matches

No sibling lane claims, implements, or grounds any of these kernel or systemd mechanisms.
There is zero boundary contention on the round's C2 surface (`btrfs-scrub-grounding-r45.md`
rows GR1, GR2, GR3). No sibling PROVINCE.md boundary sentence requires adjustment.

### 2. Broad `btrfs` and `scrub` nets

- **`btrfs` (18 matches across 6 lanes):**
  - `chousa-shokunin/corpus/knowledge/mount-alias-r14.md:31`: repo on btrfs dev 30.
  - `kama-shokunin/SKILL.md:1515`: llama.cpp lifecycle receipt on host.
  - `kasegi-shokunin/corpus/knowledge/source-tree-loss-2026-09-28.md:37,55,270`: `/home` btrfs mount options; btrfs subvolume enumeration not permitted.
  - `kumitate-shokunin/corpus/knowledge/agent-isolation-substrates.md:47,167` & `omp-task-contract.md:94,96`: lane repo jj-colocated on btrfs; OMP PAL isolation backends (`btrfs`, `zfs`, etc.).
  - `mori-shokunin/SKILL.md:438` ("Never threshold the btrfs chunk percent. Data-chunk fill reads 94.25%") & `corpus/knowledge/surfaces-r7.md:154` (`dm-0` is the btrfs device).
  - `souji-shokunin/corpus/knowledge/count-objects-linked-worktree-garbage.md:90,129`, `quarantine-same-filesystem-rename.md:44,49`, `quarantine-staging-no-copy-r23.md:30,40,41`: btrfs directory sizing, tmpfs vs btrfs rename benchmarks, `mv --no-copy` support.
  *Assessment:* All 18 matches are host filesystem substrate observations. None touches `btrfs scrub`, scrub sysfs limits, or device replace.

- **`scrub` (76 matches across 9 lanes):**
  - All hits in `audio`, `chousa`, `kaidoku`, `kama`, `kotoba`, `kumitate`, `mori`, and `tameshi` are the environment-scrubbing homonym (`env -u`, `BASH_ENV`, `LD_PRELOAD`, `CHOUSA_*`, loader scrubs).
  - `kotodama-shokunin/corpus/knowledge/culture-material/bathing-and-body-hygiene.md:7,81`: physical body scrubbing.
  *Assessment:* Zero matches for filesystem scrubbing.

### 3. `SIGPIPE` / `exit 141` / `pipefail` early readers

A primary finding of this scan is that **`mori-shokunin` holds deep, measured grounding on the exact same class of pipefail/SIGPIPE/141 failures that Claim C1 addresses**:

- **`mori-shokunin/corpus/knowledge/selftest-flake-r9.md:1-60`:**
  - Documents the race in pipeline `printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss |$re|"` under `set -euo pipefail`.
  - Explains the mechanism: `grep -q` exits 0 on the first match and closes its read end; bash's `printf` emits line-by-line (one `write(1)` per line); the writer's next write receives `EPIPE` and dies of `SIGPIPE` (exit 141); `pipefail` sets the pipeline return code to the rightmost non-zero element (141) despite the consumer exiting 0.
  - Corroborated with PIPESTATUS (`ps0=141 ps1=0`) and strace traces.
- **`mori-shokunin/corpus/knowledge/verdict-contract-r13.md:1-68`:**
  - Sourced from S031 (`man7.org/linux/man-pages/man7/pipe.7.html`, man-pages 6.19) and `tools/mori-census.sh:1494`.
  - Details kernel `pipe(7)` capacity: default 16 pages = 65,536 bytes (64 KiB).
  - Identifies defect F01: `printf '%s\n' "$inwin" | sed -E 's/^[0-9]+ //' | grep -Fxq ...` under `set -euo pipefail`. When `grep` matches and exits early, `sed` continues writing; if the payload exceeds 64 KiB, `sed`'s next `write(2)` encounters a closed read end, receiving `SIGPIPE` (exit 141).
  - Explains why ordinary short payloads pass while payloads exceeding 64 KiB reliably fail with exit 141.
- **`mori-shokunin/corpus/knowledge/audit-r11.md:99,156,168,216,372` & `surfaces-r8.md:247-256`:**
  - Additional audit records and archaeological context for defect F01 and the r9 selftest flake.

Other sibling references to `SIGPIPE` or early readers:
- `mado-shokunin/corpus/knowledge/event-delivery-limits-r26.md:67`: note that hyprutils ignores `SIGPIPE` when closing descriptor in `removeClientByFD`.
- `game-dev-3d-shokunin/corpus/knowledge/unreal-mcp/gate/run_gate.sh:323,327`: uses `rec=$(grep -nE "$LABEL_RE" "$f" | head -1)` and `lab=$(printf '%s' "$text" | grep -oE "$TOKENS" | head -1)`. However, `run_gate.sh` runs with `set -u` only (not `-e`, not `-o pipefail`), so early exit from `head -1` does not cause failure.
- `kengaku-shokunin/corpus/knowledge/tb2-password-recovery-grader.md:46`: quotes benchmark solve script `OFFSET=$(grep -aob "$FIRST_PARTIAL_PART" "$IMG_PATH" | head -n1 | cut -d: -f1)`. Benchmark task code; not fleet code.

### 4. Dependencies on tsukuroi's census (consumers that may break)

- **`tameshi-shokunin` — registered consumer/mutator of `tools/tsukuroi-census.sh`:**
  - Mentions across PROVINCE.md:32, SKILL.md:675,681,1101,1175,1314,1406, and corpus/knowledge/fleet-kill-rate-ledger.md:47,71,183,260,337,358.
  - Analyzed impact of Round 45 C1:
    1. C1 changes the five production first-line readers from `printf '%s\n' "$CAP_OUT" | head -n1` to parameter expansion (`${var%%$'\n'*}`). The emitted line grammar (`TSUKUROI_CENSUS: ...` and `PLANE ...`) is byte-preserved; no prefix, field, or line order moves.
    2. C1 adds 6 selftest cases labelled `(R45-C1)` (148 -> 154), changing `TSUKUROI_CENSUS_SELFTEST: PASS (148 cases...)` to `(154 cases...)`.
    3. Tameshi's mutation testing harness (`tools/mutate-and-run.sh:90,755-796,1470`) runs against an isolated historical git checkout at commit `165307fe` (blob `084951be…`), not the live worktree.
    4. Tameshi's posture ("re-read, never carry") treats worktree edits as `stale` ledger status (`pin-disposition.py:141,805,858`), not test failure.
    *Conclusion:* No consumer break in tameshi.

- **`mori-shokunin` — line-anchor citation in `PROVINCE.md:287`:**
  - `mori-shokunin/PROVINCE.md:287` cites `../tsukuroi-shokunin/tools/tsukuroi-census.sh:376,1100-1115` as line anchors for reading `/proc/pressure/memory`.
  - Drift verification: in tsukuroi-shokunin commit `18389f44` (C1 implementation) vs `5bbd5ff5` (round base), all five reader edits (lines 962, 1000, 1082, 1457, 1532) are exact 1-line-for-1-line replacements, and the 44 new lines (six selftest cases) are appended at line 3330+.
  - Line 376 and lines 1100-1115 in `tools/tsukuroi-census.sh` are identical in position and content between base and implementation.
  *Conclusion:* Zero citation drift on mori's inbound line anchors.

### 5. Knowledge another lane holds that this round should cite (report, do not absorb)

1. **`mori-shokunin` — POSIX pipe buffer capacity & `SIGPIPE` / exit 141 under `pipefail`:**
   - Cites S031 (`pipe(7)`) in `corpus/knowledge/verdict-contract-r13.md:1-68` and `corpus/knowledge/selftest-flake-r9.md:1-60`.
   - Explains the exact kernel limit: default Linux pipe buffer is 16 pages (65,536 bytes). A producer writing past 64 KiB to a pipe whose reader closed receives `EPIPE` / `SIGPIPE` (exit 141), which `set -o pipefail` promotes to pipeline exit status.
   - Grounding for C1: This explains why tsukuroi's C1 selftest cases require ~150 KB of padding (substantially exceeding the 64 KiB buffer) to reliably trigger the exit 141 fault. Tsukuroi should cite mori's grounding in its closeout lesson or documentation for C1.

2. **`kotoba-shokunin` — standing sibling-overlap census method:**
   - Precedent in `PROVINCE.md:33` and `corpus/knowledge/sibling-overlap-census-round74.md:29-45,66-103`.
   - Standing verification tooling: `verifiers/check_sibling_census.py` and `verifiers/check_sibling_reread.py`. Cite if tsukuroi formalizes a standing overlap verifier.

## UFO-FSD Connector Proposal

- **Evidence:** `mori-shokunin/corpus/knowledge/verdict-contract-r13.md:1-68` (citing S031 `pipe(7)` and measuring the Linux 16-page / 64 KiB pipe buffer capacity) and `mori-shokunin/corpus/knowledge/selftest-flake-r9.md:1-60` (documenting the `printf | grep -q` SIGPIPE exit 141 race under `set -euo pipefail`).
- **Affected Axes:** Operability (C1) and Depth / Adjacency.
- **Proposed Move:** In tsukuroi's closeout lesson or knowledge record for Claim C1 (e.g. `corpus/lessons/round-45-*.md`), explicitly cross-cite mori's `verdict-contract-r13.md` and S031 (`pipe(7)`) as the theoretical foundation for the ~150 KB padding threshold in the `(R45-C1)` selftests. Rather than leaving the ~150 KB size as an unexplained arbitrary choice, ground it in the 64 KiB (16-page) Linux kernel pipe capacity where `write(2)` triggers `EPIPE`/`SIGPIPE` once the reader closes.
- **Risks:** Zero. This is read-only cross-lane citation; no code, script, or contract changes.
- **Verification:** Run `python3 tools/check-adjacency-anchors.py --revision <REV>` to confirm all inbound and outbound anchors remain valid and non-mutated.

## What I did not do

- Ran no C1 or C2 scoring counters; no selftests; no git/jj mutations in any repo; no host queries or service manipulation.
- Wrote nothing in any sibling lane; wrote nothing at the fleet root; wrote nothing in tsukuroi-shokunin except this report (`.ufo/waves/round-45/a2w1/ConnSiblings.md`) and receipts under `.ufo/waves/round-45/a2w1/ConnSiblings/`.
- Cleaned up private scratch directory `/fast/scratch/hyaku/tsukuroi-r45/ConnSiblings/`.

## Bottom line

Zero contested scope on the round's C2 surfaces (`memparse`, `scrub_speed_max`, `dev-replace` / `device replace`, `KillSignal`, `DefaultTimeoutStopSec`, `faster-shutdown`, `TimeoutStopSec`) across all 20 sibling lanes. Zero breaking consumers on tsukuroi's census line format (tameshi's mutation testing is revision-pinned to `165307fe` and handles live drift as `stale`; mori's line anchors at `376,1100-1115` did not move between base `5bbd5ff5` and impl `18389f44`). One rich cross-lane knowledge ground identified: `mori-shokunin`'s `verdict-contract-r13.md` and `selftest-flake-r9.md` provide established grounding on the Linux 64 KiB pipe buffer and `SIGPIPE` 141 under `pipefail`, directly explaining the ~150 KB padding in tsukuroi's C1 selftests.
