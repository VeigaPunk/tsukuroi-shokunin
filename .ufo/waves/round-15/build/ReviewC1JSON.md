# ReviewC1JSON — round 15 C1 (depth) read-only review

Status: **ALIGNED from the C1 pair's side**, with one residual outside it. Pair: `corpus/knowledge/source-locator-clarification-r15.md` / `.json`; S046 row at `corpus/SOURCES.md:52`. No test or checker was run; nothing is claimed to pass. Read-only; I edited no pair file.

## Verified against source (text rendering, footer `systemd 262.1`, opened 2026-10-20)
- Definition, exact (line 1402): `Takes a boolean argument or the special values "full" or "strict".` 11 words. Matches MD R15-POSITIVE-DOMAIN, JSON R15-POSITIVE-DOMAIN.quote and the S046 row.
- Following sentence, exact (lines 1403–1404, break after `(/boot` / `and /efi)`): `If true, mounts the /usr/ and the boot loader directories (/boot and /efi) read-only for processes invoked by this unit.` 20 words. MD R15-LOCATOR blockquote and JSON R15-LOCATOR.quote are now identical.
- Recurrence fix: the MD no longer claims the full sentence recurs. The template `Takes a boolean argument or the special values` does recur at ProtectHome (1430) and ProtectControlGroups (2324) with different values, which the MD now says.
- r14 fields the r15 notice supersedes exist: `corrections[0].location` (r14 JSON line 13), `corrections[0].replacement` (line 15), `sources[0].anchor` (line 167). `r15_supersession` (lines 203–241) is additive.
- No bare line number appears in JSON `location`, `quote` or `replacement`. The only `1266-1267` is quoted and withdrawn.
- MD order: provenance trio, `## R15-LOCATOR`, `## R15-POSITIVE-DOMAIN`, `## QUALITY check`.

## Residual outside the pair (not fixed here)
- **S046 row, `corpus/SOURCES.md:52`** (SourceRegistry's file, not this pair): the row text says "systemd 262.1 man-page footer, core/systemd 262.1-1". The footer I read says only `systemd 262.1`; the package string is not on the page. Owner should remove it or mark it as an unverified host or package fact. The same string appears in the SourceRegistry re-open paragraph at `SOURCES.md:89`.

## Unverified / limits
- "No `id` anchor in native HTML" is executor-observed in the bytes that executor fetched. My HTML fetch failed three times (ECONNRESET), so it is not reproduced here.
- The "293394 bytes" body size and the S046 sha256 are not reproduced here.
- QUALITY criteria 21–22 in the MD are not checked against `corpus/QUALITY.md`; if they are not defined there, they are local labels.
- No check of `LOG.md`, `SCORECARD.md` or the round-15 checker; those are L1's.

## Coordination and tools
- Replied to `TsukuroiR15.LocatorEntry` (delivered): aligned from my side.
- Tools: read, grep on the spilled text artifact, bash (file presence). Installed or updated: **none**. No package, service, sudo or pacman action.
- Checks for L1 after integration: re-grep the S046 row for `core/systemd`; confirm QUALITY 21–22 exist or are labelled local.
