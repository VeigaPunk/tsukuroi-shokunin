# RevS130 — wave-2 falsify of source S130 (btrfs-progs v7.1 Documentation/mkfs.btrfs.rst)

Verdict: holds. The re-opened bytes hash to the anchor digest and equal the committed snapshot; both Gate quotes for S130 in `corpus/lessons/round-26.md` are exact, at most 25 words, and sit at the stated lines; the row's scope, tier, teaches and used-by cells are accurate and not wider than the source; and every entry statement citing S130 is supported by it. No falsifying finding.

Method note: the lane working copy is at `7f9f08894fce41146f76fa5c3f3282037211555a` (3 dirty entries), ahead of the measured revision. All repository artifacts were read from a sandbox built with `git archive 7dfea9244a84a0e2439f0698e54491e5d7b7c467 | tar -x` (no git init needed; no lane write commands). The source URL was re-fetched by plain curl on 2026-10-22.

## Findings

1. [obs] Fetched bytes equal the anchor digest and the snapshot. `curl -fsSL https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/mkfs.btrfs.rst` (exit 0, 29,867 bytes) hashes to `ce7c0cbca90eda4bc84040e9f5a43c227bd02d77bd50b006e481f19d918de769`, which is the full digest in the anchor cell of `corpus/SOURCES.md:136`, and `diff -q` reports the fetched file identical to the sandbox copy of `.ufo/waves/round-26/sources/S130.rst` (same sha256, 723 lines).

2. [obs] Gate quote 1 is exact and at the stated line. `corpus/lessons/round-26.md:25` quotes "For example, a SSD drive can remap the blocks internally to a single copy--thus" at "mkfs.btrfs.rst line 639, entry row SH3". Programmatic check on the snapshot: `splitlines()[638]` equals the quote byte for byte (14 words, at most 25; whitespace-normalised text is a substring of the whole snapshot).

3. [obs] Gate quote 2 is exact and at the stated line. `corpus/lessons/round-26.md:27` quotes "The mkfs utility will let the user create a filesystem with profiles that write" at "mkfs.btrfs.rst line 635, entry row SH3". `splitlines()[634]` equals the quote byte for byte (14 words). These are the only two S130 rows in the Gate table; no other lesson quote cites S130.

4. [obs] The anchor's line ranges are accurate. Range "lines 508-521 (PROFILES table and its Copies column)": snapshot line 508 is the `PROFILES` heading, 513-521 are the table grid whose `Copies` column header is line 516, `single` (1 copy) is line 518 and `DUP` (2 / 1 device) is line 520, with 521 the DUP row's closing separator; the RAID rows the row does not claim begin at 522, so the range is not wider than the taught scope. Range "lines 632-641 (DUP PROFILES ON A SINGLE DEVICE)": line 632 is that section heading and line 641 is "wastes filesystem space without providing the expected level of redundancy.", containing both quote lines.

5. [obs] The row's cells are accurate and not wider than the source. Scope cell "Copies per block group profile for single and DUP, and what DUP means on one device, for the installed btrfs-progs 7.1-1": `pacman -Q btrfs-progs` returns `btrfs-progs 7.1-1`, and the pinned tag v7.1 upstream file delivers exactly the copies table (lines 518, 520) and the DUP-on-one-device chapter (632-641). Teaches cell "single keeps one copy and DUP two, but on a single SSD device the DUP pair may be deduplicated to one physical copy": line 518 (`single`, 1), line 520 (`DUP`, 2 / 1 device), lines 639-640 (SSD "can remap the blocks internally to a single copy--thus deduplicating them"); the hedged "may" also matches the doc's own qualification that "not all blocks get deduplicated". Tier `docs`, status `mined`, opened `2026-10-22`, recheck `on-release`, and used-by `corpus/knowledge/storage-health-r26.md` all match the lesson's admitted-rows record and the row text.

6. [obs] Every entry statement citing S130 is supported. In `corpus/knowledge/storage-health-r26.md` S130 appears in the header source list and in row SH3. SH3's S130-dependent clauses: "With the data profile `single` there is one copy" (line 518); "Metadata with `dup` has two logical copies on the same device" (lines 635-636 "write the logical blocks to 2 physical locations" plus line 520 "2 / 1 device"); "but an SSD may store both as one physical copy" (lines 639-640). The remaining SH3 clauses (repair only from a replicated copy; `single` data error uncorrectable; NOCOW not verified) are carried by S139 and S129, which SH3 cites alongside S130. The "How this changes OS triage" bullet and the entry's Limits section ("Whether the SSD deduplicates the `dup` metadata copies is not observable from the host") stay inside what S130 claims.

7. [obs] The machine-readable entry agrees. In `corpus/knowledge/storage-health-r26.json` the SH3 `statement` is identical to the markdown statement; its `sources` list is S139, S130, S129; its two S130 quotes have exactly the Gate table text with locations "mkfs.btrfs.rst line 639" and "mkfs.btrfs.rst line 635" (json lines 156-159 and 166-169). The C1 receipt `measure/c1-ef72f10d.json` records the line-639 S130 quote with all checks true and 14 words.

8. [obs] No stray use. `corpus/knowledge/memory-pressure-r25.md` contains no S130 or mkfs reference, correct for a source whose used-by names only the storage-health entry; a sandbox-wide sweep finds no other lane file claiming S130 beyond the registry row, the lesson Gate rows, the entry, the C1 tool's internal fixtures, and the wave-1 records.

## Residual risk and verification gaps

- The anchor pins upstream tag v7.1 while the scope cell says "for the installed btrfs-progs 7.1-1". `pacman -Q` confirms 7.1-1 installed [obs]; that the packaged 7.1-1 man page renders this exact rst text was not verified byte-for-byte against the installed manual [unk]. The wave-1 seat verified the release tag exists and a control 404, and S131's record already establishes the Arch packaging channel for the unit; this residual is the same channel assumption, judged small.
- Whether the host's SSD actually deduplicates the `dup` metadata pair is undisclosed by the source and unmeasured; the entry already records this limit, so it is not a defect here.
- All findings apply to the measured revision `7dfea9244a84a0e2439f0698e54491e5d7b7c467`; the working copy has since moved to `7f9f0889` and was not checked for later mutations of these files.
- The C1 counting tool was not re-run by this seat; the receipt and the checker's fixture constants referencing S130 were read, not executed.

Report: .ufo/waves/round-26/w2/RevS130.md

Scope: read=sandbox archive of 7dfea924 (corpus/SOURCES.md:136, corpus/lessons/round-26.md, corpus/knowledge/storage-health-r26.md and .json, corpus/knowledge/memory-pressure-r25.md, .ufo/waves/round-26/sources/S130.rst, SCORECARD.md round-26 sections, wave-1 seat reports and c1 receipt) plus curl re-fetch of the v7.1 URL; wrote=.ufo/waves/round-26/w2/RevS130.md, /fast/scratch/hyaku/tsuku26/w2/RevS130/ (sandbox and fetched copy); executed=git archive (read-only), curl, sha256sum, diff, wc, pacman -Q btrfs-progs, python quote/line checks
Model: zai/glm-5.3-flash
Installs: none
