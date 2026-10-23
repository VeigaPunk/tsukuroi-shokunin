# RevSourceS169 — re-open of source S169 (Trim.rst, btrfs-progs v7.1)

Verdict: **holds** — every checked cell of S169 verifies at f3a5723a988bf1c2835985880e7a38d477462cd0: fetch matches the anchor and the committed snapshot, the lesson Gate row's quote is verbatim at one line within 25 words, and the registry row's kind/tier/scope/teaches/status/opened/recheck/used-by are all true.

Evidence is bound to sandbox clone /fast/scratch/hyaku/tsukuroi-r31/RevSourceS169/repo checked out at f3a5723a988bf1c2835985880e7a38d477462cd0 (`git rev-parse HEAD` = f3a5723a988bf1c2835985880e7a38d477462cd0). Fetched bytes saved at /fast/scratch/hyaku/tsukuroi-r31/RevSourceS169/Trim.rst.fetch (2216 bytes).

## Findings

1. [obs] Fetch matches anchor and committed snapshot. `curl -sL https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/Trim.rst` → sha256 `2a114d56f29d727002a981e868cc97e89d7dd77a5e1cf42ad5a9ff05bfcf0ffc` (2216 bytes). The SOURCES.md row anchor (line 263) is the same hash, and the committed snapshot `.ufo/waves/round-31/w1/ScribeSrcTrim/Trim.rst` has the same hash and size (2216 bytes) — byte-for-byte equal to the live URL.

2. [obs] Source identity. `git ls-remote https://github.com/kdave/btrfs-progs.git refs/tags/v7.1 refs/tags/v7.1^{}` prints `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b	refs/tags/v7.1^{}`, matching the row's "peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b".

3. [obs] Lesson Gate row (corpus/lessons/round-31.md line 16): URL identical; Opened `2026-10-22` matches the lesson's stated fetch date (line 7: "Each was fetched by plain curl on 2026-10-22"). Located quote `the tool :command:\`fstrim\` starts a trim operation on the whole filesystem, no` is a verbatim substring of ONE line: `sed -n '29p' Trim.rst.fetch | grep -cF '<quote>'` = 1 (12 words ≤ 25).

4. [obs] File geometry matches the row: fetched file has 43 lines and 2216 bytes, equal to the row's "(43 lines, 2216 bytes)".

5. [obs] Registry row cells (SOURCES.md line 263 at f3a5723): kind=`docs`, tier=`A`, scope, teaches, status=`mined`, opened=`2026-10-22`, recheck=`on-release`, used-by=`corpus/knowledge/btrfs-repair-r31.json, corpus/knowledge/btrfs-repair-r31.md, SKILL.md, corpus/lessons/round-31.md`. The Gate decision column agrees (admit, mined, tier A; lesson line 22: S164–S169 "absent → mined (recheck on-release)").

6. [obs] teaches is fully contained in the anchor line range 14–43 and keeps every source branch (QUALITY 66, line 133). Each teaches sentence maps to source lines: synchronous (14–18: `-o discard`/`discard=sync`, "right after the file extents get freed", "severe performance hit", "not recommended", "too fragmented"); asynchronous (20–26: `discard=async`, improved version, tracked in memory, "after a period or enough ranges accumulate", "much larger", throttle IO requests, "does not interfere with the rest of the filesystem activity"); manual fstrim (29–32: whole filesystem, "no mount options need to be specified", traverse free space, "periodic service"); hint (34–36: three branches all kept — "ignore it completely", "start it only on ranges meeting some criteria", "decide not to do it because of other factors affecting the memory cells" — teaches renders all three); relocation (36–38: "unexpected performance drop", "prevent that too"); mkfs/kernel defaults (40–43: "by default performed on all devices", kernel 6.2, `discard=async` "automatically enabled on devices that support that"). Phrase presence inside lines 14–43 confirmed by sed range + grep -cF (discard=sync=1, fstrim=2, periodic=2, hint=1, mkfs.btrfs=1, 6.2=1, async=3; not recommended/severely/fragmented/throttling/interfered/criteria/memory cells/unexpected performance drops/prevent/performed by default on all devices/automatically enabled all present). No "otherwise"/"exactly" overclaim; the only "only" use is sourced ("start it only on ranges meeting some criteria").

7. [obs] used-by: all four named files exist at f3a5723 and cite S169 (`grep -cF 'S169'`: btrfs-repair-r31.json=1, btrfs-repair-r31.md=3, SKILL.md=1, round-31.md=3).

8. [inf] No failing cell found. Residual risk is limited to the located quote being truncated mid-sentence at "no" (line 29 continues ", no mount options need to be specified"), but it is still a verbatim substring of one line within the word cap, so it satisfies the Gate row contract; the full sentence is covered by the teaches cell and anchor range.

Scope: read=corpus/SOURCES.md:263 (sandbox @ f3a5723), corpus/lessons/round-31.md:5-23, corpus/QUALITY.md (rules 26-39, 65-67), Trim.rst.fetch (full), git ls-remote tag peel, git rev-parse; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevSourceS169.md, /fast/scratch/hyaku/tsukuroi-r31/RevSourceS169/Trim.rst.fetch; executed=curl, sha256sum, wc, sed/grep -cF checks, git ls-remote, git rev-parse
Model: not exposed
Installs: none
