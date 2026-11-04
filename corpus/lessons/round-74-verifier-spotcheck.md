# Round 74 — verifier spot-check (hyaku closure, non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04
lane: tsukuroi-shokunin
base → measured: `d749a625b3054b7cb3435983fb9626ab3d0ed0c4` → `dc5114c5eb8e6349780d7bca8eb6e7470ec55553`; lane tip / remote `c3faaef8c47be23a831f0f9310815549767e8112`

Round verdict: **rejected-honest-stop** — real, verified work (six true sourced UF rows; both r73
repairs), but the frozen C1 clause ("service, socket, target, device, and **volume**") is falsified by
the pinned `unit-file.h:25-32` (SERVICE/SOCKET/TARGET/DEVICE/**TIMER/PATH**), so not every claim
verifies. The lane self-declared the honest stop; this closure independently reproduces it. No axis
harmed. Three read-only reviewer seats re-checked in parallel (C1 rows / C2 repairs / wave accounting).

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report authorship | `git log --format='%an %ae %H' -- .ufo/reports/round-74/tsukuroi.md` | `tsukuroi-shokunin <tsukuroi@shokunin.local> 2c0039b1a889f23f97b2d5fc3aa73c322dabe173` | PASS |
| SHONEN heading | `grep -c '^## SHONEN' .ufo/reports/round-74/tsukuroi.md` | 1 heading + 4 `[~]` lines (4 boxes) | PASS |
| Cited commits exist + ancestor of branch | `git cat-file -t` + `git merge-base --is-ancestor <h> master` for e51fb49d, 810daf13, dc5114c5, c3faaef8, d749a625 | all `ancestor-of-master OK` | PASS |
| Lane pushed / no lane debt | `scripts/hyaku/jj-lane.sh state` | `branch=master local=remote=c3faaef8 ahead=0 behind=0` | PASS |
| Working tree | `git status --porcelain` | 5 untracked wave-runner markers only (`.ufo/waves/{66,67,73,74}/w1.ready.dispatched`, `round-73/w1-run.stderr` — seat→id dispatch bookkeeping written by the wave runner, not lane round work; same class carried untracked through r72/r73 closures) | PASS (noted) |
| Prompt contract | read `.ufo/prompts/tsukuroi-round-74.md` | full template contract rendered (report path/filename, commit-before-report order, SHONEN heading rule, hash-citation rule, write scope) + §6 run-15 addendum + pacman/scratch guards; committed by lane identity (698efaa2 attempt 2) | PASS |
| Marker predicate | report substance | real report, 4 landed commits, evidence pointers throughout | not a marker |

Attempt-1 dispatch died without a report (`lane-dead-no-report`, watchdog 00:23:35-03:00); attempt 2
launched 00:23:37 and completed 00:57:24. Digest copied into MANIFEST notes.

## 2. Per-claim re-check (closure-run measurements over committed bytes)

### C1 depth — mechanical target re-measured; literal claim independently FALSIFIED

Closure-run (not lane receipts):

```
$ python3 tools/count-uf-rows-r74.py --revision d749a625b3054b7cb3435983fb9626ab3d0ed0c4
UF_MAP absent            rc=128
$ python3 tools/count-uf-rows-r74.py --revision dc5114c5eb8e6349780d7bca8eb6e7470ec55553
UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0 met=1   rc=0
$ python3 tools/count-uf-rows-r74.py --revision c3faaef8c47be23a831f0f9310815549767e8112
UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0 met=1   rc=0
```

Registry/knowledge counts, closure-counted: `git show <REV>:corpus/SOURCES.md | grep -cE '^ {0,3}\| *S[0-9]+ *\|'`
and `git ls-tree --name-only <REV>:corpus/knowledge | grep -c '\.md$'`:
d749a625 → 308 / 91; dc5114c5 → 313 / 92; c3faaef8 → 313 / 92. Report values reproduce exactly.

Literal-claim falsification (closure-read of the frozen snapshot, digest `e55b17a1…` = SHA256SUMS =
S311 row = note UF3/UF4 digest cells):

```
25| static inline bool unit_type_may_alias(UnitType type) {
26|         return IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET,
31|                       UNIT_TIMER, UNIT_PATH);
```

`grep UNIT_VOLUME` over the whole header: 0 occurrences. The frozen C1 sentence ("…service, socket,
target, device, and volume units") is false; timer/path are the true members. The lane's SCORECARD
erratum R74-DECL-ALIAS-SET refuses literal credit and claims no uplift; QUALITY 106 carries the
red/green evidence. Reviewer seat R74C1Rows additionally verified: note absent at e51fb49d and at base
(fatal rc 128, first lands dc5114c5); R1Reviewer's reviewed-bytes pin `5daaa9f7046c…` equals the
sha256 of the landed SC1Entry draft and the UF table landed verbatim (prose hunks only); all three
snapshot digests match their pins; live URLs for unit-file.c / load-fragment.c / unit-file.h all HTTP
200 today.

Held-ground sweep re-run: `git grep -nE 'unit_file_find_fragment|unit_ids_map_get|unit_file_build_name_map|unit_type_may_alias|unit_file_resolve_symlink|builtin_unit_lookup' d749a625 -- corpus/ SKILL.md PROVINCE.md` → 0 matches (exit 1). The plane is genuinely new ground.

Instrument integrity: `sha256sum tools/*.py` → counter `94d46a5e…36482`, checker `2da4ff1f…fd77`, both
equal to the frozen digests; `git diff d749a625 c3faaef8 --stat -- tools/` shows the two files as new
this round (574 insertions, 0 deletions) — no pre-existing instrument or tool modified. Gate-standard
evidence verified (not re-scored by the lane's own authority alone): committed receipt
`after/measure-dc5114c5.txt` records the frozen run (cat-file commit → before rc128/rc1 → after rc0/rc0),
selftests `PASS (13 cases)` / `PASS (6 cases)`, digests, census rc 0. The closure's own runs above match
the receipt byte-for-byte in verdict and counts.

Claim verdict: **mechanical target met and re-measured; literal claim not verified** (lane's own
honest-stop reproduced independently). Depth ordinal stays 8; no score uplift taken.

### C2 freshness — repairs re-measured and read directly

Closure-run:

```
$ python3 tools/check-r73-routed-r74.py --revision d749a625b3054b7cb3435983fb9626ab3d0ed0c4
ROUTED_STALE=2 ROUTED_OK=0/2   rc=1
$ python3 tools/check-r73-routed-r74.py --revision dc5114c5eb8e6349780d7bca8eb6e7470ec55553
ROUTED_STALE=0 ROUTED_OK=2/2   rc=0
$ python3 tools/check-r73-routed-r74.py --revision c3faaef8c47be23a831f0f9310815549767e8112
ROUTED_STALE=0 ROUTED_OK=2/2   rc=0
```

Reviewer seat R74C2Repairs verified by direct reading: Correction 3 appended to
`corpus/lessons/round-73.md` (diff = 0 deletions / 6 additions; absent at base); the pinned install.c
snapshot (S306, digest `c11cd575…`) shows the quoted content at **2383** (`path_make_absolute`) while
2387 is a different statement (`create_symlink /dev/null`) — the supersede is correct; the S304 man-page
snapshot (digest `eb9479be…`) confirms the three narrowed anchors :368-370, :237-238, :238-239 (old
:238-240 over-ran into a blank line); LOG's count correction is an unheaded append inside the last
Round-73 block naming superseded 12/11 and final 13/14 (diff: one hunk, all `+`); R2Reviewer HIGH-1
proves the frozen checker's first-match predicate shadows an EOF-headed correction, which is why Form A
was required. Freshness ordinal stays 9 (no uplift claimed).

Claim verdict: **verified** — mechanically re-measured and semantically read.

## 3. Discernment spot-check (LEARNING.md — non-author, this file)

| item | lane decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S309 admit (unit-file.c v262) | admit, mined | frozen snapshot digest `141ab101…` + live URL HTTP 200 | **agree** | :416 quote "Search paths are ordered by priority (highest first)…" verified verbatim at snapshot line 416; ≤25 words; tier A/code correct |
| S311 admit (unit-file.h v262) | admit, mined | frozen snapshot digest `e55b17a1…` + live URL HTTP 200 | **agree** | :26-32 quote matches the pinned bytes exactly; this is also the source that falsifies the literal C1 clause |
| S312 reject (ArchWiki Systemd) | reject, tier B/community | live URL HTTP 200, body 152032 bytes (exactly the recorded size) | **agree** | `grep -oiE 'unit_type_may_alias\|UNIT_MASKED\|load-fragment\|fragment'` over the fetched body: 0 matches — the page is an administrative overview and cannot ground alias-type/mask rules; flip condition is sound |
| S313 reject (unit-load.c v262) | reject, unreachable | live URLs HTTP **404** at both src/core and src/shared candidate paths | **agree** | payload genuinely unavailable; refusal discloses the missing quote instead of fabricating one — the disclosed-null handling is exactly right |

SOURCES.md row check (rule: ≤25-word located quote for every new row): S309/S310/S311 row quotes
re-verified against snapshots (word counts 14/8/22 incl. code tokens — within limit; S310 quote
"don't allow perpetual units to ever be masked" verified at load-fragment.c:6250). S312's teaches cell
is a rejection reason (title quote, 3 words) and S313's states the 404 with no content quote — both
contract-conformant for rejected rows.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` →
`tsukuroi ok … corpus/SOURCES.md`, exit_code=0 (W04 duplicate-URL warnings only, all pre-existing) —
closure-run, matches the report's start/end receipts.

Spot-check result: **agree on 2 admits + 2 rejects, zero disagreements**. Discernment is checked from
outside this round by this closure.

## 4. Wave accounting (critic seat R74Wave, corroborated)

12 seats, roles {scout 1, executor 3, scribe 3, connector 1, reviewer 2, critic 1, mutation-tester 1};
band 8-16 (spawn 12); strict attack 4/12 = 33% (R1Reviewer, R2Reviewer, K1Critic, M1Mutation);
connector 1; L1 held planner; residual 0; dispatch commit 810daf13 carries spec+dispatch;
`w1-results.json` = 9 nonempty finals, exactly SC1Entry/SC3Index/M1Mutation empty (`len:0`, `note:null`);
no dead seat replaced. Watchdog digest (launch/dead/launch/complete) corroborated from
`.ufo/watchdog.log`. SC1Entry's 429 quota death corroborated in-wave by R2Reviewer's final;
M1Mutation left only a fixture matrix, no battery — not credited, as reported. Accounting: accurate.

## 5. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth | unchanged | C1 falsified as declared; honest stop, no uplift. True six-row note is real corpus expansion (carried under expansion), not an admitted depth axis-move |
| coverage | unchanged | no coverage claim; registry growth is expansion, not surface coverage |
| operability | unchanged | no new capability row claimed; round instruments are claim tools, not registered capabilities |
| freshness | **improved** | both r73 routed repairs landed append-only, verified mechanically (stale 2→0, closure-run) and by direct snapshot reading |
| calibration | unchanged | score 9; strong self-catch is real (false claim refused, all limits disclosed) but no ordinal move is taken |
| adjacency | unchanged | connector scan names no sibling absorption; boundaries restated |

No owned axis harmed: the SCORECARD diff base→tip is append-only (all `+` lines); LOG/PROVINCE/SKILL/
README/QUALITY diffs are appends; `tools/` gained two new files with 0 deletions elsewhere.

## 6. Trend verdicts

- **expansion: improved.** One true six-row note on verified-new ground (held-ground 0 matches,
  closure-run), three mined tier-A sources, two measured refusals; registry 308→313 and notes 91→92
  closure-counted; census rc 0.
- **quality: improved.** Both r73 repairs closed (stale 2→0 on the unchanged frozen instrument);
  the false frozen alias set and the invalid base OID are explicitly rejected, corrected append-only,
  and mined into QUALITY 106/107 with red/green evidence; no admitted entry left failing its re-check
  (the errata are append-only, the original declaration text preserved as the falsified record).
- **discernment: improved.** The outside (this closure) spot-check agrees with the gate on all sampled
  admits and rejects; in-wave attacks found the literal claim error and the lexical channels; every
  disagreement/limit is mined (eight mistake classes in the r74 lesson; QUALITY 106/107) — no
  unlearned disagreement, no criterion without a lesson behind it.

## 7. Routed defects for the lane's next round

1. **SC3Index death receipt missing.** The 429 `RESOURCE_EXHAUSTED` death exists only as L1 report
   prose; no committed death receipt under `.ufo/waves/round-74/` (lane convention r21/r65 persists
   `death-*.json`). Persist the receipt or file an erratum naming its absence.
2. **Report wording vs disk.** "SC3Index left no completed doc drafts" contradicts the 27.5 KB
   self-verified `SC3Index/report.md` on disk; the accurate statement is "no review-accepted drafts
   (no reviewer covered scribe docs)". Fix the wording in the next report/lesson.
3. **Corrections-sweep residue.** `.ufo/waves/round-74/w1/E3HostProbe/receipt-g-landing.txt:4` still
   prints the fabricated full OID `d749a625f483c66f2a6f2005db3799630c776bc3` in its header (controls
   cite the resolving short). QUALITY 107's own rule requires the sweep to catch every mention; append
   a naming correction.
4. **Stale freshness axis-table row.** The last structured `| freshness |` axes-table row is round 65;
   rounds 66-74 updated the ordinal in prose only. Restate the axes table so the score row resolves.
5. **Named instrument limits (disclosed; fix only if instruments are ever revised):** the counter's
   aggregate prints `PASS` with exit 3 on a failing run (exit code is decisive, label misleading);
   C2's selftest embeds a literal answer key.
6. **Process (self-disclosed conformance debt):** protocol/skill loading completed after freeze and
   dispatch; initial wave context omitted the pacman/scratch guard paragraphs. Load contracts before
   freeze next round.
7. **Operator note (not a lane defect):** all four SHONEN boxes now look fully checkable by a
   non-author — box 1 (SKILL r74 decision table + UF1-UF6 + S309-S311), box 2 (logged read-only host
   task with receipts), box 3 (whole-skill no-oral-context retest still the open L0 round-60 item),
   box 4 (connector scan clean). Promotion review is operator-owned; no `[x]` was written by this
   closure.

Closure grade: round **rejected-honest-stop** (C1 literal claim falsified; C2 verified; no axis
harmed; every defect above is wording/evidence-persistence level, none reaches the claim accounting).
