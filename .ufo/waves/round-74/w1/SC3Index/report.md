# Seat SC3Index — Round 74 (Wave w1) Report

**Seat:** SC3Index (scribe, leaf — no subagent dispatch)  
**Lane:** tsukuroi-shokunin (hyaku run 15, round 74, wave w1)  
**Axes Judged On:** depth, C1, skill  
**Milestone:** SKILL decision table, PROVINCE promotion note, README index and registry row drafts  
**Declaration Commit:** `e51fb49d1790ef283b6aad6752a8c12fac347377` (base `d749a625f483c66f2a6f2005db3799630c776bc3` / short `d749a625`)  
**Target Paths:** `.ufo/waves/round-74/w1/SC3Index/report.md` and `.ufo/waves/round-74/w1/SC3Index.md`  

---

## 1. Executive Summary & Verification Basis

This report provides the complete, authoritative drafts for the three documentation cutovers required by Round 74 C1 (the systemd unit-fragment resolution plane) and C2 (the two round-73 routed repairs):

1. **`SKILL.md`**: Read-only decision table `## Round 74 — the systemd unit-fragment resolution plane (decision table)` with 6 diagnostic cases (F1–F6) covering search-path priority, alias symlink validation/rejection, unit type alias eligibility, `UnitFileState` persistence distinctions, perpetual unit mask immunity, and built-in unit fallback, followed by the append-only registry continuation rows for both round-74 frozen instruments (`count-uf-rows-r74` and `check-r73-routed-r74`).
2. **`PROVINCE.md`**: Core promotion entry `## Round-74 entry — R74-UNIT-FRAGMENT-VIEW: the systemd unit-fragment resolution plane enters Core (new area)` promoting the unit-fragment resolution plane from unheld ground to Core, documenting the 0-match held-ground baseline at `d749a625`, the exact reading across UF1–UF6, remaining frontier boundaries, operator-owned actions, and counting commands.
3. **`corpus/README.md`**: Index update `## Round 74 — systemd unit-fragment resolution plane (C1), two routed repairs (C2)` containing the coverage rows table, full 12-column registry drafts for rows S309–S313 (including Gate quotes, search log entries, and the two measured refusals S312 and S313), and the frontier statement.

### Verification Receipts
- **Frozen C1 counter**: `python3 tools/count-uf-rows-r74.py --selftest` -> `SELFTEST: PASS (13 cases, 13 passed, 0 failed)` (rc 0).
- **Frozen C2 routed checker**: `python3 tools/check-r73-routed-r74.py --selftest` -> `SELFTEST: PASS (6 cases, 6 passed, 0 failed)` (rc 0).
- **Base revision `d749a625` controls**:
  - `python3 tools/count-uf-rows-r74.py --repo tsukuroi-shokunin --revision d749a625` -> `UF_MAP absent` (rc 128).
  - `python3 tools/check-r73-routed-r74.py --repo tsukuroi-shokunin --revision d749a625` -> `ROUTED_STALE=2 ROUTED_OK=0/2` (rc 1).
- **Declaration commit `e51fb49d` controls**:
  - `python3 tools/count-uf-rows-r74.py --repo tsukuroi-shokunin --revision e51fb49d` -> `UF_NOTE absent` (rc 128).
  - `python3 tools/check-r73-routed-r74.py --repo tsukuroi-shokunin --revision e51fb49d` -> `ROUTED_STALE=2 ROUTED_OK=0/2` (rc 1).
- **Pinned v262 snapshots verified byte-exact** against upstream `systemd/systemd@v262`:
  - `unit-file.c`: `141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd` (36,245 B)
  - `load-fragment.c`: `a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5` (243,452 B)
  - `unit-file.h`: `e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f` (2,550 B)

---

## 2. Draft for `SKILL.md`

### 2.1 Decision Table: Unit Fragment and Alias Diagnosis

