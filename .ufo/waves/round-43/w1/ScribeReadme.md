VERDICT: draft

Seat `ScribeReadme`, lane round 43 (hyaku run 9), wave w1 — item F-5. Three append-only notes drafted for the L1
integrator (`AgentR43`): one `corpus/README.md` coverage row, one `## Frontier` section for
`corpus/knowledge/btrfs-scrub-record-r43.md`, one `PROVINCE.md` note under the storage Frontier scrub-record line.
Nothing was written in the lane; the drafts were validated on a scratch clone and are reproduced byte-exact below.

## 1. What I read (and the anchors the drafts rest on)

- `corpus/README.md` (414 lines before the append): the coverage map `| Note | Holds | Sources |` at
  `corpus/README.md:3-8` (header `:5`), the `## Frontier` bullets at `:28-40`, and the appended-round convention —
  round 39 `:303`, round 40 `:319`, round 41 `:355`, round 42 `:406-414` (`## Round-42 coverage note (appended
  2026-10-26)` with `| Entry | What it adds | Sources / evidence |` at `:408`). The last content line before my
  append is `:414`.
- `PROVINCE.md` (244 lines): `## Core` `:6`, `## Round-26 frontier — storage integrity` `:154-171` (the promotion
  condition "This area becomes Core only after a census arm exists", `:169`), `## Round-38 promotion —
  R38-STORAGE-CORE` `:199` (Still Frontier = scrub record + NVMe SMART), `## Round-39 limit closure` `:225`, and the
  storage Frontier scrub-record line itself —
  `**Round-42 note — scrub record read from source (appended 2026-10-26).**` at `PROVINCE.md:239-244`.
- `corpus/knowledge/btrfs-scrub-record-r43.md` (131 lines): Scope `:7-15`, SR1 `:17`, SR3 `:45`, SR6 `:80-112`
  (statement `:82-88`, the six S240 `ioctl.c` capability quotes `:98-108`, host reading `:110-112`), `## How this
  changes OS triage` `:114-122` ("Running state is an elevation-gated reading", `:122`), `## Limits` `:124-131`
  (last line "No census arm reads the record; this entry stays on Frontier ground.", `:131`).
- `.ufo/waves/round-43/frozen/hostcap/capture.txt` (sha256 `f7ecbe7c…`, matches
  `tools/check-scrub-record-r43.py` `CAPTURE`): `:2` `uid 1000 euid_caps 0000000000000000`; `:6`
  `scrub_progress_ioctl devid=1 errno=EPERM (1)`; `:7` `var_lib_btrfs absent`; `:8` `scrub_status_exit 0`; `:10`
  `scrub_status| \tno stats available`.
- `tools/check-scrub-record-r43.py` (read in full, 339 lines): `sections()` collects only `^## (SR\d)$` and resets
  on any other `^## ` line (`:108-123`, reset at `:116-118`); the predicate is
  `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and
  novelty_base_hits == 0 and pointer_ok == 1` (`:90-91`, repeated in `main`); `verdicts_ok` counts only
  `C2RevSR<n>`/`C2CritSR<n>` bound through `w2-dispatch.json` + `w2-results.json` + `.ufo/waves/round-43/w2/<name>.md`
  (`:20-31` docstring, `bound()` `:178-195`, row loop `:282-295`), so wave-1 reviews are not verdicts.
- `SCORECARD.md:2648-2684` "Round 43 — declaration", including its Causal separability sentence (`:2683-2684`:
  "C2 touches the r43 entry, the r42 entry's header line, `corpus/SOURCES.md` and frozen snapshots").
- `corpus/SOURCES.md:246,249,250` (S237, S240, S241): S240/S241 `used_by` cells name
  `corpus/knowledge/btrfs-scrub-record-r43.md`, which is what `sources_ok` reads (`tools/check-scrub-record-r43.py:304-317`).

## 2. Draft 1 — `corpus/README.md`, one coverage row (append after `:414`)

