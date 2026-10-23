# Round-33 a3w2 — MutR1CounterV4 (attack on the v4 repair counter for round-32 routed defect 1)

Verdict: **DOES NOT MEET** on its single v4 score (routed 24 of 24, live_consistent false, harness_errors 0, exit 1). The only conjunct that failed was the plain live view, and it failed because the host journal grew between the base run and the REV run. The pristine tip failed v4 in the same way 72 s earlier, and the restored tip passed about 30 s later. So the score is inconclusive as a kill. The shortcut passed every conjunct that the v4 repairs added, which means the mutant **survived the repairs**.

1. [obs] **The variant (one sandbox commit on `efe6d135`).** The commit is `d32a46d64d60acb78ec70ea3467d64f544b76aa5` in my clone. It adds 14 lines to `tools/tsukuroi-census.sh` and changes no other file. The new lines sit in `main()` just before the two HANDOFF `printf`s, and the census sha256 changes from `7daa2ccb…44e7b5` to `4305f91e…b3bf02`. When `TSUKUROI_JOURNALCTL` is non-empty, the variant overwrites both values:
   - `OOM_CLUSTERS` becomes `C2_events`, read from the oom note. That is the attribution-line count, so no minute clustering happens.
   - `JRN_COREDUMPS` becomes `err` from the journal note minus the number of entries carrying the fixture distractor label `"MESSAGE":"fixture: retained unit error entry"`. The variant gets that number from a second `journalctl -b -p err -o json` read, so no `SYSLOG_IDENTIFIER` selection happens.

   When the variable is unset, the census's own counts stand. This breaks the tip's contract at `/fast/scratch/hyaku/tsukuroi-r33a3/MutR1CounterV4/repo/tools/tsukuroi-census.sh:71` (at `efe6d135`): "never by a TSUKUROI_* name or a fixture marker". The patch is at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/MutR1CounterV4/mut-variant.patch` (sha256 `8f8b28329e3e6dd35aafcc805ced32a5a9a5de7131565ead488fa9721217ee18`).

2. [obs] **I scored it as the R1 seat did, once.** The scorer bytes were copied unchanged into my clone at the same path. I committed them as tool revision `75f744d894338ba3a536fcfbd53c432d76617ffe` (tool_sha256 `6f682fee94923acd2b5f4c27ee268f85f76289f04b0f170d5dcf884f9d7664be` in all three receipt headers; the seat's copy hashed the same before and after). The command:
   `cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && timeout 1900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 tools/run-receipt.py --lane /fast/scratch/hyaku/tsukuroi-r33a3/MutR1CounterV4/repo --revision d32a46d64d60acb78ec70ea3467d64f544b76aa5 --tool-revision 75f744d894338ba3a536fcfbd53c432d76617ffe --out …/a3w2/MutR1CounterV4/mut-variant-d32a46d6.jsonl --timeout 1700 -- .ufo/waves/round-33/a3w1/R1CensusCounterV4/score-census-handoff-v4.py --revision '{rev}' --lane '{lane}'`
   It exited 1.
   - Summary (receipt line 27): `scenarios 24, routed 24, live_consistent false, harness_errors 0, seed b20150f54cd7e475, predicate_label routed, scorer_version 4, unrouted []`.
   - Footer (line 28): `exit_code 1, timed_out false`.
   - Receipt: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/MutR1CounterV4/mut-variant-d32a46d6.jsonl` (sha256 `4ca6a15c280a40951052292d1b1fe509db385606ae295e6bc5c9a1e08d7446d7`).

3. [obs] **The shortcut routed all 24 fixture scenarios with full plane parity, including the repair cases.** Every row has at least one distractor (minimum d=1 at s03). The rows where kernel lines exceed kill events are:
   - s11: planted kill 8, kernel_lines 24, coredumps 9, d 9. Observed `kill-events=8,coredumps=9`.
   - s14: kill 6, kernel_lines 12, coredumps 7, d 9. Observed `kill-events=6,coredumps=7`.
   - s24: kill 2, kernel_lines 6, d 9. Observed `kill-events=2`.

   Evidence: the same receipt, lines 2-25 (s11 at line 12, s14 at 15, s24 at 25).

