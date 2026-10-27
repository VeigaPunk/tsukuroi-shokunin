VERDICT: draft

Seat `ScribeLesson` (L2 leaf, tsukuroi round 46 / hyaku run 9, wave `w1`, item F-4): draft `corpus/lessons/round-46.md`
as text, verify the three named candidate mistakes against evidence, and say for each whether a gate can be shown able
to fail. The draft is at the end of this report, verbatim, for the L1 to land. It is a **draft**, not a finished
lesson, for exactly three reasons: the `## Gate` rows belong to seats F-1 (new rows S250/S251, rejects) and C2-S10
(re-opened rows) and had not landed when I read; C2 has no measured after-state (the counter has not been run for the
round and `w1-results.json` did not exist); and this round's `considerthese` mining (seat `ConsiderMine`) is in flight.

Revisions read: base `2042117cfb724170772f4c128cc2ddba0b61d817`, freeze `72cc26096bc24d765a7cd70d4b4d9471cb854001`,
implementation `a44770491eb5ca15ce9f8b3207309d1af683ffaf`. HEAD moved **during** this read: I began at `a4477049` and
`b57740c21f0c68ac7eefeba0adb9c67fbeae3228` landed at 05:30Z ("GR2/GR3 narrowed per counted partly findings
(V46CritGR2a/b, V46CritGR3a, V46RevGR3a); D2/D3 correction notes appended"). Every line number I cite in
`tools/tsukuroi-census.sh` is the **committed** blob's (`git show HEAD:tools/tsukuroi-census.sh | sed -n …`, sha256
`d925839c…2cfa`, 3598 lines, 209208 bytes), which I re-checked after the move; the working tree at 05:30Z also carried
an **uncommitted** census edit, still in flight (`id_check` `|| true`, a new `--identity --help` cli case, and an
`O_CLOEXEC` + unique-descriptor rewrite of `census_identity`): 31 insertions/17 deletions at 05:30Z, 41/17 at 05:33Z,
working sha256 `48dd828b…e66d` — so anything that cites census line numbers after `:3391` must be re-pinned to the commit
it was measured at. Frozen counters at the freeze match the declaration: `tools/score-census-identity-r46.py`
`7c406eb5…524ba`, `tools/check-scrub-admission-r46.py` `28c409be…d11d8`.
I wrote only `.ufo/waves/round-46/w1/ScribeLesson.md` and `.ufo/waves/round-46/w1/ScribeLesson/`; no lane file, counter,
census or host state was written, and no frozen counter and no census selftest was run by this seat (the only counter
entry point I invoked is the read-only `--section-hash` diagnostic, which prints hashes and writes nothing).

---

## Evidence per candidate

### (1) R46-C1-COUNTER-PATHHASH — the first C1 counter draft let a must-FAIL control PASS; caught pre-data

The two battery summaries are the whole evidence, and they disagree on the one row that matters:

- first draft, `.ufo/waves/round-46/controls/battery-summary-c1-draft1.jsonl:3` —
  `{"as_expected": false, …, "control": "K2-pathhash", "expect": "FAIL", …, "identity_ok": 1, "tracks_ok": 1,
  "symlink_ok": 1, "unverifiable_ok": 1, "cli_ok": 1, "nowrite_ok": 1, "selftest_pass": 1, "selftest_r46": 5,
  "verdict": "PASS"}`. Every leg of the declared predicate is 1, so the path-hasher passed the counter by the
  predicate's own sentence.
- frozen battery, `.ufo/waves/round-46/controls/battery-summary-c1.jsonl:3` — same control,
  `"unverifiable_ok": 0`, `"selftest_pass": 0`, `"verdict": "FAIL"`, `"as_expected": true`; totals `9/9` as expected
  (`draft1` is `8/9`, the one miss being K2).
- The mechanism, in the lane's own words: `SCORECARD.md:2994-2999` — "with `${BASH_SOURCE[0]:-}` the stdin and pipe
  cases never name a regular file, so hashing the path and hashing the descriptor agree there … The frozen counter adds
  the case that separates them — the script renames a decoy over its own path on its first line, so the path names new
  bytes while bash still reads the old inode". The added leg is `tools/score-census-identity-r46.py:199-209`; the
  candidate gained the matching `(R46-C1)` case (`tools/tsukuroi-census.sh:3441-3446`).
