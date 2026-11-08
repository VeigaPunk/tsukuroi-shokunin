# ScribeLesson — criterion 132 redraft + round-92 M2 row (round 92, wave w1)

Measured at lane rev `689623fdf592a92b6de85f9869da6f264ad9ce4d` (HEAD when this seat wrote).
Lane read-only: this seat edited **no** lane file except its own seat report and
`.ufo/waves/round-92/w1/ScribeLesson/` (receipts). No `git`/`jj` mutation was run in the lane.
Scratch: `/fast/scratch/hyaku/tsukuroi-r92/ScribeLesson/`, removed on exit.

Receipts: `.ufo/waves/round-92/w1/ScribeLesson/receipts/`
(`01-number-check.txt`, `02-pointer-resolution.txt`, `03-m2-verdict-misstatement.txt`,
`04-byte-offsets.txt`).

---

## 1. Number check — 132 is TAKEN; next free number is 136

```
$ grep -cE '^[0-9]+\. \*\*' corpus/QUALITY.md
117
$ grep -oE '^[0-9]+\.' corpus/QUALITY.md | tr -d '.' | sort -n | uniq | awk 'NR!=$1{print "GAP";g=1} END{if(!g) print "contiguous 1.."NR}'
contiguous 1..135
$ grep -oE '^[0-9]+\.' corpus/QUALITY.md | tr -d '.' | sort -n | uniq -d
(no output — no duplicate numbers)
$ grep -cE '^136\.' corpus/QUALITY.md
0
```

**The seat brief's premise is stale.** The r91 wave's proposed criterion 132 was *already
drafted and landed* while this seat was running:

| number | tag | landed |
|---|---|---|
| 132 | `R92-JUDGE-ORACLE-IMPORTABLE` | `495a9f6c` ("round-92: control repair (A1, BATT=find_oracle), QUALITY 132-133 …") |
| 133 | `R92-CONTROL-DEAD-IN-BOTH-STATES` | `495a9f6c` |
| 134 | `R92-CONTROL-WILDCARD-TARGET` | `429fd1a3` ("A2 control repair (K4 frozen-name resolution)") |
| 135 | `R92-ENV-DUMP-CREDENTIAL` | `689623fd` (A3; worktree) |

So **132 is taken** and the next free number is **136**. The criterion 132 the seat was asked
to draft exists at `corpus/QUALITY.md:324` (bytes 126235..128342) in the house shape the brief
asked for — bold title with tag, red, green, shown-able-to-fail, and a `Lesson:` line. The
redraft below is therefore a **review of the landed text**, not a proposal of a new number.

---

## 2. The criterion as landed — review

`corpus/QUALITY.md:324-325`, bytes 126235..128342 (2108 bytes):

> **132. A judge's oracle is unreachable from the subject it judges, and every read channel has a
> control that would score the target through it (R92-JUDGE-ORACLE-IMPORTABLE):** when an instrument
> runs a subject that could import the instrument's own expected-answer code (same directory on
> `sys.path`, a sibling file, an absolute path, the parent's `/proc`, an environment variable), the
> run must place the subject somewhere that code is not (a private copy outside the tree, `python3 -I`,
> a mount/PID namespace, a cleared environment), and the freeze must carry one control per channel
> that reads the target when that channel leaks and a wrong-but-valid verdict when it does not — a
> control that crashes counts as an `error:` row, never as rejection (QUALITY 126). **Red:** the r91
> battery launched `[sys.executable, gate, ...]`, so a `tools/`-resident gate had the battery's
> directory as `sys.path[0]`; the wave's `sibling-oracle-forgery.py`, which models none of
> R6/R9/R10/V1/U1, read `82/82 verdict met` rc 0 (`2d7e09e1:tools/limine-pin-battery-r91.py:1635`,
> `.ufo/waves/round-91/w1/ScribeLesson/receipts/channel-open.json`). **Green, round 92:**
> `tools/limine-pin-battery-r92.py` copies the gate into an empty directory and runs it under `bwrap
> --unshare-all --clearenv --die-with-parent --new-session` with only `/usr`, `/etc`, fresh
> `/dev`/`/proc`/`/tmp`, the case directory and the copy mounted, plus `python3 -I`; the same five
> controls read `0/89 unmet` with 0 error rows while the landed gate reads `89/89 met`
> (`.ufo/waves/round-92/after/c1-controls/`). **Shown able to fail:** the controls read `82/82 met`
> against the unchanged r91 battery in the same clone layout, and `--isolation-check` prints what a
> probe actually sees (`lane_visible: false`, `sibling_files: ["gate.py"]`, PIDs `1,2`). A channel the
> sandbox cannot close (behaviour, timing) is named uncertified in the round's limits, never claimed.
>
> Lesson: `corpus/lessons/round-92.md` Mistakes `M2`; extends QUALITY 129 (channels the instrument
> hands the subject) with the subject importing the judge; QUALITY 126 governs the error-row accounting.

