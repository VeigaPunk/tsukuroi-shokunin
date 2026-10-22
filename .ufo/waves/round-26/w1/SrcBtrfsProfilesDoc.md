# Source S130 — btrfs-progs v7.1 block group profiles and their copies (SrcBtrfsProfilesDoc)

Verdict: done. The btrfs-progs v7.1 documentation was opened by plain curl at the named path, the exact fetched bytes are saved as `.ufo/waves/round-26/sources/S130.rst` (sha256 `ce7c0cbca90eda4bc84040e9f5a43c227bd02d77bd50b006e481f19d918de769`, 723 lines), and its PROFILES table states one redundancy copy for `single` and two for `DUP`. The file therefore supports the copy-count half of declared row SH3, and it limits the wording of SH3's second half rather than grounding it: it says nothing about scrub verification or repair.

## 0. Fetch, tag verification and file location

1. The file was fetched at the path the assignment named and was not moved. [obs] `curl -sS -o /tmp/S130_mkfs.rst -w "HTTP %{http_code} size=%{size_download}\n" https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/mkfs.btrfs.rst` → `HTTP 200 size=29867`. The saved snapshot is `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S130.rst`; `sha256sum` → `ce7c0cbca90eda4bc84040e9f5a43c227bd02d77bd50b006e481f19d918de769`, `wc -lc` → `723 29867`, and `cmp` against the fetched temporary copy reported `IDENTICAL`.

2. The tag `v7.1` exists. [obs] `curl -sSL -o /tmp/rel.html -w "%{http_code} url=%{url_effective}\n" https://github.com/kdave/btrfs-progs/releases/tag/v7.1` → `200 url=https://github.com/kdave/btrfs-progs/releases/tag/v7.1`, and the page title is `Release v7.1 · kdave/btrfs-progs · GitHub`. A control fetch of a nonexistent tag path, `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1-does-not-exist/Documentation/mkfs.btrfs.rst`, returned `404`, so the `200` above is specific to the `v7.1` tag. The commit linked on that release page, `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`, serves a byte-identical `Documentation/mkfs.btrfs.rst` (same sha256 when fetched by commit sha), which ties the snapshot to the release commit. [unk] The unauthenticated GitHub REST endpoints (`/git/ref/tags/v7.1`, `/commits/v7.1`) returned `HTTP 403` from this host, so the tag identity rests on the release page and on the byte-identical commit fetch, not on the API.

3. The file includes no `ch-*.rst`, and none exists under `Documentation/` at that tag. [obs] `grep -n "include::\|only::\|ch-"` over the snapshot returns no line, and a probe of `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-btrfs.rst` returned `HTTP 404`. The PROFILES section is at line 508 of `Documentation/mkfs.btrfs.rst` itself, so the one file that states the copies per profile for `single` and `dup` is the file the assignment named. [obs] Other candidates probed at the same tag and rejected: `Documentation/btrfs.rst` (`HTTP 200`, 5782 bytes) is the `btrfs(8)` toolbox manual and contains no profile table; `Documentation/btrfs-filesystem.rst` (`HTTP 200`, 24932 bytes) mentions profiles but states no per-profile copy counts; `Documentation/btrfs-scrub.rst` (`HTTP 200`, 8838 bytes) is about scrub, not about copies.

## 1. Proposed SOURCES row

`| S130 | btrfs-progs v7.1 mkfs.btrfs(8) block group profiles and their redundancy copies — https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/mkfs.btrfs.rst | docs | A | Copies per block group profile for single and DUP, and what DUP means on one device, for the installed btrfs-progs 7.1-1 | tag v7.1, Documentation/mkfs.btrfs.rst lines 508-521 (PROFILES table and its Copies column), lines 632-641 (DUP PROFILES ON A SINGLE DEVICE); raw bytes sha256 ce7c0cbca90eda4bc84040e9f5a43c227bd02d77bd50b006e481f19d918de769 | single keeps one copy and DUP two, but on a single SSD device the DUP pair may be deduplicated to one physical copy | mined | 2026-10-22 | on-release | corpus/knowledge/storage-health-r26.md |`

The row has the eleven contract cells and no `|` inside any cell. [obs] The shape matches the existing rows in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md` (for example S115 at line 121 and S126 at line 132), whose anchor cells read `tag v7.2, lines 45-49 (...); raw bytes sha256 ...`.

## 2. Four exact quotes grounding declared row SH3

Each quote is byte-for-byte from the saved snapshot `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S130.rst`, at the stated line numbers, and each is at most 25 words. [obs] I verified with a Python check that the whitespace-normalised text of each quote is a substring of the whitespace-normalised snapshot: `Q1` line 518, 11 words, `True`; `Q2` line 520, 17 words, `True`; `Q3` lines 635-636, 21 words, `True`; `Q4` lines 639-640, 23 words, `True`.

Q1 — `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S130.rst:518` (the `single` row of the PROFILES table; the column header at line 516 reads `Copies`):

```
| single   |  1            |            |            | 100%              | 1/any              |
```

Q2 — `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S130.rst:520` (the `DUP` row of the same table):

```
| DUP      |  2 / 1 device |            |            |  50%              | 1/any (see note 1) |
```

Q3 — `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S130.rst:635-636` (first sentence of the DUP-on-a-single-device section):

```
The mkfs utility will let the user create a filesystem with profiles that write
the logical blocks to 2 physical locations.
```

Q4 — `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S130.rst:639-640` (the SSD caveat that bounds the DUP guarantee):

```
For example, a SSD drive can remap the blocks internally to a single copy--thus
deduplicating them. This negates the purpose of increased redundancy
```

## 3. Does the source support, limit or contradict the declared SH3 wording?

Declared SH3, quoted from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:894`: "SH3 what scrub verifies and when it can repair: with the data profile `single` a data checksum error is detected but not repaired, and the `dup` metadata profile keeps a second copy."

