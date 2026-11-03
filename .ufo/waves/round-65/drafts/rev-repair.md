# R2RevRepair — attack on the R64-SPOTCHECK-C1-PROOF re-expression (round 65, wave w1)

Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. HEAD at start: `37c74e27b29d979ee749caa622eb58f9bfe39ed4`.
Scratch (removed at seat end): /fast/scratch/hyaku/tsukuroi-r65/R2RevRepair/. Receipts copied to
`.ufo/waves/round-65/w1-artifacts/R2RevRepair/` before removal. Read-only on the repo; no git mutation.

## Step 0 — identity of the cited revisions

| cmd | rc | result |
|---|---|---|
| `git rev-parse HEAD` | 0 | `37c74e27b29d979ee749caa622eb58f9bfe39ed4` |
| `git cat-file -t 431f0c9` | 0 | commit |
| `git cat-file -t 2f3061ef` | 0 | commit |
| `git log -1 --format=… 431f0c9` / `2f3061ef` | 0 | `431f0c97…` "round-64: work …"; `2f3061ef…` "round-64: declaration before measurement" |
| `git rev-list --count 2f3061ef..431f0c9` | 0 | `1` (one commit apart) |
| `git merge-base --is-ancestor 431f0c9 HEAD` | 0 | ancestor (HEAD later: 09468bda, 72c12b78, 1bd8e196, 37c74e27) |

## Step 1 — reproduce the additive-only proof AT 431f0c9 (what was measured)

Extraction: `git show 2f3061ef:F | tr -d '\r' > old/<F>.base` (rc 0 ×3); `git show 431f0c9:F > new/<F>.rev` (rc 0 ×3).
Counting: `git --no-pager diff --no-index --numstat <base> <rev>` (host `diff` is pi-uu-diff 0.8.0, so GNU `diff` flags were not used).

| file | numstat added/removed | rc of numstat | hunks (`-U0`) | expected | verdict |
|---|---|---|---|---|---|
| corpus/SOURCES.md | **3 / 0** | 1 (differ) | `@@ -288,0 +289,3 @@` | 3/0 | match |
| SKILL.md | **120 / 1** | 1 (differ) | `@@ -5490 +5490,120 @@` | 120/1 | match |
| SCORECARD.md | **0 / 0** (empty) | 0 (identical) | none | 0/0 | match — byte-identical |

Sha256 of the blobs (base = stripped 2f3061ef; rev = 431f0c9):
- SOURCES base (stripped 2f3061ef) `e1558e4b3eeef8857e27a64299e08c50e52c3b9f5f2160a09cd6647e90c3df77`; rev (431f0c9) `863be44bcb6a9b92c6030e5f23c07e45df91c6ff5a8dbbc0b4b999300c9a653c`
- SKILL base `bda5249b161e7442f056e924c9091331ac091a6d38e49bbcd762a93ad331c85d`; rev `5a99794d063f07465f81c4732167acf5c1ce3236516bc5c2f70e1fc086ae5c1a`
- SCORECARD base = rev = `13047505…89df66` (`git show 431f0c9:SCORECARD.md | cmp - <stripped base>` rc 0)

Receipt: `receipts/step1-reidentity-at-431f0c9.txt`.

Additional measured facts (rc in brackets):
- raw CR counts at 2f3061ef: SOURCES 381, SKILL 5452, SCORECARD 4723 [rc 0 ×3]; at 431f0c9: 0/0/0 [rc 0 ×3].
- SKILL EOF artifact: base last byte is `.` (0x2e), no terminal newline [tail -c]; `cmp` of line 5490 base vs rev → `EOF on … after byte 859` [rc 1]; base with a terminal newline appended vs rev → numstat `119 0` [rc 1, differ]. Removed content = zero; the `-1` is the EOF artifact. Receipt: `receipts/step3-prechecks.txt`.
- SOURCES inserted lines are S279/S280/S281 directly after S278 (context lines 286–292 at 431f0c9) — confirmed by the hunk header.

## Step 2 — original wording `git show 2f3061ef:F | tr -d '\r' | cmp - F`, three times, at the CURRENT worktree

`git status --porcelain -- corpus/SOURCES.md SKILL.md SCORECARD.md` → empty, rc 0 (worktree == HEAD for the three files).

| run | file | cmp rc | first difference |
|---|---|---|---|
| 1,2,3 | corpus/SOURCES.md | **1** ×3 | char 238601, line 289 (the S279 insertion) |
| 1,2,3 | SKILL.md | **1** ×3 | `cmp: EOF on - after byte 1351538` |
| 1,2,3 | SCORECARD.md | **1** ×3 | char 23030, line 166 |

FALSE for all three files at HEAD (receipt `receipts/step2-original-wording-worktree.txt`). SOURCES/SKILL fail for the same reason as at 431f0c9 (additive work). SCORECARD fails at HEAD for a reason the closure did not name: commit 09468bda inserted the `line-endings-guard` capability row at SCORECARD.md:166, and 37c74e27 appended the round-65 declaration. Mechanism confirmed by `git --no-pager diff --numstat 431f0c9 37c74e27 -- SCORECARD.md` → `85 0` (receipt `receipts/step2b-scorecard-divergence.txt`).

