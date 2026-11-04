# CriticFreeze — round 78

Axes: **depth** (lowest, tied at 8) and **operability** (9). This is a leaf adversarial review, not an admission, score, outside verdict, or rule amendment.

## Evidence and executable counterexamples

Durable evidence, relative to the lane:
- `.ufo/waves/round-78/w1/CriticFreeze/attack.py`: exact isolated reproducer.
- `.ufo/waves/round-78/w1/CriticFreeze/attack-receipt.json`: exact generated UTF-8 JSON/prose bytes, argv, stdout, exit codes, independent calculations, frozen/worktree hashes, and scratch-disposal receipt.

Executed command:

```sh
env TMPDIR=/fast/scratch/hyaku/tsukuroi-r78/CriticFreeze PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-78/w1/CriticFreeze/attack.py
```

Each of the following isolated fixtures returned **rc 0** and exactly:

```text
C1 predicate="six pinned path-usage cases match with review binding" count=6 met=1 reason=finite-content-and-review
```

1. **Fabricated complete binding bundle.** Exact expected examples plus a fabricated ReviewUsage verdict and fabricated unique reviewer-role orchestrator result passed. No genuine reviewer execution was used. Exact verdict bytes were:

```json
{"artifact_sha256":"fa4dedbff34ab9bfedd2ebdd7b4018e35871ae54580ccbf43495e99ac7210ddd","reviewer":"ReviewUsage","verdicts":{"U1":"holds","U2":"holds","U3":"holds","U4":"holds","U5":"holds","U6":"holds"}}
```

The fabricated result output was `review_sha256=bcc44a68ab3b11f2f40d82e439394a49be2afbde233d7b770367e146f3095c30`. Both JSON files end with a newline; complete data/result bytes are in the receipt.

2. **False companion prose.** With that bundle unchanged, adding this exact UTF-8 note still passed:

```text
# Deliberately false adversarial fixture

The manager follows journal symlinks and adds apparent st_size; directories count too. Failed stat entries contribute their apparent length.
```

The fixture path was `corpus/knowledge/journald-path-usage-r78.md`; its final line has a newline. This falsifies selection/no-follow/stat/block explanations while preserving all numeric examples and binding bytes.

3. **Digest-bound false review prose.** Adding the verdict field `"explanation":"AT_SYMLINK_NOFOLLOW follows symlinks; st_blocks is apparent byte length."` and recomputing its result digest also passed, even with result text beginning `I did not review this source.` Exact changed bytes are recorded. The counter authenticates neither narrative substance nor the actor behind a claimed name.

**Classification and smallest safe correction:** (1) is the expressly acknowledged complete-bundle fabrication limit in SCORECARD :6520–6526, not a newly discovered failure of a promised authenticity guarantee. (2) would fire C1's already-frozen **false companion explanation** kill rule if present in the submitted artifact, despite numeric success. (3) demonstrates a bound digest is not source-review truth; a false upstream interpretation in submitted review evidence requires substantive scrutiny, not acceptance from the digest. These fixtures are mine, not evidence that an actual seat fabricated anything. Keep the frozen gate unchanged; compare the real companion and review to source, and bind the actual review bytes through the actual orchestrator result. Never call count=6 a general semantics/authenticity verdict.

## Reopened source and six independent calculations

Opened `.ufo/waves/round-78/before/journald-manager.c` :91–135, `journalctl.xml` :941–978, and `corpus/SOURCES.md` S327/S328. The reproducer independently hashed both snapshots, both counters, and expected.json, and compared every byte digest to `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 07a607df1a5157daafc91bb5c26858af14415f43:<path>` and frozen-digests.json: all five matched. This is local frozen provenance, not an independent network-fetch or installed-Arch provenance claim.

| Case | Independently derived contribution | Source reason |
|---|---:|---|
| U1 | 8 × 512 = **4096** | `.journal`, stat succeeds, regular; size 1048576 unused |
| U2 | 16 × 512 = **8192** | `.journal~`, stat succeeds, regular; equality to size incidental |
| U3 | **0** | neither accepted suffix; rejected before stat |
| U4 | **0** | no-follow stat reports symlink mode; not regular |
| U5 | **0** | directory mode not regular; no recursive scan |
| U6 | **0** | failed fstatat is logged/skipped; supplied size/blocks never consumed |

Total if these are the only visited entries and the scan completes: **12288 bytes**. Calculation code derives contributions by the observed source predicates rather than copying expected `used` values; all six match.

Source literals withstand these attacks:
- :119–121 accepts precisely the two suffixes, not semantic active/archived status or journal-header validity. An arbitrary regular file with that suffix is included; this is not a counterexample to the frozen selection claim.
- :123 uses `AT_SYMLINK_NOFOLLOW` for each entry. It does **not** prove `opendir(path)` never traverses a symlink in the parent/supplied path. Current companion explicitly preserves that distinction.
- :125 skips failed entry stats; this does not generalize to opendir/fstatvfs errors (:105–112), which return errors before normal usage initialization.
- :128–129 excludes nonregular entries. :131 multiplies `st_blocks` by **512UL**, not by apparent size, f_bsize, or f_frsize. :114 separately computes availability using **f_bsize × f_bavail**.
- S327's located claim and source digest agree with the function. S328's rejected role is accurate: journalctl.xml says active plus archived disk usage and archived-only vacuum, but does not establish this manager's exact filters, identical CLI implementation, or installed Arch behavior.

