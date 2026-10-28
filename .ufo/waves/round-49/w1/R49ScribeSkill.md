VERDICT: draft

Seat R49ScribeSkill — round 49 (hyaku run 11), wave w1, item F-8. Execution class EXEC-AUTHORIZED: the commands named
in the item only. Freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c`. Nothing in the lane was edited; this report and its
two receipts are the only files written.

## What this seat did

Read the frozen bytes with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:<path>`
(SKILL.md, tools/tsukuroi-census.sh, corpus/knowledge/btrfs-scrub-grounding-r45.md, corpus/README.md,
tools/check-scrub-admission-r49.py, .ufo/waves/round-49/frozen/FROZEN.md) and drafted the two SKILL.md appends below.
Both drafts are text only: no line of SKILL.md was written, and the drafts are marked with the freeze facts they must
carry, so the L1 can insert one of them verbatim.

Frozen byte digests I read from (receipt `receipt-freeze-bytes.txt`):
`SKILL.md` c809745d8b42804f913bd3377014a5a6eba5752d5af9814fca22a59933981f5a (4546 lines, ends with `\n`),
`tools/tsukuroi-census.sh` c66144d73da1ac376cfe756eab3a60340e18bce91d60abe24c444408b99a2e75 (3765 lines),
`corpus/knowledge/btrfs-scrub-grounding-r45.md`, `FROZEN.md`, `check-scrub-admission-r49.py`, `corpus/README.md`.

## Independent re-derivation of the three row hashes (own scratch computation, not the counter)

I re-implemented the counter's `row_extent`/`section_hashes` convention (`tools/check-scrub-admission-r49.py:166-190`:
the lines from the `## GR<n>` header up to the next `## ` line, LF-joined, no trailing LF) over the frozen entry bytes
and got exactly the frozen values:

| Row | header line | end (exclusive) | sha256 |
|---|---|---|---|
| GR1 | 14 | 55 | `3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1` |
| GR2 | 56 | 151 | `d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f` |
| GR3 | 152 | 197 | `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` |

These equal `.ufo/waves/round-49/frozen/FROZEN.md:24-26`. I also re-ran the counter's own correction legs by regex over
the frozen entry (the 7 patterns of `CORR_REQ` at `check-scrub-admission-r49.py:100-108` and the 5 forbidden strings of
`CORR_FORBID` at `:109-115`): all 7 required forms present, 0 forbidden strings present. That is a byte fact, not a
counter verdict — the counter's `corr_ok` is its own leg and I did not run it.

## Draft 1a — SKILL.md append, PASS variant (insert ONLY if the C1 predicate passes at the integrated revision)

```markdown
## Scrub grounding — round 49 admission

Appended 2026-10-28 (round-49 C1; drafted by wave seat R49ScribeSkill, integrated by the L1). Entry
`corpus/knowledge/btrfs-scrub-grounding-r45.md`; freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c`; wave
`.ufo/waves/round-49/`; pre-data controls `.ufo/waves/round-49/controls/battery-summary-r49-c1.jsonl`.

GR1, GR2 and GR3 are **admitted**. The seven corrections the round-48 counted seats named are in the frozen bytes and
the defect strings they replaced are gone (`.ufo/waves/round-49/frozen/FROZEN.md:15` names the list: `CritGR1a` ×2,
`CritGR2a` ×4, `RevGR2a` ×2 as one list of seven), and 18 counted seats of one wave bound `holds` on exactly those
bytes.

| Row | Extent (`## GR<n>` up to the next `## ` line) | sha256 at the freeze |
|---|---|---|
| GR1 | `## GR1` → `## GR2` | `3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1` |
| GR2 | `## GR2` → `## GR3` | `d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f` |
| GR3 | `## GR3` → `## How this changes OS triage` | `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` |

The digest is sha256 over those lines LF-joined with no trailing LF (`.ufo/waves/round-49/frozen/FROZEN.md:20-26`);
print it with `python3 tools/check-scrub-admission-r49.py --revision <REV> --section-hash`.

