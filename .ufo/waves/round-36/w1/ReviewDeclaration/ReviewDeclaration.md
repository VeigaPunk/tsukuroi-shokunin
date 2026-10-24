# ReviewDeclaration — declaration fidelity review, round 36 at `6d76fb20`

Seat: `ReviewDeclaration` (independent leaf; no delegation).
Written 02:51:06Z (`date -u`, pasted at write). Captures taken 02:49:45Z; census rerun by
this seat (capture stamped 02:49:45Z). Lane repo (read-only for production): `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Machine evidence: `fidelity.md`, `census-validate.txt`, `append-only.txt`,
`append-only-full.diff`, `status.txt`, `times.txt`, `sources-state.txt`, `probe-cli.txt`
(all in this directory).

Scope: the declaration commit `6d76fb20f6ecbc940e5c8fff36c74060c885e161` against its
parent/base `cefe752d9facf74113bb00a5925e3bfd0c863659`, plus the five checklist items
(census, tarball/status, heading times, append-only sweep) and the C1 counter shape.
This seat cannot edit production files; every repair below is a recommendation for the L1
before the freeze.

## Checklist result

| item | verdict |
|---|---|
| 1. declaration section + LOG entry, contract elements | PASS with M3, M4, L1 |
| 2. census line vs rerun (rows, exit) | PASS, exact |
| 3. tarball tracked; status otherwise empty | PASS on tracking; PARTIAL on emptiness (wave-1 scratch only) |
| 4. heading times ≤ commit | PASS (no later-than-commit stamp); NOTE L2 |
| 5. append-only sweep over the five files | PASS (0 deletion lines) |
| 6. C1 counter shape (not in the five) | DEFECT H1, H2, M1, M2 |
| 7. claim count ("claims 1-3") | NOTE — brief defines two; no third-claim rule found |

## Findings

### H1 (high) — the C1 counter is declared as derived from the wrong revision of the round-34 probe

`SCORECARD.md:1637-1639` (at `6d76fb20`): the counter is "written in wave 1 as the round-34
probe (`tools/probe-child-env-allowlist-r34.py`, VERSION 4) plus this paragraph, VERSION 5,
the `livefive` set, an untraced view … and the normalisation fixes".

Evidence:
- Base bytes: `tools/probe-child-env-allowlist-r34.py:215-216` at `cefe752d` →
  `PREDICATE_LABEL = 'leaking'`, `VERSION = 6`.
- Version history of that file (`git log` + per-commit `grep '^VERSION = '`):
  `6de666c` VERSION 4 (round-34 declaration), `15c9ac0` VERSION 5 (amendment 1, claim-base
  parity), `3457f28` VERSION 6 (amendment 2, any-name value / execveat / unparseable).
- The same declaration paragraph cites the "normalisation fixes from the round-35
  `ExecV6Calibration` receipts" (`SCORECARD.md:1645`); those receipts record
  `"probe_version": 6` (`.ufo/waves/round-35/w1/ExecV6Calibration/r33claim-v6.jsonl`,
  `regression-v6.jsonl`).

Why it matters: built exactly as declared, the only instrument for the round's measured
claim would predate the two amendments that made the round-34 counter sound (the clauses
that killed round 34's C1 were about exactly this escape space), and "VERSION 5" would name
different bytes from the round-34 amendment-1 file of the same number. The freeze binds
bytes by sha256, so the freeze itself would not catch this; the declaration's lineage is
what the pre-freeze control seats and the final reviewer read.
Repair: name the VERSION 6 base (with its sha256) and number the new probe above 6, or state
that the new file restarts its own numbering; drop the "(VERSION 4)" parenthetical.

### H2 (high) — the frozen predicate sentence the declaration says is present is absent

`SCORECARD.md:1620-1621`: "its frozen predicate label is `leaking_pairs`, the same sentence
in this declaration, the probe's `PREDICATE` constant and every receipt."

Evidence: the round-36 section is 96 lines (1589–1684) and
`git show 6d76fb20:SCORECARD.md | sed -n '1589,$p' | grep -nE 'pair is leaking|FROZEN
PREDICATE|A \(target, channel\)'` prints nothing. Prior declarations print the label
followed by the sentence in quotes (`SCORECARD.md:1270`, `:1425`, `:1449`: `label \`leaking\`
… : "A (target, channel) pair is leaking when …"`) — the exact shape the freeze compares
against.
Why it matters: the freeze rule says predicate, label and set "do not change" after the
freeze; with the sentence absent from the declaration there is nothing in the frozen text
to compare the probe's `PREDICATE` against.
Repair: paste the exact predicate sentence into the declaration before the freeze.