The six descriptors do not exercise arbitrary names/kinds, zero/negative/extreme block counts, overflow, scan failure, concurrency, real errno behavior, or header validity. These are declared finite-domain limits, not grounds to invent a wider target after freeze.

## Every C1 conjunct and freeze boundary

Counter locations refer to `tools/measure-journal-usage-r78.py`:
- Snapshot pins (:41–43): both actual frozen snapshots hash correctly; changed snapshots fail before content evaluation.
- Exact six descriptors/outputs and `source: ["S327"]` (:44–53): complete-object equality, duplicate-key rejection (:23–33), strict integers and stat boolean prevent dropping a case, inventing a source, or bool-as-integer substitution. Independent source-derived outputs above agree.
- Review artifact digest, identity, and all six holds (:54–59): explicit byte binding, not evidence of genuine review authorship. Fabrication attack addresses that distinction directly.
- Unique reviewer-role result, lane/round/wave, report digest (:60–69): structural identity and digest presence are checked. Output substring presence does not establish that surrounding text assents to the review; attack (3) demonstrates this.
- Companion explanation is not an input to the numeric gate; attack (2) therefore succeeds. It remains a separate explicit kill-rule conjunct.
- Target 6, expected cases, pins and frozen counter remain unchanged in this review. The command loads expected.json from the working counter's ROOT, not from `--revision` or fixture root (:126); external freeze-byte comparison remains necessary, not a license to edit expected data. All compared bytes matched the frozen commit in this execution.

Read ScribeNote's now-available `note.md` :1–66: its actual explanations match all six derivations, retain directory-open/statvfs error distinctions, distinguish supplied-path from entry symlinks, do not infer archival validity from names, and do not equate this sum to journalctl output or installed Arch behavior. No false companion explanation was found in that draft. ReviewUsage's `source-review.md` was explicitly a derivation, not a completed verdict, when opened. This review does not claim that final integrated binding already exists.

## C2: operability attack, scope and separability

Frozen checker `_coverage` :262–326 matches paths, row kinds, verdict digits, and literal selftest flags; it does not execute advertised commands or establish truthful verdict semantics. The isolated reproducer called this exact frozen subfunction with one existing tool and this false entry:

```text
python3 tools/measure-journal-usage-r78.py --invented-mode
```

With verdict text `0 pass; 1 fail; 2 cannot-evaluate`, it returned **findings=[]** and covered that path. This is a **subfunction** observation, not a claim that the entire C2 checker passed a committed false table. The source parser has no `--invented-mode`. A submitted row like this would fire the already-frozen **false command** kill rule. Smallest safe correction: keep the counter frozen and inspect actual advertised commands and code-2 meanings against each tool's parser/returns; do not replace source inspection with digit counting.

Existing-tool retention also needs independent comparison: the ordinary counting command enumerates tools in the selected revision (:414), not an immutable base set. Deleting a tool together with its row can evade that numeric surface; this is source-derived, not executed against production. Even `--baseline-tools` reports missing counts (:421–425), while the final exit decision uses findings (:426). Deleting an existing tool is explicitly a C2 kill, regardless of that limitation. No tool deletion was performed here.

Read ExecRegistry's eight rows and two fixes. They address exactly the baseline missing-path set and missing code-2 maps, distinguish argparse usage from absent inputs, and preserve historical non-2 returns rather than promising universal historical conformance. Its command evidence records invalid-option rc 2; those are the executor's receipts, not my executions. Final candidate command truth, complete existing-tool retention, and actual integrated count remain the independent registry review/integration responsibilities; I did not award them from my synthetic example.

C1 reads its two pinned snapshots, data, review and orchestrator result; it never reads SKILL.md. C2 reads operative SKILL.md and committed tool blobs (:409–415), not the new note, data or review. Thus registry repair cannot numerically compensate for false companion prose or a missing depth binding; correct examples cannot repair registry commands. The shared repository/source-control process is not evidence of numeric causation between these two claims.

## Do-nothing and lowest-axis challenge

Read the pre-seat durable controls rather than rerunning reported failures:
- `before/controls.json`: C1 base `b9019a1d0558241bf67cf31ff90256284d8657af` = **count 0, rc 1**, versus target 6.
- C2 same base = **10 findings, rc 1**: eight missing rows (check-r71-routed-r72, check-r72-routed-r73, check-r73-routed-r74, check-r75-routed-r76, count-jd-rows-r76, count-md-rows-r72, count-uf-rows-r74, count-ul-rows-r73) plus missing code 2 for count-jt-rows-r75 and check-r74-routed-r75, versus target 0.
- Source-fetch/fill without review and fabricated review without orchestrator result both fail with rc 1. They do not contradict the complete-bundle success demonstrated here.

Do-nothing cannot meet either target. C1 explicitly targets depth, one of the tied lowest non-retired axes, with worked source explanations rather than relabeling the operability repair. Merely repairing C2 while leaving C1 absent would fail the frozen depth target. Conversely, count=6 alone does not establish ordinal depth improvement or saturate the wider source domain. Such frontier judgments remain with the canonical authority, not this seat.

## Boundaries

No production/results mutation, sibling write, git mutation, clone, commits, package install, privileged probe, host configuration change, full build, or other orchestration/judgment runtime. Only the assigned isolated Python counter attacks and private registry-subfunction fixture were executed. Scratch `/fast/scratch/hyaku/tsukuroi-r78/CriticFreeze/` was removed in the harness's finally block; durable exact-byte receipts remain in this seat. No tools installed or upgraded. No final candidate admission or universal authenticity guarantee is asserted.
