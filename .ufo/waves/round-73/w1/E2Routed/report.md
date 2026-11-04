# E2Routed — C2 repair drafts against the frozen routed checker, plus tamper probes (r73/w1)

status: done
verdict: drafts pass the declared predicate in committed-bytes mode (3/3, rc 0) under the frozen
instrument and under both post-declaration hardened revisions; five of the required tamper probes hold,
one denial-form attack survives, and seven instrument findings (F1–F7, one frozen-only) are recorded
with commands.

## 0. Axes (Godspeed)

- **A1 predicate** — the three drafted blocks make `check-r72-routed-r73.py` print
  `ROUTED_STALE=0 ROUTED_OK=3/3` rc 0 in both `--root` and `--revision` modes.
- **A2 grounding** — every drafted sentence is measured against committed bytes, never inferred.
- **A3 discrimination** — probes that satisfy the predicate without the work must be separated from
  probes that do the work; each probe is reported `held` / `survived` with its output.
- **A4 committed-bytes mode** — the claim counts committed bytes only; a worktree-only fixture proves
  nothing.
- **A5 evidence economy** — one reproducible fixture recipe, no instrument edits, no lane mutations.

Kept moves: drafts phrased to satisfy the frozen instrument *and* the hardened one (no axis harmed);
fixtures rebuilt from base blobs after the worktree drifted (A4 improved); probe set extended to the
new code paths (A3 improved).

## 1. Instrument identity — the target moved during this seat

| instrument | sha256 | where |
|---|---|---|
| frozen by the declaration, committed at `8eeadcb9` | `93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e` | `git show 8eeadcb9:tools/check-r72-routed-r73.py`; copy kept at `receipts/instrument-frozen-HEAD.py` |
| worktree revision observed at 23:12 | `328a6bf60c5237fe4ba857b36d2b4401833a61b933f735ec468139b7531a03fe` | uncommitted `M`; outputs in `receipts/current-328a6bf6/` (bytes not snapshotted — see Limits) |
| worktree revision at report time; committed at `3efb9b24` | `71931c1c225ecda5f8b6529091dc9383542d0c054ae62ff6e0a16f3fbe51496e` | bytes at `receipts/instrument-71931c1c.py`; outputs in `receipts/current-71931c1c/`; `git show HEAD:tools/check-r72-routed-r73.py` now equals it |
| C1 counter, frozen | `542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6` | declared |
| C1 counter, committed at `3efb9b24` | `97f6f5ec83401b02d6c83b48bcad27f0f97c06c9e4ad134cc1cbfb202dbb03d0` | `git show HEAD:tools/count-ul-rows-r73.py` |

During this seat the instruments were uncommitted and moving (`71931c1c` was unrecorded when measured).
By yield the L1 had committed `3efb9b24`, and the record is complete in committed bytes: `SCORECARD.md`
gains a “final instrument digests” table naming declared → intermediate → final for both tools
(`93f034e3 → 328a6bf6 → 71931c1c`; `542f9c29 → 84501ab8 → 97f6f5ec`), and
`.ufo/waves/round-73/after/c2-before-final-instrument.txt` now names `71931c1c` and shows
`ROUTED_STALE=3` rc 1 at `eb105757`, `ROUTED_STALE=3` rc 1 at `a7015d27`, `ROUTED_STALE=0` rc 0 at
`583eea87`. I re-ran all three read-only and reproduce them: `receipts/yield-state.txt`. The only
residue is timeliness — the erratum followed the edits instead of preceding them, which the L1's own
block records as the round's `R73-INSTRUMENT-MIDWAVE` mistake.

Consequence for the claim: `--revision` executes the *worktree* tool bytes, so the before control must be
re-run with the final bytes after they are committed. Measured now:
`python3 tools/check-r72-routed-r73.py --revision eb105757` → `ROUTED_STALE=3 ROUTED_OK=0/3` rc 1 under
`71931c1c` (`receipts/current-71931c1c/revision-eb105757.txt`) and under `93f034e3`
(`receipts/P-base-and-head.txt`); `--revision 8eeadcb9` (the declaration commit) read `ROUTED_STALE=3`
rc 1 at measure time. At yield, `--revision HEAD` (`3efb9b24`) and `--revision 583eea87` both read
`ROUTED_STALE=0 ROUTED_OK=3/3` rc 0 (`receipts/yield-state.txt`).

