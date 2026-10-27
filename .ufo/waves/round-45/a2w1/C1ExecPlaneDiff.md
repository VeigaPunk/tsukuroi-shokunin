VERDICT: supports

# C1ExecPlaneDiff — item C1-4 (kill rule: PLANE/HANDOFF/DRIFT/STORAGE/SCRUB/TSUKUROI_CENSUS line shape and live exit code unchanged)

Kill rule tested: "a PLANE/HANDOFF/DRIFT/STORAGE/SCRUB/TSUKUROI_CENSUS line changes shape or the live
exit code changes base -> IMPL". Result: **no shape change, no exit-code change, no revision-induced
value change** across six live runs (base x3 / impl x3, alternating). The only body differences are
per-run host counters inside the drivers line, and every one of them also moves between two runs of
*one* revision, so they are live drift by the rule's own test.

## 1. What was run (exact commands)

```
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecPlaneDiff
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
git -C "$L" show 5bbd5ff588120fd8e7c744695351a6978b4241c1:tools/tsukuroi-census.sh > $S/fresh/census-base.sh
git -C "$L" show 18389f44cf6ce414d7be205998b29c79fb0b490c:tools/tsukuroi-census.sh > $S/fresh/census-impl.sh
chmod +x $S/fresh/census-{base,impl}.sh
TMPDIR=$S/fresh/tmp $S/fresh/run-alternating.sh          # b i b i b i, captures stdout, stderr, rc, time
```

Export hashes (seat copies, `sha256sum`):

| file | sha256 | bytes |
|---|---|---|
| `census-base.sh` (5bbd5ff5) | `17c82406fe7a7d06261b1fb2ac4be56e7d5498c6712ae90fe8233d2bb0e81a35` | 198 992 |
| `census-impl.sh` (18389f44) | `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc` | 202 665 |

The two exports differ in exactly 6 hunks (`rev-diff.txt`): the five production reader sites at base
lines 965 / 1003 / 1085 / 1460 / 1535 (`head -n1` assignment forms, e.g. base:965
`state=$(printf '%s\n' "$CAP_OUT" | head -n1 | tr -d '\r' | sed -E 's/[[:space:]]+$//')` -> impl:965
`state=${CAP_OUT%%$'\n'*}; state=${state//$'\r'/}; state=${state%"${state##*[![:space:]]}"}   # first line, no early reader (R45-C1)`)
plus one 44-line selftest block (impl 3332-3375, the six `(R45-C1)` cases). Nothing else changed in the
file, so any output delta is attributable to those sites or to the host.

## 2. Run matrix (`runlog.txt`, reproduced verbatim)

```
base run1 rc=2 dur_ms=2337 lines=13 bytes=7215 sha256=118084f2cf05b3b8d32d113f3bf32f6e3a8e4eed324f92822d9a0652ad590635
impl run1 rc=2 dur_ms=2331 lines=13 bytes=7215 sha256=9dd058e32e4a8475c3c19136bf7358b0a2adb937af13ee131128e7f59f37ee81
base run2 rc=2 dur_ms=2450 lines=13 bytes=7215 sha256=d764dbc4337e51db5efcf44cd88cc2178e1b776cc9349da741e6b9b19ba8cd95
impl run2 rc=2 dur_ms=2518 lines=13 bytes=7215 sha256=bc3cdbe467c200056b48bc54a2768680c8de67e32338cd0426f8df956319cae2
base run3 rc=2 dur_ms=2487 lines=13 bytes=7215 sha256=a043780537b04b021252169799217945661d9baef89f8a043ce3d6eaa4d414bc
impl run3 rc=2 dur_ms=2444 lines=13 bytes=7215 sha256=02e9e881f782b0a0f544fc6dffa18767b54367184e88420e9f3099813ccdb884
```

Run order and header timestamps (line 1, dropped before every diff): base-1 03:24:54Z, impl-1 03:24:56Z,
base-2 03:24:59Z, impl-2 03:25:01Z, base-3 03:25:04Z, impl-3 03:25:06Z. stderr was **0 bytes in all six
runs**; every run wrote its 13 lines / 7215 bytes and exited 2.

After dropping line 1: **12 lines / 7132 bytes in all six runs** (`body-*.out`). The full-file sha256
differs only because of the timestamp; that is why line 1 is normalised out, as the item specifies.