**Shape check against the brief — all four required parts are present:**

| brief requirement | landed? |
|---|---|
| bold title with the tag | yes — `**A judge's oracle is unreachable … (R92-JUDGE-ORACLE-IMPORTABLE):**` |
| red: what went wrong, with the measured r91 evidence | yes — r91 battery argv, the forgery's `82/82 verdict met` rc 0, two cited receipts |
| green: the rule as an executable requirement | yes — "the run must place the subject somewhere that code is not (a private copy outside the tree, `python3 -I`, a mount/PID namespace, a cleared environment)" |
| shown able to fail, from the r92 before/after receipts | yes — `82/82 met` (r91 battery) vs `0/89 unmet` (r92 battery), plus the `--isolation-check` probe output |
| precise about what a launcher must close **and what it cannot** | yes — "A channel the sandbox cannot close (behaviour, timing) is named uncertified in the round's limits, never claimed" |
| cites `corpus/lessons/round-92.md` | yes — `Lesson:` line, bytes 128143..128341 |

**The claim's own numbers verify against the committed receipts** (`receipts/` + inline checks):

- r91 battery + the five controls → `82/82 met` — `.ufo/waves/round-92/after/c1-controls/before-clone/summary.tsv`
  reads `K3/K5/K6/K7 … 82,82,82 met`; `before-clone-fixed/summary.tsv` reads `K4-syspath … 82,82,82 met`
  (A2 repaired bytes `efb53f76…`). ✔
- r92 battery + the same five controls → `0/89 unmet`, 0 error rows — `after-clone/summary.tsv` and
  `canonical-after/summary.tsv` both read `0,0,0 unmet,errors 0` for all five. ✔
- the landed gate → `89/89 met` — `gate-canonical.txt` and `gate-clone.txt` each read three
  `families_passed 89/89 verdict met`. ✔
- `--isolation-check` → `lane_visible: false`, `sibling_files: ["gate.py"]`, `pids ["1","2"]` —
  `isolation-check.json` reads exactly those. ✔
- red-leg anchors: `2d7e09e1:tools/limine-pin-battery-r91.py:1635` reads
  `argv = [sys.executable, gate, "--conf", conf, "--esp", esp]`; `channel-open.json`'s `gate` is
  `oracle-channel-control.py` at `82/82 met`. ✔

**One pointer defect in the red leg.** The red leg cites
`.ufo/waves/round-91/w1/ScribeLesson/receipts/channel-open.json` for the **sibling-oracle
forgery**'s `82/82 verdict met`. That file's `gate` field is `oracle-channel-control.py`, not
`sibling-oracle-forgery.py` — it is the *control's* receipt, not the forgery's. The forgery's own
`82/82 met` measurement is in `receipts/commands.txt` (block **B1**) and in the r91 seat report
`.ufo/waves/round-91/w1/ScribeLesson.md:47-48,104-105`; the forgery *source* is committed at
`.ufo/waves/round-91/w1/ScribeLesson/receipts/sibling-oracle-forgery.py`. The cited path resolves
and carries the right number, but it is the receipt of a different subject — the same
"pointer names a receipt for something else" shape as the round's own M2 defect (§4).

