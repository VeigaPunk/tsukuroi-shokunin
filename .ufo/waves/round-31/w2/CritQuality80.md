Verdict: partly holds. QUALITY 80 refuses the round-30 C1 artefact. Round 31 meets its pins, frozen-predicate, base-sweep, before-data and positive-control clauses. Round 31 fails two clauses of 80 on its own record. Its enumerated control list misses a source-free control that reaches 8 of 8 under the frozen counter. Its 64KiB example misdescribes the mistake it cites. The 78/79 note is right that both IDs are missing, but its 79 re-pointer is weak provenance.

Revision under attack: f3a5723a988bf1c2835985880e7a38d477462cd0. QUALITY 80 is `corpus/QUALITY.md:153` and the note is `:155` at that revision (exported to /fast/scratch/hyaku/tsukuroi-r31/CritQuality80/QUALITY.md).

## A. Can 80 fail?

1. [obs] Yes: 80 refuses round-30 C1. `git show f3a5723a:.ufo/waves/round-30/w2/CritClaimFraming2/out-v2self-under-v1.txt | tail -1` prints `"verified": 10, "of": 10` with counter_sha256 `1bf7ee14…`. The paired fixture cites `"source": "S900"` on all 10 rows (`grep -o '"source": *"S[0-9]*"' … | uniq -c` gives `10 "source": "S900"`). The spot-check records the result at `corpus/lessons/round-30-verifier-spotcheck.md:57-60` ("Can the target fail on depth? No.").
   - Round 30 had no committed do-nothing control and no sha256 pin in its counter, and a sourceless control reached the target.
   - That is exactly 80's withdrawal trigger, and 80's failing-example pointer ("section 2") resolves.

## B. Round 31 against each clause of 80

2. [obs] **Frozen predicate, same sentence: partly holds.**
   - The C1 sentence in the declaration (`SCORECARD.md:1205`) and in the counter docstring (`tools/check-btrfs-repair-r31.py:7-13`) are equal after whitespace normalisation. A python compare of the two extracted sentences printed `equal: True`.
   - The receipt carries only the label: every summary line reads `{"predicate": "new_sourced", …}`. That meets 80's "receipt label".
   - Two texts overclaim. The declaration says the sentence is "in every receipt's summary field `predicate`" (`SCORECARD.md:1205`), and the counter docstring says the same at lines 5-6. Both are false: that field holds the 11-byte label, not the sentence.
   - "The plan" in 80 names no file. The fleet prompt states the rule at `/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-31.md:359` but does not contain the predicate (`rg -c new_sourced` on it gives 0). [inf] So "plan" is satisfiable only if the declaration counts as the plan.
3. [obs] **Pins: holds.** `rg -o '\b[0-9a-f]{64}\b' counter.py` finds 8 `pin=` lines (lines 62-90) covering 6 distinct digests. Each equals the sha256 of the committed snapshot under `.ufo/waves/round-31/w1/ScribeSrc*/`: the first 16 hex match for all six (71ad07a3…, 838504fe…, 927b67b4…, aac3b1b6…, da4bf595…, 2a114d56…). Counter bytes at f3a5723a and f4861f4d both hash to `4f69a109e9b5…5cb8`.
4. **Base sweep: holds as tokens, but the token set fails 80's own spelling clause on one reading.**
   - [obs] The counter re-runs R8 on every run. No committed round-31 receipt carries an R8 failure (`git grep -c R8 f3a5723a -- .ufo/waves/round-31/measure/` prints nothing).
   - [obs] The pinned Q06 source spells the property NOCOW: `ch-mount-options.rst:136` has the quote "under *nodatacow* are also set the NOCOW file attribute". The base holds `nocow` 10 times: `git grep -i -F -c -e nocow 2077e2fa -- SKILL.md PROVINCE.md corpus`, summed, gives 10, including `SKILL.md:2367` row SH3.
   - [obs] Q08's own question text names `discard=async`, and pinned `Trim.rst:21` uses it. The base holds `discard` 6 times, including `storage-health-r26.md:11`.
   - [inf] If "every spelling the source itself uses" covers NOCOW, R8 would fail Q06. The errata (`SCORECARD.md:1222`) already concede both neighbours.
