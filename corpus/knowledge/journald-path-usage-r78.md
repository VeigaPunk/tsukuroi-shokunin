source: S327 (tier A, code, mined) — https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c :91-135; S328 (tier A, docs, rejected for implementation support; context only) — https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml :941-948
verified-at: 2026-11-04; local frozen v262 snapshot reading only; no network refetch, C execution, or live-host measurement by this author
recheck: on-release; reopen the upstream function and documentation, compare frozen pins, and run python3 tools/measure-journal-usage-r78.py --revision <REV> after integration and independent review binding
companion: journald-path-usage-r78.json

# Journald path usage — six finite worked examples

Axes: depth and operability. This note deepens the existing journald accounting explanation; it does not expand coverage or establish a live-manager state. The companion contains exactly `source: ["S327"]` and the six U1–U6 case objects from `.ufo/waves/round-78/before/expected.json`, in order. These are hypothetical entry descriptors, not measured filesystem fixtures or observed journal contents.

## Source and accounting boundary

S327 is the upstream systemd v262 `manager_determine_path_usage` function, registered at `corpus/SOURCES.md` row S327 with lines 91–135 in `.ufo/waves/round-78/before/journald-manager.c`. Its frozen SHA-256 is recorded as `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`. The contextual man-page snapshot is `.ufo/waves/round-78/before/journalctl.xml`, recorded SHA-256 `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd`. Both digests here are transcribed from frozen expected.json, not independently rehashed by this author. Registered row S328 is explicitly rejected as implementation support: its broad documentation provides context only and is not an admitted source for U1–U6. The finite JSON source remains exactly ["S327"].

Exact source anchors in the manager snapshot:

- Lines 105–108 open the supplied path as a directory; failure returns an error, not an observed usage of zero.
- Lines 110–114 use `fstatvfs(dirfd(d), &ss)` and assign `*ret_free = ss.f_bsize * ss.f_bavail`. Failure here also returns an error before the scan.
- Lines 115–121 initialize used to zero and enumerate direct directory entries, rejecting names that end in neither `.journal` nor `.journal~`.
- Line 123 calls `fstatat(dirfd(d), de->d_name, &st, AT_SYMLINK_NOFOLLOW)`; lines 124–125 log and skip a failed stat.
- Lines 128–129 reject anything not regular according to the resulting `st_mode`.
- Line 131 adds `*ret_used += (uint64_t) st.st_blocks * 512UL;`.

Thus `used` below is an entry's contribution to allocated-byte accounting, **blocks × 512**, not its apparent `st_size`, and not filesystem free space. The 512 multiplier is independent of the filesystem's `f_bsize`. `ret_free` is a separate filesystem-availability result, not the sum's complement and not `st_size` subtraction. These fixtures supply no `f_bsize` or `f_bavail`, so they establish no free-space value.

## U1–U6 worked examples

The table preserves every input and expected output; bytes are used for size and contribution, while blocks are units counted in 512-byte accounting blocks.

| Case | name | kind | stat_ok | blocks | apparent size | used contribution | Source path |
|---|---|---|---|---:|---:|---:|---|
| U1 | active.journal | regular | true | 8 | 1048576 | 4096 | :119–121 accepts suffix; :123 stat succeeds; :128 accepts regular; :131 computes 8 × 512 |
| U2 | archived.journal~ | regular | true | 16 | 8192 | 8192 | :119–121 accepts second suffix; :123 stat succeeds; :128 accepts regular; :131 computes 16 × 512 |
| U3 | ignored.txt | regular | true | 8 | 4096 | 0 | :119–121 rejects suffix before stat or block addition |
| U4 | link.journal | symlink | true | 8 | 4096 | 0 | :123 does not follow the entry symlink; :128–129 rejects its non-regular mode |
| U5 | directory.journal | directory | true | 8 | 4096 | 0 | :123 obtains directory metadata; :128–129 rejects non-regular mode |
| U6 | unstatable.journal | regular | false | 8 | 4096 | 0 | :123 fails; :124–125 skips without using stat fields |

