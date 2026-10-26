VERDICT: falsifies

# C2-10 — the cheapest mechanical writer produces a PASSING C2 entry, 8/8, exit 0

Item asked: the cheapest script that produces a passing entry **without reading the source semantics**; does it pass, which
conjunct stops it, and how does it compare with the pre-data scripted-writer control C2-K5.

Result: it passes. `rules_verified 8, source_ok 1, counts_ok 2, novelty_base_hits 0, duplicate_rows 0,
duplicate_headings 0` -> PASS exit 0 with the frozen counter `d4a2bb94…bb7d9d`. **No conjunct stops it.** The pre-data
control K5 was killed by exactly one conjunct, and dropping that one trick is enough to pass.

## 1. The writer

Receipt: `.ufo/waves/round-40/w1/C2CritControl/writer.py` (111 lines, sha256 `9776bdeaaed25b2d97b56256e3cb575f1bca5cb9c99eba7786942703900bafb4`).
It is built only from the counter's own parser and answer key, plus the registry's metadata columns:

- cell order from `ROW_RE` and the `cells[1..4]` unpack, `tools/check-exec-environment-r40.py:98,274,278`;
- `TOKENS` (`:85`) joined in frozen order as the rule cell — the script never learns what a token means;
- `derive_values` (`:145`) and `host_values` (`:183`) are imported and their return values printed back verbatim, so
  the `value` cell and the two `counts_ok` cells need no source reading at all;
- the quote is the **first line of the required file with 4-25 collapsed words** (skipping `|`, curly quotes and `S\d{3,}`),
  cited as `file:N-N`; the padding is the literal word list `alpha bravo … mike`;
- registry rows: variant A reuses the lane's `S220-S223`; variant B fabricates `S226-S229` from `ARTIFACT` (`:79`) with
  `scope|anchor|teaches = auto`.

Commands (scratch under `/fast/scratch/hyaku/tsukuroi-r40/C2CritControl/`, clone of lane `f951f28`, origin removed,
`rev-parse --show-toplevel` checked, fixture identity `fixture@shokunin.local`; scratch removed after receipts were copied):

```
git clone -q --shared <lane> "$D" && git -C "$D" remote remove origin
python3 writer.py "$D" reuse        # variant A, commit cc9c336b…, PASS exit 0
python3 writer.py "$D" fabricate    # variant B (fresh clone), commit 23f0ae0d…, PASS exit 0
python3 "$D/tools/check-exec-environment-r40.py" --repo "$D" --revision <sha>
```

Variant A JSON: `.ufo/waves/round-40/w1/C2CritControl/reuse.json`; variant B: `fabricate.json`. The author's real entry
re-scored independently with the frozen counter on the lane: PASS 8/8 (`author.json`), so the counter is not broken — it
simply does not discriminate.

## 2. What passed (verbatim, receipt `entry-reuse.md`)

```
| EX1 | working directory chroot `/` alpha bravo charlie delta echo foxtrot golf hotel | / | S221 util.c:4-4 “*  Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | mechanical host cell |
| EX4 | /usr/bin/bash /bin/sh -c alpha bravo charlie delta echo foxtrot golf hotel india | /usr/bin/bash | S220 PKGBUILD:1-1 “# Maintainer: Levente Polyak <anthraxx[at]archlinux[dot]org>” | /usr/bin/bash libalpm.so.16.0.1 |
| EX7 | Depends running AbortOnFail satisfy dependencies alpha bravo charlie delta echo foxtrot golf | could not satisfy dependencies | S223 hook.c:4-4 “*  Copyright (c) 2015-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | mechanical host cell |
```

Every rule cell is a token list plus the same seven filler words; every quote is a **copyright/maintainer header**
(`util.c`/`trans.c`/`hook.c` line 4, `PKGBUILD` line 1), chosen by line number only, with no relation to the row. Six of
eight host cells are the literal string `mechanical host cell`. This is the strongest available counterexample: it is not
a near-miss, it is a word-salad that the counter certifies as 8/8.

## 3. Why each conjunct is blind to it

| Conjunct (`tools/check-exec-environment-r40.py`) | Why the writer satisfies it |
|---|---|
| value equals derived (`:280-281`) | imports `derive_values` — same call as the counter |
| tokens present (`:282-286`) | pastes `TOKENS[ex]` |
| no negation word (`:287-289`) | filler vocabulary carries none |
| >= 12 words, quote not copied (`:291-292,318-319`) | padded past 12; the quote is a different line |
| upstream row fields (`:294-304`) | `ARTIFACT` strings are echoed into a row title; variant A reuses real rows |
| quote found in cited lines (`:306-317`) | the writer **chooses** the cited range and picks the line from it |
| `counts_ok` (`:322-326`) | prints `host_values` back (`14 of 69 effective hook files`, `/usr/bin/bash libalpm.so.16.0.1`) |
| novelty (`:35-36,212,231`) | `git grep` at `BASE` only; the entry content at REV is never tested |

The two clauses in the docstring that claim more than this are `:4` "each rule READ (QUALITY 87)" and `:12-13`
"a writer cannot pass it with any value the source does not produce" — the second is true only of the *value* cell; the
first is contradicted by the run above.

## 4. Comparison with C2-K5 (pre-data scripted writer)

