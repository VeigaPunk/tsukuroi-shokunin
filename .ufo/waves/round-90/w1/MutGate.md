# MutGate — held-out mutants of the round-90 limine-pins gate

Seat: mutation-tester (wave w1, round 90). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Report-time lane master: `587234994bbea98559daa5f92b01e7fe6f01a492` (the C1 measured commit; `git diff
ce89df93..master -- tools/` is empty). Sweep-time master (asserted by the driver, matched):
`ce89df93e5f576c5c236d4547299e9ea954e8853`.

Bytes measured (hashes before and after the sweep, identical):

| artifact | sha256 |
|---|---|
| `tools/check-limine-pins.py` (candidate) | `4780da83ba411db1dc6afc250b618edc336a42790d79578018b40a2d7593a332` |
| `tools/limine-pin-battery-r90.py` (frozen) | `8f0daee82b9d487b5412a45ec1b8cf74c4e037e87d67213f756f1f850fb303e5` |

## Method

1. Copied the candidate gate byte-identically into `$S/gate.py` (sha matches the lane file) and ran the
   frozen battery with `--runs 3`: three times `families_passed 73/73 verdict met failed -`, exit 0,
   53.57 s. That is the pristine baseline (C1's counting command, gate side only; the lane/clone legs are
   other seats' surface).
2. Generated **29 single-point mutants** from the pristine bytes. Each patch anchor occurs exactly once
   (`assert count == 1`), each mutant `py_compile`s clean, and each `patch.diff` is in
   `MutGate/<mutant>/patch.diff`. No mutant source is byte-identical to any N01–N27 control (sha256 check:
   0 collisions); each patch changes a distinct point from every control patch.
3. Ran, per mutant, cwd `$S`:
   `python3 <lane>/tools/limine-pin-battery-r90.py --gate $S/mutants/<id>/gate.py --runs 3 --work "$S/work/<id>" --json ...`
   (`JOBS=4` mutants in parallel; each battery is internally serial; 651.3 s total).
4. Classified: **killed** = verdict `unmet` in all 3 runs; **flaky** = met in some, unmet in others;
   **survived** = `met` in all 3 runs.
5. Restoration: pristine scratch gate sha unchanged, lane file sha unchanged, `git status --porcelain`
   on the gate and battery empty, and a post-sweep `--runs 1` on the pristine bytes reads
   `families_passed 73/73 verdict met failed -` (exit 0). The lane file was never edited; mutants are
   separate scratch files.

## Counts

- 29 held-out single-point mutants: **26 killed, 3 survived, 0 flaky, 0 inconclusive**.
- Follow-up probe `m08b` (30th source, not part of the held-out table): **killed 3/3**.
- All survivors are coverage findings, not evidence of a green contract.

## Table (killed families = failed in every one of the 3 runs)

| mutant | clause bent | change | verdict | per-run passed | killed by |
|---|---|---|---|---|---|
| m01-entry-not-indented | R9/R8 body boundary | entry line detected on `raw` (`raw.startswith("/")`) instead of the blank-stripped line | killed | 69/69/69 | ENTRY-LABEL, ENTRY-LABEL-EDGES, ENTRY-SCOPE, HOST-SHAPE |
| m02-cr-trailing-only | R1 every CR removed | `raw.rstrip("\r")` (only a trailing CR) in `split_key` | killed | 72/72/72 | CR-INTERNAL |
| m03-strip-all-whitespace | R1 blanks are space/tab only | `.strip()` instead of `.strip(" \t")` on the key line | killed | 72/72/72 | BLANK-CLASS |
| m04-protocol-value-untrimmed | R9 with R1 protocol value trimmed | protocol recorded from the raw text after `:`, untrimmed | killed | 57/57/57 | EFI-IMAGE-MISSING, EMPTY-PATH, FIRST-PATH, FIRST-PROTOCOL, MISSING, MULTI-FAULT, PATH-PRECEDENCE, PROTOCOL-DECOY, MEASURED-DECOY, MEASURED-FIRST, MEASURED-IN-ENTRY, MEASURED-SB, MEASURED-TPM0, MEASURED-TPM-ABSENT, MEASURED-TPM1, MEASURED-VALUE-CASE |
| m05-image-path-key-case | R9 key case-insensitive (`image_path`) | body records `image_path` only when written lowercase | **survived** | 73/73/73 | — |
| m06-empty-resource-unresolved | R4 empty resource name is LP-BAD-RESOURCE | validity check skipped for the empty name (falls to LP-UNRESOLVED) | killed | 70/70/70 | BAD-RESOURCE, BAD-RESOURCE-OPTIONAL, BAD-OVER-UNRESOLVED |
| m07-tpm0-halt-if-tpm | R10 tpm 0 → menu | `tpm==0` returns `halt-if-tpm` | killed | 71/71/71 | MEASURED-TPM0, SECUREBOOT |
| m08-bad-only-rc2 | R7 LP-BAD-RESOURCE-only file rc 1 | rc forced 2 when the whole status set is exactly `{LP-BAD-RESOURCE}` | **survived** | 73/73/73 | — |
| m09-unreadable-conf-degraded | R7 unreadable conf rc 2 | unreadable conf returns DEGRADED rc 1 | killed | 71/71/71 | CONF-UNREADABLE, MALFORMED-INPUT |
| m10-optional-missing-skip | R6 optional LP-MISSING is not-modelled | optional missing → `skip` | killed | 72/72/72 | OPTIONAL-MISSING |
| m11-empty-path-not-pin | R2 an empty path is still a pin | `cut == 0` (empty path) → not a pin | killed | 72/72/72 | EMPTY-PATH |
| m12-first-hash | R2 hash after the LAST `#` | `tail.find("#")` | killed | 72/72/72 | LAST-HASH |
| m13-last-uri-sep | R2 path after the FIRST `):/` | `value.rfind("):/")` | killed | 72/72/72 | FIRST-URI-SEP |
| m14-measured-key-case | R10 measured_boot key case-insensitive | `written == "measured_boot"` | killed | 69/69/70 | MEASURED-TPM1, MEASURED-TPM-ABSENT, MEASURED-IN-ENTRY |
| m15-measured-and-sb | R10 measured OR Secure Boot | `and secure_boot` | killed | 67/67/68 | MEASURED-TPM1, MEASURED-TPM-ABSENT, MEASURED-SB, MEASURED-FIRST, MEASURED-IN-ENTRY |
| m16-directory-exists | R5 a directory path is LP-MISSING | `os.path.exists` instead of `isfile` | killed | 72/72/72 | EMPTY-PATH |
| m17-esp-root-not-contained | R5 the ESP root itself is inside | dropped the `resolved != root` allowance | killed | 72/72/72 | EMPTY-PATH |
| m18-hash-case-sensitive | R5 hash compare case-insensitive | `got == h` | killed | 72/72/72 | HASH-UPPER |
| m19-pin-keys-drop-dtb | R2 all eight path keys are pins | `dtb_path` removed from `PIN_KEYS` | killed | 72/72/71 | ALL-PIN-KEYS |
| m20-measured-value-strip | R10 exact `yes` (R1 blanks space/tab) | `.strip()` on the measured value | **survived** | 73/73/73 | — |
| m21-tpm-flag-inverted | R10 `--tpm-present 1` means present | CLI parse `== "0"` | killed | 67/67/67 | MEASURED-TPM0, MEASURED-TPM1, MEASURED-SB, MEASURED-TPM-ABSENT, MEASURED-FIRST, MEASURED-IN-ENTRY |
| m22-prompt-ignores-sb | R6 Secure Boot suppresses the prompt | dropped `and not secure_boot` from `prompt` | killed | 72/72/72 | SECUREBOOT |
| m23-label-trailing-plus-stripped | R8 a trailing `+` stays | `.rstrip("+")` on the label | killed | 72/72/72 | ENTRY-LABEL-EDGES |
| m24-entry-empty-not-null | R8 pre-entry pins carry null | pre-entry entry emitted as `""` | killed | 66/66/66 | BAD-RESOURCE-OPTIONAL, ENTRY-SCOPE, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-MISSING, OPTIONAL-SKIP, OPTIONAL-UNRESOLVED |
| m25-panic-last-wins | R6/R8 the FIRST hash_mismatch_panic wins | dropped the first-wins guard | killed | 71/71/71 | PANIC-FIRST, PANIC-METADATA |
| m26-bad-consequence-not-modelled | R6 LP-BAD-RESOURCE outside optional keys panics | non-optional bad resource → `not-modelled` | killed | 68/68/68 | BAD-RESOURCE, BAD-OVER-UNRESOLVED, DOUBLE-DOLLAR, EMPTY-ROOT-RESOURCE, RESOURCE-CASE |
| m27-hash-length-below-128 | R3 exactly 128 characters | `len(h) < 128` (129 accepted) | killed | 70/72/71 | HASH-LENGTH |
| m28-sb-flag-truthiness | R7 `--secure-boot-enforced 0` is not enforced | `bool(a.secure_boot_enforced)` (`"0"` truthy) | killed | 33/32/33 | 19 families, incl. SB-FLAG-ZERO, POSITIVE, MISMATCH-EARLY/LATE, PANIC-*, MEASURED-*, UNRESOLVED, EFI-IMAGE-MISSING, NON-EFI-MISSING, HOST-SHAPE |
| m29-faults-include-unresolved | R7 LP-UNRESOLVED is not a fault | added `LP-UNRESOLVED` to `FAULTS` | killed | 68/68/68 | UNRESOLVED, OPTIONAL-UNRESOLVED, EMPTY-ROOT-RESOURCE, ROOT-ON-BOOT, VALID-RESOURCES |

Randomised families make some kill sets run-dependent without changing the verdict: m14, m15, m19, m27
and m28 show different failed-family sets across their 3 runs, but all three runs are `unmet` (the union
is in `MutGate/results.json`). m27 is the expected flakiness case (129-char hash drawn with p=1/4 per
case); it was killed in all three runs (70/72/71 passed), so the observed classification is killed, but
one run out of a repeated sampling can plausibly pass this mutant (single-run family power ≈ 0.68).

## Survivors (coverage findings; no contract change proposed)

### 1. `m05-image-path-key-case` — R9: the `image_path` key matches case-insensitively
Patch: the body records `image_path` only when the key was written exactly `image_path`; `IMAGE_PATH` /
`Image_Path` / `image_PATH` lines are dropped from the body, so they never become the entry's image line.

Probe (pristine vs mutant, identical case):

```
conf:  /probe-entry
       protocol: efi
       IMAGE_PATH: boot():/missing-image.efi#<128 x "0">
pristine: rc 1 DEGRADED  pins [[3, "LP-MISSING", "panic"]]
mutant:   rc 1 DEGRADED  pins [[3, "LP-MISSING", "not-modelled"]]
```

No family writes a mixed-case image line: FIRST-PATH covers `path` key case, FIRST-PROTOCOL covers
`protocol` key case, but `image_path` is always lowercase in the roster. Proposed family:

```python
def fam_efi_image_missing_keycase(c):
    """R9: the image_path key matches case-insensitively, so a mixed-case IMAGE_PATH line is the
    entry's image line; only a pin on it panics when missing (R6)."""
    c.header()
    for key in ("IMAGE_PATH", "Image_Path", "image_PATH"):
        efi_entry(c)
        c.pin("LP-MISSING", key=key)
    efi_entry(c)
    c.pin("OK", key="IMAGE_PATH")   # a present mixed-case image line stays OK
```

### 2. `m08-bad-only-rc2` — R7: an LP-BAD-RESOURCE-only file is DEGRADED rc 1
Patch: rc is forced to 2 when `statuses == {"LP-BAD-RESOURCE"}`, i.e. when the file's pin list consists
solely of bad-resource pins. Every family that carries a bad-resource pin also carries an OK pin
(`BAD-RESOURCE`, `BAD-RESOURCE-OPTIONAL`, `DOUBLE-DOLLAR`, `RESOURCE-CASE`, `BAD-OVER-UNRESOLVED`
unresolved+bad), so the condition never holds on the roster: 73/73 in each of the 3 runs.

That the rc clause itself is checked (and only this shape is missing) is shown by the 30th-source probe
`m08b-faultonly-rc2`, which keys the same rc on the *fault set* (`(statuses & set(FAULTS)) ==
{"LP-BAD-RESOURCE"}`): it is killed 3/3 by BAD-OVER-UNRESOLVED, BAD-RESOURCE, BAD-RESOURCE-OPTIONAL,
DOUBLE-DOLLAR, RESOURCE-CASE (plus EMPTY-ROOT-RESOURCE in two runs). Proposed family:

```python
def fam_bad_resource_only(c):
    """R7: a file whose only pin names an invalid resource is DEGRADED rc 1 (no OK pin beside it)."""
    c.header()
    efi_entry(c)
    c.pin("LP-BAD-RESOURCE", resource="%s()" % c.rng.choice(bad_names(c)))
```

### 3. `m20-measured-value-strip` — R10: `measured_boot` value compared exactly (`strcmp yes`), R1: blanks are space/tab only
Patch: `measured_setting[1].strip() == "yes"`. R1 already removes space/tab from the value, so `.strip()`
is a no-op on every fixture the roster writes; it only diverges for a value that ends in a non-blank
control character (or starts with one). Probe:

```
conf:  measured_boot: yes<0x0b>
       /probe-entry
       path: boot():/present.efi#<blake2b>
arg:   --tpm-present 1
pristine: rc 0 HEALTHY  on_panic "menu"
mutant:   rc 0 HEALTHY  on_panic "halt"
```

`PANIC-VALUE-BLANKS` exercises this shape for `hash_mismatch_panic` but no family does it for
`measured_boot`. Proposed family:

```python
def fam_measured_value_blanks(c):
    """R10 with R1: only space/tab are blanks, so `yes<0x0b>` and `<0x0b>yes` are not the strcmp value
    `yes`; measured boot is not requested (--tpm-present 1 -> menu)."""
    c.header()
    c.add("measured_boot:%syes%s" % (c.rng.choice([" ", "\t"]), c.rng.choice(CONTROL_WS)))
    c.add("measured_boot:\x0byes")          # leading control char survives the R1 value trim too
    set_tpm(c, "1")
    panic_pins(c)
```

`CONTROL_WS` is the existing battery constant (`("\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x1f")`).

## Notes

- m04's broad kill set (16 families) has a mechanical cause worth knowing: `Case.entry()` writes a
  literal `protocol: efi`; the raw-slice mutant reads that value as `" efi"`, so every family that relies
  on `c.entry()`'s protocol line silently stops being an efi entry. It is killed, not a coverage gap.
- Every killed mutant failed on all three runs; there were no flaky verdicts and no inconclusive
  (crash/timeout/bad-output) cases.
- Nothing was refused or skipped: no host writes, no `sudo`, no lane edits, no subagents, no tool installs.
- Receipts: `MutGate/receipt.txt` (verbatim command outputs and hashes), `MutGate/results.json` (slim,
  per-mutant/per-run), `MutGate/probe.json` (survivor probes), `MutGate/<mutant>/{gate.py,patch.diff,
  slim.json,stdout.log,result.json.gz}`, `MutGate/m08b-faultonly-rc2/{gate.py,result.json.gz}`.
