VERDICT: supports

# C1ExecFinalPrior — item C1-5: frozen predecessor storage counters at base and at the integrated tip

Base `98020ece0674e0b569ee23aed10ffbee355b248e`; measured revision `8eee79db608b5815c325a5af7cbfdeac50eda9f4`.
Every run went through `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/run-receipt.py`
(private `git clone --no-local` of the lane at the measured revision, every inherited `GIT_*` name stripped,
`HOME`/`XDG_CONFIG_HOME` at an empty private dir), one counter at a time. `run-receipt.py` has no
`--scratch` option; its own temp trees are `mkdtemp` under `/fast/scratch/hyaku` and were removed on exit
(`ls -d /fast/scratch/hyaku/run-receipt-*` → 0 after the runs). `--scratch
/fast/scratch/hyaku/tsukuroi-r44/C1ExecFinalPrior/s` was passed to all four counters, each of which accepts it.

Tool bytes are identical at both revisions (the run-receipt `tool_sha256` field, confirmed independently with
`git show <rev>:tools/<tool> | sha256sum`), so tool-version is not a confound in any delta below:

| tool | sha256 at base and at tip |
|---|---|
| `tools/score-storage-arm-r38.py` | `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218` |
| `tools/score-storage-arm-r38-q82.py` | `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3` |
| `tools/score-storage-hidden-r39.py` | `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973` |
| `tools/score-size-invariance-r42.py` | `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03` |

## Results (receipts in `.ufo/waves/round-44/w2/C1ExecFinalPrior/`)

| counter | base `98020ece` | tip `8eee79db` | verdict delta |
|---|---|---|---|
| `score-storage-arm-r38.py` | FAIL exit 1 — `fixtures_matched` 9/10, `live_match` 1, `six_planes_all` 1 (`score-storage-arm-r38-base.jsonl`, 00:55:32–00:56:00Z) | FAIL exit 1 — `fixtures_matched` 9/10, `live_match` 1, `six_planes_all` 1 (`…-tip.jsonl`, 00:56:28–00:56:54Z) | **none** (same single fixture, byte-identical fixture legs) |
| `score-storage-arm-r38-q82.py` | PASS exit 0 — `ns_views_matched` 3/3, `ns_available` 1 (`…q82-base.jsonl`, 00:57:05–00:57:11Z) | PASS exit 0 — 3/3, `ns_available` 1 (`…q82-tip.jsonl`, 00:57:15–00:57:22Z) | **none** |
| `score-storage-hidden-r39.py` | PASS exit 0 — `hidden_matched` 2, `views_matched` 3, `fixtures_matched` 5, `live_match` 1, `six_planes_all` 1 (`…hidden-r39-base.jsonl`, 00:57:26–00:57:49Z) | PASS exit 0 — identical conjuncts (`…hidden-r39-tip.jsonl`, 00:58:11–00:58:34Z) | **none** |
| `score-size-invariance-r42.py` | PASS exit 0 — `cases` 10, `invariant` 10, `ns_invariant` 3, `selftest_pass` 1, `default_equal` 1 (`…size-invariance-r42-base.jsonl`, 00:58:39–00:59:20Z) | PASS exit 0 — identical conjuncts (`…size-invariance-r42-tip.jsonl`, 00:59:25–01:00:05Z) | **none** |

Machine summary of the eight receipts: `C1ExecFinalPrior/summary.json`.

Leg-by-leg comparison of the receipt bodies (base vs tip, same fields):

- `score-storage-arm-r38`: all ten fixtures have the same `got` at both revisions and `census_exit` 2 in every
  fixture at both; the live leg is `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`
  with `six_planes` true and `census_exit` 2 at both. The one non-match is `F06-no-btrfs-root` at *both*
  revisions: expected `HEALTHY 0/0/0`, got `BLOCKED 0/0/0`
  (`detail=mounts:btrfs-without-sysfs` on the STORAGE line).
- `score-storage-arm-r38-q82`: views `zero`, `nonzero`, `any` all match at both, `census_exit` 2 in every view.
- `score-storage-hidden-r39`: H1/H2 hidden legs `got` byte-identical at both; the five override fixtures and the
  live leg `got` byte-identical at both (`census_exit` 2 in all seven); all three random views match at both.
- `score-size-invariance-r42`: per-case invariants and both twins' exit codes identical at both
  (P4/U1/U2/U3 rc 1, P5/U4 rc 0, P1/P2/P3/P6 rc 2); N1/N3/N6 namespace legs invariant at both;
  `selftest_pass` 1 and `default_equal` 1 at both.

## The r38 v1 FAIL is pre-existing, declared staleness — not a base→tip delta

