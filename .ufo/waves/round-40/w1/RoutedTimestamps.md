VERDICT: defect-found

Item R-1 (round-39 closure §6.3) — heading stamps later than their commits. Swept at HEAD
`f951f288483c1af0cef4afd458488b84cf7a2165`; `git diff --quiet -- SCORECARD.md LOG.md` → rc 0, so every line number below pins
to HEAD. `sha256(SCORECARD.md)=3faf7ff1e9eb7154a609da0cf3c83cb134e03ddcf7e77c5b43dc47eed0c52e62` (2321 L),
`sha256(LOG.md)=721ee7114b5f1409b3efaadbb3bd99bdfd37af8385bca0b27d20aeb232119088` (1477 L). Method: committer time `%cI`
(converted to UTC), introducing commit = the *oldest* `-S` hit whose own blob contains the heading line and whose parent does
not. Sweep clock at run: 2026-10-26T07:16:39Z.

## 1. The two prescribed measurements

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --format='%h %cI' -S'Round 39 — declaration (2026-10-26T06:20Z' -- SCORECARD.md LOG.md
93fddb2 2026-10-26T02:59:31-03:00

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --format='%h %cI' -S'Round 39 — hyaku run 8, 2026-10-26T07:45Z' -- SCORECARD.md LOG.md
eeba342 2026-10-26T03:35:44-03:00
```

Introductions proven against the parent (one `-S` hit each, so the line never changed afterwards):
`93fddb2c37aed8227b4a0ff2417b104e01446a9d` SCORECARD.md present_in_commit=1 present_in_parent=0;
`eeba342ea06ad0069899b3b8b4bbea6af98df610` LOG.md present_in_commit=1 present_in_parent=0.

| Target | Heading line (HEAD) | Stated | Introducing commit (committer, UTC) | Delta |
|---|---|---|---|---|
| SCORECARD.md:2209 | `## Round 39 — declaration (2026-10-26T06:20Z, base \`0eff65b2…\`, before any seat)` | 2026-10-26T06:20Z | `93fddb2c` 2026-10-26T05:59:31Z | **+20 min 29 s** |
| LOG.md:1457 | `## Round 39 — hyaku run 8, 2026-10-26T07:45Z` | 2026-10-26T07:45Z | `eeba342e` 2026-10-26T06:35:44Z | **+1 h 09 min 16 s** |

Both commits have author time == committer time (`%aI` == `%cI`), so the offset choice does not affect the finding.

## 2. Full sweep — every heading in rounds 35–39 carrying a clock token

Ranges (append-only files): SCORECARD.md from 1499 (`## Round 35 — declaration, pre-freeze candidate`) to EOF; LOG.md from
1329 (same heading) to EOF. Per heading the same `-S '<heading text>' -- SCORECARD.md LOG.md` introduction test above.
26 headings carry a clock token: 25 parseable stamps, 1 malformed. `d` = stated − committer, seconds unless marked m.

