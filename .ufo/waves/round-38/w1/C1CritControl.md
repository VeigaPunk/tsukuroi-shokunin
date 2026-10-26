VERDICT: defect-found — against the frozen v1 C1 counter `tools/score-storage-arm-r38.py` taken alone: a 14-line arm that opens no `error_stats` file passes it 10/10 fixtures + live + six planes, exit 0. The C1 pair as governed by the pre-seat amendment (v1 **and** q82) is **not** beaten by any control I built, and the real arm at the measured lane tip passes both. So the finding is a counter defect that the amendment's conjunct already closes, not a falsification of C1 at the declared pair.

# What I tested

Fixture discipline: one scratch clone (`/fast/scratch/hyaku/tsukuroi-r38/C1CritControl/clone`, `git clone -q --shared` of the lane, `remote remove origin`, toplevel verified) at base `5edb6c2`; each control is a `reset --hard` to `5edb6c2`, one insertion into `tools/tsukuroi-census.sh` placed *before* the `# ---- hermetic selftest` anchor (bash keeps the last `probe_storage_arm` definition, so the frozen arm bytes stay present and only the effective function changes), committed with `-c user.name=C1CritControl -c user.email=crit@example.invalid`, then scored with the lane's frozen counters read from the lane (read-only). Scratch removed at the end; receipts in `.ufo/waves/round-38/w1/C1CritControl/`.

Frozen bytes first: `sha256sum` of the lane's `tools/score-storage-arm-r38.py` = `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218` and q82 = `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3`, matching `SCORECARD.md:2117` and `:2148`; `git show 7cbaeb63:tools/score-storage-arm-r38.py | sha256sum` is the same digest and `git diff --stat 7cbaeb63..HEAD -- tools/score-storage-arm-r38.py` is empty — the counter really is frozen and unchanged since the declaration.

# Scores

| control | inserted size | what it does | v1 (`score-storage-arm-r38.py`) | q82 | census `--selftest` |
|---|---|---|---|---|---|
| real arm @ lane tip `5edb6c2` | — | reads `error_stats` per HO/contract | **PASS 10/10, live 1, six 1, exit 0** (`base.json`) | **PASS 3/3** (`head_q82.json`) | not run |
| committed one-line gate (`run-controls-q82.sh:27-33`) | 1 line | real logic only when `TSUKUROI_BTRFS_SYSFS` set | PASS 10/10 (`controls-q82.jsonl:1`) | 0/3 FAIL | **PASS 111/111** (`gated-selftest.txt`) |
| **K0 six-arm name key (cheapest algorithm-free PASS)** | **14 lines / 536 B** | keys the fixture *directory name*, opens nothing | **PASS 10/10, live 1, six 1, exit 0** (`K0_min_name.json`) | 0/3 FAIL (`K0_q82.json`) | FAIL 5 cases (`k0-selftest.txt`) |
| K1 ten-arm name key | 19 lines / 629 B | same class, one arm per fixture | PASS 10/10, live 1, six 1 (`K1_name_dispatch.json`) | 0/3 FAIL (`K1_q82.json`) | not run |
| K2 size key | 17 lines / 682 B | `wc -c` of `error_stats`, no value parse | FAIL 3/10, live 0 (`K2_size_key.json`) | not run | not run |
| K3 first line only | 18 lines / 687 B | reads line 1 of each file | FAIL 4/10, live 0 (`K3_first_line.json`) | not run | not run |
| K4 unvalidated grep | 18 lines / 685 B | counts `^[a-z_]+ [1-9][0-9]*$` lines, no schema | FAIL 3/10, live 0, six 0 (`K4_line_grep.json`) | not run | not run |

`fixtures_expected` is 10 in every v1 receipt (`.ufo/waves/round-38/w1/C1CritControl/*.json`).

## The cheapest passing control (K0)

Inserted verbatim before the `# ---- hermetic selftest` anchor (full diff `K0.diff`, commit `e3772e9` in the scratch clone):

```bash
# CONTROL K0: six-arm name key on the fixture directory digit; opens no error_stats file.
probe_storage_arm() {
  local s='HEALTHY 1 1 0' d=${BTRFS_SYSFS##*/fx/F}
  case $d in
    02*)            s='DEGRADED 1 1 2' ;;
    03*)            s='DEGRADED 1 2 1' ;;
    04*|05*|10*)    s='BLOCKED 1 1 0' ;;
    06*)            s='HEALTHY 0 0 0' ;;
    07*)            s='BLOCKED 1 0 0' ;;
    09*)            s='DEGRADED 2 2 1' ;;
  esac
  set -- $s
  STORAGE_LINE="STORAGE btrfs-device-stats state=$1 filesystems=$2 devices=$3 nonzero=$4"
}
```

It touches only the string `$BTRFS_SYSFS`; no `open`, `cat`, `read` or `stat` of any tree file. The `*)` fall-through is the host's cached live answer, which is also F01/F08's expected tuple — the six remaining arms are the information-theoretic minimum for this channel (seven distinct expected tuples, one shared with the default).

Why this channel exists: the counter hands the fixture path to the child as `TSUKUROI_BTRFS_SYSFS` (`tools/score-storage-arm-r38.py:154-160`, `env['TSUKUROI_BTRFS_SYSFS'] = sysfs`) and builds the fixtures under `work/fx/<fixture name>` with the frozen, committed names (`:84-93`, `build()` at `:96-108`). The name is therefore a stable, free signal that the counter never randomizes, and the live leg on this host has one constant answer (`base.json` live `expected ["HEALTHY", 1, 1, 0]`, from `/sys/fs/btrfs/1d02a454-…/devinfo/1/error_stats`, `filesystems=1 devices=1 nonzero=0`).

Two corroborating facts for how narrow the defect is, and for internally available evidence the counter ignores:

