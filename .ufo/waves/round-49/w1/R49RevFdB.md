VERDICT: defect-found

Seat R49RevFdB — item C3-B4, review of the frozen C3 counter `tools/check-fd-band-r49.py`.
Bytes under test: `git -C <lane> show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:tools/check-fd-band-r49.py`
(census at the same revision sha256 `c66144d7…99a2e75`; base census `6256760…` sha256 `375aa737…e2426`).
All citations `path:line` are read at the frozen revision unless marked `base`.
Receipts: `.ufo/waves/round-49/w1/R49RevFdB/` (9 files). Scratch removed; no tool installed.

The C3 claim's own bytes hold and I measured them: the frozen census prints
`selftest: fd band 240 241 242 243 244 245 246 247 248 249 exhausted (…)` on the real exhaustion path,
the stale literal `builds a /tmp fixture tree` is absent (0 hits at freeze, 1 at `tools/tsukuroi-census.sh:415` base),
and the counter passes at the freeze (`167 cases, 167 passed, 0 failed`). The defects below are in the
counter's *discriminating power* and *input trust*, plus one reproducibility gap — not in the census bytes.

## Measurements (my own runs)

| leg | command | result |
|---|---|---|
| freeze, expect PASS | `check-fd-band-r49.py --revision 55c07cd3… --work <scratch>/work-freeze` | `verdict PASS`, `stale_ok 1 diag_ok 1 band_ok 1 cases 167`, `selftest_rc 0`, 1m09s |
| base, expect FAIL/166 | `… --revision 6256760…` | `verdict FAIL`, `stale_ok 0 diag_ok 0 band_ok 0 cases 166`, `selftest_rc 1`, summary `FAIL (166 cases, 165 passed, 1 failed)`, 1m24s |
| mutant M1, diagnostic silenced | `… --census-file <scratch>/census-mutant-m1.sh` | **`verdict PASS`** (`diag_ok 1 band_ok 1 cases 167`), 1m44s |
| provenance bypass | `… --revision deadbeef… --lane /nonexistent/lane --census-file <scratch>/census-freeze.sh` | **`verdict PASS`**, 1m44s |

