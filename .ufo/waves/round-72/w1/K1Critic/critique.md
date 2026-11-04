# K1Critic — round 72 declaration falsification

Read: SCORECARD.md "Round 72 — declaration" at `6b42676` (base `a7015d27`), every receipt under
`.ufo/waves/round-72/before/`, the three frozen instruments, both batteries, `corpus/lessons/
round-71-verifier-spotcheck.md` §6, the r70/r71 declarations and errata, and the fleet `AXES.md`
§The stagnation nudge. Read-only; nothing in the lane was written.

Scope of the verdict: the declaration is not falsified as *targets* — all three predicates are
measurable, the before-state reproduces at `a7015d27`, and the drafted after-artefacts (note,
registry rows, `--selftest`, erratum) already read what the claims ask. What fails is the fit
between each claim's prose and its instrument: every one of the three targets survives a
do-nothing/fabricated artefact, one cited red-before is not in committed bytes, one host fact is
false, and one frozen battery case does not test the clause it names. Nine defects, none of which
requires amending a frozen predicate.

## 1. Conjunct enumeration and measuring command

### C1 — depth (lowest tied 8; SOURCED S301–S303)

| # | conjunct | measured by | state |
|---|---|---|---|
| 1 | note exists at the measured revision | `git cat-file -e <REV>:corpus/knowledge/modprobe-config-plane-r72.md` | base rc 128 (confirmed) |
| 2 | 6 MD rows, each one physical line, 7 pipes, grammar cells | `python3 tools/count-md-rows-r72.py --revision <REV>` | drafted note: 6/6 rows parse |
| 3 | id unique, contiguous from 1 | same counter (`seen_ids`, `contiguous`) | pass |
| 4 | statement ≥ 12 words | counter `words(stmt)` | pass |
| 5 | ≥ 6 shared distinct non-stopword tokens (len≥4) **and** shared/total ≥ 0.5 vs the row's snapshot | counter `grounding()` | pass — but see CONTROL 1 |
| 6 | `source=` a registry row at the same revision, kind in KINDS, not own-work | counter (`KINDS`, `regrow`) | S301 docs / S302,S303 code |
| 7 | snapshot exists under `before/src`, sha256 == digest, == `SOURCES.json` map digest | counter `rb()` + map | 3 digests match `sha256sum -c` rc 0 |
| 8 | registry source cell contains the map URL; anchor cell contains the snapshot basename | counter `source-not-bound` / `anchor-not-bound` | pass |
| 9 | quote ≤ 25 words, no pipe, verbatim (whitespace-normalised) | counter `norm()` | pass |
| 10 | no MD-shaped line that fails to parse | counter `malformed` | 0 |
| 11 | no snapshot cited > 2 | counter `reuse` | S301×2, S302×2, S303×2 |
| 12 | totals `MD_ROWS=6 MD_VERIFIED=6 MD_SOURCES=3 MD_SNAPSHOTS=3 MD_MALFORMED=0`, met=1, rc 0 | counter | drafted tree: met=1 rc 0 |
| 13 | registry 300 → 303 rows | `git show <REV>:corpus/SOURCES.md \| grep -cE '^\| *S[0-9]{3,}'` | base 300 (confirmed); working tree 303, NF=13 each |
| 14 | knowledge notes 89 → 90 | `git ls-tree --name-only <REV>:corpus/knowledge \| grep -c '\.md$'` | base 89 (confirmed) |
| 15 | canonical census validate rc 0 | **no command named** | see D7 |
| 16 | novelty: 0 token hits, `SKILL.md` 0, `PROVINCE.md` 4, `README.md` 2 | git grep at base | confirmed (0/0/0/0/0/0; 4; 2; 0) |

### C2 — operability, capability `gate-selftest`

