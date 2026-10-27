VERDICT: defect-found

Seat C2RevFinal — item C2-3, wave-2 whole-entry fidelity review of
`corpus/knowledge/btrfs-scrub-record-r44.md` @ 8eee79db608b5815c325a5af7cbfdeac50eda9f4
against the wave-1 pre-reads (`w1/C2DraftCritSR7.md`, `w1/C2DraftCritSR8.md`,
`w1/C2DraftCritSR9.md`, `w1/C2DraftRevAll.md`). This report emits **no `ROW SR* VERDICT:`
line** — verdicts bind only from the counted seats (C2RevSR7/8/9, C2CritSR7/8/9).

Method: `git diff 7e081698d4fc3c4ea944884fd093058de9909de1 8eee79db… -- <entry>` (48 lines,
exactly two hunks — receipt `C2RevFinal/entry-preread-to-tip.diff`); pinned S242/S243 bytes
read from the frozen set at the tip; two read-only fetches at the exact `FETCH.txt` URL
pattern (`fs/btrfs/dev-replace.c`, `fs/btrfs/volumes.c`, tag v7.2.11 — digests in
`C2RevFinal/unpinned-fetches.sha256`). No counter run, no host action, no lane mutation
beyond this report and its receipts.

## 1. What changed after the pre-reads — exactly two hunks

1. SR7 statement sentence 1 rewritten (the C2DraftCritSR7 narrowing).
2. SR8 statement gained a final sentence — the in-memory persistence sentence (§4).

Nothing else in the entry moved; every w1 narrowing target sentence is byte-identical at the
tip, so the w1 proposed texts apply verbatim where still warranted.

## 2. Fidelity of the integrated narrowing (SR7) — faithful, plus one correction

The integrated sentence keeps every load-bearing element of C2DraftCritSR7's proposal, in
condensed form: the biconditional is re-keyed from "exactly while `btrfs_scrub_dev` runs on
it" to "exactly while a scrub or device-replace run is in progress on it"; attach is
line-anchored ("scrub.c:3159 after all refusal checks and before any scrub work"); detach is
placed "before the function's finalize tail"; and "every return path leaves the field as it
found it" is retained. Re-verified against pinned S242 today: the only writers of
`dev->scrub_ctx` are 3159/3222 (grep; reader 3313). The proposal's optional evidence
parentheticals (work anchors 3193/3208; `need_commit` commit 3232-3246) were dropped —
acceptable; no claim was lost by the condensation.

Coordinate fix: the tip cites dev-replace.c "lines 701-703 and 1265-1268"; both w1 pre-reads
said "1265-1267". Fetched bytes (same URL/tag as FETCH.txt) show the second call spans
1265-1268 (`…, false, true);` ends on 1268) and the first 701-703. **The tip is right; both
pre-reads were off by one** — the integration corrected a pre-read error. Receipt
`C2RevFinal/dev-replace-callsites.txt`. Both call sites pass `is_dev_replace = true` on the
source device, so the entry's "source of a running replace" phrasing stays supported.

## 3. Not integrated: all nine w1 narrowings and both tightenings

`git diff` shows none of C2DraftRevAll's N1–N9 landed, nor C2DraftCritSR8's tightening
(base-0 memparse, T/P/E suffixes, `return len`, timeslice anchoring) nor C2DraftCritSR9's two
parenthetical nuances. All nine targets are unchanged at the tip, and all nine grounds were
re-checked and still hold at 8eee79db:

- N1 (medium) — SR8 states unpinned `memparse` suffix semantics as fact. Still unwarranted:
  the frozen set contains only the call site (sysfs.c:2040). Still open.
- N2 (medium) — SR8 host reading attributes fsid `1d02a454-…` to the root filesystem; the
  pinned capture (capture.txt:4, re-read today) never makes that attribution. Still open.
- N3 (medium) — SR9's SIGINT→canceled chain lacks the kernel-side pin (cancel ioctl raises
  `scrub_cancel_req`, scrub ends `-ECANCELED`, progs records `canceled`). I byte-verified the
  proposed quote targets in pinned S242 today: 3285 `atomic_inc(&fs_info->scrub_cancel_req);`
  and 2083 `return -ECANCELED;` (receipts `C2RevFinal/scrub-cancel-3278-3295.txt`,
  `scrub-should-cancel-2077-2083.txt`). Still open.
- N4 (low) — superseded in part: the line numbers the entry kept are now **correct** (§2), so
  "drop the numbers" is no longer required for accuracy; what remains of N4 is that
  `dev-replace.c` is not in the frozen set, so the entry's recheck procedure cannot re-verify
  any number cited for it. The marker's "opened this round … but not pinned" discloses this,
  but "opened" reads as if the file joined the round's frozen set; see P3.
- N5/N6 (low) — triage bullets 3 and 2 still over-broad/over-causal, verbatim as w1 quoted
  them.