## 2. Selftest and base control (required step 1)

```
$ TMPDIR=$S python3 <frozen 93f034e3> --selftest
SELFTEST: PASS (5 cases, 5 passed, 0 failed)                       rc=0
$ TMPDIR=$S python3 tools/check-r72-routed-r73.py --selftest       # 71931c1c
SELFTEST: PASS (11 cases, 11 passed, 0 failed)                     rc=0
$ python3 tools/check-r72-routed-r73.py --revision eb105757…      # 71931c1c
LESSON-STALE path=corpus/lessons/round-72.md reason=no-block
DIGEST-STALE path=SCORECARD.md reason=block-tokens
CAPABILITY-STALE path=SCORECARD.md reason=block-incomplete
ROUTED_STALE=3 ROUTED_OK=0/3                                        rc=1
```

Receipts: `receipts/frozen-93f034e3/selftest.txt`, `receipts/current-71931c1c/selftest.txt`,
`receipts/current-71931c1c/revision-eb105757.txt`, `receipts/P-base-and-head.txt`.

## 3. Fixture recipe (required step 2)

**The fixture must be built from committed base blobs, not from the worktree.** Measured: with the
worktree as `--root`, both instruments already print `ROUTED_STALE=0 ROUTED_OK=3/3`
(`receipts/N1-live-worktree-drafts.txt`, `receipts/N2-frozen-worktree-drafts.txt`) because the L1's
uncommitted repairs are in the worktree — a worktree-copy control is vacuous.

```
S=/fast/scratch/hyaku/tsukuroi-r73/E2Routed            # deleted before yield
mkdir -p "$S/fixture/corpus/lessons" "$S/fixture/.ufo/waves/round-72/after"
git -C <lane> show eb105757:SCORECARD.md > "$S/fixture/SCORECARD.md"
git -C <lane> show eb105757:corpus/lessons/round-72.md > "$S/fixture/corpus/lessons/round-72.md"
git -C <lane> show eb105757:.ufo/waves/round-72/after/selftest-selftest-after.txt \
  > "$S/fixture/.ufo/waves/round-72/after/selftest-selftest-after.txt"
cat drafts/01-scorecard-erratum.md drafts/02-scorecard-capability-refresh.md >> "$S/fixture/SCORECARD.md"
cat drafts/00-lesson-correction.md >> "$S/fixture/corpus/lessons/round-72.md"
python3 tools/check-r72-routed-r73.py --root "$S/fixture"
```

Scored (required step 2):

```
ROUTED_ITEM LESSON ok
ROUTED_ITEM DIGEST ok
ROUTED_ITEM CAPABILITY ok
ROUTED_STALE=0 ROUTED_OK=3/3        rc=0      # both 93f034e3 and 71931c1c
```

Receipts: `receipts/frozen-93f034e3/P0-control.txt`, `receipts/current-71931c1c/P0-control.txt`.
The base state without drafts is `ROUTED_STALE=3` rc 1 under both instruments
(`…/P0b-base-without-drafts.txt`), so the control has a real before.

**Committed-bytes mode** (the mode the C2 claim uses; instrument `71931c1c`, fixture repo built from
base blobs, `git init -q`, toplevel asserted, `GIT_*` author vars only):

```
$ python3 $S/gfinal2/tools/check-r72-routed-r73.py --revision HEAD   # base commit
ROUTED_STALE=3 ROUTED_OK=0/3        rc=1
$ … --revision HEAD                                                 # drafts written, NOT committed
ROUTED_STALE=3 ROUTED_OK=0/3        rc=1
$ … --revision HEAD                                                 # drafts committed
ROUTED_ITEM LESSON ok
ROUTED_ITEM DIGEST ok
ROUTED_ITEM CAPABILITY ok
ROUTED_STALE=0 ROUTED_OK=3/3        rc=0
```

