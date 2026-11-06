# MutBattery — battery self-test and answer-channel mutants (Tsukuroi r87, w1)

Seat: MutBattery (mutation-tester, leaf; no subagents).
Lane revision measured: `cefb4188b484329c4908a19a277f8fb120fb4f56` (`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`).
Instrument under test: `tools/limine-pin-battery-r87.py`, sha256 `f2551c8e8386d599e3c2aca8888d5fbb0351a5a399dc43dc448556e99361989d` == the freeze-manifest digest (measured in the clone).
Candidate gate: `tools/check-limine-pins.py`, sha256 `bbcc874ac8143ffb9bd97e4d3e2dfd934af3d6573f741d8b8ee3c00ecda9b73c` (read only; never modified).
No lane file was edited. All mutants live in a `git clone --shared` at `/fast/scratch/hyaku/tsukuroi-r87/MutBattery/lane` (`rev-parse --show-toplevel` verified); probes and receipts are in my wave dir. No host command was run; no `sudo`; `/boot` and `/efi` were never touched. No tool installed.

## 1. Baseline (pristine, both cwds)

```
$ cd /fast/scratch/hyaku/tsukuroi-r87/MutBattery/lane && python3 tools/limine-pin-battery-r87.py --selftest
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
reference-gate     PASS families_passed=22
selftest PASS 5/5        rc=0   (6.9 s)
$ cd /fast/scratch/hyaku/tsukuroi-r87/MutBattery/unrelated && python3 .../tools/limine-pin-battery-r87.py --selftest
... identical, selftest PASS 5/5  rc=0
```
The routed r86 defect 2 (cwd-dependent self-test) does not reproduce in the battery as committed: `ref` is resolved from `__file__` (`tools/limine-pin-battery-r87.py:569`) and the run chdirs to a temp work dir first. Both cwds read 5/5.

## 2. Nine battery mutants, `--selftest` from two cwds

Built by exact single-anchor replacements (`scratch-receipts/build_mutants.py`, anchors asserted to occur once); unified diffs in `scratch-receipts/mutants.diff`, sha256s in `sha256sums.txt`.

| # | mutation | selftest from clone lane root | selftest from unrelated cwd | verdict |
|---|---|---|---|---|
| M1 | comparison never true (`ok = False`) | FAIL 4/5 rc 1 (reference-gate 0/22) | FAIL 4/5 rc 1 | **killed** |
| M2 | comparison always true (`ok = True`) | FAIL 1/5 rc 1 (all four negatives read 22/22 met) | FAIL 1/5 rc 1 | **killed** |
| M3 | one family's expectation skipped (`MULTI-FAULT` always counted passed) | **PASS 5/5 rc 0** (negatives now print `families_passed=1`) | **PASS 5/5 rc 0** | **survived** |
| M4 | family set shrunk to 21 (`HOST-SHAPE` removed) | **PASS 5/5 rc 0** (`reference-gate ... families_passed=21`) | **PASS 5/5 rc 0** | **survived** |
| M5 | ignores rc (neither process exit code nor `out["rc"]` compared) | **PASS 5/5 rc 0** | **PASS 5/5 rc 0** | **survived** |
| M6 | ignores consequence (pins compared as `(line,status)`) | **PASS 5/5 rc 0** | **PASS 5/5 rc 0** | **survived** |
| M7 | ignores line numbers (pins compared as `(status,consequence)`) | **PASS 5/5 rc 0** | **PASS 5/5 rc 0** | **survived** |
| M8 | reference path from the invocation cwd, captured at import | PASS 5/5 rc 0 (looks green in the usual invocation) | **FAIL 4/5 rc 1** `missing .../unrelated/.ufo/waves/round-87/before/controls/ref-gate-r87.py` | **killed only by the unrelated cwd** |
| M8b | reference path from cwd at resolve time | FAIL 4/5 rc 1 | FAIL 4/5 rc 1 (selftest chdirs before resolving) | **killed** |

Killed: 2 of 9 outright (M1, M2), 2 conditionally (M8 only from an unrelated cwd; M8b always). Survived: 5 of 9 (M3–M7). Every surviving mutant still reads 22/22 `met` against the *correct* candidate gate (see §3, `realgate-matrix.txt`), because a correct gate exercises none of the broken fields.

## 3. The survivors are real defects: one-field lie gates

Three probes wrap the committed reference gate and bend exactly one output field (`probes`, `probe-matrix.txt`). Each probe is a gate that is demonstrably wrong in one field and correct in all others.

