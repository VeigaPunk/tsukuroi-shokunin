survives with defects — attacked the tsukuroi corpus/SOURCES.md census at 22fd1642: the exact `sources-census.sh validate` run, the frozen CORPUS.md census commands, the start-census delta, and the round-24 registry-change claims in corpus/lessons/round-24.md. The counts, the malformed-row result and the start-census delta survive. The lesson's W04 disclosure, the missing Search-log note, two citation and anchor rules, and the undisclosed re-registrations of existing pages do not.

## Measured results

Both tools exit 0 from the lane root and agree on every number.

- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`: exit 0; no E-codes (validator errors); 15 W04 lines (warning: same URL under two scopes) plus `tsukuroi ok`.
- Frozen block (CORPUS.md lines 134–147, run from the lane root): rows 103; malformed rows 0; tier A=95 B=1 C=7; status mined=89 queued=5 rejected=9; no duplicate IDs; no enum or tier-inflation hits; no mined used-by path missing.
- `sources-census.sh census`: same totals. `overdue`: 0 rows overdue as of 2026-10-22; all 103 rows carry cadence-only recheck values.

| Dimension | Counts |
|---|---|
| Tier | A 95 · B 1 · C 7 |
| Status | mined 89 · queued 5 · rejected 9 |
| Kind | docs 55 · code 16 · own-work 23 · dataset 2 · tool 2 · community 5 |

- Tier by status: A/mined 88, A/queued 5, A/rejected 2, B/mined 1, C/rejected 7. No invalid tier, status or kind; no community row at tier A.
- Structure: 103 rows, IDs S001–S103 contiguous with no duplicates; every row has 13 fields (11 cells plus the empty ends); no indented, carriage-return or tab lines.
- Round-24 rows S087–S103: 17; all tier A, all mined, all opened 2026-10-22; kinds docs 9, code 7, dataset 1. This matches lesson line 29.
- New warnings against `census-start.txt`: six lines added, none removed, no other code changed. The six are S087, S089, S090, S092, S095 and S098, all W04. The nine start lines reproduce exactly from the claim-base blob f169b3ba (86 rows). That run also printed E11 lines and exit 1, because the temporary copy has no knowledge tree; only its W04 lines are meaningful.
- Git: the worktree corpus/SOURCES.md equals HEAD blob 68e0d4ac…; the f169b3ba→HEAD numstat is 17 insertions and 0 deletions, so no existing row changed.

Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevCensusEnd/ (validate-end.tsv, census-end.tsv, frozen-end.txt, validate-f169b3ba.tsv, overdue.tsv, checks.py, checks-output.txt).

## Findings

1. [obs, medium] The lesson's W04 disclosure names three of the five new duplicate pages. Lesson line 29 lists "pacman.8, the btrfs-overlayfs URL and the MR !482 URL". Two of the six new lines are not named: S087 (SOURCES.md line 93, archlinux.org/news, same URL as S001 at line 7) and S092 (line 98, System_maintenance?oldid=885170, same URL as S010 at line 16). Checker output: "archlinux.org/news (S087): False; System_maintenance (S092): False". Correction: rewrite lesson line 29 to list all six lines with their partner rows: S087 with S001; S089 and S090 with S048 and S049; S092 with S010; S095 with S057; S098 with S021.

2. [obs, medium] Round 24 has no Search-log note. The Search log in SOURCES.md (lines 118–171) ends with "Round23 bounded curation (2026-10-21)" at line 170. A search for round 24 or 2026-10-22 inside that section finds nothing. CORPUS.md line 82 and rule 5 (lines 126–128) require one prose note per bounded search, and rounds 20–23 each added one. Correction: append a round-24 paragraph (question, pages opened, identified, screened, included, excluded, exclusion reasons, stop rationale) before "## Leads (unopened)" at line 172.

3. [obs, medium; the reason is [inf]] Six of the 17 round-24 rows repeat pages already registered, and the lesson does not say so. S087, S089, S090, S092, S095 and S098 repeat the URLs of S001, S048 and S049 (pacman.8, twice), S010, S057 and S021. The 17 rows therefore cover 11 new pages (checker: distinct normalized URLs 55 before the round, 66 now). Wave-1 notes give the reason. SrcPacmanQuery.md lines 180–185 and 196–199 say the pacman.8 rows are needed because the pause-lift gate requires an `opened` date of 2026-10-22 and `opened` is immutable for existing rows. SrcPaccache.md line 43 gives the same reason. SrcSystemMaintenance.md line 15 calls the S092 row a same-revision re-opening "at a narrower scope". [inf] The gate's date rule is driving row creation, so "17 rows added" overstates new evidence. Correction: state in the lesson "17 rows: 11 new pages plus 6 same-page re-registrations opened for the gate's date rule". Whether the rule should change is an L1 decision.

4. [obs, medium] S059 is never cited by its own ID. S059 (line 65) supersedes S055 and lists two used-by files. Neither file contains "S059". boot-chain-r17.md line 1 still cites "S055 … overlay-emulation.txt". initramfs-v42-sysroot-recovery.md line 89 cites only the artifact path. The "mined" status therefore rests on path-level reuse of the superseded row's artifact. Checker: "path does not cite row id" for both files. Correction: append a notice to each file naming S059 as the current row for overlay-emulation.txt. If that is not wanted, record in the lesson that S059's mined status is path-level.

5. [obs, medium-low] Three new anchors carry no revision, and two carry it only in the URL. CORPUS.md lines 99–100 require "exact section … plus revision (version, commit, or publication date)". S090 (line 96; a pacman.8 section with no version), S100 (line 106; a `master` README with no commit or date) and S102 (line 108; a `master` file with no commit or date) cite only the `opened` date, which is not a revision. S096 (line 102) and S103 (line 109) give the revision (26.134.222, v3.8.4) only in the URL. Correction: add superseding rows ("supersedes S090 —", "supersedes S100 —", "supersedes S102 —") that pin the fetched bytes by sha256 or commit, and record the exception in the lesson.

6. [obs, low-medium] The lesson's Gate table has no location column, and the S087 entry is not a located quote. Lesson line 9 reads "| Row | URL | Located quote (at most 25 words) | Opened by |". The access date appears once, in the preamble at line 7. CORPUS.md lines 112–115 ask for URL, access date and location per row, and most rows give no location. The S087 entry at line 11 is a page heading plus a paraphrase: "Arch Linux News Archives; two rows dated 2026-10-21 (php; ca-certificates-mozilla)". The wave seat located a different quote for S087, "Update to ca-certificates-mozilla ≥ 3.131.1-1 to prevent man-in-the-middle attacks" (SrcArchNews.md line 38), and the lesson does not use it. Correction: add access-date and location columns, and replace the S087 entry with the located quote.

7. [obs, low-medium] S030's only artifact no longer exists, and two tool rows have no URL or DOI. S030 (line 36) names /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/fleet-ledger/.ufo/waves/kaika-w1/tsukuroi-art.md. `test -e` returns 1. The .tower/worktrees directory exists; the kaika directory does not. S030 and S033 (line 39) are kind `tool` with no URL or DOI, but CORPUS.md line 90 requires a canonical URL or DOI, or a repo path or command for own-work. Both rows are rejected, so tier and status counts are unaffected. Correction: record in the lesson that S030's artifact was absent on 2026-10-22 and cannot be reopened. The path check proposed in finding 12 would catch this.

8. [obs, low; definitional] One revision of one page is registered three times, and W04 shows two. S010 (line 16) and S092 (line 98) cite System_maintenance?oldid=885170. S047 (line 53) cites System_maintenance without the oldid, but its anchor says "revision oldid 885170". W04 keys on the literal URL (sources-census.sh line 601), so S047 is never reported. Checker: "same page under different URL strings" returns S010, S047, S092. Correction: say in the lesson that S092 repeats the revision already held by S010 and S047. Decide whether W04 should key on page plus oldid.

9. [obs, low] S101's recheck value "every capture" is outside the documented values. CORPUS.md lines 105–106 list 90d, 180d and on-release. sources-census.sh line 582 (symbolic()) accepts any words, so the validator never flags it. Correction: change S101's recheck to on-release. Rule 2 allows an in-place recheck change, logged old→new in the lesson. Alternatively, add the value through a new contract version.

10. [obs, low; inherited] At least 15 inherited rows contain run-together tokens. Confirmed rows: S061–S065 and S077–S086, all from rounds 18–23. Examples: S061 (line 67) "updated2.43.0" and "accessed2026-10-20"; S064 (line 70) "says2026-10-20T13:03:06"; S065 (line 71) "labels2454–2467"; S083 (line 89) "baseline894d1e…"; S084 (line 90) "opened2026-10-21". The same search finds none in S087–S103. Correction: leave the immutable cells as they are. Add a validator check for a letter run directly followed by a digit or an ISO date.

11. [inf, low] Host-state conclusions appear in the teaches cells of external-source rows. Examples: S088 (line 94: "The host runs 3.131-1 …"), S100 (line 106: "A full upgrade on this host …"), S101 (line 107: "so the host databases are older …") and S103 (line 109: "The host's core, extra and multilib repositories follow …"). CORPUS.md line 101 defines teaches as one grounded learner benefit. Older precedent exists (S029, line 35). Correction: none for immutable rows. For future rows, keep host conclusions in corpus/knowledge with their captures.

12. [obs, low; latent] The validator has gaps that no current row triggers. sources-census.sh line 559 checks used-by paths for mined rows only; the rejected rows S045 and S080 do point at existing files today. Line 648 exempts a duplicate whenever "supersedes S0NN" appears anywhere in teaches, although CORPUS.md lines 117–118 place it at the start. No current row relies on this. Line 601 reads only the first URL in a source cell; S015, S053 and S070 have two URLs, and no second-URL duplicate exists today. No check covers own-work or tool paths (finding 7) or revision anchors (finding 5). Correction: extend the used-by loop to all statuses, require the supersedes prefix at the start, scan every URL, and add the path and revision checks, each with a selftest fixture.

13. [obs, low] S089 repeats S049's quotation under a new scope. Both rows quote "Only package versions are used to find outdated packages; replacements are not checked here." (S049 line 55; S089 line 95). The cross-scope rule allows this, with a W04 warning only. Correction: state in the lesson that S089 repeats S049's quotation and why a second row is needed.

14. [obs, low] S069's source cell names "siblings/" without its parent. The directory exists at .ufo/waves/round-19/l1-capture/siblings/. Correction: none for the immutable row; the lesson can give the full path.

## Survived checks (no defect found)

- The nine start lines reproduce exactly from the f169b3ba blob, as described above.
- My independent re-implementation of the W04 rule returns the same 15 rows as the validator.
- Zero malformed rows; zero duplicate IDs; zero E-codes for invalid kind, tier or status, invalid date, invalid recheck, community at tier A, or same URL in the same scope. Zero W01, W02 or W03 warnings.
- Teaches format: all nine rejected rows read "REJECTED: …; flip: …"; no REJECTED text appears on any other row; all seven supersedes targets exist and precede their row.
- No dangling S-references: 103 distinct tokens, all registered.
- Credential-like substrings: four hits, all benign ("session" twice, "PrivateTmp=", and "tokens" in "25 whitespace tokens"). No op:// references.
- Leads #11100 and #6683 appear only as prose leads, not as rows.
- All 49 distinct used-by paths exist on disk and are tracked at HEAD, including the two gate files.
- The lesson claim "Rows touched old→new: none" holds: zero deletions.

## Residual risk and verification gaps

- I did not check the 17 new rows' quotes against their fetched pages. Wave-2 seats RevSourcesA and RevSourcesC own that.
- The frozen block cannot see date, recheck, W-code, anchor or non-mined used-by problems, and it assumes column-zero rows (CORPUS.md line 154). The maintained validator covers the first four. I did not run its selftest, which was outside this assignment.
- census-start.txt has no revision header. The exact match with f169b3ba is the evidence that it reflects the claim-base state.
- No end census is committed under .ufo/waves/round-24/census/; only census-start.txt exists. [unk] Whether the round requires one. validate-end.tsv is the candidate.
- Checks ran on the working tree, which equals HEAD for SOURCES.md and for every used-by path.

Scope: read=lane corpus/SOURCES.md, corpus/lessons/round-24.md, SCORECARD.md round-24 section (lines 740–752), corpus/knowledge/boot-chain-r17.md and initramfs-v42-sysroot-recovery.md (cited lines), census-start.txt, wave-1 notes SrcPacmanQuery, SrcPaccache, SrcSystemMaintenance, SrcArchNews, CritClaimSizing (read only), CORPUS.md census and rule sections, /home/vgpnk/Projects/shokunin/scripts/sources-census.sh (source), the tsukuroi entry of shokunin.conf (grep only), and read-only git metadata; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevCensusEnd.md and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevCensusEnd/{f169b3ba/corpus/SOURCES.md, overdue.tsv, validate-end.tsv, census-end.tsv, validate-f169b3ba.tsv, frozen-end.txt, checks.py, checks-output.txt}; executed=sources-census.sh validate (tsukuroi, exit 0), census (exit 0), overdue (exit 0) and validate --file on the f169b3ba copy (exit 1, E11 lines from the temporary copy; W04 lines compared); frozen CORPUS.md commands via sed | bash from the lane root (exit 0); git rev-parse, log, diff --stat, diff --numstat, show, hash-object without -w, status --porcelain and ls-tree (read-only); test -e path checks; python3 checks.py (read-only); read-only python checks.
Installs: none
