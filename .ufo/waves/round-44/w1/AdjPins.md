VERDICT: supports (round-44 census insertions mapped byte-identical base→impl for all eight hunks; zero sibling pins into `btrfs-scrub-record-r43.md`; 47 live sibling pin rows inventoried — 13 accurate at base and moved by R44, the rest already stale at base (restated with both coordinate sets); both round-43 handoffs restated)

# AdjPins — F-9 moved sibling pins, round 44 wave w1

Seat AdjPins (L2, leaf, read-only). Base `98020ece0674e0b569ee23aed10ffbee355b248e` ("B"), implementation `7e081698d4fc3c4ea944884fd093058de9909de1` ("I"). Lane HEAD at sweep time: `7e081698` (I). Did not run any counter, the census, or the selftest; did not touch the lane, any sibling or the host. Scratch `/fast/scratch/hyaku/tsukuroi-r44/AdjPins/` (copies of B/I file bytes via `git show`), removed at the end. Receipts: `.ufo/waves/round-44/w1/AdjPins/` (`raw.json` full sibling grep hits, `strict.json` parsed pins, `ranges.json` base→impl range map, `hits.txt` first sweep).

## 0. Method (all read-only)

```sh
for r in /home/vgpnk/Projects/shokunin/*-shokunin; do [ $(basename $r) = tsukuroi-shokunin ] && continue
  git -C $r grep -n -I -E 'tsukuroi-census\.sh|btrfs-scrub-record-r43' -- .; done   # 3175 hits
# parse hits with a strict pin grammar: tsukuroi-census.sh:<n> / :<a>-<b> (comma/slash lists allowed)
# -> 267 strict pins + 53 continuation candidates (tabulated below)
git -C tsukuroi-shokunin diff -U0 98020ece 7e081698 -- tools/tsukuroi-census.sh | grep '^@@'
git -C tsukuroi-shokunin show <rev>:tools/tsukuroi-census.sh | sed -n <range>p   # B and I, diffed
```

The sweep used the broad pattern (any mention of the file name, not only `:<n>`), so pins written as `tsukuroi-census.sh:<n>`, `:<a>-<b>`, `:<a>,<b>-<c>` or `:<a>/<b>/…` are all inside the 3175 hits. 53 continuation candidates (bare `:NNN` after a backticked path, or revision-qualified) are listed in section 5.

## 1. Hunk map B→I of `tools/tsukuroi-census.sh`

`git diff -U0 98020ece 7e081698 -- tools/tsukuroi-census.sh | grep '^@@'`:

```
@@ -383,0 +384,28 @@     # 28 header lines after B:382 → I:384-411
@@ -408,0 +437,2 @@     # 2 after B:407 → I:437-438
@@ -463,0 +494,2 @@     # 2 after B:462 → I:494-495
@@ -568 +600,2 @@        # usage line B:568 split into I:600-601 (SCRUB line added)
@@ -1932,0 +1966,76 @@   # probe_scrub_record + storage-arm block after B:1931 → I:1966-2041
@@ -2172,0 +2282,2 @@   # 2 after B:2171 → I:2282-2283
@@ -3115,0 +3227,61 @@  # selftest near-end block after B:3114 → I:3227-3287
@@ -3201,0 +3374,4 @@   # 4 in main() after B:3200 → I:3374-3377
```

Net shift by region (each verified by `diff <(sed -n a,bp base) <(sed -n c,dp impl)` on flanking/identical lines):

| base range | I range | shift |
|---|---|---|
| 1-382 | 1-382 | 0 |
| 383-407 | 411-435 | +28 |
| 408-462 | 438-492 | +30 |
| 463-567 | 495-599 | +32 |
| 568 (one line, split) | 600-601 | content replaced (1 → 2 lines) |
| 569-1931 | 602-1964 | +33 |
| 1932-2171 | 2042-2281 | +109 |
| 2172-3114 | 2283-3225 | +111 |
| 3115-3200 | 3287-3372 | +172 |
| 3201-3221 | 3377-3397 | +176 (B 3221 → I 3397) |

