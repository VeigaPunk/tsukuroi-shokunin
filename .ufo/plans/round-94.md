# Round 94 — frozen declaration, narrowings and honest stops (tsukuroi lane)

Frozen at the round-94 freeze commit (this file, `SCORECARD.md` "Round 94 — declaration",
`.ufo/waves/round-94/claims.json`, the two instruments, the six one-clause bends, the two
do-nothing controls, the fake-`limine` probe-shape fixtures and the freeze manifest all land in
the same commit). Nothing here is edited after the first candidate score; a later narrowing is an
appended amendment section that names what it narrows.

Inputs read first: the round-93 closure (MANIFEST `rounds[]`, tsukuroi r93, `admitted`, verification
`corpus/lessons/round-93-verifier-spotcheck.md` at `add107e0`) and that spot-check's §6 routed
defects 1-6; the round-93 lesson M1-M4; `corpus/QUALITY.md` 124-138; `corpus/README.md`
round-93 Frontier (the r92 launcher residuals, the probe-leniency note, the `auto`-not-default
limitation, the refusal set's finiteness, and the still-open r89 blanks/ESP/empty-label frontier);
the r93 `claims.json` A2/A3 narrowings. The lane's fresh-start round is r91 (Amendment 58/62):
r91-r93 are admitted, so no post-fresh-start rejection stands. The C2 claim additionally executes
the `auto` live-default recommendation of `corpus/knowledge/limine-version-probe-r93.md` lines 54-61
(the entry's Limits section names the probe as opt-in and the default as `12.9.4`; turning on
`auto` is the action that recommendation asks for), and C1 widens `REFUSAL-VERSIONS` to a "ten-digit
component" (the exact gate text, `tools/check-limine-pins.py:89-96`, caps components at 1-9 digits =
under 1,000,000,000, and the two digit-count adversaries are the 9-digit all-'9's and the 10-digit
`'1' + '0'*9` = 1,000,000,000).

## Claims (2; distinct axes; causally separable)

**C1 — depth 8 (tied lowest non-retired axis with adjacency 8).** Surface: the `limine-pins`
battery's version-refusal sampling and probe-shape certification. The r93 battery's
`REFUSAL-VERSIONS` family (ten values) closes nine out-of-range spellings and one X.Y.Z-shaped value
whose first component exceeds the gate's 1-9-digit bound, but the live `usage_check` roster
(limine-pin-battery-r93.py:2219-2224) proves only the over-bound member and never an in-bound
ten-digit component: the surviving mutant M13 (refusal bound `<= 10`, `MutEra.md:51`, `96/96 met`,
also carried as a `falsifies-wording` row of the r93 ledger) therefore passes every family. The
`AUTO-PROBE-FAIL` family (limine-pin-battery-r93.py:1694-1701) sends only `exit 1` and never the
certified no-parsable-version (`echo "no version here"`) and stderr-only (`echo "Limine 12.9.6" >&2`)
shapes that the gate's own selftest (`probe-version`) and ExecLive's probe-isolated receipts
(`w1/ExecLive/probe-isolated.json`) measure; the r93 declaration named the three uncertified shapes
(non-UTF-8 stdout, a nonzero exit carrying a version, an unanchored two-component probe answer at
length) but never the route that walks the live probe from flagged as certified, and MutAuto's M03
(two-component answer) and M04 (version on a nonzero exit) survive.

