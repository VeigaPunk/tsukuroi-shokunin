# ScribeKnowledge — round 96, wave w1 (scoped findings)

Seat: scribe (leaf member, no dispatch). Scope: draft the round's knowledge entry (prose only) and
carry the receipts for it.

- **Draft:** `.ufo/waves/round-96/w1/ScribeKnowledge/knowledge-draft.md` — the draft of
  `corpus/knowledge/limine-bound-per-component-r96.md`, with the frontmatter (`source:`,
  `verified-at:`, `recheck:`), the per-component accepted leg (X and Y), the echoed
  version/source and era field, the four-component refusal with its same-list positive control,
  the r95 Frontier correction (`12.9.5.1` was already sampled), and Limits.
- **Seat report with commands, raw output and the PASS/FAIL table:**
  `.ufo/waves/round-96/w1/ScribeKnowledge/report.md`
- **Receipts:** `.ufo/waves/round-96/w1/ScribeKnowledge/receipts/`

## What this seat measured (own runs, own receipts)

| leg | measured | verdict |
|---|---|---|
| roster | 99 → 103 unique, added exactly `EXPLICIT-VERSION-ECHO`, `EXPLICIT-VERSION-ERA`, `REFUSAL-VERSIONS-9DIGIT-Y`, `EXTRA-COMPONENT`, none removed | PASS |
| landed gate, 3 runs | `met 103/103`, `failed_families []`, 412 cases, 0 error rows, each of the four new families `[4, 0]` | PASS |
| `N01-echo-wrong`, 3 runs | `unmet 102/103`, `["EXPLICIT-VERSION-ECHO"]`, 0 error rows | PASS |
| `N02-y-cap-8`, 3 runs | `unmet 102/103`, `["REFUSAL-VERSIONS-9DIGIT-Y"]`, **4 error rows per run** (the bend's own rc-64 refusals; amendment A3 records this narrowing) | PASS |
| `N03-era-label-flip`, 3 runs | `unmet 102/103`, `["EXPLICIT-VERSION-ERA"]`, 0 error rows | PASS |
| `N04-extra-components`, 3 runs | `unmet 101/103`, `["EXTRA-COMPONENT", "REFUSAL-VERSIONS"]`, 0 error rows | PASS |
| r95 do-nothing battery, 3 runs × landed gate and N01/N02/N03 | `met 99/99`, 0 error rows (blind to the three new families) | PASS |
| r95 do-nothing battery, 3 runs × N04 | `unmet 98/99`, `["REFUSAL-VERSIONS"]`, failing row `12.9.5.1` rc 0 / 343 bytes | PASS |
| gate metadata probe | six explicit versions echo the flag value with source `flag`; era `pre-12.9.5` for `12.9.4` and `0.999999999.0`, `12.9.5+` for the other four | PASS |
| four-component probe | the four shapes rc 64 / stdout 0; the same-list control `12.9.6` rc 0 / 922 bytes `HEALTHY` | PASS |
| era-rule mutants | `M-z-only-era` kills exactly `REFUSAL-VERSIONS-9DIGIT-Y`; `M-y-only-era` kills it too; `M-x-only-era` does **not** (passes 4 of 4) | PASS |
| gate selftest | `selftest PASS 39/39` | PASS |
| source re-opens | S390 280632 B `a7e00587…`; S389 815447 B `6bf2ce2b…`; S382 23351 B `a940acae…` | PASS |

## Findings (reported, not edited — the instruments are frozen)

1. **The r96 battery's `fam_refusal_versions_9digit_y` docstring carries a false mutant claim**
   (`tools/limine-pin-battery-r96.py:1773-1775`): it says a gate that "reads the era from X alone
   answers era B for `0.999999999.0` and fails". X of that value is 0, so an X-only rule answers
   era **A** — the correct answer; the own-work X-only mutant passes the Y family 4 of 4. It is
   killed instead by `EXPLICIT-VERSION-ERA` and the ERA families, on `12.9.4`. Same class as the
   r95 docstring superlative the round already corrected (routed 4).
2. **The Z position of the per-component cap is unsampled at family level.** No family sends a
   version whose third component is at the cap; `999999999.999999999.999999999` is accepted by the
   gate (measured) but sent by no family, so a bend of Z's bound to `<= 8` is untested.
3. **Four-component shapes beyond the four enumerated are unsampled at family level.** The gate
   refuses `12.9.6.`, `12.9.6.1.2`, `12.9.6.1.2.3` and a non-ASCII digit rc 64 / stdout 0, but
   `EXTRA_COMPONENT_VALUES` is exactly four members, so no case asserts them.

## Relation to the entry the L1 already landed

The L1 landed `corpus/knowledge/limine-bound-per-component-r96.md` at `59cbfe2f` while this seat
worked. The draft agrees with it on every clause and adds the three-run receipt table, the
era-rule mutant evidence, the four gate limit probes, the source byte/sha receipts and the three
named limits. Two differences worth the L1's eye: the landed entry cites S386-S388 for the era
split while this draft's Limits follow the seat brief and name S382-S384/S389-S390 (the v12.9.6
counterparts are byte-identical files per the S382 row); and the landed entry carries neither the
mutant table nor the three named limits.

## Constraints honoured

Only `.ufo/waves/round-96/w1/ScribeKnowledge/` (and this trailer file) and the scratch root
`/fast/scratch/hyaku/tsukuroi-r96/ScribeKnowledge` were written; the scratch tree was deleted after
the receipts were copied. No lane file was edited. `tools/make-r96-bends.py` and
`tools/make-r95-bends.py` were not run; every bend used is the frozen copy under
`before/controls/bends/`, and the three own-work mutants were re-derived in scratch by reading the
lane's gate, with the one-clause diff shown before each run. No git or jj mutation; no tool
installed or upgraded; no subagent dispatched.

{"seat":"ScribeKnowledge","verdict":"findings","notes":"Knowledge draft at .ufo/waves/round-96/w1/ScribeKnowledge/knowledge-draft.md; seat report and receipts under the seat dir. Own measurements confirm the C1 shape: roster 99->103, landed gate 103/103 met x3 (0 error rows), four bends x3 each with the exact frozen failed_families (N02 with 4 error rows per run, as amendment A3 records), r95 do-nothing 99/99 met x3 on the landed gate and N01/N02/N03 and 98/99 unmet ['REFUSAL-VERSIONS'] x3 on N04, plus own-work probes of the echo/source/era fields, the four-component refusal with its same-list positive control, and three era-rule mutants. Three findings: the r96 battery docstring's X-only-era claim is false (measured); the Z position of the cap is unsampled at family level; four-component shapes beyond the four enumerated are unsampled. Frozen instruments not edited."}
