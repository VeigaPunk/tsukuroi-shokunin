VERDICT: defect-found

F-10 seat, round 49 wave w1. Assigned: read the frozen record and the assimilation rules,
inspect the staged `merge/tsukuroi` package read-only, count staged and lane registry ids with
CORPUS.md's 0-3-space pattern, report the collision set against the round-48 prior state, and
draft the `Assimilation:` line the report must carry. No lane byte was written; no campaign tool
was run; nothing was fetched. Executed commands are exactly the item's (`ls -R`, the reads, the
CORPUS.md census patterns applied to a `git show` copy of the registry and to a copy of the staged
append). Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ScribeAssim/` removed after the receipts
were copied into `.ufo/waves/round-49/w1/R49ScribeAssim/`.

## 1. Census — the two id spaces

Freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c`; registry read with
`git -C tsukuroi-shokunin show <FREEZE>:corpus/SOURCES.md`.

| | lane registry @freeze | staged `SOURCES.append.md` |
|---|---|---|
| rows, `^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|` | **255** | **147** |
| id extent | S001–S255, contiguous, **no gaps** | S200–S346, contiguous |
| rows, column-zero pattern (`^\|…`) | 255 | 147 |
| rows with 1–3 leading spaces | 0 | 0 |
| malformed `awk -F'\|' … NF!=13` | **0** | **14** |
| tier histogram | A=239 B=5 C=11 | A=102 B=43 C=2 |
| status histogram | mined=228 queued=5 rejected=22 | mined=140 + 7 cells that are not statuses |
| duplicate ids | 0 | 0 |
| knowledge entries | 91 files | 70 files |

Receipt: `R49ScribeAssim/census.txt`. The 0-3-space pattern and the column-zero pattern return the
same counts on both files because **neither file carries an indented row** (0 and 0): the spacing
tolerance is untested by these inputs. What does bind this package is a different character —
the escaped pipe (defect D3 below).

## 2. Collision set — 56, and none of them is the same document

`staged ∩ registry` = **56 ids, S200–S255** (`R49ScribeAssim/collisions`).
Same-document collisions inside that set: **0 of 56** (`R49ScribeAssim/collisions-by-document.txt`;
lane document from the freeze, staged document from the append).

