# Wave 2 — RevSourceS167 (falsify): source S167 re-open

Verdict: S167 holds — every checked cell (URL fetch vs anchor hash, snapshot identity vs fetch, lesson Gate row, registry cells including QUALITY-66 branch retention, status/opened/recheck/used-by) verifies at f3a5723a988bf1c2835985880e7a38d477462cd0.

## Findings

1. Fetch matches the anchor hash [obs]. Command: `curl -sL --fail -o fetched-ch-mount-options.rst https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-mount-options.rst`; exit 0. Output: `aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f fetched-ch-mount-options.rst`, 557 lines, 26871 bytes. This equals the SOURCES.md:261 anchor `sha256 aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f`.

2. Committed snapshot is identical to the fetch, and the tag/peel claim holds [obs]. `sha256sum repo/.ufo/waves/round-31/w1/ScribeSrcMountOpts/ch-mount-options.rst` → same digest; `cmp -s` → `IDENTICAL_TO_SNAPSHOT`; `git ls-files` shows the snapshot path tracked at f3a5723 (count 1). Independent provenance: `git ls-remote` on kernel.org → `0a919c7d6e389c07920675b7fad3f793b92aa78b refs/tags/v7.1`; shallow clone of that tag checked out detached HEAD `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b` and `Documentation/ch-mount-options.rst` at it has the same sha256, 557 lines, 26871 bytes — confirming the anchor's peeled-commit claim.

3. Lesson Gate row holds [obs] (corpus/lessons/round-31.md:14): URL identical to the SOURCES row; Opened `2026-10-22` (= today); quote `"May not be well suited for large database workloads."` found verbatim at the stated location: `sed -n '39p' <snapshot> | grep -cF 'May not be well suited for large database workloads.'` → `1`, a single line (snapshot line 39), 9 words ≤ 25; Location sha256 matches the anchor.

4. Registry row cells hold [obs] (corpus/SOURCES.md:261): kind=`docs` (upstream .rst documentation), tier=`A` (v7.1 primary upstream documentation; lesson decision column agrees), scope matches content (mount-option documentation, explicitly "not host-specific behavior"), and the teaches cell is fully contained by the anchor line ranges: autodefrag clauses within 33-51, commit= clauses within 89-101, nodatacow/nodatasum clauses within 131-159 (verified against snapshot lines 33-51, 89-101, 131-159).

5. QUALITY 66 (corpus/QUALITY.md:133) branch retention holds [obs]. Every branch the source states is kept in teaches: the reflink warning retains all five kernel-version disjuncts (snapshot lines 46-48 `< 3.9 or ≥ 3.14-rc2` and stable `≥ 3.10.31, ≥ 3.12.12 or ≥ 3.13.4`; teaches lists all five); commit= keeps both "upper bound is not forced" and "warning ... more than 300 seconds" (lines 95-96); nodatacow keeps both the performance benefit and the partial-write cost (lines 141-143); nodatasum keeps no-checksums, slight gain, and hardware support (lines 149-159). No stated branch is dropped.

6. status/opened/recheck/used-by hold [obs] at f3a5723: status=`mined` (consistent with lessons/round-31.md:22: S164-S169 absent → mined); opened=`2026-10-22`; recheck=`on-release` (appropriate for a version-pinned upstream doc). used-by: all four files exist at f3a5723 and cite S167 — `corpus/knowledge/btrfs-repair-r31.json` (3 hits: lines 34, 43, 52), `corpus/knowledge/btrfs-repair-r31.md` (3 hits: rows Q04-Q06), `SKILL.md` (3 hits: R31-Q04/Q05/Q06 citing "S167 lines 33-43 / 89-96 / 131-159"), `corpus/lessons/round-31.md` (1 hit: Gate row). Verified via `git grep -n -c S167` per file (counts 3/3/3/1).

7. Minor cosmetic divergence, not a defect [obs]: the teaches cell writes "64 KiB" while the source (line 38) writes "64KiB". Same fact and value; this exact spelling is already disclosed as the R31-KEY-SPELLING incident for Q04 (lessons/round-31.md:37,56). It does not drop a branch or overstate.

## Residual risk and verification gaps

- The raw fetch was performed 2026-10-22; tag objects are immutable upstream, so the pinned bytes are stable absent history rewrites.
- The counter's sealed answer keys are not re-derived here (out of scope for this source row review); row truth for Q04-Q06 rests on the wave-2 per-row reviews, and the snapshot bytes this row pins are verified identical to upstream.
- No [unk] cells encountered.

Scope: read=corpus/SOURCES.md:261, corpus/lessons/round-31.md:14,22,37-38,56, corpus/QUALITY.md:133, SKILL.md:2682-2687, snapshot lines 33-51/89-101/131-159 (absolute: /fast/scratch/hyaku/tsukuroi-r31/RevSourceS167/repo/.ufo/waves/round-31/w1/ScribeSrcMountOpts/ch-mount-options.rst); wrote=.ufo/waves/round-31/w2/RevSourceS167.md, .ufo/waves/round-31/w2/RevSourceS167/fetched-ch-mount-options.rst (sha256 aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f, 557 lines, 26871 bytes, unchanged from the URL); executed=curl -sL --fail, sha256sum, wc, cmp, sed -n '39p' | grep -cF, git ls-files, git grep -n -c, git ls-remote https://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git refs/tags/v7.1, git clone --depth 1 --branch v7.1 (kernel.org), git rev-parse HEAD
Model: inception/mercury-3
Installs: none