Seats: reviewers `R49RevGR{1,2,3}{a,b,c}` and critics `R49CritGR{1,2,3}{a,b,c}` (18). Each binds as a file
`.ufo/waves/round-49/w1/<seat>.md` whose line 1 is `ROW GR<n> VERDICT: holds` and whose line 2 is
`SECTION SHA256: <the row hash above>`, with a body of at least 300 bytes whose `file:line` citations resolve in the
pinned snapshots, one completed `w1-results.json` entry of the declared role and one dispatch task of that role.

Counter: `python3 tools/check-scrub-admission-r49.py --revision <REV>` — PASS iff `structural_ok == 1 and
corr_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3` (`.ufo/waves/round-49/frozen/FROZEN.md:15`).
The three marks must land in the same revision: this heading, `## Gate status — round 49 (GR1-GR3 admitted)` in the
entry, and one `corpus/README.md` sentence that names `btrfs-scrub-grounding-r45.md` and `admitted round 49`
(`tools/check-scrub-admission-r49.py:85-87`, `:312-322`). A SKILL-only insert admits nothing, and a bound
`partly`/`fails` report on the current hash blocks its row whatever its citations (`:365`).

Retained, not withdrawn: the round-48 findings stay as written and stay the reason the rows were not admitted then —
`.ufo/waves/round-48/w2/R48CritGR1a.md` (the `0X` prefix; the unmarked permission inference), `R48CritGR2a.md` (the
`is_valid` gate; the cancel sentence's subject; the suspend-path effects; the stricter `writeable`; the
`dev-replace.c:1171-1199` range end) and `R48RevGR2a.md` (the STARTED cancel branch; the range end and the omitted
`time_stopped`/writeback effects; the `ioctl.c:3132` citation; the `-ENODEV` devid case). The corrections answer those
defect statements; they do not retract the findings or the round-45/-46 gate paragraphs above.

Limits: the counter counts bound reports, not the truth of the kernel statements. GR1's examples still follow from the
quoted code — nothing was written to `scrub_speed_max`, which this caller cannot write (capture.txt:1) — and the
`[inference]` marks of GR1-GR3 stay in force. The measurement is the live integrated revision; the pre-data controls
only prove the counter can pass and can fail.
```

Admission status of that heading, checked mechanically against the counter's own mark string: the line
`## Scrub grounding — round 49 admission` is byte-identical to `MARK_SKILL` (`tools/check-scrub-admission-r49.py:86`),
which `marks_leg` matches by strip equality (`:313-314`). Inserted alone it satisfies one of the three marks only.

## Draft 1b — SKILL.md append, WITHHELD variant (insert ONLY if the C1 predicate FAILS at the integrated revision)

```markdown
## Scrub grounding — round 49 admission (withheld)

Appended 2026-10-28 (round-49 C1; drafted by wave seat R49ScribeSkill). Use this variant only when
`tools/check-scrub-admission-r49.py` prints FAIL at the integrated revision: GR1, GR2 and GR3 are **not admitted** this
round. Entry `corpus/knowledge/btrfs-scrub-grounding-r45.md`; freeze
`55c07cd3f8bff2e12117c34d57b4c618de74d85c`; wave `.ufo/waves/round-49/`.

The heading above is deliberately not the counter's mark line (`## Scrub grounding — round 49 admission`, matched by
strip equality in `tools/check-scrub-admission-r49.py:86,314`): a withheld note must not satisfy `marks_ok`. Admission
needs the exact mark, `## Gate status — round 49 (GR1-GR3 admitted)` in the entry and one `corpus/README.md` sentence
naming `btrfs-scrub-grounding-r45.md` as `admitted round 49`, all in one revision.

Blocking seat at the measured revision: `<seat>` bound `<holds|partly|fails>` on `<row>` at hash `<hash>` (the
counter's field `per_row.<row>.blocking`; a bound `partly`/`fails` blocks the row whatever its citations,
`.ufo/waves/round-49/frozen/FROZEN.md:34-35`). Counter
`python3 tools/check-scrub-admission-r49.py --revision <REV>`; predicate `structural_ok == 1 and corr_ok == 1 and
quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3`.

