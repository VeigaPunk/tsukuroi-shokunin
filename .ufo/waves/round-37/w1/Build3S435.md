# Build3S435 — build:S4 PATH canary design (round-37 w1)

Seat: executor (L2 leaf). Axis: operability / C1 (probe V8). Milestone: Independent runnable design.
Item: build/check design item 3/12 — S4 PATH canary.

## Design summary

A hermetic, runnable canary (`s4-path-canary.py`, stdlib-only) that imports the
committed round-36 probe's own source-channel scanner
(`tools/probe-child-env-allowlist-r36.py`, frozen VERSION 7,
sha256 `a2a5acac…` — matches the W2RevCounter receipts) and runs it over fixture
targets in a private `mktemp` workdir. Fixtures replicate the W2RevCounter S4
variant shape (`zzv-gpexec.py`, `.ufo/waves/round-36/w2/W2RevCounter/variants.json`):
a child environment built by `os.pathsep.join(os.get_exec_path())` and exec'd by
absolute path (`/usr/bin/git --version`). A second fixture (`os.environ` builder)
is a regression guard: it must stay flagged by both baseline and patched scanners.

Patch proposal (precise, `patch-proposal.diff`): add `'get_exec_path'` to the
probe's `OS_AMBIENT` frozenset (line 782). This makes the existing
`ast.Attribute` branch (lines 980–982) emit `ambient-read .get_exec_path`, and
the `from os import get_exec_path[ as …]` branches (lines 972–975, 988–989)
flag aliased imports too. A sweep of `tools/` for `get_exec_path` finds zero
occurrences today, so the addition creates no false positive on the current
tree.

## Observed behavior (exact evidence in seat dir)

- `run-baseline.json`: **baseline** scanner returns `[]` findings on
  `fixture_s4.py` (`s4_missed: true`) — the check **FAILS on unchanged baseline**
  (exit 1). Probe sha256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a`.
- Same file, patched bytes: `OS_AMBIENT` includes `get_exec_path`;
  findings = `["tools/fixture_s4.py:5 ambient-read .get_exec_path"]`;
  environ guard still caught (`…:5 ambient-read .environ`). Verdict
  `after_state_measured: true`.
- `run-after-patch.json`: `--check after` exit 0 (after-state holds).
- `run-before.json`: `--check before` exit 0 (baseline defect reproduced as expected).

## What the after-state measures

The source channel reading > 0 on any target whose child environment is built
from `os.get_exec_path()` — i.e. the S4 backstop (“fixed-PATH ambient-copy
mutants are caught by the names/quiet strace channels **and the source
channel**”, probe docstring lines 42–44) becomes real instead of a docstring
claim. Combined with the already-committed names/quiet dynamic receipts
(W2RevCounter variant 6: 2 leaks), the S4 leak is no longer invisible on any
channel. The untraced view remains uninformative for absolute-path execs by
design, but is no longer load-bearing for PATH.

## Cited sources (all opened this round)

- `.ufo/waves/round-36/w2/W2RevCounter/W2RevCounter.md:164–187` (S4): “`os.get_exec_path()` returns the ambient PATH and is **not** in `OS_AMBIENT` (`environ`, `environb`, `getenv`, `getenvb`), so the source scan reads clean on the most natural ambient-PATH read.” Also :263 variant 6 row.
- `tools/probe-child-env-allowlist-r36.py:782` (OS_AMBIENT), `:103–104` (source-channel docstring), `:980–982` (Attribute branch).
- `.ufo/waves/round-37/w1/C13S403.md` (sibling S4 counter) — supports scope, no experiment duplicated.
- `/home/vgpnk/.omp/agent/RULES.md` — tooling authorization read; no installs performed (no pacman, no channel record needed).

## Constraints honored

No git/jj writes anywhere (fixture Git intentionally unused — stronger than the
“outside a mktemp fixture repo” bound, so no top-level verification was needed);
lane read-only except this seat's outputs; no pacman/host changes; no
delegation; no campaign tools.

## Risks / blockers

- Canary validates the source-scan half of S4; the dynamic names/quiet catch is
  inherited from committed receipts, not re-run (no strace battery executed
  here). Zero strace dependency keeps the canary fast and harness-free.
- Other unflagged ambient-PATH readers (`shutil.which`, fragment-based reads)
  remain documented scan limits (W2RevCounter residual risk, :291–292); out of
  S4 scope. No blockers.
