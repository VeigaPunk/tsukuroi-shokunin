VERDICT: defect-found

# R-3 — falsifying read of the a2w1 integration outside GR2

Seat ResRevGR3Triage (leaf, not counted). Item: the L1's changes outside GR2 at
`194a4523288759b4b73248d1ebcce53e43d0eec7` in `corpus/knowledge/btrfs-scrub-grounding-r45.md` — the added GR3
quote `systemd.kill.xml:115`, the three rewritten `## How this changes OS triage` bullets, the new `## Limits`
bullet, and QUALITY-check item 14. Diff read: `git diff 18389f44…194a4523 -- corpus/knowledge/btrfs-scrub-grounding-r45.md`.
All snapshot digests re-verified first (`sha256sum -c SHA256SUMS` → OK in `frozen/src` for rounds 45/44/42;
`capture.txt` sha256 `f5958a83…` equals the entry front-matter and the S249 row). Receipts:
`.ufo/waves/round-45/a2r1/ResRevGR3Triage/evidence.txt`.

## Findings

**D1 (medium) — `## Limits` bullet: S242's out-of-range list is wrong.** The bullet says the S242 row's declared
ranges "do not list `scrub.c:3081`, 3123-3142 or 3147" (entry :182-184). At `194a4523` `corpus/SOURCES.md:251`
declares `fs/btrfs/scrub.c lines 1365-1385, 3140-3162, 3215-3226, 3321-3337`. Of the six new S242 quotes, `3142`
(`ret = -EIO;`) and `3147` (`if (dev->scrub_ctx ||`) — and the `3139`/`3148`/`3149` pins — sit **inside**
3140-3162; only `3081`, `3123` and `3133` are outside. The claim as written is false for 3140-3142 and 3147
(`a2w1/C2ExecQuotes.md` F1 named only `scrub.c:3081`). The S237 half is true (`scrub.c:421` is outside S237's
declared ranges, F2), and the digest point is true (F1-F2 say digests cover whole snapshots; re-verified here).
Exact replacement text for entry :182-184:

> `Two registrations stay as they are: the S242 row's declared line ranges do not list scrub.c:3081 or 3123-3139
> (scrub.c:3081 is a2w1/C2ExecQuotes.md F1; the new quotes at 3140-3142 and 3147 sit inside the declared range
> 3140-3162), and the S237 row's do not list scrub.c:421; the file digests cover the whole snapshots
> (a2w1/C2ExecQuotes.md F1-F2).`

**D2 (low) — `## Limits` bullet: `C2ResGR2` is not a seat, and "is read" precedes the wave.**
`.ufo/waves/round-45/a2r1-dispatch.json` `taskCall/tasks` names exactly five seats: `ResRevGR2`, `ResCritGR2`,
`ResRevGR3Triage`, `ResRevSkill`, `ResRevAppends`. No seat is named `C2ResGR2`; the GR2 residual seats are
`ResRevGR2` and `ResCritGR2`. Also `194a4523` predates a2r1 delivery (`.ufo/waves/round-45/a2r1/` holds only
`ResCritGR2.md` and `ResRevAppends.md` as I read), so "the corrected row is read" was asserted before any GR2
residual read existed. Exact replacement text:

> `the corrected row is re-read by the residual GR2 seats of wave a2r1 (a2r1-dispatch.json: ResRevGR2,
> ResCritGR2; their reports land at .ufo/waves/round-45/a2r1/).`

**D3 (medium) — QUALITY item 14, criterion 5: pointer resolves to nothing.** Item 14 claims "the round's rejects
sit in `corpus/lessons/round-45.md` `## Gate`". `git show 194a4523:corpus/lessons/round-45.md` → `fatal: path does
not exist`; `git ls-tree` of `corpus/lessons/` (65 files) has no round-45 file. Item 14's own criterion
(QUALITY.md:19, criterion 14) requires the check to "resolve its source/evidence pointers"; this one is
unresolvable at the judged revision — and it is also where QUALITY 61 (QUALITY.md:125, a criterion item 14 skips)
owes the Gate records of this round's new source rows S246-S249. Exact replacement text:

> `5 — not evaluated at this revision: corpus/lessons/round-45.md does not exist at 194a4523; the round's
> rejects and the S246-S249 Gate records (QUALITY 61) are owed in its ## Gate when the lesson lands,`

**D4 (low) — QUALITY item 14, criterion 11: "lands with" has not landed.** Item 14 claims "the LOG.md round-45
entry lands with this entry's integration". `git show 194a4523:LOG.md | grep -n 'round.45\|Round 45\|round-45'`
→ exit 1 (zero hits); `git log -5 194a4523 -- LOG.md` tops at `ae337aab` (round-44 measured outcome). The
integration commit `0503400b` and the evidence commit `194a4523` both contain no LOG.md change, so at the judged
revision the claim is false as written (a promised check is not a performed check, QUALITY 14). Exact
replacement text:

> `11 — deferred: LOG.md at 194a4523 carries no round-45 entry (last LOG.md commit ae337aab, round 44); it is
> owed by the round's final landing,`

## Changes that check out

- **Added GR3 quote `:150`.** Byte-accurate: `systemd.kill.xml:115` in the digest-verified S248 snapshot reads
  `"<constant>SIGCONT</constant>, to ensure that even suspended tasks can be terminated cleanly.</para>"`,
  continuing the quoted `:114` sentence; 115 is inside S248's declared range (SOURCES.md:257, `lines 62-116`).
- **Triage bullet 1 (`:161-163`).** Follows GR1 (`cmdline.c:147` suffix set, `kstrtox.c:29-33` base-0 radix) and
  capture.txt:8 (`mode=644 owner=root`); "root's and a mutation" also matches the host guard; "a bare newline
  ... clears it" restates GR1's parse-as-0/0-means-no-limit.
- **Triage bullet 2 (`:164-167`).** Follows the pinned lines and the row: `scrub.c:3147-3154` returns
  `-EINPROGRESS` on `dev->scrub_ctx` (set unconditionally at `scrub.c:3159` — covers both a plain scrub and the
  replace's copy, whose callers pass `is_dev_replace=true` at `dev-replace.c:701-703`, `:1265-1268`) and on
  `btrfs_dev_replace_is_ongoing` (true for STARTED and SUSPENDED, including umount-suspended per
  `dev-replace.c:1276-1303`). The two sysfs reads are shown unprivileged on this host (`C2ExecHostRecheck.md`
  :84-89: both `-r--r--r--`, read `0`/`none` as uid 1000), and the row's Host reading only claims exclop held on
  the *resume* path (`dev-replace.c:1235` verified — the only `BTRFS_EXCLOP_DEV_REPLACE` site in any pinned
  snapshot; a fresh start's exclop, if any, lives in unpinned `fs/btrfs/ioctl.c`, a residual scope caveat, not a
  defect of this text).
- **Triage bullet 3 (`:168-170`) — keeps systemd's condition.** `systemd.kill.xml:87-97` sends SIGKILL only
  "If processes still remain after: … the delay configured via `TimeoutStopSec=` has passed" (unless
  `SendSIGKILL=`). The bullet now reads "SIGKILL only if a process is still there after the 5 s stop timeout" —
  the earlier unconditional "5 s later, SIGKILL" is corrected, and the host constants (`capture.txt:3`,
  `SendSIGKILL=yes`, `TimeoutStopUSec=5s`, `FinalKillSignal=9`, `KillSignal=2`) are honoured.
- **Item 14 remainder.** 6 and 13 correctly not-applicable (no pacman advice — capture.sh reads the pacman db as
  files, `capture.sh:4-5`; no EACCES triage in the entry). 8 true (header lines :1-3 present; no `[unknown]`
  token — `grep -n unknown` hits prose only). 9 true with a caveat the receipt itself records: the `dropin_owner`
  sweep is bounded in `capture.sh:16-21`, dated `capture.txt:1`, value `capture.txt:5`; `C2ExecHostRecheck.md`
  :71-74 re-ran it via positive controls plus `pacman -Qo` (exit 1, "No package owns") — while its §4 (:123-134)
  notes the grep conflates "unowned" with "glob-matched non-directory" (exit 2), the negative is independently
  established, so the cited support holds. The `fs/`/`lib/` claim still carries `[inference]` (:174-175). 10
  true: the sweep is `a2w1/C2ExecSweep.md` (91 hits over 13 files, F-1..F-6, drafts D1-D3) and its corrections
  landed in the same integration — SKILL.md `### Correction — the round-44 scrub rows` plus round-45 blocks,
  `corpus/README.md:453-467` coverage note (3-column `|Note|Holds|Sources|` table intact),
  `corpus/knowledge/btrfs-scrub-record-r44.md:163-` `## Round-45 qualification — the stop outcome`; apparent
  pipe-count irregularities in the appended SKILL span are escaped `\|` inside cells, not column drift.

## Scoped observations (not defects)

- Item 14's "the criteria not listed above" enumerates only 5-13 of the ~90 criteria; the unaddressed range
  includes 61 (round's source-row Gate records — owed in the same missing `corpus/lessons/round-45.md`, folded
  into D3) and 60/66 (the round's in-place edits — S246 teaches cell, S243 `used_by` — need disclosure in that
  lesson). A literal reading leaves a gap; my named scope was criteria 5, 6, 8, 9, 10, 11, 13.
- The `## Gate status` section added in the same commit is outside item R-3's named changes; its account matches
  the dispatch/results files I read (`a2r1-dispatch.json`, `a2w1-results.json` `output` nulls, both GR2 verdict
  files' first lines `partly`).

## What I did not do

No gate or counter run (`tools/check-scrub-grounding-r45.py`), no re-fetch of upstream URLs (digests checked
locally only), no re-verification of the recovered-yield scoring under `a2w1/L1-recovery/`, no host mutation or
privileged probe. Tools installed/upgraded: none.
