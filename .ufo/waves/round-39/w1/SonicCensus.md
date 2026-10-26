VERDICT: supports

# R-6 — SOURCES mechanical counts (seat SonicCensus)

Scope: mechanical row counts, malformed-row census, tier/kind deltas for this round, and the
used-by change set, on `corpus/SOURCES.md` at base `0eff65b21bb81195ee06c96a83afbd7a07e52eef`
and dispatch tip `2e1c2a40c13dc52e155d89e72f3fdd560db7399a`, plus the lane tip as found
(`394e1ba4fab39a417abe66a7802f87cf1ff8dd61`). All claims below are count/integrity checks; I did
**not** judge any TO row against source (kill rule belongs to reviewer seats), so this report
carries no `TO<n>:` lines by design.

Lane HEAD at seat start: `394e1ba4fab39a417abe66a7802f87cf1ff8dd61`; `git status --porcelain` showed
` M PROVINCE.md`, `?? .ufo/waves/round-39/w1-dispatch.err`, `?? .ufo/waves/round-39/w1.ready.dispatched`,
`?? .ufo/waves/round-39/w1/` and no tracked SOURCES change (not mine, not touched). During the wave a
sibling seat's work surfaced ` M SKILL.md`; I never opened it for writing and it is not part of this item.

Snapshots used (scratch, sha256 in `SonicCensus/frozen-checks.txt`):
base `516c1be45553754caa678a72f63427d63b879bb3722319248e755687411330c7`,
tip `c2e4598670c50a69a5694b616928f7011199ea1be2dcae73b9b7c440540af34e`;
`diff -q` of the 2e1c2a40 and 394e1ba4 blobs reports them identical, so every count below holds at
the current lane tip as well.

## 1. Row counts at both revisions

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 0eff65b21bb81195ee06c96a83afbd7a07e52eef:corpus/SOURCES.md | grep -cE "^ {0,3}\| *S[0-9]{3,} *\|"
212
$ ... show 2e1c2a40c13dc52e155d89e72f3fdd560db7399a:corpus/SOURCES.md | grep -cE ...
218
$ ... show 394e1ba4fab39a417abe66a7802f87cf1ff8dd61:corpus/SOURCES.md | grep -cE ...
218
```

212 → 218, +6. Receipt: `SonicCensus/counts.txt`. This is consistent with the round-38 declaration
(`SCORECARD.md:2178` "Sources: 207 → 212 rows") and with the round-39 declaration's
"S213–S218 opened this round" (`SCORECARD.md`, Round 39 declaration, measure section). Delta shape:

```
$ git diff --numstat 0eff65b2..2e1c2a40 -- corpus/SOURCES.md
7	1	corpus/SOURCES.md
$ git diff -U0 ... | grep '^@@'
@@ -217 +217 @@
@@ -221,0 +222,6 @@
```

So exactly six appended registry rows (tip lines 222–227) and one in-place line change (line 217,
S208). `## Paths` (line 229) and `## Search log` (line 236) are untouched by the diff.

## 2. Malformed rows (registry table lines, `NF!=13`)

```
$ git show <rev>:corpus/SOURCES.md | awk -F'|' '/^ {0,3}\| *S[0-9]{3,} *\|/ {if (NF!=13) print NR": NF="NF}'
-- 0eff65b21bb81195ee06c96a83afbd7a07e52eef: malformed_count=0
-- 2e1c2a40c13dc52e155d89e72f3fdd560db7399a: malformed_count=0
$ git show 2e1c2a40:corpus/SOURCES.md | awk -F'|' '/^\|/ && NF!=13'   # header + separator + all rows
(no output = none malformed)
```

All 218 rows carry 11 cells (`cell-count histogram tip: {11: 218}`), ids are unique
(`duplicate ids ... []`) and monotonically ordered in document order. Receipts:
`SonicCensus/malformed.txt`, `SonicCensus/rows-analysis.txt`.

Cross-checked with the lane's own contract validator (SOURCES-CONTRACT-v1, E01 malformed, E03
duplicate id, E05–E10 enums). I copied the fleet script read-only into scratch and ran it with
`--file` against the lane registry (stdout only, no `--out`, nothing written to the lane):

