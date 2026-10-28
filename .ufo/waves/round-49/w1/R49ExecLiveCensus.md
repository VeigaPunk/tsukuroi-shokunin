VERDICT: supports

# R49ExecLiveCensus — P-7: the live census is unchanged by C3

Kill rule tested: C3 (the fd-band diagnostic in `tools/tsukuroi-census.sh`) must leave the
**live** census output unchanged. Result: every PLANE / HANDOFF / DRIFT / STORAGE / SCRUB
line, the rollup line and the exit code are identical between the base blob
(6256760d…, the lane tip at round start) and the fixed blob (55c07cd3…, FREEZE) once digit
runs are stripped; the only differing tokens are the ones that also differ between two runs
of the *same* blob (timestamp, memory/PSI/swap counters). No line-shape change, no verdict
change, no exit-code change. Live mode creates no files.

## Bytes actually executed

| role | blob | source | sha256 of executed bytes |
|---|---|---|---|
| base | `6256760d1382ce4ce20fcba830d4b2912cfbf12b:tools/tsukuroi-census.sh` (git blob `1ad97580eb526bafc678ded479aa9389af591476`) | `git show <rev>:…` | `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426` (216047 B, 3718 lines) |
| fix | `55c07cd3f8bff2e12117c34d57b4c618de74d85c:tools/tsukuroi-census.sh` (git blob `61f9f6348981e3d4b37076afb24e1d554441fdeb`) | `git show <rev>:…` | `c66144d73da1ac376cfe756eab3a60340e18bce91d60abe24c444408b99a2e75` (218581 B, 3765 lines) |

Receipts: `R49ExecLiveCensus/base.sh`, `R49ExecLiveCensus/fix.sh` (byte-exact copies of the
two `git show` outputs).

Each run: `env -i PATH=/usr/bin:/bin LC_ALL=C HOME=<scratch> bash <blob>` (no arguments →
live mode), cwd = scratch dir. Nothing outside the scratch/wave dirs was written.

## Output diff

Normalisation per item: strip every digit run (`sed -E 's/[0-9]+/N/g'`).

```
$ cd …/out && for f in …; do sed -E 's/[0-9]+/N/g' $f.txt > $f.norm.txt; done
$ diff -u base-live-1.norm.txt fix-live-1.norm.txt ; echo rc=$?
rc=0
$ diff -u base-live-1.norm.txt base-live-2.norm.txt ; echo rc=$?      # same-blob noise baseline
rc=0
```
Full matrix (`R49ExecLiveCensus/COMPARE.txt`): all 11 normalised outputs share
`md5 4a1ef421db371859ff1af0a99d89a294` — 5 base runs (base-live-1, -2, -a, -b, -attr,
plus base-dirtytmp) and 5 fix runs (fix-live-1, -a, -b, -attr, plus fix-dirtytmp):

```
IDENTICAL  base-live-1 vs base-live-2      (same blob, second run: noise baseline)
IDENTICAL  base-live-1 vs base-live-a
IDENTICAL  base-live-1 vs base-live-b
IDENTICAL  base-live-1 vs base-live-attr
IDENTICAL  base-live-1 vs base-dirtytmp
IDENTICAL  base-live-1 vs fix-live-1
IDENTICAL  base-live-1 vs fix-live-a
IDENTICAL  base-live-1 vs fix-live-b
IDENTICAL  base-live-1 vs fix-live-attr
IDENTICAL  base-live-1 vs fix-dirtytmp
```

Line shape (digit-stripped) is equal for every pair; all 13 output lines are present in
every run: 1 header + 6 `PLANE` + 2 `HANDOFF ADJ-04` + `DRIFT` + `STORAGE` + `SCRUB` +
`TSUKUROI_CENSUS:` rollup. Raw byte counts are equal too (9110 B per run; no stderr output,
0 bytes on all `.err` captures).

Token-level diff (difflib on whitespace/punctuation-split tokens, receipts
`base-live-1.txt` / `fix-live-1.txt` / `base-live-2.txt`):

```
== token diffs base1 vs fix ==
(1, 'replace', ['2026-10-28T17:43:09Z'], ['2026-10-28T17:43:30Z'])
(4, 'replace', ['10309654/17870380'], ['10309788/17870508'])   # C5_pswp
(4, 'replace', ['335211'], ['335581'])                         # C5_sock_throttled
(4, 'replace', ['0.20'],   ['0.19'])                           # C6_psi_full_avg300
(4, 'replace', ['351990908'], ['352095847'])                   # C6_psi_full_total_us
(4, 'replace', ['10962720'],  ['11284588'])                    # C6_avail_kb
(4, 'replace', ['66556'],     ['66568'])                       # C6_shmem_kb
== token diffs base1 vs base2 (SAME blob, second run) ==
(1, … timestamp …) (4, C5_pswp) (4, C5_sock_throttled) (4, C6_psi_full_avg300)
(4, C6_psi_full_total_us) (4, C6_avail_kb) (4, C6_shmem_kb)
```
The base-vs-fix differing-token set is exactly the same token positions as the same-blob
noise set — all live counters, no structural token. Verdicts in both blobs and all runs:
`packages=DEGRADED systemd=BLOCKED drivers=DEGRADED journal=DEGRADED
update-safety=DEGRADED oom=DEGRADED` → `TSUKUROI_CENSUS: BLOCKED`, exit **2** in every one
of the 11 runs (base-live-1/-2/-a/-b/-attr, base-dirtytmp, fix-live-1/-a/-b/-attr,
fix-dirtytmp).

