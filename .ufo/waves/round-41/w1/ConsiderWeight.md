VERDICT: supports

# ConsiderWeight — K-1 "Evidence-weight watch" (round-41 w1, `considerthese/2026-10-25.md:20`)

Item: measure, per round 35–41, the bytes each round's commits added under `.ufo/waves/` and
`corpus/`, flag any added blob over 1 MB, show the table and the command
(`considerthese/2026-10-25.md:20`: "Report how many bytes each round adds under `.ufo/waves/` and
`corpus/` … so repo growth from raw evidence is noticed before it slows clones and reviews").

The premise holds and is now quantified: **61.1% of the 158.7 MB added under `.ufo/waves/` in
rounds 35–41 arrives in six files, all in round 36**, and nothing over 1 MB has been added in the
five rounds since. Read-only seat: no tracked lane file was created, edited or deleted; only
`git log`, `git rev-list`, `git diff-tree`, `git cat-file`, `git ls-tree` and `git grep` were run,
plus `gzip`/`awk`/`find` reads on the working tree. No tool was installed or upgraded (nothing
was needed), no pacman query was made, no service touched.

Deliverables in `.ufo/waves/round-41/w1/ConsiderWeight/`:
`weight.py` (the measuring script, sha256 `ccd231ffefbf1d0c7d0b0d7429302eab3cdc3361876426800e3e93a95400384f`)
and `weight.out` (3,647 B, the exact observed output reproduced below).

## 1. Command

```bash
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
export TMPDIR=/fast/scratch/hyaku/tsukuroi-r41/ConsiderWeight
python3 .ufo/waves/round-41/w1/ConsiderWeight/weight.py --json "$TMPDIR/weight.json"
```

Run three times in this seat — 3.3 s and 4.4 s wall on the two timed runs, on a shared host — with
byte-identical output each time and identical to the committed `weight.out` (`cmp` clean).

Definitions the script implements (stated so the numbers can be argued with):

- **Basis** = the commits whose subject starts `round-NN` (`git log --format=%H --grep '^round-NN'`,
  reversed to oldest-first). Round 41 uses the declared base..tip range
  `0e5805a1f149bd2ed9fe0db2e0a832afb034a835..71851d636ab1bffaf8fee5016617c88878a666f1`, per the
  item; §5 F7 corrects what that range actually contains.
- **Added bytes** = sum of the sizes of blobs introduced with raw status `A`
  (`git diff-tree -r -z --no-commit-id <c>`) sized by `git cat-file --batch-check`. Modified and
  deleted content is *not* counted (144 `M` and 2 `D` files across the window; see the closure
  test in §2). Attribution is by the adding commit, not by the directory the file lands in, so a
  commit that writes into an earlier round's directory counts against the round that added it.
- **Net growth** = blob bytes under the watched dirs at the round's last commit minus the same at
  its first commit's parent (`git ls-tree -r -l`), i.e. adds + modifications + deletions.
- **Over 1 MB** = blob size > 1,048,576 bytes.

## 2. Output table

Observed output of the command above (`weight.out`, first block):

| round | basis | commits | added files (waves/corpus) | .ufo/waves added | corpus added | other added | total added | net growth waves+corpus | added blobs >1 MiB |
|---|---|---|---|---|---|---|---|---|---|
| 35 | grep ^round-35 | 8 | 1556/3 | 18,878,220 | 36,230 | 46,081 | 18,960,531 | 18,937,545 | 0 |
| 36 | grep ^round-36 | 10 | 1445/3 | 104,460,254 | 33,981 | 69,022 | 104,563,257 | 104,516,984 | 6 |
| 37 | grep ^round-37 | 20 | 742/4 | 16,154,164 | 31,275 | 79,197 | 16,264,636 | 16,210,675 | 0 |
| 38 | grep ^round-38 | 10 | 740/3 | 6,464,189 | 62,666 | 28,075 | 6,554,930 | 6,551,753 | 0 |
| 39 | grep ^round-39 | 10 | 1058/3 | 8,338,525 | 47,821 | 26,220 | 8,412,566 | 8,405,331 | 0 |
| 40 | grep ^round-40 | 11 | 540/3 | 4,009,731 | 41,294 | 26,756 | 4,077,781 | 4,023,345 | 0 |
| 41 | range 0e5805a1..71851d63 | 8 | 47/2 | 379,100 | 26,797 | 42,892 | 448,789 | 411,873 | 0 |

`other added` is everything the round's commits added outside the two watched dirs (SCORECARD,
LOG, lessons, tools) — shown only so the watched numbers are not mistaken for total round weight.

