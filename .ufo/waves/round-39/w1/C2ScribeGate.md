VERDICT: draft

# Seat C2ScribeGate — item C2-20, round-39 lesson `## Gate` rows for S213–S218 + S208 used-by change

Leaf seat, scribe role. Read-only on lane content; no host mutation; no scratch tree was needed (no clone, copy,
mutant or fixture — nothing to remove). Every quote below was verified by `grep -n` in the committed frozen
snapshot; the quoted text is copied from the grep output, not from the knowledge entry.

Draft target: `corpus/lessons/round-39.md` § `## Gate`. That file does not exist yet
(`wc -l corpus/lessons/round-39.md` → `No such file or directory`), so this table is a draft for the L1 to paste.
Table shape, column titles and Decision wording are copied from the round-38 precedent
(`corpus/lessons/round-38.md:12-21`), and the row obligation (URL + access date + ≤25-word located quote grounding
`teaches`) is fleet `CORPUS.md:112-115` rule 1.

## 1. Paste-ready block

### New SOURCES rows (all opened 2026-10-26 by this round; quotes verified by grep in the committed snapshots,
`.ufo/waves/round-39/w1/C2ScribeGate.md`)

| Row | Source URL/path and opened date | Located quote (≤25 words) | Location | Decision |
|---|---|---|---|---|
| S213 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/add.c — opened 2026-10-26 | “alpm_logaction(handle, ALPM_CALLER_PREFIX, "upgraded %s (%s -> %s)\n",” | `commit_single_pkg` (definition add.c:415), add.c:630 — the `upgraded` log line sits between the pre block :465-474 (`_alpm_runscriptlet(…, pkgfile, …)` from the package file :472 with `newpkg->version, oldpkg ? oldpkg->version : NULL` :473) and the post block :638-647 (scriptlet path from the local-db `install` file :641); `skip_ldconfig` :681-682, `_alpm_ldconfig` :689-691 | admit, mined, tier A |
| S214 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/sync.c — opened 2026-10-26 | “/* remove conflicting and to-be-replaced packages */” | `_alpm_sync_commit` sync.c:1336-1356, sync.c:1340 — removal call `_alpm_remove_packages(handle, 0)` :1345 precedes the add call `_alpm_upgrade_packages(handle)` :1354 | admit, mined, tier A |
| S215 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/remove.c — opened 2026-10-26 | “_alpm_runscriptlet(handle, scriptlet, "pre_remove", pkgver, NULL, 0);” | `_alpm_remove_single_package` (definition remove.c:685) at remove.c:711 — pre-remove block :706-713, file removal :716-719, `removed %s (%s)` log :722, `post_remove` :727-733; the old half of an upgrade takes the `if(newpkg)` branch :698 and skips all three because the log and post block are gated on `if(!newpkg)` :721, :727 | admit, mined, tier A |
| S216 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/util.c — opened 2026-10-26 | “alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);” | `_alpm_chroot_process_output` util.c:521-529, util.c:527 — fed by `_alpm_run_chroot` (util.c:610) for scriptlets and `_alpm_ldconfig` (util.c:820), and by hook children through hook.c:525-528 | admit, mined, tier A |
| S217 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c — opened 2026-10-26 | “alpm_logaction(handle, ALPM_CALLER_PREFIX, "transaction started\n");” | `alpm_trans_commit` trans.c:167, trans.c:208 — Pre hook call :201-204 before the line; `transaction completed` :235 and the Post call :237-239 after it, with the interrupted branch :230-232 skipping Post; `_alpm_trans_commit` has 0 occurrences in the snapshot | admit, mined, tier A |
| S218 | `.ufo/waves/round-39/frozen/txcapture/` (own-work) — opened 2026-10-26 | “# captured 2026-10-26T05:42:12Z host=plazir27 read-only by TsukuroiR39” | capture-meta.txt:1-5 (provenance header: pacman 7.1.0.r9.g54d9411-3, pacman.log mtime, hook-owners and hook-when recipes); MANIFEST.sha256, 4 entries, sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4` | admit, mined, tier A |