5. [obs] **Controls committed before data: holds narrowly. Two of six controls are not reproducible from the lane.**
   - Controls commit 8cff9e7 is dated 19:57:58 -0300 (22:57:58Z). The earliest wave-1 file mtime is `w1/swarm-registry.json` at 19:58:14 local, and the first seat bytes are `w1/ScribeSrcTrim/Trim.rst` at 19:59:29 local (`find .ufo/waves/round-31/w1 -type f -printf '%T… %p'`). The control receipts finished 22:52:40-48Z.
   - The control commits named in `measure/controls/c1-controls-commits.jsonl` are absent from the lane. `git cat-file -t` on bf2c014a (K1), 92cdff13 (K5) and 078fb86a (K2) each give "fatal: git cat-file: could not get object info".
   - The sealed builder exists in the lane only as a digest (`sealed-builder.sha256`, `54f003b8…`). Its bytes are in scratch: `sha256sum /fast/scratch/hyaku/tsukuroi-r31/sealed/build-c1-sealed.py` matches `54f003b8…`.
   - `git ls-tree -r --name-only f3a5723a | rg build-c1` lists only `build-c1-controls.py`. The declaration promises the sealed file "after data" (`SCORECARD.md:1211`); at f3a5723a the after receipts exist and the file is still not committed.
   - The K3 commit 5e31121e is not reachable even in the L1 scratch clone. Checking it out in a `--no-local` clone gave "fatal: unable to read tree (5e31121e…)".
   - K2-K4 are reproducible from the committed patches. I applied `patches/0001-K3-junk-real.patch` onto f4861f4d and got `new_sourced` 0 of 8 under `4f69a109…`.
6. **Positive control: holds numerically.**
   - [obs] K5 reads 8 of 8, exit 0 (`measure/controls/c1-K5-reader-ceiling.jsonl`, last two lines).
   - [unk] Who wrote K5 is unknown. Its builder mtime (19:49 local) predates the declaration commit (19:52). 80's "reader-written" is undefined: it could mean a key-holder or a non-author.
7. [obs] **Synonym sweep recorded with the declaration: fails.**
   - 80 says this limit is "recorded with the declaration, not discovered after it". The declaration cell says "a topic with 0 base hits" (`SCORECARD.md:1202`) and has no synonym sweep.
   - The held neighbours (SH3 for Q06, `discard=async` for Q08, `btrfs-space-r30.md:28` for Q01) were found by wave-1 CritNoveltySemantic and CritClaimFraming. They were appended as errata item 2 (`SCORECARD.md:1222`) "after wave 1".
   - The lesson's own row R31-TOKEN-NOT-FACT-NOVELTY (`corpus/lessons/round-31.md:55`) says the same. By 80's text, round 31's C1 declaration is a refused artefact for this clause.
8. **Per-row non-author review: declared in part, not yet performed.**
   - [obs] The declaration's ceiling commits to "row truth and usefulness … judged by wave-2 row reviewers" (`SCORECARD.md:1211`). That records 80's second limit in time.
   - [obs] It does not mention "novelty beyond the held neighbours", which 80 also requires.
   - [obs] At f3a5723a no per-row review exists. The RevRowQ01-Q08 seats are wave 2.
   - [inf] Admission under 80 is not yet earned.

## C. Strongest counterexample: a source-free control reaches the target

