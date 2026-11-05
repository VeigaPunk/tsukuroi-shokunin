# ScribeOrdinal — round-82 w1 (scribe seat, C3 calibration)

**Scope.** Land C3's candidate: append one named ordinal correction to `SCORECARD.md` that retires
the round-81 depth contradiction, then prove it with the frozen instrument
`tools/check-scorecard-ordinals.py` (sha256 `888a3da9b34dcbd4786a815f5656854c946d2168b7d73cc9f79c2eaa7c341e84`,
unchanged by this seat).

**Axes walked.** calibration (C3: exactly one *after* ordinal per asserted (round, axis); one named
correction retires the disagreeing pair) · depth (the disputed value itself: which of 8 or 9 the lane
stands behind, and on whose authority) · no-harm (the file is append-only; nothing above the
correction was edited, and the instrument's own 8-case selftest is unchanged).

## Files written

| path | change |
|---|---|
| `SCORECARD.md` | +17 lines appended at the end (the one correction block). Nothing deleted or rewritten: `git diff --stat -- SCORECARD.md` → `17 insertions(+)`, 0 deletions. |
| `.ufo/waves/round-82/w1/ScribeOrdinal.md` | this report (named by the seat spec). |

`git status --porcelain` also shows ` M tools/count-mount-rows-r81.py`,
` M tools/measure-round81.py`, ` M corpus/knowledge/mount-unit-fstab-plane-r81.json` and
` M corpus/knowledge/mount-unit-fstab-plane-r81.md` — **not this seat's changes** (C1's and C2's
seats own those paths; this seat never opened them for writing). They appeared while this seat was
running, which is expected in a 13-seat wave sharing one working tree. Reported here only so the
integrator can attribute them correctly. No commit, no `git add`, no index/worktree mutation was
performed by this seat.

## The exact block appended (verbatim, `SCORECARD.md:7002-7018`)

```markdown
## Round 81 — ordinal correction (supersedes the depth ordinal asserted above)

supersedes-ordinal: round-81 depth

depth 8 → 8 — the round-81 depth ordinal is 8. Two round-81 outcome blocks were appended
to this file by two concurrent writers and they disagree about the depth after-ordinal:
the earlier block at `SCORECARD.md:6861` prints `C1 | depth 8 → 9` and
`Axes now: depth9`, while the later block at `SCORECARD.md:6903` prints
`depth 8 → 8 … no uplift claimed`. The lane stands behind the later block. The 9 in the
earlier block was an author-side self-assessment that the non-author closure
`corpus/lessons/round-81-verifier-spotcheck.md` does not endorse: that closure records
the depth verdict as improved while stating in so many words that the self-assessed
ordinal uplift is not endorsed by it, and it awards no promotion, scope transfer or
ordinal uplift. This correction names the single round-81 depth after-ordinal (8) and
retires the earlier assertion of it; no other round-81 ordinal value is asserted here,
and no other axis carries a conflicting number.
```

Structural requirements met, and each is machine-checkable against the frozen instrument's own
regexes:

- `supersedes-ordinal: round-81 depth` starts a line, exactly as written
  (`SCORECARD.md:7005`; grep `^supersedes-ordinal: round-81 depth$` → one hit, line 7005). The
  instrument's `SUPERSEDES` regex is `^supersedes-ordinal:\s*round-(\d+)\s+([a-z, ]+)$` matched
  against `line.strip()`, so the trailing space/comma class and the axis name must be lowercase —
  both hold.
- The heading is `## Round 81 — …`, so the block is filed under round 81 and the instrument's
  `BLOCK` regex (`^## Round (\d+)\b`) attributes it there.
- The reasoning names both prior blocks by line — `SCORECARD.md:6861` (prints `C1 | depth 8 → 9`
  and `Axes now: depth9`) and `SCORECARD.md:6903` (prints `depth 8 → 8 … no uplift claimed`) — and
  the non-author closure `corpus/lessons/round-81-verifier-spotcheck.md`, which does not endorse
  the 8→9 uplift. It states that the lane stands behind the later block (depth 8) and that the
  earlier block's 9 was a self-assessment the closure did not endorse. It states that no other
  round-81 ordinal value is asserted and no other axis carries a conflicting number.

