VERDICT: draft

# F-2 — Gate line for S237's re-open (round 43) and the S237 used-by Rows-touched line

Seat `SrcGateS237`, round 43 wave 1. Read-only on the lane: no lane file was created, edited or deleted; the
two blocks in §2 are seat draft text for the L1 to paste. `corpus/lessons/round-43.md` does not exist yet
(`git -C … cat-file -e 717b716a:corpus/lessons/round-43.md` → `fatal: path … does not exist`, rc 128; `ls` of the
worktree → rc 2), so the draft targets that future file, following the `## Gate` shape of
`corpus/lessons/round-42.md:16-30`.

## 1. Registry facts at the two revisions

Command (observed): `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff
6951ead90566b2d74f7c45b4efca29246badad64 717b716a8943151ace8657e0ca23d7d9b8434f26 -- corpus/SOURCES.md`
(receipt `SrcGateS237/sources-diff.txt`) — a single hunk `@@ -243,9 +243,11 @@`; `--stat` → `corpus/SOURCES.md | 4 +++-`,
`1 file changed, 3 insertions(+), 1 deletion(-)`; `--numstat` → `3	1	corpus/SOURCES.md`.

The one deleted line is old S237 (`corpus/SOURCES.md:246` at the base); the three inserted lines are new S237 plus
the two new rows S240 and S241. Cell comparison of old vs new S237 (receipt `cell-diff.txt`):

- old line 728 bytes, new line 772 bytes, common prefix 725 bytes, common suffix 3 bytes (`" |\n"`), 11 cells each.
- old tail after the common prefix: `''`; new tail: `', corpus/knowledge/btrfs-scrub-record-r43.md'` — i.e. 44 bytes
  appended inside the `used-by` cell, before the closing separator. Every other byte of the line is unchanged.
- `used-by` cell old: `corpus/knowledge/btrfs-scrub-record-r42.md`; new:
  `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md` (11 cells, `|`-split,
  receipt `usedby-replication.txt`).
- `teaches` cell (unchanged, `SOURCES.md:246` at 717b716a): "The status record is a userspace file the scrub start
  process writes and the status command reads; its format, its write discipline and the cases that leave no record".

Replication of the counter's own S237 clause at both revisions (`tools/check-scrub-record-r43.py:304-305`
`used_by(c)` splits cell 10 on `[,;]` and strips; `:313-314` requires `ENTRY in used_by(c)`): base → `ENTRY in
used_by → False`; fix → `True`. The counter itself was not run (see §6).

## 2. Proposed text (exact Markdown)

### 2a. Gate row

```markdown
### Re-opened SOURCES row (S237 re-opened 2026-10-26; quote located with `grep -n` in the pinned snapshot)

| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S237 | https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c (raw: https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c; tag v7.1 peeled 4ab0e80b) | "ret = rename(datafile_old, datafile_new);" | `.ufo/waves/round-42/frozen/src/scrub.c:534` |
```

Quote = 4 whitespace tokens, one physical line, `grep -n -F` hit exactly once in the snapshot (`534:`), and it lies
inside the row's own anchor range `446-535` and inside the frozen counter's SR1 window `476-540`
(`tools/check-scrub-record-r43.py:75`). It is the rename step of the record write path: line 534 sits in
`scrub_rename_file`, whose head is `scrub.c:520` (`grep -n '^static' scrub.c` → `520:static int scrub_rename_file(…`);
it therefore grounds the `teaches` clause "its write discipline" (the record is renamed into place). Round 42's Gate
already quotes `:1502` (`/* write all-zero progress file for a start */`) for the "writes" clause
(`corpus/lessons/round-42.md:21`); the two quotes together cover the write and the rename.

### 2b. Rows touched line

```markdown
Rows touched old→new: S237 only — `used-by` gained `corpus/knowledge/btrfs-scrub-record-r43.md` and now reads `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md`; `status` stays `mined`, and `opened` (`2026-10-26`), `recheck` (`on-release`), `kind` (`code`), `tier` (`A`), `scope`, `anchor` and `teaches` are byte-identical. S240 and S241 are new rows added in the same commit, not touched rows. `git diff 6951ead9 717b716a -- corpus/SOURCES.md` is 3 insertions and 1 deletion (`--numstat`: `3`, `1`, `corpus/SOURCES.md`): the deletion is old S237's line, the insertions are new S237's line plus S240 and S241.
```

