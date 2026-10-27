VERDICT: defect-found

# LessonCrit — R-4, Mistakes rows in `corpus/lessons/round-44.md`

Scope check on the pinned target first: `corpus/lessons/round-44.md` **does not exist at the pinned tip**
`8eee79db608b5815c325a5af7cbfdeac50eda9f4` (`git ls-tree 8eee79db -- corpus/lessons/` lists round-1…43 only). It was
added two commits later at `8728e8bc` (unchanged at HEAD `3a1c6b5c`; `git log --follow` → one commit). I checked the
committed text as it stands at HEAD = `8728e8bc`'s version; every row citation below is
`corpus/lessons/round-44.md:42-48`.

## Row-by-row grounding

### R44-L1-FLEET-ROOT-FIXTURE — grounded, two nits

- The stray is real and quarantined: `.tower/quarantine/fleet-root-strays-20261026T2114/` holds exactly
  `fx/A2-uppercase-fsid-sysfs/sysfs/11111111-2222-3333-4444-555555555555/devinfo/1/scrub_speed_max`, with
  `TREE.txt` + `SHA256SUMS`; fleet commit `685f7b36` (21:11 -03) records the orchestrator notice and says "bytes
  unchanged". The seat disclosed it (`w1/C1ExecEdgeNames.md:243-256`); `git -C fleet status --porcelain` is clean
  today. "Able to fail" (porcelain red at notice, empty at close): the ledger side is the recorded quarantine +
  status; real.
- **Nit 1:** "orchestrator notice 2026-10-26T21:14Z" — every other timestamp on this host is local (-03; commit times,
  fleet commit `685f7b36` = 21:11 -03). "Z" is almost certainly the quarantine dir name read as UTC. Propose
  `2026-10-26T21:14-03` (or "the T2114 quarantine").
- **Nit 2 (source artifact, not the row's claim):** the seat report and `SentMisroot`'s F3 both write "(4 bytes,
  `0\n`)". The quarantined file is **2 bytes** (`wc -c` = 2; `xxd` = `30 0a`; its `SHA256SUMS` entry `9a271f2a…`
  equals `echo "0" | sha256sum`). "4 bytes" is wrong in both w1 reports; the row does not quote it, but the fix cell
  can carry the correct size.

### R44-L1-TIMERS-BRANCH — event real; the artifact anchoring is loose

The incident happened exactly as described, in the worktree during the wave-1 repair session (L1 transcript
`TsukuroiR44.jsonl`): at 00:42:36Z a "Cleaning duplicated block" edit moved `for e in "$tw"/btrfs-scrub@*.timer`
inside the unreadable-wants branch (`timers=0` for enabled instances); `bash tools/tsukuroi-census.sh --selftest`
printed `FAIL (148 cases, 147 passed, 1 failed)` at 00:47:43Z — case 138 `scrub-timers` — plus a direct probe
`timers=0` at 00:46-47Z; the restore edit landed 00:48:21Z and selftest printed
`PASS (148 cases, 148 passed, 0 failed)` at 00:48:52Z. Able-to-fail: REAL (FAIL→PASS observed, before→after).
Two grounding caveats worth one clause each:
- The buggy state **never landed in git**: every committed version of `probe_scrub_record` (`ab8aae16`, `071ab0d1`,
  `9608ebc3`, `8eee79db`, plus sibling commits `b67c7847`/`407e7c08`) already has the loop in the `else` branch.
  The FAIL exists only in the L1 transcript and scratch, not in a preserved receipt.
- Commit `9608ebc3` ("fix timers branch (loop moved to listable-branch; unreadable wants blocks)") carries a
  **message-vs-diff mismatch**: its parent-diff is only the `sysfs:` `-d` guard at `:2018-2020` (the fix for the
  `sysfs-unreadable` case's double detail `sysfs:unreadable,sysfs:not-directory`, see
  `after/c1-after-071ab0d1.jsonl` wrong[]). The message describes the worktree repair, which netted to zero because
  `071ab0d1` already held the correct loop. A reader checking the commit cannot find the named fix in it.

### R44-W1-UNREPORTED-SEATS — material misattribution (the required content is present but wrong)

Both names and the "round-43 path" appear, but the reconstruction claim is false for C1MutArm and conflated for
SentMisroot:

- **C1MutArm.md is the seat's own file, not an L1 reconstruction.** Transcript `C1MutArm.jsonl` entry 217-219:
  `write /home/.../w1/C1MutArm.md` at 00:43:01Z → "wrote 9559 bytes". Byte-for-byte comparison of the transcript's
  `arguments.content` with `git show 8eee79db:.ufo/waves/round-44/w1/C1MutArm.md` → **identical (9559 B)**. The seat
  wrote its report; what was missing was only the *commit* (the file landed at `8eee79db`, after `071ab0d1`).
  "reconstructed by the L1 … byte-exact final texts" is therefore wrong here: there is nothing to reconstruct.
