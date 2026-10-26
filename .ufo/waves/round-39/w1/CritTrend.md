VERDICT: defect-found

# CritTrend — R-9, pre-attack of the round's trend verdicts

Seat: L2 critic, round 39 w1 (`hyaku` run 8). Read-only on lane content. Tip read: `394e1ba4fab39a417abe66a7802f87cf1ff8dd61`
(`git log -1`). Two read-only census runs of the lane's own tool in my scratch (`/fast/scratch/hyaku/tsukuroi-r39/CritTrend`,
removed). No host mutation, no install, no lane write except this report and
`.ufo/waves/round-39/w1/CritTrend/receipts.txt`.

## 0. Bottom line at the tip, before integration

| Trend | Honest verdict now | Reaches `improved` only if |
|---|---|---|
| expansion | **unchanged** | a *new* admitted entry lands on coverage-map ground the map does not hold (none is possible from C1/C2 as declared) |
| quality | **unchanged** (and `harmed` if the two stale limit sentences ship unmarked) | §3's five items land: per-row TO verdicts with no `fails`, `partly` corrected in-entry, S217 carried into the round-38 entry, the two stale limit carriers superseded, Gate + search-log records |
| discernment | **unchanged** (no external sample exists) | a non-author spot-check of ≥1 admit **and** ≥1 reject with `agree`/`disagree` + reason in `corpus/lessons/round-39.md`, by someone who is not a lane-dispatched subagent |

The round's own instruments cannot substitute for any of these: both counters are format/location counters (§3.1), so a green
counter is not a trend verdict.

## 1. The rule each verdict is judged against

- Vocabulary and table: `LEARNING.md:28-29`, `:31-35`. Expansion `improved` = "net new admitted entries on uncovered ground,
  each citing its coverage-map row"; quality `improved` = "a weaker entry is superseded by a stronger one, or stale entries
  re-verify, with no admitted entry failing its re-check", quality `harmed` = "an entry is found false or stale and left
  unmarked"; discernment `improved` = "the spot-check agrees with the gate on admits *and* rejects, or a disagreement becomes
  a lesson that adds a grounded `QUALITY.md` criterion", `harmed` = "a disagreement is left unlearned, or a criterion is added
  with no lesson behind it".
- Expansion counts **entries, not rows**: `CORPUS.md:123-125` ("Expansion is knowledge, not rows. … There is no row quota").
- Discernment is external: `LEARNING.md:42-46` — "Each round a non-author … spot-checks a sample of that round's gate
  decisions, **at least one admit and one reject**, and records `agree`/`disagree` with a reason in the round's lesson. A
  subagent the lane dispatched is still the lane."
- Lesson shape: `LEARNING.md:71-73` (`## Gate`: candidates, admitted, rejected with reasons, **and the spot-check result**);
  `CORPUS.md:19`. Row-level Gate record: `CORPUS.md:112-114`. Search log: `CORPUS.md:126-128`.
- Trade rule: `LEARNING.md:37-38`. Axes: `LEARNING.md:86-90`. Criterion provenance: `LEARNING.md:61-63`.

## 2. expansion — `unchanged`; the honest verdict is not in doubt

Evidence the round is held ground:
1. The round itself declares C2's axis `depth`, not coverage (`SCORECARD.md:2221`); C1's axis is `operability` (`:2220`).
2. The entry states its own ground: "Ground: the update-safety plane (`PROVINCE.md` Core)" (`corpus/knowledge/pacman-transaction-order-r39.md:7`).
3. The source **kind** is not new: libalpm C source was already mined in round 38 — `S208` libalpm `hook.c`
   (`corpus/SOURCES.md:217`, `code`, tier A, `mined`). Round 39 adds the same kind (`S213`–`S217`, `corpus/SOURCES.md:222-226`).
4. No capability is admitted: `SCORECARD.md` "Capabilities — current full evidence set (round 38)" already carries
   `storage-error-counter-reader`; C1 repairs that arm, it does not add a capability (the only new rows are
   `SKILL.md:3116-3117`, counter rows, not capabilities).
