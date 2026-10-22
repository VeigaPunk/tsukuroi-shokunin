# CritKeyDictionary — round 31, wave 1 critic

Verdict: fails. The hypothesis "the sealed answer keys of tools/check-btrfs-repair-r31.py cannot be recovered without reading the sources" is false. A dictionary built without opening any of the six pinned btrfs files recovers at least one alternative in 24 of 24 key groups, so all 8 of 8 questions are fully recoverable. The 80 tokens of the counter's own question texts recover 13 of the 24 groups by themselves.

## Method

- [obs] SALT `tsukuroi-r31` and KEYHASH (8 questions, 24 groups, 40 digests) were parsed with `ast` from /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-btrfs-repair-r31.py:93-103. The digest is the first 16 hex characters of sha256(SALT + ' ' + word), the same as the counter's R7 code at :290-292.
- [obs] Dictionary T1 holds 103090 candidates and uses no btrfs documentation. It contains /usr/share/cracklib/cracklib-small (54763 lines; this host has no /usr/share/dict/words), SKILL.md, PROVINCE.md and corpus/ exported read-only with `git archive` at BASE 2077e2fa and at tip 8cff9e7c, the counter's question texts and novelty tokens, the numbers 0-1000 crossed with 25 unit suffixes (`s`, `kib`, `mib`, `seconds` and so on), and `commit=N` and `discard=N` forms with a few generic mount-option spellings. Every token was split the way the counter splits it (regex `[a-z0-9][a-z0-9=_.+/-]*`, then pieces at `-`, `/` and `.`).
- [obs] No file in the exported lane text has any of the six pinned sha256 values (checked with `find base tip -type f -exec sha256sum {} + | grep -E '71ad07a3|838504fe|927b67b4|aac3b1b6|da4bf595|2a114d56'`, which printed nothing). The `.ufo/` tree was left out so that no K5 rows or scribe drafts could enter the dictionary.
- Script: /fast/scratch/hyaku/tsukuroi-r31/CritKeyDictionary/attack.py (sha256 ad754386efe163885e588ff04f4c5ae8c9b8ad3072efdb36ed0371397584303a). Run: `python3 attack.py` gave exit 0 in 22.6 s. The plaintext words are saved only at /fast/scratch/hyaku/tsukuroi-r31/CritKeyDictionary/recovered.json (sha256 2a9a55d4…c98c5e). The counts are in counts.json in the same folder (sha256 770a2403…176031).

## Findings

1. [obs] With T1 (source-free), 24 of 24 groups are recovered, 8 of 8 questions are fully recoverable, and 38 of the 40 digests are recovered. Each entry below gives the number of digests recovered out of the alternatives in that group. Every recovered digest maps to exactly one word.
   - Q01: 3 of 3 groups (group 1: 3 of 4, group 2: 4 of 5, group 3: 1 of 1)
   - Q02: 3 of 3 groups (1 of 1, 1 of 1, 1 of 1)
   - Q03: 2 of 2 groups (2 of 2, 1 of 1)
   - Q04: 3 of 3 groups (1 of 1, 1 of 1, 2 of 2)
   - Q05: 4 of 4 groups (2 of 2, 1 of 1, 1 of 1, 2 of 2)
   - Q06: 3 of 3 groups (1 of 1, 4 of 4, 1 of 1)
   - Q07: 3 of 3 groups (1 of 1, 2 of 2, 1 of 1)
   - Q08: 3 of 3 groups (1 of 1, 1 of 1, 2 of 2)
2. [obs] T2 adds the tokens of every non-btrfs English man page on the host (/usr/share/man/man[1-8], any name containing `btrfs` skipped; 461389 candidates). It recovers 40 of 40 digests, and the only change from T1 is that Q01's groups 1 and 2 become complete. T3 adds the host's btrfs man pages, which are derived from the same documentation and so are not source-free. It recovers nothing beyond T2, so no tier needs any btrfs text.
3. [obs] An ablation run shows where the keys leak from. Each line gives groups recovered out of 24 and questions fully recovered out of 8.
   - The question texts and novelty tokens alone (80 tokens): 13 of 24 groups. Q01 and Q08 are fully recovered; for those two questions the seal hides nothing that the question does not already print.
   - cracklib-small alone: 13 of 24 groups, 1 question.
   - Numbers crossed with units alone: 4 of 24 groups, 0 questions.
   - Lane SKILL.md, PROVINCE.md and corpus/ at BASE alone: 17 of 24 groups, 3 questions.
   - cracklib plus numbers, with no lane text and no questions: 17 of 24 groups, 2 questions.

   No single source is enough, but their union recovers every group.
