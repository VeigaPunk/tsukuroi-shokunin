VERDICT: defect-found

Claim C1 (the seven round-42 early-reader sites in `tools/tsukuroi-census.sh` are load-bearing and the tip
`--selftest` passes 132/132 with four R42-C1 labels) is **supported on the production path and by five of the
seven single-site reverts**. Two defects are recorded, both in the *guard* rather than in the fix:
(D1) no shipped selftest case covers the `:743` baseline lookup — reverting it alone leaves `132/132 PASS`,
although a >64 KiB baseline fixture proves it is load-bearing (base exit 141 vs tip completion);
(D2) the selftest stub still contains the same `printf | grep -q` early-reader idiom the round removed from the
probes (`:2178`, `:2181`, `:2183`, `:2187`, `:2198`, `:2229`), and with a ~56 KB census output I observed that
assertion flip once (1 FAIL / 4 PASS over five runs of the identical case). Fail-closed direction only.

## 0. Objects and provenance

- Lane tip at my run: `a968393c`, which only adds `.ufo/waves/round-42/w2-*` files over the dispatch tip —
  `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --stat 78abb8b5cdc9da511b4fc523e661517a68dd33d3 HEAD`
  lists 8 files, none under `tools/`. My measurements therefore stand for tip `78abb8b5`.
- `tools/tsukuroi-census.sh` at tip and in the working tree are identical:
  `sha256sum tools/tsukuroi-census.sh` → `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9`
  = `sha256sum` of `git show 78abb8b5:tools/tsukuroi-census.sh`.
- Base copy `git show c8efaa3f:tools/tsukuroi-census.sh` → `646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95`.
- All work in `/fast/scratch/hyaku/tsukuroi-r42/C1FinalSelftest/` (removed at the end). No lane file was
  written, no git/jj state touched, no host mutation, no install, no counter run.

## 1. Tip selftest: PASS 132/132, four R42-C1 labels

Command (scratch copy of the tip blob, `TMPDIR` inside scratch):

    bash ./census-tip.sh --selftest      # RC=0, elapsed 26.5 s

Observed (`00-tip-selftest-132.log`):

    TSUKUROI_CENSUS_SELFTEST: PASS (132 cases, 132 passed, 0 failed)          # 132 "PASS " lines
    PASS blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1) (exit 2, BLOCKED)
    PASS degraded: 4002 update candidates keep the names and the trap row (R42-C1) (exit 1, DEGRADED)
    PASS degraded: -Qu empty against a large -Sup keeps the disagree names (R42-C1) (exit 1, DEGRADED)
    PASS degraded: -Qu/-Sup count mismatch against a large -Sup keeps the disagree names (R42-C1) (exit 1, DEGRADED)

The four labels sit at `tools/tsukuroi-census.sh:2360,2567,2577,2584` (tip). Cross-check on case counts: the
base blob (`c8efaa3f`) with the same fixture harness reports 128 shipped cases (`03-f2-base-fixture-141.log`:
`129 cases` = 128 + my one added case), and 128 + 4 = 132, so tip adds exactly the four R42-C1 cases.

## 2. Single-site reverts, one at a time (shipped case set)

Method: nine scratch copies of the tip blob (`01-site-revert-diffs.txt` carries every diff); each copy restores
exactly one site's base text and nothing else. Line numbers are base → tip.

