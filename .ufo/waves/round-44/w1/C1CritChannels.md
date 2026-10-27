VERDICT: defect-found

# C1-12 — observation channels of `score-scrub-arm-r44.py` (N/W legs vs production)

Reviewed: `tools/score-scrub-arm-r44.py` (frozen, sha256 `1409a5fd…`) legs `INNER`/`make_cases`/`materialize`/`expect`/`live_model`/`wired_check`; `tools/tsukuroi-census.sh` `probe_scrub_record`; round-44 controls (`run_controls_c1.py`, `C1-K*.jsonl`, `battery-summary-c1.jsonl`) against QUALITY 82, 85, 87, 90. Empirical channel probe reproduced the N-leg namespace exactly (same `unshare --map-*` maps, same `setpriv --reuid=1000 --regid=1000 --clear-groups`, same tmpfs sources `r44lib`/`r44view`, same cwd `/mnt/home`, same cleaned env): receipt `.ufo/waves/round-44/w1/C1CritChannels/ns-capture.txt` (sha256 `a21a79a1…`), driver `inner2.py` beside it.

## 1. Channel inventory (census-under-test can tell N/W from production)

| Channel | State | Evidence |
|---|---|---|
| Override environment (`TSUKUROI_*`, `UFO_*`, `TMPDIR`) | **closed** | `clean_env()` drops all (`score-scrub-arm-r44.py:179-180`); same dict fed to INNER, L leg and selftest. Control K2 (env-gated on `TSUKUROI_SCRUB_DIR`) FAILs: `correct=1` (`battery-summary-c1.jsonl`). |
| Process identity — numeric uid/euid/gid | **closed** | `setpriv --reuid=1000 --regid=1000 --clear-groups` (`INNER` :97, spec uid/gid :564); `/proc/self/status` `Uid/Gid 1000 1000 1000 1000` inside the leg (`ns-capture.txt`), identical to host. `identity_ok=1` in every receipt. Control K3 (uid-gated `id -u = 0`) FAILs (`correct=1`). |
| Process identity — supplementary groups | **open, not declared** | Leg runs `--clear-groups`; `/proc/self/status` `Groups:` is empty and `id -G` prints only `1000` (`ns-capture.txt`). Host caller has `Groups: 967 992 998 1000` (`/proc/self/status`). Live leg has no setpriv (`score-scrub-arm-r44.py:597`), so it carries the full group set. The docstring's "process identity (caller uid/gid, no groups)" (:47-48) labels this closed — the groups half is open. |
| cwd / `$PWD` | **open, not declared** | N/W run with `cwd='/mnt/home'` (`INNER` :143); `pwd` = `/mnt/home`, `PWD=/mnt/home` while `HOME=/home/vgpnk` (skew) (`ns-capture.txt`). Live leg runs with `cwd=work` (scratch). Both `getcwd()` and `$PWD` differ. |
| stdin | **open, not declared** | N/W census children inherit the spec pipe; `read` returns EOF instantly (`ns-capture.txt`: "stdin: EOF-or-empty"). Live leg inherits the counter's stdin (tty/pipe with data). |
| Mount table (`/proc/self/mountinfo`) | **open, declared** | Four extra tmpfs mounts over `/mnt`, `/sys/fs/btrfs`, `/var/lib`, `/etc/systemd/system` with sources `r44lib`/`r44view` and `uid=1000,gid=1000` options (`ns-capture.txt`). Control K7 (gate on tmpfs-on-`/var/lib`, `run_controls_c1.py:80`) scores `correct=16, wired=1, live=1` — the watcher fires in N/W and not in live; recorded as the declared limit (`battery-summary-c1.jsonl`; `SCORECARD.md:2766-2767`). |
| uid_map / gid_map | **open, declared** | Leg shows `0 1000 1 | 1 100000 65535` (`ns-capture.txt`); production shows `0 0 4294967295`. **No control arm exists at it** (K0–K13 contain none; only K2 env, K3 uid-numeric, K7 mount, K10 live-fsid-negative). |
| Script path (`$0`, `$BASH_SOURCE`) | **open, declared** | N: lib sourced as `/mnt/census-lib.sh` (`CALL` :80); W: `bash /mnt/census.sh` (:152); L: `bash <scratch>/census.sh` (:597). `$0`/`$BASH_SOURCE` reveal each (`ns-capture.txt`: `argv0=bash` for the N `-c` form). No control arm. |
| statfs / fs type of scored roots | **open, not declared** | Inside leg all four roots are `tmpfs`; host reports `btrfs` on `/var/lib`, `/etc/systemd/system`, `/mnt` and `sysfs` on `/sys/fs/btrfs` (`ns-capture.txt`; `stat -f -c %T`). Discoverable via `fstatfs(2)`; inherent to unprivileged namespaces (cannot mount btrfs/sysfs). |
| Process ancestry (ppid chain) | **open, not declared** | N/W census's parent is `python3 -c <INNER>`; live's parent is `score-scrub-arm-r44.py`. `ps -o cmd= -p $PPID` shows the driver (`ns-capture.txt`). Not closable without changing harness shape. |
| Namespace identity (`/proc/self/ns/{user,mnt}`) | **open, not declared** | Fresh inodes `user:[4026533760] mnt:[4026533764]` (`ns-capture.txt`); production runs in init namespaces (inode `4026531837`). Inherent to any user/mount-namespace test. |
| Fixture values (drawn) | **closed** | All case values drawn per run from `random.Random(os.urandom(16))` (:559): fsids, devids, counts, modes, speeds, names, kinds. Host fsids injected half the time (`make_cases` :353-361) so a "not-this-host's-fsid" gate cannot fire uniformly — control K10 FAILs with `correct=6` (`battery-summary-c1.jsonl`). |
| Fixture literals common to every fixture (`r44lib`, `r44view`, `/mnt`, `/mnt/home`) | **open, not declared** | Uniform across all 16 cases and W; `r44view`/`r44lib` appear verbatim in mountinfo, `/mnt*` in script path and cwd. No arm keys on any of them (see §3). |
| File owners of planted fixtures | **closed (presentationally)** | Fixtures are created as ns-root, which maps to the caller's host uid; inside the leg `stat` shows `uid=0 gid=0` (`ns-capture.txt`) — numerically identical to production (root-owned `/var/lib/btrfs`). The ns translation masks the host-side uid. |
| Timing | **not a usable channel** | The scored code has no clock/comparison probe; nothing in `probe_scrub_record` (:1967-2040) or the census main (:3374-3376) measures duration. No discriminator. |

