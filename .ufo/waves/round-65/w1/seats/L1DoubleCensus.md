# L1DoubleCensus — double-entry census of the INITRAMFS arm (round 65, wave w1)

Seat: L1DoubleCensus (labrat, EXEC-AUTHORIZED bounded probe). Claim served: **C2
coverage+operability** — specifically whether the newly wired `INITRAMFS` arm's live counts
survive an independent second census of the same directories.

**H:** the INITRAMFS arm's live line counts equal an independent census of the same directories
computed with find/awk (double-entry). Disprovable by any count mismatch.

**VERDICT: H HELD** on all seven fields. No mismatch. Zero-byte stderr.

## Method (ground first, live second)

The independent ground census was computed from `stat`/`find`/`grep`/`command -v` against the
host and written to disk *before* the census output was read, so the comparison is genuine
double-entry, not a re-run of the arm's own arithmetic.

Ground receipt: `.ufo/waves/round-65/probes/r65-double-census-ground.txt` (exact commands +
raw outputs + rc).
Verdict receipt: `.ufo/waves/round-65/probes/r65-double-census-verdict.txt`.

Host: plazir27, kernel 7.2.11-arch1-1, UTC 2026-11-03T19:49:32Z. Lane HEAD `37c74e27`;
working-tree `tools/tsukuroi-census.sh` sha256 `fe15cc5d…a39f3f` (git shows it modified vs
HEAD blob `8c2e4888` — E2's in-flight edit; I never touched it).

## Field-by-field double entry

| field | independent ground | live line | verdict |
|---|---|---|---|
| mkinitcpio-conf | PRESENT (regular, readable, 3357 B, 644 root:root) | PRESENT | held |
| conf_d | 4 (`find -mindepth 1 -maxdepth 1` = 4 regular files, 0 hidden) | 4 | held |
| hooks | 12 (`find -maxdepth 1 -type f` = 12, all readable) | 12 | held |
| newroot_latehooks | 2 (`grep -ls '/new_root'` = btrfs-overlayfs, plymouth) | 2 | held |
| presets | 0 (`/etc/mkinitcpio.d` exists, empty) | 0 | held |
| ukify | ABSENT (`command -v ukify` rc=1, no output) | ABSENT | held |
| unreadable | 0 (0 unreadable conf/drop-ins/hooks; dirs r+x) | 0 | held |

Live line (identical in two runs):

```
INITRAMFS initramfs-plane mkinitcpio-conf=PRESENT conf_d=4 hooks=12 newroot_latehooks=2 presets=0 ukify=ABSENT unreadable=0
```

## Wiring and neutrality evidence

- Wiring: `grep -c INITRAMFS tools/tsukuroi-census.sh` = **22**, rc 0. Before control
  (`before/absence-controls-receipt.txt`, base HEAD `1bd8e196`): count **0**. The label went
  0 → 22 this round.
- Arm is at `probe_initramfs_arm()` lines 2101-2178; printed after `SCRUB`, before the rollup
  (`printf` at 4049, rollup term starts 4053). `INITRAMFS_LINE` is read only at 2175
  (assignment), 2176 (detail append), 4049 (print) — never by `worse`, the rollup printf or
  the exit map.
- Observed before/after: pre-arm baseline receipt has 13 stdout lines, 0 INITRAMFS lines,
  `census-rc=1`; post-arm is 14 stdout lines with exactly one INITRAMFS line and `census-rc=1`.
  Delta = exactly +1 line; exit code and rollup text unchanged.
- Two live runs ~4.1 s each (4.13 s, 4.05 s), stderr 0 bytes, stdout 14 lines. Run 2 rc=1
  (DEGRADED rollup, six planes DEGRADED — pre-existing, same as the pre-arm baseline).

## Commands run (all read-only; rc shown)

| # | command (abridged) | rc | result |
|---|---|---|---|
| 1 | `mkdir -p /fast/scratch/hyaku/tsukuroi-r65/L1DoubleCensus .ufo/.../probes` | 0 | dirs |
| 2 | `grep -c INITRAMFS tools/tsukuroi-census.sh` | 0 | 22 |
| 3 | `stat -c '%n %s %a %U:%G' /etc/mkinitcpio.conf` | 0 | 3357 644 root:root |
| 4 | `find /etc/mkinitcpio.conf.d -maxdepth 1 \| sort` | 0 | dir + 4 drop-ins |
| 5 | `find /usr/lib/initcpio/hooks -maxdepth 1 -type f \| sort` | 0 | 12 hook files |
| 6 | `grep -ls '/new_root' /usr/lib/initcpio/hooks/*` | 0 | 2 files |
| 7 | `find /etc/mkinitcpio.d -maxdepth 1 \| sort` | 0 | dir only |
| 8 | `command -v ukify` | 1 | absent |
| 9 | `bash tools/tsukuroi-census.sh 2>/dev/null \| grep '^INITRAMFS '` | 0 (grep) | one line |
| 10 | `bash tools/tsukuroi-census.sh >run2 2>run2.err` | 1 | 14 lines, stderr 0 B |
| 11 | hidden/unreadable `find` checks (conf.d, presets, hooks) | 0 | 0/0/0, 0 unreadable |
| 12 | `grep -n 'INITRAMFS_LINE' tools/tsukuroi-census.sh` | 0 | 2175, 2176, 4049 |
| 13 | `sed -n '4042,4062p' tools/tsukuroi-census.sh` | 0 | print before rollup |
| 14 | `wc -l`/`grep -c '^INITRAMFS '` on `before/live-census-baseline-prearm.txt` | 0 | 13 stdout lines, 0 INITRAMFS, rc1 |
| 15 | `git rev-parse --short HEAD`, `sha256sum tools/tsukuroi-census.sh` | 0 | 37c74e27, fe15cc5d… |

## Files written

- `.ufo/waves/round-65/probes/r65-double-census-ground.txt` — ground census, exact commands,
  raw outputs.
- `.ufo/waves/round-65/probes/r65-double-census-verdict.txt` — field-by-field comparison and
  verdict.
- `.ufo/waves/round-65/w1/seats/L1DoubleCensus.md` — this report (copy at
  `.ufo/waves/round-65/w1/L1DoubleCensus.md`).

No edits to `tools/tsukuroi-census.sh` (E2 owns it) or to any L1-landed file (LOG, SCORECARD,
SKILL, SOURCES, knowledge, PROVINCE, SHONEN, AGENTS).

## Defects / risks

- **No defect found.** All seven fields matched; stderr empty; exit code and non-INITRAMFS lines
  unchanged.
- **Boundary risk (not a defect):** the arm counts drop-ins via the shell glob `"$dir"/*`,
  which skips dotfiles, while the ground used `find` (includes them). Measured hidden entries
  are 0/0/0 on this host, so no divergence today; a future dotfile drop-in (e.g.
  `.nvidia.conf`) would be invisible to the arm.
- **Context, not drift:** census rc=1 is the pre-existing DEGRADED rollup (same rc in the
  pre-arm baseline). The INITRAMFS line is outside the rollup and the exit map.
- E2's `tools/tsukuroi-census.sh` remains uncommitted in the working tree (expected; L1 lands).

## Scratch

All temp files lived under `/fast/scratch/hyaku/tsukuroi-r65/L1DoubleCensus/` and were removed
after the receipts above were copied into the wave dir. No files under `/tmp` were citable
evidence and none remain.
