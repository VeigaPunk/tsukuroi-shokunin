# Round 78 — non-author closure spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed 2026-11-04. Base `b9019a1d0558241bf67cf31ff90256284d8657af`; delivered revision
`a15aff6ea38961cae5e6748b1e8f924a1b454c34`. Status **ok**, **admitted**. Both declared
claims were re-measured over committed bytes; no owned axis is harmed. This is not a
promotion, capability or semantic-universality verdict.

## Conformance

- Report attribution: `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-78/tsukuroi.md`
  returned `tsukuroi-shokunin 81c5eba373196618a89be64ef649ba561c2b5066`. The report commit is an
  ancestor of fleet `HEAD` and `origin/master`; the fleet repo had 0 unpushed commits. Report
  landed 2026-11-04 15:39:02 -0300, after lane HEAD 15:37:20. Real report, not a completion marker.
- Cited commits all exist and are ancestors of `master` (checked with `git cat-file -e` and
  `git merge-base --is-ancestor <hash> master`, branch ref never `@{u}`): `07a607df1a5157daafc91bb5c26858af14415f43`,
  `cd71642588c0282a9b73b48f87b415ecdadf6225`, `a15aff6ea38961cae5e6748b1e8f924a1b454c34` — 3/3 OK.
  All three carry author and committer `tsukuroi-shokunin <tsukuroi@shokunin.local>`.
- Lane state: `scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
  printed `branch=master local=a15aff6ea38961cae5e6748b1e8f924a1b454c34 remote=a15aff6ea38961cae5e6748b1e8f924a1b454c34 ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git status --porcelain` was empty before this artifact was written. Remotes:
  `git ls-remote origin refs/heads/master` printed `a15aff6ea38961cae5e6748b1e8f924a1b454c34 refs/heads/master`.
- Report sections appear in the template order: Work performed; Landed changes;
  Before → after measurements; Sources & frontier; Trend verdicts; `## SHONEN` with exactly four
  `[~]` box lines and pointers.
- Prompt fidelity: `.ufo/prompts/tsukuroi-round-78.md` (721 lines; commit
  `f75a24287986fcb90c76ef13f666c979a91a658e`) renders template sections 1–5 byte-identically
  except the concrete working-dir line; §6 hyaku addendum and §7 scratch discipline are present;
  no unresolved `{{…}}` placeholder; the L2 floor is quoted as ≥8 in one batched call and the wave
  used 12.
- `PROVINCE.md`, `SHONEN.md` and `corpus/QUALITY.md` are unchanged; no promotion or capability row
  is claimed.

Dispatch/completion digest (durable copy of the mutable log lines):

```text
2026-11-04T15:16:30-03:00 launch tsukuroi round=78 pgid=256586 driver=hyaku-inline attempt=1
2026-11-04T15:39:35-03:00 complete tsukuroi round=78; hyaku-inline attempt=1
```

## Claim re-checks

No lane gate or lane selftest was executed. Both claims were re-measured over committed bytes with
independent `git show` readers; the lane's selftest tallies and revision-bound receipts were
evidence-verified only.

### C1 — depth (six pinned path-usage cases with review binding)

Independent re-derivation of the frozen predicate (expected cases and pins from
`.ufo/waves/round-78/before/expected.json`; data, reviewer verdict and orchestrator result from the
named paths; no import of the lane instrument). Observed:

```text
b9019a1d0558241bf67cf31ff90256284d8657af  (0, False, 'unreadable:FileNotFoundError')
cd71642588c0282a9b73b48f87b415ecdadf6225  (6, True, 'finite-content-and-review')
a15aff6ea38961cae5e6748b1e8f924a1b454c34  (6, True, 'finite-content-and-review')
```

- The knowledge JSON has exactly six distinct U1–U6 objects and `source: ["S327"]`; equality with
  `expected.json` holds at both the measured revision and lane HEAD.
- `sha256(corpus/knowledge/journald-path-usage-r78.json)` = `13fc82d4cd0756f05b997c7f7a8f64a6976c61aa34d601611a0c73a86a06bd1d`
  equals `ReviewUsage/verdict.json.artifact_sha256`; every verdict is `holds`.
- Companion `sha256` = `f1099591008b0fc8db50a79d72ac9033358dc8af0322816697f2c0a899e98608`
  equals the verdict's `companion_sha256`.
