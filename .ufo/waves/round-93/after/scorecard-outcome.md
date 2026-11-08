## Round 93 — measured outcome (instruments `6b4c53d1…`/`ddd7e955…`/`d0c3d3e7…` at the freeze `c633f49a`; receipts at the landing commit)

| Claim | Axis | Before → after (counting command) | Target | Verdict |
|---|---|---|---|---|
| C1 (measured; surface: the battery's era/refusal sampling) | depth 8 → 8 (tied lowest; a sharper sourced arm) | `python3 tools/limine-pin-battery-r93.py --gate tools/check-limine-pins.py --runs 3 --json OUT` → `96/96 met` ×3, 0 error rows (`.ufo/waves/round-93/after/c1-canonical.json`, `after/clone-gate.json`, `after/clone-bend-N0*.json`); the r92 battery has none of the four families (`grep -c` = 0, `after/do-nothing-roster.txt`); bends `--runs 3` each: N01 `95/96 unmet` failed `ERA-EXACT-125`, N02 `88/96 unmet` failed `ERA-B-FIRST-BODY` (+7 collateral), N03 `95/96 unmet` failed `ERA-B-U1`, N04 `95/96 unmet` failed `REFUSAL-VERSIONS`, 0 error rows in all 12 runs (`after/bend-N0*.json`, `after/bend-family-matrix.txt`); the clone legs at the freeze commit read the same (`w1/ExecReplicate/` cross-check, `after/clone-*` x3) | 96/96 ×3 both layouts; N01-N04 unmet ×3 both with the named family; 0 error rows | **met** |
| C2 (measured; surface: the gate's era-selection input) | operability 9 → 9 (assurance arm; capability `installed-version-probe` enters) | `python3 tools/limine-pin-battery-r93.py --gate tools/check-limine-pins.py --runs 3 …` → the three auto families 4/4 each in every canonical run, 0 error rows; clone leg at the freeze tip: `96/96 met`, auto families 4/4, N05 `unmet` ×3 (`AUTO-ERA-B` alone), N06 `unmet` ×3 (`AUTO-PROBE-FAIL` alone) (`w1/ExecAutoReplicate/{c2-gate,n05,n06}.json`; the clone gate x3 is `after/clone-gate.json`); `python3 tools/check-limine-pins.py --live --limine-version auto` → rc 1, `limine_version 12.9.4`, `limine_version_source probe`, `visibility_era pre-12.9.5`, findings lines 30/38 (`after/live-c2.json`, `/boot` digest `cmp`-identical) | auto families met ×3 both layouts; N05/N06 unmet ×3 both with the named family; live probe fields | **met** |

Capability row (AXES.md §Capabilities; it entered only after a real inventory run):

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| installed-version-probe | The Limine gate can answer the era from the installed bootloader instead of a hand-typed flag: `--limine-version auto` runs `limine --version` read-only (5 s timeout, first `X.Y.Z`), records the value and `limine_version_source`, and refuses (rc 64, empty stdout) on every probe failure; a live host run reads 12.9.4/probe and will flip with the pending 12.9.4-1 → 12.9.6-1 upgrade | `python3 tools/check-limine-pins.py --live --limine-version auto`; `tools/limine-pin-battery-r93.py` AUTO families; `w1/ExecLive.md` (syscall trace) | round 93 |

Falsified-or-narrowed this round (all recorded in `.ufo/plans/round-93.md`): A1 narrows the C2
control sentence (`AUTO-PROBE-FAIL` passes on a gate that refuses every `auto` value; N06 is its
discriminator); A2 narrows C1-1 (N02 is a suppressed cut, not a one-line-late one), C1-2 (the tenth
refusal member is X.Y.Z-shaped above the gate's 1-9-digit bound), C1-3 (empty-or-whitespace-only
stdout), C2-1 (the battery certifies the result, the live trace certifies the mechanism) and C2-2
(the certified probe-failure shapes); A3 narrows C2-3 (the live rc-1 receipt is the L1/root run; the
unprivileged run prints the same fields with rc 2), C2-4 (the parse is "first X.Y.Z after `limine`"),
C2-5 (the timeout is exercised by ExecLive, not the selftest row) and adds C1-4 (the ×3 clone bend
receipts). Axes now: depth 8, coverage 9,
operability 9, freshness 9, calibration 9, adjacency 8 (unchanged). No retirement. No axis harmed:
the 89 r92 families still pass (they are inside the 96), and era-A answers are unchanged (the same
ERA-DEFAULT/ERA-FLE-PANIC-A families pass).
