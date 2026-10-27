VERDICT: draft

Seat `ScribeLesson` (L2 leaf, tsukuroi round 44 / hyaku run 9, wave w1), item F-3: draft
`corpus/lessons/round-44.md` as text, verify the four candidate mistakes against evidence, and say which QUALITY
criterion should have caught each. The draft text is at the end of this report, verbatim, for the L1 to land. It is a
**draft** and not a finished lesson for three reasons I can name exactly: the `## Gate` rows belong to seats F-1/F-2
and are placeholders; C2 has no measured after-state before wave 2 binds the six counted verdicts; and two of the four
candidate rows do not satisfy the Mistakes table's own last column (see Findings).

Revisions read: base `98020ece0674e0b569ee23aed10ffbee355b248e`, freeze `1d2afffeaedbb553d951f53c9edb0190e345b1ab`
(2026-10-26 20:37:25 -0300), implementation `7e081698d4fc3c4ea944884fd093058de9909de1` (21:02:02), w1 spec
`ff2c264a` (21:04:58). I wrote only `.ufo/waves/round-44/w1/ScribeLesson.md` and
`.ufo/waves/round-44/w1/ScribeLesson/`; no lane file, counter, census or host state was touched, and no counter >2 s
was run.

---

## Evidence per candidate

### (1) The C2 counter's source-line check and control K17 — hole real, "first draft" not preserved

The check exists and is a **leading-id-list** parse, not a substring search
(`tools/check-scrub-record-r44.py:336-338`):

- `:336` `srcline = next((ln for ln in entry.splitlines() if ln.startswith('source:')), '')`
- `:337` `lead = re.match(r'source:\s*((?:S\d{3,}[\s,]*)+)', srcline)`
- `:338` `src['source_line'] = {'S237','S240','S242','S243','S244','S245'} <= ids`

The docstring states the rule and names the control (`:40-42`): "the entry's `source:` line opens with an id list (the
S-ids before any other text) that holds S237, S240, S242, S243, S244 and S245 (an id named only later in the line's
prose does not count; pre-data control K17)." The declaration's control list agrees: "K17 S244 only in the source
line's prose: each must FAIL" (`SCORECARD.md:2756`, read in the `:2756` block of the round-44 declaration).

K17's mutant is built by deleting the **leading-list** occurrence only (`controls/run_controls_c2.py`, `srcfix =
re.sub(r'^(source: [^\n]*?) S244', r'\1', entry, ...)`); S244 survives later in the same physical line ("S242, S243 and
S244 are …"). The receipt `controls/C2-K17.jsonl:1-2` reads `{"control": "K17", "expect": "FAIL", "exit": 1}` and
`"sources": {"S237": true, "S240": true, "S242": true, "S243": true, "S244": true, "S245": true, "source_line":
false}, "sources_ok": 0, "verdict": "FAIL"` — i.e. every *other* conjunct is green (`rows 3, quotes_ok 3, props_ok 3,
host_ok 3, verdicts_ok 3`), so the mutant is refused by exactly the source-line conjunct and by nothing else.

My own measurement of the same two parsers on the same bytes (`ScribeLesson/k17-parse.txt`): the mutant's leading ids
are `S237 S240 S242 S243 S245` → `source_line False`; `'S244' in msrc` is `True`; a substring-anywhere variant reads
`source_line True`. So the leading-list parse is the thing that makes K17 red, and a substring implementation would be
vacuous on it.

**What the record does not support:** that the counter's *first draft* accepted prose. The counter has a single
committed version, created at the freeze (`git log -- tools/check-scrub-record-r44.py` → `1d2afffe` only; sha256
`c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059` at the freeze, at `7e081698` and at HEAD), and no
pre-freeze draft survives in the lane or in the L1 scratch (`/fast/scratch/hyaku/tsukuroi-r44/L1/` holds only fetched
sources and empty `ctl`, `ctl2`). "The first draft accepted prose" is therefore the L1's narrative (`w1-spec.json`
item F-3; `make-w1-spec.py:131`), not a preserved artifact. What is evidenced is the hole, the control that separates a
leading-list parse from a substring parse, and that all of it predates the wave: control battery inside `1d2afffe`
(20:37:25), w1 dispatch `ff2c264a` (21:04:58), 27 min later.

### (2) R43-SR1-LIMITS-CONTRADICTION — routed, appended, and read by no instrument

- The defect is real: at the base, `corpus/knowledge/btrfs-scrub-record-r43.md:152` is the Limits bullet "SR1's
  trailing-bytes consequence is read from the open flags and was not reproduced (no record exists on this host and no
  scrub is run)", while SR1's own statement at `:28` states the consequence and round-43's harness reproduced it
  (`corpus/lessons/round-43-verifier-spotcheck.md:144-146`, §5 item 1).
- It was routed by the non-author closure, not by a counter: `round-43-verifier-spotcheck.md` §5 item 1.
- Round-44's repair is in `ab8aae16`: `## Corrections — round 44` at `corpus/knowledge/btrfs-scrub-record-r43.md:157`,
  the correction text at `:159`, and the header pointer at `:4` (`extended-by: … the "Limits" sentence on SR1 is
  corrected in "Corrections — round 44" at the end of this file`). Same commit also has the counter's `pointer_ok`
  visible to it (the counter greps the first 20 lines of the r43 entry for `btrfs-scrub-record-r44.md`, `:344`).