**The `Lesson:` line is mis-anchored.** It cites round-92 Mistakes `M2`, but M2 is the
lie-wrapper/vacuous class, not the judge-oracle-import class. The class criterion 132 captures was
mined in **round 91** as `R91-JUDGE-ORACLE-IMPORTABLE`
(`corpus/lessons/round-91.md:29`, "**M1 (ScribeLesson, routed): `R91-JUDGE-ORACLE-IMPORTABLE`**").
Round-92's M2 is a different defect (the `--selftest` lie wrapper). The anchor should be
`corpus/lessons/round-91.md` Mistakes `M1`; the round-92 anchor that fits is **M3/M4**, which are
the round-92 rows that carry the class's own refinements. *(The `Lesson:` line is the last line of
the criterion paragraph; M3/M4 are the rows whose content the criterion's "shown able to fail"
leg now rests on.)*

---

## 3. Drafted criterion 132 (house shape, with the two corrections folded in)

This is the text the L1 should carry. It is the landed 132 with **two** changes, both marked
`⟨edit⟩`; everything else is byte-for-byte the landed text.

```markdown
132. **A judge's oracle is unreachable from the subject it judges, and every read channel has a control that would score the target through it (R92-JUDGE-ORACLE-IMPORTABLE):** when an instrument runs a subject that could import the instrument's own expected-answer code (same directory on `sys.path`, a sibling file, an absolute path, the parent's `/proc`, an environment variable), the run must place the subject somewhere that code is not (a private copy outside the tree, `python3 -I`, a mount/PID namespace, a cleared environment), and the freeze must carry one control per channel that reads the target when that channel leaks and a wrong-but-valid verdict when it does not — a control that crashes counts as an `error:` row, never as rejection (QUALITY 126). Red: the r91 battery launched `[sys.executable, gate, ...]`, so a `tools/`-resident gate had the battery's directory as `sys.path[0]`; the wave's `sibling-oracle-forgery.py`, which models none of R6/R9/R10/V1/U1, read `82/82 verdict met` rc 0 (`2d7e09e1:tools/limine-pin-battery-r91.py:1635`, `.ufo/waves/round-91/w1/ScribeLesson/receipts/commands.txt` block B1). ⟨edit 1: the landed text cited `…/receipts/channel-open.json`, whose `gate` is `oracle-channel-control.py`, not the forgery; the forgery's own measurement is `commands.txt` B1 and the r91 seat report `:47-48`.⟩ Green, round 92: `tools/limine-pin-battery-r92.py` copies the gate into an empty directory and runs it under `bwrap --unshare-all --clearenv --die-with-parent --new-session` with only `/usr`, `/etc`, fresh `/dev`/`/proc`/`/tmp`, the case directory and the copy mounted, plus `python3 -I`; the same five controls read `0/89 unmet` with 0 error rows while the landed gate reads `89/89 met` (`.ufo/waves/round-92/after/c1-controls/`). Shown able to fail: the controls read `82/82 met` against the unchanged r91 battery in the same clone layout (`.ufo/waves/round-92/after/c1-controls/before-clone/summary.tsv` for K3/K5/K6/K7 and `…/before-clone-fixed/summary.tsv` for K4), and `--isolation-check` prints what a probe actually sees (`lane_visible: false`, `sibling_files: ["gate.py"]`, PIDs `1,2`). A channel the sandbox cannot close (behaviour, timing) is named uncertified in the round's limits, never claimed.
Lesson: `corpus/lessons/round-91.md` Mistakes `M1`; extends QUALITY 129 (channels the instrument hands the subject) with the subject importing the judge; QUALITY 126 governs the error-row accounting.
```

**Edit 1 — the red-leg receipt pointer.** `channel-open.json` → `commands.txt` block B1 (the
forgery's own `82/82 verdict met` rc 0). `commands.txt` is committed at
`.ufo/waves/round-91/w1/ScribeLesson/receipts/commands.txt` and its B1 block reads verbatim
`families_passed 82/82 verdict met failed - / rc=0`.

**Edit 2 — the `Lesson:` anchor.** `round-92.md` Mistakes `M2` → `round-91.md` Mistakes `M1`.
The class was *mined* in round 91 (`R91-JUDGE-ORACLE-IMPORTABLE`, `corpus/lessons/round-91.md:29`);
round-92's M2 is a different defect. The round-92 rows that refine the class are M3 (dead controls
in both legs → QUALITY 133) and M4 (wildcard target resolution → QUALITY 134), and those are
already anchored by criteria 133 and 134 respectively.

