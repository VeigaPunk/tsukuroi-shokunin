Verdict: JD3 FAIL; JD7 PARTLY; JD1/JD2/JD4/JD5/JD6/JD8 HOLD. These are recommendations, not admission.
Unchecked/residual: live manager min_use, installed binary equivalence, journalctl allocation implementation, historical rotation date and timestamp/causal provenance absent from the frozen host receipt. No counter result substitutes for entailment.
Axes: depth; C1 source truth; attack (scope, caps, attribution).

## Scope and method

Reviewed the actual working-tree note, not merely the draft: corpus/knowledge/journald-retention-plane-r76.md snapshot 068D, lines 1–106. All source paths below are relative to .ufo/waves/round-76/before/src/; host references name before/host.txt. Read quoted source lines with surrounding branches. Read the actual diff of the three stale carriers. The lsp device is unavailable: read xd://lsp returned 'No such tool'. Therefore textual source inspection/search was the explicit fallback, not semantic reference proof. No builds, counter instruments, mutations, installation, runtime rerouting or host service actions were performed. Only assigned report files were written.

## Findings by severity

### High — JD3 uses the wrong operation, repeated in the host derivation

Note:18 says 'used space plus the smaller of free space and keep_free'; note:39–40 repeats that interpretation and :81 explicitly computes min(free,4G). Checked journald-manager.c:161–171: after the usage read succeeds, :168 is `avail = LESS_BY(vfs_avail, metrics->keep_free);` and :170 is `space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use);`. LESS_BY is subtraction floored at zero, not minimum. The erroneous formulation becomes especially dangerous on a nearly full filesystem: min(free,reserve) adds available free bytes instead of reserving them. The unconditional 'both limits are respected' also needs the min_use qualification; journald.conf.xml:285–298 explicitly describes startup accommodation and surviving active files.

Corrected sentence: 'The manager computes avail as max(free space − keep_free, 0), then clamps current journal usage + avail between min_use and max_use; the startup minimum and active-file exemption qualify the resulting retention bound.' Replace both prose and host arithmetic, not just the table.

### Medium — JD7 assigns two defaults to the wrong function

Note:22 attributes all four defaults to journal_config_set_defaults. Checked journald-config.c:24–27 (four macros), :39–68 (actual initializer), :113–142 (merge). Only the rate interval/burst pair is assigned in the initializer (:51–52). Sync is merged at :133; max-file duration is merged at :142. The explanatory paragraph :57–63 partly corrects sync attribution but does not repair the table statement. The table quote concatenates two separate #define lines; it is not one contiguous verbatim source span.

Corrected sentence: 'journald-config.c defines DEFAULT_RATE_LIMIT_INTERVAL=30 seconds, DEFAULT_RATE_LIMIT_BURST=10000, DEFAULT_SYNC_INTERVAL_USEC=5 minutes and DEFAULT_MAX_FILE_USEC=one month; journal_config_set_defaults initializes the rate pair, while manager_merge_configs applies the sync and max-file defaults.'

### Medium — Host limit is a derivation with an unmeasured lower clamp, not an observed live manager value

Note:79–82 asserts an unconditional effective_limit. The frozen receipt contains no live metrics.min_use or startup journal usage. journald-manager.c:185 preserves max(previous minimum,current startup usage), and :170 uses that minimum. Therefore 256M follows as the configured MaxUse ceiling and as the arithmetic result under min_use <= 256MiB; the receipt alone does not establish the live clamp's lower bound. Recommend: 'Configured SystemMaxUse is 256MiB; given min_use <=256MiB, the space calculation yields 256MiB. Live min_use was not captured.' Avoid claiming a hard post-vacuum usage ceiling: journald.conf.xml:294–298 explicitly permits surviving active usage above it.

### Low — Some host narrative exceeds this receipt

Note:75 and the errata quote a size.conf birth timestamp, but before/host.txt:7–64 contains configuration content, not stat/birth provenance. Note:90–91 attributes the changed retained-boot window to the drop-in and storm ending; receipt :98–100 establishes only the present count of 3. Retain these as separately sourced facts if another receipt exists; otherwise mark the birth value unsupported here and the cause inference. The note's :4 'rows reviewed independently' must not be construed as all rows passing this review.

## Per-row entailment

- **JD1 HOLD**, journald.conf.xml:77–108. Quote :84–86: auto 'behaves like persistent' when /var/log/journal exists, volatile otherwise, and 'the existence of the directory controls the storage mode'. Surrounding :81–84 says persistent prefers disk but falls back during early boot/unwritable disk; :92–95 requires the flush transition; :102–108 explains namespaced directory creation. Row preserves 'like persistent', so it does not promise disk storage whenever the directory exists. Prose :28–29 should not turn this into an assertion that actual persistent use has no mount/writability condition; :260–266 explicitly has those conditions.
- **JD2 HOLD**, journald.conf.xml:274–298. Quote :283–285 gives 10%,15% and 'each ... capped to 4G'. :274–281 maps the first pair to MaxUse and second to KeepFree and says both constraints apply. Checked cap, startup exception and active-file scope, not just the percentages.
- **JD3 FAIL**, journald-manager.c:161–171. Exact quote :170 matches the formula text in the quote cell, but does not entail the row's 'smaller' interpretation; :168 contradicts it. Correction above.
- **JD4 HOLD**, journald-manager.c:176–185. Quote :179–183: 'Let's bump the min_use limit to the current usage on disk', startup/first open, and 'only a restart ... reset this value'. :185 uses MAX, not assignment to a possibly smaller current value. Checked another caller :1656–1668: full rotation also invokes patch_min_use; row says 'At startup', not 'only at startup', so that caller does not contradict it. Better precise wording: 'At startup/first open patch_min_use raises the minimum to at least current usage; full rotation also reapplies the patch; the comment describes reset on restart.' Manual :285–294 supplies the stops-growth/non-shrink outcome.
- **JD5 HOLD**, journald.conf.xml:300–309. Quote :302–305 gives one eighth capped 128M, 'usually seven rotated journal files', and compact mode cap 4G. The actual row retains 'usually'; no unconditional seven-file guarantee is admitted. :307–309 specifies binary units and synchronous extension enforcement.
- **JD6 HOLD**, journald.conf.xml:311–318. Quote :313–315 limits deletion to archived files and preserves active files; :316–318 explicitly allows total above the limit after vacuum and sets default 100. The row's 'only' is correctly scoped to deletion for that number limit.
- **JD7 PARTLY**, journald-config.c:24–27,39–68,113–142. Four values supported; function attribution incorrect as detailed above. No claim that these are the actual configured host rate or effective service limit is admitted.
- **JD8 HOLD**, journalctl.xml:941–985. Quote :954–957 gives oldest archived size-vacuum semantics; :943–944 includes active usage; :969–973 explicitly calls the effect indirect and exempts active files. :975–979 describes combined/zero switches; :981–985 rotates active files first when requested. The scoped 'only' is source-supported.