Base census selftest re-runs (byte-identical input, counter's exact env): 2× `env -i PATH=/usr/bin:/bin LC_ALL=C
TMPDIR=… HOME=… /bin/bash census-base.sh --selftest` → 166/166 PASS both; 1 exact replica of the counter's own
invocation (extract into `work/tools/`, `stdin=DEVNULL`, `capture_output`, same env) → 166/166 PASS (123 s).
So the base row above is a single observed 165/166, not a property of the bytes — see F6.

## Findings, by severity

### F1 (medium) `diag_ok` cannot tell a printed diagnostic from a literal in a comment; the round's "no longer silent" property is unpinned
`diag_ok` is purely textual (`tools/check-fd-band-r49.py:92-93`: `DIAG_CODE in text and DIAG_TEXT in text and
text.count('fd band') >= 2`), and `band_ok`'s only behavioural probe is `--selftest` (`:97-106`), whose `(R49-C3)`
case asserts resolver *state* (`ST_BASE_ERR=fd-band`, empty base/fd — `tools/tsukuroi-census.sh:3586-3596`), never
the message. Fixture M1 replaces the print in `run_selftest`'s `fd-band)` branch (`tools/tsukuroi-census.sh:2113-2116`)
with a comment carrying the same literal:

- freeze census, all of 240-249 held + dirty TMPDIR → `selftest: fd band 240 241 … 249 exhausted (…)`, rc 1;
- M1, same invocation → **0 bytes of output**, rc 1 (the silent failure is back);
- counter on M1 → `band_ok 1, diag_ok 1, cases 167, verdict PASS`.

The four shipped controls do not cover this shape (K1 removes the case, not the print: `controls/battery.py:262-270`).
Recommendation: make `diag_ok` behavioural — run the census with `SELFTEST_FD_BAND` exhausted and a dirty TMPDIR and
require the exact `fd band … exhausted` line on stderr (and that it is absent from a non-exhausted run) — or add a
selftest case that executes `run_selftest` and greps its own stderr.

### F2 (medium, control evidence) `--census-file` bypasses the git read, the BASE check and any provenance, and the receipt repeats the caller's `--revision`
`tools/check-fd-band-r49.py:79-85` uses `a.census_file` verbatim (any path, inside or outside the lane), skips the
`BASE^{commit}` readability check at `:82`, and `:107-112` prints `revision: rev` — the argument, not the bytes read.
Measured: frozen bytes copied outside the lane, `--revision deadbeef…`, `--lane /nonexistent/lane` → `verdict PASS`
(`counter-runs.jsonl` leg 4). Consequences for this round's controls: all four C3 controls ran through
`--census-file` (`controls/battery.py:250`), so `battery-summary-r49-c3.jsonl:1-4` stamps every line with
`"revision": "32a855608aa3ebb19b0602a94cc33bcfda564a61"` although K0 tested *base* bytes and K1/K2 tested fixtures —
a provenance mislabel an auditor cannot see through. Recommendation: require the census file to resolve inside
`--lane` (or add an explicit `--allow-outside-lane`), and emit `census_sha256` + `provenance: "git-archive"|"file"` in
the JSON so a control receipt is attributable to bytes.

### F3 (low-medium, side effect) `--revision` is spliced into git's argv unvalidated: it can write outside `--work`
`tools/check-fd-band-r49.py:64` runs `git archive --format=tar <rev> <path>` with no `--`/validation. Measured:
`--revision=--output=<scratch>/injected.tar` → git creates (truncates) `injected.tar` **outside the work dir**, then the
counter reports `unreadable … verdict FAIL` rc 2. The docstring's `Writes nothing outside --work` (`:29`) is therefore
false, and the same shape admits `--remote=`. Recommendation (measured to work): resolve first with
`git rev-parse --verify --quiet --end-of-options '<rev>^{commit}'` (rejects `--output=…`, rc 1) and archive the
resolved sha with `git archive --format=tar <sha> -- <path>`.

### F4 (low, portability) tar extract path safety is an accident of the interpreter version
`extract()` calls `tf.extractall(dest)` with no `filter=` (`:70-71`). Measured on the host: 3.14.8 raises
`OutsideDestinationError` for `../escape.txt`, `AbsoluteLinkError` / `LinkOutsideDestinationError` for escaping
symlinks (default `data` filter, `/usr/lib/python3.14/tarfile.py:2448`); **3.12.15 and 3.13.16 extract `../escape.txt`
outside the destination with no error**. `python3` on this host is 3.14.8, so today's runs are safe; the code does not
pin it. Recommendation: `extractall(dest, filter='data')` (verified accepted on 3.14). No `.gitattributes`
export-ignore hazard exists at the freeze (`git ls-tree -r <FREEZE> | grep gitattributes` matches only two `.ufo/`
documents); if one were added, the counter fails *loudly* (`extract` returns a path it never wrote, `os.path.isfile`
at `:86` is false → `unreadable at <rev>`, rc 2).

### F5 (low, hygiene) the census child inherits the caller's cwd
`subprocess.run` at `:97-98` sets `env` but no `cwd`. Measured: a `--census-file` that does
`printf 'cwd proof\n' > cwd-write-proof.txt` wrote that file into the *caller's* cwd. Any census under `--census-file`
can therefore write relative paths into the caller's directory (for the controls: wherever the operator stood).
Recommendation: `cwd=rundir`.

### F6 (low-medium, reproducibility) `band_ok` is a single-run all-167-green gate and a failure is unattributable
One base execution through the counter (under ~90-seat host load) returned `FAIL (166 cases, 165 passed, 1 failed)` while three later executions
(2 manual + 1 exact replica) returned 166/166 on byte-identical input; at the base revision the failure did not change
the verdict (base is FAIL either way), but at the freeze one flaky case would flip C3's measurement to FAIL. The
counter's JSON drops every `FAIL` line (`:99-112` keeps only `summary` and the first `R49-C3` line), so a red run at
the freeze cannot be diagnosed from the receipt. I did not reproduce the failure, so the cause is unattributed
(round 48 observed the same class of load sensitivity — `.ufo/waves/round-48/w1/R48Attack11.md:255`). Recommendation:
record `fail_lines` (all `^FAIL ` lines) in the JSON and state the accepted single-run risk, or retry once and record
`attempts`.

### F7 (minor) cleanup claims are optimistic
`shutil.rmtree(work, ignore_errors=True)` (`:118`) silently leaves what it cannot remove — measured: a subtree mode
`000` survived (`leftover: run True, run/sub True`). A normal run does remove the `mkdtemp` dir (also on the
`TimeoutExpired` path: rc 2 + `error: TimeoutExpired…`, work cleaned), but the `--work` parent is always left behind
empty (`work-freeze/`, `work-base/` after their runs). Only the docstring line `:25-27` overstates it.

### F8 (nits, no action required)
`SUMMARY` (`:48`) is anchored and uses `fullmatch`; multi-digit counts parse (`1670` → `('1670','1670','0')`), leading
text does not match, `strip()` tolerates padding. `\d` is Unicode-wide, so `…(١٦٧ cases…)` matches and `int()`
converts it — cosmetic only (the census prints `%d`). `case_pass` (`:104`) requires `lstrip().startswith('PASS')`
with no word boundary, which is correct against the census's own reporters (`ok()` prints `PASS %s`,
`bad()` prints `FAIL %s` to stderr — `tools/tsukuroi-census.sh:2214-2215`), so a failing `(R49-C3)` line can never
satisfy it.

## The item's questions, answered directly

- **`git archive` extraction / `.gitattributes` / export-ignore** — no root `.gitattributes` exists at the freeze, so
  nothing is dropped today; a future `export-ignore` on the census makes the counter fail loudly with rc 2 (fixture
  `fx-attr` in `tar-extract-safety.txt`). Extracted bytes are byte-identical to `git cat-file blob` and the mode is
  0755 (irrelevant: the file is passed to `/bin/bash`, never executed).
- **Path safety of the tar extract** — safe on the host's 3.14.8 by the implicit `data` filter; *not* safe on
  3.12/3.13 (measured writes outside dest), because `filter=` is never passed.
- **`env -i` environment** — sufficient: the frozen 167-case selftest passes with exactly
  `PATH=/usr/bin:/bin LC_ALL=C TMPDIR=<work>/run HOME=<work>`; the census reads no `HOME`/`USER`/`LOGNAME` (0 hits) and
  every binary it touches on that path resolves under `/usr/bin:/bin`. `TMPDIR` exists and is inside `--work`.
- **Does `LC_ALL=C` matter for the summary regex?** — No: `printf '%d'` emits identical ASCII digits under `C`,
  `C.UTF-8`, `en_US.UTF-8`. It *is* protective for a `%'d` grouping flag (`1670` vs `1,670`), which the census does not
  use. Keep it for the census's own collation, not for the regex.
