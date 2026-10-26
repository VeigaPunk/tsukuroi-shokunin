VERDICT: supports

# C1-6 — live large sample (seat C1ExecLiveLarge, round 42, wave w1)

Host `plazir27` (linux 7.2.11-arch1-1), as user `vgpnk`, no sudo, read-only probes only.
`pacman v7.1.0 - libalpm v16.0.1`, `GNU bash 5.3.20`, 1,409 installed packages, pipe capacity
65,536 B (`fcntl F_GETPIPE_SZ` on a fresh pipe). Lane tip while measuring: `87c4f7c627e3…`
(unchanged; I ran the base/implementation sources extracted with `git show` into
`/fast/scratch/hyaku/tsukuroi-r42/C1ExecLiveLarge`, sha256 of both extracts in
`C1ExecLiveLarge/sizes.txt`). Receipts: `.ufo/waves/round-42/w1/C1ExecLiveLarge/` (sha256 in
`hashes.txt`).

## 1. Probe sizes — `pacman -Qkk $(pacman -Qq | head -n N)`, stdout+stderr merged

Command per row: `p=$(pacman -Qq | head -n $N); pacman -Qkk $p > req.$N 2>&1` (receipts
`req.8 req.50 req.200 req.600`, sizes table in `sizes.txt`):

| N | merged bytes | `^error:` lines | pacman rc |
|---|---|---|---|
| 8 | 617 | 0 | 1 |
| 50 | 2,819 | 0 | 1 |
| 200 | 13,608 | 0 | 1 |
| 600 | 32,538 | 0 | 1 |
| 1000 | 50,880 | 0 | 1 |
| 1200 | 61,994 | 0 | 1 |
| 1250 | 64,401 | 0 | 1 |
| 1409 (all) | 74,575 | 0 | 1 |

rc=1 on every row is pacman's "altered files" status (backup diffs), i.e. the code path the
census accepts (`base-census.sh:687`, rc 0|1). **No `^error:` line exists at any N up to the
full local DB.** At N=1268 the merged buffer splits 61,671 B stdout + 3,896 B stderr
(the `1password-*` GID/permission `warning:` lines; `split.1268.out`/`split.1268.err`).

Threshold bracket (binary search, `sizes.txt`, receipts `b.1267`, `min.1268`, `out.1409`):

- N=1267 → 65,530 B (below capacity)
- **N=1268 → 65,567 B (smallest N above the 64 KiB pipe capacity; 31 B over)**
- N=1409 → 74,575 B

Replay of the base's own buffer construction on the live host at `--sample 1268`
(`replay-1268.txt`):

```
cap_rc=1
s_out_bytes=65566
base_grep_q_rc=1
impl_herestring_rc=1
```

So the packages-plane buffer really does exceed the pipe capacity in the live code path at
--sample 1268; `base_grep_q_rc=1` says the base's `printf | grep -q '^error:'` found no match
(reads to EOF → correct branch on clean data).

## 2. Live census runs, base `c8efaa3…` vs implementation `4476620…`

Same host, same sample, base first (`run-live.sh`; raw stdout/stderr receipts
`s1268.{base,impl}.{out,err}`, `s1409.{base,impl}.{out,err}`):

| leg | base rc | impl rc | PLANE packages sha256 (both) | verdict |
|---|---|---|---|---|
| `--sample 1268` | 1 | 1 | `4b56bfc810646040…` | identical, DEGRADED |
| `--sample 1409` | 1 | 1 | `aa2685739c16fea5…` | identical, DEGRADED |

The packages PLANE lines are byte-identical at both sizes (15,856 B at 1268). Live content at
1268: `pacman -Qkk rc=1 sample=1268(…1268 names…) drift=42[1password-beta,1password-cli,amd-ucode,
asdcontrol,audit,cups,cups-browsed,cups-pdf,dbus,filesystem,fwupd,java-runtime-common,
libutempter,openssh,passim,power-profiles-daemon,shadow,sudo,systemd] backup_diffs=72
nonroot_artifacts=29`; at 1409: `sample=1409(…) drift=51[…] backup_diffs=97
nonroot_artifacts=37`. Whole-output diff is 2 hunks / 4 changed lines in both legs: the
timestamp line and the drivers PSI counters only (`C6_psi_some_avg300` 0.09→0.10 and neighbours).
`TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED
update-safety=DEGRADED oom=DEGRADED)` in all four runs.

Update-safety plane live buffers (the other three early readers, `-Qu` / `-Sup --print-format
'%r/%n %v'` / `-Suu --print-format '%r/%n %v'`): 136 B / 3 lines, 28 B / 1 line, 28 B / 1 line
— three orders of magnitude below the pipe capacity, and at 45 B per `-Qu` line the 64 KiB mark
would need ≈1,450 candidates [INFERENCE], more than the 1,409-package DB.

