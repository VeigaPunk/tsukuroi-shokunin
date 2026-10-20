# Round 14 — repair-first source-scope corrections

Author: tsukuroi L1; 2026-10-20. Baseline `8606bad4cbc6451ac2890c9f8e2548a36c386db6`. Only the externally steered round 14 is worked.

## Declared claim

C1 — **depth**, repair the active source-inconsistent ProtectSystem value-domain sentence and S042 comment self-description through named corrections **R14-VALUE-DOMAIN** and **R14-COMMENT-ATTRIBUTION**. Before: neither correction is present and both unsupported assertions stand. After: both have located primary-source support, preserved history has explicit supersession notices, and a bounded correction-conformance command counts 0→2 while failing the named old defects. Source agreement is assessed separately from that structural counter. No general semantic proof or historical-host-cause proof is claimed.

Depth and adjacency are tied lowest at 8; C1 works depth. Scores remain depth8/coverage9/operability9/freshness9/calibration9/adjacency8: no count-to-ordinal scale is invented. No second claim, new capability, uncovered ground or exploratory claim is declared. The two metadata corrections support the same repair; they are not additional claims.

## Gate

Candidate: `corpus/knowledge/source-scope-correction-r14.md` and `.json`, citing opened S044 and S045. This correction only supersedes the two defective propositions and stale metadata, not the valid surrounding r13 technical teaching. Rounds 12 and 13 remain independently rejected; no retroactive admission or changed verifier record is claimed.

Sources opened this round, 2026-10-20:

| Row | URL | Exact location | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S044 | https://man.archlinux.org/man/systemd.exec.5 | SANDBOXING > ProtectSystem=, first definition sentence; footer systemd 262.1 | “Takes a boolean argument or the special values "full" or "strict".” | Admit the documented option-domain correction. This is not a closed list of all unit-side read-only mechanisms or a runtime-host observation. |
| S045 | https://api.github.com/repos/omacom/omarchy/issues/comments/6071740243 | exact comment6071740243 body opening sentence | “I tried this on a stock Omarchy worker VM” | Reject this comment as this host's cause or maintainer acceptance. It asserts VM execution; that assertion is not independently verified here. |

The full #8047 comment was successfully opened by L1 before a repeated GitHub API request became rate-limited (HTTP403). Its API fields say login `omarchybot`, type `User`, association `COLLABORATOR`; those fields do not establish generation method. Its **Second opinion** paragraph attributes review to Codex Medium and explicitly qualifies independence. Its maintainer-decision sentence concerns **#6634's remount failure**, not a decision accepting #8047's diagnosis; #8047 itself ends “This now waits on your answer.” The #6629 comment's separate disclaimer is not transferred to #8047. Source-content shell commands were treated as data and not executed. Exact source-reading records and any additional source-seat access limits live in `.ufo/waves/round-14/repair/`.

Rejected propositions retained: the option's documented value domain is non-exhaustive; #8047 self-describes as model-generated automated triage; the API account's name/association establishes generation method or maintainer acceptance; a VM assertion proves this host's historical failure. Flips require matching source text for the exact proposition and source object, or primary incident-bound evidence for the host-cause claim. No such evidence is asserted.

S044 is docs/A/mined; S045 is community/C/rejected and supersedes S042. Original S042 immutable fields remain visible as history. Existing status/recheck/used-by changes are recorded after registry integration; adding rows is curation, not expansion credit.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| claim exceeds source / R14-VALUE-DOMAIN | outside `round-13-verifier-spotcheck.md:143-153`; active r13 MD original line97 | QUALITY #2/#17 existed but did not distinguish option domain from mechanism universe | Named correction R14-VALUE-DOMAIN; source S044; explicit historical notice; QUALITY #19 requires proposition-level located source support. Same checker is measured against old and corrected content, with restored-defect fixture. |
| claim exceeds source / R14-COMMENT-ATTRIBUTION | outside spotcheck:155-165; S042 teaches and round13 lesson collective self-description | QUALITY #3/#7/#18; #18 itself generalized bot attribution without inspecting each body | Named correction R14-COMMENT-ATTRIBUTION; source S045 supersedes immutable S042; QUALITY #19 and #20 distinguish account fields, author assertions, second opinions and maintainer authority. Same check must reject the old attribution and its restored-defect fixture. |
| stale draft metadata / R14-S041-METADATA | outside spotcheck:243-246; r13 JSON sources[0] says reserved/SourceRegistry despite S041 mined | QUALITY #10/#11 | Additive supersession records actual mined registry status and removes draft-owner metadata from the active contract; historical keys remain preserved. |
| specification exceeds executable / R14-GATE-CONTRACT | outside spotcheck:248-252; ten-heading JSON gate_contract versus five-heading checker | QUALITY #2/#14 plus Gate standard | Explicitly supersede residual JSON contract as non-executable historical draft; executable checker and its SKILL registry define only their listed bounded predicates. No passing gate is presented as source truth. |

A criterion alone is not a demonstrated fix. The red-before and isolated restored-defect observations are appended only after L1 executes them; no unrun check is a pass.

## Scope and wave

At entry the worktree was clean, identity `tsukuroi-shokunin <tsukuroi@shokunin.local>`. Inherited lane-authored leftovers: none. The independent round13 verifier lesson is preserved untouched. Launch digest: `2026-10-20T02:55:31-03:00 launch tsukuroi round=14 pgid=1551465 driver=hyaku-inline attempt=1`.