`controls.jsonl:7`: `rules_verified 0`, and every row's only reason is `rule cell contains its own quote` (EX7 also
`rule carries negation word 'not'`, from the quoted text). K5's script prefixed the quote into the rule cell; the
counter's paraphrase clause caught exactly that. Deleting the prefix and padding with unrelated words — a one-line change
— turns 0/8 into 8/8. So the pre-data control measured the counter's weakest and most avoidable clause, and the
declaration's reading of it ("scripted writer … 0/8 FAIL", `SCORECARD.md:2310`) overstates the protection.

## 5. Optional hardening, measured (not required for the verdict)

**Vocabulary floor** — after removing the frozen token words and the derived value, require >= 5 rule words that occur in
the required file. Run with a patched copy of the counter (`check-exec-environment-r40-patched.py`, receipt):

- author entry `f951f28`: PASS 8/8 (`patched-author.json`);
- variant A (token list + filler): FAIL 0/8, reason `rule lacks 5 non-token words from <file>` (`patched-mech.json`);
- **adaptive variant C** (same writer, padding taken from the quote line itself: `Copyright 2006-2025 Pacman Development
  Team …`): PASS 8/8 (`patched-adaptive.json`, entry `entry-adaptive.md`).

So the floor is a cost bump, not a read check: any lexical condition derived from the same frozen file can be satisfied by
copying words out of it. The same holds for a second candidate: requiring the cited registry row's `anchor` range to cover
the entry's `file:A-B` window keeps the author PASS on all 12 cited references (`check_anchor.py`, receipt, rerunnable
against the lane; e.g. EX1 `util.c:677-687` inside `S221` 610-760) and kills variant B (`anchor = auto`), but a writer can
copy the range into the anchor cell.

## 6. Smallest safe correction

The demonstrated hole is not closable by another lexical conjunct, because the counter publishes its answer key
(`TOKENS`, `derive_values`, `host_values`, `ARTIFACT`) and every lexical condition is derivable from the frozen file. The
smallest correction that is actually sound is to stop claiming the counter establishes a read. Exact proposed text:

(a) Counter docstring, replace line 4 and add one paragraph after the bullet list:

```
7.1.0.r9.g54d9411-3), EX1-EX8, each rule carrying the row's derived value, its frozen proposition tokens, no negation
word and a paraphrase of at least 12 words, quoted from a pinned source at the cited lines,
```
```
These are shape gates, not a read check: a scripted writer that pastes TOKENS, imports derive_values and quotes the
first 4-25 word line of each cited file passes this counter 8/8 (round-40 seat C2CritControl, receipts
.ufo/waves/round-40/w1/C2CritControl/). "Rule READ" is a reviewer judgment under the C2 kill rule, not a property this
counter establishes.
```

(b) `SCORECARD.md:2304`, C2 counter cell, replace

```
reads the RULE cell (source-derived value, frozen proposition tokens, negation words, paraphrase) — QUALITY 87
```

with

```
reads the RULE cell lexically (source-derived value, frozen proposition tokens, negation words, paraphrase of >= 12
words) — a shape gate, not a read check: a mechanical token-list writer passes it (seat C2CritControl); the QUALITY 87
read stays with the wave reviewer under the kill rule
```

(c) If a floor is wanted anyway, the measured one is the vocabulary conjunct in `check-exec-environment-r40-patched.py`
(after the `if copied:` block at `tools/check-exec-environment-r40.py:319`), declared as a cost floor with the adaptive
variant C as its recorded bypass.

## 7. Impacted axes

- **depth (C2)**: the counter proves presence and provenance shape, not depth of the rule text; the round's anti-gaming
  claim (`SCORECARD.md:2304`, `tools/check-exec-environment-r40.py:4,12-13`) is overstated by 8/8 on a word-salad.
- **verification integrity**: the pre-data control set treats the scripted writer as killed (`SCORECARD.md:2310`); the
  counterexample is one line away from that control, so the control set over-certifies the counter.
- Not impacted: the author's entry itself is genuine and independently passes (`author.json`); no value, token, quote or
  registry row in the lane is wrong. The defect is in what the counter is claimed to establish.

## 8. Evidence index and limits

- Counter: `tools/check-exec-environment-r40.py` sha256 `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d`
  (verified on the clone before running), lines cited above; declaration `SCORECARD.md:2303-2304,2310`; control
  `controls.jsonl:7`.
- Lane tip at dispatch `f951f288483c1af0cef4afd458488b84cf7a2165` (entry and `S219-S225` present, `git show HEAD:…`).
- Receipts in `.ufo/waves/round-40/w1/C2CritControl/`: `writer.py`, `entry-reuse.md`, `entry-adaptive.md`,
  `mechanical-vs-authored.diff`, `reuse.json`, `fabricate.json`, `author.json`, `patched-{author,mech,adaptive}.json`,
  `check-exec-environment-r40-patched.py`, `check_anchor.py`, `eval_hardening.py`, `fabricated-registry-rows.txt`.
- Tooling: nothing installed or upgraded. Host untouched (no package/service/sysfs/mount/sudo; no `unshare` needed).
  Lane untouched: no lane file written; all work in `git clone --shared` under `/fast/scratch/hyaku/tsukuroi-r40/C2CritControl/`,
  now removed.
- Not done: no review of the two `counts_ok` host cells beyond replaying `host_values`; no attempt to defeat a
  human reviewer (out of scope); no test of a writer that edits the counter itself (frozen hash prevents it).
