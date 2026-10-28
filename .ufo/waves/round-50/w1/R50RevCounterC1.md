VERDICT: defect-found

# R50RevCounterC1 — review of the frozen C1 counter (item C1-B3)

Seat: R50RevCounterC1, L2, wave `w1`, round 50. Bytes under test:
`8029cdba1049df25632c91a23c8db4eefb54be5f` (`tools/check-scrub-admission-r50.py`,
`corpus/knowledge/btrfs-scrub-grounding-r45.md`). All counter line numbers below are lines of
`git -C <lane> show 8029cdba…:tools/check-scrub-admission-r50.py` (475 lines); entry line numbers are
lines of the frozen `corpus/knowledge/btrfs-scrub-grounding-r45.md`. I did not edit the counter, the
entry, or any tracked file, and ran no git mutation at all: the probe harness drives the counter through
`--entry-file`/`--skill-file`/`--readme-file`/`--wave-dir`/`--results-file`/`--dispatch-file` overrides in
scratch and reads snapshots with `git show`.

Receipts: `.ufo/waves/round-50/w1/R50RevCounterC1/probe.py` (driver, 19 probes, regenerates
`receipts.jsonl`), `receipts.jsonl` (observed output per probe), `live-citation-leg.json` (the live
cohort measurement, 2026-10-28T19:13:25Z). Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50RevCounterC1/`
removed on exit. No tool installed or upgraded.

## Method and baseline

I first proved the counter *can* pass on a synthetic all-`holds` cohort, so that every later FAIL is
attributable to the leg under test and every later PASS is a real acceptance (probe P1, `receipts.jsonl`):

```
P1-kpass  rc=0  verdict=PASS  verdicts_ok=3  seats_ok=18  marks_ok=3
```

The production invocation at the freeze revision is the pre-cohort state (P0): `verdict=FAIL`,
`seats_ok=0`, `marks_ok=0`, `corr_ok=1`, `quotes_ok=3`, `structural_ok=1`, `section_sha256` equal to the
three frozen row hashes in `FROZEN.md`. So the entry bytes and the frozen hashes agree at the freeze:
C1's first conjunct ("the four corrections … are in the bytes") holds at `8029cdba`, and the four C9
strings are present at entry:1 (`source: … S240`), entry:83-85 (the narrowed `[inference]` mark),
entry:127 (the exact `dev-replace.c:1128` quote with `* `), entry:229-232 (the declared S247 gaps).
The defects below are in the *instrument*, not in the entry.

## Findings, by severity

### F1 (critical, live) — the citation leg still refuses real counted reports; the round-49 defect is reproduced, not closed

`verify_citation` (counter:273-289) resolves a `file:line` only in a digest-pinned snapshot
(counter:274-278) or in one of **eight hard-coded basenames** (`LANE_FILES`, counter:121-133). And
`report_citations_ok` (counter:292-304) fails the whole seat if **any single** `file.ext:NNN` token in
the body does not resolve (counter:300-303) — one stray path in a "further reading" line voids a report.

Measured on the real wave at 2026-10-28T19:13:25Z (17 of 18 counted reports present;
`live-citation-leg.json`), using the counter's own `snapshots()` cache and its own
`report_citations_ok()`:

```
reports_present 17   citation_ok 4   citation_refused 13
refusal_reasons: SOURCES.md 6 · btrfs-scrub-record-r44.md 2 · 10-faster-shutdown.conf 3
                 R49CritGR1c.md 1 · C2ExecHostRecheck.md 1
per_row_refused: GR1 R50CritGR1a/b/c, R50RevGR1a · GR2 R50CritGR2a, R50RevGR2b, R50RevGR2c
                 GR3 all six (R50RevGR3a/b/c, R50CritGR3a/b/c)
```

Every refused report has a body >= 6.5 kB and cites **all four** row source files, so no refusal is a
citation-poverty case: each dies on one real lane artifact outside the whitelist. `corpus/SOURCES.md` is
named in the entry's own `source:` line (entry:1); `btrfs-scrub-record-r44.md` is the round-44 entry the
frozen entry links at entry:8; `R49CritGR2b.md`/`R49CritGR1c.md` are the critic reports the frozen entry
cites at entry:232. A seat that cites what the entry cites is refused.

This falsifies `FROZEN.md` C1's "the counter's citation leg now binds real seat reports" and reproduces
the round-49 number (17/18 refused) at 13/17. Reproduced in isolation as probes P9 (`R49CritGR2b.md`
cited → all six GR2 seats refused) and P10 (`SOURCES.md` cited → all six GR2 seats refused); P11 shows
the same refusal for a URL with a port (`https://example.com:8443/…` → "example.com is neither a pinned
snapshot nor a declared lane artifact").

