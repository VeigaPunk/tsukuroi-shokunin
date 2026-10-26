# Round 42 — lesson (tsukuroi, hyaku run 9)

author: tsukuroi L1 (`TsukuroiR42`), 2026-10-26. Base `c8efaa3f120834541f8de1e5e0367e8d1593bae6` — the lane tip at round
start as `jj-lane.sh state` printed it (`local=c8efaa3f…`; round-41 routed defect R41-BASE-MISREAD). Claims, controls and
outcome: `SCORECARD.md` sections "Round 42 — declaration" and "Round 42 — measured outcome". Waves: two v1 waves, `w1`
(build + first falsifiers) and `w2` (falsify, with the ten counted C2 row verdicts); specs, dispatches and the
orchestrator's results files are in `.ufo/waves/round-42/`. Seats are the lane, not outside reviewers (LEARNING.md); this
round's non-author closure is pending.

The round-41 Gate's spot-check item is answered by `corpus/lessons/round-41-verifier-spotcheck.md`: its §4 re-opened
S230, S232, S233 and both sampled staged rejects and agreed with every one; its §6 routed the five defects dispositioned
below.

## Gate

### New SOURCES rows (all opened 2026-10-26 by this round's L1; each quote located with `grep -n` in the pinned snapshot)

| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S237 | https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c (raw: https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c; tag v7.1 peeled 4ab0e80b) | "/* write all-zero progress file for a start */" | `.ufo/waves/round-42/frozen/src/scrub.c:1502` |
| S238 | https://github.com/kdave/btrfs-progs/blob/v7.1/CHANGES (raw: https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/CHANGES) | "* scrub limit: new command to show or set the per-device scrub limits" | `.ufo/waves/round-42/frozen/src/CHANGES:468` |
| S239 | own-work capture `.ufo/waves/round-42/frozen/hostcap/` (`capture.sh`, run 2026-10-26T19:13:44Z, unprivileged) | "var_lib_btrfs absent"; "scrub_timer_unit_file btrfs-scrub@.timer disabled disabled"; "journal_scrub_lines 0" | `frozen/hostcap/capture.txt:6,8,10` |

Snapshot digests: `frozen/src/SHA256SUMS`; fetch log `frozen/src/FETCH.txt`; live re-fetch byte-identical and the Arch
build 7.1-1 applies no patch (`w1/C2ExecLiveSources.md`). Rows touched old→new: S237, S238, S239 `status` queued→mined
and `used-by` —→`corpus/knowledge/btrfs-scrub-record-r42.md` (`git diff a84fc9de f50c28d8 -- corpus/SOURCES.md`: the
three lines); no older row changed.

### Entry gate (C2)

Outcome: **not admitted as verified** — the counted wave-2 reads bound SC1 `fails` (critic), SC3 `fails` (both seats), SC4 and SC5 `partly`, SC2 `holds`/`holds` (`after/c2-after-342d104.jsonl`: `verdicts_ok 1`; the C2RevSC1 and C2RevSC4 final outputs carried no verdict line and bound nothing). The entry stays in the corpus with the false sentences withdrawn in its section "Corrections — round-42 wave 2"; it must not be cited as a verified C2 outcome.
Wave-1 first reads: all five `holds` (`w1/C2DraftRevSC1..5.md`); their precision notes and `w1/C2CritNovelty.md` were
taken as a pre-admission revision of the draft before wave 2 (`git diff f50c28d8 78abb8b5 -- <entry>`: the scope
paragraph now names the held name pattern and SC5; SC1 mode/flock referent; SC3 resume, the silent mid-run write
failure, `[inference]` on the other-tool clause and the held conclusion; SC4 error exit, the recorded-device
quantifier, `[inference]`; the SC4 host reading now cites the unprivileged `btrfs scrub status /` run; the triage
bullet's new verdict token `UNRECORDED` withdrawn — the lane's vocabulary stays HEALTHY/DEGRADED/BLOCKED/UNVERIFIED).
Rejected: none of the five rows; rejected sentence: the draft's "It held no statement of the record itself: how the
file is named" (false — SH4 held the name pattern; C2CritNovelty §2).

### Assimilation (`merge/tsukuroi/`, theme: btrfs scrub/ioctl) — evaluated, nothing adopted

