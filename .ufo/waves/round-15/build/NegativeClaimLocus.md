# NegativeClaimLocus — round 15 scout report (C1 depth)

Seat: TsukuroiR15.NegativeClaimLocus (scout, read-only research, leaf).
Assigned target: Locate exact prior docs "no further values" assertion and supplemental reader lines in r14 MD/JSON; give precise affected loci.

## 1. Summary & Verification Verdict

The round-14 verifier spot-check (`corpus/lessons/round-14-verifier-spotcheck.md` § Adjudicated concerns and routing, items 1-2, lines 233-247) identified two status-neutral documentation debts:
1. **Supplemental reader lines:** Unqualified "rendered lines 1266-1267" for S044 (`systemd.exec(5)`), which vary across renderers/readers (in the verifier's reader, lines 1266-1267 discuss AF_UNIX sockets, whereas `ProtectSystem=` is at line 1270, definition at 1272-1273).
2. **Negative absence assertion:** Asserting "documents no further values for this option" / "The opened revision documents no further values for `ProtectSystem=`" without a recorded command-and-date sweep or parser proof.

The primary quote (`Takes a boolean argument or the special values "full" or "strict".`, 11 whitespace words) and the positive documented domain are exact, verified, and remain fully supported. The historical stable heading `SANDBOXING > ProtectSystem=` remains valid. Only the supplemental unqualified renderer line locators and unsupported negative absence claims require supersession.

## 2. Precise Affected Loci

### A. Supplemental Reader Lines (`rendered lines 1266-1267`)
1. **`corpus/knowledge/source-scope-correction-r14.md:34`**
   - Locus: Section `## R14-VALUE-DOMAIN`, Source object paragraph.
   - Text: `Source object: S044, \`systemd.exec(5)\` § ProtectSystem= (under SANDBOXING), rendered lines 1266-1267, page footer systemd 262.1, opened 2026-10-20.`
   - Defect: Unqualified reader line numbers `rendered lines 1266-1267`.

2. **`corpus/knowledge/source-scope-correction-r14.json:13`** (`corrections[0].location`)
   - Locus: `corrections[0]` (`R14-VALUE-DOMAIN`).
   - Text: `"location": "systemd.exec(5) § ProtectSystem= (SANDBOXING), rendered lines 1266-1267; page footer systemd 262.1; opened 2026-10-20"`
   - Defect: Supplemental locator contains `rendered lines 1266-1267`.

3. **`corpus/knowledge/source-scope-correction-r14.json:167`** (`sources[0].anchor`)
   - Locus: `sources[0]` (`S044`).
   - Text: `"anchor": "§ ProtectSystem= (SANDBOXING), rendered lines 1266-1267; footer systemd 262.1"`
   - Defect: Anchor metadata cites `rendered lines 1266-1267`.

4. **`corpus/knowledge/source-scope-correction-r14.md:178`** (`QUALITY check` item 2)
   - Locus: Evaluated anchor in author-side QUALITY check table.
   - Text: `S044 URL, section, rendered lines and footer; S045 comment id, fields, timestamps and body fragments.`

### B. Negative Claim: "no further values"
1. **`corpus/knowledge/source-scope-correction-r14.md:41-42`**
   - Locus: Section `## R14-VALUE-DOMAIN`, **Proposition supported** block.
   - Text: `**Proposition supported:** the documented input forms for this option are a boolean argument and the special values \`full\` and \`strict\`. The opened revision documents no further values for \`ProtectSystem=\`.`
   - Defect: Second sentence (`The opened revision documents no further values for \`ProtectSystem=\`.`) asserts negative absence without an attached command/date search sweep.

2. **`corpus/knowledge/source-scope-correction-r14.md:51-53`**
   - Locus: Section `## R14-VALUE-DOMAIN`, **Replacement** block.
   - Text: `“The opened revision documents \`ProtectSystem=\` as taking a boolean argument or the special values \`full\` and \`strict\`, and documents no further values for this option. ...”`
   - Defect: Embedded clause `and documents no further values for this option.`

3. **`corpus/knowledge/source-scope-correction-r14.json:15`** (`corrections[0].replacement`)
   - Locus: `corrections[0]` (`R14-VALUE-DOMAIN`), `replacement` field.
   - Text: `"replacement": "The opened revision documents ProtectSystem= as taking a boolean argument or the special values full and strict; that is the documented value domain, and it documents no further values for this option. ..."`
   - Defect: Clause `and it documents no further values for this option.`

## 3. Preserved True Statements (NOT Defective)

1. **Exact 11-word Quote:** `Takes a boolean argument or the special values "full" or "strict".`
2. **Stable Heading Locator:** `SANDBOXING > ProtectSystem=`, definition paragraph.
3. **Domain vs Mechanism Distinction:** `boolean`, `full`, `strict` are the documented option domain; other-mechanism list (`BindReadOnlyPaths=`, `TemporaryFileSystem=` with `ro`, `RootDirectory=`/`RootImage=`) is illustrative lane scope `[inference]`.

## 4. Recommendations for C1 Pair

1. **R15-LOCATOR:** Supersedes `source-scope-correction-r14.json:13`, `:167`, and `source-scope-correction-r14.md:34`. Active locator is `systemd.exec(5) § SANDBOXING > ProtectSystem= (stable heading), page footer systemd 262.1`. Unqualified reader lines withdrawn.
2. **R15-POSITIVE-DOMAIN:** Supersedes `source-scope-correction-r14.md:41-42`, `:51-53`, and `source-scope-correction-r14.json:15`. Active replacement defines domain positively: `Takes a boolean argument or the special values full or strict.` Avoid negative absence language (`documents no further values`).
3. **Additive Notices:** In r14 MD append `## R15 supersession (2026-10-20) — locator and positive-domain notices`. In r14 JSON append `r15_supersession` key. Preserve historical baseline text.

## 5. Sources, Limits & Tools

- **Sources:** `corpus/lessons/round-14-verifier-spotcheck.md`, `corpus/knowledge/source-scope-correction-r14.{md,json}`, `corpus/SOURCES.md`, `tools/check-locator-clarification.py`.
- **Limits:** Read-only research. No verification runs or tests executed. No host mutations.
- **Tools:** read, grep, glob. Installs/updates: none.