The row bytes below are frozen and unchanged by the failed gate; the seven corrections the round-48 counted seats named
are in them (`CritGR1a` ×2, `CritGR2a` ×4, `RevGR2a` ×2 as one list of seven) and their defect strings are gone.

| Row | Extent | sha256 at the freeze |
|---|---|---|
| GR1 | `## GR1` → `## GR2` | `3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1` |
| GR2 | `## GR2` → `## GR3` | `d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f` |
| GR3 | `## GR3` → `## How this changes OS triage` | `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` |

Retained, not withdrawn: the round-48 findings (`.ufo/waves/round-48/w2/R48CritGR1a.md`, `R48CritGR2a.md`,
`R48RevGR2a.md`) and the round-49 seat that read the row short of `holds` are both on the record; the next round
re-reads the row from its frozen bytes, not from this note.
```

Note for the L1: the two variants are mutually exclusive and must never both stand — the withheld heading cannot
satisfy `marks_ok` by construction, so leaving both would still open the withheld text while silently satisfying the
mark through the pass variant's heading. Also, the blocked row must be named from the counter's JSON, not from my
observation below.

## Draft 2 — SKILL.md append, census selftest descriptor-band diagnostic (C3)

```markdown
## Census selftest — descriptor-band diagnostic (round 49)

Appended 2026-10-28 (round-49 C3; drafted by wave seat R49ScribeSkill, integrated by the L1). Surface
`tools/tsukuroi-census.sh` at freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c`: usage text `:603-609`, alias
resolver `selftest_base_dir` `:2063-2099`, diagnostic `:2113-2122`, selftest case `(R49-C3)` `:3574-3599`. Counter
`python3 tools/check-fd-band-r49.py --revision <REV>`; predicate `stale_ok == 1 and diag_ok == 1 and band_ok == 1 and
cases == 167`.

| Observation | Reading | Action |
|---|---|---|
| `selftest: fd band 240 241 242 243 244 245 246 247 248 249 exhausted (every descriptor already open), cannot alias TMPDIR <…>; no /tmp fallback (R49-C3)` on stderr, `--selftest` exit 1, no fixture tree created (`mktemp -d` is not reached, `:2124`) | every descriptor of the alias band was already open, so `selftest_base_dir` returned `ST_BASE_ERR=fd-band` (`:2091`); a dirty `TMPDIR` can no longer fail silently or fall back to `/tmp` | close the descriptor holding the band, or run `--selftest` from a fresh shell; there is still no `/tmp` fallback (R48-C2) |
| the same line names a band other than `240 … 249` | a caller exported `SELFTEST_FD_BAND`; the message interpolates `${SELFTEST_FD_BAND:-…}` (`:2115-2116`) | read the named band, not 240-249, and treat the run as a caller-altered selftest |
| `selftest: could not reserve the 240/241 probe descriptors for the fd-band case (R49-C3)` and the run FAILS | descriptor 240 or 241 was already open in the caller's environment, so the case cannot exhaust its two-descriptor band (`:3580-3582`, `:3599`) | not a census defect — the case is a deliberate should-fail probe; re-run where those descriptors are free |
| `TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)` | the 166 legacy cases plus the one `(R49-C3)` case, with the built-in band | the count is the C3 counter's `cases` leg |

`SELFTEST_FD_BAND` exists only for the selftest case: `selftest_base_dir` is its only reader (`:2082`) and its only
callers are `run_selftest` (`:2112`) and three selftest cases (`:3558`, `:3568`, `:3587`), so a live census run never
reads it and production keeps the fixed 240-249 band documented above.

Named limit: a caller-exported override changes selftest behaviour, not just the message. `--selftest` inherits the
variable, the `(R49-C3)` case saves and restores it around its own `SELFTEST_FD_BAND='240 241'` (`:3584`, `:3586`,
`:3594`), and a band that includes an auto-allocated descriptor (10 and up) or a descriptor at or above bash's script
mark (255) reintroduces the two failure modes the fixed band avoids — a fixture child's `exec 10<…` re-pointing the
alias (the `/proc/self/fd/10 … Not a directory` failure recorded at `:2069-2078`) and an alias above the shell's own
script descriptor. Read a substituted band line as the caller's override, never as production behaviour.
```

