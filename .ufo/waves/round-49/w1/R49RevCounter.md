VERDICT: defect-found

# R49RevCounter — review of `tools/check-scrub-admission-r49.py` at 55c07cd3

Counter under review: `tools/check-scrub-admission-r49.py` at `55c07cd3f8bff2e12117c34d57b4c618de74d85c`,
sha256 `3dd52ef376e233192f955208c1132f6b0d23bbebe97dd1df75e6296f55d970a4` (receipt
`.ufo/waves/round-49/w1/R49RevCounter/counter.sha256`, copy `.../R49RevCounter/counter.py`).
Spec read: `.ufo/waves/round-49/frozen/FROZEN.md` line 15 (C1 row), lines 31-38 (counted cohort),
line 45 (C1 controls). 421 lines, read in full. Nothing was edited; every probe ran on a copy in
`/fast/scratch/hyaku/tsukuroi-r49/R49RevCounter/` and on a `git clone --shared` fixture there
(`git -C <fx> rev-parse --show-toplevel` == the fixture dir; the lane was read-only throughout).

## 0. Blast radius: the live cohort scores `FAIL` today, and the counter is not the only cause

Measured on the live wave dir at 2026-10-28T17:41:44Z (`live-projection.txt`), 18 GR reports present,
all 18 carrying a row-source citation:

| row | reports `holds` | survives `report_citations_ok` | blocking |
|---|---|---|---|
| GR1 | 6 | 1 (`R49CritGR1c`) | — |
| GR2 | 5 (`R49CritGR2b` = `partly`) | 0 | `R49CritGR2b` |
| GR3 | 6 | 0 | — |

