VERDICT: supports

# C1ExecPriorCounters — item C1-6 (kill rule: prior counters)

Kill-rule clause checked: "the round-42 C1 counter / census selftest regresses". Both prior
instruments pass at the implementation commit, and both files are byte-identical between base
6951ead9 and implementation 717b716, so this wave neither broke nor silently redefined the
round-42 C1 evidence. The clause holds; nothing to escalate.

## 1. Round-42 C1 counter at 717b716 — PASS

Command (from the lane root, TMPDIR in scratch), exactly as assigned:

```
python3 tools/run-receipt.py --revision 717b716a8943151ace8657e0ca23d7d9b8434f26 \
  --tool-revision 717b716a8943151ace8657e0ca23d7d9b8434f26 \
  --out /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-43/w1/C1ExecPriorCounters/r42-c1-717b716.jsonl \
  -- tools/score-size-invariance-r42.py --revision '{rev}' \
     --scratch /fast/scratch/hyaku/tsukuroi-r43/C1ExecPriorCounters/s
```

Observed:

- Header (`.ufo/waves/round-43/w1/C1ExecPriorCounters/r42-c1-717b716.jsonl:1`): `revision` =
  `tool_revision` = `717b716a8943151ace8657e0ca23d7d9b8434f26`; `tool_sha256`
  `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03`, equal to
  `sha256sum tools/score-size-invariance-r42.py` at the worktree.
- Body (`:2`): `"verdict": "PASS"`, `cases` 10, `invariant` 10, `ns_cases`
  N1/N3/N6 all `"invariant": true`, `selftest_pass` 1, `default_equal` 1,
  `selftest_label` `"PASS (132 cases, 132 passed, 0 failed)"`, `selftest_rc` 0.
- Footer (`:3`): `"exit_code": 0`, `"timed_out": false`, `"stderr_tail": ""`.
- Runtime: receipt spans `2026-10-26T22:08:05Z` → `2026-10-26T22:09:01Z` (56 s);
  measured wall 57.99 s (58.35 s including process echo). One heavy counter was run at a time.

No regression against the round-42 tip: the same frozen tool at 4476620 produced PASS with the
same predicate fields
(`.ufo/waves/round-42/w1/C1ExecRerun/c1-after-4476620.jsonl:2`: `"verdict": "PASS"`, cases 10,
invariant 10, `default_equal` 1, `selftest_label` `"PASS (130 cases, 130 passed, 0 failed)"`).
The label rose 130 → 132 because the census itself gained two selftest cases after 4476620 and
before base 6951ead9 — the census blob at the base equals the one at 717b716 (§3) — not because
of this wave; the counter's predicate does not read the case count.

## 2. Census `--selftest` at 717b716 — PASS (132 cases, 132 passed, 0 failed)

The census was extracted from the revision rather than read from the worktree:

```
git show 717b716a8943151ace8657e0ca23d7d9b8434f26:tools/tsukuroi-census.sh > $S/census-717b716.sh
git hash-object $S/census-717b716.sh   # 18a1db6448358d7ecf4634570fcd2bf075eccb1b = rev blob
sha256sum $S/census-717b716.sh         # 7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9
bash $S/census-717b716.sh --selftest   # TMPDIR=$S
```

Observed: exit 0, wall 36.486 s. Final line
(`.ufo/waves/round-43/w1/C1ExecPriorCounters/census-selftest-717b716.out:135`):
`TSUKUROI_CENSUS_SELFTEST: PASS (132 cases, 132 passed, 0 failed)` — the exact expected label.
132 lines begin `PASS `; `grep -n FAIL census-selftest-717b716.out` matched nothing.
Runtime metadata in `census-selftest-717b716.meta`; content hash in `census-717b716.sha256`.

## 3. Census (and counter) unchanged base → implementation

`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --quiet
6951ead90566b2d74f7c45b4efca29246badad64 717b716a8943151ace8657e0ca23d7d9b8434f26 --
tools/tsukuroi-census.sh` → exit 0.

Blob identity, both commits:

| path | blob |
|---|---|
| `tools/tsukuroi-census.sh` | `18a1db6448358d7ecf4634570fcd2bf075eccb1b` (base = impl) |
| `tools/score-size-invariance-r42.py` | `bf7c16bdba29fe972848c1cc853248b0e62bb132` (base = impl) |

The base→implementation diff is 50 files (46 added, 4 modified:
`corpus/knowledge/btrfs-scrub-record-r43.md`, `tools/boot-chain-audit.sh`,
`tools/check-scrub-record-r43.py`, `tools/score-bootinputs-r43.py`); a name-only grep confirms
neither prior C1 instrument is in that changed set. So the two instruments exercised above are
the same bytes the round-42 wave closed on, and the C1 change is confined to
`tools/boot-chain-audit.sh` (37 +/− lines) — its function-scope review is a different item, not
claimed here.

## Not run / limits

- I did not rerun the counter at the base or at 4476620; the round-42-tip comparison is that
  wave's existing receipt (`C1ExecRerun/c1-after-4476620.jsonl`), not a fresh run.
- I did not run the census in live mode; this item asks for `--selftest` only.
- Side-check only, not evidence: package and service state were not touched; no git/jj mutation
  was run in the lane. All runs used `TMPDIR` and `--scratch` under
  `/fast/scratch/hyaku/tsukuroi-r43/C1ExecPriorCounters/`; the scratch tree (including
  run-receipt's sandbox clone and the counter's scratch dir `s`) was deleted after copying
  receipts into the seat directory.

## Proposed receipt text (LOG/SCORECARD)

> Kill rule at 717b716a8943151ace8657e0ca23d7d9b8434f26: round-42 C1 counter PASS (10/10 cases,
> 10/10 invariant, ns N1/N3/N6, default_equal 1; receipt
> `.ufo/waves/round-43/w1/C1ExecPriorCounters/r42-c1-717b716.jsonl`) and census `--selftest`
> PASS (132 cases, 132 passed, 0 failed); `tools/tsukuroi-census.sh` and
> `tools/score-size-invariance-r42.py` byte-identical to base 6951ead9 (`git diff --quiet`
> exit 0).

Report path: `.ufo/waves/round-43/w1/C1ExecPriorCounters.md`
Receipts: `.ufo/waves/round-43/w1/C1ExecPriorCounters/` (`r42-c1-717b716.jsonl`,
`census-selftest-717b716.out`, `census-selftest-717b716.meta`, `census-717b716.sha256`,
`checks.txt`).
