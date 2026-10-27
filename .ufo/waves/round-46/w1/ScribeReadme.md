VERDICT: draft

# ScribeReadme — item F-6: the round-46 knowledge-index row and the round-44 D1 status note

Seat `ScribeReadme`, round 46 wave w1. Drafted, not landed by this seat: no lane file was written. Two things changed
under the item while it ran: the lane moved three commits (`a4477049` → `b57740c2` → `61e06740` → `c7e4d7d9`) and the
L1 **already landed** a `## Round-46 coverage note` and a round-44 D1 status paragraph at `c7e4d7d9` (480-line
`corpus/README.md`). So this report gives (3.1) the exact corrective append that closes the gaps in what landed, and
(3.2) the exact full section drafted from the item's revision, for the L1 to choose between. Both are patch-checked
against the tip; evidence in `ScribeReadme/evidence.txt`, bytes in `ScribeReadme/append.md` (3.2) and
`ScribeReadme/correct.md` (3.1).

Axes this item moves: **coverage** (the knowledge index names the new entry) and **depth** (the index stops presenting
unadmitted rows as holdings). No Frontier/Core line is moved or re-worded by either option: both append after the last
line and leave lines 1-466 (and 1-480) byte-identical.

## 1. State of the two items

| Item | State in committed bytes |
|---|---|
| (a) knowledge-index row for `corpus/knowledge/census-identity-r46.md` | Absent at `a4477049`, `b57740c2` and `61e06740` (`corpus/README.md` 466 lines, no `census-identity` string). Landed by the L1 at `c7e4d7d9` as a table row at `corpus/README.md:474`. |
| (b) D1: README:434 and `:440-452` never say the round-44 depth gate FAILED | Reproduced at `a4477049` and at the tip: `git show <REV>:corpus/README.md \| sed -n '427,452p' \| grep -n -i -E 'fail\|pending\|admit'` is empty (exit 1) at both revisions. Landed by the L1 at `c7e4d7d9` as the paragraph at `:476-480`. |

The D1 premise is therefore confirmed in committed bytes, and it is still visible in the file as the L1 left it:
`:434` and `:440-452` are untouched, and the status lives at `:476-480`.

## 2. Where text goes (line numbers)

At `a44770491eb5ca15ce9f8b3207309d1af683ffaf` (the revision the item pins), `corpus/README.md` is 466 lines
(`sha256 f4e39671…7e7ca`), last line `:466` = `and GR1-GR3 are pending, not admitted (entry section "Gate status —
round 45").` — the end of the round-45 note. `git diff --stat a4477049 b57740c2 -- corpus/README.md` and
`a4477049 61e06740 -- corpus/README.md` are both empty, so the same 466-line base held at those two revisions.

At the tip read here, `c7e4d7d99892ea36b7ac3c83be32b8bcf25a9d57`, `corpus/README.md` is 480 lines and the landed
round-46 section occupies `:468-480`. The full line map for both options, including the heading counts, is
`ScribeReadme/line-map.txt`.

- 3.1 appends after `:480` → 481-503 (23 lines), file 503 lines.
- 3.2 replaces `:468-480` (13 landed lines) with its 45 content lines → 512 lines. It is byte-identical to
  (466-line base) + (one blank line) + (45 lines), i.e. the file the item's revision would have carried.

## 3. Exact proposed Markdown

### 3.1 Recommended: corrective append after `corpus/README.md:480` (`ScribeReadme/apply-A.diff`, 23 insertions, 0 deletions)

This keeps the L1's own fresh lines and adds only what the landed text does not say. Apply:
`git apply -p1 .ufo/waves/round-46/w1/ScribeReadme/apply-A.diff` at a revision whose `corpus/README.md` is 480 lines.

```markdown

### Round-46 index row — the fields, the counter and the round-44 receipt (appended 2026-10-27)

Append-only; the row at `:474` and the round-44 status paragraph at `:476-480` stay as written, and no
Frontier/Core line moves. Read them with this:

- **The fields and the CLI contract.** The row names "sha256, md5, bytes and newline count"; the line's fields, in
  order, are `version=… sha256=… md5=… bytes=… lines=… planes=… exit_map=… verified=yes|no`, printed once before
  any plane probe with exit 0. `--identity` with any other argument (`--selftest`, `--help`) prints
  `--identity takes no other argument` and exits 2 (`../tools/tsukuroi-census.sh:3518-3522`). `lines` counts
  newline bytes, and `version` stays the literal `census-v2`, so the sha256 alone names the revision.
- **Sources in the round-45 row's shape.** That row's Sources cell names its counter
  (`tools/check-scrub-grounding-r45.py`) and its frozen snapshot (sha256 `f5958a83…`); this round's are
  `tools/score-census-identity-r46.py --revision <REV> --scratch <DIR>` and
  `.ufo/waves/round-46/frozen/src/SHA256SUMS` (sha256 `02fa1d2d…`), with `FETCH.txt` for the fetch log.
- **`:476` reads "the row above".** The round-44 row is at `:434`, above the round-45 note; the row directly
  above that sentence is this round's census-identity row.
- **The FAILED mark's chain.** The round-44 legs are rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1,
  verdicts_ok 0, novelty_base_hits 0, pointer_ok 1, verdict FAIL
  (`.ufo/waves/round-44/after/c2-final-fbfef071.jsonl`,
  `corpus/lessons/round-44-verifier-spotcheck.md:84`), against a predicate that requires `verdicts_ok == 3`
  (`../tools/check-scrub-record-r44.py:50-51`); the SR8/SR9 narrowings made after the counted reads were judged by
  no counted seat (that lesson §2 C2).
```

