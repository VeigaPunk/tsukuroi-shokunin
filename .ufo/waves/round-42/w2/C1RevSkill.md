VERDICT: defect-found

# C1RevSkill — item F-8: the round-42 SKILL.md sections appended at 78abb8b5

Seat C1RevSkill (L2 leaf, tsukuroi r42 hyaku 9, wave w2). Reviewed text: `## Census early readers under pipefail — round 42` (SKILL.md:3851-3894), `## Scrub status record — round 42` (:3896-3924), `## Counter lineage — round 42 rows (append-only continuation)` (:3926-3931), `## Counter-attack scoreboard — round 42 (continuation)` (:3933-3941), and the two registry rows after `| package-anatomy-r41 |` (:3122 `scrub-record-r42`, :3123 `size-invariance-r42`) — all at 78abb8b5cdc9da511b4fc523e661517a68dd33d3.

Ground truth used: the census at 78abb8b5 (blob `18a1db64`, 3220 lines), the base census `c8efaa3f` (blob `dda066f4`, 3176 lines), the first-fix census `44766208` (blob `ed83079c`), `git diff c8efaa3f 78abb8b5 -- tools/tsukuroi-census.sh`, the entry `corpus/knowledge/btrfs-scrub-record-r42.md`, both frozen counters' sources, `corpus/QUALITY.md:177`, `corpus/SOURCES.md:246-248`, `SCORECARD.md:2560-2595`, `LOG.md` (tip), the frozen snapshots and capture, the controls, and every wave-1 report the sections cite (C1SweepSites, C1RevFix, C1ExecAbleToFail, C1MutSelftest, C1MutSites, C1CritNsView, C1CritEvasion, ConnClaims, C2CritControl, C2MutCounter, C2ExecHostRecheck, ScribeSkill) plus `w1-results.json`. Method: `git show`/`git archive` into scratch only (no lane write, no mutating git in the lane); static line-number and count checks; one scratch bash repro of the two SIGPIPE signatures. No frozen counter was run (other seats own them; one-at-a-time rule). No tool installed or upgraded (nothing needed — no tooling record). Scratch `/fast/scratch/hyaku/tsukuroi-r42/C1RevSkill` removed after receipts were copied. Receipts: `.ufo/waves/round-42/w2/C1RevSkill/` (7 files, each < 11 KB).

## Findings (each with the exact replacement text)

### F1 (defect) — "With the base plane bodies swapped in, exactly those cases fail" cites a receipt that shows two of the four, measured on the first-fix census, not this one

SKILL.md:3876-3879:

> Selftest: 128 → 132 cases, four `R42-C1` cases (a large error-bearing `-Qkk` sample; 4002 equal candidates on `-Qu`/`-Sup`/`-Suu`; a large `-Sup` against an empty `-Qu`; a large `-Sup` against a two-line `-Qu`). With the base plane bodies swapped in, exactly those cases fail (`impl/c1-able-to-fail.txt`; wave-1 `C1ExecAbleToFail`, `C1MutSelftest`: every one of the six single-site reverts is now killed).

"those cases" = the four `R42-C1` cases of the 132-case suite just enumerated. The cited `impl/c1-able-to-fail.txt` is unchanged since the first fix (`git log --follow` → only 44766208; `git diff 44766208 78abb8b5 -- <file>` empty — receipt `able-to-fail-stale.txt`): it records the hybrid built from the **4476620** census (impl sha `46d62a24…`, hybrid sha `a8fbfd51…`), 130 cases, and exactly **two** `R42-C1` failures — the two cases that existed at that commit. The other two `R42-C1` cases (the two `-Sup` disagreement arms) did not exist there; wave-1 `C1ExecAbleToFail` §2 found the `-Sup` reverts **surviving** that 130-case suite, and `C1MutSelftest` §4.1 demonstrates the two added cases red on each revert and green with them integrated (131-case runs) — composition supports "all six reverts killed by the integrated suite", but no artifact at 78abb8b5 runs the base-body hybrid against the **tip** census, and the only able-to-fail artifacts under `.ufo/waves/round-42/` at 78abb8b5 are the first-fix ones (receipt `able-to-fail-stale.txt`; the w2 spec contains no able-to-fail item).

