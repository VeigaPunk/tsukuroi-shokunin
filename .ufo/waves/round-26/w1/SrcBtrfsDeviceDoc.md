# S128 — btrfs-progs v7.1 `btrfs device stats` documentation (round 26, wave 1)

Verdict: done — the pinned upstream doc opens at the installed release tag, grounds the counter set and the sysfs mirror for SH1, partially grounds SH2 (persistence and explicit reset only), and contradicts nothing in the frozen capture.

## Findings

1. [obs] The tag `v7.1` exists and the file did **not** move at that tag: `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-device.rst` returned HTTP 200 with 11664 bytes; the same path under a deliberately wrong tag `v7.1-nope` returned HTTP 404, so the 200 is tag-specific and not a redirect artifact. Evidence: `curl -sS -o /dev/null -w '%{http_code}'` on both URLs, exit 0.

2. [obs] Tag identity is anchored by `git ls-remote --tags https://github.com/kdave/btrfs-progs` (exit 0): `refs/tags/v7.1` → `0a919c7d6e389c07920675b7fad3f793b92aa78b` (annotated tag object), peeled `refs/tags/v7.1^{}` → commit `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`. Fetching the file at that peeled commit returned HTTP 200 with 11664 bytes and `cmp` against the saved snapshot exited 0 (`TAG-CONTENT == COMMIT-CONTENT`). Evidence: command output above; the peeled commit is the anchor in the proposed row.

3. [unk] `https://api.github.com/repos/kdave/btrfs-progs/git/ref/tags/v7.1` returned HTTP 403 (280-byte body) from this host, so tag identity rests on `git ls-remote` and the byte-identical commit fetch, not on the REST API. Evidence: `curl -sS -o /tmp/s128_tag.json -w '%{http_code}\n'` → `403`, `wc -c` → 280.

4. [obs] Snapshot saved at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S128.rst`; sha256 `0d4f425a49c1483f1cc598695d9a456e6d5542e5c59df4946fd471e5d4f7a0e6`; 284 lines; 11664 bytes; ends with a newline (`tail -c 1` → `0x0a`). Evidence: `sha256sum` and `wc -l -c` on the saved file, exit 0.

5. [obs] The pin matches the host install: capture line 12 reads `btrfs-progs 7.1-1`. Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt:12`.

6. [obs] **SH1 is supported.** The DEVICE STATS section defines exactly five counters, `write_io_errs`, `read_io_errs`, `flush_io_errs`, `corruption_errs`, `generation_errs` (snapshot lines 244, 247, 249, 254, 256), each with a meaning (lines 245-257), including "A block checksum mismatched or a corrupted metadata header was found." (line 255) and "The block generation does not match the expected value (e.g. stored in the parent node)." (lines 257-258). Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S128.rst:244-258`.

7. [obs] **SH1's sysfs clause is supported with a limit.** The doc states that the device stats — the same statistics the `btrfs device stats` query prints — "are also available in textual form" in `/sys/fs/btrfs/FSID/devinfo/DEVID/error_stats` since kernel 5.14 (snapshot lines 260-261). It does not enumerate the sysfs field names, so field-by-field identity of the two renderings is not established by this source: the doc's example uses `write_io_errs` while the host's sysfs file uses `write_errs` (`capture.txt:40-44`). [inf] The mapping of the five sysfs names to the five ioctl names is consistent with "the same statistics in textual form" but must be cited from the kernel side (S132/S133) or from the capture, not from this file alone. Evidence: snapshot lines 260-261 against `capture.txt:40-44` and `capture.txt:112-116`.

8. [obs] The doc also gives the mounted-versus-offline split: in mounted mode "the stats are read using an ioctl and can be reset or checked" (snapshot lines 132-133), and `--reset` "does not work" in offline mode (lines 137-138, and again 146-147). [inf] The host capture queried the mounted path with the ioctl, so it is inside the documented mode. Evidence: snapshot lines 132-138, 146-147; `capture.txt:110-116`.

9. [obs] **SH2's first half is supported.** "The device stats keep persistent record of several error classes related to doing IO." (snapshot lines 231-232) plus "The current values are printed at mount time and updated during filesystem lifetime or from a scrub run." (lines 232-233) is the doc's own statement that the record outlives a mount cycle and is re-reported at mount time. Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S128.rst:231-233`.

