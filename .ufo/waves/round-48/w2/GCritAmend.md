VERDICT: defect-found

Item: C2-A5, GR2 amendment-fidelity attack, non-counted seat. Revision under test: ae99f021b76f8eb1c8805d32d80644464afb1ff6.
Section bytes verified: `python3 tools/check-scrub-admission-r48.py --revision ae99f021b76f8eb1c8805d32d80644464afb1ff6 --section-hash` printed GR2 = e0b391e198f67ff57ce7971e2dd589faaa9390ebf2d2fd49dc6d103c163a52ce, structural_ok 1, no problems (receipt: section-hashes.json). The r47-read predecessor was extracted at revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 (the revision R47CritGR2a bound) and diffed against current (receipts: gr2-cur.txt, gr2-r47read.txt, stmt-r47-to-r48.diff).

## What the amendment fixed correctly

R47CritGR2a's defective clause was "When the unmount suspend path runs, it calls `btrfs_scrub_cancel`" (`.ufo/waves/round-47/w1/R47CritGR2a.md` line 19): the quoted call at dev-replace.c:1143-1144 sits inside `btrfs_dev_replace_cancel`'s `case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:` (dev-replace.c:1126), not in `btrfs_dev_replace_suspend_for_unmount` (dev-replace.c:1171-1195, which contains no `btrfs_scrub_cancel`; its only writes are state=SUSPENDED at :1185-1186, time_stopped, item_needs_writeback, a btrfs_info). Grep over `.ufo/waves/round-45/frozen/src/dev-replace.c` confirms the only `btrfs_scrub_cancel` callsites are :1111 (STARTED case) and :1144 (SUSPENDED case), both inside `btrfs_dev_replace_cancel` (:1085-1169).

The current GR2 text does move the attribution: "…`btrfs_dev_replace_cancel` calls `btrfs_scrub_cancel` when its cancel ioctl handles a suspended replace (`dev-replace.c:1126-1144`)" and adds "The unmount suspend path itself only sets the state to SUSPENDED (`dev-replace.c:1171-1199`) and does not cancel the scrub." Both are code-true at the pinned snapshot. The r46 residual finding (missing `-EAGAIN` ordering, `V46ResCritGR2.md` line 5) is also correctly applied: "after a filesystem-closing check that returns `-EAGAIN` first (`btrfs_fs_closing`), the function allocates its scrub context and takes the scrub workers … whose errors return first" matches scrub.c:3094-3116 exactly (closing check first, then setup_ctx :3109, workers_get :3114, then device checks :3120/:3127/:3138, then the EINPROGRESS refusal :3147-3154).

The other surfaces the item named are clean: the exclusive-op sentence (sysfs.c:1288 "device replace\n" name; resume takes exclop at dev-replace.c:1235 — verified verbatim) is unchanged and accurate; the EINPROGRESS wording matches scrub.c:3147-3153 and dev-replace.c:1281-1300 (STARTED and SUSPENDED both fall through to `return true`); the SUSPENDED-state claim is properly conditioned on `btrfs_dev_replace_is_ongoing`, and "a replace suspended by an unmount still counts" is an example, not an exclusivity claim — resume-failure suspensions at dev-replace.c:1223-1224 and :1236-1238 do not contradict it.

## DEFECT F1 — the amendment was welded onto the SR7 relative clause, not the sentence it replaced

R47CritGR2a prescribed replacing the whole *sentence* ("Smallest safe correction", report line 25). Instead the integration spliced the new cancel clause in place of the progress-query consequence inside the old sentence. Diff of the r47-read row vs current (receipt stmt-r47-to-r48.diff):

- r47-read: "…the scrub context the copy attached, which by SR7 **makes a privileged progress query for that devid answer 0.** When the unmount suspend path runs, it calls `btrfs_scrub_cancel`; once the scrub returns and clears its context, the progress query returns `-ENOTCONN`"
- current: "…the scrub context the copy attached, which by SR7 **`btrfs_dev_replace_cancel` calls `btrfs_scrub_cancel` when its cancel ioctl handles a suspended replace** (`dev-replace.c:1126-1144`)…"

Three defects ride on this one weld:

1. **False provenance / scope misattribution.** "which by SR7" now introduces `btrfs_dev_replace_cancel` → `btrfs_scrub_cancel`. SR7 (`corpus/knowledge/btrfs-scrub-record-r44.md` §SR7) covers `dev->scrub_ctx` attach/clear and `btrfs_scrub_progress` semantics; it says nothing about the dev-replace cancel path (its replace side is still marked `[inference]` there). The cancel call's deciding source is S247 dev-replace.c:1143-1144, which the row does cite — but the SR7 connector claims a lineage the cited row does not have. Grammatically the relative clause either attaches "which" to "the scrub context" (a context does not call a function — `btrfs_scrub_cancel(fs_info)` is filesystem-wide, scrub.c:3277-3296, waits on `fs_info->scrubs_running`, takes no context) or to the whole preceding clause (a false causal link: the call is not triggered by the device carrying a context; in the SUSPENDED case cited, the comment at dev-replace.c:1127-1129 says the scrub is *not* running, so no copy context is attached).
2. **Impossible temporal scope.** The clause remains under "While the copy runs". A replace whose cancel ioctl is handling the SUSPENDED state is not copying — the cited comment (dev-replace.c:1127-1129) says exactly that. The STARTED-case cancel at dev-replace.c:1107-1111 is the branch that cancels a running copy; the clause describes its behavior while citing the SUSPENDED branch.
3. **Lost verified consequence.** The r47-read "answer 0" progress-query consequence (supported: scrub.c:3331-3336 — `sctx` copied and 0 returned while `dev->scrub_ctx` is set) was deleted, leaving "carries the scrub context the copy attached" dangling with no stated consequence, and the new clause "When the replace context is absent" is imprecise: `-ENOTCONN` is keyed to the *scrub* context (`dev->scrub_ctx`), not to `fs_info->dev_replace` state.