4. [obs] **Both synthetic live views were consistent.** Evidence: receipt line 26.
   - View A planted n 3, mult 1, m 6, d 3. The base read `err=9 (coredump=6 kernel=0 other=3)` and `C2_events=3 C3_events=3 clusters=3`. The variant printed `kill-events value=3` and `coredumps value=6` (parity true, consistent true).
   - View B planted n 9, mult 2, m 1, d 4. The base read `C1_kernel=18 killed_process=18; C2_events=9 C3_events=9 clusters=9` and `err=5 (coredump=1 kernel=0 other=4)`. The variant printed `kill-events value=9` and `coredumps value=1` (parity true, consistent true).

5. [obs] **The plain view failed on journal growth, not on the shortcut.** The scorer strips every `TSUKUROI_*` name in the plain view (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/R1CensusCounterV4/score-census-handoff-v4.py:887`), so the variant ran the tip's own code there.
   - On attempt 2 the base read `err=1608 (coredump=1522 kernel=85 other=1)` and REV read `err=1623 (coredump=1537 …)`.
   - The oom lines, the rollup and rc 1 were equal, and kill-events was 24 against 24.
   - REV's coredumps HANDOFF (1537) equalled its own journal plane. The scorer expected the base's 1522, so parity was false (receipt line 26).

6. [obs] **Baseline bracket, run with the same scorer and tool revision.**
   - Pristine `efe6d135`, started 07:40:03Z: routed 24, live_consistent false, harness_errors 0, exit 1. The plain view failed on attempt 2 with base coredump 1331 against REV 1344; synthetic A and B were consistent. Receipt: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/MutR1CounterV4/pristine-tip-efe6d135.jsonl` lines 26-28, sha256 `3f8cf6c3…4f0d57`.
   - Restored `efe6d135`, 04:42:35-04:43:09 -03: routed 24, live_consistent true, harness_errors 0, exit 0, with plain coredumps 1603 on both runs. Receipt: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/MutR1CounterV4/restored-tip-efe6d135.jsonl` lines 26-28, sha256 `85aba609…21fee3`.

   The variant's failure therefore matches a failure the baseline also showed in the same minute. By this lane's rule that makes it inconclusive, not killed.

7. [obs] **Ordinary-run check: the mutant is not equivalent, and it misroutes the live host's own journal.** I ran one bounded script outside the scorer: `timeout 300 /usr/bin/bash /fast/scratch/hyaku/tsukuroi-r33a3/MutR1CounterV4/ordinary-run-check.sh` (sha256 `418b2f5c…88d0`), exit 0. It ran four censuses back to back from 04:43:52 to 04:44:13 -03.
   - Plain tip and plain variant printed identical counts and HANDOFF lines: `clusters=24`, `coredump=1603`, `kill-events value=24`, `coredumps value=1603`, both with rc 1.
   - With `TSUKUROI_JOURNALCTL=/usr/bin/journalctl`, which is the real binary and so the same journal, the tip printed the same 24 and 1603.
   - With that override, the variant printed `kill-events value=78` and `coredumps value=1689`. Those are `C2_events=78` and `err=1689`, printed over the same PLANE counts.

   Output: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/MutR1CounterV4/ordinary-run-check.txt` (sha256 `cc6b78ed…21d4`).

8. [inf] **Why the shortcut survives each repair.** Line numbers below refer to the v4 scorer file named in finding 5.
   - Repair (1), distractors: every planted distractor carries one fixed label (`:423` and `:818`) and a `fixture-*` identifier (`:421`, `:816`). So err minus the labelled count is exactly m. The repair defeats a fixed floor (K11's err−52), but not a floor derived from the fixture's own label.
   - Repair (3), kernel repeats: only the kernel line repeats (`:388-390`, `:790-792`). The attribution and sigkill lines stay at one per minute (`:391-394`, `:793-796`). As a result C2_events = C3_events = clusters in every fixture and synthetic view; the tip's clusters come from those two streams (census `:1248`). On the live host C2_events is 78 against 24 clusters, which is why the variant must branch rather than use C2 everywhere.
   - Repair (2), synthetic views: they set `TSUKUROI_JOURNALCTL` (`:908-909`), as every fixture does (`:495`), and they reuse the fixture's line shapes and labels (`:786-821`). One bit therefore separates the views whose counts vary and whose shape is the scorer's from the one view whose shape is real. Varying the counts defeats constants only.

9. [inf] **Calibration against R1's report.**
   - R1's findings 5-6 (K11 and the content-free control fail) still stand.
   - R1's finding 3 is literally true, but the variation does not catch a census keyed on labels or line shape.
   - R1's residual risk 11(a) was marked [inf]; it is now [obs] for the fixture and synthetic conjuncts.
   - The only remaining defence is the plain view, and the variant passes it in substance by running the claimed code there (finding 7). For this variant, v4's verdict therefore comes down to whether the journal stays quiet during the run.
   - Hyaku §9: a shortcut keyed on a fixture label and a `TSUKUROI_*` name reached every conjunct except the plain one, and the pristine tip missed that one too.
   - [unk] I did not rescore the variant on a quiet host, because the contract says score once. Given finding 7 and the restored pass, [inf] a quiet-host rescore would most likely MEET.
   - [inf] Coverage data only, not a contract change: a pass-through view (`TSUKUROI_JOURNALCTL` set to the real binary, expecting the plain counts) is exactly the finding 7 check and kills this mutant. Unlabelled distractors, or minutes with several attribution lines (the live host has 78 lines over 24 clusters), would kill the label and C2 parts.

10. [obs] **v4's plain view is unstable on this host right now, and it reports drift as a census failure.** The boot-0 coredump count rose quickly:

    | Time (-03) | Coredump count |
    |---|---|
    | ~04:14 (R1 tip run, R1 #9) | 265 |
    | 04:36:43 | 1240 |
    | 04:37:00 | 1272 |
    | 04:37:20 | 1275 (`journalctl -b 0 -p err -o json` grep count) |
    | 04:40 (pristine, base / REV) | 1331 / 1344 |
    | 04:41-04:42 (variant, base / REV) | 1522 / 1537 |
    | 04:42:35-04:44:13 | 1603 |

    Two of the three v4 runs in 3 minutes lost parity on journal growth. Both reported it as exit 1 with `harness_errors 0`, not as a harness error. A v4 exit 1 on this host is therefore not, by itself, evidence that a census lacks the routing.

11. [obs] **Restoration and containment.**
    - My clone is back at `efe6d135`: `tools/tsukuroi-census.sh` sha256 is `7daa2ccb…44e7b5`, the same as before the mutation, and `git status` is clean.
    - The branches `mut-tool` and `mut-variant` exist only in my clone.
    - No lane file outside this seat directory was edited, no git or jj write ran in the lane, and every git call used `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`.
    - No process I started is still running (pgrep count 0).
    - The four `/fast/scratch/hyaku/run-receipt-*` directories present are timestamped 02:01 and 04:09, before I started at 04:32, so they are not mine and I left them alone.
    - I fetched no external source, so there is no SOURCES.md duplicate question.

Scope: read=R1 report and scorer (`.ufo/waves/round-33/a3w1/R1CensusCounterV4.md`, `…/R1CensusCounterV4/score-census-handoff-v4.py` all 1154 lines, `K11-label-noise-floor.patch`), census diff `58cc2e0b..efe6d135` and `efe6d135:tools/tsukuroi-census.sh` (header, oom/journal probes, main), `tools/run-receipt.py`, `/home/vgpnk/.omp/agent/RULES.md`, a3w2 swarm registry; wrote=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/MutR1CounterV4.md`, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/MutR1CounterV4/{mut-variant.patch,pristine-tip-efe6d135.jsonl,mut-variant-d32a46d6.jsonl,restored-tip-efe6d135.jsonl,ordinary-run-check.txt}`, `/fast/scratch/hyaku/tsukuroi-r33a3/MutR1CounterV4/{repo (clone; sandbox commits 75f744d8, d32a46d6),ordinary-run-check.sh,census-tip.sh,census-variant.sh}`; executed=sandbox clone/checkout/commit in my clone only, one live tip census read (`timeout 180 bash tools/tsukuroi-census.sh`, rc 1), two `journalctl -b 0 -p err` coredump counts, three `tools/run-receipt.py … score-census-handoff-v4.py` runs (pristine exit 1, variant exit 1, restored exit 0), `ordinary-run-check.sh` (exit 0), sha256sum/pgrep/ls checks
Model: anthropic/claude-opus-5-5
Installs: none
