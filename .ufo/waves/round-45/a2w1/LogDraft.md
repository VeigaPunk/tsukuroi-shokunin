VERDICT: draft

# X-8 — round-45 `LOG.md` entry (exact Markdown, register of the round-44 entry)

Seat LogDraft (leaf). Lane `tsukuroi-shokunin`, wave `a2w1`. Nothing tracked was written: the only new file is this
report, and the entry below is **draft text for the L1 to land**, not a landed entry.

Written at lane tip `3c42f556f8301500aa30409e05a45dad5923872d` with the measured revision
`18389f44cf6ce414d7be205998b29c79fb0b490c`. Every number below is copied from a receipt I opened this seat; every
number I could not read from a receipt is written `<PENDING: …>` and listed in the placeholder ledger (§2), with the
path that will fill it. I ran no counter, no census and no selftest (§4).

Register followed: `LOG.md:1615-1624` (round 44) for shape and length, `LOG.md:1588-1614` (round 43) for the
D-item / considerthese / adjacency sentence order, and `LOG.md:1606` for the `Re-verification of predecessor pins: …`
phrasing that routed defect D10 asks for.

## 1. Draft entry (exact Markdown; land directly under the round-44 entry in `LOG.md`)

```markdown
## Round 45 — 2026-10-27 (hyaku run 9; L1 TsukuroiR45a2)

Motivating evidence: the round-44 closure (`corpus/lessons/round-44-verifier-spotcheck.md` §2, §6) routed ten defects D1-D10 and four still-open items; the C1
line is the R41-CENSUS-PIPEFAIL-692 class (five production readers that keep the first line of a captured output
inside an assignment, which under `set -euo pipefail` kills the census with exit 141 once the output passes the pipe buffer),
routed since round 42; the C2 line grounds the three `[inference]` marks of the round-44 entry (SR7 replace caller, SR8 `memparse`,
SR9 stop signal) in pinned source. Attempt 1 (L1 `TsukuroiR45`) died with its orchestrator session at 2026-10-26 23:57:36
-03 while its single v2 wave `w1` was filling: 66 seats dispatched, 14 spawned, 0 outputs recovered (`.ufo/waves/round-45/w1-results.json`), nothing
in `w1/` citable; orchestrator salvage `5b3029bf`. Attempt 2 re-dispatched the same 66 items as wave `a2w1` with the C2
counter's two counted-wave literals rebound to `a2w1`/`a2r1` (`057c1804`; predicate, kill rule, target, seats and roles
unchanged; the 30-control battery re-run gives field-identical results, `should_fail_accepted 0`). Claims (base `5bbd5ff588120fd8e7c744695351a6978b4241c1`, the lane tip at
round start; frozen and declared `ea6e0ee38d8066663bb0871b53bade14441eb304`): C1 operability — the five production readers that keep the first line of a
captured output (`probe_systemd` `state` and the timer `Result` `r`, `probe_drivers` `driver`, `probe_journal` `t_word` and the timer `ActiveState` `r`) stop using `printf '%s\n' "$CAP_OUT" | head -n1`
inside an assignment and take the first line by parameter expansion; six selftest cases labelled `(R45-C1)` put the
deciding first line before ~150 KB of padding and the sixth drives the foreign-baseline lookup past the pipe
buffer with the deciding row last; counter `tools/score-census-readers-r45.py` (sha256 `fe0e31e2…3250bd50`), predicate `lexical_hits == 0 and sites_found == 5 and equiv_ok == 5 and selftest_pass == 1 and selftest_r45 >= 6 and revert_killed == 6 and adjacency_ok == 1`. C2 depth (sourced, S246-S249 opened
this round) — new entry `corpus/knowledge/btrfs-scrub-grounding-r45.md` rows GR1 (`memparse` as the `scrub_speed_max` write parser: base-0 radix, `K`..`E` suffix either case,
1024 per step, overflow to `ULLONG_MAX`, trailing text `EINVAL`), GR2 (device replace runs `btrfs_scrub_dev` with `is_dev_replace` true, and a
non-replace scrub is refused with `EINPROGRESS` while a replace is ongoing), GR3 (`systemctl stop` of the packaged scrub service under
systemd v262: `KillSignal=SIGINT`, `SIGCONT`, `SIGKILL` after `TimeoutStopSec=`, 5 s on this host); an appended `## Round-45` section in the round-44 entry;
SOURCES rows S246-S249 plus `used-by` edits on S237, S242, S243, S244; counter `tools/check-scrub-grounding-r45.py` (sha256 `a1eb402d…d011331`), predicate `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1`, row
verdicts from the counted seats `C2RevGR<n>`/`C2CritGR<n>` in `a2w1` with residual `C2ResGR<n>` in `a2r1`. Controls before any seat (`controls/battery-summary-c1.jsonl`,
`controls-a2/battery-summary-c2.jsonl`): C1 K0-K7 and K10 FAIL, K8 (candidate) and K9 (`sed -n 1p` full-read alternative) PASS; C2 K0-K29 with K3 (forged
records), K19 (`partly` + bound residual `holds`) and K26 (JSON-string outputs) PASS and the rest FAIL, K3 the standing
limit; `should_fail_accepted 0` and `control_accepted 1` in both summaries (the C1 battery is attempt-1's, valid because the C1 counter and its
controls are unchanged). Gates at base (`.ufo/waves/round-45/before/`): adjacency FAIL (IN-109), self-assessment FAIL 1 mismatch (65
lessons), census selftest PASS 148/148, sources census exit 0, C2 `rows 0`. Waves: `a2w1` 66 seats `<PENDING: outputs, dead seats, misroot/incident accounting>`; residual `a2r1`
`<PENDING: seats>`; attempt-1 `w1` 14/66 spawned, 0 outputs, its records not evidence. Measured: C1 PASS at `18389f44` on all seven
conjuncts — `lexical_hits 0`, `sites_found 5`, `equiv_ok 5`, `selftest_pass 1`, `selftest_r45 6`, `revert_killed 6`, `adjacency_ok 1`, selftest line `TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)` (148 → 154), census sha256 `237b21c9…b5fcdc`, two runs
identical in every leg but the per-run `seed` (`a2w1/C1ExecRerun/c1-after-1.jsonl` at 03:28:44Z, `c1-after-2.jsonl` at 03:34:02Z). C2 `<PENDING: rows / quotes_ok / props_ok / host_ok / sources_ok / verdicts_ok / novelty_base_hits / pointer_ok at <INTEGRATION-REV>>`; counted row verdicts
read so far: GR1 `holds` (`C2CritGR1`), GR2 `partly` (`C2CritGR2`), GR3 `holds` (`C2CritGR3` and `C2RevGR3`), `C2RevGR1`/`C2RevGR2` `<PENDING>`; the `partly` row needs its
bound `C2ResGR2` `holds` before `verdicts_ok` can reach 3. Wave findings integrated: GR2's Host reading is false in its deciding
clause — replace state *is* readable unprivileged (`/sys/fs/btrfs/<uuid>/exclusive_operation`, `devinfo/<devid>/replace_target`, S243 sysfs.c:1302, 2019) and here reads
`none`/`0`, so the row is narrowed to "scrub progress and the record stay unprivileged-unreadable" (`a2w1/C2ExecHostRecheck.md` §3,
§6); GR2's "any device of that filesystem" is narrowed to the replace source devid and the existing-context branch
(`a2w1/C2ExecKernelGR2.md` §1, `a2w1/C2RevEntryWhole.md` finding 2); GR3's "if processes remain once TimeoutStopSec has passed" regains systemd's
condition (`SendSIGKILL=yes`, capture.txt:3) and SIGINT is attributed to S244, not S248 — S248 v262 does not contain `SIGINT` at
all (`a2w1/C2ExecLiveSources.md` §6, `a2w1/C2RevEntryWhole.md` finding 3); three citation registrations are short of the quotes they carry — S242 must gain
`3079-3081` and S237 `412-444`, `1512-1550`, and the `systemd.kill.xml` SIGCONT quote must cite `114-115` (`a2w1/C2ExecQuotes.md` F1-F3); the entry's QUALITY block
does not evaluate QUALITY 14 (`a2w1/C2RevEntryWhole.md` finding 1); three of the five C1 case labels do not independently pin
CR/whitespace normalization and case 6 detects early-exit-on-large-input forms only (`a2w1/C1CritCases.md`); the C1 kill-rule cell
needs its universe and its "shape" definition fixed (`a2w1/C1RevKillRules.md` §Actionable gaps); the C2 counter is beaten by a
Unicode-lookalike contradiction, a duplicate same-name result under another role, a sibling `note` key, prose
contradiction and a cross-row contradiction (`a2w1/C2MutBinding.md` survivors), and its host leg scores citation presence, not
truth — which is why the GR2 refutation above is a wave finding and not a counter FAIL (`tools/check-scrub-grounding-r45.py:27`). `<PENDING: each item above must be applied or
explicitly refused in the integration commit — every source report is advisory and none edited lane content, so the
list is "integrated" only after that check>`. Routed defects
D1-D10: D1 repaired (`ea6e0ee3` IN-109 `found_line` 2468 → 2582, adjacency gate PASS at `18389f44`, `inbound_total 114`, `live_object_match 10`); D3 repaired
(`18389f44` appends the round-44 gate status and the grounding pointer); D7 repaired (`ea6e0ee3` commits the round-44 gz
receipts and their `.ready` markers); D8 drafted, not landed (`a2w1/SrcGateNew.md` §3 reject rows, re-checked against live text); D9
open with a plan — staged ids collide 30 times with the 183-id absent-defect register (S242, S243, S244, S249
inside the required subset) and 50 times with the lane's 249-row registry, so any landing renumbers to S250+
(`a2w1/AsmGate.md`, `a2w1/SrcGateNew.md` finding 3); D2, D5 and D6 are open at the implementation and still open at tip `3c42f556` (`SKILL.md:4225` still
says `memparse` takes `K/M/G` only and treats trailing whitespace as skipped; no round-44 report section in either
repository); D4 is disposed in the declaration's own prose — the round takes the stale round-44 row's item (3) as
C1 and replaces its items (1)-(2) with C2, and no new `planned (next round)` bullet is written (`SCORECARD.md:2858-2859` at `ea6e0ee3`); D10 is repaired by
the freshness line below. Re-verification of predecessor pins (D10, 2026-10-27): S237 (btrfs-progs v7.1 `cmds/scrub.c`),
S242 (`fs/btrfs/scrub.c`), S243 (`fs/btrfs/sysfs.c`) and S244 (`btrfs-scrub@.timer`, `btrfs-scrub@.service`, `PKGBUILD` at packaging 7.1-1) re-fetched byte-identical (`cmp` 6/6
against the round-42/round-44 frozen copies: `48df2e2f…0801`, `f347931b…a5b8`, `ce146120…1c43`, `9a0b6cc2…f8ad`/`eaa7af92…0252`/`3b803e8b…ce98`) and the tags still peel to
`4ab0e80b…ba8b`, `a2de78ee…bea6` and `0c0a4d77…3e0e` (`a2w1/SrcGateReopen/`); this round's own S246-S249 re-fetched live byte-identical to `SHA256SUMS` (5/5) and to
the commit-pinned bytes, the tag peels `a2de78ee…bea6` (Linux v7.2.11) and `8cc40e0c…b492` (systemd v262) unmoved (`a2w1/C2ExecLiveSources.md` §1-§4, `a2w1/SrcGateNew.md`
§1); the S249 host capture re-ran to the same nine lines with only the `captured` timestamp differing (75 minutes
later, digest `f5958a83…1e70` frozen) (`a2w1/C2ExecHostRecheck.md` §1); the sources census re-ran `validate` at exit 0, `ok`, 40 W04 unchanged over
249 rows against 245 at base, and the `used-by` cell is the only cell changed on those four rows (`a2w1/SrcGateReopen.md` §2, S-2).
Adjacency: the round repairs its round-44 harm with the D1 repin at the declaration, the C1 counter carries the
adjacency gate as a kill rule, and a sibling sweep found no pin moved (`a2w1/AdjPins.md`; `check-adjacency-anchors.py --revision 18389f44` exit 0, `status PASS`, `findings []`). Landed:
`ea6e0ee3` declaration, frozen counters, control batteries, frozen sources and the D1/D7 repairs; `18389f44` C1 readers plus
six `(R45-C1)` cases and the C2 entry, SOURCES rows and r44 append; `5b3029bf` attempt-1 salvage; `057c1804` attempt-2 rebinding;
`3c42f556` `a2w1` spec, generator and validated dispatch; `<PENDING: a2w1 integration>` wave-1 integration; `<PENDING: a2r1 dispatch / integration>` residual; `<PENDING: measured outcome commit>` measured
outcome and axes/capabilities tables; this entry with the outcome and QUALITY `<PENDING>`. considerthese: no proposal
from `considerthese/2026-10-26.md` was taken this round (proposals 4 and 5 were taken in rounds 42 and 43); burst-aware reading, the
counter-attack scoreboard and the seat-harm incident log stay open, and this round is itself evidence for the
third — attempt 1 lost 52 never-spawned seats and 14 killed seats to one orchestrator session exit, recorded in
`w1-results.json` rather than in a seat report. Assimilation: none — the staged append is not a safe append against the
present registry (30 id collisions against the 183-id absent-defect register, 50 against the lane's 249-row `corpus/SOURCES.md`,
with S242-S249 inside the required subset), staged S230 is rejected for intake as an own-work entry with no
re-openable locator, and no examined staged row supplies evidence for this round's three surfaces (`a2w1/AsmGate.md`); a
superseding append-only gate-registry table is drafted and proved only in a scratch clone (`a2w1/RegistryDraft.md`). Lesson `<PENDING: corpus/lessons/round-45.md>`;
report `<PENDING: .ufo/reports/round-45/tsukuroi.md>` (fleet repo).
```

## 2. Placeholder ledger — what each `<PENDING: …>` needs, and from where

| # | Placeholder | Filled by | Why I could not read it |
|---|---|---|---|
| P1 | `a2w1` outputs, dead seats, misroot/incident accounting | `.ufo/waves/round-45/a2w1-results.json` (does not exist yet; `ls .ufo/waves/round-45/` shows only `w1-results.json`) | the wave is still running; attempt-1's `w1/` holds 6 seat dirs and `swarm-registry.json`, no reports |
| P2 | residual `a2r1` seats | the L1's residual dispatch, gated on a counted `partly`: only GR2 is `partly` today (`a2w1/C2CritGR2.md:1`) | not dispatched; `SCORECARD.md:2898-2902` names the wave, no spec file exists |
| P3 | C2 counter readout (`rows`, `quotes_ok`, `props_ok`, `host_ok`, `sources_ok`, `verdicts_ok`, `novelty_base_hits`, `pointer_ok`) at the integration revision | `python3 tools/check-scrub-grounding-r45.py --lane <lane> --revision <INTEGRATION-REV>` (~2 s), receipt to `.ufo/waves/round-45/after/` | a mid-wave readout cannot be honest: `verdicts_ok` needs `C2RevGR1`/`C2RevGR2` (absent) and a bound `C2ResGR2` for the `partly` row (`a2r1`) |
| P4 | `C2RevGR1`, `C2RevGR2` counted verdicts | those seats' reports in `a2w1/` (`C2RevGR3.md` is the only counted reviewer landed) | seats live |
| P5 | integration / residual / measured-outcome commit ids | the L1's commits after this wave | the only commits that exist are `ea6e0ee3`, `18389f44`, `5b3029bf`, `057c1804`, `3c42f556` (`git log --format='%h %ad %s' -18`) |
| P6 | `corpus/lessons/round-45.md` | the round's lesson commit | `ls corpus/lessons/` ends at `round-44-verifier-spotcheck.md` / `round-44.md` |
| P7 | the fleet-repo report `.ufo/reports/round-45/tsukuroi.md` | the closure (fleet repo, not this lane) | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-45/` holds eight sibling-lane files and no `tsukuroi.md` |
| P8 | traceability ref (no traceability is claimed — see §3 L-2) | a round-end `check-self-assessment.py` run (D5) | not run this wave |
| P9 | QUALITY `<n>` | the verifier at closure | not assigned yet |
| P10 | the exact GR2 proposition sentence as landed | the entry text at the integration revision | the draft's GR2 clause mirrors the frozen declaration; the wave narrows it (replace source devid, existing-context branch, `exclusive_operation` readable), so the LOG sentence must be re-read from the landed row, not copied from `SCORECARD.md:2864` |
| P11 | the census selftest case count if integration adds cases | the C1 counter receipt at the integration revision | 154 is the count at `18389f44` only |

