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

## Amendment A1 (2026-11-08, after the freeze; controls only) — the C2 do-nothing leg refuses all `auto`
## values, so `AUTO-PROBE-FAIL` passes on it

The frozen C2 do-nothing sentence read "the r92 gate … rejects `auto` with rc 64, so all three auto
families fail on it". Measured (`.ufo/waves/round-93/after/c2-donothing-r92-gate.{json,txt}`, one run):
`families_passed 94/96 verdict unmet failed AUTO-ERA-A,AUTO-ERA-B`, 8 error rows. `AUTO-PROBE-FAIL`
PASSES on the r92 gate, because a gate that refuses every `auto` value satisfies a family that expects
a refusal when the probe fails. The predicate, target and kill rule of C2 are unchanged: the claim
never says the do-nothing fails all three families; only the control sentence did. `AUTO-PROBE-FAIL`'s
discrimination against a silent fallback is N06's leg (probe failure -> 12.9.4), measured separately.
The control sentence is narrowed to: the r92 do-nothing leg proves `AUTO-ERA-A` and `AUTO-ERA-B`
unreachable without V3, and N06 proves `AUTO-PROBE-FAIL` is not vacuous. Lesson M2 records the class
(a refusal-shaped control cannot certify a refusal family).

## Amendment A2 (2026-11-08, after the wave's attack receipts; claim-wording narrowings only) — what
## the wave falsified, and what the claims now say

No predicate arithmetic, target, kill rule or counting command changes; the frozen instruments and
controls are untouched (a byte edit after the freeze would void every receipt). Each narrowing names
the wave artifact that forced it.

**C1-1 — N02's label.** The declaration called N02 "the era-B cut one line late". ReviewBattery F1
and ReviewGate F4 measured the bend's real shape: the replacement
`lineno == first_entry + 1` lives inside the `if stripped.startswith("/")` branch, so the transition
never fires on an entry line and the era-B cut is **suppressed** (on a 12.9.4 config whose first entry
is line 2 the landed gate answers `panic`; N02 answers `prompt` with the key visible). The target
"N02's `failed_families` contains `ERA-B-FIRST-BODY`" still holds; the parenthetical now reads
"N02 (era-B cut suppressed)". The r92 M13 class ("cut one line late") is measured by **no** committed
bend; the corrected bend is routed to the next freeze.
Artifacts: `.ufo/waves/round-93/w1/ReviewBattery/probes-n02-nocut.txt`,
`.ufo/waves/round-93/w1/ReviewGate.md` F4, `after/bend-N02-first-body.json`.

**C1-2 — the refusal set's tenth member.** "Each of ten values outside `X.Y.Z`" is false for
`"9"*5000 + ".0.0"`: that string is X.Y.Z-shaped, and its refusal follows from the gate's published
1-9-digit component cap (`check-limine-pins.py:96`), not from the battery's V2 paragraph
(ReviewBattery F2; MutEra M13 shows a 10-digit component survives the roster). The claim now reads
"nine values outside `X.Y.Z` plus one X.Y.Z-shaped value whose first component exceeds the gate's
1-9-digit bound"; the cap's text and a ten-digit row are routed to the next freeze.
Artifacts: `.ufo/waves/round-93/w1/ReviewBattery/probes-run_usage.txt`,
`.ufo/waves/round-93/w1/MutEra.md` (M13).

**C1-3 — "empty stdout".** `run_usage` asserts `p.stdout.strip() == ""`, so a whitespace-only
refusal output passes (ReviewBattery F3, measured `stdout_bytes=1`, `ok=True`). The claim now reads
"empty-or-whitespace-only stdout"; the landed gate writes nothing to stdout, so no receipt changes.
Artifact: `.ufo/waves/round-93/w1/ReviewBattery/probes-run_usage.txt` (`b_newline_stdout_rc64`).

