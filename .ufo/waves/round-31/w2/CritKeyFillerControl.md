# CritKeyFillerControl — round 31, wave 2 (falsify)

Verdict: done. Control K6 ("download but do not read") scores 8 of 8 under the frozen C1 counter, with exit 0. A human reader would accept 0 of the 8 statements as a true, useful answer. The counter's 8 therefore cannot tell a writer who read the sources (K5, also 8 of 8) from a script that only fetched and hashed them. This attacks the C1 claim that an 8 from `tools/check-btrfs-repair-r31.py` is evidence of depth.

## Build

- [obs] Base: sandbox clone /fast/scratch/hyaku/tsukuroi-r31/CritKeyFillerControl/repo, checked out at 8cff9e7cfb034b49c645d548801ac3185a827cb4. The assignment calls this commit the parent of f3a5723a. `git log --oneline -5 f3a5723a…` shows the parent is 4e1659f, and 8cff9e7c is the before-receipts and controls commit that precedes the wave-1 integration 13ca52d0. I used 8cff9e7c as instructed. At 8cff9e7c, `grep -cE '^\|\s*S16[4-9]\s*\|' corpus/SOURCES.md` gives 0, `grep -c '^| \[R31-' SKILL.md` gives 0, and `corpus/knowledge/btrfs-repair-r31.json` is absent.
- [obs] The counter in the clone has sha256 4f69a109e9b56b3fcba0df5a3555f7ff833b6b04fff28176060efe82ebde5cb8 (the frozen value). `git diff --stat 8cff9e7c f3a5723a -- tools/check-btrfs-repair-r31.py` is empty, so the counter is the same at the lane tip.
- [obs] Script: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/CritKeyFillerControl/build-k6.py (sha256 7ad5c44e4c10c6d4063ffb363d4cb25bf6ab576a6d1523bd7c7de96791ce4404). It imports the counter from the clone and uses the counter's own `SALT`, `KEYHASH`, `QUESTIONS`, `URL`, `words()` and `has_token()`. For each question it does the following, with no human step:
  - Downloads the six files from the frozen URL. It would fall back to kernel.org cgit at v7.1, but that was not needed. It keeps a file only if its bytes match the pin.
  - Takes as the quote the first line of the question's own pinned file that has 6 to 25 whitespace-separated words and contains a frozen novelty token. The whole stripped line is the quote.
  - Recovers each key group by hashing every counter token of that file (and its pieces split at `-`, `/` and `.`) with the salt. It keeps the first hit in file order and tries the other five files only on a miss.
  - Writes the statement as the first novelty token, then one recovered word per group, then a fixed filler (`the answer for this question is recorded here as the lane notes it …`) cut to reach 12 words.
  - Adds the registry rows S164–S169 (status `mined`, frozen URL, pin), one `| [R31-Qnn] ` SKILL.md line carrying the token, and the snapshots under `.ufo/waves/round-31/fixture-k6/`.
  - Commits in the clone and runs the frozen counter on that commit.