- Coordinate note, not a defect: the closure's `:152` is correct at its own revision (`git show
  98020ece:…-r43.md | sed -n 152p` prints the same bullet) and at `8acf0b02`; the round-44 `:4` insert moved it to
  `:153` (`grep -n "was not reproduced"` → `153:` and `159:`). Any citation of that bullet now needs its revision.
- The declared limit is that nothing reads the repair: `grep -ln "Limits" tools/check-*.py tools/score-*.py` →
  `tools/check-adjacency-overlap.py` only; the round-44 declaration says the correction is "outside both claims (an
  appended correction in the r43 entry; no counter reads it)" (`SCORECARD.md:2754`-block).

### (3) The 19:55 fleet-root strays — **not attributable** from the evidence

Bytes, observed in the quarantine with `od -c` (`ScribeLesson/stray-attribution.txt`):

- `=1239` 16 B `19:56:24` → `=   =       s   h   i   f   t       I   -       f   o   r  \n`
- `=3900` 49 B `19:55:45` → `=   =   =       t   r   a   c   k   e   d   -   a   l   l       s   i   b   l   i   n   g   s       S   K   I   L   L   .   m   d   :       n   e   a   r       t   s   u   k   u   r   o   i  \n`
- `T` 0 B `19:56:24`

Search for the writers' command text — `git grep -n` in the lane for `tracked-all`, `shift I-`, `near tsukuroi` →
**no hit in any committed lane file**; the same three patterns in `mori-shokunin/.ufo/waves/round-51/` → no hit;
`3900` appears in the round-43 wave tree only as two unrelated hash substrings
(`C2ExecKernelPatch/kernelorg-sha256sums.asc:125`, `SentScopeFinal/objects-touched-1957.ids:112`).

Candidate writers, both by shape only:

1. tsukuroi r43 wave-2 seat `AdjFinal`, a sibling-pin sweep whose subject is exactly "sibling `SKILL.md:<n>` lines near
   tsukuroi" (`.ufo/waves/round-43/w2/AdjFinal.md:11` third sweep, receipt
   `.ufo/waves/round-43/w2/AdjFinal/sibling-skillmd-pin-lines.txt`, 450 lines) and whose report states the shift
   arithmetic ("shift vs `c8efaa3f`: lines ≥ 693 **+6**", `:31`). Its own receipts are stamped `19:58:09`, i.e. 2-3 min
   after the strays, so a seat still writing at 19:55 fits.
2. A mori r51 w1 connector seat, `Mo51ConnSiblings`, which misrooted into the fleet root five minutes earlier at 19:50
   (`.scratch/goal-20261026-hyaku-run9.md:203-210`), same cwd error.

Neither is provable: no artifact carries the echo strings, and the numbers `1239`/`3900` do not name any object in
either seat's report (`1239` occurs in `AdjFinal.md:23` as "T:1238-1239"; `3900` occurs nowhere). Owner: the r43/r51
closures — the strays predate r44's base commit (`98020ece`, 20:37:25), so they are **outside this round's window**;
they are recorded in the lesson only because the guard in every r44 seat prompt is the fix and because the next strays
(20:10, 21:08) belong to other lanes' closures.

### (4) SR7's device-replace branch — real, narrowed pre-wave, and **not enforced by the counter**

- The draft at `ab8aae16` read: "a scrub runs on a device exactly while that device carries a scrub context"
  (`git diff ab8aae16 7e081698 -- corpus/knowledge/btrfs-scrub-record-r44.md`). The narrowing at `7e081698` (commit
  subject: "C2 SR7 narrowed before wave 1 (btrfs_scrub_dev also serves device replace)") rewrites it to "a device
  carries a scrub context exactly while `btrfs_scrub_dev` runs on it … serves both a scrub and a device replace (its
  `is_dev_replace` argument) [inference for the replace side: its caller is in `fs/btrfs/dev-replace.c`, opened this
  round at v7.2.11 lines 701-703 and 1265-1267 but **not pinned**]", adds the outcome clause "or is the source of a
  running replace", and adds one quote: `S242` scrub.c:3081 `"bool readonly, bool is_dev_replace)"` (`sed -n 3081p`
  on the frozen snapshot prints exactly that). The replace side is unpinned in the evidential sense:
  `.ufo/waves/round-44/frozen/src/` holds seven entries and `SHA256SUMS` lists five files — no `dev-replace.c`.
- Enforcement gap, measured (`ScribeLesson/sr7-props-gap.json`, fixture revision `46e075fc…`, command in
  `ScribeLesson/sr7-props-gap.cmd.txt`): deleting the 40-character replace clause from the statement of a fixture clone
  leaves `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1` unchanged (per-row SR7 `prop_ok true`,
  `quote_ok true`); only `verdicts_ok` is 0, because no wave-2 records exist in a fixture. The cause is the token list
  and the check: `ROWS['SR7']['props'] = ['btrfs_scrub_progress', 'scrub_ctx', 'ENOTCONN', 'ENODEV', 'EINPROGRESS']`
  (`tools/check-scrub-record-r44.py:86`) with `p_ok = bool(st) and all(t in st for t in spec['props'])` (`:296`) —
  no token names the replace branch. So the declaration's own fix for this row has **no counter that can fail on it**.
- The same class recurred inside the row after the narrowing: wave-1 seat `C2ExecKernelSR7` reports `VERDICT:
  defect-found` and finds that 0 also covers the attach→start window (3159→3167, which can block before start),
  scan-end→clear (3211→3222) and the replace source device, with the row's exact line numbers and the two
  `dev-replace.c:700-703, 1264-1268` call sites (`w1/C2ExecKernelSR7.md:1, :100-101, :109, :121, :138`). That is a
  wave-2 binding question; the lesson records the class, not the outcome.

---

## Findings (things the L1 should act on before landing the lesson)

1. **Two candidate rows cannot fill the table's last column.** Row (2)'s repair is append-only and read by no counter
   (`grep -ln "Limits" tools/check-*.py` → one unrelated tool), and row (4)'s narrowing is invisible to every lexical
   conjunct of the frozen C2 predicate (measured). Neither can be written as "fix shown able to fail" without either a
   named instrument or an explicit "no instrument; the repair is asserted" clause. I wrote both honestly in the draft
   and propose the missing instruments there. This is a real cost: the round can land a lesson in which two of four rows
   are not falsifiable.
2. **Row (1) must not be written as a landed mistake.** The counter never landed in a prose-accepting state: one
   committed version, at the freeze, already carrying the leading-list parse. The lesson value is the control's
   construction — K17 is a *stronger family member* than QUALITY 86 requires ("an entry with an S-id dropped from
   `source:`"), because a fully dropped id is refused by a substring implementation too; a prose-only survivor is not.
   I wrote it as "caught pre-data, did not land" and said so in the evidence cell.
3. **Row (3) is outside the round's window and unattributed.** Recommend the lesson keep it as an inherited incident
   with the two candidate writers and the ownership line, and not import it into the r44 claims; the attributed part of
   the fleet-root pattern (20:10 chousa, 21:08 tsukuroi C1 fixture) belongs to those lanes' closures.
4. **A coordinate duty for the Gate.** The r43 Limits bullet moved `:152` → `:153` in the same commit that fixed it
   (the `:4` `extended-by:` insert). Any Gate or disposition row citing that bullet needs its revision (QUALITY 21), and
   that is the second round in a row where a routed-defect citation had to be re-based by content.

## QUALITY attribution per candidate

| Candidate | Class | Criterion that should have caught it | Adequacy |
|---|---|---|---|
| (1) source-line prose | vacuous check (caught pre-data, did not land) | **86** (`corpus/QUALITY.md:169`): "every S-id that row cites is named on the entry's `source:` line … its frozen controls include … an entry with an S-id dropped from `source:`" | 86's letter is met by a control a substring implementation also refuses; K17 strengthens it to a prose-only survivor. Recommended amendment: name the prose-only variant. |
| (2) r43 Limits contradiction | internal contradiction / provenance | **87** is the nearest ("a content counter reads the content it credits", `:171`), but no criterion requires an entry's `## Limits` block to be read with the statements it qualifies | Gap, not a 87 miss. Failing example any such instrument must separate: base `98020ece` (`:152` bullet, no correction) vs tip (`:153` bullet + `:159` correction); today only a presence grep exists. |
| (3) 19:55 strays | scope / misroot, writer unattributed | **none** — the seat-prompt host guard (ROUND-PROMPT §7) is a process rule with no QUALITY row, and its enforcement receipt (the orchestrator watcher) covers `~/.local/bin`, not the fleet root | Gap. The guard prevents the file; nothing records the writer (`pid`/`cwd`/`argv`), which is why 19:55 stayed unattributed while 20:10 and 21:08 were attributed by the shape of their directories. |
| (4) SR7 "exactly" without replace | unstated branch | **66** (`corpus/QUALITY.md:133`): a statement keeps every branch its quoted source states; "words such as 'only', 'otherwise' or 'exactly' need a source sentence that says so" | Fits exactly, and 66 was not enforced: the capture was the L1 reading `dev-replace.c`, and the counter's token list has no replace token. |