Seat AsmGate (`w1/AsmGate.md`) read the staged `btrfs-ioctl-surface-r27.md` and
`btrfs-filesystem-troubleshooting-bilingual-r26.md` against the pinned scrub.c and the local v7.1 header:
- **Admit candidate (not adopted this round):** P1, the nine-row ioctl-number table with magic 0x94, verified against
  `/usr/include/btrfs/ioctl.h` of btrfs-progs 7.1-1. Not adopted: neither staged entry carries a `## QUALITY check`
  (QUALITY 14), and the table is outside this round's claims. Flip: a lane entry that re-grounds it with its own check.
- **Reject:** P2, the staged claim that the ioctl surface is closed by nine subvolume commands — false against the
  pinned scrub.c's own `BTRFS_IOC_SCRUB`/`_PROGRESS`/`_CANCEL` use (scrub.c:421, :965, :986, :1200, :1792). Reason
  class: false statement. Flip: none.
No staged row or text appended; no collision check was needed (no append).

### considerthese — downstream patch-offset check (`considerthese/2026-10-26.md`, proposal 4)

Mined: "flag any knowledge anchor that cites upstream line numbers for code the host runs as a patched Arch build".
Grounded by seat ConsiderPatchOffset (`w1/ConsiderPatchOffset.md`, script `w1/ConsiderPatchOffset/patch-offset.py`,
108 cited pins checked, 15 drifting): Arch pacman 7.1.0.r9.g54d9411-3 shifts `add.c` after :417 by +23,
`makepkg.sh.in` by +118 and `PKGBUILD.5.asciidoc` by +9; btrfs-progs 7.1-1 applies no patch. Landed as appended notes
in `pacman-transaction-order-r39.md` and `alpm-package-anatomy-r41.md` (the r40 util.c offset was already recorded).

### Spot-check

Non-author closure pending. Candidates for it: one admit (S237 / SC4 or S238 / SC5) and one reject from the
assimilation set below.

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R42-OBSERVED-CHANNEL | vacuous | The C1 counter's namespace legs run as uid 0 with the fixed `alpha beta gamma delta` sample, so censuses fixed only under `TSUKUROI_FIXTURE`-or-uid-0, or only for those names, PASS the full predicate while the production path reads DEGRADED where BLOCKED is due (`w1/C1CritNsView.md` §3-4; `w1/C1CritEvasion.md` V1i) | QUALITY 82/85 asked for it; the frozen controls K7/K8 covered only the fixture variable | QUALITY 90; able to fail: the same view at uid 1000 (setpriv) separates V1 (DEGRADED vs BLOCKED) from the tip (BLOCKED/BLOCKED) (`w1/C1CritNsView.md` §4, re-run `w2/C1FinalProdIdentity.md`) |
| R42-ADOPTED-UNREAD | survivor | Wave-1 first reads of SC1-SC5 were all `holds`; two precision notes the L1 adopted without re-reading the source turned SC3 false ("(or is resumed)" from `w1/C2DraftRevSC3.md` N1; "only the final write reports a failure" from its N2), and the pre-existing SC1 clause "never a half-written one" was missed by the wave-1 read; the counted wave-2 reads returned SC1 `fails` (critic) and SC3 `fails` (both) (`w2/C2RevSC3.md`, `w2/C2CritSC3.md`, `w2/C2CritSC1.md`), so the declared kill rule fired | none — no criterion asks an integrator to verify a reviewer's proposed text before adopting it | QUALITY 91; able to fail: the counted read of the adopted text is the check that failed here (`w2/C2RevSC3.md` S1, S4) |
| R42-HERESTRING-TEMPFILE | survivor | The first fix (`44766208`) used here-strings; over 64 KiB bash writes a temp file, and on a full `$TMPDIR` or `/tmp` the redirection fails and the `if` takes the clean branch: HEALTHY, exit 0 (`w1/C1RevFix.md` D1, E3/E4) | none (no case exercises a full temp dir) | awk full-consumer test at `78abb8b5`; red at `44766208`, green at the tip (`w2/C1FinalENOSPC.md`) |
| R42-SUP-UNCOVERED | survivor | The two `-Sup` disagreement sites reverted to `head -n3` still passed the 130-case selftest (`w1/C1ExecAbleToFail.md`, `w1/C1MutSelftest.md` §2) | QUALITY 88 (named content parameters) | two cases at `78abb8b5` (132); red on each revert, green on the tip (`w1/C1MutSelftest.md` §4.1; `w2/C1FinalSelftest.md`) |
| R42-VERDICT-MENTION | vacuous | The C2 counter's verdict match is unanchored: a disputing sentence that quotes the holds line binds as holds (`w1/C2CritControl.md` D1) | QUALITY 89 (binding) did not ask for an asserted line | QUALITY 90 second clause; this round: a manual audit of the ten counted reports (`w2/C2PostCritBinding.md`) and prompts that never spell the holds line |
| R42-C1-SELFTEST-UNMEASURED | vacuous | The declaration names a new selftest case as part of C1's surface, but the predicate has no conjunct over it (`selftest_pass` is 1 at the base); the K6 control passes without the cases (`w1/MistakesSweep.md`) | QUALITY 88 | reported separately by the able-to-fail receipt (`impl/c1-able-to-fail.txt`); next counter: a conjunct that runs the revision's selftest against the base plane bodies |
| R42-C1-P6-NOT-NEUTRAL | stale-premise | The counter docstring calls every twin's padding verdict-neutral; P6's padding is error lines the parser reads (`w1/MistakesSweep.md`) | none | recorded here; P6 is a signal-dense twin, not a neutral one (its oracle still holds: the first error decides) |
| R42-BATTERY-SUMMARY-COLLISION | landing | Both control runners write `battery-summary.jsonl` into one directory; the C2 summary was copied aside before the C1 run overwrote it (`controls/battery-summary-c1.jsonl`, `-c2.jsonl`; `w1/MistakesSweep.md`) | none | next runners take a battery-specific name; the copy is disclosed here |
| R42-FREEZE-CENSUS-LIVE-PATH | reference-drift | `before/sources-census-at-freeze-a84fc9de.txt` ran on the live lane path, not an export of `a84fc9de`; the true start receipt is `before/sources-census-start.txt` (base export) (`w1/MistakesSweep.md`) | none | the start value cites only the base export |
| R42-C1-SCRATCH-FALLBACK-TMP | landing | Without `--scratch` and with `TMPDIR` unset the C1 counter builds under `/tmp` (`w1/MistakesSweep.md`; scratch discipline §7.4) | R40-TMP-MISROOT | routed: a frozen-counter amendment next round (refuse to run without `--scratch`) |
| R42-COUNTER-SIGINT-LEAK | landing | 1 of 2 SIGINTs during the counter's selftest child left 91 entries in the run root (`w1/C1SentScope.md`) | none | routed with the amendment above |
| R42-C1-CLASS-UNSWEPT | scope | Early readers remain at single-line probes (`:931`, `:969`, `:1051`, `:1426`, `:1501`) and `tools/boot-chain-audit.sh:480-487` reads false whenever `find` exits 1 (`w1/C1SweepSites.md`) | none | `:743` fixed this round (full read); the rest routed to round 43 |