The scored census itself consults none of the open channels (it uses only `[ -d/-r/-x/-f/-L/-S/-e ]`, globs, and reads `scrub_speed_max`; `tsukuroi-census.sh:1973-2033`); every open channel above is *readable* by a hostile variant, which is what QUALITY 90 requires the battery to cover.

## 2. Is the declaration's "named open" set complete? — No

`SCORECARD.md:2765-2767` and the counter's `channels_open` JSON list only `mount table`, `uid_map`, `script path /mnt/census-lib.sh` (:630). Missing open channels with evidence above: **supplementary groups** (identity family; docstring even asserts them closed), **cwd/`$PWD`**, **statfs/fs type**, **process ancestry**, **namespace-identity inodes**, **stdin state**, **N-leg argv shape** (`bash -c …`), and the **uniform fixture literals** (`r44lib`/`r44view`). File-owner channel is genuinely closed (ns uid 0 == root). The set should be extended or each unlisted channel explicitly reasoned away.

## 3. QUALITY 87 (b) — one-literal fixture-shape arm: **not covered**

The battery (`run_controls_c1.py:64-98`) contains no arm keyed on a literal common to every fixture. The closest, K7, is keyed on the *structural* fact "tmpfs on `/var/lib`" (:80), not on any literal; its `recorded` outcome already proves the mount-table family open. The strongest uniform literals (`r44view` in mountinfo; `/mnt*` in script path/cwd) are never varied across fixtures (infrastructure shape is constant; only per-case *values* are drawn), and no watcher on any of them exists. So the Q87(b) arm is absent; given the current counter, such an arm would score `correct=16` and be recorded-open exactly like K7 — the gap is that it is neither run nor recorded.

## 4. QUALITY mapping

