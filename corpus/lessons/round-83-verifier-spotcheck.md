# Round 83 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Subject: tsukuroi round 83, attempt 1. Lane tip `a1b8191c3e4f99a744efad82e9aec8e13a46c963`; frozen declaration `d78b3b3982b5df62286dd65b0a42ae8a91847608`; pre-round tip `a8598038dbcbaa07d4b5899b647bf30aa81e9e3f`. Report `.ufo/reports/round-83/tsukuroi.md` (landed in fleet commit `5b7268d5595544d628552e613472a507cec06060`, author `tsukuroi-shokunin <tsukuroi@shokunin.local>`).

Method: the lane's gate (`tools/round83-battery.py`) was **not executed**; committed receipts were read and compared (PROTOCOL §Gate standard). Plain measurements were run over committed bytes. The mandated census command was run.

## 1. Conformance (step 1)

| Check | Command / evidence | Result |
|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-83/tsukuroi.md` | `tsukuroi-shokunin 5b7268d5…` ✓ |
| Required sections, in order | read of the report | Work performed, Landed changes, Before → after, Sources & frontier, Trend verdicts, SHONEN present ✓ |
| `## SHONEN` heading, one line per box | read of the report | 4 boxes, all `[~]` with pointers ✓ |
| Cited commits exist and are ancestors of the branch | `git merge-base --is-ancestor <h> refs/heads/master` for `d78b3b39`, `a1b8191c`, `a8598038` | all three `EXISTS ancestor-of-master` ✓ |
| Lane pushed, no round leftovers | `jj-lane.sh state …tsukuroi-shokunin` → `branch=master local=a1b8191c… remote=a1b8191c… ahead=0 behind=0 tracked=0 untracked=0`, rc 0; `git status --porcelain` empty | ✓ |
| Dispatched prompt carries the template contract | `.ufo/prompts/tsukuroi-round-83.md` §1–§5 match `templates/round-prompt.md`; §6 addendum present; five child-lane items present | ✓ |
| L2 floor | 13 seats (report, Wave) ≥ 8 | ✓ |
| Role split | prompt §3 requires 1× planner; report says the L1 held the planner seat (validator forbids the role) | **conformance defect**, named, status-neutral |
| Dispatch digest (`.ufo/watchdog.log` is mutable; digest is the pointer) | `2026-11-05T04:18:34-03:00 launch tsukuroi round=83 pgid=2188625 driver=hyaku-inline attempt=1` and `2026-11-05T05:33:10-03:00 complete tsukuroi round=83; hyaku-inline attempt=1` | launch and complete both present ✓ |

Status: **ok**. Real report, real committed work, verified hashes, clean tree. Defects are in notes below.

## 2. Claims re-check

Committed receipts read with `jq` (`.ufo/waves/round-83/before/`):

| Claim | Before: do-nothing r82 counters at `a8598038`, `battery-do-nothing-r82-at-tip.json` | After: r83 counters at `a8598038`, `battery-candidate-r83-at-tip.json` | Report says | Agrees |
|---|---|---|---|---|
| C1 depth | `passed 2 of 3`; C1.a rc 0, count 8, `met`, verdict miss | `passed 3 of 3`; C1.a rc 2 `snapshot-digest-mismatch` | 2/3 → 3/3 | yes |
| C2 calibration | `passed 1 of 4`; C2.a rc 0 `clean`, verdict miss | `passed 4 of 4`; C2.a rc 1 `findings` | 1/4 → 4/4 | yes |

Re-measurement type: **evidence-verified** (committed receipts), not re-executed. The before/after numbers match the report.

