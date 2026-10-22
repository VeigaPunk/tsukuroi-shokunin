Verdict: the requested recapture reproduces all 22 nonvolatile blocks shared with the named L1 baseline; six additional blocks reflect script expansion, not observed host-state drift.

1. [obs] The exact assigned command completed with exit 0:
`bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/capture/capture.sh /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRecapture/cap`.
The capture timestamp is 2026-10-22T08:37:33Z. The baseline contains 198 lines and 24 blocks; the recapture contains 708 lines and 30 blocks. `diff -u` exited 1, as expected for differing files. Retained evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRecapture/cap/capture.txt:3 and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRecapture/cap/diff.txt:1. The baseline and recapture SHA-256 digests are respectively `63baf1c8522f2d597f4616c32caa77dfa1debae42a33a65a1e3b30db826601bb` and `b63e8060f93c2ae2cdfd230bce4bd03a196b809e6ff3a546f2be45bb0b51df8c`.

2. [obs] Every differing block in the requested comparison is classified below. All other 22 baseline blocks match byte-for-byte, including their recorded command and exit status.

- `time`: volatile. The timestamp changes from 08:19:59Z to 08:37:33Z.
- `boots`: volatile. Only the active boot's last journal timestamp changes, from 05:19:39 to 05:37:28 -03. Boot IDs, boot start times and the three previous boot rows remain identical. This is not a new boot or its completion time.
- `mirror-servers`: substantive capture-coverage difference; absent from the baseline.
- `repo-servers`: substantive capture-coverage difference; absent from the baseline.
- `pacman-commands-since-pause`: substantive capture-coverage difference; absent from the baseline.
- `cache-file-count`: substantive capture-coverage difference; absent from the baseline.
- `sudo-package-commands-since-pause`: substantive capture-coverage difference; absent from the baseline, not a comparable journal-tail change in this particular pair.
- `foreign-new`: substantive capture-coverage difference; absent from the baseline.

Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRecapture/cap/diff.txt:3-29. The capture script at declaration commit 674891d has 24 `run` commands and ends with `pacnew-count`; at commit 10b45f0 it has 30. Read-only `git show` of these revisions established that the six added blocks are script expansion. [inf] Their absence from the baseline is not evidence that host state changed.

3. [obs] These P1–P5 relevant blocks match exactly in the named baseline and the assigned recapture. Line numbers below apply to both files:

- P1: `pending`, `pending-count`, `pending-repos`, lines 38–56. Three pending packages remain: 1password-beta and claude-code from omarchy; chatgpt-bin from openai-chatgpt.
- P2: `local-newer-than-sync`, lines 57–60, has empty result output and exit 0. `boot-chain-installed` and `boot-chain-sync`, lines 61–90, match, including libinput 1.32.0-1 at lines 73 and 88.
- P3: `boot-chain-installed`, `boot-chain-sync`, `hooks-new-root`, `hooks-config`, `init-root`, and `buildroot-symlink`, lines 61–119, all match. These retain mkinitcpio 42.2-1, both `/new_root` hooks, `/sysroot` in init, and functions:1213 creating the relative symlink. Both `plymouth-boot0` and `plymouth-boot-1`, lines 136–176, also match in this pair. The `boots` block is NOT an exact match; only its active-boot last timestamp differs as classified above.
- P4: `sync-db-mtime`, lines 29–37, and `pacman-log-last-sync`, lines 129–135, match. Core/extra/multilib retain their 2026-10-17 mtimes and the latest logged sync remains 2026-10-21 20:32 -03. Mirror URL and exact pacman invocation blocks are absent from the named baseline; they cannot honestly be counted as matching it.
- P5: `pacman-log-since-pause`, lines 120–128, matches exactly and retains the five installations: zcode, tizen-sdb, tizen-sdb-debug, openssl-1.0, openssl-1.0-debug. Cache count, foreign-package query and cleanup-command blocks are absent from the named baseline; they cannot be counted as matching it.

Evidence pointers: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/capture/l1/capture.txt:29-176 and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRecapture/cap/capture.txt:29-176. An in-memory Python block comparison found 22 identical blocks, two differing blocks and six absent baseline blocks.