Extra probe of the changed code path (its precondition is a *dirty* TMPDIR): both blobs run
with `TMPDIR="<scratch>/dirty tmp"` (contains a space → the resolver's dirty branch) give the
same 13 lines, same rollup, exit 2, and the normalised bytes equal `base-live-1` (matrix
rows `base-dirtytmp`, `fix-dirtytmp`). Live mode therefore never reaches the resolver at all.

## Why live mode cannot see C3 (source check, both blobs)

- The delta is 3 hunks + 2 comment blocks: usage text (`fix.sh:601-609`), `selftest_base_dir`
  (`fix.sh:2063-2103`), its caller's error printing (`fix.sh:2112-2122`), the new selftest
  case (`fix.sh:3574-3602`). See `git -C <lane> diff 6256760d 55c07cd3 -- tools/tsukuroi-census.sh`
  → `1 file changed, 56 insertions(+), 9 deletions(-)`.
- `main()` → EOF is **byte-identical** between the blobs:
  `sha256 283b0bebdf125c54e40d91b8f8d96b8722747116817cf81a18e6f0dfc60af5b6` for both
  (`R49ExecLiveCensus/base-main.txt`, `fix-main.txt`; `diff` → IDENTICAL). `main()` starts
  at `fix.sh:3659`, the live probes at `fix.sh:3699`…`fix.sh:3744`; `run_selftest` is only
  reached from `fix.sh:3688-3689` (`if [ "$selftest" -eq 1 ]; then run_selftest`).
- All 11 `probe_*` functions are byte-identical between blobs (script-compared bodies; list
  of functions with any changed line: `[]`).

## No files created by live mode

- Scratch tree before/after the runs contains only my own artifacts plus the two blobs; the
  directory I gave the dirty-TMPDIR runs (`<scratch>/dirty tmp`) is still empty afterwards
  (`find "$S/dirty tmp" -mindepth 1` → no output).
- `find /tmp -maxdepth 1 -newer <marker> -name 'tsukuroi*'` inside single-run windows
  produced `[]` twice (base-live-1, and the attribution pair `base-live-attr` and
  `fix-live-attr`, where any newly appearing dir was inspected immediately).
- Caveat, reported honestly: other windows of the *same* size DO show new
  `/tmp/tsukuroi-r3-2-selftest.XXXXXX` dirs, but they are sibling seats' `--selftest`
  fixtures — **control windows with no census run of mine at all show the same churn**:

```
control_window=1 (no census run) new=[/tmp/tsukuroi-r3-2-selftest.7jGsRh ]
control_window=2 (no census run) new=[/tmp/tsukuroi-r3-2-selftest.HBYZXr ]
control_window=3 (no census run) new=[]
control_window=4 (no census run) new=[]
```
(one transient, `/tmp/tsukuroi-r3-2-selftest.bvlH0s`, was gone ~30 s after first sighting —
`stat` at 2026-10-28T17:44:35Z: No such file or directory). Structurally it cannot be mine:
`fix.sh:2124 work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")` is the only
`mktemp` call in either blob and lives inside `run_selftest`, unreachable without
`--selftest`. Receipt: `R49ExecLiveCensus/TMP-CHURN.txt`.

## One live line that legitimately differs, called out

`--identity` (a live, no-probe mode) prints the executed script's own hashes, so it must
change with the bytes:
`base: sha256=375aa737… bytes=216047 lines=3718` vs
`fix: sha256=c66144d7… bytes=218581 lines=3765` (`base-identity.txt`, `fix-identity.txt`,
both `verified=yes`, exit 0). This line is not among PLANE/HANDOFF/DRIFT/STORAGE/SCRUB and
its change is the intended one (identity by hash).

## Not done

- I did not run `--selftest` on either blob (not named in this item; the C3 counter seat owns
  it and each selftest is a 60 s / multi-CPU-minute run). The C3 selftest case's own
  pass/fail is therefore **not** evidenced here.
- No pacman/systemctl/journal writes, no lane-tracked file touched, no git/jj mutation
  anywhere (only `git show`/`git diff`/`git rev-parse` reads in the lane).
- No tool installed or upgraded (nothing was needed).

## Axis notes (godspeed)

- operability: live path provably untouched (main + 11 probes byte-identical; 11 runs
  identical after normalisation) — the fix cannot regress the census readers consume.
- kill-rule: satisfied with a same-blob noise baseline, so the "identical" verdict is not an
  artefact of normalising away everything: the same normalisation still distinguishes
  nothing between the blobs, while raw diffs show the counters moving within the noise set.