This clause is what I would mark `partly` as a counted seat: the row's machinery is sound and the cancel attribution is now on the right branch, but the carrying sentence asserts a nonsensical/false linkage and silently dropped a consequence that previously survived review.

### Exact replacement text

Replace the current sentence span (in `## GR2` **Statement.**, between "…and no scrub is started." and "[inference for the ioctl and btrfs-progs side…]"):

> While the copy runs, the replace's source device carries the scrub context the copy attached, which by SR7 makes a privileged progress query for that devid answer 0. When the replace-cancel ioctl handles a suspended replace, `btrfs_dev_replace_cancel` calls `btrfs_scrub_cancel` (dev-replace.c:1143-1144) even though the replace scrub is already not running (dev-replace.c:1127-1129); once the scrub's context is cleared the progress query returns `-ENOTCONN` (scrub.c:3222, :3336). The unmount suspend path `btrfs_dev_replace_suspend_for_unmount` (dev-replace.c:1171-1195) only sets the state to SUSPENDED and does not cancel the scrub; the in-code comment at dev-replace.c:1288-1297 of `btrfs_dev_replace_is_ongoing` is what makes a suspended replace still count as ongoing.

(First sentence restores the r47-read wording verbatim — already read clean. The rest is R47CritGR2a's prescribed correction with its cited ranges corrected to :1127-1129 for the comment and :1288-1297 for the full comment span, and the function named.)

## DEFECT F2 — `## Limits` amendment ledger does not record the round-48 amendment and misdescribes the current text

The ledger's last GR2 bullet says the "unmount-only wording of the suspend-path cancellation were added at the round-47 integration …; the amended row was re-read by the counted round-47 seats". Two problems at the frozen revision:

1. The round-48 substitution of that wording (attribution moved to the cancel ioctl's SUSPENDED branch, `dev-replace.c:1126-1144`; the unmount path re-described as not cancelling) is recorded nowhere. Every prior GR2 amendment carries an entry naming the round, the triggering seat report and the read status; the r48 amendment — made *after* a counted read — has none, and there is no "Gate status — round 47" section noting R47CritGR2a's `partly` that triggered it.
2. The bullet now misdescribes the *current* bytes to a reader: "the unmount-only wording of the suspend-path cancellation" no longer exists in the row (the unmount path is now described as *not* cancelling). Similarly the earlier bullet's "no seat has read that last narrowing" is stale as a present-tense claim — subsequent amendments and reads superseded it — though it is framed as r45 integration history.

Proposed appended bullet (smallest fix, keeps history immutable):

> - GR2's suspended-replace cancel attribution was reworded at the round-48 integration after the counted round-47 critic read `partly` (`.ufo/waves/round-47/w1/R47CritGR2a.md`): the `btrfs_scrub_cancel` call was attributed to `btrfs_dev_replace_cancel`'s suspended case (dev-replace.c:1126-1144) and the unmount suspend path (dev-replace.c:1171-1199) recorded as not cancelling; the earlier "unmount-only" description and the "no seat has read that last narrowing" note refer to superseded wording.

This defect is outside the GR2 section hash (bytes `## GR2`..`## GR3`), so it does not block the C2 row predicate, but it is exactly the kind of stale ledger a future amendment attack or seat reads as current state.

## Minor observations (not defects)

- Quote `S247 dev-replace.c:1128` is verbatim inside its line; the cited comment is at :1127-1130 (range :1126-1144 covers it).
- `:1171-1199` cited for the unmount path overshoots the function end at :1195 by the comment/declaration lines :1197-1198; the function *is* fully inside the range, so the claim holds.
- All other GR2 `**Quote.**` lines were spot-verified verbatim against the pinned snapshots (dev-replace.c:700/701/703/1259/1265/1268, scrub.c:3081/3094/3095/3123/3133/3138/3139/3142/3147/3148/3149/3153/3222/3336, sysfs.c:1288/2015, dev-replace.c:1235/1287/1128/1143/1144).
- Host reading unchanged from the r47-read text R47CritGR2a marked SUPPORTED (report line 21); re-verified consistent.

## Checks not run

- No selftest/census run (not this item). No host sysfs/ioctl reads (unprivileged-only policy; row cites capture.txt + C2ExecHostRecheck attribution, not re-executed).
- `btrfs_dev_replace_cancel`'s ioctl caller is in S240 ioctl.c (round-43 snapshot), not in S247; the row's "its cancel ioctl" lineage follows R47CritGR2a's assertion, which I verified is consistent with dev-replace.c structure (the function is exported for the ioctl path; only two `btrfs_scrub_cancel` callsites exist) but I did not re-verify the S240 callsite line-by-line.
- Scratch dir `/fast/scratch/hyaku/tsukuroi-r48/GCritAmend` removed on completion after receipts copied.