1. Supports the copy-count half of SH3. [obs] The PROFILES table gives one redundancy copy for `single` (line 518) and two for `DUP` (line 520), under a column headed `Copies` (line 516). So the declared clause "the `dup` metadata profile keeps a second copy" is exactly what the table states, and the declared clause "the data profile `single`" is the profile whose table row carries a single copy.

2. Limits SH3: this file says nothing about scrub verification or repair. [obs] A case-insensitive grep of `scrub` and `repair` over the whole snapshot returns exactly one line, `S130.rst:665`: `In any case, a device that starts to misbehave and repairs from the DUP copy`, and that sentence is about replacing a device that misbehaves, not about scrub repair semantics. The declared half "a data checksum error is detected but not repaired" therefore cannot be grounded by S130; it must be carried by the scrub source S129 (`Documentation/btrfs-scrub.rst`), whose bytes are a different seat's snapshot. [inf] The inference from one copy to "no repair from a second copy" is sound only in combination with that scrub source, because detection and repair are scrub behaviours, not profile properties.

3. Limits SH3's wording on "a second copy". [obs] Lines 635-641 and 665-666 qualify what DUP guarantees on one device: `physical copies highly depends on the underlying device type.` (line 637), `wastes filesystem space without providing the expected level of redundancy.` (line 641), and `should be replaced! **DUP is not backup**.` (line 666). [inf] The declared wording "keeps a second copy" is therefore correct as a statement about a second logical copy, and would be too strong if the entry were written as "keeps a second physical copy" or as a backup guarantee. This is a limit on the phrasing, not a contradiction of the declared text.

4. Contradicts nothing in the declared SH3 text. [obs] No line of the snapshot contradicts the profile names, the copy counts, or the direction of the SH3 claim. The only wording the source narrows is the strength of "second copy", as in finding 3.

## 4. Anything that contradicts the frozen capture's host facts

1. No contradiction with the captured profile assignment. [obs] The capture at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt` shows the file `single` under `allocation/data` and the file `dup` under `allocation/metadata` and `allocation/system`. The snapshot's own example output matches that triple at `S130.rst:692-695`:

```
       Block group profiles:
         Data:             single            8.00MiB
         Metadata:         DUP              40.00MiB
         System:           DUP              12.00MiB
```

2. One host fact is bounded by this source rather than contradicted by it. [obs] The capture shows one device, `/dev/mapper/root` on `nvme0n1p2` of `/dev/nvme0n1`, an NVMe SSD, and the metadata and system profiles are `dup`. The source says at `S130.rst:635-641` that a SSD can remap blocks internally to a single copy, deduplicating them, which "negates the purpose of increased redundancy", and at lines 665-666 that "DUP is not backup". [inf] The host's metadata DUP is therefore a second logical copy whose physical independence on that single SSD is not guaranteed by the profile alone; the capture cannot show whether the device deduplicates, because no btrfs or NVMe counter in the capture exposes that, so this is a limit on the redundancy claim and not an observed contradiction of a captured fact.

3. Consistency with the documented default, no conflict. [obs] `S130.rst:59-60` reads `Default on a single device filesystem is *DUP* and is recommended for metadata`, and line 69 reads `changed in version 5.15 to be always *dup*.` The host has `dup` metadata on a single-device filesystem, as the default would produce.

4. Nothing in this source speaks to the other captured facts. [obs] The snapshot contains no statement about the five btrfs error counters, their persistence, the scrub record, the `btrfs-scrub@.timer`, or the NVMe health fields, so it neither supports nor contradicts those capture lines. Rows SH1, SH2, SH4, SH5 and SH6 must be grounded by the other sources of this round.

## Verification gaps and bounds

- [unk] The GitHub REST tag and commit endpoints were unreachable from this host (`HTTP 403` unauthenticated), so the tag is evidenced by the release page, by the `404` control on a nonexistent tag, and by the byte-identical fetch of the release-page commit `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`.
- [inf] The claim that `4ab0e80…` is the tag object of `v7.1` is an inference from the release page link and the identical tree content; the API that would state the tag object directly was not reachable.
- [obs] No host state was changed. No package was installed, no service was started or stopped, no scrub was run, no counter was reset, no configuration was written, and no `git` or `jj` command was run against the lane repository or any other repository.
- [obs] The snapshot was written only to the sanctioned source path `.ufo/waves/round-26/sources/S130.rst`; this report is the only other file written.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:874-908 and :894 (declared rows SH1 to SH6); /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:116-133 (row shape); /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt (frozen host facts); https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/mkfs.btrfs.rst plus probe fetches of btrfs.rst, btrfs-filesystem.rst, btrfs-scrub.rst and ch-btrfs.rst at the same tag; https://github.com/kdave/btrfs-progs/releases/tag/v7.1; wrote=.ufo/waves/round-26/sources/S130.rst and .ufo/waves/round-26/w1/SrcBtrfsProfilesDoc.md; executed=curl fetches of the snapshot, the release page, the control 404 tag and the candidate documentation files; sha256sum and wc on the saved snapshot; cmp between the fetched and saved copies; grep over the snapshot for include directives, scrub, repair and profile lines; python3 substring and word-count verification of the four quotes
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
