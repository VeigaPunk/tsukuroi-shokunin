# Round 68 — lesson (tsukuroi)

author: seat SC2Scribe (scribe), round 68 wave w1
date: 2026-11-03
basis: lane base `42400ec6`, declaration frozen in `SCORECARD.md` "Round 68 - declaration";
pinned bytes `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-68/before/src/`
(access date 2026-11-03; `SHA256SUMS` and `FETCH.txt` in that directory).

Command base: every `$` line below was run from this lane root,
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. `before/src/` is the shorthand for
`.ufo/waves/round-68/before/src/`; a `before/src/…` operand was executed as that full path (or with the
command run from inside that directory; both forms give the same output), and the sha256 lines below show the
full `.ufo/…` spelling. Commands over `corpus/…` also ran from the lane root.

## Gate

**Trigger.** The QUALITY 98 upstream watch fired on Linux v7.3 —
`$ sed -n '1p' before/src/FETCH.txt` → `round-68 pre-declaration fetches (L1, 2026-11-03, QUALITY 98 watch fired on Linux v7.3)` (rc 0).
The watch's method is recorded in that file: `curl -s --max-time 60 -o <file> <url>` per tag, then
`sha256sum` over the saved bytes.

**Candidates considered.**

1. Linux v7.3 `Documentation/admin-guide/cgroup-v2.rst` —
   `$ cmp before/src/v72-Documentation_admin-guide_cgroup-v2.rst before/src/v73-Documentation_admin-guide_cgroup-v2.rst`
   → `differ: char 43698, line 1133` (rc 1); `$ diff -u before/src/v72-Documentation_admin-guide_cgroup-v2.rst before/src/v73-Documentation_admin-guide_cgroup-v2.rst | grep -c '^@@'` → `16` (rc 0).
   **Admitted** as S286.
2. Linux v7.3 `fs/btrfs/sysfs.c` —
   `$ cmp before/src/v72-fs_btrfs_sysfs.c before/src/v73-fs_btrfs_sysfs.c` → `differ: char 37180, line 1339` (rc 1);
   `$ diff -u before/src/v72-fs_btrfs_sysfs.c before/src/v73-fs_btrfs_sysfs.c` → one hunk `@@ -1336,7 +1336,7 @@`, the comment line only (rc 1). **Admitted** as S287.
3. Linux v7.3 `mm/oom_kill.c` — `$ cmp before/src/v72-mm_oom_kill.c before/src/v73-mm_oom_kill.c` → rc 0 (identical).
   **Rejected**: a v7.3 row would repeat the v7.2-pinned S149/S182 bytes with no new authority.
4. Linux v7.3 `Documentation/accounting/psi.rst` — `$ cmp before/src/v72-Documentation_accounting_psi.rst before/src/v73-Documentation_accounting_psi.rst`
   → rc 0 (identical). **Rejected**: same bytes as S185, and S185 is already `rejected` in the registry as an exact
   duplicate of S115 (`$ grep -n '^| S185 ' corpus/SOURCES.md` → `191:`, status cell `rejected`; rc 0).
5. btrfs-progs v7.3 `CHANGES` — `$ grep -n '^| S285 ' corpus/SOURCES.md` → `295:` (rc 0). **Rejected**: the file is
   already registered as S284/S285 in round 67.
6. systemd v262.1 — `before/src/FETCH.txt` records `systemd/systemd releases/latest: v262.1 (published 2026-10-16) — host
   systemd 262.1-1 (no delta)`. **Rejected**: no delta below the host, and outside the round's Linux v7.3 scope.

**Admitted rows** (drafted in `.ufo/waves/round-68/drafts/c1/sources-rows.md`, NF 13 each; the L1 appends them
after `corpus/SOURCES.md:295`):

- **S286** — Linux v7.3 `Documentation/admin-guide/cgroup-v2.rst`,
  URL `https://raw.githubusercontent.com/torvalds/linux/v7.3/Documentation/admin-guide/cgroup-v2.rst`,
  access date 2026-11-03, kind `docs`, tier A, anchor v7.3 lines 1501, 1535 and 1545, raw bytes
  sha256 `2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68` (re-computed:
  `$ sha256sum .ufo/waves/round-68/before/src/v73-Documentation_admin-guide_cgroup-v2.rst` → that hash, rc 0; matches `SHA256SUMS:6`).
  Located quote, line 1545: `Similar to memory.events but the fields in the file are local` —
  `$ grep -cF 'Similar to memory.events but the fields in the file are local' before/src/v73-Documentation_admin-guide_cgroup-v2.rst`
  → `1` (rc 0; 11 words).
