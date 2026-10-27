VERDICT: defect-found

# C1-R6 — Amendment fidelity attack on GR2 (round 47, wave w1)

Seat: C1CritAmend. Target: diff of `corpus/knowledge/btrfs-scrub-grounding-r45.md` between base
`916019057147d7e9ba6b137647b2cee26decf4b8` and freeze `77e9e2b2e96b85d8f048ae2087e246a542b71611`,
limited to `## GR2` and `## Limits`, against the round-46 counted residual critic's corrections
(`.ufo/waves/round-46/r1/V46ResCritGR2.md`, bound verdict `ROW GR2 VERDICT: partly`).

## 1. Diff scope — clean, no out-of-bounds edits

Command: `git -C <lane> show <base>:corpus/knowledge/btrfs-scrub-grounding-r45.md > base-gr.md`,
same for freeze; `diff -u base-gr.md amended-gr.md` (receipts in seat dir). Observed hunks, exactly three:

1. GR2 **Statement** body (base lines 57-76 region): fs-closing sentence inserted, ordering rewritten,
   suspend sentence replaced.
2. GR2 **Quote** list: two quotes added — `S242` scrub.c:3094 and `S242` scrub.c:3095 (still inside
   `## GR2`; amended file headers: `## GR2` at line 55, `## GR3` at line 141).
3. `## Limits`: one bullet added recording the round-47 amendment provenance.

No other section touched. Amendment stays inside the item's declared scope.

## 2. Fidelity to the counted corrections — both applied verbatim, no drift, no weakening

