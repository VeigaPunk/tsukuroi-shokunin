VERDICT: supports

# F-2 — S237 / S240 re-open, used-by log, registry validate (seat SrcGateReopen, round 44 w1)

Claim under test: the two rows the round-44 entry leans on for the older halves of its story — S237 (btrfs-progs
v7.1 `cmds/scrub.c`) and S240 (Linux v7.2.11 `fs/btrfs/ioctl.c`) — still re-open to the same bytes, and the
`98020ece` → `7e081698` registry diff changes only their `used-by` cell (column 11). Both hold. Extra finding: the
round-44 lesson's own `recheck:` line does not name the fetch log that covers these two rows (§5, observation, does
not change the verdict).

## 1. Re-open (live, this seat, 2026-10-27T00:20:00Z)

| Row | URL re-opened (raw route) | HTTP | bytes | live sha256 | frozen file | round-4x `SHA256SUMS` line |
|---|---|---|---|---|---|---|
| S237 | `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` | 200 | 57034 | `48df2e2f…8f0801` | `.ufo/waves/round-42/frozen/src/scrub.c` (57034) | `48df2e2f…8f0801  scrub.c` |
| S240 | `https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/ioctl.c` | 200 | 145999 | `7b3488f2…4ba01` | `.ufo/waves/round-43/frozen/src/ioctl.c` (145999) | `7b3488f2…4ba01  ioctl.c` |

Full digests: S237 `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`,
S240 `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01`. Three-way equality
live = frozen = `SHA256SUMS` for both (`w1/SrcGateReopen/refetch.txt`).

Second route for S240, the one the round-43 `FETCH.txt` names
(`https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11`): HTTP 200,
145999 bytes, same sha256 — the two hosts agree.

The URLs written in the registry rows (HTML views, not the raw files) also resolve now:
`…/btrfs-progs/blob/v7.1/cmds/scrub.c` → HTTP 200, `…/stable/linux.git/tree/fs/btrfs/ioctl.c?h=v7.2.11` → HTTP 200.

Tag pins re-read with `git ls-remote` in the same session and unchanged since the pins were written:

```
0a919c7d6e389c07920675b7fad3f793b92aa78b	refs/tags/v7.1
4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b	refs/tags/v7.1^{}
8316c24ec1b77dba19ba072ca4fe251b36dc65d3	refs/tags/v7.2.11
a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea	refs/tags/v7.2.11^{}
```

These equal the round-42 `FETCH.txt` ("tag v7.1 = 0a919c7d…, peeled commit 4ab0e80b…") and the round-43 one
("tag v7.2.11 = 8316c24e…, peeled commit a2de78ee…"), so the anchors are still the released trees, not moved tags.

Quote lines re-read in the frozen snapshots (tabs present in the file; the lesson prints them with indentation
stripped): `scrub.c:421` `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);`, `scrub.c:1293`
`do_background = false;`, `scrub.c:1295` `do_print = true;`, `scrub.c:1546` `scrub_handle_sigint_child(fdmnt);`,
`ioctl.c:3139` `ret = btrfs_scrub_progress(fs_info, sa->devid, &sa->progress);`, `ioctl.c:3141`
`if (ret == 0 && copy_to_user(arg, sa, sizeof(*sa)))` (`w1/SrcGateReopen/quotes.txt`). Because the frozen bytes
equal the live bytes, these line numbers are the line numbers of the tagged upstream files, not just of a snapshot.

## 2. Field-level registry diff (claim: only column 11 may change)

`git -C …/tsukuroi-shokunin diff 98020ece0674e0b569ee23aed10ffbee355b248e 7e081698d4fc3c4ea944884fd093058de9909de1
-- corpus/SOURCES.md` is `8 ++++++--` (6 insertions, 2 deletions). Splitting each registry line on `|` gives 11 cells
in both revisions for both rows, and exactly one cell differs per row:

- **S237**, `corpus/SOURCES.md:246` in both revisions, cell 11
  old `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md`
  new `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md`
- **S240**, `corpus/SOURCES.md:249` in both revisions, cell 11
  old `corpus/knowledge/btrfs-scrub-record-r43.md`
  new `corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md`

Cells 1–10 of both rows are byte-identical (`status` `mined`, `opened` `2026-10-26`, `recheck` `on-release`).
S242–S245 are appended at `corpus/SOURCES.md:251-254`; S241 stays at `:250`, so no earlier row is renumbered
(`w1/SrcGateReopen/field-diff.txt`). The added used-by target
`corpus/knowledge/btrfs-scrub-record-r44.md` exists (145 lines, read by this seat), so the new cells do not create a
dangling reference.

## 3. `sources-census.sh validate`

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
EXIT=0
stderr: (empty)
stdout: 41 lines = 40 × `tsukuroi W04 …` + `tsukuroi ok /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`
```

Warning count: **40**, all `W04` (duplicate URL across scopes; W-codes do not affect lane status). Zero `E` codes and
zero `E11` (used-by path missing). The bytes validated are the implementation bytes: the worktree
`corpus/SOURCES.md` is sha256 `4da9c02c…63b845`, identical to `git show 7e081698:corpus/SOURCES.md`, and
`git status --porcelain` reports nothing pending for that file.

Pre-existing check: the same 40 `W04` lines (code + message, sorted) are produced from the base registry
`98020ece`, and the two sorted sets are identical (`diff` printed nothing), so the wave introduced no new warning.
No warning names S237–S245. Caveat on that control: `--file` mode derives the used-by base as
`realpath dirname(<file>)/..` (`scripts/sources-census.sh:497-502`), so a copy at a scratch root reports every
used-by path as `E11` (387 lines at base). That flood is a mode artifact, not base-state evidence; the required
`--root … tsukuroi` run reports `E11` zero times. Receipt: `w1/SrcGateReopen/census-validate.txt`.

## 4. Proposed text — lesson Gate lines for `corpus/lessons/round-44.md`

The file does not exist yet (`corpus/lessons/` holds `round-40.md` … `round-43.md`), so this is a draft in the
round-43 Gate shape, ready to paste as a subsection of `## Gate`:

