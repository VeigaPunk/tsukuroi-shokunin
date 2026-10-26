VERDICT: defect-found
(one counter coverage gap: dropping the uncited S-id S218 from the entry's `source:` line survives the
frozen counter; the entry itself was not falsified — 8 of 9 mutants killed, baseline PASS)

# C2-11 — mutation test of the C2 entry against tools/check-transaction-order-r39.py

Entry under test: `corpus/knowledge/pacman-transaction-order-r39.md` at 4078eb236c7c67f343c76956c587d0a356e0bf5c.
Counter: `tools/check-transaction-order-r39.py`, sha256 `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`
(observed via `sha256sum` this session, 2026-10-26) — matches the frozen declaration. Counter logic read at
tools/check-transaction-order-r39.py:67-68 (REQUIRED per-row file), :154-156 (argparse), :177 (dup heads),
:182-184 (source_ok), :189 (dup rows), :201-203 (cited-id-on-source-line check), :204-207 (upstream-row check),
:213-219 (4-25-word quote at cited lines), :223-226 (host counts).

## Method

Per mutant: `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$D"` under
/fast/scratch/hyaku/tsukuroi-r39/C2MutEntry/fx.<tag>; `git remote remove origin`; repo-local fixture identity
`C2MutEntry fixture <c2mutentry@fixture.invalid>`; `git rev-parse --show-toplevel` == clone asserted; variant
committed on master; counter run as `python3 <clone>/tools/check-transaction-order-r39.py --repo <clone>
--revision <mutant sha>`. The item's literal `--scratch` flag is NOT accepted by this counter (argparse defines
only --repo/--revision/--branch, tools/check-transaction-order-r39.py:154-156; passing it gives
`error: unrecognized arguments: --scratch`, exit 2 — receipt baseline-scratch-flag.stderr); TMPDIR was pointed
at the scratch dir instead. Deviation is from the tasking boilerplate, not from any counter promise.

Baseline first (role rule: a baseline failure makes every verdict inconclusive): pristine 4078eb2 in a clone →
`PASS` exit 0, host windows=86 transactions_started=60 scriptlet_tag_outside_commit=252/441
running_inside_commit=0 (receipt baseline.json). All mutants share pristine before-hash
`701a462dfe9c3d03fba0366719e772e081d6cb181e25398d78c0f1ebf5b0d74a` (entry) / `c2e4598670c50a69a5694b616928f7011199ea1be2dcae73b9b7c440540af34e`
(corpus/SOURCES.md), asserted equal to the blob at 4078eb2.

## Kill table

Predicate fields: rules / dupR / dupH / srcOK / cntOK / oracle.

| # | mutant (location) | expected detector | observed (rules dupR dupH srcOK cntOK oracle → result) | verdict |
|---|---|---|---|---|
| M1a | drop S218 from `source:` line (entry:1) — S218 is cited by NO TO row (mentions only entry:1,3) | none should fire: source_ok :182-184 requires only that the ids present are good, never that the declared set is complete | 8 0 0 1 2 0 → PASS exit 0 (mutant 95d3dffefc502ab76ab816c0c628da945cc5c168) | **SURVIVED** |
| M1b | drop S213 from `source:` line (entry:1) — S213 carried by TO3/TO4/TO6 | cited-id check :201-203 | 5 0 0 1 2 0 → FAIL exit 1; reasons `cited S-id not on source: line: S213` ×3 (mutant 530cff8bb3bbea9fbf88524dd0c21b9812d1963a) | KILLED |
| M2 | TO7 file ref remove.c:699-733 → add.c:699-733 (entry:30) | quote check keyed on REQUIRED[TO7]=remove.c :67,:213-219 | 7 0 0 1 2 0 → FAIL; `no 4-25 word quote found in remove.c at the cited lines` (mutant 76b779e4af399648761b245e9f7620cb83b2c7fe) | KILLED |
| M3 | TO4 quote truncated to 3 words (entry:27) | 4-word minimum :217 | 7 0 0 1 2 0 → FAIL; same quote reason for TO4 (mutant 6affd38634257d1602aaee5c7ef8677c7dca3e82) | KILLED |
| M4 | TO4 quote one token changed: `newpkg->version` → `newpkg->versions` (entry:27) | quote-in-body match :217-219 | 7 0 0 1 2 0 → FAIL (mutant ed098dfeff726918e0f51b413af6c2d67514c873) | KILLED |
| M5 | duplicate TO4 row, appended at EOF | duplicate_rows :189 | 8 1 0 1 2 0 → FAIL exit 1 (mutant 150f68e7d41f1706e378a8a161ba40545ad643be) | KILLED |
| M6 | duplicate `## Rules (source-level, pacman 54d9411)` heading (entry:20) | duplicate_headings :176-177 | 8 0 1 1 2 0 → FAIL exit 1 (mutant bc627b63037f54f62059ab0219583fcdf8ad1b2b) | KILLED |
| M7 | TO1 host cell `60 transactions` → `61 transactions` (entry:24) | counts_ok :223-224 (recomputed from frozen capture) | 8 0 0 1 1 0 → FAIL exit 1 (mutant 4cf8b357bca4f86e41ae2235e1cac85aad3f44a2) | KILLED |
| M8 | SOURCES S208 used-by cell drops `corpus/knowledge/pacman-transaction-order-r39.md` (corpus/SOURCES.md:217) | source_ok :182-184 AND upstream :204-207 | 7 0 0 **0** 2 0 → FAIL; also `TO5: no mined upstream row for hook.c at 54d9411 naming the entry` (mutant a21d25e8ecdd1e6758c4ce6ad9116a496d7095c0) | KILLED |