| # | conjunct | measured by | state |
|---|---|---|---|
| 1 | `--selftest` mode exists, rc 0 | `python3 tools/check-selftest-tally.py --selftest` | base tool rc 2, 0 case lines (confirmed); drafted tool rc 0, 9 case lines |
| 2 | prints `SELFTEST: PASS (N cases, N passed, 0 failed)`, N ≥ 7, one named line per case | same command (stdout only) | drafted: 9/9 |
| 3 | fixtures built under `$TMPDIR`, never `/tmp` | **no named measurement** | see D4 |
| 4 | cases cover match / mismatch (stable finding id) / wrong label / superseded skip / out-of-scope battery / no-PASS receipt rc 2 | **no named measurement** | see D4 |
| 5 | red-before mutant fails the suite with a named failing case | `before/control/selftest-redbefore.txt` | file is **not committed** (D1) |
| 6 | r70 self-demo unchanged: `added_figures_mismatched=0 receipt_cases=214 receipt_labels=18` rc 0 | declared command, base tool | confirmed rc 0, 214/18 (base and drafted tool) |

### C3 — freshness

| # | conjunct | measured by | state |
|---|---|---|---|
| 1 | `.ufo/waves/round-71/after/count-mp-rows-final.txt` exists and its summary lines equal a fresh run at `2b358d2d` | `python3 tools/check-r71-routed-r72.py --revision <REV>`; fresh counter | base: missing; fresh run `MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0`, met=1 |
| 2 | SCORECARD has a `## Round 71 — receipt erratum` block naming the receipt path and `2b358d2d` | same checker, substring in block | base: missing; drafted: present |
| 3 | note correction names `R71-NOTE-MODPROBE-COUNT`, the five `/usr/lib/modprobe.d` paths, the superseded four figure | same checker: `"five" in tail and "four" in tail and "/usr/lib/modprobe.d" in tail` | base: missing; **not the five paths** (D2) |
| 4 | `ROUTED_STALE=3` rc 1 → `ROUTED_STALE=0` rc 0 | same checker | base confirmed 3/rc 1; control reaches 0 (CONTROL 3) |

## 2. Do-nothing / fabrication controls (measured; full transcript in controls.txt)

