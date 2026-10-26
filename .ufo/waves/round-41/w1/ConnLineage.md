VERDICT: draft

# ConnLineage — item X-4: round-41 counter lineage rows

Scope: extend `## Counter lineage — rounds 35-40` in `SKILL.md:3494-3522` with the two round-41
counters, per the table's own method (first-carrying commit on the master ancestry + sha256 at that
commit). Draft only — I am read-only on lane files and did not edit `SKILL.md`.

## Evidence (all measured this seat, read-only)

- **First-carrying commits (master ancestry).** `git log --diff-filter=A --format='%h %s' -- <tool>`
  names one commit for both tools: `e479fdc5 round-41: freeze C1/C2 counters, pinned sources, host
  capture, registry rows` — the freeze commit (`SCORECARD.md:2460-2461`), which is the declaration's
  "counters frozen at `e479fdc54d0977ccd8112a42d8d139baaebcb02e`".
- **Digest at that commit equals the frozen sha256.** `git show e479fdc5:<tool> | sha256sum`:
  - `tools/score-selftest-mounts-r41.py` → `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`
  - `tools/check-package-anatomy-r41.py` → `c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`
  Identical to the frozen digests declared in `SCORECARD.md:2465-2466` and `SKILL.md:3120-3121`, and
  to the bytes at HEAD (`sha256sum` at `71851d6`; no post-freeze amendment).
- **Non-ancestor refs.** `git log --all` adds `4bf47d08`, `75d08364`, `fbcc8624` with empty
  descriptions; none is an ancestor of master (`git merge-base --is-ancestor` → no) and each holds a
  byte-identical blob (`8306d999…`) — snapshots, not divergence (same pattern the section already
  records for the round-40 pair, `SKILL.md:3506-3511`).
- **Defect closed.** Both counters close the round-40 closure's routed defect R40-ANSWER-KEY
  (`corpus/lessons/round-40-verifier-spotcheck.md:141-146`): C1 — a one-line `declare -f`/`${0}`/
  `${BASH_ARGV0}` prologue passing the round-40 predicate with no fixture, plus held-out H5/H6/H9 and
  §6.2 counter-side fixes; C2 — the token-list writer and non-negated false rules scoring 8/8.
  Docstrings: `tools/score-selftest-mounts-r41.py:2-29`, `tools/check-package-anatomy-r41.py:2-36`.
- **Bypass still admitted.**
  - C1: "A self-reader that skips here-documents is not refused (recorded limit)"
    (`tools/score-selftest-mounts-r41.py:13`); the declaration carries the same limit and names the
    wave attack: "a self-reader that strips here-documents before grepping is not refused by the decoy
    (wave item C1CritDecoy attacks it)" (`SCORECARD.md:2492-2493`). Controls: K1/K3 prologue variants
    FAIL with `decoy_pass 0` (`controls/C1-K1-declare-f-prologue-on-base.jsonl`,
    `controls/C1-K3-declare-f-prologue-on-candidate.jsonl`); K2 candidate without the no-`subvol=`
    case FAIL (`params 3`, H9 survives, `controls/C1-K2-candidate-without-H9-case.jsonl`); K4 after
    receipt at implementation commit `568c397d` PASS (`after/c1-after-568c397.jsonl`,
    `SCORECARD.md:2491-2492`).
  - C2: "A writer that concatenates the RELATIONS literals and the derived values still passes every
    lexical check (the recorded bypass); the verdict files are the read, the lexical checks are shape
    gates" (`tools/check-package-anatomy-r41.py:21-22`); declared the same way
    (`SCORECARD.md:2468-2471`). Control C2-K2 confirms it: `rules_verified 8, verdicts_ok 0`, FAIL
    (`controls/controls-c2.jsonl`).
- **Class recurrence across rounds 35-41.** The section's own taxonomy:
  "a pass that a non-reading, single-literal or fixture-gated arm also reaches" (`SKILL.md:3549-3552`).
  For C2 this class returns by design (lexical gates remain passable; the read moved to committed
  reviewer verdict files, QUALITY 81). For C1 the round-40 self-reading-prologue class returns only in
  the here-doc-skipping variant; the fixture-monoculture/single-literal family is countered by the
  four-shape fixture capture and the thirteen varied mutants, with the round-40 "mutant sample, not
  proof of immunity" caveat still applying to the sample scope.

## Draft — exact rows for `SKILL.md` "## Counter lineage — rounds 35-40" table