10. [obs] **SH2's reset semantics are supported.** `-z|--reset`: "Print the stats and reset the values to zero afterwards. Does not work in offline mode." (snapshot lines 145-147) is the only zeroing path the doc describes; the `-c|--check` path only reports — "If the *-c* option is used, *btrfs device stats* will add 64 to the exit status if any of the error counters is non-zero." (lines 269-270), with exit 65 when a device could not be read (lines 149-152). Evidence: snapshot lines 145-152, 269-270.

11. [inf] **Wording limit on SH2.** The doc never uses the phrase "persist across mounts" and never states that unmounting leaves the values intact; cross-mount persistence is inferred from "keep persistent record" plus "printed at mount time". The declared row should be worded as the doc supports it (a persistent record re-reported at mount time, cleared only by an explicit `-z/--reset`), not as a verbatim guarantee. Evidence: snapshot lines 231-233 contain no such sentence; the whole file has no "unmount" mention of the counters.

12. [obs] **SH2's second half is not grounded by this source.** The document says nothing about kernel log lines or dated incidents; "a dated incident comes from the kernel's per-error log line" has no basis in this file and must be sourced from the kernel sources (S132/S133) or dropped from SH2's citation of S128. Evidence: a case-insensitive `grep -n "log"` over the snapshot returns exactly one hit, line 248 "Read request analogy to write_io_errs.", which is a substring artefact and not error logging; the document contains no log-line, journal or dated-incident text.

13. [obs] **A wording limit for the entry as a whole.** The doc says the counters are "updated during filesystem lifetime **or from a scrub run**" (snapshot line 233). A scrub run can therefore move a counter, so any wording that the counters change only on I/O failure would be wrong. Evidence: snapshot line 233.

14. [obs] **No contradiction with the frozen capture.** Capture line 39 uses the sysfs path `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/error_stats`, matching the doc's template `FSID/devinfo/DEVID/error_stats` (snapshot line 261) with the host's FSID and device id substituted. Capture lines 40-44 show the five sysfs fields `write_errs`, `read_errs`, `flush_errs`, `corruption_errs`, `generation_errs`, all `0`; capture lines 112-116 show the ioctl rendering `[/dev/mapper/root].write_io_errs`, `read_io_errs`, `flush_io_errs`, `corruption_errs`, `generation_errs`, all `0`, using the doc's own field names (snapshot lines 237-242). Evidence: `capture.txt:39-44`, `capture.txt:110-116` against `S128.rst:237-242,261`.

15. [obs] Capture line 121 (`btrfs scrub status /` → "no stats available") is consistent with the doc, since a scrub run updates the counters (snapshot line 233) and no scrub has ever run on this host, so no scrub-derived counter movement is expected. Evidence: `capture.txt:118-124`.

16. [inf] The doc's example device is `/dev/sda3` while the host device is `/dev/mapper/root` (a LUKS mapping); the doc covers "a single *device* or *file*" generally (snapshot lines 128-131), so this is an example substitution, not a divergence. Evidence: snapshot lines 128-131, 237; `capture.txt:110-116`.

17. [unk] The host kernel is 7.2.11 (`capture.txt:9`), so the doc's "Since kernel 5.14" condition for the sysfs textual form is satisfied by version, but this source cannot by itself certify that the host's kernel implements it; the host's own sysfs file does exist (`capture.txt:39-44`). Evidence: `capture.txt:9`.

## Proposed SOURCES row (11-column contract shape)

