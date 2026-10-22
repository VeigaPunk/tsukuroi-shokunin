# RerunC1Battery — round 28 wave 1, C1 measurement rerun

Verdict: C1 holds. The declared values reproduce exactly: 19 of 24 should-fail mutants accepted by the old counter at `dd94cb1f`, 0 of 24 accepted by the new counter at `f8e3a8f2`, `control_live_anchored_rows` 6 exit 0 in every run, on both data bases.

## Runs (all exit 0; each run prints one JSON summary line, quoted verbatim)

1. `--base f8e3a8f2 --counter-rev f8e3a8f2` (tip data, new counter):
   `{"summary": "mutants-adjacency-overlap", "base": "f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0", "counter_rev": "f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0", "counter_sha256": "450b020b0bae5e1f43e77303f4e726f6c3a7e15e5d7e9b34b9d9a21bc0faf25e", "control_live_anchored_rows": 6, "control_live_exit": 0, "should_fail_total": 24, "should_fail_accepted": 0, "accepted_mutants": [], "should_pass_accepted": 4}`

2. `--base f8e3a8f2 --counter-rev dd94cb1f` (tip data, old counter):
   `{"summary": "mutants-adjacency-overlap", "base": "f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0", "counter_rev": "dd94cb1f", "counter_sha256": "4d992f83f1868a61d01ce77d5f91964ceb266dec52add3fb8b360b4d10a1d690", "control_live_anchored_rows": 6, "control_live_exit": 0, "should_fail_total": 24, "should_fail_accepted": 19, "accepted_mutants": ["wrong-class-and-owner", "lane-quote-from-register", "lane-quote-from-ufo-report", "lane-quote-from-mori-snapshot", "quote-line-at-heading", "quote-window-crosses-section", "six-lane-gap", "lanegap-class-with-lane-side", "one-char-lane-quote", "one-word-sibling-quote", "fabricated-snapshot-other-path", "fabricated-snapshot-pin-name-variant", "other-real-mori-file", "extra-row-ov7", "extra-row-id-trailing-space", "extra-non-dict-rows", "snapshot-field-bogus", "province-ids-in-code-fence", "province-contradicts-register"], "should_pass_accepted": 0}`

3. `--base 3b9e0430 --counter-rev f8e3a8f2` (round-base data, new counter):
   `{"summary": "mutants-adjacency-overlap", "base": "3b9e0430b88d01415c241dd5a18b8939b8a520ac", "counter_rev": "f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0", "counter_sha256": "450b020b0bae5e1f43e77303f4e726f6c3a7e15e5d7e9b34b9d9a21bc0faf25e", "control_live_anchored_rows": 6, "control_live_exit": 0, "should_fail_total": 24, "should_fail_accepted": 0, "accepted_mutants": [], "should_pass_accepted": 4}`

4. `--base 3b9e0430 --counter-rev dd94cb1f` (round-base data, old counter):
   `{"summary": "mutants-adjacency-overlap", "base": "3b9e0430b88d01415c241dd5a18b8939b8a520ac", "counter_rev": "dd94cb1f", "counter_sha256": "4d992f83f1868a61d01ce77d5f91964ceb266dec52add3fb8b360b4d10a1d690", "control_live_anchored_rows": 6, "control_live_exit": 0, "should_fail_total": 24, "should_fail_accepted": 19, "accepted_mutants": ["wrong-class-and-owner", "lane-quote-from-register", "lane-quote-from-ufo-report", "lane-quote-from-ufo-report" duplicate-quoted-name-truncated: same 19 names as run 2], "should_pass_accepted": 0}`
   (The 19 accepted-mutant names are identical to run 2; see run 2 for the verbatim list.)

## Direct checker runs

5. `python3 tools/check-adjacency-overlap.py --revision f8e3a8f2... --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin` → exit 0, output `{"revision": "f8e3a8f2...", "anchored_rows": 6, "expected_rows": 6, "sibling_check": "sibling-verified", "rows": {"OV1".."OV6": []}, "shape_errors": [], "status": "PASS"}`. The live register keeps its count under the new counter.

6. `python3 tools/check-adjacency-overlap.py --selftest` → exit 0, `{"cases": 36, "failed": 0, ...}` — all 36 selftest cases pass.

## Findings

1. Declared after-value confirmed: `should_fail_accepted` 0 of 24 with `counter_sha256` `450b020b…f25e` (the `f8e3a8f2` counter), `accepted_mutants` `[]`, control 6 exit 0 — identical on both bases. [obs]

2. Declared before-value confirmed: `should_fail_accepted` 19 of 24 with `counter_sha256` `4d992f83…d690` (the `dd94cb1f` counter), the same 19 names on both bases. Matches the declared "19 of 24 before". [obs]

3. `control_live_anchored_rows` is 6 with `control_live_exit` 0 in all four battery runs, and the direct `--revision` run gives `anchored_rows` 6 `status` PASS `sibling-verified`. The live register keeps its count. [obs]

4. [inf] The result is data-base invariant: identical counters-by-sha and identical accept sets on `3b9e0430` and `f8e3a8f2` data, so the before/after delta is attributable to the counter bytes alone, not to the data revision.

5. [obs] Side observation, not in the claim: `should_pass_accepted` is 4 under the new counter and 0 under the old — the new counter additionally accepts four should-pass shapes (e.g. `register-utf8-bom` exit 0 rows 6 both roots) that the old counter rejected; conversely the old counter let through 19 should-fail shapes. No should-pass shape regressed under the new counter. [inf] This strengthens, not weakens, C1.

6. [obs] One should-pass shape stays rejected under the new counter: `crlf-snapshot` fails with `sibling-path-not-pinned` (exit 1, 5 rows) in both roots on both bases; `heading-trailing-space-in-row` (marked kind `should-pass?`) fails `heading-not-nearest`. These are battery labels, not the claimed axis; noting for completeness.

Scope: read=SCORECARD.md round-28 declaration, exported tree tools, battery summary lines; wrote=.ufo/waves/round-28/w1/RerunC1Battery.md; executed=git archive (read-only export) to /fast/scratch/hyaku/tsuku28/RerunC1Battery/tree; 4× mutants-adjacency-overlap.py runs, check-adjacency-overlap.py --revision, --selftest; all battery writes confined to its mkdtemp.

Model: not exposed

Installs: none
