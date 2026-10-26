VERDICT: defect-found

Seat ResFixCheck (L2 residual re-check, tsukuroi round 43 / hyaku run 9), item R-FIX — re-check of the post-wave
fixes at `5647d4ff94f5882f99c02d20ec703d0191aea2d9`. All five wave-2 fixes the L1 claims are present and correct
against their pinned sources, and the narrowed entry text passes every content conjunct of the frozen C2 counter;
one low-severity residual defect: the same "SC4's `running` row" mislabel that SkillReview F1 fixed in SKILL.md
survives in the lesson's considerthese paragraph, which now contradicts the corrected SKILL text.

Pinning. Worktree blobs equal tip blobs for SKILL.md and corpus/knowledge/btrfs-scrub-record-r43.md
(`git rev-parse 5647d4ff94f5882f99c02d20ec703d0191aea2d9:<f>` == `git hash-object <f>`, both `89d18aa9…` /
`24702999…`); corpus/lessons/round-43.md DIFFERS in the worktree (uncommitted, L1 in flight: `git status
--porcelain` shows ` M corpus/QUALITY.md`, ` M corpus/lessons/round-43.md`, untracked `residual.ready*`), so the
lesson was read from `git show 5647d4ff94f5882f99c02d20ec703d0191aea2d9:corpus/lessons/round-43.md` (blob
`9cfa3aba…`). All lesson line numbers below are that tip blob. The dispatch commit d950df34 adds only
`.ufo/waves/round-43/residual-dispatch.json`, so tip content equals HEAD content for everything checked. Frozen
scrub.c digest re-measured: `sha256sum .ufo/waves/round-42/frozen/src/scrub.c` →
`48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` — matches the declaration.

Item 1 — SkillReview F1 (superseded `running` row called "SC4's") — fixed, with a residual in the lesson.
- `git diff 64646d6e 5647d4ff -- SKILL.md` hunk 2 (SKILL.md:4009 at tip): "SC1 (the `_tmp` row), SC3 (the
  recording-disabled and "no record" rows) and SC4's `running` row are superseded by the" → "SC1 (the `_tmp` row)
  and SC3 (the recording-disabled, "no record" and `running` rows) are superseded by the".
- Ground truth: the round-42 row being superseded reads `| status `running` | the kernel answered
  `BTRFS_IOC_SCRUB_PROGRESS` for a device (SC3) | the file's mtime says nothing about running |` (SKILL.md:3914 at
  tip) — it carries (SC3). The SC4 rows in the same table cover `no stats available` (:3907), open-errno (:3909),
  `aborted` (:3915), `finished` (:3916) and `interrupted` (:3917) — none is the running row. The fix attributes the
  row to the right SC and still supersedes the SC5-narrowing reading of `scrub_speed_max` (:4009-4012).
- RESIDUAL DEFECT (low): corpus/lessons/round-43.md:91 (tip blob) still says the SKILL section "supersedes the
  round-42 table rows resting on SC1, SC3 and SC4's `running` row" — the same mislabel, now contradicting the
  corrected SKILL.md:4009 (rows resting on SC1 and SC3; `running` under SC3). Neither wave-2 report flagged the
  lesson copy (SkillReview F1 was SKILL-scoped; GateReview Finding 2 flagged the LOG-entry part of the same
  sentence, still open — see Observations). Severity low: a label in prose; no counter conjunct reads it. Not
  addressed by the current uncommitted worktree edit either (that touches only the R43-CAP-HEADER-DUP mistakes row,
  adding a QUALITY-92 reference).

Item 2 — SkillReview F3 (routed-defect item number) — fixed.
- Diff hunk 1 (SKILL.md:3960-3961 at tip): "R42-C1-COUNTER-AMEND item 5 (`corpus/lessons/round-42-verifier-spotcheck.md`
  §6)" → "4 (R42-C1-COUNTER-AMEND), its boot-chain bullet (`corpus/lessons/round-42-verifier-spotcheck.md` §6)".
