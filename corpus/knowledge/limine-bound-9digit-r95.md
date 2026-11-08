# The accepted leg of a published numeric bound — Limine `--limine-version`, 1-9 digits per component

`source:` S389 (Python 3 docs, integer string conversion length limitation — opened 2026-11-08),
S382/S384 (Limine v12.9.5 `common/lib/config.c`, `host/limine.c`), S386/S387/S388 (Limine v12.9.6
`common/lib/config.c`, `ChangeLog`, `host/limine.c`), and this lane's own gate bytes
`tools/check-limine-pins.py` at the round-95 freeze (`7d79ac29…`).
`verified-at:` 2026-11-08 (round 95). `recheck:` on any change to `parse_limine_version`, to
`VISIBILITY_ERA_SPLIT`, or to the battery's `REFUSAL-VERSIONS-*` families.

## The rule this entry lands

A **published numeric bound** is a two-legged contract: the largest value **inside** it must be
ACCEPTED (and answered from), and the smallest value **outside** it must be REFUSED. A battery that
sends only the refused side certifies nothing about where the boundary is — a gate whose bound is
one digit too strict passes every refused-side case and is indistinguishable from a correct gate
(QUALITY 139).

The gate publishes exactly such a bound for `--limine-version`: three dot-separated ASCII-digit
components, 1-9 digits each (`tools/check-limine-pins.py:99`,
`len(parts) != 3 or not all(… and len(p) <= 9 …)`). A component longer than 9 digits is refused
rather than handed to `int()`, which raises above CPython's conversion limit (gate docstring, lines
92-95).

## Why 9 digits is a real program input, not a toy

CPython's decimal int↔str conversion limit is documented: "The default limit is 4300 digits as
provided in sys.int_info.default_max_str_digits." (S389, byte 785297) and "When an operation would
exceed the limit, a ValueError is raised:" (S389, byte 782228). On this host
(`python3 -c "import sys; print(sys.int_info.default_max_str_digits)"` → `4300`) the documented
failure is observable: `int("2"*4301)` raises `ValueError: Exceeds the limit (4300 digits) for
integer string conversion`. So an unbounded component is a program-crashing input, and a gate that
length-checks before `int()` is doing real work — which is why the bound's *accepted* side deserves
the same evidence as its refused side.

Scope note the source adds and this entry keeps: the CPython limit applies only to non-power-of-two
bases, and "Underscores and the sign are not counted towards the limit." (S389). The gate's 9-digit
cap is **the gate's own published contract**, not a consequence of CPython's 4300 — the entry does not
claim that nine digits is the right design.

## The two legs the lane now holds

| leg | family | sends | expected | what a bent gate shows |
|---|---|---|---|---|
| refused | `REFUSAL-VERSIONS` (r93), `REFUSAL-VERSIONS-10DIGIT` (r94) | 10 out-of-shape spellings + four ten-digit-component values (`1234567890.0.0`, …) | rc 64, empty stdout, no verdict | a `<= 10` bound (r94 N01/N03) reads `unmet` with the ten-digit family named |
| accepted | `REFUSAL-VERSIONS-9DIGIT` (r95) | `999999999.9.9` — a boundary member: the first component is 999,999,999 (the largest nine-digit value), the second and third are 9 | rc 1, `DEGRADED`, the LP-MISMATCH pin with consequence `panic`, `on_panic` as the fixture fixes it | a `<= 8` bound (`N05-strict-8`) refuses at rc 64 and reads `unmet` with the family named |

The accepted leg's fixture is era-sensitive on purpose: its first physical line is an entry label and
a `hash_mismatch_panic: no` line follows, so `999999999 ≥ (12, 9, 5)` (`VISIBILITY_ERA_SPLIT`,
`tools/check-limine-pins.py:104`, used at `:193`) selects era B, the label-end cut makes the key
invisible, and the gate must answer `panic`. A gate that accepts the value but reads era A answers
`prompt` and fails the family.

