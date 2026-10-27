VERDICT: draft

# C1ScribeGate — the three admission marks and the S252 Gate row (C1-D1)

Axes: **marks** (all three mark texts are final and machine-checked against the frozen counter's
literals), **C1** (the marks are landable only after GR2 is narrowed a second time and re-read —
see the blocking finding), **depth** (the wave-1 critic's GR2 finding is verified independently
here, and the lesson's S252 row carries a wrong snapshot basename).

No lane file was edited, no host state was touched, no git/jj mutation was run. The only network
call is one read-only `curl` of S252. Scratch was `/fast/scratch/hyaku/tsukuroi-r47/C1ScribeGate/`
(removed after the receipts were copied).

## 1. Blocking finding — GR2 reads `partly`, so the admission marks cannot be landed yet

The counted critic seat `R47CritGR2a` wrote (`.ufo/waves/round-47/w1/R47CritGR2a.md:1-2`):

```
ROW GR2 VERDICT: partly
SECTION SHA256: 909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2
```

Its defective clause, verbatim (`R47CritGR2a.md:19`):

> - DEFECTIVE CLAUSE — "When the unmount suspend path runs, it calls `btrfs_scrub_cancel`" —
>   CONTRADICTED by the pinned snapshot. The quoted call dev-replace.c:1143-1144 sits inside
>   `int btrfs_dev_replace_cancel(...)` (function starts at dev-replace.c:1085), in that
>   function's `case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:` … The actual unmount suspend
>   path, `void btrfs_dev_replace_suspend_for_unmount(...)` …, sets `replace_state =
>   BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED` (dev-replace.c:1182-1187) and contains NO
>   `btrfs_scrub_cancel` call. The only two `btrfs_scrub_cancel` callsites in dev-replace.c are
>   :1111 and :1144, both inside `btrfs_dev_replace_cancel`.

Independently re-checked against the pinned snapshot
`.ufo/waves/round-45/frozen/src/dev-replace.c` (digest `f07ef0a0…4f3a`, per the counter's pin):

- `grep -n "btrfs_scrub_cancel\|^int btrfs_dev_replace_cancel\|btrfs_dev_replace_suspend_for_unmount"`
  → `1085:int btrfs_dev_replace_cancel(`, `1111:\tret = btrfs_scrub_cancel(fs_info);`,
  `1144:\t\tbtrfs_scrub_cancel(fs_info);`, `1171:void btrfs_dev_replace_suspend_for_unmount(`.
- `sed -n '1171,1198p'` shows the suspend function sets
  `BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED`, `time_stopped`, `item_needs_writeback` and returns;
  its closing brace is **1195** (not 1199 — see §6 note), and it contains no cancel call.
- The entry sentence under attack is `corpus/knowledge/btrfs-scrub-grounding-r45.md:73-74`
  ("When the unmount suspend path runs, it calls / `btrfs_scrub_cancel`; once the scrub returns
  and clears its context, the progress query returns `-ENOTCONN`").

Consequence for landing: `tools/check-scrub-admission-r47.py` `run()` makes a row ok only when
`all(s['verdict'] == 'holds' for s in on_cur)` plus `not any_fails` (`tools/check-scrub-admission-r47.py:354-356`).
One bound `partly` on the current hash sets `row_ok` false, so `verdicts_ok` stays ≤ 2 and a
`marks_ok 3` alone cannot produce a PASS. The marks below are therefore **provisional
on the GR2 second narrowing**: if the L1 replaces the misattributed sentence (critic's smallest safe
correction, verified substantively correct) the row's section hash changes and every GR2 seat that
read `909830c8…` is off-current; the residual reviewer `R47ResRevGR2` is already spent (it read the old
bytes `partly`, `C1ScribeGate/binding-state-2.txt`), so a second narrowing can bind only from seats
that have not read the old bytes (`R47ResCritGR2`, `R47Res2RevGR2`, `R47Res2CritGR2`, whichever the
L1 dispatches); GR2 needs ≥ 2 distinct `holds` on the new hash.

Also note for the L1: the trigger of this defect is the round-46 residual critic's own correction,
whose anchor `dev-replace.c:1143-1144` it called "the unmount suspend path" — the anchor belongs to
the cancel ioctl. The pre-wave amendment adopted the anchor without resolving its enclosing function,
and the entry's frozen Limits paragraph (`corpus/knowledge/btrfs-scrub-grounding-r45.md:217-220`)
records the adoption, not its failure. The new Gate-status paragraph below records the second
narrowing; do not let the marks imply the pre-wave bytes passed.

State observed by this seat at 2026-10-27T08:57:00Z (report files only; the counter binds nothing
until `w1-results.json` is committed — at HEAD it prints `w1-results.json unreadable` for every
dispatched seat, `.ufo/waves/round-47/w1-dispatch.json` is tracked, no results file is):

| Row | current section sha256 | reports seen (`holds` on that hash) | counter-bound |
|---|---|---|---|
| GR1 | `fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8` | R47RevGR1a, R47RevGR1b, R47CritGR1a, R47CritGR1b, R47ResRevGR1 | 0 (results absent) |
| GR2 | `909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2` | R47CritGR2a and R47ResRevGR2 both read **partly** (second snapshot 2026-10-27T08:59:17Z, `C1ScribeGate/binding-state-2.txt`) | 0 |
| GR3 | `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` | R47RevGR3a, R47RevGR3b, R47CritGR3a, R47CritGR3b, R47ResRevGR3, R47ResCritGR3 | 0 (results absent) |

These counts are *not* verdicts: quoting `R47CritGR2a.md:1` and `R47RevGR1a.md:1` etc. is a file
read, and the counter's own legs (citations, distinct bodies, K23) have not run.

## 2. Draft (a) — entry block

Land as the new last section of `corpus/knowledge/btrfs-scrub-grounding-r45.md` (after
`## Gate status — round 46 …`, file end at line 264). One header line, one paragraph:

```
## Gate status — round 47 (GR1-GR3 admitted)

The depth gate PASSES at `<REV>`: `python3 tools/check-scrub-admission-r47.py --revision <REV>` reads `structural_ok 1 quotes_ok 3 verdicts_ok 3 marks_ok 3`, and each row's verdicts bind only from counted seats' first two report lines under `.ufo/waves/round-47/` — `ROW GR<n> VERDICT: holds` on the row's current section hash — GR1 through <SEATS-GR1>, GR2 through <SEATS-GR2>, GR3 through <SEATS-GR3>, with two or more distinct bodies per row and no seat reading `partly` or `fails` on the current bytes. GR1 and GR3 were not amended this round. GR2 was narrowed at round 46 (`b57740c2`: the setup returns, the metadata condition, the suspended `-ENOTCONN` timing), amended before wave 1 on the round-46 residual critic's finding (`r1/V46ResCritGR2.md`: the filesystem-closing `-EAGAIN` return at scrub.c:3094-3095 leads the ordering), and narrowed again after the wave-1 critic `R47CritGR2a` showed that the `btrfs_scrub_cancel` call at dev-replace.c:1143-1144 belongs to `btrfs_dev_replace_cancel`'s SUSPENDED arm, while `btrfs_dev_replace_suspend_for_unmount` (dev-replace.c:1171-1195) only records the suspended state; the row now states the cancel path and the unmount path separately. GR1 and GR3 were read at revision `77e9e2b2e96b85d8f048ae2087e246a542b71611` (the freeze revision) and are unchanged at `<REV>`; GR2's second narrowing was read on the bytes of `<REV>`, the revision the counter passes on.
```

Fill rule — the four non-final tokens are data, never hand-guessed:

- `<REV>` = the revision whose counter run PASSes (the commit that carries these marks **and**
  `w1-dispatch.json`, `w1-results.json` and the seat reports).
- `<SEATS-GR1|2|3>` = the per-row seats with `verdict == "holds"` and
  `hash == per_row[row].section_sha256` in that same counter output, joined with `, ` and each in
  backticks. One command prints exactly those strings (verified to run; it prints empty lists when
  the counter binds nothing, as it does at HEAD):

```
python3 tools/check-scrub-admission-r47.py --revision <REV> | python3 -c '
import json,sys
d=json.load(sys.stdin); print("rev", d["revision"], "verdict", d["verdict"], "marks_ok", d["marks_ok"])
for r in ("GR1","GR2","GR3"):
    v=d["per_row"][r]
    print(r, v["section_sha256"], len([s for s,x in v["seats"].items() if x["verdict"]=="holds" and x["hash"]==v["section_sha256"]]),
          ", ".join("`%s`" % s for s,x in v["seats"].items() if x["verdict"]=="holds" and x["hash"]==v["section_sha256"]))
'
```

A §3 variant without the second-narrowing sentence exists only if GR2's bytes do not change; that is
not reachable with a bound `partly` on the current hash, so no such variant is drafted.

## 3. Draft (b) — SKILL.md section

Land at the end of `SKILL.md` (after the round-46 registry table, file end at line 4546):

```
## Scrub grounding — round 47 admission

Appended 2026-10-27 (round-47 C1; drafted by wave seat C1ScribeGate, integrated by the L1). `corpus/knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3 are admitted round 47 at `<REV>` (`python3 tools/check-scrub-admission-r47.py --revision <REV>`, `structural_ok 1 and quotes_ok 3 and verdicts_ok 3 and marks_ok 3`; the verdicts bind from counted seat report bytes only, never from a yield or an orchestrator record).
- GR1 (`## GR1`): a write to `devinfo/<devid>/scrub_speed_max` is parsed by `memparse` — base-0 radix (`0x` hexadecimal, any other leading `0` octal), one `K`/`M`/`G`/`T`/`P`/`E` suffix in either case at 1024 per step, overflow to `ULLONG_MAX`, any trailing text `EINVAL`, a bare newline 0 = no limit (S246, S243).
- GR2 (`## GR2`): a device replace copies through `btrfs_scrub_dev(..., false, true)`; a scrub start is refused `-EINPROGRESS` for a device that already carries a scrub context and for a non-replace call while a replace is started or suspended, after the filesystem-closing `-EAGAIN` and the `-ENODEV`/`-EROFS`/`-EIO` device checks; the replace-cancel ioctl cancels the replace scrub, and the unmount path only records the replace suspended (S247, S242, S243).
- GR3 (`## GR3`): `systemctl stop btrfs-scrub@<instance>.service` under systemd v262 sends `KillSignal=SIGINT` to the whole control group, then SIGCONT, then SIGKILL once the 5 s `TimeoutStopUSec=` has passed; the `canceled` write inside that window stays undecided (S248, S244, S249).
```

(6 physical lines: header, blank, intro, three bullets — inside the 3-8 line bound.)

## 4. Draft (c) — corpus/README.md section and mark line

Land at the end of `corpus/README.md` (after the round-46 coverage note, file end at line 480).
The mark-bearing sentence is its **own physical line** (the counter tests per line):

```
## Round 47 — scrub grounding admission (appended 2026-10-27)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-46 notes above stay as written.

`knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3 are admitted round 47 at `<REV>`: the three scrub-grounding rules now stand as counted admissions (entry `## Gate status — round 47 (GR1-GR3 admitted)`), read with `tools/check-scrub-admission-r47.py` under its frozen predicate, and the entry's round-45 and round-46 gate paragraphs stay as written.
```

The sentence carries both required tokens and no negation; the older negating line in the round-46
note ("SR7, SR8 and SR9 are pending, not admitted") is untouched and does not satisfy the counter on
its own (`tools/check-scrub-admission-r47.py:75-78` requires a line with both tokens and no
`unadmitted|not admitted|never admitted|stay pending|stays pending` match).

## 5. Machine check of the three marks (run now, against the frozen counter's own literals)

The three drafts were checked by importing the frozen counter and applying its exact predicates
(`MARK_ENTRY in entry_lines`, `MARK_SKILL in skill_lines`, the README `all(...) and not NEGATE_RE`
rule). Receipt `.ufo/waves/round-47/w1/C1ScribeGate/marks-check.txt`:

```
MARK_ENTRY repr: '## Gate status — round 47 (GR1-GR3 admitted)'
entry exact-line mark: True
skill exact-line mark: True
readme candidate lines: 1
  negation match: False
readme mark (counter rule): True
entry header line == MARK_ENTRY: '## Gate status — round 47 (GR1-GR3 admitted)'
skill header line == MARK_SKILL: '## Scrub grounding — round 47 admission'
  has tokens: True True
```

This is a literal-level check only; the full `marks_ok` leg can only run on the committed revision.

## 6. Lesson `## Gate` row — S252 (as needed)

**Finding: the round-47 lesson names a snapshot file that does not exist.** `corpus/lessons/round-47.md:27`
and `:29` name `mktemp.1.html`; the frozen directory holds `mktemp.html`
(`.ufo/waves/round-47/frozen/src/SHA256SUMS:1` → `74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266  mktemp.html`;
`FETCH.txt:2` gives the URL). `sha256sum .ufo/waves/round-47/frozen/src/mktemp.html` prints that
digest, so the pin is right and only the basename is wrong. A read-only live re-open at
2026-10-27T08:55:25Z returned the same sha256 and `cmp` identical to the frozen file
(receipt `…/C1ScribeGate/reopen.txt`). The registered quote is verbatim on the page: raw HTML
lines 101-102, `interpret TEMPLATE as a single file name component,` / `relative to a directory:
$TMPDIR, if set; else the`; normalized containment of the registered quote is `True`.

The row itself exists and is correct except for that basename. Exact replacement row:

```
| S252 | https://man7.org/linux/man-pages/man1/mktemp.1.html | "-t interpret TEMPLATE as a single file name component, relative to a directory: $TMPDIR, if set" | mktemp.html:101-102, the -t option description |
```

Exact replacement for the paragraph below the table (adds the re-open receipt; append SrcGate's
independent receipt path when it lands):

```
Snapshot digest: `.ufo/waves/round-47/frozen/src/SHA256SUMS` (mktemp.html `74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266`), fetch log `frozen/src/FETCH.txt`. Live re-open 2026-10-27T08:55:25Z by wave seat C1ScribeGate: sha256 equal and `cmp` identical to the frozen file (`.ufo/waves/round-47/w1/C1ScribeGate/reopen.txt`).
```

Reject rows: no row is needed for S252 — the candidate was admitted and its bytes byte-match on
re-open. The table's `(none yet — updated at integration)` is the L1's line to settle from the whole
wave; this seat records no refused S252 candidate.

Proposed lesson Mistake rows (not applied; outside the marks draft, recorded because the round's
lesson should carry them):

```
| R47-GR2-ANCHOR-MISATTRIBUTION | claim accuracy — a narrowed sentence cited a `file:line` without resolving its enclosing function | the pre-wave GR2 amendment wrote "When the unmount suspend path runs, it calls `btrfs_scrub_cancel`" on dev-replace.c:1143-1144; those lines are inside `btrfs_dev_replace_cancel`'s `BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED` arm (function :1085; the only two cancel calls are :1111 and :1144), and `btrfs_dev_replace_suspend_for_unmount` (:1171-1195) has none — it only records the suspended state | wave-1 counted critic R47CritGR2a (`partly`) | narrow the row per its smallest safe correction and re-read on the new bytes with unused counted seats. Able to fail: resolving each anchor's enclosing function (`sed -n '1171,1195p' dev-replace.c`) separates :1144 from the unmount path |
| R47-LESSON-SNAPSHOT-NAME | evidence handling — a lesson row named a snapshot file that does not exist | `corpus/lessons/round-47.md:27,29` name `mktemp.1.html`; `frozen/src/SHA256SUMS:1` and `FETCH.txt:2` name `mktemp.html`, whose `sha256sum` equals the pinned digest | wave seat C1ScribeGate (this report) | the Gate row's Location and the snapshot sentence now name `mktemp.html`; able to fail: `sha256sum -c SHA256SUMS` in `frozen/src/` reports the missing file the old text would have produced |
```

Note on the critic's own correction text: its proposed replacement writes the suspend function's
extent as `dev-replace.c:1171-1199`; the closing brace is line **1195** (the next function,
`btrfs_resume_dev_replace_async`, starts at 1198). The draft (a) paragraph uses `1171-1195`. The
critic's anchor `:1127-1129` was verified as the SUSPENDED-arm comment.

## 7. Landing checklist (what a PASS requires, in order)

1. Narrow the GR2 sentence (`corpus/knowledge/btrfs-scrub-grounding-r45.md:73-74`) and commit; the
   GR2 section hash changes away from `909830c8…`.
2. Dispatch/collect GR2 residual seats on the new bytes; commit `w1-results.json` (or the residual
   wave's `-results.json`) with exactly one entry per seat and the matching `agent` role — bind()
   requires one dispatch hit, one results entry, and the seat report's first two lines
   (`tools/check-scrub-admission-r47.py:178-219`).
3. Land mark (a), (b), (c) at their exact lines, commit.
4. Run `python3 tools/check-scrub-admission-r47.py --revision <REV>`; require exit 0, `verdict PASS`,
   `structural_ok 1 quotes_ok 3 verdicts_ok 3 marks_ok 3` (the same run proves the marks, so no
   separate marks runner is needed).
5. Fill `<REV>` and the three `<SEATS-…>` tokens from that run (§2 command); re-run the counter after
   the text-only commit (the slots are prose, so no leg changes; this is the audit step, not a new
   binding).

Do not land the marks on the current GR2 bytes: with `R47CritGR2a` bound at `909830c8…`,
`row_ok` is false and the counter exits 1 with `marks_ok` credited but `verdicts_ok` < 3 — a
`FAIL` that would read as a false admission if the marks were quoted without the verdict.

## 8. What I did not do

- Did not run the counter against the wave: it cannot bind anything until the L1 commits the wave's
  results file; at HEAD every dispatched seat reads `w1-results.json unreadable` and
  `waves_seen ['w1']`.
- Did not edit the entry, SKILL.md, corpus/README.md, corpus/lessons/round-47.md, or any other
  tracked lane file; did not commit, stage or stash; no host mutation, no unit/sysfs/package action.
- Did not re-run any seat's verification; the §1 finding was re-derived from the pinned snapshot
  lines only (quoted above), and the seat's other clauses were not re-audited.
- Did not verify the wave's other seats, K23 distinctness or citation resolution — those are the
  counter's legs and the L1's run.

## 9. Receipts

`.ufo/waves/round-47/w1/C1ScribeGate/`:

- `marks-check.txt` — the three-mark literal check (§5).
- `reopen.txt` — S252 live re-open: time, both sha256 values, `cmp` identical, the SHA256SUMS line.
- `section-hashes.txt` — `--section-hash` at HEAD (`f6bc6d05`): GR1 `fe77ac76…`, GR2 `909830c8…`,
  GR3 `43430a14…`, `structural_ok 1`, `problems []`.
- `counter-head.json` — full counter output at HEAD (`verdict FAIL`, `verdicts_ok 0`, `marks_ok 0`,
  `waves_seen ['w1']`, per-seat detail `w1-results.json unreadable`).
- `binding-state.txt` — the report-file first two lines for each `R47*.md` present at
  2026-10-27T08:57:00Z; `binding-state-2.txt` — the GR2 reports at 2026-10-27T08:59:17Z (two
  `partly`, same section hash).
- `draft-entry-block.md`, `draft-skill-section.md`, `draft-readme-section.md` — the byte copies of
  the three drafts checked in §5.