## 3. Shape check (prefix + key sequence, all six runs)

`analysis.py` -> `analysis.txt`; result line: `shape_or_revision_induced_problems: 0`.

* Line count identical (12) in all six.
* For every one of the 12 body lines the prefix (text before the first `(`) is identical across all six
  runs, and the ordered `key=` sequence is identical: 11 / 7 / 30 / 13 / 5 / 15 keys for the six PLANE
  lines, then `HANDOFF ADJ-04 … class=kill-events`, `HANDOFF ADJ-04 … class=coredumps` (6 keys each),
  `DRIFT pacnew-plane` (9), `STORAGE btrfs-device-stats` (4), `SCRUB btrfs-scrub-record` (9),
  `TSUKUROI_CENSUS:` (6). No line gained, lost or reordered a field; no line was added or removed.
* Rollup word and terms identical in all six: `TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED
  systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)`.

## 4. Diff of the bodies — only line 3, only C6 memory counters

Every pairwise comparison (`cmp` on `body-*.out`) reports exactly 2 changed lines = one removed + one
added = **line 3 (`PLANE drivers`) only**. The differing span is byte-identical in position: common
prefix 393 chars, common suffix 80 chars of a 549-char line; the span is
`…; C6_psi_some_avg300=A C6_psi_full_avg300=B C6_psi_full_total_us=C C6_avail_kb=D C6_shmem_kb=E; guards=…`.
Lines 1, 2, 4-12 (packages, systemd, journal, update-safety, oom, HANDOFF x2, DRIFT, STORAGE, SCRUB,
rollup) are byte-identical in all six runs.

Pasted diffs (`diff -U0`, long lines intact):

```
### intra-revision (same revision, live drift reference): body-base-1.out vs body-base-2.out
@@ -3 +3 @@
-PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=67 (oom=0 io=65 gpu=0 other=2) [unknown: accepted noise floor]; nvidia=present smi=615.78.08 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=0 C2_sysd_oom=0 C3_sigkill=1; C4_sweep=208 C4_present=0 C4_local=0; C5_swap_fail=495 C5_swap_peak_pct=57% C5_pswp=885225/2223211 C5_sock_throttled=85390; C6_psi_some_avg300=0.01 C6_psi_full_avg300=0.01 C6_psi_full_total_us=69612719 C6_avail_kb=20841044 C6_shmem_kb=31188; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
+PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=67 (oom=0 io=65 gpu=0 other=2) [unknown: accepted noise floor]; nvidia=present smi=615.78.08 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=0 C2_sysd_oom=0 C3_sigkill=1; C4_sweep=208 C4_present=0 C4_local=0; C5_swap_fail=495 C5_swap_peak_pct=57% C5_pswp=885225/2223211 C5_sock_throttled=85390; C6_psi_some_avg300=0.00 C6_psi_full_avg300=0.00 C6_psi_full_total_us=69612722 C6_avail_kb=20809968 C6_shmem_kb=30700; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)

### cross-revision: body-base-1.out vs body-impl-1.out
@@ -3 +3 @@
-PLANE drivers: DEGRADED (… C6_psi_some_avg300=0.01 C6_psi_full_avg300=0.01 C6_psi_full_total_us=69612719 C6_avail_kb=20841044 C6_shmem_kb=31188; …)
+PLANE drivers: DEGRADED (… C6_psi_some_avg300=0.00 C6_psi_full_avg300=0.00 C6_psi_full_total_us=69612720 C6_avail_kb=20838016 C6_shmem_kb=31188; …)

### cross-revision: body-base-2.out vs body-impl-2.out
@@ -3 +3 @@
-PLANE drivers: DEGRADED (… C6_psi_some_avg300=0.00 C6_psi_full_avg300=0.00 C6_psi_full_total_us=69612722 C6_avail_kb=20809968 C6_shmem_kb=30700; …)
+PLANE drivers: DEGRADED (… C6_psi_some_avg300=0.00 C6_psi_full_avg300=0.00 C6_psi_full_total_us=69623822 C6_avail_kb=20967484 C6_shmem_kb=30700; …)
```

(The `…` elisions above are the byte-identical 393-char prefix and 80-char suffix; the unabridged
`diff -U0` output for all eight pairs is in `compact-diffs.txt`, and the whole 549-char lines are in
`body-*.out`.)

