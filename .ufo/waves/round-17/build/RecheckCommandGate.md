# RecheckCommandGate — tools/check-recheck-commands.py

[obs] Gate audits the LAST `recheck:` line per file (later supersedes, journal-boot-plane.md:442) of each `--paths` target — blobs or dirs expanding to `*.md`, default `corpus/knowledge` — at `--revision`, flagging a `--forbid` binary (default pacman,checkupdates,yay,paru,mkinitcpio,limine-update) only as argv0 of a backticked command; `sudo`/env/`timeout`/`xargs`/`sh -c`/`eval` recurse. `## R17-RECHECK — steer-safe procedure` (exactly once, ≥1 command, zero forbidden invocations) resolves; else RECHECK-FORBIDDEN-INVOCATION / RECHECK-STEER-SAFE-INVALID. Binding contract: hex-only, E-REVISION-INVALID/NOT-LANDED/NOT-PUSHED; JSON carries revision/branch/branch_tip/origin_tip and counts; exit 0/1/2.

[obs] `python3 tools/check-recheck-commands.py --selftest` → `{"cases": 40, "passed": 40}` exit 0; all fixtures in mktemp repos.

[obs] Expected red: case `baseline-mined-line` embeds initramfs-v42-sysroot-recovery.md:3 verbatim → exit 1, flagged_count 1, invocation_count 1, site `fixture.md:3`.

[obs] Read-only baseline audit (git ls-tree/show): all 36 corpus `.md` carry recheck; last-line flags 5 files — initramfs:3, driver-firmware-plane:268, foreign-provenance-r6:313, package-state-plane:328, snapper-eacces-mechanism:3 (`pacman -Qo`). aur-risk-plane.md:15 is superseded by safe :347; boot-chain-r17.md:3 clean (pacman only in prose; `sudo -n cat` allowed).

[obs] Worktree initramfs file carries the steer-safe heading at :74 (commands `ls -d /var/lib/pacman/local/…` only) — case `landed-r17-section` pins it, resolved_count 1. [unk] Non-backticked commands are out of scope per CritMinedMistake.md:17. [obs] No installs, no host probes, no lane git writes.

Scope: executed=python3 tools/check-recheck-commands.py --selftest (7 runs; final exit 0), python3 - <<EOF (two read-only baseline audits), git log/status/show/ls-tree/merge-base (read-only), ls/find/sed/grep (lane reads), git init+commit in /tmp (one throwaway probe; selftest sandboxes are mktemp)
