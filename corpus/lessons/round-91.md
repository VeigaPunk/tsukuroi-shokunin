# Round 91 lesson — tsukuroi lane

## Gate

The r91 gate `tools/check-limine-pins.py` repairs the r90 visibility defect (R90-R1):
`hash_mismatch_panic` and `measured_boot` are now read ONLY from the global section
(lines before the first `/` entry line), except when the file's first line is itself
an entry line (config.c 642-650: the buffer cut is skipped when `c == config_addr`).
It also adds `unverified_image_lines` — the image line of an efi chainload entry whose
value is not a pin URI — reporting the silent no-shape fail that `uri_resolve` returns
false for without a `URI_ERROR` message.

## Mistakes

- **S1 (ReviewGate, FIXED):** `measured_boot.value` and `hash_mismatch_panic.value` were
  emitted raw into JSON output; a non-UTF-8 byte survives as a lone surrogate under
  `errors="surrogateescape"` and breaks strict JSON consumers. Fixed by applying
  `sanitize()` to both fields at output (commit `45ae6518`).
- **S2 (ReviewGate, routed):** the gate's `--selftest` has zero V1/U1 coverage — all 25
  cases are r90 rules. The battery covers V1/U1, but a future "whole-file" regression
  would pass the selftest silently. Proposed patch exists at
  `.ufo/waves/round-91/w1/ReviewGate/patch-selftest-coverage.diff`; routed to QUALITY.md
  as a known gap (selftest is smoke-only, battery is the frozen target).
- **S3 (ReviewGate, INFO):** dead `pass` block in the V1 guard was removed (commit
  `45ae6518`); the actual flip happens at the `in_global = False` line.
- **S4 (ReviewGate, INFO):** U1 comment overstated the empty-path case; code was correct
  (`boot():/#<hash>` is a pin, `boot():/` with empty tail is unverified). Comment fixed
  in docstring update.
- **M1 (ScribeLesson, routed): `R91-JUDGE-ORACLE-IMPORTABLE`** — the r91 battery launches
  the gate with `argv=[sys.executable, gate, ...]` (`tools/limine-pin-battery-r91.py:1635`),
  so for a `tools/`-resident gate `sys.path[0]` is the battery's own directory and the
  subject can `import` the judge's `Case` oracle. Measured: `tools/sibling-oracle-forgery.py`
  (receipts in `w1/ScribeLesson/receipts/`) implements none of R6/R9/R10/V1/U1 and still
  reads `82/82 verdict met` rc 0 against the frozen battery; under a bwrap-allowlist
  isolated battery (`receipts/battery-iso-r91.py`) the same forgery reads `0/82 unmet`
  while the landed gate still reads `82/82 met`. C1's 82/82 cannot distinguish an honest
  gate from an oracle-importing one — the count is real but the channel is open. Drafted
  QUALITY 132 in `w1/ScribeLesson/draft-mistakes.md`; the battery-isolation patch
  (`patch-01-battery-isolate-gate.diff`) is proposed, not landed — freezing is already
  committed and re-pinning mid-round would falsify the freeze record.
- **Instrument defects found by the wave (all disclosed in `.ufo/plans/round-91.md`):**
  K2 was a broken control (duplicate `--tpm-present` registration → 984/984 `error:`
  cases; fixed in `6d12e07f`, re-measured 2/82 unmet ×3 canonical + clone); N10 duplicated
  N01 byte-identically (`7e158cd2…`; rewritten as whole-file LAST-wins in `6d12e07f`,
  measured 78/82 unmet ×3 canonical + clone); the freeze
  manifest omits the battery itself and predates `203b3872`/`1652b086`; declaration
  literals (`8f0daee8…` sha, "78 families") describe the r90 instrument, not the frozen
  82-family r91 battery (CriticClaims items 1-2, 8).

## Wave summary

13 seats dispatched in one v1 wave (8 executors/reviewers/scouts/critics/mutators +
2 connectors + 1 scribe + 1 planner-held-by-L1). Attack seats: 4 (MutGate, MutBattery,
CriticForgers, CriticClaims) = 31% ≥ 25% required. Connectors: 1 (ConnectorOverlap) ≤ 2.

Key findings:
- ReviewGate: S1 JSON sanitize (fixed `45ae6518`), S2 selftest coverage gap (routed),
  S3/S4 INFO.
- ReviewSource: all battery clauses V1/U1/R6/R9/R10 confirmed against pinned v12.9.4
  sources; two precision notes folded into C2 entry.
- ExecLints: registry coverage FAIL on frozen revision (fixed by SKILL.md row addition);
  selftests 25/25 + battery selftest 18/18 PASS (spec text said 17 — `LIE_KINDS` has 12).
- ExecReplicate: C1 replicated 82/82 ×3 in clone AND canonical AND at the moved tip
  `2d7e09e1`; freeze manifest `sha256sum -c` clean; `--runs 0`/`-1` exit 2.
