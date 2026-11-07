# CriticForgers — docstring-only forgers against the round-88 Limine pin battery

Seat: `CriticForgers` (w1, round 88). Lane: `tsukuroi-shokunin`, branch `master`.
Lane revision measured: `1fac4195243e55e7d9d8a2eddd653443d8559bff`
(`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`).
Candidate under test: `tools/limine-pin-battery-r88.py` at commit
`5b98ca98c9a19641e77832bc57579d95fa5571a3`, sha256
`ab6c1b33f84dd252979296d1b56ccea8c5e89af221e02e1ec08ef8e579fac374` (working-tree blob equals the
candidate blob; `git status --porcelain` on it is empty). Frozen counter:
`tools/battery-discrimination-r88.py`, sha256
`7d2073dfd120c8ac5ebaf8c68e7c270f970b5c7a75850561d7ceb9db76c13305`.
Axis: **operability** (the assurance arm of the `limine-pins` gate, C1).

## 1. What was read (independence)

Only the **module docstring** of the r88 battery (rule set R1-R8, lines 23-60 of that file) and the
frozen roster's `id`/`basis` fields. `tools/check-limine-pins.py` was **never opened**; no battery
body, family implementation, fixture generator or `_lib.py` was read. `base.py` is a reimplementation
from the docstring alone. The only outside hints were the roster basis strings (what the 48 frozen
gates bend) and the r87 MutGate report table (which families the r87 battery had); no r88 gate source.
One `grep -n` run to locate docstring line numbers also surfaced two family docstring lines
(`ROOT-ON-BOOT`); they restate R4 from the module docstring and were not used.

## 2. Faithful reimplementation — `met` 3/3 (no docstring/expectation disagreement)

`base.py` (sha256 `e1663ef35d15517d36541a816652fee25a77156283daa39681718bcb89a63912`) implements
R1-R8 including the optional R8 fields.

Command (cwd = `$S`, `TMPDIR=$S`; exact argv; each gate got its own `--work` subdir under `$S/work/`
instead of one shared `"$S/work"`, so the six-way overlap could not collide):

```
$ python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/limine-pin-battery-r88.py \
      --gate /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-88/w1/CriticForgers/base.py \
      --runs 3 --work /fast/scratch/hyaku/tsukuroi-r88/CriticForgers/work/base \
      --json /fast/scratch/hyaku/tsukuroi-r88/CriticForgers/out/base.json
families_passed 38/38 verdict met failed -
families_passed 38/38 verdict met failed -
families_passed 38/38 verdict met failed -
rc=0
```

`receipts/base.runs.json` records 3 runs x 152 cases, 38 families, every case matched (including the
optional `entry` and `hash_mismatch_panic` fields). There is **no** docstring/expectation disagreement
to report as a battery defect.

## 3. Method

`gen.py` derives 19 one-clause forgers from `base.py` by a **single-occurrence literal replacement**
(it aborts unless the anchor occurs exactly once), writes one `.diff` per forger and `forgers.json`
with the clause text and sha256. Every gate ran 3x with the same command as above (own `--work` dir);
full stdout is in `receipts/<name>.out`. Two controls (`ctl-*`) lie about an optional R8 field to show
that the battery's optional-field assertions are live. Nothing was installed; no host contact; the
lane tree was not mutated (these files are untracked under my own wave dir).

## 4. Results (3 runs each)