*Scope honesty:* this round the defect is **masked**, not outcome-determining — GR1 is blocked by
`R50RevGR1b` (`partly`), GR2 by `R50CritGR2a`/`R50CritGR2c`/`R50RevGR2c` (`partly`), and GR3 by all six
`partly` reports, and `blocking` is applied *before* the citation check (counter:415-417), so those rows
fail on the cohort's judgment whatever the citations say. On a `holds` cohort the same defect would zero
GR3's credited set outright (6/6 refused) and leave GR1 at one credited seat — `verdicts_ok` could not
reach 3. Any round that reuses this counter inherits that.

### F2 (high) — the ">=2 distinct row source files" repair is content-free: two junk line numbers pass

`report_citations_ok` requires only that the *basenames* cited intersect `CITE[row]` in >= 2 elements
(counter:298-299), and `verify_citation` checks nothing but `1 <= lineno <= len(lines)` against **any**
snapshot with that basename (counter:274-278). Content at the cited line is never compared with the
report. Probes:

```
P2-junk-citations-line-1        rc=0 verdict=PASS verdicts_ok=3   (every seat cites <src>:1, <src>:1, entry.md:5)
P8-two-junk-sources-plus-artifacts rc=0 verdict=PASS verdicts_ok=3 (cmdline.c:1 + vsprintf.c:1 + FROZEN.md:10 + entry.md:5)
```

So "binds real seat reports" is satisfied by a 300-byte template naming any two in-range line numbers of
the row's sources. The `>=2` requirement raises the cost of a forgery from one basename to two; it does
not bind content.

Aggravating: a row needs only `len(credited) >= 3` of its six seats (counter:430), and a refused seat is
neither credited nor blocking, so up to three seats per row can fail the citation leg silently. P3
(`entry.md:999999` in one GR1 seat) still returns `verdict=PASS`, `verdicts_ok=3` — the refusal costs the
row nothing.

### F3 (high) — `corr_ok` is a whole-file substring search: a superset string satisfies C9/C10 without the correction

`corr_missing`/`corr_present`/`corr49_missing`/`corr49_present` (counter:394-399) are `re.search` over the
**whole entry**, never over a row extent, and the required/forbidden lists (counter:108-118, 136-152) are
literal fragments. Probe P14: I restored the round-49 defect *substance* inside GR2 with wording that is
not in `CORR49_FORBID`, and parked the four required strings in a comment block after the last row:

```
defect in GR2 : "[inference: how the btrfs-progs CLI prints these returns, and the ioctl side with it,
                 is not pinned here]"                                  (ioctl.c is pinned at S240 and cited)
                "**Quote.** `S247` dev-replace.c:1128: Scrub doing the replace isn't running …"  (no "* ")
                Limits: "the S247 ranges were left as registered; …"  (gap undeclared)
                line 1: S240 -> S999                                 (S240 off the source: line)
parked after every row:
                [inference: how `btrfs scrub start` and `btrfs scrub status` print these returns is not pinned here
                source: S240
                dev-replace.c:1128: "* Scrub doing the replace
                the widened S247 ranges still do not list
observed      : rc=0 verdict=PASS corr_ok=1 corr49_missing=[] corr49_forbidden_present=[]
```

A full PASS on bytes that carry all four round-49 defects. Two independent holes compose here: the legs
are not row-bound (F3), and the counter does not pin the row bytes (F4), so the seat cohort simply echoes
the mutated row hash.

### F4 (high) — the counter never compares the computed row hashes to the frozen ones

`section_hashes` (counter:216-226) computes the three hashes from whatever entry it is handed; the only
consumer is the seat echo check `if h != hashes.get(row)` (counter:418). The frozen table in `FROZEN.md`
(`3a2ba180…`, `a2e955ce…`, `43430a14…`) appears nowhere in the counter — `grep -nE
'3a2ba180|a2e955ce|43430a14' tools/check-scrub-admission-r50.py` returns nothing (the only `FROZEN`
token is the `LANE_FILES` entry at counter:131). Consequences observed: P14 PASSed with
`GR2 7300e261…` (frozen `a2e955ce…`), P15 PASSed with `GR1 62b7a080…` (frozen `3a2ba180…`), and neither
run emitted a `problem`. `verdicts_ok` is therefore self-referential: it proves the cohort read *some*
bytes, not the frozen bytes. The freeze guarantee rests entirely on an out-of-band table that the
instrument does not consult.

