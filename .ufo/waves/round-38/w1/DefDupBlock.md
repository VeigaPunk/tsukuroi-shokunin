VERDICT: defect-found

# Seat DefDupBlock — round-38 item D-1 (round-37 closure routed defect 1)

Item source: `corpus/lessons/round-37-verifier-spotcheck.md:125` (§6 item 1) — "`corpus/knowledge/journalctl-v262-field-filter-r36.md` carries the round-37 correction block twice (lines 129-157 and 158-185, introduced by `543a7ce`). Append a named correction that marks the second block a duplicate (append-only; do not delete)."

The defect is real and still open at lane tip `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` (2026-10-26). Line numbers and the one-phrase difference are confirmed below; the draft append-only correction block follows in §4. Nothing in the lane was modified by this seat.

## 1. Both headings and their line numbers (confirmed)

Command and observed output (`receipt-01-headings.txt`):

```
$ grep -n '^## Round 37 correction' corpus/knowledge/journalctl-v262-field-filter-r36.md
129:## Round 37 correction — predicate count, output states, action precedence and prior teaching
158:## Round 37 correction — predicate count, output states, action precedence and prior teaching
```

- First block: lines **129-157** (29 lines, 3629 bytes, `sha256 e17aa221bf028203cd1ad972a2abff54a203ee62c40fe1da8165012f4671c5ae`). Line 157 is the blank separator.
- Second block: lines **158-185** (28 lines, 3623 bytes, `sha256 fd04c078533bcded434156e22109ce360d81cb1a4791a2afd404d0c62160812b`). Line 185 is the last line of the file; the file ends with a newline.

History: both copies were introduced in one commit, `543a7cee2c5119f42023aa72597ce452d4a060d5` ("round-37: correct journalctl v262 note and add finite counter", 2026-10-25T16:20:15-03:00): `git show 543a7ce --stat` = `corpus/knowledge/journalctl-v262-field-filter-r36.md | 58 +`, and the diff adds the 58 lines 128-185 in one hunk. Its parent `8936643` has 127 lines and 0 such headings. `git log -G'^## Round 37 correction' --oneline -- <file>` returns only `543a7ce`; `git log --oneline 543a7ce..HEAD -- <file>` is empty. `grep -c` returns 2 at `543a7ce`, `c231d0b` (round-37 tip), `8bd001f` (round-38 base) and `5edb6c2`; the file is byte-identical at `543a7ce` and `5edb6c2` (`sha256 dedb5c2fa0e0efbad04cc38fd60896c7e479454d4b74f5818d9aa4625281483b` for both). I sampled those four revisions, not every commit in between.

## 2. The one-phrase difference (diffed)

`receipt-02-diff.txt`, `diff <(sed -n '129,157p' <file>) <(sed -n '158,185p' <file>)`:

```
14c14
< | `journalctl --no-pager -n 1 -N` | accepted (exit 0); `-N` field-name output is unchanged from plain `-N` | same matrix, `ext_lines1_N` and `ext_plain_N`: both 2882 bytes and identical stdout SHA-256 `3480f2aac48ee794f741dfd7dbffa31c86d933df70482db14adf5e57dfc2f20a` |
---
> | `journalctl --no-pager -n 1 -N` | accepted (exit 0); field-name output is unchanged from plain `-N` | same matrix, `ext_lines1_N` and `ext_plain_N`: both 2882 bytes and identical stdout SHA-256 `3480f2aac48ee794f741dfd7dbffa31c86d933df70482db14adf5e57dfc2f20a` |
29d28
<
```

So the substantive difference is at note line **142** (first block) versus **171** (second block): the second block omits the code span `` `-N` `` and its trailing space before `field-name output` — 5 bytes. The remaining 1-byte delta is the blank separator line 157 that `29d28` reports. Byte counts 3629 vs 3623 agree with 6 bytes total. `cat -A` shows no trailing-whitespace or line-ending difference on either side.

Precision note on the routed text: §6 item 1 and `corpus/lessons/round-37-verifier-spotcheck.md:62` say "The blocks differ by one phrase". That holds for text; the byte-level diff also carries the separator blank line, and the phrase difference is a **loss of the code span**, not of the words, which is why it matters to §3.

## 3. Which block is operative, and why (evidence, not position)

Both copies come from the same commit, so neither is later in history. The operative copy is fixed by the committed conformance gate:

- `tools/check-journalctl-v262-corrections.py:53` requires the verbatim phrase ``"`-N` field-name output is unchanged from plain `-N`"``; selftest case `missing-n-unchanged` at `:115` proves that phrase is load-bearing.
- Scored per copy by importing the tool's `evaluate()` (counter bytes `sha256 6fb5b589e2ac2678013885e7cb0bcb290d83d1547e0e3389d9360f2a858fd0cc`; `receipt-04-operability.txt`): first copy alone `PASS`, 0 findings; second copy alone `FAIL`, exactly one `C2-CLAIM-MISSING`; the committed 185-line note `PASS`, 0 findings.

**Operative block: lines 129-157, the first copy.** Lines 158-185 are inert duplicate history. This also keeps the more precise text (the second copy is a strict degradation that drops a code span). Choosing "last block governs" instead would leave the note's own gate unable to pass on the block it declared, so that alternative is rejected on evidence, not taste.

## 4. Exact append-only draft (for the lane to land as an appending commit)

Path: `corpus/knowledge/journalctl-v262-field-filter-r36.md`, appended after line 185. Copy kept byte-exact at `.ufo/waves/round-38/w1/DefDupBlock/draft-block.md` (`sha256 711bc5ed1c9c67de1a63a0c7c6a2e3a8ac40ed619a026d79015296dc9a814971`, 3576 bytes, 15 lines).

```markdown
## Round 38 correction — duplicate round-37 block

The round-37 correction block appears twice in this note, and both copies were introduced by one commit: `543a7ce` (`543a7cee2c5119f42023aa72597ce452d4a060d5`, "round-37: correct journalctl v262 note and add finite counter", 2026-10-25T16:20:15-03:00). Its parent `8936643` holds 127 lines and no such heading, and `git log -G'^## Round 37 correction' -- corpus/knowledge/journalctl-v262-field-filter-r36.md` returns only `543a7ce`, so no later commit repaired or re-added the duplicate (swept 2026-10-26 over this file's full history).

The heading `## Round 37 correction — predicate count, output states, action precedence and prior teaching` sits at line 129 and again at line 158. The first copy occupies lines 129-157; the second occupies lines 158-185 and ends the file. `grep -c '^## Round 37 correction' corpus/knowledge/journalctl-v262-field-filter-r36.md` therefore returns 2, and it returns 2 at `543a7ce`, at the round-37 tip `c231d0b`, at the round-38 base `8bd001f` and at `5edb6c2`, the revision these line numbers were measured at. No commit after `543a7ce` edits this file, and the file is byte-identical at `543a7ce` and `5edb6c2` (sha256 `dedb5c2fa0e0efbad04cc38fd60896c7e479454d4b74f5818d9aa4625281483b`), so the line numbers are stable across that range and this appended block leaves them unchanged.

**Operative block: lines 129-157, the first copy.** Lines 158-185 are a duplicate: they assert nothing the first copy does not assert, so read every citation of "the round-37 correction" against lines 129-157 and treat lines 158-185 as inert history. Nothing is deleted by this correction, which is an append-only block in the sense of QUALITY 4.

The two copies differ in one phrase and one separator. In the `-n` output table the operative copy's `-N` row (line 142) prefixes the words `field-name output` with the code span `` `-N` `` and one space; the duplicate's `-N` row (line 171) begins that same cell at `field-name` directly, without the code span. That 5-byte omission is the only textual difference: `diff <(sed -n '129,157p' corpus/knowledge/journalctl-v262-field-filter-r36.md) <(sed -n '158,185p' corpus/knowledge/journalctl-v262-field-filter-r36.md)` reports one changed line (block-relative 14, note lines 142 and 171) and one deleted blank line (block-relative 29, note line 157, the separator before the duplicate heading). Block sizes are 3629 and 3623 bytes.

Which copy is operative is fixed by the committed conformance gate, not by position. `tools/check-journalctl-v262-corrections.py` requires that code span in the `-N` row (`:53`, selftest case `missing-n-unchanged` at `:115`). Scored on the first copy alone its `evaluate()` returns PASS with 0 findings; scored on the second copy alone it returns FAIL with exactly one `C2-CLAIM-MISSING` finding for the missing phrase; the note as committed at `5edb6c2` returns PASS with 0 findings. The first copy is therefore the load-bearing one, and a later round that deletes the duplicate would lose no gated content.

