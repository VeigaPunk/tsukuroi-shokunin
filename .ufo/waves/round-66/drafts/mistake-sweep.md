2026-11-03T21:14:36Z

# E3Mistake — round-65 in-place SCORECARD edit: RED/PASS append-only sweep

Seat: E3Mistake (executor, round 66 wave w1). All reads are read-only git. No tracked file edited.

Defect under test: round 65 edited one already-filed SCORECARD line in place — the round-63
"Measured outcome" sentence — instead of appending an erratum (closure defect 2 of
`corpus/lessons/round-65-verifier-spotcheck.md` §1: "SCORECARD prior-round line edit").

```
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r66/E3Mistake
```

Revisions:
- known-bad pair: `1bd8e196` (round-65 base) .. `7ab7c876` (round-65 judged tip)
- append-only control pair: `c68bfe97` (round-66 base) .. working copy = HEAD `aa75398e`

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse 1bd8e196 7ab7c876 c68bfe97 HEAD
1bd8e19666a12e5aeea0e485983cd289ebd11ebc
7ab7c8760fcc6766248df23a6a1db3bbdd8190fa
c68bfe97e9ed8fda5477fa9ba80f979eaf278fd0
aa75398e0d0ae837b438a52b7be5a226633e3b2a
rc=0
```

## 1. RED — the sweep must be able to fail (known-bad round-65 pair)

### RED-1: raw removed-line count

```
$ git -C "$L" diff 1bd8e196 7ab7c876 -- SCORECARD.md > "$S/r65-raw.diff"
rc=0
$ wc -l "$S/r65-raw.diff"
129 /fast/scratch/hyaku/tsukuroi-r66/E3Mistake/r65-raw.diff
rc=0
$ grep -c '^-[^-]' "$S/r65-raw.diff"
1
rc=0
```

The item's verbatim pipeline form:

```
$ git -C "$L" diff 1bd8e196 7ab7c876 -- SCORECARD.md | grep -c '^-[^-]'
1
grep_rc=0
```

### RED-2: CR-stripped removed-line count (the frozen form)

```
$ diff <(git -C "$L" show 1bd8e196:SCORECARD.md | tr -d '\r') <(git -C "$L" show 7ab7c876:SCORECARD.md | tr -d '\r') > "$S/r65-stripped.diff"
diff_rc=1        # files differ
$ grep -c '^<' "$S/r65-stripped.diff"
1
grep_rc=0
$ grep -c '^>' "$S/r65-stripped.diff"
113
grep_rc=0
```

Verbatim pipeline form:

```
$ diff <(git -C "$L" show 1bd8e196:SCORECARD.md | tr -d '\r') <(git -C "$L" show 7ab7c876:SCORECARD.md | tr -d '\r') | grep -c '^<'
1
grep_rc=0
```

Expected on this pair: >= 1 removed line. Observed: **1**. RED holds (the check can fail).

The 113 `>` lines decompose as 1 replacement addition + 112 appended lines (base 4787 lines
→ tip 4899 lines; 4899 − 4787 = 112). The raw diff has two hunks:
`@@ -4647,7 +4647,7 @@` (the in-place edit) and `@@ -4785,3 +4785,115 @@` (the append).

### RED-3: the removed line, verbatim

```
$ grep '^<' "$S/r65-stripped.diff" | head -3 | cut -c1-200
< view is untrusted on this host, r56/r57 lesson). Gates at the work revision: knowledge-header PASS
rc_pipeline=0
```

Raw unified-diff form (same line, `-` prefix, no space):

```
$ grep '^-[^-]' "$S/r65-raw.diff" | head -3 | cut -c1-200
-view is untrusted on this host, r56/r57 lesson). Gates at the work revision: knowledge-header PASS
rc_pipeline=0
```

Context, base `1bd8e196:SCORECARD.md` lines 4646-4651:

```
4646:## Round 63 — measured outcome (2026-11-01, author-side; non-author closure pending)
4647:
4648:Measured at the work tree `82f0e1a9` (declaration `cdfd8b8c`; counting battery
4649:`.ufo/waves/round-63/after/c1-c2-counts-at-work.txt`, plumbing reads of the revision — the worktree
4650:view is untrusted on this host, r56/r57 lesson). Gates at the work revision: knowledge-header PASS
4651:**79 notes / 0 findings / 79 complete** (JSON `.ufo/waves/round-63/after/knowledge-header-at-work.json`,
```

Context, tip `7ab7c876:SCORECARD.md` lines 4648-4651 (same paragraph, line 4650 rewritten):

```
4648:Measured at the work tree `82f0e1a9` (declaration `cdfd8b8c`; counting battery
4649:`.ufo/waves/round-63/after/c1-c2-counts-at-work.txt`, plumbing reads of the revision — the worktree
4650:view is untrusted on this host, r56/r57 lesson). Adjacency anchors gate: FAIL at `2ddd5e79` (IN-109 line shifted by the arm), PASS **114/114** at `cecc9e3e` after the re-pin. Gates at the repair revision: knowledge-header PASS
4651:**79 notes / 0 findings / 79 complete** (JSON `.ufo/waves/round-63/after/knowledge-header-at-work.json`,
```

Line 4650 grew from 99 bytes / 15 words (base) to 227 bytes / 34 words (tip): the round-63
sentence was edited in place, not superseded by an appended erratum. This is exactly closure
defect 2.

CR-byte check (the `tr -d '\r'` is inert on these files):

```
$ for r in 1bd8e196 7ab7c876 c68bfe97; do printf '%s CR-lines=' "$r"; git -C "$L" show $r:SCORECARD.md | grep -c $'\r'; done
1bd8e196 CR-lines=0
7ab7c876 CR-lines=0
c68bfe97 CR-lines=0
$ printf 'worktree CR-lines='; grep -c $'\r' "$L/SCORECARD.md"
worktree CR-lines=0
# each grep -c exits 1 on zero matches; the printed count is 0 in all four cases (no CR bytes)
# re-checked: git show 1bd8e196:SCORECARD.md | grep -c $'\r' → 0, grep_rc=1; worktree → 0, rc=1
```

Consequence stated plainly: on the bytes measured here, raw and CR-stripped counts agree
(1 on the known-bad pair); the stripping removes no bytes. The frozen form is still run as
specified and remains the portable form for files that do carry CRLF.

## 2. PASS — append-only control on the round-66 landing (must be able to pass)

```
$ diff <(git -C "$L" show c68bfe97:SCORECARD.md | tr -d '\r') <(tr -d '\r' < /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md) > "$S/r66-append-control.diff"
diff_rc=1        # files differ (additions only)
$ grep -c '^<' "$S/r66-append-control.diff"
0
grep_rc=1        # grep rc 1 = no matching line; this is the expected 0
$ grep -c '^>' "$S/r66-append-control.diff"
29
grep_rc=0
$ grep -n -v '^>' "$S/r66-append-control.diff"
1:4899a4900,4928
grep_rc=0
```

Verbatim pipeline form:

```
$ diff <(git -C "$L" show c68bfe97:SCORECARD.md | tr -d '\r') <(tr -d '\r' < /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md) | grep -c '^<'
0
grep_rc=1
```

Expected: 0. Observed: **0**. The control single hunk is `4899a4900,4928`: 29 added lines,
no removed line, no no-newline marker.

Sensitivity (the same PASS-form command applied to the known-bad pair returns 1, not 0):

```
$ diff <(git -C "$L" show 1bd8e196:SCORECARD.md | tr -d '\r') <(git -C "$L" show 7ab7c876:SCORECARD.md | tr -d '\r') | grep -c '^<'
1
grep_rc=0
```

So the identical check discriminates: 1 on the round-65 in-place edit, 0 on the round-66
landing. PASS is not vacuous.

### Grounding: the round-66 landing is the declaration commit and is additive

```
$ git -C "$L" diff --numstat c68bfe97..HEAD -- SCORECARD.md
29	0	SCORECARD.md
rc=0
$ git -C "$L" log --oneline c68bfe97..HEAD -- SCORECARD.md
aa75398e round-66: freeze declaration (C1 depth S283, C2 adjacency anchors) and wave w1 spec
rc=0
$ git -C "$L" show --stat --oneline --format='%H %s' HEAD
aa75398e0d0ae837b438a52b7be5a226633e3b2a round-66: freeze declaration (C1 depth S283, C2 adjacency anchors) and wave w1 spec
 .../round-66/before/absence-controls-receipt.txt   |  19 ++
 .ufo/waves/round-66/before/census-before-receipt.txt |  47 ++++
 .ufo/waves/round-66/before/s283-open-receipt.txt   |  15 ++
 .ufo/waves/round-66/before/s283-open-v262-release.json |  56 +++++
 .ufo/waves/round-66/w1-plan.json                   | 250 +++++++++++++++++++++
 .ufo/waves/round-66/w1-plan.stderr                 |   0
 .ufo/waves/round-66/w1-spec.json                   | 153 +++++++++++++
 LOG.md                                             |  12 +
 SCORECARD.md                                       |  29 +++
 9 files changed, 581 insertions(+)
rc=0
$ git -C "$L" status --porcelain -- SCORECARD.md
(no output)
rc=0
$ git -C "$L" diff --stat HEAD -- SCORECARD.md
(no output)
rc=0
$ git -C "$L" merge-base --is-ancestor c68bfe97 HEAD; echo rc=$?
rc=0
```

The working copy equals HEAD for SCORECARD.md; HEAD `aa75398e` is a descendant of base
`c68bfe97` and is the only commit in the range touching SCORECARD.md; it adds 29 lines and
removes 0. The declaration only appends.

## 3. Outcomes

| Check | Command (as above) | Expected | Observed | Outcome |
|---|---|---|---|---|
| RED-1 raw | `git diff 1bd8e196 7ab7c876 -- SCORECARD.md \| grep -c '^-[^-]'` | >= 1 | 1 (rc 0) | RED Holds |
| RED-2 CR-stripped | `diff <(show 1bd8e196) <(show 7ab7c876) \| grep -c '^<'` | >= 1 | 1 (rc 0; diff rc 1) | RED Holds |
| RED-3 quote | `... \| grep '^<' \| head -3 \| cut -c1-200` | the removed line | `< view is untrusted on this host, r56/r57 lesson). Gates at the work revision: knowledge-header PASS` | RED Holds |
| PASS | `diff <(show c68bfe97) <(worktree) \| grep -c '^<'` | 0 | 0 (grep rc 1; 29 additions) | PASS |
| Sensitivity | same PASS form on 1bd8e196..7ab7c876 | 1 | 1 (rc 0) | check discriminates |
| CR bytes | `grep -c $'\r'` per revision | (shape) | 0/0/0/0 | stripping inert here |

## 4. Scope limit — the class elsewhere

The same class in other filed rounds is **not verified here**. This sweep measures exactly two
pairs: the round-65 known-bad pair (`1bd8e196..7ab7c876`) and the round-66 landing control
(`c68bfe97..aa75398e` as committed, working copy equal). No claim is made about rounds
37-64, about filed reports other than SCORECARD.md, or about sibling repositories. The command
form generalizes to any `<base>:<file>` .. `<landing>:<file>` pair, but no other pair was run.

## 5. Proposed QUALITY criterion text (one paragraph; QUALITY.md not edited)

**Append-only corrections (proposed).** A correction to bytes already filed in `SCORECARD.md`
— and, by the same form, to a filed report — lands as an appended erratum naming the
superseded text, never as an in-place edit; the round gate checks this with the CR-stripped
removed-line sweep `diff <(git show <base>:SCORECARD.md | tr -d '\r') <(tr -d '\r' < SCORECARD.md) | grep -c '^<'`
and requires **0** removed lines, with the receipt showing the check can fail: the round-65
pair `1bd8e196..7ab7c876` returns **1** removed line (the round-63 "Measured outcome" sentence
at `SCORECARD.md:4650`, closure defect 2 of `corpus/lessons/round-65-verifier-spotcheck.md`)
while the round-66 declaration landing (`c68bfe97..aa75398e`) returns **0** in this sweep
(commands, outputs and rcs above, retained in `.ufo/waves/round-66/drafts/mistake-sweep.md`).

## 6. Receipt retention

Scratch `$S` (raw diff, stripped diff, control diff) is deleted before this seat yields. Every
number above is the verbatim output of the command printed with it; the commands re-derive the
scratch files (`git diff ... > "$S/r65-raw.diff"`, etc.). No tracked file was modified.