- Independently re-caught in-wave by seat `C1CritControls` (`.ufo/waves/round-46/w1/C1CritControls.md:5`: "K2-pathhash
  in `battery-summary-c1-draft1.jsonl` is a decisive counterexample … hence the draft battery missed its named
  path-trust defect"), and read the same way by `C1CritClaim.md:8`.

**Can a gate be shown able to fail?** Yes, and it is the round's cleanest red→green: the red shape is a committed row
where a control declared `expect: FAIL` records `verdict: PASS` with every leg 1 (draft1 `:3`); the green shape is the
same control killed with the leg that was missing (`battery-summary-c1.jsonl:3`), while the candidate control K8 still
PASSes (`:8`), so the new leg kills the mutant rather than the candidate. The gate is the battery itself, and it ran
**before the freeze and before any seat** — this mistake never reached a scored revision, which is why its class is
"caught pre-data", not "harm".

### (2) R46-CENSUS-STDIN-UNBOUND — `SELF=${BASH_SOURCE[0]}` died under `bash -s` from the file's first executable commit

- At base, the census exits before doing anything when it is read from stdin:
  `git show 2042117c:tools/tsukuroi-census.sh > base-census.sh && bash -s -- --identity < base-census.sh` →
  `bash: line 455: BASH_SOURCE[0]: unbound variable`, `rc=1` (`ScribeLesson/stdin-unbound.txt`). No identity line, no
  plane line, no verdict: under `set -euo pipefail` (`:451`) the assignment at `:455` is the first thing that runs.
- The line's landing commit, from the prompt's own command: `git log -S'SELF=${BASH_SOURCE[0]}' --oneline --
  tools/tsukuroi-census.sh` prints two commits — `5f906451` ("probation round 2: first executable gate
  tools/tsukuroi-census.sh", 2026-10-14 11:17:42 -0300, the commit that created the file) and `a4477049` (this round,
  which re-adds the guarded form). Between them the string was never removed, so the unguarded line is present at every
  revision in `5f906451..2042117c` — 22 commits touched the census in that range (`git rev-list --count`), and
  `git show 2042117c:…| sed -n 455p` reads `SELF=${BASH_SOURCE[0]}` at exactly the line number the runtime error names.
- Why nothing caught it: the base file contains no invocation of itself from stdin (`git show 2042117c:…| grep -c
  'bash -s'` → 0), so no test in 44 rounds exercised the shape.
- At the implementation the same command prints the identity line with all four byte fields `unverifiable` and
  `verified=no`, `rc=0` (`ScribeLesson/stdin-unbound.txt`); `:455` now reads
  `SELF=${BASH_SOURCE[0]:-}  # round 46 (C1): empty when the script is read from stdin (--identity: unverifiable)`.
- The lane records the defect itself: `corpus/knowledge/census-identity-r46.md:39-41` — "before round 46 the stdin form
  died at line 455 with `BASH_SOURCE[0]: unbound variable`". The change is visible as a one-line diff in a seat receipt,
  `.ufo/waves/round-46/w1/C1ExecPlaneDiff.md:121`:
  `SELF=${BASH_SOURCE[0]} -> SELF=${BASH_SOURCE[0]:-}   [impl:455]`.

**Captured-by, stated precisely:** not by any review seat, and every seat that names it postdates the change. I grepped
every landed seat report for `unbound`/`BASH_SOURCE` (`.ufo/waves/round-46/w1/*.md`) at draft time; the hits are the
plane-diff edit line above, a base-vs-impl line table (`.ufo/waves/round-46/w1/C1ExecAdjacency.md:101`), a positive
review note on the guard (`.ufo/waves/round-46/w1/C1RevImpl.md:14`), and the base-bytes control that witnesses the
failure empirically — `.ufo/waves/round-46/w1/C1ExecRerunA.md:70`: "`unverifiable_ok | 0 (stdin case rc 1
`bash: line 455: BASH_SOURCE[0]: unbound variable`; …`". The discovery channel was the implementation work — the
`--identity` design has to name what bash executes when bash holds no script file, and that forced `SELF` to be
optional.

**Can a gate be shown able to fail?** Yes. Red: the base bytes under `bash -s` (rc 1, no line). Green: the same bytes at
`a4477049` (rc 0, `verified=no`). The gate that keeps it green is a `(R46-C1)` selftest case that runs
`bash -s -- --identity` in a cwd holding a decoy regular file named `bash` and requires all four fields `unverifiable`
(`tools/tsukuroi-census.sh:3435-3439`), plus the frozen counter's `unverifiable_ok` leg, which runs three stdin-shaped
cases (`tools/score-census-identity-r46.py:185-215`). Mutation evidence that the leg bites: the base-bytes control K0 in
the frozen battery records `unverifiable_ok 0` (`battery-summary-c1.jsonl:1`).

### (3) R46-SELFTEST-EOF-NEWLINE — the census ends without a newline, so an appended case fuses into `main "$@"`

- Shape: `tail -c1 tools/tsukuroi-census.sh | od -c` → `0000000   "` — a quote, no `\n` — at base `2042117c`, at
  `a4477049` and at HEAD. The last line is `main "$@"` and it carries the file's final byte.
- Consequence, reproduced on the implementation bytes (append one line with no leading newline, as a first selftest
  draft would):

  | appended line | resulting last line | `bash <copy> …` |
  |---|---|---|
  | `# appended selftest case (no leading newline)` | `main "$@"# appended selftest case (no leading newline)` | `syntax error near unexpected token '('`, rc 2 |
  | `# r46 case` | `main "$@"# r46 case` | usage text, rc 2 (the arg becomes `--identity#`) |
  | `  ok 'identity case (R46-C1)'` (a real case line) | `main "$@"  ok 'identity case (R46-C1)'` | usage text, rc 2 (never runs the selftest) |

  Exact-match count of the invocation line `^main "\$@"$`: 1 unfused, 0 fused. So the appended case never exists as a
  command; the file either fails to parse or mis-parses argv (`ScribeLesson/eof-fusion.txt`).
- The hazard is known in three places and worked around in each, never fixed:
  `tools/tsukuroi-census.sh:3410` (`printf '\n# r46 identity selftest copy\n' >> "$idd/copy.sh"   # the census ends
  without a newline`), `tools/score-census-identity-r46.py:148-150` (`gb = fb + b'\n# r46 identity probe\n'  # leading
  newline: the census may end without one`) and `.ufo/waves/round-46/controls/make_c1_variant.py:47`.
- **The fix is not the missing byte, and that is why I do not propose adding one.** Adding a trailing newline to
  `tools/tsukuroi-census.sh` today would move nothing (the line is the file's last and the anchor rule protects only
  lines ≤ :3383, which do not move either way), but it would invalidate the census sha256 that the round-45 and
  round-46 receipts, `SKILL.md` and `LOG.md` quote, and it would silently change what `--identity` reports for the
  frozen implementation. The durable fix is a gate, not a byte. What a gate would have to assert: every
  `tools/*.sh` and `tools/*.py` ends with `\n` — cheap, and it fails today on this file.

**Captured-by:** the L1's own selftest drafting (the work-around lands in the same commit that adds the cases). No seat
report names it.

**Can a gate be shown able to fail?** No gate can be shown able to fail, because none exists: I found no checker in
`tools/` or `scripts/` that reads a tool file's last byte (`grep -rln 'endswith(b"\\n")' tools/*.py scripts/*.sh` →
none); the four `newline` hits in `tools/` are about first-line capture shape and receipt text
(`tools/score-census-readers-r45.py:25,196,271`), not file termination. So this row's last column is honest only as
"fix not yet able to fail — a gate is owed", and I say so in the draft rather than claim a kill I did not observe.
The class is unguarded, and the evidence it is unguarded is the reproduction plus the absent checker.

