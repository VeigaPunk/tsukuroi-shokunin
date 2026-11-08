# MutAuto — held-out mutants of V3 (round 93, wave w1)

Seat: MUTATION-TESTER. Target: `tools/check-limine-pins.py` V3 (`--limine-version auto`) and the three
families that are supposed to certify it (`AUTO-ERA-A`, `AUTO-ERA-B`, `AUTO-PROBE-FAIL`) in
`tools/limine-pin-battery-r93.py`. Lane read-only; every mutant is a **copy** under
`/fast/scratch/hyaku/tsukuroi-r93/MutAuto/mutants/` (mirrored into `w1/MutAuto/mutants/`).

Axes (godspeed): (a) killed mutants per battery run, (b) coverage gaps that survive, (c) operability
honesty of `auto` — a host whose bootloader cannot be identified must never be answered with another
release's rule.

## Instrument identity and restoration evidence

| instrument | sha256 (before first command) | sha256 (after all runs) | frozen value |
|---|---|---|---|
| `tools/check-limine-pins.py` | `6b4c53d1b56f4935cbcad3327259c15dd643af5ecec428522f998b7c5b6260aa` | `6b4c53d1…b6260aa` | matches freeze line |
| `tools/limine-pin-battery-r93.py` | `ddd7e9550da163575ea5c41416f7fc6effd6dcdea9e477843b9fd759675e1aad` | `ddd7e955…675e1aad` | matches freeze line |
| probe source of every mutant | `gate-orig.py` = byte-identical copy of the gate | `6b4c53d1…b6260aa` | — |

`sha256sum -c .ufo/waves/round-93/before/freeze-manifest.sha256` from the lane root: **12/13 OK**;
the single FAILED entry is `.ufo/plans/round-93.md` (`git status` → ` M`, a pre-existing
**Amendment A1** appended by another seat, `git diff --stat` = `1 file changed, 14 insertions(+)`);
both gate and battery are `OK`. I wrote nothing in the lane outside
`.ufo/waves/round-93/w1/MutAuto/`; scratch was deleted on exit.

## Method

```
S=/fast/scratch/hyaku/tsukuroi-r93/MutAuto; TMPDIR=$S
python3 tools/limine-pin-battery-r93.py --gate <mutant> --runs 1 --work $S/w/<id> --json $S/out/<id>.json
```

Each mutant is one exact-string replacement on a single clause of the gate copy (replacement count
asserted `== 1`); each compiles clean (`python3 -m py_compile`). Every run has its own `--work` dir;
runs were launched `&`/`wait` in two batches. The battery's own bwrap isolation applies unchanged.
Baseline (identical command, `--gate gate-orig.py`):

```
families_passed 96/96 verdict met failed -        cases=384  error_rows=0
```

## Mutant table

