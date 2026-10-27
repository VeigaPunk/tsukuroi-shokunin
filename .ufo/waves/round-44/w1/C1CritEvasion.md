VERDICT: defect-found

# Seat C1CritEvasion — item C1-11 (cheapest PASS variants without a real arm)

Frozen counter used throughout: `tools/score-scrub-arm-r44.py`, sha256 `1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388` (matches the declaration). Engine revision for every variant: `ab8aae1627426c29e1445e30da0efb0c19c1bca1` (census sha256 `fca419b4…` == `controls/candidate-tsukuroi-census.sh`). Variants were built only in scratch clones under `/fast/scratch/hyaku/tsukuroi-r44/C1CritEvasion/` (`git clone --shared`, origin removed, toplevel asserted, fixture identity commit); no lane/fleet file was touched (`git status --porcelain` shows no tracked modifications), no host mutation occurred, no mounts left behind (`findmnt -t tmpfs` clean), and the C1 counter ran one at a time (~30–60 s each, ~21 min total).

## Battery (score files: `w1/C1CritEvasion/score-V*.json`; diffs: `w1/C1CritEvasion/diff-V*.txt`)

| Variant | Channel (detector) | Verdict | correct | wired_ok | live_agree | selftest_pass | selftest_r44 |
|---|---|---|---|---|---|---|---|
| V1-gate-mntlib | script host `/mnt/census-lib.sh` exists | **PASS** | 16 | 1 | 1 | 1 | 9 |
| V2-gate-statfs-tmpfs | `stat -f -c %T /sys/fs/btrfs` == tmpfs | **PASS** | 16 | 1 | 1 | 1 | 9 |
| V3-gate-script-path | `${BASH_SOURCE[0]}` == /mnt/census-lib.sh or /mnt/census.sh | **PASS** | 16 | 1 | 1 | 1 | 9 |
| V4-gate-cwd | `$PWD` == /mnt/home | **PASS** | 16 | 1 | 1 | 1 | 9 |
| V5-gate-uidmap | `/proc/self/uid_map` has != 1 line | **PASS** | 16 | 1 | 1 | 1 | 9 |
| V6-gate-fixture-literal | record content `scrub status:1` (grep) | FAIL | 6 | 1 | 1 | 0 | 9 |
| V7-compact-reader | none (36-line faithful rewrite, no comments) | **PASS** | 16 | 1 | 1 | 1 | 9 |
| V8-sysfs-blind | skips devinfo/scrub_speed_max reads | FAIL | 12 | 0 | 1 | 0 | 9 |
| V9-pure-constant | no reads at all (= control K1) | FAIL | 1 | 0 | 1 | 0 | 9 |
| V10-selftest-only-real | real logic only when override env set | FAIL | 1 | 0 | 1 | 1 | 9 |

Every gated variant (V1–V6, V10) keeps the **real** `probe_scrub_record` logic (renamed `_scrub_real`) inside the namespace and inside the census selftest (selftest detected via `TSUKUROI_SCRUB_DIR` being set, which `run_selftest` does at `tools/tsukuroi-census.sh:2282`), and prints a hardcoded line on the live host. The hardcoded line is exactly the declared zero-state constant: `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`.

## Findings

**F1 — counter defect (live leg accepts a cached answer): V1–V5 PASS while answering the live host from a constant, never reading it.** The only difference between V1–V5 and the real arm at `ab8aae1` is the live branch: it emits the constant without touching `/var/lib/btrfs`, `/sys/fs/btrfs` or `timers.target.wants` (diff evidence `diff-V1-gate-mntlib.txt` etc.). The counter's L leg (`score-scrub-arm-r44.py:593-605`) only checks that the full live census prints exactly one SCRUB line equal to `expect(live_model())` (its own Python walk) between STORAGE and the rollup; it cannot distinguish a real read from a cache. Today the host is quiet (`expect(live_model())` == the constant, same as in `after/c1-after-ab8aae1.jsonl`), so any cached-answer arm passes. This is exactly the declared "cached live answer" channel, and it is open. It is latent: if the host later gains records/limits/timer links, V1–V5 would FAIL L while a genuine arm would pass — so the claim's verification is hostage to the host staying in the NONE/absent state. The open channels (mount table, uid_map, script path) documented under "Channels (QUALITY 90)" (`score-scrub-arm-r44.py:47-50`) and the new statfs/cwd channels I measured are all genuinely open, but for **this** counter they are only useful to *select* real logic; they cannot substitute for it (see F2).

