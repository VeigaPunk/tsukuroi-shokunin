VERDICT: supports
Item R-4 — no-harm sweep, all six axes (seat RevNoHarmAxes, round 38 w1, 2026-10-26).
Base `8bd001f58bfda29c92d90d2a7a413825c0ca9fcb` → master `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf`
(5 commits: 7cbaeb6 freeze, 52ffd65 C1 arm, 1fe28e7 C2 entry, 9c9bb64 pre-seat amendment, 5edb6c2 registry).

## 1. The round's two named checks — both pass

- `git diff --numstat 8bd001f58.. master` → 94 files, 90 A + 4 M, 0 D, no renames
  (receipt `name-status.txt`; `cut -f1 name-status.txt | sort | uniq -c` → "90 A / 4 M").
- `git diff 8bd001f58.. master -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -c '^-[^-]'`
  → **0** (grep rc=1 = no matching lines). No removed line in any append-only path.

## 2. Every file the round changed, and whether the change is append-only

By directory (receipt `name-status.txt`; counts `cut -f2 | sed 's|/[^/]*$||' | sort | uniq -c`):

| Files | Location | Class | Append-only? |
|---|---|---|---|
| 67 | .ufo/waves/round-38/frozen/hooks-capture/usr-share-libalpm-hooks/*.hook | A (new) | n/a (creation) |
| 6  | .ufo/waves/round-38/controls/ (controls{,-q82}.{jsonl,err}, run-controls{,-q82}.sh) | A | n/a |
| 5  | .ufo/waves/round-38/sources/ (SHA256SUMS, alpm-hooks.5.asciidoc, alpm.c, hook.c, trans.c) | A | n/a |
| 4  | tools/ (census.sh **M**; check-hook-order-r38.py, score-storage-arm-r38{,-q82}.py A) | 3 A + 1 M | see census row |
| 3  | .ufo/waves/round-38/frozen/hooks-capture/etc-pacman.d-hooks/*.hook | A | n/a |
| 3  | .ufo/waves/round-38/before/ (c1-before.json, c2-before.json, c2-novelty-sweep.txt) | A | n/a |
| 2  | .ufo/waves/round-38/frozen/hooks-capture/ (MANIFEST.sha256, capture-meta.txt) | A | n/a |
| 1  | corpus/knowledge/pacman-hook-order-r38.md | A | n/a |
| 1  | corpus/SOURCES.md (M, +5/−0) | M | **insert-only, NOT append-only** — hunk `@@ -216,0 +217,5 @@` (old file 309 lines): 5 rows S208–S212 inserted mid-table, zero removals/modifications |
| 1  | SKILL.md (M, +3/−0) | M | append-only — hunk `@@ -3112,0 +3113,3 @@` at old EOF (old 3112 lines); 3 registry rows (storage-arm-r38, storage-arm-r38-q82, hook-order-r38) |
| 1  | SCORECARD.md (M, +57/−0) | M | append-only — hunk `@@ -2105,0 +2106,57 @@` at old EOF (old 2105 lines): round-38 declaration + pre-seat amendment |

- LOG.md, SHONEN.md, PROVINCE.md: absent from the diff entirely
  (`git diff --name-only 8bd001f.. master | grep -E '^(LOG|SHONEN|PROVINCE)\.md$'` → rc=1, no output).
- Working tree carries only untracked `.ufo/waves/round-38/{after,assimilation,l1,w1,...}` entries
  (`git status --porcelain=v1` → only `??` lines); the committed diff is the round's complete tracked change.

## 3. The only file with removed lines: tools/tsukuroi-census.sh (115+/4−)

All four removed lines (receipt `census-diff.txt`, grep `'^-'`):
1. header comment `# (selftest writes only under a mktemp dir named /tmp/tsukuroi-r3-2-selftest.XXXXXX).`
2. usage line `(incl. the memory-pressure arm) / journal-boot / update-safety / oom (kill-event watch)` — replaced by text naming the added DRIFT/STORAGE lines
3. usage line `/tmp/tsukuroi-r3-2-selftest.*); exit 0 pass, 1 fail` → `${TMPDIR:-/tmp}/...`
4. executable: `work=$(mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX)` → `work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")` (selftest scratch honours TMPDIR; default unchanged)

No probe, PLANE emitter, verdict, rollup or exit-map line was removed or modified — everything else is pure
addition: header contract comments, `probe_storage_arm()` (ends with unconditional `return 0`;
reads only `$BTRFS_SYSFS` via `-d`/`-r`/`read`), selftest env `TSUKUROI_BTRFS_SYSFS="$FX/btrfs"`,
6 new selftest cases, and in `main()` exactly 4 lines (`probe_storage_arm; printf '%s\n' "$STORAGE_LINE"`)
inserted **before** the rollup fold, which starts from the six plane verdicts and never reads the storage
state (`census-diff.txt` hunks `@@ -1822,10 +1844,52 @@` and `@@ -2896,6 +3003,10 @@ main()`).

## 4. Live census vs base census — same planes, same rollup, same rc

Commands (verbatim runs; full stdout kept as receipts):
- base: `git show 8bd001f58..:tools/tsukuroi-census.sh > /fast/scratch/hyaku/tsukuroi-r38/RevNoHarmAxes/base.sh; TMPDIR=$S bash $S/base.sh` → rc=**1**
- live: `TMPDIR=$S bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh; echo rc=$?` → rc=**1**
- `diff base-run.txt live-run.txt` (receipt `run-diff.txt`) — exactly two differences:
  1. `PLANE drivers`: only `C6_avail_kb=17372172` → `17368684` (live MemAvailable moved between the two
     runs, 3.4 s apart; every other field byte-identical). Host drift, not a code change.
  2. one **added** line after the HANDOFF lines: `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`.
- Identical in both runs: all six `PLANE` lines (packages/systemd/drivers/journal/update-safety/oom
  verdicts DEGRADED/HEALTHY/DEGRADED/DEGRADED/DEGRADED/DEGRADED), both `HANDOFF ADJ-04 mori` lines
  (value=138 / value=5), and the rollup `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY
  drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)` — no storage term.

## 5. Axis-by-axis harm assessment

- **Exit codes**: unchanged live (1=1). Structural: `probe_storage_arm` cannot alter the exit path
  (`return 0`, no `exit`); selftest cases pin `0 HEALTHY` rollups even when STORAGE reads
  DEGRADED/BLOCKED (`census-diff.txt` checks "healthy rollup: nonzero lifetime counters read DEGRADED
  on the STORAGE line only", "…a missing counter is BLOCKED…"). Usage errors still exit 2 (unchanged CLI).
- **Plane text**: the six PLANE lines are byte-identical base vs live; STORAGE is a new line without the
  `PLANE` prefix, so consumers pinning six PLANE lines read the same fields (contract documented in the
  header: "no PLANE text, rollup term or exit code changes"). HANDOFF lines unchanged.
- **Rollup / worst-plane rule**: rollup line identical; `main()` fold never sees the storage state.
- **Update-safety / package / systemd / journal / oom planes**: no code touched beyond the additions above;
  base-vs-live identity on this host is direct evidence.
- **New counter tools** (3 py files, SKILL registry rows): pure additions; nothing existing invokes them,
  so no existing behaviour can change. The q82 counter's `unshare -rm` + bind-mount-over-/sys/fs/btrfs is
  documented namespace-local in its SKILL.md row; **I did not run it** (outside this item) — claim carried,
  not verified by me.
- **corpus/SOURCES.md insert-only (mid-file)**: only observation worth flagging — any consumer pinning
  SOURCES by line number sees rows after old line 216 shift +5 (rows S001–S207). No row removed or
  altered; the named rows S208–S212 are the new ones. Informational, no axis harmed.

## Residual risk / what I did not run

- Two live runs are 3.4 s apart: identity of PLANE lines is empirical at those instants (drivers
  `C6_avail_kb` already drifted). Format invariance across host states rests on the selftest assertions,
  and **I did not run `tools/tsukuroi-census.sh --selftest`** — outside R-4's two named commands.
- Not run: `check-hook-order-r38.py`, `score-storage-arm-r38.py`, `score-storage-arm-r38-q82.py`, and the
  controls; their behaviour is cited from SKILL.md/SCORECARD.md rows, not exercised by me.
- No host mutation performed: no sudo, no pacman, no service/sysfs touch; the census itself is read-only
  (script header; verified no write redirection into /etc, /home, lane paths — grep rc=1) and selftest
  writes only under a mktemp dir honouring TMPDIR.

Receipts (this seat dir): `name-status.txt`, `census-diff.txt`, `base-run.txt`, `live-run.txt`, `run-diff.txt`.
Scratch `/fast/scratch/hyaku/tsukuroi-r38/RevNoHarmAxes/` removed after receipts were copied out.
