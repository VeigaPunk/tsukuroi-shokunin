ROW GR2 VERDICT: partly
SECTION SHA256: 9fd581a0c9d02b02100b6a15648b7c6e4be896ac746ed09303a88dc8a24f0ec5

Axes: depth, C1, clause truth, citation support, inference/provenance accuracy. Review is limited to GR2 at ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0, with Limits and Range gaps as context. No admission mark written.

## Binding identity and mechanical evidence

Extracted the entry using git show at the named revision, not the mutable worktree. check-scrub-admission-r52.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0 --section-hash --no-base-check printed structural_ok 1, problems [], and the GR2 hash above. Independently hashing the section from its heading up to the next heading (without an extra final newline) reproduced that exact hash. The full entry SHA256 at 6abef5d0 and ff9470ea was a421bf27ce3d11b7a48e9fff5fe45c88447f49e3cf53c399223479d95f88e32b at both revisions; git diff --stat between them for the entry was empty.

sha256sum -c SHA256SUMS in each source directory reported every listed file OK. Relevant mapping:
- S240 = .ufo/waves/round-43/frozen/src/ioctl.c, 7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01.
- S242 = .ufo/waves/round-44/frozen/src/scrub.c, f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8.
- S243 = .ufo/waves/round-44/frozen/src/sysfs.c, ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43.
- S247 = .ufo/waves/round-45/frozen/src/dev-replace.c, f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a.
FETCH.txt in these directories identifies Linux v7.2.11, peeled a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea. The round-45 capture hash independently matched f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70.

lint-grounding-r51.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0 reported PASS: lint_ok 3, rows_clean 3, quotes 99, quote_bad 0, cites 96, cite_bad 0, gap_ok 1, gaps_computed 98, gap_missing [], gap_extra [], pin_problems [], snapshot_problems []. GR2: quotes 44, quote_bad 0, cites 41, cite_bad 0, problems []. Receipt: .ufo/waves/round-52/w1/R52CritGR2b/lint-grounding-r51.json. An independent stripped-whole-line comparison of all 44 GR2 quotes against the four mapped snapshots found 0 mismatches. --emit-gaps reproduced the entry's block, and my manual cited-lines-minus-declared-ranges recount agreed. Mechanical PASS does not establish semantic truth.

## Defect: Host-reading visibility wording overreaches

Entry lines 233-235 say a replace set to suspended without taking the exclusive operation "shows in neither" file. This is safe only if narrowly interpreted as "neither file labels the state SUSPENDED". It is not safe as a claim that neither file exposes that replace: the target marker remains observable.

Strongest pinned counterexample: dev-replace.c:170-172 handles both STARTED and SUSPENDED items and finds the target; dev-replace.c:196-210 sets REPLACE_TGT on that target during initialization. To reach the cited resume failure at dev-replace.c:1235-1242, the target-presence check at dev-replace.c:1218-1227 must already have passed. The failure branch changes replace_state but does not clear REPLACE_TGT or destroy the target. sysfs.c:2015-2017 prints that bit as 1. sysfs.c:2112 includes replace_target in the device attributes; sysfs.c:2165-2166 creates devinfo/<devid>, and sysfs.c:2185-2188 adds those attributes for each device in the filesystem device list (assuming successful registration). The initial setup also sets the bit at dev-replace.c:309; successful finishing clears it at dev-replace.c:970.

Thus the target marker can remain 1 while exclusive_operation names a competing operation. The state itself is not exposed, but the replace is not necessarily invisible. This is a precision defect rather than a rejection of the kernel Statement: the preceding phrase about "replace state itself" supplies a defensible narrow reading, hence partly, not fails. Impacted axes: depth and C1, specifically operator-facing interpretation of the sysfs observations.

Smallest safe correction, exact replacement for the sentence beginning "Neither file reports":

"Neither file reports the replace state itself: when the resume path sets the replace to suspended after failing to take the exclusive operation (dev-replace.c:1235-1242), `exclusive_operation` does not name that replace. The target's `replace_target` flag may still read 1: initialization sets the target bit for STARTED and SUSPENDED items (dev-replace.c:170-172, :196-210), and sysfs reads that bit (sysfs.c:2015-2017); neither attribute labels the state SUSPENDED, although the Statement counts it as ongoing."