| id | one clause mutated | sha256 (16) | battery result | verdict |
|---|---|---|---|---|
| M01 | probe returns a hardcoded `12.9.4` | `d1c63f3c5d235ad8` | unmet 95/96, failed `AUTO-ERA-B`, 0 error rows | **killed** |
| M02 | probe returns the fake's output unchanged (no parse) | `5d0af7be87de35ca` | unmet 94/96, failed `AUTO-ERA-A,AUTO-ERA-B`, 8 error rows | **killed** |
| M03 | probe accepts `Limine 12.9` (two components) as `12.9.0` | `130a51870f3223df` | met 96/96, 0 error rows | **survived** |
| M04 | probe ignores the exit code | `3c82aa7e09e4f033` | met 96/96, 0 error rows | **survived** |
| M05 | probe passes no timeout at all | `a36255800bd72c3e` | met 96/96, 0 error rows | **survived** |
| M06 | probe reads stderr instead of stdout | `89a41ee886a9277c` | unmet 94/96, failed `AUTO-ERA-A,AUTO-ERA-B`, 8 error rows | **killed** |
| M07 | probe failure falls back to `12.9.4` (N06's class) | `5e2d3cf742bd4582` | unmet 95/96, failed `AUTO-PROBE-FAIL`, 0 error rows | **killed** |
| M08 | probed version recorded, `limine_version_source` stays `flag` | `c92c881431d44f4a` | unmet 94/96, failed `AUTO-ERA-A,AUTO-ERA-B`, 0 error rows | **killed** |
| M09 | `auto` accepted case-insensitively (`AUTO`, `Auto`) | `54668ff6f9b9e63a` | met 96/96, 0 error rows | **survived** |
| M10 | probe runs only after the conf is confirmed readable (unreadable conf → rc 2 first) | `ad127ac152c658ba` | met 96/96, 0 error rows | **survived** |
| M11 | probe timeout 30 s (longer than the battery's 20 s) | `ab69b3f45e36994e` | met 96/96, 0 error rows | **survived** |
| M12 | probe blocks 25 s (models a probe consuming its 30 s budget) | `c00db4a0f8c88cac` | unmet 93/96, failed `AUTO-ERA-A,AUTO-ERA-B,AUTO-PROBE-FAIL`, 8 error rows (`timeout`) | **killed as error rows** |

Killed = 6/12. 5 killed by a named family with a *wrong answer*; M12 is killed only by the battery's
per-case wall clock, not by an answer (see "Timeout implication").

Observed answer rows (from `out/auto-rows.json`):

- M01 `AUTO-ERA-B`: want `LP-MISMATCH→panic`, got `LP-MISMATCH→prompt` with
  `limine_version 12.9.4, source probe` (the fake said `12.9.6`).
- M02 `AUTO-ERA-A/B`: gate exits 64 with usage on stderr, no JSON (`bad-output: JSONDecodeError rc=64`).
- M06 `AUTO-ERA-A/B`: same shape, stderr `--limine-version auto: \`limine --version\` probe failed`.
- M07 `AUTO-PROBE-FAIL`: row `('auto', rc=0, stdout=885 B)` — a verdict where rc 64 + empty stdout is
  required (the silent-fallback class).
- M08 `AUTO-ERA-A/B`: correct era answer, but `limine_version_source = "flag"` instead of `"probe"`.
- M12: `AUTO-ERA-A/B` each `passed=False, error="timeout"` (4+4 rows); `AUTO-PROBE-FAIL` rows
  `('auto', rc=None, stdout_bytes=None)`.

## Diff hunks (each mutant, against `gate-orig.py`)

M01 `probe_limine_version`
```diff
     if p.returncode != 0:
         return None
-    m = re.search(r"(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b", p.stdout)
-    return m.group(1) if m else None
+    return "12.9.4"
```
M02 (same two lines)
```diff
-    m = re.search(r"(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b", p.stdout)
-    return m.group(1) if m else None
+    return p.stdout.strip() or None
```
M03 (same two lines)
```diff
-    m = re.search(r"(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b", p.stdout)
-    return m.group(1) if m else None
+    m = re.search(r"(?i)\blimine\s+v?(\d+\.\d+(?:\.\d+)?)\b", p.stdout)
+    return (m.group(1) + ".0" if m.group(1).count(".") == 1 else m.group(1)) if m else None
```
M04
```diff
     except (OSError, subprocess.SubprocessError):
         return None
-    if p.returncode != 0:
-        return None
     m = re.search(r"(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b", p.stdout)
```
M05
```diff
-        p = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=5)
+        p = subprocess.run([executable, "--version"], capture_output=True, text=True)
```
M06
```diff
-    m = re.search(r"(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b", p.stdout)
+    m = re.search(r"(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b", p.stderr)
```
M07 (`main`)
```diff
     if version == "auto":
         probed = probe_limine_version()
-        if probed is None:
-            ap.print_usage(sys.stderr)
-            print("check-limine-pins: --limine-version auto: `limine --version` probe failed",
-                  file=sys.stderr)
-            return 64
-        version, version_source = probed, "probe"
+        version, version_source = (probed if probed is not None else "12.9.4"), "probe"
```
M08 (`main`)
```diff
-        version, version_source = probed, "probe"
+        version, version_source = probed, "flag"
```
M09 (`main`)
```diff
-    if version == "auto":
+    if version.lower() == "auto":
```
M10 (`main`)
```diff
     if version == "auto":
+        if a.conf and not os.path.isfile(a.conf):
+            return 2
         probed = probe_limine_version()
```
M11
```diff
-        p = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=5)
+        p = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=30)
```
M12
```diff
     try:
-        p = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=5)
+        __import__("time").sleep(25)
+        p = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=30)
```

## Survivors: gap, not equivalent

Each survivor was re-measured on the input the roster never builds, with a fake `limine` first on
`PATH` and a one-line conf (`timeout: 3`; no pins → verdict HEALTHY). All six change behavior on those
inputs, so none is an equivalent mutant; each is a **coverage gap** plus the family that should catch it.

| mutant | unsampled input | pristine gate | mutant | gap / family that should catch it |
|---|---|---|---|---|
| M03 | fake prints `Limine 12.9`, `--limine-version auto` | rc 64 (usage), empty stdout | rc 0, verdict, `limine_version 12.9.0, source probe` | no family feeds a two-component probe output; the *era split* it lands on is era-A, so `AUTO-ERA-A` with a `Limine 12.9` fake would catch it (a two-component answer must be a refusal per `parse_limine_version`). |
| M04 | fake prints `Limine 12.9.6` **and** `exit 1` | rc 64 (usage) | rc 0, verdict, `12.9.6, probe` | the only failing fake (`AUTO-PROBE-FAIL`) prints **nothing**, so "nonzero exit" and "no parsable version" are the same branch; a fourth auto family (or one more case in `AUTO-PROBE-FAIL`) whose fake prints a version *and* exits 1 would catch it. |
| M05 | fake `sleep 8; echo "Limine 12.9.6"`, auto | rc 64 at **5104 ms** (own 5 s timeout) | rc 0 at **8107 ms**, verdict | no fake outlives the probe's budget, so the timeout clause is inert; a fake that sleeps > 5 s would catch both M05 and M11. |
| M09 | `--limine-version AUTO` | rc 64 | rc 0, verdict, `12.9.6, probe` | `REFUSAL-VERSIONS` enumerates 10 values and none is a case-variant of `auto`; adding `AUTO`/`Auto` there would catch it. Note: the contract fixes the spelling `auto` but does not forbid lenience, so this is a strictness gap, not a contract breach. |
| M10 | `auto` + missing `--conf`, probe succeeds | rc 2 with JSON `{"error": "conf unreadable…", "limine_version": "12.9.6", "limine_version_source": "probe"}` | rc 2, **empty stdout**, probe never run | every auto case has a readable conf, so refusal *precedence* (probe-before-conf vs conf-before-probe) is never exercised; an auto case with `conf_missing=True` would catch it (and would also pin whether the JSON must carry `limine_version_source` on rc 2). |
| M11 | same slow fake as M05 | rc 64 at 5104 ms | rc 0 at 8128 ms | as M05: the 30 s value is only observable when the binary outlives 5 s, which no fake does. |

Relevance to C2's wording: C2 says `auto` "refuses (rc 64, empty stdout) when the probe fails". The
battery samples three failure shapes — absent binary (not sampled at all in the roster: no auto case
runs on an empty PATH), nonzero exit with empty output, and (after the `Limine 12.9` / `exit 1` gaps
above) neither a nonzero exit *with* output nor a timeout. M03/M04/M05/M11 are that boundary.

M02 and M06 also pass `AUTO-PROBE-FAIL` while failing `AUTO-ERA-A/B`: a gate that refuses **every**
auto value satisfies a family whose expected answer *is* a refusal. This is the same class already
recorded as Amendment A1 in `.ufo/plans/round-93.md` ("a refusal-shaped control cannot certify a
refusal family"); my M02 measurement is an independent instance from the other direction (a
successful-probe gate that refuses everything), and it confirms the family is not self-sufficient —
`AUTO-ERA-A/B` are what kill M02/M06.

## Timeout implication (M11 vs M12) — what it does to "0 error rows"

- **M11 (probe `timeout=30`) survives**: with fakes that exit immediately the value is inert, so the
  family cannot see the budget at all. The 30 s value equals the probe's own budget, which is
  **larger than the battery's per-case `TIMEOUT = 20`**.
- **M12 (probe blocks 25 s, i.e. a probe that actually consumes the 30 s budget)**: `AUTO-ERA-A`,
  `AUTO-ERA-B` and `AUTO-PROBE-FAIL` all fail, but not by an answer — the battery's `subprocess.run(…,
  timeout=20)` fires first and the case is recorded `error="timeout"` (`AUTO-ERA-A/B`, 8 rows) or a
  usage row with `rc=None, stdout_bytes=None` (`AUTO-PROBE-FAIL`). Verdict: `unmet 93/96`, **8 error
  rows / 384 cases**.

So: **a gate whose probe hangs is reported as a `timeout` error row, never as the rc-64 refusal.** The
refusal-on-timeout clause can only be observed as a refusal when the probe's own budget is *shorter*
than 20 s; with M11's 30 s budget the two verdicts "refused because the probe timed out" and "still
blocked when the battery gave up" are indistinguishable from the case log (both `passed=False`, and
the second is an error row). Consequences for the declaration:

1. The landed gate's `0 error rows` (C1/C2 wording) is true of today's fixture shapes and is **not**
   evidence for the timeout half of V3's refusal contract: no fixture creates a probe that outlives
   5 s, so that clause is untested by construction, and any battery run against a gate that blocks
   past 20 s necessarily carries error rows. "0 error rows" therefore cannot be quoted as proof that
   the timeout branch refuses rather than hangs.
2. If a mutant/bend ever *does* hang the probe, the family's failure mode is `error="timeout"` — a
   detector/execution failure, not a substantive `unmet` answer; it must be reported as inconclusive
   on the refusal clause, not as a kill (per the mutation-tester rule: a baseline failure is
   inconclusive, and here a battery-side timeout is not the mutant's answer).

## Verdict

Supports C2 for the probe clauses the roster actually samples — hardcoded version then era selection
(M01 killed by `AUTO-ERA-B`), unparsed output (M02 killed by `AUTO-ERA-A/B`), stdout-vs-stderr
(M06 killed), silent fallback to `12.9.4` (M07 killed by `AUTO-PROBE-FAIL`), and source labelling
(M08 killed by `AUTO-ERA-A/B`). Qualifies C2 and finds 6 coverage gaps (M03, M04, M05, M09, M10, M11:
two-component probe output, nonzero-exit-with-output, probe timeout budget, `auto` spelling,
refusal precedence, and the timeout budget again), and shows that with a probe budget longer than the
battery's 20 s per-case cap the timeout branch can only surface as a `timeout` error row (M12: 8 error
rows / 384 cases), so "0 error rows" is not evidence for the timeout sub-clause. Mutants are
survivals/gaps, not permission to change the contract.

Receipts: `w1/MutAuto/mutants/M01…M12-*.py` (mutant sources), `w1/MutAuto/gate-orig.py` (pristine
copy, `6b4c53d1…b6260aa`), `w1/MutAuto/out/*.log` (battery summary + rc per run),
`w1/MutAuto/out/auto-rows.json` (every AUTO case row: want/got/error/usage rows),
`w1/MutAuto/receipts/{base,M01…M12}.case-log.json.gz` (full 384-case battery logs, gzipped; the
uncompressed copies lived only in scratch), `w1/MutAuto/receipts/freeze-check.txt` (manifest 12/13 OK;
the FAILED `round-93.md` is Amendment A1, `git status` ` M`, not written by this seat).
