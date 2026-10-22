# RevS139: re-open of source S139 (btrfs-progs v7.1 Documentation/ch-scrub-intro.rst)

Verdict: partly holds. The fetched bytes, the tag, the include line, the installed version and all six Gate quotes check out, but the entry statement that ordinary reads verify checksums overreaches S139 for NOCOW data, and the row teaches cell is wider than the source in two places.

Convention: lane file citations are at revision 7dfea9244a84a0e2439f0698e54491e5d7b7c467, read with git show or git grep, unless a path is marked as a working copy. The S139 row is line 145 of corpus/SOURCES.md at that revision. The snapshot is .ufo/waves/round-26/sources/S139.rst, which is byte-identical to the fetched upstream file.

## Findings

1. [medium] The entry statement for row SH4 overreaches S139 for NOCOW data. It is at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/storage-health-r26.md line 57 at the revision, and its JSON twin is corpus/knowledge/storage-health-r26.json line 180. The sentence reads: "Ordinary reads do verify checksums, so data that was read has been checked, but no record shows a full pass over stored data."
   - S139 does not say that reads verify checksums. Its line 17, which the entry quotes at md line 65, reads "Such automatic repair is also carried out when reading metadata or data from a", and line 18 continues "read-write mounted filesystem." That sentence describes automatic repair on reads of replicated profiles (line 13), not checksum verification. [inf: the closest S139 support for read-time checksum checking is line 28, "damage is detected by", which the entry does not quote.]
   - S139 says the opposite for NOCOW files, inside the anchored range 20-35. Line 28: "replicas. This is not a problem normally because damage is detected by". Line 29: "checksum validation, but because ``NOCOW`` files are". Line 30: "not protected by checksums, btrfs has no idea which mirror is good thus it can". Line 31: "return the bad contents to the user space tool."
   - The entry's own Limits section, md line 112, says: "NOCOW file data (systemd journals) is outside scrub; which files carry NOCOW on this host was not measured." So the unqualified sentence is unsupported for those files on this host.
   - The sentence holds for checksummed data. A fix would qualify it to checksummed data and cite lines 28 to 31 for the exception. [obs: the author may have meant non-NOCOW data by "ordinary", but the sentence as written covers all data read.]
   - The lane declaration repeats the same citation. SCORECARD.md line 916 at the revision says: "ordinary reads also verify checksums (S139 lines 17-18)".

2. [low] The row teaches cell says "reads also repair" with no conditions (corpus/SOURCES.md line 145, teaches column). S139 lines 13 to 18 limit read repair to replicated block group profiles on a read-write mounted filesystem. The entry Gate quote (md line 65; corpus/lessons/round-26.md line 30) stops before "read-write mounted filesystem." On this host the root is read-write (.ufo/waves/round-26/capture/capture.txt line 26 mount options begin "rw,noatime"), but the data profile is single (capture line 64: "single"). So for this host's data, reads do not repair, and the cell as written is wider than the source.

3. [low] Qualifiers from S139 are dropped in the teaches cell and in SH3. "NOCOW file data has no checksums" drops the opening of line 21, "As currently implemented, setting the ``NOCOW`` file attribute (by". The teaches phrase "systemd sets NOCOW on journals" drops "by default" from line 35, "systemd sets +C on journals by default". The installed man page keeps the qualifier at line 61 of /usr/share/man/man8/btrfs-scrub.8.gz, decompressed. [obs]

4. [low] Two uses of "only" rest on lines outside the anchored ranges. The teaches cell says "Scrub repairs only from a replicated profile by copying verified good data", and SH3 says "it repairs a bad block only by copying a verified good copy from another replica". The support is S139 line 43, "filesystem damage by copying from other known good replicas." The row anchor lists lines 1-3, 13-18, 20-35 and 67-74 (SOURCES.md line 145, anchor column), so line 43 is not pointed to. The text is true of the file. [obs]

5. [low] The SH3 dup clause is cited to S139, but S139 never names DUP. SH3 says: "Metadata with `dup` has two logical copies on the same device and can be repaired from the second, but an SSD may store both as one physical copy." The snapshot has zero matches for "DUP". Its only "dup" text is the directive ".. duplabel:: scrub-io-limiting" on line 80. The repair-from-the-DUP-copy support is S130 line 665, "In any case, a device that starts to misbehave and repairs from the DUP copy", and S129 line 80, "group profiles with redundancy. No-repair can be enabled by option *-r*." The entry quotes neither. The S130 quote it does use, line 639, supports only the SSD deduplication point. [obs]

6. [low] The SH3 single-profile clause, "detected and reported as uncorrectable, not repaired", is not supported by S139. The snapshot has zero matches for "single" and zero for "uncorrect". S139 supports only the replicated-profile precondition at line 13. The word "Uncorrectable" comes from S129. The entry cites it as "btrfs-scrub.rst line 190" (md line 51, corpus/lessons/round-26.md line 26, and the JSON SH3 quote). The quoted text is at line 192 of .ufo/waves/round-26/sources/S129.rst, and line 190 is blank. That Gate location is wrong. S129 belongs to another seat; I flag it because the SH3 source list cites it. [obs]