Correction 1 demanded (V46ResCritGR2.md line 5, quoting the row's own text): the row must state that
after the filesystem-closing check, `btrfs_scrub_dev` allocates its context and acquires workers,
setup/worker errors return first, then device checks, then EINPROGRESS refusals. The amendment's
sentence: "after a filesystem-closing check that returns `-EAGAIN` first (`btrfs_fs_closing`), the
function allocates its scrub context and takes the scrub workers (`scrub_setup_ctx`,
`scrub_workers_get`), whose errors return first; then three device checks answer: … Only after those
checks is a call with `is_dev_replace` false refused with `-EINPROGRESS` while
`btrfs_dev_replace_is_ongoing` is true …" — faithful, adds no claim beyond the correction.

Correction 2 demanded (V46ResCritGR2.md line 8): narrow to exactly "When the unmount suspend path
runs, it calls `btrfs_scrub_cancel`; once the scrub returns and clears its context, the progress
query returns `-ENOTCONN`." The amendment applies this verbatim, including dropping the old
immediate-cancellation framing ("A suspended replace requests the cancellation of its scrub").

No weakened wording that still overreaches was introduced elsewhere; the pre-existing clauses the
critic accepted (replace-start/continuation parameters, three device checks and their order,
ongoing-state consequence conditioned on present/writeable/metadata/not-target, "While the copy
runs" progress phrasing) are unchanged.

## 3. Per-clause re-verification of the new Statement against pinned sources

Sources verified: `sha256sum -c SHA256SUMS --ignore-missing` in both frozen dirs → scrub.c OK
(round-44), dev-replace.c OK (round-45).

- **C-A (new fs-closing clause): "after a filesystem-closing check that returns `-EAGAIN` first
  (`btrfs_fs_closing`)".** SUPPORTED. scrub.c:3094-3095 (pinned, verified by `awk` line dump):
  3094 `if (btrfs_fs_closing(fs_info))`, 3095 `return -EAGAIN;`. Both new row quotes are byte-exact
  against those lines. The check is the first control-flow test in `btrfs_scrub_dev`'s tail after the
  `last_physical` fallback (scrub.c:3090-3092).
- **C-B (ordering): context allocation + worker acquisition, "whose errors return first".** SUPPORTED.
  scrub.c:3109-3116: `sctx = scrub_setup_ctx(...)` at 3109, `if (IS_ERR(sctx)) return PTR_ERR(sctx);`
  3110-3111; `ret = scrub_workers_get(fs_info);` 3114, `if (ret) goto out_free_ctx;` 3115-3116. Both
  precede the device-list lock at 3118.
- **C-C (three device checks, stated order -ENODEV / -EROFS / -EIO).** SUPPORTED. scrub.c:3118-3144:
  unknown-devid or missing-on-non-replace → -ENODEV (3120-3125); non-writeable on non-replace,
  non-readonly → -EROFS (3127-3135); outside metadata or replace target → -EIO (3137-3144).
- **C-D (EINPROGRESS refusals "only after those checks").** SUPPORTED. scrub.c:3146-3154:
  `down_read(&fs_info->dev_replace.rwsem)` 3146, `if (dev->scrub_ctx || (!is_dev_replace &&
  btrfs_dev_replace_is_ongoing(...)))` 3147-3149, `ret = -EINPROGRESS;` 3153.
- **C-E ("which it is for a replace in state started or suspended (a replace suspended by an unmount
  still counts)").** SUPPORTED. dev-replace.c:1279-1298 (`btrfs_dev_replace_is_ongoing`): returns
  false for NEVER_STARTED/FINISHED/CANCELED, true for STARTED and SUSPENDED; comment at 1290-1296
  explicitly covers the umount-suspended, tgtdev-missing-degraded case.
- **C-F (amended suspend sentence, first half): "When the unmount suspend path runs, it calls
  `btrfs_scrub_cancel`".** FALSIFIED against the pinned source. The unmount suspend path is
  `btrfs_dev_replace_suspend_for_unmount` (dev-replace.c:1171-1195); its full body — switch over
  replace_state, sets SUSPENDED at 1185-1186, logs "suspending dev_replace for unmount" at 1189 —
  contains **no** `btrfs_scrub_cancel` call. The only two `btrfs_scrub_cancel` calls in the pinned
  dev-replace.c are at 1111 and 1144, both inside `btrfs_dev_replace_cancel` (function spans
  1085-1169): 1111 cancels a STARTED replace, and 1143-1144 is the SUSPENDED-state case of the cancel
  ioctl ("/* Scrub for replace must not be running in suspended state */ / btrfs_scrub_cancel(fs_info);"),
  i.e. canceling an already-suspended replace. The amendment — like the round-46 critic it quotes —
  misattributes the 1143-1144 call site to the unmount suspend path. Faithful transcription of the
  correction, but the correction itself is factually wrong about the code; the row now asserts as
  positive fact something the pinned source contradicts.
- **C-G (amended suspend sentence, second half): "once the scrub returns and clears its context, the
  progress query returns `-ENOTCONN`".** SUPPORTED. scrub.c:3332-3336 (`btrfs_scrub_progress`):
  `if (sctx) memcpy(...)` 3332-3333; `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` 3336. Timing
  qualifier ("once the scrub returns and clears its context") is correctly preserved.
- **C-H (unchanged "While the copy runs … privileged progress query … answer 0" and the SR7
  inference bracket).** Unchanged from base; not a correction target; no new issue introduced by the
  amendment.

## 4. Smallest safe correction

Replace the first half of the amended suspend sentence with the true call site, keeping the
critic's accepted second half:

> "When a suspended replace is canceled, the cancel path calls `btrfs_scrub_cancel`
> (dev-replace.c:1143-1144); once the scrub returns and clears its context, the progress query
> returns `-ENOTCONN`."

This removes the false "unmount suspend path" attribution, stays inside what dev-replace.c:1143-1144
and scrub.c:3332-3336 actually pin, and preserves the narrowing intent (no claim that every
suspension requests cancellation). The L1 should also treat the round-46 residual critic's
"unmount suspend path" gloss of 1143-1144 as itself erroneous, so the row's quote citation stays
at 1143-1144 but the surrounding sentence must not call it the suspend path.

## 5. Impacted axes

- **C1 / GR2 depth:** the amended row cannot be admitted as-is; clause C-F is false against pinned
  bytes. The fs-closing correction (C-A..C-E) is sound and quote-exact, so this is one defective
  clause, not a wholesale rejection of the amendment.
- **Provenance:** the round-46 `partly` verdict's proposed wording encoded a code-reading error that
  verbatim application amplified into a positive false claim — a fixable defect, not a tradeoff the
  judge must accept.

## 6. What I did not do

Did not re-run `tools/check-scrub-admission-r47.py` (counter verification is the counted seats'
item, and my finding concerns clause truth, not bind mechanics). Did not inspect sysfs.c/capture.txt
claims (outside this item). Did not run the census selftest (unrelated to C1-R6).
