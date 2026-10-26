VERDICT: draft

# Seat SrcGateS240 — F-1: `## Gate` "New SOURCES rows" entries for S240 and S241

Item: draft the two Gate rows for `corpus/lessons/round-43.md`. That file does not exist yet (newest in
`corpus/lessons/` is `round-42.md`), so the block below is proposed text for the L1 to land, not an edit of an
existing file. Format source: `corpus/lessons/round-42.md:15-23` — the `### New SOURCES rows (all opened 2026-10-26 by
this round's L1; each quote located with \`grep -n\` in the pinned snapshot)` heading, the four-column table
`| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |`, and the `Snapshot digests:` paragraph
after it (`round-42.md:26-28`).

## Draft — exact Markdown

```markdown
### New SOURCES rows (all opened 2026-10-26 by this round's L1; each quote located with `grep -n` in the pinned snapshot)

| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S240 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/ioctl.c?h=v7.2.11 (raw: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11; tag v7.2.11 peeled a2de78ee) | "if (!capable(CAP_SYS_ADMIN))" / "return -EPERM;" — the first check in each of the three scrub handlers | `.ufo/waves/round-43/frozen/src/ioctl.c:3072-3073, 3120-3121, 3132-3133` (handlers open `:3066`, `:3118`, `:3126`; dispatch `:5578-5583`) |
| S241 | own-work capture `.ufo/waves/round-43/frozen/hostcap/` (`capture.sh`, run 2026-10-26T21:51:26Z, uid 1000) | "uid 1000 euid_caps 0000000000000000"; "root_fs btrfs 1d02a454-c549-4a35-b567-89d60902af8e"; "scrub_progress_ioctl devid=1 errno=EPERM (1)"; "scrub_status_exit 0"; "no stats available" | `.ufo/waves/round-43/frozen/hostcap/capture.txt:2,5,6,8,10` (probe on `/` at `capture.sh:18`; `btrfs scrub status /` at `:34`) |

Snapshot digests: `.ufo/waves/round-43/frozen/src/SHA256SUMS` and `.ufo/waves/round-43/frozen/src/FETCH.txt`
(ioctl.c `7b3488f2…4ba01`); the plain URL re-fetched live on 2026-10-26 is byte-identical (145999 bytes, same
sha256) and `git ls-remote` gives tag v7.2.11 → `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`. S241 `capture.txt`
sha256 `f7ecbe7c…c556`, `capture.sh` `77ffeecb…a1a9`. S240 and S241 are new rows this round: neither id exists at
the base `6951ead9`, and both enter already `mined` at `717b716a` — so no `status`/`used-by` transition line applies
to them (the only row touched old→new this round is S237's, drafted by its own seat).
```

Both quote cells are 16 whitespace tokens (≤25). The Location cells carry the `grep -n` line numbers, so each cell is
auditable without re-deriving the offsets from the SOURCES.md anchor ranges.

## Row identity — the `teaches` cell each draft quote must ground

| Row | `corpus/SOURCES.md` | `teaches` cell (verbatim) |
|---|---|---|
| S240 | `:249` | "The scrub start, cancel and progress ioctls each return EPERM to a caller without CAP_SYS_ADMIN before any other check" |
| S241 | `:250` | "For uid 1000 the scrub-progress ioctl on the root filesystem fails with EPERM and scrub status prints no stats available" |

Both rows: `status` `mined`, `opened` 2026-10-26, `recheck` `on-release` (S240) / `30d` (S241), `used-by`
`corpus/knowledge/btrfs-scrub-record-r43.md`.

## Why these quotes ground those cells

**S240** — the cell has three clauses: (a) the three scrub ioctls, (b) each returns EPERM, (c) without
CAP_SYS_ADMIN, before any other check.

- (a) dispatch: `.ufo/waves/round-43/frozen/src/ioctl.c:5578-5583` maps `BTRFS_IOC_SCRUB` →
  `btrfs_ioctl_scrub(file, argp)`, `_CANCEL` → `btrfs_ioctl_scrub_cancel(fs_info)`, `_PROGRESS` →
  `btrfs_ioctl_scrub_progress(fs_info, argp)`.
- (b)+(c) `grep -n -A1 "if (!capable(CAP_SYS_ADMIN))" ioctl.c` returns `3072: / 3073-: return -EPERM;`,
  `3120: / 3121-`, `3132: / 3133-`; the three handler heads (`:3066` `btrfs_ioctl_scrub`, `:3118`
  `btrfs_ioctl_scrub_cancel`, `:3126` `btrfs_ioctl_scrub_progress`) show the guard is the first check after the
  locals, so nothing is checked before it (the single local initializer in `btrfs_ioctl_scrub`,
  `inode_to_fs_info(file_inode(file))` at `:3068`, is an accessor, not a check). The dispatcher itself adds no capability test on this path:
  `long btrfs_ioctl(` opens at `:5495`, `switch (cmd) {` at `:5503`, and no `capable(` occurs in `:5495-5502`.
  File open on a btrfs mount is VFS permission, not an ioctl check.

