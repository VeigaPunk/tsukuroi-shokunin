VERDICT: supports

# C1CritFinal — C1-F5: attack C1 as landed at 8acf0b022586a0f3164c77659fb96ba5f90949b6

Scope: `tools/boot-chain-audit.sh` diff `6951ead90566b2d74f7c45b4efca29246badad64..8acf0b022586a0f3164c77659fb96ba5f90949b6` read line by line; frozen counter `tools/score-bootinputs-r43.py` (sha256 `886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f`, matches declared); kill rule both clauses; axis fairness vs open channels (K7) and counter gaps. All runs used the frozen counter copied into scratch (`--scratch` passed), a scratch fixture clone of the lane (origin removed, `rev-parse --show-toplevel` asserted before any commit — none was made), and scratch TMPDIR. No lane file was edited/created beyond this report and the receipt dir below; no git/jj mutation in the lane; no host mutation; no tool installs.

## 1. The diff (base → tip), line by line

`git diff 6951ead..8acf0b -- tools/boot-chain-audit.sh` has exactly three hunks (receipt `repro-fix.log` plus the scope receipt; full hunk text captured from the repo in scratch):

1. `@@ -462,0 +463,14 @@` — new helper `inputs_newer_than()` (tip 463-475):
   `hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)`; then `[ -n "$hit" ]` → `printf '1\n'` else `printf '0\n'`. Decision is exclusively on find's stdout; find's exit status is never consulted, so `set -o pipefail` (tip 139, unchanged from base) cannot mask a listed match. `2>/dev/null` matches base's suppression. No environment, namespace, mount-table, uid_map, path-, cwd-, stdin- or identity-conditional anywhere in the helper.
2. `@@ -480 +494 @@` and `@@ -482,6 +496 @@` — `boot_inputs_newer()` production path (tip 494-496) now calls `inputs_newer_than "$btime"` with the **same eight start points in the same order** as base (`/etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d /etc/default/limine /etc/limine-snapper-sync.conf /usr/lib/initcpio /usr/lib/modules`). The `fixture_mode` branch (`$BOOTCHAIN_FIXTURE`) is byte-identical to base and predates the change; it is the only conditional external-input branch in the function and is not part of this diff.
3. `@@ -1215,0 +1225,16 @@` — `run_selftest()` gains four `R43-C1-*` `st_check` cases (tip 1231-1239): `missing-start-point-none-newer` (0), `missing-start-point-deep-newer` (1), `all-present-deep-newer` (1), `missing-start-point-silent` (0).

Impl→tip (`717b716a..8acf0b`) differs only by the fourth case (`missing-start-point-silent`, added at w1 integration `9b974f2a`) — `git diff 717b716a..8acf0b -- tools/boot-chain-audit.sh` shows exactly that two-line addition. The declared surface ("helper inputs_newer_than decides on find's output; four R43-C1-* selftest cases; selftest 45 → 49") matches what moved exactly.

## 2. No namespace-trace gating in production code

Full-file greps (tip blob) for `unshare`, `/mnt`, `mountinfo`, `uid_map`, `TSUKUROI_`, `UFO_`, `TMPDIR`, `ENV`, `BASH_SOURCE`, `id -u` show no reference from any production function to those channels; the only environment-sensitive production branch is the pre-existing `fixture_mode` (`[ -n "$BOOTCHAIN_FIXTURE" ]`, tip 205 — present identically at base 205). The 16-case N leg therefore runs the real production bytes; nothing in the landed code can detect it is inside the counter's namespace.

Independent behavioral reproduction (scratch, under `set -uo pipefail`, `repro-fix.log`):

```
NEW-HELPER missing-first+none-newer -> 0 (want 0)
NEW-HELPER missing-first+deep-newer -> 1 (want 1)
NEW-HELPER all-present+deep-newer -> 1 (want 1)
NEW-HELPER missing-first+silent -> 0 (want 0)
BASE-PIPE missing-first+deep-newer -> 0 (want 1, base masked -> 0)
```

The declared defect reproduces on the base pipeline (missing start point before a newer input → find exits 1, `grep -q .` match masked by pipefail → 0) and the fix closes it (1).

## 3. Declared conjuncts at tip — verified by my own counter run

`python3 tools/score-bootinputs-r43.py --lane <fixture> --revision 8acf0b022586a0f3164c77659fb96ba5f90949b6 --scratch <scratch>` (receipt `counter-tip.jsonl`), exit 0:

```
{"btime": 1793027300, "cases": 16, "correct": 16, "identity": ["1000","1000","1000"],
 "identity_ok": 1, "live": {"expect":"0","got":"0","rc":0}, "live_agree": 1,
 "selftest_pass": 1, "selftest_line": "TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=49 failed=0",
 "selftest_r43": 4, "verdict": "PASS", "wrong": []}
```

