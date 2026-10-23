# W2QuoteHash — re-open of S191/S194 quotes and line pointers, C2 draft (round 35 w2)

Verdict: VERIFIED — all 11 in-scope quotes are verbatim at their cited lines and every sentence states exactly what its source states (branches kept, no added "only"); one minor code-branch pointer truncation, zero fabricated, misplaced or overstated quotes.

Scope: the upgrade hash-decision table, the sentence pair around it, and the NoUpgrade paragraph of `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ScribeC2Draft/pacman-backup-files-r35.md`, checked against S191 `lib/libalpm/add.c` and S194 `doc/pacman.8.asciidoc` at pacman 54d9411, plus the S195 sentence inside the NoUpgrade paragraph. Source bytes re-fetched 2026-10-23 from `https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/...`; all verification below cites `.../w2/W2QuoteHash/src/` (my fetch) — byte-identical to the snapshots (finding 10).

## Provenance [obs]

1. Fresh fetches: `src/add.c` sha256 `fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1` (695 lines), `src/pacman.8.asciidoc` `bf1569d62f74c1f380565ab55c4f8edb07d6d59ae3e5de3b79847ac6f520ee3b` (595 lines), `src/pacman.conf.5.asciidoc` `c8e659b15d77133699ac541cfdc162d66ae5580bad5996ee30149f76671fff8f`. All three equal the wave-1 snapshots (`w1/SrcAddC/add.c`, `w1/SrcPacmanDocs/pacman.8.asciidoc`, `w1/SrcPacmanDocs/pacman.conf.5.asciidoc`) and the ScribeC2Draft copies (`w1/ScribeC2Draft/S191-add.c`, `S194-pacman.8.asciidoc`, `S195-pacman.conf.5.asciidoc`) and the copies inside `w1/ScribeC2Draft/pacman-54d9411/` (`doc/pacman.8.asciidoc`, `lib/libalpm/add.c`) — same hashes everywhere. So cited line numbers mean the same lines in every copy.
2. Bonus, cheap check: the draft's declared supplemental-NEWS hash `30c0da27238efffb96b4fe27fcf512b2f7194f40cef4c6350681821af8d94bed` matches `w1/ScribeC2Draft/pacman-NEWS-54d9411` exactly [obs].

## Hash-decision table quotes (S194, verbatim + support)

All checks byte-level with whitespace normalized (source prose is line-wrapped; tab-indent only in add.c). Method: whitespace-joined cited span must contain the whitespace-joined quote; 11/11 PASS.

3. [obs] Preamble "Pacman 7.1's manual names all three (S194, `Handling Config Files`, lines 529–534)" — verbatim YES: the three-hash sentence ("one for the original file installed, one for the new file ... one for the actual file existing on the file system") sits at `pacman.8.asciidoc:530-533`, inside the cited 529–534. Sentence support exact.
4. [obs] Row X/X/X — verbatim YES at `pacman.8.asciidoc:537` ("All three files are the same, so overwrites are not an issue."), inside cited 536–538. Outcome sentence "Install new file over current; no `.pacnew`" matches manual plus code (rename path, no pacnew event).
5. [obs] Row X/X/Y — verbatim YES at `pacman.8.asciidoc:542-543`, inside cited 540–543.
6. [obs] Row X/Y/X — verbatim YES at `pacman.8.asciidoc:546-547`, inside cited 545–547. The added clause "discard staged new copy when newly staged" is code-true, not an overstatement of the manual: `add.c:378-379` unlinks the extracted file only `if(isnewfile)`, i.e. exactly when newly staged.
7. [obs] Row X/Y/Y — verbatim YES at `pacman.8.asciidoc:550`, inside cited 549–550.
8. [obs] Row X/Y/Z — verbatim YES at `pacman.8.asciidoc:553-554`, inside cited 552–555.
9. [obs] Row NULL/Y/Z — both fragments verbatim inside cited 557–560: "package was not previously installed" at `pacman.8.asciidoc:558` (draft drops the leading "The", a clean mid-sentence fragment) and "Install the new file with a '.pacnew' extension and warn the user." spanning `pacman.8.asciidoc:559-560`. The row's "first install or retroactively designated backup" is grounded in the two citations it gives: `add.c:306-309` (oldpkg path leaves `hash_orig` NULL) and `add.c:310-313` (retroactive path). Not overstated.

## add.c pointers (S191)

