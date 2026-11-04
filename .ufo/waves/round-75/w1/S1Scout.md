# S1Scout — second-route re-fetch of the three v262 snapshots (r75 w1)

**Verdict: PASS with three content deltas and five range-boundary deltas named.**
Sources verified **3/3** by two independent network routes; quotes located **6/6**
(5 byte-exact, 1 whitespace-normalized, both consistent with the frozen counter's own
`normalize_ws` rule); host re-read **7 of 8 readings identical, 1 transient delta**;
all five declared anchor ranges contain the functions the draft rows name, but all five are
substrings of a function rather than function extents — only two touch a boundary at one end
(`transaction.c:800`, `job.c:529`) — and the JT1 quote sits one line *before* the S315 range.

| Axis | Count |
|---|---|
| sources verified (bytes+sha256) | **3/3** |
| quotes located | **6/6** (5 byte-exact, 1 ws-normalized) |
| host readings re-captured / deltas | 8 / **1 transient** |
| declared anchor ranges inside-topic | **5/5**; function-aligned **0/5** (2/5 clean at one end) |
| content gaps found vs the six JT rows | **3** |

Method note: this seat has no `lsp` device mounted and the question is about vendored
upstream C bytes under `.ufo/waves/round-75/before/src/`, not this repo's own symbols, so
`grep -nF` over second-route bytes plus `sha256sum`/`cmp` is the operative method. No
semantic server could answer these files; that unavailability is recorded rather than
papered over.

---

## 1. Second-route fetch — 3/3 verified

Two routes, deliberately different services:

- **route2** — per-file: `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/{transaction.c,job.c,job.h}`
- **route-codeload** — archive: `https://codeload.github.com/systemd/systemd/tar.gz/refs/tags/v262`
  (tarball 19 038 647 B, sha256 `6aa77506c0644aa67f940a48e3d3a7368601f787e4f249139516d353f107bcab`),
  extracting `systemd-262/src/core/*`.

A third probe through `https://github.com/systemd/systemd/raw/v262/...` returned
`url_effective = raw.githubusercontent.com` (GitHub redirects), so it is the *same* origin
as route2 and is **not** counted as independent; the codeload archive is the independent route.

```
route2 (per-file)
transaction.c HTTP 200 bytes 57987
job.c         HTTP 200 bytes 63346
job.h         HTTP 200 bytes 7851

sha256 (route2 == codeload, byte-identical via cmp)
c1c704bb4330ffee5203980219adf1ff1e11402a4a02092f471129ff7c5df2f3  transaction.c
024a1accfd833223f2913d72e1f106fd40175429d31fcaca2321370fb5a10897  job.c
22d7b942426402ddba376c7b713bc9937c2eaa9f5817e8735dec8d5b6cf57c3a  job.h
```

Agreement with the frozen map:

| file | SOURCES.json bytes | fetched bytes | SOURCES.json sha256 | fetched sha256 | cmp |
|---|---|---|---|---|---|
| transaction.c | 57987 | **57987** | `c1c704bb…f2f3` | **match** | identical to snapshot |
| job.c | 63346 | **63346** | `024a1acc…0897` | **match** | identical to snapshot |
| job.h | 7851 | **7851** | `22d7b942…c3a` | **match** | identical to snapshot |

`sha256sum -c SHA256SUMS` inside `.ufo/waves/round-75/before/src` → all three `OK`, rc 0.
`cmp` of route2 vs codeload vs the committed snapshots → identical for all three. The
pinned bytes are reproducible from the public tag and have not drifted since the snapshots
were taken.

## 2. Six quotes — 6/6 located

Line numbers are in the route2/codeload bytes, which are byte-identical to
`before/src/<file>`, so the same numbers hold for the committed snapshots.