**S241** — four clauses, four located lines: uid 1000 (`capture.txt:2`), the root filesystem (`capture.txt:5`
`root_fs btrfs 1d02a454…`; the probe opens `/` at `capture.sh:18`, the status run is `btrfs scrub status /` at
`capture.sh:34`), the progress ioctl failing EPERM (`capture.txt:6`), and status printing no stats
(`capture.txt:10` `no stats available`, with `capture.txt:8` `scrub_status_exit 0` showing the line is printed on a
successful run, not an error banner).

## Verification run (2026-10-26)

Full transcript: `.ufo/waves/round-43/w1/SrcGateS240/verify.txt` (92 lines). Summary:

- **Frozen identity.** `sha256sum` on the pinned files: `ioctl.c` `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01`
  (equals `frozen/src/SHA256SUMS` and the SOURCES.md:249 anchor), `capture.txt`
  `f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556` (equals the SOURCES.md:250 anchor and the
  round-43 declaration), `capture.sh` `77ffeecb…a1a9`.
- **URL live.** `curl -sS -o /dev/null -w '%{http_code} %{size_download}' -L` on the tree URL → `200 367878` (HTML
  page); on the plain URL → `200 145999`, saved and `sha256sum` `7b3488f2…` — byte-identical to the frozen snapshot.
  `timeout 60 git ls-remote --tags https://github.com/gregkh/linux refs/tags/v7.2.11 'refs/tags/v7.2.11^{}'` →
  `8316c24ec1b77dba19ba072ca4fe251b36dc65d3 refs/tags/v7.2.11` and
  `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea refs/tags/v7.2.11^{}` (receipt §B).
- **Quotes located.** Each quoted string appears at its cited line: receipt §C (`grep -n -A1` plus
  `sed -n '3066,3074p;3118,3122p;3126,3134p'` and `sed -n '5578,5584p'` for ioctl.c), §D (`grep -n` and
  `sed -n '2p;5p;6p;8p;10p'` for capture.txt; `grep -n` on capture.sh for the two probe lines).
- **Row novelty.** `git show 6951ead90566b2d74f7c45b4efca29246badad64:corpus/SOURCES.md | grep -c '| S240 |\|| S241 |'`
  → `0`; first present at `717b716a` as lines 249-250; `git diff 717b716a…HEAD -- corpus/SOURCES.md` → 0 lines at
  HEAD `7d0ed1c2` (receipt §E).

## Limits and notes

- The `round-43.md` preamble sentence in my draft ("all opened 2026-10-26 by this round's L1") mirrors round-42's
  heading; the rows themselves record `opened 2026-10-26` in SOURCES.md, and my URL check was made today.
- Unlike round 42 (S237-S239 `queued` at the freeze `a84fc9de`, flipped `mined` at the implementation commit), S240
  and S241 are absent at the round-43 freeze `fe357001` and are introduced already `mined` at `717b716a`. That is why
  the draft carries a novelty sentence instead of a `status`/`used-by` old→new line.
- The SOURCES.md:249 anchor ranges `3066-3075, 3118-3140, 5578-5584` are pointers at the guards, not handler
  extents: the handlers end at `:3116` (scrub), `:3124` (cancel), `:3145` (progress). Every quoted line falls inside
  the ranges, so nothing is false — but the ranges should not be read as complete function bodies. Reported as a
  note, not a defect of the row.
- Deliberately not checked: which upstream commit introduced the guards (no clause depends on it); behaviour on
  non-btrfs filesystems. I ran no lane counter — F-1 asks for text only.
- Not done by me: no edit to `corpus/SOURCES.md` or any other tracked file; `corpus/lessons/round-43.md` untouched
  because it does not exist; no git/jj mutation; no tool installed.

## Touched surfaces

- Written: this report (`.ufo/waves/round-43/w1/SrcGateS240.md`) and
  `.ufo/waves/round-43/w1/SrcGateS240/verify.txt`; scratch `/fast/scratch/hyaku/tsukuroi-r43/SrcGateS240/` removed
  after the receipt was copied.
- Read-only: the lane's `corpus/SOURCES.md`, `corpus/lessons/round-42.md`, `.ufo/waves/round-43/frozen/**`,
  `.ufo/waves/round-43/w1-spec.json` and the lane's git object store (`git show`/`git diff` only).
