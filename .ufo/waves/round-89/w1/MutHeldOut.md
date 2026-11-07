# MutHeldOut — held-out discrimination of the r89 battery (round 89, wave w1)

Seat: mutation-tester (leaf). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Lane revision measured: `665408cc45a88ed49717e22f4593e8e6152ac665` (`git rev-parse master`).
Base gate: `.ufo/waves/round-89/before/roster/pos-landed-gate-3ba37eb0.py`,
sha256 `e3b0fab4f2d276fe579b64ce5c8741a065bd9afe281257d38aa2209062407352` (equals the roster digest in
`roster-r89.json`, so the base is the frozen P-landed-gate and not a moving file).

No lane file, roster file, counter, scorecard, manifest or host state was modified. Nothing was
installed; no pacman/uv/npm call was made. All fixtures live under
`/fast/scratch/hyaku/tsukuroi-r89/MutHeldOut/` (removed at the end); receipts are in this directory.

## 1. What was run

* 23 new single-point mutants of the pristine gate (`mutants/`, one `@@` hunk each — verified with
  `grep -c '^@@' mutants/*.diff` = 1 for all 23), each bending one R1-R8 clause of the
  `tools/limine-pin-battery-r89.py` docstring. 22 change behaviour, 1 is marked **EQUIVALENT**
  (`h47-entry-trim-redundant`); the equivalence is proved by its probe (identical answer) and by
  R1: the line is already `strip(" \t")`-ed before the label is read.
* 23 probe witnesses (`probes/<id>.json` built by `probe_harness.py`, answers in
  `probes/<id>.out.json`, table in §3): pristine vs mutant on the same conf/ESP bytes.
* Both batteries on the pristine gate and on every mutant, `--runs 3`:

```
python3 tools/limine-pin-battery-r89.py --gate <GATE> --runs 3 --work $S/tmp-<id> --json $S/bat/<id>.r89.json
python3 tools/limine-pin-battery-r88.py --gate <GATE> --runs 3 --work $S/tmp-<id> --json $S/bat/<id>.r88.json
```

The frozen r89 counter was deliberately not used: it judges roster gates over an opaque launcher and
one battery per gate, while these are held-out probes that are not in the roster (the counter would
answer a roster mismatch, not a discrimination result). Driver: `receipts/battery-logs/index.txt`,
verbatim stdout per gate in `receipts/battery-logs/<id>.r8{8,9}.log`.

