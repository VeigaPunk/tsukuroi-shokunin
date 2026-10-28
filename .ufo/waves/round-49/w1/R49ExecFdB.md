VERDICT: supports

# R49ExecFdB — item C3-B2: the `(R49-C3)` case is not vacuous (with one named limit)

Bytes under test: `tools/tsukuroi-census.sh` at the FREEZE `55c07cd3f8bff2e12117c34d57b4c618de74d85c`,
sha256 `c66144d73da1ac376cfe756eab3a60340e18bce91d60abe24c444408b99a2e75`
(`git -C <lane> show 55c07cd…:tools/tsukuroi-census.sh | sha256sum` == `sha256sum census.base.sh`, both
`c66144d7…`). All work on scratch copies under `/fast/scratch/hyaku/tsukuroi-r49/R49ExecFdB/`; the lane,
its index, the fleet repo and `/tmp` were never written.

Summary of the measurement matrix (all `--selftest`, one run at a time, `env -i PATH=/usr/bin:/bin
LC_ALL=C TMPDIR=<space-free dir> HOME=<dir>`, ~60–130 s per run):

| variant | R49-C3 result line | summary | counter verdict |
|---|---|---|---|
| freeze bytes, direct harness (2 runs) | `PASS … (R49-C3)` in both | 166/167 in both — one *unrelated* case failed (§4) | not run on this harness |
| freeze bytes via counter, `--census-file` copy | `PASS … (R49-C3)` | 167/167 PASS | PASS |
| freeze bytes via counter at `--revision 55c07cd…` | `PASS … (R49-C3)` | 167/167 PASS | PASS |
| M1 delete `ST_BASE_ERR=fd-band` | `FAIL … must name err=fd-band (got '<empty>') (R49-C3)` | 166/167 | FAIL (`band_ok` 0) |
| M2 ignore held descriptor, reuse fd 240 | `FAIL … an exhausted fd band must fail the base resolver (R49-C3)` | 166/167 | FAIL (`band_ok` 0) |
| M3 expected class `alias-open` | `FAIL … must name err=fd-band (got 'fd-band') (R49-C3)` | 166/167 | FAIL (`band_ok` 0) |
| M4 hard-coded PASS, resolver never run | `PASS … (R49-C3)` | 167/167 PASS | **PASS — not caught** |

Receipts (this dir): `r49-c3-runs.txt` (all runs, exact lines), `counter-verdicts.jsonl` (verbatim counter
JSON, six runs), `mutants.diff` (exact mutant edits), `probes.txt` (two direct probes).

## 1. Which assertion each mutant kills

Frozen case body `census.base.sh:3574-3601`; the three outcomes are exclusive branches at 3587-3593.

- **M1** (delete the assignment at `census.base.sh:2091`, keep `return 1`): resolver still refuses, but
  `ST_BASE_ERR` stays empty (reset at `census.base.sh:2079`). Killed assertion: the **err-class branch at 3589**, falling
  through to `bad` at **3592** — observed `got '<empty>'`
  (`r49-c3-runs.txt`, `## m1`: `169:FAIL selftest: exhausted fd band must name err=fd-band (got '<empty>') (R49-C3)`).
  Counter: `FAIL`, `band_ok 0`, `diag_ok` still 1 — `diag_ok` is a source-text grep
  (`check-fd-band-r49.py:92`), and the literal `ST_BASE_ERR=fd-band` survives in the comment at
  `census.base.sh:3576` and the messages at 3590/3592. So M1 is caught **only** by the case, never by
  `diag_ok`.
  M1 also degrades the production fail-fast diagnostic: with a dirty `TMPDIR` and fds 240-249 held, the
  frozen census prints `selftest: fd band 240 241 … exhausted …; no /tmp fallback (R49-C3)`
  (`census.base.sh:2115`) while M1 prints the generic `… cannot host the fixture tree (resolver; no /tmp
  fallback, R48-C2)` (`probes.txt`, probe 2). C3's operability promise ("names descriptor-band exhaustion
  instead of failing silently") therefore dies with M1 on that path too, and `diag_ok` does not see it.

