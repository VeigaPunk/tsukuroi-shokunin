# MutC2Counter — mutate-run-revert of `tools/check-adjacency-overlap.py` (claim C2, round 27 attempt 2)

**Verdict: partly holds.** The pristine counter is correct on every rule probe I ran, but its own
self-test pins only 6 of the 12 rule points named in the assignment (3 more are pinned only in part):
23 of 44 mutants survived both detectors, and 9 of those survivors are *counting holes* — the mutated
checker reports `anchored_rows` 6 / exit 0 / PASS on a register that the pristine checker rejects.
This is a coverage finding about the self-test suite, not a defect in the shipped checker.

| rule point named in the assignment | pinned by the self-test? | mutant that shows it |
|---|---|---|
| exact OV1-OV6 id set | no | M01, M02 survive; M37/M38 killed (duplicate protection only) |
| sibling name | no | M03 survives (counting hole) |
| pinned commit | partly | M04 killed (any other sha), M05 survives (the literal pin value) |
| snapshot sha256 = `sibling_blob_sha256` | yes | M07 killed |
| snapshot sha256 = pinned `a5368ee7…` | no | M08 survives (counting hole) |
| `..` refusal | no | M06 survives (label-only), M26 survives |
| nearest-heading rule | partly | M09 killed (wrong heading), M10 survives (lookup off-by-one) |
| quote_line window of 3 lines | partly | M14 killed (widening), M15 survives (narrowing) |
| 25-word cap | no | M12, M13 survive (both counting holes) |
| lane-side quote lookup | partly | M16 killed (lookup), M17/M18 survive (file absent, lane cap) |
| class and owner vocabulary | yes | M21, M22 killed |
| PROVINCE row requirement | partly | M24 killed (row present), M36 survives (id must be the first cell) |

Scope of the attack: the tool blob at lane revision `099c7b3f42d073203d9448807860f04c175eccd7`
(sha256 `4d992f83f1868a61d01ce77d5f91964ceb266dec52add3fb8b360b4d10a1d690`), read-only export at
`/fast/scratch/hyaku/tsuku27a2/MutC2Counter/tree`. The lane tip moved to `2e519d6` while this seat
ran (L1 is the only VCS writer); `git cat-file -p 2e519d6:tools/check-adjacency-overlap.py` hashes to
the same `4d992f83…`, so every finding below applies to the current tip as well.

---

## 1. Method

1. Export: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 099c7b3f… | tar -x -C
   /fast/scratch/hyaku/tsuku27a2/MutC2Counter/tree` (read-only export; no lane file was written).
2. Pristine bytes kept at `/fast/scratch/hyaku/tsuku27a2/MutC2Counter/pristine-check-adjacency-overlap.py`,
   sha256 `4d992f83f1868a61d01ce77d5f91964ceb266dec52add3fb8b360b4d10a1d690`, identical to
   `git cat-file -p 099c7b3f…:tools/check-adjacency-overlap.py | sha256sum`.
3. Driver `/fast/scratch/hyaku/tsuku27a2/MutC2Counter/mutate.py` (spec `mutants.json`, 44 mutants):
   for each mutant — assert the file is at the pristine sha, apply one exact-string edit (the
   `old` string must occur exactly once), `python3 -m py_compile` the result, run
   `python3 tools/check-adjacency-overlap.py --selftest` and
   `python3 tools/check-adjacency-overlap.py --revision 099c7b3f… --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
   then restore the pristine bytes and re-verify the sha256.
4. Detectors: `--selftest` is the specification-encoding detector (killed = exit ≠ 0);
   `--revision` is the real-data detector (killed = exit ≠ 0, or `anchored_rows` ≠ 6, or status ≠ PASS).
   Overall verdict = killed if either detector fires.
5. Second stage `/fast/scratch/hyaku/tsuku27a2/MutC2Counter/probes.py`: for each surviving mutant a
   fixture lane repository is built that violates exactly one declared rule, then evaluated with the
   pristine tool and with the mutant. This separates *counting holes* (the mutant accepts what the
   pristine rejects) from *label-only* survivors (same count, different reason string).

