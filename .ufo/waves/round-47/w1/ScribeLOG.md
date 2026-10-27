VERDICT: draft

# ScribeLOG — F-16: the round-47 `LOG.md` entry draft

Seat ScribeLOG (L2 leaf, tsukuroi r47 hyaku run 10, wave `w1`). Base `916019057147d7e9ba6b137647b2cee26decf4b8`,
impl (freeze revision the counted seats read) `77e9e2b2e96b85d8f048ae2087e246a542b71611`, lane tip at write
`f6bc6d056ebdf79a585745d4292faf90ae12d9fd`. Lane read-only: nothing tracked was edited, no git/jj mutation in the
lane, no host mutation. All receipts in `.ufo/waves/round-47/w1/ScribeLOG/` (100 KB); every scratch run happened in
`/fast/scratch/hyaku/tsukuroi-r47/ScribeLOG/`, now removed. No tools installed or upgraded.

The draft entry is §3, between the `[BEGIN]`/`[END]` markers, ready to replace the landed header at `LOG.md:1672` and
append. Six tokens remain: they are the facts only the integration run can produce (§4).

## 1. Measurements this seat made (the entry's numbers, with the command that produced each)

| # | Command (lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`) | Observed | Receipt |
|---|---|---|---|
| 1 | `python3 tools/check-scrub-admission-r47.py --revision 91601905…` | exit 1; `structural_ok 1, quotes_ok 3, verdicts_ok 0, marks_ok 0`; quotes GR1 12/12, GR2 26/26, GR3 12/12, `bad []`; `marks {entry:false, readme:false, skill:false}` | `c1-at-base.json` |
| 2 | `python3 tools/check-scrub-admission-r47.py --revision 77e9e2b2…` | exit 1; `structural_ok 1, quotes_ok 3, verdicts_ok 0, marks_ok 0`; quotes GR1 12/12, GR2 28/28, GR3 12/12 (52/52); every seat `dispatched 0 times` (no `w1-results.json`) | `c1-at-impl.json` |
| 3 | `… --revision <base|impl> --section-hash` | GR1 `fe77ac76…9ca8` and GR3 `43430a14…c32c` equal at both revisions; GR2 `4bf28bcf…f6da` (base) → `909830c8…11a2` (impl); `structural_ok 1`, `problems []` at both | `sections-base.json`, `sections-impl.json` |
| 4 | `env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/tmp" bash /fast/…/l1-before/census-base.sh --selftest` (script sha256 `ac4e38ff…48e4` = `git show 91601905:tools/tsukuroi-census.sh`) | rc 0; `TSUKUROI_CENSUS_SELFTEST: PASS (162 cases, 162 passed, 0 failed)` | `selftest-base-clean.log` |
| 5 | frozen counting command: `env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" bash tools/tsukuroi-census.sh --selftest` (worktree script sha256 `adb1b4ce…ce41` = `git show 77e9e2b2:tools/tsukuroi-census.sh`) | rc 0; `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`; both `(R47-C2)` cases PASS; eight `(R46-C1)`-tagged lines PASS | `selftest-impl-space.log` |
| 6 | same, `TMPDIR="$S/tmp"` (space-free) | rc 0; PASS 164/164 | `selftest-impl-clean.log` |
| 7 | `cmp` on the L1's `live-before.norm` / `live-after.norm` (`/fast/scratch/hyaku/tsukuroi-r47/l1-before/`) | identical (and the raw `.txt` pair identical); SCRUB line and the `TSUKUROI_CENSUS: BLOCKED (…)` rollup equal | §2 F6 |
| 8 | `python3 tools/check-adjacency-anchors.py --revision {91601905, 77e9e2b2, f6bc6d05}` | PASS / **FAIL** / PASS — impl finding `INBOUND-CLASSIFICATION-WRONG` at `corpus/knowledge/adjacency-anchors-r19.json:inbound[108]`; `branch_tip f6bc6d05` in all three | `adjacency-*.json` |
| 9 | fixture replay: `git clone -q --shared <lane> $D` (toplevel asserted `= $D`), copy the 18 `R47*.md` counted reports, write `w1-results.json` `{results:[{name,agent}]}` from `w1-spec.json` roles, commit `-c user.name=fixture -c user.email=fixture@invalid`, `python3 tools/check-scrub-admission-r47.py --lane "$D" --revision 867ce10` | exit 1; `structural_ok 1, quotes_ok 3, verdicts_ok 1, marks_ok 0, verdict FAIL`; GR1 `row_ok true` (6 bound, all `holds`, bodies distinct, citations resolve); GR2 `row_ok false` (`any_fails true`, `bound 6`: 5 `partly` + 1 `fails`); GR3 `row_ok false` (6 bound, all `holds`, but `citations_ok false`) | `fixture-replay.json` |
| 10 | assimilation id check, the round-46 method: `git show 77e9e2b2:corpus/SOURCES.md \| grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → `reg-ids`; same expression on `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` → `staged-ids`; `comm -12` | registry 252 ids, staged 147, collisions **53** (S200-S252) — identical to the wave seat's own `assimilation/{reg-ids,staged-ids,collisions}` (252/147/53) | `reg-ids`, `staged-ids`, `collisions` |
| 11 | `w1-spec.json` / `w1-dispatch.json` | 64 seats: reviewer 15, critic 15, executor 9, scout 9, scribe 6, mutation-tester 4, sentinel 3, connector 3; `counts.spawn 64`; no `R47Res2*` member | §3 waves line |
| 12 | `controls/battery-summary-r47.jsonl` | 12 lines, `as_expected true` 12/12 | controls line |

Not run: the round's real binding (see §4), the round-end sources census, any host mutation.

## 2. Findings that change how the entry must read

**F1 — the C1 wave as written admits GR1 only (replay: `verdicts_ok 1`).** This is the draft's most consequential
fact. The 18 counted reports all satisfy the two binding lines (checked one by one, `seat-first-lines.txt`): GR1 6/6
`holds`, GR2 5 `partly` + 1 `fails`, GR3 6/6 `holds`; every hash matches the counter's section hash. The rows still
fail, and for reasons the L1 cannot repair by amending rows:

- *GR3* — `R47RevGR3a.md:28` and `R47RevGR3b.md:19` quote `capture.txt:4`, whose content is
  `stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`. `CITE_RE`
  (`tools/check-scrub-admission-r47.py:83`, `\b([A-Za-z0-9_.@+-]+\.[a-z0-9]+):(\d+)\b`) matches the drop-in path
  inside that quoted capture line, and `verify_citation` (`:281-286`) rejects it because no snapshot holds a file
  named `10-faster-shutdown.conf`. The seats' reasoning is correct; the counter's citation leg reads a path *inside a
  quote* as a citation. Both reports otherwise say `holds`, so the row is lost to a text artifact.
- *GR2* — beside `R47CritGR2b`'s `fails`, four bodies (`R47RevGR2a`, `R47RevGR2b`, `R47CritGR2a`, `R47ResRevGR2`)
  cite `S240 ioctl.c:3190`. S240 is a live registry row with a frozen snapshot (`corpus/SOURCES.md:249`;
  `.ufo/waves/round-43/frozen/src/ioctl.c`, sha256 `7b3488f2…ba01`) but it is absent from the round-47
  `SNAPSHOTS` map (`:54-76`, S237, S242-S244, S246-S249), so the K22 seat leg refuses the citation.
- *Entanglement (K23)* — `distinct_bodies` is computed over the bodies that survived K22 (`:347-353`), so any citation
  problem also flips K23 false (GR2 and GR3 both read `distinct_bodies false` with 4 clean bodies against 6 bound).
  The counter cannot distinguish "duplicate bodies" from "some bodies excluded".

Both are counter-versus-report collisions, not row edits: a second row amendment cannot clear them, and the
`R47Res2*` generation (held, undispatched) would re-read the same citation problem. The draft therefore states C1
FAIL with the causes instead of leaving the outcome to be invented at integration. Route them in the lesson as wave
findings (proposed ids `R47-C1-K22-PATH-IN-QUOTE` and `R47-C1-K22-S240-UNPINNED`).

**F2 — the adjacency gate is red at the impl revision, green at the tip.** `check-adjacency-anchors.py` reads PASS at
`91601905`, FAIL at `77e9e2b2` (`INBOUND-CLASSIFICATION-WRONG`, `adjacency-anchors-r19.json` inbound[108]: IN-109's
`found_line` is 2593 while the JSON at that revision still carries 2582), PASS at `f6bc6d05`, which repins it
(`round-47: adjacency anchor IN-109 found_line 2582->2593 (R47-C2 census edit moved the D14/D15 case)`). The C1 kill
rule names "adjacency anchors gate PASS"; the draft says where that holds (the tip) and discloses the red revision
rather than citing only the green one. `w1/C1ExecGatePred.md` reached the same reading independently.

**F3 — the landed round-47 header does not match the round-46 shape.** `LOG.md:1672` reads
`## Round 47 (2026-10-27, base \`91601905…\`)`: no `— `, no `hyaku run 10`, no `L1 TsukuroiR47`, no impl sha
(round 46: `## Round 46 — 2026-10-27 (hyaku run 9; L1 TsukuroiR46)`). The draft supplies the replacement line.