- **M2** (drop the scan and exhaustion return at 2088-2091; `fdn=240`): `exec 240<"$base"` **succeeds on the
  descriptor the case already holds**, silently re-pointing it (`probes.txt`, probe 1: `240 -> /dev/null`
  becomes `240 -> …/dirty fd band`, `rc=0`). Resolver returns 0 with `ST_BASE_DIR=/proc/self/fd/240`, i.e.
  it aliases through a stolen descriptor — the exact silent defect C3 names. Killed assertion: the
  **positive branch at 3587-3588** `bad 'selftest: an exhausted fd band must fail the base resolver
  (R49-C3)'` (`r49-c3-runs.txt`, `## m2`). No misbehaviour beyond that: the case still restores `TMPDIR`/
  `SELFTEST_FD_BAND` (3594-3595) and closes 240/241 (3596-3597), and the run summary stayed `167 cases`.
  The other conjuncts would also have caught it (`ST_BASE_DIR`/`ST_BASE_FD` are left non-empty at 2093-2094),
  but they are never reached because the first branch already fires.

- **M3** (`census.base.sh:3589` expects `alias-open` instead of `fd-band`): resolver returns `fd-band`, so
  the branch is false. Killed assertion: same **err-class branch 3589 → `bad` 3592**, observed
  `got 'fd-band'` (`r49-c3-runs.txt`, `## m3`). M1 and M3 die on the same assertion; they are distinguishable
  only by the interpolated `got` value (`<empty>` vs `fd-band`), which the counter preserves as
  `case_line`.

- **M2 vs M3 distinction.** Both mutants lose; the case reports *different* lines for "the resolver no longer
  refuses" (3588) and "the resolver refuses for the wrong class" (3592). The three functional mutants are
  each caught by exactly one assertion.

## 2. Restore

Pristine bytes, two clean runs through the counter: `--census-file census.base.sh` and the authoritative
`--revision 55c07cd3f8bff2e12117c34d57b4c618de74d85c` (the counter extracts the census into its own scratch)
both returned `{"band_ok": 1,"cases": 167,"stale_ok": 1,"diag_ok": 1,"selftest_rc": 0,"verdict": "PASS"}`
with `TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)` and
`PASS selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)`
(`counter-verdicts.jsonl`). The C3 predicate therefore holds at the frozen bytes on this host. The two
direct-harness runs of the same bytes showed the R49-C3 line PASS but one unrelated failing case each (§4),
so the counter's clean runs are what establish 167/167 as reproducible here.

## 3. Is a hard-coded `(R49-C3)` PASS, with the resolver never run, caught? — **No** (named limit)

M4 replaces the whole 20-line case with one unconditional line
(`mutants.diff`): `ok 'selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)'`.
The census then reports `PASS (167 cases, 167 passed, 0 failed)` and `check-fd-band-r49.py --census-file`
returns `{"band_ok": 1,"cases": 167,"diag_ok": 1,"stale_ok": 1,"selftest_rc": 0,"verdict": "PASS"}`
(`counter-verdicts.jsonl`, `M4-…`: `_rc: 0`) — **the counter cannot distinguish M4 from the freeze bytes**.
Contrast M1, which the same counter fails. Cause, by line:

- `check-fd-band-r49.py:91` `stale_ok` — substring absence of `builds a /tmp fixture tree`.
- `check-fd-band-r49.py:92-93` `diag_ok` — substring presence of `ST_BASE_ERR=fd-band` and
  `fd band %s exhausted` plus `text.count('fd band') >= 2`; satisfiable by comments and an unreachable
  `printf`.
- `check-fd-band-r49.py:104` `case_pass = any(DIAG_CASE in ln and ln.lstrip().startswith('PASS') …)` —
  a *printed string*, not an exercised path.
- `check-fd-band-r49.py:105-107` `band_ok` — `rc == 0 and summary PASS and failed == 0 and case_pass and
  cases == 167`; `113` composes the predicate.
