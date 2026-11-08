# MutProbe — r94 w1 mutation tester (C2: auto-by-default V4 / installed-version probe)

Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (read-only; HEAD `b6447374…`, freeze
manifest `.ufo/waves/round-94/before/freeze-manifest.sha256` verifies 12/12 OK).
Scratch (deleted on exit): `/fast/scratch/hyaku/tsukuroi-r94/MutProbe/`.
Seat receipts: `.ufo/waves/round-94/w1/MutProbe/` (`mutants/`, `make_mutants.py`, `mutants.diff`,
`adhoc.py`, `run_one.sh`, `evidence/summary.json`).

Instruments used read-only, bytes as declared:

| instrument | sha256 (measured) |
|---|---|
| `tools/check-limine-pins.py` | `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32` |
| `tools/limine-pin-battery-r94.py` | `d66b4a59778f8d5d006259d275875f95f002430b0e41990a111d73b6dc7bb503` |
| seat copy `mutants/gate-pristine.py` (baseline) | `7d79ac29…d6090d32` (identical) |

## Method

Eight mutants of a **copy** of the V4 gate, each a single behavioural clause replaced (see
`mutants.diff`; one diff per mutant, `M05` is a whole-mechanism swap of the probe's *read* step —
the f6 forger framed as a mutant). Detectors, all run against the same bytes:

1. **battery** `limine-pin-battery-r94.py --gate <copy> --runs 1` (98 families × 4 cases, bwrap
   ISOLATION launcher, 392 cases; `--work` and `TMPDIR` under the seat scratch).
2. **gate selftest** `<copy> --selftest` (39 assertions).
3. **battery `--usage-check`** (extra, not in the assignment's scoring pair — it is the one
   instrument that drives `--limine-version auto` and the *omitted* flag at CLI level).
