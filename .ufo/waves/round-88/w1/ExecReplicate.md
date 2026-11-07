# ExecReplicate — r88/w1 — clean-room replication of C1 and the freeze controls

axes: operability (assurance arm of the `limine-pins` gate) + freshness (host operability/repair)
seat: executor, leaf (no subagents spawned)
lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` = `1fac4195243e55e7d9d8a2eddd653443d8559bff`
clone measured: `git clone --shared` under `/fast/scratch/hyaku/tsukuroi-r88/ExecReplicate/lane`, `git rev-parse HEAD` = `5b98ca98c9a19641e77832bc57579d95fa5571a3` (candidate), `git rev-parse --show-toplevel` = `/fast/scratch/hyaku/tsukuroi-r88/ExecReplicate/lane`
receipts: `.ufo/waves/round-88/w1/ExecReplicate/` (this seat dir; listed with digests in §7)

Nothing in the lane, the fleet root or the host was written: the counter writes only `--scratch` and `--json`, both under my scratch/wave dirs.
No `sudo`, no `/boot`, `/efi`, `/etc`, `/usr`, `/var` write, no pacman, no tool installed.

## 1. Freeze verification (claim-void gate)

In the clone at `5b98ca98`:

```
$ sha256sum -c .ufo/waves/round-88/before/freeze-manifest.sha256
tools/battery-discrimination-r88.py: OK
tools/limine-pin-battery-r87.py: OK
.ufo/waves/round-88/before/roster/_lib.py: OK
… (48 roster entries) …
.ufo/waves/round-88/before/controls/bat-roster-oracle.py: OK
RC=0        # 57/57 lines OK, 0 FAILED
```

Counter digest agrees with the freeze (`7d2073dfd120c8ac5ebaf8c68e7c270f970b5c7a75850561d7ceb9db76c13305`, matching `master:tools/battery-discrimination-r88.py`).
Roster: 48 gates = 3 POSITIVE / 45 NEGATIVE, `roster_sha256` `1e2dcc8bab709b99dfdb62fad1b123fe3cd3fab4fc542e782b8a20489a95ae8c`.
Battery under test: `ab6c1b33f84dd252979296d1b56ccea8c5e89af221e02e1ec08ef8e579fac374` (identical at `5b98ca98` and at `master`).

## 2. C1 counting command — MET (3/3 runs)

```
$ cd /fast/scratch/hyaku/tsukuroi-r88/ExecReplicate/lane      # HEAD 5b98ca98, candidate
$ python3 tools/battery-discrimination-r88.py --battery tools/limine-pin-battery-r88.py \
      --runs 3 --jobs 4 --scratch "$S/work" --json <wave>/ExecReplicate/c1.json
run 1 positives 3/3 negatives 45/45 failures -
run 2 positives 3/3 negatives 45/45 failures -
run 3 positives 3/3 negatives 45/45 failures -
verdict met
RC=0                      # 2026-11-06T21:00:18-03:00 .. 21:05:33-03:00, wall 314 s
```

`c1.json`: `verdict met`, `counter_sha256 7d2073df…`, `roster_sha256 1e2dcc8b…`, `battery_sha256 ab6c1b33…`, `failures []` in every run.
The C1 predicate sentence is reproduced verbatim from `tools/battery-discrimination-r88.py:3-9` and the declaration table.

## 3. Battery selftest — PASS 14/14

Run from cwd `$S` (scratch, i.e. outside the lane), not from the lane:

```
$ cd /fast/scratch/hyaku/tsukuroi-r88/ExecReplicate
$ python3 lane/tools/limine-pin-battery-r88.py --selftest
roster-literal     PASS families_passed=38
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
reference-gate     PASS families_passed=38
lie-exit-code      PASS families_passed=2
lie-rc-field       PASS families_passed=2
lie-line           PASS families_passed=2
lie-consequence    PASS families_passed=31
lie-status         PASS families_passed=36
lie-verdict        PASS families_passed=35
lie-entry          PASS families_passed=2
lie-panic-line     PASS families_passed=25
selftest PASS 14/14
RC=0
```

## 4. Freeze-control replication — 5 of 6 reproduce, 1 does not

Each re-run once (`--runs 1`, `--jobs 4`) **from the clone**, i.e. under the C1 counting-command harness, against `.ufo/waves/round-88/before/controls/controls-summary.txt`:

| control | frozen (3 runs) | my run 1 (clone) | agrees? |
|---|---|---|---|
| K1 do-nothing (r87 battery) | 3/3, 29/45 · 32/45 · 30/45, unmet rc=1 | `positives 3/3 negatives 31/45`, unmet, `RC=1` | yes (within the recorded 29-32 spread; fixture randomness) |
| `bat-always-met` | 3/3, 0/45, unmet rc=1 | `positives 3/3 negatives 0/45`, unmet, `RC=1` | yes |
| `bat-always-unmet` | 0/3, 45/45, unmet rc=1 | `positives 0/3 negatives 45/45`, unmet, `RC=1` | yes |
| `bat-digest-landed` | 0/3, 45/45, unmet rc=1 | `positives 0/3 negatives 45/45`, unmet, `RC=1` | yes |
| `bat-neg-digest-list` | 3/3, 0/45, unmet rc=1 | `positives 3/3 negatives 0/45`, unmet, `RC=1` | yes |
| **`bat-roster-oracle`** | **0/3, 0/45, unmet rc=1** ("cannot read the hidden lane") | **`positives 3/3 negatives 45/45`, verdict met, `RC=0`** | **NO** |

Verbatim, from the clone:

```
$ python3 tools/battery-discrimination-r88.py --battery .ufo/waves/round-88/before/controls/bat-roster-oracle.py --runs 1 --jobs 4 ...
run 1 positives 3/3 negatives 45/45 failures -
verdict met
RC=0
```

## 5. DEFECT D1 — the isolation clause is path-coupled: from a clean `--shared` clone the lane is NOT hidden

**Where.** `tools/battery-discrimination-r88.py:41` (`LANE = os.path.dirname(HERE)`), `:86` (`"--tmpfs", lane`), `:151` (`lane = LANE`);
control `.ufo/waves/round-88/before/controls/bat-roster-oracle.py:8` (`R = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-88/before/roster/roster-r88.json"`).

