# Declaration fidelity — round 36 at `6d76fb20f6ecbc940e5c8fff36c74060c885e161`

Seat: ReviewDeclaration. Captures at 02:49:45Z; this file written 02:50:44Z (`date -u`).
Base of the declaration: `cefe752d9facf74113bb00a5925e3bfd0c863659` (parent of the
declaration commit, confirmed by `git rev-parse 6d76fb20^`).

Verdict legend: **PASS** / **DEFECT** / **PARTIAL** / **NOTE**.

## Item 1 — declaration section + LOG entry exist and match the campaign contract

**PASS with defects (M3, M4, L1) in sub-elements.**

Evidence:
- `git show 6d76fb20:SCORECARD.md | sed -n '1589p'` →
  `## Round 36 — declaration, pre-freeze candidate (2026-10-23, base \`cefe752d\`)`;
  section spans lines 1589–1684 (96 lines), appended (item 5 sweep shows no deletion).
- `git show 6d76fb20:LOG.md` line 1359 →
  `## Round 36 — declaration (2026-10-23, 02:33Z stamped at write)`; body lines 1361–1375.

Contract elements, each located:
- **Claims (brief text match).** C1 (SCORECARD:1598–1621) names the same five files, the
  same `--set livefive` probe, the same `leaking_pairs` measure, before >0 on each of the
  five, after 0 on all five, and the same sensitivity conjuncts (`MutAttrgetterCopy` /
  `MutPathCopy` above 0; `claim`/`r33claim`/`regression` at base 0). C2 (SCORECARD:1623–1634)
  names `corpus/knowledge/journalctl-v262-field-filter-r36.md`, the systemd 262 `-F`/`-N` +
  limiting-option rejection, live read-only host verification, S024 + new S198, and a
  prior-state counting command. Both match the round brief.
- **Distinct axes.** SCORECARD:1595–1596: "Two claims, distinct axes"; C1 operability,
  C2 depth — distinct.
- **Lowest-axis duty named.** SCORECARD:1593–1596: "Depth and adjacency are tied lowest at
  8; none retired; saturation 9 / window 3 unchanged … the depth claim (C2) carries the
  lowest-axis duty." Verified against the base state table: `depth | 8`
  (SCORECARD:1570), `adjacency | 8` (SCORECARD:1575), saturation/window rules at
  SCORECARD:173–178 and round-35 ordinal record at :1560.
- **Sourced claim.** Present at SCORECARD:1658–1663, but states future registry state as
  done — see **M3**, and its in-place re-open plan — see **M4**.
- **Separability.** SCORECARD:1660–1663: C1 touches the five tools + new probe; C2 adds one
  note plus `SKILL.md`/`corpus/README.md`/`SOURCES.md` rows; the probe never reads the note.
- **Repairs.** SCORECARD:1665–1678 lists items (1), (2), (4), (5) plus the routed-debt-3b
  note; item (3) is repaid in C1 and the counter paragraph but is not cross-referenced —
  see **L1**. Repair (4)'s anchors are accurate at base: `SKILL.md:397-399`,
  `corpus/knowledge/update-safety-note.md:420-424`, `corpus/knowledge/update-safety-v2.md:52`
  and `:198` all name `NoUpgrade`/`NoExtract` as pins (verified by `git show cefe752d:<f> |
  sed -n`).

## Item 2 — census line vs rerun

**PASS (exact).**

`./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
rerun by this seat (capture stamped 02:49:45Z): exit 0; 197 source rows; 31 `W04` advisories; 32 `tsukuroi` output lines
(31 W04 + 1 `ok`); last line `tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`.
Capture: `census-validate.txt`.
The LOG entry claims "exit 0, 197 rows, 31 W04 advisories, last line `tsukuroi ok`"
(LOG.md:1370–1372) — every element reproduces. The independent row count agrees:
`git show 6d76fb20:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3}'` → 197.
The exact claimed run time (2026-10-24T02:26:45Z) is not independently reproducible;
the values are.

## Item 3 — tarball tracked; status otherwise empty

**PASS on tracking; PARTIAL on "otherwise empty" (time-dependent, explained).**

- `git ls-files | grep pacman-54d9411` → `.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz`
  (tracked), and `git diff --name-status cefe752d 6d76fb20` lists exactly three paths:
  `A .ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz`, `M LOG.md`, `M SCORECARD.md`.
  Repair (1) is therefore satisfied by this commit.
