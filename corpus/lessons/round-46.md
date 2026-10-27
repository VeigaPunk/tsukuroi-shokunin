# Round 46 — lesson (tsukuroi, hyaku run 9)

author: tsukuroi L1 (`TsukuroiR46`), 2026-10-27. Base `2042117cfb724170772f4c128cc2ddba0b61d817` (the lane tip at
round start), freeze `72cc26096bc24d765a7cd70d4b4d9471cb854001` (declaration, frozen counters, pre-data controls,
round-start receipts, S250/S251 snapshots), C1 first landing `a44770491eb5ca15ce9f8b3207309d1af683ffaf`, GR2/GR3
narrowing `b57740c21f0c68ac7eefeba0adb9c67fbeae3228`, C1 hardening `61e067408ad73c144e42ea8f2ec5ed3f333d7e2e`. Claims,
controls and the pre-freeze counter fix: `SCORECARD.md` "Round 46 — declaration". One v2 wave `w1` (66 seats) and a
residual call `r1` (4 counted reviewer/critic seats). Seats are the lane, not outside reviewers (LEARNING.md); the
non-author closure is pending.

## Outcome (author-side; non-author closure pending)

- **C1 operability — PASS** at `61e067408ad7` (`.ufo/waves/round-46/l1/c1-61e06740.jsonl`): identity_ok 1, tracks_ok 1,
  symlink_ok 1, unverifiable_ok 1, cli_ok 1, nowrite_ok 1, selftest_pass 1 (162/162), selftest_r46 8; also PASS at the
  first landing `a4477049` (`l1/c1-impl-a4477049.jsonl`, selftest_r46 6). Before: FAIL at base (`before/c1-before-base.jsonl`,
  identity_ok 0). Wave w1 hardened it: the inherited-descriptor wrong digest (R46-C1-INHERITED-FD-WRONG-DIGEST) and
  `--identity --help` (seat C1RevImpl). Kill-rule receipts: `w1/C1ExecPlaneDiff.md`, `C1ExecLiveWrite.md`,
  `C1ExecAdjacency.md`, `C1ExecPriorC.md` (at `a4477049`), the L1's final-revision runs under `l1/killrule/` and
  `l1/planediff/` (those not finished when the round closed are named in the report).
- **C2 depth — FAIL**: verdicts_ok 2 (GR1, GR3), r45_legs_ok 1, marks_ok 0 (`after/c2-final.jsonl`). GR2 was read
  `partly` on its narrowed bytes by the residual critic and the frozen universe has no seat left (R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT).
  No admission mark was written; GR1-GR3 stay pending (entry "Gate status — round 46").
- Found, not claimed: the census selftest fails 149/160 when TMPDIR contains a space, at base too (`w1/C1ExecRerunB.md`);
  C2 counter holes (unbound tail after an inner `## ` line, negating marks scored, RecursionError, `w1/C2RevCounter.md`;
  K22/K23, `w1/C2CritControls.md`; six mutation survivors, `w1/C2MutBinding.md`) — planned for round 47.

## Gate

### New SOURCES rows (opened 2026-10-27; L1 fetch 04:59:34Z, re-opened live by wave seat SrcGateNew at 05:23:21-05:23:37Z, byte-identical)

| Row | URL (access 2026-10-27) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S250 | https://git.savannah.gnu.org/cgit/bash.git/plain/shell.c?h=bash-5.3 (same `plain/…?h=bash-5.3` form for `general.c`, `general.h`; tag `bash-5.3` peeled `b8c60bc9ca365f8261fa97900b6fa939f6ebc303`) | "fd = move_to_high_fd (fd, 1, -1);"; "SET_CLOSE_ON_EXEC (default_buffered_input);"; "for (nfds--; check_new && nfds > 3; nfds--)"; "#define HIGH_FD_MAX	256" | shell.c:1700, :1703; general.c:696; general.h:252 |
| S251 | https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html | "named by its file descriptor, and which is a symbolic link to the actual file"; "type:[inode]" | proc_pid_fd.5.html:74-75, :84 |

Snapshot digests: `.ufo/waves/round-46/frozen/src/SHA256SUMS` (shell.c `5f3d539f…f73d`, general.c `669ef408…d165`,
general.h `bf9251e3…f2f2`, proc_pid_fd.5.html `3a50ddef…ff27e`), fetch log `FETCH.txt`. Live re-fetch receipts:
`.ufo/waves/round-46/w1/SrcGateNew/` (`digests-live.txt` 4/4 equal, `cmp` 4/4 identical, `quotes.txt`). Row review:
`w1/SrcReview.md` (supports; census exit 0).

