# R2Reviewer — C2 arm attack review

## Findings, by severity

### F1 — High: delivered selftest violates the assignment's explicit no-control-file-writes rule even for fixtures

In the applied `tools/tsukuroi-census.sh`, lines 4359–4361 write `stats_clear`, `error/fail_at_unmount`, and `error/metadata/EIO/max_retries`; line 4408 creates another `stats_clear`. The immutable patch has these at lines 170–172 and 219. All are inside `run_selftest`, not the live arm. The assignment expressly prohibits these writes even on fixtures. The requested selftest executed these fixture writes; additionally my own scratch driver created a regular file named `error/metadata/max_retries` before attack runs. These are disclosed execution-policy deviations, not evidence of mutation of host XFS controls. No actual `/sys`, `/proc`, `/etc`, `/boot`, package, or service state was written. Recommendation: remove forbidden-name fixture writes before any further execution under this assignment; arbitrary ordinary error/log fixture names suffice. No reviewer fix applied.

### F2 — Medium: recursive counting follows file symlinks, overstating regular-file counts

Applied `tools/tsukuroi-census.sh:2454–2461` uses `[ -f "$e" ] && [ -r "$e" ]`, which follows a symlink to a regular file. In receipt j, each error/log directory contains one ordinary regular file and one symlink to the fixture stats file. Independent `find ... -type f -readable` enumerates one regular file per directory; arm emits `error=2 log=2`. This differs from the frozen regular-file-count predicate, despite no rollup or exit change. Exclude symlink entries when counting regular files; retain a regression case. No production-host mismatch observed.

### F3 — Medium: recursive glob silently omits hidden regular files

Applied `tools/tsukuroi-census.sh:2454,2459` expands `"$d/error"/**/*` and `"$d/log"/**/*` after enabling only `globstar`, not dot-inclusive traversal. In receipt i, each tree has `visible` and `.hidden`, both readable regular files. Independent `find ... -type f -readable` returns two per tree; arm emits `error=1 log=1 detail=none`. Frozen enumeration has no hidden-name exclusion. Enumerate all readable regular files without following symlinks, and test both hidden files and hidden subdirectories.

## Scope, axes and identity

Axes: operability/C2, honest enumeration, read-only safety, echo integrity, verdict neutrality. No axis or frozen predicate amended; no admission/judgment/ship action performed.

Frozen declaration: `1710bd74aec840c71d5e4ffbdc0ca54198e953fa`, SCORECARD section “Round 70 — declaration”. Shared clone base HEAD: `84e013a732d7526d08064c6823858d602029ecd7`. Clone toplevel asserted as `/fast/scratch/hyaku/tsukuroi-r70/R2Reviewer/clone` before applying the patch. Patch: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-70/probes/E1XfsArm/r70-xfs-arm.diff`, sha256 `88d94bc81e1cae7a0fc8c4c469f43dd1a265fa7045bab3a4f154f8699b698406`. Applied script sha256: `ee6d0bd042b74399080eaadeab6bdf667291db8308948cbf27749478ce6e83b8`. All code references below identify that applied script or the immutable diff, not a later lane revision.

LSP device unavailable: `read xd://lsp` returned “No such tool”; therefore definition/caller/diagnostics requests could not be made. Text search and source inspection are literal fallback evidence, not semantic proof. Definitions inspected: `xfs_detail_add:2394`, `probe_xfs_arm:2398`; live caller at 4643, emitter at 4644. Six existing rollup terms at 4646–4655 and exit map at 4657 onward remain unchanged. Canonical runtime is the existing Bash census script; no competing agent/runtime, resume implementation, rerouting or saturation claim is introduced by this diff.

## Executed verification

Baseline selftest before applying patch: rc 0, 196 cases / 196 passed / 0 failed. Patched command: `/usr/bin/bash /fast/scratch/hyaku/tsukuroi-r70/R2Reviewer/clone/tools/tsukuroi-census.sh --selftest`, with `TMPDIR=/fast/scratch/hyaku/tsukuroi-r70/R2Reviewer`. Result: `TSUKUROI_CENSUS_SELFTEST: PASS (212 cases, 212 passed, 0 failed)`, rc 0. The 16 R70-C2 labels were:

