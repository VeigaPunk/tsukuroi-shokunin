VERDICT: defect-found — write scope and mount containment hold cleanly; the frozen claim that the counter "remove[s] their
scratch on exit and on SIGINT/SIGTERM" (SCORECARD.md:2576; counter docstring :47) fails intermittently: 1 of 2 SIGINTs
delivered during the `--selftest` child left 91 entries / 220 KB of the run root behind. The C1 predicate itself is not
touched — both traced runs returned PASS with every conjunct.

# Seat C1-15 — security/scope review of `tools/score-size-invariance-r42.py`

Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (read-only for me). Counter under review:
`tools/score-size-invariance-r42.py`, sha256 `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03`
(= the frozen declaration hash; `git show 447662088dfd…:tools/score-size-invariance-r42.py | sha256sum` prints the same,
so the file I traced is byte-identical to the file at the implementation commit). Lane HEAD at my runs was
`87c4f7c627e377e5f6d361498e8db9b3886d7953` (controls commit on top of the declared tip `f50c28d8…`, which
`git merge-base --is-ancestor` confirms is its ancestor). I made no lane writes: `git status --porcelain -- tools/` is
empty and every `git` call traced below is `rev-parse --verify` / `show` (no `.git/*.lock` was ever created —
`grep -c 'index.lock\|config.lock' trace2` = 0).

Receipts: `.ufo/waves/round-42/w1/C1SentScope/` (this report's sibling directory; traces themselves stayed in
`/fast/scratch/hyaku/tsukuroi-r42/C1SentScope/` and are identified by sha256 + size + line count in
`receipts/traces.txt`).

## 1. What was run (three counter runs, never two at once)

Run 1 — the seat's command, verbatim filter set plus `unshare,clone,clone3,setns` so the mount namespace structure
could be reconstructed (the extra four only add visibility):

```
cd /fast/scratch/hyaku/tsukuroi-r42/C1SentScope && export TMPDIR=$PWD
strace -f -s 300 -e trace=openat,mkdir,unlink,rename,execve,mount,unshare,clone,clone3,setns \
  -o /fast/scratch/hyaku/tsukuroi-r42/C1SentScope/trace \
  python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-size-invariance-r42.py \
    --revision 447662088dfd3155e31aed239179a79c1d1046c7 \
    --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
    --scratch /fast/scratch/hyaku/tsukuroi-r42/C1SentScope/s
```

Observed: `rc=0`, 131 s wall, `trace` = 111812261 bytes / 635611 lines
(sha256 `b453866493acbf445ebdd030b1b176d3da07a580f058ea5fdbabca4f09d06f61`), and after exit
`ls -la …/s` shows `total 0` (only `.` and `..`). Verdict line (`receipts/counter-run1.txt`):
`{"cases": 10, "invariant": 10, "ns_invariant": 3, "selftest_pass": 1, "default_equal": 1, "verdict": "PASS",
"token": "00bae3689431", "selftest_label": "PASS (130 cases, 130 passed, 0 failed)"}`.

Run 2 — I had to repeat it with a complete write/mount filter, because the seat's list is blind to exactly the calls
that matter here: `openat,mkdir,unlink,rename` sees no `unlinkat`/`rmdir`/`renameat*` (what Python's `shutil.rmtree`,
`os.unlink` and coreutils `rm` actually use), and `mount` alone sees none of util-linux 2.4x's mount operations, which
go through the new mount API (`fsopen/fsconfig/fsmount/move_mount/open_tree`). Run 1 caught 6 `mount(2)` calls and
would have shown "no tmpfs, no bind mount at all"; run 2 caught all 48 mount-family calls:

```
strace -f -s 300 -e trace=open,openat,creat,mkdir,mkdirat,unlink,unlinkat,rmdir,rename,renameat,renameat2,\
symlink,symlinkat,link,linkat,chmod,fchmodat,chown,fchownat,truncate,ftruncate,utimensat,mount,umount2,\
unshare,setns,clone,clone3,execve,execveat,fsopen,fsconfig,fsmount,move_mount,open_tree,mount_setattr \
  -o …/trace2 python3 …/score-size-invariance-r42.py --revision 44766208… --lane …/tsukuroi-shokunin --scratch …/s2
```

Observed: `rc=0`, 98.7 s wall, `trace2` = 112059954 bytes / 648856 lines
(sha256 `cfe8dd3180b2bbd2ad398c9568d8da7940da126826c866a55da59bbdc770e108`), `s2` empty after exit, same PASS with a
new per-run token `fb376a9d3a0b` (`receipts/counter-run2.json`). Root cause of the difference, for the record:
`trace2` lines 65253-65257 show the helper doing `fsopen("tmpfs")/fsconfig/fsmount/move_mount(…, "/mnt", …)`, not
`mount("tmpfs", "/mnt", …)`.

