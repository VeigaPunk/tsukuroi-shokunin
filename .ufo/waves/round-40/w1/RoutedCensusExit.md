VERDICT: supports

Item R-4 (round-39 closure §6.2, last bullet): the live leg of `tools/score-storage-hidden-r39.py`
matched while recording `census_exit 2`. Three questions were asked — why the census exited 2, whether
ignoring it was intended, and whether a nonzero exit can coexist with a correct STORAGE line. Answer:
the 2 is a *six-plane rollup* verdict produced by the counter's own stripped child environment, the
STORAGE line is outside that rollup by contract, and the pairing is pinned as legitimate by the census
selftest itself. Ignoring the field as a match input is correct but is **nowhere stated** in the counter
docstring, and nothing (in this or either round-38 storage counter) ties the recorded exit to the census's
own printed rollup. That gap is the item, and the drafted decision below closes it.

## 1. What the exit code is: a rollup over six PLANE vars, with STORAGE outside it

- `tools/tsukuroi-census.sh:81-82` (header, master): "Exit map (firmware-style, plan:5): 0 HEALTHY | 1 DEGRADED | 2 BLOCKED. Usage errors also exit 2. Rollup: worst plane wins (BLOCKED > DEGRADED > HEALTHY)."
- Rank order: `rank()` `tools/tsukuroi-census.sh:589-596` (`BLOCKED) printf 2` `:593`, `*) printf 9` `:594`), `worse()` `:598-600`.
- The rollup folds exactly the six PLANE variables and nothing else — `tools/tsukuroi-census.sh:3129-3147` (master; identical block at `:3093-3111` in the `a2d7aad` census bytes I ran): `printf '%s\n' "$STORAGE_LINE"` at `:3129`, then `local roll=HEALTHY` `:3131`, six `roll=$(worse …)` lines, `TSUKUROI_CENSUS: …` printf, then `case "$roll" in HEALTHY) exit 0 ;; DEGRADED) exit 1 ;; BLOCKED) exit 2 ;; *) exit 2 ;;` `:3142-3147`.
- STORAGE is printed **before** the rollup is computed and is deliberately verdict-neutral: header `:347` "The line is verdict-neutral: no PLANE text, rollup term or exit code changes" (repeated at `:371-372`).

So `exit` is rank(worst of packages/systemd/drivers/journal/update-safety/oom). A correct STORAGE line
has no causal path into it.

## 2. Why the live leg got 2: the counter's own env removes the user bus

- Child env is two variables plus scratch paths: `CHILD_ENV_BASE = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}` (`tools/score-storage-hidden-r39.py:56`), applied at `:192` `env = dict(CHILD_ENV_BASE, HOME=str(work/'home'), TMPDIR=str(work/'tmp'))`. No `XDG_RUNTIME_DIR`, no `DBUS_SESSION_BUS_ADDRESS` — so `systemctl --user` cannot find `/run/user/1000/bus`.
- Measured, census bytes at the receipt revision (`git show a2d7aad740977088ff9fc70ed36d3ef978b27e81:tools/tsukuroi-census.sh`, sha256 `432cd5834a2de1abaf0b87cfd10581c9d6c63e2f02b11d277b9ff0f4c3d1de35`, 3113 lines), run with exactly the counter's env:
  `env -i PATH=/usr/bin:/bin LC_ALL=C HOME=<scratch>/home TMPDIR=<scratch>/tmp bash census </dev/null`
  → **exit 2**, `PLANE systemd: BLOCKED (systemctl --user unusable rc=1 [Failed to connect to user scope bus via local transport: $DBUS_SESSION_BUS_ADDRESS and $XD…])`, `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`, `TSUKUROI_CENSUS: BLOCKED (packages=DEGRADED systemd=BLOCKED drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)` — receipt `run-exact.txt:2,4,12,13`.
- Same bytes, same host, one variable added (`XDG_RUNTIME_DIR=/run/user/$(id -u)`) → **exit 1**, `PLANE systemd: HEALTHY (scope=user state=running failed=0 …)`, and the STORAGE line is **byte-identical** to the run above; rollup `TSUKUROI_CENSUS: DEGRADED (… systemd=HEALTHY …)` — `run-exact+xdg.txt:2,4,12,13`.
  So the recorded 2 tracks the environment the counter builds, not the storage reading and not host storage health.
- The other leg families reach 2 by different planes, which is the point (the value carries no storage information in any leg):
  - fixture leg F2 (overrides only, same env) → exit 2, systemd BLOCKED, STORAGE line exactly the expected `detail=mounts:btrfs-without-sysfs` — `run-f2.txt:2,4,12,13`;
  - namespace leg H1 (`unshare -rm`, tmpfs over `/sys/fs/btrfs`, `exec bash census </dev/null`) → exit 2, `PLANE journal: BLOCKED (boot target probe unusable rc=1 [Failed to connect to system scope bus via local transport: Operation not permitt…])`, systemd **HEALTHY**, STORAGE `state=BLOCKED … detail=mounts:btrfs-without-sysfs` — `run-h1.txt:2,4,6,11,12`.
