VERDICT: defect-found

Seat C2EntryDiff, item F-14, wave w2 (round 42 / hyaku run 9). Lane root for every relative path below:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. `record@f50c28d8:L` / `record@78abb8b:L` = `corpus/knowledge/btrfs-scrub-record-r42.md`
at the diff's old/new commits, line numbers from my line-numbered dumps (receipts `C2EntryDiff/record-at-f50c28d.txt`, `record-at-78abb8b.txt`).
Wave-1 reports cited as `.ufo/waves/round-42/w1/<file>:<line>`.

Run exactly as the item prescribes:
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff f50c28d83e1832ecd7eba765caace531f45d6b27 78abb8b5cdc9da511b4fc523e661517a68dd33d3 -- corpus/knowledge/btrfs-scrub-record-r42.md`
→ 111 diff lines, 8 hunks (receipt `C2EntryDiff/diff-f50c28d-78abb8b.md.diff`). `git log f50c28d8..78abb8b -- <file>` shows the
whole change landed in the single integration commit 78abb8b5 ("round-42: integrate w1 (43 seats) … entry corrections
SC1/SC3/SC4/scope/triage …"). Only this one commit in the range touched the file.

**Answer in one line:** all 17 changed sentences are substantive integrations of wave-1 findings and 14 of them trace to a
named proposal, but two changes have no report provenance (the scope softening "whether"→"how far"; the new SC1
progress-socket sentence) and four proposed corrections were not taken (both socket addenda of C2ExecHostRecheck, its SC5
Host-reading replacement, and the CHANGES:469 quote asked by three seats).

## 1. Changed-sentence map

Adoption forms: **verbatim** = proposed text adopted as written; **reworded** = same content, different wording/structure;
**condensed** = content shortened, elements dropped (dropped elements named).

| # | Changed sentence (compressed) | record@f50c28d8 | record@78abb8b | Asked by (wave-1, path:lines) | Form |
|---|---|---|---|---|---|
| 1 | Scope 1st sentence extended: "…SH3, SH4; S129, S139), including the record's name pattern (SH4) and that a scrub run with recording disabled cannot be excluded (SH4 note)." | :9 | :9-10 | C2CritNovelty C1 (`.ufo/waves/round-42/w1/C2CritNovelty.md:125-133`) | reworded — C1 proposed a standalone sentence incl. the S139 pointer; adopted as a clause on the existing sentence, S139 pointer dropped |
| 2 | "how the file is named and replaced" → "how the file is replaced" | :10 | :11 | C2CritNovelty C1 (`C2CritNovelty.md:126-128`) | verbatim |
| 3 | Scope list extended: "…one filesystem verdict, and the per-device throughput limit that same command reports (SC5)." | :11 | :12-13 | C2CritNovelty C1 (`C2CritNovelty.md:127-128`); also closes its §5 SC5-framing caveat (`C2CritNovelty.md:116-119`) | verbatim |
| 4 | "Those decide **whether**" → "Those decide **how far**" | :11 | :13 | **none — flagged U1** | unattributed |
| 5 | SC1: "(the base path plus a dot plus the filesystem UUID**; the name pattern is already held, SH4**)" | :18-19 | :19-20 | C2CritNovelty C6, optional (`C2CritNovelty.md:156-159`) | reworded — proposed " — the name pattern is already held (SH4, `storage-health-r26.md:57`) —"; adopted semicolon clause without the :57 pointer |
| 6 | SC1 mode sentence: "A **record or `_tmp` file** the CLI creates gets mode 0600 **(the `open` mode argument, subject to the umask)**, and every open of **either**…" | :20-22 | :21-24 | C2DraftRevSC1 N1 (`.ufo/waves/round-42/w1/C2DraftRevSC1.md:66-79`) | verbatim |
| 7 | SC1 new closing sentence: "(The progress socket `/var/lib/btrfs/scrub.progress.<fsid>` is a different file, created by `bind`, not covered here.)" | — | :24-25 | **no proposed text — flagged U2** (topic raised: `C2DraftRevSC1.md:66-69`, `C2ExecHostRecheck.md:121`) | new sentence (fact-checked, see §2) |
| 8 | SC3: "when the scrub starts **(or is resumed)**" | :63-64 | :66-67 | C2DraftRevSC3 N1 (`.ufo/waves/round-42/w1/C2DraftRevSC3.md:52`) | verbatim (N1's exact suggested wording) |
| 9 | SC3 new: "A record-write failure later in the run ends the progress writes without that warning; only the final write reports a failure ("failed to record the result")." | — | :70-72 | C2DraftRevSC3 N2 (`.ufo/waves/round-42/w1/C2DraftRevSC3.md:53`) — depth note, no exact text proposed | integrator wording; content verified against frozen src (see §2) |
| 10 | SC3: "through the ioctl **[inference from the write path]**, leaves none. **That conclusion was already held (SH4 note); new here are the mechanism and the disable conditions.**" | :67-68 | :72-74 | C2CritNovelty C4 (`C2CritNovelty.md:149-150`) + C3 (`C2CritNovelty.md:143-147`) | C4 tag verbatim; C3 insertion reworded — drops the `storage-health-r26.md:133` pointer and the word "two"; C3's inline-tag clause superseded by taking C4 |
| 11 | SC4: "any other open failure prints a warning **and the command exits with an error**" | :87-88 | :93-94 | C2DraftRevSC4 F1 (`.ufo/waves/round-42/w1/C2DraftRevSC4.md:83-85`) | verbatim |
| 12 | SC4: "finished only if every device **that has a record in the file** is finished (…; **devices without a record are skipped**)" | :91 | :97-98 | C2DraftRevSC4 F2 (`.ufo/waves/round-42/w1/C2DraftRevSC4.md:86-91`) | verbatim |
| 13 | SC4: "that ended before the scrub did**) [inference]**, not a device error" | :95 | :102 | C2CritNovelty C5 (`C2CritNovelty.md:152-154`) | verbatim |
| 14 | SC4 Host reading rewritten: "…the status summary of this root **prints** `no stats available`: wave-1 seat C2ExecHostRecheck ran `btrfs scrub status /` unprivileged, read-only, exit 0… (…`C2ExecHostRecheck.md` §2); the frozen capture holds the absent directory only." (old: "**would** print…; the command itself was not run") | :111-112 | :118-120 | C2ExecHostRecheck §2 (`.ufo/waves/round-42/w1/C2ExecHostRecheck.md:45-77`) + §6 SC4 replacement (`C2ExecHostRecheck.md:156-162`) | condensed — proposed replacement's `-d -R` per-device line, empty-stderr and "/var/lib/btrfs still absent afterwards" clauses and receipt paths dropped; kept exit-0 + §2 pointer |
| 15 | Triage bullet 1: "Read "no scrub record" as **a gap in evidence (`UNVERIFIED`, SH4)**, not as "never scrubbed" (SC3); **what SC3 adds is the mechanism, not a new verdict**." (old: "as `UNRECORDED`, not `NEVER SCRUBBED` …; the lane's SH4 verdict `UNVERIFIED` for stored data stands.") | :136-137 | :144-145 | C2CritNovelty C2 (`C2CritNovelty.md:135-140`) | condensed — drops C2's "a recording-disabled scrub is already unexcluded at the base (`storage-health-r26.md:133`)" clause and the closing "SH4's `UNVERIFIED` for stored data stands"; "not the verdict" → "not a new verdict"; the fifth-token defect itself is fully removed (`UNRECORDED` now 0 hits in the file) |
| 16 | Triage bullet 2: "a filesystem `finished` needs **every device that has a record** finished" | :138 | :146 | C2DraftRevSC4 F2 triage clause (`.ufo/waves/round-42/w1/C2DraftRevSC4.md:91-93`) | reworded (F2: "it means every device with a record") |
| 17 | Limits bullet 1: "…whose packaging **applies no patch (wave-1 C2ExecLiveSources: `source=()` names the v7.1 tag and no `*.patch`), so the line pins hold for the installed binary**." (old: "whose packaging patches were not compared … (wave item; see the round-42 lesson).") | :146-147 | :154-156 | C2ExecLiveSources §7 (`.ufo/waves/round-42/w1/C2ExecLiveSources.md:144-166`) | condensed — the §7 draft's five-entry `source=()` enumeration, `prepare()` no-op detail, checked-date and tag-identity clauses dropped; core claim + attribution kept (its :160-162 one-line alternative is close to what was adopted) |

Hunks with no changed sentence: none — every hunk maps to ≥1 row above. SC2 and SC5 are untouched by the diff
(SC2 old :39-59 = new :42-62; SC5 old :114-132 = new :122-140), consistent with C2DraftRevSC2's "Proposed replacement
text: None" (`.ufo/waves/round-42/w1/C2DraftRevSC2.md:60-62`) — but see NT3/NT4 for SC5 proposals that were not taken.

Invariant check on the adopted set: no `**Quote.**` line changed anywhere in the diff, and all five frozen proposition
tokens are still present in the new text (`LOCK_EX` record@78abb8b:23, `scrub status:1` :44, `status recording disabled`
:68, `_SCRUB_FS_STAT_MIN` :98, `scrub_speed_max` :124), so the counter's quote/novelty legs see the same bytes as at
f50c28d8 — matching the constraint both proposing reports stated (`C2CritNovelty.md:121-123`, `C2ExecHostRecheck.md:154`).

## 2. Changes no report asked for

- **U1 — record@78abb8b:13, "Those decide whether" → "Those decide how far".** No wave-1 report proposes this wording;
  the only occurrence of "how far" in w1 is the post-integration working-tree snapshot
  `.ufo/waves/round-42/w1/SentScope/scrub-record-workingtree.diff:17`, i.e. the change itself, not a request. It
  coheres with C2CritNovelty's finding that the base already partly holds the conclusion, but it is an unrequested
  editorial weakening of a scope sentence. Content-safe; provenance gap only.
- **U2 — record@78abb8b:24-25, the new SC1 progress-socket sentence.** No report proposed an SC1 sentence: C2DraftRevSC1
  N1 (`C2DraftRevSC1.md:66-79`) proposed only the mode-0600 replacement (its note explains the socket is the reason "a
  file" is too broad) and C2ExecHostRecheck §5(a) (`C2ExecHostRecheck.md:121-142`) named SC1 in the gap but proposed
  addenda for SC3/SC4 only. The sentence is factually consistent with the pinned source: `SCRUB_PROGRESS_SOCKET_PATH`
  at frozen `.ufo/waves/round-42/frozen/src/scrub.c:68`, `bind(prg_fd, …)` at
  `scrub.c:1466` (verified by grep/sed on the frozen snapshot this session). So: unprovenance'd, not untrue. Note it
  also partially covers SC1's side of the C2ExecHostRecheck socket gap, which is why U2 and NT1/NT2 must be read
  together.

## 3. Wave-1 corrections not taken

- **NT1 — SC3 socket addendum.** C2ExecHostRecheck §6 (`C2ExecHostRecheck.md:173-180`) proposed: "While the scrub runs,
  the start process also serves the record stream over that socket, and it does so before the `do_record` test, so a
  scrub with recording disabled still shows live progress in `btrfs scrub status` while leaving no record." + quotes
  `scrub.c:1112` and `:1121`. Absent: the diff adds no SC3 sentence and no quote; SC3 still quotes only
  1502/1336/1507/1121/1200 (record@78abb8b:76-84). The window-compatibility argument that justified the proposal holds
  and was left unused.
- **NT2 — SC4 socket addendum.** C2ExecHostRecheck §6 (`C2ExecHostRecheck.md:164-171`) proposed the socket-before-file
  sentence + quotes `scrub.c:1927`, `:1930`, both inside SC4's frozen window 1925-1945. Absent: SC4's quote block is
  unchanged (7 quotes, record@78abb8b:104-116); the observed socket-ENOENT-then-file-ENOENT trace
  (`C2ExecHostRecheck/scrub-status.strace:22-23`) remains uncited by the entry.
- **NT3 — SC5 Host reading replacement.** C2ExecHostRecheck §6 (`C2ExecHostRecheck.md:182-187`) proposed replacing SC5's
  Host reading with the observed `btrfs scrub limit /` run: the limit column renders 0 as `-` (`scrub.c:2200-2201`),
  sysfs file mode 0644 root:root, read unprivileged / set privileged. Absent: SC5 Host reading is byte-identical
  old :132 = new :140 ("…reads `scrub_speed_max` 0, no limit (capture.txt:9)."). The operator-facing `-`-not-`0`
  surprise documented in `C2ExecHostRecheck.md:88-97` is still unexplained by the entry.
- **NT4 — SC5 `S238` CHANGES:469 quote.** Asked by three wave-1 seats: C2CritNovelty §6 tail
  (`C2CritNovelty.md:178-180`, marked "Minor, outside my item"), C2DraftRevSC5 item 2
  (`.ufo/waves/round-42/w1/C2DraftRevSC5.md:50-51`, "[strengthening] … insert after the CHANGES:468 quote line"), and
  C2ExecHostRecheck §5(b)+§6 (`C2ExecHostRecheck.md:144-146`, `:182-187`). Absent: SC5's quote block is unchanged at
  460/467/468 (record@78abb8b:134-138); the row's "…and `btrfs scrub start` read it and report a set limit" (:125)
  still rests on an unquoted line, exactly the gap all three named.

Guidance with nothing to take in this file: C2ExecHostRecheck §5(c) (`C2ExecHostRecheck.md:148-152`, do not append
status output to the frozen capture) — the capture is untouched, consistent. C2CritControl's proposed docstring text
(`.ufo/waves/round-42/w1/C2CritControl.md:204-208`) targets `tools/check-scrub-record-r42.py`, outside this file's diff.

## 4. Verdict basis and residual risk

Defect-found because the item's two flag conditions both fire: two unprovenance'd changes (§2) and four not-taken
corrections (§3), three of them exact-text proposals designed to be counter-safe. No adopted sentence is false as far as
I could check: spot-verified U2's `bind` claim (`frozen/src/scrub.c:1466`) and row 9's "failed to record the result"
(`frozen/src/scrub.c:1706`; monitor-cycle failure path `goto out` at :1125-1126 without warning), and rows 6/8/11/12/13
are adopted verbatim from reports that verified them against the same digest-pinned snapshot
(scrub.c `48df2e2f…`, CHANGES `bd881ab8…`, per `C2DraftRevSC1.md:9-13`). The dropped condensation elements (rows 1, 5,
10, 14, 15, 17) are pointers and corroborating detail, not load-bearing claims — with one caveat: the base-ground
pointer `storage-health-r26.md:133` that C2/C3 carried was dropped in both places it was proposed (rows 10, 15), so the
integrated entry no longer says *where* the base held SC3's conclusion, only "SH4 note".

Residual risk / what I did not do:
- I did not run `tools/check-scrub-record-r42.py` (wave-2 counted seats own the predicate; also the host is shared). My
  quote/token invariance statements in §1 are textual observations on the diff, not a counter run.
- I did not audit the wave-1 reports' own correctness (their verification is their seats' items); I mapped and, where
  cheap, re-verified the integrated claims against the frozen snapshots.
- I did not check whether some of NT1-NT4 were consciously declined by the L1 outside the reports (no decision record
  was searched beyond this file's diff and the six+four reports named above; the other C2 wave-1 reports
  (SC2/SC5/CritControl/RevCounter/MutCounter) were scanned for record-text proposals — only the ones cited here exist).
- No scratch was needed (no clone/fixture/counter); no tools installed (nothing to record under the 2026-10-19
  authorization); no lane file written except this report and the receipts under `.ufo/waves/round-42/w2/C2EntryDiff/`.