| row | snapshot | quote (as written in the draft) | located at | mode |
|---|---|---|---|---|
| JT1 | job.c | `Merging is commutative, so imagine the matrix as symmetric. We store only` | **job.c:399** | byte-exact (`grep -nF`) |
| JT2 | job.c | `Reload jobs are never considered redundant/duplicate.` | **job.c:454** | byte-exact |
| JT3 | job.h | `JOB_TRY_RESTART can never appear in a transaction, because` | **job.h:33** | byte-exact |
| JT4 | job.h | `JOB_DEPENDENCY, /* A required dependency job did not result in JOB_DONE */` | **job.h:65** | **whitespace-normalized only** |
| JT5 | transaction.c | `/* Fifth step: verify order makes sense and correct cycles if necessary and possible. */` | **transaction.c:841** | byte-exact |
| JT6 | transaction.c | `We propagate RESTART only as TRY_RESTART, in order not to start dependencies that` | **transaction.c:1203** | byte-exact |

Absent quotes: **none**. One qualification on JT4: the source line is
`        JOB_DEPENDENCY,          /* A required dependency job did not result in JOB_DONE */`
— ten spaces before the comment, the draft carries one. `grep -nF` on the draft string
therefore **fails**; the quote matches under collapsed whitespace, which is exactly the
rule the frozen counter implements (`normalize_ws`, `tools/count-jt-rows-r75.py:71-72`,
applied at `:207-209`). So JT4 is *valid under the predicate* but is **not** byte-verbatim:
a future reader grepping the literal cell will get no hit. Worth one line in the note if
the row is otherwise restated.

Digest columns agree with the file each row cites: JT1/JT2 → job.c `024a…`, JT3/JT4 →
job.h `22d7…`, JT5/JT6 → transaction.c `c1c7…`.

## 3. Host readings — 7/8 identical, 1 transient delta

Re-captured 2026-11-04T04:25:52Z against `before/host.txt` (2026-11-04T04:20:32Z), five
minutes apart, same boot:

| reading | before | now | delta |
|---|---|---|---|
| `systemctl --version \| head -1` | `systemd 262 (262.1-1-arch)` | same | none |
| `pacman -Q systemd` | `systemd 262.1-1` | same | none |
| `systemd-analyze unit-paths` | 12 paths | **same 12, same order** | none |
| `systemctl list-jobs --no-legend` | empty | **empty** | none |
| `show user@1000.service` Id/Names/FragmentPath/DropInPaths | `user@1000.service`, `/usr/lib/systemd/system/user@.service`, two drop-ins | same | none |
| `show sshd.service` Job/ActiveState/SubState | `Job=`, `inactive`, `dead` | same | none |
| running service count | 22 | **21** | **−1, transient** |

The running-service count is the only delta and is a property of a live system, not of the
pinned sources; it is expected to move. No delta touches any fact the C1 rows assert. The
host is the same systemd **262.1-1**, so the pinned v262 `src/core` bytes match the running
binary's release line — the note's host context claim holds.

## 4. Anchor ranges — all five on-topic, four boundary-sloppy

Registry rows S314–S316 exist in the round mirror (`/fast/scratch/hyaku/tsukuroi-r75/L1/mirror/corpus/SOURCES.md:325-327`)
and declare exactly these ranges; their sha256 cells (`c1c704bb…f2f3`, `024a1acc…0897`,
`22d7b942…c3a`) are the same three digests this seat re-derived from the public tag, so the
registry, the frozen map and the bytes agree three ways. They are **not** in `corpus/SOURCES.md` at the declaration
commit `1e2bb29` (`git show 1e2bb29:corpus/SOURCES.md | grep -E '^\s*\| *S31[456] *\|'` → rc 1),
so registration lands with this round's sources seat, not before it. Flagging that as a
sequencing fact for the C1 `JT_SOURCES=3` target, not as a defect of the snapshot work.

Boundary lines, and containment of the functions each draft row names:

| range | first line at `a` | last line at `b` | function(s) in range | contains the named function? |
|---|---|---|---|---|
| transaction.c 636–700 | `SET_FOREACH(a, tr->anchor_jobs)` | `/* Ok, let's get rid of this. */` | `transaction_is_destructive` (618–650, tail only) + `transaction_minimize_impact` (651–711, head 651–700) | yes — impact minimization; **starts mid-body and cuts the function at 700** |
| transaction.c 800–880 | `int transaction_activate(` | `if (r < 0)` | `transaction_activate` (800–892) | yes — all ten step labels 822–878 inside; **apply call and tail 879–892 excluded** |
| transaction.c 1090–1210 | `"Job type %s is not applicable for unit %s.",` | *(blank line 1210)* | `transaction_add_job_and_dependencies` (1030–1258) | yes — pull-in block 1144–1210 + JT6 quote at 1203; **both ends mid-body** |
| job.c 400–530 | ` * its lower triangle to avoid duplication. …` | *(blank / `job_is_runnable` head)* | `job_type_lookup_merge` (426), `job_type_is_redundant` (443), `job_type_collapse` (482), `job_type_merge_and_collapse` (518–529) | yes — all four; **but the JT1 quote is at 399, one line before the range**, and the merge doc block opens at 398 |
| job.h 10–80 | `JOB_VERIFY_ACTIVE,` | `* some way. This structure is used only while building a transaction. */` | `enum JobType` (8–…), `typedef enum JobResult` (60–76) | yes — JT3 at 33, JT4 at 65; **`enum JobType {` (8) and `JOB_START` (9) fall outside; the range ends inside the `JobDependency` comment** |

Consequence for the note: the ranges are **cited as if they were whole functions but are
substrings**. Either widen them to the real spans — transaction.c `618–711`, `800–892`,
`1030–1258`; job.c `398–530`; job.h `8–81` — or keep them and drop the implication that
they are function-extents. The single most consequential instance is `job.c` starting at
400 while the JT1 quote is on 399: a checker that greps the *range* rather than the file
would miss it.

## 5. Source-content gaps that the rows under-state (depth, not existence)

These do not break any frozen predicate — the counter checks quote location, digest and
shared-token density, not completeness — but they are the places where the note would be
asserting a set that the source does not bear out. Numbers below are from the second-route
bytes.

1. **JT4 enumerates 7 of 13 `JobResult` values.** `job.h:60-76` defines `JOB_DONE`,
   `JOB_CANCELED`, `JOB_TIMEOUT`, `JOB_FAILED`, `JOB_DEPENDENCY`, `JOB_SKIPPED`,
   `JOB_INVALID`, **`JOB_ASSERT` (68)**, **`JOB_UNSUPPORTED` (69)**, **`JOB_COLLECTED` (70)**,
   **`JOB_ONCE` (71)**, **`JOB_FROZEN` (72)**, **`JOB_CONCURRENCY` (73)**, then the
   `_JOB_RESULT_MAX` / `_JOB_RESULT_INVALID` sentinels. If the note's JT4 restates the row as
   *the* outcome set, it is six members short; the honest wording is "seven of the thirteen,
   with six further failure/terminal values for assert, unsupported type, collection,
   oneshot repeat, frozen unit and concurrency".
2. **JT6 covers 2 of the 5 pull-in classes in the same block.** Inside
   `if (IN_SET(type, JOB_START, JOB_RESTART))` (`transaction.c:1144`): `PULL_IN_START` →
   `JOB_START` + `TRANSACTION_MATTERS` (1145–1154), `PULL_IN_START_IGNORED` → `JOB_START`
   without it (1155–1167), **`PULL_IN_VERIFY` → `JOB_VERIFY_ACTIVE` + `MATTERS` (1168–1176)**,
   **`PULL_IN_STOP` → `JOB_STOP` + `MATTERS|CONFLICTS` (1178–1186)**,
   **`PULL_IN_STOP_IGNORED` → `JOB_STOP` bare (1188–1197)**. The row names the first two and
   the propagation; the "per-class pull-in flags" wording in the round claim needs all five
   or it is a partial map.
3. **JT2's "active or reloading" is narrower than the helper.** `job_type_is_redundant`
   (`job.c:443-481`) returns `UNIT_IS_ACTIVE_OR_RELOADING(b)` for `JOB_START` and
   `JOB_VERIFY_ACTIVE`, and that helper is `IN_SET(t, UNIT_ACTIVE, UNIT_RELOADING, UNIT_REFRESHING)`
   (`src/core/unit.h:64-66`, fetched for corroboration only — not one of the three pinned
   snapshots, sha256 `563a8180f79038ddc28d267cd971c902bd6c1df438ac92cee6e0a6612b8e1eca`).
   **`UNIT_REFRESHING` is a third redundant state.** `UNIT_IS_INACTIVE_OR_FAILED` is exactly
   `IN_SET(t, UNIT_INACTIVE, UNIT_FAILED)` (`unit.h:76-78`), so the stop half of the row is
   exact. The row's own quote (`job.c:454`) does not carry the state list, so this gap is
   invisible from the quote alone — which is precisely why the second route was worth running.