Projection through the counter with the live reports + live dispatch + synthetic results entries
(each seat's real `name`/`agent`, `output` = non-empty): **`verdicts_ok 0`, `seats_ok 18`,
`FAIL`** (GR1 credited 1, GR2 credited 0 + blocking, GR3 credited 0). Two independent causes:
(A) `R49CritGR2b` is a bound-format `partly` on the current GR2 hash `d4296085…`, which FROZEN
lines 36-37 make blocking whatever its citations — that is working as frozen, and C1 cannot pass
while that report stands; (B) 16 of 18 reports cite at least one `file:line` of a file outside the
ten pinned snapshots (finding 3 below), so they earn nothing even though every one of them cites its
row's sources. If the L1 wants C1 to pass, the reports (not the counter) must be rewritten to cite
only `scrub.c ioctl.c sysfs.c btrfs-scrub@.service cmdline.c vsprintf.c kstrtox.c dev-replace.c
systemd.kill.xml capture.txt`, or FROZEN's "citations resolving in the pinned snapshots" must be
read as "at least one" and the counter amended — it currently implements "every one".

The battery reproduces the frozen controls: K-pass (`fx-pass.json`) `PASS rc=0`; base
(`base-run.json`) `corr_ok 0, verdicts_ok 0, seats_ok 0, marks_ok 0`, `FAIL rc=1`, matching FROZEN's
"Before at base" column; freeze with no cohort `FAIL` (`freeze-run.json`); re-run of K2 (five defect
strings restored) `corr_ok 0 FAIL`; K4 (two byte-identical bodies) `distinct_bodies False FAIL`;
K5 (reviewers only) `seats_ok 9 FAIL`; K6 (results absent) `seats_ok 0 FAIL`. The counter can pass and
does fail its controls. The defects below are about what a PASS then means.

## 1. HIGH — the row hashes are not pinned to FROZEN.md; a row can drift and still PASS

`section_hashes` (counter.py:178-189) is recomputed from the revision under test, and the seat's line 2
is compared against that recomputed value (counter.py:367), never against FROZEN.md lines 24-26
(`3a2ba180…`, `d4296085…`, `43430a14…`). Those three constants appear nowhere in the source
(`grep -F '3a2ba180' counter.py` → no match; also `d4296085`, `43430a14`).

Concrete end-to-end proof, fixture repo, real counter invocation, all 18 seats `holds` on the emitted hash:

- **Mutant A**: in GR2 the claim `an unknown devid gives \`-ENODEV\` (\`scrub.c:3336\`)` is replaced by
  `an unknown devid gives \`-EINVAL\` …` (a wrong claim inside the row) and the correct sentence is
  appended *outside* every row extent (the gate-status section, which FROZEN line 28-29 says may be
  edited). Result: `rc=0 PASS`, `corr_ok 1`, `quotes_ok 3`, `verdicts_ok 3`, `seats_ok 18`,
  `marks_ok 3`, with **GR2's computed hash ≠ `d4296085…`**.
- **Mutant B**: A plus a stray `## GR2b` heading after GR2's last quote. Extent silently shrinks to
  `(55,70)`, `structural_ok 1`, `quotes_ok 3`, `rc=0 PASS`, again with GR2 ≠ frozen.

FROZEN line 28 freezes the row bytes ("The row bytes are frozen from here") and lists their hashes as
*the* frozen values; the counter cannot see a violation of that sentence. Every "correction landed"
claim below is therefore only as strong as `corr_ok`, which §2 shows can be satisfied from outside the
rows.

## 2. HIGH — `corr_ok` is entry-wide, not row-scoped, and presence-only

`corr_missing`/`corr_present` (counter.py:346-348) run `re.search` over the whole `entry` string, not
over the three row extents that `section_hashes` already computes.

- The seven required patterns are all satisfied inside their rows at the freeze (line map: GR1 18, 53;
  GR2 69, 75-76, 80, 82, 144), **but `ioctl\.c:3132` is also present at line 283, outside every row**
  (in the round-49 gate-status prose). Deleting GR2's in-row `ioctl.c:3132` citation leaves
  `corr_ok 1` (probe P2). So one of the seven corrections is already double-satisfied and the row
  requirement is not what the leg measures.
- Mutant A above is the general case: revert a correction in-row, restate it out-of-row → `corr_ok 1`.
- Presence-only: `picks hexadecimal for a leading \`0x\` or \`0X\` followed by a hex digit …` rewritten as
  `never picks hexadecimal for a leading \`0x\` or \`0X\` followed by a hex digit, and no other leading \`0\`
  is octal.` still yields `corr_ok 1` (probe N1). No negation or polarity is checked.
- Superset matches, no boundaries (probes with the counter's own compiled patterns):
  `dev-replace\.c:1171-1195` matches inside `dev-replace.c:1171-11950`; `ioctl\.c:3132` matches inside
  `ioctl.c:31321`; `not \`is_valid\`, dev-replace.c:1278-1279` and `not an unknown devid gives \`-ENODEV\``
  both match their REQ patterns. `the copy attached\s*\n?\(scrub\.c:3159\)` matches across six blank lines
  or a tab (`\s*` already spans newlines; the `\n?` is redundant).

### 2b. The forbidden list false-positives on legitimate text, and is case/space blind

Four plausible errata/narrative sentences, appended to the frozen entry, each flip `corr_ok` to 0
(probe F1): `The cancel clause, which by SR7 is outside the pinned bytes, is marked inference.`;
`A reworded sentence that says the path only sets the state to SUSPENDED would be wrong.`;
`dev-replace.c:1171-1199 covers the wider region including the writeback flag.`;
`The clause "which it is for a replace in state" was imprecise.` — i.e. any honest note that names a
defect trips it, including quoting the round-48 finding (probe E2, `corr_ok 0`). FROZEN lines 28-29 allow
the gate-status heading text to be rewritten after the wave, and lines 281-287 already narrate the
round-48 findings in that area; the next amendment that quotes one will silently break `corr_ok`.

Conversely the same patterns are case- and whitespace-sensitive: `only sets the state to Suspended`,
`only  sets the state to SUSPENDED`, `only sets the state to\nSUSPENDED` all pass `CORR_FORBID[3]`
(no `re.I`, no `\s+` between words), so restoring the defect with a case change is invisible.

## 3. HIGH (operational) — the citation leg requires *every* `file.ext:NNN` token in the body to be a pinned snapshot file

`report_citations_ok` (counter.py:244-257): after the 300-byte floor and the "≥1 row-source citation"
gate (`counter.py:247`), it iterates **all** `CITE_RE` hits and returns False on the first that fails
`verify_citation` (counter.py:252-255). One incidental token voids the seat.

Measured on the 18 live GR reports: 16 voided (table in §0). The voiding tokens are ordinary evidence
prose, not bad citations: `check-scrub-admission-r49.py:205` (6 reports), `FETCH.txt:3` (3),
`capture.sh:12`, `SOURCES.md:249`, `btrfs-scrub-record-r44.md:138`, `entry.md:…`,
`10-faster-shutdown.conf:2`, sibling reports (`R49RevGR2a.md:103`), and one real over-range citation
`dev-replace.c:3081` (S247 `dev-replace.c` is 1323 lines). Two seats that *do* cite the counter they
were asked to review (`R49CritGR1b`, `R49RevGR1a`) are voided for it.

Answers to the item's sub-questions, with inputs:

- **300-byte floor — bytes or characters?** Bytes: `len(body.encode('utf-8'))` (counter.py:245), which
  is what FROZEN line 35 says. Harmless, but note a 162-character body with multibyte padding passes
  at 312 bytes; a 299-byte ASCII body fails.
- **Citations in a fenced block?** They count. There is no fence awareness anywhere in the leg:
  `GR1 reading follows.\n\`\`\`\ncmdline.c:5\n\`\`\`\n<300B>` → `ok=True`. FROZEN does not exclude
  fences, so this is spec-harmless; it does let a pasted source dump carry the citation leg.
- **Citation of a file not in the row's CITE list?** It passes if the file is a pinned snapshot
  (`capture.txt:8` in a GR1 body → `ok=True`, 2 citations resolve), and voids the body if it is not
  (`FROZEN.md:12`, `PROVINCE.md:44`, `SKILL.md:1000`, `round-49.md:9`, a URL with a port
  `example.org:8443` → all `ok=False`). `CITE_RE` (counter.py:93) tokenises ordinary prose as
  citations: `kernel 6.4.2:3` → `6.4.2`, `v7.2.11:18` → `v7.2.11`, `ratio 1.5:2` → `1.5`.
- **Negated citations count**: `I did NOT read scrub.c:3159. ` ×12 and `scrub.c:3159 is not the line I
  checked. ` ×12 both return `ok=True`; a body of 30 repetitions of `cmdline.c:5 ` returns
  `ok=True, 30 citations resolve`. The leg measures token presence, never that a citation was used.
- **Off-by-one**: `verify_citation` allows `lineno == len(lines)` (counter.py:239) where `lines` came
  from `split('\n')` of a newline-terminated file, so the phantom trailing empty element "resolves":
  `scrub.c:3338` → `(True, 'resolves')` against `''` (S242 `scrub.c` has 3337 real lines; every one of
  the 10 pinned files resolves at `len(lines)`). Same for quote lines (counter.py:224).

## 4. MEDIUM — `quotes_ok` is satisfied by empty or trivial quote text, and silently skips malformed lines

`quote_legs` (counter.py:202-232) counts a row ok when `quotes > 0` and no entry is `bad`; a line that
does not match `QUOTE_RE` is skipped without being counted or flagged, and the match predicate is
`norm(want) in norm(got[line-1])` (counter.py:227) — a substring test with `norm('') == ''`.

- Deleting all 29 GR2 quote lines and inserting one `**Quote.** \`S242\` scrub.c:1: ""` gives
  `{'quotes': 1, 'ok': 1, 'bad': []}` → `quotes_ok 3`. Whitespace-only text and `"f"` against a real
  line behave the same (all 29 replaced by `"f"` → `quotes: 29, ok: 29`).
- Appending a trailing note to a quote line breaks `QUOTE_RE` and the line disappears from the leg:
  6 of 29 broken → `quotes: 23, ok: 23, bad: []`, `quotes_ok 3`; the 6 unchecked lines could cite any
  line with any text. (Breaking all 29 is caught, because `quotes 0` fails the `> 0` guard.)
- Real content mismatches are caught (`totally invented text` → `S242 scrub.c:1: quote mismatch`; 29/29
  real quotes resolve), and the leg depends only on digest-verified snapshots, so this is a floor
  problem, not a false-accept on honest bytes. With §1 unfixed, though, a gutted row passes.

## 5. MEDIUM — `section_hashes` extent rule: dead inner-heading guard, asymmetric header match, silent truncation

`row_extent` (counter.py:166-176):

- `inner = [ln for ln in lines[i+1:j] if ln.startswith('## ')]` (counter.py:172) is **dead code**:
  `j` is by construction the first index > i with `startswith('## ')` (counter.py:171), so the slice can
  never contain one. The docstring's "one header each, no inner heading (F1 carry-over)" (counter.py:11-12)
  is never enforced. Proof: `inner == []` for every row; a stray `## GR2b` inside GR2 returns
  `row_extent(...) == (None, None)` — no problem — and instead **truncates** GR2 to `(55,70)`, dropping
  29 quotes to 0 (`structural_ok 1`). Placed after the last quote it drops only the tail: mutant B of §1
  passes with the row truncated and its hash different from frozen.
- **Asymmetry**: the header is found with `ln.strip() == f'## {row}'` (counter.py:167) but the terminator
  requires column 0 (`lines[k].startswith('## ')`, counter.py:171). An indented `  ## GR2` is accepted as
  GR2's header yet does not end GR1: GR1's extent becomes `(13,151)`, swallowing 41 GR2 quotes, with
  `structural_ok 1` (`GR1` hash changes, `GR2` unchanged). A fenced `## GR1` is likewise taken as the row
  header (no fence awareness) and shifts the row's start.
- **The documented hash convention is wrong** (also raised by `R49CritGR2b` §Hash). The extent includes
  the blank line that precedes the next `## ` heading, so `'\n'.join(lines[i:j])` **ends with a newline**.
  FROZEN lines 19-20 and counter.py:33 both say "LF-joined row lines, no trailing LF"; the values that
  match the frozen table are the *with*-trailing-LF ones:

  | row | counter value (with final LF) | rstrip value (the documented convention) |
  |---|---|---|
  | GR1 | `3a2ba180…43fee1` = frozen | `0b67bea0…911aff` ≠ frozen |
  | GR2 | `d4296085…bd027f` = frozen | `75d24ea6…1d9a02` ≠ frozen |
  | GR3 | `43430a14…bbc32c` = frozen | `17b19a53…7720e7` ≠ frozen |

  A seat that re-derives the hash per the written convention gets the right-hand column and is unbound
  (`h != hashes.get(row)`, counter.py:367). `R49CritGR2b` hit exactly this. `R48CritGR2a` described the convention as
  join-without-trailing-LF while printing the frozen value; recomputing the round-48 GR2 extent at
  `ae99f021` gives `e0b391e1…` **with** the final LF and `7bf985d8…` without it, so the record's
  prose is wrong at both revisions and only the printed constants are self-consistent.

## 6. MEDIUM — seat binding: cross-row verdict *quotations* block a row; prose contradictions do not

- `bind_seat` scans the whole body for `ROW GR<n> VERDICT: <word>` (counter.py:306) and converts any
  line whose row or verdict differs from line 1 into `partly`. A GR1 reviewer that quotes the sibling
  binding format as an example (`Sibling format example: ROW GR2 VERDICT: holds.`) is returned as
  `('partly', <its own correct hash>, …, 'contradicting line ROW GR2 VERDICT: holds')` and blocks GR1:
  end-to-end fixture `rc=1 FAIL`, `verdicts_ok 2`, `GR1 blocking ['R49RevGR1a']` (probe F1). FROZEN
  lines 36-37 make a *bound-format negative* blocking; a quotation of another row's positive verdict is
  not that, and with 18 seats cross-referencing each other this is a live false-block hazard.
- The inverse: a real contradiction in prose is not seen. `On reflection, ROW GR2 verdict: fails — the
  suspend-path clause still overreaches.` in a GR2 critic's body → `rc=0 PASS`, `verdicts_ok 3`
  (probe F2), because `ANY_VERDICT_RE` (counter.py:90) is exact-case and requires `ROW GRn `.
- Blocking ignores the hash: a `partly` whose line 2 is `'f'*64` still lands in `blocking`
  (counter.py:364-366 precedes the hash test at :367) — fixture S1 `verdicts_ok 2` with a stale hash.
  FROZEN lines 36-37 say a bound negative "on the current hash" blocks; this blocks on any hash.
  Conservative, but it means a seat that read the wrong revision can sink a row.
- Output truthiness only: `{'output': ' '}` passes `if not hits[0].get('output')` (counter.py:280) —
  fixture T3 `PASS`. FROZEN says "non-empty output"; a space is non-empty by the letter, so a
  placeholder is indistinguishable from a completion.
- Duplicate dispatch tasks are invisible: `dispatch_tasks` builds a dict `{name: agent}`
  (counter.py:269), last wins. A dispatch that lists `R49RevGR1a` first as `executor` and then as
  `reviewer` still binds (`PASS`, fixture T1), as does listing the reviewer twice (T2). FROZEN line 38
  requires "one dispatch task with the declared role"; duplicates are not detected. (Duplicate
  *results* entries are detected: `len(hits) != 1` → unbound, fixture S3 `seats_ok 17 FAIL`.)
- CRLF/BOM/trailing-space first or second lines are unbound (exact `fullmatch`, counter.py:300-305;
  fixture D7b `(None, None)`). Fail-closed, but a report written with CRLF can never bind, and the
  frozen bytes are LF. Worth a line in the seat prompt rather than a fix.

## 7. LOW — `--revision` need not descend from `BASE`

The base check is `git cat-file -e <BASE>^{commit}` (counter.py:328): it only proves `BASE` is readable
in the lane. Nothing ties the measured revision to `BASE`, to `master`, or to the freeze, so the
counter measures "whatever commit you name" as long as that commit contains the three rows, SKILL,
README, dispatch and results. Paired with §1 this is how a fixture PASS becomes indistinguishable from
a lane PASS in the log — the only provenance is the `revision` field in the JSON.

## Receipts

`.ufo/waves/round-49/w1/R49RevCounter/` — `counter.py` + `counter.sha256` (bytes under review),
`freeze-run.json`, `base-run.json`, `fx-pass.json` (K-pass), `live-projection.txt` (live cohort at
17:41:44Z), `repro-probes.py` + `repro-probes.out` (re-runs §1-§6 unit findings against the frozen
bytes with no temp files and no lane writes; `python3 repro-probes.py [<lane>]`).

## What is sound, with the input that proves it

- Predicate string == the code predicate == FROZEN line 15 (`structural_ok == 1 and corr_ok == 1 and
  quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3`).
- `structural_ok`: duplicate row header → `(0, ['GR1: header appears 2 times'])`.
- `quotes_ok`: digest mismatch or absent snapshot is caught (`snapshot absent or digest moved`);
  a wrong quote text is caught; all 53 real quote lines across the three rows resolve at the freeze
  (GR1 12, GR2 29, GR3 12).
- `verdicts_ok`: needs ≥3 credited, ≥1 reviewer and ≥1 critic, pairwise distinct bodies; K4 reproduces
  `distinct_bodies False → FAIL` and K5 `seats_ok 9 → FAIL`.
- `seats_ok`: duplicate *results* entries and absent results fail closed; duplicate JSON object keys
  fail closed (`load_json` → `None`, `DupKey` swallowed by `except Exception`).
- `marks_ok`: entry mark must be an exact line (a trailing space fails), SKILL mark a stripped whole
  line (an inline mention fails); README mark correctly rejects `GR1-GR3 are not admitted round 49`
  when the file name is in the same sentence (`readme=False`), and rejects `unadmitted`,
  `never admitted`, `stay pending`, `stays pending` (counter.py:88).
- `report_citations_ok` 300-byte floor measures bytes, as FROZEN says.
- A `--section-hash` run prints the three values and returns 0 only with all three rows found.

## Residual risk

1. **Marks leg on the README (medium).** `NEGATE_RE` (counter.py:88) is a 5-phrase case-sensitive list,
   and the splitter (`re.split(r'(?<=[.!?])\s+', ' '.join(readme.split()))`, counter.py:316-321)
   whitespace-normalises the whole 64 KB README first, so its 225 "sentences" include 11 KB table
   blobs. Concrete false positives: `btrfs-scrub-grounding-r45.md is NOT admitted round 49.` and
   `… isn’t admitted round 49.` both set `readme=True`; so does a synthetic table with the name in one
   cell and `admitted round 49` in an unrelated cell of the same mega-sentence. Concrete false
   negative: `btrfs-scrub-grounding-r45.md is admitted round 49 while other.md stays pending.` →
   `readme=False`, because `stay pending` is in the same sentence. A phrase inside a code span counts
   (`readme=True`), which is probably intended. The mark is a bookkeeping sentence the L1 writes, so
   this ranks below §1-§5, but it means "the README says admitted" is not what is checked.
2. **Marks leg on the entry (low).** `MARK_ENTRY in entry.split('\n')` (counter.py:313) accepts the
   heading inside a fenced code block; CRLF fails.
3. The counter has no fence awareness anywhere (header detection, quote lines, citations), and
   `quote_legs`/`verify_citation` ignore snapshot identity: `scrub.c` exists in both S237 and S242, so
   a citation resolves against either file's length.

## Verification gaps — what I did not do

- I did not run any census selftest, the C2 or C3 counters, or `--section-hash` inside the lane working
  tree; every probe used a copy, the fixture clone, or the lane at the frozen revision via
  `git show` (read-only).
- I did not re-derive the pinned snapshot digests with `sha256sum -c`; the counter's own digest gate
  loaded all 10 files, which is what the quote leg depends on.
- The live-cohort projection used the working-tree wave dir (mutable) via `--wave-dir` and a synthetic
  `w1-results.json` (the real one does not exist yet); it is a snapshot at 17:41:44Z, not a measurement
  of the integrated revision. The `R49CritGR2b` `partly` and the citation voiding are facts about the
  files present at that time; seats may still change them.
- No lane file, fleet file, PATH entry or external source was written. Tooling: nothing installed
  (python3 from the host); no pacman/uv/npx transaction.
