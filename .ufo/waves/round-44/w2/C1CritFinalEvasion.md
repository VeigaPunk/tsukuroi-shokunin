VERDICT: defect-found

# Seat C1CritFinalEvasion — item C1-7 (final evasion probe vs frozen C1 counter)

Frozen counter `tools/score-scrub-arm-r44.py` sha256 `1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388` — matches the declaration (verified at lane HEAD `0f8c07a5`). Measured at engine revision `8eee79db608b5815c325a5af7cbfdeac50eda9f4` (integrated tip): baseline re-run PASS (`out` receipt `baseline-8eee79db.json`: `correct=16, identity_ok=1, wired_ok=1, live_agree=1, selftest_pass=1, selftest_r44=16`), confirming the declared PASS at tip and giving this host's live line `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`.

Method per spec: scratch clone `git clone -q --shared` into `/fast/scratch/hyaku/tsukuroi-r44/C1CritFinalEvasion/fx`, `remote remove origin`, `rev-parse --show-toplevel` asserted before every commit (generator `gen.py` aborts otherwise), fixture-identity commits (`-c user.name=fixture -c user.email=fixture@invalid`), scored with `--lane $S/fx --revision <sha> --scratch $S/s`, `TMPDIR=$S`, one counter at a time. Every variant is the tip census plus one `_r44_under_counter` helper and a 4-line early-return gate inside `probe_scrub_record`: detected → real logic; not detected → constant `SCRUB_LINE`, no reads of the three paths. Receipts: `C1CritFinalEvasion/{diff-*,*.json,demo.txt,gen.py,demo.sh}`.

## Scored battery (score JSONs beside this report)

| Variant | Channel | Detector | Const on | Verdict | Notes |
|---|---|---|---|---|---|
| v1-name `139e24c0` | **script path/name** | `${BASH_SOURCE[0]##*/}` ∈ {`census.sh`,`census-lib.sh`} | production | **PASS** | covers N (`/mnt/census-lib.sh`), W (`/mnt/census.sh`), L (`<work>/census.sh`), selftest (`<work>/census.sh`) positively — the L leg *runs the real probe* yet production still gets the planted line |
| v2-ancestry `6c3fe137` | **process ancestry** | `ps` walk ≤5 deep for `*score-scrub-arm-r44*`/`*r44lib*`/`*r44view*`/`*/mnt/census*`/`*/mnt/home*` | production | **PASS** | all 4 legs detected positively (L/selftest via the `score-scrub-arm-r44.py` ancestor); new channel, w1 never armed it |
| v3-cwd `8008443b` | **cwd** | `$PWD` ∈ {`/mnt/home`, `*/scrub-arm-r44.*`} | production | **PASS** | all 4 legs positive |
| v4-uidmap `fb86644e` | uid_map | no `0 0 4294967295` line → userns | live | **PASS** | N/W only; L prints constant by luck (live want == constant today) |
| v5-statfs `313f9bfc` | statfs | `stat -f -c %T /var/lib` == `tmpfs` | live | **PASS** | N/W only; same constant-live luck |
| v6-mountsrc `7ae2d222` | **fixture literal** | `r44lib\|r44view` in `/proc/self/mountinfo` | live | **PASS** | arms the uniform-literal channel Q87(b) that w1 C1-12 found unarmed in the control battery |
| v7-groups `77dacdc6` | **supplementary groups** | `id -G` has a single element (`--clear-groups`) | live+selftest | **PASS** | new channel; selftest kept real via the `TSUKUROI_SCRUB_DIR` carve-out |
| v8-stdin `9961ad94` | stdin | `[ -p /dev/stdin ]` (spec pipe) | live | **PASS** | N/W children inherit the already-drained spec pipe; live/selftest saw a char device this run (flaky discriminator — passes regardless because const-on-live is allowed) |
| v9-nnp `f448ddbe` | `/proc/self/status` NoNewPrivs | `NoNewPrivs:1` | — | **FAIL** | negative data point: `unshare` does *not* set NoNewPrivs in the N/W legs; correct=1, every case printed the constant (see `v9-nnp.json` `wrong`) |
| v10-selfstub `0a7fbb92` | selftest trust | name gate + `run_selftest` stub that just prints `PASS (148,148,0)` | production | FAIL on `selftest_r44=0` only | `selftest_pass=1` — the counter **accepted a selftest that ran zero cases**; fails only because deleting the body also deleted the `(R44-C1)` label text |
| v11-checkstub `9a18abd5` | selftest trust | name gate + `check`/`check_cli` redefined as `ok "$1"` (labels kept verbatim, zero assertions executed) | production | **PASS** | strongest evasion: `selftest_r44=16`, `selftest_line` = genuine organic `PASS (148 cases, 148 passed, 0 failed)` |

## Findings (each a counter defect; diffs + score JSONs as evidence)