Mapping function used below: `f(L) = L` (L≤382), `L+28` (383..407), `L+30` (408..462), `L+32` (463..567), `600/601` (L=568), `L+33` (569..1931), `L+109` (1932..2171), `L+111` (2172..3114), `L+172` (3115..3200), `L+176` (3201..3221).

## 2. Sibling pins into `tools/tsukuroi-census.sh`

`Verdict` column: **moved** = pinned content accurate at B and shifted by R44; **stale@B** = cited range does not hold the cited subject at B (pre-existing drift; I-range restated for completeness); **frozen** = the pin names the old blob `084951be…@165307fe` (977-line census) and is unaffected by R44 (historical records). "I range holding it" gives the coordinate that holds the same bytes/subject at I.

### 2a. Live pins (resolve against the current census)

| # | repo | file:line | pinned range (B) | B content at the range | I range holding it | verdict |
|---|---|---|---|---|---|---|
| 1 | mori | `PROVINCE.md:287` | `:376,1100-1115` | B:376 = btrfs devid comment (not the pressure path); B:1100-1115 = memory-pressure arm header `probe_mem_arm` (B:1102-1111) + first body lines | `:376` unchanged (subject: `PRESSURE_FILE` default B:401 → **I:429**; read path B:1196-1207 → **I:1229-1240**); `:1100-1115` → **I:1133-1148** | stale@B (376), moved (1100-1115) |
| 2 | mori | `.ufo/waves/round-42/assimilation/validate/PROVINCE.md:287` | `:376,1100-1115` | same | same as #1 | stale@B/moved |
| 3 | mori | `.ufo/waves/round-43/assimilation/validate/PROVINCE.md:287` | `:376,1100-1115` | same | same as #1 | stale@B/moved |
| 4 | mori | `.ufo/waves/round-24/w1/ConnectSiblingPsi.md:43,:44,:136` | `:376` / `:1100-1115` / `:376,1100-1115` | same as #1 | same as #1 | stale@B/moved |
| 5 | mori | `.ufo/waves/round-24/w1/DraftProvinceFrontier.md:103,:150,:289` | `:376` / `:376` / `:376` (+`:1100-1115` in prose) | same | same as #1 | stale@B/moved |
| 6 | mori | `.ufo/waves/round-24/w2/CriticHarmAxes.md:158,:180,:209` | `:376` / `:376,1100-1115` / `:370-385,1100-1115` | B:370-385 = btrfs sysfs privilege comment (not pressure); rest same | B:370-382 unchanged, B:383-385 → **I:411-413**; rest as #1 | stale@B/moved |
| 7 | mori | `.ufo/waves/round-24/w2/ReviewSkillProvince.md:175` | `:376` | same | same as #1 | stale@B |
| 8 | mori | `.ufo/waves/round-27/w1/CriticC1Novelty.md:68` | `:1081` | B:1081 = `if [ "$smi" = ok ]…` (nvidia smi check); `memory.oom.group` reads are B:1177/1228 | `:1081` → **I:1114** (mechanical); subject → **I:1210/1261** | stale@B |
| 9 | mori | `.ufo/waves/round-47/w1/ConnSiblings.md:98` | `:400` | B:400 = env-override comment list; `avg300` read is B:1196-1207 | `:400` → **I:428**; subject → **I:1229-1240** | stale@B |
| 10 | mori | `.ufo/waves/round-17/build/OverlapTsukuroi.md:100` | `:2659` | B:2659 = `r8oom` wc-l count check (update-safety plane) | `:2659` → **I:2770** | moved |
| 11 | kama | `.ufo/waves/round-16/build/advice/ConnectTsukuroi.md:20,:21` | `:624` / `:355-357` | B:624 = blank (between functions); `-Qm` foreign probe is B:716/720/723; `pacman -Qo /` root-arm precedent is B:434 (comment)/835 (code) | `:624` → **I:657**; `:355-357` unchanged; subject → **I:749/753/756** and **I:464/868** | stale@B |
| 12 | kama | `.ufo/waves/round-17/build/advice/ConnectTsukuroi.md:29,:30` | `:620` / `:355-356` | B:620 = `count_pci_nvidia` line; B:355-356 = btrfs sysfs comment | `:620` → **I:653**; `:355-356` unchanged; subject → I:749/753/756 | stale@B |
| 13 | kama | `.ufo/waves/round-19/build/advice/TsukuroiOverlap.md:15` | `:696-717` | B:696-717 = `foreign_rc` block; `pins=none holds=pacman glibc` appears nowhere in census (B or I) — it lives in `SKILL.md:397-399` | `:696-717` → **I:729-750** | stale@B (subject absent from census) |
| 14 | kama | `.ufo/waves/round-20/build/advice/ConnectTsukuroi.md:8,:10` (+ `build/out/…` copy) | `:594-613` / `:1713-1716` | B:594-613 = awk-map end/`}` fragment; `pacman -Qkk` sample loop is B:684/689/700; cleanup trap/mktemp pattern is B:1936 | `:594-613` → **I:627-646**; `:1713-1716` → **I:1746-1749**; subject → **I:717/722/733** and **I:2045** | stale@B |
| 15 | kagi | `.ufo/waves/round-24/build/ConnSiblingLedgers.md:11` (+ round-27 sandbox copy) | `:312-328` | B:312-328 = whole-gate live-run timing comments; "fixture overrides for each host command/path" live at B:393-430 | `:312-328` unchanged (≤382); subject → **I:421-458** | stale@B |
| 16 | kagi | `.ufo/waves/round-27/build/ConnTsukuroi.md:21,:23,:24,:42` | `:384` / `:1410-1429` / `:277` / `:1609-1617` | B:384 = read-only-guarantee comment; B:1410-1429 = `cap`/t-word block; B:277 = PROVINCE.md comment; B:1609-1617 = INERT comment + `cap "$PACMAN" -Qu`. Subjects: `VERCMP` default B:466; `version_join` B:1523/1535; `REQUIRES-PREP` verdict B:1546-1550; `diff_unclassifiable` B:1772 | `:384` → **I:412**; `:1410-1429` → **I:1443-1462**; `:277` → I:277; `:1609-1617` → **I:1642-1650**; subjects → I:498, I:1556/1568, I:1579-1583, I:1805 | stale@B |
| 17 | kagi | `.ufo/waves/round-28/build/ConnTsukuroi.md:55,:56` | `:384,:1609-1610,:1631-1632` / `:1411-1430` | as #16; B:1631-1632 = `sup_rc` block | `:1631-1632` → **I:1664-1665**; `:1411-1430` → **I:1444-1463** | stale@B |
| 18 | chousa | `.ufo/waves/round-33/w1/ConnectorSiblings33.md:20` | `:566-575` | B:566-575 = usage text (no class_counts); `class_counts()` is B:625 | `:566-575` → **I:598-607**; subject → **I:658** | stale@B |
| 19 | chousa | `.ufo/waves/round-41/w1/ConnectorSiblingScan.md:35` | `:548` | B:548 = comment on `-Qm` fold; `have() { command -v…}` is B:587 | `:548` → **I:580**; subject → **I:620** | stale@B |
| 20 | kotoba | `.ufo/waves/round-53/build/ScoutPriorArtLinters.md:170` | `:336` | B:336 = DRIFT pacnew-plane comment; `verify_surfaces` appears nowhere in census (B or I) | `:336` unchanged | stale@B (subject absent) |
| 21 | kumitate | `.ufo/waves/round-44/falsify/ConnAdjacency.md:16` | `:483` | B:483 = `R6_FOREIGN_CLASSES` data (elephant-bluetooth row); the `TSUKUROI_CENSUS:` rollup print is B:3210 | `:483` → **I:515**; subject → **I:3386-3387** | stale@B |
| 22 | kumitate | `.ufo/waves/round-44/falsify/ConnAdjacency.md:18` | `:3-16` / `:2501-2517` | B:3-16 = six-plane header (accurate); B:2501-2517 = oom fixture JSON rows; fixture-mode `0555/0644/0400/1777` checks are B:2772-2784 | `:3-16` unchanged; `:2501-2517` → **I:2612-2628**; subject → **I:2883-2895** | moved (3-16), stale@B (2501-2517) |
| 23 | mado | `.ufo/waves/round-18/w1/reports/SentinelHostPause.md:94` | `:351-383` (+`:312-316`) | B:351-383 = btrfs-integrity comments (not "defaults to pacman/systemctl/journalctl/expac"); the override surface is B:393-430; B:312-316 = timing comments (selftest-prefix claim lives at B:385) | `:351-382` unchanged, `:383` → I:411; subject → **I:421-458**; selftest prefix → **I:413** | stale@B |
| 24 | mado | `.ufo/waves/round-24/w1/reports/ConnSiblingOverlap.md:54` | `:2235` | B:2235 = `fi` (closing line) | `:2235` → **I:2346** | moved |
| 25 | mado | `.ufo/waves/round-40/w1/ConnSiblingOverlap.md:80` | `:1950` / `:2279` | B:1950 = `rc_of()` helper; B:2279 = elephant multi-package args (both accurate) | `:1950` → **I:2059**; `:2279` → **I:2390** | moved |
| 26 | mado | `.ufo/waves/round-40/w1-results.json:322` | `:1950,2279` | same | same as #25 | moved |
| 27 | mado | `.ufo/waves/round-41/w1/ScrQualityCriteria/scratch/results-r40-fixed.json:316` | `:1950,2279` | same | same as #25 | moved |
| 28 | tameshi | `corpus/knowledge/service-optin-protocol.md:153` | `:915-970` | B:915-970 = root-arm tail + `probe_systemd` head (no kill-rate/ledger skeleton; the round-5 "23-defect" quote does not exist at B — no kill-table tokens anywhere; the only `6/10` text is B:2749, a comment about the tameshi sweep) | `:915-970` → **I:948-1003** (mechanical); subject absent from I | stale@B (subject dead) |
| 29 | tameshi | `corpus/knowledge/fleet-kill-rate-ledger.md:71` | `:915-920` | B:915-920 = `if [ -n "$report" ]… return` inside root-arm; no 23-defect quote | `:915-920` → **I:948-953** | stale@B (subject dead) |
| 30 | tameshi | `corpus/knowledge/fleet-suite-census.md:302` | `:119-126` | B:119-126 = root-arm documentation (root_status/root_mode notes); "no host touched" selftest header is not verbatim at B | `:119-126` unchanged | stale@B |
| 31 | tameshi | `.ufo/waves/round-16/w2/RunnerDiff.md:106` | `:2174` | B:2174 = `"${EXTRA_ENV[@]}"` (env pass-through, not a runner comment); the `mutate-and-run` comment is B:2426 | `:2174` → **I:2285**; subject → **I:2537** | stale@B |
| 32 | tameshi | `.ufo/waves/round-17/w2/SiblingImpact.md:86` | `:2174` | same as #31 | same | stale@B |
| 33 | tameshi | `.ufo/waves/round-18/w2/SiblingImpact.md:97` | `:2174` | same as #31 | same | stale@B |
| 34 | tameshi | `.ufo/waves/round-25/w1/SiblingOverlap.md:131` | `:2174,2468` | B:2174 as #31; B:2468 = `check 'degraded: kernel ring class counts…'` (accurate) | `:2174` → I:2285; `:2468` → **I:2579** | moved (2468), stale@B (2174) |
| 35 | tameshi | `.ufo/waves/round-31/w1/SentinelCounter.md:11` | `:628-633` | B:628-633 = journal class-count print; the selftest prefix path is B:570/385/1936 | `:628-633` → **I:661-666** | stale@B |
| 36 | tameshi | `.ufo/waves/round-35/w2/ConnectorConfigGuards.md:102` | `:393-430` | B:393-430 = "# host state:" + `PACMAN=${TSUKUROI_PACMAN:-pacman}` etc. (accurate override surface) | straddles first insertion: `:393-407` → **I:421-435**, `:408-430` → **I:438-460** | moved |
| 37 | tameshi | `.ufo/waves/round-47/w1/T47ExecObsE.md:159,:171,:250` | `:487-493` / `:945-948` / `:630` | B:487-493 = R6 foreign-baseline data (B10 mutant region, accurate); B:945-948 = `SYS_NOTE` scope/offline line (accurate); B:630 = `g=` GPU-count line (accurate) | `:487-493` → **I:519-525**; `:945-948` → **I:978-981**; `:630` → **I:663** | moved |
| 38 | tameshi | `.ufo/waves/round-48/a2w1/T48A2ConnFleetFlaky.md:24` | `:2175/2177/2181/2187/2192/2223` | B:2175 = `"$BASH" "$SELF"`; 2177 = `set -e`; 2181 = `host=fixture-host` grep; 2187 = `TSUKUROI_CENSUS:` verdict grep; 2192 = `ABSENT:*)`; 2223 = `rc=$?` (all accurate) | → **I:2286/2288/2292/2298/2303/2334** | moved |
| 39 | tameshi | `.ufo/waves/round-48/a2w1/T48A2RevSalvage.md:106` | `:638` | B:638 = `head -n1` helper; `set -uo pipefail` (selftest entry) is B:1946 | `:638` → **I:671**; subject → **I:2055** | stale@B |
| 40 | tameshi | `.ufo/waves/round-48/a2w1/T48A2RevenSigpipePair.md:12,:23,:179` | `:638` | same as #39 | same | stale@B |
| 41 | tameshi | `.ufo/waves/round-48/a2w1/T48W2ExecC1ProbeB.md:126` | `:935` | B:935 = `case "$state" in` (accurate) | `:935` → **I:968** | moved |
| 42 | tameshi | `.ufo/waves/round-48/w1/T48ExecObs2.md:115` | `:487-493` | as #37 | I:519-525 | moved |
| 43 | tameshi | `.ufo/waves/round-48/w1/T48RevenRegression.md:22,:106` | `:638` | same as #39 | same | stale@B |
| 44 | tameshi | `.ufo/waves/round-48/w1/T48RevenRegression.md:208` | `:771/773/777` | B:771-777 = `fr_note` foreign-count construction (accurate) | → **I:804/806/810** | moved |
| 45 | tameshi | `.ufo/waves/round-21/w2/ProfileBashTsukuroiCensus.md:26` | `:692-694` | B:692-694 = R41-CENSUS-PIPEFAIL warning comment (accurate) | → **I:725-727** | moved |
| 46 | tameshi | `.ufo/waves/round-13/w1/FreshnessCritic.md:91` | `@HEAD :757-814` | B:757-814 = probe code (round-13 HEAD coordinate, historical) | → **I:790-847** | stale@B (historical) |
| 47 | kasegi | `.ufo/waves/round-34/wave1-results.json:364` | `:651-702` / `:1447-1453` | B:651-702 = probe-tail/empty + `probe_packages` head; B:1447-1453 = `journalctl -b -p err` arm (embedded text of another seat's report) | `:651-702` → **I:684-735**; `:1447-1453` → **I:1480-1486** | moved (mechanical) |

### 2b. Frozen pins (old blob `084951be…@165307fe`, 977-line census; unaffected by R44)

| repo | file:line(s) | pinned ranges | note |
|---|---|---|---|
| mado | `.ufo/waves/round-13/frozen/harness.sh:676-712` | B1 `:473`, B2 `:281`, B3 `:434-452`, B4 `:578`, B5 `:615`, B6 `:210`, B7 `:160`, B8 `:935`, B9 `:967`, B10 `:487-493` | frozen round-13 harness; regression runs census at pin `165307fe` (`084951be…`), never live |
| mado | `.ufo/waves/round-14/frozen/harness.sh:676-712` | same | frozen round-14 copy |
| tameshi | `tools/mutate-and-run.sh:748-784` | same ten | the runner's leg spec table; the leg itself pins `165307fe`/`084951be…` — coordinates refer to that blob, not B/I |
| tameshi | `.ufo/waves/round-16/w1/RGLeg.mutate-and-run.sh:687-723`, `round-17/staged/tools/mutate-and-run.sh:729-765`, `round-18/staged/tools/mutate-and-run.sh:737-773` | same ten | frozen/staged copies |
| tameshi | `.ufo/evidence/round-20/coldread/source-{131,1272,1380,1499,1517,1548,1563,1609,1846}.stdout`, `round-25/mte-reports/bash-tsukuroi-census.{spec,mte.json}` | same ten | evidence snapshots of the frozen runner |
| tameshi | `corpus/knowledge/mutation-case-tsukuroi-census.md:356-371` | same ten | historical case note (round 5-era table) |
| tameshi | `.ufo/waves/round-31/w2/RegressionFlake.md:47,:79` | B7 `:160` | run-log quotes of the frozen sweep |

## 3. `btrfs-scrub-record-r43.md`: zero sibling pins; the R44 insertion

`git diff -U0 98020ece 7e081698 -- corpus/knowledge/btrfs-scrub-record-r43.md` → one hunk: `@@ -3,0 +4 @@` (the `extended-by: round 44…` line). Every line ≥4 moves **+1** (`## SR1` B:17 → I:18; `## SR3` B:51 → I:52; `## SR6` B:97 → I:98).

Sibling sweep for `btrfs-scrub-record-r43.md:<n>`: **0 hits** in any sibling repo (all 21 r43 mentions in the fleet outside tsukuroi are tsukuroi's own `.ufo/waves/round-43/…` records; none pin a line). No sibling pin moves because of the r43.md:4 insertion.

## 4. Restated round-43 handoffs (exact draft lines; recipients decide)

Draft — tameshi (`service-optin-protocol.md:153`):

> **Handoff update (round 44).** `tools/tsukuroi-census.sh:915-970` → `:948-1003` mechanically, but note the semantic change: at base `98020ece` lines 915-970 are root-arm/systemd probe code — the round-5 "23-defect" kill-rate quote (ledger skeleton) is **not** in the census anymore (no kill-table tokens; the only `6/10` note is `:2749`, a comment on the tameshi sweep). Point the protocol at the ledger itself (`fleet-kill-rate-ledger.md`) or re-anchor to the sweep comment `:2749` → `:2860`.

Draft — mori (`PROVINCE.md:287`):

> **Handoff update (round 44).** `../tsukuroi-shokunin/tools/tsukuroi-census.sh:376,1100-1115` → mechanical `:376,1133-1148`; `:376` does not hold the `PRESSURE_FILE` default at base (it is `:401`, now `:429`). Re-anchor to `:429` (default) + `:1233-1240` (read/parse), or keep the arm-level range `:1135-1148`.

## 5. Continuation candidates (informational, not counted as strict pins)

53 hits where the `:<n>` reference is separated from the file name by a backtick/space, or is revision-qualified: tameshi `round-13/w1/TsukuroiPin.md:17` (`:1123`), `GateScribe.md:53`, `FreshnessCritic.md:91` (`@HEAD :757-814`), `CR20.md:70` (`@165307fe:139`), `ScoutLegAnchors.md:71-74`, `Read15.md:32`, `T48A2RevenSigpipePair.md:43` (`tools/mutate-and-run.sh:1204`), and the historical `source-*.stdout`/`CR*.md` evidence files. All but the last carry their own revision anchor and are not live pins.

## 6. What I did not do

Did not run `score-scrub-arm-r44.py`, `check-scrub-record-r44.py`, the census or `--selftest` (not in F-9 scope). Did not modify any file in any lane or the fleet root beyond the report path and the receipts dir. Scratch removed at the end.
