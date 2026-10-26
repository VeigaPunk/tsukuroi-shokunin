VERDICT: defect-found

# C1-7 — line-by-line review of the round-39 block + 4 new selftest cases (tools/tsukuroi-census.sh @ 49cc53c7)

Reviewed at commit 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82 (scratch clone `/fast/scratch/hyaku/tsukuroi-r39/C1RevBash/lane`; `git rev-parse HEAD` there = `49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82`). Shell options: `set -euo pipefail` at tools/tsukuroi-census.sh:420; no `shopt`, no `set -f`; `cap()` (577-582) and the selftest harness (2134/2166, 2210/2213) toggle `set +e`/`-e` and restore it. bash 5.3.20(1)-release. Method: static read + 12 adversarial cases appended to a scratch copy of the script and run through the production selftest harness (129/129 PASS — receipts/mutant-selftest.out), plus direct census runs. No LSP device answered for this bash file in this session — text review + fixtures used instead. No tools installed (none needed).

## The six named checks — all hold

1. **`mtab=$(cat ...)` inside `if` with errexit/pipefail — SAFE.** census.sh:1906 `if mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null); then` is an assignment in if-condition position, so errexit cannot fire on cat failure; failure routes to the else at 1911-1912 (`blocked=1; detail+='mounts:unreadable,'`). No pipe, so pipefail is not exposed. Fixtures: exists-but-unreadable table (chmod 000) → `BLOCKED ... detail=mounts:unreadable` (mutant case `x-mt-chmod000`, PASS); table replaced by a directory → same (`x-mt-dir`, PASS); absent table → same (shipped case `storage-mounts-unreadable`, census.sh:2984-2987, PASS). Note: the shipped selftest pins only the absent-table leg; the exists-but-unreadable (EACCES) leg is covered by my mutant case.
2. **Here-string on an empty table — SAFE.** census.sh:1909 `done <<< "$mtab"` with `mtab=""` delivers exactly one empty line; the body runs once with empty fields, guarded by `${fst:-}` at 1908; loop rc 0 (receipts/read-split-demo.txt: `body: a=[]`, `loop_rc=0`). Fixture: zero-byte table → `HEALTHY 0/0/0`, no crash (`x-mt-empty`, PASS).
3. **Octal escapes (`\040`) and fstype field position — SAFE.** `read -r` at 1907 preserves backslash escapes (receipts/read-split-demo.txt: `mp=[/mnt/w\040s] fst=[btrfs]`), and `fst` is field 3 — the fstype in /proc/self/mounts order (device, mountpoint, fstype, options, dump, pass); escapes contain no IFS whitespace, so they cannot shift the field. Fixture: four btrfs lines with `\040`/`\011`/`\134`/`\012`-escaped mount points → `BLOCKED ... detail=mounts:btrfs-without-sysfs` (`x-mt-escapes`, PASS). fx_default's table (census.sh:2030) and the case table `fxmt` (2973) both put fstype at field 3.
4. **Very long tables — SAFE.** 200,001-line / 6.2 MB table with the btrfs line last → correct `BLOCKED ... mounts:btrfs-without-sysfs`; whole-census wall time 4.122 s vs 3.420 s baseline (receipts/long-table-timing.txt) — the read loop costs ~0.7 s. A ~340 KB single options line also parses (`x-mt-longline`, PASS). No ARG_MAX exposure: the table is never expanded into an argument list (cat → variable → here-string → `read -r` loop is O(n), memory-bounded).
5. **`local` placement — SAFE.** census.sh:1905 `local mtab mt=0 _src _mp fst _rest` declares without assignment; the assignment happens at 1906 inside the `if`, so the failure-masking `local x=$(cat ...)` pattern (where `local`'s rc hides the substitution's rc) is avoided. The outer `local` (1863) contains no command substitutions. receipts/errexit-while-demo.txt shows the hazard class and why this body shape is safe: a failing while-body kills the shell under `set -e` (`rc=1`, no `reached`), but an if-without-else body always returns 0 (`reached`, rc=0) — the census body at 1908 is exactly that shape, and `mt=$((mt + 1))` is an assignment (rc 0).
6. **fx_default's new mounts file + EXTRA_ENV — CORRECT.** fx_default writes a no-btrfs mtab-format table (census.sh:2029-2030, comment "no btrfs mount, so an absent sysfs root stays 0/0/0"), which keeps the round-38 case `storage-absent` (2925-2928) HEALTHY under the new guard. `check()` passes `TSUKUROI_PROC_MOUNTS="$FX/mounts"` (2161) and `TSUKUROI_BTRFS_SYSFS="$FX/btrfs"` (2160) to EVERY case, with `"${EXTRA_ENV[@]}"` appended after (2163) so a case may override. `check_cli` runs with no fixture env (2204-2205) but only arms that exit before any probe (the three CLI cases exit 2/2/0 at parse). Exactly two census self-invocation sites exist (2164, 2211; the third grep hit is check_cli's own comment at 2204).

The four new selftest cases (census.sh:2972-2992) pin all three declared legs plus the negative: hidden-absent (2974-2977), hidden-empty root holding only `features` (2979-2982), unreadable=absent table (2984-2987), and populated-root-ignores-table (2989-2992). Base selftest at the pinned commit: 117/117 PASS; with my 12 appended cases: 129/129 PASS (receipts/mutant-selftest.out).

## Defect D1 (low severity, latent): an explicitly empty TSUKUROI_PROC_MOUNTS or TSUKUROI_BTRFS_SYSFS silently falls back to the live host path