- N7 (low) — intro still says the census arm "relies on" SR7. Ground re-verified at tip:
  `tools/tsukuroi-census.sh`'s SCRUB header cites only SR1 and SR6 (:392-393) and never
  consumes the running state.
- N8 (low) — the systemd stop-signal inference is still asserted inline at :95 and in triage
  (:135) with the hedge only in Limits; the entry's own convention (SR7) is an inline
  bracket.
- N9 (info) — `recheck` still re-verifies only the round-44 frozen set; carried S237/S240
  are re-checkable only via the round-42/43 `FETCH.txt`+`SHA256SUMS`.

Given the wave-2 declaration ("Wave 2 verdicts decide the claim"), leaving four medium/low
overreach narrowings unintegrated is the residual defect set of this entry.

## 4. The new SR8 in-memory persistence sentence

Sentence: "The value is in-memory only: written with `WRITE_ONCE` into `struct btrfs_device`
and read with `READ_ONCE`; nothing on this write path persists it, so a single-device
filesystem loses it on unmount and the device's `kzalloc` initialisation restores 0
[inference: no persistence site was found in `fs/btrfs` at v7.2.11; `kzalloc_obj` zeroes the
device allocation]."

- Accurate where pinned: the store body (S243 sysfs.c:2031-2046, receipt
  `C2RevFinal/sysfs-store-2031-2047.txt`) is parse → `skip_spaces` → `-EINVAL` →
  `WRITE_ONCE(device->scrub_speed_max, limit)` → `return len`, so "nothing on this write path
  persists it" is pinned-true; the READ_ONCE readers are already quoted (sysfs.c:2028,
  scrub.c:1380).
- **B1 (medium): the `WRITE_ONCE` claim is load-bearing but unquoted.** The entry's
  convention quotes every load-bearing pinned line; sysfs.c:2045 has no Quote. Fix: P1.
- **B2 (medium): the unmount step is an inference outside the marker's stated grounds.** The
  marker grounds the claim with (i) no persistence site and (ii) `kzalloc_obj` zeroing, but
  the sentence additionally asserts "loses it on unmount", which needs the unpinned premise
  that the device object is freed at unmount. As written the sentence outruns its own marker.
  Fix: P2 (moves the teardown premise inside the bracket and cites the now-verified
  `kzalloc_obj(*dev)` at volumes.c:7470 in `btrfs_alloc_device` — receipt
  `C2RevFinal/volumes-alloc-device.txt`).
- B3 (low, folded into P2): the sentence says "`kzalloc` initialisation" while the marker and
  the real symbol say `kzalloc_obj` — unify.

## 5. Inference-marker sweep — rest of the entry

Beyond N1/N8 and §4, three minor unhedged spots, none blocking:

- Bytes-per-second (SR8 S4) is grounded only by throttle arithmetic; the grounding comment is
  quotable at **S242 scrub.c:1368-1369** ("Throttling of IO submission, bandwidth-limit
  based, the timeslice is 1 / second."). Note w1's O2 cited "scrub.c:1371", which is the
  function signature — second off-by-one in the pre-reads; use P9's coordinates if taken.
- SR9 S2 "so enabling an instance creates a `timers.target.wants/…` link" is generic systemd
  Install semantics, unpinned and unhedged (low; could take an "(systemd Install semantics)"
  parenthetical or join the Limits hedge).
- SR9 S1's negative half "not from btrfs-progs upstream" rests on w1's unpinned upstream-tree
  listing; the pinned half (PKGBUILD:49-50 sources, :100-101 install) is grounded (low).

No other unmarked inference found; all 20 quoted lines remain exact against the pinned
bytes, and the r43 pointer line, `source:` line and host-reading capture references check out.

## 6. Proposed exact text

P1 (B1) — after the `S243` sysfs.c:2044 quote, add:

> **Quote.** `S243` sysfs.c:2045: "WRITE_ONCE(device->scrub_speed_max, limit);"

P2 (B2+B3) — replace the SR8 final sentence with:

> The value is in-memory only: written with `WRITE_ONCE` into `struct btrfs_device` and read
> with `READ_ONCE`; nothing on this write path persists it (store body sysfs.c:2031-2046:
> parse, `skip_spaces`, `-EINVAL`, `WRITE_ONCE`, `return len`), so a single-device filesystem
> loses it on unmount and the device's `kzalloc_obj` initialisation restores 0 [inference: no
> persistence site was found in `fs/btrfs` at v7.2.11; the device object is freed on unmount
> and its `kzalloc_obj` allocation (volumes.c:7470, unpinned) is zeroed at creation].

P3 (N4 remnant) — replace the SR7 inference bracket with:

> [inference for the replace side: its caller is in `fs/btrfs/dev-replace.c`, fetched this
> round at v7.2.11 — lines 701-703 and 1265-1268, both call sites passing `is_dev_replace =
> true` on the source device — but not pinned, so the recheck procedure cannot re-verify
> these numbers]