**U1:** 8 allocated blocks yield 4096 bytes, despite apparent size 1048576 bytes. This illustrates a discrepancy; it does not prove a sparse file was actually created or explain why its blocks differ from size.

**U2:** 16 × 512 = 8192 bytes happens to equal apparent size. That equality is incidental, not a switch to apparent-size accounting. The `.journal~` suffix is accepted; neither that suffix nor the illustrative word `archived` proves file validity or lifecycle state.

**U3:** The failed suffix predicate alone yields zero. Its hypothetical successful stat and size/block descriptors are never consulted on this source path.

**U4:** The direct entry is a symlink, not its target. `AT_SYMLINK_NOFOLLOW` at line 123 and the regular-file predicate at lines 128–129 exclude it, regardless of whether its target would be regular. This flag addresses the directory entry being statted; it does not prove that `opendir(path)` never follows a symlink in the supplied directory path.

**U5:** A directory named with an accepted suffix still contributes zero. The function does not descend into it: lines 116–132 contain one direct-entry loop with no recursive invocation or child-directory scan. Its children's contents are outside this call's scan.

**U6:** A stat failure means skip, not an assumed allocation or a failure of the whole function at this branch. The supplied `kind`, `blocks`, and `size` are hypothetical annotations only; a failed `fstatat` does not establish them and its output structure is not consumed. No particular errno or real host permission failure is asserted.

If these six descriptors were the only entries examined and the function reached the end successfully, their contributions would sum to 12288 bytes. This is arithmetic over the descriptors, not a claim that such a directory was measured.

## Exact descriptor limits and non-universal inferences

The finite domain is precisely six named entries, the displayed three kinds, the displayed stat outcomes, block counts 8 or 16, apparent sizes 4096, 8192, or 1048576, and outputs 0, 4096, or 8192. Successful opening, successful filesystem-availability lookup, and reaching the relevant entries are assumptions of these worked cases. Zero block counts, negative or extreme `st_blocks`, uint64 accumulation overflow, additional kinds, other names, scan errors, concurrent changes, filesystem quirks, and all possible errno values are not tested. No safe numeric range for arbitrary source inputs is inferred. These are entry descriptors, not file-descriptor resource-limit tests: no RLIMIT_NOFILE value or exhaustion threshold is measured or established.

The suffix check is a selection filter, not journal-header validation. This function performs no journal-content or header validation before adding a matching regular entry's blocks. Likewise, accepting the two suffixes does not authenticate a journal, classify every active/archived state, or guarantee recoverability. A sequential metadata scan is not an atomic filesystem snapshot; failures and concurrent changes can affect observed contributions. The six cases are not a universal semantic oracle.

## journalctl, upstream, and Arch boundaries

The v262 `journalctl.xml` lines 943–944 describe `--disk-usage` as summing disk usage of archived and active journal files; lines 969–973 distinguish that from vacuum operations restricted to archived files. Those documentation lines do not establish that journalctl uses this manager function, enumerates exactly the same path set, admits exactly the same files, or observes the same instant. Therefore **there is no guarantee that `journalctl --disk-usage` is identical to this path-usage sum**. A discrepancy alone does not prove corruption or a failed accounting implementation.

All cited line numbers and semantics belong to the pinned upstream v262 snapshots. This note does not identify the installed Arch package version, Arch patch set, effective storage namespace/path, mount behavior, host file allocations, or runtime values. Matching an upstream tag is not evidence that an installed Arch binary was built from byte-identical sources. Host observations and package provenance must be recorded separately and cannot be inferred from these hypothetical descriptors. No vacuum, rotation, flush, restart, configuration write, package transaction, or adoption decision is authorized by this note.

## Evidence and gate limits

The frozen C1 predicate is “six pinned path-usage cases match with review binding.” Its counter additionally requires the independent ReviewUsage verdict bound to the exact companion byte digest and the unique reviewer-role result bound to that report's digest. This author neither supplies that verdict nor claims the gate passed. Exact companion-object matching alone is not source execution, review authenticity, an outside verdict, or proof about installed Arch behavior. C2 operative-registry repair is outside this note.

