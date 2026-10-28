VERDICT: supports — all four round-49 corrections landed (three verbatim, one with a change); NEW defect D5 found in the retained half of the `[inference]` mark (below), same class as the defect the correction fixed.

Seat R50ExecGRCorr, item C1-B1. Every byte below is read from the freeze revision
`8029cdba1049df25632c91a23c8db4eefb54be5f` (`git -C …/tsukuroi-shokunin show <rev>:corpus/knowledge/btrfs-scrub-grounding-r45.md`);
the lane working tree was never opened. I reproduced the frozen GR2 row hash from the freeze bytes
(lines 56-152, LF-joined, no trailing LF → `a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f`,
the value the round claims give), so the row I checked is the row under test
(`.ufo/waves/round-50/w1/R50ExecGRCorr/defect-matches.txt`). Demanded wording is from
`.ufo/waves/round-49/w1/R49CritGR2b.md:19-24` (raw).

## Per-defect result

| # | Demanded by R49CritGR2b | Frozen location | Status |
|---|---|---|---|
| 1 | `[inference]` mark narrowed to btrfs-progs printing (exact replacement at R49CritGR2b.md:19) | `btrfs-scrub-grounding-r45.md:83-85` | **adopted verbatim** (line-wrap only; a sentence-final `.` follows the `)]`) — mechanical fixed-string match count 1 after newline→space flattening |
| 2 | S240 with snapshot path and digest in the `source:` line and QUALITY item 7 (R49CritGR2b.md:20) | `:1` (`source:`), `:261` (QUALITY 7) | **adopted verbatim** for `source:`; **adopted with a change** for QUALITY 7 |
| 3 | dev-replace.c:1128 quote gains its `* ` prefix (exact replacement at R49CritGR2b.md:21) | `:127` | **adopted verbatim** — fixed-string match count 1 |
| 4 | Declare the S247 range gap in Limits (exact sentence at R49CritGR2b.md:22) | `:229-232` | **adopted with a change** (same four line refs, reworded tail, new bullet + attribution) |

### Defect 1 — mark narrowed (adopted verbatim)
Frozen `:83-85`: "[inference: how `btrfs scrub start` and `btrfs scrub status` print these returns is not pinned here; the
scrub-start ioctl's own path is pinned and returns the `btrfs_scrub_dev` value (ioctl.c:3093-3095) unless the
argument copy fails, when it returns `-EFAULT` instead (ioctl.c:3109-3110, ioctl.c:3115)]."
The old conjunct ("ioctl and btrfs-progs side … hands these returns to userspace unchanged") is gone — `grep -cF 'ioctl and btrfs-progs side'` = 0.
Citations resolve in the pinned S240 snapshot:
- `ioctl.c:3093` `ret = btrfs_scrub_dev(fs_info, sa->devid, sa->start, sa->end,` / `:3094` `&sa->progress, sa->flags & BTRFS_SCRUB_READONLY,` / `:3095` `false);`
- `:3109` `if (copy_to_user(arg, sa, sizeof(*sa)))` / `:3110` `ret = -EFAULT;`
- `:3115` `return ret;`
- `:3132` `if (!capable(CAP_SYS_ADMIN))` / `:3133` `return -EPERM;` (the row's Host reading cites both)
- `:3190` `if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {`
Receipt: `.ufo/waves/round-50/w1/R50ExecGRCorr/citations.txt`.
**New imprecision introduced by the adopted wording (minor):** "returns the `btrfs_scrub_dev` value … unless the argument
copy fails" reads as exhaustive over the ioctl's returns, but the same ioctl returns earlier at `ioctl.c:3081-3082`
(`memdup_user` failure), `:3085` (`-EOPNOTSUPP` for unsupported flags) and `:3089-3090` (`mnt_want_write_file`).
Proposed tightening (append inside the bracket, before `)]`): "; the ioctl can also return before the call, from `memdup_user`
(ioctl.c:3080-3082), on unsupported flags (ioctl.c:3084-3085) or from `mnt_want_write_file` (ioctl.c:3087-3090)".

### Defect 2 — provenance (adopted; one change)
Frozen `:1` now reads "source: S246 S247 S248 S249 S242 S243 S244 S237 S240 (… S240 is Linux v7.2.11 `fs/btrfs/ioctl.c`,
snapshot `.ufo/waves/round-43/frozen/src/ioctl.c`, sha256 7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01
(round 50: the row cites it at ioctl.c:3093-3095, :3109-3110, :3115, :3132-3133 and :3190); …)". Fixed-string match count 1.
Digest verified three ways: `sha256sum .ufo/waves/round-43/frozen/src/ioctl.c` =
`7b3488f2…ba01`; `.ufo/waves/round-43/frozen/src/SHA256SUMS:1` carries the same value; `corpus/SOURCES.md:249`
registers "raw bytes sha256 7b3488f2…ba01". The parenthetical's five cited lines are exactly the ioctl.c lines the row uses.
QUALITY `:261` now reads "7. External claims cite S246-S248 and S240 (tier A, code and docs at pinned tags)" — **change**:
S240 was appended as demanded but the item was reworded rather than minimally extended.
**No new error.** Pre-existing and unchanged: S249, S242, S243, S244 and S237 are still not named in QUALITY 7 although the
`source:` line declares them; the round-49 critic did not raise it and this correction neither fixed nor worsened it.

