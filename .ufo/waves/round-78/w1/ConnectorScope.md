# ConnectorScope — Round 78 bounded data-walk

Status: completed advisory analysis; no admission, integration, ordinal change or production edit.
Axes: **depth 8 (lowest tied), operability 9**. Base `b9019a1d0558241bf67cf31ff90256284d8657af` is an ancestor of freeze `07a607df1a5157daafc91bb5c26858af14415f43`. HEAD at capture equals freeze; the working source registry already contains the integration draft S327/S328. Committed and working bytes are therefore reported separately.

## Evidence and finite novelty

- Frozen SCORECARD Round 78 and `before/expected.json` constrain C1 to U1–U6, source S327, six exact objects and separate ReviewUsage file/report/result binding. C2 independently repairs eight missing operative tool rows and two code-2 maps. Neither claim authorizes new coverage or package adoption.
- `corpus/knowledge/journal-boot-plane.md:14-16,24-52,470-474` already holds historical disk footprint, retained boots and the round-76 configuration correction. It does not establish the six manager selection branches.
- `corpus/knowledge/journald-retention-plane-r76.md:13-18,26-31,39,43,57-66` already holds the cache arithmetic, startup floor, vacuum/active-file distinction, and **apparent length versus allocated-block distinction**. Calling that distinction itself novel would be false.
- `corpus/knowledge/journald-space-arithmetic-r77.md` holds A1–A6 on S324/S325, specifically manager lines 143–186 and macro definitions. New depth is the bounded provenance of its supplied `used/free` inputs: manager lines 91–135 select entries and compute allocated consumption/free space. It is not a newly discovered journal surface or a universal accounting oracle.
- Crucial runtime join: pinned `journald-manager.c:161` calls `manager_determine_path_usage(...,&vfs_used,&vfs_avail)`; :165–171 stores those values and applies the already-held arithmetic. `vfs_used` here is the selected-file allocated-block sum, **not total filesystem used bytes**. `vfs_avail` is filesystem availability from :114. Confusing the two substrates would corrupt both notes even if their finite JSON gates passed.
- Direct read of the pinned :91–135 body confirms suffix tests :119–121; no-follow stat :123; failed-stat skip :125; regular-file guard :128–129; `(uint64_t) st.st_blocks * 512UL` :131. U1/U2 are 4096/8192; U3–U6 are zero under their descriptors. The examples do not exercise every opendir/fstatvfs/readdir error, hard-link accounting or concurrent mutation.
- Independently computed snapshot SHA256 values match expected.json: manager `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`; manual `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd`. No network reopen or installed-build equivalence was performed by this seat.

## One bounded proposed move: a typed provenance bridge

For L1 consideration only: add a small **input provenance / scope bridge** from the r78 note to r77's formula, with explicit document-qualified source identities. State: S327 path scan produces selected allocated `used` and filesystem `free`; S325 consumes those values at :161–171; S328's manual supports broad CLI disk-usage meaning but does not prove the internal selection predicates. Keep the six objects, frozen counters, source pins and targets unchanged.

Affected axes: depth through the source-to-input-to-formula causal join; operability through a discoverable path that prevents selecting a stale or colliding source identity. This is a proposed non-harming move, not a measured Pareto verdict. No new runtime, tool, host read or ownership expansion is needed.

Pointer-addition surfaces for that single bridge (L1 owns edits):

1. `corpus/knowledge/journald-path-usage-r78.md` and its `.json` companion: preserve expected source/cases; prose joins to r77 without adding computed fields to frozen JSON.
2. `corpus/knowledge/journald-space-arithmetic-r77.md`: append a pointer identifying where its `used/free` inputs originate; retain A6's hypothetical/startup boundary.
3. `corpus/knowledge/journald-retention-plane-r76.md:39,57-66`: append the path-selection elaboration after the already-held allocated/apparent-size distinction; do not relabel that distinction new.
4. `SKILL.md:6068,6099-6103`: current cap-diagnosis and arithmetic navigation should point to r78's producer explanation, without claiming journalctl and the manager are identical implementations.
5. `corpus/README.md:717-727`: add a discoverable r78 companion entry alongside r77; explicitly retain existing coverage/Core–Frontier boundaries.
6. `corpus/SOURCES.md`: S327 used-by should name the r78 knowledge and lesson; S328 should name the rejection lesson, not become sole implementation support. Current working rows already do this. S320's historical false minimum wording remains superseded by S325.
7. `PROVINCE.md:555-573` can carry only a navigation/depth clarification, not another promotion. Existing mori evidence-reach and mado safety boundaries remain reported, not absorbed. Historical journal-boot capture needs no factual rewrite; an optional navigation pointer must not imply its old footprint was remeasured.

## False-source and downstream boundaries

