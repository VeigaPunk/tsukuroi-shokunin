# Append-block draft — target `SKILL.md`, site `SKILL.md:397-399`

Seat: `ScribeNoUpgrade` (round 36, wave 1, routed repair 4).
Target (lane-relative): `SKILL.md`
Site: lines 397-399 (three-line bullet, one sentence)
Base commit read: `6d76fb20f6ecbc940e5c8fff36c74060c885e161` (declaration); file digests below at `189d8a080ba8d508d5faab12cad9e688aee91dab`
Target sha256 at that commit: `f4d7c9d918688130883d1f7684c0f9b842e12608ee288efb78bb260894696def`

## Landing instruction (for the L1)

**Append this block at the END of `SKILL.md`. Do not insert it at line 397-399 and do not edit
the three cited lines.** Evidence for that constraint (verified, not inferred):

- `tools/check-appended-notices.py` `_record_findings` requires `target_bytes.startswith(base_bytes)`
  against the r18 registry baseline `842a5312b704b5cda10fd80ec1fdee5fb381ba97`
  (`corpus/knowledge/freshness-recheck-r18.json`), else finding `NOTICE-HISTORY`. 11 of the
  registry records target `SKILL.md`. At `189d8a08` `SKILL.md` satisfies the prefix property
  (base 1916 lines, target 3009 lines, `head.startswith(base)` True; first differing offset =
  168208 = start of line 1917). A 3-line insert at line 397 makes it False.
- `tools/check-adjacency-anchors.py` `inbound` records pin `SKILL.md` line numbers:
  `IN-023` (`SKILL.md:101,404,755,842`, found_line 755) and `IN-042`
  (`SKILL.md:101,404,427,734-756`, found_line 427). Simulated 3-line insert at 397 moves
  `` `walker-restart.hook` `` from 404 to 409 and `Cross-domain: …` from 427 to 432 → the
  `found_line` values stop being occurrences of `evidence_quote`.
- `tools/check-self-assessment.py` K08/K09 read the depth row (last `## Axes — ` section,
  `SCORECARD.md:1570`): it states `SKILL.md` 3009 `wc -l` and 784 pipe-prefixed lines, both
  true at `189d8a08`. This block adds lines but no line starting with `|`, so only the `wc -l`
  figure moves; the round-36 axes depth row must state the new number.

## Verbatim original (quoted; NOT to be rewritten)

> - `HoldPkg = pacman glibc` is removal-protection, **not a version hold**; true
>   pins are `IgnorePkg` / `IgnoreGroup` / `NoUpgrade` / `NoExtract` — all empty
>   (`:204-222`).

The defect: the sentence groups `NoUpgrade` / `NoExtract` with `IgnorePkg` / `IgnoreGroup` under
"true pins" (package version pins). The recorded values are correct and are not in dispute.

## Append block (paste at EOF, verbatim)

```markdown
## Round 36 — `NoUpgrade` / `NoExtract` are file-extraction rules, not version pins (supersedes `SKILL.md:397-399`)

Appended in round 36 as routed repair 4 (`corpus/lessons/round-35-verifier-spotcheck.md` §6 item 4).
The historical bullet at `SKILL.md:397-399` is preserved unchanged; this block supersedes its
**classification only**.

Prior locus (`SKILL.md:397-399`), verbatim:

> - `HoldPkg = pacman glibc` is removal-protection, **not a version hold**; true
>   pins are `IgnorePkg` / `IgnoreGroup` / `NoUpgrade` / `NoExtract` — all empty
>   (`:204-222`).

Superseded as a classification by `corpus/knowledge/pacman-backup-files-r35.md`
(§ `[obs] NoUpgrade and NoExtract (S191, S195)`), whose sources are S191 pacman
`lib/libalpm/add.c` at 54d94116164b and S195 pacman `doc/pacman.conf.5.asciidoc` at
54d94116164b (`corpus/SOURCES.md:197` and `:201`):

- the version pins are `IgnorePkg` / `IgnoreGroup` — "Instructs pacman to ignore any upgrades for
  this package when performing a '--sysupgrade'." (S195 lines 102-104; group form S195 lines 106-109);
- `NoUpgrade` / `NoExtract` act on package-archive **file paths**, not on package versions:
  "All files listed with a `NoUpgrade` directive will never be touched during a package
  install/upgrade" (S195 lines 136-137) and "All files listed with a `NoExtract` directive will
  never be extracted from a package into the filesystem" (S195 lines 147-148). In the code,
  `NoExtract` skips the member outright (S191 lines 223-230), `NoUpgrade` leaves an existing
  target untouched (S191 lines 302-304) and the incoming file is written as `.pacnew` with the
  warning `warning: %s installed as %s.pacnew` (S191 lines 338-350).

Replacement sentence:

> - `HoldPkg = pacman glibc` is removal-protection, **not a version hold**; the true
>   version pins are `IgnorePkg` / `IgnoreGroup` — all empty — while `NoUpgrade` /
>   `NoExtract` are file-extraction rules, not version pins (also empty) (`:204-222`;
>   classification per `corpus/knowledge/pacman-backup-files-r35.md`, S191/S195).

Values stand unchanged: `IgnorePkg`, `IgnoreGroup`, `NoUpgrade` and `NoExtract` are all empty on
this host (re-measured 2026-10-23 by round-35 wave-1 `ExecHostPacnew`,
`.ufo/waves/round-35/w1/ExecHostPacnew/capture.txt:76-97`; re-measured read-only
2026-10-24T03:08:20Z: `/etc/pacman.conf` carries no `IgnorePkg`/`IgnoreGroup`/`NoUpgrade`/
`NoExtract` line — only `HoldPkg = pacman glibc` at line 7 — and `pacman-conf` prints nothing
for each of the four keys, rc=0).
```

## Block size (for the round-36 depth row)

The fenced text above is the exact text to append (one trailing newline). Its line count is in
`INDEX.md`; it contains no line starting with `|`, so the K09 table-line count is unchanged.
