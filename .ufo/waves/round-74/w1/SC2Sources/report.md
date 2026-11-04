status: complete
verdict: pass — drafts complete; rows S309-S313, Gate quotes, search log, two honest rejections drafted and verified; C1 target revision not yet committed

# SC2Sources — C1 registry, Gate and search-log draft

Seat: L2, tsukuroi lane round 74 (hyaku run 15), wave w1. Leaf member, no subagent dispatch.
Scope: draft text. This seat appended nothing to the lane and committed nothing.

## Produced

| path | content |
|---|---|
| `.ufo/waves/round-74/w1/SC2Sources/rows.md` | rows **S309-S311** (admitted) and **S312-S313** (REJECTED, with flip conditions), each one line, 11 cells, no `|` inside any cell (13 parts when split by `|`), plus measurement logs and census projection |
| `.ufo/waves/round-74/w1/SC2Sources/gate.md` | the `## Gate` block for `corpus/lessons/round-74.md` and the rule-5 `## Search log` paragraph, with one ≤25-word located quote per new row, supplementary located quotes, admitted/census/ordering notes, and instrument reach probes |
| `.ufo/waves/round-74/w1/SC2Sources/report.md` | this report (same body as `w1/SC2Sources.md`) |
| `.ufo/waves/round-74/w1/SC2Sources/SC2Sources.md` | binding file inside seat directory |
| `.ufo/waves/round-74/w1/SC2Sources.md` | wave-level report |

Registry state measured before drafting: 308 rows, last id **S308**, `malformed = 0`, duplicate ids none,
tier `A=292 B=5 C=11`, status `mined=275 queued=5 rejected=28`, 91 knowledge `.md` notes. Collision checks
for the candidate URLs (`src/shared/unit-file.c`, `src/core/load-fragment.c`, `src/shared/unit-file.h`,
`wiki.archlinux.org/title/Systemd`, `unit-load.c`) each printed `0`.

## Verification I actually ran

```
# 1. Snapshot checksum verification against committed SHA256SUMS
cd .ufo/waves/round-74/before/src && sha256sum -c SHA256SUMS
  unit-file.c: OK      load-fragment.c: OK      unit-file.h: OK        (3/3 OK)

# 2. Declared instrument digests at seat start
# count-uf-rows-r74.py:   94d46a5edfcdc00858a1b1c37bc459322fc7e337fba19cc38a85776d0dd36482
# check-r73-routed-r74.py: 2da4ff1fd8e7ed1287230e43769a1d75233b992b9f04eeb77cc981f2677efd77

# 3. Selftest execution of both frozen instruments
python3 tools/count-uf-rows-r74.py --selftest
  -> SELFTEST: PASS (13 cases, 13 passed, 0 failed), rc 0
python3 tools/check-r73-routed-r74.py --selftest
  -> SELFTEST: PASS (6 cases, 6 passed, 0 failed), rc 0

# 4. Absence controls at base revision d749a625 and working tree HEAD
python3 tools/count-uf-rows-r74.py --revision d749a625
  -> UF_MAP absent, rc 128
python3 tools/count-uf-rows-r74.py --revision HEAD
  -> UF_NOTE absent, rc 128
python3 tools/check-r73-routed-r74.py --revision d749a625
  -> ROUTED_STALE=2 ROUTED_OK=0/2, rc 1

# 5. Candidate rejections live fetch & measurement
curl -sS -L --max-time 15 -o /tmp/archwiki-systemd.html -w '%{http_code} %{size_download}\n' https://wiki.archlinux.org/title/Systemd
  -> 200 152032, sha256 b26b7bb117b0f58a5987d033c00a3c81850640e03b37271e81527505f9fc9a6c
curl -sS -L -I --max-time 15 https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit-load.c
  -> HTTP/2 404 (Not Found)
curl -sS -L -I --max-time 15 https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-load.c
  -> HTTP/2 404 (Not Found)

# 6. Fixture evaluation of count-uf-rows-r74.py with simulated registry and valid UF1-UF6 rows
python3 tools/count-uf-rows-r74.py --fixture <mirror>
  UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0
  met=1 rc=0
```

`--fixture` proves the drafted rows S309-S311 bind to the snapshots and allow UF1-UF6 to evaluate to `met=1`;
it does not prove a commit.

## Findings

