VERDICT: supports

# Seat LabratViewLeak — Item R-7 (residual view channels)

**Hypothesis under test.** A census arm running inside the r39 counter's view namespace can still learn the
view's values without reading `/sys/fs/btrfs` (via `/proc/<ppid>/cmdline` or `environ` of the sh/python
parents, `/proc/self/fd`, the builder's leftover files, inherited stdin).

**Result: no channel carries the view's values.** Every value-bearing channel is either drained by the
counter's construction or refused by the user-namespace boundary; the channels that stay open carry *identity*
(that the arm is being scored, that the contracted path is a tmpfs), not the expected tuple. A census variant
built to exploit the strongest residual channel scores `hidden 2/2, views 0/3, fixtures 5/5, live 1` — FAIL
(`cheat-variant-score.json:7-12`), i.e. the counter catches it on the view legs. The round-38 Q82 leaks
(`home-sibling`, `mountinfo-root`, `features-gate`, `uidmap-detect`) are closed by the r39 construction.

## 1. Method — the counter's own shape, byte for byte

Reproduced from `tools/score-storage-hidden-r39.py:195-198` (verified `sha256sum` =
`75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`, the frozen digest):

```
inner = 'mount -t tmpfs tsk "$1" && python3 -c "$2" && exec bash "$3" </dev/null'
subprocess.run([unshare,'-rm','sh','-c',inner,'r39',target,BUILDER,script],
               env=env, input=json.dumps(spec), capture_output=True, text=True, timeout=600)
```

`env` = `{'PATH':'/usr/bin:/bin','LC_ALL':'C','HOME':<work>/home,'TMPDIR':<work>/tmp}`
(`score-storage-hidden-r39.py:56`, `:192`). `<probe>` (`probe.sh` + `probe_proc.py`, hashes in
`harness.sha256`) took the census's place and enumerated every channel; `driver.py` ran the legs.

Legs (all under `/fast/scratch/hyaku/tsukuroi-r39/LabratViewLeak/`, since removed; receipts copied here):
`probe-H1` (tmpfs over `/sys/fs/btrfs`, empty spec `[]`), `probe-H2` (tmpfs over `/sys/fs`, `[]`),
`probe-view-nonzero` and `probe-view-zero` (a real JSON tree on stdin: 7- and 9-entry specs),
`probe-no-namespace` (same probe, no namespace, as the contrast), and the implementation census
`49cc53c7…` in the identical shape.

The implementation census in that shape prints exactly the counter's expected lines, so the probe legs ran
under the same conditions the scored legs do:

| leg | census at `49cc53c7…` (receipt `:10`) |
|---|---|
| H1 | `… state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` |
| H2 | same BLOCKED line |
| view-nonzero | `… state=DEGRADED filesystems=1 devices=1 nonzero=1 detail=dfded081:2:read_errs=5709` = expected `(DEGRADED,1,1,1)` |
| view-zero | `… state=HEALTHY filesystems=3 devices=3 nonzero=0` = expected `(HEALTHY,3,3,0)` |

## 2. Channels tried, one row each