| probe gate (bent field) | pristine battery | M5 / M6 / M7 battery |
|---|---|---|
| `rclie-lie.py` (correct verdict+pins, `rc=0`, exit 0) | 4/22 unmet rc 1 | **M5: 22/22 met rc 0** |
| `conslie-lie.py` (all consequences forced `none`) | 5/22 unmet rc 1 | **M6: 22/22 met rc 0** |
| `lineshift-lie.py` (every pin `line + 1`) | 1/22 unmet rc 1 | **M7: 22/22 met rc 0** |

So the surviving mutants are not cosmetic: `--selftest` has no control whose only defect is the exit code, the consequence, or the line number, and it cannot see a skipped family or a one-family-short roster.

## 4. Answer channel: `met` is self-referential

Counting command, 1 run per battery (`realgate-matrix.txt`), candidate gate, cwd clone lane root:

```
pristine              rc=0  families_passed 22/22 verdict met failed -
m4-families-21        rc=0  families_passed 21/21 verdict met failed -     <-- shrunken roster reads met
m3-family-skipped     rc=0  families_passed 22/22 verdict met failed -     <-- one family unchecked
m5-ignore-rc          rc=0  families_passed 22/22 verdict met failed -
m6-ignore-consequence rc=0  families_passed 22/22 verdict met failed -
m7-ignore-line        rc=0  families_passed 22/22 verdict met failed -
m8-ref-from-cwd       rc=0  families_passed 22/22 verdict met failed -
m1-never-met          rc=1  families_passed 0/22 verdict unmet failed <all>
m2-always-met         rc=0  families_passed 22/22 verdict met failed -
```

`met = len(passed) == len(FAMILIES)` and `families_total: len(FAMILIES)` (`tools/limine-pin-battery-r87.py:537,539`): the denominator is whatever the file says, so the counting command cannot distinguish 21/21-met from 22/22-met. The target `22` exists only in the docstring and receipt; the only guard against an edited battery is the external sha256 check against `.ufo/waves/round-87/before/freeze-manifest.sha256` (the void rule), not the instrument itself. This is not a predicate violation as frozen (bytes-differ ⇒ void), but it means the counting command alone does not authenticate the instrument, and the `--selftest` smoke test does not either.

## 5. Fixture answer leak (no BLAKE2b anywhere)

`probes/leak-gate.py` parses R1/R4/R6/R7 faithfully but decides OK vs LP-MISMATCH from fixture shape only. It never computes BLAKE2b (LEAK=sha uses SHA-256 only as a filename oracle). Against the pristine battery (`leak-matrix.txt`):

| mode | families passed | passed families |
|---|---|---|
| `LEAK=upper` | 3/22 unmet rc 1 | `HASH-UPPER` (uppercase hex ⇒ OK), `PANIC-FIRST` (its only pin is a mismatch), `MALFORMED-INPUT` (rc 2) |
| `LEAK=uuid` | 4/22 unmet rc 1 | + `POSITIVE` (`cmdline: quiet root=UUID=` occurs only in `fam_positive`, `:204`) |
| `LEAK=sha` | 5/22 unmet rc 1 | + `HOST-SHAPE` (`omarchy_linux.efi_sha256_<hex>` history names at `:442` carry SHA-256 of the content, used as an OK oracle) |

No shape-only gate exceeds 5/22, so the 22/22 target is not reachable without a content compare (the remaining 17 families need at least one true OK over random bytes). But the docstring sentence "Fixtures carry no answer: random file and directory names" (`:53`) is false for `HOST-SHAPE`: those names carry a digest of the file content, and a name-trusting gate gets three OK pins for free. `HASH-UPPER` likewise certifies nothing about hashing if "uppercase ⇒ OK" is accepted, and `POSITIVE` is passable by any text marker unique to it.

## 6. Reference-delegating forger (answer on disk)

A candidate-shaped gate with no R1–R7 code that execs `.ufo/waves/round-87/before/controls/ref-gate-r87.py` resolved from its own path reads:

```
$ python3 tools/limine-pin-battery-r87.py --gate tools/check-limine-pins-delegate.py
families_passed 22/22 verdict met failed -        rc=0
```

The battery cannot tell an implementation from a delegation, because its positive control *is* that file. Mitigation tested (`delegate-mitigation.txt`): in a lane copy with `controls/ref-gate-r87.py` removed, the delegate reads `0/22 unmet rc=1` and the real candidate still reads `22/22 met rc=0`. Proposal: run the counting command against a copy without the committed reference gate (or rely on the L1 byte review that the candidate shares no code with it, as the controls receipt already states).