- `score-storage-arm-r38.py` fails **at base** because its fixture `F06-no-btrfs-root` (override root absent,
  real `/proc/self/mounts` naming a btrfs mount) predates the round-39 absent-root rule. The census blob at base
  `18a1db6448358d7ecf4634570fcd2bf075eccb1b` already carries that cross-check: both census blobs contain the
  `mounts:btrfs-without-sysfs` branch (10 occurrences each), and the base fixture therefore reads BLOCKED too.
- This is the documented superseded state, not a new observation: `SKILL.md:3318` registry row
  `historical-storage-arm-r38-f06` marks the tool HISTORICAL at `F06-no-btrfs-root` only and pins it to census
  blobs `119b6453…` / `8ef604c0…`; our blobs (`18a1db64…` base, `8a2a665c8c9ac1795ea52819ee565ae4f0b65b00` tip)
  lie outside that pin. Round 39's declaration and seat `C1ExecR38Counters` recorded the same flip
  (PASS 10/10 at `0eff65b2`, FAIL 9/10 after the fix — `.ufo/waves/round-39/w1/C1ExecR38Counters.md:28-31,88`).
- Consequence for the C1 kill clause: the clause fires on "FAILs at the measured revision where it PASSes at
  base". Here base FAILs with the identical fixture set and identical live leg, so the clause does not fire and
  the v1 counter carries **no** regression signal at this tip. The three counters that PASS at base (q82,
  hidden-r39, size-invariance-r42) all still PASS at the tip; those are the ones that discriminate.

## Secondary no-harm observation (outside this item's predicate)

To make sure the three PASSing counters were not blind to a `PLANE`/rollup change (they parse only the STORAGE
line, a plane count, or the packages plane in a fixture), I ran the **live** census from both committed blobs
with the fixed child environment the counters use (read-only; nothing written under `/var/lib` or `/etc`):

- base blob `18a1db64…` (file sha256 `7c9f7903…`) exit 2, six `PLANE` lines, one `TSUKUROI_CENSUS:` line;
- tip blob `8a2a665c…` (file sha256 `2ef86357…`) exit 2, six `PLANE` lines, one `TSUKUROI_CENSUS:` line;
- after normalizing the live-volatile fields (timestamp header, `C5_pswp`, `C6_psi_full_total_us`,
  `C6_avail_kb`) the tip output equals the base output plus exactly one inserted line and nothing removed:
  `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`,
  placed between `STORAGE …` and the rollup. STORAGE and the rollup line are byte-identical, and both exit 2.
- Raw captures: `C1ExecFinalPrior/live-census-base.out`, `C1ExecFinalPrior/live-census-tip.out`.
- This is not this seat's scored predicate (the C1 counter owns the PLANE/rollup/exit conjunct); it is recorded
  only as a supporting observation that the tip adds the claimed line and changes nothing else on the live host,
  and that `default_equal 1` at the tip independently shows the same for the fixture path on the packages plane.

## Limits

- Host state during the runs: btrfs mounted (one filesystem, one device, all five counters zero), `/var/lib/btrfs`
  absent, unprivileged user namespaces enabled, `unshare`/`setpriv` present. The live legs of the v1 and hidden
  counters, and the namespace legs of q82/hidden/size, were exercised against this host only.
- `master` advanced while the wave was in flight: the v1 base receipt recorded `branch_tip`
  `0f8c07a5035cc9469f59ae41726335388b1cbcac`, every later receipt `3a1c6b5c958c4f289a8b12551f96d843877b700e`.
  Both measured revisions were ancestors of both tips (`git merge-base --is-ancestor`), and each receipt pins
  the tip it saw, so the comparison is still base-commit vs tip-commit content, not branch state.
- Because the v1 counter FAILs at base on this host, a future round that keeps it in a kill rule should either
  pin it inside the `historical-storage-arm-r38-f06` window or drop F06; as written the clause is
  vacuous for it here (it cannot fail "where it PASSes at base").

## Proposed text

> C1-5 (w2, predecessor counters): at base `98020ece` and integrated tip `8eee79db`, each of the four frozen
> predecessor storage counters was run through `tools/run-receipt.py` from a private clone at the measured
> revision (receipts `.ufo/waves/round-44/w2/C1ExecFinalPrior/*.jsonl`). `score-storage-arm-r38-q82.py` PASSes
> 3/3 namespace views at both; `score-storage-hidden-r39.py` PASSes (2 hidden + 3 views + 5 fixtures + live) at
> both; `score-size-invariance-r42.py` PASSes (10/10 cases, 3/3 namespace legs, selftest, `default_equal`) at
> both; `score-storage-arm-r38.py` FAILs 9/10 at **both** revisions on the superseded fixture
> `F06-no-btrfs-root` (`SKILL.md:3318`, historical row), with the live leg and the six-plane count unchanged.
> No counter FAILs at the measured revision where it PASSes at base: the C1 predecessor-counter kill clause does
> not fire, and the live census diff is exactly the declared `SCRUB btrfs-scrub-record …` line added between
> STORAGE and the rollup with the rollup line and exit code unchanged.
