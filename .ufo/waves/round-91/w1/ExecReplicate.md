# ExecReplicate — C1 clean-room replication, round 91 w1

**Lane revision measured (clone time):** `b516d6ae13ec0bba3ef89589ac1cac86f73a9632`
(`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` at start).
Lane drifted during replication: current tip at scoring time `2d7e09e1` (lesson+receipts;
gate file changed by `45ae6518` after clone). Both tips measured — see Step 2b.

**Axes:** operability (C1 counting command must replicate 82/82 ×3) + freshness (battery/manifest pins intact).
**Relevant deviation from spec context:** spec named candidate `ce89df93…` and freeze `d3b0987d…`;
clone HEAD is `b516d6ae` which contains both (ce89df93 = r90 gate, d3b0987 = freeze commit).
Battery sha256 `655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9` matches
lane file; landed gate at clone `dfc63548ddf06492e7667465cda0d249a3b12346246cbeb8759a6c0918ab139d`,
after `45ae6518` `62bb06c997fb99a9fd811ec97440eebe2dafa7e63c4f21f43aa0ead9af7da737`.

## Step 1 — clone battery (--runs 3) — PASS
```
$ git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$S/lane"   # rc=0
$ git -C "$S/lane" rev-parse HEAD   # b516d6ae…
$ cd "$S/lane" && sha256sum -c .ufo/waves/round-91/before/freeze-manifest.sha256  # rc=0, all OK
$ cd "$S" && python3 "$S/lane/tools/limine-pin-battery-r91.py" --gate "$S/lane/tools/check-limine-pins.py" --runs 3 --work "$S/work" --json "$S/c1.json"
rc=0
families_passed 82/82 verdict met failed -
families_passed 82/82 verdict met failed -
families_passed 82/82 verdict met failed -
```
`c1.json`: 3 runs, `families_total 82, families_passed 82, failed_families [], cases 328, verdict met` each.

## Step 2 — canonical lane read-only (--runs 3) — PASS
```
$ python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/limine-pin-battery-r91.py --gate /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py --runs 3 --work "$S/work2"
rc=0
families_passed 82/82 verdict met failed -  (×3)
```
(Step 2 log `step2-canonical.log` = the three lines above, verbatim.)

## Step 2b — current tip (2d7e09e1, gate sha 62bb06c9) canonical rerun — PASS
```
rc=0
families_passed 82/82 verdict met failed -  (×3)
```
Lane tip moved mid-wave (b516d6ae → 2d7e09e1) but the post-freeze gate fix `45ae6518`
also reads 82/82 ×3. Current-tip canonical verdict is met; the L1 should score against
whichever tip it pins — both recorded here.

## Step 3 — selftests
### 3a gate --selftest — PASS 25/25 (rc=0)
```
ok PASS rc=0 [(2, 'OK', 'none'), ('on_panic', 'menu')]
… (all 25 cases PASS, verbatim in receipt step3-gate-selftest.log)
selftest PASS 25/25
rc=0
```

### 3b battery --selftest --reference — PASS 18/18 (all legs PASS)
Seat spec expected 17/17; measured battery code yields 18 legs
(1 roster + 4 negative gates + 1 reference + 12 lies — `LIE_KINDS` has 12 entries).
```
roster-literal     PASS families_passed=82
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
reference-gate     PASS families_passed=82
lie-exit-code      PASS families_passed=3
lie-rc-field       PASS families_passed=3
lie-line           PASS families_passed=3
lie-consequence    PASS families_passed=71
lie-status         PASS families_passed=61
lie-verdict        PASS families_passed=77
lie-entry          PASS families_passed=3
lie-panic-line     PASS families_passed=63
lie-panic-value    PASS families_passed=63
lie-on-panic       PASS families_passed=2
lie-bad-resource   PASS families_passed=75
lie-missing-panic  PASS families_passed=64
selftest PASS 18/18
```
The 17-vs-18 delta is a spec-text stale count vs the battery's actual leg count
(`1+4+1+len(LIE_KINDS)=18`); the battery's own printed total is 18/18, not a silent miss.
Reference leg verified `full=True` (CASES_PER_FAMILY=4 over all 82 roster families).
Note: battery selftest takes ~10–20 min wall under w1 fleet load (18 full battery legs);
direct 300 s/600 s tool calls time out — it was run detached and its output captured verbatim.

## Step 4 — guards and controls
### --runs 0 / --runs -1 — PASS (exit 2 both)
```
$ python3 …/limine-pin-battery-r91.py --gate …/check-limine-pins.py --runs 0
usage: limine-pin-battery-r91.py [-h] …   # runs0 rc=2
$ python3 …/limine-pin-battery-r91.py --gate …/check-limine-pins.py --runs -1
usage: limine-pin-battery-r91.py [-h] …   # runs-1 rc=2
```

### Controls (single run each, battery --runs 1) — all unmet with expected killers
Index: `.ufo/waves/round-91/before/controls/gates/INDEX.tsv`
| Control | Output (verbatim) | Expected killer | Match |
|---|---|---|---|
| `K2-landed-adapter` | `families_passed 0/82 verdict unmet failed ALL-PIN-KEYS,…` rc=1 | "r91 families" / do-nothing + on_panic always menu | ✓ unmet (0/82) |
| `N03-no-first-line-exception` | `families_passed 81/82 verdict unmet failed FIRST-LINE-ENTRY` rc=1 | FIRST-LINE-ENTRY | ✓ exact |
| `N05-no-unverified-field` | `families_passed 2/82 verdict unmet failed ALL-PIN-KEYS,…` rc=1 | UNVERIFIED-IMAGE / -MIXED / -NON-EFI / -IMAGE-PATH / -SORTED | ✓ unmet (2/82; truncated lines consistent) |
| `N06-unverified-includes-pins` | `families_passed 6/82 verdict unmet failed ALL-PIN-KEYS,…` rc=1 | UNVERIFIED-MIXED | ✓ unmet (6/82) |

## Matches / deviations vs SCORECARD "Round 91 — declaration"
- **Matches:** 82/82 ×3 in clone and canonical; freeze manifest `sha256sum -c` rc=0;
  gate selftest 25/25; battery selftest all legs PASS; `--runs 0/-1` exit 2; K2 + 3 N-controls unmet with named killers.
- **Deviation 1 (spec stale count):** Step 3 expected 17/17; battery selftest code runs 18 legs
  (12 lies, not 11 — `LIE_KINDS` = exit-code, rc-field, line, consequence, status, verdict,
  entry, panic-line, panic-value, on-panic, bad-resource, missing-panic) and reports 18/18. All legs PASS.
- **Deviation 2 (lane tip moved):** clone was taken at `b516d6ae` (wave-w1-spec commit, contains candidate+freeze);
  lane advanced to `2d7e09e1` during replication (`45ae6518` changes the gate). Current tip also 82/82 ×3 —
  recorded as Step 2b so the L1 can pin either.
- **Deviation 3 (declaration family count):** declaration table text says "78 families"; the battery's
  `FAMILY_ROSTER` is 82 and both runs report `82/82`. The 82 is the measured one; seat context's 82/82 is correct.

## Receipts
`.ufo/waves/round-91/w1/ExecReplicate/`: `step1-clone.log`, `step2-canonical.log`,
`step2b-canonical-current.log`, `step3-gate-selftest.log`, `step3-battery-selftest.log`,
`manifest.log`, `c1-clone.json`.

## Tooling
No tools installed/upgraded (none needed).

Report: `.ufo/waves/round-91/w1/ExecReplicate.md`