Every predicate conjunct holds: 16 cases, 16 correct, identity_ok 1, live_agree 1, selftest_pass 1 (total=49), selftest_r43 4 ≥ 2. Live leg agrees with the host oracle (no /etc or /usr input newer than boot; `boot_inputs_newer` prints 0 under a clean `env -i`). Selftest at tip run directly: `PASS total=49 failed=0` (receipt `selftest-tip.log`). Base selftest total = 45, implementation 717b716a = 48, tip = 49 (comm `grep -cE "st_check '"` over `git show` at each revision) — the declared 45 → 49 is exact.

## 4. Kill rule — neither clause fires

Clause 1 (function scope): my base→tip hunk-to-function checker reports changed top-level functions exactly `{inputs_newer_than, boot_inputs_newer, run_selftest}`, zero non-blank out-of-scope lines, no other top-level code change. KILL-RULE-DOES-NOT-FIRE.
Clause 2 (round-42 C1 counter / census selftest regression): structurally impossible — the base→tip `tools/` change set is only `tools/boot-chain-audit.sh` + the two new r43 counters; `tools/score-size-invariance-r42.py` (round-42 C1 counter) and `tools/tsukuroi-census.sh` are byte-identical, and neither references boot-chain-audit.sh (grep: no matches). Executed anyway: round-42 counter at tip → exit 0, `invariant 10/10, ns_invariant 3/3, default_equal 1` (receipt `r42-counter-tip.jsonl`); census `--selftest` at tip → `PASS (132 cases, 132 passed, 0 failed)` (receipt `census-selftest-tip.log`). No regression.

## 5. Axis fairness and the counter gaps (K7 etc.) — fair, with the declared caveat

- The operability axis is the right frame and the "improved" reading is fair: the change is exactly the production predicate's fail-open under "missing/unreadable start point listed before a newer input". Independent host reachability was established in w1 (`C1CritAxis.md`: all eight start points exist/package-owned on this host; `/etc/fstab`, `/etc/crypttab`, `/etc/mkinitcpio.conf`, `/etc/mkinitcpio.conf.d`, `/etc/default/limine`, `/etc/limine-snapper-sync.conf`, `/usr/lib/initcpio`, `/usr/lib/modules`). The improvement is conditional on that state; without it behavior is unchanged (K9 equivalent-fix control passes, so the counter is not overfit to one implementation).
- The counter's own declared limits are real and honestly recorded in SCORECARD.md (round-43 declaration): the N leg leaves the mount-table, uid_map and script-path (`/mnt/bca-lib.sh`) channels open (QUALITY 90 "named open"); control C1-K7 (a fix gated on `tmpfs` at `/etc` in the mount table) PASSes and is recorded as that limit. Consequence: the frozen counter alone cannot distinguish a namespace-gated mimic from an honest fix — the line-by-line diff review (Section 1-2) is the load-bearing evidence, and it passes. This is a limitation of the certification instrument, not a defect in the landed code.
- Other counter gaps (documented, none flips the predicate): `selftest_r43` counts `st_check 'R43-C1-` source occurrences, not executions (at tip all four are inline unconditional calls, so the observed `PASS total=49` proves execution; fails-closed for these revs); the live oracle compares float `st_mtime > bt` (false-FAIL only, never false-PASS); the "unreadable directory" N-case approximates EACCES via the ns uid split (files created as ns-root, run as ns-uid 1000) — it discriminates (K10, the missing-point pre-filter variant, fails exactly there) but is not a literal host-equivalent unreadable tree; `channels_open` is a declared string, not a measurement.

## 6. What I did not do

- Did not re-run the whole control battery `run_controls_c1.py` (it writes control files into the lane's `controls/`; its recorded JSON is in-repo evidence and all should-fail controls failed as expected, `battery-summary-c1.jsonl`). Did not run at 717b716a (w1 seat did; tip ⊇ impl + the fourth case). Did not run `--live` audit, btrfs ioctl, sudo, or any host mutation; no installs; no lane writes beyond this report and receipts.

## Receipts (relative to lane root)

- `.ufo/waves/round-43/w2/C1CritFinal.md` — this report
- `.ufo/waves/round-43/w2/C1CritFinal/counter-tip.jsonl` — frozen r43 counter at tip (PASS, exit 0)
- `.ufo/waves/round-43/w2/C1CritFinal/r42-counter-tip.jsonl` — round-42 C1 counter at tip (PASS, exit 0)
- `.ufo/waves/round-43/w2/C1CritFinal/census-selftest-tip.log` — census --selftest at tip (132/132)
- `.ufo/waves/round-43/w2/C1CritFinal/selftest-tip.log` — boot-chain-audit.sh --selftest at tip (PASS total=49)
- `.ufo/waves/round-43/w2/C1CritFinal/repro-fix.log` — independent fail-open/fix reproduction under `set -uo pipefail`
- `.ufo/waves/round-43/w2/C1CritFinal/sha256.txt` — receipt digests
