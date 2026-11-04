# Round-73 lesson `## Gate` block and search log — draft (SC2Sources)

Target: `## Gate` in `corpus/lessons/round-73.md`, plus the rule-5 search-log paragraph in
`corpus/SOURCES.md`. **Nothing here is appended by this seat.** Registry rows are drafted separately in
`.ufo/waves/round-73/w1/SC2Sources/rows.md`.

## Gate

**Trigger and sources.** Three upstream systemd **v262** artifacts were committed byte-exact before any
rule text was written, under `.ufo/waves/round-73/before/src/` with `SHA256SUMS` and `SOURCES.json`.
Re-verified this round from the lane root:

```
cd .ufo/waves/round-73/before/src && sha256sum -c SHA256SUMS
  systemd.unit.xml: OK      unit.c: OK      install.c: OK        (3/3)
jq -S '.snapshots|map_values(.sha256)' .ufo/waves/round-73/before/src/SOURCES.json
  install.c        c11cd57579931f04ab08f17fe058fd9d4a962c0fe5c4c4a9d5ae2e86c7e6ef4d
  systemd.unit.xml eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6
  unit.c           47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7
```

The map digests equal the `SHA256SUMS` digests and the committed bytes. The host runs systemd **262.1-1**
(`systemctl --version`, `.ufo/waves/round-73/before/host.txt`); every upstream line anchor below is a line
in the pinned **tag v262**, not a verified line in the Arch build, which may carry patches (QUALITY 103).
Access date for every quote: **2026-11-03**.

| id | snapshot (tag v262) | URL | sha256 | rules |
|---|---|---|---|---|
| **S304** | `man/systemd.unit.xml` | `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml` | `eb9479be…f14c6` | UL1, UL2 |
| **S305** | `src/core/unit.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c` | `47e98d39…efcb7` | UL3, UL4 |
| **S306** | `src/shared/install.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/install.c` | `c11cd575…e6ef4d` | UL5, UL6 |

**Gate quotes — one located quote per new row (each ≤ 25 words).** Each was re-read from the committed
snapshot, not copied from a draft.

| id | URL | quote (words) | location |
|---|---|---|---|
| **S304** | `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml` | "Unit files found in directories listed earlier override files with the same name in directories lower in the list" (19) | `man/systemd.unit.xml:367-370` |
| **S305** | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c` | "any drop-ins that are masked are simply omitted from the list" (11) | `src/core/unit.c:3908` |
| **S306** | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/install.c` | "Unit %s is masked via a generator and cannot be unmasked, skipping." (11) | `src/shared/install.c:348` |

**Supplementary located quotes** (each ≤ 25 words, same access date), for the clauses the required quote
does not carry:

| id | quote | location |
|---|---|---|
| S304 | "Multiple drop-in files with different names are applied in lexicographic order, regardless of which of the directories they reside in" (20) | `man/systemd.unit.xml:238-239` |
| S304 | "the contents of this variable overrides the unit load path" (9) | `man/systemd.unit.xml:375` |
| S305 | "For masked files check if they are still so" (9) | `src/core/unit.c:3875` |
| S305 | "return !null_or_empty(&st);" (code line) | `src/core/unit.c:3876` |
| S305 | "if (!strv_equal(u->dropin_paths, dropins))" (code line) | `src/core/unit.c:3905` |
| S306 | "create_symlink(&lp, "/dev/null", path, flags & UNIT_FILE_FORCE, changes, n_changes)" (code line) | `src/shared/install.c:2387` |
| S306 | "(flags & UNIT_FILE_RUNTIME) ? lp.runtime_config : lp.persistent_config" (code line) | `src/shared/install.c:2369` |
| S306 | "Unit %s is an alias to a non-existent unit, ignoring." (10) | `src/shared/install.c:351` |

**Admitted (draft — the L1 appends).** Three rows, all tier **A**, status **mined**, `opened` 2026-11-03,
`recheck` on-release, `used-by` `corpus/knowledge/systemd-unit-load-plane-r73.md`: **S304** (docs, the
documented load-path and drop-in merge plane), **S305** (code, the reload-staleness and masked-state
plane), **S306** (code, the install-time mask and alias plane). Row text:
`.ufo/waves/round-73/w1/SC2Sources/rows.md`.