Run 3 (three probes) — SIGINT (§5); counters were run strictly one at a time.

## 2. Every path written outside the scratch

Full table with returns: `receipts/writes-outside-run2.txt`. Scratch root of run 2 was
`/fast/scratch/hyaku/tsukuroi-r42/C1SentScope/s2/size-inv-r42.185qu6mk`. Grouping every write-ish syscall of trace2
(write-mode `open/openat/creat`, `mkdir(at)`, `unlink(at)`, `rmdir`, `rename(at,at2)`, `symlink(at)`, `link(at)`,
`chmod`, `chown`, `truncate`, `utimensat`) by path outside that root:

| count | syscall | path | what it is | effect |
|---|---|---|---|---|
| 11815 | openat | `/dev/null` | shell `2>/dev/null` redirects (`O_WRONLY`) | none |
| 4811 | openat | `/dev/tty` | failed probes, `= -1 ENXIO` (e.g. pid 3801846) | none |
| 1346 | mkdir | `/fast` | `mkdir -p` component walk, `= -1 EEXIST` | none |
| 60 | openat | `/etc/pacman.d/gnupg/trustdb.gpg` | real pacman keyring, `O_RDWR` `= -1 EACCES` (e.g. pid 3966691) | none (write refused) |
| 18 / 12 / 6 | openat | `/dev/nvidia0`, `/dev/nvidia-uvm`, `/dev/nvidiactl` | live `nvidia-smi` probe opening GPU nodes `O_RDWR` (fds 10/11/13, 11/13, 9) | device open only, no file mutation |
| 12 | mkdir | `/dev/nvidia-caps` | live `nvidia-smi`, `= -1 EEXIST` | none |
| 42 | chmod | `/dev/nvidia0` 18, `/dev/nvidiactl` 6, `/dev/nvidia-uvm` 6, `/dev/nvidia-caps/nvidia-cap{1,2}` 12 | nvidia-smi permission fixups, every one `= -1 EPERM` | none |
| 18 | openat | `/proc/self/uid_map`, `/proc/self/setgroups`, `/proc/self/gid_map` | the `unshare` process writing its own user-namespace maps | own process only |
| 6 | openat | `/proc/self/task/<tid>/comm` | thread naming by the process itself (fd 9 each) | own process only |
| 30 + 6 | openat/chmod | `/mnt/real-pacman`, `/mnt/pacman`, `/mnt/qq`, `/mnt/qkk`, `/mnt/qkk.rc` | writes into the tmpfs mounted over `/mnt` **inside** the private namespace | invisible to the host |
| 1 | mkdir | `/fast/scratch/hyaku/tsukuroi-r42/C1SentScope/s2` | the `--scratch` parent, `os.makedirs(parent)` :302 | the operator-named dir, left in place |

Negative results that matter (all verified over the whole trace, not sampled):

* **Zero** `unlink/unlinkat/rmdir/rename/renameat/renameat2/symlink/link/linkat/chown/truncate/utimensat` calls outside
  `--scratch`. The relative-path removals in the trace (`unlinkat(5, "pacman", 0)`, 447× `unlinkat(…, "memory.events")`,
  149× `"sync"`, …) are dirfd-relative children of `rm -rf -- <absolute scratch path>` (trace2 line 633618:
  `execve("/usr/bin/rm", ["rm","-rf","--","/fast/…/tmp-selftest/tsukuroi-r3-2-selftest.sL0pF2"])`) and of
  `mkdir -p <absolute scratch path>`; every one resolves inside the run root.
* **Zero** write-mode opens under `/home/vgpnk/Projects` (lane repo, fleet repo) or `/home/vgpnk/` (`~/.local`, `~/.omp`).
  The only reads of the lane are git objects / `.git/config` / `packed-refs`.
* `/usr/bin/pacman` is still the packaged binary after the runs (`sha256 590759eddb4c0cac6c5ad66f0f9bc093e15529675c0aa909eea396af5b07459d`,
  `pacman -Qo` → `pacman 7.1.0.r9.g54d9411-3`), `/proc/self/mounts` has no `/mnt` entry and no `tsk` mount
  (`receipts/host-integrity.txt`), and no `/tmp/size-inv-r42.*` or `/tmp/tsukuroi-r3-2-selftest.*` exists.