### QUALITY check for this correction

QUALITY 1-3, 4, 9 and 14: pass — every statement here is about committed bytes and carries its re-runnable command and scope (`grep -n '^## Round 37 correction'`, the `diff` above, `git log -G` over this file's history, and the gate's `--selftest`, which returns 7/7 PASS). The block deletes nothing, separates observation (line numbers, byte counts, diff shape) from inference (none is needed), and claims no new host behaviour, coverage surface or ordinal move.
```

Draft-safety checks I ran in scratch before proposing it (all PASS, `receipt-04-operability.txt`):

- Appending `"\n" + draft` to the committed note is a pure append: `diff -u` yields 1 hunk, **0 deleted** lines, 16 added lines, and the augmented note is 201 lines.
- The augmented note still scores `PASS`, 0 findings, 3 checked under `evaluate()`, and still has exactly two `## Round 37 correction` headings plus one `## Round 38 correction` heading at lines 129/158/187.
- The draft deliberately does **not** reproduce the gate's required phrase contiguously (`"`-N` field-name output is unchanged from plain `-N`"` absent; `"`-N` field-name"` absent). If it did, a future deletion of the operative `-N` row would stop failing the gate; this keeps the gate's discriminating power intact while still naming the difference exactly.

## 5. Gates and companions

- `python3 tools/check-journalctl-v262-corrections.py --selftest` → `{"cases": 7, "passed": 7, "failures": [], "status": "PASS"}`, exit 0 (`receipt-03-counter.txt`).
- `python3 tools/check-journalctl-v262-corrections.py --revision 5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` → `checked 3, mismatches 0, PASS`, exit 0.
- Companion sweep for this note (`ls corpus/knowledge/ | grep journalctl-v262`) returns only `journalctl-v262-field-filter-r36.md`; there is no JSON companion, so QUALITY 67 (`R27-COMPANION-UNSWEPT`) has nothing to mark here.
- Nothing else cites the correction block by line number: `corpus/README.md:282` describes the round-37 correction without line references, and `SKILL.md:3111` describes the gate's semantics. So no README/SKILL edit is required for this duplicate marking. (Pre-existing and out of scope: `corpus/README.md:264` and `:269` still read "16-term predicate"; `:282` already marks those rows historical.)
- The counter bytes I measured are `sha256 6fb5b589…` (current, unfrozen — the routed defect 2 at `corpus/lessons/round-37-verifier-spotcheck.md:126` stands: this counter still carries no freeze sha), so the per-copy scoring in §3 binds those exact bytes only.

## 6. What I did not do

- Did not edit, create or delete any tracked lane file; no `git add`/`commit`/`stash`/`checkout`/`reset`/`push`, no jj command, no index or ref change (`git status --porcelain` shows only pre-existing untracked `.ufo/waves/round-38/` paths).
- Did not land the draft, so no gate exists at any new revision; the PASS statements above are at `5edb6c2` (committed note) and on scratch strings (draft-safety), nothing else.
- Did not re-run `journalctl` or any host probe; no package, service, hook, sysfs, counter-reset, boot or `/etc` change; no `sudo`; no tool installed or upgraded.
- Did not verify the heading count at *every* intermediate commit (four revisions sampled), and did not run `check-registry-coverage.py` or other wave gates (no commit was made to gate).
- Scratch `/fast/scratch/hyaku/tsukuroi-r38/DefDupBlock/` removed after copying receipts into the seat dir.

## Receipts

- `.ufo/waves/round-38/w1/DefDupBlock/receipt-01-headings.txt` — heading lines, per-revision counts, `git log -G`, byte-identical sha256, parent line count.
- `.ufo/waves/round-38/w1/DefDupBlock/receipt-02-diff.txt` — both-block `diff` (plain and `cat -A`), byte counts, block sha256s, lines 142/171 verbatim, lines 157/158/185.
- `.ufo/waves/round-38/w1/DefDupBlock/receipt-03-counter.txt` — counter `--selftest`, counter `--revision 5edb6c2`, phrase locations in the counter.
- `.ufo/waves/round-38/w1/DefDupBlock/receipt-04-operability.txt` — per-copy and augmented-note `evaluate()` results, counter digest, pure-append diff, draft phrase-absence checks.
- `.ufo/waves/round-38/w1/DefDupBlock/draft-block.md` — byte-exact draft text proposed in §4.
