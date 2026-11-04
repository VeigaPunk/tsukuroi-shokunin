# R1Reviewer — round-74 w1 — per-row UF entailment review (tsukuroi, hyaku run 15)

Seat: R1Reviewer (reviewer, leaf — no dispatch). Inputs: declaration `e51fb49d1790ef283b6aad6752a8c12fac347377`, pinned snapshots `.ufo/waves/round-74/before/src/{unit-file.c,load-fragment.c,unit-file.h}` + `SOURCES.json` + `SHA256SUMS`, instruments `tools/count-uf-rows-r74.py` and `tools/check-r73-routed-r74.py` (both frozen at the declaration), registry `corpus/SOURCES.md` (308 rows at base).

Status: **FINAL for the six proposed rows.** SC1Entry's draft note landed at `.ufo/waves/round-74/w1/SC1Entry/systemd-unit-fragment-plane-r74.md`; per-row verdicts in §6 are computed on those exact bytes (receipt `rows-final-receipt.txt`), with an independent reproduction of the frozen counter's `met=1` over those bytes. Remaining open item: registry rows S309-S311 had not landed in `corpus/SOURCES.md` at review close (REGISTRY_ROWS_ABSENT), so source-cell resolution against the real registry is the integrator's check (F4 states the required cell layout).

## 1. Verification basis (receipts)

- **Snapshot integrity, two routes.** Local `sha256sum` of the three pinned snapshots equals `SOURCES.json` digests and `SHA256SUMS`, and equals S1Scout's independent second-route re-fetches (`w1/S1Scout/receipts/fetched_*`):
  - `unit-file.c` `141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd` (36245 bytes)
  - `load-fragment.c` `a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5` (243452 bytes)
  - `unit-file.h` `e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f` (2550 bytes)
- **Frozen C1 counter.** `--selftest` = `SELFTEST: PASS (13 cases, 13 passed, 0 failed)` (requires a non-`/tmp` `TMPDIR`; see F5). Working tree at review time: `UF_NOTE absent`, rc 128. Base `d749a625`: `UF_MAP absent`, rc 128 — matches `before/absence-controls.txt`.
- **Frozen C2 checker at base `d749a625`**: `ROUTED_STALE=2 ROUTED_OK=0/2`, rc 1, reasons = real base state (gate section absent; LOG token `14` missing). Matches the frozen before-state.
- Harness: `rowcheck.py` (this seat dir) mirrors the counter's tokenizer/STOP set, word bounds, and quote-location rule; output receipt `rowcheck-receipt.txt`.

## 2. Findings, by severity

### F1 — HIGH (C1/UF3 entailment): the frozen C1 claim misstates v262 `unit_type_may_alias`

Committed claim (SCORECARD.md:6092, also the wave dispatch text): "`unit_type_may_alias` permits aliasing strictly for **service, socket, target, device, and volume** units". The pinned v262 header (unit-file.h:25-32, digest-verified) says:

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

The alias-capable set is **{service, socket, target, device, timer, path}**. "Volume" is wrong (no volume in the set) and "timer"/"path" are omitted. Consequence: a UF3 row that parrots the frozen wording is **not entailed** by its pinned snapshot; a row that states the true set contradicts the frozen claim text. The author seat must write the true set; the round then needs an erratum/flag noting the declaration's own misstatement (the claim is frozen, the source is authoritative). Verdict on the committed clause as worded: **NOT ENTAILED**. Verdict on the corrected clause: **ENTAILED** (quote below).

### F2 — HIGH (evidence chain/attack): the declared base full hash is unresolvable, and base controls pass vacuously under it