Replacement (SKILL.md:3877-3879, keeping the first line):

> `-Qu`/`-Sup`/`-Suu`; a large `-Sup` against an empty `-Qu`; a large `-Sup` against a two-line `-Qu`). With the base plane bodies swapped into the first-fix census, exactly the two `R42-C1` cases that existed there fail (`impl/c1-able-to-fail.txt`, recorded at `44766208`; wave-1 `C1ExecAbleToFail` reproduced it byte-exactly); the two `-Sup` disagreement reverts survive that 130-case suite, and wave-1 `C1MutSelftest` demonstrates the two added cases red on each of those reverts and green with them integrated — so all six single-site reverts are killed by the integrated suite.

### F2 (defect) — "QUALITY 90 makes those channels frozen controls" — the round-42 battery fields no such controls; the criterion's own failing examples are this round's counters

SKILL.md:3940-3941 (scoreboard Reading paragraph):

> Reading: the metamorphic oracle removed the answer key, and the hole moved to the channels through which the code can see it is observed. QUALITY 90 makes those channels frozen controls.

The round-42 pre-data battery is C1-K0…K8 and C2-K0…K5 only — no K9/K10 (uid-0-gated, data-gated arms) exists (`git ls-tree 78abb8b5:.ufo/waves/round-42/controls/`; `battery-summary-c1.jsonl` lists K0-K8 — receipt `controls-listing.txt`), and `corpus/QUALITY.md:177` names this round's counters as its **failing examples** ("Failing examples (round 42): the C1 counter's namespace legs ran as uid 0 … the C2 counter's unanchored `ROW SC<n> VERDICT:` match counted as `holds` a critic's sentence that quoted the holds line"). As written, the sentence asserts a state (those channels are frozen controls) that does not hold for the counters this scoreboard row is about.

Replacement (SKILL.md:3941):

> see it is observed. QUALITY 90 requires those channels to become frozen pre-data controls; the round-42 battery does not field them yet (no K9/K10 beside `controls/C1-K0-K8.jsonl`), so the channels stand reported open — the criterion's own failing examples are this round's counters (`corpus/QUALITY.md:177`).

### F3 (citation defect) — "foreign baseline lookup `:743`" is not the base line number

SKILL.md:3864 (table column "Seen at the base"):

> | a `$( … )` assignment | `set -e` kills the census: exit 141, header line only | `-Qu`/`-Sup`/`-Suu` name extraction `:1621`, `:1635`, `:1641`, `:1652`; foreign baseline lookup `:743` |

The four update-safety numbers are base numbers (verified: `grep -n` on `git show c8efaa3f:tools/tsukuroi-census.sh` → :1621, :1635, :1641, :1652 — receipt `line-numbers.txt`). The foreign-baseline lookup (`bn=$(printf '%s\n' "$base_txt" | awk … '$1 == n {print $2; exit}')`) is at base **:740**; :743 is the first-fix (4476620-blob) number — the numbering `C1SweepSites` and the integration commit message ("`:743` lookup full read") use — and the tip line is :746. One cell mixes two revisions' numbering under a "Seen at the base" header.

Replacement (SKILL.md:3864, cell tail): `foreign baseline lookup `:743`` → `foreign baseline lookup `:740``.

### F4 (citation defect) — the five single-line probe readers are cited at first-fix numbers, stale at this commit

SKILL.md:3893:

> boot start (wave-1 `C1SweepSites`); the single-line probe readers (`:931`, `:969`, `:1051`, `:1426`, `:1501`) keep the early reader on inputs that cannot reach 30 KB.

