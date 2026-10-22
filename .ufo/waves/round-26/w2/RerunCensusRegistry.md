# RerunCensusRegistry: rerun of census, registry coverage and memory-pressure checks

Verdict: holds. Every assigned check exits 0 with the expected values. The census reads 139 rows, 25 W04 warnings (S136, S137 and S138 among them) and no E finding. Registry coverage passes with 29 of 29 rows and 29 of 29 tools covered. Memory pressure passes with 6 of 6 rows verified. One caveat: my memory-pressure run used the HEAD copy of the checker (7f9f088), which differs from the copy pinned at 4de2b6b. Both copies give the same verdict at revision 7dfea92 (Finding 6).

Terms used below: "working copy" is the lane checkout at HEAD 7f9f088. "Measured revision" is 7dfea92. "Pinned base" is 4de2b6b, the commit that pins the round-26 tools and comes before the round-26 source rows S128 to S139 landed (commit ef72f10). "W04" is the validator warning for one URL cited under two different scope strings; it is a warning only and does not change the exit code. "E" findings are the validator's error classes E01 to E12.

## Results

| Command (run from the lane root unless noted) | Exit | Result |
|---|---|---|
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | 0 (run twice) | One `ok` line for tsukuroi, 25 `W04` lines, no E lines, no W01/W02/W03 lines |
| Frozen census, CORPUS.md line 135 (row count) | 0 | 139 |
| Frozen census, line 137 (malformed rows, must be 0) | 0 | 0 |
| Frozen census, line 139 (tier histogram) | 0 | A=129 B=3 C=7 (sums to 139) |
| Frozen census, line 141 (status histogram) | 0 | mined=125 queued=5 rejected=9 (sums to 139) |
| Frozen census, line 143 (duplicate ids, must print nothing) | 0 | prints nothing |
| Frozen census, line 145 (enum and tier inflation, must print nothing) | 0 | prints nothing |
| Frozen census, line 147 (mined rows with missing used-by paths, must print nothing) | 0 | prints nothing; 231 used-by path entries checked |
| `python3 tools/check-registry-coverage.py --revision 7dfea9244a84a0e2439f0698e54491e5d7b7c467` | 0 | PASS; registered 29, rows_total 29, tools_total 29, missing 0, findings 0 |
| `python3 tools/check-memory-pressure.py --revision 7dfea9244a84a0e2439f0698e54491e5d7b7c467` | 0 | PASS; verified_rows 6 of declared_rows 6; findings none |

Row count is 139, inside the expected 127 to 139 window. The pinned base has 127 rows. Tier and status histograms are given above. The W04 count is 25, inside the expected 22 to 25 window. The 25 W04 ids are S038, S041, S042, S043, S044, S046, S049, S058, S082, S087, S089, S090, S092, S095, S098, S105, S106, S107, S108, S109, S111, S126, S136, S137 and S138. The first 22 of these are exactly the W04 ids at the pinned base, and S136, S137 and S138 are the three new ones. E findings: none. The validator's only finding codes are W04 (25) and ok (1).

## Findings

1. [obs, holds] The census on the working copy equals the census on the measured-revision bytes. The sha256 of corpus/SOURCES.md is 9573a318737019ae871c8b8b050621562088ce839a1c2b4520f531eae0949fcf (137022 bytes) in the working copy, at HEAD 7f9f088 and at 7dfea92 (read with `git show`). `git diff --quiet 7dfea92 -- corpus/SOURCES.md` exits 0. The seven frozen commands and the validator, run on a git-archive sandbox of 7dfea92 (/fast/scratch/hyaku/tsuku26/w2/RerunCensusRegistry/rev-7dfea92/tsukuroi-shokunin), give the same outputs as the working copy. Only corpus/QUALITY.md (+2 lines) and corpus/lessons/round-26.md (+9 lines) differ between 7dfea92 and HEAD. SKILL.md and both capture directories are unchanged.

