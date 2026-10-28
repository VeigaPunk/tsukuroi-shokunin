VERDICT: supports

# C1-X7 — kill rule: live census output unchanged by the R48-C2 selftest fix

Item: run the census LIVE (no `--selftest`), read-only, under the default driver-like
environment for BOTH bytes, and show the live output and exit code are unchanged.

Answer: **unchanged.** Six live runs under `env -i PATH=/usr/bin:/bin LC_ALL=C` (base ×3,
fix ×3) produce byte-identical output after digit-stripping (0 diff lines in every pair,
including base↔fix), the same 11 `PLANE|HANDOFF|DRIFT|STORAGE|SCRUB` lines, the same
`TSUKUROI_CENSUS:` verdict line and exit code 2 (BLOCKED) in all six. Neither file creates
a file anywhere in live mode (`strace -f` of both: zero syscalls naming `/tmp` or
`tsukuroi-r3`, the only `mkdir` being the pre-existing `/dev/nvidia-caps` probe, `EEXIST`).

## 0. Bytes under test (read from the frozen revisions, not the working tree)

```
$ cd /fast/scratch/hyaku/tsukuroi-r48/TExecLiveKill
$ git -C .../tsukuroi-shokunin show 5fdf062f...:tools/tsukuroi-census.sh > base.sh   # 3644 lines
$ git -C .../tsukuroi-shokunin show ae99f021...:tools/tsukuroi-census.sh > fix.sh    # 3718 lines
adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41  base.sh   (rev 5fdf062f)
375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426  fix.sh    (rev ae99f021)
```
`fix.sh` sha256 equals the C1 frozen blob `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`
declared in the round claim — the live-run bytes are the frozen bytes.
Receipts: `TExecLiveKill/base.sh`, `TExecLiveKill/fix.sh`, `TExecLiveKill/sha256` (in the `.out`
hashes below).

## 1. Primary measurement — six live runs, driver-like env

Command shape (one per run, timed with `date +%s%N`; stdout/stderr/exit captured separately):

```
env -i PATH=/usr/bin:/bin LC_ALL=C bash {base,fix}.sh > <run>.out 2> <run>.err; echo $? > <run>.exit
```

| run | file | exit | stdout lines | stderr bytes | wall |
|---|---|---|---|---|---|
| base.1 | base.sh | 2 | 13 | 0 | 5273 ms |
| base.2 | base.sh | 2 | 13 | 0 | 4986 ms |
| base.3 | base.sh | 2 | 13 | 0 | (run with fix.3, same batch) |
| fix.1 | fix.sh | 2 | 13 | 0 | 5047 ms |
| fix.2 | fix.sh | 2 | 13 | 0 | 5070 ms |
| fix.3 | fix.sh | 2 | 13 | 0 | (same batch) |

Exit 2 is the frozen exit map's BLOCKED rollup — `fix.sh:3714` `BLOCKED)  exit 2 ;;`
(`base.sh:3640` identical) — because `systemctl --user` is unusable under `env -i` (no
`DBUS_SESSION_BUS_ADDRESS`): output line 3 is
`PLANE systemd: BLOCKED (systemctl --user unusable rc=1 [Failed to connect to user scope bus ...])`.
That is host/environment, identical in both bytes, and is the pre-existing live verdict on
this host, not an effect of the fix.

Verdict line, identical in all six (`grep '^TSUKUROI_CENSUS:'`):
```
TSUKUROI_CENSUS: BLOCKED (packages=DEGRADED systemd=BLOCKED drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)
```
Plane-line count per run (`grep -cE '^(PLANE|HANDOFF|DRIFT|STORAGE|SCRUB) '`): **11** for
base.1 and fix.1 (6 PLANE + 2 HANDOFF + 1 DRIFT + 1 STORAGE + 1 SCRUB).

## 2. Digit-stripped diffs (the item's comparison)