- `git status --porcelain -uall` is **not** empty: every entry is untracked wave-1 scratch
  under `.ufo/waves/round-36/` (seat receipts, `w1-*.json`, `l1/gen-w1-spec.py`) plus this
  seat's own new directory. **Zero modified tracked files** and no production path appears
  (`tools/`, `corpus/`, `SCORECARD.md`, `LOG.md` clean against HEAD).
- Consequence: the "otherwise empty" clause can only be tested before wave-1 seats write;
  the substantive property it protects (no uncommitted production change) holds.

## Item 4 — heading times vs commit

**PASS on the routed rule; NOTE L2 on the LOG heading's date basis.**

- `git log -1 --format=%cI 6d76fb20` → `2026-10-23T23:34:31-03:00` = `2026-10-24T02:34:31Z`.
- Declaration text: `Written 2026-10-24T02:33Z` (SCORECARD:1591) — 91 s **before** the
  commit. LOG census run: `2026-10-24T02:26:45Z` — before the declaration stamp.
- LOG heading (LOG.md:1359) writes `2026-10-23, 02:33Z`: local date + UTC clock. As written
  it denotes 2026-10-23T02:33Z, ~24 h before the commit; it is not *later* than the commit,
  so the round-35 routed defect (later-than-commit headings) does not recur, but the date
  component is not the `date -u` date (which is 2026-10-24) and differs from the body's
  `2026-10-24T02:33Z`.

## Item 5 — append-only sweep

**PASS.**

`git diff -U0 cefe752d 6d76fb20 -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md | grep -E '^-[^-]'`
prints nothing (exit 1; 0 deletion lines). The same diff adds 94 lines and touches only
`SCORECARD.md` and `LOG.md` (`diff --git` headers); `corpus/QUALITY.md`, `corpus/SOURCES.md`
and `SHONEN.md` are unchanged. Captures: `append-only.txt`, `append-only-full.diff`.

## Item 6 — C1 counter shape (lineage, predicate, label, counting command)

This is the item the five above do not cover and where the material defects sit.

**DEFECT H1 — counter lineage names the wrong base revision.**
SCORECARD:1637–1639: "written in wave 1 as the round-34 probe
(`tools/probe-child-env-allowlist-r34.py`, VERSION 4) plus this paragraph, VERSION 5".
At `cefe752d` the file reads `VERSION = 6` and `PREDICATE_LABEL = 'leaking'`
(`tools/probe-child-env-allowlist-r34.py:215-216`). Version history of that file:
`6de666c` → `VERSION = 4` (round-34 declaration), `15c9ac0` → `VERSION = 5`
(amendment 1, claim-base parity), `3457f28` → `VERSION = 6` (amendment 2, any-name value /
execveat / unparseable). The same paragraph cites "the normalisation fixes from the
round-35 `ExecV6Calibration` receipts" (SCORECARD:1645), and those receipts record
`"probe_version": 6` (`.ufo/waves/round-35/w1/ExecV6Calibration/r33claim-v6.jsonl`,
`regression-v6.jsonl`). Building the r36 counter from VERSION 4 as written would drop
amendments 1–2 — the clauses that made the round-34 counter sound — and would reuse version
number 5, which already denotes different bytes. Capture: `probe-cli.txt`.
Fix before the freeze: name the V6 base (with its sha256) and give the new probe a version
above 6, or state explicitly that the new file restarts its own numbering.

**DEFECT H2 — the frozen predicate sentence is not in the declaration, although the
declaration says it is.** SCORECARD:1620–1621: "its frozen predicate label is
`leaking_pairs`, the same sentence in this declaration, the probe's `PREDICATE` constant and
every receipt." `git show 6d76fb20:SCORECARD.md | sed -n '1589,$p' | grep -nE 'pair is
leaking|FROZEN PREDICATE|A \(target, channel\)'` prints nothing: the 96-line round-36
section carries no predicate sentence. Prior declarations print the label followed by the
sentence in quotes (`SCORECARD.md:1270`, `:1425`, `:1449`: `label \`leaking\` … :
"A (target, channel) pair is leaking when …"`), which is the shape the freeze compares. Without the sentence in the declaration, the
pre-freeze control seats and the freeze cannot compare `predicate` against declared text,
only against the probe's own docstring/constant.