- `w1-results.json` has 12 results and exactly one `ReviewUsage` seat with `agent: reviewer`; its
  output contains `review_sha256=ed92cb4e52eb2aa5cbdf206eb49e46c9eefa64cdfb06c3bbe658522182d0b66e`,
  which equals `sha256(verdict.json)`. All 12 seats have `recovery.source/basis/recovered_at`.
- Snapshot pins match live bytes: I re-fetched
  `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c` and
  `…/v262/man/journalctl.xml` on 2026-11-04 and got the pinned digests `428dc830…a7ffa2` and
  `d54bbede…dedbdd`. Lines 114, 119–121, 123, 124–125, 128–129 and 131 read exactly as the note
  states; the companion explanations (suffix selection, no-follow, failed-stat skip, regular-file
  guard, `st_blocks * 512`, no recursive descent) are accurate for the cited function.
- Reported `count0/met0/rc1 → count6/met1/rc0`: **agree**. The base arm fails because the target
  file does not exist; the after arm is the finite six-case plus binding predicate, not an
  authenticity proof.

### C2 — operability (operative registry findings 10 → 0)

An independent parser over committed bytes (highest `## Gate and probe registry — roundN
superseding current rows` section, its eight-column table, `tools/…` path extraction, kind/verdict/
selftest checks) reproduced the reported counts without running the lane's checker:

```text
b9019a1d…  tools=116 rows=108 registered=108 missing=8 verdict-incomplete=2  → 10 findings
cd716425…  tools=117 rows=117 registered=117 missing=0 findings=0
a15aff6e…  tools=117 rows=117 registered=117 missing=0 findings=0
```

The eight base-missing paths are exactly the eight rows the report names; the two base findings
are the code-2 gaps on `count-jt-rows-r75` and `check-r74-routed-r75`, both now complete.
`git diff --name-status b9019a1d… a15aff6e… -- tools/` is `A tools/measure-journal-usage-r78.py`
only: no existing tool was changed or deleted. Reported
`findings10/missing8/registered108/tools116/rc1 → findings0/missing0/registered117/tools117/rc0`:
**agree**.

### Gate evidence (verified, not executed)

- C1 selftest receipt: `SELFTEST total=15 passed=15 failed=0`, exit 0. Registry selftest receipt:
  `PASS (23 cases, 23 passed, 0 failed)`, exit 0. Knowledge-reference gate: `finding_count: 0`,
  exit 0. All at measured revision `cd716425…`.
- `after/{before,after}-C{1,2}.txt` bind the base and measured revisions, the tool path and digests,
  stdout and exit headers/footers; `after/commands.json` retains the exact runner argv.
- Frozen inputs are unchanged: both source snapshots, `expected.json`, the counter and the target
  data match their freeze digests (`after/structural.json`), and the measured-to-HEAD diff adds
  only evidence/outcome files (LOG/SCORECARD/lesson and `after/*`), not SKILL, tools, corpus data or
  reviewer files.
- Declared limits are retained, not closed here: a complete fabricated review/result bundle and
  false companion prose can pass the numeric C1 gate; the instrument does not import
  `tools/_revision.py`; its selftest is same-reader. These are limits of the finite predicate, not
  a missed target.

## Outside discernment spot-check

The lesson's `## Gate` carries two new rows: **S327 admitted** (tier A, code, mined) and **S328
rejected** as sole implementation support. Both sources were re-opened live on 2026-11-04.

| Item | Gate decision | Re-opened source | Result | Reason |
|---|---|---|---|---|
| S327 | admit, A/code/mined | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c :114–131 | agree | Live sha256 equals the pin `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`; the located quote at :131, `*ret_used += (uint64_t) st.st_blocks * 512UL;` (7 words), and the suffix/no-follow/regular guards at :119–129 are exact; the teaching is scoped to this function, not a live daemon state. |
| S328 | reject as sole proof of manager predicates | https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml :941–948 | agree | Live sha256 equals the pin `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd`; the ≤25-word quote at :943–944 (`This shows the sum of the disk usage of all archived and active journal files.`, 16 words) is present, but the manual describes the CLI result, not suffix selection, `AT_SYMLINK_NOFOLLOW` or `S_ISREG`; the stated flip is the right condition. |
| "Apparent size or symlink-target size determines the sum" | reject | Same manager snapshot :123, :128–129, :131 | agree | `AT_SYMLINK_NOFOLLOW`, the `S_ISREG(st.st_mode)` guard and the `st_blocks * 512UL` addition contradict apparent-size or target-size accounting. |
| Staged adoption / promotion | reject while operator-held | `corpus/SOURCES.md` staging boundary and prior closure | agree | No operator release exists; no package row, promotion or capability is claimed this round. |

