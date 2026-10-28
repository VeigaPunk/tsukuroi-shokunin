VERDICT: defect-found

Seat: R50CritCounterDiff — item D-11, attack the three counter diffs (C1, C3, C2)
Freeze: 8029cdba1049df25632c91a23c8db4eefb54be5f. Prior tip: b866a1d3d26616119a089f1a69b080136becc17b.
Receipts: .ufo/waves/round-50/w1/R50CritCounterDiff/

Axes attacked (what each hunk could do): (a) measurement fidelity — does a leg still
measure what its name/docstring says; (b) provenance/identity — does the report name
the instrument that produced it; (c) discrimination — can it fail the thing it was
built to fail; (d) dead weight — code that runs and reports but decides nothing;
(e) hermeticity — does the verdict depend on state outside REV.

STRUCTURE NOTE (diff basis). `git diff` on each pair is not a modification: the three
r49 files are byte-identical at both revisions (diffstat for the r49 paths is 0 lines;
receipt d_stat.txt). The r50 files are NEW files (C1 +475, C3 +393 insertions). Both
generations coexist at the freeze: `tools/check-scrub-admission-r49.py` and
`tools/check-adjacency-table-r49.py` still exist at 8029cdba and still pass a stub
(receipt c3-r49-stub.json). So "the diff" is a semantic delta between two independent
programs; I compare them function-for-function below.

======================================================================
FILE 1: tools/check-scrub-admission-r50.py  (C1; frozen +475)
======================================================================
Line numbers refer to the frozen r50 file.

Leg-by-leg (r49 -> r50):
- L9-20 docstring: declares the repairs. Line 19-20 claims "compares whitespace-collapsed
  bodies, so padding a copy is not a distinct body". The implementation does NOT
  collapse whitespace — see D-C1-3.
- L62 BASE b866a1d3... (was 6256760d...): re-anchors the base check. Reporting/anchor.
- L96-98 MARK_* round 49->50, WAVES round-50 (L66): measurement, declared.
- L107-118 CORR49_REQ/CORR49_FORBID added, wired at L396-399 (re.M on REQ only):
  measures MORE (4 required, 3 forbidden). Tightens, no loosening. Keep.
- L121-133 LANE_FILES added (8 names): the routed repair — loosens the citation leg.
  The loosening is bounded by L298 (>=2 distinct row-source files). See D-C1-1, D-C1-2.
- L273-289 verify_citation + LANE_FILES branch. Two defects in the repaired code
  (D-C1-1, D-C1-2).
- L292-304 report_citations_ok: requires >=2 distinct CITE[row] files (was >=1 via
  `any(...)`). STRICTER. Keep.
- L298: every `file:line` hit must resolve — still all-or-nothing, so a prose citation
  of any file outside the 8-name allowlist voids the seat. Same over-refusal class the
  routed defect named; partial repair.
- L426-427 distinct-bodies normalization: replaces raw-body sha256 with a normalized
  sha256. Incompletely repairs the routed defect (D-C1-3) and the docstring mis-describes it.
- L437 `'counter': 'check-scrub-admission-r49'` in the r50 file — provenance defect
  (D-C1-4). Line 469's error path correctly says r50: internal inconsistency.
- L360 marks_leg(entry, skill, readme, hashes): `hashes` is never read in the body —
  dead parameter carried from r49 (D-C1-5).
- L313-317 + L462 + L400: --dispatch-file control override, matches docstring line 21. Fine.
- Dead weight check (AST): no unused module-level defs/names other than the
  marks_leg parameter (receipt: scan printed []).