- PASS healthy: two xfs mounts, two present roots, both stats files valid, 4 error and 4 log files (R70-C2) (exit 0, HEALTHY)
- PASS healthy: a listed xfs mount with no sysfs root counts absent and names sysfs:absent (R70-C2) (exit 0, HEALTHY)
- PASS healthy: a mode-000 stats file is never counted and names stats:unreadable (R70-C2) (exit 0, HEALTHY)
- PASS healthy: a first line outside the frozen shape names stats:malformed and is not counted (R70-C2) (exit 0, HEALTHY)
- PASS healthy: a FIFO stats file is never opened (no block) and a FIFO is never counted under error/log (R70-C2) (exit 0, HEALTHY)
- PASS healthy: an escaped-space source and an embedded forged line never forge the census line (R70-C2) (exit 0, HEALTHY)
- PASS healthy: the global stats directory under the sysfs root is never counted as a filesystem (R70-C2) (exit 0, HEALTHY)
- PASS healthy: a host with no xfs mount reads all zeros, detail=none, no absent noise (R70-C2) (exit 0, HEALTHY)
- PASS healthy: an unreadable mount table reads all zeros with detail=mounts:unreadable (R70-C2) (exit 0, HEALTHY)
- PASS healthy: one source mounted twice counts once, so the fields stay per-filesystem (R70-C2) (exit 0, HEALTHY)
- PASS healthy: an existing-but-unreadable sysfs root counts unreadable, never absent (R70-C2) (exit 0, HEALTHY)
- PASS healthy: an unlistable sysfs ROOT routes every listed mount to unreadable, never absent (R70-C2) (exit 0, HEALTHY)
- PASS healthy: a sysfs entry that is not a directory counts unreadable, never present or absent (R70-C2) (exit 0, HEALTHY)
- PASS healthy: only the FIRST stats line is judged, so a valid first line keeps stats=1 (R70-C2) (exit 0, HEALTHY)
- PASS xfs: one XFS line per run; rollup line, exit code and non-XFS line count identical with the arm inputs present or absent (exit 1) (R70-C2)
- PASS xfs: the emitted line carries every field, in contract order, once (R70-C2)

Live census, unprivileged: exactly one XFS line, at stdout position 15 (one-based), immediately after KERNEL and immediately before the rollup. `findmnt -rn -t xfs -o SOURCE` independently returned `/dev/nvme1n1p1` and `/dev/nvme1n1p2`, hence two distinct sources. Independent live `find` traversal enumerated 18 readable regular error files and eight log files. The earlier host prose says seven error files per filesystem; current enumeration is nine per filesystem and is the relevant frozen live-count predicate. Header and unrelated host-derived material deliberately withheld.

`XFS xfs-stats mounts=2 present=2 absent=0 unreadable=0 stats=2 error=18 log=8 detail=none`

Rollup before and after, and the supplied base capture, all equal:

`TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=DEGRADED drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)`

Live baseline and patched rc are both 1. A/B unified rollup diff is empty.

## One receipt per required break attempt

### a — Listed mount, absent sysfs device

Mount table contains `/dev/testdev /fixture xfs rw 0 0` plus an ext4 root; sysfs override is an existing empty directory. Absent=1, not a HEALTHY/zero reading.

`XFS xfs-stats mounts=1 present=0 absent=1 unreadable=0 stats=0 error=0 log=0 detail=sysfs:absent`

rc=1; fixture type/mode/content digest unchanged; stderr empty.

### b — FIFO stats file

Device exists; `stats/stats` is a FIFO. Full census invocation guarded by `/usr/bin/timeout 10 /usr/bin/bash <absolute census path>`; rc 1, not timeout rc 124. No FIFO writer exists.

`XFS xfs-stats mounts=1 present=1 absent=0 unreadable=0 stats=0 error=1 log=1 detail=stats:unreadable`

rc=1; fixture type/mode/content digest unchanged; stderr empty.

### c — Space/newline device names

Standard mount-table source `/dev/bad\040name`; an actual `bad name` directory exists beneath fixture sysfs. Second subcase `/dev/bad\012FORGED` has an actual newline-bearing directory. Both names are withheld with `echo:bad-name`; exactly one XFS line and no FORGED text emitted.

`XFS xfs-stats mounts=1 present=0 absent=1 unreadable=0 stats=0 error=0 log=0 detail=echo:bad-name`

