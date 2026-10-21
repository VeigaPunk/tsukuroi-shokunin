## Attack

Tested the C1 outbound adjacency claim against the attacked `PROVINCE.md`: whether the new section is strictly appended, uses the exact heading, publishes all ten ownership anchors with heading/quote/commit/blob-SHA256, agrees with the JSON registry and pinned sibling bytes, and associates each old sibling line-range citation with a portable anchor. This is falsifiable by comparing the baseline prefix, the published table, registry records, and pinned sibling objects.

## Method

- Read `PROVINCE.md` at `452a054677f6b18284917d7c08c45361f91c25ac` and `8e5916360f2dfe7bc4eb4ba144081af555900116`; compared their bytes, lengths, and diff; checked baseline ancestry.
- Read `corpus/knowledge/adjacency-anchors-r19.json` and `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json` at the attacked revision. Cross-compared all outbound IDs and pointer strings against body citations and rows.
- Ran read-only Python cross-checks of every body row against its registry entry; for each pinned sibling commit checked commit type, tree mode, full-blob SHA-256, lane snapshot SHA-256, heading, quote line/text, and whether the displayed 12-hex commit prefix resolves uniquely. Checked cited range components against each matched anchor's `quote_line`.
- Read relevant sibling source ranges from the pinned commits for the multi-range citations.
- Ran `python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116` from the lane. Compared `git --no-optional-locks status --porcelain` hashes before and after; status was unchanged.
- No tools were installed or updated.

## Verdict

**REFUTE — C1 outbound portable-anchor claim.** The section is append-only and its heading is exact; all ten registry pins and quotes are internally verified. But the ten published anchors do not carry the claimed blob SHA-256 field, so not all four portable fields are present in `PROVINCE.md`. All ten old pointer strings do have corresponding anchor IDs; three multi-range citations retain components not represented by their anchor quote locations.

## Evidence

**High — published anchors omit the blob digest.** At `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:119`, the table columns are `Anchor | ADJ row | Sibling file @ commit | Heading | Quote | Proposition`; there is no blob-SHA column. All ten rows at `PROVINCE.md:121-130` contain a 12-hex commit prefix, heading, and quote, but none contains a 64-hex digest. The body mentions `blob sha256` only as prose at `PROVINCE.md:114`; it does not publish a digest value. The exact section heading is at line 108: `## Adjacent — portable ownership anchors (round 19)`.

The JSON registry does carry a full `sibling_commit` and `sibling_blob_sha256` for each record (for example, `corpus/knowledge/adjacency-anchors-r19.json:9-19` for OUT-001 and `:126-136` for OUT-010). The cross-check found all ten body rows agree with their registry records on ID, sibling, displayed commit prefix, heading, quote, and proposition. Each registry commit is a valid commit with a regular `100644` `PROVINCE.md` blob; the blob's SHA-256 and the lane's committed snapshot SHA-256 both equal the registry value for all ten. Every quote occurs verbatim on its registered quote line under the registered heading, with 6–17 words. Each body commit prefix resolves uniquely in the current sibling repository. Thus registry/source integrity is confirmed, but it does not supply the missing digest in the published body anchors.

The gate returned `status=PASS`, `outbound_total=10`, `outbound_portable=10`, `live_object_checked=10`, and `live_object_match=10`, with no findings. Its publication check at `tools/check-adjacency-anchors.py:224-227` and `:432-437` only requires an anchor ID and quote on a line after the section heading; it does not require the body row to publish the blob SHA-256. The gate pass therefore does not contradict the missing-field finding.

**Confirmed — additive, exact heading.** Baseline `PROVINCE.md` is 9,384 bytes; attacked `PROVINCE.md` is 13,845 bytes. `cmp -n 9384` and comparison of the complete baseline against the attacked file's first 9,384 bytes both succeeded. The diff is solely an insertion after baseline line 106 (`106a107,132`): 26 appended lines, no removed or changed baseline bytes. The baseline is an ancestor of the attacked revision. The heading at attacked `PROVINCE.md:108` matches the required heading exactly, including the em dash.

**Pointer mapping — none wholly unanchored; old references remain.** The ten old pointer strings in attacked `PROVINCE.md:33` and `:46-52` exactly match the ten `province_pointer` values in the registry and the ten census outbound pointers; each has one corresponding OUT anchor in `PROVINCE.md:121-130`. No pointer string lacks a matching anchor. The original pointers remain byte-identical: the appended-section preamble explicitly says they “are not changed” at `PROVINCE.md:110-113`, and the baseline-prefix comparison confirms that. They were retained, not removed.

There is partial coverage if “superseding” is read as replacing every component of each multi-range citation: OUT-003's quote is at kagi line 3 but the old citation also includes `10-17,32-34,54` (`PROVINCE.md:47`; registry `:35-45`); OUT-008 quotes kaidoku line 3 but the citation also includes `88-100` (`PROVINCE.md:51`; registry `:99-110`); OUT-009 quotes revenger line 3 but the citation also includes `19-25` (`PROVINCE.md:51`; registry `:112-123`). The pinned kagi lines 10-17 describe historical/absent substrate and lines 32-34 runtime-state surfaces; line 54 is blank. The pinned kaidoku lines 88-100 include its adjacent refusal/defer boundary; revenger lines 19-25 include its refusal and write boundary. These are not represented by those anchors' quote locations. This does not leave an entire body pointer without an OUT ID, but it does leave those cited components line-range-only.

## Residual

- No body pointer is wholly missing a corresponding anchor; the partial-range issue above depends on whether “superseding” requires coverage of every component of a multi-range citation rather than one portable locator per pointer.
- Commit-prefix uniqueness was checked in the current sibling object databases only. The report makes no claim that a 12-hex abbreviation is collision-proof in future object sets.
- No mutation test was run; the actual attacked revision, gate, registry, snapshots, and pinned sibling blobs were inspected read-only.

Scope: executed=git show 8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md; git show 452a054677f6b18284917d7c08c45361f91c25ac:PROVINCE.md; sha256sum /tmp/fxprov/prov_8e59.md /tmp/fxprov/prov_452a.md; cmp -n 9384 /tmp/fxprov/prov_8e59.md /tmp/fxprov/prov_452a.md; cmp /tmp/fxprov/prov_452a.md <(head -c 9384 /tmp/fxprov/prov_8e59.md); diff /tmp/fxprov/prov_452a.md /tmp/fxprov/prov_8e59.md; python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116; git --no-optional-locks status --porcelain; git merge-base --is-ancestor 452a054677f6b18284917d7c08c45361f91c25ac 8e5916360f2dfe7bc4eb4ba144081af555900116; read-only Python Eval cross-checks of registry/body/sibling pins and pointer ranges; git show of the cited sibling ranges.