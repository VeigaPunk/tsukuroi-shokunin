# E2SibHeads — C2-LOCATE summary (round 66, w1)

UTC stamp of the locating pass: 2026-11-03T20:59:23Z (scratch creation) …
2026-11-03T21:00:09Z (probe receipt header).
Register read: `corpus/knowledge/adjacency-anchors-r19.json` (authoritative; 10 outbound anchors OUT-001..OUT-010).
Lane base commit for this round: `c68bfe97`; lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

## Result: 10 / 10 located at each sibling's live HEAD

Counting command and its verbatim output:

```
$ awk -F'\t' 'NR>1{c[$6]++} END{for(k in c) print k, c[k]}' \
    /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-66/drafts/c2-anchors-live.tsv
located 10
rc=0
```

```
$ awk -F'\t' 'NR>1' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-66/drafts/c2-anchors-live.tsv | wc -l
10
rc=0
```

| status | count |
|---|---|
| located | 10 |
| unlocated | 0 |
| unreachable | 0 |

Every one of the 8 sibling directories answered `git rev-parse HEAD` with rc=0 and
`git -C <D> cat-file -t <HEAD>` printed `commit` with rc=0 (probe file §A). No `git show`
failed, so no anchor is `unreachable`; every file was readable, so no anchor is `unlocated`.

## Normalisation rule (applied before matching, nothing else changed)

1. delete every occurrence of `**`;
2. delete every occurrence of the backtick character `` ` ``;
3. collapse every run of whitespace to a single space, then strip leading/trailing space;
4. case-sensitive substring test, applied line-by-line first, then (as a fallback) across a
   contiguous span of up to 12 lines.

Only steps 1–2 modify characters, and only the two marker kinds the item named. No case
folding, no punctuation folding, no em-dash or arrow substitution, no HTML-entity decoding.
Result of the rule on the two extreme cases:

- OUT-001 register quote `… cgroup \`memory.events\` …` normalises to
  `independently labeled user/system journals, plus cgroup memory.events and the explicit same-boot journal window after a retained anchor;`
  and matches mori `PROVINCE.md:9`. The **un**normalised literal (backticks kept) also matches
  the same line — see probe §E.
- OUT-009 register quote is `Owns: reverse engineering of shipped artifacts` with no markers at
  all; the live revenger line 3 is plain text with no bold, so normalisation is a no-op there and
  the literal also matches (probe §E).

## Locator convention for the C2 rows

`locator` in the claim's row form is `<path>:<line>` taken straight from the TSV's `path` and
`line` columns, e.g. `PROVINCE.md:9` for AR1. All 10 anchors live in the sibling's `PROVINCE.md`,
which is also the register's `province_pointer` target file.

## Cross-check against the register snapshot (drift context only)

`git rev-parse HEAD` at each sibling differs from the register's `sibling_commit` for **all 8**
siblings, and the live `PROVINCE.md` blob sha256 differs from the register's
`sibling_blob_sha256` for all 8 as well (probe §D lists both). The anchor *text* nevertheless
survives unchanged at live HEAD for all 10 anchors, at the same line numbers the register
recorded (`quote_line` 9, 12, 3, 6, 8, 3, 12, 3, 3, 7 — identical to the live `line` column).
So round 66's recheck can cite live HEADs safely; the register's commits are stale pointers, not
stale text.

## Files produced by this seat

- `.ufo/waves/round-66/probes/c2-sibling-heads.txt` — receipts: UTC stamp, §A HEAD + `cat-file -t`,
  §B blob sha256, §C per-anchor location, §D register-vs-live, §E full-quote literal checks, §F rule.
- `.ufo/waves/round-66/drafts/c2-anchors-live.tsv` — 10 data rows + header, columns
  `AR_n, OUT_id, sibling, live_head, blob_sha256, status, line, path`.
- `.ufo/waves/round-66/drafts/e2-summary.md` — this file.

No tracked file, no sibling repo, and no git state was written. Read-only git verbs used:
`rev-parse`, `cat-file`, `show`.