Deliberately **not** written as a bare number anywhere in the entry: seat counts for `a2w1` outputs, any C2 counter
conjunct, the residual seat count, and the round's QUALITY. The three figures I did print (`66` dispatch items, `14`
spawned / `0` outputs for attempt 1, `154` selftest cases) are read from `a2w1-spec.json` (`items` length 66),
`w1-results.json` (`seats 66`, `spawned 14`, `outputs_recovered 0`) and
`a2w1/C1ExecRerun/c1-after-1.jsonl` (`selftest_line`).

## 3. Findings (this seat)

**L-1 — the entry must state attempt 1 as uncitable, not merely mention it.** `w1-results.json` records
`{"seats": 66, "spawned": 14, "outputs_recovered": 0, "settled_by": "orchestrator session exit (no seat live)"}`, and
`w1/` contains six seat directories plus `swarm-registry.json` with no reports. A later reader who finds six attempt-1
directories under `w1/` must be told by the entry that they carry no evidence; the draft says so in the motivating
sentence and again in the waves sentence.

**L-2 — no traceability number is claimed.** `ScoutR44Defects.md` D5 records the self-assessment counter as not re-run
and no tip receipt, and this wave has no receipt for it either (no `a2w1` seat ran it; `grep -ri traceab
corpus/lessons/round-44-verifier-spotcheck.md` is empty, so nothing in the routed set asks for a figure). The draft
therefore prints no traceability number rather than a stale one; if the L1 wants one, it must come from a round-end
`check-self-assessment.py` run, which is still the open half of D5.