Prior state, for the delta the round asked for: round-48 recorded **53** collisions over registry
**252** ids (`round-48/assimilation/collisions` 53 lines; `reg-ids` 252 lines). The registry then
grew by exactly three rows — `corpus/lessons/round-48.md:17-19` — S253 admitted (POSIX.1-2024
§2.6.5), S254 rejected (U&L Q131766), S255 admitted (GNU Bash Reference Manual 5.3, Redirections),
so the collision set grew 53 → 56 with no change on the staged side (staged extent S200–S346 and
row count 147 are identical to round 48's `staged-ids`).

Non-colliding staged ids: **91** (S256–S346) — free, but not appendable at their own ids *and* at
the renumbered ids without deciding an order: with the whole package adopted in package order the
map is S200→S256 … S346→S402 (offset +56).

**The collision is not a numbering shift; it re-points provenance.** The eight rows the frozen C1
entry cites and the three the C3 claim rests on mean different documents in the staged package
(`R49ScribeAssim/frozen-claim-ids.txt`):

| id | lane @freeze | staged |
|---|---|---|
| S246 | Linux v7.2.11 `lib/cmdline.c`, `lib/vsprintf.c`, `lib/kstrtox.c` | PKGBUILD（源文） — Arch Linux 中文维基 |
| S247 | Linux v7.2.11 `fs/btrfs/dev-replace.c` | Plymouth（Cloudflare CDN 镜像） |
| S248 | systemd v262 `man/systemd.kill.xml` | arch-wiki-docs-zh (offline package recipe) |
| S249 | Round-45 host scrub-service stop capture (own-work) | 繁體中文翻譯 (zh_TW/index.rst) — Linux v7.2 |
| S242 | Linux v7.2.11 `fs/btrfs/scrub.c` | boot-writers-r19 (own-work) |
| S243 | Linux v7.2.11 `fs/btrfs/sysfs.c` | btrfs-space-r30 (own-work) |
| S244 | Arch btrfs-progs packaging 7.1-1 | btrfs-repair-r31 (own-work) |
| S237 | btrfs-progs v7.1 `cmds/scrub.c` | Arch Linux 中文维基（Cloudflare CDN 镜像） |
| S253 | POSIX.1-2024 (Issue 8) ch.2 word expansion | mkinitcpio（源文） — ArchWiki（日本語版） |
| S254 | Unix & Linux Stack Exchange Q131766 | Plymouth（Cloudflare CDN 镜像，zh 变体） |
| S255 | GNU Bash Reference Manual 5.3, Redirections | Plymouth（Cloudflare CDN 镜像，zh-hant 变体） |

C1's `source:` line cites S246 S247 S248 S249 S242 S243 S244 S237; C3 is "sourced: S255 bash fd>9"
(`frozen/FROZEN.md:17`) on rows admitted at `corpus/lessons/round-48.md:17-19`. Appending any
staged row at its own id would therefore rewrite what those frozen entries point at. Every staged
row must be renumbered by document before it can land; nothing lands by id.

## 3. Defects found in the staged package and its own report

**D1 — `MERGE-REPORT.md:9` is stale by 56.** "lane registry currently holds **199** rows; first
staged id is **S200**". At the freeze the registry holds **255** (S001–S255), so S200 is occupied,
not free; the first genuinely free id is **S256**. The report's duplicate section
(`MERGE-REPORT.md:90`) consequently names one overlapping source (S201) where the registry holds a
row for **10** staged sources by exact URL (`R49ScribeAssim/document-dups.txt`): S201, S215, S220,
S279, S280, S281, S282, S288, S301, S319 — seven of them the errno(3) page the lane already holds
three times (S202/S203/S204), one the errno-base.h header (S205), one `fs/btrfs/ioctl.c` (S201).

**D2 — one knowledge path is not a new file.** `MERGE-REPORT.md` lists
`corpus/knowledge/errno-contract-variance-r37.md` as `new-file`. The lane already holds that path at
the freeze (5289 B, `verified-at: 2026-10-25`, `source:` S202–S207); the staged file of the same
name is a **different document** (5938 B, sha256 `52b63255…`, `source:` S279/S280/S281/S282/S286/
S287, `verified-at: 2026-10-24`). Copying it is a rewrite of a held entry, which CORPUS.md forbids
("Corrections are new entries, never rewrites"). It is the only path overlap of the 70
(`R49ScribeAssim/knowledge-path-overlap.txt`: lane 91 files, staged 70, overlap 1; lane bytes 5289
sha256 `8e01096e…`, staged 5938 sha256 `52b63255…`, not identical).

**D3 — 14 of 147 staged rows are malformed under the corpus census, and that makes the enum check
vacuous.** CORPUS.md:89 forbids `|` inside a cell; 14 rows carry escaped pipes (`\|` inside wikitext
templates and `TranslationStatus` invocations), so `awk -F'|'` reads NF 14–17 instead of 13
(`R49ScribeAssim/malformed-rows.txt`: S231, S234, S245, S246, S253, S254, S255, S262, S263, S264,
S265, S266, S267, S268). Two consequences, both observed:
- the CORPUS.md malformed test prints **14**, not 0 — the block cannot be appended and pass the
  lane's own census;
- the CORPUS.md enum command is gated `&& NF==13`, so it **silently skips those 14 rows and prints
  nothing** (`R49ScribeAssim/enum-nf13-gated.txt`: zero lines, rc 0). It passes vacuously while 7 of
  the 14 rows have a non-status in `awk $9` (`\`, `2024-08-30\`, `2025-12-27\`, `2025-03-22\`,
  `mkinitcpio\`, `#\`×2) — the `vacuous` class CORPUS.md's own mistake vocabulary names.

**D4 — no staged entry can be admitted as written.** None of the 70 staged knowledge files carries
a `## QUALITY check` (grep for the token `quality`, case-insensitive: 0 files), and the lane's
`corpus/QUALITY.md:19` (criterion 14, R12) requires exactly that block before an admit: "a promised
check is not a performed check". All 70 do carry `source:`/`verified-at:`/`recheck:` (70/70), so the
provenance trio is fine; the admission block is what is missing.

**Consistent, for the record:** 147 staged rows = `MERGE-REPORT.md:5` "147 accepted, 0 refused"; 70
staged entries = "proposed knowledge entries: 70"; the 70 report-table rows match the 70 files one
to one (no orphan either way).

## 4. Gate table (round-49 candidates)

Quarantine slice carried from `round-48/assimilation/quarantine-slice` (12 rows: S211 and S213
`payload-absent`; S225 unreachable; S230, S231, S242, S243, S244, S249, S250, S251, S252 no locator).
It applies unchanged — the staged bytes are the same bytes — and it blocks **9 of the 70 entries**
(`R49ScribeAssim/quarantine-entries.txt`): boot-writers-amend (S242), btrfs-space-repair-amend
(S243/S244), errno-falsifier-amend (S230), lane-harness-selftest (S252), snapper-rollback-bilingual
(S213), snapshot-boot-preconditions-amend (S231), translation-scope-at-kernel-tag-r29
(S249/S250/S251), translation-status-ledger-r27 (S225), upstream-release-watch-r25 (S211).

| candidate | verdict | reason | flip |
|---|---|---|---|
| `btrfs-ioctl-surface-r27.md` (row S223) | **ADMIT**, conditional on the two steps named in §5 | one cited row, tier A `code`; the lane holds **no** row for `include/uapi/linux/btrfs.h` at the freeze (`grep -c` = 0); path is new; no quarantine row; campaign gate block with URL, opened date 2026-10-23, revision pin `v7.2` and five located quotes at `lanes/tsukuroi/round3/SOURCES-PROPOSED.md:48` | re-open the raw header at tag v7.2 and find the ioctl numbers or the two masks differ from the entry's table; or the lane admits a scrub/ioctl entry first |
| `mount-errno-contract-r26.md` (rows S214/S220) | **REFUSE as written** | its two rows are documents the lane already holds — S220 by exact URL (lane S201, `fs/btrfs/ioctl.c`), S214 the same mount(2) page the lane holds at S200 under a different mirror — so the entry restates held ground and would add a mirror duplicate | admit only the proposition the lane's S200 scope excludes (EACCES vs EROFS reading of a read-only mount) as a new entry citing the lane's own S200, not the mirror row |
| `errno-contract-variance-r37.md` (rows S279–S282, S286–S288, S301, S319) | **REFUSE** | occupied path, different document (D2); appending is a rewrite of the lane's 2026-10-25 entry | take the staged body as an appended amendment/superseding *new* path that keeps the lane's current text, after resolving the shifted `source:` ids by document |
| the 9 quarantine-resting entries | **HOLD** | each rests on at least one round-48 quarantine row | re-verify the named row (payload for S211/S213, reachability for S225, locator for the nine) and record the outcome; the entry is admissible the round its rows clear |
| remaining 58 entries | **not evaluated** | outside this seat's command scope — every verdict would need a source fetch, which this item does not authorize | evaluate in an adoption seat that may fetch and re-open |
| all 147 staged rows | **do not append by id** | 56 id collisions, 0 same-document (§2) | renumber by document from S256 in package order (S200→S256 … S346→S402) |

## 5. Drafted `Assimilation:` line (exact text for the round-49 report)

```
Assimilation: one theme taken from merge/tsukuroi (read-only) — the BTRFS_IOC interface surface —
one entry and one row: corpus/knowledge/btrfs-ioctl-surface-r27.md ← staged S223, renumbered S223 →
S256 by document (registry 255 ids S001–S255 no gaps; staged 147 ids S200–S346; 56 id collisions
S200–S255, none the same document, so nothing lands by id; whole-package map S200→S256 … S346→S402).
Row S223 is include/uapi/linux/btrfs.h at tag v7.2, tier A code: the registry holds no row for that
path at the freeze (`grep -c include/uapi/linux/btrfs.h` = 0), its campaign gate block with URL,
opened 2026-10-23, revision pin v7.2 and five ≤25-word located quotes is at
lanes/tsukuroi/round3/SOURCES-PROPOSED.md:48. Admission is conditional on two steps and is not
claimed complete here: (i) the lane's own re-open of that header at v7.2 (step 3 of RUNBOOK §5);
(ii) appending the entry's `## QUALITY check` block (QUALITY criterion 14 — none of the 70 staged
entries carries one). Refused with reasons and flips: mount-errno-contract-r26.md (both cited
documents already held: fs/btrfs/ioctl.c = S201 by exact URL, mount(2) = S200 under another mirror;
flip: only the EACCES-vs-EROFS proposition its rows add, cited to the lane's own S200) and
errno-contract-variance-r37.md (the lane already holds that path at 5289 B, verified-at 2026-10-25;
the staged 5938 B body is a different document, so appending is the rewrite CORPUS.md forbids; flip:
append it as a superseding new path that keeps the held text). Held: the 9 entries resting on the
round-48 quarantine rows S211/S213 (payload-absent), S225 (unreachable) and
S230/S231/S242/S243/S244/S249/S250/S251/S252 (no locator); quarantine slice 12 rows re-read,
0 appended. Guard receipts .ufo/waves/round-49/w1/R49ScribeAssim/ (collisions 56 vs round-48's 53,
registry 252 → 255 via corpus/lessons/round-48.md:17-19; MERGE-REPORT.md:9's 199 is stale by 56 and
its duplicate list names 1 of the 10 held sources; 14 staged rows malformed under the corpus census,
S231 S234 S245 S246 S253 S254 S255 S262–S268, which also makes the NF==13-gated enum check vacuous).
Not evaluated: the remaining 58 entries (no fetch in this seat's command scope).
```

Short form, if the report prefers one sentence:

```
Assimilation: one theme (the BTRFS_IOC interface surface), one entry admitted conditionally —
btrfs-ioctl-surface-r27.md on staged S223 → S256; 56 id collisions S200–S255 all naming different
documents, so nothing lands by id; two refusals with flips (mount-errno-contract-r26.md,
errno-contract-variance-r37.md) and nine holds on the round-48 quarantine slice.
```

If the L1 does not run the two admission steps this round, the honest line is:

```
Assimilation: none this round — the staged package's only non-duplicative btrfs candidate
(btrfs-ioctl-surface-r27.md, staged S223) needs a source re-open and a `## QUALITY check` block
before admission (QUALITY criterion 14) and neither was run; merge/tsukuroi stays read-only and
unappended, as in round 48.
```

## 6. What this seat did not do

- No source fetch, no re-open of S223, no quote verification against `include/uapi/linux/btrfs.h`.
  The ADMIT above is a draft resting on the campaign's own gate block and on the registry
  observation that the lane holds no row for that path — not on a re-opened source.
- No `sources-census.sh` / `validate` run and no campaign tool of shokuknow: the item authorized
  only the named commands, and the census numbers here are the CORPUS.md awk/grep patterns run on
  copies, which is what the item asked for.
- No adoption, no renumbering, no lane write, no git/jj mutation anywhere.
- 58 of the 70 staged entries were not assessed.

## 7. Receipts

`.ufo/waves/round-49/w1/R49ScribeAssim/` — `census.txt`, `collisions` (56 ids), `collisions-by-document.txt`,
`frozen-claim-ids.txt`, `document-dups.txt`, `quarantine-entries.txt`, `malformed-rows.txt`,
`enum-nf13-gated.txt`, `knowledge-path-overlap.txt`, `reg-ids` (255), `staged-ids` (147), `sha256.txt` (staged append
`7914d3b93cea2015c00091d7db28ca2acd289d5097cb513ad1176dc0d7148406`, MERGE-REPORT
`3b14f7b38e3f3296e6b0fbde25c57d5adba062aa534b52a3cc521534f91ea5fa`, candidate entry
`385097cb31823eff48384e33c0ca732b69d360eb11463c70f171a1c0f5101a1c`).
