# ConnReport connector-checks

Heading time: 02:50:13Z (`date -u +%H:%M:%SZ` immediately before this write).
Seat: `tsukuroi-r36.ConnReport`. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Base named by the assignment: `6d76fb20f6ecbc940e5c8fff36c74060c885e161`.
No tools installed. Pacman not run. Nothing deleted. No production file edited.

## Dependency

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ConnSiblings/` and `.../w1/ConnSiblings.md` were absent at 02:47:29Z, 02:48:51Z, and 02:49:32Z (`ls`, both ENOENT). No ConnSiblings table to compare. This scan stands alone.

## (1) Sibling spot scan — own `git log --oneline -3`

Repos exist: `kumitate-shokunin`, `mado-shokunin`, `kama-shokunin` under `/home/vgpnk/Projects/shokunin`.

### kumitate

```
3304a56 2026-10-23 23:44:06 -0300 round-51: w2 dispatch evidence (spec, dispatch, taskCall, registry with agentIds)
51f2ecf 2026-10-23 23:41:15 -0300 round-51: w2 spec + validated dispatch payload (32 attack seats)
7d88faa 2026-10-23 23:39:26 -0300 round-51: A2 receipts 1-2 + A3 doctored control (receipt 3 scheduled pre-close for the >=300s span)
```

Paths in those three commits: `.ufo/waves/round-51/w2-assignments.json`, `w2/swarm-registry.json`, `w2-spec.json`, `w2-taskcall.json`, `w2-validate.json`, `receipts/attest-run-2-replayed.txt`, `attest-run-2.txt`, `attest-run-2.txt.sha256`. No tsukuroi tool, no journal note.

### mado

```
317ff19 2026-10-23 20:39:01 -0300 round-28 integration: three suite-A blind-spot probes, rotated H2 set + seal, v5 boolword counter, q36 witness runner/receipts, open-ended population checker, D1-D9 record repairs, wave evidence
4f61006 2026-10-23 19:35:22 -0300 round-28: freeze registration + six-leg C1 counter + nine-defect C2 counter + controls; wave-1 spec (39 seats); round-start census exit 0
123d8cd 2026-10-23 18:55:15 -0300 round-28: pre-data counter hardening — missing artifacts fail their leg, never abort setup
```

Subject lines say C1/C2. Those are mado round-28 counters, not tsukuroi's five tools or the journalctl v262 note.

### kama

```
f129e27 2026-10-23 20:39:35 -0300 round-31: final receipts — C1/C2 at tip, C3 gate, wave-2 seat evidence, census end, independent re-runs
af6be31 2026-10-23 20:12:10 -0300 round-31 attempt 2: SCORECARD/LOG/lesson/KQ42, wave-2 evidence (44 seats), inherited receipts committed, C3 receipts
a918109 2026-10-23 20:10:46 -0300 round-31 attempt 2: meaning-cell corrections (6 rows), PROVINCE/README count corrections, dead snapshot weight removed (404 utils.hpp, two unpinned duplicate sources, duplicate c1-remap receipt)
```

Subject lines say C1/C2. The third commit is meaning-cell corrections. Not the five tools, not the journalctl rejection sentence.

### Surface tokens

HEAD `git grep -I -F` excluding `.ufo`, match counts:

| token | kumitate | mado | kama |
|---|---:|---:|---:|
| `cannot be combined with options that limit the journal` | 0 | 0 | 0 |
| `probe-child-env-allowlist` | 0 | 0 | 0 |
| `leaking_pairs` | 0 | 0 | 0 |
| `check-revision-binding` | 0 | 0 | 0 |
| `journalctl` | 0 | 17 | 0 |

`git diff --unified=0 HEAD~3 HEAD` match counts for `journalctl|leaking_pairs|probe-child-env|check-revision-binding|cannot be combined with options that limit`: kumitate 0, mado 0, kama 0.
Five tool basenames, counted 02:50:57Z, HEAD `git grep -I -F` excluding `.ufo` and `git diff --unified=0 HEAD~3 HEAD`, all 0 on kumitate, mado, and kama: `check-revision-binding.py`, `check-report-receipts.py`, `score-census-handoff-r32.py`, `mutants-btrfs-space-r30.py`, `run-receipt.py`.

`GIT_CONFIG_NOSYSTEM` in that same last-3 diff: kumitate 0, mado 3, kama 0.

Mado's three last-3 hits:

- `.ufo/waves/round-28/w1-spec.json` and `w2-spec.json`: the string sits inside added seat-prompt JSON (ExecQ36Runner), not a tool change.
- `quality/q36-successor-run.sh` (new file in that window), quoted from the diff:

```
export HOME="$WORK/home" GIT_CONFIG_NOSYSTEM=1 GIT_OPTIONAL_LOCKS=0
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR GIT_CONFIG_GLOBAL GIT_CONFIG_COUNT GIT_CONFIG_PARAMETERS
```

That is a scrubbed git env for mado's q36 runner. It is not `os.environ.copy()`, not `leaking_pairs`, and not one of the five tsukuroi tools.

Mado's 17 HEAD `journalctl` lines are outside the last-3 window. Files: `corpus/knowledge/config-health-report-r3.md` (5), `idle-lock-route-r17.md` (2), `walker-route-r18.md` (1), `corpus/README.md` (1), `plans/round-4-record-draft.md` (2), `reports/r11-ver-m11.md` (2), `SKILL.md` (3), `tools/mado-tripwire.py` (1). They are `journalctl --user` / hypridle probes or a live-probe denylist (`LIVE_PROBE_BINS = {"journalctl", ...}`). None is the v262 `-F`/`-N` rejection sentence (that token's count is 0).

### Pickaxe trap (do not use for this window)

`git log -3 -S GIT_CONFIG_NOSYSTEM` is not "among the last three commits". On kumitate it returned `4e4f471` (round-48), `ce9aee5` (round-48), `8de35e7` (round-47). Those hashes are not in `git log -3` (`3304a56`, `51f2ecf`, `7d88faa`). The same command on mado returned `317ff19`, `4f61006`, and `b6650d5` (round-27, outside the tip three). On kama it returned `6de225c`, `d8bf180`, `1471f67` (rounds 29–27), not `f129e27` / `af6be31` / `a918109`. Window evidence below uses `git diff HEAD~3 HEAD` only.

Standing fixed-git-env outside the window (not overlap for this spot scan): kumitate HEAD has `GIT_CONFIG_NOSYSTEM` in `corpus/knowledge/agent-isolation-substrates.md` and several `scripts/*.mjs`; kama HEAD has it in lesson/test/tool files (`tools/citation-provenance.py`, `tools/error-verdict-census.py`, `tools/report-landing-audit.py`, and others). Not introduced by their last three commits.

## (2) Misroot sweep

Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain`. 32 paths at 02:47:29Z and again at 02:49:32Z. Each path: first 512 bytes, then a full read (every dirty file was ≤ 8_000_000 bytes; largest was `.ufo/watchdog.log` at 104160). Nothing deleted.

Substring `round-36` and `round 36`: 0 files, head and whole.

Content contains `tsukuroi` (case-insensitive):

| path | porcelain | bytes | in first 512B | in whole file | `round-36` |
|---|---|---:|---|---|---|
| `.ufo/watchdog.log` | ` M` | 104160 | no | yes (64 lines) | no |
| `.ufo/waves/hyaku/inline-run-20261023.md` | `??` | 3989 | no | yes, one line | no |

Every other porcelain path: neither string in the first 512 bytes or the whole file. That includes modified `SCORECARD.md` (73649 bytes, diff is one added blank line at EOF, `+` only) and `.ufo/state/tsukuroi.report-baseline`.

`tsukuroi.report-baseline` is named tsukuroi. Its content is not. Working tree (68 bytes):

```
36 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Diff against HEAD: `-22 <same digest>` / `+36 <same digest>`. `printf '' | sha256sum` at 02:49:32Z printed `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The digest is the empty-input sha256, which matches check (3): there is no report body. Other dirty baselines in the same sweep are the same shape with other round integers (`chousa` 27→37, `kama` 23→31, `kumitate` 38→51, `mado` 22→28, …). `souji` is the exception: round stays 22, digest changes to `7573fed9ec776b772f19f18c970f3e8fc5dc9ba817d19d40aa86ca4e2585269f`. These are fleet round counters, not a tsukuroi seat file.

Watchdog contradiction, not smoothed: the working tree does name this launch. Lines:

```
1086:2026-10-23T20:41:36-03:00 launch tsukuroi round=36 pgid=3491994 driver=hyaku-inline attempt=1
1101:2026-10-23T23:24:29-03:00 launch tsukuroi round=36 pgid=908597 driver=hyaku-inline attempt=1
```

The token is `round=36`, not `round-36`. First 512 bytes start `2026-09-28T15:44:59-03:00 watchdog tick` and do not contain `tsukuroi`. Uncommitted diff is `+492/-0`. An added-line filter for `tsukuroi|round-36|round=36` was truncated at 40 lines in this seat; the sample runs from `launch tsukuroi round=23` through other lanes' `round=36` lines (kake, mori). It did not show a `round-36` substring. This file is fleet driver state. It is not a copy of the five tools, the probe, or the C2 note.

Untracked `inline-run-20261023.md` line 49, whole file, not in the first 512 bytes:

```
- tsukuroi: three consecutive rejected closures through r35 (2026-10-23T15:14) — merit block.
```

Hyaku lifecycle note about r35. No `round-36`.

Untracked fleet-root files with neither string (first 512 and whole): `.omp/mcp.json`, `.ufo/state/kotoba.report-baseline`, `kotodama.report-baseline`, `revenger.report-baseline`, `AGENTS.md`, `bm.json`, `live.html`, `live_s228.html`, `nama.html`, `s395.txt` (0 bytes), `scripts/hyaku/append-closure.py.bak-20261023T040735Z`, `scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z`, `tf_bavelas.html`, `unblob.log`, `wb2.html`, `write` (25 bytes), `xc.xml`.

## (3) Report path absent

`/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/` exists. `ls -la` at 02:47:29Z showed `chousa.md`, `kake.md`, `kotodama.md`, `kumitate.md`, `mori.md`. `stat` of `.../round-36/tsukuroi.md` at 02:47:29Z and `ls` at 02:49:32Z: `No such file or directory` (os error 2). Absent, read-only, not created by this seat.