| forger | clause bent | runs | outcome |
|---|---|---|---|
| f01-any-whitespace-blank-class | R1 blank class: `strip(None)` instead of `" \t"` | 38/38, 38/38, 38/38 | **MET — survives** |
| f02-panic-value-prefix-no | R6 value "equal to `no`": `startswith("no")` | 37/38, 37/38, 37/38 | unmet, `PANIC-NON-NO` |
| f03-optional-missing-skip | R6 `LP-MISSING -> not-modelled` for optional keys | 38/38 x3 | **MET — survives** |
| f04-optional-term-font-dropped | R6 "wallpaper or term_font" (term_font dropped) | 35/38, 35/38, 36/38 | unmet, `OPTIONAL-*`, `ALL-PIN-KEYS` |
| f05-hash-128-any-chars | R3 "[0-9a-fA-F]" char set (length only) | 35/38, 36/38, 35/38 | unmet, `HASH-NONHEX`, `OPTIONAL-HASH-FORMAT`, `FORMAT-BEFORE-RESOLVE` |
| f06-empty-pin-list-cannot-evaluate | R7 `else HEALTHY rc0` on an empty pin list | 38/38 x3 | **MET — survives** |
| f07-dollar-lstrip-all | R4 "a leading `$`" (one marker) | 38/38 x3 | **MET — survives** |
| f08-entry-label-trailing-plus | R8 label "without a leading `+`, trimmed" | 38/38 x3 | **MET — survives** |
| f09-entry-null-as-empty-string | R8 "or null before any entry line" | 36/38 x3 | unmet, `OPTIONAL-HASH-FORMAT`, `OPTIONAL-SKIP` |
| f10-entry-first-not-nearest | R8 "nearest preceding entry line" | 10/38 x3 | unmet, 28 families incl. `ENTRY-LABEL` |
| f11-entry-requires-column-zero | R8 "first non-blank character is `/`" | 36/38 x3 | unmet, `ENTRY-LABEL`, `HOST-SHAPE` |
| f12-panic-value-raw-trailing-blanks | R8 "value: its R1 value" (trailing blanks kept) | 38/38 x3 | **MET — survives** |
| f13-unhashed-uri-reports-format | R2 "no `#` after `):/` ... not a pin" | 36/38 x3 | unmet, `HOST-SHAPE`, `UNHASHED-DECOYS` |
| f14-cr-stripped-only-trailing | R1 "strip CR ... per line" (only a trailing CR) | 38/38 x3 | **MET — survives** |
| f15-esp-join-no-separator | R4 "resolves to ESP/path" (no separator) | 2/38 x3 | unmet, 36 families |
| f16-optional-unresolved-skip | R6 `LP-UNRESOLVED -> not-modelled` for optional keys | 38/38 x3 | **MET — survives** |
| f17-entry-one-leading-slash | R8 "without its leading `/` characters" | 36/38 x3 | unmet, `ENTRY-LABEL`, `HOST-SHAPE` |
| f18-resource-case-insensitive | R4 "resource `boot`" (case-folded) | 38/38 x3 | **MET — survives** |
| f19-entry-label-not-trimmed | R8 label "..., trimmed" | 38/38 x3 | **MET — survives** |
| ctl-meta-value-lie | control: metadata value `+ "!"` | 25/38, 25/38, 26/38 | unmet, incl. `PANIC-METADATA` |
| ctl-entry-label-lie | control: entry label `+ "!"` | 2/38 x3 | unmet, incl. `ENTRY-LABEL` |

Verbatim survivor line (f01; the other nine are byte-identical, see `receipts/`):

```
families_passed 38/38 verdict met failed -
families_passed 38/38 verdict met failed -
families_passed 38/38 verdict met failed -
rc=0
```

## 5. Surviving forgers — ten written clauses uncertified by r88

Each survived 3/3 runs (456 cases). Each bends exactly one written clause; none duplicates a bend in the
frozen roster (g01-g16, m02-m30). The controls in section 7 show this is not an optional-field
tolerance artefact.

| # | forger | clause (docstring line) | discriminating input class |
|---|---|---|---|
| 1 | f01 | R1 "leading spaces/tabs" / "trailing spaces/tabs" (l. 26, 28): `str.strip(None)` | a key line whose blanks are `\x0c`, `\x0b`, NBSP ...; a value ending in `\x0b` |
| 2 | f03 | R6 "LP-MISSING ... -> `not-modelled`" (l. 45) for `wallpaper`/`term_font` | an optional-resource pin whose file is absent |
| 3 | f06 | R7 "else HEALTHY rc 0" (l. 51) on zero pins | a readable conf with only comments / non-pin keys |
| 4 | f07 | R4 "a leading `$` (gzip marker) is dropped" (l. 38) | `$$boot():/...` (double marker) |
| 5 | f08 | R8 label "without a leading `+`, trimmed" (l. 57) | an entry label ending in `+` (`/+Arch+`) |
| 6 | f12 | R8 "value: its R1 value" (l. 58) | `hash_mismatch_panic: no<TAB>` (trailing blank) |
| 7 | f14 | R1 "strip CR ... per line" / "trailing ... CR removed" (l. 23, 28) | a CR inside the line (`boot():\r/EFI/x.efi#...`) |
| 8 | f16 | R6 "LP-UNRESOLVED -> `not-modelled`" (l. 45) for optional keys | `term_font: boot(2):/...` (unresolved optional) |
| 9 | f18 | R4 "resource `boot`" (l. 39) | `BOOT():/...` (resource name case) |
| 10 | f19 | R8 label "..., trimmed" (l. 57) | an entry line with a blank after the prefix (`/+ Arch`) |

Smallest safe correction per clause (exact conf + expected record) is written up in
`proposed-cases-r88.md`; each is one case, not a new family. Why they matter: the battery is the
assurance instrument for a host-boot gate, so a gate that keeps a mid-line CR, folds the resource case,
treats `$$boot` as `boot`, skips a missing optional pin, or lies about the panic value still reads
`met` today — the written rule is not asserted anywhere in the fixture set.

