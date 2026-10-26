VERDICT: supports

# Seat RoutedSelfAssessScratch — item R-1 (round-40 closure §6.3)

Claim under test: the uncommitted working-tree change to `tools/check-self-assessment.py`
(adds `--scratch`, extracts the census archive there and gives the census child a `TMPDIR`
inside it) stops the census selftest tree from landing under `/tmp`; the pre-change script
must be shown to misroot it. Base revision for the comparison:
`71851d636ab1bffaf8fee5016617c88878a666f1` (lane tip at dispatch).

## The change (diff read, not modified)

`git -C <lane> diff 71851d636ab1bffaf8fee5016617c88878a666f1 -- tools/check-self-assessment.py`
(1 file, +18/−7; full copy at `RoutedSelfAssessScratch/script.diff`):

- base `census_case_count` at `tools/check-self-assessment.py` base blob:181 —
  `work = tempfile.mkdtemp(prefix="self-assessment-census-")` (caller `TMPDIR` only), and the
  child at base:189 runs with `env=git_env()`, whose allow-list (`CHILD_ENV_BASE`,
  base:94-110) never carries `TMPDIR`; the census child therefore always used `/tmp`.
- working version at `tools/check-self-assessment.py:185` — `mkdtemp(..., dir=scratch)`;
  `:192-194` — `child_tmp = work/.census-tmp`, `os.mkdir(child_tmp)`,
  `child_env = dict(git_env(), TMPDIR=child_tmp)`; `--scratch` parsed at `:1097-1101`;
  forwarded by `evaluate` at `:1120`. Nothing else in the diff.

Hashes: base blob `1e1ab6113d665684e15d147c0f3dae519cf2d313877e1603b841ad4db85d4257`
(= `old.py`), working tree `44b474fb5401559d9a4052f04f03145cd165a688a78455694d7dd25dba5838e6`
(= `new.py`, re-hashed after the runs; receipt `script-sha256.txt`).

## Run

Each copy was run once (old twice, see Flake) from
`/fast/scratch/hyaku/tsukuroi-r41/RoutedSelfAssessScratch/` under

```
strace -f -e trace=mkdir -o <trace> python3 <script> \
  --revision 71851d636ab1bffaf8fee5016617c88878a666f1 \
  --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
```