## QUALITY check

This is the author's explicit check against `corpus/QUALITY.md`, not an admission, reviewer verdict or gate success.

- **1–3 (falsifiability, anchors, evidence classes):** Each U1–U6 output has an exact source branch and arithmetic or skip explanation. Source reading is observed; the descriptors and combined 12288-byte sum are hypothetical; installed Arch behavior and live state are not inferred. The snapshot paths, upstream tag, line ranges and companion pointer above resolve the evidence objects.
- **7 (source row, tier, section):** `corpus/SOURCES.md` S327 is tier A/code/mined and registers upstream v262 manager lines 91–135, covering every implementation anchor here. S328 is tier A/docs/rejected, registering journalctl.xml:941–948. Its rejection is preserved: contextual manual prose cannot establish manager suffix/stat/type implementation predicates. No effective configuration claim is made.
- **8 (sweep and metadata):** The author read the frozen upstream manager :91–134 and manual :940–973 on 2026-11-04; required source/verified-at/recheck fields are present. No unresolved host-cause explanation or [unknown] journal finding is retained. No local journal-message sweep was performed or needed to explain these hypothetical descriptors; this limits the entry to source semantics rather than host diagnosis.
- **14 (performed entry check):** This section evaluates the requested criteria now. It does not promise that somebody else will supply the entry's quality check. Independent review and integration remain distinct acceptance prerequisites.
- **19 (located quote and exact proposition):** S327:114, `*ret_free = ss.f_bsize * ss.f_bavail;`, supports the separate filesystem-availability assignment; :123, `if (fstatat(dirfd(d), de->d_name, &st, AT_SYMLINK_NOFOLLOW) < 0) {`, supports no-follow and the failed-stat branch; :128, `if (!S_ISREG(st.st_mode))`, supports regular-file selection; :131, `*ret_used += (uint64_t) st.st_blocks * 512UL;`, supports allocated-block accumulation. Each quote is a complete cited source line apart from indentation and under 25 words. The suffix proposition preserves both accepted suffixes at :119–121. No correction-fixture failure or execution claim follows from these quotes.
- **66 (all branches retained):** Both suffix alternatives, successful versus failed stat, regular versus nonregular mode, and directory-open/statvfs errors versus per-entry skips are retained. Nonrecursive scope and the limitation of no-follow to the statted entry are explicit. Neither file validity nor a universal lifecycle classification is asserted.
- **81 (non-author review and controls):** This seat authored the examples, not their independent verdict. The frozen scorecard records pre-data controls, but this author did not execute them. ReviewUsage must read the final note and bind the exact unchanged JSON digest; L1 must preserve the reviewer result binding and commit the artifacts before the frozen revision gate can count them. No row is self-certified here.
- **86 (upstream rather than own-work support):** U1–U6 rely on S327's upstream code locator, not the fact that this seat wrote matching data. Every named S-id is on the note's source line; S328 remains expressly rejected as implementation support. The JSON's exact single-source requirement is unchanged.
- **94 (range accounting and complete quotes):** All manager citations fall inside S327:91–135. **Limits:** contextual manual citations :940 and :969–973 lie outside S328's registered :941–948 range; they are explicitly enumerated here as supplementary rejected-row context, not implementation support or an expanded admitted range. :943–944 falls within that registered range. Inline source quotations above preserve complete cited line text apart from indentation; no stripped comment quote or fabricated line is used.
- **106 (pinned set before interpretation):** The pinned code's accepted suffix identifiers are `.journal` and `.journal~`; the selected mode predicate is `S_ISREG`, the stat flag is `AT_SYMLINK_NOFOLLOW`, and the multiplier is `512UL`. These are the actual source expressions, not reconstructed from expected outputs. This seat did not freeze the declaration and cannot retroactively certify that process. Any contradiction found by review must remain a claim miss even if exact JSON matching succeeds.

**Remaining limits:** finite descriptor matching does not establish universal source correctness, execution, host state, Arch build equivalence, independent reviewer authenticity, admission or outside closure. No rejected source is promoted by appearing in this note.
