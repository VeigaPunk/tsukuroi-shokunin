VERDICT: defect-found

Item C1-R2: review of the frozen counter tools/check-scrub-admission-r47.py (sha256
e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b, verified identical to the
freeze revision 77e9e2b2e96b85d8f048ae2087e246a542b71611) against its docstring and the
SCORECARD.md "Round 47 — declaration" C1 row.

Every leg was exercised both as code review and by scoring fixture-variant commits in shared
clones (git clone -q --shared, origin removed, toplevel asserted, committed as fixture/fixture,
counter run with --lane "$D" --revision <sha>). Full JSON of all 13 scored variants:
.ufo/waves/round-47/w1/C1RevCounter2/fixture-outcomes.json; static transcripts:
.ufo/waves/round-47/w1/C1RevCounter2/static-checks.txt. Receipts are the two files in that seat
dir; scratch was removed after scoring.

== Predicate and leg-label consistency (positive) ==

- The counting sentence is byte-identical in the three required places: PREDICATE at
  tools/check-scrub-admission-r47.py:84, the docstring ("Output: one JSON line; exit 0 PASS…"),
  and the SCORECARD C1 row ("predicate structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3
  and marks_ok == 3"); the receipt re-emits it as the 'predicate' field (:376) and the final gate
  is exactly that sentence (:373).
- Docstring legs map to code and behave as declared under the kill variants:
  F1 -> row_extent (:131-148) + section_hashes (:150-157); F2 -> marks (:368-372);
  F3 -> load_obj/no_dups (:112-125) with every parse failure surfaced in-band as a seat reason;
  K22 -> quote_legs (:251-271) for entry Quote lines and verify_citation (:241-248) +
  report_citations_ok (:286-296) for seat-report citations; K23 -> the distinct-bodies leg (:352).
- Exit map verified live: 0 PASS / 1 FAIL / 2 usage-or-read-error (missing --revision -> 2;
  unresolvable revision -> 2; counter at base -> 1 with structural_ok=1 quotes_ok=3 verdicts_ok=0
  marks_ok=0, matching the declaration's "before" row).
- Battery coverage is real but narrow: 12/12 as expected in controls/battery-summary-r47.jsonl;
  my two findings below are NOT among its cases.

== Findings (each: what the item asked, what the counter does, the scored repro) ==

F1 (defect, HIGH) — F2's README negation leg under-delivers: an explicit negation outside the
   five frozen phrases earns full mark credit, up to overall PASS.
   tools/check-scrub-admission-r47.py:78 NEGATE_RE =
   re.compile(r'unadmitted|not admitted|never admitted|stay pending|stays pending')
   tools/check-scrub-admission-r47.py:370-371 readme credit =
   any(all(x in ln for x in MARK_README) and not NEGATE_RE.search(ln) for ln in readme_lines)
   The declaration says "F2: marks pinned exact / negation-rejecting" and the docstring says "the
   README mark rejects lines carrying an explicit negation of admission". The implementation
   rejects only those five phrases. A README line such as
   "- `corpus/knowledge/btrfs-scrub-grounding-r45.md` admitted round 47 (admission withheld —
   pending operator countersign; do not treat as landed)" carries both required substrings and an
   explicit negation ("withheld", "do not treat as landed") that NEGATE_RE never sees.
   Scored repro (fixture s2-f2-readme-withheld, full candidate with all six counted seats
   binding 'holds' on current bytes): counter returned rc=0 verdict=PASS with
   marks={'entry': True, 'readme': True, 'skill': True}, marks_ok=3. The battery's F2a only tries
   "remains unadmitted round 47" (caught: 'unadmitted') and the SKILL "(WITHHELD — rows stay
   pending)" variant (caught by the exact-line SKILL leg, control s3: marks.skill=False). The
   README-withheld shape is uncovered. Impact: a negating README admission sentence can
   contribute the third mark toward a round PASS; the mark leg needs a wider negation class or
   exact-line pinning like SKILL/entry.

