# Round 83 — digest-bound anchor counter and positional ordinal counter: honest stop

Lane base `a8598038dbcbaa07d4b5899b647bf30aa81e9e3f`; frozen declaration `d78b3b3982b5df62286dd65b0a42ae8a91847608`;
one v1 wave `w1` of 13 seats (L1 holds the planner seat). Both claims are **not verified**: the frozen
battery that scores them is reached in full by a fixture-gated do-nothing variant, which QUALITY 82 requires
the battery to fail before freeze. The pristine counters pass every probe the wave built; the battery does not
discriminate. No ordinal moves. Evidence: `.ufo/waves/round-83/w1/` and `SCORECARD.md` "Round 83".

## Gate

Sources opened 2026-11-05 by seat ScoutSources; fetch receipts in `.ufo/waves/round-83/w1/ScoutSources.md` and
`.ufo/waves/round-83/w1/ScoutSources/sources.json`. The `systemd.mount.xml` pin was also re-opened this round.

| Candidate | URL, access date, location | Located quote (≤25 words) | Decision, reason and flip |
|---|---|---|---|
| S334 (new row, spec/A) | https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf, accessed 2026-11-05, §6.2 SHA-256, printed p.21 (PDF p.26) | "The final result of SHA-256 is a 256-bit message digest." (10 words) | ADMIT, row S334 `mined`. Used by C1 (digest gate). Flip: none needed. |
| S334, second quote | same PDF, §6.2.2 step 5, printed p.23 (PDF p.28) | "the resulting 256-bit message digest of the message, M, is" (10 words) | ADMIT as the same row's second anchor. |
| REJECTED reading: SHA-256 digest truncated to its left-most 256 bits | same PDF, §6.7 SHA-512/256, printed p.26 (PDF p.31) | "The 256-bit message digest is obtained by truncating the final hash value, H(N), to its left-most 256 bits." (17 words) | REJECTED for SHA-256: the sentence states the SHA-512/256 rule. No row. Flip: a passage that states the same rule for SHA-256. |
| canonical csrc FIPS URL | https://csrc.nist.gov/pubs/fips/180-4/upd1/final, HTTP 200 on 2026-11-05 | none | NOT A SOURCE: the body is a landing page with no "SHA-256" text; recorded in the S334 `source` cell. |
| S335 (new row, docs/A) | https://docs.python.org/3/library/subprocess.html, accessed 2026-11-05, raw lines 289-291 (`run()`) | "If the timeout expires, the child process will be killed and waited for." (13 words) | ADMIT, row S335 `mined`. Used by the timeout repair. Flip: none needed. |
| S335, second quote | same page, raw lines 1066-1071 (`Popen.communicate()`) | "The child process is not killed if the timeout expires" (10 words) | ADMIT as the same row's second anchor: the two calls differ. |
| REJECTED negative: `call()` kills the child on timeout | same page, `call()` entry raw 1496-1522 | none; sweep = all raw lines of the page that mention `timeout` near `call` | REJECTED, no row: the page has no sentence about `call()` killing or TimeoutExpired; behaviour reaches it only through `Popen.wait`. Flip: a sentence on `call()` timeout behaviour in the same revision. |
| S333 re-open (systemd.mount v262) | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml, accessed 2026-11-05, HTTP 200, 37234 B | "With nofail, this mount will be only wanted, not required, by local-fs.target or remote-fs.target." (raw 502-503); "In the created mount unit, configures a Before= or After= dependency on another systemd unit, such as a mount unit." (raw 234-236) | RE-OPENED, no status change. sha256 `afbf3be6…2394` equals the pin; two fetches byte-identical (`cmp`). |

Registry changes (old → new), all logged here per CORPUS.md SOURCES rule 2:

- `S333` `used-by`: `corpus/knowledge/mount-unit-fstab-plane-r81.md, corpus/knowledge/mount-unit-fstab-plane-r81.json` →
  `corpus/lessons/round-82.md`. Neither knowledge file contains `S333` (`grep -c S333` = 0 for both); the round-82 lesson
  cites it. This is the R82-V7 correction. `status`, `recheck` and the other cells are unchanged.
