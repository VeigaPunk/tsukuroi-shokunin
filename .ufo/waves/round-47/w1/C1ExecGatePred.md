VERDICT: defect-found

# C1ExecGatePred — item C1-K1 (kill rule "predecessor scrub counters PASS→PASS where measured")

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (read-only; nothing tracked was edited).
Base `916019057147d7e9ba6b137647b2cee26decf4b8`, impl `77e9e2b2e96b85d8f048ae2087e246a542b71611`.
Receipts: `.ufo/waves/round-47/w1/C1ExecGatePred/<tool>-<rev8>.json` (12 files, 52 KB total).

## Headline

The **r42–r46 predecessor scrub counters** satisfy the kill rule as written (PASS→PASS where a
counter PASSes; FAIL→FAIL elsewhere, which is by design and not a violation). But the sixth
counter in my item, `tools/check-adjacency-anchors.py`, is **PASS at base and FAIL at the impl
revision** — and the C1 kill-rule cell in `SCORECARD.md:3065` names "adjacency anchors gate PASS"
as a separate clause of the same C1 kill rule. That gate is red at the impl revision.

The red is **already repaired at the lane tip** (`f6bc6d05`, on `master` and `origin/master`):
`IN-109`'s `found_line` was re-pinned 2582→2593 in `corpus/knowledge/adjacency-anchors-r19.json`
because the round-47 C2 census edit moved the D14/D15 case. So this is a **round-47-caused gate red
at the impl revision, fixed after the impl commit** — the "gates at the outcome commit" class the
lane already has a lesson for. The L1 must decide whether the C1 kill rule is scored at the impl
revision (red) or at the tip (green), and must disclose the red either way.

## 1. Kill rule, as declared

`SCORECARD.md:3065` (Round 47 declaration, C1 row, Kill-rule cell), read whole:

> Live census output digits-stripped byte-identical base vs final; GR1/GR3 section hashes equal to
> base; adjacency anchors gate PASS; predecessor scrub counters (r42-r45) PASS→PASS where measured;
> sources census exit 0 at round end

Note the clause is written "r42-r45", but my item lists r42, r43, r44, r45, r46 **and**
check-adjacency-anchors.py. I ran all six.

## 2. Counter invocations (all read-only, `--help` read first)

Each tool's `--help` was read before invocation (usage strings quoted in §5). Every counter takes
`--revision <rev>`; r42–r45 also accept `--lane`/`--sessions`, r46 accepts `--lane`/`--section-hash`,
anchors accepts `--revision`/`--branch`/`--registry`/`--siblings-root`. All six are byte-identical
at base and impl (`git show <rev>:tools/<tool>.py | sha256sum` equal for all six and for
`tools/_revision.py`, and equal to the worktree copy — so no counter was edited this round):

| tool | sha256 (base = impl = worktree) |
|---|---|
| check-scrub-record-r42.py | `dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f` |
| check-scrub-record-r43.py | `b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854` |
| check-scrub-record-r44.py | `c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059` |
| check-scrub-grounding-r45.py | `a1eb402dffae97fcefd9bd539529f1cacc5034419b6de06e1f8ac1c08d011331` |
| check-scrub-admission-r46.py | `28c409bef9a87338831e0cab4c194a78e7fedfefbd9c4a300a33f30b24dd11d8` |
| check-adjacency-anchors.py | `a4f500ef680d92132400b1b75f8c2d26db4a9398deed62bcfa8037ec7bbce2e2` |
| _revision.py (shared binder) | `fc861ec8a4f2539ac3f16d1a04af8335a974c17c8ffba0a41f6dad972cad36de` |

Commands (cwd = my scratch `/fast/scratch/hyaku/tsukuroi-r47/C1ExecGatePred`, `TMPDIR` exported
there):

```
python3 <lane>/tools/check-scrub-record-r42.py     --revision <rev> --lane <lane>
python3 <lane>/tools/check-scrub-record-r43.py     --revision <rev> --lane <lane>
python3 <lane>/tools/check-scrub-record-r44.py     --revision <rev> --lane <lane>
python3 <lane>/tools/check-scrub-grounding-r45.py  --revision <rev> --lane <lane>
python3 <lane>/tools/check-scrub-admission-r46.py  --revision <rev> --lane <lane>
python3 <lane>/tools/check-adjacency-anchors.py    --revision <rev>
```

