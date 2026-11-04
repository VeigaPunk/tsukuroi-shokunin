# R2Reviewer — C2 attack report (tsukuroi r73 w1)

Scope: re-derive the three r72-routed defects at base `eb1057575d5d8b940c4846e21611674cf5571aea`; attack the frozen instrument `tools/check-r72-routed-r73.py` with adversarial fixtures; judge whether the planned repair direction actually closes C2. Fixture battery run under `/fast/scratch/hyaku/tsukuroi-r73/R2Reviewer` (deleted after the run); each fixture scored with `python3 tools/check-r72-routed-r73.py --root <case>`.

## Instrument identity (frozen declaration vs measured)

| Instrument | Measured sha256 (tip) | Frozen value | Match |
|---|---|---|---|
| `tools/check-r72-routed-r73.py` | `93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e` | declaration C2 digest `93f034e3…` | yes — instrument unmodified |
| `tools/check-r71-routed-r72.py` | `2610ff433bf5d4e945ce5b2da0cf168745e4142ecffabc3d160afee33005cdcc` | checker's `TIP_DIGEST` constant `2610ff43…` | yes |
| `tools/count-ul-rows-r73.py` (C1 cross-check) | `542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6` | declaration C1 digest `542f9c29…` | yes |

Checker `--selftest` re-run at tip: `SELFTEST: PASS (5 cases, 5 passed, 0 failed)` rc 0.

## Defect re-derivation at base — all three REAL

1. **R72-LESSON-SUPERSEDED-CLAIMS — real.** Base `corpus/lessons/round-72.md` lines 160/164 assert "No capability row enters this round" and "nine hermetic cases". The same base tree supersedes both: `LOG.md:3173-3175` — "C2 instrument superseded in-round: `E2GateSelftest` v2 adds the `SELFTEST-CASES` guard …; the landed tool is 10 cases / 10 passed (sha256 `f22eb94f…`)"; the committed receipt `.ufo/waves/round-72/after/selftest-selftest-after.txt` reads `SELFTEST: PASS (10 cases, 10 passed, 0 failed)` rc 0; and base `SCORECARD.md:5754` enters the `gate-selftest` capability row the lesson claims never entered.
2. **R72-C3-INSTRUMENT-DIGEST-DRIFT — real.** Base `SCORECARD.md:5615-5616` freezes `check-r71-routed-r72.py` at `df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712`. Measured history: `df8a59c7…` was the true digest at the r72 declaration commit `6b426762`; the tool changed in repair commit `53bcddef`; from base `eb105757` through HEAD the committed tool is `2610ff43…` (measured at base, `7fb35c74`, and tip — identical). SCORECARD was never updated; the drift is in committed bytes.
3. **R72-CAPABILITY-ROW-STALE — real.** Base `SCORECARD.md:5754`, capability row `gate-selftest`: "nine named cases … `python3 tools/check-selftest-tally.py --selftest` -> PASS 9/9". The receipt it describes reports **10 cases / 10 passed**. Row is stale by one case.

Frozen control reproduced: checker at base → `ROUTED_STALE=3 ROUTED_OK=0/3`, rc 1 — exactly the declared before reading. Worktree/HEAD (repairs not yet landed): same `ROUTED_STALE=3`, rc 1.

## Probe table

`held` = checker passed the adversarial fixture (predicate satisfied without the real work); `survived` = checker rejected it. All fixtures carry honest F0-grade blocks for the two items not under test.