**F4 — the landed paragraph's C2 before-receipt path does not resolve in the lane.** `LOG.md:1680` cites
`l1-before/selftest-space-before.log`; `.ufo/waves/round-47/before/` holds only `sources-census-start.txt` and
`c1-before-base.jsonl` — the log lives at `/fast/scratch/hyaku/tsukuroi-r47/l1-before/selftest-space-before.log`.
Its space-free twin ("space-free PASS 162/162", `LOG.md:1681`) had no receipt until this seat ran the base blob
(§1 row 4). The draft cites lane-resolvable receipts only (`w1/ScribeLOG/…`) plus the absolute `/fast` path for the
L1's log; the L1 may instead copy `l1-before/*.log` into `before/` and shorten the citation.

**F5 — `controls/battery.py` docstring names the wrong revision.** `:4` "fixture git clone of the lane at IMPL
(3629c46a)" against `:12` `IMPL = '77e9e2b2e96b85d8f048ae2087e246a542b71611'`. The code is the authority and the
12/12 summary is consistent with the F1 closure existing only at `77e9e2b2`; the docstring is stale. The draft does
not quote it.

**F6 — C2's live-output kill rule is satisfied on the L1's own receipts.** `cmp` on `live-before.norm` /
`live-after.norm` (432 B each) and on the raw pair returns identical; the SCRUB line
(`state=NONE dir=absent records=0 …`) and the rollup line agree. The `--identity` shape and the exit map are the
remaining legs and are the seats' to report (`w1/C2ExecKillRules.md` had not landed at write), so the draft carries
that clause as a token.

