VERDICT: supports

# C2ExecFinalSources — C2-2 source-registry verification (round 44, hyaku run 9, wave w2)

Seat: leaf executor, item C2-2 ("run `sources-census.sh validate` at tip; verify S242–S245 parse as 11 cells, mined,
used-by names the entry; S237/S240 used-by updated; run `check-knowledge-header.py --revision 8eee79db…`").
Axis: sources / registry and census. I do not touch the counted C2 row verdicts (`C2RevSR<n>`/`C2CritSR<n>`).

Environment. Lane tip at run time `8728e8bcf23eecad46829ad5f0f993b329c35813`; frozen integrated tip
`8eee79db608b5815c325a5af7cbfdeac50eda9f4`; base `98020ece0674e0b569ee23aed10ffbee355b248e`. `corpus/SOURCES.md`
and `corpus/knowledge/btrfs-scrub-record-r44.md` are byte-identical between the tip and the frozen revision
(`git diff --quiet 8eee79db… -- corpus/SOURCES.md corpus/knowledge/btrfs-scrub-record-r44.md` → rc 0), so the
"run at tip" result speaks for the frozen claim on my surface. Scratch `/fast/scratch/hyaku/tsukuroi-r44/C2ExecFinalSources`
(TMPDIR there; removed on exit). No lane tracked file was written; the only lane writes are this report and its receipt
directory. No pacman, no sudo, no scrub, no service/sysfs/mount action, no git/jj mutation in the lane or the fleet root.

## 1. Assigned gate — `sources-census.sh validate` at tip → exit 0

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin tsukuroi        # EXIT=0
```
Output: 40 `W04` duplicate-URL-across-scopes warnings (all pre-existing, S038…S230) and
`tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`. No `E`-codes, empty stderr.
None of S237/S240/S242/S243/S244/S245 appears in the W04 list. Receipt `validate-tip.out`, `validate-tip.err`.

The same registry blob at the frozen revision, run against a faithful fixture (lane symlinked, registry copied so the
E11 disk check reads the committed bytes), is identical: exit 0, the same 40 W04, `ok`, no E-codes.
Receipt `validate-8eee.out` (last line names the fixture registry; E-code count 0).

## 2. The four new rows parse as 11 cells, are mined, and name the entry

Parsed both at the tip worktree and from the committed blob at `8eee79db` (`git show 8eee79db:corpus/SOURCES.md`):

```
S237 NF=11 kind=code     tier=A status=mined opened=2026-10-26 recheck=on-release usedby=r42.md, r43.md, r44.md
S240 NF=11 kind=code     tier=A status=mined opened=2026-10-26 recheck=on-release usedby=r43.md, r44.md
S242 NF=11 kind=code     tier=A status=mined opened=2026-10-26 recheck=on-release usedby=btrfs-scrub-record-r44.md
S243 NF=11 kind=code     tier=A status=mined opened=2026-10-26 recheck=on-release usedby=btrfs-scrub-record-r44.md
S244 NF=11 kind=code     tier=A status=mined opened=2026-10-26 recheck=on-release usedby=btrfs-scrub-record-r44.md
S245 NF=11 kind=own-work tier=A status=mined opened=2026-10-26 recheck=30d         usedby=btrfs-scrub-record-r44.md
```
(used-by shown shortened; full paths are `corpus/knowledge/btrfs-scrub-record-{r42,r43,r44}.md`.) All six rows sit
inside `## Registry` (lines 246–254; `## Paths` starts at 256), so E12 cannot apply. Receipts `rows-tip.txt`,
`rows-8eee.txt`.

`sources-census.sh overdue` shows S242–S244 as `cadence … recheck=on-release` and S245 as `cadence … recheck=30d`
(due 2026-11-25, not overdue on 2026-10-26); the recheck column therefore parses under both modes.
Receipt `overdue-tip.out`.

## 3. Base → frozen tip: exactly these changes, nothing else

Row-set diff of `corpus/SOURCES.md` base `98020ece` vs `8eee79db`:

```
added    S242 S243 S244 S245
removed  (none)
changed  S237 S240 — column 11 (used-by) only
           S237 r42,r43        -> r42,r43,r44
           S240 r43            -> r43,r44
```

Census counters at base → tip: `rows 241 → 245`, `tier.A 226 → 230`, `status.mined 215 → 219`, all other buckets
unchanged (`tier.B 5`, `tier.C 10`, `queued 5`, `rejected 21`, `invalid 0`, `missing 0`). Each new row is counted
exactly once: deleting S245 from a fixture copy moves rows to 244, tier.A to 229, mined to 218.
Receipts `base-census.out`, `census-sensitivity.json`.

## 4. Assigned gate — knowledge-header at the frozen revision → PASS

```
python3 tools/check-knowledge-header.py --revision 8eee79db608b5815c325a5af7cbfdeac50eda9f4   # EXIT=0
```
`status=PASS`, `note_count=65`, `clean_count=65`, `complete_count=65`, `finding_count=0`; the binding reports
`revision=8eee79db…`, `branch=master`, `origin_tip=efbffe086…` (so the revision is landed and pushed). The r44 entry
is clean, with its three header keys at column 0 on lines 1 (`source:`), 2 (`verified-at:`), 3 (`recheck:`).
The entry's `source:` line opens with the id list `S237 S240 S242 S243 S244 S245` before any prose, and its
`recheck:` names the frozen `FETCH.txt`/`SHA256SUMS` and `tools/check-scrub-record-r44.py`.
Receipt `kheader-8eee.out`.

The gate bites (scratch fixture repo `…/khfix`, `git rev-parse --show-toplevel` asserted before each commit):
a note missing `verified-at:` → `FAIL`, 1 finding `KNOWLEDGE-HEADER-MISSING` at `corpus/knowledge/bad.md`, exit 1;
the repaired note → `PASS`, 2 clean, exit 0; a non-existent branch → `CANNOT_EVALUATE` with
`E-BRANCH-MISSING` (the binding refuses rather than passes). The tool's own `--selftest` is 25/25 PASS.
Receipts `khfix-neg.out`, `khfix-pos.out`, `khfix-refuse.out`, `kheader-selftest.out`.

## 5. The evidence the rows cite is committed, digested and line-exact

- All five round-44 frozen files are tracked at `8eee79db` and the committed blobs hash to the digests in both
  `.ufo/waves/round-44/frozen/src/SHA256SUMS` and the row evidence cells: `scrub.c f347931b…`, `sysfs.c ce146120…`,
  `btrfs-scrub@.timer 9a0b6cc2…`, `btrfs-scrub@.service eaa7af92…`, `PKGBUILD 3b803e8b…`; worktree and committed
  bytes agree (`sha256sum -c SHA256SUMS` → all OK).
- `.ufo/waves/round-44/frozen/hostcap/capture.txt` committed sha256 `efb52388…` equals the value in row S245's
  evidence cell and in the entry's `source:` line; `FETCH.txt` maps each file to its row and to tag/peeled commit
  (Linux v7.2.11 `a2de78ee…`, btrfs-progs v7.1 `4ab0e80b…`, packaging 7.1-1 `0c0a4d77…`).
- 32/32 quote anchors resolve exactly at their cited line numbers: S242 `scrub.c` 1380, 1381, 3147, 3153, 3159, 3222,
  3321, 3331, 3333, 3336; S243 `sysfs.c` 72, 74, 2028, 2040, 2042, 2044, 2113; S244 `btrfs-scrub@.timer` 5, 7, 8, 11,
  `btrfs-scrub@.service` 9, 10, `PKGBUILD` 100, 101; S240 (round-43 snapshot) `ioctl.c` 3139, 3141; S237 (round-42
  snapshot) `scrub.c` 421, 969, 1293, 1295, 1546. Receipts `digests.txt`, `spotcheck.txt`.

## 6. The validator sees these rows — 15/15 mutations detected (fixture copy only)

Fixture: a copied `corpus/SOURCES.md` inside a lane-symlinked tree that reproduces the real validate output
byte-for-byte apart from the `ok` path (40 W04 + `ok`, exit 0). Each mutation was applied to one row, run, and
reverted; the lane registry was never written.

| Mutation (row) | Result |
|---|---|
| drop used-by cell (S242, S243) | E01 `fields=10`, exit 1 |
| status `mined`→`watched` (S242, S244) | E07, exit 1 |
| used-by → nonexistent note (S242) | E11 `missing used-by …`, exit 1 |
| opened 2027-01-01 (S242) | E08, exit 1 |
| recheck `3w` (S242) | E09, exit 1 |
| tier `D` (S242) | E06, exit 1 |
| kind `source` (S242) | E05, exit 1 |
| S245 kind `community` at tier A | E10 `community-at-A`, exit 1 |
| row moved under `## Paths` (S242, S245) | E12 `row outside Registry section`, exit 1 |
| duplicate S242 row | E03 (+E04), exit 1 |
| used-by `—` (S242) | W03 only, **exit 0** (warning by contract) |

Receipt `mutations.json` (driver `mutate.py`). This is the sensitivity evidence that the six rows are not merely
tolerated but actually parsed and judged, and that a warning-only state still exits 0 as documented.

## 7. Context from the frozen C2 counter (not counted here)

Read-only run at `8eee79db` of `tools/check-scrub-record-r44.py`: `sources_ok=1` with
`sources = {S237,S240,S242,S243,S244,S245,source_line} = all true`, `novelty_base_hits=0` (SR7/8/9 = 0/0/0),
`quotes_ok=3`, `props_ok=3`, `host_ok=3`, `pointer_ok=1`, `snapshots_ok=true`, `capture_ok=true`,
`transcripts_bound=0`; `verdicts_ok=0` because the w2 verdict seats have not yet reported — expected at this point,
and the counted verdicts belong to `C2RevSR<n>`/`C2CritSR<n>`, not to this seat. Overall `verdict=FAIL` pre-verdict is
therefore the declared pre-data state, not a source finding. Receipt `counter-8eee.json`.

## Observations and limits (no defect)

1. S245's evidence cell names `capture.sh` and `capture.txt` but pins only `capture.txt`'s sha256; `capture.sh`
   (committed at `8eee79db`, sha256 `6a297e4f…`) carries no digest anywhere. This is the exact phrasing of the
   two predecessor own-work captures S239 (`…r42.md`) and S241 (`…r43.md`), and the counter's `capture_ok` pins
   `capture.txt`; inherited convention, not a round-44 regression.
2. `sources-census.sh validate` resolves E11 used-by paths against the worktree, not against `--revision`. For the
   frozen claim I re-ran it on the committed blob in a fixture (item 1); anyone re-running from an archive without the
   knowledge files present would see E11 noise. Behaviour as designed, worth knowing.
3. The 40 W04 warnings are pre-existing across the registry and unrelated to the round-44 rows.
4. Lane tip ≠ frozen revision: SKILL.md is modified and `.ufo/waves/round-44/{after,w1,w2}` carry other seats' files
   at the time of my run. My surface (registry + r44 entry) is identical across the two commits, so this does not
   weaken the results above.

## Proposed text

Receipt/wave-note line the L1 can paste:

> w2 C2 sources/registry (C2ExecFinalSources): `sources-census.sh validate` exit 0 at tip `8728e8b` and at frozen
> `8eee79db` (40 pre-existing W04, no E-codes); S242–S245 are 11-cell tier-A `mined` rows whose used-by names
> `corpus/knowledge/btrfs-scrub-record-r44.md` (S237/S240 extended, base→tip adds exactly those four rows and changes
> only their used-by column; 241→245 rows, mined 215→219); `check-knowledge-header.py --revision 8eee79db…` PASS
> (65/65 notes, 0 findings) and its fixture controls fail closed; 32/32 cited quote anchors exact against committed,
> digest-matching snapshots; 15/15 registry mutations detected, warning-only used-by still exit 0. Support, no defect.

If the L1 wants a one-clause qualifier for the counter discussion: "sources_ok conjunct independently reproduced on the
committed registry blob; verdicts_ok pending the counted w2 seats."

Report path: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w2/C2ExecFinalSources.md`
Receipts: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w2/C2ExecFinalSources/`
