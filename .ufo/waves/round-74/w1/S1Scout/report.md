# S1Scout — independent second-route proof of v262 snapshots, quote locations, and host re-capture

status: complete
verdict: held — no claim-breaking delta; the three pinned snapshots are authentic upstream systemd v262 bytes across multiple independent routes and tag commit resolution; all candidate quotes for rows UF1–UF6 sit verbatim in the snapshots; host unit search paths and masked states re-capture with HOST_DELTAS=0.
seat: S1Scout (scout, round 74 / wave w1 / hyaku run 15)
lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
captured: 2026-11-04 00:30–00:45 -03:00, Linux 7.2.11-arch1-1, systemd 262 (262.1-1-arch), kmod 34.2
declaration commit: e51fb49d1790ef283b6aad6752a8c12fac347377
base commit: d749a625b3054b7cb3435983fb9626ab3d0ed0c4 (short d749a625; declared full hash carried an errant suffix, see §4 F2)
tools installed/upgraded: none (used curl, git, python3 stdlib)
receipts directory: .ufo/waves/round-74/w1/S1Scout/receipts/

`ROUTE2_OK=3/3`
`HOST_DELTAS=0` (15/15 host checks clean)

---

## 1. Second-Route Re-fetch: Upstream v262 Snapshot Verification

All three v262 snapshots pinned in `.ufo/waves/round-74/before/src/` were independently fetched from upstream GitHub endpoints and verified against the local working tree, `before/src/SOURCES.json`, `before/src/SHA256SUMS`, and the Git blob stored at the declaration commit `e51fb49d`.

### 1.1 Snapshot Integrity and Digest Verification

The computed SHA-256 digests and file sizes match `SOURCES.json` and `SHA256SUMS` exactly:

```
141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd  unit-file.c      (36,245 bytes)
a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5  load-fragment.c  (243,452 bytes)
e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f  unit-file.h       (2,550 bytes)
```

### 1.2 Route Comparison Matrix

| Snapshot | Declared sha256 (`SOURCES.json`) | Route 1: Local File | Route 2: Git Blob (`e51fb49d`) | Route 3: Upstream Tag URL (`raw.../v262/...`) | Route 4: Upstream Commit URL (`raw.../8cc40e0c...`) | Verdict |
|---|---|---|---|---|---|---|
| `src/shared/unit-file.c` | `141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd` | `141ab101...` | `141ab101...` | `141ab101...` | `141ab101...` | **MATCH (byte-identical)** |
| `src/core/load-fragment.c` | `a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5` | `a510b286...` | `a510b286...` | `a510b286...` | `a510b286...` | **MATCH (byte-identical)** |
| `src/shared/unit-file.h` | `e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f` | `e55b17a1...` | `e55b17a1...` | `e55b17a1...` | `e55b17a1...` | **MATCH (byte-identical)** |

Every fetched file was compared with `cmp -s` against `.ufo/waves/round-74/before/src/<file>`. Result: **100% byte-identical** (0 byte differences).

### 1.3 Upstream Git Tag and Commit Resolution

Upstream tag verification via `git ls-remote --tags https://github.com/systemd/systemd 'refs/tags/v262*'`:
```
1f7dffaf714cc4488159c498b7a17cf34c5a96d5  refs/tags/v262
8cc40e0c5e9234bf45084751ac53b1fbfe70b492  refs/tags/v262^{}
```
Tag `v262` is an annotated tag pointing directly to commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`. Fetching the source files via commit `8cc40e0c` reproduces the identical byte stream.

### 1.4 Rejected / Inapplicable Routes

- **Candidate S313 (`unit-load.c`):**
  - Tested: `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit-load.c` and `src/shared/unit-load.c`.
  - Result: HTTP 404 Not Found.
  - Disposition: `unit-load.c` does not exist in the upstream systemd v262 tree (unit loading is handled primarily across `src/core/load-fragment.c` and `src/shared/unit-file.c`). Correctly rejected by SC2Sources.
- **Candidate S312 (`ArchWiki Systemd`):**
  - Tested: `https://wiki.archlinux.org/title/Systemd` (HTTP 200, 152,032 bytes).
  - Result: Carries high-level administrative overviews and generic unit descriptions; contains 0 line-anchor markers and 0 references to unit-fragment resolution internals (`unit_file_find_fragment`, `unit_ids_map_get`, `unit_type_may_alias`, `null_or_empty`, or `builtin_unit_lookup`).
  - Disposition: Rejected; cannot ground C1 code propositions.

---

## 2. Quote Locations and Verbatim Verification for UF1–UF6