- **S287** — Linux v7.3 `fs/btrfs/sysfs.c`, URL `https://raw.githubusercontent.com/torvalds/linux/v7.3/fs/btrfs/sysfs.c`,
  access date 2026-11-03, kind `code`, tier A, anchor v7.3 line 1339, raw bytes sha256
  `098cb522131501deabde61ffcdc56138a8516098f4e980f9c34cb9e62b467377` (re-computed:
  `$ sha256sum .ufo/waves/round-68/before/src/v73-fs_btrfs_sysfs.c` → that hash, rc 0; matches `SHA256SUMS:7`).
  Located quote, line 1339: `Set perms to 0, disable /sys/module/btrfs/parameters/read_policy interface.` —
  `$ grep -cF 'Set perms to 0, disable /sys/module/btrfs/parameters/read_policy interface.' before/src/v73-fs_btrfs_sysfs.c`
  → `1` (rc 0; 7 words); the same command on the v7.2 file prints `0` (rc 1), because v7.2 line 1339 reads
  `parameter/read_policy`.

Cross-check with the note: the note draft `.ufo/waves/round-68/drafts/c1/note.md` (SC1Scribe) cites the same
v7.3 lines — 1501, 1535 and 1545 for S138 and 1339 for S158 — and names S286/S287 as the round's reference
rows (`$ grep -n '^| RW[12] ' .ufo/waves/round-68/drafts/c1/note.md` prints RW1 at 30 and RW2 at 31), so the
rows and the note agree on every anchor the note cites.

**Sources census.** The lane census is the L1's command at integration; this seat does not run it:

    $ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
    → BLOCKED-until-run (L1 to fill the rc, the ok/FAIL line and the W04 duplicate-URL count)

No value is asserted for that run here.

**C2 gate (drafted; receipts read, not produced, by this seat).** The round-66 routed gap — a note citing
`source: S999` passes the header gate because that gate checks presence only — is the failing example the new
criterion QUALITY 101 is drafted to hold (`.ufo/waves/round-68/drafts/c2/quality-101.md`). The instrument is
`tools/check-knowledge-refs-r68.py` (draft `.ufo/waves/round-68/drafts/c2/check-knowledge-refs-r68.py`), which
resolves every id on an operative `source:` line against `corpus/SOURCES.md` at the revision and reports
`KNOWLEDGE-REF-DANGLING` for a miss. The executor's receipts, read at draft time: selftest
`.ufo/waves/round-68/probes/c2-selftest.txt` → `{"selftest": {"cases": 19, "failures": [], "passed": 19,
"status": "PASS"}}` (rc 0); red-before `.ufo/waves/round-68/probes/c2-red-before.txt` → the fixture note
`corpus/knowledge/s999-fixture-r68.md` with `source: S999` at line 3 gives `"dangling_count": 1` and
`KNOWLEDGE-REF-DANGLING`, rc 1; live base `.ufo/waves/round-68/probes/c2-live-base.json` → `"branch_tip":
"3f6edcc9…"`, `"dangling_count": 0`, `"note_count": 85`, rc 0. This seat ran no gate; the L1 runs it at
integration.

## Mistakes

- **R67-POSITIVE-CONTROL-COMMAND-MISMATCH** — class `number-drift` · evidence pointer: the round-67 verifier
  spot-check `corpus/lessons/round-67-verifier-spotcheck.md` §6 item 1, against the superseded figure in the
  round-67 lesson (`corpus/lessons/round-67.md:31` "`grep -c -i limit` on r42 returns 21"; `:79` the same figure
  in the "Shown able to fail" sentence) · captured-by: the round-67 non-author spot-check (§6 item 1), re-derived
  here over `corpus/knowledge/btrfs-scrub-record-r42.md` — `$ grep -c -i limit corpus/knowledge/btrfs-scrub-record-r42.md`
  → `14` (rc 0) and `$ grep -o -i limit corpus/knowledge/btrfs-scrub-record-r42.md | wc -l` → `21` (rc 0) ·
  criterion that should have caught it: `CORPUS.md:34` "A count carries its command" (with the admission bar's
  item 2, every claim carries a measured anchor) · fix: an appended erratum, never an in-place edit. The erratum
  text stood in the lane working tree at draft time (`$ git diff --stat -- corpus/lessons/round-67.md` →
  `1 file changed, 15 insertions(+)`; `$ git diff -- corpus/lessons/round-67.md | grep -c '^-[^-]'` → `0`, rc 1;
  `$ git diff -- corpus/lessons/round-67.md | grep -c '^+[^+]'` → `12` non-blank added lines), uncommitted at
  HEAD `3f6edcc9`. It is reproduced verbatim below so the L1 lands it once; a second append would duplicate it.

      ## Erratum (round 68) — R67-POSITIVE-CONTROL-COMMAND-MISMATCH

      Append-only. Supersedes only the figure `21` in the Mistakes row R67-NUMBER-DRIFT-WATCH and in the
      "Shown able to fail" sentence above (`grep -c -i limit` on r42 → 21). The round-67 verifier
      spot-check (`corpus/lessons/round-67-verifier-spotcheck.md` §6 item 1) found that the pasted command
      prints **14**; `21` is the occurrence count from `grep -o -i limit … | wc -l`. Re-derived at base
      `42400ec6` over `corpus/knowledge/btrfs-scrub-record-r42.md`:

          $ grep -c -i limit corpus/knowledge/btrfs-scrub-record-r42.md        → 14   (matching lines)
          $ grep -o -i limit corpus/knowledge/btrfs-scrub-record-r42.md | wc -l → 21   (occurrences)

      The positive-control claim stands unchanged (the pattern returns nonzero on r42, so the negative counts
      for "revert" and "old_limit" are not vacuous). Only the figure and the command it names differ. The
      miscount is classed as a count without its command (CORPUS.md "A count carries its command") and
      is carried by the round-68 lesson as a Mistakes row.

