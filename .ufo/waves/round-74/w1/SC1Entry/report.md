# SC1Entry Report — Round 74 w1

**Seat:** SC1Entry (scribe)  
**Lane:** tsukuroi-shokunin  
**Round:** 74 (hyaku run 15), wave w1  
**Declaration commit:** `e51fb49d1790ef283b6aad6752a8c12fac347377` (declared base `d749a625f483c66f2a6f2005db3799630c776bc3`, real base `d749a625b3054b7cb3435983fb9626ab3d0ed0c4`)  
**Milestone:** C1 knowledge entry draft: six UF rows in the frozen row format plus host prose and limits  
**Judged on:** depth, C1, note  

---

## 1. Executive Summary & Verdict

- **Drafted Knowledge Note:** `.ufo/waves/round-74/w1/SC1Entry/systemd-unit-fragment-plane-r74.md` (to land at `corpus/knowledge/systemd-unit-fragment-plane-r74.md`).
- **Row Counter Evaluation:** Tested against `tools/count-uf-rows-r74.py --fixture <mirror>`:
  `UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0 met=1`, exit code `0`.
- **Sources & Snapshots:** Exactly 3 snapshots cited exactly twice each:
  - `unit-file.c` (S309): rows UF1, UF2
  - `unit-file.h` (S311): rows UF3, UF4
  - `load-fragment.c` (S310): rows UF5, UF6
- **Entailment & Traps Averted:**
  - **F1 (UF3 "volume" wording trap):** Declaration claim text erroneously listed "service, socket, target, device, and volume units". The pinned snapshot `unit-file.h:25-32` actually admits `{service, socket, target, device, timer, path}`. UF3 uses the true set and notes that volume units cannot carry aliases, satisfying both entailment and token-sharing gates (share ratio 0.54).
  - **F4 (Quote formatting & double quotes):** All quotes avoid internal `"` characters (which break `ROW_RE`), are between 4 and 25 words, and match verbatim in normalized snapshot text.
- **Host Readings:** Live host readings re-measured read-only on 2026-11-04. Matched `before/host.txt` byte-for-byte. Additionally identified live alias symlink `/usr/lib/systemd/system/systemd-sysupdate.timer -> systemd-sysupdate-update.timer` confirming `UNIT_TIMER` aliasing.

---

## 2. Pinned Snapshots & Integrity Verification

Snapshots located under `.ufo/waves/round-74/before/src/`:

| Snapshot | Source ID | Upstream URL (tag v262) | SHA-256 Digest | Bytes |
|---|---|---|---|---|
| `unit-file.c` | S309 | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.c` | `141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd` | 36,245 |
| `load-fragment.c` | S310 | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/load-fragment.c` | `a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5` | 243,452 |
| `unit-file.h` | S311 | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.h` | `e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f` | 2,550 |

Verification command:
```bash
sha256sum -c .ufo/waves/round-74/before/src/SHA256SUMS
```
Output:
```
unit-file.c: OK
load-fragment.c: OK
unit-file.h: OK
```

---

## 3. Six UF Rows Specification

The six rows conforming to the frozen regex `ROW_RE`:

```markdown
| id | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| UF1 | Unit search paths are walked in priority order and a name already registered is skipped, so the first-seen copy wins | source=S309 | snapshot=unit-file.c | digest=141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd | quote="Search paths are ordered by priority (highest first), and we need to maintain this order." |
| UF2 | unit_validate_alias_symlink_or_warn returns ELOOP for a unit self-alias and EXDEV when the symlink target name type does not match source | source=S309 | snapshot=unit-file.c | digest=141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd | quote="-EXDEV if the target filename is not a valid unit name or doesn't match the source," |
| UF3 | unit_type_may_alias admits only UNIT_SERVICE UNIT_SOCKET UNIT_TARGET UNIT_DEVICE UNIT_TIMER UNIT_PATH so volume units can never carry aliases | source=S311 | snapshot=unit-file.h | digest=e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f | quote="static inline bool unit_type_may_alias(UnitType type) { return IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH);" |
| UF4 | UnitFileState separates UNIT_FILE_ENABLED from UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED from UNIT_FILE_LINKED_RUNTIME, and UNIT_FILE_MASKED from UNIT_FILE_MASKED_RUNTIME | source=S311 | snapshot=unit-file.h | digest=e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f | quote="UNIT_FILE_ENABLED, UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED, UNIT_FILE_LINKED_RUNTIME, UNIT_FILE_ALIAS, UNIT_FILE_MASKED, UNIT_FILE_MASKED_RUNTIME," |
| UF5 | a null_or_empty fragment sets load_state to UNIT_MASKED and zero fragment_mtime except that perpetual units load as UNIT_LOADED instead | source=S310 | snapshot=load-fragment.c | digest=a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5 | quote="u->load_state = u->perpetual ? UNIT_LOADED : UNIT_MASKED; /* don't allow perpetual units to ever be masked */ u->fragment_mtime = 0;" |
| UF6 | missing fragments for system-scope units fall back to builtin_unit_lookup while on-disk files and masks unconditionally override built-ins | source=S310 | snapshot=load-fragment.c | digest=a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5 | quote="const char *data = builtin_unit_lookup(u->id);" |
```

### Row Token Analysis & Gate Verification

| Row | Words (≥12) | Tokens | Shared Tokens (≥6) | Share Ratio (≥0.50) | Quote Words (4..25) | Quote Verbatim | Gate Verdict |
|---|---|---|---|---|---|---|---|
| UF1 | 20 | 13 | 8 (`already`, `order`, `paths`, `priority`, `search_path`, `skipped`, `unit`, `walked`) | 0.62 | 15 | Yes (`unit-file.c:416`) | PASS |
| UF2 | 19 | 12 | 12 (`alias`, `eloop`, `exdev`, `match`, `name`, `returns`, `self-alias`, `source`, `symlink`, `target`, `type`, `unit_validate_alias_symlink_or_warn`) | 1.00 | 16 | Yes (`unit-file.c:73-74`) | PASS |
| UF3 | 16 | 13 | 7 (`in_set`, `unit_device`, `unit_path`, `unit_service`, `unit_socket`, `unit_target`, `unit_timer`, `unit_type_may_alias`) | 0.54 | 14 | Yes (`unit-file.h:25-32`) | PASS |
| UF4 | 12 | 8 | 7 (`unit_file_enabled`, `unit_file_enabled_runtime`, `unit_file_linked`, `unit_file_linked_runtime`, `unit_file_masked`, `unit_file_masked_runtime`, `unitfilestate`) | 0.88 | 7 | Yes (`unit-file.h:8-14`) | PASS |
| UF5 | 18 | 13 | 12 (`fragment`, `fragment_mtime`, `instead`, `load_state`, `null_or_empty`, `perpetual`, `sets`, `unit_loaded`, `unit_masked`, `units`, `zero`) | 0.92 | 20 | Yes (`load-fragment.c:6250-6251`) | PASS |
| UF6 | 17 | 13 | 9 (`builtin_unit_lookup`, `files`, `fragments`, `masks`, `missing`, `on-disk`, `override`, `system-scope`, `units`) | 0.69 | 5 | Yes (`load-fragment.c:6291`) | PASS |

---

## 4. Mechanical Counter Verification Receipt

Tested against `tools/count-uf-rows-r74.py` in a hermetic scratch mirror (`$TMPDIR=/fast/scratch/hyaku/tsukuroi-r74/SC1Entry`):

Command:
```bash
python3 tools/count-uf-rows-r74.py --fixture "$S/mirror"
```

Output:
```
UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0 met=1
rc=0
```

Selftest verification of the counter:
```bash
python3 tools/count-uf-rows-r74.py --selftest
```
Output:
```
SELFTEST: PASS (13 cases, 13 passed, 0 failed)
```

---

## 5. Host Re-measurement (Read-Only)

Executed on 2026-11-04; all observations confirmed identical to `.ufo/waves/round-74/before/host.txt`:

1. **Systemd Version:**
   `systemd 262 (262.1-1-arch)`, Linux kernel `7.2.11-arch1-1`.
2. **System Search Paths (`systemd-analyze unit-paths`):**
   12 paths matching `before/host.txt` lines 4–16.
3. **Masked Units (`systemctl list-unit-files --state=masked --no-legend`):**
   - `passim.service` (masked disabled)
   - `systemd-networkd-wait-online.service` (masked enabled)
4. **Active Instance Units (`systemctl list-units --type=service | grep '@'`):**
   - `dirmngr@etc-pacman.d-gnupg.service`
   - `systemd-fsck@dev-disk-by\x2duuid-86D8\x2dC3F6.service`
   - `user-runtime-dir@1000.service`
   - `user@1000.service`
5. **Empirical Alias Discovery (closing round-73 limit):**
   `systemctl show -p Id -p Names -p FragmentPath systemd-sysupdate.timer` reports:
   - `Id=systemd-sysupdate-update.timer`
   - `Names=systemd-sysupdate-update.timer systemd-sysupdate.timer`
   - `FragmentPath=/usr/lib/systemd/system/systemd-sysupdate-update.timer`
   `ls -l /usr/lib/systemd/system/systemd-sysupdate.timer` confirms:
   `systemd-sysupdate.timer -> systemd-sysupdate-update.timer` (exercising `unit_type_may_alias` permitting `UNIT_TIMER`).

---

## 6. Known Limits & Findings

1. **Declaration Wording Trap on UF3 (F1):** The frozen declaration statement mentions "service, socket, target, device, and volume units". In the authoritative snapshot `unit-file.h:25-32`, the set is `UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH`. Volume is not a unit type in systemd v262. The drafted row UF3 states the authoritative code set while addressing volume units as non-aliasable.
2. **Base Object Hash Drift (F2):** The declared full OID `d749a625f483c66f2a6f2005db3799630c776bc3` does not exist in the git object database (fatal rc 128); the actual commit object is `d749a625b3054b7cb3435983fb9626ab3d0ed0c4` (short `d749a625`).
3. **Perpetual Mask Immunity:** Cannot be tested destructively by masking perpetual units (`-.slice`, `system.slice`) on a production host; it remains a code-grounded guarantee from `load-fragment.c:6250`.
4. **Built-in Fallback:** Cannot be observed live for standard units because core units are installed as regular files under `/usr/lib/systemd/system/`.

---

## 7. Artifact Paths

- **Drafted Knowledge Entry:** `.ufo/waves/round-74/w1/SC1Entry/systemd-unit-fragment-plane-r74.md`
- **Seat Report:** `.ufo/waves/round-74/w1/SC1Entry/report.md`
- **Scoped Summary / Binding:** `.ufo/waves/round-74/w1/SC1Entry.md`
