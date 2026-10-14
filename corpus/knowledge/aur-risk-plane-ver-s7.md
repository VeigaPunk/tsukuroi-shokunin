# VER-S7 — independent re-measure of the AUR-arm foreign count (S7-1's landing)

source: independent read-only probes by the VER-S7 seat, host `plazir27`, user `vgpnk`,
non-root, own commands run 2026-10-14 15:21:38–15:27:29 -03 (18:21:38Z–18:27:29Z); scratch
`/tmp/w7-tsukuroi-vers7/` (`probe-*.txt`, `live.out`, `selftest.out`, `ext-*.out`,
`bl-*.tsv`). No file was edited by this seat; the only writes are that scratch and this note.
No transaction, no `-Sy`/`-Syu`, no install/remove/restart, no AUR RPC, no network, no root.
Claim tags: **[observed]** / **[inference]** / **[unknown]**.

Target of verification (polled for, per the assignment): lane **S7-1**'s landing in
`tools/tsukuroi-census.sh` — the foreign arm that round 6 specified but did not land
(`aur-risk-plane.md:314-329`, "written, not implemented"; record Step-0 "**no**" rows
`plans/round-6-record-draft.md:259-293,§4`). Realized revision pinned by me:
md5 **`821acc24c7a1ccb7591fd9b6e3d22aa4`**, **1186** `wc -l` lines, 56 826 B, mtime
2026-10-14 15:24:40.590859462 -0300 — stable across a 5-sample, ~100 s settle poll
(15:24:40 → 15:27:29, no further write while this seat probed).

Cross-read (not the target, cited for the numbers it carries): register
`corpus/knowledge/aur-risk-plane.md` md5 `1a584300f6b07da78bc8332f04b4fd30`, 341 `wc -l`
(16-row table §1); round-6 verifier `aur-risk-plane-ver-s6.md` md5
`b0de352dec653891d5d36dd742536198`, 133 lines.

**Verdict: CONFIRMED — the foreign count and its fold reproduce from this seat's own
probes. 16 foreign packages; `known=16 new=0 drift=0 gone=0`; the gate's embedded baseline
is identical to the register's 16 rows; all four fail-closed branches fire and name their
rows. 0 measurement claims refuted. 1 citation delta, 1 realization delta, 1 scope
observation.**

## 1. What the arm claims, re-measured

Live run of the landed revision (`bash tools/tsukuroi-census.sh`, my invocation,
2026-10-14T15:26:24-03): rc=1 [observed]