Both revisions are ancestors of `refs/heads/master` and `refs/remotes/origin/master`
(`git merge-base --is-ancestor` exit 0 for both), so the shared `_revision.bind()` accepts both.
Runs are deterministic: a second run of each counter produced a byte-identical JSON
(sha256 of stdout equal across reruns for all five scrub counters and for anchors at impl).

## 3. Verdicts, base vs impl

| counter | base `91601905` | impl `77e9e2b2` | transition | kill-rule reading |
|---|---|---|---|---|
| check-scrub-record-r42 | **FAIL** rc=1 (`verdicts_ok 1`, `quotes_ok 5`, `rows 5`, `novelty_base_hits 0`, `sources_ok 1`, `host_ok 5`) | **FAIL** rc=1 (same values) | FAIL→FAIL | not a violation (no PASS to preserve) |
| check-scrub-record-r43 | **PASS** rc=0 (`verdicts_ok 3`, `quotes_ok 3`, `props_ok 3`, `host_ok 3`, `rows 3`, `sources_ok 1`, `pointer_ok 1`, `novelty_base_hits 0`) | **PASS** rc=0 (identical) | **PASS→PASS** | **satisfies** the clause |
| check-scrub-record-r44 | **FAIL** rc=1 (`verdicts_ok 0`, quotes/props/host 3, `rows 3`, `pointer_ok 1`) | **FAIL** rc=1 (identical) | FAIL→FAIL | by design, not a violation |
| check-scrub-grounding-r45 | **FAIL** rc=1 (`verdicts_ok 0`, quotes/props/host 3, `rows 3`, `sources_ok 1`, `pointer_ok 1`, `novelty_base_hits 0`) | **FAIL** rc=1 (identical except GR2 quote count, §4) | FAIL→FAIL | by design, not a violation |
| check-scrub-admission-r46 | **FAIL** rc=1 (`verdicts_ok 2`, `marks_ok 0`, `r45_legs_ok 1`) | **FAIL** rc=1 (identical except GR2 fields, §4) | FAIL→FAIL | by design, not a violation |
| **check-adjacency-anchors** | **PASS** rc=0 (`status PASS`, `findings []`, `inbound_classified 114/114`, `DRIFTED 17`, `RESOLVES 96`, `UNRESOLVABLE 1`, `operative 25`, `historical 89`, `outbound_portable 10/10`, `live_object_match 10/10`) | **FAIL** rc=1 (`status FAIL`, 1 finding) | **PASS→FAIL** | **VIOLATION** of "adjacency anchors gate PASS" at the impl revision |

So: exactly one predecessor counter passes at base (r43) and it still passes at impl — the
r42–r45 PASS→PASS clause holds. The **adjacency anchors clause of the same C1 kill rule does not
hold at the impl revision**.

### The failing finding, verbatim

`check-adjacency-anchors-77e9e2b2.json`:

```json
{"id": "INBOUND-CLASSIFICATION-WRONG",
 "site": "corpus/knowledge/adjacency-anchors-r19.json:inbound[108]",
 "detail": "classification DRIFTED is inconsistent: found_line is not an occurrence of evidence_quote (or empty quote requires line 0)"}
```

`inbound[108]` is `IN-109` (sibling `tameshi`, `tools/tsukuroi-census.sh:915-970`,
`scope operative`, `classification DRIFTED`, `evidence_quote
"check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED"`).

Mechanism (`tools/check-adjacency-anchors.py:744-753`: the row is consistent only if
`found_line` is one of the lines where the quote occurs; the expected class is `RESOLVES` if that
line falls in `target_ranges`, else `DRIFTED`):

- The round-47 C2 edit to `tools/tsukuroi-census.sh` (the R47-C2 TMPDIR base fallback + the two
  pinning cases) inserted lines **above** the anchored D14/D15 case, moving it
  **2582 → 2593**:

