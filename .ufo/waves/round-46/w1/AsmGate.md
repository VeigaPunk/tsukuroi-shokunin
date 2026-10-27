VERDICT: defect-found

## F-9 assimilation evaluation

### Quarantine slice
- The required awk extraction was run against `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`; its exact output is in `.ufo/waves/round-46/w1/AsmGate/quarantine-slice` (12 lines). It is a derived slice, not evidence that any staged row is safe to assimilate without checking.

### Staged IDs and collisions
- Registry IDs were extracted from the frozen lane revision `a44770491eb5ca15ce9f8b3207309d1af683ffaf:corpus/SOURCES.md` with `grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}'`; saved to `.ufo/waves/round-46/w1/AsmGate/reg-ids` (251 matches).
- Staged IDs were extracted from merge `SOURCES.append.md` using the same expression; saved to `.ufo/waves/round-46/w1/AsmGate/staged-ids` (147 matches).
- Sorted unique intersection saved to `.ufo/waves/round-46/w1/AsmGate/collisions`: 52 colliding IDs. This is a defect in the merge's continuous S-ID assumption; do not append the staged registry as-is. The merge report independently claims 147 appended rows continuing lane S-space, with first staged ID S200 (`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/MERGE-REPORT.md`, lines 5–10); intersection disproves collision-free continuation.
- Guard fixture: a scratch line `  | S002 |` passed the extractor and produced `  | S002`, confirming the permitted 0–3 leading-space behavior. Fixture was under `/fast/scratch/hyaku/tsukuroi-r46/AsmGate` and removed after use.

### Theme recommendation
**Assimilation: none.** The candidates surfaced by the matching-theme search are not a direct evidentiary addition to this round's bash descriptor identity or btrfs scrub/sysfs/systemd-stop mechanisms. The staged docs discovered concern the initramfs hook API, overlayfs, translated documentation, or unrelated systems (e.g. `knowledge/boot-writers-amend-2026-10-23.md` lines 39–44 explicitly says the observed association is time coincidence plus sudo record, not process identity). The search found no staged census-identity or btrfs-scrub-grounding entry; direct existence checks for those two filenames returned false. Avoid assimilating an adjacent topic as if it grounded the declared surfaces. The merge report's S201 duplicate is explicitly the same `alpm-hooks(5)` page as held S008 (`MERGE-REPORT.md`, lines 75–81), a source-checked reject reason for this round's theme; it is packaging hook semantics, not bash script execution identity.

### Limits
No campaign tool was run and no merge or lane content was modified. The collision calculation is exact for the specified regex outputs; it counts matching lines, not semantic duplicate claims. Theme search was targeted and does not establish that no relevant claim exists anywhere in all 70 staged files; the two requested exact filename checks and grep results are the scope of the observed evidence.
