
## Round-49 coverage note (appended 2026-10-28)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-46 notes above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/btrfs-scrub-grounding-r45.md` (round-49 depth admission, GR1-GR3) | The seven corrections the round-48 counted cohort named are in the row bytes and the five defect strings it named are gone: GR1's `0X` prefix and its host-reading inference mark, and GR2's `is_valid` gate, cancel-sentence subject, suspend-path range and effects, `ioctl.c:3132` citation and `-ENODEV` devid case. A fresh cohort of one wave (18 seats: three reviewers and three critics per row) re-reads the corrected rows `holds` with pairwise distinct bodies, every `**Quote.**` line resolves on its digest-pinned snapshot, and each row extent is pinned by sha256 at the freeze (GR1 `3a2ba180…`, GR2 `d4296085…`, GR3 `43430a14…`; `## GR<n>` to the next `## ` heading, no inner heading) | S246-S249 (Linux v7.2.11, systemd v262); `corpus/knowledge/btrfs-scrub-grounding-r45.md:277-287`; `.ufo/waves/round-49/frozen/FROZEN.md`; counter `tools/check-scrub-admission-r49.py --revision <REV>` |
| `../PROVINCE.md` `## Adjacent — finding-to-owner handoffs` (round-49 C2) | The seven **Ownership source** cells cite portable `OUT-0NN` anchors (ADJ-01 → OUT-002, ADJ-02 → OUT-003, ADJ-03 → OUT-004, ADJ-04 → OUT-005, ADJ-05 → OUT-006 and OUT-007, ADJ-06 → OUT-008 and OUT-009, ADJ-07 → OUT-010) instead of sibling `*.md:N-M` ranges, of which 9 occurrences stood at the base and 0 remain in those cells. Each cited anchor carries its ADJ class, a pinned sibling `PROVINCE.md` commit, an `# …` heading and a ≤25-word quote, with the blob sha256 in the round-19 registry. Finding classes, retains, recipients and handoff evidence are unchanged, and the withdrawn ranges survive only as history in the PROVINCE round-49 note | `../PROVINCE.md:108-130` (anchor table), `:296-320` (round-49 note), `:46-52` (ADJ rows); `knowledge/adjacency-anchors-r19.json`; counter `tools/check-adjacency-table-r49.py --revision <REV>`, cross-check `tools/check-adjacency-anchors.py` |
| `../tools/tsukuroi-census.sh` (`selftest_base_dir` / `run_selftest`, round-49 C3) | Descriptor-band exhaustion is named, not silent: the resolver records `ST_BASE_ERR` (`fd-band`, `dirty-missing`, `alias-open`, `alias-not-dir`), `run_selftest` prints `selftest: fd band 240-249 exhausted (every descriptor already open), cannot alias TMPDIR <…>; no /tmp fallback (R49-C3)` on stderr and returns 1, and the stale `builds a /tmp fixture tree` comment is gone. One new case `(R49-C3)` pins the exhausted-band path under a narrowed two-descriptor band: `--selftest` now ends `PASS (167 cases, 167 passed, 0 failed)`, 166 at the base. `+56/−9` in nine hunks, all inside the hermetic-selftest surface; probe arms, verdict vocabulary and exit map untouched (Frontier notice below) | S255 (GNU bash 5.3 reference, `Redirections`, the fd>9 caveat); S252 and S253 (the `$TMPDIR` base contract of rounds 47-48); counter `tools/check-fd-band-r49.py --revision <REV>` |

### Frontier notice — round 49

Frontier: nothing moves, on either moved surface.

C2 changes a locator class, not ownership. The seven ownership cells gained `OUT-0NN` anchors and lost their
bare ranges (`../PROVINCE.md:296-320`); the anchor table itself is unchanged since round 19 (`:108-130`), the
finding classes, retains, recipients and evidence columns are unchanged, and ADJ-06 still names both OUT-008
(kaidoku) and OUT-009 (revenger) while the round-49 note keeps that arbitration open (`:314-315`), so the
contested-ownership bullet (`:33-34`) stays as written. An anchor pins a sibling commit, its heading and a
≤25-word quote: a snapshot of what that sibling declared, not a recipient-side acknowledgement, so the
replay/acceptance bullet (`:30-32`) gains nothing either. No census arm reads the adjacency table or the
anchor registry — the census carries a round-32 `HANDOFF ADJ-04` line that publishes counts its own probes
already measured, and it never opens `PROVINCE.md` or `knowledge/adjacency-anchors-r19.json` — so the round-26
promotion rule (`:243`) does not fire and adjacency stays a handoff surface, not new host ground. One limit
stays named: the registry keeps OUT-001's round-19 `province_pointer` as a `PROVINCE.md:6-16` range and no ADJ
row cites OUT-001, so the range leg is scoped to the seven ownership cells and never sees that row.

C3 does not change the census contract. The BASE→FREEZE diff of `../tools/tsukuroi-census.sh` is `+56/−9` and
every hunk sits in the hermetic-selftest surface: the header comment (`:415-417`), the `--selftest` usage text
(`:606-609`), `selftest_base_dir` (`:2076-2097`), the base-failure branch of `run_selftest` (`:2112-2122`) and
the new `(R49-C3)` case (`:3574-3601`). No probe arm changes, and no verdict token or exit-map entry changes:
`git diff <BASE> <FREEZE> -- tools/tsukuroi-census.sh | grep -E 'TSUKUROI_CENSUS:|HEALTHY|DEGRADED|BLOCKED'`
matches nothing, so the four-plane contract, the rollup and the 0/1/2 exit map (`corpus/README.md:12`) stand as
written. What moves is the `--selftest` receipt — 166 → 167 cases, plus a named stderr diagnostic where the
resolver used to fail without a word — and that is a test surface, not a reading of the host. Two limits stay
named. The new `SELFTEST_FD_BAND` override (`:2082`) is an unvalidated environment input read only by
`selftest_base_dir`, whose only production caller is `run_selftest` (`:2112`), so it can narrow the alias band
in a test and never reaches a probe arm. And no current `SKILL.md` line declares either count — the highest one
it declares is the `154 cases` line inside the round-45 census-readers block (`SKILL.md:4259`) — so this note
records the count without asserting a SKILL expectation.

C1 admission: `corpus/knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3 are admitted round 49 — the fresh
18-seat w1 cohort re-read the corrected rows `holds` with distinct bodies and the frozen counter passes all
six legs — so the rows leave the pending state that the round-45 and round-46 gate sections recorded.