7. [low] The used-by cell names only corpus/knowledge/storage-health-r26.md. corpus/knowledge/storage-health-r26.json also cites S139, in rows SH3 and SH4, at revision lines 135, 141, 146, 151, 185, 191, 196 and 201. The markdown-only pattern matches the sibling rows S128 to S135, so the cell is incomplete by convention, not wrong. [obs]

8. [low] The SH4 source list cites S139 line 68, "recommended period is a month but it could be less." No SH4 statement uses it. The monthly-timer claim rests on S131. [obs]

## Checks that hold

- Fetch. `curl -sS -L` of https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-scrub-intro.rst returned HTTP 200 and 5738 bytes, with sha256 c3b9d344e11d842e2aed43d191b120572753bb75e8bbedd5b3e10978d24c3485. That equals the row anchor, and `cmp` reports it byte-identical to .ufo/waves/round-26/sources/S139.rst.
- Tag. The GitHub API ref refs/tags/v7.1 is annotated tag object 0a919c7d6e389c07920675b7fad3f793b92aa78b. That object peels to commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b, the same peel the S128 row records. The commit-pinned raw URL returns the same digest.
- Scope include. Upstream Documentation/btrfs-scrub.rst at v7.1 line 12 is ".. include:: ch-scrub-intro.rst", with fetched sha256 7900b474aebfee2be79ff168c750f282ee33803ee6914928c20117a24aefe3f0.
- Installed version. `pacman -Q btrfs-progs` gives "btrfs-progs 7.1-1", and `btrfs --version` gives "btrfs-progs v7.1". The installed /usr/share/man/man8/btrfs-scrub.8.gz carries the same sentences as the chapter, at decompressed lines 51-52, 55, 61, 64, 122 and 125-126. So "for the installed btrfs-progs 7.1" holds.
- Gate quotes, corpus/lessons/round-26.md lines 22-24 and 28-30. All six are exact substrings of the stated S139 lines (13, 14, 24, 71, 68 and 17), with 10 to 14 words each. No whitespace normalisation was needed.
- Entry quotes. The markdown quotes (md lines 51 and 65) and the JSON quotes for rows SH3 and SH4 match the Gate quotes exactly. The markdown and JSON statements for SH3 and SH4 are identical strings.
- Clauses that hold. S139 line 1 supports "Scrub reads all data and metadata and checks checksums": "Scrub is a validation pass over all filesystem data and metadata that detects". Line 24 supports "scrub does not verify" NOCOW file data: "be validated and corrected by scrub, the actual file data is not." Line 35 supports systemd setting NOCOW on journals. Lines 71 and 72 support the status-file path.
- Row fields. Kind docs, tier A, status mined, opened 2026-10-22 and recheck on-release all match the sibling rows S128 and S130. [unk] The pinned corpus/SOURCES.md has no tier legend that I could find.
- Frozen capture. .ufo/waves/round-26/capture/capture.txt hashes to 002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd, as the entry states.

## Residual risk and verification gaps

- [unk] I did not run tools/check-storage-health.py or any other lane checker. I therefore did not test whether the checker accepts these S139 rows.
- [unk] No one has measured whether journal files on this host carry NOCOW, so the practical effect of finding 1 on this host is unknown.
- [inf] The single-profile and dup repair outcomes in findings 5 and 6 are sound btrfs behaviour as S129 and S130 describe it. S139 is not their source.
- [unk] I compared only the listed sentences of the installed man page with the upstream chapter, not the whole page.

Scope: read=lane revision 7dfea9244a84a0e2439f0698e54491e5d7b7c467 via git show and git grep (corpus/SOURCES.md, corpus/lessons/round-26.md, corpus/knowledge/storage-health-r26.md and .json, corpus/README.md lines 238-240, SCORECARD.md lines 912-921, SKILL.md by grep), lane files .ufo/waves/round-26/sources/S129.rst, S130.rst and S139.rst, .ufo/waves/round-26/capture/capture.txt, upstream kdave/btrfs-progs v7.1 ch-scrub-intro.rst and btrfs-scrub.rst (branch and commit 4ab0e80 URLs), GitHub API tag refs for v7.1, installed /usr/share/man/man8/btrfs-scrub.8.gz; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RevS139.md and scratch copies under /fast/scratch/hyaku/tsuku26/w2/RevS139/; executed=git show, git grep, git cat-file, git rev-parse, git log (all read-only), curl against raw.githubusercontent.com and api.github.com, sha256sum, cmp, zcat, pacman -Q btrfs-progs, btrfs --version, python3 string and JSON checks, grep, sed, cat -n
Model: anthropic/claude-haiku-5-5
Installs: none