- Structural keying does not work: K2 (byte size) scores 3/10 with the collision visible — F02's file `write_errs 1 / corruption_errs 3` has exactly F01's 74-byte length, `exp ['DEGRADED', 1, 1, 2] got ['HEALTHY', 1, 1, 0]` (`K2_size_key.json`). Value-distinct fixtures are invisible to shape/size heuristics.
- The census's **own** six storage selftest cases already reject K0: `bash tsukuroi-census.sh --selftest` → `TSUKUROI_CENSUS_SELFTEST: FAIL (111 cases, 106 passed, 5 failed)`, the five failures being exactly the R38-C1 cases that need a non-default STORAGE tuple (`k0-selftest.txt`). The frozen counter never runs them: `subprocess.run(['bash', str(script)], …)` with no arguments (`tools/score-storage-arm-r38.py:160`).

## Why the pair still holds

- q82 rejects both bypass classes: K0 `ns_views_matched 0/3` with `exp ['HEALTHY',3,4,0] / ['DEGRADED',3,6,12] / ['DEGRADED',3,5,6]` against three identical `got ['HEALTHY',1,1,0]` (`K0_q82.json`); K1 likewise 0/3 (`K1_q82.json`). The committed one-line gate is also 0/3 (`controls-q82.jsonl:1`).
- The real arm at the measured tip passes both: v1 `fixtures_matched 10, live_match 1, six_planes_all 1, result PASS, exit 0` (`base.json`, 34 s) and q82 `ns_views_matched 3, ns_available 1, PASS exit 0` (`head_q82.json`, 10 s).
- The cheap v1-side patches I could have proposed are individually insufficient, measured: randomizing the fixture directory name kills K0 (same F02 tree under `fx/F0a91f3c07d` → `STORAGE … state=HEALTHY filesystems=1 devices=1 nonzero=0`, expected `DEGRADED 1 1 2`) but not the one-line gate, which keys on `${TSUKUROI_BTRFS_SYSFS+x}` and is name-blind (`run-controls-q82.sh:31`); adding a `--selftest` conjunct kills K0 (5 failing cases above) but not the one-line gate, which keeps the real arm under fixtures and therefore passes the selftest 111/111 (`gated-selftest.txt`; the selftest sets `TSUKUROI_BTRFS_SYSFS="$FX/btrfs"`, `tools/tsukuroi-census.sh:2125`). Only the no-override production path separates them.

# Impacted axes

Coverage (C1) only, and only for a closure that admits C1 on the v1 sentence of `SCORECARD.md:2117` alone. Under the amendment's added kill rule (`SCORECARD.md:2142-2152`) C1 is unaffected: both cheap PASSes die on q82, and the real arm passes both counters at the same revision.

Separate robustness note, not an exploit: `tools/score-storage-arm-r38.py:215` withholds credit for F10 when `os.geteuid() == 0`, while the predicate requires `fixtures_matched == 10` (`:230`), so C1 is unpassable by construction if any scoring run is root (this host's seat runs as uid 1000 — `id -u` → 1000 — so the branch was not exercised here).

# Smallest safe correction

No counter edit, no claim edit. Fix the C1 admit rule's wording so the q82 conjunct is not separable from the v1 PASS (it is already frozen in the amendment; the correction is to carry it into the closure text verbatim):

> C1 admit text: C1 is verified only when, at one and the same measured revision `<REV>`, both pass with exit 0 — `python3 tools/score-storage-arm-r38.py --revision <REV>` (`fixtures_matched == 10`, `live_match == 1`, `six_planes_all == 1`) **and** `python3 tools/score-storage-arm-r38-q82.py --revision <REV>` (`ns_views_matched == 3`, `ns_available == 1`). The v1 counter alone is gameable by at least two disjoint controls (a 1-line env-presence gate with the real algorithm behind it: `controls-q82.jsonl:1`; a 14-line, six-arm, zero-open fixture-name key: `.ufo/waves/round-38/w1/C1CritControl/K0_min_name.json`), and no v1-side patch tested closes the env-presence class (randomized fixture names and a `--selftest` conjunct each kill only the name-key class). No finder may be credited on v1 evidence alone.

# What I did not do

- I did not exhaustively search the space of cheap emitters; I stopped when a class was shown (name key) and when the structural classes failed (size, first-line, unvalidated grep). A control keyed on, e.g., fixture file mtimes was not built.
- q82 was run once per control (3 views, one random seed per run); K0's three observed views all mismatched, and its output is constant, so repeat runs cannot improve its score, but this was not sampled repeatedly.
- K2/K3/K4 were scored with v1 only; q82 was not run on them since they already fail v1.
- The one-line gate's `--selftest` result was measured on a scratch copy of the tip census with that gate inserted (`gated-selftest.txt`), not on the committed control commit itself (which is not in the clone; `run-controls-q82.sh` reproduces it at `52ffd65`).
- I did not run the lane's own after-receipts or the real arm's `--selftest`; only the tip q82/v1 PASSes above.
- No tool was installed or upgraded; no pacman, service, sysfs or `/etc` mutation; the lane was read only through `git show`/`rev-parse`/`log`/`diff`/`sha256sum`.

# Receipts

`.ufo/waves/round-38/w1/C1CritControl/` — `base.json` (real arm v1), `head_q82.json` (real arm q82), `K0_min_name.json`, `K0_q82.json`, `K0.diff`, `K1_name_dispatch.json`, `K1_q82.json`, `K1.diff`, `K2_size_key.json`, `K3_first_line.json`, `K4_line_grep.json`, `k0-selftest.txt`, `gated-selftest.txt`, `cands/*.sh` (the four inserted snippets plus K0), `drive.py` (harness), `commands.txt` (reproduction).
