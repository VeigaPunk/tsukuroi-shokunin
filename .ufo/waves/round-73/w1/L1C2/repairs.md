# Round-73 C2 repair drafts (L1 working copy; the wave's E2Routed/R2Reviewer findings amend these)

## 1. Append to `corpus/lessons/round-72.md`

```markdown
## Correction (round 73, append-only; R72-LESSON-SUPERSEDED-CLAIMS)

The round-72 trend verdicts above say "No capability row enters this round" and the C2 section says the
suite is "nine hermetic cases". Both are superseded by the round's own landing, and the superseded
sentences stay visible as filed. The landed state is the `gate-selftest` capability row in
`SCORECARD.md` (round 72) and a **ten**-case suite (`SELFTEST: PASS (10 cases, 10 passed, 0 failed)`,
`.ufo/waves/round-72/after/selftest-selftest-after.txt`, tool sha256 `f22eb94f…`), as the SCORECARD
supersession note and the round-72 LOG entry already record. Counted by
`python3 tools/check-r72-routed-r73.py --revision <REV>` (item LESSON).
```

## 2. Append to `SCORECARD.md`

```markdown
## Round 72 — instrument digest erratum (appended round 73; R72-C3-INSTRUMENT-DIGEST-DRIFT)

The round-72 declaration froze `tools/check-r71-routed-r72.py` at sha256
`df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712` (`SCORECARD.md:5616`). The tool's
committed bytes are `2610ff433bf5d4e945ce5b2da0cf168745e4142ecffabc3d160afee33005cdcc`, at the round-72
landing and at the present tip alike; the frozen string matches no committed blob, and the tool did not
exist at the declaration's declared base `a7015d27` (it was created in round 72), so the frozen digest
could not have been taken from any revision. The round-72 erratum described the three repairs (unanchored
block, receipt provenance, token list) without recording a digest old→new; this block records it.

**Same-instrument evidence, re-run with the final instrument** (`.ufo/waves/round-73/after/
r72-c3-same-instrument-before.txt`): `python3 tools/check-r71-routed-r72.py --revision a7015d27` reads
`ROUTED_STALE=3` rc 1 (pre-repair) and `--revision eb105757` reads `ROUTED_STALE=0` rc 0 (post-repair),
with the tool's bytes `2610ff43…` on both sides. `--revision` selects only the data revision the tool
reads, so this is a same-instrument pair; the frozen `df8a59c7…` is superseded by `2610ff43…`.
Counted by `python3 tools/check-r72-routed-r73.py --revision <REV>` (item DIGEST).

## Capability refresh — round 73 (append-only)

The `gate-selftest` row above (round 72) still reads "nine named cases" and `PASS 9/9`. The landed
instrument prints **ten** cases (`SELFTEST: PASS (10 cases, 10 passed, 0 failed)`, receipt
`.ufo/waves/round-72/after/selftest-selftest-after.txt`, tool sha256 `f22eb94f…`), the tenth being
`SELFTEST-CASES`, which fails when a declared case row is deleted. Read the row with this line as its
current count; the row's own text stays as filed (QUALITY 99). Counted by
`python3 tools/check-r72-routed-r73.py --revision <REV>` (item CAPABILITY).
```