**Baseline (pristine bytes, export tree):**
- `python3 tools/check-adjacency-overlap.py --selftest` → exit 0, `{"cases": 17, "failed": 0}`.
- `python3 tools/check-adjacency-overlap.py --revision 099c7b3f… --repo …/tsukuroi-shokunin` → exit 0,
  `{"anchored_rows": 6, "expected_rows": 6, "sibling_check": "sibling-verified", "status": "PASS"}`.

**Restoration evidence:** all 44 mutants report `restore_ok: true`; after the last mutant the export
file hashes to `4d992f83f1868a61d01ce77d5f91964ceb266dec52add3fb8b360b4d10a1d690`, equal to the
pristine copy and to the revision blob (`/fast/scratch/hyaku/tsuku27a2/MutC2Counter/mutation-log.json`,
field `final_sha256`). No git write command was run against the lane; `git -C …/tsukuroi-shokunin status --porcelain`
shows only other seats' untracked report files.

---

## 2. Findings

### F1 — The self-test pins 12 of 21 rule points; 9 unpinned points are counting holes [obs]

44 mutants, 21 killed, 23 survived. Of the 23 survivors, 9 let the mutated checker report
`anchored_rows` 6 / exit 0 / PASS on input the pristine checker refuses. Probe evidence
(`/fast/scratch/hyaku/tsuku27a2/MutC2Counter/probe-log.json`):

| mutant | rule dropped | pristine on the probe | mutant on the probe |
|---|---|---|---|
| M03 | `sibling-not-mori` (tool line 109-110) | exit 1, anchored 5, `OV1: [sibling-not-mori]` | exit 0, anchored 6, PASS |
| M08 | `snapshot-not-pinned-bytes` (line 127-128) | exit 1, anchored 0, all rows `snapshot-not-pinned-bytes` | exit 0, anchored 6, PASS |
| M12 | `quote-too-long` (line 149-150) | exit 1, anchored 0, `quote-too-long` | exit 0, anchored 6, PASS |
| M13 | word cap off-by-one (`> MAX_WORDS + 1`) | exit 1, anchored 0 | exit 0, anchored 6, PASS |
| M17 | `lane-file-missing` (line 159-160) | exit 1, anchored 5, `lane-file-missing` | exit 0, anchored 6, PASS |
| M18 | `lane-quote-too-long` (line 163-164) | exit 1, anchored 0 | exit 0, anchored 6, PASS |
| M20 | `lane-side-malformed` (line 165-166) | exit 1, anchored 5 | exit 0, anchored 6, PASS |
| M27 | sibling byte comparison (line 131-132) | exit 1, anchored 0, `sibling-bytes-differ` | exit 0, anchored 6, PASS |
| M36 | PROVINCE id must be the first cell (line 173-174) | exit 1, anchored 5, `province-row-missing` | exit 0, anchored 6, PASS |

Concrete: M27's probe (P16) builds a snapshot whose bytes differ from the live mori blob at
`ef9dbee1:corpus/knowledge/audit-r11.md`; the pristine tool answers
`{"anchored_rows": 0, "status": "FAIL"}` with `sibling-bytes-differ` on every row, the mutant answers
`{"anchored_rows": 6, "status": "PASS"}`. M08's probe (P05) tampers the committed snapshot at
`PIN_PATH` and re-stamps `sibling_blob_sha256` to the tampered bytes; the pristine tool refuses
(`anchored_rows` 0, `snapshot-not-pinned-bytes`), the mutant passes.

The rule points the self-test *does* pin (killed mutants): sibling commit (M04), row digest (M07),
nearest heading (M09), window widened (M14), lane quote lookup (M16), LANE-GAP condition (M19),
class vocabulary (M21), owner vocabulary (M22), PROVINCE section (M23), PROVINCE row (M24),
snapshot directory prefix (M29), exit code (M30), anchored count (M31), id set width (M33),
duplicate protection (M37/M38), word cap with the window also removed (M42), pinned-path constant
(M43), sibling repository presence (M44).

### F2 — A1's "exactly the ids OV1 to OV6" is not enforced by the counter at all [obs]

