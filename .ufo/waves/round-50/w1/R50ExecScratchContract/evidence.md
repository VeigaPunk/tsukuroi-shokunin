# R50ExecScratchContract evidence

Tested frozen revision `8029cdba1049df25632c91a23c8db4eefb54be5f`. Extracted counters from that revision with `git show`; SHA-256: `check-selftest-matcher-r50.py` = `ec24f5887d5b735bc61ede11587c75e72d81c0cf55fca937b322be81e74d7aa6`; `check-adjacency-table-r50.py` = `d571adc9562b2832baf270086181c770b25eea6c5147d49b27a1525564e00a8b`.

## Commands and observed counter output

Both runs per counter used `TMPDIR` on `/fast/scratch`:
- Space path: `/fast/scratch/hyaku/tsukuroi-r50/R50ExecScratchContract/tmp plain`.
- Plain path: `/fast/scratch/hyaku/tsukuroi-r50/R50ExecScratchContract/tmpplain`.
- Each run was traced with `strace -f -e trace=%file -o <log>`; C2 was invoked with `--scratch` on `/fast/scratch` (space path for first run; plain path for second); both were passed `--lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin` and the frozen revision.

C2 space-TMPDIR run: shell reported `RC_SPACE=0`; JSON fields: `verdict=PASS`, `idiom_sites=0`, `base_misses=20`, `full_misses=0`, `cases=168`, `pass_runs=2`, `case_ok=1`; both selftests reported `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` and the `(R50-C2)` line. Elapsed 173 seconds. After exit, `find "$S/scratch space" -mindepth 1` returned `0` entries.

C2 plain-TMPDIR run: shell reported `RC_PLAIN=0`; same JSON metrics and both 168/168 selftest summaries; elapsed 150 seconds. After exit, `find "$S/scratchplain" -mindepth 1` returned `0` entries.

C3 space-TMPDIR run: `RC_SPACE=0`, JSON `verdict=PASS`, `adj_rows=7`, `linked_rows=7`, `bare_ranges=0`, `anchors_ok=7`, `registry_ok=7`, `anchors_checker_rc=0`, `quote_at_pin_ok=9`, `live_quote_ok=9`, `stub_fails=1`.

C3 plain-TMPDIR run: `RC_PLAIN=0`, same metrics and `verdict=PASS`.

Full C2/C3 JSON output and strace logs were captured under the scratch directory named in the test commands; scratch was removed after this receipt was copied.

## Write-location audit

C2 space strace: parsed exact absolute paths on write-intent `openat` calls; **0 destinations under `/tmp`**, **0 under `/home/vgpnk/Projects/shokunin` (lane/fleet)**, and no other absolute write destination outside the owned scratch tree. The 23,416 open-intent paths spelled `/proc/self/fd/240/...` are the census selftest's TMPDIR alias: the trace shows the C2-generated `work/tmp` under `--scratch`, and the census changes directory through `/proc/self/fd/240/tsukuroi-r3-2-selftest.*` before its relative fixture creates. The 406 successful mutations through that alias are inside that scratch-resident selftest tree; direct successful scratch mutations were 8. The thousands of `/dev/tty` opens failed with `ENXIO`; successful `O_RDWR` opens were `/dev/null` subprocess redirections. C2 plain run also passed and its traced scratch work tree was empty after exit.

C3 space/plain strace logs each had 11,301 lines. Each showed 209 write-intent opens, all to `/dev/null`; **zero mutating syscalls**, **zero `/tmp` paths**, and no lane/fleet write path. C3 invokes `check-adjacency-anchors.py --revision <rev>` only; its file-writing fixture code is in its `--selftest` path, not the invocation exercised here.

`find /tmp -xdev -newer <marker>` was attempted after C2. It reported 18 newer paths (including `/tmp` itself and unrelated worker/round files) and permission errors on systemd-private directories, so that global snapshot is inconclusive in this concurrent wave. Per-process strace is the write-location evidence and recorded no counter write to `/tmp`.

## Source inspection evidence

Frozen C2 counter source: creates `work = tempfile.mkdtemp(dir=a.scratch, prefix='matcher-r50.')`; passes `TMPDIR=os.path.join(work, 'tmp')` and `HOME=os.path.join(work, 'home')` to the census selftest; removes `work` in `finally` with `shutil.rmtree(work, ignore_errors=True)`. Frozen C3 counter docstring says “Writes nothing”; its implementation has no tempfile or write calls and invokes the checker with `--revision`.

Frozen census source (`tools/tsukuroi-census.sh`): the selftest base is `base=${TMPDIR:-/tmp}` (line 2094 in the frozen source); comments state unset/empty TMPDIR uses `/tmp`, while dirty TMPDIR resolves through an in-TMPDIR `/proc/self/fd` alias and invalid TMPDIR fails without fallback (lines 2055-2063, 2119-2135). Thus the explicit `/tmp` default remains only when TMPDIR is unset/empty; it was not used in these runs.
