VERDICT: supports

# C1ExecPriorStorage — item C1-5: the predecessor storage counters at base and at the round-45 implementation

Kill rule scored: **"a predecessor census counter goes PASS → FAIL"** (`SCORECARD.md:2863`, kill-rule cell; the
cell names six predecessor counters — `score-scrub-arm-r44.py`, `score-storage-arm-r38.py`,
`score-storage-arm-r38-q82.py`, `score-storage-hidden-r39.py`, `score-size-invariance-r42.py`,
`score-bootinputs-r43.py`). This seat ran exactly the three the item names. No predecessor counter changes
verdict between base and implementation; **the clause does not fire**.

Base `5bbd5ff588120fd8e7c744695351a6978b4241c1` (lane tip at round start); implementation
`18389f44cf6ce414d7be205998b29c79fb0b490c`. Both are ancestors of `refs/heads/master`
(`git merge-base --is-ancestor … master` → both true; master tip at run time `3c42f556`), so every
`_revision.bind` succeeded (no counter exited 2 for binding).

## Method

Every run went through the frozen runner, one counter at a time, from a private `git clone --no-local` of the
lane at the measured revision (the receipt header records that revision), with `TMPDIR` and the counters'
`--scratch` inside my scratch dir:

```
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecPriorStorage
TMPDIR=$S/tmp python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/run-receipt.py \
  --revision <REV> --out /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-45/a2w1/C1ExecPriorStorage/<tool>-<rev8>.jsonl \
  -- tools/<tool> --revision '{rev}' --scratch /fast/scratch/hyaku/tsukuroi-r45/C1ExecPriorStorage/s
```

All three tools accept `--scratch` (`add_argument('--scratch', default=None)`: `tools/score-storage-arm-r38.py:181`,
`tools/score-storage-arm-r38-q82.py:90`, `tools/score-storage-hidden-r39.py:169`), so nothing was built under
`/tmp`. Each counter `mkdtemp`s its work tree inside that scratch dir and removes it on exit.

**Tool version is not a confound:** each tool's bytes are identical at base and at implementation, both as
measured (`tool_sha256` equal in the two receipt headers) and independently (`git show <REV>:tools/<tool> |
sha256sum`):

| tool | sha256 at base and at implementation | working-tree sha256 |
|---|---|---|
| `tools/score-storage-arm-r38.py` | `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218` | same |
| `tools/score-storage-arm-r38-q82.py` | `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3` | same |
| `tools/score-storage-hidden-r39.py` | `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973` | same |

## Results (receipts in `.ufo/waves/round-45/a2w1/C1ExecPriorStorage/`)

| counter | base `5bbd5ff5` | impl `18389f44` | verdict delta |
|---|---|---|---|
| `tools/score-storage-arm-r38.py` | **FAIL** exit 1 — `fixtures_matched` 9/10, `live_match` 1, `six_planes_all` 1, `euid_root` false (`score-storage-arm-r38-5bbd5ff5.jsonl`) | **FAIL** exit 1 — `fixtures_matched` 9/10, `live_match` 1, `six_planes_all` 1, `euid_root` false (`score-storage-arm-r38-18389f44.jsonl`) | **none** (both FAIL, identical legs) |
| `tools/score-storage-arm-r38-q82.py` | **PASS** exit 0 — `ns_views_matched` 3/3, `ns_available` 1 (`score-storage-arm-r38-q82-5bbd5ff5.jsonl`) | **PASS** exit 0 — `ns_views_matched` 3/3, `ns_available` 1 (`score-storage-arm-r38-q82-18389f44.jsonl`) | **none** |
| `tools/score-storage-hidden-r39.py` | **PASS** exit 0 — `hidden_matched` 2, `views_matched` 3, `fixtures_matched` 5, `live_match` 1, `six_planes_all` 1 (`score-storage-hidden-r39-5bbd5ff5.jsonl`) | **PASS** exit 0 — identical conjuncts (`score-storage-hidden-r39-18389f44.jsonl`) | **none** |

Wall times (one at a time, never two C1-class counters concurrently): r38 25.7 s / 27.4 s, q82 10.4 s / 11.0 s,
r39 33.2 s / 32.6 s.