If adopted, regenerate the gap block because these additional source citations are not all currently declared/cited. No edit applied; frozen verdict binds to existing bytes.

## Remaining clauses checked

- Start/resume copy: dev-replace.c:700-703 gives the reuse comment and source devid with false,true; dev-replace.c:1197 names the unmount-interrupted resume, dev-replace.c:1245 starts its kthread, and dev-replace.c:1265-1268 makes the second matching call. scrub.c:3079-3081 confirms the parameter order. Both actual call sites match; no claimed range crosses a function boundary.
- Early error ladder: scrub.c:3094-3095 closing -> EAGAIN; scrub.c:3109-3111 setup error; scrub.c:3114-3116 worker-get error jumps to out_free_ctx and returns ret at scrub.c:3250-3253. Then scrub.c:3120-3123 unknown device or MISSING && !is_dev_replace -> ENODEV; scrub.c:3127-3133 !replace && !readonly && !WRITEABLE -> EROFS; scrub.c:3138-3142 !IN_FS_METADATA || REPLACE_TGT -> EIO; scrub.c:3147-3153 context present, or !replace && ongoing -> EINPROGRESS. Order and conditions all match.
- Ongoing: dev-replace.c:1278-1279 rejects !is_valid; STARTED and SUSPENDED at dev-replace.c:1286-1287 reach return true at :1300. The comment at :1288-1297 supports the unmount-suspended case. "True when" is supported as a sufficient condition; I do not infer rejection of arbitrary corrupt/unlisted state values, since the switch has no default.
- Universal "any": current entry qualifies it by passing the earlier checks. This fixes the pre-read counterexample: an earlier EROFS/ENODEV/EIO wins before scrub.c:3147. Once reached, the context disjunct applies to replace and non-replace calls; attachment at scrub.c:3159 has not happened on refusal.
- ioctl: ioctl.c:3072-3073 CAP_SYS_ADMIN; :3075-3078 extent-tree-v2; :3080-3082 memdup_user; :3084-3085 unsupported flags; :3087-3090 write access when READONLY is absent. All precede :3093-3095, which stores the scrub return. :3109-3110 overwrites ret with EFAULT on failed copy-back, and :3115 returns ret. All cited ranges remain within btrfs_ioctl_scrub.
- Progress: scrub.c:3321-3336 reads only the looked-up device's scrub_ctx, and :3336 exactly implements 0/ENOTCONN/ENODEV as described. scrub.c:3159 attaches and :3222 clears; I inspected the intervening run path and found no early return bypassing that clear. The replace passes the source devid, so the source carries the context during its copy.
- Quotes: all 44 matched. The CLI-printing inference is appropriately marked; this review did not establish how userspace prints those errors.
- Host provenance: capture.txt:1 records uid 1000 and CapEff 0; ioctl.c:3132-3133 gates the progress ioctl. sysfs.c:76-78 gives BTRFS_ATTR mode 0444, with registrations at sysfs.c:1302 and :2019. sysfs.c:1287-1288 maps DEV_REPLACE to its string; dev-replace.c:1235 and ioctl.c:3190 request that exclusive operation. The capture has no exclusive_operation/replace_target readings. C2ExecHostRecheck.md:84-89 (its section 3) really records both world-readable files, exclusive_operation none and devinfo/1/replace_target 0. I did not treat those observations as a live round-52 measurement.

## Boundaries

No live scrub, replace, ioctl, sysfs write, service operation, upstream fetch, or full admission scoring performed. No other R52 GR report was read before writing this report. I read round-51 pre-read findings only after independently checking the current clauses; the earlier universal/gap/registration defects are fixed in these bytes. I did not verify helper implementations absent from the pinned snapshots (including btrfs_exclop_start), Arch patch equivalence, arbitrary corrupt-state behavior, or the CLI output. No tools installed or updated. No tracked lane file edited and no admission mark written. Scratch removed after report/receipt delivery.
