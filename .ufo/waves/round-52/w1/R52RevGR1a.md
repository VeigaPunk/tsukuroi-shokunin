ROW GR1 VERDICT: holds
SECTION SHA256: 98fa4e07768d240eaf5ea2cce13ce0623fdb756054e5df9f7b9fe68ab2e63987

## Scope and axes

Axes: semantic accuracy; citation/quote fidelity; explicit uncertainty; frozen-byte identity. This is an independent review of GR1 only, not an admission or an assessment of the other rows. No other R52 GR report was read. No actionable defect found within the row's expressly qualified scope; no replacement text proposed.

The entry was extracted exactly once with the assignment's `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:corpus/knowledge/btrfs-scrub-grounding-r45.md` command into the seat scratch. I read entry lines 14–102, Limits 338–366, and Range gaps 367–375. All entry conclusions refer to that frozen extraction, not the mutable working-tree entry.

## Observed mechanical evidence

`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r52.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0 --section-hash --no-base-check` returned `structural_ok: 1`, `problems: []`, and GR1's section hash exactly as bound above. This is identity evidence, not semantic validation or a counted admission.

Before opening source implementations, `sha256sum -c SHA256SUMS` in each absolute snapshot directory returned OK for every manifest entry: round-45 src (cmdline.c, dev-replace.c, systemd.kill.xml, kstrtox.c, vsprintf.c) and round-44 src (scrub.c, sysfs.c, timer, service, PKGBUILD). Source mapping for this row: S246 = round-45/frozen/src/{cmdline.c,vsprintf.c,kstrtox.c}; S243 = round-44/frozen/src/sysfs.c; S242 = round-44/frozen/src/scrub.c. These are the pinned snapshots, not similarly named checkout sources. Manifest evidence: round-45 src/SHA256SUMS:1,4-5 and round-44 src/SHA256SUMS:1-2.

`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/lint-grounding-r51.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0` returned PASS: `lint_ok=3`, `rows_clean=3`, `cites=96`, `cite_bad=0`, `quotes=99`, `quote_bad=0`, `gaps_computed=98`, `gap_ok=1`; gap_missing/gap_extra/gap_dups, entry_problems, pin_problems and snapshot_problems were empty. GR1 specifically: cites 27, quotes 30, cite_bad 0, quote_bad 0, problems empty. The whole-entry lint results are reported as requested, not substituted for semantic review of GR2/GR3.

LSP availability: reading `xd://lsp` returned `No such tool`; no LSP device/server could answer status, definitions, references or diagnostics. Source analysis therefore used direct pinned-source reads; literal heading search located the permitted entry sections and was not treated as semantic proof.

## Clause-by-clause source review