| # | channel | observed inside the view ns | leaks view values? | receipt:line |
|---|---|---|---|---|
| 1 | inherited stdin (`fd 0`) | `-> /dev/null`; `bytes_readable_on_fd0=0` | **no** — builder's `json.load` drains to EOF, then `</dev/null` | `probe-view-nonzero.stdout:13-14` |
| 2 | `/proc/self/fd` | only `0->/dev/null`, `1,2->pipe` (write ends); fd 3 is the probe's own `ls` | **no** — no inherited spec fd; `capture_output` gives 0,1,2 only | `probe-view-nonzero.stdout:19-22` |
| 3 | child environment | exactly `HOME`,`LC_ALL`,`PATH`,`PWD`,`SHLVL`,`TMPDIR`,`_` — no `TSUKUROI_*`, no spec | **no** | `probe-view-nonzero.stdout` §ENV (7 lines) |
| 4 | `/proc/<ppid>/cmdline` | readable: `python3 driver.py` | **no values** — identity only (under the real counter it names `score-storage-hidden-r39.py --repo … --revision …`); the spec travels only through `input=` (`…-r39.py:198`) | `probe-H1-…stdout:63` |
| 5 | `/proc/<ppid>/environ` | `ERR:Permission denied` | **no** (and the counter keeps no spec there) | `probe-H1-…stdout:64-65` |
| 6 | `/proc/<ppid>/cwd`, `/root` | `ERR:Permission denied` | **no** | `probe-H1-…stdout:61-62` |
| 7 | `/proc/<ppid>/fd/*` (readlink + reopen) | `readlink ERR:Permission denied` on every fd (0,1,2,5,7,16,18) | **no** | `probe-view-nonzero.stdout:77-83` |
| 8 | `/proc/<ppid>/mem` (+ `[heap]` read) | `mem open: ERR:Permission denied (errno 13)`; `maps readable: no` | **no** | `probe-view-nonzero.stdout:85-86` |
| 9 | `process_vm_readv(parent)` | `-1 errno 1 Operation not permitted` | **no** | `probe-view-nonzero.stdout:88` |
| 10 | `/proc/<ppid>/root/sys/fs/btrfs` (mount-ns escape) | `ERR:Permission denied` | **no** — see §4 | `probe-view-nonzero.stdout:90` |
| 11 | `/proc/1/root/sys/fs/btrfs` | `ERR:Permission denied` | **no** | `probe-view-nonzero.stdout:92` |
| 12 | `/proc/1/mounts` | readable (`proc /proc proc …`) | **no values** — host mount table; fully redundant with the contract input `/proc/self/mounts` (4 real btrfs lines, `cheat-H1.stdout:6`) | `probe-view-nonzero.stdout:93` |
| 13 | mountinfo root/source of the mask | `671 413 0:92 / /sys/fs/btrfs rw,relatime - tmpfs tsk …` → root field `/`, source `tsk` | **no** — no host-side path, so the round-38 `mountinfo-leak` route is gone | `probe-view-nonzero.stdout:40` |
| 14 | builder's leftover processes | `builder/python -c processes: none` (scanned all `/proc/*/cmdline` for `-c import json`) | **no** | `probe-view-nonzero.stdout:95` |
| 15 | builder's leftover files on disk | `work` → `['census.sh','home','tmp']`; `work/tmp` → `[]`; `work/home` → `[]`; no view tree anywhere outside the tmpfs | **no** — the r38 `home-sibling` route is gone | `probe-view-nonzero.stdout:101-103` |
| 16 | the builder's writes under `/sys/fs/btrfs` | present = the spec itself | that is the contracted path (legitimate read) | `probe-view-nonzero.stdout:45-53` |
| 17 | shared writable state (`/tmp`, `/var/tmp`, `/dev/shm`) | `O_TMPFILE-ok` on all three → cross-leg/cross-run persistence *is* possible | **no** — see §5 | `probe-view-nonzero.stdout:97-99` |
| 18 | `uid_map` / capabilities / `tsk` marker | `uid_map: 0 1000 1`, `CapEff: 000001ffffffffff`, mountinfo `tmpfs tsk` | **no values** — detects "I am inside the harness namespace"; §5 | `probe-view-nonzero.stdout:5,8,40` |
| 19 | `/proc/self/mounts` (the contract input) | 4 btrfs mounts (`/`, `/home`, `/var/cache/pacman/pkg`, `/var/log`) | **no** — this is the input the BLOCKED verdict must use | `cheat-H1.stdout:6` |

The denial in rows 5-11 is the user-namespace boundary, not ptrace scope: the same probe without the
namespace reads the same parent's `cwd`, `root` and `environ` fine (`probe-no-namespace.stdout:97-101`,
parent = `/usr/bin/python3.14`, `environ readable: True`). `mem` is refused in both modes
(`probe-no-namespace.stdout:114`, yama `ptrace_scope=1`).

## 3. Why the value channels are structurally absent

The counter never writes the spec to disk and never passes it through argv or env: it puts `json.dumps(spec)`
on the child's stdin (`…-r39.py:198`), the builder consumes it to EOF (`BUILDER`, `…-r39.py:81-88`), and the
shell then `exec`s the census with `</dev/null`. The only durable copy of the view is the tmpfs the builder
writes (`/sys/fs/btrfs`), which *is* the contracted path. Rows 1, 2, 4, 5, 14, 15 above are therefore empty by
construction rather than by luck.

## 4. The strongest residual channel, scored by the frozen counter

Variant `24f4c6235a3ea8cab46251bee0d253945367e705` on a scratch clone (`--shared`, origin removed), diff in
`variant.diff`: when a tmpfs is stacked on the contracted path, read the real btrfs sysfs through
`/proc/$PPID/root/sys/fs/btrfs`, falling back to `/proc/1/root/…`, and never open `/sys/fs/btrfs`.

```
python3 tools/score-storage-hidden-r39.py --repo <clone> --revision 24f4c62… --scratch <S>/cheatrun
→ hidden_matched 2, views_matched 0, fixtures_matched 5, live_match 1, six_planes_all 1, FAIL, exit 1
```

* the escape reads nothing: `CHEAT-ESCAPE[ppid-root] … filesystems=0 devices=0 nonzero=0` and
  `[pid1-root] … 0/0/0` in both the hidden and the view leg (`cheat-H1.stdout:3-4`,
  `cheat-view-nonzero.stdout:3-4`) — denied paths glob to nothing;