Original wording at 431f0c9 (reconstructed by the Step 1 blobs, not by a new run against the worktree): rc 1 / 1 / 0 — SOURCES and SKILL fail, SCORECARD passes (`cmp` rc 0 on the 431f0c9 blob, sha equal to the stripped base). Consistent with the closure's finding.

Recorded: the original wording's operand was the fix-time worktree; the r64 receipt digests (`e1558e4b`, `bda5249b`, `13047505`) equal the stripped declaration blobs above — so the original wording was true of that moment only.

## Step 3 — review of E3RoutedRepair's draft

Draft: `.ufo/waves/round-65/w1-artifacts/E3/routed-repair-draft.md` (143 lines, 8653 bytes at read; present at first poll — no polling needed). Receipt it cites: `.ufo/waves/round-65/w1-artifacts/E3/routed-repair-receipt.txt` (present, untracked).

### Block A's command — extracted from the draft's ```sh block and re-run verbatim

I transcribed the block into `new/block-A-command.sh` with the write device (the attempted awk extraction failed with a parser error: `pi-natives:command: syntax error at line 1 col 509`, rc 2 — recorded, not used). Then:

| cmd | rc | output |
|---|---|---|
| `bash block-A-command.sh` (REV=431f0c9) | **0** | `corpus/SOURCES.md added=3 removed=0 (expected 3/0)`; `SKILL.md added=120 removed=1 (expected 120/1)`; `SCORECARD.md added=0 removed=0 (expected 0/0)`; `gate rc=0` |
| `sh block-A-command.sh` (same, under sh) | **0** | identical output, `gate rc=0` |
| negative control `REV=2f3061ef` (`sed` copy) → `bash block-A-negative.sh` | **1** | `381/381`, `5452/5452`, `4723/4723`; `gate rc=1` |

Receipts: `receipts/step4-block-A-run.txt`, `receipts/step4c-under-sh.txt`, `receipts/step4b-negative-control.txt`. Its counts and its negative control are as the draft states.

### Checklist

1. Append-only-safe: **mostly yes.** Block A is append-only (no rewrite of the round-64 text, no axis/claim/gate change). It quotes the closure verbatim (matches `corpus/lessons/round-64-verifier-spotcheck.md` §5, lines 116–120) and names the wording it supersedes (`git show 2f3061ef:F | tr -d '\r' | cmp - F` rc 0 ×3). **Gap:** it does not say *where* that wording lives. The text is at SCORECARD.md:4744 (the round-64 C1 row, contains "`cmp - F` rc 0 ×3"), and also in LOG.md and corpus/lessons/round-64.md. The erratum should cite SCORECARD.md's round-64 C1 row, or it leaves the reader to grep for the superseded text.
2. The stated command is exactly the one I re-derived: yes (Step 3 table; output and gate rc identical to my independent Step 1 numstat).
3. The counts are the measured ones: yes, 3/0, 120/1, 0/0 at 431f0c9; negative control 381/5452/4723 at 2f3061ef. The SKILL `−1` is the EOF artifact (cmp `EOF after byte 859`; `119 0` with newline restored).
4. Duplicate erratum: a second landable block already exists at `.ufo/waves/round-65/drafts/scorecard-erratum-r64-proof.md` with heading `## Round 65 — routed repair (R64-SPOTCHECK-C1-PROOF): …`. Its counts agree with the measurements. Landing both would give two erratum blocks for one routed defect; the E3 draft's landing note 4 says to land A only. The L1 must pick one (recommend A, which carries the receipt).

## Verdicts

| item | verdict |
|---|---|
| Independent re-derivation at 431f0c9: SOURCES 3/0, SKILL 120/1, SCORECARD 0/0 | **PASS** — exactly as expected; no count differs from expectation, so no finding against the repair's measurement |
| Original wording at the current worktree (HEAD 37c74e27) | **FALSE for 3/3** (rc 1 / 1 / 1) — SCORECARD now fails because of 09468bda and 37c74e27 (SCORECARD.md:166 + declaration); the closure's "only true of the fix-time worktree" holds |
| E3 Block A — command as stated | **AGREE** (exact re-derived command; rc 0 green at 431f0c9; rc 1 at 2f3061ef) |
| E3 Block A — counts | **AGREE** (measured, not fitted) |
| E3 Block A — append-only-safe | **AGREE with one minor defect**: superseded text not located (cite SCORECARD.md:4744, round-64 C1 row) |
| E3 — landing | **Disagree with landing both erratum blocks**: exactly one may land (A); the drafts/ erratum duplicates the defect id |

## Findings (ranked)