- **R67-COUNTER-SHAPE-ONLY** (carried) — class `vacuous` · evidence pointer: round-67
  `.ufo/waves/round-67/probes/m1-c1-counter-battery.txt` (the frozen `grep -cE '^\| SL[0-9]+ \|'` kills Ma and
  passes Mb, Mc, Md, Me) · captured-by: the round-67 mutation tester M1; the strict counter that answers it is
  this round's E2Battery battery. Receipt read by this seat at 2026-11-03T22:45:48Z: 264 lines, sha256
  `5ff7a184334ee624ca074fec5483e3b427f16292192b0e295fadfff47cffc260`, with the summary at lines 58-59 and
  again at 262-263 reading `battery_should_fail_accepted=5 of 5 red/5 control=6` and
  `extra_controls=14/14 failed_fixtures=0`, `rc=0`, and its ORDERING CHECK section reading `violations=0`;
  the counter hash line inside the receipt is `b93f5912…438458`, matching `sha256sum
  .ufo/waves/round-68/drafts/c1/count-rw-r68.py` at that moment. The receipt also records the draft note
  read-only: `RW_ROWS=6`, `LAYOUT=8` on `drafts/c1/note.md` (sha256 `1d2a4d8d…0bbd8b`), the frozen grep and
  the strict counter agreeing at 6. An earlier revision of the same receipt (142 lines, sha256 `71df5fcc…`)
  read `extra_controls=11/11` and is superseded; the settled file is 15887 bytes with the same 264-line
  digest. The receipt's frozen-artefact line reads `frozen note corpus/knowledge/linux-v73-pinwatch-r68.md:
  ABSENT (counter rc 2, EDGE PROBES below)`, i.e. the battery froze before any note existed; the L1 re-hashes
  both files at landing · criterion: QUALITY 73 (a
  counter's evidence is a committed should-fail battery whose last-line measure is the claim) plus the freeze
  rule that a rule changed after scoring is not the claim's rule · fix: the strict counter is the next
  frozen-counter amendment, declared before data; it is **not** applied to this round's C1 predicate (frozen),
  so round 68 reports the carry and the instrument, not an in-round replacement.

- **R68-CROSSLINE-QUOTE-GREP** — class `quote-verification` · evidence pointer: this seat's own drafting work.
  The first Gate-quote candidate was the memory.events hierarchy sentence spanning v7.3 lines 1501-1503;
  `$ grep -cF 'Note that all fields in this file are hierarchical and the file modified event can be generated due to an event down the hierarchy.' before/src/v73-Documentation_admin-guide_cgroup-v2.rst`
  → `0` (rc 1), while the same sentence's first physical line alone →
  `$ grep -cF 'Note that all fields in this file are hierarchical and the' before/src/v73-Documentation_admin-guide_cgroup-v2.rst`
  → `1` (rc 0). A line-based grep cannot match a sentence broken by a newline, so a genuine quote would have been
  recorded as absent · captured-by: the `grep -cF` check itself, run before the quote entered any row and shown
  able to print both `1` and `0` · criterion: `CORPUS.md:42` "A quote names its location" is the nearest; no
  criterion states the single-physical-line requirement, which is the gap this row records · fix: every Gate
  quote is one physical line, printed with its line number and its `grep -cF` count. The sweep over the finished
  draft found nothing further: `$ grep -c '^## Mistakes' .ufo/waves/round-68/drafts/c1/lesson-round-68.md` → `1`
  (rc 0), NF `13` and `13` on the two rows, and both quotes at count `1` of `1`.

## Sources

- **S286** — Linux v7.3 `Documentation/admin-guide/cgroup-v2.rst`, opened 2026-11-03, kind `docs`, tier A;
  used by `corpus/knowledge/linux-v73-pinwatch-r68.md`.
- **S287** — Linux v7.3 `fs/btrfs/sysfs.c`, opened 2026-11-03, kind `code`, tier A; used by
  `corpus/knowledge/linux-v73-pinwatch-r68.md`.
