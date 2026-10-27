VERDICT: no-finding

Seat ConnSiblings-9 — round 44 wave 1, item X-2: sibling-overlap scan for the round's
surfaces (godspeed). Scan over sibling lanes only; tsukuroi-shokunin itself was skipped
entirely. Read-only; written nothing except this report.

## Scope (files scanned)

Fleet root: /home/vgpnk/Projects/shokunin. 20 sibling lanes, all `*-shokunin` except
tsukuroi-shokunin: audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama,
kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi,
tameshi. Per lane, exactly the three surfaces the seat names: `PROVINCE.md` (20/20
exist), `SKILL.md` (18/20 exist — audio and game-dev-2d have none), and
`corpus/knowledge/` (20/20 exist; recursion includes nested dirs such as
kotodama/corpus/knowledge/culture-material/).

Inventory command (bash, existence only):

    for l in /home/vgpnk/Projects/shokunin/*-shokunin; do n=$(basename "$l");
      [ "$n" = tsukuroi-shokunin ] && continue;
      p=no; s=no; k=no;
      [ -f "$l/PROVINCE.md" ] && p=yes;
      [ -f "$l/SKILL.md" ] && s=yes;
      [ -d "$l/corpus/knowledge" ] && k=yes;
      printf '%s PROVINCE=%s SKILL=%s knowledge=%s\n' "$n" "$p" "$s" "$k"; done

Output: all 20 lanes `PROVINCE=yes knowledge=yes`; 18 `SKILL=yes`; audio and game-dev-2d `SKILL=no`.

## Commands (grep runs)

Let P be the union (58 paths) of the 20 PROVINCE.md files, the 18 SKILL.md files, and
the 20 corpus/knowledge dirs named above. Each term below was run as one grep over P
(pattern, case flag as noted):

    grep -i 'scrub'           P      # broad net (27 files matched — see §Broad)
    grep -i 'scrub_speed_max' P      # 0 matches
    grep -i 'btrfs-scrub@'    P      # 0 matches
    grep -i 'timers\.target\.wants' P  # 0 matches
    grep -i '/var/lib/btrfs'  P      # 0 matches
    grep -i 'ENOTCONN'        P      # 0 matches
    grep -i 'memparse'        P      # 0 matches
    grep    'SCRUB'           P      # 0 matches (case-sensitive)
    grep -i 'scrub-record'    P      # 0 matches
    grep -i 'btrfs[ -]scrub' P      # 0 matches
    grep -i 'btrfs'           P      # sanity: hits are btrfs-as-filesystem only, no scrub
    grep -i 'tsukuroi'        P      # cross-lane refs; 7 lanes, classified below
    grep    'TSUKUROI_CENSUS' P      # 1 lane only (tameshi)

## Results

### 1. Contested scope on the btrfs-scrub surface: NONE

Zero occurrences of every round-surface token in all 20 sibling lanes' PROVINCE.md,
SKILL.md, corpus/knowledge: `btrfs scrub`, `scrub.status`, `scrub_speed_max`,
`btrfs-scrub@`, `timers.target.wants`, `/var/lib/btrfs`, `ENOTCONN`, `memparse`, a
census `SCRUB` line, `scrub-record`. No sibling lane claims or touches any part of the
round's C1/C2 surface; no boundary sentence needs amending for overlap.

The only `btrfs` hits are filesystem-level (not scrub): mori SKILL.md:438-441 (never
threshold btrfs chunk percent) and corpus/knowledge/surfaces-r7.md:153-157 (dm-0 is the
btrfs system+home device); chousa corpus/knowledge/mount-alias-r14.md:30-34 (repo on
btrfs dev 30); kasegi corpus/knowledge/source-tree-loss-2026-09-28.md:36-37,270-273
(mount table; btrfs subvolume query not permitted); kumitate corpus/knowledge/
agent-isolation-substrates.md:47,166-168 and omp-task-contract.md:94-98 (OMP PAL
isolation backends incl. btrfs); souji corpus/knowledge/count-objects-linked-worktree-
garbage.md:89-92,128-131, quarantine-same-filesystem-rename.md:43-49, quarantine-staging-
no-copy-r23.md:29-44 (mv --no-copy support, device ids). None intersects scrub.

### 2. Broad `scrub` net: 27 files matched, all the verb "to scrub an environment"

Every hit is the environment-scrubbing homonym (GIT_*/BASH_ENV/ENV/`env -u`/loader
scrubs), none is btrfs scrub. Representative lines: chousa SKILL.md:96-101,697-733,
corpus/knowledge/capture-bash-pin-r39.md:31-32, capture-path-pin-r41.md:39-40,
env-pin-capture-r38.md:57-73, pin-capture-env-r37.md:26-33; kaidoku SKILL.md:813-817;
kama SKILL.md:751-755; mori SKILL.md:189-197; tabi SKILL.md:1823-1827; tameshi SKILL.md
:477-481,1778-1785,1826-1831, corpus/knowledge/guard-kill-closure.md:97-134,249-252,
mutation-case-kumitate-round-gate.md:141-144, mutation-case-kumitate-sources-check.md:204-206,
verification-patterns-fleet.md:32-35,150-154; audio corpus/knowledge/2026-10-14-sox-posttable-
fallback.md:32-34; kagi corpus/knowledge/config-layering.md:74-78; kotoba corpus/knowledge/
harness-independent-round37.md:18-19,337-481; kotodama corpus/knowledge/culture-material/
bathing-and-body-hygiene.md:7,81, costume-semiotics.md:43; kumitate corpus/knowledge/
agent-isolation-substrates.md:32-36,77-93,161-237,279-283, runtime-remainder-census.md:163-166,
test-inventories.md:109-113. Not relevant to this round; reported for completeness.