rc=1; fixture type/mode/content digest unchanged; stderr empty.

Newline subcase: `XFS xfs-stats mounts=1 present=0 absent=1 unreadable=0 stats=0 error=0 log=0 detail=echo:bad-name`; rc=1, fixture digest unchanged, stderr empty.

### d — Malformed first stats line

A readable regular stats file starts with `garbage`; observed stats=0 and fixed token stats:malformed.

`XFS xfs-stats mounts=1 present=1 absent=0 unreadable=0 stats=0 error=1 log=1 detail=stats:malformed`

rc=1; fixture type/mode/content digest unchanged; stderr empty.

### e — Unreadable stats file

A regular stats file has mode 000. Unprivileged run observed stats=0 and stats:unreadable. Directory presence remains separate from stats readability.

`XFS xfs-stats mounts=1 present=1 absent=0 unreadable=0 stats=0 error=1 log=1 detail=stats:unreadable`

rc=1; fixture type/mode/content digest unchanged; stderr empty.

### f — Zero XFS mounts

Readable nonempty mount table contains only an ext4 root. Every XFS count is zero with detail=none; no absent noise.

`XFS xfs-stats mounts=0 present=0 absent=0 unreadable=0 stats=0 error=0 log=0 detail=none`

rc=1; fixture type/mode/content digest unchanged; stderr empty.

### g — Rollup/exit A/B

Unpatched clone live census: rc 1. Same clone with only frozen patch applied: rc 1. Rollup strings byte-equal and equal to declaration base capture; unified rollup diff empty. Every required fixture invocation also emits that same rollup and exits 1. Patched selftest additionally exercises a hermetic present/absent XFS-seam A/B with degraded systemd fixture, unchanged rollup/rc and exactly one XFS line in each arm. The XFS count variables never feed `worse` or the exit-map case.

### h — No-write and callsite audit

Live arm survives no-write test: all eight required fixture invocations (c has two subcases) leave a SHA256 digest of entry names/types/modes and readable regular-file bytes unchanged. This deliberately excludes access timestamps and cannot prove absence of transient writes. Static added live-code audit complements it:

- Diff line 83: `cat -- "$mtab" 2>/dev/null` reads the validated regular mount table; `2>/dev/null` discards diagnostics, not a control write.
- Diff line 84: `read -r src mp fst rest` consumes the captured mount table. Diff line 138: `done <<< "$mtabbuf"` supplies an internal here-string, not a host target.
- Diff line 110: `IFS= read -r first < "$f" || true` is the only stats-content input redirection, gated by `-f` and `-r` at line 108.
- Diff lines 120–132: `shopt -p/-s/-u globstar` inspects/restores process shell options; `for` plus `test` and arithmetic only enumerate metadata. `xfs_detail_add` has only constant-token callers; its assignments mutate shell memory only.
- Diff lines 143 and 312: compose `XFS_LINE`, then `printf '%s\n' "$XFS_LINE"` to inherited stdout. There is no live destination redirection, `tee`, file creation/deletion/permission operation, privilege escalation, package transaction, or XFS command call added.
- HOWEVER the full patch is not write-free: diff lines 166–175 define selftest `xfs_fs`, calling mkdir and six redirected printf writes; selftest case setup at 177–270 adds mkdir, printf redirections, `:` redirection (219), chmod (190/193,228/231,241/244,248/251), rm and mkfifo (204–205), and calls fixture helpers. These execute only through `run_selftest` / `--selftest`, never through the live probe. The specifically forbidden fixture filenames are finding F1. Accordingly h is a safety-policy break for the complete delivered patch, not a live-host mutation finding.

## Additional enumeration receipts

### i-hidden

Independent `find <error> <log> -type f -readable` requires error=2 log=2. Actual: `XFS xfs-stats mounts=1 present=1 absent=0 unreadable=0 stats=1 error=1 log=1 detail=none`; rc=1, stderr empty. Rollup unchanged.

### j-symlink

Independent `find <error> <log> -type f -readable` requires error=1 log=1. Actual: `XFS xfs-stats mounts=1 present=1 absent=0 unreadable=0 stats=1 error=2 log=2 detail=none`; rc=1, stderr empty. Rollup unchanged.

## QUALITY 84 echo discipline