- [obs] Run: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE /usr/bin/python3 build-k6.py --repo /fast/scratch/hyaku/tsukuroi-r31/CritKeyFillerControl/repo --baserev 8cff9e7c… --out <seat dir> --private /fast/scratch/hyaku/tsukuroi-r31/CritKeyFillerControl/private` gave exit 0 in under 1 s. It made control commit c355dac64afa2b85a6b7ba79750a0f677c9a4e74, which exists only in the sandbox clone.
- [obs] Fetches: all six came from `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/<file>` with HTTP 200, and each sha256 equals its pin (`k6-result.json`, field `fetched`). The bytes are saved unchanged in `.ufo/waves/round-31/w2/CritKeyFillerControl/snapshots/`:

  | File | sha256 |
  |---|---|
  | Defragmentation.rst | 71ad07a3f200284b01d6ee18fc4cc8732fe0542b80556e2cc798247505daa60b |
  | btrfs-rescue.rst | 838504fe8b00d221e017457e7953717f3ca2a0e886a48a4c457367b8c4063a1d |
  | btrfs-check.rst | 927b67b4ab13f681866e699fcd6ea4917a42ef08e4db1731b0adf065022d955c |
  | ch-mount-options.rst | aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f |
  | btrfs-replace.rst | da4bf595f072a96a309535c1022b0171a8657a4f207a3d3da73250886fd8bc9e |
  | Trim.rst | 2a114d56f29d727002a981e868cc97e89d7dd77a5e1cf42ad5a9ff05bfcf0ffc |

- [obs] No person read the six pinned files. I never opened them, and the script prints only counts, fail lists and statements with the keys masked. The plaintext rows are kept only in the sandbox (the commit, and `private/k6-rows-plaintext.json`). To judge the rows below I read the plaintext K6 statements, which hold only the recovered key words and filler. I did not open the source files to do it.

## Findings

1. [obs] **Score: 8 of 8, exit 0.** The receipt `.ufo/waves/round-31/w2/CritKeyFillerControl/c1-K6-download-not-read.jsonl` (sha256 0d58100c…bdcaf63) shows `"new_sourced": true, "fail": []` on lines 1–8 for Q01–Q08. Line 9 reads `{"predicate": "new_sourced", "new_sourced": 8, "of": 8, "revision": "c355dac6…", "base": "2077e2fa…", "counter_sha256": "4f69a109…"}`.
2. [obs] **What the script found, as counts only** (`build-k6.stdout` and `k6-result.json` field `per_question`):
   - Every question found a quote line on the first scan. Quote lines and word counts: Q01 line 4 (14 words), Q02 line 126 (13), Q03 line 30 (14), Q04 line 38 (12), Q05 line 92 (11), Q06 line 13 (9), Q07 line 12 (12), Q08 line 29 (12).
   - 24 of 24 key groups were recovered from the question's own pinned file. None needed another file and none was missing.
   - Of the 40 sealed digests, 34 hash words that occur in their question's own file.
   - Every statement has exactly 12 words.
3. [obs] **The frozen novelty tokens alone satisfy 10 of the 24 key groups, and at least one group in each of the 8 questions.** I checked this by importing the counter, hashing the counter tokens of each question's `tokens` list with SALT, and intersecting them with KEYHASH, which gave `{"groups_hit_by_tokens_alone": 10, "of_groups": 24, "questions_with_token_hit": 8}`. Because R6 already forces the token into the statement, R7 in effect asks for only 14 further words across the 8 questions.
4. [obs] **R7 is the only rule that separates junk over the real snapshots from a pass, and hashing the file's own words beats it.** K3 junk-real (the same layout as K6, with filler statements) scores `"new_sourced": 0`. Every K3 failure is an R7 missing-group failure, for example `.ufo/waves/round-31/measure/controls/c1-K3-junk-real.jsonl:2` reads `"fail": ["R7 sealed answer-key group 2 missing", "R7 sealed answer-key group 3 missing"]`. K6 changes only the statement words and reaches 8. Scores under the same counter:

   | Control | Score |
   |---|---|
   | K1 sourceless forgery | 0 |
   | K3 junk over real snapshots | 0 |
   | K4 quote copied as statement | 0 |
   | K5 reader-written positive control | 8 |
   | K6 download but do not read | 8 |

5. [obs] **Human-reader judgment for each row: not a true, useful answer in 8 of 8.** Each statement is a novelty token, then 2 to 4 bare key words with no verb or relation between them, then the filler "the answer for this question is recorded here". The masked statements are in `k6-result.json`, field `statements_masked`, for example Q01 `defragment <g1> <g2> <g3> the answer for this question is recorded here`. The filler's only claim is false, because no answer is recorded. No row asserts anything a reader could act on.
   - Q01: does not say whether defragmenting changes space use under shared extents, or in which direction.
   - Q02: names no trigger condition and no loss.
   - Q03: states no condition under which `--repair` may be run, and gives no warning.
   - Q04: does not say what the option does or that any workload is unsuitable.
   - Q05: the bare words cannot be mapped onto "what it bounds", "default" and "warning limit".
   - Q06: lists nouns and does not state what is given up.
   - Q07: gives no procedure and states no size relation.
   - Q08: names modes and makes no recommendation.

   [inf] A reader who already knows btrfs might guess the intended answer from the key words for some rows. That knowledge comes from the reader, not the row, so none of these rows counts as a useful answer.
6. [inf] **The counter's 8 is reachable with no understanding.** Under the frozen R1–R8, "8 of 8" proves only that the pinned bytes were fetched and committed, that each quote is a verbatim line holding a token, that the registry rows are well formed, and that each statement contains a token plus words from the source's vocabulary. It does not prove that the writer read or understood the source. This confirms wave-1 CritKeyDictionary finding 7 by construction and run, where wave 1 had only predicted it. The declared ceiling (counter docstring, `tools/check-btrfs-repair-r31.py:37-41`) foresaw "a writer who has read the source can string them together with filler". K6 shows that reading is not needed: a script with no reading step gets the same score.
7. [obs] **No frozen rule, counter or probe was changed.** The declaration's withdrawal rule names only K0–K4 (`SCORECARD.md:1211`, "If any do-nothing control (K0, K1, K2, K3, K4) reaches 8, C1 is withdrawn before data"). K6 is a control built after data, so that rule does not trigger on its own wording. [inf] Whether a no-understanding control reaching the target disqualifies the counter as depth evidence is a decision for the judge, not a fixable code defect.
8. [obs] **Side note, not caused by this seat:** the lane working tree shows ` M corpus/SOURCES.md` in `git status --short`. Its diff (`git diff -- corpus/SOURCES.md`) is 3 insertions and 3 deletions and contains 0 `K6` strings. The script wrote SOURCES.md only inside the sandbox clone.

## Impacted axes

- depth (C1): the 8 of 8 at 13ca52d0 is not evidence of depth on its own, because K6 matches it with no reading.
- calibration: any sentence that credits depth because the counter reads 8 overclaims.

## Smallest safe correction

The counter, its keys and the targets stay unchanged.

1. The round record lists K6 = 8 of 8 (receipt above) next to K1 and K3–K5. It states plainly that the counter's `new_sourced` cannot separate fetching from reading, because K5 and K6 score the same.
2. C1 depth is credited only through the wave-2 row reviews (RevRowQ01–Q08) of each row's truth and usefulness. The counter's 8 is recorded as a well-formedness and provenance check, not a depth measurement.
3. The plaintext keys stay out of the lane until the lesson reveals them after data, as declared.

The L1 should commit this seat folder. I made no git writes in the lane, as the contract requires. The only commit is c355dac6 in the sandbox clone.

Scope: read=tools/check-btrfs-repair-r31.py (lane and clone), SCORECARD.md:1196-1225, .ufo/waves/round-31/w1/CritKeyDictionary.md, .ufo/waves/round-31/measure/controls/build-c1-controls.py and c1-K1/K3/K4/K5 receipts (grep), K6 plaintext statements in the sandbox only (pinned btrfs files never opened by a human); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/CritKeyFillerControl.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/CritKeyFillerControl/{build-k6.py,build-k6.stdout,c1-K6-download-not-read.jsonl,k6-result.json,snapshots/*.rst}, /fast/scratch/hyaku/tsukuroi-r31/CritKeyFillerControl/{repo (clone, commit c355dac6),private/k6-rows-plaintext.json}; executed=env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-local <lane> <sandbox>/repo and checkout 8cff9e7c (exit 0), git remote set-url --push origin DISABLED in the clone (exit 0), python3 build-k6.py (exit 0; counter exit 0), inline python token-only key count (exit 0), read-only git log/diff/status in the lane
Model: not exposed
Installs: none