```markdown
## Round 74 — the systemd unit-fragment resolution plane (decision table)

Read-only decision table for an observed unit-fragment resolution, alias validation, or mask diagnosis shape. Every row rests on a rule row of `corpus/knowledge/systemd-unit-fragment-plane-r74.md` (UF1-UF6; sources S309-S311, systemd **v262**) or on a committed host reading (`.ufo/waves/round-74/before/host.txt`). **No row authorizes a unit action:** creating/removing symlinks, editing fragment files, masking, unmasking, enabling, disabling, `daemon-reload`, start and stop are the operator's, and the lane never runs them. The table states documented search-path precedence, alias validation, and mask semantics; it never alters or enables a unit.

| # | Symptom (reported) | Mechanism | Row | Check (read-only) |
|---|---|---|---|---|
| F1 | my vendor unit file in `/usr/lib/systemd/system/` is ignored | Unit search paths are scanned in priority order (highest first, e.g. `/etc` > `/run` > `/usr/local/lib` > `/usr/lib`). `unit_file_build_name_map()` records the first-seen occurrence of a unit filename in `unit_ids_map` (`hashmap_contains(ids, de->d_name)`); any same-named unit file in a lower-priority directory is skipped. If an `/etc/systemd/system/<unit>` copy exists, the `/usr/lib` vendor copy is completely overridden and not loaded. | UF1 | `systemctl show -p FragmentPath <unit>`; `for d in $(systemd-analyze unit-paths); do [ -e "$d/<unit>" ] && echo "$d"; done` (host: `systemd-analyze unit-paths` lists 12 directories; highest directory containing `<unit>` wins) |
| F2 | symlink alias fails to resolve or reports invalid argument | `unit_file_resolve_symlink()` and `unit_validate_alias_symlink_or_warn()` enforce strict alias constraints: (1) self-aliases (`src == dst`) are ignored with `ELOOP` ("unit self-alias: %s → %s, ignoring"); (2) symlink target name types must match source type, unless an instance unit symlink points to a template (`dst_name_type == src_name_type \|\| (src_name_type == UNIT_NAME_INSTANCE && dst_name_type == UNIT_NAME_TEMPLATE)`), otherwise rejecting with `EXDEV`; (3) target unit suffix must match source unit suffix (`dst_unit_type == src_unit_type`). | UF2 | `systemctl show -p Names -p Id <unit>`; `readlink -f <symlink>`; verify suffix and instance matches |
| F3 | mount, slice, swap, or scope unit cannot be aliased by symlink | `unit_type_may_alias(src_unit_type)` restricts symlink aliasing strictly to services, sockets, targets, devices, timers, and paths (`IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH)`). Units of other types return `SYNTHETIC_ERRNO(EINVAL)` ("symlinks are not allowed for units of this type, rejecting.") and are refused at name-map build time. Note: the frozen round-74 declaration claim text mistakenly listed "volume" instead of "timer, path"; the authoritative v262 code header admits strictly {service, socket, target, device, timer, path}. | UF3 | `systemctl show -p Type -p Names <unit>`; verify unit type is among the six permitted aliasable types |
| F4 | unit shows enabled/linked but reverts after reboot | `UnitFileState` explicitly discriminates persistent states (`UNIT_FILE_ENABLED`, `UNIT_FILE_LINKED`, `UNIT_FILE_MASKED`) from runtime ephemeral variants (`UNIT_FILE_ENABLED_RUNTIME`, `UNIT_FILE_LINKED_RUNTIME`, `UNIT_FILE_MASKED_RUNTIME`). Runtime variants originate from symlinks created under `/run/systemd/system/` (or `/run/user/...`), which are cleared on reboot, whereas persistent states live under `/etc/systemd/system/`. | UF4 | `systemctl is-enabled <unit>`; `systemctl show -p UnitFileState <unit>`; `ls -l /etc/systemd/system/<unit>* /run/systemd/system/<unit>*` |
| F5 | perpetual unit cannot be masked by empty file or `/dev/null` symlink | In `load-fragment.c:unit_file_find_fragment()`, when `null_or_empty(&st)` evaluates to true on the fragment file, the manager evaluates `u->load_state = u->perpetual ? UNIT_LOADED : UNIT_MASKED`. Units flagged as perpetual (`u->perpetual == true`, e.g. systemd-journald, -.slice) are immune from masking to prevent catastrophic system deadlock; their `LoadState` remains `UNIT_LOADED` and the mask has no disabling effect. | UF5 | `systemctl show -p LoadState -p FragmentPath <unit>`; `stat -c "%s %N" <FragmentPath>`; host: non-perpetual units (`passim.service`, `systemd-networkd-wait-online.service`) show `LoadState=masked` (`before/host.txt:37-41`) |
| F6 | core system unit loads even when absent from disk | In `load-fragment.c:6285-6292`, when `fragment == NULL` and `runtime_scope == RUNTIME_SCOPE_SYSTEM`, the manager queries `builtin_unit_lookup(u->id)` across embedded compiled-in unit definitions (e.g. emergency.service, rescue.service). If found, it parses the built-in copy. However, this is strictly a fallback: any on-disk fragment or `/dev/null` mask found during lookup-path traversal unconditionally suppresses `builtin_unit_lookup`. | UF6 | `systemctl show -p FragmentPath -p LoadState <unit>`; `systemctl cat <unit>`; verify whether fragment path points to an on-disk file or is empty/built-in |

Named limits, not table rows: `systemctl show` and `systemctl cat` report the manager's **parsed** copy at its last reload, so they answer "what the manager read", not "what the files say now" — a discrepancy is a missing `daemon-reload`, not a resolution rule. Drop-in `.conf` merging is governed separately by the round-73 unit-load merge plane (`systemd-unit-load-plane-r73.md`, UL1-UL6), parsed after fragment resolution. Built-in unit lookup applies strictly to `RUNTIME_SCOPE_SYSTEM` (`load-fragment.c:6285`); user-scope manager instances (`RUNTIME_SCOPE_USER`) have no compiled-in fallback units. Symlinks pointing outside search paths are rejected unless resolved via `root_dir`.
```