Required census re-run:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
→ exit **0**, final line `tsukuroi ok …/tsukuroi-shokunin/corpus/SOURCES.md`, W04 duplicate-URL
warnings only (including the new S327/S328 URLs shared with S325/S323). The report's counts were
re-derived over committed bytes with the contract's documented pattern: rows 326 → 328
(A 309 → 311, B 6, C 11), mined 289 → 290, queued 5, rejected 32 → 33, Markdown knowledge notes
95 → 96. No existing SOURCES row was modified or removed (0 removed `S###` lines).

## Verdicts

| Owned axis | Verdict | Evidence |
|---|---|---|
| depth | improved | C1: six exact finite cases plus a byte-bound author-side review; ordinal 8 unchanged, no uplift claimed. |
| operability | improved | C2: independent count 10 → 0 findings, 117/117 tool rows, 8 missing paths registered and 2 code-2 maps repaired; ordinal 9 unchanged. |
| coverage | unchanged | Existing journald accounting ground deepened; `corpus/README.md` Round 78 says no coverage/frontier promotion. |
| freshness | unchanged | No prior note re-verified or superseded; the new source recheck is `on-release`. |
| calibration | unchanged | Limits and measurement scope stated; no calibration move claimed. |
| adjacency | unchanged | `PROVINCE.md` unchanged; ConnectorScope reports no sibling scope absorbed. |

No owned axis is harmed. Measured ordinals stay depth 8 / operability 9 / coverage 8 / freshness 9 /
calibration 9 / adjacency 7; the round claims no ordinal uplift.

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | unchanged | SOURCES rows +2 but the one new knowledge note deepens existing journald accounting ground; no frontier row advanced, no capability entered. |
| quality | improved | Source-grounded entry with exact upstream anchors and byte-bound review; inherited registry red debt cleared; all receipts revision-bound; no admitted entry found false or stale. |
| discernment | improved | This non-author spot-check agrees on both the S327 admit and the S328 reject (and on the apparent-size reject); the lane's author-side pending status is resolved here, not rewritten. |

## Routed defects — tsukuroi round 79

1. **QUALITY28 instrument conformance.** `tools/measure-journal-usage-r78.py` implements its own
   `git show` revision path instead of importing `tools/_revision.py`. The round discloses this.
   For the next fresh instrument, adopt the shared validator (landed-commit/branch checks) or record
   a named, grounded exception; do not retrofit this frozen counter.
2. **Gate-standard selftest.** The newly registered operative rows `check-r71-routed-r72` and
   `count-md-rows-r72` declare `none: no self-test mode` while registered as `gate`. PROTOCOL
   §Gate standard requires every gate to expose an isolated-fixture selftest asserting exit code and
   a stable finding id. Add it or reclassify as `probe` with a justified registry note; resolve the
   disclosed r73/r74 `rc2` selftest/usage conflation in the same sweep.
3. **Distinguishable red-before controls.** In `before/controls.json`,
   `scripted-fetch-fill-no-review` and `fabricated-review-without-orchestrator-result` both run the
   same `--root` and both print `unreadable:FileNotFoundError`. Record which fixture input is missing
   (or give the two stages distinct reason ids) so the no-review and no-result attacks are
   independently evidenced rather than inferred from the runner's write order.
4. **Duplicate registry rows.** Seven re-registered tools now appear both in the operative round-71
   table and in the round-76/77 continuation tables. Mark those continuation tables explicitly
   non-operative or collapse the duplicates so a reader cannot count two rows for one tool; the
   round-77 routed duplicate concern is only fixed for the new r78 row.
5. **Canonical load order.** The round again discloses that the exact canonical-copy load order was
   not fully followed before freeze (repeat of the r77 routed item). Record the order actually used,
   before freezing, in the r79 declaration, or state why the deviation is unavoidable.
6. **Promotion input (operator-owned, not a defect).** SHONEN box 3's whole-SKILL no-oral-context
   replay remains unexecuted; boxes 1, 2 and 4 look checkable from committed artifacts by a fresh
   non-author, but promotion is operator-owned and no `[x]` is written here.

## Support

Fresh read-only closure checks; no lane gate, tool or selftest was executed; no model parameter was
passed; no tools were installed or updated. Only this verifier artifact and the closure MANIFEST
entry are authored by this closure session.
