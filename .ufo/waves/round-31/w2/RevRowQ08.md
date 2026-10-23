# C1 row Q08 review (wave 2, seat RevRowQ08)

Verdict: **holds** — Q08 is a genuinely sourced, novel, decision-shaped row at f3a5723a; every clause is supported by the pinned btrfs-progs v7.1 Trim.rst bytes, the quote is verbatim at line 29, and the held neighbour (storage-health-r26.md:11) is a host-capture fact, not the trim-mode choice the row states.

## Evidence

- Row: `corpus/knowledge/btrfs-repair-r31.json:66-74` (id Q08; source S169; snapshot `.ufo/waves/round-31/w1/ScribeSrcTrim/Trim.rst`; line 29; quote `the tool :command:`fstrim` starts a trim operation on the whole filesystem, no`).
- SKILL decision line: `SKILL.md:2687` (`| [R31-Q08] | Choosing a trim mode on a btrfs SSD | ... | S169 line 14-32 |`).
- Decision-table row: `corpus/knowledge/btrfs-repair-r31.md:19` (Q08 row; notes "[inf] The cited text does not state a universal winner between async discard and periodic fstrim"), plus Not-covered row at `:37`.
- SOURCES row: `corpus/SOURCES.md:263` (S169, status `mined`, contains frozen URL and frozen sha256 `2a114d56...ffc`, "upstream documentation, not host-state evidence").
- Snapshot pin: `tools/check-btrfs-repair-r31.py:76-82` (Q08 → Trim.rst, pin `2a114d56f29d727002a981e868cc97e89d7dd77a5e1cf42ad5a9ff05bfcf0ffc`, token `fstrim`).
- Snapshot bytes: fetched `curl -sL https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/Trim.rst` → sha256 `2a114d56f29d727002a981e868cc97e89d7dd77a5e1cf42ad5a9ff05bfcf0ffc`, byte-identical to the snapshot at REV (`cmp` IDENTICAL; saved at `.ufo/waves/round-31/w2/RevRowQ08/Trim.rst`, 2216 bytes).

## Findings

1. [obs] Quote verbatim at the cited line. `sed -n '29p' Trim.rst | grep -cF 'the tool :command:`fstrim` starts a trim operation on the whole filesystem, no'` → `1`; the quote (12 words) is a substring of line 29 (`Trim.rst:29`). R4 satisfied (line 29, 6–25 words, substring).

2. [obs] Clause-by-clause support (source `Trim.rst:12-43`; all clauses map to cited lines):
   - "Do not recommend discard=sync: it trims freed extents immediately" → `:15-16` ("the trim is done right after the file extents get freed", "is not recommended").
   - "fragmented ranges may cause a severe performance hit" → `:17-18` ("could have severe performance hit ... could be too fragmented"); softened "may" is safe (QUALITY 66: no "only"/"always" the source lacks).
   - "discard=async ... improved version of synchronous trim; tracks freed extents in memory, then starts after a period or when enough ranges accumulate, expecting larger ranges and throttling the number of I/O requests so other filesystem activity is not disrupted" → `:21-26` (verbatim structure: "improved version of the synchronous trim", "tracked in memory", "after a period or enough ranges accumulate", "expecting the ranges to be much larger", "throttle the number of IO requests which does not interfere with the rest of the filesystem activity").
   - "Manual fstrim needs no mount options, traverses free space across the filesystem, and suits a periodic service" → `:29-32` ("no mount options need to be specified", "traverse the free space", "suitable for running it as periodic service").
   - "periodic trimming may also prevent unexpected slowdown from device-internal data relocation" → `:37-38` ("The device itself could internally relocate the data ... unexpected performance drop. Running trim periodically could prevent that too").
   - "Since kernel 6.2, the discard=async mount option is automatically enabled for devices that support it" → `:41-43` (verbatim sense).
   - "Trim is a device hint: it may be ignored, applied only to ranges meeting criteria, or skipped for other factors affecting memory cells" → `:34-36` (verbatim sense).
   - SKILL line's three clauses (avoid discard=sync / fstrim no mount option, periodic service / discard=async tracks freed ranges and throttles I/O) all supported by `:14-32`.
   - No lost branch: all three modes (synchronous, asynchronous, manual fstrim) are covered; the absence of a single universal winner is marked `[inf]` in the decision table and Not-covered, not asserted.

3. [obs] The row answers every part of the frozen question ("Which trim mode should a btrfs SSD use: discard=sync, discard=async or periodic fstrim?"): it rejects discard=sync, describes the two viable options, notes the automatic kernel-6.2 default, and honestly flags that the source does not pick a universal winner.

4. [obs] Novelty (frozen token `fstrim`): `git grep -i -F -c -e fstrim 2077e2fa -- SKILL.md PROVINCE.md corpus` → exit 1, no hits. Synonym sweep at base: `trim` hits only `SKILL.md:1222` (meta-text "not trimmed by dropping a probe") and round-29 lesson rows about SOURCES trim; `discard` hits `storage-health-r26.md:11` (host fact), `boot-chain-r17.json:299` ("allow-discards" cmdline note), and lesson/log prose ("pass was discarded", "Discarded premises"). None states the trim-mode choice.

5. [obs] Held neighbour judged: `storage-health-r26.md:11` records a host capture ("mount options include `discard=async`"). The Q08 row states a trim-mode **choice** (recommendation across the three modes, grounded in upstream docs — S169's own description says "upstream documentation, not host-state evidence"). The row does not state the host mode, and the held neighbour does not answer the question; the overlap is phrase-level ("discard=async" appears in both), which the wave-1 erratum already flagged as "partly held as a host fact". Distinct claims, so the row's claim stands.

6. [obs] Frozen counter at REV confirms every rule: `python3 tools/check-btrfs-repair-r31.py --revision f3a5723a... --lane <sandbox>` → `{"id": "Q08", "new_sourced": true, "fail": []}`; summary `new_sourced 8 of 8`, exit 0 (counter_sha256 `4f69a109...` matches the declared sha256). R3 (snapshot pin), R4 (line/quote), R5 (S169 mined at REV, absent at base, URL+pin present), R6 (token in quote/statement/SKILL line; exactly one `| [R31-Q08] ` line), R7 (key groups, no 6-word run with quote), R8 (0 base hits) all pass.

## Residual risk / verification gaps

- [unk] The sealed answer keys were not recovered (per instruction); R7 is verified only by the counter's digest check, not by inspecting plaintext keys.
- [obs] The statement's "slowdown" for the source's "unexpected performance drop" is a paraphrase, not a quote; meaning-preserving and flagged as supported above.
- [obs] The host fact (root mounts with discard=async) is not asserted by the row; no conflict with the round-26 note.

Scope: read=corpus/knowledge/btrfs-repair-r31.json, SKILL.md, corpus/knowledge/btrfs-repair-r31.md, corpus/SOURCES.md, tools/check-btrfs-repair-r31.py, corpus/knowledge/storage-health-r26.md, SCORECARD.md (round-31 declaration + errata), fetched Trim.rst bytes; wrote=.ufo/waves/round-31/w2/RevRowQ08.md, .ufo/waves/round-31/w2/RevRowQ08/Trim.rst; executed=git checkouts (sandbox), git grep/show (read-only), curl -sL raw.githubusercontent.com Trim.rst, sha256sum, cmp, sed -n '29p' | grep -cF, python3 tools/check-btrfs-repair-r31.py --revision f3a5723a... --lane <sandbox>
Model: inception/mercury-3
Installs: none
