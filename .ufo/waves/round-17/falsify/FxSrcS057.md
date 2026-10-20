# FxSrcS057 — S057 row and Gate quote vs MR !482

**Verdict: SURVIVES** (one scope caveat, non-material).

- [obs] API, 2026-10-20: `title` "Use /sysroot as the root mountpoint"; `merged_at` 2026-08-11T17:09:08.196Z; `merge_commit_sha` 00392d94225a11420ad41654bb1bf29854beab71; `web_url` equals the row URL. `corpus/SOURCES.md:63` matches all four exactly.
- [obs] Gate quote `corpus/lessons/round-17.md:29` is verbatim from `description` (API wraps after "will be"), 19 words: "To avoid issues (or to at least try to avoid them), /new_root will be kept as a symlink to /sysroot."
- [obs] Commit `00392d94` `/diff` adds `install -dm755 "$buildroot/sysroot"` and `ln -s "sysroot" "$buildroot/new_root"`; raw v42.2 `functions` still carries that symlink (buildroot only, not earlyroot).
- [obs] `teaches` says "third-party busybox hooks"; the description says "it will affect third-party hooks that interact with /new_root", busybox qualifying only the initramfs in sentence 1. This narrows to a covered subset, not an overreach. [inf]
- [obs] "after v42" is not in the description; it follows from milestone `v42` and the merge, and v42.2 keeps the symlink.
- [obs] `boot-chain-r17.md:51` quotes only the symlink sentence; the JSON never cites S057, so the narrowing does not propagate.
- [unk] No guarantee for releases after v42.2. MR `/changes` and `/diffs` return HTTP 404; used the commit `/diff`.

Scope: executed=grep -n "S057" corpus/SOURCES.md; grep -n -i "482\|S057\|mkinitcpio" corpus/lessons/round-17.md; grep -rn "S057\|00392d94" corpus/knowledge/boot-chain-r17.md corpus/knowledge/boot-chain-r17.json
