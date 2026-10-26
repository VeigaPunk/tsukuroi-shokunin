VERDICT: draft

# A-5 — QUALITY criteria draft (2 criteria, numbering 85–86)

Seat: QualityCriteria (L2, leaf). Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Item A-5: read `corpus/QUALITY.md` (criteria up to 84), draft at most two new criteria each citing a
lesson row, check non-duplication by grep, output exact markdown with numbering 85+.
I wrote nothing but this report. No counter was run, no mutant built, no child process spawned, no
scratch directory created (nothing needed building). Every command below is a read-only
`grep`/`sed`/`awk`/`wc` over committed lane bytes.

## 1. Non-duplication sweep (commands and observed output)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ grep -c "own-work" corpus/QUALITY.md        -> 0
$ grep -c "kind" corpus/QUALITY.md            -> 0
$ grep -n "namespace" corpus/QUALITY.md       -> 20   (criterion 15: permission-denial explanations)
$ grep -n "production" corpus/QUALITY.md      -> 161  (criterion 82 only)
$ grep -n "argv" corpus/QUALITY.md            -> 40 (criterion 30), 80 (criterion 36)
$ grep -n "environment" corpus/QUALITY.md     -> 143 (criterion 74), 149 (criterion 78)
$ wc -l corpus/QUALITY.md                     -> 165  (criterion 84 is the last, at :165)
```

Nearest neighbours and why each draft is an increment, not a duplicate:

| Draft | Nearest existing criterion | What the neighbour already says | What it does not say |
|---|---|---|---|
| 85 | 82 (`corpus/QUALITY.md:161`, R32-FIXTURE-GATEABLE) | a fixture-building counter must also be scored in "a view the code cannot tell from production use", with a fixture-gated and a cached-live control reading below target | nothing about *how* that view is staged, so a view staged as a host tree bind-mounted into the child is indistinguishable from a fixture; the Q82 counter met 82's text and still lost (R38-Q82-LEAK) |
| 86 | 7 (`corpus/QUALITY.md:11`, source-row citation and tier) and 19 (`:26`, claim/source scope) | every claim cites an exact `S###` row with tier and anchor; each admitted sentence names the source object, its ≤25-word quote and the proposition it supports | both accept an `own-work` row as the cited source object; neither distinguishes a rule about upstream code from a host capture, which is precisely the round-38 C2 gap |

Also checked: criteria 74 and 78 (`:143`, `:149`) build child environments for *git* tools and say
nothing about view reachability; criterion 15 (`:20`) mentions a mount namespace only inside a
permission-denial explanation; criterion 60 (in-place change sweeps) and 64 (table cell shapes) are
unrelated. No criterion in the file contains `own-work` or `kind`.

## 2. Proposed criteria — exact markdown

Insert after current line 165 (criterion 84), separated by one blank line, matching the blank-line
separation used from criterion 14 onward. Numbering is provisional: 85 and 86 are free today; the L1
assigns final numbers if another wave item also drafts at 85+.

```markdown
85. **A production-path view is built inside the child namespace and no host name reaches its content (R38-Q82-LEAK):** when a counter claims that the scored code cannot tell a view from production use, the view's content is created inside the child's own mount namespace before the scored code starts — a `tmpfs` mounted inside an unprivileged user+mount namespace and filled from data the child reads on stdin — and no name the scored code can resolve on the host side leads to it: not a `$HOME` or `$TMPDIR` sibling, not a bind-mount source, not an argv element or environment value, not `/proc/self/mountinfo`'s mount root, not an inherited cached answer. The frozen pre-data controls include one arm per channel, each arm reaching for the view through that channel alone, and each must score below the target. A docstring assertion of non-distinguishability is not the test; the leak arms are. Falsified by: a counter that stages the view as a host directory bind-mounted over the production path, an arm that reaches it by an inherited path and still scores the target, or leak arms committed after seats scored. Failing example: the round-38 Q82 counter bind-mounts the census "inside an unprivileged user+mount namespace (`unshare -rm`) in which a fresh tree is bind-mounted over the production path /sys/fs/btrfs" while its docstring claims "neither the path nor a cached answer distinguishes a view from production use" (`tools/score-storage-arm-r38-q82.py:10-13`), and the four arms `home-sibling-leak`, `features-empty-leak`, `fsid-shape-leak` and `mountinfo-leak` each score v1 PASS and Q82 3/3 PASS (`.ufo/waves/round-38/w1/Q82Attack.md:30-33`). Lesson: `corpus/lessons/round-38.md` Mistakes R38-Q82-LEAK.

86. **A rule row verifies on an upstream source row, never on an own-work capture alone (round-38 C2 counter gaps):** a knowledge row that states how upstream code behaves is verified only when its `source:` cell names at least one `corpus/SOURCES.md` row whose `kind` is not `own-work` and whose locator names the upstream artifact at the pinned revision, and every S-id that row cites is named on the entry's `source:` line; an `own-work` row, whose locator is a lane path, may carry a host observation, a count or a capture digest for that row and never makes the rule verified by itself. The counter keeps those as separate conjuncts, and its frozen controls include an entry whose rule rows cite only the own-work row and an entry with an S-id dropped from `source:`, each scoring below the target. Falsified by: a counter that passes an entry citing only the own-work capture, or counts a rule row verified while its `source:` cell names no upstream row. Failing example: `tools/check-hook-order-r38.py` passes a stripped entry that cites only the own-work capture `S212` and carries zero rule rows (`.ufo/waves/round-38/w1/CritControlsC2.md:5-7,46`) and survives dropping an S-id from `source:` (`.ufo/waves/round-38/w1/C2MutEntry.md:28-29`). Lesson: `corpus/lessons/round-38-verifier-spotcheck.md` §6.3 (routed defect 3, `:175-178`); the closed shape is `tools/check-transaction-order-r39.py`, which requires a mined upstream row at `54d9411` for the row's own libalpm file (`:8-9`, `:204-209`).
```

