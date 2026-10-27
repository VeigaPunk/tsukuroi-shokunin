VERDICT: supports

# Seat C2MutCases — item C2-5: can the two (R47-C2) selftest cases be weakened into always-pass?

Date: 2026-10-27. Wave w1. Scratch: /fast/scratch/hyaku/tsukuroi-r47/C2MutCases (removed after receipts copied).

## Detector (the frozen C2 counting command, run against scratch copies only)

    S=/fast/scratch/hyaku/tsukuroi-r47/C2MutCases
    mkdir -p "$S/t 2"
    env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" bash $S/census-<variant>.sh --selftest

PASS predicate (per the C2 claim): last line `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)` and exit code 0.

Tested lane bytes: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh
sha256 adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41 (copy byte-identical; lane file never written).

Relevant lane lines: `root_locator_class` 850-866 (whitespace rejection `*[!A-Za-z0-9._/+-]*)` at 862); fixture-base fallback 2055-2058 (pattern at 2057); `work=$(mktemp -d ...)` 2059; R47-C2 pin 1 assertion at 3476 (`[ "$(root_locator_class "$work")" = 'absolute' ]`); fixture `mkdir -p "$work/fx/sp dir/root"` 3479; R47-C2 pin 2 assertion at 3480 (`[ "$(root_locator_class "$work/fx/sp dir/root")" = 'unsafe' ]`).

## Baseline (pristine copy, census-pristine.sh)

    TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed), rc 0

Both R47-C2 cases PASS; the R46-C1 identity/cli cases adjacent to them PASS (see mut-*.log in the seat dir).

## (a) Weaken `root_locator_class` to accept whitespace — is any case a catcher?

Mutation (a) — classifier only, line 862: `*[!A-Za-z0-9._/+-]*)` -> `*[![:space:]A-Za-z0-9._/+-]*)`.
Unit probe before the run (extracted function, pristine vs mutant):
  pristine: `/x y/z` -> unsafe,  `/x root_mode=0755` -> unsafe
  mutant:   `/x y/z` -> absolute, `/x root_mode=0755` -> unsafe (`=` still rejected)
Detector run (receipts mut-a.log):
  FAIL selftest: root_locator_class must refuse whitespace overrides (R47-C2)
  TSUKUROI_CENSUS_SELFTEST: FAIL (164 cases, 163 passed, 1 failed); rc 1  -> KILLED by pin 2.
Pin 1 still passes (fallback at 2057 untouched, so the fixture base lands under /tmp and classifies absolute).

Mutation (a2) — classifier AND fixture-base fallback both whitespace-accepting (lines 862 and 2057):
  FAIL selftest: root_locator_class must refuse whitespace overrides (R47-C2)
  TSUKUROI_CENSUS_SELFTEST: FAIL (164 cases, 163 passed, 1 failed); rc 1  -> KILLED by pin 2.
  Note: pin 1 PASSES even here — a wholesale charset relaxation makes the spaced fixture base classify 'absolute', which is exactly what pin 1 asserts. Pin 1 cannot catch a classifier weakening; that is pin 2's axis.

Mutation (a3) — fallback deleted, strict classifier kept (2055-2058 replaced by `:`):
  FAIL selftest: the fixture base must classify absolute under a dirty TMPDIR (R47-C2)
  TSUKUROI_CENSUS_SELFTEST: FAIL (164 cases, 14 passed, 150 failed); rc 1  -> KILLED by pin 1 (+ 149 sibling cases BLOCKED, the round-46 C1ExecRerunB failure mode).

Answer to (a): yes. Every whitespace/charset weakening on either behavior-bearing point is caught — pin 2 catches classifier weakening (a, a2), pin 1 catches fallback removal (a3). No always-pass weakening exists on this axis.

## (b) Make `work` an empty string — fail or silently skip?

Mutation (b): `work=''` inserted immediately before pin 1 (census-mut-b.sh:3476).
Observed (mut-b.log):
  FAIL selftest: the fixture base must classify absolute under a dirty TMPDIR (R47-C2)
  mkdir: cannot create directory '/fx': Permission denied
  rc 1; the summary line `TSUKUROI_CENSUS_SELFTEST: ...` is NEVER printed (grep count 0).