So the frozen write-scope claim holds for this counter: nothing outside `--scratch` is created, modified or deleted,
and the only outside writes are the null device, the process's own `/proc/self` entries, the namespace's tmpfs, and the
`--scratch` directory the caller named.

## 3. Every mount — all 48 inside the user namespace

Full list with issuing pid and namespace tag: `receipts/mounts-run2.txt`. Structure repeats identically in all six
`unshare -rm` legs (N1, N3, N6 × 2 twins):

```
pid 3953018 [SELF] unshare(CLONE_NEWNS|CLONE_NEWUSER) = 0            (trace2)
pid 3953018 [SELF] mount("none", "/", NULL, MS_REC|MS_PRIVATE, NULL) = 0   ← after its own unshare
pid 3953037 [descendant of 3953018] fsopen("tmpfs") → fsconfig("source","tsk") → fsconfig(FSCONFIG_CMD_CREATE)
                                    → fsmount → move_mount(4, "", AT_FDCWD, "/mnt", MOVE_MOUNT_F_EMPTY_PATH) = 0
pid 3953329 [descendant of 3953018] open_tree("/mnt/pacman", OPEN_TREE_CLONE) = 3
                                    → move_mount(3, "", AT_FDCWD, "/usr/bin/pacman", MOVE_MOUNT_F_EMPTY_PATH) = 0
```

48 mount-family syscalls = 6 × (1 `mount` propagation fix + 1 tmpfs via the new API + 1 bind via
`open_tree`+`move_mount`), and **0** of them lacks the unshare as self or ancestor: `unshare` pids
`[3953018, 4001082, 4044400, 4095349, 4139934, 4174136]`, every mount-API pid is a child of one of them. `umount2` and
`setns` never appear. The propagation change (`MS_REC|MS_PRIVATE`) is issued by the same pid *after* its
`unshare(CLONE_NEWNS)`, so it cannot reach the host mount tree. The 30 `/mnt` writes and the 18 `/proc/self` user-namespace writes of §2 carry
the same ancestry (48/48 have the unshared pid as self or ancestor). Corroboration from outside the namespace:
after both runs the host mount table shows no `/mnt` mount and no `tsk` (`receipts/host-integrity.txt`).

## 4. Every execve

Run 2: **30895 successful execve calls, 60 distinct binaries** (`receipts/execs-run2.txt` has the list and the full
argv of every state-mutating command). Distinct binaries: `cat 8038, bash 4763, awk 4628, grep 2279,
<root>/tmp-selftest/…/bin/journalctl 1462, stat 1072, …/bin/pacman 962, head 893, …/bin/systemctl 861, sed 759,
find 663, mkdir 596, tr 486, tail 330, date 307, env 283, <root>/rig/bin/journalctl 264, sha256sum 259,
<root>/rig/bin/pacman 168, chmod 165, cut 155, <root>/rig/bin/systemctl 154, …/bin/dmesg 129, …/bin/nvidia-smi 122,
…/bin/lsmod 122, …/bin/expac 118, …/bin/pacman-conf 117, sort 78, gpg 74, paste 72, gpgconf 64, wc 55, journalctl 54,
pacman 42, vercmp 38, /mnt/real-pacman 30, gpgsm 24, <root>/rig/bin/dmesg 22, …/bin/nvidia-smi 22, …/bin/lsmod 22,
…/bin/expac 22, …/bin/pacman-conf 14, mount 12, systemctl 12, ln 12, id 8, python3 7, cp 7, unshare 6, sh 6, dmesg 6,
nvidia-smi 6, lsmod 6, expac 6, rm 4, git 3, touch 2, mv 2, mktemp 1, mkfifo 1`
(`<root>` = `/fast/scratch/hyaku/tsukuroi-r42/C1SentScope/s2/size-inv-r42.185qu6mk`; the `…/bin/*` dispatchers are the
fixture stubs, and they answer from `$TSUKUROI_FIXTURE` only).

Mutating-command argv, complete audit (`receipts/execs-run2.txt`, section `argv of every successful exec of a command
that can mutate state`):

* `rm` — 4 calls, all `-f <abs scratch path>` or `-rf -- <abs scratch path>`; `mv` 2, `touch -d @<epoch>` 2, `ln -s` 12,
  `chmod` 165, `cp` 7, `mkdir -p` 596: every target is under `<root>`.
* `mount` — only `mount -t tmpfs tsk /mnt` (6) and `mount --bind /mnt/pacman /usr/bin/pacman` (6), all inside the
  namespaces of §3. `unshare` 6 × `-rm`.
