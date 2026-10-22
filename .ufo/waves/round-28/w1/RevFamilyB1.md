# RevFamilyB1 — rule B1 family attack, round 28 wave 1

Verdict: holds — every mutant in the B1 family (extra-row-ov7, extra-row-id-trailing-space,
extra-non-dict-rows, unhashable-id-row) is refused by rule B1 itself, not incidentally; no
rescue variant was needed because none of the four is refused "only incidentally."

## Method

Battery run, exactly as assigned, from a read-only `git archive` export of
f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 at /fast/scratch/hyaku/tsuku28/RevFamilyB1/tree:

    TMPDIR=/fast/scratch/hyaku/tsuku28/RevFamilyB1/tmp \
    python3 tools/mutants-adjacency-overlap.py \
      --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
      --base f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 \
      --counter-rev f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 --keep

Full output: /fast/scratch/hyaku/tsuku28/RevFamilyB1/battery.out (exit 0; summary line:
`should_fail_total` 24, `should_fail_accepted` 0, `accepted_mutants` [],
`control_live_anchored_rows` 6, `control_live_exit` 0, `should_pass_accepted` 4,
`counter_sha256` 450b020b…af25e). Kept sandbox:
/fast/scratch/hyaku/tsuku28/RevFamilyB1/tmp/mut-adj-a4knz_8y (sbx/, nosib/, counter/).

B1 mechanism (counter source at the attack revision, exported tree lines 124–127 and 235–237
of tools/check-adjacency-overlap.py): `shape_errors` collects `rowN-not-object` /
`rowN-id-not-declared` for any row that is not an object or whose `id` is not one of the
strings OV1..OV6, and `if sibling_note == 'sibling-mismatch' or shape_errors: anchored = 0`
forces the count to zero. Per-row reasons attached to a non-OV* key can never reduce
`anchored`, because `anchored = sum(1 for rid in IDS if ids.count(rid) == 1 and not
result.get(rid))` sums only over the six declared ids.

## Findings

1. extra-row-ov7 — refused by B1 itself, exclusively. [obs] Battery JSON (battery.out, mutant
   line): `accepted: false`, `anchored_rows` 0 in both runs; `failing` carries only the `OV7`
   key (`id-unknown, class-invalid, owner-invalid, action-empty, province-row-missing`) —
   every OV1..OV6 row is clean. Direct counter re-run on kept commit
   2543505679499490f55467ee2815b11f551d5a63 shows `shape_errors: ["row6-id-not-declared"]`.
   With the `or shape_errors` clause stripped from a scratch copy of the counter
   (/fast/scratch/hyaku/tsuku28/RevFamilyB1/variants/counter-noB1.py), the same commit yields
   exit 0, anchored_rows 6 under both the live mori root and the empty root — so no other
   rule contributes. [obs] Note: the mutant's deliberately invalid class/owner/action on OV7
   are dead weight for refusal; `row6-id-not-declared` alone triggers B1.
2. extra-row-id-trailing-space — refused by B1 itself, exclusively. [obs] `failing` key is
   `"OV4 "` with only `id-unknown, province-row-missing`; all six declared ids are clean and
   each still occurs exactly once (`"OV4 " != "OV4"` under `==`, so no `id-duplicate` is even
   raised). `shape_errors: ["row6-id-not-declared"]` on kept commit
   1a2cf8e2e35427f4461a635491c4eccf12f58d87; stripped counter → exit 0, anchored 6 both roots.
3. extra-non-dict-rows — refused by B1 itself, exclusively. [obs] `failing: {}` (non-object
   rows are skipped before per-row checks and produce no `result` entry at all);
   `shape_errors: ["row6-not-object", "row7-not-object"]` on kept commit
   f28f54b85b8bb846d2305ee2f07e9bc58b6950a4. Stripped counter → exit 0, anchored 6 both roots.
   [obs] This mutant is the purest demonstration: zero per-row diagnostics, refusal comes
   solely from `shape_errors`.
4. unhashable-id-row — refused by B1 itself, exclusively. [obs] `failing` key `row6`
   (positional fallback key since `id` is the list `["OV1"]`) with `id-unknown,
   province-row-missing`; OV1..OV6 all clean. `shape_errors: ["row6-id-not-declared"]` on
   kept commit 1d329f45805871aee0fec2fa170d6ab2ea415427; stripped counter → exit 0,
   anchored 6 both roots. [obs] No crash: `r.get('id') not in IDS` and `ids.count(rid)` use
   `==` against strings, never hashing, so the list id is safe — it counts as 0 duplicates,
   so only `id-unknown` (not `id-duplicate`) fires.

5. Incidental-refusal check for the whole family. [inf] For each mutant, all six declared ids
   have empty per-row reason lists and `sibling_check` is `sibling-verified` /
   `sibling-unavailable` (never `sibling-mismatch`), so the only term that can zero
   `anchored` is `shape_errors`. The stripped-counter experiment confirms causality directly:
   removing B1's zeroing makes all four mutants fully accepted under both sibling roots.
   Therefore no mutant in this family is refused "only incidentally," and no rescue variant
   of a mutant was required or built; the only sandbox variant constructed was the
   B1-stripped counter used as the control experiment, which confirmed B1 alone refuses each
   mutant.

6. Residual gap, out of the declared register but worth noting. [inf] `shape_errors` is
   computed from `rows` as loaded by `json.loads(raw.decode('utf-8'))['rows']`; a register
   whose top-level `rows` is a dict (object) instead of a list — e.g. `{"rows": {"OV7": {…},
   "OV1": {…}, …}}` — would pass `assert isinstance(rows, list)`? No: the assert catches it
   and returns exit 2 `register-unreadable`, which is a refusal anyway (exit ≠ 0). [unk] A
   `rows` list containing exactly the six valid rows *plus* duplicate ids appears covered by
   A1 (`ids.count(rid) != 1` → `id-duplicate` on both copies), independently of B1 — the
   duplicate family is assigned to another reviewer. No exploitable hole found inside the B1
   perimeter.

Scope: read=lane SCORECARD.md round-28 declaration, tools/check-adjacency-overlap.py and
tools/mutants-adjacency-overlap.py at f8e3a8f2 (via git-archive export), battery JSON output;
wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/w1/RevFamilyB1.md,
scratch files under /fast/scratch/hyaku/tsuku28/RevFamilyB1/ (tree export, battery.out,
kept sandbox tmp/mut-adj-a4knz_8y, variants/counter-noB1.py);
executed=battery command above, four counter re-runs on kept mutant commits, eight
stripped-counter control runs, git reflog/rev-parse read-only queries on the sandbox repo
Model: not exposed
Installs: none
