# E3Routed — round 72 w1: C3 repair drafts and checker attack

Axes: receipt re-derivation fidelity / draft correctness / checker tamper sensitivity.
Scope: scratch-only fixtures; no lane write, no commit, no git mutation, no install.

## 1. Drafts (bytes ready to land)

| draft | sha256 | shape |
|---|---|---|
| `count-mp-rows-final.txt` | `9032d8782da1961fa5e9de368b3df667deda489d149cb654b9071b231511f2c3` | 12 lines; 2 summary lines, equal to a fresh run at `2b358d2d` |
| `erratum.md` | `896b75b64ced9154fc1a57987597eadfe1a1876755b37cc74fdb47af0e848d7e` | one `## Round 71 — receipt erratum` block naming the receipt and `2b358d2d` |
| `note-correction.md` | `f6e9a5fa7582d3052c6fa21638aef28b0ea1dd974347f559b253c18518372032` | `## Correction` block: defect id, five named `/usr/lib/modprobe.d` paths, superseded `four` |

All three live in `.ufo/waves/round-72/w1/E3Routed/`. The trio, assembled as one fixture, reads
`ROUTED_STALE=0` rc 0 (`ROUTED_RECEIPT ok revision=2b358d2d`, `ROUTED_SCORECARD ok`, `ROUTED_NOTE ok`).

Receipt re-derivation, run from the lane root:
`python3 tools/count-mp-rows-r71.py --revision 2b358d2d` rc 0 ->
`MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0` /
`MP_TARGET rows=6 verified=6 sources>=4 snapshots>=4 max_reuse=2 met=1`. Deterministic across two runs.

## 2. Working-tree state and the one blocking hazard

At `HEAD 6b426762` all three items are missing (`ROUTED_STALE=3` rc 1, as declared). The working tree
now carries the receipt (byte-identical to my draft), a note `## Correction`, and an erratum block —
all uncommitted, so the checker (which reads committed bytes) still reports 3.

**Hazard: the erratum block is appended at EOF and is therefore unreadable.** Checker line 78 is
`re.search(r"## Round 71 — receipt erratum.*?(?=\n## |\Z)", score, re.S)` — no `^` anchor. The Round 72
C3 row already contains that literal heading inline (SCORECARD line 5624), so the first match starts
there and stops at the next line-initial `##`, which is the appended block's own heading. The block's
body is never examined.

- identical block bytes appended at EOF -> `ROUTED_SCORECARD missing`, `ROUTED_STALE=1` rc 1 (with a correct receipt)
- identical block bytes moved above `## Round 72 — declaration` -> `ROUTED_SCORECARD ok`, `ROUTED_STALE=0` rc 0

Required placement: insert the erratum block **before `## Round 72 — declaration`** (e.g. after the
round-71 declaration errata list). Appending at EOF cannot satisfy the frozen checker no matter how
correct the block is. Same constraint applies to any future `## Round 71 — receipt erratum` block.

## 3. Adversarial probes (all recorded in `tamper-probes.txt`)

| probe | checker | verdict |
|---|---|---|
| (i) receipt summary lines correct, revision fabricated (`deadbeef`) | green | **false pass** — receipt revision text is never read (line 31/70 compare two summary lines only) |
| (ii) erratum names receipt in a sentence, no revision | caught (`STALE=1`) | ok |
| (ii-b) block names receipt + revision, no statement | green | literal pass (line 81 is a two-substring test) |
| (iii) correction says five, omits defect id | caught | ok |
| (iii-b) id + "five" + "four" + `/usr/lib/modprobe.d`, no path named | green | **false pass** — the five paths are not checked |
| (iii-c) filed MP5 sentence edited to five *and* a correction appended | green | **false pass** — "quoted, not edited" is unverified |
| (iv) receipt correct, tree under test's real run red (`git clone --shared`, one MP row removed, `MP_ROWS=5 … met=0` rc 1) | green | **false pass** — `counter_summary()` (line 50) always re-derives from the lane at the constant revision and ignores `--fixture` (by its own docstring, but the predicate is then not tested over the tree) |
| (v) no heading at all; receipt path + `2b358d2d` as plain prose later in the Round 72 declaration | green | **false pass** — consequence of the unanchored line-78 regex |

Tally: `FALSE_PASSES=5`, 2 probes caught, 1 false negative (EOF placement).

## 4. Notes for the L1

- Land the receipt (already byte-identical in the working tree) and keep it unedited; the two summary
  lines are the only part the checker compares, but the per-row lines are the evidence a human reads.
- Move the existing erratum block above `## Round 72 — declaration` — do not append. After commit,
  `python3 tools/check-r71-routed-r72.py` should print three `ok` lines and `ROUTED_STALE=0` rc 0.
- The working-tree note correction already satisfies `ROUTED_NOTE`; my `note-correction.md` is an
  alternative only if that text is rewritten.
- Checker defects above are reported, not repaired: `tools/check-r71-routed-r72.py` is frozen
  (sha256 `df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712`, matches the declaration)
  and out of my write scope.

## 5. Cleanup

Scratch `S=/fast/scratch/hyaku/tsukuroi-r72/E3Routed` (mirrors + 433 MB shared clone) removed before
yield. No `/tmp` write, no package install, no service action.
