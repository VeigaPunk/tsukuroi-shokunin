VERDICT: defect-found

Seat R49RevMarks (reviewer), item M-1, claim C1. Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
bytes under test `55c07cd3f8bff2e12117c34d57b4c618de74d85c` (read with `git show`; the working tree was used only
to read the uncommitted `w1` seat reports, which are not lane bytes under test). Fixtures and the counter copy:
`.ufo/waves/round-49/w1/R49RevMarks/` (driver `drive.py`, `drive2.py`, matrices `drive.out.json`,
`drive2.out.json`, freeze run `freeze_run.json`, counter sha256 `3dd52ef376e233192f955208c1132f6b0d23bbebe97dd1df75e6296f55d970a4`).

Legs observed at the freeze revision (`python3 counter.py --revision 55c07cd3… --no-base-check`):
`structural_ok 1, corr_ok 1, quotes_ok 3, verdicts_ok 0, seats_ok 0, marks_ok 0` →
`marks {'entry': false, 'readme': false, 'skill': false}`, verdict FAIL. The pending heading therefore does
not accidentally score the mark, and the seven corrections are in the bytes (`corr_ok 1`) while no cohort is
committed.

## F1 (high, blocking) — the admitted marks must not land this round; marks_ok 0 is the honest reading

The 18 `w1` GR reports exist with the frozen section hashes, and 17 read `holds`; `R49CritGR2b` reads
`partly` on the frozen GR2 hash:

- `.ufo/waves/round-49/w1/R49CritGR2b.md:1` `ROW GR2 VERDICT: partly`, `:2`
  `SECTION SHA256: d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f` (= frozen GR2,
  `FROZEN.md` row-hash table; my re-run of `--section-hash` prints the same three values).
- Its defect: the row's `[inference …]` bracket names the ioctl hand-off as unpinned although `S240`
  `ioctl.c` is pinned at that revision with a matching digest (`R49CritGR2b.md` "Defects", item 1).
- A bound-format negative blocks the row whatever its citations: `counter.py:364-365`
  `if v in ('partly', 'fails'): blocking.append(seat)`.

So `verdicts_ok` cannot exceed 2 and the predicate (`counter.py:94-95`) FAILs. Inserting `MARK_ENTRY`
(`counter.py:85`) would make `marks_ok 3` while the counter's own verdicts leg says the row is blocked —
the mark would assert an admission the measurement denies. Do not insert any of the three admitted marks
this round; land the FAIL wording in §"This round's honest replacement" instead.

## F2 (high) — the frozen pending heading is honest at freeze, but its closing sentence makes two false claims once the cohort settles

1. Honest at freeze: at `55c07cd3` the wave tree does not exist —
   `git -C … ls-tree 55c07cd3 .ufo/waves/round-49/` prints only `before/` and `frozen/` (no `w1/`, no
   `w1-results.json`), so `## Gate status — round 49 (pending; the frozen cohort has not settled)`
   (`entry:277`) was true. Keep it as the freeze-state record.
2. It is false now: the cohort has settled, so the heading may not stand as written after this round. `FROZEN.md`
   allows editing the heading text outside the row extents; the heading must become the FAIL wording below.
3. `entry:285-287` "This heading records **pending**, not admission: it says `admitted` only after the cohort
   settles `holds` on the current row bytes, and the round-48 findings are retained above as the reason the
   rows were not admitted then." — the retention clause is false: the entry has no round-48 gate section.
   Its headings are `:14 GR1`, `:56 GR2`, `:152 GR3`, `:198`, `:211`, `:233` (round 45), `:265` (round 46),
   `:277` (round 49); `grep -n -i 'round.48\|r48'` matches only `:280` and `:286`. The round-48 negatives
   survive only as a correction list (`:280-283`), not as findings with seat names and verdicts, so item
   requirement (c) is not met by the frozen bytes and the pending paragraph itself is inaccurate.
   `corpus/QUALITY.md:5` ("A rejection is kept, not silently dropped") is the bar this misses.

## F3 (high) — naming the round-48 defects verbatim re-breaks `corr_ok`; the body sentence must paraphrase

`CORR_FORBID` (`counter.py:108-114`) forbids the defect strings, so a body sentence that names a defect the
honest way flips `corr_ok` to 0 and FAILs the whole predicate even with 18 `holds`:

- fixture `v_V10_body_reintroduces_forbidden.entry.md` (my admitted entry with the clause
  "the suspend-path range dev-replace.c:1171-1199 and that it only sets the state to SUSPENDED") →
  `marks_ok 3`, `corr_ok 0` (`drive.out.json`).