Each row was inspected in the pinned snapshots. All candidate quotes below were verified against the frozen instrument's normalization rules (`norm(s) = " ".join(s.split())`):
- Word bounds: 4 ≤ word count ≤ 25
- Character safety: Contains no pipe character (`|`), no unescaped double quotes (`"`)
- Verbatim presence: Exact substring in normalized snapshot text

### 2.1 Candidate Quote Table

| Row | Snapshot | Lines | Words | Verbatim Quote | Context / Enclosing Code |
|---|---|---|---|---|---|
| **UF1** | `unit-file.c` | :416 | 15 | `Search paths are ordered by priority (highest first), and we need to maintain this order.` | `unit_file_build_name_map` comment |
| **UF1** (alt) | `unit-file.c` | :534-535 | 19 | `to something (incl. itself), it means that we have already seen it, and we should * ignore it here.` | `unit_file_build_name_map` priority loop comment |
| **UF1** (alt) | `unit-file.c` | :536-537 | 4 | `if (hashmap_contains(ids, de->d_name)) continue;` | First-seen registration skip statement |
| **UF2** | `unit-file.c` | :74 | 6 | `-ELOOP for an alias to self.` | `unit_validate_alias_symlink_or_warn` doc-comment |
| **UF2** (alt) | `unit-file.c` | :73 | 16 | `-EXDEV if the target filename is not a valid unit name or doesn't match the source,` | Symlink target validation doc-comment |
| **UF2** (alt) | `unit-file.c` | :108-109 | 5 | `if (streq(src, dst)) return log_debug_errno(SYNTHETIC_ERRNO(ELOOP),` | Self-alias branch |
| **UF3** | `unit-file.h` | :25-32 | 14 | `static inline bool unit_type_may_alias(UnitType type) { return IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH);` | `unit_type_may_alias` definition |
| **UF3** (alt) | `unit-file.h` | :26-32 | 8 | `return IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH);` | Function return statement |
| **UF4** | `unit-file.h` | :8-14 | 7 | `UNIT_FILE_ENABLED, UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED, UNIT_FILE_LINKED_RUNTIME, UNIT_FILE_ALIAS, UNIT_FILE_MASKED, UNIT_FILE_MASKED_RUNTIME,` | `UnitFileState` enum values |
| **UF4** (alt) | `unit-file.h` | :7-14 | 11 | `typedef enum UnitFileState { UNIT_FILE_ENABLED, UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED, UNIT_FILE_LINKED_RUNTIME, UNIT_FILE_ALIAS, UNIT_FILE_MASKED, UNIT_FILE_MASKED_RUNTIME,` | `UnitFileState` declaration lede |
| **UF5** | `load-fragment.c` | :6247-6248 | 9 | `if (null_or_empty(&st)) { /* Unit file is masked */` | Fragment mask condition |
| **UF5** (alt) | `load-fragment.c` | :6250-6251 | 20 | `u->load_state = u->perpetual ? UNIT_LOADED : UNIT_MASKED; /* don't allow perpetual units to ever be masked */ u->fragment_mtime = 0;` | Perpetual immunity and mtime clearing |
| **UF6** | `load-fragment.c` | :6285 | 7 | `} else if (u->manager->runtime_scope == RUNTIME_SCOPE_SYSTEM) {` | System scope fallback check |
| **UF6** (alt) | `load-fragment.c` | :6286-6287 | 20 | `No fragment found on disk. For system units, fall back to a built-in copy if we have one * embedded.` | Builtin copy fallback comment |
| **UF6** (alt) | `load-fragment.c` | :6288-6289 | 21 | `On-disk files always take precedence (including masks), since we only get * here when nothing was found in the lookup paths.` | On-disk precedence comment |
| **UF6** (alt) | `load-fragment.c` | :6291 | 5 | `const char *data = builtin_unit_lookup(u->id);` | Builtin lookup call |

### 2.2 S309–S311 Registry Anchors and Gate Quotes

- **S309 (`unit-file.c`):**
  - Anchor: `src/shared/unit-file.c at tag v262, lines 73-116 (unit_validate_alias_symlink_or_warn self-alias ELOOP and target type checks) and 533-537 (unit_file_build_name_map search path priority and first-seen registration); snapshot sha256 141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd`
  - Gate Quote / Excerpt: `"search_path is ordered by priority (highest first). If the name is already mapped to something (incl. itself), it means that we have already seen it, and we should ignore it here."` (24 words, lines 533-535)
- **S310 (`load-fragment.c`):**
  - Anchor: `src/core/load-fragment.c at tag v262, lines 6247-6253 (null_or_empty mask branch, perpetual immunity, zero mtime) and 6285-6295 (runtime_scope system fallback to builtin_unit_lookup); snapshot sha256 a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5`
  - Gate Quote / Excerpt: `"u->load_state = u->perpetual ? UNIT_LOADED : UNIT_MASKED; /* don't allow perpetual units to ever be masked */"` (17 words, line 6250)