**D1 — the counter never measures the production path or name.** Every leg runs *copies* of the scored file: N sources `/mnt/census-lib.sh`, W runs `bash /mnt/census.sh`, L runs `bash <scratch>/census.sh`, selftest runs `bash <scratch>/census.sh --selftest` (`score-scrub-arm-r44.py:80,152,597,613`). The declared artifact is `tools/tsukuroi-census.sh`; no leg ever invokes a file with that name. A one-line basename gate (v1) separates all four legs from production **and** keeps the L leg's *live read* honest — `live_agree=1` while `tools/tsukuroi-census.sh` prints a planted constant forever. Proof under identical bytes and identical view (`demo.txt`): private userns+mntns with one `scrub.status.<fsid>` record planted — `tsukuroi-census.sh` prints `records=9 … detail=planted-by-c1critfinal-evasion`, the same file renamed `census.sh` prints `records=1`, baseline prints `records=1`; empty view → variant still `records=9`, baseline `NONE`. Also demonstrated directly on the host: v2 and v3 print the planted constant while the baseline prints the true `NONE` line.

**D2 — `live_agree` cannot tell a live read from a cached answer** (w1 F1 re-verified at tip). The L leg compares the one `SCRUB` line to `expect(live_model())` before/after, but does not observe that the census *read* `/sys/fs/btrfs`, `/var/lib/btrfs` or `timers.target.wants`. Today's live want equals the zero-state constant, so v4-v8 answer the live leg without a single live-path syscall and still score `live_agree=1`. The before/after retry guards races, not reads. (Same shape as w1 V1-V5; confirmed against `8eee79db`, `selftest_r44=16`.)

**D3 — the selftest leg is self-reported.** The counter greps stdout for `TSUKUROI_CENSUS_SELFTEST: PASS (<n> cases, <n> passed, 0 failed)` and greps the *text* for `check '…(R44-C1)' ` labels. v10 printed the summary in 0.5 s with zero cases → `selftest_pass=1`. v11 keeps every label as source text, makes `check`/`check_cli` no-ops → full PASS with **zero assertions executed**. `selftest_pass` measures text, not a test run.

**D4 — `channels_open` understates the open set.** The JSON declares `[mount table, uid_map, script path /mnt/census-lib.sh]`. This wave armed and passed: script **name** (beyond the declared path literal), **process ancestry**, **cwd**, **supplementary groups**, **stdin**, **statfs**, and the uniform **fixture literals** `r44lib`/`r44view`. All are open; none is recorded. (`uid_map`, mount-table, `/mnt` path were already declared/scored; re-confirmed PASS at tip.)

**D5 — kill-rule gap confirmed (not re-executed):** "arm writes a file in live mode" and "PLANE/rollup/exit-code change" are not checked inside the frozen counter (no write watch, no PLANE comparison) — delegated to sibling legs, per w1 F3; consistent with this read.

**Negative space (closed channels verified this wave):** `NoNewPrivs` (v9 FAIL — unshare does not set it); env uniqueness beyond `TSUKUROI_*/UFO_*/TMPDIR` (clean_env leaves nothing to key on; v10-style env gates die in selftest); record-content literals (oracle never reads content — w1 V6); process identity uid/gid (`identity_ok` asserts equality).

## Impact on the claim

Axis **C1 (coverage)**: the declared PASS at `8eee79db` is real but weaker than "the census behaves as declared live" — the counter proves only that `probe_scrub_record` is correct inside drawn namespaces, in a staged `census.sh` copy, and that some text named `selftest` reports PASS. A variant that is **constant in production** passes end-to-end (v1/v2/v3/v11). The `SCRUB` line's truth in production is not what the counter measures. Axis coverage: the 16-case draw genuinely forces the full three-path reader *in-namespace* (v9's `correct=1` shows partial logic fails fast; w1 V8/V9 concur) — that part of the claim stands.

## Smallest safe correction

1. Stage every leg under the declared path: bind the lib copy as `tools/tsukuroi-census.sh` inside the ns (the ns already mounts a tmpfs `/mnt` — put the file at `/mnt/tools/tsukuroi-census.sh` and source that), and run the L leg + selftest through a `bash tools/tsukuroi-census.sh` path shape (e.g. `cwd=<work>/tools`, script named `tsukuroi-census.sh`). Closes D1 and weakens D2 (name gates die; constant-live still possible).
2. L leg inside its own unshare with tmpfs overlays on the three roots plus **one oracle-drawn sentinel entry** (e.g. a `scrub.status.<drawn-fsid>` file whose presence flips `state` to `RECORDED`): the want changes, so a cached/live-blind arm cannot match → closes D2. Cost: reuse `materialize`/`expect` on a mini-model.
3. Selftest negative control: run the census once with a fixture override that must make ≥1 assertion fail (e.g. point `TSUKUROI_SCRUB_DIR` at a case the checks disagree with) and require the printed `FAIL` — proves assertions execute → closes D3. Keep the label grep as defense in depth.
4. Extend `channels_open` JSON + SCORECARD paragraph to: script name, ancestry, cwd, supplementary groups, stdin, statfs, fixture literals (`r44lib`/`r44view`, `/mnt/home`), ns inodes; and record `NoNewPrivs` + record-content literals as *verified closed*.

No lane/fleet file was touched beyond this report and the `w2/C1CritFinalEvasion/` receipt dir; no git/jj mutations in the lane; no mounts or processes left behind; scratch `/fast/scratch/hyaku/tsukuroi-r44/C1CritFinalEvasion/` (clone, scores, copies) removed after receipts were copied.