## Not done (explicit)

- No census selftest, no C1/C2 counter battery, no live census: outside an F-3 seat's scope, and the C1 counter is
  ~30 s / 2-4 CPUs (one heavy job per wave at a time).
- No re-fetch of S242-S245: F-1/F-2 own the live byte-identity check; I read the frozen digests only.
- No wave-2 data exists, so the Gate's per-sentence table and every counted verdict are placeholders.
- I did not attempt to wake, message or inspect any sibling seat's in-flight work; the two peer reports I would have
  wanted (C2RevCounter, C1RevCounter) are wave-1 reads of the same counters and are not counted by any predicate.

---

# Draft text — `corpus/lessons/round-44.md`

```markdown
# Round 44 — lesson (tsukuroi, hyaku run 9)

Drafted by wave-1 seat `ScribeLesson`; the author of record is the round's L1 (`TsukuroiR44`), who fills the
`## Gate` placeholders from seats F-1/F-2 and owns every claim below. Base `98020ece0674e0b569ee23aed10ffbee355b248e`
— the lane tip at round start as `jj-lane.sh state` printed it. Declaration and freeze
`1d2afffeaedbb553d951f53c9edb0190e345b1ab` (2026-10-26 20:37:25 -0300); implementation
`7e081698d4fc3c4ea944884fd093058de9909de1`, which carries a pre-wave narrowing of SR7. Waves: two v1 waves, `w1`
(build + first falsifiers, 46 seats, dispatched 21:04:58 from `.ufo/waves/round-44/w1-dispatch.json`) and `w2`
(falsify, with the six counted C2 row verdicts). Specs, dispatches and the orchestrator's results files are in
`.ufo/waves/round-44/`. Seats are the lane, not outside reviewers (`LEARNING.md`); this round's non-author closure is
pending.