Diff lines 73–74: `local name_re='^[A-Za-z0-9._:-]+$'` and `local stats_re='^[a-z][a-z0-9_]*([ ][0-9]+)+$'`. Lines 93–95 gate basename path construction: `if ! [[ $name =~ $name_re ]]; then` followed by `absent=$((absent + 1)); xfs_detail_add 'echo:bad-name'; continue`. No source/basename/path, error/log filename, or stats content is inserted in the output line. Space and newline-bearing fixture names therefore cannot forge fields or lines.

All printed counts originate as literal zero and change only via `=$((... + 1))`; they are computed integers rather than echoed input. Diff line 143 spells the entire fixed field sequence:

`XFS_LINE="XFS xfs-stats mounts=$mounts present=$present absent=$absent unreadable=$unreadable stats=$stats error=$errn log=$logn detail=${detail:-none}"`

The only `xfs_detail_add` call arguments are fixed literals `echo:bad-name`, `sysfs:unreadable`, `stats:malformed`, `stats:unreadable`, `sysfs:absent`, `mounts:unreadable`; no dynamic caller exists in this diff. `none` is a fixed fallback; the helper deduplicates tokens. Closed echo grammar survives both forgery subcases. QUALITY 84's generic BLOCKED wording cannot be used to add XFS to the rollup: the frozen C2 contract expressly makes the line verdict-neutral.

## Residual risk and verification gaps

Findings F2/F3 are fixture-reproducible contract errors; actual canonical-host counts match the frozen live predicate. No symlink/hidden entry was observed on the live XFS trees. No race injection between metadata validation and file open was attempted; checks are not atomic. No mount-source alias resolution or future revision was tested. Read-only evidence does not establish resumed-run continuity or saturation; those are not changed by this patch. No assertion about universal write containment is made. No tool install/update, host service change, judgment, integration, commit or push performed.

Execution-discipline deviations: besides F1's executed fixture writes and my named `max_retries` fixture file, an early read-only `git show` named the lane rather than the sandbox, contrary to the user's all-git-calls-in-clone rule. A preliminary clone command also failed because its requested cwd did not yet exist; retry created only the intended scratch tree. These do not mutate the lane but are explicitly disclosed rather than claimed conformant.

Scratch `/fast/scratch/hyaku/tsukuroi-r70/R2Reviewer` removed recursively before report delivery; nonexistence confirmed. All per-attempt receipts and exact output lines needed for the review are retained above; disposable raw host captures were not retained. Only this scoped report is delivered.

Self-evaluation: accuracy 4 (direct command outputs, with static/no-write limits stated); completeness 4 (a–h plus two counting mutants, LSP unavailable); clarity 4 (findings separated from passing behavior); actionability 4 (specific affected code and counterexamples, no reviewer fixes); conciseness 4 (detailed audit requested). Mean 4.0; no broader correctness or safety claim.

Counting: ten attack groups a–j (c has two subcases); breaks are h's explicit fixture-policy violation and the two regular-file enumeration mutants; seven remaining required groups survive. Three actionable findings, two runtime counting defects and one execution-policy defect. Recommendation only, not admission.

SELFTEST_RC=0 CASES=212 R70C2=16
LIVE_LINE=XFS xfs-stats mounts=2 present=2 absent=0 unreadable=0 stats=2 error=18 log=8 detail=none
ROLLUP_EQ=1 BREAKS=3 SURVIVORS=7 FINDINGS=3

## Revised-patch re-review — supersedes the open findings above

After initial delivery, E1 supplied a revised diff at the same path: sha256 `003cf0d5a98e39d7411bc5f39b8cde220f54218afd3f21192ed8793e8637f1ad`. Previous sections preserve the original hash-bound review, not allegations against this revision. “Immutable diff” above denotes the originally reviewed bytes, not an immutable shared pathname. A fresh shared clone was created, its toplevel asserted, and the revised patch applied. Applied script sha256: `7324c1a81f3d70c75edfa1328239c34cdf39d248498db6f813a62102b48a827d`.

**Current actionable findings: none.** F1's prohibited fixture targets have been removed; literal search found no `stats_clear`, `fail_at_unmount`, or `max_retries` in the revised patch. Revised custom fixtures use ordinary filenames. Historical execution deviations remain disclosed, not erased by the repair. F2/F3 are repaired by default non-following GNU find traversal, revised diff lines 123–126:

```bash
cnt=$(find "$d/error" -type f -readable -printf 'x' 2>/dev/null || true)
errn=$((errn + ${#cnt}))
cnt=$(find "$d/log" -type f -readable -printf 'x' 2>/dev/null || true)
logn=$((logn + ${#cnt}))
```

Only fixed `x` markers enter this intermediate string; filenames never reach the output. These calls read metadata and add no live write sites. Existing basename/stat closed patterns, fixed detail callers, field construction and verdict-neutral main integration remain unchanged in substance.

Independent rerun: selftest rc 0, `TSUKUROI_CENSUS_SELFTEST: PASS (214 cases, 214 passed, 0 failed)`; 18 R70-C2 labels. The original sixteen labels remain, plus:

- `PASS healthy: dot files under error/ and log/ are regular files and are counted (R70-C2) (exit 0, HEALTHY)`
- `PASS healthy: a symlink entry and a symlinked dir are not regular files; only real files count (R70-C2) (exit 0, HEALTHY)`

Live line remains exactly once, between KERNEL and rollup, rc 1:

`XFS xfs-stats mounts=2 present=2 absent=0 unreadable=0 stats=2 error=18 log=8 detail=none`

Revised per-attempt receipts; every custom invocation has rc 1, empty stderr, no forged text and unchanged fixture type/mode/content digest:

- a absent: `XFS xfs-stats mounts=1 present=0 absent=1 unreadable=0 stats=0 error=0 log=0 detail=sysfs:absent`
- b FIFO, timeout 10, no timeout: `XFS xfs-stats mounts=1 present=1 absent=0 unreadable=0 stats=0 error=1 log=1 detail=stats:unreadable`
- c space: `XFS xfs-stats mounts=1 present=0 absent=1 unreadable=0 stats=0 error=0 log=0 detail=echo:bad-name`
- c newline: `XFS xfs-stats mounts=1 present=0 absent=1 unreadable=0 stats=0 error=0 log=0 detail=echo:bad-name`
- d garbage: `XFS xfs-stats mounts=1 present=1 absent=0 unreadable=0 stats=0 error=1 log=1 detail=stats:malformed`
- e mode 000: `XFS xfs-stats mounts=1 present=1 absent=0 unreadable=0 stats=0 error=1 log=1 detail=stats:unreadable`
- f zero: `XFS xfs-stats mounts=0 present=0 absent=0 unreadable=0 stats=0 error=0 log=0 detail=none`
- g valid arm: `XFS xfs-stats mounts=1 present=1 absent=0 unreadable=0 stats=1 error=1 log=1 detail=none`. Every revised fixture rollup and the revised live rollup equal the supplied base capture and the initial unpatched baseline; every rc is 1. Revised selftest additionally passes its identical-invocation seam A/B.
- h no-write audit: new `find` calls read metadata and discard stderr to `/dev/null`; existing mount/stats input redirections and fixed stdout emission are unchanged. Revised selftest still uses mkdir, redirected printf, chmod, rm, mkfifo and newly ln for ordinary fixture files, but no prohibited control-name targets remain. This is not a claim that selftest is write-free.
- i hidden: `XFS xfs-stats mounts=1 present=1 absent=0 unreadable=0 stats=1 error=2 log=2 detail=none`, now equal to the two regular files per tree.
- j symlink: `XFS xfs-stats mounts=1 present=1 absent=0 unreadable=0 stats=1 error=1 log=1 detail=none`, now equal to the one actual regular file per tree, excluding each symlink.

Residual risks unchanged: no LSP device, no race/atomicity proof, fixture hashes exclude access timestamps and cannot exclude transient writes. Recommendation only, not admission. No resumed-run, rerouting or saturation behavior is added. Second scratch tree removed and nonexistence confirmed before this addendum. Ten groups a–j now survive; c includes two independently exercised forgery encodings. Historical findings remain in the original review; final keys below describe the revised patch.

SELFTEST_RC=0 CASES=214 R70C2=18
LIVE_LINE=XFS xfs-stats mounts=2 present=2 absent=0 unreadable=0 stats=2 error=18 log=8 detail=none
ROLLUP_EQ=1 BREAKS=0 SURVIVORS=10 FINDINGS=0