5. `CORPUS.md:123-125` explicitly denies row count as expansion, so `207/212 → 218` rows (`grep -cE '^\| *S[0-9]{3} *\|' corpus/SOURCES.md`
   → 218) is not expansion evidence.

Three ways a report could dishonestly claim `improved`, and why each fails:
- "the mount table is now a Core surface" — C1 reads it for one guard; the round's own text refuses that claim
  (`PROVINCE.md:232-234`: "read for this guard only and is not a new owned surface"). Note that text is **uncommitted** (§3.2d).
- "between-phase order was uncovered" — the coverage map already holds `knowledge/pacman-hook-order-r38.md` on the same
  plane (`corpus/README.md:291`); the new entry says it complements HO1–HO7 (`…r39.md:7-11`). Deeper ground, not new ground.
- "six new mined source rows" — `CORPUS.md:123-125`.

What would honestly land `improved`: a net-new admitted entry whose `source:` cites a mined row on ground the map does not
hold, with the README row it cites — on this lane that means the areas `PROVINCE.md:212-214` still lists as Frontier (the scrub
record, NVMe SMART) entering Core through a census arm, as round 26's condition required.

## 3. quality — `unchanged` now; `improved` needs five landings; two defects already tested

### 3.1 The round's C2 counter cannot carry the verdict

`tools/check-transaction-order-r39.py:1-20` and `:25-38` define `rules_verified` as: quote (4–25 words) found inside the
cited lines of a digest-pinned snapshot, an `S###` row with `status=mined`/`used-by`/URL shape, and every S-id present on the
entry's `source:` line. It never compares rule text to source semantics — the assignment says so too. So
`rules_verified == 8` (`SCORECARD.md:2221`) is a format-and-location count; the truth of the eight sentences is exactly what
`QUALITY 81` (`corpus/QUALITY.md:157`, "a committed non-author reviewer verdict file (holds, partly holds, fails)") and the
closure spot-check have to supply. At the tip there is no committed per-row verdict: the reviewer seats' outputs live only as
untracked seat directories under `.ufo/waves/round-39/w1/` (`C2RevTransSync`, `C2RevHookC`, …).

### 3.2 Tested counterexamples

(a) **TO3 is at best `partly` on its own wording, and the counter passes it anyway.** The row
(`corpus/knowledge/pacman-transaction-order-r39.md:26`) writes "then `installed`/`upgraded` is logged". The pinned source
also logs `downgraded` (`.ufo/waves/round-39/frozen/src/add.c:622`) and `reinstalled` (`:626`), and both scriptlet legs are
gated on `alpm_pkg_has_scriptlet(newpkg) && !(trans->flags & ALPM_TRANS_FLAG_NOSCRIPTLET)` (`:468-469` pre, `:639-640` post)
— a branch the row does not state. `QUALITY 66` (`corpus/QUALITY.md:133`) requires a statement to keep every branch its
quoted source states. My TO line is at the end of this report. Note the asymmetry this exposes: C2's declared kill rule
(`SCORECARD.md:2221`) fires only on a row judged **FALSE**; the quality trend's bar (`LEARNING.md:34`) is stricter (no admitted
entry failing its re-check), so a `partly` row does not kill C2 but does stop an unqualified `improved` until the entry carries
a correction block. TO6 I checked against `add.c:655-692` and it holds.

(b) **S217 supersedes S210's anchor, but the entry that cites S210 is unmarked.** `corpus/SOURCES.md:226` is the conformant
correction (`CORPUS.md:115-118`: a new row whose `teaches` opens `supersedes S0NN —`). But
`corpus/knowledge/pacman-hook-order-r38.md:1` still lists `S210` in `source:` and `grep -n "S217" corpus/knowledge/pacman-hook-order-r38.md`
returns nothing; its own bullet (`:145-147`) says only "the registry row is not rewritten". `LEARNING.md:34`'s observable is an
*entry* superseded — so quality `improved` needs an append-only notice in that entry pointing at S217. Without it the round has a
strengthened registry row and an unchanged entry.