**Mechanism.** The sandbox is `--ro-bind / /` followed by one `--tmpfs <LANE>`. `LANE` is the repository that *contains the counter*. The
declared counting command runs the counter from a clean `git clone --shared`, so `LANE` is the clone and only the clone is masked; the canonical
lane at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` stays readable read-only, roster and labels included. The oracle control resolves
the roster through that absolute path, so it answers every gate correctly.

Three measurements pin the mechanism (same control file, same counter bytes):

| counter run from | masked path | oracle reads | rc |
|---|---|---|---|
| clone (candidate `5b98ca98`) | clone only | `positives 3/3 negatives 45/45` met | 0 |
| canonical lane (read-only run; writes only to my scratch/wave dirs) | canonical lane | `positives 0/3 negatives 0/45` unmet | 1 |
| clone + proposed patch | clone **and** canonical lane | `positives 0/3 negatives 0/45` unmet | 1 |

The frozen receipt itself shows which layout produced it: `bat-roster-oracle.receipt.txt` line 4 records `--battery .ufo/waves/round-88/before/controls/bat-roster-oracle.py` and its `bat-roster-oracle.json` `"battery"` field is the absolute `/home/vgpnk/...` path — i.e. the freeze controls were measured from the canonical lane, the only layout in which the oracle's hardcoded target is masked. Its `got` fields are all
`error:json FileNotFoundError … '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-88/before/roster/roster-r88.json'`.

**Consequence for the claim.** C1's measured arm (§2) is unaffected — the battery under test reads fixtures, not the roster, and reads 3/3 + 45/45 ×3 in both layouts. But the declaration's isolation sentence ("inside a sandbox that hides the lane repository") and the controls column ("roster-label oracle 0/3, 0/45 ×3 … cannot read the hidden lane") are **not reproducible under the counting command they are stated for**: a roster-reading battery passes C1 from a clean clone. The receipt also records no masked path, so a reviewer cannot see from the JSON what was hidden.

**Proposed patch (not applied; L1 decides).** `.ufo/waves/round-88/w1/ExecReplicate/patch-isolation-hide-origin.diff`
(sha256 `72644147d46642f6f1f01b3da80d557526e6122a3e48414d701e5c04fc15a7bb`, 106 lines, applies cleanly with `patch -p1`; patched file sha256
`a772abebb2e38135dde0b7b1bd427fc7b32ee7aa111539099fe86e0abb50fe55`):

- `hidden_paths(lane, extra)`: mask the lane **plus every repository this lane is a `--shared` clone of**, read from `.git/objects/info/alternates`
  (a shared clone's `alternates` names `<origin>/.git/objects`; the origin worktree is what leaks);
- `one()` emits one `--tmpfs` per hidden path instead of the single `lane`;
- `--hide PATH` (repeatable) for clones that are *not* shared (a `git clone` without `--shared` has no `alternates`, so the origin path has to be named);
- the receipt gains `"hidden": [...]`, so every run states exactly which paths were masked.

**Patch validation (both directions, patched counter in a scratch copy of the clone):**

```
$ cd lane-patched && python3 tools/battery-discrimination-r88.py --battery .ufo/…/controls/bat-roster-oracle.py --runs 1 ...
run 1 positives 0/3 negatives 0/45 failures N-g01-…,N-m02-…       (48 ids)
verdict unmet
RC=1                     # receipt "hidden": [lane-patched, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin]

$ cd lane-patched && python3 tools/battery-discrimination-r88.py --battery tools/limine-pin-battery-r88.py --runs 1 ...
run 1 positives 3/3 negatives 45/45 failures -
verdict met
RC=0