- MutGate: 38 held-out gate mutants — 30 killed 3/3, 8 survived = 4 equivalent no-ops
  (whitespace-strip bends the `split_key` already normalises) + 4 undetected bends
  (V1e panic-last-wins, V1n measured-last-wins, R8a empty-label, CONF-a on_panic on
  unreadable conf) — all are battery coverage gaps, routed.
- MutBattery: 31 battery mutants × 12 controls = 312 runs; 4 DETECTED escapes
  (DROP-PANIC-AFTER-PIN frees N01+N10, DROP-FIRST-LINE-ENTRY frees N03,
  NO-ONPANIC-COMPARE frees N02, NO-U1-COMPARE frees N05/N06/N08); only
  PANIC-AFTER-PIN + FIRST-LINE-ENTRY are singly load-bearing r91 families.
- CriticForgers: docstring-only `base.py` met 82/82 ×3; 27 one-clause forgers, 23
  killed, 4 survived as roster gaps (F01 blank-first-line, F04 last-panic-wins,
  F05 exception-measured-only, F06 entry-line boundary).
- CriticClaims: declaration literals falsified (r90 sha `8f0daee8…` and "78 families"
  vs frozen 82-family battery `655ee8f3…`); K2 broken control; N01/N10 byte-identical;
  freeze manifest omits the battery; F2-oracle-import 80/82 and F3-unsorted 82/82
  recorded as battery-discrimination limits.
- ScoutDrift: upstream v12.9.5/v12.9.6 INVERTED the V1 first-line-is-entry exception
  (compiled upstream bytes verbatim; upstream issue #700 confirms 12.9.4 behaviour
  was the bug). Host runs limine 12.9.4-1 → pin stays correct FOR THE HOST; re-pin
  is a round-92 item gated on host upgrade (Arch extra already has 12.9.6-1).
- ScoutURI/ScoutChainload: uri_resolve/chainload semantics confirmed from pinned
  bytes; host receipt's `path:` lines are truncated at 140 cols — only line 72 is
  complete; proposed S377-S379 rows and anchor extensions for S353/S374/S375/S376
  left for the L1.
- ConnectorOverlap: 20-lane sibling sweep, 0 conflicts; found the C2 entry had no
  QUALITY-8 header (gates FAIL at tip) and a falsified `uri_resolve` sentence —
  repaired in `6d181609`; host-build patch-offset probe PASS for uri.c/chainload.c/
  config.c (Arch PKGBUILD sha matches .BUILDINFO; bootstrap touches none of them).
- ScribeLesson: M1 `R91-JUDGE-ORACLE-IMPORTABLE` mined (see Mistakes); QUALITY 132
  drafted; battery-isolation patch proposed not landed.

## Before→after

- Battery families: 73 (r90) → 82 (r91), +9 (V1 visibility ×4, U1 unverified ×5).
- Gate fields: +`unverified_image_lines`, `hash_mismatch_panic`/`measured_boot` scoped
  to global section; S1 sanitize fix.
- C1 measured: 82/82 ×3 `verdict met` in canonical lane, `git clone --shared`, and at
  the mid-wave moved tip `2d7e09e1`; battery selftest 18/18, gate selftest 25/25;
  `--runs 0`/`-1` exit 2.
- Controls after repair: K1 valid (2/82 ×3 both layouts); K2 fixed and re-measured
  2/82 unmet ×3 canonical + clone (`6d12e07f`); N01-N10 each kill their named
  families ×3 both layouts — N10 now a distinct whole-file LAST-wins bend
  (78/82 unmet ×3 canonical + clone; receipts `runs-{canonical,clone}/N10-panic-first-anywhere-fixed.*`).
- Narrowed claims (falsification ledger `.ufo/waves/round-91/claim-falsification.tsv`,
  amendment `.ufo/plans/round-91.md`): C1's 82/82 does not exclude oracle-import
  forgeries (sibling-oracle reads met; F2-oracle-replay 80/82); F3 missing-sort is an
  equivalent mutant (append order already sorted); freeze manifest does not pin the
  battery. C2 entry repaired (header + falsified `uri_resolve` sentence).
- Census: 53 → 56 `^tsukuroi` lines (3 new W04 duplicate-url warnings from S374-S376
  sharing URLs with before/src/ pins — expected, same URLs different snapshot dirs).

## Frontier

- C1 measured outcome: battery 82/82 met in both layouts at the landed tip
  (`20f65353`); narrowed — oracle-import discrimination and freeze-manifest battery
  binding are NOT established (`.ufo/plans/round-91.md`).
- C2 exploratory: entry `limine-unverified-image-r91` + JSON sidecar committed and
  repaired; S374-S376 registered; ScoutURI/ScoutChainload proposed rows (S377-S379,
  anchor extensions) await the L1's decision.
- Round-92 candidates: V1 inversion on limine ≥12.9.5 (ScoutDrift, gated on host
  upgrade); battery oracle-isolation patch + QUALITY 132 (ScribeLesson M1);
  battery coverage families for the MutGate/MutBattery/CriticForgers survivors;
  freeze-manifest battery pinning; selftest V1/U1 coverage (ReviewGate S2).
- Lesson: selftest coverage gap is a known limitation; battery is the frozen target.