- **SentMisroot is a three-party collision, not a no-report seat.** Transcripts show `SentMisroot` (round-43 X-5
  seat, yielded 22:24Z at r43) woke during r44, verified the pyc finding, and produced a late addendum whose text is
  preserved verbatim in `/fast/scratch/hyaku/tsukuroi-r44/L1/sentmisroot-final.txt` — naming
  `.ufo/waves/round-43/w1/SentMisroot.md` (the r43 path; that seat's own report path, so not a typo in context).
  The L1 path-corrected it (44 for 43) and committed it as the 5-line stub in `071ab0d1`. The **r44** seat
  `SentMisroot-2` then wrote the real `w1/SentMisroot.md` itself (transcript: write 00:44:27Z + edits → yield
  00:46:06Z), appending the stub verbatim in its "## Appendix — name collision" — the committed `8eee79db` text is
  that seat's file, not an L1 reconstruction. (It even mis-attributes the stub to "a second X-5 seat".)
- The ledger half of the able-to-fail cell stands: `w1-results.json` lists both seats with parsed, verdict-bearing
  outputs and both `.md` files exist. What fails is the sentence "both reconstructed by the L1 … (byte-exact final
  texts, path-corrected)" — for C1MutArm nothing was reconstructed, and for SentMisroot the reconstruction is only
  the stub inside the seat's appendix.
- Unverifiable from artifacts: whether `C1MutArm`'s `mut-*.json` receipts are "the seat's" (they are, committed at
  `071ab0d1`) — the row's receipt claim is fine; only the report-file story is wrong.

### R44-C2-SR7-REPLACE-OMISSION — misquotes the draft and aims the able-to-fail at the wrong sentence

- **Misquote:** the row says "The first SR7 draft said a context is attached exactly while `btrfs_scrub_dev`
  runs". The actual first draft (`git show ab8aae16:corpus/knowledge/btrfs-scrub-record-r44.md`) said: "a scrub
  runs on a device exactly while that device carries a scrub context". The row quotes the *narrowed* sentence of
  `7e081698` as if it were the buggy original.
- **Able-to-fail is inverted.** `w1/C2DraftCritSR7.md:15,28` — the [3159,3222] window check — **fails the
  `7e081698` sentence** ("context exactly while `btrfs_scrub_dev` runs": pre-attach validation and the post-detach
  `need_commit` tail run with `scrub_ctx == NULL`) but by the critic's own reading **holds the first-draft
  sentence** (context-carried ⇔ actively scrubbing is exactly [3159,3222]). So "the pre-narrowing sentence fails
  the window check" cannot demonstrate the replace-omission; it demonstrates the *overreach the fix itself
  introduced*. The real sequence: omission (draft) → fix added the replace branch but overshot the biconditional →
  second narrowing (`071ab0d1`, now reading "exactly while a scrub or device-replace run is in progress on it")
  restored it. `C2ExecKernelSR7` also returned `VERDICT: defect-found` (w1/C2ExecKernelSR7.md:1), so
  "C2ExecKernelSR7/C2DraftCritSR7 confirmed the invariant" overstates — they confirmed attach/clear/no-mid-return
  and the call-site coordinates; the first still found a defect.
- Captured-by "none — a pre-freeze self-check" is correct for the replace branch (ScribeLesson measured that no
  counter token names it: `w1/ScribeLesson/sr7-props-gap.json`; dev-replace.c coordinates verified by
  C2DraftCritSR7 :17-21). But the row should say so without claiming the seats "confirmed" the wording.

### R44-C2-CONTROL-K17-CATCH — real draft defect, wrong fix-status and no preserved unfixed counter

- The defect is real in L1's transcript (`TsukuroiR44.jsonl` ~23:57-58Z): draft code was
  `src['source_line'] = all(re.search(rf'\b{s}\b', srcline) for s in (...))` — a whole-line substring check; the
  fix to the leading-list parse is recorded. But **no artifact preserves the unfixed counter**: all four git
  objects carrying `tools/check-scrub-record-r44.py` (`1d2afffe`, `368920a9`, `771a2743`, `d6e7315c`) are the same
  sha256 `c96aeda9…` already containing `lead = re.match(r'source:\s*((?:S\d{3,}[\s,]*)+)', srcline)`.
- Therefore "the pre-data control K17 … FAILed **only after the counter was fixed**" is ungrounded: the frozen
  receipt `controls/C2-K17.jsonl` (`{"control":"K17","expect":"FAIL","exit":1}`, `source_line:false`,
  `sources_ok:0`) ran on the committed — already leading-list — counter; no run of K17 against the substring draft
  exists in the repo. The battery never observed the defect; it guards its fix.