| # | Attack | Result | Evidence |
|---|---|---|---|
| F0 | honest-correction control (all three blocks, checker-selftest template shape) | control-ok rc 0, `ROUTED_STALE=0 ROUTED_OK=3/3` | harness sanity |
| F0b | nothing appended | control-ok rc 1, `ROUTED_STALE=3` | harness sanity |
| F1 | LESSON block quotes both superseded sentences, asserts they **were right**, carries every token incl. `R72-LESSON-SUPERSEDED-CLAIMS`, `10 cases` | **held** rc 0 | token presence cannot reject a contradiction |
| F2 | DIGEST erratum re-freezes `df8a59c7…` as canonical, calls `2610ff43…` "the drifted artifact to be reverted", carries every token incl. `same-instrument` | **held** rc 0 | direction unenforceable on DIGEST too |
| F3 | CAPABILITY refresh says ten but names `…selftest-selftest-after-v2.txt` (wrong receipt) | **survived** rc 1 `CAPABILITY-STALE` | exact receipt-path token rejects substitutions |
| F4 | CAPABILITY names `…selftest-selftest-after.txt.bak` — nonexistent superstring of the required path; receipt file not present in fixture | **held** rc 0 | tokens are substring-matched and the receipt file's existence/content is never read |
| F5 | all matching text inside paragraphs only — no line-start `## correction|erratum|capability` heading anywhere (the r72 unanchored-regex class, all three items) | **survived** rc 1, all three stale | heading must be a line-start `## ` heading and tokens must sit inside that block — the r72 defect class is closed in this instrument |
| F6 | content-free keyword list as the LESSON correction block | **held** rc 0 | vacuity passes |
| F7 | LESSON block with no standalone word "ten"; "often" carries the token as a substring | **held** rc 0 | substring tokens |

## Direction of the repair (item 3)

`E2Routed.md` was still a stub ("Sections to follow") at both read times, so per the item I judged direction from the frozen checker's own `good_block` templates plus reference texts I drafted and scored as F0. The template sentences read as corrections to a reader: "the sentences … are superseded; the landed state is the gate-selftest capability row and 10 cases"; "check-r71-routed-r72.py moved from `df8a59c7…` to `2610ff43…`; the before control was re-run with the final instrument (same-instrument) at `.ufo/waves/round-72/after/selftest-selftest-after.txt`". A sentence that would fail the to-a-reader test is one that keeps the tokens while asserting the opposite — F1's "the original sentences 'No capability row enters this round' and 'nine hermetic cases' were right; the gate-selftest reading of ten (10 cases) is the misreading" passes the frozen checker (rc 0) and must never appear in the landed blocks. F1/F2 are the experimental proof that the instrument cannot carry the direction; the landed text must.

## Findings

- No attack found a defect in the frozen instrument **outside its declared contract**: the docstring declares token-in-anchored-block semantics, and F3/F5 confirm both hardening properties (line-start anchored heading; exact receipt-path token). F1/F2/F4/F6/F7 are residual laxities inside that contract, recorded here, not repair-blocking defects.
- Named limit re-proven (F1/F2): a block that names the right tokens while contradicting them satisfies `ROUTED_STALE=0`. The round-72 unanchored-regex defect itself is fixed here (F5 survived).
- F4 note: the checker treats `RECEIPT` as a string token only; naming any superstring path (e.g. `….txt.bak`) passes even with no receipt file in the tree. Direction and existence assurance must come from reading the landed blocks / re-running the receipt command, not from this instrument.
- C1 cross-check: counter digest matches the declaration; at HEAD it reads `UL_NOTE absent` rc 128 because `corpus/knowledge/systemd-unit-load-plane-r73.md` is not yet committed (mid-wave state, outside C2 scope).

## C2_CLOSABLE=yes

All three routed defects are real at base, and each closes with an appended, correctly directed block: a lesson correction superseding both sentences toward the 10-case landed state; a SCORECARD erratum recording the `df8a59c7…` → `2610ff43…` drift with the same-instrument re-run; a capability refresh correcting `gate-selftest` to ten cases with the real receipt path. On such text the frozen checker prints `ROUTED_STALE=0 ROUTED_OK=3/3` rc 0 (F0), rejects wrong-receipt (F3) and paragraph-only (F5) substitutes, and its base control reads `ROUTED_STALE=3` rc 1 as declared. Residual risk: token-presence cannot prove direction (F1/F2) or receipt existence (F4) — the L1 should read the landed block sentences for supersession direction before calling C2 closed.

## Hygiene

No tool installs (none needed); pacman untouched; no lane mutations outside my wave dir; no git/jj mutations; scratch deleted before yield.
