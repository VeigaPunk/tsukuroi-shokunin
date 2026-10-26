VERDICT: supports

Seat C1FinalENOSPC — item F-4: reproduce C1RevFix defect D1 (a full temp dir turns an error-bearing large `-Qkk` sample into `PLANE packages: HEALTHY` / exit 0) on the census at 447662088dfd3155e31aed239179a79c1d1046c7, and show it is gone at the wave tip 78abb8b5cdc9da511b4fc523e661517a68dd33d3 (here-strings replaced by an awk test); also strace the tip run for any write-open outside the fixture.

**Result.** D1 reproduces exactly on the census at 4476620: with a 304126-byte error-first `pacman -Qkk` sample and TMPDIR (or `/tmp`) on a 1 MiB tmpfs filled to 100 %, the packages plane reads `HEALTHY`, the run prints `TSUKUROI_CENSUS: HEALTHY`, and the process exits **0** — matching C1RevFix E3/E4 token for token (`.ufo/waves/round-42/w1/C1RevFix.md:30` and its `r-e2e.txt`). At 78abb8b5 the same fixture, same env, same full temp dirs, yields `PLANE packages: BLOCKED`, `TSUKUROI_CENSUS: BLOCKED`, exit **2**, empty stderr; the two TMPDIR states produce byte-identical output (timestamp masked). The tip trace shows **zero** write-opens outside the fixture apart from `/dev/null` and `/dev/tty`, and no `creat`/`mkdir`/`unlink`/`rename` at all. The item's statement holds: supports.

Lane tip at run time was `a968393c` (one receipt commit past 78abb8b5); the tracked census is blob `18a1db6448358d7ecf4634570fcd2bf075eccb1b`, byte-identical to `78abb8b5:tools/tsukuroi-census.sh` (`git diff --stat 78abb8b5 -- tools/tsukuroi-census.sh` empty), so the line numbers below are the lane's own file.

## Method (exactly the C1RevFix r-e2e fixture, re-derived)

- Census blobs read read-only out of git into scratch: `git show 44766208:tools/tsukuroi-census.sh` (sha256 `46d62a24709ece8efbcd231f4c269bd5b3791237e3c78ac7433fb0115494f1b1`) and `git show 78abb8b5:tools/tsukuroi-census.sh` (sha256 `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9`). No lane file touched.
- Fixture = the selftest's own `fx_default` (extracted verbatim from the 4476620 blob `:2025-2114`) plus the `blocked-sample-error-large` qkk shape (`:2355-2359`): `qkk.out` = 304126 bytes, line 1 `error: alpha: /usr/bin/alpha (Permission denied)`, then 4000 `warning:` lines, two `N total files, 0 altered files` rows; `qkk.rc=1`; `pq` = alpha/beta/gamma/delta. sha256 `fd9244165d330d22e5b78b8e4c4d07c6a29ea6b8e215add749930c87ede59c34`.
- Env = the selftest `check()` environment: live census with **every** `TSUKUROI_*` override stubbed at the fixture (`TSUKUROI_FIXTURE`, `TSUKUROI_PACMAN=$bin/pacman`, …, `TSUKUROI_PROC_MOUNTS=$FX/mounts`); the `bin/*` stubs are the selftest's own `.dispatch` heredoc, so `pacman -Qkk` answers from `$FX/qkk.out` with rc 1 while `-Qq` lists the four names. Full list in `r-fixture.txt`.
- Temp-dir legs, both in a private `unshare -rm` mount namespace (host `/tmp` and host mounts untouched): (a) `TMPDIR` = 1 MiB `tmpfs` on scratch, `dd`-filled; (b) `/tmp` itself is a private-ns 1 MiB `tmpfs` filled the same way, TMPDIR unset — C1RevFix's E4 shape; (c) control: writable 1 MiB `tmpfs`. `df -k` shows `1024 1024 0 100%` on every full leg (`df-4476620-full.txt`, `df-4476620-tmpfull.txt`).
- Tools (no installs): GNU bash 5.3.20(1)-release, GNU Awk 5.4.1, strace 7.2, unshare util-linux 2.42.4.

## R1 — D1 reproduces at 4476620 (`if grep -q '^error:' <<<"$s_out"`, :695/:697)