**L-3 — the C2 counter cannot catch the GR2 host refutation, so the LOG must not rest C2 on the counter alone.** The
counter's host leg is documented as "the row's host block names existing, non-empty `capture.txt` lines"
(`tools/check-scrub-grounding-r45.py:27`, scored at `:360-382`). `a2w1/C2ExecHostRecheck.md` §3 shows the GR2 block names
real lines while its conclusion ("no replace or scrub state is observable to this caller") is false: both
`exclusive_operation` and `devinfo/<devid>/replace_target` are world-readable (S243 `sysfs.c:1302`, `:2019`) and read
`none` / `0` to uid 1000 with `CapEff=0`. Any C2 PASS readout will therefore be consistent with a false sentence unless
GR2 is narrowed at integration; the draft records the refutation as a wave finding and does not print a C2 verdict.

**L-4 — the freshness line cannot come from `SrcGateReopen.md` alone.** That seat's §5 draft deliberately names only the
four predecessor rows and says in its own note that "S246-S249 are *opened* this round (not re-verifications) and their
live re-fetch belongs to C2ExecLiveSources; S245 and the S249 host capture re-run belong to C2ExecHostRecheck". Routed
defect D10 asks for all three arms (S246-S248 re-fetch, S237/S242-S244 re-open, host capture re-run), so the draft merges
them into one `Re-verification of predecessor pins (D10, 2026-10-27)` sentence and cites three receipt dirs. Landing
`SrcGateReopen.md` §5 verbatim would have left D10 half-repaired.