4. **ad-hoc probes** (`adhoc.py`, 4 observations over 2 fixtures) only for mutants 1–3 leave alive:
   `--live` with no flag (C2's own shape), `--live --limine-version 12.9.6` (flag vs probe),
   `--limine-version 12.09.6` (zero-padded era), and a fake `limine` that answers after 8 s
   (probe timeout; 8 s > gate's 5 s, < the battery's 20 s case TIMEOUT).

Baseline of the pristine bytes: **battery 98/98 `met`, selftest `PASS 39/39`, usage-check `met`**,
ad-hoc = `12.9.4/probe/pre-12.9.5`, `12.9.6/flag/12.9.5+`, `12.09.6/flag/12.9.5+`, hang → rc 64 in 5.1 s.

## Table

`families_passed` is x/98; `failed_families` is the battery's own list; selftest is the gate's own
count; "ad-hoc" is the probe that first fails on that mutant.

| gate | battery | families_passed | failed_families | selftest | usage-check | ad-hoc | verdict |
|---|---|---|---|---|---|---|---|
| baseline | met | 98/98 | – | PASS 39/39 | met | all 4 as expected | – |
| M01 default `12.9.6` | unmet | 97/98 | ERA-DEFAULT | PASS 39/39 | unmet (omitted-flag row) | live-default | **KILLED** (ERA-DEFAULT) |
| M02 `--live` ignores the flag | met | 98/98 | – | PASS 39/39 | met | live-flag | **SURVIVED** battery+selftest; killed ad-hoc |
| M03 probe falls back to `12.9.4` | unmet | 96/98 | AUTO-PROBE-FAIL, AUTO-PROBE-SHAPES | PASS 39/39 | met | probe-hang | **KILLED** (2 families) |
| M04 probe timeout 60 s | met | 98/98 | – | PASS 39/39 | met | probe-hang (8.1 s) | **SURVIVED** battery+selftest; killed ad-hoc |
| M05 probe reads source text | unmet | 97/98 | AUTO-PROBE-SHAPES | FAIL 38/39 (`probe-version`) | met | probe-hang (0.1 s) | **KILLED** (2 detectors) |
| M06 source always `"flag"` | unmet | 96/98 | AUTO-ERA-A, AUTO-ERA-B | PASS 39/39 | unmet (auto + omitted rows) | live-default | **KILLED** (2 families) |
| M07 era from the raw string | met | 98/98 | – | PASS 39/39 | met | zero-padded-era | **SURVIVED** battery+selftest; killed ad-hoc |
| M08 probe `--version-only` | unmet | 97/98 | ERA-DEFAULT | PASS 39/39 | unmet (auto + omitted rows) | live-default | **KILLED** (ERA-DEFAULT) |

Mutation score on the assigned pair (battery + gate selftest): **5/8 killed** (M01, M03, M05, M06,
M08), **3/8 survived** (M02, M04, M07). With `--usage-check` added, still 5/8 (it kills nothing the
battery misses). With the four ad-hoc probes: 8/8.

## Per-mutant evidence

### M01 — default is `12.9.6` instead of `auto` (KILLED)
```diff
-    ap.add_argument("--limine-version", default="auto",
+    ap.add_argument("--limine-version", default="12.9.6",
```
Battery: `families_passed 97/98 verdict unmet failed ERA-DEFAULT` — all 4 ERA-DEFAULT cases read
`[[3,"LP-MISMATCH","panic"],[7,"OK","none"]]` where the family wants `prompt` (era B selected from a
hand-typed default; the probe never ran). `limine_version_source` stayed `flag`.
Selftest: `PASS 39/39` — its `era-default` case calls `check()` directly and never touches argparse.
`--usage-check`: `unmet`, the omitted-flag row reads a verdict with `limine_version 12.9.6 /
source flag` instead of `12.9.4 / probe`. Ad-hoc `live-default`: `12.9.6/flag` vs baseline
`12.9.4/probe`.

### M02 — `--live` always probes, even with an explicit `X.Y.Z` (SURVIVED the pair)
```diff
-    if version == "auto":
+    if a.live or version == "auto":
```
Battery `98/98 met`, selftest `PASS 39/39`, usage-check `met`: **no detector runs `--live`**.
Counterexample (ad-hoc `live-flag`, era fixture, host limine 12.9.4):
`--live --limine-version 12.9.6` → pristine `ver=12.9.6 src=flag era=12.9.5+ cons=panic`;
mutant `ver=12.9.4 src=probe era=pre-12.9.5 cons=prompt` — an explicitly requested release silently
replaced by the installed one. Coverage finding: the C2 contract "an explicit `X.Y.Z` is not probed"
is certified by no instrument; only the ExecLive seat exercises `--live` outside the sandbox.

### M03 — probe failure falls back to `12.9.4` (KILLED)
```diff
-        probed = probe_limine_version()
-        if probed is None:
-            ap.print_usage(sys.stderr)
-            print("check-limine-pins: --limine-version auto: `limine --version` probe failed",
-                  file=sys.stderr)
-            return 64
+        probed = probe_limine_version() or "12.9.4"
```
(The literal clause `probed or "12.9.4"` alone is a **dead clause** in the pristine gate: the
`if probed is None: … return 64` guard runs first, so that mutant is equivalent and scored nothing —
observation, not a contract finding.)
Battery `96/98 unmet failed AUTO-PROBE-FAIL,AUTO-PROBE-SHAPES` — 8 failing cases: `AUTO-PROBE-FAIL`
cases want `[64,"usage"]`, got a verdict (`probed or 12.9.4` on `exit 1`); `AUTO-PROBE-SHAPES` cases
want `[64,"usage"]`, got a verdict on the `no version here` / `12.9.6-rc1` fake. Ad-hoc
`probe-hang`: mutant answers `rc=0 HEALTHY ver=12.9.4 src=probe` where pristine is `rc=64` in 5.1 s.

### M04 — probe timeout 60 s (SURVIVED the pair)
```diff
-        p = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=5)
+        p = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=60)
```
Battery `98/98 met`, selftest `PASS 39/39`, usage-check `met`: every probing executable in the
roster answers immediately, so the 5 s bound is unexercised — the battery's 20 s case TIMEOUT can
only fire on a gate that hangs longer than 20 s, and 60 s never reaches it from these fixtures.
Counterexample (ad-hoc `probe-hang`, fake `limine` = `sleep 8; echo "Limine 12.9.6"`):
pristine `rc=64` after 5.1 s with empty stdout; mutant `rc=0 HEALTHY ver=12.9.6 src=probe era=12.9.5+`
after 8.1 s — a slow bootloader binary becomes an answered verdict instead of a refusal.

### M05 — probe reads the executable's source text instead of running it (KILLED)
```diff
-        p = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=5)
-    except (OSError, subprocess.SubprocessError):
-        return None
-    if p.returncode != 0:
-        return None
-    m = re.search(r"(?i)\blimine\s+v?(\d+\.\d+\.\d+)(?![\w.-])", p.stdout)
+        with open(shutil.which(executable) or executable, "r", errors="replace") as f:
+            text = f.read()
+    except OSError:
+        return None
+    m = re.search(r"(?i)\blimine\s+v?(\d+\.\d+\.\d+)(?![\w.-])", text)
```
Battery `97/98 unmet failed AUTO-PROBE-SHAPES`: the shapes fake's source is
`… echo "Limine 12.9.6" >&2`, and the forger answers `12.9.6` from the *text* where the family
demands `[64,"usage"]`. Gate selftest `FAIL 38/39`, `probe-version FAIL` — the
`echo "Limine 12.9.6" >&2` assertion returns `12.9.6` instead of `None` (it passes the other seven
probe assertions because the fake scripts contain their own answer as a literal, which is exactly
the forger's advantage). Note ERA-DEFAULT does *not* kill it: `/usr/bin/limine` is an ELF that really
contains the bytes `Limine 12.9.4`, so the forger answers the host correctly.

### M06 — `limine_version_source` is always `"flag"` (KILLED)
```diff
-        version, version_source = probed, "probe"
+        version, version_source = probed, "flag"
```
Battery `96/98 unmet failed AUTO-ERA-A,AUTO-ERA-B`: pins are correct (`prompt` for 12.9.4,
`panic` for 12.9.6) but 8 cases fail `auto_ok` on `limine_version_source == "flag"` instead of
`probe`. This is the only mutant the era families kill without a wrong verdict — the probe's
provenance field is load-bearing. `--usage-check` `unmet` on the same field for the `auto` and
omitted-flag rows. Ad-hoc `live-default`: `src=flag` vs baseline `src=probe`.

### M07 — era selected from the raw string, not the parsed tuple (SURVIVED the pair)
```diff
-    era_b = version >= VISIBILITY_ERA_SPLIT
+    era_b = limine_version >= "12.9.5"
```
Battery `98/98 met`, selftest `PASS 39/39`, usage-check `met`: every era-bearing fixture sends a
`X.Y.Z` whose lexicographic order matches numeric order (`12.9.4`/`12.9.5`/`12.9.6`), and
`--usage-check`'s zero-padded `12.09.4` row asserts only rc 0, never the era. The selftest asserts
`parse_limine_version("12.09.4") == (12,9,4)` — the parser, not the era it feeds. Counterexample
(ad-hoc `zero-padded-era`, era fixture, `--limine-version 12.09.6`): pristine
`ver=12.09.6 src=flag era=12.9.5+ cons=panic`; mutant `era=pre-12.9.5 cons=prompt` — a config whose
first body line carries `hash_mismatch_panic: no` is read as visible and the pin demoted from
`panic` to `prompt`. This is a live path: the probe passes through whatever `limine --version`
prints, and `12.09.6` is accepted by the parser.

### M08 — probe runs `limine --version-only` (KILLED)
```diff
-        p = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=5)
+        p = subprocess.run([executable, "--version-only"], capture_output=True, text=True, timeout=5)
```
Host `limine --version-only` → usage text, rc 1. Battery `97/98 unmet failed ERA-DEFAULT` — all 4
cases `bad-output: JSONDecodeError rc=64 … `limine --version` probe failed`: the default can never
resolve. `--usage-check` `unmet` (auto + omitted rows, rc 64). Ad-hoc `live-default` → `rc=64`.
Selftest `PASS 39/39` — its `fake_probe` scripts ignore `argv`, so the flag name is invisible to it:
the battery is the only instrument that pins the probe's argument.

## What the mutant frontier says

- The C2 mechanism is well welded: the default, the refusal, the provenance field and the probe's
  own read step each have a family (or two) that fails when broken. `ERA-DEFAULT` is the load-bearing
  family for the default/probe rewire (M01, M08); `AUTO-ERA-A/B` for provenance (M06);
  `AUTO-PROBE-FAIL`/`AUTO-PROBE-SHAPES` for the refusal (M03) and the forger (M05).
- Three clauses are **certified by nothing** in the assigned pair, each with a working
  counterexample: the `--live` × explicit-flag precedence (M02), the 5 s probe timeout (M04), and
  the era's normalisation of a zero-padded version (M07). All three are cheap to close with the
  fixtures already in `adhoc.py`; none of them contradicts a claim under test — they are coverage
  gaps, not contract failures.
- Asymmetry worth knowing: the gate selftest alone kills only M05 (1/8); the battery alone 5/8.
  `--usage-check` adds no kill the battery lacks. The battery's fakes all answer instantly and
  ignore `argv`, which is precisely why M04 and M08 differ in outcome.

## Restoration / cleanliness

- Every mutant is a **copy** under the seat dir; the lane instruments were never written
  (`sha256sum -c .ufo/waves/round-94/before/freeze-manifest.sha256` → 12/12 `OK` after the runs),
  `git status --porcelain` shows only the untracked `.ufo/waves/round-94/w1/` receipts and wave
  markers. The seat copy of the pristine gate still hashes `7d79ac29…d6090d32`.
- No `git`/`jj` mutation, no `sudo`, no writes outside the seat dir and the scratch root; all
  `--work`/`TMPDIR` dirs were under `/fast/scratch/hyaku/tsukuroi-r94/MutProbe/`, deleted on exit.
- No tool installs or upgrades were needed.

## Verdict

**C2's two clauses are supported and one of its documented boundaries is under-certified.**
The battery + gate selftest kill 5/8 one-clause mutants of the V4 default and probe mechanism
(M01 default `12.9.6` → `ERA-DEFAULT` 97/98; M03 fallback → `AUTO-PROBE-FAIL` + `AUTO-PROBE-SHAPES`
96/98; M05 source-read forger → `AUTO-PROBE-SHAPES` 97/98 and selftest 38/39; M06 source always
`flag` → `AUTO-ERA-A/B` 96/98; M08 `--version-only` → `ERA-DEFAULT` 97/98), so "auto is the default,
the probe is executed, its failure refuses, and its provenance is recorded" is not a paper claim;
the pristine instrument reads 98/98 `met`, selftest `PASS 39/39`, usage-check `met`, and the
flag-free live run records `limine_version 12.9.4` + `limine_version_source probe`.
Three mutants survive the assigned pair with executable counterexamples — M02 (`--live` ignores an
explicit `X.Y.Z`: 12.9.6 requested, 12.9.4 answered), M04 (60 s probe timeout: an 8 s bootloader
answers a verdict instead of refusing), M07 (era from the raw string: `12.09.6` demotes `panic` to
`prompt`) — so the pair's coverage is 5/8 and the timeout, `--live` precedence and version
normalisation clauses are falsifiable only by the ad-hoc probes in
`.ufo/waves/round-94/w1/MutProbe/adhoc.py`. Nothing observed falsifies C1; no instrument, contract
or claim was changed.
