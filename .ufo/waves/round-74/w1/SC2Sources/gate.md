# Round-74 lesson `## Gate` block and search log — draft (SC2Sources)

Target: `## Gate` in `corpus/lessons/round-74.md`, plus the rule-5 search-log paragraph in
`corpus/SOURCES.md`. **Nothing here is appended by this seat.** Registry rows are drafted separately in
`.ufo/waves/round-74/w1/SC2Sources/rows.md`.

## Gate

**Trigger and sources.** Three upstream systemd **v262** artifacts were committed byte-exact before any
rule text was written, under `.ufo/waves/round-74/before/src/` with `SHA256SUMS` and `SOURCES.json`.
Re-verified this round from the lane root:

```
cd .ufo/waves/round-74/before/src && sha256sum -c SHA256SUMS
  unit-file.c: OK      load-fragment.c: OK      unit-file.h: OK        (3/3)
jq -S '.snapshots|map_values(.sha256)' .ufo/waves/round-74/before/src/SOURCES.json
  load-fragment.c  a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5
  unit-file.c      141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd
  unit-file.h      e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f
```

The map digests equal the `SHA256SUMS` digests and the committed bytes. The host runs systemd **262 (262.1-1-arch)**
(`systemctl --version`, `.ufo/waves/round-74/before/host.txt`); every upstream line anchor below is a line
in the pinned **tag v262**, not a verified line in the Arch build, which may carry patches (QUALITY 103).
Access date for every quote: **2026-11-04**.

| id | snapshot (tag v262) | URL | sha256 | rules |
|---|---|---|---|---|
| **S309** | `src/shared/unit-file.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.c` | `141ab101…090bcd` | UF1, UF2 |
| **S310** | `src/core/load-fragment.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/load-fragment.c` | `a510b286…a44f5` | UF5, UF6 |
| **S311** | `src/shared/unit-file.h` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.h` | `e55b17a1…1270f` | UF3, UF4 |

**Gate quotes — one located quote per new row (each ≤ 25 words).** Each was re-read from the committed
snapshot, not copied from a draft.

| id | URL | quote (words) | location |
|---|---|---|---|
| **S309** | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.c` | "Search paths are ordered by priority (highest first), and we need to maintain this order." (15) | `src/shared/unit-file.c:416` |
| **S310** | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/load-fragment.c` | "u->load_state = u->perpetual ? UNIT_LOADED : UNIT_MASKED; /* don't allow perpetual units to ever be masked */" (17) | `src/core/load-fragment.c:6250` |
| **S311** | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.h` | "return IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH);" (8) | `src/shared/unit-file.h:26-32` |

**Supplementary located quotes** (each ≤ 25 words, same access date), for the specific clauses the required quote
does not carry:

| id | quote (words) | location |
|---|---|---|
| S309 | "%s: unit self-alias: %s → %s, ignoring." (7) | `src/shared/unit-file.c:110` |
| S309 | "%s: symlinks are not allowed for units of this type, rejecting." (11) | `src/shared/unit-file.c:97` |
| S309 | "-ELOOP for an alias to self." (6) | `src/shared/unit-file.c:74` |
| S309 | "-EXDEV if the target filename is not a valid unit name or doesn't match the source," (16) | `src/shared/unit-file.c:73-74` |
| S309 | "if (hashmap_contains(ids, de->d_name)) continue;" (5) | `src/shared/unit-file.c:536-537` |
| S310 | "const char *data = builtin_unit_lookup(u->id);" (5) | `src/core/load-fragment.c:6291` |
| S310 | "log_unit_debug(u, \"Loading built-in fragment for %s.\", u->id);" (7) | `src/core/load-fragment.c:6299` |
| S310 | "if (null_or_empty(&st)) {" (3) | `src/core/load-fragment.c:6247` |
| S310 | "No fragment found on disk. For system units, fall back to a built-in copy if we have one * embedded." (20) | `src/core/load-fragment.c:6286-6287` |
| S310 | "On-disk files always take precedence (including masks), since we only get * here when nothing was found in the lookup paths." (21) | `src/core/load-fragment.c:6288-6289` |
| S311 | "UNIT_FILE_ENABLED, UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED, UNIT_FILE_LINKED_RUNTIME, UNIT_FILE_ALIAS, UNIT_FILE_MASKED, UNIT_FILE_MASKED_RUNTIME, UNIT_FILE_STATIC," (8) | `src/shared/unit-file.h:8-15` |
| S311 | "UNIT_FILE_DISABLED, UNIT_FILE_INDIRECT, UNIT_FILE_GENERATED, UNIT_FILE_TRANSIENT, UNIT_FILE_BAD," (5) | `src/shared/unit-file.h:16-20` |

