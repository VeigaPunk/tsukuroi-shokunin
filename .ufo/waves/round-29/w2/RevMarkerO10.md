# RevMarkerO10 — R29-OWED-O10 review (tip 10d5288)

**Verdict: holds.** The O10 marker (corpus/knowledge/storage-health-r26.json line 327) is
well-formed, the base statement is append-only unchanged, "corrected" is the right verdict,
and the systemd claims in `now` were independently verified against freshly fetched upstream
bytes. The only caveat is structural: the marker's primary support rests on upstream files the
wave admits it did not register, so the only M6-resolvable basis is the lane's own correction
note. Findings below.

## Findings

1. **(a) Original statement unchanged in place — holds [obs].**
   SH3 `statement` ends "... scrub does not verify it; systemd sets that attribute on journal
   files by default." The anchor is a verbatim substring exactly once (grep count 1). The
   sha256 of the `statement` field is `de10215a6992a2e8422b554b1c7af5ebad6e1d9f91d54290fef5653a1c7c0da0`
   at both the claim base `16e9ab2a` and tip `10d5288`, matching BASE_DIGEST['O10'] in
   tools/check-owed-statements-r29.py:98. `git diff 16e9ab2a..10d5288` removes zero lines
   containing the anchor. Marker id `R29-OWED-O10` appears in exactly one target file.

2. **(b) Verdict "corrected" is right — holds [obs].**
   The withdrawn clause was literally true of systemd ≤219 (NEWS line 18788, under
   "CHANGES WITH 219": "journald now sets the special FS_NOCOW file flag for its journal files")
   and the stale claim came in via the row's own doc source — S139 line 35
   (.ufo/waves/round-26/sources/S139.rst:35) reads "systemd sets +C on journals by default",
   citing the pre-v220 commit 11689d2a. For installed systemd 262 (host: `systemctl --version`
   → "systemd 262 (262-1-arch)") both halves of the statement are wrong in mechanism: new
   journal files get NOCOW by directory inheritance, and archived files get it removed.
   Wrong mechanism = "corrected", not "rebutted" (the NOCOW default outcome persists for
   active files) and not "qualified" (the claim is not narrowed but refuted as stated).

3. **(c-1) Basis `corpus/knowledge/storage-health-r26.md:135` — resolves and supports [obs].**
   Line 135 exists, is the "- SH3, late wave-2 corrections (RevRowSH3)" bullet, and restates
   the same claims (tmpfiles snippet since 220, cleared/rewritten on archive). Counter run at
   tip: `{"id": "O10", "ok": true}` with basis paths
   `["corpus/knowledge/storage-health-r26.md:135"]`; last line `marked: 12`.

4. **(c-2) Unregistered systemd sources — claims verified against live upstream [obs].**
   The second basis string says v262 NEWS and `src/shared/journal-file-util.c` "are not
   registered in corpus/SOURCES.md, so no S id exists for this claim". Grep of SOURCES.md
   finds no journal-file-util or journal-nocow row; S024 (systemd NEWS, status `queued`,
   used-by `—`, scope 258–262 changes) could not satisfy M6 anyway, so the note is accurate
   [obs]. I fetched the cited bytes:
   - `https://raw.githubusercontent.com/systemd/systemd/v262/tmpfiles.d/journal-nocow.conf`
     sha256 `b0cfe7fb…`; lines 25–27 set `h /var/log/journal{,/%m,/remote} - - - - +C` and
     line 11 states the flag "is inherited by their new files and sub-directories" — directly
     supporting "applied to the journal directories, so active journal files inherit it".
     Identical (two comment-typo diffs) at tag v220, sha256 `b44c95c0…`.
   - `https://raw.githubusercontent.com/systemd/systemd/v262/NEWS` sha256 `a494f038…`;
     lines 18604–18607 under `CHANGES WITH 220` (header line 18424): "systemd-journald will
     no longer unconditionally set the" "btrfs NOCOW flag on new journal files. This is
     instead done / with tmpfiles snippet ... journal-nocow.conf". Recomputes "since systemd 220" ✓.
   - `src/shared/journal-file-util.c` v262 sha256 `1532b899…`; lines 201–206 comment "first try
     to re-enable COW on the file. If the FS_NOCOW_FL flag ... cannot be removed ... rewrite the
     file without the NOCOW flag" and code lines 208–224 (`chattr_fd(f->fd, 0, FS_NOCOW_FL)`
     then `copy_file_atomic_at_full` fallback) — exactly "clears it, or rewrites a file
     without it, when the file is archived". NEWS line 10424 ("re-enables COW for archived
     journal files") sits under `CHANGES WITH 250` (header line 9634), so the behavior
     predates but is present in v262 — "systemd v262 clears it" is accurate [obs].

5. **Residual risk / gap [inf].** M6 is satisfied only by the lane's own wave-2 note
   (md:135); the primary upstream evidence backing the correction is declared-but-unregistered
   (no S### row, no snapshot in .ufo/waves/round-29/w1/ — the w1 dir holds seat reports, not
   source bytes). The marker therefore passes the counter while its load-bearing citations
   are self-described rather than registry-checkable. Verifying this marker required fetching
   upstream myself (done above); a future lane reader cannot re-resolve the basis without
   repeating that fetch. Not a falsification — an auditability gap worth a follow-up SOURCES
   row if the round allows one.
   Numbers recomputed: "220" ✓ (NEWS CHANGES WITH 220 + file exists at tag v220); "v262" ✓
   (code present at tag v262; feature since v250). No other numerals in `now`.

Scope: read=storage-health-r26.json (O10 marker + SH3 row), storage-health-r26.md:135,
check-owed-statements-r29.py docstring/BASE_DIGEST, SOURCES.md (systemd/journal/S024/S139
rows), S139.rst:35, upstream journal-nocow.conf@v220/v262, NEWS@v262,
journal-file-util.c@v262; wrote=.ufo/waves/round-29/w2/RevMarkerO10.md and fetched bytes
under .ufo/waves/round-29/w2/RevMarkerO10/ (sha256 above); executed=
`python3 tools/check-owed-statements-r29.py --revision 10d5288…` (marked 12, O10 ok),
read-only git diff/show, curl -sL fetches, grep -cF verbatim checks.
Model: devin/swe-2
Installs: none