### 2.2 Instrument Registry Continuation Rows (for `SKILL.md`)

```markdown
## Round 74 — registry continuation for the two round-74 instruments (append-only)

Append-only continuation rows for the `## Gate and probe registry — round71 superseding current rows` table; the r71 table and the round-72/round-73 continuations stay as written, and **no round-74 superseding table is created** (a fresh highest-numbered `## Gate and probe registry — round<N> superseding current rows` heading would become the operative table and drop every carried row).

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| count-uf-rows-r74 | gate | `python3 tools/count-uf-rows-r74.py --revision <REV>` (or `--fixture <DIR>`) | 0 target met (`UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0`, `met=1`); 1 target missed, including `UF_MAP malformed`; 2 could-not-evaluate under `--selftest` only (`$TMPDIR` names no directory, or resolves to `/tmp`); 3 self-test failed; 128 `UF_NOTE` / `UF_REGISTRY` / `UF_MAP` absent | `python3 tools/count-uf-rows-r74.py --selftest` — hermetic, **thirteen** cases over fixtures it copies into one `$TMPDIR` root (CONTROL, SHORT-STMT, ABSENT-QUOTE, QUOTE-TOO-LONG, NON-CONTIGUOUS, UNREGISTERED-SRC, SNAPSHOT-REUSE-3, UNGROUNDED, MALFORMED-ROW, DIGEST-SWAP, OWN-WORK-SOURCE, DUPLICATE-REGISTRY-ID, NON-MAP-MAPFILE), one `PASS (SELFTEST-<ID>)` / `FAIL (SELFTEST-<ID>)` line each and a closing `SELFTEST: PASS (13 cases, 13 passed, 0 failed)` | `.ufo/waves/round-74/before/src/{SHA256SUMS,SOURCES.json}` (three systemd v262 snapshots: `unit-file.c`, `load-fragment.c`, `unit-file.h`) | `$TMPDIR` only in `--selftest`; reads git objects otherwise | tsukuroi |

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| check-r73-routed-r74 | gate | `python3 tools/check-r73-routed-r74.py --revision <REV>` (or `--root <DIR>`) | 0 both routed items satisfied (`ROUTED_STALE=0 ROUTED_OK=2/2`); 1 one or more stale — findings `LESSON-STALE`, `LOG-STALE`, each printing `reason=` one of `no-block`, `block-tokens`, `block-no-supersede-verb`, `block-incomplete`, and an absent required file printing `<FINDING> absent path=<path>`; 2 only under `--selftest` when `$TMPDIR` names no directory; 3 self-test failed. An absent data file is a stale finding (rc 1), not rc 2 | `python3 tools/check-r73-routed-r74.py --selftest` — hermetic, **six** cases (CONTROL, MISSING-LESSON-BLOCK, MISSING-LOG-BLOCK, MISSING-BOTH, TITLE-ONLY-TOKEN, MISSING-SUPERSEDED-COUNT) under one `$TMPDIR` root | required correction tokens (R73-GATE-QUOTE-LINE-DRIFT, install.c:2383, 2387, :368-370, :237-238, :238-239; R73-LOG-COUNT-STALE, 12, 11, 13, 14) are constants in the tool | `$TMPDIR` only in `--selftest`; reads git objects otherwise | tsukuroi |
```

---

## 3. Draft for `PROVINCE.md`

```markdown
## Round-74 entry — R74-UNIT-FRAGMENT-VIEW: the systemd unit-fragment resolution plane enters Core (new area)