- **82 (R32-FIXTURE-GATEABLE)**: live view present and read-only (L leg, `:594-605`; walks `SYS`/`DIR`/`WANTS` only, no writes). Live oracle is re-derived before/after each run with one retry (`:594-604`) — no caching in the counter. **However**, the pre-data control **cached-live variant** mandated by QUALITY 82 is absent: no `C1-K9.jsonl` exists and no arm in `run_controls_c1.py` simulates a counter that caches the live answer. The docstring's "pre-data controls" paragraph does not claim it, so this is a battery gap, not a docstring lie.
- **85 (R38-Q82-LEAK)**: satisfied on the leak axis — fixtures are built inside the child namespace before the scored code starts (`INNER` build before `run`), fed solely via stdin, and no host-resolvable name leads to the fixture content (tmpfs sources `r44lib`/`r44view` are labels; `/mnt` resolves host-side only to the empty host dir). The open channels are *detection* channels (Q90), not leaks.
- **87 (R39-CONTENT-UNREAD)**: (b) uncovered as above. (a) content-free-entry control is a C2-side concern; the C1 battery has no analogous "content-free" census arm, but the probe's reads are structural (no content semantics), so 87(a) is not applicable to C1.
- **90 (R42-OBSERVED-CHANNEL)**: the per-channel battery is incomplete. Present arms: env (K2), numeric uid (K3), mount-table structure (K7, recorded-open), live-fsid-negative fixture value (K10). Missing arms: **groups**, **uid_map**, **script path**, **fixed literal** (`r44view` etc.), **statfs**, **cwd**, **stdin**. The declaration only records K7 as the limit (`SCORECARD.md:2766-2767`), so the "named open" disclosure understates the open set (see §2).

## 5. Cheapest leg change that closes the largest open channel

The largest *closable* channel is **cwd/`$PWD`** (every N/W case displays `/mnt/home`; trivial to align). In `INNER`, `run()` already passes `cwd` — change the two `run(…, cwd='/mnt/home')` calls to use the host work directory (the namespace shares the host's mounts, so `$work` resolves identically inside), matching the live leg's cwd exactly, and additionally redirect `stdin` to `/dev/null` for every census child so N/W and live see the same stdin state. Proposed text for `INNER`:

```python
def run(cmd, timeout):
    try:
        p = subprocess.run(pre + ['bash', '-c', cmd], env=env, capture_output=True, text=True,
                           timeout=timeout, cwd=spec.get('cwd', '/mnt/home'))
        return p.stdout, p.returncode
    except subprocess.TimeoutExpired:
        return 'timeout', 124
```

with `spec['cwd'] = work` and `stdin=subprocess.DEVNULL` added to both `subprocess.run` calls in `INNER`. This closes two open channels for two lines. The remaining open channels fall into two classes and should be *declared* rather than fought: (a) inherently unclosable unprivileged — mount table (incl. statfs type), uid_map, namespace inodes, process ancestry, supplementary groups (host gids 967/992/998 are outside the subgid range and cannot be mapped); (b) closable later with more effort — script path (run the census from a path identical to the live one inside the ns) and uniform fixture literals (randomize the tmpfs source names per run, e.g. `r44lib`→a drawn word, and the `/mnt` home name). The `channels_open` JSON list and the scorecard paragraph should be extended accordingly.

## 6. Other observations

- K7's receipt: `expect=recorded`, verdict FAIL only because `selftest_pass=0` (the gate never fires under selftest, so the R44-C1 selftest cases emit CONST); `correct=16, wired=1, live=1` — the recorded-limit semantics is intact (`C1-K7.jsonl`).
- K10 (`live-fsid` watcher) `correct=6`: injection covers only ~half the cases; the drawn-value design is what stops it, not full masking — fine.
- Battery: `should_fail_accepted=0`, `control_accepted=1` (`battery-summary-c1.jsonl`).

## 7. Scope / method notes

- Read-only on the lane; no host mutation. The empirical probe ran only inside a private `unshare` user+mount namespace in scratch (replica of the counter's own maps); receipt under `.ufo/waves/round-44/w1/C1CritChannels/`. No tools installed (not needed). No subagents.
- Not run: the full counter/controls (already run; receipts read), and no live census execution beyond reading existing receipts.
