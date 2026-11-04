# K1Critic — round-75 declaration critique (BINDING FILE, final)

Seat: K1Critic (critic, L2, tsukuroi r75 w1). Declaration commit `1e2bb29c`, base `a21302a4`.
Scope: adversarial critique of the frozen declaration — controls, channels, sizing, unfalsifiable
conjuncts. Instruments re-verified from source; every attack below was executed in scratch
(`/fast/scratch/hyaku/tsukuroi-r75/K1Critic/`, deleted before yield; construction recipes in the
appendix). No tools installed; no git/jj mutations; no repo writes outside this file.

## Verdict

The declaration is **freeze-clean and controlled** — both tool digests match the frozen sha256
(`5e87238c…`, `4b5c801c…`), both selftests read 13/13 PASS, and every declared do-nothing control
reproduces exactly (note/cat-file rc 128; counter at base `JT_MAP absent` rc 128; README `JT[0-9]`
grep 0; routed checker at base `ROUTED_STALE=4 ROUTED_OK=0/4` rc 1). But the claims' falsification
power is narrower than their prose:

- **C1 proves plumbing, not truth.** The counter tests vocabulary overlap, quote location and
  registry geometry. A polarity-negated plane (D1) and a false step count (D2) both read
  `met=1 rc 0`.
- **C2's checker is a self-documenting answer key** with a first-occurrence shadowing hazard (D4,
  D5) and a free verb clause (D6). All four items close by token dump (D4).
- **One cheap control is missing**: the C2 positive reachability replay at real base bytes (D7).
- **The depth ordinal is an unfalsifiable conjunct** unless the band rule is frozen (D8).

Net: the round is sized and honest enough to run as filed **if** C1 is re-scoped in prose
(sourcing discipline, not semantic verification) and the D5/D7/D8 corrections land. D1/D2 do not
block the round; they bound what its green counter may be cited for.

## Answers to the six assigned questions

### 1. C1 — independent testability, counter-derivable rows, sizing

