## Attack

Test C1's outbound-anchor claim against OUT-004 (`mado/PROVINCE.md`): the pinned snapshot, heading, quote, commit, and digest are all checkable, as are the preserved pointer and the appended publication row. The specific failure criterion is whether that appended PROVINCE row itself republishes the anchor's blob SHA-256, rather than merely storing it in the registry. Also check whether a reader using only the retained line range misses ownership-scope qualifications.

## Method

Read the OUT-004 registry/census records, pinned snapshot, target PROVINCE section, and gate source. Ran these read-only commands from the tsukuroi lane:

```sh
sha256sum .ufo/waves/round-19/l1-capture/siblings/mado/a4046a821608/PROVINCE.md
python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116
git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -e a4046a8216080d4004de3f268c62cf142095ac07^{commit}
git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -p a4046a8216080d4004de3f268c62cf142095ac07:PROVINCE.md | sha256sum
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse --abbrev-ref HEAD
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --format='%H' HEAD..a4046a8216080d4004de3f268c62cf142095ac07 | wc -l
git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --format='%H' a4046a8216080d4004de3f268c62cf142095ac07..HEAD | wc -l
git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --stat a4046a8216080d4004de3f268c62cf142095ac07 HEAD -- PROVINCE.md
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md | sha256sum
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-19/l1-capture/siblings/mado/a4046a821608/PROVINCE.md | sha256sum
```

Also compared the committed registry, census, knowledge file, and PROVINCE.md at the target revision with their working-tree copies; inspected the gate's outbound checks at `tools/check-adjacency-anchors.py:382-445` and publication helper at `:224-227`; and compared the census's recorded `3-16` text with snapshot lines 3-16.

## Verdict

**REFUTE — C1, limited to OUT-004's published digest.**

1. **CONFIRM:** the pinned snapshot has heading `# mado-shokunin — Province` at line 1.
2. **CONFIRM:** registry quote is an exact substring of snapshot line 6 and is 6 words (within the 25-word limit).
3. **CONFIRM:** snapshot SHA-256 is `1b25bb1e980925b356663602d002c1c15307a0dfac8bfafd9988bd4d8df7464b`, matching the registry and the blob at the pinned sibling commit.
4. **CONFIRM:** full pinned commit `a4046a8216080d4004de3f268c62cf142095ac07` exists and is an ancestor of sibling `master` tip `451c7e41f278e55e85347f91246dd32ad86c346e`. The sibling checkout is detached at that same tip. There are 0 commits in `HEAD..pin`, 12 in `pin..HEAD`, and the PROVINCE blob/diff is unchanged between pin and tip.
5. **Pointer CONFIRMED; publication REFUTED:** the original pointer remains at target `PROVINCE.md:48`. The appended row at `PROVINCE.md:124` carries OUT-004, heading, quote, and commit prefix `a4046a821608`; the prefix resolves to the pinned commit. It does **not** carry the blob SHA-256: the table header at line 119 has no digest column, and the expected digest is absent from PROVINCE.md. The full commit and digest are in the registry (`corpus/knowledge/adjacency-anchors-r19.json:52-57`), not republished in this row.

The gate treats this appended section as the outbound publication surface, but does not give outbound anchors an `operative`/`historical` classification (those scopes apply to inbound records). Its publication predicate only requires a line after the section heading to contain the anchor ID and quote (`tools/check-adjacency-anchors.py:224-227,432-438`); digest and pinned-object verification come from the registry/snapshot/live-object checks, not the published row. The requested gate run passed with no findings: `outbound_portable=10`, `live_object_checked=10`, `live_object_match=10`, revision `8e5916360f2dfe7bc4eb4ba144081af555900116`.

A reader following only `../mado-shokunin/PROVINCE.md:3-16` can be misled about theme/wallpaper scope: snapshot lines 8-9 describe themes/wallpapers as declared files, while line 18, outside that range, refines this to the omarchy theme plane and names exclusions including `hooks/**`, `branding/`, `extensions/`, and `themed/` machinery. The census's stored `cited_text_at_tip["3-16"]` exactly matches snapshot lines 3-16, so the refinement is not covered by that citation.

## Evidence

- OUT-004 source fields: `corpus/knowledge/adjacency-anchors-r19.json:48-58` (pointer, full commit, SHA-256, snapshot path, heading, quote, quote line).
- Snapshot: `.ufo/waves/round-19/l1-capture/siblings/mado/a4046a821608/PROVINCE.md:1,6,8-9,18`. The `sha256sum` result matches both the registry digest and `git cat-file`'s pinned `PROVINCE.md` blob; byte comparison was identical.
- Census: `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json:2871-2888` records pointer `../mado-shokunin/PROVINCE.md:3-16`, pin, digest and captured range text.
- Published target: `PROVINCE.md:108-117` defines the append-only locator section; `:119` is the table header; `:124` is OUT-004. The digest does not occur in PROVINCE.md; its only row commit value is the 12-character prefix.
- Gate: `tools/check-adjacency-anchors.py:392-416` validates snapshot digest, heading and quote; `:426-438` checks pointer presence and publication; `:440-445` checks the live pinned object. The run returned `PASS`, `findings: []`, and 10/10 outbound/live-object counts.
- Sibling tip evidence: `git log --all --format='%h %D | %s' -n 6` identified `451c7e41` as `HEAD, origin/master, origin/HEAD, master`; pin-to-tip log counts were 0 and 12. `git diff --stat <pin> HEAD -- PROVINCE.md` was empty and both file blob IDs were `885f4ea0018a0442ebb8d768882b08169298e853`.

## Residual

This seat checked only OUT-004, not all ten outbound anchors. The gate PASS confirms the registry/snapshot/live-object checks for the whole outbound set, but does not establish that each PROVINCE row republishes its digest. No host state or sibling files other than mado's PROVINCE.md were inspected for behavior beyond the assigned anchor.

Scope: executed=sha256sum .ufo/waves/round-19/l1-capture/siblings/mado/a4046a821608/PROVINCE.md; python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116; git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -e a4046a8216080d4004de3f268c62cf142095ac07^{commit}; git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -p a4046a8216080d4004de3f268c62cf142095ac07:PROVINCE.md | sha256sum; git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse --abbrev-ref HEAD; git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD; git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --format='%H' HEAD..a4046a8216080d4004de3f268c62cf142095ac07 | wc -l; git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --format='%H' a4046a8216080d4004de3f268c62cf142095ac07..HEAD | wc -l; git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --stat a4046a8216080d4004de3f268c62cf142095ac07 HEAD -- PROVINCE.md; git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md | sha256sum; git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-19/l1-capture/siblings/mado/a4046a821608/PROVINCE.md | sha256sum