## Verification (both commands, observed output)

Command 1 — the C3 counter over the edited file:

```
$ python3 tools/check-scorecard-ordinals.py --fixture /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md
{"claim": "C3", "revision": null, "count": 0, "examined": 77, "finding": "clean", "findings": []}
rc=0
```

`count 0`, exit 0 — the required outcome.

Command 2 — the instrument's own suite:

```
$ python3 tools/check-scorecard-ordinals.py --selftest
  ok   contradiction: rc=1 findings=1 examined=2
  ok   named-correction: rc=0 findings=0 examined=1
  ok   silent-correction: rc=1 findings=1 examined=1
  ok   single-block: rc=0 findings=0 examined=1
  ok   two-axes: rc=1 findings=2 examined=2
  ok   no-blocks: rc=2 could-not-evaluate no-round-blocks
  ok   hyphenated-name: rc=0 findings=0 examined=1
  ok   ascii-arrow: rc=1 findings=1 examined=1
SELFTEST total=8 passed=8 failed=0
rc=0
```

8/8, exit 0 — unchanged from the pre-edit run (same 8 lines, same results).

### Before/after, same instrument, same file

| state | command | observed |
|---|---|---|
| lane tip before the append (`HEAD` = `683ae4563bf6967ed0cc533aec06c971a1a87bbc`, byte-identical to the frozen control at `d5b3e134…`) | `python3 tools/check-scorecard-ordinals.py --revision 683ae4563bf6967ed0cc533aec06c971a1a87bbc` | `count 1, examined 78`, one finding: round 81, axis depth, ordinals `[8, 9]`, sites line 6861 (×3) and 6903; rc 1 |
| working tree after the append | `python3 tools/check-scorecard-ordinals.py --fixture …/SCORECARD.md` | `count 0, examined 77`, `finding clean`; rc 0 |

The pre-edit reading reproduces the frozen no-work control exactly
(`.ufo/waves/round-82/before/controls.txt:31-33` records the same `count 1`, same ordinals
`[8, 9]`, same sites 6861/6903 at `d5b3e134…`). `examined` drops 78 → 77 because retiring
`(81, depth)` removes that one (round, axis) key from the examined set — the instrument's own
`named-correction` selftest case shows the same shape (`examined=1`).

Instrument bytes untouched by this seat: `sha256sum tools/check-scorecard-ordinals.py` →
`888a3da9b34dcbd4786a815f5656854c946d2168b7d73cc9f79c2eaa7c341e84`, equal to the value frozen in
the round-82 declaration row for C3.

File provenance: `sha256sum SCORECARD.md` → `27be59322c63e710b8d631eade3641617471d66e7a8af57745842c97bef44d50`
(after); `git show HEAD:SCORECARD.md | sha256sum` → `98b4df16e4b9e283b63b367524bfe7ea77aa3074e9fb9d5bc9516bb50029935d`
(before).

### Why depth 8 and not 9 (authority, not preference)

`corpus/lessons/round-81-verifier-spotcheck.md` (committed at `d5b3e13492b3878fc8734368b0bbcab04f6c79c0`,
`git merge-base --is-ancestor d5b3e134… HEAD` holds; `git cat-file -e HEAD:corpus/lessons/round-81-verifier-spotcheck.md`
→ present) states, verbatim:

- `Status **ok**, admitted **false**, verdict **rejected-honest-stop**.`
- `| depth | improved | … the self-assessed ordinal 8→9 is **not** endorsed by this closure (the lane's own second outcome block says "depth 8 → 8 … no uplift claimed") |`
- `No promotion, capability, scope transfer or ordinal uplift is awarded.`
- routed defect `R81-V1 SCORECARD depth contradiction` … `Append a named correction stating one ordinal; this closure awards no uplift.`

The closure therefore does not endorse the uplift, and the lane's own later round-81 block prints
`depth 8 → 8 (one plane, finite equality counter; no uplift claimed)`. Depth 8 is the value the
lane stands behind. [INFERENCE] The closure's `improved` verdict on depth concerns the *content*
(the new eight-row mount-unit plane), not the ordinal number; the ordinal is what the lane
asserts, and the closure awards no uplift.