Mechanics: `root_locator_class ''` prints 'empty' != 'absolute', so pin 1 records `bad` (FAIL count 1) — not a skip. The next line, `mkdir -p "$work/fx/sp dir/root"`, becomes `mkdir -p /fx/...` and fails with EACCES; `run_selftest` runs under `set -e` (restored at 3465), so the selftest aborts before the summary. The counting command's PASS predicate (summary + rc 0) is not met.

Answer to (b): the cases fail loudly. There is no silent-skip path via an empty `work`; the failure is doubly visible (recorded FAIL + abort with rc 1).

## (c) Corrupt the fixture `sp dir` path so it lacks a space — does the unsafe pin still trip?

Mutation (c1): only the fixture creation de-spaced — line 3479 `mkdir -p "$work/fx/spdir/root"`; pin 2 assertion left classifying the literal `"$work/fx/sp dir/root"`.
Observed (mut-c1.log):
  PASS selftest: a space in a root override stays unsafe by design (R47-C2)
  TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed); rc 0  -> SURVIVED.
Mechanics: `root_locator_class` is a pure string classifier — it never stats (by design, comment at 851-854: an override is caller data and the unsafe class is decided before any stat). The assertion tests the string literal, so the on-disk fixture is irrelevant to the pin; the `mkdir -p` at 3479 is decorative with respect to pin 2.

Mutation (c2): fixture and assertion both de-spaced (`spdir` in 3479 and 3480) — the "assertion itself corrupted" control:
  FAIL selftest: root_locator_class must refuse whitespace overrides (R47-C2)
  TSUKUROI_CENSUS_SELFTEST: FAIL (164 cases, 163 passed, 1 failed); rc 1  -> KILLED by pin 2.

Answer to (c): corrupting the on-disk fixture alone does NOT trip the pin (survivor, c1); corrupting the asserted path does (c2). The pin guards the classifier contract on the override string, not the fixture tree.

## Guard-axis map (which pin catches what)

| Regression                                   | Catcher          | Evidence |
|----------------------------------------------|------------------|----------|
| classifier accepts whitespace (a, a2)        | pin 2 (case 3480)| mut-a.log, mut-a2.log |
| fixture-base fallback removed (a3)           | pin 1 (case 3476)| mut-a3.log |
| empty `work` (b)                             | pin 1 + set -e abort | mut-b.log |
| assertion path de-spaced (c2)                | pin 2            | mut-c2.log |
| on-disk fixture de-spaced, literal kept (c1) | none — SURVIVOR  | mut-c1.log |

## Is a third case needed?

No, not on detection coverage. The two pins are complementary and together cover every behavioral weakening I could construct on this contract: pin 1 owns the fixture-base derivation axis, pin 2 owns the classifier axis. All six behavioral mutants (a, a2, a3, b, c2, and the implicit combined forms) are killed; only the cosmetic (c1) mutant survives, and it preserves every behavior the two pins assert — the whitespace-refusal contract is still pinned via the literal override string, which is the actual contract (an override path is caller data; whether a directory happens to exist under the fixture tree is not part of it).

Hygiene finding (not a coverage gap): the `mkdir -p "$work/fx/sp dir/root"` at line 3479 is load-bearing for nothing — pin 2 never looks at the created directory. Either drop the mkdir or bind the assertion to the created path (e.g. classify `"$sp_root"` after `mkdir -p "$sp_root"` with `sp_root=$work/fx/'sp dir/root'`) so the fixture becomes load-bearing. A third selftest case would add nothing beyond this cosmetic binding.

## Restoration evidence

Lane file unwritten throughout; sha256 of /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh before and after all probes: adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41 (unchanged). Scratch copies census-mut-{a,a2,a3,b,c1,c2}.sh retained only until receipts were copied; receipts (mut-*.log, receipts-diffs.txt) are in this seat's directory:
  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-47/w1/C2MutCases/
Mutant diffs vs pristine: receipts-diffs.txt. Scratch dir removed after report write (trap 'rm -rf -- "$S"' EXIT).

## Not done

- No mutation of the lane file; all probes ran on scratch copies.
- I did not probe mutations outside the assigned item (e.g., the 149 sibling cases, the R46-C1 identity cases) except as they were incidentally exercised by the detector logs.
- One selftest run at a time, serialized, per the cost rule (7 runs total: 1 baseline + 6 mutants).
