# S129 — btrfs-progs v7.1 `Documentation/btrfs-scrub.rst` (round 26, wave 1, seat SrcBtrfsScrubDoc)

Verdict: partly holds — the source opens at the pinned tag exactly as declared and supports the
declared SH3 and SH4 wording in mechanism (repair only with redundancy; scrub status read from
`/var/lib/btrfs`), but it limits both rows on one point each (it never names the `single`/`dup`
allocation profiles, and it never states the monthly cadence or the timer), and it does not
contradict the frozen capture.

## 1. Snapshot saved

| item | value |
|---|---|
| path | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S129.rst` |
| sha256 | `7900b474aebfee2be79ff168c750f282ee33803ee6914928c20117a24aefe3f0` |
| size / lines | 8838 bytes, 243 lines |
| fetch | `curl -sSL -o scrub.rst https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-scrub.rst` → HTTP 200, 8838 bytes |
| tag proof | `git ls-remote --tags https://github.com/kdave/btrfs-progs.git 'refs/tags/v7.1*'` → `0a919c7d6e389c07920675b7fad3f793b92aa78b refs/tags/v7.1` and `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b refs/tags/v7.1^{}` (annotated tag, peeled commit `4ab0e80b`) |
| byte proof | a shallow fetch of `refs/tags/v7.1` into a scratch clone (`/fast/scratch/hyaku/tsuku26/SrcBtrfsScrubDoc/vtag`) yields `Documentation/btrfs-scrub.rst` with the identical sha256 `7900b474…`, so the raw URL served the tag tree and not a moving branch |
| host pin | frozen capture line 12 `btrfs-progs 7.1-1` (`.ufo/waves/round-26/capture/capture.txt:12`), so tag `v7.1` is the installed release |

## 2. Proposed SOURCES row (11 columns, no `|` inside any cell)

```
| S129 | btrfs-progs v7.1 Documentation/btrfs-scrub.rst — https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-scrub.rst | docs | A | What btrfs scrub reads and verifies, when it repairs damaged copies, what scrub status reports and where the scrub status file lives, for the installed btrfs-progs 7.1 | tag v7.1 (peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b), Documentation/btrfs-scrub.rst lines 76-80, 133-138, 165-201; raw bytes sha256 7900b474aebfee2be79ff168c750f282ee33803ee6914928c20117a24aefe3f0 | Scrub repairs damaged copies by default only for block group profiles with redundancy and reports a checksum error with no other copy as uncorrectable; scrub status is read from the file in /var/lib/btrfs, so a filesystem with no /var/lib/btrfs has no scrub statistics at all | mined | 2026-10-22 | on-release | corpus/knowledge/storage-health-r26.md |
```

Note for the L1, not a deviation: the `used-by` cell is exactly the shape the assignment fixes. If
the round-25 convention of listing both the entry and its JSON is wanted, the only cell to touch is
`corpus/knowledge/storage-health-r26.md, corpus/knowledge/storage-health-r26.json`. `kind` `docs` and
`tier` `A` follow the round-25 rows for upstream release documentation at a pinned tag.

## 3. Exact quotes from the saved snapshot (each ≤ 25 words)

Verified by script over the committed bytes: each string below is a whitespace-normalised substring of
`.ufo/waves/round-26/sources/S129.rst`, and the line spans were read back from the saved file.

**Quote A — grounds SH3** (lines 78–80, 16 words):
`The automatic repairs of damaged copies are performed by default for block group profiles with redundancy.`

**Quote B — grounds SH3** (line 192, 15 words as printed; the asterisk-free tail is also a verified substring):
`*Uncorrectable* -- errors detected at read time but not possible to repair from other copy`
(asterisk-free form, 13 words, also a substring: `errors detected at read time but not possible to repair from other copy`)

**Quote C — grounds SH4** (lines 136–137, 19 words):
`If no scrub is running, show statistics of the last finished or cancelled scrub for that filesystem or device.`

**Quote D — grounds SH4** (lines 137–138, 10 words):
``The status is read from the file located in :file:`/var/lib/btrfs`.``

Supporting, not row-grounding, for the entry body: line 191 `*Corrected* -- number of bad blocks that were repaired from another copy`;
line 197 `*csum* -- checksum mismatch`; line 199 `*verify* -- metadata block header errors`; line 180 `Error summary:    no errors found`.

## 4. Findings

1. [obs] The declared URL resolves at the declared tag and the file did not move:
   `Documentation/btrfs-scrub.rst` returned HTTP 200 at tag `v7.1`, and the bytes are identical to
   that tag's tree file (sha256 `7900b474aebfee2be79ff168c750f282ee33803ee6914928c20117a24aefe3f0`,
   243 lines, 8838 bytes). Evidence: `curl -sSL -w "%{http_code}"` output `HTTP:200 SIZE:8838` and
   `git ls-remote --tags https://github.com/kdave/btrfs-progs.git 'refs/tags/v7.1*'`.

2. [obs] SH3 is supported in mechanism: repair is performed by default only for block group profiles
   with redundancy (Quote A, `.ufo/waves/round-26/sources/S129.rst:78-80`), and an error with no
   other copy is reported uncorrectable (Quote B, `:192`), with *Corrected* defined as a block
   "repaired from another copy" (`:191`). The document's own model of "detected but not repaired" is
   therefore the same as the declared wording.