Verification lines the script prints under the table (verbatim):

```
Watched total (rounds 35-41): .ufo/waves 158,684,183 added bytes in 6128 files; corpus 280,064 added bytes in 21 files.
diff statuses across all measured commits (A = counted above): A=6164, D=2, M=144
size cross-check: every added blob compared with ls-tree -r -l at its commit, 0 mismatches.
distinct-commit total (each commit counted once): .ufo/waves 158,684,183 bytes in 6128 files, corpus 262,336 bytes in 20 files, other 318,243 bytes, 76 commits
closure over b40c01df..71851d63 (79 commits): added-deleted+modified waves=158,645,960 corpus=393,818; ls-tree delta waves=158,645,960 corpus=393,818 -> OK
```

Two checks, not one assertion:

1. **Per-blob**: every `A` blob's `cat-file --batch-check` size is compared with the size
   `git ls-tree -r -l <commit>` reports for that path — 6,164 additions, 0 mismatches.
2. **Closure**: over the whole window (`b40c01df`, the parent of round 35's first commit, to
   `71851d63`), added − deleted + modified-delta equals the `ls-tree` size delta exactly in both
   dirs (`waves=158,645,960`, `corpus=393,818`). This path never uses the per-round additions, so
   the table's added-bytes sum and the tree's real growth agree: 158,684,183 added vs
   158,645,960 net = 38,223 B of deletions and shrinking rewrites.

The 76-commit distinct set is the 75 round-labelled commits plus `1f5e74aa`, which the round-41
range sweeps in; it adds no watched bytes.

Size distribution of the 6,148 added files (distinct commits, watched dirs): median **1,587 B**,
mean 25,853 B, p99 166,257 B — the weight is a tail, not a drift.

## 3. Blobs over 1 MB (the flag)

Six added blobs exceed 1,048,576 B; all six are in round 36, whose 104,494,235 B they are **93%** of:

| round | bytes | file | adding commit |
|---|---|---|---|
| 36 | 45,594,475 | `.ufo/waves/round-36/w1/ExecLiveViewDesign/capture/base-final-6d76fb20/handoff.execve.log` | `fe24c4c2` |
| 36 | 42,058,597 | `.ufo/waves/round-36/w2/W2LiveOracle/capture/quality82-liveview-c052-W2LiveOracle/handoff.execve.log` | `fe24c4c2` |
| 36 | 3,692,706 | `.ufo/waves/round-36/w1/ExecLiveViewDesign/capture/base-final-6d76fb20/binding.execve.log` | `fe24c4c2` |
| 36 | 2,359,003 | `.ufo/waves/round-36/w2/W2LiveOracle/capture/quality82-liveview-c052-W2LiveOracle/binding.execve.log` | `fe24c4c2` |
| 36 | 1,934,105 | `.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz` | `6d76fb20` (round-36 declaration) |
| 36 | 1,271,752 | `.ufo/waves/round-36/w1/SrcSystemdNews/NEWS-v262.full` | `fe24c4c2` |

The script also prints `of these, 0 lie outside .ufo/waves and corpus/`.

What the two biggest are (`git cat-file blob` reads in this seat):