Evidence that the family bites: `tools/limine-pin-battery-r95.py` line 1694 declares
`REFUSAL_DIGIT9 = "9" * 9 + ".9.9"`; it was declared in r94 and referenced nowhere there
(`grep -c REFUSAL_DIGIT9` → **1** in `tools/limine-pin-battery-r94.py`, the declaration only), and
r95 references it three times (`grep -c REFUSAL_DIGIT9` → **3** in
`tools/limine-pin-battery-r95.py`: docstring `:29`, declaration `:1694`, the live use `:1715`).
Line 1707 defines `fam_refusal_versions_9digit`. Landed gate 99/99 `met` ×3 canonical and ×3 in a
`git clone --shared`; `N05-strict-8` 98/99 `unmet` ×3 in both layouts with `failed_families` exactly
`["REFUSAL-VERSIONS-9DIGIT"]`; the four N05 case rows carry `bad-output: JSONDecodeError rc=64` — the
bend's refusal, which is the expected error shape in that leg only.

## The blindness this closed

The r94 roster was **blind** to the over-strict bound: `do-nothing-battery-r94.py --gate
N05-strict-8 --runs 3` reads `met` **98/98** in every run, with 0 error rows and 0
`REFUSAL-VERSIONS-9DIGIT` rows in `case_log` — the before instrument cannot see the defect at all.
That is the difference the round buys: the same bend that was invisible is now named. The lane's own
gate is byte-unchanged this round (`7d79ac29…`, the same hash as the r94 control copy), so the gain
is measurement capability, not gate behaviour.

Mutation evidence (`w1/MutBound.md`): M01 (`<= 8`), M03 (bound kept, exact member rejected) and M07
(era forced to A above 1000) all die with `failed_families` exactly `["REFUSAL-VERSIONS-9DIGIT"]`;
M02 (`<= 10`) and M05 (no bound) die on the refused leg; M04 (`>` era split) dies on
`ERA-EXACT-125`. M06 (echo a wrong `limine_version`) SURVIVES — a coverage gap, recorded, not
papered over.

## Limits (declared, not claimed)

- **One boundary member.** The family sends the first component at the cap with Y and Z at 9. The
  cap admits `999999999.999999999.999999999`, which the gate accepts (rc 1, `DEGRADED`, era
  `12.9.5+`; `w1/ReviewBattery/boundary-probe.txt`), and the battery sends neither that value nor a
  9-digit Y or Z position: a bend of **Y's** bound to `<= 8` still reads `met` 99/99
  (`w1/ReviewBattery/middle-bound-probe.txt`). The per-component accepted boundary is Frontier work.
- **The era mechanism is unclaimed.** The battery's `got` tuple carries no `visibility_era`; a gate
  that clamps the era tuple but still answers the enforced `panic`/`prompt` pair reads `met`
  (`w1/ReviewBattery.md` F2). The observable is certified, the mechanism is not.
- **The echoed `limine_version` is recorded, not compared,** for explicit-version cases
  (`ReviewBattery` F3); `auto_ok` short-circuits when `c.auto is None`. M06 survives for this reason.
- **The extra-component probe answer is unsent.** The open `12.9.6.1` gap is the PROBE answer
  (`Limine 12.9.6.1`): `AUTO-PROBE-SHAPES` sends only `no version here` and `Limine 12.9.6-rc1`
  (battery `:1718`, `:1938`). The refusal roster does send `12.9.5.1` (battery `:1643`), so a
  "refusal-shape gap" wording would be stale.
- **The ten-digit leg's boundary member is not the smallest out-of-bound value.**
  `REFUSAL-VERSIONS-10DIGIT` sends `1234567890` (and the .0.0 variants), not `1000000000`;
  a mutant that accepted only values below 1000000000 would still pass (r94's `capvalue`
  counterexample, unchanged by r95).
- **The 1-9-digit cap is the gate's contract,** not upstream Limine's: S388 shows the binary prints
  `Limine %VERSION%` and says nothing about component widths.

## Related ground

- `limine-auto-default-r94.md` — `auto` became the default version source, and its probe refuses
  rather than defaulting.
- `limine-r92-oracle-isolation.md` — the battery runs each gate in a private copy under `bwrap`, so the
  number this entry cites is a result, not a borrowed answer.
