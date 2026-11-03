# E3 — routed-repair draft (R64-SPOTCHECK-C1-PROOF)

Deliverable for the L1 only. Two landable texts follow — **A** for `SCORECARD.md` (append at end of
file, after the round-65 declaration) and **B** for `LOG.md`. Both are append-only; neither changes
a claim, a verdict, an axis value or a gate. This seat did not edit either file.

Everything below is measured; the transcript is
`.ufo/waves/round-65/w1-artifacts/E3/routed-repair-receipt.txt`.

---

## A. SCORECARD.md block — append verbatim

## Round 65 — routed repair (R64-SPOTCHECK-C1-PROOF)

Append-only repair. It supersedes the WORDING of the round-64 C1 identity proof and nothing else: the
normalization fact stands as measured (stray-CR 381/5452/4723 at `2f3061ef` → 0/0/0 at `431f0c9`;
`SCORECARD.md` byte-identical between the CR-stripped declaration base and the cited blob). No axis
value, claim, predicate or gate changes; round 64's C1 verdict is untouched.

The round-64 closure (`corpus/lessons/round-64-verifier-spotcheck.md` §5, routed defect
R64-SPOTCHECK-C1-PROOF) ruled:

> **(minor, fix next round)** The C1 identity proof as worded (`git show 2f3061ef:F | tr -d '\r' |
> cmp - F` rc 0 ×3) is only true against the fix-time worktree; re-run against the cited measured
> revision `431f0c9` it is false for SOURCES/SKILL because the same commit carries the round's
> additive work. The normalization fact stands (stray-CR 0/0/0; additive-only delta, removed=0) —
> next round, state the identity proof against the fix-time tree explicitly, or re-express as
> "stripped-base vs blob diff is additions only" so the counting command re-runs green at the cited
> revision. Status-neutral; this closure re-derived the fact either way.

**What the original wording compared, stated precisely.** Its right-hand operand `F` was the
*uncommitted worktree at fix time*, not any committed revision. At that instant the worktree carried
only the CR normalization, proven twice inside the r64 receipt
`.ufo/waves/round-64/after/c1-cr-identity.txt`: `git diff --numstat` read 381/381 `corpus/SOURCES.md`,
5452/5452 `SKILL.md`, 4723/4723 `SCORECARD.md` (deletions == insertions == that file's CR count, so no
additive work was present), and `git status --porcelain -uno` listed those three ` M` entries and
nothing else. The end-state digests recorded there — `e1558e4b…`, `bda5249b…`, `13047505…` — are
byte-identical to `git show 2f3061ef:F | tr -d '\r'` recomputed from committed bytes in round 65, so
the operand *was* the stripped base and `cmp` held there by construction. It cannot hold at the cited
revision, which is the same commit that added the round's work: at `431f0c9` `cmp` returns rc 1 for
`corpus/SOURCES.md` (first difference char 238601, line 289 = the S279 insertion) and for `SKILL.md`
(`cmp: EOF on - after byte 1351538` — the base is a strict prefix), and rc 0 only for
`SCORECARD.md`. **The proof was true of a moment, not of a revision.**

**Re-expressed proof** — the form the closure asked for, re-runnable green at the cited revision from
committed bytes alone (measured 2026-11-03; host `diff` is pi-uu-diff 0.8.0, not GNU diff, so the
counts come from `git diff --no-index --numstat`):

```sh
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
BASE=2f3061ef; REV=431f0c9; fail=0
while read -r F ea er; do
  got=$(git --no-pager diff --no-index --numstat \
        <(git show "$BASE":"$F" | tr -d '\r') <(git show "$REV":"$F") 2>/dev/null || true)
  a=$(printf '%s\n' "$got" | awk 'NF{print $1; exit}'); a=${a:-0}
  r=$(printf '%s\n' "$got" | awk 'NF{print $2; exit}'); r=${r:-0}
  printf '%-18s added=%-4s removed=%-3s (expected %s/%s)\n' "$F" "$a" "$r" "$ea" "$er"
  { [ "$a" = "$ea" ] && [ "$r" = "$er" ]; } || fail=1
done <<'EOF'
corpus/SOURCES.md 3 0
SKILL.md 120 1
SCORECARD.md 0 0
EOF
echo "gate rc=$fail"; exit "$fail"
```

Output at `431f0c9`:

```
corpus/SOURCES.md  added=3    removed=0   (expected 3/0)
SKILL.md           added=120  removed=1   (expected 120/1)
SCORECARD.md       added=0    removed=0   (expected 0/0)
gate rc=0
```

Reading of the three pairs:

