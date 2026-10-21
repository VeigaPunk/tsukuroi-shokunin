## Attack

Axis: adjacency publication fidelity. Falsify OUT-001 by checking its snapshot and pointer against the pinned sibling object and the landed target revision, then determine whether the appended PROVINCE section actually republishes the complete pin (commit and SHA-256) and what the gate enforces.

## Method

Read-only checks against target `8e5916360f2dfe7bc4eb4ba144081af555900116`:

```sh
python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116
sha256sum .ufo/waves/round-19/l1-capture/siblings/mori/91940fa339e3/PROVINCE.md
git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -p 91940fa339e38006f8db5bd7d78bb6f037f4d016:PROVINCE.md | sha256sum
git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e '91940fa339e38006f8db5bd7d78bb6f037f4d016^{commit}'
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse master origin/master HEAD
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline master..91940fa339e38006f8db5bd7d78bb6f037f4d016
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline 91940fa339e38006f8db5bd7d78bb6f037f4d016..master | wc -l
```

Also inspected committed target blobs with read-only `git show`/Python line and JSON checks; compared sibling `PROVINCE.md` lines 6–16 at the pin and `master`; and confirmed the gate source is identical to its target-revision blob with `git diff --exit-code 8e5916360f2dfe7bc4eb4ba144081af555900116 -- tools/check-adjacency-anchors.py`.

## Verdict

**REFUTE — C1 adjacency, specifically OUT-001's claimed full republication.** Snapshot, quote, pointer, and pin checks pass, but the appended PROVINCE row publishes only the 12-character commit prefix and omits the SHA-256 value. The full commit and digest exist in the JSON registry, not in the appended section. The gate passes because its publication test requires only the anchor ID and quote there.

## Evidence

- **Snapshot heading — PASS.** The pinned snapshot has `# mori-shokunin — Province` at line 1 (`8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-19/l1-capture/siblings/mori/91940fa339e3/PROVINCE.md:1`). The target registry records that exact heading (`8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/adjacency-anchors-r19.json`, `outbound[0]`).
- **Quote and limit — PASS.** The recorded quote is exact on snapshot line 9, appears once, and is 17 whitespace-separated words; line 9 lies inside pointer range 6–16 (same snapshot line above; target registry `outbound[0].quote`, `quote_line`, and `province_pointer`).
- **Snapshot digest — PASS.** `sha256sum` of the captured snapshot and of `git cat-file -p <pin>:PROVINCE.md` both output `73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130`, matching target registry `outbound[0].sibling_blob_sha256`.
- **Pinned commit and reachability — PASS.** `cat-file -e '<pin>^{commit}'` exited 0. `master`, `origin/master`, and `HEAD` resolve to `3786f3f1bde2fbcc5ce617e35e8c9becdbf9d9e8`; `master..91940fa...` has no commits and `91940fa... ..master` contains 11 commits. Thus the pin is reachable from master and is 11 commits behind its tip. `--abbrev-ref HEAD` reported `HEAD`, so the checkout is detached at that same tip; this does not change the master reachability result.
- **Original pointer — PASS.** At target `PROVINCE.md:33`, the Core text retains `../mori-shokunin/PROVINCE.md:6-16` (`8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:33`).
- **Appended section — PARTIAL / FALSIFIER.** The target section starts at `PROVINCE.md:108`; row 121 includes the expected title heading and verbatim quote, but lists only `91940fa339e3` and contains no 64-hex SHA-256 anywhere in the target PROVINCE file (`8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:119-121`; target-blob line check). The complete pin and digest are in the registry JSON, not republished in that row. The prose at `PROVINCE.md:114-117` says the commit and digest identify the bytes, but does not state either digest value.
- **Gate treatment.** The exact target gate source was confirmed unchanged from the invoked source. Its `_outbound_publication` checks only that a line after the configured section heading contains both anchor ID and quote (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-adjacency-anchors.py:224-227`); `evaluate` uses that result to emit `ANCHOR-UNPUBLISHED` or mark the anchor portable (`:432-447`). It does not require the publication line to carry the full commit or digest. The run returned `PASS`, `outbound_portable: 10`, `live_object_checked: 10`, and `live_object_match: 10`, with no findings. Operationally, the section is a required publication location for gate passage, but the gate does not classify outbound rows as “operative”; operative/historical scope is the inbound classification. The section itself says it “grants no authority” and is “an ownership locator, not a repair mandate” (`PROVINCE.md:117`).
- **Old-range reader — NOT MISLED at present.** Comparing committed sibling `PROVINCE.md` lines 6–16 at the pin and current master returned `cited_range_identical=True`. The pin is stale by 11 commits, but the cited range is unchanged at the tip.

## Residual

This attack establishes that the full digest is absent from the appended OUT-001 publication; it does not challenge the correctness of the proposition itself. The current old line range is accurate, but future edits above it could move the referenced content. No tools were installed and no host actions were taken.

Scope: executed=python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116; sha256sum .ufo/waves/round-19/l1-capture/siblings/mori/91940fa339e3/PROVINCE.md; git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -p 91940fa339e38006f8db5bd7d78bb6f037f4d016:PROVINCE.md | sha256sum; git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e '91940fa339e38006f8db5bd7d78bb6f037f4d016^{commit}'; git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse master origin/master HEAD; git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline master..91940fa339e38006f8db5bd7d78bb6f037f4d016; git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline 91940fa339e38006f8db5bd7d78bb6f037f4d016..master | wc -l; git diff --exit-code 8e5916360f2dfe7bc4eb4ba144081af555900116 -- tools/check-adjacency-anchors.py; read-only git-show/Python line and JSON checks.