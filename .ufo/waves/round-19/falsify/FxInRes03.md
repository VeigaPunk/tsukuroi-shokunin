## Attack

Tested whether the ten historical inbound `RESOLVES` entries IN-026..IN-035 remain anchored at target revision `8e5916360f2dfe7bc4eb4ba144081af555900116`: each quote must occur at its recorded line inside the target range, the pinned sibling line must retain the stated reliance, and `relied_on` must fairly describe the lane text. A wrong quote, range, pin, or overbroad reliance would falsify the batch.

## Method

- Read the registry and pointer census, then loaded target blobs from the target revision and sibling files with read-only `git show` at the census-pinned sibling commit `a4046a8216080d4004de3f268c62cf142095ac07` (mado). Compared the exact quote occurrence and range membership for every ID; compared each pinned sibling line against the census line text.
- Scanned the full cited PROVINCE range for IN-027’s input/probing/DRM terms and checked the round-15 sibling discussion for scope context. Checked that the four corpus entries named by IN-034 exist as blobs at the target revision.
- Created a fresh clone at `/tmp/fxinres03/lane`, checked out the target revision, and ran `python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116` there. It returned `PASS`, 114/114 classified, with 97 RESOLVES, 17 DRIFTED, no findings, and 10/10 live sibling object matches. The gate’s inbound check verifies quote occurrence and range/classification consistency (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-adjacency-anchors.py:521-541`); it does not establish that a broader sibling proposition is semantically supported.

## Verdict

**REFUTE — C1 adjacency, IN-027.** The quote and range pass, but the sibling line asserts ownership for kernel input events and specific probing interfaces not established by its cited lane text; the RESOLVES result overstates that pointer’s support. The other nine IDs CONFIRM.

| ID | Verdict | Target quote / found line (range) | Pinned sibling reliance line |
|---|---|---|---|
| IN-026 | CONFIRM | `SKILL.md:1707` (`1705-1715`) | mado `RegistryDraft.md:57` |
| IN-027 | REFUTE | `PROVINCE.md:12` (`3-14`) | mado `SiblingOverlap.md:28` |
| IN-028 | CONFIRM | `PROVINCE.md:12` (`6-14`) | mado `SiblingOverlap.md:130` |
| IN-029 | CONFIRM | `PROVINCE.md:12` (`6-14`) | mado `reports/SiblingOverlap.md:130` |
| IN-030 | CONFIRM | `PROVINCE.md:11` (`11-14`) | mado `ReviewSafety.md:65` |
| IN-031 | CONFIRM | `PROVINCE.md:48` (`48-48`) | mado `ReviewSafety.md:65` |
| IN-032 | CONFIRM | `PROVINCE.md:8` (`8-15`) | mado `SiblingBoundary.md:155` |
| IN-033 | CONFIRM | `PROVINCE.md:8` (`8-14`) | mado `SiblingBoundary.md:35` |
| IN-034 | CONFIRM | `PROVINCE.md:20` (`16-23`) | mado `SiblingBoundary.md:36` |
| IN-035 | CONFIRM | `PROVINCE.md:28` (`25-28`) | mado `SiblingBoundary.md:37` |

## Evidence

- The ten registry records and their recorded lines/ranges are present at target revision in `8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/adjacency-anchors-r19.json:681-878`. All ten quotes occur on their exact recorded `found_line`, with no offset needed, and every found line is inside its target range. Pinned sibling lines match the census text; the sibling blobs were read at commit `a4046a8216080d4004de3f268c62cf142095ac07`.
- IN-026’s eight-column header is at `8e5916360f2dfe7bc4eb4ba144081af555900116:SKILL.md:1707`; the sibling cites that row-shape precedent at `a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-13/w1/reports/RegistryDraft.md:57`.
- **IN-027:** target line 12 says “driver/firmware plane (kernel modules, nvidia driver + GSP firmware”; the line is inside the `Owns` section and the pointer range. But the pinned sibling line `a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-13/w1/reports/SiblingOverlap.md:28` extends the assertion to `/dev/input/event*`, `evtest`, `evemu`, `libinput debug-events`, and DRM/KMS/video drivers. The cited target range `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:3-14` names the OS substrate, drivers/firmware, and host probes, but does not name input events or those probing tools. The registry itself acknowledges that these specifics are “not literal PROVINCE text” at `8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/adjacency-anchors-r19.json:718`. Thus the narrowed `relied_on` description is fair for the driver/firmware clause, but does not account for the full reliance made by the sibling sentence. Round-15 mado `ReviewSafety.md:65` likewise notes that PROVINCE.md:6-9 does not list input devices; it infers the kernel/driver boundary rather than supplying the missing input-device text.
- IN-028 and IN-029 have valid quotes/ranges and both point to the next-recipient line in the pinned mado snapshot. The two sibling files are byte-identical at the pin (read-only comparison); these are duplicate support, not independent corroboration.
- IN-030/031 quotes match the cited journal/boot and ADJ-03 rows. IN-032/033’s owns-surfaces declaration covers the cited host surfaces. IN-034’s table contains the cited four additional surfaces in rows 20-23, and all four named corpus paths are blobs at the target revision. IN-035’s no-mutation/detection-only paraphrase matches lines 27-28.

## Residual

The pinned text does not establish a separate authoritative owner for input-event and hardware-probing behavior; IN-027’s broader boundary therefore remains unsupported by this cited range. All ten pointers are historical and this check does not establish their validity against later sibling heads.

Scope: executed=mkdir -p /tmp/fxinres03 && rm -rf /tmp/fxinres03/lane && git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/fxinres03/lane && git -C /tmp/fxinres03/lane checkout -q 8e5916360f2dfe7bc4eb4ba144081af555900116; git -C /home/vgpnk/Projects/shokunin/mado-shokunin show a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-13/w1/reports/RegistryDraft.md; git -C /home/vgpnk/Projects/shokunin/mado-shokunin show a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-13/w1/reports/SiblingOverlap.md; git -C /home/vgpnk/Projects/shokunin/mado-shokunin show a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-14/w1/SiblingOverlap.md; git -C /home/vgpnk/Projects/shokunin/mado-shokunin show a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-14/w1/reports/SiblingOverlap.md; git -C /home/vgpnk/Projects/shokunin/mado-shokunin show a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-15/w1/reports/ReviewSafety.md; git -C /home/vgpnk/Projects/shokunin/mado-shokunin show a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-15/w1/reports/SiblingBoundary.md; git -C /home/vgpnk/Projects/shokunin/mado-shokunin show a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-16/w1/reports/SiblingBoundary.md; python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116