| rev | TMPDIR state | exit | packages plane |
|---|---|---|---|
| 4476620 | writable tmpfs | 2 | `BLOCKED (pacman -Qkk sample probe error: error: alpha: /usr/bin/alpha (Permission denied); …)` |
| 4476620 | **full 1 MiB tmpfs** | **0** | **HEALTHY** |
| 4476620 | TMPDIR unset, `/tmp` full | **0** | **HEALTHY** |

Full lines (both `HEALTHY` legs are identical):

```
PLANE packages: HEALTHY (pacman -Qkk rc=1 sample=4(alpha,beta,gamma,delta) drift=0 backup_diffs=0 nonroot_artifacts=1; foreign=0(known=0 new=0 drift=0 gone=0) base=file(0); pins=none; holds=pacman glibc; db.lck=absent; root_status=ok root_mode=0755 root_uid=0 root_gid=0 root_euid=0 root_owner_write=present root_owner_search=present root_src=override root_dir=<scratch>/fx/root)
PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: alpha: /usr/bin/alpha (Permission denied); root_status=ok root_mode=0755 root_uid=0 root_gid=0 root_euid=0 root_owner_write=present root_owner_search=present root_src=override root_dir=<scratch>/fx/root)
```

(Production path text keeps the real scratch absolute path; both receipts `4476620-full.out` and `4476620-rw.out` carry it verbatim.)

Verdict coupling: at 4476620/full the whole census line is `TSUKUROI_CENSUS: HEALTHY (packages=HEALTHY systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)`, exit 0; at 4476620/rw it is `… BLOCKED (packages=BLOCKED … update-safety=DEGRADED …)`, exit 2. The single here-string failure therefore also flips **update-safety** from `unavailable(not-run)` to `offline-exile:0,aur-local:0`: the qkk error path returns from `probe_packages` before the foreign fold, leaving `PKG_FOREIGN_FOLD='not-run'` (`tools/tsukuroi-census.sh:550`), which composes `classes=unavailable(not-run)` → DEGRADED (`:1779`); when the error is missed, the fold runs (`:1788`) and reports HEALTHY. One ENOSPC corrupts two planes' readings and the firmware-style exit code — this is precisely why C1RevFix saw exit 0 in E3/E4.

stderr on both full legs (nothing else):

```
<census-4476620.sh>: line 695: cannot create temp file for here-document: No space left on device
```

Mechanism, traced (`r-strace.txt`, full log `r-strace-file-4476620.log`):
- `openat(AT_FDCWD, "<scratch>/tmp-full/sh-thd.dMuxQT", O_RDWR|O_CREAT|O_EXCL, 0600) = 3` — a temp file is created in TMPDIR, outside the fixture, then `unlink`ed (log lines 570-571).
- the body write fails in a second `-e trace=openat,write` run: `write(3, "error: alpha: /usr/bin/alpha (Pe"..., 304126) = -1 ENOSPC (No space left on device)`; bash then writes `line 695: cannot create temp file…` to fd 2. The `if` sees status 1 and silently takes the else branch.

Isolated confirmation on the exact two forms with the same 304126-byte buffer and the same full tmpfs (`r-micro.txt`): old form prints the ENOSPC message and takes `ELSE-branch (wrong)`; new form prints `BLOCKED-branch note=[error: alpha: /usr/bin/alpha (Permission denied)]`.

Not a regression: at base the same buffer was misread regardless of the temp dir (C1RevFix T9a). D1 was new to 4476620 because the here-strings introduced a temp-dir dependence the base `printf | grep` form did not have.

## R2 — D1 is gone at 78abb8b5 (`if err_line=$(printf '%s\n' "$s_out" | awk '/^error:/ { if (!p) { print; p = 1 } } END { if (!p) exit 1 }')`, :697-701)

| rev | TMPDIR state | exit | packages plane | stderr |
|---|---|---|---|---|
| 78abb8b5 | writable tmpfs | 2 | `BLOCKED (… sample probe error: error: alpha: …)` | empty |
| 78abb8b5 | **full 1 MiB tmpfs** | **2** | **BLOCKED (same line, byte-identical to the rw leg)** | empty |
| 78abb8b5 | TMPDIR unset, `/tmp` full | **2** | **BLOCKED (same line)** | empty |