1. **C1 survives a fabricated note.** A 6-row fixture whose MD1 statement is the negation of its
   own verbatim quote ("Configuration directories are **never** read in SYNOPSIS order … the same
   name in subsequent directories is **still parsed**") reads `MD_ROW ok MD1`, `MD_VERIFIED=6`,
   `met=1` rc 0. The empty-note control reads `MD_ROWS=0 … met=0` rc 1 (declaration (d) confirmed).
   So the target is reached by a note that states a rule its source contradicts: the floor is
   lexical, not substantive. The declaration discloses this channel in "planned (next round)", so
   it is a *disclosed* limitation — the defect is that the C1 row's prose ("states the plane")
   reads as content-correctness while the instrument cannot see direction.
2. **C2 survives an echo.** A copy of the base tool plus a `--selftest` branch that prints seven
   `PASS (SELFTEST-…)` lines and `SELFTEST: PASS (7 cases, 7 passed, 0 failed)`, builds no fixture
   and runs no core, reads rc 0 with 7 case lines and keeps the r70 self-demo at 214/18. Every
   counted term of the C2 after-state is met with no fixtures at all.
3. **C3 survives both fabrication and contradiction.** (a) A 137-byte receipt carrying only the two
   summary lines, a one-line SCORECARD block that merely repeats the path and `2b358d2d`, and a
   one-line note "correction" containing `R71-NOTE-MODPROBE-COUNT … five four … /usr/lib/
   modprobe.d` (zero paths enumerated) reads `ROUTED_STALE=0` rc 0. (b) A SCORECARD block reading
   "No erratum is needed; `2b358d2d` stands; … is not a receipt" and a note reading "the correction
   is withdrawn: there are not five or four `/usr/lib/modprobe.d` paths" also reads rc 0. The
   committed green fixture of `routed-battery.py` already demonstrates (a) — its NOTE enumerates no
   paths and the checker passes.

## 3. Separability, axis distinctness, window arithmetic

- **Separability holds.** C1 writes the note, three registry rows, the note count and its counter;
  C2 writes only `tools/check-selftest-tally.py`; C3 writes the r71 receipt, one SCORECARD erratum
  and the r71 note. No path overlap; the C2 self-demo reads a fixed past range
  (`4035c1a0..40c35ee7`), so a later SCORECARD erratum cannot perturb it. Each verifies alone.
- **Axes distinct.** depth / operability / freshness. The lowest non-retired axis is depth 8, tied
  with adjacency 8 (r71 outcome: depth 8→8, adjacency 8); C1 works it. C2 and C3 work 9s.
- **Window arithmetic is wrong.** `AXES.md` §The stagnation nudge counts *rounds without a new
  capability*. The lane's own precedents: r68 declaration "capability entered r68 … window at 1 of
  3"; r70 "capability entered round 69 … 1 of 3"; r71 "capability entered round 70 … 1 of 3". r71
  entered `selftest-case-timeout`, so at r72 the window is **1 of 3**, not "2 of 3". Two
  capability rounds do not advance a window that measures their absence. No duty change: the nudge
  needs every axis ≥ 9 and depth is 8, so D6 is calibration-only.

## 4. D-items

**D1 — HIGH — C2's cited red-before is not in committed bytes.**
`before/control/selftest-redbefore.txt` is named in the frozen C2 row but
`git cat-file -e 6b42676:.ufo/waves/round-72/before/control/selftest-redbefore.txt` is rc 128; the
file exists only as an untracked working-tree file, and its own header names the mutant as
`/fast/scratch/hyaku/tsukuroi-r72/L1/redbefore/mutant.py` — a scratch path deleted with the scratch
tree. The declaration's (e) section does not list it among the committed receipts either.
*Correction (append-only):* an erratum under "Round 72 — declaration errata" stating that the
red-before receipt is uncommitted at `6b42676`; the round must commit an equivalent, reproducible
mutant proof under `.ufo/waves/round-72/after/` and the erratum must cite that path. Do not edit the
frozen row.

**D2 — HIGH — C3's text conjuncts are word presence, so "closed" overclaims.**
The NOTE conjunct is `"R71-NOTE-MODPROBE-COUNT" in tail and "five" in tail and "four" in tail and
"/usr/lib/modprobe.d" in tail`; the SCORECARD conjunct is two substring tests. Measured: a
*withdrawn/contradicted* pair passes (CONTROL 3b), and the five paths are never checked. The
declaration's "the two statement/receipt defects … are closed in committed bytes" therefore states
more than the instrument can see; the committed routed-battery green fixture itself shows a
zero-path note passing.
*Correction (append-only):* an erratum narrowing C3's measured claim to "the checker's substring
set is met"; the five-path enumeration and the correction's direction must be checked by the
non-author reviewer against `before/host.txt` and recorded in the after receipt. The future-round
counter should test the five names, not the word "five".

**D3 — MEDIUM — declaration (b)'s `/proc/cmdline` fact is false.**
The captured cmdline itself carries `zswap.enabled=1` and `zswap.max_pool_percent=25`
(`/sys/module/zswap/parameters/{enabled,max_pool_percent}` exist; `tr ' ' '\n' </proc/cmdline`
yields four `a.b=` tokens, two of them module parameters). "carries no `module.parameter` token" is
wrong, and the host is in fact a live instance of MD4's path rather than an inert one.
*Correction (append-only):* erratum replacing the fact with "carries two zswap module-parameter
tokens (`zswap.enabled`, `zswap.max_pool_percent`); the MD4 path is live on this host". The drafted
note does not repeat the false sentence; keep it that way.

**D4 — MEDIUM — C2's predicate is under-determined relative to its claim and to the routed repair.**
(a) The frozen row names six case behaviours but requires **N ≥ 7**; the seventh (green-control)
exists only in the uncommitted red-before (D1) and the drafted tool has nine differently-named
cases. Any seventh case satisfies the count. (b) "fail with a stable finding id" is unmeasured —
the checker prints `MISM f:ln …`/case-name lines, not a stable finding id, and the r71 lesson's
"committed expected verdicts" is not in the predicate. (c) "builds every fixture under `$TMPDIR`"
and the kill rule "any case writing under `/tmp`" have no named measurement; the only command is
the tool reporting on itself (CONTROL 2).
*Correction (append-only):* erratum listing the seven (or nine) case ids as the frozen set and
requiring the after receipt to carry the per-case expected verdicts and the `$TMPDIR` proof; the
reviewer must spot-check that at least one case fails when its branch is disabled.

**D5 — MEDIUM — the C1 battery's `mutant-duplicate-id` case does not test duplicate ids.**
`[ROWS[0], ROWS[1], ROWS[1], ROWS[3], ROWS[4], ROWS[5]]` renumbers to MD1–MD6, so it reads
`MD_ROW fail snapshot-reuse modprobe.d.5.scd=3` with `MD_VERIFIED=6` — killed by reuse, not by the
id clause. A true duplicate-id fixture (`MD1, MD2, MD2, …`) prints `duplicate-id` +
`ids-not-contiguous` + reuse. No battery case isolates `duplicate-id` or `ids-not-contiguous`; a
mutant that disables either clause survives. This is the r71 erratum (d) class recurring in a new
instrument.
*Correction (append-only):* erratum recording the battery defect; add a case that duplicates a row
in place of a row citing the **same** source and relabels the duplicate with the original id (e.g.
MD1 S301, MD2 S301, MD3 S302, MD3 S302 [duplicate of MD3], MD5 S303, MD6 S303): reuse stays at 2
per snapshot, so the only failures are `duplicate-id`/`ids-not-contiguous`.

**D6 — MEDIUM — stagnation window "2 of 3" contradicts AXES and three precedents.**
See §3. *Correction (append-only):* erratum reading "window at 1 of 3; the nudge is inapplicable
because depth/adjacency are 8". No predicate change.

**D7 — LOW — C1's "canonical census validate rc 0" has no command.**
It appears in the C1 before→after cell and in `before/absence-controls.txt` as bare "census
validate rc=0"; the r71 erratum (c) established the intended command as
`scripts/sources-census.sh validate --root … tsukuroi` (fleet repo, present at
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`), but r72 neither names it nor captures
its output. Recurrence of the r71 erratum (c) defect.
*Correction:* the after receipt must print the command and its rc, or the erratum must drop the
conjunct.

**D8 — LOW — the frozen instruments' own docstrings disagree with their case counts.**
`battery.py` docstring: "one well-formed control plus eleven mutants" — the code builds 11 cases
(1+10), as `battery.txt` and the declaration say. `routed-battery.py` docstring: "one green control
plus three red mutants" — it defines 5 cases (1+4). The declaration's counts are right; the frozen
bytes' prose is wrong.
*Correction (append-only):* note in the erratum; do not rewrite the frozen instrument bytes.

**D9 — LOW — "all under `before/` at base `a7015d27`" conflates the measured tree with the commit.**
No `before/` file exists at `a7015d27`; all thirteen were introduced by the declaration commit
`6b42676` (`git show --stat`). The measurement base is `a7015d27`; the provenance commit is
`6b42676`.
*Correction (append-only):* say "measured against `a7015d27`, committed with this declaration at
`6b42676`".

## 5. Residual limits (not counted as defects)

- R1: the C1 lexical channel (a negating row reads `met=1`) is disclosed in "planned (next round)";
  CONTROL 1 measures it. The C1 verdict must be worded "lexically grounded rows", not
  "content-correct rules", until that channel lands.
- R2: the SOURCED binding is self-attested — S301–S303's `kind`/URL/anchor cells are authored in
  the same round, and the counter checks substring presence. The byte-anchored snapshot digests are
  the real defence; the registry labels are not independently verified.
- R3: `R71-RECEIPT-MISPATH` is a report-time promise and cannot be verified at declaration time.

## 6. Impacted axes

Calibration (the round's own record accuracy) for D1–D9. The measured axes are not harmed *if the
predicates are read as frozen*: C1 depth (8), C2 operability (9, capability row only), C3 freshness
(9). The one scoring hazard is C2: if the echo control is accepted as the `--selftest` mode, the
capability row `gate-selftest` would be false provenance — the capability table must be filled from
the committed expected-verdict receipt, not from `SELFTEST: PASS`.

## 7. Append-only amendments requested (no frozen predicate changes)

1. Erratum D1 (red-before provenance) + the after receipt path.
2. Erratum D2 (C3 measured scope) + the five-path enumeration in the after receipt.
3. Erratum D3 (cmdline fact).
4. Erratum D4 (case ids / expected verdicts / `$TMPDIR` proof in the after receipt).
5. Erratum D5 (battery duplicate-id case) + the isolated fixture.
6. Erratum D6 (window 1 of 3).
7. Erratum D7 (census validate command) or drop.
8. Erratum D8 (instrument docstrings).
9. Erratum D9 (base vs provenance commit wording).
