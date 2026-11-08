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

## Wave summary

13 seats dispatched in one v1 wave (8 executors/reviewers/scouts/critics/mutators +
2 connectors + 1 scribe + 1 planner-held-by-L1). Attack seats: 4 (MutGate, MutBattery,
CriticForgers, CriticClaims) = 31% ≥ 25% required. Connectors: 1 (ConnectorOverlap) ≤ 2.

Key findings:
- ReviewGate: S1 JSON sanitize (fixed), S2 selftest coverage gap (routed), S3/S4 INFO.
- ReviewSource: all battery clauses V1/U1/R6/R9/R10 confirmed against pinned v12.9.4
  sources; two precision notes folded into C2 entry.
- ExecLints: registry coverage FAIL on frozen revision (fixed by SKILL.md row addition);
  selftests 25/25 + battery selftest 5/5 PASS.

## Before→after

- Battery families: 73 (r90) → 82 (r91), +9 (V1 visibility ×4, U1 unverified ×5).
- Gate fields: +`unverified_image_lines`, `hash_mismatch_panic`/`measured_boot` scoped
  to global section.
- Controls: K1/K2/N01-N10 all correctly discriminate in canonical + clone layouts.
- Census: 53 → 56 `^tsukuroi` lines (3 new W04 duplicate-url warnings from S374-S376
  sharing URLs with before/src/ pins — expected, same URLs different snapshot dirs).

## Frontier

- C1 measured outcome: battery 82/82 met in both layouts (canonical + `git clone --shared`).
- C2 exploratory: knowledge entry + JSON sidecar committed; S374-S376 registered.
- Lesson: selftest coverage gap is a known limitation; battery is the frozen target.