## Other contradictions found in `SCORECARD.md` — reported, not fixed

These are outside this seat's write scope (one appended block) and outside C3's mechanical scope
(the instrument only counts (round, axis) ordinal collisions). Each is quoted, not paraphrased.

1. **The prose of the retired block still prints `depth9`.** `SCORECARD.md:6898` still reads
   `Axes now: depth9, coverage9, operability9, freshness9, calibration9, adjacency8.`, and
   `SCORECARD.md:6872` still reads `| C1 | depth 8 → 9 |`. The instrument retires these by the
   supersedes line, so the counter is clean, but a human reading the file top-to-bottom still meets
   "depth9" in a round-81 block whose heading (`:6861`) reads "three claims, all met at `c6fd9949`".
   The appended block names the conflict and states depth 8 stands; it cannot rewrite `:6861` or
   `:6898` without violating the append-only/no-delete bound.

2. **The depth ordinal's own counting command was a file count.** `SCORECARD.md:6882`:
   `Score deltas and their counting commands: depth 8→9 — `ls corpus/knowledge/*.md | wc -l``. The
   8→9 transition is evidenced by counting knowledge files, not by any ordinal-scaled measurement.
   This is the self-assessment the closure declined to endorse. This seat did not re-derive or
   contest that command; the C1 counter (`tools/count-mount-rows-r81.py`) is C1's instrument, not
   C3's.

3. **Round 81's admission verdict conflicts with the SCORECARD's own round-81 outcome blocks.**
   `SCORECARD.md:6861`'s heading says `## Round 81 — measured outcome (three claims, all met at
   `c6fd9949`)` and its rows end `met`, while the non-author closure says `admitted **false**,
   verdict **rejected-honest-stop**` because `none of the three claims was declared before data`.
   Both `SCORECARD.md:6900` (`Non-author closure and its spot-check are pending; author verdicts
   only.`) and the heading at `SCORECARD.md:6903` (`author-side, non-author closure pending`) are
   stale: the closure has landed at `d5b3e134…` and its verdict is not recorded anywhere in
   `SCORECARD.md` (grep for `rejected-honest-stop` / `admitted false` → no hits outside this seat's
   report). The round-82 declaration block (`:6965`) cites `R81-V2` but not the closure's verdict.
   This is a verdict-vs-verdict conflict, not an ordinal collision, so C3's counter cannot see it.

## Known limits of this seat's evidence

- The C3 counter is a regex/ordinal checker over `SCORECARD.md` blocks. `count 0` means the file
  carries no *unretired* two-valued (round, axis) disagreement. It does **not** mean the file's
  prose is internally consistent (items 1–3 above), and it does not adjudicate which of two
  disagreeing ordinals is truthful — that authority came from the non-author closure, read here.
- Because the supersede retires `(81, depth)` wholesale, the instrument does not independently
  re-check that the surviving value is 8; it checks that no *second* value survives. The named
  value is 8 by the text of the correction block, and the file is checked clean.
- The instrument's `--revision` mode reads `SCORECARD.md` out of a git revision. This seat did not
  commit (the L1 commits; a seat that commits breaks the round), so `--revision HEAD` still shows
  the pre-append `count 1`. The two commands the seat spec names are `--fixture` (working tree) and
  `--selftest`; both were run and are quoted above verbatim.
- No claim is made here about C1's raw-line anchors or C2's mutant kills; this seat read neither
  instrument's output and neither is C3's axis.

## Scratch

No scratch directory was created: this seat needed no clone, mirror, fixture, mutant copy or temp
tree. All work was done in place in the lane's working tree, and the only files written are the two
listed above. There is nothing to delete under `/fast/scratch/hyaku/tsukuroi-r82/ScribeOrdinal/`
(that path does not exist).

## Tooling

No tool was installed or upgraded by this seat; the frozen instrument already present was used
unmodified (`python3`, `git`, `sha256sum` only).