2. [obs, holds] The row and W04 deltas match the round-26 additions exactly. Pinned base 4de2b6b: ids S001 to S127 with no gaps, 127 rows, tiers A=117 B=3 C=7, statuses mined=113 queued=5 rejected=9, 22 W04. Working copy: ids S001 to S139 with no gaps, 139 rows, tiers A=129 B=3 C=7, statuses mined=125 queued=5 rejected=9, 25 W04. The ids present in the working copy but not the base are exactly S128 to S139, all tier A and status mined (corpus/SOURCES.md lines 134 to 145). No base id was removed. The three new W04 rows are S136 (line 142), S137 (line 143) and S138 (line 144). Each teaches cell begins with "supersedes" and names an earlier row with the same URL: S136 names S121 (line 127), S137 names S122 (line 128), and S138 names S118 (line 124). The W04 warning on S126 (line 132, supersedes S120) was already present at the pinned base.

3. [obs, holds] No E finding in any census or validator check. Malformed rows (field count not 13): 0. Duplicate ids: none. Tier or status enum breaks, kind breaks and tier-A community rows: none. Mined rows whose used-by paths are missing on disk: none, and the validator's E11 check agrees. The validator's finding codes are defined at scripts/sources-census.sh lines 24 to 33. Its exit-code rule (line 16) is 0 for clean or warnings-only lanes and 1 for E or overdue findings. Saved output: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RerunCensusRegistry/validate.txt.

4. [obs, holds] Registry coverage is bound to revision 7dfea92 and independently confirmed. The checker reads SKILL.md with `git show <rev>:SKILL.md` (tools/check-registry-coverage.py line 106, called at line 380) and lists tools with `git ls-tree` at the revision (lines 67 and 84 to 86). Independent counts at 7dfea92: the round-26 registry section of SKILL.md has 29 data rows (one header), and tools/ holds 29 files (27 .py and 2 .sh). The checker's selftest exits 0 with 23 of 23 passing. Comparing against the pinned base with `--baseline-tools 4de2b6b` exits 0 with baseline_tools_total 29, baseline_tools_missing 0 and discovered_tools empty. The checker file itself is byte-identical at 4de2b6b and in the working copy.

5. [obs, holds] The memory-pressure sha256 in the output is the round-25 capture, not the round-26 frozen capture. The output field capture_sha256_observed is e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136. The checker pins that value for its own capture, `.ufo/waves/round-25/capture/capture.txt` (tools/check-memory-pressure.py lines 66 and 67; SKILL.md line 2305). It is not a tamper signal. The round-26 frozen capture `.ufo/waves/round-26/capture/capture.txt` hashes to 002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd in the working copy and in the 7dfea92 git blob (7329 bytes), as the task requires. The round-25 capture also matches its pin at 7dfea92 (`git show` piped to sha256sum gives e60f1bbc). The checker's selftest exits 0 with 41 of 41 cases passing.

6. [obs, low] The memory-pressure run used a checker version that is not the pinned one, but the verdict does not change. The pinned tools commit is 4de2b6b. `tools/check-memory-pressure.py` differs between 4de2b6b and HEAD 7f9f088 by 183 lines (159 insertions, 24 deletions). The HEAD commit message reads "memory-pressure checker hardened". The tools/ tree at 7dfea92 is identical to 4de2b6b, so the measured revision used the pinned file. My `--revision 7dfea92` run used the HEAD file. To test whether that matters, I read the pinned file with `git show 4de2b6b:tools/check-memory-pressure.py` and executed it in-process, with its file path set to the lane's tools directory so that it resolved the lane as its root and read every input through git at 7dfea92. The lane was not written to. Results: exit 0, PASS, verified 6 of 6, zero findings, the same observed capture sha. The per-row output is identical except that the HEAD copy adds a tier field to each source record (sources[].tier). The pinned selftest exits 0 with 32 of 32 cases passing, against 41 of 41 for HEAD. Comparison file: /fast/scratch/hyaku/tsuku26/w2/RerunCensusRegistry/mp-pinned-vs-head.json. Any receipt that claims the 4de2b6b pin should state which file produced it.

7. [obs, low] The frozen used-by check at CORPUS.md line 147 cannot fail on its exit status. It ends in a `while read` loop, so its exit status is 0 whether or not a "missing:" line prints. Only the printed output carries the signal, and here that output is empty. The maintained validator covers the same ground with its E11 check, and it found no missing used-by path, so the gap is closed for this lane.