F2 (defect, MEDIUM) — K23 catches byte-identity only; whitespace-normalized-identical bodies
   bind as distinct, and the full predicate passes on them.
   tools/check-scrub-admission-r47.py:348 bodies.append(hashlib.sha256(body.encode()).hexdigest())
   tools/check-scrub-admission-r47.py:352 distinct = len(set(bodies)) == len(bodies) == len(on_cur)
   The item asked explicitly whether whitespace-normalized identical content is caught: it is
   not. Two reports whose bodies are ' '.join(split())-equal but byte-distinct (spacing/blank-line
   padding) hash differently and pass K23. Scored repro (fixture s1-k23-whitespace-identical):
   all three rows bound with two such bodies each; counter returned rc=0 verdict=PASS with
   per_row GR1 distinct_bodies=True. The declaration says "not byte-identical", so the code is
   letter-compliant, but the anti-collusion intent ("the counted seats bound for a row must not
   be identical") is defeated by trivial re-padding — one analysis, two bindings. Recommend
   normalizing whitespace before hashing bodies.

F3 (gap, LOW, fail-closed but strictness loss) — seat-side citation verification is
   content-free and generation-ambiguous; some citation shapes evade it entirely.
   tools/check-scrub-admission-r47.py:83 CITE_RE = r'\b([A-Za-z0-9_.@+-]+\.[a-z0-9]+):(\d+)\b'
   tools/check-scrub-admission-r47.py:241-248 verify_citation resolves fname against ALL pinned
   snapshots carrying that filename, checking only 1 <= lineno <= len(lines).
   Consequences: (a) scrub.c is pinned in both S237 (2231 lines) and S242 (3337 lines), so a seat
   citing "scrub.c:3000" resolves via S242 even if the author's text was mined from S237 — no sid
   is required on the seat side and no quote-text check anchors it (weaker than entry-side K22,
   though exactly what the declaration's "must resolve" demands); (b) CITE_RE only matches
   lowercase extensions and a clean word boundary after the digits, so "scrub.C:12" or "scrub.c:12x"
   are not checked at all; (c) any incidental file:line mention of a non-pinned file (e.g.
   "tsukuroi-census.sh:2377") breaks binding (fixture s8 -> seat unbound, row falls to one bound
   seat -> FAIL), which is fail-closed but a sharp edge for honest seats. Reported as residual
   risk, not a leg violation.

== Item-listed binding holes checked and CLOSED (controls, all scored with the frozen counter) ==

- Seat binding without a spawn: impossible. bind (:178-226) requires exactly one dispatch task
  (:188-192, else 'dispatched N times'), a readable {wave}-results.json with exactly one
  (name, agent) entry (:196-201), and a present report (:202-204). Control s5 (reports+results,
  dispatch deleted): all seats 'dispatched 0 times', verdicts_ok=0. Live at lane tip: every
  counted seat reads 'w1-results.json unreadable' until the wave commits its results file.
- Verdict bound to unread bytes: impossible. The bound hash is compared against hashes[row]
  computed from the same revision's entry bytes (:343, :349-350); an unresolvable --revision
  exits 2 before any verdict (:312-316). Controls s6 (a 'fails' verdict on stale base bytes):
  any_fails (:351) sinks GR2 to row_ok=False even with two current 'holds' bound.
- Quorum by one seat: impossible. :354 requires len(on_cur) >= 2, all bound verdicts 'holds',
  and no 'fails' anywhere in the universe. Control s4 (one seat per row): verdicts_ok=0.
- Wave-name dependency: seats bind only via *-dispatch.json under .ufo/waves/round-47
  (:47, :167-176); a dispatch under any other name is invisible (control s12: waves_seen=[],
  verdicts_ok=0). Fail-closed and matches "every committed round-47 wave's seats count"; noted
  because the file-naming convention is now part of the trusted contract.
- Duplicate JSON keys: load_obj (:112-125) wires object_pairs_hook=no_dups for both dispatch and
  results files; a duplicate key raises DupKey -> None -> seat unbound. Control s7: verdicts_ok=0.
- Report-path traversal: closed by construction. Seat names come from the frozen universe()
  (:88-93); the wave stem is a flat git tree-entry name (no '/'), so the constructed path
  f'{WAVES}/{wave}/{seat}.md' stays under WAVES; and git treats '..' literally in rev:path
  lookups — `git show 'HEAD:.ufo/waves/round-47/../round-47/w1-dispatch.json'` is rejected
  (transcript in static-checks.txt).
- Snapshot map integrity: quotes key strictly on (sid, fname) (:270-271), so a quote can only
  verify against the snapshot it names; a moved or tampered snapshot fails the digest at
  snapshots() (:232-237) and drops out of the cache, failing every quote that cites it closed
  (control s11: S246 sysfs.c quote -> quotes_ok=2). No wrong-file verification is possible.
- Exact-line marks: SKILL and entry marks are whole-line equality (:368-369); control s3 shows a
  suffixed SKILL line earns nothing (marks.skill=False). Entry mark placed inside a row extent
  is caught by F1 instead (control s13: structural_ok=0) — the legs compose safely.
- Distinct-body rule: byte-distinctness is enforced and identical bodies fail (battery K23a);
  the whitespace bypass is finding F2 above.
- Universe of seat names: fixed at 8 seats per row (:87-92) covering two reviewers, two critics,
  and both residual generations; the committed w1 dispatch contains exactly the 18 round-47
  counted seats with correct reviewer/critic roles and no duplicate names (checked live); the
  held R47Res2* generation is undispatched as declared.
- In-report contradiction: ANY_VERDICT_RE (:218-220) rejects a report whose body carries any
   second ROW verdict line that differs from line 1 (control s9: seat unbound).
- Role binding: dispatch agent and results agent must both equal the seat's frozen role
  (:194-195, :200-201); control s10 (results agent 'executor') -> 'not exactly one results
  entry'.

== Residual risk (not defects; the counter's contract is committed bytes) ==

1. The counter cannot prove a spawn occurred or that two seats are different authors/agents —
   dispatch and results JSONs are trusted as committed evidence. Quorum >=2 plus K23 raises the
   cost of fabrication but cannot exclude an L1 authoring two distinct reports. In-contract.
2. "Marks written only after the counted seats bind" has no temporal dimension at one revision;
   the counter checks presence only. In-contract, but ordering discipline is an L1 procedure.
3. The results entry's payload fields are not cross-checked against the report's verdict line;
   the bound verdict is the report's first line per the declaration. Orchestrator/results
   contradictions would be invisible to this counter.

== What I did not do ==

- Did not re-run the 12-control battery (cost/serialization rule; its summary is committed and
  read: 12/12 as expected).
- Did not mutate the lane, the fleet repo, the host, or any PATH directory; all fixture clones
  lived under /fast/scratch/hyaku/tsukuroi-r47/C1RevCounter2 and were removed after receipts
  were copied (trap 'rm -rf -- "$S"' semantics applied manually; /tmp never used).