- Same file URL/digest does not mean same claim: S320/S325 cover cache/vacuum ranges; S327 covers :91–135. URL novelty alone cannot demonstrate depth.
- S321 mined the manual for CLI vacuum/disk-usage scope; S328 rejects it only **as sole support for manager predicates**. Those dispositions are compatible, not a contradiction about source quality.
- `corpus/knowledge/pacman-exec-environment-r40.md:111-115` records an actual downstream Arch patch: +5 lines after upstream util.c:675. That offset applies to that pacman source, **not** to systemd. It is a concrete reason to preserve the upstream-v262 versus Arch-installed-build boundary, not permission to invent a systemd offset. R76 already states this at :22,43; r77 and SKILL :6076 repeat it. An installed package version alone does not establish identical code, build options or cache state.
- Mechanical source-ID existence, matching six objects and reviewer digest binding do not prove semantic entailment or authentic review. SCORECARD expressly retains the wholly fabricated report/result-bundle limitation. No admission authority is inferred from this seat.

## Recomputed source-ID lists and collision control

Input paths: live `corpus/SOURCES.md` and read-only `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`, located via existing assimilation/L0 references. No staged content was imported or renumbered.

Parser used: `^ {0,3}\|[ \t]*(S[0-9]{3,})[ \t]*\|` with multiline matching, ASCII exact first-cell IDs, sorted full row lists and set intersection. This is the requested indentation-tolerant census extraction, **not a claim that the production knowledge-ref parser accepts indented registry rows**: `tools/check-knowledge-refs-r68.py:63` still uses a column-zero ROW regex. No parser changed.

| Surface | Observed |
|---|---|
| Base committed registry | 326 rows |
| Freeze committed registry | 326 rows; 127 staged collisions, S200–S326 |
| Working registry at capture | 328 rows / 328 unique, S001–S328; no internal duplicate IDs |
| External staged registry | 147 rows, S200–S346 |
| Working-vs-staged intersection | **129 IDs, S200–S328** |
| Staged-only IDs | 18, S329–S346 |
| Indented control | 1/2/3-space rows S200/S327/S328 all extracted and collide; 4-space S346 and non-exact `S999 extra` excluded |

Contradictions kept explicit: the package manifest's “registry currently holds 199” is historical; L0 r64's 79 collisions is historical; neither is today's 129. Working S327/S328 are single current rows, not duplicate insertions, but external staged S327 means a Chinese translation-programme chronology capture and staged S328 a mirror locale-list capture. They are **different documents** from current systemd manager/manual rows. A bare-ID global search is therefore unsafe. Preserve namespace/document/URL context and the package quarantine; do not solve it by arithmetic ID shifting.

Durable artifacts in this seat directory: `reg-ids`, `base-reg-ids`, `freeze-reg-ids`, `staged-ids`, `collisions`, `indented-registry.md`, `indented-ids`, `indented-collisions`, `source-id-receipt.json`, `commits.json`. The receipt binds input SHA256 values and the capture state; commits.json lists full base/freeze/HEAD and recent registry/history commits. “Commit lists” are evidence files only: no git commit was made.

## Operator holds, followed through existing L0 references

- Fleet `.ufo/l0-questions.md:258` (tsukuroi r64) requests a document-keyed renumber campaign/re-stage/quarantine ruling and explicitly adopts nothing until ruled. The read-only package is still not adopted. No evidence here closes that operator decision.
- L0 :54–55,97 preserve partial-upgrade recovery and operator-owned pause-lift requests. LOG :2744 later describes a historical pause-lifted upgrade arc. These dated states must not be flattened into permanent host clearance: **this dispatch explicitly pauses all pacman transactions now**. No package transaction or host probe ran here.
- L0 :53 already answers planner topology: L1 holds planner, bounded data-walk may ride a connector. No runtime/route change needed.
- L0 :82 requests enforced future NO-EXEC review toolsets; :253 reserves whole-SKILL non-author SHONEN disposition to the operator. This report grants neither tool enforcement nor SHONEN verification.
- Round-78 LOG/SCORECARD retain no host mutation, package adoption, promotion or ordinal uplift. PROVINCE :25–28 and :563–570 retain operator remediation and sibling ownership boundaries.

## Verification, risks and handoff

Exercised: immutable base/freeze log and ancestry read, pinned source/body/caller reading, both snapshot hashes, scoped Markdown/source-ID recomputation, 0–3-space collision control, input hashes and commit-list capture. No production counter, full build/lint/test, live host accounting, privileged probe, network source fetch or another runtime was invoked. No tool installed/upgraded. All evidence writes are scoped; scratch was empty and removed.

L1 verification after any chosen bridge integration: run the unchanged C1 and C2 counting commands from SCORECARD at the landed revision; have ReviewUsage bind the final actual JSON and verdict report/result; run source census/knowledge-ref checks for the final source identities and companion paths. Check prose against the producer/caller join and keep the S328 rejection scoped. These are recommendations, not exercised results.

Remaining risks: mutable working inputs can move after capture (receipt hashes bind this observation); broad duplicate URL warnings are not ID collisions; examples cover six descriptors only; installed Arch behavior/cache and fabricated complete review bundles remain unproven. Stop at this one bridge proposal; no sibling work absorbed.