```
$ bash sources-census.sh validate --today 2026-10-26 --file <lane>/corpus/SOURCES.md
file	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md     (exit 0, 34 W04)
$ bash sources-census.sh validate --today 2026-10-26 --file <scratch base tree>/corpus/SOURCES.md
file	ok	.../basefull/corpus/SOURCES.md                                        (exit 0, 33 W04)
```

(script sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`, copied from
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`). Base tree built with
`git archive 0eff65b2 corpus tools SKILL.md | tar -x -C <scratch>` so E11 resolution is real; no
E-code at either revision. Receipts: `SonicCensus/base.validate.out`, `SonicCensus/tip.validate.out`.

Census metrics, both from the same tool:

```
$ bash sources-census.sh census --file <lane>/corpus/SOURCES.md
file	rows	218
file	tier.A	203
file	tier.B	5
file	tier.C	10
file	status.mined	192
file	status.queued	5
file	status.rejected	21
FLEET	missing	0
```

(`SonicCensus/tip.census.out`; identical to my independent parse below.)

## 3. Rows by tier and kind added this round

```
added: ['S213', 'S214', 'S215', 'S216', 'S217', 'S218'] removed: []
added by tier: {'A': 6}
added by kind: {'code': 5, 'own-work': 1}
added by status: {'mined': 6}
tier delta: {'A': 6}
kind delta: {'code': 5, 'own-work': 1}
```

| row | line (tip) | tier | kind | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|
| S213 add.c | 222 | A | code | mined | 2026-10-26 | on-release | pacman-transaction-order-r39.md |
| S214 sync.c | 223 | A | code | mined | 2026-10-26 | on-release | pacman-transaction-order-r39.md |
| S215 remove.c | 224 | A | code | mined | 2026-10-26 | on-release | pacman-transaction-order-r39.md |
| S216 util.c | 225 | A | code | mined | 2026-10-26 | on-release | pacman-transaction-order-r39.md |
| S217 trans.c | 226 | A | code | mined | 2026-10-26 | on-release | pacman-transaction-order-r39.md |
| S218 round-39 txcapture | 227 | A | own-work | mined | 2026-10-26 | 30d | pacman-transaction-order-r39.md |

Whole-registry distribution, base → tip: tier A 197→203, B 5→5, C 10→10; kind code 53→58,
own-work 26→27, docs 123→123, community 6→6, dataset 2→2, tool 2→2; status mined 186→192,
queued 5→5, rejected 21→21. No B/C row was added and no `community`-at-A violation exists
(validator E10 clean). Every one of the six new rows is used-by the new entry, and the entry cites
exactly `S208 S213 S214 S215 S216 S217 S218` (`grep -oE '\bS[0-9]{3}\b' corpus/knowledge/pacman-transaction-order-r39.md | sort -u`) — no unregistered id, no orphan row.

## 4. Rows whose used-by changed

```
rows whose used-by changed:
  S208
    was: corpus/knowledge/pacman-hook-order-r38.md
    now: corpus/knowledge/pacman-hook-order-r38.md, corpus/knowledge/pacman-transaction-order-r39.md
used-by changed row count = 1
```

Exactly one. `rows changed in any field between base and tip: S208 (field 10 only)` — every other
pre-existing row is byte-identical between the two revisions, and S208 kept line 217. Empty-used-by
set is unchanged (17 rows: S006, S012, S013, S018, S024, S029, S030, S033, S036, S037, S042, S043,
S183, S184, S185, S190, S197); zero of them are `mined`, so the W03 population is 0 at both
revisions. All used-by targets that are lane paths resolve on disk (`missing: [] count 0`; validator
E11 clean at tip).

## 5. Integrity corroboration for the rows this item counts

These are bound checks, not truth judgments of the TO rules:

- Anchor digests of S208/S213/S214/S215/S216/S217 each match one file in
  `.ufo/waves/round-39/frozen/src/SHA256SUMS`, and `sha256sum -c SHA256SUMS` reports all six OK.
- Cited line maxima fall inside the frozen files: add.c 695≤695 (S213, exactly the last line),
  sync.c 1356≤1360, remove.c 733≤798, util.c 820≤1657, trans.c 239≤452, hook.c 683≤683.