- old: `TMPDIR=<scratch>/t`, no `--scratch`
- new: `env -u TMPDIR`, `--scratch <scratch>/s` (the item's literal new invocation)
- new-tmpdir (supplementary, to separate the residual below): `TMPDIR=<scratch>/t`,
  `--scratch <scratch>/s`

Counts are `grep -c 'mkdir("/tmp'` on each trace; `/usr/bin/time` is absent on this host,
elapsed came from `date +%s` around each run. Repair: coreutils `mktemp` and `mkdir -p`
both issue the `mkdir` syscall here (checked with a one-directory probe trace), so
`-e trace=mkdir` is sufficient and no `mkdirat` is missed.

## Counts (mkdir under /tmp)

| run | elapsed | absolute `/tmp` mkdir calls | of which created | census-selftest `/tmp` refs |
|---|---|---|---|---|
| old (TMPDIR=t) | 303 s | **1153** | 1 dir (`/tmp/tsukuroi-r3-2-selftest.rR8CO1`, 0700) + 1152 `mkdir -p` component attempts (EEXIST) | yes — this is the census tree |
| old2 (rerun) | 97 s | **1153** | same | yes |
| new (`--scratch` only) | 119 s | **2** | 2 | **0** |
| new + TMPDIR=t | 148 s | **0** | 0 | 0 |

Observed lines (extracts in `RoutedSelfAssessScratch/trace-*.tmp-lines.txt`):

- old, `trace-old` line: `3941778 mkdir("/tmp/tsukuroi-r3-2-selftest.rR8CO1", 0700) = 0`
  — the census child's `mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX"`
  (`tools/tsukuroi-census.sh:1930`) with `TMPDIR` stripped from its environment. The 1152
  remaining `/tmp` lines are `mkdir -p` component walks resolving into that same directory
  (coreutils changes directory while creating, so nested components appear as relative
  `mkdir("tsukuroi-r3-2-selftest…")` calls; the absolute root creation above fixes where
  they land). The pre-change script's own archive work did go to `<scratch>/t` — only the
  census child was misrooted, which is exactly the defect.
- new, `trace-new`: `1768298 mkdir("/tmp/self-assessment-git-yhgoajv0", 0700) = 0` and
  `1768298 mkdir("/tmp/self-assessment-git-yhgoajv0/home", 0777) = 0`. These are the
  module-level `_GIT_SANDBOX = tempfile.TemporaryDirectory(...)` and
  `os.mkdir(_GIT_HOME)` at working `tools/check-self-assessment.py:69-71`, which run at
  import time, before `--scratch` is parsed. They are present in the base script too and are
  untouched by the diff. The census child contributes **0**: its 1154 absolute census mkdirs
  are under `<scratch>/s/…/.census-tmp/`, e.g.
  `2077559 mkdir("<scratch>/s/self-assessment-census-vp_zd0ev/.census-tmp/tsukuroi-r3-2-selftest.kR4VIW", 0700) = 0`.
- new + TMPDIR: no `/tmp` line at all; same census tree under `<scratch>/s/…/.census-tmp/`.

So the exact acceptance stated in the item ("new 0") holds only if the runner's `TMPDIR` is
also pointed at scratch (new-tmpdir = 0), or if the count is restricted to census-originated
mkdirs (0 in the literal `--scratch`-only run). The literal total for the literal invocation
is 2, both pre-existing `_GIT_SANDBOX` dirs, not the R40 misroot. If the wave harness exports
`TMPDIR` for the counter run (as the scratch rule asks), the 0 expectation holds as written.

## JSON summaries (full stdout copies in the seat directory)

All four runs: `"checked": 27`, `"mismatches": 6`, `"status": "FAIL"`, requested revision
`71851d63…`; mismatch ids identical: K07, K08, K09, K10, K13, K17. The two new runs and old2
are byte-identical after `json.dumps(..., sort_keys=True)`; old's only difference is the K13
reason text (the flake below). Example (`new.json`):

```
"revision": "71851d636ab1bffaf8fee5016617c88878a666f1",
"checked": 27,
"mismatches": 6,
"status": "FAIL",
...
K13: "operability row states 124 cases; the census selftest at this revision prints 128 cases
      (TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed))"
```

K13 is already a mismatch at this base revision (stated 124 vs measured 128 cases), which is
why `status` is FAIL in every run; the fix changes no check outcome, only where the census
child's temporary tree lives.

## Observation — one-off census selftest failure in the first old run (reported for calibration)

The first old run's K13 reason was
`operability row states 124 cases; the census selftest at this revision prints 128 cases (FAIL healthy: C1 root arm — 0755 owner bits present (R12-C1): hostname override not honoured — possible host read)`
— one FAIL line; the counter keeps only the last output line, so the passed/failed tally itself
was not captured. The identical command rerun (old2, 97 s) printed
`PASS (128 cases, 128 passed, 0 failed)`, and both new runs passed 128/128. I did not
reproduce or diagnose the one-case flip further (it did not affect the `/tmp` finding: both
old runs produced the same 1153 `/tmp` mkdir calls). I have no mechanism that ties it to
`TMPDIR`; treat it as an observed one-run flake of the archived census selftest on a loaded
host, not as evidence about this fix. If it recurs, the census selftest is the place to look
(`tools/tsukuroi-census.sh:2175-2176` hostname assertion).

## Limits / not done

- Only the base revision `71851d63…` was measured, as the item specifies; the round-41
  implementation commit was not exercised here.
- Traces were consulted only for `mkdir`; no `chdir` trace was taken, so the 1152 relative
  component calls are attributed to the census work root by the absolute `mktemp` creation
  in the same trace, not by resolved paths.
- No build/lint/test commands beyond the four script invocations; no package, service, mount
  or `/etc` change; no `sudo`; no tool installs. Lane content untouched except this seat's
  report and receipt directory.

## Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-41/w1/RoutedSelfAssessScratch/`:
`old.json`, `old2.json`, `new.json`, `new-tmpdir.json`, `script.diff`,
`script-sha256.txt`, `trace-old.tmp-lines.txt`, `trace-old2.tmp-lines.txt`,
`trace-new.tmp-lines.txt`, `trace-new-tmpdir.tmp-lines.txt`, `metadata.txt`.
Scratch (`/fast/scratch/hyaku/tsukuroi-r41/RoutedSelfAssessScratch/`, including the 8-9 MB
strace files) was removed after the receipts were copied.
