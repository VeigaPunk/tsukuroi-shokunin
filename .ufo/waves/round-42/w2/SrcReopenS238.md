VERDICT: supports

# F-12 — Re-open S238 (btrfs-progs v7.1 CHANGES), seat SrcReopenS238, round-42 w2

Item: fetch https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/CHANGES, compare sha256 with the row
anchor, check lines 460-470 and the `teaches` cell (6.6.3 scrub limit entries), and judge whether `docs` is the
right kind and `A` the right tier for release notes. All four checks pass; the S238 row as declared
(`corpus/SOURCES.md:247`) is supported. One observation on the record's SC5 quotes (line 469 unquoted) is
carried below; it was already raised by wave-1 seats and is not a defect of the S238 row.

## 1. Fetch and digest — matches the row anchor exactly

Fetched 2026-10-26T20:45:24Z from the raw URL with `curl -sSfL -o CHANGES.fetched
https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/CHANGES` (exit 0). Observed:

```
$ sha256sum CHANGES.fetched <frozen>/CHANGES
bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22  CHANGES.fetched
bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22  .ufo/waves/round-42/frozen/src/CHANGES
$ cmp CHANGES.fetched <frozen>/CHANGES   # exit 0, no output -> byte-identical
$ wc -l CHANGES.fetched
2357 CHANGES.fetched
```

