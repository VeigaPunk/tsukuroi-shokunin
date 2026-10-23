# W2RevSourceRows — review of drafted SOURCES rows S191–S195 and the need for S196

Verdict: S191 pass with a used-by precision fix; S194 and S195 pass as drafted; S192 FAILS the
registry census as drafted (status `candidate` is not an enum value); S193 FAILS as drafted
(`mined` with a used-by path that does not exist); S196 is NEEDED if the C2 note's `.pacorig`
claims are admitted, and it duplicates neither S006 nor any other row by URL or bytes. The full
hash resolves to `54d94116164b0b2202c6061c4a59c6f3e70820d8` and all six pinned byte fetches are
sha256-identical to the seat snapshots.

## Cell-by-cell results

All five draft rows: exactly 11 cells (awk NF=13 over each row line — printed 11 for each), no
`|` inside cells, ids S191–S195 are the next unused (registry `corpus/SOURCES.md` has 190 rows
ending at S190), `kind` in enum (code/code/code/docs/docs), `tier` A with row-scoped `scope`
(none community), `anchor` carries revision plus line numbers in every row, `opened` 2026-10-23
(ISO), `recheck` `on-release`. Per-row verdicts on the two cells that differ:

| row | status cell | used-by cell | verdict |
|---|---|---|---|
| S191 | mined | tools/score-pacnew-arm-r35.py | pass with finding 3 |
| S192 | candidate | tools/score-pacnew-arm-r35.py | FAIL — finding 1 |
| S193 | mined | corpus/knowledge/pacman-backup-files-r35.md, tools/score-pacnew-arm-r35.py | FAIL — finding 2 |
| S194 | queued | — | pass |
| S195 | queued | — | pass |

## Numbered findings

1. **S192 status `candidate` is an enum violation.** The frozen contract allows only
   `queued|mined|rejected`; the CORPUS.md census (`status !~ /^(queued|mined|rejected)$/`)
   prints `status S192` for this row. Evidence: draft line 5, ninth cell
   (`.ufo/waves/round-35/w1/SrcRemoveC/S192-draft.md:5`); contract at
   `/home/vgpnk/Projects/shokunin/CORPUS.md:141`. The draft's own prose describes the state the
   enum calls `queued` (opened, nothing cites it yet). Fix: `queued`.

2. **S193 is `mined` citing a used-by path that does not exist.**
   `ls corpus/knowledge/pacman-backup-files-r35.md` → "No such file or directory" (exit 2); the
   note is still the seat draft `.ufo/waves/round-35/w1/ScribeC2Draft/pacman-backup-files-r35.md`.
   The census check "mined rows whose used-by paths do not exist — must print nothing" prints
   `missing: corpus/knowledge/pacman-backup-files-r35.md`. Evidence:
   `.ufo/waves/round-35/w1/SrcPacdiff/S193-row.md:1` (ninth and eleventh cells); contract at
   `/home/vgpnk/Projects/shokunin/CORPUS.md:147`. Fix: land the note and the row in the same
   landing, or draft the row as `queued` with used-by `—` until then.