Confirmations that strengthen C1 rather than wound it:

- "lower triangle only" is *implemented*, not just commented: `assert_cc(ELEMENTSOF(job_merging_table) ==
  _JOB_TYPE_MAX_MERGING * (_JOB_TYPE_MAX_MERGING - 1) / 2)` and indexing
  `job_merging_table[(a - 1) * a / 2 + b]` after swapping so `a > b` (`job.c:426-441`).
  Commutativity is enforced by that swap, not merely asserted in prose.
- merge-then-collapse is exactly `job_type_merge_and_collapse`: lookup, `-EEXIST` if
  unmergeable, then `*a = job_type_collapse(t, u)` (`job.c:518-529`) — the row's
  "collapsed immediately afterwards" is the actual code path used by callers.
- ten labelled steps are really ten, and they are labelled: `transaction.c:822` First,
  `825` Second, `833` Third, `837` Fourth, `841` Fifth, `853` Sixth, `862` Seventh,
  `869` **"Eights step"** (upstream's typo, not the note's), `872` Ninth, `878` Tenth.
  A note that says "ten labelled steps" is exact; one that reproduces the labels verbatim
  will inherit the `Eights` spelling.
- `JOB_TRY_RESTART = _JOB_TYPE_MAX_IN_TRANSACTION` sits directly after the
  `_JOB_TYPE_MAX_IN_TRANSACTION` enumerator and before `JOB_TRY_RELOAD` (`job.h:31-39`), so
  JT3's mechanism claim (equality with the bound, collapse before entry) is the source's own
  wording at `job.h:33-35`.
- the propagation is gated on `IN_SET(type, JOB_RESTART, JOB_STOP) || (type == JOB_START &&
  FLAGS_SET(flags, TRANSACTION_PROPAGATE_START_AS_RESTART))` and collapses via
  `job_type_collapse(is_stop ? JOB_STOP : JOB_TRY_RESTART, dep)` with `JOB_NOP` skipping
  (`transaction.c:1199-1211`) — JT6's "restart propagated only as try-restart" is exact,
  including the NOP skip the row omits but does not contradict.

## 6. Counts

- **Sources verified: 3/3.** Two independent routes (`raw.githubusercontent` per file;
  `codeload` tag tarball), HTTP 200 each, bytes 57987/63346/7851, sha256 all three equal to
  `SOURCES.json`, `sha256sum -c` rc 0, `cmp` identical to the committed snapshots.
- **Quotes located: 6/6.** Lines 399 (job.c), 454 (job.c), 33 (job.h), 65 (job.h),
  841 (transaction.c), 1203 (transaction.c). Five byte-exact, JT4 whitespace-normalized
  (valid under the counter's `normalize_ws`, not byte-verbatim). No absent quote.
- **Deltas named: 9.** 1 host (running-service count 22→21, transient); 5 range-boundary
  (four mid-function truncations + JT1's quote one line outside S315's declared range);
  3 content gaps (13-member `JobResult` vs 7 listed; 5 pull-in classes vs 2 listed;
  `UNIT_REFRESHING` missing from the redundancy wording).
- **Registry timing:** S314–S316 are absent from `corpus/SOURCES.md` at the declaration
  commit (rc 1) and present only in the round mirror — registration is a same-round
  dependency of `JT_SOURCES=3`, not pre-existing ground.

## 7. Remaining unknowns

- Whether the note (not yet in the lane at the time of this seat) restates JT4/JT6/JT2 in
  the narrow wording of the draft rows or widens them; the gaps above are conditional on
  that text. The route2/codeload evidence needed to widen them is in this report, with line
  numbers, so the widening is a one-line edit per row.
- The five labelled-step *names* beyond the numbers: steps 3/4 and 6/7 are individually
  labelled but the draft compresses them ("redundant dropping", "a second collection and
  redundant drop"), so "ten labelled steps" and the row's eight-item prose disagree in
  cardinality by design, not by error. No further source evidence will settle which phrasing
  the note should use — that is an editorial call for the note's author.