| # | site | base | tip | mutant | revert result (shipped cases) |
|---|------|------|-----|--------|-------------------------------|
| 1 | `-Qkk` error test + note (`printf\|grep -q`, `printf\|grep -m1`; now one awk assignment) | 692,694 | 697-700 | `m1_errorpair` | **FAIL** `blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1): exit 0 wanted 2` |
| 1a | test line only | 692 | 698 | `m1a_testonly` | **FAIL** same case, `exit 0 wanted 2` (wrong verdict: HEALTHY, not BLOCKED) |
| 1b | note line only | 694 | 700 | `m1b_noteonly` | **FAIL** same case, `exit 141 wanted 2` (killed in the assignment) |
| 2 | foreign-baseline lookup `bn=$(printf\|awk … exit)` | 740 | 746 | `m2_743` | **PASS 132/132** — survives; see §3 |
| 3 | `-Qu` candidate names `printf\|head -n3\|awk` | 1621 | 1627 | `m3_qu` | **FAIL** `degraded: 4002 update candidates …: exit 141 wanted 1` |
| 4 | `-Sup` names, `qu=empty` arm | 1635 | 1641-1642 | `m4_supempty` | **FAIL** `degraded: -Qu empty against a large -Sup …: exit 141 wanted 1` |
| 5 | `-Sup` names, count-mismatch arm | 1641 | 1647-1648 | `m5_mismatch` | **FAIL** `degraded: -Qu/-Sup count mismatch …: exit 141 wanted 1` |
| 6 | `-Suu` trap-row first line `printf\|head -n1` | 1652 | 1658 | `m6_suu` | **FAIL** `degraded: 4002 update candidates …: exit 141 wanted 1` |
| 7 | stub ABSENT evidence `printf\|grep -qE` → here-string | 2187 | 2193 | `m7_absent` | **PASS 132/132** — survives; see §4 |

Each mutant failure is exactly one case (`131 passed, 1 failed`), so no revert has collateral effects:
`10-*.log`.

Sites 1a and 1b are the two base lines the item counts separately; the pair is one awk statement at tip, so
1a also empties `$err_line` (the small-error case still passes because its expected text is the note prefix
`sample probe error`). 1b is the clean single-line proof that the *note* alone was an exit-141 source: the awk
test still fires BLOCKED, then `$(printf … | grep -m1 '^error:')` dies of SIGPIPE and takes the census with it.

**Which revert survives:** only #2 (`:743`) and #7 (the stub's ABSENT arm). #7 is selftest-stub code, not a
production probe, and no shipped case's census output reaches the 64 KiB pipe buffer, so its revert is silent —
but it is the same fail-open idiom the round fixed, i.e. the harness can still read "absent" falsely if a case
ever produces >64 KiB of output. #2 is the real finding.

## 3. `:743` fixture: base exit 141 vs tip completion

The shipped set has no case with a baseline beyond 64 KiB — `grep -n fbase` shows only `:2038` (`: > "$d/fbase"`),
the `r6base` 16-row snapshots (`:2290,2302,2308,2314,2610`), a 2-line file (`:2622`) and `fbase-absent`
(`:2320,2616`). I therefore added one case to two scratch copies (`05-fixture-harness-diff.txt`), one of the tip
blob and one of the base blob, driving the **production** `probe_packages` code through the selftest dispatcher:

- `$FX/pm` = `alpha-bin 1.0-1`, `beta-bin 2.0-1` (two `-Qm` rows; the first name is on baseline line 1);
- `$FX/fbase` = those two rows + 900 rows of `pad%05d 1.0-1 <120 chars>` = **122431 bytes, 902 lines** (> 64 KiB;
  `wc -c`/`wc -l` in `05-fixture-harness-diff.txt`); the 6000-short-row variant used for the stub probe is
  90031 bytes / 6002 lines;
- assertion: exit 1, verdict DEGRADED, evidence
  `foreign=2\(known=2 new=0 drift=0 gone=900\) base=file\(902\)`.

Observed:

- base blob + case (`03b-f2-base-fixture-141.log`):
  `FAIL f2-743: …: exit 141 wanted 1; output: tsukuroi-census census-v2 — host=fixture-host — … — read-only`
  (the run dies right after the header, inside `probe_packages`, before any plane line).
- tip blob + case (`02b-f2-tip-fixture-pass.log`): `PASS f2-743: … (exit 1, DEGRADED)`,
  `TSUKUROI_CENSUS_SELFTEST: PASS (133 cases, 133 passed, 0 failed)`.