9. [obs] **K6 = K3's committed junk rows, with each statement replaced by filler that carries source-free dictionary words for every key group. It scores 8 of 8, exit 0, under the frozen counter `4f69a109…`.**
   - Run: `python3 tools/check-btrfs-repair-r31.py --revision 9e478ae5f01dcf9da15cce2ad29beffcc3c4d4ae --lane /fast/scratch/hyaku/tsukuroi-r31/CritQuality80/repo`. Every row reads `"fail": []`, and the summary reads `"new_sourced": 8, "of": 8`. That is a sandbox commit on f4861f4d plus the K3 patch.
   - Output (ids, verdicts and summary only, no statements): `.ufo/waves/round-31/w2/CritQuality80/k6-run.jsonl`, sha256 `22748ef6a1e8654c47ce34e5658bfee935d5374fdb851dc567a73806f2fdecaa`. It is a plain run, not a `run-receipt.py` receipt.
   - Key recovery used `/usr/share/cracklib/cracklib-small`, numbers, unit suffixes and the question texts, and recovered 23 of 24 groups. A 60-word generic btrfs vocabulary list written without opening any pinned file recovered the 24th, Q07 group 1. No source was read for keys. Plaintext keys stay in scratch (`/fast/scratch/hyaku/tsukuroi-r31/CritQuality80/k6-keys.json`) and are not printed here.
   - [obs] Why it works: in the committed receipts every K3 and K4 row fails only R7. A per-row set print gives `['R7']` for Q01-Q08 in both `c1-K3-junk-real.jsonl` and `c1-K4-quote-copy.jsonl`. So the seal is the only content discrimination, and the seal is dictionary-recoverable (wave-1 CritKeyDictionary findings 1 and 4). CritKeyDictionary recommended exactly this "K6" (`w1/CritKeyDictionary.md:49`); no K6 receipt is committed.
   - Impacted axes: depth (C1's 8 cannot separate reading from fetching) and calibration.
   - Effect on 80: its list of controls is written as the set to commit and omits "junk rows carrying dictionary-recovered key words". Round 31 therefore satisfies 80 while a do-nothing-equivalent control reaches the target. The plan's rule (prompt `:351-355`, "build the cheapest control that skips the claimed work … if it meets the target, the counter or target is wrong") is not met by 80's list.
   - 80's own wording "a format check a reader can satisfy with filler" understates the gap: a non-reader can satisfy it. 80's "Shown able to fail" sentence is true only for K0, K1 and K2, which fail R1, R3 and R5 at the pin and registry gate.

## D. Overreach: clauses no counter or reviewer can check as written

10. [obs] **The 64KiB example is not a case of the rule it illustrates.** `grep -c -F '64 KiB'` over the six pinned snapshots gives 0, and `64KiB` occurs once (`ch-mount-options.rst:38`). The source uses one spelling only.
    - The counter's key already accepted that sole source spelling. R31-KEY-SPELLING (`round-31.md:56`) arose because the scribe's "64 KiB" was refused, and the source never uses that spelling.
    - So "lists every spelling the source itself uses" would not have caught its own failing example. The clause and its Mistake disagree.
11. [inf] **Clauses with no fail condition a reviewer can apply:**
    - "the plan" names no file.
    - "reader-written" does not say who.
    - "cheapest controls" is unbounded, as finding 9 shows.
    - "a synonym sweep … naming what the lane already holds in other words" has no completeness test. A reviewer can see that a sweep exists but cannot fail an omission.
    - "before any seat produces data" is checkable only by file mtimes or dispatch logs. No receipt binds it: `w1-dispatch.json` carries no ISO timestamp (`rg -o '20..-..-..T'` gives nothing).

## E. The 78/79 note against `corpus/lessons/round-30.md`

12. [obs] **"Neither ID exists": holds.** `git grep -n "GIT-RESIDUAL\|SOURCED-ROWS" f3a5723a -- corpus/lessons/round-30.md` exits 1. The lesson's Mistakes rows are exactly R30-UNRECEIPTED-GATES, R30-DECLARATION-OVERCLAIM, R30-UNSCREENED-TARGET, R30-SEAT-MISROOT and R30-CHECKER-SELF-SATISFY (`round-30.md:52-56`).
13. **The 78 re-pointer partly holds.**
    - [obs] R30-UNSCREENED-TARGET (`:54`) carries 78's failing input: `check-self-assessment.py --selftest` control exit 2, "declared before (17 of 30)".
    - [obs] The C2 notes (`:42-47`) carry the probe's limits.
    - [obs] 78's main substance is the contract itself: drop `GIT_`, `GIT_CONFIG_NOSYSTEM`, private `HOME`/`XDG_CONFIG_HOME`, fixed `PATH`, ceiling. That is in neither re-pointed place. It is in the Gate rows S162 and S163 (`:21-22`) and routed item 4 (`:31`). C2 notes line `:44` names only the probe result.
    - Smallest correction: add "Gate rows S162/S163 and routed defect 4" to the 78 pointer.
14. **The 79 re-pointer is weak and risks false provenance.**
    - [obs] R30-DECLARATION-OVERCLAIM (`:53`) is about the declaration's novelty sentence for the allocation directory. It matches only 79's appended "Novelty is a property of bytes" tail, whose re-read substance is C1 notes `:37`.
    - [obs] 79's core is the row shape, digest-bound snapshot, quote starting within `line`, line-start `| [R30-Dnn] ` marker and 46/6 battery. That core has no Mistakes row in round 30. Its nearest anchor is C1 notes `:38` (counter v2, CritCounterShapes 39 of 49), and 79's own failing input cites `SCORECARD.md:1149` and `tools/mutants-btrfs-space-r30.py:10-13`, outside the lesson.
    - [inf] Saying "the substance of 79 is in … Mistakes R30-DECLARATION-OVERCLAIM" attributes the row-format rule to a declaration-sizing mistake.
    - Smallest correction: an appended line stating that 79's row-format rule has no round-30 Mistakes row, that its grounding is C1 notes `:38` plus `SCORECARD.md:1149`, and that DECLARATION-OVERCLAIM grounds only 79's novelty tail.
15. [obs] **No other files need the pointer correction.** The stale IDs remain outside QUALITY only in historical or wave files: `round-30-verifier-spotcheck.md:37,180`, round-30/31 w1 spec, dispatch and seat files, and `w2/RevQuality7779.md`. QUALITY `:149` and `:151` stay unchanged under append-only. No `SKILL.md` or `corpus/knowledge` file cites them (`git grep -n -o 'R30-GIT-RESIDUAL-CHANNELS\|R30-SOURCED-ROWS' f3a5723a`).

## Smallest safe corrections (no frozen rule, counter or target changes)

- **Score K6 and append to 80.**
  - Run K6 under the frozen counter with `run-receipt.py`, and commit the receipt after the keys are revealed (its statements contain keys).
  - Add "junk rows carrying dictionary-recovered key words" to the enumerated controls.
  - Change "a reader can satisfy with filler" to "a writer who never opens the source can satisfy".
  - Scope "Shown able to fail" to K0, K1 and K2, which fail at the pin and registry gate.
  - State that C1's 8 of 8 is a format count whose admission rests entirely on the wave-2 per-row reviews.
- **Commit the sealed builder and the K1/K5 control trees as patches** after keys are revealed, as the declaration promised. Without them, K1 and K5 are unreproducible from the lane.
- **Record round 31 as failing 80's clause "recorded with the declaration, not discovered after it"** for the synonym limit. This disclosure is what the clause demands. It is not a target change.
- **Replace the 64KiB example** with the actual defect: a key rule refused a writer's variant spelling ("64 KiB") that the source does not use. Alternatively, restate the clause as "accepts the orthographic variants of each source spelling".
- **Correct the receipt overclaim** in the declaration and counter docstring by an appended erratum: receipts carry the label, not the sentence.
- **Re-point 78 and 79** as in findings 13 and 14.

Scope: read=QUALITY.md, SCORECARD.md (round-31 declaration and errata), corpus/lessons/round-30.md, round-31.md and round-30-verifier-spotcheck.md, tools/check-btrfs-repair-r31.py, measure/ and measure/controls/ receipts and commit lists, w1/CritKeyDictionary.md, round-30 w2 CritClaimFraming2 fixture and output, fleet prompt tsukuroi-round-31.md:343-365, the six pinned snapshots (grep counts only), sealed builder (sha256 only), all at f3a5723a or base 2077e2fa; wrote=.ufo/waves/round-31/w2/CritQuality80.md, .ufo/waves/round-31/w2/CritQuality80/k6-run.jsonl, /fast/scratch/hyaku/tsukuroi-r31/CritQuality80/ (exports, repo sandbox clone with K3 and K6 commits, k6-keys.json, k6-run.jsonl); executed=read-only git show, log, grep, ls-tree and cat-file in the lane; env -u GIT_* git clone, checkout, am and commit only in /fast/scratch/hyaku/tsukuroi-r31/CritQuality80/repo; python3 tools/check-btrfs-repair-r31.py on sandbox K3 (0 of 8, exit 1) and K6 (8 of 8, exit 0); python3 dictionary hash recovery and sentence compare; sha256sum, find, rg
Model: not exposed
Installs: none
