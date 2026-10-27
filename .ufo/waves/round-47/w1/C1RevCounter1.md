VERDICT: defect-found

Seat C1RevCounter1, item C1-R1: review of the frozen counter `tools/check-scrub-admission-r47.py`
(sha256 e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b, matches
`git show 77e9e2b2e96b85d8f048ae2087e246a542b71611:tools/check-scrub-admission-r47.py | sha256sum` — verified)
against its docstring and `SCORECARD.md` "Round 47 — declaration" C1 row.

Axes named for this pass: (1) predicate/declaration fidelity (code vs docstring vs receipt labels);
(2) binding-hole coverage beyond the battery (each hole the item lists, scored in a fixture clone);
(3) live-byte impact (what the frozen counter does to the w1 reports as they stand);
(4) reproducibility (every score is a committed variant in a scratch clone, receipts below).

Fixture method: `git clone -q --shared` of the lane under
/fast/scratch/hyaku/tsukuroi-r47/C1RevCounter1/fx.0RSFOH, origin removed, toplevel verified, checked
out at the impl freeze 77e9e2b2e96b85d8f048ae2087e246a542b71611, one commit per variant, scored with
the frozen counter itself (`--lane <clone> --revision <sha>`). Driver and all receipts are copied to
`.ufo/waves/round-47/w1/C1RevCounter1/` (driver.py, receipt-E1..E11, receipt-live-scan.txt,
receipt-livefull-counter.json, live-citation-fails.txt).

FINDINGS

F1 (high, live impact) — the seat-citation leg tokenizes every `word.ext:N` in a report body and
requires each to resolve against the C1 pinned snapshot set; honest, digest-verified citations and
verbatim-quoted capture lines fail binding, and the row then fails through the distinct-bodies leg.
  Code: CITE_RE `tools/check-scrub-admission-r47.py:83`;
  verify_citation `:241-248` (fname absent from the pinned map -> False, "not a pinned snapshot file");
  report_citations_ok `:286-292` (returns on first failure);
  wired in run() around `:346-351` (a citation failure keeps the seat out of `bodies` while it still
  counts in `on_cur`), so `distinct` at `:352` goes False and the row fails at `:354`.
  K22's docstring intent (:23-25) reads "cited file:line locations must resolve" — implemented far
  broader: ANY `word.ext:N` token, including paths inside quoted evidence.
  Live evidence (scan 2026-10-27T06:05:59-03:00, receipt-live-scan.txt): 6 of 17 live counted reports
  currently fail this leg —
    - R47CritGR2a.md:21, R47ResRevGR2.md:93, R47RevGR2a.md:10-11, R47RevGR2b.md:9 cite
      `S240 ioctl.c:3190` — a real round-43 frozen snapshot whose sha256 the seats verified, but S240
      is not in this counter's SNAPSHOTS map (`:44-70`); the regex hits `ioctl.c:3190`.
    - R47RevGR3a.md:28 and R47RevGR3b.md:19 quote capture.txt:4 verbatim; its text embeds
      `/etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`; the regex hits
      `10-faster-shutdown.conf:2` — a config path, not a citation (live-citation-fails.txt).
  End-to-end: fixture at the impl freeze + the 17 live reports + all three marks -> counter verdict
  FAIL, GR2 row_ok=False, GR3 row_ok=False (receipt-livefull-counter.json).
  Mechanism repro: receipt-E4.json (one embedded drop-in path in one GR3 critic report ->
  citations_ok=False and, via the on_cur/bodies coupling, distinct_bodies=False -> whole C1 FAILs).
  Corroboration: w1/R47CritGR3a.md as first read (05:54) carried the colon form and was edited at
  05:56 to "`10-faster-shutdown.conf` line 2 … so the report carries no pseudo-citation" (current
  line 32) — a counted seat already had to self-censor verbatim evidence against this leg.
  Constraint: the counter is frozen for the round, so the actionable path is on report bytes — every
  `word.ext:N` token in a counted report must name one of the pinned files (scrub.c, sysfs.c,
  cmdline.c, vsprintf.c, kstrtox.c, dev-replace.c, systemd.kill.xml, btrfs-scrub@.service,
  capture.txt) at an existing line; GR2 seats must reword the S240 ioctl citation accordingly.

F2 (medium) — the README negation filter has phrasing gaps; "not yet admitted" earns the mark.
  NEGATE_RE `:78` = unadmitted|not admitted|never admitted|stay pending|stays pending — no `yet`,
  case-sensitive, no hyphenated `un-admitted`. The readme mark `:370-371` grants on both substrings
  (`btrfs-scrub-grounding-r45.md`, `admitted round 47`) plus the filter. Fixture E5: README line
  "- `corpus/knowledge/btrfs-scrub-grounding-r45.md` not yet admitted round 47" ->
  marks.readme=True, verdict PASS (receipt-E5.json). The docstring's F2 claim ("rejects lines
  carrying an explicit negation of admission", `:16-17`) is stronger than the code.