- tip blob with **only** site #2 reverted, same case (`04-f2-743only-revert-141.log`):
  `FAIL f2-743: …: exit 141 wanted 1` — so the single restored `awk … exit` is sufficient to reproduce base's
  141, i.e. the site is load-bearing in isolation, independent of the four update-list sites.
- Full census lines from a debug copy of the tip blob (`F2-` lines, same fixture):
  `PLANE packages: DEGRADED (… foreign=2(known=2 new=0 drift=0 gone=900) base=file(902) gone=[pad00000 …])`,
  `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED … update-safety=DEGRADED oom=HEALTHY)`.

`known=2` is the positive control: both `-Qm` names were found in the 122 KB baseline, so the tip lookup really
scanned the large buffer rather than short-circuiting.

## 4. Defects

**D1 — uncovered site (verified).** Revert of `:743` alone is indistinguishable from tip by the shipped guard
(`10-m2_743.log`: `PASS (132 cases, 132 passed, 0 failed)`), while §3 shows the same revert restores exit 141 on a
>64 KiB baseline. A future edit re-introducing `| awk … exit` there ships green. Not claiming the C1 fix is wrong
— it is fixed and I measured it — only that the "two R42-C1 selftest cases" guard does not span this site.

**D2 — residual early readers in the harness (observed once).** `tools/tsukuroi-census.sh:2198` and `:2229`
(stub, must-match arm) and `:2178,2181,2183,2187` (gate arm) still run `printf '%s\n' "$out" | grep -q…` under
`set -euo pipefail` (`:1946` sets `set -uo pipefail` for the stub, the harness check body inherits `set -e` from
`:423`). With the 6000-row fixture (census output ≈ 56.5 KB) the *same* case produced:

- `30-stub-pipe-flake-FAIL.log:20` — `FAIL f2-743: …: plane evidence missing: 'foreign=2\(known=2 new=0 drift=0 gone=6000\) base=file\(6002\)'; got: PLANE packages: DEGRADED (… gone=6000) base=file(6002) …`
  — the regex demonstrably matches the printed line, yet the arm reported it missing;
- `31-stub-pipe-probe-PASS.log` — same case, same regex: `F2-PROBE out_bytes=56512 printf_rc=0 grep_rc=0 here_rc=0`;
- `32-stub-big-repeat-1..3.log` — three further runs, all `PASS (133 cases, 133 passed, 0 failed)`.

So 1 FAIL in 5 runs of an unchanged assertion. Direction is fail-closed (a good census reported as a failed
case; it cannot hide a regression), and no shipped case carries enough output to reach it, so today's
`PASS 132/132` is trustworthy — but the idiom, and the flake, remain. Mechanism [INFERENCE]: `grep -q` exits on
the first match and closes the pipe while `printf` is still writing, so the pipeline status is 141 and
`|| miss=…` fires; that is exactly what the round-42 comment at `:692-696` describes.

No other deviation: no package/service/sysfs/mount/boot change, no `btrfs scrub` verb, no lane write, no counter
run, no tool install or upgrade (nothing was missing).

## 5. What I did not do

- Did not run the frozen C1 counter `tools/score-size-invariance-r42.py` (not my item; the wave's count is the
  parent's).
- Did not run the census against the live host (fixture dispatcher only, by design of `--selftest`).
- Did not add any case to the lane: the `:743` fixture exists only in scratch copies; shipping it is the L1's call.
- Did not run the base/tip blobs' full selftest more than once per configuration except as tabulated; the tip
  `132/132` was observed once.

## 6. Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/w2/C1FinalSelftest/`
`00-tip-selftest-132.log`, `01-site-revert-diffs.txt`, `02*-f2-tip-*`, `03*-f2-base-141*`,
`04-f2-743only-revert-141.log`, `05-fixture-harness-diff.txt`, `10-<mutant>.log` (9 files),
`30-stub-pipe-flake-FAIL.log`, `31-stub-pipe-probe-PASS.log`, `32-stub-big-repeat-{1,2,3}.log`.