**C2-1 — the mechanism clause and its certifier.** "Resolves the installed bootloader by running
`limine --version` read-only" is certified by the live run's syscall trace (ExecLive:
`execve("/usr/bin/limine", ["limine","--version"])`, `O_RDONLY` opens only) and the gate's
`probe-version` selftest rows — **not** by the battery's AUTO families: CriticForgers' f6 (a gate
that reads `<cwd>/bin/limine`'s source instead of executing it) reads `96/96 met`. The claim now
splits the two: the battery families certify the observable result (reported version, source, era,
refusal); the mechanism is certified by the live trace and the selftest.
Artifacts: `.ufo/waves/round-93/w1/CriticForgers.md` §3 (`f6.json`),
`.ufo/waves/round-93/w1/ExecLive/strace-gate-live.txt`, `after/live-c2.json`.

**C2-2 — "when the probe fails".** The certified failure shapes are: binary absent (live,
`PATH=/nonexistent` → rc 64, 0 B stdout), nonzero exit with no output (`AUTO-PROBE-FAIL`'s fake
`exit 1`), no parsable stdout (selftest `probe-version`; ExecLive cases c/e), and the 5 s timeout
(selftest/live d: `None` at 5.012 s). The claim does **not** cover: non-UTF-8 stdout (ReviewGate F2:
`UnicodeDecodeError` is uncaught by `OSError/SubprocessError` → exit 1, measured counterexample), a
nonzero exit **with** a version on stdout (MutAuto M04), a two-component probe answer (MutAuto M03),
or the battery observing the 5 s budget at all (M05/M11; M12's 25 s block surfaces as `timeout`
error rows, never as a refusal). The claim now reads: "refuses (rc 64, empty stdout) on the four
certified failure shapes"; the three uncertified shapes are routed to the next freeze as a gate fix
(`errors="replace"`, `(?![\w.-])` suffix guard, a `default` source label) plus families.
Artifacts: `.ufo/waves/round-93/w1/ReviewGate.md` F1/F2, `.ufo/waves/round-93/w1/MutAuto.md`
(M03/M04/M05/M11/M12).

**C2/docstring — the leakage sentence, routed not fixed.** The battery docstring still says
"Fixtures carry no answer … no expected value on disk"; CriticForgers §3 measured it false for the
AUTO families (the fake's literal source encodes the expected version/refusal). The claim does not
repeat that sentence, and editing the frozen battery now would void every receipt, so the docstring
rewording and the decoy-line hardening (`# Limine 12.9.2 (fixture metadata)` before the echo) are
routed to the next freeze.
Artifacts: `.ufo/waves/round-93/w1/CriticForgers.md` §3, `f6.json`.

**Process note — the void leg.** The 14-line freeze manifest verifies 14/14 at `c633f49a`; in the
worktree its `.ufo/plans/round-93.md` line changes only by this file's own permitted appended
amendments (A1, A2). The kill rule's "instrument byte" leg is therefore read against
`.ufo/waves/round-93/before/instruments.sha256` (13 lines, instruments + controls only), which
verifies clean at the landing tip; see ExecBends `freeze-check.txt`, ReviewBattery, MutAuto and
ReviewGate F3, all of which measured the same split.

## Amendment A3 (2026-11-08, from CriticClaims F3/F4/F7; claim-wording narrowings and the missing clone
## leg) — the live parenthetical, the parse clause, and the C1 clone runs

No arithmetic, target, kill rule or counting command changes; the frozen instruments and controls stay
byte-identical.

**C2-3 — the live `rc 1` parenthetical is a privileged receipt.** The frozen predicate said "`--live
--limine-version auto` on this host prints `limine_version` 12.9.4 … (rc 1, the two operator-owned pin
mismatches at lines 30 and 38)". `/boot` is `0700 root:root`, so the lane user cannot read
`/boot/limine.conf`: the unprivileged invocation prints the same `limine_version 12.9.4` and
`limine_version_source probe` with rc 2 `CANNOT-EVALUATE` and `error: conf unreadable`
(`w1/ExecLive/live.stdout`), while the rc-1/pins-30-38 receipt is the L1's root run
(`after/live-c2.json`, `/boot` digest `cmp`-identical, read-only). The claim now states both shapes and
their producers: the root receipt for the pin verdict, the unprivileged run for the fields.
Artifacts: `.ufo/waves/round-93/w1/CriticClaims.md` F3, `w1/ExecLive/live.stdout`,
`after/live-c2.json`.

**C2-4 — the parse clause is "first X.Y.Z after `limine`".** The frozen wording said "the first
`X.Y.Z` in its output". The gate's `probe_limine_version` regex is
`(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b`: the version must immediately follow the word `limine` (optional
`v`). Measured counterexamples (CriticClaims §5): a bare `12.9.6` → `None`; `Limine version: 12.9.6` →
`None`; `gcc 13.2.1` then `Limine 12.9.6` → `12.9.6`; `Limine 12.9.5.1` → `12.9.5`;
`Limine 12.9.6-rc1` → `12.9.6`. The claim now reads "the first `X.Y.Z` immediately following `limine`
(case-insensitive, optional `v`); a bare `X.Y.Z`, a version after other text, or a two-component answer
is a probe failure". The suffix/extra-component leniency is a named limit (routed: add `(?![\w.-])`
and a bare-version family next freeze).
Artifacts: `.ufo/waves/round-93/w1/CriticClaims/evidence.md` §5,
`.ufo/waves/round-93/w1/ReviewGate.md` F1.

**C2-5 — the timeout's certifier.** The declaration's Named limits said the 5 s timeout was certified
by the `probe-version` selftest row; that row tests parse/exit/absent and **not** the timeout. The
timeout is implemented (`timeout=5`, `TimeoutExpired` is a `SubprocessError`) and exercised by
ExecLive's `d_fake_sleep6` probe: `None` at 5.012 s (`w1/ExecLive/probe-isolated.json`). The Named
limits sentence is corrected to name that receipt; no claim number changes.
Artifacts: `w1/CriticClaims/evidence.md` §5, `w1/ExecLive/probe-isolated.json`.

**C1-4 — the clone bend leg is now ×3.** CriticClaims F7 correctly read the clone receipts as one run
per C1 bend. The missing leg is supplied by this round's own clone run at the freeze commit:
`after/clone-gate.json` (landed gate, 3 runs, `96/96 met`) and `after/clone-bend-N0{1,2,3,4}.json`
(3 runs each, `unmet` with the named family, 0 error rows), in addition to ExecReplicate's
one-run-each cross-check. The target "each ×3 both layouts" is now evidenced by committed receipts;
the earlier one-run receipts stay as corroboration.
Artifacts: `after/clone-gate.json`, `after/clone-bend-N01-exact-split.json`,
`after/clone-bend-N02-first-body.json`, `after/clone-bend-N03-era-b-u1.json`,
`after/clone-bend-N04-accept-any.json`, `w1/CriticClaims.md` F7.

**Reading rule for "0 error rows".** CriticClaims F2 and ReviewBattery F5 are right that a usage-family
failure always carries `error: null` (its detail lives in `rows`/`got`), so "0 error rows" is not a
clean-case proof by itself. The claim's clean-case proof is `failed_families` naming the family in every
run plus the `error: null` count; the report and SCORECARD cite both, never the error count alone.

## Amendment A4 (2026-11-08, after data; disclosure only) — the pre-freeze instrument-development smoke

Before the freeze commit (`c633f49a`), the L1 ran the candidate battery once against the candidate
gate during instrument development (`96/96 met`). The run left no receipt, and **no number in this
round's claims is derived from it**: every cited canonical, bend, clone and live receipt was produced
after the freeze and scored the frozen bytes (the 13-line `before/instruments.sha256` verifies clean at
the landing tip). This amendment records the run as instrument development under QUALITY 114
(`R82-FROZEN-CONTROLS`) and QUALITY 73 (`R28-BATTERY-MEASURE`), and lesson M1 records the class.
Artifacts: `corpus/lessons/round-93.md` M1; `w1/ScribeLesson/receipts/02-freeze-manifest-check.txt`
(the freeze/landing hashes).