Predicate (the same sentence is in the battery docstring's C1 paragraph and in the receipts):
`tools/limine-pin-battery-r94.py --gate G --runs 3` carries, on fixtures generated fresh per run,
two families the r93 roster did not have — `REFUSAL-VERSIONS-10DIGIT` (each of four values —
`12.9.-1`, `12.9.+1`, `+12.9.1`, `12.9.1#` — exits 64 with empty-or-whitespace-only stdout and no
verdict, and the nine r93 out-of-range members are still refused by the same run; the family
exercises the flag API only) and `AUTO-PROBE-SHAPES` (a fake `limine` printing `no version here` with
exit 0, and a fake printing `Limine 12.9.6` to stderr with exit 0, both are refused rc 64 with empty
stdout, and `AUTO-ERA-B` still reads `met` with `12.9.6` on the same gate) — and against the landed
gate the whole roster reads `102/102 met` in each of three runs in the canonical lane and in a
`git clone --shared`, while each of the four one-clause gates N01 (refusal bound `<= 10`, i.e. a
ten-digit component is accepted), N02 (probe regex anchored nowhere after `limine`, i.e. a suffixed
`12.9.6-rc1` and the stderr `Limine 12.9.6` are accepted as `12.9.6`), N03 (refusal bound `<= 11`,
i.e. the live `usage_check`'s ten-digit half becomes unreachable), and N04 (stale-tree reading) reads
`unmet` in each of three runs in both layouts with its named family in `failed_families` and zero
`error` rows.

Target: landed gate `102/102 met` ×3 both layouts; N01 `failed_families` contains
`REFUSAL-VERSIONS-10DIGIT`; N02 contains `AUTO-PROBE-SHAPES`; N03 contains `REFUSAL-VERSIONS-10DIGIT`;
N04 `failed_families` is non-empty; each ×3 both layouts; every case row has `error: null`.

Kill rule: `unmet` if any landed-gate run reads below 102/102; `unmet` if any named bend does not
read `unmet` in all three runs in both layouts; `unmet` if the named family is absent from that
bend's `failed_families` in any run (N04: if it is empty in any run); `unmet` if any case row carries
a non-null `error`; void if any instrument byte differs from
`.ufo/waves/round-94/before/instruments.sha256` (`sha256sum -c`).

Counting command:
`python3 tools/limine-pin-battery-r94.py --gate <GATE> --runs 3 --work <scratch> --json <out>`
then `python3 .ufo/waves/round-94/before/controls/count-runs.py <json> --family
REFUSAL-VERSIONS-10DIGIT --family AUTO-PROBE-SHAPES` (exit 0 iff `verdict met` and 0 `error` rows
in every run).

Do-nothing controls (committed with the freeze): (a) the r93 battery `ddd7e955…`
(`before/controls/do-nothing-battery-r93.py`) has none of the two families — `grep -c` over its
roster is 0, so the pre-change instrument cannot reach the target; (b) the r93 gate `6b4c53d1…`
(`before/controls/do-nothing-gate-r93.py`) reads `96/96 met` on the r93 battery and `100/102 unmet`
on the r94 roster (it answers a verdict for `12.9.6-rc1` and for the stderr fake) but still refuses
a 10-digit component, so the r93 gate cannot reach the target either — measured, not asserted.

**C2 — operability 9 (assurance arm; capability acquisition).** Surface: the gate's era-selection
input. The r93 gate still defaults `--limine-version` to the host-package `12.9.4`
(`tools/check-limine-pins.py`: `ap.add_argument("--limine-version", default="12.9.4")`); Arch `extra`
ships `12.9.6-1` and the host is pinned at `12.9.4` (`pacman -Si limine` here:
`Version : 12.9.4-1`), so a host upgraded without `auto` is still judged under the old era.

Predicate: `tools/check-limine-pins.py` resolves the installed bootloader by default — `auto` is
the default of `--limine-version`, and `--live` probes the installed `limine --version` unless
`--limine-version X.Y.Z` is given explicitly — recording the probed value in JSON `limine_version`
with `limine_version_source` `probe` and selecting the visibility era from that value; a host whose
probe fails is refused (rc 64, empty stdout) rather than answered with the packaged `12.9.4` rule;
and `python3 tools/check-limine-pins.py --live` on this host — with no `--limine-version` flag —
prints `limine_version` `12.9.4` with `limine_version_source` `probe` and era `pre-12.9.5` (rc 1,
the two operator-owned pin mismatches at `/boot/limine.conf` lines 30 and 38; the unprivileged
invocation prints the same fields with rc 2 `CANNOT-EVALUATE` per the A2 C2-3 precedent).

Target: `--live` without the flag on this host prints `limine_version` `12.9.4`, source `probe`,
era `pre-12.9.5`; `--selftest` `PASS 39/39`; the live receipt is byte-consistent with
`limine --version`'s first `X.Y.Z`; 0 `error` rows on the live receipt.

Kill rule: `unmet` if the flag-free live JSON's `limine_version` is not `12.9.4` or its source is not
`probe`; `unmet` if the selftest is not `PASS 39/39`; `unmet` if the live receipt carries a non-null
`error`; void if any instrument byte differs from the freeze manifest.

Counting command: `python3 tools/check-limine-pins.py --live` (live receipt) and
`python3 tools/check-limine-pins.py --selftest` (`PASS 39/39`).

Do-nothing control: the r93 gate `6b4c53d1…` (`before/controls/do-nothing-gate-r93.py`) defaults to
`12.9.4`, so its flag-free live run prints `limine_version` `12.9.4` (identical by value, since the
host is still `12.9.4`) with source `flag` in a fixture where the probe would answer otherwise —
the discriminator is the source field and the fixture divergence, measured in the wave (see Flawed
interpretation §1 below: beam-0 is measured as divergence, never as the flag-free live claim).

C1 and C2 are causally separable: C1 reads the two new families, the four bends and the freeze-manifest
void rule; C2 reads the default's change, the flag-free live receipt and the selftest. A round that
landed only the families, or only the default change, would still measure its own claim.

## Named limits (frozen, not claimed)

- `REFUSAL-VERSIONS-10DIGIT` certifies that the ten-digit enumeration is refused; it does not
  certify that the refusal follows from a length check rather than from a `123456789`-cap or a
  value check (the gate's `int()` normalization is `GGG`).
- The `AUTO-PROBE-SHAPES` family certifies the observable refusal; the mechanism (read-only
  `O_RDONLY`, the 5 s timeout) is certified by the live trace ExecLive receipts, not by the family.
- `auto` is the default, never the absence of a default: `--limine-version auto` is still accepted
  explicitly, `default=` absent no longer exists once `auto` is the default (argparse `default="auto"`).
- The live receipt with the host still at `12.9.4` prints the pre-12.9.5 era; the era flips only
  when the package upgrade lands (operator-owned), which this round does not perform.
- The r92 launcher's residual channels (argv via `/proc`, host fingerprint, writable gate-copy
  parent, `/dev` writes; r92 A6) are recorded and are not claimed here.
- Four new probe-shape toys are committed as `before/fake-limine/` fixtures (four one-line shell
  scripts under `before/fake-limine/` that exist so the `--live`-default path can be exercised
  without mutating `/usr/bin/limine`).

## Amendments (appended after data; never an in-place rewrite)

(none yet)

## Flawed interpretation §1 (L1 read of the r93-routed defects, pre-freeze) — discrimination and
## control seams to be closed in the wave

1. The `AUTO`-fake source leakage (r93 spot-check routed 4; CriticForgers §3 `f6`): a gate that reads
   `<cwd>/bin/limine`'s source instead of executing it reads `96/96 met`, because the faked source
   carries the expected version. The fix is a docstring rewording, a decoy-line hardening (a
   `# Limine 12.9.2 (fixture metadata)` line before the `echo`), and a new probe-shape family whose
   fake does not contain its answer as a literal; the landed battery docstring stops saying
   "Fixtures carry no answer" for the AUTO families.
2. The probe grammar leniency (r93 spot-check routed 5; ReviewGate F1, CriticClaims §5): the
   first-`X.Y.Z`-after-`limine` parse reads `12.9.6-rc1` as `12.9.6`. Fix: an `(?![\w.-])` suffix
   guard after the version (so `12.9.6-rc1` and `12.9.6.1` are probe failures) and a bare-version
   family carrying the statement (the faked `limine` prints `12.9.6` without the word `Limine`).
3. The ten-digit component (r93 spot-check routed 4; MutEra M13): a 10-digit component survives
   `REFUSAL-VERSIONS`. Fix: `REFUSAL-VERSIONS-10DIGIT`.
4. The unfinished `--reference` leg (r93 spot-check routed 3; ExecLints F3): a fresh `--reference`
   run of the r94 battery against the landed gate is owed. Fix: the round runs
   `python3 tools/limine-pin-battery-r94.py --selftest --reference tools/check-limine-pins.py`
   before the freeze is filed, and `--selftest` on the battery at the freeze tip.

## Amendment A1 (2026-11-08, after the freeze; wording only) — the stale-tree decoy's breadth

N04's kill condition was frozen as "`failed_families` non-empty". That bar is too weak as a sentence:
any wrong family satisfies it. The decoy's intent is to forbid a gate that reads a tree default
(`LIM_STD_VERSION`) instead of the probe. N04 (`os.environ.get("LIM_STD_VERSION", "12.9.4")`
assigning `_stale_default`, an unused write) is one write into a stale env default; the witness that
proves the env channel is live is `LIM_STD_VERSION=12.9.6` + `12.9.6-rc1` on `AUTO-ERA-B`. No
predicate arithmetic, target, kill rule or counting command changes; the claim sentence remains
"`failed_families` non-empty" as written in `claims.json`, and this amendment records what the
receipts must additionally show.