**L-5 — D2/D5/D6 are still open, and the entry says so.** `SKILL.md:4225` (checked at tip `3c42f556`) still reads
`writes parse with memparse (K/M/G suffixes, trailing whitespace skipped, else -EINVAL)`, which the round's own GR1
contradicts on both counts (`K`..`E`, and trailing text is `EINVAL` rather than skipped whitespace). The draft's D-line
names D2, D5 and D6 open rather than folding them into a "repaired" list; the entry may not claim them.

**L-6 — the S246-S249 registration gaps are the one thing the entry must not paper over with a row count.** The draft
cites the counter's conjuncts but the wave found three quote/registration mismatches (`a2w1/C2ExecQuotes.md` F1-F3:
S242 `scrub.c:3081` and S237 `cmds/scrub.c:421/439/1546` outside the declared ranges; `systemd.kill.xml` quote stopping at
`:114` where the SIGCONT object is on `:115`). Integration must widen those ranges or the entry's `source:` mapping is
weaker than the quotes it presents.

**L-7 — two wording points resolved against source rather than guessed.** (a) D4 is disposed by prose, not by a new
planned-row bullet: `SCORECARD.md:2858-2859` at `ea6e0ee3` reads "The planned row of round 44 was stale (D4); this round
takes its item (3) as C1 and replaces its items (1)-(2) (landed or failed in round 44) with C2", and no
`planned (next round)` bullet follows the round-45 declaration (the last four such bullets are at `:2535`, `:2640`,
`:2739`, `:2840`). The entry therefore describes a disposition, not a rewritten planned row — an earlier wording of mine
("replaces the stale row in this commit") claimed more than that line says. (b) The attempt-1 salvage/rebinding order in
the landed list (`5b3029bf` then `057c1804`) is the commit order from `git log --format='%h %ad %s'`; the entry states
order only, not authorship.

