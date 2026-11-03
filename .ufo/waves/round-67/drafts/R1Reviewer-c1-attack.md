2026-11-03T21:53:06Z
# R1Reviewer — adversarial review of C1 frozen predicate

VERDICT=FAILS
CONTROLS_PASSING=2 of 3

## Frozen predicate (quoted, not reinterpreted)
From SCORECARD.md section "Round 67 — declaration", row C1 (lines 5013-5027 of the working tree; declaration frozen at 071a55c9):
- note present; `grep -cE '^\| SL[0-9]+ \|'` **>= 4**
- `corpus/SOURCES.md` rows **>= 284**, S284 directly after S283, `awk -F'|' NF == 13`
- Kill rule: "the v7.3 revert-after-all-devices block is absent from the re-fetched bytes (sha256 or line mismatch) -> honest stop, no row lands"

The counting command listed in the row checks only the SL row count (regex), the SOURCES row count (regex), and the S284 NF. It does not inspect what an SL row cites, and it does not check the note's content against the pinned bytes.

## Inputs and hashes
Command: `sha256sum` on the three pinned files
```
$ sha256sum .../round-42/frozen/src/scrub.c .../round-67/before/src/scrub.c .../round-67/before/src/CHANGES
48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801  .../round-42/frozen/src/scrub.c
b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528  .../round-67/before/src/scrub.c
5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249  .../round-67/before/src/CHANGES
rc=0
```
All three match the declared hashes. Pinned v7.3 scrub.c: `wc -l` = 2233 (rc 0).

## Controls
Scratch: /fast/scratch/hyaku/tsukuroi-r67/R1Reviewer (removed on exit).

### Do-nothing control (base 5abc31d9, no edits)
```
$ git -C .../tsukuroi-shokunin cat-file -e 5abc31d9:corpus/knowledge/btrfs-scrub-limit-revert-r67.md
rc=128   (fatal: path ... does not exist in '5abc31d9')
$ git -C .../tsukuroi-shokunin show 5abc31d9:corpus/SOURCES.md > $S/SOURCES.md ; rc=0
$ grep -cE '^\| S[0-9]{3,}' $S/SOURCES.md   -> 283   rc=0
$ awk -F'|' '/^\| S283 /{print "S283_NF="NF}' $S/SOURCES.md -> S283_NF=13  rc=0
$ git ... show 5abc31d9:corpus/knowledge/btrfs-scrub-limit-revert-r67.md | grep -cE '^\| SL[0-9]+ \|'
   -> 0 (pipe rc 128; git error on stderr)
```
Result: KILLED. The note-presence gate and the SL count both fail. Do-nothing does not pass.

### Negative control A: S284 placeholder, NF 10 (not 13)
Row inserted directly after S283: `| S284 | CONTROL-PLACEHOLDER-NOT-FETCHED | docs | A | placeholder | ... |` (NF=10).
```
$ grep -cE '^\| S[0-9]{3,}' SOURCES.control.md -> 284  rc=0
$ awk -F'|' '/^\| S284 /{print "S284_NF="NF}' ... -> S284_NF=10  rc=0
```
Result: the count check passes (284 >= 284); the NF == 13 check kills it. Killed only if the NF clause is run.

### Negative control B: S284 placeholder, NF 13, adjacent to S283 (the case that matters)
Row inserted directly after S283, nine free-text cells, invented source name, never fetched.
```
$ awk -F'|' '/^\| S284 /{print "S284_NF="NF}' SOURCES.nf13.md -> S284_NF=13  rc=0
$ grep -cE '^\| S[0-9]{3,}' SOURCES.nf13.md -> 284  rc=0
$ grep -n -A1 '^| S283 ' SOURCES.nf13.md -> 293:| S283 ... / 294:| S284 CONTROL-PLACEHOLDER-NOT-FETCHED ...  rc=0
$ awk -F'|' '/^\| S283 /{print "S283_NF="NF}' SOURCES.nf13.md -> S283_NF=13  rc=0
```
Result: PASSES every clause of the frozen SOURCES predicate (count >= 284, S284 directly after S283, NF 13). The frozen predicate does not look at the source, tier, Gate quote, or the bytes behind the row. A sourceless row passes.

### Negative control C: fake SL note, four rows citing a nonexistent line
File `fake-note.md` contains `| SL1 | scrub.c:9999 | claim |` through `| SL4 | scrub.c:9999 | claim |`.
```
$ grep -cE '^\| SL[0-9]+ \|' fake-note.md -> 4  rc=0          (frozen >= 4: PASS)
$ sed -n '9999p' .../round-67/before/src/scrub.c | wc -c -> 0   (empty; file has 2233 lines)
$ sed -n '1640,1649p' .../round-67/before/src/scrub.c | wc -l -> 10   (the cited v7.3 region does exist, so the real cite is checkable)
```
Result: PASSES the frozen SL count. The cited line does not exist in the pinned bytes; no clause of the frozen predicate reads it. Only the kill rule's "sha256 or line mismatch" would catch it, and that clause concerns the re-fetched source bytes, not the cites in the note. A cite-checker is not part of the frozen counting command.

### Duplicate-id test
`dup-note.md`: four rows all `| SL1 | x | ...`.
```
$ grep -cE '^\| SL[0-9]+ \|' dup-note.md -> 4  rc=0
```
Result: PASSES. The regex counts rows, not distinct ids; SL1-SL4 are not required to be distinct.

## Which kill rule could still stop a sourceless note
- The sha256 recheck and the v7.3 block line check operate on the re-fetched scrub.c, not on the note's cites. They can kill a note only if the note is compared against those bytes by a step the frozen command list does not contain.
- The NF == 13 clause kills only a SOURCES row with the wrong field count. It does not check the source text, the Gate quote length, or whether the cited URL/file was fetched (Control B passes).
- Nothing in the frozen counting commands joins SL rows to SOURCES rows or to the S284 bytes.

## Does the frozen predicate distinguish a sourced note from a sourceless one?
No. Control B (sourceless S284, NF 13) and Control C (SL rows with a nonexistent cite, duplicate ids allowed) both pass the frozen counting commands. Only the do-nothing control (note absent, S283 at 283) is killed.

## Verdict
FAILS. Controls passing the frozen counters: fake SL note (C) and sourceless S284 row at NF 13 (B); duplicate-id rows (dup test) pass the SL count. Do-nothing (control 0) is killed. CONTROLS_PASSING = 2 of 3 named controls.

Suggested amendment, for the L1 to consider (not applied; predicates are frozen): require each SL row's cited path:line to exist in the pinned sha256-matched source, require distinct SL ids, and require the S284 row's source field to match a recorded fetch receipt. Those are amendments, not findings about the work.

## Commands run (all rc shown above)
sha256sum x3; wc -l scrub.c; sed -n '9999p'; sed -n '1636,1652p' (read); git cat-file -e; git show ... | grep -cE; awk NF checks; grep -cE on SOURCES/SL fixtures; sed -n '1640,1649p' | wc -l.
Host-guard: no sudo, no pacman, no mutating git, no write outside drafts/ and the scratch dir.
