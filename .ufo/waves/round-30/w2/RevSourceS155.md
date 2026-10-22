# Round 30 wave-2 falsification — S155 (RevSourceS155)

Verdict: partly holds — the admit's substance (source, digest, quote, kind, tier, scope,
teaches, status/opened/recheck) verifies against the live bytes, but the row's `used-by`
cell is factually wrong at the attacked revision: it names `corpus/lessons/round-30.md`,
which does not exist at 29bf87fa3971df04cb96e4ad9a28805d8154ed2f. Disagree with the row as
committed at the tip on that one cell; agree with everything else.

Note on method: lane HEAD is `857126711c9a5dd5e62f5f0ad2bf403f479fa4f0`, not the attacked
tip, with 8 porcelain entries (2 modified, rest untracked wave artifacts). All revision
checks below ran read-only via `git show`/`git grep`/`git ls-tree` at 29bf87fa, not the
working tree. The S155 row itself is byte-identical between tip and working tree
(`diff` of line 161 both sides: IDENTICAL).

## Findings

1. **Defect — `used-by` names a file absent at the tip.** The row (corpus/SOURCES.md:161)
   lists `corpus/knowledge/btrfs-space-r30.json, corpus/knowledge/btrfs-space-r30.md,
   SKILL.md, corpus/lessons/round-30.md`. At 29bf87fa:
   `git ls-tree 29bf87fa -- corpus/lessons/round-30.md` prints nothing (no such blob), and
   `git show 29bf87fa:corpus/lessons/round-30.md | grep -c S155` = 0 (file absent). The
   lesson was added post-tip in `7165f11` (`git log --oneline 29bf87fa..HEAD --
   corpus/lessons/round-30.md` → only 7165f11; at HEAD it does carry the gate row for S155
   at line 14, verbatim matching the w1 seat draft). Consequence: the contract-v1 census
   rule "mined rows whose used-by paths do not exist — must print nothing" would print
   `missing: corpus/lessons/round-30.md` when run against the tip tree. [obs] The row
   appears to have been committed naming a lesson file that had not landed yet; the defect
   self-corrects at HEAD but stands at the judged revision.

2. **Live bytes match the anchor and the snapshot.** `curl -sL -w` of
   https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/mkfs.btrfs.rst on
   2026-10-22 returned HTTP 200; sha256 of the fetched bytes =
   `ce7c0cbca90eda4bc84040e9f5a43c227bd02d77bd50b006e481f19d918de769` = anchor-cell digest =
   sha256 of `.ufo/waves/round-30/w1/ScribeSrcMkfs/S155-mkfs.btrfs.rst`. Both are 723 lines,
   29867 bytes — matching the anchor's parenthetical. Live copy saved unchanged at
   `.ufo/waves/round-30/w2/RevSourceS155/S155-mkfs.btrfs.rst.live` (sha256 as above). [obs]

3. **Gate quote verifies verbatim at the cited line.** Seat draft
   `.ufo/waves/round-30/w1/ScribeSrcMkfs/S155-gate.md` cites line 59 with quote
   `Default on a single device filesystem is *DUP* and is recommended for metadata`
   (13 words ≤ 25). `sed -n '59p'` on both live bytes and committed snapshot piped to
   `grep -cF` of that string returns 1 for each. The secondary claim in the same cell
   (PROFILES table line 520: `DUP      |  2 / 1 device |            |            |  50%`)
   also verifies verbatim at line 520 (`grep -cF` = 1). [obs]

4. **Row shape and enums conform to CORPUS.md contract v1.** Row at tip line 161 splits on
   `|` to NF=13 → 11 cells. `id` `S155` fits `S`+3 digits; `kind` `docs` in enum;
   `tier` `A` in enum (kind docs is eligible; community is the only never-A);
   `status` `mined` is satisfied by the three real citing files; `opened` `2026-10-22`
   is the ISO date of today's re-open, matching the gate draft's Opened cell;
   `recheck` `on-release` is a listed cadence. No `|` inside cells. [obs]

5. **Tier/kind/scope/teaches are accurate.** `git ls-remote
   https://github.com/kdave/btrfs-progs refs/tags/v7.1*` returns `0a919c7d6e389c07920675b7fad3f793b92aa78b refs/tags/v7.1` (annotated) and `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b refs/tags/v7.1^{}` — exactly the tag object and tagged commit the anchor and gate claim. Host `btrfs --version` = `btrfs-progs v7.1`, so "installed btrfs-progs 7.1" in the tier rationale is true. Anchor line ranges each contain what they claim: 21-23 defaults-depend-on-device-count; 54-77 the `-m|--metadata` option with DUP default and the 5.15 "always dup" note (lines 59, 66-69); 508-534 the PROFILES table; 630-666 the "DUP PROFILES ON A SINGLE DEVICE" section ending `**DUP is not backup**` (line 666). `teaches` is grounded: two copies + 50% utilization (line 520), SSD dedup caveat (lines 62, 639-641), not-backup (line 666); the "twice their logical size in raw space" phrasing is the doc's own 2-copies/50% arithmetic. [obs/inf]

6. **The other three `used-by` entries really cite S155 at the tip.** `git grep S155
   29bf87fa -- <paths>`: btrfs-space-r30.json twice (D04 block lines 38-41: `"source":
   "S155"`, snapshot path, `"line": 59`, and the same 13-word quote); btrfs-space-r30.md
   twice (front-matter `source:` list line 1; body line 16 `(S155 line 59)`); SKILL.md once
   (line 2609, `[R30-D04]` rule `| S155 line 59 |`). All consistent with the verified
   line 59. [obs]

7. **[obs] Contract rule 1 consequence.** Rule 1 wants the round lesson's `## Gate` to
   record each new row's URL/access-date/quote; at the tip no round-30 lesson exists, so
   the Gate record lived only in the w1 seat directory. Commit 7165f11 added
   `corpus/lessons/round-30.md` with the gate table (S155 row at its line 14, text
   identical to `S155-gate.md`). The landing order — SOURCES row first, lesson later —
   is what makes the tip-time `used-by` wrong; flagging for the integrator's judgment
   rather than re-scoping.

## Residual risk / gaps

- Digest equality proves byte equality; no separate diff of live vs snapshot needed. [obs]
- I checked only the ScribeSrcMkfs S155 seat artifacts; other seats' S155-named files
  were globbed and none exist. [obs]
- Whether the used-by/lesson landing-order defect is judged a row error or a wave-1
  sequencing artifact is outside this seat's call; the factual claim stands either way.
  [unk]

Scope: read=corpus/SOURCES.md:161 (tip+worktree), CORPUS.md:64-153, w1/ScribeSrcMkfs/S155-gate.md and S155-mkfs.btrfs.rst, live mkfs.btrfs.rst, used-by files at 29bf87fa; wrote=.ufo/waves/round-30/w2/RevSourceS155/S155-mkfs.btrfs.rst.live, .ufo/waves/round-30/w2/RevSourceS155.md; executed=curl, sha256sum, wc, sed, grep -cF, awk, diff, btrfs --version, read-only git (show/grep/ls-tree/log/rev-parse/status/ls-remote)
Model: devin/swe-2
Installs: none