```markdown

## Round-43 coverage note (appended 2026-10-26)

| Entry | What it adds | Sources / evidence |
|---|---|---|
| `knowledge/btrfs-scrub-record-r43.md` | Storage-integrity frontier, scrub record, re-grounding the two rows round 42 withdrew and the running-state limit it stated from a host errno alone: SR1 the record update path — `scrub_write_progress` opens `scrub.status.<fsid>_tmp` with `O_WRONLY\|O_CREAT` and no `O_TRUNC`, writes the record from the start of that file, renames `_tmp` over the record only after a write that returned no error, and unlinks no `_tmp` (all three `unlink` calls name the progress socket), so an old file's trailing bytes can ride into a shorter record [inference, not reproduced]; SR3 `btrfs scrub resume` runs `scrub_start(…, true)`, and the first record it writes for a resumed device carries the interrupted run's counters, its `t_start` and the two durations summed, while a failed progress or final record write prints only under `do_print` (set by `-B`, cleared when output is quiet) and assigns no `err`; SR6 the running state comes only from `BTRFS_IOC_SCRUB_PROGRESS` through `is_scrub_running_in_kernel`, which reads any failed call as not running, and Linux v7.2.11 returns `-EPERM` there without `CAP_SYS_ADMIN`, so an unprivileged status never prints `running` | S237, S240 (opened this round), S241; `../tools/check-scrub-record-r43.py` (frozen, sha256 `b4602c56…`); capture `.ufo/waves/round-43/frozen/hostcap/capture.txt` (sha256 `f7ecbe7c…`); `../SCORECARD.md` "Round 43 — declaration"; `lessons/round-43.md` Gate (not yet written at draft time) |
```

Format decision: three columns (`Entry | What it adds | Sources / evidence`), matching the two immediately preceding
appended rounds `corpus/README.md:408` and `:367`, not the top map's `Note | Holds | Sources` (`:5`); rounds 39-42 all
use the three-column form. Pipes inside the cell are escaped `\|` as in `corpus/README.md:410`. If the L1 prefers the
top map's header names, only the header cells change, not the row.

Deliberately not drafted: a `### Frontier notice — round 43` paragraph in README. The round-39…41 precedent has one,
but item F-5 puts the Frontier statement in the entry and `PROVINCE.md`; adding a third copy would restate the same
promotion condition in three files. (Round 42 also kept its README Frontier paragraph to the surface statement.)

## 3. Draft 2 — `corpus/knowledge/btrfs-scrub-record-r43.md`, `## Frontier` section (append after `:131`)

```markdown

## Frontier

This entry stays on Frontier ground: it states the record's write discipline, its resume arithmetic and the gate on
the running state, and no read-only census arm reads the record yet, which is the round-26 condition for this area to
become Core (`PROVINCE.md` "Round-26 frontier — storage integrity"). SR6 bounds what such an arm can decide. The
record itself needs no privilege: as uid 1000 with no effective capabilities (capture.txt:2) `btrfs scrub status /`
exited 0 and printed `no stats available` (capture.txt:8, capture.txt:10), with no record present (capture.txt:7). The
kernel's running state does need privilege: the progress ioctl on `/` for devid 1 failed with `EPERM` (capture.txt:6),
so an unprivileged arm can report the record's absence, its contents and its permissions, and never "a scrub is
running". A status that prints `no stats available` reports a missing record, not the absence of a scrub (SR6).

What this page does not settle. SR1's trailing-bytes consequence is an inference from the open flags and was not
reproduced (no record exists here, capture.txt:7). The kernel side is upstream v7.2.11 source only; whether the Arch
kernel patches `fs/btrfs/ioctl.c` is unchecked (`## Limits` above). Rows SC2, SC4 (as narrowed) and SC5 of the
round-42 entry are neither restated nor re-verified here. A counted verdict exists only as the wave-2 seat verdicts
bound through `.ufo/waves/round-43/w2-dispatch.json` and `w2-results.json`
(`python3 tools/check-scrub-record-r43.py --revision <REV>`); the wave-1 reviews of this text are its first
falsifiers, not verdicts.

Nothing on this page runs a scrub, writes `/var/lib/btrfs` or calls a privileged ioctl. Running a scrub, enabling
`btrfs-scrub@.timer`, resetting a device counter and any repair remain operator-owned.
```

Every factual clause maps to the entry or the capture: capability gate and `-EPERM` → SR6 `:84-88` and S240 quotes
`:102-108`; record readable unprivileged → capture `:8,:10`; record absent → `:7`; leftover-tail inference and its
unreproduced status → SR1 `:19-25` (consequence `:23-25`), `## Limits` `:129-130`; Arch patch question → `## Limits`
`:126-128`; non-restated
round-42 rows → Scope `:14`; verdict binding → counter docstring `:20-31` and `verdicts_ok` code `:282-295`.

## 4. Draft 3 — `PROVINCE.md`, note under the storage Frontier scrub-record line (append after `:244`)

