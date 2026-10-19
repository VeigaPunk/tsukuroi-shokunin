# round-1 — non-author verification and spot-check (orchestrator, kaika)

Written by the integrator, not the lane (CORPUS.md: corrections and outside reviews are new
files; the lane owns `round-1.md`). Verifiers were fresh agents dispatched by the orchestrator
after the round landed at `daa918749`; full reports are committed in the fleet repo at
`.ufo/waves/kaika-w3/tsukuroi-review.md` and `tsukuroi-critic.md`.

## Spot-check (LEARNING.md — at least one admit and one reject)

| decision | sample | verifier | result |
|---|---|---|---|
| admit | four new entries (Arch news gate, `.pacnew` drift, initramfs v42 / boot recovery, snapper `errno:13`) — reviewer re-opened S010/S002/S020/S034; agree; `adjacency-recheck-2026-10-19.md` was admitted without its `## QUALITY check` — disagree at landing, fixed by appended check in `459e3ce` | W3ReviewTsukuroi | agree |
| reject | S029 rejected — re-opened; agree (6 of 7 sampled decisions agreed; the seventh became the appended QUALITY check) | W3ReviewTsukuroi | agree |

## Adjudication

ADMITTED after post-review fixes `459e3ce` + `daa9187`. Per-axis: freshness improved (errata 0→7 for the W1-flagged errors incl. bare `pacman -Sy` advice; notes missing `source:` 6→0; date-or-cadence rechecks 0→25/25; score 8→9), coverage improved (four read-only surfaces added to PROVINCE.md, coverage 0→4; capability `sources-registry`, 34 rows, census ok), adjacency improved (bounded: rebased on mori's committed receipt of packet TSUKUROI-F1-MEM-01 — `mori-shokunin` PROVINCE.md:58 at its round-12 head; sibling PROVINCE pins read 1/8 matching after this campaign's PROVINCE edits, 8/8 anchors in range — re-pin next round), depth/operability/calibration unchanged. Trends: expansion improved, quality improved (D1 count 9→14 explained), discernment improved (the outside disagreement became the appended QUALITY check). Host finding for the operator (not acted on): a second bare `pacman -Sy` on 2026-10-18 (`pacman.log:2287`) left the host in a partial-upgrade state — route a full upgrade through this lane's update-safety gate (mkinitcpio 42 `/sysroot` vs `btrfs-overlayfs`/`plymouth` hooks).