Receipts: `receipts/G-G1-base-71931c1c.txt`, `G-G2-drafts-uncommitted-71931c1c.txt`,
`G-G3-drafts-committed-71931c1c.txt`, `G-git-mode-71931c1c.txt`. The same three-point control against
`93f034e3` is `receipts/G1-git-base-committed.txt` … `G-git-mode-commands.txt`.

## 4. Drafts, verbatim (the L1 adopts these)

sha256 `fe040cda9bee9e80b39ed9bc9c8610b665202237487ed43d55896005010ee545`
(`drafts/00-lesson-correction.md`, append to `corpus/lessons/round-72.md`):

```markdown
## Correction (round 73, append-only) — R72-LESSON-SUPERSEDED-CLAIMS

R72-LESSON-SUPERSEDED-CLAIMS. Two sentences filed in this round-72 lesson are superseded, and both stay
visible as filed:

- "No capability row enters this round" (Trend verdicts, expansion bullet) is superseded: round 72
  landed the `gate-selftest` capability row in `SCORECARD.md`'s capability table, so a capability row
  did enter.
- "nine hermetic cases" (Trend verdicts, quality bullet) is superseded: the landed `gate-selftest` suite runs ten cases
  (10 cases) — `SELFTEST: PASS (10 cases, 10 passed, 0 failed)`, rc 0 — recorded in
  `.ufo/waves/round-72/after/selftest-selftest-after.txt`.

Counted by `python3 tools/check-r72-routed-r73.py --revision <REV>` (item LESSON).
```

sha256 `a3eafde37505306452936cd8efa0292666c4a1a8a181147e02bbe419cf117931`
(`drafts/01-scorecard-erratum.md`, append to `SCORECARD.md`):

```markdown
## Round 72 — instrument digest erratum (appended round 73; R72-C3-INSTRUMENT-DIGEST-DRIFT)

R72-C3-INSTRUMENT-DIGEST-DRIFT. The round-72 declaration (`SCORECARD.md:5616`, commit `6b42676`) froze
`tools/check-r71-routed-r72.py` at sha256
`df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712`, and that is the tool's actual blob
at the declaration commit. The tool's committed bytes then moved
`df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712` →
`2610ff433bf5d4e945ce5b2da0cf168745e4142ecffabc3d160afee33005cdcc` (landed by the round-72 repair
commit `53bcddef`, unchanged at the round-73 base `eb105757`), after an intermediate `b17fddfa…` state
committed at `123e1c57`.

The repairs the round-72 close landed in that checker: the receipt must now carry the record revision
token `2b358d2d`; the `## Round 71 — receipt erratum` block is matched from a line start, so prose that
quotes the heading no longer satisfies it; and the round-71 note correction is checked against the five
`/usr/lib/modprobe.d` filenames (`README`, `bluetooth-usb.conf`, `gsr-nvidia.conf`, `nvidia-utils.conf`,
`systemd.conf`) instead of a prose token list.

Same-instrument evidence: `python3 tools/check-r71-routed-r72.py --revision a7015d27` reads
`ROUTED_STALE=3` rc 1 (pre-repair data) and `--revision eb105757` reads `ROUTED_STALE=0` rc 0
(post-repair data) with the same tool bytes `2610ff43…` on both sides, recorded at
`.ufo/waves/round-73/after/r72-c3-same-instrument-before.txt`. The same-instrument selftest receipt for
the capability chain — its header records a run on the committed tool with the ten-case v2 patch — is
`.ufo/waves/round-72/after/selftest-selftest-after.txt`
(`SELFTEST: PASS (10 cases, 10 passed, 0 failed)`, rc 0).

Counted by `python3 tools/check-r72-routed-r73.py --revision <REV>` (item DIGEST).
```

sha256 `db2354d68f61c5a9f0fb1ed4bc46995b0d35ebbf109b9b4f098cb9d3a5e465a6`
(`drafts/02-scorecard-capability-refresh.md`, append to `SCORECARD.md` after the erratum):

```markdown
## Capability refresh (round 73, append-only) — gate-selftest is ten cases