### Reject rows (candidates considered this round and refused; source-checked by wave seat SrcGateNew)

| Entry (candidate) | Rejected | Reason | Flip |
|---|---|---|---|
| `doc/bash.1` at tag bash-5.3 (sha256 `23f7bd15…1971`) and the installed `bash.1.gz` (bash 5.3.20-1) | yes — as the docs-tier source for S250 | Neither page states which descriptor bash holds an opened script on: the only `\b255\b` hits are exit-status text (`bash.1:5912`; installed page `:3160`) | a manual revision that documents the script descriptor |
| GNU Bash Reference Manual, https://www.gnu.org/software/bash/manual/bash.html | yes | Unreachable from this host on 2026-10-27 (`curl: (28) Connection timed out after 25001 milliseconds`, 0 bytes): no digest, no quote | a fetch with bytes and a stable locator |
| `input.c` at bash-5.3 (sha256 `d88d0583…a50b`) | yes — read for the honesty limit, not registered | Its lines decide buffered reads, not the descriptor; the entry's limit cites the behaviour without a row | an entry claim that rests on the buffering itself |
| staged `merge/tsukuroi/SOURCES.append.md` (147 rows) | yes — assimilation none | 52 staged ids collide with the lane registry S200-S251 (`.ufo/waves/round-46/assimilation/collisions`); no staged theme fits the round's surfaces (`w1/AsmGate.md`) | a renumber-by-document of an admitted entry's rows |

### Re-opened rows and rows touched old→new

`git diff 2042117c b57740c2 -- corpus/SOURCES.md` is two insertions (S250, S251) and no deletion: no old row's cell
changed. Re-opened for evidence (no cell edited):

| Row | used-by old → new | Log |
|---|---|---|
| S246, S247, S248 | unchanged | live re-fetch 2026-10-27 by seat C2ExecLiveSources, byte-identical to `.ufo/waves/round-45/frozen/src/SHA256SUMS` (`w1/C2ExecLiveSources/sha256-live.txt`); tag pins re-resolved (`tags.txt`) |
| S237, S242, S243, S244 | unchanged | same seat, byte-identical to the round-42 and round-44 `SHA256SUMS`; also re-opened by seat SrcReopenR45 (`w1/SrcReopenR45/cmp-live-vs-frozen.txt`) |
| S249 | unchanged | capture re-run read-only by seat C2ExecHostRecheck (`w1/C2ExecHostRecheck/`): every value GR1-GR3 cite unchanged |

