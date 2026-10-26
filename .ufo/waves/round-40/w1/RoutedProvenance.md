VERDICT: defect-found

Item R-3 (round-39 closure §6.5, `corpus/lessons/round-39-verifier-spotcheck.md:190`): confirm or refute that the
`SCORECARD.md:2245` sentence "Receipts under `.ufo/waves/round-39/after/`, each written by `tools/run-receipt.py`
(revision, tool, tool_sha256, tool_revision `6a08925d`)" holds for every file in that directory, and draft the exact
append-only scoping correction.

**Sub-verdicts**

| Question | Result |
|---|---|
| Does every file under `.ufo/waves/round-39/after/` carry a `run-receipt.py` header? | **No — 4 of 9.** The universal "each" is false. |
| Was the sentence false when it was written, or only overtaken later? | **False when written.** It landed in `eeba342e`, when the directory already held 7 files, 3 of them headerless. |
| Are the four counter receipts (the ones the outcome table cites for its numbers) truly bound? | **Yes.** Header present, `tool_revision 6a08925d…`, and each `tool_sha256` equals the tool bytes at `6a08925d`. |
| Does any claim measurement depend on a file whose content names no revision? | **No.** The only revision-less file (`after/selftest-49cc53c.txt`) is not cited in the round-39 outcome section. |
| Do the round-40 claim receipts carry the header (the L1's "all claim receipts" aim)? | **Yes — 4 of 4**, digests equal the freeze-commit bytes. |

## 1. Header census, round-39 `after/` (the item's literal check)

Command, run at lane tip `f951f288483c1af0cef4afd458488b84cf7a2165` (dispatch tip; unchanged since):

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ for f in .ufo/waves/round-39/after/*; do printf '%-45s ' "$(basename "$f")"; head -1 "$f" | grep -o 'tool_sha256' || echo 'NO-HEADER'; done
c1-after-49cc53c.jsonl                        tool_sha256
c1-final-a2d7aad.jsonl                        tool_sha256
c2-after-4078eb2.jsonl                        tool_sha256
c2-final-a2d7aad.jsonl                        tool_sha256
gates-final-a2d7aad.txt                       NO-HEADER
self-assessment-final.json                    NO-HEADER
selftest-49cc53c.txt                          NO-HEADER
selftest-final-a2d7aad.txt                    NO-HEADER
sources-census-final.txt                      NO-HEADER
```

Header authority is `tools/run-receipt.py:13-15` (layout) and `:104-105` (header dict with `revision`,
`tool_revision`, `tool`, `tool_sha256`, `argv`, `started_utc`); the digest is taken from the tool checked out at
`tool_revision` (`:97`). Parsing line 1 of each file as JSON (machine copy at
`.ufo/waves/round-40/w1/RoutedProvenance/binding-audit.json`):

| # | File | Header | `revision` | `tool_revision` | `tool_sha256` | Binding class |
|---|---|---|---|---|---|---|
| 1 | `after/c1-after-49cc53c.jsonl` | yes | `49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82` | `6a08925d…d46a` | `75a9e8ab…f973` | run-receipt.py |
| 2 | `after/c1-final-a2d7aad.jsonl` | yes | `a2d7aad740977088ff9fc70ed36d3ef978b27e81` | `6a08925d…d46a` | `75a9e8ab…f973` | run-receipt.py |
| 3 | `after/c2-after-4078eb2.jsonl` | yes | `4078eb236c7c67f343c76956c587d0a356e0bf5c` | `6a08925d…d46a` | `f1c97836…c991e` | run-receipt.py |
| 4 | `after/c2-final-a2d7aad.jsonl` | yes | `a2d7aad740977088ff9fc70ed36d3ef978b27e81` | `6a08925d…d46a` | `f1c97836…c991e` | run-receipt.py |
| 5 | `after/gates-final-a2d7aad.txt` | no | 8 rows, all `a2d7aad7…` (5 as `"revision"`, 3 as `"branch_tip"`) | — | — | lane-gate capture |
| 6 | `after/self-assessment-final.json` | no | `eeba342ea06ad0069899b3b8b4bbea6af98df610` (line 2; `requested_revision` identical) | — | — | lane-gate capture |
| 7 | `after/selftest-49cc53c.txt` | no | none in content (1 line, `PASS (117 cases, 117 passed, 0 failed)`) | — | — | bare capture |
| 8 | `after/selftest-final-a2d7aad.txt` | no | `a2d7aad740977088ff9fc70ed36d3ef978b27e81` (line 1 prefix) | — | — | bare capture |
| 9 | `after/sources-census-final.txt` | no | `eeba342e…` (line 1 wraps the command and "lane tip") | — | — | fleet-script capture |

`grep -c sha256` in each of the five non-header files → `0` (no file carries a tool digest outside the JSON header).
The four receipts' footers read `receipt_end: 1, exit_code: 0` (parsed; e.g. `after/c1-final-a2d7aad.jsonl` last line).

## 2. Was the sentence false at introduction?

`git log -S'each written by' -- SCORECARD.md` → introduced by `eeba342e` (2026-10-26T03:35:44-03:00,
"round-39: measured outcome, current axes and capabilities, LOG entry, final receipts"). Directory trees:

```
$ git ls-tree --name-only 2e1c2a4 .ufo/waves/round-39/after/   → 3 files (2 with header, selftest-49cc53c.txt without)
$ git ls-tree --name-only eeba342 .ufo/waves/round-39/after/   → 7 files (4 with header; gates-final, selftest-49cc53c, selftest-final without)
$ git ls-tree --name-only a6ca817 .ufo/waves/round-39/after/   → 9 files (adds self-assessment-final.json, sources-census-final.txt)
$ git log --format='%h %s' --name-status -- .ufo/waves/round-39/after/   → only `A` rows; no file was modified after creation
```

So at the commit that wrote "each", three of seven files already lacked the header. The claim was not a statement that
later additions invalidated; it was over-broad when asserted. (The `A`-only history also means the header state I read
today equals the state at each commit.)

## 3. Bound receipts — digest equality re-verified (not a rerun of the counters)

```
$ git show 6a08925daa30767809eb13bb4b01448ff954d46a:tools/score-storage-hidden-r39.py | sha256sum
75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973  -
$ git show 6a08925daa30767809eb13bb4b01448ff954d46a:tools/check-transaction-order-r39.py | sha256sum
f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e  -
$ sha256sum tools/score-storage-hidden-r39.py tools/check-transaction-order-r39.py      # working tree, identical
```

Both declared pins (`SCORECARD.md:2245` parenthetical, the round-39 declaration table) and all four receipt headers
agree with these bytes. The round-39 `w1/RevReceiptBinding.md` audit reached the same values at `2e1c2a40`.

## 4. Round-40 receipts (the L1's "all claim receipts" aim)

Read-only census of both directories at dispatch tip `f951f28`:

| Directory | File | Header | `revision` | `tool_revision` | `tool_sha256` | Footer |
|---|---|---|---|---|---|---|
| `before/` | `c1-before.jsonl` | **yes** | `53b294a2…77ce` | `a447b67b…ae524` | `8b06de18…f0159` | `exit_code: 0` |
| `before/` | `c2-before.jsonl` | **yes** | `53b294a2…77ce` | `a447b67b…ae524` | `d4a2bb94…b7d9d` | `exit_code: 0` |
| `before/` | `sources-census-start.txt` | no (not a claim receipt) | line 1: lane revision `53b294a2…`, `scripts/sources-census.sh sha256 3fb72615…e30`, fleet revision `8b9f360e…`, run stamp; line 2: the command | — | — | — |
| `after/` | `c1-after-c707e35.jsonl` | **yes** | `c707e356…0610` | `a447b67b…ae524` | `8b06de18…f0159` | `exit_code: 0` |
| `after/` | `c2-after-bf23805.jsonl` | **yes** | `bf238050…b86` | `a447b67b…ae524` | `d4a2bb94…b7d9d` | `exit_code: 0` |

Freeze bytes check:

```
$ git show a447b67b2502bae1e96fda341ae5ad32243ae524:tools/score-selftest-literals-r40.py | sha256sum
8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159  -
$ git show a447b67b2502bae1e96fda341ae5ad32243ae524:tools/check-exec-environment-r40.py | sha256sum
d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d  -
```

Answer to the item's second half: **all four round-40 claim receipts carry the header**, and each digest equals the
frozen tool bytes. Two calibration notes: (a) `before/sources-census-start.txt` is a fleet-script capture that
`run-receipt.py` cannot wrap (tool not lane-tracked, `tools/run-receipt.py:93`), and unlike the round-39 version it now
self-binds command, script digest, lane revision, fleet revision and run stamp — the round-39 U1 defect class is
repaired in form; (b) `after/` at dispatch holds only the two counter receipts, so the round-40 outcome sentence is
not yet at risk — but the round-39 pattern shows closure adds gates/selftest/self-assessment/sources-census captures,
which would reproduce the defect. All gate tools are lane-tracked (`git ls-files tools | grep -c 'check-'` → 35), so
`run-receipt.py` can wrap them; only the fleet `scripts/sources-census.sh` cannot.

## 5. Findings

- **F1 (the routed item, confirmed).** `SCORECARD.md:2245` over-quantifies over the directory: 4 of 9 files carry the
  header at the tip, 4 of 7 at the writing commit. Revision is not in doubt; scope is.
- **F2 (filename/content divergence, disclosed).** `after/self-assessment-final.json` and `after/sources-census-final.txt`
  are named `-a2d7aad` but both measure `eeba342e` (self-assessment: `"revision"` and `"requested_revision"`
  `eeba342ea06…`, 27 checked, 0 mismatches, PASS; sources census: "lane tip `eeba342ea06…`"). The `a2d7aad7`
  self-assessment reading is the second row of `gates-final-a2d7aad.txt` (`check-self-assessment rc=1`, 7 mismatches),
  which §6.4 already routes. Not a second claim of mine — recorded so a correction written from filename alone would
  misstate the revision each file measures.
- **F3 (same quantifier one sentence earlier; not routed).** `SCORECARD.md:2215-2216` says "the before receipts were
  written by `tools/run-receipt.py` at the base with `--tool-revision 6a08925d`, so each names the revision, the tool
  and its sha256". `before/` holds 3 files: `c1-before.jsonl`, `c2-before.jsonl` (both headered) and
  `sources-census-start.txt` (no header). Under a directory reading this carries the same defect; under a
  "receipts-for-the-before-measurement" reading it is true. Ambiguous, lower severity — the draft below closes it in
  one clause so the block is self-consistent either way.
- **F4 (forward risk, not a defect at this tip).** If round-40 closure adds bare captures under `after/`, a sentence of
  the round-39 form will be false again. Either wrap the four lane gate tools and `tools/tsukuroi-census.sh --selftest`
  in `tools/run-receipt.py` (both are lane-tracked; `bash … --selftest` is the form round-39 `RevReceiptBinding.md` §6
  proposed), or state the two classes explicitly.

## 6. Exact proposed append-only correction

Insertion point: `SCORECARD.md` after line 2290 (the blank line closing the round-39 capabilities block, which ends
`- **retired:** none.` at `:2289`) and before `## Round 40 — declaration` at `:2291`. Inserting there leaves every
existing line number unchanged, including the `:2245` reference the routed defect names. If the lane prefers strictly
monotone appends, the identical block placed at end of file is equally append-only; only the "at `SCORECARD.md:2245`"
pointer changes meaning, so keep it.

Proposed text, verbatim:

```markdown
### Round-39 receipt-provenance scoping correction (append-only; routed defect §6.5)

The measured-outcome paragraph at `SCORECARD.md:2245` says "Receipts under `.ufo/waves/round-39/after/`, each written
by `tools/run-receipt.py` (revision, tool, tool_sha256, tool_revision `6a08925d`)". The universal quantifier is wrong
and that reading is superseded; no file and no measurement changes. The check is
`for f in .ufo/waves/round-39/after/*; do head -1 "$f" | grep -o tool_sha256 || echo NO-HEADER; done`: 4 hits, 5
`NO-HEADER`, over 9 files. The sentence was already false when written, not merely overtaken: `git ls-tree` at
`eeba342e`, the commit that introduced it, lists 7 files, of which `gates-final-a2d7aad.txt`,
`selftest-49cc53c.txt` and `selftest-final-a2d7aad.txt` had no header.

Scoped correctly, the evidence classes are:

- **Four `tools/run-receipt.py` receipts**, fully bound: `after/c1-after-49cc53c.jsonl`,
  `after/c1-final-a2d7aad.jsonl` (tool `tools/score-storage-hidden-r39.py`, `tool_sha256`
  `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`), `after/c2-after-4078eb2.jsonl`,
  `after/c2-final-a2d7aad.jsonl` (tool `tools/check-transaction-order-r39.py`, `tool_sha256`
  `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`). Each header names the measured `revision`,
  `tool_revision` `6a08925daa30767809eb13bb4b01448ff954d46a`, the tool and its digest, and each footer carries
  `exit_code`; both digests equal the tool bytes at `6a08925d`.
- **Four direct tool-output captures with no tool digest**, each naming the revision it measured in content:
  `after/gates-final-a2d7aad.txt` (8 gate rows, every row naming `a2d7aad740977088ff9fc70ed36d3ef978b27e81`, five as
  `revision` and three as `branch_tip`), `after/self-assessment-final.json` (`"revision"` and `"requested_revision"`
  `eeba342ea06ad0069899b3b8b4bbea6af98df610`, 27 checked, 0 mismatches), `after/selftest-final-a2d7aad.txt` (line 1
  names `a2d7aad7` and `PASS (119 cases, 119 passed, 0 failed)`), and `after/sources-census-final.txt` (line 1 names
  the command and lane tip `eeba342e`).
- **One capture that names no revision in content**: `after/selftest-49cc53c.txt`, a single line
  (`PASS (117 cases, 117 passed, 0 failed)`) whose only revision hint is the 7-hex filename. It is not cited by the
  round-39 outcome section, so no claimed number rests on it.

Two of the file names disagree with the revision their content measures: `self-assessment-final.json` and
`sources-census-final.txt` are named `-a2d7aad` and measure `eeba342e`. The `a2d7aad7` self-assessment reading is the
second row of `gates-final-a2d7aad.txt` (`check-self-assessment rc=1`, 7 mismatches), superseded at `eeba342e` as
§6.4 records.

Read for scope, the sentence at `SCORECARD.md:2215-2216` ("the before receipts were written by
`tools/run-receipt.py` … so each names the revision, the tool and its sha256") is bounded the same way: of the three
files in `before/`, `c1-before.jsonl` and `c2-before.jsonl` are headered bindings to the frozen counters, and
`before/sources-census-start.txt` is a fleet-script capture with no header and no tool digest.

No claim measurement, counter, frozen predicate, kill rule, axis ordinal or capability row changes; the four receipts
the outcome table cites for C1 and C2 are unchanged and remain bound to the frozen tool bytes.
```

## 7. Out of scope / not done

- No counter, census or selftest was re-run (the item is a provenance-wording audit; re-running is not evidence of the
  header question, and the wave forbids decorative reruns). No TO row, C1 mutant or control was judged.
- I did not audit `.ufo/waves/round-39/controls/`, `before/` beyond the three-file header check, the round-40
  `controls/` rows, `candidate-sha256.txt`, or the frozen snapshots — other seats own those.
- I did not verify that `gates-final-a2d7aad.txt` rows are truthful gate outputs beyond their self-named revision, and
  did not restate the §6.4 red-row disclosure.
- No product file, SCORECARD line, lesson, counter or judge was edited; the correction above is a proposal only.

## 8. Tooling and housekeeping

- No tool installed or upgraded; no pacman transaction (host-wide pause respected); no sudo; no host mutation; no
  service touched; no process signalled. Scratch `/fast/scratch/hyaku/tsukuroi-r40/RoutedProvenance/` was created for
  the audit script's `TMPDIR` and removed at finish; nothing was built under `/tmp`.
- Read-only git only (`log`, `ls-tree`, `show`); no `add`/`commit`/`checkout`/`reset`/`stash`/`status`-mutating call,
  no fleet-repo or sibling-lane access, no `shokuknow` access.

## Artifacts

- Report: `.ufo/waves/round-40/w1/RoutedProvenance.md`
- Machine audit (per-file sha256, header fields, footers for the four directories): `.ufo/waves/round-40/w1/RoutedProvenance/binding-audit.json`
- Cited in-lane evidence (read-only): `SCORECARD.md:2215-2216,2243-2245,2289-2291`; `tools/run-receipt.py:13-15,93,97,104-105`;
  `corpus/lessons/round-39-verifier-spotcheck.md:38-41,190`; `corpus/lessons/round-39.md:90`;
  `.ufo/waves/round-39/w1/RevReceiptBinding.md` (prior audit); `.ufo/waves/round-39/after/*` (9 files);
  `.ufo/waves/round-40/{before,after}/*` (5 files).