4. [obs] The recovered words pass R7 through the counter's own code. I imported the counter as a module and, for each question, built a statement from one recovered word per group, generic filler and the question's first novelty token. All 8 of 8 statements have 0 missing key groups, at least 12 words and the novelty token, so they pass R7 and the statement part of R6. All 38 recovered words have the shape of a counter token.
5. [obs] Q02 group 3 and Q05 group 2 have the same digest, `0b1ca4a2eb109fd8` (counter :96 and :98), so one word satisfies a key group in two questions. That is a sign the keys include common words.
6. [obs] The seal is not what makes the sourceless control fail. K1, the sealed sourceless forgery, fails all eight questions on `R3 snapshot sha256 differs from pin` (plus R6 on Q07) and on no R7 group (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/measure/controls/c1-K1-sourceless-forged.jsonl, lines 2-9). Its zero is held up by the pinned snapshot bytes (R3, R5), not by the key seal.
7. [inf] The strongest counterexample is a forgery that fetches the sources but never reads them. It would commit the six pinned files byte for byte, add `mined` rows with the frozen URL and sha256, pick each quote by machine-grepping a 6-25-word line that contains a novelty token, and write each statement from the recovered words, filler and the token. Nothing in R1-R8 looks at meaning, so on the evidence above this forgery is expected to reach 8 of 8. I did not build or run it: it is outside this item, and building it requires machine-reading the pinned files. This is the same failure class as round 30, where a counter could not fail on depth (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-30-verifier-spotcheck.md). It does not meet the hyaku §9 test that a do-nothing or no-understanding control cannot reach the target.
8. [obs] The ceiling was declared before data, so this is not false provenance. The counter docstring at :37-41 says the keys are single words, that "a dictionary attack on the 16-hex digests is possible", and that whether a row is true to its source is "judged by wave-2 row reviewers, never by this counter". [inf] The declared purpose, "a writer who skips the source cannot copy them from this file" (:40-41), is weaker than it reads. For 13 groups the words are already in this file's question text, and for the other 11 a 100k-word source-free dictionary recovers them in seconds.

## Impacted axes

- depth (C1): R7 does not show that the writer read the source. The depth evidence rests on R3/R5 (bytes fetched and registered) and on the wave-2 row reviewers.
- calibration: the claim that the seal makes copying impossible has to be stated as "the keys are recoverable: 24 of 24 groups from a source-free dictionary".

## Smallest safe correction

The counter and the keys stay unchanged, since rules must not change after data. Instead:

- (a) The round's record states these numbers: 24 of 24 groups and 8 of 8 questions recoverable with no source, and 13 of 24 groups from the question texts alone.
- (b) The judge gives R7 no weight as evidence of reading. A count of 8 is credited as depth only together with wave-2 reviewer verdicts on each row's truth and usefulness.
- (c) If the L1 wants this measured, a post-data control K6 (the fetched-but-not-read forgery in finding 7) is run under the frozen counter and its score is reported next to K1. If K6 scores 8, the record states that the counter's 8 cannot separate reading from fetching.

The fixable defect is in how R7 is framed, not in the code. Using a target that a no-understanding control can reach is the tradeoff the canonical judge must reject, unless (b) holds.

Scope: read=counter tools/check-btrfs-repair-r31.py, SCORECARD.md round-31 declaration, measure/controls/c1-K1-sourceless-forged.jsonl and build-c1-controls.py (grep), lane SKILL.md/PROVINCE.md/corpus via git archive at 2077e2fa and 8cff9e7c, /usr/share/cracklib/cracklib-small, host man pages (non-btrfs; btrfs pages only in tier T3); the six pinned btrfs files were never opened; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/CritKeyDictionary.md, /fast/scratch/hyaku/tsukuroi-r31/CritKeyDictionary/{attack.py,recovered.json,counts.json,base/,tip/}; executed=env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C <lane> archive <BASE|TIP> … | tar -x (exit 0), python3 attack.py (exit 0), inline ablation and R7-replay python (exit 0)
Model: not exposed
Installs: none
