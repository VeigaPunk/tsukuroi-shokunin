VERDICT: defect-found

# GRevCounterB — second admission-rule review of the r48 C2 counter

Scope: is `>= 3 credited holds seats, both roles, distinct bodies, no blocking negative`
the right rule for a row, exercised against the frozen counter
`tools/check-scrub-admission-r48.py` (blob at ae99f021 = live working-tree bytes,
sha256 eab290589fe2a8d3e900d41891bee688dd36250928aa93678b68cad5895284d4,
verified 2026-10-28). Method: 15 sandbox fixtures, each a `git clone --shared` of the
lane checked out at BASE 5fdf062f (section hashes there equal the frozen GR hashes —
`counter.py --section-hash` receipt below), marks appended, a synthetic w2 cohort
committed, and the frozen counter run per fixture. Driver + per-case receipts:
`.ufo/waves/round-48/w2/GRevCounterB/drive.py`, `.../cases.jsonl`,
`.../counter.py` (byte-identical copy of the frozen counter). All clones lived under
`/fast/scratch/hyaku/tsukuroi-r48/GRevCounterB/fx/`; lane tree untouched.

## Bottom line on the rule

The rule itself is right for a grounding row and the counter implements it
faithfully for well-formed reports: a row is admitted only on `>=3` credited seats
spanning both roles with pairwise-distinct bodies and **zero** negative verdicts
bound to the current section hash. Zero dissent is the correct threshold here (a
`partly` from a seat that measured the same bytes is evidence against the row; a
majority rule would admit rows a counted seat found defective). The defects found
are all in the **negative-binding layer**: *which* seat reports the counter treats
as a negative at all. None of them weaken a real `holds` cohort this wave.

## Case answers (all reproduced; `cases.jsonl`)

- **5 holds + 1 `partly` on a wrong (stale but well-formed) hash** → row admitted
  (A1, PASS). The stale-hash negative is ignored, per A2's "on the CURRENT row hash"
  wording. Correct as specified — but see F1: the *other* negative word on the same
  stale hash is **not** ignored.
- **3 critics hold + 3 reviewers `partly` (current hash)** → row blocked (B, FAIL;
  `blocking=[R48RevGR2a,b,c]`, `verdicts_ok 2`). Double-locked: also fails the
  both-roles conjunct. Correct.
- **`holds` on line 1, prose says the row fails** → credited, row admitted (C1,
  PASS). True to the documented contract: only line 1 and later structured
  `ROW GR<n> VERDICT:` lines are read. A *structured* contradiction is caught and
  fails closed (C2 → seat converted to `partly`, row blocked, FAIL). Prose is not —
  documented limit, see F5 note.
- **Marks at base**: confirmed by direct read — base entry carries only
  `## Gate status — round 45`/`round 46` lines; base README's scrub lines are either
  negated ("pending, not admitted", corpus/README.md:466) or lack `admitted round 48`
  (line 460); SKILL.md has `## Scrub grounding — round 45 rows`, not `round 48
  admission`. No pre-existing line satisfies a mark; consistent with K0 marks_ok 0.
  The marks are round-48-specific. But see F4 for a vocabulary gap in the negation
  guard.

## Demonstrated findings (all routed to next round; counter is frozen for scoring)

**F1 — `fails` and `partly` have different stale-hash semantics; a `fails` on a
malformed hash vanishes while a `fails` on a stale hash vetoes.** `blocking`
(counter:341) requires `hash == cur`, but `any_fails` (counter:342) ignores the
hash entirely, and a non-hex line 2 fails `HASH_RE.fullmatch` (counter:78,202) so
the seat unbinds before either check. Reproduced: `fails`+stale-hex hash → row
blocked (A1b FAIL); `fails`+`SECTION SHA256: zzzz-not-hex` → seat silently dropped,
row admitted on 5 holds (A1c PASS); `partly`+stale hash → ignored, admitted (A1
PASS). So a negative seat's veto power depends on the hex well-formedness of line
2, not on what it measured; the direction is also backwards — garbage
(unverifiable) loses the veto that a correct-format-but-wrong hash keeps.
Proposed change (next round): when line 1 parses but line 2 does not, bind the
seat with hash `None` and treat any negative (`partly`/`fails`) from such a seat
exactly like a stale-hash negative — i.e. route `fails` through `blocking` with
`hash == cur` like `partly`, or keep the stricter `fails` veto but apply it
uniformly to malformed hashes too. Pick one rule per verdict class and document it.

