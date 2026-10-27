VERDICT: draft

# ConnClaims — round 44, wave 1 (item X-1: cross-claim pattern across C1 and C2)

Scope: proposed QUALITY criterion. No claim is falsified here; this is a draft for the L1's
integration. Evidence is read from committed files only: the frozen counters
(`tools/score-scrub-arm-r44.py`, `tools/check-scrub-record-r44.py`), the pre-data control batteries
(`.ufo/waves/round-44/controls/run_controls_c1.py`, `run_controls_c2.py`), the committed battery
receipts (`battery-summary-c1.jsonl`, `battery-summary-c2.jsonl`, `C2-K*.jsonl`, `C1-K*.jsonl`),
`SCORECARD.md` "Round 44 — declaration", `corpus/QUALITY.md` criteria 77-92, and `SKILL.md`'s
counter-attack scoreboards (rounds 40-42). I did NOT run the counters or the batteries (a leaf seat;
the receipts exist), did not run any git-mutating command, and did not use scratch (nothing to build).
Report only; no receipts.

## 1. What each counter closes, and what it leaves open

### C1 (`tools/score-scrub-arm-r44.py`)

Closed channels, per the counter's own docstring (`:47-50`) and `run_controls_c1.py`:

- Override environment: `clean_env()` drops `TSUKUROI_*`, `UFO_*`, `TMPDIR` (`score-scrub-arm-r44.py:179-180`); the namespace leg runs with that env (`:564`).
- Process identity: `setpriv --reuid=<caller> --regid=<caller> --clear-groups` (`INNER` `:97`, `:142`); `identity_ok` requires `[uid, gid, gid]` (`:578-579`). Control C1-K3 (uid-gated) must FAIL and does (battery: `correct 1`).
- Fixture values: every case value is drawn per run (`Draw`, `make_cases`; docstring `:35-36`).
- Name channel: the counter mixes the **host's own live fsids** into the drawn views — `make_cases`'s `sysfs()` takes `live_fsids` from `os.listdir('/sys/fs/btrfs')` at run time and, for the first fsid of a case, picks a real host fsid with probability 1 for `live=True` cases and 1/2 otherwise (`score-scrub-arm-r44.py:353-361`, `:560`). A fix gated on "an fsid that is not this host's" therefore fires identically in the view and in production; control C1-K10 (the real arm only when the host fsid is absent from sysfs) must FAIL and does (`correct 6`, battery-summary-c1).

Reported open channels (printed in the verdict JSON as `channels_open: ["mount table", "uid_map", "script path /mnt/census-lib.sh"]`, `:630`; docstring `:48-50`):

- mount table (`/proc/self/mountinfo` shows the tmpfs roots), uid_map (`/proc/self/uid_map` shows the subuid mapping), script path (the census is sourced from `/mnt/census-lib.sh`). Control C1-K7 (mount-table-gated) is scored as `recorded`, not demanded to FAIL (`run_controls_c1.py:21-22,98`; battery: K7 verdict FAIL via the selftest leg only, behavioural legs green). This is the QUALITY 90 carve-out used as designed: the declaration names the legs and reports the channels open (`SCORECARD.md` round-44 declaration: "C1's namespace legs leave the mount-table, uid_map and script-path channels open (QUALITY 90 'named open')").

### C2 (`tools/check-scrub-record-r44.py`)

Closed (new this round, per docstring `:24-42` and `SCORECARD.md`):

- Verdict-line grammar: the declared line is the JSON `verdict_line` string, or the output's FIRST line with no leading blank and no leading/trailing whitespace; a JSON `verdict` key, when present, must equal the line's verdict word ("a contradiction binds nothing"); the committed report's raw first line must be byte-identical (`:27-31`, `declared_line` `:187-203`, `bound` `:206-225`). Controls C2-K13 (report first line differs), K14 (padded: two leading spaces), K15 (blank-line-prefixed), K16 (JSON `verdict: fails` beside `verdict_line: holds`) all must FAIL and do (each `verdict FAIL`, `verdicts_ok 2`).
- Source-line lead list: the entry's `source:` line must open with the id list containing S237/S240/S242/S243/S244/S245 before any other text — an id named only later in the line's prose does not count (`:335-338`). Control C2-K17 (S244 removed from the lead list) must FAIL and does (`sources.source_line false`, `sources_ok 0`).
- Quote/conf/host/pointer/novelty conjuncts are carried over from rounds 38-43 (QUALITY 79/86/87 and the pointer/novelty rules).