| file:line | rnd | stated (UTC) | introducing commit (committer, UTC) | d |
|---|---|---|---|---|
| LOG.md:1333 | 35 | 2026-10-23T11:40Z (`~11:40Z`) | `7186722b` 11:37:49Z | **+131** |
| LOG.md:1337 | 35 | 2026-10-23T12:00Z (`~12:00Z`) | `e2f97e6e` 11:52:40Z | **+440** |
| LOG.md:1343 | 35 | 2026-10-23T12:00Z (`~12:00Z`) | `95684c65` 11:57:41Z | **+139** |
| LOG.md:1347 | 35 | 2026-10-23T12:05Z (`~12:05Z`) | `199beb97` 12:00:35Z | **+265** |
| LOG.md:1351 | 35 | 2026-10-23T12:26Z | `6f92080d` 12:25:23Z | **+37** |
| LOG.md:1355 | 35 | — (erratum heading, no stamp) | `c535371b` 12:25:57Z | — |
| LOG.md:1359 | 36 | 2026-10-23T02:33Z (`2026-10-23, 02:33Z`) | `6d76fb20` 2026-10-24T02:34:31Z | −1441.5 m |
| LOG.md:1369 | 36 | 2026-10-24T04:22Z | `1e926801` 04:28:11Z | −371 |
| LOG.md:1375 | 36 | 2026-10-24T04:28Z | `1e926801` 04:28:11Z | −11 |
| LOG.md:1379 | 36 | **unparseable** `2026-10-24T04:4043Z` | `d39da87a` 04:41:33Z | n/a |
| LOG.md:1383 | 37 | 2026-10-25T19:07:13Z | `543a7cee` 19:20:15Z | −13.0 m |
| LOG.md:1393 | 37 | 2026-10-25T19:20:00Z | `543a7cee` 19:20:15Z | −15 |
| LOG.md:1397 | 37 | 2026-10-25T19:21:12Z | `718cc8f1` 19:21:32Z | −20 |
| LOG.md:1401 | 37 | 2026-10-25T19:22:22Z | `d621b712` 19:22:39Z | −17 |
| LOG.md:1405 | 37 | 2026-10-25T19:33:21Z | `29b22df1` 19:34:37Z | −76 |
| LOG.md:1409 | 37 | 2026-10-25T19:36:54Z | `6dbfe327` 19:37:13Z | −19 |
| LOG.md:1419 | 37 | 2026-10-25T19:39:22Z | `3c456a50` 19:39:36Z | −14 |
| LOG.md:1423 | 37 | 2026-10-25T19:41:40Z | `e2e32de7` 19:42:06Z | −26 |
| LOG.md:1441 | 38 | 2026-10-26T05:24:56Z | `fc931bdb` 05:24:56Z | **0** |
| LOG.md:1457 | 39 | 2026-10-26T07:45Z | `eeba342e` 06:35:44Z | **+4156** |
| SCORECARD.md:1686 | 36 | 2026-10-24T04:22Z | `c052bb7d` 04:28:31Z | −391 |
| SCORECARD.md:1761 | 36 | 2026-10-24T04:39Z | `d39da87a` 04:41:33Z | −153 |
| SCORECARD.md:1816 | 36 | 2026-10-24T04:44Z | `4b2d2636` 04:49:22Z | −322 |
| SCORECARD.md:1835 | 36 | 2026-10-24T04:48Z | `4b2d2636` 04:49:22Z | −82 |
| SCORECARD.md:2107 | 38 | 2026-10-26T04:16Z | `7cbaeb63` 04:16:08Z | −8 |
| SCORECARD.md:2133 | 38 | 2026-10-26T04:32Z | `9c9bb647` 04:32:13Z | −13 |
| SCORECARD.md:2209 | 39 | 2026-10-26T06:20Z | `93fddb2c` 05:59:31Z | **+1229** |

Full machine output, the literal command transcripts and the per-heading introduction proof:
`.ufo/waves/round-40/w1/RoutedTimestamps/sweep.txt`.

Date-only headings (no clock token, so no clock comparison possible) and their committer dates — all stated dates are equal
to or earlier than the committer date, i.e. **no date-granularity violation**: SCORECARD 1499, 1526 (2026-10-23 / 10-23), 1589
(2026-10-23 / 10-24), 1857, 1950, 2060 (2026-10-25 / 10-25), 2164, 2241 (2026-10-26 / 10-26); LOG 1329 (2026-10-23 / 10-23),
1359 (2026-10-23 / 10-24). Headings with no stamp at all: SCORECARD 1540, 1547, 2070, 2093, 2103; LOG 1355.

## 3. Findings

**F0 (calibration, passes).** The sweep independently reproduces the five round-35 findings already recorded at LOG.md:1357
("Five round-35 LOG headings carry estimated times that are later than the commits that carry them …"): the same five commit
hashes `7186722b`/`e2f97e6e`/`95684c65`/`199beb97`/`6f92080d` and the same committer times 11:37:49Z/11:52:40Z/11:57:41Z/
12:00:35Z/12:25:23Z, with deltas +131/+440/+139/+265/+37 s. The measurement procedure therefore has a known-positive control.

**F1 (new, SCORECARD).** SCORECARD.md:2209 states `2026-10-26T06:20Z`; its introducing commit `93fddb2c37aed8227b4a0ff2417b10
4e01446a9d` ("round-39: declaration, before receipts and pre-seat controls") was committed 2026-10-26T05:59:31Z — the heading
claims a time **20 min 29 s after** the commit that carries it. No commit in the lane has 06:20 as its committer time (the
round-39 committer times are 05:47:11, 05:59:31, 05:59:37, 05:59:39, 06:00:47, 06:01:19, 06:32:00, 06:35:44, 06:36:27Z).