- 45,594,475 B → `gzip -9` **809,151 B** (56.3×); 42,299 lines, all distinct. The bytes are
  strace records whose arguments are absolute scratch paths, e.g.
  `execve("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ExecLiveViewDesign/wrappers/python3", …)` and env arrays under `/tmp/tsukuroi-r36-liveview.*/handoff/work/…`.
- 42,058,597 B → `gzip -9` **779,363 B** (54.0×).

The lane's own rule that "a /tmp path is never evidence" is about citations, not logs; still, the
single heaviest committed artifact in the lane is 43.5 MiB of `/tmp/…` paths captured verbatim.

## 4. Corroboration (independent methods, independent seats)

- **Byte-exact agreement with the round-39 seat.** `.ufo/waves/round-39/w1/ConsiderWeight.md` §2
  measured *directory* sizes per round; this seat measures *added* bytes by commit. For rounds
  35–38 the two agree exactly where they should: r35 own-dir additions `18,137,294` = that
  report's `18,137,294`; r37 `16,154,164` = `16,154,164`; r38 `6,464,189` = `6,464,189`; r36 own
  dir `102,526,149` vs its `102,534,030` (−7,881 B of net modification, which an added-only
  measure does not carry). The residual of round 35's row, `18,878,220 − 18,137,294 = 740,926 B`,
  is exactly that report's round-34 late-write figure — the leftovers landed in a round-35 commit
  and are attributed to round 35 here, which is the attribution rule its F5 asks for.
- **Round 40's own row.** `SCORECARD.md:2420-2421` records "Evidence weight: `.ufo/waves/round-40/`
  about 4 MB, no file above 2 MB"; this measurement gives round 40 `4,009,731 + 41,294 = 4,051,025 B`
  added and no blob over 1 MB. The manual figure and the counter agree.
- **The proposal's own cited number.** `d411c3d` ("round-29: RevMarkerO10 systemd v262 NEWS
  snapshot (1.27 MB evidence file)") adds one blob,
  `.ufo/waves/round-29/w2/RevMarkerO10/NEWS-v262` at `1,271,752` B by `git cat-file -s` — the
  exact 1.27 MB the proposal names, reproduced by the same method used for the table.

## 5. Findings

**F1 — six files are 61.1% of seven rounds of evidence.** 96,910,638 B of the 158,684,183 B added
under `.ufo/waves/` in rounds 35–41 sits in the six blobs of §3; the two `handoff.execve.log` files
alone are 87,653,072 B, **55.2%** of the seven-round total. The remaining 61,773,545 B is spread
over 6,142 files (median 1,587 B).

**F2 — the round-36 spike did not recur.** Added watch weight per round (bytes, waves+corpus):
35 `18,914,450`; 36 `104,494,235`; 37 `16,185,439`; 38 `6,526,855`; 39 `8,386,346`;
40 `4,051,025`; 41 `405,897` (in flight). Excluding the six large blobs round 36 falls to
`7,583,597 B`, i.e. in line with 38–40 — the spike is the capture dump, not the round's work.

**F3 — nothing over 1 MB in rounds 37–41.** Zero added blobs exceed 1 MiB in the five rounds after
round 36; the largest added blob since is round 38's `w1/C1RevKernelFormat/abi-tree.html`
(582,410 B), then round 37's two `SKILL.md` fixture copies (564,927 B each). Measured against the
cap proposed at `corpus/lessons/round-39.md:99-101` ("no committed evidence file above 2 MB"), the
cap has had **no new violations in five rounds**, and it would have bitten exactly four files, all
in round 36. If K-1 wants a gate, the tail it targets is already one round old.

