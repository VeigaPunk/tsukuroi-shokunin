# Round-96 plan amendments (the plan bytes are frozen at 38adc4ed; this file is append-only)

### A1 (2026-11-08, before the C2 after-receipt; datum: ExecControls pass 2, R2/R4)

The frozen C2 target sentence "each of its six one-fault fixtures fails exactly its own finding" is
narrowed to "each one-fault fixture fails exactly its own finding **id** (one or more findings of
that id, no other id)". Datum: R2 (one corrupted receipt-hash hex digit) emits two F2 findings —
"receipt hash != current tool" and "the freeze manifest does not pin the receipt hash" — and R4's
over-scope revert can emit one F4 under the pinned line-based bytes; the id set is exactly `{F2}` /
`{F4}` in the receipt. No counter, kill rule or target number changes; "clean fixture: none" and
"selftest 7/7" hold as frozen.

### A2 (2026-11-08, disclosure, no predicate change)

Between 07:47:39 and 07:54:00 the working-tree `tools/check-r96-calibration.py` was `ad894667…`
(a post-freeze whitespace-flattening edit) while `before/instruments.sha256` pinned `7ff63524…`.
Two seats read the drift (ExecDoNothing §4, ExecControls D1) and the L1 restored the pinned bytes;
`sha256sum -c .ufo/waves/round-96/before/instruments.sha256` reads 17 × OK at scoring time. The C2
void clause is evaluated on the manifest bytes; the drift receipts are in the seat dirs. The repair
that makes the pinned checker pass without editing it is a wrap-only reflow of
`tools/make-r95-bends.py` (hash `bbcb18f3…`), not a lane-instrument change.

### A3 (2026-11-08, after the wave's bend receipts, before the report; datum: `w1/ExecBend/bend-N02*.json`, `w1/ExecBattery/c1-bend-N02-y-cap-8.json`)

The frozen C1 target's "each bend ... and 0 error rows" is falsified by N02: the bend refuses the
four Y-family cases (rc 64, empty stdout, no JSON), so the battery records four `error` rows per
run — exactly the shape round 95's A1 recorded for N05. The measured clause is narrowed to: "0 error
rows on every landed-gate and do-nothing leg; on a bend leg, only the bend's own refusal rows, named
and counted (N02: 4 per run; N01/N03/N04: 0)". The frozen numbers (`102/103`, N04 `101/103`, exact
`failed_families`) and every other clause stand. The frozen sentence is left as filed; this is the
QUALITY 140 class miss the round records as `R96-N02-ERRORROWS`, and the report states the raw
error-row counts so the closure can judge the narrowing on the bytes.

### A4 (2026-11-08, after CriticClaims F-2, before the report)

C1's predicate sentence is narrowed: the roster goes 99 → 103 with four names; **three** of them
(`EXPLICIT-VERSION-ECHO`, `EXPLICIT-VERSION-ERA`, `REFUSAL-VERSIONS-9DIGIT-Y`) sample classes the
r95 roster does not; `EXTRA-COMPONENT` re-answers the four-component refusal class the r95 roster
already carries (`REFUSAL_VERSIONS` value `12.9.5.1`) and the r95 instrument's `--usage-check` mode
already sends (`12.9.6.1`), and the r95 roster alone kills its bend (98/99 unmet,
`REFUSAL-VERSIONS`), so it is a twin under QUALITY 136 and the round's measured discrimination delta
is three families, not four. Every frozen number and every other clause stands; the twin stays in
the roster as coverage broadening and is not counted as new discrimination.

### A5 (2026-11-08, after CriticClaims F-3 E1b-E4, before the report)

C2's predicate sentence is narrowed: the checker asserts six **remedy conditions**, one per routed
r95 defect — F1/F3/F4 are substring conditions on the repair text, F2 binds one recorded sha256 to
one tool's current bytes, F5 lints a committed receipt without re-measuring it, and F6 is the only
finding that binds a recorded number (the report's prose count) to committed bytes (the round's own
ledger); F6 binds the FIRST numeric occurrence of each class, so a truthful report that quotes the
r95 wrong count first is rejected (measured E4). The claim is that the six repairs exist, F2's
equality holds on the landed bytes, and F6's count agrees at filing — not that any finding
re-measures an r95 fact.
