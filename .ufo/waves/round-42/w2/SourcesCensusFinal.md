VERDICT: supports

# F-17 — sources census at tip (seat SourcesCensusFinal, w2)

Read-only census of `corpus/SOURCES.md` at lane tip `a968393c678171f8a5a2907da5015735396da4cc`
(SOURCES.md content identical to the dispatch tip `78abb8b5cdc9da511b4fc523e661517a68dd33d3`:
`git diff --stat 78abb8b5..HEAD -- corpus/SOURCES.md` empty; `git show 78abb8b5:corpus/SOURCES.md`
and `git show HEAD:corpus/SOURCES.md` both sha256 `0ea5dcb6dc7d24055532e0bbd3fb3e65c464a0219280370ab2bd6efc29604971`).

All commands below were run once, in this order, from the fleet root for the fleet script and
from the lane root (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`) for the frozen manual block.
Raw stdout and exit codes: `.ufo/waves/round-42/w2/SourcesCensusFinal/`.

## 1. Maintained CLI (`scripts/sources-census.sh`, sha256 3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30)

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

Observed: 41 stdout lines — 40 `tsukuroi W04 …` warnings, then
`tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`; **exit 0**
(receipt `SourcesCensusFinal/validate-tip.out`, sha256 29ae7e9d…fd37732). Warnings never change
status (`scripts/sources-census.sh:17-18`: “W-codes and unlisted lanes never change status”), so
exit 0 is the expected value for a W-only registry.

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tsukuroi
```

Observed (**exit 0**, receipt `census-tip.out`):

| lane | metric | value |
|---|---|---|
| tsukuroi | rows | **239** |
| tsukuroi | tier.A / tier.B / tier.C | 224 / 5 / 10 |
| tsukuroi | status.queued / mined / rejected | 5 / 213 / 21 |
| FLEET | rows / missing / tier.invalid / status.invalid | 239 / 0 / 0 / 0 |

Only `tsukuroi` is discovered; no `unlisted` line. 224+5+10 = 239 and 5+213+21 = 239, so the
histograms fully partition the row count.

## 2. Frozen manual census block (`CORPUS.md:133-148`), run from the lane root

Exact commands as frozen (receipt `manual-tip.out`, whole block exit 0):

| check | CORPUS.md | observed |
|---|---|---|
| rows, `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | :135 | **239** |
| malformed rows (NF!=13, must be 0) | :137 | **0** |
| tier histogram | :139 | `A=224 B=5 C=10` |
| status histogram | :141 | `mined=213 queued=5 rejected=21` |
| duplicate ids (must print nothing) | :143 | *(empty)* |
| enum violations + tier inflation (must print nothing) | :145 | *(empty — no tier/status/kind/tier-inflation line)* |
| mined rows whose used-by paths do not exist (must print nothing) | :147 | *(empty — 0 missing)* |

Manual row count (239), tier and status histograms are **identical to the maintained CLI**, so the
two parsers agree at tip. Last five ids in file order: S235, S236, S237, S238, S239 (no gap, no reuse).

## 3. Comparison with `.ufo/waves/round-42/before/sources-census-start.txt`

I reproduced the before receipt from an export of the declared base: `git archive c8efaa3f` into a
scratch fleet-root layout with the fleet `shokunin.conf`, then the same two commands with
`--root <scratch>/baseroot tsukuroi`.

| state | validate | W04 | rows | queued | mined | rejected | tier A/B/C |
|---|---|---|---|---|---|---|---|
| base `c8efaa3f` (export) | exit 0, ok | **40** | **236** | 5 | 210 | 21 | 221/5/10 |
| freeze `a84fc9de` (export) | exit 0, ok | 40 | 239 | 8 | 210 | 21 | 224/5/10 |
| tip `a968393c` (live lane) | exit 0, ok | **40** | **239** | 5 | 213 | 21 | 224/5/10 |
| `before/sources-census-start.txt` | exit 0, ok | 40 | (236 from base census) | — | — | — | — |

- My base export output is **identical** to `before/sources-census-start.txt` after path
  normalization (header comment and `exit=0` trailer excluded); receipt `comparison.txt`.
- **W04 sets are byte-identical** base↔tip and freeze↔tip (40 lines each; `SourcesCensusFinal/w04-*.txt`,
  diff empty). No new duplicate-URL warning was introduced by the round’s new rows.
- Rows 236 → 239 (+3) and status queued 8 → 5 / mined 210 → 213 at tip are **exactly** the declared
  S237–S239 transition, not drift:
  - `a84fc9de` (freeze) adds the three rows queued: `git diff a84fc9de^..a84fc9de -- corpus/SOURCES.md`
    shows 3 insertions only, and `git show a84fc9de:corpus/SOURCES.md | grep -cE '^\|…S[0-9]{3,}…\|'` = 239.
  - `f50c28d8` flips them queued→mined with `used-by corpus/knowledge/btrfs-scrub-record-r42.md`
    (`git diff a84fc9de..HEAD -- corpus/SOURCES.md` = 3 changed lines, 3 insertions/3 deletions);
    `corpus/lessons/round-42.md:25` records “Rows touched old→new: S237, S238, S239 `status` queued→mined”.
- New-row states at tip (`corpus/SOURCES.md:246-248`): S237 tier A status mined; S238 tier A mined;
  S239 tier A mined; their `used-by` target `corpus/knowledge/btrfs-scrub-record-r42.md` exists, and
  S239’s own-work capture `.ufo/waves/round-42/frozen/hostcap/capture.txt` exists (both covered by the
  empty E11/W-missing output above). S237 and S238 URLs each occur once in the registry, so the new
  rows do not add a duplicate-URL warning.

The guided before figure “236 rows, 40 W04” is therefore the base snapshot; at tip rows are 239 with
the same 40 W04. Both halves of the guided comparison hold when the base is read as the base and the
tip as the tip.

## 4. Notes / limitations

- `before/sources-census-at-freeze-a84fc9de.txt` was produced from the live lane path, not an export of
  `a84fc9de` — already declared as R42-FREEZE-CENSUS-LIVE-PATH (`corpus/lessons/round-42.md:77`). I
  did not re-adjudicate that item, but an export of `a84fc9de` gives the same 40 W04 lines and exit 0
  (receipt `validate-freeze.out`), so the receipt’s content is correct even though its provenance label
  is not.
- The 40 W04 warnings are pre-existing at base and unchanged; the census CLI only warns, and the frozen
  manual block has no duplicate-URL check at all. They are not a round-42 regression.
- I did not run `sources-census.sh selftest` (C1’s item), did not re-open any URL or re-verify `teaches`
  against sources (C2 row-verdict seats), and did not run either frozen counter. No writes to the lane,
  the fleet repo or the host; no git/jj mutations; scratch removed.
- Tooling: nothing installed or upgraded (existing `bash`, `gawk`, `coreutils`, `git`).