**Also worth the L1's attention (not a change this seat asks for):** the green leg's parenthetical
points at the *directory* `.ufo/waves/round-92/after/c1-controls/`. That directory now holds six
leg sets, including the A2 `-fixed/` ones; naming the two `before-clone*` files explicitly (as
drafted above) removes the ambiguity of which receipt supports "82/82 met".

---

## 4. Round-92 `## Mistakes` row for M2 — the required shape, and what it says

### Vocabulary check (`CORPUS.md` §"A round lesson that mines mistakes carries `## Mistakes`")

> One row per mistake: class · evidence pointer · captured-by (the `QUALITY.md` criterion or protocol
> rule that should have caught it, or `none`) · fix. Classes come from the `mistakes.md` §5 vocabulary
> (`vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`,
> `attribution`, `landing`, `provider`).

The landed M2 row's class is `vacuous` — **in the vocabulary** ✔. Its `captured-by` is
`QUALITY 126 (R88-CONTROL-PASSED-BY-CRASH)` — a real criterion ✔. Its shape is
class · evidence pointer · captured-by · fix ✔. **The row's structure is right; two of its content
fields are not.**

### The two content defects (both measured)

**(a) Both evidence pointers name paths that never existed in any commit.**

```
$ git log --all --oneline -- '.ufo/waves/round-92/before/controls/m2-lie-wrapper-path.py' \
    '.ufo/waves/round-92/after/m2-lie-wrapper-check.txt' '.ufo/waves/round-92/after/m1-landing-check.txt'
(no output — never existed in any commit)
```

The files that DO carry the M2 evidence, all committed:

```
$ git ls-files .ufo/waves/round-92/after/m2/ .ufo/waves/round-92/before/controls/m2-evidence.py
.ufo/waves/round-92/after/m2/drafted-path-form.json
.ufo/waves/round-92/after/m2/landed-embedded-form.json
.ufo/waves/round-92/after/m2/lie-consequence-embedded.py
.ufo/waves/round-92/after/m2/lie-consequence-path.py
.ufo/waves/round-92/after/m2/m2-summary.json
.ufo/waves/round-92/before/controls/m2-evidence.py
```

A full sweep of every backticked path in the round-92 lesson
(`receipts/02-pointer-resolution.txt`) finds three MISSING paths and six OK ones:

| path | status |
|---|---|
| `.ufo/waves/round-92/before/controls/m2-lie-wrapper-path.py` (M2) | **MISSING** |
| `.ufo/waves/round-92/after/m2-lie-wrapper-check.txt` (M2) | **MISSING** |
| `.ufo/waves/round-92/after/m1-landing-check.txt` (M1) | **MISSING** |
| the other six backticked paths in the lesson | OK |

**(b) The row's "reads `met`" contradicts the receipt it points at.**

```
$ python3 -c "import json;d=json.load(open('.ufo/waves/round-92/after/m2/m2-summary.json'));…"
drafted-path-form   families 0  / 89 unmet error_rows 356 verdict_rows 0
landed-embedded-form families 74 / 89 unmet error_rows 0   verdict_rows 356
reading: the path form reaches `unmet` only through error rows (its child cannot exec an
         unmounted reference); the embedded form reaches `unmet` through verdict rows that lie in
         exactly one field
```

The landed M2 row says "the path form yields `error` rows and reads `unmet` on the POSITIVE
reference leg, the embedded form yields verdict rows and reads `met`". The receipt's own `reading`
field says the embedded form reaches **`unmet`** through verdict rows (74/89 — the lie is caught on
exactly the families that check the lied field). The two-leg contrast the row wants (356 error rows
vs 356 verdict rows) **is** in the receipt; only the verdict word is wrong. The row's claim that
the embedded form reads `met` would mean the lie went undetected — the opposite of what the fix
does.

