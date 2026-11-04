# ExecHost — round 78 read-only journald accounting

Axes: depth and operability. Read SCORECARD Round 78 and before/expected.json.
No C1/C2 verdict, uplift, or outside closure claimed. No production files changed.

## Observed results

- `pacman -Q systemd`: `systemd 262.1-1`.
- `stat -f /var/log/journal`: btrfs; block size 4096; total 243661568,
  free 187226886, available 186252614 blocks.
- User and sudo `journalctl --disk-usage`: both report
  `Archived and active journals take up 193.4M in the file system.`
- Metadata-only Python scan: 2 immediate directories traversed, 16 regular
  `.journal` files; 0 `.journal~`; 202866688 allocated bytes (`st_blocks * 512`),
  268435456 apparent bytes (`st_size`). Nonregular ignored 0, stat errors 0,
  directory-list errors 0, regular nonmatching suffix 0.
- Filtered configuration: active `SystemMaxUse=256M`, `RuntimeMaxUse=64M`;
  commented `#Storage=persistent`, `#SystemMaxUse=`, `#SystemKeepFree=`,
  `#RuntimeMaxUse=`, `#RuntimeKeepFree=`. Commented lines are not active settings.
  Configuration on disk does not establish the running daemon's loaded settings.

The allocated total is approximately 193.47 MiB; the apparent total is 256 MiB.
The rounded journalctl display is broadly consistent with allocated accounting,
not apparent size. This is corroboration, not an exact equality assertion:
journalctl's search scope and scan time differ from this metadata traversal.
Neither identical populations nor per-file uniform sizes were established.
The apparent aggregate numerically matches 256M, but this does not establish cap
compliance, daemon health, or any need for cleanup. No compression/sparsity cause
or keep-free threshold was determined.

The scan mirrors the frozen examples' suffix, no-follow, regular-file and
allocated-block decisions. It found no exceptional examples on this host;
it does not replace the six-case fixture review or prove installed source identity.

## Exact probes and receipts

All executed commands returned rc 0. Receipts carry UTC `2026-11-04T18:26:34Z`,
recorded after each operation (not distinct start/end timestamps).

1. `pacman -Q systemd` — P1-pacman-Q-systemd.txt
2. `stat -f /var/log/journal` — P2-stat-f-var-log-journal.txt
3. `journalctl --disk-usage` — P3-journalctl-disk-usage-user.txt
4. `sudo -n journalctl --disk-usage` — P4-journalctl-disk-usage-sudo.txt
5. `systemd-analyze cat-config systemd/journald.conf` — P5-journald-conf-directives.txt.
   Exact Python filter: `^\s*#?\s*(Storage|SystemMaxUse|RuntimeMaxUse|SystemKeepFree|RuntimeKeepFree)\s*=`.
6. Invocation: `TMPDIR=/fast/scratch/hyaku/tsukuroi-r78/ExecHost python3 /fast/scratch/hyaku/tsukuroi-r78/ExecHost/probe_driver.py`.
   P6-scandir-lstat-aggregation-user.txt and summary.json retain the aggregation;
   receipts/probe_driver.py preserves exact executed methodology.
   `os.scandir` and `DirEntry.stat(follow_symlinks=False)` do not read file contents.
7. Additional read-only lane bookkeeping:
   `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD`;
   `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -t 07a607df1a5157daafc91bb5c26858af14415f43`;
   `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -t b9019a1d0558241bf67cf31ff90256284d8657af`.
   P8a/P8b/P8c receipts: HEAD equals the frozen claim; both objects are commits.

## Limitations and execution deviations

The scanner treats immediate real directories as machine-id journal directories;
it did not validate their names. Names and file basenames were never emitted or
retained in receipts. The conditional sudo ls/stat fallback was not executed.
Python rc 0 denotes completed aggregation; separate error counters govern coverage.

The configuration command's complete output was captured transiently in Python
memory before exact-directive filtering; only safe matching lines were retained
or displayed. Thus this was output-filtered, not a field-restricted read.
This implementation limitation is disclosed rather than claiming no raw read.
The driver also performed the additional read-only git bookkeeping above, beyond
the requested host probe list. Bash unexpectedly supervised the finite commands
because a name was supplied; the driver exited rc 0 and left no running work.

No journal contents, environment, or credentials read; no package installation,
transaction, vacuum, rotate, flush, restart, clone, git mutation, or tests run.
Scratch was removed after preserving the driver and receipts. No external state
remediation attempted. See handoff.md for operator disposition.