- Declared everywhere (SCORECARD.md:6050 in committed bytes, plus w1-dispatch.json/w1-spec.json and all 12 seat prompts): base `d749a625f483c66f2a6f2005db3799630c776bc3`.
- `git cat-file -t d749a625f483c66f2a6f2005db3799630c776bc3` → fatal, rc 128 (object absent). The real base is `d749a625b3054b7cb3435983fb9626ab3d0ed0c4` (short `d749a625`; it is the parent of the declaration commit).
- This git's `rev-parse --verify` accepts even the all-zeros OID (existence unchecked for full OIDs), so `cat-file` is the arbiter.
- **Vacuous-control demonstration (run, not inferred):**
  - C1 counter with the bogus hash: `UF_MAP absent` rc 128 — byte-identical to the true-base control, wrong reason (missing object, not absent note/map).
  - C2 checker with the bogus hash: `ROUTED_STALE=2 ROUTED_OK=0/2` rc 1 — the expected base numbers, for the wrong reason (`lesson file absent`/`LOG.md absent` instead of the true base's `section absent`/`missing token '14'`).
- Anyone scripting the frozen predicate with the declared full hash gets indistinguishable "before" evidence from a nonexistent tree. Receipts should cite `d749a625` (short) or `d749a625b3054b7cb3435983fb9626ab3d0ed0c4`. This is a dispatch/declaration pointer defect, not a claim-content defect (the do-nothing controls at the real base are otherwise sound).

### F3 — MEDIUM (mechanical, UF2/UF3/UF4): the frozen token gate is vocabulary-strict; 3 of 6 committed clause wordings fail it as written

The counter shares distinct non-stopword tokens (len ≥ 4, lowercased) between the statement and the row's whole snapshot, requiring ≥ 6 shared and shared/total ≥ 0.5. `UNIT_SERVICE` tokenizes to `unit_service`, so prose words like "service" do **not** match code identifiers; hyphenation and word form matter (`self-aliases` ≠ `self-alias`, `reject` ≠ `rejecting`). Canaries (committed clause wording vs intended snapshot):

| clause | snapshot | shared/total | ratio | gate |
|---|---|---|---|---|
| UF1 | unit-file.c | 7/13 | 0.54 | PASS |
| UF2 | unit-file.c | 4/12 | 0.33 | **FAIL** |
| UF3 | unit-file.h | 2/10 | 0.20 | **FAIL** |
| UF4 | unit-file.h | 1/8 | 0.12 | **FAIL** |
| UF5 | load-fragment.c | 7/12 | 0.58 | PASS |
| UF6 | load-fragment.c | 9/13 | 0.69 | PASS |

Statements must embed the snapshot's identifier vocabulary. Verified PASSing statement shapes per row are in §4 (all six ≥ 12 words, ≥ 6 shared, ratio ≥ 0.5).

### F4 — MEDIUM (authoring traps for the rows; both proven against the frozen counter, `fx_probe-receipt.txt`)

- **Escaped quotes break the row parser (PROVEN, probe T1).** `ROW_RE` is `quote="([^"]*)"` — a quote containing C string literals with `\"` (e.g. `"%s: symlink target name type \"%s\" does not match source, rejecting."`, unit-file.c:122) terminates the field early → `malformed row shape` + `non-contiguous IDs` → `UF_MALFORMED=2`, `met=0`, rc 1. UF2's natural log-message quotes are unusable; use the comment/code quotes in §4.
- **Multi-line block comments keep their ` * ` markers (PROVEN, probe T2).** Under whitespace-only normalization a quote spanning continuation lines must include them; the asterisk-less variant of the UF6 override sentence yields `quote not located in snapshot load-fragment.c`, `met=0`, rc 1.
- **Quote word bounds are 4..25.** `u->fragment_mtime = 0;` alone is 3 words (fails); use the 20-word span at load-fragment.c:6250-6251.
- **Snapshot reuse cap is 2**: 6 rows over 3 snapshots forces exactly 2 rows per snapshot — e.g. UF1+UF2 → unit-file.c, UF3+UF4 → unit-file.h, UF5+UF6 → load-fragment.c.
- **Registry cell placement** (counter's parse): the URL must be in the **Title** cell (parts[2]) and the snapshot basename in the **Location** cell (parts[6]) of S309-S311, mirroring S304-S306.

### F5 — LOW (instrument ops)

`count-uf-rows-r74.py --selftest` exits 2/`SELFTEST-HERMETIC` when `TMPDIR=/tmp` or unset (frozen hermeticity guard; R2Reviewer's `selftest-counter.txt` receipt shows the trip). With a real non-`/tmp` `TMPDIR` it passes 13/13 (this seat's `selftest-counter.txt`). Not a defect; an operational precondition worth stating in receipts.

## 3. Per-clause entailment verdicts against the pinned sources (PROVISIONAL on clause wording)

| row | clause (committed C1 wording) | snapshot anchor | verdict |
|---|---|---|---|
| UF1 | search paths in priority order; first-seen name registration ignores lower duplicates | unit-file.c:416 (`Search paths are ordered by priority (highest first)...`), :533-537 (already-mapped skip + `hashmap_contains(ids, de->d_name)) continue;`), :577 (`hashmap_ensure_put(&ids, ...)` first write wins) | **ENTAILED** |
| UF2 | symlinks reject self-aliases; validate target name types | unit-file.c:73-74 (`-EXDEV if the target filename is not a valid unit name or doesn't match the source,` / `-ELOOP for an alias to self.`), :108-111 (streq self-alias → ELOOP), :117-137 (dst name-type/instance/suffix EXDEV rejections) | **ENTAILED** |
| UF3 | `unit_type_may_alias` permits aliasing strictly for service, socket, target, device, and volume units | unit-file.h:25-32 — actual set is service, socket, target, device, **timer, path** | **NOT ENTAILED as worded** (F1); corrected wording entailed |
| UF4 | `UnitFileState` distinguishes enabled/linked/masked from runtime variants | unit-file.h:5-19 enum: `UNIT_FILE_ENABLED`/`_RUNTIME`, `UNIT_FILE_LINKED`/`_RUNTIME`, `UNIT_FILE_MASKED`/`_RUNTIME` | **ENTAILED** |
| UF5 | `null_or_empty` fragment sets `UNIT_MASKED` + zero mtime; perpetual units immune | load-fragment.c:6247-6251 (`if (null_or_empty(&st))` → `u->load_state = u->perpetual ? UNIT_LOADED : UNIT_MASKED; /* don't allow perpetual units to ever be masked */` → `u->fragment_mtime = 0;`) | **ENTAILED** |
| UF6 | missing system-scope fragments fall back to `builtin_unit_lookup`; on-disk files and masks unconditionally override built-ins | load-fragment.c:6285 (`} else if (u->manager->runtime_scope == RUNTIME_SCOPE_SYSTEM) {`), :6286-6289 (comment: "No fragment found on disk. For system units, fall back to a built-in copy... On-disk files always take precedence (including masks)..."), :6291 (`const char *data = builtin_unit_lookup(u->id);`) | **ENTAILED** (override is definitional: the builtin branch is reached only when nothing was found in the lookup paths) |

## 4. Verified quotes and statement shapes (all mechanically PASS; ready for the author)

Quotes are whitespace-normalized verbatim (with required ` * ` markers); line anchors are 1-based snapshot lines. Statements pass 12-word / ≥6-token / ≥0.5-share gates (receipt: `rowcheck-receipt.txt`). **End-to-end dry run:** a fixture note built from exactly these six statements+quotes+digests, with S309/S310/S311 laid out per F4, satisfies the frozen counter at `UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0 met=1` rc 0 (`fx_probe-receipt.txt`, CONTROL case).

- **UF1** (unit-file.c) quote q1 :416 `Search paths are ordered by priority (highest first), and we need to maintain this order.` (15w) or q2 :534-535 `to something (incl. itself), it means that we have already seen it, and we should * ignore it here.` (19w). Statement (0.62): `Unit search paths are walked in priority order and a name already registered is skipped, so the first-seen copy wins`
- **UF2** (unit-file.c) quote :73-74 `-EXDEV if the target filename is not a valid unit name or doesn't match the source,` (16w) or `-ELOOP for an alias to self.` (6w) or :108-109 `if (streq(src, dst)) return log_debug_errno(SYNTHETIC_ERRNO(ELOOP),` (5w). Do NOT quote the `\"%s\"` log strings (F4). Statement (1.00): `unit_validate_alias_symlink_or_warn returns ELOOP for a unit self-alias and EXDEV when the symlink target name type does not match source`
- **UF3** (unit-file.h) quote :25-32 `static inline bool unit_type_may_alias(UnitType type) { return IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH);` (14w). Statement (0.54): `unit_type_may_alias admits only UNIT_SERVICE UNIT_SOCKET UNIT_TARGET UNIT_DEVICE UNIT_TIMER UNIT_PATH so volume units can never carry aliases`
- **UF4** (unit-file.h) quote :8-14 `UNIT_FILE_ENABLED, UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED, UNIT_FILE_LINKED_RUNTIME, UNIT_FILE_ALIAS, UNIT_FILE_MASKED, UNIT_FILE_MASKED_RUNTIME,` (7w). Statement (0.88): `UnitFileState separates UNIT_FILE_ENABLED from UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED from UNIT_FILE_LINKED_RUNTIME, and UNIT_FILE_MASKED from UNIT_FILE_MASKED_RUNTIME`
- **UF5** (load-fragment.c) quote :6250-6251 `u->load_state = u->perpetual ? UNIT_LOADED : UNIT_MASKED; /* don't allow perpetual units to ever be masked */ u->fragment_mtime = 0;` (20w) or :6247-6248 `if (null_or_empty(&st)) { /* Unit file is masked */` (9w). Statement (0.92): `a null_or_empty fragment sets load_state to UNIT_MASKED and zero fragment_mtime except that perpetual units load as UNIT_LOADED instead`
- **UF6** (load-fragment.c) quote :6286-6287 `No fragment found on disk. For system units, fall back to a built-in copy if we have one * embedded.` (20w) or :6288-6289 `On-disk files always take precedence (including masks), since we only get * here when nothing was found in the lookup paths.` (21w) or :6291 `const char *data = builtin_unit_lookup(u->id);` (5w). Statement (0.69): `missing fragments for system-scope units fall back to builtin_unit_lookup while on-disk files and masks unconditionally override built-ins`

## 5. FINAL per-row verdicts (on landed draft bytes, `.ufo/waves/round-74/w1/SC1Entry/systemd-unit-fragment-plane-r74.md`)

Reviewed-bytes pin: sha256 `5daaa9f7046ccad5a913d0edab411500b3397b2c96a38191bf3e0726edc37bb4` (rechecked after review; registry rows S309-S311 still absent, corpus path still draft-only at that time).

Mechanical checks (receipt `rows-final-receipt.txt`): every row passes word count ≥ 12 (12..20 words), token sharing ≥ 6 distinct non-stopword tokens and ratio ≥ 0.5 (ratios 0.54–1.00), `digest=` equals both the `SOURCES.json` digest and the actual snapshot bytes (`digest_ok=True` ×6), quotes are verbatim in the pinned snapshots at the cited lines (UF1 :416, UF2 :73, UF3 :25-32, UF4 :8-14, UF5 :6250-6251, UF6 :6291), 4..25 words, no pipes, ids contiguous 1..6, snapshot reuse exactly 2 each, sources/snapshots 3/3. Frozen counter over these exact bytes (fixture scaffold): `UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0 met=1`, rc 0 — independently reproducing SC1Entry's claim.

| row | word count | shared/ratio | digest ok | quote (verbatim @ lines) | entailment | verdict |
|---|---|---|---|---|---|---|
| UF1 | 20 | 8/13 = 0.62 | yes | yes @ unit-file.c:416 | search-path priority + contains-skip + first `hashmap_ensure_put` wins (:416, :533-537, :577) | **ENTAILED — PASS** |
| UF2 | 19 | 12/12 = 1.00 | yes | yes @ unit-file.c:73 | `-EXDEV` target-name comment + `-ELOOP` self-alias branch (:73-74, :108-111, :117-137) | **ENTAILED — PASS** |
| UF3 | 16 | 7/13 = 0.54 | yes | yes @ unit-file.h:25-32 | TRUE six-type set {service, socket, target, device, timer, path}; negative "volume can never carry aliases" is correct (F1 avoided) | **ENTAILED — PASS** |
| UF4 | 12 | 7/8 = 0.88 | yes | yes @ unit-file.h:8-14 | enum pairs ENABLED/LINKED/MASKED vs *_RUNTIME (:5-19) | **ENTAILED — PASS** |
| UF5 | 18 | 12/13 = 0.92 | yes | yes @ load-fragment.c:6250-6251 | `null_or_empty` → `UNIT_MASKED`, `fragment_mtime = 0`, perpetual → `UNIT_LOADED` (:6247-6251) | **ENTAILED — PASS** |
| UF6 | 17 | 9/13 = 0.69 | yes | yes @ load-fragment.c:6291 | `RUNTIME_SCOPE_SYSTEM` branch + builtin_unit_lookup + "On-disk files always take precedence (including masks)" (:6285-6291) | **ENTAILED — PASS** |

Caveats carried into integration: (a) rows reference S309/S310/S311 which must appear in `corpus/SOURCES.md` with the map URL in the Title cell and the snapshot basename in the Location cell (F4) before the frozen counter passes against the real repo — at review close those registry rows were still absent; (b) UF3's correctness is measured against the pinned v262 header, and per F1 the round record should note that the frozen declaration's own clause-3 wording ("volumes") is wrong, so no seat "corrects" the row back to the declaration text.

## 6. Residual risk and verification gaps

- Registry integration is the one open predicate: rows cite S309/S310/S311, which must land in `corpus/SOURCES.md` with the map URL in the Title cell and the snapshot basename in the Location cell (F4); those rows were absent at review close, so the frozen counter over the real repo cannot yet return `met=1` — the integrator should run `python3 tools/count-uf-rows-r74.py` (working tree) once both land.
- F1 requires a round-record erratum: the frozen declaration's clause-3 wording ("service, socket, target, device, and volume units") misstates the pinned v262 header ({service, socket, target, device, timer, path}). The landed UF3 row states the true set — no seat should "fix" it back to the declaration text.
- F2 should be corrected or erratum'd in the wave record: the declared base full hash `d749a625f483c66f2a6f2005db3799630c776bc3` is not an object in this repo (real base `d749a625b3054b7cb3435983fb9626ab3d0ed0c4`); base controls run with the declared hash pass vacuously (proven in §F2).
- C2 freshness closure, host probes, and the mutation battery belong to other seats and were not re-verified here.