## Every changed field, base vs implementation

A structural walk of the two receipt bodies per tool (`summary.json` was generated from the same parse) reports
**only** these differences; no predicate conjunct, no `match` flag and no exit code moves:

- `score-storage-arm-r38`: `/revision` — **1 diff total**. All ten fixtures, their `expected`/`got`/`six_planes`/
  `census_exit`, and the live leg are byte-identical strings at both revisions.
- `score-storage-arm-r38-q82`: `/revision`, `/seed`, and the seed-derived random view draws —
  `/views/{0,1,2}/expected`, `/views/{0,1,2}/got`, `/views/{0,1,2}/storage_lines/0` — **21 diffs**. These are the
  counter's own `os.urandom(16)` view construction (`score-storage-arm-r38-q82.py:104-118`): base drew
  `HEALTHY 3/6/0, DEGRADED 1/1/3, DEGRADED 2/4/8`, impl drew `HEALTHY 1/3/0, DEGRADED 3/6/12, DEGRADED 3/7/20`;
  in both runs `got == expected` in all three views and `ns_available` 1.
- `score-storage-hidden-r39`: `/revision`, `/seed`, and the same class of seed-derived view draws
  (`/views/1`, `/views/2`) — **9 diffs**. The H1/H2 hidden legs, all five override fixtures, the live leg and
  every `census_exit` are byte-identical at both revisions (H1/H2 both
  `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs`).

No other field changes, including `census_exit` on all 10 + 3 + 7 legs (2 everywhere at both revisions — the
census exits with its rollup: `HEALTHY 0 / DEGRADED 1 / BLOCKED 2`, `tools/tsukuroi-census.sh` (base) `:3435-3438`).

## The r38 v1 FAIL is pre-existing declared staleness, not a base → impl delta

- The single mismatch is `F06-no-btrfs-root` **at both revisions**: expected `HEALTHY 0/0/0`, got
  `BLOCKED 0/0/0` (`detail=mounts:btrfs-without-sysfs` on the STORAGE line). The fixture encodes the superseded
  R38-ABSENT-ROOT rule; the round-39 declaration predicted exactly this and this reading:
  `SCORECARD.md:2232-2234` — "Predicted side effect, declared now: the round-38 v1 counter's fixture F06 …
  encodes the superseded R38-ABSENT-ROOT rule, so at post-C1 revisions it reads BLOCKED and
  `score-storage-arm-r38.py` FAILs 9/10 by construction; the round-38 claim stays measured at `b0005ae9`"
  (observed at `SCORECARD.md:2256`).
- The tool is HISTORICAL outside a two-blob pin: `SKILL.md:3318` row `historical-storage-arm-r38-f06` —
  "HISTORICAL at fixture `F06-no-btrfs-root` only. Read only where `tools/tsukuroi-census.sh` is blob
  `119b645349b5eadf182aaa473d2fac38eadea45a` … or `8ef604c001ae2b2edc1598a6dd3877f30dc13de5`".
  Verified: `git rev-parse 52ffd65f:tools/tsukuroi-census.sh` → `119b6453…`, `02eeed07`/`b0005ae9f56f` →
  `8ef604c0…`; **our** blobs are `a7a4fa3d9bd90c903b151341ce660021eab93f02` (base) and
  `f129a18e19106ea4fe7927dc4191477fbfc4077c` (impl), i.e. outside the pin at both ends — so this FAIL is not a
  usable regression reading in either direction, and it is identical at base.
- Same measurement, same conclusion, one round earlier:
  `.ufo/waves/round-44/w2/C1ExecFinalPrior.md:27,48-60` records FAIL 9/10 at both round-44 ends and the
  reasoning ("base FAILs with the identical fixture set and identical live leg, so the clause does not fire").

## Cross-check that the two PASSing counters are not blind to a live plane change

