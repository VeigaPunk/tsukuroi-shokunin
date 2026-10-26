VERDICT: supports

# AsmCollision — F-1 assimilation id-collision re-derivation (tsukuroi round 40, wave 1)

Leaf executor seat. Item F-1: re-derive the §10 id-collision check at the pinned registry blob
`f951f288483c1af0cef4afd458488b84cf7a2165` vs `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`,
compare with the L1's `assimilation/{reg-ids,staged-ids,collisions}`, and prove the guard on a
census-valid scratch registry carrying an indented `  | S219 |` row.

Axes (godspeed): (1) agreement of the three collision artifacts, (2) validity of the guard fixture
itself, (3) provenance binding of both inputs.

**Result: all three files reproduce byte-for-byte; the L1's guard-proof fixture, however, is not
census-valid — my re-proof is (evidence in §3–§4).**

## 1. Inputs and their provenance

| input | binding | sha256 |
|---|---|---|
| registry at the pinned rev | `git -C <lane> show f951f288:corpus/SOURCES.md` | `1676992a3d2013e2c9e4a9d6715f704bb287e37cc6942bd0f05c5c1a2c2c42a1` |
| same path in the worktree | `cmp` with the pinned blob → identical (`TIP==WORKTREE`) | same |
| staged package | `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` (153 lines) | `7914d3b93cea2015c00091d7db28ca2acd289d5097cb513ad1176dc0d7148406` |

Registry row counts at the revisions that matter: base `53b294a` = **218** rows (last `S218`); tip
`f951f288` = **225** rows (last `S225`), i.e. round 40 added `S219`–`S225`
(`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` on each blob).

## 2. Re-derivation — the exact §10 block

Commands are verbatim from `/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-40.md:499-505`
(the only substitution: the registry is read from the pinned blob so the check binds to the revision,
and is a byte-identical copy — `cmp` above):

```sh
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' SOURCES-f951f288.md | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md \
  | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions
```

| artifact | lines | sha256 (mine) | L1 counterpart | compare |
|---|---|---|---|---|
| `reg-ids` | 225 (`S001`–`S225`) | `f6da39ad2a3e57272ca9312eb22e4672d4397d1e606f22070cbecccdd82a99da` | same sha | `cmp` → **IDENTICAL** |
| `staged-ids` | 147 (`S200`–`S346`) | `d3918d7c61a351d9f57f3ee317d8684503403e594c7d5bac0980ee5371542f3c` | same sha | `cmp` → **IDENTICAL** |
| `collisions` | 26 (`S200`–`S225`) | `6600bebffae53addf4ee668f8deb6cbc57a99746c7f405acad6ec99ea77b5578` | same sha (130 B) | `cmp` → **IDENTICAL** |

Collision set, expanded: `S200 S201 … S225` (26 ids, contiguous). Integrity checks:
- `sort | uniq -d` on each of the three lists → 0 duplicates.
- both lists are hole-free: `diff` against `seq -f 'S%03g' 1 225` and `seq -f 'S%03g' 200 346` → no output.
- The census agrees with the pattern on the real registry: `scripts/sources-census.sh census --file <pinned blob>`
  → `file rows 225`, exit 0 (`census-tip.txt`), so the extractor drops no row the census counts.

Split of the 26, which is the substantive reading:
- **19 are pre-existing** — registry at base `53b294a` (`S001`–`S218`) ∩ staged = `S200`–`S218`
  (`base-collisions`, sha256 `3cfa6074…`). The package was built against a registry ending at `S199`.
- **7 come from this round's own rows** `S219`–`S225` (`awk '$0>="S219"' collisions | wc -l` → 7),
  added by `a447b67`/`bf23805`. The collision count is therefore revision-keyed: 19 at base, 26 at tip.

No difference found between my derivation and the L1's three artifacts — counts, ranges and bytes all agree.

## 3. Guard proof on a census-valid scratch registry

Fixture (`fixture-census-valid-SOURCES.md`, 461 B; `## Registry` heading, 11-column header, one
column-zero row `S001`, one **two-space-indented** row `S219`; `cat -A` shows `  | S219 | … |` with
exactly two leading spaces):

```sh
scripts/sources-census.sh census   --file fixture-census-valid-SOURCES.md   # file rows 2, tier.A 2, exit 0
scripts/sources-census.sh validate --file fixture-census-valid-SOURCES.md   # file ok … (W03 ×2), exit 0
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' fixture… | grep -oE 'S[0-9]+' | sort   # ids-03        = S001 S219
grep -oE '^\|[[:space:]]*S[0-9]{3,}'      fixture… | grep -oE 'S[0-9]+' | sort   # ids-col0      = S001
comm -12 ids-03   <real staged-ids>                                             # collisions-03 = S219
comm -12 ids-col0 <real staged-ids>                                             # collisions-col0 = (0 bytes)
```

So on a registry the maintained parser **counts** (`scripts/sources-census.sh:614-615`, `:40-42`;
`/home/vgpnk/Projects/shokunin/CORPUS.md:152-154`), the 0–3-space pattern catches the collision and
the column-zero-only pattern false-greens it — the failure mode §10:492-497 requires the guard to catch.

Boundary control (`fixture-4space-SOURCES.md`, same file with `S219` indented four spaces):
`census` → `file rows 1` (the row is indented code and ignored, per the parser note above) and the
0–3-space pattern also stops seeing `S219`. The acceptance window really is 3 spaces, not "any indent".