```markdown
| 13 | `tools/score-selftest-mounts-r41.py` | r41 | `e479fdc54d0977ccd8112a42d8d139baaebcb02e` | `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c` | Closes R40-ANSWER-KEY for C1 (`corpus/lessons/round-40-verifier-spotcheck.md` §6.1; QUALITY 88) and the held-out survivors: 13 frozen mutants (round-40 M1-M9, H5, H6, H9, new count-direction H10) applied as exact substring replacements to the census `run_selftest` mount-table arms, three neutral rewrites N1-N3, one DECOY carrying every mutant's replacement text inside a dead `: <<'R41DECOY'` here-document in `probe_storage_arm`, kill attribution (a baseline case label failing, twice), one serial retry per failed non-mutant run, and a fixture capture of the four declared table shapes (mountpoint not absolute, source not under `/dev`, no `subvol=` option, two btrfs lines); predicate `baseline_pass == 1 and neutral_pass == 3 and decoy_pass == 1 and mutants_applied == 13 and survivors == 0 and params == 4` | Live in round 41. Pre-data controls K0-K4 (`SCORECARD.md:2483-2493`): K1/K3 self-reading `declare -f` prologue FAIL (`decoy_pass 0`, survivors 13), K2 candidate without its no-`subvol=` case FAIL (`params 3`, H9 survives), K4 after receipt at implementation commit `568c397d` PASS (survivors 0, params 4). Recorded limit, attack carried into this wave: a self-reader that strips here-documents before grepping is not refused by the decoy (`SCORECARD.md:2492-2493`; wave item C1CritDecoy); the mutant sample still covers only the mount-table cross-check arm, cf. round-40 "mutant sample, not proof of immunity" (`SKILL.md:3379`). Same defect class across rounds 35-41: the self-reading-prologue family returns in the here-doc-skipping variant; the fixture-monoculture/single-literal family (R39-FIXTURE-MONOCULTURE) is addressed by the four-shape capture |
| 14 | `tools/check-package-anatomy-r41.py` | r41 | `e479fdc54d0977ccd8112a42d8d139baaebcb02e` | `c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f` | Closes R40-ANSWER-KEY for C2 (`corpus/lessons/round-40-verifier-spotcheck.md` §6.1; QUALITY 81, 87, 88): PA1-PA8 on rows S227-S236 opened 2026-10-26, each rule carrying its frozen proposition RELATIONS, quoted inside the row's frozen source window on a mined upstream row, no negation word, value derived from the pinned snapshot, six host values from the frozen capture, and a per-row committed reviewer VERDICT file (`w1/C2RevPA<n>*.md`, first line `VERDICT: holds|partly|fails`; a row counts with >=1 holds and 0 fails); predicate `rules_verified == 8 and verdicts_ok == 8 and host_ok == 6 and source_ok == 1 and duplicate_rows == 0 and duplicate_headings == 0 and novelty_base_hits == 0` | Live in round 41. Pre-data controls K0-K8 (`controls/controls-c2.jsonl`): K2 relation-literal writer without verdicts scores `rules_verified 8, verdicts_ok 0` (FAIL) — the recorded lexical bypass; K5 one `fails` verdict → 7; K6 no verdicts → 0; K7 `partly`-only → 7; K8 candidate PASS. The lexical checks stay declared shape gates (`SCORECARD.md:2468-2471`, `tools/check-package-anatomy-r41.py:21-22`): a writer that concatenates the frozen RELATIONS literals and the derived values still passes them — the read is the per-row verdict files. Same defect class across rounds 35-41: yes — the non-reading/literal-writer family (R38-C2-COUNTER-GAPS, R39-CONTENT-UNREAD) recurs in lexical form by design; the read is displaced to human verdict files, not eliminated |
```

Numbering note: rows 13-14 continue the rounds 35-40 table's own numbering (1-12); the predecessor
table above (rounds 30-34, rows 13-20) is a separate table and is left untouched — append-only.

Suggested closing annotation (mirrors the section's existing class-recurrence paragraph):

```markdown
Round-41 wave note (drafted by seat ConnLineage, item X-4): rows 13 and 14 both close the routed defect
R40-ANSWER-KEY, and both still admit a named bypass. For row 13 the admitted bypass is a self-reader
that strips here-documents before grepping (decoy skipped; SCORECARD.md:2492-2493, wave item
C1CritDecoy). For row 14 it is the relation-literal writer passing the lexical shape gates (control
C2-K2, rules_verified 8) — a declared continuation of the rounds 35-40 family, with the read carried by
the per-row verdict files. Read either row with its key: the C1 kills are behaviour-only for the
mount-table cross-check surface, and the C2 lexical pass is not a content read.
```

## Not done

- No counter runs (not needed for a lineage draft; the declared freeze digests and control receipts are
  the anchors). I did not run `score-selftest-mounts-r41.py` / `check-package-anatomy-r41.py`.
- No lane file edited; no `git`/`jj` mutation; nothing written outside this report.
- No tool installs (none needed).
