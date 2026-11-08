# MutGate — held-out single-point mutants of the r91 `limine-pins` gate

Seat: `MutGate` (mutation-tester, round 91, wave w1). Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Scratch: `/fast/scratch/hyaku/tsukuroi-r91/MutGate` (deleted after these receipts were copied here).

## 1. Bytes measured (and the mid-wave drift)

| item | digest / value |
|---|---|
| gate frozen for mutation | `62bb06c997fb99a9fd811ec97440eebe2dafa7e63c4f21f43aa0ead9af7da737` (`gate-frozen-62bb06c9.py`) |
| battery | `655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9` (== the digest in the assignment) |
| `git rev-parse master` at freeze | `b516d6ae13ec0bba3ef89589ac1cac86f73a9632` |
| `git rev-parse master` at report | `2d7e09e101996cc1ac5836c6d635f3f608453ac5`; `tools/check-limine-pins.py` = `62bb06c9…`, worktree clean |
| freeze manifest `sha256sum -c` | 13/13 `OK`, exit 0 |

Drift observed and handled, not a reproach: when I started, the worktree gate was **dirty** (`62bb06c9`, mtime 23:47:47) against `HEAD` (`b516d6ae`) whose gate was `dfc63548`. I did not mutate the lane file; I copied the worktree bytes at that instant into scratch and mutated the copy. By the time the receipts were written, `HEAD` had landed those exact bytes (`45ae6518 round-91: V1/U1 gate fixes …`), so **the frozen bytes equal the gate at lane tip `2d7e09e1`**. The same 38 patches also match `HEAD`'s earlier gate `dfc63548` exactly once each (the intervening diff was docstring + a dead 3-line `pass` block + `sanitize()` on the two reported setting values; no mutated line is touched), so the results transfer across both candidate revisions.

The freeze manifest does not list the gate/battery (it pins `before/` fixtures only); its 13 entries verified clean at report time, and the battery digest matches the assignment, so the C1 void condition is not triggered by anything I did.

## 2. Method

- 38 mutants, each **one textual substitution** on the frozen gate, asserted to match exactly once; `difflib` proves **1 changed hunk per mutant, 0 multi-hunk** (`mutants/diffshapes.json`). Every mutant compiles (`py_compile`).
- Detector: the frozen battery, unchanged, run as `python3 tools/limine-pin-battery-r91.py --gate <mutant> --runs 3 --work <own dir>`, cwd = scratch, `TMPDIR` = scratch. 114 battery runs total, 6 at a time.
- Classification: **killed** = 3/3 runs `unmet`; **flaky** = mixed; **survived** = 3/3 `met`. Survivors were then split into **equivalent** (structurally a no-op) and **undetected bend** (differ from pristine on a conf the battery never draws), using (a) targeted differential probes (`probe.py`, receipts `receipts/probe-*.json`) and (b) a 200-case differential fuzz over random `limine.conf`-shaped inputs (`fuzz.py`, `receipts/fuzz-*.json`).

### Baseline of record (pristine frozen bytes)

```
families_passed 82/82 verdict met failed -
families_passed 82/82 verdict met failed -
families_passed 82/82 verdict met failed -
exit=0
```
(225 s, `receipts/baseline-frozen.json`.) An earlier invocation was invalidated by my own `rm -rf w0` racing its work dir while it ran — `FileNotFoundError …/limine-battery-r91-eqi2l5tj/ce9kbc9zc`, exit 1 — and is discarded; it is not the baseline.

## 3. Result

```
{'killed': 30, 'survived': 8, 'flaky': 0, 'error': 0}
```
38/38 mutants gave three readable runs (no timeout, no bad-output, no error) — the 20 s per-case budget held under 6-way parallel load. Of the 34 mutants that are not no-ops, **30 are killed 3/3** and **4 survive as undetected bends**. No flaky mutant.