Reproduction of the L1's own fixture: running the 0–3-space pattern over
`assimilation/guard-proof/reg.md` gives `S219`, byte-identical to their `guard-proof/ids-03`
(sha256 `07f653d8…` blob); their `collisions-03` (`S219\n`, 5 B) and `collisions-col0` (0 B) are
**byte-identical to mine**. Their `ids-col0` is 0 B vs my 5 B only because their fixture carries no
column-zero row.

## 4. Difference found — the L1's guard fixture is not census-valid

`assimilation/guard-proof/reg.md` is 28 B:

```
| id |
|---|
  | S219 | x |
```

Measured with the maintained parser (`census-guard-fixtures.txt`):

- `sources-census.sh census --file reg.md` → `file rows 0` (exit 0).
- `sources-census.sh validate --file reg.md` → `file E12 S219 row outside Registry section`, **exit 1**.
- The same bytes with a `## Registry` heading prepended → `E01 S219 fields=2`, exit 1: three cells,
  not the contract's 13.

So the L1's guard proof exercises the 0–3-space *pattern* but not the census clause that motivates it:
its fixture is not a registry the census accepts, at either indentation or schema level. The guard
conclusion ("0-3 spaces catches, column-zero misses") survives — my `ids-03`/`collisions-03` reproduce
their bytes — but the artifact does not demonstrate the case the item names ("census-valid scratch
registry"). If the wave wants that proof on file, the fixture in §3 is the one to adopt; the L1's
`reg.md` cannot be repaired in place by this read-only seat.

## 5. Latent-risk reading of the real inputs

Both real inputs are flat today — `indented1-3 = 0` and `indented4+ = 0` in the registry and in the
staged file (all 225 and 147 rows at column zero). Consequently the column-zero-only pattern yields
the **same** 26 collisions on the real inputs (`col0-collisions` shares sha256 `6600bebf…` with
`collisions`). Two consequences worth recording:

- The 0–3-space form is not redundant *today* — it is the form that survives the first indented paste;
  there is no present-day counterexample in this lane, only the fixture.
- A future check cannot be told apart from the weaker one by its output until such a row exists, so the
  guard's own validity is only ever visible in its proof fixture — which makes §4 load-bearing.

## 6. Provenance observation on the staged side

`merge/tsukuroi/SOURCES.append.md` in the shokuknow **worktree** differs from its blob at shokuknow
HEAD `8b94c5c`: worktree 153 lines / 147 ids vs HEAD blob 113 lines / 107 ids (`diff` → 40 added lines
`S307`–`S346`, campaign rows written after the last commit `ba6779f0`, 2026-10-24). The L1's
`staged-ids` — and mine — bind to the **worktree** bytes (`7914d3b…`), which is the correct interface
(§10 says read the package bytes), but the staged id set is therefore a moving target: a re-run against
the committed tree would report 107 staged ids. The 26 collisions are unaffected either way, because the
40 extra ids are all above `S225`.

## 7. What I did not do

- I did not verify the renumber-**by-document** map for the adopted entries; F-1 is the id set, and the
  map is the L1's report duty (other seats carry the document checks).
- I did not check staged-row schema validity beyond id extraction (that is the §10 transformation step).
- I ran no counter, no `--selftest`, no build/lint/format; none belongs to this item.
- No lane file was written except this report and the receipts below; no git/jj mutating command, no
  host change, no `sudo`, no package action, no tool install. Scratch was
  `/fast/scratch/hyaku/tsukuroi-r40/AsmCollision` and has been removed; receipts were copied out first.

## Receipts — `.ufo/waves/round-40/w1/AsmCollision/`

| file | what it is |
|---|---|
| `reg-ids`, `staged-ids`, `collisions` | my re-derivation (byte-identical to the L1's) |
| `col0-collisions` | column-zero-only pattern on the real inputs (same 26 ids) |
| `base-collisions` | 19 pre-existing collisions against the registry at `53b294a` |
| `ids-03`, `ids-col0`, `collisions-03`, `collisions-col0` | guard proof on the census-valid fixture |
| `fixture-census-valid-SOURCES.md` | the 2-space `S219` fixture (census-valid: rows 2, exit 0) |
| `fixture-4space-SOURCES.md` | 4-space boundary control (census ignores it) |
| `l1-guard-fixture-reg.md`, `l1-guard-fixture-with-Registry-heading.md` | the L1 fixture, and with a heading added |
| `census-guard-fixtures.txt`, `census-tip.txt`, `census-staged.txt` | parser runs with exit codes |
| `transcript.txt`, `provenance.txt`, `SHA256SUMS` | full command transcript, input bindings, digests |

Key digests: `reg-ids f6da39ad…`, `staged-ids d3918d7c…`, `collisions 6600bebf…`,
`ids-03 dff48809…`, `collisions-03 4968bde6…`, `fixture-census-valid-SOURCES.md 0fd8661b…`.

## Risks

1. **Guard evidence gap (defect, auxiliary).** The L1's guard-proof fixture fails the census
   (`rows 0`, `E12`, and `E01 fields=2` once headed). The collision artifacts stand; the *proof* of the
   census-clause case does not exist in `assimilation/` and would not exist without §3.
2. **Revision-keyed collision count.** 26 at tip, 19 at base. Anyone quoting "26 collisions" must quote
   the revision; the 7 extra ids are this round's own `S219`–`S225`.
3. **Staged-set drift.** The staged file is campaign-mutable and currently ahead of its own HEAD blob
   by 40 rows. The collision set is stable only while no adopted-registry id is added above `S225`.
4. **Silent-mode risk.** With both real inputs flat, a future seat could swap in the column-zero
   pattern and see identical output; only the fixture distinguishes the two guards.