## Recomputed host derivation

before/host.txt:60–63 supplies SystemMaxUse=256M and RuntimeMaxUse=64M; :35–42 shows no explicit KeepFree or MaxFileSize. Binary unit basis: journald.conf.xml:307–308.

- Filesystem size :72 = 998037782528 bytes. Uncapped defaults: 10%=99803778252.8 bytes, 15%=149705667379.2 bytes. Each exceeds 4GiB=4294967296 bytes. MaxUse is overridden to 256MiB=268435456 bytes; KeepFree remains 4GiB.
- Available :72 = 764239769600 bytes. Independent receipt consistency: :76 bsize*bavail = 4096*186581975 = 764239769600. Do not use bfree, which includes blocks unavailable to ordinary users; manager :114 uses bavail.
- Correct avail = max(764239769600−4294967296,0) = **759944802304 bytes**, not 4GiB.
- Manager limit = clamp(journal allocated usage+759944802304, min_use,268435456). The sum vastly exceeds 256MiB. If min_use<=256MiB, result is **256MiB**. min_use was not measured; see finding.
- Configured default SystemMaxFileSize = min(268435456/8,134217728) = **33554432 bytes =32MiB**. This is an upstream-default derivation, not a measured internal metric.
- **148.6M is exactly the journalctl --disk-usage figure**, receipt :66–68, rounded presentation of archived+active journals, not an exact byte count. Receipt :84–86 reports 13 files and a logical size sum **209715200 bytes =200MiB**. Those are distinct measurements; sparse allocation can differ from logical length. manager :119–131 selects .journal/.journal~ regular files and sums st_blocks*512. The supplied journalctl.xml:943–944 specifies disk usage, but its implementation is not in the four pinned snapshots; do not treat the manager implementation as proof of journalctl's precise implementation or exact equality of its scanned scope.
- Largest listed file :89 =25165824 bytes=24MiB, below 32MiB. Neither that nor 13 files proves a rotation schedule.

Arithmetic exercised with shell integer expressions only; output: keep_free=4294967296, avail=759944802304, max_use=268435456, max_file_size=33554432, logical_sum_MiB=200, fs_available=764239769600.

## Stale-carrier quotations and supersession scope

All requested old claims are present; append-only errata match their text. This proves target identification, not the correctness of every replacement inference.

1. corpus/knowledge/journal-boot-plane.md:362–363: 'Effective journald retention (`SystemMaxUse`, rotation date of boot −12): shipped config is defaults-only; effective value not derived.' The merged drop-in now refutes defaults-only and resolves the configured size. It does **not** determine historical boot −12's rotation date; the erratum must leave that part open.
2. corpus/knowledge/degraded-triage-r4.md:70 (J2): 'no retention policy configured anywhere (merged coredump/journald conf = defaults only); storm is the growth engine (§3)' and blast-radius cell '3.9 G and climbing; `/` has 847 G free (measured)'. The journald drop-in contradicts a present-tense no-policy claim; 148.6M supersedes present journald usage, not necessarily any combined coredump+journal total. Preserve historical measurements as historical, rather than claiming they were false at capture.
3. corpus/knowledge/boot-plane.md:79–80: 'Retention wall: nothing older than boot −12; effective journald retention not derived (round-3 open item).' :240: 'Effective journald retention beyond the 13 retained boots.' The new read resolves configured size rules, not guaranteed retained time/boot count or a historical retention window.

## Residual risk and verification gaps

No canonical runtime/resume-continuity implementation was changed in this scoped documentation task; runtime identity, saturation, preflight mutation and routing claims were not made or tested. These checks are not evidence of runtime admission. Source inspection is upstream v262, while host receipt says systemd 262.1-1; binary equivalence remains unverified. Source hashes were read from frozen SOURCES.json, not independently recomputed by this seat. No counter instrument or live vacuum was run. Proposed corrections are grounded in the named pinned source ranges. Review result remains FAIL/PARTLY until the L1 updates the authoritative note and its copied derivation.

Self-evaluation: accuracy 4/5 (macro definition and journalctl allocation implementation absent from pinned files); completeness 5/5 (all eight rows, host arithmetic and four carrier locations covered); clarity 4/5 (long report, machine-readable rows provided); actionability 5/5 (corrected sentences and exact affected lines); conciseness 4/5 (row evidence intentionally duplicates severity detail). Overall 4.4/5. Main verification: ensure JD3 and JD7 corrections land in table and prose, preserve min_use/historical-window qualifications, and run the assigned format instruments separately from truth review.