```markdown
### Re-opened rows and rows touched old→new (F-2, wave-1 seat SrcGateReopen)

| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S237 | https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c (raw re-fetched byte-identical, HTTP 200, 57034 bytes, sha256 `48df2e2f…8f0801`; `w1/SrcGateReopen.md`) | "ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);" | `.ufo/waves/round-42/frozen/src/scrub.c:421` |
| S240 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/ioctl.c?h=v7.2.11 (raw `plain/…?h=v7.2.11` and raw.githubusercontent.com re-fetched byte-identical, HTTP 200, 145999 bytes, sha256 `7b3488f2…4ba01`; `w1/SrcGateReopen.md`) | "ret = btrfs_scrub_progress(fs_info, sa->devid, &sa->progress);" | `.ufo/waves/round-43/frozen/src/ioctl.c:3139` |

Tag pins re-read with `git ls-remote` this round: btrfs-progs `refs/tags/v7.1` `0a919c7d…aa78b` peeled
`4ab0e80b…7ba8b`, Linux `refs/tags/v7.2.11` `8316c24e…65d3` peeled `a2de78ee…b6ea`, both as recorded in the
round-42 and round-43 `FETCH.txt`.

Rows touched: **S237 `used-by`** `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md` → `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md`;
**S240 `used-by`** `corpus/knowledge/btrfs-scrub-record-r43.md` → `corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md`
(status `mined`, `opened` 2026-10-26 and `recheck` on-release unchanged in both). Both rows keep their line numbers
`corpus/SOURCES.md:246` and `:249`; the diff `98020ece` → `7e081698` changes column 11 of those two rows and nothing
else (cells split on `|`, 11 columns before and after; `w1/SrcGateReopen/field-diff.txt`).

Registry check: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` exits 0 with
40 `W04` duplicate-URL warnings and no `E` code; the `W04` set is identical at base and no S237-S245 row carries a
warning (`w1/SrcGateReopen/census-validate.txt`).
```

If the round-44 Gate keeps the round-43 table header verbatim (`### Re-opened row and rows touched old→new`), drop the
suffix and the singular/plural difference; the table and the `Rows touched:` prose are unchanged.

## 5. Observations (reported, not absorbed)

1. **The lesson's `recheck:` line covers S242–S245 only.** `corpus/knowledge/btrfs-scrub-record-r44.md:3` says
   "re-fetch the URLs in `.ufo/waves/round-44/frozen/src/FETCH.txt` and compare `sha256sum` with its `SHA256SUMS`",
   but that file lists only kernel `scrub.c`/`sysfs.c` and the three Arch packaging files (`S242`, `S243`, `S244`).
   S237's and S240's raw URLs appear in `.ufo/waves/round-42/frozen/src/FETCH.txt` and
   `.ufo/waves/round-43/frozen/src/FETCH.txt`. A reader following the lesson's recheck literally cannot recheck the
   two rows this seat re-opened. Suggested one-clause fix for the L1: append "S237 and S240 per the round-42 and
   round-43 `FETCH.txt`". Not claimed as a defect of the frozen claims — those do not mention the recheck line.
2. **`--file` mode and `E11`.** `scripts/sources-census.sh:497-502` sets the used-by base to
   `realpath "$(dirname "$file_abs")/.."`, so `validate --file` on a registry copied outside a lane tree reports
   every non-`—` used-by path as missing (387 at base). Harmless for the required command, worth knowing before
   anyone reads a `--file` run as a base-state control.
3. **Quote indentation.** The upstream lines are tab-indented; the lesson quotes start at the first non-space
   character. Same text, not byte-identical to the file line — consistent with the round-42/43 entries' style.

## 6. Limits — what this seat did not do

- Did not run the C1 counter (`tools/score-scrub-arm-r44.py`), the census selftest, or the C2 counter
  (`tools/check-scrub-record-r44.py`); none is in this item, and the cost rule forbids stacking heavy counters.
  `validate` is the only counter this seat ran, once against the live lane and once against the extracted base file.
- Did not establish a full base-state `validate` control: `E11` cannot be compared between revisions without a
  complete corpus tree at the base commit, and this seat writes no clone. The pre-existing claim therefore rests on
  the identical `W04` sets, which are URL-derived and independent of the used-by base.
- No host mutation: no package command, no unit/timer action, no sysfs or `/var/lib` write, no scrub command, no
  sudo; the only network operations are `curl` GETs and `git ls-remote`. No lane file was edited; nothing was
  committed.
- `corpus/lessons/round-44.md` does not exist, so the Gate text is a draft and no lesson file was written.

Receipts (under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w1/SrcGateReopen/`):
`refetch.txt` (re-open, sizes, digests, tag peels), `field-diff.txt` (cell-level registry diff, row positions),
`census-validate.txt` (exit code, full stdout, warning counts, base control), `quotes.txt` (located quote lines).
Scratch `/fast/scratch/hyaku/tsukuroi-r44/SrcGateReopen/` is removed before the seat ends.