Defects (measured, not argued):
  D-C1-1  Citation leg contradicts its documented rule for multi-candidate names.
    Docstring L119-120: "the first one that exists at REV and covers the line wins."
    Impl L279-287 returns False on the FIRST existing path even when it does NOT cover
    the line, and never tries later candidates. Executed (fake show(): round-45 file
    has 41 lines, round-44 file has 200): `verify_citation({}, 'SHA256SUMS', 120, ...)`
    -> (False, 'SHA256SUMS:120 outside .ufo/waves/round-45/frozen/src/SHA256SUMS (41
    lines)'). A real citation that resolves under the documented rule is refused.
    Fix: `continue` instead of `return False` at L287, keeping the last why-string.
  D-C1-2  Digest bypass for names that are both snapshots and LANE_FILES.
    `capture.txt` is a pinned snapshot (S249) AND a LANE_FILES entry (L132). L274 only
    falls through to LANE_FILES when `cands` is empty — i.e. also when the digest
    moved. Executed: `verify_citation({}, 'capture.txt', 5, ...)` with an empty
    snapshot cache -> (True, 'resolves in .ufo/waves/round-45/frozen/hostcap/capture.txt').
    So a moved S249 digest is silently forgiven for that name while `quote_legs` still
    counts it bad. Smallest correction: distinguish "known snapshot name, digest moved"
    from "not a snapshot name" and refuse the former.
  D-C1-3  Distinct-bodies leg only repairs half the routed defect.
    Impl L426-427 does `'\n'.join(ln.rstrip() for ln in body.split('\n') if ln.strip())`
    — rstrips and drops blank lines, does NOT collapse whitespace. Executed: a copy
    with every non-blank line prefixed by a space yields a DIFFERENT sha256 (dfa5f99c...
    -> 113ce1cc...), i.e. it is credited as a distinct body; trailing-space padding is
    collapsed. Routed defect ("padding a copy is not a distinct body") is half
    repaired, and docstring L19-20 says "whitespace-collapsed" — false. Smallest
    correction: normalize with `' '.join(body.split())` or `re.sub(r'\s+', ' ', body)`.
  D-C1-4  The counter mis-identifies itself in its own output.
    L437 `'counter': 'check-scrub-admission-r49'` (the exception path L469 says r50).
    Executed live at REV (receipt c1-run.json): `"counter": "check-scrub-admission-r49"`.
    A control-battery receipt is byte-identical in identity to an r49 receipt.
    One-word fix; also L452 main() argparse usage docstring at L51 still names r49.
  D-C1-5  marks_leg(entry, skill, readme, hashes) — `hashes` never used (L360-370). Dead.
  Structural note: LANE_FILES admits `entry.md`, `btrfs-scrub-grounding-r45.md`
  (the row's own bytes — circular evidence) and `check-scrub-admission-r50.py`
  (the measuring instrument). The >=2-row-source rule keeps these out of the credit
  floor, so no bypass today, but citing the instrument's own line numbers couples the
  leg to the counter's line count (an edit that shifts lines silently invalidates a
  cited line while the leg still reports "resolves"). Resolution is bounds-only for
  both branches (L276-278, L285-287): the leg measures "file exists and has >=N
  lines", never content. Smallest correction: drop `check-scrub-admission-r50.py`
  from LANE_FILES, or verify the cited line is non-blank.

Executed (frozen counter at REV):
  python3 tools/check-scrub-admission-r50.py --revision 8029cdba... --lane <lane>
  -> verdict FAIL, counter=check-scrub-admission-r49, structural_ok 1, corr_ok 1,
     quotes_ok 3, verdicts_ok 0, seats_ok 0, marks_ok 0 (receipt c1-run.json).
  The 0s are pre-data (cohort has not reported): consistent with the frozen design,
  not a defect. `--section-hash` reproduces the claimed row hashes exactly
  (GR1 3a2ba180..., GR2 a2e955ce..., GR3 43430a14...; receipt sh.json).

======================================================================
FILE 2: tools/check-adjacency-table-r50.py  (C3; frozen +393)
======================================================================
Leg-by-leg:
- L272-329 inline shape loop: identical five legs as L194-228 shape_legs. They agree
  today (executed on the real table: both = {7,7,0,7,7}; receipt: AGREE True). But the
  predicate (L366-368) scores the REAL table with the inline copy while `stub_fails`
  proves only that `shape_legs` accepts a stub (L343-349). Two authorities for the same
  legs; the stub discriminator validates a DIFFERENT code path than the one that
  scores the real table. If they drift, the stub check is meaningless. And L330
  `shape = shape_legs(adj, anchors, registry)` is DEAD — never read (only `stub_shape`
  is reported). D-C3-1.