### M1 (medium) — the frozen predicate label is misstated

`SCORECARD.md:1620` states the frozen label is `leaking_pairs`. The base probe's label is
`leaking` (`tools/probe-child-env-allowlist-r34.py:215`); `leaking_pairs` is the summary
line's list of leaking pairs (`:1006`, `'leaking_pairs': leaking`), not a label. The
round-34 declarations state label `leaking` (`SCORECARD.md:1425, 1449, 1461`), and the
committed receipts carry it — 29 `"predicate_label": "leaking"` lines under
`.ufo/waves/round-34/w2/` and `l1/`, plus 2 in the round-35 `ExecV6Calibration` receipts.
Repair: either keep label `leaking` and call `leaking_pairs` the measure key (matching the
round brief), or declare the label change as such.

### M2 (medium) — the declared counting command uses a flag the base probe does not accept

`SCORECARD.md:1614`: `python3 tools/probe-child-env-allowlist-r36.py --lane <lane>
--revision <REV> --set livefive --json`.
The base probe's argparse accepts only `--revision --lane --scratch --set --only --base`
(`--help`, capture `probe-cli.txt`); `grep -n "'--json'" tools/probe-child-env-allowlist-r34.py`
finds nothing. Under the declared lineage ("the round-34 probe plus this paragraph") the
command is not runnable as written; `--json` is an undeclared CLI addition.
Repair: declare the flag among the changes, or drop it — the probe already emits one JSON
line per pair plus a summary line.

### M3 (medium) — the sourced-claim paragraph states future registry state as done

`SCORECARD.md:1658-1660`: "C2 rests on S024 opened this round (re-opened pinned to the
systemd v262 tag) and a new row S198 (journalctl(1) at systemd 262); both quotes are recorded
in the round-36 lesson `## Gate`."
At the declaration commit: `corpus/SOURCES.md` has 197 rows, last row S197, no S198
(`sources-state.txt`); S024 is `status queued` with anchor "main branch fetched 2026-10-19
(mutable: main now opens with CHANGES WITH 263 in spe; no commit pin claimed)"
(`corpus/SOURCES.md:30`); no `corpus/lessons/round-36*` file exists. The same declaration's
C2 *Before* correctly says "S024 (queued)" (`SCORECARD.md:1626`), so the two paragraphs
contradict each other. Rounds 34/35 used an explicit "(opened in wave 1)" marker for
planned sources.
Repair: mark the sentence as wave-1 work (or "to be recorded"), keeping the frozen claim
text honest about what exists at freeze.

### M4 (medium) — the S024 "re-open" plan conflicts with the registry's own append-only discipline

`SCORECARD.md:1658-1659` plans to re-open S024 "pinned to the systemd v262 tag". The
registry's curation records state the discipline explicitly: "no old immutable cell, status,
recheck or used-by changed" (`corpus/SOURCES.md:258`, `:262`, `:264`). An in-place pin
change to S024's anchor/status would mutate an existing row.
Repair: record the pinned v262 re-open as a new/supersession row (the new S198 can carry the
pin) and leave S024's cells untouched; say so in the declaration.

### L1 (low) — repair list numbering

`SCORECARD.md:1665-1678` lists repairs "…(1) … (2) … (4) … (5)". The round-35 spot-check
§6 has five items; item 3 is repaid (C1 for the five tools, the counter paragraph for the
probe debts) but has no pointer in the list. Repair: add "(3) repaid by C1 and the counter
paragraph" or renumber as a mapped list.

### L2 (low) — LOG heading mixes date bases

`LOG.md:1359`: `## Round 36 — declaration (2026-10-23, 02:33Z stamped at write)`. The commit
is `2026-10-23T23:34:31-03:00` = `2026-10-24T02:34:31Z`; the body says
`2026-10-24T02:33Z` (`SCORECARD.md:1591`). The heading's time is **not later** than the
commit, so the routed round-35 defect does not recur, but the heading as written denotes
2026-10-23T02:33Z (~24 h early) and its date is not the `date -u` date.
Repair: write `2026-10-24, 02:33Z` or drop the date component.

## What verified clean