## Round-41 routed defects — round-42 disposition

1. R41-PA6-UNJUDGED — seat PA6Verdict read PA6 with all three appended corrections against the frozen `be_local.c`:
   `ROW PA6 VERDICT: holds` for the row as corrected (`w1/PA6Verdict.md`). Recorded as the disposition; round 41's
   outcome stands.
2. R41-CENSUS-PIPEFAIL-692 — C1 of this round (fixed `44766208`, hardened `78abb8b5`).
3. R41-GUARD-BYPASS — C1's oracle holds no answer key and C2's verdicts bind to the orchestrator records; both were
   beaten again through other channels (R42-OBSERVED-CHANNEL, R42-VERDICT-MENTION) → QUALITY 90.
4. R41-BASE-MISREAD — base `c8efaa3f` from `jj-lane.sh state` local at round start, named in the declaration and both
   counters (`BASE`).
5. N3 — both before receipts finished (19:29:59Z, 19:30:01Z) before the implementation commit (19:32:12Z) and before
   any after receipt (`w1/RevRoutedDefects.md` §N3).

## Sources census

Start: `tsukuroi ok`, exit 0, 40 W04, 236 rows (base `c8efaa3f` exported into a scratch fleet-root layout:
`.ufo/waves/round-42/before/sources-census-start.txt`; the same command at the freeze commit, with S237-S239 queued, is
`before/sources-census-at-freeze-a84fc9de.txt`).

End: see the report's Sources & frontier section (`.ufo/waves/round-42/after/sources-census-final.txt`).

## Spot-check candidates for the non-author closure

One admit: SC2 (both counted reads `holds`; S237 scrub.c:826-895). One reject: the staged P2 "closed ioctl surface"
claim (AsmGate) or the withdrawn SC3 sentence "(or is resumed)" (`w2/C2CritSC3.md` F1).
