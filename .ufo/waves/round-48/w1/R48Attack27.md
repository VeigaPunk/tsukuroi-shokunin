# R48Attack27 — adversarial C2 falsifier: descriptor collisions + `/proc/self/fd` target identity

**Verdict: KILLED on the claim's literal kill rule ("any case fails"); SURVIVED on every assigned
resolver axis** (descriptor collision, alias target identity, clobbering, wrong-root write,
`/tmp` fallback). The kill is **not** the R48-C2 resolver: it is a pre-existing false alarm in the
selftest's shared `host=fixture-host` gate that also fires on the alias-free `TMPDIR=/tmp` path.

**Status: advisory.** `.ufo/waves/round-48/frozen/FROZEN.md` ("Attempt 1's `w1` … is not part of
this record") voids this seat's wave, so this file is evidence for the counted `w2` wave, not a
score. It is written only because the bytes are now frozen and the finding changes what the frozen
C1 counter can be trusted to measure.

**Bytes under test (frozen):** `tools/tsukuroi-census.sh`
`sha256 375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`
(`.ufo/waves/round-48/frozen/census.sha256`; same digest in
`.ufo/waves/round-48/controls/battery-summary-r48-c1.jsonl` "K-pass: the fix revision").
Anchor commits: `ae99f021` (FREEZE), `23f85377` (w2 dispatch).
All probes ran on a scratch copy, `$HYAKU_SCRATCH/tsukuroi-r48/R48Attack27/frozen.sh`. The lane
working copy was never executed and never written (read-only git only).

## Axes

| axis | question |
|---|---|
| A descriptor collision | with fds already held (240–249, some or all, by dir/file/deleted-file/socket/pipe), does the resolver skip them or clobber one? |
| B target identity | does `/proc/self/fd/<n>` resolve to **exactly** the requested `$TMPDIR` — not `/tmp`, not a decoy — in the census process **and** in its children? |
| C isolation | under a spaced `TMPDIR`, does anything land under `/tmp` or outside `TMPDIR`? |
| D exhaustion | whole band held → fail closed, or silent `/tmp` fallback / wrong-root write? |
| E claim determinism | is `PASS (166 cases, 166 passed, 0 failed)` reproducible under the four frozen TMPDIR conditions? |

## Reproducible method

```sh
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tsukuroi-r48/R48Attack27; mkdir -p "$S"
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
    show ae99f021:tools/tsukuroi-census.sh > "$S/frozen.sh"
sha256sum "$S/frozen.sh"   # 375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426

# A. no clobber: hold markers on 240-244 across a full selftest
d="$S/c space"; mkdir -p "$d"; for n in 240 241 242 243 244; do printf 'MARKER-%s\n' "$n" > "$d/m$n"; done
TMPDIR="$d" bash -c 'for n in 240 241 242 243 244; do eval "exec $n<\"$1/m$n\""; done
  bash "$2" --selftest >/dev/null 2>&1; for n in 240 241 242 243 244; do
  printf "fd%s -> %s | %s\n" "$n" "$(readlink /proc/self/fd/$n)" "$(cat /proc/self/fd/$n)"; done' _ "$d" "$S/frozen.sh"

# A/D. resolver matrix: occupancy detection for dir, file, deleted file, socket, pipe; band held
#      (resolver verbatim: sed -n '/^selftest_base_dir() {/,/^}/p' "$S/frozen.sh")

# B. decoy dir held on 240; the alias must NOT be the decoy
w="$S/decoy"; mkdir -p "$w"; TMPDIR="$S/c space" bash -c 'exec 240<"$1"; exec bash "$2" --selftest' _ "$w" "$S/frozen.sh"
ls -A "$w"          # empty: no write into the caller-held target

# C. no /tmp fallback: /tmp read-only in a private namespace, code still sees TMPDIR=/tmp or a spaced dir
mkdir -p "$S/ro"
bwrap --dev-bind / / --dev /dev --proc /proc --ro-bind "$S/ro" /tmp \
  env TMPDIR="$S/c space" bash "$S/frozen.sh" --selftest | tail -1     # PASS 166/166
#    and: watcher during the run sees the tree inside TMPDIR, never under /tmp

# D. launcher consumes the whole band
TMPDIR="$S/c space" bash -c 'for f in 240 241 242 243 244 245 246 247 248 249; do eval "exec $f</dev/null"; done
  exec bash "$1" --selftest' _ "$S/frozen.sh"   # exit 1, explicit error, nothing written anywhere

# E. determinism under fleet load (this is the kill)
for i in $(seq 1 16); do f="$S/f$i"; mkdir -p "$f"
  ( bwrap --dev-bind / / --dev /dev --proc /proc --bind "$f" /tmp \
      env TMPDIR=/tmp bash "$S/frozen.sh" --selftest > "$S/out$i" 2>&1 ) & done; wait
grep -h '^FAIL' "$S"/out*          # 165/166 runs appear here at ~1-in-16
```

Host context for the determinism leg: load average 55–70, ~5 000 processes (70-seat round),
30 GB RAM with 10.7 GB available, no OOM kills in the ring. A private `/tmp` bind per run keeps the
real `/tmp` untouched while the code under test still sees `TMPDIR=/tmp`.

## Results

| case | observed | axis |
|---|---|---|
| four frozen TMPDIR conditions (unset / `/tmp` / under `$HYAKU_SCRATCH/tsukuroi-r48` / spaced) | `PASS (166 cases, 166 passed, 0 failed)` — every sequential run, 25+ repeats | E |
| same, 16 concurrent runs, `TMPDIR=/tmp` | **1 of 16 → `FAIL … hostname override not honoured`** (exit 1, 165/166) | E |
| same, 8 concurrent runs, `TMPDIR=/tmp` | **1 of 8 → 165/166** | E |
| same, 2 concurrent runs, spaced | **1 of 2 → 165/166** (pre-freeze working-copy blob, case D19) | E |
| fds 240–244 pre-held on marker files | markers byte-identical afterwards; fds still point at the markers; no reuse | A |
| fd 240 held on: dir / regular file / **deleted** file / socket / pipe | every case `[ -e /proc/self/fd/240 ]` → TRUE, resolver picked 241, holder untouched | A |
| fd 240 held on a **decoy** directory | alias = the requested TMPDIR; decoy left empty; selftest PASS 166/166 | B |
| whole band 240–249 held by a launcher | exit 1, `selftest: TMPDIR <…> cannot host the fixture tree (no /tmp fallback, R48-C2)`; no tree anywhere; `/tmp` delta empty | D |
| alias identity: spaced / symlinked / relative / trailing-slash TMPDIR | `readlink -f /proc/self/fd/240` == `readlink -f "$TMPDIR"` in every case; children inherit fd 240 and resolve it | B |
| physical landing, spaced TMPDIR, private `/tmp` | watcher (191 samples): tree **inside TMPDIR** = yes, under `/tmp` = never; private `/tmp` empty after the run; TMPDIR empty after the run | C |
| mktemp template actually used (`execve` trace) | `mktemp -d /proc/self/fd/240/tsukuroi-r3-2-selftest.XXXXXX` | B |
| `/tmp` remounted read-only in a namespace, spaced TMPDIR | PASS 166/166 (a `/tmp` fallback would have failed loudly) | C |

## Defect D1 — the kill: false-alarm `host=fixture-host` gate under fleet concurrency

Gate, frozen blob line 2362:

```sh
    elif ! printf '%s\n' "$out" | grep -q 'host=fixture-host'; then
      bad "$label: hostname override not honoured — possible host read"
```

Every `check` case (166 of them) passes through it, so a false alarm fails whichever case is running.
Observed failing cases: **D19** (PCI inventory), **D10** (user scope), **C5/S7-2** (swap anchors) —
case-independent, always exactly one case per run, always 165/166.

Decisive evidence that the child census is **correct** and the gate is **wrong**: the instrumented
copy (frozen blob + a dump of `$out` inside that branch) captured the C5 run's child output:

```
===== degraded: memory arm — swap-pressure anchors C5 (S7-2) rc=1 =====
tsukuroi-census census-v2 — host=fixture-host — 2026-10-28T12:07:16Z — read-only
PLANE packages: HEALTHY (… root_src=override root_dir=/tmp/tsukuroi-r3-2-selftest.guz1Ck/fx/degraded-mem-swap/root)
…
TSUKUROI_CENSUS: DEGRADED (packages=HEALTHY systemd=HEALTHY drivers=DEGRADED …)
```

The pattern the gate searches for **is present**, the rc is the wanted 1, the verdict is the wanted
DEGRADED — and the gate still returned non-zero.

Mechanisms ruled out (each measured, not argued):

- *hostname read failure* — refuted: the captured output carries `host=fixture-host`.
- *`printf | grep -q` SIGPIPE under `pipefail`* — real class in this script, but wrong size: with the
  captured value the pipeline failed 0/4 000 times; a synthetic sweep fails only past the pipe
  buffer (`≈65 KiB`: 2/10; `70 KiB`: 9/10; `200 KiB`: 10/10, raw rc 141, rc 0 without `pipefail`).
  Census output here is 2.6–9 KB.
- *fork/exec pressure visible in stderr* — none: the failing run's captured stderr has no
  `fork`/`cannot execute`/`Resource temporarily` line.
- *frequency* — gate-rc instrumentation (frozen blob + a logging wrapper around the same pipeline)
  logged **0 non-zero rc in 2 849 gate invocations** (one complete 16-way batch plus a second
  16-way batch still in flight when counted); the trigger is rarer than one in a thousand gate calls
  and reproduced only under multi-census concurrency.

Measured rate on the frozen blob: **3 false FAILs in ~109 selftest runs**, all of them in batches of
2, 8 and 16 concurrent selftests; **0 in 25+ sequential runs**, and 0 in a paired 6-vs-6 experiment
(alias-spaced vs clean TMPDIR, identical load).

**Why the integrator must care:** the frozen C1 counter `tools/score-selftest-tmpdir-r48.py`
(`sha256 8eead161…`) consumes exactly this line — it requires the literal
`TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)` and its predicate is
`pass_ok == 4 and loc_ok == 4 and clean_ok == 4 …`. Each of the four `pass_ok` legs carries this
false-alarm risk under fleet load, so the counter can report a **false C1 miss** with no defect in
the property it measures. The same gate is *not* reached by the C2 counter
(`check-scrub-admission-r48.py` parses seat reports), so C2's counted predicate is unaffected.

Fix direction (not implemented here — the seat is read-only): make the gate distinguish
"no match" from "the tooling failed", e.g. capture `printf … | grep -c` into a variable and assert
the count, or wrap the pipeline so a non-0/1 status (141/2/126) is reported as a *gate error* rather
than as a host read. A re-run policy in the counter is the cheap mitigation.

## Defect D2 — bounded band, hard failure on exhaustion (fail-closed limit)

With all of 240–249 held by a launcher, the selftest exits 1 with an explicit message and builds
nothing anywhere. Fail-closed, no `/tmp`, no wrong-root write — so no frozen C2 rule is violated,
but a 10-slot band with no retry converts an environmental descriptor into a hard operability
error. Recorded as a limit, not a kill.

## Defect D3 — the w1 claim's "frozen after-state" digest has no counterpart

The w1 claim text froze `sha256 4c94a17ae2a72f3dd538cfcbbff5cccb5dd2422b9a00a2f286c5e2b6d33044f4`
for "PASS (166 cases, 166 passed, 0 failed) under spaced TMPDIR". Measured on the frozen blob:

- last line with trailing newline → `dee269f13c2ed51c7c26d0b97659e5738e762f9f43c97407dbb02979b7f5f4a7`
- last line without trailing newline → `76a7ba9924d06ce77bdaa8bd0c41ef9866a2330008c6aa247db7658f6620da3b`
- full stdout, `TMPDIR` unset → `09d7e2455ca1c7777bc27d276ae9948c825160616cfc9ab4f29e922fba5ef0bd`
- full stdout, spaced `TMPDIR` → `90b1c1a769571577e038e0793c53e4c4fc5b916a5ed4c4f80d4b5d9d98c0b67d`

None equals `4c94a17a…`. `FROZEN.md` replaces the digest with a blob pin, which is consistent with
w1 being void — recorded so no later reader tries to "reproduce" a digest that never existed.

## Not established here

- The exact micro-trigger of D1 (which syscall returns non-zero in the gate under load) is not
  named: the gate's own rc was never captured non-zero in 1 843 logged invocations, and the failing
  run left no error text. What is established is that the child census was correct and the gate
  reported a false negative.
- Signal/interruption cleanup (SIGTERM/kill mid-run) is another seat's axis; this seat only measured
  clean-exit cleanup (TMPDIR empty, private `/tmp` empty after every PASS).
- Nothing was measured under `env -i`; the frozen C1 counter runs the selftest that way and would
  carry the same gate.

## Tooling

Nothing installed or upgraded (pacman paused host-wide; nothing was needed). Probes used bash,
`strace`, `bwrap`, `python3` — all already present.

## Scratch

All clones, fixture trees and private `/tmp` binds lived under
`$HYAKU_SCRATCH/tsukuroi-r48/R48Attack27/` and were removed before this yield (the one stray path
this seat created outside it, `$HYAKU_SCRATCH/tsukuroi-r48/fixt`, was removed too).

Real `/tmp` was written by exactly four legs — the `TMPDIR=/tmp` and `TMPDIR`‑unset conditions
themselves (`probe7` c1/c2, `frozenprobe` cond1/cond2) — because that is the condition under test:
the census creates its fixture tree in `/tmp` and removes it through its own `EXIT` trap. Every
twelve-way-or-wider replay used a private `bwrap` `/tmp` bind instead, so no load leg touched the
real `/tmp`. Residue seen in `/tmp` during this seat (`tsukuroi-r3-2-selftest.{Cj2Xcj,HTXztw,ORbPqj}`,
09:09–09:11) is **not attributable to this seat**: its mtimes are after this seat's last `/tmp` leg
and those trees belong to sibling seats' live runs. Left in place rather than deleted, since they
are not mine.