```
$ git show 91601905…:tools/tsukuroi-census.sh | grep -n "kernel ring class counts are evidence (D14/D15)"
2582:  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
$ git show 77e9e2b2…:tools/tsukuroi-census.sh | grep -n "kernel ring class counts are evidence (D14/D15)"
2593:  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
```

- The registry still carried `found_line: 2582` at the impl revision, so `2582` was no longer an
  occurrence of the quote → classification inconsistent → `INBOUND-CLASSIFICATION-WRONG`.

Attribution is exact: the census edit landed in `3629c46a` ("round-47: C2 TMPDIR-space selftest fix
+ R47-C2 cases; GR2 amended per r46 residual critic; r47 admission counter; S252; declaration"),
which is inside the base..impl range. Bisect by counter status across the round-47 commits:

```
$ python3 tools/check-adjacency-anchors.py --revision <rev>   # status
3c738a87  (round-46 verifier spot-check)   PASS
3629c46a  (round-47 C2 edit + GR2 amendment) FAIL   ← regression enters here
77e9e2b2  (impl)                          FAIL
e31070a9  (round-47 freeze commit)        FAIL
f6bc6d05  (lane tip)                      PASS   ← repaired
```

### Already repaired at the tip

`f6bc6d056ebdf79a585745d4292faf90ae12d9fd` — "round-47: adjacency anchor IN-109 found_line
2582->2593 (R47-C2 census edit moved the D14/D15 case)" — changes exactly two leaves of
`corpus/knowledge/adjacency-anchors-r19.json` (`/inbound[108]/found_line` 2582→2593 and the
appended `/inbound[108]/note` sentence); the rest of the 2571-line file diff is a
re-indentation (1-space → 2-space JSON indent; `git show --stat` reports 2571 insertions /
2571 deletions). Anchors at the tip: **PASS**, `findings []`, `inbound_classified 114/114`,
`DRIFTED 17`, `operative 25` — identical counts to base, and identical to base in every field
except `revision`. Commit is on `master` and on `origin/master`
(`git merge-base --is-ancestor f6bc6d05 origin/master` exit 0).

**Two residue items the L1 should decide on** (neither is a counter failure):

1. The registry's **Markdown companion was not updated**: `corpus/knowledge/adjacency-anchors-r19.md`
   still shows `| IN-109 | … | operative | DRIFTED | 2277 |` (line 204) and `HP-IN-109 … line 2277`
   (line 231) at base, at impl and at the tip. The lane's own precedent (round 32) updated the
   `.json` **and** the two `.md` cells together
   (`corpus/lessons/round-32.md:53-54`: "the IN-109 `found_line` and note in
   `corpus/knowledge/adjacency-anchors-r19.json` and its two cells in `.md`"). The `.md` was
   already stale at base (2277 while the `.json` said 2582) — pre-existing drift, not introduced
   this round — but the round-47 repair widened the gap to 2277 vs 2593 and did not close it.
2. The registry file's **sha256 changed** by the re-indent
   (`ab487c4006d7d496ffc7ab3f8a87a8da7303660591f11387ee374495d291e245` at impl →
   `d613bdf70064f6a8...` at tip). The old digest is pinned as a candidate digest in
   `.ufo/waves/round-45/controls/battery-summary-c1.jsonl:1`
   (`candidate_sha256["corpus/knowledge/adjacency-anchors-r19.json"]`). That is a round-45
   historical receipt, not a live gate, and no tool pins the registry bytes
   (`grep -l "adjacency-anchors-r19.json" tools/*.py` → only `check-adjacency-anchors.py`, which
   parses JSON and does not digest it), so nothing breaks — but a re-indent of a 2571-line pinned
   corpus file for a two-leaf change is avoidable churn and it is worth disclosing.

## 4. Every differing field, base vs impl

Computed by `diff <(python3 -m json.tool --sort-keys <base>.json) <(python3 -m json.tool --sort-keys <impl>.json)`.

### check-scrub-record-r42 — no differing field except the echoed revision
```
97c97
<     "revision": "916019057147d7e9ba6b137647b2cee26decf4b8",
---
>     "revision": "77e9e2b2e96b85d8f048ae2087e246a542b71611",
```
`rows 5, quotes_ok 5, novelty_ok 5, host_ok 5, sources_ok 1, verdicts_ok 1,
novelty_base_hits 0, transcripts_bound 8/8, snapshots_ok true, capture_ok true` — all identical.
Per-row verdicts identical: SC1 `rev None / crit fails`, SC2 `holds/holds`, SC3 `fails/fails`,
SC4 `None/partly`, SC5 `holds/partly`. (r42's own row verdicts come from round-42 wave files,
untouched this round.)

### check-scrub-record-r43 — no differing field except the echoed revision
```
79c79
<     "revision": "916019057147d7e9ba6b137647b2cee26decf4b8",
---
>     "revision": "77e9e2b2e96b85d8f048ae2087e246a542b71611",
```
`verdicts_ok 3, quotes_ok 3, props_ok 3, host_ok 3, rows 3, sources_ok 1, pointer_ok 1,
novelty_base_hits {SR1:0,SR3:0,SR6:0}, transcripts_bound 7/7` — identical. **PASS→PASS.**

### check-scrub-record-r44 — no differing field except the echoed revision
```
83c83
<     "revision": "916019057147d7e9ba6b137647b2cee26decf4b8",
---
>     "revision": "77e9e2b2e96b85d8f048ae2087e246a542b71611",
```
`verdicts_ok 0, quotes_ok 3, props_ok 3, host_ok 3, rows 3, pointer_ok 1,
novelty_base_hits {SR7:0,SR8:0,SR9:0}, transcripts_bound 4/4` — identical. Per-row:
SR7 `rev None/crit holds`, SR8 `partly/holds`, SR9 `partly/crit None`.

### check-scrub-grounding-r45 — one substantive differing field
```
49c49
<                 "good": 26,
---
>                 "good": 28,
86c86
<     "revision": "916019057147d7e9ba6b137647b2cee26decf4b8",
---
>     "revision": "77e9e2b2e96b85d8f048ae2087e246a542b71611",
```
The change is confined to `per_row.GR2.quotes.good` **26 → 28**; `in_window` stays 11 and `bad`
stays 0, and `files` stays `["S242:scrub.c","S243:sysfs.c","S247:dev-replace.c"]`. Cause: the
pre-wave GR2 amendment added two new `**Quote.**` lines to the entry —
`S242 scrub.c:3094 "if (btrfs_fs_closing(fs_info))"` and `S242 scrub.c:3095 "return -EAGAIN;"`
(`git diff 91601905… 77e9e2b2… -- corpus/knowledge/btrfs-scrub-grounding-r45.md`) — which is the
declared amendment. Both new quotes are outside the r45 GR2 windows
(`(('S242','scrub.c'),3079,3081)` and `(('S242','scrub.c'),3146,3153)`), so `in_window` does not
move, but both validate against the frozen S242 snapshot, so `good` rises by 2. `quotes_ok`
remains 3. **This is the amendment working as declared, not a drift.**

### check-scrub-admission-r46 — two substantive differing fields, both inside GR2
```
52c52
<             "bound_on_current": 2,
---
>             "bound_on_current": 0,
86c86
<             "section_sha256": "4bf28bcf3682fc5bed1d020601f35d19f696301579d2fe66f8667e7f7602f6da"
---
>             "section_sha256": "909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2"
```
Both are consequences of the **same pre-wave GR2 amendment** and are expected:
the row's section bytes changed, so its section sha256 changed, so the round-46 seats'
`SECTION SHA256:` lines (bound to the *old* GR2 bytes, `4bf28bcf…`) no longer match the current
section (`909830c8…`) — hence `bound_on_current` 2 → 0 and `row_ok` false for GR2. This is
precisely the round-47 mechanism the declaration describes (round-47 seats re-read the amended
rows and bind new hashes; the round-46 residual seats bound the pre-amendment bytes and are
therefore stale by construction). Verified independently with the counter's own hash printer:

```
$ python3 tools/check-scrub-admission-r46.py --revision <rev> --lane <lane> --section-hash
base  91601905: GR1 fe77ac76… GR2 4bf28bcf… GR3 43430a14…
impl  77e9e2b2: GR1 fe77ac76… GR2 909830c8… GR3 43430a14…
tip   f6bc6d05: GR1 fe77ac76… GR2 909830c8… GR3 43430a14…
```

`GR1` and `GR3` section hashes are **equal to base** at impl and at tip — the kill rule's
"GR1/GR3 section hashes equal to base" clause holds. `verdicts_ok 2`, `marks_ok 0`,
`r45_legs_ok 1`, `waves_seen ["r1","w1"]`, `marks {entry:false, readme:false, skill:false}` are
identical at base and impl; only GR2 moved. (r46 reads the *round-46* seat universe
`V46*GR<n>{a,b}`, `V46Res*GR<n>`; the round-47 seat names `R47*` are a different universe, so
r46's `verdicts_ok 2` cannot rise from this round's seats.)

### check-adjacency-anchors — every differing field
```
status:              "PASS" → "FAIL"
findings:            [] → [1 finding: INBOUND-CLASSIFICATION-WRONG @ …:inbound[108]]
counts.inbound_by_class.DRIFTED:            17 → 16
counts.inbound_by_class.RESOLVES:           96 → 96   (unchanged)
counts.inbound_by_class.UNRESOLVABLE:        1 →  1   (unchanged)
counts.inbound_by_scope.operative:          25 → 24
counts.inbound_by_scope.historical:         89 → 89   (unchanged)
counts.inbound_classified:                 114 → 113
counts.inbound_total:                      114 → 114   (unchanged)
counts.outbound_portable / outbound_total:  10/10 → 10/10 (unchanged)
counts.live_object_checked / live_object_match: 10/10 → 10/10 (unchanged)
branch / branch_tip:  master / f6bc6d05… → master / f6bc6d05…  (unchanged)
revision:             91601905… → 77e9e2b2…
```
The single classified record lost is `IN-109` (it drops out of `inbound_classified` and out of
the `DRIFTED`/`operative` tallies because its classification became inconsistent). No other row
moved. At the tip `f6bc6d05` every one of these counts returns to the base value and `findings`
is empty again.

## 5. `--help` output, per tool (read before running)

```
check-scrub-record-r42:    usage: … [--revision REVISION] [--lane LANE] [--sessions SESSIONS]
check-scrub-record-r43:    usage: … [--revision REVISION] [--lane LANE] [--sessions SESSIONS]
check-scrub-record-r44:    usage: … [--revision REVISION] [--lane LANE] [--sessions SESSIONS]
check-scrub-grounding-r45: usage: … [--revision REVISION] [--lane LANE] [--sessions SESSIONS]
check-scrub-admission-r46: usage: … [--revision REVISION] [--lane LANE] [--section-hash]
check-adjacency-anchors:   usage: … (--revision REV | --selftest) [--ownership-corrections]
                                    [--branch BRANCH] [--registry REGISTRY]
                                    [--registry-from REV] [--siblings-root SIBLINGS_ROOT]
```
(`--revision` is 7-64 hex, "landed and pushed on the selected branch"; `--branch` defaults to
`master`.)

## 6. Cross-checks and what I did NOT do

- The round-47 counter itself (`tools/check-scrub-admission-r47.py`) was run read-only for
  orientation only, at impl and at tip: both **FAIL** with
  `structural_ok 1, quotes_ok 3, verdicts_ok 0, marks_ok 0` — i.e. the wave's seats have not yet
  bound, so C1 is still open. This is expected mid-wave and is not part of the K1 kill rule.
- `check-scrub-admission-r46.py` **re-executes** the r45 counter as a leg
  (`r45_legs`: `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, novelty_base_hits 0,
  pointer_ok 1`, `r45_legs_ok 1`) — identical at base and impl, and the r45 script's sha256
  matches r46's frozen `R45_SHA` constant, so the leg is running the frozen counter.
- Not run: the census `--selftest` (C2's measured command; the rule says one heavy counter at a
  time and it is not mine to measure here), `check-adjacency-anchors.py --selftest`, and any
  mutating/host-touching action. No package, service, sysfs write, `btrfs` scrub/replace, or
  `systemctl` mutating call was made; no `git add/commit/stash/checkout/reset/push` and no `jj`
  mutation was run in the lane. Only `git show/ls-tree/log/merge-base/status/rev-parse` reads.
- The lane working tree was already dirty before I started (other seats' untracked wave files and
  a modified `.ufo/waves/round-47/w1.ready.partial`); `git status --porcelain` shows no tracked
  file modified by me. My only lane writes are the 13 receipt JSONs in
  `.ufo/waves/round-47/w1/C1ExecGatePred/` and this report.
- No tools were installed or upgraded for this item; `python3` and `git` (system) sufficed.
  Nothing was installed, so no tool/channel/version record is owed under
  `/home/vgpnk/.omp/agent/RULES.md`.
- My scratch `/fast/scratch/hyaku/tsukuroi-r47/C1ExecGatePred/` was removed after the receipts
  were copied into the seat directory.

## 7. Exact proposed text for the L1 (SCORECARD / LOG — do not apply; the L1 integrates)

For the C1 kill-rule cell (`SCORECARD.md:3065`), if the kill rule is scored at the impl revision,
the adjacency clause must read as violated; if scored at the tip, the disclosure is:

> C1 kill-rule reading: the r42–r46 predecessor scrub counters satisfy the rule as written
> (r43 PASS→PASS; r42, r44, r45, r46 FAIL→FAIL by design, `verdicts_ok` unchanged).
> `check-adjacency-anchors.py` was **PASS at base `91601905` and FAIL at the impl revision
> `77e9e2b2`** — one finding, `INBOUND-CLASSIFICATION-WRONG` at
> `corpus/knowledge/adjacency-anchors-r19.json:inbound[108]` (`IN-109`), because the round-47 C2
> census edit moved the anchored D14/D15 case in `tools/tsukuroi-census.sh` from line 2582 to
> 2593 while the registry still pinned `found_line` 2582. The regression entered at `3629c46a`
> (bisect: `3c738a87` PASS → `3629c46a` FAIL) and was repaired at the tip `f6bc6d05`
> (`found_line` → 2593; anchors PASS, `findings []`, `inbound_classified 114/114`, counts equal
> to base). Disclosure: the repair re-indented the whole 2571-line registry file (two semantic
> leaves changed) and left the Markdown companion `corpus/knowledge/adjacency-anchors-r19.md`
> lines 204 and 231 still showing the round-32-era `2277`.

## 8. Risks and blockers

- **Risk (the one that matters):** if the C1 kill rule is scored at the impl revision
  `77e9e2b2`, the "adjacency anchors gate PASS" clause is **red** — a real PASS→FAIL regression
  caused by this round. It is green at the tip, so the score depends on the scoring revision and
  on whether the L1 discloses the red rather than presenting only the tip. The lane already has
  the applicable lesson: "Gates at the outcome commit" (round-35,
  `corpus/lessons/round-35-verifier-spotcheck.md:91`) and the identical R38-ANCHOR-SHIFT
  recurrence (`corpus/lessons/round-38.md:87`).
- **Risk:** the counted round-47 C1 seats bind verdicts to the **current** GR2 section bytes
  (`909830c8…`). The r46 counter shows the round-46 residual seats bound the pre-amendment GR2
  bytes (`4bf28bcf…`) and therefore no longer bind. This is expected under the declaration's
  two-generation amendment rule, but it means any narrative that cites r46's `verdicts_ok 2` as
  "GR2 still bound" would be wrong: GR2's `bound_on_current` is 0 at impl and tip.
- **Risk:** the registry re-indent changes the file's sha256 (`ab487c40…` → `d613bdf7…`), which
  is quoted as a candidate digest in the round-45 battery receipt. No live gate consumes it, so
  nothing is broken, but the digest quoted in `.ufo/waves/round-45/controls/battery-summary-c1.jsonl:1`
  no longer matches the file on disk.
- **No blocker.** Every check in this item ran and is reported; nothing was skipped silently.

## 9. Addendum (measured after the item closed): the r47 C1 counter has no anti-recycle leg

Prompted by a peer report of the same defect class in another lane ("the C1 counter admits a
recycled round-49 entry"), I probed the round's own counter
`tools/check-scrub-admission-r47.py` for the same gap. Two fixtures, both in scratch, both
read-only against the lane; receipts in this seat directory.

### 9a. A recycled (pre-amendment) entry PASSes — the counter cannot see the amendment

The counter carries **no novelty leg**: `grep -c novelty tools/check-scrub-admission-r47.py` = **0**,
while every predecessor carries one (`novelty_base_hits == 0`: r42, r43, r44, r45 each with 5
`novelty_hits` references, r46 2; e.g. `tools/check-scrub-grounding-r45.py:286-291`
`def novelty_hits(lane, token)` → `git grep -n -F -- token BASE -- corpus/knowledge SKILL.md`).

Fixture: clone the lane at impl `77e9e2b2`, restore `corpus/knowledge/btrfs-scrub-grounding-r45.md`
to its **base `91601905` bytes** — i.e. GR2 in the pre-amendment wording the round-46 residual
critic read `partly` — append only the round-47 admission mark line, add the SKILL/README marks,
and bind two fabricated `holds` per row to the recycled section hashes. Result:

```
python3 tools/check-scrub-admission-r47.py --revision <fixture> --lane <fixture>   -> rc 0
{"verdict": "PASS", "structural_ok": 1, "quotes_ok": 3, "verdicts_ok": 3, "marks_ok": 3}
per_row GR1/GR2/GR3: row_ok true, bound_on_current 2, distinct_bodies true, citations_ok true
GR2 section hash bound: 4bf28bcf3682fc5bed1d020601f35d19f696301579d2fe66f8667e7f7602f6da
                     (the PRE-amendment GR2; the lane's amended GR2 is 909830c8…)
```

Deterministic (two runs, byte-identical stdout). Receipts:
`C1ExecGatePred/check-scrub-admission-r47-recycled-entry.json`,
`C1ExecGatePred/recycled-entry-witness.txt`, `C1ExecGatePred/recycle-probe.py`.

**Why it matters for this round's C1 claim.** The declaration's C1 surface is "GR1-GR3 admitted:
GR2 **amended** pre-wave per `r1/V46ResCritGR2.md`". The counter's predicate
(`structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`) is satisfied by
the *un-amended* entry, because section hashes are computed from whatever bytes are current and
the seats bind to those same bytes. The counter therefore proves internal consistency, not that
the amendment happened — so it cannot be cited as evidence for the "amended" half of the claim.
The lane's actual tip *does* carry the amendment (verified in §3 of this report), so the claim's
factual content is intact; what is not intact is the counter's discriminating power on that axis.

### 9b. A one-line stub body is correctly rejected — that guard does exist

The same counter *does* resist the other half of the peer's finding class. A fixture whose seat
reports are the two binding lines plus a single `see cmdline.c:156` line FAILs:

```
{"verdict": "FAIL", "verdicts_ok": 0}
GR1 R47CritGR1a -> report body under 300 bytes
GR2 R47CritGR2a -> report body under 300 bytes
GR3 R47CritGR3a -> report body under 300 bytes
```

Guards responsible: body ≥ 300 bytes and a row-source `file:line` citation
(`tools/check-scrub-admission-r47.py:222-224`), citation resolution against the digest-pinned
snapshots (`:286-293` `report_citations_ok` → `:241` `verify_citation`), pairwise-distinct bound
bodies (K23, `:352-354`). Receipt:
`C1ExecGatePred/check-scrub-admission-r47-stub-oneline.json`. Individual controls K22a
(nonexistent citation) and K23a (byte-identical reports) already cover these at
`.ufo/waves/round-47/controls/battery-summary-r47.jsonl:3-4`.

### 9c. Disposition

Not a blocker for this item and not a change to any verdict above: my item (C1-K1) is the
predecessor counters, and they are reported in §3. This addendum is for the L1's C1 falsification
budget: the natural closure is a novelty leg on GR2 (require the row's section hash to differ from
its base/round-46 value, or grep the amended sentences at BASE = 0 hits, mirroring r45's
`novelty` leg), applied only to a future generation of the counter — the r47 counter is frozen for
this round and `--revision` scoring stays as declared.