**Row not independently testable: JT5 ("ten labelled steps").** It is the only quantitative row,
and the counter has no counting clause — its content tests are token-share and a verbatim quote,
neither of which sees the number. The count is checkable only by reading the step comments in
`transaction.c` — where the eighth step is spelled **"Eights step"** (line 864, upstream typo), so
even the natural `grep -n Eighth` returns rc 1 and a token-level audit undercounts the labels at
nine. Fixture fx3 changed `ten` → `eleven labelled steps`: `JT_ROWS=6 … met=1` rc 0. Secondary:
every row's polarity is untested (D1). Minor content note: the committed draft's JT5 enumeration
lists nine surface items ("matter discovery, impact minimization, redundant dropping, garbage
collection, order verification with cycle repair, job merging, a second collection and redundant
drop, the destructive check and apply") under its own "ten" — the Seventh and Eights steps are
fused into one item. The instrument cannot see this; the note writer should disambiguate.

**Row writable from the counter's own text: the JT2-shaped row (redundancy predicate).** The
counter's own selftest sentence — "The manager merges job types and drops redundant entries before
applying the transaction across dependency edges and ordering constraints." — passes its own
lexical gates verbatim against the real `job.c` snapshot: 12 statement tokens, **6 shared
(= MIN_TOKENS), share 0.50 (= MIN_SHARE)**, both at zero margin. (The JT3-shaped selftest sentence
falls one token short vs `job.h`: 5 shared, 0.38.) No row clears the **quote clause** from counter
text alone — a verbatim 4–25-word span of the real snapshot is required, and the counter embeds no
real snapshot text (round-74 D3 fix confirmed: synthetic fixtures only). But the wave commits the
complete set of quotes: `before/draft-rows-validated.md` carries all six statements, digests and
quotes, and `SOURCES.json` carries all three digests and URLs. fx1 (verbatim draft rows + three
composed registry rows, zero snapshot opens) scores `JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3
JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1` rc 0 — byte-identical to the declared
`before/draft-row-control.txt`. So: counter alone → one row's vocabulary; counter + committed wave
bytes → **all six rows**, without opening any snapshot.

**Sizing: yes, one round — by construction a transcription round.** 6 rows with max-snapshot-reuse
2 and ≥3 sources/snapshots forces exactly the pinned 3 snapshots × 2 rows; there is no slack and no
overreach. With the answer pre-drafted and pre-validated (draft-row-control), the residual work is
the note copy, three registry rows (S314–S316, absent at base **and** at tip — measured) and
receipts. Sized fine; the honest framing is transcription of a pre-validated plane, not discovery.

### 2. C2 — token dumps, the 80-line window, the admitted shadowing shape

**All four items are token-dumpable.** fx5: base bytes + one appended content-free block covering
items 1+2 (`R74-DEATH-RECEIPT-MISSING` and `R74-REPORT-WORDING` lines with the required
substrings), one receipt paragraph quoting both OIDs (both constants are printed in the checker
source), and a restated axes table with **`echo` counting commands and the round-65 scores copied
verbatim** → `ROUTED_STALE=0 ROUTED_OK=4/4` rc 0. Item 4's real work — re-deriving the counts — is
never enforced: commands are not executed, scores are not compared, `| depth | 8 | `echo depth` |`
passes.

**The window binds weakly.** It binds content *forward* within 81 lines (token line + 80), and the
DECOY-DISTANT case proves the >80-line rejection. But `need_all`/`need_any` are case-insensitive
substrings anywhere in the window (order- and proximity-free), and the supersede-verb may be
**pre-existing prose**: the base lesson already contains "corrections sweep", "superseded",
"correction propagation" within any window reaching lines 43–68. fx7: one inserted line carrying
the token + required substrings and **no corrective verb of its own** passes item 1
(`ROUTED_OK=1/4`) on the inherited verb alone.

**The admitted shadowing shape: first-occurrence-wins.** `token_block` returns the *first* line
containing the token, so any innocuous earlier mention of the token name shadows every later,
genuine block. fx6a: genuine correction block appended at EOF → item 1 PASSES (1/4). fx6b: the
same genuine block at EOF **plus one realistic dispatch line near the top** ("routed to round 75:
R74-DEATH-RECEIPT-MISSING … R74-REPORT-WORDING") → item 1 flips to STALE `reason=need`, whole run
0/4. An honest writer who appends a perfect closure below an innocent cross-reference can never
pass without hunting the early mention — and the selftest's DECOY-DISTANT covers only the
self-inflicted >80-line decoy, not this direction. Pass-side twin: dropping the token above
pre-existing prose that already contains the required phrases (parasite window).

### 3. Controls — sufficiency and the missing cheap control

The declared set (note-absent rc 128; counter-at-base rc 128; README grep 0; routed checker at
base rc 1 with all four reasons; registry 313 / notes 92 / lessons 124; S314–S316 absent;
held-ground 0/0; SHA256SUMS 3/3; draft-row-control met=1) is **sufficient for the base** and I
reproduced every line. Missing:

1. **The C2 positive reachability control** — the draft-row-control asymmetry. C1 proves its
   target is *reachable* from repo-like bytes (draft-row-control.txt, which I reproduced
   exactly); C2 proves only that its target is *missed* at base, with reachability left to a
   synthetic selftest fixture (`# Scorecard` toy, not the 6,2xx-line real file). The C2 analog —
   base bytes + the four would-be repair blocks → `ROUTED_OK=4/4` — was never receipted. I ran it
   (fx5): it passes, including on the real SCORECARD's heading/row geometry. Cheap: one fixture,
   one command. Its absence means the round's only untested-in-advance predicate direction is the
   one C2 will be measured by.
2. Cheap add-on: neither `absence-controls.txt` nor the declaration records `--selftest` rc for
   either instrument or re-verifies the two frozen sha256 digests at base (I verified: 13/13 +
   13/13; both digests match). One line each.

### 4. Answer-key channels

- **`check-r74-routed-r75.py` embeds real corpus bytes and is a complete C2 answer key.** The two
  real OIDs (`FABRICATED`, `REAL` constants — genuine receipt bytes), the exact required phrases
  ("no review-accepted drafts", "w1/SC3Index/report.md", "SC3Index", "RESOURCE_EXHAUSTED"/"429"),
  the exact heading, the axis list, and four full `good_*` block templates. A writer can copy the
  selftest fixtures, swap the toy paths for real ones, and pass — fx5 was built from exactly that.
- **`count-jt-rows-r75.py` embeds no real corpus text** (synthetic fixtures only — the round-74 D3
  defect is genuinely fixed), but its selftest paraphrases JT2/JT3 content ("merges job types",
  "drops redundant entries", "try restart onto restart … otherwise onto nop"), and its JT2
  sentence verbatim clears its own gates against the real `job.c` (measured 6/6 tokens, 0.50).
- **Wave-level channel: the complete C1 answer is committed** as `before/draft-rows-validated.md`
  (the reachability control doubles as the key). "No answer key" is true of the C1 instrument and
  false of the wave. A writer can produce an acceptable C1 note and all four C2 items from
  committed bytes alone, without opening any snapshot.

### 5. Sizing and honesty — the depth 8 → 8 verdict I would file

**Not defensible as frozen; file an honesty erratum.** The ordinal has been 8 since round 4
(round-64 axes table: "Last change: round 4"), with every sourced entry logged "ordinal unchanged"
— including round 64's sourced plane on **r17-held** ground. Round 75's plane is on ground the
lane **never held** (held-ground grep 0/0 at base) — categorically the stronger depth event — yet
the declaration freezes no rubric clause for why six sourced rows on empty ground leave the
ordinal at 8, and no post-round arithmetic. Meanwhile the axes table restated (C2 item 4) will
print `| depth | 8 | <backticked command> |` and **no instrument executes that command or compares
its output to 8** — an unfalsifiable ordinal conjunct. The strategic wrinkle: at 9 depth crosses
the saturation line (SCORECARD.md:179) and retires from lowest-axis duty, so both 8 and 9 have
strategic readings; freezing the rule is what removes the ambiguity. Smallest safe correction:
cite the band rule in the declaration (or restate depth's counting command as the JT counter
itself and declare the ordinal a function of its output). Defensible fallback framing, if the lane
owns it in prose: depth's ordinal stopped discriminating at band 8 seventy rounds ago; the axis's
real movement is the row counters (JT_ROWS / S-rows), which this round's instrument measures well.

## Findings, ranked

- **D1 — C1 predicate is polarity-blind (falsifiability).** Negating every load-bearing polarity
  ("never redundant"→"always redundant", "can never appear"→"can always appear", "always
  collapses"→"never collapses", "is associative … transitive"→"is not associative … not
  transitive", "propagates only as"→"propagates never as") still reads `JT_ROWS=6 JT_VERIFIED=6 …
  met=1` rc 0. The counter tests vocabulary + quote location + registry plumbing, never truth; the
  quote is not required to relate to the statement at all.
  Evidence: fx2 (recipe A2) → `met=1 rc 0`.
  Smallest safe correction (instrument-generic, no answer key): add a quote↔statement token-overlap
  clause (≥1 shared non-stopword token) and **state C1's honest scope in the claim**: sourcing
  discipline and non-held vocabulary, not semantic verification; content falsification remains the
  reader's job.
- **D2 — JT5's count is untestable and grep-hostile (C1).** "ten labelled steps" → "eleven" passes
  (`met=1`); the eighth step is spelled "Eights step" (`transaction.c:864`), so `grep Eighth` rc 1
  undercounts nine; the draft's own enumeration lists nine items under "ten".
  Evidence: fx3 (A3); `grep -n "Eighth" .ufo/waves/round-75/before/src/transaction.c` → rc 1;
  `sed -n '864p'` → "Eights step".
  Correction: fix the draft enumeration before it becomes the note (list ten, or say the eighth is
  the typo'd "Eights step"); optionally name the label sequence in the note prose.
- **D3 — wave-level answer key (C1 channel).** `draft-rows-validated.md` + `SOURCES.json` let a
  writer assemble a green note with zero snapshot reads; fx1 (A1) reproduces the declared control
  byte-identically. Correction: none required if the round's prose claims transcription, not
  discovery; keep the draft (the control needs it) but say what it implies.
- **D4 — C2 closes by token dump; item 4 is decorative (C2).** Content-free blocks + `echo`
  commands + verbatim stale scores → `ROUTED_STALE=0 ROUTED_OK=4/4` rc 0; commands never executed,
  scores never compared. Evidence: fx5 (A4).
  Smallest safe correction: require item 4's block to carry the two frozen instrument digests
  (backticked) and the two tool paths, tying the restated table to instruments that exist and are
  hashed; accept dumps for items 1–3 as the nature of routed clerical closure, but say so.
- **D5 — first-occurrence shadowing (C2).** One innocuous early token mention flips a genuine
  closure from PASS to permanent STALE (fx6a 1/4 → fx6b 0/4, same EOF block). DECOY-DISTANT does
  not cover this direction. Evidence: fx6a/fx6b (A5).
  Smallest safe correction: `token_block` scans **all** occurrences and the item passes if **any**
  occurrence's window satisfies the clauses (DECOY-DISTANT still fails under any-occurrence, since
  its content sits >80 lines from every occurrence).
- **D6 — the supersede verb is free (C2).** Pre-existing lesson prose (lines 43–68: "corrections
  sweep", "superseded") satisfies `has_verb` for any window reaching it; fx7 passes item 1 with no
  corrective verb in the appended line. Evidence: fx7 (A6).
  Correction (optional, cheap): require the verb on the token's own line or within 3 lines of it.
- **D7 — missing cheap control (controls).** No C2 positive reachability receipt at real base
  bytes (the draft-row-control asymmetry); no `--selftest`/digest verification lines in
  `absence-controls.txt`. Evidence: this report §3; fx5 demonstrates the missing control passes.
  Correction: append the C2 repair replay and the two selftest+digest lines to
  `absence-controls.txt` before data.
- **D8 — unfalsifiable depth ordinal (sizing/honesty).** §5. Correction: freeze the band rule or
  make the restated depth command the JT counter; state the post-round arithmetic in the
  declaration.

Not defects (checked and passed): instrument digests match frozen values; both selftests 13/13; all
declared base controls reproduce; held-ground sweep 0/0 claim reproduces (grep exit 1, 0 lines);
SHA256SUMS 3/3; causal separability holds (the two counters read disjoint files); the frozen
instrument-change rule (erratum with old→new digests) is adequate; the exit maps match the
declared receipts (128 for absent at base, not 1).

## Appendix — evidence reproduction (scratch deleted; recipes only)

All fixtures under `/fast/scratch/hyaku/tsukuroi-r75/K1Critic/` (deleted). Common: snapshots =
`.ufo/waves/round-75/before/src/{transaction.c,job.c,job.h,SOURCES.json}` copied into
`<fx>/.ufo/waves/round-75/before/src/`; note at
`<fx>/corpus/knowledge/systemd-job-transaction-plane-r75.md`; registry = `git show
1e2bb29c:corpus/SOURCES.md` + three appended rows `S314/S315/S316` (kind `code`, source cell
carrying the map URL, anchor cell carrying the basename) — composed, since they are absent at base
and tip. Run `python3 tools/count-jt-rows-r75.py --fixture <fx>`.

- A1 fx1: note = `grep '^| JT' .ufo/waves/round-75/before/draft-rows-validated.md` → met=1 rc 0.
- A2 fx2: A1 note with polarities negated (D1 list) → met=1 rc 0.
- A3 fx3: A1 note with `ten`→`eleven` in JT5 → met=1 rc 0.
- A4 fx5: base `round-74.md` + dump block; base `receipt-g-landing.txt` + both-OID paragraph; base
  `SCORECARD.md` + restated table with `` `echo <axis>` `` commands → checker `--root` rc 0 4/4.
- A5 fx6a/fx6b: base lesson + genuine EOF block (6a → 1/4); + innocuous early token line (6b → 0/4,
  `reason=need`).
- A6 fx7: base lesson + line 41 token+substrings, no verb → item 1 passes on inherited verb (1/4).
- Base-control reproduction: `python3 tools/count-jt-rows-r75.py --selftest && --revision a21302a4`;
  `python3 tools/check-r74-routed-r75.py --selftest && --revision a21302a4`; `sha256sum` both tools.