(c) **A statement in the file C1 changed is now false.** `tools/tsukuroi-census.sh:377-380` still reads: "Known limit, recorded
not repaired (C1CritAbsentRoot): an ABSENT root still reads HEALTHY 0/0/0, so a namespace that hides /sys/fs/btrfs while btrfs
is mounted gives a false all-clear; a /proc/self/mounts cross-check … is next-round work." Two runs falsify it:

```
$ TSUKUROI_BTRFS_SYSFS=<existing empty dir> TSUKUROI_PROC_MOUNTS=<file with "/dev/sda1 / btrfs rw"> bash tools/tsukuroi-census.sh | grep '^STORAGE'
STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs
$ TSUKUROI_BTRFS_SYSFS=<nonexistent path>     TSUKUROI_PROC_MOUNTS=<same file>            bash tools/tsukuroi-census.sh | grep '^STORAGE'
STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs
```

(`.ufo/waves/round-39/w1/CritTrend/receipts.txt` R1, R2.) The same file now carries the opposite rule at `:364-369`. Two
authorities in one header, one of them false at the tip. `git show 49cc53c -- tools/tsukuroi-census.sh` shows the commit did not
touch `:377-380`.

(d) **The supersession record exists only in the working tree.** `git status --porcelain` at the tip prints ` M PROVINCE.md`
and ` M SKILL.md`; `git diff --stat` = `PROVINCE.md | 14 +`, `SKILL.md | 21 +`. The content is right
(`PROVINCE.md:225-237` "Round-39 limit closure — R38-ABSENT-ROOT … its **Known limit** sentence is superseded here, not deleted";
`SKILL.md` working tree `:3205-3224`, which also carries the correct consumer note for the round-38 v1 counter F06) — but at
`394e1ba` it is not committed, so it is **not evidence yet**. Meanwhile `corpus/README.md:300-301` still states the limit as
current ("Known limit carried to the frontier: an absent `/sys/fs/btrfs` reads `HEALTHY 0/0/0`, so a namespace that hides it
gives a false all-clear"), and `git show --stat 49cc53c` shows README was not touched. Under `LEARNING.md:34` a stale entry left
unmarked is `harmed`; at the tip that is the literal state of two carriers.

(e) **The assimilation record is stale by the round's own appends.** `.ufo/waves/round-39/assimilation/collisions` lists 13 ids
(S200–S212). After S213–S218 the intersection with the staged set is 19:
`S200 … S218` (`receipts.txt` R3), corroborated by the peer artifact `.ufo/waves/round-39/w1/AsmCollision/rerun/collisions`.
Round 38 recorded both numbers in its Gate (`corpus/lessons/round-38.md:40-41`: "before the round's appends 207 … collisions 8
(S200–S207); after S208–S212 the collisions are 13"). The round-39 Gate must carry collisions-after = 19, and the fact that the
staged package also numbers S213–S218 with *different* subjects (`AsmCollision/rerun/collision-map.txt`: staged S217 = PKGBUILD(5),
lane S217 = trans.c) is the reason a by-document renumber is still required before any assimilation.

(f) **No search-log paragraph for rounds 38 or 39.** `CORPUS.md:126-128` requires one prose note per bounded search with
identified/screened/included/excluded counts and exclusion reasons; `grep -n "Round-38 bounded\|Round-39 bounded" corpus/SOURCES.md`
prints nothing (R7). The last such note is the round-37 one (`corpus/SOURCES.md:297`, erratum `:300`). Six rows opened this round
(`:222-227`) and a proposition map promised (`…r39.md:16-18`) need that note.

(g) **QUALITY 83's parenthetical label resolves nowhere.** `corpus/QUALITY.md:163` labels its lesson `R38-VERDICT-CONJUNCT`;
`grep -rl` over `corpus/lessons/` finds it in 0 files (R6). The criterion's own `Lesson:` clause names
`R38-CLOSURE-DISAGREEMENT`, which exists (`corpus/lessons/round-38.md:90`). Precedent for the reading: `corpus/QUALITY.md:155`
(the R31 correction reading round 30's wrong pointers as the sections that exist). So this is a label erratum to append, **not**
"a criterion added with no lesson behind it" — I do not read it as a discernment harm.

### 3.3 What `improved` requires (`unchanged` → `improved`)

- q1. Eight committed non-author per-row verdicts; no `fails`; every `partly` answered by an appended correction block in the
  entry — round 38's exact route: HO5/HO6 partly-hold corrected append-only, then quality `improved`
  (`.ufo/reports/round-38/tsukuroi.md:106`).
- q2. An append-only notice in `corpus/knowledge/pacman-hook-order-r38.md` pointing its `source:`/HO5/HO6 rows at S217's
  corrected anchor (closes (b)).
- q3. (c) corrected in the same file, and README `:300-301` superseded append-only (closes (d)'s README half); SKILL.md and
  PROVINCE.md committed.
- q4. `corpus/lessons/round-39.md` `## Gate` with URL, access date and a ≤25-word quote for each of S213–S218 (`CORPUS.md:112-114`),
  plus collisions-after 19 and the search-log note (closes (e), (f)).
- q5. The QUALITY 83 label erratum appended (closes (g)).

Harmed if any of (a)/(c)/(d) ships unmarked: a TO row found partly/false and left unmarked, or a committed statement that the
tool now contradicts. If the round instead declares `quality: improved` while leaving them, that is the trade `LEARNING.md:37-38`
forbids admitting — and here it is not even a trade, because (c) is a false sentence in the very file C1 rewrote.

## 4. discernment — `unchanged`; the round must not repeat round 38's ordering mistake

The precedent to avoid, on the record: round 38's report declared "**discernment: improved** — … Outside spot-check of this
round is pending" (`.ufo/reports/round-38/tsukuroi.md:108-110`). `LEARNING.md:42-46` says self-assessed taste is not discernment
and the sample is taken by a non-author. That claim was later vindicated — `corpus/lessons/round-38-verifier-spotcheck.md:113-138`
records `agree` on four admits (S208–S211) and both rejects, with reasons — but the ordering was wrong and only luck made it
right. Round 39 must either wait for the external sample or say `unchanged`.

State at the tip: `corpus/lessons/round-39.md` does not exist (`ls corpus/lessons | tail` ends at
`round-38-verifier-spotcheck.md`); the entry promises its Gate (`…r39.md:16-18`, "Which of its propositions this entry admits,
corrects or rejects is recorded in `corpus/lessons/round-39.md` Gate"); no round-39 spot-check file exists.

The reject-supply problem, which is the real risk here: this round's own gate decisions are all **admits** — six rows
(`corpus/SOURCES.md:222-227`, all `mined`) and one entry. The only refusals in view are round 38's two staged rejections
(`corpus/lessons/round-38.md` Gate), and this entry partially satisfies one flip condition ("a lane-authored entry that applies
C1–C9, re-points each citation by document to new lane rows opened in that round"): it re-grounds the propositions on S213–S218.
Re-adjudicating a round-38 reject is not a fresh reject decision, so the `at least one … reject` half of the sample
(`LEARNING.md:44`) has no supply unless the round opens and refuses a fresh candidate, or records a proposition-level rejection
inside the staged-entry map (`C2RevenStaged`) and states that it is being used as the reject sample. Either is honest; a report
that samples round 38's rejects as if they were this round's is not.

What `improved` requires:
- d1. `corpus/lessons/round-39.md` `## Gate` with candidates considered, admitted, rejected-with-reason, and the spot-check
  result (`LEARNING.md:71-73`).
- d2. ≥1 admit and ≥1 reject sampled, each with `agree`/`disagree` and a reason (`LEARNING.md:44`).
- d3. The sampler is a non-author outside the lane's dispatch (`LEARNING.md:45-46` — "A subagent the lane dispatched is still
  the lane"), i.e. the hyaku closure or the operator, and the report must say so; `[x]` in SHONEN is allowed only with that
  named verifier (`.ufo/prompts/tsukuroi-round-39.md:118-119`).
- d4. If the sample disagrees, the disagreement becomes a lesson that adds a grounded `QUALITY.md` criterion citing it
  (`LEARNING.md:35`, `:61-63`).

## 5. Axes this attack touches

- freshness — (c), (d): false/stale limit statements at the tip.
- calibration — (g): a criterion label that does not grep; the counters' scope claims.
- depth — (a): one row narrower than its source.
- coverage — untouched (expansion holds at `unchanged`); `SKILL.md:3116-3117` registry rows are already committed, so
  QUALITY 70 is satisfied for both counters at the tip (`git show HEAD:SKILL.md | grep -n` → 3116, 3117).
- operability — the arm's behaviour is correct (R1/R2); only its documentation is wrong.

## 6. Smallest safe corrections (exact text)

1. `tools/tsukuroi-census.sh:377-380`, replace the four lines with:
   `# Superseded round 39 (R38-ABSENT-ROOT): the rule is stated above at :364-369. An absent or empty root whose mount table`
   `# lists a btrfs mount reads BLOCKED detail=mounts:btrfs-without-sysfs; no such root reads HEALTHY 0/0/0.`
2. `corpus/README.md`, append after `:301`:
   `## Round 39 — R38-ABSENT-ROOT closed (2026-10-26)`
   `The round-38 Frontier sentence above ("an absent /sys/fs/btrfs reads HEALTHY 0/0/0, so a namespace that hides it gives a`
   `false all-clear") is superseded: since `49cc53c7` an absent or empty root with a btrfs mount in the table reads`
   ``BLOCKED … detail=mounts:btrfs-without-sysfs``, and an unreadable table `BLOCKED … detail=mounts:unreadable`. The old`
   `sentence stays as written. Counted by `tools/score-storage-hidden-r39.py`; `SCORECARD.md` "Round 39".`
3. `corpus/knowledge/pacman-hook-order-r38.md`, append:
   `- **S210 anchor, superseded row.** `corpus/SOURCES.md` S217 (round 39) opens "supersedes S210 —" and carries the correct`
   `symbol `alpm_trans_commit` (`trans.c:167`, Pre `:201-204`, `transaction started` `:208`, Post `:232-239`). The S210 row`
   `itself is not rewritten (CORPUS.md rule 2); read HO5 and HO6 trans.c citations through S217.`
4. `corpus/lessons/round-39.md` Gate: add `collisions-after = 19 (S200–S218)` beside the staged collision count, and the
   `CORPUS.md:126-128` search-log note for the round-39 search.
5. `corpus/QUALITY.md` append: `R39 clarification to 83: the parenthetical label reads `R38-VERDICT-CONJUNCT`, which occurs in no`
   `lesson file; the lesson is `R38-CLOSURE-DISAGREEMENT` (`corpus/lessons/round-38.md:90`), as the criterion's own Lesson clause says.`
6. If a reviewer judges TO3 `partly`: append a TO3 correction block naming `add.c:622`, `:626` and the
   `ALPM_TRANS_FLAG_NOSCRIPTLET` gate at `:468-469`/`:639-640`, and state that `installed`/`upgraded` is the "not exhaustive" set.

## 7. What I did not do

I ran neither frozen counter (`score-storage-hidden-r39.py`, `check-transaction-order-r39.py`) and claim no predicate result;
I ran two override fixtures of the census storage arm only, in my own scratch. I judged exactly two rule rows (TO3, TO6) and no
others. I read peer seat directories only to check whether a finding was already taken (AsmCollision's collisions-after) — I did
not treat their outputs as evidence for anything else. I did not verify the host counts (60/86/441/252) or the append-only sweep
(that is `RevNoHarmAxes` and `C2ExecRerun`). I did not install or upgrade any tool. I wrote only this file and
`.ufo/waves/round-39/w1/CritTrend/receipts.txt`.

TO3: partly — .ufo/waves/round-39/frozen/src/add.c:618,622,626,468-469 (omits the `downgraded`/`reinstalled` log lines and the `ALPM_TRANS_FLAG_NOSCRIPTLET` gate on both scriptlet legs)
TO6: holds — .ufo/waves/round-39/frozen/src/add.c:655-692