census.sh:459-460 use `${VAR:-default}`, which treats an explicitly empty override as unset:

```
BTRFS_SYSFS=${TSUKUROI_BTRFS_SYSFS:-/sys/fs/btrfs}
PROC_MOUNTS=${TSUKUROI_PROC_MOUNTS:-/proc/self/mounts}
```

The lane's own precedent for this exact class is the ROOT_DIR guard at census.sh:435-437 (`${VAR-default}`, not `:-`, plus a `${VAR+set}` probe) with the comment at 431-434: "an explicitly empty TSUKUROI_ROOT_DIR must read as unavailable, never silently become the live `/`" — pinned by selftest case `blocked-root-empty-override` (2803-2807). The storage arm's two overrides do not follow it, so a selftest case or counter leg that sets either var empty silently reads host state, breaking the hermeticity promise at census.sh:389-390 ("the selftest touches no host state").

Reproduction A — `TSUKUROI_PROC_MOUNTS=` (receipts/override-leak-demo.txt; fixture: no btrfs sysfs dir, table without btrfs; live /proc/self/mounts lists 4 btrfs mounts):

```
$ TSUKUROI_BTRFS_SYSFS=$FX/no-btrfs TSUKUROI_PROC_MOUNTS= bash lane/tools/tsukuroi-census.sh | grep ^STORAGE
STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs
$ TSUKUROI_BTRFS_SYSFS=$FX/no-btrfs TSUKUROI_PROC_MOUNTS=$FX/mounts bash ... | grep ^STORAGE
STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0
```

Same fixture, only the override differs: the empty override read the LIVE table. Also reproduced inside the production harness: mutant case `x-mt-empty-override` (`EXTRA_ENV=(TSUKUROI_PROC_MOUNTS=)`) PASSed expecting the BLOCKED line (receipts/mutant-selftest.out).

Reproduction B — `TSUKUROI_BTRFS_SYSFS=` (same receipt; live /sys/fs/btrfs holds fsid 1d02a454-c549-4a35-b567-89d60902af8e):

```
$ TSUKUROI_BTRFS_SYSFS= TSUKUROI_PROC_MOUNTS=$FX/mounts bash ... | grep ^STORAGE
STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0
$ TSUKUROI_BTRFS_SYSFS=$FX/no-btrfs TSUKUROI_PROC_MOUNTS=$FX/mounts bash ... | grep ^STORAGE  (control)
STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0
```

The empty override reported the LIVE filesystem (1 fs, 1 device) inside a fixture run.

Impact today: latent — no current selftest case passes either var empty, and the declared claim's three legs behave exactly as written (census.sh:364-368 vs 1903-1914). But the class is one EXTRA_ENV entry away from a nondeterministic selftest, and the lane has already ruled it a defect for ROOT_DIR.

Proposed text (for the implementer; this seat is read-only on lane content and applied nothing):
- census.sh:459-460 → detect set-but-empty like ROOT_DIR (435-437), e.g. `PROC_MOUNTS=${TSUKUROI_PROC_MOUNTS-/proc/self/mounts}` with the arm treating an explicitly empty value as unreadable (fail closed → `mounts:unreadable` / root-unreadable), plus one selftest case per var pinning `EXTRA_ENV=(TSUKUROI_PROC_MOUNTS=)` → BLOCKED.
- Minimal alternative: document the `:-` semantics at the header override list (census.sh:405) so an empty override is a documented live-path fallback.

## Residual risks (observed, not defects)

- **Format assumption:** the arm parses mtab format only (fstype at field 3). A mountinfo-format table (e.g. /proc/self/mountinfo) is silently unparsed → a hidden btrfs reads HEALTHY (mutant case `x-mt-mountinfo`, PASS expecting HEALTHY). Misuse-only: census.sh:405 documents the default as /proc/self/mounts.
- **CRLF:** a 3-field line ending `btrfs\r` misses (`fst=btrfs<CR>` ≠ btrfs) → silent HEALTHY (`x-mt-crlf`, PASS). Kernel tables never emit \r.
- **Fifo table:** `cat` blocks forever on a fifo with no writer; the census printed all six `PLANE` lines but 0 `STORAGE` lines and 0 rollup lines within a 12 s window (baseline prints at ~3.4-4.1 s) and had to be killed (receipts/fifo-hang.txt). Override-only hazard; a killed run can orphan the stuck `cat`.
- **Precedence:** when the sysfs root is unreadable (`blocked=1`), the mount table is not consulted — `detail=root:unreadable` only (`x-mt-root-unreadable-precedence`, PASS). Honest (already BLOCKED); worth a header sentence if the precedence is ever relied on.
- **Here-string temp files:** strace of `while read ... done <<< hello` with a watched TMPDIR shows no temp file (receipts/herestring-strace.txt), so the header's "creates no files at all in live mode" (census.sh:381-382) holds even when the mtab branch runs.

## What I did not do

- Did not audit tools/score-storage-hidden-r39.py or the frozen counter legs (other seats' items); the D1 risk note for the counter is inference from the env contract, not a counter run.
- Did not test NUL bytes in the table (bash command substitution drops them; a kernel-generated table cannot contain NUL) or >100 MB tables.
- No mutating git/jj command ran in the lane; the scratch clone (--shared, origin removed) was checked out to 49cc53c7 and deleted after receipts were copied. No packages or tools installed; no host mutation (all census runs are read-only; fixtures lived under /fast/scratch/hyaku/tsukuroi-r39/C1RevBash/ and were removed at the end).