**F2 — no hollow variant passes: the 16-case draw + wired + selftest force the full three-path reader.** Random per-run fsids, speeds, readability and names (and the 9 selftest fixtures) mean every canned or partial answer mismatches at least one case:
- V6 (fixture-literal gate) fails 10 cases: the literal gate fires only when a *readable* record exists, so unreadable/record-free cases fall to the constant (`score-V6…`: wrong ids `root-records-unreadable, progress-socket, limited-devices, speed-malformed, speed-unreadable, dir-unreadable, dir-not-directory, timers-enabled, timers-unreadable, wrong-types`); note `wrong-types` also timed out. Record content is never part of the oracle, so content literals are useless as a channel.
- V8 (sysfs-blind) fails exactly the four cases whose expected line depends on devinfo speed reads (`limited-devices, speed-malformed, speed-unreadable, mixed`) — proving the `scrub_speed_max` reads are forced.
- V9 (V constant) passes only `none-dir-absent` (1/16); V10 (real only in selftest) also 1/16, proving the N/W legs (not the selftest) are what force real logic in the namespace.
- The 16-case *order* is not observable (mounts are static across cases; only contents change), so an order-keyed lookup would have to read the contents anyway — equivalent to the real arm. Env shape cannot separate harness from live (clean_env drops only `TSUKUROI_*`/`UFO_*`/`TMPDIR`, leaving nothing unique); it only separates selftest from the rest via the override variables.
- V7: a 36-line comment-free faithful rewrite (vs ~74-line authored body) PASSes, showing the counter scores behaviour, not implementation shape.

**F3 — declared kill rule "the arm writes or creates a file in live mode" is not implemented in the frozen counter.** The counter's `run()` (`score-scrub-arm-r44.py:532-632`) never checks for writes/creates: no open-path scan, no before/after host-state comparison, no check of the census process's opened files. The before/after receipts (`before/c1-before.jsonl`, `after/c1-after-ab8aae1.jsonl`) record only the counter's JSON and lane branches — no host state. The other declared kill rules ("a PLANE line, the rollup line or the census exit code changes between base and measured revision", "predecessor storage counters FAIL") are likewise absent from the counter itself; they are delegated to sibling wave-1 seats (`C1ExecPlaneDiff`, `C1ExecPriorCounters`). So the *counter* alone does not enforce the declared kill rules; the "no file in live mode" rule has no enforcement seat visible in `make-w1-spec.py` (it appears only as a host-guard instruction). Evidence: `grep -n "open(\|creat\|touch\|kill\|KILL" tools/score-scrub-arm-r44.py` → only the harness's own writers (lines 89, 125, 546) and no kill-rule code.

## Comparison with declared controls

- K7 (`controls/C1-K7.jsonl`): mount-gated, real-in-namespace, const-on-live scored `correct=16, live_agree=1, wired_ok=1` and failed **only** the selftest (`st_pass=0`, 8 selftest failures). V1 is exactly K7 plus a selftest branch (override env detected → real logic), which closes K7's one gap and scores full PASS. K7's recorded status ("recorded" as the control battery's expectation) is confirmed.
- V9 reproduces K1 (constant emitter): correct=1, FAIL — consistent.
- All other control mutations (K2/K3 env/uid-gated, K4/K5/K6 count-only/no-orphan/tmp-as-record, K10-K13) remain scored in `battery-summary-c1.jsonl`; none passed, and no new hollow channel emerged.

## Milestone assessment

"Pass without the arm" is **not achievable** with any tested channel: the cheapest passing census is behaviourally the full three-path reader (V7 demonstrates a compact rewrite passes). The only piece a passing variant can drop is the *live-host read* (F1), and the only unchecked kill rule is the live-mode file-creation ban (F3). Both are counter defects to record; neither lets a do-nothing arm through today.

## Evidence index (all under `w1/C1CritEvasion/`)

- `score-V1..V10-*.json` — per-variant full counter JSON (wrong-item lists, live blocks, selftest lines).
- `diff-V1..V10-*.txt` — exact probe-body diffs vs `ab8aae1`.
- `battery-summary-c1crit.json` — condensed table (also in this report).
- Commands: `python3 tools/score-scrub-arm-r44.py --revision <sha> --scratch /fast/scratch/hyaku/tsukuroi-r44/C1CritEvasion/s --lane <clone>`; clone toplevel asserted before each commit; counter hash verified as above.
- Nothing was created or modified outside the seat receipt dir and scratch; scratch (`/fast/scratch/hyaku/tsukuroi-r44/C1CritEvasion/`) was removed after copying receipts.