These ten are sub-clauses outside the r87 lesson's R87-R1..R5 list. They do **not** re-scope C1: the
frozen roster's 48 gates are untouched, and the counter's discrimination claim is about those gates.
What they bound is the docstring's assurance sentence ("the families ... each certify one R1-R7
clause"): the ten clauses below the family granularity are not certified by any family.

## 6. Discriminated forgers (the battery does real work beyond the roster)

- f02: `PANIC-NON-NO` every run — value must equal `no`, not merely start with it.
- f04: `OPTIONAL-HASH-FORMAT` and `OPTIONAL-SKIP` every run (term_font case present); `ALL-PIN-KEYS` in 2/3.
- f05: `HASH-NONHEX` and `OPTIONAL-HASH-FORMAT` every run; `FORMAT-BEFORE-RESOLVE` in 2/3.
- f09: `OPTIONAL-HASH-FORMAT`, `OPTIONAL-SKIP` every run (pins before the first entry line exist there).
- f10: 28 families, incl. `ENTRY-LABEL` — nearest-entry tracking is asserted.
- f11: `ENTRY-LABEL`, `HOST-SHAPE` — indented entry lines exist.
- f13: `HOST-SHAPE`, `UNHASHED-DECOYS` — a URI-form value with no `#` is a decoy, not a pin.
- f15: 36 families — `ESP/path` resolution is exercised everywhere.
- f17: `ENTRY-LABEL`, `HOST-SHAPE` — labels with two or more leading `/` exist.

## 7. Controls — the optional-field comparisons are live

`ctl-meta-value-lie` (every emitted `hash_mismatch_panic.value` is wrong) is killed by 13 families on
two runs and 12 on the third, always including `PANIC-METADATA`, `PANIC-FIRST`, `PANIC-KEY-CASE`.
`ctl-entry-label-lie` (every emitted `entry` is wrong) is killed by 36/38 every run, including
`ENTRY-LABEL`. So f08/f12/f19 survive because no fixture carries the discriminating shape, not because
R8 is ignored.

## 8. Equivalence note (a discarded forger)

The first f15 candidate `os.path.join(esp, path)` (no `lstrip("/")`) was **behaviourally identical** to
`base.py`: R2 takes the path between `):/` and the last `#`, i.e. the slice starts after the `/` of the
separator, so it never begins with `/` and `lstrip("/")` is a no-op. Probe (scratch, not a receipt):
`path: boot():/EFI/Linux/x.efi#<correct>` read `OK` under both gates. It was replaced by
`esp + path` (no separator), which is genuinely wrong and is killed 36/38 — the R4 join is certified.

## 9. Sampling variance observed (evidence for the L1, not a finding against C1)

Families are re-drawn per run: f04 lost `ALL-PIN-KEYS` in one of three runs and f05 lost
`FORMAT-BEFORE-RESOLVE` in one of three. The kills stay stable because the same clause is covered by
two or more families (`OPTIONAL-*`, `HASH-NONHEX`), which is the redundancy the roster needs. No
survivor's 38/38 is explained by such a one-run draw: all ten were met in all three runs
(456/456 cases).

## 10. Environment checks (read-only, at report time)

```
$ sha256sum -c .ufo/waves/round-88/before/freeze-manifest.sha256
...
.ufo/waves/round-88/before/controls/bat-roster-oracle.py: OK
manifest_rc=0   (57/57 lines OK)
```

The 57 frozen instrument entries (counter, r87 battery, 48 roster gates + roster json, 6 controls) all
verify; C1's void condition was intact when I measured. Two environment observations, outside my seat's
scope and not used in any finding: (a) `before/src/` is not covered by those 57 entries; (b) at
21:08:42 -0300 a sibling (`TsukuroiR88`, per the note it added to `URLS.txt`) added
`before/src/limine-entry-tool-1.40.0/Main.java` (untracked) and updated `before/src/SHA256SUMS` and
`URLS.txt` in the working tree, not committed; `sha256sum -c SHA256SUMS` in that directory returns
`src_rc=0`, so the amendment is self-consistent but is a post-candidate change to the frozen snapshot
dir. No lane file was touched by this seat.

## 11. Files, bounds, cleanup

- `base.py`, `gen.py`, `forgers.json`, `f01..f19*.py` + `.diff`, `ctl-*.py` + `.diff` — this directory.
- `receipts/` — 22 `<gate>.out` with the verbatim 3-run stdout and exit code, plus `base.runs.json`
  (3 x 152 case log).
- `proposed-cases-r88.md` — one discriminating case per surviving clause.
- No lane file edited, nothing committed, no host tool run, no `sudo`, no `/boot`, no subagent. Scratch
  `/fast/scratch/hyaku/tsukuroi-r88/CriticForgers` removed after the receipts were copied.
- Tooling: none installed or upgraded.