- S218's manifest digest in its anchor cell (`cb5cb4f4…2c1bb4`) equals
  `sha256sum .ufo/waves/round-39/frozen/txcapture/MANIFEST.sha256`, and
  `sha256sum -c MANIFEST.sha256` returns OK for all four captured files.
- S218's teachable counts recompute from the frozen log: `ALPM-SCRIPTLET=441`,
  `transaction started=60`, command windows (`Running '…'`)=86, `wc -l`=3254 —
  the row's "86 command windows, 60 started transactions, 441 ALPM-SCRIPTLET lines" holds. The
  "252 outside every commit phase" figure needs the C2 counter's phase logic and I did not re-derive
  it.

## Adjacent observations (not falsifiers of this item)

1. **S210 vs S217.** S217's teaches cell opens "supersedes S210 —" and states trans.c has
   `alpm_trans_commit` at line 167, not `_alpm_trans_commit`. Mechanically confirmed:
   `grep -c '_alpm_trans_commit' trans.c` = 0 and `trans.c:167` is
   `int SYMEXPORT alpm_trans_commit(alpm_handle_t *handle, alpm_list_t **data)`. S210 was left
   unchanged (`status=mined`, used-by still only `pacman-hook-order-r38.md`, anchor still naming the
   absent symbol). That matches the registry's own precedent: of the 26 `supersedes S###` mentions in
   registry rows (28 across the file, the other two at lines 246 and 260 in prose), 25 predate S217
   and none marks the superseded row's status, so leaving S210 as-is is convention-consistent rather
   than a defect. Consequence to keep in view: a reader following S210's anchor cell to
   trans.c finds no such symbol. Watch item, not a count error.
2. **W04 warning added.** Validator warning count went 33 → 34; the single delta is
   `W04 S217 duplicate url .../54d9411/lib/libalpm/trans.c across scopes` (S217 vs S210, different
   scope cells). Warnings do not affect the clean verdict, and E04 (same URL *and* same scope) does
   not fire — confirmed by /contract code path (`url_scope_nonrejected` keyed on URL+scope), and a
   scratch mutant that removed the phrase "supersedes S210 —" still produced no E04, i.e. the entry
   does not rely on the supersedes wording for validity.
3. **Gate-record obligation for the six new rows** (`corpus/QUALITY.md:125`, criterion 61,
   R26-GATE-RECORD-MISSING): each row added in a round needs URL/repo path, access date and a
   ≤25-word located quote in that round's `## Gate`. `corpus/lessons/round-39*.md` does not exist at
   `394e1ba4` (`ls corpus/lessons | grep round-3[89]` → only round-38 files), so this is a
   prospective handoff to the scribe seat, not a present defect.
4. **Criterion 70** (`corpus/QUALITY.md:138`, tool rows in the `## Gate and probe registry` table of
   `SKILL.md` plus `tools/check-registry-coverage.py`) is outside SOURCES and outside this item; I
   did not run it (`tools/check-registry-coverage.py` exists, 34828 bytes) because it is another
   seat's assigned surface.

## What I did not do

- No TO-row truth judgment (no `TO<n>:` lines); no run of `tools/check-transaction-order-r39.py` or
  the C1 storage counter.
- No judging of the 252-outside-phase figure, of host counts beyond the three recomputed above, or of
  the two counters' predicates.
- No installs or upgrades; no pacman, no sudo, no host mutation. Tooling used: lane `git show`,
  coreutils awk/grep/sha256sum, python3, and a read-only copy of the fleet census validator run
  against scratch trees. Scratch `/fast/scratch/hyaku/tsukuroi-r39/SonicCensus/` is removed after
  receipts were copied into `SonicCensus/`.

## Receipts (all in `.ufo/waves/round-39/w1/SonicCensus/`)

- `counts.txt` — row counts at the three revisions.
- `malformed.txt` — NF≠13 scan at base and tip, diff hunk map, numstat.
- `rows-analysis.txt` — ids, cell histogram, distributions, added rows, changed rows, used-by set,
  anchor digest/line-bound checks, used-by existence.
- `frozen-checks.txt` — SOURCES blob digests, tip/now identity, `SHA256SUMS`/`MANIFEST.sha256`
  verification, pacman.log recounts, trans.c symbol check.
- `base.validate.out`, `tip.validate.out`, `tip.census.out` — contract validator and census output.
