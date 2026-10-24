# Append-block draft — target `corpus/knowledge/update-safety-note.md`, site `:420-424`

Seat: `ScribeNoUpgrade` (round 36, wave 1, routed repair 4).
Target (lane-relative): `corpus/knowledge/update-safety-note.md`
Site: lines 420-424 (the routed range) — the errata bullet it belongs to ends on line 425 (`did not name.`)
Base commit read: `6d76fb20f6ecbc940e5c8fff36c74060c885e161` (declaration); file digests below at `189d8a080ba8d508d5faab12cad9e688aee91dab`
Target sha256 at that commit: `8f2a7c188c6653f0510ccb0d09a8bcd0ef39eeb0dd4b1cb9cb3e628078952519` (544 lines)

## Landing instruction (for the L1)

**Append this block at the END of the file. Do not insert it at 420-424 and do not edit the
cited bullet.** Evidence (verified):

- `corpus/knowledge/freshness-recheck-r18.json` has 3 records on this path with baseline
  `842a5312...`; `check-appended-notices.py` requires `target_bytes.startswith(base_bytes)`
  (`NOTICE-HISTORY`). At `189d8a08` the property holds (base 518 lines, target 544 lines,
  first differing offset = start of line 519). Inserting at 420-424 breaks it.
- Inserting there would also shift this file's own line citations: `update-safety-note.md:481`
  and `:488` ("Superseded (`corpus/knowledge/update-safety-note.md:378-381`)") stay correct only
  under an EOF append; so do `pause-lift-gate-r24.md:82,92` (`:281-282`, `:280-284`) and
  `host-health-report-r3.md:168,304,317,322,353`.
- The operative `recheck:` line is the LAST one (`check-recheck-commands.py` `recheck_line()`),
  currently `:496`; the operative header trio is the last `source:`/`verified-at:`/`recheck:`,
  also `:494-496` (`check-knowledge-header.py`). **Do not add a `source:`, `verified-at:` or
  `recheck:` line at column 0 in the block** — see "Gate constraints" below.

## Verbatim original (quoted; NOT to be rewritten)

> - 2026-10-14 — **Round-1 row refinement, not a contradiction:** `SKILL.md:45`
>   names `HoldPkg = pacman glibc` under "pins/holds"; this note keeps the value
>   but splits it from the true version pins (`IgnorePkg`/`IgnoreGroup`/
>   `NoUpgrade`/`NoExtract`, all empty) and adds the second soft-trust surface
>   `LocalFileSigLevel = Optional` (`/etc/pacman.conf:16`), which the round-1 row
>   did not name.

(The routed range 420-424 stops at "which the round-1 row"; the bullet's last line is 425,
"did not name." The quote above is the complete bullet, lines 420-425.)

The defect: the phrase "the true version pins (`IgnorePkg`/`IgnoreGroup`/`NoUpgrade`/`NoExtract`,
all empty)" classifies `NoUpgrade`/`NoExtract` as version pins.

## Append block (paste at EOF, verbatim)