- The drafted body below names the same seven defects without any forbidden string; the same run gives
  `corr_ok 1`, and a scripted check of all five `CORR_FORBID` patterns against the drafted entry text and
  README sentence found no hit.

## F4 (medium) — `marks_leg` accepts a heading contradicted by the body it heads

Fixture `w_W5_entry_body_keeps_pending_sentence.e.md` (heading flipped to `MARK_ENTRY`, the frozen sentence
"This heading records **pending**, not admission" left in place) scores `marks_ok 3`
(`drive2.out.json`). `marks_leg` (`counter.py:312-322`) reads only the heading line, so the counter cannot
catch the contradiction. Landing the heading without the body sentence is therefore a dishonesty the counter
silently rewards; §"Strings" carries the sentence that must land with it.

## F5 (medium) — exact landing rules observed (each variant run against the frozen counter)

| Fixture | Change from the accepted set | marks | marks_ok | corr_ok |
|---|---|---|---|---|
| `v_V1_admitted_note` | the three drafted strings | entry/readme/skill all true | **3** | 1 |
| `v_V2_negate_same_sentence` | README sentence ends `; the GR1-GR3 rows stay pending …` | readme false | 2 | 1 |
| `v_V3_negate_same_table_row` | sentence inside a table cell whose row also says `rounds 45-48 were unadmitted` | readme false | 2 | 1 |
| `v_V4_negate_neighbour_sentence` | full-strength negation in the NEXT sentence (`were unadmitted … stay pending`) | readme true | **3** | 1 |
| `v_V5_skill_trailing_spaces` | SKILL heading + two trailing spaces | skill true | 3 | 1 |
| `v_V6_skill_deeper_heading` | same heading at `###` | skill false | 2 | 1 |
| `v_V7_entry_trailing_space` | entry heading + one trailing space | entry false | 2 | 1 |
| `v_V8_pending_entry` | frozen pending entry with SKILL+README marks | entry false | 2 | 1 |
| `v_V9_readme_no_phrase` | README names the entry without `admitted round 49` | readme false | 2 | 1 |
| `w_W1_frozen_readme_with_admitted_entry` | frozen README unchanged | readme false | 2 | 1 |

Consequences for the landing: (i) the entry heading is an exact line match (`counter.py:313`) with no
trailing whitespace; (ii) the SKILL line is `strip()`-tolerant but must be a `##` heading
(`counter.py:314`); (iii) the README check splits the whitespace-normalised file on `(?<=[.!?])\s+`
(`counter.py:318-321`, inside `marks_leg` at :312-322), so a table row or a semicolon-joined clause is ONE sentence — negation there kills
the mark, while a separate neighbouring sentence does not; (iv) the frozen README alone does not pass, and
its last sentence ends in `.` (`readme:480`), so an EOF append begins a fresh sentence.

One caveat on (iv): because sentences are split after terminal punctuation, a non-negated *earlier* sentence
that already names the entry plus the phrase would also satisfy the leg; the frozen README has no such
sentence, so placement of the drafted sentence is load-bearing only against negation, not against absence.

## F6 (low) — the row-hash convention prose is wrong (no mark depends on it)

`FROZEN.md` says the row hashes are "LF-joined row lines, no trailing LF", and `counter.py`'s docstring says
"NO trailing LF". The empty line that precedes the next `## ` heading is inside the extent, so the hashed text
ends with `\n`: for GR1, `sha256('\n'.join(lines[i:j]))` = `3a2ba1807a7f2308…` (frozen) while
`sha256('\n'.join(lines[i:j-1]))` = `0b67bea0ed4960e3…`. `R49CritGR2b.md` reached the same conclusion
independently. The printed `--section-hash` value is authoritative, so no seat can be misled if it prints
rather than re-derives; the prose should say "extent joined with LF, blank separator line included".

## Strings — the admitted set (land ONLY when the counter's own predicate passes)

(a) Entry heading — replace `entry:277` `## Gate status — round 49 (pending; the frozen cohort has not settled)`
with exactly (UTF-8, em dash U+2014, no trailing whitespace; accepted by `counter.py:313`):

```
## Gate status — round 49 (GR1-GR3 admitted)
```

(b) Entry body sentence — replace `entry:285-287` (the whole "This heading records **pending** …" sentence)
with exactly (tested: `marks_ok 3`, `corr_ok 1`; no `CORR_FORBID` hit, so it does not re-break the correction
leg; keeps CritGR1a/CritGR2a/RevGR2a and their seven defects visible in the same entry):