## Frozen claims (declaration `SCORECARD.md` "Round 44 — declaration", frozen at `1d2afffe`)

| Claim | Axis | Surface moved | Counter (frozen; sha256) | Predicate |
|---|---|---|---|---|
| C1 | coverage | The scrub-record line of the storage-integrity frontier moves Frontier → Core for the unprivileged view: `tools/tsukuroi-census.sh` gains `probe_scrub_record` (`:1967`, wired at `:3375`) and one verdict-neutral line `SCRUB btrfs-scrub-record state=NONE\|RECORDED\|BLOCKED dir=absent\|present\|unreadable records=N tmp=N sockets=N unreadable=N orphan=N limited=N timers=N [detail=…]` after STORAGE and before the rollup; `/var/lib/btrfs` by name and stat only, each device's `scrub_speed_max`, the `btrfs-scrub@*.timer` links under `timers.target.wants`; never content, never an ioctl, never the running state; plus nine `(R44-C1)` selftest cases (132 → 141) | `tools/score-scrub-arm-r44.py` `1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388` | `cases == 16 and correct == 16 and identity_ok == 1 and wired_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r44 >= 6` |
| C2 | depth (S242, S243, S244 opened this round) | New entry `corpus/knowledge/btrfs-scrub-record-r44.md`, rows SR7 (the scrub-progress success direction), SR8 (`scrub_speed_max`: `BTRFS_ATTR_RW` 0644, `%llu\n` read, `memparse` write with `-EINVAL` on trailing text, 0 = no limit), SR9 (the Arch-packaged `btrfs-scrub@.timer`/`.service`: monthly, `Persistent=true`, `WantedBy=timers.target`, `btrfs scrub start -B %f`, `KillSignal=SIGINT` → `BTRFS_IOC_SCRUB_CANCEL`), on S237, S240 (re-opened), S242-S245, plus an `extended-by:` pointer in the r43 entry | `tools/check-scrub-record-r44.py` `c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059` | `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1` |