3. [obs] SH3 is limited by the source on the profile names: the string `dup` does not occur anywhere
   in the file, and the only occurrences of `single` are "a single *device*" and "single-device
   filesystem" (lines 74, 104, 206). The `single`/`dup` half of the declared SH3 wording rests on
   S130 and on the capture's sysfs listing (`capture.txt:46-63` data profile `single`, `:68-88`
   metadata `dup`, `:89-108` system `dup`), not on S129.

4. [obs] SH4 is supported on the "no statistics exist" half: with no scrub running, `status` shows
   the statistics of the last finished or cancelled scrub (Quote C, `:136-137`) and that status "is
   read from the file located in :file:`/var/lib/btrfs`" (Quote D, `:137-138`). The capture supplies
   exactly the matching condition: `capture.txt:126-127` prints
   `ls: cannot access '/var/lib/btrfs': No such file or directory` with `[exit 2]`, and
   `capture.txt:119` prints `no stats available`.

5. [obs] SH4 is limited by the source on the monthly cadence and the timer: the string `month` does
   not occur in `S129.rst`. The sentence "The recommended period is a month" is in the file included
   by this one, not in the S129 bytes; the shipped unit's `OnCalendar=monthly` is at
   `capture.txt:137-141` and belongs to S131.

6. [obs] The document's structure matters for the entry: line 12 is `.. include:: ch-scrub-intro.rst`,
   so the prose "Scrub is a validation pass over all filesystem data and metadata" and the monthly
   recommendation are in a different file that is not part of the S129 snapshot bytes. The error
   taxonomy scrub reports (`csum`, `super`, `verify`, `read`) is inside S129 at lines 195–201, so
   "what scrub verifies" can be cited from S129 without the include. A fetched copy of the included
   file was kept for the record at
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/SrcBtrfsScrubDoc/ch-scrub-intro.rst.fetched`
   (sha256 `c3b9d344e11d842e2aed43d191b120572753bb75e8bbedd5b3e10978d24c3485`, 123 lines, same tag,
   byte-identical to the tag tree). It was deliberately not written into `.ufo/waves/round-26/sources/`,
   because that directory takes one file per pre-assigned source id and S129 is btrfs-scrub.rst. If
   the entry wants the "validation pass" wording, that file needs its own id (the next free id is
   S139), which is the L1's decision.

7. [inf] The declared SH4 conclusion "stored data has never been verified end to end" is an inference
   from two capture facts (no status file, timer disabled), not a claim this document makes. The
   document supplies the mechanism of scrub verification and the record of it; it does not assert
   anything about this host's history. The entry should mark that sentence as inference.

8. [obs] Nothing in the document contradicts the frozen capture. The capture's clean-status output
   (`capture.txt:119-125`: `no stats available`, `Total to scrub: 174.40GiB`, `Rate: 0.00B/s`,
   `Error summary: no errors found`) lacks the `Scrub started:` and `Status: running` lines that the
   document's own clean-status example carries (lines 165–180), which matches "no statistics for a
   last finished or cancelled scrub" rather than a completed scrub. The capture's allocation profiles
   are consistent with Quote A: a redundant metadata profile can be repaired from another copy, a
   non-redundant data profile cannot.

9. [obs] One trap worth carrying into the entry: the capture line `Error summary:    no errors found`
   (`capture.txt:125`) sits next to `no stats available` (`capture.txt:119`), and the document shows
   the same string attached to a scrub that actually ran (line 180). Read carelessly it looks like
   evidence that stored data was checked and is clean. Under this document it is not: the summary
   line belongs to the statistics of a last finished or cancelled scrub (`:136-137`), and this host
   has no such statistics. The SH4 verdict must read "never verified", not "verified and clean".

10. [unk] I could not confirm the GitHub REST tag object through the API:
    `https://api.github.com/repos/kdave/btrfs-progs/git/ref/tags/v7.1` returned HTTP 403 with
    "API rate limit exceeded". The tag is proven instead by `git ls-remote --tags` and by the
    byte-identical shallow fetch of `refs/tags/v7.1` (finding 1), which is stronger evidence than
    the REST answer would have been.

## 5. Method and boundaries

- Only public URLs were opened, by plain `curl`, plus `git ls-remote` and one shallow `git fetch` of
  the public tag into a scratch clone under `/fast/scratch/hyaku/tsuku26/SrcBtrfsScrubDoc/`, read-only
  against public upstream. The lane repository was written only at the two paths this seat owns: the
  S129 snapshot and this report. No `git` or `jj` write command was run against
  `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, and no message was sent to any seat.
- No host mutation: no scrub, no counter reset, no service action, no package transaction, no
  configuration write, no sudo command of any kind.
- Quote substring checks were run over the saved snapshot with a small Python script; Quotes A–D all
  reported `SUBSTRING` against `.ufo/waves/round-26/sources/S129.rst`, with word counts 16, 15, 19
  and 10.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md (round-26 declaration), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md (registry row shape), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-25-verifier-spotcheck.md (routed defects 1-8), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt (host facts), /home/vgpnk/.omp/agent/RULES.md, https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-scrub.rst, https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-scrub-intro.rst; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S129.rst, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/SrcBtrfsScrubDoc.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/SrcBtrfsScrubDoc/ch-scrub-intro.rst.fetched; executed=curl (three public fetches), git ls-remote --tags, git init plus one shallow fetch into a scratch clone under /fast/scratch/hyaku/tsuku26/SrcBtrfsScrubDoc/, sha256sum, wc, grep, python3 substring and word-count checks over the saved snapshot

Model: opencode-go/minimax-m3.1-flash-free

Installs: none