## 3. Draft entry — text to put in `LOG.md` at integration

Placement: the block replaces `LOG.md:1672-1682` (the landed header plus its five lines) and appends the
rest. The motivating evidence, the ordinals and the three round-start receipts are kept; the header is brought to
the round-46 shape (F3) and the receipt citations are made lane-resolvable (F4).

`[BEGIN]`

## Round 47 — 2026-10-27 (hyaku run 10; L1 TsukuroiR47; base `916019057147d7e9ba6b137647b2cee26decf4b8`, impl `77e9e2b2e96b85d8f048ae2087e246a542b71611`)

Fresh-start round (rounds 44-46 closed rejected-harmed / rejected-honest-stop / rejected-harmed;
the three spot-checks were read before any claim: `corpus/lessons/round-4{4,5,6}-verifier-spotcheck.md`).
Ordinals at base: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8;
depth and adjacency tied lowest; C1 works depth, C2 works operability. Saturation 9 / window 3.
Round-start receipts (`.ufo/waves/round-47/before/`): sources census exit 0
(`sources-census-start.txt`, 40 W04, this attempt's own start — round-45 routed D4); C1 before-state
at base: `check-scrub-admission-r47.py --revision 91601905…` FAILs `verdicts_ok 0, marks_ok 0`
(`before/c1-before-base.jsonl`; structural 1, quotes 3, 50/50 quote texts located on their pinned
lines); C2 before-state at base: the selftest under a `TMPDIR` containing a space FAILs
`(162 cases, 13 passed, 149 failed)` rc 1 (control C2-K0 reproduces it; the L1's
`/fast/scratch/hyaku/tsukuroi-r47/l1-before/selftest-space-before.log`), and PASS 162/162 space-free
at the base blob `ac4e38ff…48e4` (`w1/ScribeLOG/selftest-base-clean.log`).

Claims (frozen in `SCORECARD.md` "Round 47 — declaration", before any seat). C1 depth: GR1-GR3 of
`corpus/knowledge/btrfs-scrub-grounding-r45.md` are admitted only through counted seats that bind
`ROW GR<n> VERDICT: <holds|partly|fails>` and `SECTION SHA256: <64-hex>` as the first two lines of
their own reports (18 counted seats, the `R47Res2*` generation held; sized for two amendment rounds);
GR2 amended pre-wave per the round-46 counted residual critic (the filesystem-closing `-EAGAIN`
return, scrub.c:3094-3095, leads the ordering, and the suspend sentence is narrowed to the unmount
path, dev-replace.c:1143-1144); predicate `structural_ok == 1 and quotes_ok == 3 and
verdicts_ok == 3 and marks_ok == 3`, each row bound to `## GR<n>` up to its expected next header and
failing closed on any other `## ` line inside. C2 operability (sourced S252, mktemp(1)): the census
selftest derives a classifiable fixture base (`root_locator_class` charset, `/tmp` fallback) and
gains two `(R47-C2)` pinning cases; predicate `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164
passed, 0 failed)` rc 0 under a `TMPDIR` containing a space, and 164/164 space-free. Controls before
any seat (`.ufo/waves/round-47/controls/`, `battery-summary-r47.jsonl`): 12/12 as declared — C1
K0/K1/K22a/K23a/F1a/F1b/F2a/F3a FAIL, K-pass PASS; C2 K0/K2 FAIL, K-pass PASS.

Waves: `w1` one v2 wave of 64 seats (15 reviewer, 15 critic, 9 executor, 9 scout, 6 scribe,
4 mutation-tester, 3 sentinel, 3 connector; 18 of them counted C1 seats; `R47Res2*` not dispatched)
— {DEADSEATS}.

Measured at `77e9e2b2`. C1 — **FAIL**: {C1LEGS}. The verdicts bound from the 18 counted report bytes
(replayed with a results record, `w1/ScribeLOG/fixture-replay.json`) read `verdicts_ok 1` — GR1
admitted (6/6 `holds`, bodies pairwise distinct, every citation resolving); GR2 not admitted (five
`partly` and one `fails`, `R47CritGR2b`, with four bodies also citing S240 `ioctl.c`, which the
round-47 snapshot map does not pin); GR3 not admitted (6/6 `holds`, but `R47RevGR3a.md:28` and
`R47RevGR3b.md:19` carry the drop-in path `10-faster-shutdown.conf:2` inside the `capture.txt:4`
quote, and `CITE_RE` reads a path inside a quote as a cited file). Quote legs 52/52 (GR1 12,
GR2 28, GR3 12); GR1 `fe77ac76…9ca8` and GR3 `43430a14…c32c` section hashes equal to base, GR2
`4bf28bcf…f6da` → `909830c8…11a2` (the amendment's own bytes). C2 — **PASS**: 164/164 rc 0 under a
space `TMPDIR` and 164/164 space-free, both `(R47-C2)` cases green, every `(R46-C1)` case green
(`w1/ScribeLOG/selftest-impl-{space,clean}.log`, impl blob `adb1b4ce…ce41`). Kill rules: live census
output digits-stripped byte-identical base vs final (`cmp` on the L1's `live-before.norm` /
`live-after.norm`), `--identity` line shape unchanged, exit map {EXITMAP}.

Adjacency: `check-adjacency-anchors.py` PASS at base `91601905` and at the tip `f6bc6d05` (IN-109
`found_line` re-pinned 2582→2593 after the C2 census edit moved the D14/D15 case), **FAIL at the impl
revision `77e9e2b2`** (`INBOUND-CLASSIFICATION-WRONG`, `corpus/knowledge/adjacency-anchors-r19.json`
inbound[108]); disclosed, not smoothed — the C1 kill rule's adjacency clause is green only at the
tip.

**Freshness.** Re-verification of predecessor pins, 2026-10-27: S252 re-opened live by wave seat
C2ScoutMktemp, byte-identical (9832 B, `74186433…3266`; `w1/C2ScoutMktemp.md` §1); the frozen
snapshot digests of S237, S242-S244 and S246-S249 re-checked with `sha256sum -c` by the counted
seats (`w1/R47RevGR1b.md`, `w1/R47ResRevGR1.md`, `w1/R47ResRevGR3.md`) and every `**Quote.**` line
verified against them by the counter's quote leg (50 at base, 52 at impl, no `bad` entry); the six
predecessor counters (r42-r46 plus the adjacency gate) re-run by `w1/C1ExecGatePred.md`; the sources
census re-run at round end ({CENSUSEND}).

considerthese: {PROPOSAL} mined (`considerthese/…`, `w1/ConsGate.md` §3). Assimilation: none — the
staged corpus-expansion-1 package collides with 53 lane ids (252 registry ids at impl, 147 staged,
S200-S252; `assimilation/{reg-ids,staged-ids,collisions}`, `w1/AsmGate.md`; independently
re-derived at `w1/ScribeLOG/collisions`), and no staged theme meets the scrub-grounding or census
surfaces.

Landed: `3629c46a` C2 TMPDIR-space fix and the two `(R47-C2)` cases, the GR2 amendment, the r47
admission counter, S252 and the declaration; `77e9e2b2` the counter's F1 closure (row extent bound,
battery F1a); `e31070a9` the freeze — w1 spec (64 seats), controls battery 12/12, before receipts;
`f6bc6d05` the IN-109 repin; {OUTCOME} this entry with the outcome, corrections, lesson and receipts.
Lesson `corpus/lessons/round-47.md`; report `.ufo/reports/round-47/tsukuroi.md` (fleet repo).

`[END]`

## 4. The six tokens, and where each value comes from at integration

1. `{DEADSEATS}` — from `w1-results.json` (seats with no output) plus the seat list in `w1-dispatch.json`: e.g.
   "no dead seat" / "N dead: …". At the count made here, 49 of 64 seat reports existed (54 by the end of this seat's
   work, `ls w1/*.md | wc -l`); no results record yet.
2. `{C1LEGS}` — the real run, `python3 tools/check-scrub-admission-r47.py --revision 77e9e2b2…`, after the L1 commits
   `w1-results.json`: `verdicts_ok`/`marks_ok` and exit code. The replay (§1 row 9, `fixture-replay.json`) is a
   prediction under a synthetic results record, not the binding; if the real run differs, its numbers replace the
   replay's sentence and the entry says which run produced them.
3. `{EXITMAP}` — `w1/C2ExecKillRules.md`; not landed at write, so the clause is quoted as the kill rule states it and
   completed at integration ("unchanged, `w1/C2ExecKillRules.md`" or the observed map).
4. `{CENSUSEND}` — the round-end sources census (kill rule "exit 0 at round end"), e.g. "exit 0, `ok`, 40 W04
   unchanged, N rows against 252 at impl" (`.ufo/waves/round-47/after/…`). At write only the round-start run exists.
5. `{PROPOSAL}` — the L1's choice among `w1/ConsGate.md` §3's four relevant-and-unimplemented proposals (upstream
   release watch, routed-defect disposition criterion, and two more); the seat's report is a draft and names no pick.
6. `{OUTCOME}` — the outcome commit sha.

## 5. What I did not do

- Did not write `w1-results.json` in the lane or simulate it there: the replay ran in a throwaway `git clone --shared`
  fixture under my scratch (`fx.9x6HlN`, commit `867ce106f29545e10a8867548721742f4f008b6b`, removed with the scratch
  dir). No lane index, ref or jj state was touched.
- Did not edit `LOG.md`, `SCORECARD.md`, the entry, `SKILL.md`, `corpus/README.md` or any seat report; did not run
  `pacman`; did not start/stop a unit; did not write sysfs; did not run `btrfs scrub`/`replace`.
- Did not re-fetch S237/S242-S249 live (the counted seats verified their digests against `SHA256SUMS`; only S252 was
  re-opened over the network, by `w1/C2ScoutMktemp.md`), and did not run the round-end sources census.
- Did not measure QUALITY or the registry row count for round 47; the entry omits both rather than guessing.