`sed -E 's/[0-9]+/#/g'` on each output, then `diff`:

| pair | diff lines |
|---|---|
| base.1 vs base.2 (noise floor) | **0** |
| fix.1 vs fix.2 (noise floor) | **0** |
| base.1 vs fix.1 | **0** |
| base.2 vs fix.2 | **0** |
| base.3 vs fix.3 | **0** |

Receipts: `TExecLiveKill/d.base-noise.diff`, `d.fix-noise.diff`, `d.cross1.diff`,
`d.cross2.diff`, `d.cross3.diff` (all zero bytes), plus `base.{1,2,3}.strip`,
`fix.{1,2,3}.strip`.

## 3. Noise floor at full (unstripped) resolution

The only differences between two runs of the SAME file are the timestamp and the drivers
memory counters — exactly the fields the item anticipated:

```
$ diff base.1.out base.2.out
1c1  tsukuroi-census census-v2 — host=plazir27 — 2026-10-28T11:58:24Z ...  vs  ...T11:58:37Z
4c4  PLANE drivers: ... C5_pswp=9823643/16311784 ... C6_psi_full_total_us=291075196 C6_avail_kb=12928044 C6_shmem_kb=7324
       vs              ... C5_pswp=9823847/16311784 ... C6_psi_full_total_us=291078451 C6_avail_kb=13092184 C6_shmem_kb=7320
```
`base.3` vs `fix.3` unstripped differs on line 1 (timestamp) and line 4 (the same C5/C6
memory fields) only — nothing else, so the base↔fix comparison is noise-free at
digit-stripped granularity with a measured noise floor of those two lines.

## 4. Live mode creates no files (before/after + syscall proof)

Scratch listing before the first run vs after all runs (`before.ls` / `after.ls`): the only
new entries are my own captured artifacts (`*.out`, `*.err`, `*.exit`, `*.strip`, `*.diff`,
traces, marker); no census-created path.

Decisive check — `strace -f` over the whole process tree of each live run
(`-e trace=mkdir,mkdirat,openat,creat,unlink,unlinkat,rename,renameat,renameat2`):

```
base: total_trace=15605  mkdir_lines=2  tsukuroi_hits=0  tmp_path_hits=0   exit 2
fix:  total_trace=15623  mkdir_lines=2  tsukuroi_hits=0  tmp_path_hits=0   exit 2
$ grep -hE '"/tmp/|tsukuroi-r3' tr.base tr.fix      -> (empty)
$ grep -hE 'mkdir\(' tr.base                        -> mkdir("/dev/nvidia-caps", 0755) = -1 EEXIST (pre-existing nvidia probe)
```
Non-`/dev` write-opens in both traces are only `/etc/pacman.d/gnupg/trustdb.gpg` opened
`O_RDWR` and refused `EACCES` (pacman's own read-only probe path), and the traced outputs
reproduce the earlier runs digit-for-digit (`base.trace.out == base.1.out`,
`fix.trace.out == fix.1.out`). Receipts: `TExecLiveKill/tr.base`, `tr.fix`.

`find /tmp -maxdepth 1 -newer <marker> -name 'tsukuroi*'` DID list directories during the
window (e.g. `/tmp/tsukuroi-r3-2-selftest.iK8UzB`, born 09:00:03 -0300). These are **not
mine**: my traces contain no `/tmp` path and no `tsukuroi-r3` string at all, while 49
concurrent sibling `--selftest` processes were live in the same window (saved snapshot
`TExecLiveKill/ps.snapshot.txt`, e.g. `bash /fast/scratch/hyaku/tsukuroi-r48/R48FalsFdAlias/census-post.sh --selftest`,
`TExecBaseControl/w/census-under-test.sh --selftest`, `TExecStrace/census.sh --selftest`).
Those seats' selftests legitimately build under `/tmp` when TMPDIR is unset (C1's first case).