$ cd lane-patched && python3 tools/battery-discrimination-r88.py --battery tools/limine-pin-battery-r87.py --runs 1 ...   # do-nothing
run 1 positives 3/3 negatives 32/45 …
verdict unmet
RC=1                     # unchanged by the patch, inside the frozen 29-32 band
```

Unit probe of `hidden_paths`: no `alternates` → lane only; `alternates` → lane + origin root; `alternates` naming a non-existent path → lane only; `--hide` → union. (`python3` exit 0.)

**Residual limit of the patch (reported, not fixed).** Only the `--shared` origin is inferred; a full clone must be run with `--hide <canonical lane>`.
A battery that reads a *copy* of the roster elsewhere on the host (another checkout, a wave dir) is still outside what one sandbox can mask; the honest
fix for the claim text is to state "the lane and the repository the counter was cloned from" and to record `hidden` in the receipt, which the patch does.

## 6. Candidate vs master

```
$ git diff --stat 5b98ca98 master -- tools/limine-pin-battery-r88.py
(empty)
$ git diff --stat 5b98ca98 master
 SKILL.md | 2 ++
 1 file changed, 2 insertions(+)
```

No change to the battery, the counter or the roster after the candidate commit; `master` differs only by the `SKILL.md` registry rows in `1fac4195`.
`git show master:tools/limine-pin-battery-r88.py | sha256sum` = `ab6c1b33…` = the candidate bytes.

## 7. Receipts (this dir) and what each proves

| file | sha256 | proves |
|---|---|---|
| `c1.json` | `92ebd42c…` | C1 counting run, 3/3 × 45/45, `verdict met` |
| `c1.stdout.txt` | `646404ad…` | the three quoted run lines + rc, from the clone |
| `selftest.txt` | `9a869eaa…` | selftest 14/14 from cwd outside the lane |
| `ctl-donothing.json` / `.txt` | `0d2f8a08…` / `c426241c…` | do-nothing 3/3, 31/45, unmet |
| `ctl-oracle.json` / `.txt` | `85b237d7…` / `7e6d846b…` | oracle reads **met** from the clone (D1) |
| `ctl-oracle-from-original-lane.json` / `.txt` | `4de4674d…` / `1ce2ea26…` | same control from the canonical lane reads 0/3, 0/45 (mechanism) |
| `ctl-bat-always-met.json` / `.txt` | `d30db6d6…` / `2eee7505…` | 3/3, 0/45 unmet |
| `ctl-bat-always-unmet.json` / `.txt` | `e0ba187c…` / `5c9ea56d…` | 0/3, 45/45 unmet |
| `ctl-bat-digest-landed.json` / `.txt` | `bfa6b663…` / `5c9ea56d…` | 0/3, 45/45 unmet |
| `ctl-bat-neg-digest-list.json` / `.txt` | `35b40dc0…` / `2eee7505…` | 3/3, 0/45 unmet |
| `patch-isolation-hide-origin.diff` | `72644147…` | proposed counter patch (D1) |
| `patch-oracle-check.json` / `.txt` | `8147e3e4…` / `1ce2ea26…` | patched counter blocks the oracle (0/3, 0/45) and records `hidden` |
| `patch-battery-check.json` / `.txt` | `1d60f198…` / `7e6d846b…` | patched counter keeps 3/3, 45/45 met |
| `patch-donothing-check.json` / `.txt` | `4b98a9f5…` / `c66fc776…` | patched do-nothing 3/3, 32/45 unmet, `hidden` = clone + canonical lane |

## 8. Refused / not run

- No host fact was needed beyond the L1's committed `host/receipt.txt` (read-only); no host command was run.
- Not run: C2 (not this seat), the non-author review, and any repair landing — reported only.
- One control (`bat-roster-oracle`) uses an absolute lane path; it cannot be re-run meaningfully from another checkout, which is D1 itself. No other
  control source contains an absolute path (`grep -n "/home/\|/boot\|/efi\|/etc" controls/*.py` → only `bat-roster-oracle.py:8`).

## 9. Lane state at exit

- `master` still `1fac4195243e55e7d9d8a2eddd653443d8559bff`; no commit, no jj/git mutation, no edit of any lane file by this seat.
- Frozen inputs intact in the **live working tree** as well as in the clone (read-only check at exit):
  `sha256sum -c .ufo/waves/round-88/before/freeze-manifest.sha256` → `RC=0`, `57/57 OK`, 0 FAILED.
- The working tree carries sibling seats' uncommitted work (`corpus/README.md`, `.ufo/waves/round-88/before/src/SHA256SUMS`, `…/URLS.txt`,
  new `…/src/limine-entry-tool-1.40.0/Main.java`, `corpus/lessons/round-88.md`); none of it is mine and none is covered by the freeze manifest.
  My only lane writes are `.ufo/waves/round-88/w1/ExecReplicate.md` and the `.ufo/waves/round-88/w1/ExecReplicate/` receipt dir.