### 3.2 The item's own draft: one section, appended after a 466-line `corpus/README.md` (`ScribeReadme/append.md`; `apply-B.diff` replaces `:468-480` at the tip)

Use this if the L1 prefers one self-contained section rather than a corrective append. Validated at both bases:
applying `apply-B.diff` at `c7e4d7d9` yields 512 lines and bytes equal to (base 1-467 + this block); applying
`append.md` after `:466` at `b57740c2` gave `46 0` in `git diff --numstat`, 512 lines, `cmp` identical to the
simulated file, and `git apply -R --check` OK.

```markdown

## Round-46 coverage note (appended 2026-10-27)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-45 notes above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/census-identity-r46.md` | The census's own identity in one command: `bash tools/tsukuroi-census.sh --identity` prints one `TSUKUROI_CENSUS_IDENTITY: version=… sha256=… md5=… bytes=… lines=… planes=… exit_map=… verified=yes\|no` line before any plane probe and exits 0, while `--identity` with any other argument (`--selftest`, `--help`) prints `--identity takes no other argument` and exits 2. The digests are read through the descriptor bash holds the script on (`/proc/$$/fd/<n>`; bash moves the script to a high descriptor, normally 255, capped at `HIGH_FD_MAX` 256) and a descriptor qualifies only when it is 10 or more, a regular file, its link equals `readlink -f` of the invoked path, its `flags:` line in `/proc/$$/fdinfo/<n>` carries `O_CLOEXEC` (`02000000`), and exactly one descriptor qualifies; a script read from stdin (`BASH_SOURCE[0]` unset), through a pipe or process substitution (`pipe:[…]`), a file replaced after bash opened it, a relinked path, or an ambiguous match prints `unverifiable` in the four byte fields and `verified=no`, and a path is never hashed on trust. `lines` counts newline bytes as `wc -l` does; sha256 is taken again after md5, bytes and lines, and all four print only when both sha256 reads agree. The sha256 names a revision (hash each committed census blob and compare); `version` stays the literal `census-v2` | S250 (bash tag bash-5.3 `shell.c`, `general.c`, `general.h`), S251 (`proc_pid_fd(5)`); `.ufo/waves/round-46/frozen/src` (SHA256SUMS + FETCH.txt); counter `tools/score-census-identity-r46.py` |

Frontier: nothing moves. `--identity` extends the existing host-census gate (`../PROVINCE.md`, the
`../tools/tsukuroi-census.sh` row) and claims no new coverage-map ground; the mode runs no plane probe and writes
nothing (`../tools/tsukuroi-census.sh:3467-3513`, the `nowrite_ok` leg), so the storage, boot and boot-loader
frontiers stay as the round-38 to round-45 notes leave them. Measured with
`../tools/score-census-identity-r46.py --revision <REV> --scratch <DIR>` at the revision named in
`../SCORECARD.md` "Round 46 — measured outcome" (predicate identity_ok == 1 and tracks_ok == 1 and symlink_ok == 1
and unverifiable_ok == 1 and cli_ok == 1 and nowrite_ok == 1 and selftest_pass == 1 and selftest_r46 >= 4); the
selftest cases carrying the label `(R46-C1)` are the entry's own.

## Round-44 correction — the depth gate FAILED and SR7-SR9 are pending (appended 2026-10-27, routed D1)

Append-only; the round-44 note above, its row at `:434` and its paragraph at `:440-452` stay byte-for-byte as
written, and no Frontier/Core line moves. Read that note with this status:

- **The round-44 depth gate FAILED.** `tools/check-scrub-record-r44.py` at `fbfef071` reports rows 3, quotes_ok 3,
  props_ok 3, host_ok 3, sources_ok 1, verdicts_ok 0, novelty_base_hits 0, pointer_ok 1: three rows measured, no
  counted seat bound a verdict (`.ufo/waves/round-44/after/c2-final-fbfef071.jsonl`), against a predicate that
  requires `verdicts_ok == 3` (`tools/check-scrub-record-r44.py:50-51`).