(N4's original drop-the-numbers variant remains an acceptable alternative.)

P4 (N1, verbatim from w1, target unchanged) — replace the memparse sentence with:

> Writing parses the text with `memparse` [inference: `memparse`'s size-suffix table —
> `K`, `M`, `G` — is defined outside the pinned files], skips trailing whitespace including
> the newline (sysfs.c:2041's own comment: "There could be trailing '\n'"), and rejects
> anything else after the number with `-EINVAL`.

P5 (N2, verbatim from w1) — replace the SR8 host-reading line with:

> **Host reading.** The only btrfs sysfs shows on this host (fsid
> `1d02a454-c549-4a35-b567-89d60902af8e`, devid 1 — `findmnt -no UUID /` names the same
> fsid for `/`; the attribution is not in the pinned capture) has `scrub_speed_max` mode
> 644, owner root, value 0: no limit (capture.txt:4), read as uid 1000 with no effective
> capabilities (capture.txt:1).

P6 (N3, quote targets byte-verified by this seat today) — after the `S237` scrub.c:969 quote
add:

> **Quote.** `S242` scrub.c:3285: "atomic_inc(&fs_info->scrub_cancel_req);"
>
> **Quote.** `S242` scrub.c:2083: "return -ECANCELED;"

and replace "the foreground start installs a SIGINT handler that issues
`BTRFS_IOC_SCRUB_CANCEL`, so a SIGINT sent to it" with:

> the foreground start installs a SIGINT handler that issues `BTRFS_IOC_SCRUB_CANCEL` —
> the kernel cancel path raises `scrub_cancel_req`, which makes the running scrub end with
> `-ECANCELED` (S242 scrub.c:3281-3293, 2077-2083), the value the start ioctl returns — so a
> SIGINT sent to it

P7 (N8, verbatim from w1) — inline-mark the systemd inference:

> :95 — "so a SIGINT sent to it (the service's stop signal [inference: systemd.kill(5), see
> Limits]) cancels the running scrub, …"
> :135 — "Stopping a running scrub service sends SIGINT (see Limits) and so cancels the
> scrub and leaves a canceled, resumable record (SR9, SR3)."

P8 (N5/N6/N7/N9, verbatim from w1 — targets byte-unchanged at tip): apply the four
replacements as written in `w1/C2DraftRevAll.md` (triage bullets 3 and 2; intro
"relies on" → "that ground what … reads and refuses to read"; recheck carried-sources
clause). N7's census ground re-verified at tip (:392-393 cite SR1/SR6 only).

P9 (optional) — quote the timeslice comment (corrected coordinates):

> **Quote.** `S242` scrub.c:1368: "Throttling of IO submission, bandwidth-limit based, the
> timeslice is 1"

(comment spans S242:1368-1369; w1's O2 line 1371 is the function signature.)

Priority for integration: P1+P2 (new sentence hygiene), then N3/P6, N2/P5, N1/P4, N8/P7,
then P3 and N5/N6/N7/N9. All are text-only narrowings; none touches a claim the C1 arm or
the frozen counter depends on.

## 7. Counter impact

Every proposal preserves the frozen counter's PASS structure at the tip: added quotes
(P1, P6, P9) are byte-substrings of pinned files (bad stays 0; in-window ≥1 already satisfied
by existing quotes); P2/P4/P6/P7 keep all per-row props tokens (`scrub_speed_max`, `0644`,
`memparse`, `EINVAL`, `no limit`; `btrfs-scrub@`, `OnCalendar=monthly`, `Persistent=true`,
`KillSignal=SIGINT`, `-B`, `BTRFS_IOC_SCRUB_CANCEL`; SR7 tokens untouched); P5 keeps the
capture.txt references; P8's recheck clause is outside `sources_ok`'s `source:`-line check.

## 8. Residual risk and verification gaps

- No scrub, sysfs write, unit change or privileged probe was run (forbidden for this seat);
  SR7 remains source-only, as the entry declares.
- dev-replace.c and volumes.c are unpinned; my verification is a same-tag fetch today
  (digests recorded), not a frozen-set recheck — exactly the gap P3 discloses.
- The frozen counter was not run by this seat; its PASS at 8eee79db is taken from the
  declaration and the textual conjunct analysis in §7.
- w1 line-coordinate drift was found in two places (dev-replace.c 1265-1267→1268, corrected
  at the tip; O2's 1371→1368, corrected here). Other w1-cited unpinned coordinates
  (S237:1704, S242:1370-1372, volumes.c) were not all re-walked; P6's coordinates were.

Receipts: `.ufo/waves/round-44/w2/C2RevFinal/{entry-preread-to-tip.diff,
unpinned-fetches.sha256, sysfs-store-2031-2047.txt, scrub-cancel-3278-3295.txt,
scrub-should-cancel-2077-2083.txt, dev-replace-callsites.txt, volumes-alloc-device.txt}`.
