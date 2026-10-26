VERDICT: supports

# ConsiderWeight — A-2 "Evidence-weight watch" (round-39 w1, considerthese/2026-10-25.md)

Item implemented as a measurement on committed history: rounds 30–38 per-round bytes under
`.ufo/waves/round-N/` and under `corpus/`, the largest single files, plus round 39 so far.
Read-only seat: no tracked lane file was created, edited or deleted; every number below comes
from `git ls-tree`/`git log` reads at lane tip `394e1ba` (round-39 w1 still in flight) and from
`find` on the live working tree at the stamped times.

## 1. Method — exact commands

Definitions used, so the numbers are reproducible and falsifiable:

- **Round span** = the contiguous `--first-parent` commits on `master` whose subject starts
  `round-N`, from the first such commit to the last (`round-38 verifier spot-check` closes a
  round). Verified contiguous and disjoint for N=30..39; only `d9099b2`/`f0b8f7a`/`09045c5`
  (`considerthese:` reflections) sit inside the window untagged.
- **Round start rev** = the parent of the round's first commit.
- **Bytes** = committed tree byte sizes from `git ls-tree -r -l` (content as checked out),
  *not* pack size. `ls-tree -l` prints `<mode> <type> <sha> <size>\t<path>`, so `$4` is the size.
- **Evidence:prose** = round `.ufo/` delta ÷ round `corpus/` delta.

```bash
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin

# R1. the round's commit span (--reverse, so the first line is the round's first commit)
git log --first-parent --format='%h %ad %s' --date=short --grep '^round-36' master

# R1b. dispatched seats for the round (items in the frozen wave spec)
git show master:.ufo/waves/round-36/w1-spec.json | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["items"]))'

# R2. evidence bytes in the round's dir (committed, as checked out)
git ls-tree -r -l master -- .ufo/waves/round-36 | awk '{s+=$4} END{print s, NR}'

# R3. heaviest single files in that dir
git ls-tree -r -l master -- .ufo/waves/round-36 | sort -k4 -n | tail -3 | awk '{print $4, $5}'

# R4. knowledge growth over the round span (S = first round commit's parent, E = last round commit)
S=$(git rev-parse $(git log --first-parent --format=%H --grep '^round-36' --reverse master | head -1)^)
E=$(git log --first-parent --format=%H --grep '^round-36' master | head -1)
git ls-tree -r -l "$E" -- corpus | awk '{s+=$4} END{print s}'
git ls-tree -r -l "$S" -- corpus | awk '{s+=$4} END{print s}'
git ls-tree -r -l "$E"          | awk '{s+=$4} END{print s}'
git ls-tree -r -l "$S"          | awk '{s+=$4} END{print s}'

# R5. duplicate blobs under the wave dirs (git stores one copy; every checkout pays per path)
git ls-tree -r -l master -- .ufo/waves | awk '{print $3, $4}' | sort \
 | awk '{c[$1]++; s[$1]=$2} END{for(k in c) if(c[k]>1) e+=s[k]*(c[k]-1); print e}'

# R6. round-39 so far: committed, then live working tree
git ls-tree -r -l master -- .ufo/waves/round-39 | awk '{s+=$4;n++} END{print n, s}'
find .ufo/waves/round-39 -type f -printf '%s\n' | awk '{s+=$1;n++} END{print n, s}'

# R7/R8. the commit that added 87.7 MB, and what one heavy file really costs
git show --stat --format='' fe24c4c | tail -1
git show master:.ufo/waves/round-36/w1/ExecLiveViewDesign/capture/base-final-6d76fb20/handoff.execve.log | gzip -9 | wc -c
git verify-pack -v .git/objects/pack/*.idx | grep '^61bae29e1d3d860fb95f0201b51a96b2b8a56c19 '
```

Observed outputs of the checked commands (run in this seat): R2 `102534030 1444`; R4
`2806746` / `2757897` (corpus at close / start of round 36); R5 `24699165`; R6 `48 2073917`
(committed) and `308 3988014` (working tree at 2026-10-26 03:07 local); R7
`5 files changed, 126033 insertions(+)`; R8 `809151` and `45594475 1164118`.

Receipts kept beside this report: `ConsiderWeight/table.tsv` (the table as TSV),
`measurement.json` (machine form, with span commit ids), `top-files.txt`, `dup-blobs.txt`,
`late-writes.txt`, `commands.sh` (the block above, runnable).