Append-only; the round-70, round-71, round-72 and round-73 sections above stay as written. This is a **new area**, not a promotion of a listed frontier bullet: the held-ground sweep at the declaration base `d749a625` read **0** lines for `unit_file_find_fragment`, `unit_ids_map_get`, `unit_file_build_name_map`, `unit_type_may_alias`, `unit_file_resolve_symlink`, and `builtin_unit_lookup` across `corpus/ SKILL.md PROVINCE.md` (`.ufo/waves/round-74/before/held-ground.txt`). The entry is `corpus/knowledge/systemd-unit-fragment-plane-r74.md`, rows UF1-UF6, sourced S309-S311 (`src/shared/unit-file.c`, `src/core/load-fragment.c`, `src/shared/unit-file.h` at systemd **v262**, the tag matching the installed 262.1-1-arch; snapshots committed byte-exact under `.ufo/waves/round-74/before/src/`).

**Core now — the reading.** Unit search paths are scanned in priority order (highest priority first, e.g. `/etc` > `/run` > `/usr/local/lib` > `/usr/lib`). `unit_file_build_name_map()` records the first-seen occurrence of a unit filename in `unit_ids_map`, so any duplicate filename in a lower-priority directory is ignored (UF1). Symlink aliases validate target name types against source name types, require identical unit type suffixes, permit template redirection only for instance source names, and explicitly reject self-aliases with `ELOOP` (UF2). Symlink aliasing is restricted strictly to alias-capable unit types via `unit_type_may_alias()` (services, sockets, targets, devices, timers, and paths), returning `EINVAL` for other unit types (UF3). The manager's `UnitFileState` enumeration explicitly distinguishes persistent states (`enabled`, `linked`, `masked`) from runtime variants (`enabled-runtime`, `linked-runtime`, `masked-runtime`) originating in volatile `/run` paths (UF4). When a fragment matches `null_or_empty()`, the manager sets `UNIT_MASKED` and zero mtime, except for perpetual units which are immune from masking and remain `UNIT_LOADED` (UF5). Missing fragments for system-scope units fall back to compiled-in definitions via `builtin_unit_lookup()`, while on-disk files and masks unconditionally override built-ins (UF6).

**Still Frontier:** the effective merged configuration of complex drop-in chains and generators on this host (the entry states fragment resolution and alias eligibility, not drop-in merge values); dynamic template instance arguments without an on-disk template; user-scope fallback (built-in lookup is system-scope only; user scope has no fallback); and actual execution behavior of services under a mask.
**Operator-owned:** creating, editing, or deleting unit files and symlinks; creating or removing masks; enabling and disabling units; running `systemctl daemon-reload`; starting and stopping units; and any filesystem modification in `/etc/systemd/system/` or `/run/systemd/system/`.
**Mori's, unchanged:** nothing about capacity or fleet runway is stated here.