**DEFECT M1 — predicate label misstated.** SCORECARD:1620 names the frozen label
`leaking_pairs`; the base probe's label is `leaking` (`:215`), and `leaking_pairs` is the
summary line's *list* of leaking pairs (`:1006`: `'leaking': len(leaking), 'leaking_pairs':
leaking`). The round-34 declarations name the label `leaking` (SCORECARD:1425, 1449, 1461),
and the committed receipts carry it: 29 `"predicate_label": "leaking"` lines under
`.ufo/waves/round-34/w2/` and `l1/`, plus 2 in the round-35 `ExecV6Calibration` receipts.
Either keep `leaking` as the label and name `leaking_pairs` as the measure key, or declare
the label change explicitly (the round-34 receipts carry `leaking`).

**DEFECT M2 — the declared counting command passes an undeclared flag.** SCORECARD:1614:
`python3 tools/probe-child-env-allowlist-r36.py --lane <lane> --revision <REV> --set livefive --json`.
The base probe's argparse accepts only `--revision --lane --scratch --set --only --base`
(`--help`, capture `probe-cli.txt`); `grep -n "'--json'"` finds nothing. `--json` is
therefore a new CLI surface that the declared lineage ("the round-34 probe plus this
paragraph") does not mention; as written the command is not runnable against the named
base. Fix: declare the flag as an addition, or drop it (output is already one JSON line per
pair plus a summary line).

**PASS — before-state of the five tools is accurate.** All five build a child environment
from the ambient environment minus a prefix and pass it to spawns:
`check-revision-binding.py:103-105` (`clean_env()`, `GIT_*` filter; used at :115, :188,
:226, :369, :417, :1116), `check-report-receipts.py:311-321` (`find_receipts`, `GIT_*`
filter, existing `GIT_CONFIG_SYSTEM`/`HOME`/`XDG_CONFIG_HOME`/`GIT_CEILING_DIRECTORIES`;
passed at :328), `score-census-handoff-r32.py:786` (`TSUKUROI_*` filter; passed at :489),
`mutants-btrfs-space-r30.py:362-364` (`GIT_*` filter; passed at :364),
`run-receipt.py:36-40` (`env()`, `GIT_*` filter, existing `HOME`/`XDG_CONFIG_HOME`; passed
at :52, :81, :83, :86, :96, :102). So "Any non-`GIT_*` ambient name … reaches every child"
is true of the base.

**PASS — sensitivity artifacts exist and are committed.** `MutAttrgetterCopy` and
`MutPathCopy` receipts and reports are tracked under `.ufo/waves/round-34/w2/`
(`MutAttrgetterCopy.md`, `MutPathCopy.md`, `mutant-claim.jsonl`, `execution.json`, etc.).

**PASS — freeze/kill rule shape.** sha256 in the LOG at freeze, kill rule fixed before any
seat scores the after value, and the kill rule forbids the "skip the work" escape
(SCORECARD:1645–1657). Note [inf]: a mutant reading 0 does not itself fire the kill rule,
but it fails the declared after-conjunct ("sensitivity checks green"), so coverage holds by
conjunction.

## Item 7 — claim count ("claims 1-3")

**NOTE, not a defect attributable to the declaration.** The declaration carries two claims
(C1, C2) and both match the round brief verbatim in substance. No fleet-root or lane
document states a three-claim requirement: `grep -rniE 'claims? (1.?3|three claims)'` over
`scripts/`, `SHONEN.md` and the lane finds no rule; `SHONEN.md` is the promotion checklist.
Prior rounds vary (SCORECARD:587 "Three declared, causally separable claims"; round 35 has
two). If the campaign contract does mandate three, the declaration is one short and no
wave-1 seat can supply it — L1 must reconcile before the freeze.

## Defect list (severity order)

| id | severity | location | summary |
|---|---|---|---|
| H1 | high | SCORECARD:1637–1645 | counter lineage names r34 VERSION 4 → VERSION 5; base is VERSION 6, and V5 already denotes round-34 amendment-1 bytes; cited receipts are V6 |
| H2 | high | SCORECARD:1620–1621 | "the same sentence in this declaration" — the predicate sentence is absent from the 96-line section |
| M1 | medium | SCORECARD:1620 | frozen label stated `leaking_pairs`; base label is `leaking` (that key is the pair list) |
| M2 | medium | SCORECARD:1614 | counting command passes `--json`, absent from the base probe CLI |
| M3 | medium | SCORECARD:1658–1660 | S024 described as "opened this round (re-opened pinned …)" and S198/lesson quotes as recorded; at the commit S024 is `queued`/unpinned, S198 absent, no round-36 lesson |
| M4 | medium | SCORECARD:1658–1659 | in-place S024 re-open conflicts with the registry's no-old-row-change discipline (SOURCES.md:258, :262, :264) |
| L1 | low | SCORECARD:1665–1678 | repair list (1),(2),(4),(5) omits (3) with no pointer |
| L2 | low | LOG.md:1359 | heading mixes local date with UTC clock; not later than the commit, but not the `date -u` date |