```markdown

**Round-43 note — the record read is unprivileged, the running state is not (appended 2026-10-26).** The scrub record
stays Frontier and the promotion condition is unchanged: this area becomes Core only after a read-only census arm reads
it (the round-26 section above, "This area becomes Core only after a census arm exists"). Round 43 grounds what such an
arm must not claim. `btrfs scrub status` decides whether a scrub is running only from `BTRFS_IOC_SCRUB_PROGRESS` through
`is_scrub_running_in_kernel`, which reads any failed call as not running, and Linux v7.2.11's
`btrfs_ioctl_scrub_progress` returns `-EPERM` before doing anything unless the caller has `CAP_SYS_ADMIN` — as do the
scrub start and cancel ioctls (`corpus/knowledge/btrfs-scrub-record-r43.md` § SR6, S240). On this host, uid 1000 with
no effective capabilities got `EPERM` from that ioctl (`.ufo/waves/round-43/frozen/hostcap/capture.txt:6`) while
`btrfs scrub status /` exited 0 (capture.txt:8), so the record read is unprivileged and the running state is
elevation-gated: an unprivileged arm can report a record's absence, its contents and its permissions, never "running",
and `no stats available` is the absence of a record, not evidence that no scrub runs. Round 43 also re-grounds, as SR1
and SR3, the write-discipline and resume text round 42 withdrew; no record exists on this host (capture.txt:7), so
neither row has a host instance. **Still Frontier, unchanged:** the record, `btrfs scrub status` and
`btrfs-scrub@.timer`; NVMe SMART is untouched by this note. **Operator-owned, unchanged:** running a scrub, enabling
its timer, resetting a counter. Counted by `python3 tools/check-scrub-record-r43.py --revision <REV>`
(`SCORECARD.md` "Round 43 — declaration"). No package, service, mount, scrub, counter-reset, firmware or configuration
action is authorized by this paragraph.
```

Placement and style follow the round-42 note it sits under (`PROVINCE.md:239-244`): a bold lead-in paragraph inside the
existing `## Round-39 limit closure` section rather than a new `##` heading, so no earlier `PROVINCE.md` line number
moves (`PROVINCE.md:244` stays the last line of the round-42 note; the note starts at `:246`).

## 5. Validation actually run (scratch clone, no lane write)

Scratch: `/fast/scratch/hyaku/tsukuroi-r43/ScribeReadme/` (now removed). `export TMPDIR` into it; all fixtures below it.

1. `git clone -q --shared <lane> $S/lane` → `git -C $S/lane rev-parse --show-toplevel` =
   `/fast/scratch/hyaku/tsukuroi-r43/ScribeReadme/lane` (toplevel asserted before any commit); `remote remove origin`;
   HEAD `7d0ed1c2d62961cbde8a4d6be120b2573ebbd8f9` (lane git tip; base `6951ead9` is its ancestor `git log --oneline`).
2. Baseline counter, tip `7d0ed1c2`:
   `python3 tools/check-scrub-record-r43.py --lane $S/lane --revision 7d0ed1c2` → exit 1,
   `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, verdicts_ok 0, novelty_base_hits 0, pointer_ok 1,
   verdict FAIL` (`c2-before.json`). The FAIL is the mid-round state: the w2 verdict seats are not bound yet.
3. Applied Drafts 1-3 to the clone (append only), committed with
   `-c user.name=fixture -c user.email=fixture@invalid` → `21c6cb8679a4e666e5a3b12d4ed41d8b1ed0c4b2`,
   `3 files changed, 46 insertions(+)`.
4. Counter at the draft commit: **every conjunct identical to the baseline**, same FAIL for the same reason —
   `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, verdicts_ok 0, novelty_base_hits 0, pointer_ok 1`
   (`c2-final.json`, diff of the two files is empty on those keys). This is the check that the appended `## Frontier`
   heading does not disturb `sections()`: a `## ` heading closes the SR6 section (`tools/check-scrub-record-r43.py:116-118`),
   and the new section sits after `## Limits`.
5. Row shape: the appended README line has 5 raw cells (2 outer delimiters + 3 columns) with the pipe inside the cell
   escaped, and the file has no trailing whitespace; `corpus/README.md` newline count after the append = 420.
6. Entry headings after the append: `SR1, SR3, SR6, How this changes OS triage, Limits, Frontier`.
7. Lane untouched: `git status --porcelain | grep -v '^?? \.ufo/'` → 0 lines; `git hash-object` of
   `corpus/README.md` = `95b83b2b…`, `PROVINCE.md` = `34c2495b…`, `btrfs-scrub-record-r43.md` = `98258c5a…`, each
   identical to `git show 7d0ed1c2:<path> | git hash-object --stdin`. The repo's Git index received nothing from this
   seat; the only lane path written is this seat's own `.ufo/waves/round-43/w1/ScribeReadme*`.

## 6. Findings for the L1

