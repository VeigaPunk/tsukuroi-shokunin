# Round-74 registry rows — draft for append (SC2Sources)

State before appending, measured from the lane root on 2026-11-04:

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md          -> 308
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++}
  END{print n+0}' corpus/SOURCES.md                                          -> 0
awk -F'|' '/^\|[[:space:]]*S[0-9]+/ {print $2}' corpus/SOURCES.md | sort | uniq -d -> (empty)
grep -c 'src/shared/unit-file.c' corpus/SOURCES.md                            -> 0
grep -c 'src/core/load-fragment.c' corpus/SOURCES.md                          -> 0
grep -c 'src/shared/unit-file.h' corpus/SOURCES.md                            -> 0
grep -c 'wiki.archlinux.org/title/Systemd' corpus/SOURCES.md                  -> 0
grep -c 'unit-load.c' corpus/SOURCES.md                                       -> 0
```

Last used id is **S308**, so the three admitted rows take **S309-S311** and the two refusals take
**S312-S313**. The S309/S310/S311 assignment binds to the three v262 snapshots committed in
`.ufo/waves/round-74/before/src/` (`unit-file.c` -> S309, `load-fragment.c` -> S310, `unit-file.h` -> S311)
as defined in `SOURCES.json` and evaluated by the frozen instrument `tools/count-uf-rows-r74.py`.

Each row below is one line, 11 cells, no `|` inside a cell (split by `|` produces exactly 13 fields).
Copy verbatim into the registry table after S308. The three `used-by` paths name the C1 note; append the
rows and the note in the same commit, or the census check `mined rows whose used-by paths do not exist`
reports `missing:` for all three.

| S309 | systemd v262 src/shared/unit-file.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.c | code | A | The unit-file resolution and symlink alias validation plane that grounds UF1-UF2: priority-ordered search path traversal with first-seen name registration, symlink resolution, and self-alias rejection | src/shared/unit-file.c at tag v262, lines 80-133 (unit_file_resolve_symlink with self-alias streq check and instance type matching) and 364-555 (unit_file_build_name_map search path priority order and hashmap_contains first-seen registration); snapshot sha256 141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd | Unit search paths are traversed in priority order (highest first) where first-seen unit names are registered and duplicate filenames in lower directories ignored, while symlinks reject self-aliases (ELOOP) and validate matching instance/template types | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-unit-fragment-plane-r74.md |
| S310 | systemd v262 src/core/load-fragment.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/core/load-fragment.c | code | A | The core unit fragment loading and masking plane that grounds UF5-UF6: null_or_empty mask detection with perpetual unit immunity, and system-scope fallback to builtin_unit_lookup overridden by on-disk files | src/core/load-fragment.c at tag v262, lines 6247-6253 (null_or_empty mask check setting UNIT_MASKED with perpetual unit immunity) and 6285-6315 (runtime_scope RUNTIME_SCOPE_SYSTEM fallback to builtin_unit_lookup); snapshot sha256 a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5 | A fragment matching null_or_empty sets load_state to UNIT_MASKED and clears fragment_mtime except for perpetual units which remain UNIT_LOADED, and missing system units fall back to builtin_unit_lookup while on-disk files and masks take absolute precedence | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-unit-fragment-plane-r74.md |
| S311 | systemd v262 src/shared/unit-file.h — https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.h | code | A | The unit-file header state definitions and alias restrictions that ground UF3-UF4: the unit_type_may_alias predicate restricting aliasing to service/socket/target/device/timer/path, and the UnitFileState enum separating persistent and runtime states | src/shared/unit-file.h at tag v262, lines 7-23 (UnitFileState enum defining persistent and runtime variants) and 25-33 (unit_type_may_alias inline predicate); snapshot sha256 e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f | Unit aliasing via symlinks is strictly limited to service, socket, target, device, timer, and path unit types by unit_type_may_alias, and UnitFileState explicitly discriminates persistent states (enabled, linked, masked) from their corresponding runtime variants | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-unit-fragment-plane-r74.md |
| S312 | ArchWiki systemd article — https://wiki.archlinux.org/title/Systemd | community | B | Community administration guide for systemd on Arch Linux, evaluated as a potential secondary source for the unit fragment resolution plane and alias semantics | ArchWiki page title systemd - ArchWiki; accessed 2026-11-04, 152032 bytes, HTTP 200, sha256 b26b7bb117b0f58a5987d033c00a3c81850640e03b37271e81527505f9fc9a6c | REJECTED: the article provides high-level user administration commands and symlink examples (default.target, preset overrides) but lacks specification or implementation details of the internal unit fragment resolution plane, symlink alias rejection, UnitFileState discrimination, or perpetual unit mask immunity; additionally community wikitext is subject to unversioned edits; flip: a community section documenting an Arch-specific packaging or distro-level override rule for unit fragment resolution not specified in upstream source | rejected | 2026-11-04 | on-release | — |
| S313 | systemd v262 src/core/unit-load.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit-load.c | code | A | Hypothesized unit loading C source file in systemd v262 evaluated as candidate source for unit fragment loading rules | Upstream git path src/core/unit-load.c at tag v262; HTTP 404 Not Found on 2026-11-04 | REJECTED: candidate file does not exist in upstream systemd at release tag v262 (HTTP 404 at both src/core/unit-load.c and src/shared/unit-load.c); unit fragment resolution and loading logic in v262 reside in src/core/load-fragment.c, src/shared/unit-file.c, and src/core/unit.c; flip: upstream refactoring that splits fragment loading into a separate unit-load.c source file in a subsequent release tag | rejected | 2026-11-04 | on-release | — |

## Measurement log for the two refusals

```
# Candidate S312: ArchWiki Systemd article
curl -sS -L --max-time 15 -o /tmp/archwiki-systemd.html -w '%{http_code} %{size_download}\n' https://wiki.archlinux.org/title/Systemd
-> 200 152032
sha256sum /tmp/archwiki-systemd.html
-> b26b7bb117b0f58a5987d033c00a3c81850640e03b37271e81527505f9fc9a6c
grep -i '<title>' /tmp/archwiki-systemd.html
-> <title>systemd - ArchWiki</title>
grep -ci 'fragment\|symlink\|alias\|null_or_empty\|builtin\|perpetual' /tmp/archwiki-systemd.html
-> 9 (all 9 are user-facing symlink commands or target symlink pointers; 0 internal resolution rules)

# Candidate S313: Hypothesized upstream unit-load.c
curl -sS -L -I --max-time 15 https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit-load.c
-> HTTP/2 404 (Not Found)
curl -sS -L -I --max-time 15 https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-load.c
-> HTTP/2 404 (Not Found)
```

## Census projection

Simulated after appending S309-S313 to `corpus/SOURCES.md`:
- Total rows: **313 rows** (308 + 5)
- Malformed rows: **0**
- Duplicate IDs: **none**
- Tier counts: **A=296** (292 + 4), **B=6** (5 + 1), **C=11** (unchanged)
- Status counts: **mined=278** (275 + 3), **queued=5** (unchanged), **rejected=30** (28 + 2)
- Knowledge notes: **92** once `corpus/knowledge/systemd-unit-fragment-plane-r74.md` lands (91 at base)