Census (frozen command): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` — start
exit 0, 249 rows, 40 W04 (`.ufo/waves/round-46/before/sources-census-start.txt`, run by this attempt at its own start,
routed D4); end in `.ufo/waves/round-46/after/sources-census-final.txt`.

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT | claim sizing — a frozen verdict universe too small for the amendment path it allows | The C2 rule lets a row be narrowed after a `partly` and re-read by residual seats, but froze one residual pair per row (`V46ResRevGR<n>`, `V46ResCritGR<n>`). GR2 was read `partly` by both counted critics (`w1/V46CritGR2a.md`, `V46CritGR2b.md`), narrowed at `b57740c2`, and read `partly` again by `r1/V46ResCritGR2.md` (an `-EAGAIN` return before the setup steps; more than one path sets a replace suspended, `dev-replace.c:1186`, `:1224`, `:1238`). No counted seat is left to read a second narrowing, so GR2 cannot bind on any bytes this round and C2 fails `verdicts_ok == 3`. The round-43 and round-45 C2 rows show the same shape: each needed a narrowing after its counted read | none; the pre-data battery tested the amendment path once (K18: one narrowing answered by both residual seats) and never a second `partly` | Size the verdict universe to the amendment depth the rule allows, or freeze a rule that admits per row (a row-level claim) so one contested row does not sink the others. Able to fail: the round-46 receipt itself — `per_row.GR2.bound_on_current` counts a `partly` on the current bytes and the row is not ok, with no seat name left in the universe (`after/c2-final-*.jsonl`) |
| R46-C1-INHERITED-FD-WRONG-DIGEST | honesty — `verified=yes` over bytes that did not run | The first landing `a4477049` took the first descriptor ≥ 10 whose link equalled the invoked path. Wave seat C1LabUlimit: a parent-held descriptor on a decoy, relinked over the script path after bash opened it, printed the decoy's digests with `verified=yes`, 15/15 with a racer and 1/1 deterministic (`w1/C1LabUlimit.md` "Falsification"). The frozen counter's legs did not exercise this case | wave seat C1LabUlimit; not the frozen counter | `61e06740`: only a descriptor carrying `O_CLOEXEC` in `/proc/$$/fdinfo` (set by bash on its script descriptor, S250 `shell.c:1703`; never on an inherited or redirected one) and the only such match is hashed. Able to fail: the L1 ran the reproducer on both revisions — `a4477049` prints the decoy sha256 with `verified=yes`, `61e06740` prints `unverifiable` (`.ufo/waves/round-46/l1/held-fd-old-new.txt`); the selftest case "a parent-held descriptor on a relinked decoy is never hashed (R46-C1)" fails on the old function |
| R46-C1-COUNTER-PATHHASH | control design — a must-FAIL control passed the counter draft | The first battery scored `K2-pathhash` PASS (`controls/battery-summary-c1-draft1.jsonl:3`); with `${BASH_SOURCE[0]:-}` the stdin and pipe legs never name a regular file, so a path hasher and the descriptor reader agree there | the pre-data battery (prompt §9), before the freeze | the frozen counter adds the replaced-after-open case; K2 FAILs (`controls/battery-summary-c1.jsonl:3`, 9/9 as expected) |
| R46-CENSUS-STDIN-UNBOUND | latent shell defect under `set -u` | `bash -s < tools/tsukuroi-census.sh` died at `:455` with `BASH_SOURCE[0]: unbound variable` since the file was created (`5f906451`, probation round 2; `w1/ScribeLesson/stdin-unbound.txt`) | the L1 while testing the stdin case of `--identity` | `:455` reads `${BASH_SOURCE[0]:-}`; the stdin identity case exits 0 with `unverifiable` (selftest and counter `unverifiable_ok`) |
| R46-SEAT-WROTE-LANE-FILES | seat scope — a drafting seat wrote tracked lane files | Seat D2D3Draft, asked for draft text, appended its correction notes directly to three tracked files (`.ufo/waves/round-44/w1/C1ExecLiveRead/commands.txt`, `.ufo/waves/round-44/w2/SkillReview.md`, `.ufo/waves/round-45/a2w1/AsmGate.md`) and overwrote the L1's own appends made minutes earlier (`w1/D2D3Draft.md` "What I did"); the wave context forbids it ("never edit, create or delete any tracked lane file") | the L1 at integration (`git diff --stat` showed +56 lines in AsmGate.md) | The text was checked against an independent L1 recount (249/147/50; five non-registry ids; 25 omitted) and adopted at `b57740c2`. Prose rule only; no gate refuses a seat's write to a tracked file (`rule-only`, round-45 seat-harm ledger class `lane-pollution`) |
| R46-FLEET-ROOT-MISROOT | seat scope — live fetches landed at the fleet root | Twelve files (`btrfs-scrub@.service`, `dev-replace.c`, `kstrtox.c`, `scrub.c`, `scrub237.c`, `sha256-live.txt`, `sysfs.c`, `systemd.kill.xml`, `tags-*.txt`, `vsprintf.c`) landed at `/home/vgpnk/Projects/shokunin/` at 02:22:07-16 -03 with cwd = fleet root; `w1/C2ExecLiveSources/sha256-live.txt` names `scrub237.c`, so the seat is C2ExecLiveSources. The orchestrator quarantined them under the fleet's `.tower/quarantine/fleet-root-strays-20261027T0600/` | the orchestrator (fleet-root sweep), not the lane | Recurrence of `fleet-root-write` (round-45 ledger: rounds 37, 44; now 46). The context's first rule names the fleet root; the item's own `curl` lines did not `cd` first. Fix carried: every seat item that fetches names its output directory in the command (`curl -o {SC}/<seat>/…`), not only in the context |

## Round-45 routed defects — round-46 disposition

| Defect | State | Evidence |
|---|---|---|
| D1 R45C-D3-R44-MARK-SWEEP | closed | appended at `c7e4d7d9`: `SKILL.md` "Scrub record — round 44 status note (routed defect D1; appended 2026-10-27)" and `corpus/README.md` "Round-46 coverage note" paragraph "Round-44 status": round 44's depth gate FAILED (`verdicts_ok 0`), SR7-SR9 pending; capture `.ufo/waves/round-46/l1-capture/scribe-d1.txt:1`. The round-45 lesson's D3 row (`round-45.md:94`) stays as written; this row supersedes its "closed" for the README/SKILL half |
| D2 R45C-D7-CITATION | closed | appended correction lines at `.ufo/waves/round-44/w1/C1ExecLiveRead/commands.txt:88` and `.ufo/waves/round-44/w2/SkillReview.md:104` name the committed `strace-rev-live1.log.gz`; `git cat-file -e 2042117c:<…>.log` 128, `.log.gz` 0 (`b57740c2`) |
| D3 R45C-ASMGATE-RECEIPT | closed | appended "Correction (round 46, R45C-ASMGATE-RECEIPT)" in `.ufo/waves/round-45/a2w1/AsmGate.md`: 249 / 147 / 50 at `44560592`, five non-registry ids, 25 omitted, pointer to `assimilation/collisions` (`b57740c2`) |
| D4 R45C-START-CENSUS | closed | `.ufo/waves/round-46/before/sources-census-start.txt` (exit 0, 249 rows, tip `2042117c`), run by this attempt at its start |
| D5 R45C-POSTFREEZE-NAME | closed | the C2 counter binds seat names across every round-46 `<wave>-dispatch.json` and names no wave; control K15 (an arbitrary wave name) PASSes as designed; no post-freeze counter edit this round (`git log 72cc2609.. -- tools/score-census-identity-r46.py tools/check-scrub-admission-r46.py` is empty) |
| Carried: re-bind GR1-GR3 through a seat-written channel (QUALITY 93) | channel works; claim FAIL | 16 counted reports bound through their own first two lines (none refused for shape): see Outcome |
| Carried: round-45 C1 review gaps, C2MutBinding survivors | open, re-raised | `w1/C1CritControls.md`, `w1/C2MutBinding.md` (six binding-check mutants survive the 22-control battery: agent role, results count, quorum 1, body length, r45 sha, one mark), `w1/C2CritControls.md` (K22 nonexistent citation line, K23 byte-identical reports both bind) — planned for round 47 |

## Assimilation and considerthese

Assimilation: none. Package `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/` read-only, no campaign tool run. Id check
with the prompt's 0-3-space extractor on the lane at `c7e4d7d9`: registry 251 ids, staged 147, collisions 52 (S200-S251;
S250/S251 are this round's new rows and also staged ids) — `.ufo/waves/round-46/assimilation/` (`reg-ids`,
`staged-ids`, `collisions`); guard proved on a scratch registry with an indented `  | S002 |` row (`guard-proof.txt` =
`S002`). Quarantine slice: 12 rows (`assimilation/quarantine-slice`), none hand-checked this round, so none is
appendable. No staged theme fits (`w1/AsmGate.md` "Theme recommendation").

### considerthese — burst-aware reading (`considerthese/2026-10-26.md`, proposal "Burst-aware reading", 2026-10-26)

Mined by wave seat ConsiderMine (`w1/ConsiderMine.md`; the other four proposals of that file were mined in rounds 41,
42, 43 and 45 — verified by grep there). Proposal: "In a burst, I could read each round's LOG entry and verifier
spot-check first, then sample commits only where the two disagree, and say up front how many rounds the window holds."
Measured on rounds 43-45 (5 h 01 m, 39 commits, 319,049 inserted lines against 1,046 lines of LOG entry, spot-check and
lesson): 28 statements both documents speak to, 3 disagreements, all in status or harm wording and none in a number —
round 44's LOG names neither the `adjacency harmed` grade nor the `quality harmed` grade, and round 45's LOG reports
D1-D6/D8-D10 closed while the spot-check found round-44 D3 half closed (`w1/ConsiderMine/tally.txt`,
`log-vs-spotcheck.jsonl`). Rule taken: a burst read opens with the window's round count and compares LOG and spot-check
field by field — every axis grade, every trend verdict, every routed-defect state — before sampling commits; agreement on
numbers is weak evidence (a closure copies the LOG's counters) and never replaces a receipt (QUALITY 77). The seat's
checker (`w1/ConsiderMine/check-log-axis-coverage.py`, four fixtures) is wave evidence, not a lane gate.

## Spot-check candidates for the non-author closure

Admits: S250 (bash-5.3 `shell.c:1700,1703`, `general.c:696`) and S251 (`proc_pid_fd.5.html:74-75`), each re-fetched
byte-identical (`w1/SrcGateNew/digests-live.txt`); the C1 identity line (`bash tools/tsukuroi-census.sh --identity` at
the measured revision vs `sha256sum tools/tsukuroi-census.sh`). Rejects: the bash manual pages as the S250 docs source
(no descriptor statement) and the staged registry (52 collisions). Not an admit: GR1-GR3 (C2 FAIL; see Outcome).