Status/recheck/used-by changes to existing rows: **S208** `used-by` `corpus/knowledge/pacman-hook-order-r38.md` →
`corpus/knowledge/pacman-hook-order-r38.md, corpus/knowledge/pacman-transaction-order-r39.md`. No `status` and no
`recheck` change; no immutable cell of any existing row was touched (fleet `CORPUS.md:116-118` rule 2 — only
`status`, `recheck` and `used-by` change in place, each change logged old→new in the round lesson). S210 is **not**
changed and gains no used-by path: the new entry cites S217, whose `teaches` opens
`supersedes S210 — …` as rule 2 requires (verified cell text below).

Row-advisory notes for the pasted block (not table cells, since a cell may not contain a pipe character or a second
sentence):

- S217 repeats the S210 URL string (`corpus/SOURCES.md:219` and `:226`); S213 repeats S191's document at the same
  commit in the other renderer form (`/blob/54d9411` vs `/raw/54d94116164b…`, `corpus/SOURCES.md:197`); S215
  repeats S192 (`/raw/54d9411`, `corpus/SOURCES.md:198`). Scope and anchor differ in each pair, so these are W04
  duplicate-URL advisories, non-blocking (round-37 precedent: the census reported 33 W04 advisories while the corpus
  validated, `corpus/lessons/round-37.md:92`).
- Each new row's `status: mined` is grounded by the entry's own source line and the row's `used-by` cell
  (`corpus/knowledge/pacman-transaction-order-r39.md:1` lists S208 and S213–S218; each of S213–S218 carries
  `corpus/knowledge/pacman-transaction-order-r39.md` in `used-by`), matching `CORPUS.md:103`
  (`mined` = cited by ≥1 path in `used-by`).

## 2. Evidence — commands and observed output

### 2.1 Snapshot and capture digests (the rows' `anchor` cell digests reproduce)

```
$ cd .ufo/waves/round-39/frozen/src && sha256sum -c SHA256SUMS
add.c: OK
hook.c: OK
remove.c: OK
sync.c: OK
trans.c: OK
util.c: OK

$ cd .ufo/waves/round-39/frozen/txcapture && sha256sum -c MANIFEST.sha256
capture-meta.txt: OK
hook-owners.tsv: OK
hook-when.tsv: OK
pacman.log: OK

$ sha256sum MANIFEST.sha256
cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4  MANIFEST.sha256
```

The six digests equal the `anchor` cells of S208/S213–S216 and S217 respectively
(`.ufo/waves/round-39/frozen/src/SHA256SUMS:1-6`), and `cb5cb4f4…` equals the S218 anchor cell.

### 2.2 Quote locations — one `grep -n` per Gate row (frozen copy, verbatim)

```
$ cd .ufo/waves/round-39/frozen/src
$ grep -nF 'ALPM_CALLER_PREFIX, "upgraded %s (%s -> %s)' add.c
630:			alpm_logaction(handle, ALPM_CALLER_PREFIX, "upgraded %s (%s -> %s)\n",
$ grep -nF '/* remove conflicting and to-be-replaced packages */' sync.c
1340:	/* remove conflicting and to-be-replaced packages */
$ grep -nF '"pre_remove", pkgver, NULL, 0' remove.c
711:			_alpm_runscriptlet(handle, scriptlet, "pre_remove", pkgver, NULL, 0);
$ grep -nF 'alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);' util.c
527:	alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);
$ grep -nF 'ALPM_CALLER_PREFIX, "transaction started' trans.c
208:	alpm_logaction(handle, ALPM_CALLER_PREFIX, "transaction started\n");
$ cd ../txcapture && grep -nF '2026-10-26T05:42:12Z' capture-meta.txt
1:# captured 2026-10-26T05:42:12Z host=plazir27 read-only by TsukuroiR39
```

Each quote is a single line of the snapshot, so the grep line number is the quote's location. Word counts of the
quoted strings (whitespace tokens): 7, 6, 4, 4, 4, 8 — all ≤25.