- `corpus/SOURCES.md` **+3/−0** — the round's three registry rows S279/S280/S281 at id position
  (hunk `@@ -288,0 +289,3 @@`, directly after S278), nothing else moved;
- `SKILL.md` **+120/−1** — the round's SKILL appends. The `−1` removes no content: the declaration
  blob ends at byte `0x2e` with no terminal newline, the removed line and added line #1 are the same
  859 bytes, and with a terminal newline restored on the base the same diff is `119 0`. The `−1` is
  the disclosed EOF-newline artifact, now proven byte-for-byte rather than asserted;
- `SCORECARD.md` **0/0** — byte-identical (`cmp` rc 0, sha256 `13047505…` on both sides).

So the round-64 delta against the CR-stripped declaration base is **additions only** in all three
files: the normalization rewrote no content anywhere.

Able to fail: the same gate with `REV=2f3061ef` prints `381/381`, `5452/5452`, `4723/4723` and exits
1 — it sees the unnormalized tree as a full-file rewrite, and those counts equal the raw CR counts
(i.e. the r64 instrument, reproduced). Receipt: `.ufo/waves/round-65/w1-artifacts/E3/routed-repair-receipt.txt`
(§2 measured counts, §3 the three-state table on the original wording, §4 gate + negative control).
Independent agreement: `.ufo/waves/round-65/after/reidentity-at-431f0c9.txt` states the same three
pairs from a separate extraction.

---

## B. LOG.md entry — append verbatim

## Round 65 — routed repair (R64-SPOTCHECK-C1-PROOF), receipt-after-subject

The round-64 closure's routed defect — the C1 identity proof as worded (`git show 2f3061ef:F | tr -d
'\r' | cmp - F` rc 0 ×3) holds only against the fix-time worktree, not the cited measured revision
`431f0c9` — is discharged by re-expressing the proof as "CR-stripped declaration base vs cited blob =
additions only", which re-runs green at the cited revision from committed bytes alone:

- `corpus/SOURCES.md`: added 3 / removed 0 — S279-S281 at id position (hunk `@@ -288,0 +289,3 @@`);
- `SKILL.md`: added 120 / removed 1 — the `−1` is the disclosed EOF-newline artifact: the removed
  line and added line #1 are the same 859 bytes and the base's last byte is `0x2e` (no terminal
  newline); with the terminal newline restored the same diff is `119 0`, so removed content is zero;
- `SCORECARD.md`: added 0 / removed 0 — byte-identical, sha256 `13047505…` both sides.

The original wording's operand is stated exactly: the uncommitted worktree at fix time, whose
recorded state (`git diff --numstat` 381/381, 5452/5452, 4723/4723 — the CR counts, no additive work;
`git status --porcelain -uno` = the three ` M` entries only; end-state digests `e1558e4b…`,
`bda5249b…`, `13047505…` in `.ufo/waves/round-64/after/c1-cr-identity.txt`) equals the CR-stripped
declaration blobs recomputed from committed bytes. At `431f0c9` the wording fails precisely at the
additive work (SOURCES first difference char 238601 / line 289; SKILL `cmp: EOF on - after byte
1351538`). Counting command green at `431f0c9` (rc 0) and red at `2f3061ef` (rc 1: 381/381, 5452/5452,
4723/4723 — able to fail). Receipt
`.ufo/waves/round-65/w1-artifacts/E3/routed-repair-receipt.txt`; SCORECARD block
`## Round 65 — routed repair (R64-SPOTCHECK-C1-PROOF)`. Not a claim: no axis value, predicate, gate
or round-64 verdict changes.

---

## Landing notes for the L1

1. Both texts are append-only; block A goes at the end of `SCORECARD.md` (after `## Round 65 —
   declaration (2026-11-03, base `1bd8e196`, …)`), block B at the end of `LOG.md`. Nothing else in
   either file is touched, so both base→outcome diffs remain pure appends.
2. Title uses the house em dash, matching every other round heading (`## Round 62 — correction
   block…`, `## Round 64 — measured outcome…`); the id `R64-SPOTCHECK-C1-PROOF` is the literal grep
   target either way.
3. Block A is self-contained: it quotes the closure it supersedes, gives the exact command and the
   measured counts, and cites a receipt that exists in the tree. If the round's validator checks
   cited paths, both paths named there are committed by the L1 commit.
4. Pre-existing draft `.ufo/waves/round-65/drafts/scorecard-erratum-r64-proof.md` carries the same
   three pairs and the same mechanism; this seat measured them independently (separate blob
   extraction, separate counting tool) and additionally proved the SKILL `−1` byte-for-byte
   (`119 0` with the terminal newline restored). If only one block lands, land **A** — it is the
   only one carrying the receipt of the measurement.