- Rows added: `S334` and `S335` (status none → `mined`; opened 2026-11-05; recheck `180d` and `90d`; used-by
  `corpus/lessons/round-83.md`, which cites both ids).
- Census before → after: rows 333 → 335; malformed 0 → 0; duplicate ids none; tier A 316 → 318 (before: A316 B6 C11);
  status mined 295 → 297, queued 5, rejected 33. Command and exit codes are in SCORECARD.md "Round 83 — measured outcome".
- Collision check: the lane's highest id was S333, next free S334/S335. `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`
  guard proven able to fail (indented S333 row → prints `S333`, `.ufo/waves/round-83/w1/ScribeRegistry/guard-red.txt`).
- Lane-rule tension, decided and flagged: QUALITY 60 and 99 read as forbidding in-place edits to filed record bytes;
  CORPUS rule 2 explicitly permits `used-by` to change in place with an old→new log. The fleet contract was followed.
  Ruling requested in `.ufo/l0-questions.md`.

Assimilation: none. `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/MERGE-REPORT.md` holds no depth-anchor or
calibration-ordinal theme (ConnectorScope §3).

## Mistakes

| Class · evidence · captured-by · fix |
|---|
| **R83-CHRONOLOGY** — instrument iterations and controls ran before the declaration commit · `SCORECARD.md` "Round 83 — declaration" chronology paragraph; `.ufo/waves/round-83/before/controls.txt:1-5` · captured-by: none · fix: the freeze commit `d78b3b39` pins the bytes; disclosed, not repaired retroactively. |
| **R83-PRE-CONTROL-SKIPPED** — the frozen battery was not run against a fixture-gated do-nothing variant before freeze, as QUALITY 82 requires. A four-line path-sniff added to the round-82 counters reaches C1 3/3 and C2 4/4 · evidence `.ufo/waves/round-83/w1/CriticClaims.md` F1 and `CriticClaims-receipts/`; the legs key on fixture file names in `tools/round83-battery.py` · captured-by: QUALITY 82 existed and was not run · fix: QUALITY 117 (below); the next declaration must show this control reading below target before freeze. |
| **R83-BATTERY-LEG-GAPS** — the frozen legs leave kill-rule clauses unmeasured: revision-path digest bypass (M05), undeclared digest (`ExecAnchorRed` M-UNDECLARED), uppercase digest (M03), decoded-text digest (M04), off-by-one range (M10), calibration-axis removal (M11), revision exit codes (M19, M20) · evidence `.ufo/waves/round-83/w1/MutAnchor.md` GAP list, `ExecAnchorRed.md`, `MutOrdinal.md` GAP list · captured-by: none · fix: QUALITY 117(a); separating fixtures listed in the wave reports for the next declaration. |
| **R82-V1** — recipe encoding: `C16-empty-manifest` and `M06-mutation-unlink-noop` store backslash-n in `old` · `.ufo/waves/round-82/before/mutants-r82.json` · captured-by: none · fix: `.ufo/waves/round-83/before/mutants-r83.json`. The re-encoding alone reaches the round-82 frozen target (24/26, 17/17) with zero tool edits, so that target was an encoding defect and is not credited as operability · receipt `.ufo/waves/round-83/before/do-nothing-reencoded-mutation-r83-at-tip.json`. |
| **R82-V2** — global retirement `if key[0] == round_no or True:` · `tools/check-scorecard-ordinals.py:102` · captured-by: none (the round-82 selftest had no later re-assertion case) · fix: `tools/check-ordinals-r83.py` positional retirement; red-before `controls.txt` "C3 red-before A" (round-82 counter prints clean on the late-contradiction fixture). |
| **R82-V3** — `--revision` absence leaks a traceback with rc 1 (findings code) · `tools/check-scorecard-ordinals.py:204-206` · captured-by: none · fix: `read_scorecard_at` in `tools/check-ordinals-r83.py` returns JSON rc 2; red-before `controls.txt` absent-SCORECARD block (round-82 rc1 traceback, `fx` repo at `main`). |
| **R82-V4** — a selftest that does not finish is scored as a kill · `tools/mutation-kill-r82.py` (`rc 124` counted by `rc != 0`) · captured-by: none · fix: `tools/mutation-kill-r83.py` `observed` flag; red proof `ExecTimeoutRed.md` (round-82 harness kills a 30 s sleep mutant at a 2 s bound; the round-83 harness marks it unobserved). Uncredited repair. |
| **R82-V5** — the anchor counter never reads the declared `snapshot_sha256` · `tools/check-anchor-coordinates.py` `load()` · captured-by: none · fix: `bind_digest` in `tools/check-anchor-coordinates-r83.py`; red-before `controls.txt` "C2 red-before" (round-82 counter prints met on the doctored snapshot). |
| **R82-V7** — S333 `used-by` names two files that do not cite it · `corpus/SOURCES.md` S333 row · captured-by: census passes (E11 checks existence only) · fix: `used-by` → `corpus/lessons/round-82.md` (see Gate). |
| **R83-SCRATCH-RETAINED** — `ExecAnchorRed` kept its scratch past exit to hold a proposed patch; scratch is reaped after 45 idle minutes · lane `.ufo/waves/round-83/w1/proposals/` · captured-by: scratch discipline §7.2 existed · fix: the four proposals were copied byte-exact into the wave directory. |
| **R83-SCRATCH-SWEEP-OVERBROAD** — the L1's first sweep for proposal patches copied about 5,870 historical files from full-history `--shared` clones · captured-by: none · fix: removed before any commit; copy only named files. |