Outside this item's predicate I ran the census itself twice per revision from a scratch clone (`env -i
PATH=/usr/bin:/bin LC_ALL=C HOME=… TMPDIR=…`, no `TSUKUROI_*` override), because the C1 kill rule also fires on a
line-shape or live-exit-code change:

- exit code **2 in all four runs** (base runs 1/2, impl runs 1/2) — unchanged base → impl.
- `diff base-run1 base-run2` and `diff base-run1 impl-run1` differ **only** in the header timestamp and
  `PLANE drivers` `C6_psi_full_total_us`, `C6_avail_kb`, `C6_shmem_kb` — fields that drift between two runs of
  the *same* revision (69985014 → 69985021 µs within base; 19365476 → 19293020 kB), i.e. the live drift the rule
  permits.
- All six `PLANE` states, both `HANDOFF` lines, the `DRIFT` line, the `STORAGE` line
  (`state=HEALTHY filesystems=1 devices=1 nonzero=0`), the `SCRUB` line (`state=NONE dir=absent …`) and
  `TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=BLOCKED drivers=DEGRADED journal=DEGRADED
  update-safety=BLOCKED oom=DEGRADED)` are identical base vs impl. Captures:
  `live-census-{base,impl}-run{1,2}.txt`.
- The census blobs differ only in the five converted readers plus the six `(R45-C1)` selftest cases:
  `census-base-vs-impl.diff` — 5 removed lines, 49 added lines, and **no line mentioning `STORAGE`, `SCRUB` or
  `btrfs` is touched**. Blob sha256 `17c82406…` (base) → `237b21c9…` (impl).

## Receipts (all in `.ufo/waves/round-45/a2w1/C1ExecPriorStorage/`)

| file | sha256 |
|---|---|
| `score-storage-arm-r38-5bbd5ff5.jsonl` | `0f713f350c594cb011bbaab5e2adaf4db10bdb45ffa4255ccaa40d12c66515db` |
| `score-storage-arm-r38-18389f44.jsonl` | `6125aea6914723497be970b5d94c1051d924d025a69810b5cd8bb8d408ffa3c0` |
| `score-storage-arm-r38-q82-5bbd5ff5.jsonl` | `308e45ac612d272263eb8b9c98b8fa515a50137d6b4864b86a30c031954568a1` |
| `score-storage-arm-r38-q82-18389f44.jsonl` | `0c06f45210439f53a4d353dee133fa43e417f1066a3e82720f3b9fc0364f7395` |
| `score-storage-hidden-r39-5bbd5ff5.jsonl` | `5bb57230b30f3c9a9e9a4bb95f6e2c6086fb98e98c51b3da2c0836c7cc5f6992` |
| `score-storage-hidden-r39-18389f44.jsonl` | `46d1606cc6727d4689a38c2f241b062f16ac8ac33371067c804645ed2864f2e5` |
| `summary.json` | machine digest of the three rows above (results, predicate fields, per-file sha256) |
| `live-census-{base,impl}-run{1,2}.txt` | the four live census captures quoted above |
| `census-base-vs-impl.diff` | `diff -u` of the two census blobs |

## What I did not do (limits of this report)

- I did **not** run the other three predecessor counters named in the same kill cell
  (`score-scrub-arm-r44.py`, `score-size-invariance-r42.py`, `score-bootinputs-r43.py`) — other seats' items.
  The clause is therefore covered by this seat only for the three storage counters.
- I did not run the round-45 C1 counter `tools/score-census-readers-r45.py`, any mutant battery, or any
  fidelity/adjacency leg; other seats own those. No build, lint or test gate was run (main agent's job).
- I installed and upgraded nothing (no `pacman`/`uv`/`npx` transaction; no tool version changed), so this
  report has no tooling-authorization entry.
- All six counter runs are single-sample per revision; the seed-derived draws are freshly random each run by
  design and are reported as differences, not as drift. Live-plane stability was sampled twice per revision.
- Scratch `/fast/scratch/hyaku/tsukuroi-r45/C1ExecPriorStorage` (including `s/`, `tmp/` and the fixture clone
  `fx.*`) was removed after the receipts above were copied into the seat dir. Each of my six `run-receipt.py`
  invocations removed its own `run-receipt-*` clone/home in its `finally`; the `run-receipt-*` trees still under
  `/fast/scratch/hyaku` belong to concurrently running sibling seats (mtimes 23:51–00:28 local, none in my runs'
  00:25–00:27 window) and were left untouched.