3. **S191's used-by names the artifact that does not cite it by id.** The v1 counter's docstring
   names the source files only ("pacman 7.1.0 libalpm add.c / remove.c log formats … rows
   registered in corpus/SOURCES.md this round", `tools/score-pacnew-arm-r35.py:15-17`, no row
   ids); the artifact that cites S191 by id is the v2 counter ("rows S191-S195 registered this
   round", `tools/score-pacnew-arm-r35b.py:23-24`). Registry precedent S146 shows the accepted
   shape: tool paths plus a corpus/lessons path
   (`corpus/SOURCES.md:152`, used-by `tools/mutants-adjacency-overlap.py,
   tools/mutants-kernel-taint.py, corpus/lessons/round-28.md`). Recommendation: S191's used-by
   should name `tools/score-pacnew-arm-r35b.py` (and the knowledge note at landing), or drop to
   `queued`/`—` until something that names S191 lands. Same point applies to S192's used-by cell.

4. **Hash-pin inconsistency, now resolvable.** S191 pins the full commit everywhere; S192, S194
   and S195 pin the short ref `54d9411` in URL and anchor. GitLab commit API (read-only, curl)
   resolves `54d9411` → `54d94116164b0b2202c6061c4a59c6f3e70820d8` (created
   2026-01-07T21:33:46.000+10:00, "libmakepkg: fix linting of xdata"). Short refs are accepted
   registry practice (S099, `corpus/SOURCES.md:105`), so this is minor; recommend uniform
   full-hash pins now that the expansion is known.

5. **Byte verification passes for all five rows and for S196's candidate bytes.** Re-fetching
   each pinned URL today (curl, GitLab raw) reproduces the seat snapshots and every anchor's
   recorded digest exactly: add.c `fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1`,
   remove.c `a052d455f088f34bf1d713a434957de7e1b9322862a07b69160c65ee15dca314`,
   pacdiff.sh.in `f65e626da3d4c6d30c9fda8efcfa5ef64d790c902890de62b9b7f4a71056d309`,
   pacman.8.asciidoc `bf1569d62f74c1f380565ab55c4f8edb07d6d59ae3e5de3b79847ac6f520ee3b`,
   pacman.conf.5.asciidoc `c8e659b15d77133699ac541cfdc162d66ae5580bad5996ee30149f76671fff8f`,
   NEWS-at-54d9411 `30c0da27238efffb96b4fe27fcf512b2f7194f40cef4c6350681821af8d94bed`.
   Re-fetched copies with these digests are at
   `/fast/scratch/hyaku/tsukuroi-r35/W2RevSourceRows/`. This is the contract's non-author
   verification re-open (CORPUS.md rule 1), done for all six objects, not a sample. Line-count
   claims in the anchors also check out (add.c 695 lines, remove.c 798 lines, wc -l).

6. **Quote verification passes.** Every located quote is an exact substring at its claimed
   location and ≤25 words: add.c `noupgrade`/`notouch` at 303-304, `.pacnew` warning in the
   notouch branch (~350), hash branches at 365/373/381 and warnings at 399-404
   (`.ufo/waves/round-35/w1/SrcAddC/add.c` reads 300-405); remove.c lines 400, 533, 536, 548,
   560 match the draft's list (reads 398-402, 531-538, 546-550, 558-562); pacdiff anchors
   84-91, 224-245, 327-331 all contain what the row claims (reads 84-91, 222-247, 325-333);
   pacman.8 `-R, --remove` at 50-56, "Handling Config Files" heading at line 527 (grep -n),
   quotes at 54-55, 552-554, 558-559; pacman.conf.5 NoUpgrade 135-144, NoExtract 146-157,
   quotes at 137-138 and 147-148. Largest quote is S194's third at 24 words. All grounded for
   their `teaches` cells; S192's teaches correctly states the `cmp != 0` gate and the missing
   success-path logcall for shifted saves.

7. **No duplicates by URL or bytes.** Registry sweep (grep over `corpus/SOURCES.md`): no S-row
   carries any of the five row URLs; none of the six digests appears anywhere; the only
   `54d9411` match is S099 (dload.c — same commit, different file). Near-family rows are not
   duplicates: S006 is NEWS at `master` (different URL, unpin), S007 is pacman.conf(5) rendered
   at man.archlinux.org, S048/S049/S089/S090/S106/S107 are rendered pacman(8) pages — different
   URLs and different bytes from the pinned asciidoc sources.

8. **S196 is needed — conditionally on admitting the C2 note's `.pacorig` claims.** The note
   grounds "[inf] Pacman 7.1 no longer makes `.pacorig`" on NEWS:527 and its own QUALITY items 2
   and 7 say the supplemental NEWS object "must be registered before its claim is admitted";
   CORPUS.md requires an admitted knowledge entry's `source:` to cite its `S###` row with URL
   and anchor (`CORPUS.md:164-166`). Both line pins verify: `5.0.0` heading at NEWS line 510,
   `.pacorig` bullet at line 527 (grep -n), quote "Remove support for ".pacorig" files.
   Instead, packages files are extracted as a ".pacnew" and the original stays in place" = 19
   words. S196 is not a duplicate of S006: different URL (pinned 54d9411 vs master), different
   bytes (master today hashes `688783f987e29be109142e08d93382c54aadd19c30cdcf3a13244fef69a3b8b4`
   ≠ `30c0da27…`), different scope (S006 covers the 7.0/7.1 signature and downloader sections),
   and S006's own anchor concedes its bytes are unreproducible, so its 2026-10-19 fetch cannot
   collide byte-wise either. Recommended shape: kind `docs` (S006 convention), tier A scoped to
   "pacman ≥ 5.0.0 no longer creates `.pacorig`; package files land as `.pacnew` and the
   original stays in place", anchor "commit 54d94116164b0b2202c6061c4a59c6f3e70820d8; 5.0.0
   entry lines 510-528, quote at line 527; sha256 30c0da27…; snapshot
   `.ufo/waves/round-35/w1/ScribeC2Draft/pacman-NEWS-54d9411`", status `queued`/used-by `—`
   until the note lands (then `mined` with the note path). This is a new scoped row, not a
   `supersedes S006` correction — S006's claims are untouched.

9. **Minor wording, S193 teaches.** "Find and locate match `.pacorig` and `.pacsave.N`" means
   the find(1)/locate(1) modes but reads as a sentence fragment; suggest "The find and locate
   modes match …". Also, S193's one-line draft file carries no located-quotes section of its
   own (its gate quote lives in the C2 note at `S193:327-330`, verified at lines 327-331);
   the other four drafts each carry their own quotes.

10. **Landing-order constraint.** Per contract rule 1 the round lesson's `## Gate` must record
    URL, access date and located quote per new row — all five drafts already carry that
    material, so the gate can be filled at landing. The census-failing states in findings 1-2
    must not be merged: either the note lands in the same commit set as S191-S195 (making the
    mined statuses and the note-path used-by true), or the rows land as `queued` with `—`.

## Residual risk and verification gaps

- S006's exact 2026-10-19 master bytes were never saved, so the S006/S196 byte-difference is
  proven against today's master only; S006's own anchor already declares non-reproducibility,
  which closes the practical duplication risk [unk, bounded].
- The awk/enum checks were applied directly to the draft row lines; the maintained
  `scripts/sources-census.sh` was not run because none of these rows is in
  `corpus/SOURCES.md` yet (registry verified still to end at S190).
- Snapshot-to-URL byte identity was verified at fetch time today; GitLab raw responses could
  in principle differ for future fetchers at the same short ref only if the ref were reused,
  which a 40-char pin (finding 4's recommendation) removes.

Scope: read=lane registry corpus/SOURCES.md (190 rows, S006/S009/S099/S146 raw), CORPUS.md:64-152, four w1 seat drafts + five snapshots + C2 note + NEWS snapshot, both counter docstrings; wrote=.ufo/waves/round-35/w2/W2RevSourceRows.md, /fast/scratch/hyaku/tsukuroi-r35/W2RevSourceRows/{add.c,remove.c,NEWS,NEWS-master,pacman.8.asciidoc,pacman.conf.5.asciidoc,pacdiff.sh.in}; executed=curl GitLab commit API + 7 raw fetches (read-only), sha256sum, awk census/enum checks, wc/grep line pins, cp+rm (a first fetch landed in /tmp/w2revsrc outside seat bounds and was moved to the sanctioned scratch dir and deleted there)
Model: not exposed
Installs: none