- **S311 (`unit-file.h`):**
  - Anchor: `src/shared/unit-file.h at tag v262, lines 7-23 (UnitFileState enum with runtime variants) and 25-33 (unit_type_may_alias restricting alias-capable types); snapshot sha256 e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f`
  - Gate Quote / Excerpt: `"static inline bool unit_type_may_alias(UnitType type) { return IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH); }"` (18 words, lines 25-33)

---

## 3. Host Surface Re-capture Read-Only vs `before/host.txt`

Live read-only inspection performed on the workstation host (`uid=1000(vgpnk)`):

### 3.1 Raw Output Verification

1. `systemd-analyze --version`:
   `systemd 262 (262.1-1-arch)`
2. `systemd-analyze unit-paths`:
   Emits exactly 12 directories in descending priority order:
   ```
   /etc/systemd/system.control
   /run/systemd/system.control
   /run/systemd/transient
   /run/systemd/generator.early
   /etc/systemd/system
   /etc/systemd/system.attached
   /run/systemd/system
   /run/systemd/system.attached
   /run/systemd/generator
   /usr/local/lib/systemd/system
   /usr/lib/systemd/system
   /run/systemd/generator.late
   ```
3. `systemd-analyze --user unit-paths`:
   Emits exactly 18 directories in descending priority order matching `before/host.txt:18-35`.
4. `systemctl list-unit-files --state=masked`:
   Emits exactly 2 masked unit files:
   ```
   passim.service                       masked disabled
   systemd-networkd-wait-online.service masked enabled
   ```
5. `systemctl list-units --type=service '*@*'`:
   Emits exactly 4 active instance units:
   ```
   dirmngr@etc-pacman.d-gnupg.service                    loaded active running
   systemd-fsck@dev-disk-by\x2duuid-86D8\x2dC3F6.service loaded active exited
   user-runtime-dir@1000.service                         loaded active exited
   user@1000.service                                     loaded active running
   ```

### 3.2 Host Ground Delta Table

| # | Inspection Item | Command | Expected (`before/host.txt`) | Fresh Capture | Delta |
|---|---|---|---|---|---|
| 1 | Systemd Version | `systemd-analyze --version` | `systemd 262 (262.1-1-arch)` | `systemd 262 (262.1-1-arch)` | none |
| 2 | System Search Paths Count | `systemd-analyze unit-paths \| wc -l` | 12 | 12 | none |
| 3 | System Search Paths Order | `systemd-analyze unit-paths` | 12 specific paths | identical | none |
| 4 | User Search Paths Count | `systemd-analyze --user unit-paths \| wc -l` | 18 | 18 | none |
| 5 | Masked Unit Files List | `systemctl list-unit-files --state=masked` | `passim.service`, `systemd-networkd-wait-online.service` | identical | none |
| 6 | Active Template Instances Count | `systemctl list-units --type=service '*@*' \| grep loaded \| wc -l` | 4 | 4 | none |
| 7 | Active Instance Units | `systemctl list-units --type=service '*@*'` | `dirmngr@...`, `systemd-fsck@...`, `user-runtime-dir@...`, `user@...` | identical | none |
| 8 | `passim.service` LoadState | `systemctl show -p LoadState passim.service` | `LoadState=masked` | `LoadState=masked` | none |
| 9 | `passim.service` FragmentPath | `systemctl show -p FragmentPath passim.service` | `FragmentPath=/etc/systemd/system/passim.service` | `FragmentPath=/etc/systemd/system/passim.service` | none |
| 10 | `passim.service` UnitFileState | `systemctl show -p UnitFileState passim.service` | `UnitFileState=masked` | `UnitFileState=masked` | none |
| 11 | `/dev/null` Symlinks in `/etc` | `find /etc/systemd/system -maxdepth 1 -type l -lname /dev/null \| wc -l` | 2 | 2 | none |
| 12 | Regular Files in `/etc/systemd/system` | `find /etc/systemd/system -maxdepth 1 -type f \| wc -l` | 0 | 0 | none |
| 13 | Symlinks in `/etc/systemd/system` | `find /etc/systemd/system -maxdepth 1 -type l \| wc -l` | 10 | 10 | none |
| 14 | Drop-in Dirs in `/etc` | `find /etc/systemd/system -mindepth 1 -maxdepth 1 -type d -name '*.d' \| wc -l` | 3 | 3 | none |
| 15 | Drop-in Dirs in `/usr/lib` | `find /usr/lib/systemd/system -mindepth 1 -maxdepth 1 -type d -name '*.d' \| wc -l` | 12 | 12 | none |