### 3. Dependencies on tsukuroi's census (report; do not absorb)

(a) **tameshi-shokunin — a registered consumer/mutator of `tools/tsukuroi-census.sh`**
(the only lane with a `TSUKUROI_CENSUS` token):
- SKILL.md:674-681 cites the census as a gate: "tsukuroi-shokunin/tools/tsukuroi-census.sh
  — a four-plane host-health census (bash, 977 lines, sha256 `084951be…c78c5` at
  measurement) … summary `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)`".
- SKILL.md:687-691 documents the failure mode this round's change is the same class as:
  "the substrate moved mid-run — a concurrent lane (tsukuroi's own S5-1) hardened the tool
  at 14:06:23 (+56 lines, 0 deletions, 9 new selftest cases, 26 → 35)" — i.e., adding
  selftest cases already invalidated their pinned baseline once.
- SKILL.md:1046,1073-1074: their regression ledger already marks the census pin stale —
  `bash-tsukuroi-census 165307fe aa136d69 stale 084951be != bba6cdf6`, "re-read, never
  carry".
- corpus/knowledge/mutation-case-tsukuroi-census.md:63-67 records the census selftest
  case grammar (`PASS <label> (exit N, VERDICT)` per case; the suite "holds on every run")
  and :126-130 asserts the verdict-line prefix `^TSUKUROI_CENSUS: <VERDICT> \(`.
- Impact: C1 adds the `SCRUB` line between the STORAGE line and the rollup and adds nine
  `(R44-C1)` selftest cases (132 → 141). The two existing production lines and the rollup
  line are unchanged, so prefix/field consumers (tameshi's recorded grammar) are safe;
  the selftest rollup case count and the nine new `PASS` lines do change, which is exactly
  the "counting consumer breaks on a new line" class — tameshi's own posture ("re-read,
  never carry") already treats census change as re-pin-only. No action required; notify
  tameshi if the round wants its regression ledger re-pinned.

(b) **mori-shokunin — shared host-evidence adjacency, line-anchor citations**:
- PROVINCE.md:286-290: "tsukuroi's census reads the same system `/proc/pressure/memory`
  file (`../tsukuroi-shokunin/tools/tsukuroi-census.sh:376,1100-1115`) for OS memory
  triage … Shared evidence is not shared ownership."
- Soft break: those two cited line ranges are in-script anchors. If `probe_scrub_record`
  is inserted before line ~1100 (or before 376), mori's citations drift. They are prose
  references, not code deps, so it is a citation-drift note, not a consumer break.
- Also relevant precedent: mori corpus/knowledge/earlyoom-invocation-scope-r30.md:138-139
  cites `.ufo/waves/round-30/w1/ConnectorSiblings.md` — the same seat name as this file.

### 4. Knowledge another lane holds that this round should cite (report; do not absorb)

(a) **kotoba-shokunin — a standing sibling-overlap census method** (the direct precedent
for this seat):
- PROVINCE.md:33: "Sibling census re-pin (round 74, freshness): all 20 § Adjacent lanes
  re-read at frozen fleet heads … counted by `verifiers/check_sibling_reread.py --rev
  <rev>` beside the base `verifiers/check_sibling_census.py --province PROVINCE.md`".
- corpus/knowledge/sibling-overlap-census-round74.md:29-45,66-103,127-131 and
  sibling-overlap-census-round49.md:82-90: method, per-lane row table with frozen commit
  pins and boundary quotes; tsukuroi classified `adjacent` ("Domain specialist — host
  operability & system repair", `PROVINCE.md:22`). If the round wants a standing overlap
  check, kotoba's verifiers are the reusable implementation — cite, do not absorb.

(b) Adjacency statements naming tsukuroi, none touching census lines: kagi PROVINCE.md:67
(tsukuroi tracks 1Password packages); kaidoku PROVINCE.md:124-125 (full-system upgrades go
through tsukuroi's update-safety gate — an existing dependency, unaffected by C1); mado
PROVINCE.md:20,24,34 (package/service state stays with tsukuroi; unit-state rows sit next
to tsukuroi's unit-health ground); souji PROVINCE.md:53-54 (tsukuroi repairs host
operability, never removes packages); kotoba SKILL.md:13-15,126-127 + hook-files-round59.md
:19-23 (host package/initramfs hooks are tsukuroi's). None reads or counts census lines.

## What I did not do

- Ran no counters (C1/C2), no selftests, no git/jj mutations, no host queries.
- Did not scan surfaces outside the three named per lane (e.g., souji `census/`, tools/,
  LOG.md/SCORECARD.md, `.ufo/waves/` receipts). Notes for completeness: souji has a
  `census/` dir and kotoba has `verifiers/` (out of scope here); a future consumer audit
  for census-line counting would look in tameshi `tools/mutate-and-run.sh` + kagi/kumitate
  gate registries. Not performed.
- No peer messaging; leaf seat.

## Bottom line

No contested scope on the btrfs-scrub surface anywhere in the 20 sibling lanes
(PROVINCE.md / SKILL.md / corpus/knowledge). One genuine dependency class found: tameshi
regresses tsukuroi-census.sh and pins its selftest case count — C1's +9 cases (132→141)
and +1 line are a re-pin event for tameshi, not a break (their ledger already treats the
census as stale/moving; "re-read, never carry"). One citation-drift note: mori anchors
`tsukuroi-census.sh:376,1100-1115` in prose and those offsets may move. One method worth
citing: kotoba's sibling-overlap census (`check_sibling_census.py` /
`check_sibling_reread.py`) is the standing tool for exactly this scan.