**L-8 — heading style is a choice the L1 should make knowingly.** The draft uses the round-44 shape
(`## Round 45 — 2026-10-27 (hyaku run 9; L1 TsukuroiR45a2)`), i.e. a date. Rounds 41-43 instead wrote
`(stamp: the commit that lands this entry)` after the round-40 erratum about headings stamped later than their commits
(`LOG.md:1479`). The date is safe if the entry lands on 2026-10-27; if the wave runs past midnight, take the round-43
form instead of editing the date.

## 4. What I ran, and what I did not do

Read-only work only: `git log --format='%h %ad %s' -18`, `git show 18389f44:<paths>` (entry front matter, r44 append,
`SKILL.md`), `python3` parses of `.ufo/waves/round-45/{before/c2-before.jsonl,controls/battery-summary-c1.jsonl,
controls-a2/battery-summary-c2.jsonl,a2w1/C1ExecRerun/c1-after-{1,2}.jsonl,w1-results.json,a2w1-spec.json}`, and reads of
the `a2w1/*.md` seat reports named above. No counter, census or selftest was run by this seat (the C1 readouts are two
other seats' `run-receipt.py` receipts; the C2 predicate has no readout at the implementation revision anywhere in
`.ufo/waves/round-45/` — I searched every `*.jsonl` in `a2w1/` for `verdicts_ok` and found only the round-43/round-44
counters' receipts under `RevGatesAll/` and the mutant receipts under `C2MutBinding/`).

I did not edit `LOG.md`, `SCORECARD.md` or any other tracked lane file; did not run any counter; did not fetch any URL;
did not query the host; did not create a scratch directory (an empty seat scratch was never needed — no fixture was
built and nothing was written outside this report); installed or upgraded no tool.

Scratch: unused, so nothing to remove.

Report: .ufo/waves/round-45/a2w1/LogDraft.md