| S128 | btrfs-device(8) — https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-device.rst | docs | A | The `btrfs device stats` subcommand of btrfs-progs v7.1: what the five per-device IO error counters count, how their values persist and are cleared, and the sysfs `error_stats` mirror; upstream documentation only, not host state | tag v7.1, peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b, Documentation/btrfs-device.rst, lines 127-152 and 226-270; raw bytes sha256 0d4f425a49c1483f1cc598695d9a456e6d5542e5c59df4946fd471e5d4f7a0e6 | The device stats are five per-device IO error counters kept as a persistent record over the filesystem lifetime, printed at mount time and since kernel 5.14 also exposed as text in the sysfs `error_stats` file; only the explicit `-z/--reset` zeroes them, so a non-zero value carries no date of its own | mined | 2026-10-22 | on-release | corpus/knowledge/storage-health-r26.md |

No `|` appears inside any cell of the row above.

## Exact quotes from the saved snapshot

Each quote is copied from `.ufo/waves/round-26/sources/S128.rst` and is at most 25 words. Where the source sentence wraps, the quoted text is the whitespace-normalised join of the cited lines; the source lines carry 8-space indentation for list and block content. Each of these nine strings was checked programmatically to be a whitespace-normalised substring of the saved snapshot.

1. SH2 (persistence) — snapshot lines 232-233: "The current values are printed at mount time and updated during filesystem lifetime or from a scrub run."
2. SH2 (explicit reset) — snapshot lines 146-147: "Print the stats and reset the values to zero afterwards. Does not work in offline mode."
3. SH1 (the five counters) — snapshot lines 238-242: "[/dev/sda3].write_io_errs 0 [/dev/sda3].read_io_errs 0 [/dev/sda3].flush_io_errs 0 [/dev/sda3].corruption_errs 0 [/dev/sda3].generation_errs 0"
4. SH1 (sysfs mirror of the same counters) — snapshot lines 260-261: "Since kernel 5.14 the device stats are also available in textual form in :file:`/sys/fs/btrfs/FSID/devinfo/DEVID/error_stats`."

Decisive lines quoted separately for the support and limit analysis above:

- snapshot line 231: "The device stats keep persistent record of several error classes related to"
- snapshot lines 132-133: "the stats are read using an ioctl and can be reset or checked."
- snapshot lines 269-270: "If the *-c* option is used, *btrfs device stats* will add 64 to the exit status if any of the error counters is non-zero."

## Gates and touched surfaces

- [obs] The C1 acceptance rule requires every cited source to be a `corpus/SOURCES.md` row with status `mined`, opened `2026-10-22` and `used-by` naming `corpus/knowledge/storage-health-r26.md`; the proposed row satisfies that shape. The integrator writes the row into `corpus/SOURCES.md`, where the registry currently ends at S127 (`corpus/SOURCES.md:133`), so S128 is the next free id.
- [obs] The anchor cell carries the tag, the path, the line ranges and the sha256 of the committed snapshot, as the declaration requires.
- [obs] Any lesson `## Gate` table entry for S128 must reproduce one of quotes 1-4 byte-for-byte; the same quote text must also appear in the corpus entry row that cites S128.
- [obs] Out of scope and untouched: `corpus/SOURCES.md`, `corpus/knowledge/storage-health-r26.md`, `corpus/knowledge/storage-health-r26.json`, `SKILL.md`, `SCORECARD.md`, `SHONEN.md`, `tools/check-storage-health.py` — all are the integrator's surfaces.
- [obs] No package, service, configuration, counter, scrub, mount, image or VCS write action was performed; no lane file outside the two seat paths was written.

Scope: read=SCORECARD.md round-26 declaration, round-25 verifier spot-check routed defects, corpus/SOURCES.md registry rows, frozen capture.txt, btrfs-progs v7.1 Documentation/btrfs-device.rst; wrote=.ufo/waves/round-26/sources/S128.rst, .ufo/waves/round-26/w1/SrcBtrfsDeviceDoc.md; executed=plain curl fetches of the raw file at tag v7.1, at a wrong tag and at peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b, curl of the GitHub tags REST ref, git ls-remote --tags on github.com/kdave/btrfs-progs, cmp, sha256sum, wc, grep, tail
Model: MiniMax-M3.1-Flash
Installs: none