1. (minor) E3 Block A does not locate the superseded wording; add the SCORECARD.md:4744 pointer (and the LOG.md round-64 outcome line that carries the same text) so the erratum names the text it supersedes, not only quotes it.
2. (minor) Two erratum drafts for one defect id (E3 block A and `drafts/scorecard-erratum-r64-proof.md`); L1 must land exactly one.
3. (info) The original wording fails at HEAD for SCORECARD as well as SOURCES/SKILL; the round-65 erratum's "true of a moment" claim is correct but the SCORECARD mechanism is the later row/declaration, not the round-64 additive work.
4. (info) The host `diff` is pi-uu-diff 0.8.0; the Block A gate correctly uses `git diff --no-index --numstat`. No GNU-diff flags used in this seat.

## Commands run (every command, rc)

| # | command (abridged) | rc |
|---|---|---|
| 1 | `mkdir -p …/R2RevRepair/{old,new,receipts}` | 0 |
| 2 | `git rev-parse HEAD`; `git cat-file -t 431f0c9`; `git cat-file -t 2f3061ef`; `git log -1 … 431f0c9`; `git log -1 … 2f3061ef` | 0 ×5 |
| 3 | grep `R64-SPOTCHECK-C1-PROOF`, grep `431f0c9`, glob round-65 (tool calls) | ok |
| 4 | `git show 2f3061ef:F \| tr -d '\r' > old/F.base`; `git show 431f0c9:F > new/F.rev` (×3) | 0 ×6 |
| 5 | `git --no-pager diff --no-index --numstat old new` (×3) | 1,1,0 |
| 6 | `git --no-pager diff --no-index -U0 …` (×3) + `grep ^@@` | 1,1,1 (grep no-match for SCORECARD) |
| 7 | `git status --porcelain -- F` (×3 files) | 0 (empty) |
| 8 | `git show 2f3061ef:F \| tr -d '\r' \| cmp - F` ×3 runs ×3 files | 1 ×9 |
| 9 | `git show 431f0c9:SCORECARD.md \| cmp - old/SCORECARD.md.base`; `sha256sum` ×2 | 0; sha equal |
| 10 | `git --no-pager diff --numstat 431f0c9 37c74e27 -- SCORECARD.md SOURCES SKILL` | 0 (`85 0` SCORECARD) |
| 11 | `git --no-pager log --oneline 431f0c9..37c74e27` | 0 |
| 12 | `git show 37c74e27:SCORECARD.md \| sed -n …`; `git show 431f0c9:…`; `sed -n … SCORECARD.md` `cat -A` | 0 ×3 |
| 13 | `git show <c>:SCORECARD.md \| grep -c $'\r'` for 37c74e27/431f0c9/2f3061ef; worktree `grep -c` | 0 ×4 (counts 0,0,4723,0) |
| 14 | `git rev-list --count 2f3061ef..431f0c9`; `git merge-base --is-ancestor 431f0c9 HEAD`; `git --no-pager log --oneline --parents -n1 431f0c9` | 0 ×3 |
| 15 | `sha256sum` base files; `git show 2f3061ef:F \| sha256sum` ×2 | 0 |
| 16 | `git show 2f3061ef:F \| grep -c $'\r'`; `git show 431f0c9:F \| grep -c $'\r'` (×3 ×2) | 0 ×6 (381/0, 5452/0, 4723/0) |
| 17 | `tail -c 16 base \| od -c`; `wc -l base`; `sed -n 5490p base/rev`; `cmp` of line 5490 | 0; `cmp` 1 |
| 18 | `cp` base → SKILL.nl.base; `printf '\n' >>`; `git --no-pager diff --no-index --numstat` (119/0) | 0; diff 1 |
| 19 | `grep -n '^## Round 65'`; `tail -n 3 SCORECARD.md`; grep `rc 0 ×3`/`cmp - F`/`tr -d` in SCORECARD; `awk` line 4700–4760; grep in LOG/corpus | 0 ×n (grep matches: LOG.md, SCORECARD.md, corpus/lessons/round-64-verifier-spotcheck.md, corpus/lessons/round-64.md) |
| 20 | `git status --porcelain -uall -- …/E3 …/after …/drafts` | 0 |
| 21 | `diff --version` | 0 (`pi-uu-diff 0.8.0`) |
| 22 | `sleep 5; ls -la …/E3; wc -l routed-repair-draft.md` | 0 (143 lines) |
| 23 | read draft (tool read) | ok |
| 24 | `_write` `new/block-A-command.sh` (transcribed from the draft sh block) | ok |
| 25 | awk extraction of the draft's sh block | **2** (parser error, pi-natives; not used) |
| 26 | `bash new/block-A-command.sh` (REV=431f0c9) | **0** |
| 27 | `sed` → `new/block-A-negative.sh` (REV=2f3061ef); `bash` it | **1** |
| 28 | `sh new/block-A-command.sh` | **0** |
| 29 | `_read` of lesson / draft (tool) | ok |

No pacman, no systemctl, no sudo, no installs; no tool installed (no ~/.local/bin writes).