Still accepted (declared, outside the predicate): forged orchestrator records — control C2-K3 (forged dispatch + results + all-holds reports) and C2-K19 (`partly` + bound residual `holds`) are controls that must PASS and do (`verdict PASS`); `transcripts_bound` is reported outside the predicate and cross-checks against host-local omp sessions (`:46-47`). The declaration states this: "The committed-bytes predicate cannot tell forged orchestrator records from real ones (control C2-K3 passes it); transcripts_bound is reported outside the predicate."

## 2. Comparison with QUALITY 82, 85, 87, 88, 89, 90, 92

| Criterion | Round-44 C1 | Round-44 C2 | Covered? |
|---|---|---|---|
| 82 (R32-FIXTURE-GATEABLE): behavioural counter also scores code outside its fixtures; frozen predicate names the views; fixture-gated + cached-live controls | live leg present and named; drawn views run at caller identity inside `unshare -m` + `setpriv` (`:566-567`, `:97`). The "second live view whose expected answer changes per run" is not present (the live answer is walked twice only to detect instability, `:593-604`) — narrower than 82's text, but the declaration does not claim it | n/a (content counter) | mostly; cached-live variant absent (declared by omission) |
| 85 (R38-Q82-LEAK): production-path view built inside the child namespace; no host-resolvable name leads to its content; one arm per channel must score below target | views are built inside the namespace from stdin (`INNER`), no bind-mount source, no `$HOME`/`$TMPDIR` sibling; names are drawn, not host paths — the LEAK channels are closed by construction | n/a | yes (the view is created in-namespace, filled from stdin) |
| 87 (R39-CONTENT-UNREAD): content counter reads the rule cell; pre-data controls include a content-free entry and a one-literal fixture-shape arm | n/a | `prop_ok` reads the statement cell's frozen tokens; content-free entry = C2-K7 (must FAIL, does) | yes |
| 88 (R40-CLAIM-PARAMETERS): acceptance implies the declaration's named content parameters; a control violates exactly one named parameter | selftest parameter = C1-K11 (four of nine `(R44-C1)` labels renamed; must FAIL, does) | row-count/proposition conjuncts exercised by K0-K18 | yes |
| 89 (R41-GUARD-BYPASS): an adversarial guard is scored against the evasion that defeats its own mechanism; a family is closed only by a non-lexical refusal, else reported open | the fixture-gated family's cheapest members (env/uid/name) are armed and refused; the mount-table/uid_map/script-path members are **reported open**, not closed (K7 recorded) | planted-verdict and grammar families are refused (K1-K18); forged-records family reported open (K3 control) | yes, both sides report open families instead of claiming closure |
| 90 (R42-OBSERVED-CHANNEL): no-answer-key counter is scored per observation channel; each channel variant must read below the target OR the leg is named override-free with channels reported open; a verdict binding matches the asserted line, not a mention | channels named per channel (env, identity, fixture values, namespace traces); open traces reported; K7 recorded | verdict binding is the asserted first line / `verdict_line`, with the contradiction check; K6 (mention-not-assertion) must FAIL, does | yes — 90's carve-out is exactly the round-44 practice |
| 92 (R43-CAP-HEADER-DUP): rendered machine-readable tables carry exactly one header row | orthogonal (no new tables in the scored surface) | orthogonal | n/a |

**The gap.** The only pattern this round shows that no existing criterion states as a standing rule is the
*ladder of structural binding*: C2's checks used to be satisfied by substring presence, and the round
tightens each to the exact region — the leading id list of the `source:` line (K17), the first line
before blank/padding (K14/K15), an internally consistent JSON object (K16), the identical report first
line (K13). QUALITY 90's second sentence covers the asserted-verdict-line case only ("never a substring
that a disputing sentence may quote"); QUALITY 86 requires every cited S-id to be *named on* the
`source:` line, but not that it sit in the leading list. Nothing requires (a) region-exact binding for
every structured carrier and (b) a pre-data battery with the *shift* of the same content into each
neighbouring region (id later in prose, verdict on the second line or padded/blank-prefixed, a
contradictory JSON key). A presence-only control (delete the content) does not exercise a shift.
Round 44 demonstrates such controls are cheap and closable (K13-K17), and the round-42 D1 shows the
unshifted family really was a live failure mode.

