# Proposed discriminating cases for the ten uncertified r88 clauses

Seat `CriticForgers`. These are the smallest inputs that separate the faithful reimplementation
(`base.py`, met 38/38 x3) from each surviving forger. One case per clause (not a new family unless the
L1 prefers that). Expectations are derived from the battery docstring rules R1-R8; the L1 decides
whether and where they land. I did not read the battery body, so this is a case-shape proposal, not a
code patch.

Placeholders: `<H>` = the BLAKE2b-512 hex of the ESP file's raw bytes; `<wrong>` = any other 128-hex
string. `esp/` holds the file at the relative path after `):/`.

| case | conf (1 line unless shown) | expected (base.py, verified) | forger reads |
|---|---|---|---|
| S1a form-feed prefix (R1 l. 26: "leading spaces/tabs") | `\x0ckernel_path: boot():/EFI/x.efi#<H>` | rc 0 HEALTHY, pins `[]` (the line is not a key line) | f01: 1 pin `(1, OK, none)` |
| S1b vertical-tab suffix (R1 l. 28: "trailing spaces/tabs/CR") | `path: boot():/EFI/x.efi#<H>\x0b` | rc 1 DEGRADED, `(1, LP-HASH-FORMAT, panic)` (hash is 129 chars) | f01: rc 0 HEALTHY, 1 OK pin |
| S2 optional missing (R6 l. 45: "LP-MISSING ... -> not-modelled") | `wallpaper: boot():/absent.png#<H>` (file absent) | rc 1 DEGRADED, `(1, LP-MISSING, not-modelled)` | f03: `(1, LP-MISSING, skip)` |
| S3 zero pins (R7 l. 51: "else HEALTHY rc 0") | `# nothing to pin` / `timeout: 5` | rc 0 HEALTHY, pins `[]` | f06: rc 2 CANNOT-EVALUATE |
| S4 double gzip marker (R4 l. 38: "a leading `$` ... is dropped") | `path: $$boot():/EFI/x.efi#<H>` | rc 2 CANNOT-EVALUATE, `(1, LP-UNRESOLVED, not-modelled)` | f07: rc 0 HEALTHY, 1 OK pin |
| S5 entry label trailing `+` (R8 l. 57) | `/+Arch+` / `path: boot():/EFI/x.efi#<H>` | pin `entry` = `"Arch+"` | f08: `entry` = `"Arch"` |
| S6 panic value trailing tab (R8 l. 58 "its R1 value") | `hash_mismatch_panic: no<TAB>` / `path: boot():/EFI/x.efi#<wrong>` | `hash_mismatch_panic` = `{"line": 1, "value": "no"}`, consequence `prompt` | f12: `value` = `"no\t"`, consequence `panic` |
| S7 CR inside the line (R1 l. 23/28 "strip CR ... per line") | `path: boot():\r/EFI/x.efi#<H>` | rc 0 HEALTHY, `(1, OK, none)` (CR stripped from the line) | f14: rc 0 HEALTHY, pins `[]` (no `):/` after the CR) |
| S8 optional unresolved (R6 l. 45) | `term_font: boot(2):/fonts/x#<H>` | rc 2 CANNOT-EVALUATE, `(1, LP-UNRESOLVED, not-modelled)` | f16: `(1, LP-UNRESOLVED, skip)` |
| S9 resource name case (R4 l. 39 "resource `boot`") | `path: BOOT():/EFI/x.efi#<H>` | rc 2 CANNOT-EVALUATE, `(1, LP-UNRESOLVED, not-modelled)` | f18: rc 0 HEALTHY, 1 OK pin |
| S10 label trim after prefix (R8 l. 57 "..., trimmed") | `/+ Arch` / `path: boot():/EFI/x.efi#<H>` | pin `entry` = `"Arch"` | f19: `entry` = `" Arch"` |

Observed pairs (scratch probe, base.py vs the forger, same conf):

```
S1a  base rc=0 HEALTHY []                                      f01 rc=0 HEALTHY [(1,'OK','none',None)]
S1b  base rc=1 DEGRADED [(1,'LP-HASH-FORMAT','panic',None)]    f01 rc=0 HEALTHY [(1,'OK','none',None)]
S2   base rc=1 DEGRADED [(1,'LP-MISSING','not-modelled',None)] f03 rc=1 DEGRADED [(1,'LP-MISSING','skip',None)]
S3   base rc=0 HEALTHY []                                      f06 rc=2 CANNOT-EVALUATE []
S4   base rc=2 CANNOT-EVALUATE [(1,'LP-UNRESOLVED','not-modelled',None)]  f07 rc=0 HEALTHY [(1,'OK','none',None)]
S5   base rc=0 HEALTHY [(2,'OK','none','Arch+')]               f08 rc=0 HEALTHY [(2,'OK','none','Arch')]
S6   base rc=1 DEGRADED [(2,'LP-MISMATCH','prompt',None)] value "no"   f12 rc=1 DEGRADED [(2,'LP-MISMATCH','panic',None)] value "no\t"
S7   base rc=0 HEALTHY [(1,'OK','none',None)]                  f14 rc=0 HEALTHY []
S8   base rc=2 CANNOT-EVALUATE [(1,'LP-UNRESOLVED','not-modelled',None)]  f16 rc=2 CANNOT-EVALUATE [(1,'LP-UNRESOLVED','skip',None)]
S9   base rc=2 CANNOT-EVALUATE [(1,'LP-UNRESOLVED','not-modelled',None)]  f18 rc=0 HEALTHY [(1,'OK','none',None)]
S10  base rc=0 HEALTHY [(2,'OK','none','Arch')]                f19 rc=0 HEALTHY [(2,'OK','none',' Arch')]
```

Notes for the L1:
- S6 needs the optional-field comparison (the consequence already differs here, but a case whose
  setting line is otherwise inert keeps the metadata assertion the point: with a *matching* pin and
  `hash_mismatch_panic: no<TAB>` the only difference is the reported value).
- S7's failure shape is the worst one for operability: the pin is silently dropped, not reported as
  damaged. It is the same shape as r87's m05 (`PAREN-PATH`) gap.
- S1a/S1b, S4, S9 are tolerance directions (a gate that is too lenient about the written bytes). S2, S3,
  S8 are consequence/verdict table gaps. S5, S6, S10 are R8 reporting gaps.
- If all ten land as cases, the r88 battery's written-clause coverage becomes complete for every clause
  this seat could bend without reading the gate source; C1's roster predicate is unchanged either way.