## 7. Defects and proposed patches (report-only; L1 decides)

**D1 — answer channel is self-referential; roster and per-field checks missing.**
`tools/limine-pin-battery-r87.py:537,539` compute `met` from `len(FAMILIES)` in the same bytes; `SELFTEST_GATES` (`:544`) holds only absent/constant/non-JSON gates and never asserts a family or a field. Proposed patch:
1. Freeze a literal roster and size:
```python
FAMILY_NAMES = frozenset("""POSITIVE MISMATCH-EARLY MISMATCH-LATE MISSING HASH-LENGTH HASH-NONHEX
    HASH-UPPER COMMENT-DECOY KEY-CASE WHITESPACE-CRLF LAST-HASH GZ-RAW UNRESOLVED PANIC-DEFAULT
    PANIC-NO-ONLY PANIC-FIRST SECUREBOOT OPTIONAL-SKIP MULTI-FAULT UNHASHED-DECOYS
    MALFORMED-INPUT HOST-SHAPE""".split())
if set(FAMILIES) != FAMILY_NAMES:
    raise SystemExit("family roster drift")
met = len(passed) == len(FAMILIES) == 22
```
2. In `selftest()` add three generated lie-controls (wrappers around the resolved reference gate: rc forced 0; all consequences forced `none`; every line +1) and one committed near-miss (`REF_DROP=first-fault-only`), and assert **the named family** is in `failed_families`, not merely that the run is unmet.
Prototype `scratch-receipts/improved_selftest.py` (runs these four probes against any battery via its own `run_battery`):
```
pristine              improved-selftest PASS 5/5
m3-family-skipped     FAIL (refdrop-first-fault-only: MULTI-FAULT not in failed)
m4-families-21        FAIL (family-roster-22: 21)
m5-ignore-rc          FAIL (rc-lie: 22/22 met)
m6-ignore-consequence FAIL (consequence-lie: 22/22 met)
m7-ignore-line        FAIL (line-shift: 22/22 met)
```
`improved-selftest-matrix.txt`. This kills all five survivors at no cost to the pristine battery.

**D2 — fixture shape correlates with the expected answer.**
`:204` (`root=UUID=` only in POSITIVE), `:250` (`fam_hash_upper`: every pin is OK, so case alone is a status signal), `:442` (`fam_host_shape`: `_sha256_<digest>` names carry the content digest). Proposed patch (tested, `p3-fixture-patch.txt`): add one uppercase-hash *mismatch* pin to `fam_hash_upper`; make one history name digest stale (name built from different bytes than the file, pin correct for the stored bytes). Effect:
```
ref gate      22/22 met rc=0        candidate gate 22/22 met rc=0
leak=upper    3/22 -> 2/22 unmet    leak=sha       5/22 -> 3/22 unmet
```
So the two families stop certifying "hashes stored bytes" to a gate that trusts case or file names. POSITIVE remains passable by any all-OK gate by construction; it must not be cited as a hashing family.

**D3 — battery cannot detect delegation.** Covered in §6; mitigation is a counting run in a tree without the committed reference gate, evidence above, plus the L1 byte review.

## 8. Refusals and unrun

- No host read or write; no `sudo`; `/boot`, `/efi`, `/sys`, `/proc` untouched; no `objcopy`/`limine`/`bootctl`/`pacman`. Host facts are taken from the committed receipts only. I did not need an additional host fact.
- Did not run the 3× counting command at the tip and did not judge C1 met/unmet (L1's gate).
- Did not edit the lane, MANIFEST.json, `.ufo/state/`, sibling lanes, or anything outside my wave dir and scratch. No tool installed (none needed).
- Scratch `/fast/scratch/hyaku/tsukuroi-r87/MutBattery` removed after copying receipts.

## 9. Receipts

`scratch-receipts/`: `selftest-matrix.txt` (all 18 mutant runs + pristine), `realgate-matrix.txt`, `probe-matrix.txt`, `leak-matrix.txt`, `improved-selftest-matrix.txt`, `p3-fixture-patch.txt`, `delegate-forger.txt`, `delegate-mitigation.txt`, `mutants.diff`, `sha256sums.txt`, and the generators (`build_mutants.py`, `improved_selftest.py`, `patch_fixtures.py`, `leak-gate.py`, `forger-delegate.py`).