**F2 (new, LOG).** LOG.md:1457 states `2026-10-26T07:45Z`; introducing commit `eeba342ea06ad0069899b3b8b4bbea6af98df610`
("round-39: measured outcome, current axes and capabilities, LOG entry, final receipts") committed 2026-10-26T06:35:44Z —
**1 h 09 min 16 s after** the commit. Stronger than a future-hour stamp: at the sweep clock 2026-10-26T07:16:39Z the stated
time had still not arrived (lane tip committer 2026-10-26T07:12:34Z), and the heading describes work whose last commit
(`a6ca8171`, round-39 final self-assessment) is at 06:36:27Z. It matches neither UTC nor local (UTC−03:00, 03:35:44) write
time.

**F3 (recurrence, not new).** Five round-35 LOG headings (1333, 1337, 1343, 1347, 1351) remain future-dated; they are already
corrected append-only at LOG.md:1355–1357 with the rule "The commit times are the record; the heading times were estimates
written without reading the clock." The round-39 pair is a recurrence of that same class 3 rounds later, in both files, after
the round-36 UTC-stamp convention was declared at LOG.md:1373.

**F4 (observation, no correction proposed).** LOG.md:1441 states `2026-10-26T05:24:56Z` and its introducing commit `fc931bdb`
is committered 2026-10-26T05:24:56Z — equality to the second. Not future-dated, but a stamp identical to its own commit second
was not written *before* that commit; recorded as a calibration datum for what "stamped at write" can mean in practice.

**F5 (adjacent class, malformed stamp).** LOG.md:1379 heading reads `(2026-10-24T04:4043Z stamped via date -u)` — five digits
in the minute field, not a time. Introducing commit `d39da87a` is committered 2026-10-24T04:41:33Z; read as the intended
04:40:43Z it would be 50 s earlier, so this is a transcription defect, not future-dating. It is unparseable by any
`date`/ISO reader, so the stamp cannot be compared at all without guessing.

Not found: no future-dated heading in SCORECARD.md besides 2209; no date-granularity violation anywhere in the ranges; no
heading whose stated time is later than HEAD's own committer time other than LOG.md:1457 (which exceeds even the tip).

## 4. Exact proposed text (append-only; land verbatim at LOG.md EOF after line 1477, and nothing else changes)

Heading carries no stated time on purpose, so the paragraph cannot repeat the defect it corrects. Its own commit time is its
stamp; the rule sentence says so.