## Seat harm

| Round | Harmed seat | Causing seat | Evidence class | Effect | Fix |
|---|---|---|---|---|---|
| 83 | none observed | — | `.ufo/waves/round-83/w1-results.json` (13 seats, 13 non-empty outputs) and the 13 wave reports | no kill signal, no lane write outside the wave directory, no shared-file collision reported | none needed |

Sentinel finding (`SentinelGate.md` check 3): the four `git` subprocess calls inherit the parent environment. This is a
product finding about the instruments, not seat-to-seat harm. Routed; patch in `proposals/`.

## Wave settlement

One v1 wave, 13 seats: scout 1, scribe 2, executor 3, mutation-tester 2, reviewer 2, critic 1, connector 1,
sentinel 1; L1 holds the planner seat (validator forbids the role). Attack seats 5/13 = 38%. Connector 1.
Dead seats 0; residual 0. Every seat returned non-empty output; `w1-results.json` lists 13 seats. The results record
carries no per-seat status field in this format.

Seat results, one line each (report under `.ufo/waves/round-83/w1/`):
- ScoutSources: three sources re-opened; the canonical NIST URL serves a landing page, so the PDF was used.
- ScribeMistakes: six mistake rows, each pointer verified by grep.
- ScribeRegistry: collision guard proven able to fail; validate exit 0 for both variants; S333 edit proof.
- ExecAnchorRed: M-NODIGEST red for the battery (C1.a rc 0 instead of 2); M-UNDECLARED survives the battery, caught only by the counter's selftest.
- ExecOrdinalRed: three mutants each red for a C2 leg; O-TRACEBACK survives the counter's own selftest.
- ExecTimeoutRed: round-82 harness counts a timed-out selftest as a kill; the round-83 harness does not.
- MutAnchor: 6 of 13 mutants killed; survivors EQUIVALENT (M01, M02, M13) or GAP (M03, M04, M05, M10).
- MutOrdinal: 10 of 20 killed; GAPs M05, M07, M08, M11, M13, M14, M16, M19, M20.
- ReviewAnchor: digest check precedes row scoring on both paths; C1.a refusal is the digest mismatch, not an XML artifact.
- ReviewOrdinal: positional rule verified against the real SCORECARD; 110 bare sites, 4 retired, examined 81; two quoted-only sites, both citations.
- CriticClaims: F1 FOUND (fixture-gated variant reaches 3/3 and 4/4); F2, F3, F5, F6 hold; F4 holds with a second `cannot-evaluate` reason (corrupt encoding), still JSON rc 2.
- ConnectorScope: no sibling owns these surfaces; the still-open considerthese proposal #22 (patch-offset) needs a host-build measurement outside these legs and is not taken.
- SentinelGate: no credential-shaped material; no lane write; git children inherit env (routed).