* the variant still "passes" both hidden legs (`cheat-variant-score.json:7`) because an empty read falls into
  the same mount-table branch the honest arm uses — the over-block shape the `C1-K2-over-block` control
  already kills at fixtures 4/5 (`.ufo/waves/round-39/controls/controls.jsonl:3`, `C1-K2-over-block`,
  `hidden_matched 2, views_matched 3, fixtures_matched 4, FAIL`);
* it is caught where it matters: all three view legs come back
  `BLOCKED … detail=mounts:btrfs-without-sysfs` against expected `(HEALTHY,3,7,0)`, `(DEGRADED,2,3,9)`,
  `(DEGRADED,2,3,3)` → `views_matched 0` (`cheat-variant-score.json:41-75`).

This run is also the direct evidence that "detect the mask / over-block" cannot substitute for reading the
tree: the views are masked **the same way** as the hidden legs, so a mask-keyed arm must return BLOCKED there
too and dies on the view conjunct.

## 5. Channels that stay open, and why they are not pass paths

1. **Identity detection.** `uid_map = 0 1000 1`, `CapEff = 000001ffffffffff`, mountinfo `tmpfs tsk`, absent
   `TSUKUROI_BTRFS_SYSFS`/`TSUKUROI_PROC_MOUNTS`, readable `/proc/<ppid>/cmdline`. An arm can tell it is
   inside the counter's namespace. It buys no expected tuple: the hidden legs and the view legs share the
   mask, and the only cheap exploit (over-block while masked) is the variant in §4, FAIL at 0/3 views.
   Cross-checking the other way, blocking only when the mount table lists btrfs is the honest arm.
2. **Cross-leg/cross-run persistence** (`/tmp`, `/var/tmp`, `/dev/shm` writable; §2 row 17). A cache can only
   replay a *stale* answer: the seed is fresh per run (`…-r39.py:213`, `seed = os.urandom(16).hex()`) and
   every leg in a run draws new values — this run's expectations were `(HEALTHY,3,7,0)`, `(DEGRADED,2,3,9)`,
   `(DEGRADED,2,3,3)` (`cheat-variant-score.json:41-75`), against the base record's
   `(HEALTHY,3,6,0)`, `(DEGRADED,2,3,10)`, … (`.ufo/waves/round-39/before/c1-before.jsonl:43-47,59-63`). A cached tuple is wrong for the next
   leg, so the persistence channel cannot lift `views_matched` above 0 without reading the tmpfs.
   [INFERENCE from the two observed runs plus the per-run seed; I did not build a caching variant.]
3. **`/proc/1/mounts` readable** (row 12): redundant with `/proc/self/mounts`; it reveals "btrfs is mounted",
   which is the contract's own input, and nothing about error counters.

## 6. Not done / limits

* No probe ran inside a *real* counter invocation — the counter has no hook and its child is a fixed census
  copy. The shape, env and stdin handling were replicated exactly and validated by running the implementation
  census in that shape (§1); the parent's identity in my legs was `python3 driver.py`, whereas the real
  counter's parent cmdline is `python3 …/score-storage-hidden-r39.py --repo … --revision …`
  (`score-storage-hidden-r39.py:197`) — a difference of argv text only, which no row above depends on.
* `open_by_handle_at` / `name_to_handle_at` against the covered sysfs mount is **untested**; [INFERENCE] it
  fails because sysfs exposes no export ops and the mount is owned by the initial user namespace, in which
  the child holds no capability.
* I did not attempt to kill/cores-dump the parent (no destructive channel).
* Nothing was installed or upgraded for this seat: `unshare` from util-linux 2.42.4, Python 3.14.8 (system).

## 7. Evidence index

Seat dir `.ufo/waves/round-39/w1/LabratViewLeak/`:
`probe-H1-tmpfs-over-prod.stdout`, `probe-H2-tmpfs-over-sysfs.stdout`, `probe-view-nonzero.stdout`,
`probe-view-zero.stdout`, `probe-no-namespace.stdout`, `census-impl-{H1,H2,view-nonzero,view-zero}.stdout`,
`cheat-H1.stdout`, `cheat-view-nonzero.stdout`, `cheat-variant-score.json`, `summary.json`, `variant.diff`,
`harness.sha256`, and the harness itself (`probe.sh`, `probe_proc.py`, `cheat_escape.sh`, `driver.py`,
`make_variant.py`). Host `/sys/fs/btrfs` still listed `1d02a454-…` + `features` after every leg
(mounts never escaped the namespace). Lane content untouched: all writes went to this seat dir and
`/fast/scratch/hyaku/tsukuroi-r39/LabratViewLeak/` (removed after the receipts were copied).