* `pacman` — the census's own read-only query set only: `-Qq`, `-Qkk <sample>`, `-Qm`, `-Qu`, `-Sup --print-format`,
  `-Suu --print-format`, `-Q`, `-Sl`. No `-S`, no `-Sy`, no `-U`, no `-R`, no `--dbpath` override, no `pacman-key`.
* `systemctl` — live host calls are exactly `--user is-system-running --no-pager` (6) and `is-active graphical.target
  --no-pager` (6); everything else goes to the fixture stub. No `start/stop/enable/disable/restart/daemon-reload`.
* read-only live probes only: `journalctl` 54, `dmesg` 6, `lsmod` 6, `expac` 6, `nvidia-smi 6` (+ the GPU-node
  `O_RDWR` opens of §2, which are driver queries, not mutations; systemd normally creates those nodes, and nvidia-smi's
  `chmod` fixups all failed EPERM).
* `git` — 3 calls, exactly `-C <lane> rev-parse --verify 44766208…^{commit}`, `-C <lane> show c8efaa3a…:tools/tsukuroi-census.sh`,
  `-C <lane> show 44766208…:tools/tsukuroi-census.sh`. No `add/commit/checkout/reset/stash/push/worktree/remote`.
* No `sudo`, `su`, `btrfs`, `mkfs*`, `modprobe`, `hostnamectl`, `timedatectl`, `pacman-key`, `dd`, `shred`, `tee`,
  `install`, `systemd-*`, and no `kill`/`pkill` binary was ever executed.

**Low-severity trust-boundary note (not a defect against the frozen claim, but a review finding).** The counter and the
fixtures resolve their own helpers through the caller's `PATH`, not a fixed one:
`env_for` :103 uses `os.environ.get('PATH', '/usr/bin:/bin')`, the fixture builder is exec'd as `bash` (:243), children
are started as `bash` (:251), `_cleanup` shells out to `chmod` (:68), the selftest keeps the same `PATH` (:352), and
`git` is resolved by name (`subprocess.run(['git', …])`). trace2 shows the resulting search order, including
user-writable directories, before the packaged binaries: `execve("/home/vgpnk/.local/bin/git")`,
`execve("/home/vgpnk/.local/share/mise/shims/git")`, `execve("/run/user/1000/fnm_multishells/…/bin/bash")`,
`/home/vgpnk/.local/bin/bash`, … and only then `/usr/bin/git` (`= 0`) / `/usr/bin/bash`. Today no shadow exists, but a
planted `git`/`bash`/`chmod` on `PATH` would execute inside the counter and could substitute the census source that
`git show` returns — i.e. a verdict-minting surface outside the counter's own write scope. The namespace legs already do
the right thing (`env = {'PATH': '/usr/bin:/bin', …}`, :280). Smallest fix: use the same fixed `PATH` in `env_for`
(:103) and `st_env` (:352), and name `/usr/bin/git`, `/usr/bin/chmod` (or `os.chmod`-based cleanup) absolutely.

## 5. Scratch removal — success yes, SIGINT sometimes

* **On success: removed.** After run 1 `ls -la …/s` → `total 0`; after run 2 `ls -la …/s2` → `total 4` with only `.`
  and `..` (`ls -A` empty), i.e. the run root is gone and only the `--scratch` directory itself remains (created at :302
  and deliberately left). Both runs exit 0.