All 38 are behaviourally distinct from controls `N01`–`N10` (different patch sites: e.g. `V1c` exposes only the *first* entry body rather than the whole file; `U1b`/`U1e` bend the empty-path clause and the reported line number, not the field's existence/order).

## 4. Table

| # | mutant | r91 clause bent | 3-run families passed | class | killing families (failed in 3/3 runs) |
|---|---|---|---|---|---|
| 1 | `V1a-entry-scan-needs-double-slash` | V1 entry-line detection | 79/79/79 | killed 3/3 | GLOBAL-VS-ENTRY, MEASURED-IN-ENTRY, PANIC-AFTER-PIN |
| 2 | `V1b-entry-scan-no-break` | V1 first entry line = last '/' line | 80/80/80 | killed 3/3 | GLOBAL-VS-ENTRY, MEASURED-IN-ENTRY |
| 3 | `V1c-flip-lag-one-line` | V1 global section ends before first entry | 79/79/79 | killed 3/3 | GLOBAL-VS-ENTRY, MEASURED-IN-ENTRY, PANIC-AFTER-PIN |
| 4 | `V1d-firstline-exception-line2` | V1 first-line-is-entry exception guard | 80/80/80 | killed 3/3 | MEASURED-IN-ENTRY, PANIC-AFTER-PIN |
| 5 | `V1e-panic-last-wins` | V1/R6 first visible hash_mismatch_panic wins | 82/82/82 | **survived (undetected bend)** | — |
| 6 | `V1f-panic-value-strip` | R6 panic value compared after rstrip | 82/82/82 | survived (equivalent, no-op) | — |
| 7 | `V1g-measured-value-strip` | R10 measured_boot value compared after rstrip | 82/82/82 | survived (equivalent, no-op) | — |
| 8 | `V1h-measured-value-lower` | R10 measured_boot strcmp is case-sensitive | 81/81/81 | killed 3/3 | MEASURED-VALUE-CASE |
| 9 | `V1i-tpm0-as-absent` | R10 `--tpm-present 0` forces menu | 80/80/81 | killed 3/3 | MEASURED-TPM0 (+SECUREBOOT in 2/3 runs) |
| 10 | `V1j-tpm-absent-menu` | R10 flag absent → halt-if-tpm | 80/80/80 | killed 3/3 | MEASURED-TPM-ABSENT, SECUREBOOT |
| 11 | `V1k-secboot-dropped-onpanic` | R10 Secure Boot requests measured boot | 80/80/80 | killed 3/3 | MEASURED-SB, SECUREBOOT |
| 12 | `V1l-secboot-dropped-prompt` | R6 Secure Boot suppresses prompt | 81/81/81 | killed 3/3 | SECUREBOOT |
| 13 | `U1a-image-path-precedence` | U1/R9 image line = first `path` else first `image_path` | 78/78/78 | killed 3/3 | NO-PAREN, PATH-PRECEDENCE, UNHASHED-DECOYS, UNVERIFIED-IMAGE-PATH |
| 14 | `U1b-empty-path-listed` | U1 empty path is still a pin (not unverified) | 81/81/81 | killed 3/3 | EMPTY-PATH |
| 15 | `U1c-offbyone-line-index` | U1 physical-line lookup | 70/70/70 | killed 3/3 | FIRST-LINE-ENTRY, FIRST-PATH, GLOBAL-VS-ENTRY, HOST-SHAPE, PANIC-AFTER-PIN, PANIC-GLOBAL-ONLY, POSITIVE, UNVERIFIED-IMAGE, UNVERIFIED-IMAGE-PATH, UNVERIFIED-MIXED, UNVERIFIED-NON-EFI, UNVERIFIED-SORTED |
| 16 | `U1d-discard-none-removed` | U1 image-line set drops `None` | 72/72/72 | killed 3/3 | crash: `TypeError: unsupported operand type(s) for -: 'NoneType' and 'int'` at `check` line 188 (`split_key(lines[img_ln - 1])`) whenever a body is an efi entry with no image line — families ALL-PIN-KEYS, BAD-RESOURCE, CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH, ENTRY-SCOPE, GZ-RAW, KEY-CASE, PAREN-PATH, UNHASHED-DECOYS |
| 17 | `R9a-body-last-key-wins` | R9 first key line of a body wins | 78/78/78 | killed 3/3 | FIRST-PATH, FIRST-PROTOCOL, NO-PAREN, UNHASHED-DECOYS |
| 18 | `R9b-protocol-set-adds-linux` | R9 chainload protocols = efi/uefi/efi_chainload | 78/78/78 | killed 3/3 | FIRST-PROTOCOL, NON-EFI-MISSING, UNVERIFIED-NON-EFI, UNVERIFIED-SORTED |
| 19 | `R9c-protocol-lower` | R9 protocol compared with strcmp (case-sensitive) | 81/81/81 | killed 3/3 | NON-EFI-MISSING |
| 20 | `R9d-protocol-value-strip` | R9 protocol value compared with strcmp (trailing blanks matter) | 82/82/82 | survived (equivalent, no-op) | — |
| 21 | `R6a-missing-any-panics` | R6 LP-MISSING panics only on an efi image line | 74/74/74 | killed 3/3 | EMPTY-PATH, ENTRY-SCOPE, FIRST-PATH, FIRST-PROTOCOL, NON-EFI-MISSING, OPTIONAL-MISSING, PATH-PRECEDENCE, PROTOCOL-DECOY |
| 22 | `R6b-image-missing-not-modelled` | R6 efi image LP-MISSING panics | 64/64/64 | killed 3/3 | EFI-IMAGE-MISSING, EMPTY-PATH, FIRST-PATH, FIRST-PROTOCOL, all eight MEASURED-*, MISSING, MULTI-FAULT, PATH-PRECEDENCE, PROTOCOL-DECOY, UNVERIFIED-MIXED |
| 23 | `R6c-optional-missing-panics` | R6 optional LP-MISSING is not-modelled | 81/81/81 | killed 3/3 | OPTIONAL-MISSING |
| 24 | `R7a-rc-bad-resource-not-fault` | R7 LP-BAD-RESOURCE is DEGRADED rc 1 | 76/77/76 | killed 3/3 | BAD-OVER-UNRESOLVED, BAD-RESOURCE, BAD-RESOURCE-OPTIONAL, DOUBLE-DOLLAR, RESOURCE-CASE (+EMPTY-ROOT-RESOURCE in 1/3) |
| 25 | `R4a-resource-lower` | R4 resource name compared case-sensitively | 78/78/78 | killed 3/3 | BAD-OVER-UNRESOLVED, BAD-RESOURCE, BAD-RESOURCE-OPTIONAL, RESOURCE-CASE |
| 26 | `R4b-double-dollar` | R4 exactly one leading `$` dropped | 81/81/81 | killed 3/3 | DOUBLE-DOLLAR |
| 27 | `R5a-hash-upper-compare` | R5 hash compare is case-insensitive | 81/81/81 | killed 3/3 | HASH-UPPER |
| 28 | `R2a-first-hash` | R2 hash starts after the LAST `#` | 81/81/81 | killed 3/3 | LAST-HASH |
| 29 | `R2b-rfind-paren` | R2 resource ends at the FIRST `(` | 81/81/81 | killed 3/3 | PAREN-PATH |
| 30 | `R1a-value-trailing-strip` | R1 value keeps trailing blanks | 82/82/82 | survived (equivalent, no-op) | — |
| 31 | `R1b-value-no-lstrip` | R1 value loses leading blanks | 2/2/2 | killed 3/3 | 80/82 (all but MALFORMED-INPUT, CONF-UNREADABLE) |
| 32 | `R1c-cr-dropped` | R1 every CR removed before the key is read | 80/80/80 | killed 3/3 | CR-INTERNAL, WHITESPACE-CRLF |
| 33 | `R8a-empty-entry-label` | R8 empty cleaned label keeps the previous entry | 82/82/82 | **survived (undetected bend)** | — |
| 34 | `V1m-child-entry-boundary` | R9/V1 an indented `//` line starts a new body | 78/78/78 | killed 3/3 | ENTRY-LABEL, ENTRY-LABEL-EDGES, ENTRY-SCOPE, HOST-SHAPE |
| 35 | `V1n-measured-last-wins` | V1/R10 first visible measured_boot wins | 82/82/82 | **survived (undetected bend)** | — |
| 36 | `U1e-reported-line-offset` | U1 reports the physical line number | 72/72/72 | killed 3/3 | EMPTY-PIN-LIST, FIRST-PATH, HOST-SHAPE, NO-PAREN, UNHASHED-DECOYS, UNVERIFIED-IMAGE, UNVERIFIED-IMAGE-PATH, UNVERIFIED-MIXED, UNVERIFIED-NON-EFI, UNVERIFIED-SORTED |
| 37 | `CONF-a-onpanic-menu` | unreadable conf: `on_panic` is null | 82/82/82 | **survived (undetected bend)** | — |
| 38 | `CONF-b-rc-1` | unreadable conf: rc 2 | 80/80/80 | killed 3/3 | CONF-UNREADABLE, MALFORMED-INPUT |

## 5. The four undetected bends (survivors) — clause, evidence, proposed family

### S1 `V1e-panic-last-wins` — V1/R6: the FIRST VISIBLE `hash_mismatch_panic` wins

Patch: `if in_global and key == "hash_mismatch_panic" and panic_setting is None:` → drop `and panic_setting is None`. Two *visible* panic keys make the gate report the last one.

Probe (`receipts/probe-V1e-panic-last-wins.json`, conf `hash_mismatch_panic: yes` / `hash_mismatch_panic: no` / `/e` / mismatch pin):

```
pristine: {"hash_mismatch_panic": {"line": 2, "value": "yes"}, "pins": [[5,"LP-MISMATCH","panic","e"]], "rc": 1, "verdict": "DEGRADED"}
mutant  : {"hash_mismatch_panic": {"line": 3, "value": "no"},  "pins": [[5,"LP-MISMATCH","prompt","e"]], "rc": 1, "verdict": "DEGRADED"}
```
Fuzz also diverged within 10 random confs (two identical global keys: reported line 2 vs 3). **The battery draws no case with two visible panic keys**, so neither the consequence nor `hash_mismatch_panic.line/value` is constrained for it.

```python
def fam_panic_two_global(c):
    """V1/R6: the FIRST VISIBLE hash_mismatch_panic wins. A last-wins read reports the second
    line/value and flips a mismatch from panic to prompt."""
    c.header()
    set_panic(c, "yes")
    set_panic(c, "no")        # second GLOBAL key: must not win (`set_panic` keeps the first as panic_value)
    c.entry()
    c.pin("LP-MISMATCH")      # want: panic, hash_mismatch_panic.line = first key's line
```

### S2 `V1n-measured-last-wins` — V1/R10: the FIRST VISIBLE `measured_boot` wins

Patch: drop `and measured_setting is None` on the `measured_boot` read.

Probe (`receipts/probe-V1n-measured-last-wins.json`, `measured_boot: yes` / `measured_boot: no`, `--tpm-present 1`):

```
pristine: {"measured_boot": {"line": 2, "value": "yes"}, "on_panic": "halt", "verdict": "HEALTHY", "rc": 0}
mutant  : {"measured_boot": {"line": 3, "value": "no"},  "on_panic": "menu", "verdict": "HEALTHY", "rc": 0}
```
(`MEASURED-FIRST` writes its second key inside an entry body, where it is invisible to both readings, so it does not test this. The 200-case fuzz also missed it — its grammar never writes two global `measured_boot` keys.)

```python
def fam_measured_two_global(c):
    """V1/R10: the FIRST VISIBLE measured_boot wins; a later global `no` must not veto `yes`."""
    c.header()
    measured(c, "yes")
    measured(c, "no")
    set_tpm(c, "1")
    panic_pins(c)             # want: on_panic == "halt"
```

### S3 `R8a-empty-entry-label` — R8: an empty cleaned label keeps the previous entry

Patch: drop `or entry` from `entry = sanitize(stripped.lstrip("/").lstrip("+").strip()) or entry`. A bare `/` line then yields `""` instead of inheriting the previous label.

Probe (`receipts/probe-R8a-empty-entry-label.json`, entry `/first`, then a bare `/`):

```
pristine: pins entries [ … [4,"LP-MISMATCH","panic","first"], [7,"LP-MISMATCH","panic","first"] ]
mutant  : pins entries [ … [4,"LP-MISMATCH","panic","first"], [7,"LP-MISMATCH","panic",""]      ]
```
The battery's `r8_entries()` expects `first` for both pins (`label or cur`), so this is a real R8 divergence; no family writes a bare `/` line (`ENTRY-LABEL-EDGES` writes `/+`, `/name+`, `/<blank>name extra`, all non-empty after cleaning).

```python
def fam_entry_bare_slash(c):
    """R8: a '/' entry line whose cleaned label is empty keeps the previous label."""
    c.header()
    c.add("/first")
    c.add("  protocol: efi")
    c.pin("OK")
    c.add("/")                 # cleaned label "" -> label stays "first"
    c.add("  protocol: efi")
    c.pin("LP-MISMATCH")       # want: pin.entry == "first"
```

### S4 `CONF-a-onpanic-menu` — unreadable conf: `on_panic` must be null

Patch: the `OSError` return dict gets `"on_panic": "menu"` instead of `None`.

Probe (`receipts/probe-CONF-a-onpanic-menu.json`, `--conf` names an absent file):

```
pristine: {"rc": 2, "verdict": "CANNOT-EVALUATE", "on_panic": null,   "pins": []}
mutant  : {"rc": 2, "verdict": "CANNOT-EVALUATE", "on_panic": "menu", "pins": []}
```
This one is a **harness** gap, not a family gap: `run_battery()` sets `want_op = None if (c.conf_missing or c.conf_dir) else c.want_on_panic()`, and the check `(want_op is None or got[6] == want_op)` then accepts any `on_panic`. The gate has read no `measured_boot`, so "menu" asserts a state it never observed. One-line battery amendment (proposed patch under `receipts/proposed-battery-onpanic.md`):

```python
want_op = "null" if (c.conf_missing or c.conf_dir) else c.want_on_panic()
...
ok = (… and (want_op is None or (got[6] is None if want_op == "null" else got[6] == want_op)))
```
A companion family is not needed: `CONF-UNREADABLE`/`MALFORMED-INPUT` already produce the unreadable conf; only the expectation is missing.

## 6. The four equivalent survivors (no-op patches) — argument and evidence

`split_key()` (gate lines 72 and 80) already does `line = raw.replace("\r","").strip(" \t")` **and** `value = line[i+1:].lstrip(" \t")`. A value can therefore never carry a leading or trailing space/tab at the point these patches apply, so stripping it again changes nothing:

| mutant | patch | why it is a no-op |
|---|---|---|
| `V1f-panic-value-strip` | `panic_setting[1].strip().lower() == "no"` | value already trimmed both ends; the half-space variant family `PANIC-VALUE-BLANKS` (`no` + trailing blanks) is normalised away by the same line strip in both gate and battery model |
| `V1g-measured-value-strip` | `measured_setting[1].strip() == "yes"` | same |
| `R9d-protocol-value-strip` | `body[key] = value.strip() if key == "protocol"` | same (`efi ` with a trailing blank never reaches the comparison with a blank in either implementation) |
| `R1a-value-trailing-strip` | `line[i+1:].strip(" \t")` | same |

Evidence: differential fuzz, 200 random confs each, **0 divergences** on the full compared JSON (`verdict, rc, on_panic, hash_mismatch_panic, measured_boot, unverified_image_lines, pins, findings`): `receipts/fuzz-V1f…/V1g…/R9d…/R1a….json`. They are reported as equivalent, not as coverage gaps; they should not be counted as surviving defects.

Note the neighbouring case mutant `V1h` (`.lower()` on the measured value) **is** killed by `MEASURED-VALUE-CASE`, so the battery does distinguish value case — the equivalence above is specific to whitespace stripping.

## 7. What the battery constrains well (positive evidence)

- V1 visibility: four independent bends of the global-section cut (`V1a`–`V1d`, `V1m`) all die 3/3, including the `first '/'-line is line 1` exception and the first-body off-by-one.
- U1: existence (`N05`-class), membership, ordering, precedence, empty path, non-efi scope and line-number offset all die; `U1c`/`U1e` fail 12 and 10 families respectively, `U1a` fails 4.
- R6/R9/R10: the efi image consequence, protocol set/case, body scope and all four `--tpm-present`/Secure Boot combinations die; `R6b` alone fails 18 families.
- R1–R5, R7: hash position/case/format, `$` handling, resource case, rc/verdict aggregation all die; `R1b` fails 80/82 (only the two unreadable-conf families pass, as expected).

## 8. Notes, refusals, hygiene

- No lane file was edited; no commit/jj mutation anywhere. `git` was used read-only (`rev-parse`, `log`, `show`, `status`, `cat-file`). Mutants, probes and fuzz ran only in scratch against **copies**.
- Host untouched: no `/boot`, `/efi`, `/etc`, `/usr`, `/var`, `/sys`, `/proc` writes; no `objcopy`/`ukify`/`limine*`/`bootctl`/`pacman`; no sysctl; no `sudo`. Only file reads of the lane.
- No tool installed or upgraded (nothing needed).
- `$S` receipts copied here before scratch removal: `receipts/` (results, summary, sweep log, baseline, 6 probes, 8 fuzz runs, drivers), `mutants/` (38 mutant files + `INDEX.json` + `diffshapes.json`), `gate-frozen-62bb06c9.py`, `gate-b516d6ae-dfc63548.py`, `frozen-sha256.txt`, `receipts-baseline.md`.
- Unrun: `--selftest --reference` of the battery (not assigned to this seat), and any measurement of the canonical-vs-clone C1 legs (other seats own those).