The counter enforces "the six ids are each present exactly once", not "the register holds exactly
those six ids". Probe P01: a register with OV1…OV6 **plus** a seventh well-formed row `OV7` yields,
from the pristine tool, `{"anchored_rows": 6, "status": "PASS"}` (exit 0); the extra row appears only
in the `rows` map as `OV7: ["id-unknown", "province-row-missing"]`. The declared rule
("`corpus/knowledge/adjacency-mori-oom-r27.json` holds exactly the ids OV1 to OV6, each once", tool
docstring lines 7-8) is therefore not what `anchored_rows` measures. M01 (drop the `id-unknown`
reason, line 105-106) survives both detectors; the missing self-test case is a register that carries
an id outside OV1-OV6.

### F3 — The 25-word cap is unpinned by the existing `quote-too-long` case [obs]

The case at line 239 builds a 26-word quote (`' '.join(['w'] * 26)`) that is *also* absent from the
quote window, so the window check (line 151-152) masks the cap. Consequences: M12 (cap deleted) and
M13 (cap off-by-one, 26 accepted) both survive the self-test, and both pass a probe whose 26-word
quote *is* inside the window (P06: pristine `anchored_rows` 0 / `quote-too-long`; mutant
`anchored_rows` 6 / PASS). The compound M42 (cap **and** window removed) is killed, which confirms the
cap is observable only when the window check is also gone. Missing self-test cases: "a quote of
exactly 26 words that is inside the window must be refused" and "a quote of exactly 25 words inside
the window must be accepted" (the boundary). The same holds for the lane-side cap: M18 (lane quote
cap deleted) survives, and P08 shows the mutant accepting a 26-word lane quote that the pristine
refuses.

### F4 — The pinned-digest rule is dead code inside the self-test [obs]

`snapshot-not-pinned-bytes` (line 127-128) fires only when `spath == PIN_PATH`
(`corpus/knowledge/userspace-oom-killers-r26.md`), but the self-test fixture always uses
`sibling_path: 'x/entry.md'` (line 221, in `base()` at line 217), so the branch is never taken: M08 survives
with `failed: 0`. M43 (re-point `PIN_PATH` at the fixture path) is killed by the `clean` case, which
is the proof that the branch exists but is unreachable in the fixture. Missing self-test case: a
fixture whose `sibling_path` is `PIN_PATH` with bytes whose digest differs from `a5368ee7…`.

### F5 — The exit-2 `CANNOT_EVALUATE` contract has no self-test case [obs]

M32 (register-unreadable guard, lines 91-93), M39 (register-missing guard, lines 85-87), M40
(revision-invalid guard, lines 81-82) and M41 (`isinstance(rows, list)` assertion, line 90) all survive. Probes:
P13 (register file contains `NOT-JSON`) → pristine `exit 2, status CANNOT_EVALUATE`; M32 `exit 1`,
M41 `exit 2` but with a different finding. P14 (`rows` is a dict) → pristine `exit 2`; M32 and M41
`exit 1`. So the documented "exit 2 when the register or the snapshot cannot be read" is not pinned by
the suite: a future edit that turns it into exit 1 would pass the self-test.

### F6 — `..` refusal: the pristine rule is correct, the strict variant is a false positive [obs]

The pristine refuses a `..` *path segment* (line 115). M06 (segment refusal deleted) survives: probe
P04 shows both pristine and M06 rejecting the row, but M06 with the reason `snapshot-missing` instead
of `sibling-path-invalid` — the count is protected by the missing-snapshot path, so the refusal is
defence in depth only. M26 (substring refusal, `'..' in spath`) also survives, and probe P15 shows it
is *worse*: a legitimate path with `..` inside a segment (`x..y/entry.md`) is accepted by the
pristine (`anchored_rows` 6, PASS) and rejected by M26 (`anchored_rows` 0). Missing self-test cases:
"a sibling_path with a `..` segment is refused" and "a sibling_path whose segment contains `..` but
is not a `..` segment is accepted".

### F7 — Duplicate-id detection is protected twice, so neither guard is pinned alone [obs]