### F5 (medium) — the "no inner heading" structural check is unreachable; an inner `## ` line silently truncates a row

`row_extent` (counter:204-213) sets `j` to the first `## ` line after the header (counter:209) and then
tests `lines[i+1:j]` for a `## ` line (counter:210-212) — a slice that cannot contain one by
construction, so `inner` is always empty and the F1 carry-over is vacuous. The real behaviour is silent
truncation. Probe P15 inserted `## note (truncates the extent silently)` 40 lines into GR1 and a
deliberately wrong quote after it:

```
P15  rc=0 verdict=PASS structural_ok=1 problems=[] quotes_ok=3 verdicts_ok=3
     GR1 quotes parsed: 12 of 13 (the wrong one is outside the truncated extent)
     GR1 hash 62b7a080… vs frozen 3a2ba180…
```

Everything after the injected heading leaves the row: not hashed, not quote-checked, and — with F4 — not
detected.

### F6 (medium) — unparseable `**Quote.**` lines are silently skipped, not flagged

`quote_legs` increments `n_q` only when `QUOTE_RE` matches (counter:252-255); any line starting
`**Quote**` (no period), or with a malformed tail, is invisible. Probe P16 replaced one GR1 quote with
`**Quote** \`S246\` kstrtox.c:999999: "…"` → `verdict=PASS`, `quotes_ok=3`, GR1 `quotes: 11` (was 12),
`bad: []`. This is exactly how the round-49 defect (the missing `* ` prefix at
`dev-replace.c:1128`) can reappear: P14's malformed 1128 line is skipped rather than reported, so
`quotes_ok` stayed 3 on a quote that no longer matches its source line.

### F7 (medium) — the "whitespace-collapsed" distinct-bodies leg collapses only trailing whitespace

`norm_body = '\n'.join(ln.rstrip() for ln in body.split('\n') if ln.strip())` (counter:426-427) strips
each line's *trailing* whitespace and drops blank lines; it does not collapse internal or leading
whitespace, contrary to the docstring "compares whitespace-collapsed bodies, so padding a copy is not a
distinct body" (counter:19-20) and to the entry's own sentence "whose distinct-bodies leg ignores
whitespace-only differences" (entry:305-307). Probes:

```
P12-trailing-space-pad     rc=1 verdict=FAIL distinct_bodies=false   (the documented repair works)
P13-internal-double-space  rc=0 verdict=PASS distinct_bodies=true    (one doubled internal space defeats it)
```

