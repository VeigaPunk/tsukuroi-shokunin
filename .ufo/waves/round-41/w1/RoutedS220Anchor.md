VERDICT: draft — the routed drift is real (row and round-40 Gate say `110-117`; the pinned and live PKGBUILD say `111-117`, `:110` blank), and the exact append-only text for both artifacts is in §Draft A/§Draft B. Nothing in the row's substance (scope, tier A, quote, sha256, EX4 value) changes.

# Seat RoutedS220Anchor — item R-2 (round-40 closure §6.4)

Lane tip at work: `71851d636ab1bffaf8fee5016617c88878a666f1` (`git -C … rev-parse HEAD`, 2026-10-26T18:08Z).
Read-only on lane content; no file was edited, added or deleted in the lane, no git or jj write was run, no host
command outside `curl`/`sed`/`awk`/`grep`/`sha256sum`/`cmp`/`stat` was run, no package or service was touched, nothing
was installed (operator tooling authorization unused). Scratch `/fast/scratch/hyaku/tsukuroi-r41/RoutedS220Anchor/`,
removed at the end.

## 1. The two observations the item asks to verify

1. **Row claim** — `corpus/SOURCES.md:229`: "`build()` meson call lines 110-117, `-Dscriptlet-shell` line 115;
   patch sources lines 52-55; tag 7.1.0.r9.g54d9411-3, snapshot sha256
   32d40dfd36919597b3d5b57c74d7f87ca8c463a7d10c00a87ff2149aa9ba67f4`".
   The round-40 Gate repeats the range — `corpus/lessons/round-40.md:21`: "`PKGBUILD:115 inside `build()` (meson call
   :110-117; `_git_patch_level_commit=54d9411…` :9; patch sources :52-55)`".
2. **Source** — `awk 'NR>=108 && NR<=118 {printf "%d|%s\n", NR, $0}' .ufo/waves/round-40/frozen/src/PKGBUILD`
   (receipt `RoutedS220Anchor/verify.txt`):
   `108|build() {`, `109|  cd "$pkgname"`, `110|` (blank), `111|  meson --prefix=/usr \`, `112|        --buildtype=plain \`,
   `113|        -Ddoc=enabled \`, `114|        -Ddoxygen=enabled \`, `115|        -Dscriptlet-shell=/usr/bin/bash \`,
   `116|        -Dldconfig=/usr/bin/ldconfig \`, `117|        build`, `118|` (blank).
   So the `build()` body opens at :108, the meson invocation is **:111-117**, `:110` is blank, and
   `-Dscriptlet-shell=/usr/bin/bash \` is at **:115** — the one locator in the row's anchor cell that is exact.

Both observations hold; the drift is confined to the range start (one line early, still enclosing the call, nothing
in the call outside it). Prior seats reached the same reading: `corpus/lessons/round-40-verifier-spotcheck.md:116`
("Anchor nit: the meson call is :111-117 (:110 is blank), the row and Gate say :110-117") and its §6 item 4 at
`:149-151` (the routed defect this seat closes); `.ufo/waves/round-40/w1/C2RevSourcesRows.md:150-152` and
`.ufo/waves/round-40/w1/C2ScribeGate.md:69-71` (D3) agree.

## 2. Freshness — the live tag still matches the snapshot

`curl -sS -o live2 -w 'http=%{http_code} bytes=%{size_download}\n' https://gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/raw/7.1.0.r9.g54d9411-3/PKGBUILD`
→ `http=200 bytes=4719`; `sha256sum live2` →
`32d40dfd36919597b3d5b57c74d7f87ca8c463a7d10c00a87ff2149aa9ba67f4` (equal to the S220 cell);
`cmp live2 .ufo/waves/round-40/frozen/src/PKGBUILD` → `identical`; `sha256sum -c SHA256SUMS` in the snapshot dir →
`PKGBUILD: OK`. Access date 2026-10-26 (fetch 18:08:16Z). The snapshot is not stale, and the row's `recheck:
on-release` is not due; the defect is the range text only, not the bytes it points at.

## 3. Draft A — one-line note for the round-41 lesson Gate

Insertion point: `corpus/lessons/round-41.md` (untracked in the worktree, so this lands in the round's uncommitted
lesson), `## Gate`, as a bullet immediately after the digests paragraph that ends at `:32` ("…the census reports it as
W04.") and before the blank line `:33` / `### Assimilation` `:34`. Exact text, one line:

```
- **S220 anchor correction** (round-40 closure §6.4; wave item RoutedS220Anchor): the `build()` meson call is `PKGBUILD:111-117` (`:110` blank; `sed -n 108,118p .ufo/waves/round-40/frozen/src/PKGBUILD`), not `:110-117` as the S220 anchor cell and the round-40 Gate write; the live tag re-fetch of 2026-10-26 (sha256 `32d40dfd…`, byte-identical to the snapshot) leaves the row's scope, tier, quote and EX4 value intact, so the row is unchanged (CORPUS.md rule 2) and the fix is the appended note at `corpus/knowledge/pacman-exec-environment-r40.md:117`.
```

This satisfies the disposition line already written at `corpus/lessons/round-41.md:86` ("4. S220 anchor drift: see the
appended note in this lesson's Gate (wave item RoutedS220Anchor)") — that bullet is presently a dangling pointer:
`grep -n S220 corpus/lessons/round-41.md` returns only line 86, and the Gate (`:17-32`) carries no S220 bullet.

## 4. Draft B — the appended sentence for the knowledge entry

Insertion point: end of `corpus/knowledge/pacman-exec-environment-r40.md` (append-only; the file currently ends at
`:123` with "read its range as 111-117."). Exact text:

```
## Anchor correction (appended round 41; round-40 closure §6.4)

S220's anchor cell and the round-40 Gate give the `build()` meson call as PKGBUILD lines 110-117; in the pinned snapshot, and in the live tag re-fetch of 2026-10-26 that is byte-identical to it (sha256 `32d40dfd36919597b3d5b57c74d7f87ca8c463a7d10c00a87ff2149aa9ba67f4`; `.ufo/waves/round-40/frozen/src/PKGBUILD`), `build() {` opens at :108, :110 is blank and the call spans :111-117, while `-Dscriptlet-shell=/usr/bin/bash \` stays at :115 — so read the range as 111-117; the row keeps its cells (CORPUS.md rule 2) and EX4's value and quote are unchanged.
```

Why the row is not edited and no `status`/`recheck`/`used-by` log is owed: fleet `CORPUS.md:116-118` (rule 2) —
"Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson. A
correction is a new row whose `teaches` opens `supersedes S0NN —`." The row's `status` (`mined`), `recheck`
(`on-release`) and `used-by` (`corpus/knowledge/pacman-exec-environment-r40.md`, which already cites S220) are all
correct at `corpus/SOURCES.md:229`, so nothing changes and no old→new entry arises.

## 5. Collision with the worktree (read before integrating)

`corpus/knowledge/pacman-exec-environment-r40.md` is **already modified, uncommitted** at `71851d63`
(`git status --porcelain -- corpus/` → ` M corpus/knowledge/pacman-exec-environment-r40.md`), and the diff
(`git diff -- corpus/knowledge/pacman-exec-environment-r40.md`, +8 lines, no deletions) is an "## Anchor correction
(appended round 41; round-40 closure §6.4)" block at `:117-123` written 2026-10-26T18:06:45Z (file mtime), i.e. ~90 s
before this seat's live fetch. Its every claim was verified above and is correct: :108 opens `build() {`, :110 blank,
call `:111-117`, `-Dscriptlet-shell` at :115, `sed -n 108,118p` locator, CORPUS.md rule 2 basis, "read its range as
111-117". It differs from Draft B only by carrying the abbreviated `32d40dfd…` instead of the full sha256 and by not
naming the live re-fetch.

Integration instruction: if the L1 keeps that block, **do not append Draft B on top** (it would duplicate the note);
add Draft A only. If a single sentence is preferred, replace the uncommitted block with Draft B before committing —
the block is uncommitted at `71851d63`, so replacing it rewrites no committed text. I did not write to the file (read-only
seat), so the choice is the L1's.

## 6. Findings

1. **The routed defect is confirmed and still current** at lane tip `71851d63`: `corpus/SOURCES.md:229` and
   `corpus/lessons/round-40.md:21` both say `110-117`; the pinned and live source say `111-117` with `:110` blank.
   Content (tag, sha256, quote, tier, scope, patch lines 52-55, `_git_patch_level_commit=54d94116164b…` at :9) is
   unaffected: EX4 cites `PKGBUILD:113-115` (`corpus/knowledge/pacman-exec-environment-r40.md:24`), which is exactly
   doc/doxygen/scriptlet-shell, so the scriptlet-shell line 115 is right.
2. **Rule-2 mechanics leave the row's own locator wrong.** Rule 2's only in-registry correction route is a new row
   whose `teaches` opens `supersedes S0NN —`; the round-40 disposition chose an appended note instead
   (`corpus/lessons/round-40-verifier-spotcheck.md:149-150`: "Correct by an appended note (registry rows are
   append-only except status/recheck/used-by)"). The note fixes the reading, not the cell: a reader of
   `SOURCES.md:229` alone still sees `110-117`. No supersedes row exists (`grep -n 'supersedes S220'
   corpus/SOURCES.md` → no output, exit 1). If the L1 wants the registry itself correct, rule 2 requires a new row
   (next unused id `S237`; highest at tip is `S236`, 236 rows) whose `teaches` cell opens
   `supersedes S220 — the build() meson call is lines 111-117 (line 110 blank); the rest of S220 stands`. That route
   was **not** taken here because the item prescribes the note and leaves the row alone.
3. **Other `110-117` occurrences are historical and must stay.** Sweep
   `grep -rn '110-117\|110–117' --include='*.md' --include='*.json' --include='*.jsonl' .` (excluding `.git/`) finds,
   in lane corpus text, only the four sites above — `SOURCES.md:229`, `lessons/round-40.md:21`,
   `lessons/round-40-verifier-spotcheck.md:116,149` — plus the new knowledge note's own quotation at
   `pacman-exec-environment-r40.md:119` and round-40 dispatch artefacts (`.ufo/waves/round-40/w1-spec.json:179`,
   `w1-dispatch.json:850`). The round-40 lesson and closure are append-only history and are correctly not edited; the
   Gate note is the forward record.
4. **The round-41 lesson is untracked.** `git ls-files --error-unmatch corpus/lessons/round-41.md` → "did not match
   any file(s) known to git"; `git status --porcelain -- corpus/` → `?? corpus/lessons/round-41.md`. Draft A therefore
   has no committed home yet; the note reaches the record only when the lesson is committed, so the item is not closed
   by the worktree alone.
5. **No `used-by` change is owed.** The S220 row already names `corpus/knowledge/pacman-exec-environment-r40.md` as its
   sole `used-by`; the appended note lands in that same entry.

## 7. What I did not do

- Did not edit, create or delete any lane file; did not commit; Draft A and Draft B are text only.
- Did not run `tools/check-exec-environment-r40.py` or the census; the item needs a locator check, not a counter run,
  and no counter run was started (host load, one-counter-at-a-time rule).
- Did not re-open the HTML `/-/blob/` page the row's `source` cell names; the raw tag URL is the same bytes and is the
  one the snapshot and the round-40 spot-check use (sha256 equality).
- Did not test any pacman transaction (paused host-wide).

## 8. Receipts

- `.ufo/waves/round-41/w1/RoutedS220Anchor/verify.txt` — live fetch header (URL, HTTP 200, 4719 bytes), `sha256sum`,
  `cmp` vs snapshot, numbered `:108-118` listing.
- `.ufo/waves/round-41/w1/RoutedS220Anchor/citations.txt` — `SOURCES.md:229`, `lessons/round-40.md:21`,
  `round-40-verifier-spotcheck.md:149-151`, `grep -n S220 corpus/lessons/round-41.md`, `grep -n 'supersedes S220'`
  (exit 1), `git status --porcelain -- corpus/`, file mtime, highest registry id.
