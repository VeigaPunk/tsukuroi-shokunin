# CritClaimFraming2 — round 30, wave 2 (second framing attack at 29bf87fa)

Partly holds. C1 is verified as a count under the declared v1, but it is not verified as depth. C2 is verified as a count under the declared probe, but its after-receipt is not committed at the tip. The depth ordinal 8 → 8 is justified, and no move would be. The committed round-30 records are incomplete, and the uncommitted lesson draft overcounts depth.

Per-claim verdicts:
- **C1 count: verified.** The declared v1 (`1bf7ee14…`) reads 10 of 10 with exit 0 at `a3f19372` (committed receipt) and at the tip (my sandbox run).
- **C1 as depth: partly holds.** 4 of the 10 rows are firm new depth and 1 is thin. Both v1 and v2 give 10 of 10 to a fixture that contains no btrfs source at all.
- **Counter v2: not attacked before use.** The claim is still judged on v1.
- **C2 count: verified.** The declared probe (`c8f61996…`) reads 0 of 33 with empty `harness_errors` at `a3f19372` and at the tip. However, its `a3f19372` receipt is untracked, so under the lane's own QUALITY 77 the after-value is not yet admissible.

## Findings

1. **C1 count under the declared v1: verified.**
   - [obs] Committed receipt `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/measure/after-a3f19372/c1-declared-v1.jsonl:1,12-13`:
     - `tool_revision` is `8fb2cef0`;
     - `tool_sha256` is `1bf7ee14…c079`;
     - the last line reads `"verified": 10, "of": 10` with `exit_code 0`.
   - [obs] `SKILL.md` changed between `a3f19372` and the tip (`git diff --stat a3f19372 29bf87fa` shows `SKILL.md | 3 +-`). So I re-ran the v1 bytes (`git show 8fb2cef0:tools/check-btrfs-space-r30.py`, sha256 `1bf7ee14…c079`) at the tip from the sandbox clone with `--revision 29bf87fa… --lane /fast/scratch/hyaku/tsukuroi-r30/CritClaimFraming2/repo`.
     - Result: exit 0, `"verified": 10, "of": 10`.
     - Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/CritClaimFraming2/out-v1-tip.txt` (sha256 `aee17a1d…`).
   - [obs] All ten quotes occur verbatim on their cited snapshot lines (python check of `quote in line[line-1]`: 10 of 10 report "verbatim-on-line").

2. **The counter does not measure depth: v1 and v2 both give a trivial fixture 10 of 10.**
   - [obs] I built a new fixture designed to pass v2's added rules (`build_trivial_v2.py`, sha256 `5ca091bb…`):
     - the snapshot is the v2 counter's own source (no btrfs bytes);
     - quotes come from its `ROWS` comments and docstring;
     - each statement is 11 filler words plus the row's frozen token;
     - the host capture is a hand-written three-line file, `allocation/metadata/bytes_used: 7`, `unallocated: 8` and `allocation/global_rsv_size: 9` (`fixture-v2self-capture.txt`, sha256 `e8f4b827…`);
     - the `SKILL.md` markers sit in a minimal pipe table.
   - [obs] Results:
     - `python3 ctr-v2.py --tree fx/v2self --base-sources base-SOURCES.md` gives exit 0, `"verified": 10, "of": 10, "counter_version": 2` (`out-v2self.txt`, sha256 `960f060a…`);
     - the same tree under v1 also gives 10 of 10 (`out-v2self-under-v1.txt`, sha256 `dce494f3…`).
   - [inf] v2's new R8 capture-key check only requires that the key text appears on the line. Any authored text file under `.ufo/waves/round-30/` satisfies it.
   - [obs] v2 did not adopt any of wave-1 CritClaimFraming's three content corrections:
     - statement bound to the question (R3');
     - snapshot bytes new at the base (R4');
     - a pinned sysfs capture (R8').
   - The docstring at `/fast/scratch/hyaku/tsukuroi-r30/CritClaimFraming2/repo/tools/check-btrfs-space-r30.py:20-44` has R3 at 12 words only and R4 on registry cells only. The battery has no shape for re-registered base bytes or for an authored capture line (shape list, `tools/mutants-btrfs-space-r30.py:180-272`).

3. **Three "opened this round" sources are byte-identical to blobs committed at the claim base `fbfec6bd`. Two of them duplicate registry rows that already exist.**
   - [obs] Method: `git hash-object` of each snapshot, compared against `git ls-tree -r fbfec6bd` (list at `/fast/scratch/hyaku/tsukuroi-r30/CritClaimFraming2/base-blobs.txt`):
     - S155 `S155-mkfs.btrfs.rst` (blob `0d3d6051…`) equals `.ufo/waves/round-26/sources/S130.rst`. The registry rows carry the same raw sha256: `ce7c0cbca90e…` in S130 (`corpus/SOURCES.md:136`) and S155 (`:161`), with the same URL.
     - S158 `S158-sysfs.c` (blob `0d14570c…`) equals `.ufo/waves/round-26/sources/S133.c`. The same sha256 `ce146120f29a…` appears in S133 (`:139`) and S158 (`:164`), with the same URL.
     - S154 `S154-ch-sysfs.rst` (blob `6232f98c…`, sha256 `295b9265…`) equals the round-26 supporting file `.ufo/waves/round-26/w1/SrcKernelSysfs/supporting-btrfs-progs-v7.1-ch-sysfs.rst`.
   - [obs] D10's quote `BTRFS_ATTR(allocation, global_rsv_size, global_rsv_size_show);` is already present at the base as `fbfec6bd:.ufo/waves/round-26/sources/S133.c:679` (`git grep -n -F global_rsv fbfec6bd`).
   - [obs] None of the S154, S155 or S158 rows names S130, S133 or round 26 (grep over the row cells). The knowledge entry and the lesson draft do not disclose the byte identity either.
   - [inf] Two source ids for one URL at one sha256 creates duplicate authorities in the registry.
   - [obs] QUALITY 79 (`corpus/QUALITY.md:151`) codifies novelty as "absent from the base `fbfec6bd` registry", which is a test on the id. So the round's new criterion encodes this gap.
   - Rows affected: D04 (S155), D05 and D08 (S154), D06 and D10 (S158).

4. **New depth: 4 of 10 firm, plus 1 thin. The lane's committed record says 8 of 10.** Count, with reasons:
   - **New depth (4):**
     - D01 (S159 `space-info.c`, new bytes; `unallocated` has 0 base hits);
     - D02 (S152 plus the S156 512 MiB cap, new bytes; `Global reserve` and `global_rsv` have 0 base hits in `SKILL.md`, `corpus/` and `PROVINCE.md`);
     - D03 (S153, new bytes; `usage=` and `dusage` have 0 hits);
     - D07 (S157, new bytes; `share all`, `shared extent` and `extents` have 0 hits).
     - [obs] Hit counts: `git grep -c -i -F` at `fbfec6bd` over `SKILL.md corpus/ PROVINCE.md`.
   - **Thin (1): D05.** `bg_reclaim` has 0 base hits, but:
     - the source bytes have been in the lane since round 26 (finding 3);
     - the row leaves the operating answer open: "what 0 means is not stated by this chapter" (JSON D05; `SKILL.md:2610` marks it `[unk]`).
     - [obs] The lane's own S159 snapshot answers it for the periodic path, at `/fast/scratch/hyaku/tsukuroi-r30/CritClaimFraming2/repo/.ufo/waves/round-30/w1/ScribeSrcSpaceInfo/S159-space-info.c` (sha256 `5654929f…`):
       - lines 2111-2117: `btrfs_calc_reclaim_threshold` returns `bg_reclaim_threshold` when `dynamic_reclaim` is 0 (capture line 57 reads 0);
       - line 2154: `thresh = mult_perc(bg->length, thresh_pct)`;
       - line 2155: `if (bg->used < thresh && bg->reclaim_mark)`.
     - [inf] With `thresh_pct` 0, no block group is marked for periodic reclaim.
     - [unk] The `block-group.c` paths were not opened.
   - **Restatement (2):**
     - D04 (DUP: `SKILL.md` SH3 at `fbfec6bd:SKILL.md:2367` and S130, with S155 the same bytes);
     - D06 (allocation directory: SH3; S158 is the same bytes as S133). D06's only increments are the `global_rsv_*` file names and the world-readable mode.
   - **Captures, not durable depth (3): D08, D09 and D10.**
     - [obs] D09's `capture_line` 98 is not a sysfs file. It is an arithmetic line written by the executor (`ExecHostCapture/btrfs-allocation-capture.txt:97-98`, sha256 `853afe89…`): "Derived block (bytes; operands cited by capture line)". The declaration promised "values from a read-only sysfs capture" (`SCORECARD.md:1146`).
     - [obs] The value is still correct: `btrfs-filesystem-usage.out.txt:4` reads `Device unallocated:		      690922455040`.
   - **The lane's own count.** `corpus/knowledge/btrfs-space-r30.md:12` (committed) reads "the other eight rows are new to the lane". The uncommitted draft `corpus/lessons/round-30.md:37,53` says D08–D10 are new and "eight of ten rows are new". That count includes captures as depth, and it omits finding 3.

5. **The depth ordinal 8 → 8 is justified (it was declared, and it holds). A move would not be.**
   - [inf] 4 to 5 firm rows out of 10, a counter that a sourceless fixture satisfies (finding 2), and re-registered base bytes (finding 3) cannot support 8 → 9.
   - [inf] This round is better than round 29's 4 of 12. The difference is not large enough to escape the round-28/29 lowest-axis dispute, which stays with the operator.

6. **Counter v2 was not attacked before use. The claim is still judged on v1.**
   - [obs] v2 was first committed in `a3f19372` (`git log -- tools/check-btrfs-space-r30.py`: only `8fb2cef` and `a3f1937`). The commit time is 18:28:09 -0300 (21:28:09Z).
   - [obs] Its first counted run is the receipt `c1-v2.jsonl` at `started_utc` 21:28:24Z, 15 seconds later. Battery v2 was run by the same runner at 21:28:25Z (`c1-battery-v2-counter-v2.jsonl:1`).
   - [obs] No wave-1 artifact names the v2 digest: searching `.ufo/waves/round-30/w1/` for `4953203d` finds nothing. The non-author attack on v2 is wave 2, which comes after its use.
   - [obs] Judged on v1:
     - the receipts header names `tool_sha256 1bf7ee14…` for the declared run;
     - the v2 docstring (`tools/check-btrfs-space-r30.py:4-5`) and `corpus/lessons/round-30.md:38` say "The claim is judged on the declared v1".
   - [obs] One coupling: rows were edited to suit the frozen counter. The lesson draft says "Two data rows moved to quotes both versions accept (D05 to S154 line 169; D06 to S158 line 1068)" (`corpus/lessons/round-30.md:38`). The moved quotes are verbatim (finding 1). This is tuning the data to v1 after seeing its refusals, and it is disclosed only in an uncommitted file.
   - [obs] Under v1, battery v2 accepts 20 of 72 should-fail shapes and refuses 5 of 11 should-pass shapes (`c1-battery-v2-counter-v1.jsonl` footer `exit_code 1`). So v1's 10 of 10 is weaker evidence than v2's, and v2's in turn falls to finding 2.

7. **C2 under the declared probe: the count is verified. The after-receipt is uncommitted, and the before-value framing needs the restated before.**
   - [obs] The probe at the tip is byte-equal to the declared bytes, sha256 `c8f61996…` both from the file and from `git show 8fb2cef0:`.
   - [obs] My sandbox run at the tip (`--revision 29bf87fa… --lane <sandbox>`):
     - result: `"pairs": 33, "leaking": 0, "leaking_pairs": [], "harness_errors": []`, with 33 `"leak": false` lines and empty stderr;
     - evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/CritClaimFraming2/out-c2-tip.jsonl` (sha256 `6db48f13…`).
     - [obs] Exit code 0 (`probe exit=0`, wall time 76.5 s). A second run at the tip also exited 0 with the same summary (71.7 s). This matches the probe's rule at `tools/probe-git-env-residual-r30.py:263` (`return 2 if errors else (1 if leaking else 0)`).
   - [obs] The L1's after-receipt `.ufo/waves/round-30/measure/after-a3f19372/c2-declared-probe.jsonl` (sha256 `6be58c3a…`) reads 0 of 33 with exit 0. However:
     - it is untracked in the lane (`git status --short` lists it as `??`);
     - `git ls-tree -r --name-only 29bf87fa -- .ufo/waves/round-30/measure | grep -c c2-declared` gives 0;
     - commit `29bf87fa`'s message lists only "C1 and gate receipts".
     - Under the round's own QUALITY 77 (`corpus/QUALITY.md:147`, "admissible only with a committed receipt"), the C2 after-value is not yet admissible. The lesson draft cites this path at `corpus/lessons/round-30.md:44`.
   - [obs] **Before-value.** The honest before is at least 19 of 33, not 17 of 30. The lesson draft now says so (`:54`, R30-UNSCREENED-TARGET), and it notes that 10 of the 17 measured leaks were path-wrapper log hits with no change in outcome (`:46`).
     - The three `check-self-assessment` pairs became measurable only after the `--selftest` dispatch was moved ahead of the `.git` check (`git diff 8fb2cef0 29bf87fa -- tools/check-self-assessment.py`, hunk at old `:1071-1083`). That is a harness repair, not a channel fix.
     - The path-wrapper fix pins `"PATH": "/usr/bin:/bin"` (same diff, `git_env`). That is a hermeticity-versus-operator-choice tradeoff, not a pure gain.

