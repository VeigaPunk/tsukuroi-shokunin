VERDICT: defect-found

# F-9 — QUALITY 90 attack (seat QualityCrit)

Item F-9. Bytes under test: `corpus/QUALITY.md` at `78abb8b5cdc9da511b4fc523e661517a68dd33d3`,
file sha256 `47c404049cfb43e38809626272f5e02e7da6406bb20351af9739560af59a8129`; criterion 90 is
`corpus/QUALITY.md:177`, sha256 `d69870a4ca5694d02e0ad7fe288d56d2ca1b14433a757d480e83fa5be3778a41`, 273 words
(`w2/QualityCrit/digests.txt`). Frozen C1 counter read at the same revision, sha256 `c511104a8e69fe6a…`
(identical at `a84fc9de`, `87c4f7c6`, `78abb8b5`, `a968393c` and the worktree — `digests.txt`).

## 1. The four questions, answered

**1. Does it cite a lesson that exists?** The row exists only in an **untracked** worktree draft: at `78abb8b5`
(the commit that appends the criterion) and at HEAD `a968393c`, `git cat-file -e <rev>:corpus/lessons/round-42.md`
fails, `git ls-files --error-unmatch` errors, and `git status --porcelain` reports `?? corpus/lessons/round-42.md`
(`w2/QualityCrit/lesson-pointer.txt`; draft sha256 `fd005cb5…` when read — a sibling scribe is editing it, so cite
the row id, not its line). The item allows the lesson to land after this wave, so the file itself is acceptable if
the round's final commit lands it. **The pointer is incomplete:** criterion 90 carries two independent rules — the
observed-channel rule and the verdict-binding rule — and the draft holds them as two rows, `R42-OBSERVED-CHANNEL`
and `R42-VERDICT-MENTION` (the draft's own routed-defect item 3 maps both to "QUALITY 90"). A reader following
`Lesson: … Mistakes R42-OBSERVED-CHANNEL` for the second clause lands on a row about the C1 namespace legs.

**2. Are the failing examples accurate?** Partly.

- The C2 example is accurate: `tools/check-scrub-record-r42.py:66` is
  `VERDICT_RE = re.compile(r'ROW (SC\d) VERDICT: (holds|partly|fails)\b')`, the report test at `:134` is a plain
  substring, and `w1/C2CritControl.md` D1's mutants M3/M4/M4b reached `verdict=PASS verdicts_ok=5` on a disputing
  sentence. One role word is off: the cited mutant is the **reviewer** of SC1 ("Mutant M4 — reviewer of SC1
  writes…"), not a critic.
- The C1 example overreaches its sources. `w1/C1CritNsView.md` §3 measured V1, V2 **and** V3 at `PASS`; §4
  measured the production-identity break for **V1/V2 only** ("Independent measurement: the V1/V2 arms are broken
  at production identity"). V3 has no production-identity measurement in either cited report, and
  `w1/C1CritEvasion.md` §1's V1i production reading is `HEALTHY` on `qkk-large` and exit 141 on `qu-large` — not
  `DEGRADED`. So "censuses fixed only under `TSUKUROI_FIXTURE`-or-uid-0 **or only for those four names** … while
  the production path still read `DEGRADED`" merges one measured arm (V1/V2) with one unmeasured arm (V3) and one
  differently-reading arm (V1i) under a single `DEGRADED` claim.
- The second locator is a bare filename, `C1CritEvasion.md` §1, with no directory (QUALITY 32: a bare path is not
  a locator; the first citation in the same parenthesis is fully qualified).

**3. Does it duplicate 82/85/89?** Not in content — the identity channel, the fixture-provenance channel, the
production-identity requirement and the verdict-line anchoring are all new. But the mechanism sentence
("the frozen pre-data controls include, per channel … and each must read below the target") **restates QUALITY
85's sentence** ("The frozen pre-data controls include one arm per channel … and each must score below the
target", `corpus/QUALITY.md:167`) with a channel list that reads exhaustive and **omits 85's five channels**
(`$HOME`/`$TMPDIR` sibling, bind-mount source, argv element or environment value, `/proc/self/mountinfo`'s mount
root, inherited cached answer) and 82's cached-live second view. A counter that satisfies 90's four families can
drop the five 85 arms and still claim 90. 89 is not duplicated: its subject is the scored artifact's lexical
guard; 90's second clause is the counter's binding (the draft row itself records that "QUALITY 89 (binding) did
not ask for an asserted line").

**4. Is it checkable?** A **miss** is demonstrable, and a **meet** is demonstrable for two of the four families —
but not for the third, which is the one the clause names by example:

- meet, identity channel: `w2/C1FinalProdIdentity.md` §2-3 runs at `id=1000 euid=1000 tsk_vars=0 … nenv=7`
  (`probe-identity.txt:1-2`) and separates V1 (`DEGRADED`) from the tip (`BLOCKED`) — clause 2's
  "production identity (same uid, real environment shape)" is measurable;
- meet, override-environment channel: control K7 reads `FAIL inv 10 ns 0` (`controls/C1-K7.jsonl`);
- **miss, stub-text channel (measured, §2 below):** a census fixed only when its `$PACMAN` is a script scores
  `PASS` on the full predicate. Clause 1 demands that this arm "read below the target", and no leg in the frozen
  battery can make it: the fixture legs' pacman is a symlink to the **BASE census's own** `.dispatch`
  (`#!/usr/bin/env bash`, `tools/tsukuroi-census.sh:1937-1938` at `c8efaa3f`; the counter copies it,
  `tools/score-size-invariance-r42.py:233`), the namespace leg's pacman is `NS_STUB` (`#!/bin/bash`, `:266`), and
  the host's is ELF (`od -c`: `177 E` — `w2/QualityCrit/gate-and-legs.txt`). The only leg with a non-stub pacman
  and a probe large enough to fire is a live run at a raised sample, and that knob is
  `SAMPLE_N=${TSUKUROI_SAMPLE_N:-8}` (`:451`) or `--sample` (`:3135-3139`) — a channel 85 names and 90 does not.
  The criterion gives no rule for recording such a channel: it either demands an arm that cannot fail, or its
  second-sentence escape ("named an override-free leg and its channels are reported open") leaves the first
  sentence's "each must read below the target" unexplained and unmet.
- **The clause-2 trigger is evadable by wording:** the counter "is offered as" a production-path leg in its
  docstring ("Production-path legs (QUALITY 82/85)", `tools/score-size-invariance-r42.py:30`, unchanged at
  `78abb8b5`) and in the declaration (`SCORECARD.md:2573`, "(QUALITY 82/85)"), but it never writes the quoted
  phrase "a view the code cannot tell from production". Under a literal reading, clause 2 does not bind the very
  instrument it was written for — and that instrument's legs do run as uid 0 with the fixed sample.

## 2. Measured counterexample: the stub-text channel reaches the target

Arm built on a fixture clone of the lane (`git clone -q --shared`, origin removed, `rev-parse --show-toplevel`
asserted equal to the clone), census from BASE `c8efaa3f`, five sites gated only on
`[ "$(head -c 2 -- "$PACMAN" 2>/dev/null)" = '#!' ]`; commit `835306ac7b0bb6ed2a4b5fbfeaaf87cbde921624`
(scratch clone, removed; driver and diff kept: `w2/QualityCrit/variant-stubtext.py`, `stubtext.diff`):

```
$ python3 <lane>/tools/score-size-invariance-r42.py --lane <clone> --revision 835306ac --scratch <scratch>
exit=0
{'verdict': 'PASS', 'cases': 10, 'invariant': 10, 'ns_invariant': 3,
 'selftest_pass': 1, 'selftest_label': 'PASS (128 cases, 128 passed, 0 failed)',
 'default_equal': 1, 'non_invariant': []}
ns_cases: {'N1': True, 'N3': True, 'N6': True}
```
(`w2/QualityCrit/stubtext.jsonl`, 65.11 s wall.)

The unwatched branch of `stubtext.diff` is the base's R41 readers verbatim (`printf '%s\n' "$s_out" | grep -q
'^error:'` / `| grep -m1`, `head -n3`), and the base at production identity reads `DEGRADED` (and `HEALTHY` on a
quiet foreign arm) where the tip reads `BLOCKED` (`w2/C1FinalProdIdentity.md` §3, `uid1000-base.txt:1-2`,
`capture-base-cleanforeign.txt:3`). So the arm is a census that is broken at production identity while reading
exactly like the fixed tip under every observation the frozen battery can make — the class of evasion criterion 90
exists to close, on a channel criterion 90 names.

What this falsifies is the sentence "each must read below the target" for the stub-text family, not clause 1's
usefulness: the identity and environment arms are sound and already measured. The smallest correction is to make
the arm requirement conditional on a leg in which the channel reads unwatched **and** the probe still fires, and
to record an inherent channel as an armed control with its observed result, exactly as the criterion's own cited
report asks (`w1/C1CritNsView.md` §7: "that has to be an armed control that is expected to PASS, disclosed as a
limit of every namespace leg, not a claim of non-distinguishability") and as QUALITY 89 already permits ("where no
such check refuses it the family is reported open, not closed").

## 3. Defects and their smallest safe correction

| # | defect | correction |
|---|---|---|
| D1 | lesson pointer names one of the two rows it encodes; the file is untracked at `78abb8b5` | name `R42-OBSERVED-CHANNEL` **and** `R42-VERDICT-MENTION`; the round's final commit lands the file (say so in the round report) |
| D2 | C1 example merges V1/V2's measured production break with V3 (unmeasured) and with V1i (`HEALTHY`, 141); bare `C1CritEvasion.md`; "a critic's sentence" where D1's mutant is the SC1 reviewer | attach the `DEGRADED` reading to V1/V2 only, cite §4 for it, spell the second locator as `.ufo/waves/round-42/w1/C1CritEvasion.md` §1, and write "a reviewer's sentence" |
| D3 | arm sentence restates QUALITY 85 and reads as its replacement | "in addition to the channels of QUALITY 82 and 85" |
| D4 | "an anchored first line" is wrong for the answer channel: the dispatch requires the report's **first** line but only "one line of your final answer" (`make-w2-spec.py:40-43`); the fix its own source verified is an anchored **line of its own** plus one verdict per row (`w1/C2CritControl.md` §4), and D2's self-contradictory report must not bind | "the report's first line, or an answer line that is exactly the verdict line and a line of its own; … an artifact carrying two different verdict lines for one row binds neither" |
| D5 | clause 1 unsatisfiable for an inherent channel, and the escape is not tied to the arm; clause 2's trigger is a quoted phrase the round's own counter never writes | arm must read below the target *in a leg where the channel reads unwatched and the probe still fires*; a knob-carrying leg is an 85 leg; an inherent channel is an armed control with an observed PASS and the leg renamed; trigger = "cites QUALITY 82 or 85, or calls itself a production-path leg" |

## 4. Exact replacement text (replaces `corpus/QUALITY.md:177`)

```
90. **A counter that holds no answer key is scored against every channel through which the scored code can see it is being watched, and a verdict binding matches an asserted line, not a mention (R42-OBSERVED-CHANNEL, R42-VERDICT-MENTION):** when a counter's oracle is the code's own behaviour (a metamorphic twin, a production-path leg) or a verdict bound through orchestrator records, the frozen pre-data controls include, in addition to the channels of QUALITY 82 and 85, one arm per readable channel family — the override environment, the process identity (uid/euid, groups), the fixture data's own provenance (the sample is not the host's package list; the probe binary is not the package's binary) and the namespace's own traces (mount table, bind targets, stub text); each arm is the variant that applies the claimed fix only when that channel reads "watched", and each must read below the target in a leg where the channel reads unwatched and the probe that carries the defect is still large enough to fire it, while a leg that needs the sample-size or probe-path knob to fire reaches the view through that knob (QUALITY 85) and is not production identity. A channel inherent to fabricating the probe — the stub binary's own text or identity, which every leg that fabricates the sample presents — cannot be closed by an arm: it is committed as an armed control whose observed PASS is reproduced in the battery output, the leg is named an override-free leg with its channels reported open, and no claim of a view "the code cannot tell from production" is made. A leg that cites QUALITY 82 or 85, or calls itself a production-path leg, makes that claim and runs at the production identity (same uid, real environment shape, no `TSUKUROI_*` value) with fixture values drawn per run, or it is renamed. A verdict binding counts a line only where it is the report's first line, or an answer line that is exactly the verdict line and a line of its own; never a substring that a disputing sentence may quote, and an artifact carrying two different verdict lines for one row binds neither. Failing examples (round 42): the C1 counter's namespace legs ran as uid 0 with the fixed `alpha beta gamma delta` sample, so censuses fixed only under `TSUKUROI_FIXTURE`-or-uid-0 (V1, V2) and one fixed only for those four names (V3) passed the full predicate (`.ufo/waves/round-42/w1/C1CritNsView.md` §3; also V1i, `.ufo/waves/round-42/w1/C1CritEvasion.md` §1), V1/V2 reading `DEGRADED` at uid 1000 where the tip reads `BLOCKED` (§4); a census whose only gate is the stub's own text still scores PASS (`.ufo/waves/round-42/w2/QualityCrit/stubtext.jsonl`); the C2 counter's unanchored `ROW SC<n> VERDICT:` match (`tools/check-scrub-record-r42.py:66`) counted as `holds` a reviewer's sentence that quoted the holds line in order to dispute the row (`.ufo/waves/round-42/w1/C2CritControl.md` D1). Lesson: `corpus/lessons/round-42.md` Mistakes R42-OBSERVED-CHANNEL and R42-VERDICT-MENTION.
```

If the L1 prefers not to cite a wave-2 receipt in the criterion text, delete the fifth failing example; the
"inherent channel" clause still needs an example of a channel that cannot be closed, and C1CritNsView §7 supplies
one only in prose, not as a scored arm.

## 5. What I ran, and what I did not

Ran: read-only `git show`/`git status`/`grep`/`sed` on the lane; one pinned-source check
(`git cat-file -e` at three commits); one frozen-counter invocation (65.11 s wall, exit 0) against my own fixture
clone; one `od`/`head` on `/usr/bin/pacman`. No lane write, no sudo, no pacman, no mount or namespace of any kind,
no tool install. Scratch `/fast/scratch/hyaku/tsukuroi-r42/QualityCrit-2/` removed after the receipts were copied.

Disclosure: the dispatched item carries no execution class (QUALITY 31 would file it `SCOPE-UNDECLARED`); the
counter invocation above is disclosed as a deviation from any NO-EXEC reading, not claimed as authorized.

Did not: run the C2 counter; re-run V3 at production identity (so I report the criterion's V3 clause as unmeasured,
not false); edit `corpus/QUALITY.md`, the lesson draft, or any lane file; measure whether an arm gated on the
disjunction of several channels can be closed (I argue only the single-channel stub-text case, measured).

Receipts (this seat dir): `stubtext.jsonl` (counter output for the arm), `stubtext.diff` (base→arm census diff),
`variant-stubtext.py` (driver), `gate-and-legs.txt` (shebang/ELF evidence and the sample knob), `lesson-pointer.txt`
(pointer resolution at three commits; the two lesson rows), `digests.txt`.

Report: `.ufo/waves/round-42/w2/QualityCrit.md`