C2's verdicts bind only from wave 2 (`C2RevSR<n>`, `C2CritSR<n>`; a `partly` needs a bound residual `C2ResSR<n>`
reading `holds`); wave 1 produces no counted verdict. Kill rules, both claims, are in the declaration: C1 — a PLANE
line, the rollup line or the census exit code changing on the live host between base and the measured revision, a
frozen predecessor storage counter (`score-storage-arm-r38.py`, `-r38-q82.py`, `score-storage-hidden-r39.py`,
`score-size-invariance-r42.py`) FAILing where it PASSes at base, or the arm creating a file in live mode; C2 — a bound
`fails`, a `partly` with no bound residual `holds`, a counted output carrying a second verdict line contradicting the
bound one (audited by hand).

Pre-data controls: `.ufo/waves/round-44/controls/` (batteries committed with the counters at the freeze;
`battery-summary-c1.jsonl` and `-c2.jsonl` each read `should_fail_accepted 0, control_accepted 1`). Recorded limits:
C1 leaves the mount-table, `uid_map` and census-script-path channels open; C2's lexical conjuncts cannot tell forged
orchestrator records from real ones (control K3 passes) and `transcripts_bound` is reported outside the predicate.
Before receipts in `.ufo/waves/round-44/before/`; the C1 after receipt at `ab8aae16`
(`.ufo/waves/round-44/after/c1-after-ab8aae1.jsonl`: `cases 16, correct 16`, identity `1000/1000/1000`, `wired_ok 1`,
`live_agree 1`, `selftest 141 PASS`, `selftest_r44 9`).

