VERDICT: draft

Sources verdict: both rows support the claim they carry — S256 (grep(1)) was fetched live twice on 2026-10-28 and its
bytes match the row's pin; S240 (`fs/btrfs/ioctl.c` at v7.2.11) was fetched live twice on 2026-10-28 and its bytes are
byte-identical to the pin and to the round-43 snapshot. The `## Gate` text below is ready to paste. Four cells of
S256 need repair before that text is accurate about the row (R1-R4); S240 needs one declared-range widening (R5) that
the entry's `Limits` already discloses.

Lane bytes were read only with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8029cdba…`; no lane file
was written. No tool was installed. Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50ScribeSourcesGate/` removed after
the receipts were copied to `.ufo/waves/round-50/w1/R50ScribeSourcesGate/`.

## 1. Draft — `## Gate` block (round-49 shape, paste-ready)

Shape copied from `git show 8029cdba:corpus/lessons/round-49.md` § Gate (paragraph, then
`| Row | Opened | Evidence | Change |`), and the trailing wave-re-open paragraph it also carries.

```markdown
## Gate

Rows touched by using them in this round's claims. `## Gate` records the URL, access date and a ≤25-word located
quote for every row opened here; a `used-by` change is logged old → new.

| Row | Opened | Evidence | Change |
|---|---|---|---|
| S256 | GNU grep(1) manual page — https://man7.org/linux/man-pages/man1/grep.1.html | Opened by wave seat `R50ScoutGrepSource` on 2026-10-28 and re-fetched by seat `R50ScribeSourcesGate` the same day (`HTTP/1.1 200`, `Date: Wed, 28 Oct 2026 19:14:28 GMT`, 43199 bytes); fetched bytes sha256 `d6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2`, identical to the row's recorded digest; footer `GNU grep 3.12.39-8017d-modified 2025-03-21` (raw HTML line 711); located quote (raw HTML lines 202-204): "Exit immediately with zero status if any match is found, even if an error was detected"; the EXIT STATUS section repeats it for `-q` at lines 483-486. | `status` absent → `mined`; `recheck` `on-release`; `used-by` `—` → `corpus/lessons/round-50.md` (new row, `docs` tier A): C2 (`tools/check-selftest-matcher-r50.py`, the `(R50-C2)` case and the `buf_has`/`out_has` full-read matcher). |
| S240 | Linux v7.2.11 fs/btrfs/ioctl.c — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11 | Re-opened by wave seat `R50ScoutReopenS240` on 2026-10-28 and re-fetched by seat `R50ScribeSourcesGate` the same day (145999 bytes, 5678 lines); fetched bytes sha256 `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01`, byte-identical to the row's pin and to `.ufo/waves/round-43/frozen/src/ioctl.c`; tag v7.2.11 peels to `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`, the row's anchor. Located quote (source line 3132, the row's taught proposition): "if (!capable(CAP_SYS_ADMIN))"; GR2's five cites sit at `:3093-3095`, `:3109-3110`, `:3115`, `:3132-3133` and `:3190`. | `status` `mined` → `mined`; `recheck` `on-release` → `on-release` (no change); `used-by` `corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/lessons/round-48.md` → that list plus `corpus/knowledge/btrfs-scrub-grounding-r45.md` (C1's GR2 correction names the row). |

Refused this round: the staged `merge/tsukuroi` package (`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/`, staged by
`corpus-expansion-1`, 147 rows starting at `S200`) is **not adopted** — 57 of its ids (`S200`-`S256`) collide with the
lane registry's 256 ids, so appending would duplicate live ids instead of extending the S-space, and the collision
reaches rows the round cites by id (`S237`-`S249` on C1's `source:` line, `S240` above). Flip condition: the package is
renumbered above the lane's high-water mark (`S257` onward) in scratch, and the adopting round records a `## Gate` row
for every id it admits (QUALITY 61).

Rows re-opened by wave seats (byte-equality and located anchors recorded by each seat's report): S240, S242, S243,
S247 — in the seats' reports under `.ufo/waves/round-50/w1/`.
```

## 2. Row check

### 2.1 Evidence base

- S256 row at the freeze: `git show 8029cdba:corpus/SOURCES.md | sed -n 265p`, 11 schema cells (header line 5), no
  column shift. Tier `docs`, status `mined`, `opened` `2026-10-28`, `recheck` `on-release`,
  `used-by` `corpus/lessons/round-50.md`.
- Live page: `curl -sS -D hdr2.txt -o grep1b.html https://man7.org/linux/man-pages/man1/grep.1.html` (2026-10-28) →
  `HTTP/1.1 200`, `Date: Wed, 28 Oct 2026 19:14:28 GMT`, `Last-Modified: Wed, 28 Oct 2026 18:28:41 GMT`,
  `Content-Length: 43199`; `sha256sum grep1b.html` = `d6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2`.
  Receipt `R50ScribeSourcesGate/grep1b.html` + `hdr2.txt`. The independent scout fetch (19:04:05 GMT, same 43199
  bytes, same digest) is `R50ScoutGrepSource.md` § (a).
- Quote location on that body: `202` `Quiet; do not write anything to standard output.  Exit` / `203`
  `immediately with zero status if any match is found, even if` / `204` `an error was detected.  Also see the …`
  (the `-q` block is 201-205); EXIT STATUS heading `482`, paragraph `483-486`, `487` is `</pre>`. Footer version at
  line `711`. Case-insensitive counts on the same 43199 bytes: `SIGPIPE` 0, `pipeline` 0, `pipefail` 0, `broken pipe`
  0; `first` 0 inside the two cited spans, 7 elsewhere on the page.
- S240 row at the freeze: `corpus/SOURCES.md:249`, 11 cells. Anchor `raw bytes sha256
  7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01; reopened live 2026-10-28, byte-identical`;
  scope ranges `3066-3075, 3118-3140, 5578-5584`; `used-by` `corpus/knowledge/btrfs-scrub-record-r43.md,
  corpus/knowledge/btrfs-scrub-record-r44.md, corpus/lessons/round-48.md`.
- Live S240: `curl -sS -o ioctl.live.c https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11`
  → `sha256sum` `7b3488f2…ba01`, 5678 lines; `git show 8029cdba:.ufo/waves/round-43/frozen/src/ioctl.c | sha256sum`
  = the same digest. Lines 3093-3095, 3109-3110, 3115, 3132-3133, 3190 read exactly as the scout's
  `cited-lines.txt` records. Receipt `R50ScribeSourcesGate/ioctl.live.c`.
- Package collision: lane ids `S001`-`S256` (256) vs staged ids (147); `comm -12` → 57 (`S200`-`S256`), receipt
  `R50ScribeSourcesGate/collisions.txt`; `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/MERGE-REPORT.md` header:
  "proposed rows accepted: **147**", "first staged id is **S200**".

### 2.2 Findings

| # | Row | Cell | Finding | Proposed text |
|---|---|---|---|---|
| R1 | S256 | `anchor` | **Defect.** Fetch stamp is the truncated token `page fetched 2026-10-28T` — a dangling `T` with no time; no sibling row uses that shape (S251 `2026-10-27T04:59:34Z`, S253 `2026-10-28`). | `page fetched 2026-10-28T19:14:28Z (sha256 d6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2), raw HTML lines 202-204 and 483-486` — the time is bound to the body that was hashed (`hdr2.txt` `Date` + `grep1b.html`). |
| R2 | S256 | `anchor` | **Defect (imprecision).** The cited ranges overshoot the located text: `201-205` includes the option header and the "Also see" line, the quoted sentence is `202-204`; `483-487` includes the closing `</pre>` and excludes the heading (`482`) that the range's first line would suggest. QUALITY 21 (portable locators) wants the quote's own lines. | as in R1 (`202-204 and 483-486`). |
| R3 | S256 | `scope` | **Defect (unmarked inference).** "which makes an upstream writer in a pipeline die of SIGPIPE and the pipeline read false" is not on the page (zero `SIGPIPE`/`pipeline`/`pipefail` hits), and "the first selected line" is a paraphrase (`first` occurs 0 times in either cited span — 7 times elsewhere on the page; `immediately`/`any match` at 203, `selected` at 483/485). QUALITY 19 requires the inference to be marked where it is made. | ``grep -q`` exit semantics: the page states an immediate exit with zero status if any match is found, even if an error was detected (raw HTML 202-204), and EXIT STATUS states that with `-q` the status is 0 when a line is selected even if an error occurred (483-486). "First selected line" is a paraphrase of `immediately`/`any match`; that the early exit can make an upstream writer in a pipeline die of SIGPIPE, and the pipeline read false, is `[inference: POSIX pipe semantics, not a statement of this page]`. |
| R4 | S256 | `used-by` | **Defect (dangling at the freeze).** `corpus/lessons/round-50.md` does not exist in the bytes under test: `git cat-file -e 8029cdba:corpus/lessons/round-50.md` exits 128, `git ls-tree --name-only 8029cdba:corpus/lessons/` ends at `round-49.md`; the working tree has it untracked. QUALITY 61 requires the row's Gate record in that round's lesson, so the lesson must land with the Gate block above. | keep `corpus/lessons/round-50.md`, conditional on the L1 landing that file in this round. |
| R5 | S240 | `anchor` | **Declared gap, not silent.** Declared ranges cover only `:3132-3133` of GR2's five cites; `:3093-3095`, `:3109-3110`, `:3115`, `:3190` fall outside. `corpus/knowledge/btrfs-scrub-grounding-r45.md:233-235` declares exactly those four (and correctly omits 3132-3133, which the ranges do cover). Whole-file digest pins the bytes, so no claim is unsupported — but the row's own locator no longer matches the cites it carries. | widen at closeout to `fs/btrfs/ioctl.c lines 3066-3075, 3093-3115, 3118-3140, 3168-3190, 5578-5584`, then the `Limits` sentence can be narrowed to the S247 gap it already keeps. |
| R6 | S240 | `opened` | **No defect.** `reopened live 2026-10-28, byte-identical` is confirmed by two independent fetches (scout 19:04:52 GMT, this seat later the same day) and by `cmp` against the round-43 snapshot; date granularity only, which the column's other rows also use. | unchanged. |
| R7 | S256 | `recheck` | **Observation, not a defect.** `on-release` is a legal cadence (QUALITY 8) and matches S255; but S256's two closest siblings — S251 and S252, both man7.org `docs`/A — use `180d`, and this page is a mutable render (`Last-Modified` 2026-10-28T18:28:41Z, regenerated the same day the row was opened; the digest is the only pin). Consistency argument for `180d`; leave to the L1. | either is admissible. |

### 2.3 Note on the working-tree draft (read-only observation)

`corpus/lessons/round-50.md` exists untracked in the lane working tree and already carries a `## Gate — sources`
block in a **five-column** shape (`id | status change | access | located quote | note`), not the round-49 four-column
shape this item asked for, and its S256 note repeats the unmarked inference ("teaches the `-q` early exit that makes
an upstream writer in a pipeline die of SIGPIPE"), which R3 removes. Its refusal paragraph (57 collisions, 256 vs
147) matches my independent count; its cited receipt path `.ufo/waves/round-50/assimilation/collisions` exists and
lists `S200`-`S256`. I did not edit that file.

## 3. Not done

- I did not run the C1/C2/C3 counters, the census selftest, or any gate — this is a prose seat.
- I did not verify S242/S243/S247 beyond reading their seats' verdict lines (`VERDICT: supports`) and confirming the
  report files exist; their re-opens are those seats' evidence, not mine.
- I did not fetch a POSIX page, so the SIGPIPE clause carries no POSIX line number (the scout did not either).

## 4. Receipts

`.ufo/waves/round-50/w1/R50ScribeSourcesGate/`: `grep1b.html` (43199 B, sha256 `d6f07a7f…a3c2`), `hdr2.txt`
(`Date: Wed, 28 Oct 2026 19:14:28 GMT`, `Last-Modified: …18:28:41 GMT`, `ETag: "a8bf-65eeabb7aa840"`),
`ioctl.live.c` (145999 B, sha256 `7b3488f2…ba01`), `collisions.txt` (57 ids).
