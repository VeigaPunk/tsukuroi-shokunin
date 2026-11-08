# Review of the landed corpus draft `corpus/knowledge/limine-metadata-cap-families-r99.md`

Seat: ScribeKnowledge (scribe, leaf member; no dispatch). Scope: draft the round's knowledge entry
(the entry itself is in this seat dir, `limine-metadata-cap-families-r99.md`); this file records
what the **landed** corpus draft already says and where it needs narrowing. The corpus file is the
L1's; nothing under `corpus/` was edited by this seat.

The landed draft is at `corpus/knowledge/limine-metadata-cap-families-r99.md` (untracked in the
working tree at the time of this review; `git status --porcelain` → `?? corpus/knowledge/
limine-metadata-cap-families-r99.md`). Its header trio is at column 0 on lines 1-3:

```
source: corpus/SOURCES.md S395 (own-work, the r99 battery's assertion sites) + S392 (...)
verified-at: 2026-11-08
recheck: 180d
```

## F1 — a cited receipt does not exist in the tree (R98-RECEIPT-NAME-MISMATCH class)

Section 3 cites `.ufo/waves/round-99/before/dev/c1-N10-twin-r98-control.json` for the dropped
`N10-z-echo` bend's r98-control reading, and `corpus/lessons/round-99.md` cites the same path.

Sweep (the command that shows the absence):

```
$ find .ufo/waves/round-99 -name "*N10*"
(no output)
$ ls .ufo/waves/round-99/before/dev/ | grep -i n10
(no output)
```

The plan names a third spelling, `before/dev/c1-N10-twin-r98.json` (`.ufo/plans/round-99.md:77`);
that path is absent too. The whole `before/dev/` directory holds 30 files and none of them is an
N10 receipt:

```
$ ls .ufo/waves/round-99/before/dev/ | wc -l
30
$ ls .ufo/waves/round-99/before/dev/ | grep -c '^c1-'
14
```

Consequence: the twin's reading (`unmet 104/105` on the r98 control) is asserted in two landed
files with no receipt behind it. The reading is plausible — the r98 battery already sets
`check_echo` on the Z family (`tools/limine-pin-battery-r99.py` BYTE 83173), so a Z-echo lie would
name that family — but it is not measured in this tree, and this seat did not re-derive it. Either
the receipt lands under its real name, or the sentence is marked as the plan's recorded reading
rather than a measured one.

## F2 — the blanket lie kinds' `unmet` reading is not only the field assertion

Section 4's table reports the two new lie kinds as `unmet 93/105` and `unmet 95/105` with the cap
families named. That is the right number, but the sentence "Each wraps the reference gate and
falsifies one field of its answer" reads as if every failing family failed **because of the
falsified field**. Measured on the L1's own receipts
(`.ufo/waves/round-99/before/dev/c1-lie-limine-version.json`,
`.ufo/waves/round-99/before/dev/c1-lie-visibility-era.json`), the failing families split in two:

| lie kind | failing families caused by the falsified field | failing families caused by the wrapper's own refusal-path breakage |
|---|---|---|
| `limine-version` | 7 — AUTO-ERA-A, AUTO-ERA-B, EXPLICIT-VERSION-ECHO, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT, REFUSAL-VERSIONS-9DIGIT-Y, REFUSAL-VERSIONS-9DIGIT-Z | 5 — AUTO-PROBE-FAIL, AUTO-PROBE-SHAPES, EXTRA-COMPONENT, REFUSAL-VERSIONS, REFUSAL-VERSIONS-10DIGIT |
| `visibility-era` | 5 — EXPLICIT-VERSION-ERA, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT, REFUSAL-VERSIONS-9DIGIT-Y, REFUSAL-VERSIONS-9DIGIT-Z | 5 — the same five |