- "Able to fail: control C2-K17 is red on the unfixed counter" is **not demonstrable** — there is no unfixed
  counter to point at. What is demonstrable (and what ScribeLesson recommended writing): K17 is red *on the*
  counter (`C2-K17.jsonl`) and `w1/ScribeLesson/k17-parse.txt` shows a substring-anywhere variant would go green —
  the fix is able to fail via its control, but the row must not claim a landed change it cannot cite.

## Proposed text

Replace the three defective rows (and one timestamp nit in row 1) as follows; IDs kept:

```
| R44-W1-UNREPORTED-SEATS | delivery | At wave close two report paths needed L1 recovery, for different reasons: (a) `w1/C1MutArm.md` was written by the seat itself (transcript: 9559 B write at 00:43Z) but stayed uncommitted until `8eee79db` — the seat settled while its report file was uncommitted, and the committed text is the seat's byte-identical; (b) the parked round-43 `SentMisroot` seat woke during w1 and yielded a final text naming `round-43/w1/SentMisroot.md` (captured in `/fast/scratch/hyaku/tsukuroi-r44/L1/sentmisroot-final.txt`); the L1 path-corrected and committed it as a 5-line stub at `071ab0d1`; the w1 `SentMisroot` seat then wrote `w1/SentMisroot.md` itself and preserved the stub verbatim in its appendix (name collision) | round prompt §4/§6 (every seat settles with a committed report) | The L1 committed both files at `8eee79db`; the wave's results ledger lists both seats with parsed verdict outputs, and both .md files exist |
| R44-C2-SR7-REPLACE-OMISSION | depth-overreach | The first SR7 draft (`ab8aae16`) said "a scrub runs on a device exactly while that device carries a scrub context", omitting the device-replace caller; the pre-w1 narrowing added `is_dev_replace` (dev-replace.c:701-703,1265-1268, honest [inference]) but overshot to "context exactly while `btrfs_scrub_dev` runs" — a literal overreach `C2DraftCritSR7` failed on the [3159,3222] window (pre-attach and the `need_commit` tail run without a context), and `C2ExecKernelSR7` still returned defect-found | none — a pre-freeze self-check (the L1 read dev-replace.c); no counter token names the replace branch (w1/ScribeLesson/sr7-props-gap.json) | Second narrowing integrated at `071ab0d1` ("exactly while a scrub or device-replace run is in progress on it"). Able to fail: the overreaching `7e081698` sentence fails C2DraftCritSR7's window check; the first draft's fault is the omission the fix repaired |
| R44-C2-CONTROL-K17-CATCH | calibration | While drafting the C2 counter pre-commit, the `source:` conjunct searched the whole line (`all(re.search(\b{s}\b, srcline))`), so an S-id named only in prose satisfied it; only the L1 transcript preserves the draft — every committed copy is the leading-list parse | none — caught in pre-commit drafting; K17 was authored to hold the line | The counter ships with the leading-list parse (`:335-338`). Able to fail: control C2-K17 (S244 dropped from the lead list) is red on the counter — `controls/C2-K17.jsonl` exit 1, `source_line:false` — while `w1/ScribeLesson/k17-parse.txt` shows a substring-anywhere check on the same bytes would pass, i.e. K17 separates the two implementations |
```

Row 1: change `2026-10-26T21:14Z` → `2026-10-26T21:14-03 (T2114 quarantine)`. Row 3: append to Fix cell —
`(the buggy tree never committed; the FAIL/PASS pair is in the L1 transcript at 00:47:43Z/00:48:52Z; `9608ebc3`'s
parent-diff carries only the sysfs `-d` guard, so its message describes the worktree repair, not the committed
delta)`.

## Verdict

Two of five rows (fleet-root, timers-branch) describe real events with real able-to-fail demonstrations; three
(unreported-seats, SR7-replace, K17-catch) carry misattributed or undemonstrable claims, and the SR7 row's
able-to-fail points at the wrong sentence. The required misroot and both seat names do appear. `defect-found`.

## Tooling
None installed; pacman untouched. Reads only: lane git history/objects, fleet `git status`, quarantine receipts,
`w1-results.json`, and transcripts under `~/.omp/agent/sessions/` (C1MutArm, SentMisroot, SentMisroot-2,
TsukuroiR44). Scratch: `/fast/scratch/hyaku/tsukuroi-r44/LessonCrit/` (extracted comparison copies; removed on
exit). No counter/selftest was re-run; the FAIL→PASS pair cited is from the L1 transcript.
