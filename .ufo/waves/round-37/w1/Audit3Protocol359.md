# Audit3Protocol359 — protocol/source audit

## Axes
- **Operability:** reproducible claim gates and auditable inputs.
- **Frontier:** errno discrimination without inflating novelty or historical causality.
- **Process:** faithfully distinguish executed evidence, declarations, and unavailable material.

## Scope and evidence opened (2026-10-25)
Read `SCORECARD.md` round-37 declaration and pre-freeze C3 correction (lines 1857–1973); `corpus/SOURCES.md` registry and contract context; `corpus/README.md` coverage/frontier context; `corpus/QUALITY.md` criteria 61–72 and related corrections; `.ufo/waves/round-37/w1-spec.json`; assimilation `reg-ids`, `staged-ids`, and `collisions`; the merge package's `MERGE-REPORT.md`, `SOURCES.append.md`, and three proposed errno notes; and `Frontier4Errno428.md`. Read-only inspection only. Tooling rules read first at `/home/vgpnk/.omp/agent/RULES.md`. No tool installed or updated; no external source opened this round.

## Findings

1. **C3 is precisely declared as a fixed-population calibration repair, not an ordinal uplift.** The pre-freeze correction withdraws the unsupported new verified-rate ledger, states a 27-check predicate, and gives base evidence of 5 mismatches (K07–K11) versus a required measured-tip result of zero. This is a coherent gate contract, but this audit did not run the checker or independently inspect a post-change receipt; the after-value remains declaration-only from this seat. Do not report it as executed evidence based on this declaration. (SCORECARD lines 1950–1973.)

2. **Assimilation is not independently auditable from its local package index alone.** SCORECARD says three errno entries and nine S-rows were transformed, census-validated, collision-guard proven, and that twelve quarantine rows were hand-checked with verdicts. The checked-in round-37 assimilation directory only contains `reg-ids`, `staged-ids`, and an empty `collisions` file; no staged payload, quarantine table, row-level verdict record, or census/collision receipts were present there. `reg-ids` ends at S199 and staged ids run S200–S346, but these are ID lists, not evidence for content or decisions. The detailed merged package exists under read-only `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/`; the merge report says 147 rows accepted, zero refused, 70 entries, and explicitly says nothing was written into the lane. Action: retain the read-only merge package and per-row quarantine/admission evidence as explicit provenance when judging the later landed package; do not treat declaration text or numeric totals as proof of spot-check execution.

3. **The errno package contains a substantial overlap and an evidentiary boundary that must be kept visible.** The staged errno-name entry says it supplies vocabulary and explicitly does not explain the standing observation; the mount-contract entry treats mount(2) and Btrfs ioctl returns as distinct contracts; the variance entry is chiefly the `errno(3)` portability/meaning caveat and retention-window aging. These are related but potentially non-duplicate propositions. Yet existing lane coverage already includes S027–S038 and `snapper-eacces-mechanism.md`; `Frontier4Errno428.md` specifically warns that ordinary `mkdir(2)` distinctions cannot prove historical Btrfs ioctl behavior. Preserve the API-specific qualification and do not label the collection as newly uncovered broad errno ground without comparing each exact proposition to existing held notes. The variance note's claim that the host's retained journal query now returns zero and that the fault may be “aged out” is a dated package claim, not a fresh observation by this seat.

4. **SOURCES append contract itself is concrete, but proposal provenance differs from current lane registry evidence.** The append proposal has the 11-column schema, source URL, scope/anchor/teaches/status/opened/recheck/used-by fields; the merge report names S200 as first staged ID and flags S201 as overlapping held S008. The staged errno rows identify specific sources and used-by paths. This audit did not open those external URLs this round; per task context, their citation/recheck claims cannot be represented as newly sourced here. A later judge should require each source row's actual Gate/opening evidence and verify the used-by and anchor relationships against landed content, rather than infer that from row shape.

## Actionable gaps
- Keep C3's 27-check result explicitly unverified until a revision-bound executed receipt supports it; do not conflate proposal, counter output, and measured outcome.
- Preserve a durable, auditable mapping for the claimed twelve-row quarantine slice: frozen row identities, each verdict/reason, and the associated source/proposal bytes. Current round-37 local package index does not expose them.
- For errno assimilation, compare exact claims against held S035, S034/S038 and existing mechanism note; retain narrow API scope and `[inf]`/unknown boundaries. In particular, ordinary mkdir or mount-man-page contracts do not prove historical Btrfs subvolume-create cause.
- Reconcile the staged S200–S346 IDs with the stated subset used by errno assimilation; the ID lists alone cannot establish which cited rows were admitted or their row verdicts.

## Scope limitations
No tracked lane, fleet, sibling, source, or Git/jj state was modified. No checker, test, census, or campaign tool was run. No external URL was opened in this audit. No admission verdict is offered for all 147 proposed sources or 70 knowledge entries; the review is limited to the declared errno subset and its available package evidence.

## Report trailer
Scope: executed=read-only inspection; no shell commands or external fetches; no repository writes. Sources opened locally on 2026-10-25: lane SCORECARD.md, SOURCES.md, README.md, QUALITY.md, round-37 wave spec and assimilation ID/collision files; read-only merge package files under `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/`. External sources opened: none. Tools installed/updated: none.