One validated 32-seat task batch was dispatched unchanged: executor4, scout8, reviewer6, critic4, connector4, sentinel2, scribe2, revenger1, mutation-tester1. L1 holds the canonical planner seat; DataWalk is bounded revenger reconnaissance, not a planner swarm-role bypass. Spec, dispatch payload and actual IDs: `.ufo/waves/round-14/repair/{spec,dispatch,swarm-registry,task-result}.json`. An initial registry-record call rejected an absolute registry path; using its required lane-relative path succeeded. No wave was split or dispatched twice; no model parameter or routing change.

No privileged probe, snapper query, daemon activation, service operation, package transaction, Btrfs operation, boot or remediation is part of this round. The mkinitcpio42 `/sysroot` versus `/new_root` hook blocker remains. Whole-SKILL no-oral-context execution and independent admit/reject sampling remain outside this author-side work; SHONEN boxes are not promoted.

## Source census — start

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`

Observed exit0:

```text
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

Baseline row histogram: rows43; A36/B1/C6; mined31/queued5/rejected7; malformed0. Command parses eleven cells from lines matching `^\|\s*S\d{3,}\s*\|`; baseline `git show <revision>:corpus/SOURCES.md`. Exact baseline source counts and entry state are in `.ufo/waves/round-14/repair/start.json`.

## Gate — completed author-side integration

All32 wave seats and the requested source-retention handoffs finished before
L1 shipping verification. Measured implementation:
`9dd82bceda4cf45c1e1e59e17c996ac898a5ecb7`.
Same evaluator SHA256 for baseline and implementation:
`0771619dde7cc69fdb37538ad786f293b629f4062167a44a2d9cf4702ec6d428`.

Counting command: `python tools/check-source-scope-correction.py --revision
<revision>`. Baseline `8606bad4cbc6451ac2890c9f8e2548a36c386db6` returned
exit1/count0/findings7, including **VALUE_DOMAIN_OVERCLAIM** and
**COMMENT_ATTRIBUTION_OVERCLAIM** at their preserved active loci. This
red-before is not only a missing-new-file check. Implementation returned
exit0/count2/findings0. Count requires resolved correction predicates and
preceding notices, not just two JSON objects.

`python tools/check-source-scope-correction.py --selftest` returned exit0:

```text
CHECK_SOURCE_SCOPE_CORRECTION_SELFTEST: PASS (15 cases, 15 passed, 0 failed)
```

The restored-domain and restored-attribution fixtures require failed exit,
specific finding-ID sets and count1, not merely any nonzero result. Missing
notices require count0; moving a notice after its site and removing historical
phrases also fail. The independent noun-denial fixture accepts “contains no
self-description”. Invalid CLI returned exit2/E-CLI, not a false red.
The owner's preliminary 14-case static report is superseded by this observed
15-case result; no fixture or source truth is inferred from that older report.

Exact commands/stdout/stderr: `.ufo/waves/round-14/repair/verification.json`.
Its integration pointer resolves to `integration-verification.json`, which
records the source-agreement, table, history, census and safety measurements.
The first safety enumeration mistakenly included this newly written
measurement file in the older committed-input scope, so git show returned128;
only that enumeration was corrected. No checker or census was rerun.

Source agreement was evaluated separately. The two correction quotes are
verbatim located source fragments of11 and16 words; all five supplemental
comment quotes match the retained body and their declared word counts.
The canonical API body and HTML witness use the same body digest. The body
contains no occurrence of the generation-method phrases in the bounded sweep
recorded by `l1-source-review.json`; this is a statement about this exact
comment, not about the account's actual generation method.

L1's bounded final mention sweep covers SKILL, PROVINCE, corpus index,
QUALITY, SOURCES, the affected lessons and all knowledge MD/JSON. Its24 hits
are historical assertions under explicit notices, S043's separate #6629
scope, or new correction/rejection descriptions. Original source rows
S001–S043 are byte-preserved; existing status/recheck/used-by changes: **none**.
Ten changed historical text files have0 removed/replaced lines. Removing
only r13 JSON's additive r14_supersession gives the original object exactly.
Census code, old checker, both outside verifier lessons and SHONEN are
byte-identical to baseline. New entry/lesson table blocks have consistent
column counts. Credential-material, IPv4 and raw-journal-prefix pattern
sweeps over the committed new evidence/code/entry have0 hits; the patterns
and exact scope are recorded, not represented as a full privacy audit.

Admit author-side: the two narrowly sourced corrections and supporting
metadata errata. Reject: the old domain-open assertion, unsupported #8047
self-description, cross-comment disclaimer transfer, mis-scoped maintainer
decision and host-cause/acceptance uses. All lane-dispatched reviewers are
author-side; **fresh non-author admit/reject sampling remains pending**.
No gate pass pre-admits this round, changes prior rejections or certifies
general semantic truth.

## Source census — end

Same command as start; observed exit0, stderr empty:

```text
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
tsukuroi	W04	S044 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

Rows43→45; tiers A36/B1/C6→A37/B1/C7; statuses
mined31/queued5/rejected7→mined32/queued5/rejected8; malformed0→0.
Added tiers A1/B0/C1; no pre-existing mutable-field changes. W04 URL reuse is
disclosed scope-separated curation, not a warning-free result. Frontier
ground advanced: none; the rollback-net surface is repaired, not expanded.

Author-side C1/depth verdict **improved**, ordinal8→8 (0); all other axes
unchanged. Trends: expansion unchanged; quality improved; discernment improved
because the outside disagreement became grounded criteria19/20 with named
corrections and observed red-before/restoration evidence. Outside agreement
is not asserted. No capability, host remediation, promotion or new L0
decision is claimed. Tools installed/updated by L1 and every seat: **none**.