4. [obs] The same-generation comparison resolves the six coverage gaps. The tracked extended L1 capture `l1-2` and the assigned recapture have the same 30 blocks; 28 match exactly and only `time` and `boots` differ. This includes exact matches for all six added blocks: mirror URL at line 201; pacman sync and cache-clean invocations at lines 228–230; cache count 4 at line 235; cleanup journal entries at lines 694–697; foreign packages at lines 702–706. Both Plymouth journal blocks match in this comparison.
Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRecapture/cap/diff-l1-2.txt:1-19. `diff -u` exited 1 with only two hunks. `sha256sum -c` successfully verified the sidecars for `l1`, `l1-2`, the assigned capture and the second capture.

5. [obs] The script changed during the assignment. Supplemental runs were retained without overwriting the assigned capture:

- `cap2`, timestamp 08:42:35Z, exit 0: the 30-block script with narrowed Plymouth filtering and revised sudo filtering. Against `l1-3`, 27 blocks match exactly. The differing blocks are volatile `time`, volatile active-boot last timestamp, and volatile sudo-journal tail growth: one new entry at 05:41:45 -03 records user vgpnk running `paccache -d -k1` from inside the fleet repo. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRecapture/cap2/diff-vs-l1-3.txt:1-27. `paccache --help`, exit 0, identifies `-d` as a dry run; this entry is not evidence of a cache deletion.
- `cap3`, timestamp 08:44:22Z, exit 0: the subsequently expanded 35-block script. Its shared blocks reproduce `l1-3` except those same three volatile blocks. Five appended blocks are substantive coverage additions: `cache-package-files`, `cache-entries`, `paccache-runs-since-pause`, `snapper-list`, `snap-pac`. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRecapture/cap3/capture.txt:284-319.
- `cap-head`, timestamp 08:49:27Z, exit 0: a retained copy of the committed HEAD script was run to distinguish script drift from live-journal drift. Against `l1-2`, the differing blocks are `time`, `boots`, `plymouth-boot0` and `sudo-package-commands-since-pause`. The latter two are journal-tail growth. The old broad Plymouth grep additionally matches four later sudo inspection entries containing Plymouth-related command text. No additional package-query or pacman-log block changes were observed.

[unk] These are snapshots over an interval, not proof that no transient host operation occurred between them. No attribution to a particular peer seat was established.

6. [obs] Two integration risks follow directly from the retained evidence, without changing the gate entry:

- At observed HEAD 10b45f050c16f5f1d4f7e15a285d9f5294f7a486, `l1` and `l1-2` were tracked, `l1-3` was untracked, and `capture.sh` was modified. `git show HEAD:.ufo/waves/round-24/capture/l1-3/capture.txt` exited 128. The draft gate Markdown references `l1-3` and its numbering. The gate checker reads evidence using `git show <revision>:<path>`, so the L1 must land the cited capture at the eventual checked revision, or remap citations to a committed capture. This is an observed integration risk, not a final gate verdict. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-pause-gate.py:44-50 and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/pause-lift-gate-r24.md:1. For example, the mirror URL is line 194 in `l1-3`, line 201 in `l1-2`, and absent in `l1`. Plymouth start/finish milestones are lines 139/146/152/159 in `l1-3`, versus 139/150/156/167 in `l1` and `l1-2`.
- The cache count of 4 means four directory entries, not four package archives. `cap3` records zero `*.pkg.tar*` matches and lists four download directories. Its Snapper query reports `No permissions.` and its snap-pac query reports the package missing, although both blocks end with exit 0 because the script appends `true`. No usable snapshot rollback was established by this run. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRecapture/cap3/capture.txt:284-319.

[obs] No production files, configuration, package databases or services were intentionally changed by this seat. No tools were installed. No build, test, linter or gate-checker execution was performed. Retained artifacts comprise the report; `cap`, `cap2`, `cap3`, `cap-head` capture directories and their SHA-256 sidecars; `cap/diff.txt`, `cap/diff-l1-2.txt`, `cap2/diff-vs-l1-3.txt`; and the committed-script copy `capture-head.sh`. There is also an unused empty `tmp-head-script` directory.

Scope: read=lane capture scripts and captures, gate draft and checker source, SOURCES registry, read-only git objects and host queries; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRecapture.md and artifacts under /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRecapture/; executed=bash capture runs (four, exit 0), diff, SHA-256 checks, in-memory Python block comparisons, read-only git queries, paccache --help and the read-only host commands recorded inside the captures
Installs: none
