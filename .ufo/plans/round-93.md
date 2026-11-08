# Round 93 — frozen declaration, narrowings and honest stops (tsukuroi lane)

Frozen at the round-93 freeze commit (this file, `SCORECARD.md` "Round 93 — declaration",
`.ufo/waves/round-93/claims.json`, the two instruments, the six one-clause bends, the two
do-nothing controls and the freeze manifest all land in the same commit). Nothing here is edited
after the first candidate score; a later narrowing is an appended amendment section that names what
it narrows.

Inputs read first: the round-92 closure (MANIFEST `rounds[]`, tsukuroi r92, `admitted`, verification
`round-92-verifier-spotcheck.md@7793773a`) and that spot-check's §6 routed defects 1-5; the round-92
lesson M1-M6; `corpus/QUALITY.md` 124-135; `corpus/README.md` round-92 Frontier (the r92 named
limits: 12.9.5-exact boundary, first body line after the cut, era-B U1, `N04-accept-any`'s
family-level survival, and the launcher's residual channels); the r92 `claims.json` A7 §5 pointer.
The lane's fresh-start round is r91 (Amendment 58/62): r91 and r92 are admitted, so no
post-fresh-start rejection stands.

## Claims (2; distinct axes; causally separable)

**C1 — depth 8 (tied lowest non-retired axis with adjacency 8).** Surface: the `limine-pins`
battery's era/refusal sampling. The r92 battery names three era limits it does not sample — the
exact `12.9.5` boundary (12.9.5 is passed only to a family whose answer is era-invariant), a
visibility-sensitive key on the FIRST body line after the era-B cut, and era-B U1 — and its
survivor `N04-accept-any` (the version refusal deleted) passes every family because every family
uses an in-range version (r92 `claims.json` C2, "Named limits"; r92 A5/A7).

Predicate (the same sentence is in the battery docstring's C1 paragraph and in the receipts):
`tools/limine-pin-battery-r93.py --gate G --runs 3` carries, on fixtures generated fresh per run,
four families the r92 roster did not have — `ERA-EXACT-125` (the version is exactly `12.9.5`; a
first-line-entry config's `hash_mismatch_panic: no` is invisible, so its mismatch pin's consequence
is `panic`), `ERA-B-FIRST-BODY` (12.9.6; a `hash_mismatch_panic: no` key on the line immediately
after the first entry label is invisible, so the mismatch consequence is `panic`), `ERA-B-U1`
(12.9.6; an unhashed efi image line inside an entry body appears in `unverified_image_lines`) and
`REFUSAL-VERSIONS` (each of ten values outside `X.Y.Z` exits 64 with empty stdout and no verdict) —
and against the landed gate the whole roster reads `96/96 met` in each of three runs in the
canonical lane and in a `git clone --shared`, while each of the four one-clause gates N01 (era
split strict), N02 (era-B cut one line late), N03 (U1 restricted to the pre-cut text in era B) and
N04 (version refusal deleted) reads `unmet` in each of three runs in both layouts with its named
family in `failed_families` and zero `error` rows.

Target: landed gate `96/96 met` ×3 both layouts; N01 `failed_families` contains `ERA-EXACT-125`;
N02 contains `ERA-B-FIRST-BODY`; N03 contains `ERA-B-U1`; N04 contains `REFUSAL-VERSIONS`; each
×3 both layouts; every case row has `error: null`.

Kill rule: `unmet` if any landed-gate run reads below 96/96; `unmet` if any named bend does not
read `unmet` in all three runs in both layouts; `unmet` if the named family is absent from that
bend's `failed_families` in any run; `unmet` if any case row carries a non-null `error`; void if
any instrument byte differs from `.ufo/waves/round-93/before/freeze-manifest.sha256`
(`sha256sum -c`).

Counting command:
`python3 tools/limine-pin-battery-r93.py --gate <GATE> --runs 3 --work <scratch> --json <out>`
then `python3 - <<'PY'` counting `failed_families` and `error` rows per run (recipe in
`.ufo/waves/round-93/before/controls/count-runs.py`).

Do-nothing controls (committed with the freeze): (a) the r92 battery `aef33925…`
(`before/controls/do-nothing-battery-r92.py`) has none of the four families — `grep -c` over its
roster is 0, so the pre-change instrument cannot reach the target; (b) the battery's own
`constant-healthy` selftest gate reads 0/96 on the r93 roster (no family is satisfiable by a
constant answer), and each bend's kill is the anti-vacuity control for its family.

**C2 — operability 9 (assurance arm; capability acquisition).** Surface: the gate's era selection
input. The r92 gate takes `--limine-version X.Y.Z` only, default `12.9.4`; Arch `extra` already
ships `12.9.6-1` (r92 ScoutUpstream) and a hand-typed default after an upgrade silently applies the
wrong rule. The r92 launcher probe (A6) additionally names argv/fingerprint residuals that are
recorded, not claimed here.

Predicate: `tools/check-limine-pins.py --limine-version auto` resolves the installed bootloader by
running `limine --version` read-only (PATH lookup, 5 s timeout, the first `X.Y.Z` in its output),
records the resolved value in JSON `limine_version` and its origin in
`limine_version_source: "probe"`, selects the visibility era from that value, and refuses (rc 64,
empty stdout, no verdict) when the probe fails; the r93 battery's `AUTO-ERA-A` (a fake `limine`
answering `12.9.4` selects era A), `AUTO-ERA-B` (a fake answering `12.9.6` selects era B) and
`AUTO-PROBE-FAIL` (a fake exiting 1 must be refused) families, whose inputs are committed fake
`limine` scripts under the case directory on `PATH`, read `met` in each of three runs in the
canonical lane and in a `git clone --shared`; the one-clause gates N05 (a probed version is not
used for era selection) and N06 (probe failure falls back to `12.9.4`) read `unmet` in each of
three runs in both layouts with `AUTO-ERA-B` and `AUTO-PROBE-FAIL` respectively in
`failed_families`; and `python3 tools/check-limine-pins.py --live --limine-version auto` on this
host prints `limine_version` `12.9.4` with `limine_version_source` `probe` (rc 1, the two
operator-owned pin mismatches at `/boot/limine.conf` lines 30 and 38).

Target: the three auto families `met` ×3 both layouts; N05/N06 `unmet` ×3 both layouts with the
named family; the live JSON's `limine_version` equals `limine --version`'s first `X.Y.Z` and its
source is `probe`; 0 `error` rows.

Kill rule: `unmet` if any auto family fails in any run; `unmet` if N05 or N06 does not read `unmet`
with its named family in `failed_families` in all three runs in both layouts; `unmet` if the live
JSON's source is not `probe` or its version differs from the probed binary's answer; void if any
instrument byte differs from the freeze manifest.

Counting command:
`python3 tools/limine-pin-battery-r93.py --gate <GATE> --runs 3 --work <scratch> --json <out>`
(family filter recipe in `count-runs.py`), and
`python3 tools/check-limine-pins.py --live --limine-version auto` (live receipt).

Do-nothing control: the r92 gate `35c1088b…` (`before/controls/do-nothing-gate-r92.py`) rejects
`auto` with rc 64, so all three auto families fail on it — measured, not asserted.

C1 and C2 are causally separable: C1 reads the four era/refusal families and N01-N04; C2 reads the
three auto families, N05/N06 and the live receipt. A round that landed only the families, or only
the probe, would still measure its own claim.

## Named limits (frozen, not claimed)

- `REFUSAL-VERSIONS` certifies that ten out-of-range spellings exit 64 with empty stdout; it does not
  certify that each is refused for the same internal reason (all pass through
  `parse_limine_version`).
- `auto` is explicit, never a default: `--limine-version` still defaults to `12.9.4` (the host
  package) and `--live` probes only when `auto` is passed. The capability is available, not
  defaulted; changing the default is a later round's claim.
- The fake `limine` is a case input on the case's `PATH`. The probe's own PATH sensitivity is what
  the fakes certify; a gate that hardcodes `/usr/bin/limine` fails `AUTO-ERA-B` here (observed by
  N05? no — by the landed gate's probe), and the probe's 5 s timeout and first-`X.Y.Z` parse are
  certified by the gate's selftest rows (`probe-version`), not by a battery family.
- Versions after `12.9.6` still map to V2's rule (r92 limit, unchanged).
- The r92 launcher's residual channels (argv via `/proc`, host fingerprint, writable gate-copy
  parent, `/dev` writes) are recorded in r92 A6 and are not claimed here.
- `N07`-style bends for the two new auto families beyond N05/N06 are not built: the two bends are
  the minimum that falsify this predicate's stated clauses.

## Amendments (appended after data; never an in-place rewrite)

(none yet)
