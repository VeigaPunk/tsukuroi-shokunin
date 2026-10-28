VERDICT: supports

# R50ExecAnchorContent — C3-B1: the nine ADJ anchors re-derived by content

Frozen bytes under test: revision `8029cdba1049df25632c91a23c8db4eefb54be5f` (lane
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`). Frozen `PROVINCE.md` sha256
`177cd834a0d9a63375979c21fbf143d5fa588987f45cfdac07a44a35a895e1cd`; frozen
`corpus/knowledge/adjacency-anchors-r19.json` sha256
`bcf6ac93434dddf3ee96a804cde896bf085b320573b917956b21ee059c95feb1`.

I re-derived every anchor independently of `tools/check-adjacency-table-r50.py`
(that counter was **not run** — see "Not done"). Every content leg holds for all
nine OUT ids the ADJ table names (`OUT-002`..`OUT-010`, ADJ rows at
`PROVINCE.md:46-52`), and for the Core row `OUT-001` (`PROVINCE.md:121`).

## Method (commands actually run)

Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50ExecAnchorContent` (`TMPDIR` set to it;
free space 542 G on `/fast`). Frozen reads:

```
git -C .../tsukuroi-shokunin show 8029cdb...:PROVINCE.md > PROVINCE.md
git -C .../tsukuroi-shokunin show 8029cdb...:corpus/knowledge/adjacency-anchors-r19.json > adjacency-anchors-r19.json
python3 rederive.py          # parses both, then for each OUT id:
                             #   git -C <sib> cat-file -t <commit>
                             #   git -C <sib> show <commit>:PROVINCE.md | sha256
                             #   git -C <sib> rev-parse HEAD ; git -C <sib> merge-base --is-ancestor <pin> <tip>
                             #   git -C <sib> show <tip>:PROVINCE.md   (live quote leg)
                             #   git -C <sib> diff --unified=0 <pin> <tip> -- PROVINCE.md
```

All sibling git calls are read-only (`cat-file`, `show`, `rev-parse`, `merge-base`,
`diff`); no sibling or lane write, no git mutation anywhere. Sibling repos and the
tips observed at run time (2026-10-28):

| sibling | repo | live tip |
|---|---|---|
| mori | `/home/vgpnk/Projects/shokunin/mori-shokunin` | `325f7e639916fcbc77fa2ec7475951a1b86bb1cb` |
| kama | `.../kama-shokunin` | `7ee8cbdf160f8c945954e4737e7a2f797e3b2987` |
| kagi | `.../kagi-shokunin` | `69b61db46be4ed955994f6f1d1cba522bc5f4e97` |
| mado | `.../mado-shokunin` | `3b55b6e91e40f455dd56b2985e4ffc087ada92d5` |
| kumitate | `.../kumitate-shokunin` | `14057f3e3899180c95713bace088fb9c0d0046e3` |
| kaidoku | `.../kaidoku-shokunin` | `04f9d4b7698deb9bff04380e781ae5090ea9bb76` |
| revenger | `.../revenger-shokunin` | `6defe31e4af9f7b3780b2942f1e4e325f6d53cbc` |
| tameshi | `.../tameshi-shokunin` | `c3e2ca9f020776b3d66c7af854fb82c834674fcf` |

## Per-id table

Legs: **C** = registry `sibling_commit` exists as a commit in the sibling repo;
**D** = `sha256(git show <commit>:PROVINCE.md)` == registry `sibling_blob_sha256`;
**H** = anchor heading cell present as the sibling's exact title line (line 1);
**Q@pin** = quote cell is a verbatim substring of the pinned blob (line);
**CLS** = ADJ class in the anchor row == ADJ class that names this OUT id in the
ADJ table; **ANC** = pin is an ancestor of the live tip; **Q@live** = quote still
verbatim in the live tip bytes (line); **occ** = occurrences of the quote in the
blob (pin / live).

| OUT | ADJ | sibling @ pin | C | D | H | Q@pin | CLS | ANC | Q@live | occ | live tip |
|---|---|---|---|---|---|---|---|---|---|---|---|
| OUT-002 | ADJ-01 | kama @ `e75cf680b53484a61709ee1b2787d8dbc6419f74` | ok | ok | ok (1) | ok (12) | ADJ-01 | ok | ok (12) | 1/1 | `7ee8cbdf160f` |
| OUT-003 | ADJ-02 | kagi @ `c2cab35bc92e57e39e5489bac3386db078345b3f` | ok | ok | ok (1) | ok (3) | ADJ-02 | ok | ok (3) | 1/1 | `69b61db46be4` |
| OUT-004 | ADJ-03 | mado @ `a4046a8216080d4004de3f268c62cf142095ac07` | ok | ok | ok (1) | ok (6) | ADJ-03 | ok | ok (6) | 1/1 | `3b55b6e91e40` |
| OUT-005 | ADJ-04 | mori @ `91940fa339e38006f8db5bd7d78bb6f037f4d016` | ok | ok | ok (1) | ok (8) | ADJ-04 | ok | ok (8) | 1/1 | `325f7e639916` |
| OUT-006 | ADJ-05 | kumitate @ `1770305fae20826b39905a8251ddeca6b4957ac4` | ok | ok | ok (1) | ok (3) | ADJ-05 | ok | ok (3) | 1/1 | `14057f3e3899` |
| OUT-007 | ADJ-05 | mori @ `91940fa339e38006f8db5bd7d78bb6f037f4d016` | ok | ok | ok (1) | ok (12) | ADJ-05 | ok | ok (12) | 1/1 | `325f7e639916` |
| OUT-008 | ADJ-06 | kaidoku @ `d1d981d2cc041dda4656c5b01d2c8445d8d17124` | ok | ok | ok (1) | ok (3) | ADJ-06 | ok | ok (3) | 1/1 | `04f9d4b7698d` |
| OUT-009 | ADJ-06 | revenger @ `cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97` | ok | ok | ok (1) | ok (3) | ADJ-06 | ok | ok (3) | 1/1 | `6defe31e4af9` |
| OUT-010 | ADJ-07 | tameshi @ `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` | ok | ok | ok (1) | ok (7) | ADJ-07 | ok | ok (7) | 1/1 | `c3e2ca9f0207` |
| OUT-001 (Core) | Core | mori @ `91940fa339e38006f8db5bd7d78bb6f037f4d016` | ok | ok | ok (1) | ok (9) | n/a | ok | ok (9) | 1/1 | `325f7e639916` |

Aggregates: commit exists 10/10; digest == registry 10/10; heading exact title 10/10;
quote verbatim at pin 10/10 (9/9 among the ADJ-named ids); ADJ class match 7/7 ADJ
rows; pin ancestor of tip 10/10; quote verbatim at live tip 10/10 (9/9 ADJ-named).
Registry `quote_line` equals the observed line for 10/10.

## Additional legs I ran (beyond the four the item names)

1. **Registry pointer ranges contain the quoted line** — 10/10. `province_pointer`
   ranges (`../mori-shokunin/PROVINCE.md:6-16` etc.) contain the observed quote line
   for every id (e.g. OUT-007 pointer `12-16`, quote at 12; OUT-003 pointer
   `3-6,10-17,32-34,54`, quote at 3).
2. **Registry snapshot blobs in the lane match the registry digests** — 10/10.
   `git show 8029cdb...:<snapshot>` for each `outbound[].snapshot`
   (`.ufo/waves/round-19/l1-capture/siblings/<sib>/<abbrev>/PROVINCE.md`) hashes to
   the registry `sibling_blob_sha256`, so the lane carries the same bytes the pins
   name.
3. **Portable digest list** (`PROVINCE.md:137-146`) — 10/10 entries carry the full
   40-hex commit and the 64-hex sha256, both equal to the registry fields and to the
   observed blob digest; abbreviated commits in the table (col 3) are prefixes of the
   registry full commits 10/10.
4. **Live leg is a genuinely different blob** — `live_digest != pin_digest` for all
   eight siblings (10/10 anchors), so the live quote leg is not a re-read of the
   pinned bytes.
5. **Pin→tip diffs are additive and touch no anchor** — `git diff <pin> <tip> --
   PROVINCE.md` removed 0 (kama, mado, tameshi), 1 (revenger: `npx -y
   rea-agents@6.4.0` → `@6.5.0`), 3 (kumitate: three "queued" SOURCES rows), 5
   (kagi: old gate list, re-written round 21), 5 (kaidoku: old PE/REA rows), 7
   (mori: old R12/kaika bullets). No removed line contains any anchor quote, and the
   live line for every anchor is byte-identical to its pinned line.

## Anchors that survive only formally

Nine of nine are **content** anchors: the digest leg binds exact bytes at a commit
that exists in the sibling, and the quote occurs exactly once in that blob and once
in the live tip. Nothing here is a line-number-only locator. Three qualifications,
all of them properties of the quoted *text*, not failures:

- **Heading leg is formal-only by construction.** All ten headings are the sibling
  file's title line (`heading_line == 1`, exact string equality) — this is stated in
  the lane's own limits paragraph (`PROVINCE.md:132`: "Every heading above is the
  sibling file's title heading because the cited ownership text sits in its
  preamble"). A heading therefore locates nothing on its own; the locating force is
  entirely the quote + digest legs. This is disclosed, not hidden.
- **OUT-009 is the one anchor whose support is partly formal.** Its quote ("Owns:
  reverse engineering of shipped artifacts") is verbatim at pin (revenger line 3) and
  at live tip (line 3), but the lane's own `## R20 ownership clarification — OUT-009`
  (`PROVINCE.md:148-152`) supersedes "only the OUT-009 proposition's unqualified
  'Revenger owns' wording and its broad 'packages' paraphrase" and records that
  "ADJ-06's unresolved recipient and Frontier arbitration remain controlling". The
  bytes survive; the proposition they once supported is narrowed, so OUT-009 anchors
  a declaration, not an assigned owner.
- **Four quotes are mid-line fragments** (verbatim and unique, but syntactically
  cut, so the full claim needs the neighbouring lines): OUT-002 is a table cell
  (`| served-model-id reconciliation | `GET /v1/models` vs `--alias` vs the
  configured model id |`); OUT-004 ends at a list comma (`**Owns (surfaces):**
  `~/.config/hypr/` (hyprland.conf, keybinds, rules,` — the list continues on line
  7); OUT-007 ends at `OS package,` (continues line 13); OUT-005 begins mid-sentence
  after `pair); ` and ends at `records from` (mori line 8). Each still names the
  operative clause, and each is unique in the blob, so the locator is exact — but a
  reader who takes the quote as a complete sentence would be reading a fragment.

No anchor is falsified: no missing commit, no digest mismatch, no absent heading, no
absent or relocated quote, no class mismatch, no non-ancestor pin, no quote lost
between pin and live tip.

## Not done

- I did **not** run `python3 tools/check-adjacency-table-r50.py --revision <REV>`:
  my execution class authorises only the reads above. My independent counts are
  compatible with its predicate fields but are not a run of it: `quote_at_pin` = 9/9
  and `live_quote` = 9/9 for the nine ADJ-named ids (`== 9` and `>= 8` in the
  predicate hold on my numbers, unverified by the counter itself).
- I did **not** test `stub_fails` or any mutation of the table; that is another
  seat's leg.
- No selftest-bearing command was run (none applies), so no census timing was spent.

## Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-50/w1/R50ExecAnchorContent/`:
`rederive.py` (the driver, sha256 `fa1ec7729d71cbcf43655cbc66050db017512701a703cd5edc2052f4ceea2b83`),
`rederive.json` (per-id checks, `d28e32549ebd45eb3d806a28ca7731122279194fd49670acb32c5ca8a92046a2`),
`lines.json` (pin/live line text per anchor, `ee6e4b3893a5bcc214b18fef7cf5c7316fe46d85cea8a86fe31667878bf9f982`),
`run.log` (`f997536447e6a99164f73ef622960a3e3d547fd76a547f7e9bc32e0ef0c206cb`).
Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50ExecAnchorContent` removed after copying.
No tool install or upgrade was needed.