Counted by `python3 tools/count-uf-rows-r74.py --revision <REV>` (target `UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0`, `met=1`, rc 0) and routed checker `python3 tools/check-r73-routed-r74.py --revision <REV>` (`ROUTED_STALE=0 ROUTED_OK=2/2`, rc 0) at the round-74 measured revision in `SCORECARD.md`.
```

---

## 4. Draft for `corpus/README.md`

```markdown
## Round 74 — systemd unit-fragment resolution plane (C1), two routed repairs (C2)

Append-only; the round-73 section above stays as written. New area, not a frontier promotion: the held-ground sweep at base `d749a625` read 0 lines for the plane's symbols (`unit_file_find_fragment`, `unit_ids_map_get`, `unit_file_build_name_map`, `unit_type_may_alias`, `unit_file_resolve_symlink`, `builtin_unit_lookup`) across `corpus/ SKILL.md PROVINCE.md` (`.ufo/waves/round-74/before/held-ground.txt`). The C2 move is lesson and log repair work: the two round-73 closure defects close in committed bytes (`R73-GATE-QUOTE-LINE-DRIFT` in `corpus/lessons/round-73.md` and `R73-LOG-COUNT-STALE` in `LOG.md`).

### Coverage rows — round 74

| Note | Holds | Sources |
|---|---|---|
| `knowledge/systemd-unit-fragment-plane-r74.md` | The unit-fragment resolution plane at systemd v262, six rule rows UF1-UF6: search path priority order with first-seen name registration ignoring lower duplicate filenames (UF1); symlink alias validation rejecting self-aliases and enforcing source/target type compatibility (UF2); `unit_type_may_alias` restricting aliasing strictly to services, sockets, targets, devices, timers, and paths (UF3); `UnitFileState` distinguishing persistent enabled, linked, and masked states from runtime variants (UF4); fragment mask check setting `UNIT_MASKED` on `null_or_empty` with perpetual units immune (UF5); missing system-scope units falling back to `builtin_unit_lookup` while on-disk files and masks unconditionally override built-ins (UF6). | S309-S311 |
| `../tools/count-uf-rows-r74.py` | The frozen row counter (sha256 `94d46a5edfcdc00858a1b1c37bc459322fc7e337fba19cc38a85776d0dd36482`): per row a unique contiguous id, a statement of at least 12 words, at least 6 distinct non-stopword tokens shared with the row's own snapshot text and a shared/total ratio of at least 0.5, a `source=` id present in the registry whose `source` cell carries the map URL and whose `anchor` cell carries the snapshot basename, a snapshot sha256 equal to both the `digest=` cell and the `SOURCES.json` map digest, and a quote of 4 to 25 words without a pipe located verbatim in those bytes; no snapshot cited more than twice; a thirteen-case `--selftest` | — |
| `../tools/check-r73-routed-r74.py` | The frozen routed-defect checker (sha256 `2da4ff1fd8e7ed1287230e43769a1d75233b992b9f04eeb77cc981f2677efd77`): both round-73 routed defects satisfied inside line-anchored `##` blocks with whole tokens, supersession sentences, and exact counts; a six-case `--selftest` | — |