- **SR7-SR9 are pending, not admitted.** `:434` lists what the entry holds; it is not a pass mark. The SR8/SR9
  narrowings made after the counted reads were judged by no counted seat
  (`corpus/lessons/round-44-verifier-spotcheck.md` §2 C2, its D3, carried as D1 in
  `corpus/lessons/round-45-verifier-spotcheck.md` §5). The entry carries the same status in
  `knowledge/btrfs-scrub-record-r44.md` section "Round-45 grounding and gate status"; D1 names the same status for
  `SKILL.md` section "Scrub record — round 44 rows".
- **The grounding is not the admission.** Round 45 grounded the three `[inference]` marks from source
  (`knowledge/btrfs-scrub-grounding-r45.md`, rows GR1-GR3) and bound none of them either (round-45 gate FAILED,
  `verdicts_ok` 0, `:462-466`). The round-46 attempt is counted by `tools/check-scrub-admission-r46.py`
  (`r45_legs_ok == 1 and verdicts_ok == 3 and marks_ok == 3`); until that counter reports `verdicts_ok 3` at a
  measured revision, SR7-SR9 stay pending.
- **The Frontier/Core split at `:436-444` is unaffected.** The promotion rests on the round-44 census arm
  (`../tools/tsukuroi-census.sh` `probe_scrub_record`, counted by `tools/score-scrub-arm-r44.py`), not on the depth
  rows; the record's content, the running state and NVMe SMART/Health stay Frontier exactly as `:441-444` writes
  them, and running, canceling, resuming or limiting a scrub stay operator-owned.
- **The round-45 lesson's D3 row credits a half-close.** `corpus/lessons/round-45.md:94` marks the defect closed and
  credits `194a4523` with the mark in `corpus/README.md`; that commit appended only the round-45 note's sentence
  (`:465-466`, GR1-GR3 pending), and `:434` with `:440-452` still carries no status — the half-close
  `corpus/lessons/round-45-verifier-spotcheck.md` §5 routes as D1.
```

## 4. What the landed text (c7e4d7d9:468-480) does and does not say

| Point | Landed at `:474`/`:476-480` | Verdict |
|---|---|---|
| Reads through a unique close-on-exec script descriptor of 10 or more resolving to the invoked path | yes, in those words | matches `tools/tsukuroi-census.sh:3481-3513` at the tip (`>=10`, regular file, link = `readlink -f $SELF`, `flags:` carries `O_CLOEXEC`, `hits -eq 1`) |
| `unverifiable` for stdin, pipes, a path relinked after open, ambiguous or inherited descriptor | yes | matches the entry §"Which bytes it names" |
| The sha256 → commit `git log` loop | yes | matches the entry §"Re-deriving the revision from the line" |
| The line's full field list (`version` … `verified`), `planes`, `exit_map` | no | gap; 3.1 bullet 1 |
| `--identity` refuses every other argument with exit 2 (`--selftest`, `--help`) | no | gap; the contract at `tools/tsukuroi-census.sh:3518-3522` |
| Sources cell names the counter and the frozen snapshot, as the round-45 row does | no — only S250/S251 | gap; 3.1 bullet 2 |
| Round 44's depth gate FAILED, `verdicts_ok 0` | yes | D1 satisfied |
| The receipt and the predicate behind that | partially — cites the lesson lines `:84,:133`, not the JSONL receipt or `check-scrub-record-r44.py:50-51` | thin; 3.1 bullet 4 |
| "the row above for `knowledge/btrfs-scrub-record-r44.md` (`:434`)" | says "the row above" | **false as written**: at `:476` the row directly above is the census-identity row at `:474`; the r44 row is 42 lines above. 3.1 bullet 3 |
| SR7-SR9 pending, not admitted | yes | D1 satisfied |
| Frontier: nothing moves | yes | consistent with the round-46 declaration (C1 is the operability axis; PROVINCE carries no round-46 section) |

No Frontier/Core line moved in the landed text, and none moves under either option.

## 5. Findings

1. **The D1 headline defect is real and half the round-45 lesson credits it as closed.** `corpus/lessons/round-45.md:94`
   ("D3 C2 unadmitted mark | closed") credits `194a4523` with the mark in `corpus/README.md`. That commit's README hunk
   (`git show 194a4523 -- corpus/README.md`) appends exactly two lines to the round-45 Frontier paragraph — now
   `:465-466` — and touches neither `:434` nor `:440-452`. The row is therefore true of the round-45 rows and false of
   the round-44 rows; that is the half-close D1 names. `ScribeLesson-2` reproduced the same state independently and is
   carrying D1 as `partial` in the round-46 lesson.
2. **The round-44 receipt chain D1 relies on** is `verdicts_ok 0` against a predicate requiring 3: aggregate record of
   `.ufo/waves/round-44/after/c2-final-fbfef071.jsonl` = `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1,
   verdicts_ok 0, novelty_base_hits 0, pointer_ok 1`; `tools/check-scrub-record-r44.py:50-51` states the predicate.
   The same legs are restated in `corpus/lessons/round-44-verifier-spotcheck.md:84` and its verdict table at `:133`.
3. **The census identity moved after the item's revision, and the index row must not describe the old algorithm.**
   `61e06740` replaced the "try 255 first, then any descriptor ≥10" rule with an `O_CLOEXEC` + exactly-one-descriptor
   rule (`tools/tsukuroi-census.sh:3467-3513`, entry `:34-40`). A row drafted from `a4477049` alone would be stale at
   the measured revision; both option texts above describe the tip.
4. **Observed identity lines** (observation, not the counter): running `--identity` while the worktree held the
   `a4477049` bytes printed `sha256=d925839c…`, `bytes=209208 lines=3598`, `verified=yes`, rc 0; at the `61e06740`
   bytes it printed `sha256=ac4e38ff…`, `bytes=210762 lines=3622`, `verified=yes`, rc 0 — equal to
   `git show 61e06740:tools/tsukuroi-census.sh | sha256sum`. `--identity --selftest` (on the `a4477049` bytes) and
   `--identity --help` (on the `61e06740` bytes) each exit 2 with `tsukuroi-census: --identity takes no other
   argument`, and neither run created a file in the scratch
   cwd or `TMPDIR`.
5. **K11 consequence for the self-assessment.** `tools/check-self-assessment.py` K11 compares the coverage cell's
   stated `corpus/README.md N \`wc -l\`` with the file's newline count at the same revision. With 3.1 the count is
   503 (`480 + 23`); with 3.2 it is 512. Any other README append (the C2 mark line) shifts it again, so the number
   must be measured in the commit that lands the axes table (as `SelfAssess` states).
