## Attack

Re-verified OUT-002 end to end against its pinned sibling snapshot and the lane revision. C1 is falsifiable at the publication boundary: the claim says the appended PROVINCE section republishes the blob SHA-256, not merely that the registry stores it or that the section mentions a hash generically.

## Method

Read the OUT-002 registry row and snapshot, inspected the sibling commit and current `master` tip read-only, compared the pinned and current sibling PROVINCE content, and read the gate implementation. Ran the gate only in a fresh `/tmp` clone of the assigned lane revision.

Commands used for the decisive checks:

```text
sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/kama/e75cf680b534/PROVINCE.md
git cat-file -e e75cf680b53484a61709ee1b2787d8dbc6419f74^{commit}
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kama-shokunin rev-parse master origin/master HEAD
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kama-shokunin merge-base --is-ancestor e75cf680b53484a61709ee1b2787d8dbc6419f74 HEAD
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kama-shokunin rev-list --count e75cf680b53484a61709ee1b2787d8dbc6419f74..HEAD
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kama-shokunin show e75cf680b53484a61709ee1b2787d8dbc6419f74:PROVINCE.md | sha256sum
cmp /tmp/fxout002/kama-PROVINCE.pin-e75cf680.md /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/kama/e75cf680b534/PROVINCE.md
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md > /tmp/fxout002/PROVINCE.8e59163.md
git clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/fxout002/tsukuroi-clone
git -C /tmp/fxout002/tsukuroi-clone checkout --quiet --detach 8e5916360f2dfe7bc4eb4ba144081af555900116
PYTHONDONTWRITEBYTECODE=1 python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116 --siblings-root /home/vgpnk/Projects/shokunin
```

Also used read-only JSON/line inspection and `git diff --stat e75cf680b53484a61709ee1b2787d8dbc6419f74 37bd4c5bd456a2f8a54d3312c28495c321715856 -- PROVINCE.md` to compare the pin with the sibling tip.

## Verdict

**REFUTE — C1 (OUT-002).**

1. **PASS — heading:** snapshot line 1 is exactly `# kama-shokunin — Province`.
2. **PASS — quote and line:** snapshot line 12 contains the exact registry quote, `` `GET /v1/models` vs `--alias` vs the configured model id ``; it is 9 whitespace-delimited words (under 25).
3. **PASS — snapshot digest:** snapshot SHA-256 is `799432d748bd40bcf859de806cc2ef90df069da14c8e5c07bf72250ac411c7a6`, matching the registry. The pinned commit's `PROVINCE.md` blob has the same SHA-256, and `cmp` confirms the captured snapshot is byte-identical to that blob.
4. **PASS — pinned commit:** `cat-file -e` succeeded. The sibling `master`, `origin/master`, and detached `HEAD` all resolve to `37bd4c5bd456a2f8a54d3312c28495c321715856`; the pin is an ancestor, 21 commits behind that tip.
5. **REFUTE — republished digest:** at lane revision `8e5916360f2dfe7bc4eb4ba144081af555900116`, PROVINCE preserves the old pointer and the appended section includes OUT-002's heading, quote, and 12-character commit prefix, but the section contains no OUT-002 blob SHA-256 value (nor any 64-hex digest). The digest is in the registry, not in the published PROVINCE row. Thus the required publication is incomplete even though the underlying snapshot pin is sound.

The gate treats the appended section as required outbound publication: it checks for an anchor id and quote after that section heading. It does **not** require the heading, commit, or SHA-256 to be present in the published row. The gate passed in the scratch clone with `outbound_portable: 10`, `live_object_checked: 10`, `live_object_match: 10`, and no findings; this PASS does not test the missing digest publication. “Operative/historical” scope labels are applied to inbound classifications, not outbound anchors.

A reader following only the old line-range pointer is **not misled about the cited ownership text as of the checked sibling tip**: the range is `3-24`, the quote is still on line 12, and those lines match the pin; the later sibling change appends after line 80. The old range alone does not expose the appended publication metadata. The lane's ADJ-01 row separately supplies the driver/GPU boundary; the pinned sibling text itself does not mention driver/GPU readiness.

## Evidence

- Registry row: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/adjacency-anchors-r19.json:22-32` records the pointer, full commit, expected blob SHA-256, heading, quote, and `quote_line: 12`.
- Pinned bytes: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/kama/e75cf680b534/PROVINCE.md:1-12` shows the exact title and quote. `sha256sum` output was `799432d748bd40bcf859de806cc2ef90df069da14c8e5c07bf72250ac411c7a6`; `git show <pin>:PROVINCE.md | sha256sum` returned the same digest; `cmp` succeeded.
- Commit reachability: `git cat-file -e <full-pin>^{commit}` succeeded; `git merge-base --is-ancestor <full-pin> HEAD` exited 0; `git rev-list --count <full-pin>..HEAD` returned `21`; branch refs and HEAD reported tip `37bd4c5bd456a2f8a54d3312c28495c321715856`.
- Lane pointer and appended row: `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:46` retains `../kama-shokunin/PROVINCE.md:3-24`; `:108-122` contains the appended section and OUT-002 row. The row has `@ e75cf680b534`, the expected title and quote, but not the full commit or `799432d748bd40bcf859de806cc2ef90df069da14c8e5c07bf72250ac411c7a6`.
- The sibling pin-to-tip diff is only a 16-line append after line 80; the evaluated pin/tip lines 3-24 are equal. The quote remains at line 12 at both revisions.
- Gate source: `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-adjacency-anchors.py:392-423` validates the stored snapshot digest, heading/quote location, and quote length; `:426-437` checks the old pointer's presence and publication of only anchor id plus quote. Gate command output: `status: PASS`, `findings: []`, `outbound_portable: 10`, `live_object_checked: 10`, `live_object_match: 10`.

## Residual

No host/service/boot action was taken and no tool was installed. The pinned commit is behind the sibling tip, so future sibling edits could change the unpinned line-range target; this check establishes that lines 3-24 have not changed at the observed tip. The sibling quote supports served-model reconciliation; the separate GPU-readiness boundary is in the lane's ADJ-01 text rather than the pinned quote.

Scope: executed=sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/kama/e75cf680b534/PROVINCE.md; git cat-file -e e75cf680b53484a61709ee1b2787d8dbc6419f74^{commit}; git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kama-shokunin rev-parse master origin/master HEAD; git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kama-shokunin merge-base --is-ancestor e75cf680b53484a61709ee1b2787d8dbc6419f74 HEAD; git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kama-shokunin rev-list --count e75cf680b53484a61709ee1b2787d8dbc6419f74..HEAD; git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kama-shokunin show e75cf680b53484a61709ee1b2787d8dbc6419f74:PROVINCE.md | sha256sum; cmp /tmp/fxout002/kama-PROVINCE.pin-e75cf680.md /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/kama/e75cf680b534/PROVINCE.md; git --no-optional-locks -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md > /tmp/fxout002/PROVINCE.8e59163.md; git clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/fxout002/tsukuroi-clone; git -C /tmp/fxout002/tsukuroi-clone checkout --quiet --detach 8e5916360f2dfe7bc4eb4ba144081af555900116; PYTHONDONTWRITEBYTECODE=1 python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116 --siblings-root /home/vgpnk/Projects/shokunin