- L349 stub_fails = int(stub_shape_ok==1 and s_pin==0 and s_live==0). The stub names
  sibling 'stub' (L184), so s_pin/s_live are 0 because `/home/vgpnk/Projects/shokunin/
  stub-shokunin/.git` does not exist (L133-136) — the failure mode is "repo absent",
  NOT "quote does not match the pinned bytes". `stub_fails == 1` therefore does not
  establish that a shape-valid stub whose sibling resolves fails the content legs;
  it only proves the counter rejects a stub that names a non-existent repo. D-C3-2.
  Smallest correction: name a REAL sibling in the stub with a real commit but a
  fabricated quote/digest, so the discriminator is quote-vs-bytes.
- L115 `ids` = only OUT ids NAMED by ADJ rows. The anchor table has 10 rows; 9 are
  referenced. OUT-001 is never content-checked. Executed: fabricating OUT-001's quote
  (receipt prov-mut.md, c3-mut.json) -> verdict PASS, quote_at_pin_ok 9. A fabricated
  quote in an unreferenced anchor row is invisible to the counter. D-C3-3. The docstring
  ("every OUT id an ADJ row names") admits this, so it is a coverage note, not a
  violation — but the anchor table presents OUT-001 as a pinned locator and readers
  will assume it was checked.
- L127 `sib = rr.get('sibling') or (anc[2].split...)` — the registry `sibling` is
  preferred over the anchor cell's stem with no cross-check. If they disagree, the
  counter verifies a different repo than the one the table names. D-C3-4. Smallest
  correction: require the registry sibling to equal the stem parsed from anc[2].
- L137/L155-156 `sibling_path` from the registry is read but ignored; 'PROVINCE.md' is
  hardcoded in the git-show path. Consistent with SIB (L73) pinning /PROVINCE.md in the
  anchor cell, so low risk — but the registry field is dead input.
- L52 `Usage: python3 tools/check-adjacency-table-r49.py` — identity leak, same class
  as C1's L437. D-C3-5.
- L51 fixture-override list omits the NEW `--siblings-root` (argparse L382, default
  L80) — a control can point the sibling scan anywhere and the docstring does not say so.