- **`band_ok` requiring `case_pass` with a leading `PASS` after `lstrip`** — correct and well matched to the
  reporters; combined with `selftest_rc == 0`, `summary PASS`, `failed == '0'`, `cases == 167`.
- **Work-dir removal in `finally`** — runs on the normal, timeout and exception paths (measured); `ignore_errors`
  plus the surviving `--work` parent are the only gaps (F7).
- **Can `--census-file` point outside the lane?** — Yes, unconditionally, with the base check skipped and the receipt
  echoing the unverified `--revision` (F2).

## Residual risk and verification gaps

- The 165/166 base run is *unexplained*: it is the one failure in the four base-suite executions I ran myself
  (three passed 166/166 on byte-identical input); the shipped K0 control at dispatch time also passed. Cause not
  captured because the counter discards FAIL lines. The freeze measurement (167/167) is a single run of mine plus the
  K-pass control; reproducibility at the freeze under a loaded host is not established.
- I did not run the counter under `python3.12`/`3.13` end-to-end (only the extraction primitive), and I did not build
  a hostile lane tree (symlink/`export-ignore` census) to exercise `extract()` through the counter itself.
- I did not review the census's own 167 cases beyond the resolver/`R49-C3` path, and I did not attempt the C3-B6
  cheat class (sibling seat); F1 and F2 are narrower and independent of it.
- Nothing here falsifies claim C3 at `55c07cd3`: the diagnostic is printed, the stale comment is gone, the case exists
  and the counter passes. F1–F6 are counter-side defects and control-evidence defects; the honest C3 statement is
  "the frozen bytes name the failure, and the frozen counter cannot tell whether a later revision still does".