**F-5a (action required, not a defect in the drafts): appending the README row moves a live axis count.**
`tools/check-self-assessment.py` K11 compares the *current* axes table's stated `corpus/README.md` count with the
observed newline count at the evaluated revision (`:628-637`); the table at `SCORECARD.md:2615` ("round 42 final
measured surface") states 414 on its coverage row (`:2622` per the check's `stated_line`). Measured on the clone:

- `check-self-assessment.py --repo $S/lane --revision 7d0ed1c2 --scratch $S/sa` → `FAIL 27 2`;
  K11 `match`, stated 414 / observed 414; the two mismatches are K07 ("depth row states 63 notes;
  `corpus/knowledge` holds 64 .md files") and K10 ("depth row states 60 lesson files; `corpus/lessons` holds 61
  files") — both already stale at the tip, before any scribe edit (`sa-before.json`).
- Same command at the draft commit `21c6cb86` → `FAIL 27 3`; K11 becomes `mismatch`, "coverage row states 414
  `corpus/README.md` lines; the file holds 420 newline characters" (`sa-final.json`).
So the round-43 "axes — current self-assessment" table must state `corpus/README.md` 420 `wc -l` (and fix the K07/K10
counts) for `check-self-assessment.py` to be clean at the outcome revision. This is the same maintenance every
previous README append implied (round 42's table states the post-r42 count, 414); it is reported, not applied —
the axes table is the L1's file.

**F-5b (scope note): the declared Causal separability list does not name these two ledgers.**
`SCORECARD.md:2683-2684` lists C2's touched paths as the r43 entry, the r42 header line, SOURCES and frozen snapshots.
Drafts 1 and 3 add `corpus/README.md` and `PROVINCE.md` as documentation surfaces. Measure 5 of §5 shows the C2
counter is byte-insensitive to them (identical conjuncts), and no other round-43 counter reads README or PROVINCE; the
one coupling is F-5a. If the L1 wants the declaration's list exact, it needs an append-once amendment line, not a
rewrite.

**F-5c (provenance limit): the drafts, not the notes, are what this report proves.**
Wave-1 reviews are first falsifiers, per §1's counter reading; nothing here makes SR1/SR3/SR6 "holds". The drafts are
byte-exact as appended (`drafts.diff` is `git diff 7d0ed1c2 21c6cb86`), but the fixture revisions die with the scratch
clone, so re-measurement means re-applying `drafts.diff` to a fresh clone — the receipts record the numbers, the diff
records the bytes.

**F-5d (small, honest): `corpus/lessons/round-43.md` does not exist at draft time** (`ls corpus/lessons/` stops at
`round-42-verifier-spotcheck.md`, `round-42.md`). The README row's Sources cell therefore says
"`lessons/round-43.md` Gate (not yet written at draft time)" rather than citing a row set that has no file behind it.
L1 can drop the parenthetical once the Gate lands, or keep it as the provenance of this draft.

## 7. Not done (and why)

- No lane file, index entry, commit, `git`/`jj` mutation, or fleet-root file was written; no scrub, no
  `device stats -z`, no privileged ioctl, no mount, no package/service action, no `sudo`. Only the read-only
  `BTRFS_IOC_SCRUB_PROGRESS` probe result already frozen in `capture.txt:6` was cited, not re-run.
- No tool installed or upgraded (nothing was missing: `git`, `python3` sufficed); `pacman` untouched.
- Not verified by me: SR1/SR3/SR6 semantics against the source lines (that is `C2RevSR*`/`C2CritSR*` wave-1/2 work);
  whether an unprivileged census arm is *worth* adding (a round decision, not a scribe one); `PROVINCE.md`'s
  round-26/38/39 sections beyond the anchors quoted in §1.
- Not drafted: a README `### Frontier notice` paragraph (§2), a `SKILL.md` registry row (not in F-5's item list), and
  the axes-table update (F-5a, L1's file).

## 8. Artifacts

- This report: `.ufo/waves/round-43/w1/ScribeReadme.md`
- `.ufo/waves/round-43/w1/ScribeReadme/drafts.diff` — `git diff 7d0ed1c2 21c6cb86`, the three append-only blocks
  byte-exact (7.0 KB)
- `.ufo/waves/round-43/w1/ScribeReadme/c2-before.json` — frozen C2 counter at the tip `7d0ed1c2`
- `.ufo/waves/round-43/w1/ScribeReadme/c2-final.json` — same counter at the draft commit `21c6cb86` (conjuncts
  identical; both FAIL on `verdicts_ok 0`)
- `.ufo/waves/round-43/w1/ScribeReadme/sa-before.json` — `check-self-assessment.py` at `7d0ed1c2` (K11 match 414/414;
  K07/K10 stale)
- `.ufo/waves/round-43/w1/ScribeReadme/sa-final.json` — same at `21c6cb86` (K11 mismatch 414/420; F-5a evidence)