- Ground truth: `sed -n '195,215p'` of the tip blob of corpus/lessons/round-42-verifier-spotcheck.md — §6 item 4 is
  R42-C1-COUNTER-AMEND and its boot-chain bullet reads "fix the `tools/boot-chain-audit.sh:480-487` `find -quit |
  grep -q` fail-open with a red-before case;"; item 5 is R42-VERDICT-FORM (a C2 item). The citation now matches the
  cited file's own numbering and names the right bullet.

Item 3 — GateReview Finding 1 + Nits A, B — fixed.
- Finding 1 (off-by-one pin): lesson :61 now reads "the extra `scrub_write_buf(fd, buf, ret)` at :869 writes 0
  bytes". `grep -n 'scrub_write_buf(fd, buf, ret)'` on the digest-verified frozen scrub.c → `792:` and
  `869: scrub_write_buf(fd, buf, ret) ||`, with :868 `use->scrub_args.devid) ||`. Pin now exact.
- Nit A (evidence breadth): lesson :81 now reads "(its lines 14 and 31-32 re-read unchanged, `w1/AsmGate.md` §6)" —
  matching the actual evidence scope: `w1/AsmGate.md:13` lists `btrfs-ioctl-surface-r27.md:14,31-32` and `:63` "I
  re-read only the three lines above, not its table". The unsupported whole-file-unchanged claim is gone.
- Nit B (wording): lesson :79 now reads "no ext4 mount: `findmnt -rno TARGET,FSTYPE` lists no `ext4` filesystem —
  its disk mounts are btrfs, vfat and xfs" — no longer asserts the command lists only those three (it also lists
  pseudofilesystems); the operative no-ext4 conclusion is unchanged.

Item 4 — 'Post-wave-2 narrowing' paragraph (lesson :64-70) — quotes scrub.c:1430-1437 correctly.
- `sed -n '1430,1437p'` on `.ufo/waves/round-42/frozen/src/scrub.c` prints, in order: `if (resume && last_scrub &&
  (last_scrub->stats.canceled ||` (:1430), `!last_scrub->stats.finished)) {` (:1431), `++n_resume;` (:1432),
  `sp[i].scrub_args.start = last_scrub->p.last_physical;` (:1433), `sp[i].resumed = last_scrub;` (:1434),
  `} else if (resume) {` (:1435), `sp[i].skip = 1;` (:1436), `sp[i].resumed = last_scrub;` (:1437).
- The lesson's joined quote of :1430-1431 (`if (resume && last_scrub && (last_scrub->stats.canceled ||
  !last_scrub->stats.finished))`) is token-exact (line break normalized); ":1435-1437 (`else if (resume) {
  sp[i].skip = 1; …`)" spans exactly :1435-:1437, the ellipsis standing for :1437. Semantics: the skip branch is
  taken iff there is no `last_scrub` or (finished && !canceled) — exactly the narrowed parenthetical "(`skip` set:
  its record is finished and not canceled, or it has no record)"; the resume branch does engage a canceled record
  even when it is finished, as the lesson says. The out-of-row observation pin is also real: `grep -n
  'sp\[i\]\.resumed->p'` → `1550: sp[i].scrub_args.progress = sp[i].resumed->p;` (lesson marks it "not claimed").

Item 5 — entry diff — only the SR3 parenthetical.
- `git diff 64646d6e5749e0b5b6e458aa0753d39c47404e6b 5647d4ff94f5882f99c02d20ec703d0191aea2d9 --
  corpus/knowledge/btrfs-scrub-record-r43.md`: one hunk, one -/+ pair at :60, inside `## SR3` (:51-96):
  "(`skip` set: its record is finished, or it has no record)" → "its record is finished and not canceled, or it has
  no record)". Nothing else changes. Receipt `item5-entry-diff.diff`.

Nothing new broke.
- Range scope: `git diff --name-only 64646d6e 5647d4ff` outside `.ufo/` lists exactly SKILL.md,
  corpus/knowledge/btrfs-scrub-record-r43.md and corpus/lessons/round-43.md (218 files total; the other 215 are
  wave-2 reports/receipts under `.ufo/waves/round-43/w2/`). No tool code changed in the range, so the C1 kill-rule
  surface is untouched by these fixes.
- Frozen C2 counter executed at the tip, script mode from my scratch (`python3
  …/tools/check-scrub-record-r43.py --revision 5647d4ff… --lane <lane>`; never imported): rows 3, quotes_ok 3 (SR1
  9 good/9 in-window/0 bad; SR3 14 good/13 in-window/0 bad; SR6 10 good/10 in-window/0 bad), props_ok 3, host_ok 3,
  sources_ok 1 (S237/S240/S241 all true), novelty_base_hits 0, pointer_ok 1, verdicts_ok 2 — SR1 holds/holds and
  SR6 holds/holds bound; SR3 rev `holds`, crit `partly`, residual null → verdict FAIL, exit 1. That is exactly the
  declared residual-pending state: the narrowed row passes every content conjunct, and the verdict conjunct waits
  on the counted residual reviewer C2ResSR3's bound `holds`. Receipt `counter-c2-tip-5647d4ff.json`.
- SKILL/lesson diff contains only the four fixes above plus the inserted narrowing paragraph
  (`skill-lesson-diff.diff`); no other sentence in either file moved.

Not done. The round-42 C1 counter and the census selftest were not rerun (heavy; the three-file non-`.ufo` scope of
the range is the basis for skipping, not a rerun). No language server covers this prose subject, so all checks are
text and execution against pinned blobs. No tools installed (none needed); no pacman, no host or lane mutation, no
lane git/jj write (only read-only git: show/rev-parse/hash-object/diff/status/log/grep).

Observations (not item defects).
- GateReview Finding 2 remains open at this tip: the lesson's Closed list still ends "and this round's `LOG.md`
  entry" (tip :92) while `git show 5647d4ff…:LOG.md | grep -ic 'round 43\|round-43'` → 0. Finding 2 was not in this
  item's fix list; recorded as residual risk for round close (the map itself anticipated it, F-6/f).
- Worktree drift: corpus/QUALITY.md and corpus/lessons/round-43.md carry uncommitted modifications and
  `residual.ready*` markers are untracked — the L1's in-flight work. This report is pinned to the tip blobs, not
  the worktree.

Receipts: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-43/residual/ResFixCheck/`
(`item5-entry-diff.diff`, `skill-lesson-diff.diff`, `counter-c2-tip-5647d4ff.json`). Scratch
`/fast/scratch/hyaku/tsukuroi-r43/ResFixCheck` removed at close.