That sentence is true of the diff exactly as it stands (§1: 44 bytes appended, 725-byte prefix and 3-byte suffix
identical, 3 insertions / 1 deletion). If the L1 also amends S237's `anchor` cell, the word `anchor` must leave the
byte-identical list — see F1 and the conditional variant there.

## 3. Quote verification (all candidates, receipt `quote-checks.txt`, `quote-tokens.txt`)

Snapshot `.ufo/waves/round-42/frozen/src/scrub.c`, `sha256sum` → `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`,
which is the digest the S237 anchor cell pins. Row `teaches` grep target: "The status record is a userspace file the
scrub start process writes and the status command reads".

| scrub.c line | quote | tokens | occurrences in file | in row anchor ranges | note |
|---|---|---|---|---|---|
| **534** | `ret = rename(datafile_old, datafile_new);` | 4 | 1 | yes (`446-535`) | **draft**: the rename half of "write discipline"; no `|` |
| 1502 | `/* write all-zero progress file for a start */` | 9 | 1 | yes (`1498-1512`) | round 42's quote; the "writes" half |
| 67 | `#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"` | 3 | 1 | yes (`67-70`) | names the record file ("userspace file") |
| 517 | `return scrub_open_file(datafile, O_WRONLY\|O_CREAT);` | 3 | 1 | yes (`446-535`) | carries a pipe (escaped here for the table); see F2 — not usable unescaped in a Gate cell |
| 487 | `ret = flock(fd, LOCK_EX\|LOCK_NB);` | 4 | 1 | yes (`446-535`) | carries a pipe (escaped here for the table); see F2 |
| 483 | `fd = open(datafile, m, 0600);` | 5 | 1 | yes (`446-535`) | generic open helper |
| 925 | `err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");` | 5 | 1 | **no** (`826-895` ends at 895) | on-point for `_tmp`+rename, but outside the row's anchor |

Alternate cell, if the L1 prefers the same located quote round 42 used (swap the quote and location cells only; do
not add a second S237 row):

```markdown
| S237 | https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c (raw: https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c; tag v7.1 peeled 4ab0e80b) | "/* write all-zero progress file for a start */" | `.ufo/waves/round-42/frozen/src/scrub.c:1502` |
```

## 4. URL resolution

`curl -sSfLI -o /dev/null -w '%{http_code}'` (receipt `http-status.txt`), 2026-10-26:

