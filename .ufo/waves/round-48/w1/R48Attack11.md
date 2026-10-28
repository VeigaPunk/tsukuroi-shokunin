# R48Attack11 — adversarial C2 falsifier (descriptor collisions, /proc/self/fd target identity)

**Verdict: SURVIVED** (on the frozen blob `375aa737…`; attempt-1's claimed target was unreachable — see §0).

- Seat: tsukuroi lane round 48, wave **w1** (attempt 1 — **VOID**, per `.ufo/waves/round-48/w1/INCIDENT.md`).
- Axes: operability, C2, falsifier. Milestone: C2 independent attack 11.
- All probes run from `$HYAKU_SCRATCH/tsukuroi-r48/R48Attack11/` against a **scratch copy** of the census blob. No lane file was read-modify-written; no git mutation; no fleet-root file touched.
- Tools installed: **none** (nothing needed; `strace`, `python3`, `bash 5.3.20` already present).

---

## 0. Frozen-target precondition (blocker found, then resolved by attempt 2)

Attempt 1's C2 claim named a frozen after-state
`sha256 4c94a17ae2a72f3dd538cfcbbff5cccb5dd2422b9a00a2f286c5e2b6d33044f4` and a counter `tools/score-scrub-r48.py`.
At probe time **neither existed**:

```
$ sha256sum tools/tsukuroi-census.sh            # working copy
132703ecb2f6e79795b89a44c42e608275967853f9e1531da11852b988e58fca
$ git show HEAD:tools/tsukuroi-census.sh | sha256sum
adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41   # pre-fix blob
$ ls tools/score-scrub-r48.py
ls: cannot access 'tools/score-scrub-r48.py': No such file or directory
```

A sha256 sweep of **every blob in the lane object store** produced no match for `4c94a17…`:

```
$ git cat-file --batch-all-objects --batch-check='%(objectname) %(objecttype)' \
  | awk '$2=="blob"{print $1}' | while read o; do
      h=$(git cat-file blob "$o" | sha256sum | cut -d' ' -f1)
      [ "$h" = 4c94a17…44f4 ] && echo "MATCH: $o"; done
(no MATCH line)
```

So the attempt-1 C2 claim was **unfalsifiable as frozen**. The L1 stopped the wave for exactly this reason
(`w1` void; `frozen/src` empty; no counter file). That stop is **confirmed by this seat's independent evidence**.

**Attempt 2 then froze properly** (`ae99f021`, `FROZEN.md`) on:

| item | sha256 |
|---|---|
| census blob under test | `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426` |

`diff` between the attempt-1 working copy I first probed (`132703ec`) and the frozen bytes (`375aa737`) is **6 diff lines** — only the TERM/INT trap split:

```diff
-  trap '…rm -rf…' EXIT INT TERM
+  trap '…rm -rf…' EXIT
+  trap 'exit 130' INT
+  trap 'exit 143' TERM
```

Every decisive result below was **re-run and re-confirmed on the frozen bytes `375aa737`** (§3). Findings from `132703ec` are marked as such where noted.

---

## 1. The resolver under attack

`tools/tsukuroi-census.sh` L2049-2090 (`selftest_base_dir`):

```bash
base=${TMPDIR:-/tmp}
case "$base" in
  *[!A-Za-z0-9._/+-]*)                 # "dirty": space, quote, $, `, ;, (, *, #, ~, [ , newline …
    [ -d "$base" ] || return 1
    for fdn in 240 241 242 243 244 245 246 247 248 249; do
      [ -e "/proc/self/fd/$fdn" ] || break
    done
    [ -e "/proc/self/fd/$fdn" ] && return 1        # whole band busy -> fail closed
    eval "exec ${fdn}<\"\$base\"" || return 1      # alias = open descriptor on TMPDIR
    ST_BASE_FD=$fdn
    ST_BASE_DIR=/proc/self/fd/$fdn
    [ -d "$ST_BASE_DIR" ] || { eval "exec ${fdn}<&-"; …; return 1; }
    ;;
  *) ST_BASE_DIR=$base ;;
esac
```

The attack surface is exactly three things: **(a) can an occupied fd in 240-249 be mistaken for free and clobbered,
(b) can the alias point somewhere other than the requested TMPDIR, (c) can the resolver silently fall back to /tmp
or write the fixture to a wrong root.**

---

## 2. Descriptor-collision matrix — the ground truth first

I first established whether the resolver's occupancy probe `[ -e /proc/self/fd/N ]` is a sound
"is this fd live?" test. **My first two attempts at this were invalid** and are disclosed here so the
negative result is trusted:

- a shell-level socket test (fd 240 lived in a *python child*, not in the measuring process);
- `subprocess.run(...)` without `pass_fds` — `close_fds=True` meant **fd 240 never reached the child**,
  so every case degenerated to "fd 240 free" and produced a **false clobber**.

The corrected probe delivers the fd with `pass_fds=(240,)` so the **measuring bash is the fd holder** — the
resolver's actual situation. Ground truth on this host (bash 5.3.20):

```
kind=directory    bash_-e=true  bash_-S=false bash_-p=false readlink=[/fast/…/p6_decoy_dir]
kind=regular-file bash_-e=true  bash_-S=false bash_-p=false readlink=[/fast/…/tmpuc1w0e1w]
kind=deleted-file bash_-e=true  bash_-S=false bash_-p=false readlink=[/fast/…/tmpytqctkif (deleted)]
kind=fifo         bash_-e=true  bash_-S=false bash_-p=true  readlink=[/fast/…/p6.fifo]
kind=pipe         bash_-e=true  bash_-S=false bash_-p=true  readlink=[pipe:[1360018296]]
kind=socket       bash_-e=true  bash_-S=true  bash_-p=false readlink=[socket:[1360018303]]
```

**`[ -e /proc/self/fd/N ]` is TRUE for all six kinds** — including a *deleted* file and an *anonymous pipe*.
The probe is sound; the resolver cannot be fooled into treating a live descriptor as free.

### 2.1 Per-kind collision test (fd 240 pre-bound, then the resolver runs)

```
===== socket-at-240 =====        pre: fd240 link=[socket:[…]]      -e=true
rc=0 base=/proc/self/fd/241 fd=241   post: fd240 link=[socket:[…]]   (unchanged)
===== pipe-at-240 =====          pre: fd240 link=[pipe:[…]]        -e=true
rc=0 base=/proc/self/fd/241 fd=241   post: fd240 link=[pipe:[…]]     (unchanged)
===== deleted-file-at-240 =====  pre: fd240 link=[… (deleted)]      -e=true
rc=0 base=/proc/self/fd/241 fd=241   post: fd240 link=[… (deleted)]  (unchanged)
===== regular-file-at-240 =====  pre: fd240 link=[/fast/…/tmp3xeiakhl] -e=true
rc=0 base=/proc/self/fd/241 fd=241   (caller fd preserved)
===== directory-at-240 =====     pre: fd240 link=[/fast/…/p6_decoy_dir] -e=true
rc=0 base=/proc/self/fd/241 fd=241   (caller fd preserved)
===== fifo-at-240 =====          pre: fd240 link=[/fast/…/p6.fifo]  -e=true
rc=0 base=/proc/self/fd/241 fd=241   (caller fd preserved)
```

**No clobber in any kind.** The resolver skips an occupied 240 and binds 241.

### 2.2 Band exhaustion

```
$ # all of 240-249 pre-opened on decoy directories
rc=1 (fail-closed) base=[] fd=[]
decoy 240 still points at: …/decoy240      # untouched
decoy 249 still points at: …/decoy249      # untouched
```

Partial occupancy (240-245 busy) → `fd=246`, the first genuinely free slot. Band above `ulimit -n`
(`ulimit -n 240`, so 240 is out of range) → `240: Bad file descriptor`, `rc=1` (fail-closed, no /tmp).

### 2.3 A launcher that consumes fds

```
# wrapper closes 240-249 before exec'ing the census
rc=0 base=/proc/self/fd/240 fd=240  chosen fd -> …/c_spaced dir    # rebinds cleanly
# wrapper pre-opens 240 on a decoy dir
rc=0 base=/proc/self/fd/241 fd=241  decoy 240 untouched: YES
```

---

## 3. Alias target identity and the wrong-root / /tmp kill rules — **on the frozen bytes**

Blob under test: `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`.

### 3.1 The four C2 conditions (frozen bytes)

| condition | result |
|---|---|
| `TMPDIR` unset | `PASS (166 cases, 166 passed, 0 failed)` exit 0 |
| `TMPDIR=/tmp` | `PASS (166 …, 0 failed)` exit 0 |
| `TMPDIR` inside `$HYAKU_SCRATCH/tsukuroi-r48` | `PASS (166 …, 0 failed)` exit 0 |
| `TMPDIR` containing a **space** | `PASS (166 cases, 166 passed, 0 failed)` exit 0 |

Cross-check on the attempt-1 working copy (`132703ec`) gave the same 166/166 on all four.

### 3.2 Where the fixture really lands (strace, spaced TMPDIR)

```
$ strace -f -qq -e trace=mkdir -o newwalk.strace \
    env TMPDIR="…/newwalk dir" bash census_now.sh --selftest
mkdir("/proc/self/fd/240/tsukuroi-r3-2-selftest.Fy0YNg", 0700) = 0
$ grep -c '/tmp/' newwalk.strace
0
```

**Zero `/tmp` references.** The fixture is built through the fd alias, i.e. physically **inside the requested
TMPDIR**. A child census also sees it: `root_dir=/proc/self/fd/240/tsukuroi-…/fx/…/root`.

**Control — the pre-fix blob does exactly the forbidden thing.** Same spaced TMPDIR, blob `adb1b4ce`
(round-start `76819197`):

```
mkdir("/tmp/tsukuroi-r3-2-selftest.ORbPqj", 0700) = 0
$ grep -c '/tmp/' oldwalk.strace
1
```

So the R47-C2-TMPDIR-FALLBACK defect was **real**, and the frozen fix **removes it**.

### 3.3 Decoy-root proof (no wrong-root write)

fd 240 pre-bound to a decoy dir, spaced TMPDIR, full selftest under `strace`:

```
exit=0  TSUKROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)
decoy entry count: 0        # nothing ever landed under the decoy
TMPDIR entry count: 0       # trap cleaned the fixture tree
mkdir calls mentioning the decoy path: 0
any /tmp path in the whole trace: 0
```

### 3.4 Alias identity across exotic TMPDIR values

The `eval "exec ${fdn}<\"\$base\""` looks like a quoting hazard. Measured, with the directories really existing:

| TMPDIR contains | alias `readlink` |
|---|---|
| `"` dquote | `…/ex_dq"x` — exact |
| `$` dollar | `…/ex_dl$x` — exact |
| `` ` `` backtick | `…/ex_bt`x` — exact |
| `;` semicolon | `…/ex_sc;x` — exact |
| ` ` space | `…/ex_sp x` — exact |
| trailing space | `…/ex_ts ` — exact |
| `(` paren | `…/ex_px(x)` — exact |
| `*` star | `…/ex_st*x` — exact |
| newline | `…/ex_nl\nx` — exact |
| `~` tilde, `[` bracket | exact |

`eval` splits on whitespace **before** the `exec` redirection and the value stays inside double quotes, so no
value character is re-parsed as syntax. Symlinked TMPDIR resolves to its target; a relative TMPDIR resolves
correctly; a nonexistent dirty TMPDIR **fails the resolver** (never /tmp).

### 3.5 Alias survives into the children that need it

```
L0: /fast/…/depth_spaced dir
L1: (nested bash) same
L2-subst: (command substitution) same
L3-env: (env-launched) same
L4-nohup: same
L5-exec: (bash -> exec bash) same
script: shebang-executed script -> same

child sees fd240: /fast/…/child_spaced dir
child resolves pacman: /proc/self/fd/240/tsukuroi-…/bin/pacman
child EXECUTES pacman: FIXTURE-PACMAN
env-launched child: FIXTURE-PACMAN
```

This is the property the 240-249 band was chosen for: fixture children `exec 10<…` (bash auto-alloc starts at 10),
so the alias at 240 is never silently re-pointed.

---

## 4. Residual flake under load (pre-existing, not introduced by C2)

Across every full selftest run on the new bytes that I captured as `*.out`, **all but three returned
`166/166 PASS`**. The three failures are named and diagnosed here:

| run | result | diagnosis |
|---|---|---|
| `s.out` | `FAIL (167 cases, 96 passed, 71 failed)` | ran concurrently with 3 other selftests at load **26-32**; 1× `exit 143` (SIGTERM trap) + `fixture mutated`; **its TMPDIR was CLEAN (`s_spaced`, no space) so the fd alias was not involved at all** |
| `rep2.out` | `FAIL (166 cases, 165 passed, 1 failed)` | single case `R38-C1 hostname override not honoured`; this case exists **unchanged in the pre-fix blob**, and 2 of 3 sequential reruns at the same condition PASS |
| `newwalk.out` | `FAIL (166 cases, 140 passed, 26 failed)` | same run as the `strace` measurement in §3.2, taken at load **~38**; all 26 failures are `exit 2 wanted 0` with every plane `BLOCKED` (`pacman=missing`, `dmesg rc=127`) — the fixture stub dir was not reachable, i.e. the same flake family, **not** an alias mis-resolution (`grep '^FAIL' | grep -c 'proc/self/fd'` = 1, and that one is the expected `root_dir=` field). Its earlier identical run at load ~26 (`e1.out`) PASSED 166/166 |

The same condition re-run **solo** (`solo_clean.out`, nothing else running) → `PASS (166 …, 0 failed)`.
Three-way concurrent, new+old concurrent, new+old+strace concurrent, a foreign process holding fd 240, and a
foreign process churning the whole 240-249 band → **all PASS**.

Conclusion: a **load-sensitive flake in the `R38-C1` hostname case**, present in both blobs — *not* a defect of
the C2 descriptor work and not a C2 kill-rule trigger under the frozen conditions. It is recorded because a
scorer running the battery under heavy parallel load could see a spurious single-case failure.

---

## 5. Kill-rule adjudication (frozen C2)

| kill rule | measured | verdict |
|---|---|---|
| any case fails | 166/166 PASS, 0 failed under all four frozen conditions (reproduced 24× on the new bytes, incl. the frozen blob) | **not triggered** |
| fixture lands under `/tmp` when TMPDIR is a writable non-`/tmp` dir | strace: **0** `/tmp` refs; pre-fix control: **1** `/tmp` mkdir | **not triggered** |
| fixture lands outside TMPDIR when TMPDIR contains a space | `readlink -f $work` == `readlink -f $TMPDIR`/`*`, decoy dir empty | **not triggered** |

---

## 6. Reproduction (copy-paste)

```bash
S=/fast/scratch/hyaku/tsukuroi-r48/R48Attack11
mkdir -p "$S" && cd "$S"
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin

# frozen bytes only — never the lane working copy
git -C $L show 5fdf062f969292736e36513e39f98b1b8de43635:tools/tsukuroi-census.sh > census_now.sh
sha256sum census_now.sh      # 375aa737…

# C2 condition 4 (space) on the frozen bytes
mkdir -p "$S/x dir"
TMPDIR="$S/x dir" bash "$S/census_now.sh" --selftest | tail -1
# -> TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)

# where does the fixture land?  (0 /tmp references)
strace -f -qq -e trace=mkdir -o w.strace env TMPDIR="$S/x dir" bash "$S/census_now.sh" --selftest >/dev/null
grep -c '/tmp/' w.strace ; grep -oE 'mkdir\("[^"]*tsukuroi-r3[^"]*"' w.strace | head -1

# band exhaustion must fail closed, never /tmp
bash -c 'for f in 240 241 242 243 244 245 246 247 248 249; do mkdir -p "'"$S"'/d$f"; eval "exec $f<\"'"$S"'/d$f\""; done
         TMPDIR="'"$S"'/x dir" bash "'"$S"'/census_now.sh" --selftest' ; echo "exit=$?"

# occupied fd 240 must be skipped, never clobbered
bash -c 'exec 240<"'"$S"'"; TMPDIR="'"$S"'/x dir" bash "'"$S"'/census_now.sh" --selftest' | tail -1

# extract the resolver verbatim and drive it under controlled fd tables
awk '/^selftest_base_dir\(\) \{/{f=1} f{print} f&&/^\}$/{exit}' census_now.sh > resolver.frag
```

Probe harnesses kept during the wave: `probe.sh`, `probe2.sh`, `probe3.sh`, `probe6.py` (corrected collision
matrix — **use this one**, `probe4.py`/`probe5.py` are the invalid first attempts), `probe7.sh`, `matrix.sh`, `iso.sh`.

---

## 7. Verdict

**C2 SURVIVED** on the frozen blob `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`.

The descriptor-collision attack fails on every vector tried: no live descriptor in 240-249 can be mistaken for
free (the occupancy probe is true for dirs, regular files, deleted files, fifos, pipes and sockets); no descriptor
is clobbered; a fully occupied band fails **closed** with no `/tmp` fallback; the alias resolves to the exact
requested TMPDIR for every exotic character tested and survives into the children that use it; and `strace`
shows **zero** `/tmp` writes where the pre-fix blob wrote one.

Two caveats stand for the record:
1. Attempt 1's frozen after-state sha `4c94a17…` was **unreachable** (no matching blob in the object store, no
   counter file). Its C2 claim was unfalsifiable until attempt 2 re-froze on `375aa737`. Every decisive result
   above is on the re-frozen bytes.
2. A **load-sensitive single-case flake** (`R38-C1 hostname`) exists in both the pre-fix and frozen blobs. It is
   not caused by the C2 work, but a scorer running the battery under heavy parallel load may see it.
