VERDICT: supports

Seat SkillReview-2, item R-2 (milestone SKILL review), lane tsukuroi round 44 wave w2.
Scope: SKILL.md sections "Scrub-record census arm — round 44" and "Scrub record — round 44 rows"
vs the census header paragraph, the census entry, and both counter docstrings, every table row,
line number and command.

## Base note (read first)

The two sections do NOT exist at the declared integrated tip 8eee79db608b5815c325a5af7cbfdeac50eda9f4;
they were added post-tip in 8728e8bc ("round-44: promotion notes …, SKILL sections and registry table,
lesson draft") and stand at HEAD 3a1c6b5c958c4f289a8b12551f96d843877b700e (working tree clean for
SKILL.md; `git status --porcelain` lists only `.ufo/` wave outputs). All four comparison anchors —
`tools/tsukuroi-census.sh`, `tools/score-scrub-arm-r44.py`, `tools/check-scrub-record-r44.py`,
`corpus/knowledge/btrfs-scrub-record-r44.md` — are byte-identical between 8eee79db and HEAD
(`git diff --stat 8eee79db..HEAD -- <anchors>` is empty). I therefore reviewed the HEAD sections
(SKILL.md:4184-4213 and 4214-4230) against the 8eee79db anchors, which is the only coherent reading of
the item. All evidence in `w2/SkillReview/evidence.md`.

## What was verified (all exact)

Census arm section (SKILL.md:4184-4213):

- `probe_scrub_record` exists (census `tools/tsukuroi-census.sh:1965`), prints exactly one
  `SCRUB btrfs-scrub-record state=…` line, after the STORAGE line (`probe_storage_arm`,
  `:3417-3418`) and before the rollup (`:3423-3430`) — matches "after the STORAGE line and before the
  rollup"; verdict-neutral confirmed (no PLANE/rollup/exit-code change; `main` computes the rollup from
  the six plane verdicts only).
- The contract paragraph "Round-44 addition (C1)" exists at `tools/tsukuroi-census.sh:384` and states
  the same surface, field order, block labels and limits the section summarizes.
- Every table row matches the probe body: state precedence (BLOCKED > RECORDED when
  records+tmp+sockets>0 > NONE, `:2038-2039`); dir absent/present/unreadable with `dir:unreadable`
  (`:1994-1997`); records/tmp/sockets name+stat rules, symlinks and wrong types BLOCKED
  (`:2000-2016`); `unreadable` counts records+tmp only (`:2005,2012`); orphan computed only when sysfs
  is listable (`sysok` gate, `:2007`); `limited` = nonzero single-decimal `scrub_speed_max` with detail
  `<fsid8>:<devid>:speed_max=<v>` (`:1985-1990`); timers skip the bare `btrfs-scrub@.timer` and
  directories (`:2027-2034`); detail = block reasons in traversal order then speed pairs
  (`detail+=$info` at `:2041`), under `local LC_ALL=C` (`:1967`), no name echoed.
- Frontier citations exact: `PROVINCE.md:212-214` is the "Still Frontier" sentence naming the scrub
  record; `corpus/README.md:243` is the Frontier bullet ("becomes Core only after a read-only census
  arm reads it").
- Counter command `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR> [--lane <repo>]`
  matches the docstring Usage line verbatim; sha256 of the file at 8eee79db is
  `1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388` (matches declaration and SKILL).
- Predicate string matches the counter's `PREDICATE` constant verbatim; the four legs described (16
  drawn namespace cases / wired full-census leg / live leg vs independent Python walk / census
  selftest) match docstring legs N/W/L/S.
- "148 cases, sixteen `(R44-C1)` labels": 145 `check` + 3 `check_cli` calls in the selftest
  (census `:2046-3345`) = 148; exactly 16 check labels end `(R44-C1)` (`:3232-3330`); threshold
  `selftest_r44 >= 6` consistent (16 ≥ 6).
- Recorded limits all evidenced: `sysfs:not-directory` in the probe (`:2021`); C1CritEvasion F1 is the
  cached-live-answer defect (`.ufo/waves/round-44/w1/C1CritEvasion.md:26`); C1CritChannels lists
  supplementary groups, cwd/$PWD, stdin, statfs, ancestry as open channels
  (`.ufo/waves/round-44/w1/C1CritChannels.md:13-20`); C1ExecLiveRead strace log exists
  (`.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log`).

Rows section (SKILL.md:4214-4230):

- Header source mapping matches the entry `source:` line (S237 S240 S242 S243 S244 S245; S242/S243/S244
  round-44 frozen, S237 round-42, S240 round-43, S245 host capture).
- Every cited source line was read in the digest-verified pinned snapshots and matches the entry
  quotes: S242 scrub.c 3081/3147/3153/3159/3222/3321/3331/3333/3336/1380/1381; S243 sysfs.c
  72/74/2028/2040/2042/2044/2048; S240 ioctl.c 3132-3133/3139/3141; S237 scrub.c 67-68/421/969/1293/
  1295/1546; S244 timer 5/7/8/11, service 9/10, PKGBUILD 100/101. Snapshot sha256s match the counter's
  pinned constants (all 7 files + capture.txt). Semantics confirmed in context: attach at 3159 precedes
  `scrub_supers`/`scrub_enumerate_chunks`, clear at 3222 follows them; copy-back at 3141 gated on
  `ret == 0` after the 3132-3133 CAP_SYS_ADMIN gate.
- dev-replace citation (701-703,1265-1268) is consistently marked unpinned in both section and entry.
- Limits paragraph matches the entry's Limits section item for item (v7.2.11 pin with the Arch-patch
  [inference] carried from round 43; SR7 source-only; SR9 systemd side systemd.kill(5) [inference];
  replace side unpinned caller).

Adjacent (not in item scope, checked because they name the same counters): registry rows
SKILL.md:4110-4111 — CLIs and predicates match the counter docstrings verbatim; frozen sha256s match;
"candidate census sha256 `fca419b4…`" is the census blob at ab8aae16 (the w1 candidate commit) —
correct; the frozen C1 receipt `.ufo/waves/round-44/after/c1-after-8eee79db.jsonl` is exit 0 with the
same predicate string.

## Findings

No incorrect table row, line number or command found. One precision correction proposed:

F1 (minor, precision): SKILL.md:4217 says "S244 (Arch btrfs-progs 7.1-1 units)" but S244 also
comprises the `PKGBUILD` — the entry's SR9 quotes `S244 PKGBUILD:100-101` and the section's own row 5
("The Arch package, not upstream, ships …") rests on those quotes; the counter's snapshot keys are
`(S244, btrfs-scrub@.timer | btrfs-scrub@.service | PKGBUILD)`.

Proposed exact text (SKILL.md:4217):

- Current: "… S244 (Arch btrfs-progs 7.1-1 units), with S237, S240 and S245."
- Proposed: "… S244 (Arch btrfs-progs 7.1-1 units and PKGBUILD), with S237, S240 and S245."

## Residual risk and verification gaps

- I did not execute either counter (that is the counted seats' measurement); I verified frozen
  hashes, docstring contracts, snapshot digests and one stored receipt instead.
- dev-replace.c:701-703,1265-1268 has no pinned snapshot (declared unpinned) — unverifiable here by
  design.
- The "Arch patch touches no `fs/` file" pin is a declared [inference] carried from round 43, not
  re-measured (entry Limits says so; the section repeats it faithfully).
- The base note above: the sections under review are post-tip work (8728e8bc..HEAD); if the L1 intended
  the review target to be the tip itself, the target did not exist there.