## 3. Does the base misreport live?

**No, not on the host's current probe data.** Every live sample from N=8 to N=1409 contains zero
`^error:` lines, so the base's `printf '%s\n' "$s_out" | grep -q '^error:'` reads the buffer to
EOF, returns 1, and the census takes the same path and prints the same packages PLANE line as
the implementation (evidence §2). The size precondition is only met when an operator asks for
`--sample 1268` or larger; the default (`SAMPLE_N=8`, `base-census.sh:451`) yields a 617 B buffer.

**The wrong-verdict arm does reach the live-sized buffer once an anchored error token exists**
(100 iterations each, `race.sh` → `race.txt`):

```
buffer=min.1268 bytes=65595 iterations=100 rc0(match->BLOCKED)=21 rc1(no-match)=0 rc141(SIGPIPE->wrong)=79 other=0
buffer=out.1409 bytes=74603 iterations=100 rc0(match->BLOCKED)=0  rc1(no-match)=0 rc141(SIGPIPE->wrong)=100 other=0
```

i.e. the base's row at `:692` reads the error as *not* an error in 79/100 runs at the minimal
live size and 100/100 at the full-sample size; the same buffer through the implementation's
here-string gives rc=0 → BLOCKED (`diag-min1268.txt`: `C_herestring_rc=0`). The assignment form
of the base's `:694` note kills its shell: `D_subshell_rc=141` (`diag-min1268.txt`). At the minimal
size only ~60 B of the write remain beyond the pipe capacity, which is why that race is partial
(21/100 still saw the token); at 74,603 B it is total (0/100).

## 4. Residual live finding — real pacman errors are not line-anchored (flag for L1, not a claim change)

A genuine probe error inside this buffer is **not** at line start once stderr is merged, so the
`^error:` test — base row and implementation row alike — does not see it. Command:
`pacman -Qkk $(pacman -Qq | head -n 1268) no-such-package-r42-probe 2>&1 | cat > pipeerr.1268`
(the shape of a package vanishing between `-Qq` and `-Qkk`, or any pacman diagnostic).

- `pipeerr.1268`: 65,624 B, 1,395 lines, `grep -c '^error:'` = **0**;
  `pipeerr.1268:1389` = `systemd-libs: 935 total error: package 'no-such-package-r42-probe' was not found`
  — the error text is spliced into the middle of a stdout line at a buffer-flush boundary.
- Three independent runs are byte-identical (`pipeerr.1268`, `rep1.1268`, `rep2.1268` all sha256
  `a4da8356…`), so this is deterministic, not a one-off.
- When the error is the only output it *is* anchored: `pacman -Qkk no-such-package-r42-probe 2>&1`
  → 57 B, `error: package 'no-such-package-r42-probe' was not found` (`tiny.err`).
- Replay of both readers on that buffer (`diag2-pipeerr.txt`):
  `BASE grep-q pipeline rc=1 -> verdict=NOT-BLOCKED`, `IMPL here-string rc=1 -> verdict=NOT-BLOCKED`.

Consequence: a real probe error in a large merged buffer is silently read as healthy by the base
(`c8efaa3`) **and** by the implementation (`4476620`); the R42-C1 fixture builds the token at line
start by construction (`impl-census.sh:2352-2358`, `blocked-sample-error-large`), so the frozen
counter does not exercise this shape. This is the same user-visible class as
R41-CENSUS-PIPEFAIL-692 ("an error line read as HEALTHY") via anchoring instead of SIGPIPE; it is
pre-existing, not introduced by the fix. Proposed one-line note for the L1's call (no claim
change proposed):

> R42-C1 residual: `probe_packages` merges pacman stderr into stdout (`cap` does `2>&1`) and
> anchors the error test at line start; a real pacman error inside a >64 KiB buffer can land
> mid-line (3/3 runs at `--sample 1268`, `pipeerr.1268:1389`), so both the old `grep -q` and the
> new here-string miss it — detect the token unanchored or capture stderr separately.

## 5. What I did not do

- Did not run the frozen C1 counter, the census `--selftest`, or any build/lint/test: wave-1
  editing is in flight and post-integration gates belong to the parent.
- Did not run more than one heavy probe at a time; no counter was run at all.
- No sudo, no host mutation, no mount outside `unshare`, no package/service/sysfs change; only
  read-only `pacman -Qkk/-Qu/-Sup/-Suu`, `pacman -V`, `wc`, `grep`, `diff`, `sha256sum`.
- No tool installs or upgrades (nothing was needed).
- Scratch `/fast/scratch/hyaku/tsukuroi-r42/C1ExecLiveLarge` removed after receipts were copied;
  no lane file touched (`git status --short -- .ufo/waves/round-42/w1/` shows the untracked seat
  dir only; lane HEAD still `87c4f7c627e3…`).