- `https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c` → **200** (the row's URL; status only, as asked).
- `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` → **200**.
- Extra check (not asked, cheap): a full `curl -sSfL` of the raw URL gave `sha256 48df2e2f…f0801` — the digest the
  anchor cell pins — and `cmp` against the frozen round-42 copy was silent (byte-identical), so the tag's live bytes
  still match the snapshot the Gate quote is located in.

## 5. Findings

**F1 — the row's `anchor` ranges do not cover 13 of the 22 S237 quote sites in the round-43 entry.**
`corpus/knowledge/btrfs-scrub-record-r43.md` quotes scrub.c at these lines (`grep -n '`S237` scrub\.c:'`, entry line →
scrub.c line, receipt `anchor-coverage.txt`): 27→517, 29→483, 31→487, 33→917, 35→922, 37→925, 39→534, 41→1485,
58→1833, 60→1434, 62→864, 64→823, 66→1502, 68→1698, 70→1706, 72→1249, 74→1295, 76→1333, 90→1200, 92→1201, 94→1946,
96→341. The S237 anchor cell lists `67-70, 280-330, 446-535, 826-895, 1110-1125, 1186-1220, 1330-1340, 1498-1512,
1925-1945`; 13 sites fall outside all of them: **917, 922, 925** (`scrub_write_progress`, the SR1 write path),
**823** (`dest->stats.t_start`), **1249, 1295** (`do_print`), **1434** (`sp[i].resumed`), **1485** (`unlink(sock_path)`),
**1698, 1706** (the two recording-failure `error()` lines that ground the `teaches` clause "the cases that leave no
record"), **1833** (`return scrub_start(cmd, argc, argv, true);`), **1946**, **341** (`"running"` label). The frozen
counter's own windows do cover every one of them (`tools/check-scrub-record-r43.py:75-86`: SR1 `897-935`,
`1480-1500`; SR3 `795-830`, `1245-1300`, `1425-1445`, `1686-1710`, `1828-1836`; SR6 `336-344`, `1940-1950`), and the
counter never reads the row's anchor (`sources_ok` checks only kind/`mined`/`opened`/`used-by`, `:306-316`). So no
gate fails, but on a re-open the row's evidence pointer and the text it is cited for disagree. If the L1 closes that
by extending the anchor, the Rows-touched line must say so; the used-by-only sentence in §2b is correct only while
`anchor` is untouched. Suggested minimal edit (L1's call, not part of my draft): append
`, 341, 823, 917-925, 1249-1300, 1434, 1485, 1686-1710, 1828-1836, 1940-1950` to the anchor's `cmds/scrub.c lines`
list, and replace "`anchor` and `teaches` are byte-identical" in §2b with "`teaches` is byte-identical and `anchor`
gained the ranges this round quotes".

**F2 — pipe-bearing lines are unsafe as Gate quotes in this lane's readers, which is why the draft uses `:534`.**
`tools/check-kernel-taint.py:84` splits table cells with `CELL_SPLIT = re.compile(r'(?<!\\)\|')`, and `norm()` there
(`:106`) and in `tools/check-memory-pressure.py:98` is only `' '.join(str(text).split())` — no `\|` → `|` unescape.
A Gate quote escaped as `O_WRONLY\|O_CREAT` would therefore not whitespace-match the snapshot bytes. `:517` and `:487`
both carry `|`; `:534`, `:1502`, `:67` and `:483` do not. Nothing in this round's counter reads the lesson's Gate
(`grep -n 'Gate' tools/check-scrub-record-r43.py` → no match), so this is preventive, not a live failure.

**F3 — the anchor ends one line before the line this round's running-state claim cites.** The anchor's last range is
`1925-1945`; `corpus/knowledge/btrfs-scrub-record-r43.md:94` quotes `:1946`
`in_progress = is_scrub_running_in_kernel(fdmnt, di_args, fi_args.num_devices);`. `:1925` is the `EOVERFLOW`
socket-name comment and `:1946` is the kernel probe itself — the range looks like it was closed on the status-read
fallback block and missed the probe. Same remedy as F1 (`1940-1950`).

**F4 — the used-by chain is consistent with the entry's own source line.** `corpus/knowledge/btrfs-scrub-record-r43.md:1`
opens `source: S237 S240 S241 (…)` and names the round-42 snapshot with digest `48df2e2f…f0801`, matching the S237
anchor cell; the `used-by` edit at 717b716a is therefore the pointer the entry expects, and S237's `status` stays
`mined` (no re-open flip is implied).

## 6. Not run, and why

- The round-43 C2 counter (`tools/check-scrub-record-r43.py`) was **not** run: its verdict conjunct needs wave-2
  `C2RevSR*`/`C2CritSR*` records that do not exist yet, so it would print `verdicts_ok 0`/FAIL with no bearing on a
  Gate draft. Its predicate also does not read the lesson.
- The C1 counter, the census and the census selftest were not run: no claim here depends on them.
- The S237 URL was checked status-only as the item asked, plus the one extra raw fetch in §4; no other network read.
- No tool was installed or upgraded. No sudo, no pacman, no service, no mount, no `btrfs` verb, no git/jj mutation in
  the lane (only `git show/diff/grep/cat-file`, all read-only). Scratch `/fast/scratch/hyaku/tsukuroi-r43/SrcGateS237/`
  was removed after the receipts were copied.

## Artifacts

- Report: `.ufo/waves/round-43/w1/SrcGateS237.md` (this file).
- Receipts: `.ufo/waves/round-43/w1/SrcGateS237/` — `sources-diff.txt` (full diff, numstat, stat), `old-s237.txt`,
  `new-s237.txt`, `cell-diff.txt`, `usedby-replication.txt`, `anchor-coverage.txt`, `quote-checks.txt` (all `grep -n`
  hits and function heads), `quote-tokens.txt`, `line534.txt` (`cat -A`), `http-status.txt` (HTTP codes, live digest,
  `cmp`), `counter-windows.txt` (the frozen windows and `used_by` source).