Present tense about the current census, but those are the 4476620-blob numbers (C1SweepSites/C1RevFix numbering). At 78abb8b5 the same five sites are **:934, :972, :1054, :1429, :1504** (`grep -n 'head -n1'` on the tip census — receipt `line-numbers.txt`). The substance (five `$(printf … | head -n1 …)` assignments on single-line probes, unreachable size) is correct per `C1SweepSites` §Site table.

Replacement (SKILL.md:3893): `(`:931`, `:969`, `:1051`, `:1426`, `:1501`)` → `(`:934`, `:972`, `:1054`, `:1429`, `:1504` at this commit; `:931`, `:969`, `:1051`, `:1426`, `:1501` at the first fix `44766208`)`.

### F5 (forward reference) — "its hash is in `LOG.md`" is not yet true at this commit

SKILL.md:3854-3855:

> hardening). Defect R41-CENSUS-PIPEFAIL-692. Base `c8efaa3f`; first fix `44766208`; hardened at the round-42 integration commit (its hash is in `LOG.md`).

`LOG.md` at 78abb8b5 ends at the round-41 entry; there is no round-42 entry (`grep -n '## Round'` → last is `## Round 41` at :1534; no `Round 42`/`round-42` hit — receipt `tree-evidence.txt`), and a commit cannot carry its own hash. The round-42 LOG entry lands at the round close per the lane's "(stamp: the commit that lands this entry)" convention.

Replacement (SKILL.md:3855): `integration commit (its hash is in `LOG.md`)` → `integration commit (this commit; the round-42 `LOG.md` entry, landed at the round close, names it)`.

### F6 (forward reference) — the Evidence list names `w2/` and `after/`, absent from this commit's tree

SKILL.md:3855-3856:

> Evidence: `.ufo/waves/round-42/` (`before/`, `controls/`, `impl/`, `w1/`, `w2/`, `after/`).