Every factual claim in that draft is code-derived from the frozen census at the cited lines, not from a run I made:
`band=${SELFTEST_FD_BAND:-240 … 249}` (`census:2082`), `ST_BASE_ERR=fd-band; return 1` (`:2091`), the `printf` naming
the band and the `no /tmp fallback (R49-C3)` tail (`:2115-2116`), `selftest_base_dir || { case "${ST_BASE_ERR:-}" in …
return 1; }` (`:2112-2122`), `work=$(mktemp -d …)` after the resolver (`:2124`), the `(R49-C3)` case's reservation and
restore block (`:3580-3597`), and the selftest's return status reaching the script's exit through `run_selftest;
return` in `main` (`:3688-3691`) with `main "$@"` as the sole invocation (`:3766`). I did **not** run
`--selftest` and did **not** run `check-fd-band-r49.py`: the 167-case count, the PASS, and the stderr text as printed
are the C3 seats' measurement, not mine.

## Findings

1. **C1 is not admissible on the bytes I can see now — the pass variant should not be inserted without the L1's own
   counter run.** A read-only snapshot of the 18 cohort reports at 2026-10-28T17:39:48Z (receipt
   `receipt-cohort-observation.txt`) shows 17 `holds` and one bound negative: `R49CritGR2b` line 1 reads
   `ROW GR2 VERDICT: partly` with line 2 equal to GR2's frozen hash (`.ufo/waves/round-49/w1/R49CritGR2b.md:1-2`).
   By `.ufo/waves/round-49/frozen/FROZEN.md:34-35` a bound negative blocks the row whatever its citations, and
   `check-scrub-admission-r49.py:365` implements exactly that (`blocking.append(seat)`; `row_ok` requires
   `not blocking`, `:378-380`). So on this snapshot `verdicts_ok <= 2` and the predicate FAILS. That is my observation,
   not the counter's run: I did not evaluate citation resolution, body distinctness, `w1-results.json`/dispatch
   entries, `corr_ok`, `quotes_ok` or `marks_ok`. If that seat revises its report or the L1's run differs, the pass
   variant is the one to use; until then the withheld variant is the truthful one.
2. **Two earlier SKILL.md lines state the stale `/tmp` behaviour that round 49 removes, and neither is in my item's
   scope.** `SKILL.md:481-482` says "the selftest now writes only `/tmp/tsukuroi-r3-2-selftest.XXXXXX`
   (`tools/tsukuroi-census.sh:118-120`)", and `SKILL.md:1301` says "the selftest still writes only under its
   `mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX`". The frozen census contradicted that already at R48-C2 and again now:
   the base is `${TMPDIR:-/tmp}` and a dirty TMPDIR resolves to a `/proc/self/fd/<n>` alias inside TMPDIR with never a
   `/tmp` fallback (`census:2083-2098`, usage `:603-609`). My draft 2 notes the correct behaviour but does not correct
   those two lines; the L1 may want a one-line erratum pointing `SKILL.md:481-482` and `:1301` at the round-49 note.
3. **The withheld heading is a deliberate non-mark, and that is load-bearing.** `marks_leg` compares
   `ln.strip() == MARK_SKILL` (`check-scrub-admission-r49.py:313-314`), so `## Scrub grounding — round 49 admission
   (withheld)` satisfies no mark. Inserting the withheld text is therefore safe against a false admission only as long
   as the pass variant is absent; the L1 should insert exactly one of the two.
4. **`SELFTEST_FD_BAND` can change the selftest itself, not only the message.** Beyond the message interpolation
   (`census:2115-2116`), the `(R49-C3)` case reports `bad` and fails the run when the caller already holds descriptor
   240 or 241 (`:3580-3582`, `:3599`), and a substituted band can re-create the auto-allocated-descriptor collision the
   fixed band exists to prevent (`:2069-2078`). Drafted as a named limit in the note rather than as a defect: the
   variable is `SELFTEST_`-prefixed, has no live reader, and is restored by the case.
