# ScribeLesson — round 81 wave w1 report

Seat: ScribeLesson (scribe, leaf, no dispatch). Axes: depth, operability, freshness. Milestone scope: fstab→mount-unit plane, round-80 counter gate-standard repair, provenance-header closure (this seat covers the lesson draft only).

## Deliverables
- Draft lesson skeleton: `.ufo/waves/round-81/w1/ScribeLesson/round-81.md` (DRAFT; no production file written).
- Receipts (observed command outputs): `.ufo/waves/round-81/w1/ScribeLesson/receipts.md`.
- No production registry, knowledge, lesson, tool or Git/jj state was changed. No SOURCES.md edit.

## Observations (command and output in receipts.md)
1. Pinned digests: `sha256sum -c SHA256SUMS` in `before/src/` → 3 of 3 OK (receipts R1).
2. Live re-fetch of S331 and the generator doc (curl rc0) gives SHA256 afbf3be6…2394 and 8de8acb8…c41; `cmp` against the pinned copies rc0 for both (receipts R2).
3. Registry: rows 330 → 332; malformed 0; mined 292 → 294; queued 5 unchanged; rejected 33 unchanged; tier A 313 → 315 (receipts R6). `git diff --numstat` on SOURCES.md is `2 0`, so no existing row changed.
4. Defect A (count): knowledge note line 30 says "six local file systems; four are required". The `/etc/fstab` awk count gives 7 local block file systems, 5 required and 2 nofail (receipts R4). S332's `teaches` cell says "four required mounts" and generator.txt lines 141-145 show five (receipts R3, R5).
5. Defect B (wrong unit line range): the note cites tmp.mount at S332 :35-47 vs :95-107. Lines 95-107 are var-log.mount; tmp.mount is at 64-77 (receipts R3). MT5's measured leg (S332 99-100) is also var-log.mount.
6. Round-80 defect class R80-C2-REGISTRY-NAME is located at `corpus/lessons/round-80-verifier-spotcheck.md:281-283`, `corpus/lessons/round-80.md:51`, and QUALITY 111 at `corpus/QUALITY.md:217`. QUALITY 111 was written after the miss, so it was not in force at the round-80 freeze.
7. Checker reading (not executed): `tools/check-knowledge-header.py:212` uses the last operative `verified-at:` hit, so the appended round-81 lines in the two filed notes are the lines that count.
8. Adjacent community source opened: ArchWiki "fstab" (reader text, 2026-11-04). It has no revision anchor, and its "External devices" section carries a factual-accuracy-disputed banner on the nofail claim. Refused; the Gate records the flip conditions.

## Gate decisions (in draft)
- S331 admitted (tier A/docs, mined, on-release).
- S332 admitted with defect: its `teaches` cell is false and needs a `supersedes S332 —` row. Tier A for an own-work one-time capture is [INFERENCE], flagged for the outside check.
- Snapshot-only generator XML and fstab-generator.c not admitted (no citation in the note).
- Rejected interpretation of S331: nofail does not guarantee no waiting once an explicit Before= is set.
- Outside admit/reject spot-check: PENDING. No wave seat can supply it.

## Registry changes (old → new)
- Existing rows: none.
- S331: status none → mined; recheck none → on-release; used-by none → knowledge note (add lesson path when filed).
- S332: status none → mined; recheck none → 30d; used-by none → knowledge note. Its `teaches` cell needs correction (see defect A).

## Unknown / not done
- Not run: `count-mount-rows-r81.py`, `measure-round81.py`, `check-knowledge-header.py`. Assignment was read-only drafting, so verification belongs to the main agent.
- Whether `measure-round81.py` consumes `before/actual-registry-identities.json` is not verified.
- Whether the wave's Seat harm entries are empty is unknown: no `after/` settlement exists (receipts R7, rc2). Seat harm is recorded as pending, not as "none observed".
- The boot-time cost of the /tmp device wait is not measured; the note's "up to ten seconds" is [INFERENCE] from the device timeout and ordering.
- The uncommitted tools/measure-round80.py change in the working tree is not attributed; no process trace or disclosure is in my evidence.

## Tools
None installed or updated. Read `/home/vgpnk/.omp/agent/RULES.md` (the first path I tried was mistyped; the correct path read fine). pacman not used. curl was used for read-only fetches; it is an existing tool, not an install.

## Scratch
Owned scratch `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tsukuroi-r81/ScribeLesson/` held only the live S331/generator XML fetches (copied digests into receipts R2). It is removed before yield.

## Next actions for the lane (not performed here)
1. Re-point tmp.mount to lines 64-77 and fix MT5's measured leg.
2. Replace "six … four" with "seven … five required, two nofail" and cite the awk command.
3. File `supersedes S332 —` with the corrected teaches cell.
4. Outside admit/reject check before filing the production lesson.