---

## Findings the L1 should act on before landing

1. **C2 cannot reach `holds` on GR2 and GR3 in this wave as dispatched — binding arithmetic, not a verdict claim.**
   The frozen rule is `tools/check-scrub-admission-r46.py:31-32`: "Row ok iff no bound seat of the row reads `fails` (on
   any hash), and the bound seats whose SECTION SHA256 equals the row's section hash at REV number at least 2 and all
   read `holds`." The landed reports, and the row hashes at the two revisions, are:

   | row | section hash the reports carry | section hash at `a4477049` | section hash at `b57740c2` | readers on the reported hash |
   |---|---|---|---|---|
   | GR1 | `fe77ac76…f9ca8` | `fe77ac76…f9ca8` | `fe77ac76…f9ca8` (unchanged) | RevGR1a `holds`, RevGR1b `holds`, CritGR1a `holds`, CritGR1b `holds` |
   | GR2 | `a963df81…781` | `a963df81…781` | **`4bf28bcf…6da`** | RevGR2a `holds`, CritGR2a **`partly`**, CritGR2b **`partly`** |
   | GR3 | `8fa62676…800` | `8fa62676…800` | **`43430a14…32c`** | RevGR3a **`partly`**, CritGR3a **`partly`**, CritGR3b `holds` |

   (`--section-hash` at `b57740c2`, exit 0; the counter's scored run was **not** made by this seat.) Consequences, in
   order of severity:
   - Before the narrowing, GR2 and GR3 already failed: their matching-hash sets were ≥ 2 and not all `holds`.
   - After `b57740c2`, **no landed report matches the narrowed bytes at all**, so both rows sit at 0 matching seats and
     the ≥ 2 requirement fails in the other direction. The narrowing also bound nothing new: it invalidated `RevGR2a`'s
     `holds` on GR2 and `CritGR3b`'s `holds` on GR3.
   - The only path the frozen predicate allows is the residual pair on the amended bytes — `V46ResRevGR<n>` /
     `V46ResCritGR<n>` (`:15-16`, `:18-20`; control K18 is exactly that shape, `controls/battery-summary-c2.jsonl:19`).
     **No residual seat is in this wave's dispatch**: `w1-dispatch.json` holds 66 tasks and zero `V46Res*` names
     (`ScribeLesson/c2-binding-state.txt`, captured twice). The counter scans every `<wave>-dispatch.json` under the wave
     dir (the binding names no wave), so a second dispatch file with the two seats per row would be found — that is the
     one move that can still bind GR2/GR3 this round.
   - `w1-results.json` did not exist at either capture (05:27Z, 05:30Z) and binding leg (2) requires it, so no seat was
     bound yet — the same channel hole that cost round 45 its `verdicts_ok` (`R45-C2-BINDING-CHANNEL`).
   - GR1 alone is in shape: four `holds` on an unchanged hash. Even so, `verdicts_ok == 3` needs the other two rows.
2. **Two ids minted this round are already staged ids.** `corpus/SOURCES.md:259-260` adds S250/S251; both ids exist in
   the staged package as the zh_CN and ja_JP translation rows
   (`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md:57-58`). My re-derivation with the prompt's
   0-3-space extractor: lane registry 251, staged 147, intersection **52** (round 45: 249/147/50) — matching
   `w1/AsmGate.md:9-11` to the digit. Any future landing renumbers by document; the round-45 D9 carry is now wider by
   two ids.
3. **Round-45 D1 is still half open, and the half that is open is the hall that reads as admission.**
   `corpus/README.md:465-466` does mark the **round-45** rows "depth gate FAILED … pending" — those two lines are what
   `194a4523` added (`git show 194a4523 -- corpus/README.md` shows exactly that pair, replacing the earlier sentence).
   But the **round-44** scrub row (`corpus/README.md:434`) and its paragraph `:440-452` carry no status:
   `git show <REV>:corpus/README.md | sed -n '427,452p' | grep -c -i -E 'fail|pending|admit'` → 0 at `a4477049` **and**
   at `b57740c2`. The SKILL section that lists SR7-SR9 (`SKILL.md:4214-4231`) is the same:
   `grep -c 'FAILED\|pending'` → 0. Round 44's depth gate also FAILED
   (`corpus/lessons/round-44-verifier-spotcheck.md:81`), so those three rows read as admitted in the two files that index
   them. Seat `ScribeReadme-3` reached the README half independently (its F-6 note; a message, not a receipt) and is
   drafting a `## Round-44 correction` section — that append plus the SKILL half's is what closes D1.
4. **D2 and D3 landed at `b57740c2`, after I first read them as working-tree drafts.** At `a4477049` both were
   uncommitted (` M` in `git status --porcelain`); at `b57740c2` the three correction files are committed
   (`git diff --stat a4477049 b57740c2` lists `commands.txt` +2, `SkillReview.md` +2, `AsmGate.md` +56) and
   `git status --porcelain` shows no modification on them. The corrections themselves: `commands.txt:88` and
   `SkillReview.md:104` name the `.log.gz`, and `git cat-file -e HEAD:<…strace-rev-live1.log>` is `rc=128` against
   `rc=0` for the `.gz`; the AsmGate recount paragraph replaces 183/147/30 with 249/147/50 at `44560592`. The lesson
   row must therefore cite `b57740c2`, not "uncommitted".
5. **`C1CritRace.md:7` is a limit already in the entry, not a new defect.** It argues that `verified=yes` does not
   prove the bytes bash executed, because the identity hashes the live descriptor twice
   (`tools/tsukuroi-census.sh:3478-3486`). The entry's own Limits say the same and narrow it honestly
   (`corpus/knowledge/census-identity-r46.md`, "Bash reads a script in pieces … the second sha256 read only narrows
   that window"). Worth quoting in the closure so the claim is not read as stronger than it is; no text change owed.

---

## Not done (explicit)

- I did not run either frozen counter (`score-census-identity-r46.py`, `check-scrub-admission-r46.py`) or the census
  selftest: they belong to seats `C1Exec*`/`C2*` and to the L1's measured run, and the wave was still in flight.
- I did not re-fetch S246-S251 live: that is F-1's and C2-S10's item. I verified only the frozen digests
  (`sha256sum -c .ufo/waves/round-46/frozen/src/SHA256SUMS` → 4/4 OK) and that the SOURCES diff adds two rows and
  changes no old cell (`git diff 2042117c a4477049 -- corpus/SOURCES.md` = 2 insertions, 0 deletions).
- I did not read the 12 counted seat reports in full, only their first two lines and their row-hash sets, which is what
  the binding reads; their content findings (e.g. `C2CritGR2a.md`'s scrub.c:3137-3144 `-EIO` narrowing) are the
  critic seats' to grade.
- I did not write the lane lesson file, per the item.

---

# Draft text — `corpus/lessons/round-46.md`

```markdown
# Round 46 — lesson (tsukuroi, hyaku run 9)

author: tsukuroi L1 (`TsukuroiR46`), 2026-10-27. Base `2042117cfb724170772f4c128cc2ddba0b61d817` (the lane tip at round
start, carrying the round-45 spot-check), freeze `72cc26096bc24d765a7cd70d4b4d9471cb854001` (declaration, frozen
counters, pre-data controls, S250/S251 snapshots, round-start receipts), implementation
`a44770491eb5ca15ce9f8b3207309d1af683ffaf`. Claims, controls and the pre-freeze counter fix: `SCORECARD.md`
"Round 46 — declaration". One v2 wave, `w1` (66 seats). Seats are the lane, not outside reviewers (LEARNING.md); the
non-author closure is pending.

## Outcome — _placeholder (filled by the L1 at the measured revision)_

Measured revision: _pending_ (`after/c1-final-*.jsonl`, `after/c2-final-*.jsonl` through `tools/run-receipt.py`; the
`after/` directory did not exist when this draft was written).

- **C1 operability — _pending_.** The only receipt at draft time is the implementation run
  `.ufo/waves/round-46/l1/c1-impl-a4477049.jsonl` (row 2): `identity_ok`, `tracks_ok`, `symlink_ok`, `unverifiable_ok`,
  `cli_ok`, `nowrite_ok`, `selftest_pass` all 1, `selftest_r46 6`, census sha256 `d925839c…2cfa`, identity line ending
  `verified=yes`, selftest `TSUKUROI_CENSUS_SELFTEST: PASS (160 cases, 160 passed, 0 failed)`, `exit_code 0`
  (row 3). Before: control K0 on the base bytes FAILs every leg (`controls/C1-K0.jsonl`). The kill rules — PLANE/HANDOFF
  drift, the ten predecessor counters, the no-write rule, `check-adjacency-anchors`, and the census line at or before
  `:3383` — are the seats' receipts (`w1/C1Exec*`, `w1/RevGatesAll`), not this draft's.
- **C2 depth — _pending_.** The counter has not been run for the round and no counted verdict is claimed here; nothing
  is admitted by this draft. At both captures (05:27Z, 05:30Z) 10 of the 12 counted reports existed, no `V46Res*` seat
  was dispatched, and `w1-results.json` did not exist
  (`.ufo/waves/round-46/w1/ScribeLesson/c2-binding-state.txt`). Reading the reports' `SECTION SHA256` lines against the
  entry's own hashes (`--section-hash`, read-only): GR1 was unchanged by the `b57740c2` narrowing (`fe77ac76…f9ca8`, four
  `holds`); GR2 moved `a963df81…781 → 4bf28bcf…6da` and GR3 `8fa62676…800 → 43430a14…32c`, so every landed
  GR2/GR3 reader — the three `partly` **and** the two `holds` — now binds to bytes the entry no longer carries, and both
  rows sit at 0 matching seats where the predicate needs ≥ 2 `holds`
  (`.ufo/waves/round-46/w1/ScribeLesson/section-hashes.txt`). _The L1 states the measured `verdicts_ok` and, if it is
  below 3, the reason, and keeps GR1-GR3 pending rather than marking them admitted._

## Gate

### New SOURCES rows (F-1; _placeholder — the F-1 seat's live re-fetch had not landed when this draft was written_)

| Row | URL (access date) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S250 | _F-1_ | _F-1_ (≤25 words, located with `grep -n`) | _F-1_, `shell.c` / `general.c` / `general.h` at the lines the row's anchor names |
| S251 | _F-1_ | _F-1_ | _F-1_, `proc_pid_fd.5.html:72-81` |

What this draft does carry, verified by the lesson's seat: `corpus/SOURCES.md:259-260` at `a4477049` holds both rows,
and `git diff 2042117c a4477049 -- corpus/SOURCES.md` is 2 insertions and 0 deletions, so no old row's cell moved. The
frozen snapshot digests are `sha256sum -c .ufo/waves/round-46/frozen/src/SHA256SUMS` → 4/4 OK: `shell.c`
`5f3d539f…f73d`, `general.c` `669ef408…d165`, `general.h` `bf9251e3…f2f2`, `proc_pid_fd.5.html` `3a50ddef…27e`; the
fetch log is `FETCH.txt` (2026-10-27T04:59:34Z, tag `bash-5.3` peeled `b8c60bc9…c303`).

### Reject rows (F-1)

_placeholder — one candidate source or entry considered and refused this round, with reason and flip (the F-1 item names
the example class: a bash manual page that does not document the script descriptor). Rejects are recorded here, not only
under spot-check candidates (round-44 D8)._

### Re-opened rows and rows touched old→new (C2-S10; _placeholder_)

The SOURCES diff above proves that **no** old row's `used-by` cell changed this round; the rows below are re-opened for
evidence, not edited. The re-open receipts are the C2-S10 seat's:

| Row | used-by old → new | Log |
|---|---|---|
| S246 | unchanged (`corpus/knowledge/btrfs-scrub-grounding-r45.md`) | _C2-S10: live re-fetch of `lib/cmdline.c`, `lib/vsprintf.c`, `lib/kstrtox.c` vs `round-45/frozen/src/SHA256SUMS`_ |
| S247 | unchanged (same entry) | _C2-S10: live `fs/btrfs/dev-replace.c`_ |
| S248 | unchanged (same entry) | _C2-S10: live `man/systemd.kill.xml` at v262_ |
| S249 | unchanged (same entry, own-work capture) | _C2-S10 / C2ExecHostRecheck: read-only `systemctl show` behind the capture_ |
| S237 | unchanged (`btrfs-scrub-record-r42.md`, `-r43.md`, `-r44.md`, `btrfs-scrub-grounding-r45.md`) | _C2-S10: btrfs-progs 7.1 `scrub.c`_ |
| S242 | unchanged (`btrfs-scrub-record-r44.md`, `btrfs-scrub-grounding-r45.md`) | _C2-S10: `fs/btrfs/scrub.c`_ |
| S243 | unchanged (same two entries) | _C2-S10: `fs/btrfs/sysfs.c`_ |
| S244 | unchanged (same two entries) | _C2-S10: Arch units, three files_ |

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R46-C1-COUNTER-PATHHASH | control design — a must-FAIL control passed the frozen predicate (caught pre-data; the counter never landed in this state) | The first battery scored `K2-pathhash` `verdict: PASS`, `as_expected: false`, every leg 1, `selftest_r46 5` (`controls/battery-summary-c1-draft1.jsonl:3`); with `${BASH_SOURCE[0]:-}` the stdin and pipe legs never name a regular file, so a path hasher and the descriptor reader agree there (`SCORECARD.md:2994-2996`). The frozen battery kills it: `unverifiable_ok 0`, `selftest_pass 0`, `verdict FAIL` (`controls/battery-summary-c1.jsonl:3`), 9/9 as expected against draft1's 8/9 | pre-data battery, before the freeze and before any seat; re-caught in-wave by `w1/C1CritControls.md:5` and read the same way at `w1/C1CritClaim.md:8` | The frozen counter adds the shape that separates path from descriptor — the script's first line renames a decoy over its own path, so the path names new bytes while bash keeps the old inode (`tools/score-census-identity-r46.py:199-209`) — and the candidate gained the matching `(R46-C1)` case (`tools/tsukuroi-census.sh:3441-3446`). Able to fail: the draft1 row is the red shape (PASS on a must-FAIL control) and the frozen row the green one, while control K8 (candidate) still PASSes (`:8`) — the leg kills the mutant, not the candidate |
| R46-CENSUS-STDIN-UNBOUND | latent shell defect under `set -u`, never exercised by any test since the file became executable | `bash -s -- --identity < base-census.sh` at `2042117c` → `bash: line 455: BASH_SOURCE[0]: unbound variable`, rc 1 (`w1/ScribeLesson/stdin-unbound.txt`); the unguarded assignment landed in the commit that created the file, `5f906451` ("probation round 2", 2026-10-14 11:17:42 -0300), and `git log -S'SELF=${BASH_SOURCE[0]}'` names only that commit and `a4477049`, so it was present at every revision in between (22 commits touched the census in `5f906451..2042117c`); `git show 2042117c:…\|sed -n 455p` reads the unguarded line at exactly the number the runtime error names; the base file invokes itself from stdin nowhere (`grep -c 'bash -s'` → 0), so no test could see it | no review seat: every seat that names it postdates the change (a base-vs-impl line table `w1/C1ExecAdjacency.md:101`, a positive review note `w1/C1RevImpl.md:14`, and the base-bytes control that witnesses the failure, `w1/C1ExecRerunA.md:70`); the discovery channel was the `--identity` implementation, which has to name what bash executes when bash holds no script file. Recorded by the lane at `corpus/knowledge/census-identity-r46.md:39-41` and as a one-line diff at `w1/C1ExecPlaneDiff.md:121` | `SELF=${BASH_SOURCE[0]:-}` (`tools/tsukuroi-census.sh:455`) plus a `(R46-C1)` case that runs `bash -s -- --identity` in a cwd holding a decoy regular file named `bash` and demands four `unverifiable` fields (`:3435-3439`), and the counter's `unverifiable_ok` leg, three stdin-shaped runs (`tools/score-census-identity-r46.py:185-215`). Able to fail: base bytes exit 1 with no line, the implementation prints the line with `verified=no` rc 0, and the base-bytes control K0 records `unverifiable_ok 0` (`controls/battery-summary-c1.jsonl:1`) |
| R46-SELFTEST-EOF-NEWLINE | file-shape hazard — the census's last line carries no newline, so an appended selftest case fuses into `main "$@"` | `tail -c1 tools/tsukuroi-census.sh \| od -c` → `"` with no `\n`, at base `2042117c`, at `a4477049` and at HEAD; appending one line with no leading newline turns the last line into `main "$@"<appended text>`, so `^main "\$@"$` matches 0 times instead of 1 and the copy exits 2 (syntax error, or usage when the appended text has no metacharacter, or usage instead of running the selftest for a real case line) (`w1/ScribeLesson/eof-fusion.txt`) | the L1 while drafting the cases: the work-around is in the same commit in three places — `tools/tsukuroi-census.sh:3410` "the census ends without a newline", `tools/score-census-identity-r46.py:148-150` "leading newline: the census may end without one", `controls/make_c1_variant.py:47` | No gate exists, and that is the row: no checker in `tools/` or `scripts/` reads a tool file's last byte (`grep -rln 'endswith(b"\\n")' tools/*.py scripts/*.sh` → none; the four `newline` hits in `tools/` are first-line capture and receipt text, `tools/score-census-readers-r45.py:25,196,271`). The candidate fix is a newline-termination check over `tools/*.sh`; it is **not yet able to fail** because it is not written, and appending the byte instead is refused here — it would invalidate the census sha256 the round-45 and round-46 receipts, `SKILL.md` and `LOG.md` quote |

## Round-45 routed defects — round-46 disposition (at `b57740c2`)

| Defect | State | Evidence |
|---|---|---|
| D1 R45C-D3-R44-MARK-SWEEP | **partial** | `corpus/README.md:465-466` marks the **round-45** rows FAILED/pending — the pair `194a4523` added — but the **round-44** scrub row (`corpus/README.md:434`) and its paragraph `:440-452` carry no status (`git show <REV>:corpus/README.md \| sed -n '427,452p' \| grep -c -i -E 'fail\|pending\|admit'` → 0 at `a4477049` and at `b57740c2`), and the SKILL section listing SR7-SR9 (`SKILL.md:4214-4231`) has no mark (`grep -c 'FAILED\|pending'` → 0). Round 44's depth gate also FAILED (`corpus/lessons/round-44-verifier-spotcheck.md:81`), so those rows read as admitted. Note the scope: the round-45 lesson's own D3 row (`corpus/lessons/round-45.md:94`) is accurate about the round-45 rows it names; it does not cover this |
| D2 R45C-D7-CITATION | closed at `b57740c2` | Appended notes at `.ufo/waves/round-44/w1/C1ExecLiveRead/commands.txt:88` and `.ufo/waves/round-44/w2/SkillReview.md:104` name the `.log.gz`; `git cat-file -e HEAD` is 128 for the `.log` and 0 for the `.log.gz`; both files left `git status --porcelain` at `b57740c2` (`git diff --stat a4477049 b57740c2` → +2, +2) |
| D3 R45C-ASMGATE-RECEIPT | closed at `b57740c2` | The recount paragraph in `.ufo/waves/round-45/a2w1/AsmGate.md` (+56 lines in that commit) replaces 183/147/30 with 249/147/50 at `44560592`, names the five non-registry ids in `id-collisions.txt` and points at `assimilation/collisions` |
| D4 R45C-START-CENSUS | closed | `before/sources-census-start.txt:1` stamps 2026-10-27T04:49:57Z, run by this attempt at its own start, with the command and the W04 warning set on the following lines |
| D5 R45C-POSTFREEZE-NAME | closed by design, limit disclosed | The frozen C2 counter binds seat names across **any** wave name, so a retired wave cannot strand it (`tools/check-scrub-admission-r46.py:18-19`); control K15 (records under an arbitrary wave name) PASSes as expected (`controls/battery-summary-c2.jsonl:16`). The standing limit is the round-45 forgery one, restated in the counter (`:42-43`) |
| Carried: re-bind GR1-GR3 on a channel the seat writes itself (QUALITY 93) | form closed, verdict pending | The channel is the seat's own report file, first two lines frozen, bound to the row's section hash (`tools/check-scrub-admission-r46.py:21-32`); whether it binds is the round's C2 outcome. _Binding arithmetic at `b57740c2` (read-only `--section-hash`): the narrowing moved GR2 `a963df81… → 4bf28bcf…` and GR3 `8fa62676… → 43430a14…`, so all five landed GR2/GR3 readers — the three `partly` and the two `holds` — now bind to bytes the entry no longer carries; both rows are at 0 matching seats where the rule wants ≥ 2 `holds`, and the only path left is a residual pair (`V46ResRevGR<n>`/`V46ResCritGR<n>`, control K18) in a second `<wave>-dispatch.json`, since none is in `w1`_ |
| Carried: the C1 review gaps (`a2w1/C1CritCases.md`, `C1RevKillRules.md`) | still open, re-reviewed this round | The two round-45 files exist (`.ufo/waves/round-45/a2w1/`); this round's C1 critics re-raise the same class — `w1/C1CritControls.md:13` asks for per-leg fixture variants (path hashing, absent `readlink` verification, fd≥255 search, a cache-file writer) and notes the battery "demonstrates rejection, not isolated leg attribution" |
| Carried: the `C2MutBinding` survivors | re-run this round | Item `C2MutBinding` is in the `w1` dispatch; its survivors are its own report's material |

Conflicts recorded verbatim for the canonical judge:

- `w1/AsmGate.md:11` calls the 52-id overlap "a defect in the merge's continuous S-ID assumption"; the same set now
  includes S250/S251, which this round minted — and the round-45 lesson's D9 row records the intersection as 50
  (S200-S249). Both statements are true at their own revisions; the pair must not be read as one number.

## Assimilation and considerthese

Assimilation: **none**. The package is `/home/vgpnk/Projects/shokuknow/merge/tsukuroi` (read-only); there is no `merge/`
directory in the lane or at the fleet root, and no campaign tool was run. Id check with the prompt's 0-3-space
extractor at `a4477049`: lane registry 251 ids, staged 147, intersection **52** (`w1/AsmGate.md:9-11`, receipts
`w1/AsmGate/{reg-ids,staged-ids,collisions}`), re-derived independently by the round-46 lesson seat. The guard is proved
on a scratch registry row `  | S002 |`, which the extractor reports. The two ids minted this round, S250 and S251, are
already staged ids (the zh_CN and ja_JP translation rows at `merge/tsukuroi/SOURCES.append.md:57-58`), so any landing
renumbers by document (round-45 D9, widened by two). No staged theme fits the round's surfaces (`w1/AsmGate.md`
"Theme recommendation"). Quarantine slice: 12 rows (`w1/AsmGate/quarantine-slice`); none was hand-checked this round, so
none is appendable and nothing was appended.

### considerthese — seat-harm incident log

The newest mined file is `considerthese/2026-10-26.md` (mined in round 45; its "Seat-harm incident log" proposal is the
ledger in `corpus/lessons/round-45.md` §Assimilation, ten incidents over rounds 37-44 with a 15-mutant kill set). No
2026-10-27 file exists yet; this round's mining is seat `ConsiderMine`. The ledger's own closing sentence still holds and
is the item to re-read: no gate reads it — `git grep -l seat-harm -- tools SKILL.md corpus` returns only the lesson
prose (`corpus/lessons/round-45.md`), and a grep for `seat-harm` finds no gate in `tools/`. Rule carried: a seat-harm fix
counts as landed only when the incident's own site refuses the old shape and a receipt shows red before green; prose is
`rule-only`, a removal is not a fix.

## Spot-check candidates for the non-author closure

Admits: S250 (GNU bash `bash-5.3` `shell.c`/`general.c`/`general.h`) and S251 (`proc_pid_fd(5)`) — _pending F-1's live
bytes against `frozen/src/SHA256SUMS`; the frozen digests themselves verify 4/4 locally_. The C1 capability
(`--identity`) is the round's operability move and is a candidate for the closure's own re-measurement, not a source
admit. Rejects: _F-1_ (at least one source or entry refused with reason and flip). Not an admit: GR1-GR3 — the depth
gate's verdict is pending, and at `b57740c2` the narrowing left GR2 and GR3 with **zero** seated readers on their current
section hash (the five landed GR2/GR3 readers all bind the pre-narrowing bytes), so neither can reach the rule's ≥ 2
`holds` without a residual pair. Watch for the closure: the double-hash window (`w1/C1CritRace.md:7`) is already stated
in the entry's Limits, so quote the Limits rather than grading it twice; bind the three rows against `b57740c2`'s bytes,
not the intent; and treat the uncommitted census edit as a measurement hazard — a receipt that quotes the census sha256
must name the commit it read, since the working tree carried `48dd828b…e66d` against the committed `d925839c…2cfa`.
```

---

## Receipts

Under `.ufo/waves/round-46/w1/ScribeLesson/`:

| File | What it is |
|---|---|
| `coordinates.txt` | lane HEAD and log, census sha256/size, the two frozen counter digests, `git log -S'SELF=${BASH_SOURCE[0]}'`, `blame -L 451,456`, base `:455`, the 22-commit count, the EOF byte at base/impl/HEAD, the base file's `bash -s` count (0), `R46-C1` label count, the implementation receipt's legs and selftest line, the round dir's contents (no `after/`), and the working-tree state |
| `stdin-unbound.txt` | base vs implementation under `bash -s -- --identity` (rc 1 with `unbound variable` vs rc 0 with `verified=no`), the guard at `:455`, the entry's own record (`:39-41`), and the seat's diff line (`C1ExecPlaneDiff.md:121`) |
| `eof-fusion.txt` | the last byte and last line, three appended-line shapes with their exit codes, the exact-match counts (1 → 0), the three work-arounds (`census:3410`, counter `:148-150`, generator `:47`), and the absent newline checker |
| `k2-draft-battery.txt` | the draft1 and frozen K2 rows, `as_expected` totals for all three batteries (8/9, 9/9, 22/22), the SCORECARD's fix paragraph, the separating leg, and the seat's re-catch |
| `c2-binding-state.txt` | two captures (05:27Z, 05:30Z) of the twelve counted names with their first two lines and hashes, the six residual names (all absent), the dispatch's 66 tasks with zero `V46Res*`, and the missing `w1-results.json` |
| `section-hashes.txt` | `--section-hash` at `a4477049` and at `b57740c2` (read-only, exit 0), the distinct `SECTION SHA256` values the landed reports carry, the narrowing commit's stat, and the uncommitted census edit's stat |
| `ids-collision.txt` | 251/147/52 re-derived, S250/S251 as staged rows, the AsmGate receipt sizes, the seat's own figures, and the package's location |
| `routed-defects.txt` | D1-D5 evidence (README marks, SKILL section count, D2 corrections and `cat-file` results, D3 modification + recount paragraph, D4 start stamp, D5 any-name rule and K15 row, the SOURCES 2-insertion diff) |

Scratch `/fast/scratch/hyaku/tsukuroi-r46/ScribeLesson/` (base and implementation census copies, the three fused copies)
was removed after the receipts were written. No tool was installed or upgraded by this seat.