8. **The round-30 records in `SCORECARD.md` and `LOG.md`: no outcome record exists yet, and the declaration's false sentence stands uncorrected in any committed record.**
   - [obs] `git diff 8fb2cef0 29bf87fa -- SCORECARD.md LOG.md | wc -l` gives 0, and `grep -c 'Round 30\|round 30\|round-30' LOG.md` gives 0.
   - [obs] `SCORECARD.md:1142` still reads "the allocation sysfs files have 0 hits" (`sed -n '1142p' … | grep -cF` gives 1).
   - [obs] Committed disclosures exist only in `corpus/knowledge/btrfs-space-r30.md:12` (D04 and D06 restate) and in the v2 docstring (`tools/check-btrfs-space-r30.py:10-13`).
   - [obs] The honest-limits text is in the uncommitted draft `corpus/lessons/round-30.md`: R30-DECLARATION-OVERCLAIM at `:53`, the 19-of-33 before at `:54`, the v1/v2 split at `:38`, and the probe blind spots at `:45`. It has the gaps from findings 3 and 4.
   - [obs] At the tip, the S152–S159 used-by cells name `corpus/lessons/round-30.md` (for example `corpus/SOURCES.md:160-164`, column 12). That file is absent at `29bf87fa` (`git ls-tree -r --name-only 29bf87fa -- corpus/lessons | grep round-30` is empty), so those cells point to a path that does not exist at the revision.

