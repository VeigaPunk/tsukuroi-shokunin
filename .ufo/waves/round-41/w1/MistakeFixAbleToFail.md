VERDICT: defect-found

# M-2 — pipefail/SIGPIPE: a fix shown able to fail, and a live instance in the census

Seat: MistakeFixAbleToFail. Lane tip at dispatch `71851d636ab1bffaf8fee5016617c88878a666f1`.
Lane content was read-only throughout; the only lane writes are this report and its receipts.
Scratch `/fast/scratch/hyaku/tsukuroi-r41/MistakeFixAbleToFail/` removed at exit.
No pacman transaction, no service, no sudo, no host mutation.

## 1. The class, demonstrated

Fixture (`receipts/red-green-panel.txt` §1–§5): `big.txt` 82,888,917 B compressed to
`big.gz` 10,553,466 B, needle `X_NEEDLE_MARKER` on line 1.

Red — 5/5, no output, status 141 (128+SIGPIPE):

```
$ set -o pipefail; zcat big.gz | grep -q X_NEEDLE_MARKER && echo hit
  run 1: pipeline status=141   ... run 5: pipeline status=141
```

Green — 5/5, the capture.sh form reports the match:

```
$ set -o pipefail; c=$(zcat big.gz | grep -c X_NEEDLE_MARKER || true)
  run 1: c='1' ... run 5: c='1'      absent-needle control: c='0'
```

`grep -m1` is the same trap as `grep -q` (`status=141`, ×2), and `PIPESTATUS` confirms the
diagnosis: `statuses=141 0` — grep *did* match; only pipefail's report is wrong.

**The fixture size is part of the test.** With a small file the red case passes and the bug
is invisible:

| payload | compressed | red-case result |
|---|---|---|
| 1,000 lines | 1,892 B | `hit`, status 0 |
| 10,000 lines | 22,664 B | `hit`, status 0 |
| 50,000 lines | 109,186 B | no output, **141** |
| 200,000 lines | 428,527 B | no output, **141** |

So a regression fixture under the pipe buffer (65,536 B; `F_GETPIPE_SZ`=65536,
`/proc/sys/fs/pipe-max-size`=1,048,576) is *unable to fail* — it validates a bug.

Shape matrix, 6 reps per size, `( set -euo pipefail; ! printf '%s\n' "$out" | grep -q … )`
with the marker on line 1: 32/64/96 KiB → 0/6; 128 KiB → 1/6; 256/512/1024 KiB → 6/6. The
boundary is a race between grep closing the read end and printf finishing its write, not a
single byte count; it sits between one and two pipe capacities.

Also worth recording against the assignment's premise: the green form is correct for
SIGPIPE but blind to a *truncated* stream. With the needle at the end, an intact
`tail.gz` gives `1`, a 200,000 B truncation of it gives `0` — identical to "absent" —
because `|| true` erased the status that said the stream was cut.

## 2. A live instance of the class, in the census that this round's C1 extends

`tools/tsukuroi-census.sh:692`:

```sh
  if printf '%s\n' "$s_out" | grep -q '^error:'; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qkk sample probe error: $(printf '%s\n' "$s_out" | grep -m1 '^error:')"
```

`$s_out` is the merged `pacman -Qkk` output over `SAMPLE_N=8` packages
(`tsukuroi-census.sh:451`, `:687`), unbounded in the number of altered-file lines. The
probe surface is overridable (`PACMAN=${TSUKUROI_PACMAN:-pacman}`, `:430`; `cap()` at
`:580-583`), so the defect reproduces against the **unmodified** script with no lane edit
(receipt `live-defect-692.txt`):

```
$ env TSUKUROI_PACMAN=stub/pacman QKK_OUT=qkk-small.txt QKK_RC=1 bash tools/tsukuroi-census.sh
  -> PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: pkgA: /usr/bin/x (Permission denied); …)  rc=2
$ env TSUKUROI_PACMAN=stub/pacman QKK_OUT=qkk-large.txt QKK_RC=1 bash tools/tsukuroi-census.sh
  -> PLANE packages: DEGRADED (… drift=0 backup_diffs=0 nonroot_artifacts=1; …)                                rc=1
```

Both fixtures carry the identical line 1, `error: pkgA: /usr/bin/x (Permission denied)`;
only the size differs (163 B vs 272,053 B). Reproduced 2/2 each way. That the error line
*was consumed* is visible in the wrong-verdict line itself: `nonroot_artifacts=1` is counted
by `:705` from the `(Permission denied)` text of that same line.

