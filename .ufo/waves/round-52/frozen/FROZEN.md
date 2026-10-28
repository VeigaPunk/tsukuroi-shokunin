# Round 52 — FROZEN record (tsukuroi, hyaku run 11 continuation, L1 TsukuroiR52, attempt 1)

Base revision (lane tip at round start, before any round-52 byte):
`cc88b81d78bcbe06bce3f6bf722a108432ad276f` · branch `master`.

Freeze revision = the lane commit that carries this file (`round-52: FREEZE …`). Every seat reads lane
bytes with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show <FREEZE>:<path>`; the working
tree is mutable and is never the bytes under test.

Resume posture (declared before data): rounds 49-51 each closed `rejected-honest-stop` on claim C1.
Round 51 froze and amended everything C1 needs; the counted cohort never ran, and the C2 receipt was
broken by the L1's own scratch deletion (`corpus/lessons/round-51.md`, Gate rejection). Round 52 does
NOT refreeze the row bytes: the counted bytes are the round-51 AMENDMENT-1 bytes, unchanged since
`6abef5d0` (`git diff 6abef5d0 cc88b81d -- corpus/knowledge/btrfs-scrub-grounding-r45.md` is empty),
and the C2/C3 instruments are the round-51 tools reused unchanged. The only new instrument is
`tools/check-scrub-admission-r52.py` — the round-51 counter with exactly four round bindings changed
and no logic change: wave path (`.ufo/waves/round-52/w1`), seat names (`R52RevGR<n>{a,b,c}` /
`R52CritGR<n>{a,b,c}`), admission marks (round 52), base. Its sha256 at the freeze is in
`FROZEN-hashes.txt` beside this file; the round-51 counter sha256 it derives from is recorded in its
docstring. Because no round-52 seat had scored at freeze time, this renaming is the claim's rule as
first declared for round 52 — nothing was widened, loosened or narrowed relative to the round-51
frozen predicate, which is reproduced verbatim below.

## Claims (3, causally separable, distinct axes)

| Claim | Axis | Surface moved | Frozen counter | Do-nothing control scores | Target predicate |
|---|---|---|---|---|---|
| C1 | depth (lowest tied 8; sourced S237 S240 S242 S243 S246 S247 S248; row bytes = the r51 amendment) | GR1-GR3 read `holds` by the fresh counted 18-seat cohort of `w1`; the three round-52 admission marks land only on three clean counted rows | `python3 tools/check-scrub-admission-r52.py --revision <REV>` (defaults read `.ufo/waves/round-52/w1-results.json` / `-dispatch.json` at REV) | base bytes, no cohort: `lint_ok 3, quotes_ok 3, verdicts_ok 0, seats_ok 0, marks_ok 0` FAIL (`before/c1-at-base.json`) | `structural_ok == 1 and lint_ok == 3 and quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3` |
| C2 | operability (instrument-measurement completion; sourced S256 + S257 opened this round) | a VALID receipt of `tools/score-counter-cheats-r51.py` (5 cheats) in an undisturbed scratch at the integrated revision — the r51 amend1 attempt is committed broken (ERROR rows; spot-check defect e) | `python3 tools/score-counter-cheats-r51.py --revision <REV> --scratch <DIR>` | skip the run: no valid receipt exists anywhere (r51 spot-check graded C2 `unprovable`) | `real_pass == 1 and cheats == 5 and cheats_rejected == 5 and r50_cheats_rejected == 0`; kill: any ERROR row, any unrejected cheat, or a scratch disturbed between run and receipt |
| C3 | adjacency (lowest tied 8; instrument-measurement completion) | the round-51 counter measured at ONE named integrated revision with the full leg set; r51 closed with battery K-pass rows only | `python3 tools/check-adjacency-table-r51.py --revision <REV>` | at base the counter already PASSES all legs with `r50_blind 1` (`before/c3-at-base-r52.json`); what a skip cannot produce is the receipt at the integrated revision with the battery green | the full r51 predicate (`adj_rows == 7 and linked_rows == 7 and bare_ranges == 0 and anchors_ok == 7 and registry_ok == 7 and anchors_checker_rc == 0 and quote_at_pin_ok == 9 and live_quote_ok >= 8 and stub_fails == 1 and display_bound_ok == 10 and quote_specific_ok == 10 and display_forge_fails == 1 and override_blocked == 1 and digests_bound_ok == 10 and r50_blind == 1 and anchor_rows_exact == 1 and adj_exact == 1 and bare_all == 0 and ancestry_ok == 10 and recipient_ok == 7`) |

Causal separability: C1 reads the entry, SOURCES.md, snapshots and the w1 cohort; C2 reads the census
blob and its own scratch; C3 reads `PROVINCE.md`, the anchor registry and sibling repos. No counter
reads another claim's surface. C2 and C3 are instrument claims; the census, `PROVINCE.md` and the
registry are not changed by them.

## Counted cohort (claim C1) — 18 seats in wave `w1`

`R52RevGR{1,2,3}{a,b,c}` (reviewer) and `R52CritGR{1,2,3}{a,b,c}` (critic). A report binds only as a
FILE at `.ufo/waves/round-52/w1/<seat>.md`, line 1 `ROW GR<n> VERDICT: holds|partly|fails`, line 2
`SECTION SHA256: <hex>`, body ≥ 300 bytes citing at least TWO distinct row source files by `file:line`
that resolve in the pinned snapshots (or a declared lane artifact). A bound-format negative
(`partly`/`fails`) on any hash blocks the row whatever its citations; a report whose citations do not
resolve earns nothing. Each expected seat must also be exactly one completed entry of
`w1-results.json` (name, agent, non-empty output) and one dispatch task with the declared role.

Section hashes at the freeze (`--section-hash`):
GR1 `98fa4e07768d240eaf5ea2cce13ce0623fdb756054e5df9f7b9fe68ab2e63987` ·
GR2 `9fd581a0c9d02b02100b6a15648b7c6e4be896ac746ed09303a88dc8a24f0ec5` ·
GR3 `0405f38a5783c49b6c078b118c9868543eb494b43f8b1c5e6c14284a123b9eac`.

## Pre-data controls (receipts under `.ufo/waves/round-52/controls/`, run after the freeze commit, before dispatch)

Battery `.ufo/waves/round-52/controls/battery.py --freeze <FREEZE> --tag freeze`:

- C1 (26 controls): K0 base entry no cohort (FAIL) · K1 corrected entry + marks, no cohort (FAIL) ·
  K2 all-holds on bytes with the cmdline.c:147 leader dropped (FAIL) · K3 undeclared range gap
  (FAIL) · K3b fragment quote (FAIL) · K4 one bound `partly` (FAIL) · K5 whitespace-padded identical
  bodies (FAIL) · K6 GR1 reviewers only (FAIL) · K7 reports but no results entries (FAIL) · K8
  lane-artifact citations only (FAIL) · K9-K11 + A/G/D/Q/H lint cheats (FAIL) · K-pass corrected
  entry + marks + 18 valid R52 reports (PASS).
- C2 (2 controls): K-pass the scorer on the real census (PASS: 5/5 cheats rejected, r50 rejects 0) ·
  K0 the round-50 counter in the claim slot (FAIL: rejects none).
- C3 (15 controls): K0 false displayed OUT-009 commit · K1 override without `--control` · K2
  shape-valid stub · K3 registry digest mutated · K4 registry `quote_line` moved · K5 displayed
  digest-list line altered · K6-K13 round-51 additions — none may PASS; K-pass real province +
  registry (PASS).

K-pass runs use synthetic fixtures to prove a counter CAN pass; they are never reported as the
claim's measurement. The measurement is the live integrated revision.

## Named limits carried from rounds 50-51 (disclosed, not closed)

A coordinated forgery that swaps a quote for another REAL sentence of the same pinned blob (C3:
bytes-bound, not proposition-bound); a PATH/sitecustomize shim that changes what git returns (C3); a
liar that reasons semantically about arbitrary edits of itself, a producer that is a function, alias
or `eval` (C2); a clause the pre-read and the cohort both misjudge (C1: the lint checks quotes and
citations, not truth).

## Environment / guards carried into every seat prompt

Lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (git `master`, jj-colocated: the L1 is
the only writer, `jj-lane.sh` only). Seats are read-only on tracked files and write only their report
plus receipts under `.ufo/waves/round-52/w1/<seat>[.md]` and `<seat>/`; scratch under
`/fast/scratch/hyaku/tsukuroi-r52/<seat>/`, removed on exit; no git/jj mutation outside a throwaway
fixture repo under that scratch dir; tooling authorization (operator, 2026-10-19) with the pacman
pause (install via `uv tool`/`npx`/official `~/.local/bin` binary only). Relative `Report:` trailers
land under the lane root. Absolute paths for every file-touching tool call (QUALITY 95).