## Impacted axes
- **depth:** 8 of 10 is overcounted to the record; the honest count is 4 to 5. Sources are re-registered from base bytes, and the counter is gameable under v2 too.
- **calibration:** the premise sentence is uncorrected in committed records; the novelty test in QUALITY 79 checks only the id; the C2 receipt is uncommitted.
- **operability:** C2 holds at 0 of 33; the path-wrapper fix carries a PATH tradeoff, and the self-assessment harness repair is folded into the claim.
- **adjacency:** no new harm. The mori split is disclosed at `corpus/knowledge/btrfs-space-r30.md:10`.

## Smallest safe corrections
1. Commit `after-a3f19372/c2-declared-probe.jsonl`, `r29-probe-git-env-leak.jsonl` and `corpus/lessons/round-30.md` before any report row cites them (QUALITY 77).
2. The round-30 outcome record (`SCORECARD.md` append and `LOG.md`) should say:
   - the C1 depth content is D01–D03 and D07, with D05 thin;
   - D04 and D06 are restatements;
   - D08–D10 are captures, and D09 is a derived line (cite `btrfs-filesystem-usage.out.txt:4` as the measurement);
   - S155 is the same bytes as S130, S158 is the same bytes as S133, and S154 is the same bytes as round 26's supporting `ch-sysfs.rst`;
   - C2's before is at least 19 of 33.
