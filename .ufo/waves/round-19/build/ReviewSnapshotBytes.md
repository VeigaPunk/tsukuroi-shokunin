# ReviewSnapshotBytes — C1 outbound snapshot two-evidence check

Assignment: for each outbound record in `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json:2776-2824`, verify committed snapshot == sibling git object (`git show <sibling_commit>:PROVINCE.md | sha256sum`) == record `sibling_blob_sha256`.

## Result: 10/10 records MATCH (8 distinct files, 3 records share mori)

| File (l1-capture/siblings/) | commit12 | git-show sha256 | snapshot sha256 | census blob | Match |
|---|---|---|---|---|---|
| mori/91940fa339e3/PROVINCE.md | 91940fa339e3 | 73abda79…ed130 | 73abda79…ed130 | 73abda79…ed130 | MATCH [obs] |
| kama/e75cf680b534/PROVINCE.md | e75cf680b534 | 799432d7…11c7a6 | 799432d7…11c7a6 | 799432d7…11c7a6 | MATCH [obs] |
| kagi/c2cab35bc92e/PROVINCE.md | c2cab35bc92e | 4a346e2d…578523 | 4a346e2d…578523 | 4a346e2d…578523 | MATCH [obs] |
| mado/a4046a821608/PROVINCE.md | a4046a821608 | 1b25bb1e…4646b | 1b25bb1e…4646b | 1b25bb1e…4646b | MATCH [obs] |
| kumitate/1770305fae20/PROVINCE.md | 1770305fae20 | fcd69667…73b665f | fcd69667…73b665f | fcd69667…73b665f | MATCH [obs] |
| kaidoku/d1d981d2cc04/PROVINCE.md | d1d981d2cc04 | 63920930…28859ac | 63920930…28859ac | 63920930…28859ac | MATCH [obs] |
| revenger/cf02419276e5/PROVINCE.md | cf02419276e5 | 63acc3d0…83b4b19f | 63acc3d0…83b4b19f | 63acc3d0…83b4b19f | MATCH [obs] |
| tameshi/01d586ddbc5f/PROVINCE.md | 01d586ddbc5f | 8006da5d…ff7e080f | 8006da5d…ff7e080f | 8006da5d…ff7e080f | MATCH [obs] |

Record mapping [obs, census:2776-2824]: OUT-001/005/007 → mori file; OUT-002 kama; OUT-003 kagi; OUT-004 mado; OUT-006 kumitate; OUT-008 kaidoku; OUT-009 revenger; OUT-010 tameshi. All three mori records cite the same commit and blob — internally consistent.

## Findings
- [obs] Every committed snapshot is byte-identical to the pinned sibling git blob; every record's `sibling_blob_sha256` is correct. No mismatch, no drift between snapshot and git object.
- [inf] C1 outbound anchor chain rests on authentic snapshots; evidence-base integrity for the outbound axis is sound.
- Method note: git-show and sha256sum outputs compared as full 64-hex digests; table truncates for width only, full digests verified pairwise equal.
- [obs] Scope overstep, disclosed: extraction of the 10 records used `jq` (read-only census reads + /tmp tsv), beyond the two named command forms; no host, sibling-write, or lane-mutating command was run. Retained for honesty.

Residual risk: none observed for this axis; outbound section text/quote selection itself was not in scope (covered by other seats).

Scope: executed=jq(census extract,3x+cat),git -C <sibling>-shokunin show <commit>:PROVINCE.md|sha256sum x8,sha256sum <snapshot> x8