* **On SIGINT at ~20 s (the seat's probe): removed.** `receipts/sigint-20s.txt`. At the trigger the tree held 16 MB
  (`…/s/size-inv-r42.kk5vu9iw/{rig,ns,base-census.sh,rev-census.sh}`); `ns/` is created only after the ten fixture
  cases (:333-335), so the one live child (`860087`) was a namespace leg, not a fixture case (inference from the tree —
  the probe recorded the child pid, not its argv). `kill -INT <counter pid>` → `counter_exit=130` inside the 20 s
  window, the run root gone (only the empty `--scratch/s` left), child `860087` gone at exit, no orphan, stdout empty
  (the JSON verdict is only printed at the end, so an interrupted run emits no partial verdict line — good for a
  scorer).
* **On SIGINT during `--selftest`: removed 1 of 2 times.** `receipts/sigint-selftest-1.txt` (leak) and
  `receipts/sigint-selftest-2.txt` (the same script, clean). The probe waits for the counter's child to be
  `bash …/rev-census.sh --selftest`, then sends SIGINT to the
  counter's own pid. Leak run: trigger `2026-10-26T16:48:36`, counter exit 130 after **102 ms**, and the run root
  `size-inv-r42.2ae6f581` survived with **91 entries / 220 KB** under `tmp-selftest/tsukuroi-r3-2-selftest.Q9zCiY/fx/…`,
  whose mtimes (`…:36.7368304`–`…:36.7438303`) are *after* the trigger. Repeat run: `scratch root present=0 entries in
  s=0`, exit 130 in 102 ms. So the deletion races the still-running child; it is not a systematic failure, and it has no
  host effect — the leak stays inside the operator's `--scratch`.

Mechanism (this is the part I would fix):

1. `_sig` (:73-75) calls `_cleanup()` **first** and then `sys.exit(128 + signum)`; `_cleanup` (:66-70) chmods and
   `shutil.rmtree(..., ignore_errors=True)` the run root, then does `_SCRATCH.clear()`.
2. The SIGINT arrives while the main thread is blocked in `subprocess.run(['bash', rev_c, '--selftest'], …)`
   (:356) — i.e. the child that owns `tmp-selftest/` is still alive and creating fixture directories.
3. Because `_sig` raises `SystemExit` (not `KeyboardInterrupt`), `Popen.__exit__`
   (`/usr/lib/python3.14/subprocess.py:1105-1130`) closes the pipes and, in the `else` branch, calls `self.wait()` —
   an unbounded wait for that child, *after* its directory has already been deleted. (The special-cased fast path
   `exc_type == KeyboardInterrupt` that returns after `_sigint_wait_secs` is not taken here.)
4. `_SCRATCH.clear()` has already run, so the `finally: _cleanup()` at :378 cannot retry once the child has exited:
   anything the child created between `rmtree` and its own death stays forever. That is exactly the 91 surviving
   entries, and it is why the surviving root's mtimes postdate the trigger.

Two related consequences of the same design (not measured, marked as inference): the counter never signals its
children itself, so an interrupted census that does not die quickly (fixture run ≤ 300 s at :251, namespace leg ≤ 900 s
at :283, selftest ≤ 1800 s at :356) would keep the counter alive in `self.wait()` for that long with the scratch already
gone; and a child that outlives its removed cwd keeps burning CPU with no supervisor. In the selftest-phase probe the
counter exited 102 ms after the signal with the child already gone, so this is a latent, not an observed, hang.

### Smallest remediation (8 lines, no change to the predicate)

```python
_CUR = []                                    # Popen objects of blocking children

def _cleanup(*_):
    for d in list(_SCRATCH):
        subprocess.run(['chmod', '-R', 'u+rwx', '--', d], capture_output=True)
        shutil.rmtree(d, ignore_errors=True)
        if not os.path.exists(d):            # keep the path so `finally` can retry
            _SCRATCH.remove(d)

def _sig(signum, _frame):
    for p in _CUR:                           # stop the child that owns the tree ...
        try:
            os.killpg(p.pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            pass
    raise SystemExit(128 + signum)           # ... and let `Popen.__exit__` reap it;
                                             # `finally: _cleanup()` at :378 then removes the tree
```

with every child started as `subprocess.Popen(..., start_new_session=True)` (so `killpg` reaches the census's own
grandchildren, not just bash) and appended to `_CUR`. That makes the removal happen after the reap instead of racing it,
and keeps a partial tree registered for the second attempt. SIGTERM shares `_sig`, so it is fixed by the same edit; I
did not measure the SIGTERM path separately. `SIGHUP`/`SIGQUIT` are still unhandled and would lose the whole run root —
outside the declared claim, mentioned only for completeness.

## 6. Not done / limits of this seat

* No `SIGTERM` probe (same handler, not measured); no `SIGHUP`/`SIGQUIT` probe.
* No host mount-table snapshot taken *before* the traced runs; the post-run checks (`/mnt` unlisted, no `tsk`, packaged
  pacman intact, its sha256) are what I have. The namespace-containment proof itself is from the in-namespace ancestry.
* The K8 "cached-live" control variant, which makes a census write a replay cache under `$HOME`, is another seat's
  surface (`controls/`); I did not run it, so I can say nothing about writes on that code path.
* I reviewed the counter, not the census's own semantics; the census's correctness is C1Exec*/C1Crit* territory. Where a
  write in §2 came from the census (nvidia-smi, pacman keyring), I traced it but did not judge it.
* Counter runs: three (`--scratch s`, `--scratch s2`, and the 20 s SIGINT run), plus two selftest-phase SIGINT probes;
  never two at once. No packages installed or upgraded (strace 7.2 was already present), so nothing to record under the
  tooling authorization.
* Scratch `/fast/scratch/hyaku/tsukuroi-r42/C1SentScope/` removed at the end; receipts copied here first.