Also: `body` is `lines[2:]`, so the verdict and section-hash lines are excluded from the hash; and bodies
that differ only by the seat name are distinct (that is how P1's K-pass satisfies the leg). The leg stops
byte-identical copies, nothing more.

### F8 (medium) — the citation leg ignores the snapshot id, so the two different `scrub.c` files are interchangeable

`cands = [lines for (sid, sf), lines in cache.items() if sf == fname]` (counter:274) drops `sid`, then
accepts the line if it is in range of **any** snapshot with that basename (counter:276). `S237` is
btrfs-progs `scrub.c` (2231 lines) and `S242` is kernel `fs/btrfs/scrub.c` (3337 lines), and `scrub.c` is
in `CITE['GR3']` (counter:95). Probe P5: all six GR3 seats cited `systemd.kill.xml:68` + `scrub.c:3000`
— out of range for btrfs-progs, in range for the kernel file — `rc=0 verdict=PASS`. A GR3 report can
therefore cite a kernel line number as its btrfs-progs evidence.

### F9 (low) — off-by-one past end of file on both legs

Both legs use a split/count that includes the phantom element after a trailing newline:
`n = b.decode(...).count('\n') + 1` (counter:284) and `len(got)` with `got = text.split('\n')`
(counter:236, range test at counter:262). Probes:

```
P4 entry.md:308  rc=0 PASS  (real_lines 307, cited_line 308, no seat note)
P6 scrub.c:3338  rc=0 PASS  (kernel S242 has 3337 lines)
```

The item's specific question — `entry.md:999999` — is correctly refused
(`R50RevGR1a: entry.md:999999 outside corpus/knowledge/btrfs-scrub-grounding-r45.md (308 lines)`, P3), so
the line-count check exists and bounds the number; it is off by exactly one at the end.

### F10 (low) — `LANE_FILES` consults only the first existing candidate

Inside the lane branch, `return False` sits inside the `for path in LANE_FILES[fname]` loop
(counter:287), so the first candidate that exists at REV decides and the rest are never tried.
`SHA256SUMS` declares four candidates (counter:124-127) with 5, 5, 1 and 2 lines at REV
(`git show …:<path> | wc -l`), so `SHA256SUMS:6` is refused by the 5-line round-45 file even though no
candidate is longer — a latent false-negative the moment a later candidate is longer. It should be
`continue`, and the final `return False` moved outside the loop.

### F11 (low) — the override surface leaves no provenance in the output

The output object (counter:437-448) records `revision` and `base` but not which of
`--entry-file --skill-file --readme-file --wave-dir --results-file --dispatch-file --no-base-check` were
used; the key list from P0 is exactly
`[base, corr49_forbidden_present, corr49_missing, corr_forbidden_present, corr_missing, corr_ok, counter,
marks, marks_ok, per_row, predicate, problems, quotes_ok, revision, seat_notes, seats_ok, section_sha256,
structural_ok, verdict, verdicts_ok]`. A control-battery PASS (P1) and a production PASS are
indistinguishable in the JSON, and the overrides are accepted on any invocation, not only under a
fixture flag. `FROZEN.md`'s discipline ("the measurement is the live integrated revision") therefore rests
on the caller, not on the instrument.

### F12 (low) — a whitespace-only results `output` counts as a completed output

`if not hits[0].get('output')` (counter:328) is a truthiness test. Probe P18 set every results entry to
`"output": " "` → `rc=0 verdict=PASS seats_ok=18`. The docstring's "no completed output" (counter:329) is
not what is checked.

### F13 (low) — duplicate dispatch task names silently rebind a seat's role

`dispatch_tasks` builds `{t.get('name'): t.get('agent') …}` (counter:317), so a name listed twice keeps
the last agent and the docstring's "the dispatch carries it once" (counter:33) is never checked. Probe
P17 appended `{"name":"R50RevGR1a","agent":"critic"}` → `R50RevGR1a: unbound (dispatch agent 'critic' !=
reviewer)`, `seats_ok=17`, FAIL. Fail-closed, but the failure surfaces as a seat-binding error rather than
a dispatch error.

### F14 (low) — identity and doc drift, dead parameters

`out['counter'] = 'check-scrub-admission-r49'` (counter:437) while the file, the exception handler
(counter:469) and the frozen record are r50 — confirmed in every probe (`counter_field`). The docstring
still names the round-49 marks and the r49 filename (counter:34-37, 42-43, 51) although the constants are
round 50 (counter:96-98). `bind_seat`'s `hashes` and `cache` parameters (counter:320) and `marks_leg`'s
`hashes` (counter:360) are unused.

## The four questions in the item, answered directly

1. **Can a report cite `entry.md:999999` and still bind?** No. The `LANE_FILES` line-count check refuses
   it — P3: `entry.md:999999 outside corpus/knowledge/btrfs-scrub-grounding-r45.md (308 lines)`. The check
   is off by one at the end (F9/P4: `entry.md:308` resolves on a 307-line file).
2. **Can a forger pass by citing a declared lane artifact plus one real source line and padding?** No —
   P7: `fewer than 2 distinct row source files cited`, all six GR1 seats refused. But **yes** with two
   junk row-source line numbers plus artifact padding (P2, P8: `cmdline.c:1`, `vsprintf.c:1`,
   `FROZEN.md:10`, `entry.md:5` → PASS). The barrier is the count of row-source basenames, not content.
3. **Does the whitespace-collapsing hash let two different reports collide, and what is hashed?**
   Hashed: `sha256` of the body only (`lines[2:]`, so verdict and section-hash lines excluded), each line
   `rstrip`ped, blank lines dropped, joined with LF (counter:426-427). Two reports that differ only in
   trailing whitespace or blank lines collide — intended and observed (P12). Two reports that differ in
   *leading* or *internal* whitespace do not collide (P13). Reports differing only by the seat name do not
   collide, so the leg cannot distinguish name-substituted copies (P1).
4. **Are the C9/C10 patterns satisfiable by a superset string?** Yes — P14, a full PASS with all four
   required strings parked after every row and the four defects paraphrased in-row (F3).

## Governance consequence (post-data)

Seventeen of the eighteen counted reports have landed (`ls .ufo/waves/round-50/w1/`), so the wave has
scored and `FROZEN.md`'s pre-data amendment window is closed. **I recommend no patch to the frozen counter
this round** — changing a leg or the predicate now would be a post-hoc instrument change to a frozen
claim, and `verdicts_ok` would be measured against a rule the cohort did not read. Instead:

1. Record F1 and F3-F4 as declared limits of the C1 instrument in the round-50 record, the way the entry
   declares its S247/S240 range gaps (entry:229-236), and stop asserting "the counter's citation leg now
   binds real seat reports" in `FROZEN.md`/the entry (entry:305-307), because 13 of 17 real reports were
   refused.
2. Note in the round-50 close that C1's FAIL is the cohort's judgment (`partly` blocks GR1/GR2/GR3 before
   any citation is examined, counter:415-417), not the citation leg — so the citation defect is latent,
   not the cause of this round's verdict.
3. Fix in round 51's pre-data freeze (exact proposed text, minimal, no predicate change required except
   where noted):