**F4 — `corpus/` is flat; the growth is entirely evidence.** Rounds 35–41 added 21 `corpus/` files /
280,064 B (262,336 B distinct) against 158,684,183 B of `.ufo/waves/` — a **605:1** added-byte
ratio. At tip (`71851d63`) `.ufo/waves/` is 271,867,991 B in 13,574 files and `corpus/` is
3,092,390 B in 146 files (87.9:1). `.git` is 42 MB while `du -sh .ufo/waves` reports 291 MB: git
stores the weight at roughly 6:1, but every checkout, `grep` and reviewer pays it whole. The
proposal's cost model ("slows clones and reviews") applies to *checkout*, not clone — a local clone
hardlinks objects, as `.ufo/waves/round-39/w1/ConsiderWeight.md` §7 already recorded.

**F5 — attribute by commit, not by directory.** In this window, `2,675,031 B` lands in a round's
directory from a *different* round's commit: 740,926 B of round-34 leftovers in round 35's
declaration commit `6b4561e4`, and 1,934,105 B of `pacman-54d9411.tar.gz` written into
`.ufo/waves/round-35/` by round 36's declaration commit `6d76fb20`. A directory-size watch would
charge both to the wrong round; the table charges them where the commit did.

**F6 — round 41 is, so far, the lightest round in the window.** Committed at `71851d63`:
379,100 B / 47 files under `.ufo/waves/` (largest added file 59,521 B,
`after/c1-after-568c397.jsonl`) and 9,069 B / 1 file of `corpus/`.
The live working tree (uncommitted w1 seat reports included) is 1,757,214 B in 270 files, of which
`w1/` is 1,137,422 B in 216 files — about 23,700 B per declared seat (74 items in
`.ufo/waves/round-41/w1-spec.json`), against round 36's 3.2 MB/seat at close.

**F7 — the round-41 range in the item's brief double counts one commit.** The instructed range
`0e5805a1..71851d63` holds 8 commits, but only 6 match `^round-41`; the other two are
`8b7c4132` ("round-40 verifier spot-check", corpus 17,728 B) and `1f5e74aa`
("considerthese: 2026-10-26 daily reflection", other 4,551 B, no watched bytes). `8b7c4132` is
also inside round 40's grep row, so the naive seven-row sum reports `corpus 280,064` where the
distinct total is `262,336`. The script prints both:

```
note: round-41 subject-grep only (6 commits, the range extras removed): waves=379,100 in 47 files, corpus=9,069 in 1 files, other=38,341
```

Round 41 asked alone is therefore 379,100 B of `.ufo/waves/` and **9,069 B** of `corpus/`, and the
headline `.ufo/waves` figure (158,684,183 B) is unaffected because neither extra adds any wave
bytes. Use the distinct column, not the row sum, for the corpus total.

## 6. Not done / limits

- **Added-only measure.** 144 modified and 2 deleted files are not in the added columns; the
  closure test in §2 accounts for them exactly, so nothing is unmeasured, only unlisted.
- **Round 41 is live.** The table is the committed state at `71851d63`; the `w1/` seat reports now
  being written are untracked and will raise round 41's final figure (currently 1.76 MB whole-dir,
  max file 109,887 B).
- **No clone-time metric.** Local clones hardlink objects, so they measure nothing about this
  weight; size on checkout is used instead.
- **No per-file necessity judgment.** The report measures weight and redundancy, not whether each
  byte was needed for its claim. The two big logs are unreferenced outside bare inventory lines:
  `git grep -l 'handoff\.execve\.log' 71851d63 -- '*.md'` returns only
  `.ufo/waves/round-39/w1/ConsiderWeight.md`, and
  `git grep -n 'execve\.log' 71851d63 -- '.ufo/waves/round-36/**/*.md'` returns two file-name
  mentions with no size (`w1/ExecLiveViewDesign/ExecLiveViewDesign.md:7`,
  `w2/W2LiveOracle/W2LiveOracle.md:37`).
- **Not run:** no counter, census `--selftest`, gate, build, lint or formatter was executed (out of
  scope for this seat); no lane write beyond this report and `ConsiderWeight/`; scratch
  `/fast/scratch/hyaku/tsukuroi-r41/ConsiderWeight/` removed after `weight.out` was copied here.