M02 (drop the `id-duplicate` reason, line 107-108) survives; probe P02 shows the pristine and M02
both report `anchored_rows` 4 — the count is protected by `ids.count(rid) == 1` in the anchored sum
(line 178). M37 (drop that count guard) is killed, but its probe shows `anchored_rows` 5, i.e. the
count guard also enforces *existence* of the id. Only the compound M38 (both guards removed) opens
the hole: P02 → `anchored_rows` 6, PASS. Missing self-test case: "a duplicated id is reported as
`id-duplicate`" (the current `duplicate-id` case only checks the count).

### F8 — Two behaviours are caught only by the real-data detector, not by the suite [obs]

- M15 (quote window narrowed from 3 lines to 2, line 151-152): the self-test passes (`failed: 0`) and
  the `--revision` run fails — `{"anchored_rows": 5, "rows": {"OV6": ["quote-not-in-window"]}}`. The
  real OV6 quote sits on the third line of the window, so the self-test fixture cannot see the
  difference. Missing self-test case: "a quote that appears only on the third line of the window
  (quote_line+1) must be found".
- M11 (the `1 <= quote_line <= len(lines)` bound removed, line 139-140): survives the self-test, and
  probe P10 shows it turns a clean refusal (`quote-line-invalid`, `anchored_rows` 5) into an uncaught
  `IndexError: list index out of range` (tool exit 1 with a traceback, not a rejection). Missing
  self-test case: "a quote_line outside the snapshot is refused".

### F9 — The pin constant is not pinned by the suite; only the live sibling cross-check catches it [obs]

M05 (re-pin `PIN_COMMIT` to a different sha, line 42) survives the self-test, because the fixture
writes the same constant into the register and compares against it (self-consistent). It is killed by
the `--revision` detector only: `{"anchored_rows": 0, "sibling_check": "sibling-mismatch", "rows": {…:
["sibling-commit-not-pinned", "sibling-bytes-differ"]}}`. Missing self-test case: a fixture whose
`sibling_commit` is the literal sha `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` while the tool's own
constant differs, i.e. the pin value itself is asserted nowhere.

### F10 — `sibling_check` reporting is unpinned [obs]

M28 (the `sibling-verified` note removed, line 134-135) survives the self-test. Measured at the
revision: pristine reports `"sibling_check": "sibling-verified"`, M28 reports
`"sibling_check": "sibling-unavailable"` with the same `anchored_rows` 6 and exit 0. The compound M44
(the sibling repository presence check removed as well) is killed by the
`sibling-unavailable-then-mismatch` case, so the *presence* half is pinned and the *byte* half (M27,
F1) and the *reporting* half (M28) are not. Missing self-test cases: "sibling_check is
`sibling-verified` when the live sibling blob equals the snapshot" and "sibling_check is
`sibling-mismatch` when the live sibling blob differs".

### F11 — Remaining label-only survivors [obs]

M10 (nearest-heading lookup starts one line too low, line 142) survives; no fixture row quotes a
heading line, so the off-by-one is invisible. Missing case: "the quote line is itself a heading".
M25 (the `snapshot-missing` reason removed, line 121-122) survives; probe P11 shows the pristine and
M25 both report `anchored_rows` 5 — the row is refused by the quote-line and heading checks, not by
the missing-snapshot rule. Missing case: "a sibling_path with no committed snapshot is refused".
M34 (`quote-missing` removed, line 146-147) and M35 (the non-string / empty `sibling_path` check
removed, line 115-116) survive: no case exercises an empty quote or an empty path. M39/M40 survive as
label-only (exit code stays 2, the `finding` string changes). Missing cases: "a row with an empty
quote", "a row with an empty sibling_path", "a revision without the register exits 2 with finding
register-missing", "an unresolvable revision exits 2 with finding revision-invalid".

### F12 — Methodology defect I introduced and fixed (recorded so the L1 can trust the table) [obs]