## 3. Proposed criterion (exact text)

> 93. **A structural check binds its match to the exact region the definition names, and the pre-data
> battery includes a shift of the same content to every neighbouring region of the same carrier
> (R44-REGION-BINDING):** a check that reads a structured carrier — a knowledge entry's `source:`
> line, a verdict line, a report's first line, a machine-grammar `key=value` line — is satisfied only
> by the content in the named region: the leading id list before any other text, the first line before
> any blank or leading/trailing whitespace, the asserted verdict line in the committed report, the
> validated token slot. The same content elsewhere in the carrier — an id later in the line's prose, a
> verdict line preceded by a blank line or indented, a sentence that merely quotes the verdict, a JSON
> `verdict` key contradicting the `verdict_line` — never satisfies the check. The frozen pre-data
> controls include, for each named region, a variant that keeps the content and shifts it to a
> neighbouring region of the same carrier, each of which must read below the target; a control that
> deletes the content outright does not close a shift, and where a shifted variant is not refused the
> region's closure is reported open. Failing example: the round-42 C2 counter matched
> `ROW SC<n> VERDICT:` anywhere in the output and report, so a critic's sentence quoting the holds line
> counted as `holds` (`.ufo/waves/round-42/w1/C2CritControl.md` D1); the round-38 echo of a raw
> `devinfo` basename into `detail=` was the corresponding machine-grammar violation (QUALITY 84).
> Shown able to fail: the round-44 C2 counter refuses a report first line differing from the bound line
> (control C2-K13), a padded verdict line (C2-K14), a blank-line-prefixed verdict (C2-K15), a JSON
> object whose `verdict` key contradicts its `verdict_line` (C2-K16), and an id moved out of the
> leading `source:` id list (C2-K17, `sources.source_line` false), with `should_fail_accepted 0`
> (`.ufo/waves/round-44/controls/battery-summary-c2.jsonl`, `run_controls_c2.py`). Lesson:
> `corpus/lessons/round-44.md` (to be written at integration; drafted by wave-1 seat ConnClaims; the
> round-44 C2 binding closes the two round-43 binding gaps and sharpens QUALITY 86's source-line
> requirement and QUALITY 90's asserted-line rule; the round-44 C1 counter closes the fixture-name
> channel by mixing the host's own fsids into drawn views, control C1-K10).

Notes for adoption:

- The criterion's failing example is historical (round 42 D1), as required: this round's K13-K17 are
  already refused, so they serve as the "shown able to fail" demonstration of the family, not as a
  defect.
- The committed C2-K17 variant deletes the first ` S244` token from the `source:` line (the lead
  list), i.e. it exercises the deletion form of the shift; the declared intent covers the prose form
  (id present later in the same line). Both forms fail the counter's lead-list regex
  (`^source:\s*((?:S\d{3,}[\s,]*)+)`), so the control family is sound; if adopted, the battery may
  add the prose-form variant as a second member.
- No new criterion is proposed for the reported-open channels (C1 mount-table/uid_map/script-path; C2
  forged records): QUALITY 90's "named override-free leg, channels reported open" carve-out and the
  declared `transcripts_bound` reporting already govern them, and the forged-records limit is an
  environmental property of commit-based verification that no lane counter can remove.

## 4. Risks and boundaries of the proposal

- Risk of overlap with QUALITY 90's tail if read too broadly: the criterion is scoped to *any
  structured carrier* and adds the *shift-control battery* requirement, which 90 does not state for
  non-verdict carriers. It should be adopted as an extension, not a replacement.
- The criterion touches the verification surface of the C2 depth claim (its counter already passes the
  demonstrated controls) and would bind future counters to carry shift controls; it does not change the
  declared axes or the C1/C2 predicates.
- I did not run the counters or the batteries; every claim above cites a committed file or receipt
  (path:line, or the control JSONL result lines).