- The committed receipt matches: `.ufo/waves/round-39/after/c1-final-a2d7aad.jsonl` — `grep -o '"census_exit": [0-9]*' … | sort | uniq -c` → `11 "census_exit": 2` (2 hidden + 3 views + 5 fixtures + 1 live). Every leg, not just the live one.
- Still true at round-40 tip: census at `f951f288483c1af0cef4afd458488b84cf7a2165` (sha256 `032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733`), same env → exit 2, same systemd BLOCKED line, `STORAGE … state=HEALTHY filesystems=1 devices=1 nonzero=0` — `run-tip.txt:2,4,12,13`. Round 40 touched `run_selftest` only; the live exit path is unchanged.

## 3. Is nonzero-exit-with-correct-STORAGE-line legitimate? Yes, and the selftest already freezes both directions

Not an accident of this host — it is the instrument's declared shape, pinned by the census's own selftest (119 cases at
`a2d7aad`, 124 at the round-40 tip — `grep -cE "^  check '|^  check_cli '"` on the two blobs); `check` asserts the exit code, the rollup verdict and the STORAGE regex, with the exit
assertion at `tools/tsukuroi-census.sh:2174` `bad "$label: exit $rc wanted $wrc; …"`:

- **STORAGE BLOCKED under a healthy rollup, exit 0**: 19 STORAGE cases all want `0 HEALTHY`; 13 of them want a `state=BLOCKED` STORAGE line with exit 0 (`:2951, 2957, 2962, 2967, 2973, 2981, 2986, 2991, 3001, 3006, 3015, 3023, 3041`), one wants `state=DEGRADED` with exit 0 (`:2943-2944`, label "… reads DEGRADED on the STORAGE line only; 010 is ten, not octal (R38-C1)"), five want `HEALTHY`. Counting: `19` STORAGE checks, pairings `{('0','HEALTHY','BLOCKED'):13, ('0','HEALTHY','HEALTHY'):5, ('0','HEALTHY','DEGRADED'):1}`.
- **Rollup BLOCKED, exit 2, with a btrfs-free (hence HEALTHY) STORAGE line**: 34 cases want `2 BLOCKED`. The default fixture writes a mount table with no btrfs mount (`fx_default`, `:2035`: `proc /proc … /dev/fx0 / ext4 …`), so those runs print `STORAGE … state=HEALTHY filesystems=0 devices=0 nonzero=0` under exit 2 (code read; those cases do not assert the STORAGE line). One of them is literally the live leg's cause: `:2350` `check 'blocked: systemd user bus unreachable' 2 BLOCKED '^PLANE systemd: BLOCKED .*unusable rc=1'`.
- **Already measured in the round-39 receipt, same pairing**: fixture leg `F1-absent-root-no-btrfs-mounted` records a `state=HEALTHY filesystems=0 devices=0 nonzero=0` STORAGE line beside `"census_exit": 2` and `"match": true` (`.ufo/waves/round-39/after/c1-final-a2d7aad.jsonl:91-98`, exit at `:96`), and `F4` does the same with `filesystems=1 devices=1` (`:121-128`, exit at `:126`). In that single run the counter matched exit 2 against STORAGE states `HEALTHY`, `BLOCKED` (F2/F5, hidden H1/H2) and `DEGRADED` (views 1/2) — so before the live leg that one run had already matched exit 2 against every STORAGE state it produced, and the exit was demonstrably independent of the line it was scoring.
- Distribution of wanted exits across the selftest: 55 × `0 HEALTHY`, 32 × `1 DEGRADED`, 34 × `2 BLOCKED` (`grep -oE "check '[^']*' [0-9] (HEALTHY|DEGRADED|BLOCKED)" … | sort | uniq -c`).

Corollary for the counter: a pass on the STORAGE line while the census exits 2 is the *expected* case
whenever any other plane blocks, and "exit must be 0" would have made the live leg fail on an unrelated
plane (and on any host without a reachable user bus).

## 4. Was ignoring it intended? Not recorded — and the field has no consumer anywhere