**F2 — veto by omission: a bound `fails` seat is erased by not appearing exactly
once in w2-dispatch.json or w2-results.json.** `bind` returns unbound for
`dispatched 0 times` and for `dispatched 2 times` (counter:175-181) and for
`not exactly one results entry` (counter:189-190); an unbound seat's file is never
read, so its `fails` never reaches `blocking` or `any_fails`. Reproduced three
ways, all PASS with a live `fails` report file on disk: seat absent from dispatch
tasks (E1), seat present twice (E2), seat absent from results (E3). An integrator
who dislikes a seat's negative erases it with a one-line artifact edit — the
counter cannot distinguish "seat never ran" from "seat ran and was struck from the
record". Proposed change (next round): read the report FILE for every name in the
universe regardless of dispatch bookkeeping; a parseable negative line 1 (+ current
hash) blocks even for a seat the artifacts forgot. Dispatch/results uniqueness
should gate *credit*, not *dissent*.

**F3 — an unlisted verdict word unbinds the seat; `rejects` is silently dropped.**
`VERDICT_RE` (counter:76) is closed over `holds|partly|fails`; line 1 `ROW GR1
VERDICT: rejects` fails `fullmatch` → unbound → ignored (C3, PASS). Any negative
word outside the trio — `fails on GR1`, `blocks`, `rejects` — is a dissent the
counter cannot see. Proposed change (next round): parse line 1 with
`ROW (GR\d) VERDICT: (\w+)` and map `{holds}` to credit, everything else to a
negative (fail-closed), or whitelist-check the word and bind an unknown word as
`partly` for its row.

**F4 — README negation guard has a vocabulary gap.** `NEGATE_RE` (counter:75)
covers `unadmitted|not admitted|never admitted|stay(s)? pending` but not
`not yet admitted`, `pending` alone, `admission withheld`, `rejected`.
Reproduced: README line `- btrfs-scrub-grounding-r45.md review pending; not yet
admitted round 48` satisfies the readme mark and the whole counter PASSes (D,
`marks_ok 3`). The mark leg is cosmetic (it cannot rescue a failed verdicts leg —
K1), but an honestly-negating README can still earn the mark. Proposed change
(next round): extend NEGATE_RE with `not yet admitted|pending\b|withheld|rejected|
stays? (?:open|pending)` — or invert to a positive form check, e.g. require the
line to match `- .*btrfs-scrub-grounding-r45\.md.*\badmitted round 48\b` and also
not match an explicit `pending|withheld|unadmitted|not admitted|rejected` list.

## Behavioral notes for seat authors (not defects)

- A `holds` body's every `file.ext:N` token is checked against pinned snapshots;
  `notes.txt:3` or `check-scrub-admission-r48.py:120` in a report uncredits the
  seat (G: `unbound_for_citation: R48RevGR3a: notes.txt not a pinned snapshot
  file`; row still passed on 5). Avoid bare `name.ext:N` strings for unpinned
  files; cite as "tools/… at line N" instead.
- Any later `ROW GR<n> VERDICT: <word>` line — for a *different* row, or a
  different word for the same row, even inside quoted material — converts the seat
  to `partly` (counter:207-210). Fail-closed, but seats must never quote another
  row's verdict block verbatim.
- Results-entry fields other than `name`/`agent` are ignored (counter:189-190):
  an entry with `output: "ERROR: seat stopped"` still binds if the file parses
  (F, PASS). The fleet's results schema has no status field the counter could
  check (r47 w1-results entries: `name/agent/output/note`, all `note: null`); a
  stale file left by a crashed seat would credit. Acceptable for this wave; note
  for artifact review.
- `>=3` credited is the exact boundary: 3 current-hash holds + 3 stale-hash holds
  admits a row (only 3 credited needed); 2 current + 4 stale fails it (A2, FAIL).
- A `partly`/`fails` seat with clean citations still blocks via `blocking`
  regardless of its citation quality — a citation slip cannot launder a negative
  (A2/K3 verified by the frozen battery; not re-disputed here).

## What was not done

- Did not re-run the frozen control battery (its receipts are at
  `.ufo/waves/round-48/controls/battery-summary-r48-c2.jsonl`; all 13 cases
  `as_expected: true` there, incl. K3c contradicting-report and K3d thin `fails`).
- Did not judge whether prose-level contradiction parsing *should* exist (F5/C1
  is a contract limit, reported as such).
- Did not test JSON-level corruption of dispatch/results beyond count edits
  (`load_obj` duplicate-key / non-dict paths also unbind seats silently — same
  class as F2, untested variant).
- LSP review not applicable (single Python file, no server on this host was
  consulted; review was by direct read + sandbox reproduction).
- `lsp` device: not used; no LSP server is configured for this lane, so all
  checks are reproductions on sandbox clones plus direct source reads — no
  grep-based semantic claims.

All findings are routed to next round; the frozen counter stands for round-48
scoring as specified.