**Admitted (draft — the L1 appends).** Three rows, all tier **A**, status **mined**, `opened` 2026-11-04,
`recheck` on-release, `used-by` `corpus/knowledge/systemd-unit-fragment-plane-r74.md`: **S309** (code, the
unit search path and symlink alias resolution plane), **S310** (code, the fragment mask check and builtin
lookup plane), **S311** (code, the UnitFileState enum and unit_type_may_alias restriction plane). Row text:
`.ufo/waves/round-74/w1/SC2Sources/rows.md`.

Counter evidence at the time of drafting — `--fixture` mode against a scratch mirror (lane registry +
this seat's five drafted rows + the L1Entry note + the committed snapshots), **not** `--revision`:

```
python3 tools/count-uf-rows-r74.py --fixture <mirror>
UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0
met=1 rc=0
TMPDIR=<non-tmp> python3 tools/count-uf-rows-r74.py --selftest
SELFTEST: PASS (13 cases, 13 passed, 0 failed) rc=0
```

The `--revision <commit>` run is the L1's and is the only one that counts; a `--fixture` pass shows the
rows bind, not that the commit is correct.

**Ordering constraint.** The three admitted rows name `corpus/knowledge/systemd-unit-fragment-plane-r74.md` in
`used-by`. The note and the rows must land in the same commit: with the rows alone, the census check
`mined rows whose used-by paths do not exist` prints `missing:` for all three, and the C1 counter returns
`UF_NOTE absent`.

**Rejected / refused (opened this round; each row keeps the rejection).**

| candidate | fetch command and observed status | verdict |
|---|---|---|
| `https://wiki.archlinux.org/title/Systemd` | `curl -sS -L --max-time 15 -o /tmp/archwiki-systemd.html -w '%{http_code} %{size_download}'` -> `200 152032`; `sha256 b26b7bb117b0f58a5987d033c00a3c81850640e03b37271e81527505f9fc9a6c`; title `systemd - ArchWiki`; `grep -ci 'fragment\|symlink\|alias\|null_or_empty\|builtin\|perpetual'` -> `9` (user-facing symlink commands and target pointers only; 0 internal resolution rules) | **S312 rejected** — High-level community administration guide. Does not cover internal unit fragment resolution, search path priority, symlink alias rejection, UnitFileState discrimination, or perpetual unit mask immunity. |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit-load.c` | `curl -sS -L -I --max-time 15 https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit-load.c` -> `HTTP/2 404 (Not Found)`; `src/shared/unit-load.c` -> `HTTP/2 404 (Not Found)` | **S313 rejected** — Candidate source file does not exist in upstream systemd at tag v262. Fragment loading and alias logic reside in `load-fragment.c`, `unit-file.c`, and `unit.c`. |

Exact `REJECTED: <reason>; flip: <what would change the verdict>` text for both is in
`.ufo/waves/round-74/w1/SC2Sources/rows.md`. Two honest rejections are drafted and satisfy the requirement.

**Instrument reach — this seat's own falsification attempts.** Both instruments are frozen; the probes
below attack the predicate, not the wording.

| probe | method | result |
|---|---|---|
| anchor binding | delete `src/shared/unit-file.c` from the S309 `anchor` cell of a fixture mirror | **held** — `findings: [(3, 'registry row S309 does not anchor unit-file.c')]`, `UF_VERIFIED=0`, `met=0`, rc 1. The anchor cells drafted here are load-bearing, not decorative. |
| map URL binding | mutate the S310 `title` cell to omit `https://raw.githubusercontent.com/...` | **held** — `findings: [(5, 'registry row S310 does not cite URL https://...')]`, `UF_VERIFIED=0`, `met=0`, rc 1. |
| invalid kind | change S311 kind from `code` to `own-work` in a fixture mirror | **held** — `findings: [(7, 'source S311 invalid kind own-work')]`, `UF_VERIFIED=0`, `met=0`, rc 1. |
| fabricated quote | test quote not located verbatim in snapshot | **held** — `findings: [(..., 'quote not located in snapshot ...')]`, rc 1. |

**Census.** Declaration receipt: 308 rows, malformed 0, duplicate ids none, tier `A=292 B=5 C=11`,
status `mined=275 queued=5 rejected=28`, 91 knowledge `.md` notes. Simulated after appending S309-S313
(one fixture registry): **313 rows**, malformed **0**, duplicate ids **none**, tier `A=296 B=6 C=11`,
status `mined=278 queued=5 rejected=30`, notes 92 once the C1 note lands. Commands are the frozen census
block in `CORPUS.md` § CENSUS.

## Search log

**Question.** Which systemd rules decide how unit fragments and symlink aliases are resolved and validated — unit search path traversal order, first-seen name registration ignoring lower duplicates, symlink alias validation and self-alias rejection, restrictions on aliasable unit types in `unit_type_may_alias`, discrimination of persistent versus runtime states in `UnitFileState`, fragment masking with perpetual unit immunity, and system-scope fallback to builtin unit lookup — and which sources ground them at release tag v262?

**Queries.**

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md                    (row count)
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md (malformed)
awk -F'|' '/^\|[[:space:]]*S[0-9]+/ {print $2}' corpus/SOURCES.md | sort | uniq -d      (duplicate ids)
grep -c 'src/shared/unit-file.c' corpus/SOURCES.md                                      (URL/registry collision)
grep -c 'src/core/load-fragment.c' corpus/SOURCES.md
grep -c 'src/shared/unit-file.h' corpus/SOURCES.md
grep -c 'wiki.archlinux.org/title/Systemd' corpus/SOURCES.md
grep -c 'unit-load.c' corpus/SOURCES.md
grep -n 'Search paths are ordered by priority\|unit self-alias\|symlinks are not allowed' unit-file.c
grep -n 'unit_type_may_alias\|UnitFileState' unit-file.h
grep -n 'null_or_empty\|UNIT_MASKED\|builtin_unit_lookup' load-fragment.c
```

**Where searched.** The lane's own registry `corpus/SOURCES.md` (collision and census first); the
committed v262 snapshots under `.ufo/waves/round-74/before/src/`; live web candidate
`https://wiki.archlinux.org/title/Systemd`; and candidate repository path
`https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit-load.c`.

**Date.** 2026-11-04.

**Identified 5 · screened 5 · included 3 · excluded 2.**

- Included: `src/shared/unit-file.c`, `src/core/load-fragment.c`, `src/shared/unit-file.h` at tag v262 — three
  artifacts that between them state every rule the note uses, each byte-pinned with a digest and verified lines.
- Excluded: the ArchWiki Systemd article (community guide, lacks internal resolution plane specification, non-versioned)
  and `unit-load.c` (HTTP 404 Not Found at both `src/core/unit-load.c` and `src/shared/unit-load.c`).
- **Stop rationale.** The three upstream artifacts already ground all six rules at tag v262 matching the host's
  installed systemd version; both further candidates were secondary or absent, so another round of searching
  would add commentary rather than resolve an open question. Every registry collision check above printed `0`,
  so no id or URL is duplicated by these rows.