Note on `/tmp`: ReviewAnchor's idempotence probe cites run logs under `/tmp`. Those are not citable evidence (reaper); the
claim they supported is not used here.

## Verdicts

- **C1 depth (tied lowest, 8) — NOT VERIFIED (honest stop).** Frozen legs C1.a–c read 3/3 on the pristine counter and
  at the freeze. A path-sniffing do-nothing counter also reads 3/3 (F1), so the legs do not discriminate. The
  ordinal stays 8. No uplift.
- **C2 calibration (9) — NOT VERIFIED (honest stop).** Frozen legs C2.a–d read 4/4 on the pristine counter. The same
  sniffing variant reads 4/4 (F1). MutOrdinal M11 (calibration removed from `AXES`) survives every frozen leg, so the
  battery cannot see the calibration axis. The ordinal stays 9. No uplift.
- **Repairs, uncredited:** the re-encoded recipes (reach 24/26 and 17/17 with zero tool edits), the timeout arm, and
  the r83 counters' digest bind and positional retirement. They are landed in the lane and can be re-declared with
  discriminating legs next round.

Do-nothing controls (frozen, reproduced by CriticClaims F2): round-82 counters at the pre-round tip score
battery C1 2/3 and C2 1/4, exit 1. Round-83 counters score C1 3/3 and C2 4/4, exit 0. The round-82 counters with four
sniff lines score C1 3/3 and C2 4/4, exit 0 (F1).

## Routed to the next round (declare before data; run the QUALITY 82 control before freeze)

1. Replace fixture-name-keyed legs with legs whose verdict does not depend on a path string (QUALITY 117(c)).
2. Add legs for: revision-path digest bypass (M05), undeclared digest (M-UNDECLARED), uppercase digest policy (M03,
   needs an explicit policy), decoded-text digest (M04), off-by-one range (M10), calibration-axis removal (M11),
   revision exit codes (M19), `problems` reason (M20, diagnostic only).
3. Selftest on the public `main` path (O-TRACEBACK); supersedes forms: indented marker (M07), `=>` (M05 ord),
   non-round `##` heading (M13), round-number boundary (M14), digit boundary in `Axes now:` (M16).
4. `tools/check-anchor-coordinates-r83.py` prints `"claim": "C2"` on every line (line 51) and its docstring says C2;
   the depth instrument is C1. Label-only; ExecAnchorRed.
5. Git subprocess environment: pass the scrubbed env to the four `git` calls (SentinelGate proposal in `proposals/`).
6. C1.a reason check: `problems[0].startswith("snapshot-digest-mismatch")` (ReviewAnchor proposal in `proposals/`).
7. Citation grammar: a value that a block both asserts and cites cannot be expressed bare-only (ReviewOrdinal note).

## QUALITY check

Applicable: 1, 2, 3, 5, 7, 8, 14, 19, 21, 23, 60, 66, 82, 93, 94, 96, 99, 103, 108, 110, 113, 114, 115, 116, 117.
The round added QUALITY 116 and 117, each citing this lesson's Mistakes rows. No criterion predating the round was
rewritten. QUALITY 82 is the criterion that the round violated before freeze; it is cited, not weakened.

## Frontier step

- Sourced claim: C1 cites S334 (opened this round) in the declaration and the battery's digest rule.
- Mistake mined: R83-PRE-CONTROL-SKIPPED (and nine others above). Sweep: `grep -n 'or True' tools/*.py` finds no other
  instance in the round's tools.
- Discernment spot-check: pending the closure session (this lesson's admits are S334 and S335; rejects are the
  two REJECTED rows above; the closure must re-open at least one admit and one reject).
- considerthese: none taken (see Gate). Assimilation: none.
