# RevSourceS170 — review of rejected source S170 (btrfs.readthedocs.io "latest" Trim.html / Defragmentation.html)

Verdict: agrees with the reject — holds. S170 (unpinned `latest` Trim/discard and Defragmentation pages) is correctly rejected as redundant with the pinned btrfs-progs v7.1 files and unpinned; the stated flip condition is not triggered by the current latest pages; the Gate quote is real and single-located.

## Findings

1. [obs] Fresh live fetch (2026-10-22, this review) is byte-identical to the wave-1 saved snapshots: `curl -sL` → HTTP 200, `CURL_EXIT=0` for both pages; `sha256sum` of `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevSourceS170/Trim-live.html` = `07d83d2e5af70e4f270a8784f588406a72c36c224f1479946089c74ab941d2e1` = saved `Trim.html`, and `Defragmentation-live.html` = `3d329b36e46b8836237ffe42b04df3fa9cebc7d825f350d48d0e84c73cdcffbe` = saved `Defragmentation.html`; `cmp` exit 0 for both pairs. The snapshots the row cites are faithful, current captures; the latest alias has not drifted since wave 1.

2. [obs] Unpinned: both saved pages carry `readthedocs-version-slug` content="latest" on line 28 (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/ScribeSrcRejectRtd/Trim.html:28` and `Defragmentation.html:28`). No release tag, version number, or source revision appears in the captured bytes; the only "Devel" hits are the nav-sidebar word "Developer"/"Developer's FAQ" (Trim.html lines 95-101), i.e. page chrome, not version identification. The pages cannot name their own version ([unk], as in wave 1: the HTML discloses no generating commit).

3. [obs] Redundancy with pinned v7.1 verified mechanically: a normalized-token coverage check of the rendered article body against the saved v7.1 files (`Trim-v7.1.rst` 43 lines, `Defragmentation-v7.1.rst` 31 lines) finds every substantive rst token in the rendered body — Trim 354/354 content tokens present (0 missing); Defragmentation 288/288 present (3 tokens "man/cmd/defragment" are the `:ref:`btrfs filesystem defrag<man-filesystem-cmd-defragment>`` target-name artifact of my own normalization, not absent content; the HTML renders the link text "btrfs filesystem defrag"). Manual paragraph mapping confirms the bodies at Trim.html lines 141-179 and Defragmentation.html lines 141-170 reproduce the rst content one-for-one; differences are only HTML markup/link expansion and typographic apostrophes (`there's` → `there’s` at Trim.html:145, Defragmentation.html:145). Neither rendered body adds an operation-specific sentence beyond the v7.1 files — nothing the pages add qualifies as materially new guidance.

4. [obs] The pinned comparison base is genuine: independent re-fetch from `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/Trim.rst` and `.../Defragmentation.rst` (HTTP 200, exit 0) returns sha256 `2a114d56f29d727002a981e868cc97e89d7dd77a5e1cf42ad5a9ff05bfcf0ffc` and `71ad07a3f200284b01d6ee18fc4cc8732fe0542b80556e2cc798247505daa60b` — byte-identical to the saved snapshots cited in the row.

5. [obs] The Gate quote is exact and unique: `sed -n '147p' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/ScribeSrcRejectRtd/Trim.html | grep -cF 'The trim operation issued by user provides hints about what data are'` → `1` (12 words, line 147, inside the body paragraph at lines 143-149). Matches S170-gate.md's quote/location/hash.

6. [obs] The flip condition in the row is well-formed and currently untriggered: "an explicitly release-pinned page adds materially new, operation-specific guidance absent from the pinned v7.1 files, and the release page is saved and anchored by its version and full-byte sha256". The current latest pages add no guidance beyond v7.1 (finding 3), so neither arm of the flip is met; the 180d recheck is an appropriate cadence for a `latest` alias.

7. [obs] Row integrity: the hashes, lines, opened date (2026-10-22), status `rejected`, and recheck `180d` in the S170 row all match the files on disk; the row's stated reject reason (unpinned `latest`, redundant with v7.1) is exactly what findings 2-4 reproduce.

## Residual risk and verification gaps

- [unk] The exact upstream commit behind the `latest` build is not disclosed by the pages; the redundancy verdict rests on rendered-byte equality with v7.1 text, not on knowing the doc-source commit. This was the wave-1 unknown too and does not affect the current rejection.
- [inf] The `latest` content can change after this review; that is governed by the recheck cadence and the flip condition, not by this verdict.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:1196-1224 (declaration + errata), S170-row.md, S170-gate.md, ScribeSrcRejectRtd.md, Trim.html/Defragmentation.html/Trim-v7.1.rst/Defragmentation-v7.1.rst (wave-1 saved snapshots); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevSourceS170/Trim-live.html,/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevSourceS170/Defragmentation-live.html,/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevSourceS170.md,/fast/scratch/hyaku/tsukuroi-r31/RevSourceS170/Trim-v7.1-refetch.rst,/fast/scratch/hyaku/tsukuroi-r31/RevSourceS170/Defragmentation-v7.1-refetch.rst; executed=curl (4 fetches), sha256sum, wc -c, cmp, grep, sed|grep -cF, python3 token-coverage analysis
Model: not exposed
Installs: none