8. [obs, info] S138 cites the same URL as S118 (raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst) under a scope string that differs only by the words "including their hierarchy" (corpus/SOURCES.md lines 124 and 144). Its teaches cell declares "supersedes S118", so the W04 warning is an accepted one, not an error. Any later row that re-cites a URL under a slightly different scope string will also produce W04.

9. [obs, none] Side effects on the lane. The lane's working tree is not changed by this seat. `git --no-optional-locks status --porcelain -- tools/ corpus/ SKILL.md` lists no entries. The `tools/__pycache__/` directory is git-ignored (.gitignore line 2) and holds three .pyc files with timestamps 08:56, 10:52 and 11:21, all before this seat's first run. This seat added none. All outputs of this seat are listed under "Files" below.

10. [unk] Outside this seat's scope. I did not check the content of S128 to S139 (quotes, raw-bytes digests, anchors or the sources themselves). I did not run check-storage-health.py or check-self-assessment.py, and I did not check the wave-1 receipts. The C1 and C2 seats should cover those.

## Commands executed (all read-only toward the lane)

- Validator: the working-copy run plus two runs on sandboxes with explicit lane directories (exit 0 each).
- Frozen census: lines 135, 137, 139, 141, 143, 145 and 147 of CORPUS.md, extracted and run verbatim from the file, on the working copy and on both sandboxes (exit 0 each).
- Registry: `--revision 7dfea92…`, `--selftest`, and `--revision 7dfea92… --baseline-tools 4de2b6b…` (exit 0 each).
- Memory pressure: `--revision 7dfea92…` and `--selftest` on the HEAD copy (exit 0 each); the pinned 4de2b6b copy loaded from `git show`, run in-process against 7dfea92 and its selftest (exit 0 each).
- Read-only git: rev-parse, log, merge-base --is-ancestor, cat-file, show, ls-tree, diff, diff --quiet, and status with --no-optional-locks. Sandboxes were built with `git archive <rev> | tar -x` and then `git init` with no remote.
- Hashing and counting: sha256sum, awk, grep, sort, comm.

## Files

- Report: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RerunCensusRegistry.md (this file).
- Seat directory in the lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RerunCensusRegistry/validate.txt.
- Scratch directory: /fast/scratch/hyaku/tsuku26/w2/RerunCensusRegistry/ holds census-working.json, census-rev-7dfea92.json, census-rev-4de2b6b.json, validate-working.txt, validate-rev-7dfea92.txt, validate-rev-4de2b6b.txt, mp-pinned-vs-head.json, ids-base.txt, ids-working.txt, and the git-archive sandboxes rev-7dfea92/ and rev-4de2b6b/ (each with `git init` and no remote).

Scope: read=CORPUS.md lines 120-160; SOURCES.md at the working copy, 7dfea92 and 4de2b6b; SKILL.md (working copy, registry sections); tools/check-registry-coverage.py and tools/check-memory-pressure.py (working copy and the 4de2b6b blob); scripts/sources-census.sh (header and finding codes); .ufo/waves/round-26/capture/capture.txt and the round-25 capture blob; git metadata and diffs (read only); skill://godspeed; /home/vgpnk/.omp/agent/RULES.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RerunCensusRegistry.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RerunCensusRegistry/validate.txt, /fast/scratch/hyaku/tsuku26/w2/RerunCensusRegistry/ (outputs, id lists, git-archive sandboxes rev-7dfea92 and rev-4de2b6b); executed=sources-census.sh validate (working copy and two sandboxes); frozen census commands at CORPUS.md lines 135-147 (working copy and two sandboxes); check-registry-coverage.py --revision 7dfea92, --selftest, and --baseline-tools 4de2b6b; check-memory-pressure.py --revision 7dfea92 and --selftest; pinned 4de2b6b check-memory-pressure.py run in-process against 7dfea92 and its selftest; git rev-parse, log, merge-base, cat-file, show, ls-tree, archive, init (sandboxes only), diff, diff --quiet, status --no-optional-locks; sha256sum; awk, grep, sort, comm
Model: anthropic/claude-haiku-5-5 (from the workstation context block of my system prompt; not separately confirmed by the runtime)
Installs: none