Paths below are relative to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/`; R45src means round-45/frozen/src, R44src means round-44/frozen/src. Each filename:line names the corresponding pinned file above.

1. Store and parser chain: sysfs.c:2031-2046 defines the store, calls memparse at :2040, and commits the parsed value only at :2045. cmdline.c:153-156 calls simple_strtoull with base 0; vsprintf.c:112-114 forwards that base to simple_strntoull, and :79-100 contains that function including radix fixup at :86. Each cited line supports its attached claim, not just a nearby declaration.

2. Radix: kstrtox.c:28-35 selects hexadecimal only when the leading zero is followed by x/X and a hex digit, otherwise octal for a leading zero and decimal otherwise. kstrtox.c:37-38 skips a 0x/0X prefix when the resulting base is 16. The row's lowercase `0x` prefix wording follows its preceding explicit x/X case qualification; it does not exclude uppercase X. The cited condition and assignment lines are inside the same complete function (:26-40).

3. Digit scan and negative text: kstrtox.c:65-78 checks numeric digits or case-insensitive a–f, breaks for other characters, and rejects a digit value outside the base. vsprintf.c:89-98 advances by the consumed count with the overflow flag removed and returns that pointer. Thus the row's `first` invalid character description is supported for the sysfs inputs discussed, and a leading minus remains unconsumed. There is no sign-skipping wrapper in vsprintf.c:79-114. The parser also has a max_chars bound, passed as INT_MAX here; the row is describing sysfs writes, not promising unbounded parsing of arbitrary strings.

4. Suffix conditions and order: cmdline.c:160-186 lists E/e, P/p, T/t, G/g, M/m, K/k, each level contributing ten bits by fallthrough. :189 requires both a recognized suffix shift and `ptr != endptr`; with base 0, prefix skipping requires at least a valid following hex digit (kstrtox.c:30-38), so this does establish a preceding parsed digit in this call chain. :191-192 saturates shifted overflow to ULLONG_MAX. :193 advances once, not repeatedly. Therefore `at most one`, case-insensitivity, the digit prerequisite, the 1024 multiplier, and the overflow result are all supported. I checked the surrounding branches as well as the quoted K and M lines. The quoted overflow-consumption comment at cmdline.c:159 is consistent with the actual unconditional increment within :189's qualifying branch.

5. Store rejection and mutation boundary: sysfs.c:2040 parses before :2042's skip_spaces call; :2043 checks the remaining byte and :2044 returns -EINVAL before :2045 writes. No earlier errno branch appears in this store and there is no hidden success-before-validation path in :2031-2046. Successful stores return len at :2046. This supports the row's errno and ordering, without claiming that VFS/permissions cannot reject a write before the store is called.

6. Examples checked by tracing: decimal 100 with either M or m gives 100 shifted by 20 = 104857600 (cmdline.c:177-183); octal 010 yields 8 and hexadecimal 0x10 yields 16 (kstrtox.c:28-38,65-78). For 10MB only M is consumed and B remains (cmdline.c:193; sysfs.c:2043-2044). For 10 M the suffix switch sees a space rather than M, so even after whitespace skipping M remains. For -1 the minus remains. Those three examples therefore reach EINVAL under the explicitly stated whitespace-helper assumption. A bare newline consumes no digit and leaves the initialized zero result (vsprintf.c:82,89-100; kstrtox.c:64-78,93-94); under the row's explicit whitespace and buffer-termination assumptions it reaches WRITE_ONCE with zero. These are source-derived traces, not experimental sysfs writes.

7. Zero and timeslice: scrub.c:1380 reads the attribute, :1381-1382 immediately returns on zero. The comment at scrub.c:1368-1369 explicitly states bandwidth-limit-based throttling with a one-second timeslice, and :1374 sets 1000. The row's removal of this throttle limit is supported; it does not promise unlimited actual disk throughput. I also opened the unquoted scrub.c:1400-1401 citation: it adds bio_size to throttle_sent and compares that against the divided bandwidth limit, consistent with the expressly inferred bytes-per-second interpretation.

## Quotes, ranges and inference boundaries

I compared all 30 GR1 quotes to the displayed pinned lines, including the leading `*` on cmdline.c:147. Groups checked: cmdline.c:147,156,159,177-178,183,189,191-193; vsprintf.c:86,91,114; kstrtox.c:29-30,33,35,37-38,70,75,77; sysfs.c:2040,2042-2044; scrub.c:1368-1369,1381-1382. Quotes match the source-line text subject to the entry/linter's whitespace normalization. They support the associated claims when read with their actual branches.

No prose range used for GR1 runs into a following function: kstrtox.c:30-31 and :37-38 are within radix fixup; cmdline.c:161-184 and :191-192 are inside memparse; scrub.c:1368-1369 is the throttle comment, :1381-1382 is its zero branch, and :1400-1401 is inside the same throttle. The Limits section openly distinguishes declared evidence ranges from whole-file pin coverage; the Range gaps block explicitly includes S246 kstrtox.c:70,75,77 and S242 scrub.c:1400-1401. I did not mistake omitted declared-range lines for unavailable snapshot bytes.

The inference labels are material and appropriate: skip_spaces' implementation is outside these snapshots, so its exact character class is not directly proved here. The bare-newline example separately labels sysfs buffer NUL termination, which this store assumes rather than establishes. The byte unit is marked inference; the local variable/comment evidence is consistent, but a complete proof of bio_size's unit would require caller tracing outside the row's quoted range. The Arch/upstream equivalence and ordinary permission/ACL/LSM qualifications are likewise not asserted as direct observations. No additional unmarked speculative clause was identified within this limited source analysis.

## Host reading

round-45/frozen/hostcap/capture.txt:1 records uid=1000 and CapEff=0000000000000000; :2 records 7.2.11-arch1-1; :8 records the UUID's devinfo/1/scrub_speed_max with mode=644, owner=root, value=0; :9 records devids=1 for that captured filesystem. These support the reported captured device/value and the explicitly qualified ordinary-mode inability to change the root-owned attribute. The capture is not an enumeration of all possible unmounted filesystems or a permissions experiment; I read “the host's one btrfs device” as the one device in the captured filesystem, not an independent host-wide inventory. Under the row's stated unchanged-kernel assumption, scrub.c:1380-1382 supports the no-limit interpretation. No write, privilege escalation, ACL inspection or live host test was performed.

## Residual risk and verification gaps

No code or tracked lane content was changed, no admission mark was written, and no tools were installed. I did not check GR2/GR3 semantics, external skip_spaces/sysfs buffering implementations, the Arch patch, effective ACL/LSM policy, or run a live scrub/write. Those limits are not hidden passes. This review makes no runtime/rerouting/saturation/resume claim; those contracts are outside this assigned knowledge row.

Self-evaluation: accuracy 4/5 (external-helper and host assumptions remain explicitly unverified); completeness 4/5 (all GR1 clauses/quotes checked, no live write by design); clarity 4/5 (source aliases above require that mapping); actionability 5/5 (bound verdict and no requested corrections); conciseness 4/5 (detailed clause coverage is necessarily longer than the mechanical receipt). Overall 4.2/5. Highest-impact further evidence would be independent helper/buffer and Arch-patch verification, outside this seat's pinned-source scope. The scoped verdict does not promote those assumptions into observed facts.