Why both claims are not verified (the reason is the non-discrimination, not the numbers):
- Critic receipt `.ufo/waves/round-83/w1/CriticClaims-receipts/f1-v2-r82.json` reads `{"C1":3,"C2":4}` for the round-82 counters with four fixture-name lines added. That is the full-marks sniff.
- Plain grep over committed bytes: `grep -nE 'anchor-fixture|ordinals-fixture|\.name|basename' tools/check-anchor-coordinates-r83.py tools/check-ordinals-r83.py` → no output. The shipped r83 counters are pristine; the keying lives in the battery legs, which pass one fixture path each (`tools/round83-battery.py` lines 72, 76, 90, 94). So a path-sniff reaches full marks on the frozen battery.
- The sniff patch that CriticClaims F1 cites (`proposal-battery-fixture-alias.md`) is **absent from the committed tree**: `find .ufo/waves/round-83 -name 'proposal-battery-fixture-alias*'` → empty. F1 stands on the receipt `f1-v2-r82.json`; the named pointer does not resolve. Routed (§6).
- Repairs (re-encoded recipes 24/26 and 17/17 with zero tool edits, timeout arm, digest bind, positional retirement) are uncredited by the lane and not re-credited here.

Per-claim verdicts: **C1 unprovable**; **C2 unprovable**. The battery admitted a fixture-gated variant at both claims, so neither before→after can be read as an improvement.

Axis check: `git diff a8598038 a1b8191c -- SCORECARD.md` adds the round-83 declaration and measured-outcome sections. It moves no axis score; the outcome section reads `Axes now: depth8, coverage9, operability9, freshness9, calibration9, adjacency8 (unchanged)`. No axis harmed.

## 3. Discernment spot-check (LEARNING.md)

Sample from `corpus/lessons/round-83.md` `## Gate`: two admits (S334, S335 — four quotes) and two rejects. The newly written rows were re-opened.