Baseline (pristine gate, my own receipts, not a re-run of anyone's claim):

```
$ cat receipts/battery-logs/pristine.r89.log
families_passed 50/50 verdict met failed -
families_passed 50/50 verdict met failed -
families_passed 50/50 verdict met failed -

$ cat receipts/battery-logs/pristine.r88.log
families_passed 38/38 verdict met failed -
families_passed 38/38 verdict met failed -
families_passed 38/38 verdict met failed -
```

Both baselines are `met` on all three runs, so every non-zero kill count below is a kill and not a
baseline artefact.

## 2. Discrimination table (r88 vs r89)

`killed` = runs (of 3) in which the battery did NOT return `met`. `3/3` means the battery catches
the mutant deterministically; `0/3` means the mutant survives the battery.

| mutant | clause bent | r88 killed | r89 killed | r89 families that failed |
|---|---|---|---|---|
| `h25-traversal-uncontained` | R4 path containment (`..` leaves the ESP -> LP-UNRESOLVED) | 0/3 | 0/3 | - |
| `h26-symlink-abspath` | R4 a symlink pointing outside the ESP -> LP-UNRESOLVED | 0/3 | 0/3 | - |
| `h27-contain-prefix-only` | R4 containment is a path-component test, not a string prefix | 0/3 | 0/3 | - |
| `h28-bare-key-line-crash` | R1 a line of key characters with no `:` is not a key line (must not crash) | 0/3 | 0/3 | - |
| `h29-hash-first-mib` | R5 BLAKE2b-512 over ALL raw stored bytes (no size truncation) | 0/3 | 0/3 | - |
| `h30-panic-after-pin` | R6 the prompt rule reads the FIRST `hash_mismatch_panic` key line in the WHOLE file | 0/3 | 0/3 | - |
| `h31-any-hex-char` | R3 the hash must be ENTIRELY `[0-9a-fA-F]` | 3/3 | 3/3 | FORMAT-BEFORE-RESOLVE, HASH-NONHEX, OPTIONAL-HASH-FORMAT |
| `h32-len-at-most` | R3 the hash must be EXACTLY 128 characters | 3/3 | 3/3 | FORMAT-BEFORE-RESOLVE, HASH-LENGTH, MULTI-FAULT, OPTIONAL-HASH-FORMAT |
| `h33-exit-zero` | R7/output contract: the process exit code equals `rc` | 3/3 | 3/3 | ALL-PIN-KEYS, BLANK-CLASS, CONF-UNREADABLE, CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH (+37 more) |
| `h34-sb-absent-enforced` | R7 `--secure-boot-enforced 0` and an absent flag both mean not enforced | 3/3 | 3/3 | ALL-PIN-KEYS, HOST-SHAPE, MULTI-FAULT, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-VALUE-BLANKS |
| `h35-missing-consequence-skip` | R6 LP-MISSING consequence is `not-modelled` | 3/3 | 3/3 | EMPTY-PATH, MISSING, MULTI-FAULT, OPTIONAL-MISSING |
| `h36-unresolved-consequence-none` | R6 LP-UNRESOLVED consequence is `not-modelled` | 3/3 | 3/3 | DOUBLE-DOLLAR, EMPTY-ROOT-RESOURCE, MULTI-FAULT, OPTIONAL-UNRESOLVED, RESOURCE-CASE, ROOT-ON-BOOT (+1 more) |
| `h37-dir-as-file` | R5 a path naming a directory is LP-MISSING, not an error | **0/3** | **3/3** | EMPTY-PATH |
| `h38-optional-dtb` | R6 only wallpaper/term_font are optional (dtb_path is not) | 3/3 | 3/3 | ALL-PIN-KEYS, KEY-CASE |
| `h39-hash-prefix-compare` | R5 the WHOLE 128-hexdigit digest is compared | 3/3 | 3/3 | ALL-PIN-KEYS, CR-INTERNAL, ENTRY-LABEL, ENTRY-LABEL-EDGES, FIRST-URI-SEP, HOST-SHAPE (+19 more) |
| `h40-entry-first-sticks` | R8 the entry label is the NEAREST preceding entry line | 3/3 | 3/3 | ALL-PIN-KEYS, BLANK-CLASS, CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH, EMPTY-ROOT-RESOURCE (+29 more) |
| `h41-root-whitespace` | R4 a NON-empty root (a blank) does not resolve | 0/3 | 0/3 | - |
| `h42-plus-slash-lstrip` | R8 label = strip the leading `/` run, THEN one leading `+` | 0/3 | 0/3 | - |
| `h43-empty-label-entry` | R8 an entry line with an empty label keeps the previous label | 0/3 | 0/3 | - |
| `h44-empty-resource-boot` | R4 only resource `boot` resolves (the empty resource does not) | 0/3 | 0/3 | - |
| `h45-isdir-check` | R5 an absent file is LP-MISSING (not an unreadable/UNRESOLVED error) | 3/3 | 3/3 | MISSING, MULTI-FAULT, OPTIONAL-MISSING |
| `h46-conf-decode-strict` | R1/R7 a readable conf with non-UTF-8 bytes still parses (`surrogateescape`) | 0/3 | 0/3 | - |
| `h47-entry-trim-redundant` | R8 trim of the label is redundant (R1 already stripped the line) — **EQUIVALENT** | 0/3 | 0/3 | (equivalent: probe differs=False) |

Machine-readable form (per-run failures, all 50/38 family names): `battery-results.json`,
`battery-table.txt`.

## 3. Kill counts

* **r88: 10 / 22 non-equivalent mutants killed** (23/23 counting the equivalent one as "survived",
  which is correct: an equivalent mutant must survive).
* **r89: 11 / 22 non-equivalent mutants killed.**
* Pristine baseline in both: `met`, 3/3 runs, 0 failed families → no baseline failure, so no
  inconclusive row.
* The single r89-vs-r88 delta is `h37-dir-as-file`, caught **only** by `EMPTY-PATH`
  (`tools/limine-pin-battery-r89.py:833`), the r89-new family that pins `boot():/#hash`, i.e. a pin
  whose path names the ESP directory. r88 has no fixture whose pin names a directory:
  `receipts/battery-logs/h37-dir-as-file.r88.log` = `families_passed 38/38 verdict met` ×3.

## 4. Survivors and the clause each bends (coverage findings, not contract changes)

11 non-equivalent mutants survive r89 and the same 11 survive r88 (the two survivor sets are identical; `h37` is the only mutant whose verdict differs between them).
Each row names the fixture the battery does not generate.

| mutant | clause it bends | missing fixture | witness answer |
|---|---|---|---|
| `h25-traversal-uncontained` | R4 containment: the gate's own r87 hardening says a path leaving `--esp` is LP-UNRESOLVED. `resolve_in_esp` returns the joined target unchecked. | a conf pin `path: boot():/../<name>#<b2>` where `<name>` is a regular file beside the ESP carrying that hash; no family writes a file outside the ESP or a `..` component. | pristine rc2 CANNOT-EVALUATE / LP-UNRESOLVED; mutant rc0 HEALTHY / OK |
| `h26-symlink-abspath` | R4 containment for symlinks: `realpath` replaced by `abspath`, so an ESP symlink to an outside file is treated as inside. | an ESP entry that is a symlink to a file beside the ESP, pinned with that file's true hash; no family creates a symlink. | pristine LP-UNRESOLVED rc2; mutant OK rc0 |
| `h27-contain-prefix-only` | R4 containment must be a path-component test (`root + os.sep`), not a string prefix. | ESP symlink to `<espname>x/f.efi` (sibling whose name shares the ESP prefix); again needs a symlink. | pristine LP-UNRESOLVED rc2; mutant OK rc0 |
| `h28-bare-key-line-crash` | R1: a line of key characters with no `:` is simply not a key line (and R7 still answers). `i >= len(line)` widened to `i > len(line)` makes the parser raise IndexError. | a conf line that is a bare token, e.g. `timeout` alone; every family writes `KEY: value` or `#...` lines, never a colon-less key-char line. | pristine HEALTHY rc0; mutant exit 1, no JSON (traceback) |
| `h29-hash-first-mib` | R5: BLAKE2b-512 over ALL raw stored bytes. The hash loop `break`s after the first 1 MiB chunk. | an ESP file larger than 1 MiB pinned with its true hash; `Case.blob` is bounded at 4096 bytes (`tools/limine-pin-battery-r89.py:144`), so no fixture crosses one chunk. | pristine OK rc0; mutant LP-MISMATCH rc1 |
| `h30-panic-after-pin` | R6: the prompt rule reads the FIRST `hash_mismatch_panic` key line "in the whole file". The mutant only accepts one seen before any pin. | a conf whose `hash_mismatch_panic: no` line comes AFTER the mismatching pin; every family (`set_panic`, `HOST_TEMPLATE`) writes it before the pins. | pristine `prompt` rc1; mutant `panic` rc1 |
| `h41-root-whitespace` | R4: a non-empty root does not resolve (root `" "` is not empty). `uri["root"]` compared with `.strip()`. | a pin `path: boot( ):/<file>#<b2>`; families only draw `boot()`, `boot(N)` and named resources. | pristine LP-UNRESOLVED rc2; mutant OK rc0 |
| `h42-plus-slash-lstrip` | R8: strip the leading `/` run, then ONE leading `+`. `lstrip("/+")` also eats slashes after the `+`. | an entry line `/+/<label>`; `fam_entry_label_edges` (`:763`) only writes `/+/` with no slash between `+` and the label (`/+name`). | pristine entry `"/alpha"`; mutant `"alpha"` |
| `h43-empty-label-entry` | R8: an entry line whose label is empty keeps the previous label (`or entry`). The mutant sets `""`. | an entry line `//` with no label between two labelled entries; no family writes an empty label (all forms append `rname`). | pristine entry `"alpha"`; mutant `""` |
| `h44-empty-resource-boot` | R4: only resource `boot` resolves; `(root):/path#h` (empty resource) is not `boot`. | a pin `path: ():/<file>#<b2>`; `fam_empty_root_resource` (`:595`) writes named resources (`hdd()`, `odd()`, ...), never an empty name. | pristine LP-UNRESOLVED rc2; mutant OK rc0 |
| `h46-conf-decode-strict` | R1/R7: a readable conf with non-UTF-8 bytes still parses (the gate decodes with `surrogateescape`); strict decoding aborts the whole evaluation. | a conf containing a byte such as `0xFF` (e.g. inside a comment line) plus one valid pin; every family writes ASCII confs only. | pristine HEALTHY rc0 with the OK pin; mutant exit 1, no JSON (UnicodeDecodeError) |

Not a coverage gap: `h47-entry-trim-redundant` is **EQUIVALENT** — `check()` has already done
`raw.replace("\r", "").strip(" \t")` before the entry label is read, so the extra `strip()` on the
label is dead work; the probe answers are byte-identical, so surviving both batteries is correct.

## 5. Probe witnesses (pristine vs mutant on the same bytes)

| mutant | pristine | mutant |
|---|---|---|
| `h25-traversal-uncontained` | exit 2 CANNOT-EVALUATE pins [[2,LP-UNRESOLVED,not-modelled]] | exit 0 HEALTHY pins [[2,OK,none]] |
| `h26-symlink-abspath` | exit 2 CANNOT-EVALUATE pins [[2,LP-UNRESOLVED,not-modelled]] | exit 0 HEALTHY pins [[2,OK,none]] |
| `h27-contain-prefix-only` | exit 2 CANNOT-EVALUATE pins [[2,LP-UNRESOLVED,not-modelled]] | exit 0 HEALTHY pins [[2,OK,none]] |
| `h28-bare-key-line-crash` | exit 0 HEALTHY pins [[3,OK,none]] | exit 1, no JSON (IndexError: string index out of range) |
| `h29-hash-first-mib` | exit 0 HEALTHY pins [[2,OK,none]] | exit 1 DEGRADED pins [[2,LP-MISMATCH,panic]] |
| `h30-panic-after-pin` | exit 1 DEGRADED pins [[2,LP-MISMATCH,prompt]] | exit 1 DEGRADED pins [[2,LP-MISMATCH,panic]] |
| `h31-any-hex-char` | exit 1 DEGRADED pins [[2,LP-HASH-FORMAT,panic]] | exit 1 DEGRADED pins [[2,LP-MISMATCH,panic]] |
| `h32-len-at-most` | exit 1 DEGRADED pins [[2,LP-HASH-FORMAT,panic]] | exit 1 DEGRADED pins [[2,LP-MISMATCH,panic]] |
| `h33-exit-zero` | exit 1 DEGRADED (rc field 1) | exit 0 DEGRADED (rc field 1) |
| `h34-sb-absent-enforced` | exit 1 DEGRADED pins [[2,LP-MISMATCH,prompt]] (no flag passed) | exit 1 DEGRADED pins [[2,LP-MISMATCH,panic]] |
| `h35-missing-consequence-skip` | exit 1 DEGRADED pins [[2,LP-MISSING,not-modelled]] | exit 1 DEGRADED pins [[2,LP-MISSING,skip]] |
| `h36-unresolved-consequence-none` | exit 2 CANNOT-EVALUATE pins [[2,LP-UNRESOLVED,not-modelled]] | exit 2 CANNOT-EVALUATE pins [[2,LP-UNRESOLVED,none]] |
| `h37-dir-as-file` | exit 1 DEGRADED pins [[2,LP-MISSING,not-modelled]] | exit 2 CANNOT-EVALUATE pins [[2,LP-UNRESOLVED,not-modelled]] |
| `h38-optional-dtb` | exit 1 DEGRADED pins [[2,LP-MISMATCH,panic]] | exit 1 DEGRADED pins [[2,LP-MISMATCH,skip]] |
| `h39-hash-prefix-compare` | exit 1 DEGRADED pins [[2,LP-MISMATCH,panic]] | exit 0 HEALTHY pins [[2,OK,none]] |
| `h40-entry-first-sticks` | entries {2:alpha, 4:beta} | entries {2:alpha, 4:alpha} |
| `h41-root-whitespace` | exit 2 CANNOT-EVALUATE pins [[2,LP-UNRESOLVED,not-modelled]] | exit 0 HEALTHY pins [[2,OK,none]] |
| `h42-plus-slash-lstrip` | entry "/alpha" | entry "alpha" |
| `h43-empty-label-entry` | entry "alpha" | entry "" |
| `h44-empty-resource-boot` | exit 2 CANNOT-EVALUATE pins [[2,LP-UNRESOLVED,not-modelled]] | exit 0 HEALTHY pins [[2,OK,none]] |
| `h45-isdir-check` | exit 1 DEGRADED pins [[2,LP-MISSING,not-modelled]] | exit 2 CANNOT-EVALUATE pins [[2,LP-UNRESOLVED,not-modelled]] |
| `h46-conf-decode-strict` | exit 0 HEALTHY pins [[3,OK,none]] | exit 1, no JSON (UnicodeDecodeError) |
| `h47-entry-trim-redundant` | exit 0 HEALTHY pins [[2,OK,none]] entries {2:alpha} | identical to pristine (EQUIVALENT) |

Sample case the battery used to kill (verbatim from `w1/MutHeldOut/receipts/h37-dir-as-file.r89.json`, run 1): family
`EMPTY-PATH`, `want` `[1,"DEGRADED",[[4,"LP-MISSING","not-modelled"],[7,"OK","none"]]]`, `got`
`[2,"CANNOT-EVALUATE",[[4,"LP-UNRESOLVED","not-modelled"],[7,"OK","none"]],2]`.

## 6. Observations for the L1 (no patch applied; nothing in the lane was edited)

1. `tools/limine-pin-battery-r89.py:859` (`FAMILIES`) / `:914` (`FAMILY_ROSTER`): six clauses have no
   family at all — R4 containment for `..` and symlinks (`h25`-`h27`), R4 root/resource edges
   (`h41`, `h44`), R1/R7 non-UTF-8 conf (`h46`). Note the R4 containment clause is stated in the
   *gate* docstring ("round-87 hardening, not a Limine rule") and not in the r89 battery docstring;
   if the battery is meant to certify only Limine rules, the docstring's "Not modelled" list should
   say so explicitly, otherwise a gate that resolves outside the ESP passes both batteries.
2. `tools/limine-pin-battery-r89.py:143` (`Case.blob`, bound at `:144`) bounds every fixture file at 4096 bytes, so a
   gate that hashes only the first chunk of a large file (`h29`) is invisible.
3. `tools/limine-pin-battery-r89.py:255` (`set_panic`) is only ever called before the pins, so the
   R6 "whole file" reading (`h30`) is untested.
4. `tools/limine-pin-battery-r89.py:763` (`fam_entry_label_edges`) never writes `/+/` (a slash after
   the `+`), an empty-label entry line, or a bare colon-less token line — `h42`, `h43`, `h28`.
5. `tools/limine-pin-battery-r89.py:972` (`r8_ok`): `state == "absent"` returns True, so a gate that
   never emits `hash_mismatch_panic` passes. R8 says the field MAY be carried, so this is contract
   conformant — recorded so nobody reads it as an escape.
6. Deterministic kills worth knowing: `h39` (compare only the first 64 hexdigits) is killed by
   `MISMATCH-LATE` only because that family always flips the LAST hexdigit; `MISMATCH-EARLY` (first
   hexdigit) cannot see it. The kill is still 3/3 because MISMATCH-LATE is deterministic.

## 7. Files

* `mutants/` — 23 mutants (`.py`, `.diff` one hunk each) + `manifest.json` (sha256, clause, probe).
* `probes/` — 23 specs (`.json`), 23 answer pairs (`.out.json`); `probe-summary.json`.
* `battery-results.json`, `battery-table.txt` — per-run verdicts and failed families for both batteries.
* `receipts/battery-logs/` — verbatim battery stdout for all 24 gates × 2 batteries, `index.txt` exit codes.
* `probe_harness.py`, `gen.py`, `analyze.py` — the three tools used (read-only w.r.t. the lane).

Refused / not done: no `sudo`, no host write, no `limine*`/`objcopy`/`snapper`/`pacman` call, no
commit/push/jj, no message to `agent://all`, no subagent, no model choice. Scratch
`/fast/scratch/hyaku/tsukuroi-r89/MutHeldOut` deleted after the receipts were copied here.