The consequence is a wrong verdict, in the direction that matters: a probe that could not
be read is reported as a merely degraded plane, and `drift=0` is asserted from a buffer
that carried an error. The rc gate above it cannot cover this — `:686` deliberately treats
`rc=1` as normal because `pacman -Qkk` returns 1 for "files altered", so line 692 is the
only thing that notices an error line arriving with rc=1. Size sweep against the real
census: correct `BLOCKED` at 84 B / 2,442 B / 19,430 B; wrong `DEGRADED` at 78,846 B and at
every larger size tested up to 644,334 B.

`tools/tsukuroi-census.sh:694` is the same class — `$(… | grep -m1 '^error:')` short-circuits
identically — and here `set -e` makes it fatal. Proven by fixing 692 alone: the large
fixture then returns **rc=141 with no `PLANE packages:` line at all**
(`live-defect-692.txt`, "site 694 is the same class").

## 3. The fix, shown able to fail

```
-  if printf '%s\n' "$s_out" | grep -q '^error:'; then
-    PKG_V=BLOCKED
-    PKG_NOTE="pacman -Qkk sample probe error: $(printf '%s\n' "$s_out" | grep -m1 '^error:')"
+  s_err_n=$(printf '%s\n' "$s_out" | grep -c '^error:' || true)
+  if [ "${s_err_n:-0}" -gt 0 ]; then
+    PKG_V=BLOCKED
+    s_err_first=$(printf '%s\n' "$s_out" \
+      | awk 'f == 0 && /^error:/ { f = 1; e = $0 } END { print e }')
+    PKG_NOTE="pacman -Qkk sample probe error: $s_err_first"
     return
   fi
```

`grep -c` and the `awk` both read to EOF, so the writer is never stared down by an early
close; `awk` has no `exit`, so it yields the first matching line after reading the whole
buffer. This is the same form the lane already uses at `:603` (`nlines`) and `:703`/`:705`
— not a new convention.

Panel (each row a full census run against a stub `-Qkk`):

| script | fixture | rc | verdict |
|---|---|---|---|
| `tools/tsukuroi-census.sh` (lane) | 163 B | 2 | `PLANE packages: BLOCKED` + probe-error note |
| fixed copy, 2 sites | 163 B | 2 | `PLANE packages: BLOCKED` + probe-error note |
| `tools/tsukuroi-census.sh` (lane) | 272 KiB | 1 | `PLANE packages: DEGRADED`, no note |
| fixed copy, 2 sites | 272 KiB | **2** | `PLANE packages: BLOCKED` + probe-error note |
| `tools/tsukuroi-census.sh` (lane) | 78,846 B | 1 | `PLANE packages: DEGRADED`, no note |
| fixed copy, 2 sites | 78,846 B | **2** | `PLANE packages: BLOCKED` + probe-error note |

The fixture is shown able to fail in three distinct ways: it fails the unfixed census (red),
it fails a plausible single-site fix (rc=141), and it passes the two-site fix (green) —
while the 163 B fixture distinguishes none of the three. A green run alone would have
proved nothing here.

## 4. Audit of the rest: every `| grep -q` / `| head` pipeline under pipefail

Only three files under `tools/` carry `pipefail` (`grep -n pipefail tools/`):
`tsukuroi-census.sh:423` (`set -euo pipefail`), `boot-chain-audit.sh:139`
(`set -uo pipefail`, no `-e`), and a generator string at `score-census-handoff-r32.py:725`.
`capture.sh:6` is `set -euo pipefail`. Full per-site table in `pipeline-audit.txt`; the
discernment that matters is that three *different* failure directions are in play:

**a. Live / wrong verdict** — `census:692` (proven), `census:694` (proven).

**b. Latent / census abort.** `x=$(printf … | head …)` is a plain assignment, so a 141
terminates the census and truncates its output (proven: `status=141`, the next statement
never runs). Sites: `:928`, `:966`, `:1048`, `:1423`, `:1498`, `:1621`, `:1635`, `:1641`,
`:1652`. Reachability is what separates them: `:928/:966/:1048/:1423/:1498` capture a
one-line `systemctl show`/`nvidia-smi` value and cannot grow; `:1621/:1635/:1641` read
`pacman -Qu`/`pacman -Sup` name lists and `:1652` reads the whole `pacman -Suu
--print-format` list, so a host with a large pending upgrade set reaches them. Those five
are the ones to fix alongside 692.