## Gate

### New SOURCES rows (drafted and quoted by F-1; each quote located with `grep -n` in the pinned snapshot by the L1)

| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S242 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/scrub.c?h=v7.2.11 | _(F-1)_ | `.ufo/waves/round-44/frozen/src/scrub.c`, sha256 `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` |
| S243 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/sysfs.c?h=v7.2.11 | _(F-1)_ | `…/frozen/src/sysfs.c`, sha256 `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` |
| S244 | https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/tree/7.1-1 | _(F-1, per unit and PKGBUILD)_ | `…/frozen/src/btrfs-scrub@.timer` `9a0b6cc2…6f8ad`, `btrfs-scrub@.service` `eaa7af92…40252`, `PKGBUILD` `3b803e8b…0ce98` |
| S245 | own-work capture `.ufo/waves/round-44/frozen/hostcap/` (`capture.sh`) | _(F-1)_ | `…/hostcap/capture.txt`, sha256 `efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900` |

Snapshot digests `.ufo/waves/round-44/frozen/src/SHA256SUMS` (five files), fetch log `frozen/src/FETCH.txt` (Linux tag
v7.2.11 peeled `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`; packaging tag 7.1-1 commit
`0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0`). _(F-1: live re-fetch byte-identity and the entry's `source:` line ids.)_

### Re-opened row and rows touched old→new (F-2)

S237 (`corpus/SOURCES.md:246`) and S240 (`:249`) carry this entry in `used-by`; both stay `mined`. S242-S245 are new
rows, `mined` at entry, opened 2026-10-26. Also touched: `corpus/knowledge/btrfs-scrub-record-r43.md:4` (an
`extended-by:` pointer) and its appended `## Corrections — round 44`. _(F-2: the old→new log with the exact cells.)_

### Entry gate (C2) — per adopted sentence, the source line the L1 checked (QUALITY 91)

| Row | Change | Proposed by | Source line checked by the L1 |
|---|---|---|---|
| SR7 | "a scrub runs on a device exactly while that device carries a scrub context" → "a device carries a scrub context exactly while `btrfs_scrub_dev` runs on it … serves both a scrub and a device replace (its `is_dev_replace` argument)", plus a new quote | the L1, pre-wave (`7e081698`) | `frozen/src/scrub.c:3081` `bool readonly, bool is_dev_replace)` (`sed -n 3081p`, observed). The replace **call sites** are in `fs/btrfs/dev-replace.c:700-703, 1264-1268` and are **not pinned**, so the row marks the replace side [inference] |
| SR7/SR8/SR9 | _(F-1/F-2: every other adopted sentence, one row each)_ | | |

Recorded limit of the §"Entry gate" itself: the SR7 narrowing is not enforced by any lexical conjunct — the frozen
SR7 proposition tokens are `btrfs_scrub_progress, scrub_ctx, ENOTCONN, ENODEV, EINPROGRESS` and none names the replace
branch, so a fixture that deletes the clause still reads `props_ok 3, quotes_ok 3, sources_ok 1`
(`.ufo/waves/round-44/w1/ScribeLesson/sr7-props-gap.json`). The fix is a proposition token for the branch plus a
control that deletes it.

### Assimilation (`merge/tsukuroi/`) — _(F-2: evaluated, and either `Assimilation: none` or the adopted rows)_

### considerthese — _(F-2: the cross-note correction propagation map for this round's moves)_

### Spot-check — pending the non-author closure; candidates below.

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R44-C2-SOURCELINE-PROSE | vacuous (caught pre-data; the counter never landed in this state) | The `source:` check was a **leading-id-list** parse, not a substring search: `tools/check-scrub-record-r44.py:336-338` (`re.match(r'source:\s*((?:S\d{3,}[\s,]*)+)')`), documented at `:40-42` ("an id named only later in the line's prose does not count; pre-data control K17"). Control K17 keeps S244 in the line's prose and drops it from the list (`controls/run_controls_c2.py`, `srcfix`); its receipt reads `sources.source_line false`, `sources_ok 0`, `verdict FAIL` with every other conjunct 3/3 (`controls/C2-K17.jsonl:1-2`). Measured independently (`.ufo/waves/round-44/w1/ScribeLesson/k17-parse.txt`): mutant leading ids `S237 S240 S242 S243 S245` → `source_line False`, while `'S244' in line` is `True` and a substring-anywhere variant reads `True`. The control battery is inside the freeze commit (20:37:25); w1 dispatch is 21:04:58. The counter has one committed version, at the freeze (`c96aeda9…`), so "the first draft accepted prose" is the L1's narrative and no draft bytes are preserved | QUALITY 86 (`corpus/QUALITY.md:169`), whose required control — "an entry with an S-id dropped from `source:`" — is **weaker**: a fully dropped id is refused by a substring implementation too | The list parse, plus the docstring's parenthetical naming K17. Able to fail, both directions measured on the same bytes: list parse → `source_line False` on K17; substring parse → `source_line True` on a prose-only S244, i.e. the mutant would be credited. Recommended: amend 86 to name the prose-only survivor as the control |
| R43-SR1-LIMITS-CONTRADICTION | internal contradiction (provenance) | `corpus/knowledge/btrfs-scrub-record-r43.md:152` (at base and at `8acf0b02`) said SR1's trailing-bytes consequence "was not reproduced"; SR1's own statement (`:28`) and round-43's harness (`.ufo/waves/round-43/w1/C2ExecTailRepro.md`) say it was. Routed by `corpus/lessons/round-43-verifier-spotcheck.md:144-146` (§5 item 1) and repaired append-only in `ab8aae16`: `## Corrections — round 44` at `:157`, text at `:159`, header pointer at `:4` | no counter: the non-author closure's read. `grep -ln "Limits" tools/check-*.py tools/score-*.py` → `tools/check-adjacency-overlap.py` only, and the declaration states the repair is "outside both claims … no counter reads it" | The correction and the header pointer. **Not shown able to fail**: the repair has no instrument, and the only check available today is a presence grep, which any appended text satisfies. A future instrument must separate base (`:152`, no correction) from tip (`:153` + `:159`) by content, not presence. Coordinate note: the closure's `:152` is right at its revision; the round-44 `:4` insert moved the bullet to `:153` |
| R44-FLEETROOT-STRAYS-1955 | scope (writer unattributed; outside this round's window) | Three untracked files at the fleet root, 19:55:45-19:56:24: `=1239` (16 B, `== shift I- for`), `=3900` (49 B, `=== tracked-all siblings SKILL.md: near tsukuroi`), `T` (0 B); bytes observed with `od -c`, now in `.tower/quarantine/fleet-root-strays-20261026T1956/`. Not attributable: `git grep` in the lane for `tracked-all`, `shift I-`, `near tsukuroi` → no hit in any committed file; the same in `mori-shokunin/.ufo/waves/round-51/` → no hit. Shape matches the r43 wave-2 sibling-pin seat `AdjFinal` (`.ufo/waves/round-43/w2/AdjFinal.md:11, :31`; its receipts are stamped 19:58:09) or a mori r51 connector seat, which misrooted at 19:50. 19:55 predates the r44 base commit (20:37:25) | no criterion — the orchestrator's incident log (`.scratch/goal-20261026-hyaku-run9.md:211-216`). The fleet-root watcher covers `~/.local/bin`, not the fleet root | The seat-prompt host guard (cd to scratch first, absolute paths) is preventive; the attributable fix is a fleet-root write watcher recording the writer's pid, cwd and argv. Able to fail: no receipt names a writer for 19:55, while the 20:10 (`p.out`/`p.err`, S115 build spans) and 21:08 (`fx/A2-uppercase-fsid-sysfs/…`) strays were attributed by the shape of their directories alone |
| R44-SR7-EXACTLY-NO-REPLACE | unstated branch ("exactly" without a source sentence) | The draft at `ab8aae16` read "a scrub runs on a device exactly while that device carries a scrub context"; `7e081698` narrowed it to `btrfs_scrub_dev` (which "serves both a scrub and a device replace (its `is_dev_replace` argument)") and added the quote `S242` scrub.c:3081 `bool readonly, bool is_dev_replace)`. The replace call sites are in `fs/btrfs/dev-replace.c:700-703, 1264-1268`, opened but **not pinned** (`.ufo/waves/round-44/frozen/src/` has no `dev-replace.c`) | QUALITY 66 (`corpus/QUALITY.md:133`): "words such as 'only', 'otherwise' or 'exactly' need a source sentence that says so" — captured by the L1 reading `dev-replace.c`, not by an instrument | The narrowed statement and the added quote. **Not shown able to fail**: the SR7 proposition tokens (`check-scrub-record-r44.py:86`) contain no replace token and the check is a substring test (`:296`), so a fixture that deletes the clause still reads `props_ok 3, quotes_ok 3, sources_ok 1` (`.ufo/waves/round-44/w1/ScribeLesson/sr7-props-gap.json`). A token for the branch plus a deletion control would close it. The same class recurred inside the row: wave-1 `w1/C2ExecKernelSR7.md` finds 0 also covers the attach→start window (3159→3167), scan-end→clear and the replace source device, and binds in wave 2 |

## Round-43 routed defects — round-44 disposition

_(F-10: the per-item state at `7e081698` — R43-SR1-LIMITS-CONTRADICTION (repaired append-only, above), the C2 binding
gaps (closed by the JSON/`verdict_line`/whitespace rules and controls K13-K16), the C1 open channels (declared, not
closed), the census `:743`/`:746` lookup case and five single-line readers (still routed), and the `superseded-in-part`
pointer note.)_

## Sources census

Start: `.ufo/waves/round-44/before/sources-census-start.txt`. End: _(L1, from the round's report)._

## Spot-check candidates for the non-author closure

One admit: SR8's `0644` read / `memparse` write direction, on S243 at pinned lines with the host's own attribute
description in the capture. One reject: the SR7 sentence as narrowed at `7e081698` — "answers 1 exactly when some
device it asks about is being scrubbed, or is the source of a running replace, at that moment" is still false per
`w1/C2ExecKernelSR7.md` (0 also covers the attach→start window), so the wave-2 read should bind the narrowed text, not
the corrected intent.
```

---

## Receipts

Under `.ufo/waves/round-44/w1/ScribeLesson/`:

| File | What it is |
|---|---|
| `coordinates.txt` | the command/output log for every coordinate cited above (lane log, counter sha256 at freeze/HEAD, `grep -c "(R44-C1)"` → 9, `probe_scrub_record` at `:1967`/`:3375`, r43 `:152`→`:153` and `:159`, `grep -ln Limits`, the prop-check line, `scrub.c:3081`, `frozen/src` listing, the C1 after-receipt fields, the battery summary tails) |
| `k17-parse.txt` | the two-parser measurement on the entry and the K17 mutant (leading-list vs substring-anywhere) |
| `sr7-props-gap.json` | the frozen C2 counter's output on the replace-clause deletion (fixture rev `46e075fc…`): `quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1` |
| `sr7-props-gap.cmd.txt` | the exact fixture commands (clone `--shared` from the lane, origin removed, toplevel asserted, throwaway identity, no lane write) |
| `stray-attribution.txt` | the `od -c` bytes, mtimes, the three greps in the lane and in `mori-shokunin/.ufo/waves/round-51/`, and the `AdjFinal` receipt stamps |

Scratch `/fast/scratch/hyaku/tsukuroi-r44/ScribeLesson/` (including the fixture clone) was removed after the receipts
were copied. No tool was installed or upgraded this seat (nothing was needed).
