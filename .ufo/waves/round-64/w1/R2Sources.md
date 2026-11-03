# R2Sources — w1 report (C3-SOURCES-ATTACK)
2026-11-03T19:06:15Z

Seat: R2Sources (reviewer, tsukuroi r64 w1). Full receipts: `.ufo/waves/round-64/after/review-sources.md` (base review + addendum). Lane writes: that file only. Scratch `/fast/scratch/hyaku/tsukuroi-r64/R2Sources/` deleted before yield; every citable byte is embedded in the review file. No tools installed.

## Headline
S279 **ADMIT**. S280, S281 **ADMIT conditional on one 12-byte wording fix each** (strip the `opens: ` prefix from the teaches cells so they open `supersedes S021 - ` / `supersedes S022 - ` per the contract letter and the registry's own 19-row house pattern; census-neutral either way). No REJECT findings. The draft landed at ~19:02-19:03Z, just inside my window; all verdicts are against the real rows, verified end-to-end.

## Verification legs (all with `$ command` + output + rc in the review file)
1. **Live re-opens (independent, pre-draft)**: release v42.2 API (http 200, released_at `2026-10-01T07:10:00.872Z`, CHANGES WITH v42.2 body captured; every scope entity byte-present; U+00A0 inside "Aidan Dang" documented as a quote trap); btrfs-overlayfs hook (line 4 `root_mnt="/new_root"` exact; latest upstream commit = S021's pin `3c011dc`, so master is unchanged since the pin); plymouth hook (line 11 `plymouth update-root-fs --new-root-dir=/new_root` exact; latest commit = S022's pin `df08850`).
2. **Host byte-identity (teaches claims proven true)**: fetched master hook ≡ installed `/usr/lib/initcpio/hooks/btrfs-overlayfs` (cmp rc 0, sha256 `eeac1ed3…`), owner `limine-mkinitcpio-hook 1.40.0-2`; fetched plymouth hook ≡ installed `/usr/lib/initcpio/hooks/plymouth` (cmp rc 0, sha256 `de852646…`), owner `plymouth 26.134.222-3`. Scribe's independent fetches hash-identical to mine.
3. **Registry shape**: all three rows NF==13 (11 cells), ids S279-S281 free (S278 last row, line 287), tier A with docs/code, statuses/dates/recheck/used-by exact, used-by path = frozen C3 predicate (`LOG.md:2762`, `SCORECARD.md:4717`).
4. **Gate quotes**: all 9 quotes ≤ 25 words by `printf '%s' "<q>" | wc -w`; hook quotes strict byte-matches at the cited lines (4/6/21/11/10); the four S279 release-body quotes byte-present modulo the source's own markdown line-wrap (disclosed by the scribe; normalized match = 1 each). Minor receipt flag: the gate block's "offsets 57/191/289" don't reproduce (I measure 163/241/334 under whitespace-run normalization) — verbatim-ness itself verified.
5. **Duplicate-URL / census**: E04 exemption mechanics proven live with synthetic probes (same-URL-same-scope without the token → E04 rc 1; with `supersedes S0NN` → suppressed; scope text compared byte-exactly). Census on the real rows in a post-C1 CR-stripped mirror: **rc 0, zero E-codes, 44 W04** (42 baseline + S280 + S281), S279→S281 directly after S278. Without the MK note present: exactly 3 E11 — the note must land with-or-before the final census receipt. S279's API URL is new to the registry (no W04); S053/S054/S058/S098/S111 adjacencies disclosed (contract-blessed, no census code).

## Flags for the L1 (nothing blocks)
- **Required fix**: strip `opens: ` from S280/S281 teaches cells (house style opens `supersedes S0NN —`; `grep -c 'opens:' corpus/SOURCES.md` = 0 today). Census-neutral; contract-letter-restoring. Scribe self-flagged the same in draft schema note #3.
- **Predicate restatement**: frozen C1 text says "the 42 W04 … reappear"; post-landing truth is 44 (exit-0 and zero-E halves unaffected). Restate in the round receipt.
- **Paste discipline**: the draft also contains NF=6 summary-table rows mentioning S279-S281 — paste ONLY the three fenced ```text rows.
- **Landing order**: CR-strip (E1) → rows after S278 → prefix strip → MK note with-or-before → census expect rc 0 / 0 E / 44 W04.
- Cross-note honored: SC2Census's CRLF re-materialization (worktree SOURCES.md back to HEAD CRLF bytes at 18:47:32Z) — my fixture CR-strips before census so results model the post-C1 state; acknowledged to the peer; repair belongs to E1LineEnd.
- Residual risk (disclosure): S279-S281 carry different meanings (man7 errno(3)) in the never-adopted round-37/38/39 staged-id quarantine artifacts; registry is authoritative; a disclosure line in the round log would prevent future cross-wiring.

## Tooling record
No installs/updates (system binaries only: curl, awk, gawk via the fleet census, python3, coreutils, sha256sum) — operator tooling directive satisfied by non-use.