```
After the freeze the `w1` cohort settled with `verdicts_ok 3` and `seats_ok 18` — all 18 bound seats read `holds`, at least three credited per row on the frozen row hashes with pairwise distinct bodies, and `corr_ok 1` — and that is all `admitted` records here: the round-48 counted seats read GR1 and GR2 `partly` (CritGR1a; CritGR2a and RevGR2a) and GR3 `holds`, and the seven defects they named (the `0X` case, the unmarked host-mode inference, the `is_valid` gate, the cancel sentence's subject, the suspend-path range that ran three lines past its function and its effects, the ioctl citation at `ioctl.c:3132`, and the `-ENODEV` devid case) stay named above as the reason the rows were not admitted then; the seat verdicts are this lane's own records, committed bytes cannot tell a forged orchestrator record from a real one (standing limit K3), and the Limits block is unchanged.
```

(c) SKILL heading line — exactly (accepted by `counter.py:314`; place it after the round-45 grounding section,
`skill:4286-4455`, or at EOF, so that "above" in the body line is true):

```
## Scrub grounding — round 49 admission
```

Recommended body line under it (not parsed by the counter; only the heading line is):
`GR1-GR3 of corpus/knowledge/btrfs-scrub-grounding-r45.md are admitted by 18 bound seat verdicts of wave w1, all reading holds with at least three credited per row on the frozen row hashes (tools/check-scrub-admission-r49.py); the round-48 negatives, the Limits and the standing limit on forged records carry over from the round-45 section above.`

(d) README sentence — exactly (accepted by `counter.py:318-321`; contains both `btrfs-scrub-grounding-r45.md`
and `admitted round 49`; no `NEGATE_RE` word in the same sentence; scoped to seat verdicts, not outside review
or any host observation), to be placed in the appended round-49 coverage note as its own sentence:

```
`knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3 are admitted round 49 on the wave `w1` cohort's 18 bound seat verdicts, all `holds`, at least three credited per row on the frozen row hashes, and not on outside review or any host observation.
```

Its honest neighbour sentence (separate sentence — tested `v_V4`: a negation here does NOT cost the mark,
while the same words joined by `;` or placed in the same table row do, `v_V2`/`v_V3`):

```
The round-48 counted seats read GR1 and GR2 `partly` and named seven defects that the freeze corrected, and the row Limits (no sysfs write, no stop trace) stand.
```

Wording checks against item (b): the heading says `admitted`, which in this lane means the frozen C1
predicate passed on the frozen row bytes; every string names the measured legs (`verdicts_ok 3`,
`seats_ok 18`, `corr_ok 1`, credited seats on the frozen hashes) and states what is NOT proven — no outside
review, no host observation, seat records of this lane, the K3 forged-record limit, Limits unchanged — so a
reader cannot infer host verification, external review, or the absence of unlisted defects.

## This round's honest replacement (use this, not the three marks)

Because `R49CritGR2b` blocks GR2 (F1), the heading and the closing sentence must be rewritten to the measured
outcome. `marks_ok` stays 0 — admission is the only state the marks leg can record, and the predicate fails on
`verdicts_ok` regardless, so no leg is being smuggled.

Heading (`entry:277`):

```
## Gate status — round 49 (the depth gate FAILED; GR2 blocked by a counted partly)
```

Sentence (replaces `entry:285-287`; verified against the 18 reports: 17 `holds`, 1 `partly`, all 18 with the
frozen section hashes):

```
The 18-seat `w1` cohort settled after the freeze: GR1 and GR3 read `holds` in all six seats on the frozen row hashes, and GR2 does not — `R49CritGR2b` bound `partly` on `d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f` because the row's `[inference …]` bracket calls the ioctl hand-off unpinned although the counter loads `S240` `ioctl.c` at this revision with its digest checked — and the A2 rule blocks GR2 whatever the other seats read, so `verdicts_ok` cannot reach 3 and GR1-GR3 are pending again; the round-48 negatives at `:280-283` and the Limits block stand, and `marks_ok` stays 0 because admission is the only state the marks can record.
```

## Not done

- I did not run the counter with `--wave-dir`/`--results-file`: `w1-results.json` does not exist yet and my
  item authorises fixtures for `--readme-file` only, so the "verdicts_ok ≤ 2" statement rests on the
  blocking rule (`counter.py:364-365`) plus the 18 report files, not on a bound counter run.
- I did not re-derive any snapshot digest; the frozen counter's own `quotes_ok 3` was read from its output.
- No lane file was created or edited; no census selftest was run; no pacman/tool install was needed.

Tooling: no install or upgrade (python3/git only, already present).