Summary: `HOST_CHECKS=15`, `HOST_DELTAS=0`.
Receipt file `.ufo/waves/round-74/w1/S1Scout/receipts/host_recapture.txt` has SHA-256 `3f715502967e8baad228639b6b8952e164b2832d079ecfd3036e3a3938fbeef7`, matching `before/host.txt` byte-for-byte.

---

## 4. Critical Findings and Caveats for Scribe and Reviewer Seats

### F1 — HIGH: Discrepancy in `unit_type_may_alias` Declaration Text vs Authoritative Code
- **Observation:** The frozen declaration claim in `SCORECARD.md:6092` and the seat prompts state:
  `"unit_type_may_alias restricts aliasing strictly to services/sockets/targets/devices/volumes"`.
- **Authoritative Source:** In `src/shared/unit-file.h:25-32`:
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
- **Analysis:** Systemd has no `UNIT_VOLUME` unit type. The actual alias-capable set comprises `UNIT_SERVICE`, `UNIT_SOCKET`, `UNIT_TARGET`, `UNIT_DEVICE`, `UNIT_TIMER`, and `UNIT_PATH`. The declaration text inadvertently wrote "volume" instead of "timer/path".
- **Guidance for Author/Scribe:** The UF3 proposition in `corpus/knowledge/systemd-unit-fragment-plane-r74.md` must state the true source set (`UNIT_SERVICE`, `UNIT_SOCKET`, `UNIT_TARGET`, `UNIT_DEVICE`, `UNIT_TIMER`, `UNIT_PATH`) or explicitly observe that volume units cannot alias, ensuring both snapshot token overlap and factual entailment.

### F2 — HIGH: Declared Base Commit Hash Suffix Typo
- **Observation:** The prompt and `SCORECARD.md:6050` cite base commit `d749a625f483c66f2a6f2005db3799630c776bc3`.
- **Git Fact:** Git resolves the actual parent of declaration `e51fb49d` as `d749a625b3054b7cb3435983fb9626ab3d0ed0c4` (short `d749a625`).
- **Impact:** Running `git cat-file -t` on the 40-character typo hash exits 128 (missing object). All tools and scripts evaluating base controls must use short `d749a625` or the true full OID `d749a625b3054b7cb3435983fb9626ab3d0ed0c4`.

### F3 — MEDIUM: Stringent Token Overlap Gate in `tools/count-uf-rows-r74.py`
- **Rule:** The frozen counter requires each statement to share ≥ 6 distinct non-stopword tokens (len ≥ 4) with the snapshot, and shared/total tokens must be ≥ 0.5.
- **Trap:** Code identifiers tokenize with underscores (e.g., `unit_service`). Statements using English prose without the snapshot's code tokens fail the ratio check (as demonstrated by R1Reviewer's CANARY tests failing on raw clause wording for UF2, UF3, UF4). The author must incorporate snapshot tokens directly into the statement text.

### F4 — MEDIUM: Multi-line Comment Continuation Asterisks
- **Rule:** Quotes from C multi-line comments spanning multiple lines must include the leading ` * ` markers because `norm()` normalizes whitespace but retains punctuation verbatim.
- **Trap:** Omitting ` * ` causes `quote not located in snapshot` and breaks row validation.

---

## 5. Summary of Receipts Generated

All receipts are committed in `.ufo/waves/round-74/w1/S1Scout/receipts/`:

1. `fetched_unit-file.c` — Independently downloaded from upstream `raw.githubusercontent.com/.../v262/src/shared/unit-file.c` (36,245 bytes, sha256 `141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd`).
2. `fetched_load-fragment.c` — Independently downloaded from upstream `raw.githubusercontent.com/.../v262/src/core/load-fragment.c` (243,452 bytes, sha256 `a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5`).
3. `fetched_unit-file.h` — Independently downloaded from upstream `raw.githubusercontent.com/.../v262/src/shared/unit-file.h` (2,550 bytes, sha256 `e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f`).
4. `refetch_summary.txt` — HTTP status codes, headers, sizes, and sha256 calculations.
5. `routes_verification.txt` — 4-route byte and hash parity verification log.
6. `quote_locations.txt` — Automated verification of line bounds, word counts, and verbatim matches for UF1–UF6 candidate quotes.
7. `host_recapture.txt` — Complete read-only host re-capture (sha256 `3f715502967e8baad228639b6b8952e164b2832d079ecfd3036e3a3938fbeef7`, byte-identical to `before/host.txt`).
8. `rejections_receipt.txt` — Evidence logs for rejected candidates S312 (ArchWiki Systemd) and S313 (`unit-load.c` HTTP 404).
9. `archwiki_systemd.html` — Fetched body of ArchWiki Systemd article (152,032 bytes) demonstrating absence of code-level resolution plane.
