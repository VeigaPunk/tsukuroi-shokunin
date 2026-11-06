# MutGate — mutation test of the round-87 Limine path-pin gate

Seat: `MutGate` (w1, round 87). Lane: `tsukuroi-shokunin`, branch `master`.
Lane revision measured: `cefb4188b484329c4908a19a277f8fb120fb4f56`.
Candidate under test: `tools/check-limine-pins.py`, sha256
`bbcc874ac8143ffb9bd97e4d3e2dfd934af3d6573f741d8b8ee3c00ecda9b73c` (identical to the file copied into
scratch before and after the probe — see "Restoration evidence").
Frozen battery: `tools/limine-pin-battery-r87.py`, sha256
`f2551c8e8386d599e3c2aca8888d5fbb0351a5a399dc43dc448556e99361989d` (22 families, 4 cases each, 88 cases).
Reference gate (freeze control, never mutated): `.ufo/waves/round-87/before/controls/ref-gate-r87.py`,
sha256 `77504d34bc370b7eac48b8d40d0dcce38f76983cf6222480cb8743254668ea9c`.

Verdict: **candidate killed 26 of 30 single-point mutants; 4 survivors — 1 equivalent, 3 battery gaps.**
No host contact, no `sudo`, no `/boot` access, no commit; lane files untouched.

## 1. Detector baseline (pristine bytes)

```
$ python3 tools/limine-pin-battery-r87.py --gate $S/pristine.py --work $S/work --runs 3
families_passed 22/22 verdict met failed -
families_passed 22/22 verdict met failed -
families_passed 22/22 verdict met failed -
baseline rc=0
$ python3 tools/limine-pin-battery-r87.py --selftest
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
reference-gate     PASS families_passed=22
selftest PASS 5/5
battery-selftest rc=0
```

The detector is stable on pristine bytes, so a mutant that reads unmet is a kill, not a flake.

## 2. Method

30 mutants, each produced by exactly one literal replacement in a copy of the candidate
(`$S/gen.py` asserts the anchor occurs exactly once before writing; `mutants/<name>.diff` records the hunk).
Every mutant was run through the full battery (`--runs 1`, own `--work` dir) and through the gate's own
`--selftest`; the four survivors were re-run three times. No battery case produced `error` (no timeout,
no `bad-output`), so every kill is a semantic mismatch, not a crash.

Artifacts: `mutants/` (30 `.py` + 30 `.diff` + `manifest.json`), `receipts/` (per-mutant
`.battery.out`, `.selftest.out`, `mutants-table.md`, `survivor-probes.txt`), `gen.py`, `runone.sh`,
`probe.py`.

## 3. Per-mutant results (battery 22 families)

