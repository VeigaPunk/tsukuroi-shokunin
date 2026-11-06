# Mutants exercised against the three `--selftest` modes

All mutants are byte copies of the file named in `base`, each changed on **one line**
(the changed line is marked `# MUTANT`). They live here so the L1 can re-run them; the
lane's own `tools/` files were never touched.

| mutant file | base | one-line change | selftest rc |
|---|---|---|---|
| `nonauthor-mut1-exemptions-off.py` | `check-nonauthor-label-r85.py` (patched, this dir) | `if EXEMPT_LANE.search(line) or EXEMPT_NEGATION.search(line):` → `if False:` | 1 (FAIL: `red-and-green`, `green-only`) |
| `nonauthor-mut2-site-no-line.py` | same | `"site": f"{path}:{number}",` → `"site": f"{path}",` | 1 (FAIL: `red-and-green`, `mismatched: ["sites"]`) |
| `nonauthor-mut3-empty-census-passes.py` | same | `if not names:` → `if not names and False:` | 1 (FAIL: `results-empty`, rc 0 vs want 2) |
| `hibernate-resume-mut1-exact-match.py` | `tools/check-hibernate-resume.py` (r86 tip) | `return len(tok) >= n and tok[:n].replace("-", "_") == setup.replace("-", "_")` → `return tok == setup` | 1 (FAIL: 10 of 13 cases) |
| `hibernate-resume-mut2-noresume-value-ignored.py` | same | `elif matches(tok, "noresume"):` → `elif tok == "noresume":` | 1 (FAIL: `noresume-valued`) |
| `hibernate-resume-mut3-first-token-wins.py` | same | `val = tok[len(setup):]` → `val = tok[len(setup):] if val is None else val` | 1 (FAIL: `empty-resume-last`) |
| `battery-r86-mut1-family-expectation-flipped.py` | `tools/resume-gate-battery-r86.py` (r86 tip) | `NORESUME-VALUED` want `(1, "DEGRADED", ["HR-NORESUME-ARG"])` → `(0, "HEALTHY", [])` | 1 (FAIL: `const-healthy`, missing `NORESUME-VALUED`) |
| `battery-r86-mut2-findings-comparison-dropped.py` | same | `ok = why == "ok" and got == (want[0], want[1], want[2])` → `ok = why == "ok"` | 1 (FAIL: `const-healthy`, 26 missing families) |
| `battery-r86-mut3-base-unreadable-rc1.py` | same | base-unreadable `return 2` → `return 1` | 1 (FAIL: `base-unreadable`) |
| `battery-r86-mut4-never-met.py` | same | `return 0 if summary["verdict"] == "met" else 1` → `return 1` | **0 (PASS — undetected; defect D2)** |

Battery mutants must be run with cwd = the lane root: the lane battery's `BASE` is
cwd-relative (defect D1), so from any other cwd the `--selftest` crashes before it can
judge anything. `battery-r86-mut4-never-met.py` passes its own selftest because the
selftest has no positive control (every case expects a non-zero rc).

`resume-gate-battery-r86-fixed.py` is the proposed patch (D1 + D2) applied; its
`--selftest` passes from `/tmp` and catches `mut4`.
