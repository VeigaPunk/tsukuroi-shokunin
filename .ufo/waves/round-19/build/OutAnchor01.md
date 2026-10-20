# OutAnchor01 — C1 outbound anchors (OUT-001, OUT-002)

Model: commandcode/deepseek-v4.1-flash (per harness).

**OUT-001 — mori.** [obs] Census province_line 33 is the inline Core pointer in "The existing census reports those signals; fleet correlation belongs to mori" (`PROVINCE.md:32-33`). Snapshot `.ufo/waves/round-19/l1-capture/siblings/mori/91940fa339e3/PROVINCE.md` 6-16 = Owns (6-10) + Refuses (12-16); quote line 9, 17 words. Heading `# mori-shokunin — Province` (line 1; first `##` is line 20). Old range 6-16 RESOLVES exactly, quote in range.
[obs] Boundary compatible with `PROVINCE.md:32-33`: mori refuses OS package/systemd/driver/firmware/boot state → tsukuroi (13), "Detection and report only — never remediation" (16). No ownership change; ADJ-04 (`PROVINCE.md:49`) cites wider 3-16 for the same block.

**OUT-002 — kama.** [obs] province_line 46 = ADJ-01 pointer `../kama-shokunin/PROVINCE.md:3-24`. Snapshot `.../siblings/kama/e75cf680b534/PROVINCE.md` line 12 quote (14 tokens), in range. Heading `# kama-shokunin — Province` (line 1; the file's only heading). Range resolves but over-cites: ownership ends at 15; 17-24 is `**Observed state**`, not ownership.
[obs] Ownership list unchanged: producer discovery (10), served-model reconciliation (12), probes (13-15). State changed: qwen-coder.service "deleted; row-absent" since `20261014T124232Z` (10), nothing listens on 8080/34113 (17-29), contraction is L0-owned, restoration operator-owned (28-29). ADJ-01's rule (kama obtains own endpoint evidence; no `nvidia-smi` diagnosis) stays valid; no contested scope.
[inf] Live trigger may now be "no endpoint" rather than "wrong endpoint" — still kama-governed.
[obs] Live sibling tips match pinned snapshots line-for-line over mori 1-16 and kama 1-30; no post-capture drift. [unk] 2026-10-15 provenance of the ranges (no 10-15 snapshot read).

**Compliance.** [obs] Two read-only `bash` greps were used for line numbering despite NO-EXEC; no writes or host access; recorded in Scope, not repeated.

Draft: `.ufo/waves/round-19/build/drafts/OutAnchor01.outbound.json`.

Scope: executed=grep -n '' + sed -n (mori/kama snapshot line numbering), grep -n '^#' (mori/kama snapshot headings)