| mutant | rule | deleted -> inserted (single point) | battery | failed families | gate --selftest |
|---|---|---|---|---|---|
| `m01-comment-not-skipped` | R1 comment skip | `if not line or line[0] == "#":` -> `if not line:` | 22/22 met | - | PASS 14/14 |
| `m02-no-blank-strip` | R1 blank strip | `line = raw.replace("\r", "").strip(" \t")` -> `line = raw.replace("\r", "")` | 1/22 unmet | COMMENT-DECOY, GZ-RAW, HASH-LENGTH, HASH-NONHEX, HASH-UPPER, HOST-SHAPE, KEY-CASE, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MISSING, MULTI-FAULT, OPTIONAL-SKIP, PANIC-DEFAULT, PANIC-FIRST, PANIC-NO-ONLY, POSITIVE, SECUREBOOT, UNHASHED-DECOYS, UNRESOLVED, WHITESPACE-CRLF | FAIL 12/14 |
| `m03-key-case-sensitive` | R1 key case | `return line[:i].lower(), line[:i], line[i + 1:].lstrip(" \t")` -> `return line[:i], line[:i], line[i + 1:].lstrip(" \t")` | 21/22 unmet | KEY-CASE | FAIL 13/14 |
| `m04-first-hash` | R2 last # | `cut = tail.rfind("#")` -> `cut = tail.find("#")` | 21/22 unmet | LAST-HASH | PASS 14/14 |
| `m05-last-open-paren` | R2 first ( | `lp = value.find("(")` -> `lp = value.rfind("(")` | 22/22 met | - | PASS 14/14 |
| `m06-hash-127` | R3 128->127 | `if len(h) != 128 or not set(h) <= HEXDIGITS:` -> `... != 127 ...` | 1/22 unmet | 21 families (only MALFORMED-INPUT passes) | FAIL 3/14 |
| `m07-hash-129` | R3 128->129 | `if len(h) != 128 or not set(h) <= HEXDIGITS:` -> `... != 129 ...` | 1/22 unmet | 21 families (only MALFORMED-INPUT passes) | FAIL 3/14 |
| `m08-hex-lowercase-only` | R3 hex case | `HEXDIGITS = frozenset(string.hexdigits)` -> `frozenset("0123456789abcdef")` | 21/22 unmet | HASH-UPPER | FAIL 13/14 |
| `m09-any-resource-resolves` | R4 resource check | `if resource != "boot" or uri["root"] != "":` -> `if False:` | 20/22 unmet | MULTI-FAULT, UNRESOLVED | FAIL 13/14 |
| `m10-root-ignored` | R4 root check | `if resource != "boot" or uri["root"] != "":` -> `if resource != "boot":` | 21/22 unmet | UNRESOLVED | PASS 14/14 |
| `m11-gzip-decompress` | R5 gzip raw | chunked raw hash -> `gzip.decompress` when magic matches | 21/22 unmet | GZ-RAW | PASS 14/14 |
| `m12-missing-as-unresolved` | R5 missing->unresolved | `status="LP-MISSING"` -> `status="LP-UNRESOLVED"` | 20/22 unmet | MISSING, MULTI-FAULT | FAIL 13/14 |
| `m13-missing-as-ok` | R5 missing->OK | `status="LP-MISSING", consequence="not-modelled"` -> `status="OK", consequence="none"` | 20/22 unmet | MISSING, MULTI-FAULT | FAIL 13/14 |
| `m14-panic-last-wins` | R6 first panic | `if key == "hash_mismatch_panic" and panic_setting is None:` -> drop `and panic_setting is None` | 21/22 unmet | PANIC-FIRST | FAIL 13/14 |
| `m15-panic-default-prompt` | R6 panic default | `prompt = (... and not secure_boot)` -> `prompt = (panic_setting is None or (...))` | 14/22 unmet | GZ-RAW, KEY-CASE, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MULTI-FAULT, PANIC-DEFAULT, WHITESPACE-CRLF | FAIL 13/14 |
| `m16-panic-no-inverted` | R6 'no' compare | `... == "no" ...` -> `... != "no" ...` | 18/22 unmet | HOST-SHAPE, MULTI-FAULT, PANIC-FIRST, PANIC-NO-ONLY | FAIL 12/14 |
| `m17-secureboot-ignored` | R6 secure boot | drop `and not secure_boot` | 21/22 unmet | SECUREBOOT | FAIL 13/14 |
| `m18-optional-no-skip` | R6 optional skip | `consequence="skip" if optional else (...)` -> `consequence=(...)` | 21/22 unmet | OPTIONAL-SKIP | FAIL 13/14 |
| `m19-degraded-only-mismatch` | R7 fault set | `if statuses & set(FAULTS):` -> `if "LP-MISMATCH" in statuses:` | 19/22 unmet | HASH-LENGTH, HASH-NONHEX, MISSING | FAIL 12/14 |
| `m20-unresolved-precedence-first` | R7 precedence | swap DEGRADED / CANNOT-EVALUATE order | 21/22 unmet | MULTI-FAULT | PASS 14/14 |
| `m21-lines-0-based` | R7 line numbering | `enumerate(text.split("\n"), 1)` -> `, 0)` | 1/22 unmet | 21 families (only MALFORMED-INPUT passes) | FAIL 2/14 |
| `m22-cr-not-stripped` | R1 CR strip | `line = raw.replace("\r", "").strip(" \t")` -> `line = raw.strip(" \t")` | 21/22 unmet | WHITESPACE-CRLF | FAIL 13/14 |
| `m23-value-not-lstripped` | R1 value lstrip | `line[i + 1:].lstrip(" \t")` -> `line[i + 1:]` | 1/22 unmet | 21 families (only MALFORMED-INPUT passes) | FAIL 4/14 |
| `m24-entry-not-tracked` | R2 entry label | `entry = stripped.lstrip("/")... or entry` -> `entry = None` | 22/22 met | - | PASS 14/14 |
| `m25-panic-line-metadata-zero` | R6 panic line | `panic_setting = (lineno, value)` -> `(0, value)` | 22/22 met | - | PASS 14/14 |
| `m26-pin-keys-path-only` | R2 pin key set | `PIN_KEYS` -> `frozenset({"path"})` | 19/22 unmet | GZ-RAW, KEY-CASE, OPTIONAL-SKIP | FAIL 13/14 |
| `m27-optional-wallpaper-dropped` | R6 optional keys | `OPTIONAL_KEYS` -> `frozenset({"term_font"})` | 21/22 unmet | OPTIONAL-SKIP | FAIL 13/14 |
| `m28-hash-case-sensitive-compare` | R3 hash compare case | `if got == h.lower():` -> `if got == h:` | 21/22 unmet | HASH-UPPER | FAIL 13/14 |
| `m29-sha256-instead-of-blake2b` | R5 digest | `hashlib.blake2b()` -> `hashlib.sha256()` | 2/22 unmet | 20 families (only MALFORMED-INPUT, PANIC-FIRST pass) | FAIL 10/14 |
| `m30-last-pin-only` | R2 pin accumulation | `raw_pins.append(...)` -> `raw_pins[:] = [...]` (last pin wins) | 4/22 unmet | 18 families (only COMMENT-DECOY, MALFORMED-INPUT, PANIC-FIRST, UNHASHED-DECOYS pass) | PASS 14/14 |

Counts: **killed 26/30**, survivors 4/30, battery errors 0. The gate's own `--selftest` killed only
21/30 (it misses m04, m10, m11, m20, m30 as well), so the battery is doing real work beyond the
in-file selftest — but it leaves three behavioural gaps below.

## 4. Survivors

### 4.1 `m01-comment-not-skipped` — EQUIVALENT (not a gap)

The removed guard is unreachable: a line whose first non-blank character is `#` cannot pass
`split_key`'s `KEYCHARS` scan (`i == 0` -> `return None`), so both programs reject every `#` line.
Probe (`probe/m01`, comment decoys in four shapes plus one live pin):

```
m01 pristine (0, 'HEALTHY', [(6, 'OK', 'none', 'Linux')], None)
m01 mutant   (0, 'HEALTHY', [(6, 'OK', 'none', 'Linux')], None)
```

Byte-identical JSON. The battery's COMMENT-DECOY family only writes a `comment:` key line, which is
why it cannot see this guard at all; that is fine because the guard is redundant, not because the
family is wrong. No family proposed; the mutant is equivalent, not a coverage finding.

### 4.2 `m05-last-open-paren` — BATTERY GAP (R2: resource ends at the FIRST `(`)

A stored path may itself contain `(` and `)`; `rfind("(")` then finds the wrong parenthesis and the
pin is dropped silently, turning a mismatch into HEALTHY. Probe (`probe/m05`,
`path: boot():/EFI/Linux/a(1).efi#<correct>`):

```
m05 pristine (0, 'HEALTHY', [(2, 'OK', 'none', 'Linux')], None)
m05 mutant   (0, 'HEALTHY', [], None)
```

The mutant reports no pin at all and exits 0 — the worst failure shape for an operability gate.
No frozen family writes a `(`/`)` into a stored path.

Proposed family `PAREN-PATH` (in `proposed-battery-r87.patch`):

```python
def fam_paren_path(c):
    """R2: the resource ends at the FIRST '('; a stored path may itself contain '(' and ')'."""
    c.header()
    label = rname(c.rng, "")
    c.entry(label)
    rel = "EFI/Linux/%s(%d).efi" % (rname(c.rng, ""), c.rng.randrange(10))
    c.files[rel] = c.blob()
    c.pin("OK", rel=rel)
    c.pin("LP-MISMATCH", key="kernel_path", rel=rel)
```

### 4.3 `m24-entry-not-tracked` — BATTERY GAP (reported entry label never asserted)

The battery compares only `(line, status, consequence)` per pin; `entry` is never read. Probe
(`probe/m24`, two entries):

```
m24 pristine (0, 'HEALTHY', [(3,'OK','none','Linux'), (6,'OK','none','EFI fallback')], None)
m24 mutant   (0, 'HEALTHY', [(3,'OK','none',None),    (6,'OK','none',None)], None)
```

Proposed family `ENTRY-LABEL`, plus an opt-in `entry=` assertion in `Case.pin` so only this family
demands the field:

```python
def fam_entry_label(c):
    """The per-pin entry label is reported; sibling entries must not be confused."""
    c.header()
    for label in (rname(c.rng, ""), "EFI fallback", rname(c.rng, "")):
        c.entry(label)
        c.pin(c.rng.choice(["OK", "LP-MISMATCH"]), entry=label)
```

### 4.4 `m25-panic-line-metadata-zero` — BATTERY GAP (panic record's line never asserted)

`hash_mismatch_panic` is compared only indirectly through consequences (PANIC-FIRST). Probe
(`probe/m25`, setting on line 2, mismatch on line 3):

```
m25 pristine (1, 'DEGRADED', [(3,'LP-MISMATCH','prompt','Linux')], {'line': 2, 'value': 'no'})
m25 mutant   (1, 'DEGRADED', [(3,'LP-MISMATCH','prompt','Linux')], {'line': 0, 'value': 'no'})
```

Proposed family `PANIC-METADATA` (asserts the first occurrence's line/value; `set_panic` records the
expectation):

```python
def fam_panic_metadata(c):
    """The reported hash_mismatch_panic record names the first occurrence's line and value."""
    c.header()
    set_panic(c, c.rng.choice(["no", "NO", "No"]), indent="  ")
    c.entry()
    c.pin("LP-MISMATCH")
```

## 5. Proposed battery extension (validated in scratch, not applied)

`proposed-battery-r87.patch` (93 diff lines) against `tools/limine-pin-battery-r87.py` adds the three
families above, `Case.meta` expectations, and extends `run_gate`/the comparator. One rule keeps the
frozen reference gate valid: **a metadata field is judged only when the gate emits it** (the ref gate
prints `{verdict, rc, pins[{line,key,status,consequence}]}` and no `entry`/`hash_mismatch_panic`), so
the ref gate skips those assertions while a gate that emits a wrong value (the mutants) is killed.
L1 decides whether that rule is acceptable; without it the ref gate itself reads unmet on the new
families.

Validation of the proposal (battery copy in `prop/tools/`, ref gate mirrored at the path the battery
resolves):

```
$ python3 prop/tools/battery-proposed.py --selftest
absent PASS 0 | constant-healthy PASS 0 | non-json PASS 0 | constant-degraded PASS 0
reference-gate PASS families_passed=25
selftest PASS 5/5
$ ... --gate pristine.py  --runs 3   -> 25/25 met, 25/25 met, 25/25 met
$ ... --gate ref-gate-r87.py --runs 3 -> 25/25 met, 25/25 met, 25/25 met
$ ... --gate m01 --runs 3 -> 25/25 met (still equivalent)
$ ... --gate m05 --runs 3 -> 24/25 failed PAREN-PATH
$ ... --gate m24 --runs 3 -> 24/25 failed ENTRY-LABEL
$ ... --gate m25 --runs 3 -> 18/25 failed HOST-SHAPE,MULTI-FAULT,OPTIONAL-SKIP,PANIC-FIRST,PANIC-METADATA,PANIC-NO-ONLY,SECUREBOOT
```

So the three gaps are closeable without changing any frozen rule: pristine and the reference gate
stay at full marks, and the three mutants are killed. `m25` also trips six existing families because
`set_panic` is used by them; that is expected, not a rule change.

Adjacent observation (not a mutant verdict, no action taken): a pin-key line whose value fails
`parse_uri` (e.g. no `(`, no `):/`, no `#`) is silently dropped by the candidate instead of being
reported. `m05` is one route into that behaviour. The frozen rule set does not define a status for
it, so I did not propose a family; flagged for L1 only.

## 6. Bounds, refusals, restoration evidence

- Lane file untouched: `sha256(tools/check-limine-pins.py)` = `bbcc874a…b73c` before and after; the
  scratch copy has the same hash. `git -C <lane> status --porcelain tools/` is empty; the only new
  path is the untracked `.ufo/waves/round-87/w1/` tree.
- No `/boot` or `/efi` access, no `objcopy`/`strip`/`sbsign`/`ukify`/`mkinitcpio`/`limine*`/`bootctl`/
  `efibootmgr`, no `sudo`, no `/sys` or `/proc` writes, no sysctl change, no pacman, no commit/push.
  Host facts came from the freeze receipts only; no host command was run.
- No tool installs or upgrades were needed (python3 stdlib only).
- Scratch `/fast/scratch/hyaku/tsukuroi-r87/MutGate` holds the working copies; receipts were copied
  into this wave dir before exit and the scratch tree was removed.

## 7. Files

- `mutants/` — 30 mutant sources, 30 diffs, `manifest.json`
- `receipts/` — `*.battery.out`, `*.selftest.out`, `mutants-table.md`, `survivor-probes.txt`
- `proposed-battery-r87.patch`, `battery-proposed.py` — proposal (not applied to the lane)
- `gen.py`, `butch.py`, `probe.py`, `runone.sh`, `names.txt` — generators and probe drivers