6. **The C2 README mark must not be produced by this text.** `tools/check-scrub-admission-r46.py` reads its README mark
   as a line containing both `btrfs-scrub-grounding-r45.md` and `admitted round 46`. No line of either option carries
   both (checked mechanically), so neither can grant that mark. `C2CritLimits` was told to keep its own line to one
   line and to append after mine.
7. **Item-text nit, not a defect in the file:** the item calls the round-44 paragraph `:440-452`; at the pinned
   revision the paragraph starts at `:438` (the heading is `:436`) and `:440-452` is the body the item means. The
   landed text inherited the same range.

## 6. Not done

- No counter was run (`score-census-identity-r46.py`, `check-scrub-admission-r46.py`, `check-self-assessment.py`,
  `check-adjacency-anchors.py`): the item is a draft, and the C1 counter is the L1's once-per-round cost. Reading the
  committed round-44 receipt is not a re-run and is not treated as one.
- No census selftest was run; the two `--identity` invocations above run no plane probe and write nothing (cwd and
  `TMPDIR` snapshotted empty before and after).
- No lane file was created, edited or deleted; no `git add/commit/stash/checkout/reset/push` and no jj command ran in
  the lane. The only git writes were in a throwaway clone under
  `/fast/scratch/hyaku/tsukuroi-r46/ScribeReadme/` (its `rev-parse --show-toplevel` was checked to equal the clone
  path before any patch), and the scratch dir is removed at the end.
- No host query beyond read-only reads (`git show`, `grep`, `sed`, `/proc` reads through the census); no package,
  service, unit, sysfs, mount or namespace action; no tool installed or upgraded, so there is no install line.
- Two reports were sent by message and are not evidence here: `SelfAssess` (counts 503/512, K11 shape) and
  `C2CritLimits` (append placement, one-line mark constraint).

## 7. Receipts (`.ufo/waves/round-46/w1/ScribeReadme/`)

| File | What it is |
|---|---|
| `append.md` | 3.2 byte-for-byte (45 content lines after one blank line; sha256 `6a2733cf…`) |
| `correct.md` | 3.1 byte-for-byte (23 lines; sha256 `62377d24…`) |
| `apply-A.diff` | `-480,0 +481,23` against `c7e4d7d9:corpus/README.md`; `git apply --check` OK, applied `23 0`, 503 lines |
| `apply-B.diff` | `-468,13 +468,45` against the same file; applied → 512 lines, bytes equal to base 1-467 + 3.2 |
| `line-map.txt` | line numbers for both options at `a4477049` (466 lines) and `c7e4d7d9` (480 lines) |
| `evidence.txt` | every command above with its observed output, including the revision walk and the patch checks |