- **F1 (Anchor and URL binding held).** The frozen counter strictly checks that `rinfo["source_cell"]` contains
  the snapshot's `SOURCES.json` URL and `rinfo["anchor"]` contains the snapshot basename (`unit-file.c`,
  `load-fragment.c`, `unit-file.h`). In fixture tests, omitting or modifying either field triggered
  `registry row S309 does not cite URL ...` or `registry row S309 does not anchor unit-file.c`, yielding
  `UF_MALFORMED>0`, `UF_VERIFIED=0`, `met=0`, rc 1. The drafted rows adhere strictly to this schema.
- **F2 (Honest rejections: S312 and S313).**
  - **S312** (`https://wiki.archlinux.org/title/Systemd`): Fetched live (152032 bytes, HTTP 200). A broad community
    administration guide discussing symlink operations for `default.target` and preset overrides. It provides zero
    specification of internal unit fragment resolution, search path priority, symlink alias rejection rules,
    `UnitFileState` enumeration, or perpetual unit mask immunity. Status: `rejected` (community tier B).
  - **S313** (`https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit-load.c`): Fetched live (HTTP 404
    Not Found; checked also at `src/shared/unit-load.c` -> 404). In upstream systemd v262, unit fragment resolution
    and loading logic reside in `src/core/load-fragment.c`, `src/shared/unit-file.c`, and `src/core/unit.c`. There is
    no `unit-load.c`. Status: `rejected` (code tier A).
- **F3 (Snapshot vocabulary and C tokenization).** The C1 instrument requires statements to share ≥6 tokens
  and ≥50% of statement tokens with the cited snapshot, where tokens are extracted via `[A-Za-z][A-Za-z0-9_-]{3,}`
  minus a stopword list. In small snapshots like `unit-file.h` (80 lines, 2550 bytes), identifiers like
  `UNIT_FILE_ENABLED` or `UNIT_SERVICE` do not tokenize to separate words like "enabled" or "service". Statements
  must use exact code identifiers to clear the shared token threshold.
- **F4 (Entailment of unit_type_may_alias).** In `unit-file.h:25-32`, the function `unit_type_may_alias` permits
  aliasing strictly for: `UNIT_SERVICE`, `UNIT_SOCKET`, `UNIT_TARGET`, `UNIT_DEVICE`, `UNIT_TIMER`, and `UNIT_PATH`.
  The declared claim in SCORECARD.md mistakenly included "volume" and omitted "timer"/"path". S311 and the Gate quotes
  anchor the true code in `unit-file.h:25-32`.
- **F5 (Row quote syntax constraints).** `ROW_RE` in `count-uf-rows-r74.py` uses `quote="([^"]*)"`. Any quote
  containing escaped C string quotes (e.g. `\"%s\"`) breaks row parsing. The drafted quotes avoid strings with
  escaped quotes and use clean comment or statement spans. Multi-line comment quotes preserve the literal ` * `
  continuation markers under whitespace normalization.
- **F6 (Snapshot reuse limit).** `MAX_SNAPSHOT_REUSE = 2` requires exactly two rows per snapshot across the six
  rows: UF1 and UF2 cite `unit-file.c` (S309), UF3 and UF4 cite `unit-file.h` (S311), UF5 and UF6 cite
  `load-fragment.c` (S310).

## Overlap and dependencies (for the L1)

- **Registry rows draft ready.** Rows S309-S313 are formatted with 11 cells, no interior pipes, and valid kinds
  (`code`, `code`, `code`, `community`, `code`). They can be appended verbatim to `corpus/SOURCES.md` after S308.
- **Commit requirement.** S309-S311 cite `corpus/knowledge/systemd-unit-fragment-plane-r74.md` in `used-by`. The
  note and rows must land in the same commit to avoid missing used-by path warnings during census.
- **Gate quotes and Search log ready.** The `gate.md` text provides the complete `## Gate` section for
  `corpus/lessons/round-74.md` and the Rule-5 search log paragraph for `corpus/SOURCES.md`.

## Bounds observed

Leaf seat: no subagents dispatched. No `git` mutating commands (`commit`, `add`, `push`, `reset`, `checkout`),
no `jj` commands, no package transactions, no tool installs. All writes confined to this seat's wave directory
and `.ufo/waves/round-74/w1/SC2Sources.md`.

## Artifact paths

- `.ufo/waves/round-74/w1/SC2Sources/rows.md`
- `.ufo/waves/round-74/w1/SC2Sources/gate.md`
- `.ufo/waves/round-74/w1/SC2Sources/report.md`
- `.ufo/waves/round-74/w1/SC2Sources/SC2Sources.md`
- `.ufo/waves/round-74/w1/SC2Sources.md`