At 78abb8b5 the tree has `before/`, `controls/`, `frozen/`, `impl/`, `w1/` — no `w2/`, no `after/` (`git ls-tree --name-only 78abb8b5:.ufo/waves/round-42/` — receipt `tree-evidence.txt`). Both appear only in the working lane after this commit (`after/` is landed by the after-receipt commit `a968393c`, `w2/` by this wave's integration). The wave-1 scribe explicitly flagged the `after/` receipt as not-yet-existing and warned not to let the section stand as a claim about it (`w1/ScribeSkill.md` finding 2).

Replacement (SKILL.md:3855-3856):

> Evidence: `.ufo/waves/round-42/` — `before/`, `controls/`, `impl/` and `w1/` exist at this commit; `w2/` (this wave's reports) and `after/` (the round-close receipt) land with the wave-2 integration and the round close.

### F7 (unsupported) — "the file exists (SC4)" is neither in the entry nor guaranteed by the pinned code

SKILL.md:3907:

> | open fails with an errno other than `ENOENT` | status warns and exits with an error; the file exists (SC4) | re-read with the owner's privileges before writing "no record" |

The entry's SC4 says only: "an open failure of `ENOENT` is not an error; any other open failure prints a warning and the command exits with an error" — no existence claim. The pinned code (`frozen/src/scrub.c:1931` `if (fdres < 0 && fdres != -ENOENT)` → `warning("failed to open status file: %m")`, `err = 1`) branches on the errno alone; e.g. `EACCES` on a non-searchable parent directory leaves the file's existence unknown, so "the file exists" overstates what SC4 carries. (The wave-1 draft had the same over-claim with an SC1 citation; `w1/ScribeSkill.md` draft (b).)

Replacement (SKILL.md:3907, Reading cell): `status warns and exits with an error; the file exists (SC4)` → `status warns and exits with an error; the record's absence is not established (SC4)`.

### F8 (precision defect) — lineage row 15: "still admits a fix gated on uid 0" — no fielded arm is uid-0-only, and a uid-0-only gate fails

SKILL.md:3930 (row 15 tail):

> … still admits a fix gated on uid 0 or on the fixed fixture names, and a grammar-complete padding filter

The ten fixture legs run as the invoking user (uid 1000) with `TSUKUROI_FIXTURE` set (`w1/C1CritNsView.md` §5: "Every U1-U4 fixture runs with `TSUKUROI_FIXTURE` set"), so a census gated **only** on uid 0 takes the unfixed branch there and fails the large twins. The fielded admitted arms gate on `TSUKUROI_FIXTURE`-or-uid-0 (V1/V2, `C1CritNsView` §3) or on fixture-env-or-(uid 0 **and** the `/usr/bin/pacman` mountinfo line) (V1i, `C1CritEvasion` §1), or on the four fixed fixture names (V3). The row also omits the size-gate admission (`C1CritEvasion` V2, PASS — recorded as a passing variant in `w1-results.json`). An attacker working from the row as written would try a uid-0-only gate and fail.

Replacement (SKILL.md:3930, row tail):

> … still admits a fix gated on the fixture environment or on the counter's uid-0 namespace view (`TSUKUROI_FIXTURE` set, or uid 0 — V1/V2; uid 0 with the `/usr/bin/pacman` mountinfo line — V1i), on the four fixed fixture names (V3), and a size gate at the pipe capacity (V2) or a grammar-complete padding filter (K5Z)

### F9 (precision defect) — scoreboard row: "2 sniffer variants (`w1/C1CritEvasion.md`)" and the PASS cell drop arms that report shows

SKILL.md:3937:

> | `score-size-invariance-r42.py` | r42 | 6 single-site reverts (`w1/C1MutSites.md`), 3 view-gated + 1 data-gated (`w1/C1CritNsView.md`), 2 sniffer variants (`w1/C1CritEvasion.md`), 3 padding filters (`w1/ConnClaims.md` K5X-K5Z) | 5 (V1, V2, V3, V1i, K5Z) | observation-channel read (uid 0, the fixture names, the counter's padding grammar) |

`w1/C1CritEvasion.md` fielded **four** arms (§9 evidence index): V1 (top-level gate — counter PASS, refused only by the diff kill rule), V1i (the two uid-0/mountinfo sniff lines — PASS), V1n (sniffer-removed control — FAIL), V2 (size gate at the pipe capacity — PASS). The L1's own `w1-results.json` records C1CritEvasion's passing variants as V1i **and V2**; the scoreboard's PASS cell lists five arms and omits C1CritEvasion's V2 (and, if "reached PASS" means the counter's verdict, V1 as well). The sibling columns enumerate exhaustively (the rounds-40-41 rows do), so this cell undercounts on any exhaustive reading.

Replacement (SKILL.md:3937):

> | `score-size-invariance-r42.py` | r42 | 6 single-site reverts (`w1/C1MutSites.md`), 3 view-gated + 1 data-gated (`w1/C1CritNsView.md`), 4 evasion arms — V1 top-level gate (counter PASS, refused by the diff kill rule), V1i with the two uid-0/mountinfo sniff lines (PASS), V1n the sniffer-removed control (FAIL), V2 a size gate at the pipe capacity (PASS) (`w1/C1CritEvasion.md`), 3 padding filters (`w1/ConnClaims.md` K5X-K5Z) | 6 (C1CritNsView V1, V2, V3; C1CritEvasion V1i, V2; ConnClaims K5Z) | observation-channel read (uid 0, the fixture names, the counter's padding grammar) |

### F10 (precision defect) — registry row `scrub-record-r42` drops the committed-report leg of the verdict binding

SKILL.md:3122 (verdict-map cell):

> … five wave-2 seat verdicts bound through `w2-dispatch.json` and `w2-results.json`; …

The binding is through dispatch **+ results + the committed report**: `bound()` requires `w2/<name>.md` to carry the identical line (`tools/check-scrub-record-r42.py:133-136`), and the SKILL body states all three ("binds the ten wave-2 seats through `w2-dispatch.json` + `w2-results.json` + the committed report", SKILL.md:3921-3922). The registry row names two of the three.

Replacement (SKILL.md:3122, cell fragment): `five wave-2 seat verdicts bound through `w2-dispatch.json` and `w2-results.json`` → `five wave-2 seat verdicts bound through `w2-dispatch.json`, `w2-results.json` and the committed `w2/<seat>.md` report`.

## Minor notes (wording suggestions, not false sentences)

- N1 — SKILL.md:3864: the assignment-signature row's base examples omit the packages `:694` `grep -m1` note assignment, which is also seen at the base and also kills with 141 (wave-1 `C1MutSelftest` mut694: "the census child died of SIGPIPE (141) in the reverted command-substitution assignment"). Suggested cell addition: `; packages `:694` (`grep -m1` in the `PKG_NOTE` assignment)`.
- N2 — SKILL.md:3906: "a run with recording disabled, or driven through the ioctl, leaves no file" — the entry marks the ioctl-driven case "[inference from the write path]" (entry SC3); the SKILL states it as fact. Suggested: "a run with recording disabled — or, the entry's inference from the write path, one driven through the ioctl — leaves no file".
- N3 — SKILL.md:3921-3924: the Known-limit sentence presents `transcripts_bound` as the cross-check on forged records. Per wave-1 `C2CritControl` D4 the cross-check cannot falsify a bound verdict (it is evaluated only on already-bound lines) and a planted seat-named file satisfies it (M15: `PASS transcripts_bound 10/10`); suggest appending: "; the cross-check cannot falsify a bound verdict and a planted seat-named file satisfies it (`C2CritControl` D4)".

## What checked out (verified, no finding)

- **Census mechanics.** `set -euo pipefail` at tip :423; the two signatures reproduce in a scratch repro (error-first 1.5 MB buffer: `if printf | grep -q` → CLEAN-branch wrong verdict; `grep -m1`/`head -n1` assignment forms → rc 141 — receipt `sigpipe-repro.txt`), matching wave-1 receipts (`C1MutSelftest` mut692/mut694, `C1RevFix` T9a/T9b).
- **Base sites.** :692 `printf | grep -q '^error:'` and :694 `grep -m1` (packages), :1621/:1635/:1641/:1652 `head -n3`/`head -n1` (update-safety) — all verified at base (receipt `line-numbers.txt`); the packages row's "read `HEALTHY` (P1, P3, P6)" matches `before/c1-before.jsonl` (`P1/P3/P6 large_rc=0`) and `C1MutSites` m1.
- **Threshold sentence.** "8 of 300 at 32 KB, 300 of 300 at 304 KB" matches `C1SweepSites` §Evidence 1 verbatim (32422 B: 8; 303814 B: 300; "false pipeline status starts around 30 KB"; "printf writes in 4 KiB stdio chunks").
- **The awk rule and forms.** All five quoted forms match the tip census exactly (:698 awk error test, :746 lookup without `exit`, :1627/:1642/:1648 `NR <= 3`, :1658 `NR == 1`).
- **Here-string warning.** Matches `C1RevFix` D1 exactly (65485 B → pipe, 65561 B → temp file; full `$TMPDIR`/`/tmp` → redirection failure → `if` takes the clean branch → `HEALTHY` exit 0, E3/E4); "the first fix used here-strings; the integration replaced them with the awk test" matches both diffs.
- **Selftest counts.** base 125 `check` + 3 `check_cli` = 128; first fix 127+3 = 130; tip 129+3 = 132 (receipt `selftest-counts.txt`); exactly four `R42-C1` labels at tip (:2360, :2567, :2577, :2584) with the four described shapes.
- **Counter (C1).** sha256 `c511104a…53e03` at tip = frozen declaration; predicate sentence verbatim (`:43`, `:365-370`); no expected verdict; ten P1-P6/U1-U4 twins; three `unshare -rm` legs N1/N3/N6 as uid 0 with the fixed `alpha beta gamma delta` names; `PAD_BYTES = 1 << 20`; fixtures built from the base census; exit 0/1/2; usage matches both the section and registry row. Refuses the six single-site reverts (`C1MutSites`: all six FAIL, six of six). Sufficiency falsifiers verified: V1/V2/V3 (`C1CritNsView` §3 PASS), V1i (`C1CritEvasion` §1 PASS, prodpath shows the production defect), K5Z (`ConnClaims` §3 PASS).
- **QUALITY 90 and the setpriv sentence.** `corpus/QUALITY.md:177` says exactly "a leg offered as 'a view the code cannot tell from production' runs at the production identity … or it is named an override-free leg and its channels are reported open"; the uid-1000 `setpriv` measurement is `C1CritNsView` §4 and is not in the predicate.
- **boot-chain-audit routed defect.** `tools/boot-chain-audit.sh:480-487` is the `find … -print -quit 2>/dev/null | grep -q .` block under `set -uo pipefail` (:139), unchanged since base (empty `git diff c8efaa3f 78abb8b5 -- tools/boot-chain-audit.sh`) — "Not fixed here (routed)" is accurate; the failure mode matches `C1SweepSites`'s reproduction.
- **Scrub section vs the entry.** All 28 quote lines of SC1-SC5 resolve exactly on their named lines of the pinned snapshots (`frozen/src/scrub.c`, `CHANGES` — checked every one); S237/S238/S239 match `corpus/SOURCES.md:246-248`; all thirteen table rows match the entry's SC1-SC5 statements except F7's "the file exists"; "The Arch build 7.1-1 applies no patch" matches the entry's Limits and `C2ExecLiveSources` §3 (`source=()` names the v7.1 tag, no `*.patch`, `prepare()` never invokes `patch`); the host sentence matches `capture.txt:6-10` (absent dir, timer disabled, `journal_scrub_lines 0`, limit 0) and `C2ExecHostRecheck` §2 (`btrfs scrub status /` unprivileged, exit 0, `no stats available`); "stored-data integrity stays `UNVERIFIED` (SH4)" matches `storage-health-r26.md` SH4 (Verdict `UNVERIFIED`).
- **Counter (C2) and registry rows.** sha256 `dbe933ec…0503f` at tip = frozen; predicate verbatim; `--revision [--lane] [--sessions]`; no self-test mode (either counter); committed Git reads only; `VERDICT_RE` unanchored + substring report test (= "matches the verdict string anywhere in the output and the report", `:66`, `:134`); binding through dispatch+results+report (`:119-136`); C2-K3 PASS with `transcripts_bound 0` (controls receipt); lineage rows' K1/K2/K3/K7/D1 attributions match the declaration's controls paragraph (`SCORECARD.md:2586-2591`); row numbering 15/16 continues the round-41 table (row 14); both registry rows' commands, predicates, self-test and write-scope cells match the counter sources.
- **Provenance sentences.** "wave seat ScribeSkill drafted, the L1 integrated and updated it for the wave-1 hardening" / "trimmed it to the integrated entry" match `w1/ScribeSkill.md` (drafts (a)/(b) and its findings list).

## Not done

- Neither frozen counter was run (the C1 counter takes minutes and several CPUs; other seats own the re-runs) — the counter claims above are verified from the sources, the committed control/before receipts, and the wave-1 reports, not re-executed.
- The census `--selftest` was not executed at any revision (case counts verified statically from `check`/`check_cli` call counts; the wave-1 receipts record the runs).
- The base-body hybrid against the **tip** census was not built or run — that is exactly the gap F1 reports.
- The entry's quotes were checked against the pinned snapshots only (line resolution); the C2 row-verdict seats own the row-level judgment.
- No web fetches; no tool installs (nothing needed, so no tooling record).