F3 (medium) — K23 distinct-bodies compares exact bytes; whitespace-normalized identical reports evade.
  bodies are sha256'd raw (`:346-350`, hash at `:352`). Fixture E2: two seats per row with bodies
  identical except double-vs-single spaces -> distinct_bodies=True, verdict PASS (receipt-E2.json).
  Within the declaration's letter ("byte-identical") but weaker than the wave finding's anti-copy intent.

F4 (low-medium) — quorum has no role diversity; two same-role seats satisfy the row.
  run() `:354` requires len(on_cur) >= 2 and all 'holds', never a critic. Fixture E3: GR1 bound only
  by R47RevGR1a + R47RevGR1b (zero critics) -> row_ok=True, verdict PASS (receipt-E3.json). The
  declaration's universe is "two reviewers and two critics"; the counting rule never enforces mix.

F5 (low) — diagnostics conflation: a citation-failed bound seat inflates bound_on_current while
  bodies undercount, surfacing as distinct_bodies=False rather than the actual citation failure.
  `:344-356`; visible in receipt-E4.json and receipt-E10.json. citation_problems carries the true
  reason (mitigating).

F6 (low, doc) — the docstring (`:1-35`) never states the predicate sentence. PREDICATE `:84`
  equals the SCORECARD declaration verbatim and is emitted as the JSON `predicate` field (observed),
  so code and receipt labels agree; only the docstring side of the item's "same sentence in code,
  docstring, receipt labels" is missing.

HOLES LISTED IN THE ITEM, SCORED — ALL FAIL CLOSED OR SOUND (no defect)

- Seat binding without a spawn: results entry + report for an undispatched seat -> not bound
  (receipt-E7.json; bind `:182-186` requires exactly one dispatch hit).
- Duplicate JSON keys: no_dups `:99-105` via load_obj `:117-124` poisons the whole dispatch file ->
  all its seats unbound (receipt-E8.json); deep-nesting parse failure degrades in-band per F3
  (battery-summary-r47.jsonl C1-F3a).
- Same seat dispatched in two waves -> "dispatched 2 times", unbound (receipt-E9.json).
- Report-path traversal: wave name `..` (`..-dispatch.json`) looks up the literal tree path
  round-47/../<seat>.md, which git does not normalize -> "no report ../R47RevGR1a.md", fails closed
  (receipt-E6.json). Git tree entry names cannot contain `/`, bounding the interpolation at
  bind `:214`.
- Snapshot map: digests re-checked at REV `:229-239`; a tampered/moved snapshot drops out and every
  quote citing it fails (receipt-E10.json, quotes_ok 2). Quotes verify against the exact (sid, file)
  key — a wrong-sid quote mismatches (receipt-E11.txt). No wrong-file or slipped-pin path found.
- Exact-line marks: MARK_ENTRY/MARK_SKILL are full-line membership tests `:368-369` (fail closed on
  trailing whitespace; battery F2a).
- Universe of seat names: hardcoded exact list `:87-92`, exact == match against dispatch tasks
  (`:188`); role enforced at `:196-197`; no regex surface.
- Predicate: code `:84`, JSON output field, and declaration are identical; exit codes 0/1/2 and the
  base-ancestor gate `:320-323` behave as declared (E1 rc=0 PASS; deadbeef revision -> in-band error).

RESIDUAL RISK AND VERIFICATION GAPS

- "Verdict bound to unread bytes" is inherent to the trust model: the section sha256 binds the
  verdict to the bytes but is copyable; distinct-bodies (F3) is the only anti-copy leg. No counter
  change short of an out-of-band reading proof would close it; not closed.
- Wave names are arbitrary (no whitelist): any committed `<name>-dispatch.json` + matching
  `-results.json` pair counts — declaration-sanctioned ("every committed round-47 wave's seats
  count"), noted for completeness.
- Seat citations resolve by filename across ANY pinned version with line-existence only (no content
  check): `scrub.c:100` resolves via S237 even if the seat meant S242. As designed ("an existing
  line"), noted.
- Live reports were still being written by running peers; the live scan is a 2026-10-27T06:05:59
  snapshot and the end-to-end livefull score reflects those bytes. The verdict impact of F1 depends
  on the final committed report bytes.
- Not run (out of item scope): the C2 census selftest (30-50 s, C2 seat's domain); LSP-based
  reference checks (no server configured for this lane; all checks executed the frozen counter
  directly against fixture commits instead).

Receipts: `.ufo/waves/round-47/w1/C1RevCounter1/` (driver.py + receipt-E1..E11 + live scan +
livefull counter output + live-citation-fails.txt).