10. [obs] Order sentence "compares current/new first, then original/new, then original/current (S191 lines 357–404)": branch conditions at `add.c:365` (hash_local vs hash_pkg), `add.c:373` (hash_orig vs hash_pkg), `add.c:381` (hash_orig vs hash_local) — order claim exact; all inside the cited span (357–364 are declarations plus the `checking hashes`/`current:`/`new:`/`original:` debug prints, `add.c:360-363`). Containment accurate; the comparisons strictly begin at 365, not 357 — no defect.
11. FINDING (minor, pointer truncation): row X/X/X cites "Code branch S191:365–370", but branch 1 (`hash_local == hash_pkg`) spans `add.c:365-372` (condition, comment, debug log, `try_rename` 370, `errors++` 371, close 372). The cited span starts at the right condition and stays inside the right branch, so it is not misplaced, but it stops mid-branch and omits the closing two lines; the X/Y/Y row cites the very same branch with the full 365–372. Evidence: `src/add.c:365-372`. Fix: cite 365–372 in both rows.
12. [obs] X/X/Y → "Code S191:381–388" is exactly branch 3 (`add.c:381` condition through close at 388, `} else {` at 389). X/Y/X → "Code S191:373–380" is exactly branch 2 (373–380). X/Y/Y → "Code S191:365–372" is exactly branch 1. All three mappings semantically correct (original==current installs new; original==new leaves local and unlinks a newly staged copy; current==new installs new).
13. [obs] Log artifact column "warning: <path> installed as <path>.pacnew (S191:403–404)" — `add.c:403-404` is `alpm_logaction(... "warning: %s installed as %s\n", origfile, filename)` where `filename` is `origfile` + appended `".pacnew"` (`add.c:345`). The rendered runtime string is exactly the draft's artifact rendering; the draft labels it a pacman.log artifact line, not a verbatim source quote, so the `%s` form is correctly presented.
14. [obs] Post-table sentence "The first four cases take debug-log branches; the warning `alpm_logaction` for hash-based `.pacnew` creation is the final branch (S191:365–404)": DEBUG `action:` lines exist for all four cases (`add.c:368`, `376-377`, `384`, `399-401`); the `alpm_logaction` warning is at `add.c:403-404` inside the final `else` (389–405); all inside the cited span. Exact.

## NoUpgrade paragraph

15. [obs] "add.c emits the `.pacnew` warning (S191:301–314, 338–350)": `add.c:303-304` sets `notouch` on `noupgrade` fnmatch inside case 3 (301–314); `add.c:338-350` is the notouch branch ending in `alpm_logaction(... "warning: %s installed as %s.pacnew\n", filename, filename)` at 349–350. The sentence ("matching archive paths are not touched, the package version becomes `.pacnew`, and add.c emits the `.pacnew` warning") states exactly what the code does — the needbackup/hash path is never entered when `notouch` is set, so "bypasses the hash decision" is accurate.
16. [obs] S195 quotes, span 135–138: "files listed with a `NoUpgrade` directive will never be touched during a package install/upgrade" is verbatim at `pacman.conf.5.asciidoc:136-137` (draft drops the leading "All" — clean fragment), and "new files will be installed with a '.pacnew' extension." is verbatim at `pacman.conf.5.asciidoc:137-138` (drops leading "and the" — clean fragment). Both inside the cited 135–138; no added exclusivity, no dropped branch (the source's one sentence is fully covered by the two fragments combined).

## QUALITY 66 check (branches kept, no added "only") [obs]

17. No in-scope sentence adds "only"/exclusivity absent from its source. The two outcome clauses that go beyond their manual quote ("no `.pacnew`" in rows X/X/X and X/X/Y; "discard staged new copy when newly staged" in X/Y/X) are each code-grounded in the same table cell's cited branch (`add.c:365-372`, `381-388`, `373-380` respectively) and are true of that code. No manual branch is dropped: all six scenario rows of `pacman.8.asciidoc:536-561` appear in the draft table.

## Residual risk and verification gaps

- [unk] S192 `remove.c`, S193 `pacdiff.sh.in`, and the S010/S011 wiki quotes are outside this seat's scope. I hashed the wave-1 snapshots (`w1/SrcRemoveC/remove.c` `a052d455f088f34bf1d713a434957de7e1b9322862a07b69160c65ee15dca314`, `w1/SrcPacdiff/pacdiff-v1.13.1.sh.in` `f65e626da3d4c6d30c9fda8efcfa5ef64d790c902890de62b9b7f4a71056d309`) but did not fetch those bytes from the network, so their upstream equality is unverified here (owned by W2QuoteRemove / W2QuotePacdiff).
- [obs] Verbatim comparison normalized whitespace only; punctuation, quotes ('.pacnew'), backticks (`NoUpgrade`), and word content compared exactly. No other normalization applied.
- No fabricated, misplaced, or overstated quote found; the single actionable item is finding 11 (cite 365–372 for the X/X/X row).

Scope: read=w1/ScribeC2Draft/pacman-backup-files-r35.md, w1/Src*/ source snapshots, w1/ScribeC2Draft source copies; wrote=.ufo/waves/round-35/w2/W2QuoteHash.md, .ufo/waves/round-35/w2/W2QuoteHash/src/{add.c,pacman.8.asciidoc,pacman.conf.5.asciidoc}; executed=curl fetch of 3 pinned URLs + sha256sum/cmp snapshot comparisons + grep/read line verification (no lane repo writes, no git/jj commands)
Model: zai/glm-5.3-flash
Installs: none