Receipts per mutant: `.json` (full counter record), `.diff` (exact mutation), `.hashes` (before/after sha256 +
mutant commit), plus sweep-summary.json — all in `.ufo/waves/round-39/w1/C2MutEntry/`.

## Round-38 closure status (three routed gaps)

1. **Stripped entry citing only own-work — CLOSED.** A rule verifies only on a `mined` SOURCES row whose title
   contains `54d9411` and `lib/libalpm/<required file>` (:67-68, :204-207); own-work rows cannot carry a rule.
   Author control C2-E1-no-upstream-row scores rules_verified 0 FAIL (.ufo/waves/round-39/controls/controls.jsonl);
   baseline here PASSes only because every TO row (entry:24-31) carries an upstream S-id plus a located quote.
2. **S-id drop — PARTIALLY CLOSED.** Closed for S-ids a row cites (M1b killed; author control C2-E3-sid-dropped
   shows the same rules_verified 5). Open for S-ids no row cites: M1a survives — S218 (the own-work capture row)
   can silently vanish from `source:` (entry:1) and the counter still PASSes. Practical exposure is real, not
   hypothetical: the entry's own recheck policy ages S218 out at 30d (entry:3), so a future cleanup that trims
   the source line is invisible to the counter. This is a counter coverage gap, not an entry defect.
3. **Duplicated block — CLOSED.** Duplicates are counted anywhere in the file: duplicated TO row → duplicate_rows
   (M5, author control C2-E4-block-duplicated dup_rows 8), duplicated `## ` heading → duplicate_headings (M6,
   E4 dup_heads 1); both FAIL the predicate.

## Coverage finding (the defect)

`source_ok` (tools/check-transaction-order-r39.py:182-184) checks that every id present on the `source:` line is
a good SOURCES row — it never checks that the declared set (S208, S213-S218, entry:1) is still fully present.
Proposed tightening for the L1's consideration (NOT applied — leaf, read-only on lane content): source_ok == 1
should additionally require each of S208, S213-S218 to be named on the entry's `source:` line, so a shrinking
source line fails like a dropped citation does. The declared kill rule for TO-row truth (QUALITY 81) is
unaffected by this sweep; the counter checks quote placement, not rule truth, exactly as declared.

## Hygiene and bounds

- Lane untouched: HEAD 394e1ba4fab39a417abe66a7802f87cf1ff8dd61 and `git status --porcelain` identical before and
  after the sweep (observed in-session); no git mutation, no checkout/reset in the lane; all variants lived in
  scratch clones, removed afterward — /fast/scratch/hyaku/tsukuroi-r39/C2MutEntry verified absent post-run.
- No tools installed or upgraded (none needed).
- Not done: judging any TO row's truth against the source (reviewer-seat job); exercising the counter's
  exit-2 tamper arms; any C1 work; any live pacman or host mutation.
