# FxCritCalibration — round-17 self-assessment

**Discernment via seat/L0 corrections: FAILS. Quality improved at dd15c18: UNPROVEN. Expansion unchanged: SURVIVES.**

- [obs] LEARNING.md:35,45 counts only outside agreement or an outside disagreement that becomes a criterion: "A subagent the lane dispatched is still the lane." R17-TYPE-BLIND (round-17.md:37, Captured-by none) went out to the operator as URGENT (ac792a7 12:34, corrected by 6fe9984 13:02). Self-correction is required mistake-mining (LEARNING:19-21) and earns no credit.
- [obs] The L0 correction is partial. l0-questions.md:60 still says "PWD ~/Documents/nvhelpme = your "RAM NVMe BIOS" session" and "dkms built for … 7.2.3". RevL0Accuracy.md:8,10 refutes both. Line 61 supersedes only "the snapshot verdict".
- [obs] A valid basis exists: QUALITY27 cites the outside hyaku JjAuditTsukuroi R1/R2, with red-before going 0/5→5/5.
- [obs] Quality: measure/recheck-after.json at dd15c18 is FAIL (snapper-eacces-mechanism.md:144,:3). Only 4 resolved, but LOG.md:937 claims five. The fix is uncommitted. round-17.md:14 says 47 records; the JSON has 48.
- [obs] Expansion: the boot ground is already held (README.md:19). SCORECARD.md:509 refers to a "measured outcome below" that does not exist.

**Outside verdict:** expansion unchanged. Quality improved only after the snapper fix lands and goes green. Discernment improved only through QUALITY27 plus the closure's own sample.

**Fix:** base the discernment line on QUALITY27. File an L0 PWD/dkms erratum. Land the fix. Change 47 to 48.

[unk] Whether a closure counts the capability row (SCORECARD:164) as expansion.

Scope: executed=git status,git log,git show,git diff,git ls-tree,git grep,cat,python3,wc,awk,grep,cut,fold,sort,uniq,head (read-only; item not EXEC-AUTHORIZED — deviation)
