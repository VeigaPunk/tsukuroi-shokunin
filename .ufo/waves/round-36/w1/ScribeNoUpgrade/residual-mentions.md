# Residual `NoUpgrade` / `NoExtract` mentions outside the routed four sites

Finding only — no draft blocks for these; the routed repair 4 scope is exactly four sites
(`SKILL.md:397-399`, `corpus/knowledge/update-safety-note.md:420-424`,
`corpus/knowledge/update-safety-v2.md:52` and `:198`). Listed so the L1 can decide, because the
round-35 verifier spot-check's own quality verdict was that "the supersession sweep did not reach
every mention" (`corpus/lessons/round-35-verifier-spotcheck.md:82`).

Measured at lane head `189d8a08` with
`grep -rn 'NoUpgrade\|NoExtract' SKILL.md corpus/knowledge/ | grep -v 'pacman-backup-files-r35.md'`.

## A. Loci that still classify the four directives together as pins/holds (same defect class)

| Locus | Verbatim | Why it is the same class |
|---|---|---|
| `corpus/knowledge/update-safety-note.md:346` | `\| 4 \| pins/holds declared \| \`pacman-conf IgnorePkg IgnoreGroup NoUpgrade NoExtract\` \| all empty; \`HoldPkg = pacman glibc\` (removal-only) \| **PASS** (with §4 misread warning) \|` | the decision-table row is labelled `pins/holds declared` and probes all four together |
| `corpus/knowledge/degraded-triage-r4.md:392` | ``no pins/holds (`pacman-conf IgnorePkg IgnoreGroup NoUpgrade NoExtract` → none; only HoldPkg).`` | states the four-directive probe as the `pins/holds` test |
| `corpus/knowledge/update-safety-note.md:204`+`:212` | heading `## 4. Pins and holds — measured, plus what \`HoldPkg\` does not mean [observed]`, row `\| any \| \`pacman-conf NoUpgrade\` / \`NoExtract\` \| **empty** \|` | the section heading groups the two file directives under "Pins and holds"; the row itself asserts only "empty" |

## B. Loci that merely list the four keys (no classification claim)

- `corpus/knowledge/update-safety-v3.md:264` — `IgnorePkg/IgnoreGroup/NoUpgrade/NoExtract all empty` (standing rows).
- `corpus/knowledge/degraded-triage-r4.md:382-383` — ``no `IgnorePkg/IgnoreGroup/NoUpgrade/NoExtract/HookDir` keys at all`` (key inventory).
- `corpus/knowledge/host-health-report-r3.md:509` — `pacman-conf IgnorePkg IgnoreGroup NoUpgrade NoExtract; pacman-conf HoldPkg` (probe list).

## C. Correct as written (checked, no action)

- `corpus/knowledge/package-state-plane.md:27-28` — `` `pacman-conf IgnorePkg` / `IgnoreGroup` print empty — no pins/holds beyond `HoldPkg`. Nothing here blocks an `-Syu` of any package.`` probes only the two version pins.

## Verbatim conflict to report to the judge

`corpus/lessons/round-35-verifier-spotcheck.md:82` says: "One defect kept it short of stronger: the
supersession sweep did not reach every mention (routed defect 5)." But §6 of the same file numbers
the NoUpgrade correction sweep as **item 4** (`:90`) and gate-timing discipline as item 5 (`:92`).
The round-36 declaration (`SCORECARD.md:1669-1672`) and this seat's prompt both call the sweep
repair **(4)**, matching §6. The §5 cross-reference is off by one.