### 2.3 Anchor lines resolve to the named constructs

```
$ grep -n 'commit_single_pkg(alpm_handle_t' add.c        → 415:static int commit_single_pkg(…
$ grep -n '_alpm_upgrade_packages(alpm_handle_t' add.c   → 655:int _alpm_upgrade_packages(…
$ grep -n '_alpm_sync_commit(alpm_handle_t' sync.c       → 1336:int _alpm_sync_commit(…
$ grep -n '_alpm_remove_single_package(alpm_handle_t' remove.c → 685:int _alpm_remove_single_package(…
$ grep -n '_alpm_chroot_process_output' util.c          → 521:static void _alpm_chroot_process_output(…
$ grep -n '_alpm_run_chroot(alpm_handle_t' util.c        → 610:int _alpm_run_chroot(…
$ grep -n '_alpm_ldconfig(alpm_handle_t' util.c          → 820:int _alpm_ldconfig(…
$ grep -n 'alpm_trans_commit' trans.c                    → 167:int SYMEXPORT alpm_trans_commit(…
```

`trans.c` contains exactly one line matching `alpm_trans_commit` (167), so the string `_alpm_trans_commit` occurs
0 times at 54d9411 — the S217 `teaches` supersession statement holds on its face.

Supporting line reads used above (`awk 'NR>=…&&NR<=…'`): add.c:464-476 (pre block: log :465-466, `scriptlet_name`
:470, `_alpm_runscriptlet(…, pkgfile, …)` :472-473), add.c:636-648 (post block), add.c:676-692 (`skip_ldconfig`
:681-682, `_alpm_ldconfig` :689-691), sync.c:1325-1360, remove.c:695-735 (`if(newpkg)` :698, file removal :716-719,
`removed` :722, `post_remove` :727-733), util.c:515-530, hook.c:519-530 (`_alpm_run_chroot` calls :525, :528),
trans.c:201-208 and :230-239.

### 2.4 S218 host counts that the row's `teaches` states (read from the frozen log)

```
$ cd .ufo/waves/round-39/frozen/txcapture
$ grep -c '\[PACMAN\] Running' pacman.log          → 86
$ grep -c 'transaction started' pacman.log         → 60
$ grep -c '\[ALPM-SCRIPTLET\]' pacman.log          → 441
$ grep -c '\[ALPM\] removed ' pacman.log           → 28
```

86 windows, 60 started transactions, 441 `[ALPM-SCRIPTLET]` lines, 28 `removed` lines reproduce the S218 row and the
knowledge entry's host cells. The fourth figure in that row (`252` of 441 outside every commit phase) is **not**
re-derived by this seat — it needs the commit-phase join, which is `counts_ok` in
`tools/check-transaction-order-r39.py` (declared predicate), not a grep.

### 2.5 S208 used-by change — old value from the base commit, new value at the declared commit

```
$ git show 93fddb2:corpus/SOURCES.md | grep '^| S208 ' | awk -F'|' '{print $12}'
 corpus/knowledge/pacman-hook-order-r38.md
$ grep '^| S208 ' corpus/SOURCES.md | awk -F'|' '{print $12}'
 corpus/knowledge/pacman-hook-order-r38.md, corpus/knowledge/pacman-transaction-order-r39.md
```

The change is the one landed line of `4078eb236c7c67f343c76956c587d0a356e0bf5c`:

```
$ git show --stat 4078eb2 -- corpus/SOURCES.md
 corpus/SOURCES.md | 8 +++++++-
 1 file changed, 7 insertions(+), 1 deletion(-)
```

6 inserted rows (S213–S218) + 1 replaced line (S208) = 7 insertions, 1 deletion. Registry size after the commit is
218 rows (`grep -c '^| S[0-9]' corpus/SOURCES.md` → `218`), ids contiguous S200 … S218 with no reuse
(`grep -o '^| S2[0-9][0-9]' … | sort -V`), so the six new ids are the next unused ones (`CORPUS.md:89`).