- L80/L382 SIBLINGS default '/home/vgpnk/Projects/shokunin': the verdict depends on
  fleet state outside REV (hermeticity). Declared by the frozen claim ("the quote
  again at the sibling's live tip"), and live_quote_ok >= 8 is the stated hedge, so
  this is a declared tradeoff — but it means the counter cannot fail-then-heal on a
  pure-REX basis and a sibling-side rename breaks it.
- Executed frozen run at REV: PASS, quote_at_pin_ok 9, live_quote_ok 9, stub_fails 1,
  stub_shape_ok 1 (receipt c3-run.json). Executed r49 counter on the same stub: PASS
  (receipt c3-r49-stub.json) — the routed defect is real and the r50 content legs DO
  bite on referenced ids (executed: OUT-002 fabricated quote -> FAIL, pin 8 live 8;
  receipt c3-mut2.json). So the repair is real; the stub discriminator is just weaker
  than its name.

======================================================================
FILE 3: tools/tsukuroi-census.sh  (C2; +47, 5 hunks)
======================================================================
Frozen line numbers.
- @@ -2226,6 +2226,18 @@ : adds buf_has (L2236-2238) / out_has (L2239) and a comment
  (L2229-2235). Changes HOW it matches, not WHAT: same line-oriented ERE over the
  same buffer, now with no early exit. This removes the SIGPIPE class. Semantics are
  preserved for every CURRENT arm — grep for `\b`/`\w`/`\s`/`\</`\>` in the call sites
  returns none (receipt: grep output empty). LATENT DIALECT CHANGE: gawk (installed,
  5.4.1) and GNU grep -E differ on `\b`: executed `\bbar\b` on 'foo bar' -> awk rc=1
  (no match), grep rc=0 (match). If a future arm uses a word-boundary class, the same
  pattern will match differently. Smallest correction: add one line to the comment
  "ERE dialect is awk, not grep — no `\b`/`\w`/`\<`" or add a guard rejecting those
  classes.
- @@ -2378,17 +2390,17 @@ : L2393 pkgline via awk `!p` (full read, prints first match).
  Equivalent to grep|head -n1 minus the SIGPIPE; drops `|| true`, safe because awk
  exits 0 with no match. L2396/2398/2402/2413/2444 swap the arms to out_has/buf_has —
  same patterns, same leg.
- @@ -3628,6 +3640,27 @@ : new case R50-C2 (L3643-3662). One counted arm -> +1 case
  (167->168 structurally; I did NOT run the selftest — the 168 figure is the C2
  counter's job and was not run here). The case uses a ~200 KB probe (L3648-3649),
  above the 96 KiB where the flake was measured — correctly above the threshold.
- Provenance defect (D-C2-1): the comment L2231-2232 says "measured 4/20 false misses
  at a 64 KiB buffer and 11/20 at 96 KiB"; the round claim repeats "11/20 at 96 KiB".
  Executed on this host (receipts matcher.out, var.out): old idiom false-missed 14/20
  at 64 KiB, 19/20 at 96 KiB in one run, and 18-20/20 across five 20-trial batches at
  96 KiB — never 11/20. The failure is racy so absolute counts vary, but the stated
  numbers are not reproduced and are presented as measured. Direction is confirmed
  (old idiom loses mid-stream lines; new matcher 0/20 at all sizes). Smallest
  correction: replace the counts with the direction, e.g. "measured 14-20/20 false
  misses at 64-96 KiB on the round-50 host" or "the old idiom false-misses a
  mid-stream match in ~every trial past the 64 KiB pipe buffer".
- The new case pins the NEW matcher (buf_has at L3653/3657), not the absence of the
  old idiom — that leg is the C2 counter's `idiom_sites == 0`, not this case's job.

======================================================================
Smallest safe corrections (per file, exact text)
======================================================================
C1 L437:     'counter': 'check-scrub-admission-r49'  ->  'counter': 'check-scrub-admission-r50'
C1 L287:     `return False, f'{fname}:{lineno} outside {path} ({n} lines)'`
             -> `why = f'{fname}:{lineno} outside {path} ({n} lines)'; continue`
             (then `return False, why` after the loop) — restores the documented rule.
C1 L426:     `'\\n'.join(ln.rstrip() for ln in (body or '').split('\\n') if ln.strip())`
             -> `' '.join((body or '').split())`  — real whitespace collapse.
C1 L132:     remove `'check-scrub-admission-r50.py': ('tools/check-scrub-admission-r50.py',),`
C3 L330:     delete the dead `shape = shape_legs(adj, anchors, registry)` OR score the
             real table with `shape` and delete the duplicated inline loop L272-329 —
             pick ONE authority and have the stub scored by the same function.
C3 L184:     `sib = 'stub'` -> a real sibling name with a fabricated quote and wrong
             digest, so stub_fails discriminates quote-vs-bytes, not repo-absent.
C3 L127:     cross-check `rr['sibling']` against the stem parsed from anc[2]; disagree -> why.
C3 L52:      Usage line r49 -> r50; add `--siblings-root` to L51.
Census L2231-2232: replace the quoted counts with the direction (see above) or re-measure;
             add an awk-dialect caveat to the comment or a `\b`-rejecting guard.

Axes summary: (a) measurement fidelity — C1 D-C1-1/D-C1-3, C3 D-C3-2; (b) provenance —
C1 D-C1-4, C3 L52, C2 D-C2-1; (c) discrimination — C3 D-C3-2 (weak stub), C3 content
leg bites on referenced ids (supports the repair); (d) dead weight — C1 L360 param,
C3 L330 `shape`; (e) hermeticity — C3 live legs and stub_fails depend on fleet state,
declared.

NOT RUN (so it cannot be claimed): the census selftest itself (the 168 case-count and
the R50-C2 pass) — the C2 counter runs it; I verified the +1 arithmetic structurally.
No tooling installs made; no writes outside the wave dir and scratch; scratch
/fast/scratch/hyaku/tsukuroi-r50/R50CritCounterDiff removed on exit.
