# R2Reviewer — C2 attack seat, tsukuroi r73 w1

status: complete
verdict: C2_CLOSABLE=yes

Attacked C2 (freshness): re-derived all three r72-routed defects as REAL at base `eb105757` (lesson superseded sentences at `corpus/lessons/round-72.md:160,164` vs committed 10-case receipt and `LOG.md:3175`; SCORECARD:5616 freezing stale digest `df8a59c7…` while the committed `tools/check-r71-routed-r72.py` measures `2610ff43…` from base through tip; capability row `SCORECARD.md:5754` saying nine/9-of-9 vs the receipt's 10 cases/10 passed). Base control reproduced `ROUTED_STALE=3 ROUTED_OK=0/3` rc 1.

Frozen instrument verified: `tools/check-r72-routed-r73.py` sha256 `93f034e3…` matches the declaration; `--selftest` PASS 5/5 rc 0. Nine-fixture adversarial battery: F3 (wrong receipt `-v2.txt`) and F5 (paragraph-only text, the r72 unanchored-regex class) SURVIVED; F1 (block asserting the superseded sentences were right), F2 (erratum re-freezing the old digest as canonical), F4 (superstring receipt path `….txt.bak`, receipt file absent), F6 (content-free keyword list), F7 (token "ten" satisfied by "often") HELD — all within the docstring's declared token-in-anchored-block contract, so no instrument defect; they record that direction/receipt-existence assurance cannot come from the instrument.

Direction judgment: `E2Routed.md` still a stub at both reads; judged from the checker's own good_block templates + reference texts scored as F0 (rc 0 `ROUTED_OK=3/3`). Reference sentences read as corrections to a reader; a contradiction sentence like F1's would satisfy the frozen checker and must not land.

Full probe table, measured digests (checker `93f034e3…`, r71 tool `2610ff43…`, C1 counter `542f9c29…` cross-check), and residual risk: `.ufo/waves/round-73/w1/R2Reviewer/report.md`.

Hygiene: no installs, no lane mutations outside my wave dir, no git/jj mutations, scratch `/fast/scratch/hyaku/tsukuroi-r73/R2Reviewer` deleted.