Numbering choice: both drafts add a rule that the existing criterion does not state (85 narrows *how*
82's view is staged; 86 narrows *which* source object satisfies 7's citation), so they go in as new
numbered criteria rather than as appended clarifications — the file's precedent for a scope-narrowing
addition is a numbered criterion that names the criterion it narrows (criterion 19, "Supersedes
criterion 18's blanket bot attribution only", `corpus/QUALITY.md:26`). If the L1 prefers the
clarification form, the same two paragraphs work as `R39 clarification to 82` and `R39 clarification
to 7` blocks appended under the existing text.

## 3. Grounding for each draft

### 85 — view reachability

- Defect: `.ufo/waves/round-38/w1/Q82Attack.md:8-9` — the cause is that "the counter leaves the fixture
  tree reachable from inside the child (via `$HOME`/`$TMPDIR` siblings and via `/proc/self/mountinfo`)";
  `:30-33` lists the four arms with `v1` PASS and `Q82` 3/3 PASS, each marked BEATS BOTH; `:28-29` shows
  the two arms that were killed (`first-device`, `uidmap-detect-cached`), so the table discriminates.
- False claim: `tools/score-storage-arm-r38-q82.py:10-13` — bind-mounts "a fresh tree … over the
  production path /sys/fs/btrfs" (exact span: "inside an unprivileged user+mount namespace (`unshare -rm`)
  in which a fresh tree is bind-mounted over the production path /sys/fs/btrfs", `:9-10`) and asserts
  "neither the path nor a cached answer distinguishes a view from production use". `:9-11` records the
  mechanism (host tree, `unshare -rm`, bind over the prod path), which is exactly the leak: the source of
  the bind lives on the host.
- Lesson row: `corpus/lessons/round-38.md:89` — `| R38-Q82-LEAK | vacuous | … "neither the path nor a
  cached answer distinguishes a view from production use" is false … QUALITY 82 | … Next round: build each
  view in a tmpfs mounted inside the child namespace (no host path, no mountinfo source) and add the four
  leak arms as committed should-fail controls.` The draft restates that prescription as an admission rule
  and adds the falsifier and the "arms are the test, not the docstring" clause.
- Not duplicate of 82: criterion 82's failing example (round-32 scorer v1) is a fixture-gated arm; the
  Q82 counter *is* the 82 remedy and still failed, which is why 85 must exist. Criterion 82 is kept as the
  parent requirement (a view the code cannot distinguish); 85 fixes the staging contract under it.
- Satisfiability, read from bytes (not run): `tools/score-storage-hidden-r39.py:8-10` describes views as
  "a tmpfs mounted INSIDE the child's unprivileged user+mount namespace … filled from data the child reads
  on stdin, so no host path, no bind source and no argv carries the view"; `:196-197` is the
  `mount -t tmpfs tsk "$1"` inside `unshare -rm` with the spec on stdin. I did **not** verify that the
  round-39 leak arms read below target — that is seat C1-2's measurement, not this seat's.

### 86 — own-work cannot verify a rule

- Round-38 C2 counter gap: `corpus/lessons/round-38-verifier-spotcheck.md:175-178` — "**C2 counter gaps**:
  `tools/check-hook-order-r38.py` passes a stripped entry citing only S212 (`w1/CritControlsC2.md`); it
  survives an S-id drop from `source:` (`w1/C2MutEntry.md`); it cannot see block duplication past the next
  `## `."
- The passing stripped entry: `.ufo/waves/round-38/w1/CritControlsC2.md:5-7` — "Two of twelve cheap tables
  PASS the frozen C2 counter, including one whose entry cites only the own-work capture `S212` and contains
  **zero** rule rows … `rows_expected 69, rows_matched 69, …, source_ok 1, result PASS, exit 0`"; `:46`
  names the receipt `stripC-dedup-etcfirst-srcS212`.
- The surviving mutant: `.ufo/waves/round-38/w1/C2MutEntry.md:28-29` — M9 `source:` line without S208 →
  "exit 0 PASS, … source_ok 1"; M9b (without S212) → "exit 0 PASS, source_ok 1". Cause at `:36`:
  `source_check` "validates only the ids still present".
- Why the own-work row is the discriminator: `corpus/SOURCES.md:221` (S212) has `kind` = `own-work` and a
  lane-path locator (`.ufo/waves/round-38/frozen/hooks-capture/`), as does `:227` (S218,
  `.ufo/waves/round-39/frozen/txcapture/`). Column vocabulary measured over the registry with
  `awk -F'|' '/^\| S[0-9]/{gsub(/ /,"",$4); print $4}' corpus/SOURCES.md | sort | uniq -c` → `58 code,
  6 community, 2 dataset, 123 docs, 27 own-work, 2 tool`; the header is `corpus/SOURCES.md:5`. The draft
  therefore keys on `kind` + locator shape, not on a tier (own-work rows are tier A, so criterion 7's
  "tier C is never sole support" does not reach them).
- Closed shape (read, not run): `tools/check-transaction-order-r39.py:8-9` — "a rule row verifies only on
  an UPSTREAM source row (an own-work row alone cannot carry it)"; `:204-209` requires the mined row's
  title to contain `54d9411` and `lib/libalpm/<file>`, which a lane-path own-work row cannot satisfy.

## 4. Findings (routed, not folded into the criteria)

1. **No `## Mistakes` row exists for the round-38 C2 counter gaps.** Criterion 86's natural lesson anchor
   is a lesson row, but `corpus/lessons/round-38.md` has none for this class: its Mistakes table
   (`grep -n "^| R38"` over the section) lists 11 rows and the only counter mention is R38-QUALITY-UNREAD
   (`:84`) about freezing C1/C2 counters, not the source gap. The ground is the non-author spot-check
   §6.3 and the two seat receipts. If the round-39 lesson lands the A-3 disposition row, swap the last
   sentence of 86 for:
   `Lesson: corpus/lessons/round-39.md Mistakes <that row's ID>; outside corpus/lessons/round-38-verifier-spotcheck.md §6.3 (routed defect 3).`
   Until then 86 cites the spot-check, which is what 83 does for its outside pointer.
2. **The round-39 counter still hands the child a host-side run directory.** `tools/score-storage-hidden-r39.py:192,196-197`
   pass `HOME=<work>/home` and `TMPDIR=<work>/tmp`, and argv carries `<work>/census.sh`, where `work` is
   `mkdtemp(dir=<scratch>)`. The *view content* lives only in the namespace tmpfs, so 85 as drafted is not
   violated; but a fixture-gated arm could still detect the harness from the `run-*` directory name. This
   is an observation on the bytes; I ran nothing, so the channel is unmeasured. If the L1 wants it closed,
   the fix belongs in the counter, not in a criterion.
3. **The third round-38 C2 gap is deliberately uncovered.** "It cannot see block duplication past the next
   `## `" (`round-38-verifier-spotcheck.md:178`) is a file-integrity rule, not a source-provenance rule;
   A-5's (b) scopes me to provenance, so I did not pad criterion 86 with it. It stays a routed debt for a
   separate criterion or for the round-39 counter's duplicate-heading conjunct (which already counts it,
   `tools/check-transaction-order-r39.py:9-10`).
4. **Criterion 85's leak arms are not yet shown able to fail for round 39.** The four round-38 arms exist
   and beat the round-38 counter, but porting them onto the round-39 counter is seat C1-2's item. Until
   that receipt exists, 85 is a rule with a known failing example from round 38, not a rule whose control
   set has been re-run.

## 5. What I did not do

- No counter, scorer, selftest or mutant was executed; no `unshare`, no mount, no child process.
- No scratch directory was created; nothing was copied; no `/fast/scratch` or `/tmp` path is claimed as
  evidence (none was produced).
- No lane file was created, edited or deleted; no `git`/`jj` mutating command; the only write is this
  report (`.ufo/waves/round-39/w1/QualityCriteria.md`). `git show`/`git grep` were read-only.
- No tool was installed or upgraded (none needed), so there is no tool/version/channel record to make.
- Both criteria are proposals; the numbering 85/86 and the final wording are the L1's to land.
