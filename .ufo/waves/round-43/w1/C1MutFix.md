VERDICT: defect-found
Item C1-8 — mutation testing of the R43-C1 fix (717b716a8943151ace8657e0ca23d7d9b8434f26) against the frozen
counter tools/score-bootinputs-r43.py (sha256 88f92c… family declared in SCORECARD; run as
`python3 tools/score-bootinputs-r43.py --lane <fixture clone> --revision <sha> --scratch <seat>/s`).

The counter kills the fail-open decision core of the old defect (mutants a, h; f; g; e probabilistically),
but five mutants survive, three of which change behavior on a real host: (c) stderr leak, (i) boot-second
boundary, (j) fail-open when btime is unavailable. (j) is the sharpest: a guard flipped to the fail-open
direction passes the frozen counter on every run.

METHOD
- Fixture: git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
  /fast/scratch/hyaku/tsukuroi-r43/C1MutFix/clone; remote origin removed;
  `git rev-parse --show-toplevel` == the clone dir (asserted before first commit). Mutants committed with
  -c user.name=fixture -c user.email=fixture@invalid; counter run with --lane <clone> --revision <sha>
  --scratch /fast/scratch/hyaku/tsukuroi-r43/C1MutFix/s. 32 counter invocations total, sequential.
- tools/boot-chain-audit.sh is byte-identical at 717b716, at lane HEAD 7d0ed1c2…, and in the lane worktree
  (blob 3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74; `git diff --stat 717b716 HEAD --
  tools/boot-chain-audit.sh` empty), so each mutant commit is exactly 717b716 + one change. All ten mutants
  touch only inputs_newer_than / boot_inputs_newer bodies (patches in C1MutFix/patches.txt) — kill-rule clean.
- Pristine baseline (717b716): PASS, correct 16/16, live_agree 1, selftest PASS total=48 failed=0,
  selftest_r43 3 — matches .ufo/waves/round-43/after/c1-after-717b716.jsonl. Restored-bytes leg after all
  mutants: PASS, identical JSON. Lane worktree hash identical before/after; `git status --porcelain -- tools/`
  empty throughout. Receipts: C1MutFix/runs.jsonl, C1MutFix/patches.txt, C1MutFix/probes.txt.

PER-MUTANT RESULTS (verdict = counter verdict; full JSON in runs.jsonl)
| mut | change (site)                                  | sha 12ch  | verdict | correct | wrong ids | selftest_pass |
| a   | `[ -n "$hit" ]` → `[ -z "$hit" ]`              | 1760af7a… | FAIL    | 0/16    | all 16 (every expect inverted) | 0 (3 R43-C1 selftest fails) |
| b   | drop `-quit`                                   | a1fbfb86… | PASS ×3 | 16/16   | —         | 1 |
| c   | drop `2>/dev/null`                             | 9618a467… | PASS ×3 | 16/16   | —         | 1 |
| d   | `hit=$(find …)` → `… | head -n1`               | e9e37e3c… | PASS ×3 | 16/16   | —         | 1 |
| e   | drop /etc/crypttab from production list        | 0ed22e38… | PASS 4/8, FAIL 4/8 | 16 or 15 | miss/etc/fstab-newer ×3, all-present-newer ×1 | 1 always |
| f   | drop /usr/lib/modules from production list     | 6bddc859… | FAIL ×2 | 12, 11  | multi-miss-deep-modules-newer + unreadable-dir-modules-newer always, plus k-missing/all-present draws landing on modules | 1 |
| g   | `-newermt "@$epoch"` → `-newer /proc/stat`     | 4afa7876… | FAIL ×2 | 13, 11  | k-missing/all-present/deep modules draws (mtime ≤ now never newer) | 0 (R43-C1-missing-start-point-deep-newer, R43-C1-all-present-deep-newer) |
| h   | print 1 iff find exit 0, else output test      | ab360101… | FAIL ×2 | 15/16   | all-present-older (also live_agree 0) | 1 |
| i   | own: `"$btime"` → `"$((btime - 1))"`           | 95697bf2… | PASS ×3 | 16/16   | —         | 1 |
| j   | own: btime guard `printf '1'` → `printf '0'`   | 43ec711a… | PASS ×3 | 16/16   | —         | 1 |