| Item | Decision | Re-opened source | Observed | Agree / disagree · reason |
|---|---|---|---|---|
| S334 quote 1 "The final result of SHA-256 is a 256-bit message digest." | admit (row S334) | `https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf`, fetched 2026-11-05; sha256 `0455b406d89648d20cbde375561e19c245b9815e894164c2670772e3d54deb82` (matches the row's pin); `pdftotext -layout` | line 1016–1017, sentence wrapped across two lines; quote verbatim | **agree** — located, 10 words |
| S334 quote 2 "the resulting 256-bit message digest of the message, M, is" | admit (same row) | same PDF | lines 1095–1096 | **agree** — located, 10 words |
| S335 quote 1 "If the timeout expires, the child process will be killed and waited for." | admit (row S335) | `https://docs.python.org/3/library/subprocess.html` (title "Python 3.15.2 documentation"), fetched 2026-11-05 | verbatim, in the `run()` timeout paragraph | **agree** — 13 words |
| S335 quote 2 "The child process is not killed if the timeout expires" | admit (same row) | same page | verbatim, `Popen.communicate()` paragraph | **agree** — 10 words |
| SHA-512/256 truncation read as SHA-256 | **reject** (no row) | same PDF, §6.7 SHA-512/256 (its initialisation references §5.3.6.2, the SHA-512/256 IV) | lines 1228–1229 read "The 256-bit message digest is obtained by truncating the final hash value, H(N), to its left-most 256 bits." | **agree** — the quoted rule belongs to SHA-512/256, not SHA-256 |
| `call()` kills the child on timeout | **reject** (no row; "behaviour reaches it only through `Popen.wait`") | docs page: sweep of the page for `call()`/`TimeoutExpired` (the lesson's docs sweep). Source: CPython 3.14.8 `inspect.getsource(subprocess.call)` | Source ends `with Popen(...) as p: try: return p.wait(timeout=timeout) except: p.kill(); raise`. The child **is** killed on timeout. | **disagree (reason)** — the decision (no row) is defensible because no admitted entry needs the row, but the stated reason is false. Tier A admits source code, and the lesson's sweep looked only at docs. The flip "a sentence on `call()` timeout behaviour in the same revision" is docs-only and mis-specified. The lesson does not learn this. |

Tally: 5 agree, 1 disagree. The disagreement is recorded and routed (§6.1); it is not learned in round 83.

Note on S335: the row's anchor is a rolling page, dated by fetch date (`2026-11-05`), not a pinned version. Adequate for a 90-day recheck; a versioned anchor is preferred next time (minor).

Census re-run: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → exit 0 (`ok` on `corpus/SOURCES.md`). The output also lists W04 across-scope duplicate-url warnings; these are warnings, not failures. Manual census: rows 335; malformed 0; duplicate ids none; tiers A318 B6 C11; status mined 297, queued 5, rejected 33. All match the report.

## 4. Trend verdicts (with evidence)

- **expansion: unchanged.** No admitted `knowledge/` entry on uncovered ground. S334 and S335 are registry rows with `used-by` = the round lesson; no entry cites them. The lane's own grade is also unchanged.
- **quality: unchanged.** No admitted entry failed a re-check. The S333 `used-by` correction is a registry fix, not a superseded entry.
- **discernment: harmed.** Five of six spot-check items agree. The one disagreement (`call()` reject reason) is a factual error in a reject reason, and the round does not learn it. The in-wave fixture-gate finding (critic F1 → QUALITY 116/117 with lesson cites) is learned, and is not counted against this trend. The operator may rule on the weighting.

## 5. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth | unchanged | score held at 8; C1 unprovable (see §2) |
| calibration | unchanged | score held at 9; C2 unprovable (see §2) |
| coverage | unchanged | no score change in SCORECARD diff |
| operability | unchanged | no score change; re-encoding uncredited |
| freshness | unchanged | no score change |
| adjacency | unchanged | no score change; ADJ-06/OUT-009 unruled, not claimed |

No axis harmed. Admitted: **false** (both claims unprovable).

## 6. Routed defects (lane fixes next round)

1. **[discernment · lesson-owned]** `corpus/lessons/round-83.md` `## Gate`, row "REJECTED negative: `call()` kills the child on timeout": the reason "behaviour reaches it only through `Popen.wait`" is false (CPython 3.14.8 `subprocess.call`: `except: p.kill(); raise`). Correct by appending a new Gate row citing the source (not by rewriting); add a Mistakes row (class: wrong reject reason from a docs-only sweep · evidence: this file §3 · captured-by: none · fix: source-code sweep for tier-A claims). Restate the flip so source code can change the verdict.
2. **[evidence]** CriticClaims F1 cites `proposal-battery-fixture-alias.md`, which is absent from the committed tree. Commit it under `.ufo/waves/round-83/w1/proposals/` or cite the receipt `CriticClaims-receipts/f1-v2-r82.json`.
3. **[conformance]** Prompt §3 requires 1× planner; the L1 held the seat because the validator forbids the role. Disclose in the next report and name the validator conflict to the operator.
4. **[discernment]** Record this closure's spot-check result in the next round's `## Gate` (the round-83 lesson left it "pending the closure session").
5. **[carried, lane-owned]** The battery's routed list (fixture-path-keyed legs, unmeasured kill clauses M03/M04/M05/M10/M11/M19/M20, git subprocess env scrub) stands. Next declaration must run the QUALITY 82 fixture-gated control before freeze and show it reads below target.
6. **[operator-owned]** L0 question on CORPUS rule 2 (`used-by` in place) versus QUALITY 60/99. CORPUS rule 2 expressly permits in-place `used-by` with an old→new log, so the round followed the contract. The ruling is the operator's.
7. **[SHONEN]** No box is newly checkable by a non-author this round; no `[x]` is proposed and nothing is flagged for promotion.

## 7. Checks run (this file)

- `git merge-base --is-ancestor` on three hashes; `jj-lane.sh state`; `git status --porcelain`.
- `jq` over the two committed battery receipts; `grep` over committed r83 counters; `find` for the F1 patch.
- Re-open: NIST FIPS 180-4 PDF (sha256 matched the pin) and `pdftotext`; Python `subprocess` docs; `inspect.getsource(subprocess.call)` on CPython 3.14.8.
- `scripts/sources-census.sh validate` (exit 0).