## 2. Per-round table

| round | commits | seats | dir B @ round close | files | B/seat | dir B @ master | corpus Δ | evidence:prose | tree B @ close |
|---|---|---|---|---|---|---|---|---|---|
| 30 | 11 | 35 | 8,871,112 | 588 | 253,460 | 8,747,378 | 95,260 | 93.1× | 77,584,672 |
| 31 | 9 | 33 | 11,790,988 | 739 | 357,303 | 11,790,988 | 79,511 | 146.7× | 89,414,375 |
| 32 | 12 | 34 | 15,830,434 | 713 | 465,601 | 15,831,180 | 47,332 | 334.5× | 105,422,631 |
| 33 | 14 | 45 | 5,022,994 | 595 | 111,622 | 5,022,994 | 67,675 | 74.2× | 110,614,019 |
| 34 | 8 | 39 | 8,386,828 | 690 | 215,047 | 9,127,754 | 58,955 | 142.3× | 119,198,737 |
| 35 | 8 | 37 | 18,137,294 | 1,486 | 490,197 | 20,071,399 | 59,325 | 318.2× | 138,255,578 |
| 36 | 10 | 32 | 102,534,030 | 1,444 | 3,204,188 | 102,534,030 | 48,849 | 2138.6× | 242,902,628 |
| 37 | 20 | 64 | 16,154,164 | 742 | 252,409 | 16,154,164 | 56,511 | 285.9× | 259,239,836 |
| 38 | 10 | 71 | 6,464,189 | 740 | 91,045 | 6,464,189 | 87,564 | 73.8× | 265,861,270 |
| 39 | 6 | 70 | 2,073,917 | 48 | 29,627 | 2,073,917 | 12,159 | 170.6× | 267,983,346 |

Totals 30–38: **193,192,033 B** in the ten evidence dirs, **600,982 B** of `corpus/` growth,
**197,413,067 B** of whole-tree growth. At master `.ufo/waves` is 261,260,656 B (97.5% of the
267,983,346 B tree) and rounds 30–39 are 74.7% of it; `corpus/` is 2,962,980 B.

Footnotes: "seats" is `len(items)` in the round's frozen `w1-spec.json` (round 33 uses
`a3w1-spec.json`, its attempt-3 spec); "dir B @ round close" is measured at the round's last
`^round-N` commit, "dir B @ master" at `394e1ba` — the two differ wherever a later round wrote
into the dir (F5). Round 39 has no close yet: its row is the committed state at `394e1ba`, and
the live working tree is 3,988,014 B (see §4).

## 3. Largest single files