KILLED — WHY THE KILLS ARE REAL
- a, h: the two reintroduced decision errors are caught in-leg (a: everything inverted, live_agree 0,
  selftest 0; h: clean find exit 0 on an all-older tree prints 1 → all-present-older + live_agree 0).
  Probe (probes.txt §1): `find <missing> <old> <d> -newermt @2000 -print -quit` prints the match and exits 1 —
  -quit preserves the pending error status — which is why h's missing-point cases still answer correctly and
  only the clean-exit case kills it. The fix comment at boot-chain-audit.sh:464-466 ("decide on find's output,
  never on its exit status") is exactly what the counter enforces here.
- f: the two deterministic modules-carrier cases (multi-miss-deep-modules-newer,
  unreadable-dir-modules-newer, expect 1) are wrong on every run — a production-list omission of
  /usr/lib/modules cannot pass a single counter run.
- g: killed twice over — selftest R43-C1 deep-newer cases use fixed epochs (2000/3000; tmp files cannot be
  newer than /proc/stat's mtime = now), and N-leg expect-1 cases with drawn mtime ≤ now answer 0.
- e (probabilistic): killed only when the random draw makes /etc/crypttab the sole newer input —
  miss/etc/fstab-newer draws its carrier uniformly from the 7 points after fstab (p=1/7) and
  all-present-newer from all 8 (p=1/8); per-run kill probability 1−(6/7)(7/8)=0.25, observed 4/8.
  Counter gap (grade 2): a single green run does NOT certify the /etc/crypttab production path. Catch:
  pin one deterministic case per start point as the sole newer input (e.g. make miss/etc/fstab-newer's
  carrier fixed to /etc/crypttab, or iterate the sole-newer carrier across all 8 points in 8 cases).

SURVIVORS — COVERAGE FINDINGS
- b, d (equivalent mutants, no counter change required): removing `-quit`, or piping through `head -n1`,
  leaves stdout emptiness — the only thing the fix decides on — identical (`-quit` already caps output at
  one line; the pipefail status lands on a dead assignment under `set -uo pipefail`, no `-e`, boot-chain-audit.sh
  runs `set -uo pipefail` at :139). Real-host delta is scan cost only. Recorded for completeness; not a gap.
- c (SURVIVED; real-host behavior change → counter gap): without `2>/dev/null`, find's diagnostics
  ("X: No such file or directory", unreadable-directory errors) reach boot_inputs_newer's stderr on every
  host missing a start point; the fix suppresses them (boot-chain-audit.sh:469 at 717b716). The counter
  cannot see this: both the namespace leg and the live leg run the scored call with capture_output=True and
  read only p.stdout (tools/score-bootinputs-r43.py, INNER and live leg). Catch: in the k-missing and
  unreadable-dir legs assert `p.stderr == ''` for the scored call — that one assertion kills c.
- i (own; SURVIVED; real-host behavior change → counter gap): comparing against `$((btime - 1))` widens the
  window so an input modified during the boot second (mtime == btime) is reported "newer than boot" — a
  fail-closed false positive that downgrades a verdict spuriously. The counter is structurally blind:
  make_cases draws older() = bt−randint(3600, 30·86400) and newer() = bt+randint(60, 86400)
  (tools/score-bootinputs-r43.py make_cases), so no fixture mtime ever lands in (bt−1, bt]; the live host has
  no start-point mtime within 526268 s of btime (probes.txt §2). Catch: one N-leg case with an entry at
  mtime exactly == btime expecting "0" (strictly-newer semantics, matching oracle `st.st_mtime > bt`).
- j (own; SURVIVED; real-host fail-open → counter gap, sharpest finding): flipping the unreadable-btime
  guard from `printf '1'` to `printf '0'` (boot-chain-audit.sh:490-493 at 717b716) means a host where
  /proc/stat is unreadable/absent (hardened or recovery environment) gets "no input newer" with ZERO mtime
  evidence, and the BOOTED-OBSERVED gate (`newer = 0`) passes blind — precisely the fail-open shape the fix
  exists to close, reintroduced one branch over. No leg exercises it: btime() reads the real /proc/stat, the
  mount namespace only overlays /etc, /usr/lib/initcpio, /usr/lib/modules (INNER), and the selftest's
  R43-C1 cases call inputs_newer_than directly with tmp paths (boot-chain-audit.sh:1231-1237), bypassing
  boot_inputs_newer's guard entirely. Catch: one N-leg case mounting an empty tmpfs over /proc (same overlay
  mechanism INNER already uses) and expecting boot_inputs_newer to print "1".

BOTTOM LINE
- The declared kill rule holds for the exact defect shape it names (status-masking fail-open: a, h, g, f
  killed; e killed with p≈0.25 per run — do not certify e's path on a single green run).
- Three real-host behavior changes pass the frozen counter on every run: c (stderr noise), i (boot-second
  boundary, fail-closed), j (btime-guard fail-open). Suggested counter amendments, in priority order:
  (1) masked-/proc case expecting "1" (kills j), (2) stderr-empty assertion in k-missing/unreadable legs
  (kills c), (3) mtime == btime case expecting "0" (kills i), (4) deterministic sole-newer carrier per
  start point (makes e's kill certain). None of these change the fix; they close counter gaps only.

NOT DONE / SCOPE
- Did not run the round-42 C1 counter or the census selftest (not in this seat's item); did not verify
  mutant j's masked-/proc scenario as a live-host run (reasoned from INNER's overlay mechanism; only
  read-only probes were allowed and performed); single-host btime (1793027300) — boundary-gap arithmetic
  (i) is draw-based and host-independent, but the live-leg coincidence risk for i (a real file at
  mtime == btime) was not tested on other hosts.
- Tooling record: nothing installed or upgraded for this seat (bash/find/git/python3 all preexisting).

Restoration: lane worktree untouched (hash 3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74
before == after; status --porcelain -- tools/ = 0 lines); fixture clone and all scratch under
/fast/scratch/hyaku/tsukuroi-r43/C1MutFix/ removed after receipts were copied out (final state: path absent).