3. Resolve the duplicate authorities. Either extend S130 and S133 (anchor and used-by) and withdraw S155 and S158, or annotate S155 and S158 "same bytes as S130/S133, re-read 2026-10-22". Do not count them as new sources.
4. Next counter version and battery:
   - snapshot blob not reachable at `fbfec6bd`;
   - each capture line must start with `/sys/fs/btrfs/` or come from a named tool-output file whose sha is pinned;
   - the statement must contain the row's frozen token;
   - add battery shapes for the `build_trivial_v2.py` fixture and for re-registered base bytes.
   - Change QUALITY 79's novelty clause from registry id to snapshot bytes.
5. D05: either cite S159:2111-2117 and 2154-2155 for the periodic path with threshold 0, or keep the `[unk]` and stop counting D05 as answered depth.

Scope: read=SCORECARD.md:1125-1153, .ufo/waves/round-30/w1/CritClaimFraming.md, corpus/lessons/round-29-verifier-spotcheck.md:60-160, corpus/knowledge/btrfs-space-r30.json and .md:10-12, SKILL.md:2600-2625 and registry rows, corpus/SOURCES.md:136-169, corpus/QUALITY.md:145-151, tools/check-btrfs-space-r30.py v1 and v2 docstrings, tools/mutants-btrfs-space-r30.py:1-40 and shape list, tools/check-self-assessment.py diff 8fb2cef0..29bf87fa, probe exit rule, ExecHostCapture capture and usage outputs, S159 snapshot lines 168-183 and 2090-2165, S156:390-396, S154:160-172, S153:48-56, measure/ and measure/after-a3f19372/ receipts, uncommitted corpus/lessons/round-30.md, git ls-tree at fbfec6bd and 29bf87fa; wrote=.ufo/waves/round-30/w2/CritClaimFraming2.md, .ufo/waves/round-30/w2/CritClaimFraming2/{build_trivial_v2.py,fixture-v2self-btrfs-space-r30.json,fixture-v2self-capture.txt,out-v2self.txt,out-v2self-under-v1.txt,out-v1-tip.txt,out-v2-tip.txt,out-c2-tip.jsonl}, /fast/scratch/hyaku/tsukuroi-r30/CritClaimFraming2/ (clone at 29bf87fa, ctr-v1.py, ctr-v2.py, base-SOURCES.md, base-blobs.txt, fx/v2self, probe outputs); executed=read-only git log/show/diff/status/ls-tree/ls-files/grep/hash-object on the lane and sandbox, git clone --no-local and checkout in scratch, python3 ctr-v1.py and tools/check-btrfs-space-r30.py --revision 29bf87fa (exit 0, 10 of 10 each), python3 build_trivial_v2.py, ctr-v2.py and ctr-v1.py --tree fx/v2self (exit 0, 10 of 10 each), python3 tools/probe-git-env-residual-r30.py --revision 29bf87fa --lane <sandbox> twice (both exit 0, leaking 0 of 33, harness_errors [])
Model: not exposed
Installs: none