- The digest equals the S238 row anchor (`corpus/SOURCES.md:247`: "raw bytes sha256
  bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22") and the pinned `SHA256SUMS` line 2
  (`.ufo/waves/round-42/frozen/src/SHA256SUMS:2`). The live tag serves the same bytes the L1 pinned on
  2026-10-26 (FETCH.txt:1-3); the snapshot is faithful and stable.
- Tag identity re-verified independently of the fetch log: `git ls-remote https://github.com/kdave/btrfs-progs
  v7.1 'v7.1^{}'` → `0a919c7d6e389c07920675b7fad3f793b92aa78b  refs/tags/v7.1` and
  `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b  refs/tags/v7.1^{}` — the annotated tag and its peeled commit match
  FETCH.txt:1 and the record's `verified-at` line (`corpus/knowledge/btrfs-scrub-record-r42.md:2`).
- Receipts: `.ufo/waves/round-42/w2/SrcReopenS238/receipt-fetch.txt` (commands + outputs),
  `CHANGES-v7.1-fetched` (the fetched bytes, 93779 bytes), `CHANGES-lines-459-471.txt` (numbered excerpt).

## 2. Lines 460-470 — the 6.6.3 entry says what the row and the record quote

Raw read of the fetched file, lines 460-470 (receipt `CHANGES-lines-459-471.txt`):

```
460  btrfs-progs-6.6.3 (2023-12-14)
461  """"""""""""""""""""""""""""""
462     * subvol create: accept multiple arguments
463     * subvol delete: print the subvolume id in the output
464     * subvol sync: check if the filesystems is still writeable so it does not
465       wait indefinitely
466     * device delete: add a timeout and warning when deleting multiple devices
467     * scrub status: report limit if set in sysfs/../scrub_speed_max
468     * scrub limit: new command to show or set the per-device scrub limits
469     * scrub start: report the limit if set
470     * build:
```

- All three S238 quotes in the record reproduce exactly: CHANGES:460 "btrfs-progs-6.6.3 (2023-12-14)",
  CHANGES:467 "* scrub status: report limit if set in sysfs/../scrub_speed_max", CHANGES:468 "* scrub limit:
  new command to show or set the per-device scrub limits" (`corpus/knowledge/btrfs-scrub-record-r42.md:134,136,138`).
  The record's quotes omit the three leading spaces of 467/468; the counter binds quotes as substrings of the
  snapshot line (`q in src[n - 1]`, `tools/check-scrub-record-r42.py:196`), so the trimmed quotes match the
  snapshot lines exactly as substrings and QUALITY 79's line binding holds without any normalization. Wave-1
  C2RevCounter already scored SC5 5/5/0 good/in-window/bad (`.ufo/waves/round-42/w1/C2RevCounter.md:16`).
- The anchor window "CHANGES lines 460-470 (btrfs-progs-6.6.3 entry)" (`corpus/SOURCES.md:247`) covers the
  entry header (460) and all three scrub-limit entries (467-469). The full 6.6.3 entry runs to line 477; the
  anchor pins the subset the row relies on, which is the correct narrowing.
- Observation (not a defect of S238): line 469 "* scrub start: report the limit if set" lies inside the frozen
  window and is the only upstream support for SC5's "and `btrfs scrub start` read[s] it and report[s] a set
  limit ... all three arrived in btrfs-progs 6.6.3" clause (`btrfs-scrub-record-r42.md` SC5 statement), but the
  record quotes only 460/467/468. Wave-1 flagged this as a strengthening suggestion, not a row change
  (`.ufo/waves/round-42/w1/C2CritNovelty.md:179-180`; `.ufo/waves/round-42/w1/C2DraftRevSC5.md:50-51`), and the
  record at tip still carries five SC5 quotes without 469. The counter requires only ≥1 good in-window quote per
  row (`tools/check-scrub-record-r42.py:205`), so the predicate does not bind 469. I verified the line exists
  and reads exactly as the suggestion quotes it, so the suggestion remains valid and open for the SC5 seats /
  L1.

## 3. The `teaches` cell — supported by the 6.6.3 scrub limit entries

- Teaches cell: "Which btrfs-progs release introduced a scrub command or status behaviour"
  (`corpus/SOURCES.md:247`). The anchored entry answers it for the per-device scrub limit: line 468 says the
  limit command is new ("scrub limit: new command to show or set the per-device scrub limits") and lines 467/469
  say the status and start reporting behaviours are new in the same release. The claim cell "The per-device
  scrub limit and its status report arrived in btrfs-progs 6.6.3" is exactly what lines 467-468 state (469 adds
  the start report that SC5's "all three" counts).
- Scope is honest: the 6.6.3 entry references the kernel-side sysfs path as already existing ("if set in
  sysfs/../scrub_speed_max", line 467); the row claims only the btrfs-progs command/behaviour introduction, not
  the kernel-side introduction of the attribute. Wave-1 recorded the same boundary
  (`.ufo/waves/round-42/w1/C2DraftRevSC5.md:53`, gap (c)). Nothing in lines 460-470 contradicts the cell.
- This row also closes the round-26 lead "btrfs-progs 7.x release notes ... remain unopened"
  (`corpus/SOURCES.md:341`, lead listed at `:336`): the release notes are now opened, at the v7.1 tag, at the
  narrow scope the entry needs.

## 4. Kind `docs` and tier `A` — right for release notes

- Kind: CHANGES is upstream prose release notes — not executable source (`code`), not own-work, not a dataset.
  The registry's own precedent treats upstream NEWS/CHANGES/release pages exactly this way: pacman NEWS S006
  `docs`/`A` (`corpus/SOURCES.md:12`), systemd NEWS S024 and S199 `docs`/`A` (`:30`, `:208`), mkinitcpio release
  notes S015 and S053 `docs`/`A` (`:21`, `:59`). `docs` is the consistent kind.
- Tier: tier A is the registry's tier for primary/official sources (official news, man pages, upstream code at a
  pinned commit, own-work captures); ArchWiki sits at B and community/tool material at C (usage survey:
  S161 ArchWiki `docs`/`B` at `:167`; S036/S037 community `C` at `:42-43`; S030/S033 tool `C` at `:36-39`;
  QUALITY 7 points at the tier definitions in SOURCES.md, `corpus/QUALITY.md:11`). S238 is the upstream
  project's own changelog for the exact tag the host's package is built from (btrfs-progs 7.1-1), pinned to an
  immutable tag whose peeled commit I re-verified, digest-pinned in SHA256SUMS, and authoritative for precisely
  the claim drawn from it (which release introduced a command/behaviour). Tier `A` is right; tier C is never
  sole support and nothing here needs C.
- Recheck `on-release` (`corpus/SOURCES.md:247`) matches the anchor's nature: a tag URL is immutable, so the
  only recheck trigger is a new release, and the record's recheck procedure names exactly this re-fetch and
  digest comparison (`btrfs-scrub-record-r42.md:3`) — which this seat has now executed once with a matching
  result.
- Minor convention, consistent with S237: the row's URL field is the human-browsable blob URL
  (`https://github.com/kdave/btrfs-progs/blob/v7.1/CHANGES`) while the fetch log pins the raw URL that serves
  the bytes (FETCH.txt:3); the two serve identical content at the tag, and the digest anchors the bytes. No
  change needed.

## 5. What I did not do

- Did not re-run `tools/check-scrub-record-r42.py` (the C2 counter is other seats' item and the host-load rule
  allows at most one counter at a time); my quote checks against the snapshot were done directly.
- Did not verify the Arch 7.1-1 packaging patch-free claim myself; I rely on the record's Limits section citing
  wave-1 C2ExecLiveSources (`btrfs-scrub-record-r42.md` Limits; `.ufo/waves/round-42/w1/C2ExecLiveSources.md`).
- Did not determine the kernel-side introduction version of `scrub_speed_max` (the row makes no such claim).
- Did not fetch any other release's CHANGES or any other btrfs-progs file; scope was S238 only.

## 6. Residual risk

None material for the S238 row: digest, tag identity, line content, teaches cell, kind and tier all check out
against live upstream and the pinned snapshot. The one open item in reach of this source — adding the
`S238 CHANGES:469` quote to SC5 — is a strengthening already proposed in wave-1 and left to the SC5 seats/L1;
until it lands, SC5's "scrub start reports the limit" clause is supported by the anchored window but not
line-quoted in the record.