```
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(…); foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16); pins=none; holds=pacman glibc; db.lck=absent)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

The count in that note is what the assignment sends this seat to re-measure — twice, by
probes that do not involve the gate.

## 2. My own count, two methods (the gate not used)

| method | my command | my result | vs the note |
|---|---|---|---|
| A. pacman's own list | `pacman -Qm` (rc=0), `wc -l` | **16** rows, exact 16 names | = `foreign=16` |
| B. set difference vs the configured sync dbs | `pacman -Slq \| sort -u` = **15 651** names; `comm -23 <(pacman -Qq \| sort) <(pacman -Slq \| sort -u)` | **16** rows | `diff` A vs B → **identical 16/16** [observed] |
| context, same window | `pacman -Qq` **1188** · `pacman -Qme` **3** · `pacman -Qu` rc=1 empty · `pacman -Sup --print-format '%n %v'` rc=0, 0 lines · `pacman -Qmdtq` rc=1 empty · `pacman -Qdtq` = `electron39 mbedtls webp-pixbuf-loader` | — | all equal the register §0/§1 and the round-6 record |

The 16, verbatim from my run: `android-apktool-bin 3.0.3-1`, `elephant*` 2.21.0-1 ×13,
`obsidian-cli-inspector 1.0.3-1`, `omarchy-walker 1.0.0-2`.

## 3. The fold, recomputed from a *different* source than the gate

The gate folds the live set against an embedded snapshot. I folded the live set against the
**register's §1 table**, extracted by my own `awk` over `aur-risk-plane.md` (16 name/vendor
pairs), then my own join with the live `pacman -Qm` [observed]:

- `known=16 new=0 drift=0 gone=0` — byte-for-byte the numbers the live note prints.
- The gate's embedded snapshot (`tools/tsukuroi-census.sh:188-203`, `R6_FOREIGN_BASELINE`)
  diffed against my register-derived table: **identical 16/16 name+version** — so the fold
  compares live state against the register's rows, not against a re-typed list.
- Class split, version-level (stronger than the register's name-level check): for each of
  the 16 I asked whether `<name>-<version>` is a directory in `offline.db` →
  **14 in-offline / 2 not**; the 2 are exactly `android-apktool-bin-3.0.3-1` and
  `obsidian-cli-inspector-1.0.3-1`, i.e. the two `AUR-local` rows. The register's
  14 `offline-exile` / 2 `AUR-local` split reproduces at the version level [observed].

## 4. Fail-closed battery (my runs, through the documented env override)

`TSUKUROI_FOREIGN_BASELINE=<my file>` against the live host, five cases, each rc=1 DEGRADED
[observed]:

| my baseline file | rows | printed foreign field | names printed |
|---|---|---|---|
| `bl-hit.tsv` (the register's 16 rows) | 16 | `foreign=16(known=16 new=0 drift=0 gone=0) base=file(16)` | — |
| `bl-new.tsv` (16 rows minus `elephant-todo`) | 15 | `known=15 new=1 drift=0 gone=0` | `new=[elephant-todo]` |
| `bl-drift.tsv` (`elephant-todo` version altered to `1.0.0-1`) | 16 | `known=15 new=0 drift=1 gone=0` | `drift=[elephant-todo(1.0.0-1->2.21.0-1)]` |
| `bl-gone.tsv` (the 16 rows + `obsidian 1.11.0-1`) | 17 | `known=16 new=0 drift=0 gone=1` | `gone=[obsidian]` |
| `no-such-file.tsv` (unreadable/absent) | — | `foreign=16(base=absent [known/new/drift/gone unknown])` | — |

Every branch matches the round-6 contract's rules 1–4 (`plans/round-6-record-draft.md:270-281`):
a new arrival is counted and named, a silent version change is visible with **both** versions,
a stale baseline row is never dropped in silence, and a missing baseline never reads HEALTHY
(the count still gates). Rule 5 (the baseline cannot lower a verdict) is carried by the
hermetic case `healthy: foreign set equals the accepted baseline (16 rows, hit)` → exit 0
HEALTHY.

Hermetic suite, my run: `bash tools/tsukuroi-census.sh --selftest` → **rc=0,
`TSUKUROI_CENSUS_SELFTEST: PASS (41 cases, 41 passed, 0 failed)`** — 35 (round 5) + **6** new,
against the plan's `35+N, N≥4` bar. The 6, verbatim from my transcript: *foreign set equals
the accepted baseline (16 rows, hit)* · *embedded r6 snapshot is the default source* · *new
foreign arrival is named* · *baseline version change shows both versions* · *baseline row no
longer installed is never silent* · *absent baseline never reads HEALTHY*.

## 5. Spot-checks (the three this seat was asked for, verbatim results)

1. **The live set equals the register's table, cell for cell.** `diff <(sort live -Qm output)
   <(sort register §1 name+version)` → **empty** — the 16 live name+version pairs are exactly
   the register's 16 rows, 16/16, three days after the register's run.
2. **The class boundary is real, not asserted.** Per-row `offline.db` lookup of
   `<name>-<version>` → 14 hits, 2 misses, and the 2 misses are the 2 `AUR-local` rows; the
   two `~/.cache/yay/` package dirs are exactly those two (`find … -maxdepth 1 -type d` = 2),
   and their clone HEADs reproduce the register's pins
   (`android-apktool-bin` `92ce7df1…` `2026-09-28T17:22:27+03:00 update to v3.0.3`;
   `obsidian-cli-inspector` `ce7b4258…` `2026-03-08T07:56:23Z Update to …v1.0.3`).
3. **The gate's hermetic hit case and the live host agree.** `bl-hit.tsv` — my own copy of the
   register's rows, passed in from outside the repo — produced `known=16 new=0 drift=0 gone=0`
   and rc=1 DEGRADED on the live host, the same fold the embedded default produced. The
   embedded snapshot's md5 (as I extracted it, lines 188–203): `bde5487579e57c044768112d17e54ab4`,
   16 lines.

## 6. Deltas the verifier found (kept, not smoothed)

- **D1 — citation, not result (register §0 method B).** The register's second method is
  written as `union of tar -tf …/{core,extra,multilib,omarchy}.db | grep '/desc$'` → "15651
  unique names", then `comm -23 <(pacman -Qq | sort) <(sync-union | sort)` → 16. **As written
  this does not reproduce**: those tar paths are versioned directories
  (`acl-2.4.0-1/desc`), the four archives hold 297/14 954/181/231 = **15 663 versioned
  entries** (`sort -u` = 15 663, so 15 651 is a *name*-level number, not that pipeline's
  output), and `comm` against bare installed names returns **all 1188** installed names. The
  *result* is right and I reproduced it with a name-level pipeline (`pacman -Slq`, §2 B): 15 651
  names → the same 16. Fix belongs to the register's errata or the round record; this seat
  edits neither. VER-S6's §3 quotes the same "15651-name sync union" figure — the number
  travels, the cited command does not.
- **D2 — the baseline realized as an embedded block, not a file.** The round-6 record's
  contract bullet proposed a committed machine-readable file
  (`corpus/knowledge/foreign-aur-baseline.tsv`); the register's §8 allowed "…or an embedded
  block". What landed is the embedded block (`tools/tsukuroi-census.sh:188-203`) plus
  `TSUKUROI_FOREIGN_BASELINE` for an external file. Recorded, not smoothed: the embedded block
  is byte-identical to the register §1 rows **today** [observed], but it is a copy — a later
  append-only errata entry in the register would not move it, and the gate cannot notice
  [inference]. Not a defect in the delivered contract; an operator-visible choice worth the
  record's one line.
- **D3 — live value, three days stable.** 16 is a live reading (15:21:38 -03), identical to
  the round-2 pin, the round-6 register, and both of my methods. No drift to report; recorded
  so nobody re-dates the row from a second number.
- **D4 — scope observation (not a defect of this arm).** The revision I verified carries
  **four** planes (`packages/systemd/drivers/journal`; header `:2`, usage `:220-227`,
  rollup line). The round-7 plan's claim (a) — the fifth, update-safety plane — is not in this
  revision; a sibling artifact `corpus/knowledge/update-safety-v2.md` (353 lines, md5
  `92803aea74ebeb1598fa4f450489e5d2`) landed alongside and was still moving at my pin. The
  record should name the lane that owns the plane, so the debt does not read as closed.

## 7. Not re-verified by this seat (stated so the verdict is not overread)

- The note v2 (`update-safety-v2.md`) and the round-7 record draft were **in flight** at my
  pin (record draft grew 390 → 425 lines during this run). Neither is the target of `VER-S7`;
  the note's own row `| 8 | foreign census | 16 …` agrees with my measurement, read as shape
  only [observed, heads].
- The 16 rows' per-package cells (payload, validation, provenance, clone HEADs) stay VER-S6's
  recompute (2 rows) and the register's own evidence; I re-measured the **count, the set, the
  class split and the fold**, not the per-package table.
- Fixture *strength* (whether each selftest case can actually fail, i.e. mutation resistance)
  is tameshi's sweep, not this seat's; I ran the suite, I did not mutate it.
- The record's final realized-string quote, and whether S7-1 edits the census again after my
  pin, are outside my window: the revision was stable 15:24:40 → 15:27:29.

## 8. Mutation statement

Every command above is a read: `pacman -Q*/-Slq/-Sup --print-format`, `tar` listing of
`/var/lib/pacman/sync/*.db`, `stat`, `grep/awk/diff/sort/comm` over the repo and `/tmp`,
`git status/log`, and two read-only gate runs (`--selftest` writes only under
`/tmp/tsukuroi-r3-2-selftest.*`; the live run writes nothing). `git status --porcelain` taken
before and after my whole battery is **byte-identical** (`tree-before.txt` = `tree-after.txt`):
only S7-1's own ` M tools/tsukuroi-census.sh` and the sibling lanes' untracked files appear,
none of them touched by me. The only two writes by this seat are `/tmp/w7-tsukuroi-vers7/*`
and this note.

## 9. Unknowns [unknown]

- Whether S7-1's revision is final (stable for ~3 min at my pin, 25-min poll not exhausted
  when the verdict was written).
- Whether the round-7 record quotes my measured live string (`base=r6(16)`) or only its
  fixture expectation (`base=file(16)` — what the draft carried when I read it).
- Operator acceptance of the baseline as a decision (the gate treats it as a constant;
  unchanged from round 6's open item).
- Upstream AUR delta for any of the 16 — read-only-unmeasurable here by discipline, carried
  from round 6, never a pass.## Errata (append-only)

- **E-1** 2026-10-14 15:28:17 -03 — after my probe battery closed, the working tree gained
  `?? plans/round-8.plan.md` (a sibling lane's next-round draft; **not** a write by this
  seat) alongside `?? corpus/knowledge/aur-risk-plane-ver-s7.md` (this note). §8's
  before/after comparison covers 15:26:16 → 15:26:48 and is unaffected; recorded so a later
  reader does not read concurrent lane movement as a mutation by this seat. [observation]