- `census_exit` appears only as a dict literal in the round-39 counter: `tools/score-storage-hidden-r39.py:209, 226, 253, 263`; `grep -nE "\[.census_exit.\]|census_exit *==|census_exit *!=" ` over that file returns nothing (exit status 1, zero matches). The predicate (`:26-29`, `:265-267`) folds only `hidden_matched`, `views_matched`, `fixtures_matched`, `live_match`, `six_planes_all`.
- Same shape in the two round-38 storage counters: `tools/score-storage-arm-r38.py:219,229`, `tools/score-storage-arm-r38-q82.py:128` — recorded, never read.
- The docstring does not mention it. Its "Exit:" line (`tools/score-storage-hidden-r39.py:32`) is about the *counter's* exit ("0 PASS; 1 FAIL; 2 could-not-evaluate (binding, git, unshare unavailable)"), and the closest sentence is `:31` "six_planes_all: every run printed exactly six PLANE lines, one STORAGE line and one TSUKUROI_CENSUS line" — i.e. the author substituted a *structural completeness* check (which does catch a census that aborts before the rollup, since such a run has no STORAGE/rollup line and fails `six_all`) for an exit check, without writing down why. Nothing in `SCORECARD.md` or `corpus/lessons/round-39.md` names `census_exit` (`grep -rn 'census_exit' SCORECARD.md corpus/lessons/round-39.md` → no hits).
- Verdict on intent: **intended in effect, unrecorded in text**. The 11/11 `2` values in the receipt show the author saw the value and shipped it as a diagnostic; no leg ever observed a 0, so the field was never exercised as a signal either.
- Residual defect (what the discount costs): `parse()` (`tools/score-storage-hidden-r39.py:149-153`) counts lines and never reads the rollup token, so a census whose `case "$roll"` block went stale, or fell through `*)` on an out-of-vocabulary rollup verdict, would be accepted by all three storage counters. That fallthrough is reachable in the current bytes, not hypothetical: `rank()` maps an unknown verdict to **9** (`tools/tsukuroi-census.sh:594`), `worse()` propagates it, and the rollup block's `*) exit 2` (`:3146`) would then print `TSUKUROI_CENSUS: <junk> (…)` and exit 2 — a line `parse()` still counts as present. And a reader of the round-39 receipt cannot tell *which* plane blocked — recovering that needed these four re-runs.

## 5. Exact proposed decision text for the round-40 lesson

> **R-4 (round-39 §6.2, live-leg `census_exit`).** The `census_exit 2` recorded while the live leg matched
> is a six-plane rollup verdict, not a storage signal, and it does not weaken the pass: the exit is
> `rank`/`worse` over the PLANE vars (`tools/tsukuroi-census.sh:589-600`) reduced by `case "$roll"` at
> `:3142-3147` with the map at `:81-82`, and the STORAGE line is printed before the rollup and is
> verdict-neutral by contract (`:347`, `:371-372`); the selftest already freezes both pairings — 13 STORAGE
> cases assert `state=BLOCKED` under `0 HEALTHY` (`:2951-3041`) and 34 cases assert `2 BLOCKED` over the
> default btrfs-free mount table (`:2035`), one of them being this very condition, `blocked: systemd user
> bus unreachable` (`:2350`). In the live leg the 2 came from the counter's own environment, not the host:
> `CHILD_ENV_BASE` passes only `PATH` and `LC_ALL` (`tools/score-storage-hidden-r39.py:56`, used at `:192`),
> so `systemctl --user` returns 1 (`Failed to connect to user scope bus … $DBUS_SESSION_BUS_ADDRESS and
> $XDG_RUNTIME_DIR are not set`) and the systemd plane blocks, while adding `XDG_RUNTIME_DIR=/run/user/1000`
> to the same census bytes flips the exit to 1 with a byte-identical STORAGE line, and the namespace legs
> exit 2 for a third, unrelated reason (journal plane, system boot-target probe not permitted inside
> `unshare -rm`). Ignoring the exit as a match input is therefore correct and must be stated in the counter
> docstring beside `six_planes_all`, which is the structural check that catches an aborted census; but the
> counter MUST consume the field in one host-independent way — parse the printed `TSUKUROI_CENSUS:` verdict
> token, require it in {HEALTHY, DEGRADED, BLOCKED}, require `census_exit == rank(token)` (0/1/2), and name
> the blocking plane in the leg receipt — because a census whose exit diverges from its own rollup is
> currently accepted by all three storage counters, and this check makes the `2` self-explaining in the
> receipt instead of costing four re-runs.

## 6. Scope, limits

- Read-only throughout the lane: no lane file created except this report and the receipts under
  `.ufo/waves/round-40/w1/RoutedCensusExit/`; no `git`/`jj` mutating command (only `git show` of two
  committed blobs into scratch); no host change; the only mount was `mount -t tmpfs` inside
  `unshare -rm`; no `pkill`; no package operation, so no install record (nothing installed).
- Not done: I did not re-run the frozen round-39 counter end to end (13 selftests, ~75 s) — I reproduced
  its four leg *shapes* individually against the same census bytes, which is what the exit question needs;
  I did not run `--selftest` (not this item's surface); I did not test the `*)`-fallthrough rollup case in
  the census, so the proposed `rank(token)` check is argued from the code path, not from a fired mutant.
- Scratch `/fast/scratch/hyaku/tsukuroi-r40/RoutedCensusExit/` removed after the receipts above were
  copied out.
- No claim here rests on a name or a comment alone: every "legitimate" pairing is either executed
  (`run-*.txt`) or frozen in an asserting selftest case (line-cited above). The intent reading in §4 is
  inference from absence of consumers plus the docstring's substitution of `six_planes_all`, and is
  labelled as such.
