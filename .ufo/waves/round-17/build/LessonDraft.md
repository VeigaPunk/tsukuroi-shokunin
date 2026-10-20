# LessonDraft — round 17 scoped findings

Draft: `.ufo/waves/round-17/build/drafts/lesson-r17.md` (about 80 lines; ≤150 limit). Placeholders `<L1 fills>` remain for every measured result.

## Findings

1. [obs] The round-17 L1 captures use the steer-safe substitute `ls -d /var/lib/pacman/local/<pkg>-[0-9]*` (`l1-capture/boot-chain-capture.txt:31`) and state "no pacman invocation" (`l1-capture/fresh-capture.txt:2`). No `pacman -Q` appears in `l1-capture/`.
2. [unk] The mined mistake's round-17 timing ("at round start, before re-reading the steer") has no artifact in this repo. Recorded pacman -Q output is dated 2026-10-19 (`corpus/knowledge/initramfs-v42-sysroot-recovery.md:9`). L1 must supply the transcript pointer.
3. [obs] `initramfs-v42-sysroot-recovery.md:3` still prescribes `pacman -Q`. Fixing it conflicts with append-only corrections (CORPUS). The gate design must choose: dated supersession block, or a newest-block rule. Draft leaves this as a decision for L1.
4. [obs] `boot-chain-r17.md:3` names `tools/boot-chain-audit.sh --live`, which does not exist at baseline. The entry is not admissible until that tool lands or the recheck line changes.
5. [obs] `corpus/QUALITY.md` ends at item 24. QUALITY25–27 exist only in the build spec, so "QUALITY26" is a proposal.
6. [obs] S051–S054 already exist in `corpus/SOURCES.md:57–60`.
7. [obs] r16 § 5 items 1–5 are carried as a routed-debt table. `round-16/build/frozen-cases.json` still exists (item 4).

## Not verified

No gate, census, or grep count was executed. All numbers in the draft are placeholders. Quotes and line citations come from files read with the read and grep tools.

Scope: executed=none