```python
# F1: resolve any path that exists at REV, not an 8-name whitelist; and do not void a whole report
#     for one stray token — require that >=2 row-source citations resolve and ignore unresolvable others.
def verify_citation(cache, fname, lineno, lane=None, rev=None, sid=None):
    cands = [lines for (s, sf), lines in cache.items()
             if sf == fname and (sid is None or s == sid)]          # F8: honour the snapshot id
    if cands:
        return any(1 <= lineno <= len(lines) for lines in cands), 'resolves'
    if lane is not None and fname in LANE_FILES:
        for path in LANE_FILES[fname]:
            b = show(lane, rev, path)
            if b is None:
                continue
            n = len(b.decode('utf-8', errors='replace').split('\n')) - 1   # F9
            if 1 <= lineno <= n:
                return True, f'resolves in {path}'
        return False, f'{fname} declared but absent or out of range at REV'  # F10: outside the loop
    ...

# F3: bind the corrections to the sections that must carry them.
FROZEN_ROWS = {'GR1': '3a2ba180…', 'GR2': 'a2e955ce…', 'GR3': '43430a14…'}   # F4
corr_ok = int(not corr_missing and not corr_present and not corr49_missing
              and not corr49_present and hashes == FROZEN_ROWS)             # F4: add to predicate
# F3: evaluate CORR_REQ/CORR_FORBID over row_text('GR1')/row_text('GR2') and the `## Limits` extent,
#     never over the whole entry.
# F5: replace the unreachable inner check with a rejection when the extent's terminator is not a known
#     section heading (`## How this changes OS triage`, `## Limits`, `## Gate status — round 50 …`, …).
# F6: count every line whose stripped text starts with '**Quote' and flag the ones QUOTE_RE rejects.
norm_body = re.sub(r'\s+', ' ', body).strip()                                # F7
'overrides': {k: getattr(a, k) for k in ('entry_file', 'skill_file', 'readme_file', 'wave_dir',
                                         'results_file', 'dispatch_file') if getattr(a, k)},   # F11
if not (hits[0].get('output') or '').strip(): ...                            # F12
if len({t['name'] for t in tasks}) != len(tasks): error('duplicate dispatch task')   # F13
'counter': 'check-scrub-admission-r51'                                       # F14
```

F1's "ignore unresolvable citations, require two that resolve" is the one change that would have let this
round's cohort bind; it is also the change that most needs a counter-critic, because it trades a
false-negative (current) for a weaker per-token guarantee.

## Residual risk and what I did not do

- I did not verify the *content* of the pinned snapshots (that `scrub.c:3159` really is the copy
  attachment); that is the quote leg's job and it passed at the freeze (`quotes_ok 3`).
- I did not evaluate any seat's verdict, the C2/C3 counters, or the K0-K7 control battery in
  `.ufo/waves/round-50/controls/` — out of scope for this item. I only re-proved that a synthetic
  all-`holds` cohort passes (P1), which is the K-pass shape.
- The live measurement is a snapshot at 17/18 reports; the eighteenth may land after this report. The
  GR3 result is complete (6/6 present, 6/6 refused) and does not depend on it.
- I did not test `--section-hash` on a row header appearing twice (structurally rejected by
  counter:206-207) or a non-UTF-8 report (rejected at counter:341-344); both read fail-closed.
- F2's "two junk citations" and F3's superset-string PASS are synthetic fixtures, not claims about what
  the counted cohort did.