5. **The C1 mark set is wider than SKILL.md.** `marks_ok == 3` needs the entry heading and a `corpus/README.md`
   sentence as well; `corpus/README.md` (not the repo `README.md`, which does not exist at the freeze —
   `git cat-file` returns `fatal: path 'README.md' does not exist`) is the third surface
   (`check-scrub-admission-r49.py:54,87`). Draft 1a states this so a SKILL-only insert cannot be mistaken for
   admission.

## Gates (what must hold before either draft is inserted)

- Draft 1a: only with a printed PASS at the integrated revision on the predicate of
  `.ufo/waves/round-49/frozen/FROZEN.md:15`, with the entry heading and the `corpus/README.md` sentence landing in the
  same revision. Evidence today points the other way (finding 1).
- Draft 1b: only with a printed FAIL; the blocking seat and verdict must be taken from the counter's
  `per_row.<row>.blocking` field, and the `<seat>`/`<hash>` placeholders must be filled from that JSON.
- Draft 2: renders the `stale_ok`/`diag_ok`/`band_ok` facts of the C3 counter; the L1 should insert it only after
  `python3 tools/check-fd-band-r49.py --revision <REV>` reports `cases == 167` with the three legs at 1, and should
  quote the counter's own line rather than my transcription of the `printf`.

## Not done / limits of this seat

- No counter run (`check-scrub-admission-r49.py`, `check-adjacency-table-r49.py`, `check-fd-band-r49.py`) and no
  `bash tools/tsukuroi-census.sh --selftest`: not named in this item, and the item's cost guard puts the selftest-bearing
  runs with their own seats. Every 167-case/PASS figure above is cited to the code, not measured by me.
- No citation-resolution, body-distinctness, `w1-results.json` or dispatch-task evaluation — the cohort file above is a
  line-1/line-2 snapshot only.
- No Gate-and-probe-registry rows drafted. Item F-8 asks two appends; the `scrub-admission-r49` and `fd-band-r49`
  rows belong in the next `## Gate and probe registry — roundN superseding current rows` table (pattern:
  `SKILL.md:4467`), and that table is the L1's to extend. Nothing in `tools/check-appended-notices.py` forces a record
  for a new heading either: it validates only the records declared in its registry JSON
  (`notices.frozen.py:330,407` iterates the declared records and never enumerates SKILL headings on its own).
- No git/jj mutation anywhere, no lane file edited, no `~/.local/bin` or PATH write, no package install (no tool was
  needed). No pacman transaction.
- Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ScribeSkill/` was removed after the receipts were written (only the
  frozen-byte dumps and the two observations lived there).

## Touched surfaces

- Written: `.ufo/waves/round-49/w1/R49ScribeSkill.md` (this report),
  `.ufo/waves/round-49/w1/R49ScribeSkill/receipt-freeze-bytes.txt`,
  `.ufo/waves/round-49/w1/R49ScribeSkill/receipt-cohort-observation.txt`.
- Read only: lane bytes through `git show 55c07cd3:…` (SKILL.md, tools/tsukuroi-census.sh,
  corpus/knowledge/btrfs-scrub-grounding-r45.md, corpus/README.md, tools/check-scrub-admission-r49.py,
  .ufo/waves/round-49/frozen/FROZEN.md), and the untracked wave reports under `.ufo/waves/round-49/w1/` and
  `.ufo/waves/round-48/w2/`.
- Not touched: `SKILL.md` itself, `corpus/README.md`, the entry, the counters, `SCORECARD.md`, `LOG.md`, the fleet repo,
  `~/.omp`, `~/.agents`, `/home/vgpnk/Projects/shokuknow`.

## Artifacts

- This report: `.ufo/waves/round-49/w1/R49ScribeSkill.md`
- Receipts: `.ufo/waves/round-49/w1/R49ScribeSkill/receipt-freeze-bytes.txt`,
  `.ufo/waves/round-49/w1/R49ScribeSkill/receipt-cohort-observation.txt`