- `diff` of the tip rw and full-TMPDIR runs with only the timestamp masked: `IDENTICAL-TIP` — the packages plane is now TMPDIR-independent.
- Code at the lane's own path today, `tools/tsukuroi-census.sh:697-701`: `local err_line=''`; the pipeline `printf '%s\n' "$s_out" | awk '…'`; `PKG_NOTE="pacman -Qkk sample probe error: $err_line"`. The comment `:694-696` names D1 explicitly. awk consumes the whole input (no SIGPIPE) and reads a pipe, so no temp file is involved.
- Mechanism at the buffer: the awk side's stdout is a pipe, not a file — `fstat(1, {st_mode=S_IFIFO|0600, …})` and **0** `sh-thd` occurrences in the new-form micro trace (`r-micro.txt`).

## R3 — no-write contract at the tip (strace, same full-TMPDIR run)

`strace -f -qq -e trace=%file` over the whole tip census (`r-strace-file-tip.log`, `r-strace.txt`):

- total `openat` lines 1888: 186 under the fixture `fx/`, 150 of the stub dispatchers `bin/`, **0** under `/tmp`, `/var/tmp` or the lane, the rest host-system reads.
- write-flag opens (`O_CREAT|O_WRONLY|O_RDWR|O_TRUNC|O_APPEND`) outside `/dev/`: **0**. The only such opens are the null/console devices — `/dev/null` (60, shell `>/dev/null` redirections with `O_WRONLY|O_CREAT|O_TRUNC`) and `/dev/tty` (32, `O_RDWR|O_NONBLOCK`, all `ENXIO`).
- `creat(`, `mkdir*`, `unlink*`, `rename*`, `truncate`: **0 occurrences** in the whole trace.
- failed writes at tip: none (`grep 'write(.*= -1'` on the `openat,write` trace is empty), i.e. no ENOSPC anywhere.
- fixture immutability across a tip full-TMPDIR run: tree digest `a17acc4d…12ee256` before and after (the selftest's own `fx_hash` formula).

So on the packages path the letter of the census header (`:8-9`, "… or writes anything", and `:348`, "Live mode creates no files") now holds even when the temp dir is full; it did not at 4476620.

## Residuals (recorded, outside this item — L1's ledger)

- Here-strings remain at tip on other live paths (`tools/tsukuroi-census.sh:754, 762, 879, 1359, 1367, 1473, 1732, 1753, 1833, 1858, 1863, 1865, 1920`), plus the selftest-only `grep -qE … <<<"$out"` at `:2193` (introduced by this wave's fail-open fix). Every one of these would still need a temp file if its input ever exceeded 64 KiB with a writable-but-full temp dir; their inputs are bounded in practice (mount table, `/etc` listing, link/timer lists, selftest output), and none was exercised here.
- The selftest still has no case for a full or unwritable temp directory — D1's class remains uncovered by `--selftest`; the new awk form is nonetheless TMPDIR-free, so the case would be a regression guard only.
- Under `unshare -rm` the census reports `root_uid=0 … root_euid=0` (namespace root) instead of 1000; all cross-rev comparisons use the same namespace, and the mode/owner-write fields the root arm scores are identical, so the verdict is unaffected.

## Scope / not done

- Did not run the census `--selftest`, the frozen counter `tools/score-size-invariance-r42.py`, or any other counter — not this item, and the parent owns the post-integration gate.
- Did not fill the host `/tmp` or any shared temp dir: the `/tmp`-full leg is a tmpfs mounted over `/tmp` **inside** a private `unshare -rm` mount namespace, so the host filesystem was never touched.
- No lane mutation (no edit, add, commit, stash, checkout, jj), no writes outside this report, its receipt directory and scratch; no tools installed; scratch `/fast/scratch/hyaku/tsukuroi-r42/C1FinalENOSPC` removed after the receipts were copied.

## Receipts (this seat's directory)

`r-matrix.txt` (3×2 matrix with exact lines, verdicts, stderr, df), `r-strace.txt` (extract + counts), `r-micro.txt` (old-vs-new form under a full tmpfs, `fstat` FIFO proof), `r-fixture.txt` (blob/fixture hashes, env, versions), `r-code.txt` (numbered code regions of both blobs, remaining here-strings), `r-strace-file-tip.log`, `r-strace-file-4476620.log` (full `%file` traces), plus the raw runs `4476620-{rw,full,tmpfull}.{out,err,rc}`, `78abb8b5-{rw,full,tmpfull}.{out,err,rc}`, the `df-4476620-*.txt` captures (the 78abb8b5 `df` lines are quoted inside `r-matrix.txt`).