- **Census (item 2): exact.** `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tsukuroi` → exit 0, 197 rows, 31 `W04` advisories, last line
  `tsukuroi ok`; matches `LOG.md:1370-1372` and the independent SOURCES row count (197).
- **Tarball (item 3).** `.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz` is
  tracked and added in this commit; `git diff --name-status cefe752d 6d76fb20` is exactly
  `A` tarball + `M LOG.md` + `M SCORECARD.md`. `git status --porcelain -uall` shows only
  untracked wave-1 scratch under `.ufo/waves/round-36/` — no modified production file.
- **Heading times (item 4).** Declaration 02:33Z and census 02:26:45Z both precede the
  commit's 02:34:31Z; the round-35 routed "later than commit" defect does not recur.
- **Append-only (item 5).** Zero `^-[^-]` lines across `SCORECARD.md`, `LOG.md`,
  `corpus/QUALITY.md`, `corpus/SOURCES.md`, `SHONEN.md`; 94 added lines; only SCORECARD and
  LOG changed.
- **Contract elements.** C1/C2 text matches the round brief in substance; axes are distinct
  (operability/depth); the lowest-axis duty is named and the base numbers check out (depth 8
  and adjacency 8 tied lowest, saturation 9 / window 3; `SCORECARD.md:1560, 1570, 1575`,
  rules `:173-178`); separability is stated and plausible; repair (4)'s four anchors are
  accurate at base; repair (1) lands in this commit.
- **C1 before-state.** All five tools do build child environments from the ambient
  environment minus a prefix and pass them to spawns, at the exact functions the declaration
  names (`check-revision-binding.py:103-105/115`, `check-report-receipts.py:311-321/328`,
  `score-census-handoff-r32.py:786/489`, `mutants-btrfs-space-r30.py:362-364`,
  `run-receipt.py:36-40/52-102`). The five targets are real and the leak surface is real.
- **Sensitivity artifacts.** `MutAttrgetterCopy` and `MutPathCopy` reports/receipts are
  committed under `.ufo/waves/round-34/w2/`, so the after-conjunct references committed
  artifacts, not planned ones.

## Residual risk

1. If the freeze is cut with H1/H2 standing, the round's only instrument carries a lineage
   that omits two amendment clauses and a predicate the declaration does not print; the
   pre-freeze control receipts would score bytes the declaration misdescribes. This is
   repairable before the freeze with no data change.
2. M1/M2 are small but sit on the frozen surface (label, set, counting command); the freeze
   rule freezes exactly those, so they should be settled now rather than discovered after.
3. M3/M4 decide whether the C2 note's sourcing claim is true at the moment it is frozen and
   whether SOURCES stays append-only; both are wave-1/outcome actions, so the declaration
   should mark them as such now.
4. The before-value (>0 on each of the five) and after-value (0 on all five) are wave-1 and
   outcome work — not measured here. [inf] The before-value is reachable: the ambient-copy
   constructs and their spawns are confirmed at base.

## Verification gaps

- No `lsp` device is available in this seat's toolset, and LSP cannot serve historical blob
  revisions (`cefe752d`) in any case; definition/caller checks were done by reading the base
  blobs with `git show` plus grep. No current-tree production file was edited, so no
  diagnostics run was applicable.
- The probe's target sets were not executed here (the probe for `livefive` does not exist
  yet, and the before receipts are wave-1 control-seat work). No anti-duplication: I did not
  run any target set.
- The `MutAttrgetterCopy`/`MutPathCopy` receipts were verified as committed files only; their
  values were not re-run (mutation-tester work, wave 1).
- The census claim's exact run time `2026-10-24T02:26:45Z` is taken from the LOG; only the
  values (197 / 31 / exit 0 / `tsukuroi ok`) were reproduced by this seat's rerun
  (capture stamped 02:49:45Z).
- "Status otherwise empty" cannot be established during wave 1: sibling seat scratch is
  untracked by design and is committed by the L1.

## Repairs recommended before the freeze (ordered)

1. H2: paste the predicate sentence into the declaration.
2. H1: correct the counter lineage (VERSION 6 base + sha256; distinct new version).
3. M1: settle the label (`leaking`) vs measure key (`leaking_pairs`).
4. M2: declare or drop `--json` in the counting command.
5. M3/M4: mark S024/S198/lesson as wave-1 work and record the pin as a new/supersession row.
6. L1/L2: add the (3) pointer; fix the LOG heading's date basis.

Trailer: Report: `.ufo/waves/round-36/w1/ReviewDeclaration`