### The row, as it should stand

```markdown
- **M2 (`vacuous`, self-found before filing) — a lying-control wrapper exec'd the reference gate by
  PATH, which the round's own isolation turns into a crash.** Class: `vacuous`. The battery's
  `--selftest` lie legs (`LIE_KINDS`) wrap the reference gate by running it; the first draft passed
  the child the reference's absolute path, so under the r92 launcher the wrapper's child could not
  see it, every leg would have read `unmet` from `error:` rows, and the selftest would have been
  green for the wrong reason. Evidence pointer: `.ufo/waves/round-92/after/m2/lie-consequence-path.py`
  (the drafted path form, emitted by `.ufo/waves/round-92/before/controls/m2-evidence.py`) against
  the landed `LIE_WRAPPER` (embeds `GATE_SRC`, writes it to the sandbox's `/tmp`); the measured
  contrast is `.ufo/waves/round-92/after/m2/m2-summary.json` (per-form receipts
  `drafted-path-form.json`, `landed-embedded-form.json`). Captured-by: QUALITY 126
  (`R88-CONTROL-PASSED-BY-CRASH`). Fix: the wrapper carries the reference's bytes, and the fix is
  shown able to fail — the path form reaches `unmet` only through 356 `error:` rows (0 verdict
  rows), the embedded form reaches `unmet` through 356 verdict rows and 0 error rows at 74/89,
  because the lie is caught on exactly the families that check the lied field
  (`.ufo/waves/round-92/after/m2/m2-summary.json`).
```

Changes from the landed row, all three in the content fields:

1. **Evidence pointer** — `.ufo/waves/round-92/before/controls/m2-lie-wrapper-path.py` →
   `.ufo/waves/round-92/after/m2/lie-consequence-path.py` (emitted by
   `.ufo/waves/round-92/before/controls/m2-evidence.py`), and
   `.ufo/waves/round-92/after/m2-lie-wrapper-check.txt` → `.ufo/waves/round-92/after/m2/m2-summary.json`
   with its two per-form receipts named.
2. **The verdict word** — "the embedded form yields verdict rows and reads `met`" → "reaches `unmet`
   through 356 verdict rows and 0 error rows at 74/89". The "POSITIVE reference leg" phrase is also
   dropped: the `m2` receipts measure the two wrapper forms as **gates the battery scores**, not the
   selftest's positive reference leg, and no committed receipt of the `--selftest` legs exists
   (`ExecLints/battery-selftest.log` is 0 bytes; the battery's `--selftest` was not run to a
   committed receipt in this round).
