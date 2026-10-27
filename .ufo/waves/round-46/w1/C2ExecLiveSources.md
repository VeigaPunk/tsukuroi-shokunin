VERDICT: supports

Scope: C2-S1 live source re-fetch / freshness. All eight S246–S248/S242–S244 source files and the S237 file were fetched with `curl -sfL URL -o FILE`; live digests were recorded in `.ufo/waves/round-46/w1/C2ExecLiveSources/sha256-live.txt`. The digest rows match the frozen manifests at `.ufo/waves/round-45/frozen/src/SHA256SUMS` (S246/S247/S248), `.ufo/waves/round-44/frozen/src/SHA256SUMS` (S242/S243/S244), and `.ufo/waves/round-42/frozen/src/SHA256SUMS` (S237). A sequential `cmp` batch against each corresponding frozen file was attempted, but stopped on the first comparison because the shell batch ran before its parallel downloads finished; therefore byte-for-byte `cmp` is **not established**. Matching SHA-256 digests provide strong byte identity evidence, not a successful observed cmp result.

| File | Frozen digest | Live digest | Identical (digest) | UTC time |
|---|---|---|---|---|
| cmdline.c (S246) | 1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d | 1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d | yes | 2026-10-27T05:22:16Z* |
| vsprintf.c (S246) | cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca | cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca | yes | 2026-10-27T05:22:16Z* |
| kstrtox.c (S246) | 0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4 | 0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4 | yes | 2026-10-27T05:22:16Z* |
| dev-replace.c (S247) | f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a | f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a | yes | 2026-10-27T05:22:16Z* |
| systemd.kill.xml (S248) | 448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72 | 448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72 | yes | 2026-10-27T05:22:16Z* |
| scrub.c (S242) | f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8 | f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8 | yes | 2026-10-27T05:22:16Z* |
| sysfs.c (S243) | ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43 | ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43 | yes | 2026-10-27T05:22:16Z* |
| btrfs-scrub@.service (S244) | eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252 | eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252 | yes | 2026-10-27T05:22:16Z* |
| scrub237.c (S237) | 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801 | 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801 | yes | 2026-10-27T05:22:16Z* |

*Timestamp is the shell-observed timestamp printed immediately after the fetch batch, not per-file transfer completion times. Source URLs and frozen digests are documented in the respective `FETCH.txt` and `SHA256SUMS`; S237 URL is in `corpus/SOURCES.md` row S237.

Tag pins re-resolved live with `git ls-remote`; exact output is in `.ufo/waves/round-46/w1/C2ExecLiveSources/tags.txt`. Peeled object IDs match the frozen pins: Linux v7.2.11 `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`; systemd v262 `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`; btrfs-progs v7.1 `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`. Re-fetch procedure notes are in `commands.txt`.

Evidence paths: `.ufo/waves/round-45/frozen/src/FETCH.txt` and `SHA256SUMS`; `.ufo/waves/round-44/frozen/src/FETCH.txt` and `SHA256SUMS`; `.ufo/waves/round-42/frozen/src/SHA256SUMS`; `corpus/SOURCES.md` row S237; receipts listed above. Risk/limitation: this scope did not retry `cmp` after observing its scheduling error; byte equivalence is supported by matching SHA-256 only, and timestamp is batch-level.