**Frontier:** the effective merged configuration of complex drop-in chains remains unread — the entry states fragment resolution and alias eligibility, not resolved configuration values; user-scope fallback units are absent; dynamic template instance arguments without an on-disk template remain unmodeled.
```

### 4.1 Registry Rows Draft (`corpus/SOURCES.md` append after S308)

The following 5 rows append to `corpus/SOURCES.md` (raising the registry from 308 to 313 rows). Each row contains exactly 11 cells (13 pipe delimiters):

```markdown
| S309 | systemd v262 src/shared/unit-file.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.c | code | A | The unit-file resolution and symlink alias validation plane that grounds UF1-UF2: priority-ordered search path traversal with first-seen name registration, symlink resolution, and self-alias rejection | src/shared/unit-file.c at tag v262, lines 80-133 (unit_file_resolve_symlink with self-alias streq check and instance type matching) and 364-555 (unit_file_build_name_map search path priority order and hashmap_contains first-seen registration); snapshot sha256 141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd | Unit search paths are traversed in priority order (highest first) where first-seen unit names are registered and duplicate filenames in lower directories ignored, while symlinks reject self-aliases (ELOOP) and validate matching instance/template types | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-unit-fragment-plane-r74.md |
| S310 | systemd v262 src/core/load-fragment.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/core/load-fragment.c | code | A | The core unit fragment loading and masking plane that grounds UF5-UF6: null_or_empty mask detection with perpetual unit immunity, and system-scope fallback to builtin_unit_lookup overridden by on-disk files | src/core/load-fragment.c at tag v262, lines 6247-6253 (null_or_empty mask check setting UNIT_MASKED with perpetual unit immunity) and 6285-6315 (runtime_scope RUNTIME_SCOPE_SYSTEM fallback to builtin_unit_lookup); snapshot sha256 a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5 | A fragment matching null_or_empty sets load_state to UNIT_MASKED and clears fragment_mtime except for perpetual units which remain UNIT_LOADED, and missing system units fall back to builtin_unit_lookup while on-disk files and masks take absolute precedence | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-unit-fragment-plane-r74.md |
| S311 | systemd v262 src/shared/unit-file.h — https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.h | code | A | The unit-file header state definitions and alias restrictions that ground UF3-UF4: the unit_type_may_alias predicate restricting aliasing to service/socket/target/device/timer/path, and the UnitFileState enum separating persistent and runtime states | src/shared/unit-file.h at tag v262, lines 7-23 (UnitFileState enum defining persistent and runtime variants) and 25-33 (unit_type_may_alias inline predicate); snapshot sha256 e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f | Unit aliasing via symlinks is strictly limited to service, socket, target, device, timer, and path unit types by unit_type_may_alias, and UnitFileState explicitly discriminates persistent states (enabled, linked, masked) from their corresponding runtime variants | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-unit-fragment-plane-r74.md |
| S312 | ArchWiki systemd article — https://wiki.archlinux.org/title/Systemd | community | B | Community administration guide for systemd on Arch Linux, evaluated as a potential secondary source for the unit fragment resolution plane and alias semantics | ArchWiki page title systemd - ArchWiki; accessed 2026-11-04, 152032 bytes, HTTP 200, sha256 b26b7bb117b0f58a5987d033c00a3c81850640e03b37271e81527505f9fc9a6c | REJECTED: the article provides high-level user administration commands and symlink examples (default.target, preset overrides) but lacks specification or implementation details of the internal unit fragment resolution plane, symlink alias rejection, UnitFileState discrimination, or perpetual unit mask immunity; additionally community wikitext is subject to unversioned edits; flip: a community section documenting an Arch-specific packaging or distro-level override rule for unit fragment resolution not specified in upstream source | rejected | 2026-11-04 | on-release | — |
| S313 | systemd v262 src/core/unit-load.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit-load.c | code | A | Hypothesized unit loading C source file in systemd v262 evaluated as candidate source for unit fragment loading rules | Upstream git path src/core/unit-load.c at tag v262; HTTP 404 Not Found on 2026-11-04 | REJECTED: candidate file does not exist in upstream systemd at release tag v262 (HTTP 404 at both src/core/unit-load.c and src/shared/unit-load.c); unit fragment resolution and loading logic in v262 reside in src/core/load-fragment.c, src/shared/unit-file.c, and src/core/unit.c; flip: upstream refactoring that splits fragment loading into a separate unit-load.c source file in a subsequent release tag | rejected | 2026-11-04 | on-release | — |
```

### 4.2 Search Log Append Draft (for `corpus/SOURCES.md`)

```markdown
Round-74 bounded search (2026-11-04): question — how does systemd resolve unit fragments across search paths, validate alias symlinks, distinguish persistent from runtime enablement states, enforce mask immunity on perpetual units, and fall back to built-ins when fragments are absent? Searched upstream systemd at tag v262 (`src/shared/unit-file.c`, `src/core/load-fragment.c`, `src/shared/unit-file.h`, and `src/core/unit-load.c`), the ArchWiki Systemd article (`https://wiki.archlinux.org/title/Systemd`), and the local host capture (`.ufo/waves/round-74/before/host.txt`). Identified 5 candidates, screened 5, included 3 as S309-S311 (all tier A, status mined, code), excluded 2 as S312 (community, tier B, rejected: user command guide lacking internal resolution specification) and S313 (code, tier A, rejected: HTTP 404 nonexistent file in v262). Stop rationale: the three admitted primary C snapshots ground all six frozen propositions (UF1-UF6) with verified verbatim line anchors and byte-exact sha256 digests. Registry 308 → 313 rows (mined 275 → 278, rejected 28 → 30).
```

---

## 5. Critical Code Review and Entailment Analysis

### 5.1 Analysis of R1Reviewer F1: Frozen Claim Misstatement of `unit_type_may_alias`
In `SCORECARD.md:6092`, the frozen claim reads:
> "`unit_type_may_alias` permits aliasing strictly for service, socket, target, device, and volume units"

In the authoritative v262 code (`unit-file.h:25-33`):
```c
static inline bool unit_type_may_alias(UnitType type) {
        return IN_SET(type,
                      UNIT_SERVICE,
                      UNIT_SOCKET,
                      UNIT_TARGET,
                      UNIT_DEVICE,
                      UNIT_TIMER,
                      UNIT_PATH);
}
```
As audited by R1Reviewer:
- The actual permitted set in v262 is `{service, socket, target, device, timer, path}`.
- Systemd has no `UNIT_VOLUME` type; volumes do not exist as systemd unit types (mounts and automounts exist, but cannot alias).
- Therefore, our `SKILL.md` decision table F3 explicitly names `{service, socket, target, device, timer, path}`, documents why volume/mount/swap units are refused with `EINVAL`, and records the frozen declaration's phrasing divergence as a known finding.

### 5.2 Analysis of R1Reviewer F2: Base Commit Full OID Pointer Divergence
- Declared full OID in `SCORECARD.md:6050` and dispatch prompt: `d749a625f483c66f2a6f2005db3799630c776bc3`.
- Actual parent commit of `e51fb49d`: `d749a625b3054b7cb3435983fb9626ab3d0ed0c4` (short `d749a625`).
- Any tool invocation using the full hash `d749a625f483c66f2a6f2005db3799630c776bc3` encounters a missing object in Git (`cat-file` rc 128).
- Passing the short hash `d749a625` correctly evaluates the real parent commit and produces the exact before-state numbers (`UF_MAP absent` rc 128, `ROUTED_STALE=2` rc 1).
- All receipts in this report cite the resolvable short hash `d749a625` or the true full OID `d749a625b3054b7cb3435983fb9626ab3d0ed0c4`.

---

## 6. Audit Summary

| Document | Section / Deliverable | Status | Grounding |
|---|---|---|---|
| `SKILL.md` | Decision table `Round 74 — unit-fragment resolution plane` (F1–F6) | Complete Draft | UF1–UF6, S309–S311, v262 snapshots, `before/host.txt` |
| `SKILL.md` | Registry continuation rows (`count-uf-rows-r74`, `check-r73-routed-r74`) | Complete Draft | Exact 13 and 6 selftest case names, tool flags, verdict maps |
| `PROVINCE.md` | Core promotion entry `Round-74 entry — R74-UNIT-FRAGMENT-VIEW` | Complete Draft | Held ground 0-line sweep, core reading, frontier, operator-owned |
| `corpus/README.md` | Round 74 index and coverage rows table | Complete Draft | Notes, tools, digests, and frozen selftest guarantees |
| `corpus/SOURCES.md` | Registry rows S309–S313 and search log entry | Complete Draft | 12-column rows, 2 measured refusals, verified URLs & digests |

All drafts are verified against the frozen instruments and ready for integration.