3. **"the first draft embedded the reference's absolute path"** → "the first draft **passed the
   child** the reference's absolute path". The landed `LIE_WRAPPER` embeds the *bytes*
   (`GATE_SRC`, written to the sandbox's `/tmp`); the draft handed over the *path*
   (`PATH_WRAPPER` → `subprocess.run([sys.executable, <abs path>])`,
   `.ufo/waves/round-92/before/controls/m2-evidence.py:37-38,52`). The landed row's own sentence
   uses "embedded" for both — for the draft's path and for the landed wrapper's bytes — so the
   contrast it draws is not legible from the sentence. (The row's *title* already gets it right:
   "exec'd the reference gate by PATH".)

**Class** `vacuous` and **captured-by** QUALITY 126 are unchanged and correct: a control that
reaches `unmet` only through crash rows is exactly the vacuous reading QUALITY 126 forbids.

**Not my row, flagged for the L1:** M1's pointer `.ufo/waves/round-92/after/m1-landing-check.txt`
is missing by the same mechanism (never existed). M1's class is `landing`, which *is* in the
vocabulary; the fix is the same pointer repair.

---

## 5. The exact edit the L1 should make

Two files, two edits. **Byte offsets are pinned to rev `689623fd` and must be re-derived at the
landing revision before applying** (`receipts/04-byte-offsets.txt` carries the re-derivation
snippet) — the lane is moving under this round (four commits landed during this seat).

### Edit A — `corpus/QUALITY.md`, criterion 132's paragraph

- **File**: `corpus/QUALITY.md` (lane root; absolute `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md`)
- **Insertion point**: the whole of criterion **132**, bytes **126235..128342** inclusive (2108 bytes) at rev `689623fd`; that is the two lines currently at `corpus/QUALITY.md:324-325`, beginning `132. **A judge's oracle is unreachable` and ending `… error-row accounting.`
- **Bytes**: replace 2108 bytes with the drafted text of §3 (the red-leg pointer and the `Lesson:`
  anchor are the only two changes; everything else is byte-identical).
- **Constraint**: criterion 132 is one numbered item, so a wholesale paragraph replacement is
  required — no line-level splice will produce the corrected text without a rewrite of the item.
  QUALITY 60 (`R26-UNDISCLOSED-INPLACE`) therefore applies: the landing commit must disclose this
  in-place change of `corpus/QUALITY.md` in the round-92 lesson, and the sweep
  `git diff -U0 <base> <REV> -- corpus/QUALITY.md | grep -E '^-[^-]'` must print exactly that
  disclosure.

### Edit B — `corpus/lessons/round-92.md`, the M2 row

- **File**: `corpus/lessons/round-92.md` (lane root; absolute `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-92.md`)
- **Insertion point**: the M2 row block, bytes **3550..4598** inclusive (1049 bytes) at rev
  `689623fd`; that is the row at `corpus/lessons/round-92.md:47-57`, beginning
  `- **M2 (\`vacuous\`, self-found before filing)` and ending `(`.ufo/waves/round-92/after/m2-lie-wrapper-check.txt`).`
- **Bytes**: replace 1049 bytes with the drafted text of §4. Within that block the three strings
  that change are at abs **4083** (58 bytes, `…/before/controls/m2-lie-wrapper-path.py`), **4386**
  (49 bytes, `the embedded form yields verdict rows and reads \`met\``) and **4544** (50 bytes,
  `…/after/m2-lie-wrapper-check.txt`).
- **Constraint**: `PROTOCOL.md` §"Corpus corrections are new entries, never in-place rewrites" and
  `CORPUS.md` §"Corrections are new entries, never rewrites" both govern `corpus/knowledge/`
  entries; the lane's own `corpus/lessons/round-<N>.md` is lane-authored and the r91 precedent
  (`71fc1b66`, "lesson sync") edited a landed lesson row in place in the same commit that landed
  the receipt. The r89/r90 lessons carry a separate `## Errata` section (before `## Mistakes`) for
  corrections to *knowledge entries*. **Either is defensible; the L1 picks.** This seat's
  recommendation: **rewrite the M2 row in place in the same commit that lands the corrected
  receipts**, and disclose the changed lines per QUALITY 60 — the row is still open (the round's
  `## Wave summary` and `## Frontier` are placeholders), and an `## Errata` entry for a row that
  has not yet been read by a closure would duplicate the row.

### Not asked for, and not proposed here

- **No new criterion.** The seat brief asked for "one QUALITY criterion (number 132)". 132 exists.
  The class the round's own repairs uncovered (control dead in both legs → 133; control resolving
  its target by wildcard → 134) already has criteria. The one class this seat's §4 finding belongs
  to — *a lesson row's evidence pointer that names a path which never existed* — is a
  **`reference-drift`**-class instance of the round-92 M2 row, not a new corpus criterion, and
  QUALITY 113 (`R82-RAW-LINE-ANCHOR`, "the instrument that reads that anchor proves that the cited
  range IS the located span") plus QUALITY 127 (`R88-CORRECTION-NOT-SWEPT`) already cover the
  pointer-resolution discipline for corpus citations. The L1 may still want a criterion here; that
  is the L1's call and the seat did not draft one.
- **No `## Mistakes` row for §4's defect.** M2 *is* the row for that defect class; §4 repairs it.
- **The lane's frozen instruments, the freeze manifest, the declaration, `SCORECARD.md`, `LOG.md`,
  `SKILL.md`, `corpus/SOURCES.md` and every sibling seat's file were not touched by this seat.**

---

## 6. Out-of-scope observations (reported, not acted on)

These are findings this seat made while verifying its own item. They are outside the seat's
scope and outside the two edits above; they are recorded so the L1 does not have to re-derive
them.

1. **`run-c1.sh` does not reproduce the K1 receipt it produced.** The script's do-nothing leg is
   `git -C "$LANE" show "$REV^:tools/check-limine-pins.py"` with `REV=495a9f6c` — so `REV^` is
   `da99b2f4`, whose gate is `af90ae63…` = the **V2 gate**, not the r91 gate. The script therefore
   scores the candidate against itself (`89/89 met`). The committed `k1-donothing.txt` at `689623fd`
   reads `1/89 verdict unmet` with 352 error rows, and its JSON's `gate` is
   `…/l1/r91-gate.py` — so the receipt was produced by a **different** extraction than the script
   performs. Re-running the committed script reproduces `89/89 met`, not the committed receipt. The
   true r91 gate (`62bb06c9…`, at `07c58264`) measured under the r92 battery reads `1/89 unmet`
   with 352 error rows — this seat measured it directly and it matches the committed receipt, so
   the **receipt is right and the script is stale**. The C2 declaration's do-nothing clause
   ("the r91 gate … rejects `--limine-version` with rc 64, so every r92 case is an error row and
   the count is 0/89") is also off by one family: the measured count is **1/89** (`ERA-DEFAULT`
   passes, because the battery omits `--limine-version` for that family — `battery:243`,
   `pass_version = True`).

2. **C2's near-miss controls N01/N02 are non-executing.** `make-c2-gates.py` splices the override
   line `era_b = False  # N01: one v92 clause bent` at **column 0** while the surrounding code is
   indented 4 spaces, so both files raise `IndentationError: unexpected indent` at import
   (`python3 -c "import ast; ast.parse(...)"` → `IndentationError` on N01 and N02, clean on N03 and
   N04). Their receipts read `0/89 unmet` with **1068 error rows** — the "unmet" is a crash, not the
   declared 2-family / 3-family failure. `CriticClaims.md` §7 and `CriticForgers/` already report
   this (`falsifies-number`); the worktree now shows the L1 repairing `make-c2-gates.py`. Recorded
   here because criterion 132's green leg does not touch C2, but the round's C2 claim depends on
   these controls.

3. **`K4-syspath`'s before-leg receipt is split across two directories.** `before-clone/summary.tsv`
   records K4 at `0/82 unmet, 984 errors` with the **pre-A2** bytes `f3be5624…`, while the repaired
   `before-clone-fixed/summary.tsv` records `82/82 met` with the A2 bytes `efb53f76…`. Both are
   committed. A reader following criterion 132's "shown able to fail" leg needs both files; the
   drafted §3 text names both.

---

## Verdict

**C1 (operability) — supported by the corpus text this seat drafted, with two pointer repairs
outstanding.** Criterion 132's numbers all verify against the committed receipts (r91 battery
`82/82 met` on the five controls; r92 battery `0/89 unmet` with 0 error rows on the same five in
both layouts; the landed gate `89/89 met` ×3 in both layouts; `--isolation-check` printing
`lane_visible: false`, `sibling_files: ["gate.py"]`, PIDs `1,2`). The criterion exists in the house
shape with the required red / green / shown-able-to-fail and the "cannot close behaviour/timing"
limit. **This seat's edits (Edit A: the red-leg receipt pointer and the `Lesson:` anchor; Edit B:
the M2 row's two never-existing evidence pointers and its inverted `met` verdict) do not change any
verdict number — they repair pointers that name the wrong or a non-existent subject.**

**C2 (depth) — not falsified by this seat's item, but two out-of-scope defects (§6.1, §6.2) bear
on it:** `run-c1.sh`'s do-nothing leg extracts the V2 gate instead of the r91 gate (so the committed
script cannot reproduce the committed `K1-do-nothing` receipt), and the N01/N02 near-miss controls
crash on import so their `unmet` is a crash, not the declared 2/3-family failure. Both are
already being repaired in the worktree by other seats. This seat's item (criterion text + M2 row)
does not speak to C2's measurements.
