VERDICT: defect-found

Item C1-6 — re-probe of the seven declared mutants on the INTEGRATED arm at 8eee79db608b5815c325a5af7cbfdeac50eda9f4 (tools/tsukuroi-census.sh), scored with the frozen C1 counter and `bash tools/tsukuroi-census.sh --selftest`. 7 of 8 probes killed (one site scored twice: (b)≡(c)); **1 behaviour-changing survivor** — the literal (g) reading `btrfs-scrub@*.timer` → `btrfs-scrub@*timer`, which the w1 hardening (commit 8eee79db's `btrfs-scrub.timer` guard) does not reach. Proposed killing case below.

# Setup and integrity
- Counter verified frozen: `sha256sum tools/score-scrub-arm-r44.py` → `1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388` (matches SCORECARD). Run form: `python3 tools/score-scrub-arm-r44.py --lane <fixture-clone> --revision <sha> --scratch /fast/scratch/hyaku/tsukuroi-r44/C1MutFinal/s` (with `--lane` the scratch clone; the counter errors `cannot resolve <sha>` against the lane repo, per w1).
- Fixture: `git clone -q --shared` of the lane into /fast/scratch/hyaku/tsukuroi-r44/C1MutFinal/clone, origin removed, `git rev-parse --show-toplevel` == that dir; worktree checked out at 8eee79db (lane HEAD 3a1c6b5c is registry-only beyond the tip; census blob identical). One mutation per commit with `-c user.name=fixture -c user.email=fixture@invalid`; after each probe `git reset --hard 8eee79db` and rehash.
- Pristine census sha256 `2ef86357c14aec3f4346f7ac9013cdda3b399d38bae67f4ca2e286e5a37c4639` (git blob `8a2a665c`); verified before every probe and restored byte-identical after every probe (echoed `RESTORED_SHA` each run). Final restored-state gate: counter **PASS** rc=0 (16/16, identity_ok=1, wired_ok=1, live_agree=1, selftest_pass=1, selftest_r44=16; `restored-final.json`) and selftest `TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed, 0 failed)`.
- Baseline (pristine 8eee79db): **PASS** — rc=0, same leg greens; live leg `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0` (host read-only: no /var/lib/btrfs, no btrfs timer links).
- No tool installs or updates (RULES.md channel order not exercised; pacman paused; none needed).
- Lane untouched by me: lane HEAD still 3a1c6b5c…; the only lane-tree writes from this seat are `.ufo/waves/round-44/w2/C1MutFinal.md` and `.ufo/waves/round-44/w2/C1MutFinal/` (untracked seat set, per tasking).

# Per-mutant results (site = tools/tsukuroi-census.sh @ 8eee79db; full hunks in mut-*.diff)

| id | exact edit (old → new) | mutant sha256 / commit | counter | selftest | failing case | verdict |
|----|------------------------|------------------------|---------|----------|--------------|---------|
| a | sysfs split block (lines 2017-2021) → old single line `if [ "$rec" -gt 0 ] && [ "$sysok" -eq 0 ] && [ ! -e "$root" ]; then blocked=1; detail+='sysfs:absent,'; fi` | 6b0100ff… / cb3234c7 | FAIL rc=1, 16/16 correct, wired_ok=1, live_agree=1, selftest_pass=0 | 147/148 | "a sysfs root that exists but is not a directory is BLOCKED…" (`scrub-sysfs-not-dir`) | killed |
| b | drop `        [ -d "$e" ] && continue` (timer loop, line 2032) | 229cf9aa… / 6c5001e1 | FAIL rc=1, 16/16, wired_ok=1, live_agree=1, selftest_pass=0 | 147/148 | "a directory named like a scrub timer is not an enabled instance" (`scrub-timers-dir`) | killed |
| c | same edit as (b) — spec lists both wordings of one site | 229cf9aa… / 5e7156ab | FAIL rc=1, identical leg profile to (b) | 147/148 | `scrub-timers-dir` | killed |
| d | speed line regex `[[ $v =~ ^[0-9]+$ ]]` → `^[0-9]*$` (line 1987) | 42344e74… / 6097a9c4 | FAIL rc=1, 16/16, wired_ok=1, live_agree=1, selftest_pass=0 | 147/148 | "an empty scrub_speed_max line is malformed, never a silent no-limit" (`scrub-speed-empty`) | killed |
| e | `if ! [[ $v =~ ^0+$ ]]` → `if ! [ "$v" = 0 ]` (speed zero, line 1990) | 77376777… / 8f5dfff5 | FAIL rc=1, 16/16, wired_ok=1, live_agree=1, selftest_pass=0 | 147/148 | "a zero-padded scrub_speed_max is still no limit" (`scrub-speed-zero-padded`) | killed |
| f | `detail+=$info` → `detail=$info$detail` (line 2040) | ea9f5e62… / fdc3b3d5 | FAIL rc=1, 16/16, wired_ok=1, live_agree=1, selftest_pass=0 | 147/148 | "detail evidence precedes limit info in the detail join" (`scrub-detail-info-both`) | killed |
| g1 | glob `"$tw"/btrfs-scrub@*.timer` → `"$tw"/btrfs-scrub@*timer` (line 2029; literal (g) reading) | 9fc6c135… / 3063b8ed | **PASS rc=0** — 16/16 correct, identity_ok=1, wired_ok=1, live_agree=1, selftest_pass=1, selftest_r44=16 | **148/148 PASS** | — | **survived (behaviour-changing)** |
| g2 | glob `"$tw"/btrfs-scrub@*.timer` → `"$tw"/btrfs-scrub*.timer` (w1 mutant k reading) | d7321df3… / 6d984dfb | FAIL rc=1, 16/16, wired_ok=1, live_agree=1, selftest_pass=0 | 147/148 | "enabled scrub timer instances count by link name; the bare template and other timers do not" (`scrub-timers`, now guarding `btrfs-scrub.timer`) | killed |

(b) and (c) name the same hardened line from the spec's two phrasings; they were still probed as two separate commits and produced byte-identical mutants with identical results.

# Survivor (g1): behaviour delta proven, proposed killing case
- **Delta (constructed fixture, uid 1000, receipt `mut-g1-delta.txt`):** wants dir containing `btrfs-scrub@home.timer`, `btrfs-scrub@home-timer` (no dot before "timer"), and the bare `btrfs-scrub@.timer`; sysfs root absent, record dir empty; probe sourced census-minus-main and called `probe_scrub_record` with `TSUKUROI_BTRFS_SYSFS/SCRUB_DIR/TIMER_WANTS` overrides.
  - pristine: `SCRUB btrfs-scrub-record state=NONE dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=1`
  - mutant g1: `SCRUB btrfs-scrub-record state=NONE dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=2`
- **Why every leg is blind:** the counter's drawn timer pool (`timer_names()`, tools/score-scrub-arm-r44.py:363-366) and the drawn `wants` extras are all `@…​.timer`/`fstrim.timer`/`word.timer` forms on which both globs agree; `btrfs-scrub@.timer` matches both but the name skip catches it; the live host has no btrfs-scrub links; and the w1 guard name `btrfs-scrub.timer` (added in 8eee79db) carries no `@`, so it kills the `@`-dropping mutant (g2) but not the suffix-widening one. The selftest `scrub-timers` fixture likewise contains no `@…​timer`-without-dot name.
- **Proposed killing case (census selftest, the lane-owned surface — the counter is frozen):** in the `scrub-timers` case (census :3270-3275) add one plain file, e.g. `: > "$FX/wants/btrfs-scrub@home-timer"`, keeping the expected `… limited=0 timers=2$` line: pristine ignores the name (glob demands `.timer`), g1 counts it (`timers=3`) and goes red. Equivalently `btrfs-scrub@x-timer` in the same fixture; a counter-side fix would be adding that name to `timer_names()`, but that tool is frozen this round.

# Kill-path observations
- All seven kills rode the S leg (selftest) deterministically: in every killed run the 16 namespace cases were 16/16 correct and wired_ok/live_agree stayed 1 — the drawn namespace/W/live views never exercise a non-directory sysfs root, a timer-named directory, an empty speed line, a zero-padded zero, a flag+`speed_max` detail mix, or a non-`.timer`-suffixed `@` name. Same shape w1 reported for its draw-dependent kills; the w1 fixes live in the selftest, so the S leg is the load-bearing leg for this whole mutant class (as w1 already saw for its mutant g).
- (d) also stays draw-dependent in the counter legs (`speed-malformed` picks `'\n'`/`''` only 2/8 runs, counter :403); the single counter run here drew neither and still failed via the S leg.
- `selftest_r44=16` R44 labels counted on every run (9 ab8aae16 + 7 w1 cases), above the ≥6 predicate floor.

# Receipts (.ufo/waves/round-44/w2/C1MutFinal/)
`pristine-baseline.json`, `restored-final.json`, `mut-{a,b,c,d,e,f,g1,g2}.json` (counter JSON lines), `mut-*.diff` (exact hunks vs 8eee79db), `mut-g1-delta.txt` (survivor fixture transcript), `selftest-{pristine,restored}.txt` and `selftest-mut-*.txt` (full selftest outputs incl. failing case lines).

# Not done
- Single counter run per mutant (the frozen control battery's shape); no reruns to sample (d)'s draw-dependent namespace kill. No judgment of sibling seats' concurrent work.