- The `cases == 167` guard is **not** an anti-vacuity witness: replacing the case's branches with a single
  `ok` preserves one outcome per run, so the count stays exactly 167.

Named limit: **`check-fd-band-r49.py` measures that the census *prints* the claim and that the suite totals
167, not that the case executes the resolver; a hard-coded PASS line is accepted.** Exact proposed
tightening (advisory — not applied; the seat is read-only on tracked lane files):

```python
# check-fd-band-r49.py, after band_ok: a behavioural probe, independent of the case line.
# Hold the whole documented band, give the census a TMPDIR the alias cannot name, expect the named failure
# before any fixture work. Measured on the freeze bytes: probe 2 in probes.txt.
def band_probe(src, rundir):
    dirty = os.path.join(rundir, 'probe dirty')       # a space: root_locator_class refuses it
    os.makedirs(dirty, exist_ok=True)
    hold = list(range(240, 250))
    code = ('for n in 240 241 242 243 244 245 246 247 248 249; do eval "exec $n<&0" 2>/dev/null || exit 91; done\n'
            'exec /bin/bash "$1" --selftest\n')
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TMPDIR': dirty, 'HOME': rundir}
    p = subprocess.run(['/bin/bash', '-c', code, 'probe', src], env=env, capture_output=True,
                       stdin=subprocess.DEVNULL, text=True, timeout=300)
    out = (p.stdout or '') + (p.stderr or '')
    named = 'fd band 240 241 242 243 244 245 246 247 248 249 exhausted' in out
    return 1 if (p.returncode == 1 and named and 'TSUKUROI_CENSUS_SELFTEST:' not in out) else 0
```
with `probe_ok` added to the predicate (`… and band_ok == 1 and probe_ok == 1 and cases == 167`). The probe
fails for M1 (`probes.txt`, probe 2: generic `(resolver; …)` message) and for a census that does not run the
resolver at all, while the frozen bytes print the named line and exit 1. A second, cheaper option is to
require `DIAG_CODE` to be absent from comments/labels, i.e. search only the resolver body — that would close
M1's `diag_ok` blind spot but still not M4.

## 4. Risk to counted C3 verdicts: ambient flake in the census selftest (not C3)

Out of six direct `--selftest` runs, three failed **one unrelated case**; out of six counter runs, one showed
two failures. Observed, with exact lines in `r49-c3-runs.txt`:

- `FAIL blocked: memory arm — no cgroup and no journal: no class readable (S7-2): hostname override not
  honoured — possible host read`
- `FAIL healthy: the joined class split is the register AUR-local pair (R9): plane evidence missing:
  'classes=offline-exile:0,aur-local:2'`
- `FAIL healthy: the drift arm pairs /etc warnings by full path; unlogged and gone (R35-C1): hostname
  override not honoured — possible host read`

In every case the R49-C3 line itself was correct. Both shapes are "expected evidence missing from a child
census's captured output", including the banner (`host=` is printed at `census.base.sh:3696`), which points
at fixture/child-output loss under load rather than at the fd-band machinery — `[INFERENCE]`, root cause not
established (host was running ~90 seats, 18/30 GB RAM used). Consequence: `band_ok` can read 0 on a loaded
host for reasons unrelated to C3, so a C3 measurement must quote `case_line`, not the summary alone; the
counter does report `case_line`, which is enough to attribute. This did not affect the freeze-revision run
(clean `167/167`).

## 5. Scope, non-actions, tools

- Files changed in the lane: **none**. Written only `.ufo/waves/round-49/w1/R49ExecFdB.md` and this seat's
  receipt dir. No git/jj mutation anywhere; no `pacman`; no tool installs (bash + python3 used as shipped).
- Not done: root-causing the ambient flake (§4); no second-order mutants of the R48-C2 cases (out of item).
- Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ExecFdB/` removed after copying receipts; `/fast` had 487 G
  free, no ENOSPC.
