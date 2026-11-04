# N1Sentinel — round-71 w1 — boundary audit

Read-only audit of `.ufo/waves/round-71/{w1,probes}` (73 files at snapshot 2026-11-04T01:08Z),
both repositories' working trees, `/tmp`, and every scratch tree. Full method, evidence and
severity reasoning: `probes/N1Sentinel/audit.md`.

## Verdict

WRITES=73 SECRETS=0 SUDO_NONREADONLY=0 TMP_EVIDENCE=0 LANE_DIRTY=2 MISROOT=0

## Findings

- **No host write, no package/service state command, no interactive sudo.** 46 `/sys` mentions
  are descriptive; four pattern hits (a `> /sys/` prose fragment, the S300 upstream `modprobe`
  example, two census fixture heredocs) were inspected and cleared.
- **No secret shape** (no key/token/JWT/`op://`/bearer/password assignment). F1 LOW: the raw
  capture `probes/S1Scout/host-enum.txt` publishes the btrfs filesystem UUID and the
  `PARTUUID`; the seat's own reports redact to `<uuid>`. `plazir27` is census-tool output and
  pre-existing in the committed `before/`/`after/` receipts.
- **No `/tmp` evidence.** Runtime leftovers are 700 B gate files and one pre-wave empty dir;
  the only `/tmp` mention describes a mutant's deliberate hermeticity break.
- **F2 MEDIUM, reporting:** `probes/SC3Lesson/sweep-receipt.txt` records six invocations with
  lane-relative paths and no `cd`; from the fleet root, `.ufo/waves/round-71` does not exist and
  `SCORECARD.md` is a *different* 531-line file (lane: 5504 lines). Observed line 5467 proves
  lane cwd, so nothing was misrooted — the receipt is simply not reproducible as written.
- **No seat wrote outside the wave dirs.** Both lane dirty files are L1-authored; the committed
  census bytes are byte-identical to `L1/proto/census.sh`.
- **F3 HIGH, provenance:** the committed C2 block (`db58e7c9`, `487feeb6…`) is not reproducible
  from E1Harness's artifact. Its first `harness.patch` is a reverse diff that fails 4/5 hunks
  on the HEAD base; the seat later published byte-different patched copies (`ebe3ab2d…`,
  `81628076…`), and the lane working tree is a third version (`598ae252…`). E1Harness's own
  report agrees: "Independent alternative to the harness the L1 landed at `db58e7c9` … Nothing
  here was applied to the lane tree." The round must not claim the seat's patch produced the
  commit.

## Scratch

Gone: C1Connector, E2CounterAttack, E3Repairs, E1Harness, K1Critic, M1Mutation, R1Reviewer,
S1Scout, SC1Entry, SC2Sources, SC3Lesson, SC4Index. Remaining at snapshot: L1 (orchestrator),
R2Reviewer (published, tree not removed), N1Sentinel (this seat, removed at yield).