My first compound mutant M42 was malformed: it replaced the `if` line of the window check with
`if …: pass` and left the original `reasons.append('quote-not-in-window')` line in the block. `pass`
does not end the block, so the window check stayed live and the first M42 run falsely reported
"survived". Re-run with the body statement removed, M42 is killed (`failed: 2`,
`quote-outside-window,quote-too-long`). The driver now compiles every mutant before running it
(`py_compile` guard) and every mutant is re-verified against the pristine sha after restore. Any
future mutation run against this lane should keep that guard.

---

## 3. Full mutant table

`ST` = `--selftest` verdict (exit, number of failing cases), `REV` = `--revision 099c7b3f…` verdict
(exit, anchored_rows). Every row was restored to sha256 `4d992f83…` (`restore_ok: true`).

| id | rule point | kind | ST | REV | overall | missing self-test case (survivors) |
|---|---|---|---|---|---|---|
| M01 | A1 id set | drop | survived (0, 0) | survived (0, 6) | survived | register with an id outside OV1-OV6 (F2) |
| M02 | A1 id set | drop | survived (0, 0) | survived (0, 6) | survived | duplicated id reported as `id-duplicate` (F7) |
| M03 | A2 sibling name | drop | survived (0, 0) | survived (0, 6) | survived | row whose sibling is not `mori` (F1) |
| M04 | A2 pinned commit | drop | killed (1, 1) | survived (0, 6) | killed | — |
| M05 | A2 pinned commit | value | survived (0, 0) | killed (1, 0) | killed | pin value asserted against the literal sha (F9) |
| M06 | A2 `..` refusal | drop | survived (0, 0) | survived (0, 6) | survived | sibling_path with a `..` segment (F6) |
| M07 | A2 digest vs row | drop | killed (1, 1) | survived (0, 6) | killed | — |
| M08 | A2 digest vs pinned | drop | survived (0, 0) | survived (0, 6) | survived | fixture at `PIN_PATH` with non-pinned bytes (F4) |
| M09 | A3 nearest heading | invert | killed (1, 1) | survived (0, 6) | killed | — |
| M10 | A3 nearest heading | boundary | survived (0, 0) | survived (0, 6) | survived | the quote line is itself a heading (F11) |
| M11 | A4 quote_line bounds | drop | survived (0, 0) | survived (0, 6) | survived | quote_line outside the snapshot (F8) |
| M12 | A4 25-word cap | drop | survived (0, 0) | survived (0, 6) | survived | 26-word quote inside the window (F3) |
| M13 | A4 25-word cap | boundary | survived (0, 0) | survived (0, 6) | survived | 25/26-word boundary inside the window (F3) |
| M14 | A4 3-line window | invert | killed (1, 1) | survived (0, 6) | killed | — |
| M15 | A4 3-line window | boundary | survived (0, 0) | killed (1, 5) | killed | quote only on the third window line (F8) |
| M16 | A5 lane quote lookup | drop | killed (1, 1) | survived (0, 6) | killed | — |
| M17 | A5 lane file must exist | drop | survived (0, 0) | survived (0, 6) | survived | lane_path absent at the revision (F1) |
| M18 | A5 25-word cap | drop | survived (0, 0) | survived (0, 6) | survived | 26-word lane quote present in the lane file (F3) |
| M19 | A5 LANE-GAP | invert | killed (1, 2) | killed (1, 5) | killed | — |
| M20 | A5 lane-side shape | drop | survived (0, 0) | survived (0, 6) | survived | lane_path set with lane_quote null (F1) |
| M21 | A6 class vocabulary | drop | killed (1, 1) | survived (0, 6) | killed | — |
| M22 | A6 owner vocabulary | drop | killed (1, 1) | survived (0, 6) | killed | — |
| M23 | A7 PROVINCE section | invert | killed (1, 1) | survived (0, 6) | killed | — |
| M24 | A7 PROVINCE row | drop | killed (1, 2) | survived (0, 6) | killed | — |
| M25 | A2 snapshot must exist | drop | survived (0, 0) | survived (0, 6) | survived | sibling_path with no committed snapshot (F11) |
| M26 | A2 `..` refusal | invert | survived (0, 0) | survived (0, 6) | survived | `..` inside a segment must be accepted (F6) |
| M27 | A2 sibling byte cross-check | drop | survived (0, 0) | survived (0, 6) | survived | live sibling blob differs from the snapshot (F1) |
| M28 | A2 sibling cross-check | drop | survived (0, 0) | survived (0, 6) | survived | `sibling_check` is `sibling-verified` (F10) |
| M29 | A2 snapshot directory | drop | killed (1, 16) | killed (1, 0) | killed | — |
| M30 | exit code | drop | killed (1, 15) | survived (0, 6) | killed | — |
| M31 | anchored count | drop | killed (1, 12) | survived (0, 6) | killed | — |
| M32 | register readable | drop | survived (0, 0) | survived (0, 6) | survived | invalid JSON → exit 2 (F5) |
| M33 | id set width | boundary | killed (1, 15) | killed (1, 6) | killed | — |
| M34 | A4 quote must exist | drop | survived (0, 0) | survived (0, 6) | survived | empty or non-string quote (F11) |
| M35 | A2 sibling_path shape | drop | survived (0, 0) | survived (0, 6) | survived | empty or non-string sibling_path (F11) |
| M36 | A7 first cell | invert | survived (0, 0) | survived (0, 6) | survived | id must be the first cell of the PROVINCE row (F1) |
| M37 | A1 duplicate guard | drop | killed (1, 2) | survived (0, 6) | killed | — |
| M38 | A1 duplicate guards (compound) | compound | killed (1, 2) | survived (0, 6) | killed | — |
| M39 | register must exist | drop | survived (0, 0) | survived (0, 6) | survived | revision without the register → exit 2 (F11) |
| M40 | revision must resolve | drop | survived (0, 0) | survived (0, 6) | survived | unresolvable revision → exit 2 `revision-invalid` (F11) |
| M41 | register rows shape | drop | survived (0, 0) | survived (0, 6) | survived | `rows` not a list → exit 2 (F5) |
| M42 | A4 cap + window (compound) | compound | killed (1, 2) | survived (0, 6) | killed | — |
| M43 | A2 pinned-path constant | value | killed (1, 16) | survived (0, 6) | killed | — |
| M44 | A2 sibling checks (compound) | compound | killed (1, 1) | survived (0, 6) | killed | — |