**c. Latent / false test failure.** Inside an `if`/`elif` condition `set -e` does not
abort, so the branch simply inverts and `bad` fires. Sites: `:2175`, `:2181`, `:2187`,
`:2192`, `:2223`, plus `:2177` on `$pkgline`. `$out` is the whole census output; on the
host that is 8,417 B with a 5,121 B longest line, and the fixture `$out` is *bounded below
the flip threshold* by the base receipt's own result — `.ufo/waves/round-41/before/c1-before.jsonl`
records `TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)`, and a `$out`
past the threshold would fail all 124 on the `:2175` branch. So these are latent with
roughly a 10× margin, not firing — but they are one verbose plane away from converting
every selftest case into "hostname override not honoured", and the same shape at `:2192`
is proven to populate `miss` for a pattern that *is* present. A round-41 verdict that
leans on the selftest passing should know this margin is finite.

**d. Safe, for the record.** `:676`, `:960`, `:1159`, `:1494` use process substitution
(status discarded, values correct); `:699`–`:709`, `:794`, `:1480`, `:1779`, `:1780`,
`:2172` funnel into sed/awk/paste/`grep -c`, which read to EOF, or are `|| true`-guarded;
`:1852` is a herestring with no pipe at all.

**e. boot-chain-audit.sh.** `:374/:379/:384` (`sed | head -n 1` in `$( )`) are benign on
value — `head -n1` wants line 1 — and with no `-e` a 141 only pollutes an exit status
nobody reads. `:483` (`find … -print -quit | grep -q .`) is SIGPIPE-safe by construction
(`find` emits one path and exits before grep can close the pipe), but it reaches the same
conclusion by another route: a failing `find` (missing `/usr/lib/initcpio`, unreadable
`/etc/fstab`) has stderr discarded at `2>/dev/null`, `grep -q .` is false, and
`boot_inputs_newer` prints `0` — "nothing newer than boot start", i.e. clean. A refused
measurement reads as a healthy one, unflagged because `-e` is absent. Adjacent to the
assigned class, reported because it shares the collapse.

## 5. Adjacent finding that touches this round's C2 gate

`capture.sh:19` is *not* in the SIGPIPE class — it is the correct form, and the assignment
is right that it reports the match. Its exposure is the mirror image:

```sh
c=$(zcat -- "$d/mtree" 2>/dev/null | grep -c '^\./\.MTREE ' || true)
[ "${c:-0}" -gt 0 ] && self=1
```

Demonstrated on the fixture: intact stream → `1`; truncated stream → `0`, indistinguishable
from "no `.MTREE` entry", because `|| true` erases the status that said the stream was cut
(without it, `status=1` is detectable). `self` is the `mtree_lists_self` column of
`localdb-anatomy.tsv`, which is one of the six host values the C2 counter gates on
(`host_ok == 6`). A silently-truncated capture therefore enters as a host **fact** rather
than a capture failure — the same "shape gate looks validated, the read is what matters"
hazard C2 already names. `capture.sh:33` (`p=$(ls -d "$db"/pacman-[0-9]*/ | head -n1)`) is
the set-e abort class, but the directory list is 2–3 entries and fits the pipe buffer, so it
is unreachable today. `:15`, `:18`, `:32`, `:34` are safe (wc / `head -c 2` / `grep -n` /
`sed -n 1,4p` without `q` all read to EOF or to a fixed offset).

## 6. What I did not do

- Did not run `--selftest` or the round-41 counters (C1 owns those; my item did not need
  them). The 124/124 baseline is cited from the existing before-receipt, not re-run.
- Did not test the `:1652` / `:1621` / `:1635` / `:1641` sites against the real script —
  reaching them needs a fixture that produces a multi-thousand-row `pacman -Suu`/`-Qu`
  list, which I did not build. Their *shape* is proven in isolation and their reachability
  is argued from the buffer sizes each command can emit; treat the severity as inference,
  the mechanism as observed.
- Did not touch the C1 declaration, the frozen counters, or any tracked file.

## Receipts

`.ufo/waves/round-41/w1/MistakeFixAbleToFail/`

| file | content |
|---|---|
| `red-green-panel.txt` | §1 red/green, size dependence, grep -m1, truncation, capacity, 6-rep matrices, `set -e` abort shapes |
| `live-defect-692.txt` | real-census reproduction, size sweep, single-site vs two-site fix, verdict panel |
| `pipeline-audit.txt` | every site with buffer, direction of error and reachability |
| `make-qkk-fixture.sh` | regenerates the 163 B / 272,053 B fixture pair |
| `qkk-small.txt`, `qkk-large.head.txt` | the fixture pair (large one truncated to its head; full size via the generator) |
| `pacman-stub.sh` | the read-only `-Qkk` stub used to drive the unmodified census |