S217's `teaches` cell begins with the required supersession prefix:

```
$ grep '^| S217 ' corpus/SOURCES.md | awk -F'|' '{print $8}'
 supersedes S210 — the commit function is `alpm_trans_commit` (trans.c:167), not `_alpm_trans_commit` as the S210
 anchor says; Pre hooks run before `transaction started` is logged, Post hooks after `transaction completed`
```

## 3. Findings (scribe observations; none blocks the draft)

1. **Anchor range vs function definition (S215, S213).** S215's anchor reads `_alpm_remove_single_package` lines
   699-733, but the function is defined at `remove.c:685`; 699-733 is the scriptlet/log block inside it. S213
   likewise cites `commit_single_pkg` lines 466-474 and 616-648 while the definition is `add.c:415`. The cited
   lines hold the quoted constructs, so the anchors resolve, but a reader cannot derive the definition line from
   them — the Gate Location cells above therefore name the definition line. No row rewrite: those cells are
   immutable under `CORPUS.md:116-118` rule 2.
2. **Duplicate-URL advisories (W04, non-blocking).** S217 = S210 (identical URL string); S213 = S191 and
   S215 = S192 as the same commit:path in the other renderer form. `corpus/SOURCES.md:219`, `:226`, `:197`, `:198`.
   The corpus tool that counts advisories (`scripts/sources-census.sh validate`) lives in the fleet root, which this
   seat must not touch; the duplicate finding here is a direct `grep` observation, not a census run.
3. **URL form vs fetch form.** The row URLs are the `/blob/` view; `frozen/src/FETCH.txt:2` records the `/raw/`
   fetch base (`https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/<file>`). Both name commit
   `54d9411` and the same path, and the committed bytes verify against `SHA256SUMS`, so access evidence is the
   snapshot content rather than the HTML view. No action; recorded so a Gate reader does not read the difference as
   an unverified URL.
4. **`mined` status is legitimate for all six rows** only because the entry cites them (verified in 2.5/§1), and
   tier A is the pinned primary source (S213–S217) or the committed own-work capture with a pinned MANIFEST
   (S218, same shape as S212 at `corpus/SOURCES.md:221`).
5. **Draft target absent.** No `corpus/lessons/round-39.md` exists yet; the block above is the paste source for its
   `## Gate` section. Header sentence and table columns follow `corpus/lessons/round-38.md:12-16`.

## 4. Not done by this seat (declared limits)

- Did not run `tools/check-transaction-order-r39.py` (its predicate, including `counts_ok` and the 252-outside-phase
  figure, and the quote-at-line check across all 8 TO rows): that is the L1's verification, and the seat's item is
  the Gate table.
- Did not judge any TO row — no `TO<n>: holds|partly|fails` lines, since item C2-20 asks for SOURCES Gate rows, not
  rule verdicts; the declaration routes that to reviewer seats.
- Did not re-open the GitLab URLs: the Gate quote obligation is satisfied against the committed snapshot
  (`frozen/src/`, digests verified), and the seat is a scribe on existing frozen inputs.
- Did not edit any lane file, did not run any mutating git command, no scratch directory was created.

## 5. Touched surfaces

- Written: `.ufo/waves/round-39/w1/C2ScribeGate.md` (this report) only.
- Read: `SCORECARD.md` § "Round 39 — declaration", `corpus/SOURCES.md` (rows S191, S192, S197, S208, S210,
  S213–S218), `corpus/knowledge/pacman-transaction-order-r39.md`, `corpus/lessons/round-37.md:92`,
  `corpus/lessons/round-38.md:1-28`, `corpus/QUALITY.md`, `corpus/README.md`, fleet `CORPUS.md:98-122`,
  `.ufo/waves/round-39/frozen/src/*` and `.ufo/waves/round-39/frozen/txcapture/*`,
  `.ufo/waves/round-39/w1/GateHeaderRecheck/summary.md` (peer, read for the declared-tip cross-check).
- Git: read-only (`git log`, `git show`, `git show <rev>:path`); nothing staged, committed or checked out.