The five wrapper-side failures are mechanical, not semantic: the wrapper does
`out = json.loads(p.stdout)` before it can falsify a field, and a refusal answers rc 64 with an
**empty** stdout, so `json.loads("")` raises and the wrapper exits 1 — the refusal family sees
`rc 1`, not `rc 64` (the failing rows read `{"version": "12.9", "rc": 1, "stdout_bytes": 0,
"ok": false}` against a landed-gate row `{"version": "12.9", "rc": 64, "stdout_bytes": 0,
"ok": true}`). This seat measured that decomposition directly, on its own re-run of the same two lie kinds
against the pinned battery's own `LIE_WRAPPER` template
(`.ufo/waves/round-99/w1/ScribeKnowledge/receipts/14-lie-composition-own.txt`,
`receipts/c1-lie-limine-version-r99.json`, `receipts/c1-lie-visibility-era-r99.json`); the split
is identical in all three runs of each kind. The earlier decomposition over the L1's receipts is
kept as `receipts/05-lie-kind-composition.txt`.

So the lie kind certifies two things and one non-thing:

- it certifies the battery **sees** the falsified field (the field-caused column above);
- it certifies the selftest now has a per-field adversary (the `LIE_KINDS` tuple grew 12 → 14);
- it does **not** certify that all 12 failing families were asserting that field.

## F3 — the `recheck:` line carries no procedure

`recheck: 180d` is a cadence, which `tools/check-knowledge-header.py` accepts, but it names no
command. The predecessor entry (`corpus/knowledge/limine-metadata-assertions-r98.md`) carried a
runnable procedure on that line, and `tools/check-recheck-commands.py` reads the **last** `recheck:`
line as a procedure another agent is invited to follow. This seat's draft carries the procedure.

## F4 — the `source:` line does not carry the gate's byte offsets

`source:` cites S395 (the battery's assertion sites) and S392 (CPython `int()`), which is right for
the battery, but the entry's first proposition is about the **gate's** two emission sites and the
entry does not anchor them in the header. The gate's own row (S394) carries them; the seat's draft
repeats them in `source:` so the header stands alone.

## F5 — the draft's "three committed one-clause bends" heading counts a bend that was dropped

Section 3's heading says "three committed one-clause bends", and its third row is marked
"(dropped)". Two bends are committed
(`.ufo/waves/round-99/before/controls/bends/N09-y-era.py`, `N11-x-era.py`; sweep:
`ls .ufo/waves/round-99/before/controls/bends/` → two files). The seat's draft says "two
committed bends, and the one that was dropped".

## F6 — the era-from-the-whole-tuple sentence is true but the entry does not say what "whole" costs

Section 1 says the era follows "the whole numeric tuple". That is right, and the r98 entry already
carried the counter-example (`12.000000009.000000005` is era B under `int()` but era A under a text
comparison). The seat's draft restates it with the measured spelling list, because the accepted-cap
families are exactly the families whose tuples put the cap in a component other than the first:
`999999999.9.9` (era B), `12.999999999.4` (era B), `0.999999999.0` (era A) — the Y family is the
one where an era reader that looks at the first component alone answers correctly for both
members, which is why the Y family's era assertion needs the Y-cap *spellings*, not the X-cap one.

## What the landed draft gets right (and this seat keeps)

- Both emission sites of both fields, with byte offsets (verified independently: 16931 / 17037 at
  the MAIN return, 11230 / 11344 at the CANNOT-EVALUATE early return — receipt 01).
- The third `visibility_era` occurrence at BYTE 19205 (line 361) is the gate's own selftest
  expectation, not an emission site (measured, receipt 01).
- The rule "a family certifies a reported field only if it reads that field on its own cases", and
  the r98 G6 measurement that made the rule necessary.
- The X-leg honesty: N11 is a **delta** closure (one additional failed family), not a flip.
- The twin-bend lesson (a bend the do-nothing instrument already kills witnesses the predecessor).
- The Limits section naming the uncertified echo legs and the unchanged roster.