Field-level table across all six runs (`compact-diffs.txt`):

| line | key | base b1,b2,b3 | impl i1,i2,i3 | verdict |
|---|---|---|---|---|
| 3 | `C6_psi_some_avg300` | 0.01, 0.00, 0.00 | 0.00, 0.00, 0.00 | live drift — recurs inside base (b1 vs b2) |
| 3 | `C6_psi_full_avg300` | 0.01, 0.00, 0.00 | 0.00, 0.00, 0.00 | live drift — recurs inside base |
| 3 | `C6_psi_full_total_us` | 69612719, 69612722, 69626721 | 69612720, 69623822, 69626722 | live drift — every run differs, also within each revision |
| 3 | `C6_avail_kb` | 20841044, 20809968, 20694700 | 20838016, 20967484, 20663424 | live drift — every run differs, also within each revision |
| 3 | `C6_shmem_kb` | 31188, 30700, 30700 | 31188, 30700, 30700 | live drift — recurs inside base *and* inside impl |

No key is constant within both revisions and different between them (`shape_or_revision_induced_problems: 0`).

## 5. Why the moving keys cannot be the five converted readers

The differing keys are the round-7 memory-pressure arm, read directly from procfs, not from a
`$CAP_OUT` pipeline: `census-impl.sh:1229` `avail=$(mem_field "$MEMINFO_FILE" MemAvailable)`,
`:1230` `shmem=$(mem_field "$MEMINFO_FILE" Shmem)`, `:1232` `read -r psi_s psi_f psi_t < <(awk … )` on
`PRESSURE_FILE=${TSUKUROI_PRESSURE_FILE:-/proc/pressure/memory}` (`:483`), assembled at `:1259`
(`MEM_NOTE=… C6_psi_some_avg300=$psi_s …`). The five converted sites at 965 / 1003 / 1085 / 1460 / 1535
feed `state`, timer `Result` `r`, `driver`, `t_word`, timer `ActiveState` `r` — all of which are
identical across the six runs (section 6). So the drift sits on a reader that C1 did not touch, and the
readers C1 did touch produced identical output.

Independent volatility check with the *same* binary: the two sensitivity-control runs in section 7 also
executed `census-impl.sh` (only the output was piped through `sed`), about 2 minutes after impl-3, and
returned `C6_avail_kb` 20838016 -> 19115660, `C6_shmem_kb` 31188 -> 84044, `C5_sock_throttled`
85390 -> 85515, `C6_psi_some_avg300` 0.00 -> 0.01. Same script, different numbers: those fields are
host-volatile.

Cross-time corroboration (earlier evidence for the same drift, not needed by the rule): the attempt-1
wave's leftovers in this seat's scratch (`/fast/scratch/hyaku/tsukuroi-r45/C1ExecPlaneDiff/prior-attempt1/`,
uploaded into this seat dir as `prior-now-base1.diff`) were produced at 02:53Z from the same two git
blobs (their exports hash to `17c824…` / `237b21…`, identical to mine, so the bytes are the same
revisions). Comparing their base-1 body with mine, 5 body lines moved in 31 minutes with *no* revision
change: journal `err=156 (coredump=88 …)` -> `err=159 (coredump=91 …)`, `HANDOFF … coredumps value=88` ->
`91`, oom window `2026-10-24..2026-10-26` -> `2026-10-24..2026-10-27`, drivers `C4_sweep=218` -> `208`.
That is the same failure mode as the C6 counters, on the same two revisions.

## 6. Per-site live equivalence (the five readers, observed on the live host)

Extracted from body lines 2-4 of every run — all six agree exactly:

| reader site (impl line) | field | value in all six runs |
|---|---|---|
| 965 `state` | `state=` | `running` |
| 1003 timer `Result` `r` | `timer_fail=` / `timer_unknown=` | `0` / `0` |
| 1085 `driver` (nvidia-smi first line, last comma field) | `smi=` | `615.78.08` |
| 1460 `t_word` (boot target) | `target=` | `graphical.target:active` |
| 1535 timer `ActiveState` `r` | `timer_drift=` / `timer_unknown=` | `0` / `0` |

The affected lines themselves, byte-identical across base and impl (base-1 = impl-1 = … = impl-3):