Counter evidence at the time of drafting — `--fixture` mode against a scratch mirror (lane registry +
this seat's five drafted rows + the L1Entry note + the committed snapshots), **not** `--revision`:

```
python3 tools/count-ul-rows-r73.py --fixture <mirror>
UL_ROW ok UL1 source=S304 snapshot=systemd.unit.xml
UL_ROW ok UL2 source=S304 snapshot=systemd.unit.xml
UL_ROW ok UL3 source=S305 snapshot=unit.c
UL_ROW ok UL4 source=S305 snapshot=unit.c
UL_ROW ok UL5 source=S306 snapshot=install.c
UL_ROW ok UL6 source=S306 snapshot=install.c
UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
UL_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1        rc=0
python3 tools/count-ul-rows-r73.py --selftest
SELFTEST: PASS (11 cases, 11 passed, 0 failed)                               rc=0
```

The `--revision <commit>` run is the L1's and is the only one that counts; a `--fixture` pass shows the
rows bind, not that the commit is correct.

**Instrument replacement observed during this round.** When this seat started (23:00-23:05) both
instruments hashed to the declared digests (`count-ul-rows-r73.py` `542f9c29…11a3d6`,
`check-r72-routed-r73.py` `93f034e3…a2f9e`). At 23:15 they read
`84501ab8d4968293de8b38f68a9f53d658535d90df8191cbd96a20df98e94832` and
`328a6bf60c5237fe4ba857b36d2b4401833a61b933f735ec468139b7531a03fe`, with mtimes 23:14:42 and 23:12:19,
and `git rev-parse HEAD` reads `8eeadcb92ad5362cae155e1903cdf11b52a5ac5d`, not the declaration commit
`7493713`. The repair and its old→new digest record belong to the L1; this seat edited neither file.
Re-run of the **current** counter against the landed tree (registry with S304-S308, the landed note, the
committed snapshots): `UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `met=1`, rc 0;
its `--selftest` reads `PASS (12 cases, 12 passed, 0 failed)`. At `--revision HEAD` the same counter reads
`UL_NOTE absent path=corpus/knowledge/systemd-unit-load-plane-r73.md`, rc 128, because the note and the
registry rows are uncommitted at `8eeadcb9` (`git cat-file -e HEAD:corpus/knowledge/systemd-unit-load-plane-r73.md`
-> `fatal: … exists on disk, but not in 'HEAD'`; `git show HEAD:corpus/SOURCES.md | grep -c '^| S30[4-8] '`
-> `0`). The C1 target revision therefore does not exist yet.

**Ordering constraint.** The three admitted rows name `corpus/knowledge/systemd-unit-load-plane-r73.md` in
`used-by`. The note and the rows must land in the same commit: with the rows alone, the census check
`mined rows whose used-by paths do not exist` prints `missing:` for all three, and the C1 counter returns
`UL_NOTE absent`.

**Rejected / refused (opened this round; each row keeps the rejection).**

| candidate | fetch command and observed status | verdict |
|---|---|---|
| `https://man.archlinux.org/man/systemd.unit.5` | `curl -sS -L --max-time 45 -o man.html -w '%{http_code} %{size_download}'` -> `200 135978`; `sha256 69dba09794c028cbb69c7210b52c705f2e6df103def4ab099c082913fd927916`, identical on a second fetch; footer `systemd 262.1`; `grep -c 'id="l[0-9]\+"\|data-line'` -> `0`; the load-path override and drop-in lexicographic sentences appear verbatim (counts 1 and 2), while the `SYSTEMD_UNIT_PATH` sentence appears only once markup is stripped (tag-free `grep -F` -> `0` in raw HTML), which is exactly why the render cannot stand in for the pinned bytes | **S307 rejected** — a rendering of the same upstream manual text already pinned as S304, at renderer version 262.1 rather than tag v262, with no line anchor |
| `https://archlinux.org/packages/core/x86_64/systemd/` | `curl -sS -L --max-time 45 -o pkg.html -w '%{http_code} %{size_download}'` -> `200 101009`; title `Arch Linux - systemd 262.1-1 (x86_64)`; `Last Packager: Christian Hesse`, `Build Date: 2026-10-17 08:46 UTC`; `grep -ci 'drop-in\|load path\|masked'` -> `0`; two consecutive fetches differ in exactly one line, the per-response CSP `nonce` (`diff` -> `2966c2966`), so no content digest is claimed | **S308 rejected** — build provenance only; names no merge, precedence or mask rule |

Exact `REJECTED: <reason>; flip: <what would change the verdict>` text for both is in
`.ufo/waves/round-73/w1/SC2Sources/rows.md`. One refusal would satisfy the routed defect R72-GATE-NO-REJECT;
two are drafted so the L1 can take either.

**Instrument reach — this seat's own falsification attempts.** Both instruments are frozen; the probes
below attack the predicate, not the wording.

| probe | method | result |
|---|---|---|
| anchor binding | delete `src/core/unit.c` from the S305 `anchor` cell of a fixture mirror | **held** — `UL_ROW fail UL3 anchor-not-bound`, `UL_ROW fail UL4 anchor-not-bound`, `UL_VERIFIED=4`, `met=0`, rc 1. The anchor cells drafted here are load-bearing, not decorative. |
| statement grounding | replace the UL5 statement with generic systemd vocabulary ("The unit file path and service system name are checked in the load directory before the install operation completes and the system reads the manager state") while keeping the real located quote | **survived** — `UL_ROW ok UL5 source=S306 snapshot=install.c`, `UL_ROWS=6 UL_VERIFIED=6`, `met=1`, rc 0. Against a 140 KB C file the 6-token/50%-share test can be met by vocabulary almost any systemd sentence contains, so a scripted writer that copies quotes can mint a content-free statement. The note's own UL5 is not vacuous: its three clauses are each located (`install.c:2369`, `:2387`, `:2437-2445`, and the `masked-runtime` state name at `:3888`), and the six drafted statements measure `grounding=18/18, 16/17, 16/18, 11/13, 13/16, 9/11` with quote `located=True` for all six. This is a limit to record against the predicate, not a defect in these rows. |
| fabricated quote | not re-run here: the frozen `--selftest` `QUOTE` case covers it (`quote-absent`, rc 1) and my fixture run scored all 11 cases PASS | **held** |

**Non-author spot-check.** A non-author seat re-located all six note quotes in the committed snapshots
(`norm(quote) in norm(snapshot)` true for all six; statement lengths 34, 35, 38, 30, 28 and 30 words) and
re-ran the counter against a fixture mirror. That is a self-check of the draft, not the closure judge's
live re-open of the three URLs; the spot-check remains owed and no author-side `[x]` is written.

**Census.** Declaration receipt: 303 rows, malformed 0, duplicate ids none, tier `A=287 B=5 C=11`,
status `mined=272 queued=5 rejected=26`, 90 knowledge `.md` notes. Simulated after appending S304-S308
(one fixture registry): **308 rows**, malformed **0**, duplicate ids **none**, tier `A=292 B=5 C=11`,
status `mined=275 queued=5 rejected=28`, notes 91 once the C1 note lands. Commands are the frozen census
block in `CORPUS.md` § CENSUS.

## Search log

**Question.** Which systemd rules decide what bytes become a unit — the compiled load path and its
override order, the drop-in directories and their precedence and lexicographic merge, masking and its
persistence, the daemon-reload staleness test, and the moment an `[Install] Alias=` becomes a symlink — and
which of them can this lane read read-only from the tag the host's build descends from?

**Queries.**

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md                    (row count)
awk -F'|' '... NF!=13 {n++}' corpus/SOURCES.md                                          (malformed)
awk ... print i | sort | uniq -d                                                        (duplicate ids)
grep -c 'man/systemd.unit.xml' corpus/SOURCES.md                                        (URL/registry collision)
grep -c 'src/core/unit.c' corpus/SOURCES.md
grep -c 'src/shared/install.c' corpus/SOURCES.md
grep -c 'man.archlinux.org/man/systemd.unit' corpus/SOURCES.md
grep -c 'archlinux.org/packages/core/x86_64/systemd' corpus/SOURCES.md
grep -n 'directories listed earlier override\|lexicographic order\|SYSTEMD_UNIT_PATH' systemd.unit.xml
grep -n 'drop-ins that are masked\|For masked files\|null_or_empty\|strv_equal(u->dropin_paths' unit.c
grep -n 'masked via a generator\|create_symlink(&lp, "/dev/null"\|UNIT_FILE_RUNTIME\|IS_DANGLING' install.c
```

**Where searched.** The lane's own registry `corpus/SOURCES.md` (collision and census first); the
committed v262 snapshots under `.ufo/waves/round-73/before/src/`; then two live pages,
`https://man.archlinux.org/man/systemd.unit.5` and
`https://archlinux.org/packages/core/x86_64/systemd/`.

**Date.** 2026-11-03.

**Identified 5 · screened 5 · included 3 · excluded 2.**

- Included: `man/systemd.unit.xml`, `src/core/unit.c`, `src/shared/install.c` at tag v262 — three
  artifacts that between them state every rule the note uses, each byte-pinned with a digest.
- Excluded: the rendered Arch man page (same upstream manual text as S304, renderer version 262.1, zero
  line anchors — a rendering, not a second source) and the Arch package page (build provenance only;
  version 262.1-1, packager, build date; zero occurrences of drop-in, load path or masked).
- **Stop rationale.** The three upstream artifacts already ground all six rules at the tag the host's
  build descends from; both further candidates were derivative or provenance-only, so another round of
  searching would add vocabulary, not resolve an open question. Every registry collision check above
  printed `0`, so no id or URL is duplicated by these rows.