Heaviest file per round (share of that round's dir):

| round | file | bytes | share |
|---|---|---|---|
| 30 | `w2/SentinelProbeHollow/runs/batteries.jsonl` | 1,728,561 | 19.8% |
| 31 | `w1/SentinelRepoLocal/traces/check-self-assessment.py.B.trace.gz` | 1,567,739 | 13.3% |
| 32 | `w2/RevAllowMutantsOwed/before.trace` | 1,033,101 | 6.5% |
| 33 | `a3w2/MutAfterHomeKeep/frozen-SCORECARD.md` | 257,627 | 5.1% |
| 34 | `res/R2ReplayDummy/replay-variant.patch` | 403,271 | 4.4% |
| 35 | `w1/ScribeC2Draft/pacman-54d9411.tar.gz` | 1,934,105 | 9.6% |
| 36 | `w1/ExecLiveViewDesign/capture/base-final-6d76fb20/handoff.execve.log` | 45,594,475 | 44.5% |
| 37 | `w1/C32Ledger218/fixture-before/SKILL.md` (also at `assimilation/validate/`) | 564,927 | 3.5% |
| 38 | `w1/C1RevKernelFormat/abi-tree.html` | 582,410 | 9.0% |
| 39 | `frozen/txcapture/pacman.log` | 252,016 | 12.2% |

Top five under `.ufo/waves` at master (`git ls-tree -r -l master -- .ufo/waves | sort -k4 -n | tail -5`):
45,594,475 and 42,058,597 (the two round-36 `handoff.execve.log`), 3,692,706 and 2,359,003
(the matching `binding.execve.log`), 1,934,105 (`pacman-54d9411.tar.gz`). Pooled over the 7,737
files of rounds 30–38 at their close commits, the median file is 1,795 B, the mean 24,969 B and
p99 167,610 B — the weight is a tail, not a drift (`top-files.txt`).

## 4. Round 39 so far

Committed at `394e1ba`: **2,073,917 B in 48 files** — `controls/` 1,420,141 B (17 files),
`frozen/` 422,576 B (13), top-level `w1-spec.json`/`w1-dispatch.json`/`make-w1-spec.py` etc.
208,497 B (5), `before/` 11,330 B (3), `after/` 8,720 B (3), `assimilation/` 2,653 B (7).
Working tree at 2026-10-26 03:07 local: **308 files / 3,988,014 B**, of which `w1/` is live
(seat reports and receipts; it was 245 files / 1,812,367 B three minutes earlier). At the
declared 70 seats, round 39 is at 29,627 B/seat committed and ~57,000 B/seat live — the
lightest round since 38 (91,045 B/seat) and ~108× lighter per seat than round 36.

## 5. Findings

**F1 — one round is 53% of the window's evidence weight.** Round 36 committed 102,534,030 B
in 1,444 files: 53.1% of the 193,192,033 B of rounds 30–38 and 39.2% of all `.ufo/waves` at
master. The next heaviest (round 35) is 18,137,294 B.

**F2 — 87.7 MB arrives in one undisclosed commit.** `fe24c4c` ("round-36: capture evidence
logs (liveview + NEWS-v262)", 2026-10-24 01:54 −0300) added 5 files / 126,033 lines, two of
them `handoff.execve.log` at 45,594,475 B and 42,058,597 B — 45.4% of the nine-round evidence
total. The message is one line and names neither size nor purpose
(`git log -1 --format=%B fe24c4c` → `round-36: capture evidence logs (liveview + NEWS-v262)`).
Nothing afterwards measures it: `grep -rniE '\b[0-9]+ ?MB\b' .ufo/waves/round-36 --include='*.md'`
returns only W2MutTool3's 871 MB scratch note
(`.ufo/waves/round-36/w2/W2MutTool3/W2MutTool3.md:117`); `grep -rn 'execve.log'
.ufo/waves/round-36 --include='*.md'` returns three hits, all inventory lines that name no
size (`w1/ExecLiveViewDesign/ExecLiveViewDesign.md:7`, `w2/W2LiveOracle/W2LiveOracle.md:37`,
`w2/W2ScribeMistakes/W2ScribeMistakes.md:30`); and `grep -rnE '4[25] ?MB|45,?594|42,?058|handoff\.execve'
corpus/lessons corpus/knowledge .ufo/waves/round-36/*.md .ufo/waves/round-36/after` returns
nothing. No lesson, knowledge note or assessor row records the 87.7 MB since.

**F3 — the weight is path verbosity, not evidence.** The 45,594,475 B log has 42,299 lines, all
distinct; 20+ character absolute paths are 29,320,490 B of it
(**64.3%**), average line 1,078 B, and `gzip -9` on the blob returns **809,151 B** (56×). In
git it is already cheap: `verify-pack` gives 1,164,118 B stored for this blob and 654,802 B for
the second (delta), ≈1.8 MB of pack for 87.7 MB of checkout. The cost being bought is therefore
checkout, `grep`/`ls`/review surface — not disk — which is exactly the cost the watch should
count. The lane already has the pattern: 26 `.gz` evidence files exist under `.ufo/waves`,
including round 31's three largest (`*.trace.gz`).

**F4 — duplicates are paid twice at checkout.** 617 blobs under `.ufo/waves` appear at more
than one path: **24,699,165 B** of extra checkout (9.5% of the wave tree). Live example in the
current round: `controls/c2-entries/E1..E6/SOURCES.md` are six paths of one blob
(`2085234387…`, 225,466 B) — the same bytes as `corpus/SOURCES.md` — so the fixtures cost
1,352,796 B, 65.2% of round 39's committed weight, for five ~8 KB mutated `entry.md` files
that are the actual controls. The copies are functional (each fake repo needs a `SOURCES.md`
for the counter's source check), so this is a fixture-seam question, not a mistake; the point
is that it is neither measured nor declared. Same content, twice, unchecked: `NEWS-v262` and
`NEWS-v262.full` are one blob (`1329d035`) at 1,271,752 B in round 29 and round 36.

**F5 — round dirs are not immutable, so weight must be attributed by commit span.** At master
the round-34 dir is 9,127,754 B but was 8,386,828 B when its round closed: 66 files /
+740,926 B of late wave-2 evidence landed in round 35's declaration commit `6b4561e`
("round-34 w2 leftovers landed as non-evidence records"). Round 35 gained
`pacman-54d9411.tar.gz` (+1,934,105 B) in round 36's declaration commit `6d76fb2`, and
round 30 lost 123,734 B when round 31's `8cff9e7` deleted three committed
`__pycache__/*.pyc` (41,186 B each). Net late growth into closed round dirs: **+2,552,043 B**
(`late-writes.txt`). A dir-size-only watch would misreport all four rounds.

**F6 — prose growth is flat and small; the gap is not a corpus problem.** `corpus/` grew
600,982 B over nine rounds (47,332–95,260 B per round) against 193,192,033 B of evidence, a
322:1 ratio; round 38's largest contributions are its lesson (31,040 B) and
`pacman-hook-order-r38.md` (17,020 B). The knowledge side is not inflating — the evidence
side is unbounded.

**F7 — nothing in the lane measures it.** `grep -rn 'st_size\|getsize\|du -sh\|os.path.getsize'
tools/*.py tools/*.sh` returns nothing, and no rule in `SKILL.md`/`AXES.md`/`QUALITY.md` caps
evidence bytes (the only "bytes" rule is `check-review-snapshots`' hash pin at `SKILL.md:2151`).
Round 36 is what the absence of a gate looks like.

## 6. Proposed lesson paragraph (exact text)

> **Lesson (round 39): price evidence by checkout weight, not by commit size.** Evidence is
> paid three times — in the commit, in every checkout and `grep` a later seat runs, and in the
> reviewer's reading — and only the first is cheap: the two round-36 strace captures committed
> by `fe24c4c` cost about 1.8 MB of pack but 87.7 MB of every working tree, 45.4% of rounds
> 30–38's evidence weight, while 64.3% of the larger one's bytes are absolute-path text and
> `gzip -9` returns it to 809,151 B. The lane already knew the fix (round 31 stored its
> three heaviest traces as `*.trace.gz`) and still shipped a 102.5 MB round six rounds later,
> unnoticed by that round's verifier spot-check. So: no committed evidence file above 2 MB; a
> capture that would exceed it lands gzipped, path-relative or reduced to the lines that carry
> the claim, with the raw file left in scratch and only its sha256 and line pointers committed;
> duplicate frozen files are not free either — round 39's six copies of `corpus/SOURCES.md`
> are 1,352,796 B, 65.2% of that round's weight, so a fixture that needs one should take a
> repo-root seam or declare the copies in the round's evidence line; and each round's
> measured-outcome row carries `evidence: <MB> MB in <n> files;
> largest <file> (<MB>)`, one `git ls-tree -r -l` over the round dir, so a 100 MB round cannot
> close as quietly as round 36 did.

Check on the proposal's threshold: `for n in $(seq 30 39); do git ls-tree -r -l master --
.ufo/waves/round-$n | awk '$4+0>2000000'; done` returns **exactly four files, all in round 36**
(45,594,475 / 42,058,597 / 3,692,706 / 2,359,003 B — the two capture pairs). Nothing else in
rounds 30–39 exceeds 2 MB — the next largest is round 35's 1,934,105 B tarball — so the cap is
tight enough to bite where the problem is and loose enough to leave every other round's
evidence untouched.

## 7. Not done / limits

- No lane writes beyond this report and `ConsiderWeight/`; no build, lint, counter or gate run
  (out of scope for the seat); no tool installed or upgraded.
- Round 39 is live: its working-tree figures are a snapshot that only grows. Nothing here
  measures uncommitted bytes outside `.ufo/waves/round-39/`.
- Clone-time was not used as a metric: local `git clone` hardlinks objects (0.03 s bare,
  0.43 s full), so it measures nothing about this weight. Measured instead: `git count-objects
  -vH` gives `size-pack: 34.03 MiB` (+13.22 MiB loose) for tracked content of 267,983,346 B at
  master (`.ufo/waves` 261,260,656 B), i.e. 47.25 MiB of objects for 255.6 MiB of content:
  git stores this weight at 5.4:1, while the checkout and every reviewer pay it uncompressed.
- I did not judge whether any individual heavy file was *necessary* for its claim; the report
  measures weight and redundancy, not evidentiary value per byte. A per-file necessity audit
  would be a separate seat with the counters' predicates in hand.
