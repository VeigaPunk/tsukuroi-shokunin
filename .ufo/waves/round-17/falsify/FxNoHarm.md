# FxNoHarm — "no axis harmed" vs the wrong URGENT L0 line

**Verdict: FAILS (narrow, fixable) on calibration. Holds for adjacency, depth and the edited entries.**

- **Calibration: harmed, residual.** [obs] Fleet reflog `.git/logs/HEAD:471,474`: ac792a7 at 1792510478, 6fe9984 at 1792512170, so the correction came 28 min later. The lesson says "within 40 minutes", which holds. The correction `l0-questions.md:61` supersedes only the line-60 "snapshot verdict". Wrong statements from `RevL0Accuracy.md:8,10,24` still stand uncorrected for the operator: the PWD attribution "PWD ~/Documents/nvhelpme = your 'RAM NVMe BIOS' session" (actual split is 4 nvhelpme, 4 tmp, 5 home; `boot-chain-capture.txt:76-96`), "dkms built for … 7.2.3", and an unanchored `/var/backups` path. The lane corpus fixed the PWD split (`boot-chain-r17.md:16`), but `round-17.md:37` records only the type-blind error. [obs] `boot-chain-r17.md:25` still states "the operator ran `limine-update`".
- **Adjacency: unchanged.** [obs] tabi pins `ebeb396…:62` (`tabi-shokunin/corpus/adjacency.tsv:6-7`). hyaku cites the correction (`.ufo/waves/hyaku/PHASE2.md:113-114`). No sibling cites the wrong verdict.
- **Depth: improved.** [obs] The rejected reading is kept at `boot-chain-r17.md:133-137`.
- **Edited entries: no false statement found.** [obs] The no-op premise is withdrawn at `initramfs-v42…md:83`. [inf] `partial-upgrade-recheck-r15.md:179` ("mismatch … live … not a future risk") lacks a pointer to R17-SYMLINK.

**Fix:** append an L0 erratum for these facts, add a mistake row, and make line 25 say [inf].
Unverified: SCORECARD r17 outcome (absent); whether option (b) was acted on.

Scope: executed=none
