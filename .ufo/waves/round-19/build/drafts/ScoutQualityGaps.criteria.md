# QUALITY criteria 31–33 — draft append (round 19)

Read 2026-10-20. Target file `corpus/QUALITY.md`: criteria 1–30 occupy lines 3–40; criterion 30 is
the last line (`corpus/QUALITY.md:40`). The text below is written for verbatim append after line 40,
preserving lines 1–40 byte-for-byte (QUALITY4 append-only). No renumbering of 1–30.

Provenance limit: `corpus/lessons/round-19.md` does not exist at read time (glob of `corpus/lessons/`
returns round-1…round-18 plus verifier files). The three `Lesson:` citations use the row ids confirmed by
the round-19 lesson author (ScoutMistakes, this wave): `R19-SEAT-DECLARE`, `R19-ADJ-POINTERS`,
`R19-BOOT-ATTRIBUTION`. The lesson file must land those ids with these criteria, or the L1 maps the ids and
keeps the evidence anchors, which are all committed bytes today. A QUALITY criterion whose only support is
an unlanded lesson row is not admissible; none of the three is in that state.

## Proposed appended text

31. **Seat execution class is fixed at dispatch (R19-SEAT-DECLARE):** every dispatched item names its
    execution class before delivery — `EXEC-AUTHORIZED` with the exact commands, or `NO-EXEC` with
    read/grep/glob only and the literal trailer `Scope: executed=none`. A wave is green only when
    `tools/check-seat-scope.py` at the landed revision reports zero `EXEC-UNAUTHORIZED`, `SCOPE-UNDECLARED`
    and `TRAILER-MALFORMED` for build and falsify, and `REPORT-MISSING` only for seats recorded dead with
    their provider outcome (QUALITY29). Authorization added after delivery,
    reclassifying a disclosed command as read-only, or rewriting a trailer does not clear the seat; the
    deviation stays recorded. Falsified by: dispatching any item with no class, or an `EXEC-AUTHORIZED`
    item whose report lists an unlisted command, and the gate not exiting non-zero. Lesson:
    `corpus/lessons/round-19.md` § Mistakes, R19-SEAT-DECLARE (scope); baseline red
    `round-18-verifier-spotcheck.md:256-259` (build 37/1/4/2, falsify 9/0/0/2).

32. **Sibling ownership is cited by portable anchor, not line range (R19-ADJ-PORTABLE):** each of the 10
    outbound ownership pointers in `PROVINCE.md` (:33, :46-52) publishes the pinned sibling commit, the
    exact heading, an exact ≤25-word quote and the sibling blob sha256; each inbound sibling pointer into
    a lane file carries a found_line and a RESOLVES/DRIFTED/UNRESOLVABLE class. A bare `path:N-M` is not a
    locator: it is red when the quote is absent from the pinned blob even if the range still holds text,
    and a quote found at another line is DRIFTED and handed to the owner, never repaired in the sibling.
    Falsified by: moving the quoted sentence one paragraph, or advancing the sibling commit — the anchor
    must still resolve by quote plus blob while the line range alone misses it. Lesson:
    `corpus/lessons/round-19.md` § Mistakes, R19-ADJ-POINTERS (reference-drift); live drift
    `round-18-verifier-spotcheck.md:269-270` (mori `PROVINCE:66` → tsukuroi ADJ-04 now `PROVINCE:49`);
    the drift warning already sits at `PROVINCE.md:70-73`.

33. **Known `/boot` writers are attributed before a write is a finding (R19-BOOT-ATTRIBUTION):** a boot-plane
    audit reports a `/boot/limine.conf` write only with writer class, mechanism file:line, unit/hook
    identity and event timestamp. Known scheduled writers are the `snapper-cleanup.service` drop-in
    `ExecStopPost=limine-snapper-sync` (`host-capture-r19.txt:256-260`) under `snapper-cleanup.timer`
    `OnUnitActiveSec=1h` (:221-231), the snapper plugin's transient `limine-snapper-add-*` `systemd-run`
    units (`host-capture-r19b.txt:1093-1245`), and pacman's `90-mkinitcpio-install.hook` →
    `limine-mkinitcpio-install` (`host-capture-r19.txt:346-409`; writes :3015,3047). A write matching a
    known writer is expected automation, not evidence of interference; an unattributed unit, a failed
    run, or a write without a matching timer or hook remains a finding. Falsified by: filing the hourly
    10:07–17:07 `snapper-cleanup.service` writes (`host-capture-r19c.txt:13-20`) as unexplained, or the
    audit still attributing those writes after the drop-in and timer are removed. Lesson:
    `corpus/lessons/round-19.md` § Mistakes, R19-BOOT-ATTRIBUTION (stale-premise/attribution); round-18
    recorded the rewrite as expected automation at `round-18-verifier-spotcheck.md:206-208,271-273`.

## Gate mapping

| Criterion | Measured by | Red condition |
|---|---|---|
| 31 | `tools/check-seat-scope.py --revision <landed hex>` over build and falsify registries | any declaration counter > 0, or a missing report not reconciled as a dead seat |
| 32 | `tools/check-adjacency-anchors.py` over `PROVINCE.md` plus the inbound census | `outbound_portable` < 10 or an anchor quote not found in its pinned blob, or an inbound row without `found_line`/class |
| 33 | `tools/check-boot-writers.py` over the round-19 captures | `attributed_events` < 12, or an event without writer class + mechanism file:line + unit identity + timestamp |

## Relationship to existing criteria

- 31 tightens 24 (seat-side execution scope) at the dispatch boundary; 24 still governs what happens
  inside a dispatched seat.
- 32 extends 21 (portable locators) from external sources to cross-lane ownership pointers; line numbers
  remain permitted as supplements, not as the locator.
- 33 adds write-event attribution for `/boot`; 25 (next-boot verdict from images) is untouched — an image
  verdict is not a write-event verdict.
- Appending after :40 does not disturb inbound pointer IN-047, which cites `corpus/QUALITY.md:40` (30):
  lines 1–40 are unchanged, so the sibling sentence keeps resolving.

## Rejected candidates (retained)

- **Registry-membership criterion** (every gate must have a row): rejected as redundant. C3's
  `tools/check-registry-coverage.py` measures the 13-row/14-file gap directly (lesson row R19-REGISTRY-ROW);
  a QUALITY rule would restate the count, not add a falsifiable behavior, and round-18 offered a legitimate
  alternative (state that `_revision.py` is not a gate and drop it from the tally).
- **Exec-log universal coverage** (every host-touching read must appear in the harness log): rejected as
  unverifiable (lesson row R19-EXECLOG-BOUND). A rule cannot prove a log contains a read that was never
  captured; the honest form is the round-18 §5.3 bound — bind the reads that exist and state the bound
  wherever a zero is cited.