## 5. Isolation cross-check with a private `/tmp` (bwrap) — and why it is not the primary env

```
bwrap --unshare-user --unshare-pid --die-with-parent --dev-bind / / --tmpfs /tmp \
      bash -c 'env -i PATH=/usr/bin:/bin LC_ALL=C bash {base,fix}.sh; ls -A /tmp'
base: rc=2  tmp_entries=0        fix: rc=2  tmp_entries=0
base.bwrap vs fix.bwrap (digit-stripped): 0 diff lines
```
Both bytes leave the private `/tmp` completely empty (0 entries) and agree with each other.
But this environment perturbs the packages plane for BOTH files identically —
`drift=2[1password-beta,1password-cli]` outside vs `drift=1403[...]` inside — because
`pacman -Qkk` under the user namespace reports UID/GID mismatches on package-DB files and
directories:

```
$ pacman -Qkk <the 8 sampled names>    outside: 12 lines, rc=1
  warning: 1password-beta: /opt/1Password/1Password-BrowserSupport (GID mismatch)
$ (same inside bwrap)                  inside: 2816 lines, rc=1
  warning: 1password-beta: /var/lib/pacman/local/1password-beta-8.12.42_34.BETA-1/install (UID mismatch)
  warning: 1password-beta: /opt (UID mismatch)
```
(`qkk.outside`, `qkk.inside`; `id -u` inside the namespace is still 1000, so this is the
userns UID/GID view, not privilege.) So bwrap is *not* a driver-like environment and was
used only as a write-isolation cross-check; the primary comparison in §1–§2 is the plain
`env -i` run.

## 6. Static corroboration (why the live path cannot have changed)

`diff -u base.sh fix.sh` has exactly 4 hunks, and every non-comment added line falls inside
the selftest machinery:

```
@@ -408,9   +408,9    header comment (TMPDIR wording)          fix.sh:411-413
@@ -599,8   +599,9    usage text (--selftest description)      fix.sh:602-604
@@ -2045,21 +2046,69  selftest_base_dir() (new) + run_selftest head
                      fix.sh:2058-2091 (function), 2092 run_selftest, 2106 work=$(mktemp ...),
                      2110 trap 'exit 130' INT, 2111 trap 'exit 143' TERM
@@ -3481,6 +3530,31  new R48-C2 selftest cases           fix.sh:3533-3559
```
`selftest_base_dir` call sites in `fix.sh`: 2101 (`run_selftest`), 3540 and 3550 (the two new
selftest cases) — and its definition at 2058. Nothing in the live planes (687-2047) or in
`main()` (3612-3644) is added, removed or modified; the only `TMPDIR` reads in the file are
inside `selftest_base_dir` (2074) and the selftest case block, so live mode never consults
`TMPDIR` at all.

## 7. What I did not do

- Did not run `--selftest` (not this item; the C1 counter seats own it) and did not run any
  counter, so this report makes no claim about the 166-case selftest verdict.
- Did not run the bwrap shape as the primary environment (see §5).
- No git/jj mutation anywhere; all git access was `git -C <lane> show <rev>:<path>`.
- Tooling: nothing installed (no pacman, no uv/npx); used only host `bash`, `strace`,
  `bwrap`, `pacman`, `sha256sum`, `find`.

## 8. Residual risk

The live verdict on this host is BLOCKED/exit 2 for both bytes, so the kill rule is
demonstrated for the BLOCKED rollup path only; a HEALTHY-path live run was not reachable in
this environment (systemd --user unusable under `env -i`). The digit-stripped equality covers
all 11 plane lines and the verdict composition, which is the whole live surface; no
plane-specific branch was left unexercised except the ones the host itself blocks.

Receipts directory: `.ufo/waves/round-48/w2/TExecLiveKill/` (41 files, 3.6 MB).
Scratch `/fast/scratch/hyaku/tsukuroi-r48/TExecLiveKill/` removed at exit.