```markdown
## R36-SUPERSESSION — `NoUpgrade` / `NoExtract` are file-extraction rules, not version pins (2026-10-24)

Appended in round 36 as routed repair 4 (`corpus/lessons/round-35-verifier-spotcheck.md` §6 item 4).
The 2026-10-14 bytes above are preserved and remain the historical record; this block supersedes
one classification inside them. Prior locus (`:420-425`), verbatim:

> - 2026-10-14 — **Round-1 row refinement, not a contradiction:** `SKILL.md:45`
>   names `HoldPkg = pacman glibc` under "pins/holds"; this note keeps the value
>   but splits it from the true version pins (`IgnorePkg`/`IgnoreGroup`/
>   `NoUpgrade`/`NoExtract`, all empty) and adds the second soft-trust surface
>   `LocalFileSigLevel = Optional` (`/etc/pacman.conf:16`), which the round-1 row
>   did not name.

Superseded as a classification by `corpus/knowledge/pacman-backup-files-r35.md`
(§ `[obs] NoUpgrade and NoExtract (S191, S195)`; S191 pacman `lib/libalpm/add.c` at
54d94116164b, S195 pacman `doc/pacman.conf.5.asciidoc` at 54d94116164b): the version pins are
`IgnorePkg` / `IgnoreGroup` ("Instructs pacman to ignore any upgrades for this package when
performing a '--sysupgrade'." — S195 lines 102-104), while `NoUpgrade` / `NoExtract` name package
archive **file paths**: "All files listed with a `NoUpgrade` directive will never be touched during
a package install/upgrade" (S195 lines 136-137), "All files listed with a `NoExtract` directive
will never be extracted from a package into the filesystem" (S195 lines 147-148); the code skips
a `NoExtract` member (S191 lines 223-230) and turns a `NoUpgrade` member into `.pacnew`
(S191 lines 302-304, 338-350).

Replacement sentence (the same value claim, with the classification split):

> 2026-10-14 — **Round-1 row refinement, not a contradiction:** `SKILL.md:45` names
> `HoldPkg = pacman glibc` under "pins/holds"; this note keeps the value but splits it from the
> true version pins (`IgnorePkg`/`IgnoreGroup`, all empty) and from the file-extraction rules
> `NoUpgrade`/`NoExtract` (also empty, and not version pins), and adds the second soft-trust
> surface `LocalFileSigLevel = Optional` (`/etc/pacman.conf:16`), which the round-1 row did not
> name.

Values stand unchanged: all four directives are empty on this host (re-measured 2026-10-23 by
round-35 wave-1 `ExecHostPacnew`; re-measured read-only 2026-10-24T03:08:20Z — `/etc/pacman.conf`
carries no `IgnorePkg`/`IgnoreGroup`/`NoUpgrade`/`NoExtract` line, only `HoldPkg = pacman glibc`
at line 7). The superseding note records the same: "the values those entries recorded … stand"
(`corpus/knowledge/pacman-backup-files-r35.md:32`).
```

## Gate constraints this block respects (checked against the tool sources)

- No line starts with `recheck:`, `source:` or `verified-at:`, so the operative trio
  (`:494-496`) and the operative `recheck:` line (`:496`) are unchanged for
  `check-knowledge-header.py` and `check-recheck-commands.py`.
- The heading is new; it is not `## R18-FRESHNESS — sibling current-use restatements (2026-10-20)`
  (the only heading registered for this path in `freshness-recheck-r18.json`), so
  `NOTICE-HEADING-DUP`/`-BASE` cannot fire, and it is not one of the two
  `## R1[78]-RECHECK — steer-safe procedure` headings (`RECHECK-STEER-SAFE-INVALID`).
- The block begins with a `## ` heading, which terminates the operative steer-safe section
  (`## R18-RECHECK — steer-safe procedure`, `:532`, then `## R24 current-use notice (2026-10-22)`,
  `:542`). Its body — and therefore the section's command scan — is unchanged.
- The block's backticked spans are identifiers, not invocations; no `$ command` line appears, so
  the exec-log scanner (`R17-STEER-SCOPE`) has nothing to read even if this file were passed to
  it.

## Adjacent observation (not part of this repair)

`SKILL.md:45` in the quoted bullet no longer resolves to the Update-safety plane row it named on
2026-10-14: at `55b2186` (round 1) line 45 was `| Update-safety | …`, today `SKILL.md:45` is the
table separator `|---|---|---|---|---|` and that row is `SKILL.md:50` (`git show 55b2186:SKILL.md`,
`sed -n '45p'` vs `sed -n '45p;50p' SKILL.md`). Because the bullet is explicitly dated 2026-10-14
and this lane keeps historical locators, the replacement sentence above leaves it as-is; a re-pin
to `SKILL.md:50` would be a separate repair.
