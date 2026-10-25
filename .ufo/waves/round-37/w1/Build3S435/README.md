# Build3S435 — S4 PATH canary design (round-37 w1)

Independent, runnable design for the round-37 C1 item **build:S4 PATH canary**.
The check is hermetic: it imports the committed round-36 probe's own
source-channel scanner over fixture targets placed in a private `mktemp`
workdir; the only lane file it reads is
`tools/probe-child-env-allowlist-r36.py` (read-only). No git/jj operations are
used at all; no pacman/host changes; no tools installed (Python 3.14 stdlib
only).

## What the canary proves

| state | probe bytes | source findings on `os.get_exec_path()` fixture | verdict |
|---|---|---|---|
| baseline | committed r36 (sha256 `a2a5acac…`, `probe_version 7`) | `[]` — silent | **check FAILS (exit 1)** |
| after | same bytes + proposed V8 patch (1-line `OS_AMBIENT` change) | `tools/fixture_s4.py:5 ambient-read .get_exec_path` | **check PASSES (exit 0)** |

Regression guard: an `os.environ` reader stays flagged by both scanners
(`…:5 ambient-read .environ`), i.e. the patch adds the missing name without
breaking the existing ambient-read detection.

## Files

- `s4-path-canary.py` — the runnable check (stdlib only).
- `patch-proposal.diff` — the precise V8 patch proposal (unified diff, baseline → patched).
- `run-baseline.json` — full observed JSON (both phases + diff + verdicts).
- `run-after-patch.json` — `--check after` receipt (exit 0).
- `run-before.json` — `--check before` receipt (exit 0 = defect reproduced as expected).

## Run

```
python3 s4-path-canary.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
    --scratch /tmp --out-json run.json      # both phases; exit 1 on baseline red
python3 s4-path-canary.py --check after ...  # exit 0 when the after-state holds
python3 s4-path-canary.py --check before ...  # exit 0 when the baseline defect reproduces
```

Exit codes: `0` = measured state holds, `1` = measured state absent (red),
`2` = harness error (probe line moved, fixture scan failure).