Totals: 44 mutants, 21 killed, 23 survived, 44/44 restored.

---

## 4. What the L1 should consider (not a contract change, a test change) [inf]

The checker itself behaves correctly on every probe I built; the gap is that
`tools/check-adjacency-overlap.py:selftest()` (cases list at lines 233-250) does not pin the 9 rule
behaviours listed in F1, whose removal would let a wrong register pass the C2 counter. The cheapest fix
is to extend the fixture, not the rule set: use `sibling_path = PIN_PATH` in one case (unlocks the
pinned-digest rule),
add a 26-word quote that *is* inside the window, add a missing lane file, add a half-filled lane side,
add a row whose sibling is not `mori`, add a PROVINCE row with the id in the second cell, add a
sibling repository whose pinned blob differs in bytes, and add the exit-2 cases (missing register,
invalid JSON, `rows` not a list, unresolvable revision).

---

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin (git cat-file / ls-tree / status, read-only), /fast/scratch/hyaku/tsuku27a2/MutC2Counter/tree (read-only export of 099c7b3f42d073203d9448807860f04c175eccd7), /home/vgpnk/Projects/shokunin/mori-shokunin (git cat-file -p at ef9dbee136d6ed2ef98687f5cb0c0a16506a5155, read-only); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/MutC2Counter.md and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/MutC2Counter/{mutants.json,mutate.py,probes.py,mutation-log.json,probe-log.json} plus /fast/scratch/hyaku/tsuku27a2/MutC2Counter/{pristine-check-adjacency-overlap.py,mut/*.py,tree/}; executed=git archive|git cat-file|git ls-tree|git status (read-only), python3 tools/check-adjacency-overlap.py --selftest and --revision 099c7b3f42d073203d9448807860f04c175eccd7 (44 mutants x 2 detectors, plus 16 fixture probes x pristine+mutants)
Model: minimax-code/MiniMax-M3.1-Flash
Installs: none