```
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=2 timers_scanned=2 timer_fail=0 timer_unknown=0)
PLANE journal: DEGRADED (boots=5 current=yes target=graphical.target:active err=159 (coredump=91 kernel=67 other=1); failedhist=0; timers_enabled=2 timers_scanned=2 armed=2 timer_drift=0 timer_unknown=0)
```

## 7. Exit code (unchanged) and detector sensitivity controls

Exit code: `2` in all six runs; rollup `TSUKUROI_CENSUS: BLOCKED`; the script's exit map is
`census-impl.sh:605` "0 HEALTHY | 1 DEGRADED | 2 BLOCKED (worst plane wins; usage errors also 2)" and
`:3481` `BLOCKED)  exit 2`. Same rollup word, same code, base and impl, every run. stderr empty in all six.

The method was not blind, as two controls show:

1. **Shape detector fires.** A mutant of the impl script whose output renamed two stable keys
   (`timer_drift=` -> `timer_driftX=`, plus `state=running` -> `state=run`) was run twice. The key-sequence
   check flagged line 4 (`{'timer_drift', 'timer_driftX'}`); the prefix check stayed equal. So a field
   rename *is* caught by the check that returned 0 above.
2. **Value classifier fires.** Fed a pair that differs constantly within each revision but across
   revisions (`state` running vs run; `timer_drift` 0 vs absent), the classifier printed
   `REVISION-INDUCED` for both. So the "every difference recurs within a revision" results in section 4
   are a live finding, not a default.

## 8. Secondary read-only cross-check (C1-3 owns the definitive proof)

Both revisions were also run live under
`strace -f -qq -e trace=openat,open,creat,mkdir,mkdirat,rename,renameat,unlink,unlinkat,link,symlink`
(`trace-base.log.gz`, `trace-impl.log.gz`): 365 write-mode/mutation calls each; the normalised sets are
27 lines each (`tset-base.txt`, `tset-impl.txt`) and differ **only** in `strace -f` `unfinished …>`
accounting on `/dev/null` (2 vs 3 unfinished, 16 vs 15 completed) — no path appears in impl that is
absent from base. The only *successful* filesystem-mutating call in either trace is
`openat("/proc/self/task/<pid>/comm", O_WRONLY|O_CREAT|O_TRUNC)` (the shell writing its own procfs comm
name, present identically in both). The `/dev/char/*` symlinks, `/dev/nvidia*` opens and
`/etc/pacman.d/gnupg/*` lock/trustdb opens all fail `EACCES`/`EEXIST` identically in both traces. The
`TMPDIR` I pointed the census at (`fresh/tmp/`) was empty after all runs — no temp file.

## 9. Limits — what I did not do

* The live outputs are small (7215 bytes total; each converted probe's captured output is one line), so
  the live runs never push a capture past the pipe buffer. What this item establishes is that the
  rewritten first-line readers return the same values, that every line keeps its shape, and that the exit
  code is unchanged on the live host; it does **not** itself demonstrate the exit-141 fix, which is the
  selftest's and the counter's job (C1-1/C1-2 seats).
* I did not run `tools/score-census-readers-r45.py`, the census selftest, or the predecessor counters —
  other seats' items. No C1 counter was run in this seat.
* Three rounds per revision, as specified; nothing was mutated: no git command, no host change, no lane
  file written. Scratch was `rm -rf`'d after the receipts below were copied.

## 10. Receipts (all under `.ufo/waves/round-45/a2w1/C1ExecPlaneDiff/`)

`census-base.sh`, `census-impl.sh` (the scored bytes), `runlog.txt`, `run-{base,impl}-{1,2,3}.out` and
`.err` (full stdout incl. header, timestamps 03:24:54Z-03:25:06Z), `body-{base,impl}-{1,2,3}.out`
(header dropped), `analysis.txt` + `analyze.py` (shape/value checker), `compact-diffs.txt` (field-level
diff for all eight pairs), `rev-diff.txt` (the 6 hunks between revisions), `prior-now-base1.diff`
(cross-time drift), `run-alternating.sh`, `body-mut-*.out` + `mut-*.out` (sensitivity control),
`tset-{base,impl}.txt`, `tset-diff.txt`, `trace-{base,impl}.log.gz` (strace sets).