```
## Round 40 — erratum: heading stamps later than their commits (R40-HEADING-TIMES; no stated time in this heading, by design — its commit time is its stamp)

Swept at `f951f288483c1af0cef4afd458488b84cf7a2165` over every SCORECARD.md and LOG.md heading of rounds 35–39 that carries a
clock token (26 headings: 25 parseable stamps, one malformed; per-heading method `git -C <lane> log --format='%h %cI' -S'<heading
text>' -- SCORECARD.md LOG.md`, introducing commit taken as the oldest hit whose blob contains the line and whose parent does
not, committer times converted to UTC; table in `.ufo/waves/round-40/w1/RoutedTimestamps/sweep.txt`), seven headings state a
time later than the committer time of the commit that introduced them — two of them introduced in round 39, and five round-35
LOG headings already corrected at LOG.md:1355 which are restated here so this paragraph names every one. The round-39 pair, both
in that round's record:
SCORECARD.md:2209 `## Round 39 — declaration (2026-10-26T06:20Z, base `0eff65b21bb81195ee06c96a83afbd7a07e52eef`, before any seat)` states 2026-10-26T06:20Z and
is introduced by `93fddb2c37aed8227b4a0ff2417b104e01446a9d`, committed 2026-10-26T05:59:31Z (+20 min 29 s); LOG.md:1457
`## Round 39 — hyaku run 8, 2026-10-26T07:45Z` states 2026-10-26T07:45Z and is introduced by
`eeba342ea06ad0069899b3b8b4bbea6af98df610`, committed 2026-10-26T06:35:44Z (+1 h 09 min 16 s) — a time that had not yet elapsed
anywhere in the lane when this erratum was swept (tip committer 2026-10-26T07:12:34Z, sweep clock 2026-10-26T07:16:39Z); and the
five round-35 headings, already corrected at LOG.md:1355, remain future-dated: LOG.md:1333 "~11:40Z" in `7186722b8eba243439c6724766bdae2ef13c595c` committed 11:37:49Z (+2 min 11 s); LOG.md:1337
"~12:00Z" in `e2f97e6e4beaadda8e1d5ae7bd08baa0e82d61e0` committed 11:52:40Z (+7 min 20 s); LOG.md:1343 "~12:00Z" in
`95684c65a9f90a5c3d2a47d764657e72000f3fc6` committed 11:57:41Z (+2 min 19 s); LOG.md:1347 "~12:05Z" in
`199beb97d0c30507d732a0ebb4dba69adb973596` committed 12:00:35Z (+4 min 25 s); LOG.md:1351 "12:26Z" in
`6f92080dd2e85400bc86f3f94654b731ce69f046` committed 12:25:23Z (+37 s). The rule, and the reason no heading above is rewritten:
the commit time is the authority — the committer time of the introducing commit is when the text became reachable in history,
the heading stamp is only a recollection of when the seat believed it was writing, so where the two disagree the committer time
is the record and the stated time may not be cited as evidence of ordering, of being "before any seat", or of being "stamped at
write"; this is the same rule the round-35 erratum (LOG.md:1355–1357) already applied, and the recurrence in round 39 shows the
rule needs restating rather than re-deriving.

Adjacent class, same family, not a future-dating: LOG.md:1379 `## Round 36 — wave 2, measured outcome, budget-forced landing
(2026-10-24T04:4043Z stamped via date -u)` carries `04:4043Z`, which is not a time (five digits in the minute field); its
introducing commit `d39da87a1647cca7bf36a1d171ee905e73ee97b0` is committed 2026-10-24T04:41:33Z, so the intended 04:40:43Z lies
50 s earlier and the stamp is unparseable rather than future-dated; the committer time is the record there too.
```

Optional single-line pointer, if the closure wants the SCORECARD reader to find it without reading the LOG (append after
SCORECARD.md:2241, changes nothing above it):

```
Erratum: the round-39 declaration heading above states 2026-10-26T06:20Z but its commit `93fddb2c` is committered
2026-10-26T05:59:31Z; the commit time is the authority (R40-HEADING-TIMES, LOG entry).
```

Notes for landing: the draft is inside a fenced block only for verbatim copying — when it lands in LOG.md it must be plain
prose with a `##` heading at column 0, and the step is one append after the current EOF (LOG.md:1477), which no later section
contradicts. The heading deliberately states no date or clock time, so nothing in this erratum can itself become a
future-dated stamp; its stamp is the commit that lands it.

## 5. What I did not do

- Did not run any git mutation: no `add`/`commit`/`stash`/`checkout`/`reset`/`push`, no `git gc`, no jj command; only
  `log`, `show`, `rev-parse`, `diff --quiet`, `sha256sum` reads. No scratch clone was needed (all evidence is read-only
  history), so no `/fast/scratch/hyaku/tsukuroi-r40/RoutedTimestamps/` directory was created or removed; `TMPDIR` untouched.
- Did not sweep rounds 1–34 (out of the item's scope; the round-35 erratum itself records that the round-34 class was routed by
  the round-34 spot-check §5 item 5).
- Did not re-run, decorate or re-derive any counter, census or gate; this item is historical-record analysis only.
- Did not attempt to reconstruct *why* the two round-39 stamps were off (e.g. whether 06:20Z/07:45Z were expected-finish
  estimates); the lane records no clock reading for them, so any explanation would be inference. Not claimed.

## 6. Touched surfaces

- Created: `.ufo/waves/round-40/w1/RoutedTimestamps.md` (this report) and
  `.ufo/waves/round-40/w1/RoutedTimestamps/sweep.txt` (7 952 B receipt: literals, introduction proof, 26-row table, negative
  results).
- Everything else in the lane and on the host: read only. No package installed or upgraded (no tool was needed).