### Defect 3 — quote exactness (adopted verbatim)
Frozen `:127`: `**Quote.** `S247` dev-replace.c:1128: "* Scrub doing the replace isn't running so we need to do the"`.
Pinned line (`round-45/frozen/src/dev-replace.c:1128`, `cat -A`): `^I^I * Scrub doing the replace isn't running so we need to do the`
— the quote is now the line's text with only the leading whitespace removed, matching the GR1 convention the critic noted.
**No new error.**

### Defect 4 — S247 range gap (adopted with a change)
Frozen `:229-232`: "Round 50: the widened S247 ranges still do not list `dev-replace.c:1111`, `:1126-1142`, `:1171-1195` or
`:1184-1188`, the lines the GR2 cancel and unmount-suspend clauses cite; the snapshot bytes are digest-pinned whole-file, so
no claim is unsupported, but the gap is declared here instead of left undeclared (`.ufo/waves/round-49/w1/R49CritGR2b.md`
defect 4)." The demanded first clause matches as a fixed string; the demanded tail ("which GR2 cites for the two cancel
branches and for the unmount-suspend function") was replaced by an equivalent phrase, and the sentence sits in its own Limits
bullet with an attribution instead of being appended to the sentence at `:224-225` that names the widened ranges.
The four line refs are genuinely outside S247's registered ranges (`corpus/SOURCES.md:256`: 700-703, 1143-1144, 1235,
1256-1268, 1276-1300). Beyond the demand, `:233-235` adds the matching S240 disclosure; its facts check out against
`corpus/SOURCES.md:249` (ranges 3066-3075, 3118-3140, 5578-5584; digest `7b3488f2…ba01`).
**No new error.**

## D5 — NEW defect: the retained half of the mark is false (not one of the four)

The correction narrowed the mark to "how `btrfs scrub start` and `btrfs scrub status` print these returns is not pinned here"
(`:83`). Under the exact standard the round-49 critic applied to the ioctl conjunct — the file is pinned, digest-checked
whole-file, and the entry names it — that conjunct fails too:

- **S237 is pinned and named by this entry.** `corpus/SOURCES.md:246` registers btrfs-progs v7.1 `cmds/scrub.c`, "raw bytes
  sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801"; the frozen `source:` line (`:1`) names it as
  "S237 `.ufo/waves/round-42/frozen/src/scrub.c`"; `sha256sum` of that file = `48df2e2f…0801` (matches). GR3 cites the same
  file (`scrub.c:421`, `:439`, `:1546`).
- **The start path's printing is decided by it.** `cmds/scrub.c:965` `ret = ioctl(sp->fd, BTRFS_IOC_SCRUB, &sp->scrub_args);`
  stores the errno at `:970` (`sp->ioctl_errno = errno;`); the per-device report at `:1619-1639` switches on it —
  `:1621-1625` `case ENODEV:` → `warning("device %lld not present", devid)`; `:1626-1628` `case ECANCELED:` → error counted,
  no message; `:1629-1636` `default:` → `error("scrubbing %s failed for device id %lld: ret=%d, errno=%d (%m)", …)`.
  `EINPROGRESS` takes the default arm, so "how `btrfs scrub start` prints these returns" is pinned at `:1619-1639`.
- **The status half is vacuous.** `cmd_scrub_status` is `:1847`; the file's only `BTRFS_IOC_SCRUB` call site is `:965`
  (`:1200` is `BTRFS_IOC_SCRUB_PROGRESS`, used as a boolean at `:1201-1202`; `:1792` is `_CANCEL`), so `btrfs scrub status`
  never receives the start ioctl's return — it reads the userspace record.

Evidence: `.ufo/waves/round-50/w1/R50ExecGRCorr/btrfs-progs-printing.txt`, `.ufo/waves/round-50/w1/R50ExecGRCorr/hashes.txt`.
Risk to the round: a round-50 critic applying the round-49 test will find the same "pinned file called unpinned" defect and
bind GR2 `partly` again, which the C1 predicate cannot survive.

Proposed replacement for `:83-85` (exact, one paragraph; range gap declared as the Limits style requires):

"[inference: `btrfs scrub status` never receives these returns — it reads the userspace record (`S237` cmds/scrub.c:1847) —
while `btrfs scrub start` stores the ioctl's errno (`S237` cmds/scrub.c:965, :970) and prints it from a per-device switch:
`ENODEV` as "device %lld not present", `ECANCELED` as an error with no message, and every other errno, `EINPROGRESS`
included, as "scrubbing %s failed for device id %lld: ret=%d, errno=%d (%m)" (`S237` cmds/scrub.c:1619-1639)]"

If that text is taken, Limits must gain the matching disclosure, because `scrub.c:965`, `:970` and `1619-1639` are outside
S237's registered ranges: "S237's declared ranges (67-70, 280-330, 446-535, 826-895, 1110-1125, 1186-1220, 1330-1340,
1498-1512, 1925-1945) likewise do not list `scrub.c:965`, `:970` or `:1619-1639`, the start-path lines this round cites."

## What I did not do

No counter was run (`tools/check-scrub-admission-r50.py`, the C2 matcher counter and the C3 adjacency counter are outside
this item's command list); no census selftest; the 18-seat cohort and the GR1/GR3 rows were not re-read; no upstream fetch;
no lane or fleet file was created, edited or deleted except this report and the four receipts; no git or jj mutation
anywhere; no tool was installed or upgraded.

Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50ExecGRCorr/` was removed after the receipts were copied into the wave dir.