The `gate-selftest` capability row above (round 72) still says "nine named cases" and `PASS 9/9`. The
landed instrument prints ten cases — `SELFTEST: PASS (10 cases, 10 passed, 0 failed)`, rc 0, receipt
`.ufo/waves/round-72/after/selftest-selftest-after.txt` — with named ids SELFTEST-MATCH,
SELFTEST-MISMATCH, SELFTEST-LABEL, SELFTEST-SUPERSEDED, SELFTEST-OUT-OF-SCOPE, SELFTEST-NO-RECEIPT,
SELFTEST-GREEN-DIFF, SELFTEST-MIXED, SELFTEST-HERMETIC and SELFTEST-CASES; the tenth is the case-count
guard that fails when a declared case row is deleted. The row text stays as filed; read it with this
block as its current count.

Counted by `python3 tools/check-r72-routed-r73.py --revision <REV>` (item CAPABILITY).
```

## 5. Probe table (required step 3 + adversarial)

“F” = frozen `93f034e3`; “C” = report-time `71931c1c`; “F/C” = same result. Full outputs under
`receipts/frozen-93f034e3/` and `receipts/current-71931c1c/`.

| probe | mutation | F rc | C rc | finding line | verdict |
|---|---|---|---|---|---|
| P1 | remove the digest line (line carrying `2610ff43…`) | 1 | 1 | `DIGEST-STALE … reason=block-incomplete missing_tokens=1` (F) / `reason=block-tokens` (C) | **held** |
| P2 | rename the erratum heading so the block becomes prose | 1 | 1 | `DIGEST-STALE … reason=block-incomplete missing_tokens=0` (F) / `block-tokens` (C) | **held** |
| P3 | put every erratum token in prose under `## Note (unrelated)` | 1 | 1 | F: `DIGEST-STALE … reason=block-incomplete missing_tokens=0`; C: `reason=block-tokens` | **held** |
| P4a | replace the body with “no repair was needed” | 1 | 1 | `DIGEST-STALE … missing_tokens=1` (F) / `block-tokens` (C) | **held** |
| P4b | *append* “no repair was needed; the digest did not drift” to the valid block | 0 | 0 | `ROUTED_STALE=0 ROUTED_OK=3/3` | **survived** (F2) |
| P5 | change the word `ten` → `nine`, keep `(10 cases…)` | 1 | 0 | F: `CAPABILITY-STALE`; C: `ROUTED_STALE=0` | survived in C (F6) |
| P5b | consistent nine-claim (word and numeral) | 1 | 1 | F: `CAPABILITY-STALE … reason=block-incomplete missing_tokens=0`; C: `reason=block-need-any` | **held** |
| P6 | quote truncated digests (`df8a59c7…`, `2610ff43…`) | 1 | 1 | `DIGEST-STALE … missing_tokens=1` (F) / `block-tokens` (C) | **held** |
| P7 | capability block with `10 cases` and no word `ten` | 1 | 0 | F: `CAPABILITY-STALE`; C: ok | F false negative fixed in C |
| P8 | lesson block with `10 cases` and no word `ten` | 1 | 0 | F: `LESSON-STALE`; C: ok | F false negative fixed in C |
| A1 | heading carries all lesson tokens, body says “nothing above is true; nothing is superseded” | 0 | 0 | `ROUTED_STALE=0` | **survived** (F2) |
| A2 | digest direction inverted (TIP labelled as the declaration value) | 0 | 1 | F: `ROUTED_STALE=0`; C: `DIGEST-STALE … reason=block-tokens` (misattributed, F7; decisive `block-digest-direction`) | F survived, C **held** |
| A3 | word `ten`→`nine` plus the word `content` in place of `ten` | 0 | 0 | `ROUTED_STALE=0` | survived; in C only via the retained `(10 cases…)` (F6) |
| A4 | bare `## Correction (placeholder)` + `TODO` early, tokens under a later `###` section | 0 | 0 | `ROUTED_STALE=0` | **survived** (F3) |
| A5 | content-free token dump in a `## Correction` block | 0 | 1 | F: `ROUTED_STALE=0`; C: `LESSON-STALE … block-no-supersede-verb` | F survived, C **held** |
| A6 | empty root | 1 | 1 | `…-STALE absent path=…` ×3 | rc 1 (F1: contradicts F's docstring; correct in C) |
| A7 | `--revision 000000…` | 1 | 1 | absent ×3 | rc 1 (F1: contradicts F's docstring; correct in C) |
| A8 | SCORECARD present, lesson absent | 1 | 1 | `LESSON-STALE absent`, others stale | rc 1 (F1: contradicts F's docstring; correct in C) |
| B1 | receipt path suffixed `-DOES-NOT-EXIST` | 0 | 1 | F: `ROUTED_STALE=0`; C: `CAPABILITY-STALE … block-tokens` | F survived, C **held** |
| B2 | heading “## No erratum was needed and no repair landed” | 0 | 0 | `ROUTED_STALE=0` | **survived** (F2) |
| B3 | “nine names, not ten names” | 0 | 0 | `ROUTED_STALE=0` | **survived** (F2) |
| B4 | lesson block denies both supersessions and calls `10 cases` false | 0 | 0 | `ROUTED_STALE=0` | **survived** (F2) |
| C1 | receipt replaced by `SELFTEST: FAIL (10 cases, 0 passed, 10 failed)` | 0 | 0 | `ROUTED_STALE=0` | **survived** (F5) |
| C2 | receipt cited by absolute path `/home/…/.ufo/…` | 0 | 1 | `CAPABILITY-STALE … reason=block-tokens` | C false negative (F4) |
| C3 | denial sentence *plus* the real direction sentence | 0 | 0 | `ROUTED_STALE=0` | **survived** (F2) |
| C4 | token dump plus the filler word “recorded” | 0 | 0 | `ROUTED_STALE=0` | **survived** (F2) |

Required five: P1, P2, P3, P4a hold with rc 1 and named findings. The requirement's fifth form —
“claim the old repair was a denial” — splits: replacing the content (P4a) is caught; appending the denial
(P4b) is **not**. That is the one required probe that does not hold, and it is the instrument's known
lexical limit (the L1's own SCORECARD block records the same limit).

## 6. Instrument defects (commands + observed output)

**F1 — the frozen instrument's documented exit 2 was unreachable (fixed in C).** Frozen `93f034e3`
docstring lines 10-11: “2 cannot evaluate (a required file is absent, or no readable input)”; its only
`return 2` was the selftest `TMPDIR` guard, and `check_item` returned `False` for an absent file, so
`evaluate` yielded 1. Observed: A6/A7/A8 above, all rc 1. The report-time bytes `71931c1c` document the
behaviour correctly (“an absent data file is a stale finding, not a cannot-evaluate; 2 cannot evaluate
under `--selftest` only”), so only the frozen bytes carried the defect. A harness pinned to `93f034e3`
that distinguishes “cannot evaluate” from “stale” would misread.

**F2 — negation-blind (survives the hardening).** P4b, A1, B2, B3, B4, C3, C4 read
`ROUTED_STALE=0 ROUTED_OK=3/3` while denying the repair or contradicting the block. The supersede-verb
check is satisfied by the *negated* verb (“nothing is superseded”) and by filler words (“recorded”).
Consequence: `ROUTED_STALE=0` proves the tokens are present, not that the repair is asserted.

**F3 — cross-heading swallow (the unanchored-block class the instrument claims to close).** A4:
`## Correction (placeholder)` + `TODO` early in `SCORECARD.md`, with the erratum tokens under a later
`### later section`, still reads `ROUTED_STALE=0`. `blocks()` splits only at `## `, so any earlier `## Correction`
heading makes the rest of the file its body; tokens 600 lines later satisfy “an appended block”.

**F4 — absolute receipt path rejected (hardened bytes only).** C2 output above:
`CAPABILITY-STALE path=SCORECARD.md reason=block-tokens`. `has_token`'s path branch uses
`(?<![A-Za-z0-9_./-])` before the token, so `/home/…/.ufo/waves/…` fails because the preceding byte is
`/`. The assignment names the receipt by absolute path; the relative path must be used. This is a false
negative against a correct citation.

**F5 — a failing receipt satisfies the receipt gate (hardened bytes only).** C1:
`receipt_cases` reads only `(\d+) cases` from the last `SELFTEST:` line and ignores `PASS|FAIL` and the
passed/failed counts, so `SELFTEST: FAIL (10 cases, 0 passed, 10 failed)` yields `ROUTED_STALE=0`. The predicate
says the receipt reports at least ten cases; a failing run should not ground the capability refresh.

**F6 — contradictory block accepted (hardened bytes only).** P5/A3 keep `(10 cases…)` while saying
“nine cases” and read `ROUTED_STALE=0`; the consistent nine-claim (P5b) is rejected. Low severity; the block still
carries a ten-case claim.

**F7 — the stale diagnostic names the wrong block's reason (hardened bytes only).** `check_item`
accumulates `reasons` across every heading-matching block and prints `reasons[0]`, so an earlier
unrelated `## … erratum` block that fails on tokens masks the decisive failure of the intended block.
Measured on A2: all four required tokens are present in the block (verified: id, both digests and the
filename all `in` the constructed text), the decisive failure is `block-digest-direction`, yet the line
printed is `DIGEST-STALE path=SCORECARD.md reason=block-tokens`. The base `SCORECARD.md` carries three
earlier matching headings (`:5649` “Round 71 — receipt erratum”, `:5660` “Round 72 — declaration
erratum”, `:5675` “Round 72 — wave erratum”), which is why the first reason wins. The pass/fail verdict
is correct; the operator guidance is not.

## 7. Facts I grounded independently

- **Both superseded sentences** are in `corpus/lessons/round-72.md` at the base, and both are in
  `## Trend verdicts` (expansion and quality bullets), not in a “C2 section”:
  `git show eb105757:corpus/lessons/round-72.md | grep -n "No capability row enters this round\|nine
  hermetic cases"` → lines 160 and 164.
- **The frozen r71 digest is real, not phantom** — falsifying the earlier L1 draft sentence “the frozen
  string matches no committed blob”:
  `git show 6b42676:tools/check-r71-routed-r72.py | sha256sum` →
  `df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712`. Per-commit digests:
  `6b42676 df8a59c7…`, `123e1c57 b17fddfa…`, `53bcddef`/`7fb35c74`/`eb105757 2610ff43…`; the tool is
  absent at `a7015d27` (`git cat-file -e` → rc 128). Receipt: `receipts/F1-frozen-digest-provenance.txt`.
  The worktree text has since corrected this sentence; the committed text must keep the correction.
- **The three r71 repairs** (diff `6b42676..53bcddef`): receipt record-revision token `2b358d2d`;
  `^## Round 71 — receipt erratum` line-anchored; five `/usr/lib/modprobe.d` filenames checked. Host
  listing confirms exactly those five names (`ls /usr/lib/modprobe.d` → `README`, `bluetooth-usb.conf`,
  `gsr-nvidia.conf`, `nvidia-utils.conf`, `systemd.conf`).
- **Receipt state**: 14 lines, ten `PASS (SELFTEST-…)` case lines, `SELFTEST: PASS (10 cases, 10 passed,
  0 failed)`, `rc=0`; `grep -c "SELFTEST: PASS"` → 1. Capability row `SCORECARD.md:5754` still says
  “nine named cases” / `PASS 9/9` — stale, so the refresh is real work.
- **Guard claim**: deleting the `MIXED` case tuple from a scratch copy of
  `tools/check-selftest-tally.py` (sha256 `f22eb94f1ed86157d94875d0943b5ec62fba8214dd520e7eb4d645969b283464`,
  lane file untouched) yields `FAIL (SELFTEST-CASES)` and `SELFTEST: FAIL (9 cases, 8 passed, 1 failed)`
  rc 1 → `receipts/F2-selftest-cases-guard-mutant.txt`.
- **Same-instrument pair** re-run read-only: `--revision a7015d27` → `ROUTED_STALE=3` rc 1;
  `--revision eb105757` → `ROUTED_STALE=0` rc 0; tool bytes `2610ff43…` on both sides →
  `receipts/P-same-instrument-r71.txt`.

## 8. The sentence I could not ground

One, and it is in my erratum draft: **“its header records a run on the committed tool with the
ten-case v2 patch”**. The receipt's header says exactly that (`# C2 after: --selftest on the committed
tool (E2GateSelftest v2 patch adopted: 10 cases, SELFTEST-CASES guard)`), and the current
`tools/check-selftest-tally.py` is `f22eb94f…` with ten cases — but the receipt records no tool digest,
so I cannot prove the receipt was produced by those exact bytes. I therefore wrote the sentence as a
*header record*, not as a byte-bound claim; any draft that puts “tool sha256 `f22eb94f…`” beside the
receipt (the L1's working copy does) is asserting an attribution the receipt does not carry.

Everything else in the three drafts is measured: the declaration line (`SCORECARD.md:5616`), the frozen
digest's blob, the commit that landed the new bytes, the absent-at-base fact, the repair list, the
ten-case receipt, the ten named ids, the guard's behaviour, and the capability row's stale text.

## 9. Limits and risks

- The target instrument is now committed at `71931c1c` (HEAD `3efb9b24`) with the recorded history
  `93f034e3 → 328a6bf6 → 71931c1c`; my drafts pass all three, but a further edit re-opens scoring: re-run
  the recipe in §3 and re-record the digest.
- `328a6bf6` bytes were measured but not snapshotted; its outputs are in `receipts/current-328a6bf6/`.
  `93f034e3` and `71931c1c` bytes are kept for audit.
- The C1 counter's worktree bytes (`97f6f5ec`) differ from its frozen digest (`542f9c29`); that is outside
  my item and is reported as a cross-claim observation, not a claim.
- The hardened checker requires the receipt to exist at the same revision and rejects absolute paths and
  truncated digests. If the L1 pastes paths from the assignment text (absolute) or ellipsised digests
  from the declaration row, the item reads stale.
- No tool installs, no lane mutations, no commits: this seat wrote only
  `.ufo/waves/round-73/w1/E2Routed*` and its scratch (deleted before yield).

## 10. Receipts index

```
receipts/instrument-frozen-HEAD.py        the declared 93f034e3 bytes (from git HEAD at measure time)
receipts/instrument-71931c1c.py           the report-time 71931c1c bytes
receipts/frozen-93f034e3/                 selftest + 28 probe outputs
receipts/current-71931c1c/                selftest, two revision controls, 28 probe outputs
receipts/current-328a6bf6/                the same probe suite on the earlier hardened revision (28)
receipts/G-G1-base-71931c1c.txt … G-G3-drafts-committed-71931c1c.txt,
receipts/G-git-mode-71931c1c.txt          committed-bytes three-point control (current instrument)
receipts/G1-git-base-committed.txt … G-git-mode-commands.txt   the same for the frozen instrument
receipts/G-git-mode-current.txt           the same for 328a6bf6
receipts/F1-frozen-digest-provenance.txt  per-commit r71-checker digests, absent-at-base
receipts/F2-selftest-cases-guard-mutant.txt the SELFTEST-CASES guard mutant run
receipts/P-same-instrument-r71.txt        same-instrument pair re-run
receipts/P-selftest.txt, P-base-and-head.txt   frozen-instrument selftest and base/HEAD control
receipts/N1-live-worktree-drafts.txt      --root LANE with the L1's uncommitted drafts (ROUTED_STALE=0; vacuous)
receipts/N2-frozen-worktree-drafts.txt    same, frozen instrument
receipts/N3-commit-order-and-after-receipts.txt  commit order, r73 after receipts
receipts/dual-summary.txt                 frozen-vs-328a6bf6 side-by-side
drafts/*.md                               the three blocks, verbatim
```
